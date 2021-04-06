from particle import * 

class System:
    def __init__(self, particles: list = None, kinetic_friction: float = None):
        if particles is None:
            raise NotImplementedError("Systems must have particles.")
        
        self.friction = Friction(kinetic_friction) 


