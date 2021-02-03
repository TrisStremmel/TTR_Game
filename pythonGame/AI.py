import random
import numpy as np

from Card import Card
from Player import Player
from Strategy import Strategy
class AI(Player):
    def __init__(self, name, sName=None):
        Player.__init__(self, name)
        self.strategy = Strategy(sName)
        print(self.name + " follows the " + self.strategy.strategyName + " strategy.")

    def makeMove(self, state):
        decision = self.strategy.makeDecision(state, self)
        return decision


class randomAI(Player):
    def __init__(self, name):
        super().__init__(name)

    def makeMove(self, state):

        UtrackArray = np.array(state.trackArray).copy()
        edgeHash = np.array(np.triu_indices(len(UtrackArray))).T[(UtrackArray != -1)[np.triu_indices(len(UtrackArray))]]
        openEdges = [x.occupied == 'False' for x in UtrackArray[tuple(edgeHash.T)]]
        edgeHash = edgeHash[openEdges]
        numEdges = len(edgeHash)
        if numEdges == 0: return ['pass', None]

        move = random.choices(['draw t', 'claim', 'draw d', 'pass'], [0.0, 1.0, 0.0, 0.0])[0]
        arg = None;
        if move == 'draw t':
            arg = [random.choices([['white', 'white'], ['black', 'black']])]
        elif move == 'claim':
            arg = random.randrange(numEdges)
            arg = edgeHash[arg]

            chosenEdge = state.trackArray[arg[0]][arg[1]]
            if chosenEdge.length > np.sum([x == chosenEdge.color for x in self.getHand()]):
                move = 'draw t'
                arg = [chosenEdge.color, chosenEdge.color]
            else:
                handcolors = np.array([x.color for x in self.handCards])
                tot = []
                opp = handcolors[handcolors != chosenEdge.color].tolist()
                sub = handcolors[handcolors == chosenEdge.color][:-chosenEdge.length].tolist()
                for col in sub: tot.append(col)
                for col in opp: tot.append(col)
                self.handCards = [Card(x) for x in tot]

        if move == 'draw t':
            super().addCardToHand(arg[0])
            super().addCardToHand(arg[1])
        elif move == 'draw d':
            super().addDestCardToHand()

        self.cardIndex = len(self.getHand())
        return [move, arg]

