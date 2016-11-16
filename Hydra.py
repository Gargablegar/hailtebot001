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

# main move function
def move(location):
    site = gameMap.getSite(location)
 
    if site.strength < site.production + 8:
        return Move(location, STILL)

    else:
        return Move(location,EAST)

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
        self.ProductionMatrix = np.zeros((self.gameMap.width,self.gameMap.height))
        # Spawn point 
        self.spawnPoint = Location(1,1)
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