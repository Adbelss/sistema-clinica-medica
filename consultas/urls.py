
from django.urls import path
from django.shortcuts import redirect
from . import views

def redirect_to_dashboard(request):
    return redirect('dashboard')

urlpatterns = [
    path('', redirect_to_dashboard, name='consultas_home'),
    path('registrar/', views.registrar_consulta, name='registrar_consulta'),
    path('dashboard/', views.dashboard, name='dashboard'),  
    path('todas/', views.listar_consultas, name='listar_consultas'),
    path('editar/<int:consulta_id>/', views.editar_consulta, name='editar_consulta'),
    path('eliminar/<int:consulta_id>/', views.eliminar_consulta, name='eliminar_consulta'),
    path('consultas/<int:consulta_id>/', views.detalle_consulta, name='detalle_consulta'),
    path('exportar/pdf/', views.exportar_consultas_pdf, name='exportar_consultas_pdf'),
    path('exportar/excel/', views.exportar_consultas_excel, name='exportar_consultas_excel'),
    path('exportar/estadisticas/', views.exportar_estadisticas_excel, name='exportar_estadisticas_excel'),
    path('exportar/estadisticas-pdf/', views.exportar_estadisticas_pdf, name='exportar_estadisticas_pdf'),
    path('test-export/', views.test_export, name='test_export'),
    path('test-estadisticas/', views.test_estadisticas, name='test_estadisticas'),
    path('test-export-page/', views.test_export_page, name='test_export_page'),
    
    # Nuevas funcionalidades avanzadas
    path('buscar-pacientes/', views.buscar_pacientes, name='buscar_pacientes'),
    path('estadisticas/', views.estadisticas_consultas, name='estadisticas_consultas'),
    
    # WhatsApp Notifications
    path('whatsapp/enviar-receta/<int:consulta_id>/', views.enviar_receta_whatsapp, name='enviar_receta_whatsapp'),
    path('whatsapp/enviar-resumen/<int:consulta_id>/', views.enviar_resumen_whatsapp, name='enviar_resumen_whatsapp'),
    path('whatsapp/notificaciones/', views.listar_notificaciones_whatsapp, name='listar_notificaciones_whatsapp'),
    path('whatsapp/notificacion/<int:notificacion_id>/', views.detalle_notificacion_whatsapp, name='detalle_notificacion_whatsapp'),
    path('whatsapp/reintentar/<int:notificacion_id>/', views.reintentar_notificacion_whatsapp, name='reintentar_notificacion_whatsapp'),
    path('whatsapp/estadisticas/', views.estadisticas_whatsapp, name='estadisticas_whatsapp'),
    path('whatsapp/prueba-demo/', views.prueba_whatsapp_demo, name='prueba_whatsapp_demo'),
    path('whatsapp/configuracion/', views.verificar_configuracion_whatsapp, name='verificar_configuracion_whatsapp'),
]
