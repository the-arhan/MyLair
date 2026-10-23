"""
The 8 Ball Game for My Lair.

Rules:
- Think of a yes/no question and ask the mysterious Mystic 8 Ball.
- The 8 Ball simulates a brief mystical roll.
- One of eight classic answers is revealed at random:
  1. It is certain
  2. It is decidedly so
  3. Without a doubt
  4. Reply hazy, try again
  5. Ask again later
  6. Better not tell you now
  7. My sources say no
  8. Outlook not so good
- Treat the responses as lighthearted, playful entertainment.

Beginner Customization:
- The 8 answers are defined in EIGHT_BALL_ANSWERS below.
"""

from __future__ import annotations

import random
import sys
import time
from typing import List

from mylair.display import (
    NavigationAction,
    clear_screen,
    print_divider,
    print_header,
    prompt_input,
    style_text,
    supports_color,
)

EIGHT_BALL_ANSWERS: List[str] = [
    "It is certain",
    "It is decidedly so",
    "Without a doubt",
    "Reply hazy, try again",
    "Ask again later",
    "Better not tell you now",
    "My sources say no",
    "Outlook not so good",
]


def shake_8_ball_effect(color_scheme: str = "synthwave") -> None:
    """
    Simulate a brief, terminal-friendly 8-ball shake.
    Keeps duration very short (~0.6s) and safely handles interrupts.
    """
    frames = [
        "Concentrating on the cosmos .  ",
        "Concentrating on the cosmos .. ",
        "Concentrating on the cosmos ...",
        "The mystical triangle rises ...",
    ]
    try:
        for frame in frames:
            sys.stdout.write("\r" + style_text(f"  🎱 {frame}", color_scheme, color_type="accent"))
            sys.stdout.flush()
            time.sleep(0.2)
        sys.stdout.write("\r" + " " * 50 + "\r")
        sys.stdout.flush()
    except (KeyboardInterrupt, Exception):
        sys.stdout.write("\r" + " " * 50 + "\r")
        sys.stdout.flush()


def render_8_ball_art(answer: str) -> str:
    """Render the ASCII 8-ball with the answer centered in the window."""
    padded_answer = f" {answer.upper()} ".center(26)
    return (
        "             .------------------.            \n"
        "          .-'      .------.      '-.         \n"
        "        .'       .'   (8)  '.       '.       \n"
        "       /        /            \\        \\      \n"
        "      |        |  .--------.  |        |     \n"
        f"      |        | {padded_answer} |        |     \n"
        "      |        |  '--------'  |        |     \n"
        "       \\        \\            /        /      \n"
        "        '.       '.        .'       .'       \n"
        "          '-.      '------'      .-'         \n"
        "             '------------------'            "
    )


def play_the_8_ball(
    title_style: str = "slant",
    color_scheme: str = "neon_cyan",
    direct_mode: bool = False,
) -> bool:
    """
    Run an interactive 8 Ball session.

    Returns:
    - True to return to menu / shell cleanly
    - False if user chose to quit the program
    """
    clear_screen()
    print_header(title_style, color_scheme, subtitle="Game: The 8 Ball")

    print(style_text("Welcome to The Mystic 8 Ball!", color_scheme, color_type="accent", bold=True))
    print("Consult the oracle of the terminal for playful answers to your queries.\n")
    print("Note:")
    print("  The 8 Ball is purely for fun and lighthearted entertainment!")
    print("Controls:")
    print("  Type any question and press Enter.")
    print("  Enter 'b' to go back, 'q' to quit anytime.\n")
    print_divider(color_scheme)

    while True:
        prompt_label = "Ask your question (or 'b' to go back, 'q' to quit): "
        act = prompt_input(prompt_label, color_scheme=color_scheme, allow_back=True, allow_quit=True)

        if act == NavigationAction.QUIT:
            return False
        if act == NavigationAction.BACK:
            return True

        question_text = str(act).strip()
        if not question_text:
            print(style_text("Please ask a question first!", color_scheme, color_type="warning"))
            continue

        print()
        shake_8_ball_effect(color_scheme)

        chosen_answer = random.choice(EIGHT_BALL_ANSWERS)

        print(render_8_ball_art(chosen_answer))
        print()
        print_divider(color_scheme)
        print(f"Your Question: \"{question_text}\"")
        print(style_text(f"The 8 Ball Answers: \"{chosen_answer}\"", color_scheme, color_type="accent", bold=True))
        print_divider(color_scheme)

        # Replay prompt
        replay_prompt = "Consult the 8 Ball again? [y/n] (b=back, q=quit): "
        replay_act = prompt_input(replay_prompt, color_scheme=color_scheme, allow_back=True, allow_quit=True)

        if replay_act == NavigationAction.QUIT:
            return False
        if replay_act == NavigationAction.BACK:
            return True

        if str(replay_act).strip().lower() not in ("y", "yes"):
            print(style_text("\nThe 8 Ball rests. May fortune favor your path!\n", color_scheme, color_type="accent"))
            return True

        print()
