from manim import *
import numpy as np
from objects import *
from motions import *
from utilities import *

class Fission(Scene):
    def construct(self):
        duration = 30

        rows = 3
        cols = 10
        uranium_spacing = .6

        uranium = create_uranium_grid(rows, cols, uranium_spacing)
        
        velocity = 0.02
        initial_angle = 0
        initial_position = np.array([-6, 0, 0])
        neutron_spacing = .6
        number_of_initial_neutrons = 1

        neutrons = [create_neutron(initial_position - np.array([0,neutron_spacing*i,0]), initial_angle, velocity) for i in range(number_of_initial_neutrons)]


        group_size = 2
        number_of_cr = (cols - 2) // group_size
        #number_of_cr = 0
        cr_vel = 0.005
        off_set = 0.001
        control_rod_velocity = [cr_vel + (i*off_set) for i in range(number_of_cr)]
        direction = -PI / 2

        cr_pos = get_control_rod_positions(uranium, cols, rows, uranium_spacing, group_size, number_of_cr)
        control_rods = [create_control_rod(rows, uranium_spacing, cr_pos[i], control_rod_velocity, i) for i in range(number_of_cr)]
        

        self.add(*control_rods)
        self.add(uranium)
        self.add(*neutrons)

        # neutron_count_text = Text(f"Fucking Neutrons: {len(neutrons)}").to_edge(LEFT+UP).scale(.5)
        # self.add(neutron_count_text)

        #nuclear_formula = MathTex(r"^{235}_{92}\text{U} + ^1_0\text{n} \longrightarrow \text{other shit} + 3\ ^1_0\text{n}").to_edge(DOWN)
        #self.play(Write(nuclear_formula))
        
        dt = 0.01      
        n = 0

        while n < duration:
            n += 1
            
            move_control_rod(control_rods, direction, dt)

            move_neutrons(neutrons, dt)
            self.wait(0.017)

            #neutron_count_text.become(Text(f"Fucking Neutrons: {len(neutrons)}").to_edge(LEFT+UP)).scale(.5)

            for uranium_dot in uranium:
                for neutron in neutrons:

                    for control_rod in control_rods:
                        if check_collision_cr(neutron, control_rod):
                            self.remove(neutron)
                            neutrons.remove(neutron)
                            break


                    if uranium_collision_detector(uranium_dot, neutron) == True:

                        neutron.set_color(GRAY)
                        uranium_dot.set_color(GRAY)
                        self.remove(neutron)
                        neutrons.remove(neutron)
                        angles = [np.random.uniform(-PI, PI) for _ in range(3)]
                        #angles = [-PI/4, 0, PI/4]

                        new_neutrons = [create_neutron(uranium_dot.get_center(), angle, velocity) for angle in angles]
                        neutrons.extend(new_neutrons)
                        self.add(*new_neutrons)
                        
                        break

            move_neutrons(neutrons, dt)

        
# with tempconfig({"quality": "low_quality", "disable_caching": True}):
#     scene = Fission()
#     scene.render()