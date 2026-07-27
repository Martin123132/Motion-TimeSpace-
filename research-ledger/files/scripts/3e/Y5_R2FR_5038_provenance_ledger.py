from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SOURCE = POST / "source-intake" / "functional_rg" / "5037"
RUN = SOURCE / "runs" / "paired_outer_precision_s4_v1"
ENDPOINT = SOURCE / "repairs" / "finite_endpoint_sector_v1"
CHART = SOURCE / "repairs" / "chart_origin_collision_e020_seed3_v1"
OUTPUT = SOURCE / "repairs" / "5038_provenance_ledger.json"
MARKER = "MTS_5038_PROVENANCE_LEDGER"
ENDPOINT_KEY = "E040__S503403_N0000__A14__primary24"
CHART_KEYS = (
    "E020__S503403_N0000__A01__primary24",
    "E020__S503403_N0000__A13__primary24",
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def complex_from_row(row: dict[str, Any]) -> complex:
    return complex(float(row["real"]), float(row["imaginary"]))


def relative_difference(first: complex, second: complex) -> float:
    return abs(first - second) / max(1.0, abs(first), abs(second))


def record(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    return {"path": str(path.resolve()), "sha256": digest(path)}


def job_paths(directory: Path, key: str) -> tuple[Path, Path]:
    return directory / f"{key}.json", directory / f"kernel__{key}.json"


def atomic_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def main() -> None:
    endpoint_original = ENDPOINT / "original" / f"{ENDPOINT_KEY}.json"
    endpoint_repaired, endpoint_repaired_kernel = job_paths(
        ENDPOINT / "repaired", ENDPOINT_KEY
    )
    endpoint_live = RUN / "jobs" / f"{ENDPOINT_KEY}.json"
    endpoint_live_kernel = RUN / "kernels" / f"{ENDPOINT_KEY}.json"
    primary_job = ENDPOINT / "primary_scratch" / "jobs" / f"{ENDPOINT_KEY}.json"
    primary_kernel = (
        ENDPOINT / "primary_scratch" / "kernels" / f"{ENDPOINT_KEY}.json"
    )
    audit_job = ENDPOINT / "audit_scratch" / "jobs" / f"{ENDPOINT_KEY}.json"
    audit_kernel = ENDPOINT / "audit_scratch" / "kernels" / f"{ENDPOINT_KEY}.json"
    endpoint_original_row = load(endpoint_original)
    endpoint_repaired_row = load(endpoint_repaired)
    endpoint_live_row = load(endpoint_live)
    primary_row = load(primary_job)
    audit_row = load(audit_job)
    if endpoint_original_row["status"] != "FAILED":
        raise RuntimeError("endpoint original is not the failed pre-repair job")
    if endpoint_repaired_row["status"] != "COMPLETED_CONVERGED":
        raise RuntimeError("endpoint repaired job is not converged")
    if digest(endpoint_repaired) != digest(endpoint_live):
        raise RuntimeError("endpoint repaired and live jobs differ")
    if digest(endpoint_repaired_kernel) != digest(endpoint_live_kernel):
        raise RuntimeError("endpoint repaired and live kernels differ")
    if (
        primary_row["normalized_direct_D_hhh_over_G3"]
        != audit_row["normalized_direct_D_hhh_over_G3"]
    ):
        raise RuntimeError("endpoint primary and audit values differ")

    chart_rows: dict[str, Any] = {}
    for key in CHART_KEYS:
        original = CHART / "original" / f"{key}.json"
        repaired, repaired_kernel = job_paths(CHART / "repaired", key)
        live = RUN / "jobs" / f"{key}.json"
        live_kernel = RUN / "kernels" / f"{key}.json"
        original_row = load(original)
        repaired_row = load(repaired)
        if original_row["status"] != "COMPLETED_UNCONVERGED":
            raise RuntimeError(f"{key} original is not the unconverged job")
        if repaired_row["status"] != "COMPLETED_CONVERGED":
            raise RuntimeError(f"{key} repaired job is not converged")
        direct_residual = relative_difference(
            complex_from_row(original_row["normalized_direct_D_hhh_over_G3"]),
            complex_from_row(repaired_row["normalized_direct_D_hhh_over_G3"]),
        )
        if direct_residual > 2.0e-12:
            raise RuntimeError(f"{key} direct value changed during chart repair")
        if digest(repaired) != digest(live) or digest(repaired_kernel) != digest(
            live_kernel
        ):
            raise RuntimeError(f"{key} repaired and live artifacts differ")
        chart_rows[key] = {
            "original_job": record(original),
            "repaired_job": record(repaired),
            "repaired_kernel": record(repaired_kernel),
            "live_job": record(live),
            "live_kernel": record(live_kernel),
            "direct_value_preserved": True,
            "direct_value_relative_difference": direct_residual,
        }

    ledger = {
        "checkpoint_marker": MARKER,
        "ledger_script": record(Path(__file__).resolve()),
        "endpoint": {
            "job_key": ENDPOINT_KEY,
            "original_job": record(endpoint_original),
            "repaired_job": record(endpoint_repaired),
            "repaired_kernel": record(endpoint_repaired_kernel),
            "live_job": record(endpoint_live),
            "live_kernel": record(endpoint_live_kernel),
            "primary_job": record(primary_job),
            "primary_kernel": record(primary_kernel),
            "audit_job": record(audit_job),
            "audit_kernel": record(audit_kernel),
            "repair_summary": record(ENDPOINT / "repair_summary.json"),
            "diagnostic": record(
                SOURCE
                / "diagnostics"
                / "A14_ownership_pinch_v1"
                / "diagnostic.json"
            ),
            "topology": record(
                RUN / "topologies" / "S503403_N0000__E040_A14.json"
            ),
            "primary_audit_value_equal": True,
            "repaired_live_equal": True,
        },
        "chart_resume": {
            "repair_summary": record(CHART / "repair_summary.json"),
            "jobs": chart_rows,
        },
        "scripts": {
            "endpoint_diagnostic": record(
                POST / "scripts" / "Y5_R2FR_5037_A14_ownership_pinch_diagnostic.py"
            ),
            "endpoint_repair": record(
                POST / "scripts" / "Y5_R2FR_5037_endpoint_sector_repair.py"
            ),
            "chart_repair": record(
                POST / "scripts" / "Y5_R2FR_5037_chart_origin_collision_repair.py"
            ),
            "production_runner": record(
                POST
                / "scripts"
                / "Y5_R2FR_5037_paired_outer_precision_reflection_control.py"
            ),
        },
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(OUTPUT, ledger)
    print(json.dumps(ledger, indent=2))


if __name__ == "__main__":
    main()
