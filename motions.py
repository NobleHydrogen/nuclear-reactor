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
    count = 0
    for control_rod in control_rods:
        velocity = control_rod.velocity
        if control_rod.get_center()[1] > 1:
            current_position = control_rod.get_center()
            prev_position = current_position - np.array([velocity * np.cos(direction), velocity * np.sin(direction), 0])
            new_position = get_new_position(current_position, prev_position, dt)
            control_rod.move_to(new_position)


def reflection(neutron):
    if neutron.angle > 0:
        neutron.angle -= 2 * (PI/2 + neutron.angle)
    else:
        neutron.angle += 2 * (PI/2 -neutron.angle)
    neutron.velocity /= 2
    neutron.set_color(WHITE)
    return neutron
