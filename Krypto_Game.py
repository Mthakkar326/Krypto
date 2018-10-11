# KRYPTO GAME

import random
import re

# FORMATTING

card_top = " ____ "
card_top2 = "|    |"
card_bottom = "|____|"
spacing = "\t    "

# DECK BUILDING

triple_cards = [1,2,3,4,5,6]
quadruple_cards = [7,8,9,10]
double_cards = [11,12,13,14,15,16,17]
single_cards = [18,19,20,21,22,23,24,25]
krypto_deck = 3 * triple_cards + 4 * quadruple_cards + 2 * double_cards + single_cards

# SHUFFLING

random.shuffle(krypto_deck)
krypto_input = krypto_deck[0:5]
krypto_target = (krypto_deck[5])

# DEALING

print(5 * card_top + "\n" + 5 * card_top2 + 
      f"\n|{krypto_input[0]:^4}||{krypto_input[1]:^4}||{krypto_input[2]:^4}||{krypto_input[3]:^4}||{krypto_input[4]:^4}|\n"
          + 5 * card_bottom)

print("\n" + spacing + card_top + "\n" + spacing + card_top2 + "\n" + spacing + 
          f"|{krypto_target:^4}|" 
          + "\n" + spacing + card_bottom + "\n")

# USER INTERACTION

user_input = input("Type your solution here: ")
user_input = ''.join(user_input.split())

# CHECK TO SEE IF INPUT CAN BE EVALUATED

try:
    eval(user_input)
except Exception:
    print("You have entered an invalid equation.")
else:
    
# CHECK TO SEE IF ONLY BINARY OPERATORS WERE USED
    
    user_input_sym = user_input
    user_input_sym = list(map(str,re.split("[1234567890]", user_input_sym)))
    incorrect_sym = ['//', '**', '%', '++', '--', '(-', '*-', '+-', '/-']
    if set(user_input_sym).isdisjoint(set(incorrect_sym)) == False:
        print("You can only use binary operations.")
    else:
        if user_input[0] == '-':
            print("You can only use binary operations.")
        else:
            
# CHECK TO SEE IF CORRECT NUMBERS WERE USED
            
            user_input_num = user_input       
            user_input_num = list(map(str,re.split("[()+-/*]", user_input_num)))        
            user_input_num = list(filter(None, user_input_num))
            user_input_num = list(map(int, user_input_num))
            user_input_num.sort()
            krypto_input.sort()
            if krypto_input != user_input_num:
                print("You did not use the right input numbers.")
            else:
            
# CHECK TO SEE IF ANSWER IS CORRECT
                
                if eval(user_input) == krypto_target:
                    print("You are correct!")
                else:
                    print("You are incorrect.")
