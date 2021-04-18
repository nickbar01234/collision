'''
* Computational methods for approximating velocity and displacement.
'''

from particle import * 

class Computation:

    def __init__(self, computational_method: str):
        self.method = computational_method 

    def __call__(self, delta_t: float, particle: Particle, acceleration: float):

        if self.method == "euler-cromer":
            return self.__euler_cromer(delta_t, particle, acceleration)
        elif self.method == "midpoint":
            return self.__midpoint(delta_t, particle, acceleration)
        elif self.method == "verlet":
            return self.__verlet(delta_t, particle, acceleration)

    def __euler_cromer(self, delta_t: float, particle: Particle, acceleration: float):
        '''
        * Approximate a particle's velocity and displacement using Euler's 
        algorithm.
        '''

        particle.vx = particle.vx[-1] + acceleration * delta_t 
        particle.x = particle.x[-1] + particle.vx[-1] * delta_t 
        return particle 

    def __midpoint(self, delta_t: float, particle: Particle, acceleration: float):
        '''
        * Approximate a particle's velocity and displacement using midpoint
        algorithm.
        '''

        particle.vx = particle.vx[-1] + acceleration * delta_t  
        particle.x = particle.x[-1] + (0.5 * sum(particle.vx[-2:]) * delta_t)
        return particle 
    
    def ____verlet(self, delta_t: float, particle: Particle, acceleration: float):
        '''
        * Approximate a particle's velocity and displacement using Verlet
        algorithm. This is an mathematical equivalent of leap-frog algorithm.
        '''

        particle.x = particle.x[-1] + particle.vx[-1] * delta_t + 0.5 * \
                     acceleration * delta_t ** 2
        particle.vx = particle.vx[-1] + 0.5 * acceleration * delta_t

        return particle
    
