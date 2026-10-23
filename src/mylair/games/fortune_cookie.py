"""
Fortune Cookie Game for My Lair.

Rules:
- Select one of the handcrafted fortune cookies to crack open.
- Read a short, friendly, and varied fortune along with a set of lucky numbers.
- DISCLAIMER: Fortunes are lighthearted entertainment and playful amusement —
  never factual predictions or serious advice!

Beginner Customization:
- Add or edit cookies and fortunes in COOKIE_FLAVORS and FORTUNES below.
"""

from __future__ import annotations

import random
from typing import List

from mylair.display import (
    NavigationAction,
    clear_screen,
    print_divider,
    print_header,
    prompt_input,
    style_text,
)

COOKIE_FLAVORS = [
    "Golden Lotus Cookie",
    "Neon Dragon Cookie",
    "Midnight Wanderer Cookie",
    "Cybernetic Pixel Cookie",
    "Mystery Lair Cookie",
]

FORTUNES: List[str] = [
    "A bug in your code will unexpectedly turn out to be a brilliant undocumented feature.",
    "The best way to predict your future is to write clean, maintainable code today.",
    "An unexpected compliment will brighten your terminal screen very soon.",
    "Your patience will soon be rewarded with all unit tests passing on the first attempt.",
    "Great things never come from comfort zones, but good snacks definitely do.",
    "A thrilling new side project or a quiet warm cup of tea awaits you. Choose both.",
    "Clear indentation in your code leads to clear thinking in your mind.",
    "You will soon conquer a difficult problem that once seemed impossible.",
    "A mysterious message in a commit log will bring a smile to your face.",
    "Kindness is the ultimate high-level language — everyone understands it without a compiler.",
    "The secret to progress is simply getting started; one keystroke at a time.",
    "Your creative energy is at an all-time high. Build something delightful today!",
    "A serendipitous idea will strike when you step away from the monitor.",
    "Good fortune follows those who remember to save and push their work frequently.",
    "A long-awaited pull request will soon be merged with zero merge conflicts.",
    "Life is like a terminal: simple commands often produce the most astonishing results.",
    "Curiosity is your superpower. Keep exploring the unknown depths of the lair.",
    "Today is a fantastic day to try something you have never attempted before.",
    "A warm breeze, a cool terminal font, and a fun puzzle make for a wonderful day.",
    "Remember: Even the greatest software architects once forgot a closing parenthesis.",
]


def pick_fortune() -> str:
    """Return a random friendly fortune."""
    return random.choice(FORTUNES)


def generate_lucky_numbers(count: int = 5) -> List[int]:
    """Generate a sorted set of lucky numbers between 1 and 99."""
    nums = random.sample(range(1, 100), count)
    return sorted(nums)


def render_cookie_art() -> str:
    """ASCII art showing a cracked fortune cookie with a scroll slip."""
    return (
        "       .---.          \n"
        "      /  *  \\   CRACK!  \n"
        "     |   |   | =======> 📜  [ Fortune Paper Unfolded ]\n"
        "      \\  *  /          \n"
        "       '---'           "
    )


def play_fortune_cookie(
    title_style: str = "slant",
    color_scheme: str = "neon_cyan",
    direct_mode: bool = False,
) -> bool:
    """
    Run an interactive Fortune Cookie session.

    Returns:
    - True to return to menu / shell cleanly
    - False if user chose to quit the program
    """
    clear_screen()
    print_header(title_style, color_scheme, subtitle="Game: Fortune Cookie")

    print(style_text("Welcome to the Fortune Cookie Vault!", color_scheme, color_type="accent", bold=True))
    print("Crack open a crispy fortune cookie for playful wisdom and lucky numbers.\n")
    print("Note:")
    print("  All fortunes are created purely for fun and cheerful entertainment.")
    print("  They are not factual predictions or serious life advice!\n")
    print("Controls:")
    print(f"  Select a cookie by entering a number (1-{len(COOKIE_FLAVORS)}).")
    print("  Enter 'b' to go back, 'q' to quit anytime.\n")
    print_divider(color_scheme)

    while True:
        print("Choose a Fortune Cookie to crack open:")
        for idx, name in enumerate(COOKIE_FLAVORS, start=1):
            print(f"  {idx}. 🥠 {name}")
        print()

        while True:
            prompt_msg = f"Select your cookie [1-{len(COOKIE_FLAVORS)}] (b=back, q=quit): "
            act = prompt_input(prompt_msg, color_scheme=color_scheme, allow_back=True, allow_quit=True)

            if act == NavigationAction.QUIT:
                return False
            if act == NavigationAction.BACK:
                return True

            raw_str = str(act).strip()
            try:
                choice = int(raw_str)
                if 1 <= choice <= len(COOKIE_FLAVORS):
                    chosen_cookie = COOKIE_FLAVORS[choice - 1]
                    break
                print(style_text(f"Please enter a number between 1 and {len(COOKIE_FLAVORS)}.", color_scheme, color_type="warning"))
            except ValueError:
                print(style_text("Please enter a valid number.", color_scheme, color_type="warning"))

        fortune_text = pick_fortune()
        lucky_nums = generate_lucky_numbers(5)
        num_str = ", ".join(str(n) for n in lucky_nums)

        print()
        print(style_text(f"Cracking open the {chosen_cookie}...", color_scheme, color_type="accent"))
        print(render_cookie_art())
        print()
        print_divider(color_scheme)
        print(style_text("YOUR FORTUNE:", color_scheme, color_type="accent", bold=True))
        print(f"  \"{fortune_text}\"\n")
        print(style_text(f"  Lucky Numbers: [ {num_str} ]", color_scheme, color_type="warning", bold=True))
        print_divider(color_scheme)

        # Replay prompt
        replay_prompt = "Crack open another fortune cookie? [y/n] (b=back, q=quit): "
        replay_act = prompt_input(replay_prompt, color_scheme=color_scheme, allow_back=True, allow_quit=True)

        if replay_act == NavigationAction.QUIT:
            return False
        if replay_act == NavigationAction.BACK:
            return True

        if str(replay_act).strip().lower() not in ("y", "yes"):
            print(style_text("\nMay good fortune and clean code accompany your day!\n", color_scheme, color_type="accent"))
            return True

        print()
