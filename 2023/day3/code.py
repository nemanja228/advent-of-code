import re
import functools
import pprint

def getRangeFromMatch(match, lineLength):
    start, end = match.span()

    start = max(start - 1, 0)
    end = min(end, lineLength - 1)

    return (start, end)

def getGearCoordinateFromMatch(match, rowIndex):
    return (rowIndex, match.start())

def validateRange(value, currRange, rowIndex):
    valid = validateRangeInRow(value, currRange, rowIndex - 1)
    valid |= validateRangeInRow(value, currRange, rowIndex)
    valid |= validateRangeInRow(value, currRange, rowIndex + 1)
    return valid
 

def validateRangeInRow(value, currRange, rowIndex):
    if rowIndex < 0 or rowIndex >= len(lineValidRangesGears):
        return False
    
    adjacentGears = set()
    valid = False
    for validRangeGear in lineValidRangesGears[rowIndex]:
        if rangeIntersection(currRange, validRangeGear[0]):
            valid |= True
            for gear in validRangeGear[1]:
                adjacentGears.add(gear)
    
    for gear in adjacentGears:
        if gear not in gearPartNumbers:
            gearPartNumbers[gear] = []
        gearPartNumbers[gear].append(value)

    return valid
    

def rangeIntersection(r1, r2):
    intersection = getSetFromRange(r1).intersection(getSetFromRange(r2))
    return len(intersection) 


def getSetFromRange(r):
    return set(range(*r))


try:
    partNumberSum = 0
    lineValidRangesGears = []

    gearPartNumbers = {}
    
    symbolPattern = r'[^\w\s\.]'
    symbolRegex = re.compile(symbolPattern)

    partNumberPattern = r'\d+'
    partNumberRegex = re.compile(partNumberPattern)

    filepath = 'C:\\code\\local\\aoc23\\day3\\data.txt'
    with open(filepath) as file:
        for i, line in enumerate(file):
            lineRangesGears = []

            for match in symbolRegex.finditer(line):
                currRange = getRangeFromMatch(match, len(line))
                currGear = getGearCoordinateFromMatch(match, i)
                currRangeAndGear = (currRange, [ currGear ])    
                lineRangesGears.append(currRangeAndGear)
                lastRangeGear = currRangeAndGear
            
            lineValidRangesGears.append(lineRangesGears)

    # print (lineValidRangesGears)

    with open(filepath) as file:
        for i, line in enumerate(file):
            for match in partNumberRegex.finditer(line):
                partNumber = match.group()
                currRange = getRangeFromMatch(match, len(line))
                print(i, currRange)
                valid = validateRange(partNumber, currRange, i)
                print(valid)
                if valid:
                    partNumberSum += int(match.group())

    #part1
    print(partNumberSum)

    # pprint.pprint(gearPartNumbers)
    gearRatios = [functools.reduce(lambda a,b: int(a)*int(b), pnl) for pnl in gearPartNumbers.values() if len(pnl) == 2]
    gearRatiosSum = sum(gearRatios)

    #part2
    print(gearRatiosSum)

except FileNotFoundError:
    print('File not found')
except IOError:
    print('An error occurred while reading the file')




        