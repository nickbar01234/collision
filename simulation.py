from particle import * 
from system import * 

import numpy as np 

#Sample system info 
system_info = {
    "mode": "1D",
    "particles": [],
    "n_particles": 2,
    "length": 10, 
    "width": 0,
    "max_vx": 2, 
    "max_vy": 0
}

class Simulation:
    def __init__(self, simulation_info: dict, system_info: dict):
        '''
        * Parameters:
            - simulation_info: Contains information of the simulation.
            - system_info: Contains information of the system.
        '''

        assert simulation_info["mode"] in ["1D", "2D"], "Simluation must be 1D or 2D"
        self.mode = simulation_info["mode"]
        
        assert (simulation_info["length"] and simulation_info["width"]) > 0, \
        "Grid cannot have negative value"
        self.length = simulation_info["length"]
        self.width = simulation_info["width"]

        self.particles = [] 
        if len(simulation_info["particles"]) == 0:
            self.__init_particles(
               simluation_info["n_particles"], simulation_info["max_vx"], 
               simulation_info["max_vy"]
            )
        else: 
            self.particles = simulation_info["particles"]
    
    def __init_particles(self, n_particles: int, max_vx: int, max_vy: int):
        '''
        * If not reading from file, then randomly generate a simulation of 
        n particles. 
        * NOTE: 
            - For random initialization, mass, length, and width are set to 1. 
        '''

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
        
        print("Finish random initialization")

        

            

            