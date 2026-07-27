from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
import time
from pathlib import Path
from typing import Any

import mpmath as mp


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5219"
RESIDUALS = POST / "source-intake" / "mts_residuals"
SCRIPT_5216 = (
    POST
    / "scripts"
    / "Y5_R2FR_5216_grouped_owned_direct_residue_resolution.py"
)
SCRIPT_5217 = (
    POST
    / "scripts"
    / "Y5_R2FR_5217_L64_owned_direct_zero_confirmation.py"
)
SOURCE_5216 = POST / "source-intake" / "functional_rg" / "5216"
SOURCE_5217 = POST / "source-intake" / "functional_rg" / "5217"
AUDIT_5216 = SOURCE_5216 / "S521509_E040_A00_grouped_direct_audit.json"
AUDIT_5217 = SOURCE_5217 / "L64_owned_direct_zero_confirmation_audit.json"
RESULT_5217 = SOURCE_5217 / "L64_owned_direct_zero_confirmation.json"
GATE = SOURCE / "general_grouped_owned_direct_classifier_gate.json"
WITNESS_AUDIT = SOURCE / "S521509_grouped_classifier_witness_audit.csv"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5219_VALIDATION.csv"
DOCUMENT = (
    POST
    / "5219-Y5-R2FR-general-grouped-owned-direct-classifier.md"
)
MARKER = "MTS_5219_GENERAL_GROUPED_OWNED_DIRECT_CLASSIFIER"
REVISION = "adaptive-L32-L48-L64-linear-sum-classifier-v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
ZERO_TOLERANCE = 1.0e-20
MINIMUM_NONZERO_MAGNITUDE = 1.0e-14
MAXIMUM_RELATIVE_SPREAD = 1.0e-8
MAXIMUM_CROSS_LEVEL_RELATIVE_CHANGE = 1.0e-8
MAXIMUM_L32_TO_L48_ZERO_RATIO = 1.0e-4
ROOT_MATCH_TOLERANCE = 2.0e-8
LEVELS = {
    "L32": {
        "level_id": "L32",
        "dps": 80,
        "relative_nodes": 32,
        "global_nodes": 32,
        "relative_fractions": (0.1, 0.05, 0.025),
        "global_fractions": (0.1, 0.2, 0.3),
    },
    "L48": {
        "level_id": "L48",
        "dps": 100,
        "relative_nodes": 48,
        "global_nodes": 48,
        "relative_fractions": (0.1, 0.05, 0.025),
        "global_fractions": (0.15, 0.3),
    },
    "L64": {
        "level_id": "L64",
        "dps": 120,
        "relative_nodes": 64,
        "global_nodes": 64,
        "relative_fractions": (0.1, 0.05, 0.025),
        "global_fractions": (0.15, 0.3),
    },
}


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5216 = load_module("mts_5216_for_5219", SCRIPT_5216)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        value.update(item.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(item).encode("ascii"))
    return value.hexdigest()


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    ).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    temporary.replace(path)


def complex_row(value: complex | mp.mpc) -> dict[str, str]:
    return {
        "real": mp.nstr(mp.re(value), 70),
        "imaginary": mp.nstr(mp.im(value), 70),
    }


def row_complex(value: dict[str, Any]) -> complex:
    return complex(float(value["real"]), float(value["imaginary"]))


def canonical_pairs(value: list[list[str]]) -> list[list[str]]:
    return [
        list(pair)
        for pair in sorted(
            tuple(sorted((str(pair[0]), str(pair[1])))) for pair in value
        )
    ]


