from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

app_name = 'users_api'

router = DefaultRouter()
router.register('', views.UserViewSet)

urlpatterns = [
    path('token/', views.LoginAPIView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('cookie/verify/', views.VerifySessionCookieAPIView.as_view(), name='verify-cookie'),
    path('orders/', views.OrderAPIView.as_view(), name='user-orders'),
    path('addresses/', views.AddressAPIView.as_view(), name='user-addresses'),
    path('push-subscribers/', views.PushSubscriberCreateAPIView.as_view(), name='push-subscribers-create'),
    path('orders/paid/', views.OrderPaidWebhookAPI.as_view(), name='orders-paid'),
    path('refunds/', views.RefundWebhookAPI.as_view(), name='refunds'),
    path('ips/<str:ip>/locations/', views.IPLocationAPIView.as_view(), name='ip-locations'),
    path('stock-reports/', views.ProductInStockReportCreateAPI.as_view(), name='stock-report-create'),
    path('variant-image-requests/', views.VariantImageRequestCreateAPIView.as_view(), name='image-request-create'),
    path('subscribe/mailjet/', views.SubscribeMailjetEmailAPIView.as_view(), name='subscribe-mailjet-email'),
    path('remove/mailjet/', views.RemoveMailjetEmailAPIView.as_view(), name='remove-mailjet-email'),
    path('validate/mailjet/', views.ValidateEmailSubscriptionAPIView.as_view(), name='validate-email-subscription'),
] + router.urls
