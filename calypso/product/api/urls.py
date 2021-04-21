from django.urls import path, include
from rest_framework import routers
from . import views

app_name = "products_api"

product_routers = routers.DefaultRouter()
product_routers.register(r'variant', views.VariantViewSet, basename="variant")
product_routers.register(r'product',
                         views.ProductViewSet, basename="product")
product_routers.register(r'single',
                         views.SingleProductViewSet, basename="single-product")
product_routers.register(r'image',
                         views.ProductImageViewSet, basename="image")
product_routers.register(r'tags',
                         views.TagViewSet, basename="tags")

urlpatterns = [
    path('', include(product_routers.urls)),
    # path('', views.HomePage.as_view(), name="home")
]
