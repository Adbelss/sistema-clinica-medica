from django.contrib import admin
from .models import Consulta, NotificacionWhatsApp

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'doctor', 'fecha', 'tipo_consulta', 'estado', 'motivo']
    list_filter = ['estado', 'tipo_consulta', 'fecha', 'doctor']
    search_fields = ['paciente__primer_nombre', 'paciente__primer_apellido', 'motivo', 'diagnostico']
    date_hierarchy = 'fecha'
    ordering = ['-fecha']
    
    fieldsets = (
        ('Información del Paciente', {
            'fields': ('paciente', 'paciente_nombre')
        }),
        ('Información de la Consulta', {
            'fields': ('motivo', 'sintomas', 'diagnostico', 'tratamiento', 'tipo_consulta', 'estado')
        }),
        ('Signos Vitales', {
            'fields': ('presion_arterial', 'temperatura', 'peso', 'altura', 'frecuencia_cardiaca'),
            'classes': ('collapse',)
        }),
        ('Medicamentos', {
            'fields': ('medicamentos_recetados', 'dosis_medicamentos'),
            'classes': ('collapse',)
        }),
        ('Próxima Cita', {
            'fields': ('proxima_cita', 'observaciones_cita'),
            'classes': ('collapse',)
        }),
        ('Información del Sistema', {
            'fields': ('doctor', 'fecha', 'fecha_actualizacion', 'duracion_consulta', 'costo_consulta', 'notas_adicionales'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['fecha', 'fecha_actualizacion']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('paciente', 'doctor')


@admin.register(NotificacionWhatsApp)
class NotificacionWhatsAppAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'tipo', 'estado', 'fecha_envio', 'enviado_por', 'telefono']
    list_filter = ['tipo', 'estado', 'fecha_envio', 'enviado_por']
    search_fields = ['paciente__primer_nombre', 'paciente__primer_apellido', 'telefono', 'mensaje']
    date_hierarchy = 'fecha_envio'
    ordering = ['-fecha_envio']
    readonly_fields = ['fecha_envio', 'fecha_entrega', 'fecha_lectura', 'fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = (
        ('Información del Paciente', {
            'fields': ('paciente', 'telefono')
        }),
        ('Información de la Notificación', {
            'fields': ('tipo', 'consulta', 'mensaje', 'plantilla_usada')
        }),
        ('Estado y Seguimiento', {
            'fields': ('estado', 'whatsapp_message_id', 'intentos_envio', 'error_mensaje')
        }),
        ('Fechas', {
            'fields': ('fecha_envio', 'fecha_entrega', 'fecha_lectura', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
        ('Archivos', {
            'fields': ('archivo_adjunto', 'nombre_archivo'),
            'classes': ('collapse',)
        }),
        ('Sistema', {
            'fields': ('enviado_por',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('paciente', 'consulta', 'enviado_por')
    
    def has_add_permission(self, request):
        return False  # No permitir crear notificaciones manualmente
    
    def has_change_permission(self, request, obj=None):
        return False  # No permitir editar notificaciones
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser  # Solo superusuarios pueden eliminar
