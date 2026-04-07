<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
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

=======
=======
>>>>>>> theirs
=======
>>>>>>> theirs
# Arquitectura funcional propuesta

## 1. Módulos

### Módulo de Usuarios
- Gestión de cuentas y roles (`Administrador`, `Profesor`, `Estudiante`).
- Control de acceso con permisos de Django (`Group` + `Permission`).
- Trazabilidad de quién crea o actualiza registros críticos.

### Módulo de Materias Primas
Permite crear y mantener registros con los campos:
- nombre
- número CAS
- número EINECS
- lote
- fecha de elaboración
- fecha de vencimiento
- casa comercial
- stock actual
- stock mínimo
- unidad de medida
- observaciones
- estado

Reglas clave:
- Todo registro debe poder editarse.
- El estado puede calcularse con base en fechas y stock (opcional) o mantenerse manual.

### Módulo de Formulaciones
- Registro de formulaciones magistrales.
- Datos principales:
  - código
  - nombre
  - descripción
  - tipo
  - origen (`institucional` o `docente`)
  - estado
  - observaciones
- Relación N:M con materias primas por tabla intermedia `FormulacionDetalle`.
- En `FormulacionDetalle` se guarda cantidad y unidad.

### Módulo de Alertas
Generación automática de alertas cuando una materia prima:
- está próxima a caducar
- está caducada
- tiene stock bajo
- está sin stock

Datos de alerta:
- tipo
- materia prima
- mensaje
- prioridad
- estado
- fecha de generación

## 2. Arquitectura por capas

1. **Presentación (Django Templates):**
   - Vistas de consulta y formularios CRUD.
   - Panel de alertas con filtros por prioridad/estado.

2. **Aplicación (Django Views/Services):**
   - Lógica de negocio para validaciones y permisos.
   - Servicios para generación y cierre de alertas.

3. **Persistencia (Django ORM + PostgreSQL):**
   - Modelos normalizados para usuarios, materias primas, formulaciones y alertas.

4. **Tareas programadas (cron/Celery beat):**
   - Proceso diario para recalcular alertas de vencimiento y stock.

## 3. Control de acceso (RBAC)

- `Administrador`: CRUD completo + administración de usuarios.
- `Profesor`: crear/editar formulaciones y consultar/actualizar información técnica autorizada.
- `Estudiante`: lectura de materias primas, formulaciones y alertas visibles.

Sugerencia: usar decoradores `@permission_required` y validaciones en consultas para restringir mutaciones.

## 4. Escalabilidad funcional

Para permitir nuevas formulaciones sin modificar código:
- Modelar formulaciones de forma parametrizable (datos en BD, no hardcodeados).
- Usar tabla detalle para ingredientes y cantidades dinámicas.
- Evitar lógica acoplada a códigos fijos de formulación.
<<<<<<< ours
<<<<<<< ours
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
