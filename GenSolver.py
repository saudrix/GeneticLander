from src.GenLander import *
from src.Lem import *

import random
from random import randint

import pygame
from pygame.locals import *

pop_size = 40
chromosome_size = 40
population = []

objective = pygame.Rect(510, 672, 260, 64)
ground = pygame.Rect(0, 680, 1280, 40)
lemSize = Vector2(81, 76)

probMut = 0.01

# create the initial population
def init():
    population = []
    for i in range(0, pop_size):
        c = Chromosome(chromosome_size)
        c.populateRandom()
        population.append(c)
    return population

def simRun(chromosome):
    lem = Lem(Vector2(100,600), 16437, Vector2(0,0))
    pos = [(lem.position,lem.currentVelocity)]
    for gene in chromosome.genes:
        # Update Lem control
        lem.leftThrust = gene.l
        lem.mainThrust = gene.m
        lem.rightThrust = gene.r
        # Apply physics modifications
        lem.move(1, Vector2(0,-1.62))
        # store lem position
        pos.append((lem.position,lem.currentVelocity))
    return pos

def simulateGen(population):
    for chromosome in population:
        chromosome.score = evaluateRun(simRun(chromosome))
    return population

def testWin():
    pop = init()
    display = pygame.display.set_mode((1280,720))
    for c in pop:
        data = simRun(c)
        evaluateRun(data)
        drawChromosome(data,display, (15,15,15))
    while(True):
        for event in pygame.event.get():
            # if event is QUIT leave game
            if(event.type == QUIT):
                pygame.quit()

def drawChromosome(data, surface, color):
    surface.fill((0,0,0))
    prevPos = Vector2(100,600)
    for pos, speed in data:
        t1 = prevPos.toTuple()
        t2 = pos.toTuple()
        pygame.draw.line(surface, color, (t1[0],720-t1[1]), (t2[0],720-t2[1]))
        prevPos = pos
    pygame.display.update()

def evaluateRun(data):
    for result in data:
        status = checkStatus(*result)
        if(status == "LANDED"):
            return -1
        if(status == "CRASHED_MOON"):
            return dist(result[0]) + 20 # turn malus to a variable
        if(status == "CRASHED_ON_SITE"):
            return (result[1] - Vector2(20, 40)).norm()
    else: return dist(result[0])

def checkStatus(pos, speed):
    boundsStart = (pos + lemSize / 2) - lemSize / 2
    lemBounds = pygame.Rect(boundsStart[0], boundsStart[1], lemSize[0], lemSize[1])

    if(lemBounds.colliderect(objective) and speed[0] < 20 and speed[1] < 40):
        return("LANDED")
    if(lemBounds.colliderect(objective)):
        return("CRASHED_ON_SITE")
    if(lemBounds.colliderect(ground)):
        return("CRASHED_MOON")

def dist(pos):
    return min(abs(pos[0]-510),abs(pos[0]-770))

def updatePop(population):
    population = sorted(population, key=lambda c : c.score)
    usedPop = population[:int(len(population)//1.5)]
    newPop = population[:len(population)//3] # Keep the best third of the population
    while(len(newPop) < pop_size):
        # select 2 chromosome
        p1 = random.choice(usedPop)
        p2 = random.choice(usedPop)
        #merge the 2 parents
        newPop.append(mergeChromosomes(p1,p2))

    for c in newPop:
        for g in c.genes:
            p = randint(0,100)/100
            if(p < probMut):
                g.mutate()

    return newPop

def mergeChromosomes(c1,c2):
    c = Chromosome(c1.size)
    for i in range(c.size):
        g1 = c1.genes[i]
        g2 = c2.genes[i]

        g = Gene(g1.l if randint(0,2) else g2.l,
                 g1.m if randint(0,2) else g2.m,
                 g1.r if randint(0,2) else g2.r)
        c.genes.append(g)
    return c

def computeSolution():
    pass
