from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPT_5045_COST = POST / "scripts" / "Y5_R2FR_5045_theorem_first_primary24_cost_gate.py"
SCRIPT_5045_SCOPE = (
    POST / "scripts" / "Y5_R2FR_5045_theorem_scope_falsification_and_quarantine.py"
)
SOURCE = POST / "source-intake" / "functional_rg" / "5046"
RUN = SOURCE / "runs" / "restricted_scope_primary24_v1"
DRY_RUN_JSON = SOURCE / "dry_run.json"
BENCHMARK_JSON = SOURCE / "restricted_primary24_benchmark.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5046_VALIDATION.csv"
)
MARKER = "MTS_5046_RESTRICTED_SCOPE_PRIMARY24_BENCHMARK"
REVISION = "primary24-theorem-first-restricted-owned-direct-g1-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
EXACTNESS_THRESHOLD = 2.0e-6


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5045 = load_module("mts_5045_for_restricted_benchmark", SCRIPT_5045_COST)
SCOPE = load_module("mts_5045_scope_for_restricted_benchmark", SCRIPT_5045_SCOPE)
M5043 = M5045.M5043
N5030 = M5045.N5030
ORIGINAL_CATALOG = N5030.chamber_residue_catalog
ORIGINAL_THEOREM = M5043.M5041.theorem_certificate


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    if not path.exists():
        return "MISSING"
    for file_path in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        value.update(file_path.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(file_path).encode("ascii"))
    return value.hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def normalized_single_pair(certificate: dict[str, Any]) -> tuple[str, str] | None:
    pairs = certificate.get("pairs", [])
    if len(pairs) != 1 or len(pairs[0]) != 2:
        return None
    return tuple(sorted(str(label) for label in pairs[0]))


def restricted_certificate(
    row: dict[str, Any], ownership: dict[str, bool]
) -> dict[str, Any]:
    certificate = ORIGINAL_THEOREM(row, ownership)
    owned_labels = [str(label) for label in certificate.get("owned_labels", [])]
    pair = normalized_single_pair(certificate)
    family = (
        (owned_labels[0], pair)
        if len(owned_labels) == 1 and pair is not None
        else None
    )
    witnesses = SCOPE.proof_witnesses()
    witness = witnesses.get(pair) if pair is not None else None
    family_guard = family in SCOPE.PROVED_FAMILIES
    witness_guard = bool(witness and witness["passed"])
    certificate.update(
        {
            "broad_5041_guard_passed": bool(certificate["passed"]),
            "proved_family_guard_passed": family_guard,
            "independent_witness_guard_passed": witness_guard,
            "scope_revision": SCOPE.REVISION,
            "scope_source": str(SCRIPT_5045_SCOPE),
            "scope_source_sha256": digest(SCRIPT_5045_SCOPE),
            "passed": bool(certificate["passed"] and family_guard and witness_guard),
            "valid_for_full_MTS_claim": False,
        }
    )
    return certificate


def configure_reused_runner() -> None:
    M5045.SOURCE = SOURCE
    M5045.RUN = RUN
    M5045.BENCHMARK_JSON = BENCHMARK_JSON
    M5045.MARKER = MARKER
    M5045.REVISION = REVISION


def dry_run(document: dict[str, Any]) -> dict[str, Any]:
    reused = M5045.dry_run(document)
    result = {
        **reused,
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "scope_source": str(SCRIPT_5045_SCOPE),
        "scope_source_sha256": digest(SCRIPT_5045_SCOPE),
        "proved_families": [
            {"owned_label": owned, "pair": list(pair)}
            for owned, pair in sorted(SCOPE.PROVED_FAMILIES)
        ],
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(DRY_RUN_JSON, result)
    return result


def benchmark(document: dict[str, Any], max_wall_seconds: float) -> dict[str, Any]:
    jobs = [
        (epsilon_id, base_id)
        for epsilon_id in M5045.EPSILON_IDS
        for base_id in M5045.BENCHMARK_BASE_IDS
    ]
    rows = M5045.run_set(document, jobs, max_wall_seconds)
    complete = len(rows) == len(jobs)
    converged = complete and all(row["status"] == "COMPLETED_CONVERGED" for row in rows)
    maximum_difference = max(
        (
            float(row.get("theorem_first_legacy_relative_difference", math.inf))
            for row in rows
        ),
        default=math.inf,
    )
    exactness = bool(converged and maximum_difference < EXACTNESS_THRESHOLD)
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "event_id": M5045.EVENT_ID,
        "scope_source": str(SCRIPT_5045_SCOPE),
        "scope_source_sha256": digest(SCRIPT_5045_SCOPE),
        "broad_guard_source": str(M5043.SCRIPT_5041),
        "broad_guard_source_sha256": digest(M5043.SCRIPT_5041),
        "jobs": rows,
        "expected_jobs": len(jobs),
        "completed_jobs": len(rows),
        "all_jobs_converged": converged,
        "exactness_gate_threshold": EXACTNESS_THRESHOLD,
        "maximum_relative_difference": maximum_difference,
        "exactness_gate_passed": exactness,
        "restricted_fourth_scramble_scratch_authorized": exactness,
        "full_primary_event_run_authorized": False,
        "authorization_boundary": (
            "passing this six-job gate authorizes only a separate scratch recomputation "
            "of S503404; it does not authorize a production claim"
        ),
        "formalization_workbench_tree_sha256": tree_digest(
            POST.parent / "formalization-workbench"
        ),
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(BENCHMARK_JSON, result)
    checks = [
        ("six_jobs_completed", complete, str(len(rows))),
        ("all_jobs_converged", converged, str(sum(row.get("status") == "COMPLETED_CONVERGED" for row in rows))),
        ("restricted_exactness_gate", exactness, str(maximum_difference)),
        ("no_unstable_numeric_residues", converged and all(int(row.get("unstable_numeric_residue_count", 1)) == 0 for row in rows), str([row.get("unstable_numeric_residue_count") for row in rows])),
        ("claim_remains_false", not result["valid_for_full_MTS_claim"], "required false"),
        ("formalization_workbench_unchanged", result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE, result["formalization_workbench_tree_sha256"]),
    ]
    validation_rows = [
        {"check": name, "passed": str(bool(passed)).lower(), "evidence": evidence}
        for name, passed, evidence in checks
    ]
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("check", "passed", "evidence"))
        writer.writeheader()
        writer.writerows(validation_rows)
    return result


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("dry-run", "benchmark"), default="dry-run")
    parser.add_argument("--max-wall-seconds", type=float, default=7_200.0)
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    if arguments.max_wall_seconds <= 0.0 or arguments.max_wall_seconds > 9_000.0:
        raise ValueError("wall limit must be in (0,9000] seconds")
    configure_reused_runner()
    document = M5045.config()
    M5043.M5041.theorem_certificate = restricted_certificate
    N5030.chamber_residue_catalog = M5043.theorem_first_chamber_residue_catalog
    try:
        result = (
            dry_run(document)
            if arguments.mode == "dry-run"
            else benchmark(document, arguments.max_wall_seconds)
        )
    finally:
        M5043.M5041.theorem_certificate = ORIGINAL_THEOREM
        N5030.chamber_residue_catalog = ORIGINAL_CATALOG
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
