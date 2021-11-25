from django.urls import path, include
from rest_framework import routers
from review.api import views


app_name = "review_api"


review_routers = routers.DefaultRouter()
review_routers.register(
    prefix=r'product',
    viewset=views.ReviewViewSet,
    basename="reviews",
)

urlpatterns = [
    path('', include(review_routers.urls)),
    path('product/<slug:slug>/add/', views.CreateReview.as_view(), name="create-review"),
    path('rate/<int:pk>/', views.RateReview.as_view(), name="rate-review"),
    path('images/', views.ReviewImageAPIView.as_view(), name='review-image'),
    path('me/', views.UserReviewListAPIView.as_view(), name='user-reviews'),
]
