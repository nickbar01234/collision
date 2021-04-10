'''
* Object representation of a particle. 
'''

import numpy as np 

class Particle:
    def __init__(self, length: float, width: float, mass: float,
                 x: float, y: float, vx: float, 
                 vy: float):

        assert (length and width) > 0, "Particle must have size"
        assert mass > 0, "Particle must have mass"

        self.length = length 
        self.width = width 
        self.mass = mass 

        self.xpos = []; self.x = x 
        self.v_x = []; self.vx = vx 
        self.ypos = []; self.y = y
        self.v_y = []; self.vy = vy 


    def __repr__(self):
        return f"""
        X-position: {self.x[-1]} X-velocity: {self.vx[-1]} \
        Y-position: {self.y[-1]} Y-velocity: {self.vy[-1]}
        """
        
    @property 
    def x(self):
        return self.xpos 
    
    @x.setter 
    def x(self, value: int):
        self.xpos.append(value) 
    
    @property 
    def y(self):
        return self.ypos 
    
    @y.setter 
    def y(self, value: int):
        self.ypos.append(value)
    
    @property 
    def vx(self):
        return self.v_x 
    
    @vx.setter 
    def vx(self, value: int):
        self.v_x.append(value)
    
    @property 
    def vy(self):
        return self.v_y 
    
    @vy.setter 
    def vy(self, value: int):
        self.v_y.append(value)

    def __overlap(self, other):
        '''
        * Check if two particles are overlapped. 
        * Parameters: 
            - other: Another instance of Particle. 
        '''

        overlap = False 

        if (other.x <= self.x) and (other.x >= self.x - self.length):
            overlap = True  
        elif other.x - other.length <= self.x:
            overlap = True 
        
        return overlap 

    def ke(self):
        '''
        * Compute the kinetic energy of this particle.
        '''
        return 0.5 * self.mass * (self.vx[-1] ** 2 + self.vy[-1] ** 2) 