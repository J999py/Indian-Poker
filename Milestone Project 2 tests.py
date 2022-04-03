import random

suits = ('Hearts ♥', 'Diamonds ♦', 'Spades ♠', 'Clubs ♣')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
          'Nine': 9, 'Ten': 10, 'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14}


class Chips:

    def __init__(self, name, opposite_name):
        self.opposite_name = opposite_name
        self.total = 100
        self.name = name

    def bet(self, amount):
        self.total -= amount
        print(f'{self.name} has spent {amount} chips. They have {self.total} chips now')

    def bet_start_game(self):
        if self.total <= 2:
            print(f'Insufficient credits. {self.name} you are out of funds!')
            print(f'{self.opposite_name} has won the game!!! {self.name} had insufficient credits. ')
            exit()
        else:
            self.total -= 2
            print(f'{self.name} has spent 2 chips. They have {self.total} chips now')

    def bet_extra_cards(self):
        if self.total < 3:
            print(f'Insufficient credits, {self.name}. You can not buy extra cards.')
            return True

        self.total -= 3
        print(f'{self.name} has spent 3 chips. They have {self.total} chips now')

    def receive(self, amount):
        self.total += amount
        print(f'{self.name} has won {amount} chips! They have {self.total} chips now')

    def credit(self):
        return self.total

    def __str__(self):
        return self.name


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:
    def __init__(self):
        # Note this only happens once upon creation of a new Deck
        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                # This assumes the Card class has already been defined!
                self.all_cards.append([suit, rank])

    def shuffle(self):
        # Note this doesn't return anything
        random.shuffle(self.all_cards)

    def deal_start_cards(self, name, player_hand):
        # Note we remove one card from the list of all_cards

        player_hand.append(self.all_cards[-1])
        print(f'{name} your top card is {Card(self.all_cards[-1][0], self.all_cards[-1][1])}')
        self.all_cards.pop()

        player_hand.append(self.all_cards[-1])
        self.all_cards.pop()
        player_hand.append(self.all_cards[-1])
        self.all_cards.pop()

        return player_hand

    def deal_extra_cards(self, player_hand, name):
        player_hand.append(self.all_cards[-1])
        self.all_cards.pop()
        player_hand.append(self.all_cards[-1])
        self.all_cards.pop()
        print(
            f'{name}, the extra cards you have received are {Card(player_hand[3][0], player_hand[3][1])} and a '
            f'{Card(player_hand[4][0], player_hand[4][1])}')
        return player_hand

    def clear_hands(self, player_hand):
        for cards in reversed(player_hand):
            self.all_cards.append(cards)
        player_hand.clear()

    def remove_extra_cards(self, player_hand, extra_cards):
        player_hand.remove(extra_cards[0])
        self.all_cards.append(extra_cards[0])
        player_hand.remove(extra_cards[1])
        self.all_cards.append(extra_cards[1])
        return player_hand

    def list(self):
        return self.all_cards


class Board:
    board_chips = 0

    def receive(self, amount):
        self.board_chips += amount

    def return_win(self, amount):
        self.board_chips -= amount

    def game_win(self):
        return self.board_chips

    def clear_board(self):
        self.board_chips = 0

    def __str__(self):
        return f'There are {self.board_chips} chips on the board now.'


