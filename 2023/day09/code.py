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

def extrapolatePreviousAndNextValue(sequence):
    return process(sequence)

def process(sequence):
    nextSequence = []
    previous = None
    current = None

    first = None
    last = None
    sum = 0

    for n in sequence:
        previous = current
        current = n
        if not (previous == None or current == None):
            nextSequence.append(current - previous)
        if first == None:
            first = n
        last = n
        sum += n
    
    if sum == 0:
        return (0, 0)
    
    nextFirst, nextLast = process(nextSequence)
    return (first - nextFirst, last + nextLast)


filepath = 'C:\\code\\local\\aoc23\\day9\\data.txt'
fileContent = open(filepath)

previousValuesSum = 0
nextValuesSum = 0

for line in fileContent.readlines():
    sequence = list(map(int, line.split()))
    sequencePreviousValue, sequenceNextValue = extrapolatePreviousAndNextValue(sequence)
    previousValuesSum += sequencePreviousValue
    nextValuesSum += sequenceNextValue

# Print Part 1
printProblemPartResult(1, nextValuesSum)

# Print Part 2
printProblemPartResult(2, previousValuesSum)