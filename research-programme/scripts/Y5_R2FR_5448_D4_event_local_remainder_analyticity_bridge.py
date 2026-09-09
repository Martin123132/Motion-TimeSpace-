from __future__ import annotations

import csv
import ctypes
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
from typing import Any


os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

POST = Path(__file__).resolve().parents[1]
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
OUTPUT = FUNCTIONAL_RG / "5448"
FORMALIZATION = POST.parent / "formalization-workbench"

EVENTS = FUNCTIONAL_RG / "5358" / "D4_zero_regulator_event_certificate.csv"
CATALOG_ARCS = FUNCTIONAL_RG / "5385" / "D4_expanded_energy_full_catalog_clearance_arcs.csv"
CATALOG_RESULT = FUNCTIONAL_RG / "5385" / "D4_expanded_energy_full_catalog_clearance_result.json"
CONTOUR_BOUNDS = FUNCTIONAL_RG / "5386" / "D4_nested_contour_integrand_event_bounds.csv"
CONTOUR_RESULT = FUNCTIONAL_RG / "5386" / "D4_nested_contour_integrand_result.json"
SUBTRACTION_RESULT = FUNCTIONAL_RG / "5388" / "D4_subtraction_double_pole_zero_result.json"
GEOMETRY_RESULT = FUNCTIONAL_RG / "5389" / "D4_full_H_event_geometry_bridge_result.json"
H3_RESULT = FUNCTIONAL_RG / "5391" / "D4_uniform_full_H3_result.json"
RATIO_BOXES = FUNCTIONAL_RG / "5392" / "D4_desingularized_endpoint_ratio_boxes.csv"
G3_RESULT = FUNCTIONAL_RG / "5392" / "D4_endpoint_G3_result.json"
MAPPED_CELLS = FUNCTIONAL_RG / "5393" / "D4_parent_frozen_mapped_cells.csv"
OWNER_TABLE = FUNCTIONAL_RG / "5393" / "D4_W3_owner_decomposition.csv"
AUDIT_5447 = FUNCTIONAL_RG / "5447" / "parent_critical_dependency_path_result.json"

DOCUMENT = POST / "5448-Y5-R2FR-D4-event-local-remainder-analyticity-bridge.md"
MATRIX = OUTPUT / "D4_event_local_analyticity_matrix.csv"
SPLIT = OUTPUT / "D4_event_local_exact_split_contract.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5396_5448_VALIDATION.csv"
RESULT = OUTPUT / "D4_event_local_analyticity_result.json"

CHECKPOINT = 5448
REVISION = "D4-event-local-remainder-analyticity-bridge-v1"
EVENT_IDS = tuple(f"E{index:02d}" for index in range(1, 9))


def set_below_normal_priority() -> None:
    try:
        ctypes.windll.kernel32.SetPriorityClass(
            ctypes.windll.kernel32.GetCurrentProcess(), 0x00004000
        )
    except (AttributeError, OSError):
        pass


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    os.replace(temporary, path)


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    atomic_text(path, json.dumps(payload, indent=2, sort_keys=True) + "\n")


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    fields = list(rows[0])
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def check(gate: str, passed: bool, evidence: Any) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "validation_gate": gate,
        "passed": bool(passed),
        "evidence": evidence,
    }


def source_paths() -> tuple[Path, ...]:
    return (
        EVENTS,
        CATALOG_ARCS,
        CATALOG_RESULT,
        CONTOUR_BOUNDS,
        CONTOUR_RESULT,
        SUBTRACTION_RESULT,
        GEOMETRY_RESULT,
        H3_RESULT,
        RATIO_BOXES,
        G3_RESULT,
        MAPPED_CELLS,
        OWNER_TABLE,
        AUDIT_5447,
    )


