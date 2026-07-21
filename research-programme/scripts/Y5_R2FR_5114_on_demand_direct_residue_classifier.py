from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
from typing import Any

import mpmath as mp


POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMAL = ROOT / "formalization-workbench"
SCRIPT_5112 = (
    POST
    / "scripts"
    / "Y5_R2FR_5112_recoil_holomorphy_scope_correction.py"
)
PARENT_SCOPE_GATE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5112"
    / "recoil_holomorphy_scope_correction.json"
)
PARENT_EXTENSION_GATE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5113"
    / "S507614_A00_event_local_recoil_resolution.json"
)
PARENT_REGISTRY = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5113"
    / "event_local_direct_zero_registry_v2.json"
)
RUN = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5111"
    / "runs"
    / "E020_primary_complex_control_extension_v1"
)
JOB_KEY = "E020__S507614_N0000__A01__primary24"
JOB = RUN / "jobs" / f"{JOB_KEY}.json"
KERNEL = RUN / "kernels" / f"{JOB_KEY}.json"
SOURCE = POST / "source-intake" / "functional_rg" / "5114"
RESULT_JSON = SOURCE / "on_demand_direct_residue_classifier_gate.json"
REGISTRY_JSON = SOURCE / "event_local_direct_zero_registry_v3.json"
AUDIT_CSV = SOURCE / "S507614_A01_direct_component_audit.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5114_VALIDATION.csv"
)
MARKER = "MTS_5114_ON_DEMAND_DIRECT_RESIDUE_CLASSIFIER"
REVISION = "fail-closed-source-separated-arbitrary-precision-fallback-v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
DPS = 60
RELATIVE_NODES = 24
GLOBAL_NODES = 24
RELATIVE_FRACTIONS = (0.1, 0.05)
GLOBAL_FRACTIONS = (0.15, 0.3)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5112 = load_module("mts_5112_for_5114", SCRIPT_5112)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def cross_source_recoil_scope(
    row: dict[str, Any], ownership: dict[str, bool]
) -> tuple[bool, str]:
    pairs = [tuple(str(value) for value in pair) for pair in row["pairs"]]
    if len(pairs) != 1:
        return False, "not_a_single_collision_pair"
    labels = set(pairs[0])
    if len(labels) != 2:
        return False, "collision_pair_does_not_have_two_labels"
    components = {
        "direct" if label.startswith("direct:") else "subtraction"
        for label in labels
    }
    owned = [label for label in labels if bool(ownership.get(label, False))]
    if components != {"direct", "subtraction"}:
        return False, "not_cross_additive"
    if len(owned) != 1 or not owned[0].startswith(("direct:g1:", "direct:g2:")):
        return False, "owned_label_is_not_one_direct_recoil_pole"
    root = complex(row["root"])
    fraction = float(row["residue_contour_fraction"])
    radius = float(row["outer_radius"])
    if abs(root) <= 1.0e-10 or not math.isfinite(fraction * radius):
        return False, "invalid_relative_root_or_radius"
    if fraction <= 0.0 or radius <= 0.0:
        return False, "nonpositive_relative_contour"
    return True, "exact_single_cross-additive_owned-g1-g2_scope"


def resolve_unstable_record(
    row: dict[str, Any],
    ownership: dict[str, bool],
    job_key: str,
    event: dict[str, Any],
    argument: dict[str, Any],
) -> dict[str, Any]:
    in_scope, reason = cross_source_recoil_scope(row, ownership)
    if not in_scope:
        return {
            "classification": "OUT_OF_SCOPE",
            "reason": reason,
            "job_key": job_key,
            "valid_for_full_MTS_claim": False,
        }
    safe_scale = float(row["outer_radius"]) / float(
        row["residue_contour_fraction"]
    )
    record = {
        "scope": "on_demand_exact_job_direct_component_resolution",
        "job_key": job_key,
        "event": event,
        "argument": argument,
        "pairs": [list(pair) for pair in row["pairs"]],
        "root": {
            "real": complex(row["root"]).real,
            "imaginary": complex(row["root"]).imag,
        },
        "safe_scale": safe_scale,
        "source_numeric_probe": {
            "outer_residue": str(row["outer_residue"]),
            "inner_residue": str(row["inner_residue"]),
            "residue_stability": float(row["residue_stability"]),
            "numerically_zero": bool(row["numerically_zero"]),
            "stable": bool(row["stable"]),
        },
    }
    previous_dps = mp.mp.dps
    try:
        mp.mp.dps = DPS
        result = M5112.evaluate_record(
            record,
            relative_nodes=RELATIVE_NODES,
            global_nodes=GLOBAL_NODES,
            relative_fractions=RELATIVE_FRACTIONS,
            global_fractions=GLOBAL_FRACTIONS,
        )
    finally:
        mp.mp.dps = previous_dps
    result["fallback_contract"] = {
        "dps": DPS,
        "relative_nodes": RELATIVE_NODES,
        "global_nodes": GLOBAL_NODES,
        "relative_fractions": list(RELATIVE_FRACTIONS),
        "global_fractions": list(GLOBAL_FRACTIONS),
        "source_component": "direct_only",
        "subtraction_local_residue": "zero_by_Cauchy_on_the_isolated_owned_global_cycle",
        "unresolved_action": "fail_closed",
    }
    return result


