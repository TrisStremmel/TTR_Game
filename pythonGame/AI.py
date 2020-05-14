from Player import Player
from Strategy import Strategy
class AI(Player):
    def __init__(self, name):
        Player.__init__(self, name)
        self.strategy = Strategy()
        print(self.name + " follows the " + self.strategy.strategyName + " strategy.")

    def makeMove(self, state):
        decision = self.strategy.makeDecision(state, self)
        print(self.handCards)
        return decision
