import random

suitName = ['\u2666', '\u2665', '\u2663', '\u2660']
rankName = {2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8,
            9: 9, 10: 10, 11: 'J', 12: 'Q', 13: 'K', 14: 'A'}

ranNames = ['Rohit', 'Mahesh', 'Sushil', 'Lochan']


class Deck:

    def __init__(self, no_of_deck=1):
        self.no_of_deck = no_of_deck
        self.cards = []
        for i in range(no_of_deck):
            for suit in suitName:
                for num in range(2, 15):
                    new = Card(num, suit)
                    self.cards.append(new)

    def shuffle(self):
        random.shuffle(self.cards)

    def getCard(self):
        return self.cards.pop()

    def distribute(self, playersNum, count=None):

        num = (self.no_of_deck * 52) / playersNum
        if (count == None and num % 1 == 0) or num >= count:

            count = int(num) if count == None else count

            players = [Hand(count) for i in range(playersNum)]

            round = 1
            while round <= count:
                for player in players:
                    player.add(self.getCard())

                round += 1
            return players

        else:
            return ValueError


class Hand:
    def __init__(self, size, playerName=None):
        self.size = size
        self.cards = []
        self.levels = [self.highCard, self.pair,
                       self.straight, self.fullStraight, self.trial]
        if playerName == None:
            random.shuffle(ranNames)
            try:
                self.playerName = ranNames.pop()
            except IndexError:
                raise ValueError('Not Enough PLayer Names Available')

        else:
            self.playerName = name

    def sort(self):
        self.cards.sort(key=lambda x: x.rank)

    def add(self, card):
        self.cards.append(card)

    def drop(self, card):
        if card in self.cards:
            self.cards.remove(card)

    def arrange(self, key):
        return NotImplementedError

    def getCardList(self):
        self.sort()
        self.lists = []
        for card in self.cards:
            rank = rankName[card.rank]
            suit = card.suit
            self.lists.append([rank, suit])
        return self.lists

    def getValue(self):
        self.sort()
        self.ranks = set([x.rank for x in self.cards])
        self.suits = set([x.suit for x in self.cards])
        for level in self.levels[::-1]:
            bool, val = level()

            if bool:
                self.value = val
                break

    def trial(self):
        point = ['F', 0, 0, 0]
        if len(self.ranks) == 1:
            point[1] = self.ranks.pop()
            return True, point
        return False, point

    def fullStraight(self):
        point = ['E', 0, 0, 0]
        if len(self.suits) == 1:
            res, val = self.straight()
            point[1] = max(self.ranks)
            if res == False:
                point[0] = 'C'
            return True, point
        return False, []

    def straight(self):
        point = ['D', 0, 0, 0]

        nums = [x.rank for x in self.cards]

        if nums[2] - nums[1] == nums[1] - nums[0] == 1 or nums == [2, 3, 14]:

            point[1] = nums[-1]
            return True, point
        return False, point

    def pair(self):
        point = ['B', 0, 0, 0]
        if len(self.ranks) == 2:
            nums = [x.rank for x in self.cards]
            for num in nums:
                if nums.count(num) == 2:
                    point[1] = num
                else:
                    point[2] = num
            return True, point
        return False, point

    def highCard(self):
        nums = [x.rank for x in self.cards]
        point = ['A', nums[2], nums[1], nums[0]]
        return True, point

    def __iter__(self):
        for card in self.cards:
            yield card

    def __comp__(self, other):
        raise NotImplementedError


class Card:
    def __init__(self, rank, suit):
        self.suit = suit
        self.rank = rank


if __name__ == "__main__":
    myDeck = Deck()
    myDeck.shuffle()

    hands = myDeck.distribute(3, 3)

    for hand in hands:
        b = list(map(lambda x: (x.rank, x.suit), hand))
        print(b)
        print()
