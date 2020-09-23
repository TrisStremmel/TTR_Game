import numpy as np
import os
import csv
from csv import writer
from DestinationCard import DestinationCard


class GameState:
    player1 = "player1.csv"
    player2 = "player2.csv"
    fields = ['turn', 'destination_cards', 'black_cards', 'white_cards', 'total_cards', 'points', 'action']




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
        self.LastP = 'playerOne'
        self.append_list_as_row(self.player1, self.fields)
        self.append_list_as_row(self.player2, self.fields)

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
            self.writeToCSV("player1.csv")
        elif player.getName() == 'playerTwo':
            if self.p2Action == 'draw t' or self.p2Action == 'claim':
                self.p2Hand = player.getHand()
                self.p2Points = player.points
            elif self.p2Action == 'draw d':
                self.p2dCards = player.getDestCards()
            self.writeToCSV("player2.csv")
        else:
            print("Error: player not found. No state info updated")

    def writeToCSV(self, playerFileName):  # as of now a separate csv will be made for each player that will
        # only include that player's hand, dcards, and action taken
        # I do not know how this will affect the DTM since the tracks will be changing without any action
        # being showed in the DTM whenever the other player makes a move.
        # Since there may be unknown downsides this method is subject to change
        # writing to csv file
        player1HandCount = self.blackWhiteCount(self.p1Hand)
        player2HandCount = self.blackWhiteCount(self.p2Hand)
        turnData = [self.turn, self.destinationCards(self.p1dCards), player1HandCount[0], player1HandCount[1], player1HandCount[2], self.p1Points, self.p1Action]
        self.append_list_as_row(playerFileName, turnData)

        destination = "/some_file_location"
        print("csv based on gameState for " + playerFileName + " was successfully generated at: " + destination)

    def append_list_as_row(self, file_name, list_of_elem):
        # Open file in append mode
        with open(file_name, 'a+', newline='') as write_obj:
            # Create a writer object from csv module
            csv_writer = writer(write_obj)
            # Add contents of list as last row in the csv file
            csv_writer.writerow(list_of_elem)

    def blackWhiteCount(self, hand):
        numCards=[0,0,0]
        for x in hand:
            if(x.color == 'black'):
                numCards[0] += 1
            if (x.color == 'white'):
                numCards[1] += 1
            numCards[2] += 1
        return numCards

    def destinationCards(self, dcard):
        toReturn = ''
        for x in dcard:
            toReturn += x.toString() + " and "
        return toReturn[:-5]
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
                if (self.p1dCards[i].getValues() == destDeck[j]).all(): Up1d[j] += 1

        Up2d = np.zeros(len(destDeck))
        for i in range(len(self.p2dCards)):
            for j in range(len(destDeck)):
                if (self.p1dCards[i].getValues() == destDeck[j]).all(): Up2d[j] += 1

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

    def returnListedforP(self):
        UtrackArray = np.array(self.trackArray)
        UtrackArray = UtrackArray[np.triu_indices(len(UtrackArray))]
        UtrackArray = UtrackArray[UtrackArray != -1]
        UtrackArray = np.array([[x.length, x.color, x.occupied] for x in UtrackArray])
        UtrackArray = UtrackArray.flatten()

        destDeck = DestinationCard.getDestinationDeck()
        destPoints = destDeck[:, 2]

        allColors = ['white', 'pink', 'red', 'orange', 'yellow', 'green', 'blue', 'black']

        if self.LastP == 'playerOne':
            Up1d = np.zeros(len(destDeck))
            for i in range(len(self.p1dCards)):
                for j in range(len(destDeck)):
                    if (self.p1dCards[i].getValues() == destDeck[j]).all(): Up1d[j] += 1

            Up1c = np.zeros(len(allColors))
            for i in range(len(self.p1Hand)):
                for j in range(len(allColors)):
                    if self.p1Hand[i] == allColors[j]: Up1c[j] += 1

            return [self.turn, self.LastFullAction, UtrackArray, destPoints, Up1d, Up1c, self.p1Points]

        elif self.LastP == 'playerTwo':
            Up2d = np.zeros(len(destDeck))
            for i in range(len(self.p2dCards)):
                for j in range(len(destDeck)):
                    if (self.p1dCards[i].getValues() == destDeck[j]).all(): Up2d[j] += 1

            Up2c = np.zeros(len(allColors))
            for i in range(len(self.p2Hand)):
                for j in range(len(allColors)):
                    if self.p2Hand[i] == allColors[j]: Up2c[j] += 1

            return [self.turn, self.LastFullAction, UtrackArray, destPoints, Up2d, Up2c, self.p2Points]
