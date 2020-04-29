class GameState:
    #the game state is made up of data from each player which may change from turn to turn
    #and data about the game board and turn count
    #this means the AI will have access to the other player's hand and destination cards, however
    #it will not be allowed to uses that info, simply it will not be coded to ever reference those values
    def __init__(self, turn, tracks, p1hand, p2hand, p1dCards, p2dCards):
        self.p2dCards = p2dCards
        self.p1dCards = p1dCards
        self.p2hand = p2hand
        self.p1hand = p1hand
        self.turn = turn
        self.trackArray = tracks
