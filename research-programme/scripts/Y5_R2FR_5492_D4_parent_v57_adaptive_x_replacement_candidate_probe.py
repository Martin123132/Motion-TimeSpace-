from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
OUTPUT = FUNCTIONAL_RG / "5492"
WORK = OUTPUT / "work-v1"

SCRIPT_5467 = SCRIPTS / "Y5_R2FR_5467_D4_all_outer_leaf_epsilon_fiber_transplant_runner.py"
SCRIPT_5468 = SCRIPTS / "Y5_R2FR_5468_D4_exact_outer_cuboid_coalescence_runner.py"
SCRIPT_5469 = SCRIPTS / "Y5_R2FR_5469_D4_resumable_three_axis_cuboid_certificate_runner.py"
SCRIPT_5472 = SCRIPTS / "Y5_R2FR_5472_D4_parent_v52_collision_jacobian_leaf_union_integration_gate.py"
SCRIPT_5474 = SCRIPTS / "Y5_R2FR_5474_D4_parent_v53_stable_edge_t_leaf_union_integration_gate.py"
SCRIPT_5476 = SCRIPTS / "Y5_R2FR_5476_D4_parent_v54_first_spinor_pivot_t_leaf_union_integration_gate.py"
SCRIPT_5478 = SCRIPTS / "Y5_R2FR_5478_D4_parent_v55_stable_edge_xt_leaf_union_integration_gate.py"
SCRIPT_5480 = SCRIPTS / "Y5_R2FR_5480_D4_parent_v55_hash_locked_frontier_runner.py"
SCRIPT_5483 = SCRIPTS / "Y5_R2FR_5483_D4_parent_v56_collision_jacobian_xt_leaf_union_integration_gate.py"
SCRIPT_5490 = SCRIPTS / "Y5_R2FR_5490_D4_parent_v57_collision_jacobian_epsilon_xt_leaf_union_candidate_probe.py"
SCRIPT_5491 = SCRIPTS / "Y5_R2FR_5491_D4_parent_v57_collision_jacobian_zero_leaf_dependency_probe.py"

MANIFEST_5468 = FUNCTIONAL_RG / "5468" / "D4_exact_outer_cuboid_manifest.csv"
STATE_5484 = (
    FUNCTIONAL_RG
    / "5484"
    / "work-v1"
    / "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b.json"
)
RESULT_5491 = FUNCTIONAL_RG / "5491" / "D4_parent_v57_collision_jacobian_zero_leaf_dependency_result.json"
VALIDATION_5491 = FUNCTIONAL_RG / "5491" / "P8_Y5_BRR5490_5491_VALIDATION.csv"

WORK_STATE = WORK / "adaptive_x_replacement_state.json"
LEAF_AUDIT = OUTPUT / "D4_parent_v57_adaptive_x_replacement_leaf_audit.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5491_5492_VALIDATION.csv"
STATUS = OUTPUT / "status.json"
RESULT = OUTPUT / "D4_parent_v57_adaptive_x_replacement_candidate_result.json"
DOCUMENT = POST / "5492-Y5-R2FR-D4-parent-v57-adaptive-x-replacement-candidate-probe.md"

CHECKPOINT = 5492
REVISION = "D4-parent-v57-adaptive-x-replacement-candidate-probe-v1"
PARENT_V56_REVISION = "D4-deformed-contour-regular-away-W3-v56-collision-jacobian-xt-leaf-union"
PARENT_V57_PROBE_REVISION = "D4-deformed-contour-regular-away-W3-v57-adaptive-x-replacement-candidate"
TARGET_CUBOID_ID = "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b"
TARGET_REFINEMENT_PATH = "R_E0S_E0S_E0S_E1S"
EXPECTED_STATE_SHA256 = "3f485d18bb2a55d3fda317091e58c0330166a7b5ae7e2185a82ab46602e23faa"
EXPECTED_FAILURE_MARKER = "global contour geometric denominator reaches zero"
EPSILON_COUNT = 16
X_COUNT = 16
T_COUNT = 128
ZERO_LEAF_X_CHILD_COUNT = 2


