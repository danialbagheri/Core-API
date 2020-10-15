from django.contrib import admin
from .models import Slide, Slider, SliderSlidesThroughModel
from ordered_model.admin import OrderedTabularInline, OrderedStackedInline, OrderedInlineModelAdminMixin, OrderedModelAdmin
# Register your models here.
admin.site.site_header = 'Calypso'


class SlidesthroughOrderedStackedInline(OrderedTabularInline):
    model = SliderSlidesThroughModel
    fields = ("slide", "order", 'move_up_down_links',)
    readonly_fields = ('order', 'move_up_down_links',)
    extra = 1
    ordering = ("order", )


class SliderAdmin(OrderedInlineModelAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'slug', 'mobile', 'slides_count')
    fields = ('name', 'slug', 'mobile')
    inlines = (SlidesthroughOrderedStackedInline,)

    def slides_count(self, obj, *args, **kwargs):

        return obj.slider_slides.count()


class SlideAdmin(OrderedModelAdmin):
    list_display = ("name", 'active', 'custom_slide',
                    'link', 'move_up_down_links')


admin.site.register(Slider, SliderAdmin)
admin.site.register(Slide, SlideAdmin)
#
