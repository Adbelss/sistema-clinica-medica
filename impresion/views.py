from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import DocumentoImpresion, PlantillaDocumento, ConfiguracionImpresion
from consultas.models import Consulta
from pacientes.models import Paciente

import qrcode
import io
import base64
from xhtml2pdf import pisa
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
import json


# ----------------------------
# Vista principal del módulo de impresión
# ----------------------------
@login_required
def dashboard_impresion(request):
    """Dashboard principal del módulo de impresión"""
    
    # Estadísticas
    total_documentos = DocumentoImpresion.objects.count()
    documentos_hoy = DocumentoImpresion.objects.filter(fecha_creacion__date=timezone.now().date()).count()
    documentos_pendientes = DocumentoImpresion.objects.filter(estado='borrador').count()
    
    # Documentos recientes
    documentos_recientes = DocumentoImpresion.objects.select_related('paciente', 'doctor').order_by('-fecha_creacion')[:5]
    
    # Documentos por tipo
    documentos_por_tipo = DocumentoImpresion.objects.values('tipo_documento').annotate(
        total=Count('id')
    ).order_by('-total')
    
    # Configuración
    config = ConfiguracionImpresion.obtener_configuracion()
    
    context = {
        'total_documentos': total_documentos,
        'documentos_hoy': documentos_hoy,
        'documentos_pendientes': documentos_pendientes,
        'documentos_recientes': documentos_recientes,
        'documentos_por_tipo': documentos_por_tipo,
        'config': config,
        'fecha_actual': timezone.now().strftime('%d/%m/%Y'),
    }
    return render(request, 'impresion/dashboard.html', context)


# ----------------------------
# Generar documento de consulta médica
# ----------------------------
@login_required
def generar_consulta_medica(request, consulta_id):
    """Genera un documento de consulta médica profesional"""
    consulta = get_object_or_404(Consulta, id=consulta_id)
    
    if request.method == 'POST':
        # Crear o actualizar documento
        documento, created = DocumentoImpresion.objects.get_or_create(
            consulta=consulta,
            tipo_documento='consulta',
            defaults={
                'paciente': consulta.paciente,
                'doctor': request.user,
                'titulo': f'Consulta Médica - {consulta.paciente.nombre_completo()}',
                'estado': 'finalizado'
            }
        )
        
        if not created:
            documento.fecha_modificacion = timezone.now()
            documento.save()
        
        # Generar contenido HTML
        contenido_html = generar_html_consulta(consulta, documento)
        documento.contenido_html = contenido_html
        documento.save()
        
        messages.success(request, f"✅ Documento de consulta generado exitosamente para {consulta.paciente.nombre_completo()}.")
        return redirect('impresion:previsualizar_documento', documento_id=documento.id)
    
    # Buscar documento existente
    documento_existente = DocumentoImpresion.objects.filter(
        consulta=consulta,
        tipo_documento='consulta'
    ).first()
    
    context = {
        'consulta': consulta,
        'paciente': consulta.paciente,
        'documento': documento_existente,
    }
    return render(request, 'impresion/generar_consulta.html', context)


# ----------------------------
# Generar receta médica
# ----------------------------
@login_required
def generar_receta_medica(request, consulta_id):
    """Genera una receta médica profesional"""
    consulta = get_object_or_404(Consulta, id=consulta_id)
    
    if request.method == 'POST':
        # Crear documento de receta
        documento = DocumentoImpresion.objects.create(
            consulta=consulta,
            paciente=consulta.paciente,
            doctor=request.user,
            tipo_documento='receta',
            titulo=f'Receta Médica - {consulta.paciente.nombre_completo()}',
            estado='finalizado'
        )
        
        # Generar contenido HTML
        contenido_html = generar_html_receta(consulta, documento)
        documento.contenido_html = contenido_html
        documento.save()
        
        messages.success(request, f"✅ Receta médica generada exitosamente para {consulta.paciente.nombre_completo()}.")
        return redirect('impresion:previsualizar_documento', documento_id=documento.id)
    
    # Buscar documento existente
    documento_existente = DocumentoImpresion.objects.filter(
        consulta=consulta,
        tipo_documento='receta'
    ).first()
    
    context = {
        'consulta': consulta,
        'paciente': consulta.paciente,
        'documento': documento_existente,
    }
    return render(request, 'impresion/generar_receta.html', context)


