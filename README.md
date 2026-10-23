# My Lair (mylair)

```text
 ▄▄▄▄▄ ▄▄▄▄▄  ▄▄▄▄▄ ▄▄▄▄▄  ▄▄▄▄        ▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄ ▄▄▄▄▄▄▄▄▄▄ 
█▄████▄████▄█ █████ █████ █████       █▄███████▄█ █████ █████████▄█
█▓▓▓▓▓▓▓▓▓▓▓█ █▓▓▓█ █▓▓▓█ █▓▓▓█       █▓▓▓▓▓▓▓▓▓█ █▓▓▓█ █▓▓▓▓▓▓▓▓▓█
█▒▒▒█▒▒▒█▒▒▒█ █▒▒▒█ █▒▒▒█ █▒▒▒█       █▒▒▒█▀█▒▒▒█ █▒▒▒█ █▄▄▄█▀█▒▒▒█
█░░░█░░░█░░░█ █░░░█▄█░░░█ █░░░█       █░░░█▄█░░░█ █░░░█ █░░░█▄█░░░█
█░░░█▀▀▀█░░░█ █▀▀▀▀▀▀░░░█ █░░░█ ▄▄▄▄▄ █░░░░░░░░░█ █░░░█ █░░░▀▀▀░░▄█
█▒▒▒█   █▒▒▒█ █▒▒▒█▄█▒▒▒█ █▒▒▒█▄█▒▒▒█ █▒▒▒▒▒▒▒▒▒█ █▒▒▒█ █▒▒▒█ █▒▒▒█
█▓▓▓█   █▓▓▓█ █▓▓▓▓▓▓▓▓▓█ █▓▓▓▓▓▓▓▓▓█ █▓▓▓█▀█▓▓▓█ █▓▓▓█ █▓▓▓█ █▓▓▓█
█████   █████ ███████████ ███████████ █████ █████ █████ █████ █████
 ▀▀▀▀   ▀▀▀▀▀ ▀▀▀▀▀▀▀▀▀▀▀ ▀▀▀▀▀▀▀▀▀▀▀ ▀▀▀▀▀ ▀▀▀▀▀ ▀▀▀▀▀ ▀▀▀▀▀ ▀▀▀▀▀
```

A friendly, retro-styled command-line game launcher built for developers and terminal warriors who need quick, fun, distraction-free breaks during lengthy coding sessions.

**My Lair** runs natively across **Windows**, **macOS**, and **Linux** using **only the Python standard library** — zero external runtime dependencies required!

---

## Highlights

- **Pure Python Standard Library**: No external runtime packages needed. Zero bloat, instant startup.
- **Cross-Platform ANSI Colors & Gradients**: Smooth color gradient ASCII titles, rich color schemes, and seamless fallback for terminals that do not support color.
- **Modern CLI**: Launch the full interactive menu with `mylair start` or jump directly into any game with `mylair -s <game>`.
- **14 Built-in Games & Adventures**: Puzzles, logic, strategy, arithmetic, quick-fire chance, and story-driven dungeon adventure.
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
# Rock Paper Scissors Plus (aliases: rps, rpsplus, rockpaperscissor, rock)
mylair -s rps

# First to Fifty (aliases: f2f, first-to-fifty, fifty)
mylair -s f2f

# Guess the Number (aliases: gtn, guess-the-number, guess)
mylair -s gtn

# Odd or Even (aliases: ooe, odd-or-even, odd, even)
mylair -s oddoreven

# Coin Flip Streak (aliases: cfs, coin-flip, coin, streak)
mylair -s coin

# Higher or Lower (aliases: hol, higher-or-lower, higher, lower)
mylair -s higher

# Quick Math (aliases: math, quick-math, arithmetic)
mylair -s math

# Dice Duel (aliases: dice, duel, dice-duel)
mylair -s dice

# Number Lock (aliases: lock, number-lock, vault, code)
mylair -s lock

# Word Scramble (aliases: scramble, word-scramble, words)
mylair -s scramble

# Take the Last (aliases: ttl, take-the-last, nim, tokens)
mylair -s takethelast

# Fortune Cookie (aliases: fortune, cookie, fortune-cookie)
mylair -s fortune

# The 8 Ball (aliases: 8ball, eightball, magic8ball)
mylair -s 8ball

# The Lair's Doom (aliases: doom, lair, adventure)
mylair -s doom
```

If you specify an unknown game, My Lair provides a friendly error message listing all valid games and their aliases:

```text
Error: Unknown game 'chess'.

