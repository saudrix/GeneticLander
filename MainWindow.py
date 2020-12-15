# imports for the GenetirLander project
import pygame
from pygame.locals import *

import time

from src.Lem import *
from src.GameObject import *
from src.GameWindow import Window

class MainWindow:

    def __init__(self):
        # General physics parameter and lem object
        self.lem = Lem(Vector2(100,600), 16437, Vector2(0,0))
        self.deltaT = 1 #step time in second
        self.g = Vector2(0,-1.62)#-9.8)

        self.window = Window(Vector2(1280, 720))

        self.bgGO = self.createBg()
        self.moonGO = self.createMoon()
        self.baseGO = self.createBase()
        self.lemGO = self.createLemGraphics()

        self.window.addGO(self.bgGO)
        self.window.addGO(self.moonGO)
        self.window.addGO(self.baseGO)
        self.window.addGO(self.lemGO)

    def createBg(self):
        # CREATING THE BACKGROUND GAME OBJECT
        bg = pygame.image.load("src/img/bg.png")
        bg_size = bg.get_size()
        bg = pygame.transform.scale(bg, (bg_size[0]*2, bg_size[1]*2))

        return GameObject(bg, Vector2(0, self.window.height))

    def createMoon(self):
        # CREATING THE MOON GAME OBJECT
        moon = pygame.image.load("src/img/moon.png").convert_alpha()
        moon_size = moon.get_size()
        moon = pygame.transform.scale(moon, (moon_size[0]*5, moon_size[1]*2))
        moon_size = moon.get_size()

        return GameObject(moon, Vector2(0,moon_size[1]), Vector2(moon_size[0],moon_size[1]//2), Vector2(0, moon_size[1]//4))

    def createBase(self):
        # CREATING THE BASE GAME OBJECT
        base = pygame.image.load("src/img/landingBase.png").convert_alpha()
        base_size = base.get_size()

        return GameObject(base, Vector2(640-base_size[0]//2, base_size[1]), Vector2(base_size[0]//1.5, base_size[1]//2), Vector2(0, base_size[1]//2 - 15))

    def createLemGraphics(self):
        # CREATING THE LANDER GAME OBJECT
        lander = pygame.image.load("src/img/lander.png").convert_alpha()
        lander_size = lander.get_size()
        lander = pygame.transform.scale(lander, (lander_size[0]//2, lander_size[1]//2))
        lander_size = lander.get_size()

        return GameObject(lander, Vector2(100,600), Vector2(lander_size[0], lander_size[1]))

    def moveLem(self):
        if(int(self.window.clock.get_fps()) != 0):
            self.lem.move(self.deltaT, self.g)
            self.lem.position.clamp(0, 0-self.lemGO.size[1], 1280-self.lemGO.size[0], 720)
        else:
            self.lem.move(self.deltaT, self.g)
            self.lem.position.clamp(0, 0-self.lemGO.size[1], 1280-self.lemGO.size[0], 720)

    def loose(self):
        pygame.quit()
        lost = Window(Vector2(800,300), name = 'LOST')
        img = pygame.image.load(r"img/loose.png").convert_alpha()
        lost.display.blit(img, (400-(img.get_size()[0]//2), 100))
        pygame.display.update()
        while(True):
            for event in pygame.event.get():
                # if event is QUIT leave game
                if(event.type == QUIT):
                    pygame.quit()

    def win(self):
        pygame.quit()
        win = Window(Vector2(800,300), name = 'WIN')
        img = pygame.image.load(r"img/win.png").convert_alpha()
        win.display.blit(img, (400-(img.get_size()[0]//2), 100))
        pygame.display.update()
        while(True):
            for event in pygame.event.get():
                # if event is QUIT leave game
                if(event.type == QUIT):
                    pygame.quit()

    def launch(self):
        while(True):
            for event in pygame.event.get():
                # if event is QUIT leave game
                if(event.type == QUIT):
                    pygame.quit()
                # if a key is pressed
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.lem.mainThrust = True
                    if event.key == K_LEFT:
                        self.lem.rightThrust = True
                    if event.key == K_RIGHT:
                        self.lem.leftThrust = True
                # if a key is realeased
                if event.type == KEYUP:
                    if event.key == K_UP:
                        self.lem.mainThrust = False
                    if event.key == K_LEFT:
                        self.lem.rightThrust = False
                    if event.key == K_RIGHT:
                        self.lem.leftThrust = False

            # PHYSICS COMPUTATIONS
            for obj in self.window.gameObjects:
                collider = None
                if(self.lemGO.collide(obj) and obj != self.lemGO):
                    collider = obj
                    break

            if(collider != None): # hit detected
                if(collider == self.baseGO): # if we tuch the base
                    self.lem.checkLanding()
                    if(self.lem.landed):
                        self.win()
                    else:
                        self.loose()
                else:
                    self.loose()

            self.moveLem()
            self.lemGO.updatePos(self.lem.position)

            self.window.draw()
