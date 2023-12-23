import re
import queue

class Card:
    def __init__(self, id: int, winning: [], mine: []):
        self.id = id
        self.winning = winning
        self.mine = mine

    def winningNumbersCount(self):
        return len(set(self.mine).intersection(set(self.winning)))

    def getWonCardsIds(self):
        val = [int(self.id) + i + 1 for i in range(0, self.winningNumbersCount())]
        # print(self.id)
        # print(self.winningNumbersCount())
        # print(val)
        # print()
        # print()
        return val

    def cardValue(self):
        winningCount = self.winningNumbersCount()
        # print(winningCount)
        if winningCount == 0:
            return 0
        
        powerOf2 = max(winningCount - 1, 0)
        points = 1 << powerOf2
        # print(points)
        return points

    @staticmethod
    def parse(cardString):
        cardPattern = 'Card\\s+(\\d+): (.+) \\| (.+)'
        regex = re.compile(cardPattern)
        matches = regex.search(cardString)
        
        cardId = matches.group(1)
        
        winningNumbers = Card.parseNumbersList(matches.group(2))
        # print(winningNumbers)
        myNumbers = Card.parseNumbersList(matches.group(3))
        # print(myNumbers)

        return Card(cardId, winningNumbers, myNumbers)
    
    numberPattern = '\\d+'
    numberRegex = re.compile(numberPattern)

    @staticmethod
    def parseNumbersList(numbersString):
        return [int(match.group()) for match in Card.numberRegex.finditer(numbersString)]

try:
    cardValueSum = 0
    cards = {}

    filepath = 'C:\\code\\local\\aoc23\\day4\\data.txt'
    with open(filepath) as file:
        for line in file:
            parsedCard = Card.parse(line)
            cards[int(parsedCard.id)] = parsedCard

            cardValueSum += parsedCard.cardValue()
            # print()

    # part 1
    print(cardValueSum)

    cardsIdsQueue = queue.Queue()
    actualCardsCount = 0

    for cardId in cards.keys():
        cardsIdsQueue.put(cardId)

    while not cardsIdsQueue.empty():
        cardId = cardsIdsQueue.get()
        actualCardsCount += 1
        for wonCardId in (id for id in cards[cardId].getWonCardsIds() if id in cards):
            cardsIdsQueue.put(wonCardId)

    # part 2
    print(actualCardsCount)
            



except FileNotFoundError:
    print('File not found')
except IOError:
    print('An error occurred while reading the file')
