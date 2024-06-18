from django.urls import path
from . import views
from .views import TestListView, download


urlpatterns = [
    path('quiz/', views.home, name='home'),
    path('quiz/history/', TestListView.as_view(), name='test_list'),
    path('quiz/download/<int:test_id>', download, name='test_download'),
    
]