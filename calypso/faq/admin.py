from django.contrib import admin
from .models import Faq
# Register your models here.
class FaqAdmin(admin.ModelAdmin):

    # filter_horizontal = ('tags', 'product_types')
    list_filter = ('product',)
    list_display = [
        "question",
        "answer",
    ]
    search_fields = ['question']
    



admin.site.register(Faq, FaqAdmin)