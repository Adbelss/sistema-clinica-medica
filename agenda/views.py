from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from datetime import datetime, timedelta, date
import calendar

from .models import HorarioDoctor, Cita, Disponibilidad
from .forms import HorarioDoctorForm, CitaForm, DisponibilidadForm, BusquedaCitaForm
from pacientes.models import Paciente
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def agenda_dashboard(request):
    """Dashboard principal de la agenda"""
    hoy = timezone.now().date()
    
    # Estadísticas
    total_citas_hoy = Cita.objects.filter(fecha=hoy).count()
    citas_pendientes = Cita.objects.filter(
        fecha__gte=hoy,
        estado__in=['programada', 'confirmada']
    ).count()
    doctores_activos = User.objects.filter(rol='doctor', estado='activo').count()
    
    # Próximas citas
    proximas_citas = Cita.objects.filter(
        fecha__gte=hoy,
        estado__in=['programada', 'confirmada']
    ).order_by('fecha', 'hora_inicio')[:10]
    
    # Citas de hoy
    citas_hoy = Cita.objects.filter(
        fecha=hoy
    ).order_by('hora_inicio')
    
    # Doctores con más citas esta semana
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    fin_semana = inicio_semana + timedelta(days=6)
    
    doctores_ocupados = User.objects.filter(
        rol='doctor',
        citas__fecha__range=[inicio_semana, fin_semana],
        citas__estado__in=['programada', 'confirmada']
    ).annotate(
        total_citas=Count('citas')
    ).order_by('-total_citas')[:5]
    
    context = {
        'total_citas_hoy': total_citas_hoy,
        'citas_pendientes': citas_pendientes,
        'doctores_activos': doctores_activos,
        'proximas_citas': proximas_citas,
        'citas_hoy': citas_hoy,
        'doctores_ocupados': doctores_ocupados,
        'hoy': hoy,
    }
    
    return render(request, 'agenda/dashboard.html', context)

@login_required
def calendario(request):
    """Vista de calendario mensual"""
    # Obtener mes y año de la URL o usar el actual
    year = request.GET.get('year', timezone.now().year)
    month = request.GET.get('month', timezone.now().month)
    
    try:
        year = int(year)
        month = int(month)
    except ValueError:
        year = timezone.now().year
        month = timezone.now().month
    
    # Crear calendario
    cal = calendar.monthcalendar(year, month)
    
    # Obtener citas del mes
    inicio_mes = date(year, month, 1)
    if month == 12:
        fin_mes = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        fin_mes = date(year, month + 1, 1) - timedelta(days=1)
    
    citas_mes = Cita.objects.filter(
        fecha__range=[inicio_mes, fin_mes]
    ).select_related('paciente', 'doctor')
    
    # Organizar citas por día
    citas_por_dia = {}
    for cita in citas_mes:
        if cita.fecha not in citas_por_dia:
            citas_por_dia[cita.fecha] = []
        citas_por_dia[cita.fecha].append(cita)
    
    # Navegación del calendario
    if month == 1:
        mes_anterior = 12
        año_anterior = year - 1
    else:
        mes_anterior = month - 1
        año_anterior = year
    
    if month == 12:
        mes_siguiente = 1
        año_siguiente = year + 1
    else:
        mes_siguiente = month + 1
        año_siguiente = year
    
    # Obtener doctores para filtros
    doctores = User.objects.filter(rol='doctor', estado='activo')
    
    context = {
        'calendario': cal,
        'citas_por_dia': citas_por_dia,
        'year': year,
        'month': month,
        'mes_anterior': mes_anterior,
        'año_anterior': año_anterior,
        'mes_siguiente': mes_siguiente,
        'año_siguiente': año_siguiente,
        'nombre_mes': calendar.month_name[month],
        'doctores': doctores,
    }
    
    return render(request, 'agenda/calendario.html', context)

