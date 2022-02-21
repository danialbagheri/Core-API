from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from web.models import Slide


@admin.register(Slide)
class SlideAdmin(OrderedModelAdmin):
    list_display = (
        'name', 'active', 'custom_slide', 'link', 'move_up_down_links',
    )