# ----------------------------
# Generar gestión de paciente
# ----------------------------
@login_required
def generar_gestion_paciente(request, paciente_id):
    """Genera un documento de gestión de paciente"""
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    if request.method == 'POST':
        # Crear documento de gestión
        documento = DocumentoImpresion.objects.create(
            paciente=paciente,
            doctor=request.user,
            tipo_documento='gestion',
            titulo=f'Gestión de Paciente - {paciente.nombre_completo()}',
            estado='finalizado'
        )
        
        # Generar contenido HTML
        contenido_html = generar_html_gestion(paciente, documento)
        documento.contenido_html = contenido_html
        documento.save()
        
        messages.success(request, f"✅ Documento de gestión generado exitosamente para {paciente.nombre_completo()}.")
        return redirect('impresion:previsualizar_documento', documento_id=documento.id)
    
    # Obtener historial de consultas
    consultas = Consulta.objects.filter(paciente=paciente).order_by('-fecha')
    
    context = {
        'paciente': paciente,
        'consultas': consultas,
    }
    return render(request, 'impresion/generar_gestion.html', context)


# ----------------------------
# Previsualizar documento
# ----------------------------
@login_required
def previsualizar_documento(request, documento_id):
    """Previsualiza un documento antes de imprimir"""
    documento = get_object_or_404(DocumentoImpresion, id=documento_id)
    
    context = {
        'documento': documento,
        'paciente': documento.paciente,
        'doctor': documento.doctor,
        'consulta': documento.consulta,
        'config': ConfiguracionImpresion.obtener_configuracion(),
    }
    return render(request, 'impresion/previsualizar.html', context)


# ----------------------------
# Imprimir documento
# ----------------------------
@login_required
def imprimir_documento(request, documento_id):
    """Imprime un documento en PDF profesional"""
    try:
        documento = get_object_or_404(DocumentoImpresion, id=documento_id)
        config = ConfiguracionImpresion.obtener_configuracion()
        
        # Generar PDF profesional
        response = HttpResponse(content_type='application/pdf')
        filename = f"{documento.tipo_documento}_{documento.numero_documento}_{documento.paciente.primer_apellido}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        # Renderizar HTML con plantilla simple
        template = get_template('impresion/plantillas/documento_simple.html')
        context = documento.obtener_contexto()
        context['config'] = config
        context['documento'] = documento
        html = template.render(context)
        
        # Convertir a PDF usando xhtml2pdf
        pdf = pisa.CreatePDF(
            src=html,
            dest=response,
            show_error_as_pdf=True
        )
        
        if not pdf.err:
            # Marcar como impreso
            documento.marcar_como_impreso()
            return response
        else:
            return HttpResponse(f'Error al generar PDF: {pdf.err}', status=500)
            
    except Exception as e:
        return HttpResponse(f'Error: {str(e)}', status=500)


@login_required
def descargar_documento_pdf(request, documento_id):
    """Descarga un documento en PDF con configuración profesional"""
    try:
        documento = get_object_or_404(DocumentoImpresion, id=documento_id)
        config = ConfiguracionImpresion.obtener_configuracion()
        
        # Generar PDF profesional para descarga
        response = HttpResponse(content_type='application/pdf')
        filename = f"{documento.tipo_documento.upper()}_{documento.numero_documento}_{documento.paciente.primer_apellido}_{documento.fecha_creacion.strftime('%Y%m%d')}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        # Renderizar HTML con plantilla simple
        template = get_template('impresion/plantillas/documento_simple.html')
        context = documento.obtener_contexto()
        context['config'] = config
        context['documento'] = documento
        context['modo_descarga'] = True
        html = template.render(context)
        
        # Convertir a PDF usando xhtml2pdf
        pdf = pisa.CreatePDF(
            src=html,
            dest=response,
            show_error_as_pdf=True
        )
        
        if not pdf.err:
            return response
        else:
            return HttpResponse(f'Error al generar PDF: {pdf.err}', status=500)
            
    except Exception as e:
        return HttpResponse(f'Error: {str(e)}', status=500)


