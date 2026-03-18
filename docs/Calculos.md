# Modulo de Calculos

## Objetivo

El modulo de calculos fue incorporado al sistema para apoyar procesos academicos y tecnicos relacionados con la formulacion magistral.

Su finalidad es reducir errores manuales y facilitar operaciones matematicas frecuentes dentro del laboratorio.

## Apartados del modulo

### 1. Calculo de dosis por proporcionalidad

El calculo de dosis por proporcionalidad es una herramienta matematica aplicada para calcular equivalencias entre una dosis requerida y una presentacion disponible.

Sirve para saber cuanto volumen se debe administrar cuando se conoce:

- la dosis requerida
- la cantidad disponible del medicamento
- el volumen en el que esa cantidad esta contenida

#### Ejemplo

Si se necesita administrar `15 mg` y se dispone de `200 mg en 2 ml`, el sistema calcula cuantos `ml` corresponden a esos `15 mg`.

#### Que calcula el sistema

- dosis requerida en mg
- cantidad disponible en mg
- volumen disponible en ml
- volumen final a administrar en ml

#### Utilidad

Evita errores de dosificacion y ayuda a obtener la cantidad exacta a administrar.

### 2. Dosis por peso

Sirve cuando la dosis depende del peso del paciente.

#### Ejemplo

- paciente pesa `20 kg`
- dosis es `5 mg/kg`

El sistema calcula:

- dosis total en mg
- y luego cuanto volumen corresponde

#### Proceso

Primero calcula:

`peso x dosis por kg = dosis total`

Despues aplica un calculo de proporcionalidad usando la concentracion disponible para obtener el volumen a administrar.

#### Utilidad

Este tipo de calculo es importante cuando la dosificacion cambia segun el peso corporal.

### 3. Ajuste de componentes

Sirve para recalcular una formulacion completa.

#### Ejemplo

Si una formula base esta pensada en proporciones y se desea preparar una cantidad final diferente, el sistema ajusta cuanto de cada componente se necesita.

#### Que hace el sistema

- toma una formulacion registrada
- analiza sus componentes
- calcula una nueva cantidad ajustada para cada materia prima
- mantiene la proporcion original de la formulacion

#### Utilidad

Esto ayuda a escalar una formulacion sin recalcular todo a mano.

## Importancia academica y tecnica

La inclusion de este modulo es importante porque:

- fortalece el aprendizaje practico del estudiante
- apoya el trabajo del docente
- reduce errores de calculo
- mejora la seguridad en la preparacion y dosificacion

## Alcance del modulo

El modulo de calculos es una herramienta de apoyo. Sus resultados deben interpretarse como ayuda matematica dentro del laboratorio y no sustituyen la validacion academica, tecnica o profesional.

## Relacion con el sistema

El modulo se conecta con las formulaciones del sistema, especialmente en el apartado de ajuste de componentes, donde usa los registros existentes para recalcular proporciones automaticamente.

## Conclusion

El modulo de calculos convierte al sistema en una herramienta no solo de registro y control, sino tambien de apoyo directo a la formulacion magistral y al aprendizaje academico.
