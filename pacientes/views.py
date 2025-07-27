from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q, Count, Max

from .models import Paciente
from .forms import PacienteForm

# ✅ LISTAR PACIENTES
@login_required
def listar_pacientes(request):
    pacientes = Paciente.objects.all().order_by('-fecha_creacion')
    
    # Crear formulario para el modal
    form = PacienteForm()
    
    # Definir agrupación de campos por secciones (estilo MediCloud mejorado)
    campos_generales = [
        'primer_nombre', 'otros_nombres', 'primer_apellido', 'segundo_apellido',
        'apellido_casada', 'genero', 'fecha_nacimiento', 'grupo_sanguineo',
        'tipo_documento', 'documento_identificacion', 'nit', 'nacionalidad',
        'profesion', 'ocupacion', 'discapacidad', 'tipo_paciente', 'estado_civil'
    ]
    
    campos_direccion = [
        'direccion', 'ciudad', 'zona', 'codigo_postal', 'pais'
    ]
    
    campos_telefonos = [
        'telefono', 'correo', 'notificar_whatsapp', 'notificar_correo', 'notificar_sms',
        'contacto_emergencia', 'telefono_emergencia', 'parentesco_emergencia'
    ]
    
    campos_admin = [
        'estado', 'enviar_recordatorio', 'creado_por'
    ]
    
    campos_extras = [
        'alergias', 'es_donador', 'comentarios_donacion', 'fecha_donacion', 'notas'
    ]
    
    context = {
        'pacientes': pacientes,
        'form': form,
        'campos_generales': campos_generales,
        'campos_direccion': campos_direccion,
        'campos_telefonos': campos_telefonos,
        'campos_admin': campos_admin,
        'campos_extras': campos_extras,
    }
    
    return render(request, 'pacientes/listar_pacientes.html', context)

# ✅ NUEVO PACIENTE (modal)
@login_required
def nuevo_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save(commit=False)
            paciente.creado_por = request.user
            paciente.save()
            messages.success(request, f'✅ Paciente {paciente.nombre_completo()} creado exitosamente.')
            return redirect('listar_pacientes')
        else:
            messages.error(request, '❌ Error al crear el paciente. Por favor revisa los datos.')
    else:
        form = PacienteForm()
    
    # Definir agrupación de campos por secciones (estilo MediCloud mejorado)
    campos_generales = [
        'primer_nombre', 'otros_nombres', 'primer_apellido', 'segundo_apellido',
        'apellido_casada', 'genero', 'fecha_nacimiento', 'grupo_sanguineo',
        'tipo_documento', 'documento_identificacion', 'nit', 'nacionalidad',
        'profesion', 'ocupacion', 'discapacidad', 'tipo_paciente', 'estado_civil'
    ]
    
    campos_direccion = [
        'direccion', 'ciudad', 'zona', 'codigo_postal', 'pais'
    ]
    
    campos_telefonos = [
        'telefono', 'correo', 'notificar_whatsapp', 'notificar_correo', 'notificar_sms',
        'contacto_emergencia', 'telefono_emergencia', 'parentesco_emergencia'
    ]
    
    campos_admin = [
        'estado', 'enviar_recordatorio', 'creado_por'
    ]
    
    campos_extras = [
        'alergias', 'es_donador', 'comentarios_donacion', 'fecha_donacion', 'notas'
    ]
    
    context = {
        'form': form,
        'campos_generales': campos_generales,
        'campos_direccion': campos_direccion,
        'campos_telefonos': campos_telefonos,
        'campos_admin': campos_admin,
        'campos_extras': campos_extras,
    }
    
    return render(request, 'pacientes/nuevo_paciente.html', context)

# ✅ EDITAR PACIENTE
@login_required
def editar_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            paciente = form.save(commit=False)
            paciente.creado_por = request.user
            paciente.save()
            messages.success(request, f'✅ Paciente {paciente.nombre_completo()} actualizado exitosamente.')
            return redirect('listar_pacientes')
        else:
            messages.error(request, '❌ Error al actualizar el paciente. Por favor revisa los datos.')
    else:
        form = PacienteForm(instance=paciente)
    
    context = {
        'form': form,
        'paciente': paciente,
    }
    
    return render(request, 'pacientes/editar_paciente.html', context)

# ✅ ELIMINAR PACIENTE
@login_required
def eliminar_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    nombre_paciente = paciente.nombre_completo()
    
    try:
        paciente.delete()
        messages.success(request, f'✅ Paciente {nombre_paciente} eliminado exitosamente.')
    except Exception as e:
        messages.error(request, f'❌ Error al eliminar el paciente: {str(e)}')
    
    return redirect('listar_pacientes')

# ========================================
# VISTAS PARA HISTORIAL MÉDICO
# ========================================

