"""
Higher or Lower Game for My Lair.

Rules:
- A starting number (1-50) is revealed.
- Predict whether the NEXT number will be HIGHER or LOWER.
- Reveal the next number and award points for correct predictions.
- EQUAL RULE: If the next number equals the current number, it's a PUSH (tie) —
  your streak and round continue without penalty!
- Rounds are quick (5 predictions per game). Try to achieve a perfect 5/5 score!

Beginner Customization:
- Change the number range via MIN_VALUE and MAX_VALUE, or ROUND_LENGTH below.
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

MIN_VALUE = 1
MAX_VALUE = 50
ROUND_LENGTH = 5

CHOICE_ALIASES = {
    "h": "higher",
    "high": "higher",
    "higher": "higher",
    "l": "lower",
    "low": "lower",
    "lower": "lower",
}


def compare_numbers(
    current_val: int,
    next_val: int,
    prediction: str,
) -> Tuple[str, str]:
    """
    Compare next_val against current_val given prediction ('higher' or 'lower').

    Returns:
    - (outcome_status, message)
      outcome_status is one of: 'win', 'lose', 'push'
    """
    if next_val == current_val:
        return "push", f"Both numbers are {current_val}! It's a PUSH (tie) — no penalty."

    if prediction == "higher":
        if next_val > current_val:
            return "win", f"{next_val} is HIGHER than {current_val}! Correct!"
        else:
            return "lose", f"{next_val} is LOWER than {current_val}. Incorrect."
    else:  # prediction == "lower"
        if next_val < current_val:
            return "win", f"{next_val} is LOWER than {current_val}! Correct!"
        else:
            return "lose", f"{next_val} is HIGHER than {current_val}. Incorrect."


def play_higher_or_lower(
    title_style: str = "slant",
    color_scheme: str = "neon_cyan",
    direct_mode: bool = False,
) -> bool:
    """
    Run an interactive Higher or Lower game session.

    Returns:
    - True to return to menu / shell cleanly
    - False if user chose to quit the program
    """
    clear_screen()
    print_header(title_style, color_scheme, subtitle="Game: Higher or Lower")

    print(style_text("Welcome to Higher or Lower!", color_scheme, color_type="accent", bold=True))
    print(f"Predict whether the next mystery number ({MIN_VALUE}-{MAX_VALUE}) will be Higher or Lower.\n")
    print("Rules:")
    print(f"  1. Each game consists of a short {ROUND_LENGTH}-round prediction run.")
    print("  2. If you predict correctly, you score 1 point.")
    print("  3. EQUAL RULE: If the next number is identical to the current number,")
    print("     it counts as a PUSH (tie) — your score is preserved with no penalty!")
    print("Controls:")
    print("  Enter 'h' or 'higher' for Higher, 'l' or 'lower' for Lower.")
    print("  Enter 'b' to go back, 'q' to quit anytime.\n")
    print_divider(color_scheme)

    while True:
        score = 0
        current_num = random.randint(MIN_VALUE, MAX_VALUE)

        print(style_text(f"Starting new round of {ROUND_LENGTH} turns! Starting number is [ {current_num} ].", color_scheme, color_type="accent"))
        print()

        for turn in range(1, ROUND_LENGTH + 1):
            print(f"--- Turn {turn} of {ROUND_LENGTH} ---")
            print(f"Current Number: [ {current_num} ]")

            while True:
                prompt_msg = "Will the next number be (H)igher or (L)ower? [h/l] (b=back, q=quit): "
                act = prompt_input(prompt_msg, color_scheme=color_scheme, allow_back=True, allow_quit=True)

                if act == NavigationAction.QUIT:
                    return False
                if act == NavigationAction.BACK:
                    return True

                raw_choice = str(act).strip().lower()
                if raw_choice in CHOICE_ALIASES:
                    prediction = CHOICE_ALIASES[raw_choice]
                    break
                print(style_text("Invalid choice. Please enter 'h' (Higher) or 'l' (Lower).", color_scheme, color_type="warning"))

            next_num = random.randint(MIN_VALUE, MAX_VALUE)
            status, explanation = compare_numbers(current_num, next_num, prediction)

            print()
            print(f"Revealed Number: [ {next_num} ]")

            if status == "win":
                score += 1
                print(style_text(f"★ {explanation}", color_scheme, color_type="success", bold=True))
            elif status == "lose":
                print(style_text(f"✗ {explanation}", color_scheme, color_type="error", bold=True))
            else:  # push
                print(style_text(f"═ {explanation}", color_scheme, color_type="warning", bold=True))

            current_num = next_num
            print(f"Current Score: {score}/{turn}")
            print()

        # End of round summary
        print_divider(color_scheme)
        print(style_text(f"Game Complete! Final Score: {score} out of {ROUND_LENGTH} correct.", color_scheme, color_type="accent", bold=True))
        if score == ROUND_LENGTH:
            print(style_text("★ PERFECT SCORE! Incredible intuition! ★", color_scheme, color_type="success", bold=True))
        elif score >= ROUND_LENGTH * 0.6:
            print(style_text("Great job! Solid forecasting skills.", color_scheme, color_type="accent"))
        else:
            print("Good effort! Better luck on the next run.")

        print_divider(color_scheme)

        # Replay prompt
        replay_prompt = "Play another game of Higher or Lower? [y/n] (b=back, q=quit): "
        replay_act = prompt_input(replay_prompt, color_scheme=color_scheme, allow_back=True, allow_quit=True)

        if replay_act == NavigationAction.QUIT:
            return False
        if replay_act == NavigationAction.BACK:
            return True

        if str(replay_act).strip().lower() not in ("y", "yes"):
            print(style_text("\nThanks for playing Higher or Lower!\n", color_scheme, color_type="accent"))
            return True

        clear_screen()
        print_header(title_style, color_scheme, subtitle="Game: Higher or Lower")
