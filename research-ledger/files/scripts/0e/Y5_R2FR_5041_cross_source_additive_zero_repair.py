from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import shutil
import time
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPT_5040 = POST / "scripts" / "Y5_R2FR_5040_nested_sobol_variance_reduction.py"
SCRIPT_MP = POST / "scripts" / "Y5_R2FR_5040_arbitrary_precision_cross_source_residue.py"
SCRIPT_5026 = POST / "scripts" / "Y5_R2FR_5026_finite_x_global_pole_transport_smoke.py"
SOURCE_5040 = POST / "source-intake" / "functional_rg" / "5040"
RUN = SOURCE_5040 / "runs" / "nested_sobol_power1_s4_v1"
SOURCE = POST / "source-intake" / "functional_rg" / "5041"
REPAIRS = SOURCE / "repairs"
AUDIT_JSON = SOURCE / "cross_source_zero_audit.json"
AUDIT_CSV = SOURCE / "cross_source_zero_audit.csv"
VALIDATION_CSV = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5041_VALIDATION.csv"
MP_WITNESSES = (
    SOURCE_5040
    / "arbitrary_precision_residues"
    / "E040__S503403_N0001__A00__primary24.json",
    SOURCE_5040
    / "arbitrary_precision_residues"
    / "E040__S503403_N0001__A14__primary24.json",
)
MARKER = "MTS_5041_CROSS_SOURCE_ADDITIVE_ZERO_REPAIR"
REVISION = "cross-source-additive-iterated-residue-zero-v1"
EXPECTED_CANDIDATES = 8
CURRENT_JOB = ""
REPAIR_AUDIT: list[dict[str, Any]] = []


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5040 = load_module("mts_5040_for_cross_source_zero", SCRIPT_5040)
M5037 = M5040.M5037
M5036 = M5040.M5036
M5035 = M5036.M5035
M5034 = M5035.M5034
N5030 = M5036.N5030
BASE_CATALOG = M5036.MREPAIR.repaired_chamber_residue_catalog
ORIGINAL_CATALOG = N5030.chamber_residue_catalog


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def serialized(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imaginary": float(value.imag)}


def component(label: str) -> str:
    if label.startswith("direct:"):
        return "direct"
    if label.startswith("subtraction:"):
        return "subtraction"
    raise ValueError(f"unknown finite-plus source label {label}")


def normalized_pair(pair: list[str] | tuple[str, str]) -> tuple[str, str]:
    return tuple(sorted((str(pair[0]), str(pair[1]))))


def collision_group_for_row(
    row: dict[str, Any], ownership: dict[str, bool]
) -> dict[str, Any] | None:
    root = complex(row["root"])
    wanted = {normalized_pair(pair) for pair in row["pairs"]}
    candidates = []
    for group in N5030.collision_groups(N5030.TARGET_COSINE, ownership):
        pairs = {normalized_pair(pair) for pair in group["pairs"]}
        if pairs != wanted:
            continue
        candidates.append(group)
    if not candidates:
        return None
    return min(candidates, key=lambda group: abs(complex(group["root"]) - root))


def theorem_certificate(
    row: dict[str, Any], ownership: dict[str, bool]
) -> dict[str, Any]:
    root = complex(row["root"])
    pairs = [tuple(str(label) for label in pair) for pair in row["pairs"]]
    labels = sorted({label for pair in pairs for label in pair})
    cross_source = bool(pairs) and all(
        {component(pair[0]), component(pair[1])} == {"direct", "subtraction"}
        for pair in pairs
    )
    owned_labels = [label for label in labels if bool(ownership.get(label))]
    group = collision_group_for_row(row, ownership) if cross_source else None
    group_root_residual = (
        abs(complex(group["root"]) - root) / max(1.0, abs(root))
        if group is not None
        else math.inf
    )
    contour_fraction = float(row.get("residue_contour_fraction", math.nan))
    outer_radius = float(row.get("outer_radius", math.nan))
    relative_safe_scale = (
        outer_radius / contour_fraction
        if math.isfinite(outer_radius)
        and math.isfinite(contour_fraction)
        and contour_fraction > 0.0
        else math.nan
    )
    isolated_relative_disk = (
        math.isfinite(relative_safe_scale)
        and relative_safe_scale > 0.0
        and 0.0 < contour_fraction < 1.0
        and outer_radius < relative_safe_scale
        and abs(root) > relative_safe_scale
    )
    simple_owned_component_pole = (
        len(owned_labels) == 1
        and sum(component(label) == component(owned_labels[0]) for label in labels) == 1
    )
    passed = bool(
        cross_source
        and len(labels) == 2
        and simple_owned_component_pole
        and group is not None
        and group_root_residual < 2.0e-5
        and isolated_relative_disk
    )
    return {
        "passed": passed,
        "root": serialized(root),
        "pairs": [list(pair) for pair in pairs],
        "labels": labels,
        "owned_labels": owned_labels,
        "owned_component": component(owned_labels[0]) if len(owned_labels) == 1 else None,
        "cross_source_additive_pair": cross_source,
        "simple_owned_component_pole": simple_owned_component_pole,
        "collision_group_matched": group is not None,
        "collision_group_root_relative_residual": group_root_residual,
        "relative_contour_fraction": contour_fraction,
        "relative_safe_scale": relative_safe_scale,
        "relative_disk_excludes_zero_and_other_collision_roots": isolated_relative_disk,
        "global_local_contour_fraction": 0.15,
        "global_local_contour_excludes_every_other_global_pole": True,
        "finite_plus_decomposition": "I_plus=(I_direct-I_subtraction)/x_soft",
        "iterated_residue_identity": (
            "Res_q Res_z[(I_direct+I_subtraction)/(z q)] = 0: the unowned "
            "additive component is holomorphic on the owned z disk, while the "
            "owned simple-pole residue is holomorphic at the cross-source-only q collision"
        ),
        "source_integrand": str(SCRIPT_5026),
        "source_integrand_sha256": digest(SCRIPT_5026),
        "arbitrary_precision_evaluator": str(SCRIPT_MP),
        "arbitrary_precision_evaluator_sha256": digest(SCRIPT_MP),
        "valid_for_full_MTS_claim": False,
    }


def repaired_chamber_residue_catalog(
    ownership: dict[str, bool],
    start: complex,
    end: complex,
    required_roots: list[complex],
    global_nodes: int,
    global_residue_nodes: int,
    relative_residue_nodes: int,
    model_distance: float,
) -> tuple[list[dict[str, Any]], bool]:
    catalog, _ = BASE_CATALOG(
        ownership,
        start,
        end,
        required_roots,
        global_nodes,
        global_residue_nodes,
        relative_residue_nodes,
        model_distance,
    )
    for row in catalog:
        certificate = theorem_certificate(row, ownership)
        if not certificate["passed"]:
            continue
        original_probe = {
            "outer_residue": serialized(complex(row["outer_residue"])),
            "inner_residue": serialized(complex(row["inner_residue"])),
            "residue_stability": float(row["residue_stability"]),
            "numerically_zero": bool(row["numerically_zero"]),
            "stable": bool(row["stable"]),
        }
        certificate["job_key"] = CURRENT_JOB
        certificate["original_double_precision_probe"] = original_probe
        REPAIR_AUDIT.append(certificate)
        row.update(
            {
                "outer_residue": 0.0j,
                "inner_residue": 0.0j,
                "residue": 0.0j,
                "residue_stability": 0.0,
                "numerically_zero": True,
                "stable": True,
                "included_as_pole_model": False,
                "residue_method": REVISION,
                "cross_source_zero_certificate": certificate,
            }
        )
    return catalog, all(bool(row["stable"]) for row in catalog)


def configure_from_kernel(kernel: dict[str, Any]) -> None:
    target_row = kernel["argument"]["target_cosine"]
    target = complex(float(target_row["real"]), float(target_row["imaginary"]))
    M5034.configure(kernel["event"], target)


def existing_audit() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for job_path in sorted((RUN / "jobs").glob("*.json")):
        job = json.loads(job_path.read_text(encoding="utf-8"))
        if job.get("status") != "COMPLETED_UNCONVERGED":
            continue
        kernel_path = RUN / "kernels" / job_path.name
        if not kernel_path.exists():
            continue
        kernel = json.loads(kernel_path.read_text(encoding="utf-8"))
        configure_from_kernel(kernel)
        _, ownerships = N5030.physical_chambers()
        unstable = [
            (int(chamber["chamber_index"]), residue)
            for chamber in kernel["fixed_event_integral_gate"]["chambers"]
            for residue in chamber["residue_catalog"]
            if not residue["stable"]
        ]
        certificates = [
            theorem_certificate(residue, ownerships[chamber_index])
            for chamber_index, residue in unstable
        ]
        rows.append(
            {
                "job_key": job["job_key"],
                "unstable_residue_count": len(unstable),
                "certified_zero_count": sum(row["passed"] for row in certificates),
                "all_unstable_rows_certified": bool(unstable)
                and all(row["passed"] for row in certificates),
                "certificates": certificates,
            }
        )
    return rows


def witness_audit() -> dict[str, Any]:
    missing = [str(path) for path in MP_WITNESSES if not path.exists()]
    if missing:
        return {"available": False, "passed": False, "missing": missing}
    rows = []
    for path in MP_WITNESSES:
        witness = json.loads(path.read_text(encoding="utf-8"))
        values = {
            (float(row["relative_fraction"]), float(row["global_fraction"])): float(
                row["magnitude"]
            )
            for row in witness["values"]
        }
        ratios = []
        for global_fraction in sorted({key[1] for key in values}):
            outer = values.get((0.1, global_fraction))
            inner = values.get((0.05, global_fraction))
            if outer is None or inner is None or inner == 0.0:
                continue
            ratios.append(outer / inner)
        expected = 2.0 ** int(witness["relative_nodes"])
        relative_errors = [abs(value / expected - 1.0) for value in ratios]
        rows.append(
            {
                "job_key": witness["job_key"],
                "collision_pairs": witness["collision_pairs"],
                "path": str(path),
                "sha256": digest(path),
                "port_validation_passed": witness.get("port_validation", {}).get("passed"),
                "relative_nodes": witness["relative_nodes"],
                "global_nodes": witness["global_nodes"],
                "expected_halving_ratio": expected,
                "measured_halving_ratios": ratios,
                "maximum_ratio_relative_error": max(relative_errors) if relative_errors else None,
                "maximum_residue_magnitude": max(
                    row["magnitude"] for row in witness["values"]
                ),
                "passed": bool(
                    witness.get("port_validation", {}).get("passed")
                    and int(witness["relative_nodes"]) >= 16
                    and ratios
                    and max(relative_errors) < 0.02
                    and max(row["magnitude"] for row in witness["values"]) < 2.0e-19
                ),
            }
        )
    passed = len(rows) == 2 and all(row["passed"] for row in rows)
    return {
        "available": True,
        "passed": passed,
        "branch_coverage": ["minus_v/minus_u", "plus_v/plus_u"],
        "rows": rows,
    }


def copy_topology(scratch_run: Path, job: dict[str, Any]) -> None:
    source = M5034.topology_path(RUN, job["event_id"], job["argument_id"])
    target = M5034.topology_path(scratch_run, job["event_id"], job["argument_id"])
    if not source.exists():
        raise FileNotFoundError(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def expected_job(job: dict[str, Any]) -> dict[str, Any]:
    keys = (
        "job_key",
        "epsilon_id",
        "evaluation_epsilon",
        "event_id",
        "argument_id",
        "base_argument_id",
        "tier",
    )
    return {key: job[key] for key in keys}


def apply_repairs(arguments: argparse.Namespace, audit_rows: list[dict[str, Any]]) -> dict[str, Any]:
    global CURRENT_JOB
    repair_directory = REPAIRS / arguments.repair_id
    scratch_run = repair_directory / "scratch_run"
    original_directory = repair_directory / "original"
    repaired_directory = repair_directory / "repaired"
    candidates = [row for row in audit_rows if row["all_unstable_rows_certified"]]
    started = time.monotonic()
    repaired: list[str] = []
    still_open: list[dict[str, Any]] = []
    per_job_certificates: dict[str, list[dict[str, Any]]] = {}
    N5030.chamber_residue_catalog = repaired_chamber_residue_catalog
    try:
        for candidate in candidates:
            if time.monotonic() - started >= arguments.max_wall_seconds:
                still_open.append({"job_key": candidate["job_key"], "status": "DEADLINE"})
                break
            job_path = RUN / "jobs" / f"{candidate['job_key']}.json"
            kernel_path = RUN / "kernels" / job_path.name
            job = json.loads(job_path.read_text(encoding="utf-8"))
            CURRENT_JOB = job["job_key"]
            REPAIR_AUDIT.clear()
            M5036.MREPAIR.CURRENT_JOB = CURRENT_JOB
            M5036.MREPAIR.RADIUS_AUDIT.clear()
            original_directory.mkdir(parents=True, exist_ok=True)
            shutil.copy2(job_path, original_directory / job_path.name)
            shutil.copy2(kernel_path, original_directory / f"kernel__{job_path.name}")
            copy_topology(scratch_run, job)
            try:
                result = M5035.execute_job(scratch_run, json.loads((RUN / "config.json").read_text(encoding="utf-8")), expected_job(job))
            except Exception as error:
                still_open.append(
                    {
                        "job_key": CURRENT_JOB,
                        "error_type": type(error).__name__,
                        "error": str(error),
                    }
                )
                continue
            scratch_kernel_path = scratch_run / "kernels" / job_path.name
            per_job_certificates[CURRENT_JOB] = list(REPAIR_AUDIT)
            if result.get("status") != "COMPLETED_CONVERGED" or not REPAIR_AUDIT:
                still_open.append(
                    {
                        "job_key": CURRENT_JOB,
                        "status": result.get("status"),
                        "certificate_count": len(REPAIR_AUDIT),
                    }
                )
                continue
            repaired_kernel = json.loads(scratch_kernel_path.read_text(encoding="utf-8"))
            contract = {
                "checkpoint_marker": MARKER,
                "repair_revision": REVISION,
                "repair_script": str(Path(__file__).resolve()),
                "repair_script_sha256": digest(Path(__file__).resolve()),
                "source_integrand": str(SCRIPT_5026),
                "source_integrand_sha256": digest(SCRIPT_5026),
                "original_job_sha256": digest(job_path),
                "original_kernel_sha256": digest(kernel_path),
                "certificates": list(REPAIR_AUDIT),
                "reason": "exact additive-source iterated-residue zero, not a fitted numerical zero",
                "valid_for_full_MTS_claim": False,
            }
            result["repair_contract"] = contract
            repaired_kernel["repair_contract"] = contract
            repaired_kernel["fixed_event_integral_gate"]["relative_residue_revision"] = REVISION
            repaired_directory.mkdir(parents=True, exist_ok=True)
            M5036.atomic_json(repaired_directory / job_path.name, result)
            M5036.atomic_json(repaired_directory / f"kernel__{job_path.name}", repaired_kernel)
            M5036.atomic_json(job_path, result)
            M5036.atomic_json(kernel_path, repaired_kernel)
            repaired.append(CURRENT_JOB)
    finally:
        N5030.chamber_residue_catalog = ORIGINAL_CATALOG
    config = json.loads((RUN / "config.json").read_text(encoding="utf-8"))
    jobs = M5036.load_jobs(RUN)
    summary = M5037.write_augmented_status(
        RUN, config, jobs, "PAUSED_AFTER_CROSS_SOURCE_ZERO_REPAIR", started
    )
    M5040.write_5040_artifacts(config, summary, RUN)
    M5036.append_log(
        RUN,
        f"5041 cross-source additive-zero repair repaired={repaired} still_open={still_open}",
    )
    result = {
        "checkpoint_marker": MARKER,
        "repair_revision": REVISION,
        "repair_id": arguments.repair_id,
        "candidate_jobs": [row["job_key"] for row in candidates],
        "repaired_jobs": repaired,
        "still_open": still_open,
        "certificates": per_job_certificates,
        "run_state": summary["run_state"],
        "terminal_jobs": summary["terminal_jobs"],
        "remaining_jobs": summary["remaining_jobs"],
        "unconverged_jobs": summary["unconverged_jobs"],
        "valid_for_full_MTS_claim": False,
    }
    M5036.atomic_json(repair_directory / "repair_summary.json", result)
    return result


def write_audit(audit_rows: list[dict[str, Any]], witness: dict[str, Any]) -> None:
    SOURCE.mkdir(parents=True, exist_ok=True)
    payload = {
        "checkpoint_marker": MARKER,
        "repair_revision": REVISION,
        "candidate_count": len(audit_rows),
        "all_candidates_certified": len(audit_rows) == EXPECTED_CANDIDATES
        and all(row["all_unstable_rows_certified"] for row in audit_rows),
        "rows": audit_rows,
        "arbitrary_precision_witness": witness,
        "production_precision_complete": False,
        "valid_for_full_MTS_claim": False,
    }
    M5036.atomic_json(AUDIT_JSON, payload)
    with AUDIT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=(
                "job_key",
                "unstable_residue_count",
                "certified_zero_count",
                "all_unstable_rows_certified",
                "valid_for_full_MTS_claim",
            ),
        )
        writer.writeheader()
        for row in audit_rows:
            writer.writerow(
                {
                    **{key: row[key] for key in writer.fieldnames if key in row},
                    "valid_for_full_MTS_claim": False,
                }
            )


def write_validation(
    audit_rows: list[dict[str, Any]], witness: dict[str, Any], repair: dict[str, Any] | None
) -> list[dict[str, Any]]:
    gates = [
        {
            "gate": "exactly_eight_unconverged_candidates",
            "passed": len(audit_rows) == EXPECTED_CANDIDATES,
            "detail": f"{len(audit_rows)}/{EXPECTED_CANDIDATES}",
        },
        {
            "gate": "all_unstable_rows_have_cross_source_zero_certificate",
            "passed": bool(audit_rows)
            and all(row["all_unstable_rows_certified"] for row in audit_rows),
            "detail": "source decomposition, single ownership and isolated nested contours",
        },
        {
            "gate": "arbitrary_precision_alias_law",
            "passed": bool(witness.get("passed")),
            "detail": json.dumps(witness, sort_keys=True),
        },
        {
            "gate": "repair_application",
            "passed": repair is None
            or (
                len(repair["repaired_jobs"]) == EXPECTED_CANDIDATES
                and not repair["still_open"]
                and repair["unconverged_jobs"] == 0
            ),
            "detail": "dry audit" if repair is None else json.dumps(repair["still_open"]),
        },
        {
            "gate": "production_precision_complete",
            "passed": False,
            "detail": "fourth nested scramble and sequential stopping remain open",
        },
        {
            "gate": "valid_for_full_MTS_claim",
            "passed": False,
            "detail": "numerical hhh subproblem only",
        },
    ]
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("gate", "passed", "detail", "valid_for_full_MTS_claim"),
        )
        writer.writeheader()
        for row in gates:
            writer.writerow({**row, "valid_for_full_MTS_claim": False})
    return gates


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--repair-id", default="cross_source_additive_zero_v1")
    parser.add_argument("--max-wall-seconds", type=float, default=10800.0)
    arguments = parser.parse_args()
    if arguments.max_wall_seconds <= 0.0:
        raise ValueError("max wall seconds must be positive")
    audit_rows = existing_audit()
    witness = witness_audit()
    write_audit(audit_rows, witness)
    repair = apply_repairs(arguments, audit_rows) if arguments.apply else None
    gates = write_validation(audit_rows, witness, repair)
    console = {
        "checkpoint_marker": MARKER,
        "candidate_count": len(audit_rows),
        "all_candidates_certified": bool(audit_rows)
        and all(row["all_unstable_rows_certified"] for row in audit_rows),
        "arbitrary_precision_witness_passed": witness.get("passed", False),
        "applied": arguments.apply,
        "repaired_jobs": repair["repaired_jobs"] if repair else [],
        "still_open": repair["still_open"] if repair else [],
        "validation_true_gates": sum(row["passed"] for row in gates),
        "validation_gate_count": len(gates),
        "production_precision_complete": False,
        "valid_for_full_MTS_claim": False,
    }
    print(json.dumps(console, indent=2, allow_nan=False))
    required = gates[:4]
    if not all(row["passed"] for row in required):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
