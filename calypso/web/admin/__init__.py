from django.contrib import admin

from .configuration import ConfigurationAdmin
from .contact_form import ContactFormAdmin
from .search_query import SearchQueryAdmin
from .setting import SettingAdmin
from .slide import SlideAdmin
from .slider import SliderAdmin

admin.site.site_header = 'Calypso'
