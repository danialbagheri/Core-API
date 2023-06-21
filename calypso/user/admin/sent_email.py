from django.contrib import admin

from user.models import SentEmail


@admin.register(SentEmail)
class SentEmailAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'template_name',
        'sent_date',
    )
    list_filter = ('template_name',)
    search_fields = ('email',)
