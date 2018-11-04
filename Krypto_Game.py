# KRYPTO GAME

import random
import re

def deck_construction():
    # BUILD & SHUFFLE THE DECK
    krypto_deck = (list(range(1,7))*3) + (list(range(7,11))*4) + (list(range(11,18))*2) + list(range(18,26))
    random.shuffle(krypto_deck)
    return krypto_deck

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

def game_instructions():
    # PRINT GAME INSTRUCTIONS
    print("Krypto is a mathematical card game with very simple rules. "\
          "The Krypto deck contains 56 cards labelled 1 through 25. "\
          "Five cards are randomly dealt in a straight line, known as the input cards. "\
          "An example is included below:\n[6] [10] [7] [2] [11]\n\n"\
          "A sixth card is then randomly dealt, known as the target card:\n[6] [10] [7] [2] [11]\n[4]\n\n"\
          "The objective of the game is to use all 5 input cards exactly once to achieve the target card, using binary operations "\
          "(addition, subtraction, multiplication and division):\n(6 - 10 / 2) * (11 - 7) = 4")
       
def check_solution(user_response, krypto_start, krypto_end):
    # CHECK IF RESPONSE CAN BE EVALUATED
    try:
        eval(user_response)
    except Exception:
        return "You have entered an invalid equation."
    else:
   
        # CHECK IF RESPONSE USES ONLY BINARY OPERATORS
        user_input_sym = user_response
        user_input_sym = list(map(str,re.split("[1234567890]", user_input_sym)))     # splits into list of operators
        incorrect_sym = ['//', '**', '%', '++', '--', '(-', '*-', '+-', '/-','_',',']     # static list of incorrect operators
        if set(user_input_sym).isdisjoint(set(incorrect_sym)) == False or user_response[0] == '-':     # ensure there are no incorrect operators used
            return "You can only use binary operations."
        else:
            
            # CHECK IF RESPONSE USES CORRECT NUMBERS               
            user_input_num = user_response       
            user_input_num = list(map(str,re.split("[()+-/*]", user_input_num)))     # splits into list of numbers
            user_input_num = list(filter(None, user_input_num))     # removes blanks
            user_input_num = list(map(int, user_input_num))     # converts list elements to integers
            user_input_num.sort()
            krypto_start.sort()
            if krypto_start != user_input_num:
                return "You did not use the right input numbers."
            else:
                
                # CHECK IF RESPONSE EQUALS TARGET               
                if eval(user_response) == krypto_end:
                    return "You are correct!"
                else:
                    return "You are incorrect."

def krypto_game():
    # PRINT KRYPTO HAND
    krypto_input = deck_construction()[0:5]
    krypto_target = deck_construction()[5]
    krypto_hand = print_format(krypto_input, krypto_target)
    print(krypto_hand)

    # USER INPUT
    user_input = input("Enter your solution below. You can also enter the following commands:\n'help' to view game instructions\n'reset' to reshuffle the Krypto hand\n'solve' to generate a solution\n\nEnter your response here: ")
    user_input = ''.join(user_input.split())
    user_input = user_input.lower()
    
    # EVALUATE USER INPUT    
    if user_input == 'help':
        game_instructions()
    elif user_input == 'reset':
        krypto_game()
    elif user_input == 'solve':
        print("We are still working on developing a solver.")
    else:     
        print(check_solution(user_input, krypto_input, krypto_target))

krypto_game()
