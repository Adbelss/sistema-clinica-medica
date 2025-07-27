import requests
import json
import logging
from datetime import datetime
from django.conf import settings
from django.utils import timezone
from decouple import config
from .models import NotificacionWhatsApp

logger = logging.getLogger(__name__)

class WhatsAppService:
    """Servicio para manejar la integración con WhatsApp Business API"""
    
    def __init__(self):
        self.api_token = config('WHATSAPP_API_TOKEN', default='')
        self.phone_number_id = config('WHATSAPP_PHONE_NUMBER_ID', default='')
        self.app_id = config('WHATSAPP_APP_ID', default='')
        self.business_account_id = config('WHATSAPP_BUSINESS_ACCOUNT_ID', default='')
        self.base_url = "https://graph.facebook.com/v18.0"
        self.enabled = config('WHATSAPP_ENABLED', default=False, cast=bool)
        
        # Plantillas pre-aprobadas
        self.templates = {
            'receta_medica': {
                'name': 'receta_medica',
                'language': 'es_ES',
                'components': [
                    {
                        'type': 'header',
                        'text': 'Receta Médica'
                    },
                    {
                        'type': 'body',
                        'text': 'Hola {{1}}, aquí tienes tu receta médica del Dr. {{2}} con fecha {{3}}.'
                    }
                ]
            },
            'resumen_consulta': {
                'name': 'resumen_consulta',
                'language': 'es_ES',
                'components': [
                    {
                        'type': 'header',
                        'text': 'Resumen de Consulta'
                    },
                    {
                        'type': 'body',
                        'text': 'Hola {{1}}, aquí tienes el resumen de tu consulta del {{2}} con el Dr. {{3}}.'
                    }
                ]
            },
            'recordatorio_cita': {
                'name': 'recordatorio_cita',
                'language': 'es_ES',
                'components': [
                    {
                        'type': 'header',
                        'text': 'Recordatorio de Cita'
                    },
                    {
                        'type': 'body',
                        'text': 'Hola {{1}}, tienes una cita programada para el {{2}} a las {{3}} con el Dr. {{4}}.'
                    }
                ]
            }
        }
    
    def is_enabled(self):
        """Verifica si el servicio está habilitado"""
        # Verificar que tengamos las credenciales necesarias
        return bool(self.api_token and self.phone_number_id and self.enabled)
    
    def _make_request(self, endpoint, method='GET', data=None, files=None):
        """Realiza una petición HTTP a la API de WhatsApp"""
        if not self.is_enabled():
            raise Exception("WhatsApp service is not enabled or configured. Please check your credentials in .env file")
        
        url = f"{self.base_url}/{endpoint}"
        headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                if files:
                    # Para archivos, no usar Content-Type JSON
                    headers.pop('Content-Type', None)
                    response = requests.post(url, headers=headers, data=data, files=files)
                else:
                    response = requests.post(url, headers=headers, json=data)
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"WhatsApp API error: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response status: {e.response.status_code}")
                logger.error(f"Response content: {e.response.text}")
            raise Exception(f"Error communicating with WhatsApp API: {str(e)}")
    
    def send_text_message(self, phone_number, message):
        """Envía un mensaje de texto simple"""
        endpoint = f"{self.phone_number_id}/messages"
        
        data = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "text",
            "text": {"body": message}
        }
        
        return self._make_request(endpoint, method='POST', data=data)
    
    def send_template_message(self, phone_number, template_name, parameters):
        """Envía un mensaje usando una plantilla pre-aprobada"""
        endpoint = f"{self.phone_number_id}/messages"
        
        data = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": "es_ES"
                },
                "components": []
            }
        }
        
        # Agregar parámetros si existen
        if parameters:
            data["template"]["components"].append({
                "type": "body",
                "parameters": parameters
            })
        
        return self._make_request(endpoint, method='POST', data=data)
    
    def send_document(self, phone_number, document_url, filename, caption=None):
        """Envía un documento (PDF, imagen, etc.)"""
        endpoint = f"{self.phone_number_id}/messages"
        
        data = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "document",
            "document": {
                "link": document_url,
                "filename": filename
            }
        }
        
        if caption:
            data["document"]["caption"] = caption
        
        return self._make_request(endpoint, method='POST', data=data)
    
    def send_image(self, phone_number, image_url, caption=None):
        """Envía una imagen"""
        endpoint = f"{self.phone_number_id}/messages"
        
        data = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "image",
            "image": {
                "link": image_url
            }
        }
        
        if caption:
            data["image"]["caption"] = caption
        
        return self._make_request(endpoint, method='POST', data=data)
    
    def get_message_status(self, message_id):
        """Obtiene el estado de un mensaje"""
        endpoint = f"{message_id}"
        return self._make_request(endpoint, method='GET')
    
    def format_phone_number(self, phone_number):
        """Formatea el número de teléfono para WhatsApp"""
        # Remover caracteres no numéricos
        cleaned = ''.join(filter(str.isdigit, str(phone_number)))
        
        # Agregar código de país si no está presente
        if not cleaned.startswith('502'):  # Código de Guatemala
            cleaned = '502' + cleaned
        
        return cleaned
    
    def create_notification_record(self, paciente, consulta, tipo, telefono, mensaje, 
                                 plantilla_usada=None, enviado_por=None):
        """Crea un registro de notificación en la base de datos"""
        return NotificacionWhatsApp.objects.create(
            paciente=paciente,
            consulta=consulta,
            tipo=tipo,
            telefono=telefono,
            mensaje=mensaje,
            plantilla_usada=plantilla_usada,
            enviado_por=enviado_por
        )


