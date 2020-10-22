# card class, holds color
class Card:
    def __init__(self, color):
        self.color = color

    def __eq__(self,obj):
        if type(obj) == Card: return self.color == obj.color
        elif type(obj) == str: return self.color == obj
        else: return False

    def getColor(self):
        return self.color

    def setColor(self, color):
        self.color = color

