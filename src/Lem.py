from .Vector2 import Vector2

class Lem:

    def __init__(self, start_x, start_y, mass, initial_velocity):
        # store position for the module
        self.x = start_x
        self.y = start_y
        # physics parameters to remenber
        self.currentVelocity = initial_velocity
        self.acceleration = 0
        # thruster in order [L, M, R]
        self.leftThrust = False
        self.mainThrust = False
        self.rightThrust = False
        self.thrust = [0,0,0]
        # mass of the lander in kilograms
        self.mass = mass

    def computeAcceleration(self):

        pass

    def landed(self, landed):
        return landed

    def move(self, deltaT, g):
        # Computes all strenght applying to the module
        strength = self.computeStrength()

        xComponent = sum([s[0] for s in strength])
        yComponent = sum([s[1] for s in strength])
        # computes the acceleration of the module
        self.acceleration = (xComponent / self.mass + g[0], yComponent / self.mass + g[1])
        # compute the speed of the module
        new_speed = [0,0]
        new_speed[0] = self.currentVelocity[0] + self.acceleration[0] * deltaT
        new_speed[1] = self.currentVelocity[1] + self.acceleration[1] * deltaT

        deltaX = self.currentVelocity[0] * deltaT + .5 * self.acceleration[0] * deltaT**2
        deltaY = self.currentVelocity[1] * deltaT + .5 * self.acceleration[1] * deltaT**2

        # update velocity and position
        self.currentVelocity[0] = new_speed[0]
        self.currentVelocity[1] = new_speed[1]

        self.currentVelocity = self.applyResistance(self.currentVelocity)

        self.x += deltaX
        self.y += deltaY

    def computeStrength(self):
        # Compute strenght vector according to thrust and rotation
        strenght1 =  [-self.thrust[0], 0]
        strenght2 =  [0 ,self.thrust[1]]
        strenght3 =  [self.thrust[2], 0]

        return [strenght1, strenght2, strenght3]

    def stabilyze(self):
        for i in range(0, len(self.thrust)):
            if(self.thrust[i] > 0): self.thrust[i] -= 500

    def applyResistance(self, speedVector):
        impactedSpeed = [0,0]
        impactedSpeed[0] = - speedVector[0] / 10 + speedVector[0]
        impactedSpeed[1] = - speedVector[1] / 10 + speedVector[1]
        return impactedSpeed