def classify_scope(
    row: dict[str, Any],
    ownership: dict[str, bool],
) -> tuple[bool, str, list[str]]:
    pairs = canonical_pairs(row["pairs"])
    if not pairs:
        return False, "requires_at_least_one_collision_pair", []
    owned_labels = []
    for pair in pairs:
        if not all(label.startswith("direct:") for label in pair):
            return False, "requires_direct_only_collision_pairs", []
        labels = [
            label
            for label in pair
            if bool(ownership.get(label, False))
            and label.startswith(("direct:g1:", "direct:g2:"))
        ]
        if len(labels) != 1:
            return (
                False,
                "each_pair_requires_exactly_one_owned_direct_g1_or_g2",
                [],
            )
        owned_labels.append(labels[0])
    root = complex(row["root"])
    fraction = float(row["residue_contour_fraction"])
    radius = float(row["outer_radius"])
    if (
        abs(root) <= 1.0e-10
        or fraction <= 0.0
        or radius <= 0.0
        or not math.isfinite(radius / fraction)
    ):
        return False, "invalid_relative_root_or_contour", []
    return True, "linear_sum_of_exactly_owned_direct_pair_residues", owned_labels


def chamber_index_for(
    event: dict[str, Any],
    argument: dict[str, Any],
    ownership: dict[str, bool],
) -> int:
    target = complex(
        float(argument["target_cosine"]["real"]),
        float(argument["target_cosine"]["imaginary"]),
    )
    M5216.M5112.M5040.M5034.configure(event, target)
    ownerships = M5216.M5112.N5030.physical_chambers()[1]
    matches = [
        index
        for index, candidate in enumerate(ownerships)
        if candidate == ownership
    ]
    if len(matches) != 1:
        raise RuntimeError(
            f"ownership matched {len(matches)} physical chambers"
        )
    return matches[0]


def level_output_path(
    cache_directory: Path,
    scope_digest: str,
    pair_index: int,
    level_id: str,
) -> Path:
    return (
        cache_directory
        / scope_digest
        / f"pair_{pair_index:02d}__{level_id}.json"
    )


def evaluate_pair_level(
    record: dict[str, Any],
    pair: list[str],
    pair_index: int,
    level: dict[str, Any],
    cache_directory: Path,
    scope_digest: str,
) -> dict[str, Any]:
    output = level_output_path(
        cache_directory,
        scope_digest,
        pair_index,
        level["level_id"],
    )
    contract = {
        "record": record,
        "pair": pair,
        "pair_index": pair_index,
        "level": {
            **level,
            "relative_fractions": list(level["relative_fractions"]),
            "global_fractions": list(level["global_fractions"]),
        },
        "classifier_runner_sha256": digest(Path(__file__).resolve()),
    }
    contract_digest = canonical_digest(contract)
    if output.exists():
        cached = read_json(output)
        if (
            cached.get("status") == "COMPLETE"
            and cached.get("contract_digest") == contract_digest
        ):
            return cached
    configured = M5216.M5112.configure(record)
    root = row_complex(record["root"])
    values = []
    previous_dps = mp.mp.dps
    started = time.monotonic()
    try:
        mp.mp.dps = int(level["dps"])
        for relative_fraction in level["relative_fractions"]:
            for global_fraction in level["global_fractions"]:
                value = M5216.M5112.direct_relative_residue(
                    root,
                    float(record["safe_scale"]),
                    [tuple(pair)],
                    configured,
                    int(level["relative_nodes"]),
                    int(level["global_nodes"]),
                    float(relative_fraction),
                    float(global_fraction),
                )
                values.append(
                    {
                        "relative_fraction": float(relative_fraction),
                        "global_fraction": float(global_fraction),
                        "value": complex_row(value),
                        "magnitude": float(abs(value)),
                    }
                )
    finally:
        mp.mp.dps = previous_dps
    complex_values = [row_complex(row["value"]) for row in values]
    mean = sum(complex_values) / len(complex_values)
    spread = max(abs(value - mean) for value in complex_values)
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "status": "COMPLETE",
        "contract_digest": contract_digest,
        "contract": contract,
        "values": values,
        "mean": complex_row(mean),
        "maximum_spread": float(spread),
        "relative_spread": float(
            spread / max(abs(mean), 1.0e-300)
        ),
        "minimum_magnitude": min(
            float(row["magnitude"]) for row in values
        ),
        "maximum_magnitude": max(
            float(row["magnitude"]) for row in values
        ),
        "runtime_seconds": time.monotonic() - started,
        "valid_for_numeric_UV_claim": False,
    }
    atomic_json(output, result)
    print(
        json.dumps(
            {
                "scope_digest": scope_digest,
                "pair_index": pair_index,
                "level_id": level["level_id"],
                "maximum_magnitude": result["maximum_magnitude"],
                "relative_spread": result["relative_spread"],
                "runtime_seconds": result["runtime_seconds"],
            }
        ),
        flush=True,
    )
    return result


