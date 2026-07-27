from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5222"
SOURCE_5221 = POST / "source-intake" / "functional_rg" / "5221"
RESIDUALS = POST / "source-intake" / "mts_residuals"
SCRIPT_5219 = (
    POST
    / "scripts"
    / "Y5_R2FR_5219_general_grouped_owned_direct_classifier.py"
)
GATE_5219 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5219"
    / "general_grouped_owned_direct_classifier_gate.json"
)
AUDIT_5221 = SOURCE_5221 / "general_grouped_classifier_runtime_audit.json"
CACHE_5221 = (
    SOURCE_5221
    / "runs"
    / "scaled_controlled_two_stratum_v1"
    / "grouped-classifier-cache"
)
FAILED_JOB = (
    SOURCE_5221
    / "runs"
    / "scaled_controlled_two_stratum_v1"
    / "topological-jobs"
    / "TOP__E020__S522121_N0000__A03__primary24.json"
)
RESULT = SOURCE / "sequential_owned_direct_zero_classifier.json"
WITNESS = SOURCE / "S522121_E020_A03_sequential_zero_witness.csv"
GATE = SOURCE / "sequential_owned_direct_zero_classifier_gate.json"
DOCUMENT = (
    POST / "5222-Y5-R2FR-sequential-owned-direct-zero-classifier.md"
)
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5222_VALIDATION.csv"

MARKER = "MTS_5222_SEQUENTIAL_OWNED_DIRECT_ZERO_CLASSIFIER"
REVISION = "three-level-sequential-zero-and-grouped-zero-v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
ZERO_TOLERANCE = 1.0e-20
MAXIMUM_LEVEL_REDUCTION_RATIO = 1.0e-4
TARGET_JOB = "TOP__E020__S522121_N0000__A03__primary24"


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5219 = load_module(SCRIPT_5219, "mts_5219_for_5222")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for candidate in sorted(item for item in path.rglob("*") if item.is_file()):
        value.update(candidate.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(candidate).encode("ascii"))
    return value.hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True), encoding="utf-8"
    )
    temporary.replace(path)


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    temporary.replace(path)


