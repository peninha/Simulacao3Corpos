import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constantes
G = 6.67430e-11  # Constante gravitacional em m^3 kg^-1 s^-2

# Definição das propriedades dos corpos
class Body:
    def __init__(self, mass, position, velocity):
        self.mass = mass
        self.position = np.array(position, dtype='float64')
        self.velocity = np.array(velocity, dtype='float64')
        self.acceleration = np.zeros(2)
        self.trail = [[], []]  # Para armazenar a trajetória

def compute_gravitational_force(body1, body2):
    distance_vector = body2.position - body1.position
    distance = np.linalg.norm(distance_vector)
    if distance == 0:
        return np.zeros(2)
    force_magnitude = G * body1.mass * body2.mass / distance**2
    force_vector = force_magnitude * distance_vector / distance
    return force_vector

def update_bodies(bodies, dt, trail_length):
    forces = [np.zeros(2) for _ in bodies]

    for i, body1 in enumerate(bodies):
        for j, body2 in enumerate(bodies):
            if i != j:
                force = compute_gravitational_force(body1, body2)
                forces[i] += force

    for i, body in enumerate(bodies):
        body.acceleration = forces[i] / body.mass
        body.velocity += body.acceleration * dt
        body.position += body.velocity * dt

    # Calcular o centro de massa após atualizar as posições
    center_of_mass = compute_center_of_mass(bodies)
    
    for body in bodies:
        relative_position = body.position - center_of_mass
        body.trail[0].append(relative_position[0])
        body.trail[1].append(relative_position[1])
        
        # Limitar o tamanho das trilhas
        if len(body.trail[0]) > trail_length:
            body.trail[0].pop(0)
            body.trail[1].pop(0)

def compute_center_of_mass(bodies):
    total_mass = sum(body.mass for body in bodies)
    center_of_mass = sum(body.mass * body.position for body in bodies) / total_mass
    return center_of_mass

# Inicialização dos corpos
body1 = Body(5.972e24, [0, 0], [0, 0])
body2 = Body(7.348e22, [384400000, 0], [0, 1022])
body3 = Body(7.348e22, [144400000, 0], [0, 2022])  # Novo corpo adicionado

bodies = [
    Body(5.972e24, [0, 0], [0, 0]),
    Body(7.348e22, [384400000, 0], [0, 1032]),
    Body(7.348e22, [144400000, 0], [0, 2000]),
    Body(3.348e22, [0, 84400000], [-1502, 0]),
]

# Parâmetros de simulação
dt = 100  # Intervalo de tempo em segundos
steps_per_frame = 100  # Número de passos de simulação por quadro
total_time = 10000000  # Tempo total de simulação em segundos
animation_interval = 30  # Intervalo em milissegundos na animacao
trail_length = 4000  # Comprimento máximo da trilha

# Configuração da animação
fig, ax = plt.subplots()
ax.set_xlim(-5e8, 5e8)
ax.set_ylim(-5e8, 5e8)
lines = [ax.plot([], [], 'o')[0] for _ in bodies]
trails = [ax.plot([], [], '-', alpha=0.5)[0] for _ in bodies]

def init():
    for line, trail in zip(lines, trails):
        line.set_data([], [])
        trail.set_data([], [])
    return lines + trails

def update(frame):
    for _ in range(steps_per_frame):
        update_bodies(bodies, dt, trail_length)
    center_of_mass = compute_center_of_mass(bodies)
    for line, body, trail in zip(lines, bodies, trails):
        relative_position = body.position - center_of_mass
        line.set_data([relative_position[0]], [relative_position[1]])
        trail.set_data(body.trail[0], body.trail[1])
    return lines + trails

ani = FuncAnimation(fig, update, frames=int(total_time / dt), init_func=init, blit=True, interval=animation_interval)
plt.show()
