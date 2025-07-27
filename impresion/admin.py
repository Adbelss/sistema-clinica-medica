from django.contrib import admin
from .models import DocumentoImpresion, PlantillaDocumento, ConfiguracionImpresion

@admin.register(DocumentoImpresion)
class DocumentoImpresionAdmin(admin.ModelAdmin):
    list_display = ['numero_documento', 'tipo_documento', 'paciente', 'doctor', 'estado', 'fecha_creacion']
    list_filter = ['tipo_documento', 'estado', 'fecha_creacion', 'doctor']
    search_fields = ['numero_documento', 'paciente__primer_nombre', 'paciente__primer_apellido', 'titulo']
    readonly_fields = ['numero_documento', 'fecha_creacion', 'fecha_modificacion']
    date_hierarchy = 'fecha_creacion'
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('tipo_documento', 'titulo', 'numero_documento', 'estado')
        }),
        ('Relaciones', {
            'fields': ('consulta', 'paciente', 'doctor')
        }),
        ('Contenido', {
            'fields': ('contenido_html', 'contenido_texto'),
            'classes': ('collapse',)
        }),
        ('Configuración de Impresión', {
            'fields': ('incluir_logo', 'incluir_pie_pagina', 'incluir_firma', 'incluir_sello')
        }),
        ('Formato', {
            'fields': ('orientacion', 'tamano_papel', 'margenes')
        }),
        ('Metadatos', {
            'fields': ('fecha_creacion', 'fecha_modificacion', 'fecha_impresion'),
            'classes': ('collapse',)
        }),
    )

@admin.register(PlantillaDocumento)
class PlantillaDocumentoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo', 'es_activa', 'es_predeterminada', 'creado_por', 'fecha_creacion']
    list_filter = ['tipo', 'es_activa', 'es_predeterminada', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    readonly_fields = ['fecha_creacion', 'fecha_modificacion']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'tipo', 'descripcion')
        }),
        ('Contenido', {
            'fields': ('html_template', 'css_template'),
            'classes': ('collapse',)
        }),
        ('Configuración', {
            'fields': ('es_activa', 'es_predeterminada', 'creado_por')
        }),
        ('Metadatos', {
            'fields': ('fecha_creacion', 'fecha_modificacion'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ConfiguracionImpresion)
class ConfiguracionImpresionAdmin(admin.ModelAdmin):
    list_display = ['nombre_clinica', 'telefono_clinica', 'email_clinica', 'tamano_papel_default']
    
    fieldsets = (
        ('Información de la Clínica', {
            'fields': ('nombre_clinica', 'direccion_clinica', 'telefono_clinica', 'email_clinica', 'sitio_web_clinica')
        }),
        ('Elementos Visuales', {
            'fields': ('logo_clinica', 'sello_clinica')
        }),
        ('Configuración de Documentos', {
            'fields': ('pie_pagina_default', 'incluir_codigo_qr', 'incluir_fecha_generacion', 'incluir_numero_pagina')
        }),
        ('Configuración de Impresión', {
            'fields': ('tamano_papel_default', 'orientacion_default', 'margenes_default')
        }),
        ('Seguridad', {
            'fields': ('incluir_watermark', 'texto_watermark')
        }),
    )
    
    def has_add_permission(self, request):
        # Solo permitir una configuración
        return not ConfiguracionImpresion.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # No permitir eliminar la configuración
        return False
