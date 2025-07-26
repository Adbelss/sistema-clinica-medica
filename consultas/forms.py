from django import forms
from .models import Consulta
from pacientes.models import Paciente

class ConsultaForm(forms.ModelForm):
    # Campo para seleccionar paciente con búsqueda
    paciente = forms.ModelChoiceField(
        queryset=Paciente.objects.filter(estado='Activo').order_by('primer_nombre'),
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'paciente_select'
        }),
        help_text="Selecciona el paciente para la consulta"
    )
    
    # Campos de fecha y hora
    proxima_cita = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        }),
        required=False,
        help_text="Fecha y hora de la próxima cita (opcional)"
    )
    
    # Campos de signos vitales con validación
    presion_arterial = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 120/80',
            'pattern': r'\d{2,3}/\d{2,3}'
        }),
        required=False,
        help_text="Formato: sistólica/diastólica (Ej: 120/80)"
    )
    
    temperatura = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'min': '35.0',
            'max': '42.0',
            'placeholder': '37.0'
        }),
        required=False,
        help_text="Temperatura en grados Celsius"
    )
    
    peso = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'min': '0.5',
            'max': '300.0',
            'placeholder': '70.0'
        }),
        required=False,
        help_text="Peso en kilogramos"
    )
    
    altura = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0.5',
            'max': '2.5',
            'placeholder': '1.70'
        }),
        required=False,
        help_text="Altura en metros"
    )
    
    frecuencia_cardiaca = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '40',
            'max': '200',
            'placeholder': '80'
        }),
        required=False,
        help_text="Frecuencia cardíaca en latidos por minuto"
    )
    
    # Campos de texto mejorados
    motivo = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Describa el motivo principal de la consulta'
        }),
        help_text="Motivo principal de la consulta"
    )
    
    sintomas = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Describa los síntomas presentados por el paciente'
        }),
        required=False,
        help_text="Síntomas presentados por el paciente"
    )
    
    diagnostico = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Diagnóstico médico'
        }),
        help_text="Diagnóstico médico"
    )
    
    tratamiento = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Tratamiento prescrito'
        }),
        help_text="Tratamiento prescrito"
    )
    
    medicamentos_recetados = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Lista de medicamentos prescritos'
        }),
        required=False,
        help_text="Medicamentos prescritos"
    )
    
    dosis_medicamentos = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Dosis y frecuencia de medicamentos'
        }),
        required=False,
        help_text="Dosis y frecuencia de medicamentos"
    )
    
    observaciones_cita = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Observaciones para la próxima cita'
        }),
        required=False,
        help_text="Observaciones para la próxima cita"
    )
    
    notas_adicionales = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Notas adicionales del doctor'
        }),
        required=False,
        help_text="Notas adicionales del doctor"
    )
    
    # Campos numéricos
    duracion_consulta = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '5',
            'max': '180',
            'placeholder': '30'
        }),
        required=False,
        help_text="Duración de la consulta en minutos"
    )
    
    costo_consulta = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0',
            'placeholder': '0.00'
        }),
        required=False,
        help_text="Costo de la consulta"
    )

    class Meta:
        model = Consulta
        fields = [
            'paciente', 'motivo', 'sintomas', 'diagnostico', 'tratamiento',
            'presion_arterial', 'temperatura', 'peso', 'altura', 'frecuencia_cardiaca',
            'estado', 'tipo_consulta', 'medicamentos_recetados', 'dosis_medicamentos',
            'proxima_cita', 'observaciones_cita', 'duracion_consulta', 'costo_consulta',
            'notas_adicionales'
        ]
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'tipo_consulta': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_presion_arterial(self):
        presion = self.cleaned_data.get('presion_arterial')
        if presion:
            try:
                sistolica, diastolica = map(int, presion.split('/'))
                if sistolica < 60 or sistolica > 200:
                    raise forms.ValidationError("La presión sistólica debe estar entre 60 y 200")
                if diastolica < 40 or diastolica > 130:
                    raise forms.ValidationError("La presión diastólica debe estar entre 40 y 130")
                if sistolica <= diastolica:
                    raise forms.ValidationError("La presión sistólica debe ser mayor que la diastólica")
            except ValueError:
                raise forms.ValidationError("Formato inválido. Use: sistólica/diastólica (Ej: 120/80)")
        return presion

    def clean_temperatura(self):
        temp = self.cleaned_data.get('temperatura')
        if temp and (temp < 35.0 or temp > 42.0):
            raise forms.ValidationError("La temperatura debe estar entre 35.0°C y 42.0°C")
        return temp

    def clean_peso(self):
        peso = self.cleaned_data.get('peso')
        if peso and (peso < 0.5 or peso > 300.0):
            raise forms.ValidationError("El peso debe estar entre 0.5 kg y 300.0 kg")
        return peso

    def clean_altura(self):
        altura = self.cleaned_data.get('altura')
        if altura and (altura < 0.5 or altura > 2.5):
            raise forms.ValidationError("La altura debe estar entre 0.5 m y 2.5 m")
        return altura

    def clean_frecuencia_cardiaca(self):
        fc = self.cleaned_data.get('frecuencia_cardiaca')
        if fc and (fc < 40 or fc > 200):
            raise forms.ValidationError("La frecuencia cardíaca debe estar entre 40 y 200 lpm")
        return fc

    def clean(self):
        cleaned_data = super().clean()
        peso = cleaned_data.get('peso')
        altura = cleaned_data.get('altura')
        
        # Calcular IMC automáticamente si se proporcionan peso y altura
        if peso and altura:
            imc = peso / (altura ** 2)
            if imc < 10 or imc > 60:
                self.add_error(None, "Los valores de peso y altura resultan en un IMC fuera del rango normal (10-60)")
        
        return cleaned_data
