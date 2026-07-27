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
ENDPOINT = SOURCE / "repairs" / "finite_endpoint_sector_v1"
CHART = SOURCE / "repairs" / "chart_origin_collision_e020_seed3_v1"
LEDGER_PATH = SOURCE / "repairs" / "5038_provenance_ledger.json"
RESULT = SOURCE / "paired_outer_precision_results.json"
DOCUMENT = POST / "5038-Y5-R2FR-finite-endpoint-removable-sector-lemma-and-bounded-resume.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"
OUTPUT = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5038_VALIDATION.csv"
)
MARKER = "MTS_5038_FINITE_ENDPOINT_REMOVABLE_SECTOR_AND_BOUNDED_RESUME"
CONFIG_DIGEST = "86e46b1d2663217182a1bd246c1367e6dfd1eca61694ec86c388d3182e502c49"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
ENDPOINT_KEY = "E040__S503403_N0000__A14__primary24"
CHART_KEYS = {
    "E020__S503403_N0000__A01__primary24",
    "E020__S503403_N0000__A13__primary24",
}
SCRIPTS = (
    POST / "scripts" / "Y5_R2FR_5037_A14_ownership_pinch_diagnostic.py",
    POST / "scripts" / "Y5_R2FR_5037_endpoint_sector_repair.py",
    POST / "scripts" / "Y5_R2FR_5038_provenance_ledger.py",
    Path(__file__).resolve(),
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def canonical_digest(value: Any) -> str:
    payload = json.dumps(
        value, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        value.update(item.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(item).encode("ascii"))
    return value.hexdigest()


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def finite_complex_row(row: Any) -> bool:
    return bool(
        isinstance(row, dict)
        and math.isfinite(float(row["real"]))
        and math.isfinite(float(row["imaginary"]))
    )


def verify_record(record: dict[str, Any]) -> bool:
    path = Path(record["path"])
    return path.exists() and digest(path) == record["sha256"]


def ledger_records(value: Any) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if isinstance(value, dict):
        if set(value) == {"path", "sha256"}:
            rows.append(value)
        else:
            for child in value.values():
                rows.extend(ledger_records(child))
    elif isinstance(value, list):
        for child in value:
            rows.extend(ledger_records(child))
    return rows


def check_rows() -> list[tuple[str, bool, str]]:
    config = load(RUN / "config.json")
    unsigned = dict(config)
    supplied_digest = unsigned.pop("config_digest")
    status = load(RUN / "status.json")
    result = load(RESULT)
    endpoint = load(ENDPOINT / "repair_summary.json")
    chart = load(CHART / "repair_summary.json")
    ledger = load(LEDGER_PATH)
    diagnostic = load(
        SOURCE / "diagnostics" / "A14_ownership_pinch_v1" / "diagnostic.json"
    )
    jobs = [load(path) for path in sorted((RUN / "jobs").glob("*.json"))]
    imported = [row for row in jobs if row["status"] == "IMPORTED_CONVERGED"]
    computed = [row for row in jobs if row["status"] == "COMPLETED_CONVERGED"]
    invalid = [
        row
        for row in jobs
        if row["status"] not in {"IMPORTED_CONVERGED", "COMPLETED_CONVERGED"}
    ]
    endpoint_job = load(RUN / "jobs" / f"{ENDPOINT_KEY}.json")
    endpoint_certificates = endpoint["repair_contract"]["primary_certificates"]
    endpoint_audit_certificates = endpoint["repair_contract"]["audit_certificates"]
    endpoint_extension_calls = endpoint["primary"]["extension_calls"]
    endpoint_audit_calls = endpoint["audit"]["extension_calls"]
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
    chart_jobs = {
        key: load(RUN / "jobs" / f"{key}.json") for key in CHART_KEYS
    }
    chart_original = {
        key: load(CHART / "original" / f"{key}.json") for key in CHART_KEYS
    }
    chart_value_residuals = {
        key: abs(
            complex(**{
                "real": chart_jobs[key]["normalized_direct_D_hhh_over_G3"]["real"],
                "imag": chart_jobs[key]["normalized_direct_D_hhh_over_G3"]["imaginary"],
            })
            - complex(**{
                "real": chart_original[key]["normalized_direct_D_hhh_over_G3"]["real"],
                "imag": chart_original[key]["normalized_direct_D_hhh_over_G3"]["imaginary"],
            })
        )
        / max(
            1.0,
            abs(
                complex(
                    chart_jobs[key]["normalized_direct_D_hhh_over_G3"]["real"],
                    chart_jobs[key]["normalized_direct_D_hhh_over_G3"]["imaginary"],
                )
            ),
        )
        for key in CHART_KEYS
    }
    document = DOCUMENT.read_text(encoding="utf-8")
    resume = RESUME.read_text(encoding="utf-8")
    records = ledger_records(ledger)
    formal_digest = tree_digest(FORMAL)
    return [
        (
            "scripts_parse",
            all(ast.parse(path.read_text(encoding="utf-8")) is not None for path in SCRIPTS),
            "diagnostic, repair, ledger and validator parse",
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
            "matrix_state",
            status["expected_jobs"] == 189
            and status["terminal_jobs"] == 139
            and status["remaining_jobs"] == 50
            and status["failed_jobs"] == 0
            and status["unconverged_jobs"] == 0,
            f"state={status['state']}, 139/189 terminal",
        ),
        (
            "numeric_partition",
            len(jobs) == 139
            and len(imported) == 117
            and len(computed) == 22
            and not invalid
            and all(
                row.get("integral_converged")
                and finite_complex_row(row.get("normalized_direct_D_hhh_over_G3"))
                for row in jobs
            ),
            "117 imports plus 22 computed-converged jobs",
        ),
        (
            "exact_import_provenance",
            import_lock,
            "all 117 imported source-job hashes validate",
        ),
        (
            "failure_localized",
            diagnostic["terminal_error"]["error_type"] == "RuntimeError"
            and len(diagnostic["ownership_failures"]) == 1
            and diagnostic["ownership_failures"][0]["context"]["stage"]
            == "global_chamber_value"
            and "minus_u, direct:g1:minus_v"
            in diagnostic["ownership_failures"][0]["error"],
            "A14 failure occurs only in near-endpoint global-cycle evaluation",
        ),
        (
            "endpoint_certificate_population",
            len(endpoint_certificates) == 8
            and len(endpoint_audit_certificates) == 8
            and all(row["boundary_valid"] for row in endpoint_certificates)
            and all(row["boundary_valid"] for row in endpoint_audit_certificates),
            "four boundaries, two inherited sides, two floors",
        ),
        (
            "zero_double_residue_gate",
            max(
                row["residue_probe"]["maximum_residue_magnitude"]
                for row in endpoint_certificates
            )
            < 3.6e-15
            and all(row["residue_probe"]["numerically_zero"] for row in endpoint_certificates),
            "maximum local double residue below 3.6e-15",
        ),
        (
            "two_sided_limit_gate",
            max(row["limit_relative_residual"] for row in endpoint_certificates)
            < 2.0e-8
            and max(
                row["adjacent_limit_relative_residual"]
                for row in endpoint_certificates
            )
            < 2.0e-8,
            "one-sided refinement and adjacent-sector limits pass",
        ),
        (
            "endpoint_extension_locality",
            len(endpoint_extension_calls) == 5
            and len(endpoint_audit_calls) == 5
            and max(abs(row["sector_parameter"]) for row in endpoint_extension_calls)
            < 2.1e-12
            and max(row["transverse_distance"] for row in endpoint_extension_calls)
            < 4.0e-16,
            "only five evaluations inside the numerical endpoint tube",
        ),
        (
            "endpoint_floor_audit",
            endpoint["accepted"]
            and endpoint["promoted"]
            and endpoint["kernel_relative_residual"] == 0.0
            and endpoint["primary"]["status"] == "COMPLETED_CONVERGED"
            and endpoint["audit"]["status"] == "COMPLETED_CONVERGED",
            "1e-9 and 2e-9 floors return identical kernels",
        ),
        (
            "endpoint_live_contract",
            endpoint_job["status"] == "COMPLETED_CONVERGED"
            and endpoint_job["integral_converged"]
            and endpoint_job["repair_contract"]["revision"]
            == "finite-endpoint-removable-sector-extension-v1"
            and endpoint_job["repair_contract"]["repair_script_sha256"]
            == digest(POST / "scripts" / "Y5_R2FR_5037_endpoint_sector_repair.py"),
            "A14 promoted with its immutable repair contract",
        ),
        (
            "chart_resume_repair",
            set(chart["repaired_jobs"]) == CHART_KEYS
            and not chart["still_open"]
            and all(
                row["status"] == "COMPLETED_CONVERGED"
                and row["repair_contract"]["repair_revision"]
                == "pair-local-chart-origin-filtered-residue-v5"
                and len(row["repair_contract"]["chart_origin_exclusions"]) == 12
                for row in chart_jobs.values()
            ),
            "two epsilon=0.02 chart rows close under unchanged v5",
        ),
        (
            "chart_direct_value_preserved",
            max(chart_value_residuals.values()) < 2.0e-12,
            f"maximum relative change={max(chart_value_residuals.values()):.3e}",
        ),
        (
            "provenance_ledger",
            ledger["checkpoint_marker"] == "MTS_5038_PROVENANCE_LEDGER"
            and len(records) >= 25
            and all(verify_record(record) for record in records),
            f"{len(records)} artifact hashes validate",
        ),
        (
            "claim_boundary",
            not result["target_fitted"]
            and not result["epsilon_limit_complete"]
            and not result["production_precision_complete"]
            and not result["valid_for_full_MTS_claim"],
            "four-scramble, epsilon-zero, production and MTS claims remain false",
        ),
        (
            "handoff_markers",
            MARKER in document
            and MARKER in resume
            and "139/189" in document
            and "139/189" in resume,
            "5038 document and resume ledger agree",
        ),
        (
            "formalization_untouched",
            formal_digest == FORMAL_BASELINE,
            formal_digest,
        ),
        (
            "no_python_cache",
            not any(POST.rglob("__pycache__")) and not any(POST.rglob("*.pyc")),
            "post-checkpoint-work has no Python cache artifacts",
        ),
    ]


def main() -> None:
    rows = check_rows()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("check", "passed", "detail"))
        writer.writeheader()
        for name, passed, detail in rows:
            writer.writerow(
                {"check": name, "passed": str(bool(passed)).lower(), "detail": detail}
            )
    failed = [name for name, passed, _ in rows if not passed]
    print(json.dumps({"passed": len(rows) - len(failed), "total": len(rows), "failed": failed}, indent=2))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