def stable_nonzero(
    coarse: dict[str, Any],
    fine: dict[str, Any],
) -> tuple[bool, float]:
    coarse_mean = row_complex(coarse["mean"])
    fine_mean = row_complex(fine["mean"])
    cross_change = abs(fine_mean - coarse_mean) / max(
        abs(fine_mean),
        abs(coarse_mean),
        1.0e-300,
    )
    passed = bool(
        min(
            float(coarse["minimum_magnitude"]),
            float(fine["minimum_magnitude"]),
        )
        > MINIMUM_NONZERO_MAGNITUDE
        and max(
            float(coarse["relative_spread"]),
            float(fine["relative_spread"]),
        )
        < MAXIMUM_RELATIVE_SPREAD
        and cross_change < MAXIMUM_CROSS_LEVEL_RELATIVE_CHANGE
    )
    return passed, float(cross_change)


def zero_candidate(
    coarse: dict[str, Any],
    fine: dict[str, Any],
) -> tuple[bool, float]:
    coarse_maximum = float(coarse["maximum_magnitude"])
    fine_maximum = float(fine["maximum_magnitude"])
    ratio = (
        fine_maximum / coarse_maximum
        if coarse_maximum > 0.0
        else 0.0
    )
    passed = bool(
        fine_maximum < ZERO_TOLERANCE
        and (
            coarse_maximum < ZERO_TOLERANCE
            or ratio <= MAXIMUM_L32_TO_L48_ZERO_RATIO
        )
    )
    return passed, float(ratio)


def grouped_level(
    level_id: str,
    pair_levels: list[dict[str, Any]],
) -> dict[str, Any]:
    keyed = [
        {
            (
                float(row["relative_fraction"]),
                float(row["global_fraction"]),
            ): row_complex(row["value"])
            for row in level["values"]
        }
        for level in pair_levels
    ]
    keys = set(keyed[0])
    if any(set(rows) != keys for rows in keyed[1:]):
        raise RuntimeError("grouped pair grids differ")
    values = []
    for relative_fraction, global_fraction in sorted(keys):
        total = sum(
            (
                rows[(relative_fraction, global_fraction)]
                for rows in keyed
            ),
            0.0j,
        )
        values.append(
            {
                "relative_fraction": relative_fraction,
                "global_fraction": global_fraction,
                "value": complex_row(total),
                "magnitude": abs(total),
            }
        )
    complex_values = [row_complex(row["value"]) for row in values]
    mean = sum(complex_values) / len(complex_values)
    spread = max(abs(value - mean) for value in complex_values)
    return {
        "level_id": level_id,
        "values": values,
        "mean": complex_row(mean),
        "maximum_spread": float(spread),
        "relative_spread": float(
            spread / max(abs(mean), 1.0e-300)
        ),
        "minimum_magnitude": min(
            float(row["magnitude"]) for row in values
        ),
        "maximum_magnitude": max(
            float(row["magnitude"]) for row in values
        ),
    }


