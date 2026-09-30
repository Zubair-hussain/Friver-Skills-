import copy
import contextlib
import io
import json
import os
import sys
import tempfile
import unittest

SCRIPTS = os.path.join(os.path.dirname(__file__), "..", "skills", "fiverr-gig-optimizer", "scripts")
sys.path.insert(0, os.path.abspath(SCRIPTS))

import validate_gig as vg  # noqa: E402


GIG = {
    "id": 1,
    "title": "I will build an AI chatbot",
    "tags": ["ai chatbot"],
    "desc": "I build a focused AI chatbot for your business.",
    "pricing": {"basic": {"price": 25, "rev": 1}},
    "img": {"headline": "AI CHATBOT", "sub": "Built for your team", "badge": "CUSTOM"},
}


class TestGigPolicyValidation(unittest.TestCase):
    def test_valid_gig(self):
        report = vg.validate_catalog({"gigs": [GIG]})
        self.assertTrue(report["valid"], report)

    def test_title_and_tag_limits(self):
        gig = copy.deepcopy(GIG)
        gig["title"] = "Build " + "x" * 90
        gig["tags"] = [str(i) for i in range(6)]
        report = vg.validate_catalog({"gigs": [gig]})
        self.assertFalse(report["valid"])
        self.assertGreaterEqual(len(report["errors"]), 3)

    def test_fiverr_brand_rejected_in_gig_image(self):
        gig = copy.deepcopy(GIG)
        gig["img"]["badge"] = "Fiverr Pro"
        report = vg.validate_catalog({"gigs": [gig]})
        self.assertFalse(report["valid"])

    def test_all_policy_branches_and_cli(self):
        gig = copy.deepcopy(GIG)
        gig.update({
            "title": "I will guarantee / results",
            "tags": "not-a-list",
            "desc": "Contact me on WhatsApp or owner@example.com " + ("x" * 1300),
            "pricing": {
                "basic": {"price": 2, "rev": "0 revisions"},
                "standard": {"price": 10, "rev": "unlimited"},
                "premium": {"price": 20, "rev": 1},
                "extra": {"price": 30, "rev": 1},
            },
            "img": {
                "headline": "one two three four five six",
                "sub": "seven eight nine ten eleven",
                "badge": "custom",
            },
        })
        rules = vg.load_rules()
        rules["reviewed_at"] = "2020-01-01"
        report = vg.validate_catalog({"gigs": [gig]}, rules)
        self.assertFalse(report["valid"])
        self.assertGreaterEqual(len(report["errors"]), 4)
        self.assertGreaterEqual(len(report["warnings"]), 4)
        self.assertIsNone(vg._revision_count("unlimited"))
        self.assertFalse(vg.validate_catalog({}, rules)["valid"])

        with tempfile.TemporaryDirectory() as directory:
            config_path = os.path.join(directory, "gig.json")
            rules_path = os.path.join(directory, "rules.json")
            with open(config_path, "w", encoding="utf-8") as handle:
                json.dump({"gigs": [GIG]}, handle)
            with open(rules_path, "w", encoding="utf-8") as handle:
                json.dump(vg.load_rules(), handle)
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(vg.main([config_path, "--rules", rules_path]), 0)
            self.assertTrue(json.loads(output.getvalue())["valid"])
            report_path = os.path.join(directory, "report.json")
            self.assertEqual(vg.main([config_path, "--rules", rules_path, "--out", report_path]), 0)
            with open(report_path, encoding="utf-8") as handle:
                self.assertTrue(json.load(handle)["valid"])


if __name__ == "__main__":
    unittest.main()
