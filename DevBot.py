from hlt import *
from networking import *
from random import randint

import logging

logging.basicConfig(filename='lolog2.log',level=logging.DEBUG)
logging.warning('Watch out!')  # will print a message to the console
logging.info('I told you so')  # will not print anything
# logging.info(CARDINALS) 
global count
count = 0 
global attackCoolDown
attackCoolDown= 5
global attackBool
attackBool = False
global attackLocation
attackLocation= Location(1,1)
# global productionMaxLocation
# global meanProductionMaxLocation 

def productionMax(X=1,Y=1,dx=5,dy=5):
    productionMax = 0
    productionMaxLocation = Location(1,1)
    meanProductionMaxLocation = Location(1,1)
    meanProduction = 0
    meanProductionMax = 0
    
    for y in range(Y-dy,Y+dy):
        for x in range(X-dx,X+dx):
            location = Location(x, y)
            for d in CARDINALS:
                    meanProduction = meanProduction + gameMap.getSite(location,d).production
            meanProduction = meanProduction/5
            if gameMap.getSite(location).production > productionMax:
                productionMax = gameMap.getSite(location).production
                productionMaxLocation = Location(location.x, location.y)

            if meanProduction > meanProductionMax:
                meanProductionMax = meanProduction
                meanProductionMaxLocation = Location(location.x, location.y)

    return productionMaxLocation,meanProductionMaxLocation


myID, gameMap = getInit()


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

productionMaxLocation,meanProductionMaxLocation = productionMax(spawnPoint.x,spawnPoint.y,gameMap.width/2,gameMap.height/2)
productionMaxLocation = meanProductionMaxLocation

# productionMaxLocation = Location(spawnPoint.x+3,spawnPoint.y+3)
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
    Xdist = locationA.x - locationB.x
    Ydist = locationA.y - locationB.y
    if (Xdist and Ydist) < 0:
        # Quad = 4
        direction =( SOUTH if random.random() > 0.15 else EAST)
    elif (Xdist and Ydist) > 0:
        # Quad = 2
        direction = (WEST if random.random() > 0.15 else NORTH)
    elif Xdist > 0 and Ydist < 0:
        # Quad = 3
        direction = (WEST if random.random() > 0.15 else SOUTH)
    elif Xdist < 0 and Ydist > 0:
        # Quad = 1
        direction =(EAST if random.random() > 0.15 else NORTH)
    elif Xdist > 0 and Ydist ==0:
        direction = WEST
    elif Xdist < 0 and Ydist ==0:
        direction = EAST
    elif Xdist == 0 and Ydist > 0:
        direction = NORTH
    elif Xdist == 0 and Ydist < 0:
        direction = SOUTH

    # if (Xdist<= Ydist) and Xdist != 0 or Ydist ==0:
    #     # X stuff
    #     direction = EAST
    # else:
    #     # Ydist < Xdist 
    #     # Y stuff
    #     direction = SOUTH

    return direction 

