import card
from termcolor import colored
from time import sleep


def findWinner(hands):
    maxScore = ['A', 0, 0, 0]
    winner = None
    for hand in hands:
        hand.getValue()
        a = hand.value

        if a > maxScore:
            maxScore = a
            winner = hand.playerName
        elif a == maxScore:
            winner += 'and' + hand.playerName

    return winner


def decorate(cardList):
    newList = []
    suitColor = {'\u2666': 'red', '\u2665': 'red',
                 '\u2663': 'blue', '\u2660': 'blue'}

    for card in cardList:
        card = [str(x) for x in card]
        a = ''.join(card) + ' ' * (3 - len(card[0]))

        # Coloring Cards according to the suit
        #  Spade,Club    --> Black
        #  Diamond,Heart --> Red
        newList.append(colored(a, suitColor[card[1]], on_color='on_white'))

    line = '  '.join(newList) + '  '
    return line


def showWinner(name):
    print()
    print('The winner is .  ', end='\r')
    sleep(1)
    print('The winner is .. ', end='\r')
    sleep(1)
    print('The winner is ...', end='\r')
    sleep(1)

    print(f'The winner is {name}')


def main():

    myDeck = card.Deck()
    myDeck.shuffle()

    playerNo = int(input('Enter no of player? '))
    hands = myDeck.distribute(playerNo, 3)

    for hand in hands:
        print(colored(f'\n{hand.playerName}', 'cyan'))
        line = decorate(hand.getCardList())
        print(f'{line} \n')

    winner = findWinner(hands)

    showWinner(winner)


if __name__ == "__main__":
    main()
