import os
import re
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


class TestDocumentationLinks(unittest.TestCase):
    def test_local_markdown_links_exist(self):
        missing = []
        paths = [os.path.join(ROOT, "README.md")]
        for base, _, files in os.walk(os.path.join(ROOT, "docs")):
            paths.extend(os.path.join(base, name) for name in files if name.endswith(".md"))
        for path in paths:
            with open(path, encoding="utf-8") as handle:
                text = handle.read()
            for target in LINK.findall(text):
                if target.startswith(("http://", "https://", "#")):
                    continue
                clean = target.split("#", 1)[0]
                resolved = os.path.normpath(os.path.join(os.path.dirname(path), clean))
                if clean and not os.path.exists(resolved):
                    missing.append(f"{os.path.relpath(path, ROOT)} -> {target}")
        self.assertEqual(missing, [], "Broken local documentation links:\n" + "\n".join(missing))
        index = os.path.join(ROOT, "index.html")
        workflow = os.path.join(ROOT, ".github", "workflows", "pages.yml")
        self.assertTrue(os.path.isfile(index))
        self.assertTrue(os.path.isfile(workflow))
        with open(index, encoding="utf-8") as handle:
            page = handle.read()
        self.assertIn("prefers-reduced-motion", page)
        self.assertIn("<meta property=\"og:title\"", page)
        self.assertNotIn("<script src=", page)


if __name__ == "__main__":
    unittest.main()
