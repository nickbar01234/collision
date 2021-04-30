from scipy.integrate import odeint
import numpy as np

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