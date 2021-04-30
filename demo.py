'''
* Streamlit Demo
* Usage: streamlit run demo.py
'''

import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.patches import Rectangle 
import numpy as np 
import pprint
import pandas as pd
import matplotlib.pyplot as plt 
from matplotlib import animation 
import itertools 
import streamlit as st 
import streamlit.components.v1 as components 
from scipy.integrate import odeint

class Particle:
    def __init__(self, length: float, width: float, mass: float,
                 x: float, y: float, vx: float, vy: float, particle_id: int = None):

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
        if self != other:
            return True if not (self.x[-1] <= other.x[-1] and self.x[-1] + \
                   self.length <= other.x[-1]) else False
        return False 
        
    def ke(self):
        '''
        * Compute the kinetic energy of this particle.
        '''
        return 0.5 * self.mass * (self.vx[-1] ** 2 + self.vy[-1] ** 2) 
    
    def draw(self, ax: plt.axes, add_patch: bool = True):
        '''
        * Represent a particle for animation.
        '''
        rectangle = Rectangle((self._x[-1], self._y[-1]), self.length, self.width, 
                               edgecolor = 'r', fill = False)
        
        if add_patch:
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
    
    def __verlet(self, delta_t: float, particle: Particle, acceleration: float):
        '''
        * Approximate a particle's velocity and displacement using Verlet
        algorithm. This is a mathematical equivalent of leap-frog algorithm.
        '''

        particle.x = particle.x[-1] + particle.vx[-1] * delta_t + 0.5 * \
                     acceleration * delta_t ** 2
        particle.vx = particle.vx[-1] + 0.5 * (acceleration + acceleration) * delta_t

        return particle

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
        
            # particle.update(length, width)

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

