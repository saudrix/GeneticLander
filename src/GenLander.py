from random import randint

class Gene:
    def __init__(self, l=False,m=False,r=False):
        self.l = l
        self.m = m
        self.r = r

    def randomize(self):
        self.l = True if randint(0,2) else False
        self.m = True if randint(0,10) > 6 else False
        self.r = True if randint(0,2) else False

    def mutate(self):
        choice = randint(0,3)
        if choice == 0:
            self.l = not(self.l)
        elif choice == 1:
            self.m = not(self.m)
        elif choice == 2:
            self.r = not(self.r)

    def __repr__(self):
        return(f'l: {self.l} - m: {self.l} - r: {self.r}')

class Chromosome:
    def __init__(self, size = 60):
        self.size = size
        self.genes = []
        self.score = 100000000000
        self.color = (0,0,0)

    def populateRandom(self):
        for i in range(0, self.size):
            g = Gene()
            g.randomize()
            self.genes.append(g)

    def __repr__(self):
        repr = "Chro: "
        for g in self.genes: repr += f"{g} || "
        return repr
