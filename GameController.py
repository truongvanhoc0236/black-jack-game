import random
from DeckController import Player
from DeckController import Dealer
from DeckController import DeckController
from VisualController import VisualController
import Enums

class GameController:
    def __init__(self):
        self._player = Player()
        self._dealer = Dealer()

    def reset_deck(self):
        DeckController.shuffle_deck()
        self._player.reset_deck()
        self._dealer.reset_deck()

    def dealing_intro(self):
        for i in range (2):
            VisualController.display_message(Enums.Message.DEAL_PLAYER.name)
            self._player.deal_card(Enums.Boolean.YES)
            VisualController.display_deck(self._player.deck)
            VisualController.display_message(Enums.Message.DEAL_DEALER.name)
            self._dealer.deal_card(Enums.Boolean.YES)

    def start_menu(self):
        menu_choice = VisualController.menu_display()
        while menu_choice != Enums.Menu.EXIT.value:
            if menu_choice == Enums.Menu.START_GAME.value:
                self.play_game()
            else:
                self.show_instruction()
            menu_choice = VisualController.menu_display()

    def player_draw(self):
        VisualController.display_message(Enums.Message.PLAYER_DECK.name)
        VisualController.display_deck(self._player.deck)
        hit_choice = str(Enums.Boolean.YES.value)
        while self._player.calculate_deck_sum() < 15 or (hit_choice == str(Enums.Boolean.YES.value) and self._player.calculate_deck_sum() < 21 and len(self._player._deck) < 5) :
            hit_choice = VisualController.hit_choice_display()
            if hit_choice == str(Enums.Boolean.YES.value):
                VisualController.display_message(Enums.Message.DEAL_PLAYER.name)
                self._player.deal_card(Enums.Boolean.NO)
                VisualController.display_deck(self._player.deck)
            elif self._player.calculate_deck_sum() < 15:
                VisualController.display_message(Enums.Message.INVALID_MIN_DECK.name)

    def dealer_draw(self):
        while self._dealer.make_hit_decision(len(self._player.deck)) == Enums.Boolean.YES:
            VisualController.display_message(Enums.Message.DEAL_DEALER.name)
            self._dealer.deal_card(Enums.Boolean.NO)
            VisualController.display_deck(self._dealer.deck)

    def show_result(self, result):
        print(result.name)
        VisualController.display_message(Enums.Message.PLAYER_DECK.name)
        VisualController.display_deck(self._player.deck)
        VisualController.display_message(Enums.Message.DEALER_DECK.name)
        VisualController.display_deck(self._dealer.deck)

    def play_game(self):
        VisualController.display_message(Enums.Message.SHUFFLE_DECK.name)
        DeckController.shuffle_deck()
        another_round = str(Enums.Boolean.YES.value)
        while another_round == str(Enums.Boolean.YES.value) and self._player.balance > 0:
            self.show_balance()
            self.place_bet()
            self.dealing_intro()
            result = self._dealer.compare_decks(self._player, Enums.Boolean.YES)
            if result != Enums.Result.NA:
                self.show_result(result)
            else:
                self.player_draw()
                self.dealer_draw()
                result = self._dealer.compare_decks(self._player, Enums.Boolean.NO)
                self.show_result(result)
            self._player.update_money(result)
            self.reset_deck()
            self.show_balance()
            if self._player.balance > 0:
                another_round = VisualController.play_again_display()
            else:
                VisualController.display_message(Enums.Message.GAME_OVER.name)

    def show_instruction(self):
        VisualController.display_message(Enums.Message.INSTRUCTION.name)

    def place_bet(self):
        bet_money = VisualController.bet_choose(self._player.balance)
        print(Enums.Message.BET_MONEY.value + str(bet_money))
        self._player.bet_amount = int(bet_money)

    def show_balance(self):
        VisualController.display_message(Enums.Message.BALANCE.name)
        print(self._player.balance)


game = GameController()
game.start_menu()