from .Vector2 import Vector2

class Lem:

    def __init__(self, position: Vector2, mass : float, initial_velocity: Vector2):
        # store position for the module
        self.position = position
        # physics parameters to remenber
        self.currentVelocity = initial_velocity
        self.acceleration = Vector2()
        # thruster in order [L, M, R]
        self.leftThrust = False
        self.mainThrust = False
        self.rightThrust = False
        # and their respectice powers in N
        self.lT_power = Vector2(-30000,0)
        self.mT_power = Vector2(0,47000)
        self.rT_power = Vector2(30000,0)
        # mass of the lander in kilograms
        self.mass = mass

        self.landed = False

    def computeAcceleration(self):

        pass

    def landed(self, landed):
        return landed

    def move(self, deltaT, g):
        # Computes all strenght applying to the module
        sumOfStrength = self.computeStrength()
        # computes the acceleration of the module
        self.acceleration = sumOfStrength / self.mass + g
        # compute the new speed of the module
        self.currentVelocity += self.acceleration * deltaT
        # find the position differential
        deltaPos = self.currentVelocity * deltaT + self.acceleration * .5 * (deltaT **2)
        # update position
        checkLanding(deltaPos)
        if(landing):
            
        else: self.position += deltaPos

    def checkLanding(self, movement):
        pass

    def computeStrength(self):
        # Compute strenght vector according to thrust and rotation
        strengths = []

        if(self.leftThrust):
            strengths.append(self.lT_power)
        if(self.rightThrust):
            strengths.append(self.rT_power)
        if(self.mainThrust):
            strengths.Append(self.mT_power)

        return sum(strengths, Vector2())

    def applyResistance(self, speedVector):
        impactedSpeed = [0,0]
        impactedSpeed[0] = - speedVector[0] / 10 + speedVector[0]
        impactedSpeed[1] = - speedVector[1] / 10 + speedVector[1]
        return impactedSpeed
