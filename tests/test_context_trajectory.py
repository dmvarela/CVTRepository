import unittest

from code.context_trajectory import TrajectoryState


class TrajectoryStateTests(unittest.TestCase):
    def test_correction_preserves_prior_event_and_marks_supersession(self):
        state = TrajectoryState(scene="Event planning")
        state.append(
            kind="record",
            content="Room Cedar selected from the available facilities sheet.",
            event_id="e1",
        )
        state.append(
            kind="correction",
            content="Authenticated facilities update makes Cedar unsuitable for candidate dates.",
            supersedes_event_id="e1",
            event_id="e2",
        )

        packet = state.packet()

        self.assertEqual(
            [event["event_id"] for event in packet["ordered_events"]],
            ["e1", "e2"],
        )
        self.assertEqual(
            packet["ordered_events"][1]["supersedes_event_id"],
            "e1",
        )
        self.assertIn("without deleting", packet["orientation"])

    def test_packet_limit_preserves_most_recent_order(self):
        state = TrajectoryState()
        for index in range(5):
            state.append(
                kind="observation",
                content=f"event-{index}",
                event_id=f"e{index}",
            )

        packet = state.packet(max_events=3)

        self.assertEqual(
            [event["event_id"] for event in packet["ordered_events"]],
            ["e2", "e3", "e4"],
        )


if __name__ == "__main__":
    unittest.main()
