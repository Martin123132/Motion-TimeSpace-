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
PARENT_CLASSIFIER_GATE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5114"
    / "on_demand_direct_residue_classifier_gate.json"
)
RUN = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5111"
    / "runs"
    / "E020_primary_complex_control_extension_v1"
)
JOB_KEY = "E020__S507615_N0000__A01__primary24"
JOB = RUN / "jobs" / f"{JOB_KEY}.json"
KERNEL = RUN / "kernels" / f"{JOB_KEY}.json"
SOURCE = POST / "source-intake" / "functional_rg" / "5115"
RESULT_JSON = SOURCE / "general_on_demand_owned_direct_classifier_gate.json"
AUDIT_CSV = SOURCE / "S507615_A01_same_source_direct_audit.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5115_VALIDATION.csv"
)
MARKER = "MTS_5115_GENERAL_ON_DEMAND_OWNED_DIRECT_CLASSIFIER"
REVISION = "cross-additive-or-opposite-ownership-same-source-direct-fallback-v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
DPS = 60
RELATIVE_NODES = 24
GLOBAL_NODES = 24
GLOBAL_FRACTIONS = (0.15, 0.3)
SAME_SOURCE_SUFFIX_PAIRS = {
    frozenset(("minus_u", "plus_u")),
    frozenset(("minus_v", "plus_v")),
}


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5112 = load_module("mts_5112_for_5115", SCRIPT_5112)


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


def source(label: str) -> str:
    return label.rsplit(":", 1)[0]


def suffix(label: str) -> str:
    return label.rsplit(":", 1)[1]


def classify_scope(
    row: dict[str, Any], ownership: dict[str, bool]
) -> tuple[str, str]:
    pairs = [tuple(str(value) for value in pair) for pair in row["pairs"]]
    if len(pairs) != 1 or len(set(pairs[0])) != 2:
        return "OUT_OF_SCOPE", "requires_one_two-label_collision_pair"
    labels = tuple(pairs[0])
    owned = [label for label in labels if bool(ownership.get(label, False))]
    if len(owned) != 1 or not owned[0].startswith(("direct:g1:", "direct:g2:")):
        return "OUT_OF_SCOPE", "requires_exactly_one_owned_direct_g1_or_g2_label"
    components = {
        "direct" if label.startswith("direct:") else "subtraction"
        for label in labels
    }
    if components == {"direct", "subtraction"}:
        return "CROSS_ADDITIVE", "isolated_owned_direct_component"
    if (
        components == {"direct"}
        and source(labels[0]) == source(labels[1])
        and source(labels[0]) in {"direct:g1", "direct:g2"}
        and frozenset(suffix(label) for label in labels)
        in SAME_SOURCE_SUFFIX_PAIRS
        and bool(ownership[labels[0]]) != bool(ownership[labels[1]])
    ):
        return "SAME_SOURCE_OPPOSITE_OWNERSHIP", "owned-pole residue on the pinched pair"
    return "OUT_OF_SCOPE", "pair_is_not_an_authorized_owned-direct_configuration"


def configured_chamber_index(
    event: dict[str, Any],
    argument: dict[str, Any],
    ownership: dict[str, bool],
) -> int:
    target = complex(
        float(argument["target_cosine"]["real"]),
        float(argument["target_cosine"]["imaginary"]),
    )
    M5112.M5040.M5034.configure(event, target)
    matches = [
        index
        for index, candidate in enumerate(M5112.N5030.physical_chambers()[1])
        if candidate == ownership
    ]
    if len(matches) != 1:
        raise RuntimeError(f"ownership matched {len(matches)} physical chambers")
    return matches[0]


def resolve_unstable_record(
    row: dict[str, Any],
    ownership: dict[str, bool],
    job_key: str,
    event: dict[str, Any],
    argument: dict[str, Any],
) -> dict[str, Any]:
    scope, reason = classify_scope(row, ownership)
    if scope == "OUT_OF_SCOPE":
        return {
            "classification": "OUT_OF_SCOPE",
            "reason": reason,
            "job_key": job_key,
            "valid_for_full_MTS_claim": False,
        }
    root = complex(row["root"])
    fraction = float(row["residue_contour_fraction"])
    radius = float(row["outer_radius"])
    if (
        abs(root) <= 1.0e-10
        or fraction <= 0.0
        or radius <= 0.0
        or not math.isfinite(radius / fraction)
    ):
        return {
            "classification": "OUT_OF_SCOPE",
            "reason": "invalid_relative_root_or_contour",
            "job_key": job_key,
            "valid_for_full_MTS_claim": False,
        }
    chamber_index = configured_chamber_index(event, argument, ownership)
    record = {
        "scope": f"on_demand_{scope.lower()}_direct_component_resolution",
        "job_key": job_key,
        "event": event,
        "argument": argument,
        "chamber_index": chamber_index,
        "pairs": [list(pair) for pair in row["pairs"]],
        "root": {"real": root.real, "imaginary": root.imag},
        "safe_scale": radius / fraction,
        "source_numeric_probe": {
            "outer_residue": str(row["outer_residue"]),
            "inner_residue": str(row["inner_residue"]),
            "residue_stability": float(row["residue_stability"]),
            "numerically_zero": bool(row["numerically_zero"]),
            "stable": bool(row["stable"]),
        },
    }
    relative_fractions = (
        (0.1, 0.05)
        if scope == "CROSS_ADDITIVE"
        else (0.2, 0.1, 0.05)
    )
    previous_dps = mp.mp.dps
    try:
        mp.mp.dps = DPS
        result = M5112.evaluate_record(
            record,
            relative_nodes=RELATIVE_NODES,
            global_nodes=GLOBAL_NODES,
            relative_fractions=relative_fractions,
            global_fractions=GLOBAL_FRACTIONS,
        )
    finally:
        mp.mp.dps = previous_dps
    result["fallback_contract"] = {
        "scope": scope,
        "scope_reason": reason,
        "dps": DPS,
        "relative_nodes": RELATIVE_NODES,
        "global_nodes": GLOBAL_NODES,
        "relative_fractions": list(relative_fractions),
        "global_fractions": list(GLOBAL_FRACTIONS),
        "source_component": "direct_only",
        "unresolved_action": "fail_closed",
    }
    return result


