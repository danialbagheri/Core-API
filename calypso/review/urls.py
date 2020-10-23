from django.urls import path, include
from rest_framework import routers
from . import views


app_name = "review_api"


review_routers = routers.DefaultRouter()
review_routers.register(r'product',
                        views.ReviewViewSet, basename="reviews")
# review_routers.register(r'product/<slug:slug>/add/',
#                         views.CreateReview, basename="create-review")

urlpatterns = [
    path('', include(review_routers.urls)),
    path('product/<slug:slug>/add/',
         views.CreateReview.as_view(), name="create-review")
]
