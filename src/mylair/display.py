"""
Display and styling engine for My Lair.

Provides:
- Multiple ASCII art title designs for 'MY LAIR'
- Terminal color support detection and Windows Virtual Terminal initialization
- Gradient coloring across multi-line ASCII banners
- Consistent color palettes and theme helpers
- Navigation prompt helper supporting 'b' (back) and 'q' (quit)
"""

from __future__ import annotations

import enum
import os
import shutil
import sys
import time
from typing import Dict, List, Optional, Tuple

# ==============================================================================
# WINDOWS VIRTUAL TERMINAL SETUP
# ==============================================================================

def enable_windows_ansi() -> bool:
    """
    Enable ANSI escape sequences on Windows 10/11 consoles.
    Calling os.system('') toggles the console into Virtual Terminal Processing mode.
    """
    if os.name == "nt":
        try:
            # os.system('') invokes cmd.exe and enables VT mode in modern Windows
            os.system("")
            return True
        except Exception:
            return False
    return True


_ANSI_INITIALIZED = enable_windows_ansi()


def supports_color() -> bool:
    """
    Check if the current terminal environment supports color display.
    Respects NO_COLOR standard (https://no-color.org) and checks isatty.
    """
    if "NO_COLOR" in os.environ:
        return False
    if not hasattr(sys.stdout, "isatty") or not sys.stdout.isatty():
        return False
    if os.environ.get("TERM") == "dumb":
        return False
    return True


# ==============================================================================
# COLOR PALETTES & THEMES
# ==============================================================================

class ColorPalette:
    """Represents RGB and ANSI colors for a theme."""
    def __init__(
        self,
        name: str,
        display_name: str,
        start_rgb: Tuple[int, int, int],
        end_rgb: Tuple[int, int, int],
        accent_rgb: Tuple[int, int, int],
        text_rgb: Tuple[int, int, int],
        success_rgb: Tuple[int, int, int] = (80, 220, 120),
        warning_rgb: Tuple[int, int, int] = (255, 190, 60),
        error_rgb: Tuple[int, int, int] = (255, 80, 80),
    ):
        self.name = name
        self.display_name = display_name
        self.start_rgb = start_rgb
        self.end_rgb = end_rgb
        self.accent_rgb = accent_rgb
        self.text_rgb = text_rgb
        self.success_rgb = success_rgb
        self.warning_rgb = warning_rgb
        self.error_rgb = error_rgb


THEMES: Dict[str, ColorPalette] = {
    "synthwave": ColorPalette(
        name="synthwave",
        display_name="Synthwave Magenta (Official)",
        start_rgb=(255, 45, 185),    # Vibrant Magenta (\033[0;35m, \033[0;95m)
        end_rgb=(0, 230, 255),       # Electric Cyan (\033[46m)
        accent_rgb=(255, 60, 215),   # Bright Magenta accent
        text_rgb=(245, 245, 255),    # Crisp White text (\033[0;97m)
        success_rgb=(0, 255, 175),   # Neon Mint/Cyan
        warning_rgb=(255, 205, 50),  # Bright Gold
        error_rgb=(255, 60, 110),    # Neon Coral/Red
    ),
    "retro_green": ColorPalette(
        name="retro_green",
        display_name="Retro Matrix Green",
        start_rgb=(50, 255, 90),
        end_rgb=(0, 160, 40),
        accent_rgb=(80, 255, 120),
        text_rgb=(210, 255, 220),
    ),
    "sunset_amber": ColorPalette(
        name="sunset_amber",
        display_name="Sunset Amber",
        start_rgb=(255, 175, 40),
        end_rgb=(255, 60, 80),
        accent_rgb=(255, 190, 60),
        text_rgb=(255, 240, 225),
    ),
    "cyber_purple": ColorPalette(
        name="cyber_purple",
        display_name="Cyberpunk Violet",
        start_rgb=(180, 40, 255),
        end_rgb=(70, 30, 230),
        accent_rgb=(200, 80, 255),
        text_rgb=(240, 230, 255),
    ),
    "ocean_blue": ColorPalette(
        name="ocean_blue",
        display_name="Ocean Wave Blue",
        start_rgb=(0, 195, 255),
        end_rgb=(30, 80, 230),
        accent_rgb=(90, 215, 255),
        text_rgb=(220, 240, 255),
    ),
    "no_color": ColorPalette(
        name="no_color",
        display_name="Plain Monochrome (No Color)",
        start_rgb=(255, 255, 255),
        end_rgb=(255, 255, 255),
        accent_rgb=(255, 255, 255),
        text_rgb=(255, 255, 255),
    ),
}

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
ITALIC = "\033[3m"


