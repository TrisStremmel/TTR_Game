from Player import Player
class Human(Player):
    def __init__(self):
        Player.__init__(self)

    def makeMove(self, state):

        print("player can not make a decision")
