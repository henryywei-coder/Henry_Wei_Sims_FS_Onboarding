import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dataclasses import dataclass
import numpy as np

#constants
maxTorque = 180 #nm
carMass = 300 #kg (with driver)
gearRatio = 3 #3:1
wheelRadius = 0.216 #m

rampThrottleTime = 7 #s
fullThrottleTime = 15 #s

timeStep = 0.01 #s time increments in the simulation

@dataclass
class State:
    #input
    throttleInput: float = 0.0 #0 no acceleration, 1 full acceleration
    time: float = 0.0 #s current time in the simulation

    #output     
    acceleration: float = 0.0 #m/s^2 current acceleration of the car 

def step (state:State) -> State:

    if(state.time <= rampThrottleTime): # ramping up throttle input 
            throttleInput = state.time / rampThrottleTime
    
    else: #full throttle
        throttleInput = 1.0
    
    #Calculate 
    # Multiply driver input by the maximum motor torque to get command torque (rotational force needed from the motor). 
    commandTorque = throttleInput * maxTorque

    #Force at the wheels = (command torque * gear ratio) / radius of the wheels. 
    wheelForce = (commandTorque * gearRatio) / wheelRadius

    # To find acceleration, use the formula Force = mass * acceleration. a =F/m
    acceleration = wheelForce / carMass

    newTime = state.time + timeStep

    return( State( throttleInput=throttleInput, time=newTime, acceleration=acceleration ) )

#Starting State
state = State()
timeTable = [state.time]
accelerationTable = [state.acceleration]

def animate (i):
     global state
     print("frame", i, "time", state.time)

     if state.time >= rampThrottleTime + fullThrottleTime: # stop the animation when the simulation is done
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