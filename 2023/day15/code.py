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

hashCache = {}

def getBoxId(string):
    if string not in hashCache:
        hashCache[string] = calcStringHash(string)
    return hashCache[string]


def calcStringHash(string):
    if string not in hashCache:
        currentValue = 0
        for char in string:
            currentValue = calcCharHash(currentValue, char)
        hashCache[string] = currentValue
    return hashCache[string]


def calcCharHash(currentValue, char):
    currentValue += ord(char)
    currentValue *= 17
    currentValue %= 256
    return currentValue

def addLenseToBox(boxId, lenseLabel, lensFocalLength):
    box = boxes[boxId]
    lense = (lenseLabel, int(lensFocalLength))
    existingLenseIndex = next((i for i, lense in enumerate(box) if lense[0] == lenseLabel), None)
    if existingLenseIndex is not None:
        box[existingLenseIndex] = lense
    else:
        box.append(lense)

def removeLenseFromBox(boxId, lensLabel):
    box = boxes[boxId]
    existingLenseIndex = next((i for i, lense in enumerate(box) if lense[0] == lensLabel), None)
    if existingLenseIndex is not None:
        box.pop(existingLenseIndex)

testFilePath = r'test-data.txt'
filepath = r'data.txt'
values = open(filepath).readline().strip().split(',')

def calculateFocusingPower(boxes):
    sum = 0
    for k, v in boxes.items():
        for i, lense in enumerate(v):
            sum += (k + 1) * (i + 1) * lense[1]
    return sum

# Part 1

part1Sum = 0
for val in values:
    hash = calcStringHash(val)
    part1Sum += hash

# Print Part 1
printProblemPartResult(1, part1Sum)

# Part 2

boxes = {i: [] for i in range(256)}
for val in values:
    lensLabel, lensFocalLength = None, None
    if '-' in val:
        lensLabel = val.split('-')[0]
    else:
        lensLabel, lensFocalLength = val.split('=')
    boxId = calcStringHash(lensLabel)
    if lensFocalLength:
        addLenseToBox(boxId, lensLabel, lensFocalLength)
    else:
        removeLenseFromBox(boxId, lensLabel)

focusingPower = calculateFocusingPower(boxes)

# Print Part 2
printProblemPartResult(2, focusingPower)