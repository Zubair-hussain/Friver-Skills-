import os
import sys
import unittest

SCRIPTS = os.path.join(os.path.dirname(__file__), "..", "skills", "fiverr-gig-optimizer", "scripts")
sys.path.insert(0, os.path.abspath(SCRIPTS))

from sync_policy_sources import normalized_article_text  # noqa: E402


class TestPolicyExtraction(unittest.TestCase):
    def test_extracts_article_and_ignores_script(self):
        html = "<html><nav>menu</nav><article><h1>Rules</h1><p>Use relevant tags.</p><script>noise()</script></article></html>"
        self.assertEqual(normalized_article_text(html), "Rules Use relevant tags.")


if __name__ == "__main__":
    unittest.main()
