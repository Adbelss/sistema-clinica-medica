# 🚀 Guía de Despliegue - Sistema de Clínica Médica

## Despliegue Gratuito en Railway

### 📋 Requisitos Previos
1. Cuenta en GitHub (gratuita)
2. Cuenta en Railway (gratuita)
3. Git instalado en tu computadora

### 🔧 Pasos para el Despliegue

#### 1. Preparar el Repositorio
```bash
# Asegúrate de estar en el directorio del proyecto
cd sistem

# Inicializar git si no está inicializado
git init

# Agregar todos los archivos
git add .

# Hacer commit inicial
git commit -m "Preparación para despliegue en Railway"

# Crear repositorio en GitHub y conectar
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git branch -M main
git push -u origin main
```

#### 2. Configurar Railway

1. **Ir a Railway.app**
   - Ve a https://railway.app
   - Inicia sesión con tu cuenta de GitHub

2. **Crear Nuevo Proyecto**
   - Haz clic en "New Project"
   - Selecciona "Deploy from GitHub repo"
   - Conecta tu repositorio de GitHub

3. **Configurar Variables de Entorno**
   En Railway, ve a la pestaña "Variables" y agrega:
   ```
   DEBUG=False
   SECRET_KEY=tu_clave_secreta_muy_larga_y_segura
   DATABASE_URL=postgresql://... (Railway lo genera automáticamente)
   ```

4. **Configurar Base de Datos**
   - En Railway, ve a "New Service" → "Database" → "PostgreSQL"
   - Railway generará automáticamente la DATABASE_URL

#### 3. Desplegar

1. **Railway detectará automáticamente que es un proyecto Django**
2. **El despliegue comenzará automáticamente**
3. **Espera unos minutos para que termine**

#### 4. Configurar Dominio

1. **En Railway, ve a la pestaña "Settings"**
2. **En "Domains", Railway te dará una URL como:**
   `https://tu-proyecto-production.up.railway.app`
3. **Puedes personalizar el dominio si quieres**

### 🔐 Crear Superusuario

Una vez desplegado, necesitas crear un superusuario:

1. **En Railway, ve a la pestaña "Deployments"**
2. **Haz clic en el último deployment**
3. **Ve a "Logs" y ejecuta:**
   ```bash
   python manage.py createsuperuser
   ```

### 📱 Acceder a tu Aplicación

Tu aplicación estará disponible en:
`https://tu-proyecto-production.up.railway.app`

### 🔄 Actualizaciones Futuras

Para actualizar tu aplicación:
```bash
git add .
git commit -m "Nueva actualización"
git push origin main
```

Railway detectará automáticamente los cambios y desplegará la nueva versión.

### 💰 Costos

- **Railway**: Gratis hasta 500 horas/mes
- **Base de datos PostgreSQL**: Incluida en el plan gratuito
- **Dominio personalizado**: Opcional (puedes usar el dominio de Railway gratis)

### 🛠️ Solución de Problemas

#### Error de migraciones:
Si hay errores de migración, en Railway ejecuta:
```bash
python manage.py migrate --run-syncdb
```

#### Error de archivos estáticos:
Si los archivos estáticos no se cargan:
```bash
python manage.py collectstatic --noinput
```

#### Error de base de datos:
Verifica que la DATABASE_URL esté correctamente configurada en las variables de entorno.

### 📞 Soporte

Si tienes problemas:
1. Revisa los logs en Railway
2. Verifica que todas las variables de entorno estén configuradas
3. Asegúrate de que el repositorio esté sincronizado con GitHub

¡Tu sistema de clínica médica estará funcionando en la web de forma gratuita! 🎉 