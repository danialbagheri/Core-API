from django.contrib import admin
from .models import Faq
from django_summernote.admin import SummernoteModelAdmin


class FaqAdmin(SummernoteModelAdmin):
    list_filter = ('product',)
    list_display = [
        "question",
        "public",
    ]
    ordering = ('-updated',)
    summernote_fields=('answer',)
    search_fields = ['question']


admin.site.register(Faq, FaqAdmin)
