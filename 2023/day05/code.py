from timeit import default_timer as timer
from datetime import timedelta
import sys

startTime = timer()
filepath = r'data.txt'
seedsString, *mappingsString = open(filepath).read().split('\n\n')
seeds = list(map(int, seedsString.split()[1:]))

class Mapping:
    def __init__(self, mappingString):
        self.mappingRanges = [[int(n) for n in line.split()] for line in mappingString.split('\n')[1:] if len(line) > 1]
        # print(self.mappingRanges)
    
    def transform(self, val):
        for (destStart, srcStart, length) in self.mappingRanges:
            if srcStart <= val < srcStart + length:
                return val + destStart - srcStart
        return val
    
    def transformRanges(self, ranges):
        transformedRanges = []
        for (destStart, srcStart, length) in self.mappingRanges:
            srcEnd = srcStart + length
            newRanges = []
            while ranges:
                (currStart, currEnd) = ranges.pop()
                beforeMapRange = (currStart, min(srcStart, currEnd))
                if validRange(beforeMapRange):
                    newRanges.append(beforeMapRange)
                withinMapRange = (max(currStart, srcStart), min(srcEnd, currEnd))
                if validRange(withinMapRange):
                    tr = transformRange(withinMapRange, srcStart, destStart)
                    transformedRanges.append(tr)
                afterMapRange = (max(srcEnd, currStart), currEnd)
                if validRange(afterMapRange):
                    newRanges.append(afterMapRange)
            ranges = newRanges
        return transformedRanges + ranges
    
def validRange(range):
    (start, end) = range
    return end > start
    
def transformRange(range, mappingSrc, mappingDest):
    start = range[0] - mappingSrc + mappingDest
    end = range[1] - mappingSrc + mappingDest
    return (start, end)
                
mappings = [Mapping(ms) for ms in mappingsString]

part1Locations = []
for seed in seeds:
    result = seed
    for mapping in mappings:
        result = mapping.transform(result)
    part1Locations.append(result)
part1MinLocation = min(part1Locations)
part1Time = timer()

print()
print('Part 1')
print(part1MinLocation)
print('{0} ms'.format(timedelta(seconds=part1Time-startTime).total_seconds() * 1000))
print()

part2Locations = []
for seedRangeStart, seedRangeLength in list(zip(seeds[::1], seeds[1::2])):
    ranges = [(seedRangeStart, seedRangeStart + seedRangeLength)]
    for mapping in mappings:
        ranges = mapping.transformRanges(ranges)
    minRangeStart = min(ranges)[0]
    part2Locations.append(minRangeStart)
part2MinLocation = min(part2Locations)
part2Time = timer()

print()
print('Part 2')
print(part2MinLocation)
print('{0} ms'.format(timedelta(seconds=part2Time-startTime).total_seconds() * 1000))
print()