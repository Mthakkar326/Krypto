import pygame
import random
import sys
import re
import math
from collections import Counter

# -------------------------------
# Game Constants and Configurations (1200x900)
# -------------------------------
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900

# Colors:
BG_COLOR = (0, 128, 0)            # A poker table green.
TEXT_COLOR = (255, 255, 255)      # White text.
INPUT_BOX_COLOR = (255, 255, 255) # White input box.
BUTTON_COLOR = (188, 188, 188)    # Grey buttons.
BUTTON_TEXT_COLOR = (0, 0, 0)     # Black text on buttons.
MODAL_BG_COLOR = (50, 50, 50)     # Dark grey for modal background.
MODAL_TEXT_COLOR = (255, 255, 255)  # White text for modal.

# Card dimensions (original 80×120 scaled by 1.5):
CARD_WIDTH = 120
CARD_HEIGHT = 180
CARD_MARGIN = 15

# The full deck of 56 cards (see game rules)
FULL_DECK = [
    1, 2, 3, 4, 5, 6,
    1, 2, 3, 4, 5, 6,
    1, 2, 3, 4, 5, 6,
    7, 8, 9, 10, 7, 8, 9, 10, 7, 8, 9, 10, 7, 8, 9, 10,
    11, 12, 13, 14, 15, 16, 17, 11, 12, 13, 14, 15, 16, 17,
    18, 19, 20, 21, 22, 23, 24, 25
]

# -------------------------------
# Helper Functions
# -------------------------------

def draw_card(surface, rect, number, card_images):
    """
    Blits the preloaded image corresponding to 'number' onto 'surface' at 'rect'.
    """
    surface.blit(card_images[number], rect)

