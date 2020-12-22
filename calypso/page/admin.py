from django.contrib import admin
from .models import Page
# Register your models here.
from django_grapesjs.admin import GrapesJsAdminMixin


class PageAdmin(GrapesJsAdminMixin, admin.ModelAdmin):
    pass

admin.site.register(Page, PageAdmin)