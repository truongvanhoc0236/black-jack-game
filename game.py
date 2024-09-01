import random
import math
from enum import Enum

CARD_TYPES = ["♥","♦","♧","♤"]
CARD_NUMBERS = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
OUTCOMES = ["BUSTING", "NORMAL", "PUSH", "BLACK JACK", "SOFT HAND"]
RESULT = ["WIN", "DRAW", "LOSE"]
class Outcome(Enum):
    BUSTING = 0
    NORMAL = 1
    PUSH = 2
    BLACK_JACK = 3
    SOFT_HAND = 4
class Result(Enum):
    WIN = 0
    DRAW = 1
    LOSE = 2
class Hit(Enum):
    HIT = 1
    STAND = 2
class Player_type(Enum):
    PLAYER = 1
    DEALER = 2
    

def print_deck(deck):
    decoded_deck = []
    for card_index in deck:
        #print("Card index: " + str(card_index))
        decoded_deck.append(CARD_TYPES[math.floor(card_index/13)] + CARD_NUMBERS[card_index%13-1])
    print(decoded_deck)

def deal_car(cards, deck, player_type):
    card_index = random.randrange(1,52)
    while (cards[card_index-1] != 0):
        card_index = random.randrange(1,52)
    cards[card_index-1] = player_type #Remove card from deck
    deck.append(card_index)

def check_outcome(deck):
    size_deck = len(deck)
    outcome = Outcome.NORMAL.value
    if size_deck == 2:
        if deck[0] % 13 - 1 == 0 and deck[1] % 13 - 1 == 0:
            outcome = Outcome.SOFT_HAND.value
        elif (deck[0] % 13 - 1 == 0 and deck[1] % 13 > 9) or (deck[1] % 13 - 1 == 0 and deck[0] % 13 > 9):
            outcome = Outcome.BLACK_JACK.value
    else:
        sum_card = 0
        for card_index in deck:
            if 0 < card_index % 13 < 10:
                sum_card += card_index % 13
            else:
                sum_card += 10
        if sum_card < 22 and size_deck == 5:
            outcome = Outcome.PUSH.value
        elif sum_card > 21:
            outcome = Outcome.BUSTING.value
    return outcome

def show_result(result, player_deck, dealer_deck):
    print(result)
    print("Player deck:")
    print_deck(player_deck)
    print("Dealer deck:")
    print_deck(dealer_deck)
#2 A A A #4 4 A A A #A
def calculate_possibility(dealer_deck, player_deck):
    possibility = 100
    possibility_of_player_busting = 0
    sum_card = calculate_sum_card(dealer_deck)
    if sum_card >= 15:
        possibility = (21 - sum_card) / 13 * 100
        possibility_of_player_busting = (len(player_deck) - 2) / 3 * 100
        possibility += (possibility_of_player_busting * 0.1)
    return possibility

def calculate_sum_card(deck):
    aces = []
    sum_card = 0
    for card_index in deck:
        if 1 < card_index % 13 < 10:
            sum_card += card_index % 13
        elif card_index % 13 > 9:
            sum_card += 10
        elif card_index % 13 == 0:
            sum_card += 10
        else:
            aces.append(1)
    number_of_aces = len(aces)
    for ace_index in range(number_of_aces):
        number_of_aces -=1
        if sum_card + 11 + number_of_aces < 22:
            sum_card += 11
        elif sum_card + 10 + number_of_aces < 22:
            sum_card += 10
        else:
            sum_card += 1
    return sum_card

def make_decision(possibility):
    print("Possibility:" + str(possibility))
    if possibility > 35:
        return str(Hit.HIT.value)
    else:
        return str(Hit.STAND.value)

