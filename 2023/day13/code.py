# Standard Imports
from timeit import default_timer as timer
from datetime import timedelta
import re

# Problem Imports
import math

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

def getPatternSums(pattern):
    rowSums = []
    columnSums = []
    for i, line in enumerate(pattern.split('\n')):
        rowSums.append(0)
        for j, char in enumerate(line):
            rowSums[i] += 2**j if char == '#' else 0
            if i == 0:
                columnSums.append(0)
            columnSums[j] += 2**i if char == '#' else 0
    # print()
    return rowSums, columnSums

def countsBeforeReflectionLine(rowSums, columnSums, part1Counts = None):
    if part1Counts is None:
        rowCount = countBeforeReflectionLine(rowSums)
        columnCount = 0 if rowCount > 0 else countBeforeReflectionLine(columnSums)
        return rowCount, columnCount
    
    else:
        rowCountPart1, columnCountPart1 = part1Counts
        rowCountPart2 = findPart2AdjustedCount(rowSums, len(columnSums), rowCountPart1)
        if rowCountPart2 > 0 and rowCountPart2 != rowCountPart1:
            return rowCountPart2, 0

        columnCountPart2 = findPart2AdjustedCount(columnSums, len(rowSums), columnCountPart1)
        if columnCountPart2 > 0 and columnCountPart2 != columnCountPart1:
            return 0, columnCountPart2
        
        return rowCountPart1, columnCountPart1
    

def findPart2AdjustedCount(list, powerOfTwoMax, part1Count):
    for i, el in enumerate(list):
        for j in range(powerOfTwoMax):
            powerOfTwo = 1 << j
            jBitSet = el & powerOfTwo
            adjustmentValue = powerOfTwo if jBitSet == 0 else -powerOfTwo
            
            newList = list.copy()
            newList[i] += adjustmentValue
            count = countBeforeReflectionLine(newList, ignoreValue=part1Count-1)

            if count > 0 and count != part1Count:
                return count
        
    return 0


def countBeforeReflectionLine(list, ignoreValue = None):
    max = len(list) - 1
    leftCenterIndexCandidates = []

    for i, el in enumerate(list):
        if i + 1 > max:
            break

        nextEl = list[i + 1]
        if el == nextEl:
            leftCenterIndexCandidates.append(i)
            continue

    for leftIndex in leftCenterIndexCandidates:
        i = leftIndex
        j = i + 1
        reflectionBroken = False

        while i >= 0 and j <= max:
            if list[i] != list[j]:
                reflectionBroken = True
                break
            i -= 1
            j += 1

        if reflectionBroken:
            continue
        elif ignoreValue is not None and leftIndex == ignoreValue:
            continue
        else:
            return leftIndex + 1
        
    return 0


def getMultipliedCounts(rowCount, columnCount):
    return rowCount * 100 + columnCount


testFilePath = r'test-data.txt'
filepath = r'data.txt'
patterns = (text.strip() for text in open(filepath).read().strip().split('\n\n'))


totalSumPart1 = 0
totalSumPart2 = 0

for pattern in patterns:
    rowSums, columnSums = getPatternSums(pattern)

    # Part 1
    rowCountPart1, columnCountPart1 = countsBeforeReflectionLine(rowSums, columnSums)
    # print(rowCountPart1, columnCountPart1)
    totalSumPart1 += getMultipliedCounts(rowCountPart1, columnCountPart1)

    # Part 2
    rowCountPart2, columnCountPart2 = countsBeforeReflectionLine(rowSums, columnSums, (rowCountPart1, columnCountPart1))
    # print(rowCountPart2, columnCountPart2)
    totalSumPart2 += getMultipliedCounts(rowCountPart2, columnCountPart2)


# Print Part 1
printProblemPartResult(1, totalSumPart1)

# Print Part 2
printProblemPartResult(2, totalSumPart2)