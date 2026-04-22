# TP2 - Trabajo, Energía y Potencia en Sistemas Dinámicos 🚁

## Resumen del Problema

Se trata de un **dron de transporte de insumos médicos** que debe realizar distintas misiones. Hay 3 ejercicios con dificultad creciente:

1. **Ascenso vertical** (1D) con resistencia del aire y límites de potencia/energía
2. **Navegación 3D** con viento cruzado
3. **Restricciones reales** de motor (empuje estático + potencia) y balance energético

---

## Ejercicio 1: Ascenso Vertical y Gestión de Energía

### Datos
| Parámetro | Valor |
|-----------|-------|
| Masa (m) | 15 kg |
| Altura objetivo (H) | 100 m |
| Resistencia del aire | F_d = k·v², k = 0.1 kg/m |
| Potencia máxima (P_max) | 2500 W |
| Energía máxima (E_max) | 25,000 J |

### Enfoque Teórico

**Consigna 1 — Ecuaciones dinámicas:**

Para ascenso vertical, aplicamos la 2da Ley de Newton en el eje vertical (positivo hacia arriba):

```
m·a = F_motor - m·g - k·v²
```

Donde:
- `F_motor` es la fuerza de empuje del motor
- `m·g` es el peso (147.15 N)
- `k·v²` es la resistencia del aire (siempre opuesta al movimiento → hacia abajo si sube)

La **restricción de potencia** limita la fuerza del motor:

```
P = F_motor · v  ≤  P_max
⟹  F_motor ≤ P_max / v
```

Para minimizar el tiempo, queremos aplicar la máxima fuerza posible:
- A baja velocidad: `F_motor` puede ser muy grande (pero en el Ej.3 se limita con empuje estático)
- A alta velocidad: `F_motor = P_max / v`

**Consigna 2 — Integración numérica (Euler):**

Estrategia: usar `F_motor = P_max / v` (máxima potencia), y resolver con paso temporal:

```python
# En cada paso dt:
F_motor = P_max / max(v, epsilon)  # evitar div por cero
a = (F_motor - m*g - k*v**2) / m
v = v + a*dt
y = y + v*dt
E_total += F_motor * v * dt  # energía consumida
```

**Consigna 3 — Verificación de energía:**

Calcular la energía total consumida por el motor y verificar que `E_consumida ≤ E_max = 25,000 J`.

Balance: `E_motor = ΔE_cinética + ΔE_potencial + W_fricción`

### Implementación
- Método de Euler con `dt = 0.001 s`
- Cortar cuando `y ≥ H = 100 m`
- Graficar: posición vs tiempo, velocidad vs tiempo, potencia vs tiempo, energía acumulada

---

## Ejercicio 2: Navegación 3D con Viento Cruzado

### Datos
| Parámetro | Valor |
|-----------|-------|
| Posición inicial A | (0, 0, 0) m |
| Posición destino B | (80, 50, 60) m |
| Viento v_w | (5, −2, 0) m/s |
| Coef. arrastre k | 0.15 kg/m |
| Potencia máxima P_max | 3000 W |

### Enfoque Teórico

**Consigna 1 — Fuerza de fricción con velocidad relativa:**

La fricción actúa sobre la **velocidad relativa** del dron respecto al aire:

```
v_rel = v_dron - v_viento
F_fricción = -k · |v_rel| · v_rel
```

Es decir, la magnitud es `k·|v_rel|²` y la dirección es opuesta a `v_rel`.

**Consigna 2 — Simulación 3D:**

Ecuaciones de movimiento vectoriales:

```
m·a = F_motor + F_gravedad + F_fricción
```

Donde `F_gravedad = (0, 0, -m·g)`.

**Estrategia de dirección del motor:** El dron apunta siempre hacia B desde su posición actual. La dirección unitaria es:

```
d̂ = (B - r) / |B - r|
```

Y la fuerza del motor se aplica en esa dirección, limitada por potencia:

```
F_motor_magnitud = min(F_deseada, P_max / |v|)
F_motor = F_motor_magnitud · d̂
```

