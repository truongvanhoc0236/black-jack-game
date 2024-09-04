import math
import Enums
import random

class DeckController:
    master_deck = []   
    def __init__(self):
        pass

    # Create or Shuffle deck
    def shuffle_deck():
        DeckController.master_deck = list(range(1, 53)) 
        random.shuffle(DeckController.master_deck)

class Hand(DeckController):
    def __init__(self):
        self._deck = []

    def reset_deck(self):
        self._deck = []
    
    # Deal card action
    # [Boolean] take_from_top: take card from top/bottom
    def deal_card(self, take_from_top):
        card = 0
        if take_from_top == Enums.Boolean.YES:
            self._deck.append(DeckController.master_deck.pop(1))
        else:
            self._deck.append(DeckController.master_deck.pop())

    # Calculate total value of deck
    # [List] deck to calculate value
    def calculate_deck_sum(self):
        number_of_aces = 0
        deck_sum = 0
        card_value = 0
        for card in self._deck:
            card_value = self.calculate_card_value(card)
            if card_value == 1: #Ace
                number_of_aces += 1
            else:
                deck_sum += card_value
        deck_sum += self.calculate_aces_value(deck_sum, number_of_aces)
        return deck_sum

    # Calculate value of card
    def calculate_card_value(self, card):
        if 0 < card % 13 < 10:
            return card % 13
        else:
            return 10

    # Calculate value of aces
    # [Int] deck_sum: sum of deck without aces
    # [Int] number_of_aces: Number of aces in deck
    def calculate_aces_value(self, deck_sum, number_of_aces):
        ace_sum = 0
        while number_of_aces > 0 and deck_sum < 22 - number_of_aces:
            if deck_sum + ace_sum + 11 + (number_of_aces - 1) < 22:
                ace_sum += 11
            elif deck_sum + ace_sum + 10 + (number_of_aces - 1) < 22:
                ace_sum += 10
            else:
                ace_sum += 1
            number_of_aces -= 1
        return ace_sum + number_of_aces

    # Check if the deck is Soft Hand, Black Jack, Pushing, Busting or normal
    # [List] deck: Deck to be check outcome
    def check_deck_outcome(self):
        outcome = Enums.Outcome.NORMAL
        size_deck = len(self._deck)
        if size_deck == 2:
            if self._deck[0] % 13 == 1 and self._deck[1] % 13 == 1:
                outcome = Enums.Outcome.SOFT_HAND
            elif (self._deck[0] % 13 == 1 and self._deck[1] % 13 not in range(1, 10)) or (self._deck[1] % 13 == 1 and self._deck[0] % 13 not in range(1, 10)):
                outcome = Enums.Outcome.BLACK_JACK
        else:
            sum_card = self.calculate_deck_sum()
            if sum_card < 22 and size_deck == 5:
                outcome = Enums.Outcome.PUSH
            elif sum_card > 21:
                outcome = Enums.Outcome.BUSTING
        return outcome.value

class Player(Hand):
    def __init__(self):
        self._deck = []   
        self._balance = 500 
        self._bet_amount = 0

    @property
    def deck(self):
        return self._deck
        
    @property
    def balance(self):
        return self._balance

    @property
    def bet_amount(self):
        return self._bet_amount

    @bet_amount.setter
    def bet_amount(self, amount):
        self._bet_amount = amount

    def reset_balance(self):
        self._balance = 500

    def update_money(self, result):
        if result == Enums.Result.WIN:
            self._balance += self._bet_amount
        elif result == Enums.Result.LOSE:
            self._balance -= self._bet_amount
        self._bet_amount = 0

class Dealer(Hand):
    DECISION_POINT = 35
    def __init__(self):
        self._deck = []

    @property
    def deck(self):
        return self._deck

    # Calculate the possibility for dealer to take another card
    # [player_deck]: Deck of player
    def calculate_possibility_to_take_card(self, player_deck_size):
        possibility = 100
        possibility_of_player_busting = 0
        dealer_deck_sum = self.calculate_deck_sum()
        if 22 > dealer_deck_sum >= 15:
            possibility = (21 - dealer_deck_sum) / 13 * 100
            possibility_of_player_busting = (player_deck_size - 2) / 3 * 100
            possibility += (possibility_of_player_busting * 0.1)
        elif dealer_deck_sum > 21:
            possibility = 0
        return possibility

    # Make hit or stand decision
    # [dealer_deck]: Deck of dealer
    # [player_deck]: Deck of player
    def make_hit_decision(self, player_deck_size):
        possibility = self.calculate_possibility_to_take_card(player_deck_size)
        if possibility >= Dealer.DECISION_POINT:
            return Enums.Boolean.YES
        else:
            return Enums.Boolean.NO

    # Compare decks of player and dealer
    # [dealer_deck]: Deck of dealer
    # [player_deck]: Deck of player
    # [init]: At the beginning?
    def compare_decks(self, player_deck, init):
        result = ""
        player_sum = player_deck.calculate_deck_sum()
        dealer_sum = self.calculate_deck_sum()
        player_outcome = player_deck.check_deck_outcome()
        dealer_outcome = self.check_deck_outcome()
        if player_outcome == dealer_outcome and player_outcome == Enums.Outcome.PUSH.value: #Both PUSH
            if player_sum > dealer_sum:
                result = Enums.Result.LOSE
            elif player_sum < dealer_sum:
                result = Enums.Result.WIN
            else:
                result = Enums.Result.DRAW
        elif player_outcome > dealer_outcome:
            result = Enums.Result.WIN
        elif player_outcome < dealer_outcome:
            result = Enums.Result.LOSE
        elif  player_outcome == dealer_outcome and player_outcome == Enums.Outcome.BUSTING.value: #Both BUSTING
            result = Enums.Result.DRAW
        else:
            if init == Enums.Boolean.YES:
                result = Enums.Result.NA
            else:
                if player_sum > dealer_sum:
                    result = Enums.Result.WIN
                elif player_sum < dealer_sum:
                    result = Enums.Result.LOSE
                else:
                    result = Enums.Result.DRAW
        return result