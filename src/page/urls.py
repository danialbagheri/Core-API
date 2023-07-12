from django.urls import path, include
from rest_framework import routers
from . import views


app_name = "page_api"
review_routers = routers.DefaultRouter()
review_routers.register(r'',
                        views.PageViewSet, basename="page")

urlpatterns = [
    path('', include(review_routers.urls)),
]