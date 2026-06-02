import unittest
from main import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_strips_whitespace(self):
        self.assertEqual(extract_title("#   Hello World   "), "Hello World")

    def test_first_h1_wins(self):
        md = "# First\n\n# Second"
        self.assertEqual(extract_title(md), "First")

    def test_ignores_h2(self):
        md = "## Not a title\n\n# Real Title"
        self.assertEqual(extract_title(md), "Real Title")

    def test_no_h1_raises(self):
        with self.assertRaises(ValueError):
            extract_title("## No h1 here\n\nJust a paragraph.")

    def test_multiline_doc(self):
        md = "Some text\n\n# My Page\n\nMore content"
        self.assertEqual(extract_title(md), "My Page")


if __name__ == "__main__":
    unittest.main()
