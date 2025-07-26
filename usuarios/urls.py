from django.urls import path
from . import views

urlpatterns = [
    path('configuraciones/', views.configuraciones, name='configuraciones'),
    path('respaldar/', views.respaldo_base_datos, name='respaldar_bd'),
    path('restaurar/', views.restaurar_base_datos, name='restaurar_bd'),
    path('gestion_usuarios/', views.gestion_usuarios, name='gestion_usuarios'),
    path('gestion_usuarios/nuevo/', views.crear_usuario, name='crear_usuario'),
]
