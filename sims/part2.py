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

#function parameters for steering input cubic function
# steeringInput = Ax^3 + Bx^2 + Cx + D
A = -10/27
B = 5/3
C = 0.0
D = 0.0

def steeringInputFunction( t:float ) -> float:
    """
    Input: simulation time \n
    Output: steering input \n
    Handles ramping steering and holding full steering.
    """
    # steeringInput = Ax^3 + Bx^2 + Cx + Dx 
    if(t <= turnSteeringTime): # ramping up steering input
        return A * t**3 + B * t**2 + C * t + D
    
    elif(t <= turnSteeringTime + holdSteeringTime): #hold steering
        return 5.0
    
    else: #throw error time went over simulation window
        raise ValueError("Time is out of bounds for steering input function")

@dataclass
class State:
    steeringInput: float = 0.0 #0 degrees = straight
    time: float = 0.0 #s current time in the simulation

    degSlipAngle: float = 0.0 #in degrees, current slip angle of the car
    lateralVelocity: float = 0.0 #m/s current lateral velocity of the car    
    lateralAcceleration: float = 0.0 #m/s^2 current lateral acceleration of the car
    lateralForce: float = 0.0 #N current lateral force on the car     

def step (state:State) -> State:

    steeringInput = steeringInputFunction(state.time) #0 - 5 degrees for 3 seconds, then hold for 7 seconds

    #convert to radians
    radSteeringInput = steeringInput * math.pi / 180.0

    #Calculate 
    #Slip angle = steer angle - (lateral velocity/forward speed).
    radSlipAngle = radSteeringInput - (state.lateralVelocity / forwardSpeed)
    degSlipAngle = radSlipAngle * 180.0 / math.pi # convert to degrees

    #Lateral force = cornering stiffness * slip angle
    lateralForce = corneringStiffness * radSlipAngle

    #Lateral acceleration = lateral force/mass
    lateralAcceleration = lateralForce / carMass

    #Lateral velocity = lateral velocity(previous) + (lateral acceleration * timestep)
    lateralVelocity = state.lateralVelocity + (lateralAcceleration * timeStep)
   
    newTime = state.time + timeStep

    #Update state
    return( State( 
                steeringInput=steeringInput,
                time=newTime,
                degSlipAngle=degSlipAngle,
                lateralVelocity=lateralVelocity,
                lateralAcceleration=lateralAcceleration,
                lateralForce=lateralForce ) )

#Starting State
state = State()

#Tables for sim graph
timeTable = [state.time]
slipAngleTable = [state.degSlipAngle]
steeringInputTable = [state.steeringInput]

def animate (i):
     global state

     print("frame", i, "time", state.time, "steeringInput", state.steeringInput, "slipAngle", state.degSlipAngle)

     if state.time >= turnSteeringTime + holdSteeringTime: # stop animation when simulation is done
        ani.event_source.stop()
        return steeringLine, slipAngleLine

    #update state
     state = step(state)
     timeTable.append( state.time )
     slipAngleTable.append( state.degSlipAngle )
     steeringInputTable.append( state.steeringInput )

    #adding data to graph
     steeringLine.set_data(timeTable, steeringInputTable)
     slipAngleLine.set_data(timeTable, slipAngleTable)

     return steeringLine, slipAngleLine

     
# graphing stuff

#Creates two graphs 
fig, (steeringAx, slipAngleAx) = plt.subplots(2, 1, figsize=(4, 5), dpi=150, sharex=True)
# top graph: steering input
steeringAx.grid()
steeringAx.set_xlim(-2, 15)
steeringAx.set_ylim(-2, 6)
steeringAx.set_xlabel("Time (s)")
steeringAx.set_ylabel("Steering Input")
steeringAx.set_title("Steering Input")

# bottom graph: slip angle
slipAngleAx.grid()
slipAngleAx.set_ylim(-2, 2)
slipAngleAx.set_xlabel("Time (s)")
slipAngleAx.set_ylabel("Slip Angle (deg)")
slipAngleAx.set_title("Slip Angle")
# these lines are so the animation doesnt zoom in or out
steeringLine, = steeringAx.plot([], [], color="tab:orange")
slipAngleLine, = slipAngleAx.plot([], [], color="tab:blue")

plt.pause(3)
fig.tight_layout() #adjusts graphs so they dont overlap  
#calls animate repeatedly to animate each frame of the simulation
ani = animation.FuncAnimation(fig, animate, interval=0)
plt.show()

# # graphing stuff
# fig = plt.figure(figsize=(3,3), dpi=150)
# ax = fig.add_subplot(111)
# ax.grid()
# ax.set_xlim(-2, 30)
# ax.set_ylim(-2, 10)
# ax.set_xlabel("Time (s)")
# ax.set_ylabel("Slip Angle (deg)")
# # these lines are so the animation doesnt zoom in or out
# line, = ax.plot([], [])

# plt.pause(3)

# #calls animate repeatedly to animate each frame of the simulation
# ani = animation.FuncAnimation(fig, animate, interval=0)
# plt.show()