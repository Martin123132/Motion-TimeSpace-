from __future__ import annotations

import argparse
import csv
import ctypes
import hashlib
import importlib.util
import json
import os
import sys
import time
from pathlib import Path
from typing import Any


for thread_variable in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "BLIS_NUM_THREADS",
):
    os.environ[thread_variable] = "1"
os.environ["PYTHONNOUSERSITE"] = "1"
sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
RESIDUALS = POST / "source-intake" / "mts_residuals"
SOURCE = FUNCTIONAL_RG / "5289"

SCRIPT_5288 = (
    SCRIPTS / "Y5_R2FR_5288_failed_angular_node_singularity_derivation.py"
)
RESULT_5288 = (
    FUNCTIONAL_RG / "5288" / "failed_angular_node_singularity_result.json"
)
VALIDATION_5288 = (
    FUNCTIONAL_RG / "5288" / "failed_angular_node_singularity_validation.csv"
)
POLES_5288 = (
    FUNCTIONAL_RG / "5288" / "failed_node_selected_pole_residues.csv"
)
ENDPOINTS_5288 = (
    FUNCTIONAL_RG / "5288" / "lower_endpoint_physical_coefficients.csv"
)

DRY_RUN = SOURCE / "MC04_MC12_angular_pole_dry_run.json"
SYMMETRY_AUDIT = SOURCE / "MC04_MC12_antisymmetry_audit.csv"
SCANNED_POLES = SOURCE / "MC04_owner_geometric_pole_scan.csv"
CLASSIFIED_POLES = SOURCE / "MC04_owner_exact_mask_poles.csv"
CHANNEL_ROOTS = SOURCE / "MC04_owner_channel_roots.csv"
POLE_SAMPLES = SOURCE / "MC04_owner_pole_samples.csv"
POLE_FITS = SOURCE / "MC04_owner_pole_fits.csv"
OWNER_RESIDUES = SOURCE / "MC04_owner_selected_pole_residues.csv"
FINAL_RESIDUES = SOURCE / "MC04_MC12_selected_pole_residues.csv"
RESULT = SOURCE / "MC04_MC12_angular_pole_result.json"
VALIDATION = SOURCE / "MC04_MC12_angular_pole_validation.csv"
RESIDUAL_VALIDATION = (
    RESIDUALS / "P8_Y5_BRR545_5289_VALIDATION.csv"
)
STATUS = SOURCE / "status.json"
DOCUMENT = POST / "5289-Y5-R2FR-MC04-MC12-angular-pole-derivation.md"

CHECKPOINT = 5289
PARENT_CHECKPOINT = 5288
MARKER = "MTS_5289_MC04_MC12_ANGULAR_POLE_DERIVATION"
REVISION = "MC04-MC12-angular-pole-derivation-v1"
REGULATOR_IDS = ("E040", "E020")
OWNER_NODE_ID = "A02_S02_D01"
OWNER_COMPONENT_ID = "MC04"
MIRROR_NODE_ID = "A02_S02_D02"
MIRROR_COMPONENT_ID = "MC12"
SYMMETRY_TEST_ENERGIES = (
    2.0e-4,
    2.0e-3,
    1.0e-1,
    3.0e-1,
    5.0e-1,
    9.0e-1,
    9.8e-1,
    9.98e-1,
)
SYMMETRY_RELATIVE_LIMIT = 1.0e-12
CLAIM_FIELDS = (
    "valid_for_full_phase_space_coefficient",
    "valid_for_numeric_UV_claim",
    "valid_for_local_GR_claim",
    "valid_for_full_MTS_claim",
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5288 = load_module("mts_5288_for_5289", SCRIPT_5288)
M5287 = M5288.M5287
M5283 = M5288.M5283
M5280 = M5288.M5280
M5286 = M5288.M5286
M5267 = M5288.M5267
mp = M5288.mp


def set_below_normal_priority() -> None:
    if os.name != "nt":
        return
    handle = ctypes.windll.kernel32.GetCurrentProcess()
    ctypes.windll.kernel32.SetPriorityClass(handle, 0x00004000)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise RuntimeError(f"refusing to write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def complex_fields(prefix: str, value: complex) -> dict[str, float]:
    return {
        f"{prefix}_real": float(value.real),
        f"{prefix}_imaginary": float(value.imag),
        f"{prefix}_magnitude": float(abs(value)),
    }


def relative_complex_difference(first: complex, second: complex) -> float:
    return abs(first - second) / max(abs(first), abs(second), 1.0e-300)


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5288,
        RESULT_5288,
        VALIDATION_5288,
        POLES_5288,
        ENDPOINTS_5288,
        M5267.MANIFEST_5239,
        M5288.ANGULAR_NODES_5286,
    )
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in paths
    ]


