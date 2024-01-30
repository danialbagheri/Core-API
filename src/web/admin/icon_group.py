from django.contrib import admin
from django.utils.safestring import mark_safe

from web.models import IconGroup, IconGroupItem


class IconGroupItemInlineAdmin(admin.StackedInline):
    fields = (
        'name', 'icon', 'icon_preview', 'svg_icon', 'icon_svg_preview', 'url', 'is_active', 'position',
    )
    readonly_fields = ('icon_preview', 'icon_svg_preview',)
    model = IconGroupItem
    extra = 0
    ordering = ('position',)

    def icon_preview(self, icon_group_item: IconGroupItem):
        icon = icon_group_item.icon
        if icon:
            return mark_safe('<img src="{}" width="200" />'.format(icon.url))
        return mark_safe('<p style="background-color:#c2c2c2;padding: 5px 10px;"> Please upload an image. </p>')

    icon_preview.short_description = 'Icon Preview'

    def icon_svg_preview(self, icon_group_item: IconGroupItem):
        icon = icon_group_item.svg_icon
        if icon:
            return mark_safe('<img src="{}" width="200" />'.format(icon.url))
        return mark_safe('<p style="background-color:#c2c2c2;padding: 5px 10px;"> Please upload an image. </p>')

    icon_svg_preview.short_description = 'SVG Icon Preview'


@admin.register(IconGroup)
class IconGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active',)
    list_filter = ('is_active',)
    inlines = (IconGroupItemInlineAdmin,)
