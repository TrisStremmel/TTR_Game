import numpy as np
import os
from copy import deepcopy
import csv
from csv import writer
from DestinationCard import DestinationCard
from datetime import date, datetime

#if true saves only limited feature set csv, if false saves only extended set
limitedFlag = False

#ovrights limitedFlag, prints both limited and extended set
bothCSVFlag = True

class GameState:
    limFields = ['turn', 'action', 'P1 vs P2 Point Dif', 'Card Color Dif', 'Track 1', 'Track 2', 'Track 3', 'Track 4',
                 'Track 5', 'Track 6', 'Track 7', 'Track 8', 'Track 9', 'Track 10', 'Destination Cards']
    exFields = ['turn', 'action', 'other player action', 'P1 points', 'P2 Points',
                  'P1 Num Black', 'P1 Num White', 'P2 Num Black', 'P2 Num White',
                  'Track 1 Owned', 'Track 1 Length', 'Track 1 Color', 'Track 1 Cities',
                  'Track 2 Owned', 'Track 2 Length', 'Track 2 Color', 'Track 2 Cities',
                  'Track 3 Owned', 'Track 3 Length', 'Track 3 Color', 'Track 3 Cities',
                  'Track 4 Owned', 'Track 4 Length', 'Track 4 Color', 'Track 4 Cities',
                  'Track 5 Owned', 'Track 5 Length', 'Track 5 Color', 'Track 5 Cities',
                  'Track 6 Owned', 'Track 6 Length', 'Track 6 Color', 'Track 6 Cities',
                  'Track 7 Owned', 'Track 7 Length', 'Track 7 Color', 'Track 7 Cities',
                  'Track 8 Owned', 'Track 8 Length', 'Track 8 Color', 'Track 8 Cities',
                  'Track 9 Owned', 'Track 9 Length', 'Track 9 Color', 'Track 9 Cities',
                  'Track 10 Owned', 'Track 10 Length', 'Track 10 Color', 'Track 10 Cities',
                  'Destination Cards Cities', 'Destination Cards Worth', 'Destination Cards Completed']


    # the game state is made up of data from each player which may change from turn to turn
    # and data about the game board and turn count
    # this means the AI will have access to the other player's hand and destination cards
    # it will be allowed to use that info, this could change in the future
    def __init__(self, turn, tracks, p1, p2):
        self.turn = turn
        self.trackArray = tracks
        self.p1dCards = p1.getDestCards()
        self.p2dCards = p2.getDestCards()
        self.p1Hand = p1.getHand()
        self.p2Hand = p2.getHand()
        self.p1Points = p1.points
        self.p2Points = p2.points
        #self.p1
        self.p1Action = None
        self.p2Action = None
        self.LastFullAction = None
        self.LastP = 'playerOne'
        self.player1lim = ""
        self.player2lim = ""
        self.player1ex = ""
        self.player2ex = ""

    def createCSVs(self, currentdirs, runstr):
        runstr = str(runstr)
        if limitedFlag or bothCSVFlag:
            self.player1lim = currentdirs + "/player1lim_" + runstr + ".csv"
            self.player2lim = currentdirs + "/player2lim_" + runstr + ".csv"
            self.append_list_as_row(self.player1lim, self.limFields)
            self.append_list_as_row(self.player2lim, self.limFields)
        if (not limitedFlag) or bothCSVFlag:
            self.player1ex = currentdirs + "/player1ex_" + runstr + ".csv"
            self.player2ex = currentdirs + "/player2ex_" + runstr + ".csv"
            self.append_list_as_row(self.player1ex, self.exFields)
            self.append_list_as_row(self.player2ex, self.exFields)

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
        # yea except it doesnt, i have no clue what the point of this is, it is never used but numpy scares me
        # so i wont get rid of it
        self.lastAction = None

    def updateTracks(self, tracks):
        self.trackArray = tracks

    def addFinalScores(self, playerOne, playerTwo):
        self.p1Points = playerOne.points
        self.p2Points = playerTwo.points
        self.p1Action = "none"
        self.p2Action = "none"
        self.turn = "Game end"

    def updatePlayerInfo(self, player):
        # i got rid of the points updating based on the action so now they all update each round, no errors should come
        # about from this but if CSVs start having weird values revisit this.
        if player.getName() == 'playerOne':
            #if self.p1Action == 'draw t' or self.p1Action == 'claim':
                self.p1Hand = player.getHand()
                self.p1Points = player.points
            #elif self.p1Action == 'draw d':
                self.p1dCards = player.getDestCards()

        elif player.getName() == 'playerTwo':
            #if self.p2Action == 'draw t' or self.p2Action == 'claim':
                self.p2Hand = player.getHand()
                self.p2Points = player.points
            #elif self.p2Action == 'draw d':
                self.p2dCards = player.getDestCards()

        else:
            print("Error: player not found. No state info updated")

    def writeToCSV(self):
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


        player1HandCount = self.blackWhiteCount(self.p1Hand)
        player2HandCount = self.blackWhiteCount(self.p2Hand)

        limitedP1Data = [self.turn, self.p1Action, (self.p1Points - self.p2Points), player1HandCount[3],
                         track1.getClaimed() + " " + str(track1.getLength()) + " " + track1.getColor(),
                         track2.getClaimed() + " " + str(track2.getLength()) + " " + track2.getColor(),
                         track3.getClaimed() + " " + str(track3.getLength()) + " " + track3.getColor(),
                         track4.getClaimed() + " " + str(track4.getLength()) + " " + track4.getColor(),
                         track5.getClaimed() + " " + str(track5.getLength()) + " " + track5.getColor(),
                         track6.getClaimed() + " " + str(track6.getLength()) + " " + track6.getColor(),
                         track7.getClaimed() + " " + str(track7.getLength()) + " " + track7.getColor(),
                         track8.getClaimed() + " " + str(track8.getLength()) + " " + track8.getColor(),
                         track9.getClaimed() + " " + str(track9.getLength()) + " " + track9.getColor(),
                         track10.getClaimed() + " " + str(track10.getLength()) + " " + track10.getColor(),
                         self.formatDestinationCards(self.p1dCards)
                         ]
        limitedP2Data = [self.turn, self.p2Action, (self.p2Points - self.p1Points), player2HandCount[3],
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
                         self.formatDestinationCards(self.p2dCards)
                         ]
        if limitedFlag or bothCSVFlag:
            self.append_list_as_row(self.player1lim, limitedP1Data)
            print("csv based on gameState for player 1 was successfully updated at: " + self.player1lim)
            self.append_list_as_row(self.player2lim, limitedP2Data)
            print("csv based on gameState for player 2 was successfully updated at: " + self.player2lim)
            destination = "/some_file_location"

        dcardNames1 = ""
        dcardWorth1 = ""
        dcardNames2 = ""
        dcardWorth2 = ""
        dcardComplete1 = ""
        dcardComplete2 = ""
        dcardsCopy1 = deepcopy(self.p1dCards)
        dcardsCopy2 = deepcopy(self.p2dCards)

        player1DesinationCards = self.sortedDestination(dcardsCopy1)
        player2DesinationCards = self.sortedDestination(dcardsCopy2)

        for x in player1DesinationCards:
            dcardNames1 += x.citiesNoPoints() + ' '
            dcardWorth1 += str(x.getPoints()) + ' '
            dcardComplete1 += str(x.completed) + ' '
        for x in player2DesinationCards:
            dcardNames2 += x.citiesNoPoints() + ' '
            dcardWorth2 += str(x.getPoints()) + ' '
            dcardComplete2 += str(x.completed) + ' '

        dcardNames1 = dcardNames1[:-1]
        dcardWorth1 = dcardWorth1[:-1]
        dcardNames2 = dcardNames2[:-1]
        dcardWorth2 = dcardWorth2[:-1]
        dcardComplete1 = dcardComplete1[:-1]
        dcardComplete2 = dcardComplete2[:-1]


        ''' this is the old way the robust set did number of cards in the players hand, i didnt like it so i replaced it
        if for some reason we want to go back here it is:
                         'Player 1 '+str(player1HandCount[0])+' black',
                         'Player 1 '+str(player1HandCount[1])+' white',
                         'Player 2 '+str(player2HandCount[0])+' black',
                         'Player 2 '+str(player2HandCount[1])+' white',
        '''
        robustP1Data = [self.turn, self.p1Action, self.p2Action, self.p1Points, self.p2Points,
                        str(player1HandCount[0]), str(player1HandCount[1]),
                        str(player2HandCount[0]), str(player2HandCount[1]),
                        track1.getClaimed(), track1.getLength(), track1.getColor(), 'WA MT',
                        track2.getClaimed(), track2.getLength(), track2.getColor(), 'WA TX',
                        track3.getClaimed(), track3.getLength(), track3.getColor(), 'WA CO',
                        track4.getClaimed(), track4.getLength(), track4.getColor(), 'MT NY',
                        track5.getClaimed(), track5.getLength(), track5.getColor(), 'NY TX',
                        track6.getClaimed(), track6.getLength(), track6.getColor(), 'NY KS',
                        track7.getClaimed(), track7.getLength(), track7.getColor(), 'TX OK',
                        track8.getClaimed(), track8.getLength(), track8.getColor(), 'CO KS',
                        track9.getClaimed(), track9.getLength(), track9.getColor(), 'CO OK',
                        track10.getClaimed(), track10.getLength(), track10.getColor(), 'KS OK',
                        dcardNames1, dcardWorth1, dcardComplete1.upper()
                        ]
        robustP2Data = [self.turn, self.p2Action, self.p1Action, self.p1Points, self.p2Points,
                        str(player1HandCount[0]), str(player1HandCount[1]),
                        str(player2HandCount[0]), str(player2HandCount[1]),
                        track1.getClaimed(), track1.getLength(), track1.getColor(), 'WA MT',
                        track2.getClaimed(), track2.getLength(), track2.getColor(), 'WA TX',
                        track3.getClaimed(), track3.getLength(), track3.getColor(), 'WA CO',
                        track4.getClaimed(), track4.getLength(), track4.getColor(), 'MT NY',
                        track5.getClaimed(), track5.getLength(), track5.getColor(), 'NY TX',
                        track6.getClaimed(), track6.getLength(), track6.getColor(), 'NY KS',
                        track7.getClaimed(), track7.getLength(), track7.getColor(), 'TX OK',
                        track8.getClaimed(), track8.getLength(), track8.getColor(), 'CO KS',
                        track9.getClaimed(), track9.getLength(), track9.getColor(), 'CO OK',
                        track10.getClaimed(), track10.getLength(), track10.getColor(), 'KS OK',
                        dcardNames2, dcardWorth2, dcardComplete2.upper()
                        ]
        if (not limitedFlag) or bothCSVFlag:
            self.append_list_as_row(self.player1ex, robustP1Data)
            print("csv based on gameState for player 1 was successfully updated at: " + self.player1ex)
            self.append_list_as_row(self.player2ex, robustP2Data)
            print("csv based on gameState for player 2 was successfully updated at: " + self.player2ex)
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
        numCards = [0, 0, 0, '']
        for x in hand:
            if x.color == 'black':
                numCards[0] += 1
            if x.color == 'white':
                numCards[1] += 1
            numCards[2] += 1
        cardDif = numCards[0]-numCards[1]
        if cardDif < 0:
            numCards[3] = str(abs(cardDif)) + " more white"
        else:
            numCards[3] = str(cardDif) + " more black"

        return numCards

    def formatDestinationCards(self, dcard):
        toReturn = ''
        for x in dcard:
            toReturn += x.toString() + " and "
        return toReturn[:-5]
    # def output(self):
    #     return [self.turn,]

    def sortedDestination(self, dcard):
        for x in range(0, len(dcard), 1):
            for y in range(0, len(dcard), 1):
                if dcard[x].citiesNoPoints() < dcard[y].citiesNoPoints():
                    #print(dcard[x].citiesNoPoints())
                    dcard[x], dcard[y] = dcard[y], dcard[x]
        return dcard


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
