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
    telefono_secundario = models.CharField(max_length=20, blank=True, null=True)  # ✅ Nuevo campo
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
    factor_rh = models.CharField(max_length=5, blank=True, null=True)  # ✅ Nuevo campo
    alergias = models.CharField(max_length=100, blank=True, null=True)
    antecedentes_medicos = models.TextField(blank=True, null=True)  # ✅ Nuevo campo
    medicamentos_actuales = models.TextField(blank=True, null=True)  # ✅ Nuevo campo
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

    # Métodos para historial médico
    def obtener_antecedentes_importantes(self):
        """Obtiene antecedentes médicos importantes del paciente"""
        return self.antecedentes.filter(
            tipo_antecedente__in=['personal', 'quirurgico', 'alergico']
        ).order_by('-fecha_creacion')

    def obtener_alergias(self):
        """Obtiene todas las alergias del paciente"""
        return self.antecedentes.filter(tipo_antecedente='alergico')

    def obtener_medicamentos_activos(self):
        """Obtiene medicamentos activos del paciente"""
        return self.medicamentos.filter(activo=True)

    def obtener_examenes_recientes(self, dias=30):
        """Obtiene exámenes médicos recientes"""
        from datetime import date, timedelta
        fecha_limite = date.today() - timedelta(days=dias)
        return self.examenes.filter(
            fecha_solicitud__gte=fecha_limite
        ).order_by('-fecha_solicitud')

    def obtener_evolucion_reciente(self, dias=90):
        """Obtiene evolución clínica reciente"""
        from datetime import date, timedelta
        fecha_limite = date.today() - timedelta(days=dias)
        return self.evoluciones.filter(
            fecha_evolucion__gte=fecha_limite
        ).order_by('-fecha_evolucion')

    def obtener_historial_completo(self):
        """Obtiene un resumen del historial médico completo"""
        return {
            'antecedentes': self.antecedentes.all()[:10],
            'medicamentos_activos': self.obtener_medicamentos_activos(),
            'examenes_recientes': self.obtener_examenes_recientes(),
            'evolucion_reciente': self.obtener_evolucion_reciente(),
            'consultas_recientes': self.consultas.all()[:5],
        }

    def tiene_antecedentes_importantes(self):
        """Verifica si tiene antecedentes médicos importantes"""
        return self.antecedentes.filter(
            tipo_antecedente__in=['personal', 'quirurgico', 'alergico']
        ).exists()

    def tiene_alergias(self):
        """Verifica si tiene alergias registradas"""
        return self.antecedentes.filter(tipo_antecedente='alergico').exists()

    def tiene_medicamentos_activos(self):
        """Verifica si tiene medicamentos activos"""
        return self.medicamentos.filter(activo=True).exists()

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

class AntecedenteMedico(models.Model):
    """Modelo para antecedentes médicos del paciente"""
    
    TIPO_ANTECEDENTE_CHOICES = [
        ('personal', 'Personal'),
        ('familiar', 'Familiar'),
        ('quirurgico', 'Quirúrgico'),
        ('alergico', 'Alérgico'),
        ('medicamento', 'Medicamento'),
        ('habito', 'Hábito'),
        ('otro', 'Otro'),
    ]
    
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='antecedentes')
    tipo_antecedente = models.CharField(max_length=20, choices=TIPO_ANTECEDENTE_CHOICES)
    descripcion = models.TextField()
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    estado_actual = models.CharField(max_length=50, blank=True, null=True)
    severidad = models.CharField(max_length=20, choices=[
        ('leve', 'Leve'),
        ('moderado', 'Moderado'),
        ('severo', 'Severo'),
        ('crítico', 'Crítico'),
    ], blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    
    # Sistema
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Antecedente Médico"
        verbose_name_plural = "Antecedentes Médicos"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.paciente.nombre_completo()} - {self.get_tipo_antecedente_display()}"


