import pygame, sys, random, math, os, copy
from pygame.locals import *

def vmag(vectorToMag):
    partialSum = 0
    for i in vectorToMag:
        partialSum += math.pow(i, 2)
    return math.sqrt(partialSum)

def vadd(vone, vtwo):
    #print(vone, vtwo)
    assert len(vone) == len(vtwo), 'to add vectors they must have equal lengths'
    ret = []
    for i in range(0, len(vone)):
        ret.append(vone[i] + vtwo[i])
    return ret

def dprod(vone, vtwo):
    assert len(vone) == len(vtwo), 'to dotprod vectors they must have equal lengths'
    parSum = 0
    #print('hey', vone, vtwo)
    for i in range(0, len(vone)):
        parSum += vone[i] * vtwo[i]
    #print(parSum)
    return parSum

def eWrap(boundVec, wrapVec):
    #print(boundVec, wrapVec)
    ret = []
    for i in range(0, len(wrapVec)):
        if wrapVec[i] > boundVec[1]:
            c = wrapVec[i] - boundVec[1] - 1
        elif wrapVec[i] < boundVec[0]:
            c = 1 + boundVec[1] - (boundVec[0] - wrapVec[i])
        else:
            c = wrapVec[i]
        ret.append(c)
    #print(ret)
    return ret

def bounder(minner, valueRun, maxer):
    #print(minner, valueRun, maxer, int(max(min(valueRun, maxer), minner)))
    return max(min(valueRun, maxer), minner)

def isBound(min, val, max):
    return min <= val <= max

class writerMine:
    def __init__(self, fonter = 't'):
        pygame.font.init()
        self.fonts = []
        for i in range(0, 100):
            self.fonts.append(i)
            #print(i)
        self.fontuse = fonter

    def addFont(self, size):
        self.fonts[size - 1] = pygame.font.SysFont(self.fontuse, size)
        #print(size, '--------------')

    def write(self, text, size):
        #print(str(size) + ', ' + text)
        text = str(text)
        if self.fonts[size - 1] == size - 1: self.addFont(size)
        #print(self.fonts[size - 1], size, text)
        disper = self.fonts[size - 1].render(text, True, (0, 0 , 0))
        disper2 = pygame.Surface(disper.get_size())
        disper2.fill((255, 255, 255))
        disper2.blit(disper, (0, 0))
        return disper2

drawSize = (600, 600)
FPS = 60
FPT = 30
TILESIZE = 60
FPSCLOCK = pygame.time.Clock()
drawsurf = pygame.Surface((1000, 1000))
mensurf = pygame.Surface((1000, 1000))
dispsurf = pygame.display.set_mode((600, 600), pygame.RESIZABLE)
tileImg = pygame.transform.scale(pygame.image.load('tile.png'), (TILESIZE, TILESIZE))
tileMap = []
emptyList = []
eList = []
snakeBits = []
controls = {
    0: {
        K_w: (0, -1),
        K_a: (-1, 0),
        K_s: (0, 1),
        K_d: (1, 0)
    },

    1: {
        K_UP: (0, -1),
        K_LEFT: (-1, 0),
        K_DOWN: (0, 1),
        K_RIGHT: (1, 0)
    },

    2: {
        K_t: (0, -1),
        K_f: (-1, 0),
        K_g: (0, 1),
        K_h: (1, 0)
    },

    3: {
        K_i: (0, -1),
        K_j: (-1, 0),
        K_k: (0, 1),
        K_l: (1, 0)
    }
}
starters = (
    (((3, 7), (2, 7), (1, 7)), (1, 0)),
    (((11, 7), (12, 7), (13, 7)), (-1, 0)),
    (((7, 3), (7, 2), (7, 1)), (0, 1)),
    (((7, 11), (7, 12), (7, 13)), (0, -1))
)


for i in range(0, 14):
    #print(i)
    useStr = str(i)
    if len(useStr) < 2:
        useStr = '0' + useStr
    snakeBits.append(pygame.image.load('Assets/Ekens/snek_' + useStr + '.png'))

drawNums = {
    (1, 0): 3,
    (-1, 0): 1,
    (0, 1): 2,
    (0, -1): 0,
    ((1, 0), (1, 0)): 5,
    ((1, 0), (0, -1)): 11,
    ((1, 0), (0, 1)): 12,
    ((-1, 0), (-1, 0)): 5,
    ((-1, 0), (0, 1)): 10,
    ((-1, 0), (0, -1)): 13,
    ((0, 1), (0, 1)): 4,
    ((0, 1), (-1, 0)): 11,
    ((0, 1), (1, 0)): 13,
    ((0, -1), (0, -1)): 4,
    ((0, -1), (1, 0)): 10,
    ((0, -1), (-1, 0)): 12
}

