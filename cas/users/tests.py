from django.test import TestCase
from .models import User
from urllib.parse import urlencode, urlparse, parse_qs
from xml.etree import ElementTree


class CASTestCase(TestCase):
    def setUp(self):
        self.usernames = ["testgid", "PB17110000", "SA21110000"]
        self.password = "testpwd"
        self.user = User.objects.create_user(
            gid=self.usernames[0],
            email="test@example.com",
            name="testname",
            password="testpwd",
        )
        self.user.id_set.create(id=self.usernames[1], order=0)
        self.user.id_set.create(id=self.usernames[2], order=1)
        self.service = "http://example.com/login"
        self.login = "/login"
        self.check_ticket = "/serviceValidate"
        self.cas = '{http://www.yale.edu/tp/cas}'


    def get_user_info(self):
        return {
            'username': self.user.gid,
            'password': self.password,
        }


    def test_cas_login(self):
        response = self.client.get(self.login)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.login, self.get_user_info())
        self.assertEqual(self.client.session['_auth_user_id'], self.user.gid)
        self.assertRedirects(response, self.login)
        self.client.logout()
        
    def test_cas_login_with_service(self):
        url = self.login + "?" + urlencode({'service': self.service})
        self.assertEqual(url, "/login?service=http%3A%2F%2Fexample.com%2Flogin")
        response = self.client.post(url, self.get_user_info())
        self.assertEqual(response.status_code, 302)
        query = urlparse(response.url).query
        ticket = parse_qs(query)['ticket'][0]
        ticket_check_url = self.check_ticket + "?" + urlencode({'service': self.service, 'ticket': ticket})
        response = self.client.get(ticket_check_url)
        self.assertEqual(response.status_code, 200)
        tree = ElementTree.fromstring(response.content)[0]
        self.assertEqual(tree.tag, self.cas + 'authenticationSuccess')
        attributes = tree.find('attributes')
        self.assertEqual(tree.find(self.cas + 'user').text.strip(), "testgid")  # 学号（输入的登录名）
        self.assertEqual(attributes.find(self.cas + 'gid').text.strip(), "testgid")  # GID
        self.assertEqual(attributes.find(self.cas + 'xbm').text.strip(), "1")
        self.assertIsNotNone(attributes.find(self.cas + 'logintime'))
        self.assertEqual(attributes.find(self.cas + 'ryzxztdm').text.strip(), "10")
        self.assertEqual(attributes.find(self.cas + 'ryfldm').text.strip(), "201030000")
        # self.assertEqual(attributes.find(self.cas + 'loginip').text.strip(), "127.0.0.1")
        self.assertEqual(attributes.find(self.cas + 'name').text.strip(), "testname")
        self.assertEqual(attributes.find(self.cas + 'login').text.strip(), "testgid")
        self.assertEqual(attributes.find(self.cas + 'zjhm').text.strip(), "SA21110000")
        self.assertEqual(attributes.find(self.cas + 'glzjh').text.strip(), "SA21110000\tPB17110000")
        self.assertEqual(attributes.find(self.cas + 'deptCode').text.strip(), "123")
        self.assertEqual(attributes.find(self.cas + 'email').text.strip(), "test@example.com")
