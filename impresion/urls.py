from django.urls import path
from . import views

app_name = 'impresion'

urlpatterns = [
    # Dashboard principal
    path('', views.dashboard_impresion, name='dashboard'),
    
    # Generación de documentos
    path('generar-consulta/<int:consulta_id>/', views.generar_consulta_medica, name='generar_consulta'),
    path('generar-receta/<int:consulta_id>/', views.generar_receta_medica, name='generar_receta'),
    path('generar-gestion/<int:paciente_id>/', views.generar_gestion_paciente, name='generar_gestion'),
    
    # Visualización e impresión
    path('previsualizar/<int:documento_id>/', views.previsualizar_documento, name='previsualizar_documento'),
    path('imprimir/<int:documento_id>/', views.imprimir_documento, name='imprimir_documento'),
    path('descargar/<int:documento_id>/', views.descargar_documento_pdf, name='descargar_documento_pdf'),
    
    # Gestión de documentos
    path('documentos/', views.listar_documentos, name='listar_documentos'),
    
    # Configuración
    path('configuracion/', views.configuracion_impresion, name='configuracion_impresion'),
] 