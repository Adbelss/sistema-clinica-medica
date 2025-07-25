# usuarios/forms.py

from django import forms

class RestaurarBDForm(forms.Form):
    archivo_sqlite = forms.FileField(label="Archivo de respaldo (.sqlite3)")