@login_required
def historial_medico(request, paciente_id=None):
    """Vista principal del historial médico del paciente"""
    if paciente_id:
        paciente = get_object_or_404(Paciente, id=paciente_id)
        
        # Obtener datos del historial
        antecedentes = paciente.antecedentes.all().order_by('-fecha_creacion')
        medicamentos_activos = paciente.obtener_medicamentos_activos()
        examenes_recientes = paciente.obtener_examenes_recientes()
        evoluciones_recientes = paciente.obtener_evolucion_reciente()
        consultas_recientes = paciente.consultas.all().order_by('-fecha')[:10]
        
        # Estadísticas del historial
        total_consultas = paciente.consultas.count()
        total_examenes = paciente.examenes.count()
        total_medicamentos = paciente.medicamentos.count()
        
        # Alertas médicas
        alertas = []
        if paciente.tiene_alergias():
            alertas.append({
                'tipo': 'alergia',
                'mensaje': 'Paciente con alergias registradas',
                'severidad': 'alta'
            })
        
        if medicamentos_activos.count() > 5:
            alertas.append({
                'tipo': 'medicamentos',
                'mensaje': f'Paciente con {medicamentos_activos.count()} medicamentos activos',
                'severidad': 'media'
            })
        
        context = {
            'paciente': paciente,
            'antecedentes': antecedentes,
            'medicamentos_activos': medicamentos_activos,
            'examenes_recientes': examenes_recientes,
            'evoluciones_recientes': evoluciones_recientes,
            'consultas_recientes': consultas_recientes,
            'total_consultas': total_consultas,
            'total_examenes': total_examenes,
            'total_medicamentos': total_medicamentos,
            'alertas': alertas,
        }
        
        return render(request, 'pacientes/historial_medico.html', context)
    else:
        # Si no hay paciente_id, mostrar formulario de búsqueda
        return render(request, 'pacientes/buscar_historial.html')


@login_required
def buscar_paciente_historial(request):
    """Vista para buscar pacientes por historial médico"""
    query = request.GET.get('q', '')
    pacientes = []
    
    if query:
        pacientes = Paciente.objects.filter(
            Q(primer_nombre__icontains=query) |
            Q(primer_apellido__icontains=query) |
            Q(documento_identificacion__icontains=query) |
            Q(telefono__icontains=query)
        ).annotate(
            total_consultas=Count('consultas'),
            ultima_consulta=Max('consultas__fecha'),
            medicamentos_activos=Count('medicamentos', filter=Q(medicamentos__activo=True))
        ).order_by('-ultima_consulta')[:20]
    
    return JsonResponse({
        'pacientes': list(pacientes.values('id', 'primer_nombre', 'primer_apellido', 'documento_identificacion', 'telefono', 'genero', 'total_consultas', 'medicamentos_activos'))
    })


@login_required
def antecedentes_paciente(request, paciente_id):
    """Vista para gestionar antecedentes médicos"""
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    if request.method == 'POST':
        # Lógica para agregar antecedente
        tipo_antecedente = request.POST.get('tipo_antecedente')
        descripcion = request.POST.get('descripcion')
        severidad = request.POST.get('severidad')
        
        if tipo_antecedente and descripcion:
            from .models import AntecedenteMedico
            AntecedenteMedico.objects.create(
                paciente=paciente,
                tipo_antecedente=tipo_antecedente,
                descripcion=descripcion,
                severidad=severidad,
                creado_por=request.user
            )
            messages.success(request, '✅ Antecedente médico agregado exitosamente.')
            return redirect('antecedentes_paciente', paciente_id=paciente_id)
    
    antecedentes = paciente.antecedentes.all().order_by('-fecha_creacion')
    
    context = {
        'paciente': paciente,
        'antecedentes': antecedentes,
    }
    
    return render(request, 'pacientes/antecedentes.html', context)


@login_required
def medicamentos_paciente(request, paciente_id):
    """Vista para gestionar medicamentos del paciente"""
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    if request.method == 'POST':
        # Lógica para agregar medicamento
        nombre_medicamento = request.POST.get('nombre_medicamento')
        dosis = request.POST.get('dosis')
        frecuencia = request.POST.get('frecuencia')
        
        if nombre_medicamento and dosis and frecuencia:
            from .models import Medicamento
            Medicamento.objects.create(
                paciente=paciente,
                nombre_medicamento=nombre_medicamento,
                dosis=dosis,
                frecuencia=frecuencia,
                prescrito_por=request.user
            )
            messages.success(request, '✅ Medicamento agregado exitosamente.')
            return redirect('medicamentos_paciente', paciente_id=paciente_id)
    
    medicamentos_activos = paciente.obtener_medicamentos_activos()
    medicamentos_inactivos = paciente.medicamentos.filter(activo=False).order_by('-fecha_inicio')
    
    context = {
        'paciente': paciente,
        'medicamentos_activos': medicamentos_activos,
        'medicamentos_inactivos': medicamentos_inactivos,
    }
    
    return render(request, 'pacientes/medicamentos.html', context)


