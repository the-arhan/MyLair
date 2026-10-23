"""
Dice Duel Game for My Lair.

Rules:
- You and the computer roll a pair of six-sided dice (2d6).
- The player with the highest combined total wins the round.
- Ties are handled explicitly as ties (no points awarded).
- Modes:
  1. Quick Duel: A single sudden-death roll.
  2. Best-of-3 Series: First player to win 2 rounds claims the championship.
  3. Best-of-5 Series: First player to win 3 rounds claims the championship.

Beginner Customization:
- You can change the number of sides on each die or dice count below.
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

DICE_MIN = 1
DICE_MAX = 6


def roll_dice() -> Tuple[int, int, int]:
    """
    Roll two standard 6-sided dice.
    Returns (die1, die2, total).
    """
    d1 = random.randint(DICE_MIN, DICE_MAX)
    d2 = random.randint(DICE_MIN, DICE_MAX)
    return d1, d2, d1 + d2


def compare_rolls(player_total: int, comp_total: int) -> str:
    """
    Compare totals.
    Returns 'player', 'computer', or 'tie'.
    """
    if player_total > comp_total:
        return "player"
    elif comp_total > player_total:
        return "computer"
    else:
        return "tie"


def format_dice_roll(d1: int, d2: int, total: int) -> str:
    """Format dice with a clean bracketed representation."""
    return f"[ {d1} ] + [ {d2} ] = {total}"


def play_dice_duel(
    title_style: str = "slant",
    color_scheme: str = "neon_cyan",
    direct_mode: bool = False,
) -> bool:
    """
    Run an interactive Dice Duel game session.

    Returns:
    - True to return to menu / shell cleanly
    - False if user chose to quit the program
    """
    clear_screen()
    print_header(title_style, color_scheme, subtitle="Game: Dice Duel")

    print(style_text("Welcome to Dice Duel!", color_scheme, color_type="accent", bold=True))
    print("Roll against the computer in a high-stakes battle of the dice.\n")
    print("Rules:")
    print("  1. Each player rolls two 6-sided dice (2d6).")
    print("  2. The higher roll total wins the round.")
    print("  3. Ties are handled cleanly as ties.")
    print("  4. Play a quick single round or a best-of tournament series!\n")
    print("Controls:")
    print("  Press Enter on your turn to cast your dice.")
    print("  Enter 'b' to go back, 'q' to quit anytime.\n")
    print_divider(color_scheme)

    while True:
        # Choose game mode
        print("Choose Game Mode:")
        print("  1. Quick Duel     (Single round)")
        print("  2. Best-of-3      (First to 2 wins)")
        print("  3. Best-of-5      (First to 3 wins)")

        while True:
            mode_act = prompt_input("Select mode [1-3] (b=back, q=quit): ", color_scheme=color_scheme, allow_back=True, allow_quit=True)
            if mode_act == NavigationAction.QUIT:
                return False
            if mode_act == NavigationAction.BACK:
                return True

            mode_str = str(mode_act).strip()
            if mode_str in ("1", "2", "3"):
                break
            print(style_text("Please enter 1, 2, or 3.", color_scheme, color_type="warning"))

        target_wins = 1 if mode_str == "1" else (2 if mode_str == "2" else 3)
        player_score = 0
        comp_score = 0
        tie_count = 0
        round_num = 1

        print_divider(color_scheme)
        if target_wins == 1:
            print(style_text("Quick Duel match initiated! Ready your dice.", color_scheme, color_type="accent"))
        else:
            print(style_text(f"Series started! First to {target_wins} win(s) takes the cup.", color_scheme, color_type="accent"))
        print()

        while True:
            if target_wins > 1:
                print(f"--- Round {round_num} (Score: You {player_score} - {comp_score} Computer) ---")
            else:
                print(f"--- Sudden Death Round ---")

            # Prompt to roll
            roll_act = prompt_input("Press Enter to roll your dice (b=back, q=quit): ", color_scheme=color_scheme, allow_back=True, allow_quit=True)
            if roll_act == NavigationAction.QUIT:
                return False
            if roll_act == NavigationAction.BACK:
                return True

            p1, p2, p_total = roll_dice()
            c1, c2, c_total = roll_dice()

            print()
            print(f"You rolled:        🎲 {format_dice_roll(p1, p2, p_total)}")
            print(f"Computer rolled:   🎲 {format_dice_roll(c1, c2, c_total)}")
            print()

            round_winner = compare_rolls(p_total, c_total)

            if round_winner == "player":
                player_score += 1
                print(style_text(f"★ You win round {round_num}! ({p_total} vs {c_total})", color_scheme, color_type="success", bold=True))
            elif round_winner == "computer":
                comp_score += 1
                print(style_text(f"✗ Computer wins round {round_num}! ({c_total} vs {p_total})", color_scheme, color_type="error", bold=True))
            else:
                tie_count += 1
                print(style_text(f"═ It's a TIE! Both rolled {p_total}.", color_scheme, color_type="warning", bold=True))

            print()

            # Check if series is decided
            if player_score >= target_wins:
                print_divider(color_scheme)
                print(style_text("🏆 VICTORY! You won the Dice Duel Series! 🏆", color_scheme, color_type="success", bold=True))
                print(f"Final Score: You {player_score} - {comp_score} Computer (Ties: {tie_count})\n")
                break
            elif comp_score >= target_wins:
                print_divider(color_scheme)
                print(style_text("☠ DEFEAT! The computer claimed the series.", color_scheme, color_type="error", bold=True))
                print(f"Final Score: You {player_score} - {comp_score} Computer (Ties: {tie_count})\n")
                break

            round_num += 1

        print_divider(color_scheme)

        # Replay prompt
        replay_prompt = "Play another match of Dice Duel? [y/n] (b=back, q=quit): "
        replay_act = prompt_input(replay_prompt, color_scheme=color_scheme, allow_back=True, allow_quit=True)

        if replay_act == NavigationAction.QUIT:
            return False
        if replay_act == NavigationAction.BACK:
            return True

        if str(replay_act).strip().lower() not in ("y", "yes"):
            print(style_text("\nThanks for playing Dice Duel!\n", color_scheme, color_type="accent"))
            return True

        clear_screen()
        print_header(title_style, color_scheme, subtitle="Game: Dice Duel")