class AdaptiveCandidateProbeComplete(RuntimeError):
    pass


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def truth(value: Any) -> bool:
    return value is True or str(value).strip().lower() == "true"


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def source_paths() -> tuple[Path, ...]:
    return (
        Path(__file__).resolve(),
        SCRIPT_5467,
        SCRIPT_5468,
        SCRIPT_5469,
        SCRIPT_5472,
        SCRIPT_5474,
        SCRIPT_5476,
        SCRIPT_5478,
        SCRIPT_5480,
        SCRIPT_5483,
        SCRIPT_5490,
        SCRIPT_5491,
        MANIFEST_5468,
        STATE_5484,
        RESULT_5491,
        VALIDATION_5491,
    )


def check(gate: str, passed: bool, evidence: Any) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "validation_gate": gate,
        "passed": bool(passed),
        "evidence": evidence,
    }


def atomic_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(
        json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=True),
        encoding="utf-8",
    )
    os.replace(temporary, path)


def bounds(parent: Any, value: Any) -> tuple[float, float, float, float]:
    real_lower, real_upper = parent.M5394.real_bounds(value)
    imaginary_lower, imaginary_upper = parent.M5394.imaginary_bounds(value)
    return real_lower, real_upper, imaginary_lower, imaginary_upper


def evaluate_record(
    parent: Any,
    base_5491: Any,
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    box: dict[str, float],
) -> dict[str, Any]:
    lower, denominator, method, jacobian, _ = base_5491.evaluate_box(
        parent,
        configuration,
        cell,
        path_segment,
        box,
    )
    real_lower, real_upper, imaginary_lower, imaginary_upper = bounds(
        parent,
        jacobian,
    )
    return {
        "lower": lower,
        "denominator_lower": denominator,
        "method": method,
        "jacobian_real_lower": real_lower,
        "jacobian_real_upper": real_upper,
        "jacobian_imaginary_lower": imaginary_lower,
        "jacobian_imaginary_upper": imaginary_upper,
    }


def box_volume(box: dict[str, float]) -> float:
    return (
        (box["epsilon_real_upper"] - box["epsilon_real_lower"])
        * (box["x_upper"] - box["x_lower"])
        * (box["t_upper"] - box["t_lower"])
    )


def full_bounds(
    parent: Any,
    inputs: dict[str, Any],
    path_context: dict[str, Any],
) -> dict[str, float]:
    epsilon_real_lower, epsilon_real_upper = parent.M5394.real_bounds(
        inputs["epsilon"]
    )
    epsilon_imaginary_lower, epsilon_imaginary_upper = (
        parent.M5394.imaginary_bounds(inputs["epsilon"])
    )
    x_lower, x_upper = parent.M5394.real_bounds(
        path_context["absolute_coordinate"]
    )
    t_lower, t_upper = parent.M5394.real_bounds(path_context["path_parameter"])
    return {
        "epsilon_real_lower": epsilon_real_lower,
        "epsilon_real_upper": epsilon_real_upper,
        "epsilon_imaginary_lower": epsilon_imaginary_lower,
        "epsilon_imaginary_upper": epsilon_imaginary_upper,
        "x_lower": x_lower,
        "x_upper": x_upper,
        "t_lower": t_lower,
        "t_upper": t_upper,
    }


def base_leaf_box(
    domain: dict[str, float],
    epsilon_index: int,
    x_index: int,
    t_index: int,
) -> dict[str, float]:
    return {
        "epsilon_real_lower": domain["epsilon_real_lower"]
        + (domain["epsilon_real_upper"] - domain["epsilon_real_lower"])
        * epsilon_index
        / EPSILON_COUNT,
        "epsilon_real_upper": domain["epsilon_real_lower"]
        + (domain["epsilon_real_upper"] - domain["epsilon_real_lower"])
        * (epsilon_index + 1)
        / EPSILON_COUNT,
        "epsilon_imaginary_lower": domain["epsilon_imaginary_lower"],
        "epsilon_imaginary_upper": domain["epsilon_imaginary_upper"],
        "x_lower": domain["x_lower"]
        + (domain["x_upper"] - domain["x_lower"]) * x_index / X_COUNT,
        "x_upper": domain["x_lower"]
        + (domain["x_upper"] - domain["x_lower"]) * (x_index + 1) / X_COUNT,
        "t_lower": domain["t_lower"]
        + (domain["t_upper"] - domain["t_lower"]) * t_index / T_COUNT,
        "t_upper": domain["t_lower"]
        + (domain["t_upper"] - domain["t_lower"]) * (t_index + 1) / T_COUNT,
    }


