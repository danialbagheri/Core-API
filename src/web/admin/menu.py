from django.contrib import admin
from nested_admin.forms import SortableHiddenMixin
from nested_admin.nested import NestedModelAdmin, NestedStackedInline

from web.models import Menu


class SubSubMenuInlineAdmin(SortableHiddenMixin,
                            NestedStackedInline):
    model = Menu
    extra = 0
    verbose_name = 'SubSubMenu'
    verbose_name_plural = 'SubSubMenus'
    show_change_link = True


class SubMenuInlineAdmin(SortableHiddenMixin,
                         NestedStackedInline):
    model = Menu
    extra = 0
    inlines = (SubSubMenuInlineAdmin,)
    verbose_name = 'SubMenu'
    verbose_name_plural = 'SubMenus'
    show_change_link = True


class MenuInlineAdmin(SortableHiddenMixin,
                      NestedStackedInline):
    model = Menu
    extra = 0
    inlines = (SubMenuInlineAdmin,)
    show_change_link = True
    verbose_name = 'Item'
    verbose_name_plural = 'Items'


@admin.register(Menu)
class MenuAdmin(NestedModelAdmin):
    fields = ('slug', 'name', 'text', 'url', 'image', 'svg_image', 'position')
    list_display = ('name',)
    inlines = (MenuInlineAdmin,)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(parent_menu__isnull=True)
