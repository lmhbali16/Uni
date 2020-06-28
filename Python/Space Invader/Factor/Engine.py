import pygame


class Engine:

    field = None
    spaceship = None
    keyEvent = ""

    width = 0
    length = 0
    finish = False
    start = False
    lose = False
    screen = None
    explosion = None

    def __init__(self, spaceship, field, width, length):
        self.spaceship = spaceship
        self.field = field
        self.width = width
        self.length = length



    def moveLeft(self):
        if self.spaceship.x - self.spaceship.xvel >= 0:
            self.spaceship.moveLeft()



    def moveRight(self):
        if self.spaceship.x + self.spaceship.xvel+self.spaceship.width < self.width:
            self.spaceship.moveRight()



    def tick(self):

        if self.keyEvent == "R":
            self.moveRight()
            self.keyEvent = ""
        elif self.keyEvent == "L":
            self.moveLeft()
            self.keyEvent = ""
        elif self.keyEvent == "SPACE":
            self.keyEvent = ""
            return None
        else:
            self.keyEvent =""

        self.field.doTimestep()
        die = self.checkClash()

        return die




    def checkClash(self):

        x = self.spaceship.x*self.field.width/self.width
        xWidth = self.spaceship.x + self.spaceship.width


        for i in self.field.asteroids:


            if i['xPos'] == x and i['yPos'] == 1:
                return True

        if self.field.finishLine == 1:
            return "WIN"


        return False

    def drawSpaceship(self, display):
        spaceshipImage = pygame.image.load(self.spaceship.image)

        spaceshipImage = pygame.transform.scale(spaceshipImage, (self.spaceship.width, self.spaceship.length))
        display.blit(spaceshipImage, (self.spaceship.x+self.field.cellWidth/3, self.spaceship.y))

    def drawAsteroid(self, display):
        asteroidList = self.field.asteroids
        astImg = self.field.asteroidImage
        for i in range(self.field.numAsteroids):
            asteroid = asteroidList[i]
            display.blit(astImg,(asteroid['xPos']*self.field.cellWidth+self.field.cellWidth/3,self.length-asteroid['yPos']*self.field.cellHeight))

    def drawField(self,display):
        fieldImage = self.field.fieldImage
        fieldImage = pygame.transform.scale(fieldImage,(self.width,self.length))
        display.blit(fieldImage,(0,0))

    def drawFinish(self,display):
        if(self.field.finishLine<=self.field.height):
            finishImage = self.field.finishImage
            finishImage = pygame.transform.scale(finishImage,(self.width,int(self.length/self.field.height)))
            display.blit(finishImage,(0,self.length-self.field.finishLine*self.field.cellHeight))

    def drawPause(self,display):
        pauseImage = self.field.pauseImage
        pauseImage = pygame.transform.scale(pauseImage,(self.width,self.length))
        display.blit(pauseImage,(0,0))

    def draw(self,display):
        self.drawField(display)
        self.drawFinish(display)
        self.drawAsteroid(display)
        self.drawSpaceship(display)

    def drawExplosion(self, display):
        explosion = pygame.transform.scale(pygame.image.load('./images/explosion.png'),
                               (self.spaceship.width, self.spaceship.length))

        display.blit(explosion, (self.spaceship.x+self.spaceship.width, self.spaceship.y))