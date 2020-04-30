class Player:
    def __init__(self, name):
        self.handCards = []
        self.cardIndex = 0;
        self.destinationCards = []
        self.name = name

    def makeMove(self, gameState):
        print("player can not make a decision")

    def getHand(self):
        return self.handCards

    def getCardIndex(self):
        return self.cardIndex

    def getDestCards(self):
        return self.destinationCards

    def getName(self):
        return self.name
