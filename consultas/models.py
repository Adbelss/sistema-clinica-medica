from django.db import models
from django.conf import settings  # para AUTH_USER_MODEL

class Consulta(models.Model):
    paciente_nombre = models.CharField(max_length=100)
    motivo = models.TextField()
    diagnostico = models.TextField()
    tratamiento = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.paciente_nombre} - {self.fecha.strftime('%d/%m/%Y')}" if self.fecha else self.paciente_nombre
