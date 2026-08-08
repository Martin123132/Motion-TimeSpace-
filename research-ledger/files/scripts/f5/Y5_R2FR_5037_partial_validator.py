from __future__ import annotations

import ast
import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5037"
RUN = SOURCE / "runs" / "paired_outer_precision_s4_v1"
REPAIR = SOURCE / "repairs" / "chart_origin_collision_v1"
RESULT = SOURCE / "paired_outer_precision_results.json"
DOCUMENT = POST / "5037-Y5-R2FR-paired-outer-precision-and-z-reflection-control.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"
OUTPUT = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5037_PARTIAL_VALIDATION.csv"
)
RUNNER = POST / "scripts" / "Y5_R2FR_5037_paired_outer_precision_reflection_control.py"
REPAIR_SCRIPT = POST / "scripts" / "Y5_R2FR_5037_chart_origin_collision_repair.py"
MARKER = "MTS_5037_PAIRED_OUTER_PRECISION_REFLECTION_CONTROL_IN_PROGRESS"
CONFIG_DIGEST = "86e46b1d2663217182a1bd246c1367e6dfd1eca61694ec86c388d3182e502c49"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
REPAIRED_KEYS = {
    "E040__S503403_N0000__A01__primary24",
    "E040__S503403_N0000__A13__primary24",
}
FAILED_KEY = "E040__S503403_N0000__A14__primary24"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def canonical_digest(value: Any) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        value.update(item.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(item).encode("ascii"))
    return value.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def close(value: float, expected: float, tolerance: float = 2.0e-10) -> bool:
    return abs(value - expected) <= tolerance * max(1.0, abs(expected))


