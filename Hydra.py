from hlt import *
from networking import *
from random import randint
import numpy as np
import logging

# init text files for new logs
f = open('HYDRA_TXT_LOG.txt','w')
f.write('Log init')
f.close()
f = open('BLOCKTYPES.txt','w')
f.write('Log init\n')
f.close()

# init logging on append log file
logging.basicConfig(filename='HYDR_LOG.log',level=logging.DEBUG)
logging.warning('Session Start ----------------------+') 
logging.info('info start') 

# BUSTA MOVES SECTION
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

# FOR A FIRST QUADERANT CASE ONLY 
# FUCKING 0.0 on top left fuck you images
def directionAtoB(locationA,locationB):
    Xdist = locationA.x - locationB.x
    Ydist = locationA.y - locationB.y
    direction = RndDirection()
    if (Xdist and Ydist) < 0:
        # Quad = 4
        direction =(SOUTH if random.random() > 0.05 else EAST)
    elif (Xdist and Ydist) > 0:
        # Quad = 2
        direction = (WEST if random.random() > 0.05 else NORTH)
    elif Xdist > 0 and Ydist < 0:
        # Quad = 3
        direction = (WEST if random.random() > 0.05 else SOUTH)
    elif Xdist < 0 and Ydist > 0:
        # Quad = 1
        direction =(EAST if random.random() > 0.05 else NORTH)
    elif Xdist > 0 and Ydist ==0:
        direction = WEST
    elif Xdist < 0 and Ydist ==0:
        direction = EAST
    elif Xdist == 0 and Ydist > 0:
        direction = NORTH
    elif Xdist == 0 and Ydist < 0:
        direction = SOUTH
    # return RndDirection()
    return direction
# main move function
def move(location):
    site = gameMap.getSite(location)
    location2 = Location(1,1)
    if site.strength < site.production + 8:
        return Move(location, STILL)
    else:
        # appendLog(spawnPoint.x)
        # appendLog(spawnPoint.y)

        # appendLog(location2.x)
        # appendLog(location2.y)
        return Move(location,directionAtoB(location,productionMaxLocation))
        # return Move(location,RndDirection())

def appendLog(text='_',note ='_'):
    f = open('HYDRA_TXT_LOG.txt','a+')
    f.write('Log entry:'+note+' \n')
    f.write(str(text) +'\n')
    f.close()
    return
