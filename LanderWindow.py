from src.GenLander import *
from src.Lem import *

import random
from random import randint

import pygame
from pygame.locals import *

import time
import MainWindow

class LanderWindow:

    def __init__(self):
        self.pop_size = 40
        self.chromosome_size = 60
        self.population = []
        # Collisions
        self.objective = pygame.Rect(510, 672, 260, 64)
        self.objCollider = pygame.Rect(550, 720-672, 200, 64)
        self.ground = pygame.Rect(0, 680, 1280, 40)
        self.moonCollider = pygame.Rect(0, 720-680, 1280, 70)
        self.lemSize = Vector2(81, 76)

        self.probMut = 0.01
        self.initGraphics()
        self.testWin()

    # create the initial self.population
    def init(self):
        self.population = []
        for i in range(0, self.pop_size):
            c = Chromosome(self.chromosome_size)
            c.populateRandom()
            self.population.append(c)
        return self.population

    def simRun(self,chromosome):
        lem = Lem(Vector2(100,600), 16437, Vector2(40,-10))#, Vector2(20,-10))
        data = [(lem.position,lem.currentVelocity)]
        for gene in chromosome.genes:
            # Update Lem control
            lem.leftThrust = gene.l
            lem.mainThrust = gene.m
            lem.rightThrust = gene.r
            # Apply physics modifications
            lem.move(1, Vector2(0,-1.62))
            # store lem position
            data.append((lem.position,lem.currentVelocity))
        return data

    def simulateGen(self, surface):
        for chromosome in self.population:
            data = self.simRun(chromosome)
            chromosome.score = self.evaluateRun(data, chromosome)
            self.drawChromosome(data, surface, chromosome.color)
        return self.population

    def showResults(self, data):
        display = pygame.display.set_mode((1280,720))
        lander = pygame.image.load("src/img/lander.png").convert_alpha()
        lander_size = lander.get_size()
        lander = pygame.transform.scale(lander, (lander_size[0]//2, lander_size[1]//2))

        cpt = 0
        p = data[cpt][0]
        self.drawBG(display)
        while(True):
            for event in pygame.event.get():
            # if event is QUIT leave game
                if(event.type == QUIT):
                    pygame.quit()
                if event.type == KEYDOWN:
                    if event.key == K_q:
                        pygame.quit()
                    if event.key == K_f:
                        pygame.quit()
                        gameWin = MainWindow.MainWindow()
                        gameWin.launch()
                    if event.key == K_m:
                        pygame.quit()

            if(self.checkStatus(p, Vector2(0,0)) == "LANDED"):
                 text = pygame.image.load(r"img/aiText.png").convert_alpha()
                 inst = pygame.image.load(r"img/instructionLarge.png").convert_alpha()
                 display.blit(text, (600-(text.get_size()[0]//2), 100))
                 display.blit(inst, (600-(inst.get_size()[0]//2), 300))
                 pygame.display.update()
            else:
                self.drawBG(display)
                display.blit(lander, (p[0],720-p[1]))
                pygame.display.update()
                cpt+=1
                p = data[cpt][0]



    def testWin(self):
        pop = self.init()
        display = pygame.display.set_mode((1280,720))
        #pygame.draw.rect(display, (100,100,100), self.ground)
        #pygame.draw.rect(display, (200,200,200), self.objective)
        self.drawBG(display)
        while(True):
            if(pop[0].score == -1):
                break
            else:
                for event in pygame.event.get():
                # if event is QUIT leave game
                    if(event.type == QUIT):
                        pygame.quit()
                pop = self.simulateGen(display)
                pop = self.updatePop()
                #display.fill((0,0,0))
                self.drawBG(display)
        self.drawBG(display)
        result = self.simRun(self.population[0])
        self.showResults(result)

    def drawBG(self, display):
        display.blit(self.bg, (0,0))
        display.blit(self.moon, (0,640))
        display.blit(self.base,(445,591))
        pygame.display.update()

    def initGraphics(self):
        bg = pygame.image.load("src/img/bg.png")
        bg_size = bg.get_size()
        self.bg = pygame.transform.scale(bg, (bg_size[0]*2, bg_size[1]*2))

        moon = pygame.image.load("src/img/moon.png").convert_alpha()
        moon_size = moon.get_size()
        self.moon = pygame.transform.scale(moon, (moon_size[0]*5, moon_size[1]*2))

        self.base = pygame.image.load("src/img/landingBase.png").convert_alpha()

    def drawChromosome(self, data, surface, color):
        #pygame.draw.rect(surface, (100,100,100), self.ground)
        #pygame.draw.rect(surface, (0,0,255), self.moonCollider)
        #pygame.draw.rect(surface, (0,255,0), self.objCollider)
        #pygame.draw.rect(surface, (255,0,0), self.objective)
        prevPos = Vector2(100,600)
        for pos, speed in data:
            t1 = prevPos.toTuple()
            t2 = pos.toTuple()
            pygame.draw.line(surface, color, (t1[0],720-t1[1]), (t2[0],720-t2[1]))
            prevPos = pos
        pygame.display.update()

    def evaluateRun(self, data, c):
        for result in data:
            status = self.checkStatus(*result)
            if(status == "LANDED"):
                c.color = (0, 150, 0)
                return -1
            elif(status == "CRASHED_MOON"):
                c.color = (150, 0, 0)
                return self.dist(result[0]) + 20 # turn malus to a variable
            elif(status == "CRASHED_ON_SITE"):
                c.color = (0, 0, 150)
                return (result[1] - Vector2(20, 40)).norm()
        else:
            c.color = (150,150,150)
            return self.dist(result[0])

    def checkStatus(self, pos, speed):
        boundsStart = (pos + self.lemSize / 2) - self.lemSize / 2
        lemBounds = pygame.Rect(boundsStart[0], boundsStart[1], self.lemSize[0], self.lemSize[1])

        if(lemBounds.colliderect(self.objCollider) and speed[0] < 20 and speed[1] < 40):
            return("LANDED")
        if(lemBounds.colliderect(self.objCollider)):
            return("CRASHED_ON_SITE")
        if(lemBounds.colliderect(self.moonCollider)):
            return("CRASHED_MOON")

    def dist(self, pos):
        return min(abs(pos[0]-510),abs(pos[0]-770))

    def updatePop(self):
        self.population = sorted(self.population, key=lambda c : c.score)
        usedPop = self.population[:int(len(self.population)//1.5)]
        newPop = self.population[:len(self.population)//3] # Keep the best third of the self.population
        while(len(newPop) < self.pop_size):
            # select 2 chromosome
            p1 = random.choice(usedPop)
            p2 = random.choice(usedPop)
            #merge the 2 parents
            newPop.append(self.mergeChromosomes(p1,p2))

        for c in newPop:
            for g in c.genes:
                p = randint(0,100)/100
                if(p < self.probMut):
                    g.mutate()

        return newPop

    def mergeChromosomes(self, c1,c2):
        c = Chromosome(c1.size)
        for i in range(c.size):
            g1 = c1.genes[i]
            g2 = c2.genes[i]

            g = Gene(g1.l if randint(0,2) else g2.l,
                     g1.m if randint(0,2) else g2.m,
                     g1.r if randint(0,2) else g2.r)
            c.genes.append(g)
        return c
