from django.contrib import admin

from web.models import ContactForm


@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    readonly_fields = ('sent_date',)
    list_display = ('id', 'email', 'reason', 'sent_date', 'email_sent')
    list_filter = ('email_sent',)
