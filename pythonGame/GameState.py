import numpy as np
import os
from DestinationCard import DestinationCard


class GameState:
    # the game state is made up of data from each player which may change from turn to turn
    # and data about the game board and turn count
    # this means the AI will have access to the other player's hand and destination cards, however
    # it will not be allowed to uses that info, simply it will not be coded to ever reference those values
    def __init__(self, turn, tracks, p1, p2):
        self.turn = turn
        self.trackArray = tracks
        self.p1dCards = p1.getDestCards()
        self.p2dCards = p2.getDestCards()
        self.p1Hand = p1.getHand()
        self.p2Hand = p2.getHand()
        self.p1Points = p1.points
        self.p2Points = p2.points
        self.p1Action = None
        self.p2Action = None
        #
        self.LastFullAction = None

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
        self.lastAction = None

    def updateTracks(self, tracks):
        self.trackArray = tracks

    def updatePlayerInfo(self, player):
        if player.getName() == 'playerOne':
            if self.p1Action == 'draw t' or self.p1Action == 'claim':
                self.p1Hand = player.getHand()
                self.p1Points = player.points
            elif self.p1Action == 'draw d':
                self.p1dCards = player.getDestCards()
        elif player.getName() == 'playerTwo':
            if self.p2Action == 'draw t' or self.p2Action == 'claim':
                self.p2Hand = player.getHand()
                self.p2Points = player.points
            elif self.p2Action == 'draw d':
                self.p2dCards = player.getDestCards()
        else:
            print("Error: player not found. No state info updated")

    def writeToCSV(self, player):  # as of now a separate csv will be made for each player that will
        # only include that player's hand, dcards, and action taken
        # I do not know how this will affect the DTM since the tracks will be changing without any action
        # being showed in the DTM whenever the other player makes a move.
        # Since there may be unknown downsides this method is subject to change
        destination = "/some_file_location"
        print("csv based on gameState for " + player.getName() + " was successfully generated at: " + destination)

    # def output(self):
    #     return [self.turn,]

    # alexs function to test input output data for nn
    def writeToNPY(self):
        UtrackArray = np.array(self.trackArray)
        UtrackArray = UtrackArray[np.triu_indices(len(UtrackArray))]
        UtrackArray = UtrackArray[UtrackArray != -1]
        UtrackArray = np.array([[x.length, x.color, x.occupied] for x in UtrackArray])
        UtrackArray = UtrackArray.flatten()

        # square[np.triu_indices(10, 1)].shape

        destDeck = DestinationCard.getDestinationDeck()

        destPoints = destDeck[:, 2]

        Up1d = np.zeros(len(destDeck))
        for i in range(len(self.p1dCards)):
            for j in range(len(destDeck)):
                if self.p1dCards[i] == destDeck[j]: Up1d[j] += 1

        Up2d = np.zeros(len(destDeck))
        for i in range(len(self.p2dCards)):
            for j in range(len(destDeck)):
                if self.p1dCards[i] == destDeck[j]: Up2d[j] += 1

        allColors = ['white', 'pink', 'red', 'orange', 'yellow', 'green', 'blue', 'black']

        Up1c = np.zeros(len(allColors))
        for i in range(len(self.p1Hand)):
            for j in range(len(allColors)):
                if self.p1Hand[i] == allColors[j]: Up1c[j] += 1

        Up2c = np.zeros(len(allColors))
        for i in range(len(self.p2Hand)):
            for j in range(len(allColors)):
                if self.p2Hand[i] == allColors[j]: Up2c[j] += 1



        np.save(file=os.getcwd() + '/thisturn.npy', arr=[self.turn, UtrackArray, Up1c, Up1d, Up2c, Up2d, destPoints
            , self.p1Points, self.p2Points, self.p1Action, self.p2Action], allow_pickle=True)
