"""
Unit tests for My Lair game mechanics and algorithms.
"""

import unittest

from mylair.games.coin_flip_streak import evaluate_flip, flip_coin
from mylair.games.dice_duel import compare_rolls, roll_dice
from mylair.games.first_to_fifty import (
    MAX_ADD,
    MIN_ADD,
    TARGET_SCORE,
    compute_computer_move,
    render_progress_bar,
)
from mylair.games.fortune_cookie import FORTUNES, generate_lucky_numbers, pick_fortune
from mylair.games.guess_the_number import get_guess_rating
from mylair.games.higher_or_lower import compare_numbers
from mylair.games.number_lock import evaluate_guess, generate_secret_code, validate_guess
from mylair.games.odd_or_even import evaluate_odd_or_even
from mylair.games.quick_math import generate_question
from mylair.games.rock_paper_scissors import evaluate_round
from mylair.games.take_the_last import (
    compute_computer_move as nim_compute_computer_move,
    render_token_pile,
)
from mylair.games.the_8_ball import EIGHT_BALL_ANSWERS
from mylair.games.the_lairs_doom import render_status_bar
from mylair.games.word_scramble import scramble_word


class TestGames(unittest.TestCase):
    # ==========================================================================
    # ROCK PAPER SCISSORS PLUS TESTS
    # ==========================================================================
    def test_rps_evaluate_draw(self):
        """Identical choices should result in a tie."""
        status, _ = evaluate_round("rock", "rock")
        self.assertEqual(status, "tie")
        status, _ = evaluate_round("paper", "paper")
        self.assertEqual(status, "tie")
        status, _ = evaluate_round("scissors", "scissors")
        self.assertEqual(status, "tie")
        status, _ = evaluate_round("lizard", "lizard")
        self.assertEqual(status, "tie")
        status, _ = evaluate_round("spock", "spock")
        self.assertEqual(status, "tie")

    def test_rps_evaluate_wins(self):
        """Standard 3-move wins plus lizard and spock wins."""
        status, desc = evaluate_round("rock", "scissors")
        self.assertEqual(status, "win")
        self.assertIn("crushes", desc)

        status, desc = evaluate_round("scissors", "paper")
        self.assertEqual(status, "win")
        self.assertIn("cuts", desc)

        status, desc = evaluate_round("paper", "rock")
        self.assertEqual(status, "win")
        self.assertIn("covers", desc)

        # Lizard and Spock expansions
        status, desc = evaluate_round("rock", "lizard")
        self.assertEqual(status, "win")
        self.assertIn("crushes", desc)

        status, desc = evaluate_round("lizard", "spock")
        self.assertEqual(status, "win")
        self.assertIn("poisons", desc)

        status, desc = evaluate_round("spock", "scissors")
        self.assertEqual(status, "win")
        self.assertIn("smashes", desc)

        status, desc = evaluate_round("scissors", "lizard")
        self.assertEqual(status, "win")
        self.assertIn("decapitates", desc)

        status, desc = evaluate_round("lizard", "paper")
        self.assertEqual(status, "win")
        self.assertIn("eats", desc)

        status, desc = evaluate_round("paper", "spock")
        self.assertEqual(status, "win")
        self.assertIn("disproves", desc)

        status, desc = evaluate_round("spock", "rock")
        self.assertEqual(status, "win")
        self.assertIn("vaporizes", desc)

    def test_rps_evaluate_losses(self):
        """Loss outcomes correctly identified."""
        status, _ = evaluate_round("scissors", "rock")
        self.assertEqual(status, "lose")

        status, _ = evaluate_round("paper", "scissors")
        self.assertEqual(status, "lose")

        status, _ = evaluate_round("rock", "paper")
        self.assertEqual(status, "lose")

        status, _ = evaluate_round("lizard", "rock")
        self.assertEqual(status, "lose")

        status, _ = evaluate_round("spock", "lizard")
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
        """Computer should target key strategic positions."""
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

    # ==========================================================================
    # ODD OR EVEN TESTS
    # ==========================================================================
    def test_odd_or_even_evaluation(self):
        """Odd or Even should properly evaluate sum and parity."""
        won, total, parity = evaluate_odd_or_even("odd", 2, 3)
        self.assertTrue(won)
        self.assertEqual(total, 5)
        self.assertEqual(parity, "odd")

        won, total, parity = evaluate_odd_or_even("even", 2, 3)
        self.assertFalse(won)
        self.assertEqual(total, 5)
        self.assertEqual(parity, "odd")

        won, total, parity = evaluate_odd_or_even("even", 4, 4)
        self.assertTrue(won)
        self.assertEqual(total, 8)
        self.assertEqual(parity, "even")

    # ==========================================================================
    # COIN FLIP STREAK TESTS
    # ==========================================================================
    def test_coin_flip_streak_mechanics(self):
        """Coin flip helper should generate heads/tails and evaluate matches."""
        self.assertTrue(evaluate_flip("heads", "heads"))
        self.assertTrue(evaluate_flip("tails", "tails"))
        self.assertFalse(evaluate_flip("heads", "tails"))

        flip = flip_coin()
        self.assertIn(flip, ("heads", "tails"))

    # ==========================================================================
    # HIGHER OR LOWER TESTS
    # ==========================================================================
    def test_higher_or_lower_comparison(self):
        """Higher or lower should distinguish wins, losses, and ties (pushes)."""
        status, _ = compare_numbers(20, 30, "higher")
        self.assertEqual(status, "win")

        status, _ = compare_numbers(30, 20, "lower")
        self.assertEqual(status, "win")

        status, _ = compare_numbers(20, 30, "lower")
        self.assertEqual(status, "lose")

        status, _ = compare_numbers(25, 25, "higher")
        self.assertEqual(status, "push")

        status, _ = compare_numbers(25, 25, "lower")
        self.assertEqual(status, "push")

    # ==========================================================================
    # QUICK MATH TESTS
    # ==========================================================================
    def test_quick_math_generation(self):
        """Quick Math generates questions matching the requested difficulty."""
        for diff in (1, 2, 3):
            q_text, ans = generate_question(diff)
            self.assertIsInstance(q_text, str)
            self.assertIsInstance(ans, int)
            self.assertGreater(len(q_text), 3)

    # ==========================================================================
    # DICE DUEL TESTS
    # ==========================================================================
    def test_dice_duel_mechanics(self):
        """Dice Duel roll bounds and winner comparison."""
        d1, d2, total = roll_dice()
        self.assertTrue(1 <= d1 <= 6)
        self.assertTrue(1 <= d2 <= 6)
        self.assertEqual(d1 + d2, total)

        self.assertEqual(compare_rolls(10, 8), "player")
        self.assertEqual(compare_rolls(7, 9), "computer")
        self.assertEqual(compare_rolls(8, 8), "tie")

    # ==========================================================================
    # NUMBER LOCK TESTS
    # ==========================================================================
    def test_number_lock_validation_and_scoring(self):
        """Number Lock guess validation and exact/position hints."""
        secret = generate_secret_code(4)
        self.assertEqual(len(secret), 4)
        self.assertEqual(len(set(secret)), 4)

        # Validation checks
        valid, _ = validate_guess("1234", 4)
        self.assertTrue(valid)

        valid, err = validate_guess("123", 4)
        self.assertFalse(valid)
        self.assertIn("4 digits", err)

        valid, err = validate_guess("1224", 4)
        self.assertFalse(valid)
        self.assertIn("unique", err)

        valid, err = validate_guess("1204", 4)
        self.assertFalse(valid)
        self.assertIn("zeroes", err)

        # Exact and position hints
        exact, wrong_pos, misses = evaluate_guess("1234", "1234")
        self.assertEqual((exact, wrong_pos, misses), (4, 0, 0))

        exact, wrong_pos, misses = evaluate_guess("4321", "1234")
        self.assertEqual((exact, wrong_pos, misses), (0, 4, 0))

        exact, wrong_pos, misses = evaluate_guess("1567", "1234")
        self.assertEqual((exact, wrong_pos, misses), (1, 0, 3))

    # ==========================================================================
    # WORD SCRAMBLE TESTS
    # ==========================================================================
    def test_word_scramble(self):
        """Word scramble should return rearranged letters and handle duplicates."""
        word = "PYTHON"
        scrambled = scramble_word(word)
        self.assertEqual(len(scrambled), len(word))
        self.assertEqual(sorted(scrambled), sorted(word))
        self.assertNotEqual(scrambled, word)

        # Single letter fallback
        self.assertEqual(scramble_word("A"), "A")

    # ==========================================================================
    # TAKE THE LAST TESTS
    # ==========================================================================
    def test_take_the_last_logic(self):
        """Take the Last computer moves and pile rendering."""
        self.assertEqual(nim_compute_computer_move(1), 1)
        self.assertEqual(nim_compute_computer_move(2), 2)
        self.assertEqual(nim_compute_computer_move(3), 3)
        self.assertEqual(nim_compute_computer_move(5), 1)
        self.assertEqual(nim_compute_computer_move(6), 2)
        self.assertEqual(nim_compute_computer_move(7), 3)

        rendered = render_token_pile(5)
        self.assertIn("5", rendered)

    # ==========================================================================
    # FORTUNE COOKIE TESTS
    # ==========================================================================
    def test_fortune_cookie(self):
        """Fortune Cookie selections and lucky numbers generation."""
        fortune = pick_fortune()
        self.assertIn(fortune, FORTUNES)

        lucky = generate_lucky_numbers(5)
        self.assertEqual(len(lucky), 5)
        self.assertEqual(lucky, sorted(lucky))

    # ==========================================================================
    # THE 8 BALL TESTS
    # ==========================================================================
    def test_the_8_ball_answers(self):
        """The 8 Ball must contain exactly the 8 specified answers."""
        expected_8 = [
            "It is certain",
            "It is decidedly so",
            "Without a doubt",
            "Reply hazy, try again",
            "Ask again later",
            "Better not tell you now",
            "My sources say no",
            "Outlook not so good",
        ]
        self.assertEqual(len(EIGHT_BALL_ANSWERS), 8)
        self.assertEqual(sorted(EIGHT_BALL_ANSWERS), sorted(expected_8))

    # ==========================================================================
    # THE LAIR'S DOOM TESTS
    # ==========================================================================
    def test_the_lairs_doom_status_bar(self):
        """Status bar formatting for HP and items."""
        bar = render_status_bar(3, ["Torch", "Brass Key"])
        self.assertIn("♥♥♥", bar)
        self.assertIn("Torch", bar)
        self.assertIn("Brass Key", bar)


if __name__ == "__main__":
    unittest.main()
