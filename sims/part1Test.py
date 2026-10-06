maxTorque = 180 #nm
carMass = 300 #kg (with driver)
gearRatio = 3 #3:1
wheelRadius = 0.216 #m

rampThrottleTime = 7 #s
fullThrottleTime = 15 #s

timeStep = 0.01 #s time increments in the simulation

throttleInput = 0.0 #0 no acceleration, 1 full acceleration
time = 0.0 #s current time in the simulation

#tables for simulation graph 
timeTable = []
throttleInputTable = []
accelerationTable = []
while time < rampThrottleTime + fullThrottleTime:

    if(time <= rampThrottleTime): # ramping up throttle input 
        throttleInput = time / rampThrottleTime

    else: #full throttle
        throttleInput = 1.0
    
    #Calculate 
    # Multiply driver input by the maximum motor torque to get command torque (rotational force needed from the motor). 
    commandTorque = throttleInput * maxTorque

    #Force at the wheels = (command torque * gear ratio) / radius of the wheels. 
    wheelForce = (commandTorque * gearRatio) / wheelRadius

    # To find acceleration, use the formula Force = mass * acceleration. a =F/m
    acceleration = wheelForce / carMass

    #Add to tables
    timeTable.append( time )
    throttleInputTable.append( throttleInput )
    accelerationTable.append( acceleration )

    time += timeStep 

print ("Time Table: ", timeTable)
print ("Throttle Input Table: ", throttleInputTable)
print ("Acceleration Table: ", accelerationTable)


