# 🏥 HealthLife

**HealthLife** es un sistema de gestión clínica desarrollado con **Python 3.12**, **Django 5** y **SQLite**, que permite registrar pacientes, consultas, usuarios con roles personalizados (Admin, Doctor, Asistente), respaldar/restaurar la base de datos, y visualizar todo desde una interfaz moderna con Bootstrap.

---

## 🔗 Repositorio oficial

📁 [https://github.com/Adbelss/healt_life.git](https://github.com/Adbelss/healt_life.git)

---

## 🚀 Guía de instalación

Sigue estos pasos desde **cero** para levantar el sistema HealthLife en otra máquina.

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/Adbelss/healt_life.git
cd healt_life/sistem
```

---

### 2️⃣ Crear entorno virtual

> Recomendado para evitar conflictos con otras versiones de Python o paquetes.

```bash
python -m venv venv
venv\Scripts\activate      # Windows
# o
source venv/bin/activate   # Linux/macOS
```

---

### 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Aplicar migraciones (solo si NO hay base de datos)

```bash
python manage.py makemigrations
python manage.py migrate
```

Si ya existe el archivo `db.sqlite3`, puedes omitir este paso. Si no existe, debes crear las tablas con el comando anterior.

---

### 5️⃣ Crear superusuario

```bash
python manage.py createsuperuser
```

Sigue las instrucciones en pantalla para ingresar usuario, correo y contraseña.

---

### 6️⃣ Ejecutar el servidor

```bash
python manage.py runserver
```

Luego abre tu navegador en:

📍 http://127.0.0.1:8000/

---

## 🔐 Roles y autenticación

El sistema distingue tres tipos de usuarios:

- 🛠 **Administrador:** Accede a toda la configuración, gestión de usuarios, respaldo de base de datos.
- 🩺 **Doctor:** Accede a las consultas médicas, pacientes asignados.
- 💼 **Asistente:** Apoya en el registro y edición de pacientes.

📧 **Autenticación:** Se realiza con correo electrónico y contraseña.

---

## 💾 Respaldo y restauración

Los administradores pueden realizar:

- ✅ **Respaldo automático** de la base de datos (genera archivo `.sqlite3`)
- 🔄 **Restauración manual** desde la interfaz web, subiendo un archivo `.sqlite3`

---

## 🌐 Despliegue en hosting (futuro)

Este proyecto está en fase de desarrollo local, pero se planea subirlo a un hosting con:

- Servidor web (Apache o Nginx)
- Base de datos SQLite o MySQL
- Configuración de entorno (`.env`)
- Certificado HTTPS

---

## ✅ Funcionalidades del sistema

- Registro, edición y eliminación de pacientes
- Gestión de consultas médicas por paciente
- Filtros y buscador por nombre, fecha o médico
- Formularios con validaciones
- Generación de reportes en PDF
- Dashboard con estadísticas clave
- Copia de seguridad y restauración de base de datos
- Gestión de usuarios con roles y permisos

---

## 🧑‍💻 ¿Quieres contribuir?

Si deseas mejorar el sistema:

1. Haz un **fork** del repositorio.
2. Crea una rama con tu funcionalidad:
   ```bash
   git checkout -b mi-nueva-funcionalidad
   ```
3. Sube tus cambios:
   ```bash
   git commit -m "Agrega nueva funcionalidad"
   git push origin mi-nueva-funcionalidad
   ```
4. Crea un **pull request** para revisión.

---

## 💬 Contacto

Para dudas, sugerencias o colaboración:

📧 **Adbel Eraldo Aguilar Avila**  
🔗 GitHub: [Adbelss](https://github.com/Adbelss)

---

## 📄 Licencia

Este proyecto es de uso educativo y libre para fines académicos.

---
