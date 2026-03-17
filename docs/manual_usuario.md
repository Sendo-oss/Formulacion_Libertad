# Manual de Usuario del Sistema

## Nombre del sistema

Sistema web de gestion de formulaciones magistrales para el laboratorio academico de farmacia del Instituto Superior Tecnologico Universitario Libertad.

## Objetivo del sistema

El sistema permite registrar, consultar y controlar la informacion del laboratorio de formulacion magistral. Su finalidad es mejorar la organizacion de materias primas, formulaciones, usuarios, alertas y calculos de apoyo, reduciendo errores de registro manual y facilitando el trabajo academico.

## Modulos principales

### 1. Dashboard

Es la pantalla principal del sistema.

Permite visualizar rapidamente:

- total de materias primas
- total de formulaciones
- materias primas proximas a vencer
- materias primas sin stock
- alertas activas

Tambien incluye accesos rapidos hacia inventario, formulaciones y alertas.

### 2. Materias primas

Este modulo sirve para registrar y consultar los insumos del laboratorio.

Cada materia prima puede contener:

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

Funciones disponibles:

- crear materias primas
- editar registros existentes
- filtrar por estado y nivel de stock
- exportar a Excel
- exportar a PDF
- visualizar ficha individual en PDF

### 3. Formulaciones

Este modulo almacena las formulaciones magistrales o preparaciones del laboratorio.

Cada formulacion contiene:

- codigo
- nombre
- categoria
- tipo de formulacion
- origen
- estado
- fuente de referencia
- descripcion
- observaciones

Ademas, cada formulacion puede incluir varios componentes, indicando:

- materia prima
- cantidad
- unidad de medida
- orden

Funciones disponibles:

- crear formulaciones
- editar formulaciones
- activar o desactivar formulaciones
- visualizar sus componentes
- exportar a Excel
- exportar a PDF
- generar ajuste de componentes desde la calculadora

### 4. Alertas

Este modulo muestra notificaciones generadas automaticamente por el sistema.

Tipos de alertas:

- proxima caducidad
- caducada
- stock bajo
- sin stock

Funciones disponibles:

- consultar alertas
- filtrar por prioridad
- filtrar por estado
- marcar alerta como revisada
- cerrar alerta
- exportar a Excel
- exportar a PDF

### 5. Calculadora

Este modulo sirve como apoyo academico y tecnico para realizar calculos de formulacion y dosificacion.

Incluye tres apartados:

- regla de tres
- dosis por peso
- ajuste de componentes

Su explicacion detallada se encuentra en [Calculos.md](./Calculos.md).

### 6. Usuarios

Este modulo permite gestionar cuentas y roles del sistema.

Roles disponibles:

- Administrador
- Profesor
- Estudiante

## Roles del sistema

### Administrador

Puede:

- crear, editar y consultar usuarios
- gestionar materias primas
- gestionar formulaciones
- consultar y actualizar alertas
- exportar reportes

### Profesor

Puede:

- consultar materias primas
- registrar y editar formulaciones
- consultar y gestionar alertas
- usar la calculadora

### Estudiante

Puede:

- consultar materias primas
- consultar formulaciones
- usar la calculadora

No puede modificar registros del sistema.

## Flujo general de uso

### Paso 1. Iniciar sesion

El usuario accede con sus credenciales desde la pantalla de login.

### Paso 2. Revisar el dashboard

Al ingresar, el usuario visualiza un resumen del estado general del laboratorio.

### Paso 3. Gestionar informacion

Segun su rol, puede:

- registrar materias primas
- registrar formulaciones
- revisar alertas
- realizar calculos

### Paso 4. Exportar reportes

Desde los modulos principales es posible descargar reportes en Excel o PDF.

## Alertas automaticas

El sistema genera alertas cuando:

- una materia prima esta proxima a caducar
- una materia prima ya caducó
- una materia prima tiene stock bajo
- una materia prima se encuentra sin stock

Esto permite una toma de decisiones mas rapida y mejora el control del laboratorio.

## Exportacion de reportes

Los reportes PDF incluyen:

- logo institucional
- encabezado institucional
- fecha de emision
- nombre del usuario que generó el reporte
- numeracion de pagina

## Recomendaciones de uso

- mantener actualizados los lotes y fechas de vencimiento
- revisar periodicamente el modulo de alertas
- verificar las formulaciones antes de su uso academico
- utilizar la calculadora como apoyo para reducir errores de calculo

## Conclusion

El sistema integra control de inventario, formulaciones, alertas y calculos en una sola plataforma web. Esto mejora la organizacion del laboratorio academico y ofrece una herramienta util tanto para gestion como para docencia.
