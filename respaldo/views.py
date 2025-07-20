# respaldo/views.py
import os
from django.conf import settings
from django.http import FileResponse, HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

@user_passes_test(lambda u: u.is_superuser)
def exportar_base_datos(request):
    db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')

    if os.path.exists(db_path):
        return FileResponse(open(db_path, 'rb'), as_attachment=True, filename='respaldo_healthlife.sqlite3')

    return HttpResponseForbidden("Archivo de base de datos no encontrado.")

@user_passes_test(lambda u: u.is_superuser)
@csrf_exempt
def importar_base_datos(request):
    if request.method == 'POST' and request.FILES.get('respaldo'):
        respaldo = request.FILES['respaldo']

        if respaldo.name.endswith('.sqlite3'):
            fs = FileSystemStorage()
            filename = fs.save('nuevo_respaldo.sqlite3', respaldo)
            nuevo_path = fs.path(filename)

            try:
                base_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')
                backup_path = os.path.join(settings.BASE_DIR, 'db_backup.sqlite3')

                # Backup de la base actual antes de reemplazar
                if os.path.exists(base_path):
                    os.replace(base_path, backup_path)

                os.replace(nuevo_path, base_path)

                messages.success(request, "✅ Base de datos restaurada correctamente. Reinicia el servidor.")
            except Exception as e:
                messages.error(request, f"❌ Error al restaurar: {str(e)}")
        else:
            messages.error(request, "❌ El archivo debe tener extensión .sqlite3.")

        return redirect('dashboard_admin')

    return HttpResponseForbidden("Acceso denegado.")
