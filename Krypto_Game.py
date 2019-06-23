# KRYPTO GAME

import random
import re
import sys
from itertools import permutations

def deck_construction():
    # BUILD & SHUFFLE THE DECK
    krypto_deck = (list(range(1,7))*3) + (list(range(7,11))*4) + (list(range(11,18))*2) + list(range(18,26))
    random.shuffle(krypto_deck)
    return krypto_deck# KRYPTO GAME

def print_format(print_input, print_output):
    # PRINT FORMAT AS CARDS
    card_top = " ____ "
    card_top2 = "|    |"
    card_bottom = "|____|"
    spacing = "\t    "
    print_hand = (5 * card_top + "\n" + 5 * card_top2 +
          f"\n|{print_input[0]:^4}||{print_input[1]:^4}||{print_input[2]:^4}||{print_input[3]:^4}||{print_input[4]:^4}|\n"
          + 5 * card_bottom + "\n" + spacing + card_top + "\n" + spacing + card_top2 + "\n" + spacing +
          f"|{print_output:^4}|" + "\n" + spacing + card_bottom + "\n")
    return print_hand

def check_solution(user_response, krypto_start, krypto_end):
    # CHECK IF RESPONSE CAN BE EVALUATED
    try:
        eval(user_response)
    except Exception:
        print("\nYou have entered an invalid equation.")
        user_solution(krypto_start, krypto_end)
    else:

        # CHECK IF RESPONSE USES ONLY BINARY OPERATORS
        user_input_sym = user_response
        user_input_sym = list(map(str,re.split("[1234567890]", user_input_sym)))     # splits into list of operators
        incorrect_sym = ['//', '**', '%', '++', '--', '(-', '*-', '+-', '/-','_',',']     # static list of incorrect operators
        if set(user_input_sym).isdisjoint(set(incorrect_sym)) == False or user_response[0] == '-':     # ensure there are no incorrect operators used
            print("\nYou can only use binary operations.")
            user_solution(krypto_start, krypto_end)
        else:

            # CHECK IF RESPONSE USES CORRECT NUMBERS
            user_input_num = user_response
            user_input_num = list(map(str,re.split("[()+-/*]", user_input_num)))     # splits into list of numbers
            user_input_num = list(filter(None, user_input_num))     # removes blanks
            user_input_num = list(map(int, user_input_num))     # converts list elements to integers
            user_input_num.sort()
            krypto_start.sort()
            if krypto_start != user_input_num:
                print("\nYou did not use the right input numbers.")
                user_solution(krypto_start, krypto_end)
            else:

                # CHECK IF RESPONSE EQUALS TARGET
                if eval(user_response) == krypto_end:
                    print("\nYou are correct!")
                    play_again()
                else:
                    print("\nYou are incorrect.")
                    user_solution()

