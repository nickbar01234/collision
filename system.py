'''
* Object representation of the system. Includes momentum and frictional force. 
'''

from particle import * 
from Computation import *

import numpy as np 

class System:
    def __init__(self, particles: list, system_type: str, kinetic_friction: float,
                 computational_method: str):

        assert len(particles) > 0, "System must have at least 1 particle"
        assert system_type in ["elastic", "inelastic"], "Program only supports elastic or inelastic collision"

        self.system_type = system_type
        self._ke = sum([p.ke() for p in particles])
        self.acceleration = kinetic_friction * 9.8 # m/s^2
        self.computation = Computation(computational_method)

    def __repr__(self):
        return f"System({self.ke},{self.acceleration / 9.8})"
        
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

        self.ke = -1 * particle.ke()
        particle = self.computation(delta_t, particle, a_x)
        self.ke = particle.ke()

        return particle 
        
    def wall(self, particle: Particle, length: int, width: int):
        '''
        * Bounces the particle of the wall if collision is elastic, otherwise 
        it stops. 
        '''
        if self.system_type == "elastic":
            #Check x-direction
            if particle.x[-1] < 0:  
                vox = self.__v_f(particle.x[-1], particle.vx[-1])
                particle.x = 0
                particle.vx = 0
                particle.vx = vox 
            elif particle.x[-1] > length:
                vox = self.__v_f(particle.x[-1], particle.vx[-1])
                particle.x = length - particle.length
                particle.vx = 0
                particle.vx = -1 * vox 
            elif particle.x[-1] + particle.length > length: 
                vox = self.__v_f(particle.x[-1] + particle.length - length, particle.vx[-1])
                particle.x = length - particle.length 
                particle.vx = 0
                particle.vx = -1 * vox
        
            particle.update(length, width)

        return particle  
        
    def __v_f(self, distance: float, velocity: float):
        '''
        * Compute the velocity before the particle hits the wall.
        * NOTE: 
            - If acceleration is negative then the initial velocity is also negative. 
        '''

        if velocity > 0:
            acceleration = self.acceleration 
        else:
            acceleration = -1 * self.acceleration 

        v_o = np.sqrt(velocity ** 2 - 2 * acceleration * distance)

        return v_o 

    def momentum(self, particle_1: Particle, particle_2: Particle):
        '''
        * Apply conservation of momentum on two particles in collision
        '''

        if self.system_type == "elastic":
            mass = particle_1.mass + particle_2.mass 

            v1 = (1 / mass) * (particle_1.mass - particle_2.mass) * particle_1.vx[-1] + \
                (1 / mass) * (2 * particle_2.mass * particle_2.vx[-1])
            
            v2 = (1 / mass) * (2 * particle_2.mass * particle_1.vx[-1]) + \
                (1 / mass) * (particle_2.mass - particle_1.mass) * particle_2.vx[-1]
            
            particle_1.vx = v1 
            particle_2.vx = v2 

        return particle_1, particle_2 

    @property 
    def ke(self):
        return self._ke
    
    @ke.setter 
    def ke(self, value: int):
        self._ke += value 