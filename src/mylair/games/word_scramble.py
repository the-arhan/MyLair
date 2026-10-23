"""
Word Scramble Game for My Lair.

Rules:
- The computer selects a secret word and scrambles its letters.
- The scrambled word is guaranteed never to equal the original word when an alternate
  arrangement is possible.
- You have 3 attempts to unscramble and guess the secret word.
- Optional Hint: Type 'hint' or '?' at any time to receive a helpful clue without
  consuming an attempt!

Beginner Customization:
- Add or modify words and clues in the BUILTIN_WORDS list below!
"""

from __future__ import annotations

import random
from typing import Dict, List, Tuple

from mylair.display import (
    NavigationAction,
    clear_screen,
    print_divider,
    print_header,
    prompt_input,
    style_text,
)

BUILTIN_WORDS: List[Dict[str, str]] = [
    {"word": "PYTHON", "hint": "A powerful high-level programming language and great serpent"},
    {"word": "TERMINAL", "hint": "Command-line text interface for computer power users"},
    {"word": "CYBER", "hint": "Relating to digital technology, computers, and futuristic networks"},
    {"word": "ARCADE", "hint": "Classic coin-operated gaming hall filled with retro cabinets"},
    {"word": "DRAGON", "hint": "Legendary winged fire-breathing creature guarding vast treasure"},
    {"word": "WIZARD", "hint": "Master of arcane sorcery, spellbooks, and glowing runes"},
    {"word": "MATRIX", "hint": "A rectangular array of numbers or simulated digital reality"},
    {"word": "KNIGHT", "hint": "Chivalrous armored champion sworn to protect the realm"},
    {"word": "CASTLE", "hint": "Towering medieval fortified fortress with a moat and keep"},
    {"word": "SHADOW", "hint": "Dark silhouette created when light is obstructed by an object"},
    {"word": "DUNGEON", "hint": "Underground labyrinth filled with vaults, traps, and secrets"},
    {"word": "MYSTERY", "hint": "An enigma or puzzle that demands keen deduction to solve"},
    {"word": "COSMOS", "hint": "The vast, orderly universe spanning stars and galaxies"},
    {"word": "PIXEL", "hint": "The smallest controllable illuminated dot on a digital screen"},
    {"word": "BINARY", "hint": "Base-2 numeric system consisting solely of zeroes and ones"},
    {"word": "SYNTH", "hint": "Electronic instrument producing futuristic retro musical tones"},
]

MAX_GUESSES = 3


def scramble_word(word: str) -> str:
    """
    Scramble the letters of word such that the scrambled string is NOT
    identical to the original word (as long as at least two letters differ).
    Sensibly handles words with repeated letters.
    """
    letters = list(word.upper())
    if len(set(letters)) <= 1:
        return word.upper()

    scrambled = letters[:]
    for _ in range(100):
        random.shuffle(scrambled)
        if "".join(scrambled) != word.upper():
            return "".join(scrambled)

    # Deterministic fallback: swap first two distinct characters
    for i in range(len(scrambled) - 1):
        if scrambled[i] != scrambled[i + 1]:
            scrambled[i], scrambled[i + 1] = scrambled[i + 1], scrambled[i]
            break

    return "".join(scrambled)


def play_word_scramble(
    title_style: str = "slant",
    color_scheme: str = "neon_cyan",
    direct_mode: bool = False,
) -> bool:
    """
    Run an interactive Word Scramble game session.

    Returns:
    - True to return to menu / shell cleanly
    - False if user chose to quit the program
    """
    clear_screen()
    print_header(title_style, color_scheme, subtitle="Game: Word Scramble")

    print(style_text("Welcome to Word Scramble!", color_scheme, color_type="accent", bold=True))
    print("Unscramble the jumbled letters to reveal the secret word.\n")
    print("Rules:")
    print(f"  1. You have {MAX_GUESSES} attempts to guess the scrambled word.")
    print("  2. Type 'hint' or '?' at any prompt for a clue (does NOT use an attempt).")
    print("  3. Letter casing does not matter.\n")
    print("Controls:")
    print("  Type your word guess and press Enter.")
    print("  Enter 'hint' for a clue.")
    print("  Enter 'b' to go back, 'q' to quit anytime.\n")
    print_divider(color_scheme)

    while True:
        entry = random.choice(BUILTIN_WORDS)
        target_word = entry["word"].upper()
        clue = entry["hint"]
        scrambled = scramble_word(target_word)

        attempts_left = MAX_GUESSES
        hint_revealed = False
        solved = False

        print(style_text(f"New word chosen! Scrambled letters:  [ {scrambled} ]", color_scheme, color_type="accent", bold=True))
        print(f"Word length: {len(target_word)} letters. Attempts: {attempts_left}")
        print()

        while attempts_left > 0 and not solved:
            prompt_msg = f"Your guess ({attempts_left} left, 'hint' for clue): "
            act = prompt_input(prompt_msg, color_scheme=color_scheme, allow_back=True, allow_quit=True)

            if act == NavigationAction.QUIT:
                return False
            if act == NavigationAction.BACK:
                return True

            raw_guess = str(act).strip().upper()

            if not raw_guess:
                continue

            if raw_guess in ("HINT", "?"):
                hint_revealed = True
                print(style_text(f"💡 Hint: {clue}", color_scheme, color_type="warning"))
                print(f"Scrambled: [ {scrambled} ]")
                print()
                continue

            if raw_guess == target_word:
                solved = True
                print()
                print(style_text(f"★ BINGO! The secret word was '{target_word}'! ★", color_scheme, color_type="success", bold=True))
                print(f"You unscrambled it with {attempts_left} attempt(s) remaining!")
                break
            else:
                attempts_left -= 1
                if attempts_left > 0:
                    print(style_text(f"✗ '{raw_guess}' is incorrect! {attempts_left} attempt(s) remaining.", color_scheme, color_type="warning"))
                    print(f"Scrambled: [ {scrambled} ]")
                    print()
                else:
                    print(style_text(f"✗ '{raw_guess}' is incorrect.", color_scheme, color_type="error"))

        if not solved:
            print_divider(color_scheme)
            print(style_text(f"Out of attempts! The secret word was: '{target_word}'", color_scheme, color_type="error", bold=True))
            print(f"Meaning/Clue: {clue}")

        print_divider(color_scheme)

        # Replay prompt
        replay_prompt = "Play another round of Word Scramble? [y/n] (b=back, q=quit): "
        replay_act = prompt_input(replay_prompt, color_scheme=color_scheme, allow_back=True, allow_quit=True)

        if replay_act == NavigationAction.QUIT:
            return False
        if replay_act == NavigationAction.BACK:
            return True

        if str(replay_act).strip().lower() not in ("y", "yes"):
            print(style_text("\nThanks for playing Word Scramble!\n", color_scheme, color_type="accent"))
            return True

        clear_screen()
        print_header(title_style, color_scheme, subtitle="Game: Word Scramble")
