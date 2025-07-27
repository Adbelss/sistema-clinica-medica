from django.db import models
from django.conf import settings
from consultas.models import Consulta
from pacientes.models import Paciente
from django.utils import timezone

class DocumentoImpresion(models.Model):
    """Modelo para gestionar documentos de impresión médica"""
    
    TIPO_DOCUMENTO_CHOICES = [
        ('consulta', 'Consulta Médica'),
        ('receta', 'Receta Médica'),
        ('gestion', 'Gestión de Paciente'),
        ('certificado', 'Certificado Médico'),
        ('orden_laboratorio', 'Orden de Laboratorio'),
        ('orden_imagen', 'Orden de Imagenología'),
    ]
    
    ESTADO_CHOICES = [
        ('borrador', 'Borrador'),
        ('finalizado', 'Finalizado'),
        ('impreso', 'Impreso'),
        ('archivado', 'Archivado'),
    ]
    
    # Información del documento
    tipo_documento = models.CharField(max_length=20, choices=TIPO_DOCUMENTO_CHOICES)
    titulo = models.CharField(max_length=200)
    numero_documento = models.CharField(max_length=50, unique=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='borrador')
    
    # Relaciones
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, null=True, blank=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Contenido del documento
    contenido_html = models.TextField(help_text="Contenido HTML del documento")
    contenido_texto = models.TextField(blank=True, help_text="Contenido en texto plano")
    
    # Configuración de impresión
    incluir_logo = models.BooleanField(default=True)
    incluir_pie_pagina = models.BooleanField(default=True)
    incluir_firma = models.BooleanField(default=True)
    incluir_sello = models.BooleanField(default=True)
    
    # Metadatos
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    fecha_impresion = models.DateTimeField(null=True, blank=True)
    
    # Configuración de formato
    orientacion = models.CharField(max_length=10, choices=[('portrait', 'Vertical'), ('landscape', 'Horizontal')], default='portrait')
    tamano_papel = models.CharField(max_length=20, choices=[('A4', 'A4'), ('letter', 'Carta'), ('legal', 'Legal')], default='A4')
    margenes = models.CharField(max_length=20, default='normal', choices=[
        ('normal', 'Normal'),
        ('estrecho', 'Estrecho'),
        ('ancho', 'Ancho'),
        ('personalizado', 'Personalizado')
    ])
    
    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = "Documento de Impresión"
        verbose_name_plural = "Documentos de Impresión"
        indexes = [
            models.Index(fields=['tipo_documento', 'estado']),
            models.Index(fields=['paciente', 'fecha_creacion']),
            models.Index(fields=['doctor', 'fecha_creacion']),
        ]
    
    def __str__(self):
        return f"{self.get_tipo_documento_display()} - {self.paciente.nombre_completo()} - {self.fecha_creacion.strftime('%d/%m/%Y')}"
    
    def save(self, *args, **kwargs):
        if not self.numero_documento:
            self.numero_documento = self.generar_numero_documento()
        super().save(*args, **kwargs)
    
    def generar_numero_documento(self):
        """Genera un número único de documento"""
        from datetime import datetime
        fecha = datetime.now()
        tipo_abrev = self.tipo_documento.upper()[:3]
        return f"{tipo_abrev}-{fecha.year}{fecha.month:02d}{fecha.day:02d}-{self.id or '000'}"
    
    def marcar_como_impreso(self):
        """Marca el documento como impreso"""
        self.estado = 'impreso'
        self.fecha_impresion = timezone.now()
        self.save()
    
    def obtener_plantilla(self):
        """Obtiene la plantilla correspondiente al tipo de documento"""
        plantillas = {
            'consulta': 'impresion/plantillas/consulta_medica.html',
            'receta': 'impresion/plantillas/receta_medica.html',
            'gestion': 'impresion/plantillas/gestion_paciente.html',
            'certificado': 'impresion/plantillas/certificado_medico.html',
            'orden_laboratorio': 'impresion/plantillas/orden_laboratorio.html',
            'orden_imagen': 'impresion/plantillas/orden_imagen.html',
        }
        return plantillas.get(self.tipo_documento, 'impresion/plantillas/default.html')
    
    def obtener_contexto(self):
        """Obtiene el contexto para renderizar el documento"""
        return {
            'documento': self,
            'paciente': self.paciente,
            'doctor': self.doctor,
            'consulta': self.consulta,
            'fecha_actual': timezone.now(),
            'configuracion': {
                'incluir_logo': self.incluir_logo,
                'incluir_pie_pagina': self.incluir_pie_pagina,
                'incluir_firma': self.incluir_firma,
                'incluir_sello': self.incluir_sello,
                'orientacion': self.orientacion,
                'tamano_papel': self.tamano_papel,
                'margenes': self.margenes,
            }
        }