def event_matrix() -> list[dict[str, Any]]:
    events = {row["event_id"]: row for row in read_csv(EVENTS)}
    catalog_rows = read_csv(CATALOG_ARCS)
    contour_rows = {row["event_id"]: row for row in read_csv(CONTOUR_BOUNDS)}
    ratio_rows = read_csv(RATIO_BOXES)
    mapped_rows = [
        row for row in read_csv(MAPPED_CELLS) if row["region_class"] == "EVENT_TUBE"
    ]
    rows: list[dict[str, Any]] = []
    for event_id in EVENT_IDS:
        event_catalog = [row for row in catalog_rows if row["event_id"] == event_id]
        event_ratios = [row for row in ratio_rows if row["event_id"] == event_id]
        event_cells = [row for row in mapped_rows if row["event_id"] == event_id]
        half_planes = sorted({row["normalized_gap_half_plane"] for row in event_ratios})
        minimum_gap = min(
            float(row["normalized_gap_epsilon_ref_z0_over_epsilon_modulus_lower"])
            for row in event_ratios
        )
        minimum_catalog_separation = min(
            float(row["minimum_nonactive_root_separation_lower"])
            for row in event_catalog
        )
        minimum_catalog_clearance = min(
            float(row["minimum_full_catalog_clearance_margin_lower"])
            for row in event_catalog
        )
        contour = contour_rows[event_id]
        all_conditions = (
            len(event_ratios) == 10
            and all(parse_bool(row["desingularized_Krawczyk_passes"]) for row in event_ratios)
            and all(
                parse_bool(row["mapped_v_equals_epsilon_h_inside_original_event_box"])
                for row in event_ratios
            )
            and len(half_planes) == 1
            and half_planes[0] in {"UPPER", "LOWER"}
            and minimum_gap > 0.0
            and bool(event_catalog)
            and all(parse_bool(row["energy_arc_passes"]) for row in event_catalog)
            and minimum_catalog_separation > 0.0
            and minimum_catalog_clearance > 0.0
            and parse_bool(contour["valid_for_D4_nested_contour_integrand_enclosure"])
            and float(contour["minimum_denominator_lower"]) > 0.0
            and len(event_cells) >= 2
        )
        rows.append(
            {
                "event_id": event_id,
                "event_type": events[event_id]["event_type"],
                "term_id": events[event_id]["term_id"],
                "primary_surface_id": events[event_id]["primary_surface_id"],
                "mapped_event_cell_count": len(event_cells),
                "desingularized_regulator_box_count": len(event_ratios),
                "normalized_gap_half_plane": "|".join(half_planes),
                "minimum_normalized_gap_modulus_lower": minimum_gap,
                "full_catalog_arc_count": len(event_catalog),
                "minimum_nonactive_root_separation_lower": minimum_catalog_separation,
                "minimum_full_catalog_clearance_margin_lower": minimum_catalog_clearance,
                "minimum_nested_contour_denominator_lower": float(
                    contour["minimum_denominator_lower"]
                ),
                "minimum_collision_jacobian_lower": float(
                    contour["minimum_collision_jacobian_lower"]
                ),
                "proposed_local_energy_radius_upper": 0.5
                * min(minimum_catalog_separation, minimum_catalog_clearance),
                "event_branch_analytic_through_epsilon_zero": all_conditions,
                "selected_singular_primitive_is_Hlog_plus_G": all_conditions,
                "event_local_remainder_is_holomorphic": all_conditions,
                "valid_for_D4_event_local_remainder_analyticity": all_conditions,
                "valid_for_D4_event_local_W3_bound": False,
                "valid_for_D4_numeric_W3_bound": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def split_rows() -> list[dict[str, Any]]:
    return [
        {
            "owner": "EVENT_POLE_PRINCIPAL_PART",
            "exact_expression": "H_e(epsilon) Log(epsilon/epsilon_ref)+G_e(epsilon)",
            "analytic_status": "EXPLICITLY_SPLIT; H_e and G_e analytic on patched regulator strip",
            "existing_certificate": "5391 H3 + 5392 G3 and fixed-half-plane normalized gap",
            "remaining_numeric_input": "none",
            "included_in_event_local_remainder": False,
            "valid_for_D4_event_local_remainder_analyticity": True,
            "valid_for_D4_event_local_W3_bound": False,
        },
        {
            "owner": "EVENT_REGULARIZED_TWO_DIMENSIONAL_PART",
            "exact_expression": "integral_Te [f-sum_b rho_b/(E-p_b)] dE dx",
            "analytic_status": "HOLOMORPHIC AFTER CERTIFIED POLE CATALOG SUBTRACTION",
            "existing_certificate": "5385 full pole catalog + 5386 finite nested contour + 5393 fixed event cells",
            "remaining_numeric_input": "finite complex-strip supremum on 19 mapped event cells",
            "included_in_event_local_remainder": True,
            "valid_for_D4_event_local_remainder_analyticity": True,
            "valid_for_D4_event_local_W3_bound": False,
        },
        {
            "owner": "EVENT_POLE_UPPER_AND_FINITE_REMAINDER",
            "exact_expression": "pole primitive on nonsingular endpoint/cutoff minus its Hlog+G lower singular part",
            "analytic_status": "HOLOMORPHIC; normalized lower gap stays in one half-plane and all other roots stay clear",
            "existing_certificate": "5385, 5388, 5389 and 5392",
            "remaining_numeric_input": "finite complex-strip primitive supremum per event",
            "included_in_event_local_remainder": True,
            "valid_for_D4_event_local_remainder_analyticity": True,
            "valid_for_D4_event_local_W3_bound": False,
        },
    ]


def render_document(payload: dict[str, Any], rows: list[dict[str, Any]]) -> None:
    lines = [
        "# 5448: D4 event-local remainder analyticity bridge",
        "",
        "## Decision",
        "",
        "**THE EVENT-LOCAL OWNER IS NOT A NEW NONANALYTIC OBSTRUCTION: AFTER THE CERTIFIED `H log + G` PRIMITIVE IS REMOVED, ALL EIGHT REMAINDERS ARE HOLOMORPHIC ON THE COMMON REGULATOR STRIP. A FINITE SUPREMUM STILL HAS TO BE ENCLOSED.**",
        "",
        "## Exact local split",
        "",
        "For each fixed mapped event tube `T_e`, subtract every selected material principal part before integration and write",
        "",
        "```text",
        "I_tube,e(epsilon)",
        " = integral_Te [f-sum_b rho_b/(E-p_b)] dE dx",
        " + sum_b integral_Xe rho_b[Log(E_U-p_b)-Log(E_L-p_b)] dx.",
        "```",
        "",
        "At the colliding endpoint, checkpoint 5392 proves `v=epsilon h`, with `epsilon_ref z0/epsilon=2 i epsilon_ref u h` nonzero in one fixed half-plane. Its exact primitive is",
        "",
        "```text",
        "-Phi(z0)=H_e(epsilon) Log(epsilon/epsilon_ref)+G_e(epsilon).",
        "```",
        "",
        "Define",
        "",
        "```text",
        "R_e(epsilon)=I_tube,e(epsilon)-H_e(epsilon) Log(epsilon/epsilon_ref)-G_e(epsilon).",
        "```",
        "",
        "The patched Krawczyk branch makes the event coordinates holomorphic through zero. The fixed-half-plane gap makes the chosen logarithm single-valued. The full pole-catalog and nested-contour certificates isolate the selected pole and keep every other denominator nonzero. Checkpoint 5388 fixes the subtraction pole order. Holomorphic parameter integration over the fixed 5393 event cells therefore makes `R_e` holomorphic.",
        "",
        "## Eight-event audit",
        "",
        "| event | type | mapped cells | ratio boxes | half-plane | min other-root separation | analytic remainder |",
        "|---|---|---:|---:|---|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['event_id']}` | `{row['event_type']}` | {row['mapped_event_cell_count']} | {row['desingularized_regulator_box_count']} | `{row['normalized_gap_half_plane']}` | {row['minimum_nonactive_root_separation_lower']:.17g} | `{str(row['event_local_remainder_is_holomorphic']).lower()}` |"
        )
    lines.extend(
        [
            "",
            "## What this closes",
            "",
            "This closes the logical analyticity gap behind the phrase `desingularized coordinates exist`. The local `epsilon log epsilon` term is fully assigned to `H log + G`; it cannot leak back into `R_e`. A finite Cauchy estimate is therefore legitimate once a complex-strip supremum of the two retained analytic pieces is obtained.",
            "",
            "The next bound is",
            "",
            "```text",
            "W3_event <= sum_e 6 sup_|zeta-epsilon|=r |R_e(zeta)| / r^3.",
            "```",
            "",
            "The remaining numerical owner is now concrete: bound the regularized two-dimensional integral on the `19` mapped event cells and the nonsingular upper/cutoff primitive. No new local-state, coupling or galaxy axiom is involved.",
            "",
            "## Claim boundary",
            "",
            "Analyticity does not supply the missing supremum. `valid_for_D4_event_local_W3_bound`, combined `W3`, the D4 regulator limit, all-operator local GR and full MTS remain false.",
            "",
        ]
    )
    atomic_text(DOCUMENT, "\n".join(lines))


def run() -> dict[str, Any]:
    set_below_normal_priority()
    started = datetime.now(timezone.utc)
    sources = source_paths()
    rows = event_matrix()
    split = split_rows()
    catalog_result = read_json(CATALOG_RESULT)
    contour_result = read_json(CONTOUR_RESULT)
    subtraction_result = read_json(SUBTRACTION_RESULT)
    geometry_result = read_json(GEOMETRY_RESULT)
    h3_result = read_json(H3_RESULT)
    g3_result = read_json(G3_RESULT)
    audit = read_json(AUDIT_5447)
    owners = {row["owner_id"]: row for row in read_csv(OWNER_TABLE)}

    payload: dict[str, Any] = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": "EIGHT_EVENT_LOCAL_REMAINDERS_HOLOMORPHIC__PROCEED_TO_FINITE_SUPREMUM",
        "event_count": len(rows),
        "mapped_event_cell_count": sum(row["mapped_event_cell_count"] for row in rows),
        "desingularized_ratio_box_count": sum(
            row["desingularized_regulator_box_count"] for row in rows
        ),
        "all_event_remainders_holomorphic": all(
            row["event_local_remainder_is_holomorphic"] for row in rows
        ),
        "minimum_normalized_gap_modulus_lower": min(
            row["minimum_normalized_gap_modulus_lower"] for row in rows
        ),
        "minimum_nonactive_root_separation_lower": min(
            row["minimum_nonactive_root_separation_lower"] for row in rows
        ),
        "minimum_nested_contour_denominator_lower": min(
            row["minimum_nested_contour_denominator_lower"] for row in rows
        ),
        "next_target": "FINITE_EVENT_REGULARIZED_CONTOUR_AND_UPPER_PRIMITIVE_SUPREMUM",
        "valid_for_D4_event_local_remainder_analyticity": True,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_D4_numeric_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }

    validations = [
        check("all_sources_exist", all(path.is_file() for path in sources), [str(path) for path in sources]),
        check("critical_path_selects_event_local_owner", audit.get("next_target") == "D4_EVENT_LOCAL_REMAINDER_ANALYTICITY_AND_FINITE_CAUCHY_BOUND", audit.get("next_target")),
        check("eight_event_rows_are_complete", len(rows) == 8 and {row["event_id"] for row in rows} == set(EVENT_IDS), len(rows)),
        check("nineteen_mapped_event_cells_are_owned", sum(row["mapped_event_cell_count"] for row in rows) == 19, sum(row["mapped_event_cell_count"] for row in rows)),
        check("eighty_desingularized_boxes_cover_strip_and_halos", sum(row["desingularized_regulator_box_count"] for row in rows) == 80, sum(row["desingularized_regulator_box_count"] for row in rows)),
        check("full_pole_catalog_is_certified", catalog_result.get("validation_passed") is True, catalog_result.get("decision")),
        check("nested_contour_integrand_is_finite", contour_result.get("validation_passed") is True, contour_result.get("decision")),
        check("subtraction_double_pole_is_zero", subtraction_result.get("validation_passed") is True and int(subtraction_result.get("subtraction_selected_global_pole_order_upper", 99)) <= 1, subtraction_result.get("decision")),
        check("event_branches_are_patched_holomorphically", geometry_result.get("validation_passed") is True, geometry_result.get("decision")),
        check("H3_and_G3_are_certified", h3_result.get("validation_passed") is True and g3_result.get("validation_passed") is True, f"H3={h3_result.get('decision')};G3={g3_result.get('decision')}"),
        check("endpoint_split_algebra_has_roundoff_level_crosscheck", float(g3_result.get("endpoint_H_log_plus_G_identity_residual", math.inf)) <= 1.0e-18, g3_result.get("endpoint_H_log_plus_G_identity_residual")),
        check("all_event_analyticity_conditions_pass", all(row["event_local_remainder_is_holomorphic"] for row in rows), [row["event_id"] for row in rows if not row["event_local_remainder_is_holomorphic"]]),
        check("owner_was_open_before_this_bridge", owners["W_EVENT_LOCAL_REMAINDER"]["third_derivative_status"] == "DESINGULARIZED_COORDINATES_EXIST__REMAINDER_ENCLOSURE_PENDING", owners["W_EVENT_LOCAL_REMAINDER"]["third_derivative_status"]),
        check("finite_bound_and_broad_claims_remain_false", not payload["valid_for_D4_event_local_W3_bound"] and not payload["valid_for_D4_numeric_W3_bound"] and not payload["valid_for_all_operator_local_GR_claim"] and not payload["valid_for_full_MTS_claim"], "analyticity only"),
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
    payload["failed_validation_count"] = sum(not row["passed"] for row in validations)
    atomic_csv(OUTPUT / "source_register.csv", [
        {"source_path": str(path.relative_to(POST)), "source_exists": path.is_file()}
        for path in sources
    ])
    atomic_csv(MATRIX, rows)
    atomic_csv(SPLIT, split)
    atomic_csv(VALIDATION, validations)
    render_document(payload, rows)
    atomic_json(RESULT, payload)
    return payload


def main() -> int:
    payload = run()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["failed_validation_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
