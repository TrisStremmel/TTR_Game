from random import randint
import sys
import numpy as np
from copy import deepcopy
from DestinationCard import DestinationCard

# when you update stratList here make sure to also update it in TTR.py (its early)
stratList = ['emptyHand', 'readBlock', 'blindDestination', 'longestFirst']
destinationDeck = [['Washington', 'New York', 20], ['Texas', 'Colorado', 15], ['Montana', 'Texas', 16],
                   ['Washington', 'Oklahoma', 10], ['New York', 'Colorado', 15], ['Washington', 'Kansas', 8],
                   ['Montana', 'Oklahoma', 18], ['Texas', 'Kansas', 9], ['Montana', 'Colorado', 12]]

cityIndices = {'Washington': 0, 'Montana': 1, 'New York': 2, 'Texas': 3, 'Colorado': 4, 'Kansas': 5, 'Oklahoma': 6}

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
        #next line is cool huh. it calls self.strategyNameFunction(state. player), it works cuz self.strategyName is the
        #exact name of the method for that strat. for ex it would call self.emptyHand(state, player)
        return getattr(self, self.strategyName)(state, player)

    def pickyConductor(self, state, player):
        ## Look at what tracks are claimed as well as who has claimed them.
        UtrackArray = np.array(state.trackArray).copy()  # 2d array that represents the adj matrix that is the game board
        edgeHash = np.array(np.triu_indices(len(UtrackArray))).T[
            (UtrackArray != -1)[np.triu_indices(len(UtrackArray))]]
        openEdges = [x.occupied == 'False' for x in UtrackArray[tuple(edgeHash.T)]]
        edgeHash = edgeHash[openEdges]
        edges = np.array(state.trackArray)[tuple(edgeHash.T)]
        if len(edges) == 0:
            return ['pass']  # game is actually already over

        wanted = UtrackArray[0][0]
        wantedIndex = [0, 0]
        wantedIndexes = []

        ## Check to see if there is a destination card in hand that is not completed

        tempArray = deepcopy(UtrackArray)
        for i in range(len(tempArray)):
            for j in range(len(tempArray)):
                if tempArray[i][j] == -1:
                    tempArray[i][j] = -1
                elif tempArray[i][j].getClaimed() == "False":
                    tempArray[i][j] = tempArray[i][j].length
                elif player.getName() == tempArray[i][j].getClaimed():
                    tempArray[i][j] = 0
                else:
                    tempArray[i][j] = -1
        # tempArray is an adj matrix with -1s where there is no edge (or an edge claimed by other player)
        # and 0 if this player has claimed that edge or the length of that edge if that edge is unclaimed

        targetDCard = None
        for dCard in player.destinationCards:  # looks at all the dest cards in its hand
            if not dCard.completed:  # only looks at the ones it has not completed
                fullInfo = self.dijkstra(dCard.city1, tempArray)
                distTo = fullInfo[0]
                ## and can be completed.
                if distTo[cityIndices[dCard.city2]] > 99:
                    # if dist to the 2nd city in the dCard is over 99 then it is impossible to complete that dCard
                    # so it it stops looking at it
                    continue

                else:
                    targetDCard = dCard
                    break

        ## if no
        ## If it is still possible to complete a remaining dest card
        if targetDCard is None:  # if there are no destcards in its hand that it can complete
            # checks to make sure it it possible to complete ANY remaining destCards, if not it follows
            # the emptyhand strat, if there is a destcard it can complete it draws another dest card.
            possibleCompletionArray = []  # [0] * 9
            for x in range(len(destinationDeck)):
                skip = False
                for card in player.destinationCards:
                    if destinationDeck[x] == card.getValues:
                        skip = True
                        break
                # if all(destinationDeck[x].getValues == card.getValues for card in player.destinationCards):
                if skip:  # dont add any already completed dest card to possible completion array
                    continue
                temp = self.dijkstra(destinationDeck[x][0], tempArray)[0]
                # possibleCompletionArray[x] = temp[cityIndices[destinationDeck[x][1]]]
                possibleCompletionArray.append(temp[cityIndices[destinationDeck[x][1]]])

            # the completionArray holds values equal to how close the AI is to completing each of the destination cards
            # for example if completionArray[1] = 3 then it is only 3 track lengths away from completing
            # the destination card from texas to colorado

            print("completionArray", possibleCompletionArray)
            if all(x >= 99 for x in possibleCompletionArray):  # if it is impossible to complete ANY dest cards
                print("No destination cards left so it now follows empty hand strategy to avoid errors")
                ## Else: follow empty hand
                return self.emptyHand(state, player)
            else:
                ## draw a new destination card
                player.addDestCardToHand()
                return ['draw d']


        ## If yes: Survey the game board and use Dijkstra to find the shortest track corresponding to the destination card.

        print("targetDCard ", targetDCard.toString())
        '''dijkstraResult = self.dijkstra(cityIndices[targetDCard.city1], tempArray)
        distance = dijkstraResult[0][cityIndices[targetDCard.city2]]'''
        # Run dijkstra to find the shortest path to complete the target destCard
        toClaim = self.dijkstra(cityIndices[targetDCard.city1], tempArray)[1]
        # toClaim is the toClaimTrack array returned by dijkstra when run starting from the first city on the
        # target destination

        wantedIndexes = []
        finalIndex = cityIndices[targetDCard.city2]

        for x in range(len(toClaim)):  # for loop makes it so the while loop bellow does not break
            if toClaim[x] == 0:
                toClaim[x] = -1
        print("toClaim", toClaim)

        while finalIndex != -1 and toClaim[
            finalIndex] != -1:  # type(finalIndex) != int and type(toClaim[finalIndex]) != int:#
            # print("Final index", finalIndex)
            checkIndex = deepcopy(toClaim[finalIndex])
            if checkIndex[0] > checkIndex[1]:
                checkIndex[0], checkIndex[1] = checkIndex[1], checkIndex[0]
            '''print("checkIndex", checkIndex)
            print("UtrackArray[checkIndex[0]][checkIndex[1]].occupied", UtrackArray[checkIndex[0]][checkIndex[1]].occupied)'''

            if UtrackArray[checkIndex[0]][checkIndex[1]].occupied == 'False':
                wantedIndexes.append(toClaim[finalIndex])
                '''if toClaim[finalIndex] == 0:
                    break'''
            finalIndex = toClaim[finalIndex][0]
        # this while loop works backwards, starting from the 2nd city in the target dest card, and adds every edge
        # along the most direct path between the 2nd city of the target dest card and the 1st city in the target dest
        # card to an array called wantedIndexes. The strategy wants to claim these tracks because they are the
        # tracks along the shortest path which allows it to complete its target Destination card


        ##once it has the shortest path make a list of all the cards it will need to complete that path
        neededCards = []
        for track in wantedIndexes:
            currentTrack = UtrackArray[track[0]][track[1]]
            for i in range(0, currentTrack.lenght):
                neededCards.append(currentTrack.color)

        #remove cards in hand from neededCards (you dont need cards that you already have)
        #########################^

        ##check if it already has all of the cards in that list
        #can by looking at neededCards after removing the ones you have (if its empty then you have all you need)
        if len(neededCards) == 0:
            ## claim shortest track along that shortest path
            wanted = UtrackArray[wantedIndexes[0][0]][wantedIndexes[0][1]]
            wantedIndex = []
            shortestLength = 99
            for i in range(0, len(wantedIndexes)):
                currentEdge = UtrackArray[wantedIndexes[i][0]][wantedIndexes[i][1]]
                if currentEdge.length < shortestLength:
                    shortestLength = currentEdge.length
                    wanted = currentEdge
                    wantedIndex = wantedIndexes[i]

            toDrawCards = []
            for card in player.handCards:
                if card.color == wanted.color:
                    toDrawCards.append(card)

            for toRemove in toDrawCards:
                player.handCards.remove(toRemove)
            player.cardIndex = len(player.handCards)  # prob useless if I had to guess
            # wantedIndex.reverse()
            if wantedIndex[0] > wantedIndex[1]:
                wantedIndex[0], wantedIndex[1] = wantedIndex[1], wantedIndex[0]
            return ['claim', wantedIndex]
        else:
            ## Else if AI does not have correct cards to claim all tracks
            ## Draw from needed cards
            player.addCardToHand(neededCards[0].color)
            if len(neededCards) == 1:
                player.addCardToHand('neededCards[1].color')
                #######################^
            else:
                player.addCardToHand(neededCards[1].color)

        return ['draw t']

        '''
        wanted = UtrackArray[wantedIndexes[0][0]][wantedIndexes[0][1]]
        wantedIndex = []
        shortestLength = 99
        for i in range(0, len(wantedIndexes)):
            currentEdge = UtrackArray[wantedIndexes[i][0]][wantedIndexes[i][1]]
            if currentEdge.length < shortestLength:
                shortestLength = currentEdge.length
                wanted = currentEdge
                wantedIndex = wantedIndexes[i]

        neededCards = []
        for card in player.handCards:
            if card.color == wanted.color:
                neededCards.append(card)
                
        for toRemove in neededCards:
                player.handCards.remove(toRemove)
            player.cardIndex = len(player.handCards)  # prob useless if I had to guess
            # wantedIndex.reverse()
            if wantedIndex[0] > wantedIndex[1]:
                wantedIndex[0], wantedIndex[1] = wantedIndex[1], wantedIndex[0]
            return ['claim', wantedIndex]
            
        player.addCardToHand(wanted.color)  
        if len(neededCards) + 1 == wanted.length:  # if the ai only needed one card to claim the track it wants
            # then it draws a color of another track it needs along the shortest path
            colorsAvail = []
            for i in range(0, len(edges)):
                if edges[i].occupied == 'False' and not colorsAvail.__contains__(edges[i].color):
                    colorsAvail.append(edges[i].color)
            wantedColor = colorsAvail[randint(0, len(colorsAvail) - 1)]  # randomness (stretch goal)

            colorsAlongPath = []
            for i in range(len(wantedIndexes)):
                if wantedIndexes[i] != wantedIndex:
                    edge = wantedIndexes[i]
                    if not colorsAlongPath.__contains__(UtrackArray[edge[0]][edge[1]].color):
                        colorsAlongPath.append(UtrackArray[edge[0]][edge[1]].color)
            if len(colorsAlongPath) != 0:
                wantedColor = colorsAlongPath[randint(0, len(colorsAlongPath) - 1)]

            player.addCardToHand(wantedColor)

        else:  # if it needs more then one more: draw a 2nd card of the color of the track it wants
            player.addCardToHand(wanted.color)  '''

    def ironEmpire(self, state, player):
        ## Assess the game board
        UtrackArray = np.array(state.trackArray).copy()
        edgeHash = np.array(np.triu_indices(len(UtrackArray))).T[
            (UtrackArray != -1)[np.triu_indices(len(UtrackArray))]]
        openEdges = [x.occupied == 'False' for x in UtrackArray[tuple(edgeHash.T)]]
        edgeHash = edgeHash[openEdges]
        edges = np.array(state.trackArray)[tuple(edgeHash.T)]
        if len(edges) == 0:
            return ['pass']  # game is actually already over
        '''elif not len(player.handCards) == 14 and len(edges) == 10:  # aka no edges have been claimed
            #the AI wants to draw cards until the other player claims a track, because its bad to guess what the other
            #player is trying to complete before they have even claimed a track
            player.addCardToHand('black')
            player.addCardToHand('white')
            return ['draw t']'''

        wanted = UtrackArray[0][1]
        wantedIndex = [0, 1]
        wantedIndexes = []


        ## If you can claim 1 of the tracks



        ## Claim the track
        neededCards = []
        for card in player.handCards:
            if card.color == wanted.color:
                neededCards.append(card)
            if len(neededCards) == wanted.length:  # if you can claim that track do so
                for toRemove in neededCards:
                    player.handCards.remove(toRemove)
                player.cardIndex = len(player.handCards)  # prob useless if I had to guess
                # wantedIndex.reverse()
                if wantedIndex[0] > wantedIndex[1]:
                    wantedIndex[0], wantedIndex[1] = wantedIndex[1], wantedIndex[0]
                return ['claim', wantedIndex]

        ## If not: Draw cards for 1 of them, beginning with the track with the lowest weight
        player.addCardToHand(wanted.color)
        if len(neededCards) + 1 == wanted.length:  # if the ai only needed one card to claim the track it wants
            # then it draws a color of another track it needs of the other incoming tracks to the city it wants to block
            colorsAvail = []
            for i in range(0, len(edges)):
                if edges[i].occupied == 'False' and not colorsAvail.__contains__(edges[i].color):
                    colorsAvail.append(edges[i].color)
            wantedColor = colorsAvail[randint(0, len(colorsAvail) - 1)]  # randomness (stretch goal)

            colorsAlongPath = []
            for i in range(len(wantedIndexes)):
                if wantedIndexes[i] != wantedIndex:
                    edge = wantedIndexes[i]
                    if not colorsAlongPath.__contains__(UtrackArray[edge[0]][edge[1]].color):
                        colorsAlongPath.append(UtrackArray[edge[0]][edge[1]].color)
            if len(colorsAlongPath) != 0:
                wantedColor = colorsAlongPath[randint(0, len(colorsAlongPath) - 1)]

            player.addCardToHand(wantedColor)

        else:  # if it needs more then one more: draw a 2nd card of the color of the track it wants
            player.addCardToHand(wanted.color)  ## Draw cards of the color of that track

        return ['draw t']

    def longestFirst(self, state, player):
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

        longestLength = 0
        #this strategy wants to claim the longest available track or draw cards to try to claim it next turn.
        # This is greedy
        for i in range(0, len(edges)):
            if edges[i].length > longestLength:
                longestLength = edges[i].length
                wanted = edges[i]
                wantedIndex = edgeHash[i]
            elif edges[i].length == longestLength:
                # if there are multiple longest tracks it picks one that it has more cards of its color
                if player.handCards.count(edges[i].color) > player.handCards.count(wanted.color):
                    longestLength = edges[i].length
                    wanted = edges[i]
                    wantedIndex = edgeHash[i]
                elif player.handCards.count(edges[i].color) == player.handCards.count(wanted.color) and randint(0, 1) == 1:  # at random (stretch goal)
                    longestLength = edges[i].length
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
                # wantedIndex.reverse()
                return ['claim', wantedIndex.tolist()]

        player.addCardToHand(wanted.color)
        if len(neededCards) + 1 == wanted.length:  # if the ai only needed one card to claim the track it wants
            # then the 2nd card its draws will be random
            colorsAvail = []
            for i in range(0, len(edges)):
                if edges[i].occupied == 'False' and not colorsAvail.__contains__(edges[i].color):
                    colorsAvail.append(edges[i].color)
            player.addCardToHand(colorsAvail[randint(0, len(colorsAvail) - 1)])  # randomness (stretch goal)
        else:
            player.addCardToHand(wanted.color)
        return ['draw t']


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
                return ['claim', wantedIndex.tolist()]

        player.addCardToHand(wanted.color)
        if len(neededCards)+1 == wanted.length:  # if the ai only needed one card to claim the track it wants
            # then the 2nd card its draws will be random
            colorsAvail = []
            for i in range(0, len(edges)):
                if edges[i].occupied == 'False' and not colorsAvail.__contains__(edges[i].color):
                    colorsAvail.append(edges[i].color)
            player.addCardToHand(colorsAvail[randint(0, len(colorsAvail)-1)])  # randomness (stretch goal)
        else:
            player.addCardToHand(wanted.color)
        return ['draw t']


    def readBlock(self, state, player):
        otherPlayer = 'playerOne' if player.name == 'playerTwo' else 'playerTwo'

        UtrackArray = np.array(state.trackArray).copy()  # can i deepcopy?
        UtrackCopy = ''
        edgeHash = np.array(np.triu_indices(len(UtrackArray))).T[
            (UtrackArray != -1)[np.triu_indices(len(UtrackArray))]]
        openEdges = [x.occupied == 'False' for x in UtrackArray[tuple(edgeHash.T)]]
        edgeHash = edgeHash[openEdges]
        edges = np.array(state.trackArray)[tuple(edgeHash.T)]
        if len(edges) == 0:
            return ['pass']  # game is actually already over
        # ai is responsible for making sure it does not cheat thus you need to make sure you do not go over 14 cards
        # in the case that the other player also does not claim any tracks
        elif not len(player.handCards) == 14 and len(edges) == 10:  # aka no edges have been claimed
            #the AI wants to draw cards until the other player claims a track, because its bad to guess what the other
            #player is trying to complete before they have even claimed a track
            player.addCardToHand('black')
            player.addCardToHand('white')
            return ['draw t']

        tempArray = deepcopy(UtrackArray)
        for i in range(len(tempArray)):
            for j in range(len(tempArray)):
                if tempArray[i][j] == -1:
                    tempArray[i][j] = -1
                elif tempArray[i][j].getClaimed() == "False":
                    tempArray[i][j] = tempArray[i][j].length
                elif otherPlayer == tempArray[i][j].getClaimed():
                    tempArray[i][j] = 0
                else:
                    tempArray[i][j] = -1
        #tempArray is an adj matrix with -1s where there is no edge and 0 if the other player has claimed that edge
        #or the length of that edge if that edge is unclaimed

        '''destinationDeck = [['Washington', 'New York', 20], ['Texas', 'Colorado', 15], ['Montana', 'Texas', 16],
                           ['Washington', 'Oklahoma', 10], ['New York', 'Colorado', 15], ['Washington', 'Kansas', 8],
                           ['Montana', 'Oklahoma', 18], ['Texas', 'Kansas', 9], ['Montana', 'Colorado', 12]]

        cityIndices = {'Washington': 0, 'Montana': 1, 'New York': 2, 'Texas': 3, 'Colorado': 4, 'Kansas': 5, 'Oklahoma': 6}
'''
        completionArray = [0]*9
        for x in range(len(destinationDeck)):
            temp = self.dijkstra(destinationDeck[x][0], tempArray)[0]
            completionArray[x] = temp[cityIndices[destinationDeck[x][1]]]
        #the completionArray holds values equal to how close the other player is to completing each of the destination cards
        #for example if completionArray[1] = 3 then the other player is only 3 track lengths away from completing
        #the destination card from texas to colorado

        print("completionArray", completionArray)
        if all(x >= 99 for x in completionArray):  # if the other play is unable to complete ANY dest cards
            print("No destination cards left so it now follows empty hand strategy to avoid errors")
            return self.emptyHand(state, player)

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
        # minArray holds the indexes of the destination cards in the completionArray that are closest to being completed

        minDestCost = 0
        minDestIndex = -1
        for x in range(len(minArray)):
            if destinationDeck[minArray[x]][2] > minDestCost:
                minDestCost = destinationDeck[minArray[x]][2]
                minDestIndex = minArray[x]
        #for loop finds the dest card in the minArray worth the most, sets its index to minDestIndex and the length to minDestCost

        print("minDestIndex", minDestIndex)
        print("minDestCost", minDestCost)
        toClaim = self.dijkstra(destinationDeck[minDestIndex][0], tempArray)[1]
        #toClaim is the toClaimTrack array returned by dijkstra when run starting from the first city on the destination
        # card that is the closet to being completed (tie broke by card point value)

        endCityIndex = cityIndices[destinationDeck[minDestIndex][1]]  # index of 2nd city in min dest card
        wantedIndexes = []
        finalIndex = endCityIndex

        for x in range(len(toClaim)):  # for loop makes it so the while loop bellow does not break
            if toClaim[x] == 0:
                toClaim[x] = -1
        print("toClaim", toClaim)

        while finalIndex != -1 and toClaim[finalIndex] != -1:#type(finalIndex) != int and type(toClaim[finalIndex]) != int:#
            print("Final index", finalIndex)
            checkIndex = deepcopy(toClaim[finalIndex])
            if checkIndex[0] > checkIndex[1]:
                checkIndex[0], checkIndex[1] = checkIndex[1], checkIndex[0]
            '''print("checkIndex", checkIndex)
            print("UtrackArray[checkIndex[0]][checkIndex[1]].occupied", UtrackArray[checkIndex[0]][checkIndex[1]].occupied)'''

            if UtrackArray[checkIndex[0]][checkIndex[1]].occupied == 'False':
                wantedIndexes.append(toClaim[finalIndex])
                '''if toClaim[finalIndex] == 0:
                    break'''
            finalIndex = toClaim[finalIndex][0]
        #this while loop works backwards, starting from the 2nd city in the min dest card, and adds every edge along the
        #most direct path between the 2nd city in the min dest card and the 1st city in the min dest card to an array
        #called wantedIndexes. The strategies wants to claim these tracks because it will allow the ai to block the
        #other player from completing the dest card it is closest to completing.

        print("wantedIndexes", wantedIndexes)
        '''smallestEdgeLength = 99
        smallestEdge = -1
        wantedIndex = []
        for x in range(len(wantedIndexes)):
            if UtrackArray[wantedIndexes[x][0]][wantedIndexes[x][1]].length < smallestEdgeLength:
                smallestEdgeLength = UtrackArray[wantedIndexes[x][0]][wantedIndexes[x][1]].length
                smallestEdge = UtrackArray[wantedIndexes[x][0]][wantedIndexes[x][1]]
                wantedIndex = [wantedIndexes[x][0], wantedIndexes[x][1]]
            wanted = smallestEdge'''

        wantedIndex = []
        wanted = UtrackArray[wantedIndexes[0][0]][wantedIndexes[0][1]]
        smallestCardDif = 1000000  # python has not int.max_value so this is a sub
        # this for loop is the ai deciding which track it is closest to claiming out of the wanted tracks (wantedIndexes)
        for i in range(len(wantedIndexes)):
            currentEdge = UtrackArray[wantedIndexes[i][0]][wantedIndexes[i][1]]
            # if the edge length is closest to the amount of that color that this player has in their hand
            if currentEdge.length - player.handCards.count(currentEdge.color) < smallestCardDif:
                smallestCardDif = currentEdge.length - player.handCards.count(currentEdge.color)
                wanted = currentEdge
                wantedIndex = [wantedIndexes[i][0], wantedIndexes[i][1]]
            elif currentEdge.length - player.handCards.count(currentEdge.color) == smallestCardDif:
                # if there are multiple shortest tracks it picks one that it has more cards of its color
                if player.handCards.count(currentEdge.color) > player.handCards.count(wanted.color):
                    smallestCardDif = currentEdge.length - player.handCards.count(currentEdge.color)
                    wanted = currentEdge
                    wantedIndex = [wantedIndexes[i][0], wantedIndexes[i][1]]
                elif player.handCards.count(currentEdge.color) == player.handCards.count(wanted.color) and randint(0, 1) == 1:
                    smallestCardDif = currentEdge.length - player.handCards.count(currentEdge.color)
                    wanted = currentEdge
                    wantedIndex = [wantedIndexes[i][0], wantedIndexes[i][1]]

        print("wantedIndex", wantedIndex)
        neededCards = []
        for card in player.handCards:
            if card.color == wanted.color:
                neededCards.append(card)
            if len(neededCards) == wanted.length:  # if you can claim that track do so
                for toRemove in neededCards:
                    player.handCards.remove(toRemove)
                player.cardIndex = len(player.handCards)  # prob useless if I had to guess
                # wantedIndex.reverse()
                if wantedIndex[0] > wantedIndex[1]:
                    wantedIndex[0], wantedIndex[1] = wantedIndex[1], wantedIndex[0]
                return ['claim', wantedIndex]

        player.addCardToHand(wanted.color)
        if len(neededCards) + 1 == wanted.length:  # if the ai only needed one card to claim the track it wants
            # then the 2nd card its draws will be random
            colorsAvail = []
            for i in range(0, len(edges)):
                if edges[i].occupied == 'False' and not colorsAvail.__contains__(edges[i].color):
                    colorsAvail.append(edges[i].color)
            player.addCardToHand(colorsAvail[randint(0, len(colorsAvail) - 1)])  # randomness (stretch goal)
        else:  # if it needs more then one more then draw a 2nd card of the color of the track it wants
            player.addCardToHand(wanted.color)

        print("after drawing AI's hand is: ", end='')
        for card in player.handCards:
            print(card.color, end=' ')
        print()

        return ['draw t']


    def blindDestination(self, state, player):

        UtrackArray = np.array(state.trackArray).copy()
        edgeHash = np.array(np.triu_indices(len(UtrackArray))).T[
            (UtrackArray != -1)[np.triu_indices(len(UtrackArray))]]
        openEdges = [x.occupied == 'False' for x in UtrackArray[tuple(edgeHash.T)]]
        edgeHash = edgeHash[openEdges]
        edges = np.array(state.trackArray)[tuple(edgeHash.T)]
        if len(edges) == 0:
            return ['pass']  # game is actually already over

        print("the AI's dCards are: ", end='')
        for card in player.destinationCards:
            print(card.toString(), end=' ')
        print()

        tempArray = deepcopy(UtrackArray)
        for i in range(len(tempArray)):
            for j in range(len(tempArray)):
                if tempArray[i][j] == -1:
                    tempArray[i][j] = -1
                elif tempArray[i][j].getClaimed() == "False":
                    tempArray[i][j] = tempArray[i][j].length
                elif player.getName() == tempArray[i][j].getClaimed():
                    tempArray[i][j] = 0
                else:
                    tempArray[i][j] = -1
        # tempArray is an adj matrix with -1s where there is no edge and 0 if this player has claimed that edge
        # or the length of that edge if that edge is unclaimed

        targetDCard = None
        ## if it has a destCard that is not complete
        for dCard in player.destinationCards:  # looks at all the dest cards in its hand
            if not dCard.completed:  # only looks at the ones it has not completed
                fullInfo = self.dijkstra(dCard.city1, tempArray)
                distTo = fullInfo[0]
                ## (and can be completed)
                if distTo[cityIndices[dCard.city2]] > 99:
                    #if dist to the 2nd city in the dCard is over 99 then it is impossible to complete that dCard
                    #so it it stops looking at it
                    continue

                    '''possibleCompletionArray = [0] * 9
                    for x in range(len(destinationDeck)):
                        skip = False
                        for card in player.destinationCards:
                            if destinationDeck[x] == card.getValues:
                                skip = True
                                break
                        #if all(destinationDeck[x].getValues == card.getValues for card in player.destinationCards):
                        if skip:  # dont add any already completed dest card to possible completion array
                            continue
                        temp = self.dijkstra(destinationDeck[x][0], tempArray)[0]
                        possibleCompletionArray[x] = temp[cityIndices[destinationDeck[x][1]]]

                    # the completionArray holds values equal to how close the AI is to completing each of the destination cards
                    # for example if completionArray[1] = 3 then the other player is only 3 track lengths away from completing
                    # the destination card from texas to colorado

                    print("completionArray", possibleCompletionArray)
                    if all(x >= 99 for x in possibleCompletionArray):  # if it is impossible to complete ANY dest cards
                        print("No destination cards left so it now follows empty hand strategy to avoid errors")
                        return self.emptyHand(state, player)
                    else:
                        player.addDestCardToHand()
                        return ['draw d']'''
                else:
                    ## set that destCard to target destCard
                    targetDCard = dCard
                    break

        ## if not
        if targetDCard is None:  # if there are no destcards in its hand that it can complete
            #checks to make sure it it possible to complete ANY remaining destCards, if not it follows
            # the emptyhand strat, if there is a destcard it can complete it draws another dest card.
            possibleCompletionArray = []  # [0] * 9
            for x in range(len(destinationDeck)):
                skip = False
                for card in player.destinationCards:
                    if destinationDeck[x] == card.getValues:
                        skip = True
                        break
                # if all(destinationDeck[x].getValues == card.getValues for card in player.destinationCards):
                if skip:  # dont add any already completed dest card to possible completion array
                    continue
                temp = self.dijkstra(destinationDeck[x][0], tempArray)[0]
                #possibleCompletionArray[x] = temp[cityIndices[destinationDeck[x][1]]]
                possibleCompletionArray.append(temp[cityIndices[destinationDeck[x][1]]])

            # the completionArray holds values equal to how close the AI is to completing each of the destination cards
            # for example if completionArray[1] = 3 then it is only 3 track lengths away from completing
            # the destination card from texas to colorado

            print("completionArray", possibleCompletionArray)
            if all(x >= 99 for x in possibleCompletionArray):  # if it is impossible to complete ANY dest cards
                print("No destination cards left so it now follows empty hand strategy to avoid errors")
                return self.emptyHand(state, player)
            else:
                ## Draw a dCard
                player.addDestCardToHand()
                return ['draw d']

        print("targetDCard ", targetDCard.toString())
        '''dijkstraResult = self.dijkstra(cityIndices[targetDCard.city1], tempArray)
        distance = dijkstraResult[0][cityIndices[targetDCard.city2]]'''
        ## Run dijkstra to find the shortest path to complete the target destCard
        toClaim = self.dijkstra(cityIndices[targetDCard.city1], tempArray)[1]
        # toClaim is the toClaimTrack array returned by dijkstra when run starting from the first city on the
        # target destination

        wantedIndexes = []
        finalIndex = cityIndices[targetDCard.city2]

        for x in range(len(toClaim)):  # for loop makes it so the while loop bellow does not break
            if toClaim[x] == 0:
                toClaim[x] = -1
        print("toClaim", toClaim)

        while finalIndex != -1 and toClaim[finalIndex] != -1:  # type(finalIndex) != int and type(toClaim[finalIndex]) != int:#
            #print("Final index", finalIndex)
            checkIndex = deepcopy(toClaim[finalIndex])
            if checkIndex[0] > checkIndex[1]:
                checkIndex[0], checkIndex[1] = checkIndex[1], checkIndex[0]
            '''print("checkIndex", checkIndex)
            print("UtrackArray[checkIndex[0]][checkIndex[1]].occupied", UtrackArray[checkIndex[0]][checkIndex[1]].occupied)'''

            if UtrackArray[checkIndex[0]][checkIndex[1]].occupied == 'False':
                wantedIndexes.append(toClaim[finalIndex])
                '''if toClaim[finalIndex] == 0:
                    break'''
            finalIndex = toClaim[finalIndex][0]
        # this while loop works backwards, starting from the 2nd city in the target dest card, and adds every edge
        # along the most direct path between the 2nd city of the target dest card and the 1st city in the target dest
        # card to an array called wantedIndexes. The strategy wants to claim these tracks because they are the
        # tracks along the shortest path which allows it to complete its target Destination card

        wantedIndex = []
        wanted = UtrackArray[wantedIndexes[0][0]][wantedIndexes[0][1]]
        smallestCardDif = 1000000  # python has not int.max_value so this is a sub
        # this for loop is the ai deciding which track it is closest to claiming out of the wanted tracks (wantedIndexes)
        for i in range(len(wantedIndexes)):
            currentEdge = UtrackArray[wantedIndexes[i][0]][wantedIndexes[i][1]]
            # if the edge length is closest to the amount of that color that this player has in their hand
            if currentEdge.length - player.handCards.count(currentEdge.color) < smallestCardDif:
                smallestCardDif = currentEdge.length - player.handCards.count(currentEdge.color)
                wanted = currentEdge  ## Set that track to be the wanted edge
                wantedIndex = [wantedIndexes[i][0], wantedIndexes[i][1]]
            elif currentEdge.length - player.handCards.count(currentEdge.color) == smallestCardDif:
                # if there are multiple shortest tracks it picks one that it has more cards of its color
                if player.handCards.count(currentEdge.color) > player.handCards.count(wanted.color):
                    smallestCardDif = currentEdge.length - player.handCards.count(currentEdge.color)
                    wanted = currentEdge
                    wantedIndex = [wantedIndexes[i][0], wantedIndexes[i][1]]
                elif player.handCards.count(currentEdge.color) == player.handCards.count(wanted.color) and randint(0, 1) == 1:
                    smallestCardDif = currentEdge.length - player.handCards.count(currentEdge.color)
                    wanted = currentEdge
                    wantedIndex = [wantedIndexes[i][0], wantedIndexes[i][1]]
        ## Find the track (edge) along the shortest path that it is closest to claiming

        print("wantedIndex", wantedIndex)
        neededCards = []
        ## If it can claim the wanted edge
        for card in player.handCards:
            if card.color == wanted.color:
                neededCards.append(card)
            if len(neededCards) == wanted.length:  # if you can claim that track do so
                for toRemove in neededCards:
                    player.handCards.remove(toRemove)
                player.cardIndex = len(player.handCards)  # prob useless if I had to guess
                # wantedIndex.reverse()
                if wantedIndex[0] > wantedIndex[1]:
                    wantedIndex[0], wantedIndex[1] = wantedIndex[1], wantedIndex[0]
                return ['claim', wantedIndex]  ## claim it

        ## If not
        player.addCardToHand(wanted.color)  ## Draw cards of the color of that track
        if len(neededCards) + 1 == wanted.length:  # if the ai only needed one card to claim the track it wants
            # then it draws a color of another track it needs along the shortest path
            colorsAvail = []
            for i in range(0, len(edges)):
                if edges[i].occupied == 'False' and not colorsAvail.__contains__(edges[i].color):
                    colorsAvail.append(edges[i].color)
            wantedColor = colorsAvail[randint(0, len(colorsAvail) - 1)]  # randomness (stretch goal)

            colorsAlongPath = []
            for i in range(len(wantedIndexes)):
                if wantedIndexes[i] != wantedIndex:
                    edge = wantedIndexes[i]
                    if not colorsAlongPath.__contains__(UtrackArray[edge[0]][edge[1]].color):
                        colorsAlongPath.append(UtrackArray[edge[0]][edge[1]].color)
            if len(colorsAlongPath) != 0:
                wantedColor = colorsAlongPath[randint(0, len(colorsAlongPath) - 1)]

            player.addCardToHand(wantedColor)
            ''' I tried to make it even smarter... i failed i think but i cant bring myself to delete the code
            colorCounts = []  # after the for loop colorCounts will be a 2d array of all the colors of the tracks
            # along the shortest path and their lengths
            for index in wantedIndexes:
                if not index == wantedIndex:
                    edge = UtrackArray[index[0]][index[1]]
                    newColor = True
                    for color in colorCounts:
                        if color[0] == edge.color:
                            colorCounts[colorCounts.index(color)][1] += edge.length
                            newColor = False
                            break
                    if newColor:
                        colorCounts.append([edge.color, edge.length])
            
            if len(colorCounts) != 0:
                # removes the amount of that color card you have in your hand (except of the edge you are 
                # claiming next turn)
                for color in colorCounts:
                    if color[0] == UtrackArray[wantedIndex[0]][wantedIndex[1]].color:
                        continue
                    else:
                        color[1] -= player.numCardsOfColor(color[0])
                
                #find the color you are
                minColor = 99
                for color in colorCounts:
                    if color[1] < minColor:
                        wantedColor = color[0]
                        minColor = color[1]
                    elif color[1] == minColor and randint(0, 1) == 1:
                        wantedColor = color[0]
                        minColor = color[1]
            
            player.addCardToHand(wantedColor)
            '''
        else:  # if it needs more then one more: draw a 2nd card of the color of the track it wants
            player.addCardToHand(wanted.color)  ## Draw cards of the color of that track
        print("after drawing AI's hand is: ", end='')
        for card in player.handCards:
            print(card.color, end=' ')
        print()

        return ['draw t']

    def printSolution(self, dist, city):
        print("Vertex Distance from Source")
        for node in range(7):
            print(city, " to ", node, " takes ", dist[node])

    def minDistance(self, dist, sptSet):

        minNum = sys.maxsize
        min_index = 0  # there is prob an error in this method since a min index should always be found

        for v in range(7):
            if dist[v] < minNum and sptSet[v] == False:
                minNum = dist[v]
                min_index = v

        return min_index

    def dijkstra(self, start, graph):

        '''cityIndices = {'Washington': 0, 'Montana': 1, 'New York': 2, 'Texas': 3, 'Colorado': 4, 'Kansas': 5,
                       'Oklahoma': 6}'''
        if type(start) is str:
            start = cityIndices[start]

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
        #print(dist)
        return [dist, toClaimTrack]


    @staticmethod
    def randomStrategy():
        x = randint(0, len(stratList)-1)
        return stratList[x]