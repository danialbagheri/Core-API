from django.contrib import admin
from ordered_model.admin import OrderedTabularInline, OrderedInlineModelAdminMixin, OrderedModelAdmin

from .models import Slide, Slider, SliderSlidesThroughModel, Setting, Configuration, SearchQuery, ContactForm

admin.site.site_header = 'Calypso'


class SlidesthroughOrderedStackedInline(OrderedTabularInline):
    model = SliderSlidesThroughModel
    fields = ("slide", "order", 'move_up_down_links',)
    readonly_fields = ('order', 'move_up_down_links',)
    extra = 1
    ordering = ("order", )


class SliderAdmin(OrderedInlineModelAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'slug', 'slides_count')
    fields = ('name', 'slug')
    inlines = (SlidesthroughOrderedStackedInline,)

    def slides_count(self, obj, *args, **kwargs):

        return obj.slider_slides.count()


class SlideAdmin(OrderedModelAdmin):
    list_display = (
        'name', 'active', 'custom_slide', 'link', 'move_up_down_links',
    )


class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ('name', 'key', 'value')


@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ('text', 'count')
    ordering = ('count',)
    search_fields = ('text',)


@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'reason', 'email_sent')
    list_filter = ('email_sent',)


admin.site.register(Slider, SliderAdmin)
admin.site.register(Slide, SlideAdmin)
admin.site.register(Configuration, ConfigurationAdmin)
admin.site.register(Setting)
#
