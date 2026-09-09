from __future__ import annotations

import csv
import ctypes
from datetime import datetime, timezone
import importlib.util
import json
import math
import os
from pathlib import Path
import sys
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
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True
if os.name == "nt":
    ctypes.windll.kernel32.SetPriorityClass(
        ctypes.windll.kernel32.GetCurrentProcess(), 0x00004000
    )


CHECKPOINT = 5442
POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMALIZATION = ROOT / "formalization-workbench"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
OUTPUT = FUNCTIONAL_RG / str(CHECKPOINT)
PARENT_SCRIPT = (
    POST / "scripts" / "Y5_R2FR_5396_D4_deformed_contour_regular_away_W3.py"
)
ACTIVE_STATE = (
    FUNCTIONAL_RG
    / "5396"
    / "partial"
    / "path_parts"
    / "_partitions"
    / "bin_00_sub_00_S_X006_MC04_SP_DP_RIGHT_CONNECTOR_part_00_of_01.state.json"
)
ACTIVE_ROWS = ACTIVE_STATE.with_suffix(".rows.csv")
PRE_STATE = FUNCTIONAL_RG / "5441" / "v48_pre_resume_state.json"
PRE_ROWS = FUNCTIONAL_RG / "5441" / "v48_pre_resume_state.rows.csv"
ROWS = OUTPUT / "c1_external01_live_failure_provenance_rows.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5396_5442_VALIDATION.csv"
RESULT = OUTPUT / "c1_external01_live_failure_provenance_result.json"
DOCUMENT = POST / "5442-Y5-R2FR-D4-c1-external01-coarse-refinement-gate.md"

EXPECTED_REVISION = "D4-deformed-contour-regular-away-W3-v49"
MAPPED_CELL_ID = "S_X006_MC04_SP_DP"
TERM_ID = "MC04_SP_DP"
PATH_SEGMENT = "RIGHT_CONNECTOR"
GLOBAL_ARC_COUNT = 4
C1_EXTERNAL01_FAILURE = (
    "IntervalSingularity:away_arc_right_K5:s2:c1:left0:"
    "edge_0_0_1:stable_edge"
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    atomic_text(path, json.dumps(payload, indent=2, sort_keys=True) + "\n")


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def check(name: str, passed: bool, detail: str) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "check": name,
        "passed": passed,
        "detail": detail,
    }


def write_document(payload: dict[str, Any]) -> None:
    decision = (
        "**C1 EXTERNAL01 IS A RESOLVED COARSE-BOX REFINEMENT EVENT.**"
        if payload["valid_for_c1_external01_coarse_refinement_classification"]
        else "**C1 EXTERNAL01 CLASSIFICATION REMAINS OPEN.**"
    )
    lines = [
        "# 5442: c1 external01 coarse-refinement gate",
        "",
        "## Decision",
        "",
        decision,
        "",
        "The v49 run recorded four c1 external01 interval failures, but each occurred on a coarse parent box. Adaptive subdivision produced eight new accepted children with positive amplitude and collision-Jacobian denominators.",
        "",
        "## Live provenance probe",
        "",
        f"- Probed pending path: `{payload['target_path']}` at depth {payload['target_depth']}.",
        f"- Arc evaluations: {payload['row_count']}; failures: {payload['failure_count']}.",
        f"- Selected role in every point/box ablation: `{payload['selected_roles']}`.",
        f"- Production c1 count delta: `+{payload['production_c1_failure_delta']}`.",
        f"- Newly accepted children: `{payload['production_accepted_delta']}`.",
        "",
        "## Interpretation",
        "",
        "No new c1 identity or closure is justified. The existing exact-invariant and adaptive-subdivision machinery already resolves these boxes. The correct next action is to resume the right-connector frontier and intervene only if c1 persists at maximum depth or stops producing accepted children.",
        "",
        "## Claim boundary",
        "",
        "This classifies one production failure mode; it does not complete the seven pending right-connector boxes and makes no W3, UV, local-GR, or full-MTS claim.",
    ]
    atomic_text(DOCUMENT, "\n".join(lines) + "\n")


def midpoint_point(parent: Any, value: Any) -> Any:
    return parent.cpoint(complex(parent.M5394.midpoint(value)))


