"""
Games package for My Lair.
"""

from mylair.games.registry import (
    GAME_REGISTRY,
    GameDescriptor,
    find_game,
    format_unknown_game_error,
    get_all_games,
    get_random_game,
)

__all__ = [
    "GAME_REGISTRY",
    "GameDescriptor",
    "find_game",
    "format_unknown_game_error",
    "get_all_games",
    "get_random_game",
]
