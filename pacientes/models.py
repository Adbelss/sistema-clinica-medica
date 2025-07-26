from django.db import models
from django.conf import settings  # ✅ Usar el modelo de usuario configurado

class Paciente(models.Model):
    # Generales
    primer_nombre = models.CharField(max_length=50)
    otros_nombres = models.CharField(max_length=50, blank=True, null=True)
    primer_apellido = models.CharField(max_length=50)
    segundo_apellido = models.CharField(max_length=50, blank=True, null=True)
    apellido_casada = models.CharField(max_length=50, blank=True, null=True)
    tipo_documento = models.CharField(max_length=20, choices=[
        ('DPI', 'DPI - Documento Personal de Identificación'),
        ('Pasaporte', 'Pasaporte'),
        ('Carné de Extranjería', 'Carné de Extranjería'),
        ('Otro', 'Otro documento')
    ], default='DPI')
    documento_identificacion = models.CharField(max_length=50, default='N/A')  # ✅ Agregado default
    nit = models.CharField(max_length=20, default='CF')

    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=20, choices=[
        ('Masculino', 'Masculino'),
        ('Femenino', 'Femenino'),
        ('No binario', 'No binario'),
        ('Prefiero no decir', 'Prefiero no decir')
    ], default='Masculino')
    identidad_genero = models.CharField(max_length=50, blank=True, null=True)
    nacionalidad = models.CharField(max_length=50, default='Guatemalteca')  # ✅ Default sugerido
    profesion = models.CharField(max_length=100, blank=True, null=True)
    ocupacion = models.CharField(max_length=100, blank=True, null=True)
    discapacidad = models.CharField(max_length=100, blank=True, null=True)
    tipo_paciente = models.CharField(max_length=50, blank=True, null=True)
    
    # Nuevo campo: Estado Civil
    estado_civil = models.CharField(max_length=20, choices=[
        ('Soltero/a', 'Soltero/a'),
        ('Casado/a', 'Casado/a'),
        ('Divorciado/a', 'Divorciado/a'),
        ('Viudo/a', 'Viudo/a'),
        ('Unión libre', 'Unión libre'),
        ('Separado/a', 'Separado/a')
    ], blank=True, null=True)

    # Contacto
    correo = models.EmailField(default='paciente@ejemplo.com')  # ✅ Default para evitar error
    telefono = models.CharField(max_length=20, default='0000000000')  # ✅ Default obligatorio
    notificar_whatsapp = models.BooleanField(default=False)
    notificar_correo = models.BooleanField(default=False)
    notificar_sms = models.BooleanField(default=False)

    # Contacto de Emergencia (Nuevo)
    contacto_emergencia = models.CharField(max_length=100, blank=True, null=True)
    telefono_emergencia = models.CharField(max_length=20, blank=True, null=True)
    parentesco_emergencia = models.CharField(max_length=20, choices=[
        ('Cónyuge', 'Cónyuge'),
        ('Padre', 'Padre'),
        ('Madre', 'Madre'),
        ('Hijo/a', 'Hijo/a'),
        ('Hermano/a', 'Hermano/a'),
        ('Abuelo/a', 'Abuelo/a'),
        ('Tío/a', 'Tío/a'),
        ('Primo/a', 'Primo/a'),
        ('Amigo/a', 'Amigo/a'),
        ('Vecino/a', 'Vecino/a'),
        ('Otro', 'Otro')
    ], blank=True, null=True)

    # Dirección
    direccion = models.TextField(default='Sin dirección') 
    ciudad = models.CharField(max_length=100, default='Ciudad')  # ✅ Default obligatorio
    zona = models.CharField(max_length=10, blank=True, null=True)
    codigo_postal = models.CharField(max_length=10, blank=True, null=True)
    pais = models.CharField(max_length=50, default='Guatemala')  # ✅ Default obligatorio

    # Salud
    grupo_sanguineo = models.CharField(max_length=5, blank=True, null=True)
    alergias = models.CharField(max_length=100, blank=True, null=True)
    es_donador = models.BooleanField(default=False)
    comentarios_donacion = models.TextField(blank=True, null=True)
    fecha_donacion = models.DateField(blank=True, null=True)

    # Admin
    enviar_recordatorio = models.BooleanField(default=True)
    estado = models.CharField(max_length=10, choices=[
        ('Activo', 'Activo'), ('Inactivo', 'Inactivo')
    ], default='Activo')
    notas = models.TextField(blank=True, null=True)

    # Sistema
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.primer_nombre} {self.primer_apellido}"

    def edad(self):
        from datetime import date
        if self.fecha_nacimiento:
            today = date.today()
            return today.year - self.fecha_nacimiento.year - (
                (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
            )
        return None

    def nombre_completo(self):
        """Retorna el nombre completo del paciente"""
        nombres = f"{self.primer_nombre}"
        if self.otros_nombres:
            nombres += f" {self.otros_nombres}"
        
        apellidos = f"{self.primer_apellido}"
        if self.segundo_apellido:
            apellidos += f" {self.segundo_apellido}"
        
        return f"{nombres} {apellidos}"

    def es_mayor_edad(self):
        """Verifica si el paciente es mayor de edad"""
        edad = self.edad()
        return edad >= 18 if edad else False

    def tiene_contacto_emergencia(self):
        """Verifica si tiene información de contacto de emergencia"""
        return bool(self.contacto_emergencia and self.telefono_emergencia)

    def es_donador_activo(self):
        """Verifica si es donador activo"""
        if not self.es_donador:
            return False
        if self.fecha_donacion:
            from datetime import date, timedelta
            hoy = date.today()
            # Considerar donador activo si donó en los últimos 2 años
            return (hoy - self.fecha_donacion).days <= 730
        return False

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['primer_nombre', 'primer_apellido']),
            models.Index(fields=['documento_identificacion']),
            models.Index(fields=['telefono']),
            models.Index(fields=['estado']),
        ]
