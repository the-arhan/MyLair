"""
Coin Flip Streak Game for My Lair.

Rules:
- Predict whether the coin will land on HEADS or TAILS.
- Each correct prediction increases your current streak by 1.
- After each successful flip, you can CONTINUE to build the streak or STOP to bank it!
- WHAT ENDS THE STREAK: Any incorrect prediction immediately resets your current streak to 0!
- The session tracks your all-time Best Streak.

Beginner Customization:
- Custom coin sides or messages can be edited below in FLIP_OPTIONS.
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

FLIP_ALIASES = {
    "h": "heads",
    "head": "heads",
    "heads": "heads",
    "t": "tails",
    "tail": "tails",
    "tails": "tails",
}


def flip_coin() -> str:
    """Return 'heads' or 'tails' with equal probability."""
    return random.choice(["heads", "tails"])


def evaluate_flip(player_call: str, flip_result: str) -> bool:
    """Return True if player's prediction matches the coin flip."""
    return player_call.lower() == flip_result.lower()


def play_coin_flip_streak(
    title_style: str = "slant",
    color_scheme: str = "neon_cyan",
    direct_mode: bool = False,
) -> bool:
    """
    Run an interactive Coin Flip Streak session.

    Returns:
    - True to return to menu / shell cleanly
    - False if user chose to quit the program
    """
    current_streak = 0
    best_streak = 0

    clear_screen()
    print_header(title_style, color_scheme, subtitle="Game: Coin Flip Streak")

    print(style_text("Welcome to Coin Flip Streak!", color_scheme, color_type="accent", bold=True))
    print("Test your luck and build the longest winning streak.\n")
    print("Rules:")
    print("  1. Predict Heads (h) or Tails (t) for each coin toss.")
    print("  2. Every correct call increases your Current Streak by 1.")
    print("  3. After a win, choose whether to CONTINUE risking or STOP to bank your score.")
    print("  4. WHAT ENDS THE STREAK: Any wrong call immediately resets your streak to 0!\n")
    print("Controls:")
    print("  Enter 'h' or 'heads' for Heads, 't' or 'tails' for Tails.")
    print("  Enter 'c' to continue, 's' to stop and bank.")
    print("  Enter 'b' to go back, 'q' to quit anytime.\n")
    print_divider(color_scheme)

    while True:
        # Status header
        status_line = f"Current Streak: {current_streak}  |  Best Streak: {best_streak}"
        print(style_text(status_line, color_scheme, color_type="accent", bold=True))
        print_divider(color_scheme)

        # Prompt for flip prediction
        while True:
            call_prompt = "Call the flip [h=heads / t=tails] (b=back, q=quit): "
            act = prompt_input(call_prompt, color_scheme=color_scheme, allow_back=True, allow_quit=True)

            if act == NavigationAction.QUIT:
                return False
            if act == NavigationAction.BACK:
                return True

            raw_call = str(act).strip().lower()
            if raw_call in FLIP_ALIASES:
                player_call = FLIP_ALIASES[raw_call]
                break
            print(style_text("Invalid call. Please enter 'h' (Heads) or 't' (Tails).", color_scheme, color_type="warning"))

        # Flip the coin
        result = flip_coin()
        is_winner = evaluate_flip(player_call, result)

        print()
        print(f"You called:   {player_call.capitalize()}")
        print(f"Coin landed:  🪙  {result.upper()}!")
        print()

        if is_winner:
            current_streak += 1
            if current_streak > best_streak:
                best_streak = current_streak
                new_best_note = " (★ NEW SESSION RECORD! ★)"
            else:
                new_best_note = ""

            win_msg = f"★ Correct! Your streak is now {current_streak}!{new_best_note}"
            print(style_text(win_msg, color_scheme, color_type="success", bold=True))
            print_divider(color_scheme)

            # Let the player choose to continue or stop
            while True:
                decision_prompt = f"Streak is {current_streak}. [C]ontinue flipping or [S]top and bank? (b=back, q=quit): "
                dec_act = prompt_input(decision_prompt, color_scheme=color_scheme, allow_back=True, allow_quit=True)

                if dec_act == NavigationAction.QUIT:
                    return False
                if dec_act == NavigationAction.BACK:
                    return True

                dec_str = str(dec_act).strip().lower()
                if dec_str in ("c", "continue"):
                    print()
                    break
                elif dec_str in ("s", "stop", "bank"):
                    print()
                    bank_msg = f"🏆 Banked! You secured a streak of {current_streak}!"
                    print(style_text(bank_msg, color_scheme, color_type="accent", bold=True))
                    print(f"Session Best Streak: {best_streak}\n")
                    current_streak = 0

                    # Ask if they want to start a new streak run
                    replay_prompt = "Start a fresh streak run? [y/n] (b=back, q=quit): "
                    replay_act = prompt_input(replay_prompt, color_scheme=color_scheme, allow_back=True, allow_quit=True)
                    if replay_act == NavigationAction.QUIT:
                        return False
                    if replay_act == NavigationAction.BACK:
                        return True
                    if str(replay_act).strip().lower() not in ("y", "yes"):
                        print(style_text("\nThanks for playing Coin Flip Streak!", color_scheme, color_type="accent"))
                        print(f"Final Best Streak: {best_streak}\n")
                        return True
                    print()
                    break
                else:
                    print(style_text("Please enter 'c' to continue or 's' to stop.", color_scheme, color_type="warning"))

        else:
            lost_streak = current_streak
            current_streak = 0
            lose_msg = f"✗ Wrong call! That ends your streak of {lost_streak}."
            print(style_text(lose_msg, color_scheme, color_type="error", bold=True))
            print(f"Session Best Streak: {best_streak}")
            print_divider(color_scheme)

            # Replay prompt
            replay_prompt = "Try for a new streak? [y/n] (b=back, q=quit): "
            replay_act = prompt_input(replay_prompt, color_scheme=color_scheme, allow_back=True, allow_quit=True)

            if replay_act == NavigationAction.QUIT:
                return False
            if replay_act == NavigationAction.BACK:
                return True

            if str(replay_act).strip().lower() not in ("y", "yes"):
                print(style_text("\nThanks for playing Coin Flip Streak!", color_scheme, color_type="accent"))
                print(f"Final Best Streak: {best_streak}\n")
                return True

            print()
