# player input function
def user_xo_check():
    xo_elements = ['O', 'X']

    player_1choice = 'Temp'
    while player_1choice not in xo_elements:
        player_1choice = input('Player 1, would you like to choose X or O? Enter X or O: ')

        if player_1choice not in xo_elements:
            print('\n')
            print('I do not understand, please enter O or X')

    xo_elements.remove(player_1choice)
    player_2choice = xo_elements[0]

    print(f'\nPlayer 1, you have chosen {player_1choice}. Player 2 you will be playing {player_2choice}.')
    return [player_1choice, player_2choice]


# output function
def tic_tac_out(tic_list):
    print(f' |   |   |   |\n | {tic_list[0][0]} | {tic_list[0][1]} | {tic_list[0][2]} |\n |   |   |   |\n---------------')
    print(f' |   |   |   |\n | {tic_list[1][0]} | {tic_list[1][1]} | {tic_list[1][2]} |\n |   |   |   |\n---------------')
    print(f' |   |   |   |\n | {tic_list[2][0]} | {tic_list[2][1]} | {tic_list[2][2]} |\n |   |   |   |')


def whose_turn(round_count, player_1choice, player_2choice):
    if round_count % 2 == 0:
        return [player_2choice, 2]
    return [player_1choice, 1]


def user_input(tic_list, turn, answers_list):
    cell_choice = 'a'
    while cell_choice in answers_list or not cell_choice.isdigit() or cell_choice not in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
        cell_choice = input(f'Enter the cell you choose Player {turn[1]}: ')  # use answer_storage function to not allow repetition
        if not cell_choice.isdigit():
            print("You need to input an integer")
            continue
        if int(cell_choice) in answers_list:
            print("You have already inserted a response over here")
            cell_choice = int(cell_choice)
        if not 1 <= int(cell_choice) <= 9:
            print("Invalid input. Please make sure your input is between 9 and 1.")

    # cell_choice = 0
    # while 1 <= cell_choice <= 9:
    #     cell_choice = input(f'Enter the cell you choose Player {turn[1]}: ')  # use answer_storage function to not allow repetition
    #     if cell_choice not in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
    #         print("Out of range. Input an integer between 1 and 9")

    cell_choice = int(cell_choice)
    answer_storage(cell_choice, answers_list)
    if 7 <= cell_choice <= 9:
        tic_list[0][cell_choice-7] = turn[0]
    elif 4 <= cell_choice <= 6:
        tic_list[1][cell_choice-4] = turn[0]
    elif 1 <= cell_choice <= 3:
        tic_list[2][cell_choice-1] = turn[0]


def winner_check(tic_list, player_choice):
    check_list_row = [tic_list[0][0] == tic_list[1][0] == tic_list[2][0] == player_choice,
                      tic_list[0][1] == tic_list[1][1] == tic_list[2][1] == player_choice,
                      tic_list[0][2] == tic_list[1][2] == tic_list[2][2] == player_choice]

    check_list_column = [tic_list[0][0] == tic_list[0][1] == tic_list[0][2] == player_choice,
                         tic_list[1][0] == tic_list[1][1] == tic_list[1][2] == player_choice,
                         tic_list[2][0] == tic_list[2][1] == tic_list[2][2] == player_choice]

    check_list_diagonal = [tic_list[0][0] == tic_list[1][1] == tic_list[2][2] == player_choice,
                           tic_list[0][2] == tic_list[1][1] == tic_list[2][0] == player_choice]

    if True in check_list_row:
        return True

    if True in check_list_column:
        return True

    if True in check_list_diagonal:
        return True

    return False


def answer_storage(answer, input_list):
    input_list.append(answer)
    return input_list


def tic_tac_toe_game():
    print("Starting Tic Tac Toe Game...\n")
    input("Enter anything to continue: ")

    Tic_list = [[7, 8, 9], [4, 5, 6], [1, 2, 3]]
    print(
        "\nYou can use the numbers in your numpad to place X or O position wise.\n You can see below which nums correspond to which position if you do not have a numpad or yours is different.")
    tic_tac_out(Tic_list)
    print('\n')
    input("Enter anything to start the game: ")

    print('\n Below is the Tic Tac Toe Table')
    Tic_list = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    tic_tac_out(Tic_list)

    win_check = False
    choices = user_xo_check()
    count = 0
    answers_list = ['0', 'a']

    while not win_check:
        count += 1
        player_turn = whose_turn(count, choices[0], choices[1])
        print("  ")
        print(f'GAME {count}')
        user_input(Tic_list, player_turn, answers_list)
        tic_tac_out(Tic_list)
        win_check = winner_check(Tic_list, player_turn[0])
        if count == 9 and not win_check:
            print("It's a tie!")
            break
    else:
        player_turn = whose_turn(count, choices[0], choices[1])
        print(f"Player {player_turn[1]} You won!!")


play_again = "Y"
while play_again == "Y":
    tic_tac_toe_game()
    play_again = input("Do you want to play again? Input Y to play again and any key to exit: ")

print("Thanks for playing!")
