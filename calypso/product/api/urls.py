from django.urls import path, include
from rest_framework import routers
from . import views

app_name = "products_api"

product_routers = routers.DefaultRouter()
product_routers.register(r'variant', views.VariantViewSet, basename="variant")
product_routers.register(r'product',
                         views.ProductViewSet, basename="product")

urlpatterns = [
    path('', include(product_routers.urls)),
    # path('', views.HomePage.as_view(), name="home")
]