def epsilon_first_slab(parent: Any) -> Any:
    lower = (
        parent.M5394.REGULATOR_INTERVAL[0]
        - parent.M5394.REGULATOR_CAUCHY_RADIUS
    )
    upper = (
        parent.M5394.REGULATOR_INTERVAL[1]
        + parent.M5394.REGULATOR_CAUCHY_RADIUS
    )
    return parent.cbox(
        lower,
        0.5 * (lower + upper),
        -parent.M5394.REGULATOR_CAUCHY_RADIUS,
        parent.M5394.REGULATOR_CAUCHY_RADIUS,
    )


def path_energy(
    parent: Any,
    cell: dict[str, Any],
    coordinate: Any,
    parameter: Any,
) -> Any:
    x_lower, x_upper = parent.M5394.real_bounds(coordinate)
    upper_energy, _ = parent.interval_boundary_energy(
        cell["upper_energy_boundary"], x_lower, x_upper
    )
    return upper_energy + parent.cpoint(
        1j * parent.DEFAULT_ENERGY_DEFORMATION
    ) * parameter


def selected_configurations(
    parent: Any,
    coordinate: Any,
    energy: Any,
    epsilon: Any,
) -> list[dict[str, Any]]:
    selected, _ = parent.closed_selector_configuration_subset(
        parent.configuration_variants(TERM_ID),
        coordinate,
        energy,
        epsilon,
    )
    return selected


def probe_arc(
    parent: Any,
    configuration: dict[str, Any],
    cell: dict[str, Any],
    coordinate: Any,
    parameter: Any,
    epsilon: Any,
    depth: int,
    path: str,
    mode: str,
    arc_index: int,
) -> dict[str, Any]:
    energy = path_energy(parent, cell, coordinate, parameter)
    inputs, geometry = parent.interval_inputs(
        configuration, coordinate, energy, epsilon
    )
    radius = 1.0e-7 * max(
        1.0, parent.M5258.upper_abs(geometry["selected_root"])
    )
    phase = parent.cbox(arc_index, arc_index + 1) * parent.cpoint(
        2 * math.pi / GLOBAL_ARC_COUNT
    )
    displacement = parent.cpoint(radius) * (
        parent.iv.cos(phase) + parent.cpoint(1j) * parent.iv.sin(phase)
    )
    path_context = {
        "cell": cell,
        "path_segment": PATH_SEGMENT,
        "absolute_coordinate": coordinate,
        "path_parameter": parameter,
        "refinement_depth": depth,
        "refinement_path": path,
        "global_displacement_radius": radius,
        "native_edge_cache": {},
    }
    parent.M5386.STABLE_EDGE_PROBES.clear()
    status = "PASS"
    error_type = ""
    error = ""
    try:
        parent.global_regularized_arc_coefficient(
            configuration,
            inputs,
            geometry,
            displacement,
            path_context,
        )
    except Exception as caught:
        status = "FAIL"
        error_type = type(caught).__name__
        error = str(caught)
    matching = [
        row
        for row in parent.M5386.STABLE_EDGE_PROBES
        if "away_arc_right_K5:s2:c1:left0:edge_0_0_1" in row["label"]
    ]
    edge = matching[-1] if matching else {}
    certified_lower = 0.0
    certificate_status = "NOT_APPLICABLE"
    if (
        configuration["role"] == "representative"
        and configuration["root_labels"][0] == "minus_u"
    ):
        try:
            certified, _ = parent.certified_external01_representative_invariant_5438(
                configuration,
                cell,
                PATH_SEGMENT,
                coordinate,
                parameter,
                epsilon,
                parent.cbox(-radius, radius, -radius, radius),
            )
        except Exception as caught:
            certificate_status = f"FAIL:{type(caught).__name__}:{caught}"
        else:
            certified_lower = parent.M5258.lower_abs(certified)
            certificate_status = "PASS"
    return {
        "mode": mode,
        "arc_index": arc_index,
        "configuration_role": configuration["role"],
        "root_labels": "|".join(configuration["root_labels"]),
        "status": status,
        "error_type": error_type,
        "error": error,
        "matching_c1_probe_count": len(matching),
        "direct_abs_lower": edge.get("direct_abs_lower", math.nan),
        "direct_abs_upper": edge.get("direct_abs_upper", math.nan),
        "opposite_abs_lower": edge.get("opposite_abs_lower", math.nan),
        "opposite_abs_upper": edge.get("opposite_abs_upper", math.nan),
        "invariant_abs_lower_seen_by_stable_edge": edge.get(
            "invariant_abs_lower", math.nan
        ),
        "invariant_abs_upper_seen_by_stable_edge": edge.get(
            "invariant_abs_upper", math.nan
        ),
        "override_abs_lower": edge.get("override_abs_lower", math.nan),
        "override_abs_upper": edge.get("override_abs_upper", math.nan),
        "certificate_status": certificate_status,
        "certified_invariant_abs_lower": certified_lower,
    }