def source_row() -> tuple[dict[str, Any], dict[str, bool], dict[str, Any], dict[str, Any]]:
    job = json.loads(JOB.read_text(encoding="utf-8"))
    kernel = json.loads(KERNEL.read_text(encoding="utf-8"))
    if job["status"] != "COMPLETED_UNCONVERGED":
        raise RuntimeError("5115 source job is no longer unconverged")
    adjustments = [
        row
        for row in job["profile_audit"]["residue_radius_adjustments"]
        if not bool(row["selected_stable"])
    ]
    if len(adjustments) != 1:
        raise RuntimeError("5115 requires one unresolved source row")
    wanted_root = complex(
        float(adjustments[0]["root"]["real"]),
        float(adjustments[0]["root"]["imaginary"]),
    )
    event = kernel["event"]
    argument = kernel["argument"]
    target = complex(
        float(argument["target_cosine"]["real"]),
        float(argument["target_cosine"]["imaginary"]),
    )
    M5112.M5040.M5034.configure(event, target)
    ownerships = M5112.N5030.physical_chambers()[1]
    matches = []
    for chamber_index, chamber in enumerate(kernel["fixed_event_integral_gate"]["chambers"]):
        for row in chamber["residue_catalog"]:
            if abs(complex(row["root"]) - wanted_root) < 1.0e-8 * max(1.0, abs(wanted_root)):
                matches.append((row, ownerships[chamber_index]))
    if len(matches) != 1:
        raise RuntimeError(f"5115 source root matched {len(matches)} catalog rows")
    return matches[0][0], matches[0][1], event, argument


def main() -> None:
    row, ownership, event, argument = source_row()
    resolved = resolve_unstable_record(row, ownership, JOB_KEY, event, argument)
    parent = json.loads(PARENT_CLASSIFIER_GATE.read_text(encoding="utf-8"))
    formal_hash = M5112.tree_digest(FORMAL)
    checks = [
        ("formalization_workbench_unchanged", formal_hash == FORMAL_BASELINE, formal_hash),
        (
            "same_source_scope_selected",
            resolved["fallback_contract"]["scope"]
            == "SAME_SOURCE_OPPOSITE_OWNERSHIP",
            resolved["fallback_contract"]["scope"],
        ),
        (
            "same_source_residue_is_stable_nonzero",
            resolved["classification"] == "STABLE_DIRECT_COMPONENT_NONZERO",
            str(resolved["mean"]),
        ),
        (
            "same_source_spread_passes",
            resolved["maximum_spread"]
            / max(abs(complex(resolved["mean"]["real"], resolved["mean"]["imaginary"])), 1.0e-300)
            < M5112.NONZERO_RELATIVE_SPREAD_TOLERANCE,
            str(resolved["maximum_spread"]),
        ),
        (
            "parent_classifier_passed",
            bool(parent["passed"] and parent["on_demand_classifier_authorized"]),
            parent["checkpoint_marker"],
        ),
    ]
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(("check", "passed", "detail"))
        for name, passed, detail in checks:
            writer.writerow((name, str(bool(passed)).lower(), detail))
    AUDIT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with AUDIT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(("job_key", "pairs", "chamber_index", "mean_real", "mean_imaginary", "relative_spread", "classification"))
        mean = complex(resolved["mean"]["real"], resolved["mean"]["imaginary"])
        writer.writerow(
            (
                JOB_KEY,
                json.dumps(resolved["pairs"], separators=(",", ":")),
                resolved["chamber_index"],
                mean.real,
                mean.imag,
                resolved["maximum_spread"] / abs(mean),
                resolved["classification"],
            )
        )
    passed = all(check[1] for check in checks)
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "source_job": str(JOB.resolve()),
        "source_job_sha256": digest(JOB),
        "source_kernel": str(KERNEL.resolve()),
        "source_kernel_sha256": digest(KERNEL),
        "resolved_record": resolved,
        "parent_classifier_gate": str(PARENT_CLASSIFIER_GATE.resolve()),
        "parent_classifier_gate_sha256": digest(PARENT_CLASSIFIER_GATE),
        "general_on_demand_classifier_authorized": passed,
        "cross_additive_scope_authorized": passed,
        "same_source_opposite_ownership_scope_authorized": passed,
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
                "mean": resolved["mean"],
                "maximum_spread": resolved["maximum_spread"],
                "general_on_demand_classifier_authorized": passed,
                "passed": passed,
            },
            indent=2,
        )
    )
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
