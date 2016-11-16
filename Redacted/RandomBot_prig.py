from hlt import *
from networking import *
from random import randint

import logging

logging.basicConfig(filename='example.log',level=logging.DEBUG)
logging.warning('Watch out!')  # will print a message to the console
logging.info('I told you so')  # will not print anything
logging.info(CARDINALS) 

myID, gameMap = getInit()
# Initialise
# w = gameMap.width
# y = gameMap.height
# ProducitonMatrix = [[0 for x in range(w)] for y in range(h)] 
# for y in range(gameMap.height):
#     for x in range(gameMap.width):
#         location = Location(x, y)
#         site = gameMap.getSite(location)
#         ProducitonMatrix[x][y] = site.production
#         # if gameMap.getSite(location).owner == myID:
#         #     moves.append(move(location))

# logging.info(ProducitonMatrix)
# logging.info('Ayylmao_lets')


sendInit("Ayylmao_lets go WESTbot")
# https://halite.io/basics_improve_random.php
# logging.info(gameMap)
# Move function, that does not move if at 0 strength

def move(location):
    site = gameMap.getSite(location)
    SquadFlag = IsSquad(location)

    if site.strength < site.production + 4:
        return Move(location, STILL)
    if SquadFlag == False and site.strength > 50:
        # return Move(location, EAST if random.random() > 0.5 else SOUTH)   
        return Move(location,RndDirection())   
    if SquadFlag == True and site.strength > 50:
        return Move(location,WEST)   

    for d in CARDINALS:
        neighbour_site = gameMap.getSite(location, d)
        if neighbour_site.owner != myID and neighbour_site.strength < (site.strength):
            return Move(location, d)
        else: 
            return Move(location, STILL)

    return Move(location, NORTH if random.random() > 0.5 else WEST)

def RndDirection():
    i = randint(1,4)
    if i == 1:
        return NORTH
    if i == 2:
        return EAST
    if i == 3:
        return SOUTH
    if i == 4:
        return WEST
    return STILL

def IsSquad(location):
    site = gameMap.getSite(location)
    squadCount = 1;
    for d in CARDINALS:
            neighbour_site = gameMap.getSite(location, d)
            if neighbour_site.owner == myID and neighbour_site.strength > 40:
                squadCount = squadCount + 1
    if squadCount >= 3:
        return True            
    return False


while True:
    moves = []
    gameMap = getFrame()

    for y in range(gameMap.height):
        for x in range(gameMap.width):
            location = Location(x, y)
            if gameMap.getSite(location).owner == myID:
                moves.append(move(location))
    sendFrame(moves)