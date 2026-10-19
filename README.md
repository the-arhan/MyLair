# My Lair (mylair)

```text
    __  ____  __   __    ___    ____ ____ 
   /  |/  /\ \/ /  / /   /   |  /  _// __ \
  / /|_/ /  \  /  / /   / /| |  / / / /_/ /
 / /  / /   / /  / /___/ ___ |_/ / / _, _/ 
/_/  /_/   /_/  /_____/_/  |_/___//_/ |_|  
```

A friendly, retro-styled command-line game launcher built for developers and terminal warriors who need quick, fun, distraction-free breaks during lengthy coding sessions.

**My Lair** runs natively across **Windows**, **macOS**, and **Linux** using **only the Python standard library** — zero external runtime dependencies required!

---

## Highlights

- **Pure Python Standard Library**: No external runtime packages needed. Zero bloat, instant startup.
- **Cross-Platform ANSI Colors & Gradients**: Smooth color gradient ASCII titles, rich color schemes, and seamless fallback for terminals that do not support color.
- **Modern CLI**: Launch the full interactive menu with `mylair start` or jump directly into any game with `mylair -s <game>`.
- **Three Complete Built-in Games**: Rock Paper Scissors, First to Fifty, and Guess the Number.
- **Random Game Mode**: Can't decide what to play? Let My Lair pick a surprise game for you.
- **Beginner-Friendly Architecture**: Clean, modular code with clear comments explaining every section, making it effortless to customize or add your own games and themes.
- **Robust Navigation**: Consistent numbered menus, graceful `b` (back) and `q` (quit) controls at input prompts, and clean `Ctrl+C` exits without tracebacks.
- **Persistent User Settings**: Customizable ASCII title styles and color schemes saved in your OS's standard configuration directory with automatic error recovery.

---

## Installation & Setup

### Requirements

- Python 3.8 or higher.

### Recommended: Install in Editable Mode

Clone or navigate to the repository directory, then install in editable mode:

```bash
# Optional: create and activate a virtual environment
python -m venv .venv

# On Windows:
.venv\Scripts\activate
# On Linux / macOS:
source .venv/bin/activate

# Install My Lair in editable mode
pip install -e .
```

Once installed, the `mylair` command becomes available anywhere in your active environment!

### Run Directly Without Installing

You can also run My Lair directly from the source repository using the included `main.py` entrypoint:

```bash
python main.py start
python main.py -s rps
python main.py --help
```

---

## Command-Line Usage

My Lair provides intuitive CLI commands and flags:

| Command | Description |
| :--- | :--- |
| `mylair start` | Opens the full interactive main menu. |
| `mylair -s <game>` | Launches a specific game directly without showing the menu. |
| `mylair --help` / `mylair -h` | Displays the command-line help flags and usage. |
| `mylair help` | Displays the command-line help message. |
| `mylair -v` / `mylair --version` | Shows the current program version. |

### Direct Game Launch Examples

Launch any game directly with its canonical name or friendly aliases:

```bash
# Rock Paper Scissors (aliases: rps, rock-paper-scissors, rock)
mylair -s rockpaperscissor
mylair -s rps

# First to Fifty (aliases: f2f, first-to-fifty, fifty)
mylair -s firsttofifty
mylair -s f2f

# Guess the Number (aliases: gtn, guess-the-number, guess)
mylair -s guessthenumber
mylair -s gtn
```

If you specify an unknown game, My Lair provides a friendly error message listing all valid games and their aliases:

```text
Error: Unknown game 'chess'.

Available games:
  • rockpaperscissor (aliases: 'rps', 'rock-paper-scissors', 'rockpaperscissors')
    Classic duel of rock, paper, and scissors against the computer.
  • firsttofifty (aliases: 'f2f', 'first-to-fifty', 'fifty')
    Tactical turn-based addition race to reach 50.
  • guessthenumber (aliases: 'gtn', 'guess-the-number', 'guess')
    Crack the secret mystery number between 1 and 100 with dynamic hints.

Example usage: mylair -s rockpaperscissor  or  mylair -s rps
```

