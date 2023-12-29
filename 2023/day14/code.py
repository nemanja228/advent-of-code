# Standard Imports
from timeit import default_timer as timer
from datetime import timedelta

# Problem Imports
import numpy as np

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

def rollNorth(grid):
    newGrid = np.full_like(grid, '.')
    for j in range(grid.shape[1]):
        nextInsertIndex = 0
        for i in range(grid.shape[0]):
            element = grid[i, j]
            if element == 'O':
                newGrid[nextInsertIndex, j] = 'O'
                nextInsertIndex += 1
            elif element == '#':
                newGrid[i, j] = '#'
                nextInsertIndex = i + 1
    return newGrid

def rollSouth(grid):
    newGrid = np.full_like(grid, '.')
    for j in reversed(range(grid.shape[1])):
        nextInsertIndex = grid.shape[0] - 1
        for i in reversed(range(grid.shape[0])):
            element = grid[i, j]
            if element == 'O':
                newGrid[nextInsertIndex, j] = 'O'
                nextInsertIndex -= 1
            elif element == '#':
                newGrid[i, j] = '#'
                nextInsertIndex = i - 1
    return newGrid

def rollWest(grid):
    newGrid = np.full_like(grid, '.')
    for i in range(grid.shape[0]):
        nextInsertIndex = 0
        for j in range(grid.shape[1]):
            element = grid[i, j]
            if element == 'O':
                newGrid[i, nextInsertIndex] = 'O'
                nextInsertIndex += 1
            elif element == '#':
                newGrid[i, j] = '#'
                nextInsertIndex = j + 1
    return newGrid

def rollEast(grid):
    newGrid = np.full_like(grid, '.')
    for i in reversed(range(grid.shape[0])):
        nextInsertIndex = grid.shape[1] - 1
        for j in reversed(range(grid.shape[1])):
            element = grid[i, j]
            if element == 'O':
                newGrid[i, nextInsertIndex] = 'O'
                nextInsertIndex -= 1
            elif element == '#':
                newGrid[i, j] = '#'
                nextInsertIndex = j - 1
    return newGrid


def calculateScore(grid):
    sum = 0
    maxScore = grid.shape[0]
    for i in range(grid.shape[0]):
        multiplier = maxScore - i
        for j in range(grid.shape[1]):
            if grid[i, j] == 'O':
                sum += multiplier
    return sum


testFilePath = r'test-data.txt'
filepath = r'data.txt'

grid = np.array([[c for c in line.strip()] for line in open(filepath).read().strip().split('\n')])
# print(grid)
# print()

# Part 1
rolled = rollNorth(grid)
# print(rolled)
score = calculateScore(rolled)

# Print Part 1
printProblemPartResult(1, score)

# Part 2

def rollCycle(grid):
    return rollEast(rollSouth(rollWest(rollNorth(grid))))

oldGrid = grid
prevGrids = []

loops = 1000000000
repeatStart = None
repeatLength = None

for x in range(loops):
    newGrid = rollCycle(oldGrid)
    for i, prevGrid in enumerate(prevGrids):
        if (np.array_equal(prevGrid, newGrid)):
            repeatStart = i
            repeatLength = x - repeatStart
            break
    if repeatLength != None:
        break
    prevGrids.append(newGrid)
    oldGrid = newGrid

scoringGridIndex = repeatStart + ((loops - repeatStart - 1) % repeatLength)
scoringGrid = prevGrids[scoringGridIndex]
scorePart2 = calculateScore(scoringGrid)

# # Print Part 2
printProblemPartResult(2, scorePart2)