# ----------------------------
# Listar documentos
# ----------------------------
@login_required
def listar_documentos(request):
    """Lista todos los documentos de impresión"""
    
    # Filtros
    tipo_query = request.GET.get('tipo', '').strip()
    estado_query = request.GET.get('estado', '').strip()
    paciente_query = request.GET.get('paciente', '').strip()
    fecha_query = request.GET.get('fecha', '').strip()
    
    documentos = DocumentoImpresion.objects.select_related('paciente', 'doctor', 'consulta').all().order_by('-fecha_creacion')
    
    # Aplicar filtros
    if tipo_query:
        documentos = documentos.filter(tipo_documento=tipo_query)
    if estado_query:
        documentos = documentos.filter(estado=estado_query)
    if paciente_query:
        documentos = documentos.filter(
            Q(paciente__primer_nombre__icontains=paciente_query) |
            Q(paciente__primer_apellido__icontains=paciente_query) |
            Q(paciente__documento_identificacion__icontains=paciente_query)
        )
    if fecha_query:
        documentos = documentos.filter(fecha_creacion__date=fecha_query)
    
    # Paginación
    paginator = Paginator(documentos, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'documentos': page_obj,
        'tipos_documento': DocumentoImpresion.TIPO_DOCUMENTO_CHOICES,
        'estados_documento': DocumentoImpresion.ESTADO_CHOICES,
        'tipo_query': tipo_query,
        'estado_query': estado_query,
        'paciente_query': paciente_query,
        'fecha_query': fecha_query,
    }
    return render(request, 'impresion/listar_documentos.html', context)


# ----------------------------
# Configuración de impresión
# ----------------------------
@login_required
def configuracion_impresion(request):
    """Configuración del sistema de impresión"""
    config = ConfiguracionImpresion.obtener_configuracion()
    
    if request.method == 'POST':
        # Actualizar configuración
        config.nombre_clinica = request.POST.get('nombre_clinica', config.nombre_clinica)
        config.direccion_clinica = request.POST.get('direccion_clinica', config.direccion_clinica)
        config.telefono_clinica = request.POST.get('telefono_clinica', config.telefono_clinica)
        config.email_clinica = request.POST.get('email_clinica', config.email_clinica)
        config.sitio_web_clinica = request.POST.get('sitio_web_clinica', config.sitio_web_clinica)
        config.pie_pagina_default = request.POST.get('pie_pagina_default', config.pie_pagina_default)
        
        # Configuración de impresión
        config.incluir_codigo_qr = request.POST.get('incluir_codigo_qr') == 'on'
        config.incluir_fecha_generacion = request.POST.get('incluir_fecha_generacion') == 'on'
        config.incluir_numero_pagina = request.POST.get('incluir_numero_pagina') == 'on'
        config.incluir_watermark = request.POST.get('incluir_watermark') == 'on'
        config.texto_watermark = request.POST.get('texto_watermark', config.texto_watermark)
        
        # Tamaño y orientación
        config.tamano_papel_default = request.POST.get('tamano_papel_default', config.tamano_papel_default)
        config.orientacion_default = request.POST.get('orientacion_default', config.orientacion_default)
        config.margenes_default = request.POST.get('margenes_default', config.margenes_default)
        
        # Manejar archivos
        if 'logo_clinica' in request.FILES:
            config.logo_clinica = request.FILES['logo_clinica']
        if 'sello_clinica' in request.FILES:
            config.sello_clinica = request.FILES['sello_clinica']
        
        config.save()
        messages.success(request, "✅ Configuración de impresión actualizada exitosamente.")
        return redirect('configuracion_impresion')
    
    context = {
        'config': config,
    }
    return render(request, 'impresion/configuracion.html', context)


