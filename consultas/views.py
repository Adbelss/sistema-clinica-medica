from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.auth import get_user_model

from .forms import ConsultaForm
from .models import Consulta

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
            consulta.save()
            return redirect('dashboard')
    else:
        form = ConsultaForm()
    return render(request, 'consultas/registrar_consulta.html', {'form': form})


# ----------------------------
# Vista del Dashboard
# ----------------------------
@login_required
def dashboard(request):
    total_consultas = Consulta.objects.count()
    usuario = request.user.get_full_name() or request.user.username
    ultimas_consultas = Consulta.objects.order_by('-fecha')[:5]

    context = {
        'total_consultas': total_consultas,
        'usuario': usuario,
        'ultimas_consultas': ultimas_consultas,
    }
    return render(request, 'consultas/dashboard.html', context)


# ----------------------------
# Vista para listar todas las consultas
# ----------------------------
@login_required
def listar_consultas(request):
    paciente_query = request.GET.get('paciente', '').strip()
    fecha_query = request.GET.get('fecha', '').strip()
    doctor_query = request.GET.get('doctor', '').strip()

    consultas = Consulta.objects.all().order_by('-fecha')

    if paciente_query:
        consultas = consultas.filter(paciente_nombre__icontains=paciente_query)
    if fecha_query:
        consultas = consultas.filter(fecha__date=fecha_query)
    if doctor_query:
        consultas = consultas.filter(doctor__id=doctor_query)

    paginator = Paginator(consultas, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    User = get_user_model()
    doctores = User.objects.all()

    context = {
        'consultas': page_obj,
        'paciente_query': paciente_query,
        'fecha_query': fecha_query,
        'doctor_query': doctor_query,
        'doctores': doctores,
        'page_obj': page_obj,
    }
    return render(request, 'consultas/listar_consultas.html', context)


# ----------------------------
# Vista para editar una consulta
# ----------------------------
@login_required
def editar_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    if consulta.doctor != request.user:
        messages.error(request, "No tienes permiso para editar esta consulta.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = ConsultaForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Consulta actualizada correctamente.')
            return redirect('listar_consultas')
    else:
        form = ConsultaForm(instance=consulta)
    return render(request, 'consultas/editar_consulta.html', {'form': form})


# ----------------------------
# Vista para eliminar una consulta
# ----------------------------
@login_required
def eliminar_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    if consulta.doctor != request.user:
        messages.error(request, "No tienes permiso para eliminar esta consulta.")
        return redirect('dashboard')

    if request.method == 'POST':
        consulta.delete()
        messages.success(request, 'Consulta eliminada correctamente.')
        return redirect('listar_consultas')
    return render(request, 'consultas/eliminar_confirmar.html', {'consulta': consulta})


# ----------------------------
# Vista para ver detalles individuales de una consulta
# ----------------------------
@login_required
def detalle_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    if consulta.doctor != request.user:
        messages.error(request, "No tienes permiso para ver esta consulta.")
        return redirect('dashboard')

    return render(request, 'consultas/detalle_consulta.html', {'consulta': consulta})


# ----------------------------
# Exportar consultas a PDF
# ----------------------------
@login_required
def exportar_consultas_pdf(request):
    consultas = Consulta.objects.all().order_by('-fecha')
    template_path = 'consultas/pdf_consultas.html'
    context = {'consultas': consultas}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="consultas.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa.CreatePDF(html, dest=response)
    return response


# ----------------------------
# Exportar consultas a Excel
# ----------------------------
@login_required
def exportar_consultas_excel(request):
    consultas = Consulta.objects.all().order_by('-fecha')
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Consultas"

    # Encabezados
    ws.append(['#', 'Paciente', 'Motivo', 'Diagnóstico', 'Tratamiento', 'Fecha', 'Doctor'])

    for idx, c in enumerate(consultas, 1):
        ws.append([
            idx,
            c.paciente_nombre,
            c.motivo,
            c.diagnostico,
            c.tratamiento,
            c.fecha.strftime("%d/%m/%Y %H:%M"),
            c.doctor.get_full_name() or c.doctor.username
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=consultas.xlsx'
    wb.save(response)
    return response


# ----------------------------
# Manejador personalizado de error 403
# ----------------------------
def error_403(request, exception=None):
    return render(request, '403.html', status=403)
