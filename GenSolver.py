from src.GenLander import *
from src.Lem import *

import random
from random import randint

import pygame
from pygame.locals import *

pop_size = 40
chromosome_size = 60
population = []

objective = pygame.Rect(510, 672, 260, 64)
objCollider = pygame.Rect(510, 720-672, 260, 64)
ground = pygame.Rect(0, 680, 1280, 40)
moonCollider = pygame.Rect(0, 720-680, 1280, 40)

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
    lem = Lem(Vector2(100,600), 16437, Vector2(20,-10))
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

def simulateGen(population, surface):
    for chromosome in population:
        data = simRun(chromosome)
        chromosome.score = evaluateRun(data, chromosome)
        drawChromosome(data, surface, chromosome.color)
    return population

def testWin():
    pop = init()
    display = pygame.display.set_mode((1280,720))
    pygame.draw.rect(display, (100,100,100), ground)
    pygame.draw.rect(display, (200,200,200), objective)
    while(pop[0].score != - 1):
        for event in pygame.event.get():
            # if event is QUIT leave game
            if(event.type == QUIT):
                pygame.quit()
        pop = simulateGen(pop, display)
        pop = updatePop(pop)
        display.fill((0,0,0))

def drawChromosome(data, surface, color):
    pygame.draw.rect(surface, (100,100,100), ground)
    pygame.draw.rect(surface, (200,200,200), objective)
    prevPos = Vector2(100,600)
    for pos, speed in data:
        t1 = prevPos.toTuple()
        t2 = pos.toTuple()
        pygame.draw.line(surface, color, (t1[0],720-t1[1]), (t2[0],720-t2[1]))
        prevPos = pos
    pygame.display.update()

def evaluateRun(data, c):
    for result in data:
        status = checkStatus(*result)
        if(status == "LANDED"):
            c.color = (0, 50, 0)
            return -1
        if(status == "CRASHED_MOON"):
            return dist(result[0]) + 20 # turn malus to a variable
            c.color = (50, 0, 0)
        if(status == "CRASHED_ON_SITE"):
            c.color = (0, 0, 50)
            return (result[1] - Vector2(20, 40)).norm()
    else:
        c.color = (50,50,50)
        return dist(result[0])

def checkStatus(pos, speed):
    boundsStart = (pos + lemSize / 2) - lemSize / 2
    lemBounds = pygame.Rect(boundsStart[0], boundsStart[1], lemSize[0], lemSize[1])

    if(lemBounds.colliderect(objCollider) and speed[0] < 20 and speed[1] < 40):
        return("LANDED")
    if(lemBounds.colliderect(objCollider)):
        return("CRASHED_ON_SITE")
    if(lemBounds.colliderect(moonCollider)):
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
