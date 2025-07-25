from django.shortcuts import render, redirect
from .models import Paciente
from .forms import PacienteForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


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
