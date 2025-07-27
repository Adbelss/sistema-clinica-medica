# 🔧 Configuración Completa de WhatsApp Business API

## 📋 **PASOS PARA ACTIVAR WHATSAPP REAL**

### **Paso 1: Crear Cuenta en Meta for Developers**

1. **Ve a:** [Meta for Developers](https://developers.facebook.com/)
2. **Crea una cuenta** o inicia sesión
3. **Crea una nueva aplicación:**
   - Haz clic en "Crear App"
   - Selecciona "Business" como tipo
   - Completa la información básica

### **Paso 2: Configurar WhatsApp Business API**

1. **En tu aplicación, ve a "Add Product"**
2. **Busca y agrega "WhatsApp"**
3. **Configura tu número de teléfono:**
   - Ve a "WhatsApp" → "Getting Started"
   - Agrega tu número de teléfono
   - Verifica con el código que recibirás por SMS

### **Paso 3: Obtener Credenciales**

1. **Phone Number ID:**
   - Ve a "WhatsApp" → "Getting Started"
   - Copia el "Phone number ID"

2. **Access Token:**
   - Ve a "System Users" → "Access Tokens"
   - Genera un nuevo token
   - Cópialo (es muy importante, no lo pierdas)

3. **App ID:**
   - En la página principal de tu app
   - Copia el "App ID"

4. **Business Account ID:**
   - Ve a "Business Settings" → "Business Info"
   - Copia el "Business Account ID"

### **Paso 4: Crear Plantillas de Mensaje**

1. **Ve a "WhatsApp" → "Message Templates"**
2. **Crea estas plantillas:**

#### **Plantilla 1: Receta Médica**
```
Nombre: receta_medica
Categoría: Healthcare
Idioma: Español
Contenido:
Hola {{1}}, 

Tu receta médica está lista:

🏥 Clínica: HealthLife
👨‍⚕️ Doctor: {{2}}
📅 Fecha: {{3}}
💊 Medicamentos: {{4}}

Para más información, contacta a tu médico.

Saludos,
HealthLife
```

#### **Plantilla 2: Resumen de Consulta**
```
Nombre: resumen_consulta
Categoría: Healthcare
Idioma: Español
Contenido:
Hola {{1}},

Resumen de tu consulta médica:

🏥 Clínica: HealthLife
👨‍⚕️ Doctor: {{2}}
📅 Fecha: {{3}}
🔍 Diagnóstico: {{4}}
💊 Tratamiento: {{5}}

Próxima cita: {{6}}

Saludos,
HealthLife
```

### **Paso 5: Configurar Variables de Entorno**

**Crea un archivo `.env` en la raíz del proyecto:**

```env
# Django Settings
SECRET_KEY=tu-secret-key-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# WhatsApp Business API Configuration
WHATSAPP_API_TOKEN=tu_token_aqui
WHATSAPP_PHONE_NUMBER_ID=tu_phone_number_id_aqui
WHATSAPP_BUSINESS_ACCOUNT_ID=tu_business_account_id_aqui
WHATSAPP_APP_ID=tu_app_id_aqui
WHATSAPP_VERIFY_TOKEN=tu_verify_token_aqui

# Configuración del sistema
WHATSAPP_ENABLED=True
WHATSAPP_DEMO_MODE=False

# Database
DATABASE_URL=sqlite:///db.sqlite3
```

### **Paso 6: Instalar Dependencias**

```bash
pip install python-decouple requests
```

### **Paso 7: Reiniciar Servidor**

```bash
python manage.py runserver
```

---

## 🚀 **OPCIONES ALTERNATIVAS (Más Fáciles)**

### **Opción A: Twilio WhatsApp (Recomendada para Pruebas)**

1. **Crea cuenta en [Twilio](https://www.twilio.com/)**
2. **Activa WhatsApp Sandbox**
3. **Usa estas credenciales:**

```env
# Twilio Configuration
TWILIO_ACCOUNT_SID=tu_account_sid
TWILIO_AUTH_TOKEN=tu_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

### **Opción B: MessageBird**

1. **Crea cuenta en [MessageBird](https://messagebird.com/)**
2. **Configura WhatsApp Business**
3. **Usa las credenciales de MessageBird**

---

## 🧪 **PROBAR LA CONFIGURACIÓN**

### **1. Verificar Credenciales**

Ve a: `http://127.0.0.1:8000/consultas/whatsapp/prueba-demo/`

### **2. Crear un Paciente con WhatsApp Habilitado**

1. Ve a "Pacientes" → "Nuevo Paciente"
2. Marca "Notificar por WhatsApp"
3. Agrega un número de teléfono válido

### **3. Enviar Mensaje de Prueba**

1. Ve a una consulta
2. Haz clic en "Enviar Receta" o "Enviar Resumen"
3. Confirma el envío

---

## ⚠️ **NOTAS IMPORTANTES**

### **Costos**
- **WhatsApp Business API:** ~$0.005 por mensaje
- **Twilio:** ~$0.005 por mensaje
- **MessageBird:** ~$0.005 por mensaje

### **Límites**
- **Mensajes por día:** 1000 (gratis)
- **Horarios:** 9 AM - 6 PM (recomendado)
- **Plantillas:** Deben ser pre-aprobadas

### **Seguridad**
- **Nunca compartas tu API token**
- **Usa HTTPS en producción**
- **Valida números de teléfono**

---

## 🔧 **SOLUCIÓN DE PROBLEMAS**

### **Error: "WhatsApp service is not enabled"**
- Verifica que `WHATSAPP_ENABLED=True`
- Revisa las credenciales en `.env`

### **Error: "Invalid phone number"**
- Asegúrate de incluir código de país
- Formato: 50212345678 (Guatemala)

### **Error: "Template not found"**
- Crea las plantillas en WhatsApp Business Manager
- Verifica que los nombres coincidan

### **Error: "Rate limit exceeded"**
- Espera antes de enviar más mensajes
- Revisa los límites de tu cuenta

---

## 📞 **SOPORTE**

Si necesitas ayuda:
1. Revisa los logs del servidor
2. Consulta la [documentación oficial](https://developers.facebook.com/docs/whatsapp)
3. Verifica que todas las credenciales sean correctas

---

## ✅ **LISTA DE VERIFICACIÓN**

- [ ] Cuenta en Meta for Developers creada
- [ ] Aplicación de WhatsApp configurada
- [ ] Número de teléfono verificado
- [ ] Credenciales obtenidas
- [ ] Plantillas creadas y aprobadas
- [ ] Archivo `.env` configurado
- [ ] Servidor reiniciado
- [ ] Paciente con WhatsApp habilitado
- [ ] Mensaje de prueba enviado exitosamente 