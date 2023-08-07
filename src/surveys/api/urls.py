from django.urls import path
from . import views


urlpatterns = [
    path('<slug:slug>/', views.SurveyRetrieveAPIView.as_view(), name='retrieve-survey'),
    path('submit/', views.SurveySubmissionCreateAPIView.as_view(), name='submit-survey'),
]