def x_child_box(box: dict[str, float], child_index: int) -> dict[str, float]:
    child = dict(box)
    child["x_lower"] = box["x_lower"] + (
        box["x_upper"] - box["x_lower"]
    ) * child_index / ZERO_LEAF_X_CHILD_COUNT
    child["x_upper"] = box["x_lower"] + (
        box["x_upper"] - box["x_lower"]
    ) * (child_index + 1) / ZERO_LEAF_X_CHILD_COUNT
    return child


def initial_work_state(
    domain: dict[str, float],
    configuration_role: str,
) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "source_state_sha256": EXPECTED_STATE_SHA256,
        "target_refinement_path": TARGET_REFINEMENT_PATH,
        "configuration_role": configuration_role,
        "epsilon_count": EPSILON_COUNT,
        "x_count": X_COUNT,
        "t_count": T_COUNT,
        "zero_leaf_x_child_count": ZERO_LEAF_X_CHILD_COUNT,
        "domain": domain,
        "next_epsilon_index": 0,
        "rows": [],
        "complete": False,
        "last_update_utc": datetime.now(timezone.utc).isoformat(),
    }


def verify_work_state(
    state: dict[str, Any],
    domain: dict[str, float],
    configuration_role: str,
) -> None:
    expected = {
        "source_state_sha256": EXPECTED_STATE_SHA256,
        "target_refinement_path": TARGET_REFINEMENT_PATH,
        "configuration_role": configuration_role,
        "epsilon_count": EPSILON_COUNT,
        "x_count": X_COUNT,
        "t_count": T_COUNT,
        "zero_leaf_x_child_count": ZERO_LEAF_X_CHILD_COUNT,
        "domain": domain,
    }
    for key, value in expected.items():
        if state.get(key) != value:
            raise RuntimeError(f"checkpoint-5492 work state mismatch at {key}")
    expected_rows = int(state["next_epsilon_index"]) * X_COUNT * T_COUNT
    if len(state["rows"]) != expected_rows:
        raise RuntimeError(
            "checkpoint-5492 work state row count does not match committed slices"
        )


def leaf_row(
    parent: Any,
    base_5491: Any,
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    domain: dict[str, float],
    epsilon_index: int,
    x_index: int,
    t_index: int,
) -> dict[str, Any]:
    box = base_leaf_box(domain, epsilon_index, x_index, t_index)
    base = evaluate_record(
        parent,
        base_5491,
        configuration,
        cell,
        path_segment,
        box,
    )
    row: dict[str, Any] = {
        "epsilon_index": epsilon_index,
        "x_index": x_index,
        "t_index": t_index,
        **box,
        "base_volume": box_volume(box),
        "base_lower": base["lower"],
        "base_denominator_lower": base["denominator_lower"],
        "base_method": base["method"],
        "base_jacobian_real_lower": base["jacobian_real_lower"],
        "base_jacobian_real_upper": base["jacobian_real_upper"],
        "base_jacobian_imaginary_lower": base["jacobian_imaginary_lower"],
        "base_jacobian_imaginary_upper": base["jacobian_imaginary_upper"],
        "resolution": "BASE_PASS" if base["lower"] > 0.0 else "X2_REPLACEMENT",
        "child0_lower": math.nan,
        "child0_denominator_lower": math.nan,
        "child0_method": "",
        "child0_jacobian_real_lower": math.nan,
        "child0_jacobian_real_upper": math.nan,
        "child0_jacobian_imaginary_lower": math.nan,
        "child0_jacobian_imaginary_upper": math.nan,
        "child1_lower": math.nan,
        "child1_denominator_lower": math.nan,
        "child1_method": "",
        "child1_jacobian_real_lower": math.nan,
        "child1_jacobian_real_upper": math.nan,
        "child1_jacobian_imaginary_lower": math.nan,
        "child1_jacobian_imaginary_upper": math.nan,
        "final_lower": base["lower"],
        "final_denominator_lower": base["denominator_lower"],
        "accepted_volume": box_volume(box),
        "status": "PASS" if base["lower"] > 0.0 else "ZERO",
    }
    if base["lower"] > 0.0:
        return row
    children: list[dict[str, Any]] = []
    child_volumes: list[float] = []
    for child_index in range(ZERO_LEAF_X_CHILD_COUNT):
        child_box = x_child_box(box, child_index)
        children.append(
            evaluate_record(
                parent,
                base_5491,
                configuration,
                cell,
                path_segment,
                child_box,
            )
        )
        child_volumes.append(box_volume(child_box))
    for child_index, child in enumerate(children):
        prefix = f"child{child_index}"
        row[f"{prefix}_lower"] = child["lower"]
        row[f"{prefix}_denominator_lower"] = child["denominator_lower"]
        row[f"{prefix}_method"] = child["method"]
        row[f"{prefix}_jacobian_real_lower"] = child["jacobian_real_lower"]
        row[f"{prefix}_jacobian_real_upper"] = child["jacobian_real_upper"]
        row[f"{prefix}_jacobian_imaginary_lower"] = child[
            "jacobian_imaginary_lower"
        ]
        row[f"{prefix}_jacobian_imaginary_upper"] = child[
            "jacobian_imaginary_upper"
        ]
    row["final_lower"] = min(child["lower"] for child in children)
    row["final_denominator_lower"] = min(
        child["denominator_lower"] for child in children
    )
    row["accepted_volume"] = math.fsum(child_volumes)
    row["status"] = "PASS" if row["final_lower"] > 0.0 else "ZERO"
    return row


