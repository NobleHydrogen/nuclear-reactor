from manim import *
import numpy as np



def check_collision_cr(neutron, control_rod):
    if np.abs(neutron.get_center()[0] - control_rod.get_center()[0]) < 0.1 and np.abs(neutron.get_center()[1] - control_rod.get_center()[1]) < control_rod.get_height()/2 and neutron.get_color() != RED:
        return True
    


def uranium_collision_detector(uranium, neutron):
    if np.linalg.norm(uranium.get_center() - neutron.get_center()) < 0.1 and uranium.get_color() == YELLOW_C:
        return True



def get_control_rod_positions(uranium, cols, row, uranium_spacing, group_size, number_of_cr):
    rod_positions = []

    for i in range(number_of_cr):

        col_left = (i + 1) * group_size - 1
        col_right = (i + 1) * group_size

        x_left = -((cols - 1) / 2) * uranium_spacing + col_left * uranium_spacing
        x_right = -((cols - 1) / 2) * uranium_spacing + col_right * uranium_spacing

        rod_x = (x_left + x_right) / 2
        rod_position = uranium.get_center() + np.array([rod_x, row/2, 0])
        rod_positions.append(rod_position)

    return rod_positions