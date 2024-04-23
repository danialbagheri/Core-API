from django.urls import path

from . import views

app_name = 'orders_api'

urlpatterns = [
    path('fulfilled/', views.OrderFulfilledWebhookAPI.as_view(), name='order-fulfilled-webhook'),
]
