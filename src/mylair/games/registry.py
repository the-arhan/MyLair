"""
Game registry for My Lair.

Defines game metadata, canonical identifiers, aliases, and runner functions.
Beginners can add new games to the launcher by adding an entry in GAME_REGISTRY.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional

from mylair.games.first_to_fifty import play_first_to_fifty
from mylair.games.guess_the_number import play_guess_the_number
from mylair.games.rock_paper_scissors import play_rock_paper_scissors


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
        canonical_name="rockpaperscissor",
        display_title="Rock Paper Scissors",
        description="Classic duel of rock, paper, and scissors against the computer.",
        runner=play_rock_paper_scissors,
        aliases=["rps", "rock-paper-scissors", "rockpaperscissors", "rock_paper_scissors", "rock"],
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
    lines.append("\nExample usage: mylair -s rockpaperscissor  or  mylair -s rps")
    return "\n".join(lines)
