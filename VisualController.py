import Enums
import math

class VisualController:
    CARD_TYPES = ["♥","♦","♧","♤"]
    CARD_NUMBERS = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
    def __init__(self):
        pass

    @staticmethod
    def menu_display():
        menu_choice = Enums.Menu.START_GAME
        while menu_choice not in [str(Enums.Menu.START_GAME.value), str(Enums.Menu.INSTRUCTION.value), str(Enums.Menu.EXIT.value)]:
            menu_choice = input(Enums.Question.MENU_QUESTION.value)
        return int(menu_choice)

    @staticmethod
    def hit_choice_display():
        hit_choice = Enums.Boolean.NA.value
        while hit_choice not in [str(Enums.Boolean.YES.value), str(Enums.Boolean.NO.value)]:
            hit_choice = input(Enums.Question.DRAW_CARD_QUESTION.value)
        return hit_choice

    @staticmethod
    def play_again_display():
        play_again_choice = Enums.Boolean.YES.value
        while play_again_choice not in [str(Enums.Boolean.YES.value), str(Enums.Boolean.NO.value)]:
            play_again_choice = input(Enums.Question.PLAY_AGAIN_QUESTION.value)
        return play_again_choice

    @staticmethod
    def display_message(msg_key):
        print(Enums.Message[msg_key].value)

    @staticmethod
    def display_deck(deck):
        decoded_deck = []
        for card_index in deck:
            decoded_deck.append(VisualController.CARD_TYPES[math.floor(card_index/13)] + VisualController.CARD_NUMBERS[card_index%13-1])
        print(decoded_deck)

    @staticmethod
    def bet_choose(balance):        
        bet_money_amount = 0
        bet_money_choice = str(Enums.Bet_choice.NA.value)
        while bet_money_amount > balance or bet_money_amount == 0:
            while bet_money_choice not in [str(Enums.Bet_choice.BET_1.value), str(Enums.Bet_choice.BET_2.value), str(Enums.Bet_choice.BET_3.value), str(Enums.Bet_choice.BET_4.value)]:
                bet_money_choice = input(Enums.Question.BET_QUESTION.value)
            bet_money_amount = Enums.Bet_amount[Enums.Bet_choice(int(bet_money_choice)).name].value
            if bet_money_amount > balance:
                VisualController.display_message(Enums.Message.INSUFFICIENT_BALANCE.name)
        return bet_money_amount