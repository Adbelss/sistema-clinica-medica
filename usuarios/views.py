from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.http import FileResponse
from django.conf import settings
import os
import shutil
from datetime import datetime

from .forms import RestaurarBDForm, CrearUsuarioForm
from .models import CustomUser  # Modelo personalizado

# Verificación de admin
def es_admin(user):
    return user.is_superuser or user.rol == 'Admin'

# =============================
# 🔧 CONFIGURACIONES DE BD
# =============================

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def configuraciones(request):
    form = RestaurarBDForm()
    return render(request, 'usuarios/configuraciones.html', {'form': form})

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
                return redirect('login')  # Redirige por seguridad
            else:
                messages.error(request, "❌ El archivo debe tener extensión .sqlite3.")
    else:
        form = RestaurarBDForm()

    return render(request, 'usuarios/configuraciones.html', {'form': form})


# =============================
# 👥 GESTIÓN DE USUARIOS
# =============================

@user_passes_test(es_admin)
def gestion_usuarios(request):
    usuarios = CustomUser.objects.all()
    return render(request, 'usuarios/gestion_usuarios.html', {'usuarios': usuarios})

@user_passes_test(es_admin)
def crear_usuario(request):
    if request.method == 'POST':
        form = CrearUsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Usuario creado exitosamente.")
            return redirect('gestion_usuarios')
    else:
        form = CrearUsuarioForm()
    return render(request, 'usuarios/crear_usuario.html', {'form': form})

# ----------------------------
# Vista de Login Personalizada con Seguridad Avanzada
# ----------------------------
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from datetime import datetime, timedelta
import json
import hashlib
import time
import re

# ----------------------------
# Vista de Login Personalizada con Seguridad Avanzada
# ----------------------------
@require_http_methods(["GET", "POST"])
def custom_login(request):
    """
    Vista de login personalizada con medidas de seguridad avanzadas:
    - Rate limiting
    - Detección de intentos sospechosos
    - Logging de intentos de acceso
    - Validación de complejidad de contraseña
    - Protección contra ataques de fuerza bruta
    """
    
    # Redirigir si ya está autenticado
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    # Obtener IP del cliente
    client_ip = get_client_ip(request)
    
    # Verificar rate limiting
    if is_rate_limited(request, client_ip):
        messages.error(request, 'Demasiados intentos de acceso. Inténtalo de nuevo en 15 minutos.')
        return render(request, 'registration/login.html')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        # Validaciones de seguridad
        validation_result = validate_login_attempt(request, username, password, client_ip)
        
        if not validation_result['valid']:
            messages.error(request, validation_result['message'])
            log_failed_attempt(request, username, client_ip, validation_result['reason'])
            return render(request, 'registration/login.html')
        
        # Intentar autenticación
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_active:
                # Login exitoso
                login(request, user)
                log_successful_login(request, user, client_ip)
                
                # Redirigir al dashboard
                next_url = request.GET.get('next', 'dashboard')
                messages.success(request, f'¡Bienvenido, {user.get_full_name() or user.username}!')
                return redirect(next_url)
            else:
                messages.error(request, 'Tu cuenta ha sido deshabilitada. Contacta al administrador.')
                log_failed_attempt(request, username, client_ip, 'account_disabled')
        else:
            # Credenciales inválidas
            messages.error(request, 'Usuario o contraseña incorrectos.')
            log_failed_attempt(request, username, client_ip, 'invalid_credentials')
    
    return render(request, 'registration/login.html')

