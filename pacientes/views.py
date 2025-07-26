from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages

from .models import Paciente
from .forms import PacienteForm

# ✅ LISTAR PACIENTES
@login_required
def listar_pacientes(request):
    pacientes = Paciente.objects.all().order_by('-fecha_creacion')
    
    # Crear formulario para el modal
    form = PacienteForm()
    
    # Definir agrupación de campos por secciones (estilo MediCloud mejorado)
    campos_generales = [
        'primer_nombre', 'otros_nombres', 'primer_apellido', 'segundo_apellido',
        'apellido_casada', 'genero', 'fecha_nacimiento', 'grupo_sanguineo',
        'tipo_documento', 'documento_identificacion', 'nit', 'nacionalidad',
        'profesion', 'ocupacion', 'discapacidad', 'tipo_paciente', 'estado_civil'
    ]
    
    campos_direccion = [
        'direccion', 'ciudad', 'zona', 'codigo_postal', 'pais'
    ]
    
    campos_telefonos = [
        'telefono', 'correo', 'notificar_whatsapp', 'notificar_correo', 'notificar_sms',
        'contacto_emergencia', 'telefono_emergencia', 'parentesco_emergencia'
    ]
    
    campos_admin = [
        'estado', 'enviar_recordatorio', 'creado_por'
    ]
    
    campos_extras = [
        'alergias', 'es_donador', 'comentarios_donacion', 'fecha_donacion', 'notas'
    ]
    
    context = {
        'pacientes': pacientes,
        'form': form,
        'campos_generales': campos_generales,
        'campos_direccion': campos_direccion,
        'campos_telefonos': campos_telefonos,
        'campos_admin': campos_admin,
        'campos_extras': campos_extras,
    }
    
    return render(request, 'pacientes/listar_pacientes.html', context)

# ✅ NUEVO PACIENTE (modal)
@login_required
def nuevo_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save(commit=False)
            paciente.creado_por = request.user
            paciente.save()
            messages.success(request, f'✅ Paciente {paciente.nombre_completo()} creado exitosamente.')
            return redirect('listar_pacientes')
        else:
            messages.error(request, '❌ Error al crear el paciente. Por favor revisa los datos.')
    else:
        form = PacienteForm()
    
    # Definir agrupación de campos por secciones (estilo MediCloud mejorado)
    campos_generales = [
        'primer_nombre', 'otros_nombres', 'primer_apellido', 'segundo_apellido',
        'apellido_casada', 'genero', 'fecha_nacimiento', 'grupo_sanguineo',
        'tipo_documento', 'documento_identificacion', 'nit', 'nacionalidad',
        'profesion', 'ocupacion', 'discapacidad', 'tipo_paciente', 'estado_civil'
    ]
    
    campos_direccion = [
        'direccion', 'ciudad', 'zona', 'codigo_postal', 'pais'
    ]
    
    campos_telefonos = [
        'telefono', 'correo', 'notificar_whatsapp', 'notificar_correo', 'notificar_sms',
        'contacto_emergencia', 'telefono_emergencia', 'parentesco_emergencia'
    ]
    
    campos_admin = [
        'estado', 'enviar_recordatorio', 'creado_por'
    ]
    
    campos_extras = [
        'alergias', 'es_donador', 'comentarios_donacion', 'fecha_donacion', 'notas'
    ]
    
    context = {
        'form': form,
        'campos_generales': campos_generales,
        'campos_direccion': campos_direccion,
        'campos_telefonos': campos_telefonos,
        'campos_admin': campos_admin,
        'campos_extras': campos_extras,
    }
    
    return render(request, 'pacientes/nuevo_modal.html', context)

# ✅ EDITAR PACIENTE
@login_required
def editar_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            paciente = form.save(commit=False)
            paciente.creado_por = request.user
            paciente.save()
            messages.success(request, f'✅ Paciente {paciente.nombre_completo()} actualizado exitosamente.')
            return redirect('listar_pacientes')
        else:
            messages.error(request, '❌ Error al actualizar el paciente. Por favor revisa los datos.')
    else:
        form = PacienteForm(instance=paciente)
    
    context = {
        'form': form,
        'paciente': paciente,
    }
    
    return render(request, 'pacientes/editar_paciente.html', context)

# ✅ ELIMINAR PACIENTE
@login_required
def eliminar_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    nombre_paciente = paciente.nombre_completo()
    
    try:
        paciente.delete()
        messages.success(request, f'✅ Paciente {nombre_paciente} eliminado exitosamente.')
    except Exception as e:
        messages.error(request, f'❌ Error al eliminar el paciente: {str(e)}')
    
    return redirect('listar_pacientes')
