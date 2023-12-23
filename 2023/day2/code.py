import re

limits = [12, 13, 14]

class CubeSet:
    def __init__(self, red: int, green: int, blue: int):
        self.red = red
        self.green = green
        self.blue = blue
    
    colorIndexLookup = {
        'red': 0,
        'green': 1,
        'blue': 2,
    }

    def valid(self):
        return int(self.red) <= limits[0] and int(self.green) <= limits[1] and int(self.blue) <= limits[2] 

    @staticmethod
    def parse(cubeSetString):
        cubeSetValues = [0, 0, 0]
        
        colorSubsets = cubeSetString.split(',')
        for colorQuantity in colorSubsets:
            quantity, color = colorQuantity.strip().split(' ')
            cubeSetValues[CubeSet.colorIndexLookup[color]] = quantity
        
        return CubeSet(*cubeSetValues)

class Game:
    def __init__(self, id: int, sets: []):
        self.id = id
        self.sets = sets

    def valid(self):
        return all(s.valid() for s in self.sets)

    def setPowerSum(self):
        redPower = max(int(s.red) for s in self.sets)
        greenPower = max(int(s.green) for s in self.sets)
        bluePower = max(int(s.blue) for s in self.sets)

        return redPower * greenPower * bluePower

    @staticmethod
    def parse(gameString):
        gameIdPattern = 'Game (\\d+):(.*)'
        regex = re.compile(gameIdPattern)
        matches = regex.search(gameString)
        
        gameId = matches.group(1)
        
        cubeSets = []
        gameCubeSetsString = matches.group(2)
        cubeSetsStrings = gameCubeSetsString.split(';')
        for cubeSetString in cubeSetsStrings:
            cubeSets.append(CubeSet.parse(cubeSetString))
        
        return Game(gameId, cubeSets)

try:
    gameIdSum = 0
    setPowerSum = 0
    
    filepath = 'C:\\code\\local\\aoc23\\day2\\data.txt'
    with open(filepath) as file:
        for line in file:
            parsedGame = Game.parse(line)
            if (parsedGame.valid()):
                gameIdSum += int(parsedGame.id)
            setPowerSum += int(parsedGame.setPowerSum())

    print(gameIdSum)
    print(setPowerSum)

except FileNotFoundError:
    print('File not found')
except IOError:
    print('An error occurred while reading the file')
