from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _
from .models import User
# Register your models here.
class UserAdmin(UserAdmin):
    list_display = [
        "email",
        "first_name",
        "last_name",
    ]
    search_fields = [
        "first_name",
        "last_name",
        "email",
    ]
    readonly_fields = ['date_joined', ]
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {
         'fields': ('first_name', 'last_name',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
            
        }),(_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )
    ordering = ('email',)
    class Meta:
        model = User

admin.site.register(User, UserAdmin)