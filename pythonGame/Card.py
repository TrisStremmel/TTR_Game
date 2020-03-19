# card class, holds color
class Card:
    def __init__(self, color, length):
        self.color = color
        self.length = length

    def getColor(self):
        return self.color

    def setColor(self, color):
        self.color = color

    def getLength(self):
        return self.length

    def setLength(self, length):
        self.length = length