def move(location):
    # Flag blocks as Scout,Production, Defensive, Offensive
    # use MapInit to figure out best path to production, and through lowest strength
    # When hit production assign blocks to Prod
    # Blocks of a certain size become defensive 
    # Block on edge with a squad, or that are in a squad under attack become offensive. 
    # Remark blocks once complete. 

    site = gameMap.getSite(location)
    # logging.info('PROD')
    # logging.info(site.production) 
    # logging.info('Strangth') 
    # logging.info(site.strength) 
    #Move init
    # possibleMoves
   

    if site.strength < site.production + 8:
        return Move(location, STILL)
   
    herp = lowestEnemyNeighbour(gameMap,location)
    derp = gameMap.getSite(location,herp)
    if derp.strength <= site.strength:
        return Move(location, lowestEnemyNeighbour(gameMap,location))
    
    # for d in CARDINALS:
    #     neighbour_site = gameMap.getSite(location, d)
    #     # make go to lowest square!!! TODO
    #     if neighbour_site.owner == 2:
    #     # if neighbour_site.owner != myID and neighbour_site.strength > (site.strength):
    #         global attackBool
    #         attackBool = True
    #         global attackLocation
    #         attackLocation= gameMap.getLocation(location, d)
   
    if attackBool:
        if site.strength >=250:
            return Move(location,directionAtoB(location,attackLocation))
    
    # Is on Max Production Point? 
    # logging.info('Production Max Location')
    # logging.info(productionMaxLocation.x)
    # logging.info(productionMaxLocation.y)
    # logging.info('Location Location')
    # logging.info(location.x)
    # logging.info(location.y)
    if (location.x == productionMaxLocation.x) and (location.y == productionMaxLocation.y) :
       
        # if site.strength >=255:
            # productionMaxLocation = productionMax(productionMaxLocation.x+randint(1,4),productionMaxLocation.y+randint(1,4))

        if site.strength >=150:
            # return Move(location,(STILL if random.random() > 0.5 else randint(1,4)))
            # count = count + 1
            # if count >= 8:
            #     count = 0
            #     global productionMaxLocation
            #     global meanProductionMaxLocation 
            #     productionMaxLocation,meanProductionMaxLocation = productionMax(productionMaxLocation.x+10,productionMaxLocation.y+10,5,5)
            return Move(location,(lowestEnemyNeighbour(gameMap,location)))
        else:
            return Move(location, STILL)
    
    elif location.x == productionMaxLocation.x+1 and location.y == productionMaxLocation.y:
        if site.strength >=150:
            return Move(location,(STILL if random.random() > 0.5 else randint(1,4)))
        else:
            return Move(location, STILL)
    elif location.x == productionMaxLocation.x-1 and location.y == productionMaxLocation.y:
        if site.strength >=150:
            return Move(location,(STILL if random.random() > 0.5 else randint(1,4)))
        else:
            return Move(location, STILL)
    elif location.x == productionMaxLocation.x and location.y == productionMaxLocation.y+1:
        if site.strength >=150:
            return Move(location,(STILL if random.random() > 0.5 else randint(1,4)))
        else:
            return Move(location, STILL)
    elif location.x == productionMaxLocation.x and location.y == productionMaxLocation.y-1:
        if site.strength >=150:
            return Move(location,(SOUTH if random.random() > 0.05 else randint(1,4)))
        else:
            return Move(location, STILL)
    # # Is in Squad Check
    # SquadFlag = IsSquad(gameMap,location)
    # # SquadOrders
    
     # Wait till Friendly block is at a level of the local prodction 


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

    # for d in CARDINALS:
    #     neighbour_site = gameMap.getSite(location, d)
    #     # make go to lowest square!!! TODO
    #     if neighbour_site.owner != myID and neighbour_site.strength < (site.strength):
    #         return Move(location,directionAtoB(location,productionMaxLocation))
    #     else: 
    #         # return Move(location, SquadMove)
    #         return Move(location,directionAtoB(location,productionMaxLocation))
    #         # return Move(location, EAST if random.random() > 0.65 else STILL)
    siteProduction = gameMap.getSite(productionMaxLocation)
    if siteProduction.owner == myID:
        return Move(location,directionAtoB(location,meanProductionMaxLocation))
    else:
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
# # init loop
# count = 0
count = 0 

while True:
    moves = []
    gameMap = getFrame()

    SquadMove = (WEST if random.random() > 0.30 else SOUTH)
    
    if SquadMove == WEST:
        SquadMoveOpp = EAST
    if SquadMove ==SOUTH:
        SquadMoveOpp = NORTH
    
    SquadMoveOrigional = SquadMove
    if attackBool:
        attackCoolDown = attackCoolDown - 1
        if attackCoolDown <= 0:
            attackCoolDown = 10
            global attackBool
            attackBool = False
    attackBool = (True if random.random() > 0.50 else False)
    
    for y in range(gameMap.height):
        for x in range(gameMap.width):
            location = Location(x, y)
            if gameMap.getSite(location).owner == myID:
                # SquadMove = (SquadMoveOrigional if random.random() > 0.15 else (North if random.random() > 0.30 else WEST))
                moves.append(move(location))
   
    sendFrame(moves)