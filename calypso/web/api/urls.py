from django.urls import path, include
from rest_framework import routers
from . import views

app_name = "web_api"


web_routers = routers.DefaultRouter()
# web_routers.register(r'contact-us', views.ContactForm,
#                      basename="contact-us")


urlpatterns = [
    path('', include(web_routers.urls)),
    path('contact-us/', views.ContactForm.as_view(), name="contact-us"),
    path(
        'slider/', views.SliderViewSet.as_view({'get': 'list'}), name="sliders"),
]