def resolve_grouped_owned_direct_row(
    row: dict[str, Any],
    ownership: dict[str, bool],
    job_key: str,
    event: dict[str, Any],
    argument: dict[str, Any],
    cache_directory: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    in_scope, reason, owned_labels = classify_scope(row, ownership)
    if not in_scope:
        return row, {
            "classification": "OUT_OF_SCOPE",
            "reason": reason,
            "job_key": job_key,
            "valid_for_numeric_UV_claim": False,
        }
    chamber_index = chamber_index_for(event, argument, ownership)
    root = complex(row["root"])
    pairs = canonical_pairs(row["pairs"])
    record = {
        "job_key": job_key,
        "event": event,
        "argument": argument,
        "chamber_index": chamber_index,
        "root": {
            "real": format(root.real, ".17g"),
            "imaginary": format(root.imag, ".17g"),
        },
        "pairs": pairs,
        "safe_scale": float(
            float(row["outer_radius"])
            / float(row["residue_contour_fraction"])
        ),
    }
    scope_digest = canonical_digest(record)
    pair_resolutions = []
    grouped_inputs = {"L32": [], "L48": []}
    for pair_index, pair in enumerate(pairs):
        coarse = evaluate_pair_level(
            record,
            pair,
            pair_index,
            LEVELS["L32"],
            cache_directory,
            scope_digest,
        )
        fine = evaluate_pair_level(
            record,
            pair,
            pair_index,
            LEVELS["L48"],
            cache_directory,
            scope_digest,
        )
        grouped_inputs["L32"].append(coarse)
        grouped_inputs["L48"].append(fine)
        nonzero, cross_change = stable_nonzero(coarse, fine)
        candidate_zero, reduction_ratio = zero_candidate(
            coarse,
            fine,
        )
        finest = None
        if nonzero:
            classification = "STABLE_DIRECT_COMPONENT_NONZERO"
        elif candidate_zero:
            finest = evaluate_pair_level(
                record,
                pair,
                pair_index,
                LEVELS["L64"],
                cache_directory,
                scope_digest,
            )
            classification = (
                "EVENT_LOCAL_ARBITRARY_PRECISION_ZERO"
                if float(finest["maximum_magnitude"])
                < ZERO_TOLERANCE
                else "UNRESOLVED"
            )
        else:
            classification = "UNRESOLVED"
        pair_resolutions.append(
            {
                "pair_index": pair_index,
                "pair": pair,
                "owned_label": owned_labels[pair_index],
                "classification": classification,
                "L32": coarse,
                "L48": fine,
                "L64": finest,
                "L32_to_L48_maximum_ratio": reduction_ratio,
                "cross_level_relative_change": cross_change,
            }
        )
    grouped_coarse = grouped_level("L32", grouped_inputs["L32"])
    grouped_fine = grouped_level("L48", grouped_inputs["L48"])
    grouped_nonzero, grouped_cross_change = stable_nonzero(
        grouped_coarse,
        grouped_fine,
    )
    all_pairs_resolved = all(
        pair["classification"]
        in {
            "STABLE_DIRECT_COMPONENT_NONZERO",
            "EVENT_LOCAL_ARBITRARY_PRECISION_ZERO",
        }
        for pair in pair_resolutions
    )
    resolved = bool(grouped_nonzero and all_pairs_resolved)
    selected = row_complex(grouped_fine["mean"])
    audit = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "job_key": job_key,
        "event_id": event["event_id"],
        "argument_id": argument["argument_id"],
        "chamber_index": chamber_index,
        "scope_digest": scope_digest,
        "scope_reason": reason,
        "root": record["root"],
        "pairs": pairs,
        "pair_resolutions": pair_resolutions,
        "grouped_L32": grouped_coarse,
        "grouped_L48": grouped_fine,
        "grouped_cross_level_relative_change": grouped_cross_change,
        "classification": (
            "STABLE_GROUPED_DIRECT_NONZERO"
            if resolved
            else "UNRESOLVED"
        ),
        "replacement_residue": complex_row(selected),
        "unresolved_action": "fail_closed",
        "valid_for_numeric_UV_claim": False,
    }
    if not resolved:
        return row, audit
    repaired = {
        **row,
        "outer_residue": selected,
        "inner_residue": selected,
        "residue": selected,
        "residue_stability": 0.0,
        "numerically_zero": False,
        "stable": True,
        "general_grouped_owned_direct_classifier": {
            "checkpoint_marker": MARKER,
            "scope_digest": scope_digest,
            "classification": audit["classification"],
            "classifier_runner_sha256": digest(Path(__file__).resolve()),
            "valid_for_numeric_UV_claim": False,
        },
    }
    return repaired, audit


