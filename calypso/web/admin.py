from django.contrib import admin
from .models import Slide, Slider
# Register your models here.
admin.site.site_header = 'Calypso'


admin.site.register(Slider)
admin.site.register(Slide)
