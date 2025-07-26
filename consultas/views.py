from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.contrib.auth import get_user_model
from django.db.models import Q, Count, Avg
from django.utils import timezone
from datetime import datetime, timedelta

from .forms import ConsultaForm
from .models import Consulta
from pacientes.models import Paciente

import openpyxl
from xhtml2pdf import pisa


# ----------------------------
# Vista para registrar una nueva consulta
# ----------------------------
@login_required
def registrar_consulta(request):
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.doctor = request.user
            
            # Calcular duración automáticamente si no se especifica
            if not consulta.duracion_consulta:
                consulta.duracion_consulta = consulta.calcular_duracion_consulta()
            
            consulta.save()
            messages.success(request, f"✅ Consulta registrada exitosamente para {consulta.paciente.nombre_completo()}.")
            return redirect('listar_consultas')
        else:
            messages.error(request, "❌ Hubo un error al registrar la consulta. Por favor revisa los datos.")
    else:
        form = ConsultaForm()
    
    # Obtener estadísticas para mostrar en el formulario
    total_pacientes = Paciente.objects.filter(estado='Activo').count()
    consultas_hoy = Consulta.objects.filter(fecha__date=timezone.now().date()).count()
    
    context = {
        'form': form,
        'total_pacientes': total_pacientes,
        'consultas_hoy': consultas_hoy,
    }
    return render(request, 'consultas/registrar_consulta.html', context)


# ----------------------------
# Vista del Dashboard mejorado
# ----------------------------
@login_required
def dashboard(request):
    # Estadísticas básicas
    total_consultas = Consulta.objects.count()
    total_pacientes = Paciente.objects.filter(estado='Activo').count()
    usuario = request.user.get_full_name() or request.user.username
    
    # Estadísticas por fecha
    hoy = timezone.now().date()
    consultas_hoy = Consulta.objects.filter(fecha__date=hoy).count()
    consultas_semana = Consulta.objects.filter(fecha__date__gte=hoy - timedelta(days=7)).count()
    consultas_mes = Consulta.objects.filter(fecha__date__gte=hoy - timedelta(days=30)).count()
    
    # Consultas de emergencia
    consultas_emergencia = Consulta.objects.filter(tipo_consulta='Emergencia').count()
    
    # Duración promedio
    duracion_promedio = Consulta.objects.aggregate(
        promedio=Avg('duracion_consulta')
    )['promedio'] or 30
    
    # Consultas recientes
    ultimas_consultas = Consulta.objects.select_related('paciente').order_by('-fecha')[:5]
    
    # Estadísticas por tipo de consulta
    tipos_consulta = Consulta.objects.values('tipo_consulta').annotate(
        total=Count('id')
    ).order_by('-total')[:5]
    
    # Pacientes con más consultas
    pacientes_frecuentes = Paciente.objects.annotate(
        total_consultas=Count('consultas')
    ).filter(total_consultas__gt=0).order_by('-total_consultas')[:5]
    
    # Alertas médicas recientes
    consultas_recientes = Consulta.objects.select_related('paciente').filter(
        fecha__date__gte=hoy - timedelta(days=7)
    )
    alertas = []
    for consulta in consultas_recientes:
        alertas.extend(consulta.obtener_alertas_medicas())
    
    # Próximas citas
    proximas_citas = Consulta.objects.select_related('paciente').filter(
        proxima_cita__gte=timezone.now()
    ).order_by('proxima_cita')[:5]

    # Fecha actual formateada
    from datetime import datetime
    fecha_actual = datetime.now().strftime("%A, %d de %B de %Y")

    context = {
        'total_consultas': total_consultas,
        'total_pacientes': total_pacientes,
        'consultas_hoy': consultas_hoy,
        'consultas_semana': consultas_semana,
        'consultas_mes': consultas_mes,
        'consultas_emergencia': consultas_emergencia,
        'duracion_promedio': round(duracion_promedio, 1),
        'usuario': usuario,
        'fecha_actual': fecha_actual,
        'ultimas_consultas': ultimas_consultas,
        'tipos_consulta': tipos_consulta,
        'pacientes_frecuentes': pacientes_frecuentes,
        'alertas': alertas[:10],  # Máximo 10 alertas
        'proximas_citas': proximas_citas,
    }
    return render(request, 'consultas/dashboard.html', context)