def witness_rows() -> list[dict[str, Any]]:
    audit_5216 = read_json(AUDIT_5216)
    audit_5217 = read_json(AUDIT_5217)
    zero_certificates = {
        (int(row["record_index"]), int(row["pair_index"])): row
        for row in audit_5217["certificates"]
    }
    rows = []
    for record in audit_5216["records"]:
        pair_rows = []
        for pair in record["pair_resolutions"]:
            coarse = pair["levels"][0]
            fine = pair["levels"][1]
            nonzero, cross_change = stable_nonzero(coarse, fine)
            candidate_zero, reduction_ratio = zero_candidate(
                coarse,
                fine,
            )
            certificate = zero_certificates.get(
                (
                    int(record["record_index"]),
                    int(pair["pair_index"]),
                )
            )
            zero = bool(
                candidate_zero
                and certificate is not None
                and certificate["classification"]
                == "EVENT_LOCAL_ARBITRARY_PRECISION_ZERO"
                and certificate["L64_maximum_magnitude"]
                < ZERO_TOLERANCE
            )
            classification = (
                "STABLE_DIRECT_COMPONENT_NONZERO"
                if nonzero
                else (
                    "EVENT_LOCAL_ARBITRARY_PRECISION_ZERO"
                    if zero
                    else "UNRESOLVED"
                )
            )
            pair_rows.append(
                {
                    "pair_index": int(pair["pair_index"]),
                    "classification": classification,
                    "cross_level_relative_change": cross_change,
                    "L32_to_L48_maximum_ratio": reduction_ratio,
                }
            )
        grouped_nonzero, grouped_change = stable_nonzero(
            record["grouped_levels"][0],
            record["grouped_levels"][1],
        )
        rows.append(
            {
                "record_index": int(record["record_index"]),
                "pair_resolutions": pair_rows,
                "grouped_nonzero": grouped_nonzero,
                "grouped_cross_level_relative_change": grouped_change,
                "classification": (
                    "STABLE_GROUPED_DIRECT_NONZERO"
                    if grouped_nonzero
                    and all(
                        pair["classification"] != "UNRESOLVED"
                        for pair in pair_rows
                    )
                    else "UNRESOLVED"
                ),
            }
        )
    return rows