@login_required
def listar_citas(request):
    """Lista de citas con filtros"""
    citas = Cita.objects.select_related('paciente', 'doctor').all()
    
    # Aplicar filtros
    form = BusquedaCitaForm(request.GET)
    if form.is_valid():
        if form.cleaned_data.get('fecha_inicio'):
            citas = citas.filter(fecha__gte=form.cleaned_data['fecha_inicio'])
        if form.cleaned_data.get('fecha_fin'):
            citas = citas.filter(fecha__lte=form.cleaned_data['fecha_fin'])
        if form.cleaned_data.get('doctor'):
            citas = citas.filter(doctor=form.cleaned_data['doctor'])
        if form.cleaned_data.get('paciente'):
            citas = citas.filter(paciente=form.cleaned_data['paciente'])
        if form.cleaned_data.get('estado'):
            citas = citas.filter(estado=form.cleaned_data['estado'])
        if form.cleaned_data.get('tipo_cita'):
            citas = citas.filter(tipo_cita=form.cleaned_data['tipo_cita'])
    
    # Paginación
    paginator = Paginator(citas, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Obtener doctores para filtros
    doctores = User.objects.filter(rol='doctor', estado='activo')
    
    context = {
        'page_obj': page_obj,
        'form': form,
        'doctores': doctores,
    }
    
    return render(request, 'agenda/listar_citas.html', context)

@login_required
def nueva_cita(request):
    """Crear nueva cita"""
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.creado_por = request.user
            cita.save()
            messages.success(request, 'Cita creada exitosamente.')
            return redirect('listar_citas')
    else:
        form = CitaForm()
    
    context = {
        'form': form,
        'titulo': 'Nueva Cita',
    }
    
    return render(request, 'agenda/form_cita.html', context)

@login_required
def editar_cita(request, pk):
    """Editar cita existente"""
    cita = get_object_or_404(Cita, pk=pk)
    
    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cita actualizada exitosamente.')
            return redirect('listar_citas')
    else:
        form = CitaForm(instance=cita)
    
    context = {
        'form': form,
        'cita': cita,
        'titulo': 'Editar Cita',
    }
    
    return render(request, 'agenda/form_cita.html', context)

@login_required
def eliminar_cita(request, pk):
    """Eliminar cita"""
    cita = get_object_or_404(Cita, pk=pk)
    
    if request.method == 'POST':
        cita.delete()
        messages.success(request, 'Cita eliminada exitosamente.')
        return redirect('listar_citas')
    
    context = {
        'cita': cita,
    }
    
    return render(request, 'agenda/eliminar_cita.html', context)

@login_required
def cambiar_estado_cita(request, pk):
    """Cambiar estado de una cita"""
    cita = get_object_or_404(Cita, pk=pk)
    nuevo_estado = request.POST.get('estado')
    
    if nuevo_estado in dict(Cita.ESTADOS_CITA):
        cita.estado = nuevo_estado
        cita.save()
        messages.success(request, f'Estado de cita cambiado a {cita.get_estado_display()}.')
    
    return redirect('listar_citas')

@login_required
def horarios_doctor(request, pk):
    """Gestionar horarios de un doctor"""
    doctor = get_object_or_404(User, pk=pk, rol='doctor')
    horarios = HorarioDoctor.objects.filter(doctor=doctor)
    
    if request.method == 'POST':
        form = HorarioDoctorForm(request.POST)
        if form.is_valid():
            horario = form.save(commit=False)
            horario.doctor = doctor
            horario.save()
            messages.success(request, 'Horario agregado exitosamente.')
            return redirect('horarios_doctor', pk=pk)
    else:
        form = HorarioDoctorForm(initial={'doctor': doctor})
    
    context = {
        'doctor': doctor,
        'horarios': horarios,
        'form': form,
    }
    
    return render(request, 'agenda/horarios_doctor.html', context)

@login_required
def eliminar_horario(request, pk):
    """Eliminar horario de doctor"""
    horario = get_object_or_404(HorarioDoctor, pk=pk)
    doctor_pk = horario.doctor.pk
    
    if request.method == 'POST':
        horario.delete()
        messages.success(request, 'Horario eliminado exitosamente.')
    
    return redirect('horarios_doctor', pk=doctor_pk)

@login_required
def disponibilidad_doctores(request):
    """Gestión de disponibilidad de doctores"""
    disponibilidades = Disponibilidad.objects.select_related('doctor').filter(activo=True)
    
    # Obtener doctores para el formulario
    doctores = User.objects.filter(rol='doctor', estado='activo')
    
    # Estadísticas
    total_doctores = doctores.count()
    doctores_disponibles = User.objects.filter(
        rol='doctor', 
        estado='activo'
    ).exclude(
        disponibilidades__activo=True,
        disponibilidades__fecha_inicio__lte=timezone.now().date(),
        disponibilidades__fecha_fin__gte=timezone.now().date()
    ).count()
    
    if request.method == 'POST':
        form = DisponibilidadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Disponibilidad registrada exitosamente.')
            return redirect('disponibilidad_doctores')
    else:
        form = DisponibilidadForm()
    
    context = {
        'disponibilidades': disponibilidades,
        'form': form,
        'doctores': doctores,
        'total_doctores': total_doctores,
        'doctores_disponibles': doctores_disponibles,
    }
    
    return render(request, 'agenda/disponibilidad_doctores.html', context)

@login_required
def api_citas_dia(request):
    """API para obtener citas de un día específico"""
    fecha = request.GET.get('fecha')
    doctor_id = request.GET.get('doctor')
    
    try:
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        fecha_obj = timezone.now().date()
    
    citas = Cita.objects.filter(fecha=fecha_obj)
    
    if doctor_id:
        citas = citas.filter(doctor_id=doctor_id)
    
    citas_data = []
    for cita in citas:
        citas_data.append({
            'id': cita.pk,
            'paciente': cita.paciente.nombre_completo,
            'doctor': cita.doctor.nombre_completo,
            'hora_inicio': cita.hora_inicio.strftime('%H:%M'),
            'hora_fin': cita.hora_fin.strftime('%H:%M'),
            'estado': cita.get_estado_display(),
            'tipo': cita.get_tipo_cita_display(),
        })
    
    return JsonResponse({'citas': citas_data})

@login_required
def api_horarios_disponibles(request):
    """API para obtener horarios disponibles de un doctor en una fecha"""
    doctor_id = request.GET.get('doctor')
    fecha = request.GET.get('fecha')
    
    try:
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
        doctor = User.objects.get(pk=doctor_id, rol='doctor')
    except (ValueError, TypeError, User.DoesNotExist):
        return JsonResponse({'error': 'Parámetros inválidos'}, status=400)
    
    # Obtener día de la semana (0=Lunes, 6=Domingo)
    dia_semana = fecha_obj.weekday()
    
    # Buscar horario del doctor para ese día
    try:
        horario = HorarioDoctor.objects.get(doctor=doctor, dia_semana=dia_semana, activo=True)
    except HorarioDoctor.DoesNotExist:
        return JsonResponse({'error': 'No hay horario disponible para este día'}, status=404)
    
    # Obtener citas existentes para ese día
    citas_existentes = Cita.objects.filter(
        doctor=doctor,
        fecha=fecha_obj,
        estado__in=['programada', 'confirmada']
    ).order_by('hora_inicio')
    
    # Calcular slots disponibles
    slots_disponibles = []
    hora_actual = horario.hora_inicio
    
    while hora_actual < horario.hora_fin:
        hora_fin_slot = (datetime.combine(date.today(), hora_actual) + 
                        timedelta(minutes=horario.duracion_cita)).time()
        
        # Verificar si hay conflicto con citas existentes
        conflicto = False
        for cita in citas_existentes:
            if (hora_actual < cita.hora_fin and hora_fin_slot > cita.hora_inicio):
                conflicto = True
                break
        
        if not conflicto:
            slots_disponibles.append({
                'hora_inicio': hora_actual.strftime('%H:%M'),
                'hora_fin': hora_fin_slot.strftime('%H:%M'),
            })
        
        hora_actual = hora_fin_slot
    
    return JsonResponse({
        'horario': {
            'hora_inicio': horario.hora_inicio.strftime('%H:%M'),
            'hora_fin': horario.hora_fin.strftime('%H:%M'),
            'duracion_cita': horario.duracion_cita,
        },
        'slots_disponibles': slots_disponibles,
    })
