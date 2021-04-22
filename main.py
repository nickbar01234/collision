'''
* Main driver for the simulation
* Usage: python main.py input --particles --length --vx --dt --time --friction --method
'''

from simulation import * 

import argparse 
import sys 

def sample():
    #Sample simulation info 
    simulation_info = {
        "mode": "1D",
        "particles": [],
        "n_particles": 4,
        "length": 30, 
        "width": 10,
        "max_vx": 5, 
        "max_vy": 5,
        "max_t": 10,
        "delta_t": 1e-2
    }

    #Sample sytstem info 
    system_info = {
        "system_type": "elastic",
        "kinetic_friction": 0.0,
        "computational_method": "midpoint"
    }

    return simulation_info, system_info 

def arguments():
    '''
    * Command line arguments. Can be read from a file @{filename}.
    * NOTE:
        - If first argument is 0 then all other command lines will be disregarded.
        Simulation configuration will be used from sample (line 11).
        - If first argument is 1, then --length, --time, --method is required
    '''

    parser = argparse.ArgumentParser(
        prog = "Computation modeling", 
        description = "Explore different computational methods to approximate collisions",
        fromfile_prefix_chars = '@'
    )

    #Simulation info
    parser.add_argument("input", type = int, 
                        help = """Indicating if argument should be entered from 
                                command line""")
    parser.add_argument("-p", "--particles", nargs = "+", type = int, action = "append",
                        help = """
                        Particle configuration: length, width, mass, x, y, vx, vy
                        """)
    parser.add_argument("--length", type = int, required = sys.argv[1] == '1', 
                        help = "The distance a particle can travel in the x direction")
    parser.add_argument("--vx", type = int, help = """
                        Maximum x-velocity of a particle. Required if a list 
                        of particle configurations is given.
                        """, default = 5)
    parser.add_argument("--dt", type = float, help = "Simulation time step", 
                        default = 1e-2)

    parser.add_argument("--time", required = sys.argv[1] == '1', 
                        type = int, help = "Maximum simulation run time")

    #System info 
    parser.add_argument("--friction", type = float, default = 0, 
                        help = "Kinetic friction coefficient")
    parser.add_argument("--method", type = str, required = sys.argv[1] == '1', 
                        choices = ["euler-cromer", "midpoint", "verlet"])

    return parser.parse_args()

def parse_argument(parser: argparse):
    '''
    * Parse command line argument.
    * TODO: Edit if modelling 2D.
    '''
    
    if parser.input == 0:
        return sample()

    simulation_info = {
        "mode": "1D", 
        "particles": [], 
        "n_particles": len(parser.particles), 
        "length": parser.length,
        "width": 5, 
        "max_vx": parser.vx, 
        "max_vy": 0, 
        "max_t": parser.time, 
        "delta_t": parser.dt}

    for configuration in parser.particles:
        simulation_info["particles"].append(Particle(*configuration))


    system_info = {"system_type": "elastic", "kinetic_friction": parser.friction, 
                   "computational_method": parser.method}

    return simulation_info, system_info 

def main():
    parser = arguments()
    simulation_info, system_info = parse_argument(parser)
    simulation = Simulation(**simulation_info, system_info = system_info)
    simulation.animation()

if __name__ == "__main__":
    main()
    