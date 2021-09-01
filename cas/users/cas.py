from django.utils import timezone

def custom_attributes(user, service):
    return {
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
