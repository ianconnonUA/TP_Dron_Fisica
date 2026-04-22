import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

masa_dron = 15.0
coeficiente_arrastre = 0.15
potencia_maxima_motor = 3000.0
gravedad = 9.81

destino_x = 80.0
destino_y = 50.0
destino_z = 60.0

velocidad_viento_x = 5.0
velocidad_viento_y = -2.0
velocidad_viento_z = 0.0

posicion_x = 0.0
posicion_y = 0.0
posicion_z = 0.0

velocidad_x = 0.0
velocidad_y = 0.0
velocidad_z = 0.0

tiempo_actual = 0.0
paso_de_tiempo = 0.001
energia_consumida_motor = 0.0

historial_tiempo = [0.0]
historial_x = [0.0]
historial_y = [0.0]
historial_z = [0.0]
historial_velocidad_x = [0.0]
historial_velocidad_y = [0.0]
historial_velocidad_z = [0.0]
historial_magnitud_velocidad = [0.0]
historial_potencia_total = [0.0]
historial_potencia_x = [0.0]
historial_potencia_y = [0.0]
historial_potencia_z = [0.0]

distancia_total_al_destino = math.sqrt((destino_x - posicion_x)**2 + (destino_y - posicion_y)**2 + (destino_z - posicion_z)**2)

while distancia_total_al_destino > 1.0 and tiempo_actual < 30.0:
    distancia_faltante_x = destino_x - posicion_x
    distancia_faltante_y = destino_y - posicion_y
    distancia_faltante_z = destino_z - posicion_z

    distancia_total_al_destino = math.sqrt(distancia_faltante_x**2 + distancia_faltante_y**2 + distancia_faltante_z**2)
    
    direccion_x = distancia_faltante_x / distancia_total_al_destino
    direccion_y = distancia_faltante_y / distancia_total_al_destino
    direccion_z = distancia_faltante_z / distancia_total_al_destino

    velocidad_absoluta_total = math.sqrt(velocidad_x**2 + velocidad_y**2 + velocidad_z**2)

    if velocidad_absoluta_total < 0.01:
        velocidad_efectiva = 0.01
    else:
        velocidad_efectiva = velocidad_absoluta_total

    magnitud_fuerza_motor = potencia_maxima_motor / velocidad_efectiva

    fuerza_motor_x = magnitud_fuerza_motor * direccion_x
    fuerza_motor_y = magnitud_fuerza_motor * direccion_y
    fuerza_motor_z = magnitud_fuerza_motor * direccion_z

    velocidad_relativa_x = velocidad_x - velocidad_viento_x
    velocidad_relativa_y = velocidad_y - velocidad_viento_y
    velocidad_relativa_z = velocidad_z - velocidad_viento_z

    magnitud_velocidad_relativa = math.sqrt(velocidad_relativa_x**2 + velocidad_relativa_y**2 + velocidad_relativa_z**2)

    fuerza_friccion_x = -coeficiente_arrastre * magnitud_velocidad_relativa * velocidad_relativa_x
    fuerza_friccion_y = -coeficiente_arrastre * magnitud_velocidad_relativa * velocidad_relativa_y
    fuerza_friccion_z = -coeficiente_arrastre * magnitud_velocidad_relativa * velocidad_relativa_z

    fuerza_neta_x = fuerza_motor_x + fuerza_friccion_x
    fuerza_neta_y = fuerza_motor_y + fuerza_friccion_y
    fuerza_neta_z = fuerza_motor_z + fuerza_friccion_z - (masa_dron * gravedad)

    aceleracion_x = fuerza_neta_x / masa_dron
    aceleracion_y = fuerza_neta_y / masa_dron
    aceleracion_z = fuerza_neta_z / masa_dron

    potencia_instantanea = (fuerza_motor_x * velocidad_x) + (fuerza_motor_y * velocidad_y) + (fuerza_motor_z * velocidad_z)
    energia_consumida_motor += potencia_instantanea * paso_de_tiempo

    velocidad_x += aceleracion_x * paso_de_tiempo
    velocidad_y += aceleracion_y * paso_de_tiempo
    velocidad_z += aceleracion_z * paso_de_tiempo

    posicion_x += velocidad_x * paso_de_tiempo
    posicion_y += velocidad_y * paso_de_tiempo
    posicion_z += velocidad_z * paso_de_tiempo

    tiempo_actual += paso_de_tiempo

    historial_tiempo.append(tiempo_actual)
    historial_x.append(posicion_x)
    historial_y.append(posicion_y)
    historial_z.append(posicion_z)
    historial_velocidad_x.append(velocidad_x)
    historial_velocidad_y.append(velocidad_y)
    historial_velocidad_z.append(velocidad_z)
    historial_magnitud_velocidad.append(math.sqrt(velocidad_x**2 + velocidad_y**2 + velocidad_z**2))
    historial_potencia_total.append(potencia_instantanea)
    historial_potencia_x.append(fuerza_motor_x * velocidad_x)
    historial_potencia_y.append(fuerza_motor_y * velocidad_y)
    historial_potencia_z.append(fuerza_motor_z * velocidad_z)


