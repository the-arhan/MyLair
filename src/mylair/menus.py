"""
Interactive menu system for My Lair.

Provides:
- Main menu (Game Menu, Credits, Help, Settings, Quit)
- Game menu (RPS, First to Fifty, Guess the Number, Random Game, Back, Quit)
- Settings menu (interactive title style & color scheme selection with live previews)
- Credits screen (factual attribution to My Lair and Python's standard library)
- Help screen (comprehensive instructions for launcher, games, navigation, and settings)
"""

from __future__ import annotations

import sys
import time
from typing import Dict

from mylair.display import (
    ASCII_TITLES,
    THEMES,
    NavigationAction,
    clear_screen,
    pause_prompt,
    print_divider,
    print_header,
    prompt_input,
    render_title_gradient,
    show_exit_countdown,
    style_text,
)
from mylair.games.registry import (
    find_game,
    get_all_games,
    get_random_game,
)
from mylair.settings import (
    VALID_COLOR_SCHEMES,
    VALID_TITLE_STYLES,
    load_settings,
    save_settings,
)


def show_credits_screen(title_style: str, color_scheme: str) -> None:
    """Display factual project credits."""
    clear_screen()
    print_header(title_style, color_scheme, subtitle="Project Credits")

    print(style_text("MY LAIR - Terminal Game Launcher", color_scheme, color_type="accent", bold=True))
    print("A retro-inspired, distraction-free command-line gaming break for developers.")
    print()
    print_divider(color_scheme)
    print("Project Information:")
    print("  • Project Name: My Lair")
    print("  • Author:       Arhan Ali")
    print("  • License:      MIT License")
    print("  • Language:     Python 3 (Standard Library)")
    print()
    print("Attribution & Technology:")
    print("  • Zero external runtime dependencies.")
    print("  • Built entirely on standard Python modules: sys, os, pathlib,")
    print("    argparse, json, random, and shutil.")
    print("  • Cross-platform ANSI Virtual Terminal Processing for Windows,")
    print("    macOS, and Linux.")
    print_divider(color_scheme)

    pause_prompt(color_scheme, "Press Enter to return to the main menu...")


def show_help_screen(title_style: str, color_scheme: str) -> None:
    """Display detailed help and game rules."""
    clear_screen()
    print_header(title_style, color_scheme, subtitle="Launcher & Game Help")

    print(style_text("COMMAND-LINE INTERFACE (CLI)", color_scheme, color_type="accent", bold=True))
    print("  mylair start               Open the interactive main menu.")
    print("  mylair -s <game>           Launch a specific game directly.")
    print("  mylair --help              View command-line help flags.")
    print("  mylair help                Display general usage information.\n")
    print("  Examples of direct launch:")
    print("    mylair -s rps              (Rock Paper Scissors Plus)")
    print("    mylair -s f2f              (First to Fifty)")
    print("    mylair -s gtn              (Guess the Number)")
    print("    mylair -s oddoreven        (Odd or Even)")
    print("    mylair -s coin             (Coin Flip Streak)")
    print("    mylair -s higher           (Higher or Lower)")
    print("    mylair -s math             (Quick Math)")
    print("    mylair -s dice             (Dice Duel)")
    print("    mylair -s lock             (Number Lock)")
    print("    mylair -s scramble         (Word Scramble)")
    print("    mylair -s takethelast      (Take the Last)")
    print("    mylair -s fortune          (Fortune Cookie)")
    print("    mylair -s 8ball            (The 8 Ball)")
    print("    mylair -s doom             (The Lair's Doom)\n")

    print_divider(color_scheme)
    print(style_text("NAVIGATION & SHORTCUTS", color_scheme, color_type="accent", bold=True))
    print("  • On numbered menus: Type the number of your choice and press Enter.")
    print("  • At active text input prompts:")
    print("      Type 'b' and press Enter to return to the previous menu.")
    print("      Type 'q' and press Enter to exit cleanly to your terminal.")
    print("  • Ctrl+C is caught gracefully at any point without crashes or tracebacks.\n")

    print_divider(color_scheme)
    print(style_text("GAME RULES", color_scheme, color_type="accent", bold=True))
    print("  1. Rock Paper Scissors Plus (rps, rpsplus):")
    print("     5-way expanded duel: Rock crushes Scissors/Lizard, Paper covers Rock/disproves Spock,")
    print("     Scissors cuts Paper/decapitates Lizard, Lizard poisons Spock/eats Paper,")
    print("     Spock smashes Scissors/vaporizes Rock. (Shortcuts: r, p, s, l, k).\n")
    print("  2. First to Fifty (f2f):")
    print("     Turn-based race to 50 starting from 0. On your turn, add any integer")
    print("     from 1 to 10. The first player to reach or exceed 50 wins!\n")
    print("  3. Guess the Number (gtn):")
    print("     The computer picks a secret number from 1 to 100. Enter guesses to")
    print("     receive 'Too high' or 'Too low' clues and dynamic search range hints.\n")
    print("  4. Odd or Even (oddoreven, ooe):")
    print("     Predict whether the sum will be Odd (o) or Even (e). Both pick a number (1-5).")
    print("     If the sum's parity matches your prediction, you win!\n")
    print("  5. Coin Flip Streak (coinflipstreak, cfs, coin):")
    print("     Predict Heads (h) or Tails (t). Correct calls grow your streak. Choose to")
    print("     continue or bank your score. An incorrect call resets your streak to 0!\n")
    print("  6. Higher or Lower (higherorlower, hol, higher):")
    print("     Forecast whether the next number (1-50) will be Higher (h) or Lower (l).")
    print("     Equal numbers count as a push (tie) without penalty.\n")
    print("  7. Quick Math (quickmath, math):")
    print("     Solve 5 casual arithmetic problems across Easy, Medium, or Hard difficulty.\n")
    print("  8. Dice Duel (diceduel, dice):")
    print("     Roll 2d6 against the computer. Play single rolls or best-of-3/5 series. Ties are ties.\n")
    print("  9. Number Lock (numberlock, lock):")
    print("     Crack the secret 4-digit unique code in 8 attempts. Receive Exact (🟢),")
    print("     Wrong Position (🟡), and Miss (⚪) hints. Invalid inputs do not cost an attempt.\n")
    print("  10. Word Scramble (wordscramble, scramble):")
    print("      Unscramble jumbled retro words in 3 tries. Type 'hint' for a free clue.\n")
    print("  11. Take the Last (takethelast, ttl):")
    print("      Take 1 to 3 tokens from a pile of 15. The player who takes the last token wins!\n")
    print("  12. Fortune Cookie (fortunecookie, fortune):")
    print("      Pick an artisan cookie to reveal friendly wisdom and lucky numbers (for fun only).\n")
    print("  13. The 8 Ball (the8ball, 8ball):")
    print("      Ask any question and simulate the classic oracle roll for 8 playful answers.\n")
    print("  14. The Lair's Doom (thelairsdoom, doom):")
    print("      A choice-based dungeon adventure with HP, inventory, and multiple unique endings.\n")

    print_divider(color_scheme)
    print(style_text("SETTINGS & CONFIGURATION", color_scheme, color_type="accent", bold=True))
    print("  Preferences (title style and color theme) are saved automatically in your")
    print("  user configuration directory: ~/.config/mylair/ or %APPDATA%/mylair/.")
    print_divider(color_scheme)

    pause_prompt(color_scheme, "Press Enter to return to the main menu...")


