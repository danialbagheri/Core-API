from django.contrib import admin

from web.models import Setting


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    pass
