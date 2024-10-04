from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_routes),
    path('ingress_data', views.get_ingress_data),
    path('analysis_data', views.get_analysis_data),
    path('trigger_analysis', views.trigger_analysis)

]