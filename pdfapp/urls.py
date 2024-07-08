# pdfapp/urls.py
from django.urls import path
from .views import ask_pdf

urlpatterns = [
    path('ask_pdf/', ask_pdf, name='ask_pdf'),
]