from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'products_api'

product_routers = routers.DefaultRouter()
product_routers.register(
    prefix=r'variant',
    viewset=views.VariantViewSet,
    basename='variant',
)

product_routers.register(
    prefix=r'product',
    viewset=views.ProductViewSet,
    basename='product',
)

product_routers.register(
    prefix=r'single',
    viewset=views.SingleProductViewSet,
    basename='single-product',
)

product_routers.register(
    prefix=r'image',
    viewset=views.ProductImageViewSet,
    basename='image',
)

product_routers.register(
    prefix=r'tags',
    viewset=views.TagViewSet,
    basename='tags',
)

product_routers.register(
    prefix=r'collections',
    viewset=views.CollectionViewSet,
    basename='collections',
)

product_routers.register(
    prefix=r'types',
    viewset=views.ProductTypeViewSet,
    basename='product-types',
)

urlpatterns = [
    path('', include(product_routers.urls)),
    path('favorites/', views.FavoriteProductListAPIView.as_view(), name='user-favorites'),
    path('favorites/<slug:slug>/', views.FavoriteProductUpdateAPIView.as_view(), name='set-favorite'),
    path('variants/favorites/', views.FavoriteVariantListAPIView.as_view(), name='user-favorite-variants'),
    path('variants/favorites/<str:sku>/', views.FavoriteVariantUpdateAPIView.as_view(), name='set-favorite-variant'),
    path('edit/', views.ProductEditWebhookAPI.as_view(), name='product-edit'),
    path('variants/spf-recommendations/<int:survey_submission_id>/',
         views.SPFRecommendationListAPIView.as_view(), name='spf-recommendations'),
]
