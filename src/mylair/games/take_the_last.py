"""
Take the Last Game for My Lair.

Rules:
- A pile of tokens starts on the table (default: 15 tokens).
- You and the computer take turns removing 1, 2, or 3 tokens from the pile.
- WINNING CONDITION: The player who takes the VERY LAST token WINS the game!
- The computer plays legal moves and explains its move simply after each turn.

Beginner Customization:
- You can adjust STARTING_TOKENS, MIN_TAKE, and MAX_TAKE below.
"""

from __future__ import annotations

import random
from typing import Tuple

from mylair.display import (
    NavigationAction,
    clear_screen,
    print_divider,
    print_header,
    prompt_input,
    style_text,
)

STARTING_TOKENS = 15
MIN_TAKE = 1
MAX_TAKE = 3


def compute_computer_move(remaining_tokens: int) -> int:
    """
    Decide the computer's token move.

    Strategic insight for 'Take the Last wins' with take range 1..3:
    - Multiples of 4 (4, 8, 12, 16) are losing positions for whoever must move.
    - If remaining is not a multiple of 4, taking (remaining % 4) leaves the opponent
      on a multiple of 4, securing a winning line.
    - If already on a multiple of 4, take 1 or a legal random amount.
    """
    if remaining_tokens <= MAX_TAKE:
        return remaining_tokens

    remainder = remaining_tokens % (MAX_TAKE + 1)
    if remainder != 0:
        return remainder
    else:
        # Trapped in a multiple of 4; take 1 to stall
        return 1


def render_token_pile(count: int, symbol: str = "●") -> str:
    """Render a visual representation of the token pile."""
    tokens_visual = (symbol + " ") * count
    return f"Tokens: [ {count:2d} ]  {tokens_visual.strip()}"


def play_take_the_last(
    title_style: str = "slant",
    color_scheme: str = "neon_cyan",
    direct_mode: bool = False,
) -> bool:
    """
    Run an interactive Take the Last game session.

    Returns:
    - True to return to menu / shell cleanly
    - False if user chose to quit the program
    """
    clear_screen()
    print_header(title_style, color_scheme, subtitle="Game: Take the Last")

    print(style_text("Welcome to Take the Last!", color_scheme, color_type="accent", bold=True))
    print("A tactical nim-style duel of token subtraction.\n")
    print("Rules:")
    print(f"  1. The game starts with a pile of {STARTING_TOKENS} tokens on the table.")
    print(f"  2. On each turn, you may take {MIN_TAKE}, 2, or {MAX_TAKE} tokens (up to what remains).")
    print("  3. WINNING CONDITION: The player who takes the VERY LAST token WINS!\n")
    print("Controls:")
    print(f"  Enter {MIN_TAKE}, 2, or {MAX_TAKE} on your turn.")
    print("  Enter 'b' to go back, 'q' to quit anytime.\n")
    print_divider(color_scheme)

    while True:
        # Choose who goes first
        print("Who should take the first turn?")
        print("  1. Player (You)")
        print("  2. Computer")
        print("  3. Coin toss (Random)")

        while True:
            order_act = prompt_input("Select starter [1-3] (b=back, q=quit): ", color_scheme=color_scheme, allow_back=True, allow_quit=True)
            if order_act == NavigationAction.QUIT:
                return False
            if order_act == NavigationAction.BACK:
                return True

            order_str = str(order_act).strip()
            if order_str == "1":
                player_turn = True
                break
            elif order_str == "2":
                player_turn = False
                break
            elif order_str == "3":
                player_turn = random.choice([True, False])
                starter_text = "You won the toss and take the first turn!" if player_turn else "Computer won the toss and takes the first turn!"
                print(style_text(f"\n🪙 Coin Toss: {starter_text}\n", color_scheme, color_type="accent"))
                break
            print(style_text("Please enter 1, 2, or 3.", color_scheme, color_type="warning"))

        pile = STARTING_TOKENS
        turn_count = 1

        print_divider(color_scheme)
        print(style_text(f"Match started with {pile} tokens! Goal: Take the very last token.", color_scheme, color_type="accent"))
        print(render_token_pile(pile))
        print_divider(color_scheme)

        while pile > 0:
            current_actor = "Your Turn" if player_turn else "Computer's Turn"
            print(f"\n--- Turn {turn_count}: {current_actor} ---")
            print(render_token_pile(pile))

            if player_turn:
                max_allowed = min(MAX_TAKE, pile)
                while True:
                    prompt_label = f"How many tokens do you take? (1-{max_allowed}) [b=back, q=quit]: "
                    act = prompt_input(prompt_label, color_scheme=color_scheme, allow_back=True, allow_quit=True)

                    if act == NavigationAction.QUIT:
                        return False
                    if act == NavigationAction.BACK:
                        return True

                    raw_val = str(act).strip()
                    try:
                        take_amount = int(raw_val)
                    except ValueError:
                        print(style_text(f"'{raw_val}' is not a valid number. Enter 1 to {max_allowed}.", color_scheme, color_type="warning"))
                        continue

                    if not (MIN_TAKE <= take_amount <= max_allowed):
                        print(style_text(f"You can only take between {MIN_TAKE} and {max_allowed} token(s).", color_scheme, color_type="warning"))
                        continue

                    break

                pile -= take_amount
                print(style_text(f"\nYou took {take_amount} token(s). Tokens left: {pile}", color_scheme, color_type="accent"))

                if pile == 0:
                    print()
                    print(style_text("★ VICTORY! You took the very last token and won the game! ★", color_scheme, color_type="success", bold=True))
                    break

                player_turn = False

            else:
                comp_move = compute_computer_move(pile)
                pile -= comp_move
                print(style_text(f"Computer removes {comp_move} token(s), leaving {pile} on the table.", color_scheme, color_type="warning"))

                if pile == 0:
                    print()
                    print(style_text("✗ Computer took the last token and won the game. Better luck next time!", color_scheme, color_type="error", bold=True))
                    break

                player_turn = True

            turn_count += 1

        print_divider(color_scheme)

        # Replay prompt
        replay_prompt = "Play another match of Take the Last? [y/n] (b=back, q=quit): "
        replay_act = prompt_input(replay_prompt, color_scheme=color_scheme, allow_back=True, allow_quit=True)

        if replay_act == NavigationAction.QUIT:
            return False
        if replay_act == NavigationAction.BACK:
            return True

        if str(replay_act).strip().lower() not in ("y", "yes"):
            print(style_text("\nThanks for playing Take the Last!\n", color_scheme, color_type="accent"))
            return True

        clear_screen()
        print_header(title_style, color_scheme, subtitle="Game: Take the Last")
