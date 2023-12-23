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

nodesPattern = r'[A-Z]{3}'
nodesRegex = re.compile(nodesPattern)

filepath = r'data.txt'
file = open(filepath)

instructions = []
network = {}

instructions = [0 if char == 'L' else 1 for char in file.readline().strip()]
instructionListLength = len(instructions)

for line in file.readlines():
    if len(line) < 2:
        continue
    else:
        node, left, right = nodesRegex.findall(line)
        network[node] = (left, right)


def findInstructionCount(startNode, endNodeCondition):
    totalInstructionCount = 0
    instructionIndex = 0
    currentNode = startNode

    while not endNodeCondition(currentNode):
        direction = instructions[instructionIndex]
        currentNode = network[currentNode][direction]
        totalInstructionCount += 1
        
        instructionIndex += 1
        if instructionIndex == instructionListLength:
            instructionIndex = 0

    return totalInstructionCount


# Part 1

part1TotalInstructionCount = findInstructionCount('AAA', lambda n: n == 'ZZZ')

# Print Part 1
printProblemPartResult(1, part1TotalInstructionCount)


# Part 2

part2TotalInstructionCountLcm = 1

endsWithZ = lambda n: n.endswith('Z')
for node in network.keys():
    if node.endswith('A'):
        nodeInstructionCount = findInstructionCount(node, endsWithZ)
        print(node)
        print(nodeInstructionCount)
        part2TotalInstructionCountLcm = math.lcm(part2TotalInstructionCountLcm, nodeInstructionCount)

# Print Part 2
printProblemPartResult(2, part2TotalInstructionCountLcm)