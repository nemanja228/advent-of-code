numberLookup = {
    'zero': '0',
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}

numberLookupReverse = {k[::-1]:v for (k,v) in numberLookup.items()}

def parseLineValue(line):    
    firstDigit = findFirstDigit(line, numberLookup)
    lastDigit = findFirstDigit(line[::-1], numberLookupReverse)

    if firstDigit == None and lastDigit == None:
        return 0
    elif firstDigit == None:
        return lastDigit
    elif lastDigit == None:
        return firstDigit
    else:
        return firstDigit + lastDigit


def findFirstDigit(line, currentNumberLookup):
    current = ''

    for c in line:
        if c.isdigit():
            return c
        
        current += c
        if current in currentNumberLookup:
            return currentNumberLookup[current]
        
        for key in currentNumberLookup.keys():
            if (current.find(key) > 0):
                return currentNumberLookup[key]

    return None

try:
    calibrationSum = 0
    
    with open('data.txt') as file:
        for line in file:
            lineValue = parseLineValue(line)
            calibrationSum += int(lineValue)

    print(calibrationSum)

except FileNotFoundError:
    print('File not found')
except IOError:
    print('An error occurred while reading the file')
except Exception as err:
    print('Error occurred:', err)
