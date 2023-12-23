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

print(xLen, yLen)

# Part 1

# Print Part 1
printProblemPartResult(1, None)

# Part 2

# Print Part 2
# printProblemPartResult(2, None)