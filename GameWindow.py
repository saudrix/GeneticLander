import pygame

class Window:

    def __init__(self, size, frameRate = 60, loop = None, debug = False, name = 'window'):
        pygame.init()
        self.size = size
        self.width = self.size[0]
        self.height = self.size[1]
        self.display = pygame.display.set_mode(self.size.toTuple())
        pygame.display.set_caption(name)

        self.fps = 60
        self.clock = pygame.time.Clock()
        self.gameActions = loop

        self.gameObjects = []
        self.draw()

    def addGO(self, go):
        self.gameObjects.append(go)

    def draw(self):
        for obj in self.gameObjects:
            obj.display(self.display)
        pygame.display.update()
