import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dataclasses import dataclass
import numpy as np

#constants
maxBrakeCapacity = 1850 #N
mass = 300 #kg

# rampBrakeTime = 7 #s
# fullBrakeTime = 15 #s

#function parameters for brake input cubic function
# brakeInput = Ax^3 + Bx^2 + Cx + D
A = -2/343
B = 3/49
C = 0.0
D = 0.0


timeStep = 0.01 #s time increments in the simulation




def brakeInputFunction( t:float ) -> float: 
    """
    Input: simulation time \n
    Output: brake input \n
    Handles ramping brake and holding full brake.
    """

    #Brake input improvement
    # # brakeInput = Ax^3 + Bx^2 + Cx + Dx 
    # if(t <= rampBrakeTime): # ramping up brake input
    #     return A * t**3 + B * t**2 + C * t + D
    
    # elif(t <= rampBrakeTime + fullBrakeTime): #full brake
    #     return 1.0
    
    # else: #throw error time went over simulation window
    #     raise ValueError("Time is out of bounds for brake input function")

    if(t <= 2):
        return 0.0
    else: 
        return 1.0

    
    
    

@dataclass
class State:
    brakeInput: float = 0.0 #0 no braking, 1 full braking
    velocity: float = 25.0 #m/s current velocity of the car

    time: float = 0.0 #s current time in the simulation
    stepCount: int = 0 #number of steps in the simulation (should remove small errors in time)
       


def step (state:State) -> State:
    """
    Performs a frame of the simulation
    Input: current state of the simulation \n
    Output: new state of the simulation after a time step
    """

    brakeInput = brakeInputFunction( state.time )
    
    #Calculate 
    #Braking force = driver input * maximum braking capacity 
    brakingForce = brakeInput * maxBrakeCapacity

    #Acceleration = - (braking force/mass) 
    acceleration = - (brakingForce/mass)

    #Velocity = velocity + (acceleration * timestep)
    newVelocity = state.velocity + (acceleration * timeStep)

    if newVelocity < 0: #stop the car if it goes below 0
        newVelocity = 0.0

    
    newStepCount = state.stepCount + 1
    newTime = state.stepCount * timeStep
    return( State( brakeInput=brakeInput, time=newTime, stepCount=newStepCount, velocity=newVelocity ) )

#Starting State
state = State()
timeTable = [state.time]
velocityTable = [state.velocity]
brakeTable = [state.brakeInput]

def animate (i):
     """
     Animates a frame of the simulation onto the graphs
     """
     global state
     

     if state.velocity <= 0: # stop the animation when car stops
        ani.event_source.stop()
        return brakeLine, accelLine

    #update state
     state = step(state)
     timeTable.append( state.time )
     velocityTable.append( state.velocity )
     brakeTable.append( state.brakeInput )
     
     print("frame", i, "time", state.time, "brakeInput", state.brakeInput, "velocity", state.velocity)

    #adding data to graph
     brakeLine.set_data(timeTable, brakeTable)
     accelLine.set_data(timeTable, velocityTable)
     
     return brakeLine, accelLine

     
    

# graphing stuff
#Creates two graphs 
fig, (brakeAx, velocityAx) = plt.subplots(2, 1, figsize=(4, 5), dpi=150, sharex=True)
# top graph: brake input
brakeAx.grid()
brakeAx.set_xlim(-2, 10)
brakeAx.set_ylim(-0.1, 1.1)
brakeAx.set_xlabel("Time (s)")
brakeAx.set_ylabel("Brake Input")
brakeAx.set_title("Brake Input")

# bottom graph: velocity
velocityAx.grid()
velocityAx.set_ylim(-2, 30)
velocityAx.set_xlabel("Time (s)")
velocityAx.set_ylabel("Velocity (m/s)")
velocityAx.set_title("Velocity")
# these lines are so the animation doesnt zoom in or out
brakeLine, = brakeAx.plot([], [], color="tab:orange")
accelLine, = velocityAx.plot([], [], color="tab:blue")

plt.pause(3)
fig.tight_layout() #adjusts graphs so they dont overlap  
#calls animate repeatedly to animate each frame of the simulation
ani = animation.FuncAnimation(fig, animate, interval=0)
plt.show()