class ExamenMedico(models.Model):
    """Modelo para exámenes médicos del paciente"""
    
    TIPO_EXAMEN_CHOICES = [
        ('laboratorio', 'Laboratorio'),
        ('imagen', 'Imagenología'),
        ('cardiovascular', 'Cardiovascular'),
        ('neurologico', 'Neurológico'),
        ('respiratorio', 'Respiratorio'),
        ('gastrointestinal', 'Gastrointestinal'),
        ('endocrino', 'Endocrino'),
        ('ginecologico', 'Ginecológico'),
        ('urologico', 'Urológico'),
        ('dermatologico', 'Dermatológico'),
        ('oftalmologico', 'Oftalmológico'),
        ('otorrino', 'Otorrinolaringológico'),
        ('ortopedico', 'Ortopédico'),
        ('psicologico', 'Psicológico'),
        ('otro', 'Otro'),
    ]
    
    ESTADO_CHOICES = [
        ('solicitado', 'Solicitado'),
        ('en_proceso', 'En Proceso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
        ('pendiente', 'Pendiente'),
    ]
    
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='examenes')
    tipo_examen = models.CharField(max_length=20, choices=TIPO_EXAMEN_CHOICES)
    nombre_examen = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    
    # Fechas
    fecha_solicitud = models.DateField(auto_now_add=True)
    fecha_realizacion = models.DateField(blank=True, null=True)
    fecha_resultado = models.DateField(blank=True, null=True)
    
    # Resultados
    resultado = models.TextField(blank=True, null=True)
    valores_normales = models.TextField(blank=True, null=True)
    interpretacion = models.TextField(blank=True, null=True)
    archivo_resultado = models.FileField(upload_to='examenes/', blank=True, null=True)
    
    # Estado y seguimiento
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='solicitado')
    laboratorio = models.CharField(max_length=100, blank=True, null=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Relación con consulta
    consulta_solicitante = models.ForeignKey('consultas.Consulta', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Sistema
    solicitado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Examen Médico"
        verbose_name_plural = "Exámenes Médicos"
        ordering = ['-fecha_solicitud']
    
    def __str__(self):
        return f"{self.paciente.nombre_completo()} - {self.nombre_examen}"


class EvolucionClinica(models.Model):
    """Modelo para evolución clínica del paciente"""
    
    TIPO_EVOLUCION_CHOICES = [
        ('mejoria', 'Mejoría'),
        ('estable', 'Estable'),
        ('empeoramiento', 'Empeoramiento'),
        ('complicacion', 'Complicación'),
        ('recuperacion', 'Recuperación'),
        ('cronico', 'Crónico'),
    ]
    
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='evoluciones')
    fecha_evolucion = models.DateField()
    tipo_evolucion = models.CharField(max_length=20, choices=TIPO_EVOLUCION_CHOICES)
    
    # Información clínica
    sintomas_actuales = models.TextField()
    signos_vitales = models.TextField(blank=True, null=True)
    examen_fisico = models.TextField(blank=True, null=True)
    diagnostico_actual = models.TextField()
    plan_tratamiento = models.TextField()
    
    # Medicamentos y seguimiento
    medicamentos_actuales = models.TextField(blank=True, null=True)
    dosis_medicamentos = models.TextField(blank=True, null=True)
    efectos_secundarios = models.TextField(blank=True, null=True)
    
    # Próximos pasos
    proxima_evaluacion = models.DateField(blank=True, null=True)
    recomendaciones = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    
    # Relación con consulta
    consulta_relacionada = models.ForeignKey('consultas.Consulta', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Sistema
    registrado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Evolución Clínica"
        verbose_name_plural = "Evoluciones Clínicas"
        ordering = ['-fecha_evolucion']
    
    def __str__(self):
        return f"{self.paciente.nombre_completo()} - {self.fecha_evolucion} - {self.get_tipo_evolucion_display()}"


class Medicamento(models.Model):
    """Modelo para medicamentos del paciente"""
    
    TIPO_MEDICAMENTO_CHOICES = [
        ('recetado', 'Recetado'),
        ('automedicacion', 'Automedicación'),
        ('suplemento', 'Suplemento'),
        ('vitamina', 'Vitamina'),
        ('otro', 'Otro'),
    ]
    
    FRECUENCIA_CHOICES = [
        ('una_vez_dia', 'Una vez al día'),
        ('dos_veces_dia', 'Dos veces al día'),
        ('tres_veces_dia', 'Tres veces al día'),
        ('cuatro_veces_dia', 'Cuatro veces al día'),
        ('cada_8_horas', 'Cada 8 horas'),
        ('cada_12_horas', 'Cada 12 horas'),
        ('cada_24_horas', 'Cada 24 horas'),
        ('segun_necesidad', 'Según necesidad'),
        ('otro', 'Otro'),
    ]
    
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='medicamentos')
    nombre_medicamento = models.CharField(max_length=200)
    principio_activo = models.CharField(max_length=200, blank=True, null=True)
    tipo_medicamento = models.CharField(max_length=20, choices=TIPO_MEDICAMENTO_CHOICES, default='recetado')
    
    # Dosis y frecuencia
    dosis = models.CharField(max_length=100)
    frecuencia = models.CharField(max_length=20, choices=FRECUENCIA_CHOICES)
    duracion_tratamiento = models.CharField(max_length=100, blank=True, null=True)
    
    # Fechas
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    
    # Estado
    activo = models.BooleanField(default=True)
    efectos_secundarios = models.TextField(blank=True, null=True)
    alergia = models.BooleanField(default=False)
    
    # Relación con consulta
    consulta_prescriptora = models.ForeignKey('consultas.Consulta', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Sistema
    prescrito_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Medicamento"
        verbose_name_plural = "Medicamentos"
        ordering = ['-fecha_inicio']
    
    def __str__(self):
        return f"{self.paciente.nombre_completo()} - {self.nombre_medicamento}"
    
    def esta_activo(self):
        """Verifica si el medicamento está activo actualmente"""
        from datetime import date
        hoy = date.today()
        if not self.activo:
            return False
        if self.fecha_fin and hoy > self.fecha_fin:
            return False
        return True
