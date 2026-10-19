"""
Unit tests for My Lair settings management.
"""

import json
import tempfile
import unittest
from pathlib import Path

from mylair.settings import (
    DEFAULT_SETTINGS,
    VALID_COLOR_SCHEMES,
    VALID_TITLE_STYLES,
    load_settings,
    save_settings,
    validate_settings,
)


class TestSettings(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name) / "test_settings.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_default_settings_when_file_missing(self):
        """When no config file exists, load_settings should return default configuration."""
        settings = load_settings(custom_path=self.temp_path)
        self.assertEqual(settings["title_style"], DEFAULT_SETTINGS["title_style"])
        self.assertEqual(settings["color_scheme"], DEFAULT_SETTINGS["color_scheme"])
        # It should have written the file to disk
        self.assertTrue(self.temp_path.exists())

    def test_save_and_reload_settings(self):
        """Saving custom settings and reloading them should retain the values."""
        new_settings = {
            "title_style": "official",
            "color_scheme": "retro_green",
        }
        success = save_settings(new_settings, custom_path=self.temp_path)
        self.assertTrue(success)

        loaded = load_settings(custom_path=self.temp_path)
        self.assertEqual(loaded["title_style"], "official")
        self.assertEqual(loaded["color_scheme"], "retro_green")

    def test_validate_settings_invalid_values(self):
        """Invalid keys or disallowed values should be replaced with default settings."""
        invalid_data = {
            "title_style": "nonexistent_style",
            "color_scheme": "imaginary_color",
            "extra_key": 12345,
        }
        validated = validate_settings(invalid_data)
        self.assertEqual(validated["title_style"], DEFAULT_SETTINGS["title_style"])
        self.assertEqual(validated["color_scheme"], DEFAULT_SETTINGS["color_scheme"])
        self.assertNotIn("extra_key", validated)

    def test_corrupt_json_fallback(self):
        """If settings file contains invalid JSON, load_settings should fall back to defaults without error."""
        with open(self.temp_path, "w", encoding="utf-8") as f:
            f.write("!! NOT VALID JSON {{{{")

        loaded = load_settings(custom_path=self.temp_path)
        self.assertEqual(loaded, DEFAULT_SETTINGS)


if __name__ == "__main__":
    unittest.main()
