# Arquitectura Propuesta

## Enfoque general

Se propone una arquitectura monolitica modular con Django, adecuada para una primera version institucional por su rapidez de desarrollo, facilidad de mantenimiento y buena integracion con PostgreSQL.

## Capas

### 1. Presentacion

- Vistas basadas en Django Templates
- Formularios para alta, edicion y consulta
- Panel principal con indicadores y alertas

### 2. Aplicacion

Apps de negocio separadas por dominio:

- `usuarios`: roles, perfiles, permisos
- `inventario`: materias primas
- `formulaciones`: formulaciones y detalle
- `alertas`: reglas y seguimiento de alertas
- `dashboard`: reportes y resumen ejecutivo

### 3. Persistencia

- PostgreSQL como motor principal
- Modelos Django ORM para relaciones y validaciones

## Apps sugeridas

## `usuarios`

Responsabilidades:

- autenticacion
- autorizacion
- roles
- gestion de cuentas

Implementacion sugerida:

- usar `AbstractUser`
- agregar campo `rol`
- usar `is_active` para desactivar cuentas sin borrarlas

## `inventario`

Responsabilidades:

- CRUD de materias primas
- filtros por estado, lote, vencimiento y stock
- historial de actualizacion

## `formulaciones`

Responsabilidades:

- CRUD de formulaciones
- asociacion con materias primas mediante tabla intermedia
- consulta tecnica y academica

## `alertas`

Responsabilidades:

- generacion automatica de alertas
- clasificacion por prioridad
- seguimiento de estado

## `dashboard`

Responsabilidades:

- resumen de indicadores
- alertas activas
- conteos de materias primas y formulaciones

## Estrategia de permisos

### Administrador

- acceso total
- gestiona usuarios
- crea, edita y elimina materias primas y formulaciones
- revisa y gestiona todas las alertas

### Profesor

- crea y edita formulaciones
- consulta materias primas
- revisa alertas
- actualiza informacion tecnica autorizada

### Estudiante

- consulta materias primas
- consulta formulaciones
- no modifica informacion

## Flujo de alertas

Las alertas pueden generarse con una tarea programada diaria o al guardar una materia prima.

Reglas recomendadas:

- proxima a caducar: faltan 30 dias o menos para el vencimiento
- caducada: fecha actual mayor a fecha de vencimiento
- stock bajo: stock actual menor o igual a stock minimo y mayor que 0
- sin stock: stock actual igual a 0

## Consideraciones tecnicas

- usar claves primarias autoincrementales
- usar catalogos para valores controlados
- evitar borrar datos criticos de forma fisica
- preferir estados activos e inactivos
- registrar usuario creador y fechas de auditoria

