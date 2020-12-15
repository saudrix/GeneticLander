import pygame
from .Vector2 import Vector2

class GameObject:

    object = []

    def __init__(self, sprite, pos = Vector2(), boundsSize = Vector2(), boundsOffset = Vector2(), debug = False):
        self.sprite = sprite
        self.pos = Vector2(pos[0],720-pos[1])
        self.size = Vector2(self.sprite.get_size()[0],self.sprite.get_size()[1])
        self.center = self.findCenter(self.sprite, self.pos)
        self.boundsSize = boundsSize
        self.boundsOffset = boundsOffset
        self.bounds = self.createBounds(self.center)

        self.debug = debug
        GameObject.object.append(self)

    def findCenter(self, sprite, pos):
        return self.pos + self.size / 2

    def createBounds(self, center):
        boundsStart = (center - self.boundsSize / 2) + self.boundsOffset
        return pygame.Rect(boundsStart[0], boundsStart[1], self.boundsSize[0], self.boundsSize[1])

    def updatePos(self, pos):
        self.pos = Vector2(pos[0],720-pos[1])
        self.center = self.findCenter(self.sprite, self.pos)
        self.bounds = self.createBounds(self.center)

    def display(self, surface):
        #print(self.sprite)
        #print(self.pos)
        if(self.debug):
            pygame.draw.rect(surface, (255,0,0), self.bounds)
        surface.blit(self.sprite, self.pos.toTuple())

    def collide(self, other):
        if(not isinstance(other,GameObject)): return False
        return self.bounds.colliderect(other.bounds)
