import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dataclasses import dataclass
import numpy as np

#constants
maxPropulsion = 2000 #N
vmax = 27 #m/s
mass = 300 #kg


rampThrottleTime = 3 #s
fullThrottleTime = 20 #s

#function parameters for throttle input cubic function
# throttleInput = Ax^3 + Bx^2 + Cx + D
A = -2/27
B = 1/3
C = 0.0
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
    throttleInput: float = 0.0 #0 no acceleration, 1 full acceleration
    time: float = 0.0 #s current time in the simulation
    stepCount: int = 0 #number of steps in the simulation (should remove small errors in time)
       
    velocity: float = 0.0 #m/s current velocity of the car


def step (state:State) -> State:
    """
    Performs a frame of the simulation
    Input: current state of the simulation \n
    Output: new state of the simulation after a time step
    """

    throttleInput = throttleInputFunction( state.time )
    
    #Calculate 
    # Propulsion force = maximum propulsion force * throttle input * (1 - (v/vmax)).
    propulsionForce = maxPropulsion * throttleInput * (1 - (state.velocity/vmax))

    # Force = Mass * acceleration
    acceleration = propulsionForce / mass

    # velocity = velocity + (acceleration * timestep)
    newVelocity = state.velocity + (acceleration * timeStep)

    newStepCount = state.stepCount + 1
    newTime = state.stepCount * timeStep
    return( State( throttleInput=throttleInput, time=state.stepCount * timeStep, stepCount=state.stepCount + 1, velocity=newVelocity ) )

#Starting State
state = State()
timeTable = [state.time]
velocityTable = [state.velocity]
throttleTable = [state.throttleInput]

def animate (i):
     """
     Animates a frame of the simulation onto the graphs
     """
     global state
     

     if state.time >= rampThrottleTime + fullThrottleTime: # stop the animation when the simulation is done
        ani.event_source.stop()
        return throttleLine, velocityLine

    #update state
     state = step(state)
     timeTable.append( state.time )
     velocityTable.append( state.velocity )
     throttleTable.append( state.throttleInput )
     print("frame", i, "time", state.time, "throttleInput", state.throttleInput, "velocity", state.velocity)

    #adding data to graph
     throttleLine.set_data(timeTable, throttleTable)
     velocityLine.set_data(timeTable, velocityTable)
     
     return throttleLine, velocityLine

     
    

# graphing stuff
#Creates two graphs 
fig, (throttleAx, velocityAx) = plt.subplots(2, 1, figsize=(4, 5), dpi=150, sharex=True)
# top graph: throttle input
throttleAx.grid()
throttleAx.set_xlim(-2, 30)
throttleAx.set_ylim(-0.1, 1.1)
throttleAx.set_xlabel("Time (s)")
throttleAx.set_ylabel("Throttle Input")
throttleAx.set_title("Throttle Input")

# bottom graph: velocity
velocityAx.grid()
velocityAx.set_ylim(-2, 100)
velocityAx.set_xlabel("Time (s)")
velocityAx.set_ylabel("Velocity (m/s)")
velocityAx.set_title("Velocity")
# these lines are so the animation doesnt zoom in or out
throttleLine, = throttleAx.plot([], [], color="tab:orange")
velocityLine, = velocityAx.plot([], [], color="tab:blue")

plt.pause(3)
fig.tight_layout() #adjusts graphs so they dont overlap  
#calls animate repeatedly to animate each frame of the simulation
ani = animation.FuncAnimation(fig, animate, interval=0)
plt.show()