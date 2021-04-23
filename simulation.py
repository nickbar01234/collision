from particle import * 
from system import * 

import numpy as np 
import pprint
import pandas as pd
import matplotlib.pyplot as plt 
from matplotlib import animation 
import itertools 

class Simulation:
    def __init__(self, output: str, mode: str, particles: list, n_particles: int, 
                 length: int, width: int, max_vx: int, max_vy: int, 
                 max_t: int, delta_t: float, system_info: dict):
        
        self.output = output 

        assert mode in ["1D", "2D"], "Simluation must be 1D or 2D"
        self.mode = mode
        
        assert (length and width) >= 0, "Grid cannot have negative value"
        self.length = length
        self.width = width

        assert delta_t >= 0, "Time step cannot be zero or negative"
        self.time = 0
        self.max_t = max_t
        self.delta_t = delta_t 

        self.particles = particles
        if len(self.particles) == 0:
            self.__init_particles(n_particles, max_vx, max_vy)
        else:
            for i in range(len(particles)):
                particles[i].id = i 

        self.system = System(self.particles, **system_info)

    def __repr__(self):
        return f"Configuration\nMode: {self.mode}, Length: {self.length}, " + \
            f"Width: {self.width}, \n{self.particles}" 

    def __debug(self):
        info = " ".join([str(particle) for particle in self.particles])
        print(info)

    def __init_particles(self, n_particles: int, max_vx: int, max_vy: int):

        '''
        * If not reading from file, then randomly generate a simulation of 
        n particles. 
        * NOTE: 
            - For random initialization, mass, length, and width are set to 1. 
        '''
        np.random.seed(1)

        print("Begin random initialization")

        mass = 1 #kg 
        length = 1; width = 1 #m

        xpos = [pos for pos in range(self.length)]
        ypos = [pos for pos in range(self.width)]
        vx = [v for v in range(-1 * max_vx, max_vx + 1) if v != 0]
        vy = [v for v in range(-1 * max_vy, max_vy + 1) if v != 0]

        for index, i in enumerate(range(n_particles)):
            x = int(np.random.choice(xpos))
            v_x = int(np.random.choice(vx))
            xpos.pop(xpos.index(x)) #Remove xposition so there won't be overlaps 

            y = 0
            v_y = 0
            if self.mode == "2D":
                y = np.random.choice(ypos)
                v_y = np.random.choice(vy)
                ypos.pop(ypos.index(y)) #Remove yposition so there won't be overlaps  

            particle = Particle(length, width, mass, x, y, v_x, v_y, index)
            self.particles.append(particle)
        
        print(self.__repr__())
        print("Finish random initialization")

    def __init_animation(self):
        '''
        * Initialize the initial frame for animation. 
        '''
        position = []

        for particle in self.particles:
            position.append(particle.draw(self.ax))
        
        return position 

    def __animate(self, frame: int):
        '''
        * Compute new position and velocity for every particle by a time step 
        delta_t
        '''
        if self.time >= self.max_t:
            print("Program is out of time, terminating.")
            if self.output != "":
                df = self.__get_output()
                df.to_csv(self.output + ".csv", index = False)
            exit(0)

        for index, particle in enumerate(self.particles):
            self.particles[index] = self.system(self.delta_t, particle)
        
        self.time += self.delta_t 
        
        self.__collision()
        return self.__init_animation()
    
    def __collision(self):
        '''
        * Apply momentum of conservation if particles collided with walls or 
        each other.
        ''' 

        for index, particle in enumerate(self.particles):
            self.particles[index] = self.system.wall(
                particle, self.length, self.width 
            )
        
        for i, j in itertools.combinations(range(len(self.particles)), 2):
            if self.particles[i].overlap(self.particles[j]):
                self.particles[i], self.particles[j] = self.system.momentum(
                    self.particles[i], self.particles[j]
                )
        
    def animation(self):
        '''
        * Add animations to object. The computation is done from function call 
        to __animate().
        '''

        fig, self.ax = plt.subplots()
        for spine in ["top", "bottom", "left", "right"]:
            self.ax.spines[spine].set_linewidth(2)
        self.ax.set_aspect("equal", "box")
        self.ax.set_xlim(0, self.length)
        self.ax.set_ylim(0, self.width)
        self.ax.xaxis.set_ticks([])
        self.ax.yaxis.set_ticks([])

        try:
            self.animate = animation.FuncAnimation(
                fig, self.__animate, init_func = self.__init_animation, 
                frames = 1600, interval = 1, blit = True
            )
            plt.show()
        except Exception as e:
            exit(0)
        
    def __get_output(self):
        '''
        * Get the position and velocity of each particle.
        * NOTE: A dummy padding is applied if there is a length mismatch between 
                columns.
        '''
        data = {}

        for particle in self.particles:
            data[str(particle.id) + "_x"] = particle.x
            data[str(particle.id) + "_vx"] = particle.vx 
        
        max_length = 0        
        for key in data.keys():
            max_length = len(data[key]) if len(data[key]) > max_length else max_length 
        
        for key in data.keys():
            if len(data[key]) < max_length:
                pad = [None for i in range(max_length - len(data[key]))]
                data[key].extend(pad)

        return pd.DataFrame(data)

if __name__ == "__main__":
    #Sample simulation info 
    simulation_info = {
        "output": "output",
        "mode": "1D",
        "particles": [],
        "n_particles": 4,
        "length": 30, 
        "width": 10,
        "max_vx": 5, 
        "max_vy": 5,
        "max_t": 10,
        "delta_t": 1e-2
    }

    #Sample sytstem info 
    system_info = {
        "system_type": "elastic",
        "kinetic_friction": 0.0,
        "computational_method": "midpoint"
    }
    simulation = Simulation(**simulation_info, system_info = system_info)
    simulation.animation()

            
            