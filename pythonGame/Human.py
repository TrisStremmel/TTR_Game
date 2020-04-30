from Player import Player
#import TTR  # used for make move, I hope that works but there is a back up plan
class Human(Player):
    def __init__(self, name):
        Player.__init__(self, name)

    def makeMove(self):  # gameState, deckArray, event):  # if it no work it will prob be left in anyway but never used
        #gameState = TTR.getHumanMove(gameState, deckArray, event)  # player decision input made from TTR class
        print("player made move")
        # return gameState  # bring back if TTR import is able to work
