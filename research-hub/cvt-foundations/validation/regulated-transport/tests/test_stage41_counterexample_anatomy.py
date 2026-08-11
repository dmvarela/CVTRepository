import unittest

import numpy as np
import pandas as pd

from src.stage41_counterexample_anatomy import attach_nearest_controls, classify


THRESHOLDS = {"B": 0.6, "Q": 0.6, "C": 0.6, "S": 0.6}


def example_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "row_id": ["a", "b", "c", "d"],
            "hosted": [1, 1, 0, 0],
            "g_b": [0.5, 0.7, 0.8, 0.4],
            "g_q": [0.7, 0.7, 0.8, 0.7],
            "g_c_probe_sham_adjusted_primary": [0.7, 0.7, 0.8, 0.7],
            "g_s": [0.7, 0.7, 0.8, 0.7],
        }
    )


class Stage41AnatomyTests(unittest.TestCase):
    def test_classification_is_exhaustive_and_patterns_are_ordered(self) -> None:
        anatomy = classify(example_frame(), THRESHOLDS)
        self.assertEqual(
            anatomy.primary_class.tolist(),
            [
                "hosted_failed_gate",
                "hosted_all_gates_pass",
                "nonhosted_all_gates_pass",
                "nonhosted_failed_gate",
            ],
        )
        self.assertEqual(anatomy.failed_gate_pattern.tolist(), ["B", "none", "none", "B"])
        self.assertEqual(anatomy.failed_gate_count.tolist(), [1, 0, 0, 1])

    def test_gate_margin_is_value_minus_frozen_threshold(self) -> None:
        anatomy = classify(example_frame(), THRESHOLDS)
        self.assertTrue(np.isclose(anatomy.loc[0, "gate_B_margin"], -0.1))
        self.assertTrue(np.isclose(anatomy.loc[2, "gate_C_margin"], 0.2))

    def test_nearest_controls_use_opposite_outcome_with_same_gate_status(self) -> None:
        anatomy = attach_nearest_controls(classify(example_frame(), THRESHOLDS))
        hosted_failed = anatomy[anatomy.primary_class == "hosted_failed_gate"].iloc[0]
        failed_all_pass = anatomy[anatomy.primary_class == "nonhosted_all_gates_pass"].iloc[0]
        self.assertEqual(hosted_failed.nearest_control_row_id, "d")
        self.assertEqual(hosted_failed.nearest_control_class, "nonhosted_failed_gate")
        self.assertEqual(failed_all_pass.nearest_control_row_id, "b")
        self.assertEqual(failed_all_pass.nearest_control_class, "hosted_all_gates_pass")


if __name__ == "__main__":
    unittest.main()

