class GameState:
    #the game state is made up of data from each player which may change from turn to turn
    #and data about the game board and turn count
    #this means the AI will have access to the other player's hand and destination cards, however
    #it will not be allowed to uses that info, simply it will not be coded to ever reference those values
    def __init__(self, turn, tracks, p1, p2):
        self.turn = turn
        self.trackArray = tracks
        self.p2dCards = p2.getDestCards()
        self.p1dCards = p1.getDestCards()
        self.p2Hand = p2.getHand()
        self.p1Hand = p1.getHand()
        self.p1Action = None
        self.p2Action = None

    def setPlayerMove(self, player, action):
        if player.getName() == 'playerOne':
            self.p1Action = action
        elif player.getName() == 'playerTwo':
            self.p2Action = action
        else:
            print("Error: player not found. No action was added")

    def getTrackArray(self):
        return self.trackArray

    def getP1Move(self):
        return self.p1Action

    def getP2Move(self):
        return self.p2Action

    def incrementTurn(self):
        self.turn += 1
        # next lines reset the actions for the players since they have not made a move yet on the next turn
        self.p1Action = None
        self.p2Action = None

    def updateTracks(self, tracks):
        self.trackArray = tracks

    def updatePlayerInfo(self, player):
        if player.getName() == 'playerOne':
            if self.p1Action == 'draw t' or self.p1Action == 'claim':
                self.p1Hand = player.getHand()
            elif self.p1Action == 'draw d':
                self.p1dCards = player.getDestCards()
        elif player.getName() == 'playerTwo':
            if self.p2Action == 'draw t' or self.p2Action == 'claim':
                self.p2Hand = player.getHand()
            elif self.p2Action == 'draw d':
                self.p2dCards = player.getDestCards()
        else:
            print("Error: player not found. No state info updated")

    def writeToCSV(self, player):  # as of now a separate csv will be made for each player that will
        # only include that player's hand, dcards, and action take
        # I do not know how this will affect the DTM since the tracks will be changing without any action
        # being showed in the DTM whenever the other player makes a move.
        # Since there may be unknown downsides this method is subject to change
        destination = "/some_file_location"
        print("csv based on gameState for was successfully generated at: " + destination)
