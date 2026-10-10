

Part 1 (Throttle input on acceleration)
    - This part calculates and graphs the acceleration of the car in a straight line as the throttle input increases over time.
    - Throttle input follows: throttle input = -2/343 * time^3 + 3/49 * time^2 for 7 seconds and holds at 100% for 15 seconds
    
-Part 1 test is a simple test program that prints the calculations of part one out so I could check if the logic was right before graphing. It is explained more in depth in my write up.

Part 2 (Steering input on slip angle)
    - This part calculates and graphs the slip angle of the car as steering input is applied
    - Steering input follows: steering input = -10/27 * time^3 + 5/3 * time^2 for 3 seconds and holds 5 degrees for 7 seconds

Part 3 (Drag on car velocity)
    - This part calculates and graphs the velocity of the car as drag slows the car down over time
    - The car is initially accelerated at 5mp/s^2 for 10 seconds. After 10 seconds the car decelerates from drag until it approximates a stop (velocity below 0.3 m/s)

Part 4 (Motor back-EMF resistance on velocity)
    - This part calculates and graphs the top speed the car approaches as back-EMF slows the car down at higher speeds. Set up is similar to part 1
    - Throttle input fullows: throttle input = -2/27 * time^3 + 1/3 time^2 for 3 seconds and holds at 100% for 20 seconds

Part 5 (Braking on velocity)
    - This part calculates and graphs the velocity of the car as braking is applied (0% - 100% instantly in this case, however it is set up like throttle to also be able to accept a function)
    - Holds at 25m/s for 2 seconds and applies 100% braking until velocity = 0
