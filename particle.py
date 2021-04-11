'''
* Object representation of a particle. 
'''

import numpy as np 

import matplotlib.pyplot as plt 
from matplotlib.patches import Rectangle 

class Particle:
    def __init__(self, particle_id: int, length: float, width: float, mass: float,
                 x: float, y: float, vx: float, 
                 vy: float):

        assert (length and width) > 0, "Particle must have size"
        assert mass > 0, "Particle must have mass"

        self.id = particle_id 
        self.length = length 
        self.width = width 
        self.mass = mass 

        self.xpos = []; self.x = x 
        self.v_x = []; self.vx = vx 
        self.ypos = []; self.y = y
        self.v_y = []; self.vy = vy 


    def __repr__(self):
        return f"ID: {self.id} x: {self.x[-1]} xv: {self.vx[-1]} " + \
        f"y: {self.y[-1]} yv: {self.vy[-1]}"
    
    def __eq__(self, other):
        '''
        * Equal operator overload. An easy way to check if the current instance
        is equal to the other instance by assigning each particle an unique 
        identifier.
        '''
        return self.id == other.id 

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
        if self == other:
            return overlap  
        else: 
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
    
    def draw(self, ax: plt.axes):
        rectangle = Rectangle((self.x, self.y), self.length, self.width)
        ax.add_patch(rectangle)
        return rectangle