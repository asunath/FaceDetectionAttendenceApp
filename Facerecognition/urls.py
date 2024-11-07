from django.urls import path
from Facerecognition import views


urlpatterns = [

    path('facerecognition/', views.facerecognition, name="facerecognition"),


    path('start_stream/', views.start_stream, name="start_stream"),
]