# ----------------------------
# Vista para listar todas las consultas
# ----------------------------
@login_required
def listar_consultas(request):
    # Filtros de búsqueda
    paciente_query = request.GET.get('paciente', '').strip()
    fecha_query = request.GET.get('fecha', '').strip()
    doctor_query = request.GET.get('doctor', '').strip()
    tipo_query = request.GET.get('tipo', '').strip()
    estado_query = request.GET.get('estado', '').strip()

    consultas = Consulta.objects.select_related('paciente', 'doctor').all().order_by('-fecha')

    # Aplicar filtros
    if paciente_query:
        consultas = consultas.filter(
            Q(paciente__primer_nombre__icontains=paciente_query) |
            Q(paciente__primer_apellido__icontains=paciente_query) |
            Q(paciente__documento_identificacion__icontains=paciente_query)
        )
    if fecha_query:
        consultas = consultas.filter(fecha__date=fecha_query)
    if doctor_query:
        consultas = consultas.filter(doctor__id=doctor_query)
    if tipo_query:
        consultas = consultas.filter(tipo_consulta=tipo_query)
    if estado_query:
        consultas = consultas.filter(estado=estado_query)

    # Paginación
    paginator = Paginator(consultas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Datos para filtros
    User = get_user_model()
    doctores = User.objects.all()
    tipos_consulta = Consulta.TIPO_CHOICES
    estados_consulta = Consulta.ESTADO_CHOICES

    # Estadísticas de filtros
    total_filtrado = consultas.count()
    consultas_emergencia = consultas.filter(tipo_consulta='Emergencia').count()
    consultas_pendientes = consultas.filter(estado='Programada').count()

    # Crear formulario para el modal
    form = ConsultaForm()

    context = {
        'consultas': page_obj,
        'paciente_query': paciente_query,
        'fecha_query': fecha_query,
        'doctor_query': doctor_query,
        'tipo_query': tipo_query,
        'estado_query': estado_query,
        'doctores': doctores,
        'tipos_consulta': tipos_consulta,
        'estados_consulta': estados_consulta,
        'page_obj': page_obj,
        'total_filtrado': total_filtrado,
        'consultas_emergencia': consultas_emergencia,
        'consultas_pendientes': consultas_pendientes,
        'form': form,  # Agregar formulario para el modal
    }
    return render(request, 'consultas/listar_consultas.html', context)


# ----------------------------
# Vista para editar una consulta
# ----------------------------
@login_required
def editar_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    if consulta.doctor != request.user:
        messages.error(request, "🚫 No tienes permiso para editar esta consulta.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = ConsultaForm(request.POST, instance=consulta)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.fecha_actualizacion = timezone.now()
            
            # Calcular duración automáticamente si no se especifica
            if not consulta.duracion_consulta:
                consulta.duracion_consulta = consulta.calcular_duracion_consulta()
            
            consulta.save()
            messages.success(request, f'✏️ Consulta actualizada correctamente para {consulta.paciente.nombre_completo()}.')
            return redirect('listar_consultas')
        else:
            messages.error(request, "❌ Error al actualizar la consulta.")
    else:
        form = ConsultaForm(instance=consulta)
    
    # Obtener historial del paciente
    historial_consultas = consulta.obtener_historial_consultas()
    
    context = {
        'form': form,
        'consulta': consulta,
        'historial_consultas': historial_consultas,
    }
    return render(request, 'consultas/editar_consulta.html', context)


# ----------------------------
# Vista para eliminar una consulta
# ----------------------------
@login_required
def eliminar_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    if consulta.doctor != request.user:
        messages.error(request, "🚫 No tienes permiso para eliminar esta consulta.")
        return redirect('dashboard')

    if request.method == 'POST':
        paciente_nombre = consulta.paciente.nombre_completo()
        consulta.delete()
        messages.success(request, f'🗑️ Consulta eliminada correctamente para {paciente_nombre}.')
        return redirect('listar_consultas')
    return render(request, 'consultas/eliminar_confirmar.html', {'consulta': consulta})


# ----------------------------
# Vista para ver detalles individuales de una consulta
# ----------------------------
@login_required
def detalle_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    if consulta.doctor != request.user:
        messages.error(request, "🚫 No tienes permiso para ver esta consulta.")
        return redirect('dashboard')

    # Obtener datos adicionales
    historial_consultas = consulta.obtener_historial_consultas()
    estadisticas_vitales = consulta.obtener_estadisticas_vitales()
    alertas_medicas = consulta.obtener_alertas_medicas()

    context = {
        'consulta': consulta,
        'historial_consultas': historial_consultas,
        'estadisticas_vitales': estadisticas_vitales,
        'alertas_medicas': alertas_medicas,
    }
    return render(request, 'consultas/detalle_consulta.html', context)


# ----------------------------
# Vista para búsqueda rápida de pacientes (AJAX)
# ----------------------------
@login_required
def buscar_pacientes(request):
    query = request.GET.get('q', '').strip()
    if len(query) < 2:
        return JsonResponse({'pacientes': []})
    
    pacientes = Paciente.objects.filter(
        Q(primer_nombre__icontains=query) |
        Q(primer_apellido__icontains=query) |
        Q(documento_identificacion__icontains=query),
        estado='Activo'
    )[:10]
    
    resultados = []
    for paciente in pacientes:
        resultados.append({
            'id': paciente.id,
            'nombre': paciente.nombre_completo(),
            'documento': paciente.documento_identificacion,
            'edad': paciente.edad(),
            'telefono': paciente.telefono,
        })
    
    return JsonResponse({'pacientes': resultados})


# ----------------------------
# Vista para estadísticas de consultas
# ----------------------------
@login_required
def estadisticas_consultas(request):
    # Estadísticas generales
    total_consultas = Consulta.objects.count()
    consultas_mes = Consulta.objects.filter(
        fecha__month=timezone.now().month
    ).count()
    
    # Promedios
    duracion_promedio = Consulta.objects.aggregate(
        promedio=Avg('duracion_consulta')
    )['promedio'] or 0
    
    costo_promedio = Consulta.objects.aggregate(
        promedio=Avg('costo_consulta')
    )['promedio'] or 0
    
    # Consultas por tipo
    consultas_por_tipo = Consulta.objects.values('tipo_consulta').annotate(
        total=Count('id')
    ).order_by('-total')
    
    # Consultas por estado
    consultas_por_estado = Consulta.objects.values('estado').annotate(
        total=Count('id')
    ).order_by('-total')
    
    # Top doctores
    doctores_top = Consulta.objects.values('doctor__first_name', 'doctor__last_name').annotate(
        total=Count('id')
    ).order_by('-total')[:5]
    
    context = {
        'total_consultas': total_consultas,
        'consultas_mes': consultas_mes,
        'duracion_promedio': round(duracion_promedio, 1),
        'costo_promedio': round(costo_promedio, 2),
        'consultas_por_tipo': consultas_por_tipo,
        'consultas_por_estado': consultas_por_estado,
        'doctores_top': doctores_top,
    }
    return render(request, 'consultas/estadisticas.html', context)


# ----------------------------
# Exportar consultas a PDF mejorado
# ----------------------------
@login_required
def exportar_consultas_pdf(request):
    consultas = Consulta.objects.select_related('paciente', 'doctor').all().order_by('-fecha')
    template_path = 'consultas/pdf_consultas.html'
    context = {'consultas': consultas}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="consultas_medicas.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa.CreatePDF(html, dest=response)
    return response


# ----------------------------
# Exportar consultas a Excel mejorado
# ----------------------------
@login_required
def exportar_consultas_excel(request):
    consultas = Consulta.objects.select_related('paciente', 'doctor').all().order_by('-fecha')
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Consultas Médicas"

    # Encabezados mejorados
    ws.append([
        '#', 'Paciente', 'Documento', 'Edad', 'Motivo', 'Diagnóstico', 'Tratamiento',
        'Tipo', 'Estado', 'Signos Vitales', 'IMC', 'Fecha', 'Doctor', 'Duración (min)', 'Costo'
    ])

    for idx, c in enumerate(consultas, 1):
        # Preparar signos vitales
        signos_vitales = []
        if c.presion_arterial:
            signos_vitales.append(f"PA: {c.presion_arterial}")
        if c.temperatura:
            signos_vitales.append(f"Temp: {c.temperatura}°C")
        if c.frecuencia_cardiaca:
            signos_vitales.append(f"FC: {c.frecuencia_cardiaca} lpm")
        
        signos_str = " | ".join(signos_vitales) if signos_vitales else "No registrados"
        
        ws.append([
            idx,
            c.paciente.nombre_completo(),
            c.paciente.documento_identificacion,
            c.paciente.edad(),
            c.motivo,
            c.diagnostico,
            c.tratamiento,
            c.tipo_consulta,
            c.estado,
            signos_str,
            c.calcular_imc() or "N/A",
            c.fecha.strftime("%d/%m/%Y %H:%M"),
            c.doctor.get_full_name() or c.doctor.username,
            c.duracion_consulta or "N/A",
            c.costo_consulta or "0.00"
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=consultas_medicas.xlsx'
    wb.save(response)
    return response


# ----------------------------
# Manejador personalizado de error 403
# ----------------------------
def error_403(request, exception=None):
    return render(request, '403.html', status=403)
