from Player import Player
class AI(Player):
    def __init__(self, name):
        Player.__init__(self, name)

    def makeMove(self, state):
        print("AI has not been programed to make a decision yet")
        return 'pass'
