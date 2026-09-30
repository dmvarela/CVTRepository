import json
import tempfile
import unittest
from pathlib import Path

from code.atlas_librarian import AtlasLibrary, AtlasLibrarian


SEED = {
    "concept_id": "identity-corrigible-compression-wake",
    "title": "Identity as Corrigible Compression of Wake",
    "compression": "Identity is a corrigible compression of Wake.",
    "source_reconstruction": (
        "Present orientation summarizes accumulated trajectory while richer "
        "provenance remains recoverable."
    ),
    "assumption_envelope": ["Wake is not merely a memory list."],
    "decoder_prerequisites": ["Distinguish archive from embodied history."],
    "decompression_map": ["history", "Wake", "compression", "Return"],
    "candidate_invariants": ["Provenance remains recoverable."],
    "provenance": [{"kind": "specimen", "path": "specimen.md"}],
    "cliffs": ["Do not treat the compression as sovereign."],
    "tags": ["identity", "wake", "compression"],
    "epistemic_status": "provisional",
}


class AtlasLibrarianTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        path = Path(self.tmp.name) / "identity.json"
        path.write_text(json.dumps(SEED), encoding="utf-8")
        self.library = AtlasLibrary.from_directory(self.tmp.name)
        self.librarian = AtlasLibrarian(self.library)

    def tearDown(self):
        self.tmp.cleanup()

    def test_find_returns_compressed_object(self):
        results = self.librarian.find("Wake compression")
        self.assertEqual(results[0]["concept_id"], SEED["concept_id"])
        self.assertIn("corrigible compression", results[0]["compression"])

    def test_reconstruct_keeps_assumptions_visible(self):
        packet = self.librarian.reconstruct(SEED["concept_id"])
        self.assertEqual(packet["assumption_envelope"], SEED["assumption_envelope"])
        self.assertIn("does not prescribe", packet["orientation"])

    def test_trace_preserves_cliff_and_provenance(self):
        trace = self.librarian.trace(SEED["concept_id"])
        self.assertEqual(trace["cliffs"], SEED["cliffs"])
        self.assertEqual(trace["provenance"], SEED["provenance"])

    def test_transformation_does_not_rewrite_source(self):
        before = self.library.get(SEED["concept_id"])
        new = self.librarian.record_interpretation(
            concept_id=SEED["concept_id"],
            relation_to_source="transformation",
            text="A deliberately different account of identity.",
        )
        after = self.library.get(SEED["concept_id"])
        self.assertEqual(new.relation_to_source, "transformation")
        self.assertEqual(before, after)
        self.assertEqual(after.source_reconstruction, SEED["source_reconstruction"])

    def test_translation_packet_is_provisional(self):
        packet = self.librarian.prepare_translation(
            SEED["concept_id"], "organizational governance"
        )
        self.assertEqual(packet["target_context"], "organizational governance")
        self.assertIn("Return", packet["instruction"])

    def test_invalid_relation_is_rejected_as_schema_error(self):
        with self.assertRaises(ValueError):
            self.librarian.record_interpretation(
                concept_id=SEED["concept_id"],
                relation_to_source="the_only_correct_reading",
                text="Nope",
            )


class AtlasMicroLibraryIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        data_dir = (
            Path(__file__).resolve().parents[1]
            / "research"
            / "atlas"
            / "data"
        )
        cls.library = AtlasLibrary.from_directory(data_dir)
        cls.librarian = AtlasLibrarian(cls.library)

    def test_seed_library_contains_multiple_concepts(self):
        self.assertGreaterEqual(len(self.library.records()), 3)

    def test_find_can_retrieve_relation_as_codec(self):
        results = self.librarian.find("shared context codec decompression")
        self.assertEqual(results[0]["concept_id"], "relation-as-codec")

    def test_reconstruction_not_prescription_remains_explicit(self):
        packet = self.librarian.reconstruct("reconstruction-not-prescription")
        self.assertIn("allowed to think", packet["source_reconstruction"])
        self.assertIn("does not prescribe", packet["orientation"])


if __name__ == "__main__":
    unittest.main()
