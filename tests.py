from unittest import TestCase

from easypoll import PollException
from easypoll import Poll


class Tests(TestCase):
    def test_poll(self):
        p1 = Poll("q1", ["one", "two", "three"])
        p2 = Poll.from_str('/poll "q1" "one" "two" "three"')
        self.assertEqual(p1, p2)

        p1 = Poll("Yay", [])
        p2 = Poll.from_str('/poll "Yay"')
        self.assertEqual(p1, p2)

        p1 = Poll(" ", [])
        p2 = Poll.from_str('/poll " "')
        self.assertEqual(p1, p2)

        p1 = Poll("", [])
        p2 = Poll.from_str('/poll ""')
        self.assertEqual(p1, p2)

        p1 = Poll("no", ["fkin", "commas", "!"])
        p2 = Poll.from_str('/poll "no", "fkin", "commas", "!"')
        self.assertEqual(p1, p2)

        self.assertRaises(PollException, Poll.from_str, "/poll")
        self.assertRaises(PollException, Poll.from_str, "")
        self.assertRaises(PollException, Poll.from_str, '/poll " " "')
        self.assertRaises(
            PollException, Poll.from_str, '/poll one two three?" "four five" "six"'
        )

    def test_get_regional_indicator_symbol(self):
        self.assertEqual("🇦", Poll.get_regional_indicator_symbol(0))
        self.assertEqual("🇿", Poll.get_regional_indicator_symbol(25))
        self.assertEqual("", Poll.get_regional_indicator_symbol(26))
        self.assertEqual("", Poll.get_regional_indicator_symbol(-1))
