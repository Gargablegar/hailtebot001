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


sendInit("ROFL_eastWEST")
# https://halite.io/basics_improve_random.php
# logging.info(gameMap)
# Move function, that does not move if at 0 strength

# class possibleMoves:
#     def __init__(self, gameMap, location):
#         self.gameMap = gameMap
#         self.lcoation = location
#     """Class that returns """

    # #Nearest weakest ally
    # directionWeakAlly
    # #Nearest weakest enemy
    # directionWeakEnemy

    # #Highest neighbouring Enemy Production
    # directionHighEnemyProd
    
    # #Highest neighbouring Friendly Production
    # directionHighFriendlyProd
    
def move(location):
    site = gameMap.getSite(location)

    #Move init
    # possibleMoves

    # Is in Squad Check
    SquadFlag = IsSquad(location)
    # SquadOrders
    

    #IF max strength go to lowest square
    if site.strength >=250:
        # return Move(location, lowestEnemyNeighbour(gameMap,location))
        return Move(location, SquadMove)
     #    # GOTO weakest Ally or Enemy
     #    return Move(location,WEST)
    
     # Wait till Friendly block is at a level of the local prodction 
     # !!! RND 4
    if site.strength < site.production + 4:
        logging.info(site.strength)
        logging.info(site.production) 
        return Move(location, STILL)

    if SquadFlag == False and site.strength > 70:
        # return Move(location, EAST if random.random() > 0.5 else SOUTH)   
        return Move(location,lowestEnemyNeighbour(gameMap,location))   
    if SquadFlag == True and site.strength > 50:
        return Move(location, SquadMove)   

    for d in CARDINALS:
        neighbour_site = gameMap.getSite(location, d)
        # make go to lowest square!!! TODO
        if neighbour_site.owner != myID and neighbour_site.strength < (site.strength):
            return Move(location, d)
        else: 
            # return Move(location, SquadMove)
            return Move(location,lowestNeighbour(gameMap,location))
            # return Move(location, EAST if random.random() > 0.65 else STILL)

    return Move(location, NORTH if random.random() > 0.5 else SOUTH)

def lowestNeighbour(gameMap,location):
    minimium = 255
    for d in CARDINALS:
        neighbour_site = gameMap.getSite(location, d)
        # make go to lowest square!!! TODO
        if neighbour_site.strength < (minimium):
            minimium = neighbour_site.strength
            direction = d 
            # return Move(location, d)
    if minimium == 255:
        return RndDirection()
    return direction

def lowestEnemyNeighbour(gameMap,location):
    minimium = 255
    for d in CARDINALS:
        neighbour_site = gameMap.getSite(location, d)
        # make go to lowest square!!! TODO
        if neighbour_site.owner != myID and neighbour_site.strength < (minimium):
            minimium = neighbour_site.strength
            direction = d 
            # return Move(location, d)
        else:
            direction = RndDirection()
    return direction

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
            if neighbour_site.owner == myID and neighbour_site.strength > 50:
                squadCount = squadCount + 1
    if squadCount >= randint(2,3):
        return True
    return False

while True:
    moves = []
    gameMap = getFrame()
    SquadMove = (WEST if random.random() > 0.40 else SOUTH)

    for y in range(gameMap.height):
        for x in range(gameMap.width):
            location = Location(x, y)
            if gameMap.getSite(location).owner == myID:

                moves.append(move(location))
    sendFrame(moves)