def settings_menu(current_settings: Dict[str, str]) -> Dict[str, str]:
    """
    Submenu for customizing My Lair appearance and color schemes.
    Allows testing and instant saving of settings.
    """
    while True:
        title_style = current_settings.get("title_style", "official")
        color_scheme = current_settings.get("color_scheme", "synthwave")

        clear_screen()
        print_header(title_style, color_scheme, subtitle="Settings & Appearance")

        curr_theme_obj = THEMES.get(color_scheme, THEMES["synthwave"])
        print(f"Official Logo:  {style_text('Active (Exclusive Retro Shaded Block Art)', color_scheme, color_type='accent', bold=True)}")
        print(f"Current Theme:  {style_text(curr_theme_obj.display_name, color_scheme, color_type='accent', bold=True)}\n")

        print("1. Change Color Theme (Theme Palette)")
        print("2. Reset Settings to Default")
        print("3. Back to Main Menu")
        print("4. Quit My Lair\n")
        print_divider(color_scheme)

        action = prompt_input("Enter choice [1-4]: ", color_scheme=color_scheme, allow_back=True, allow_quit=True)

        if action in (NavigationAction.QUIT, "4"):
            show_exit_countdown(seconds=3, color_scheme=color_scheme, farewell_message="Exiting My Lair. Goodbye!")
            sys.exit(0)

        if action in (NavigationAction.BACK, "3"):
            break

        if action == "1":
            # Change Color Scheme
            while True:
                clear_screen()
                print_header(title_style, color_scheme, subtitle="Select Color Theme")
                print("Available Color Palettes:\n")
                for idx, scheme_key in enumerate(VALID_COLOR_SCHEMES, start=1):
                    theme_info = THEMES[scheme_key]
                    marker = " (Active)" if scheme_key == color_scheme else ""
                    # Sample swatch preview
                    sample = style_text(" ■■■ ", scheme_key, color_type="accent", bold=True)
                    print(f"{idx}. {sample} {theme_info.display_name}{marker}")
                print(f"{len(VALID_COLOR_SCHEMES) + 1}. Cancel / Back\n")
                print_divider(color_scheme)

                choice_act = prompt_input(
                    f"Select theme [1-{len(VALID_COLOR_SCHEMES) + 1}]: ",
                    color_scheme=color_scheme,
                    allow_back=True,
                    allow_quit=True,
                )
                if choice_act in (NavigationAction.QUIT, NavigationAction.BACK, str(len(VALID_COLOR_SCHEMES) + 1)):
                    break

                try:
                    chosen_idx = int(str(choice_act).strip()) - 1
                    if 0 <= chosen_idx < len(VALID_COLOR_SCHEMES):
                        new_scheme = VALID_COLOR_SCHEMES[chosen_idx]
                        current_settings["color_scheme"] = new_scheme
                        save_settings(current_settings)
                        color_scheme = new_scheme
                        print(style_text(f"\nColor theme updated to '{THEMES[new_scheme].display_name}'!", color_scheme, color_type="success"))
                        time.sleep(0.8)
                        break
                    else:
                        print(style_text("Invalid selection number.", color_scheme, color_type="warning"))
                        time.sleep(0.8)
                except ValueError:
                    print(style_text("Please enter a valid number.", color_scheme, color_type="warning"))
                    time.sleep(0.8)

        elif action == "2":
            # Reset to defaults
            current_settings["title_style"] = "official"
            current_settings["color_scheme"] = "synthwave"
            save_settings(current_settings)
            print(style_text("\nSettings successfully reset to defaults!", color_scheme, color_type="success"))
            time.sleep(0.8)

        else:
            print(style_text("Invalid selection. Please choose an option from 1 to 4.", color_scheme, color_type="warning"))
            time.sleep(1.0)

    return current_settings


