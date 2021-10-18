from django.urls import path, include

import views

app_name = 'users_api'

urlpatterns = [
    path('', views.UserCreateAPIView.as_view(), name='user-create'),
    path('', include('djoser.urls')),
    path('orders', views.OrderAPIView.as_view(), name='user-orders'),
]