def rgb_to_ansi(r: int, g: int, b: int) -> str:
    """Format an RGB tuple as a 24-bit truecolor ANSI foreground code."""
    return f"\033[38;2;{r};{g};{b}m"


def colorize(text: str, rgb: Tuple[int, int, int], scheme_name: str = "synthwave") -> str:
    """Apply RGB color to text if colors are supported and enabled."""
    if scheme_name == "no_color" or not supports_color():
        return text
    return f"{rgb_to_ansi(*rgb)}{text}{RESET}"


def style_text(text: str, scheme_name: str, color_type: str = "text", bold: bool = False) -> str:
    """Convenient styling helper according to the active theme."""
    if scheme_name == "no_color" or not supports_color():
        return text

    palette = THEMES.get(scheme_name, THEMES["synthwave"])
    if color_type == "accent":
        code = rgb_to_ansi(*palette.accent_rgb)
    elif color_type == "start":
        code = rgb_to_ansi(*palette.start_rgb)
    elif color_type == "end":
        code = rgb_to_ansi(*palette.end_rgb)
    elif color_type == "success":
        code = rgb_to_ansi(*palette.success_rgb)
    elif color_type == "warning":
        code = rgb_to_ansi(*palette.warning_rgb)
    elif color_type == "error":
        code = rgb_to_ansi(*palette.error_rgb)
    else:
        code = rgb_to_ansi(*palette.text_rgb)

    weight = BOLD if bold else ""
    return f"{weight}{code}{text}{RESET}"


# ==============================================================================
# OFFICIAL MY LAIR RETRO SHADED ASCII LOGO
# (Official and only logo for My Lair)
# ==============================================================================

