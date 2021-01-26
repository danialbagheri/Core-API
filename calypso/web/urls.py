from django.urls import path, include
from django.conf.urls import url
from web import views
from django.contrib.auth import views as auth_views
from user.forms import LoginForm
app_name = "web"

urlpatterns = [
    path('', views.HomePage.as_view(), name="home"),
    url('login/',
        auth_views.LoginView.as_view(
            template_name='account/login.html',
            authentication_form=LoginForm,
            redirect_authenticated_user=True
        ), name="login"),
    url('logout/', auth_views.LogoutView.as_view(
        template_name='account/logout.html'), name='logout'),
]