# ----------------------------
# Funciones auxiliares para generar HTML
# ----------------------------
def generar_html_consulta(consulta, documento):
    """Genera el HTML para una consulta médica"""
    config = ConfiguracionImpresion.obtener_configuracion()
    
    # Generar código QR
    qr_data = {
        'tipo': 'consulta',
        'numero': documento.numero_documento,
        'paciente': consulta.paciente.documento_identificacion,
        'fecha': consulta.fecha.strftime('%Y-%m-%d'),
        'doctor': consulta.doctor.get_full_name()
    }
    qr_code = generar_codigo_qr(json.dumps(qr_data))
    
    # Calcular IMC
    imc = consulta.calcular_imc()
    categoria_imc = consulta.obtener_categoria_imc()
    
    html = f"""
    <div class="section">
        <h3>INFORMACIÓN DEL PACIENTE</h3>
        <table class="info-table">
            <tr>
                <td>Nombre completo</td>
                <td>{consulta.paciente.nombre_completo()}</td>
            </tr>
            <tr>
                <td>Documento</td>
                <td>{consulta.paciente.documento_identificacion}</td>
            </tr>
            <tr>
                <td>Fecha de nacimiento</td>
                <td>{consulta.paciente.fecha_nacimiento.strftime('%d/%m/%Y')}</td>
            </tr>
            <tr>
                <td>Edad</td>
                <td>{consulta.paciente.edad()} años</td>
            </tr>
            <tr>
                <td>Género</td>
                <td>{consulta.paciente.get_genero_display()}</td>
            </tr>
            <tr>
                <td>Teléfono</td>
                <td>{consulta.paciente.telefono}</td>
            </tr>
            <tr>
                <td>Dirección</td>
                <td>{consulta.paciente.direccion}</td>
            </tr>
        </table>
    </div>
    
    <div class="section">
        <h3>INFORMACIÓN DE LA CONSULTA</h3>
        <table class="info-table">
            <tr>
                <td>Fecha y hora</td>
                <td>{consulta.fecha.strftime('%d/%m/%Y %H:%M')}</td>
            </tr>
            <tr>
                <td>Tipo de consulta</td>
                <td>{consulta.get_tipo_consulta_display()}</td>
            </tr>
            <tr>
                <td>Estado</td>
                <td>{consulta.get_estado_display()}</td>
            </tr>
            <tr>
                <td>Médico tratante</td>
                <td>{consulta.doctor.get_full_name()}</td>
            </tr>
        </table>
    </div>
    
    <div class="section">
        <h3>SIGNOS VITALES</h3>
        <table class="info-table">
            <tr>
                <td>Presión Arterial</td>
                <td>{consulta.presion_arterial or 'No registrado'}</td>
            </tr>
            <tr>
                <td>Temperatura</td>
                <td>{f'{consulta.temperatura}°C' if consulta.temperatura else 'No registrado'}</td>
            </tr>
            <tr>
                <td>Peso</td>
                <td>{f'{consulta.peso} kg' if consulta.peso else 'No registrado'}</td>
            </tr>
            <tr>
                <td>Altura</td>
                <td>{f'{consulta.altura} m' if consulta.altura else 'No registrado'}</td>
            </tr>
            <tr>
                <td>Frecuencia Cardíaca</td>
                <td>{f'{consulta.frecuencia_cardiaca} lpm' if consulta.frecuencia_cardiaca else 'No registrado'}</td>
            </tr>
            <tr>
                <td>IMC</td>
                <td>{f'{imc} ({categoria_imc})' if imc else 'No calculado'}</td>
            </tr>
        </table>
    </div>
    
    <div class="section">
        <h3>MOTIVO DE CONSULTA</h3>
        <p>{consulta.motivo}</p>
    </div>
    
    {f'''
    <div class="section">
        <h3>SÍNTOMAS</h3>
        <p>{consulta.sintomas}</p>
    </div>
    ''' if consulta.sintomas else ''}
    
    <div class="section">
        <h3>DIAGNÓSTICO</h3>
        <p>{consulta.diagnostico}</p>
    </div>
    
    <div class="section">
        <h3>TRATAMIENTO</h3>
        <p>{consulta.tratamiento}</p>
    </div>
    
    {f'''
    <div class="section">
        <h3>MEDICAMENTOS RECETADOS</h3>
        <p>{consulta.medicamentos_recetados}</p>
    </div>
    ''' if consulta.medicamentos_recetados else ''}
    
    {f'''
    <div class="section">
        <h3>DOSIS Y FRECUENCIA</h3>
        <p>{consulta.dosis_medicamentos}</p>
    </div>
    ''' if consulta.dosis_medicamentos else ''}
    
    {f'''
    <div class="section">
        <h3>NOTAS ADICIONALES</h3>
        <p>{consulta.notas_adicionales}</p>
    </div>
    ''' if consulta.notas_adicionales else ''}
    
    {f'''
    <div class="section">
        <h3>PRÓXIMA CITA</h3>
        <p>{consulta.proxima_cita.strftime('%d/%m/%Y %H:%M')}</p>
    </div>
    ''' if consulta.proxima_cita else ''}
    """
    
    return html


