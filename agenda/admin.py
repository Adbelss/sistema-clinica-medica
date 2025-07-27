from django.contrib import admin
from .models import HorarioDoctor, Cita, Disponibilidad, Recordatorio

@admin.register(HorarioDoctor)
class HorarioDoctorAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'dia_semana', 'hora_inicio', 'hora_fin', 'duracion_cita', 'activo']
    list_filter = ['dia_semana', 'activo', 'doctor__especialidad']
    search_fields = ['doctor__first_name', 'doctor__last_name']
    ordering = ['doctor', 'dia_semana', 'hora_inicio']

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'doctor', 'fecha', 'hora_inicio', 'hora_fin', 'tipo_cita', 'estado']
    list_filter = ['estado', 'tipo_cita', 'fecha', 'doctor__especialidad']
    search_fields = ['paciente__primer_nombre', 'paciente__primer_apellido', 'doctor__first_name']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion', 'duracion', 'es_hoy', 'es_pasada']
    date_hierarchy = 'fecha'
    
    fieldsets = (
        ('Información de la Cita', {
            'fields': ('paciente', 'doctor', 'fecha', 'hora_inicio', 'hora_fin', 'tipo_cita', 'estado')
        }),
        ('Detalles', {
            'fields': ('motivo', 'notas')
        }),
        ('Sistema', {
            'fields': ('recordatorio_enviado', 'creado_por', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
        ('Propiedades Calculadas', {
            'fields': ('duracion', 'es_hoy', 'es_pasada'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('paciente', 'doctor', 'creado_por')

@admin.register(Disponibilidad)
class DisponibilidadAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'tipo', 'fecha_inicio', 'fecha_fin', 'activo']
    list_filter = ['tipo', 'activo', 'fecha_inicio', 'doctor__especialidad']
    search_fields = ['doctor__first_name', 'doctor__last_name', 'motivo']
    date_hierarchy = 'fecha_inicio'

@admin.register(Recordatorio)
class RecordatorioAdmin(admin.ModelAdmin):
    list_display = ['cita', 'tipo', 'enviado', 'fecha_envio', 'fecha_creacion']
    list_filter = ['tipo', 'enviado', 'fecha_creacion']
    search_fields = ['cita__paciente__primer_nombre', 'cita__doctor__first_name']
    readonly_fields = ['fecha_creacion']
    date_hierarchy = 'fecha_creacion'
