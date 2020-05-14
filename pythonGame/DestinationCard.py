# card class, holds two city names and point reward/punishment for connecting/not connecting the two given city names
from random import randint
class DestinationCard:
    def __init__(self, c1, c2, p):
        self.city1 = c1
        self.city2 = c2
        self.points = p

    def getPoints(self):
        return self.points

    def getCity1(self):
        return self.city1

    def getCity2(self):
        return self.city2

    def __eq__(self, obj):
        if type(obj) == DestinationCard:
            if self.city1 != obj.city1:
                return False
            elif self.city2 != obj.city2:
                return False
            elif self.points != obj.points:
                return False
            else:
                return True
        elif type(obj) == list:
            if self.city1 != obj[0]:
                return False
            elif self.city2 != obj[1]:
                return False
            elif self.points != obj[2]:
                return False
            else:
                return True

    @staticmethod
    def drawDestinationCard():
        destinationDeck = [['Washington', 'New York', 10], ['Texas', 'Colorado', 4], ['Montana', 'Texas', 7],
                           ['Washington', 'Oklahoma', 4], ['New York', 'Colorado', 5], ['Washington', 'Kansas', 2],
                           ['Montana', 'Oklahoma', 8], ['Texas', 'Kansas', 3], ['Montana', 'Colorado', 7]]
        randomNum = randint(0, len(destinationDeck)-1)
        return DestinationCard(destinationDeck[randomNum][0], destinationDeck[randomNum][1], destinationDeck[randomNum][2])
