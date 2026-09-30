import contextlib
import io
import json
import os
import tempfile
import unittest

SCRIPTS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "skills", "fiverr-gig-optimizer", "scripts"))
import sys
sys.path.insert(0, SCRIPTS)

import analyze_pricing
import build_benchmarks
import build_catalog
import query_dataset
import score_keyword


class TempDirTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)

    def path(self, name):
        return os.path.join(self.temp.name, name)

    def write_json(self, name, value):
        path = self.path(name)
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(value, handle)
        return path


class TestPricingCli(TempDirTest):
    def test_main_success_and_missing_category(self):
        pools = {"Cat": {"basic": [10, 20], "standard": [30], "premium": []}}
        path = self.write_json("prices.json", pools)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(analyze_pricing.main(["--prices", path, "--category", "Cat", "--experience", "New"]), 0)
        self.assertEqual(json.loads(out.getvalue())["strategy"], "new_seller")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(analyze_pricing.main(["--prices", path, "--category", "Missing"]), 1)
        self.assertIn("category not found", out.getvalue())


class TestBenchmarkBuilder(TempDirTest):
    def test_json_and_csv_loaders_and_main(self):
        rows = [{
            "category": "Programming", "subcategory": "AI", "title": "Bot",
            "tags": ["ai", "bot"], "basic_price": 10, "standard_price": 20,
            "premium_price": 40, "gig_count_in_search": 100,
        }]
        source = self.write_json("rows.json", rows)
        self.assertEqual(build_benchmarks.load_rows(source), rows)
        self.assertEqual(build_benchmarks.category_key({}), "Uncategorized")
        self.assertEqual(build_benchmarks.build_pools(rows)["Programming > AI"]["basic"], [10])
        index = build_benchmarks.build_index(rows)
        self.assertEqual(index["ai"]["gig_count"], 100)

        pools, idx = self.path("pools.json"), self.path("index.json")
        self.assertEqual(build_benchmarks.main(["--input", source, "--pools", pools, "--index", idx]), 0)
        self.assertTrue(os.path.exists(pools))
        self.assertTrue(os.path.exists(idx))

        csv_path = self.path("rows.csv")
        with open(csv_path, "w", encoding="utf-8", newline="") as handle:
            handle.write("category,tags,basic_price,standard_price,premium_price,gig_count_in_search,review_count\n")
            handle.write("Design,logo; brand,12.5,bad,,200,4\n")
        loaded = build_benchmarks.load_rows(csv_path=csv_path)
        self.assertEqual(loaded[0]["tags"], ["logo", "brand"])
        self.assertEqual(loaded[0]["basic_price"], 12.5)
        self.assertIsNone(loaded[0]["standard_price"])


class TestKeywordCli(TempDirTest):
    def test_score_and_query_mains(self):
        gigs = [{"review_count": 20}]
        top = self.write_json("top.json", gigs)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(score_keyword.main([
                "--keyword", "ai bot", "--gig-count", "12", "--top-gigs", top
            ]), 0)
        self.assertEqual(json.loads(out.getvalue())["gig_count"], 12)

        cfg = query_dataset.load_config()
        dataset = []
        for i in range(5):
            dataset.append({
                "title": f"AI chatbot {i}", "subcategory": "AI Chatbots",
                "tags": ["ai chatbot"], "review_count": i,
                "gig_count_in_search": 55,
            })
        data_path = self.write_json("dataset.json", dataset)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(query_dataset.main([
                "--keyword", "ai chatbot", "--dataset", data_path, "--top-n", "2"
            ]), 0)
        result = json.loads(out.getvalue())
        self.assertEqual(result["gig_count"], 55)
        self.assertEqual(len(result["top_gigs"]), 2)
        self.assertEqual(query_dataset.overlap_ratio(set(), {"x"}), 0.0)
        self.assertEqual(query_dataset.jaccard(set(), {"x"}), 0.0)
        self.assertIn("lookup", cfg)


class TestCatalogDirect(TempDirTest):
    @staticmethod
    def config():
        return {
            "seller": {"name": "Owner"},
            "data_provenance": {},
            "gigs": [{
                "id": 1, "phase": 1, "title": "I will build an AI chatbot",
                "cat": "Programming", "tags": ["ai chatbot"],
                "desc": "I build an AI chatbot.", "competition": {"tier": "LOW", "count": 12},
                "scores": {"opportunity": 80, "flags": []},
                "pricing": {"basic": {"name": "Basic", "price": 25, "rev": 1, "items": ["Bot"]}},
                "img": {"headline": "AI CHATBOT", "sub": "For your team", "badge": "CUSTOM"},
            }],
        }

    def test_render_and_main_paths(self):
        config = self.config()
        html = build_catalog.render(config)
        self.assertIn("og:image", html)
        self.assertIn("Policy preflight", html)
        self.assertNotIn("</script><script>", build_catalog.render({**config, "seller": {"name": "</script><script>"}}))
        source = self.write_json("gig.json", config)
        output = self.path("catalog.html")
        self.assertEqual(build_catalog.main([source, "--out", output]), 0)
        self.assertTrue(os.path.exists(output))

        invalid = self.config()
        invalid["gigs"][0]["title"] = "bad title"
        invalid_path = self.write_json("invalid.json", invalid)
        self.assertEqual(build_catalog.main([invalid_path, "--out", self.path("bad.html")]), 2)


if __name__ == "__main__":
    unittest.main()
