from random import randint

class Strategy:
    def __init__(self, sName=None):
        if sName is None:
            self.strategyName = self.randomStrategy()
        else:
            self.strategyName = sName

    def makeDecision(self, state, player):
        if self.strategyName == 'emptyHand':

            edges = state.getTrackArray()
            wanted = edges[0][0]
            wantedIndex = [0, 0]
            shortestLength = 1000000  # python has not int.max_value so this is a sub
            #this strategy wants to claim the shortest available track or draw cards to try to claim it next turn. This is greedy
            for i in range(0, len(edges)):
                for edge in edges[i]:
                    if type(edge) != int:
                        if edge.occupied == 'False' and edge.length < shortestLength:
                            shortestLength = edge.length
                            wanted = edge
                            wantedIndex = [i, edges[i].index(wanted)]
                        elif edge.occupied == 'False' and edge.length == shortestLength:
                            # if there are multiple shortest tracks it picks one at random (stretch goal)
                            if randint(0, 1) == 1:
                                shortestLength = edge.length
                                wanted = edge
                                wantedIndex = [i, edges[i].index(wanted)]

            neededCards = []
            for card in player.handCards:
                if card.color == wanted.color:
                    neededCards.append(card)
                if len(neededCards) == wanted.length:  # if you can claim that track do so
                    for toRemove in neededCards:
                        player.handCards.remove(toRemove)
                    player.cardIndex = len(player.handCards)
                    print(wantedIndex)
                    return ['claim', wantedIndex]

            player.addCardToHand(wanted.color)
            if len(neededCards)+1 == wanted.length:
                colorsAvail = []
                for i in range(0, len(edges)):
                    for edge in edges[i]:
                        if type(edge) != int:
                            if edge.occupied == 'False' and not colorsAvail.__contains__(edge.color):
                                colorsAvail.append(edge.color)
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
