import pygame
import time
from Factor.JSONFactor import JSONFactor
from Factor.Engine import Engine
from Classifier.Classifier1 import *
from data.filter import *

test = JSONFactor("config.json")
testField = test.createField()
timeStep = test.data["field"]["timeStep"]

spaceship = test.createSpaceShip()

screenWidth, screenLength = test.getScreen()

engine = Engine(spaceship, testField, screenWidth, screenLength)

running = True
pause = True
#pause = False

pygame.init()

display = pygame.display.set_mode((screenWidth, screenLength))

pygame.display.set_caption("Space Invaders")


gameOver = pygame.font.Font('freesansbold.ttf', 24)
gameOver = gameOver.render("Game over, you lost!", True, (255, 255, 255), None)
winGame = pygame.image.load('images/win.png')
winGame = pygame.transform.scale(winGame,(engine.width,engine.length))




while running:


    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            #if event.key == pygame.K_LEFT:
             #   engine.keyEvent = "L"
            #if event.key == pygame.K_RIGHT:
             #   engine.keyEvent = "R"
            if event.key == pygame.K_SPACE:
                pause = (not pause)
                engine.keyEvent = "SPACE"

    wave = filter(2)
    prediction = Classifier(wave)[-1]
    #prediction = predict([wave])

    if prediction == "L":
        engine.keyEvent = "L"

    elif prediction == "R":
        engine.keyEvent = "R"


    display.fill([0, 0, 0])

    if pause:
        engine.draw(display)
        engine.drawPause(display)
        pygame.display.update()
        continue

    die = engine.tick()
    engine.draw(display)
    pygame.display.update()

    if die:
        if die == "WIN":
            time.sleep(timeStep)
            engine.drawField(display)
            display.blit(winGame, (0,0))
        else:
            display.blit(gameOver, (screenWidth/2-130, screenLength/2))
            engine.drawExplosion(display)

        running = False
        pygame.display.update()




    time.sleep(timeStep)

#time.sleep(2) #windows
pygame.quit()
time.sleep(2) #mac
quit()
