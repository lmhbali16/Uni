class SpaceShip:
    x = 0
    y = 0

    xvel = 0
    width = 0
    length = 0
    image = "./images/rocket.png"

    def __init__(self, x, y, xvel, width, length):
        self.x = x
        self.y = y
        self.xvel = xvel
        self.width = width
        self.length = length


    def moveLeft(self):

        self.x = self.x-self.xvel


    def moveRight(self):
        self.x += self.xvel

    def move(self):
        self.y += self.yvel


