# Requisitos del Sistema

## Requisitos funcionales

### RF-01. Gestion de usuarios

El sistema debe permitir crear, editar, desactivar y consultar usuarios.

### RF-02. Gestion de roles

El sistema debe manejar tres roles:

- Administrador
- Profesor
- Estudiante

### RF-03. Control de acceso

El sistema debe restringir funcionalidades segun el rol autenticado.

### RF-04. Registro de materias primas

El sistema debe permitir registrar materias primas con estos campos:

- nombre
- numero CAS
- numero EINECS
- lote
- fecha de elaboracion
- fecha de vencimiento
- casa comercial
- stock actual
- stock minimo
- unidad de medida
- observaciones
- estado

### RF-05. Edicion de materias primas

Toda la informacion de materias primas debe poder editarse.

### RF-06. Consulta de materias primas

Los tres roles deben poder consultar materias primas segun sus permisos.

### RF-07. Registro de formulaciones

El sistema debe permitir crear formulaciones magistrales con:

- codigo de formulacion
- nombre
- descripcion
- tipo de formulacion
- origen
- estado
- observaciones

### RF-08. Detalle de formulaciones

Cada formulacion debe poder asociar multiples materias primas con:

- cantidad
- unidad de medida

### RF-09. Consulta de formulaciones

Los estudiantes deben poder consultar formulaciones sin modificarlas.

### RF-10. Generacion de alertas

El sistema debe generar alertas cuando una materia prima:

- este proxima a caducar
- este caducada
- tenga stock bajo
- este sin stock

### RF-11. Consulta de alertas

Administrador y profesor deben poder consultar alertas.

### RF-12. Estado de alertas

Las alertas deben registrar:

- tipo
- materia prima relacionada
- mensaje
- prioridad
- estado
- fecha de generacion

### RF-13. Trazabilidad

El sistema debe registrar que usuario creo o actualizo materias primas y formulaciones.

### RF-14. Escalabilidad funcional

El sistema debe permitir agregar nuevas formulaciones sin modificar el codigo fuente del sistema.

## Requisitos no funcionales

### RNF-01. Usabilidad

La interfaz debe ser sencilla y adecuada para personal academico y estudiantes.

### RNF-02. Seguridad

El acceso debe requerir autenticacion y autorizacion por rol.

### RNF-03. Integridad

La base de datos debe asegurar consistencia entre formulaciones, materias primas y alertas.

### RNF-04. Mantenibilidad

El sistema debe organizarse por apps Django para facilitar crecimiento futuro.

### RNF-05. Disponibilidad

El sistema debe funcionar en red local o servidor institucional.

