import math

class Vector2:

    # Vector constructor takes x and y as input
    def __init__(self, x = 0, y = 0):
        self.x = x
        self. y =y

    # creating a representation for the vector
    def __str__(self):
        return(f'Vector2: ({self.x},{self.y})')

    # main operators oveloading
    def __add__(self, o):
        if isinstance(o, self.__class__):
            return Vector2(self.x + o.x, self.y + o.y)
        elif isinstance(o, int) or isinstance(o, float) or isinstance(o, double):
            return Vector2(self.x + o, self.y + o)
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'").format(self.__class__, type(other))

    def __sub__(self, o):
        if isinstance(o, self.__class__):
            return Vector2(self.x - o.x, self.y - o.y)
        elif isinstance(o, int) or isinstance(o, float) or isinstance(o, double):
            return Vector2(self.x - o, self.y - o)
        else:
            raise TypeError("unsupported operand type(s) for -: '{}' and '{}'").format(self.__class__, type(other))

    def __mul__(self, o):
        if isinstance(o, self.__class__):
            return self.norm() * o.norm()
        elif isinstance(o, int) or isinstance(o, float) or isinstance(o, double):
            return Vector2(self.x * o, self.y * o)
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'").format(self.__class__, type(other))

    def __truediv__(self, o):
        if isinstance(o, int) or isinstance(o, float) or isinstance(o, double):
            return Vector2(self.x / o, self.y / o)
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'").format(self.__class__, type(other))

    # comparison operators overloading
    def __gt__(self, o):
        if(self.norm()>o.norm()):
            return True
        else:
            return False

    def __lt__(self, o):
        return not(self > o)

    def __eq__(self, o):
        return(self.x == o.x and self.y ==o.y)

    def __ne__(self, o):
        return not(self == o)

    def __le__(self, o):
        return(self == o or self < o)

    def __ge__(self, o):
        return(self == o or self > o)

    # function that returns the norm of the vector
    def norm(self):
        return(math.sqrt(self.x**2 + self.y**2))