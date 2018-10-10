# Krypto
The beginnings of a Krypto game and solver

Krypto is a mathematical card game with very simple rules. The Krypto deck contains 56 cards:
- 3 cards for each number between and including 1 and 6
- 4 cards for each number between and including 7 and 10
- 2 cards for each number between and including 11 and 17
- 1 card for each number between and including 18 and 25
    
5 cards are randomly dealt in a straight line. These cards are known as the input cards. AN example is included below:
[6] [10] [7] [2] [11]

A 6th card is then randomly dealt, known as the target card:
[6] [10] [7] [2] [11]
[4]

The objective of the game is to use all 5 input cards exactly once to achieve the target card, using binary operations (addition, subtraction, multiplication and division):
(6 - 10 / 2) * (11 - 7) = 4

In multiplayer form, the first person to come up with the answer is the winner. 

For the purposes of this repository, we will be creating an individual game with user input functionality, accompanied by a solver that can identify the answer, if one exists. 

There is opportunity to expand the scope of this repository to a multiplayer game where bymultiple users will receive the same set of input and target cards. Whichever user can submit the solution in the shortest amount of time will be declared the winner. 

Official Krypto competition rules may differ to those detailed above. 
