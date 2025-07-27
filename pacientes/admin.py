from django.contrib import admin
from .models import Paciente, AntecedenteMedico, ExamenMedico, EvolucionClinica, Medicamento

# Register your models here.

@admin.register(AntecedenteMedico)
class AntecedenteMedicoAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'tipo_antecedente', 'descripcion', 'severidad', 'fecha_creacion']
    list_filter = ['tipo_antecedente', 'severidad', 'fecha_creacion']
    search_fields = ['paciente__primer_nombre', 'paciente__primer_apellido', 'descripcion']
    date_hierarchy = 'fecha_creacion'
    ordering = ['-fecha_creacion']
    
    fieldsets = (
        ('Información del Paciente', {
            'fields': ('paciente',)
        }),
        ('Detalles del Antecedente', {
            'fields': ('tipo_antecedente', 'descripcion', 'severidad', 'estado_actual')
        }),
        ('Fechas', {
            'fields': ('fecha_inicio', 'fecha_fin'),
            'classes': ('collapse',)
        }),
        ('Información Adicional', {
            'fields': ('notas',),
            'classes': ('collapse',)
        }),
        ('Sistema', {
            'fields': ('creado_por', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es una nueva instancia
            obj.creado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(ExamenMedico)
class ExamenMedicoAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'nombre_examen', 'tipo_examen', 'estado', 'fecha_solicitud', 'laboratorio']
    list_filter = ['tipo_examen', 'estado', 'fecha_solicitud', 'laboratorio']
    search_fields = ['paciente__primer_nombre', 'paciente__primer_apellido', 'nombre_examen']
    date_hierarchy = 'fecha_solicitud'
    ordering = ['-fecha_solicitud']
    
    fieldsets = (
        ('Información del Paciente', {
            'fields': ('paciente', 'consulta_solicitante')
        }),
        ('Detalles del Examen', {
            'fields': ('tipo_examen', 'nombre_examen', 'descripcion')
        }),
        ('Fechas', {
            'fields': ('fecha_solicitud', 'fecha_realizacion', 'fecha_resultado')
        }),
        ('Resultados', {
            'fields': ('resultado', 'valores_normales', 'interpretacion', 'archivo_resultado')
        }),
        ('Información Adicional', {
            'fields': ('estado', 'laboratorio', 'costo'),
            'classes': ('collapse',)
        }),
        ('Sistema', {
            'fields': ('solicitado_por', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es una nueva instancia
            obj.solicitado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(EvolucionClinica)
class EvolucionClinicaAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'fecha_evolucion', 'tipo_evolucion', 'diagnostico_actual', 'registrado_por']
    list_filter = ['tipo_evolucion', 'fecha_evolucion', 'registrado_por']
    search_fields = ['paciente__primer_nombre', 'paciente__primer_apellido', 'diagnostico_actual']
    date_hierarchy = 'fecha_evolucion'
    ordering = ['-fecha_evolucion']
    
    fieldsets = (
        ('Información del Paciente', {
            'fields': ('paciente', 'consulta_relacionada')
        }),
        ('Información Clínica', {
            'fields': ('fecha_evolucion', 'tipo_evolucion', 'sintomas_actuales', 'signos_vitales')
        }),
        ('Evaluación', {
            'fields': ('examen_fisico', 'diagnostico_actual', 'plan_tratamiento')
        }),
        ('Medicamentos', {
            'fields': ('medicamentos_actuales', 'dosis_medicamentos', 'efectos_secundarios'),
            'classes': ('collapse',)
        }),
        ('Seguimiento', {
            'fields': ('proxima_evaluacion', 'recomendaciones', 'observaciones'),
            'classes': ('collapse',)
        }),
        ('Sistema', {
            'fields': ('registrado_por', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es una nueva instancia
            obj.registrado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'nombre_medicamento', 'tipo_medicamento', 'dosis', 'frecuencia', 'activo', 'fecha_inicio']
    list_filter = ['tipo_medicamento', 'activo', 'alergia', 'fecha_inicio']
    search_fields = ['paciente__primer_nombre', 'paciente__primer_apellido', 'nombre_medicamento']
    date_hierarchy = 'fecha_inicio'
    ordering = ['-fecha_inicio']
    
    fieldsets = (
        ('Información del Paciente', {
            'fields': ('paciente', 'consulta_prescriptora')
        }),
        ('Detalles del Medicamento', {
            'fields': ('nombre_medicamento', 'principio_activo', 'tipo_medicamento')
        }),
        ('Dosis y Frecuencia', {
            'fields': ('dosis', 'frecuencia', 'duracion_tratamiento')
        }),
        ('Fechas', {
            'fields': ('fecha_inicio', 'fecha_fin')
        }),
        ('Estado', {
            'fields': ('activo', 'alergia', 'efectos_secundarios')
        }),
        ('Sistema', {
            'fields': ('prescrito_por', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es una nueva instancia
            obj.prescrito_por = request.user
        super().save_model(request, obj, form, change)