def check_rows() -> list[tuple[str, bool, str]]:
    config = load_json(RUN / "config.json")
    unsigned = dict(config)
    supplied_digest = unsigned.pop("config_digest")
    status = load_json(RUN / "status.json")
    result = load_json(RESULT)
    repair = load_json(REPAIR / "repair_summary.json")
    jobs = [load_json(path) for path in sorted((RUN / "jobs").glob("*.json"))]
    imported = [row for row in jobs if row["status"] == "IMPORTED_CONVERGED"]
    computed = [row for row in jobs if row["status"] == "COMPLETED_CONVERGED"]
    failed = [row for row in jobs if row["status"] == "FAILED"]
    unconverged = [row for row in jobs if row["status"] == "COMPLETED_UNCONVERGED"]
    source_lock = all(
        expected is not None
        and Path(path).exists()
        and digest(Path(path)) == expected
        for path, expected in config["source_files"].items()
    )
    import_lock = all(
        Path(row["imported_from"]["source_job"]).exists()
        and digest(Path(row["imported_from"]["source_job"]))
        == row["imported_from"]["source_job_sha256"]
        for row in imported
    )
    repaired_jobs = {
        key: load_json(RUN / "jobs" / f"{key}.json") for key in REPAIRED_KEYS
    }
    original_jobs = {
        key: load_json(REPAIR / "original" / f"{key}.json")
        for key in REPAIRED_KEYS
    }
    value_preserved = all(
        close(
            repaired_jobs[key]["normalized_direct_D_hhh_over_G3"][component],
            original_jobs[key]["normalized_direct_D_hhh_over_G3"][component],
        )
        for key in REPAIRED_KEYS
        for component in ("real", "imaginary")
    )
    exclusions = {
        key: repair["chart_origin_exclusions"][key] for key in REPAIRED_KEYS
    }
    exclusion_proof = all(
        len(rows) == 12
        and len(
            {
                (
                    round(row["root"]["real"], 12),
                    round(row["root"]["imaginary"], 12),
                )
                for row in rows
            }
        )
        == 4
        and max(row["maximum_global_factor_root_modulus"] for row in rows)
        < 4.0e-15
        and all(not row["required_for_homotopy"] for row in rows)
        and all(
            {
                pair[0].rsplit(":", 1)[1],
                pair[1].rsplit(":", 1)[1],
            }
            in ({"minus_u", "plus_u"}, {"minus_v", "plus_v"})
            and pair[0].rsplit(":", 1)[0] == pair[1].rsplit(":", 1)[0]
            for row in rows
            for pair in row["pairs"]
        )
        for rows in exclusions.values()
    )
    repair_contracts = all(
        repaired_jobs[key]["repair_contract"]["repair_revision"]
        == "pair-local-chart-origin-filtered-residue-v5"
        and repaired_jobs[key]["repair_contract"]["repair_script_sha256"]
        == digest(REPAIR_SCRIPT)
        and repaired_jobs[key]["status"] == "COMPLETED_CONVERGED"
        and repaired_jobs[key]["integral_converged"]
        for key in REPAIRED_KEYS
    )
    failed_job = load_json(RUN / "jobs" / f"{FAILED_KEY}.json")
    scratch_failed = load_json(
        REPAIR / "scratch_run" / "jobs" / f"{FAILED_KEY}.json"
    )
    topology = load_json(
        RUN
        / "topologies"
        / "S503403_N0000__E040_A14.json"
    )
    endpoint_roots = [
        complex(topology["chambers"][0]["target_start_root"]),
        complex(topology["chambers"][2]["target_end_root"]),
    ]
    endpoint_finite = all(
        math.isfinite(root.real)
        and math.isfinite(root.imag)
        and abs(root) > 0.25
        for root in endpoint_roots
    )
    document = DOCUMENT.read_text(encoding="utf-8")
    resume = RESUME.read_text(encoding="utf-8")
    vector_csv = read_csv(SOURCE / "epsilon_cyclic_vector.csv")
    decomposition_csv = read_csv(SOURCE / "local_nonlocal_decomposition.csv")
    paired_csv = read_csv(SOURCE / "paired_vector_convergence.csv")
    target_csv = read_csv(SOURCE / "epsilon_zero_target_comparison.csv")
    reflection_csv = read_csv(SOURCE / "reflection_control.csv")
    precision_csv = read_csv(SOURCE / "outer_precision_diagnostic.csv")
    gate_csv = read_csv(SOURCE / "outer_precision_gate.csv")
    formal_digest = tree_digest(FORMAL)
    authoritative = (
        DOCUMENT,
        RESULT,
        REPAIR / "repair_summary.json",
        SOURCE / "PROVENANCE.md",
    )
    return [
        (
            "scripts_parse",
            all(
                ast.parse(path.read_text(encoding="utf-8")) is not None
                for path in (RUNNER, REPAIR_SCRIPT, Path(__file__).resolve())
            ),
            "5037 runner, v5 repair and partial validator parse",
        ),
        (
            "immutable_config_digest",
            supplied_digest == CONFIG_DIGEST
            and supplied_digest == canonical_digest(unsigned),
            supplied_digest,
        ),
        (
            "source_digest_lock",
            source_lock,
            f"{len(config['source_files'])} locked config sources match",
        ),
        (
            "bounded_matrix_state",
            status["state"] == "PAUSED_AFTER_CHART_ORIGIN_REPAIR"
            and status["expected_jobs"] == 189
            and status["terminal_jobs"] == 131
            and status["remaining_jobs"] == 58
            and status["failed_jobs"] == 1
            and status["unconverged_jobs"] == 0,
            "131/189 terminal after bounded batch and repair",
        ),
        (
            "job_partition",
            len(jobs) == 131
            and len(imported) == 117
            and len(computed) == 13
            and len(failed) == 1
            and not unconverged,
            "117 imports, 13 computed-converged, one failed",
        ),
        (
            "exact_import_provenance",
            import_lock,
            "all 117 source-job SHA-256 chains validate",
        ),
        (
            "chart_origin_exclusion_proof",
            exclusion_proof,
            "four non-required same-source chart roots; represented roots <4e-15",
        ),
        (
            "v5_repair_contract",
            repair_contracts
            and set(repair["repaired_jobs"]) == REPAIRED_KEYS
            and len(repair["still_open"]) == 1,
            "two unstable jobs close under hash-linked v5 repair",
        ),
        (
            "direct_values_preserved",
            value_preserved,
            "v5 classification changes the gate, not either direct integral",
        ),
        (
            "finite_endpoint_obstruction_retained",
            failed_job["status"] == "FAILED"
            and scratch_failed["status"] == "FAILED"
            and "minus_u, direct:g1:minus_v" in failed_job["error"]
            and failed_job["error"] == scratch_failed["error"]
            and topology["assignment_tracking_passed"]
            and topology["full_off_unit_collision_homotopy_enumerated"]
            and endpoint_finite,
            "A14 remains a finite transported endpoint-sector obstruction",
        ),
        (
            "precision_population_boundary",
            result["outer_precision_diagnostic"]["completed_paired_scrambles"] == 2
            and not result["gate"]["four_scramble_linear_matrix_complete"]
            and not result["gate"]["minimum_four_scramble_precision_smoke"]
            and not result["gate"]["fixed_target_verdict_ready"],
            "no incomplete seed is promoted into the precision statistic",
        ),
        (
            "reflection_not_imposed",
            not result["reflection_diagnostic"]["reflection_symmetry_imposed"]
            and not result["reflection_diagnostic"]["odd_component_zero_assumed"]
            and not result["gate"]["reflection_symmetry_imposed"],
            "reflection remains a measured diagnostic",
        ),
        (
            "claim_boundary",
            not result["target_fitted"]
            and not result["epsilon_limit_complete"]
            and not result["production_precision_complete"]
            and not result["valid_for_full_MTS_claim"],
            "target, epsilon-zero, production and MTS claims remain false",
        ),
        (
            "csv_outputs_parse",
            len(vector_csv) == 15
            and len(decomposition_csv) == 15
            and len(paired_csv) == 2
            and len(target_csv) == 5
            and len(reflection_csv) == 2
            and len(precision_csv) == 5
            and len(gate_csv) == len(result["gate"]),
            "all seven 5037 CSV artifacts parse with expected row counts",
        ),
        (
            "handoff_recorded",
            "**Status: IN PROGRESS" in document
            and CONFIG_DIGEST in document
            and MARKER in document
            and MARKER in resume
            and "Immediate next calculation" in resume
            and "No GitHub action was taken" in resume,
            "partial result, derivation, boundary and exact next calculation recorded",
        ),
        (
            "no_missing_markers",
            all(
                "MISSING_" not in path.read_text(encoding="utf-8", errors="ignore")
                for path in authoritative
            ),
            "no placeholder marker in authoritative 5037 artifacts",
        ),
        (
            "formalization_unchanged",
            formal_digest == FORMAL_BASELINE,
            formal_digest,
        ),
        (
            "pycache_removed",
            not any(path.is_dir() for path in POST.rglob("__pycache__")),
            "no __pycache__ directory under post-checkpoint-work",
        ),
    ]


def main() -> None:
    rows = check_rows()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("check_id", "passed", "detail", "checkpoint_marker"),
        )
        writer.writeheader()
        for index, (name, passed, detail) in enumerate(rows, start=1):
            writer.writerow(
                {
                    "check_id": f"V5037P_{index:02d}_{name}",
                    "passed": passed,
                    "detail": detail,
                    "checkpoint_marker": MARKER,
                }
            )
    failed = [name for name, passed, _ in rows if not passed]
    print(
        json.dumps(
            {
                "checkpoint_marker": MARKER,
                "check_count": len(rows),
                "failed": failed,
                "passed": not failed,
                "output": str(OUTPUT),
            },
            indent=2,
        )
    )
    if failed:
        raise RuntimeError(f"checkpoint 5037 partial validation failed: {failed}")


if __name__ == "__main__":
    main()
