# Standard Imports
from timeit import default_timer as timer
from datetime import timedelta
import re

# Problem Imports
import math
import functools

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
    
# a = velocity = time to accelerate
# d = (t - a) * a = -a^2 + t*a
# -a^2 + t*a -d = 0
# this will find the roots where this distance is covered
# all a values between (exclusive) these roots will be valid
def getAccelerationTimesRange(time, distance):
    # -a^2 + t*a - d = 0
    a = -1
    b = time
    c = -distance
    a1, a2 = solve_quadratic(a, b, c)

    # if roots are integer, ensure next value within is selected
    inclusiveLowerBound = math.floor(a1) + 1
    inclusiveUpperBound = math.ceil(a2) - 1

    return (inclusiveLowerBound, inclusiveUpperBound)
    

def solve_quadratic(a, b, c):
    d = (b**2) - (4*a*c)
    x1 = (-b + math.sqrt(d)) / 2*a
    x2 = (-b - math.sqrt(d)) / 2*a
    return (x1, x2)

filepath = 'C:\\code\\local\\aoc23\\day6\\data.txt'
timesString, distancesString, *empty = open(filepath).read().split('\n')

timeStrings = re.findall('\\d+', timesString)
distanceStrings = re.findall('\\d+', distancesString)

# Part 1

part1Times = list(map(int, timeStrings))
part1Distances = list(map(int, distanceStrings))
variationCounts = []

for i, time in enumerate(part1Times):
    distance = part1Distances[i]
    accRange = getAccelerationTimesRange(time, distance)
    variationCount = accRange[1] - accRange[0] + 1
    variationCounts.append(variationCount)

variationCountsProduct = functools.reduce(lambda a,b: int(a)*int(b), variationCounts)

# Print Part 1
printProblemPartResult(1, variationCountsProduct)

# Part 2

part2Time = int(''.join(timeStrings))
part2Distance = int(''.join(distanceStrings))
part2AccRange = getAccelerationTimesRange(part2Time, part2Distance)
part2VariationCount = part2AccRange[1] - part2AccRange[0] + 1

# Print Part 2
printProblemPartResult(2, part2VariationCount)