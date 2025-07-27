# Guía de Deployment - Sistema Clínico HealthLife

## Plataforma: Railway (Gratis)

### 1. Preparación del Proyecto

#### Configuración de Git
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git push -u origin main
```

### 2. Configuración en Railway

#### Crear Proyecto
1. Ve a [railway.app](https://railway.app)
2. Inicia sesión con GitHub
3. Click en "New Project"
4. Selecciona "Deploy from GitHub repo"
5. Selecciona tu repositorio

#### Agregar Base de Datos MySQL
1. En tu proyecto de Railway, click en "New"
2. Selecciona "Database" → "MySQL"
3. Railway te dará las credenciales automáticamente

#### Configurar Variables de Entorno
En Railway, ve a tu proyecto → Variables y agrega:

```
SECRET_KEY=tu_clave_secreta_muy_larga_y_compleja
DEBUG=False
RAILWAY_ENVIRONMENT=True
DATABASE_URL=mysql://usuario:contraseña@host:puerto/nombre_db
```

**Nota:** Railway te proporciona la DATABASE_URL automáticamente cuando agregas MySQL.

### 3. Configuración de la Aplicación

#### Archivos Necesarios
- `requirements.txt` ✅ (ya configurado)
- `Procfile` ✅ (ya configurado)
- `runtime.txt` ✅ (ya configurado)
- `railway.json` ✅ (ya configurado)

### 4. Deployment

#### Proceso Automático
1. Railway detectará automáticamente que es un proyecto Django
2. Instalará las dependencias de `requirements.txt`
3. Ejecutará los comandos del `Procfile`
4. Desplegará la aplicación

#### Verificar Deployment
1. Ve a la pestaña "Deployments" en Railway
2. Espera a que termine el build
3. Click en el dominio generado para acceder

### 5. Configuración Post-Deployment

#### Crear Superusuario
```bash
# En Railway CLI o terminal local conectado a Railway
railway login
railway link
railway run python manage.py createsuperuser
```

#### Ejecutar Migraciones
```bash
railway run python manage.py migrate
```

### 6. Configuración de Archivos Estáticos

El proyecto ya está configurado con:
- WhiteNoise para servir archivos estáticos
- Configuración automática de collectstatic
- Middleware optimizado para Railway

### 7. Troubleshooting

#### Problemas Comunes
1. **Error de módulos**: Verificar `requirements.txt`
2. **Error de base de datos**: Verificar `DATABASE_URL`
3. **Archivos estáticos no cargan**: Verificar WhiteNoise
4. **Error CSRF**: Verificar configuración de cookies

#### Logs
- Ve a Railway → Deployments → Click en deployment → Logs
- Revisa los logs para identificar errores

### 8. URLs Importantes

- **Aplicación**: https://tu-app.railway.app
- **Admin**: https://tu-app.railway.app/admin
- **Dashboard**: https://tu-app.railway.app/consultas/dashboard/

### 9. Mantenimiento

#### Actualizaciones
1. Haz cambios en tu código local
2. `git add . && git commit -m "descripción"`
3. `git push origin main`
4. Railway se actualizará automáticamente

#### Backups
- Railway hace backups automáticos de MySQL
- También puedes usar el módulo de respaldo del sistema

### 10. Costos

- **Railway**: Gratis hasta 500 horas/mes
- **MySQL**: Incluido en el plan gratuito
- **Dominio**: Incluido (.railway.app)

---

**Nota**: Esta configuración está optimizada para Railway y MySQL, proporcionando una solución robusta y gratuita para tu sistema clínico. 