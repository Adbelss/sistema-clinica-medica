from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_pacientes, name='listar_pacientes'),
    path('nuevo/', views.nuevo_paciente, name='nuevo_paciente'),  # ← ESTE NOMBRE DEBE USARSE EN TU FORM
    path('editar/<int:pk>/', views.editar_paciente, name='editar_paciente'),
    path('eliminar/<int:pk>/', views.eliminar_paciente, name='eliminar_paciente'),
    
    # URLs para historial médico
    path('buscar-historial/', views.historial_medico, name='historial_medico_buscar'),
    path('historial/<int:paciente_id>/', views.historial_medico, name='historial_medico'),
    path('buscar-paciente/', views.buscar_paciente_historial, name='buscar_paciente_historial'),
    path('antecedentes/<int:paciente_id>/', views.antecedentes_paciente, name='antecedentes_paciente'),
    path('medicamentos/<int:paciente_id>/', views.medicamentos_paciente, name='medicamentos_paciente'),
    path('examenes/<int:paciente_id>/', views.examenes_paciente, name='examenes_paciente'),
    path('evolucion/<int:paciente_id>/', views.evolucion_paciente, name='evolucion_paciente'),
    path('resumen/<int:paciente_id>/', views.resumen_historial, name='resumen_historial'),
    path('recientes/', views.pacientes_recientes, name='pacientes_recientes'),
]