---

## Navigation & Controls

- **Numbered Menus**: On menu screens, simply enter the number corresponding to your choice and press <kbd>Enter</kbd>.
- **Input Prompts**:
  - Enter `b` (or `B`) and press <kbd>Enter</kbd> to return to the previous screen or menu.
  - Enter `q` (or `Q`) and press <kbd>Enter</kbd> to exit cleanly to your terminal.
  - `b` and `q` are only treated as navigation actions at active input prompts, never in places where they might be unintended.
- **Clean Exit**: Press <kbd>Ctrl+C</kbd> at any point to exit cleanly with a friendly farewell and no ugly Python tracebacks.

---

## Games

### 1. Rock Paper Scissors
- **Rules**: Rock crushes Scissors, Scissors cuts Paper, Paper covers Rock.
- **Controls**: Accepts `rock`, `paper`, `scissors`, or short abbreviations `r`, `p`, `s` (case-insensitive).
- **Features**: Live score tally tracking your wins, losses, and ties across rounds.

### 2. First to Fifty
- **Rules**: A shared running total starts at 0. You and the computer take turns adding any whole number from **1 to 10** to the total. The first player to bring the total to **50 or higher** wins the match!
- **Features**:
  - Choose who goes first (Player, Computer, or random Coin Toss).
  - Visual progress bar updating in real time (`[████░░░░] 20/50 (40%)`).
  - An intelligent and understandable computer opponent that plans its moves and plays strategically without being unbeatable.

### 3. Guess the Number
- **Rules**: The computer chooses a secret mystery number between **1 and 100**. Guess the number!
- **Features**:
  - Helpful `"Too high!"` or `"Too low!"` directional feedback.
  - Active search bounds tracking (e.g. `Hint: Number is between 25 and 48`).
  - Total guess counter and performance rating upon victory (Legendary, Excellent, Good job, Persistence).
  - Graceful rejection of non-numeric or out-of-range input.

---

## Settings & Appearance

My Lair allows customizing your terminal experience:

1. **Title Styles**: Choose from 4 built-in ASCII art titles:
   - `slant`: Modern 3D angled letters (Default).
   - `block`: Bold, solid block characters.
   - `banner`: Classic arcade-style banner font.
   - `cyber`: Futuristic condensed font.

2. **Color Schemes**: Choose from multiple curated themes:
   - `neon_cyan`: Radiant cyan with violet accents (Default).
   - `retro_green`: Classic terminal green (Matrix style).
   - `sunset_amber`: Warm golden amber with fiery red accents.
   - `cyber_purple`: Synthwave magenta and neon violet.
   - `ocean_blue`: Crisp marine blue and bright sky cyan.
   - `no_color`: Plain monochrome text (ideal for strict minimalists or simple terminals).

### Configuration File Storage

Settings are saved automatically in your platform's standard configuration directory:
- **Windows**: `%APPDATA%\mylair\settings.json` (e.g. `C:\Users\<User>\AppData\Roaming\mylair\settings.json`)
- **macOS / Linux**: `~/.config/mylair/settings.json` (or `$XDG_CONFIG_HOME/mylair/settings.json`)

If the configuration file is ever missing, malformed, or edited with invalid values, My Lair automatically falls back to safe defaults without crashing.

---

## Project Structure & Architecture

```text
mylair/
├── LICENSE                     # MIT License
├── README.md                   # Project documentation & instructions
├── pyproject.toml              # Packaging metadata & console script definition
├── main.py                     # Root direct launcher script
├── src/
│   └── mylair/
│       ├── __init__.py         # Package version and docstrings
│       ├── cli.py              # CLI argument parser and direct launcher
│       ├── display.py          # ASCII titles, gradient engine, color themes, UI helpers
│       ├── menus.py            # Main menu, game menu, settings menu, credits, help
│       ├── settings.py         # Cross-platform config load/save & validation
│       └── games/
│           ├── __init__.py     # Games package export
│           ├── registry.py     # Central game catalog, aliases, random game selector
│           ├── rock_paper_scissors.py  # Rock Paper Scissors implementation
│           ├── first_to_fifty.py       # First to Fifty implementation
│           └── guess_the_number.py     # Guess the Number implementation
└── tests/
    ├── __init__.py
    ├── test_cli.py             # CLI parser and error handling tests
    ├── test_games.py           # Game mechanics and AI logic tests
    └── test_settings.py        # Settings storage, loading, and recovery tests
```

