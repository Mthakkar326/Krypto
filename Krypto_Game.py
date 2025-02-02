import pygame
import random
import sys
import re
import math
from collections import Counter

# -------------------------------
# Game Constants and Configurations
# -------------------------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# New Colors:
BG_COLOR = (0, 128, 0)  # A poker table green.
CARD_COLOR = (255, 255, 0)  # Yellow cards.
CARD_BORDER_COLOR = (0, 0, 0)  # Black border for cards.
TEXT_COLOR = (255, 255, 255)  # White text.
INPUT_BOX_COLOR = (255, 255, 255)  # White input box.
BUTTON_COLOR = (188, 188, 188)  # Grey buttons.
BUTTON_TEXT_COLOR = (0, 0, 0)  # Black text on buttons.
MODAL_BG_COLOR = (50, 50, 50)  # Dark grey for modal background.
MODAL_TEXT_COLOR = (255, 255, 255)  # White text for modal.

CARD_WIDTH = 80
CARD_HEIGHT = 120
CARD_MARGIN = 10

# The full deck of 56 cards (see game rules)
FULL_DECK = [
    1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 7, 8, 9,
    10, 7, 8, 9, 10, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 11, 12, 13, 14,
    15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25
]

# -------------------------------
# Helper Functions
# -------------------------------


def draw_card(surface, rect, number, font):
    """Draws a card as a rectangle with its number centered."""
    pygame.draw.rect(surface, CARD_COLOR, rect)
    pygame.draw.rect(surface, CARD_BORDER_COLOR, rect, 2)
    text = font.render(str(number), True, CARD_BORDER_COLOR)
    text_rect = text.get_rect(center=rect.center)
    surface.blit(text, text_rect)


def check_expression(expr, number_cards, target):
    """
    Verifies that:
      1. The expression contains only allowed characters.
      2. Exactly five numbers are used.
      3. The five numbers (as a multiset) exactly match the given number_cards.
      4. The evaluated expression equals the target.
    Returns a tuple (is_valid, message).
    """
    expr = expr.strip()
    if not re.fullmatch(r'[0-9+\-*/()\s]+', expr):
        return False, "Invalid characters in expression."
    tokens = re.findall(r'\d+', expr)
    if len(tokens) != 5:
        return False, f"You must use exactly five numbers (found {len(tokens)} numbers)."
    try:
        used_numbers = [int(token) for token in tokens]
    except Exception as e:
        return False, "Error parsing numbers."
    if Counter(used_numbers) != Counter(number_cards):
        return False, "The numbers used do not match the given number cards."
    try:
        result = eval(expr, {"__builtins__": None}, {})
    except Exception as e:
        return False, "Error evaluating expression: " + str(e)
    if math.isclose(result, target, rel_tol=1e-9):
        return True, "Correct! You win!"
    else:
        return False, f"Expression does not equal target. (Result: {result}, Target: {target})"


def solve_game(number_cards, target):
    """
    Attempts to find an expression that uses all number_cards exactly once
    and equals the target.
    Returns a solution string if found, otherwise returns a message.
    """
    numbers = [(num, str(num)) for num in number_cards]

    def search(nums):
        if len(nums) == 1:
            if math.isclose(nums[0][0], target, rel_tol=1e-9):
                return nums[0][1]
            else:
                return None
        for i in range(len(nums)):
            for j in range(len(nums)):
                if i != j:
                    a, expr_a = nums[i]
                    b, expr_b = nums[j]
                    new_nums = [
                        nums[k] for k in range(len(nums)) if k != i and k != j
                    ]
                    candidates = []
                    candidates.append((a + b, f"({expr_a}+{expr_b})"))
                    candidates.append((a * b, f"({expr_a}*{expr_b})"))
                    candidates.append((a - b, f"({expr_a}-{expr_b})"))
                    candidates.append((b - a, f"({expr_b}-{expr_a})"))
                    if not math.isclose(b, 0, rel_tol=1e-9):
                        candidates.append((a / b, f"({expr_a}/{expr_b})"))
                    if not math.isclose(a, 0, rel_tol=1e-9):
                        candidates.append((b / a, f"({expr_b}/{expr_a})"))
                    for value, new_expr in candidates:
                        next_nums = new_nums + [(value, new_expr)]
                        res = search(next_nums)
                        if res is not None:
                            return res
        return None

    solution = search(numbers)
    if solution is None:
        return "No solution found."
    return solution


