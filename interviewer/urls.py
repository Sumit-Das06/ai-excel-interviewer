# interviewer/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.start_interview_endpoint, name='start_interview'),
    path('respond/', views.respond_to_question_endpoint, name='respond_to_question'),
]