@login_required
def examenes_paciente(request, paciente_id):
    """Vista para gestionar exámenes médicos"""
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    if request.method == 'POST':
        # Lógica para solicitar examen
        tipo_examen = request.POST.get('tipo_examen')
        nombre_examen = request.POST.get('nombre_examen')
        descripcion = request.POST.get('descripcion')
        
        if tipo_examen and nombre_examen:
            from .models import ExamenMedico
            ExamenMedico.objects.create(
                paciente=paciente,
                tipo_examen=tipo_examen,
                nombre_examen=nombre_examen,
                descripcion=descripcion,
                solicitado_por=request.user
            )
            messages.success(request, '✅ Examen médico solicitado exitosamente.')
            return redirect('examenes_paciente', paciente_id=paciente_id)
    
    examenes = paciente.examenes.all().order_by('-fecha_solicitud')
    
    context = {
        'paciente': paciente,
        'examenes': examenes,
    }
    
    return render(request, 'pacientes/examenes.html', context)


@login_required
def evolucion_paciente(request, paciente_id):
    """Vista para gestionar evolución clínica"""
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    if request.method == 'POST':
        # Lógica para agregar evolución
        fecha_evolucion = request.POST.get('fecha_evolucion')
        tipo_evolucion = request.POST.get('tipo_evolucion')
        sintomas_actuales = request.POST.get('sintomas_actuales')
        diagnostico_actual = request.POST.get('diagnostico_actual')
        plan_tratamiento = request.POST.get('plan_tratamiento')
        
        if fecha_evolucion and tipo_evolucion and sintomas_actuales and diagnostico_actual:
            from .models import EvolucionClinica
            EvolucionClinica.objects.create(
                paciente=paciente,
                fecha_evolucion=fecha_evolucion,
                tipo_evolucion=tipo_evolucion,
                sintomas_actuales=sintomas_actuales,
                diagnostico_actual=diagnostico_actual,
                plan_tratamiento=plan_tratamiento,
                registrado_por=request.user
            )
            messages.success(request, '✅ Evolución clínica registrada exitosamente.')
            return redirect('evolucion_paciente', paciente_id=paciente_id)
    
    evoluciones = paciente.evoluciones.all().order_by('-fecha_evolucion')
    
    context = {
        'paciente': paciente,
        'evoluciones': evoluciones,
    }
    
    return render(request, 'pacientes/evolucion.html', context)


@login_required
def resumen_historial(request, paciente_id):
    """Vista para mostrar resumen del historial médico"""
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    # Obtener resumen completo
    historial = paciente.obtener_historial_completo()
    
    # Estadísticas adicionales
    estadisticas = {
        'total_consultas': paciente.consultas.count(),
        'consultas_ultimo_mes': paciente.consultas.filter(
            fecha__date__gte=timezone.now().date() - timedelta(days=30)
        ).count(),
        'medicamentos_activos': paciente.medicamentos.filter(activo=True).count(),
        'examenes_pendientes': paciente.examenes.filter(estado='solicitado').count(),
        'antecedentes_importantes': paciente.antecedentes.filter(
            tipo_antecedente__in=['personal', 'quirurgico', 'alergico']
        ).count(),
    }
    
    context = {
        'paciente': paciente,
        'historial': historial,
        'estadisticas': estadisticas,
    }
    
    return render(request, 'pacientes/resumen_historial.html', context)


@login_required
def pacientes_recientes(request):
    """Vista para mostrar pacientes con actividad reciente"""
    # Obtener pacientes con consultas en los últimos 30 días
    fecha_limite = timezone.now().date() - timedelta(days=30)
    
    pacientes_recientes = Paciente.objects.filter(
        consultas__fecha__date__gte=fecha_limite
    ).distinct().annotate(
        ultima_consulta=Max('consultas__fecha'),
        total_consultas=Count('consultas'),
        consultas_recientes=Count('consultas', filter=Q(consultas__fecha__date__gte=fecha_limite))
    ).order_by('-ultima_consulta')[:20]
    
    # Obtener pacientes con exámenes recientes
    pacientes_con_examenes = Paciente.objects.filter(
        examenes__fecha_solicitud__gte=fecha_limite
    ).distinct().annotate(
        ultimo_examen=Max('examenes__fecha_solicitud'),
        total_examenes=Count('examenes'),
        examenes_recientes=Count('examenes', filter=Q(examenes__fecha_solicitud__gte=fecha_limite))
    ).order_by('-ultimo_examen')[:10]
    
    # Obtener pacientes con medicamentos activos
    pacientes_con_medicamentos = Paciente.objects.filter(
        medicamentos__activo=True
    ).distinct().annotate(
        medicamentos_activos=Count('medicamentos', filter=Q(medicamentos__activo=True))
    ).order_by('-medicamentos_activos')[:10]
    
    context = {
        'pacientes_recientes': pacientes_recientes,
        'pacientes_con_examenes': pacientes_con_examenes,
        'pacientes_con_medicamentos': pacientes_con_medicamentos,
        'fecha_limite': fecha_limite,
    }
    
    return render(request, 'pacientes/pacientes_recientes.html', context)
