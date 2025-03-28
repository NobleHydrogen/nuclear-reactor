from manim import *
import numpy as np

def create_uranium_grid(rows, column, spacing):
    uranium_grid = VGroup(*[
        Dot(radius=0.1, color=YELLOW_C).move_to(np.array([
            (x - (column - 1) / 2) * spacing,
            (y - (rows - 1) / 2) * spacing,
            0
        ]))
        for x in range(column)
        for y in range(rows)
    ])
    
    return uranium_grid


def create_neutron(position, angle, velocity):
    coin = np.random.randint(1,3)
    neutron_color = WHITE
    if coin == 1:
        velocity *= 2
        neutron_color = RED

    neutron = Dot(radius=0.05, color=neutron_color).move_to(position)
    neutron.angle = angle
    neutron.velocity = velocity
    return neutron

def create_control_rod(rows, spacing, position, velocity, index):
    cr = Rectangle(height = rows * spacing, width = 0.01, color = GRAY).move_to(position)
    cr.set_fill(GRAY, 1)

    cr.velocity = velocity[index]
    return cr


def create_moderator(rows, spacing, position):
    mod = Rectangle(height = rows * spacing, width = 0.01, color = WHITE).move_to(position)

    return mod