class Edge:

    def __init__(self, length, connection, color):
        self.length = length
        self.occupied = False
        self.connection = connection
        self.color = color

    def getLength(self):
        return self.length

    def setLength(self, length):
        self.length = length

    def getColor(self):
        return self.color

    def setColor(self, color):
        self.occupied = color

    def getConnection(self):
        return self.connection

    def setConnection(self, connection):
        self.connection = connection
