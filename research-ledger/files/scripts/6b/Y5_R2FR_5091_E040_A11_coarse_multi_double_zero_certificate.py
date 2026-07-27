from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import os
from pathlib import Path
from typing import Any, Callable


POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMAL = ROOT / "formalization-workbench"
SCRIPT_5077 = POST / "scripts" / "Y5_R2FR_5077_central_anchor_pilot_runner.py"
SCRIPT_5088 = POST / "scripts" / "Y5_R2FR_5088_exact_same_source_double_zero_collision_certificate.py"
PILOT_V7 = POST / "source-intake" / "functional_rg" / "5079" / "runs" / "bounded_central_anchor_pilot_v7"
SOURCE = POST / "source-intake" / "functional_rg" / "5091"
RESULT_JSON = SOURCE / "E040_A11_coarse_multi_double_zero_certificate.json"
GATE_JSON = SOURCE / "E040_A11_coarse12_exact_collision_gate.json"
VALIDATION_CSV = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5091_VALIDATION.csv"
MARKER = "MTS_5091_E040_A11_COARSE_MULTI_DOUBLE_ZERO_CERTIFICATE"
REVISION = "multi-root-local-double-zero-and-zero-owned-residue-extension-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
EVENT_ID = "S507603_N0000"
ARGUMENT_ID = "E040_A11"
JOB_KEY = "E040__S507603_N0000__A11__coarse12"
PROFILE = "coarse12"
RESIDUE_FRACTIONS = (2.0e-4, 1.0e-4, 5.0e-5)
RESIDUE_NODES = (192, 384)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5077: Any = None
M5088: Any = None


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        value.update(item.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(item).encode("ascii"))
    return value.hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


class CertifiedMultiDoubleZeroGlobalExtension:
    def __init__(
        self,
        numerical_module: Any,
        original: Callable[[complex, dict[str, bool], int, int], complex],
        module_5085: Any,
        module_5088: Any,
        relative_roots: tuple[complex, ...],
        certified_ownership_digests: set[str],
        certificate_passed: bool,
    ) -> None:
        self.numerical_module = numerical_module
        self.original = original
        self.module_5085 = module_5085
        self.module_5088 = module_5088
        self.relative_roots = relative_roots
        self.certified_ownership_digests = certified_ownership_digests
        self.certificate_passed = certificate_passed
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
                relative_circle, ownership, global_nodes, global_residue_nodes
            )
        except RuntimeError as error:
            labels = self.module_5085.labels_from_error(error)
            if set(labels) != set(self.module_5088.COLLISION_LABELS):
                raise
            if not self.certificate_passed:
                raise
            root_index, relative_root = min(
                enumerate(self.relative_roots),
                key=lambda row: abs(relative_circle - row[1]),
            )
            relative_distance = abs(relative_circle - relative_root) / max(
                1.0, abs(relative_root)
            )
            if relative_distance >= 5.0e-9:
                raise
            current_ownership_digest = self.module_5088.ownership_digest(ownership)
            if current_ownership_digest not in self.certified_ownership_digests:
                raise
            key = (
                root_index,
                round(relative_circle.real, 11),
                round(relative_circle.imag, 11),
                int(global_nodes),
                int(global_residue_nodes),
                current_ownership_digest,
            )
            if key in self.cache:
                return self.cache[key]
            value, audit = self.module_5088.silent_pair_global_cycle(
                self.numerical_module,
                relative_circle,
                ownership,
                global_nodes,
                global_residue_nodes,
                labels,
            )
            audit.update(
                {
                    "checkpoint_marker": MARKER,
                    "revision": REVISION,
                    "certified_root_index": root_index,
                    "certified_relative_root": self.module_5088.serialized(relative_root),
                    "distance_from_certified_relative_root": float(relative_distance),
                    "ownership_digest": current_ownership_digest,
                    "original_error": str(error),
                    "valid_for_full_MTS_claim": False,
                }
            )
            self.calls.append(audit)
            self.cache[key] = value
            return value


def configured_problem() -> tuple[dict[str, Any], dict[str, Any], Any, dict[str, Any]]:
    config = json.loads((PILOT_V7 / "config.json").read_text(encoding="utf-8"))
    event = M5077.M5036.event_lookup(config)[EVENT_ID]
    argument = M5077.M5036.argument_lookup(config)[ARGUMENT_ID]
    target = M5077.M5036.complex_from_row(argument["target_cosine"])
    M5077.M5043.M5034.configure(event, target)
    topology = json.loads(
        (PILOT_V7 / "topologies" / f"{EVENT_ID}__{ARGUMENT_ID}.json").read_text(
            encoding="utf-8"
        )
    )
    return config, topology, M5077.M5043.N5030, argument