promedio_potencia_x = sum(historial_potencia_x) / len(historial_potencia_x)
promedio_potencia_y = sum(historial_potencia_y) / len(historial_potencia_y)
promedio_potencia_z = sum(historial_potencia_z) / len(historial_potencia_z)

print("=" * 60)
print("EJERCICIO 2: Navegación 3D con Viento Cruzado")
print("=" * 60)
print(f"Tiempo de llegada: {tiempo_actual:.3f} s")
print(f"Posición final: ({posicion_x:.1f}, {posicion_y:.1f}, {posicion_z:.1f})")
print(f"Velocidad final: {historial_magnitud_velocidad[-1]:.2f} m/s")
print(f"Energía consumida: {energia_consumida_motor:.1f} J")
print("\nAnálisis del viento:")
print(f"Potencia media eje X: {promedio_potencia_x:.1f} W (menor por viento a favor)")
print(f"Potencia media eje Y: {promedio_potencia_y:.1f} W (mayor por viento en contra)")
print(f"Potencia media eje Z: {promedio_potencia_z:.1f} W (sin viento, solo gravedad)")

fig = plt.figure(figsize=(10, 8))
ax3d = fig.add_subplot(111, projection='3d')
ax3d.plot(historial_x, historial_y, historial_z, 'b-', linewidth=1.5, label='Trayectoria')
ax3d.scatter(0, 0, 0, color='green', s=100, label='Inicio A')
ax3d.scatter(destino_x, destino_y, destino_z, color='red', s=100, label='Destino B')
ax3d.set_xlabel('X [m]')
ax3d.set_ylabel('Y [m]')
ax3d.set_zlabel('Z [m]')
ax3d.set_title('Trayectoria 3D con Viento Cruzado', fontsize=14, fontweight='bold')
ax3d.legend()
plt.show()

fig2, ax = plt.subplots(2, 2, figsize=(14, 10))
fig2.suptitle('Análisis de Vuelo 3D', fontsize=16, fontweight='bold')

ax[0,0].plot(historial_tiempo, historial_velocidad_x, label='Velocidad X')
ax[0,0].plot(historial_tiempo, historial_velocidad_y, label='Velocidad Y')
ax[0,0].plot(historial_tiempo, historial_velocidad_z, label='Velocidad Z')
ax[0,0].set_xlabel('Tiempo [s]')
ax[0,0].set_ylabel('Velocidad [m/s]')
ax[0,0].set_title('Componentes de Velocidad')
ax[0,0].grid(True, alpha=0.3)
ax[0,0].legend()

ax[0,1].plot(historial_tiempo, historial_magnitud_velocidad, 'b-')
ax[0,1].set_xlabel('Tiempo [s]')
ax[0,1].set_ylabel('|v| [m/s]')
ax[0,1].set_title('Magnitud de Velocidad')
ax[0,1].grid(True, alpha=0.3)

ax[1,0].plot(historial_tiempo, historial_potencia_total, 'r-')
ax[1,0].axhline(potencia_maxima_motor, color='k', ls='--', alpha=0.5)
ax[1,0].set_xlabel('Tiempo [s]')
ax[1,0].set_ylabel('Potencia [W]')
ax[1,0].set_title('Potencia Instantánea')
ax[1,0].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()