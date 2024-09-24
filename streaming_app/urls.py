from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('data_ingress/', include('data_ingress.urls'), name="data-ingress"),
    path('api/', include('data_ingress.api.urls'))
]
