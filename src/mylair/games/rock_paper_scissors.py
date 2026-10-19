"""
Rock Paper Scissors Game for My Lair.

Rules:
- Rock crushes Scissors.
- Scissors cuts Paper.
- Paper covers Rock.

Accepts inputs:
- 'rock', 'paper', 'scissors'
- 'r', 'p', 's'
- 'b' to go back, 'q' to quit
"""

from __future__ import annotations

import random
from typing import Dict, Tuple

from mylair.display import (
    NavigationAction,
    clear_screen,
    print_divider,
    print_header,
    prompt_input,
    style_text,
)

# Friendly mapping of player input shortcuts to canonical choices
MOVE_ALIASES: Dict[str, str] = {
    "r": "rock",
    "rock": "rock",
    "p": "paper",
    "paper": "paper",
    "s": "scissors",
    "scissors": "scissors",
}

# Unicode / ASCII visual representations
MOVE_ICONS: Dict[str, str] = {
    "rock": "[ Rock ]",
    "paper": "[ Paper ]",
    "scissors": "[ Scissors ]",
}

# Outcome rules: (player_choice, computer_choice) -> result
OUTCOMES = {
    ("rock", "scissors"): ("crushes", True),
    ("scissors", "paper"): ("cuts", True),
    ("paper", "rock"): ("covers", True),
    ("scissors", "rock"): ("is crushed by", False),
    ("paper", "scissors"): ("is cut by", False),
    ("rock", "paper"): ("is covered by", False),
}


def evaluate_round(player_move: str, computer_move: str) -> Tuple[str, str]:
    """
    Determine the winner of a round.
    Returns (result_status, description), where result_status is 'win', 'lose', or 'tie'.
    """
    if player_move == computer_move:
        return "tie", f"Both chose {player_move.capitalize()}. It's a draw!"

    verb, won = OUTCOMES.get((player_move, computer_move), ("versus", False))
    if won:
        desc = f"{player_move.capitalize()} {verb} {computer_move.capitalize()}! You win this round!"
        return "win", desc
    else:
        desc = f"{computer_move.capitalize()} defeats {player_move.capitalize()}. Computer wins this round!"
        return "lose", desc


def play_rock_paper_scissors(
    title_style: str = "slant",
    color_scheme: str = "neon_cyan",
    direct_mode: bool = False,
) -> bool:
    """
    Run an interactive Rock Paper Scissors session.

    Parameters:
    - title_style: ASCII title style
    - color_scheme: Active color scheme
    - direct_mode: True if launched directly from CLI (e.g. `mylair -s rps`),
                   False if launched from the interactive menu.

    Returns:
    - True to return to menu / shell cleanly
    - False if user chose to quit the program
    """
    wins = 0
    losses = 0
    ties = 0

    clear_screen()
    print_header(title_style, color_scheme, subtitle="Game: Rock Paper Scissors")

    print(style_text("Welcome to Rock Paper Scissors!", color_scheme, color_type="accent", bold=True))
    print("Beat the computer in a classic duel of wits.\n")
    print("Controls:")
    print("  Enter 'r' or 'rock'     for Rock")
    print("  Enter 'p' or 'paper'    for Paper")
    print("  Enter 's' or 'scissors' for Scissors")
    print("  Enter 'b' to go back, 'q' to quit anytime.\n")
    print_divider(color_scheme)

    while True:
        # Display current tally if more than one round has been played
        total_rounds = wins + losses + ties
        if total_rounds > 0:
            tally_msg = f"Current Score: {wins} Win(s) | {losses} Loss(es) | {ties} Tie(s)"
            print(style_text(tally_msg, color_scheme, color_type="accent"))
            print_divider(color_scheme)

        # Prompt player for move
        prompt_label = "Your move [r/p/s] (b=back, q=quit): "
        action = prompt_input(prompt_label, color_scheme=color_scheme, allow_back=True, allow_quit=True)

        if action == NavigationAction.QUIT:
            return False  # Quit entire program
        if action == NavigationAction.BACK:
            return True   # Back to menu (or shell in direct mode)

        # Validate input
        move_key = str(action).strip().lower()
        if move_key not in MOVE_ALIASES:
            print(style_text(
                f"Invalid choice '{move_key}'. Please type 'rock' (r), 'paper' (p), or 'scissors' (s).",
                color_scheme,
                color_type="warning"
            ))
            print()
            continue

        player_choice = MOVE_ALIASES[move_key]
        computer_choice = random.choice(["rock", "paper", "scissors"])

        print()
        print(f"You chose:      {MOVE_ICONS[player_choice]} ({player_choice.capitalize()})")
        print(f"Computer chose: {MOVE_ICONS[computer_choice]} ({computer_choice.capitalize()})")
        print()

        status, explanation = evaluate_round(player_choice, computer_choice)

        if status == "win":
            wins += 1
            print(style_text(f"★ {explanation}", color_scheme, color_type="success", bold=True))
        elif status == "lose":
            losses += 1
            print(style_text(f"✗ {explanation}", color_scheme, color_type="error", bold=True))
        else:
            ties += 1
            print(style_text(f"═ {explanation}", color_scheme, color_type="warning", bold=True))

        print()
        print_divider(color_scheme)

        # Replay prompt
        replay_label = "Play another round? [y/n] (b=back, q=quit): "
        replay_action = prompt_input(replay_label, color_scheme=color_scheme, allow_back=True, allow_quit=True)

        if replay_action == NavigationAction.QUIT:
            return False
        if replay_action == NavigationAction.BACK:
            return True

        replay_str = str(replay_action).strip().lower()
        if replay_str not in ("y", "yes"):
            print(style_text("\nThanks for playing Rock Paper Scissors!", color_scheme, color_type="accent"))
            print(f"Final Score: {wins} Wins, {losses} Losses, {ties} Ties.\n")
            return True
        print()
