import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Constantes gravitacionais
G = 6.67430e-11  # m^3 kg^-1 s^-2

# Propriedades dos corpos
baleia = {
    'massa': 1000000000,  # kg
    'posicao': np.array([0, 0, 0], dtype=float),  # metros
    'velocidade': np.array([0, 0, 0], dtype=float)  # metros por segundo
}

petunia = {
    'massa': 500000000,  # kg
    'posicao': np.array([100, 0, 0], dtype=float),  # metros
    'velocidade': np.array([0, 1, 0], dtype=float)  # metros por segundo
}

def calc_gravitational_force(body1, body2):
    distance_vec = body2['posicao'] - body1['posicao']
    distance = np.linalg.norm(distance_vec)
    if distance == 0:
        return np.array([0, 0, 0], dtype=float)  # Evita divisão por zero
    force_magnitude = G * body1['massa'] * body2['massa'] / distance**2
    force_direction = distance_vec / distance
    force = force_magnitude * force_direction
    return force

def update_position_and_velocity(body, force, dt):
    acceleration = force / body['massa']
    body['velocidade'] += acceleration * dt
    body['posicao'] += body['velocidade'] * dt

# Parâmetros de simulação
dt = 1000  # passo de tempo em segundos
num_steps = 1000  # número de passos de simulação

# Armazenar posições para visualização
positions_baleia = []
positions_petunia = []

for _ in range(num_steps):
    force_on_baleia = calc_gravitational_force(baleia, petunia)
    force_on_petunia = -force_on_baleia

    update_position_and_velocity(baleia, force_on_baleia, dt)
    update_position_and_velocity(petunia, force_on_petunia, dt)

    positions_baleia.append(baleia['posicao'].copy())
    positions_petunia.append(petunia['posicao'].copy())

positions_baleia = np.array(positions_baleia)
positions_petunia = np.array(positions_petunia)

# Visualizar a simulação em 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-200, 200)
ax.set_ylim(-200, 200)
ax.set_zlim(-200, 200)

line_baleia, = ax.plot([], [], [], 'bo', label='Baleia')
line_petunia, = ax.plot([], [], [], 'ro', label='Petúnia')

def init():
    line_baleia.set_data([], [])
    line_baleia.set_3d_properties([])
    line_petunia.set_data([], [])
    line_petunia.set_3d_properties([])
    return line_baleia, line_petunia

def update(frame):
    line_baleia.set_data([positions_baleia[frame, 0]], [positions_baleia[frame, 1]])
    line_baleia.set_3d_properties([positions_baleia[frame, 2]])
    line_petunia.set_data([positions_petunia[frame, 0]], [positions_petunia[frame, 1]])
    line_petunia.set_3d_properties([positions_petunia[frame, 2]])
    return line_baleia, line_petunia

ani = FuncAnimation(fig, update, frames=num_steps, init_func=init, blit=True, interval=20)
plt.legend()
plt.show()
