# 🏥 HealthLife – Sistema de Gestión para Clínica Médica

Este proyecto es un sistema web desarrollado con **Python y Django** para gestionar pacientes, consultas, agenda médica y control administrativo en clínicas pequeñas o medianas.

---

## ⚙️ Tecnologías utilizadas

- Python 3.12
- Django 5.2
- SQLite (modo desarrollo)
- Bootstrap (más adelante para frontend)
- Git y GitHub para control de versiones

---

## 📁 Estructura general del proyecto

```bash
sistem/
├── manage.py
├── sistem/
│   └── settings.py
│   └── urls.py
├── usuarios/
│   └── models.py
├── templates/
│   ├── base.html
│   └── registration/
│       └── login.html
├── db.sqlite3
├── .gitignore
└── README.md
```

---

## 🚀 ¿Cómo ejecutar este proyecto?

1. **Clona el repositorio:**

```bash
git clone https://github.com/TU_USUARIO/healthlife.git
cd healthlife
```

2. **Crea el entorno virtual:**

```bash
python -m venv env
env\Scripts\activate
```

3. **Instala dependencias:**

```bash
pip install -r requirements.txt
```

> Si no tienes `requirements.txt`, puedes generarlo con:

```bash
pip freeze > requirements.txt
```

4. **Ejecuta migraciones y crea superusuario:**

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

5. **Inicia el servidor:**

```bash
python manage.py runserver
```

Abre [http://127.0.0.1:8000/login/](http://127.0.0.1:8000/login/) para comenzar.

---

## 🔐 Usuario por defecto

Puedes crear uno con:

```bash
python manage.py createsuperuser
```

---

## ✅ Avance actual

- [x] Entorno virtual configurado
- [x] Proyecto Django creado
- [x] Base de datos SQLite funcionando
- [x] Modelo de usuario personalizado con roles
- [x] Login/logout visual básico
- [x] Panel de administración funcional

---

## 🧠 En desarrollo

- Dashboard por tipo de usuario (admin/doctor/recepcionista)
- CRUD de pacientes y consultas
- Reportes PDF
- Estadísticas gráficas
- Seguridad y auditoría
- Backup automático
- Despliegue con HTTPS

---

## 🤝 Contribuciones

Este proyecto es parte de una **tesis universitaria**. Si deseas colaborar, contacta a Adbel Avila

---

## 📄 Licencia

Este sistema es de uso académico. No está autorizado su uso comercial sin permiso del autor.
