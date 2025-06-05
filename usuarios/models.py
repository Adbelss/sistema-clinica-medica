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

    def __str__(self):
        return self.username
