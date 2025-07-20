# respaldo/views.py
import os
from django.conf import settings
from django.http import FileResponse, HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)
def exportar_base_datos(request):
    db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')
    
    if os.path.exists(db_path):
        return FileResponse(open(db_path, 'rb'), as_attachment=True, filename='respaldo_healthlife.sqlite3')
    
    return HttpResponseForbidden("Archivo de base de datos no encontrado.")
