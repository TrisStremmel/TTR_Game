class Edge:
    def __init__(self, length, color):
        self.length = length
        self.occupied = 'False'
        self.color = color

    def getLength(self):
        return self.length

    def setLength(self, length):
        self.length = length

    def getColor(self):
        return self.color

    def setColor(self, color):
        self.color = color

    def claim(self, player):
        self.occupied = player.getName()

    def getClaimed(self):
        return self.occupied