from django.urls import path, include
from rest_framework import routers
from . import views

app_name = "blogs_api"

blog_router = routers.DefaultRouter()
blog_router.register(r'all', views.BlogPostViewSet, basename="all")
blog_router.register(r'collections', views.CollectionViewSet, basename="collections")

urlpatterns = [
    path('', include(blog_router.urls)),
    path('bookmarks/', views.BookmarkedBlogPostAPIView.as_view(), name='user-bookmarks'),
    path('bookmarks/<slug:slug>/', views.UpdateBookmarkAPIView.as_view(), name='set-bookmark'),
]
