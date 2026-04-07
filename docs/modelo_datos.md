<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
# Modelo de Datos

## Entidades principales

### Rol

Aunque Django puede operar con grupos y permisos, para este sistema conviene manejar el rol de forma explicita en el usuario.

Valores sugeridos:

- ADMINISTRADOR
- PROFESOR
- ESTUDIANTE

### Usuario

Campos sugeridos:

- id
- username
- first_name
- last_name
- email
- password
- rol
- is_active
- date_joined

### MateriaPrima

Campos:

- id
- nombre
- numero_cas
- numero_einecs
- lote
- fecha_elaboracion
- fecha_vencimiento
- casa_comercial
- stock_actual
- stock_minimo
- unidad_medida
- observaciones
- estado
- registrado_por_id
- creado_en
- actualizado_en

Estados sugeridos:

- ACTIVA
- INACTIVA
- VENCIDA

### Formulacion

Campos:

- id
- codigo
- nombre
- descripcion
- tipo_formulacion
- origen
- estado
- observaciones
- creado_por_id
- creado_en
- actualizado_en

Origen sugerido:

- INSTITUCIONAL
- DOCENTE

Estado sugerido:

- ACTIVA
- INACTIVA
- EN_REVISION

### FormulacionDetalle

Tabla intermedia entre formulacion y materia prima.

Campos:

- id
- formulacion_id
- materia_prima_id
- cantidad
- unidad_medida

Restriccion sugerida:

- unico por `formulacion_id + materia_prima_id`

### Alerta

Campos:

- id
- tipo_alerta
- materia_prima_id
- mensaje
- prioridad
- estado
- fecha_generacion
- atendida_por_id
- fecha_atencion

Tipos sugeridos:

- PROXIMA_CADUCIDAD
- CADUCADA
- STOCK_BAJO
- SIN_STOCK

Prioridades sugeridas:

- BAJA
- MEDIA
- ALTA
- CRITICA

Estado sugerido:

- ACTIVA
- REVISADA
- CERRADA

## Relaciones

- un usuario registra muchas materias primas
- un usuario crea muchas formulaciones
- una formulacion tiene muchos detalles
- una materia prima puede estar en muchos detalles
- una materia prima puede tener muchas alertas

## Diagrama relacional

```text
USUARIO
- id (PK)
- rol

MATERIA_PRIMA
- id (PK)
- registrado_por_id (FK -> USUARIO.id)

FORMULACION
- id (PK)
- creado_por_id (FK -> USUARIO.id)

FORMULACION_DETALLE
- id (PK)
- formulacion_id (FK -> FORMULACION.id)
- materia_prima_id (FK -> MATERIA_PRIMA.id)

ALERTA
- id (PK)
- materia_prima_id (FK -> MATERIA_PRIMA.id)
- atendida_por_id (FK -> USUARIO.id)
```

## Modelos Django sugeridos

```python
from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    class Rol(models.TextChoices):
        ADMINISTRADOR = "ADMINISTRADOR", "Administrador"
        PROFESOR = "PROFESOR", "Profesor"
        ESTUDIANTE = "ESTUDIANTE", "Estudiante"

    rol = models.CharField(max_length=20, choices=Rol.choices)


class MateriaPrima(models.Model):
    nombre = models.CharField(max_length=150)
    numero_cas = models.CharField(max_length=50, blank=True)
    numero_einecs = models.CharField(max_length=50, blank=True)
    lote = models.CharField(max_length=80)
    fecha_elaboracion = models.DateField(null=True, blank=True)
    fecha_vencimiento = models.DateField()
    casa_comercial = models.CharField(max_length=150, blank=True)
    stock_actual = models.DecimalField(max_digits=10, decimal_places=2)
    stock_minimo = models.DecimalField(max_digits=10, decimal_places=2)
    unidad_medida = models.CharField(max_length=20)
    observaciones = models.TextField(blank=True)
    estado = models.CharField(max_length=20)
    registrado_por = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        related_name="materias_primas_registradas",
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)


class Formulacion(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    tipo_formulacion = models.CharField(max_length=100)
    origen = models.CharField(max_length=20)
    estado = models.CharField(max_length=20)
    observaciones = models.TextField(blank=True)
    creado_por = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        related_name="formulaciones_creadas",
    )
    materias_primas = models.ManyToManyField(
        MateriaPrima,
        through="FormulacionDetalle",
        related_name="formulaciones",
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)


class FormulacionDetalle(models.Model):
    formulacion = models.ForeignKey(Formulacion, on_delete=models.CASCADE)
    materia_prima = models.ForeignKey(MateriaPrima, on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    unidad_medida = models.CharField(max_length=20)

    class Meta:
        unique_together = ("formulacion", "materia_prima")


class Alerta(models.Model):
    tipo_alerta = models.CharField(max_length=30)
    materia_prima = models.ForeignKey(
        MateriaPrima,
        on_delete=models.CASCADE,
        related_name="alertas",
    )
    mensaje = models.TextField()
    prioridad = models.CharField(max_length=20)
    estado = models.CharField(max_length=20, default="ACTIVA")
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    atendida_por = models.ForeignKey(
        Usuario,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="alertas_atendidas",
    )
    fecha_atencion = models.DateTimeField(null=True, blank=True)
```

=======
=======
>>>>>>> theirs
=======
>>>>>>> theirs
# Modelo de datos (ER lógico)

## Entidades principales

1. **Rol**
   - nombre (único): administrador, profesor, estudiante

2. **Usuario**
   - username, email, password
   - rol (FK a rol)

3. **MateriaPrima**
   - nombre
   - cas
   - einecs
   - lote
   - fecha_elaboracion
   - fecha_vencimiento
   - casa_comercial
   - stock_actual
   - stock_minimo
   - unidad_medida
   - observaciones
   - estado
   - creado_por (FK a usuario)

4. **Formulacion**
   - codigo (único)
   - nombre
   - descripcion
   - tipo_formulacion
   - origen (institucional/docente)
   - estado
   - observaciones
   - creado_por (FK a usuario)

5. **FormulacionDetalle** (tabla intermedia)
   - formulacion (FK)
   - materia_prima (FK)
   - cantidad
   - unidad_medida
   - restricción única (formulación + materia prima)

6. **Alerta**
   - tipo_alerta (proxima_caducidad/caducada/stock_bajo/sin_stock)
   - materia_prima (FK)
   - mensaje
   - prioridad (baja/media/alta/critica)
   - estado (nueva/en_revision/resuelta)
   - fecha_generacion

## Relaciones
- Un rol tiene muchos usuarios (1:N).
- Un usuario registra muchas materias primas (1:N).
- Un usuario crea muchas formulaciones (1:N).
- Una formulación tiene muchas materias primas (N:M con `FormulacionDetalle`).
- Una materia prima participa en muchas formulaciones (N:M).
- Una materia prima tiene muchas alertas (1:N).

## Reglas recomendadas
- Índices en `cas`, `lote`, `fecha_vencimiento` y `estado` en materias primas.
- Índices en `tipo_alerta`, `estado`, `fecha_generacion` en alertas.
- `stock_actual` y `stock_minimo` con validación >= 0.
- Restricción de unicidad para `codigo` en formulaciones.
<<<<<<< ours
<<<<<<< ours
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