def check_expression(expr, number_cards, target):
    """
    Checks that:
      - The expression contains only allowed characters.
      - Exactly five numbers are used.
      - The multiset of numbers in the expression exactly matches number_cards.
      - The evaluated result equals the target.
    Returns (is_valid, message).
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
    Attempts to automatically find an expression that uses all number_cards
    exactly once to reach the target.
    Returns the solution string if found, or a message otherwise.
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
                    new_nums = [nums[k] for k in range(len(nums)) if k != i and k != j]
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

    # Load fonts (scaled for 1200x900)
    font = pygame.font.SysFont(None, 54)         # 36 * 1.5
    small_font = pygame.font.SysFont(None, 42)     # 28 * 1.5
    big_title_font = pygame.font.SysFont(None, 96) # 64 * 1.5
    rules_title_font = pygame.font.SysFont(None, 72)  # 48 * 1.5

    # Preload card images (from folder "images") and scale them.
    card_images = {}
    for i in range(1, 26):
        img = pygame.image.load(f"images/card_{i}.png")
        img = pygame.transform.scale(img, (CARD_WIDTH, CARD_HEIGHT))
        card_images[i] = img

    # Button definitions (scaled from the high-res version for 1200x900):
    submit_button_rect = pygame.Rect(75, SCREEN_HEIGHT - 120, 210, 60)
    solve_button_rect = pygame.Rect(405, SCREEN_HEIGHT - 120, 210, 60)
    new_round_button_rect = pygame.Rect(SCREEN_WIDTH - 465, SCREEN_HEIGHT - 120, 210, 60)
    game_rules_button_rect = pygame.Rect(SCREEN_WIDTH - 225, 30, 195, 60)

    # Modal (Game Rules) window dimensions and its Close button.
    modal_width = 900
    modal_height = 600
    modal_rect = pygame.Rect((SCREEN_WIDTH - modal_width) // 2,
                             (SCREEN_HEIGHT - modal_height) // 2,
                             modal_width, modal_height)
    close_button_rect = pygame.Rect(modal_rect.centerx - 75,
                                    modal_rect.bottom - 90,
                                    150, 60)

    # A short description for the game rules modal.
    rules_text = [
        "Combine all five given number cards with arithmetic operations",
        "(+, -, *, /) to form an expression that equals the target card.",
        "",
        "- The deck has 56 cards numbered 1 to 25.",
        "- Six cards are drawn; the 6th card is the target,",
        "  and the other five are playing cards.",
        "- Use each playing card exactly once.",
        "- Parentheses are allowed."
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
                        valid, message = check_expression(user_input, number_cards, target_card)
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
                        valid, message = check_expression(user_input, number_cards, target_card)
                        result_message = message
                    if solve_button_rect.collidepoint(pos):
                        solution = solve_game(number_cards, target_card)
                        result_message = solution
                    if new_round_button_rect.collidepoint(pos):
                        new_round()

        screen.fill(BG_COLOR)

        # Title and subtitle (moved down a bit).
        title_text = big_title_font.render("Krypto", True, TEXT_COLOR)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 75))
        screen.blit(title_text, title_rect)
        subtitle_text = small_font.render("General Milz Media", True, TEXT_COLOR)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 135))
        screen.blit(subtitle_text, subtitle_rect)

        # Draw the "Game Rules" button.
        pygame.draw.rect(screen, BUTTON_COLOR, game_rules_button_rect)
        gr_text = small_font.render("Game Rules", True, BUTTON_TEXT_COLOR)
        gr_text_rect = gr_text.get_rect(center=game_rules_button_rect.center)
        screen.blit(gr_text, gr_text_rect)

        if not show_rules:
            # Draw the target card.
            target_label = font.render("Target Card", True, TEXT_COLOR)
            screen.blit(target_label, (75, 210))
            target_rect = pygame.Rect(75, 270, CARD_WIDTH, CARD_HEIGHT)
            draw_card(screen, target_rect, target_card, card_images)

            # Draw the number cards.
            num_label = font.render("Number Cards", True, TEXT_COLOR)
            screen.blit(num_label, (300, 210))
            start_x = 300
            y = 270
            for i, card in enumerate(number_cards):
                rect = pygame.Rect(start_x + i * (CARD_WIDTH + CARD_MARGIN), y, CARD_WIDTH, CARD_HEIGHT)
                draw_card(screen, rect, card, card_images)

            # Draw the expression input box.
            input_box = pygame.Rect(75, SCREEN_HEIGHT - 225, SCREEN_WIDTH - 440, 75)
            pygame.draw.rect(screen, INPUT_BOX_COLOR, input_box)
            pygame.draw.rect(screen, (0, 0, 0), input_box, 2)
            input_text = font.render(user_input, True, (0, 0, 0))
            screen.blit(input_text, (input_box.x + 5, input_box.y + 10))

            # Draw the result/feedback message.
            result_render = font.render(result_message, True, TEXT_COLOR)
            screen.blit(result_render, (75, SCREEN_HEIGHT - 315))

            # Draw control buttons.
            pygame.draw.rect(screen, BUTTON_COLOR, submit_button_rect)
            submit_text = small_font.render("Submit", True, BUTTON_TEXT_COLOR)
            submit_text_rect = submit_text.get_rect(center=submit_button_rect.center)
            screen.blit(submit_text, submit_text_rect)

            pygame.draw.rect(screen, BUTTON_COLOR, solve_button_rect)
            solve_text = small_font.render("Solve", True, BUTTON_TEXT_COLOR)
            solve_text_rect = solve_text.get_rect(center=solve_button_rect.center)
            screen.blit(solve_text, solve_text_rect)

            pygame.draw.rect(screen, BUTTON_COLOR, new_round_button_rect)
            new_round_text = small_font.render("New Round", True, BUTTON_TEXT_COLOR)
            new_round_text_rect = new_round_text.get_rect(center=new_round_button_rect.center)
            screen.blit(new_round_text, new_round_text_rect)
        else:
            # Draw the modal overlay for Game Rules.
            pygame.draw.rect(screen, MODAL_BG_COLOR, modal_rect)
            pygame.draw.rect(screen, (0, 0, 0), modal_rect, 2)

            modal_title = rules_title_font.render("Game Rules", True, MODAL_TEXT_COLOR)
            modal_title_rect = modal_title.get_rect(center=(modal_rect.centerx, modal_rect.y + 40))
            screen.blit(modal_title, modal_title_rect)

            start_y = modal_rect.y + 80
            line_height = 48  # Increased spacing for clarity.
            for i, line in enumerate(rules_text):
                line_surf = small_font.render(line, True, MODAL_TEXT_COLOR)
                screen.blit(line_surf, (modal_rect.x + 20, start_y + i * line_height))

            pygame.draw.rect(screen, BUTTON_COLOR, close_button_rect)
            close_text = small_font.render("Close", True, BUTTON_TEXT_COLOR)
            close_text_rect = close_text.get_rect(center=close_button_rect.center)
            screen.blit(close_text, close_text_rect)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()