OFFICIAL_LOGO_COLORED: List[str] = [
    "\033[0;37m \033[0;35m▄▄▄▄▄\033[0;37m \033[0;35m▄▄▄▄▄\033[0;37m  \033[0;35m▄▄▄▄▄\033[0;37m \033[0;35m▄▄▄▄▄\033[0;37m  \033[0;35m▄▄▄▄\033[0;37m        \033[0;35m▄▄▄▄▄▄▄▄▄\033[0;37m  \033[0;35m▄▄▄▄▄\033[0;37m \033[0;35m▄▄▄▄▄▄▄▄▄▄\033[0;37m \033[0m",
    "\033[0;35m█\033[0;97;47m▄\033[0;97;46m███\033[0;97m█\033[0;97;45m▄\033[0;97;46m████\033[0;97;47m▄\033[0;35m█\033[0;37m \033[0;35m█\033[0;97;46m███\033[0;35m█\033[0;37m \033[0;35m█\033[0;97;46m███\033[0;35m█\033[0;37m \033[0;35m█\033[0;97m█\033[0;97;46m██\033[0;35m█\033[0;37m       \033[0;35m█\033[0;97;47m▄\033[0;97;46m███████\033[0;97;47m▄\033[0;35m█\033[0;37m \033[0;35m█\033[0;97m███\033[0;35m█\033[0;37m \033[0;35m█\033[0;97;46m████████\033[0;97;47m▄\033[0;35m█\033[0m",
    "\033[0;35m█\033[0;97;46m▓▓▓▓▓▓▓▓▓▓▓\033[0;35m█\033[0;37m \033[0;35m█\033[0;97;46m▓▓▓\033[0;35m█\033[0;37m \033[0;35m█\033[0;97;46m▓▓▓\033[0;35m█\033[0;37m \033[0;35m█\033[0;97;46m▓▓▓\033[0;35m█\033[0;37m       \033[0;35m█\033[0;97;46m▓▓▓▓▓▓▓▓▓\033[0;35m█\033[0;37m \033[0;35m█\033[0;97;46m▓▓▓\033[0;35m█\033[0;37m \033[0;35m█\033[0;97;46m▓▓▓▓▓▓▓▓▓\033[0;35m█\033[0m",
    "\033[0;35m█\033[0;97;46m▒▒▒\033[0;35m█\033[0;97;46m▒▒▒\033[0;35m█\033[0;97;46m▒▒▒\033[0;35m█\033[0;37m \033[0;35m█\033[0;97;46m▒▒▒\033[0;35m█\033[0;37m \033[0;35m█\033[0;97;46m▒▒▒\033[0;35m█\033[0;37m \033[0;35m█\033[0;97;46m▒▒▒\033[0;35m█\033[0;37m       \033[0;35m█\033[0;97;46m▒▒▒\033[0;35m█▀█\033[0;97;46m▒▒▒\033[0;35m█\033[0;37m \033[0;35m█\033[0;97;46m▒▒▒\033[0;35m█\033[0;37m \033[0;35m█\033[0;37;45m▄▄▄\033[0;35m█▀█\033[0;97;46m▒▒▒\033[0;35m█\033[0m",
    "\033[0;35m█\033[0;97;46m░░░\033[0;35m█\033[0;97;46m░░░\033[0;35m█\033[0;97;46m░░░\033[0;35m█\033[0;37m \033[0;35m█\033[0;97;46m░░░\033[0;35m█▄█\033[0;97;46m░░░\033[0;35m█\033[0;37m \033[0;35m█\033[0;97;46m░░░\033[0;35m█\033[0;37m       \033[0;35m█\033[0;97;46m░░░\033[0;35m█▄█\033[0;97;46m░░░\033[0;35m█\033[0;37m \033[0;35m█\033[0;97;46m░░░\033[0;35m█\033[0;37m \033[0;35m█\033[0;97;46m░░░\033[0;35m█▄█\033[0;97;46m░░░\033[0;35m█\033[0m",
    "\033[0;35m█\033[0;95;47m░░░\033[0;35m█▀▀▀█\033[0;95;47m░░░\033[0;35m█\033[0;37m \033[0;35m█\033[0;37;45m▀▀▀▀▀▀\033[0;95;47m░░░\033[0;35m█\033[0;37m \033[0;35m█\033[0;95;47m░░░\033[0;35m█\033[0;37m \033[0;35m▄▄▄▄▄\033[0;37m \033[0;35m█\033[0;95;47m░░░░░░░░░\033[0;35m█\033[0;37m \033[0;35m█\033[0;95;47m░░░\033[0;35m█\033[0;37m \033[0;35m█\033[0;95;47m░░░\033[0;37;45m▀▀▀\033[0;95;47m░░\033[0;37;45m▄\033[0;35m█\033[0m",
    "\033[0;35m█\033[0;95;47m▒▒▒\033[0;35m█\033[0;37m   \033[0;35m█\033[0;95;47m▒▒▒\033[0;35m█\033[0;37m \033[0;35m█\033[0;95;47m▒▒▒\033[0;35m█▄█\033[0;95;47m▒▒▒\033[0;35m█\033[0;37m \033[0;35m█\033[0;95;47m▒▒▒\033[0;35m█▄█\033[0;95;47m▒▒▒\033[0;35m█\033[0;37m \033[0;35m█\033[0;95;47m▒▒▒▒▒▒▒▒▒\033[0;35m█\033[0;37m \033[0;35m█\033[0;95;47m▒▒▒\033[0;35m█\033[0;37m \033[0;35m█\033[0;95;47m▒▒▒\033[0;35m█\033[0;37m \033[0;35m█\033[0;95;47m▒▒▒\033[0;35m█\033[0m",
    "\033[0;35m█\033[0;95;47m▓▓▓\033[0;35m█\033[0;37m   \033[0;35m█\033[0;95;47m▓▓▓\033[0;35m█\033[0;37m \033[0;35m█\033[0;95;47m▓▓▓▓▓▓▓▓▓\033[0;35m█\033[0;37m \033[0;35m█\033[0;95;47m▓▓▓▓▓▓▓▓▓\033[0;35m█\033[0;37m \033[0;35m█\033[0;95;47m▓▓▓\033[0;35m█▀█\033[0;95;47m▓▓▓\033[0;35m█\033[0;37m \033[0;35m█\033[0;95;47m▓▓▓\033[0;35m█\033[0;37m \033[0;35m█\033[0;95;47m▓▓▓\033[0;35m█\033[0;37m \033[0;35m█\033[0;95;47m▓▓▓\033[0;35m█\033[0m",
    "\033[0;35m█\033[0;95m█\033[0;95;47m█\033[0;95m█\033[0;35m█\033[0;37m   \033[0;35m█\033[0;95;47m██\033[0;95m█\033[0;35m█\033[0;37m \033[0;35m█\033[0;95;47m████████\033[0;95m█\033[0;35m█\033[0;37m \033[0;35m█\033[0;95m█\033[0;95;47m██\033[0;95m██████\033[0;35m█\033[0;37m \033[0;35m█\033[0;95;47m███\033[0;35m█\033[0;37m \033[0;35m█\033[0;95;47m███\033[0;35m█\033[0;37m \033[0;35m█\033[0;95;47m███\033[0;35m█\033[0;37m \033[0;35m█\033[0;95;47m██\033[0;95m█\033[0;35m█\033[0;37m \033[0;35m█\033[0;95;47m██\033[0;95m█\033[0;35m█\033[0m",
    "\033[0;37m \033[0;35m▀▀▀▀\033[0;37m   \033[0;35m▀▀▀▀▀\033[0;37m \033[0;35m▀▀▀▀▀▀▀▀▀▀▀\033[0;37m \033[0;35m▀▀▀▀▀▀▀▀▀▀▀\033[0;37m \033[0;35m▀▀▀▀▀\033[0;37m \033[0;35m▀▀▀▀▀\033[0;37m \033[0;35m▀▀▀▀▀\033[0;37m \033[0;35m▀▀▀▀▀\033[0;37m \033[0;35m▀▀▀▀▀\033[0m",
]

