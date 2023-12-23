# Standard Imports
from timeit import default_timer as timer
from datetime import timedelta
import re

# Problem Imports
from ordered_enum import OrderedEnum
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

part1CardRankList = [ 'A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2' ]
cardRankListLen = len(part1CardRankList)
part1CardRank = { el:(cardRankListLen - i + 1) for i, el in enumerate(part1CardRankList) }

part2CardRankList = [ 'A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J' ]
part2CardRank = { el:(cardRankListLen - i + 1) for i, el in enumerate(part2CardRankList) }


class CardType(OrderedEnum):
    One = 1
    Pair = 2
    TwoPairs = 3
    Three = 4
    Full = 5
    Four = 6
    Five = 7


bucketCountAndLargestBucketSizeToCartTypeLookup = {
    (1, 5): CardType.Five,
    (2, 4): CardType.Four,
    (2, 3): CardType.Full,
    (3, 3): CardType.Three,
    (3, 2): CardType.TwoPairs,
    (4, 2): CardType.Pair,
    (5, 1): CardType.One,
}


def calculateTotalWinnings(handBids, isPart1):
    totalHands = len(handBids)
    totalWinnings = 0

    sortingKey = part1HandSortingKey if isPart1 else part2HandSortingKey
    sortedIter = sorted(handBids, key=sortingKey, reverse=True)

    for i, (hand, bid) in enumerate(sortedIter):
        rank = totalHands - i
        winning = bid * rank
        totalWinnings += winning
        # print('{0}\t{1}\t{2}\t{3}\t{4}'.    format(i, rank, hand, bid, winning))
    
    return totalWinnings
    

def part1HandSortingKey(handBid):
    return handSortingKey(handBid, isPart1=True)


def part2HandSortingKey(handBid):
    return handSortingKey(handBid, isPart1=False)


def handSortingKey(handBid, isPart1):
    hand = handBid[0]
    cardType = getCardType(hand, isPart1)
    tieBreakerRanking = getTieBreakerRanking(hand, isPart1)
    sortingKey = (cardType, tieBreakerRanking)
    # print(str(hand) + ' ' + str(sortingKey))

    return sortingKey


def getCardType(hand, isPart1):
    return getPart1CardType(hand) if isPart1 else getPart2CardType(hand)


def getPart1CardType(hand):
    cardBuckets = getCardBuckets(hand)
    bucketsCount = len(cardBuckets)
    largestBucketSize = max(cardBuckets.values())

    return bucketCountAndLargestBucketSizeToCartTypeLookup[(bucketsCount, largestBucketSize)]


def getPart2CardType(hand):
    handWithoutJokers = [c for c in hand if c != 'J']
    jokersCount = len(hand) - len(handWithoutJokers)

    if jokersCount == 5:
        return bucketCountAndLargestBucketSizeToCartTypeLookup[(1, 5)]
    
    cardBucketsWithoutJokers = getCardBuckets(handWithoutJokers)
    bucketsCountWithoutJokers = len(cardBucketsWithoutJokers)

    largestBucketSizeWithoutJokers = max(cardBucketsWithoutJokers.values())
    largestBucketSizeEnhanced = largestBucketSizeWithoutJokers + jokersCount

    return bucketCountAndLargestBucketSizeToCartTypeLookup[(bucketsCountWithoutJokers, largestBucketSizeEnhanced)]


def getCardBuckets(hand):
    cardBuckets = {}
    for c in hand:
        if c not in cardBuckets:
            cardBuckets[c] = 0
        cardBuckets[c] += 1
    return cardBuckets


def getTieBreakerRanking(hand, isPart1):
    cardRank = part1CardRank if isPart1 else part2CardRank
    return [cardRank[card] for card in hand]


filepath = r'data.txt'

handBids = []
for line in open(filepath).readlines():
    hand, bid = line.split()
    bid = int(bid)
    handBids.append((hand, bid))

# Part 1
part1TotalWinnings = calculateTotalWinnings(handBids, isPart1=True)

# Print Part 1
printProblemPartResult(1, part1TotalWinnings)

# Part 2
part2TotalWinnings = calculateTotalWinnings(handBids, isPart1=False)

# Print Part 2
printProblemPartResult(2, part2TotalWinnings)