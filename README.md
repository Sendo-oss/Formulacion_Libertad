# Sistema Web de Formulacion Magistral

Aplicacion web desarrollada con Django para la gestion academica e institucional de formulaciones magistrales, materias primas, documentacion tecnica, alertas y calculos de apoyo en laboratorio.

## Modulos principales

- Usuarios y control por roles
- Inventario de materias primas
- Formulaciones magistrales
- Alertas operativas
- Documentacion tecnica
- Noticias y actualidad
- Calculadora farmaceutica

## Tecnologias

- Python 3.12
- Django 5.2
- SQLite para desarrollo local
- PostgreSQL para produccion
- Bootstrap 5
- OpenPyXL
- ReportLab

## Puesta en marcha local

1. Crear y activar un entorno virtual.
2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Crear un archivo `.env` en la raiz del proyecto:

```env
SECRET_KEY=tu_clave
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DB_ENGINE=sqlite
SQLITE_NAME=db.sqlite3
```

4. Aplicar migraciones:

```bash
python manage.py migrate
```

5. Crear un usuario administrador:

```bash
python manage.py createsuperuser
```

6. Ejecutar el servidor:

```bash
python manage.py runserver
```

## Estado actual

El proyecto incluye autenticacion, roles, gestion principal de datos, exportaciones, vistas adaptadas a movil y navegacion diferenciada por rol.
