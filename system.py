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
    
    def __repr__(self):
        return f"""
        System energy: {self.kinetic_energy} Acceleration due to friction: \
        {self.acceleration}
        """
        
    def __call__(self, delta_t: float, particle: Particle):
        '''
        * Apply kinematic equations on a particle.
        * Parameters:
            - particle: An object to apply kinematic equations. 
            - delta_t: Time step.  
        '''

        if particle.vx[-1] < 0:
            a_x = self.acceleration 
        elif particle.vx[-1] > 0:
            a_x = -1 * self.acceleration 
        else:
            a_x = 0 
        
        if particle.vy[-1] < 0:
            a_y = self.acceleration 
        elif particle.vy[-1] > 0:
            a_y = -1 * self.acceleration 
        else:
            a_y = 0

        return self.__compute_velocity(a_x, a_y, delta_t, particle)

    def __compute_velocity(self, a_x: float, a_y: float, delta_t: float, 
                           particle: Particle):
        '''
        * Compute the new velocity of the Particle and change the system's 
        total kinetic energy.  
        '''
        #Remove current kinetic energy with respect to old velocity 
        self.ke = -1 * particle.ke()
        particle.vx = particle.vx[-1] + a_x * delta_t  
        particle.x = particle.x[-1] + (0.5 * np.sum(*particle.vx[-2:]) * delta_t)
        particle.vy = particle.vy[-1] + a_y * delta_t
        particle.y = particle.y[-1] + (0.5 * np.sum(*particle.vy[-2:]) * delta_t)
        
        #Change current kinetic energy with respect to new velocity 
        self.ke = particle.ke() 

        return particle     

    @property 
    def ke(self):
        return self.kinetic_energy
    
    @ke.setter 
    def ke(self, value: int):
        self.kinetic_energy += value 