endNums = {
    (1, 0): 9,
    (-1, 0): 8,
    (0, 1): 7,
    (0, -1): 6
}

fruits = []
inputArr = os.listdir('Assets/Berries/')
for fileName in inputArr:
    if fileName[len(fileName) - 4:] == '.png':
        #print(fileName)
        fruits.append(pygame.image.load('Assets/Berries/' + fileName))

items = []
inputArr = os.listdir('Assets/Items/')
for fileName in inputArr:
    if fileName[len(fileName) - 4:] == '.png':
        #print(fileName, len(items))
        items.append(pygame.image.load('Assets/Items/' + fileName))



for i in range(0, 15):
    tileMap.append([])
    for j in range(0, 15):
        tileMap[i].append(-1)
        emptyList.append((i, j))
        drawsurf.blit(tileImg, (50 + TILESIZE * i, 50 + TILESIZE * j))

drawSize = (dispsurf.get_width(), dispsurf.get_height())



class Snek():
    def __init__(self, states, startArray = 'lad', startDirection = (1, 0)):
        #print(eList)
        #print(startArray)
        self.states = states
        self.snakeArray = copy.deepcopy(list(startArray))
        self.directO = startDirection
        self.grow0 = False
        self.frozen = 0
        #self.lastChange = (startDirection, startDirection)
        for i in startArray:
            #print(i)
            tileMap[i[0]][i[1]] = 5
            eList.remove(tuple(i))

    def snip(self):
        tileMap[self.snakeArray[-1][0]][self.snakeArray[-1][1]] = -1
        eList.append((self.snakeArray[-1][0], self.snakeArray[-1][1]))
        self.snakeArray = self.snakeArray[:-1]
        useNow = [self.snakeArray[-2][0] - self.snakeArray[-1][0], self.snakeArray[-2][1] - self.snakeArray[-1][1]]
        # useNow = tuple(eWrap((0, 1), useNow))\
        for i in range(0, len(useNow)):
            if abs(useNow[i]) > 1:
                useNow[i] = useNow[i] / abs(useNow[i]) * -1
        useNow = tuple(useNow)
        tileMap[self.snakeArray[-1][0]][self.snakeArray[-1][1]] = endNums[useNow]

    def update(self, directNew = False, grow = False):
        retter = {
            'eaten': False,
            'rabbit': False,
            'turtle': False,
            'spinny': False,
            'death': False
        }

        if self.frozen > 0:
            self.frozen = self.frozen - 1
            return retter
        #print(directNew)
        #print(self.snakeArray)
        useChange = (self.directO, self.directO)
        if(directNew and dprod(directNew, self.directO) == 0):
            lastDirect = self.directO
            self.directO = directNew
            useChange = (lastDirect, directNew)

        tileMap[self.snakeArray[0][0]][self.snakeArray[0][1]] = drawNums[useChange]
        destn = vadd(self.snakeArray[0], self.directO)
        destw = eWrap([0, len(tileMap) - 1], destn)
        if(destn != destw):
            if(self.states['DOWRAP']):
                #print(str(destw) + 'ONWRAP')
                self.snakeArray.insert(0, destw)
            else:
                retter['death'] = True
        else:
            #print(destw)
            self.snakeArray.insert(0, destw)

        curSpot = tileMap[self.snakeArray[0][0]][self.snakeArray[0][1]]
        if(type(curSpot) == tuple):
            if curSpot[0] == 'berry':
                if self.states['DOGROW']:
                    self.grow0 = True
                if self.states['DOSPEED']:
                    retter['eaten'] = True
            if curSpot[0] == 'item':
                id = curSpot[1]
                if id == 3:
                    self.frozen = 4
                if id == 4:
                    if len(self.snakeArray) > 3:
                        self.snip()
                if id == 0:
                    retter['rabbit'] = True
                if id == 1:
                    retter['turtle'] = True
                if id == 2:
                    retter['spinny'] = True


        if(not (grow or self.grow0)):
            self.snip()
        else:
            self.grow0 = False
            #print('t')

        #print(curSpot, self.snakeArray[0])
        if(tileMap[self.snakeArray[0][0]][self.snakeArray[0][1]] != -1):
            curSpot = tileMap[self.snakeArray[0][0]][self.snakeArray[0][1]]
            #print(curSpot, self.snakeArray[0])
            if(type(curSpot) == int):
                #print('hey')
                retter['death'] = True
        else:
            eList.remove(tuple(destw))
        tileMap[self.snakeArray[0][0]][self.snakeArray[0][1]] = drawNums[self.directO]
        #print(retter)
        # if retter['death']:
        #     for i in self.snakeArray:
        #         tileMap[i[0]][i[1]] = -1
        #         eList.append((i[0], i[1]))
        return retter