class Player(Chips):

    def __init__(self, name, opposite_name):
        Chips.__init__(self, name, opposite_name)
        self.name = name
        # A new player has no cards
        self.player_hand = []

    def player_stat(self):
        return f'Player {self.name} has {len(self.player_hand)} cards.'

    def update_cards(self, cards):
        self.player_hand = cards

    def hand_value(self):
        player_hand_value = 0
        royalty_list = [11, 12, 13]
        ranks_list = [values[self.player_hand[0][1]], values[self.player_hand[1][1]], values[self.player_hand[2][1]]]
        card1 = ranks_list[0] in royalty_list
        card2 = ranks_list[1] in royalty_list
        card3 = ranks_list[2] in royalty_list

        # Ace check
        if self.player_hand[0][1] == self.player_hand[1][1] == self.player_hand[2][1]:
            player_hand_value += 500 + 3 * values[self.player_hand[0][1]]
            return player_hand_value

        # Royalty check
        elif card1 and card2 and card3:
            player_hand_value += 400
            for count in range(3):
                player_hand_value += values[self.player_hand[count][1]]

        # Sequence Check
        elif sorted(ranks_list)[0] + 1 == sorted(ranks_list)[1] and sorted(ranks_list)[0] + 2 == sorted(ranks_list)[2]:
            player_hand_value += 300 + sorted(ranks_list)[2]

        # Color check
        elif self.player_hand[0][0] == self.player_hand[1][0] == self.player_hand[2][0]:
            player_hand_value += 200
            for count in range(3):
                player_hand_value += values[self.player_hand[count][1]]

            return player_hand_value

        # Sum check
        else:
            player_hand_value += 100
            for count in range(3):
                if 'Ace' in self.player_hand[count]:
                    player_hand_value += 1
                else:
                    player_hand_value += values[self.player_hand[count][1]]

        return player_hand_value

    def show_cards(self):
        if len(self.player_hand) == 3:
            print(f'{self.name} has the cards: {Card(self.player_hand[0][0], self.player_hand[0][1])}, '
                  f'{Card(self.player_hand[1][0], self.player_hand[1][1])}, '
                  f'{Card(self.player_hand[2][0], self.player_hand[2][1])}')
        else:
            print(f'{self.name} has the cards: {Card(self.player_hand[0][0], self.player_hand[0][1])}, '
                  f'{Card(self.player_hand[1][0], self.player_hand[1][1])}, '
                  f'{Card(self.player_hand[2][0], self.player_hand[2][1])}, '
                  f'{Card(self.player_hand[3][0], self.player_hand[3][1])}, '
                  f'{Card(self.player_hand[4][0], self.player_hand[4][1])}')


def decide_winner(game_player1, game_player2, chips_board):
    if game_player1.hand_value() < game_player2.hand_value():
        print(f'{game_player2.name} has won!!!')
        game_player2.receive(chips_board.game_win())
        chips_board.clear_board()
    elif game_player2.hand_value() < game_player1.hand_value():
        print(f'{game_player1.name} has won!!!')
        game_player1.receive(chips_board.game_win())
        chips_board.clear_board()
    else:
        print("It's a tie!!!")
        game_player1.receive(chips_board.game_win() / 2)
        game_player2.receive(chips_board.game_win() / 2)
        chips_board.clear_board()


def game_input(name, already_bet, current_player, other_player, chips_board, card_board):
    move = 'not bet'
    while move.lower() not in ['bet', 'show', 'close']:
        move = input(f"{name} what would you like to do? You can bet, show or close: ")
        if move.lower() == 'bet':
            amount = 0
            while amount < already_bet:
                is_int = False
                while not is_int:
                    try:
                        amount = int(input("How much would you like to bet?"))
                    except ValueError:
                        print("\nPlease make sure to enter an integer\n")
                    else:
                        is_int = True

                if amount < already_bet:
                    print("You can not bet less than the previous player or bet chips lower than 1")
            # Input validation that checks if amount < what is already bet above

            # This allows user to not bet unreasonable amount.
            if already_bet < current_player.credit() < amount:
                print("You have insufficient funds. Please make sure to bet a reasonable amount.")
                print(f"You have {current_player.credit()} chips. Try again\n")
                continue

            # If player can not bet anymore
            if current_player.credit() < already_bet:
                print(f"{name} you can not bet anymore chips. Your cards will be shown automatically. "
                      f"If you win this round the game will continue")
                current_player.bet(amount)
                chips_board.receive(amount)
                print(chips_board)
                current_player.show_cards()
                other_player.show_cards()
                decide_winner(current_player, other_player, chips_board)
                return False

            chips_board.receive(amount)
            print(chips_board)
            return amount

        elif move.lower() == 'show':
            print(f'{already_bet} will be deducted from your account.')
            current_player.bet(already_bet)
            chips_board.receive(already_bet)
            print(chips_board)
            current_player.show_cards()
            other_player.show_cards()
            decide_winner(current_player, other_player, chips_board)
            return False

        elif move.lower() == 'close':
            current_player.show_cards()
            other_player.show_cards()
            other_player.receive(card_board.game_win())
            card_board.clear_board()
            return False
        else:
            print('\nInvalid input. Please enter bet, show or close.\n')
            continue


