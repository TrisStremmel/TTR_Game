class Track():
    def __init__(self, top, left, height, width, color, img, rot):
        self.top = top
        self.left = left
        self.height = height
        self.width = width
        self.color = color
        self.img = img
        self.rot = rot

    def setTop(self,top):
        self.top = top

    def getTop(self):
        return self.top

    def setLeft(self, left):
        self.left = left

    def getLeft(self):
        return self.left

    def setHeight(self, height):
        self.height = height

    def getHight(self):
        return self.height

    def setWidth(self, width):
        self.width = width

    def getWidth(self):
        return self.width

    def setColor(self, color):
        self.color = color

    def getColor(self):
        return self.color

    def getImg(self):
        return self.img
    def getRot(self):
        return self.rot