OFFICIAL_LOGO_PLAIN: List[str] = [
    " ▄▄▄▄▄ ▄▄▄▄▄  ▄▄▄▄▄ ▄▄▄▄▄  ▄▄▄▄        ▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄ ▄▄▄▄▄▄▄▄▄▄ ",
    "█▄████▄████▄█ █████ █████ █████       █▄███████▄█ █████ █████████▄█",
    "█▓▓▓▓▓▓▓▓▓▓▓█ █▓▓▓█ █▓▓▓█ █▓▓▓█       █▓▓▓▓▓▓▓▓▓█ █▓▓▓█ █▓▓▓▓▓▓▓▓▓█",
    "█▒▒▒█▒▒▒█▒▒▒█ █▒▒▒█ █▒▒▒█ █▒▒▒█       █▒▒▒█▀█▒▒▒█ █▒▒▒█ █▄▄▄█▀█▒▒▒█",
    "█░░░█░░░█░░░█ █░░░█▄█░░░█ █░░░█       █░░░█▄█░░░█ █░░░█ █░░░█▄█░░░█",
    "█░░░█▀▀▀█░░░█ █▀▀▀▀▀▀░░░█ █░░░█ ▄▄▄▄▄ █░░░░░░░░░█ █░░░█ █░░░▀▀▀░░▄█",
    "█▒▒▒█   █▒▒▒█ █▒▒▒█▄█▒▒▒█ █▒▒▒█▄█▒▒▒█ █▒▒▒▒▒▒▒▒▒█ █▒▒▒█ █▒▒▒█ █▒▒▒█",
    "█▓▓▓█   █▓▓▓█ █▓▓▓▓▓▓▓▓▓█ █▓▓▓▓▓▓▓▓▓█ █▓▓▓█▀█▓▓▓█ █▓▓▓█ █▓▓▓█ █▓▓▓█",
    "█████   █████ ███████████ ███████████ █████ █████ █████ █████ █████",
    " ▀▀▀▀   ▀▀▀▀▀ ▀▀▀▀▀▀▀▀▀▀▀ ▀▀▀▀▀▀▀▀▀▀▀ ▀▀▀▀▀ ▀▀▀▀▀ ▀▀▀▀▀ ▀▀▀▀▀ ▀▀▀▀▀",
]

ASCII_TITLES: Dict[str, List[str]] = {
    "official": OFFICIAL_LOGO_PLAIN,
}


def render_title_gradient(style: str = "official", scheme: str = "synthwave") -> str:
    """
    Render the official MY LAIR retro shaded block logo.
    If scheme is 'synthwave' (the official primary palette), uses the authentic
    multi-colored ANSI block shading.
    If scheme is 'no_color' or colors are not supported, renders the clean plain text logo.
    Otherwise, applies the selected theme's vertical gradient across the official logo.
    """
    if scheme == "no_color" or not supports_color():
        return "\n".join(OFFICIAL_LOGO_PLAIN)

    if scheme == "synthwave":
        return "\n".join(OFFICIAL_LOGO_COLORED)

    # User selected an alternative theme (e.g. retro_green, sunset_amber)
    palette = THEMES.get(scheme, THEMES["synthwave"])
    r1, g1, b1 = palette.start_rgb
    r2, g2, b2 = palette.end_rgb

    num_lines = max(len(OFFICIAL_LOGO_PLAIN) - 1, 1)
    colored_lines: List[str] = []

    for i, line in enumerate(OFFICIAL_LOGO_PLAIN):
        fraction = i / num_lines
        curr_r = int(r1 + (r2 - r1) * fraction)
        curr_g = int(g1 + (g2 - g1) * fraction)
        curr_b = int(b1 + (b2 - b1) * fraction)
        colored_lines.append(f"{BOLD}{rgb_to_ansi(curr_r, curr_g, curr_b)}{line}{RESET}")

    return "\n".join(colored_lines)


