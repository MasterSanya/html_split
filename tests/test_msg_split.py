import unittest
from src.msg_split import split_html_message


class TestSplitMessage(unittest.TestCase):
    """Unit tests for the split_html_message function"""

    def test_basic_split(self):
        """Test basic splitting with a small message"""
        html = "<p>" + "a" * 39 + "</p><p>more text</p>"
        max_len = 40
        fragments = list(split_html_message(html, max_len))
        self.assertEqual(len(fragments), 2)

    def test_exceeding_max_length(self):
        """Test for error when a single non-splittable tag exceeds the max length"""
        html = '<a href="https://example.com">' + "a" * 50 + "</a>"
        max_len = 40
        with self.assertRaisesRegex(ValueError, f"Cannot split tag exceeding {max_len} characters"):
            list(split_html_message(html, max_len))

    def test_small_max_len(self):
        """Test when the max length is too small for any tag"""
        html = "<p>Test</p>"
        max_len = 4
        with self.assertRaisesRegex(ValueError, f"Cannot split tag exceeding {max_len} characters"):
            list(split_html_message(html, max_len))

    def test_nested_tags(self):
        """Test handling nested tags within the length limit"""
        html = "<div><p>Test</p></div>"
        max_len = 20
        fragments = list(split_html_message(html, max_len))
        self.assertEqual(len(fragments), 1)

    def test_multiple_splits(self):
        """Test splitting large content across multiple fragments"""
        html = "<p>" + "a" * 100 + "</p>" * 5
        max_len = 120
        fragments = list(split_html_message(html, max_len))
        self.assertGreater(len(fragments), 1)

    def test_links_with_urls(self):
        """Test proper handling of anchor tags with URLs"""
        html = '<a href="https://example.com">Link</a>'
        max_len = 50
        fragments = list(split_html_message(html, max_len))
        self.assertEqual(len(fragments), 1)
        self.assertIn('href="https://example.com"', fragments[0])
        self.assertIn('Link', fragments[0])


if __name__ == "__main__":
    unittest.main()
