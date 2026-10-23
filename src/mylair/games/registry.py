"""
Game registry for My Lair.

Defines game metadata, canonical identifiers, aliases, and runner functions.
Beginners can add new games to the launcher by adding an entry in GAME_REGISTRY.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional

from mylair.games.coin_flip_streak import play_coin_flip_streak
from mylair.games.dice_duel import play_dice_duel
from mylair.games.first_to_fifty import play_first_to_fifty
from mylair.games.fortune_cookie import play_fortune_cookie
from mylair.games.guess_the_number import play_guess_the_number
from mylair.games.higher_or_lower import play_higher_or_lower
from mylair.games.number_lock import play_number_lock
from mylair.games.odd_or_even import play_odd_or_even
from mylair.games.quick_math import play_quick_math
from mylair.games.rock_paper_scissors import play_rock_paper_scissors_plus
from mylair.games.take_the_last import play_take_the_last
from mylair.games.the_8_ball import play_the_8_ball
from mylair.games.the_lairs_doom import play_the_lairs_doom
from mylair.games.word_scramble import play_word_scramble


@dataclass(frozen=True)
class GameDescriptor:
    canonical_name: str
    display_title: str
    description: str
    runner: Callable[[str, str, bool], bool]
    aliases: List[str]


# ==============================================================================
# REGISTERED GAMES LIST
# (To add a new game to My Lair, add a GameDescriptor to this list!)
# ==============================================================================

GAME_REGISTRY: List[GameDescriptor] = [
    GameDescriptor(
        canonical_name="rockpaperscissorplus",
        display_title="Rock Paper Scissors Plus",
        description="Expanded 5-way tactical duel of Rock, Paper, Scissors, Lizard, Spock.",
        runner=play_rock_paper_scissors_plus,
        aliases=[
            "rps",
            "rockpaperscissor",
            "rock-paper-scissors",
            "rockpaperscissors",
            "rock_paper_scissors",
            "rock",
            "rpsplus",
            "rps-plus",
            "rpsls",
            "spock",
        ],
    ),
    GameDescriptor(
        canonical_name="firsttofifty",
        display_title="First to Fifty",
        description="Tactical turn-based addition race to reach 50.",
        runner=play_first_to_fifty,
        aliases=["f2f", "first-to-fifty", "fifty", "first_to_fifty"],
    ),
    GameDescriptor(
        canonical_name="guessthenumber",
        display_title="Guess the Number",
        description="Crack the secret mystery number between 1 and 100 with dynamic hints.",
        runner=play_guess_the_number,
        aliases=["gtn", "guess-the-number", "guess", "guess_the_number"],
    ),
    GameDescriptor(
        canonical_name="oddoreven",
        display_title="Odd or Even",
        description="Predict total sum parity and battle numbers against the computer.",
        runner=play_odd_or_even,
        aliases=["ooe", "odd-or-even", "odd_or_even", "odd", "even"],
    ),
    GameDescriptor(
        canonical_name="coinflipstreak",
        display_title="Coin Flip Streak",
        description="Call consecutive coin flips to build and bank your all-time streak.",
        runner=play_coin_flip_streak,
        aliases=["cfs", "coin-flip", "coinflip", "coin_flip_streak", "coin", "streak"],
    ),
    GameDescriptor(
        canonical_name="higherorlower",
        display_title="Higher or Lower",
        description="Forecast whether the next mystery number will rise or fall.",
        runner=play_higher_or_lower,
        aliases=["hol", "higher-or-lower", "higher_or_lower", "higher", "lower"],
    ),
    GameDescriptor(
        canonical_name="quickmath",
        display_title="Quick Math",
        description="Casual arithmetic challenges to sharpen mental calculation speed.",
        runner=play_quick_math,
        aliases=["math", "quick-math", "quick_math", "arithmetic"],
    ),
    GameDescriptor(
        canonical_name="diceduel",
        display_title="Dice Duel",
        description="Roll against the computer in quick single rolls or a best-of tournament.",
        runner=play_dice_duel,
        aliases=["dice", "duel", "dice-duel", "dice_duel"],
    ),
    GameDescriptor(
        canonical_name="numberlock",
        display_title="Number Lock",
        description="Deduce the vault's 4-digit code using exact and position clues.",
        runner=play_number_lock,
        aliases=["lock", "number-lock", "number_lock", "vault", "code"],
    ),
    GameDescriptor(
        canonical_name="wordscramble",
        display_title="Word Scramble",
        description="Unscramble jumbled retro and coding words with helpful clues.",
        runner=play_word_scramble,
        aliases=["scramble", "word-scramble", "word_scramble", "words", "anagram"],
    ),
    GameDescriptor(
        canonical_name="takethelast",
        display_title="Take the Last",
        description="Nim-style token subtraction strategy where taking the last token wins.",
        runner=play_take_the_last,
        aliases=["ttl", "take-the-last", "take_the_last", "nim", "tokens"],
    ),
    GameDescriptor(
        canonical_name="fortunecookie",
        display_title="Fortune Cookie",
        description="Crack open artisan cookies for friendly wisdom and lucky numbers.",
        runner=play_fortune_cookie,
        aliases=["fortune", "cookie", "fortune-cookie", "fortune_cookie"],
    ),
    GameDescriptor(
        canonical_name="the8ball",
        display_title="The 8 Ball",
        description="Ask any question to receive one of eight classic oracle responses.",
        runner=play_the_8_ball,
        aliases=["8ball", "eightball", "magic8ball", "the-8-ball", "8-ball", "eight-ball"],
    ),
    GameDescriptor(
        canonical_name="thelairsdoom",
        display_title="The Lair's Doom",
        description="Choice-driven dungeon adventure with multiple endings to avert the doom.",
        runner=play_the_lairs_doom,
        aliases=["doom", "lair", "lairsdoom", "the-lairs-doom", "adventure"],
    ),
]


# Build alias lookup map: normalized_alias -> GameDescriptor
_LOOKUP_MAP: Dict[str, GameDescriptor] = {}
for _game in GAME_REGISTRY:
    _LOOKUP_MAP[_game.canonical_name.lower()] = _game
    for _alias in _game.aliases:
        _LOOKUP_MAP[_alias.lower().replace("-", "").replace("_", "")] = _game
        _LOOKUP_MAP[_alias.lower()] = _game


def find_game(name_or_alias: str) -> Optional[GameDescriptor]:
    """
    Look up a game by canonical name or friendly alias.
    Case-insensitive, ignores hyphens and underscores.
    """
    clean_key = name_or_alias.strip().lower()
    if clean_key in _LOOKUP_MAP:
        return _LOOKUP_MAP[clean_key]

    # Also try stripped of hyphens and underscores
    simplified = clean_key.replace("-", "").replace("_", "")
    return _LOOKUP_MAP.get(simplified)


def get_all_games() -> List[GameDescriptor]:
    """Return all registered games."""
    return list(GAME_REGISTRY)


def get_random_game() -> GameDescriptor:
    """Select one of the registered games at random."""
    return random.choice(GAME_REGISTRY)


def format_unknown_game_error(attempted_name: str) -> str:
    """
    Generate a friendly, helpful error message when a requested game cannot be found.
    """
    lines = [
        f"Error: Unknown game '{attempted_name}'.",
        "\nAvailable games:",
    ]
    for game in GAME_REGISTRY:
        alias_str = ", ".join(f"'{a}'" for a in game.aliases[:3])
        lines.append(f"  • {game.canonical_name} (aliases: {alias_str})")
        lines.append(f"    {game.description}")
    lines.append("\nExample usage: mylair -s rps  or  mylair -s doom")
    return "\n".join(lines)