def owner_problems_and_poles() -> tuple[
    list[dict[str, Any]],
    dict[tuple[str, str, str], dict[str, Any]],
]:
    node = M5288.angular_node_lookup()[OWNER_NODE_ID]
    problems: dict[tuple[str, str, str], dict[str, Any]] = {}
    rows: list[dict[str, Any]] = []
    reusable: list[dict[str, str]] = []
    if SCANNED_POLES.exists():
        reusable = read_csv(SCANNED_POLES)
    for epsilon_id in REGULATOR_IDS:
        key = (OWNER_NODE_ID, epsilon_id, OWNER_COMPONENT_ID)
        problem = M5286.angular_problem(
            M5288.manifest_job(epsilon_id, OWNER_COMPONENT_ID),
            float(node["soft_cosine"]),
            float(node["decay_cosine"]),
        )
        problems[key] = problem
        local_reusable = [
            row
            for row in reusable
            if row["epsilon_id"] == epsilon_id
            and row["angular_node_id"] == OWNER_NODE_ID
            and row["component_id"] == OWNER_COMPONENT_ID
        ]
        if local_reusable:
            rows.extend(local_reusable)
        else:
            _, _, poles, _ = M5267.M5239.scan_problem(problem)
            rows.extend(
                {
                    "angular_node_id": OWNER_NODE_ID,
                    "soft_cosine": node["soft_cosine"],
                    "decay_cosine": node["decay_cosine"],
                    **source,
                    "symmetry_derived": False,
                    "valid_for_MC04_owner_pole_scan": True,
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
                for source in poles
            )
        atomic_json(
            STATUS,
            {
                "checkpoint": CHECKPOINT,
                "state": "RUNNING",
                "stage": "OWNER_POLE_SCAN",
                "last_completed_epsilon_id": epsilon_id,
                "pole_count": len(rows),
            },
        )
    return rows, problems


def antisymmetry_audit(
    base_context: dict[str, Any],
) -> list[dict[str, Any]]:
    nodes = M5288.angular_node_lookup()
    owner_context = M5287.local_context(
        base_context,
        nodes[OWNER_NODE_ID],
    )
    mirror_context = M5287.local_context(
        base_context,
        nodes[MIRROR_NODE_ID],
    )
    owner_cache: dict[tuple[str, float, str], Any] = {}
    mirror_cache: dict[tuple[str, float, str], Any] = {}
    rows: list[dict[str, Any]] = []
    for epsilon_id in REGULATOR_IDS:
        for energy in SYMMETRY_TEST_ENERGIES:
            owner = M5287.evaluate_component_cached(
                owner_context,
                epsilon_id,
                OWNER_COMPONENT_ID,
                energy,
                owner_cache,
                convergence_audit=True,
            )
            mirror = M5287.evaluate_component_cached(
                mirror_context,
                epsilon_id,
                MIRROR_COMPONENT_ID,
                energy,
                mirror_cache,
                convergence_audit=True,
            )
            owner_value = complex(owner["residue"])
            mirror_value = complex(mirror["residue"])
            residual = owner_value + mirror_value
            relative = abs(residual) / max(
                abs(owner_value),
                abs(mirror_value),
                1.0e-300,
            )
            passed = (
                relative <= SYMMETRY_RELATIVE_LIMIT
                and parse_bool(owner["mask_active"])
                == parse_bool(mirror["mask_active"])
            )
            rows.append(
                {
                    "owner_angular_node_id": OWNER_NODE_ID,
                    "owner_component_id": OWNER_COMPONENT_ID,
                    "mirror_angular_node_id": MIRROR_NODE_ID,
                    "mirror_component_id": MIRROR_COMPONENT_ID,
                    "epsilon_id": epsilon_id,
                    "soft_energy": energy,
                    **complex_fields("owner_residue", owner_value),
                    **complex_fields("mirror_residue", mirror_value),
                    **complex_fields(
                        "antisymmetry_residual",
                        residual,
                    ),
                    "relative_antisymmetry_residual": relative,
                    "owner_mask_active": owner["mask_active"],
                    "mirror_mask_active": mirror["mask_active"],
                    "antisymmetry_passed": passed,
                    "valid_for_MC04_MC12_residue_transport": passed,
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    return rows


def mirror_selected_residues(
    owner_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows = [dict(row) for row in owner_rows]
    for source in owner_rows:
        row = dict(source)
        row["angular_node_id"] = MIRROR_NODE_ID
        row["component_id"] = MIRROR_COMPONENT_ID
        row["pole_id"] = str(row["pole_id"]).replace(
            OWNER_COMPONENT_ID,
            MIRROR_COMPONENT_ID,
        )
        row["true_limit_residue_real"] = -float(
            row["true_limit_residue_real"]
        )
        row["true_limit_residue_imaginary"] = -float(
            row["true_limit_residue_imaginary"]
        )
        row["symmetry_derived"] = True
        row["symmetry_sign"] = -1
        row["symmetry_source_angular_node_id"] = OWNER_NODE_ID
        row["symmetry_source_component_id"] = OWNER_COMPONENT_ID
        rows.append(row)
    for row in rows[: len(owner_rows)]:
        row["symmetry_derived"] = False
        row["symmetry_sign"] = 1
    return rows


def dry_run() -> dict[str, Any]:
    SOURCE.mkdir(parents=True, exist_ok=True)
    required = (
        SCRIPT_5288,
        RESULT_5288,
        VALIDATION_5288,
        POLES_5288,
        ENDPOINTS_5288,
        M5267.MANIFEST_5239,
        M5288.ANGULAR_NODES_5286,
    )
    parent = read_json(RESULT_5288)
    checks = {
        "required_sources_exist": all(path.exists() for path in required),
        "parent_5288_accepted": bool(parent["acceptance_passed"]),
        "parent_5288_validated": all(
            parse_bool(row["passed"]) for row in read_csv(VALIDATION_5288)
        ),
        "first_promoted_pole_family_certified": (
            parent["material_pole_count"] == 8
        ),
        "endpoint_pair_cancellation_certified": all(
            parse_bool(row["pairwise_endpoint_cancellation_passed"])
            for row in read_csv(ENDPOINTS_5288)
        ),
        "formalization_workbench_unchanged": (
            M5283.formal_inventory_digest()
            == str(parent["formalization_workbench_end_digest"])
        ),
    }
    accepted = all(checks.values())
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "dry-run",
        "checks": checks,
        "acceptance_passed": accepted,
        "decision": (
            "DRY_RUN_ACCEPTED__DERIVE_MC04_MC12_ANGULAR_POLES"
            if accepted
            else "DRY_RUN_REQUIRES_REPAIR"
        ),
        "runtime_seconds": 0.0,
        "valid_for_full_phase_space_coefficient": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(DRY_RUN, result)
    return result


def execute() -> dict[str, Any]:
    started = time.perf_counter()
    set_below_normal_priority()
    mp.mp.dps = M5280.MP_DECIMAL_DIGITS
    dry = dry_run()
    if not dry["acceptance_passed"]:
        raise RuntimeError("5289 dry run did not pass")
    parent = read_json(RESULT_5288)
    base_context = M5280.source_context()
    symmetry = antisymmetry_audit(base_context)
    scanned, problems = owner_problems_and_poles()
    classified = M5288.classify_exact_masks(scanned, base_context)
    roots = M5288.refine_active_channel_roots(classified, problems)
    M5288.STATUS = STATUS
    samples, fits, owner_selected = M5288.derive_pole_residues(
        roots,
        problems,
        base_context,
    )
    selected = mirror_selected_residues(owner_selected)
    active = [
        row for row in classified if parse_bool(row["exact_mask_active"])
    ]
    material_owner = [
        row
        for row in owner_selected
        if parse_bool(row["material_pole"])
    ]
    material_all = [
        row for row in selected if parse_bool(row["material_pole"])
    ]
    checks = {
        "MC04_MC12_antisymmetry_certified": (
            len(symmetry)
            == len(REGULATOR_IDS) * len(SYMMETRY_TEST_ENERGIES)
            and all(
                parse_bool(row["antisymmetry_passed"])
                for row in symmetry
            )
        ),
        "two_owner_poles_per_regulator_scanned": (
            len(scanned) == 2 * len(REGULATOR_IDS)
        ),
        "all_owner_poles_exact_mask_active": (
            len(active) == len(scanned)
        ),
        "all_owner_pole_routes_available": (
            len(roots) == len(active)
            and all(
                parse_bool(row["root_or_fallback_route_available"])
                for row in roots
            )
        ),
        "all_owner_residues_controlled": (
            len(owner_selected) == len(active)
            and all(
                parse_bool(row["pole_residue_controls_pass"])
                for row in owner_selected
            )
        ),
        "one_material_one_removable_per_regulator": (
            len(material_owner) == len(REGULATOR_IDS)
            and len(owner_selected) - len(material_owner)
            == len(REGULATOR_IDS)
        ),
        "mirror_residue_inventory_complete": (
            len(material_all) == 2 * len(material_owner)
        ),
        "formalization_workbench_unchanged": (
            M5283.formal_inventory_digest()
            == str(parent["formalization_workbench_end_digest"])
        ),
        "claims_locked_false": True,
    }
    accepted = all(checks.values())
    formal_end = M5283.formal_inventory_digest()
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "MC04-MC12-angular-pole-derivation",
        "checks": checks,
        "acceptance_passed": accepted,
        "owner_scanned_pole_count": len(scanned),
        "owner_exact_active_pole_count": len(active),
        "owner_material_pole_count": len(material_owner),
        "combined_material_pole_count": len(material_all),
        "maximum_antisymmetry_relative_residual": max(
            float(row["relative_antisymmetry_residual"])
            for row in symmetry
        ),
        "maximum_selected_fit_residual": max(
            float(row["fit_relative_residual"])
            for row in owner_selected
        ),
        "maximum_selected_refinement_change": max(
            float(row["refinement_relative_change"])
            for row in owner_selected
        ),
        "maximum_selected_degree_change": max(
            float(row["degree_relative_change"])
            for row in owner_selected
        ),
        "source_files": source_rows(),
        "formalization_workbench_reference_digest": str(
            parent["formalization_workbench_end_digest"]
        ),
        "formalization_workbench_end_digest": formal_end,
        "formalization_workbench_modified_file_count": (
            0
            if formal_end
            == str(parent["formalization_workbench_end_digest"])
            else -1
        ),
        "resource_contract": {
            "maximum_task_python_processes": 1,
            "worker_math_threads": 1,
            "windows_priority": "BelowNormal",
            "sustained_redline_forbidden": True,
        },
        "runtime_seconds": time.perf_counter() - started,
        "decision": (
            "CERTIFY_MC04_MC12_ANGULAR_POLES__"
            "RUN_ALL_FAMILY_COMBINED_SUBTRACTION"
            if accepted
            else "MC04_MC12_ANGULAR_POLE_DERIVATION_REQUIRES_REPAIR"
        ),
        "claim_boundary": {
            "valid_for_MC04_MC12_pole_subtraction": accepted,
            "valid_for_all_family_combined_subtraction_runner": accepted,
            "valid_for_converged_angular_integration": False,
            "valid_for_full_phase_space_coefficient": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "The second angularly promoted pole family is now "
                "derived and transported by pointwise antisymmetry. "
                "The stored energy nodes must still be reassembled with "
                "both promoted families before convergence is assessed."
            ),
        },
    }
    write_csv(SYMMETRY_AUDIT, symmetry)
    write_csv(SCANNED_POLES, scanned)
    write_csv(CLASSIFIED_POLES, classified)
    write_csv(CHANNEL_ROOTS, roots)
    write_csv(POLE_SAMPLES, samples)
    write_csv(POLE_FITS, fits)
    write_csv(OWNER_RESIDUES, owner_selected)
    write_csv(FINAL_RESIDUES, selected)
    atomic_json(RESULT, result)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": "COMPLETED",
            "acceptance_passed": accepted,
            "decision": result["decision"],
            "runtime_seconds": result["runtime_seconds"],
        },
    )
    return result


