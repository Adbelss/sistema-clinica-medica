from django.shortcuts import render, redirect
from .models import Paciente
from .forms import PacienteForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

# Vista principal de pacientes
@login_required
def listar_pacientes(request):
    pacientes = Paciente.objects.all().order_by('-fecha_creacion')  # últimos primero
    form = PacienteForm()

    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Paciente registrado exitosamente.")
            return redirect('listar_pacientes')
        else:
            messages.error(request, "❌ Ocurrió un error al registrar el paciente. Revisa los campos.")

    context = {
        'pacientes': pacientes,
        'form': form,
    }
    return render(request, 'pacientes/listar_pacientes.html', context)

# Vista para guardar desde el modal
@require_POST
def crear_paciente(request):
    primer_nombre = request.POST.get('primer_nombre')
    otros_nombres = request.POST.get('otros_nombres')
    primer_apellido = request.POST.get('primer_apellido')
    segundo_apellido = request.POST.get('segundo_apellido')
    apellido_casada = request.POST.get('apellido_casada')
    telefono = request.POST.get('celular')
    notif_whatsapp = bool(request.POST.get('notificar_whatsapp'))
    notif_email = bool(request.POST.get('notificar_correo'))
    notif_sms = bool(request.POST.get('notificar_sms'))

    # Validación básica
    if not primer_nombre or not primer_apellido or not telefono:
        messages.error(request, "❌ Todos los campos obligatorios deben ser llenados.")
        return redirect('listar_pacientes')

    # Crear el paciente
    paciente = Paciente(
        primer_nombre=primer_nombre,
        otros_nombres=otros_nombres,
        primer_apellido=primer_apellido,
        segundo_apellido=segundo_apellido,
        apellido_casada=apellido_casada,
        telefono=telefono,
        notificacion_whatsapp=notif_whatsapp,
        notificacion_email=notif_email,
        notificacion_sms=notif_sms,
        # Campos necesarios con valores por defecto
        documento_identidad='DPI-PENDIENTE',
        tipo_documento='DPI',
        nit='CF',
        fecha_nacimiento='2000-01-01',
        genero='M'
    )
    paciente.save()
    messages.success(request, "✅ Paciente creado exitosamente.")
    return redirect('listar_pacientes')
