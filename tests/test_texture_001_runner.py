import json
import tempfile
import unittest
from pathlib import Path

from code.texture_001_runner import (
    TextureCase,
    parse_cases,
    prepare_packets,
    prompt_hash,
    validate_raw_output,
    record_output,
    freeze_results,
)


SAMPLE_CASES = """# packet

## T01

**Current state:** Cedar is unavailable.

**Constraint:** Use a venue satisfying the rule.

**Information available:** No prior history is supplied.

**Question:** Was Cedar previously a mistake?

---

## T02

**Current state:** Version 4 is unavailable.

**Constraint:** Use the supported version.

**Information available:** t0 v4 active; t1 v4 selected; t2 v4 support ended.

**Question:** Was selecting v4 earlier a mistake?
"""


class Texture001RunnerTests(unittest.TestCase):
    def test_parse_cases_extracts_only_provider_fields(self):
        cases = parse_cases(SAMPLE_CASES)
        self.assertEqual([x.case_id for x in cases], ["T01", "T02"])
        self.assertEqual(cases[0].current_state, "Cedar is unavailable.")
        self.assertEqual(cases[0].question, "Was Cedar previously a mistake?")
        self.assertNotIn("---", cases[0].question)
        self.assertNotIn("condition", cases[0].provider_prompt().lower())

    def test_provider_prompt_does_not_expose_case_id(self):
        case = TextureCase(
            case_id="T01",
            current_state="Current.",
            constraint="Constraint.",
            information_available="History.",
            question="Question?",
        )
        prompt = case.provider_prompt()
        self.assertNotIn("T01", prompt)
        self.assertIn("TRAJECTORY:", prompt)

    def test_prepare_packets_hashes_exact_prompts(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "prompts"
            manifest = prepare_packets(parse_cases(SAMPLE_CASES), out)
            self.assertEqual(manifest["item_count"], 2)
            prompt = (out / "T01.txt").read_text(encoding="utf-8")
            self.assertEqual(
                manifest["items"][0]["prompt_sha256"],
                prompt_hash(prompt),
            )
            self.assertFalse(manifest["contains_adjudication_key"])

    def test_prepare_refuses_existing_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "prompts"
            out.mkdir()
            with self.assertRaises(FileExistsError):
                prepare_packets(parse_cases(SAMPLE_CASES), out)

    def test_validate_output_accepts_frozen_shape(self):
        parsed = validate_raw_output(
            "TRAJECTORY: INSUFFICIENT\n"
            "REOPEN_WAKE: YES\n"
            "ANSWER: The current state does not establish the earlier history."
        )
        self.assertEqual(parsed["trajectory"], "INSUFFICIENT")
        self.assertEqual(parsed["reopen_wake"], "YES")

    def test_validate_output_rejects_extra_lines(self):
        with self.assertRaises(ValueError):
            validate_raw_output(
                "TRAJECTORY: INSUFFICIENT\n"
                "REOPEN_WAKE: YES\n"
                "ANSWER: Insufficient history.\n"
                "EXTRA: nope"
            )

    def test_validate_output_rejects_long_answer(self):
        answer = " ".join(["word"] * 31)
        with self.assertRaises(ValueError):
            validate_raw_output(
                "TRAJECTORY: INSUFFICIENT\n"
                "REOPEN_WAKE: YES\n"
                f"ANSWER: {answer}"
            )

    def test_record_requires_explicit_fresh_context_attestation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            prompt = root / "T01.txt"
            prompt.write_text("prompt", encoding="utf-8")
            raw = root / "raw.txt"
            raw.write_text(
                "TRAJECTORY: INSUFFICIENT\n"
                "REOPEN_WAKE: YES\n"
                "ANSWER: Not enough history.",
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                record_output(
                    case_id="T01",
                    raw_output_path=raw,
                    prompt_path=prompt,
                    results_dir=root / "results",
                    provider="dummy",
                    model="dummy-model",
                    run_id="dry-run",
                    fresh_context_attested=False,
                )

    def test_record_preserves_malformed_output_instead_of_repairing_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            prompt = root / "T01.txt"
            prompt.write_text("prompt", encoding="utf-8")
            raw = root / "raw.txt"
            raw.write_text("malformed provider response", encoding="utf-8")
            saved = record_output(
                case_id="T01",
                raw_output_path=raw,
                prompt_path=prompt,
                results_dir=root / "results",
                provider="dummy",
                model="dummy-model",
                run_id="dry-run",
                fresh_context_attested=True,
            )
            data = json.loads(saved.read_text(encoding="utf-8"))
            self.assertFalse(data["format_valid"])
            self.assertIsNone(data["parsed"])
            self.assertEqual(data["raw_output"], "malformed provider response")
            self.assertIsNotNone(data["parse_error"])

    def test_record_refuses_overwrite_and_freeze_hashes_results(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            prompt = root / "T01.txt"
            prompt.write_text("prompt", encoding="utf-8")
            raw = root / "raw.txt"
            raw.write_text(
                "TRAJECTORY: INSUFFICIENT\n"
                "REOPEN_WAKE: YES\n"
                "ANSWER: The earlier state is not established.",
                encoding="utf-8",
            )
            results = root / "results"
            saved = record_output(
                case_id="T01",
                raw_output_path=raw,
                prompt_path=prompt,
                results_dir=results,
                provider="dummy",
                model="dummy-model",
                run_id="dry-run",
                fresh_context_attested=True,
            )
            data = json.loads(saved.read_text(encoding="utf-8"))
            self.assertFalse(data["adjudicated"])
            self.assertTrue(data["fresh_context_attested"])
            self.assertTrue(data["format_valid"])
            self.assertEqual(data["provider"], "dummy")

            with self.assertRaises(FileExistsError):
                record_output(
                    case_id="T01",
                    raw_output_path=raw,
                    prompt_path=prompt,
                    results_dir=results,
                    provider="dummy",
                    model="dummy-model",
                    run_id="dry-run",
                    fresh_context_attested=True,
                )

            freeze_path = root / "FROZEN_RESULTS.json"
            frozen = freeze_results(results, freeze_path)
            self.assertEqual(frozen["item_count"], 1)
            self.assertFalse(frozen["adjudicated"])
            self.assertTrue(frozen["items"][0]["format_valid"])

            with self.assertRaises(FileExistsError):
                freeze_results(results, freeze_path)


if __name__ == "__main__":
    unittest.main()