Available games:
  • rockpaperscissorplus (aliases: 'rps', 'rockpaperscissor', 'rock-paper-scissors')
    Expanded 5-way tactical duel of Rock, Paper, Scissors, Lizard, Spock.
  • firsttofifty (aliases: 'f2f', 'first-to-fifty', 'fifty')
    Tactical turn-based addition race to reach 50.
  • guessthenumber (aliases: 'gtn', 'guess-the-number', 'guess')
    Crack the secret mystery number between 1 and 100 with dynamic hints.
  • thelairsdoom (aliases: 'doom', 'lair', 'lairsdoom')
    Choice-driven dungeon adventure with multiple endings to avert the doom.
...
Example usage: mylair -s rps  or  mylair -s doom
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

## Built-In Games

### 1. Rock Paper Scissors Plus (`rps`, `rpsplus`, `rockpaperscissor`)
- **Rules**: The classic 5-element duel (Rock, Paper, Scissors, Lizard, Spock).
  - Rock crushes Scissors & Lizard.
  - Paper covers Rock & disproves Spock.
  - Scissors cuts Paper & decapitates Lizard.
  - Lizard poisons Spock & eats Paper.
  - Spock smashes Scissors & vaporizes Rock.
- **Controls**: Accepts `rock` (`r`), `paper` (`p`), `scissors` (`s` / `sc`), `lizard` (`l` / `liz`), and `spock` (`k` / `sp`).
- **Features**: Live score tally, in-game rules reference, and detailed outcome descriptions.

### 2. First to Fifty (`f2f`, `first-to-fifty`, `fifty`)
- **Rules**: A shared running total starts at 0. You and the computer take turns adding any whole number from **1 to 10** to the total. The first player to bring the total to **50 or higher** wins!
- **Features**: Real-time progress bar (`[████░░░░] 20/50 (40%)`), starter selection (Player, Computer, Coin Toss), and a strategic computer opponent.

### 3. Guess the Number (`gtn`, `guess-the-number`, `guess`)
- **Rules**: The computer picks a secret mystery number between **1 and 100**.
- **Features**: Directional `"Too high!"` or `"Too low!"` feedback, dynamic search range tracking (`Hint: Number is between 25 and 48`), and performance ratings (Legendary, Excellent, Good job, Persistence).

### 4. Odd or Even (`oddoreven`, `ooe`, `odd`, `even`)
- **Rules**: Predict whether the combined sum of two numbers will be **ODD** (`o`) or **EVEN** (`e`). Choose your number (1-5); the computer also picks (1-5). Both numbers are added together. If the sum's parity matches your prediction, you win!
- **Features**: Session win/loss tracking, clear rules distinguishing parity prediction from number choice.

### 5. Coin Flip Streak (`coinflipstreak`, `cfs`, `coin`, `streak`)
- **Rules**: Predict Heads (`h`) or Tails (`t`) for each flip. Each correct call increases your current streak by 1.
- **Features**: Choose to **Continue** risking or **Stop** and bank your streak. Wrong calls reset the streak to 0. Tracks session Best Streak.

### 6. Higher or Lower (`higherorlower`, `hol`, `higher`, `lower`)
- **Rules**: A number between 1 and 50 is revealed. Predict whether the next number will be Higher (`h`) or Lower (`l`).
- **Equal Rule**: If the next number equals the current number, it is a **Push** (tie) without penalty.
- **Features**: 5-turn rounds with final accuracy rating.

### 7. Quick Math (`quickmath`, `math`, `arithmetic`)
- **Rules**: Solve 5 casual arithmetic problems under a turn-limit casual format.
- **Difficulty Modes**: Easy (1-20 addition/subtraction), Medium (up to 50 + single-digit multiplication), Hard (up to 100 + tables up to 12×12).
- **Features**: Non-numeric inputs are rejected without consuming attempts. Displays final score percentage and encouragement.

### 8. Dice Duel (`diceduel`, `dice`, `duel`)
- **Rules**: Both player and computer roll two 6-sided dice (2d6). Highest total wins. Ties are handled as ties.
- **Modes**: Quick Duel (single round), Best-of-3 Series, and Best-of-5 Series.
- **Features**: Visual bracketed dice representations and live series scoring.

### 9. Number Lock (`numberlock`, `lock`, `code`, `vault`)
- **Rules**: Deduce a secret 4-digit code using unique digits 1-9 in 8 attempts. No repeated digits are allowed.
- **Hints**: Exact match (🟢), Wrong position (🟡), and Miss (⚪).
- **Features**: Guess history table displayed every turn. Invalid guesses (wrong length, non-digits, duplicates) are rejected without consuming an attempt.

