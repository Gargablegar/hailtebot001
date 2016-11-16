from hlt import *
from networking import *
from random import randint
import numpy as np
import logging

f = open('HYDRA_TXT_LOG.txt','w')
f.write('Log init')
f.close()
# Init
# timeouts and repeated counters
# Production Zones
# Lowest strength within 5

# [][] array with info holding
# Scount - scan 5x5 block around it - head for high production low strength - depending on own strength
# Production - Sit on a production block 
# Defensive - move to perimeter wall and hold
# Offensive - Plough through perimiter wall / activly respond to enemy engagments


# check what class of block the location is
# ACTION based on class
# Mark new class of block (accounting for move)





logging.basicConfig(filename='HYDR_LOG.log',level=logging.DEBUG)
logging.warning('Session Start ----------------------+') 
logging.info('info start') 

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


def move(location):
    # Flag blocks as Scout,Production, Defensive, Offensive
    # use MapInit to figure out best path to production, and through lowest strength
    # When hit production assign blocks to Prod
    # Blocks of a certain size become defensive 
    # Block on edge with a squad, or that are in a squad under attack become offensive. 
    # Remark blocks once complete. 
    site = gameMap.getSite(location)
 
    if site.strength < site.production + 8:
        return Move(location, STILL)

    else:
        return Move(location,EAST)

   
    # # return Move(location, NORTH if random.random() > 0.5 else SOUTH)
    # return Move(location,(lowestEnemyNeighbour(gameMap,location) if random.random() > 0.15 else STILL))



class gameData:
    def __init__(self, myID,gameMap):
        self.gameMap = gameMap
        self.myID = myID
        # Empty array of 0 for unknown or init
        # 1 for Scout
        # 2 for Production
        # 3 for Defense
        # 4 for Offense
        logging.info('DEBUG::::')
        logging.info(self.gameMap.width)
        logging.info(self.myID)
        logging.info(self.gameMap)
        
        self.blockTypeMatrix = np.zeros((gameMap.width,gameMap.height))
        
        for y in range(gameMap.height):
            for x in range(gameMap.width):
                location = Location(x, y)
                # productionField[x][y] = gameMap.getSite(location).production
                if self.gameMap.getSite(location).owner == myID:
                    self.spawnPoint = location
                    self.blockTypeMatrix[self.spawnPoint.x,self.spawnPoint.y] = 1
        
        f = open('HYDRA_TXT_LOG.txt','a+')
        f.write('Game Start: \n ID:' + str(myID) + '\n')
        f.write('blockTypeMatrix::\n')
        f.close()
        self.fileWriteBlockTypes()

    def getSpawn(self):
        return self.spawnPoint
    def getBlockTypes(self):
        return self.blockTypeMatrix
    def fileWriteBlockTypes(self):
        np.savetxt('BLOCKTYPES.txt', self.blockTypeMatrix.tolist(),fmt='%1.0f', delimiter=',')
        return
    def productionMax(self):
        return
    def updateBlockType(self):
        return


# INIT GAME
myID, gameMap = getInit()
gameData = gameData(myID,gameMap)

spawnPoint= gameData.getSpawn()



# productionMaxLocation,meanProductionMaxLocation = productionMax(spawnPoint.x,spawnPoint.y,gameMap.width/2,gameMap.height/2)


# productionMaxLocation = Location(spawnPoint.x+3,spawnPoint.y+3)
logging.info('Spawn Point')
logging.info(spawnPoint.x)
logging.info(spawnPoint.y)
# logging.info('Production Max')
# logging.info(productionMax)
# logging.info('Production Max Location')
# logging.info(productionMaxLocation.x)
# logging.info(productionMaxLocation.y)

# Send response to indicate game is init.
sendInit("MaxProd5x5From spawn")

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