from manim import *
import numpy as np


def move_neutrons(neutrons, dt):
    for neutron in neutrons:
        angle = neutron.angle
        velocity = neutron.velocity
        current_position = neutron.get_center()
        prev_position = current_position - np.array([velocity * np.cos(angle), velocity * np.sin(angle), 0])
        new_position = get_new_position(current_position, prev_position, dt)
        neutron.move_to(new_position)


def get_new_position(current_position, prev_position, dt):
    acceleration = np.array([0, 0, 0])
    return 2 * current_position - prev_position + acceleration * dt**2


def move_control_rod(control_rods, direction, dt):
    for control_rod in control_rods:
        if control_rod.get_center()[1] > 0:
            velocity = control_rod.velocity
            current_position = control_rod.get_center()
            prev_position = current_position - np.array([velocity * np.cos(direction), velocity * np.sin(direction), 0])
            new_position = get_new_position(current_position, prev_position, dt)
            control_rod.move_to(new_position)