# Sistema Web de Formulación Magistral

Aplicación web desarrollada con Django para la gestión académica e institucional de formulaciones magistrales, materias primas, documentación técnica, alertas y cálculos de apoyo en laboratorio.

## Módulos principales

- Usuarios y control por roles
- Inventario de materias primas
- Formulaciones magistrales
- Alertas operativas
- Documentación técnica
- Noticias y actualidad
- Calculadora farmacéutica

## Tecnologías

- Python 3.12
- Django 5.2
- PostgreSQL
- Bootstrap 5
- OpenPyXL
- ReportLab

## Puesta en marcha

1. Crear y activar un entorno virtual.
2. Instalar dependencias con:

```bash
pip install -r requirements.txt
```

3. Crear un archivo `.env` en la raíz del proyecto con valores como estos:

```env
SECRET_KEY=tu_clave
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=formulacion_magistral_db
DB_USER=postgres
DB_PASSWORD=tu_password
DB_HOST=127.0.0.1
DB_PORT=5432
```

4. Aplicar migraciones:

```bash
python manage.py migrate
```

5. Crear superusuario:

```bash
python manage.py createsuperuser
```

6. Ejecutar el servidor:

```bash
python manage.py runserver
```

## Documentación incluida

- `docs/arquitectura.md`
- `docs/modelo_datos.md`
- `docs/puesta_en_marcha.md`

## Estado actual

El proyecto ya incluye autenticación, roles, gestión principal de datos, exportaciones, vistas adaptadas a móvil y una navegación móvil diferenciada por rol.

## Autor

Desarrollado por Michael Buitrón  
📧 michusty07@gmail.com
