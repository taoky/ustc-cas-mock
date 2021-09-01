from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, UserChangeForm as BaseUserChangForm

from .models import User


class UserCreationForm(BaseUserCreationForm):

    class Meta:
        model = User
        fields = ('gid', 'email', 'name', 'ryzxztdm', 'ryfldm', 'deptCode')


class UserChangeForm(BaseUserChangForm):

    class Meta:
        model = User
        fields = ('gid', 'email', 'name', 'ryzxztdm', 'ryfldm', 'deptCode')
