import math


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        '''addiert die Vektoren u und v'''
        return Vector(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        '''addiert die Vektoren u und v'''
        return Vector(self.x-other.x, self.y-other.y)

    def __mul__(self, other):
        '''gib das Skalarproduct von v und w zurueck'''
        return self.x*other.x + self.y*other.y

    def rot90(self):
        '''rotiert den Vektor um 90 Grad gegen den Uhrzeigersinn'''
        return Vector(-self.y, self.x)

    def norm(self):
        '''gib die Laenge von v zurueck'''
        return (self.x**2 + self.y**2)**.5

    def angle(self, other):
        '''gib den Winkel zw. v und w in Radiant zurueck'''
        alpha = math.acos(self.mul(other) / (self.norm()*other.norm()))
        return alpha

    def __repr__(self):
        '''wird automatisch aufgerufen, falls eine
           Stringrepräsentation der Instanz benötigt wird.
           Muss einen String zurück geben.
        '''
        return f'Vec({self.x}, {self.y})'