def krypto_solver(solve_input, solve_output):
    # BRUTE FORCE SOLVER
    kp = list(permutations(solve_input))
    op = list(set(list(permutations(['+','+','+','+','-','-','-','-','/','/','/','/','*','*','*','*'],4))))
    solved = False

    # GENERATING ALL PERMUTATIONS OF INPUTS, BINARY OPERATORS, PARENTHESES
    for n in range(len(kp)):
        for p in range(len(op)):
            potential_solution = ''.join([str(kp[n][0]),op[p][0],str(kp[n][1]),op[p][1],str(kp[n][2]),op[p][2],str(kp[n][3]),op[p][3],str(kp[n][4])])
            potential_solution1 = ''.join([str(kp[n][0]),op[p][0],'(',str(kp[n][1]),op[p][1],'(',str(kp[n][2]),op[p][2],'(',str(kp[n][3]),op[p][3],str(kp[n][4]),')))'])
            potential_solution2 = ''.join([str(kp[n][0]),op[p][0],'(',str(kp[n][1]),op[p][1],'((',str(kp[n][2]),op[p][2],str(kp[n][3]),')',op[p][3],str(kp[n][4]),'))'])
            potential_solution3 = ''.join([str(kp[n][0]),op[p][0],'((',str(kp[n][1]),op[p][1],str(kp[n][2]),')',op[p][2],'(',str(kp[n][3]),op[p][3],str(kp[n][4]),'))'])
            potential_solution4 = ''.join([str(kp[n][0]),op[p][0],'((',str(kp[n][1]),op[p][1],'(',str(kp[n][2]),op[p][2],str(kp[n][3]),'))',op[p][3],str(kp[n][4]),')'])
            potential_solution5 = ''.join([str(kp[n][0]),op[p][0],'(((',str(kp[n][1]),op[p][1],str(kp[n][2]),')',op[p][2],str(kp[n][3]),')',op[p][3],str(kp[n][4]),')'])
            potential_solution6 = ''.join(['(',str(kp[n][0]),op[p][0],str(kp[n][1]),')',op[p][1],'(',str(kp[n][2]),op[p][2],'(',str(kp[n][3]),op[p][3],str(kp[n][4]),'))'])
            potential_solution7 = ''.join(['(',str(kp[n][0]),op[p][0],str(kp[n][1]),')',op[p][1],'((',str(kp[n][2]),op[p][2],str(kp[n][3]),')',op[p][3],str(kp[n][4]),')'])
            potential_solution8 = ''.join(['(',str(kp[n][0]),op[p][0],'(',str(kp[n][1]),op[p][1],str(kp[n][2]),'))',op[p][2],'(',str(kp[n][3]),op[p][3],str(kp[n][4]),')'])
            potential_solution9 = ''.join(['(',str(kp[n][0]),op[p][0],'(',str(kp[n][1]),op[p][1],'(',str(kp[n][2]),op[p][2],str(kp[n][3]),')))',op[p][3],str(kp[n][4])])
            potential_solution10 = ''.join(['(',str(kp[n][0]),op[p][0],'((',str(kp[n][1]),op[p][1],str(kp[n][2]),')',op[p][2],str(kp[n][3]),'))',op[p][3],str(kp[n][4])])
            potential_solution11 = ''.join(['((',str(kp[n][0]),op[p][0],str(kp[n][1]),')',op[p][1],str(kp[n][2]),')',op[p][2],'(',str(kp[n][3]),op[p][3],str(kp[n][4]),')'])
            potential_solution12 = ''.join(['((',str(kp[n][0]),op[p][0],str(kp[n][1]),')',op[p][1],'(',str(kp[n][2]),op[p][2],str(kp[n][3]),'))',op[p][3],str(kp[n][4])])
            potential_solution13 = ''.join(['((',str(kp[n][0]),op[p][0],'(',str(kp[n][1]),op[p][1],str(kp[n][2]),'))',op[p][2],str(kp[n][3]),')',op[p][3],str(kp[n][4])])
            potential_solution14 = ''.join(['(((',str(kp[n][0]),op[p][0],str(kp[n][1]),')',op[p][1],str(kp[n][2]),')',op[p][2],str(kp[n][3]),')',op[p][3],str(kp[n][4])])

            # CHECKING IF ANY SOLUTIONS EQUAL THE TARGET. THE TRY SKIPS DIVIDE BY ZERO ERRORS
            try:
                if eval(potential_solution) == solve_output:
                    print(potential_solution, " = ", solve_output)
                    solved = True
                    break
            except: pass
            try:
                if eval(potential_solution1) == solve_output:
                    print(potential_solution1, " = ", solve_output)
                    solved = True
                    break
            except: pass
            try:
                if eval(potential_solution2) == solve_output:
                    print(potential_solution2, " = ", solve_output)
                    solved = True
                    break
            except: pass
            try:
                if eval(potential_solution3) == solve_output:
                    print(potential_solution3, " = ", solve_output)
                    solved = True
                    break
            except: pass
            try:
                if eval(potential_solution4) == solve_output:
                    print(potential_solution4, " = ", solve_output)
                    solved = True
                    break
            except: pass
            try:
                if eval(potential_solution5) == solve_output:
                    print(potential_solution5, " = ", solve_output)
                    solved = True
                    break
            except: pass
            try:
                if eval(potential_solution6) == solve_output:
                    print(potential_solution6, " = ", solve_output)
                    solved = True
                    break
            except: pass
            try:
                if eval(potential_solution7) == solve_output:
                    print(potential_solution7, " = ", solve_output)
                    solved = True
                    break
            except: pass
            try:
                if eval(potential_solution8) == solve_output:
                    print(potential_solution8, " = ", solve_output)
                    solved = True
                    break
            except: pass
            try:
                if eval(potential_solution9) == solve_output:
                    print(potential_solution9, " = ", solve_output)
                    solved = True
                    break
            except: pass
            try:
                if eval(potential_solution10) == solve_output:
                    print(potential_solution10, " = ", solve_output)
                    solved = True
                    break
            except: pass
            try:
                if eval(potential_solution11) == solve_output:
                    print(potential_solution11, " = ", solve_output)
                    solved = True
                    break
            except: pass
            try:
                if eval(potential_solution12) == solve_output:
                    print(potential_solution12, " = ", solve_output)
                    solved = True
                    break
            except: pass
            try:
                if eval(potential_solution13) == solve_output:
                    print(potential_solution13, " = ", solve_output)
                    solved = True
                    break
            except: pass
            try:
                if eval(potential_solution14) == solve_output:
                    print(potential_solution14, " = ", solve_output)
                    solved = True
                    break
            except: pass
        if solved == True:
            play_again()
            break
    else:
        print("No solution exists.")
        play_again()

