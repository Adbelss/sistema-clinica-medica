from django import forms
from .models import Consulta

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['paciente_nombre', 'motivo', 'diagnostico', 'tratamiento']
