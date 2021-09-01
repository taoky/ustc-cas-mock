from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import User, ID

class AuthBackend(BaseBackend):
    def get_user(self, user_id):
        try:
            return User.objects.get(gid=user_id)
        except User.DoesNotExist:
            return None

    def authenticate(self, request, username=None, password=None):
        # 1.  get correct user
        # 1.1  is it GID?
        try:
            user = User.objects.get(gid=username)
        except User.DoesNotExist:
            # 1.2  is it in ID?
            try:
                id = ID.objects.get(id=username)
            except ID.DoesNotExist:
                return None
            user = id.user
        # 2.  check password
        pwd_valid = check_password(password, user.password)
        if not pwd_valid:
            return None
        return user
