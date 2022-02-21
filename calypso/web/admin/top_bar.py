from django.contrib import admin

from web.models import TopBar, TopBarItem


class TopBarItemInlineAdmin(admin.StackedInline):
    model = TopBarItem
    extra = 0
    ordering = ('position',)


@admin.register(TopBar)
class TopBarAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'position')
    list_filter = ('is_active',)
    ordering = ('position',)
    list_editable = ('position',)
    inlines = (TopBarItemInlineAdmin,)
