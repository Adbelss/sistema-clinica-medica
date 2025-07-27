# 📱 Configuración de WhatsApp Business API

## 🎯 **Para recibir mensajes reales en tu WhatsApp**

### **Paso 1: Crear cuenta en Meta for Developers**
1. Ve a [Meta for Developers](https://developers.facebook.com/)
2. Crea una cuenta o inicia sesión
3. Crea una nueva aplicación
4. Selecciona "Business" como tipo de aplicación

### **Paso 2: Configurar WhatsApp Business API**
1. En tu aplicación, ve a "Add Product"
2. Busca y agrega "WhatsApp"
3. Configura tu número de teléfono de WhatsApp Business
4. Verifica tu número con el código que recibirás

### **Paso 3: Obtener Credenciales**
1. Ve a "WhatsApp" → "Getting Started"
2. Copia tu **Phone Number ID**
3. Ve a "System Users" → "Access Tokens"
4. Genera un token y cópialo

### **Paso 4: Configurar Variables de Entorno**
Crea o edita el archivo `.env` en la raíz del proyecto:

```env
# WhatsApp Business API Configuration
WHATSAPP_API_TOKEN=tu_token_aqui
WHATSAPP_PHONE_NUMBER_ID=tu_phone_number_id_aqui
WHATSAPP_BUSINESS_ACCOUNT_ID=tu_business_account_id_aqui
WHATSAPP_APP_ID=tu_app_id_aqui
WHATSAPP_VERIFY_TOKEN=tu_verify_token_aqui

# Configuración del sistema
WHATSAPP_ENABLED=True
WHATSAPP_DEMO_MODE=False
```

### **Paso 5: Crear Plantillas de Mensaje**
1. Ve a "WhatsApp" → "Message Templates"
2. Crea las siguientes plantillas:

#### **Plantilla 1: Receta Médica**
```
Nombre: receta_medica
Categoría: Healthcare
Idioma: Español
Contenido:
Hola {{1}}, 

Tu receta médica está lista:

🏥 Clínica: {{2}}
👨‍⚕️ Doctor: {{3}}
📅 Fecha: {{4}}
💊 Medicamentos: {{5}}

Para más información, contacta a tu médico.

Saludos,
{{6}}
```

#### **Plantilla 2: Resumen de Consulta**
```
Nombre: resumen_consulta
Categoría: Healthcare
Idioma: Español
Contenido:
Hola {{1}},

Resumen de tu consulta médica:

🏥 Clínica: {{2}}
👨‍⚕️ Doctor: {{3}}
📅 Fecha: {{4}}
🔍 Diagnóstico: {{5}}
💊 Tratamiento: {{6}}

Próxima cita: {{7}}

Saludos,
{{8}}
```

### **Paso 6: Activar el Sistema**
1. Reinicia el servidor Django
2. Ve a `/admin/` y verifica que las plantillas estén activas
3. Prueba enviando un mensaje desde el sistema

---

## 🔧 **Configuración Rápida (Alternativa)**

Si quieres una configuración más rápida, puedes usar servicios como:

### **Twilio WhatsApp**
1. Crea cuenta en [Twilio](https://www.twilio.com/)
2. Activa WhatsApp Sandbox
3. Usa las credenciales de Twilio

### **MessageBird**
1. Crea cuenta en [MessageBird](https://messagebird.com/)
2. Configura WhatsApp Business
3. Usa las credenciales de MessageBird

---

## 🧪 **Modo Demo (Actual)**

Actualmente el sistema está en modo demo:
- ✅ Simula envío de mensajes
- ✅ Guarda en base de datos
- ❌ No envía mensajes reales

Para desactivar el modo demo, cambia en `consultas/services.py`:

```python
def is_enabled(self):
    # Cambiar de True a verificar credenciales reales
    return bool(self.api_token and self.phone_number_id)
```

---

## 📞 **Soporte**

Si necesitas ayuda con la configuración:
1. Revisa la [documentación oficial de Meta](https://developers.facebook.com/docs/whatsapp)
2. Consulta los logs del servidor para errores
3. Verifica que las credenciales sean correctas

---

## ⚠️ **Notas Importantes**

- **Costo**: WhatsApp Business API tiene costos por mensaje
- **Límites**: Hay límites de envío diario
- **Plantillas**: Los mensajes deben usar plantillas pre-aprobadas
- **Horarios**: Respeta los horarios de envío permitidos
- **Consentimiento**: Asegúrate de tener consentimiento del paciente 