def exact_root_certificates(module: Any) -> list[dict[str, Any]]:
    rationals = module.M5029.root_rationals(
        module.SOFT_ENERGY,
        module.SOFT_COSINE,
        module.DECAY_COSINE,
        module.TARGET_COSINE,
    )
    roots = sorted(
        module.M5029.collision_roots(
            rationals[M5088.COLLISION_LABELS[0]],
            rationals[M5088.COLLISION_LABELS[1]],
        ),
        key=abs,
    )
    _, ownerships = module.physical_chambers()
    opposite = [
        ownership
        for ownership in ownerships
        if bool(ownership[M5088.COLLISION_LABELS[0]])
        != bool(ownership[M5088.COLLISION_LABELS[1]])
    ]
    M5088.RESIDUE_FRACTIONS = RESIDUE_FRACTIONS
    M5088.RESIDUE_NODES = RESIDUE_NODES
    rows = []
    for index, relative_root in enumerate(roots):
        plus_u_derivative = M5088.rational_derivative(
            rationals[M5088.COLLISION_LABELS[0]], relative_root
        )
        plus_v_derivative = M5088.rational_derivative(
            rationals[M5088.COLLISION_LABELS[1]], relative_root
        )
        split_derivative = plus_u_derivative - plus_v_derivative
        geometry = M5088.collision_geometry(module, relative_root)
        collision_residual = abs(geometry["plus_u"] - geometry["plus_v"]) / max(
            1.0, abs(geometry["collision_root"])
        )
        direction_residual = abs(
            complex(geometry["directions"]["direct:g2"][2]) - module.TARGET_COSINE
        )
        cauchy = M5088.cauchy_double_zero_audit(module, relative_root)
        residue_audits = {}
        for label in M5088.COLLISION_LABELS:
            representative = next(
                ownership for ownership in opposite if bool(ownership[label])
            )
            residue_audits[label] = M5088.selected_residue_linear_audit(
                module, relative_root, representative, split_derivative
            )
        passed = bool(
            collision_residual < 2.0e-10
            and direction_residual < 2.0e-8
            and abs(split_derivative) > 1.0e-6
            and cauchy["passed"]
            and all(audit["passed"] for audit in residue_audits.values())
        )
        rows.append(
            {
                "root_index": index,
                "relative_collision_root": M5088.serialized(relative_root),
                "global_collision_root": M5088.serialized(geometry["collision_root"]),
                "global_collision_relative_residual": float(collision_residual),
                "direction_cosine_collision_residual": float(direction_residual),
                "root_split_derivative": M5088.serialized(split_derivative),
                "root_split_derivative_magnitude": float(abs(split_derivative)),
                "cauchy_double_zero_audit": cauchy,
                "owned_residue_linear_audits": residue_audits,
                "certificate_passed": passed,
            }
        )
    return rows


