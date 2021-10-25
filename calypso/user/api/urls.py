from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

app_name = 'users_api'

urlpatterns = [
    path('', views.UserCreateAPIView.as_view(), name='user-create'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('orders/', views.OrderAPIView.as_view(), name='user-orders'),
    path('addresses/', views.AddressAPIView.as_view(), name='user-addresses'),
]
