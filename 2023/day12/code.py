# Standard Imports
from timeit import default_timer as timer
from datetime import timedelta
import re

# Problem Imports
import math
from itertools import product

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

def getArrangementsCount(springs, damagedCounts):
    # print(springs)
    states = generateStateTransferString(damagedCounts)
    # print(states)
    # Only in initial state
    statesMap = {0: 1}
    # print(statesMap)
    for s in springs:
        statesMap = processSpring(s, states, statesMap)

    # Full damaged springs configuration detected
    finalStateCount = statesMap.get(len(states) - 2, 0)

    # Encountered 1+ dots after full damaged configuration detection
    extFinalStateCount = statesMap.get(len(states) - 1, 0)

    return finalStateCount + extFinalStateCount


def generateStateTransferString(damagedCounts):
    # Neutral '.' as both first and last symbol
    states = '.'

    for d in damagedCounts:
        for i in range(d):
            states += '#'
        states += '.'

    return states


def processSpring(spring, states, statesMap):
    newStatesMap = {}
    statesCount = len(states)

    for stateIndex in statesMap:
        state = states[stateIndex]
        if shouldRemainInCurrentState(spring, state):
                remainInCurrentState(statesMap, newStatesMap, stateIndex)

        nextStateIndex = stateIndex + 1
        if nextStateIndex >= statesCount:
            continue

        nextState = states[nextStateIndex]
        if shouldTransitionToNextState(spring, nextState):
            transitionToNextState(statesMap, newStatesMap, stateIndex, nextStateIndex)

    # print(newStatesMap)

    return newStatesMap


# Remain in current state (loop) if on '.' and spring is '.' or '?'
def shouldRemainInCurrentState(spring, state):
    return (spring == '?' or spring == '.') and state == '.'

# Transition to next state if spring is matching next state or it's unknown
def shouldTransitionToNextState(spring, nextState):
    return spring == '?' or (spring == '.' and nextState == '.') or (spring == '#' and nextState == '#')

def remainInCurrentState(statesMap, newStatesMap, stateIndex):
    newStatesMap[stateIndex] = statesMap[stateIndex] + newStatesMap.get(stateIndex, 0)

def transitionToNextState(statesMap, newStatesMap, stateIndex, nextStateIndex):
    newStatesMap[nextStateIndex] = newStatesMap.get(nextStateIndex, 0) + statesMap[stateIndex]

testFilePath = r'.\test-data.txt'
filepath = r'.\data.txt'
fileContent = open(filepath)

arrangementsCountSumPart1 = 0
arrangementsCountSumPart2 = 0
for line in fileContent.readlines():
    if len(line) <= 2:
        continue
    springs, damaged = line.strip().split(' ')
    damagedCounts = [int(d) for d in damaged.strip().split(',')]
    arrangementsCount = getArrangementsCount(springs, damagedCounts)
    arrangementsCountSumPart1 += arrangementsCount
    # print()
    # print(springs, damaged, arrangementsCount)
    # print()
    # print()
    springsPart2 = '?'.join([springs] * 5)
    damagedCountsPart2 = damagedCounts * 5
    arrangementsCountPart2 = getArrangementsCount(springsPart2, damagedCountsPart2)
    arrangementsCountSumPart2 += arrangementsCountPart2

# Part 1

# Print Part 1
printProblemPartResult(1, arrangementsCountSumPart1)

# Part 2

# Print Part 2
printProblemPartResult(2, arrangementsCountSumPart2)