# -------------------------------
# Main Game Function
# -------------------------------


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Krypto Game")
    clock = pygame.time.Clock()

    # Fonts for various texts
    font = pygame.font.SysFont(None, 36)
    small_font = pygame.font.SysFont(None, 28)
    big_title_font = pygame.font.SysFont(None, 64)
    rules_title_font = pygame.font.SysFont(None, 48)

    # Button definitions for game controls
    submit_button_rect = pygame.Rect(50, SCREEN_HEIGHT - 80, 140, 40)
    solve_button_rect = pygame.Rect(270, SCREEN_HEIGHT - 80, 140, 40)
    new_round_button_rect = pygame.Rect(SCREEN_WIDTH - 310, SCREEN_HEIGHT - 80,
                                        140, 40)
    game_rules_button_rect = pygame.Rect(SCREEN_WIDTH - 150, 20, 130, 40)

    # Modal (Game Rules) window dimensions and its Close button.
    modal_width = 600
    modal_height = 400
    modal_rect = pygame.Rect((SCREEN_WIDTH - modal_width) // 2,
                             (SCREEN_HEIGHT - modal_height) // 2, modal_width,
                             modal_height)
    close_button_rect = pygame.Rect(modal_rect.centerx - 50,
                                    modal_rect.bottom - 60, 100, 40)

    # A short description for the game rules modal.
    rules_text = [
        "Combine all five playing cards with arithmetic operations",
        "(+, -, *, /) to form an expression that equals the target card.", "",
        "- The deck has 56 cards numbered 1 to 25.",
        "- Six cards are drawn; the 6th card is the target,",
        "  and the other five are playing cards.",
        "- Use each playing card exactly once.", "- Parentheses are allowed."
    ]

    show_rules = False

    state = "enter_expression"
    available_cards = []
    target_card = None
    number_cards = []
    user_input = ""
    result_message = ""

    def new_round():
        nonlocal state, available_cards, target_card, number_cards, user_input, result_message
        deck = FULL_DECK.copy()
        random.shuffle(deck)
        available_cards = deck[:6]
        target_card = available_cards[5]
        number_cards = available_cards[:5]
        user_input = ""
        result_message = ""
        state = "enter_expression"

    new_round()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if show_rules:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    if close_button_rect.collidepoint(pos):
                        show_rules = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        show_rules = False
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        valid, message = check_expression(
                            user_input, number_cards, target_card)
                        result_message = message
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    else:
                        user_input += event.unicode
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if game_rules_button_rect.collidepoint(pos):
                        show_rules = True
                    if submit_button_rect.collidepoint(pos):
                        valid, message = check_expression(
                            user_input, number_cards, target_card)
                        result_message = message
                    if solve_button_rect.collidepoint(pos):
                        solution = solve_game(number_cards, target_card)
                        result_message = solution
                    if new_round_button_rect.collidepoint(pos):
                        new_round()

        screen.fill(BG_COLOR)

        # Updated title and subtitle placement.
        title_text = big_title_font.render("Krypto", True, TEXT_COLOR)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title_text, title_rect)
        subtitle_text = small_font.render("General Milz Media", True,
                                          TEXT_COLOR)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 90))
        screen.blit(subtitle_text, subtitle_rect)

        pygame.draw.rect(screen, BUTTON_COLOR, game_rules_button_rect)
        gr_text = small_font.render("Game Rules", True, BUTTON_TEXT_COLOR)
        gr_text_rect = gr_text.get_rect(center=game_rules_button_rect.center)
        screen.blit(gr_text, gr_text_rect)

        if not show_rules:
            target_label = font.render("Target", True, TEXT_COLOR)
            screen.blit(target_label, (50, 140))
            target_rect = pygame.Rect(50, 180, CARD_WIDTH, CARD_HEIGHT)
            draw_card(screen, target_rect, target_card, font)

            num_label = font.render("Playing Cards", True, TEXT_COLOR)
            screen.blit(num_label, (200, 140))
            start_x = 200
            y = 180
            for i, card in enumerate(number_cards):
                rect = pygame.Rect(start_x + i * (CARD_WIDTH + CARD_MARGIN), y,
                                   CARD_WIDTH, CARD_HEIGHT)
                draw_card(screen, rect, card, font)

            input_box = pygame.Rect(50, SCREEN_HEIGHT - 150,
                                    SCREEN_WIDTH - 220, 50)
            pygame.draw.rect(screen, INPUT_BOX_COLOR, input_box)
            pygame.draw.rect(screen, (0, 0, 0), input_box, 2)
            input_text = font.render(user_input, True, (0, 0, 0))
            screen.blit(input_text, (input_box.x + 5, input_box.y + 10))

            result_render = font.render(result_message, True, TEXT_COLOR)
            screen.blit(result_render, (50, SCREEN_HEIGHT - 220))

            pygame.draw.rect(screen, BUTTON_COLOR, submit_button_rect)
            submit_text = small_font.render("Submit", True, BUTTON_TEXT_COLOR)
            submit_text_rect = submit_text.get_rect(
                center=submit_button_rect.center)
            screen.blit(submit_text, submit_text_rect)

            pygame.draw.rect(screen, BUTTON_COLOR, solve_button_rect)
            solve_text = small_font.render("Solve", True, BUTTON_TEXT_COLOR)
            solve_text_rect = solve_text.get_rect(
                center=solve_button_rect.center)
            screen.blit(solve_text, solve_text_rect)

            pygame.draw.rect(screen, BUTTON_COLOR, new_round_button_rect)
            new_round_text = small_font.render("New Round", True,
                                               BUTTON_TEXT_COLOR)
            new_round_text_rect = new_round_text.get_rect(
                center=new_round_button_rect.center)
            screen.blit(new_round_text, new_round_text_rect)
        else:
            pygame.draw.rect(screen, MODAL_BG_COLOR, modal_rect)
            pygame.draw.rect(screen, (0, 0, 0), modal_rect, 2)

            modal_title = rules_title_font.render("Game Rules", True,
                                                  MODAL_TEXT_COLOR)
            modal_title_rect = modal_title.get_rect(center=(modal_rect.centerx,
                                                            modal_rect.y + 40))
            screen.blit(modal_title, modal_title_rect)

            # Display all the rule lines (less than 10 lines)
            start_y = modal_rect.y + 80
            line_height = 24
            for i, line in enumerate(rules_text):
                line_surf = small_font.render(line, True, MODAL_TEXT_COLOR)
                screen.blit(line_surf,
                            (modal_rect.x + 20, start_y + i * line_height))

            pygame.draw.rect(screen, BUTTON_COLOR, close_button_rect)
            close_text = small_font.render("Close", True, BUTTON_TEXT_COLOR)
            close_text_rect = close_text.get_rect(
                center=close_button_rect.center)
            screen.blit(close_text, close_text_rect)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
