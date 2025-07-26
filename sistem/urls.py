from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

from consultas.views import dashboard
from usuarios.views import custom_login, custom_logout, validate_credentials

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),  # Página principal: dashboard
    path('consultas/', include('consultas.urls')),

    # Configuraciones y gestión de usuarios
    path('usuarios/', include('usuarios.urls')),

    # Login/Logout Personalizado con Seguridad Avanzada
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('api/validate-credentials/', validate_credentials, name='validate_credentials'),

    # Recuperación de contraseña
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset.html'), name='password_reset'),
    
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

    # Respaldo
    path('respaldo/', include('respaldo.urls')),

    # Pacientes 
    path('pacientes/', include('pacientes.urls')),
    
    # Agenda
    path('agenda/', include('agenda.urls')),
]
