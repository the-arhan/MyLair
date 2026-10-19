"""
Unit tests for My Lair CLI argument parsing and commands.
"""

import unittest
from mylair.cli import create_parser, run_direct_game
from mylair.games.registry import find_game, format_unknown_game_error


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.parser = create_parser()

    def test_start_command_parsing(self):
        """'start' should be captured as positional command."""
        args = self.parser.parse_args(["start"])
        self.assertEqual(args.command, "start")
        self.assertIsNone(args.direct_game)

    def test_help_command_parsing(self):
        """'help' should be captured as positional command."""
        args = self.parser.parse_args(["help"])
        self.assertEqual(args.command, "help")

    def test_direct_game_flag_parsing(self):
        """'-s rps' and '--start-game rockpaperscissor' should be parsed correctly."""
        args_short = self.parser.parse_args(["-s", "rps"])
        self.assertEqual(args_short.direct_game, "rps")

        args_long = self.parser.parse_args(["--start-game", "firsttofifty"])
        self.assertEqual(args_long.direct_game, "firsttofifty")

    def test_game_lookup_canonical_and_aliases(self):
        """All supported games should be found via canonical names and aliases."""
        test_cases = [
            ("rockpaperscissor", "rockpaperscissor"),
            ("rps", "rockpaperscissor"),
            ("rock-paper-scissors", "rockpaperscissor"),
            ("firsttofifty", "firsttofifty"),
            ("first-to-fifty", "firsttofifty"),
            ("f2f", "firsttofifty"),
            ("guessthenumber", "guessthenumber"),
            ("guess-the-number", "guessthenumber"),
            ("gtn", "guessthenumber"),
        ]
        for query, expected_canonical in test_cases:
            game = find_game(query)
            self.assertIsNotNone(game, f"Failed to look up game query: {query}")
            self.assertEqual(game.canonical_name, expected_canonical)

    def test_unknown_game_error_format(self):
        """Unknown games should generate a clear error string with available options."""
        error_msg = format_unknown_game_error("super_mario")
        self.assertIn("Unknown game 'super_mario'", error_msg)
        self.assertIn("rockpaperscissor", error_msg)
        self.assertIn("firsttofifty", error_msg)
        self.assertIn("guessthenumber", error_msg)

    def test_run_direct_game_unknown(self):
        """run_direct_game should return 1 when given an invalid game name."""
        ret = run_direct_game("nonexistent_game_xyz")
        self.assertEqual(ret, 1)

    def test_show_exit_countdown(self):
        """show_exit_countdown should display countdown and cleanly finish."""
        import io
        from unittest.mock import patch
        from mylair.display import show_exit_countdown

        out_buffer = io.StringIO()
        with patch("sys.stdout", out_buffer), patch("time.sleep", return_value=None):
            show_exit_countdown(seconds=3, color_scheme="no_color", farewell_message="Goodbye Test")

        output = out_buffer.getvalue()
        self.assertIn("Goodbye Test", output)
        self.assertIn("Quitting My Lair in 3 seconds", output)
        self.assertIn("Closing My Lair now... Goodbye!", output)


if __name__ == "__main__":
    unittest.main()
