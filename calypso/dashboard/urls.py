from django.urls import path, include
from dashboard import views
from dashboard.views import (
    ProductEdit,
    CollectionsList,
    CollectionEditView,
    CollectionCreate,
    CollectionDelete,
    ProductTagUpdate,
    ProductTagDelete,
    ImageUploadView,
    ApiEndpointView
)
app_name = "dashboard"

urlpatterns = [
    path('', views.dashboard, name="home"),
    path('products/', views.products, name="products"),
    path('products/<slug:slug>/',
         ProductEdit.as_view(), name="product-edit"),
    path('images/upload/', ImageUploadView.as_view(), name="image-upload"),
    path('tags/', views.product_tags, name="tags"),
    path('tags/<int:pk>/', ProductTagUpdate.as_view(), name="tag-edit"),
    path('tags/<int:pk>/delete/', ProductTagDelete.as_view(), name="tag-delete"),
    path('collection/', CollectionsList.as_view(), name="collections"),
    path('collection/add/', CollectionCreate.as_view(),
         name="collection-add"),
    path('collection/<int:pk>/', CollectionEditView.as_view(),
         name="collection-edit"),
    path('collection/<int:pk>/delete/', CollectionDelete.as_view(),
         name="collection-delete"),
    path('api-endpoint/', ApiEndpointView.as_view(),
         name="api-endpoint"),
]
