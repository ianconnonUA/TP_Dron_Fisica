masa_dron = 15.0
altura_objetivo = 100.0
coeficiente_resistencia = 0.1
potencia_maxima = 2500.0
energia_disponible_maxima = 25000.0
gravedad = 9.81

fuerza_estatica_maxima = 400.0

paso_de_tiempo = 0.01
tiempo_actual = 0.0
posicion_y = 0.0
velocidad_y = 0.0
energia_consumida = 0.0

historial_tiempo = [0.0]
historial_altura = [0.0]
historial_energia = [0.0]

while posicion_y < altura_objetivo:

    if velocidad_y == 0:
        fuerza_motor = fuerza_estatica_maxima
    else:
        fuerza_ideal_por_potencia = potencia_maxima / velocidad_y
        fuerza_motor = min(fuerza_ideal_por_potencia, fuerza_estatica_maxima)

    fuerza_peso = masa_dron * gravedad
    fuerza_resistencia_aire = coeficiente_resistencia * (velocidad_y ** 2)

    fuerza_neta = fuerza_motor - fuerza_peso - fuerza_resistencia_aire
    aceleracion =  fuerza_neta / masa_dron
    
    velocidad_y = velocidad_y + (aceleracion * paso_de_tiempo)
    posicion_y = posicion_y + (velocidad_y * paso_de_tiempo)

    energia_consumida += fuerza_motor * velocidad_y * paso_de_tiempo

    historial_tiempo.append(tiempo_actual)
    historial_altura.append(posicion_y)
    historial_energia.append(energia_consumida)

    tiempo_actual += paso_de_tiempo

print(f"Tiempo minimo de ascenso: {tiempo_actual:.2f} s")
print(f"Energia consumida: {energia_consumida:.2f} J")

if energia_consumida <= energia_disponible_maxima:
    print("El dron cumple con la restriccion de energia")
else:
    print("El dron no cumple con la restriccion de energia")