def game_menu(title_style: str, color_scheme: str) -> bool:
    """
    Submenu for selecting and launching games.
    Presents all registered games, Random Game, Back to Main Menu, and Quit.

    Returns:
    - True to return to main menu
    - False to quit application
    """
    all_games = get_all_games()

    while True:
        clear_screen()
        print_header(title_style, color_scheme, subtitle="Game Selection")

        for idx, game in enumerate(all_games, start=1):
            print(f"{idx}. {style_text(game.display_title, color_scheme, color_type='accent', bold=True)}")
            print(f"   {game.description}")

        random_idx = len(all_games) + 1
        back_idx = len(all_games) + 2
        quit_idx = len(all_games) + 3

        print(f"{random_idx}. {style_text('Random Game', color_scheme, color_type='accent', bold=True)}")
        print("   Pick a surprise game at random and jump right in!")
        print(f"{back_idx}. Back to Main Menu")
        print(f"{quit_idx}. Quit My Lair\n")
        print_divider(color_scheme)

        action = prompt_input(f"Enter choice [1-{quit_idx}]: ", color_scheme=color_scheme, allow_back=True, allow_quit=True)

        if action in (NavigationAction.QUIT, str(quit_idx)):
            return False

        if action in (NavigationAction.BACK, str(back_idx)):
            return True

        if action == str(random_idx):
            chosen_game = get_random_game()
            print()
            print(style_text(f"🎲 Random choice: {chosen_game.display_title}!", color_scheme, color_type="accent", bold=True))
            print("Launching game now...")
            time.sleep(1.2)
            should_continue = chosen_game.runner(title_style, color_scheme, False)
            if not should_continue:
                return False
            continue

        try:
            val = int(str(action).strip())
            if 1 <= val <= len(all_games):
                selected_game = all_games[val - 1]
                should_continue = selected_game.runner(title_style, color_scheme, False)
                if not should_continue:
                    return False
            else:
                print(style_text(f"Please enter a number between 1 and {quit_idx}.", color_scheme, color_type="warning"))
                time.sleep(1.0)
        except ValueError:
            print(style_text(f"Invalid input. Please enter a number between 1 and {quit_idx}.", color_scheme, color_type="warning"))
            time.sleep(1.0)


def main_menu() -> None:
    """
    Main interactive entry point for My Lair.

    Options:
    1. Game Menu
    2. Credits
    3. Help
    4. Settings
    5. Quit
    """
    settings = load_settings()

    while True:
        title_style = settings.get("title_style", "official")
        color_scheme = settings.get("color_scheme", "synthwave")

        clear_screen()
        print_header(title_style, color_scheme, subtitle="Main Menu")

        print("1. Game Menu")
        print("2. Credits")
        print("3. Help")
        print("4. Settings")
        print("5. Quit\n")
        print_divider(color_scheme)

        action = prompt_input("Enter choice [1-5]: ", color_scheme=color_scheme, allow_back=False, allow_quit=True)

        if action in (NavigationAction.QUIT, "5"):
            show_exit_countdown(seconds=3, color_scheme=color_scheme)
            break

        if action == "1":
            should_continue = game_menu(title_style, color_scheme)
            if not should_continue:
                show_exit_countdown(seconds=3, color_scheme=color_scheme)
                break

        elif action == "2":
            show_credits_screen(title_style, color_scheme)

        elif action == "3":
            show_help_screen(title_style, color_scheme)

        elif action == "4":
            settings = settings_menu(settings)

        else:
            print(style_text("Invalid selection. Please choose an option from 1 to 5.", color_scheme, color_type="warning"))
            time.sleep(1.0)
