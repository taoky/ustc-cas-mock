from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User, ID
from .forms import UserCreationForm, UserChangeForm


class IDInline(admin.TabularInline):
    model = ID


class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('gid', 'email', 'name', 'is_superuser', 'is_active',)
    list_filter = ('gid', 'email', 'name', 'is_superuser', 'is_active',)
    fieldsets = (
        (None, {'fields': ('gid', 'email', 'password', 'name', 'ryzxztdm', 'ryfldm', 'deptCode')}),
        ('Permissions', {'fields': ('is_superuser', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('gid', 'email', 'name', 'password1', 'password2', 'is_superuser', 'is_active')}
        ),
    )
    search_fields = ('email', 'gid', 'name')
    ordering = ('gid',)
    filter_horizontal = ()
    inlines = [
        IDInline,
    ]


admin.site.register(User, UserAdmin)
admin.site.register(ID)
admin.site.unregister(Group)