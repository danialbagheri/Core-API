from django.contrib.auth import views as auth_views
from django.urls import path

from user.forms import LoginForm
from web import views

app_name = 'web'

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('login/',
         auth_views.LoginView.as_view(
             template_name='account/login.html',
             authentication_form=LoginForm,
             redirect_authenticated_user=True
         ),
         name='login'
         ),
    path('logout/', auth_views.LogoutView.as_view(template_name='account/logout.html'), name='logout'),

    path('admin/login/',
         auth_views.LoginView.as_view(
             template_name='account/login.html',
             authentication_form=LoginForm,
             redirect_authenticated_user=True
         ),
         name='admin-login'
         ),
    path('admin/logout/', auth_views.LogoutView.as_view(template_name='account/logout.html'), name='admin-logout'),
]
