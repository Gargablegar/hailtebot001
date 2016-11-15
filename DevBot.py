from hlt import *
from networking import *
from random import randint

import logging

logging.basicConfig(filename='lolog.log',level=logging.DEBUG)
logging.warning('Watch out!')  # will print a message to the console
logging.info('I told you so')  # will not print anything
# logging.info(CARDINALS) 

myID, gameMap = getInit()
# Initialise 
# Find Production Field values
# Find Spawn Point
W = gameMap.width
H = gameMap.height
# productionField = [[0 for x in range(W)] for y in range(H)]
for y in range(gameMap.height):
        for x in range(gameMap.width):
            location = Location(x, y)
            # productionField[x][y] = gameMap.getSite(location).production
            if gameMap.getSite(location).owner == myID:
                spawnPoint = location

productionMax = 0
productionMaxLocation = Location(1,1)
for y in range(spawnPoint.y,spawnPoint.y+5):
    for x in range(spawnPoint.x,spawnPoint.x+5):
        location = Location(x, y)
        if gameMap.getSite(location).production > productionMax:
            productionMax = gameMap.getSite(location).production
            productionMaxLocation = location
logging.info('Spawn Point')
logging.info(spawnPoint.x)
logging.info(spawnPoint.y)
logging.info('Production Max')
logging.info(productionMax)
logging.info('Production Max Location')
logging.info(productionMaxLocation.x)
logging.info(productionMaxLocation.y)

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
sendInit("MaxProd5x5From spawn")
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

# FOR A FIRST QUADERANT CASE ONLY 
# FUCKING 0.0 on top left fuck you images
def directionAtoB(locationA,locationB):
    Xdist = locationB.x - locationA.x
    Ydist = locationB.y - locationA.y
    if Xdist<= Ydist:
        # X stuff
        direction = EAST
    else:
        # Ydist < Xdist 
        # Y stuff
        direction = SOUTH

    return direction 

def move(location):

    site = gameMap.getSite(location)
    # logging.info('PROD')
    # logging.info(site.production) 
    # logging.info('Strangth') 
    # logging.info(site.strength) 
    #Move init
    # possibleMoves
    # Is MAX PRODUCTION 
    if location == productionMaxLocation:
        if site.strength ==255:
            return Move(location,randint(1,4))
        return Move(location, STILL)

    # # Is in Squad Check
    # SquadFlag = IsSquad(gameMap,location)
    # # SquadOrders
    
     # Wait till Friendly block is at a level of the local prodction 
    if site.strength < site.production + 5:
        return Move(location, STILL)

    # #If max strength go to lowest square
    # if site.strength >=250:
    #     # return Move(location, lowestEnemyNeighbour(gameMap,location))
    #     return Move(location, SquadMove)
    # if SquadFlag == True and site.strength > 50:
    #     return Move(location, SquadMove)   
    # elif SquadFlag == False and site.strength > 40:
    #     # return Move(location, EAST if random.random() > 0.5 else SOUTH)  
    #     return Move(location, SquadMoveOpp) 
    #     # return Move(location,lowestEnemyNeighbour(gameMap,location))  

    for d in CARDINALS:
        neighbour_site = gameMap.getSite(location, d)
        # make go to lowest square!!! TODO
        if neighbour_site.owner != myID and neighbour_site.strength < (site.strength):
            return Move(location,directionAtoB(location,productionMaxLocation))
        else: 
            # return Move(location, SquadMove)
            return Move(location,directionAtoB(location,productionMaxLocation))
            # return Move(location, EAST if random.random() > 0.65 else STILL)

    return Move(location,directionAtoB(location,productionMaxLocation))
    
    # # return Move(location, NORTH if random.random() > 0.5 else SOUTH)
    # return Move(location,(lowestEnemyNeighbour(gameMap,location) if random.random() > 0.15 else STILL))

# Checks for lowest Friednyl neighbour - 
def lowestNeighbour(gameMap,location):
    minimium = 255

    # site could be a global var to reduce re calculation of this
    site = gameMap.getSite(location)
    
    for d in CARDINALS:
        neighbour_site = gameMap.getSite(location, d)
        # make go to lowest square!!! TODO
        if neighbour_site.strength < (minimium):
            minimium = neighbour_site.strength
            direction = d 
            # return Move(location, d)
    if minimium == 255:
        return RndDirection()
    if minimium < site.production + 3:
        return STILL
    return direction

# Checks for lowest Enemy piece on cardinal points, if none - moves to loves neighbour
def lowestEnemyNeighbour(gameMap,location):
    minimium = 260
    # site could be a global var to reduce re calculation of this
    site = gameMap.getSite(location)
    # productionValue = 5
    for d in CARDINALS:
        neighbour_site = gameMap.getSite(location, d)
        # make go to lowest square!!! TODO
        if neighbour_site.owner != myID and neighbour_site.strength < (minimium):
            minimium = neighbour_site.strength
            direction = d 
            if neighbour_site.owner != 0:
                logging.info('!neighbour_site.owner')
                logging.info(neighbour_site.owner)
            # return Move(location, d)
    # if minimium == 255:     
    #     return RndDirection()
    if minimium == 260:
        direction = lowestNeighbour(gameMap,location)
    return direction

# This is exsessive can use HLT class or numbers to random
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

# Checks to see if in a combat grouping of sorts
def IsSquad(gameMap,location):
    site = gameMap.getSite(location)
    squadCount = 1;
    for d in CARDINALS:
            neighbour_site = gameMap.getSite(location, d)
            if neighbour_site.owner == myID and neighbour_site.strength > 20:
                squadCount = squadCount + 1
    
    if squadCount >= randint(3,4):
        return True
    return False

# def SpecialSquad(location):
#     site = gameMap.getSite(location)
#     squadCount = 1;
#     for d in CARDINALS:
#             neighbour_site = gameMap.getSite(location, d)
#             if neighbour_site.owner == myID and neighbour_site.strength > 50:
#                 squadCount = squadCount + 1
#     if squadCount >= randint(3,4):
#         return True
#     return False

while True:
    moves = []
    gameMap = getFrame()

    SquadMove = (WEST if random.random() > 0.30 else SOUTH)
    
    if SquadMove == WEST:
        SquadMoveOpp = EAST
    if SquadMove ==SOUTH:
        SquadMoveOpp = NORTH
    
    SquadMoveOrigional = SquadMove
    
    for y in range(gameMap.height):
        for x in range(gameMap.width):
            location = Location(x, y)
            if gameMap.getSite(location).owner == myID:
                # SquadMove = (SquadMoveOrigional if random.random() > 0.15 else (North if random.random() > 0.30 else WEST))
                moves.append(move(location))
    sendFrame(moves)