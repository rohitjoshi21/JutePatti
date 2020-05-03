import card
from termcolor import colored
from time import sleep
import os


message1 = '''\
		What do you want to do?
		1. Pick up from floor
		2. Draw from deck
		'''

message2 = '''\
		Which card do you want to drop?
		Enter the card number counting from left
		'''


class JutePatti:
    def __init__(self, no_of_players, no_of_cards):
        self.no_of_players = no_of_players
        self.no_of_cards = no_of_cards
        self.turn = 0

    def gamePlay(self):
        self.deck = card.Deck()
        self.deck.shuffle()
        self.hands = self.deck.distribute(self.no_of_players, self.no_of_cards)
        for hand in self.hands:
            hand.checkForJokers()

        self.name = input('Enter your name ? ')
        self.hands[0].playerName = self.name
        while True:
            player = self.hands[self.turn]

            if self.turn != 0:
                # For Computer Player
                player.draw_card()

                if player.check_for_win():
                    self.gameOver(player)
                    break

                player.choose_and_drop_card()
                self.displayInfo()
            else:
                # For Human Player

                print(self.name)
                print('Your cards:')
                self.displayHand(player)

                print('On Floor:')
                floorCard = self.deck.get_top_card_on_floor()
                print(decorate(floorCard))

                print('Joker:', colored(card.rankName[self.deck.joker], 'red'))

                print(message1)
                inp = input('>>> ')
                if inp == '1':
                    player.pick_from_floor()
                else:
                    player.draw_from_deck()

                if player.check_for_win():
                    self.gameOver(player)
                    break

                self.displayHand(player)

                print(message2)

                index = self.getIndex()
                player.drop(player.cards[index - 1])

            self.nextTurn()

    def getIndex(self):
        while True:
            ind = int(input('>>> '))
            if ind <= self.no_of_cards + 1:
                return ind
            print('>>> Invalid Index. Enter again.')

    def displayHand(self, player):
        print(len(player.singles), len(player.jokers))
        cards = player.getCardList()
        a = decorate(cards)
        print(a)

    def displayInfo(self):
        pass

    def gameOver(self, winner):

        print('%s won the game' % winner.playerName)
        self.displayHand(winner)

    def nextTurn(self):
        # print("called")
        if self.turn < (self.no_of_players - 1):
            self.turn += 1
        else:
            self.turn = 0


def decorate(cardList):
    newList = []
    suitColor = {'\u2666': 'red', '\u2665': 'red',
                 '\u2663': 'blue', '\u2660': 'blue'}

    for card in cardList:
        if card[0] == None:
            return ''
        card = [str(x) for x in card]
        a = ''.join(card) + ' ' * (3 - len(card[0]))

        # Coloring Cards according to the suit
        #  Spade,Club    --> Black
        #  Diamond,Heart --> Red
        newList.append(colored(a, suitColor[card[1]], on_color='on_white'))

    line = '  '.join(newList) + '  '
    return line


def main():
    game = JutePatti(4, 7)
    game.gamePlay()


if __name__ == "__main__":
    main()
