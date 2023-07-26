from django.contrib import admin

from review.models import Reply


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    pass
