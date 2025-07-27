from django.urls import path
from . import views

urlpatterns = [
    # Dashboard y vistas principales
    path('', views.agenda_dashboard, name='agenda_dashboard'),
    path('calendario/', views.calendario, name='calendario'),
    
    # Gestión de citas
    path('citas/', views.listar_citas, name='listar_citas'),
    path('citas/nueva/', views.nueva_cita, name='nueva_cita'),
    path('citas/<int:pk>/editar/', views.editar_cita, name='editar_cita'),
    path('citas/<int:pk>/eliminar/', views.eliminar_cita, name='eliminar_cita'),
    path('citas/<int:pk>/estado/', views.cambiar_estado_cita, name='cambiar_estado_cita'),
    
    # Horarios de doctores
    path('doctores/<int:pk>/horarios/', views.horarios_doctor, name='horarios_doctor'),
    path('horarios/<int:pk>/eliminar/', views.eliminar_horario, name='eliminar_horario'),
    
    # Disponibilidad
    path('disponibilidad/', views.disponibilidad_doctores, name='disponibilidad_doctores'),
    
    # API endpoints
    path('api/citas-dia/', views.api_citas_dia, name='api_citas_dia'),
    path('api/horarios-disponibles/', views.api_horarios_disponibles, name='api_horarios_disponibles'),
] 