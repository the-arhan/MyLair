"""
Command-Line Interface (CLI) for My Lair.

Handles argument parsing, direct game execution, help presentation,
and graceful signal termination.
"""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from mylair import __version__
from mylair.display import show_exit_countdown, style_text
from mylair.games.registry import (
    find_game,
    format_unknown_game_error,
)
from mylair.menus import main_menu
from mylair.settings import load_settings


def create_parser() -> argparse.ArgumentParser:
    """Construct the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="mylair",
        description="My Lair - A friendly, retro command-line game launcher.",
        epilog=(
            "Quick Examples:\n"
            "  mylair start               Open interactive main menu\n"
            "  mylair -s rockpaperscissor Directly play Rock Paper Scissors (alias: rps)\n"
            "  mylair -s firsttofifty     Directly play First to Fifty (alias: f2f)\n"
            "  mylair -s guessthenumber   Directly play Guess the Number (alias: gtn)\n"
            "  mylair help                Show this help message\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "command",
        nargs="?",
        default=None,
        help="Command to run: 'start' (launch menu) or 'help' (show instructions).",
    )

    parser.add_argument(
        "-s",
        "--start-game",
        dest="direct_game",
        metavar="GAME",
        help="Directly launch a game by name or alias without opening menus.",
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"My Lair version {__version__}",
        help="Show program version and exit.",
    )

    return parser


def run_direct_game(game_query: str) -> int:
    """
    Launch a game directly without showing the main menu.
    Returns 0 on clean exit, 1 on unknown game.
    """
    descriptor = find_game(game_query)
    if descriptor is None:
        sys.stderr.write(format_unknown_game_error(game_query) + "\n")
        return 1

    settings = load_settings()
    title_style = settings.get("title_style", "official")
    color_scheme = settings.get("color_scheme", "synthwave")

    # Run the game in direct mode
    continued = descriptor.runner(title_style, color_scheme, True)
    if not continued:
        show_exit_countdown(seconds=3, color_scheme=color_scheme, farewell_message="Quitting My Lair. Goodbye!")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    """
    Main entry point invoked by the `mylair` console script or `python main.py`.
    """
    parser = create_parser()
    args = parser.parse_args(argv)

    try:
        # Check for direct game launch flag first (-s / --start-game)
        if args.direct_game:
            return run_direct_game(args.direct_game)

        # Handle positional command
        cmd = args.command.lower() if args.command else None

        if cmd in ("help", "--help", "-h"):
            parser.print_help()
            return 0

        if cmd == "start" or cmd is None:
            # Open interactive main menu
            main_menu()
            return 0

        # Check if the user passed a game name directly as a positional command (e.g. `mylair rps`)
        maybe_game = find_game(cmd)
        if maybe_game:
            return run_direct_game(cmd)

        # Unrecognized command
        sys.stderr.write(f"Error: Unrecognized command or game '{args.command}'.\n\n")
        parser.print_help(sys.stderr)
        return 1

    except KeyboardInterrupt:
        # Clean exit on Ctrl+C without stack trace
        sys.stdout.write("\n\nGoodbye from My Lair!\n")
        return 0


if __name__ == "__main__":
    sys.exit(main())
