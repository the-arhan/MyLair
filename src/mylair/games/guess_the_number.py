"""
Guess the Number Game for My Lair.

Rules:
- The computer secretly picks a whole number between 1 and 100.
- Guess the number! After each guess, you will get feedback:
  - "Too high!"
  - "Too low!"
  - "Correct!"
- The computer also keeps track of the narrowed range to help you narrow down your search.
- Try to find the secret number in as few guesses as possible!

Controls:
- Enter your guess as a number between 1 and 100.
- Enter 'b' to go back, 'q' to quit anytime.
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

LOWER_BOUND = 1
UPPER_BOUND = 100


def get_guess_rating(attempts: int) -> str:
    """Return a playful rating based on the number of attempts."""
    if attempts <= 4:
        return "Legendary Intuition! (Binary search master)"
    elif attempts <= 7:
        return "Excellent! (Optimal strategy)"
    elif attempts <= 10:
        return "Good job! You figured it out."
    else:
        return "Persistence pays off! Practice will make you faster."


def play_guess_the_number(
    title_style: str = "slant",
    color_scheme: str = "neon_cyan",
    direct_mode: bool = False,
) -> bool:
    """
    Run an interactive Guess the Number game session.

    Returns:
    - True to return to menu / shell cleanly
    - False if user chose to quit the program
    """
    clear_screen()
    print_header(title_style, color_scheme, subtitle="Game: Guess the Number")

    print(style_text("Welcome to Guess the Number!", color_scheme, color_type="accent", bold=True))
    print(f"The computer has selected a mystery number between {LOWER_BOUND} and {UPPER_BOUND}.\n")
    print("Controls:")
    print("  Type your guess as an integer (e.g. 50).")
    print("  Enter 'b' to go back, 'q' to quit anytime.\n")
    print_divider(color_scheme)

    while True:
        secret_number = random.randint(LOWER_BOUND, UPPER_BOUND)
        current_min = LOWER_BOUND
        current_max = UPPER_BOUND
        attempts = 0

        print(style_text(f"New round started! Secret number chosen between {LOWER_BOUND} and {UPPER_BOUND}.", color_scheme, color_type="accent"))

        while True:
            # Show current narrowed bounds
            range_hint = f"Hint: Number is between {current_min} and {current_max} (Guess #{attempts + 1})"
            print(style_text(range_hint, color_scheme, color_type="text"))

            action = prompt_input("Enter your guess: ", color_scheme=color_scheme, allow_back=True, allow_quit=True)

            if action == NavigationAction.QUIT:
                return False
            if action == NavigationAction.BACK:
                return True

            raw_str = str(action).strip()
            try:
                guess = int(raw_str)
            except ValueError:
                print(style_text(f"'{raw_str}' is not a valid number. Please enter a whole number.", color_scheme, color_type="warning"))
                print()
                continue

            if not (LOWER_BOUND <= guess <= UPPER_BOUND):
                print(style_text(f"Your guess must be between {LOWER_BOUND} and {UPPER_BOUND}.", color_scheme, color_type="warning"))
                print()
                continue

            attempts += 1

            if guess == secret_number:
                print()
                print(style_text(f"★ BINGO! {guess} is the correct number! ★", color_scheme, color_type="success", bold=True))
                print(f"You cracked the code in {attempts} guess(es)!")
                rating = get_guess_rating(attempts)
                print(style_text(f"Rating: {rating}", color_scheme, color_type="accent"))
                print()
                break
            elif guess < secret_number:
                print(style_text(f"▲ {guess} is TOO LOW!", color_scheme, color_type="warning"))
                if guess >= current_min:
                    current_min = guess + 1
                print()
            else:
                print(style_text(f"▼ {guess} is TOO HIGH!", color_scheme, color_type="warning"))
                if guess <= current_max:
                    current_max = guess - 1
                print()

        print_divider(color_scheme)
        replay_act = prompt_input("Play again with a new number? [y/n] (b=back, q=quit): ", color_scheme=color_scheme)
        if replay_act == NavigationAction.QUIT:
            return False
        if replay_act == NavigationAction.BACK:
            return True

        if str(replay_act).strip().lower() not in ("y", "yes"):
            print(style_text("\nThanks for playing Guess the Number!\n", color_scheme, color_type="accent"))
            return True

        clear_screen()
        print_header(title_style, color_scheme, subtitle="Game: Guess the Number")
