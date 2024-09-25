from django.urls import path
from data_display import views

urlpatterns = [
    path('', views.display, name='data-display'),
    ]