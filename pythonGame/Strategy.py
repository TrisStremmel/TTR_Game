from random import randint
import numpy as np
class Strategy:
    def __init__(self, sName=None):
        if sName is None:
            self.strategyName = self.randomStrategy()
        else:
            self.strategyName = sName

    def makeDecision(self, state, player):
        if self.strategyName == 'emptyHand':

            UtrackArray = np.array(state.trackArray).copy()
            edgeHash = np.array(np.triu_indices(len(UtrackArray))).T[
                (UtrackArray != -1)[np.triu_indices(len(UtrackArray))]]
            openEdges = [x.occupied == 'False' for x in UtrackArray[tuple(edgeHash.T)]]
            edgeHash = edgeHash[openEdges]
            edges = np.array(state.trackArray)[tuple(edgeHash.T)]
            if len(edges) == 0:
                return ['pass']  # game is actually already over

            wanted = edges[0]
            wantedIndex = [0, 0]
            shortestLength = 1000000  # python has not int.max_value so this is a sub
            #this strategy wants to claim the shortest available track or draw cards to try to claim it next turn. This is greedy
            for i in range(0, len(edges)):
                if edges[i].length < shortestLength:
                    shortestLength = edges[i].length
                    wanted = edges[i]
                    wantedIndex = edgeHash[i]
                elif edges[i].length == shortestLength:
                    # if there are multiple shortest tracks it picks one that it has more cards of its color
                    if player.handCards.count(edges[i].color) > player.handCards.count(wanted.color):
                        shortestLength = edges[i].length
                        wanted = edges[i]
                        wantedIndex = edgeHash[i]
                    elif player.handCards.count(edges[i].color) == player.handCards.count(wanted.color) and randint(0, 1) == 1:  # at random (stretch goal)
                        shortestLength = edges[i].length
                        wanted = edges[i]
                        wantedIndex = edgeHash[i]

            neededCards = []
            for card in player.handCards:
                if card.color == wanted.color:
                    neededCards.append(card)
                if len(neededCards) == wanted.length:  # if you can claim that track do so
                    for toRemove in neededCards:
                        player.handCards.remove(toRemove)
                    player.cardIndex = len(player.handCards)
                    print(wantedIndex)
                    #wantedIndex.reverse()
                    return ['claim', wantedIndex]

            player.addCardToHand(wanted.color)
            if len(neededCards)+1 == wanted.length:
                colorsAvail = []
                for i in range(0, len(edges)):
                    if edges[i].occupied == 'False' and not colorsAvail.__contains__(edges[i].color):
                        colorsAvail.append(edges[i].color)
                player.addCardToHand(colorsAvail[randint(0, len(colorsAvail)-1)])  # randomness (stretch goal)
            else:
                player.addCardToHand(wanted.color)
            return ['draw t']

        return ['pass']

    @staticmethod
    def randomStrategy():
        stratList = ['emptyHand']
        x = randint(0, len(stratList)-1)
        return stratList[x]
