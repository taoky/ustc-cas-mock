from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, gid, email, name, password=None, **extra_fields):
        if not gid:
            raise ValueError("GID 未设置。")
        email = self.normalize_email(email)
        user = self.model(gid=gid, email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, gid, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(gid, email, name, password, **extra_fields)


class User(AbstractBaseUser):
    gid = models.CharField(primary_key=True, max_length=128)
    email = models.EmailField(max_length=64)
    name = models.CharField(max_length=64)
    ryzxztdm = models.CharField(max_length=2, choices=(
        ("10", "在校"),
        ("20", "离校（含校内身份结束）"),
        ("30", "校内身份转换"),
        ("40", "离退休"),
        ("50", "暂时离校（休学/出国等）"),
        ("99", "其他"),
        ("91", "证件停用或注销"),
    ), default="10")  # 在校状态
    ryfldm = models.CharField(max_length=9, choices=(
        ("101010000", "教工-正式编制教学岗"),
        ("101020000", "教工-正式编制科研岗"),
        ("101030000", "教工-正式编制管理岗"),
        ("101040000", "教工-正式编制支撑岗"),
        ("101ZZ0000", "教工-正式编制其他岗或未明岗"),
        ("201010000", "学生-正式科学学位博士"),
        ("201020000", "学生-正式科学学位硕士"),
        ("201030000", "学生-正式本科"),
        ("201040000", "学生-正式学生专科"),
        ("201ZZ0000", "学生-正式学生其他或未知层次"),
        ("202010000", "学生-专业学位博士"),
        ("202020000", "学生-专业学位硕士"),
        ("202ZZ0000", "学生-专业学位其他或未知层次"),
        ("240030000", "学生-夜大函授培训班本科"),
        ("240040000", "学生-夜大函数培训班专科"),
        ("240ZZ0000", "学生-夜大函数培训班其他或未知层次"),
        ("290ZZ0000", "短期培训学生"),
        ("2ZZZZ0000", "学生-其他类型学生"),
        ("300000000", "博士后"),
        ("901000000", "来访人员-上级部门各种类型来访人员"),
        ("902000000", "交流访问进修人员"),
        ("903000000", "来访人员-邀请来的讲座、演出、交流人员"),
        ("904000000", "来访人员-参加会议人员"),
        ("905000000", "来访人员-来校参观人员"),
        ("906000000", "来访人员-学生家长"),
        ("9ZZ000000", "来访人员-其他来访人员"),
        ("Z01000000", "教工家属"),
        ("Z02000000", "附中学生"),
        ("ZZZ000000", "其他人员"),
        ("103ZZ0000", "教工-校聘用人员其他岗或未明岗"),
        ("180ZZ0000", "各单位自聘人员"),
        ("190ZZ0000", "各单位临时聘用人员"),
        ("301000000", "校内博士后"),
        ("309000000", "企业博士后"),
    ), default="201030000")  # 人员分类代码
    deptCode = models.CharField(max_length=10, default="123")  # 部门代码
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "gid"
    REQUIRED_FIELDS = ["email", "name"]

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_superuser

    @property
    def ordered_ids(self):
        # 排序后的证件号码
        return list(self.id_set.order_by("-order").values_list('id', flat=True))


class ID(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.CharField(max_length=32, unique=True, primary_key=True)
    order = models.IntegerField(default=0, help_text="order 值越高，排列管理证件号 (glzjh) 时就越在前面。")

    def __str__(self):
        return f"{self.id} ({self.user})"
