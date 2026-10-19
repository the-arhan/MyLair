"""
Settings module for My Lair.

This module handles loading, validating, and saving user preferences
(such as ASCII title styles and color schemes).

Settings are stored in the user's standard configuration directory:
- Windows: %APPDATA%/mylair/settings.json
- macOS/Linux: ~/.config/mylair/settings.json (or $XDG_CONFIG_HOME/mylair/settings.json)

Beginners:
- To add a new title style, add its identifier to VALID_TITLE_STYLES below.
- To add a new color scheme, add its identifier to VALID_COLOR_SCHEMES below.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict

# ==============================================================================
# AVAILABLE STYLES & COLOR SCHEMES
# (Add your custom styles and color themes here!)
# ==============================================================================

VALID_TITLE_STYLES = (
    "slant",   # Modern angled 3D ASCII letters
    "block",   # Bold, solid block ASCII art
    "banner",  # Classic wide arcade banner font
    "cyber",   # Sleek, futuristic condensed font
)

VALID_COLOR_SCHEMES = (
    "neon_cyan",     # Radiant cyan with purple accents
    "retro_green",   # Classic terminal matrix green
    "sunset_amber",  # Warm golden amber and deep red
    "cyber_purple",  # Synthwave magenta and violet
    "ocean_blue",    # Crisp cool blue and sky cyan
    "no_color",      # Monochrome plain text (for strict minimalists or simple terminals)
)

# Default configuration applied on fresh installs or corrupted configs
DEFAULT_SETTINGS: Dict[str, str] = {
    "title_style": "slant",
    "color_scheme": "neon_cyan",
}


# ==============================================================================
# CONFIGURATION PATH RESOLUTION
# ==============================================================================

def get_config_dir() -> Path:
    """
    Return the cross-platform directory where My Lair config files live.

    - On Windows, uses %APPDATA%/mylair (usually C:/Users/<User>/AppData/Roaming/mylair).
    - On Linux/macOS, uses $XDG_CONFIG_HOME/mylair or ~/.config/mylair.
    """
    if os.name == "nt":
        # Windows standard config path
        appdata = os.environ.get("APPDATA")
        if appdata:
            base_dir = Path(appdata)
        else:
            base_dir = Path.home() / "AppData" / "Roaming"
    else:
        # Linux & macOS standard config path
        xdg_config = os.environ.get("XDG_CONFIG_HOME")
        if xdg_config:
            base_dir = Path(xdg_config)
        else:
            base_dir = Path.home() / ".config"

    config_dir = base_dir / "mylair"
    return config_dir


def get_config_file_path() -> Path:
    """Return the absolute path to settings.json."""
    return get_config_dir() / "settings.json"


# ==============================================================================
# LOADING & SAVING SETTINGS
# ==============================================================================

def validate_settings(data: Any) -> Dict[str, str]:
    """
    Ensure the settings dictionary contains valid keys and allowed values.
    Falls back to sensible defaults for any missing or invalid entries.
    """
    validated = dict(DEFAULT_SETTINGS)

    if not isinstance(data, dict):
        return validated

    title_style = data.get("title_style")
    if isinstance(title_style, str) and title_style in VALID_TITLE_STYLES:
        validated["title_style"] = title_style

    color_scheme = data.get("color_scheme")
    if isinstance(color_scheme, str) and color_scheme in VALID_COLOR_SCHEMES:
        validated["color_scheme"] = color_scheme

    return validated


def load_settings(custom_path: Path | None = None) -> Dict[str, str]:
    """
    Load settings from disk.

    If the settings file is missing, malformed, or has invalid data,
    this returns the default settings without crashing.
    """
    config_path = custom_path or get_config_file_path()

    if not config_path.is_file():
        # First-time run: create default settings file
        save_settings(DEFAULT_SETTINGS, custom_path=config_path)
        return dict(DEFAULT_SETTINGS)

    try:
        with open(config_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return validate_settings(data)
    except (json.JSONDecodeError, OSError, UnicodeDecodeError):
        # File is damaged or inaccessible; fall back safely to defaults
        return dict(DEFAULT_SETTINGS)


def save_settings(settings: Dict[str, str], custom_path: Path | None = None) -> bool:
    """
    Save the given settings dictionary to settings.json.
    Returns True if successful, False otherwise.
    """
    config_path = custom_path or get_config_file_path()
    validated = validate_settings(settings)

    try:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        # Write atomically using a temporary file or direct write
        with open(config_path, "w", encoding="utf-8") as file:
            json.dump(validated, file, indent=4)
        return True
    except OSError:
        return False
