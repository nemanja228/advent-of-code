# Standard Imports
from timeit import default_timer as timer
from datetime import timedelta

# Problem Imports
from itertools import combinations

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

testFilePath = r'test-data.txt'
filepath = r'data.txt'
fileContent = open(filepath).read().strip()

spaceGrid = [[x for x in line.strip()] for line in fileContent.split('\n')]

xLen = len(spaceGrid[0])
yLen = len(spaceGrid)

stars = []
emptyRows = []
emptyColumns = []

for y, line in enumerate(spaceGrid):
    if all(c == '.' for c in line):
        emptyRows.append(y)
    for x, char in enumerate(line):
        if char == '#':
            stars.append((x, y))

for x in range(xLen):
    if all([line[x] == '.' for line in spaceGrid]):
        emptyColumns.append(x)

def calcDistancesSum(stars, emptyRows, emptyColumns, modifier):
    distancesSum = 0
    for (x1, y1), (x2, y2) in combinations(stars, 2):
        xStart = min(x1, x2)
        xEnd = max(x1, x2)

        yStart = min(y1, y2)
        yEnd = max(y1, y2)
        
        xDistance = (xEnd - xStart) + len([x for x in emptyColumns if xStart < x < xEnd]) * modifier
        yDistance = (yEnd - yStart) + len([y for y in emptyRows if yStart < y < yEnd]) * modifier

        distancesSum += xDistance + yDistance
        # print((x1, y1), (x2, y2), xDistance, yDistance, xDistance + yDistance)

    return distancesSum

# Part 1

# Print Part 1
printProblemPartResult(1, calcDistancesSum(stars, emptyRows, emptyColumns, 1))

# Part 2
printProblemPartResult(1, calcDistancesSum(stars, emptyRows, emptyColumns, 1000000-1))

# Print Part 2
# printProblemPartResult(2, None)