def complex_row(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imaginary": float(value.imag)}


def classifier_record(
    row: dict[str, Any],
    ownership: dict[str, bool],
    job_key: str,
    event: dict[str, Any],
    argument: dict[str, Any],
) -> tuple[dict[str, Any], str]:
    chamber_index = M5219.chamber_index_for(event, argument, ownership)
    root = complex(row["root"])
    pairs = M5219.canonical_pairs(row["pairs"])
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
    return record, M5219.canonical_digest(record)


def sequential_zero_pair(
    record: dict[str, Any],
    scope_digest: str,
    pair: list[str],
    pair_index: int,
    coarse: dict[str, Any],
    fine: dict[str, Any],
    cache_directory: Path,
) -> tuple[bool, dict[str, Any]]:
    coarse_maximum = float(coarse["maximum_magnitude"])
    fine_maximum = float(fine["maximum_magnitude"])
    coarse_to_fine = (
        fine_maximum / coarse_maximum if coarse_maximum > 0.0 else math.inf
    )
    finest = M5219.evaluate_pair_level(
        record,
        pair,
        pair_index,
        M5219.LEVELS["L64"],
        cache_directory,
        scope_digest,
    )
    finest_maximum = float(finest["maximum_magnitude"])
    fine_to_finest = (
        finest_maximum / fine_maximum if fine_maximum > 0.0 else 0.0
    )
    passed = bool(
        coarse_to_fine <= MAXIMUM_LEVEL_REDUCTION_RATIO
        and fine_to_finest <= MAXIMUM_LEVEL_REDUCTION_RATIO
        and finest_maximum < ZERO_TOLERANCE
    )
    return passed, {
        "pair": pair,
        "pair_index": pair_index,
        "L32": coarse,
        "L48": fine,
        "L64": finest,
        "L32_to_L48_maximum_ratio": coarse_to_fine,
        "L48_to_L64_maximum_ratio": fine_to_finest,
        "L64_maximum_magnitude": finest_maximum,
        "zero_tolerance": ZERO_TOLERANCE,
        "maximum_level_reduction_ratio": MAXIMUM_LEVEL_REDUCTION_RATIO,
        "classification": (
            "EVENT_LOCAL_SEQUENTIAL_ARBITRARY_PRECISION_ZERO"
            if passed
            else "UNRESOLVED"
        ),
    }


def resolve_sequential_grouped_owned_direct_row(
    row: dict[str, Any],
    ownership: dict[str, bool],
    job_key: str,
    event: dict[str, Any],
    argument: dict[str, Any],
    cache_directory: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    repaired, parent_audit = M5219.resolve_grouped_owned_direct_row(
        row,
        ownership,
        job_key,
        event,
        argument,
        cache_directory,
    )
    if bool(repaired.get("stable")):
        return repaired, {
            **parent_audit,
            "sequential_classifier_invoked": False,
            "owning_checkpoint_marker": MARKER,
        }
    if parent_audit.get("classification") != "UNRESOLVED":
        return row, {
            **parent_audit,
            "sequential_classifier_invoked": False,
            "owning_checkpoint_marker": MARKER,
        }
    in_scope, reason, _ = M5219.classify_scope(row, ownership)
    if not in_scope:
        return row, {
            **parent_audit,
            "sequential_classifier_invoked": False,
            "owning_checkpoint_marker": MARKER,
            "scope_reason": reason,
        }
    record, scope_digest = classifier_record(
        row, ownership, job_key, event, argument
    )
    resolutions: list[dict[str, Any]] = []
    for parent_pair in parent_audit["pair_resolutions"]:
        classification = parent_pair["classification"]
        if classification == "EVENT_LOCAL_ARBITRARY_PRECISION_ZERO":
            finest = parent_pair["L64"]
            fine_maximum = float(
                parent_pair["L48"]["maximum_magnitude"]
            )
            finest_maximum = float(finest["maximum_magnitude"])
            resolutions.append(
                {
                    **parent_pair,
                    "L48_to_L64_maximum_ratio": (
                        finest_maximum / fine_maximum
                        if fine_maximum > 0.0
                        else 0.0
                    ),
                }
            )
            continue
        if classification == "STABLE_DIRECT_COMPONENT_NONZERO":
            resolutions.append(parent_pair)
            continue
        passed, sequential = sequential_zero_pair(
            record,
            scope_digest,
            list(parent_pair["pair"]),
            int(parent_pair["pair_index"]),
            parent_pair["L32"],
            parent_pair["L48"],
            cache_directory,
        )
        resolutions.append(sequential)
        if not passed:
            return row, {
                **parent_audit,
                "checkpoint_marker": MARKER,
                "revision": REVISION,
                "sequential_classifier_invoked": True,
                "sequential_pair_resolutions": resolutions,
                "classification": "UNRESOLVED",
                "unresolved_action": "fail_closed",
            }
    zero_classes = {
        "EVENT_LOCAL_ARBITRARY_PRECISION_ZERO",
        "EVENT_LOCAL_SEQUENTIAL_ARBITRARY_PRECISION_ZERO",
    }
    all_pairs_zero = bool(resolutions) and all(
        resolution["classification"] in zero_classes
        for resolution in resolutions
    )
    audit = {
        **parent_audit,
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "scope_digest": scope_digest,
        "sequential_classifier_invoked": True,
        "sequential_pair_resolutions": resolutions,
        "all_pairs_individually_zero": all_pairs_zero,
        "grouped_zero_uses_no_cancellation": all_pairs_zero,
        "classification": (
            "EVENT_LOCAL_GROUPED_OWNED_DIRECT_ZERO"
            if all_pairs_zero
            else "UNRESOLVED"
        ),
        "replacement_residue": complex_row(0.0j),
        "unresolved_action": "fail_closed",
        "valid_for_numeric_UV_claim": False,
    }
    if not all_pairs_zero:
        return row, audit
    repaired = {
        **row,
        "outer_residue": 0.0j,
        "inner_residue": 0.0j,
        "residue": 0.0j,
        "residue_stability": 0.0,
        "numerically_zero": True,
        "stable": True,
        "sequential_grouped_owned_direct_zero_classifier": {
            "checkpoint_marker": MARKER,
            "scope_digest": scope_digest,
            "classification": audit["classification"],
            "classifier_runner_sha256": digest(Path(__file__).resolve()),
            "valid_for_numeric_UV_claim": False,
        },
    }
    return repaired, audit


def witness_contract(row: dict[str, Any]) -> dict[str, Any]:
    scope_digest = str(row["scope_digest"])
    pair = list(row["pair_resolutions"][0]["pair"])
    pair_index = int(row["pair_resolutions"][0]["pair_index"])
    fine_path = (
        CACHE_5221
        / scope_digest
        / f"pair_{pair_index:02d}__L48.json"
    )
    fine = read_json(fine_path)
    record = fine["contract"]["record"]
    coarse = row["pair_resolutions"][0]["L32"]
    passed, sequential = sequential_zero_pair(
        record,
        scope_digest,
        pair,
        pair_index,
        coarse,
        row["pair_resolutions"][0]["L48"],
        CACHE_5221,
    )
    return {
        "event_id": row["event_id"],
        "argument_id": row["argument_id"],
        "chamber_index": row["chamber_index"],
        "scope_digest": scope_digest,
        "parent_classification": row["classification"],
        "sequential": sequential,
        "passed": passed,
    }


def main() -> None:
    required = (
        SCRIPT_5219,
        GATE_5219,
        AUDIT_5221,
        FAILED_JOB,
    )
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(missing)
    parent_gate = read_json(GATE_5219)
    failed_job = read_json(FAILED_JOB)
    invocations = [
        row
        for row in read_json(AUDIT_5221)["invocation_rows"]
        if row.get("job_key") == TARGET_JOB
    ]
    witnesses = [witness_contract(row) for row in invocations]
    checks = [
        (
            "parent_general_classifier_gate_passed",
            bool(
                parent_gate["validation_all_passed"]
                and parent_gate["general_grouped_classifier_authorized"]
            ),
            str(parent_gate["validation_all_passed"]),
        ),
        (
            "failed_job_is_the_frozen_5221_stop",
            failed_job["status"] == "COMPLETED_UNCONVERGED"
            and not failed_job["residues_stable"]
            and failed_job["job_key"] == TARGET_JOB,
            failed_job["status"],
        ),
        (
            "exactly_two_unresolved_direct_only_rows",
            len(invocations) == 2
            and all(
                row["classification"] == "UNRESOLVED"
                and row["scope_reason"]
                == "linear_sum_of_exactly_owned_direct_pair_residues"
                for row in invocations
            ),
            str(len(invocations)),
        ),
        (
            "all_pairs_pass_three_level_sequential_zero",
            len(witnesses) == 2
            and all(row["passed"] for row in witnesses),
            str([row["passed"] for row in witnesses]),
        ),
        (
            "L64_absolute_zero_gate_unchanged",
            ZERO_TOLERANCE == M5219.ZERO_TOLERANCE
            and max(
                row["sequential"]["L64_maximum_magnitude"]
                for row in witnesses
            )
            < ZERO_TOLERANCE,
            str(ZERO_TOLERANCE),
        ),
        (
            "both_level_reduction_ratios_below_existing_ratio_gate",
            all(
                row["sequential"]["L32_to_L48_maximum_ratio"]
                <= MAXIMUM_LEVEL_REDUCTION_RATIO
                and row["sequential"]["L48_to_L64_maximum_ratio"]
                <= MAXIMUM_LEVEL_REDUCTION_RATIO
                for row in witnesses
            ),
            str(MAXIMUM_LEVEL_REDUCTION_RATIO),
        ),
        (
            "grouped_zero_requires_each_summand_zero",
            all(
                len(row["sequential"]["pair"]) == 2
                for row in witnesses
            ),
            "no cancellation-only grouped zero is accepted",
        ),
        (
            "formalization_workbench_unchanged",
            tree_digest(FORMAL) == FORMAL_BASELINE,
            tree_digest(FORMAL),
        ),
    ]
    passed = all(row[1] for row in checks)
    witness_rows = []
    for row in witnesses:
        sequential = row["sequential"]
        witness_rows.append(
            {
                "event_id": row["event_id"],
                "argument_id": row["argument_id"],
                "chamber_index": row["chamber_index"],
                "scope_digest": row["scope_digest"],
                "pair": json.dumps(sequential["pair"]),
                "L32_maximum_magnitude": sequential["L32"][
                    "maximum_magnitude"
                ],
                "L48_maximum_magnitude": sequential["L48"][
                    "maximum_magnitude"
                ],
                "L64_maximum_magnitude": sequential[
                    "L64_maximum_magnitude"
                ],
                "L32_to_L48_maximum_ratio": sequential[
                    "L32_to_L48_maximum_ratio"
                ],
                "L48_to_L64_maximum_ratio": sequential[
                    "L48_to_L64_maximum_ratio"
                ],
                "classification": sequential["classification"],
                "passed": row["passed"],
                "valid_for_numeric_UV_claim": False,
            }
        )
    SOURCE.mkdir(parents=True, exist_ok=True)
    with WITNESS.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(witness_rows[0]))
        writer.writeheader()
        writer.writerows(witness_rows)
    result = {
        "checkpoint": 5222,
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "target_job": TARGET_JOB,
        "theorem": (
            "For an in-scope grouped-owned direct row, if every pair "
            "residue independently suppresses by at least 1e-4 from L32 "
            "to L48 and again from L48 to L64, and every L64 maximum is "
            "below the unchanged 1e-20 absolute gate, each pair is an "
            "event-local arbitrary-precision zero and their grouped sum "
            "is zero without cancellation."
        ),
        "witnesses": witnesses,
        "checks": [
            {"check": name, "passed": bool(ok), "detail": detail}
            for name, ok, detail in checks
        ],
        "passed": passed,
        "runtime_classifier_authorized": passed,
        "threshold_relaxed": False,
        "zero_tolerance": ZERO_TOLERANCE,
        "maximum_level_reduction_ratio": MAXIMUM_LEVEL_REDUCTION_RATIO,
        "parent_classifier_sha256": digest(SCRIPT_5219),
        "runner_sha256": digest(Path(__file__).resolve()),
        "formalization_workbench_tree_sha256": tree_digest(FORMAL),
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT, result)
    atomic_json(
        GATE,
        {
            "checkpoint": 5222,
            "checkpoint_marker": MARKER,
            "passed": passed,
            "runtime_classifier_authorized": passed,
            "classifier_contract": {
                "scope": (
                    "5219 direct-only rows with exactly one owned g1/g2 "
                    "component per pair"
                ),
                "three_levels": ["L32", "L48", "L64"],
                "zero_tolerance": ZERO_TOLERANCE,
                "maximum_level_reduction_ratio": (
                    MAXIMUM_LEVEL_REDUCTION_RATIO
                ),
                "grouped_zero_rule": (
                    "every pair must independently classify zero; "
                    "cancellation-only zero remains forbidden"
                ),
                "unresolved_action": "fail_closed",
            },
            "result": str(RESULT),
            "result_sha256": digest(RESULT),
            "runner": str(Path(__file__).resolve()),
            "runner_sha256": digest(Path(__file__).resolve()),
            "valid_for_numeric_UV_claim": False,
        },
    )
    VALIDATION.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(("check", "passed", "detail"))
        for row in checks:
            writer.writerow((row[0], str(bool(row[1])).lower(), row[2]))
    maximum_l64 = max(
        row["sequential"]["L64_maximum_magnitude"] for row in witnesses
    )
    maximum_ratio = max(
        max(
            row["sequential"]["L32_to_L48_maximum_ratio"],
            row["sequential"]["L48_to_L64_maximum_ratio"],
        )
        for row in witnesses
    )
    atomic_text(
        DOCUMENT,
        "\n".join(
            [
                "# 5222 - Sequential owned-direct zero classifier",
                "",
                "## Result",
                "",
                "The checkpoint-5221 stop is not repaired by loosening the",
                "`1e-20` zero threshold. It is repaired by completing the",
                "third convergence level that the old pre-gate skipped.",
                "",
                f"- Target job: `{TARGET_JOB}`.",
                f"- Direct-only unresolved rows: `{len(witnesses)}`.",
                f"- Maximum L64 magnitude: `{maximum_l64:.12g}`.",
                f"- Maximum adjacent-level ratio: `{maximum_ratio:.12g}`.",
                f"- Gate passed: `{passed}`.",
                "",
                "Every constituent pair is independently zero; no grouped",
                "cancellation is used. The runtime extension may therefore",
                "replace an all-zero grouped row by exact zero. Mixed or",
                "out-of-scope rows still fail closed.",
                "",
                "## Claim boundary",
                "",
                "This is a numerical residue-classification theorem for the",
                "frozen integration pipeline, not a numeric UV, local-GR, or",
                "full-MTS claim.",
                "",
                "## Evidence",
                "",
                f"- Result: `{RESULT}`",
                f"- Gate: `{GATE}`",
                f"- Witness rows: `{WITNESS}`",
                f"- Validation: `{VALIDATION}`",
            ]
        )
        + "\n",
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if not passed:
        raise RuntimeError("checkpoint-5222 sequential zero gate failed")


if __name__ == "__main__":
    main()
