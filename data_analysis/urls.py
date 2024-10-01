from django.urls import path
from data_analysis import views

urlpatterns = [
    path('', views.analysis, name='data-analysis'),
    ]