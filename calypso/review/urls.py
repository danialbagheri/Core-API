from django.urls import path, include
from rest_framework import routers
from . import views


app_name = "review_api"


review_routers = routers.DefaultRouter()
review_routers.register(r'product_category',
                        views.ReviewViewSet, basename="product_category")

urlpatterns = [
    path('', include(review_routers.urls)),
    # path('', views.HomePage.as_view(), name="home")
]
