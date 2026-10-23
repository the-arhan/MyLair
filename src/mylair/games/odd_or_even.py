"""
Odd or Even Game for My Lair.

Rules:
- The player predicts the PARITY (Odd or Even) of the combined sum of two numbers.
- Step 1: Predict whether the final sum will be ODD or EVEN.
- Step 2: Choose your number between 1 and 5.
- Step 3: The computer also chooses a number between 1 and 5.
- The two numbers are added together:
  If (Your Number + Computer Number) matches your chosen parity, YOU WIN!
  Otherwise, the computer wins.

Beginner Customization:
- You can change the number range (e.g. 1 to 10) by modifying MIN_NUMBER and MAX_NUMBER below.
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

# Number selection range for both player and computer
MIN_NUMBER = 1
MAX_NUMBER = 5

PARITY_ALIASES = {
    "o": "odd",
    "odd": "odd",
    "e": "even",
    "even": "even",
}


def evaluate_odd_or_even(
    player_parity: str,
    player_num: int,
    computer_num: int,
) -> Tuple[bool, int, str]:
    """
    Evaluate the result of an Odd or Even round.

    Returns:
    - (player_won, total_sum, parity_name)
    """
    total = player_num + computer_num
    actual_parity = "even" if total % 2 == 0 else "odd"
    player_won = (player_parity.lower() == actual_parity)
    return player_won, total, actual_parity


def play_odd_or_even(
    title_style: str = "slant",
    color_scheme: str = "neon_cyan",
    direct_mode: bool = False,
) -> bool:
    """
    Run an interactive session of Odd or Even.

    Returns:
    - True to return to menu / shell cleanly
    - False if user chose to quit the program
    """
    wins = 0
    losses = 0

    clear_screen()
    print_header(title_style, color_scheme, subtitle="Game: Odd or Even")

    print(style_text("Welcome to Odd or Even!", color_scheme, color_type="accent", bold=True))
    print("A classic duel of prediction and numbers against the computer.\n")
    print("How to play:")
    print("  1. Predict whether the COMBINED SUM will be ODD (o) or EVEN (e).")
    print(f"  2. Pick your number from {MIN_NUMBER} to {MAX_NUMBER}.")
    print(f"  3. The computer also picks a number from {MIN_NUMBER} to {MAX_NUMBER}.")
    print("  4. If the sum's parity matches your call, YOU WIN!\n")
    print("Controls:")
    print("  Enter 'o' / 'odd' or 'e' / 'even' for parity prediction.")
    print(f"  Enter an integer from {MIN_NUMBER} to {MAX_NUMBER} for your number.")
    print("  Enter 'b' to go back, 'q' to quit anytime.\n")
    print_divider(color_scheme)

    while True:
        total_rounds = wins + losses
        if total_rounds > 0:
            score_msg = f"Current Score: {wins} Win(s) | {losses} Loss(es)"
            print(style_text(score_msg, color_scheme, color_type="accent"))
            print_divider(color_scheme)

        # Step 1: Predict parity
        while True:
            parity_prompt = "Predict total parity [o=odd / e=even] (b=back, q=quit): "
            act = prompt_input(parity_prompt, color_scheme=color_scheme, allow_back=True, allow_quit=True)

            if act == NavigationAction.QUIT:
                return False
            if act == NavigationAction.BACK:
                return True

            raw_parity = str(act).strip().lower()
            if raw_parity in PARITY_ALIASES:
                chosen_parity = PARITY_ALIASES[raw_parity]
                break
            print(style_text("Invalid parity choice. Please enter 'o' for Odd or 'e' for Even.", color_scheme, color_type="warning"))

        # Step 2: Choose player's number
        while True:
            num_prompt = f"Choose your number ({MIN_NUMBER}-{MAX_NUMBER}) (b=back, q=quit): "
            act = prompt_input(num_prompt, color_scheme=color_scheme, allow_back=True, allow_quit=True)

            if act == NavigationAction.QUIT:
                return False
            if act == NavigationAction.BACK:
                return True

            raw_num = str(act).strip()
            try:
                player_num = int(raw_num)
                if MIN_NUMBER <= player_num <= MAX_NUMBER:
                    break
                print(style_text(f"Please enter an integer between {MIN_NUMBER} and {MAX_NUMBER}.", color_scheme, color_type="warning"))
            except ValueError:
                print(style_text(f"'{raw_num}' is not a valid number.", color_scheme, color_type="warning"))

        # Step 3: Computer chooses number
        computer_num = random.randint(MIN_NUMBER, MAX_NUMBER)

        # Evaluate round
        won, total, actual_parity = evaluate_odd_or_even(chosen_parity, player_num, computer_num)

        print()
        print(f"Your prediction:      {chosen_parity.upper()}")
        print(f"Your number:          {player_num}")
        print(f"Computer's number:    {computer_num}")
        print(f"Sum:                  {player_num} + {computer_num} = {total} ({actual_parity.upper()})")
        print()

        if won:
            wins += 1
            win_msg = f"★ Correct! {total} is {actual_parity.upper()} — You win this round! ★"
            print(style_text(win_msg, color_scheme, color_type="success", bold=True))
        else:
            losses += 1
            lose_msg = f"✗ {total} is {actual_parity.upper()}, but you predicted {chosen_parity.upper()}. Computer wins."
            print(style_text(lose_msg, color_scheme, color_type="error", bold=True))

        print()
        print_divider(color_scheme)

        # Replay prompt
        replay_prompt = "Play another round? [y/n] (b=back, q=quit): "
        replay_act = prompt_input(replay_prompt, color_scheme=color_scheme, allow_back=True, allow_quit=True)

        if replay_act == NavigationAction.QUIT:
            return False
        if replay_act == NavigationAction.BACK:
            return True

        if str(replay_act).strip().lower() not in ("y", "yes"):
            print(style_text("\nThanks for playing Odd or Even!", color_scheme, color_type="accent"))
            print(f"Final Score: {wins} Wins, {losses} Losses.\n")
            return True

        print()
