'''
* Main driver for the simulation
* Usage: python main.py input --output --p --length --dt --time --friction --method
'''

from simulation import * 

import argparse 
import sys 
import os 
import pathlib 

def sample():
    #Sample simulation info 
    simulation_info = {
        "output": "output",
        "mode": "1D",
        "particles": [],
        "n_particles": 2,
        "length": 15, 
        "width": 10,
        "max_vx": 10, 
        "max_vy": 5,
        "max_t": 30,
        "delta_t": 1e-2
    }

    #Sample sytstem info 
    system_info = {
        "system_type": "elastic",
        "kinetic_friction": 0.0,
        "computational_method": "midpoint"
    }

    return simulation_info, system_info 

def assert_output(output: str):
    '''
    * Error checking if output file already existed 
    '''
    files = [str(file).split("\\")[-1] for file in pathlib.Path(os.getcwd()).glob("*.csv")]
    if not output + ".csv" in files:
        return output 

   
    print(f"{output + '.csv'} existed. Type 'yes' to change filename, 'no' to proceed: ", 
          end = "")

    while True:
        command = input()

        if command == "yes":
            break 
        elif command == "no":
            break

        print("Invalid input. Please type 'yes' or 'no': ", end = "")
        command = str(input())

    if command == "yes":
        print("Please enter a new filename: ", end = "")
        output = input()
    else:
        print(f"Current {output + '.csv'} in directory will be deleted")
        os.remove(output + ".csv")

    return assert_output(output) 

def arguments():
    '''
    * Command line arguments. Can be read from a file @{filename}.
    * NOTE:
        - If first argument is 0 then all other command lines will be disregarded.
        Simulation configuration will be used from sample (line 13).
        - If first argument is 1, then --length, --time, --method is required
    '''

    parser = argparse.ArgumentParser(
        prog = "Computation modeling", 
        description = "Explore different computational methods to approximate collisions"
    )

    #Simulation info
    parser.add_argument("input", type = int, 
                        help = """Indicating if argument should be entered from 
                                command line""")
    assert(len(sys.argv) >= 2), \
    "Enter '0' for random initialization and '1' for command line arguments"

    required = sys.argv[1] == '1'
    parser.add_argument("--output", type = str, help = "Name of output file")
    parser.add_argument("-p", "--particles", nargs = "+", type = int, action = "append",
                        help = "Configuration: length, width, mass, x, y, vx, vy",
                        required = required)
    parser.add_argument("--length", type = int, required = required, 
                        help = "The boundary of the simulation")
    parser.add_argument("--dt", type = float, help = "Simulation time step", 
                        required = required)
    parser.add_argument("--time", required = required, 
                        type = int, help = "Maximum simulation run time")

    #System info 
    parser.add_argument("--friction", type = float, required = required, 
                        help = "Kinetic friction coefficient")
    parser.add_argument("--method", type = str, required = required, 
                        choices = ["euler-cromer", "midpoint", "verlet"])

    return parser.parse_args()

def parse_argument(parser: argparse):
    '''
    * Parse command line argument.
    * TODO: Edit if modelling 2D.
    '''

    if parser.input == 0:
        return sample()
    
    filename = "" if parser.output is None else assert_output(parser.output)

    simulation_info = {
        "output": filename,
        "mode": "1D", 
        "particles": [], 
        "n_particles": len(parser.particles), 
        "length": parser.length,
        "width": 5, 
        "max_vx": 0, 
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
    