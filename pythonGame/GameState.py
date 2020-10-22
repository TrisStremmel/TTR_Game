import numpy as np
import os
import csv
from csv import writer
from DestinationCard import DestinationCard


class GameState:
    player1 = "player1.csv"
    player2 = "player2.csv"
    fields = ['turn', 'P1 vs P2 Point Dif', 'Card Color Dif', 'Track 1', 'Track 2', 'Track 3', 'Track 4', 'Track 5', 'Track 6', 'Track 7', 'Track 8', 'Track 9', 'Track 10', 'Destination Cards']




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

        elif player.getName() == 'playerTwo':
            if self.p2Action == 'draw t' or self.p2Action == 'claim':
                self.p2Hand = player.getHand()
                self.p2Points = player.points
            elif self.p2Action == 'draw d':
                self.p2dCards = player.getDestCards()

        else:
            print("Error: player not found. No state info updated")

    def writeToCSV(self):  # as of now a separate csv will be made for each player that will
        # only include that player's hand, dcards, and action taken
        # I do not know how this will affect the DTM since the tracks will be changing without any action
        # being showed in the DTM whenever the other player makes a move.
        # Since there may be unknown downsides this method is subject to change
        # writing to csv file

        track1 = self.trackArray[0][1]
        track2 = self.trackArray[0][3]
        track3 = self.trackArray[0][4]
        track4 = self.trackArray[1][2]
        track5 = self.trackArray[2][3]
        track6 = self.trackArray[2][5]
        track7 = self.trackArray[3][6]
        track8 = self.trackArray[4][5]
        track9 = self.trackArray[4][6]
        track10 = self.trackArray[5][6]

        limitedFlag = False;
        if(limitedFlag):
            player1HandCount = self.blackWhiteCount(self.p1Hand)
            player2HandCount = self.blackWhiteCount(self.p2Hand)

            limitedP1Data = [self.turn+1, abs(self.p1Points - self.p2Points), player1HandCount[3],
                             track1.getClaimed() + " " + str(track1.getLength()) + " " + track1.getColor(),
                             track2.getClaimed() + " " + str(track2.getLength()) + " " + track2.getColor(),
                             track3.getClaimed() + " " + str(track3.getLength()) + " " + track3.getColor(),
                             track4.getClaimed() + " " + str(track4.getLength()) + " " + track4.getColor(),
                             track5.getClaimed() + " " + str(track5.getLength()) + " " + track5.getColor(),
                             track6.getClaimed() + " " + str(track6.getLength()) + " " + track6.getColor(),
                             track7.getClaimed() + " " + str(track7.getLength()) + " " + track7.getColor(),
                             track8.getClaimed() + " " + str(track8.getLength()) + " " + track8.getColor(),
                             track9.getClaimed() + " " + str(track9.getLength()) + " " + track9.getColor(),
                             track10.getClaimed() + " " +str(track10.getLength()) + " " +track10.getColor(),
                             self.destinationCards(self.p1dCards)]
            limitedP2Data = [self.turn + 1, abs(self.p1Points - self.p2Points), player2HandCount[3],
                             track1.getClaimed() + " " + str(track1.getLength()) + " " + track1.getColor(),
                             track2.getClaimed() + " " + str(track2.getLength()) + " " + track2.getColor(),
                             track3.getClaimed() + " " + str(track3.getLength()) + " " + track3.getColor(),
                             track4.getClaimed() + " " + str(track4.getLength()) + " " + track4.getColor(),
                             track5.getClaimed() + " " + str(track5.getLength()) + " " + track5.getColor(),
                             track6.getClaimed() + " " + str(track6.getLength()) + " " + track6.getColor(),
                             track7.getClaimed() + " " + str(track7.getLength()) + " " + track7.getColor(),
                             track8.getClaimed() + " " + str(track8.getLength()) + " " + track8.getColor(),
                             track9.getClaimed() + " " + str(track9.getLength()) + " " + track9.getColor(),
                             track10.getClaimed() + " " + str(track10.getLength()) + " "+track10.getColor(),
                             self.destinationCards(self.p2dCards)]
            self.append_list_as_row(self.player1, limitedP1Data)
            print("csv based on gameState for player 1 was successfully updated at: " + self.player1)
            self.append_list_as_row(self.player2, limitedP2Data)
            print("csv based on gameState for player 2 was successfully updated at: " + self.player2)
            destination = "/some_file_location"
        else:
            player1HandCount = self.blackWhiteCount(self.p1Hand)
            player2HandCount = self.blackWhiteCount(self.p2Hand)

            player1DesinationCards = self.sortedDestination(self.destinationCards(self.p1dCards))
            dcardNames = ''
            dcardWorth = ''
            dcardComplete = ''
            for x in player1DesinationCards:
                dcardNames += str(x) + ' '
                dcardWorth += str(x) + ' '
                #dcardComplete += x.

            robustP1Data = [self.turn + 1, self.p1Points, self.p2Points,
                             'Player 1 '+str(player1HandCount[0])+' black',
                             'Player 1 '+str(player1HandCount[1])+' white',
                             'Player 2 '+str(player2HandCount[0])+' black',
                             'Player 2 '+str(player2HandCount[1])+' white',
                             track1.getClaimed(), track1.getLength(), track1.getColor(), 'WA MT',
                             track2.getClaimed(), track2.getLength(), track2.getColor(), 'WA TX',
                             track3.getClaimed(), track3.getLength(), track3.getColor(), 'WA CO',
                             track4.getClaimed(), track4.getLength(), track4.getColor(), 'MT NY',
                             track5.getClaimed(), track5.getLength(), track5.getColor(), 'NY TX',
                             track6.getClaimed(), track6.getLength(), track6.getColor(), 'NY KS',
                             track7.getClaimed(), track7.getLength(), track7.getColor(), 'TX OK',
                             track8.getClaimed(), track8.getLength(), track8.getColor(), 'CO KS',
                             track9.getClaimed(), track9.getLength(), track9.getColor(), 'CO OK',
                             track10.getClaimed(),track10.getLength(),track10.getColor(),'KS OK',
                             dcardNames, dcardWorth
                             ]
            robustP2Data = [];
            self.append_list_as_row(self.player1, robustP1Data)
            print("csv based on gameState for player 1 was successfully updated at: " + self.player1)
            self.append_list_as_row(self.player2, robustP2Data)
            print("csv based on gameState for player 2 was successfully updated at: " + self.player2)
            destination = "/some_file_location"




    def append_list_as_row(self, file_name, list_of_elem):
        # Open file in append mode
        with open(file_name, 'a+', newline='') as write_obj:
            # Create a writer object from csv module
            csv_writer = writer(write_obj)
            # Add contents of list as last row in the csv file
            csv_writer.writerow(list_of_elem)

    def blackWhiteCount(self, hand):
        #[Black count, white count, total count, black white difference]
        numCards=[0,0,0,'']
        for x in hand:
            if(x.color == 'black'):
                numCards[0] += 1
            if (x.color == 'white'):
                numCards[1] += 1
            numCards[2] += 1
        cardDif = numCards[0]-numCards[1]
        if(cardDif < 0):
            numCards[3] = str(abs(cardDif)) + " more white"
        else:
            numCards[3] = str(cardDif) + " more black"

        return numCards

    def destinationCards(self, dcard):
        toReturn = ''
        for x in dcard:
            toReturn += x.toString() + " and "
        return toReturn[:-5]
    # def output(self):
    #     return [self.turn,]

    def sortedDestination(self, dcards):
        for x in range(0, len(dcards), 1):
            for y in range(1, len(dcards), 1):
                if str(dcards[x].citiesNoPoints) > str(dcards[y].citiesNoPoints):
                    temp = dcards[x]
                    dcards[x] = dcards[y]
                    dcards[y] = temp
        return dcards


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
