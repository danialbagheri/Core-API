from django.contrib import admin
from .models import Page
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.


class PageAdmin(SummernoteModelAdmin):
    summernote_fields = ('html','section_1', 'section_2', 'section_3', 'section_4')
    list_display=['title','slug','created', 'published' ]
    search_fields=('title',)

admin.site.register(Page, PageAdmin)