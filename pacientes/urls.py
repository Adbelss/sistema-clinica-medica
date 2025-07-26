from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_pacientes, name='listar_pacientes'),
    path('nuevo/', views.nuevo_paciente, name='nuevo_paciente'),  # ← ESTE NOMBRE DEBE USARSE EN TU FORM
    path('editar/<int:pk>/', views.editar_paciente, name='editar_paciente'),
    path('eliminar/<int:pk>/', views.eliminar_paciente, name='eliminar_paciente'),
]