def runGame(states):
    global dispsurf, drawSize, eList, emptyList, tileMap
    eList = copy.deepcopy(emptyList)
    states = states
    fpt = FPT
    nowCount = 0
    degree = 0
    liveSnakes = 0
    snakes = []
    for i in range(0, states['SNAKES']):
        liveSnakes += 1
        #print(starters)
        snakes.append(Snek(states, starters[i][0], starters[i][1]))
    dirNexts = []
    groNexts = []
    for i in snakes:
        dirNexts.append(False)
        groNexts.append(False)
    blankSurf = pygame.Surface((1000, 1000))
    blankSurf.blit(drawsurf, (0, 0))

    for snake in snakes:
        snake.update()

    speedTicks = 0
    lastdeads = []
    while True:
        speedTicks = speedTicks - 1
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == VIDEORESIZE:
                #print(event, dispsurf.get_size())
                doIndex = 0 if event.size[0] < event.size[1] else 1
                size = bounder(50, event.size[doIndex], 800)
                drawSize = (size, size)
                dispsurf = pygame.display.set_mode((event.size[0], event.size[1]), pygame.RESIZABLE)
                dispsurf.fill((0, 0, 0))
            if event.type == KEYDOWN:
                for k, v in controls.items():
                    #print(k, v, event.key)w
                    if event.key in v:
                        #print(k, v[event.key])
                        if k < len(dirNexts):
                            dirNexts[k] = v[event.key]

        drawsurf.blit(blankSurf, (0, 0))
        countedBerries = 0
        countedItems = 0
        for i in range(0, len(tileMap)):
            for j in range(0, len(tileMap[i])):
                if tileMap[i][j] != -1:
                    #print(tileMap[i][j])
                    if type(tileMap[i][j]) == int:
                        drawsurf.blit(pygame.transform.scale(snakeBits[tileMap[i][j]], (TILESIZE, TILESIZE)), (50 + TILESIZE * i, 50 + TILESIZE * j))
                    else:
                        if tileMap[i][j][0] == 'berry':
                            #print(i, j)
                            drawsurf.blit(pygame.transform.scale(fruits[tileMap[i][j][1]], (TILESIZE, TILESIZE)), (50 + TILESIZE * i, 50 + TILESIZE * j))
                            countedBerries += 1
                        if tileMap[i][j][0] == 'item':
                            drawsurf.blit(pygame.transform.scale(items[tileMap[i][j][1]], (TILESIZE, TILESIZE)), (50 + TILESIZE * i, 50 + TILESIZE * j))
                            countedItems += 1

        if countedBerries < states['FRUITS']:
            if(len(eList) > 0):
                nowSpot = random.choice(eList)
                eList.remove(nowSpot)
                nowFruit = random.randint(0, len(fruits) - 1)
                tileMap[nowSpot[0]][nowSpot[1]] = ('berry', nowFruit)
            else:
                pygame.quit()
                sys.exit('victory')

        if countedItems < states['ITEMS']:
            if (len(eList) > 0):
                nowSpot = random.choice(eList)
                eList.remove(nowSpot)
                nowItem = random.randint(0, len(items) - 1)
                tileMap[nowSpot[0]][nowSpot[1]] = ('item', nowItem)
            else:
                pygame.quit()
                sys.exit('victory')

        dispsurf.blit(pygame.transform.rotate(pygame.transform.scale(drawsurf, (drawSize[0], drawSize[1])), degree), (0, 0))
        pygame.display.update()
        doGo = False
        doSpeed = False
        doSlow = False
        doSpin = False
        if nowCount >= fpt:
            liveSnakes = 0
            nowCount = 0
            #deads = []
            deads = []
            #lastdeads = []
            for snake in range(0, len(snakes)):
                #deads = []
                if(not snakes[snake]):
                    continue
                liveSnakes += 1
                #print(liveSnakes)
                #print(snakeNexts[snake])
                #print(snake)
                rettered = snakes[snake].update(dirNexts[snake], groNexts[snake])
                #print(rettered)
                doGo = doGo or rettered['eaten']
                doSpeed = doSpeed or rettered['rabbit']
                doSlow = doSlow or rettered['turtle']
                doSpin = doSpin or rettered['spinny']
                if rettered['death']:
                    deads.append(snake)
                if doGo:
                    #print('hey')
                    subber = math.ceil(math.floor(math.pow(fpt, 2) / 81) / 2)
                    #print(fpt, 'pre')
                    fpt = fpt - subber
                    #print(fpt, 'post')
                if doSpeed:
                    speedTicks = 100
                if doSlow:
                    fpt = min(fpt + 15, 45)
                if doSpin:
                    degree = degree + 90

            for snake in lastdeads:
                if(len(snakes) > snake):
                    #print(snake, snakes)
                    for i in snakes[snake].snakeArray:
                        tileMap[i[0]][i[1]] = -1
                        eList.append((i[0], i[1]))
            for i in range(len(lastdeads) - 1, -1, -1):
                if(len(snakes) > lastdeads[i]):
                    #print(lastdeads[i])
                    snakes.pop(lastdeads[i])
            lastdeads = copy.deepcopy(deads)

        #print(liveSnakes)
        if liveSnakes == 0:
            drawsurf.blit(blankSurf, (0, 0))
            tileMap = []
            for i in range(0, 15):
                tileMap.append([])
                for j in range(0, 15):
                    tileMap[i].append(-1)
            liveSnakes = -1
        if liveSnakes == -1:
            return

        FPSCLOCK.tick(FPS)
        nowCount = nowCount + 1 if speedTicks < 1 else nowCount + 3
        #print(nowCount)

