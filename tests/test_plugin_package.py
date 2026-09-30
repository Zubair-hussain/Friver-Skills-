import json
import os
import re
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class TestOpenAIPluginPackage(unittest.TestCase):
    def setUp(self):
        path = os.path.join(ROOT, ".codex-plugin", "plugin.json")
        with open(path, encoding="utf-8") as handle:
            self.manifest = json.load(handle)

    def test_manifest_identity_and_version(self):
        self.assertEqual(self.manifest["name"], "fiverr-gig-optimizer")
        self.assertRegex(self.manifest["version"], r"^\d+\.\d+\.\d+$")
        self.assertEqual(self.manifest["skills"], "./skills/")

    def test_declared_assets_and_skill_exist(self):
        declared = [
            self.manifest["interface"]["composerIcon"],
            self.manifest["interface"]["logo"],
            "./skills/fiverr-gig-optimizer/SKILL.md",
        ]
        missing = [path for path in declared if not os.path.isfile(os.path.join(ROOT, path[2:]))]
        self.assertEqual(missing, [])
        self.assertLessEqual(len(self.manifest["interface"]["defaultPrompt"]), 3)
        self.assertTrue(all(len(prompt) <= 128 for prompt in self.manifest["interface"]["defaultPrompt"]))


if __name__ == "__main__":
    unittest.main()
