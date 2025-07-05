from django.shortcuts import render, redirect
from .forms import ConsultaForm

def registrar_consulta(request):
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.doctor = request.user
            consulta.save()
            return redirect('home')  # O redirige donde prefieras
    else:
        form = ConsultaForm()
    return render(request, 'consultas/registrar_consulta.html', {'form': form})
