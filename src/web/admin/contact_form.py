from django.contrib import admin

from web.models import ContactForm


@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'reason', 'email_sent')
    list_filter = ('email_sent',)
