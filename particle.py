import numpy as np 

class Particle:
    def __init__(self, collision_type: str, x: float = None, y: float = None, 
                 vx: float = None, vy: float = None, mass: float = None):
        
        assert collision_type in ["1D", "2D"], \
        "'Collisions are only modelled for 1D and 2D kinematics.'"
        assert mass is not None, \
        "'Objects cannot be massless."

        self.x = []
        self.y = []
        self.vx = []
        self.vy = []
        self.mass = mass 
        
    @property 
    def x(self):
        return self.x[-1]
    
    @x.setter
    def x(self, value):
        self.x.append(value)
    
    @property 
    def deltaX(self):
        if len(x) == 1:
            return self.x[-1]
        return np.substract(*self.x[-1:-3:-1])

    @property 
    def y(self):
        return self.y[-1]
    
    @y.setter 
    def y(self, value):
        self.y.append(value)
    
    @property 
    def vx(self):
        return self.vx[-1]
    
    @vx.setter
    def vx(self, value):
        self.vx.append(value)

    @property 
    def vy(self):
        return self.vy[-1]    

    @vy.setter
    def vy(self, value):
        self.vy.append(value)
    

