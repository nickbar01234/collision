'''
* Streamlit Demo
* Usage: streamlit run demo.py
'''

from simulation import * 
from solver import * 

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



            