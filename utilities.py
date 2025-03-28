from manim import *
import numpy as np



def check_collision_cr(neutron, control_rod):
    if np.abs(neutron.get_center()[0] - control_rod.get_center()[0]) < 0.1 and np.abs(neutron.get_center()[1] - control_rod.get_center()[1]) < control_rod.get_height()/2:
        return True
    


def uranium_collision_detector(uranium, neutron):
    if np.linalg.norm(uranium.get_center() - neutron.get_center()) < 0.1 and uranium.get_color() == YELLOW_C:
        return True



def get_control_rod_positions(uranium, cols,initial_y, uranium_spacing, group_size, number_of_cr):
    rod_positions = []

    for i in range(number_of_cr):
        rod_x = uranium.get_center()[0] + group_size*uranium_spacing*(i-cols/2//group_size)
        if (cols // group_size) % 2 != 0:
            rod_x -= uranium_spacing*group_size / 2
        rod_position = np.array([rod_x, initial_y, 0])
        rod_positions.append(rod_position)
    return rod_positions

def get_moderator_positions(control_rod_pos, num_of_mod, uranium_spacing, group_size):
    mod_positions = []

    for i in range(num_of_mod):
        mod_positions.append(control_rod_pos[i] + np.array([uranium_spacing*group_size / 2, 0, 0]))


        # rod_x = uranium.get_center()[0] + group_size*uranium_spacing*(i-cols/2//group_size)
        # if (cols // group_size) % 2 != 0:
        #     rod_x -= uranium_spacing*group_size / 2
        # mod_position = np.array([rod_x, initial_y, 0])
        # mod_positions.append(mod_position)

    return mod_positions