from django.urls import path, include
from rest_framework import routers

from . import views

app_name = 'web_api'


web_routers = routers.DefaultRouter()
web_routers.register(
    prefix=r'configuration',
    viewset=views.ConfigurationView,
    basename='configuration',
)


urlpatterns = [
    path('', include(web_routers.urls)),
    path('contact-us/', views.ContactFormAPIView.as_view(), name='contact-us'),
    path('slider/', views.SliderViewSet.as_view({'get': 'list'}), name='sliders'),
    path('instagram-feed/', views.InstagramFeed.as_view(), name='instagram'),
    path('search/', views.Search.as_view(), name='search'),
    path('top-bars/', views.TopBarListAPIView.as_view(), name='top-bars-list'),
    path('top-bars/<slug:slug>/', views.TopBarRetrieveAPIView.as_view(), name='top-bars-retrieve'),
    path('icon-groups/<slug:slug>/', views.IconGroupRetrieveAPIView.as_view(), name='icon-groups-retrieve'),
    path('instagram-posts/', views.InstagramListAPIView.as_view(), name='instagram-posts'),
    path('menus/<slug:slug>/', views.MenuRetrieveAPIView.as_view(), name='menus-retrieve'),
    path('menus/search/', views.MenuSearchListAPIView.as_view(), name='menus-search'),
]
