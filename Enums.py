from enum import Enum

class Boolean(Enum):
    NA = 0
    YES = 1
    NO = 2

class Outcome(Enum):
    BUSTING = 0
    NORMAL = 1
    PUSH = 2
    BLACK_JACK = 3
    SOFT_HAND = 4

class Result(Enum):
    NA = 0
    WIN = 1
    DRAW = 2
    LOSE = 3

class Target(Enum):
    DEALER = 0
    PLAYER = 1

class Menu(Enum):
    START_GAME = 1
    INSTRUCTION = 2
    EXIT = 3

class Bet_choice(Enum):
    NA = 0
    BET_1 = 1
    BET_2 = 2
    BET_3 = 3
    BET_4 = 4

class Bet_amount(Enum):
    BET_1 = 1
    BET_2 = 2
    BET_3 = 5
    BET_4 = 10

class Message(Enum):
    DEAL_DEALER = "Deal card to dealer..."
    DEAL_PLAYER = "Deal card to player..."
    SHUFFLE_DECK = "Shuffling deck..."
    PLAYER_DECK = "Your Deck: "
    INVALID_MIN_DECK = "Your card has not reached 16. Please draw a card!"
    INSTRUCTION = "[INSTRUCTION]\nFor the rules, please read here https://vi.wikipedia.org/wiki/Blackjack\nYou can bet $1, $2, $5 or $10 for each round.\nOnce your balance <= $0, you are lost!\nGame Over!"    
    INSUFFICIENT_BALANCE = "Cannot bet higher than current balance!"
    GAME_OVER = "Well, you are out of money.\nGo home!\nToday is not your lucky day!"
    DEALER_DECK = "Dealer deck:"
    BALANCE = "Your balance:"
    BET_MONEY = "Bet:$"

class Question(Enum):
    MENU_QUESTION = "[MENU]\n1. Start Game\n2. Read Instruction\n3. Exit\nPlease select: "
    DRAW_CARD_QUESTION = "Draw a card?\n1. YES\n2. NO\nChoose: "
    PLAY_AGAIN_QUESTION = "Do you want to play another round?\n1. YES\n2. NO\nChoose: "
    BET_QUESTION = "How much would you like to make a bet?\n1. $1\n2. $2\n3. $5\n4. $10\nChoose: "