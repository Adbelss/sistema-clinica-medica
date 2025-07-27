from django.db import models
from django.conf import settings  # para AUTH_USER_MODEL
from pacientes.models import Paciente
from django.utils import timezone

class Consulta(models.Model):
    # Relación con paciente real (nullable temporalmente para migración)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='consultas', null=True, blank=True)
    
    # Campo temporal para mantener compatibilidad
    paciente_nombre = models.CharField(max_length=100, blank=True, null=True)
    
    # Información básica de la consulta
    motivo = models.TextField(help_text="Motivo principal de la consulta")
    sintomas = models.TextField(blank=True, null=True, help_text="Síntomas presentados por el paciente")
    diagnostico = models.TextField(help_text="Diagnóstico médico")
    tratamiento = models.TextField(help_text="Tratamiento prescrito")
    
    # Información médica avanzada
    presion_arterial = models.CharField(max_length=20, blank=True, null=True, help_text="Ej: 120/80")
    temperatura = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, help_text="Temperatura en °C")
    peso = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Peso en kg")
    altura = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True, help_text="Altura en metros")
    frecuencia_cardiaca = models.IntegerField(blank=True, null=True, help_text="Latidos por minuto")
    
    # Estado de la consulta
    ESTADO_CHOICES = [
        ('Programada', 'Programada'),
        ('En Progreso', 'En Progreso'),
        ('Completada', 'Completada'),
        ('Cancelada', 'Cancelada'),
        ('Reagendada', 'Reagendada'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Completada')
    
    # Tipo de consulta
    TIPO_CHOICES = [
        ('Primera Vez', 'Primera Vez'),
        ('Control', 'Control'),
        ('Emergencia', 'Emergencia'),
        ('Seguimiento', 'Seguimiento'),
        ('Especialista', 'Especialista'),
    ]
    tipo_consulta = models.CharField(max_length=20, choices=TIPO_CHOICES, default='Control')
    
    # Medicamentos y recetas
    medicamentos_recetados = models.TextField(blank=True, null=True, help_text="Medicamentos prescritos")
    dosis_medicamentos = models.TextField(blank=True, null=True, help_text="Dosis y frecuencia de medicamentos")
    
    # Próximas citas
    proxima_cita = models.DateTimeField(blank=True, null=True, help_text="Fecha de la próxima cita")
    observaciones_cita = models.TextField(blank=True, null=True, help_text="Observaciones para la próxima cita")
    
    # Información del sistema
    fecha = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Campos para análisis y estadísticas
    duracion_consulta = models.IntegerField(blank=True, null=True, help_text="Duración en minutos")
    costo_consulta = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, help_text="Costo de la consulta")
    
    # Notas adicionales
    notas_adicionales = models.TextField(blank=True, null=True, help_text="Notas adicionales del doctor")
    
    class Meta:
        ordering = ['-fecha']
        verbose_name = "Consulta"
        verbose_name_plural = "Consultas"
        indexes = [
            models.Index(fields=['paciente', 'fecha']),
            models.Index(fields=['doctor', 'fecha']),
            models.Index(fields=['estado', 'fecha']),
            models.Index(fields=['tipo_consulta', 'fecha']),
        ]

    def __str__(self):
        if self.paciente:
            return f"{self.paciente.nombre_completo()} - {self.fecha.strftime('%d/%m/%Y %H:%M')}"
        else:
            return f"{self.paciente_nombre or 'Paciente no especificado'} - {self.fecha.strftime('%d/%m/%Y %H:%M')}"

    def get_paciente_nombre(self):
        """Obtiene el nombre del paciente de manera compatible"""
        if self.paciente:
            return self.paciente.nombre_completo()
        return self.paciente_nombre or "Paciente no especificado"

    def calcular_imc(self):
        """Calcula el Índice de Masa Corporal"""
        if self.peso and self.altura:
            return round(self.peso / (self.altura ** 2), 2)
        return None

    def obtener_categoria_imc(self):
        """Obtiene la categoría del IMC"""
        imc = self.calcular_imc()
        if imc:
            if imc < 18.5:
                return "Bajo peso"
            elif imc < 25:
                return "Peso normal"
            elif imc < 30:
                return "Sobrepeso"
            else:
                return "Obesidad"
        return None

    def es_emergencia(self):
        """Verifica si es una consulta de emergencia"""
        return self.tipo_consulta == 'Emergencia'

    def necesita_seguimiento(self):
        """Verifica si necesita seguimiento"""
        return bool(self.proxima_cita)

    def obtener_edad_paciente(self):
        """Obtiene la edad del paciente al momento de la consulta"""
        if self.paciente:
            return self.paciente.edad()
        return None

    def es_paciente_mayor_edad(self):
        """Verifica si el paciente es mayor de edad"""
        if self.paciente:
            return self.paciente.es_mayor_edad()
        return None

    def tiene_contacto_emergencia(self):
        """Verifica si el paciente tiene contacto de emergencia"""
        if self.paciente:
            return self.paciente.tiene_contacto_emergencia()
        return False

    def obtener_historial_consultas(self):
        """Obtiene el historial de consultas del paciente"""
        if self.paciente:
            return Consulta.objects.filter(paciente=self.paciente).exclude(id=self.id).order_by('-fecha')
        return Consulta.objects.none()

    def calcular_duracion_consulta(self):
        """Calcula la duración de la consulta si no está establecida"""
        if not self.duracion_consulta:
            # Lógica para calcular duración basada en tipo de consulta
            duraciones = {
                'Primera Vez': 45,
                'Control': 20,
                'Emergencia': 30,
                'Seguimiento': 25,
                'Especialista': 60,
            }
            return duraciones.get(self.tipo_consulta, 30)
        return self.duracion_consulta

    def obtener_estadisticas_vitales(self):
        """Obtiene un diccionario con las estadísticas vitales"""
        return {
            'presion_arterial': self.presion_arterial,
            'temperatura': self.temperatura,
            'peso': self.peso,
            'altura': self.altura,
            'frecuencia_cardiaca': self.frecuencia_cardiaca,
            'imc': self.calcular_imc(),
            'categoria_imc': self.obtener_categoria_imc(),
        }

    def es_consulta_completa(self):
        """Verifica si la consulta tiene toda la información necesaria"""
        campos_requeridos = ['motivo', 'diagnostico', 'tratamiento']
        return all(getattr(self, campo) for campo in campos_requeridos)

    def obtener_alertas_medicas(self):
        """Obtiene alertas médicas basadas en los datos de la consulta"""
        alertas = []
        
        # Alerta por temperatura alta
        if self.temperatura and self.temperatura > 38:
            alertas.append(f"⚠️ Temperatura elevada: {self.temperatura}°C")
        
        # Alerta por presión arterial
        if self.presion_arterial:
            try:
                sistolica, diastolica = map(int, self.presion_arterial.split('/'))
                if sistolica > 140 or diastolica > 90:
                    alertas.append(f"⚠️ Presión arterial alta: {self.presion_arterial}")
                elif sistolica < 90 or diastolica < 60:
                    alertas.append(f"⚠️ Presión arterial baja: {self.presion_arterial}")
            except:
                pass
        
        # Alerta por IMC
        imc = self.calcular_imc()
        if imc:
            if imc < 18.5:
                alertas.append(f"⚠️ IMC bajo: {imc} (Bajo peso)")
            elif imc > 30:
                alertas.append(f"⚠️ IMC alto: {imc} (Obesidad)")
        
        # Alerta por frecuencia cardíaca
        if self.frecuencia_cardiaca:
            if self.frecuencia_cardiaca > 100:
                alertas.append(f"⚠️ Frecuencia cardíaca alta: {self.frecuencia_cardiaca} lpm")
            elif self.frecuencia_cardiaca < 60:
                alertas.append(f"⚠️ Frecuencia cardíaca baja: {self.frecuencia_cardiaca} lpm")
        
        return alertas

class NotificacionWhatsApp(models.Model):
    """Modelo para gestionar notificaciones enviadas por WhatsApp"""
    
    TIPO_CHOICES = [
        ('receta', 'Receta Médica'),
        ('consulta', 'Resumen de Consulta'),
        ('recordatorio', 'Recordatorio de Cita'),
        ('resultado', 'Resultado de Examen'),
        ('emergencia', 'Alerta de Emergencia'),
    ]
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('leido', 'Leído'),
        ('error', 'Error'),
        ('cancelado', 'Cancelado'),
    ]
    
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='notificaciones_whatsapp')
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name='notificaciones_whatsapp', null=True, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    telefono = models.CharField(max_length=20, help_text="Número de teléfono del paciente")
    mensaje = models.TextField(help_text="Mensaje enviado por WhatsApp")
    plantilla_usada = models.CharField(max_length=100, blank=True, null=True, help_text="Plantilla de WhatsApp utilizada")
    
    # Estado y seguimiento
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_envio = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateTimeField(null=True, blank=True)
    fecha_lectura = models.DateTimeField(null=True, blank=True)
    
    # Información de la API
    whatsapp_message_id = models.CharField(max_length=100, blank=True, null=True, help_text="ID del mensaje en WhatsApp")
    error_mensaje = models.TextField(blank=True, null=True, help_text="Mensaje de error si falló el envío")
    intentos_envio = models.IntegerField(default=0, help_text="Número de intentos de envío")
    
    # Archivos adjuntos
    archivo_adjunto = models.FileField(upload_to='whatsapp_archivos/', blank=True, null=True, help_text="PDF o imagen adjunta")
    nombre_archivo = models.CharField(max_length=255, blank=True, null=True)
    
    # Sistema
    enviado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='notificaciones_enviadas')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Notificación WhatsApp"
        verbose_name_plural = "Notificaciones WhatsApp"
        ordering = ['-fecha_envio']
        indexes = [
            models.Index(fields=['paciente', 'tipo']),
            models.Index(fields=['estado', 'fecha_envio']),
            models.Index(fields=['whatsapp_message_id']),
        ]
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.paciente.nombre_completo()} - {self.fecha_envio.strftime('%d/%m/%Y %H:%M')}"
    
    def obtener_estado_display(self):
        """Retorna el estado con iconos"""
        iconos = {
            'pendiente': '⏳',
            'enviado': '📤',
            'entregado': '✅',
            'leido': '👁️',
            'error': '❌',
            'cancelado': '🚫',
        }
        return f"{iconos.get(self.estado, '')} {self.get_estado_display()}"
    
    def es_exitosa(self):
        """Verifica si la notificación fue exitosa"""
        return self.estado in ['entregado', 'leido']
    
    def puede_reintentar(self):
        """Verifica si se puede reintentar el envío"""
        return self.estado in ['error', 'pendiente'] and self.intentos_envio < 3
    
    def marcar_como_enviado(self, message_id=None):
        """Marca la notificación como enviada"""
        self.estado = 'enviado'
        self.fecha_entrega = timezone.now()
        if message_id:
            self.whatsapp_message_id = message_id
        self.save()
    
    def marcar_como_entregado(self):
        """Marca la notificación como entregada"""
        self.estado = 'entregado'
        self.save()
    
    def marcar_como_leido(self):
        """Marca la notificación como leída"""
        self.estado = 'leido'
        self.fecha_lectura = timezone.now()
        self.save()
    
    def marcar_error(self, error_msg):
        """Marca la notificación como error"""
        self.estado = 'error'
        self.error_mensaje = error_msg
        self.intentos_envio += 1
        self.save()
    
    def obtener_tiempo_respuesta(self):
        """Calcula el tiempo de respuesta si fue leída"""
        if self.fecha_lectura and self.fecha_envio:
            return self.fecha_lectura - self.fecha_envio
        return None
    
    def obtener_estadisticas(self):
        """Obtiene estadísticas de la notificación"""
        return {
            'tiempo_envio': self.fecha_entrega - self.fecha_envio if self.fecha_entrega else None,
            'tiempo_respuesta': self.obtener_tiempo_respuesta(),
            'intentos': self.intentos_envio,
            'exitoso': self.es_exitosa(),
        }
