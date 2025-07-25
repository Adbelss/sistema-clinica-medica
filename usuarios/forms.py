# usuarios/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from usuarios.models import CustomUser  # Asegúrate que el modelo está bien definido


class CrearUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(label="Nombres", max_length=100)
    last_name = forms.CharField(label="Apellidos", max_length=100)
    especialidad = forms.CharField(required=False)
    firma_digital = forms.FileField(required=False)
    is_active = forms.BooleanField(initial=True, label="Activo", required=False)
    rol = forms.ChoiceField(choices=[
        ('Admin', 'Admin'),
        ('Doctor', 'Doctor'),
        ('Asistente', 'Asistente')
    ])

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'especialidad',
            'firma_digital',
            'rol',
            'password1',
            'password2',
            'is_active',
        ]


class RestaurarBDForm(forms.Form):
    archivo_sqlite = forms.FileField(label="Archivo de respaldo (.sqlite3)")
