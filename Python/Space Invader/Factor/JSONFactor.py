import json
from Field.Field import Field
from Object.SpaceShip import SpaceShip

class JSONFactor:

    data = None

    def __init__(self, file):

        with open(file, 'r') as f:
            self.data = json.load(f)

    def createField(self):
        return Field(self.data['field'],self.getScreen())


    def createSpaceShip(self):

        spaceshipData = self.data['spaceship']
       # x = spaceshipData['x']
        y = spaceshipData['y']
        width = spaceshipData['width']
        length = spaceshipData['length']

        field = self.data['field']

        x = self.getScreen()[0]/field["numWide"] * int(field["numWide"]/2)

        spaceship = SpaceShip(x,y,self.getScreen()[0]/field["numWide"],width,length)

        return spaceship


    def getScreen(self):

        return self.data['width'], self.data['length']