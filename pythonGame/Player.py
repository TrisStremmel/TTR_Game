from Card import Card
from DestinationCard import DestinationCard

class Player:
    def __init__(self, name):
        self.handCards = []
        self.cardIndex = 0
        self.destinationCards = []
        self.name = name
        self.points = 0

    def makeMove(self, gameState):
        print("player can not make a decision")

    def getHand(self):
        return self.handCards

    def addCardToHand(self, color):
        self.handCards.append(Card(color))
        self.cardIndex += 1

    def addDestCardToHand(self):
        breaker = 0
        tempCard = DestinationCard.drawDestinationCard()
        while tempCard in self.destinationCards:  # so dup dest cards are not added to hand
            tempCard = DestinationCard.drawDestinationCard()
            breaker += 1
            if breaker > 200:
                break
        self.destinationCards.append(tempCard)

    def checkDestCardCompletion(self, cityConnection):
        cityIndices = {'Washington': 0, 'Montana': 1, 'New York': 2, 'Texas': 3, 'Colorado': 4, 'Kansas': 5,
                       'Oklahoma': 6}
        for dCard in self.destinationCards:
            if not dCard.completed:
                #check if there is a path made up of tracks completed by this player
                tempArray = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0]]
                # this loop makes the temp array into a adjacency matrix of all the tracks this player has claimed
                for i in range(len(cityConnection)):
                    for j in range(len(cityConnection[i])):
                        if cityConnection[i][j] != -1 and cityConnection[i][j].occupied == self.name:
                            tempArray[i][j] = 1

                # if yes then:
                if self.DFS(tempArray, cityIndices[dCard.city1], cityIndices[dCard.city2], [False] * len(cityConnection)):
                    self.points += dCard.getPoints()
                    dCard.completed = True
                    print(self.name + " completed the destination card from " + dCard.city1 + " to " + dCard.city2 +
                          " for " + str(dCard.getPoints()) + " points.")

    def getCardIndex(self):
        return self.cardIndex

    def getDestCards(self):
        return self.destinationCards

    def getName(self):
        return self.name

    # Function to perform DFS on the graph
    def DFS(self, array, start, end, visited):
        toReturn = False
        #checks if it has reached the 2nd city (aka the destination card has been completed)
        if start == end:
            return True

        # Set current node as visited
        visited[start] = True

        # For every node of the graph
        for i in range(len(array)):
            # If some node is adjacent to the current node and it has not already been visited
            if array[start][i] == 1 and (not visited[i]):
                toReturn = self.DFS(array, i, end, visited)

        return toReturn
