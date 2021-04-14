'''
* Object representation of the system. Includes momentum and frictional force. 
'''

from particle import * 

import numpy as np 

class System:
    def __init__(self, particles: list, system_type: str, kinetic_friction: float):
        assert len(particles) > 0, "System must have at least 1 particle"
        assert system_type in ["elastic", "inelastic"], "Program only supports elastic or inelastic collision"

        self.system_type = system_type
        self._ke = sum([p.ke() for p in particles])
        self.acceleration = kinetic_friction * 9.8 # m/s^2
    
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
        
        if particle.vy[-1] < 0:
            a_y = self.acceleration 
        elif particle.vy[-1] > 0:
            a_y = -1 * self.acceleration 
        else:
            a_y = 0

        particle = self.__compute_velocity(a_x, a_y, delta_t, particle)
        
        return particle 

    def __compute_velocity(self, a_x: float, a_y: float, delta_t: float, 
                           particle: Particle):
        '''
        * Compute the new velocity of the Particle and change the system's 
        total kinetic energy.  
        '''
        #Remove current kinetic energy with respect to old velocity 
        self.ke = -1 * particle.ke()

        particle.vx = particle.vx[-1] + a_x * delta_t  
        particle.x = particle.x[-1] + (0.5 * sum(particle.vx[-2:]) * delta_t)
        
        particle.vy = particle.vy[-1] + a_y * delta_t
        particle.y = particle.y[-1] + (0.5 * sum(particle.vy[-2:]) * delta_t)
        
        #Change current kinetic energy with respect to new velocity 
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
            
            #Check y-direction
            if particle.y[-1] < 0:  
                voy = self.__v_f(particle.y[-1], particle.vy[-1])
                particle.y = 0
                particle.vy = 0
                particle.vy = voy 
            elif particle.y[-1] > width:
                voy = self.__v_f(particle.y[-1], particle.vy[-1])
                particle.y = width - particle.width
                particle.vy = 0
                particle.vy = -1 * voy 
            elif particle.y[-1] + particle.width > width: 
                voy = self.__v_f(particle.y[-1] + particle.width - width, particle.vy[-1])
                particle.y = width - particle.width 
                particle.vy = 0
                particle.vy = -1 * voy 

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

    def momentum(self, overlap_x: bool, overlap_y: bool, particle_1: Particle, 
                 particle_2: Particle):
        '''
        * Apply conservation of momentum on two particles in collision
        '''
        if self.system_type == "elastic":
            return self.__elastic_collision(
                overlap_x, overlap_y, particle_1, particle_2
            )

    def __elastic_collision(self, overlap_x: bool, overlap_y: bool, 
                            particle_1: Particle, particle_2: Particle):
        if overlap_x:
            particle_1_vx_tmp = -1 * particle_1.vx[-1]
            particle_1.vx = 0 
            particle_1.vx = particle_1_vx_tmp 

            particle_2_vx_tmp = -1 * particle_2.vx[-1]
            particle_2.vx = 0
            particle_2.vx = particle_2_vx_tmp
            particle_2.x = particle_1.x[-1] + particle_1.length
        
        if overlap_y and overlap_x:
            particle_1_vy_tmp = -1 * particle_1.vy[-1]
            particle_1.vy = 0 
            particle_1.vy = particle_1_vy_tmp 

            particle_2_vy_tmp = -1 * particle_2.vy[-1]
            particle_2.vy = 0
            particle_2.vy = particle_2_vy_tmp
            particle_2.y = particle_1.y[-1] + particle_1.width

        return particle_1, particle_2 

    @property 
    def ke(self):
        return self._ke
    
    @ke.setter 
    def ke(self, value: int):
        self._ke += value 