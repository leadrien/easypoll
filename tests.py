from unittest import TestCase

from easypoll import quotes_to_list, get_regional_indicator_symbol


class Tests(TestCase):
    def test_quotes_to_list(self):
        s = '/poll "one two three?" "four five" "six"'
        self.assertEqual(["one two three?", "four five", "six"], quotes_to_list(s))

        s = '/poll "Yay"'
        self.assertEqual(["Yay"], quotes_to_list(s))

        s = "/poll"
        self.assertEqual([], quotes_to_list(s))

        s = ""
        self.assertEqual([], quotes_to_list(s))

        s = '/poll "  "'
        self.assertEqual([], quotes_to_list(s))

        s = '/poll one two three?" "four five" "six"'
        self.assertEqual([], quotes_to_list(s))

    def test_get_regional_indicator_symbol(self):
        self.assertEqual("🇦", get_regional_indicator_symbol(0))
        self.assertEqual("🇿", get_regional_indicator_symbol(25))
        self.assertEqual("", get_regional_indicator_symbol(26))
        self.assertEqual("", get_regional_indicator_symbol(-1))
