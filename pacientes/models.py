from django.db import models
from django.utils import timezone

class Paciente(models.Model):
    # Datos personales
    primer_nombre = models.CharField(max_length=50, default='Nombre')
    otros_nombres = models.CharField(max_length=50, blank=True, null=True)
    primer_apellido = models.CharField(max_length=50, default='Apellido')
    segundo_apellido = models.CharField(max_length=50, blank=True, null=True)
    apellido_casada = models.CharField(max_length=50, blank=True, null=True)

    # Datos generales
    documento_identidad = models.CharField(max_length=25, unique=True, default='DPI-PENDIENTE')
    tipo_documento = models.CharField(max_length=15, choices=[('DPI', 'DPI'), ('CUI', 'CUI')], default='DPI')
    nit = models.CharField(max_length=20, default='CF')
    fecha_nacimiento = models.DateField(default=timezone.now)
    genero = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino')], default='M')
    profesion = models.CharField(max_length=100, blank=True, null=True)
    alergias = models.TextField(blank=True, null=True)
    grupo_sanguineo = models.CharField(max_length=3, choices=[
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')
    ], blank=True, null=True)

    # Contacto
    correo = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    notificacion_whatsapp = models.BooleanField(default=False)
    notificacion_email = models.BooleanField(default=False)
    notificacion_sms = models.BooleanField(default=False)

    # Dirección
    direccion = models.TextField(blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    pais = models.CharField(max_length=100, default='Guatemala')
    zona_residencia = models.CharField(max_length=100, blank=True, null=True)
    codigo_postal = models.CharField(max_length=15, blank=True, null=True)

    # Admin
    enviar_recordatorio = models.BooleanField(default=True)
    estado = models.CharField(max_length=10, choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')], default='Activo')
    notas = models.TextField(blank=True, null=True)

    # Extras
    nacionalidad = models.CharField(max_length=100, blank=True, null=True)
    identidad_genero = models.CharField(max_length=20, blank=True, null=True)
    discapacidad = models.CharField(max_length=100, blank=True, null=True)
    es_donador = models.BooleanField(default=False)
    fecha_donacion = models.DateField(blank=True, null=True)
    comentarios_donacion = models.TextField(blank=True, null=True)
    ocupacion = models.CharField(max_length=100, blank=True, null=True)
    tipo_paciente = models.CharField(max_length=100, blank=True, null=True)

    # Trazabilidad
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.primer_nombre} {self.primer_apellido} ({self.documento_identidad})"
