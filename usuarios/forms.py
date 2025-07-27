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
        ('administrador', 'Administrador'),
        ('doctor', 'Doctor'),
        ('recepcionista', 'Recepcionista'),
    ])
    
    # Campos específicos para doctores
    numero_colegio = forms.CharField(
        max_length=20, 
        required=False, 
        label="Número de Colegio Médico",
        help_text="Solo para doctores"
    )
    telefono = forms.CharField(
        max_length=15, 
        required=False, 
        label="Teléfono",
        help_text="Solo para doctores"
    )
    direccion_consultorio = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}), 
        required=False, 
        label="Dirección del Consultorio",
        help_text="Solo para doctores"
    )
    foto = forms.ImageField(
        required=False, 
        label="Foto",
        help_text="Solo para doctores"
    )
    biografia = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}), 
        required=False, 
        label="Biografía",
        help_text="Solo para doctores"
    )
    estado = forms.ChoiceField(
        choices=CustomUser.ESTADOS,
        initial='activo',
        required=False,
        label="Estado",
        help_text="Solo para doctores"
    )

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
            'numero_colegio',
            'telefono',
            'direccion_consultorio',
            'foto',
            'biografia',
            'estado',
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer campos de doctor opcionales inicialmente
        self.fields['numero_colegio'].required = False
        self.fields['telefono'].required = False
        self.fields['direccion_consultorio'].required = False
        self.fields['foto'].required = False
        self.fields['biografia'].required = False
        self.fields['estado'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        rol = cleaned_data.get('rol')
        
        # Si es doctor, hacer obligatorios algunos campos
        if rol == 'doctor':
            if not cleaned_data.get('especialidad'):
                self.add_error('especialidad', 'La especialidad es obligatoria para doctores.')
            if not cleaned_data.get('numero_colegio'):
                self.add_error('numero_colegio', 'El número de colegio médico es obligatorio para doctores.')
        
        return cleaned_data


class EditarUsuarioForm(forms.ModelForm):
    """Formulario para editar usuarios existentes"""
    password = forms.CharField(
        widget=forms.PasswordInput(), 
        required=False, 
        label="Nueva Contraseña",
        help_text="Dejar vacío para mantener la contraseña actual"
    )
    
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
            'is_active',
            'numero_colegio',
            'telefono',
            'direccion_consultorio',
            'foto',
            'biografia',
            'estado',
        ]
        widgets = {
            'biografia': forms.Textarea(attrs={'rows': 4}),
            'direccion_consultorio': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer campos de doctor opcionales inicialmente
        self.fields['numero_colegio'].required = False
        self.fields['telefono'].required = False
        self.fields['direccion_consultorio'].required = False
        self.fields['foto'].required = False
        self.fields['biografia'].required = False
        self.fields['estado'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        rol = cleaned_data.get('rol')
        
        # Si es doctor, hacer obligatorios algunos campos
        if rol == 'doctor':
            if not cleaned_data.get('especialidad'):
                self.add_error('especialidad', 'La especialidad es obligatoria para doctores.')
            if not cleaned_data.get('numero_colegio'):
                self.add_error('numero_colegio', 'El número de colegio médico es obligatorio para doctores.')
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Si se proporcionó una nueva contraseña, establecerla
        if self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data['password'])
        
        if commit:
            user.save()
        return user


class RestaurarBDForm(forms.Form):
    archivo_sqlite = forms.FileField(label="Archivo de respaldo (.sqlite3)")
