from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ConsultaForm
from .models import Consulta

# Vista para registrar una nueva consulta
@login_required
def registrar_consulta(request):
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.doctor = request.user
            consulta.save()
            return redirect('home')  # Puedes cambiar esto si deseas redirigir al dashboard
    else:
        form = ConsultaForm()
    return render(request, 'consultas/registrar_consulta.html', {'form': form})

# Vista del dashboard con estadísticas
@login_required
def dashboard(request):
    total_consultas = Consulta.objects.count()
    usuario = request.user

    context = {
        'total_consultas': total_consultas,
        'usuario': usuario,
    }
    return render(request, 'consultas/dashboard.html', context)
