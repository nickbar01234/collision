# Modeling collisions using Python and R 
---
* This project explores computational physics for collision in 1-dimension and 2-dimensions.
---
## Physics
---
1) **Defining the relationship between frictional force and acceleration**:

![image](https://user-images.githubusercontent.com/74647679/114636345-f4518780-9cf0-11eb-81bf-7655837fe313.png)

* Friction is defined as <img src="https://render.githubusercontent.com/render/math?math=F_f=\mu_{f_k}\times N">.
* From the FBD, we get <img src="https://render.githubusercontent.com/render/math?math=F_k=\mu_{f_k}\times N=\mu_{f_k}mg">.
* Applying Newton's second law of motion, we get <img src="https://render.githubusercontent.com/render/math?math=\pm F_f=\pm\mu_{f_k}mg=ma">, where frictional force is pointing in the positive direction if the object has a negative velocity, and vice versa. Acceleration, thus, is defined as <img src="https://render.githubusercontent.com/render/math?math=\pm F_f=\pm\mu_{f_k}g=a">.

2) **Defining momentum and collision**:
* If we take the system to be the Earth and the particles, then the effect of friction applied on an object is an internal force. Momentum will be conserved. 
* From the definition above, momentum is defined as <img src="https://render.githubusercontent.com/render/math?math=\triangle P=P_f-P_o">.
* Momentum of a system of particles is defined as <img src="https://render.githubusercontent.com/render/math?math=P=\sum_{i=1}^n m_iv_i$$$$\sum_{i=1}^n m_i v_{i, o}=\sum_{i=1}^n m_i v_{i, f}">.
* Kinetic energy is defined as <img src="https://render.githubusercontent.com/render/math?math=\0.5m_1v_{1,o}^2+0.5m_1v_{2,o}^2=0.5m_1v_{1,f}^2+0.5m_2v_{2,f}^2">.
* Solving for each velocity, we obtain:
<img src="https://render.githubusercontent.com/render/math?math=\v_{1,f}=\frac{m_1-m_2}{m_1+m_2}v_{1,o} + \frac{2m_1}{m_1+m_2}v_{2,o}">.
<img src="https://render.githubusercontent.com/render/math?math=\v_{2,f}=\frac{2m_1}{m_1+m_2}\times v_{1,o} + \frac{m_1-m_2}{m_1+m_2}\times v_{2,o}">.


---
## Checkpoint 
---
1) Object representation of a particle 
    * Check if two particles are overlapped 
    * Compute kinetic energy of a particle 
2) 
---
## TODO 
--- 
1) Check if kinematic equations 
2) Check overlapping 
3) Check architecture

