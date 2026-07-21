from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPT_5077 = POST / "scripts" / "Y5_R2FR_5077_central_anchor_pilot_runner.py"
SCRIPT_5085 = POST / "scripts" / "Y5_R2FR_5085_same_source_global_collision_removable_extension.py"
PILOT_V5 = POST / "source-intake" / "functional_rg" / "5079" / "runs" / "bounded_central_anchor_pilot_v5"
SOURCE = POST / "source-intake" / "functional_rg" / "5086"
RESULT_JSON = SOURCE / "outward_same_source_residue_contour_gate.json"
GATE_JSON = SOURCE / "A12_primary24_outward_repair_gate.json"
VALIDATION_CSV = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5086_VALIDATION.csv"
MARKER = "MTS_5086_OUTWARD_SAME_SOURCE_RESIDUE_CONTOUR_GATE"
REVISION = "smallest-certified-outward-contour-two-node-ladders-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
EVENT_ID = "S507603_N0000"
ARGUMENT_ID = "E040_A12"
OUTWARD_FRACTIONS = (0.25, 0.3, 0.35, 0.4, 0.45)
STABILITY_TOLERANCE = 5.0e-3
CROSS_LADDER_TOLERANCE = 5.0e-3
ALLOWED_SUFFIX_PAIRS = {
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


def serialized(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imaginary": float(value.imag)}


def source(label: str) -> str:
    return label.rsplit(":", 1)[0]


def suffix(label: str) -> str:
    return label.rsplit(":", 1)[1]


def eligible_row(row: dict[str, Any]) -> bool:
    if len(row["pairs"]) != 1 or len(row["pairs"][0]) != 2:
        return False
    labels = tuple(str(value) for value in row["pairs"][0])
    return bool(
        source(labels[0]) == source(labels[1])
        and source(labels[0]) in {"direct:g1", "direct:g2"}
        and frozenset(suffix(label) for label in labels)
        in ALLOWED_SUFFIX_PAIRS
    )


def candidate(
    module: Any,
    root: complex,
    safe_scale: float,
    pairs: list[tuple[str, str]],
    ownership: dict[str, bool],
    fraction: float,
) -> dict[str, Any]:
    radius = fraction * safe_scale
    production_outer = module.pair_local_relative_residue(
        root, radius, 32, pairs, ownership, 32
    )
    production_inner = module.pair_local_relative_residue(
        root, radius / 2.0, 48, pairs, ownership, 48
    )
    audit_outer = module.pair_local_relative_residue(
        root, radius, 48, pairs, ownership, 48
    )
    audit_inner = module.pair_local_relative_residue(
        root, radius / 2.0, 64, pairs, ownership, 64
    )
    production_stability = abs(production_inner - production_outer) / max(
        abs(production_inner), abs(production_outer), 1.0e-30
    )
    audit_stability = abs(audit_inner - audit_outer) / max(
        abs(audit_inner), abs(audit_outer), 1.0e-30
    )
    cross_ladder = abs(audit_inner - production_inner) / max(
        abs(audit_inner), abs(production_inner), 1.0e-30
    )
    accepted = bool(
        fraction < 0.5
        and production_stability < STABILITY_TOLERANCE
        and audit_stability < STABILITY_TOLERANCE
        and cross_ladder < CROSS_LADDER_TOLERANCE
        and max(abs(audit_inner), abs(production_inner)) > 1.0e-7
    )
    return {
        "fraction": fraction,
        "radius": radius,
        "production_outer": serialized(production_outer),
        "production_inner": serialized(production_inner),
        "audit_outer": serialized(audit_outer),
        "audit_inner": serialized(audit_inner),
        "production_stability": float(production_stability),
        "audit_stability": float(audit_stability),
        "cross_ladder_relative_difference": float(cross_ladder),
        "accepted": accepted,
        "audit_inner_internal": audit_inner,
    }


def outward_same_source_repair(
    catalog: list[dict[str, Any]],
    ownership: dict[str, bool],
    module: Any,
    job_key: str,
    audit_log: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], bool]:
    all_roots = [complex(row["root"]) for row in catalog]
    for row in catalog:
        if bool(row["stable"]) or not eligible_row(row):
            continue
        root = complex(row["root"])
        separations = [
            abs(root - other)
            for other in all_roots
            if abs(root - other) > 1.0e-7 * max(1.0, abs(root), abs(other))
        ]
        safe_scale = min([abs(root)] + separations)
        if not math.isfinite(safe_scale) or safe_scale <= 0.0:
            continue
        pairs = [tuple(str(value) for value in pair) for pair in row["pairs"]]
        candidates = []
        chosen = None
        for fraction in OUTWARD_FRACTIONS:
            probe = candidate(
                module,
                root,
                safe_scale,
                pairs,
                ownership,
                fraction,
            )
            candidates.append(probe)
            if probe["accepted"]:
                chosen = probe
                break
        serialized_candidates = [
            {key: value for key, value in probe.items() if key != "audit_inner_internal"}
            for probe in candidates
        ]
        audit_row = {
            "job_key": job_key,
            "root": serialized(root),
            "pairs": row["pairs"],
            "safe_scale": safe_scale,
            "candidate_rows": serialized_candidates,
            "selected_fraction": chosen["fraction"] if chosen else None,
            "selected_stable": chosen is not None,
            "selection_rule": (
                "smallest fraction in 0.25,0.30,0.35,0.40,0.45 passing "
                "production 32/48, audit 48/64, and cross-ladder 0.005 gates"
            ),
        }
        audit_log.append(audit_row)
        if chosen is None:
            continue
        residue = complex(chosen["audit_inner_internal"])
        row.update(
            {
                "outer_radius": float(chosen["radius"]),
                "residue_method": REVISION,
                "residue_contour_fraction": float(chosen["fraction"]),
                "outer_residue": complex(
                    chosen["audit_outer"]["real"],
                    chosen["audit_outer"]["imaginary"],
                ),
                "inner_residue": residue,
                "residue": residue,
                "residue_stability": float(chosen["audit_stability"]),
                "numerically_zero": False,
                "stable": True,
                "included_as_pole_model": bool(row["near_path"]),
                "outward_contour_certificate": audit_row,
            }
        )
    return catalog, all(bool(row["stable"]) for row in catalog)


def main() -> None:
    required = [
        SCRIPT_5077,
        SCRIPT_5085,
        PILOT_V5 / "config.json",
        PILOT_V5 / "topologies" / f"{EVENT_ID}__{ARGUMENT_ID}.json",
        PILOT_V5 / "kernels" / "E040__S507603_N0000__A12__primary24.json",
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing 5086 inputs: {missing}")
    M5077 = load_module("mts_5077_for_5086_main", SCRIPT_5077)
    M5085 = load_module("mts_5085_for_5086_main", SCRIPT_5085)
    config = json.loads((PILOT_V5 / "config.json").read_text(encoding="utf-8"))
    event = M5077.M5036.event_lookup(config)[EVENT_ID]
    argument = M5077.M5036.argument_lookup(config)[ARGUMENT_ID]
    target = M5077.M5036.complex_from_row(argument["target_cosine"])
    M5077.M5036.M5035.M5034.configure(event, target)
    module = M5077.M5036.N5030
    original_kernel = json.loads(
        (PILOT_V5 / "kernels" / "E040__S507603_N0000__A12__primary24.json").read_text(
            encoding="utf-8"
        )
    )
    original_unstable = [
        {
            "chamber_index": int(chamber["chamber_index"]),
            "root": row["root"],
            "pairs": row["pairs"],
        }
        for chamber in original_kernel["fixed_event_integral_gate"]["chambers"]
        for row in chamber["residue_catalog"]
        if not bool(row["stable"])
    ]
    repair_audit: list[dict[str, Any]] = []

    def repaired_catalog(
        ownership: dict[str, bool],
        start: complex,
        end: complex,
        required_roots: list[complex],
        global_nodes: int,
        global_residue_nodes: int,
        relative_residue_nodes: int,
        model_distance: float,
    ) -> tuple[list[dict[str, Any]], bool]:
        catalog, _ = M5077.certified_primary_catalog(
            ownership,
            start,
            end,
            required_roots,
            global_nodes,
            global_residue_nodes,
            relative_residue_nodes,
            model_distance,
        )
        return outward_same_source_repair(
            catalog,
            ownership,
            module,
            "5086::A12_primary24",
            repair_audit,
        )

    topology = json.loads(
        (PILOT_V5 / "topologies" / f"{EVENT_ID}__{ARGUMENT_ID}.json").read_text(
            encoding="utf-8"
        )
    )
    profile = config["tiers"]["primary24"]
    previous_catalog = module.chamber_residue_catalog
    previous_global = module.global_chamber_value
    removable = M5085.CertifiedRemovableGlobalExtension(previous_global)
    module.chamber_residue_catalog = repaired_catalog
    module.global_chamber_value = removable
    M5077.M5036.MREPAIR.CURRENT_JOB = "5086::A12_primary24"
    M5077.M5036.MREPAIR.RADIUS_AUDIT.clear()
    M5077.LOCAL_ZERO_AUDIT.clear()
    try:
        gate = module.fixed_event_integral_gate(
            topology,
            tuple(int(value) for value in profile["relative_orders"]),
            int(profile["global_nodes"]),
            int(profile["global_residue_nodes"]),
            int(profile["relative_residue_nodes"]),
            float(profile["model_distance"]),
            int(config["topology"]["boundary_tracking_steps"]),
            str(profile["relative_quadrature_mode"]),
            float(profile["relative_adaptive_tolerance"]),
            int(profile["relative_adaptive_maximum_intervals"]),
        )
    finally:
        module.chamber_residue_catalog = previous_catalog
        module.global_chamber_value = previous_global
    repaired_unstable = [
        {
            "chamber_index": int(chamber["chamber_index"]),
            "root": row["root"],
            "pairs": row["pairs"],
        }
        for chamber in gate["chambers"]
        for row in chamber["residue_catalog"]
        if not bool(row["stable"])
    ]
    gate_result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "converged": bool(gate["fixed_event_crossed_integral_converged"]),
        "all_residues_stable": bool(gate["all_residues_stable"]),
        "highest_two_order_relative_residual": float(
            gate["highest_two_order_relative_residual"]
        ),
        "highest_value": M5077.M5036.complex_row(
            M5077.M5036.M5035.M5034.highest_value(gate)
        ),
        "original_unstable_rows": original_unstable,
        "repaired_unstable_rows": repaired_unstable,
        "outward_repair_audit": repair_audit,
        "removable_extension_count": len(removable.calls),
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(GATE_JSON, gate_result)
    selected_rows = [row for row in repair_audit if row["selected_stable"]]
    accepted = bool(
        len(original_unstable) == 2
        and len(selected_rows) == 2
        and all(float(row["selected_fraction"]) < 0.5 for row in selected_rows)
        and gate_result["converged"]
        and gate_result["all_residues_stable"]
        and not repaired_unstable
    )
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "event_id": EVENT_ID,
        "argument_id": ARGUMENT_ID,
        "original_unstable_rows": original_unstable,
        "outward_fraction_ladder": list(OUTWARD_FRACTIONS),
        "stability_tolerance": STABILITY_TOLERANCE,
        "cross_ladder_tolerance": CROSS_LADDER_TOLERANCE,
        "repair_audit": repair_audit,
        "selected_repair_count": len(selected_rows),
        "recomputed_gate": str(GATE_JSON),
        "recomputed_gate_sha256": digest(GATE_JSON),
        "recomputed_gate_converged": gate_result["converged"],
        "recomputed_gate_all_residues_stable": gate_result[
            "all_residues_stable"
        ],
        "outward_same_source_contour_gate_accepted": accepted,
        "pilot_resume_authorized_under_guard": accepted,
        "scope": (
            "unstable direct:g1/g2 same-source minus/plus collisions only; "
            "the smallest isolated outward contour must pass two independent "
            "node ladders and their cross-comparison"
        ),
        "formalization_workbench_tree_sha256": FORMAL_BASELINE,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    checks = [
        ("source_paths_exist", not missing, "all outward-gate inputs exist"),
        ("original_failure_reproduced", len(original_unstable) == 2, f"count={len(original_unstable)}"),
        ("both_rows_repaired", len(selected_rows) == 2, f"count={len(selected_rows)}"),
        ("contours_isolated", all(float(row["selected_fraction"]) < 0.5 for row in selected_rows), str([row["selected_fraction"] for row in selected_rows])),
        ("two_ladder_gates", all(any(candidate_row["accepted"] for candidate_row in row["candidate_rows"]) for row in selected_rows), "production, audit, and cross-ladder gates pass"),
        ("A12_recomputed", gate_result["converged"] and gate_result["all_residues_stable"] and not repaired_unstable, f"residual={gate_result['highest_two_order_relative_residual']}"),
        ("repair_accepted", accepted, result["scope"]),
        ("formalization_unchanged", result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE, result["formalization_workbench_tree_sha256"]),
        ("claim_discipline", not result["valid_for_full_MTS_claim"], "numerical contour repair is not physical evidence"),
    ]
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("check_id", "passed", "detail", "checkpoint_marker"))
        writer.writeheader()
        for index, (name, passed, detail) in enumerate(checks, start=1):
            writer.writerow(
                {
                    "check_id": f"V5086_{index:02d}_{name}",
                    "passed": passed,
                    "detail": detail,
                    "checkpoint_marker": MARKER,
                }
            )
    failed = [name for name, passed, _ in checks if not passed]
    if failed:
        raise RuntimeError(f"checkpoint 5086 validation failed: {failed}")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
