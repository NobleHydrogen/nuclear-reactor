from manim import *
import numpy as np
from objects import *
from motions import *
from utilities import *

class Fission(Scene):
    def construct(self):
        duration = 1200

        #URANIUM
        rows = 9
        cols = 16
        uranium_spacing = .5

        uranium = create_uranium_grid(rows, cols, uranium_spacing)
        
        #NEUTRON
        velocity = 0.01
        initial_angle = 0
        initial_position = np.array([-6, 0, 0])
        neutron_spacing = 1
        number_of_initial_neutrons = 2

        neutrons = [create_neutron(initial_position + np.array([neutron_spacing*i,0,0]), initial_angle, velocity, flag = 0) for i in range(number_of_initial_neutrons)]

        #MODERATOR
        group_size = 4
        number_of_mod = cols // group_size + 1
        mod_init_pos = 0
        mod_pos = get_moderator_positions(uranium, cols, mod_init_pos, uranium_spacing, group_size, number_of_mod)
        moderators = [create_moderator(rows, uranium_spacing, mod_pos[i]) for i in range(number_of_mod)]

        #CONTROL ROD
        
        number_of_cr = cols // group_size
        #number_of_cr = 0
        cr_vel = 0.005
        off_set = 0.001
        control_rod_velocity = [cr_vel + (i*off_set) for i in range(number_of_cr)]
        direction = -PI / 2
        cr_init_pos = rows / 2 + 2

        cr_pos = get_control_rod_positions(mod_pos, number_of_cr , uranium_spacing, group_size, cr_init_pos)
        control_rods = [create_control_rod(rows, uranium_spacing, cr_pos[i], control_rod_velocity, i) for i in range(number_of_cr)]
        
        

        self.add(*moderators)
        self.add(*control_rods)
        self.add(uranium)
        self.add(*neutrons)

        #neutron_count_text = Text(f"Fucking Neutrons: {len(neutrons)}").to_edge(LEFT+UP).scale(.5)
        #self.add(neutron_count_text)

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

            
            for neutron in neutrons:
                if check_border(neutron):
                    self.remove(neutron)
                    neutrons.remove(neutron)

                for control_rod in control_rods:
                    if check_collision_cr(neutron, control_rod):
                        self.remove(neutron)
                        neutrons.remove(neutron)
                        break
                
                for moderator in moderators:
                    if check_moderator_collision(neutron, moderator):
                        neutron = reflection(neutron)
                        break

                for uranium_dot in uranium:
                    # if uranium_dot.get_color() == GRAY:
                    #     coin = np.random.randint(1,rows*cols)
                    #     if coin == 3:
                    #         angle = np.random.uniform(-PI, PI)
                    #         spontaneous = create_neutron(uranium_dot.get_center(), angle, velocity)
                    #         neutrons.extend(spontaneous)
                    #         self.add(spontaneous)
                    
                    if uranium_collision_detector(uranium_dot, neutron) == True:

                        neutron.set_color(GRAY)
                        uranium_dot.set_color(GRAY)
                        self.remove(neutron)
                        neutrons.remove(neutron)
                        angles = [np.random.uniform(-PI, PI) for _ in range(3)]
                        #angles = [-PI/4, 0, PI/4]

                        new_neutrons = [create_neutron(uranium_dot.get_center(), angle, velocity, flag = 1) for angle in angles]
                        neutrons.extend(new_neutrons)
                        self.add(*new_neutrons)
                        
                        break

            move_neutrons(neutrons, dt)

        
# with tempconfig({"quality": "low_quality", "disable_caching": True}):
#     scene = Fission()
#     scene.render()