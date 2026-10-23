"""
Rock Paper Scissors Plus (RPSLS) Game for My Lair.

Rules (Rock, Paper, Scissors, Lizard, Spock):
- Scissors cuts Paper
- Paper covers Rock
- Rock crushes Lizard
- Lizard poisons Spock
- Spock smashes Scissors
- Scissors decapitates Lizard
- Lizard eats Paper
- Paper disproves Spock
- Spock vaporizes Rock
- Rock crushes Scissors

Accepts inputs:
- 'rock' ('r'), 'paper' ('p'), 'scissors' ('s' / 'sc')
- 'lizard' ('l' / 'liz'), 'spock' ('k' / 'sp')
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
    "sc": "scissors",
    "l": "lizard",
    "lizard": "lizard",
    "liz": "lizard",
    "k": "spock",
    "spock": "spock",
    "sp": "spock",
}

# Visual icons / representations
MOVE_ICONS: Dict[str, str] = {
    "rock": "[ 🪨 Rock ]",
    "paper": "[ 📄 Paper ]",
    "scissors": "[ ✂️ Scissors ]",
    "lizard": "[ 🦎 Lizard ]",
    "spock": "[ 🖖 Spock ]",
}

# Outcome rules: (player_choice, computer_choice) -> (verb, player_won_boolean)
OUTCOMES = {
    # Rock
    ("rock", "scissors"): ("crushes", True),
    ("rock", "lizard"): ("crushes", True),
    ("rock", "paper"): ("is covered by", False),
    ("rock", "spock"): ("is vaporized by", False),
    # Paper
    ("paper", "rock"): ("covers", True),
    ("paper", "spock"): ("disproves", True),
    ("paper", "scissors"): ("is cut by", False),
    ("paper", "lizard"): ("is eaten by", False),
    # Scissors
    ("scissors", "paper"): ("cuts", True),
    ("scissors", "lizard"): ("decapitates", True),
    ("scissors", "rock"): ("is crushed by", False),
    ("scissors", "spock"): ("is smashed by", False),
    # Lizard
    ("lizard", "spock"): ("poisons", True),
    ("lizard", "paper"): ("eats", True),
    ("lizard", "rock"): ("is crushed by", False),
    ("lizard", "scissors"): ("is decapitated by", False),
    # Spock
    ("spock", "scissors"): ("smashes", True),
    ("spock", "rock"): ("vaporizes", True),
    ("spock", "paper"): ("is disproved by", False),
    ("spock", "lizard"): ("is poisoned by", False),
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
        desc = f"{computer_move.capitalize()} defeats {player_move.capitalize()} ({player_move.capitalize()} {verb} {computer_move.capitalize()}). Computer wins this round!"
        return "lose", desc


def play_rock_paper_scissors_plus(
    title_style: str = "slant",
    color_scheme: str = "neon_cyan",
    direct_mode: bool = False,
) -> bool:
    """
    Run an interactive Rock Paper Scissors Plus session.

    Returns:
    - True to return to menu / shell cleanly
    - False if user chose to quit the program
    """
    wins = 0
    losses = 0
    ties = 0

    clear_screen()
    print_header(title_style, color_scheme, subtitle="Game: Rock Paper Scissors Plus")

    print(style_text("Welcome to Rock Paper Scissors Plus!", color_scheme, color_type="accent", bold=True))
    print("The classic expanded 5-way battle of Rock, Paper, Scissors, Lizard, Spock.\n")
    print("Rules at a glance:")
    print("  • Rock crushes Scissors & crushes Lizard")
    print("  • Paper covers Rock & disproves Spock")
    print("  • Scissors cuts Paper & decapitates Lizard")
    print("  • Lizard poisons Spock & eats Paper")
    print("  • Spock smashes Scissors & vaporizes Rock\n")
    print("Controls:")
    print("  Enter 'r' for Rock     | 'p' for Paper | 's' for Scissors")
    print("  Enter 'l' for Lizard   | 'k' (or 'sp') for Spock")
    print("  Enter 'b' to go back, 'q' to quit anytime.\n")
    print_divider(color_scheme)

    all_moves = ["rock", "paper", "scissors", "lizard", "spock"]

    while True:
        total_rounds = wins + losses + ties
        if total_rounds > 0:
            tally_msg = f"Current Score: {wins} Win(s) | {losses} Loss(es) | {ties} Tie(s)"
            print(style_text(tally_msg, color_scheme, color_type="accent"))
            print_divider(color_scheme)

        # Prompt player for move
        prompt_label = "Your move [r/p/s/l/k] (b=back, q=quit): "
        action = prompt_input(prompt_label, color_scheme=color_scheme, allow_back=True, allow_quit=True)

        if action == NavigationAction.QUIT:
            return False
        if action == NavigationAction.BACK:
            return True

        # Validate input with forgiving aliases
        move_key = str(action).strip().lower()
        if move_key not in MOVE_ALIASES:
            print(style_text(
                f"Invalid choice '{move_key}'. Options: rock (r), paper (p), scissors (s), lizard (l), spock (k).",
                color_scheme,
                color_type="warning",
            ))
            print()
            continue

        player_choice = MOVE_ALIASES[move_key]
        computer_choice = random.choice(all_moves)

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
            print(style_text("\nThanks for playing Rock Paper Scissors Plus!", color_scheme, color_type="accent"))
            print(f"Final Score: {wins} Wins, {losses} Losses, {ties} Ties.\n")
            return True

        print()


# Friendly alias for backward compatibility
play_rock_paper_scissors = play_rock_paper_scissors_plus