def game_instructions():
    # PRINT GAME INSTRUCTIONS
    print("\nGAME INSTRUCTIONS\n\n"\
          "Krypto is a mathematical card game with very simple rules. "\
          "The Krypto deck contains 56 cards labelled 1 through 25. "\
          "Five cards are randomly dealt in a straight line, known as the input cards. "\
          "An example is included below:\n[6] [10] [7] [2] [11]\n\n"\
          "A sixth card is then randomly dealt, known as the target card:\n[6] [10] [7] [2] [11]\n[4]\n\n"\
          "The objective of the game is to use all 5 input cards exactly once to achieve the target card, using binary operations "\
          "(addition, subtraction, multiplication and division):\n(6 - 10 / 2) * (11 - 7) = 4\n\n---\n")

def krypto_game():
    # PRINT KRYPTO HAND
    global krypto_input
    global krypto_target
    global krypto_hand
    krypto_input = deck_construction()[0:5]
    krypto_target = deck_construction()[5]
    krypto_hand = print_format(krypto_input, krypto_target)
    print(krypto_hand)
    print("Enter your solution below. You can also enter the following commands:\n'help' to view game instructions\n'reset' to reshuffle the Krypto hand\n'solve' to generate a solution\n'quit' to exit the game")
    user_solution()

def user_solution():
    # USER INPUT
    user_input = input("Enter your response here: ")
    user_input = ''.join(user_input.split())
    user_input = user_input.lower()

    # EVALUATE USER INPUT
    if user_input == 'help':
        game_instructions()
        print(krypto_hand)
        user_solution()
    elif user_input == 'reset':
        krypto_game()
    elif user_input == 'solve':
        krypto_solver(krypto_input, krypto_target)
    elif user_input == 'quit':
        sys.exit()
    else:
        check_solution(user_input, krypto_input, krypto_target)

def play_again():
    # PLAY AGAIN?
    user_input = input("Play again? (y/n): ")
    user_input = user_input.lower()
    if user_input == 'y':
        krypto_game()
    elif user_input == 'n':
        sys.exit(1)
    else:
        print("You did not select a valid response.")
        play_again()

krypto_game()
