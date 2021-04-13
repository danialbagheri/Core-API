from django.contrib import admin
from .models import BlogPost
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.
class BlogPostAdmin(SummernoteModelAdmin):
    list_display = ['title', 'slug','published', 'publish_date']
    list_filter = ['category', 'tags', 'publish_date']
    search_fields = ['title', 'slug']
    summernote_fields = ['body']

admin.site.register(BlogPost, BlogPostAdmin)