def validation_gate(
    gate_id: str,
    passed: bool,
    detail: str,
) -> dict[str, Any]:
    return {
        "gate_id": gate_id,
        "passed": passed,
        "detail": detail,
    }


def render_document(result: dict[str, Any], validation_passed: bool) -> None:
    text = f"""# 5289 — MC04/MC12 angular-pole derivation

## Why this checkpoint exists

The 5288 stored-node replay removed the newly derived `MC03/MC08` poles,
but the `A02_S02_D01` and `A02_S02_D02` energy rules remained unstable.
Their paired lower-endpoint coefficients cancel, so the residual could
not honestly be assigned to the endpoint. A fresh geometric scan finds
the omitted `MC04/MC12` angular pole family.

## Result

- owner poles scanned: `{result['owner_scanned_pole_count']}`;
- owner exact-active poles: `{result['owner_exact_active_pole_count']}`;
- owner material poles: `{result['owner_material_pole_count']}`;
- owner plus mirror material poles:
  `{result['combined_material_pole_count']}`;
- maximum pointwise `MC04 + MC12` antisymmetry residual:
  `{result['maximum_antisymmetry_relative_residual']:.12g}`;
- maximum selected residue-fit residual:
  `{result['maximum_selected_fit_residual']:.12g}`;
- validation passed: `{validation_passed}`.

The `MC12` residues are not guessed. They are transported from `MC04`
with sign `-1` only after a pointwise two-regulator antisymmetry audit.

## Decision

`{result['decision']}`

This closes the second promoted-pole inventory. It does not yet establish
energy, angular, full phase-space, UV, local-GR, or full-MTS convergence.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    started = time.perf_counter()
    required_csvs = (
        SYMMETRY_AUDIT,
        SCANNED_POLES,
        CLASSIFIED_POLES,
        CHANNEL_ROOTS,
        POLE_SAMPLES,
        POLE_FITS,
        OWNER_RESIDUES,
        FINAL_RESIDUES,
    )
    if not RESULT.exists():
        raise RuntimeError(f"missing result: {RESULT}")
    result = read_json(RESULT)
    csv_rows = {path: read_csv(path) for path in required_csvs}
    serialized = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (*required_csvs, RESULT)
    )
    claim_rows = [
        row
        for rows in csv_rows.values()
        for row in rows
        if any(field in row for field in CLAIM_FIELDS)
    ]
    source_files = result["source_files"]
    current_formal_digest = M5283.formal_inventory_digest()
    reference_formal_digest = str(
        result["formalization_workbench_reference_digest"]
    )
    rows = [
        validation_gate(
            "SOURCE_PATHS_EXIST",
            all(Path(row["path"]).exists() for row in source_files),
            f"{len(source_files)} source paths",
        ),
        validation_gate(
            "SOURCE_HASHES_MATCH",
            all(
                digest(Path(row["path"])) == row["sha256"]
                for row in source_files
            ),
            "all recorded source hashes reproduce",
        ),
        validation_gate(
            "PARENT_5288_ACCEPTED",
            bool(read_json(RESULT_5288)["acceptance_passed"]),
            str(read_json(RESULT_5288)["decision"]),
        ),
        validation_gate(
            "MC04_MC12_DERIVATION_ACCEPTED",
            bool(result["acceptance_passed"]),
            str(result["decision"]),
        ),
        validation_gate(
            "REQUIRED_CSVS_PARSE",
            len(csv_rows) == len(required_csvs)
            and all(csv_rows.values()),
            f"{len(csv_rows)}/{len(required_csvs)} non-empty CSVs",
        ),
        validation_gate(
            "FOUR_COMBINED_MATERIAL_POLES",
            result["combined_material_pole_count"] == 4,
            str(result["combined_material_pole_count"]),
        ),
        validation_gate(
            "NO_MISSING_MARKERS",
            "MISSING_" not in serialized,
            "no MISSING_ token in checkpoint artifacts",
        ),
        validation_gate(
            "CLAIMS_LOCKED_FALSE",
            (
                all(
                    not result["claim_boundary"][field]
                    for field in CLAIM_FIELDS
                )
                and all(
                    row.get(field, "false").lower() == "false"
                    for row in claim_rows
                    for field in CLAIM_FIELDS
                    if field in row
                )
            ),
            "phase-space, UV, local-GR, and full-MTS claims false",
        ),
        validation_gate(
            "FORMALIZATION_WORKBENCH_UNCHANGED",
            current_formal_digest == reference_formal_digest,
            (
                f"reference={reference_formal_digest}; "
                f"current={current_formal_digest}"
            ),
        ),
        validation_gate(
            "RESOURCE_CONTRACT_RECORDED",
            (
                result["resource_contract"][
                    "maximum_task_python_processes"
                ]
                == 1
                and result["resource_contract"]["worker_math_threads"] == 1
            ),
            "one below-normal single-thread process",
        ),
    ]
    passed = all(row["passed"] for row in rows)
    write_csv(VALIDATION, rows)
    write_csv(RESIDUAL_VALIDATION, rows)
    render_document(result, passed)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": "COMPLETED",
            "mode": "validation",
            "validation_passed": passed,
            "validation_gate_count": len(rows),
            "decision": result["decision"],
        },
    )
    return {
        "checkpoint": CHECKPOINT,
        "mode": "validation",
        "acceptance_passed": passed,
        "decision": (
            "VALIDATED_MC04_MC12_ANGULAR_POLE_DERIVATION"
            if passed
            else "MC04_MC12_ANGULAR_POLE_VALIDATION_FAILED"
        ),
        "runtime_seconds": time.perf_counter() - started,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("dry-run", "run", "validate"),
        default="dry-run",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.mode == "dry-run":
        result = dry_run()
    elif args.mode == "run":
        result = execute()
    elif args.mode == "validate":
        result = validate_outputs()
    else:
        raise RuntimeError(f"unsupported mode: {args.mode}")
    print(
        json.dumps(
            {
                "checkpoint": result["checkpoint"],
                "mode": result["mode"],
                "acceptance_passed": result["acceptance_passed"],
                "decision": result["decision"],
                "runtime_seconds": result["runtime_seconds"],
            },
            sort_keys=True,
        )
    )
    return 0 if result["acceptance_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
