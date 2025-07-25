from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.http import FileResponse
from django.conf import settings
import os
import shutil
from datetime import datetime

from .forms import RestaurarBDForm

# Vista principal de Configuraciones
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def configuraciones(request):
    form = RestaurarBDForm()  # Carga el formulario vacío
    return render(request, 'usuarios/configuraciones.html', {'form': form})


# Vista para realizar respaldo de la base de datos
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def respaldo_base_datos(request):
    if request.method == "POST":
        db_path = settings.DATABASES['default']['NAME']
        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        os.makedirs(backup_dir, exist_ok=True)

        fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_name = f"backup_healthlife_{fecha}.sqlite3"
        backup_path = os.path.join(backup_dir, backup_name)

        shutil.copy2(db_path, backup_path)
        messages.success(request, f"✅ Respaldo creado exitosamente: {backup_name}")
        return FileResponse(open(backup_path, 'rb'), as_attachment=True, filename=backup_name)

    return redirect('configuraciones')


# Vista para restaurar base de datos
@user_passes_test(lambda u: u.is_superuser)
def restaurar_base_datos(request):
    if request.method == 'POST':
        form = RestaurarBDForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = form.cleaned_data['archivo_sqlite']
            if archivo.name.endswith('.sqlite3'):
                db_path = settings.DATABASES['default']['NAME']
                with open(db_path, 'wb+') as destino:
                    for chunk in archivo.chunks():
                        destino.write(chunk)

                messages.success(request, "✅ Base de datos restaurada. Inicia sesión nuevamente.")
                return redirect('login')  # Necesario porque pierde la sesión
            else:
                messages.error(request, "❌ El archivo debe tener extensión .sqlite3.")
    else:
        form = RestaurarBDForm()

    return render(request, 'usuarios/configuraciones.html', {'form': form})