def generar_html_receta(consulta, documento):
    """Genera el HTML para una receta médica"""
    config = ConfiguracionImpresion.obtener_configuracion()
    
    # Generar código QR
    qr_data = {
        'tipo': 'receta',
        'numero': documento.numero_documento,
        'paciente': consulta.paciente.documento_identificacion,
        'fecha': consulta.fecha.strftime('%Y-%m-%d'),
        'doctor': consulta.doctor.get_full_name()
    }
    qr_code = generar_codigo_qr(json.dumps(qr_data))
    
    html = f"""
    <div class="documento-medico receta">
        <!-- Encabezado -->
        <div class="encabezado">
            <div class="logo-clinica">
                {f'<img src="{config.logo_clinica.url}" alt="Logo Clínica" />' if config.logo_clinica else ''}
            </div>
            <div class="info-clinica">
                <h1>{config.nombre_clinica}</h1>
                <p>{config.direccion_clinica}</p>
                <p>Tel: {config.telefono_clinica} | Email: {config.email_clinica}</p>
            </div>
            <div class="codigo-qr">
                <img src="data:image/png;base64,{qr_code}" alt="Código QR" />
            </div>
        </div>
        
        <!-- Título del documento -->
        <div class="titulo-documento">
            <h2>RECETA MÉDICA</h2>
            <p class="numero-documento">N° {documento.numero_documento}</p>
        </div>
        
        <!-- Información del paciente -->
        <div class="seccion">
            <h3>DATOS DEL PACIENTE</h3>
            <table class="tabla-info">
                <tr>
                    <td><strong>Nombre:</strong></td>
                    <td>{consulta.paciente.nombre_completo()}</td>
                    <td><strong>Documento:</strong></td>
                    <td>{consulta.paciente.documento_identificacion}</td>
                </tr>
                <tr>
                    <td><strong>Edad:</strong></td>
                    <td>{consulta.paciente.edad()} años</td>
                    <td><strong>Fecha:</strong></td>
                    <td>{consulta.fecha.strftime('%d/%m/%Y')}</td>
                </tr>
            </table>
        </div>
        
        <!-- Diagnóstico -->
        <div class="seccion">
            <h3>DIAGNÓSTICO</h3>
            <div class="contenido-texto">
                {consulta.diagnostico}
            </div>
        </div>
        
        <!-- Medicamentos -->
        <div class="seccion">
            <h3>MEDICAMENTOS</h3>
            <div class="contenido-texto">
                {consulta.medicamentos_recetados or 'No se prescribieron medicamentos'}
            </div>
        </div>
        
        <!-- Dosis -->
        <div class="seccion">
            <h3>DOSIS Y FRECUENCIA</h3>
            <div class="contenido-texto">
                {consulta.dosis_medicamentos or 'No especificado'}
            </div>
        </div>
        
        <!-- Instrucciones especiales -->
        <div class="seccion">
            <h3>INSTRUCCIONES ESPECIALES</h3>
            <div class="contenido-texto">
                {consulta.notas_adicionales or 'Sin instrucciones especiales'}
            </div>
        </div>
        
        <!-- Pie de página -->
        <div class="pie-pagina">
            <div class="firma">
                <div class="linea-firma"></div>
                <p><strong>Dr. {consulta.doctor.get_full_name()}</strong></p>
                <p>Médico Tratante</p>
                {f'<p>Registro Profesional: {consulta.doctor.numero_registro or "N/A"}</p>' if hasattr(consulta.doctor, 'numero_registro') else ''}
            </div>
            <div class="sello">
                {f'<img src="{config.sello_clinica.url}" alt="Sello Clínica" />' if config.sello_clinica else ''}
            </div>
        </div>
        
        <!-- Información del sistema -->
        <div class="info-sistema">
            <p>Receta generada el {timezone.now().strftime('%d/%m/%Y %H:%M')} por el sistema médico</p>
            <p>{config.pie_pagina_default}</p>
        </div>
    </div>
    """
    
    return html