class WhatsAppNotificationService:
    """Servicio para manejar notificaciones específicas de WhatsApp"""
    
    def __init__(self):
        self.whatsapp_service = WhatsAppService()
    
    def send_prescription(self, consulta, enviado_por=None):
        """Envía una receta médica por WhatsApp"""
        # Verificar consentimiento del paciente
        if not consulta.paciente.notificar_whatsapp:
            raise Exception("El paciente no tiene habilitadas las notificaciones por WhatsApp")
        
        # Generar mensaje de receta
        mensaje = self._generate_prescription_message(consulta)
        
        # Crear registro de notificación
        notificacion = self.whatsapp_service.create_notification_record(
            paciente=consulta.paciente,
            consulta=consulta,
            tipo='receta',
            telefono=consulta.paciente.telefono,
            mensaje=mensaje,
            plantilla_usada='receta_medica',
            enviado_por=enviado_por
        )
        
        try:
            # Formatear número de teléfono
            phone_number = self.whatsapp_service.format_phone_number(consulta.paciente.telefono)
            
            # Enviar mensaje
            response = self.whatsapp_service.send_template_message(
                phone_number=phone_number,
                template_name='receta_medica',
                parameters=[
                    {"type": "text", "text": consulta.paciente.primer_nombre},
                    {"type": "text", "text": consulta.doctor.get_full_name()},
                    {"type": "text", "text": consulta.fecha.strftime('%d/%m/%Y')}
                ]
            )
            
            # Marcar como enviado
            message_id = response.get('messages', [{}])[0].get('id')
            notificacion.marcar_como_enviado(message_id)
            
            return notificacion
            
        except Exception as e:
            notificacion.marcar_error(str(e))
            raise e
    
    def send_consultation_summary(self, consulta, enviado_por=None):
        """Envía un resumen de consulta por WhatsApp"""
        # Verificar consentimiento del paciente
        if not consulta.paciente.notificar_whatsapp:
            raise Exception("El paciente no tiene habilitadas las notificaciones por WhatsApp")
        
        # Generar mensaje de resumen
        mensaje = self._generate_consultation_summary_message(consulta)
        
        # Crear registro de notificación
        notificacion = self.whatsapp_service.create_notification_record(
            paciente=consulta.paciente,
            consulta=consulta,
            tipo='consulta',
            telefono=consulta.paciente.telefono,
            mensaje=mensaje,
            plantilla_usada='resumen_consulta',
            enviado_por=enviado_por
        )
        
        try:
            # Formatear número de teléfono
            phone_number = self.whatsapp_service.format_phone_number(consulta.paciente.telefono)
            
            # Enviar mensaje
            response = self.whatsapp_service.send_template_message(
                phone_number=phone_number,
                template_name='resumen_consulta',
                parameters=[
                    {"type": "text", "text": consulta.paciente.primer_nombre},
                    {"type": "text", "text": consulta.fecha.strftime('%d/%m/%Y')},
                    {"type": "text", "text": consulta.doctor.get_full_name()}
                ]
            )
            
            # Marcar como enviado
            message_id = response.get('messages', [{}])[0].get('id')
            notificacion.marcar_como_enviado(message_id)
            
            return notificacion
            
        except Exception as e:
            notificacion.marcar_error(str(e))
            raise e
    
    def send_appointment_reminder(self, cita, enviado_por=None):
        """Envía un recordatorio de cita por WhatsApp"""
        if not cita.paciente.notificar_whatsapp:
            raise Exception("El paciente no tiene habilitadas las notificaciones por WhatsApp")
        
        # Generar mensaje de recordatorio
        mensaje = self._generate_appointment_reminder_message(cita)
        
        # Crear registro de notificación
        notificacion = self.whatsapp_service.create_notification_record(
            paciente=cita.paciente,
            consulta=None,
            tipo='recordatorio',
            telefono=cita.paciente.telefono,
            mensaje=mensaje,
            plantilla_usada='recordatorio_cita',
            enviado_por=enviado_por
        )
        
        try:
            # Formatear número de teléfono
            phone_number = self.whatsapp_service.format_phone_number(cita.paciente.telefono)
            
            # Enviar mensaje
            response = self.whatsapp_service.send_template_message(
                phone_number=phone_number,
                template_name='recordatorio_cita',
                parameters=[
                    {"type": "text", "text": cita.paciente.primer_nombre},
                    {"type": "text", "text": cita.fecha.strftime('%d/%m/%Y')},
                    {"type": "text", "text": cita.hora_inicio.strftime('%H:%M')},
                    {"type": "text", "text": cita.doctor.get_full_name()}
                ]
            )
            
            # Marcar como enviado
            message_id = response.get('messages', [{}])[0].get('id')
            notificacion.marcar_como_enviado(message_id)
            
            return notificacion
            
        except Exception as e:
            notificacion.marcar_error(str(e))
            raise e
    
    def _generate_prescription_message(self, consulta):
        """Genera el mensaje de receta médica"""
        return f"""
🏥 *RECETA MÉDICA*

👤 *Paciente:* {consulta.paciente.nombre_completo()}
👨‍⚕️ *Doctor:* {consulta.doctor.get_full_name()}
📅 *Fecha:* {consulta.fecha.strftime('%d/%m/%Y')}

💊 *Medicamentos Recetados:*
{consulta.medicamentos_recetados or 'No se recetaron medicamentos'}

📋 *Dosis y Frecuencia:*
{consulta.dosis_medicamentos or 'No especificada'}

💡 *Tratamiento:*
{consulta.tratamiento}

⚠️ *Importante:* 
- Tome los medicamentos según las indicaciones
- Complete el tratamiento completo
- Consulte si presenta efectos secundarios
- Guarde esta receta para futuras consultas

📞 *Para consultas:* Contacte a su médico
        """.strip()
    
    def _generate_consultation_summary_message(self, consulta):
        """Genera el mensaje de resumen de consulta"""
        return f"""
🏥 *RESUMEN DE CONSULTA*

👤 *Paciente:* {consulta.paciente.nombre_completo()}
👨‍⚕️ *Doctor:* {consulta.doctor.get_full_name()}
📅 *Fecha:* {consulta.fecha.strftime('%d/%m/%Y')}

🔍 *Motivo de Consulta:*
{consulta.motivo}

📋 *Diagnóstico:*
{consulta.diagnostico}

💊 *Tratamiento:*
{consulta.tratamiento}

📊 *Signos Vitales:*
{self._format_vital_signs(consulta)}

📅 *Próxima Cita:*
{consulta.proxima_cita.strftime('%d/%m/%Y %H:%M') if consulta.proxima_cita else 'No programada'}

💡 *Observaciones:*
{consulta.observaciones_cita or 'Ninguna'}
        """.strip()
    
    def _generate_appointment_reminder_message(self, cita):
        """Genera el mensaje de recordatorio de cita"""
        return f"""
🏥 *RECORDATORIO DE CITA*

👤 *Paciente:* {cita.paciente.nombre_completo()}
👨‍⚕️ *Doctor:* {cita.doctor.get_full_name()}
📅 *Fecha:* {cita.fecha.strftime('%d/%m/%Y')}
⏰ *Hora:* {cita.hora_inicio.strftime('%H:%M')}

📋 *Tipo de Cita:* {cita.get_tipo_cita_display()}
📝 *Motivo:* {cita.motivo or 'No especificado'}

⚠️ *Recordatorio:*
- Llegue 10 minutos antes de su cita
- Traiga su documento de identificación
- Si no puede asistir, cancele con anticipación

📞 *Para reprogramar:* Contacte a la clínica
        """.strip()
    
    def _format_vital_signs(self, consulta):
        """Formatea los signos vitales para el mensaje"""
        vital_signs = []
        
        if consulta.presion_arterial:
            vital_signs.append(f"• Presión Arterial: {consulta.presion_arterial}")
        if consulta.temperatura:
            vital_signs.append(f"• Temperatura: {consulta.temperatura}°C")
        if consulta.peso:
            vital_signs.append(f"• Peso: {consulta.peso} kg")
        if consulta.altura:
            vital_signs.append(f"• Altura: {consulta.altura} m")
        if consulta.frecuencia_cardiaca:
            vital_signs.append(f"• Frecuencia Cardíaca: {consulta.frecuencia_cardiaca} lpm")
        
        if vital_signs:
            return '\n'.join(vital_signs)
        else:
            return 'No registrados' 