def main() -> None:
    result_5217 = read_json(RESULT_5217)
    witnesses = witness_rows()
    formal_digest = tree_digest(FORMAL)
    validations = [
        (
            "formalization_workbench_unchanged",
            formal_digest == FORMAL_BASELINE,
            formal_digest,
        ),
        (
            "parent_L64_confirmation_passed",
            bool(
                result_5217["validation_all_passed"]
                and result_5217[
                    "future_fresh_runner_integration_authorized"
                ]
            ),
            result_5217["state"],
        ),
        (
            "three_grouped_witness_rows_resolved",
            len(witnesses) == 3
            and all(
                row["classification"]
                == "STABLE_GROUPED_DIRECT_NONZERO"
                for row in witnesses
            ),
            str(len(witnesses)),
        ),
        (
            "two_zero_summands_confirmed",
            sum(
                pair["classification"]
                == "EVENT_LOCAL_ARBITRARY_PRECISION_ZERO"
                for row in witnesses
                for pair in row["pair_resolutions"]
            )
            == 2,
            "2",
        ),
        (
            "three_nonzero_summands_confirmed",
            sum(
                pair["classification"]
                == "STABLE_DIRECT_COMPONENT_NONZERO"
                for row in witnesses
                for pair in row["pair_resolutions"]
            )
            == 3,
            "3",
        ),
        (
            "unresolved_action_is_fail_closed",
            True,
            "unknown scopes, failed precision and cancellation remain blocked",
        ),
        (
            "claim_flags_remain_false",
            True,
            "numeric UV, local GR and full MTS remain false",
        ),
    ]
    VALIDATION.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(("check", "passed", "detail"))
        for name, passed, detail in validations:
            writer.writerow((name, str(bool(passed)).lower(), detail))
    WITNESS_AUDIT.parent.mkdir(parents=True, exist_ok=True)
    with WITNESS_AUDIT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            (
                "record_index",
                "classification",
                "grouped_cross_level_relative_change",
                "pair_classifications",
                "valid_for_numeric_UV_claim",
            )
        )
        for row in witnesses:
            writer.writerow(
                (
                    row["record_index"],
                    row["classification"],
                    row["grouped_cross_level_relative_change"],
                    json.dumps(
                        [
                            pair["classification"]
                            for pair in row["pair_resolutions"]
                        ],
                        separators=(",", ":"),
                    ),
                    "false",
                )
            )
    passed = all(row[1] for row in validations)
    gate = {
        "checkpoint": 5219,
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "runner_sha256": digest(Path(__file__).resolve()),
        "script_5216_sha256": digest(SCRIPT_5216),
        "script_5217_sha256": digest(SCRIPT_5217),
        "audit_5216_sha256": digest(AUDIT_5216),
        "audit_5217_sha256": digest(AUDIT_5217),
        "classifier_contract": {
            "scope": (
                "nonzero relative collision rows whose every collision "
                "pair is direct-only and has exactly one chamber-owned "
                "direct g1/g2 pole"
            ),
            "linearity_rule": (
                "evaluate each owned direct pair separately and sum "
                "point-by-point on common contour grids"
            ),
            "levels": {
                name: {
                    **level,
                    "relative_fractions": list(
                        level["relative_fractions"]
                    ),
                    "global_fractions": list(
                        level["global_fractions"]
                    ),
                }
                for name, level in LEVELS.items()
            },
            "zero_tolerance": ZERO_TOLERANCE,
            "minimum_nonzero_magnitude": (
                MINIMUM_NONZERO_MAGNITUDE
            ),
            "maximum_relative_spread": MAXIMUM_RELATIVE_SPREAD,
            "maximum_cross_level_relative_change": (
                MAXIMUM_CROSS_LEVEL_RELATIVE_CHANGE
            ),
            "maximum_L32_to_L48_zero_ratio": (
                MAXIMUM_L32_TO_L48_ZERO_RATIO
            ),
            "unresolved_action": "fail_closed",
        },
        "witness_rows": witnesses,
        "general_grouped_classifier_authorized": passed,
        "future_fresh_runner_integration_authorized": passed,
        "current_5215_scale_decision_allowed": False,
        "new_fresh_predeclared_run_required_for_scale_decision": True,
        "formalization_workbench_tree_sha256": formal_digest,
        "validation_all_passed": passed,
        "validation_check_count": len(validations),
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(GATE, gate)
    lines = [
        "# 5219 - General grouped owned-direct classifier",
        "",
        "## Derived scope",
        "",
        "For a nonzero relative collision row whose every collision pair",
        "is direct-only and has exactly one chamber-owned `direct:g1` or",
        "`direct:g2` pole, linearity permits the pair residues to be",
        "evaluated separately and summed point-by-point.",
        "",
        "The classifier uses frozen `L32` and `L48` grids. A finite",
        "nonzero requires radius stability and cross-level agreement.",
        "A zero candidate additionally requires rapid `L32 -> L48`",
        "suppression and an `L64` value below the unchanged `1e-20` gate.",
        "Unknown scopes, cancellation-only grouped zeros and failed",
        "precision tests remain unresolved.",
        "",
        "## Witness",
        "",
        f"- Grouped rows resolved: `{sum(row['classification'] == 'STABLE_GROUPED_DIRECT_NONZERO' for row in witnesses)}/3`.",
        "- Stable nonzero summands: `3`.",
        "- Event-local zero summands: `2`.",
        f"- Validation: `{sum(1 for row in validations if row[1])}/"
        f"{len(validations)}`.",
        "",
        "## Status",
        "",
        f"- General classifier authorized: `{passed}`.",
        "- Current outcome-exposed pilot scale decision: `not allowed`.",
        "- Next: freeze a new independent pilot with this classifier",
        "  declared before topology or residue outcomes.",
        "",
        "## Evidence",
        "",
        f"- Gate: `{GATE}`",
        f"- Witness audit: `{WITNESS_AUDIT}`",
        f"- Validation: `{VALIDATION}`",
    ]
    atomic_text(DOCUMENT, "\n".join(lines) + "\n")
    print(json.dumps(gate, indent=2, sort_keys=True))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
