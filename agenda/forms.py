from django import forms
from django.contrib.auth import get_user_model
from .models import HorarioDoctor, Cita, Disponibilidad
from pacientes.models import Paciente
from django.utils import timezone
import datetime

User = get_user_model()

class HorarioDoctorForm(forms.ModelForm):
    """Formulario para horarios de doctores"""
    
    class Meta:
        model = HorarioDoctor
        fields = ['doctor', 'dia_semana', 'hora_inicio', 'hora_fin', 'duracion_cita', 'activo']
        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo usuarios con rol de doctor
        self.fields['doctor'].queryset = User.objects.filter(rol='doctor', estado='activo')
    
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
        # Filtrar solo usuarios con rol de doctor
        self.fields['doctor'].queryset = User.objects.filter(rol='doctor', estado='activo')
        
        if self.instance.pk:
            # Si es una edición, calcular duración
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
        
        if fecha and hora_inicio and duracion:
            # Calcular hora de fin
            inicio = datetime.datetime.combine(fecha, hora_inicio)
            fin = inicio + datetime.timedelta(minutes=duracion)
            cleaned_data['hora_fin'] = fin.time()
            
            # Verificar que no sea en el pasado
            ahora = timezone.now()
            fecha_hora_cita = datetime.datetime.combine(fecha, hora_inicio)
            if fecha_hora_cita < ahora:
                raise forms.ValidationError("No se pueden crear citas en el pasado")
        
        return cleaned_data
    
    def save(self, commit=True):
        cita = super().save(commit=False)
        
        # Calcular hora de fin basada en la duración
        if cita.fecha and cita.hora_inicio and self.cleaned_data.get('duracion'):
            inicio = datetime.datetime.combine(cita.fecha, cita.hora_inicio)
            fin = inicio + datetime.timedelta(minutes=self.cleaned_data['duracion'])
            cita.hora_fin = fin.time()
        
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo usuarios con rol de doctor
        self.fields['doctor'].queryset = User.objects.filter(rol='doctor', estado='activo')
    
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
        queryset=User.objects.filter(rol='doctor', estado='activo'),
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