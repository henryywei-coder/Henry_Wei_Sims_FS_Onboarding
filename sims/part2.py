import math

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dataclasses import dataclass
import numpy as np

#constants
forwardSpeed = 15.0 #m/s
corneringStiffness = 36000 # N/rad
carMass = 300 #kg

turnSteeringTime = 3 #s (0 - 5 degrees)
holdSteeringTime = 7 #s 5 degrees 

timeStep = 0.01 #s time increments in the simulation

@dataclass
class State:
    steeringInput: float = 0.0 #0 degrees = straight
    time: float = 0.0 #s current time in the simulation

    slipAngle: float = 0.0 #rad
    lateralVelocity: float = 0.0 #m/s current lateral velocity of the car    
    lateralAcceleration: float = 0.0 #m/s^2 current lateral acceleration of the car
    lateralForce: float = 0.0 #N current lateral force on the car




def step (state:State) -> State:

    if(state.time <= turnSteeringTime): # ramping up steering input 
            steeringInput = (5.0 * state.time) / turnSteeringTime
    #what am I outputting? is the graph time to slip angle?
    else: #hold steering
        steeringInput = 5.0

    #convert to radians
    radSteeringInput = steeringInput * math.pi / 180.0

    #Calculate 
    #Slip angle = steer angle - (lateral velocity/forward speed).
    slipAngle = radSteeringInput - (state.lateralVelocity / forwardSpeed)

    #Lateral force = cornering stiffness * slip angle
    lateralForce = corneringStiffness * slipAngle

    #Lateral acceleration = lateral force/mass
    lateralAcceleration = lateralForce / carMass

    #Lateral velocity = lateral velocity(previous) + (lateral acceleration * timestep)
    lateralVelocity = state.lateralVelocity + (lateralAcceleration * timeStep)
   
    newTime = state.time + timeStep

    return( State( 
                steeringInput=steeringInput,
                time=newTime,
                slipAngle=slipAngle,
                lateralVelocity=lateralVelocity,
                lateralAcceleration=lateralAcceleration,
                lateralForce=lateralForce ) )

#Starting State
state = State()
timeTable = [state.time]
accelerationTable = [state.acceleration]

def animate (i):
     global state
     print("frame", i, "time", state.time)
     if state.time >= turnSteeringTime + holdSteeringTime: # stop animation when simulation is done
        ani.event_source.stop()
        return line,

    #update state
     state = step(state)
     timeTable.append( state.time )
     accelerationTable.append( state.acceleration )

     line.set_data(timeTable, accelerationTable)

     
    

# graphing stuff
fig = plt.figure(figsize=(3,3), dpi=150)
ax = fig.add_subplot(111)
ax.grid()
ax.set_xlim(-2, 30)
ax.set_ylim(-2, 10)
ax.set_xlabel("Time (s)")
ax.set_ylabel("Acceleration (m/s^2)")
# these lines are so the animation doesnt zoom in or out
line, = ax.plot([], [])

plt.pause(3)

#calls animate repeatedly to animate each frame of the simulation
ani = animation.FuncAnimation(fig, animate, interval=0)
plt.show()