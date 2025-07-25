# usuarios/urls.py

from django.urls import path
from .views import configuraciones, respaldo_base_datos, restaurar_base_datos

urlpatterns = [
    path('', configuraciones, name='configuraciones'),  # /configuraciones/
    path('respaldar/', respaldo_base_datos, name='respaldar_bd'),  # /configuraciones/respaldar/
    path('restaurar/', restaurar_base_datos, name='restaurar_bd'),  # /configuraciones/restaurar/
]
