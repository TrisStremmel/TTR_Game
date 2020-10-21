# card class, holds two city names and point reward/punishment for connecting/not connecting the two given city names
from random import randint
import numpy as np

class DestinationCard:
    def __init__(self, c1, c2, p):
        self.city1 = c1
        self.city2 = c2
        self.points = p
        self.completed = False

    def __eq__(self, obj):
        if type(obj) == DestinationCard:
            if self.city1 != obj.city1: return False
            elif self.city2 != obj.city2: return False
            elif self.points != obj.points: return False
            else: return True
        elif type(obj) == list:
            if self.city1 != obj[0]: return False
            elif self.city2 != obj[1]: return False
            elif self.points != obj[2]: return False
            else: return True

    def getPoints(self):
        return self.points

    def getCity1(self):
        return self.city1

    def getCity2(self):
        return self.city2

    def getValues(self):
        return [self.city1, self.city2, self.points]

    def toString(self):
        return self.city1 + "->" + self.city2

    @staticmethod
    def drawDestinationCard():
        destinationDeck = [['Washington', 'New York', 20], ['Texas', 'Colorado', 15], ['Montana', 'Texas', 16],
                           ['Washington', 'Oklahoma', 10], ['New York', 'Colorado', 15], ['Washington', 'Kansas', 8],
                           ['Montana', 'Oklahoma', 18], ['Texas', 'Kansas', 9], ['Montana', 'Colorado', 12]]
        randomNum = randint(0, len(destinationDeck)-1)
        return DestinationCard(destinationDeck[randomNum][0], destinationDeck[randomNum][1], destinationDeck[randomNum][2])

    @staticmethod
    def getDestinationDeck():
        return np.array([['Washington', 'New York', 20], ['Texas', 'Colorado', 15], ['Montana', 'Texas', 16],
                           ['Washington', 'Oklahoma', 10], ['New York', 'Colorado', 15], ['Washington', 'Kansas', 8],
                           ['Montana', 'Oklahoma', 18], ['Texas', 'Kansas', 9], ['Montana', 'Colorado', 12]])
