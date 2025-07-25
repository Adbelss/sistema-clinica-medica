from django import forms
from .models import Paciente
from django.forms.widgets import DateInput


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'

        widgets = {
            'fecha_nacimiento': DateInput(attrs={'type': 'date'}),
            'fecha_donacion': DateInput(attrs={'type': 'date'}),
            'direccion': forms.Textarea(attrs={'rows': 2}),
            'notas': forms.Textarea(attrs={'rows': 3}),
            'comentarios_donacion': forms.Textarea(attrs={'rows': 2}),
        }

        labels = {
            'primer_nombre': 'Primer Nombre',
            'otros_nombres': 'Otros Nombres',
            'primer_apellido': 'Primer Apellido',
            'segundo_apellido': 'Segundo Apellido',
            'apellido_casada': 'Apellido de Casada',
            'documento_identidad': 'Documento de Identificación',
            'tipo_documento': 'Tipo de Documento',
            'nit': 'NIT',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'genero': 'Género',
            'profesion': 'Profesión',
            'alergias': 'Alergias',
            'grupo_sanguineo': 'Grupo Sanguíneo',
            'correo': 'Correo Electrónico',
            'telefono': 'Teléfono',
            'notificacion_whatsapp': 'Recibir notificaciones por WhatsApp',
            'notificacion_email': 'Recibir notificaciones por Correo',
            'notificacion_sms': 'Recibir notificaciones por SMS',
            'direccion': 'Dirección',
            'ciudad': 'Ciudad/Municipio',
            'pais': 'País',
            'zona_residencia': 'Zona de Residencia',
            'codigo_postal': 'Código Postal',
            'enviar_recordatorio': 'Enviar recordatorio automático',
            'estado': 'Estado',
            'notas': 'Notas / Observaciones',
            'nacionalidad': 'Nacionalidad',
            'identidad_genero': 'Identidad de Género',
            'discapacidad': 'Discapacidad',
            'es_donador': '¿Es Donador?',
            'fecha_donacion': 'Fecha de Donación',
            'comentarios_donacion': 'Comentarios Donación',
            'ocupacion': 'Ocupación',
            'tipo_paciente': 'Tipo de Paciente',
        }
