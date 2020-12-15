import pygame
from pygame.constants import *
from MainWindow import MainWindow
from LanderWindow import LanderWindow

class LanderMenu:

    def __init__(self):
        pygame.init()
        self.buttons = []
        self.selected = 0
        self.window = self.menu()

    def menu(self):
        menuWindow = pygame.display.set_mode((1486,750))
        bg = pygame.image.load(r"img/bgHome.jpg").convert()

        bg = pygame.transform.scale(bg, (int(bg.get_size()[0]*0.8), int(bg.get_size()[1]*0.8)))
        menuWindow.blit(bg, (0,0))
        # buttons
        self.buttons.append(pygame.image.load(r"img/start.png").convert())
        self.buttons.append(pygame.image.load(r"img/ai.png").convert())
        self.buttons.append(pygame.image.load(r"img/exit.png").convert())
        self.buttons.append(pygame.image.load(r"img/startSelected.png").convert())
        self.buttons.append(pygame.image.load(r"img/aiSelected.png").convert())
        self.buttons.append(pygame.image.load(r"img/exitSelected.png").convert())
        for b in self.buttons:
            b = pygame.transform.scale(b, (b.get_size()[0]//2,b.get_size()[1]//2))
        
        #self.drawButtons()
        pygame.display.update()
        return menuWindow

    def launch(self):
        while(True):
            self.drawButtons()
            for event in pygame.event.get():
                # if event is QUIT leave game
                if(event.type == QUIT):
                    pygame.quit()
                # if a key is pressed
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.selected = (self.selected-1)%3
                    if event.key == K_DOWN:
                        self.selected = (self.selected+1)%3

                    if event.key == K_RETURN:
                        if(self.selected == 0):
                            gameWin = MainWindow()
                            gameWin.launch()
                        elif(self.selected == 1):
                            landWin = LanderWindow()
                        else: pygame.quit()

    def drawButtons(self):
        pygame.draw.rect(self.window, (0,0,0), (0,450,1486,500))
        b1 = self.buttons[3] if self.selected == 0 else self.buttons[0]
        b2 = self.buttons[4] if self.selected == 1 else self.buttons[1]
        b3 = self.buttons[5] if self.selected == 2 else self.buttons[2]
        if self.selected == 0:
            self.window.blit(b1, (700-(b1.get_size()[0]//2)-45, 450))
        else:
            self.window.blit(b1, (700-(b1.get_size()[0]//2), 450))
        if self.selected == 1:
            self.window.blit(b2, (700-(b2.get_size()[0]//2)-45, 550))
        else:
            self.window.blit(b2, (700-(b2.get_size()[0]//2), 550))
        if self.selected == 2:
            self.window.blit(b3, (700-(b3.get_size()[0]//2)-45, 650))
        else:
            self.window.blit(b3, (700-(b3.get_size()[0]//2), 650))

        pygame.display.update()

game = LanderMenu()
game.launch()
