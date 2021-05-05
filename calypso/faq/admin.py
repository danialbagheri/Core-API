from django.contrib import admin
from .models import Faq
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.
class FaqAdmin(SummernoteModelAdmin):

    # filter_horizontal = ('tags', 'product_types')
    list_filter = ('product',)
    list_display = [
        "question",
        "public",
    ]
    summernote_fields=('answer',)
    search_fields = ['question']
    



admin.site.register(Faq, FaqAdmin)