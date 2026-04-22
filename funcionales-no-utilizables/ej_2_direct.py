import numpy as np
import matplotlib.pyplot as plt
import os

def ejercicio_2():
    print("=" * 60)
    print("EJERCICIO 2: Navegacion 3D con Viento Cruzado")
    print("=" * 60)

    m = 15.0;  k = 0.15;  P_max = 3000.0;  dt = 0.001; g = 9.81
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

        v_rel = v - vw
        v_rel_mag = np.linalg.norm(v_rel)
        F_fric = -k * v_rel_mag * v_rel

        v_deseada = d_hat * 15.0
        error_v = v_deseada - v
        error_v_mag = np.linalg.norm(error_v)
        
        if error_v_mag < 0.001:
            dir_motor = d_hat
        else:
            dir_motor = error_v / error_v_mag

        v_mag = np.linalg.norm(v)
        F_mag = P_max / max(v_mag, 0.01)
        F_motor = F_mag * dir_motor

        F_grav = np.array([0, 0, -m*g])

        a = (F_motor + F_grav + F_fric) / m
        P_inst = np.dot(F_motor, v)
        E_mot += P_inst * dt

        v = v + a * dt
        r = r + v * dt
        t += dt

        ts.append(t); rs.append(r.copy()); vs_mag.append(v_mag)
        Ps.append(P_inst); dist_list.append(dist); Es.append(E_mot)
        vx_l.append(v[0]); vy_l.append(v[1]); vz_l.append(v[2])
        
        Px_list.append(F_motor[0]*v[0])
        Py_list.append(F_motor[1]*v[1])
        Pz_list.append(F_motor[2]*v[2])

    rs = np.array(rs)
    print(f"  Tiempo de llegada: {t:.3f} s")
    print(f"  Posicion final: ({r[0]:.1f}, {r[1]:.1f}, {r[2]:.1f})")
    print(f"  Velocidad final: {np.linalg.norm(v):.2f} m/s")
    print(f"  Energia consumida: {E_mot:.1f} J")

    print(f"\n  Analisis del viento:")
    print(f"  Viento eje X = +5 m/s (a favor, dron va hacia x=80)")
    print(f"  Viento eje Y = -2 m/s (en contra, dron va hacia y=50)")
    print(f"  Potencia media eje X: {np.mean(Px_list):.1f} W (menor por viento a favor)")
    print(f"  Potencia media eje Y: {np.mean(Py_list):.1f} W (mayor por viento en contra)")
    print(f"  Potencia media eje Z: {np.mean(Pz_list):.1f} W (sin viento, solo gravedad)")

    fig = plt.figure(figsize=(10, 8))
    ax3d = fig.add_subplot(111, projection='3d')
    ax3d.plot(rs[:,0], rs[:,1], rs[:,2], 'b-', linewidth=1.5, label='Trayectoria')
    ax3d.scatter(*A, color='green', s=100, label='Inicio A')
    ax3d.scatter(*B, color='red', s=100, label='Destino B')
    ax3d.set(xlabel='X [m]', ylabel='Y [m]', zlabel='Z [m]')
    ax3d.set_title('Ejercicio 2: Trayectoria 3D con Viento', fontsize=14, fontweight='bold')
    ax3d.legend()
    plt.show()

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
    plt.show()

ejercicio_2()