from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import google_oauth2_callback, google_oauth2_login

urlpatterns = [
    path('google/callback/', csrf_exempt(google_oauth2_callback), name='oauth2-google-callback'),
    path('google/login/', csrf_exempt(google_oauth2_login), name='oauth2-google-login'),
]
