import matplotlib.pyplot as plt

masa_dron = 15.0
altura_objetivo = 100.0
coeficiente_resistencia = 0.1
potencia_maxima = 2500.0
energia_disponible_maxima = 25000.0
paso_de_tiempo = 0.001
gravedad = 9.81

fuerza_estatica_maxima = 670000.0 # Fuerza máxima que puede generar el motor sin pasarse de la energia disponible
# fuerza_estatica_maxima = 400.0

tiempo_actual = 0.0
posicion_y = 0.0
velocidad_y = 0.0
trabajo_acumulado_motor = 0.0
trabajo_acumulado_friccion = 0.0

historial_tiempo = [0.0]
historial_altura = [0.0]
historial_velocidad = [0.0]
historial_potencia = [0.0]
historial_energia_motor = [0.0]
historial_fuerza_motor = [0.0]
historial_fuerza_friccion = [0.0]
historial_energia_friccion = [0.0]

while posicion_y < altura_objetivo and tiempo_actual < 100.0:
    
    fuerza_resistencia_aire = coeficiente_resistencia * (velocidad_y ** 2)
    
    if velocidad_y < 1e-6:
        fuerza_motor = fuerza_estatica_maxima
    else:
        fuerza_motor = min(fuerza_estatica_maxima, potencia_maxima / velocidad_y)
    
    aceleracion = (fuerza_motor - (masa_dron * gravedad) - fuerza_resistencia_aire) / masa_dron
    
    velocidad_anterior = velocidad_y
    velocidad_y = max(velocidad_y + (aceleracion * paso_de_tiempo), 0.0)
    
    velocidad_promedio = 0.5 * (velocidad_anterior + velocidad_y)
    trabajo_acumulado_motor += fuerza_motor * velocidad_promedio * paso_de_tiempo
    trabajo_acumulado_friccion += (-fuerza_resistencia_aire) * velocidad_promedio * paso_de_tiempo
    potencia_instantanea = fuerza_motor * velocidad_promedio
    
    posicion_y += velocidad_y * paso_de_tiempo
    tiempo_actual += paso_de_tiempo
    
    historial_tiempo.append(tiempo_actual)
    historial_altura.append(posicion_y)
    historial_velocidad.append(velocidad_y)
    historial_potencia.append(min(potencia_instantanea, potencia_maxima))
    historial_energia_motor.append(trabajo_acumulado_motor)
    historial_fuerza_motor.append(fuerza_motor)
    historial_fuerza_friccion.append(fuerza_resistencia_aire)
    historial_energia_friccion.append(trabajo_acumulado_friccion)

energia_cinetica = 0.5 * masa_dron * (velocidad_y ** 2)
energia_potencial = masa_dron * gravedad * posicion_y

print(f"  Tiempo mínimo de ascenso: {tiempo_actual:.3f} s")
print(f"  Velocidad final: {velocidad_y:.3f} m/s")
print(f"  Energía consumida: {trabajo_acumulado_motor:.1f} / {energia_disponible_maxima} J")

if trabajo_acumulado_motor <= energia_disponible_maxima:
    print(f"  CUMPLE restricción de energía")
else:
    print(f"  NO CUMPLE restricción de energía")