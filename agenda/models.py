from django.db import models
from django.conf import settings
from pacientes.models import Paciente
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import datetime

class HorarioDoctor(models.Model):
    """Horarios de trabajo de cada doctor"""
    DIAS_SEMANA = [
        (0, 'Lunes'),
        (1, 'Martes'),
        (2, 'Miércoles'),
        (3, 'Jueves'),
        (4, 'Viernes'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]
    
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='horarios')
    dia_semana = models.IntegerField(choices=DIAS_SEMANA)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    duracion_cita = models.IntegerField(default=30, validators=[MinValueValidator(15), MaxValueValidator(120)], 
                                      help_text="Duración en minutos")
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Horario de Doctor"
        verbose_name_plural = "Horarios de Doctores"
        unique_together = ['doctor', 'dia_semana']
        ordering = ['doctor', 'dia_semana', 'hora_inicio']
    
    def __str__(self):
        return f"{self.doctor.nombre_completo} - {self.get_dia_semana_display()} {self.hora_inicio}-{self.hora_fin}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.hora_inicio >= self.hora_fin:
            raise ValidationError("La hora de inicio debe ser menor que la hora de fin")

class Cita(models.Model):
    """Modelo para las citas médicas"""
    ESTADOS_CITA = [
        ('programada', 'Programada'),
        ('confirmada', 'Confirmada'),
        ('en_proceso', 'En Proceso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
        ('no_show', 'No Show'),
        ('reprogramada', 'Reprogramada'),
    ]
    
    TIPOS_CITA = [
        ('primera_vez', 'Primera Vez'),
        ('control', 'Control'),
        ('emergencia', 'Emergencia'),
        ('consulta', 'Consulta'),
        ('seguimiento', 'Seguimiento'),
        ('procedimiento', 'Procedimiento'),
    ]
    
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='citas')
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='citas')
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    tipo_cita = models.CharField(max_length=20, choices=TIPOS_CITA, default='consulta')
    estado = models.CharField(max_length=20, choices=ESTADOS_CITA, default='programada')
    motivo = models.TextField(blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    recordatorio_enviado = models.BooleanField(default=False)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='citas_creadas')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Cita"
        verbose_name_plural = "Citas"
        ordering = ['-fecha', '-hora_inicio']
        unique_together = ['doctor', 'fecha', 'hora_inicio']
    
    def __str__(self):
        return f"{self.paciente.nombre_completo} - Dr. {self.doctor.nombre_completo} - {self.fecha} {self.hora_inicio}"
    
    @property
    def duracion(self):
        """Calcula la duración de la cita en minutos"""
        inicio = datetime.datetime.combine(datetime.date.today(), self.hora_inicio)
        fin = datetime.datetime.combine(datetime.date.today(), self.hora_fin)
        return int((fin - inicio).total_seconds() / 60)
    
    @property
    def es_hoy(self):
        """Verifica si la cita es hoy"""
        return self.fecha == timezone.now().date()
    
    @property
    def es_pasada(self):
        """Verifica si la cita ya pasó"""
        ahora = timezone.now()
        fecha_hora_cita = datetime.datetime.combine(self.fecha, self.hora_fin)
        return fecha_hora_cita < ahora
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.hora_inicio >= self.hora_fin:
            raise ValidationError("La hora de inicio debe ser menor que la hora de fin")
        
        # Verificar que no haya conflictos de horario
        if self.pk:  # Solo para citas existentes
            conflictos = Cita.objects.filter(
                doctor=self.doctor,
                fecha=self.fecha,
                estado__in=['programada', 'confirmada', 'en_proceso']
            ).exclude(pk=self.pk)
            
            for conflicto in conflictos:
                if (self.hora_inicio < conflicto.hora_fin and self.hora_fin > conflicto.hora_inicio):
                    raise ValidationError(f"Conflicto de horario con cita existente: {conflicto}")

class Disponibilidad(models.Model):
    """Disponibilidad temporal de los doctores (vacaciones, licencias, etc.)"""
    TIPOS = [
        ('vacaciones', 'Vacaciones'),
        ('licencia', 'Licencia'),
        ('capacitacion', 'Capacitación'),
        ('conferencia', 'Conferencia'),
        ('otro', 'Otro'),
    ]
    
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='disponibilidades')
    tipo = models.CharField(max_length=20, choices=TIPOS)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    motivo = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Disponibilidad"
        verbose_name_plural = "Disponibilidades"
        ordering = ['-fecha_inicio']
    
    def __str__(self):
        return f"{self.doctor.nombre_completo} - {self.get_tipo_display()} ({self.fecha_inicio} - {self.fecha_fin})"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.fecha_inicio > self.fecha_fin:
            raise ValidationError("La fecha de inicio debe ser menor o igual que la fecha de fin")

class Recordatorio(models.Model):
    """Sistema de recordatorios para citas"""
    TIPOS = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
    ]
    
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE, related_name='recordatorios')
    tipo = models.CharField(max_length=10, choices=TIPOS)
    fecha_envio = models.DateTimeField(blank=True, null=True)
    enviado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Recordatorio"
        verbose_name_plural = "Recordatorios"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"Recordatorio {self.get_tipo_display()} - {self.cita}"
