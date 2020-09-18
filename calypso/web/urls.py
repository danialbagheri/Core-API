from django.urls import path, include
from web import views

app_name="web"

urlpatterns = [
    path('', views.HomePage.as_view(), name="home")
]