**Consigna 3 — Análisis de impacto del viento:**

- Eje X: viento = +5 m/s → **a favor** del movimiento (si el dron va hacia x=80)
- Eje Y: viento = -2 m/s → **en contra** (el dron va hacia y=50, el viento empuja a y negativo)

Calcular la potencia consumida desglosada por componentes para mostrar el impacto.

### Implementación
- Integración Euler en 3D con vectores numpy
- Condición de parada: `|r - B| < tolerancia`
- Gráficos: trayectoria 3D, componentes de velocidad, potencia instantánea

---

## Ejercicio 3: Desafío de Diseño y Restricciones Reales

### Datos Adicionales
| Parámetro | Valor |
|-----------|-------|
| Empuje máximo estático | 400 N |
| Tiempo límite de misión | 20 s |
| Energía máxima | 40,000 J |

### Enfoque Teórico

**Consigna 1 — Restricción de fuerza del motor:**

```
F_mot ≤ min(F_static, P_max / |v|)
```

Esto modela que:
- A **baja velocidad**: el motor está limitado por el **torque** → `F_mot ≤ 400 N`
- A **alta velocidad**: el motor está limitado por la **potencia** → `F_mot ≤ 3000/|v|`
- La transición ocurre cuando `P_max / v = F_static` → `v_transición = P_max / F_static = 7.5 m/s`

**Consigna 2 — Gráfico F_motor vs F_fricción:**

Graficar ambas fuerzas en función del tiempo para identificar visualmente el cruce entre régimen limitado por torque y por potencia.

**Consigna 3 — Balance energético:**

```
ΔK + ΔU = W_motor + W_fricción
```

Donde:
- `ΔK = ½·m·v_f² - 0` (energía cinética)
- `ΔU = m·g·z_f` (energía potencial gravitatoria)
- `W_motor = ∫ F_motor · v dt` (integral numérica)
- `W_fricción = ∫ F_fricción · v dt` (negativo, disipado)

### Implementación
- Modificar el algoritmo del Ej.2 con la nueva restricción
- Graficar F_motor y F_fricción vs tiempo
- Calcular y verificar el balance energético numéricamente

---

## Estructura del Código

Propongo crear **un único archivo Python** (`tp2_dron.py`) con 3 secciones bien separadas, y que genere todos los gráficos solicitados. Usaremos:
- `numpy` para cálculos vectoriales
- `matplotlib` para gráficos 2D y 3D

### Archivos

#### [NEW] [tp2_dron.py](file:///c:/Users/ianvc_utdtct5/OneDrive/Escritorio/UA/2doAño/Fisica/TP2/tp2_dron.py)
Código principal con los 3 ejercicios, bien comentado.

#### [NEW] [guia_resolucion.md](file:///c:/Users/ianvc_utdtct5/OneDrive/Escritorio/UA/2doAño/Fisica/TP2/guia_resolucion.md)
Documento con la guía paso a paso de cómo se pensó y resolvió cada ejercicio.

---

## Verificación

### Automated Tests
- Ejecutar el script Python y verificar que:
  - El dron llega a H=100m en el Ej.1
  - La energía consumida se calcula correctamente
  - El dron llega a B en el Ej.2
  - El balance energético cierra en el Ej.3

### Checks Físicos
- La velocidad terminal debe existir (cuando F_motor = mg + kv²)
- La energía mínima teórica es `m·g·H = 15 × 9.81 × 100 ≈ 14,715 J` (solo potencial, sin fricción)
- El trabajo de fricción debe ser negativo (disipa energía)

---

## Open Questions

> [!IMPORTANT]
> **¿Querés que el código esté todo en un archivo o separado en módulos?** Propongo un solo archivo para simplicidad de entrega.

> [!NOTE]
> **¿Tenés numpy y matplotlib instalados?** Si no, los instalo antes de ejecutar.

> [!NOTE]
> **¿Querés que los gráficos se guarden como imágenes (PNG) además de mostrarse?** Esto puede ser útil para el informe.