def adaptive_candidate(
    parent: Any,
    base_5491: Any,
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    inputs: dict[str, Any],
    path_context: dict[str, Any],
    maximum_epsilon_slices: int,
) -> dict[str, Any]:
    domain = full_bounds(parent, inputs, path_context)
    configuration_role = str(configuration.get("role", ""))
    WORK.mkdir(parents=True, exist_ok=True)
    state = (
        read_json(WORK_STATE)
        if WORK_STATE.is_file()
        else initial_work_state(domain, configuration_role)
    )
    verify_work_state(state, domain, configuration_role)
    first_epsilon_index = int(state["next_epsilon_index"])
    final_epsilon_index = min(
        EPSILON_COUNT,
        first_epsilon_index + maximum_epsilon_slices,
    )
    started = time.perf_counter()
    for epsilon_index in range(first_epsilon_index, final_epsilon_index):
        slab_rows: list[dict[str, Any]] = []
        for x_index in range(X_COUNT):
            for t_index in range(T_COUNT):
                slab_rows.append(
                    leaf_row(
                        parent,
                        base_5491,
                        configuration,
                        cell,
                        path_segment,
                        domain,
                        epsilon_index,
                        x_index,
                        t_index,
                    )
                )
        state["rows"].extend(slab_rows)
        state["next_epsilon_index"] = epsilon_index + 1
        state["complete"] = state["next_epsilon_index"] == EPSILON_COUNT
        state["last_update_utc"] = datetime.now(timezone.utc).isoformat()
        state["last_run_seconds"] = time.perf_counter() - started
        atomic_json(WORK_STATE, state)
    rows = list(state["rows"])
    original_volume = box_volume(domain)
    covered_volume = math.fsum(float(row["accepted_volume"]) for row in rows)
    complete = bool(state["complete"])
    candidate_positive = complete and rows and all(
        float(row["final_lower"]) > 0.0
        and float(row["final_denominator_lower"]) > 0.0
        for row in rows
    )
    zero_rows = [row for row in rows if float(row["base_lower"]) <= 0.0]
    unresolved_rows = [row for row in rows if float(row["final_lower"]) <= 0.0]
    final_intervals: list[tuple[float, float, float, float]] = []
    for row in rows:
        if row["resolution"] == "BASE_PASS":
            final_intervals.append(
                (
                    float(row["base_jacobian_real_lower"]),
                    float(row["base_jacobian_real_upper"]),
                    float(row["base_jacobian_imaginary_lower"]),
                    float(row["base_jacobian_imaginary_upper"]),
                )
            )
        else:
            for child_index in range(ZERO_LEAF_X_CHILD_COUNT):
                prefix = f"child{child_index}"
                final_intervals.append(
                    (
                        float(row[f"{prefix}_jacobian_real_lower"]),
                        float(row[f"{prefix}_jacobian_real_upper"]),
                        float(row[f"{prefix}_jacobian_imaginary_lower"]),
                        float(row[f"{prefix}_jacobian_imaginary_upper"]),
                    )
                )
    if final_intervals:
        hull = parent.cbox(
            min(interval[0] for interval in final_intervals),
            max(interval[1] for interval in final_intervals),
            min(interval[2] for interval in final_intervals),
            max(interval[3] for interval in final_intervals),
        )
        hull_lower = parent.M5258.lower_abs(hull)
    else:
        hull_lower = 0.0
    return {
        "state": state,
        "rows": rows,
        "complete": complete,
        "candidate_positive": candidate_positive,
        "base_leaf_count": len(rows),
        "expected_base_leaf_count": EPSILON_COUNT * X_COUNT * T_COUNT,
        "base_positive_leaf_count": len(rows) - len(zero_rows),
        "base_zero_leaf_count": len(zero_rows),
        "replacement_child_count": len(zero_rows) * ZERO_LEAF_X_CHILD_COUNT,
        "unresolved_replacement_leaf_count": len(unresolved_rows),
        "final_leaf_count": len(rows)
        - len(zero_rows)
        + len(zero_rows) * ZERO_LEAF_X_CHILD_COUNT,
        "leaf_union_abs_lower": (
            min(float(row["final_lower"]) for row in rows) if rows else 0.0
        ),
        "minimum_chart_denominator_abs_lower": (
            min(float(row["final_denominator_lower"]) for row in rows)
            if rows
            else 0.0
        ),
        "rectangular_hull_abs_lower": hull_lower,
        "original_parameter_volume": original_volume,
        "covered_parameter_volume": covered_volume,
        "parameter_volume_coverage_error": (
            abs(covered_volume - original_volume) if complete else math.nan
        ),
        "processed_epsilon_slices_this_run": final_epsilon_index
        - first_epsilon_index,
        "runtime_seconds": time.perf_counter() - started,
    }


