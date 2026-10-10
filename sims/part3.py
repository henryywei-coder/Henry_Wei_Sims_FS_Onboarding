import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dataclasses import dataclass
import numpy as np

#constants
airDesnsity = 1.2 #kg/m^3
crossSectionalArea = 1.2 #m^2
dragCoefficient = 0.7
mass = 300 #kg


accelerationTime = 10 # s time at 5 m/s^2


#incereased because it was taking forever 
timeStep = 0.1 #s time increments in the simulation



@dataclass
class State:
   
    time: float = 0.0 #s current time in the simulation
    stepCount: int = 0 #number of steps in the simulation (should remove small errors in time)

    netAcceleration: float = 0.0 #m/s^2 actual acceleration after accounting for drag
    velocity: float = 0.0 #m/s current velocity of the car

def step (state:State) -> State:
    """
    Performs a frame of the simulation \n
    Input: current state of the simulation \n
    Output: new state of the simulation after a time step
    """
    if(state.time <= accelerationTime):
        acceleration = 5.0 #m/s^2
    else:
        acceleration = 0.0



#   Drag = 0.5 * Cross sectional area * drag coefficient * air density * velocity^2.
    drag = 0.5 * crossSectionalArea * dragCoefficient * airDesnsity * (state.velocity**2)

#   Net acceleration = acceleration - (drag/mass)
    newNetAcceleration = acceleration - (drag/mass)

#   Velocity = velocity + (net acceleration * timestep).
    newVelocity = state.velocity + (newNetAcceleration * timeStep)
    
    return( State(
        time = timeStep * (state.stepCount + 1),
        stepCount = state.stepCount + 1,
        netAcceleration = newNetAcceleration,
        velocity = newVelocity
      ) )

#Starting State
state = State()
timeTable = [state.time]
velocityTable = [state.velocity]


def animate (i):
     """
     Animates a frame of the simulation onto the graph
     """
     global state
     

     if state.velocity <= 0.3 and state.time > 1: # stop the animation when the velocity is slow enough to be considered stopped
        ani.event_source.stop()
        return line,

    #update state
     state = step(state)
     timeTable.append( state.time )
     velocityTable.append( state.velocity )
     print("frame", i, "time", state.time, "velocity", state.velocity)

    #adding data to graph
     line.set_data(timeTable, velocityTable)
     
     return line,
    



# graphing stuff
fig = plt.figure(figsize=(3,3), dpi=150)
ax = fig.add_subplot(111)
ax.grid()
ax.set_xlim(-2, 1000)
ax.set_ylim(-2, 100)
ax.set_xlabel("Time (s)")
ax.set_ylabel("Velocity (m/s)")
# these lines are so the animation doesnt zoom in or out
line, = ax.plot([], [])

plt.pause(3)

#calls animate repeatedly to animate each frame of the simulation
ani = animation.FuncAnimation(fig, animate, interval=0)
plt.show()