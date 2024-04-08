from django.conf import settings
from django.contrib import admin
from ordered_model.admin import OrderedTabularInline, OrderedInlineModelAdminMixin

from web.models import SliderSlidesThroughModel, Slider

admin.site.site_header = settings.BRAND_NAME


class SlidesThroughOrderedStackedInline(OrderedTabularInline):
    model = SliderSlidesThroughModel
    fields = ('slide', 'order', 'move_up_down_links',)
    readonly_fields = ('order', 'move_up_down_links',)
    extra = 1
    ordering = ('order', )


@admin.register(Slider)
class SliderAdmin(OrderedInlineModelAdminMixin,
                  admin.ModelAdmin):
    list_display = ('name', 'slug', 'slides_count')
    fields = ('name', 'slug')
    inlines = (SlidesThroughOrderedStackedInline,)

    def slides_count(self, slider: Slider):
        return slider.slider_slides.count()

    slides_count.short_description = 'Slides Count'
