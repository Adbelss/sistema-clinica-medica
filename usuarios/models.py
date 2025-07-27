from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    firma_digital = models.ImageField(upload_to='firmas/', blank=True, null=True)
    especialidad = models.CharField(max_length=100, blank=True, null=True)
    rol = models.CharField(max_length=50, choices=[
        ('administrador', 'Administrador'),
        ('doctor', 'Doctor'),
        ('recepcionista', 'Recepcionista'),
    ])
    
    # Campos específicos para doctores
    numero_colegio = models.CharField(max_length=20, blank=True, null=True, verbose_name="Número de Colegio Médico")
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion_consultorio = models.TextField(blank=True, null=True)
    foto = models.ImageField(upload_to='doctores/', blank=True, null=True)
    biografia = models.TextField(blank=True, null=True)
    
    # Estados para doctores
    ESTADOS = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('vacaciones', 'Vacaciones'),
        ('licencia', 'Licencia'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADOS, default='activo')

    def __str__(self):
        return self.username
    
    @property
    def nombre_completo(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def es_doctor(self):
        return self.rol == 'doctor'
