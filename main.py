#!/usr/bin/env python3
"""
My Lair - Top-level runner.

Allows running My Lair directly from source without installation:
  python main.py start
  python main.py -s rps
  python main.py --help
"""

import sys
from pathlib import Path

# Add src/ to sys.path so mylair can be imported without pip install
SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from mylair.cli import main

if __name__ == "__main__":
    sys.exit(main())
