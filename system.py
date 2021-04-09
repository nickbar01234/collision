'''
* Object representation of the system. Includes momentum and frictional force. 
'''

from particle import * 

import numpy as np 

class System:
    def __init__(self, particles: list, kinetic_friction: float):
        assert len(particles) > 0, "System must have at least 1 particle"

        self.kinetic_energy = sum([p.ke() for p in particles])
        self.acceleration = kinetic_friction * 9.8 # m/s^2
    
    def __call__(self, delta_t: float, particle: Particle):
        '''
        * Apply kinematic equations on a particle. 
        '''
        particle.vx = particle.vx[-1] + self.acceleration * delta_t  
        particle.x = particle.x[-1] + (0.5 * np.sum(*particle.vx[-2:]) * delta_t)

        if particle.mode == "2D":
            particle.vy = particle.vy[-1] + self.acceleration * delta_t
            particle.y = particle.y[-1] + (0.5 * np.sum(*particle.vy[-2:]) * delta_t)
        
        return particle 