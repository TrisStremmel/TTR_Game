import random
import numpy as np

from Card import Card
from Player import Player


class AI(Player):
    def __init__(self, name):
        Player.__init__(self, name)

    def makeMove(self, state):
        print("AI has not been programed to make a decision yet")
        return ['draw t']


class randomAI(Player):
    def __init__(self, name):
        super().__init__(name)

    def makeMove(self, state):
        print("randomAI uses splash!")

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
            print([x.color for x in self.handCards])
            if chosenEdge.length > len([x == chosenEdge.color for x in self.getHand()]):
                move = 'draw t'
                arg = [chosenEdge.color, chosenEdge.color]
                print(arg)
            else:
                handcolors = np.array([x.color for x in self.handCards])
                opp = handcolors[handcolors != chosenEdge.color].tolist()
                sub = handcolors[handcolors == chosenEdge.color][:-chosenEdge.length]
                for col in sub: opp.append(col)
                self.handCards = [Card(x) for x in opp]

        if move == 'draw t':
            super().addCardToHand(arg[0])
            super().addCardToHand(arg[1])
        elif move == 'draw d':
            super().addDestCardToHand()

        self.cardIndex = len(self.getHand())
        return [move, arg]
