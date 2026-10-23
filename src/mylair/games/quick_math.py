"""
Quick Math Game for My Lair.

Rules:
- Solve short arithmetic questions under a casual turn-limit format.
- Select your preferred difficulty:
  1. Easy:   Simple addition and subtraction (numbers 1-20).
  2. Medium: Addition and subtraction up to 50, plus single-digit multiplication (2-9).
  3. Hard:   Mixed addition, subtraction (up to 100), and multiplication (up to 12x12).
- Tracks correct answers and total attempts per round.
- Turn limit: 5 questions per round.

Beginner Customization:
- Questions per round and number ranges can be easily adjusted via QUESTIONS_PER_ROUND below.
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

QUESTIONS_PER_ROUND = 5


def generate_question(difficulty: int = 1) -> Tuple[str, int]:
    """
    Generate an arithmetic problem based on difficulty level.

    Returns:
    - (question_text, correct_answer)
    """
    if difficulty == 1:
        # Easy: addition and subtraction with positive results
        op = random.choice(["+", "-"])
        if op == "+":
            a = random.randint(1, 20)
            b = random.randint(1, 20)
            return f"{a} + {b}", a + b
        else:
            a = random.randint(5, 25)
            b = random.randint(1, a)  # ensure non-negative result
            return f"{a} - {b}", a - b

    elif difficulty == 2:
        # Medium: addition, subtraction, simple multiplication
        op = random.choice(["+", "-", "*"])
        if op == "+":
            a = random.randint(10, 50)
            b = random.randint(10, 50)
            return f"{a} + {b}", a + b
        elif op == "-":
            a = random.randint(20, 75)
            b = random.randint(1, a)
            return f"{a} - {b}", a - b
        else:
            a = random.randint(2, 9)
            b = random.randint(2, 9)
            return f"{a} × {b}", a * b

    else:
        # Hard: larger addition, subtraction, multiplication up to 12x12
        op = random.choice(["+", "-", "*"])
        if op == "+":
            a = random.randint(25, 100)
            b = random.randint(25, 100)
            return f"{a} + {b}", a + b
        elif op == "-":
            a = random.randint(40, 150)
            b = random.randint(1, a)
            return f"{a} - {b}", a - b
        else:
            a = random.randint(3, 12)
            b = random.randint(3, 12)
            return f"{a} × {b}", a * b


def play_quick_math(
    title_style: str = "slant",
    color_scheme: str = "neon_cyan",
    direct_mode: bool = False,
) -> bool:
    """
    Run an interactive Quick Math game session.

    Returns:
    - True to return to menu / shell cleanly
    - False if user chose to quit the program
    """
    clear_screen()
    print_header(title_style, color_scheme, subtitle="Game: Quick Math")

    print(style_text("Welcome to Quick Math!", color_scheme, color_type="accent", bold=True))
    print("Sharp arithmetic challenges for a quick mental workout.\n")
    print("Rules:")
    print(f"  1. Answer {QUESTIONS_PER_ROUND} arithmetic questions per round.")
    print("  2. Enter the numerical answer for each problem.")
    print("  3. Non-numeric answers are rejected without consuming an attempt.")
    print("Controls:")
    print("  Type your integer answer and press Enter.")
    print("  Enter 'b' to go back, 'q' to quit anytime.\n")
    print_divider(color_scheme)

    while True:
        # Select difficulty
        print("Select Difficulty Level:")
        print("  1. Easy   (Simple addition & subtraction: 1-20)")
        print("  2. Medium (Numbers up to 50 & single-digit multiplication)")
        print("  3. Hard   (Numbers up to 100 & tables up to 12×12)")

        while True:
            diff_act = prompt_input("Choose difficulty [1-3] (b=back, q=quit): ", color_scheme=color_scheme, allow_back=True, allow_quit=True)
            if diff_act == NavigationAction.QUIT:
                return False
            if diff_act == NavigationAction.BACK:
                return True

            diff_str = str(diff_act).strip()
            if diff_str in ("1", "2", "3"):
                difficulty = int(diff_str)
                break
            print(style_text("Please enter 1, 2, or 3.", color_scheme, color_type="warning"))

        print_divider(color_scheme)
        diff_names = {1: "Easy", 2: "Medium", 3: "Hard"}
        print(style_text(f"Starting {diff_names[difficulty]} round ({QUESTIONS_PER_ROUND} questions)!", color_scheme, color_type="accent"))
        print()

        correct_count = 0

        for q_idx in range(1, QUESTIONS_PER_ROUND + 1):
            q_text, ans = generate_question(difficulty)

            while True:
                prompt_label = f"Q{q_idx}/{QUESTIONS_PER_ROUND}:  {q_text} = "
                act = prompt_input(prompt_label, color_scheme=color_scheme, allow_back=True, allow_quit=True)

                if act == NavigationAction.QUIT:
                    return False
                if act == NavigationAction.BACK:
                    return True

                raw_ans = str(act).strip()
                try:
                    user_val = int(raw_ans)
                    break
                except ValueError:
                    print(style_text(f"'{raw_ans}' is not a valid number. Please enter an integer.", color_scheme, color_type="warning"))

            if user_val == ans:
                correct_count += 1
                print(style_text("★ Correct! Well done.", color_scheme, color_type="success", bold=True))
            else:
                print(style_text(f"✗ Incorrect. The correct answer was {ans}.", color_scheme, color_type="error", bold=True))
            print()

        # Round Summary
        print_divider(color_scheme)
        score_pct = int((correct_count / QUESTIONS_PER_ROUND) * 100)
        summary_msg = f"Round Summary: {correct_count}/{QUESTIONS_PER_ROUND} Correct ({score_pct}%)"
        print(style_text(summary_msg, color_scheme, color_type="accent", bold=True))

        if correct_count == QUESTIONS_PER_ROUND:
            print(style_text("★ Flawless calculation! Mathematical genius! ★", color_scheme, color_type="success", bold=True))
        elif correct_count >= 3:
            print(style_text("Solid mental math! Good work.", color_scheme, color_type="accent"))
        else:
            print("Keep practicing — speed and accuracy will follow!")

        print_divider(color_scheme)

        # Replay prompt
        replay_prompt = "Play another round of Quick Math? [y/n] (b=back, q=quit): "
        replay_act = prompt_input(replay_prompt, color_scheme=color_scheme, allow_back=True, allow_quit=True)

        if replay_act == NavigationAction.QUIT:
            return False
        if replay_act == NavigationAction.BACK:
            return True

        if str(replay_act).strip().lower() not in ("y", "yes"):
            print(style_text("\nThanks for playing Quick Math!\n", color_scheme, color_type="accent"))
            return True

        clear_screen()
        print_header(title_style, color_scheme, subtitle="Game: Quick Math")