### 10. Word Scramble (`wordscramble`, `scramble`, `words`)
- **Rules**: Unscramble retro, gaming, and tech words in 3 attempts.
- **Features**: Guaranteed non-identical scrambling, sensible handling of repeated letters, and an optional free clue by typing `hint` or `?`.

### 11. Take the Last (`takethelast`, `ttl`, `nim`, `tokens`)
- **Rules**: A pile of 15 tokens starts on the table. Players take turns removing 1, 2, or 3 tokens.
- **Winning Condition**: The player who takes the **very last token WINS**!
- **Features**: Visual token pile display, starter selection, and an intelligent computer opponent that explains its move.

### 12. Fortune Cookie (`fortunecookie`, `fortune`, `cookie`)
- **Rules**: Choose from 5 handcrafted fortune cookies to crack open.
- **Features**: 20+ varied, friendly, lighthearted fortunes, lucky number generator (5 sorted numbers 1-99), and ASCII cracking cookie animation. For playful entertainment only!

### 13. The 8 Ball (`the8ball`, `8ball`, `magic8ball`)
- **Rules**: Ask any question and watch the terminal-friendly 8-ball concentration effect.
- **Classic Answers**: Randomly picks one of eight classic answers (*It is certain*, *It is decidedly so*, *Without a doubt*, *Reply hazy, try again*, *Ask again later*, *Better not tell you now*, *My sources say no*, *Outlook not so good*).
- **Features**: ASCII 8-ball viewport display. Safe, skippable terminal animation.

### 14. The Lair's Doom (`thelairsdoom`, `doom`, `adventure`)
- **Rules**: A replayable choice-based terminal dungeon crawler.
- **Story**: Explore the Vestibule, Sunken Library, and Crystal Chasm to reach the unstable Doom Core.
- **Features**: Tracks Health (`HP: [♥♥♥]`) and Inventory (`[Torch, Brass Key, Crystal Gem]`). Multiple endings including *Master of the Lair*, *The Great Escape*, *Survivor's Luck*, and *Retreat & Regroup*.

---

## Settings & Appearance

My Lair allows customizing your terminal experience:

1. **Official Logo**: The exclusive retro shaded block ASCII banner (`MY LAIR`) is the official logo.
2. **Color Schemes**: Choose from multiple curated themes:
   - `synthwave`: Synthwave Magenta & Electric Cyan (Official Primary Theme).
   - `retro_green`: Classic terminal green (Matrix style).
   - `sunset_amber`: Warm golden amber with fiery red accents.
   - `cyber_purple`: Cyberpunk neon violet.
   - `ocean_blue`: Crisp marine blue and bright sky cyan.
   - `no_color`: Plain monochrome text (ideal for strict minimalists or simple terminals).

### Configuration File Storage

Settings are saved automatically in your platform's standard configuration directory:
- **Windows**: `%APPDATA%\mylair\settings.json`
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
│           ├── rock_paper_scissors.py  # Rock Paper Scissors Plus (RPSLS)
│           ├── first_to_fifty.py       # First to Fifty addition race
│           ├── guess_the_number.py     # Guess the Number binary search
│           ├── odd_or_even.py          # Odd or Even parity duel
│           ├── coin_flip_streak.py     # Coin Flip Streak prediction
│           ├── higher_or_lower.py      # Higher or Lower forecast
│           ├── quick_math.py           # Quick Math arithmetic challenge
│           ├── dice_duel.py            # Dice Duel 2d6 rolling series
│           ├── number_lock.py          # Number Lock vault deduction
│           ├── word_scramble.py        # Word Scramble puzzle
│           ├── take_the_last.py        # Take the Last Nim strategy
│           ├── fortune_cookie.py       # Fortune Cookie & lucky numbers
│           ├── the_8_ball.py           # The Mystic 8 Ball oracle
│           └── the_lairs_doom.py       # The Lair's Doom dungeon adventure
└── tests/
    ├── __init__.py
    ├── test_cli.py             # CLI parser, routing, and alias lookup tests
    ├── test_games.py           # Game mechanics, AI logic, and outcome tests
    └── test_settings.py        # Settings storage, loading, and recovery tests
```

---

## Running the Automated Test Suite

To run all unit tests:

```bash
# Using pytest:
pytest

# Or using standard python unittest:
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
