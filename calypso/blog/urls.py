from django.urls import path, include
from rest_framework import routers
from . import views

app_name = "blogs_api"

blog_router = routers.DefaultRouter()
blog_router.register(r'all', views.BlogPostViewSet, basename="all")
blog_router.register(r'collections', views.CollectionViewSet, basename="collections")

urlpatterns = [
    path('', include(blog_router.urls)),
    # path('', views.HomePage.as_view(), name="home")
]
