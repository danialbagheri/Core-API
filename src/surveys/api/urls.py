from django.urls import path
from . import views

app_name = 'surveys_api'

urlpatterns = [
    path('submit/', views.SurveySubmissionCreateAPIView.as_view(), name='submit-survey'),
    path('<slug:slug>/', views.SurveyRetrieveAPIView.as_view(), name='retrieve-survey'),
]