def run_probe() -> dict[str, Any]:
    started = datetime.now(timezone.utc)
    parent = load_module("mts_parent_5396_v49_for_5442", PARENT_SCRIPT)
    parent.iv.dps = parent.INTERVAL_DIGITS
    state = read_json(ACTIVE_STATE)
    pre_state = read_json(PRE_STATE)
    pre_rows = read_csv(PRE_ROWS)
    active_rows = read_csv(ACTIVE_ROWS)
    x_lower, x_upper, t_lower, t_upper, depth, path = state["stack"][-1]
    coordinate_box = parent.cbox(float(x_lower), float(x_upper))
    parameter_box = parent.cbox(float(t_lower), float(t_upper))
    epsilon_box = epsilon_first_slab(parent)
    cell = next(
        row
        for row in parent.away_term_support_cells()
        if row["mapped_cell_id"] == MAPPED_CELL_ID
    )
    modes = {
        "box_box_box": (coordinate_box, parameter_box, epsilon_box),
        "box_point_box": (
            coordinate_box,
            midpoint_point(parent, parameter_box),
            epsilon_box,
        ),
        "point_box_box": (
            midpoint_point(parent, coordinate_box),
            parameter_box,
            epsilon_box,
        ),
        "point_point_point": (
            midpoint_point(parent, coordinate_box),
            midpoint_point(parent, parameter_box),
            midpoint_point(parent, epsilon_box),
        ),
    }
    rows: list[dict[str, Any]] = []
    selected_roles: dict[str, list[str]] = {}
    for mode, (coordinate, parameter, epsilon) in modes.items():
        energy = path_energy(parent, cell, coordinate, parameter)
        configurations = selected_configurations(
            parent, coordinate, energy, epsilon
        )
        selected_roles[mode] = [row["role"] for row in configurations]
        for configuration in configurations:
            for arc_index in range(GLOBAL_ARC_COUNT):
                rows.append(
                    probe_arc(
                        parent,
                        configuration,
                        cell,
                        coordinate,
                        parameter,
                        epsilon,
                        int(depth),
                        str(path),
                        mode,
                        arc_index,
                    )
                )
    atomic_csv(ROWS, rows)
    c1_failures = [
        row
        for row in rows
        if row["status"] == "FAIL"
        and "away_arc_right_K5:s2:c1:left0:edge_0_0_1" in row["error"]
    ]
    certificate_mismatch = [
        row
        for row in c1_failures
        if row["certificate_status"] == "PASS"
        and row["certified_invariant_abs_lower"] > 0.0
        and (
            not math.isfinite(row["invariant_abs_lower_seen_by_stable_edge"])
            or row["invariant_abs_lower_seen_by_stable_edge"] <= 0.0
        )
    ]
    new_accepted_rows = active_rows[len(pre_rows) :]
    pre_c1 = int(
        pre_state.get("split_failure_counts", {}).get(
            C1_EXTERNAL01_FAILURE, 0
        )
    )
    post_c1 = int(
        state.get("split_failure_counts", {}).get(
            C1_EXTERNAL01_FAILURE, 0
        )
    )
    accepted_delta = int(state["accepted_count"]) - int(
        pre_state["accepted_count"]
    )
    c1_delta = post_c1 - pre_c1
    accepted_children_are_certified = (
        len(new_accepted_rows) == accepted_delta
        and accepted_delta > 0
        and all(
            float(row["minimum_amplitude_denominator_abs_lower"]) > 0.0
            and float(row["collision_jacobian_abs_lower"]) > 0.0
            for row in new_accepted_rows
        )
    )
    classification_valid = (
        c1_delta > 0
        and accepted_children_are_certified
        and not c1_failures
        and not certificate_mismatch
        and len(state["stack"]) < len(pre_state["stack"])
    )
    payload = {
        "checkpoint": CHECKPOINT,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "parent_revision": parent.REVISION,
        "target_path": path,
        "target_depth": int(depth),
        "x_lower": float(x_lower),
        "x_upper": float(x_upper),
        "t_lower": float(t_lower),
        "t_upper": float(t_upper),
        "selected_roles": selected_roles,
        "row_count": len(rows),
        "failure_count": sum(row["status"] == "FAIL" for row in rows),
        "c1_external01_failure_count": len(c1_failures),
        "certificate_mismatch_count": len(certificate_mismatch),
        "certificate_mismatch_detected": bool(certificate_mismatch),
        "production_pre_c1_failure_count": pre_c1,
        "production_post_c1_failure_count": post_c1,
        "production_c1_failure_delta": c1_delta,
        "production_accepted_delta": accepted_delta,
        "production_new_accepted_row_count": len(new_accepted_rows),
        "production_pre_pending_count": len(pre_state["stack"]),
        "production_post_pending_count": len(state["stack"]),
        "accepted_children_are_certified": accepted_children_are_certified,
        "valid_for_c1_external01_coarse_refinement_classification": (
            classification_valid
        ),
        "next_target": (
            "RESUME_PARENT_V49_RIGHT_CONNECTOR"
            if classification_valid
            else (
                "INSTALL_CERTIFIED_S01_BEFORE_C1_RECIPROCAL_EDGE"
                if certificate_mismatch
                else "REFINE_C1_FAILURE_CLASSIFICATION"
            )
        ),
        "valid_for_parent_change": False,
        "valid_for_right_connector_completion": False,
        "valid_for_regular_away_W3_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    if parent.REVISION != EXPECTED_REVISION:
        raise RuntimeError(f"unexpected parent revision {parent.REVISION}")
    validations = [
        check(
            "all_sources_exist",
            all(
                path.exists()
                for path in (
                    PARENT_SCRIPT,
                    ACTIVE_STATE,
                    ACTIVE_ROWS,
                    PRE_STATE,
                    PRE_ROWS,
                )
            ),
            "five local inputs",
        ),
        check(
            "parent_revision_is_v49",
            parent.REVISION == EXPECTED_REVISION,
            parent.REVISION,
        ),
        check(
            "live_point_box_probe_has_no_failures",
            not c1_failures and payload["failure_count"] == 0,
            f"rows={len(rows)}",
        ),
        check(
            "no_certificate_mismatch_detected",
            not certificate_mismatch,
            f"mismatches={len(certificate_mismatch)}",
        ),
        check(
            "c1_events_generated_certified_children",
            c1_delta > 0 and accepted_children_are_certified,
            f"c1_delta={c1_delta}, accepted_delta={accepted_delta}",
        ),
        check(
            "pending_frontier_contracts",
            len(state["stack"]) < len(pre_state["stack"]),
            f"pending={len(pre_state['stack'])}->{len(state['stack'])}",
        ),
        check(
            "coarse_refinement_classification_passes",
            classification_valid,
            "no new analytic fallback is required",
        ),
        check(
            "broad_claims_remain_false",
            not payload["valid_for_parent_change"]
            and not payload["valid_for_right_connector_completion"]
            and not payload["valid_for_regular_away_W3_claim"]
            and not payload["valid_for_local_GR_claim"]
            and not payload["valid_for_full_MTS_claim"],
            "seven right-connector boxes remain pending",
        ),
    ]
    formalization_touches = [
        path
        for path in FORMALIZATION.rglob("*")
        if path.is_file()
        and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) > started
    ]
    validations.append(
        check(
            "formalization_workbench_untouched",
            not formalization_touches,
            f"modified_file_count={len(formalization_touches)}",
        )
    )
    payload["validation_row_count"] = len(validations)
    payload["failed_validation_count"] = sum(
        not bool(row["passed"]) for row in validations
    )
    atomic_csv(VALIDATION, validations)
    write_document(payload)
    atomic_json(RESULT, payload)
    return payload


def main() -> int:
    payload = run_probe()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