# gameData class with all information on map
class gameData:
    def __init__(self, myID,gameMap):
        self.gameMap = gameMap
        self.myID = myID
        # Empty array of 0 for unknown or init
        # 1 for Scout
        # 2 for Production
        # 3 for Defense
        # 4 for Offense
        self.blockTypeMatrix = np.zeros((self.gameMap.width,self.gameMap.height))
        self.updateblockTypeMatrix = np.zeros((self.gameMap.width,self.gameMap.height))
        self.ProductionMatrix = np.zeros((self.gameMap.width,self.gameMap.height))
        # Spawn point 
        self.spawnPoint = Location(1,1)

        # self.productionMaxLocation
        # self.meanProductionMaxLocation

        # find spawn
        # find production values
        # define block types
        for y in range(self.gameMap.height):
            for x in range(self.gameMap.width):
                self.location = Location(x, y)
                if self.gameMap.getSite(self.location).owner == myID:
                    self.spawnPoint = self.location
                    self.blockTypeMatrix[self.spawnPoint.y,self.spawnPoint.x] = 1
                if self.gameMap.getSite(self.location).owner != myID:
                    self.blockTypeMatrix[y,x] = self.gameMap.getSite(self.location).owner
                self.ProductionMatrix[y,x]=self.gameMap.getSite(self.location).production

        f = open('HYDRA_TXT_LOG.txt','a+')
        f.write('Game Start: \n ID:' + str(myID) + '\n')
        f.write('blockTypeMatrix::\n')
        f.close()
        self.fileWriteBlockTypes()
        self.fileWriteProductionMatrix()

    def getSpawn(self):
        return self.spawnPoint

    def getBlockTypes(self):
        return self.blockTypeMatrix

    def updateGameMap(self,gameMap):
        self.gameMap = gameMap
        for y in range(self.gameMap.height):
            for x in range(self.gameMap.width):
                self.location = Location(x, y)
                if self.gameMap.getSite(self.location).owner == myID:
                    self.blockTypeMatrix[y,x] = 1
                if self.gameMap.getSite(self.location).owner != myID:
                    self.blockTypeMatrix[y,x] = self.gameMap.getSite(self.location).owner
        return

    def fileWriteBlockTypes(self,dscString='______BlockTypes______'):
        f = open('BLOCKTYPES.txt', 'a')
        f.write(dscString+'\n')
        np.savetxt(f, self.blockTypeMatrix.tolist(),fmt='%1.0f', delimiter=',')
        f.close()
        return

    def fileWriteProductionMatrix(self,dscString='______Production______'):
        f = open('BLOCKTYPES.txt', 'a')
        f.write(dscString+'\n')
        np.savetxt(f, self.ProductionMatrix.tolist(),fmt='%3.0f', delimiter=',')
        f.close()
        ff = open('TEMPNP', 'w')
        np.savetxt(ff, self.ProductionMatrix.tolist(),fmt='%3.0f', delimiter=',')
        ff.close()
        return

    def findProductionMax(self,X=1,Y=1,dx=5,dy=5):
        productionMax = 0
        productionMaxLocation = Location(1,1)
        meanProductionMaxLocation = Location(1,1)
        meanProduction = 0
        meanProductionMax = 0

        for y in range(Y-dy,Y+dy):
            for x in range(X-dx,X+dx):
                location = Location(x, y)
                meanProduction = 0
                for d in CARDINALS:
                    meanProduction = meanProduction + self.gameMap.getSite(location,d).production
                meanProduction = meanProduction/4
                if self.gameMap.getSite(location).production > productionMax:
                    productionMax = self.gameMap.getSite(location).production
                    productionMaxLocation = Location(location.x,location.y)
                if meanProduction > meanProductionMax:
                    meanProductionMax = meanProduction
                    meanProductionMaxLocation = Location(location.x, location.y)

        self.productionMaxLocation = productionMaxLocation
        self.meanProductionMaxLocation = meanProductionMaxLocation
        return productionMaxLocation,meanProductionMaxLocation,meanProduction
    
    def getProductionLocation(self):
        return self.productionMaxLocation,self.meanProductionMaxLocation 

    def setBlockType(self,location=Location(1,1),blockType=0):
        self.blockTypeMatrix[location.y,location.x] = blockType
        return
    def updateBlockType(self):
        return
# INIT GAME
myID, gameMap = getInit()
# gameData INIT
gameData = gameData(myID,gameMap)
spawnPoint= gameData.getSpawn()
productionMaxLocation,meanProductionMaxLocation,meanProduction = gameData.findProductionMax(spawnPoint.x,spawnPoint.y,2,2);

appendLog(str(spawnPoint.x),'spawnPoint X')
appendLog(str(spawnPoint.y),'spawnPoint Y')
appendLog(str(productionMaxLocation.x),'maxlocation X')
appendLog(str(productionMaxLocation.y),'maxlocation Y')
appendLog(str(meanProductionMaxLocation.x),'Meanmaxlocation X')
appendLog(str(meanProductionMaxLocation.y),'Meanmaxlocation Y')
appendLog(str(meanProduction),'meanProduction')
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
    
    gameData.updateGameMap(gameMap)
    # gameData.updateBlockType()

    # SquadMove = (WEST if random.random() > 0.30 else SOUTH)
    # if SquadMove == WEST:
    #     SquadMoveOpp = EAST
    # if SquadMove ==SOUTH:
    #     SquadMoveOpp = NORTH
    # SquadMoveOrigional = SquadMove
       
    for y in range(gameMap.height):
        for x in range(gameMap.width):
            location = Location(x, y)
            if gameMap.getSite(location).owner == myID:
                moves.append(move(location))
   
    sendFrame(moves)