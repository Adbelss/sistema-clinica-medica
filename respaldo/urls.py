from django.urls import path
from . import views

urlpatterns = [
    path('', views.respaldo, name='respaldo'),
    path('exportar/', views.exportar_base_datos, name='exportar_base_datos'),
    path('importar/', views.importar_base_datos, name='importar_base_datos'),
]
