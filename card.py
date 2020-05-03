import random
from collections import Counter
suitName = ['\u2666', '\u2665', '\u2663', '\u2660']
rankName = {2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8,
            9: 9, 10: 10, 11: 'J', 12: 'Q', 13: 'K', 14: 'A'}

ranNames = ['Mahesh', 'Sushil', 'Lochan', 'Soniya']


class Deck:

    def __init__(self, no_of_deck=1):
        self.no_of_deck = no_of_deck
        self.cards = []
        self.cards_on_floor = []
        self.top_card_on_floor = None
        self.joker = None

        for i in range(no_of_deck):
            for suit in suitName:
                for num in range(2, 15):
                    new = Card(num, suit)
                    self.cards.append(new)

    def drop_on_floor(self, card):
        self.cards_on_floor.append(card)
        self.top_card_on_floor = card

    def get_top_card_on_floor(self):
        card = self.top_card_on_floor
        if card != None:
            rank = rankName[card.rank]
            suit = card.suit
        else:
            rank = None
            suit = None
        return [(rank, suit)]

    def pick_from_floor(self):
        return self.cards_on_floor.pop()

    def shuffle(self):
        random.shuffle(self.cards)

    def getCard(self):
        if self.cards == []:
            self.cards = self.cards_on_floor
            self.shuffle()

        return self.cards.pop()

    def makeJoker(self):
        self.openedCard = self.getCard()

        if self.openedCard.rank <= 13:
            self.joker = self.openedCard.rank + 1
        else:
            self.joker = 2

    def distribute(self, playersNum, count=None):

        num = (self.no_of_deck * 52) / playersNum
        if (count == None and num % 1 == 0) or num >= count:

            count = int(num) if count == None else count

            players = [Hand(count, self) for i in range(playersNum)]

            round = 1
            while round <= count:
                for player in players:
                    player.add(self.getCard())

                round += 1
            self.makeJoker()
            return players

        else:
            return ValueError


class Hand:
    def __init__(self, size, deck, playerName=None):
        self.size = size
        self.cards = []
        self.pairs = []
        self.singles = []
        self.jokers = []
        self.deck = deck

        if playerName == None:
            random.shuffle(ranNames)
            try:
                self.playerName = ranNames.pop()
            except IndexError:
                raise ValueError('Not Enough PLayer Names Available')

        else:
            self.playerName = name

    def checkForJokers(self):
        card = self.search_by_rank(self.singles, self.deck.joker)
        self.singles = self.remove_by_rank(self.singles, self.deck.joker)
        if len(card) > 0:
            self.jokers.append(card[0])

        cards = self.search_by_rank(self.pairs, self.deck.joker)
        self.pairs = self.remove_by_rank(self.pairs, self.deck.joker)

        for card in cards:
            self.jokers.append(card)

    def update(self, card):

        if card.rank == self.deck.joker:

            self.jokers.append(card)
            return

        self.singlesRank = [x.rank for x in self.singles]

        if card.rank in self.singlesRank:

            nextCard = self.search_by_rank(self.singles, card.rank)[0]
            self.singles.remove(nextCard)

            self.pairs.append(card)
            self.pairs.append(nextCard)

        else:
            self.singles.append(card)

    def choose_and_drop_card(self):
        for card in self.singles:
            if card in self.deck.cards_on_floor or card in self.pairs:
                self.deck.drop_on_floor(card)
                self.singles.remove(card)
                self.cards.remove(card)
                return card

        card = self.singles.pop()
        self.cards.remove(card)
        self.deck.drop_on_floor(card)
        return card

    def draw_card(self):
        lastCard = self.deck.top_card_on_floor
        if lastCard in self.singles:
            self.add(self.deck.pick_from_floor())
        else:
            self.add(self.deck.getCard())

    def pick_from_floor(self):
        card = self.deck.pick_from_floor()
        self.add(card)

    def draw_from_deck(self):
        card = self.deck.getCard()
        self.add(card)

    def check_for_win(self):
        # print(len(self.singles), len(self.jokers))
        return len(self.singles) <= len(self.jokers)

    def remove_by_rank(self, array, rank):
        array = [x for x in array if x.rank != rank]
        return array

    def search_by_rank(self, array, rank):
        cards = []
        for i in array:
            if i.rank == rank:
                cards.append(i)
        return cards

    def sort(self):
        self.cards.sort(key=lambda x: x.rank)

    def add(self, card):
        self.cards.append(card)
        self.update(card)

    def drop(self, card):
        # if card in self.cards:
        self.deck.drop_on_floor(card)
        self.cards.remove(card)

        if card in self.singles:
            self.singles.remove(card)
        else:
            self.pairs.remove(card)
            card2 = self.search_by_rank(self.pairs, card.rank)[0]
            self.pairs.remove(card2)

            singlesRank = [x.rank for x in self.singles]
            if card.rank in singlesRank:
                self.update(card2)
            else:
                self.singles.append(card2)

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