def main() -> None:
    global M5077, M5088
    M5077 = load_module("mts_5077_for_5091", SCRIPT_5077)
    M5088 = load_module("mts_5088_for_5091", SCRIPT_5088)
    topology_path = PILOT_V7 / "topologies" / f"{EVENT_ID}__{ARGUMENT_ID}.json"
    failed_job_path = PILOT_V7 / "jobs" / f"{JOB_KEY}.json"
    required = [SCRIPT_5077, SCRIPT_5088, PILOT_V7 / "config.json", topology_path, failed_job_path, FORMAL]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing 5091 inputs: {missing}")
    config, topology, module, argument = configured_problem()
    root_rows = exact_root_certificates(module)
    relative_roots = tuple(
        M5077.M5036.complex_from_row(row["relative_collision_root"])
        for row in root_rows
    )
    _, ownerships = module.physical_chambers()
    certified_ownership_digests = {
        M5088.ownership_digest(ownership)
        for ownership in ownerships
        if bool(ownership[M5088.COLLISION_LABELS[0]])
        != bool(ownership[M5088.COLLISION_LABELS[1]])
    }
    certificate_passed = bool(
        len(root_rows) == 2 and all(row["certificate_passed"] for row in root_rows)
    )
    previous_catalog = module.chamber_residue_catalog
    previous_global = module.global_chamber_value
    exact_extension = CertifiedMultiDoubleZeroGlobalExtension(
        module,
        previous_global,
        M5077.M5085,
        M5088,
        relative_roots,
        certified_ownership_digests,
        certificate_passed,
    )
    removable_extension = M5077.M5085.CertifiedRemovableGlobalExtension(
        exact_extension
    )
    module.chamber_residue_catalog = M5077.restricted_coarse_catalog
    module.global_chamber_value = removable_extension
    M5077.M5043.CURRENT_JOB = f"5091::{JOB_KEY}"
    M5077.M5043.THEOREM_AUDIT.clear()
    M5077.M5043.CHART_AUDIT.clear()
    M5077.M5043.NUMERIC_AUDIT.clear()
    M5077.LOCAL_ZERO_AUDIT.clear()
    M5077.OUTWARD_CONTOUR_AUDIT.clear()
    profile = M5077.M5043.PROFILES[PROFILE]
    gate = None
    gate_error = None
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
    except Exception as error:
        gate_error = f"{type(error).__name__}: {error}"
    finally:
        module.chamber_residue_catalog = previous_catalog
        module.global_chamber_value = previous_global
    gate_converged = bool(gate and gate["fixed_event_crossed_integral_converged"])
    gate_residues_stable = bool(gate and gate["all_residues_stable"])
    roots_used = sorted(
        set(call["certified_root_index"] for call in exact_extension.calls)
    )
    gate_result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "job_key": JOB_KEY,
        "converged": gate_converged,
        "all_residues_stable": gate_residues_stable,
        "highest_two_order_relative_residual": float(
            gate["highest_two_order_relative_residual"]
        ) if gate else None,
        "highest_order_value": gate["highest_order_value"] if gate else None,
        "gate_error": gate_error,
        "exact_extension_call_count": len(exact_extension.calls),
        "exact_extension_calls": exact_extension.calls,
        "certified_root_indexes_used": roots_used,
        "numerical_removable_extension_call_count": len(removable_extension.calls),
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(GATE_JSON, gate_result)
    failed_job = json.loads(failed_job_path.read_text(encoding="utf-8"))
    formal_digest = tree_digest(FORMAL)
    gate_accepted = bool(
        certificate_passed
        and gate_converged
        and gate_residues_stable
        and gate_error is None
        and len(exact_extension.calls) > 0
        and len(removable_extension.calls) == 0
    )
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "event_id": EVENT_ID,
        "argument_id": ARGUMENT_ID,
        "job_key": JOB_KEY,
        "profile": PROFILE,
        "target_cosine": argument["target_cosine"],
        "collision_labels": list(M5088.COLLISION_LABELS),
        "residue_fractions": list(RESIDUE_FRACTIONS),
        "residue_nodes": list(RESIDUE_NODES),
        "certified_physical_ownership_digests": sorted(certified_ownership_digests),
        "root_certificates": root_rows,
        "all_exact_collision_roots_certified": certificate_passed,
        "failed_job_before_repair": failed_job,
        "gate_path": str(GATE_JSON),
        "gate_sha256": digest(GATE_JSON),
        "exact_collision_gate_accepted": gate_accepted,
        "runner_integration_authorized": gate_accepted,
        "decision": "ACCEPT_MULTI_ROOT_ZERO_OWNED_RESIDUE_EXTENSION" if gate_accepted else "REJECT_MULTI_ROOT_EXTENSION",
        "derived_local_lemma": {
            "definition": "For each exact q_j, G=I/w and H_j=(w-u)(w-v)G",
            "conclusion": "At both algebraic collision roots H_j has a double zero and either uniquely owned residue is C_j(q-q_j)+O((q-q_j)^2), so its exact collision limit is zero",
            "principal_value_or_half_residue_inserted": False,
        },
        "numerical_limit_threshold_relaxed": False,
        "pilot_result_claimed": False,
        "formalization_workbench_tree_sha256": formal_digest,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    checks = [
        ("source_paths_exist", not missing, "all 5091 inputs exist"),
        ("old_failure_targeted", failed_job["status"] == "FAILED" and "5085 removable extension did not converge" in failed_job["error"], failed_job["error"]),
        ("two_algebraic_roots", len(root_rows) == 2, str(len(root_rows))),
        ("root_collisions_exact", all(row["global_collision_relative_residual"] < 2.0e-10 for row in root_rows), str([row["global_collision_relative_residual"] for row in root_rows])),
        ("double_zero_cauchy", all(row["cauchy_double_zero_audit"]["passed"] for row in root_rows), "both regularized numerators have double zeros"),
        ("owned_residues_linear", all(all(audit["passed"] for audit in row["owned_residue_linear_audits"].values()) for row in root_rows), "both ownerships at both roots tend linearly to zero"),
        ("gate_converged", gate_converged, str(gate_result["highest_two_order_relative_residual"])),
        ("gate_residues_stable", gate_residues_stable, str(gate_residues_stable)),
        ("exact_guard_exercised", len(exact_extension.calls) > 0, str(len(exact_extension.calls))),
        ("numeric_fallback_unused", len(removable_extension.calls) == 0, str(len(removable_extension.calls))),
        ("no_tolerance_relaxation", not result["numerical_limit_threshold_relaxed"], str(RESIDUE_FRACTIONS)),
        ("formalization_unchanged", formal_digest == FORMAL_BASELINE, formal_digest),
        ("claim_discipline", not result["valid_for_full_MTS_claim"], "row-local numerical theorem only"),
    ]
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("check_id", "passed", "detail", "checkpoint_marker"))
        writer.writeheader()
        for index, (name, passed, detail) in enumerate(checks, start=1):
            writer.writerow({"check_id": f"V5091_{index:02d}_{name}", "passed": passed, "detail": detail, "checkpoint_marker": MARKER})
    failed = [name for name, passed, _ in checks if not passed]
    if failed:
        raise RuntimeError(f"checkpoint 5091 validation failed: {failed}")


if __name__ == "__main__":
    main()