class Simulation:
    def __init__(self, output: str, mode: str, particles: list, n_particles: int, 
                 length: int, width: int, max_vx: int, max_vy: int, 
                 max_t: int, delta_t: float, system_info: dict):
        
        self.output = output 

        assert mode in ["1D", "2D"], "Simluation must be 1D or 2D"
        self.mode = mode
        
        assert (length and width) >= 0, "Grid cannot have negative value"
        self.length = length
        self.width = width

        assert delta_t >= 0, "Time step cannot be zero or negative"
        self.time = 0
        self.max_t = max_t
        self.delta_t = delta_t 

        self.particles = particles
        if len(self.particles) == 0:
            self.__init_particles(n_particles, max_vx, max_vy)
        else:
            for i in range(len(particles)):
                particles[i].id = i 

        self.system = System(self.particles, **system_info)
        self.exit = True 

    def animation(self):
        '''
        * Add animations to object. The computation is done from function call 
        to __animate().
        '''

        fig, self.ax = plt.subplots()
        for spine in ["top", "bottom", "left", "right"]:
            self.ax.spines[spine].set_linewidth(2)
        self.ax.set_aspect("equal", "box")
        self.ax.set_xlim(0, self.length)
        self.ax.set_ylim(0, self.width)
        self.ax.xaxis.set_ticks([])
        self.ax.yaxis.set_ticks([])

        try:
            self.animate = animation.FuncAnimation(
                fig, self.__animate, init_func = self.__init_animation, 
                frames = 1600, interval = 1, blit = True
            )
            plt.show()
        except Exception as e:
            exit(0)

    def streamlit_animation(self):
        '''
        * Animation for streamlit.
        '''
        def animate(plot):
            while True:
                self.__animate(0)
                rectangle = self.__init_animation()          

                self.ax.patches = []
                for i in rectangle:
                    self.ax.add_patch(i)
                
                self.ax.texts = []
                self.ax.text(0.5, self.width - 0.5, "KE:{:.2f}J".format(self.system.ke),
                             color = "r", fontsize = "15")
                momentum = sum([particle.mass * particle.vx[-1] for particle in self.particles])
                self.ax.text(4, self.width - 0.5, r"Momentum:{:.2f}$kgm^2$".format(momentum),
                             color = "r", fontsize = "15")
                plot.pyplot(self.fig)

        self.exit = False

        self.__init_plot()
        rectangle = self.__init_animation(False)   
        for i in rectangle:
            self.ax.add_patch(i)
        
        self.ax.text(0.5, self.width - 0.5, "KE:{:.2f}J".format(self.system.ke),
                     color = "r", fontsize = "15")
        momentum = sum([particle.mass * particle.vx[-1] for particle in self.particles])
        self.ax.text(4, self.width - 0.5, r"Momentum:{:.2f}$kgm^2$".format(momentum),
                    color = "r", fontsize = "15")
        plot = st.pyplot(self.fig)
        animate(plot)

    def __repr__(self):
        return f"Configuration\nMode: {self.mode}, Length: {self.length}, " + \
            f"Width: {self.width}, \n{self.particles}" 

    def __debug(self):
        info = " ".join([str(particle) for particle in self.particles])
        print(info)

    def __init_particles(self, n_particles: int, max_vx: int, max_vy: int):

        '''
        * If not reading from file, then randomly generate a simulation of 
        n particles. 
        * NOTE: 
            - For random initialization, mass, length, and width are set to 1. 
        '''
        np.random.seed(1)

        print("Begin random initialization")

        mass = 1 #kg 
        length = 1; width = 1 #m

        xpos = [pos for pos in range(self.length)]
        ypos = [pos for pos in range(self.width)]
        vx = [v for v in range(-1 * max_vx, max_vx + 1) if v != 0]
        vy = [v for v in range(-1 * max_vy, max_vy + 1) if v != 0]

        for index, i in enumerate(range(n_particles)):
            x = int(np.random.choice(xpos))
            v_x = int(np.random.choice(vx))
            xpos.pop(xpos.index(x)) #Remove xposition so there won't be overlaps 

            y = 0
            v_y = 0
            if self.mode == "2D":
                y = np.random.choice(ypos)
                v_y = np.random.choice(vy)
                ypos.pop(ypos.index(y)) #Remove yposition so there won't be overlaps  

            particle = Particle(length, width, mass, x, y, v_x, v_y, index)
            self.particles.append(particle)
        
        print(self.__repr__())
        print("Finish random initialization")

    def __init_animation(self, add_patch: bool = True):
        '''
        * Initialize the initial frame for animation. 
        '''
        position = []

        for particle in self.particles:
            position.append(particle.draw(self.ax, add_patch))
        
        return position 

    def __animate(self, frame: int):
        '''
        * Compute new position and velocity for every particle by a time step 
        delta_t
        '''
        if self.exit:
            if self.time >= self.max_t:
                print("Program is out of time, terminating.")
                if self.output != "":
                    df = self.__get_output()
                    df.to_csv(self.output + ".csv", index = False)
                exit(0)

        for index, particle in enumerate(self.particles):
            self.particles[index] = self.system(self.delta_t, particle)
        
        self.time += self.delta_t 
        
        self.__collision()
        return self.__init_animation()
    
    def __collision(self):
        '''
        * Apply momentum of conservation if particles collided with walls or 
        each other.
        ''' 

        for index, particle in enumerate(self.particles):
            self.particles[index] = self.system.wall(
                particle, self.length, self.width 
            )
        
        for i, j in itertools.combinations(range(len(self.particles)), 2):
            if self.particles[i].overlap(self.particles[j]):
                self.particles[i], self.particles[j] = self.system.momentum(
                    self.particles[i], self.particles[j]
                )
                
    def __get_output(self):
        '''
        * Get the position and velocity of each particle.
        * NOTE: A dummy padding is applied if there is a length mismatch between 
                columns.
        '''
        data = {}

        for particle in self.particles:
            data[str(particle.id) + "_x"] = particle.x
            data[str(particle.id) + "_vx"] = particle.vx 
        
        max_length = 0        
        for key in data.keys():
            max_length = len(data[key]) if len(data[key]) > max_length else max_length 
        
        for key in data.keys():
            if len(data[key]) < max_length:
                pad = [None for i in range(max_length - len(data[key]))]
                data[key].extend(pad)

        return pd.DataFrame(data)

    def __init_plot(self):
        self.fig, self.ax = plt.subplots()
        for spine in ["top", "bottom", "left", "right"]:
            self.ax.spines[spine].set_linewidth(2)
        self.ax.set_aspect("equal", "box")
        self.ax.set_xlim(0, self.length)
        self.ax.set_ylim(0, self.width)
        self.ax.xaxis.set_ticks([])
        self.ax.yaxis.set_ticks([])

