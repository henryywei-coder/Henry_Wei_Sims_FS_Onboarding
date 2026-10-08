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

#function parameters for throttle input cubic function
# throttleInput = Ax^3 + Bx^2 + Cx + Dx 
A = 4/343
B = -6/49
C = 3/7
D = 0.0


timeStep = 0.01 #s time increments in the simulation



def throttleInputFunction( t:float ) -> float: 
    """
    Input: simulation time \n
    Output: throttle input \n
    Handles ramping throttle and holding full throttle.
    """
    # throttleInput = Ax^3 + Bx^2 + Cx + Dx 
    if(t <= rampThrottleTime): # ramping up throttle input
        return A * t**3 + B * t**2 + C * t + D
    
    elif(t <= rampThrottleTime + fullThrottleTime): #full throttle
        return 1.0
    
    else: #throw error time went over simulation window
        raise ValueError("Time is out of bounds for throttle input function")

    
    
    

@dataclass
class State:
    #input
    throttleInput: float = 0.0 #0 no acceleration, 1 full acceleration
    time: float = 0.0 #s current time in the simulation

    #output     
    acceleration: float = 0.0 #m/s^2 current acceleration of the car 

def step (state:State) -> State:
    """
    Performs a frame of the simulation
    Input: current state of the simulation \n
    Output: new state of the simulation after a time step
    """

    throttleInput = throttleInputFunction( state.time )
    
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
     """"
     Animates a frame of the simulation onto the graph
     """
     global state
     

     if state.time >= rampThrottleTime + fullThrottleTime: # stop the animation when the simulation is done
        ani.event_source.stop()
        return line,

    #update state
     state = step(state)
     timeTable.append( state.time )
     accelerationTable.append( state.acceleration )

     print("frame", i, "time", state.time, "throttleInput", state.throttleInput, "acceleration", state.acceleration)

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