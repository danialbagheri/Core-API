from django.urls import path

from . import views

urlpatterns = [
    path('notifications/change/', views.OrderChangeNotificationAPI.as_view(), name='order-change-notification'),
]