### Purpose of Each Python Module

- **`cli.py`**: Handles command-line arguments using `argparse`. Directs commands (`start`, `help`, `-s <game>`) and cleanly handles interruptions.
- **`settings.py`**: Locates the configuration directory across OSes using standard `pathlib`, loads JSON preferences, and safely handles damaged files.
- **`display.py`**: Enables Windows Virtual Terminal Processing, computes RGB gradients across multi-line ASCII banners, manages color themes, and provides the unified `prompt_input` helper.
- **`menus.py`**: Contains the interactive loops for menus (Main Menu, Games Menu, Settings Menu, Credits, and Help), handling user selections and screen flow.
- **`games/registry.py`**: The central registry linking game canonical names, titles, aliases, descriptions, and runner functions. Adding a new game here automatically exposes it to both the interactive menus and CLI flags!
- **`games/rock_paper_scissors.py`**: Implementation of the Rock-Paper-Scissors duel.
- **`games/first_to_fifty.py`**: Implementation of the First to Fifty addition race.
- **`games/guess_the_number.py`**: Implementation of the Guess the Number game.

---

## How to Customize or Add New Features (For Beginners)

### Adding a New Game
1. Create a new file in `src/mylair/games/` (e.g. `dice_duel.py`).
2. Write a function `play_dice_duel(title_style: str, color_scheme: str, direct_mode: bool) -> bool`.
3. In `src/mylair/games/registry.py`, import your runner and add a `GameDescriptor` to `GAME_REGISTRY`:
   ```python
   GameDescriptor(
       canonical_name="diceduel",
       display_title="Dice Duel",
       description="Roll against the computer to reach 100 points.",
       runner=play_dice_duel,
       aliases=["dice", "duel"],
   )
   ```
4. Your new game is now automatically accessible from the Game Menu, the Random Game selector, and the CLI flag `mylair -s diceduel`!

### Adding a New Color Scheme
1. In `src/mylair/settings.py`, add your theme name to `VALID_COLOR_SCHEMES`.
2. In `src/mylair/display.py`, add a `ColorPalette` entry to `THEMES` with your preferred RGB colors:
   ```python
   "toxic_lime": ColorPalette(
       name="toxic_lime",
       display_name="Toxic Lime",
       start_rgb=(180, 255, 0),
       end_rgb=(0, 200, 100),
       accent_rgb=(210, 255, 50),
       text_rgb=(240, 255, 230),
   ),
   ```

---

## Running the Automated Test Suite

To run all unit tests:

```bash
# Using python -m unittest:
python -c "import sys; sys.path.insert(0, 'src'); import unittest; unittest.main(module=None, argv=['unittest', 'discover', '-s', 'tests', '-v'])"
```

Or when installed in editable mode:

```bash
python -m unittest discover -s tests -v
```

---

## Troubleshooting

- **No colors displayed on Windows**:
  My Lair automatically turns on Virtual Terminal Processing via `os.system('')`. If running an older Windows console host without truecolor support, choose the `retro_green` or `no_color` theme in Settings.
- **`NO_COLOR` Environment Variable**:
  My Lair respects the [NO_COLOR standard](https://no-color.org). If `NO_COLOR` is set in your environment, all color styling will be automatically disabled.
- **Corrupted Settings**:
  If your settings file becomes unreadable, simply delete `settings.json` or select `Reset Settings to Default` from the in-game Settings menu. My Lair will recreate clean defaults automatically.

---

## Credits & License

- **Project**: My Lair
- **Author**: Arhan Ali
- **License**: [MIT License](LICENSE)
- **Built With**: Python 3 Standard Library
