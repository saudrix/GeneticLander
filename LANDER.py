# imports for the GenetirLander project
import pygame
from pygame.locals import *

from src.Lem import *

lem = Lem(Vector2(100,600), 16437, Vector2(0,0))
deltaT = 1 #step time in second
g = Vector2(0,-1.62)#-9.8)

# ===========================================
#                   SETUP                   |
#============================================

pygame.init()
fenetre = pygame.display.set_mode((1280, 720))
bg = pygame.image.load("src/img/bg.png")
bg_size = bg.get_size()
print(bg_size)
bg = pygame.transform.scale(bg, (bg_size[0]*2, bg_size[1]*2))
fenetre.blit(bg, (0,0))

clock = pygame.time.Clock()
fps = 60

#Chargement et collage du personnage
lander = pygame.image.load("src/img/lander.png").convert_alpha()
landerSprite_position = lander.get_rect()
lander_size = lander.get_size()
lander = pygame.transform.scale(lander, (lander_size[0]//2, lander_size[1]//2))
fenetre.blit(lander, (lem.position[0],720-lem.position[1]))
pygame.display.flip()

# ===========================================
#                 GAME LOOP                 |
#============================================

continuer = 1
frame_count = 0
while continuer:
    frame_count += 1
    for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
        # if event is QUIT leave game
        if(event.type == QUIT):
            continuer = 0

        if event.type == KEYDOWN:
            if event.key == K_UP:
                lem.mainThrust = True
            if event.key == K_LEFT:
                lem.rightThrust = True
            if event.key == K_RIGHT:
                lem.leftThrust = True

        if event.type == KEYUP:
            if event.key == K_UP:
                lem.mainThrust = False
            if event.key == K_LEFT:
                lem.rightThrust = False
            if event.key == K_RIGHT:
                lem.leftThrust = False

    clock.tick(fps)
    #if(int(clock.get_fps()) != 0 and frame_count % int(clock.get_fps()) == 0):
    if(lem.position[1] > 0):
        if(int(clock.get_fps()) != 0):
            lem.move(deltaT, g)
        else: lem.move(deltaT, g)
    print(f'pos: {lem.position} | s: ({lem.currentVelocity}) \n')

    #landerSprite_position.move(lem.x-landerSprite_position[0],-lem.y-landerSprite_position[1])
    fenetre.blit(bg, (0,0))
    fenetre.blit(lander, (lem.position[0], 720-lem.position[1]))
    pygame.display.update()
