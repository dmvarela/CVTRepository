"""Minimal Atlas library-librarian prototype.

Atlas keeps durable records separate from the Librarian that traverses them.
Version 0.3 adds explicit Decoder Profiles so receiving assumptions can be
represented without being confused with source semantics.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable
import json
import re


ALLOWED_RELATIONS = {
    "reconstruction",
    "compatible_extension",
    "contextual_translation",
    "transformation",
    "contradiction",
    "new_construction",
}

ALLOWED_LAYER_TYPES = {
    "source_text",
    "translation",
    "lexical_note",
    "historical_reconstruction",
    "scholarly_interpretation",
    "reader_interpretation",
    "transformation",
    "source_correction",
}


def _tokens(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-zA-Z0-9_τ]+", text.lower())
        if len(token) > 2
    }


@dataclass(frozen=True)
class KnowledgeLayer:
    layer_id: str
    layer_type: str
    content: str
    source_ref: str = ""
    language: str = ""
    status: str = "provisional"
    derived_from: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    provenance: list[dict[str, Any]] = field(default_factory=list)
    notes: str = ""

    def __post_init__(self) -> None:
        if self.layer_type not in ALLOWED_LAYER_TYPES:
            raise ValueError(
                f"layer_type must be one of {sorted(ALLOWED_LAYER_TYPES)}"
            )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "KnowledgeLayer":
        return cls(
            layer_id=str(data["layer_id"]),
            layer_type=str(data["layer_type"]),
            content=str(data["content"]),
            source_ref=str(data.get("source_ref", "")),
            language=str(data.get("language", "")),
            status=str(data.get("status", "provisional")),
            derived_from=[str(x) for x in data.get("derived_from", [])],
            assumptions=[str(x) for x in data.get("assumptions", [])],
            provenance=[dict(x) for x in data.get("provenance", [])],
            notes=str(data.get("notes", "")),
        )


@dataclass(frozen=True)
class DecoderProfile:
    profile_id: str
    context: str
    likely_assumptions: list[str] = field(default_factory=list)
    assumptions_not_guaranteed: list[str] = field(default_factory=list)
    needed_distinctions: list[str] = field(default_factory=list)
    mismatch_risks: list[str] = field(default_factory=list)
    preparation_notes: list[str] = field(default_factory=list)
    status: str = "provisional"
    provenance: list[dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DecoderProfile":
        return cls(
            profile_id=str(data["profile_id"]),
            context=str(data["context"]),
            likely_assumptions=[str(x) for x in data.get("likely_assumptions", [])],
            assumptions_not_guaranteed=[
                str(x) for x in data.get("assumptions_not_guaranteed", [])
            ],
            needed_distinctions=[
                str(x) for x in data.get("needed_distinctions", [])
            ],
            mismatch_risks=[str(x) for x in data.get("mismatch_risks", [])],
            preparation_notes=[str(x) for x in data.get("preparation_notes", [])],
            status=str(data.get("status", "provisional")),
            provenance=[dict(x) for x in data.get("provenance", [])],
        )


@dataclass(frozen=True)
class ConceptRecord:
    concept_id: str
    title: str
    compression: str
    source_reconstruction: str
    assumption_envelope: list[str] = field(default_factory=list)
    decoder_prerequisites: list[str] = field(default_factory=list)
    decompression_map: list[str] = field(default_factory=list)
    candidate_invariants: list[str] = field(default_factory=list)
    provenance: list[dict[str, Any]] = field(default_factory=list)
    cliffs: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    epistemic_status: str = "provisional"
    layers: list[KnowledgeLayer] = field(default_factory=list)
    decoder_profiles: list[DecoderProfile] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ConceptRecord":
        return cls(
            concept_id=str(data["concept_id"]),
            title=str(data["title"]),
            compression=str(data["compression"]),
            source_reconstruction=str(data.get("source_reconstruction", "")),
            assumption_envelope=[str(x) for x in data.get("assumption_envelope", [])],
            decoder_prerequisites=[str(x) for x in data.get("decoder_prerequisites", [])],
            decompression_map=[str(x) for x in data.get("decompression_map", [])],
            candidate_invariants=[str(x) for x in data.get("candidate_invariants", [])],
            provenance=[dict(x) for x in data.get("provenance", [])],
            cliffs=[str(x) for x in data.get("cliffs", [])],
            tags=[str(x) for x in data.get("tags", [])],
            epistemic_status=str(data.get("epistemic_status", "provisional")),
            layers=[KnowledgeLayer.from_dict(x) for x in data.get("layers", [])],
            decoder_profiles=[
                DecoderProfile.from_dict(x) for x in data.get("decoder_profiles", [])
            ],
        )


@dataclass(frozen=True)
class InterpretationRecord:
    concept_id: str
    relation_to_source: str
    text: str
    notes: str = ""

    def __post_init__(self) -> None:
        if self.relation_to_source not in ALLOWED_RELATIONS:
            raise ValueError(
                f"relation_to_source must be one of {sorted(ALLOWED_RELATIONS)}"
            )


class AtlasLibrary:
    """Durable concept records. The library does not interpret by itself."""

    def __init__(self, records: Iterable[ConceptRecord]):
        self._records = {record.concept_id: record for record in records}

    @classmethod
    def from_directory(cls, directory: str | Path) -> "AtlasLibrary":
        directory = Path(directory)
        records: list[ConceptRecord] = []
        for path in sorted(directory.glob("*.json")):
            with path.open("r", encoding="utf-8") as handle:
                records.append(ConceptRecord.from_dict(json.load(handle)))
        return cls(records)

    def get(self, concept_id: str) -> ConceptRecord:
        try:
            return self._records[concept_id]
        except KeyError as exc:
            raise KeyError(f"Unknown Atlas concept: {concept_id}") from exc

    def records(self) -> tuple[ConceptRecord, ...]:
        return tuple(self._records.values())


class AtlasLibrarian:
    """Interpretive operations over an AtlasLibrary.

    The Librarian preserves source fidelity as provenance, not as a restriction
    on what new interpretations may be created.
    """

    def __init__(self, library: AtlasLibrary):
        self.library = library
        self.interpretations: list[InterpretationRecord] = []

    def find(self, query: str) -> list[dict[str, Any]]:
        q = _tokens(query)
        ranked: list[tuple[int, ConceptRecord]] = []
        for record in self.library.records():
            layer_text = " ".join(layer.content for layer in record.layers)
            decoder_text = " ".join(
                " ".join(
                    [
                        profile.context,
                        *profile.likely_assumptions,
                        *profile.mismatch_risks,
                        *profile.needed_distinctions,
                    ]
                )
                for profile in record.decoder_profiles
            )
            haystack = " ".join(
                [
                    record.title,
                    record.compression,
                    *record.tags,
                    layer_text,
                    decoder_text,
                ]
            )
            score = len(q & _tokens(haystack))
            if score:
                ranked.append((score, record))
        ranked.sort(key=lambda item: (-item[0], item[1].title.lower()))
        return [
            {
                "concept_id": record.concept_id,
                "title": record.title,
                "score": score,
                "compression": record.compression,
            }
            for score, record in ranked
        ]

    def trace(self, concept_id: str) -> dict[str, Any]:
        record = self.library.get(concept_id)
        return {
            "concept_id": record.concept_id,
            "title": record.title,
            "decompression_map": list(record.decompression_map),
            "provenance": [dict(x) for x in record.provenance],
            "cliffs": list(record.cliffs),
            "epistemic_status": record.epistemic_status,
            "layer_ids": [layer.layer_id for layer in record.layers],
            "decoder_profile_ids": [
                profile.profile_id for profile in record.decoder_profiles
            ],
        }

    def reconstruct(self, concept_id: str) -> dict[str, Any]:
        record = self.library.get(concept_id)
        return {
            "concept_id": record.concept_id,
            "title": record.title,
            "compressed_object": record.compression,
            "source_reconstruction": record.source_reconstruction,
            "assumption_envelope": list(record.assumption_envelope),
            "decoder_prerequisites": list(record.decoder_prerequisites),
            "candidate_invariants": list(record.candidate_invariants),
            "layers": [
                {
                    "layer_id": layer.layer_id,
                    "layer_type": layer.layer_type,
                    "content": layer.content,
                    "source_ref": layer.source_ref,
                    "language": layer.language,
                    "status": layer.status,
                    "derived_from": list(layer.derived_from),
                }
                for layer in record.layers
            ],
            "orientation": (
                "This packet reconstructs the source concept. It does not prescribe "
                "what a reader is allowed to think or build from it."
            ),
        }

    def layered_view(
        self,
        concept_id: str,
        *,
        layer_type: str | None = None,
    ) -> list[dict[str, Any]]:
        record = self.library.get(concept_id)
        layers = record.layers
        if layer_type is not None:
            if layer_type not in ALLOWED_LAYER_TYPES:
                raise ValueError(
                    f"layer_type must be one of {sorted(ALLOWED_LAYER_TYPES)}"
                )
            layers = [layer for layer in layers if layer.layer_type == layer_type]
        return [
            {
                "layer_id": layer.layer_id,
                "layer_type": layer.layer_type,
                "content": layer.content,
                "source_ref": layer.source_ref,
                "language": layer.language,
                "status": layer.status,
                "derived_from": list(layer.derived_from),
                "assumptions": list(layer.assumptions),
                "provenance": [dict(x) for x in layer.provenance],
                "notes": layer.notes,
            }
            for layer in layers
        ]

    def prepare_decoder(
        self,
        concept_id: str,
        *,
        profile_id: str | None = None,
    ) -> dict[str, Any]:
        record = self.library.get(concept_id)
        if profile_id is None:
            profiles = record.decoder_profiles
        else:
            profiles = [
                profile
                for profile in record.decoder_profiles
                if profile.profile_id == profile_id
            ]
            if not profiles:
                raise KeyError(
                    f"Unknown decoder profile {profile_id!r} for concept {concept_id!r}"
                )

        return {
            "concept_id": record.concept_id,
            "source_assumption_envelope": list(record.assumption_envelope),
            "generic_decoder_prerequisites": list(record.decoder_prerequisites),
            "decoder_profiles": [
                {
                    "profile_id": profile.profile_id,
                    "context": profile.context,
                    "likely_assumptions": list(profile.likely_assumptions),
                    "assumptions_not_guaranteed": list(
                        profile.assumptions_not_guaranteed
                    ),
                    "needed_distinctions": list(profile.needed_distinctions),
                    "mismatch_risks": list(profile.mismatch_risks),
                    "preparation_notes": list(profile.preparation_notes),
                    "status": profile.status,
                    "provenance": [dict(x) for x in profile.provenance],
                }
                for profile in profiles
            ],
            "orientation": (
                "Decoder profiles are provisional context models, not claims about "
                "what any individual reader must believe. They exist to surface "
                "possible imported assumptions before faithful reconstruction."
            ),
        }

    def prepare_translation(self, concept_id: str, target_context: str) -> dict[str, Any]:
        record = self.library.get(concept_id)
        return {
            "concept_id": record.concept_id,
            "target_context": target_context,
            "source_reconstruction": record.source_reconstruction,
            "candidate_invariants": list(record.candidate_invariants),
            "source_assumptions": list(record.assumption_envelope),
            "source_layers": self.layered_view(concept_id),
            "decoder_preparation": self.prepare_decoder(concept_id),
            "instruction": (
                "Propose a contextual translation without claiming that identical "
                "surface implementation is required. Preserve any departure from the "
                "source as provenance and subject the result to Return."
            ),
        }

    def record_interpretation(
        self,
        *,
        concept_id: str,
        relation_to_source: str,
        text: str,
        notes: str = "",
    ) -> InterpretationRecord:
        self.library.get(concept_id)
        record = InterpretationRecord(
            concept_id=concept_id,
            relation_to_source=relation_to_source,
            text=text,
            notes=notes,
        )
        self.interpretations.append(record)
        return record