def generar_html_gestion(paciente, documento):
    """Genera el HTML para gestión de paciente"""
    config = ConfiguracionImpresion.obtener_configuracion()
    
    # Generar código QR
    qr_data = {
        'tipo': 'gestion',
        'numero': documento.numero_documento,
        'paciente': paciente.documento_identificacion,
        'fecha': timezone.now().strftime('%Y-%m-%d')
    }
    qr_code = generar_codigo_qr(json.dumps(qr_data))
    
    # Obtener historial de consultas
    consultas = Consulta.objects.filter(paciente=paciente).order_by('-fecha')
    
    html = f"""
    <div class="documento-medico gestion">
        <!-- Encabezado -->
        <div class="encabezado">
            <div class="logo-clinica">
                {f'<img src="{config.logo_clinica.url}" alt="Logo Clínica" />' if config.logo_clinica else ''}
            </div>
            <div class="info-clinica">
                <h1>{config.nombre_clinica}</h1>
                <p>{config.direccion_clinica}</p>
                <p>Tel: {config.telefono_clinica} | Email: {config.email_clinica}</p>
            </div>
            <div class="codigo-qr">
                <img src="data:image/png;base64,{qr_code}" alt="Código QR" />
            </div>
        </div>
        
        <!-- Título del documento -->
        <div class="titulo-documento">
            <h2>GESTIÓN DE PACIENTE</h2>
            <p class="numero-documento">N° {documento.numero_documento}</p>
        </div>
        
        <!-- Información del paciente -->
        <div class="seccion">
            <h3>INFORMACIÓN DEL PACIENTE</h3>
            <table class="tabla-info">
                <tr>
                    <td><strong>Nombre completo:</strong></td>
                    <td>{paciente.nombre_completo()}</td>
                    <td><strong>Documento:</strong></td>
                    <td>{paciente.documento_identificacion}</td>
                </tr>
                <tr>
                    <td><strong>Fecha de nacimiento:</strong></td>
                    <td>{paciente.fecha_nacimiento.strftime('%d/%m/%Y')}</td>
                    <td><strong>Edad:</strong></td>
                    <td>{paciente.edad()} años</td>
                </tr>
                <tr>
                    <td><strong>Género:</strong></td>
                    <td>{paciente.get_genero_display()}</td>
                    <td><strong>Teléfono:</strong></td>
                    <td>{paciente.telefono}</td>
                </tr>
                <tr>
                    <td><strong>Email:</strong></td>
                    <td>{paciente.email or 'No registrado'}</td>
                    <td><strong>Estado:</strong></td>
                    <td>{paciente.get_estado_display()}</td>
                </tr>
                <tr>
                    <td><strong>Dirección:</strong></td>
                    <td colspan="3">{paciente.direccion}</td>
                </tr>
            </table>
        </div>
        
        <!-- Historial de consultas -->
        <div class="seccion">
            <h3>HISTORIAL DE CONSULTAS</h3>
            <table class="tabla-consultas">
                <tr>
                    <th>Fecha</th>
                    <th>Tipo</th>
                    <th>Diagnóstico</th>
                    <th>Médico</th>
                </tr>
                {''.join([f'''
                <tr>
                    <td>{consulta.fecha.strftime('%d/%m/%Y')}</td>
                    <td>{consulta.get_tipo_consulta_display()}</td>
                    <td>{consulta.diagnostico[:50]}{'...' if len(consulta.diagnostico) > 50 else ''}</td>
                    <td>{consulta.doctor.get_full_name()}</td>
                </tr>
                ''' for consulta in consultas[:10]])}
            </table>
        </div>
        
        <!-- Estadísticas -->
        <div class="seccion">
            <h3>ESTADÍSTICAS</h3>
            <table class="tabla-info">
                <tr>
                    <td><strong>Total de consultas:</strong></td>
                    <td>{consultas.count()}</td>
                    <td><strong>Última consulta:</strong></td>
                    <td>{consultas.first().fecha.strftime('%d/%m/%Y') if consultas.exists() else 'N/A'}</td>
                </tr>
                <tr>
                    <td><strong>Consultas de emergencia:</strong></td>
                    <td>{consultas.filter(tipo_consulta='Emergencia').count()}</td>
                    <td><strong>Consultas de control:</strong></td>
                    <td>{consultas.filter(tipo_consulta='Control').count()}</td>
                </tr>
            </table>
        </div>
        
        <!-- Pie de página -->
        <div class="pie-pagina">
            <div class="firma">
                <div class="linea-firma"></div>
                <p><strong>Dr. {documento.doctor.get_full_name()}</strong></p>
                <p>Médico Responsable</p>
            </div>
            <div class="sello">
                {f'<img src="{config.sello_clinica.url}" alt="Sello Clínica" />' if config.sello_clinica else ''}
            </div>
        </div>
        
        <!-- Información del sistema -->
        <div class="info-sistema">
            <p>Documento generado el {timezone.now().strftime('%d/%m/%Y %H:%M')} por el sistema médico</p>
            <p>{config.pie_pagina_default}</p>
        </div>
    </div>
    """
    
    return html


def generar_codigo_qr(data):
    """Genera un código QR y lo convierte a base64"""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convertir a base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return img_str