def compare_deck(player_deck, player_outcome, dealer_deck, dealer_outcome):
    result = ""
    player_sum = calculate_sum_card(player_deck)
    dealer_sum = calculate_sum_card(dealer_deck)
    if player_outcome == dealer_outcome and player_outcome == Outcome.PUSH.value: #Both PUSH
        if player_sum > dealer_sum:
            result = RESULT[Result.LOSE.value]
        elif player_sum < dealer_sum:
            result = RESULT[Result.WIN.value]
        else:
            result = RESULT[Result.DRAW.value]
    elif player_outcome > dealer_outcome:
        result = RESULT[Result.WIN.value]
    elif player_outcome < dealer_outcome:
        result = RESULT[Result.LOSE.value]
    elif  player_outcome == dealer_outcome and player_outcome == Outcome.BUSTING.value: #Both BUSTING
        result = RESULT[Result.DRAW.value]
    else:
        if player_sum > dealer_sum:
            result = RESULT[Result.WIN.value]
        elif player_sum < dealer_sum:
            result = RESULT[Result.LOSE.value]
        else:
            result = RESULT[Result.DRAW.value]
    return result

print("BLACK JACK")
choice = '1'
while choice != '3':
    choice = input("1. Start Game\n2. Read Instruction\n3. Exit\nPlease select: ")
    if choice == '1':
        cards = [0] * 52
        another_round = '1'
        while another_round =='1':
            print("Shuffling cards...")
            player_deck = []
            dealer_deck = []
            print("Dealing cards...")
            deal_car(cards, player_deck, Player_type.PLAYER) #Add card to player deck
            deal_car(cards, dealer_deck, Player_type.DEALER) #Add card to dealer deck
            deal_car(cards, player_deck, Player_type.PLAYER) #Add card to player deck
            deal_car(cards, dealer_deck, Player_type.DEALER) #Add card to dealer deck
            print("Player deck:")
            print_deck(player_deck)
            player_outcome = check_outcome(player_deck) #Check player deck
            dealer_outcome = check_outcome(dealer_deck) #Check dealer deck
            if player_outcome == dealer_outcome and player_outcome !=Outcome.NORMAL.value:
                show_result(RESULT[Result.DRAW.value], player_deck, dealer_deck)
            elif player_outcome > dealer_outcome:
                show_result(RESULT[Result.WIN.value], player_deck, dealer_deck)
            elif player_outcome < dealer_outcome:
                show_result(RESULT[Result.LOSE.value], player_deck, dealer_deck)
            else:
                #Player takes cards
                hit = str(Hit.HIT.value)
                while hit != str(Hit.STAND.value):
                    hit = input("1. Hit\n2. Stand\nChoose: ")
                    if hit == str(Hit.HIT.value): #Take another card
                        deal_car(cards, player_deck, Player_type.PLAYER)
                        print_deck(player_deck)
                        player_outcome = check_outcome(player_deck) #Check player deck
                        if player_outcome in [Outcome.PUSH.value, Outcome.BUSTING.value]:
                            hit = str(Hit.STAND.value) #Stop taking card
                #Dealer takes cards
                hit = str(Hit.HIT.value)
                while hit != str(Hit.STAND.value):
                    possibility = calculate_possibility(dealer_deck, player_deck)
                    hit = make_decision(possibility)
                    if hit == str(Hit.HIT.value): #Take another card
                        deal_car(cards, dealer_deck, Player_type.DEALER)
                        print_deck(dealer_deck)
                        dealer_outcome = check_outcome(dealer_deck) #Check dealer deck
                        if dealer_outcome in [Outcome.PUSH.value, Outcome.BUSTING.value]:
                            hit = str(Hit.STAND.value) #Stop taking card
                #Show result
                compare_result = compare_deck(player_deck, player_outcome, dealer_deck, dealer_outcome)
                show_result(compare_result, player_deck, dealer_deck)
            another_round = input ("Another round?\n1. Yes\n2. No\nChoose: ")
            while another_round not in ['1', '2']:
                another_round = input ("Another round?\n1. Yes\n2. No\nChoose: ")
        