def take_extra_cards(current_name, other_name, current_player, deck, board):
    player1_extra_cards = input(f"{current_name} would you like to take 2 extra cards? It will cost 3 chips. Input b "
                                f"to buy them and anything else to not.")
    no_credits_exception = False
    if player1_extra_cards.lower() == 'b' and not no_credits_exception:
        f = input(f"{other_name} look away. {current_name}'s card will be shown. Enter anything to continue. ")
        current_player.update_cards(deck.deal_extra_cards(current_player.player_hand, current_name))
        no_credits_exception = current_player.bet_extra_cards()
        if no_credits_exception:
            return
        board.receive(3)
        current_player.show_cards()
        print(f"Carefully choose the cards you would like to remove.")
        count = 2

        extra_cards = []
        for cards in current_player.player_hand:
            if count == 1 and current_player.player_hand.index(cards) == 4:
                extra_cards.append(cards)
                count -= 1
                print(f"{Card(cards[0], cards[1])} has been automatically removed for you.")

            if count == 2 and current_player.player_hand.index(cards) == 3:
                extra_cards.append(cards)
                count -= 1
                print(f"{Card(cards[0], cards[1])} has been automatically removed for you.")
                continue

            if count == 0:
                current_player.update_cards(deck.remove_extra_cards(current_player.player_hand, extra_cards))
                current_player.show_cards()
                e = input('Two cards have been removed. Press anything to continue.')
                print('\n' * 50)
                break

            print(" ")
            print(Card(cards[0], cards[1]))

            input_state = input(
                "Would you like to remove this card? Input r to remove it and anything else to keep it.")
            print(" ")
            if input_state.lower() == 'r':
                extra_cards.append(cards)
                count -= 1


def game_round(entity1, entity1_name, entity2, entity2_name, board, deck):
    entity1.bet_start_game()
    entity2.bet_start_game()
    board.receive(4)

    print(" ")
    entity1.update_cards(deck.deal_start_cards(entity1_name, entity1.player_hand))
    entity2.update_cards(deck.deal_start_cards(entity2_name, entity2.player_hand))

    player1_top_card_num = values[entity1.player_hand[0][1]]
    player2_top_card_num = values[entity2.player_hand[0][1]]

    print(" ")

    if player1_top_card_num < player2_top_card_num:
        entity2.receive(3)
    elif player2_top_card_num < player1_top_card_num:
        entity1.receive(3)
    else:
        print('Top cards are the same! No chips will leave the table.')

    b = input(f"{entity1_name}'s cards will be shown now. {entity2_name} look away. Enter anything to continue")
    print(" ")
    entity1.show_cards()
    print(" ")
    c = input(
        f"Remember your cards {entity1_name} or write them down. Now {entity2_name}'s card will be shown. "
        f"Enter anything "
        f"to continue")
    print('\n' * 50)
    entity2.show_cards()
    d = input("Enter anything to continue")
    print('\n' * 50)

    take_extra_cards(entity1_name, entity2_name, entity1, deck, board)
    take_extra_cards(entity2_name, entity1_name, entity2, deck, board)

    round_state = True
    already_bet = 1
    while round_state:
        round_state = game_input(entity1_name, already_bet, entity1, entity2, board, game_board)
        if round_state is False:
            break
        else:
            already_bet = round_state

        round_state = game_input(entity2_name, already_bet, entity2, entity1, board, game_board)
        if round_state is False:
            break
        else:
            already_bet = round_state


print("Welcome to the game of Teen Patti")
print("The rules are as follows:")
print("To enter the game you pay 2 chips")
print("There will be 2 players. Both players get 3 cards and one card that is on the top is open while the others "
      "can only seen by the players.")
print("Whoever has the highest value card on the top gets 3 chips.")
print(
    "After that, the players can pay 3 extra chips to get 2 more cards. They can then choose the three cards they "
    "want and "
    "drop the 2 extra cards they have")
print("The players can start betting after that. Each player has three options every turn. They can drop which means"
      "they don't have to pay anything extra but the other player gets all the chips on the table.\nThey can Show"
      "which means that the other player has to 'show' their cards to you.\nWhoever has the highest value cards wins "
      "all "
      "the credits on the double. \nAnd lastly players can bet chips. Once a player has bet an x amount of chips the "
      "other "
      "player can only continue betting x amount of chips or more.\n")

# -------------------------------------------------------------------------------------------------------


a = input("\nStarting game... Enter any thing to continue")
player1_name = input("Enter your name player 1: ")
player2_name = input("Enter your name player 2: ")

game_board = Board()
game_deck = Deck()
game_deck.shuffle()

player1 = Player(Chips(player1_name, player2_name), player2_name)
player2 = Player(Chips(player2_name, player1_name), player1_name)

# --------------------------------------------------------------------------------------------------------

continue_game = True
round_count = 0

while continue_game:
    round_count += 1
    print(f'Round {round_count} has started')
    game_round(player1, player1_name, player2, player2_name, game_board, game_deck)
    game_state = input("This round has ended would you like to continue playing? Input y to continue.")
    if game_state.lower() != 'y':
        continue_game = False
