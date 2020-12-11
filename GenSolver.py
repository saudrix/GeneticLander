from src.GenLander import *
from src.Lem import *

import pygame

pop_size = 40
chromosome_size = 40
population = []

objective = pygame.Rect(510, 672, 260, 64)
ground = pygame.Rect(0, 680, 1280, 40)
lemSize = Vector2(81, 76)

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

def computeSolution():
    pass