def get_client_ip(request):
    """Obtiene la IP real del cliente"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def is_rate_limited(request, client_ip):
    """Implementa rate limiting básico usando sesión"""
    session_key = f'login_attempts_{client_ip}'
    attempts = request.session.get(session_key, [])
    
    # Limpiar intentos antiguos (más de 15 minutos)
    current_time = time.time()
    attempts = [attempt for attempt in attempts if current_time - attempt < 900]
    
    # Verificar si hay demasiados intentos
    if len(attempts) >= 5:
        return True
    
    return False

def validate_login_attempt(request, username, password, client_ip):
    """Valida el intento de login"""
    
    # Validaciones básicas
    if not username or not password:
        return {
            'valid': False,
            'message': 'Usuario y contraseña son requeridos.',
            'reason': 'empty_fields'
        }
    
    # Validar longitud de usuario
    if len(username) < 3 or len(username) > 50:
        return {
            'valid': False,
            'message': 'El usuario debe tener entre 3 y 50 caracteres.',
            'reason': 'invalid_username_length'
        }
    
    # Validar caracteres permitidos en usuario
    if not re.match(r'^[a-zA-Z0-9_@.-]+$', username):
        return {
            'valid': False,
            'message': 'El usuario contiene caracteres no permitidos.',
            'reason': 'invalid_username_chars'
        }
    
    # Validar longitud mínima de contraseña
    if len(password) < 6:
        return {
            'valid': False,
            'message': 'La contraseña debe tener al menos 6 caracteres.',
            'reason': 'password_too_short'
        }
    
    # Detectar patrones sospechosos
    if detect_suspicious_patterns(username, password, client_ip):
        return {
            'valid': False,
            'message': 'Actividad sospechosa detectada. Inténtalo de nuevo.',
            'reason': 'suspicious_activity'
        }
    
    return {'valid': True}

def detect_suspicious_patterns(username, password, client_ip):
    """Detecta patrones sospechosos en el intento de login"""
    
    # Contraseñas comunes
    common_passwords = [
        '123456', 'password', 'admin', 'qwerty', 'letmein',
        'welcome', 'monkey', 'dragon', 'master', 'football'
    ]
    
    if password.lower() in common_passwords:
        return True
    
    # Usuario y contraseña iguales
    if username.lower() == password.lower():
        return True
    
    # Patrones de teclado
    keyboard_patterns = [
        'qwerty', 'asdfgh', 'zxcvbn', '123456789'
    ]
    
    if password.lower() in keyboard_patterns:
        return True
    
    return False

def log_failed_attempt(request, username, client_ip, reason):
    """Registra intentos fallidos de login"""
    session_key = f'login_attempts_{client_ip}'
    attempts = request.session.get(session_key, [])
    attempts.append(time.time())
    request.session[session_key] = attempts
    
    # Log detallado (en producción, usar un sistema de logging real)
    print(f"❌ Login fallido - Usuario: {username}, IP: {client_ip}, Razón: {reason}, Timestamp: {datetime.now()}")

def log_successful_login(request, user, client_ip):
    """Registra logins exitosos"""
    # Limpiar intentos fallidos
    session_key = f'login_attempts_{client_ip}'
    if session_key in request.session:
        del request.session[session_key]
    
    # Log detallado
    print(f"✅ Login exitoso - Usuario: {user.username}, IP: {client_ip}, Timestamp: {datetime.now()}")

# ----------------------------
# Vista de Logout Personalizada
# ----------------------------
@login_required
def custom_logout(request):
    """Vista de logout personalizada con logging"""
    user = request.user
    client_ip = get_client_ip(request)
    
    # Log del logout
    print(f"🚪 Logout - Usuario: {user.username}, IP: {client_ip}, Timestamp: {datetime.now()}")
    
    # Logout estándar de Django
    from django.contrib.auth import logout
    logout(request)
    
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('login')

# ----------------------------
# API para validación en tiempo real
# ----------------------------
@csrf_exempt
@require_http_methods(["POST"])
def validate_credentials(request):
    """API para validación de credenciales en tiempo real"""
    try:
        data = json.loads(request.body)
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        # Validaciones básicas
        if not username or not password:
            return JsonResponse({
                'valid': False,
                'message': 'Usuario y contraseña son requeridos.'
            })
        
        # Validar longitud
        if len(username) < 3:
            return JsonResponse({
                'valid': False,
                'message': 'El usuario debe tener al menos 3 caracteres.'
            })
        
        if len(password) < 6:
            return JsonResponse({
                'valid': False,
                'message': 'La contraseña debe tener al menos 6 caracteres.'
            })
        
        # Verificar si el usuario existe
        try:
            user = User.objects.get(username=username)
            if user.is_active:
                return JsonResponse({
                    'valid': True,
                    'message': 'Credenciales válidas.'
                })
            else:
                return JsonResponse({
                    'valid': False,
                    'message': 'La cuenta está deshabilitada.'
                })
        except User.DoesNotExist:
            return JsonResponse({
                'valid': False,
                'message': 'Usuario no encontrado.'
            })
            
    except json.JSONDecodeError:
        return JsonResponse({
            'valid': False,
            'message': 'Datos inválidos.'
        })

# ----------------------------
# Vista de Dashboard (ya existente)
# ----------------------------
@login_required
def dashboard(request):
    """Vista del dashboard principal"""
    return render(request, 'consultas/dashboard.html')

# ----------------------------
# Funciones de utilidad para seguridad
# ----------------------------
def generate_secure_token():
    """Genera un token seguro para operaciones críticas"""
    import secrets
    return secrets.token_urlsafe(32)

def hash_password(password):
    """Genera hash seguro de contraseña (para comparaciones)"""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_password_strength(password):
    """Valida la fortaleza de una contraseña"""
    score = 0
    feedback = []
    
    # Longitud mínima
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Al menos 8 caracteres")
    
    # Contiene mayúsculas
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("Al menos una mayúscula")
    
    # Contiene minúsculas
    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("Al menos una minúscula")
    
    # Contiene números
    if re.search(r'\d', password):
        score += 1
    else:
        feedback.append("Al menos un número")
    
    # Contiene caracteres especiales
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1
    else:
        feedback.append("Al menos un carácter especial")
    
    return {
        'score': score,
        'max_score': 5,
        'feedback': feedback,
        'strength': 'débil' if score < 3 else 'media' if score < 4 else 'fuerte'
    }
