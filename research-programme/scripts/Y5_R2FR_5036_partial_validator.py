from __future__ import annotations

import ast
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
RUN = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5036"
    / "runs"
    / "paired_full_vector_s2_v1"
)
RESULT = RUN / "partial_results.json"
DOCUMENT = (
    POST
    / "5036-Y5-R2FR-paired-epsilon-full-cyclic-vector-and-local-nonlocal-decomposition.md"
)
RESUME = POST / "CURRENT_LOCAL_RESUME.md"
OUTPUT = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5036_PARTIAL_VALIDATION.csv"
)
RUNNER = POST / "scripts" / "Y5_R2FR_5036_paired_full_vector_ladder.py"
REPAIR = POST / "scripts" / "Y5_R2FR_5035_pair_local_residue_radius_repair.py"
MARKER = "MTS_5036_PAIRED_EPSILON_FULL_CYCLIC_VECTOR_IN_PROGRESS"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
EXPECTED_REMAINING = {
    "E020__S503402_N0000__A00__primary24",
    "E020__S503402_N0000__A09__primary24",
    "E020__S503402_N0000__A14__primary24",
    "E020__S503402_N0000__A04__primary24",
}


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


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def checks() -> list[tuple[str, bool, str]]:
    config = load(RUN / "config.json")
    unsigned = dict(config)
    supplied = unsigned.pop("config_digest")
    status = load(RUN / "status.json")
    result = load(RESULT)
    jobs = [load(path) for path in sorted((RUN / "jobs").glob("*.json"))]
    imported = [row for row in jobs if row["status"] == "IMPORTED_CONVERGED"]
    computed = [row for row in jobs if row["status"] == "COMPLETED_CONVERGED"]
    expected = set()
    for epsilon_id in config["epsilon_ids"]:
        for event in config["events"]:
            for base in config["base_arguments"]:
                expected.add(
                    f"{epsilon_id}__{event['event_id']}__{base['argument_id']}__primary24"
                )
        central = min(
            config["crossings"],
            key=lambda row: abs(row["physical_s_channel_cosine"]),
        )
        for base_id in (
            central["s_argument_id"],
            central["t_argument_id"],
            central["u_argument_id"],
        ):
            expected.add(
                f"{epsilon_id}__S{config['audit_seed']}_N0000__{base_id}__audit32"
            )
    remaining = expected - {row["job_key"] for row in jobs}
    source_lock = all(
        expected_digest is not None
        and Path(path).exists()
        and digest(Path(path)) == expected_digest
        for path, expected_digest in config["source_files"].items()
    )
    computed_radius = [row["residue_radius_contract"] for row in computed]
    summaries = {
        float(row["epsilon"]): row for row in result["vector_summaries"]
    }
    document = DOCUMENT.read_text(encoding="utf-8")
    resume = RESUME.read_text(encoding="utf-8")
    formal_digest = tree_digest(FORMAL)
    return [
        (
            "scripts_parse",
            all(
                ast.parse(path.read_text(encoding="utf-8")) is not None
                for path in (RUNNER, REPAIR, Path(__file__).resolve())
            ),
            "runner, residue rule and partial validator parse",
        ),
        (
            "config_digest",
            supplied == canonical_digest(unsigned),
            supplied,
        ),
        (
            "source_digest_lock",
            source_lock,
            f"{len(config['source_files'])} source hashes match",
        ),
        (
            "paused_terminal_state",
            status["state"] == "PAUSED_JOB_LIMIT"
            and status["expected_jobs"] == 99
            and status["terminal_jobs"] == 95
            and status["remaining_jobs"] == 4
            and status["failed_jobs"] == 0
            and status["unconverged_jobs"] == 0,
            "95/99 terminal with no failed or unconverged job",
        ),
        (
            "job_partition",
            len(jobs) == 95 and len(imported) == 51 and len(computed) == 44,
            "51 exact imports plus 44 newly computed kernels",
        ),
        (
            "all_terminal_jobs_numeric",
            all(
                row["integral_converged"]
                and row["topology_passed"]
                and isinstance(row["normalized_direct_D_hhh_over_G3"], dict)
                for row in jobs
            ),
            "all persisted jobs are topology-passed and numeric",
        ),
        (
            "remaining_jobs_exact",
            remaining == EXPECTED_REMAINING,
            ",".join(sorted(remaining)),
        ),
        (
            "shrinking_radius_active",
            len(computed_radius) == 44
            and all(
                row["revision"] == "pair-local-double-residue-shrinking-radius-v4"
                and row["adjustment_count"] == 0
                for row in computed_radius
            ),
            "v4 active; no first-44 kernel required radius shrinkage",
        ),
        (
            "vector_completeness",
            summaries[0.08]["complete_scrambles"] == 2
            and summaries[0.04]["complete_scrambles"] == 2
            and summaries[0.02]["complete_scrambles"] == 1,
            "two full vectors at 0.08/0.04; one at 0.02",
        ),
        (
            "paired_counts",
            [row["paired_scrambles"] for row in result["paired_convergence"]]
            == [2, 1],
            "second regulator step remains one-pair provisional",
        ),
        (
            "central_audit_complete",
            all(row["complete"] for row in result["global_tier_audit"])
            and max(
                row["relative_difference"] for row in result["global_tier_audit"]
            )
            < 2.0e-13,
            "all imported central 24/32 audits agree",
        ),
        (
            "claim_boundary",
            not result["gate"]["paired_full_vector_ladder_stable"]
            and not result["epsilon_limit_complete"]
            and not result["production_precision_complete"]
            and not result["valid_for_full_MTS_claim"]
            and not result["target_fitted"],
            "partial vector is not promoted to evidence",
        ),
        (
            "handoff_recorded",
            "**Status: IN PROGRESS (`95/99` terminal jobs).**" in document
            and MARKER in resume
            and "No GitHub action was taken" in resume,
            "in-progress document and resume carry exact boundary",
        ),
        (
            "formalization_unchanged",
            formal_digest == FORMAL_BASELINE,
            formal_digest,
        ),
        (
            "pycache_removed",
            not any(path.is_dir() for path in POST.rglob("__pycache__")),
            "no pycache under post-checkpoint-work",
        ),
    ]


def main() -> None:
    rows = checks()
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
                    "check_id": f"V5036P_{index:02d}_{name}",
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
        raise RuntimeError(f"5036 partial validation failed: {failed}")


if __name__ == "__main__":
    main()
