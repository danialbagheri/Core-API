from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    # Google urls
    path('google/login/', csrf_exempt(views.google_oauth2_login), name='oauth2-google-login'),
    path('google/callback/', csrf_exempt(views.google_oauth2_callback), name='oauth2-google-callback'),

    # Facebook urls
    path('facebook/login/', csrf_exempt(views.facebook_oauth2_login), name='oauth2-facebook-login'),
    path('facebook/callback/', csrf_exempt(views.facebook_oauth2_callback), name='oauth2-facebook-callback'),
]
