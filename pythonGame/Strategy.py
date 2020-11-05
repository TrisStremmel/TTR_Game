from random import randint
import sys
import numpy as np
from copy import deepcopy

stratList = ['commitBlock']

class Strategy:

    def __init__(self, sName=None):
        if sName is None:
            self.strategyName = self.randomStrategy()
        else:
            if sName in stratList:
                self.strategyName = sName
            else:
                self.strategyName = self.randomStrategy()

    def makeDecision(self, state, player):
        if self.strategyName == 'emptyHand':
            return self.emptyHand(state, player)
        if self.strategyName == 'commitBlock':
            return self.commitBlock(state, player)
        return ['pass']

    def emptyHand(self, state, player):

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
        ''' This is the old way which ends up being shortest track not empty hand
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
        '''

        smallestCardDif = 1000000  # python has not int.max_value so this is a sub
        #this for loop is the ai deciding which track it wants
        for i in range(len(edges)):
            #if the edge length is closest to the amount of that color that this player has in their hand
            if edges[i].length - player.handCards.count(edges[i].color) < smallestCardDif:
                smallestCardDif = edges[i].length - player.handCards.count(edges[i].color)
                wanted = edges[i]
                wantedIndex = edgeHash[i]
            elif edges[i].length - player.handCards.count(edges[i].color) == smallestCardDif:
                # if there are multiple shortest tracks it picks one that it has more cards of its color
                if player.handCards.count(edges[i].color) > player.handCards.count(wanted.color):
                    smallestCardDif = edges[i].length - player.handCards.count(edges[i].color)
                    wanted = edges[i]
                    wantedIndex = edgeHash[i]
                elif player.handCards.count(edges[i].color) == player.handCards.count(wanted.color) and randint(0, 1) == 1:  # at random (stretch goal)
                    smallestCardDif = edges[i].length - player.handCards.count(edges[i].color)
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


    def commitBlock(self, state, player):
        if self.strategyName == 'commitBlock':
            UtrackArray = np.array(state.trackArray).copy()
            UtrackCopy = ''
            edgeHash = np.array(np.triu_indices(len(UtrackArray))).T[
                (UtrackArray != -1)[np.triu_indices(len(UtrackArray))]]
            openEdges = [x.occupied == 'False' for x in UtrackArray[tuple(edgeHash.T)]]
            edgeHash = edgeHash[openEdges]
            edges = np.array(state.trackArray)[tuple(edgeHash.T)]
            if len(edges) == 0:
                return ['pass']  # game is actually already over

            tempArray = deepcopy(UtrackArray)
            for i in range(7):
                for j in range(7):
                    if tempArray[i][j] == -1:
                        tempArray[i][j] = -1
                    elif tempArray[i][j].getClaimed() == "False":
                        tempArray[i][j] = tempArray[i][j].length
                    elif player.getName() != tempArray[i][j].getClaimed():
                        tempArray[i][j] = 0
                    else:
                        tempArray[i][j] = -1


            for x in range(len(UtrackArray)):
                for y in range(len(UtrackArray)):
                    if tempArray[x][y] == 0:
                        print(0, end=" ")
                    else:
                        #print(tempArray[x][y], end =" ")
                        continue
                print('')

            print('')

            destinationDeck = [['Washington', 'New York', 20], ['Texas', 'Colorado', 15], ['Montana', 'Texas', 16],
                               ['Washington', 'Oklahoma', 10], ['New York', 'Colorado', 15],
                               ['Washington', 'Kansas', 8],
                               ['Montana', 'Oklahoma', 18], ['Texas', 'Kansas', 9], ['Montana', 'Colorado', 12]]

            cityIndices = {'Washington': 0, 'Montana': 1, 'New York': 2, 'Texas': 3, 'Colorado': 4, 'Kansas': 5,
                           'Oklahoma': 6}

            completionArray = [0]*9
            for x in range(len(destinationDeck)):
                temp = self.dijkstra(destinationDeck[x][0], tempArray)[0]
                completionArray[x] = temp[cityIndices[destinationDeck[x][1]]]
            print(completionArray)

            previousTurn = [7, 6, 8, 5, 7, 5, 8, 5, 5]
            minArray = []
            min = 99
            for x in range(len(completionArray)):
                if completionArray[x] == 0:
                    continue
                elif completionArray[x] < min:
                    minArray.clear()
                    minArray.append(x)
                    min = completionArray[x]
                elif completionArray[x] == min:
                    minArray.append(x)

            print(minArray)

            minDestCost = 0
            minDestIndex = -1
            for x in range(len(minArray)):
                print(minDestCost)
                if destinationDeck[minArray[x]][2] > minDestCost:
                    minDestCost = destinationDeck[minArray[x]][2]
                    minDestIndex = minArray[x]

            print(minDestIndex, " index")
            toClaim = self.dijkstra(destinationDeck[minDestIndex][0], tempArray)[1]
            print(toClaim)
            endCityIndex = cityIndices[destinationDeck[minDestIndex][1]]
            print(endCityIndex, " end city")
            wantedIndexies = []
            finalIndex = endCityIndex
            while(finalIndex != 0):
                wantedIndexies.append(toClaim[finalIndex])
                finalIndex = toClaim[finalIndex][0]
            print(wantedIndexies)

            smallestEdgeLength = 99
            smallestEdge = -1
            wantedIndex = []
            for x in range(len(wantedIndexies)):
                if UtrackArray[wantedIndexies[x][0]][wantedIndexies[x][1]].length < smallestEdgeLength:
                    smallestEdgeLength = UtrackArray[wantedIndexies[x][0]][wantedIndexies[x][1]].length
                    smallestEdge = UtrackArray[wantedIndexies[x][0]][wantedIndexies[x][1]]
                    wantedIndex = [wantedIndexies[x][0],wantedIndexies[x][1]]
            print(smallestEdge, "HERE")
            wanted = smallestEdge
            print(wantedIndex, "BREATH")
            neededCards = []
            for card in player.handCards:
                if card.color == wanted.color:
                    neededCards.append(card)
                if len(neededCards) == wanted.length:  # if you can claim that track do so
                    for toRemove in neededCards:
                        player.handCards.remove(toRemove)
                    player.cardIndex = len(player.handCards)
                    # wantedIndex.reverse()
                    return ['claim', wantedIndex]

            player.addCardToHand(wanted.color)
            if len(neededCards) + 1 == wanted.length:
                colorsAvail = []
                for i in range(0, len(edges)):
                    if edges[i].occupied == 'False' and not colorsAvail.__contains__(edges[i].color):
                        colorsAvail.append(edges[i].color)
                player.addCardToHand(colorsAvail[randint(0, len(colorsAvail) - 1)])  # randomness (stretch goal)
            else:
                player.addCardToHand(wanted.color)
            return ['draw t']

        return 'pass'


    @staticmethod
    def randomStrategy():
        x = randint(0, len(stratList)-1)
        return stratList[x]


    def printSolution(self, dist, city):
        print("Vertex Distance from Source")
        for node in range(7):
            print(city, " to ", node, " takes ", dist[node])

    def minDistance(self, dist, sptSet):

        min = sys.maxsize

        for v in range(7):
            if dist[v] < min and sptSet[v] == False:
                min = dist[v]
                min_index = v

        return min_index

    def dijkstra(self, start, graph):

        cityIndices = {'Washington': 0, 'Montana': 1, 'New York': 2, 'Texas': 3, 'Colorado': 4, 'Kansas': 5,
                       'Oklahoma': 6}
        start = cityIndices[str(start)]

        dist = [sys.maxsize] * 7
        dist[start] = 0
        sptSet = [False] * 7

        toClaimTrack = [0] * 7

        for cout in range(7):

            u = self.minDistance(dist, sptSet)

            sptSet[u] = True

            for v in range(7): #(graph[u][v] != 0) and
                if graph[u][v] >= 0 and sptSet[v] is False and dist[v] > dist[u] + graph[u][v]:
                    dist[v] = dist[u] + graph[u][v]
                    toClaimTrack[v] = [u, v]

        #self.printSolution(dist, start)
        #print(toClaimTrack)
        return [dist, toClaimTrack]


