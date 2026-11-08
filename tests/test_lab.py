import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class LabSmokeTests(unittest.TestCase):
    def run_script(self, script: str, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, script, *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_scripts_compile(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "compileall",
                "-q",
                "producer",
                "consumer",
                "scripts",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_cli_help_is_available(self) -> None:
        for script in ("producer/main.py", "consumer/main.py"):
            result = self.run_script(script, "--help")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("usage:", result.stdout)

    def test_producer_order_shape(self) -> None:
        sys.path.insert(0, str(ROOT))
        from producer.main import PRODUCTS, build_order

        order = build_order(__import__("random").Random(42))
        self.assertEqual(
            set(order),
            {
                "order_id",
                "customer",
                "product",
                "category",
                "price",
                "quantity",
                "created_at",
            },
        )
        self.assertIn((order["product"], order["category"], order["price"]), PRODUCTS)
        self.assertGreaterEqual(order["quantity"], 1)

    def test_json_verification_accepts_equal_data(self) -> None:
        records = [{"order_id": "test-1", "product": "4K Monitor"}]
        with tempfile.TemporaryDirectory() as directory:
            expected = Path(directory) / "expected.json"
            actual = Path(directory) / "actual.json"
            expected.write_text(json.dumps(records), encoding="utf-8")
            actual.write_text(json.dumps(records), encoding="utf-8")
            result = self.run_script(
                "scripts/verify_json.py",
                "--expected",
                str(expected),
                "--actual",
                str(actual),
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Verification passed", result.stdout)


if __name__ == "__main__":
    unittest.main()
