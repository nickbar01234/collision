'''
* Object representation of a particle. 
'''

import numpy as np 

class Particle:
    def __init__(self, mode: str, length: float, width: float, mass: float,
                 xpos: float = None, ypos: float = None, v_x: float = None, 
                 v_y: float = None):

        assert mode in ["1D", "2D"], "Mode must be 1D or 2D"
        assert (length and width) > 0, "Particle must have size"
        assert mass > 0, "Particle must have mass"

        self.length = length 
        self.width = width 
        self.mass = mass 

        self.xpos = xpos 
        self.v_x = v_x 

        if mode == "2D":
            self.ypos = ypos 
            self.v_y = v_y 
    
    def __repr__(self):
        return f"X-position: {self.x} X-velocity: {self.vx}"
        
    @property 
    def x(self):
        return self.xpos 
    
    @x.setter 
    def x(self, value: int):
        self.xpos = value 
    
    @property 
    def vx(self):
        return self.v_x 
    
    @vx.setter 
    def vx(self, value):
        self.v_x = value 

    def __overlap(self, other: Particle):
        '''
        * Check if two particles are overlapped. 
        '''
        return other.x <= self.x and self.x - self.width <= other.x 
        