# ==============================================================================
# UI FORMATTING & NAVIGATION HELPERS
# ==============================================================================

class NavigationAction(enum.Enum):
    """Signals for navigation control flow during user input."""
    BACK = "back"
    QUIT = "quit"


def clear_screen() -> None:
    """
    Clear the terminal cleanly across Windows, macOS, and Linux.
    Used selectively to keep the screen organized without losing context.
    """
    if os.name == "nt":
        os.system("cls")
    else:
        # Standard Unix clear
        os.system("clear")


def get_terminal_width(default: int = 70) -> int:
    """Return the terminal width, clamped to a reasonable range."""
    try:
        width = shutil.get_terminal_size().columns
        return max(50, min(width, 100))
    except Exception:
        return default


def print_divider(scheme: str = "synthwave", char: str = "─") -> None:
    """Print an adaptive horizontal divider line matching the official logo width."""
    width = max(min(get_terminal_width(), 66), 66)
    line = char * width
    if scheme != "no_color" and supports_color():
        palette = THEMES.get(scheme, THEMES["synthwave"])
        print(f"{DIM}{rgb_to_ansi(*palette.accent_rgb)}{line}{RESET}")
    else:
        print(line)


def print_header(title_style: str, color_scheme: str, subtitle: Optional[str] = None) -> None:
    """
    Print the top header banner with the ASCII title, divider, and optional subtitle.
    """
    print()
    print(render_title_gradient(style=title_style, scheme=color_scheme))
    print_divider(scheme=color_scheme)
    if subtitle:
        styled_sub = style_text(f"  {subtitle}", color_scheme, color_type="accent", bold=True)
        print(styled_sub)
        print_divider(scheme=color_scheme)
    print()


def prompt_input(
    prompt_msg: str = "Select an option: ",
    color_scheme: str = "synthwave",
    allow_back: bool = True,
    allow_quit: bool = True,
) -> str | NavigationAction:
    """
    Unified input prompt that safely intercepts 'b' (back), 'q' (quit),
    and keyboard interrupts (Ctrl+C).

    Returns:
    - NavigationAction.BACK if user enters 'b' or 'B' (when allow_back=True)
    - NavigationAction.QUIT if user enters 'q' or 'Q' (when allow_quit=True)
    - The raw stripped string otherwise
    """
    styled_prompt = style_text(prompt_msg, color_scheme, color_type="text", bold=True)
    try:
        raw = input(styled_prompt).strip(" \t\r\n\ufeff\ufffe")
    except (KeyboardInterrupt, EOFError):
        # Treat interrupt or EOF as a clean quit signal
        return NavigationAction.QUIT

    lowered = raw.lower()
    if allow_back and lowered == "b":
        return NavigationAction.BACK
    if allow_quit and lowered == "q":
        return NavigationAction.QUIT

    return raw


def pause_prompt(color_scheme: str = "synthwave", msg: str = "Press Enter to return...") -> None:
    """Pause execution until the user presses Enter."""
    styled_msg = style_text(f"\n{msg}", color_scheme, color_type="accent")
    try:
        input(styled_msg)
    except (KeyboardInterrupt, EOFError):
        pass


def show_exit_countdown(
    seconds: int = 3,
    color_scheme: str = "synthwave",
    farewell_message: str = "Thank you for visiting My Lair. Happy coding!",
) -> None:
    """
    Display a farewell message and a 3-second countdown before cleanly returning to the shell.
    Allows user to press Ctrl+C to skip the countdown and exit immediately.
    """
    clear_screen()
    print(style_text(f"{farewell_message}\n", color_scheme, color_type="accent", bold=True))
    try:
        for remaining in range(seconds, 0, -1):
            unit = "second" if remaining == 1 else "seconds"
            countdown_msg = f"  Quitting My Lair in {remaining} {unit}... (Ctrl+C to quit instantly)"
            sys.stdout.write("\r" + style_text(countdown_msg, color_scheme, color_type="text"))
            sys.stdout.flush()
            time.sleep(1.0)
        sys.stdout.write("\r" + style_text("  Closing My Lair now... Goodbye!                     \n\n", color_scheme, color_type="accent"))
        sys.stdout.flush()
    except (KeyboardInterrupt, EOFError):
        sys.stdout.write("\n\nGoodbye!\n")
        sys.stdout.flush()

