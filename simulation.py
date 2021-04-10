from particle import * 
from system import * 

import numpy as np 
import pprint

#Sample simulation info 
simulation_info = {
    "mode": "1D",
    "particles": [],
    "n_particles": 2,
    "length": 10, 
    "width": 0,
    "max_vx": 2, 
    "max_vy": 0
}

class Simulation:
    def __init__(self, mode: str, particles: list, n_particles: int, 
                 length: int, width: int, max_vx: int, max_vy: int):
        '''
        * Parameters:
            - simulation_info: Contains information of the simulation.
            - system_info: Contains information of the system.
        '''

        assert mode in ["1D", "2D"], "Simluation must be 1D or 2D"
        self.mode = mode
        
        assert (length and width) >= 0, "Grid cannot have negative value"
        self.length = length
        self.width = width

        self.particles = particles
        if len(self.particles) == 0:
            self.__init_particles(n_particles, max_vx, max_vy)
    
    def __repr__(self):
        return f"Configuration\nMode: {self.mode}, Length: {self.length}, " + \
            f"Width: {self.width}, \n{self.particles}" 

    def __init_particles(self, n_particles: int, max_vx: int, max_vy: int):
        '''
        * If not reading from file, then randomly generate a simulation of 
        n particles. 
        * NOTE: 
            - For random initialization, mass, length, and width are set to 1. 
        '''
        np.random.seed(42)

        print("Begin random initialization")

        mass = 1 #kg 
        length = 1; width = 1 #m

        xpos = [pos for pos in range(self.length)]
        ypos = [pos for pos in range(self.width)]
        vx = [v for v in range(-1 * max_vx, max_vx + 1) if v != 0]
        vy = [v for v in range(-1 * max_vy, max_vy + 1) if v != 0]

        for i in range(n_particles):
            x = np.random.choice(xpos)
            v_x = np.random.choice(vx)
            xpos.pop(xpos.index(x)) #Remove xposition so there won't be overlaps 

            y = 0
            v_y = 0
            if self.mode == "2D":
                y = np.random.choice(ypos)
                v_y = np.random.choice(vy)
                ypos.pop(ypos.index(y)) #Remove yposition so there won't be overlaps  

            particle = Particle(length, width, mass, x, y, v_x, v_y)
            self.particles.append(particle)
        
        print(self.__repr__())
        print("Finish random initialization")

if __name__ == "__main__":
    simulation = Simulation(**simulation_info)

            
            