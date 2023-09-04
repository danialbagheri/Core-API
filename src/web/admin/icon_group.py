from django.contrib import admin

from web.models import IconGroup, IconGroupItem


class IconGroupItemInlineAdmin(admin.StackedInline):
    model = IconGroupItem
    extra = 0
    ordering = ('position',)


@admin.register(IconGroup)
class IconGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active',)
    list_filter = ('is_active',)
    inlines = (IconGroupItemInlineAdmin,)
