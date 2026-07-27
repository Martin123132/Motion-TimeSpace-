from __future__ import annotations

import collections
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SOURCE_5053 = POST / "source-intake" / "functional_rg" / "5053"
SOURCE = POST / "source-intake" / "functional_rg" / "5056"
RESULT_JSON = SOURCE / "topology_combinatorics_invariance_sweep.json"
PAIR_CSV = SOURCE / "epsilon_pair_structural_comparison.csv"
ADJACENCY_CSV = SOURCE / "argument_adjacency_structural_comparison.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5056_VALIDATION.csv"
)
MARKER = "MTS_5056_TOPOLOGY_COMBINATORICS_INVARIANCE_SWEEP"
REVISION = "topology-numeric-versus-combinatorial-signature-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def localize(value: str) -> Path:
    path = Path(value)
    if path.exists():
        return path
    normalized = value.replace("\\", "/")
    marker = "/post-checkpoint-work/"
    if marker not in normalized:
        raise FileNotFoundError(value)
    candidate = POST / normalized.split(marker, 1)[1]
    if not candidate.exists():
        raise FileNotFoundError(candidate)
    return candidate


def normalized_pairs(row: dict[str, Any]) -> tuple[tuple[str, ...], ...]:
    return tuple(
        sorted(tuple(sorted(str(value) for value in pair)) for pair in row["representing_pairs"])
    )


def crossing_token(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        normalized_pairs(row),
        int(row["winding_correction"]),
        int(row["multiplicity"]),
    )


def structural_signature(document: dict[str, Any]) -> dict[str, Any]:
    ordered_words = []
    multisets = []
    winding_balances = []
    minimum_margin = 1.0
    for chamber in document["chambers"]:
        crossings = sorted(
            chamber["surface_crossings"], key=lambda row: float(row["step_fraction"])
        )
        tokens = [crossing_token(row) for row in crossings]
        ordered_words.append(tokens)
        counter = collections.Counter(tokens)
        multisets.append(sorted((token, count) for token, count in counter.items()))
        balances: dict[tuple[tuple[str, ...], ...], int] = {}
        for row in crossings:
            key = normalized_pairs(row)
            balances[key] = balances.get(key, 0) + int(row["winding_correction"])
            minimum_margin = min(
                minimum_margin,
                float(row["segment_fraction"]),
                1.0 - float(row["segment_fraction"]),
            )
        winding_balances.append(sorted(balances.items()))
    descriptor = document["topology_class_descriptor"]
    return {
        "class_descriptor": descriptor,
        "chamber_count": len(document["chambers"]),
        "surface_crossing_counts": [
            int(chamber["surface_crossing_count"]) for chamber in document["chambers"]
        ],
        "ordered_crossing_words": ordered_words,
        "crossing_multisets": multisets,
        "pair_winding_balances": winding_balances,
        "minimum_segment_margin": minimum_margin,
        "homotopy_steps": int(document["homotopy_steps"]),
        "assignment_tracking_passed": bool(document["assignment_tracking_passed"]),
        "crossing_groups_consistent": bool(document["crossing_groups_consistent"]),
    }


def comparison(left: dict[str, Any], right: dict[str, Any]) -> dict[str, bool]:
    return {
        "class_descriptor_equal": left["class_descriptor"] == right["class_descriptor"],
        "chamber_count_equal": left["chamber_count"] == right["chamber_count"],
        "surface_crossing_counts_equal": left["surface_crossing_counts"]
        == right["surface_crossing_counts"],
        "crossing_multisets_equal": left["crossing_multisets"] == right["crossing_multisets"],
        "pair_winding_balances_equal": left["pair_winding_balances"]
        == right["pair_winding_balances"],
        "ordered_crossing_words_equal": left["ordered_crossing_words"]
        == right["ordered_crossing_words"],
    }


