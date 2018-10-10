# Krypto Game

import random

# Formatting

card_top = " ____ "
card_top2 = "|    |"
card_bottom = "|____|"
spacing = "\t    "

# Deck Building

triple_cards = [1,2,3,4,5,6]
quadruple_cards = [7,8,9,10]
double_cards = [11,12,13,14,15,16,17]
single_cards = [18,19,20,21,22,23,24,25]

krypto_deck = 3 * triple_cards + 4 * quadruple_cards + 2 * double_cards + single_cards

# Shuffling

random.shuffle(krypto_deck)

krypto_input = krypto_deck[0:5]
krypto_target = str(krypto_deck[5])

# Dealing

print(5 * card_top + "\n" + 5 * card_top2 + 
      f"\n| {krypto_input[0]:^2} || {krypto_input[1]:^2} || {krypto_input[2]:^2} || {krypto_input[3]:^2} || {krypto_input[4]:^2} |\n"
          + 5 * card_bottom)

print("\n" + spacing + card_top + "\n" + spacing + card_top2 + "\n" + spacing + 
          f"| {krypto_target:^2} |" 
          + "\n" + spacing + card_bottom)