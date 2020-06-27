import random
import pygame
class Field:




    def __init__(self, fieldConfig,screen):
        self.width = fieldConfig['numWide']
        self.height = fieldConfig['numHigh']
        self.cellWidth = screen[0]/self.width
        self.cellHeight = screen[1]/self.height
        self.numAsteroids = fieldConfig['numAsteroids']
        self.finishLine = fieldConfig['finishLine']
        self.initAsteroids()
        self.asteroidImage = pygame.image.load('images/asteroid.png')
        self.fieldImage = pygame.image.load('images/field.gif')
        self.finishImage = pygame.image.load('images/finish.png')
        self.pauseImage = pygame.image.load('images/pause.png')
    def getWidth(self):
        return self.width*self.cellWidth

    def getHeight(self):
        return self.height*self.cellHeight

    def numCells(self):
        return self.height*self.width

    def initAsteroids(self):
        self.asteroids = []
        if self.numAsteroids>self.height*self.width:
            raise Exception('Too many asteroids')
        for i in range(self.numAsteroids):
            asteroid = self.initAsteroid(self.height)
            self.asteroids.append(asteroid)
    def initAsteroid(self,spawnRange):
        unfinished = True
        while(unfinished):
            asteroid = {'xPos': random.randrange(self.width), 'yPos': random.randrange(self.height,self.height+spawnRange)}
            if asteroid in self.asteroids:
                    continue
            unfinished = None
        return asteroid
    def doTimestep(self):
        for i in range(self.numAsteroids):
            asteroid = self.asteroids[i]
            if(asteroid['yPos']==0):
                self.asteroids[i]=self.initAsteroid(2)
            else:
                asteroid['yPos']=asteroid['yPos']-1
                self.asteroids[i]=asteroid
        self.finishLine=self.finishLine-1