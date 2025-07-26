from django import forms
from django.contrib.auth import get_user_model
from .models import Doctor, HorarioDoctor, Cita, Disponibilidad
from pacientes.models import Paciente
from django.utils import timezone
import datetime

User = get_user_model()

class DoctorForm(forms.ModelForm):
    """Formulario para crear/editar doctores"""
    first_name = forms.CharField(max_length=30, label="Nombre")
    last_name = forms.CharField(max_length=30, label="Apellido")
    email = forms.EmailField(label="Correo Electrónico")
    username = forms.CharField(max_length=150, label="Nombre de Usuario")
    password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña", required=False)
    
    class Meta:
        model = Doctor
        fields = [
            'first_name', 'last_name', 'email', 'username', 'password',
            'especialidad', 'numero_colegio', 'telefono', 'direccion_consultorio',
            'estado', 'foto', 'biografia'
        ]
        widgets = {
            'biografia': forms.Textarea(attrs={'rows': 4}),
            'direccion_consultorio': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Si es una edición, cargar datos del usuario
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            self.fields['username'].initial = self.instance.user.username
            self.fields['password'].required = False
            self.fields['password'].help_text = "Dejar vacío para mantener la contraseña actual"
    
    def save(self, commit=True):
        doctor = super().save(commit=False)
        
        if self.instance.pk:
            # Actualizar usuario existente
            user = self.instance.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.username = self.cleaned_data['username']
            
            if self.cleaned_data['password']:
                user.set_password(self.cleaned_data['password'])
            
            user.save()
        else:
            # Crear nuevo usuario
            user = User.objects.create_user(
                username=self.cleaned_data['username'],
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name']
            )
            doctor.user = user
        
        if commit:
            doctor.save()
        return doctor

class HorarioDoctorForm(forms.ModelForm):
    """Formulario para horarios de doctores"""
    
    class Meta:
        model = HorarioDoctor
        fields = ['dia_semana', 'hora_inicio', 'hora_fin', 'duracion_cita', 'activo']
        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')
        
        if hora_inicio and hora_fin and hora_inicio >= hora_fin:
            raise forms.ValidationError("La hora de inicio debe ser menor que la hora de fin")
        
        return cleaned_data

class CitaForm(forms.ModelForm):
    """Formulario para crear/editar citas"""
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=timezone.now().date()
    )
    hora_inicio = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'})
    )
    duracion = forms.IntegerField(
        min_value=15,
        max_value=120,
        initial=30,
        help_text="Duración en minutos"
    )
    
    class Meta:
        model = Cita
        fields = [
            'paciente', 'doctor', 'fecha', 'hora_inicio', 'duracion',
            'tipo_cita', 'estado', 'motivo', 'notas'
        ]
        widgets = {
            'motivo': forms.Textarea(attrs={'rows': 3}),
            'notas': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar doctores activos
        self.fields['doctor'].queryset = Doctor.objects.filter(estado='activo')
        
        if self.instance.pk:
            # Si es edición, calcular duración
            if self.instance.hora_inicio and self.instance.hora_fin:
                inicio = datetime.datetime.combine(datetime.date.today(), self.instance.hora_inicio)
                fin = datetime.datetime.combine(datetime.date.today(), self.instance.hora_fin)
                duracion = int((fin - inicio).total_seconds() / 60)
                self.fields['duracion'].initial = duracion
    
    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        hora_inicio = cleaned_data.get('hora_inicio')
        duracion = cleaned_data.get('duracion')
        doctor = cleaned_data.get('doctor')
        
        if fecha and hora_inicio and duracion:
            # Calcular hora de fin
            inicio_dt = datetime.datetime.combine(fecha, hora_inicio)
            fin_dt = inicio_dt + datetime.timedelta(minutes=duracion)
            hora_fin = fin_dt.time()
            
            # Verificar que no sea en el pasado
            ahora = timezone.now()
            if fecha < ahora.date() or (fecha == ahora.date() and hora_inicio < ahora.time()):
                raise forms.ValidationError("No se pueden programar citas en el pasado")
            
            # Verificar conflictos de horario
            if doctor:
                conflictos = Cita.objects.filter(
                    doctor=doctor,
                    fecha=fecha,
                    estado__in=['programada', 'confirmada', 'en_proceso']
                )
                if self.instance.pk:
                    conflictos = conflictos.exclude(pk=self.instance.pk)
                
                for conflicto in conflictos:
                    if (hora_inicio < conflicto.hora_fin and hora_fin > conflicto.hora_inicio):
                        raise forms.ValidationError(
                            f"Conflicto de horario con cita existente: {conflicto.paciente.nombre_completo} "
                            f"({conflicto.hora_inicio} - {conflicto.hora_fin})"
                        )
            
            cleaned_data['hora_fin'] = hora_fin
        
        return cleaned_data
    
    def save(self, commit=True):
        cita = super().save(commit=False)
        
        # Calcular hora de fin
        if self.cleaned_data.get('duracion'):
            inicio_dt = datetime.datetime.combine(cita.fecha, cita.hora_inicio)
            fin_dt = inicio_dt + datetime.timedelta(minutes=self.cleaned_data['duracion'])
            cita.hora_fin = fin_dt.time()
        
        if commit:
            cita.save()
        return cita

class DisponibilidadForm(forms.ModelForm):
    """Formulario para disponibilidad de doctores"""
    fecha_inicio = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=timezone.now().date()
    )
    fecha_fin = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=timezone.now().date()
    )
    
    class Meta:
        model = Disponibilidad
        fields = ['doctor', 'tipo', 'fecha_inicio', 'fecha_fin', 'motivo', 'activo']
        widgets = {
            'motivo': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        
        if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
            raise forms.ValidationError("La fecha de inicio debe ser menor o igual que la fecha de fin")
        
        return cleaned_data

class BusquedaCitaForm(forms.Form):
    """Formulario para buscar citas"""
    fecha_inicio = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Fecha desde"
    )
    fecha_fin = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Fecha hasta"
    )
    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.filter(estado='activo'),
        required=False,
        empty_label="Todos los doctores"
    )
    paciente = forms.ModelChoiceField(
        queryset=Paciente.objects.all(),
        required=False,
        empty_label="Todos los pacientes"
    )
    estado = forms.ChoiceField(
        choices=[('', 'Todos los estados')] + Cita.ESTADOS_CITA,
        required=False
    )
    tipo_cita = forms.ChoiceField(
        choices=[('', 'Todos los tipos')] + Cita.TIPOS_CITA,
        required=False
    ) 