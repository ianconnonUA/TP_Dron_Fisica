# Guía de Resolución - TP2: Trabajo, Energía y Potencia

## Cómo fui pensando cada ejercicio

---

## Ejercicio 1: Ascenso Vertical

### Planteo físico
El dron sube verticalmente. Las fuerzas son:
- **Motor** (hacia arriba): F_motor
- **Peso** (hacia abajo): m·g = 15 × 9.81 = 147.15 N
- **Arrastre** (hacia abajo, opone al movimiento): F_d = k·v² = 0.1·v²

La 2da Ley de Newton queda:
```
m·a = F_motor - m·g - k·v²
```

### Restricción de potencia
El motor tiene potencia máxima P_max = 2500 W. Como P = F·v:
```
F_motor ≤ P_max / v
```
A velocidad baja, P_max/v → ∞ (no hay limitación de potencia), así que usé un **cap de fuerza de 500 N** (valor realista para un dron de 15 kg).

### Estrategia de tiempo mínimo
Para minimizar el tiempo de ascenso, el dron debe aplicar la **máxima fuerza posible** en todo momento:
- Si v < P_max/F_cap → F = F_cap = 500N (limitado por torque)
- Si v ≥ P_max/F_cap → F = P_max/v (limitado por potencia)
- La transición ocurre en v = 2500/500 = 5 m/s

### Integración numérica (Euler semi-implícito)
Usé dt = 0.001 s. En cada paso:
1. Calcular fuerzas → aceleración
2. Actualizar velocidad (v_new = v + a·dt)
3. Usar velocidad promedio para calcular trabajo
4. Actualizar posición con v nueva

### Resultado
- **Tiempo mínimo**: ~7.4 s
- **Energía consumida**: ~18,328 J < 25,000 J → **CUMPLE**
- **Balance energético**: ΔK + ΔU ≈ W_motor + W_fricción (error ~1 J)

---

## Ejercicio 2: Navegación 3D con Viento

### Planteo físico
Ahora el dron va de A=(0,0,0) a B=(80,50,60) en 3D. El viento (5,-2,0) m/s modifica la **velocidad relativa**.

### Fricción con velocidad relativa
La clave es que la fricción actúa sobre la velocidad **relativa al aire**:
```
v_rel = v_dron - v_viento
F_fricción = -k · |v_rel| · v_rel
```

Si el viento va a favor (eje X, +5 m/s), la velocidad relativa es **menor** → menos fricción.
Si el viento va en contra (eje Y, -2 m/s), la velocidad relativa es **mayor** → más fricción.

### Dirección del motor
El dron siempre apunta hacia B desde su posición actual:
```
d̂ = (B - r) / |B - r|
F_motor = F_magnitud · d̂
```

### Ecuaciones vectoriales
```
m·a = F_motor + (0, 0, -mg) + F_fricción
```

### Análisis del viento
- **Eje X** (viento a favor): menor potencia necesaria para avanzar
- **Eje Y** (viento en contra): mayor potencia para avanzar contra el viento
- **Eje Z** (sin viento): solo lucha contra gravedad

---

## Ejercicio 3: Restricciones Reales

### Lo nuevo
Se agrega un **empuje estático máximo** de 400 N. Esto modela que a baja velocidad, el motor está limitado por torque, no por potencia.

### La restricción clave
```
F_mot ≤ min(F_static, P_max / |v|)
```

- A baja velocidad: F ≤ 400 N (limitado por **torque**)
- A alta velocidad: F ≤ 3000/v (limitado por **potencia**)
- **Transición**: cuando P_max/v = F_static → v = 3000/400 = **7.5 m/s**

### Balance energético
El teorema trabajo-energía dice:
```
ΔK + ΔU = W_motor + W_fricción
```
Donde W_fricción < 0 (disipa energía). Esto se verifica numéricamente integrando F·v·dt para cada fuerza.

### Resultado
- Llega en ~19.2 s < 20 s → **CUMPLE tiempo**
- Energía: ~22,068 J < 40,000 J → **CUMPLE energía**
- Balance cierra con error de ~18 J (propio de método Euler)

---

## Notas sobre la implementación

### Método numérico
- **Euler semi-implícito** con dt = 0.001 s
- Se actualiza v primero, luego se usa para posición
- El trabajo se calcula con velocidad promedio del paso para mayor precisión

### Librerías
- `numpy`: cálculos vectoriales en 3D
- `matplotlib`: gráficos 2D y 3D

### Gráficos generados
1. `ej1_ascenso_vertical.png` - Posición, velocidad, potencia y energía vs tiempo
2. `ej2_trayectoria_3d.png` - Trayectoria 3D del dron
3. `ej2_analisis_vuelo.png` - Velocidades, potencia y potencia por componente
4. `ej3_trayectoria_3d.png` - Trayectoria 3D con restricciones
5. `ej3_analisis_restricciones.png` - F_motor vs F_fricción, potencia, energía, velocidad
