"""
Unit tests for My Lair game mechanics and algorithms.
"""

import unittest
from mylair.games.first_to_fifty import (
    MAX_ADD,
    MIN_ADD,
    TARGET_SCORE,
    compute_computer_move,
    render_progress_bar,
)
from mylair.games.guess_the_number import get_guess_rating
from mylair.games.rock_paper_scissors import evaluate_round


class TestGames(unittest.TestCase):
    # ==========================================================================
    # ROCK PAPER SCISSORS TESTS
    # ==========================================================================
    def test_rps_evaluate_draw(self):
        """Identical choices should result in a tie."""
        status, _ = evaluate_round("rock", "rock")
        self.assertEqual(status, "tie")
        status, _ = evaluate_round("paper", "paper")
        self.assertEqual(status, "tie")
        status, _ = evaluate_round("scissors", "scissors")
        self.assertEqual(status, "tie")

    def test_rps_evaluate_wins(self):
        """Rock beats scissors, scissors beats paper, paper beats rock."""
        status, desc = evaluate_round("rock", "scissors")
        self.assertEqual(status, "win")
        self.assertIn("crushes", desc)

        status, desc = evaluate_round("scissors", "paper")
        self.assertEqual(status, "win")
        self.assertIn("cuts", desc)

        status, desc = evaluate_round("paper", "rock")
        self.assertEqual(status, "win")
        self.assertIn("covers", desc)

    def test_rps_evaluate_losses(self):
        """Scissors loses to rock, paper loses to scissors, rock loses to paper."""
        status, _ = evaluate_round("scissors", "rock")
        self.assertEqual(status, "lose")

        status, _ = evaluate_round("paper", "scissors")
        self.assertEqual(status, "lose")

        status, _ = evaluate_round("rock", "paper")
        self.assertEqual(status, "lose")

    # ==========================================================================
    # FIRST TO FIFTY TESTS
    # ==========================================================================
    def test_f2f_computer_winning_move(self):
        """If total is 45 (within 10 of 50), computer should immediately choose 5 to win."""
        move = compute_computer_move(45)
        self.assertEqual(move, 5)

        move = compute_computer_move(49)
        self.assertEqual(move, 1)

        move = compute_computer_move(40)
        self.assertEqual(move, 10)

    def test_f2f_computer_key_target_move(self):
        """Computer should target key strategic positions (e.g., from 35, diff to 39 is 4)."""
        move = compute_computer_move(35)
        self.assertEqual(move, 4)

        move = compute_computer_move(25)
        self.assertEqual(move, 3)

    def test_f2f_computer_move_bounds(self):
        """Computer move must always be within MIN_ADD and MAX_ADD."""
        for total in range(0, TARGET_SCORE):
            move = compute_computer_move(total)
            self.assertGreaterEqual(move, MIN_ADD)
            self.assertLessEqual(move, min(MAX_ADD, TARGET_SCORE - total))

    def test_f2f_progress_bar(self):
        """Progress bar should format properly and include current/target."""
        bar = render_progress_bar(25, 50)
        self.assertIn("25/50", bar)
        self.assertIn("50%", bar)

    # ==========================================================================
    # GUESS THE NUMBER TESTS
    # ==========================================================================
    def test_gtn_ratings(self):
        """Guess rating should return friendly tiers based on attempt count."""
        self.assertIn("Legendary", get_guess_rating(3))
        self.assertIn("Excellent", get_guess_rating(6))
        self.assertIn("Good job", get_guess_rating(9))
        self.assertIn("Persistence", get_guess_rating(14))


if __name__ == "__main__":
    unittest.main()