def source_record() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    job = json.loads(JOB.read_text(encoding="utf-8"))
    kernel = json.loads(KERNEL.read_text(encoding="utf-8"))
    unresolved = [
        row
        for row in job["profile_audit"]["residue_radius_adjustments"]
        if not bool(row["selected_stable"])
    ]
    if job["status"] != "COMPLETED_UNCONVERGED" or len(unresolved) != 1:
        raise RuntimeError("5114 source job is not the expected one-row blocker")
    adjustment = unresolved[0]
    row = {
        "root": complex(
            float(adjustment["root"]["real"]),
            float(adjustment["root"]["imaginary"]),
        ),
        "pairs": [tuple(pair) for pair in adjustment["pairs"]],
        "outer_radius": float(adjustment["selected_fraction"])
        * float(adjustment["safe_scale"]),
        "residue_contour_fraction": float(adjustment["selected_fraction"]),
        "outer_residue": complex(adjustment["candidate_rows"][2]["outer"]["real"], adjustment["candidate_rows"][2]["outer"]["imaginary"]),
        "inner_residue": complex(adjustment["candidate_rows"][2]["inner"]["real"], adjustment["candidate_rows"][2]["inner"]["imaginary"]),
        "residue_stability": float(adjustment["candidate_rows"][2]["stability"]),
        "numerically_zero": False,
        "stable": False,
    }
    return row, kernel["event"], kernel["argument"]


def main() -> None:
    row, event, argument = source_record()
    M5112.M5040.M5034.configure(
        event,
        complex(
            float(argument["target_cosine"]["real"]),
            float(argument["target_cosine"]["imaginary"]),
        ),
    )
    ownership = M5112.N5030.physical_chambers()[1][0]
    resolved = resolve_unstable_record(row, ownership, JOB_KEY, event, argument)
    parent_scope = json.loads(PARENT_SCOPE_GATE.read_text(encoding="utf-8"))
    parent_extension = json.loads(PARENT_EXTENSION_GATE.read_text(encoding="utf-8"))
    parent_registry = json.loads(PARENT_REGISTRY.read_text(encoding="utf-8"))
    new_rows = (
        [M5112.registry_row(resolved)]
        if resolved["classification"] == "EVENT_LOCAL_ARBITRARY_PRECISION_ZERO"
        else []
    )
    registry = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "policy": "merged exact-event zero registry plus authorized fail-closed on-demand classifier",
        "parent_registry": str(PARENT_REGISTRY.resolve()),
        "parent_registry_sha256": digest(PARENT_REGISTRY),
        "rows": [*parent_registry["rows"], *new_rows],
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(REGISTRY_JSON, registry)
    AUDIT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with AUDIT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(("job_key", "pairs", "root", "maximum_magnitude", "maximum_spread", "classification"))
        writer.writerow(
            (
                JOB_KEY,
                json.dumps(resolved["pairs"], separators=(",", ":")),
                json.dumps(resolved["root"], separators=(",", ":")),
                resolved["maximum_magnitude"],
                resolved["maximum_spread"],
                resolved["classification"],
            )
        )
    outer_witness = next(
        record
        for record in parent_scope["records"]
        if record["scope"] == "5111_first_job_outer_collision"
    )
    formal_hash = M5112.tree_digest(FORMAL)
    checks = [
        ("formalization_workbench_unchanged", formal_hash == FORMAL_BASELINE, formal_hash),
        ("source_row_resolved", resolved["classification"] != "UNRESOLVED", resolved["classification"]),
        (
            "source_row_is_event_local_zero",
            resolved["classification"] == "EVENT_LOCAL_ARBITRARY_PRECISION_ZERO",
            str(resolved["maximum_magnitude"]),
        ),
        (
            "stable_nonzero_branch_witness_exists",
            outer_witness["classification"] == "STABLE_DIRECT_COMPONENT_NONZERO",
            str(outer_witness["mean"]),
        ),
        (
            "parent_chain_passed",
            bool(parent_scope["passed"] and parent_extension["passed"]),
            f"{parent_scope['checkpoint_marker']} -> {parent_extension['checkpoint_marker']}",
        ),
        (
            "registry_extended_once",
            len(registry["rows"]) == len(parent_registry["rows"]) + 1,
            str(len(registry["rows"])),
        ),
    ]
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(("check", "passed", "detail"))
        for name, passed, detail in checks:
            writer.writerow((name, str(bool(passed)).lower(), detail))
    passed = all(check[1] for check in checks)
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "source_job": str(JOB.resolve()),
        "source_job_sha256": digest(JOB),
        "source_kernel": str(KERNEL.resolve()),
        "source_kernel_sha256": digest(KERNEL),
        "resolved_record": resolved,
        "parent_scope_gate": str(PARENT_SCOPE_GATE.resolve()),
        "parent_scope_gate_sha256": digest(PARENT_SCOPE_GATE),
        "parent_extension_gate": str(PARENT_EXTENSION_GATE.resolve()),
        "parent_extension_gate_sha256": digest(PARENT_EXTENSION_GATE),
        "parent_registry": str(PARENT_REGISTRY.resolve()),
        "parent_registry_sha256": digest(PARENT_REGISTRY),
        "merged_registry": str(REGISTRY_JSON.resolve()),
        "merged_registry_sha256": digest(REGISTRY_JSON),
        "on_demand_classifier_authorized": passed,
        "stable_nonzero_replacement_authorized": passed,
        "event_local_zero_replacement_authorized": passed,
        "unresolved_action": "fail_closed",
        "formalization_workbench_tree_sha256": formal_hash,
        "passed": passed,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    print(
        json.dumps(
            {
                "checkpoint_marker": MARKER,
                "classification": resolved["classification"],
                "maximum_magnitude": resolved["maximum_magnitude"],
                "on_demand_classifier_authorized": passed,
                "passed": passed,
            },
            indent=2,
        )
    )
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
