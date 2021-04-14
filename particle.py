'''
* Object representation of a particle. 
'''

import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.patches import Rectangle 

class Particle:
    def __init__(self, particle_id: int, length: float, width: float, mass: float,
                 x: float, y: float, vx: float, vy: float):

        assert (length and width) > 0, "Particle must have size"
        assert mass > 0, "Particle must have mass"

        self.id = particle_id 
        self.length = length 
        self.width = width 
        self.mass = mass 

        self._x = []; self.x = x 
        self._vx = []; self.vx = vx 
        self._y = []; self.y = y
        self._vy = []; self.vy = vy 

    def __repr__(self):
        return f"Particle({self.id}, {self.length}, {self.width}, {self.mass}, " \
        + f"{self.x[-1]}, {self.y[-1]}, {self.vx[-1]}, {self.vy[-1]})"
    
    def __str__(self):
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
        return self._x 
    
    @x.setter 
    def x(self, value: int):
        self._x.append(value)
    
    @property 
    def y(self):
        return self._y 
    
    @y.setter 
    def y(self, value: int):
        self._y.append(value)
    
    @property 
    def vx(self):
        return self._vx 
    
    @vx.setter 
    def vx(self, value: int):
        self._vx.append(value)
    
    @property 
    def vy(self):
        return self._vy 
    
    @vy.setter 
    def vy(self, value: int):
        self._vy.append(value)

    def overlap(self, other):
        '''
        * Check if two particles are overlapped. 
        * Parameters: 
            - other: Another instance of Particle. 
        '''
        overlap_x, overlap_y = False, False
        if self != other:
            #Check in x-direction
            if not (self.x[-1] <= other.x[-1] and self.x[-1] + self.length <= other.x[-1]):
                overlap_x = True 
            
            #Check in y-direction
            if self.y[-1] <= other.y[-1] and self.y[-1] + self.width >= other.y[-1]:
                overlap_y = True 

        return overlap_x, overlap_y

    def ke(self):
        '''
        * Compute the kinetic energy of this particle.
        '''
        return 0.5 * self.mass * (self.vx[-1] ** 2 + self.vy[-1] ** 2) 
    
    def draw(self, ax: plt.axes):
        rectangle = Rectangle((self._x[-1], self._y[-1]), self.length, self.width)
        ax.add_patch(rectangle)
        return rectangle
    
    def update(self, length: int = None, width: int = None):
        '''
        * Update list of positions and velocities if they are out of bound.
        '''

        if length is not None:
            for x, vx in zip(self.x, self.vx):
                if x < 0 or x > length:
                    self.x.pop(self.x.index(x))
                    self.vx.pop(self.vx.index(vx))
        
        if width is not None:
            for y, vy in zip(self.y, self.vy):
                if y < 0 or y > width:
                    self.y.pop(self.y.index(y))
                    self.vy.pop(self.vy.index(vy))