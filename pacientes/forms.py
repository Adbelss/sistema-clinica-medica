from django import forms
from .models import Paciente

class PacienteForm(forms.ModelForm):
    # Campos de fecha con mejor UX
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'placeholder': 'Selecciona fecha de nacimiento'
        }),
        label="Fecha de Nacimiento",
        help_text="Se calculará automáticamente la edad"
    )
    
    fecha_donacion = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        required=False,
        label="Fecha de Donación"
    )

    # Mejoras en campos de texto con autocompletado
    primer_nombre = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Juan Carlos',
            'autocomplete': 'given-name'
        }),
        help_text="Ingresa el primer nombre del paciente"
    )
    
    primer_apellido = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: García López',
            'autocomplete': 'family-name'
        }),
        help_text="Ingresa el primer apellido del paciente"
    )

    # Comboboxes inteligentes
    tipo_documento = forms.ChoiceField(
        choices=[
            ('DPI', 'DPI - Documento Personal de Identificación'),
            ('Pasaporte', 'Pasaporte'),
            ('Carné de Extranjería', 'Carné de Extranjería'),
            ('Otro', 'Otro documento'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'tipo_documento_select'
        }),
        help_text="Selecciona el tipo de documento de identificación"
    )

    genero = forms.ChoiceField(
        choices=[
            ('Masculino', 'Masculino'),
            ('Femenino', 'Femenino'),
            ('No binario', 'No binario'),
            ('Prefiero no decir', 'Prefiero no decir'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'genero_select'
        })
    )

    grupo_sanguineo = forms.ChoiceField(
        choices=[
            ('', 'Selecciona grupo sanguíneo'),
            ('A+', 'A+'),
            ('A-', 'A-'),
            ('B+', 'B+'),
            ('B-', 'B-'),
            ('AB+', 'AB+'),
            ('AB-', 'AB-'),
            ('O+', 'O+'),
            ('O-', 'O-'),
            ('No disponible', 'No disponible'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'grupo_sanguineo_select'
        }),
        required=False
    )

    nacionalidad = forms.ChoiceField(
        choices=[
            ('Guatemalteca', 'Guatemalteca'),
            ('Estadounidense', 'Estadounidense'),
            ('Mexicana', 'Mexicana'),
            ('Salvadoreña', 'Salvadoreña'),
            ('Hondureña', 'Hondureña'),
            ('Nicaragüense', 'Nicaragüense'),
            ('Costarricense', 'Costarricense'),
            ('Panameña', 'Panameña'),
            ('Beliceña', 'Beliceña'),
            ('Colombiana', 'Colombiana'),
            ('Venezolana', 'Venezolana'),
            ('Ecuatoriana', 'Ecuatoriana'),
            ('Peruana', 'Peruana'),
            ('Chilena', 'Chilena'),
            ('Argentina', 'Argentina'),
            ('Uruguaya', 'Uruguaya'),
            ('Paraguaya', 'Paraguaya'),
            ('Boliviana', 'Boliviana'),
            ('Española', 'Española'),
            ('Otra', 'Otra nacionalidad'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'nacionalidad_select'
        })
    )

    ciudad = forms.ChoiceField(
        choices=[
            ('', 'Selecciona ciudad'),
            ('Ciudad de Guatemala', 'Ciudad de Guatemala'),
            ('Antigua Guatemala', 'Antigua Guatemala'),
            ('Quetzaltenango', 'Quetzaltenango'),
            ('Escuintla', 'Escuintla'),
            ('Chimaltenango', 'Chimaltenango'),
            ('Sacatepéquez', 'Sacatepéquez'),
            ('Chiquimula', 'Chiquimula'),
            ('Jalapa', 'Jalapa'),
            ('Jutiapa', 'Jutiapa'),
            ('Santa Rosa', 'Santa Rosa'),
            ('Sololá', 'Sololá'),
            ('Totonicapán', 'Totonicapán'),
            ('Huehuetenango', 'Huehuetenango'),
            ('Quiché', 'Quiché'),
            ('Baja Verapaz', 'Baja Verapaz'),
            ('Alta Verapaz', 'Alta Verapaz'),
            ('Petén', 'Petén'),
            ('Izabal', 'Izabal'),
            ('Zacapa', 'Zacapa'),
            ('El Progreso', 'El Progreso'),
            ('Suchitepéquez', 'Suchitepéquez'),
            ('Retalhuleu', 'Retalhuleu'),
            ('San Marcos', 'San Marcos'),
            ('Otra', 'Otra ciudad'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'ciudad_select'
        })
    )

    zona = forms.ChoiceField(
        choices=[
            ('', 'Selecciona zona'),
            ('Zona 1', 'Zona 1 - Centro Histórico'),
            ('Zona 2', 'Zona 2 - Centro Cívico'),
            ('Zona 3', 'Zona 3 - Barrio San José'),
            ('Zona 4', 'Zona 4 - Centro Comercial'),
            ('Zona 5', 'Zona 5 - Cementerio General'),
            ('Zona 6', 'Zona 6 - Terminal de Buses'),
            ('Zona 7', 'Zona 7 - Colonia Utatlán'),
            ('Zona 8', 'Zona 8 - Villa de Guadalupe'),
            ('Zona 9', 'Zona 9 - Zona Viva'),
            ('Zona 10', 'Zona 10 - Zona Rosa'),
            ('Zona 11', 'Zona 11 - Colonia El Naranjo'),
            ('Zona 12', 'Zona 12 - Kaminal Juyú'),
            ('Zona 13', 'Zona 13 - Aurora'),
            ('Zona 14', 'Zona 14 - Zona Viva'),
            ('Zona 15', 'Zona 15 - Vista Hermosa'),
            ('Zona 16', 'Zona 16 - Colonia Bethania'),
            ('Zona 17', 'Zona 17 - Colonia Primero de Julio'),
            ('Zona 18', 'Zona 18 - Villa Nueva'),
            ('Zona 19', 'Zona 19 - Colonia La Florida'),
            ('Zona 20', 'Zona 20 - Colonia La Verbena'),
            ('Zona 21', 'Zona 21 - Colonia Justo Rufino Barrios'),
            ('Zona 22', 'Zona 22 - Colonia San José Las Rosas'),
            ('Zona 23', 'Zona 23 - Colonia San José Las Rosas'),
            ('Zona 24', 'Zona 24 - Colonia San José Las Rosas'),
            ('Zona 25', 'Zona 25 - Colonia San José Las Rosas'),
            ('Otra', 'Otra zona'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'zona_select'
        }),
        required=False
    )

    profesion = forms.ChoiceField(
        choices=[
            ('', 'Selecciona profesión'),
            ('Médico', 'Médico'),
            ('Enfermero/a', 'Enfermero/a'),
            ('Ingeniero', 'Ingeniero'),
            ('Abogado', 'Abogado'),
            ('Contador', 'Contador'),
            ('Profesor', 'Profesor'),
            ('Estudiante', 'Estudiante'),
            ('Comerciante', 'Comerciante'),
            ('Empleado público', 'Empleado público'),
            ('Empleado privado', 'Empleado privado'),
            ('Empresario', 'Empresario'),
            ('Agricultor', 'Agricultor'),
            ('Ganadero', 'Ganadero'),
            ('Pescador', 'Pescador'),
            ('Minería', 'Minería'),
            ('Construcción', 'Construcción'),
            ('Transporte', 'Transporte'),
            ('Turismo', 'Turismo'),
            ('Tecnología', 'Tecnología'),
            ('Arte', 'Arte'),
            ('Deportes', 'Deportes'),
            ('Religión', 'Religión'),
            ('Jubilado', 'Jubilado'),
            ('Ama de casa', 'Ama de casa'),
            ('Desempleado', 'Desempleado'),
            ('Otra', 'Otra profesión'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'profesion_select'
        }),
        required=False
    )

    # Campos de contacto mejorados
    telefono = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 502 1234-5678',
            'pattern': '[0-9+\-\s\(\)]+',
            'title': 'Ingresa un número de teléfono válido'
        }),
        help_text="Formato: 502 1234-5678 o (502) 1234-5678"
    )

    correo = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ejemplo@correo.com',
            'autocomplete': 'email'
        }),
        help_text="Ingresa un correo electrónico válido"
    )

    # Campos de salud mejorados
    alergias = forms.ChoiceField(
        choices=[
            ('', 'Selecciona alergias'),
            ('Ninguna', 'Ninguna alergia conocida'),
            ('Penicilina', 'Penicilina'),
            ('Amoxicilina', 'Amoxicilina'),
            ('Ibuprofeno', 'Ibuprofeno'),
            ('Paracetamol', 'Paracetamol'),
            ('Aspirina', 'Aspirina'),
            ('Látex', 'Látex'),
            ('Polen', 'Polen'),
            ('Ácaros', 'Ácaros'),
            ('Polvo', 'Polvo'),
            ('Mariscos', 'Mariscos'),
            ('Maní', 'Maní'),
            ('Lácteos', 'Lácteos'),
            ('Huevos', 'Huevos'),
            ('Gluten', 'Gluten'),
            ('Múltiples', 'Múltiples alergias'),
            ('Otra', 'Otra alergia'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'alergias_select'
        }),
        required=False
    )

    # Campos de estado civil (nuevo)
    estado_civil = forms.ChoiceField(
        choices=[
            ('', 'Selecciona estado civil'),
            ('Soltero/a', 'Soltero/a'),
            ('Casado/a', 'Casado/a'),
            ('Divorciado/a', 'Divorciado/a'),
            ('Viudo/a', 'Viudo/a'),
            ('Unión libre', 'Unión libre'),
            ('Separado/a', 'Separado/a'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'estado_civil_select'
        }),
        required=False
    )

    # Campos de emergencia (nuevo)
    contacto_emergencia = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre del contacto de emergencia'
        }),
        required=False,
        help_text="Persona a contactar en caso de emergencia"
    )

    telefono_emergencia = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Teléfono de emergencia'
        }),
        required=False,
        help_text="Teléfono del contacto de emergencia"
    )

    parentesco_emergencia = forms.ChoiceField(
        choices=[
            ('', 'Selecciona parentesco'),
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
            ('Otro', 'Otro'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'parentesco_emergencia_select'
        }),
        required=False
    )

    class Meta:
        model = Paciente
        fields = '__all__'
        widgets = {
            'otros_nombres': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Otros nombres (opcional)'
            }),
            'segundo_apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Segundo apellido (opcional)'
            }),
            'apellido_casada': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido de casada (opcional)'
            }),
            'documento_identificacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de documento'
            }),
            'nit': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'NIT o CF'
            }),
            'identidad_genero': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Identidad de género (opcional)'
            }),
            'ocupacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ocupación actual'
            }),
            'discapacidad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Discapacidad (si aplica)'
            }),
            'tipo_paciente': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tipo de paciente'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Dirección completa'
            }),
            'codigo_postal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código postal'
            }),
            'pais': forms.TextInput(attrs={
                'class': 'form-control',
                'value': 'Guatemala'
            }),
            'comentarios_donacion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Comentarios sobre donación'
            }),
            'notas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Notas adicionales sobre el paciente'
            }),
        }

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono:
            # Limpiar el teléfono de caracteres especiales
            telefono = ''.join(filter(str.isdigit, telefono))
            if len(telefono) < 8:
                raise forms.ValidationError("El número de teléfono debe tener al menos 8 dígitos.")
        return telefono

    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data.get('fecha_nacimiento')
        if fecha:
            from datetime import date
            hoy = date.today()
            edad = hoy.year - fecha.year - ((hoy.month, hoy.day) < (fecha.month, fecha.day))
            if edad < 0:
                raise forms.ValidationError("La fecha de nacimiento no puede ser en el futuro.")
            if edad > 150:
                raise forms.ValidationError("La fecha de nacimiento parece ser incorrecta.")
        return fecha
