from django.urls import path, include
from dashboard import views

app_name = "dashboard"

urlpatterns = [
    path('', views.dashboard, name="home"),
    path('products/', views.products, name="products"),
    path('products/<slug>/', views.product_add_or_edit, name="product-edit"),
    path('tags/', views.product_tags, name="tags"),
]
