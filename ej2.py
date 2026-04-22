import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

masa_dron = 15.0
coeficiente_arrastre = 0.15
potencia_maxima_motor = 3000.0
fuerza_maxima_arranque = 400.0
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
paso_de_tiempo = 0.01

trabajo_acumulado_motor_x = 0.0
trabajo_acumulado_motor_y = 0.0

historial_x = [posicion_x]
historial_y = [posicion_y]
historial_z = [posicion_z]

while posicion_x < destino_x:
    distancia_faltante_x = destino_x - posicion_x
    distancia_faltante_y = destino_y - posicion_y
    distancia_faltante_z = destino_z - posicion_z

    distancia_total_al_destino = math.sqrt(distancia_faltante_x**2 + distancia_faltante_y**2 + distancia_faltante_z**2)
    
    direccion_x = distancia_faltante_x / distancia_total_al_destino
    direccion_y = distancia_faltante_y / distancia_total_al_destino
    direccion_z = distancia_faltante_z / distancia_total_al_destino

    velocidad_absoluta_total = math.sqrt(velocidad_x**2 + velocidad_y**2 + velocidad_z**2)

    if velocidad_absoluta_total == 0:
        fuerza_arranque_motor = fuerza_maxima_arranque
    else:
        fuerza_ideal = potencia_maxima_motor / velocidad_absoluta_total
        fuerza_arranque_motor = min(fuerza_ideal, fuerza_maxima_arranque)
    
    fuerza_motor_x = fuerza_arranque_motor * direccion_x
    fuerza_motor_y = fuerza_arranque_motor * direccion_y
    fuerza_motor_z = fuerza_arranque_motor * direccion_z
    
    velocidad_relativa_x = velocidad_x - velocidad_viento_x
    velocidad_relativa_y = velocidad_y - velocidad_viento_y
    velocidad_relativa_z = velocidad_z - velocidad_viento_z

    velocidad_relativa_total = math.sqrt(velocidad_relativa_x**2 + velocidad_relativa_y**2 + velocidad_relativa_z**2)

    fuerza_arrastre_x = -coeficiente_arrastre * velocidad_relativa_x * velocidad_relativa_total
    fuerza_arrastre_y = -coeficiente_arrastre * velocidad_relativa_y * velocidad_relativa_total
    fuerza_arrastre_z = -coeficiente_arrastre * velocidad_relativa_z * velocidad_relativa_total

    fuerza_neta_x = fuerza_motor_x + fuerza_arrastre_x
    fuerza_neta_y = fuerza_motor_y + fuerza_arrastre_y
    fuerza_neta_z = fuerza_motor_z + fuerza_arrastre_z - (masa_dron * gravedad)

    aceleracion_x = fuerza_neta_x / masa_dron
    aceleracion_y = fuerza_neta_y / masa_dron
    aceleracion_z = fuerza_neta_z / masa_dron

    velocidad_x += aceleracion_x * paso_de_tiempo
    velocidad_y += aceleracion_y * paso_de_tiempo
    velocidad_z += aceleracion_z * paso_de_tiempo

    posicion_x += velocidad_x * paso_de_tiempo
    posicion_y += velocidad_y * paso_de_tiempo
    posicion_z += velocidad_z * paso_de_tiempo

    distancia_recorrida_x = velocidad_x * paso_de_tiempo
    distancia_recorrida_y = velocidad_y * paso_de_tiempo

    trabajo_acumulado_motor_x += fuerza_motor_x * distancia_recorrida_x
    trabajo_acumulado_motor_y += fuerza_motor_y * distancia_recorrida_y

    tiempo_actual += paso_de_tiempo

    historial_x.append(posicion_x)
    historial_y.append(posicion_y)
    historial_z.append(posicion_z)

print("-" * 40)
print(f"Posición Final: X={posicion_x:.1f}m | Y={posicion_y:.1f}m | Z={posicion_z:.1f}m")
print(f"Tiempo de vuelo: {tiempo_actual:.2f} segundos")
print("-" * 40)
print("ANÁLISIS DE IMPACTO DEL VIENTO (Punto 3):")
print(f"Trabajo realizado por el motor en el Eje X (Viento a favor): {trabajo_acumulado_motor_x:.2f} J")
print(f"Trabajo realizado por el motor en el Eje Y (Viento en contra): {trabajo_acumulado_motor_y:.2f} J")

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

ax.plot(historial_x, historial_y, historial_z, label='Trayectoria del Dron', color='blue')

ax.scatter(0, 0, 0, color='green', s=100, label='Inicio A (0,0,0)')
ax.scatter(80, 50, 60, color='red', s=100, label='Destino B (80,50,60)')

ax.set_xlabel('Eje X (m)')
ax.set_ylabel('Eje Y (m)')
ax.set_zlabel('Eje Z (m)')
ax.set_title('Trayectoria 3D con Viento Cruzado')
ax.legend()

plt.show()