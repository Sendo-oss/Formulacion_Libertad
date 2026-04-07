<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
# Sistema Web de Formulacion Magistral

Base funcional y tecnica de un sistema web de gestion de formulaciones magistrales en un laboratorio academico de farmacia.

## Objetivo

Centralizar la administracion de materias primas, formulaciones magistrales, usuarios y alertas tempranas para mejorar el control del laboratorio, reducir errores de registro y facilitar la consulta academica.

## Stack propuesto

- Backend: Django
- Base de datos: PostgreSQL
- Interfaz web: Django Templates con Bootstrap o similar
- Autenticacion: sistema de usuarios de Django con control de permisos por rol

## Modulos principales

- Usuarios
- Materias primas
- Formulaciones
- Alertas
- Reportes y consultas

## Estructura del proyecto creada

```text
formulacion_libertad/
  manage.py
  requirements.txt
  .env.example
  config/
    settings.py
    urls.py
    wsgi.py
    asgi.py
  apps/
    usuarios/
    inventario/
    formulaciones/
    alertas/
    dashboard/
  templates/
  static/
  media/
  docs/
```

## Documentacion incluida

- [Requisitos](./docs/requisitos.md)
- [Arquitectura](./docs/arquitectura.md)
- [Modelo de datos](./docs/modelo_datos.md)
- [Casos de uso](./docs/casos_de_uso.md)
- [Manual de usuario](./docs/manual_usuario.md)
- [Modulo de calculos](./docs/Calculos.md)

## Arranque del proyecto

1. Crear un entorno virtual.
2. Instalar dependencias con `pip install -r requirements.txt`.
3. Crear la base de datos PostgreSQL `formulacion_libertad`.
4. Configurar variables de entorno usando `.env.example`.
5. Ejecutar `python manage.py makemigrations`.
6. Ejecutar `python manage.py migrate`.
7. Crear superusuario con `python manage.py createsuperuser`.
8. Levantar servidor con `python manage.py runserver`.

## Implementacion realizada

- Proyecto Django base con configuracion central en `config`.
- Usuario personalizado con rol institucional.
- Apps separadas para `usuarios`, `inventario`, `formulaciones`, `alertas` y `dashboard`.
- Modelos principales segun el diseno funcional.
- Vistas iniciales con control de acceso por rol.
- Formularios para usuarios, materias primas y formulaciones.
- Admin de Django configurado para las entidades centrales.
- Servicio base para generacion automatica de alertas.
- Templates iniciales para login, dashboard y listados.

## Recomendacion de implementacion por fases

1. Crear proyecto Django y configurar PostgreSQL.
2. Implementar autenticacion y roles.
3. Implementar modulo de materias primas.
4. Implementar modulo de formulaciones con tabla intermedia.
5. Implementar generacion automatica de alertas.
6. Agregar reportes, filtros y panel de control.

## Nota importante

El entorno actual no tiene Django instalado, por eso no se generaron migraciones reales en esta sesion. La estructura y los archivos quedaron listos para ejecutar esos pasos apenas instales dependencias.
=======
=======
>>>>>>> theirs
=======
>>>>>>> theirs
# Sistema web de formulaciones magistrales (Diseño base)

Este repositorio contiene una propuesta de diseño técnico y de datos para un sistema web de gestión de formulaciones magistrales en un laboratorio académico de farmacia.

## Stack propuesto
- **Backend:** Django
- **Base de datos:** PostgreSQL
- **Frontend:** plantillas Django + Bootstrap (interfaz simple para consulta y gestión)

## Objetivo
Centralizar la gestión de materias primas y formulaciones, habilitar control por roles y generar alertas automáticas de vencimiento/stock.

## Entregables incluidos
1. Diseño funcional y de arquitectura: `docs/arquitectura.md`
2. Modelo de datos y relaciones: `docs/modelo_datos.md`
3. Ejemplo de implementación inicial en Django: `backend/laboratorio/models.py`
<<<<<<< ours
<<<<<<< ours
=======
4. Guía de puesta en marcha y troubleshooting: `docs/puesta_en_marcha.md`
>>>>>>> theirs
=======
4. Guía de puesta en marcha y troubleshooting: `docs/puesta_en_marcha.md`
>>>>>>> theirs

## Roles del sistema
- **Administrador:** control total (CRUD de usuarios, materias primas, formulaciones, alertas).
- **Profesor:** registra/edita formulaciones, consulta materias primas, revisa alertas.
- **Estudiante:** consulta información en modo solo lectura.
<<<<<<< ours
<<<<<<< ours
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
