from django.urls import path, include
from rest_framework import routers
from . import views

app_name = "faq"


faq_routers = routers.DefaultRouter()
faq_routers.register(r'all',
                        views.FaqViewSet, basename="faqs")

urlpatterns = [
    path('', include(faq_routers.urls)),
]