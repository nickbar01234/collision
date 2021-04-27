# Modeling collisions using Python and R 
---
* This project explores computational physics for collision in 1-dimension.
![Figure 1 2021-04-23 15-13-04](https://user-images.githubusercontent.com/74647679/115841497-0d6fdc00-a447-11eb-84c9-37078308bc32.gif)
---
## Usage
* To begin continue working on this project, type into terminal `git clone github.com/nickbar01234/collision`
* Install depedencies by typing `pip install requirements.txt`
* To run the program, type into terminal `python main.py input --output -p --length --dt --friction --method`
   - Sample input commands can be found in sample_commands.txt or viewed on terminal via `cat sample_commands.txt`
   - `input` can be either '0' or '1'. Note that if it is **1** then all other arguments, besides --output, are required. **0** prompts a random configuration for the collision, users can edit the randomization in main.cpp, beginning at line 13. 
   - `--output` is the output name of the csv file containing the position and velocity of each particle in the simulation. If output is not provided, then no files will be output.
   - `-p` is the configuration of one Particle. Users can type as many -p as needed, a particle instance requires length, width, mass, x, y, vx, vy
      - An example is -p 1, 2, 3, 4, 5, 6, 7. This corresponds to a particle of length 1, width 2, mass 3, x-position at 4, y-position at 5, x-velocity 6, y-velocity 7
   - `length` specifies the boundary in the x direction that a particle can travel
   - `--dt` is the time step for approximation. Smaller time step would result in a more accurate approximation
   - `--friction` is the coefficient for kinetic friction.
   - `--method` is the method of computation. Users can choose from **euler-cromer**, **midpoint**, or **verlet**
---
## Physics

1) **Defining the relationship between frictional force and acceleration**:

![image](https://user-images.githubusercontent.com/74647679/114636345-f4518780-9cf0-11eb-81bf-7655837fe313.png)

* Friction is defined as <img src="https://render.githubusercontent.com/render/math?math=F_f=\mu_{f_k}\times N">.
* From the FBD, we get <img src="https://render.githubusercontent.com/render/math?math=F_k=\mu_{f_k}\times N=\mu_{f_k}mg">.
* Applying Newton's second law of motion, we get <img src="https://render.githubusercontent.com/render/math?math=\pm F_f=\pm\mu_{f_k}mg=ma">, where frictional force is pointing in the positive direction if the object has a negative velocity, and vice versa. Acceleration, thus, is defined as <img src="https://render.githubusercontent.com/render/math?math=\pm F_f=\pm\mu_{f_k}g=a">. In the thereotical case that the surface has no coefficient for kinetic friction, acceleration equals 0. 

2) **Defining momentum and collision**:
* If we take the system to be the Earth and the particles, then the effect of friction applied on an object is an internal force. Momentum will be conserved. 
* From the definition above, momentum is defined as <img src="https://render.githubusercontent.com/render/math?math=\triangle P=P_f-P_o">.
* Momentum of a system of particles is defined as <img src="https://render.githubusercontent.com/render/math?math=P=\sum_{i=1}^n m_iv_i$$$$\sum_{i=1}^n m_i v_{i, o}=\sum_{i=1}^n m_i v_{i, f}">.
* Kinetic energy is defined as <img src="https://render.githubusercontent.com/render/math?math=\frac{1}{2}m_1v_{1,o}^2%2B\frac{1}{2}m_1v_{2,o}^2=\frac{1}{2}m_1v_{1,f}^2%2B\frac{1}{2}m_2v_{2,f}^2">.
* Solving the simultaneous equation, we obtain the final velocities for each particle:
   - <img src="https://render.githubusercontent.com/render/math?math=v_{1,f}=\frac{m_1-m_2}{m_1+m_2} v_{1,o}%2B\frac{2m_1}{m_1+m_2} v_{2,o}">
   - <img src="https://render.githubusercontent.com/render/math?math=v_{2,f}=\frac{2m_1}{m_1+m_2} v_{1,o}%2B\frac{m_1-m_2}{m_1+m_2} v_{2,o}">
---
## Computational methods 

* The application explores 3 different computational methods: **euler-cromer**, **midpoint**, and **verlet**. The exact derivation for each computational method can be found in 
**Resources** section. 

* **Euler-cromer**: 
   - <img src="https://render.githubusercontent.com/render/math?math=v_{n%2B1}=v_n%2B+a_ndt">
   - <img src="https://render.githubusercontent.com/render/math?math=x_{n%2B1}=x_n%2Bv_{n+1}dt">
* **Midpoint**:
   - <img src="https://render.githubusercontent.com/render/math?math=v_{n%2B1}=v_n%2Ba_ndt">
   - <img src="https://render.githubusercontent.com/render/math?math=x_{n%2B1}=x_n%2B\frac{1}{2}(v_{n%2B1}%2Bv_n)dt">
* **Verlet**:
   - <img src="https://render.githubusercontent.com/render/math?math=x_{n%2B1}=x_n%2Bv_ndt%2B\frac{1}{2}a_n(dt)^2">
   - <img src="https://render.githubusercontent.com/render/math?math=v_{n%2B1}=v_n%2B\frac{1}{2}(a_{n%2B1}%2B{a_n})dt">
   - In the case of constant acceleration, we get <img src="https://render.githubusercontent.com/render/math?math=v_{n%2B1}=v_n%2Ba_ndt">
---
## Directory structure

```
.
|--- computation.py: Computational methods.
|--- main.py: Main driver for the program.
|--- output.csv: Sample output from the pre-set configurations.
|--- particle.py: Represents a particle.
|--- README.md
|--- requirements.txt
|--- sample_commands.txt: Users can copy and paste this into the command line to run the simulation.
|--- simulation.py: Represents the simulation.
|--- system.py: Compute elastic collision and apply computational method given a time step.
```
---
## Bugs 

* If there are too many particles and not enough length for the particles to travel, or if the velocity are too high, the animation will have undefined behaviour. 
   - ![Figure 1 2021-04-23 15-21-26](https://user-images.githubusercontent.com/74647679/115842096-b0285a80-a447-11eb-8b4a-4681b2ce8bbe.gif)
---
## Resources

1) Computational methods can be found here: https://www.compadre.org/PICUP/resources/Entry.cfm?ID=124892
2) Christian wrote a great program on 2D elastic collision here. I used their logic to animate my program. The link can be found here: https://scipython.com/blog/two-dimensional-collisions/