def f_x():
    return 1

def f_y(mass: int, g: float):
    return -1 * mass * g 

def solver(mass: int, g: float, xpos: int, vx: int, ypos: int, vy: int, t: int):

    def varint(vararr, t):
        x, xt, y, yt = vararr
        return [xt, f_x(), yt, f_y(mass, g) / mass]

    var_arr = [xpos, vx, ypos, vy]
    tarr = np.linspace(0, t, 100)
    solvar = odeint(varint, var_arr, tarr)

    return solvar

def approximation(method, mass: int, g: float, xpos: int, vx: int, ypos: int, vy: int, 
                  t: int, dt: int):

    x, y = [xpos], [ypos]
    v_x, v_y = [vx], [vy]

    current_time = 0
    while (current_time <= t):

        ax = f_x()
        ay = f_y(mass, g) / mass

        xpos, vx, ypos, vy = approximate(method, x, y, v_x, v_y, ax, ay, dt)

        x.append(xpos)
        y.append(ypos)
        v_x.append(vx)
        v_y.append(vy)

        current_time += dt
    
    return np.asarray(x), np.asarray(v_x), np.asarray(y), np.asarray(v_y)

def approximate(method, x, y, v_x, v_y, ax, ay, dt):

    if method == "euler-cromer":
        vx = v_x[-1] + ax * dt 
        xpos = x[-1] + vx * dt
        
        vy = v_y[-1] + ay * dt
        ypos = y[-1] + vy * dt
    elif method == "midpoint":
        vx = v_x[-1] + ax * dt
        xpos = x[-1] + 0.5 * (vx + v_x[-1]) * dt

        vy = v_y[-1] + ay * dt
        ypos = y[-1] + 0.5 * (vy + v_y[-1]) * dt
    else:
        xpos = x[-1] + v_x[-1] * dt + 0.5 * ax * dt ** 2
        vx = v_x[-1] + 0.5 * (ax + ax) * dt

        ypos = y[-1] + v_y[-1] * dt + 0.5 * ay * dt ** 2
        vy = v_y[-1] + 0.5 * (ay + ay) * dt 

    return xpos, vx, ypos, vy

def style():
    st.markdown(
        '''
        <head>
        <link href="https://fonts.googleapis.com/css2?family=Alata&display=swap" rel="stylesheet">
        <style>
        h1 {
            color: #C9082A;
            font-family: "Times New Roman", Times, serif;
            font-size: 200%;
            text-align: center;
            font-weight: bold}
        h2 {
            font-family:  "Times New Roman", Times, serif;
            font-size: 150%;
            text-align: left;
            border-bottom: 1px solid;
        }
        p {
            font-family: "Times New Roman", Times, serif;
            font-size: 100%;
        }
        </style>
        </head>
        ''', unsafe_allow_html = True) 

def init_text():
    '''
    * Initialize texts.
    '''
    #Header
    st.markdown(
        "<h1>Computational Physics for Elastic Collision</h1><h2>Physics Applied</h2>", 
        unsafe_allow_html = True
    )

    #Momentum
    st.markdown(
        "<p>Conservation of Momentum:</p>", unsafe_allow_html = True
    )

    st.latex(
        r"""\triangle P=P_f-P_o\\[0.2in]
        \sum_{i=1}^{n}m_iv_{i,0}=\sum_{i=1}^{n}m_iv_{i,f}\\[0.2in]
        """
    )

    #KE
    st.markdown(
        "<p>Conservation of Kinetic Energy:</p>", unsafe_allow_html = True
    )

    st.latex(
        r"""
         \frac{1}{2}m_1v^2_{1,0}+\frac{1}{2}m_2v^2_{2,0}=\frac{1}{2}
        m_1v^2_{1,f}+\frac{1}{2}m_2v^2_{2,f}\\[0.2in]
        """
    )

    #Velocity after collision
    st.markdown(
        "<p>Velocity after collision:</p>", unsafe_allow_html = True
    )

    st.latex(
        r"""
        v_{1,f}=\frac{m_1-m_2}{m_1+m_2}v_{1,0}+\frac{2m_1}{m_1+m_2}v_{2,0}\\[0.2in]
        """
    )

    #Computational method
    st.markdown(
        "<h2>Computational method</h2><p>Euler-cromer:</p>", unsafe_allow_html = True
    )

    st.latex(
        r"""
        v_{n+1}=v_n+a_ndt\\[0.2in]
        x_{n+1}=x_n+v_{n+1}dt\\[0.2in]
        """
    )

    st.markdown(
        "<p>Midpoint:</p>", unsafe_allow_html = True
    )

    st.latex(
        r"""
        v_{n+1}=v_n+a_ndt\\[0.2in]
        x_{n+1}=x_n+\frac{1}{2}(v_{n+1}+v_n)dt\\[0.2in]
        """
    )

    st.markdown(
        "<p>Verlet:</p>", unsafe_allow_html = True
    )

    st.latex(
        r"""
        x_{n+1}=x_n+v_ndt+\frac{1}{2}dt^2\\[0.2in]
        v_{n+1}=v_n+\frac{1}{2}(a_{n+1}+a_n)dt\\[0.2in]
        """
    )
    
    #Interactive session
    st.markdown(
        "<h2>Interactive Session</h2>", unsafe_allow_html = True
    )

