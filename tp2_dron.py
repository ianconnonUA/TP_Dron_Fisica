"""
TP2 - Trabajo, Energia y Potencia en Sistemas Dinamicos
Simulacion de dron de transporte de insumos medicos
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

OUT = os.path.dirname(os.path.abspath(__file__))
g = 9.81

# ============================================================
# EJERCICIO 1: Ascenso Vertical y Gestion de Energia
# ============================================================
def ejercicio_1():
    print("=" * 60)
    print("EJERCICIO 1: Ascenso Vertical y Gestion de Energia")
    print("=" * 60)

    m = 15.0;  H = 100.0;  k = 0.1
    P_max = 2500.0;  E_max = 25000.0;  dt = 0.001

    t, y, v, W_motor, W_fric = 0.0, 0.0, 0.0, 0.0, 0.0
    ts, ys, vs, Ps, Es, Fms, Fds = [0],[0],[0],[0],[0],[0],[0]
    W_fric_list = [0]

    # Para minimo tiempo: maxima fuerza posible en cada instante
    # Sin limite de empuje estatico, usamos P_max/v con cap razonable
    F_cap = 500.0  # Cap de fuerza a baja velocidad [N] (valor tipico de motor de dron)

    while y < H and t < 100:
        F_drag = k * v**2
        # Fuerza del motor: limitada por potencia y por cap fisico
        if v < 1e-6:
            F_motor = F_cap
        else:
            F_motor = min(F_cap, P_max / v)
        
        # Aceleracion (2da Ley de Newton)
        a = (F_motor - m*g - F_drag) / m
        
        # Euler semi-implicito: actualizar v primero
        v_old = v
        v = max(v + a*dt, 0.0)
        
        # Trabajo incremental con velocidad promedio del paso
        v_avg = 0.5*(v_old + v)
        W_motor += F_motor * v_avg * dt
        W_fric += (-F_drag) * v_avg * dt
        P_inst = F_motor * v_avg
        
        y += v * dt  # usar v nueva (semi-implicito)
        t += dt
        ts.append(t); ys.append(y); vs.append(v)
        Ps.append(min(P_inst, P_max)); Es.append(W_motor)
        Fms.append(F_motor); Fds.append(F_drag)
        W_fric_list.append(W_fric)

    # Resultados
    Ek = 0.5*m*v**2;  Ep = m*g*y
    print(f"  Tiempo minimo de ascenso: {t:.3f} s")
    print(f"  Velocidad final: {v:.3f} m/s")
    print(f"  Energia consumida: {W_motor:.1f} / {E_max} J")
    print(f"  Balance Energetico:")
    print(f"    dK = {Ek:.1f} J")
    print(f"    dU = {Ep:.1f} J")
    print(f"    dK + dU = {Ek+Ep:.1f} J")
    print(f"    W_motor = {W_motor:.1f} J")
    print(f"    W_friccion = {W_fric:.1f} J")
    print(f"    W_motor + W_fric = {W_motor+W_fric:.1f} J")
    print(f"    Error balance: {abs((Ek+Ep) - (W_motor+W_fric)):.2f} J")
    if W_motor <= E_max:
        print(f"  CUMPLE restriccion de energia")
    else:
        print(f"  NO CUMPLE restriccion de energia")

    # Graficos
    fig, ax = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Ejercicio 1: Ascenso Vertical', fontsize=16, fontweight='bold')
    ax[0,0].plot(ts, ys, 'b-'); ax[0,0].axhline(H, color='r', ls='--', alpha=.5)
    ax[0,0].set(xlabel='Tiempo [s]', ylabel='Altura [m]', title='Posicion vs Tiempo'); ax[0,0].grid(True,alpha=.3)
    ax[0,1].plot(ts, vs, 'g-')
    ax[0,1].set(xlabel='Tiempo [s]', ylabel='Velocidad [m/s]', title='Velocidad vs Tiempo'); ax[0,1].grid(True,alpha=.3)
    ax[1,0].plot(ts, Ps, 'r-'); ax[1,0].axhline(P_max, color='k', ls='--', alpha=.5, label=f'Pmax={P_max}W')
    ax[1,0].set(xlabel='Tiempo [s]', ylabel='Potencia [W]', title='Potencia vs Tiempo'); ax[1,0].grid(True,alpha=.3); ax[1,0].legend()
    ax[1,1].plot(ts, Es, 'm-'); ax[1,1].axhline(E_max, color='r', ls='--', alpha=.5, label=f'Emax={E_max}J')
    ax[1,1].set(xlabel='Tiempo [s]', ylabel='Energia [J]', title='Energia Acumulada'); ax[1,1].grid(True,alpha=.3); ax[1,1].legend()
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, 'ej1_ascenso_vertical.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("  Grafico guardado: ej1_ascenso_vertical.png\n")

# ============================================================
# EJERCICIO 2: Navegacion 3D con Viento Cruzado
# ============================================================
def ejercicio_2():
    print("=" * 60)
    print("EJERCICIO 2: Navegacion 3D con Viento Cruzado")
    print("=" * 60)

    m = 15.0;  k = 0.15;  P_max = 3000.0;  dt = 0.001
    A = np.array([0.0, 0.0, 0.0])
    B = np.array([80.0, 50.0, 60.0])
    vw = np.array([5.0, -2.0, 0.0])

    r = A.copy();  v = np.zeros(3);  t = 0.0
    ts, rs, vs_mag, Ps, dist_list = [0],[r.copy()],[0],[0],[np.linalg.norm(B-A)]
    Px_list, Py_list, Pz_list = [0],[0],[0]
    vx_l, vy_l, vz_l = [0],[0],[0]
    E_mot = 0.0; Es = [0]

    while t < 30:
        d = B - r;  dist = np.linalg.norm(d)
        if dist < 1.0:
            break
        d_hat = d / dist

        # Velocidad relativa y friccion
        v_rel = v - vw
        v_rel_mag = np.linalg.norm(v_rel)
        F_fric = -k * v_rel_mag * v_rel

        # Fuerza del motor: direccion hacia B, magnitud max por potencia
        v_mag = np.linalg.norm(v)
        F_mag = P_max / max(v_mag, 0.01)
        F_motor = F_mag * d_hat

        # Gravedad
        F_grav = np.array([0, 0, -m*g])

        # Aceleracion
        a = (F_motor + F_grav + F_fric) / m
        P_inst = np.dot(F_motor, v)
        E_mot += P_inst * dt

        v = v + a * dt
        r = r + v * dt
        t += dt

        ts.append(t); rs.append(r.copy()); vs_mag.append(v_mag)
        Ps.append(P_inst); dist_list.append(dist); Es.append(E_mot)
        vx_l.append(v[0]); vy_l.append(v[1]); vz_l.append(v[2])
        # Potencia por eje (F_motor_i * v_i)
        Px_list.append(F_motor[0]*v[0])
        Py_list.append(F_motor[1]*v[1])
        Pz_list.append(F_motor[2]*v[2])

    rs = np.array(rs)
    print(f"  Tiempo de llegada: {t:.3f} s")
    print(f"  Posicion final: ({r[0]:.1f}, {r[1]:.1f}, {r[2]:.1f})")
    print(f"  Velocidad final: {np.linalg.norm(v):.2f} m/s")
    print(f"  Energia consumida: {E_mot:.1f} J")

    # Analisis del viento
    print(f"\n  Analisis del viento:")
    print(f"  Viento eje X = +5 m/s (a favor, dron va hacia x=80)")
    print(f"  Viento eje Y = -2 m/s (en contra, dron va hacia y=50)")
    print(f"  Potencia media eje X: {np.mean(Px_list):.1f} W (menor por viento a favor)")
    print(f"  Potencia media eje Y: {np.mean(Py_list):.1f} W (mayor por viento en contra)")
    print(f"  Potencia media eje Z: {np.mean(Pz_list):.1f} W (sin viento, solo gravedad)")

    # Grafico 1: Trayectoria 3D
    fig = plt.figure(figsize=(10, 8))
    ax3d = fig.add_subplot(111, projection='3d')
    ax3d.plot(rs[:,0], rs[:,1], rs[:,2], 'b-', linewidth=1.5, label='Trayectoria')
    ax3d.scatter(*A, color='green', s=100, label='Inicio A')
    ax3d.scatter(*B, color='red', s=100, label='Destino B')
    ax3d.set(xlabel='X [m]', ylabel='Y [m]', zlabel='Z [m]')
    ax3d.set_title('Ejercicio 2: Trayectoria 3D con Viento', fontsize=14, fontweight='bold')
    ax3d.legend()
    plt.savefig(os.path.join(OUT, 'ej2_trayectoria_3d.png'), dpi=150, bbox_inches='tight')
    plt.close()

    # Grafico 2: Velocidad, Potencia
    fig, ax = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Ejercicio 2: Analisis de Vuelo 3D', fontsize=16, fontweight='bold')
    ax[0,0].plot(ts, vx_l, label='vx'); ax[0,0].plot(ts, vy_l, label='vy'); ax[0,0].plot(ts, vz_l, label='vz')
    ax[0,0].set(xlabel='Tiempo [s]', ylabel='Velocidad [m/s]', title='Componentes de Velocidad'); ax[0,0].grid(True,alpha=.3); ax[0,0].legend()
    ax[0,1].plot(ts, vs_mag, 'b-')
    ax[0,1].set(xlabel='Tiempo [s]', ylabel='|v| [m/s]', title='Magnitud de Velocidad'); ax[0,1].grid(True,alpha=.3)
    ax[1,0].plot(ts, Ps, 'r-'); ax[1,0].axhline(P_max, color='k', ls='--', alpha=.5)
    ax[1,0].set(xlabel='Tiempo [s]', ylabel='Potencia [W]', title='Potencia Instantanea'); ax[1,0].grid(True,alpha=.3)
    ax[1,1].plot(ts, Px_list, label='P_x'); ax[1,1].plot(ts, Py_list, label='P_y'); ax[1,1].plot(ts, Pz_list, label='P_z')
    ax[1,1].set(xlabel='Tiempo [s]', ylabel='Potencia [W]', title='Potencia por Componente'); ax[1,1].grid(True,alpha=.3); ax[1,1].legend()
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, 'ej2_analisis_vuelo.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("  Graficos guardados: ej2_trayectoria_3d.png, ej2_analisis_vuelo.png\n")

# ============================================================
# EJERCICIO 3: Restricciones Reales de Motor
# ============================================================
def ejercicio_3():
    print("=" * 60)
    print("EJERCICIO 3: Restricciones Reales de Motor")
    print("=" * 60)

    m = 15.0;  k = 0.15;  P_max = 3000.0;  dt = 0.001
    F_static = 400.0;  t_limit = 20.0;  E_max = 40000.0
    A = np.array([0.0, 0.0, 0.0])
    B = np.array([80.0, 50.0, 60.0])
    vw = np.array([5.0, -2.0, 0.0])
    v_transicion = P_max / F_static  # 7.5 m/s

    r = A.copy();  v = np.zeros(3);  t = 0.0
    E_mot = 0.0;  W_fric_total = 0.0
    ts = [0]; rs = [r.copy()]; vs_mag = [0]; Ps = [0]; Es = [0]
    Fm_list = [0]; Ff_list = [0]; dist_list = [np.linalg.norm(B-A)]

    while t < t_limit:
        d = B - r;  dist = np.linalg.norm(d)
        if dist < 1.0:
            break
        d_hat = d / dist

        # Velocidad relativa y friccion
        v_rel = v - vw
        v_rel_mag = np.linalg.norm(v_rel)
        F_fric_vec = -k * v_rel_mag * v_rel
        F_fric_mag = np.linalg.norm(F_fric_vec)

        # Fuerza del motor con restriccion: F <= min(F_static, P_max/|v|)
        v_mag = np.linalg.norm(v)
        if v_mag < 0.01:
            F_mag = F_static  # limitado por empuje estatico
        else:
            F_mag = min(F_static, P_max / v_mag)
        F_motor_vec = F_mag * d_hat

        F_grav = np.array([0, 0, -m*g])
        a = (F_motor_vec + F_grav + F_fric_vec) / m

        P_inst = np.dot(F_motor_vec, v)
        E_mot += P_inst * dt
        W_fric_total += np.dot(F_fric_vec, v) * dt

        v = v + a * dt
        r = r + v * dt
        t += dt

        ts.append(t); rs.append(r.copy()); vs_mag.append(v_mag)
        Ps.append(P_inst); Es.append(E_mot)
        Fm_list.append(F_mag); Ff_list.append(F_fric_mag)
        dist_list.append(dist)

    rs = np.array(rs)
    v_final = np.linalg.norm(v)
    Ek = 0.5*m*v_final**2
    Ep = m*g*r[2]

    print(f"  Tiempo de llegada: {t:.3f} s")
    print(f"  Posicion final: ({r[0]:.1f}, {r[1]:.1f}, {r[2]:.1f})")
    print(f"  Distancia a B: {np.linalg.norm(B-r):.2f} m")
    print(f"  Velocidad final: {v_final:.2f} m/s")
    print(f"  Vel. transicion torque/potencia: {v_transicion:.1f} m/s")
    print(f"\n  Balance Energetico:")
    print(f"  W_motor = {E_mot:.1f} J")
    print(f"  W_friccion = {W_fric_total:.1f} J")
    print(f"  dK = {Ek:.1f} J")
    print(f"  dU = {Ep:.1f} J")
    print(f"  dK + dU = {Ek+Ep:.1f} J")
    print(f"  W_motor + W_fric = {E_mot+W_fric_total:.1f} J")
    print(f"  Error balance: {abs((Ek+Ep) - (E_mot+W_fric_total)):.2f} J")
    if E_mot <= E_max:
        print(f"  CUMPLE energia ({E_mot:.0f} <= {E_max} J)")
    else:
        print(f"  NO CUMPLE energia ({E_mot:.0f} > {E_max} J)")
    if t <= t_limit:
        print(f"  CUMPLE tiempo ({t:.1f} <= {t_limit} s)")
    else:
        print(f"  NO CUMPLE tiempo ({t:.1f} > {t_limit} s)")

    # Grafico 1: Trayectoria 3D
    fig = plt.figure(figsize=(10, 8))
    ax3d = fig.add_subplot(111, projection='3d')
    ax3d.plot(rs[:,0], rs[:,1], rs[:,2], 'b-', linewidth=1.5, label='Trayectoria')
    ax3d.scatter(*A, color='green', s=100, label='Inicio A')
    ax3d.scatter(*B, color='red', s=100, label='Destino B')
    ax3d.set(xlabel='X [m]', ylabel='Y [m]', zlabel='Z [m]')
    ax3d.set_title('Ejercicio 3: Trayectoria con Restricciones', fontsize=14, fontweight='bold')
    ax3d.legend()
    plt.savefig(os.path.join(OUT, 'ej3_trayectoria_3d.png'), dpi=150, bbox_inches='tight')
    plt.close()

    # Grafico 2: Fuerzas, Potencia, Energia
    fig, ax = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Ejercicio 3: Analisis con Restricciones Reales', fontsize=16, fontweight='bold')

    ax[0,0].plot(ts, Fm_list, 'b-', label='F_motor')
    ax[0,0].plot(ts, Ff_list, 'r-', label='F_friccion')
    ax[0,0].axhline(F_static, color='gray', ls='--', alpha=.5, label=f'F_static={F_static}N')
    ax[0,0].set(xlabel='Tiempo [s]', ylabel='Fuerza [N]', title='F_Motor vs F_Friccion')
    ax[0,0].grid(True,alpha=.3); ax[0,0].legend()
    # Marcar transicion torque -> potencia
    for i in range(1, len(vs_mag)):
        if vs_mag[i] >= v_transicion and vs_mag[i-1] < v_transicion:
            ax[0,0].axvline(ts[i], color='orange', ls=':', label=f'Transicion v={v_transicion}m/s')
            ax[0,0].legend()
            break

    ax[0,1].plot(ts, Ps, 'r-')
    ax[0,1].axhline(P_max, color='k', ls='--', alpha=.5, label=f'Pmax={P_max}W')
    ax[0,1].set(xlabel='Tiempo [s]', ylabel='Potencia [W]', title='Potencia vs Tiempo')
    ax[0,1].grid(True,alpha=.3); ax[0,1].legend()

    ax[1,0].plot(ts, Es, 'm-')
    ax[1,0].axhline(E_max, color='r', ls='--', alpha=.5, label=f'Emax={E_max}J')
    ax[1,0].set(xlabel='Tiempo [s]', ylabel='Energia [J]', title='Energia Acumulada')
    ax[1,0].grid(True,alpha=.3); ax[1,0].legend()

    ax[1,1].plot(ts, vs_mag, 'g-')
    ax[1,1].axhline(v_transicion, color='orange', ls='--', alpha=.5, label=f'v_trans={v_transicion}m/s')
    ax[1,1].set(xlabel='Tiempo [s]', ylabel='|v| [m/s]', title='Velocidad vs Tiempo')
    ax[1,1].grid(True,alpha=.3); ax[1,1].legend()

    plt.tight_layout()
    plt.savefig(os.path.join(OUT, 'ej3_analisis_restricciones.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("  Graficos guardados: ej3_trayectoria_3d.png, ej3_analisis_restricciones.png\n")

# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  TP2: TRABAJO, ENERGIA Y POTENCIA EN SISTEMAS DINAMICOS")
    print("  Simulacion de Dron de Transporte")
    print("=" * 60 + "\n")
    ejercicio_1()
    ejercicio_2()
    ejercicio_3()
    print("Todos los graficos guardados en:", OUT)