class PlantillaDocumento(models.Model):
    """Modelo para gestionar plantillas de documentos"""
    
    TIPO_PLANTILLA_CHOICES = [
        ('consulta', 'Consulta Médica'),
        ('receta', 'Receta Médica'),
        ('gestion', 'Gestión de Paciente'),
        ('certificado', 'Certificado Médico'),
        ('orden_laboratorio', 'Orden de Laboratorio'),
        ('orden_imagen', 'Orden de Imagenología'),
    ]
    
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_PLANTILLA_CHOICES)
    descripcion = models.TextField(blank=True)
    
    # Contenido de la plantilla
    html_template = models.TextField(help_text="Plantilla HTML")
    css_template = models.TextField(help_text="Estilos CSS")
    
    # Configuración
    es_activa = models.BooleanField(default=True)
    es_predeterminada = models.BooleanField(default=False)
    
    # Metadatos
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['tipo', 'nombre']
        verbose_name = "Plantilla de Documento"
        verbose_name_plural = "Plantillas de Documentos"
    
    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"
    
    def save(self, *args, **kwargs):
        # Si esta plantilla se marca como predeterminada, desmarcar las demás del mismo tipo
        if self.es_predeterminada:
            PlantillaDocumento.objects.filter(
                tipo=self.tipo, 
                es_predeterminada=True
            ).exclude(id=self.id).update(es_predeterminada=False)
        super().save(*args, **kwargs)


class ConfiguracionImpresion(models.Model):
    """Configuración global para impresión"""
    
    # Información de la clínica
    nombre_clinica = models.CharField(max_length=200, default="Clínica Médica")
    direccion_clinica = models.TextField(default="Dirección de la clínica")
    telefono_clinica = models.CharField(max_length=20, default="")
    email_clinica = models.EmailField(default="")
    sitio_web_clinica = models.URLField(blank=True)
    
    # Logos y elementos visuales
    logo_clinica = models.ImageField(upload_to='logos/', blank=True, null=True)
    sello_clinica = models.ImageField(upload_to='sellos/', blank=True, null=True)
    
    # Configuración de documentos
    pie_pagina_default = models.TextField(default="Documento generado automáticamente por el sistema")
    incluir_codigo_qr = models.BooleanField(default=True)
    incluir_fecha_generacion = models.BooleanField(default=True)
    incluir_numero_pagina = models.BooleanField(default=True)
    
    # Configuración de impresión
    tamano_papel_default = models.CharField(max_length=20, choices=[('A4', 'A4'), ('letter', 'Carta'), ('legal', 'Legal')], default='A4')
    orientacion_default = models.CharField(max_length=10, choices=[('portrait', 'Vertical'), ('landscape', 'Horizontal')], default='portrait')
    margenes_default = models.CharField(max_length=20, default='normal', choices=[
        ('normal', 'Normal'),
        ('estrecho', 'Estrecho'),
        ('ancho', 'Ancho'),
        ('personalizado', 'Personalizado')
    ])
    
    # Configuración de seguridad
    incluir_watermark = models.BooleanField(default=False)
    texto_watermark = models.CharField(max_length=100, default="DOCUMENTO OFICIAL", blank=True)
    
    class Meta:
        verbose_name = "Configuración de Impresión"
        verbose_name_plural = "Configuración de Impresión"
    
    def __str__(self):
        return f"Configuración de Impresión - {self.nombre_clinica}"
    
    @classmethod
    def obtener_configuracion(cls):
        """Obtiene la configuración activa o crea una por defecto"""
        config, created = cls.objects.get_or_create(id=1)
        return config