printer = writerMine('Arial')

gameStates = {
    'DOGROW': True,
    'DOSPEED': True,
    'DOWRAP': True,
    'FRUITS': 1,
    'SNAKES': 1,
    'ITEMS': 1
}

booleanVals = (
    'DOGROW',
    'DOSPEED',
    'DOWRAP'
)

intVals = (
    ('FRUITS', 1, 50),
    ('SNAKES', 1, 4),
    ('ITEMS', 0, 50)
)

buttons = []
workPos = [50, 50]

for i in booleanVals:
    surfer = printer.write(i, 50)
    sz = surfer.get_size()
    buttons.append((workPos[0], workPos[1], sz[0], sz[1], surfer, ('TOGGLE', i)))
    workPos[1] += buttons[-1][3] + 10

for i in intVals:
    surfer = printer.write(i[0], 50)
    sz = surfer.get_size()
    buttons.append((workPos[0], workPos[1], sz[0], sz[1], surfer, ('NULL', i[0])))
    workPos[0] += buttons[-1][2] + 10

    surfer = printer.write('LESS', 50)
    sz = surfer.get_size()
    buttons.append((workPos[0], workPos[1], sz[0], sz[1], surfer, ('LESS', i[0], i[1])))
    workPos[0] += buttons[-1][2] + 10

    surfer = printer.write('MORE', 50)
    sz = surfer.get_size()
    buttons.append((workPos[0], workPos[1], sz[0], sz[1], surfer, ('MORE', i[0], i[2])))
    workPos[1] += buttons[-1][3] + 10
    workPos[0] = 50

surfer = printer.write('PLAY', 80)
sz = surfer.get_size()
buttons.append((workPos[0], workPos[1], sz[0], sz[1], surfer, ('PLAY', 'GAME')))

#runGame(gameStates)

while True:
    for e in pygame.event.get():
        if e.type == QUIT:
            pygame.quit()
            sys.exit()
        if e.type == VIDEORESIZE:
            # print(event, dispsurf.get_size())
            doIndex = 0 if e.size[0] < e.size[1] else 1
            size = bounder(50, e.size[doIndex], 800)
            drawSize = (size, size)
            dispsurf = pygame.display.set_mode((e.size[0], e.size[1]), pygame.RESIZABLE)
            dispsurf.fill((0, 0, 0))
        if e.type == MOUSEBUTTONUP:
            #print(e)
            if(e.button == 1):
                nP = (e.pos[0] / drawSize[0] * 1000, e.pos[1] / drawSize[1] * 1000)
                #print(newPos)
                for i in buttons:
                    if isBound(i[0], nP[0], i[2] + i[0]) and isBound(i[1], nP[1], i[3] + i[1]):
                        #print(i[5])
                        a = i[5]
                        if a[0] == 'NULL':
                            continue
                        if a[0] == 'TOGGLE':
                            gameStates[a[1]] = not gameStates[a[1]]
                        if a[0] == 'MORE':
                            gameStates[a[1]] = min(gameStates[a[1]] + 1, a[2])
                        if a[0] == 'LESS':
                            gameStates[a[1]] = max(gameStates[a[1]] - 1, a[2])
                        if a[0] == 'PLAY':
                            runGame(gameStates)
    mensurf.fill((0, 0, 0))
    for i in buttons:
        #print(i)
        mensurf.blit(i[4], (i[0], i[1]))
        if(i[5][0] == 'MORE' or i[5][0] == 'TOGGLE'):
            #print(i[5])
            mensurf.blit(printer.write(gameStates[i[5][1]], 50), (i[0] + i[2] + 10, i[1]))

    dispsurf.blit(pygame.transform.scale(mensurf, (drawSize[0], drawSize[1])), (0, 0))
    pygame.display.update()
    FPSCLOCK.tick(FPS)
