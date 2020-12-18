from django.contrib import admin
from .models import Page
# Register your models here.
from django_grapesjs.admin import GrapesJsAdminMixin


@admin.register(Page)
class ExampleAdmin(GrapesJsAdminMixin, admin.ModelAdmin):
    pass