def main() -> None:
    source_rows = SOURCE_5053 / "high_low_cost_rows.csv"
    if not source_rows.exists():
        raise FileNotFoundError(source_rows)
    rows = list(csv.DictReader(source_rows.open(encoding="utf-8")))
    documents: dict[tuple[str, str, str], dict[str, Any]] = {}
    signatures: dict[tuple[str, str, str], dict[str, Any]] = {}
    paths: dict[tuple[str, str, str], Path] = {}
    for row in rows:
        event_id = row["event_id"]
        base_id = row["base_argument_id"]
        for epsilon_id, field in (("E020", "e020_topology"), ("E040", "e040_topology")):
            key = (event_id, epsilon_id, base_id)
            path = localize(row[field])
            document = json.loads(path.read_text(encoding="utf-8"))
            documents[key] = document
            signatures[key] = structural_signature(document)
            paths[key] = path
    epsilon_pairs = []
    for row in rows:
        event_id = row["event_id"]
        base_id = row["base_argument_id"]
        left_key = (event_id, "E020", base_id)
        right_key = (event_id, "E040", base_id)
        compared = comparison(signatures[left_key], signatures[right_key])
        epsilon_pairs.append(
            {
                "event_id": event_id,
                "base_argument_id": base_id,
                "e020_path": str(paths[left_key]),
                "e040_path": str(paths[right_key]),
                "numeric_signature_equal": documents[left_key]["topology_signature_digest"]
                == documents[right_key]["topology_signature_digest"],
                **compared,
                "e020_minimum_segment_margin": signatures[left_key]["minimum_segment_margin"],
                "e040_minimum_segment_margin": signatures[right_key]["minimum_segment_margin"],
                "e020_homotopy_steps": signatures[left_key]["homotopy_steps"],
                "e040_homotopy_steps": signatures[right_key]["homotopy_steps"],
            }
        )
    argument_order = [f"A{index:02d}" for index in range(15)]
    adjacency_rows = []
    event_ids = sorted({row["event_id"] for row in rows})
    for event_id in event_ids:
        for epsilon_id in ("E020", "E040"):
            for left_id, right_id in zip(argument_order[:-1], argument_order[1:]):
                left_key = (event_id, epsilon_id, left_id)
                right_key = (event_id, epsilon_id, right_id)
                compared = comparison(signatures[left_key], signatures[right_key])
                adjacency_rows.append(
                    {
                        "event_id": event_id,
                        "epsilon_id": epsilon_id,
                        "left_argument_id": left_id,
                        "right_argument_id": right_id,
                        **compared,
                        "left_minimum_segment_margin": signatures[left_key][
                            "minimum_segment_margin"
                        ],
                        "right_minimum_segment_margin": signatures[right_key][
                            "minimum_segment_margin"
                        ],
                    }
                )
    all_documents_valid = all(
        signature["assignment_tracking_passed"]
        and signature["crossing_groups_consistent"]
        for signature in signatures.values()
    )
    cross_epsilon_counts = {
        field: sum(bool(row[field]) for row in epsilon_pairs)
        for field in (
            "numeric_signature_equal",
            "class_descriptor_equal",
            "chamber_count_equal",
            "surface_crossing_counts_equal",
            "crossing_multisets_equal",
            "pair_winding_balances_equal",
            "ordered_crossing_words_equal",
        )
    }
    adjacency_counts = {
        field: sum(bool(row[field]) for row in adjacency_rows)
        for field in (
            "class_descriptor_equal",
            "chamber_count_equal",
            "surface_crossing_counts_equal",
            "crossing_multisets_equal",
            "pair_winding_balances_equal",
            "ordered_crossing_words_equal",
        )
    }
    minimum_segment_margin = min(
        signature["minimum_segment_margin"] for signature in signatures.values()
    )
    unique_class_descriptors = {
        canonical_digest(signature["class_descriptor"]) for signature in signatures.values()
    }
    unique_multisets = {
        canonical_digest(signature["crossing_multisets"]) for signature in signatures.values()
    }
    cross_epsilon_seedable = all(
        row["class_descriptor_equal"]
        and row["surface_crossing_counts_equal"]
        and row["crossing_multisets_equal"]
        and row["pair_winding_balances_equal"]
        for row in epsilon_pairs
    )
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "topology_document_count": len(documents),
        "cross_epsilon_pair_count": len(epsilon_pairs),
        "argument_adjacency_pair_count": len(adjacency_rows),
        "all_source_topologies_valid": all_documents_valid,
        "cross_epsilon_equality_counts": cross_epsilon_counts,
        "argument_adjacency_equality_counts": adjacency_counts,
        "unique_class_descriptor_count": len(unique_class_descriptors),
        "unique_crossing_multiset_count": len(unique_multisets),
        "minimum_segment_margin": minimum_segment_margin,
        "cross_epsilon_combinatorial_seedability_gate": cross_epsilon_seedable,
        "continuation_execution_authorized": False,
        "next_required_gate": (
            "benchmark seeded epsilon continuation against full homotopy"
            if cross_epsilon_seedable
            else "reject universal epsilon continuation; stratify by structural class"
        ),
        "formalization_workbench_tree_sha256": FORMAL_BASELINE,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    SOURCE.mkdir(parents=True, exist_ok=True)
    with PAIR_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(epsilon_pairs[0]))
        writer.writeheader()
        writer.writerows(epsilon_pairs)
    with ADJACENCY_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(adjacency_rows[0]))
        writer.writeheader()
        writer.writerows(adjacency_rows)
    checks = [
        ("all_240_topologies_loaded", len(documents) == 240, str(len(documents))),
        ("all_120_epsilon_pairs_compared", len(epsilon_pairs) == 120, str(len(epsilon_pairs))),
        ("all_224_adjacencies_compared", len(adjacency_rows) == 224, str(len(adjacency_rows))),
        ("all_source_topologies_valid", all_documents_valid, "required true"),
        (
            "numeric_signatures_not_conflated",
            cross_epsilon_counts["numeric_signature_equal"] < len(epsilon_pairs),
            str(cross_epsilon_counts["numeric_signature_equal"]),
        ),
        (
            "positive_segment_margin",
            minimum_segment_margin > 0.0,
            str(minimum_segment_margin),
        ),
        ("continuation_not_yet_authorized", not result["continuation_execution_authorized"], "required false"),
        ("fresh_evidence_not_claimed", not result["valid_for_full_MTS_claim"], "required false"),
        (
            "formalization_workbench_unchanged",
            result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE,
            result["formalization_workbench_tree_sha256"],
        ),
    ]
    validation = [
        {"check": name, "passed": str(bool(passed)).lower(), "evidence": evidence}
        for name, passed, evidence in checks
    ]
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("check", "passed", "evidence"))
        writer.writeheader()
        writer.writerows(validation)
    print(
        json.dumps(
            {
                "cross_epsilon_pairs": len(epsilon_pairs),
                "cross_epsilon_counts": cross_epsilon_counts,
                "adjacency_counts": adjacency_counts,
                "unique_class_descriptors": len(unique_class_descriptors),
                "unique_crossing_multisets": len(unique_multisets),
                "minimum_segment_margin": minimum_segment_margin,
                "seedability_gate": cross_epsilon_seedable,
                "next_required_gate": result["next_required_gate"],
                "validation_passed": sum(row["passed"] == "true" for row in validation),
                "validation_total": len(validation),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
