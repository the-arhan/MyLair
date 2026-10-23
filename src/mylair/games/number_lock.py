"""
Number Lock Game for My Lair.

Rules:
- The vault lock has generated a secret 4-digit code.
- REPEATED DIGITS: No repeated digits are allowed in the lock code (all digits 1-9 are unique).
- Hints provided after each valid guess:
  - Exact Match (🟢): Correct digit in the correct position.
  - Wrong Position (🟡): Correct digit, but located in another position.
  - Miss (⚪): Digit not found anywhere in the code.
- INPUT VALIDATION: Guesses with the wrong length, invalid characters, or duplicate
  digits are rejected without consuming an attempt.
- You have 8 attempts to crack the code and open the vault!

Beginner Customization:
- Adjust CODE_LENGTH (e.g. 3 or 4) or MAX_ATTEMPTS below.
"""

from __future__ import annotations

import random
from typing import List, Tuple

from mylair.display import (
    NavigationAction,
    clear_screen,
    print_divider,
    print_header,
    prompt_input,
    style_text,
)

CODE_LENGTH = 4
MAX_ATTEMPTS = 8
ALLOWED_DIGITS = "123456789"


def generate_secret_code(length: int = CODE_LENGTH) -> str:
    """Generate a random secret code with unique digits from 1 to 9."""
    digits = list(ALLOWED_DIGITS)
    random.shuffle(digits)
    return "".join(digits[:length])


def validate_guess(guess_str: str, length: int = CODE_LENGTH) -> Tuple[bool, str]:
    """
    Validate player guess.
    Returns (is_valid, error_reason).
    """
    clean = guess_str.strip()
    if len(clean) != length:
        return False, f"Code must be exactly {length} digits long."
    if not clean.isdigit():
        return False, "Code must contain digits only."
    if any(ch not in ALLOWED_DIGITS for ch in clean):
        return False, f"Digits must be between 1 and 9 (no zeroes)."
    if len(set(clean)) != length:
        return False, "All digits must be unique (no repeated digits)."
    return True, ""


def evaluate_guess(guess: str, secret: str) -> Tuple[int, int, int]:
    """
    Calculate (exact_matches, wrong_position_matches, misses).
    """
    exact = 0
    wrong_pos = 0

    for i in range(len(guess)):
        if guess[i] == secret[i]:
            exact += 1
        elif guess[i] in secret:
            wrong_pos += 1

    misses = len(guess) - (exact + wrong_pos)
    return exact, wrong_pos, misses


def play_number_lock(
    title_style: str = "slant",
    color_scheme: str = "neon_cyan",
    direct_mode: bool = False,
) -> bool:
    """
    Run an interactive Number Lock game session.

    Returns:
    - True to return to menu / shell cleanly
    - False if user chose to quit the program
    """
    clear_screen()
    print_header(title_style, color_scheme, subtitle="Game: Number Lock")

    print(style_text("Welcome to Number Lock!", color_scheme, color_type="accent", bold=True))
    print("Crack the vault's secret numeric combination using logic and deduction.\n")
    print("Rules:")
    print(f"  1. The vault code is {CODE_LENGTH} unique digits using numbers 1 to 9.")
    print("  2. REPEATED DIGITS: No repeated digits are allowed in the combination.")
    print("  3. After each valid guess, you receive hints:")
    print("     • Exact (🟢): Correct digit in the exact position.")
    print("     • Wrong Pos (🟡): Correct digit, but in another position.")
    print("     • Miss (⚪): Digit is not in the code.")
    print(f"  4. You have {MAX_ATTEMPTS} attempts. Invalid input is rejected without consuming a guess.")
    print("Controls:")
    print(f"  Type a {CODE_LENGTH}-digit code (e.g. 1482) and press Enter.")
    print("  Enter 'b' to go back, 'q' to quit anytime.\n")
    print_divider(color_scheme)

    while True:
        secret = generate_secret_code(CODE_LENGTH)
        history: List[Tuple[int, str, int, int, int]] = []
        attempts_used = 0
        unlocked = False

        print(style_text(f"Vault security initialized. New {CODE_LENGTH}-digit code set!", color_scheme, color_type="accent"))
        print()

        while attempts_used < MAX_ATTEMPTS and not unlocked:
            remaining = MAX_ATTEMPTS - attempts_used

            # Display previous guess history
            if history:
                print("Previous Guesses:")
                for att_num, g_str, ex, wp, ms in history:
                    hint_str = f"🟢 Exact: {ex}  |  🟡 Wrong Pos: {wp}  |  ⚪ Miss: {ms}"
                    print(f"  #{att_num}:  [ {g_str} ]  -->  {hint_str}")
                print()

            # Prompt for guess
            prompt_msg = f"Attempt {attempts_used + 1}/{MAX_ATTEMPTS} ({remaining} left) - Enter code: "
            act = prompt_input(prompt_msg, color_scheme=color_scheme, allow_back=True, allow_quit=True)

            if act == NavigationAction.QUIT:
                return False
            if act == NavigationAction.BACK:
                return True

            raw_guess = str(act).strip()
            is_valid, reason = validate_guess(raw_guess, CODE_LENGTH)
            if not is_valid:
                print(style_text(f"Invalid Guess: {reason} (Attempt NOT consumed)", color_scheme, color_type="warning"))
                print()
                continue

            attempts_used += 1
            exact, wrong_pos, misses = evaluate_guess(raw_guess, secret)
            history.append((attempts_used, raw_guess, exact, wrong_pos, misses))

            print()
            hint_disp = f"🟢 Exact: {exact}  |  🟡 Wrong Pos: {wrong_pos}  |  ⚪ Miss: {misses}"
            print(f"Guess #{attempts_used}: [ {raw_guess} ] -> {hint_disp}")

            if exact == CODE_LENGTH:
                unlocked = True
                print()
                print(style_text("🔓 *CLIIICK!* The heavy vault door swings wide open!", color_scheme, color_type="success", bold=True))
                print(style_text(f"★ Code cracked in {attempts_used} attempt(s)! Excellent deduction! ★", color_scheme, color_type="success"))
                break

            print()

        if not unlocked:
            print_divider(color_scheme)
            print(style_text("🔒 *BZZZT!* Vault lockdown triggered. Out of attempts!", color_scheme, color_type="error", bold=True))
            print(f"The secret combination was: [ {secret} ]")

        print_divider(color_scheme)

        # Replay prompt
        replay_prompt = "Play another game of Number Lock? [y/n] (b=back, q=quit): "
        replay_act = prompt_input(replay_prompt, color_scheme=color_scheme, allow_back=True, allow_quit=True)

        if replay_act == NavigationAction.QUIT:
            return False
        if replay_act == NavigationAction.BACK:
            return True

        if str(replay_act).strip().lower() not in ("y", "yes"):
            print(style_text("\nThanks for playing Number Lock!\n", color_scheme, color_type="accent"))
            return True

        clear_screen()
        print_header(title_style, color_scheme, subtitle="Game: Number Lock")
