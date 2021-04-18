from particle import * 
from system import * 

import numpy as np 
import pprint

import matplotlib.pyplot as plt 
from matplotlib import animation 
import itertools 

#Sample simulation info 
simulation_info = {
    "mode": "1D",
    "particles": [],
    "n_particles": 2,
    "length": 10, 
    "width": 10,
    "max_vx": 8, 
    "max_vy": 5,
    "delta_t": 1e-2
}

#Sample sytstem info 
system_info = {
    "system_type": "elastic",
    "kinetic_friction": 0.0,
    "computational_method": "verlet"
}

class Simulation:
    def __init__(self, mode: str, particles: list, n_particles: int, 
                 length: int, width: int, max_vx: int, max_vy: int, 
                 delta_t: float, system_info: dict):
        
        assert mode in ["1D", "2D"], "Simluation must be 1D or 2D"
        self.mode = mode
        
        assert (length and width) >= 0, "Grid cannot have negative value"
        self.length = length
        self.width = width

        assert delta_t >= 0, "Time step cannot be zero or negative"
        self.delta_t = delta_t 
        
        self.particles = particles
        if len(self.particles) == 0:
            self.__init_particles(n_particles, max_vx, max_vy)
        
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

            particle = Particle(index, length, width, mass, x, y, v_x, v_y)
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
        if self.system.ke <= 0.5:
            print("System is out of kinetic energy. Quitting the program")
            exit(0)

        for index, particle in enumerate(self.particles):
            self.particles[index] = self.system(self.delta_t, particle)

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

        self.animate = animation.FuncAnimation(
            fig, self.__animate, init_func = self.__init_animation, 
            frames = 1600, interval = 2, blit = True
        )
        plt.show()
        
        
if __name__ == "__main__":
    simulation = Simulation(**simulation_info, system_info = system_info)
    simulation.animation()

            
            