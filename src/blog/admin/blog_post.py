from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from blog.models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug','published', 'publish_date')
    list_filter = ('category', 'tags', 'publish_date')
    search_fields = ('title', 'slug')
    summernote_fields = ('body',)
