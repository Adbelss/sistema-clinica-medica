
from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrar_consulta, name='registrar_consulta'),
    path('dashboard/', views.dashboard, name='dashboard'),  
    path('todas/', views.listar_consultas, name='listar_consultas'),
    path('editar/<int:consulta_id>/', views.editar_consulta, name='editar_consulta'),
    path('eliminar/<int:consulta_id>/', views.eliminar_consulta, name='eliminar_consulta'),
    path('consultas/<int:consulta_id>/', views.detalle_consulta, name='detalle_consulta'),
    path('exportar/pdf/', views.exportar_consultas_pdf, name='exportar_consultas_pdf'),
    path('exportar/excel/', views.exportar_consultas_excel, name='exportar_consultas_excel'),
    
    # Nuevas funcionalidades avanzadas
    path('buscar-pacientes/', views.buscar_pacientes, name='buscar_pacientes'),
    path('estadisticas/', views.estadisticas_consultas, name='estadisticas_consultas'),
]
