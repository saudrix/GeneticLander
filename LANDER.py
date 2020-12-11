# imports for the GenetirLander project
import pygame
from pygame.locals import *

import time

from src.Lem import *
from src.GameObject import *

from GameWindow import Window

# General physics parameter and lem object
lem = Lem(Vector2(100,600), 16437, Vector2(0,0))
deltaT = 1 #step time in second
g = Vector2(0,-1.62)#-9.8)

# ===========================================
#                   SETUP                   |
#============================================
window = Window(Vector2(1280, 720))

# CREATING THE BACKGROUND GAME OBJECT
bg = pygame.image.load("src/img/bg.png")
bg_size = bg.get_size()
bg = pygame.transform.scale(bg, (bg_size[0]*2, bg_size[1]*2))

bgGO = GameObject(bg, Vector2(0, window.height))

# CREATING THE MOON GAME OBJECT
moon = pygame.image.load("src/img/moon.png").convert_alpha()
moon_size = moon.get_size()
moon = pygame.transform.scale(moon, (moon_size[0]*5, moon_size[1]*2))
moon_size = moon.get_size()

moonGO = GameObject(moon, Vector2(0,moon_size[1]), Vector2(moon_size[0],moon_size[1]//2), Vector2(0, moon_size[1]//4))
print(moonGO.bounds)

# CREATING THE BASE GAME OBJECT
base = pygame.image.load("src/img/landingBase.png").convert_alpha()
base_size = base.get_size()

baseGO = GameObject(base, Vector2(640-base_size[0]//2, base_size[1]), Vector2(base_size[0]//1.5, base_size[1]//2), Vector2(0, base_size[1]//2 - 15))

# CREATING THE LANDER GAME OBJECT
lander = pygame.image.load("src/img/lander.png").convert_alpha()
lander_size = lander.get_size()
lander = pygame.transform.scale(lander, (lander_size[0]//2, lander_size[1]//2))
lander_size = lander.get_size()
print(lander_size)

lemGO = GameObject(lander, Vector2(100,600), Vector2(lander_size[0], lander_size[1]))

window.addGO(bgGO)
window.addGO(moonGO)
window.addGO(baseGO)
window.addGO(lemGO)

def moveLem():
    if(int(window.clock.get_fps()) != 0):
        lem.move(deltaT, g)
        lem.position.clamp(0, 0-lemGO.size[1], 1280-lemGO.size[0], 720)
    else:
        lem.move(deltaT, g)
        lem.position.clamp(0, 0-lemGO.size[1], 1280-lemGO.size[0], 720)

def loose():
    pygame.quit()
    lost = Window(Vector2(300,300), name = 'LOST')
    while(True):
        for event in pygame.event.get():
            # if event is QUIT leave game
            if(event.type == QUIT):
                pygame.quit()

def win():
    pygame.quit()
    win = Window(Vector2(300,300), name = 'WIN')
    while(True):
        for event in pygame.event.get():
            # if event is QUIT leave game
            if(event.type == QUIT):
                pygame.quit()


# ===========================================
#                 GAME LOOP                 |
#============================================
while(True):
    for event in pygame.event.get():
        # if event is QUIT leave game
        if(event.type == QUIT):
            self.display.quit()
            pygame.quit()
        # if a key is pressed
        if event.type == KEYDOWN:
            if event.key == K_UP:
                lem.mainThrust = True
            if event.key == K_LEFT:
                lem.rightThrust = True
            if event.key == K_RIGHT:
                lem.leftThrust = True
        # if a key is realeased
        if event.type == KEYUP:
            if event.key == K_UP:
                lem.mainThrust = False
            if event.key == K_LEFT:
                lem.rightThrust = False
            if event.key == K_RIGHT:
                lem.leftThrust = False

    # PHYSICS COMPUTATIONS
    for obj in window.gameObjects:
        collider = None
        if(lemGO.collide(obj) and obj != lemGO):
            collider = obj
            break

    if(collider != None): # hit detected
        if(collider == baseGO): # if we tuch the base
            lem.checkLanding()
            if(lem.landed):
                win()
            else:
                loose()
        else:
            loose()

    moveLem()
    lemGO.updatePos(lem.position)
    print(collider)

    window.draw()
