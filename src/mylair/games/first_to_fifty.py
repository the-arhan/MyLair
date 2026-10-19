"""
First to Fifty Game for My Lair.

Rules:
- A shared running total starts at 0.
- You and the computer take turns choosing a number from 1 to 10.
- The chosen number is added to the shared total.
- The first player to bring the total to 50 (or higher) WINS!

Controls:
- Enter a whole number from 1 to 10 on your turn.
- Enter 'b' to go back, 'q' to quit anytime.
"""

from __future__ import annotations

import random
import time
from typing import Optional

from mylair.display import (
    NavigationAction,
    clear_screen,
    print_divider,
    print_header,
    prompt_input,
    style_text,
)

TARGET_SCORE = 50
MIN_ADD = 1
MAX_ADD = 10


def compute_computer_move(current_total: int) -> int:
    """
    Decide the computer's move intelligently while remaining understandable.

    Strategic insight for target 50 with step range 1..10:
    - Target 50 is won from 40..49 by adding (50 - total).
    - In general, positions congruent to 6 (mod 11) [i.e., 6, 17, 28, 39, 50]
      are winning key positions.
    """
    needed = TARGET_SCORE - current_total

    # If the computer can win in this turn, take the win!
    if needed <= MAX_ADD:
        return needed

    # Try to land on a key target position (6, 17, 28, 39)
    targets = [6, 17, 28, 39]
    for target in targets:
        diff = target - current_total
        if MIN_ADD <= diff <= MAX_ADD:
            return diff

    # Otherwise, pick a sensible move (between 3 and 7, or random)
    return random.randint(min(3, needed), min(7, needed, MAX_ADD))


def render_progress_bar(total: int, target: int = 50, width: int = 25) -> str:
    """Render a text progress bar showing progress toward the target."""
    clamped_total = max(0, min(total, target))
    filled_length = int(width * (clamped_total / target))
    bar = "█" * filled_length + "░" * (width - filled_length)
    percent = int((clamped_total / target) * 100)
    return f"[{bar}] {total}/{target} ({percent}%)"


def play_first_to_fifty(
    title_style: str = "slant",
    color_scheme: str = "neon_cyan",
    direct_mode: bool = False,
) -> bool:
    """
    Run an interactive First to Fifty game match.

    Returns:
    - True to return to menu / shell cleanly
    - False if user chose to quit the program
    """
    clear_screen()
    print_header(title_style, color_scheme, subtitle="Game: First to Fifty")

    print(style_text("Welcome to First to Fifty!", color_scheme, color_type="accent", bold=True))
    print("A tactical turn-based race to 50 against the computer.\n")
    print("Rules:")
    print("  1. The game begins with a shared total of 0.")
    print("  2. On each turn, add any number from 1 to 10 to the total.")
    print("  3. The first player to reach or pass 50 wins the game!")
    print("  4. Enter 'b' to go back, 'q' to quit at any time.\n")
    print_divider(color_scheme)

    while True:
        # Ask who goes first
        print("Who should take the first turn?")
        print("  1. Player (You)")
        print("  2. Computer")
        print("  3. Coin toss (Random)")

        choice_act = prompt_input("Choose [1-3] (b=back, q=quit): ", color_scheme=color_scheme)
        if choice_act == NavigationAction.QUIT:
            return False
        if choice_act == NavigationAction.BACK:
            return True

        choice_str = str(choice_act).strip()
        if choice_str == "1":
            player_turn = True
        elif choice_str == "2":
            player_turn = False
        elif choice_str == "3":
            player_turn = random.choice([True, False])
            starter = "You won the toss and start!" if player_turn else "Computer won the toss and starts!"
            print(style_text(f"\nCoin Toss: {starter}\n", color_scheme, color_type="accent"))
        else:
            print(style_text("Please enter 1, 2, or 3.\n", color_scheme, color_type="warning"))
            continue

        # Match loop
        shared_total = 0
        turn_number = 1
        print_divider(color_scheme)
        print(style_text("Match started! Running total is 0.", color_scheme, color_type="accent"))
        print(render_progress_bar(shared_total, TARGET_SCORE))
        print_divider(color_scheme)

        match_over = False
        while not match_over:
            print(f"\n--- Turn {turn_number}: {'Your Turn' if player_turn else 'Computer Turn'} ---")

            if player_turn:
                # Player's turn
                while True:
                    prompt_msg = f"Enter a number to add (1-10) [Current: {shared_total}]: "
                    user_act = prompt_input(prompt_msg, color_scheme=color_scheme, allow_back=True, allow_quit=True)

                    if user_act == NavigationAction.QUIT:
                        return False
                    if user_act == NavigationAction.BACK:
                        return True

                    raw_val = str(user_act).strip()
                    try:
                        move = int(raw_val)
                    except ValueError:
                        print(style_text(f"'{raw_val}' is not a valid number. Please enter an integer from 1 to 10.", color_scheme, color_type="warning"))
                        continue

                    if not (MIN_ADD <= move <= MAX_ADD):
                        print(style_text(f"Number must be between {MIN_ADD} and {MAX_ADD}.", color_scheme, color_type="warning"))
                        continue

                    break

                shared_total += move
                print(style_text(f"\nYou added {move}! New total: {shared_total}", color_scheme, color_type="accent"))
                print(render_progress_bar(shared_total, TARGET_SCORE))

                if shared_total >= TARGET_SCORE:
                    print()
                    print(style_text("★ VICTORY! You reached 50 and won the match! ★", color_scheme, color_type="success", bold=True))
                    match_over = True
                    break

                player_turn = False

            else:
                # Computer's turn
                print("Computer is calculating its move...")
                comp_move = compute_computer_move(shared_total)
                shared_total += comp_move
                print(style_text(f"Computer chooses to add {comp_move}! New total: {shared_total}", color_scheme, color_type="warning"))
                print(render_progress_bar(shared_total, TARGET_SCORE))

                if shared_total >= TARGET_SCORE:
                    print()
                    print(style_text("✗ Computer reached 50 and won this match. Better luck next time!", color_scheme, color_type="error", bold=True))
                    match_over = True
                    break

                player_turn = True

            turn_number += 1

        print_divider(color_scheme)
        # Replay prompt
        replay_act = prompt_input("Play another match of First to Fifty? [y/n] (b=back, q=quit): ", color_scheme=color_scheme)
        if replay_act == NavigationAction.QUIT:
            return False
        if replay_act == NavigationAction.BACK:
            return True

        if str(replay_act).strip().lower() not in ("y", "yes"):
            print(style_text("\nThanks for playing First to Fifty!\n", color_scheme, color_type="accent"))
            return True

        clear_screen()
        print_header(title_style, color_scheme, subtitle="Game: First to Fifty")
