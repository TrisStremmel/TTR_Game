import numpy as np


class GameState:
    isGameRunning = False
    playerList = []
    deck = None
    gameMap = None
    turn = 0
    playerTurn = 0

    gameState = None  # contains all previous and current turns

    def __init__(self):
        pass

    def newGame(self, numPlayers=2, numColors=2, mapFile=None, deckRules='easy', destinationCards='sparse'):
        if mapFile is None:
            self.generateMap(numPlayers, numColors)
        else:
            self.gameMap = mapFile

    def generateMap(self, numPlayers, numColors):
        vertices = max(numPlayers * 5, 30)
        self.gameMap = np.full((vertices, vertices, 3), None)

        # populate mat1 with lengths
        # mat2 = ownership
        # mat3 = color
        # only fill half the mats, otherwise flatten won't work right

        # start with random lengths with a min 2 max 7-10
        # remove connections so that max edges to a single vertex is 4-5
        # check triangles between every three nodes, adjust or delete lengths
        # possibly solution to crosses, compare triangles and eliminate similar ones with common connections..

        # a better method would track real x y coordinates and place only possible connections

    def getFeatures(self):
        # eventually should use 'names' of vertices to return a list of feature names making data more human readable

        mapFeatures = self.gameMap[~np.isnan(self.gameMap)].flatten()
        handFeatures = np.array([x.hand for x in self.playerList]).flatten()
        playerScores = np.array([x.score for x in self.playerList]).flatten()

        return np.concatenate((self.turn, self.playerTurn, mapFeatures, handFeatures, playerScores))

    def takeTurn(self, player, action):
        act, arg0, arg1 = action

        # only works for easy or random deckRules
        # if easy arg0 = color, arg1 = None
        # if random, both args do nothing
        if act == 'draw':
            self.playerList[player].draw(self.deck, arg0)

        # arg0 = vertex1, arg1 = vertex2
        if act == 'claim':
            self.playerList[player].claim(arg0, arg1)

        self.appendGameState()

    def appendGameState(self):
        if self.GameState is None:
            self.GameState = self.getFeatures()
        else:
            self.GameState = np.concatenate(self.GameState, self.getFeatures())

    def save(self):
        np.savetxt("GameState.csv",self.GameState)

    def load(self, fileat):
        self.GameState = np.loadtxt("GameState.csv")


class Deck:
    rules = None
    wildcards = None
    numColors = None

    def __init__(self, numColors, deckRules='easy', wildcards=False):
        self.rules = deckRules
        self.wildcards = wildcards
        self.numColors = numColors

    # full deck system = random draw and face up cards to choose from
    # - would require changes to actions to provide feedback on first choice

    # easy = ai gets choice of how many cards it wants

    # random = choosing draw is a two cards from top of randomized deck

    #
    def draw(self, color):
        if self.rules == 'easy':
            pass  # return chosen colored card

        elif self.rules == 'random':
            pass  # return random colored card


class Player:
    hand = []
    score = None

    def __init__(self, startingHand):
        self.hand = startingHand
        self.score = 0

    def draw(self, deck, color=None):
        self.hand.append(deck.draw(color))

    def claim(self, vert0, vert1):
        pass
        # claims vertex at location by setting ownership matrix, and using cards from hand
        # must perform check whether hand contains cards necessary