def option():
    '''
    * Simulation configuration.
    '''
    choice = st.selectbox(label = "", options = ["Explore", "Simulation"])

    st.sidebar.markdown("<p>Simulation Configuration</p>", unsafe_allow_html = True)
    n_particles = st.sidebar.slider(label = "Particles", min_value = 1, max_value = 4, 
                                    value = 2)
    length = st.sidebar.slider(label = "Length", min_value = 10, max_value = 30)
    max_vx = st.sidebar.slider(label = "Max velocity", min_value = 10, max_value = 30,
                               value = 20)
    friction = st.sidebar.slider(label = "Kinetic friction coefficient", 
                                min_value = 0.0, max_value = 1.0)
    st.sidebar.markdown("---")
    st.sidebar.markdown("<p>Computational method</p>", unsafe_allow_html = True)
    method = st.sidebar.selectbox(label = "", 
                              options = ["euler-cromer", "midpoint", "verlet"]
                             )

    return choice, method, n_particles, length, max_vx, friction

def explore():
    st.markdown(
    """
    <p>This project simulates 1-D motion using different computational 
    methods. Intuitively, most computational methods are well behaved 
    when there are no net force acting on object. Explore what happens 
    when an arbitrary object is in free fall.</p>
    """, unsafe_allow_html = True
    )
    vx = st.slider(label = "vx", min_value = 1, max_value = 20)
    vy = st.slider(label = "vy", min_value = 1, max_value = 20)
    dt = st.slider(label = "dt", min_value = 1e-1, max_value = 1.0, step = 0.1, value = 1.0)

    return vx, vy, dt

def get_simulation(n_particles: int, length: int, max_vx: int, 
              friction: float, method: str):

    simulation_info = {
        "output": "",
        "mode": "1D",
        "particles": [],
        "n_particles": n_particles,
        "length": length,
        "width": 5,
        "max_vx": max_vx,
        "max_vy": 0,
        "max_t": 10,
        "delta_t": 1e-2
        }
    system_info = {
        "system_type": "elastic",
        "kinetic_friction": friction,
        "computational_method": method
    }

    simulation = Simulation(**simulation_info, system_info = system_info)
    
    return simulation

def main():
    style()
    init_text()
    choice, method, n_particles, length, max_vx, friction = option()
    
    if choice == "Simulation":
        simulation = get_simulation(n_particles, length, max_vx, friction, method)
        simulation.streamlit_animation()
    elif choice == "Explore":
        vx, vy, dt = explore()
        solvar = solver(1, 9.8, 0, vx, 1000, vy, 10)
        x, vx, y, vy = approximation(method, 1, 9.8, 0, vx, 1000, vy, 10, dt)

        xsol = solvar[:, 0]
        ysol = solvar[:,2]

        fig = plt.figure(figsize=(10, 5), dpi=80)

        plt.plot(xsol, ysol, 'b', label='Exact')
        plt.plot(x, y, '--o', color='r', label='Approximation')
        plt.legend(loc='best')
        plt.xlabel('x (m)')
        plt.ylabel('y (m)')
        plt.xticks([])
        plt.yticks([])
        st.pyplot(plt)

if __name__ == "__main__":
    main()



            