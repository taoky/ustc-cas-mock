from django.utils import timezone

def custom_attributes(ticket):
    user = ticket.user
    ret = {
        "xbm": 1,  # What is this?
        "logintime": timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
        "email": user.email,
        "name": user.name,
        "gid": user.gid,
        "ryfldm": user.ryfldm,
        "deptCode": user.deptCode,
        "ryzxztdm": user.ryzxztdm,
        "glzjh": "\t".join(user.ordered_ids)
    }
    if ticket.login_ip:
        ret["login_ip"] = ticket.login_ip
    if ticket.username:
        ret['login'] = ticket.username
    if ticket.username and ticket.username != user.gid:
        zjhm = ticket.username
    else:
        zjhm = user.latest_id
    ret['zjhm'] = zjhm
    return ret