def install_candidate_probe(
    parent: Any,
    base_5491: Any,
    maximum_epsilon_slices: int,
) -> Any:
    if parent.REVISION != PARENT_V56_REVISION:
        raise RuntimeError(
            f"expected parent revision {PARENT_V56_REVISION}, found {parent.REVISION}"
        )
    original = parent.tight_energy_contour_geometric_factors
    parent.V57_ADAPTIVE_CANDIDATE = None

    def tight_probe(
        configuration: dict[str, Any],
        inputs: dict[str, Any],
        geometry: dict[str, Any],
        path_context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        factors = original(configuration, inputs, geometry, path_context)
        lower = float(
            factors.get(
                "collision_jacobian_selected_abs_lower",
                parent.M5258.lower_abs(factors["collision_jacobian"]),
            )
        )
        if (
            lower > 0.0
            or path_context is None
            or path_context.get("path_segment")
            not in {"LEFT_CONNECTOR", "RIGHT_CONNECTOR"}
        ):
            return factors
        parent.V57_ADAPTIVE_CANDIDATE = adaptive_candidate(
            parent,
            base_5491,
            configuration,
            path_context["cell"],
            path_context["path_segment"],
            inputs,
            path_context,
            maximum_epsilon_slices,
        )
        raise AdaptiveCandidateProbeComplete(
            "v57 adaptive x-replacement candidate probe complete"
        )

    parent.tight_energy_contour_geometric_factors = tight_probe
    parent.V57_PARENT_ACTION_CHANGED = False
    parent.V57_ONLY_ENCLOSURE_COMPOSITION_CANDIDATE = True
    parent.REVISION = PARENT_V57_PROBE_REVISION
    return parent


def render_document(payload: dict[str, Any], base_5467: Any) -> None:
    lines = [
        "# 5492: D4 parent-v57 adaptive x-replacement candidate probe",
        "",
        "Checkpoint 5491 proved that the first E16/X16/T128 zero leaf is an x-hull dependency: one exact x bisection closes it while epsilon-real, epsilon-imaginary and t subdivisions through 32 do not. This resumable probe applies exactly that measured operation to every and only every zero leaf of the unchanged broad target.",
        "",
        f"Complete: `{payload['candidate_cover_complete']}`. Base leaves: `{payload['base_leaf_count']}/{payload['expected_base_leaf_count']}`. Positive base leaves: `{payload['base_positive_leaf_count']}`. Replaced zero leaves: `{payload['base_zero_leaf_count']}`. Replacement children: `{payload['replacement_child_count']}`. Unresolved replacements: `{payload['unresolved_replacement_leaf_count']}`.",
        "",
        f"Adaptive leaf-union lower: `{payload['leaf_union_abs_lower']}`. Chart-denominator lower: `{payload['minimum_chart_denominator_abs_lower']}`. Rectangular-hull diagnostic lower: `{payload['rectangular_hull_abs_lower']}`. Exact parameter-volume error: `{payload['parameter_volume_coverage_error']}`.",
        "",
        f"**{payload['decision']}**",
        "",
        "This is a candidate-only finite-union proof object. It stops before parent acceptance and changes no action, contour, chart candidate, residue or threshold. A complete-amplitude target/control gate is mandatory before parent-v57 migration; all broader GR/MTS claims remain false.",
        "",
    ]
    base_5467.atomic_text(DOCUMENT, "\n".join(lines))


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--max-epsilon-slices",
        type=int,
        default=EPSILON_COUNT,
    )
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    if arguments.max_epsilon_slices < 1:
        raise ValueError("max-epsilon-slices must be positive")
    base_5467 = load_module("mts_5467_for_5492", SCRIPT_5467)
    base_5468 = load_module("mts_5468_for_5492", SCRIPT_5468)
    base_5469 = load_module("mts_5469_for_5492", SCRIPT_5469)
    base_5472 = load_module("mts_5472_for_5492", SCRIPT_5472)
    base_5474 = load_module("mts_5474_for_5492", SCRIPT_5474)
    base_5476 = load_module("mts_5476_for_5492", SCRIPT_5476)
    base_5478 = load_module("mts_5478_for_5492", SCRIPT_5478)
    base_5480 = load_module("mts_5480_for_5492", SCRIPT_5480)
    base_5483 = load_module("mts_5483_for_5492", SCRIPT_5483)
    base_5490 = load_module("mts_5490_for_5492", SCRIPT_5490)
    base_5491 = load_module("mts_5491_for_5492", SCRIPT_5491)
    base_5467.set_below_normal_priority()
    base_5480.set_single_core_affinity()
    before_formalization = base_5467.formalization_snapshot()
    missing = [str(path) for path in source_paths() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")
    state_sha256 = digest(STATE_5484)
    if state_sha256 != EXPECTED_STATE_SHA256:
        raise RuntimeError("checkpoint 5484 state differs from checkpoint-5492 lock")
    result_5491 = read_json(RESULT_5491)
    validation_5491 = read_csv(VALIDATION_5491)
    state_5484 = read_json(STATE_5484)
    cuboid = next(
        row
        for row in read_csv(MANIFEST_5468)
        if row["cuboid_job_id"] == TARGET_CUBOID_ID
    )
    candidates = [
        row
        for row in state_5484["refinement_witnesses"]
        if row.get("refinement_path") == TARGET_REFINEMENT_PATH
        and EXPECTED_FAILURE_MARKER in str(row.get("failure_message", ""))
    ]
    if len(candidates) != 1:
        raise RuntimeError(f"expected one target witness, found {len(candidates)}")
    target = candidates[0]
    stable, _, cells, support_segments, branches = base_5467.load_parent()
    parent = install_candidate_probe(
        base_5490.fresh_v56(
            base_5467,
            base_5472,
            base_5474,
            base_5476,
            base_5478,
            base_5483,
        ),
        base_5491,
        arguments.max_epsilon_slices,
    )
    probe_result = base_5469.evaluate_node(
        base_5468,
        stable,
        parent,
        cells,
        support_segments,
        branches,
        cuboid,
        target,
    )
    candidate = parent.V57_ADAPTIVE_CANDIDATE
    if candidate is None:
        raise RuntimeError("adaptive candidate probe did not trigger")
    complete = bool(candidate["complete"])
    positive = bool(candidate["candidate_positive"])
    if not complete:
        decision = "PARENT_V57_ADAPTIVE_X_REPLACEMENT_CANDIDATE_PARTIAL__RESUME"
        next_target = "RESUME_CHECKPOINT_5492_ADAPTIVE_COVER"
    elif positive:
        decision = "PARENT_V57_ADAPTIVE_X_REPLACEMENT_CANDIDATE_FOUND__BUILD_FULL_INTEGRATION_GATE"
        next_target = "BUILD_PARENT_V57_COMPLETE_AMPLITUDE_TARGET_CONTROL_GATE"
    else:
        decision = "PARENT_V57_ADAPTIVE_X_REPLACEMENT_CANDIDATE_REJECTED__DERIVE_REMAINING_ZERO_CLASS"
        next_target = "DERIVE_UNRESOLVED_REPLACEMENT_ZERO_CLASS"
    payload: dict[str, Any] = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": decision,
        "target_cuboid_id": TARGET_CUBOID_ID,
        "target_refinement_path": TARGET_REFINEMENT_PATH,
        "source_state_5484_sha256": state_sha256,
        "probe_terminated_intentionally": (
            probe_result.get("failure_type") == "AdaptiveCandidateProbeComplete"
        ),
        "candidate_cover_complete": complete,
        "candidate_positive": positive,
        "base_leaf_count": int(candidate["base_leaf_count"]),
        "expected_base_leaf_count": int(candidate["expected_base_leaf_count"]),
        "base_positive_leaf_count": int(candidate["base_positive_leaf_count"]),
        "base_zero_leaf_count": int(candidate["base_zero_leaf_count"]),
        "replacement_child_count": int(candidate["replacement_child_count"]),
        "unresolved_replacement_leaf_count": int(
            candidate["unresolved_replacement_leaf_count"]
        ),
        "final_leaf_count": int(candidate["final_leaf_count"]),
        "leaf_union_abs_lower": float(candidate["leaf_union_abs_lower"]),
        "minimum_chart_denominator_abs_lower": float(
            candidate["minimum_chart_denominator_abs_lower"]
        ),
        "rectangular_hull_abs_lower": float(
            candidate["rectangular_hull_abs_lower"]
        ),
        "original_parameter_volume": float(candidate["original_parameter_volume"]),
        "covered_parameter_volume": float(candidate["covered_parameter_volume"]),
        "parameter_volume_coverage_error": float(
            candidate["parameter_volume_coverage_error"]
        ),
        "committed_epsilon_slice_count": int(
            candidate["state"]["next_epsilon_index"]
        ),
        "processed_epsilon_slices_this_run": int(
            candidate["processed_epsilon_slices_this_run"]
        ),
        "runtime_seconds_this_run": float(candidate["runtime_seconds"]),
        "parent_action_changed": False,
        "only_enclosure_composition_candidate": True,
        "valid_for_parent_v57_adaptive_candidate": False,
        "valid_for_parent_v57_active_cuboid": False,
        "valid_for_full_outer_parent_leaf_enclosure": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "next_target": next_target,
    }
    rows = list(candidate["rows"])
    original_volume = payload["original_parameter_volume"]
    coverage_tolerance = 1.0e-12 * max(abs(original_volume), 1.0e-30)
    recomputed_lower = (
        min(float(row["final_lower"]) for row in rows) if rows else 0.0
    )
    recomputed_denominator = (
        min(float(row["final_denominator_lower"]) for row in rows)
        if rows
        else 0.0
    )
    row_indices = {
        (int(row["epsilon_index"]), int(row["x_index"]), int(row["t_index"]))
        for row in rows
    }
    expected_partial_count = payload["committed_epsilon_slice_count"] * X_COUNT * T_COUNT
    outcome_consistent = (
        (not complete and decision.endswith("PARTIAL__RESUME"))
        or (
            complete
            and positive
            and payload["unresolved_replacement_leaf_count"] == 0
            and payload["leaf_union_abs_lower"] > 0.0
        )
        or (
            complete
            and not positive
            and payload["unresolved_replacement_leaf_count"] > 0
        )
    )
    after_formalization = base_5467.formalization_snapshot()
    validations = [
        check("all_sources_exist", not missing, len(source_paths())),
        check("source_state_is_hash_locked", state_sha256 == EXPECTED_STATE_SHA256, state_sha256),
        check(
            "checkpoint_5491_x_dependency_result_is_valid",
            int(result_5491.get("failed_validation_count", -1)) == 0
            and all(truth(row["passed"]) for row in validation_5491)
            and result_5491.get("selected_single_axis") == "x"
            and int(result_5491.get("selected_single_axis_count", 0)) == 2
            and float(result_5491.get("selected_single_axis_lower", 0.0)) > 0.0,
            result_5491.get("decision"),
        ),
        check("target_witness_is_unique", len(candidates) == 1, TARGET_REFINEMENT_PATH),
        check(
            "committed_base_leaf_rows_are_complete_and_unique",
            len(rows) == expected_partial_count
            and len(row_indices) == len(rows),
            f"rows={len(rows)};expected={expected_partial_count}",
        ),
        check(
            "adaptive_cover_uses_only_the_derived_x2_replacement",
            all(
                row["resolution"] in {"BASE_PASS", "X2_REPLACEMENT"}
                and (
                    row["resolution"] == "BASE_PASS"
                    or float(row["base_lower"]) == 0.0
                )
                for row in rows
            ),
            f"zero_rows={payload['base_zero_leaf_count']}",
        ),
        check(
            "reported_minima_match_leaf_audit",
            payload["leaf_union_abs_lower"] == recomputed_lower
            and payload["minimum_chart_denominator_abs_lower"]
            == recomputed_denominator,
            f"J={recomputed_lower};chart={recomputed_denominator}",
        ),
        check(
            "complete_cover_preserves_exact_parameter_volume",
            (not complete)
            or payload["parameter_volume_coverage_error"] <= coverage_tolerance,
            payload["parameter_volume_coverage_error"],
        ),
        check("candidate_outcome_is_internally_consistent", outcome_consistent, decision),
        check(
            "candidate_probe_stops_before_parent_acceptance",
            payload["probe_terminated_intentionally"]
            and not payload["valid_for_parent_v57_adaptive_candidate"]
            and not payload["valid_for_parent_v57_active_cuboid"],
            probe_result.get("failure_type", ""),
        ),
        check(
            "parent_action_and_thresholds_are_unchanged",
            not payload["parent_action_changed"]
            and payload["only_enclosure_composition_candidate"],
            "finite-union composition only",
        ),
        check(
            "formalization_workbench_untouched",
            before_formalization == after_formalization,
            f"before={len(before_formalization)};after={len(after_formalization)}",
        ),
        check(
            "broad_claims_remain_false",
            not payload["valid_for_full_outer_parent_leaf_enclosure"]
            and not payload["valid_for_D4_event_local_W3_bound"]
            and not payload["valid_for_all_operator_local_GR_claim"]
            and not payload["valid_for_full_MTS_claim"],
            "candidate-only local enclosure",
        ),
    ]
    payload["validation_row_count"] = len(validations)
    payload["failed_validation_count"] = sum(not row["passed"] for row in validations)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    if rows:
        base_5467.atomic_csv(LEAF_AUDIT, rows)
    base_5467.atomic_csv(
        SOURCE_REGISTER,
        [
            {
                "source_path": str(path),
                "sha256": digest(path),
                "exists": path.is_file(),
            }
            for path in source_paths()
        ],
    )
    base_5467.atomic_csv(VALIDATION, validations)
    base_5467.atomic_json(STATUS, payload)
    base_5467.atomic_json(RESULT, payload)
    render_document(payload, base_5467)
    print(
        json.dumps(
            {
                key: payload[key]
                for key in (
                    "decision",
                    "candidate_cover_complete",
                    "base_leaf_count",
                    "expected_base_leaf_count",
                    "base_zero_leaf_count",
                    "replacement_child_count",
                    "unresolved_replacement_leaf_count",
                    "leaf_union_abs_lower",
                    "minimum_chart_denominator_abs_lower",
                    "parameter_volume_coverage_error",
                    "committed_epsilon_slice_count",
                    "processed_epsilon_slices_this_run",
                    "next_target",
                    "failed_validation_count",
                )
            },
            indent=2,
        )
    )
    return 0 if payload["failed_validation_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
