from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
from typing import Any, Callable

import numpy as np


POST = Path(__file__).resolve().parents[1]
SCRIPT_5077 = POST / "scripts" / "Y5_R2FR_5077_central_anchor_pilot_runner.py"
PRECEDENT_5037 = POST / "source-intake" / "functional_rg" / "5037" / "repairs" / "finite_endpoint_sector_v1" / "repair_summary.json"
PILOT_V4 = POST / "source-intake" / "functional_rg" / "5079" / "runs" / "bounded_central_anchor_pilot_v4"
SOURCE = POST / "source-intake" / "functional_rg" / "5085"
RESULT_JSON = SOURCE / "same_source_global_collision_removable_extension.json"
GATE_JSON = SOURCE / "A11_primary24_extension_gate.json"
VALIDATION_CSV = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5085_VALIDATION.csv"
MARKER = "MTS_5085_SAME_SOURCE_GLOBAL_COLLISION_REMOVABLE_EXTENSION"
REVISION = "guarded-multidirection-symmetric-richardson-extension-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
EVENT_ID = "S507603_N0000"
ARGUMENT_ID = "E040_A11"
CHAMBER_INDEX = 1
COLLISION_LABELS = ("direct:g2:plus_u", "direct:g2:plus_v")
LEVELS = (3.125e-5, 1.5625e-5, 7.8125e-6)
DIRECTIONS = (1.0 + 0.0j, 0.0 + 1.0j, complex(np.exp(0.37j)))
ALLOWED_SUFFIX_PAIRS = {
    frozenset(("plus_u", "plus_v")),
    frozenset(("minus_u", "minus_v")),
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


def ownership_digest(ownership: dict[str, bool]) -> str:
    payload = json.dumps(ownership, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def labels_from_error(error: RuntimeError) -> tuple[str, ...]:
    prefix = "relative chamber crossed an unsectorized global collision: "
    text = str(error)
    if not text.startswith(prefix):
        return ()
    return tuple(value.strip() for value in text[len(prefix) :].split(","))


def source(label: str) -> str:
    return label.rsplit(":", 1)[0]


def suffix(label: str) -> str:
    return label.rsplit(":", 1)[1]


def eligible_collision(
    labels: tuple[str, ...], ownership: dict[str, bool]
) -> bool:
    return bool(
        len(labels) == 2
        and source(labels[0]) == source(labels[1])
        and source(labels[0]) in {"direct:g1", "direct:g2"}
        and frozenset(suffix(label) for label in labels)
        in ALLOWED_SUFFIX_PAIRS
        and bool(ownership[labels[0]]) != bool(ownership[labels[1]])
    )


def symmetric_richardson_extension(
    relative_circle: complex,
    ownership: dict[str, bool],
    global_nodes: int,
    global_residue_nodes: int,
    original: Callable[[complex, dict[str, bool], int, int], complex],
    labels: tuple[str, ...],
) -> tuple[complex, dict[str, Any]]:
    if not eligible_collision(labels, ownership):
        raise RuntimeError(f"same-source collision is outside 5085 scope: {labels}")
    scale = max(abs(relative_circle), 1.0e-6)
    direction_rows = []
    limits = []
    for direction in DIRECTIONS:
        level_rows = []
        averages = []
        for fraction in LEVELS:
            offset = fraction * scale * direction
            minus = original(
                relative_circle - offset,
                ownership,
                global_nodes,
                global_residue_nodes,
            )
            plus = original(
                relative_circle + offset,
                ownership,
                global_nodes,
                global_residue_nodes,
            )
            average = (minus + plus) / 2.0
            averages.append(average)
            level_rows.append(
                {
                    "fraction": fraction,
                    "minus": serialized(minus),
                    "plus": serialized(plus),
                    "symmetric_average": serialized(average),
                    "side_difference": float(abs(minus - plus)),
                }
            )
        limit = (4.0 * averages[-1] - averages[-2]) / 3.0
        convergence = abs(averages[-1] - averages[-2]) / max(
            1.0, abs(limit)
        )
        limits.append(limit)
        direction_rows.append(
            {
                "direction": serialized(direction),
                "levels": level_rows,
                "richardson_limit": serialized(limit),
                "finest_average_relative_change": float(convergence),
            }
        )
    mean_limit = sum(limits) / len(limits)
    direction_spread = max(abs(value - mean_limit) for value in limits) / max(
        1.0, abs(mean_limit)
    )
    maximum_convergence = max(
        row["finest_average_relative_change"] for row in direction_rows
    )
    accepted = bool(
        maximum_convergence < 1.0e-7
        and direction_spread < 1.0e-7
        and math.isfinite(mean_limit.real)
        and math.isfinite(mean_limit.imag)
    )
    audit = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "relative_circle": serialized(relative_circle),
        "labels": list(labels),
        "ownership_digest": ownership_digest(ownership),
        "global_nodes": global_nodes,
        "global_residue_nodes": global_residue_nodes,
        "directions": direction_rows,
        "returned_limit": serialized(mean_limit),
        "maximum_directional_convergence_residual": maximum_convergence,
        "direction_independence_relative_spread": float(direction_spread),
        "accepted": accepted,
        "valid_for_full_MTS_claim": False,
    }
    if not accepted:
        raise RuntimeError(
            "5085 removable extension did not converge: "
            f"convergence={maximum_convergence}, direction_spread={direction_spread}"
        )
    return mean_limit, audit


class CertifiedRemovableGlobalExtension:
    def __init__(
        self,
        original: Callable[[complex, dict[str, bool], int, int], complex],
    ) -> None:
        self.original = original
        self.calls: list[dict[str, Any]] = []
        self.cache: dict[tuple[Any, ...], complex] = {}

    def __call__(
        self,
        relative_circle: complex,
        ownership: dict[str, bool],
        global_nodes: int,
        global_residue_nodes: int,
    ) -> complex:
        try:
            return self.original(
                relative_circle,
                ownership,
                global_nodes,
                global_residue_nodes,
            )
        except RuntimeError as error:
            labels = labels_from_error(error)
            if not eligible_collision(labels, ownership):
                raise
            key = (
                round(relative_circle.real, 11),
                round(relative_circle.imag, 11),
                tuple(sorted(labels)),
                ownership_digest(ownership),
                int(global_nodes),
                int(global_residue_nodes),
            )
            if key in self.cache:
                return self.cache[key]
            value, audit = symmetric_richardson_extension(
                relative_circle,
                ownership,
                global_nodes,
                global_residue_nodes,
                self.original,
                labels,
            )
            audit["original_error"] = str(error)
            self.calls.append(audit)
            self.cache[key] = value
            return value


def collision_identity_audit(module: Any, root: complex) -> dict[str, Any]:
    soft_direction, decay_direction, internal = module.M5028.event_geometry(
        module.SOFT_ENERGY,
        complex(module.SOFT_COSINE, 0.0),
        complex(module.DECAY_COSINE, 0.0),
        root,
    )
    direction = module.M5028.source_directions(
        internal, soft_direction, decay_direction
    )["direct:g2"]
    roots = module.M5028.M5024.all_factor_roots(
        direction, module.TARGET_COSINE
    )
    plus_u = complex(roots["plus_u"])
    plus_v = complex(roots["plus_v"])
    root_residual = abs(plus_u - plus_v) / max(1.0, abs(plus_u), abs(plus_v))
    direction_cosine_residual = abs(
        complex(direction[2]) - module.TARGET_COSINE
    )
    return {
        "direct_g2_plus_u_root": serialized(plus_u),
        "direct_g2_plus_v_root": serialized(plus_v),
        "global_root_collision_relative_residual": float(root_residual),
        "direction_cosine_minus_target": serialized(
            complex(direction[2]) - module.TARGET_COSINE
        ),
        "direction_cosine_collision_residual": float(direction_cosine_residual),
        "algebraic_identity": (
            "plus_u=plus_v iff e^2=h*hbar; for a null direction "
            "h*hbar=(1-n_z)/(1+n_z) and e^2=(1-z)/(1+z), hence n_z=z"
        ),
        "passed": root_residual < 2.0e-10
        and direction_cosine_residual < 2.0e-8,
    }


def main() -> None:
    required = [
        SCRIPT_5077,
        PRECEDENT_5037,
        PILOT_V4 / "config.json",
        PILOT_V4 / "topologies" / f"{EVENT_ID}__{ARGUMENT_ID}.json",
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing 5085 inputs: {missing}")
    M5077 = load_module("mts_5077_for_5085_main", SCRIPT_5077)
    config = json.loads((PILOT_V4 / "config.json").read_text(encoding="utf-8"))
    event = M5077.M5036.event_lookup(config)[EVENT_ID]
    argument = M5077.M5036.argument_lookup(config)[ARGUMENT_ID]
    target = M5077.M5036.complex_from_row(argument["target_cosine"])
    M5077.M5036.M5035.M5034.configure(event, target)
    module = M5077.M5036.N5030
    ownership = module.physical_chambers()[1][CHAMBER_INDEX]
    rationals = module.M5029.root_rationals(
        module.SOFT_ENERGY,
        module.SOFT_COSINE,
        module.DECAY_COSINE,
        module.TARGET_COSINE,
    )
    roots = module.M5029.collision_roots(
        rationals[COLLISION_LABELS[0]], rationals[COLLISION_LABELS[1]]
    )
    root = min(roots, key=abs)
    identity = collision_identity_audit(module, root)
    node_rows = []
    for nodes in (24, 32, 48):
        value, audit = symmetric_richardson_extension(
            root,
            ownership,
            nodes,
            nodes,
            module.global_chamber_value,
            COLLISION_LABELS,
        )
        node_rows.append(
            {
                "nodes": nodes,
                "value": serialized(value),
                "audit": audit,
            }
        )
    node_values = [
        complex(row["value"]["real"], row["value"]["imaginary"])
        for row in node_rows
    ]
    node_mean = sum(node_values) / len(node_values)
    node_spread = max(abs(value - node_mean) for value in node_values) / max(
        1.0, abs(node_mean)
    )
    topology = json.loads(
        (PILOT_V4 / "topologies" / f"{EVENT_ID}__{ARGUMENT_ID}.json").read_text(
            encoding="utf-8"
        )
    )
    profile = config["tiers"]["primary24"]
    extension = CertifiedRemovableGlobalExtension(module.global_chamber_value)
    previous_global = module.global_chamber_value
    previous_catalog = module.chamber_residue_catalog
    module.global_chamber_value = extension
    module.chamber_residue_catalog = M5077.certified_primary_catalog
    M5077.M5036.MREPAIR.CURRENT_JOB = "5085::A11_primary24"
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
        module.global_chamber_value = previous_global
        module.chamber_residue_catalog = previous_catalog
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
        "extension_call_count": len(extension.calls),
        "extension_calls": extension.calls,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(GATE_JSON, gate_result)
    precedent = json.loads(PRECEDENT_5037.read_text(encoding="utf-8"))
    accepted = bool(
        identity["passed"]
        and all(row["audit"]["accepted"] for row in node_rows)
        and node_spread < 1.0e-7
        and precedent["accepted"]
        and precedent["promoted"]
        and gate_result["converged"]
        and gate_result["extension_call_count"] > 0
    )
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "event_id": EVENT_ID,
        "argument_id": ARGUMENT_ID,
        "chamber_index": CHAMBER_INDEX,
        "collision_labels": list(COLLISION_LABELS),
        "relative_collision_root": serialized(root),
        "opposite_ownership": bool(ownership[COLLISION_LABELS[0]])
        != bool(ownership[COLLISION_LABELS[1]]),
        "collision_identity_audit": identity,
        "node_ladder": node_rows,
        "node_ladder_mean": serialized(node_mean),
        "node_ladder_relative_spread": float(node_spread),
        "removable_limit": serialized(node_mean),
        "precedent_5037": {
            "path": str(PRECEDENT_5037),
            "sha256": digest(PRECEDENT_5037),
            "accepted": precedent["accepted"],
            "promoted": precedent["promoted"],
            "same_source_examples": [
                "direct:g1:minus_u, direct:g1:minus_v"
            ],
        },
        "failed_A11_gate_recomputed": str(GATE_JSON),
        "failed_A11_gate_recomputed_sha256": digest(GATE_JSON),
        "failed_A11_gate_converged": gate_result["converged"],
        "extension_call_count": gate_result["extension_call_count"],
        "extension_scope": (
            "only opposite-ownership plus_u/plus_v or minus_u/minus_v "
            "coalescences of direct:g1/direct:g2; every call must pass "
            "multidirection symmetric-limit convergence"
        ),
        "same_source_collision_removable_extension_accepted": accepted,
        "pilot_resume_authorized_under_dynamic_guard": accepted,
        "formalization_workbench_tree_sha256": FORMAL_BASELINE,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    checks = [
        ("source_paths_exist", not missing, "all extension inputs exist"),
        ("collision_identity", identity["passed"], identity["algebraic_identity"]),
        ("opposite_ownership", result["opposite_ownership"], str(COLLISION_LABELS)),
        ("directional_limits", all(row["audit"]["accepted"] for row in node_rows), "all 24/32/48-node limits pass"),
        ("node_independence", node_spread < 1.0e-7, f"spread={node_spread}"),
        ("precedent_retained", precedent["accepted"] and precedent["promoted"], "5037 removable-sector extension remains accepted"),
        ("failed_job_recomputed", gate_result["converged"] and gate_result["extension_call_count"] > 0, f"calls={gate_result['extension_call_count']}"),
        ("extension_accepted", accepted, result["extension_scope"]),
        ("formalization_unchanged", result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE, result["formalization_workbench_tree_sha256"]),
        ("claim_discipline", not result["valid_for_full_MTS_claim"], "integration extension is not physical evidence"),
    ]
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("check_id", "passed", "detail", "checkpoint_marker"))
        writer.writeheader()
        for index, (name, passed, detail) in enumerate(checks, start=1):
            writer.writerow(
                {
                    "check_id": f"V5085_{index:02d}_{name}",
                    "passed": passed,
                    "detail": detail,
                    "checkpoint_marker": MARKER,
                }
            )
    failed = [name for name, passed, _ in checks if not passed]
    if failed:
        raise RuntimeError(f"checkpoint 5085 validation failed: {failed}")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
