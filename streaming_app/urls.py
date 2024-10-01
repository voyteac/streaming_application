from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('data_ingress/', include('data_ingress.urls'), name="data-ingress"),
    path('data_display/', include('data_display.urls'), name="data-display"),
    path('data_analysis/', include('data_analysis.urls'), name="data-analysis"),
    path('api/', include('data_ingress.api.urls'))
]
