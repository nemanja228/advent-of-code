# Standard Imports
from timeit import default_timer as timer
from datetime import timedelta
import re

# Problem Imports
import sys
from enum import Enum

# Start Timing
startTime = timer()

# Standard Helpers
def printProblemPartResult(part, result):
    partTime = timer()
    print()
    print('Part ' + str(part))
    print('Result = ' + str(result))
    print('{0} ms'.format(timedelta(seconds=partTime-startTime).total_seconds() * 1000))
    print() 


# # # # # # # # #
# Problem solving
# # # # # # # # #

StartTileSymbol = 'S'
Direction = Enum('Direction', [ 'Up', 'Down', 'Left', 'Right' ])

validDirectionsFromSymbol = {
    ('|', Direction.Up):  Direction.Down,
    ('|', Direction.Down):  Direction.Up,
    ('-', Direction.Left):  Direction.Right,
    ('-', Direction.Right):  Direction.Left,
    ('J', Direction.Up):  Direction.Left,
    ('J', Direction.Left):  Direction.Up,
    ('L', Direction.Up):  Direction.Right,
    ('L', Direction.Right):  Direction.Up,
    ('7', Direction.Down):  Direction.Left,
    ('7', Direction.Left):  Direction.Down,
    ('F', Direction.Down):  Direction.Right,
    ('F', Direction.Right):  Direction.Down,
}

reverseDirectionMap = {
    Direction.Up: Direction.Down,
    Direction.Down: Direction.Up,
    Direction.Left: Direction.Right,
    Direction.Right: Direction.Left,
}

def calculateNextTileIndex(tileIndex, directionFromTile):
    if directionFromTile == Direction.Up and tileIndex[0] - 1 > -1:
        return (tileIndex[0] - 1, tileIndex[1])
    if directionFromTile == Direction.Left and tileIndex[1] - 1 > -1:
        return (tileIndex[0], tileIndex[1] - 1)
    if directionFromTile == Direction.Down and tileIndex[0] + 1 < gridHeight:
        return (tileIndex[0] + 1, tileIndex[1])
    if directionFromTile == Direction.Right and tileIndex[1] + 1 < gridWidth:
        return (tileIndex[0], tileIndex[1] + 1)
    return None
      
def tileFromGrid(tileIndexTuple):
    return grid[tileIndexTuple[0]][tileIndexTuple[1]]
      
def findStartIndexTuple():
    for i, row in enumerate(grid):
        for j, element in enumerate(row):
            if element[0] == StartTileSymbol:
                return (i, j)

def buildPath(startIndex, directionFromStart):
    path = []
    startDistance = 0

    currentNode = (startIndex, startDistance)
    path.append(currentNode)

    currentIndex = startIndex
    directionFromTile = directionFromStart

    while True:
        currentIndex = calculateNextTileIndex(currentIndex, directionFromTile)
        if currentIndex == None:
            return path, False
        
        if currentIndex == startIndex:
            return adjustPathDistances(path), True

        symbol, visitedFrom = tileFromGrid(currentIndex)        
        reverseDirection = reverseDirectionMap[directionFromTile]
        
        if (symbol, reverseDirection) not in validDirectionsFromSymbol:
            return path, False
        
        if reverseDirection in visitedFrom:
            return path, False
        
        startDistance += 1
        path.append((currentIndex, startDistance))

        visitedFrom.append(reverseDirection)
        directionFromTile = validDirectionsFromSymbol[(symbol, reverseDirection)]


def adjustPathDistances(path):
    pathLen = len(path)
    midPointIndex = pathLen // 2 + 1
    return path[:midPointIndex] + [(n[0], pathLen - n[1]) for n in path[midPointIndex:]]


filepath = r'data.txt'
fileContent = open(filepath)

# grid[x][y] = [tile, visitedFrom]
grid = []
gridHeight = 0
gridWidth = 0

for line in fileContent.readlines():
    if line[0] == '\n':
        continue
    strippedLine = line.strip()
    grid.append([(tile, []) for tile in strippedLine])
    if gridWidth == 0:
        gridWidth = len(strippedLine)
    gridHeight += 1

# Part 1

startIndex = findStartIndexTuple()
longestDistance = sys.maxsize
actualPath = []
for d in Direction:
    path, pathClosed = buildPath(startIndex, d)
    if pathClosed:
        # distance
        longestDistance = max((x[1] for x in path))
        actualPath = path

# Print Part 1
printProblemPartResult(1, longestDistance)

# Part 2

def actualStartSymbolRole(startIndex):
    leftSymbol = tileFromGrid(calculateNextTileIndex(startIndex, Direction.Left))[0]
    rightSymbol = tileFromGrid(calculateNextTileIndex(startIndex, Direction.Right))[0]
    upSymbol = tileFromGrid(calculateNextTileIndex(startIndex, Direction.Up))[0]
    downSymbol = tileFromGrid(calculateNextTileIndex(startIndex, Direction.Down))[0]

    hasLeftEdge = True if (leftSymbol, Direction.Right) in validDirectionsFromSymbol else False
    hasRightEdge = True if (rightSymbol, Direction.Left) in validDirectionsFromSymbol else False
    hasUpEdge = True if (upSymbol, Direction.Down) in validDirectionsFromSymbol else False
    hasDownEdge = True if (downSymbol, Direction.Up) in validDirectionsFromSymbol else False

    if hasLeftEdge and hasRightEdge:
        return '-'
    elif hasUpEdge and hasDownEdge:
        return '|'
    elif hasLeftEdge and hasDownEdge:
        return '7'
    elif hasLeftEdge and hasUpEdge:
        return 'J'
    elif hasRightEdge and hasDownEdge:
        return 'F'
    elif hasRightEdge and hasUpEdge:
        return 'L'
    else:
        return None
        

# ray tracing from left to right, if odd number of edges before non-edge hit, point is inside path
pathIndexes = { node[0] for node in actualPath }
pointsInsidePath = 0
for i, row in enumerate(grid):
    isInside = False
    activePathEdge = False
    edgeStartDirection = None
    for j, element in enumerate(row):
        if (i, j) in pathIndexes:
            symbol = element[0]
            if symbol == 'S':
                symbol = actualStartSymbolRole((i, j))

            if symbol == '|':
                isInside = not isInside
            elif symbol == 'F':
                activePathEdge = True
                edgeStartDirection = Direction.Down
            elif symbol == 'L':
                activePathEdge = True
                edgeStartDirection = Direction.Up
            # ignore '-'
            elif symbol == 'J':
                if activePathEdge and edgeStartDirection == Direction.Down:
                    isInside = not isInside
                edgeStartDirection = None
                activePathEdge = False
            elif symbol == '7':
                if activePathEdge and edgeStartDirection == Direction.Up:
                    isInside = not isInside
                edgeStartDirection = None
                activePathEdge = False
        else:
            if isInside and not activePathEdge:
                pointsInsidePath += 1
                
    print(i+1, pointsInsidePath)

# Print Part 2
printProblemPartResult(2, pointsInsidePath)   