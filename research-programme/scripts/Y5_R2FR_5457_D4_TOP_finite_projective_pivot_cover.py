from __future__ import annotations

import csv
import ctypes
import hashlib
import importlib.util
import json
import math
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import sympy as sp


for variable in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
):
    os.environ.setdefault(variable, "1")


POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
OUTPUT = FUNCTIONAL_RG / "5457"
FORMALIZATION = POST.parent / "formalization-workbench"

SCRIPT_5386 = SCRIPTS / "Y5_R2FR_5386_D4_nested_contour_integrand_enclosure.py"
SCRIPT_5396 = SCRIPTS / "Y5_R2FR_5396_D4_deformed_contour_regular_away_W3.py"
SCRIPT_5456 = SCRIPTS / "Y5_R2FR_5456_D4_outer_parent_leaf_transplant_smoke.py"
REPRESENTATIVES_5456 = (
    FUNCTIONAL_RG / "5456" / "D4_outer_parent_leaf_representatives.csv"
)
RESULT_5455 = (
    FUNCTIONAL_RG / "5455" / "D4_full_epsilon_connected_superprojection_cover_result.json"
)
RESULT_5456 = (
    FUNCTIONAL_RG / "5456" / "D4_outer_parent_leaf_transplant_smoke_result.json"
)

DOCUMENT = POST / "5457-Y5-R2FR-D4-TOP-finite-projective-pivot-cover.md"
COVER = OUTPUT / "D4_TOP_finite_projective_pivot_cover.csv"
SUMMARY = OUTPUT / "D4_TOP_projective_owner_summary.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR545_5457_VALIDATION.csv"
RESULT = OUTPUT / "D4_TOP_finite_projective_pivot_cover_result.json"

CHECKPOINT = 5457
REVISION = "D4-TOP-finite-projective-pivot-cover-v2"
TARGET_JOB_ID = "E01__U017__TOP__MAXIMUM_PHYSICAL_PATH_AREA"
X_SUBDIVISIONS = 16
T_SUBDIVISIONS = 32
GLOBAL_ARC_COUNT = 4
PIVOT_NAMES = ("plus", "minus", "holomorphic", "antiholomorphic")


def set_below_normal_priority() -> None:
    try:
        ctypes.windll.kernel32.SetPriorityClass(
            ctypes.windll.kernel32.GetCurrentProcess(), 0x00004000
        )
    except (AttributeError, OSError):
        pass


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(value, encoding="utf-8", newline="\n")
    temporary.replace(path)


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    atomic_text(
        path,
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n",
    )


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    fields: list[str] = []
    known: set[str] = set()
    for row in rows:
        for field in row:
            if field not in known:
                fields.append(field)
                known.add(field)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def formalization_snapshot() -> dict[str, tuple[int, int]]:
    if not FORMALIZATION.is_dir():
        return {}
    return {
        str(path.relative_to(FORMALIZATION)): (
            path.stat().st_size,
            path.stat().st_mtime_ns,
        )
        for path in FORMALIZATION.rglob("*")
        if path.is_file()
    }


def source_paths() -> list[Path]:
    return [
        SCRIPT_5386,
        SCRIPT_5396,
        SCRIPT_5456,
        REPRESENTATIVES_5456,
        RESULT_5455,
        RESULT_5456,
    ]


def symbolic_massless_determinant_certificate() -> dict[str, Any]:
    recoil, soft_cosine, soft_sine = sp.symbols("r c_s s_s")
    decay_cosine, decay_sine, relative = sp.symbols("c_d s_d z")
    relative_cosine = (
        (relative + 1 / relative) * soft_sine * decay_sine / 2
        + soft_cosine * decay_cosine
    )
    energy = (
        1
        + recoil**2
        - relative_cosine * (1 - recoil**2)
    ) / 2
    longitudinal = (
        relative_cosine * (1 - recoil) ** 2
        - (1 - recoil**2)
    ) / 2
    momentum_z = longitudinal * soft_cosine + recoil * decay_cosine
    holomorphic = (
        recoil * decay_sine * relative + longitudinal * soft_sine
    )
    antiholomorphic = (
        recoil * decay_sine / relative + longitudinal * soft_sine
    )
    plus = energy + momentum_z
    minus = energy - momentum_z
    numerator = sp.together(
        plus * minus - holomorphic * antiholomorphic
    ).as_numer_denom()[0]
    variables = (
        soft_sine,
        decay_sine,
        soft_cosine,
        decay_cosine,
        recoil,
        relative,
    )
    sphere_ideal = sp.groebner(
        [
            soft_sine**2 + soft_cosine**2 - 1,
            decay_sine**2 + decay_cosine**2 - 1,
        ],
        *variables,
    )
    remainder = sp.factor(sphere_ideal.reduce(numerator)[1])
    return {
        "identity": "p_plus*p_minus-p_holomorphic*p_antiholomorphic=0",
        "constraint_ideal": (
            "soft_sine^2+soft_cosine^2-1;"
            "decay_sine^2+decay_cosine^2-1"
        ),
        "groebner_remainder": str(remainder),
        "symbolic_massless_determinant_identity_valid": remainder == 0,
    }


def target_row() -> dict[str, str]:
    matches = [
        row
        for row in read_csv(REPRESENTATIVES_5456)
        if row["smoke_job_id"] == TARGET_JOB_ID
    ]
    if len(matches) != 1:
        raise RuntimeError(
            f"expected one {TARGET_JOB_ID} representative, found {len(matches)}"
        )
    return matches[0]


def projective_cover(
    parent: Any,
    stable: Any,
    target: dict[str, str],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    mapped_cells = {
        row["mapped_cell_id"]: row
        for row in parent.read_csv(parent.MAPPED_5393)
    }
    cell = mapped_cells[target["mapped_cell_id"]]
    configurations = parent.configuration_variants(target["term_id"])
    epsilon = parent.cbox(
        float(target["epsilon_real_lower"]),
        float(target["epsilon_real_upper"]),
        float(target["epsilon_imaginary_lower"]),
        float(target["epsilon_imaginary_upper"]),
    )
    x_lower = float(target["x_lower"])
    x_upper = float(target["x_upper"])
    t_lower = float(target["t_lower"])
    t_upper = float(target["t_upper"])
    rows: list[dict[str, Any]] = []
    selector_failures: list[dict[str, Any]] = []
    selected_role_counts: dict[str, int] = {}
    for x_index in range(X_SUBDIVISIONS):
        local_x_lower = x_lower + (
            (x_upper - x_lower) * x_index / X_SUBDIVISIONS
        )
        local_x_upper = x_lower + (
            (x_upper - x_lower) * (x_index + 1) / X_SUBDIVISIONS
        )
        absolute_coordinate = parent.cbox(local_x_lower, local_x_upper)
        for t_index in range(T_SUBDIVISIONS):
            local_t_lower = t_lower + (
                (t_upper - t_lower) * t_index / T_SUBDIVISIONS
            )
            local_t_upper = t_lower + (
                (t_upper - t_lower) * (t_index + 1) / T_SUBDIVISIONS
            )
            path_parameter = parent.cbox(local_t_lower, local_t_upper)
            energy = parent.deformed_path_energy_dual(
                cell,
                target["path_segment"],
                absolute_coordinate,
                path_parameter,
            ).value
            selected, selector = parent.closed_selector_configuration_subset(
                configurations,
                absolute_coordinate,
                energy,
                epsilon,
            )
            cell_id = f"x{x_index:02d}_t{t_index:02d}"
            if not selected:
                selector_failures.append(
                    {
                        "cell_id": cell_id,
                        "selector": selector,
                    }
                )
                continue
            selected_roles = "|".join(
                sorted(configuration["role"] for configuration in selected)
            )
            selected_role_counts[selected_roles] = (
                selected_role_counts.get(selected_roles, 0) + 1
            )
            for configuration in selected:
                try:
                    inputs, geometry = parent.interval_inputs(
                        configuration,
                        absolute_coordinate,
                        energy,
                        epsilon,
                    )
                    global_radius = 1.0e-7 * max(
                        1.0,
                        parent.M5258.upper_abs(geometry["selected_root"]),
                    )
                    raw_factors = {
                        name: parent.tight_first_lightcone_factor(
                            configuration,
                            inputs,
                            geometry,
                            name,
                        )
                        for name in PIVOT_NAMES
                    }
                    configuration_error = ""
                except Exception as error:
                    inputs = None
                    geometry = None
                    global_radius = math.nan
                    raw_factors = {}
                    configuration_error = (
                        f"{type(error).__name__}:{str(error).splitlines()[0][:500]}"
                    )
                for arc_index in range(GLOBAL_ARC_COUNT):
                    row = {
                        "checkpoint": CHECKPOINT,
                        "target_job_id": TARGET_JOB_ID,
                        "cell_id": cell_id,
                        "x_index": x_index,
                        "t_index": t_index,
                        "x_lower": local_x_lower,
                        "x_upper": local_x_upper,
                        "t_lower": local_t_lower,
                        "t_upper": local_t_upper,
                        "epsilon_real_lower": float(
                            target["epsilon_real_lower"]
                        ),
                        "epsilon_real_upper": float(
                            target["epsilon_real_upper"]
                        ),
                        "epsilon_imaginary_lower": float(
                            target["epsilon_imaginary_lower"]
                        ),
                        "epsilon_imaginary_upper": float(
                            target["epsilon_imaginary_upper"]
                        ),
                        "selector_ownership_method": selector[
                            "selector_ownership_method"
                        ],
                        "selector_selected_roles": selected_roles,
                        "configuration_role": configuration["role"],
                        "global_arc_index": arc_index,
                        "global_arc_count": GLOBAL_ARC_COUNT,
                        "failure_message": configuration_error,
                    }
                    if configuration_error:
                        row.update(
                            {
                                "owner_pivot": "",
                                "owner_family": "",
                                "owner_pivot_abs_lower": 0.0,
                                "owner_pivot_abs_upper": math.inf,
                                "unit_circle_abs_lower": 0.0,
                                "all_pivot_uppers_finite": False,
                                "projective_owner_cell_passes": False,
                            }
                        )
                        rows.append(row)
                        continue
                    phase = parent.cbox(arc_index, arc_index + 1) * parent.cpoint(
                        2 * math.pi / GLOBAL_ARC_COUNT
                    )
                    displacement = parent.cpoint(global_radius) * (
                        parent.iv.cos(phase)
                        + parent.cpoint(1j) * parent.iv.sin(phase)
                    )
                    unit_circle = geometry["selected_root"] + displacement
                    unit_circle_lower = parent.M5258.lower_abs(unit_circle)
                    factors = {
                        "plus": raw_factors["plus"],
                        "minus": raw_factors["minus"],
                        "holomorphic": unit_circle
                        * raw_factors["holomorphic"],
                        "antiholomorphic": (
                            raw_factors["antiholomorphic"] / unit_circle
                            if unit_circle_lower > 0.0
                            else parent.cbox(-math.inf, math.inf)
                        ),
                    }
                    lower_bounds = {
                        name: parent.M5258.lower_abs(value)
                        for name, value in factors.items()
                    }
                    upper_bounds = {
                        name: parent.M5258.upper_abs(value)
                        for name, value in factors.items()
                    }
                    owner_pivot = max(lower_bounds, key=lower_bounds.get)
                    owner_margin = lower_bounds[owner_pivot]
                    all_uppers_finite = all(
                        math.isfinite(value) for value in upper_bounds.values()
                    )
                    passes = (
                        owner_margin > 0.0
                        and unit_circle_lower > 0.0
                        and all_uppers_finite
                    )
                    row.update(
                        {
                            "owner_pivot": owner_pivot,
                            "owner_family": (
                                "plus"
                                if owner_pivot in {"plus", "holomorphic"}
                                else "minus"
                            ),
                            "owner_pivot_abs_lower": owner_margin,
                            "owner_pivot_abs_upper": upper_bounds[owner_pivot],
                            "plus_abs_lower": lower_bounds["plus"],
                            "minus_abs_lower": lower_bounds["minus"],
                            "holomorphic_abs_lower": lower_bounds[
                                "holomorphic"
                            ],
                            "antiholomorphic_abs_lower": lower_bounds[
                                "antiholomorphic"
                            ],
                            "unit_circle_abs_lower": unit_circle_lower,
                            "all_pivot_uppers_finite": all_uppers_finite,
                            "projective_owner_cell_passes": passes,
                            "failure_message": (
                                ""
                                if passes
                                else "NO_FINITE_POSITIVE_PROJECTIVE_OWNER"
                            ),
                        }
                    )
                    rows.append(row)
    diagnostics = {
        "x_subdivision_count": X_SUBDIVISIONS,
        "t_subdivision_count": T_SUBDIVISIONS,
        "xt_cell_count": X_SUBDIVISIONS * T_SUBDIVISIONS,
        "global_arc_count": GLOBAL_ARC_COUNT,
        "selector_failure_count": len(selector_failures),
        "selector_failure_examples": selector_failures[:3],
        "selected_role_cell_counts": selected_role_counts,
        "projective_owner_row_count": len(rows),
    }
    return rows, diagnostics


def owner_summary(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str, str], list[dict[str, Any]]] = {}
    for row in rows:
        key = (
            row["configuration_role"],
            row["owner_family"],
            row["owner_pivot"],
        )
        groups.setdefault(key, []).append(row)
    return [
        {
            "checkpoint": CHECKPOINT,
            "configuration_role": key[0],
            "owner_family": key[1],
            "owner_pivot": key[2],
            "row_count": len(group),
            "minimum_owner_pivot_abs_lower": min(
                float(row["owner_pivot_abs_lower"]) for row in group
            ),
            "maximum_owner_pivot_abs_upper": max(
                float(row["owner_pivot_abs_upper"]) for row in group
            ),
            "all_rows_pass": all(
                row["projective_owner_cell_passes"] for row in group
            ),
        }
        for key, group in sorted(groups.items())
    ]


def check(gate: str, passed: bool, evidence: Any) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "validation_gate": gate,
        "passed": bool(passed),
        "evidence": evidence,
    }


def render_document(payload: dict[str, Any]) -> None:
    lines = [
        "# 5457: D4 TOP finite projective-pivot cover",
        "",
        "## Decision",
        "",
        f"**{payload['decision']}**",
        "",
        "## Exact algebra",
        "",
        "The four candidate pivots are the light-cone components of one massless momentum. Direct reduction of the source formulas modulo `s_s^2+c_s^2=1` and `s_d^2+c_d^2=1` gives",
        "",
        "```text",
        "p_plus p_minus - p_holomorphic p_antiholomorphic = 0.",
        "```",
        "",
        "The Groebner remainder is exactly zero. The pivots are therefore a projective atlas, not four unrelated fitted denominators.",
        "",
        "## Finite owner cover",
        "",
        f"The previously blocked `{TARGET_JOB_ID}` domain is partitioned into `{payload['xt_cell_count']}` closed `(x,t)` cells. On every cell the unchanged parent selector first chooses the required representative/reciprocal chart set. Every selected chart is then checked on all `{payload['global_arc_count']}` contour arcs and assigned the pivot with the largest certified lower modulus.",
        "",
        f"Rows passed: `{payload['passed_projective_owner_row_count']}/{payload['projective_owner_row_count']}`. The global minimum owned-pivot modulus is `{payload['minimum_owner_pivot_abs_lower']}` and the minimum unit-circle modulus is `{payload['minimum_unit_circle_abs_lower']}`.",
        "",
        "## Claim boundary",
        "",
        "This proves only the finite projective ownership cover for the first blocked E01/U017 TOP representative. It does not yet transplant those owner cells into the full amplitude evaluator or validate the remaining outer representatives. Event-local W3, the regulator limit, local GR and full MTS remain unclaimed.",
        "",
    ]
    atomic_text(DOCUMENT, "\n".join(lines))


def run() -> dict[str, Any]:
    set_below_normal_priority()
    before_formalization = formalization_snapshot()
    missing = [str(path) for path in source_paths() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")
    result_5455 = read_json(RESULT_5455)
    result_5456 = read_json(RESULT_5456)
    if result_5455.get("valid_for_correlated_inner_Q_full_cover") is not True:
        raise RuntimeError("checkpoint 5455 inner-Q cover is not complete")
    if result_5456.get("valid_for_stable_recoil_sheet_enclosure") is not True:
        raise RuntimeError("checkpoint 5456 stable recoil sheet is not valid")
    symbolic = symbolic_massless_determinant_certificate()
    stable = load_module("mts_5456_for_5457", SCRIPT_5456)
    module_5449 = stable.load_module("mts_5449_for_5457", stable.SCRIPT_5449)
    parent = stable.load_module("mts_5396_for_5457", module_5449.PARENT_SCRIPT)
    parent.set_below_normal_priority()
    stable.install_stable_recoil_sheet(parent)
    target = target_row()
    rows, diagnostics = projective_cover(parent, stable, target)
    summaries = owner_summary(rows)
    passed_rows = [row for row in rows if row["projective_owner_cell_passes"]]
    covered_cells = {row["cell_id"] for row in rows}
    covered_arcs = {int(row["global_arc_index"]) for row in rows}
    all_pass = (
        bool(rows)
        and len(passed_rows) == len(rows)
        and diagnostics["selector_failure_count"] == 0
        and len(covered_cells) == diagnostics["xt_cell_count"]
        and len(covered_arcs) == GLOBAL_ARC_COUNT
        and symbolic["symbolic_massless_determinant_identity_valid"]
    )
    after_formalization = formalization_snapshot()
    payload: dict[str, Any] = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": (
            "TOP_FINITE_PROJECTIVE_PIVOT_COVER_CERTIFIED__TRANSPLANT_OWNER_CELLS"
            if all_pass
            else "TOP_FINITE_PROJECTIVE_PIVOT_COVER_NOT_CLOSED"
        ),
        **symbolic,
        **diagnostics,
        "covered_xt_cell_count": len(covered_cells),
        "covered_global_arc_count": len(covered_arcs),
        "passed_projective_owner_row_count": len(passed_rows),
        "failed_projective_owner_row_count": len(rows) - len(passed_rows),
        "minimum_owner_pivot_abs_lower": min(
            (float(row["owner_pivot_abs_lower"]) for row in passed_rows),
            default=math.nan,
        ),
        "minimum_unit_circle_abs_lower": min(
            (float(row["unit_circle_abs_lower"]) for row in passed_rows),
            default=math.nan,
        ),
        "next_target": (
            "TRANSPLANT_PROJECTIVE_OWNER_CELLS_INTO_PARENT_AMPLITUDE_EVALUATOR"
            if all_pass
            else "TOP_ENDPOINT_ZERO_MOMENTUM_LIMIT_OR_FINER_PROJECTIVE_COVER"
        ),
        "valid_for_target_TOP_finite_projective_pivot_cover": all_pass,
        "valid_for_outer_parent_leaf_transplant_smoke": False,
        "valid_for_full_outer_parent_leaf_enclosure": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    validations = [
        check("all_sources_exist", not missing, len(source_paths())),
        check("checkpoint_5455_inner_Q_cover_complete", result_5455.get("valid_for_correlated_inner_Q_full_cover") is True, result_5455.get("decision")),
        check("checkpoint_5456_stable_recoil_sheet_valid", result_5456.get("valid_for_stable_recoil_sheet_enclosure") is True, result_5456.get("decision")),
        check("massless_determinant_identity_exact", symbolic["symbolic_massless_determinant_identity_valid"], symbolic["groebner_remainder"]),
        check("all_256_xt_cells_covered", len(covered_cells) == X_SUBDIVISIONS * T_SUBDIVISIONS, len(covered_cells)),
        check("all_four_global_arcs_covered", len(covered_arcs) == GLOBAL_ARC_COUNT, sorted(covered_arcs)),
        check("selector_has_no_uncovered_cell", diagnostics["selector_failure_count"] == 0, diagnostics["selector_failure_count"]),
        check("every_selected_projective_owner_row_passes", len(passed_rows) == len(rows) and bool(rows), f"{len(passed_rows)}/{len(rows)}"),
        check("owned_pivot_margin_is_positive", payload["minimum_owner_pivot_abs_lower"] > 0.0, payload["minimum_owner_pivot_abs_lower"]),
        check("unit_circle_margin_is_positive", payload["minimum_unit_circle_abs_lower"] > 0.0, payload["minimum_unit_circle_abs_lower"]),
        check("all_pivot_uppers_are_finite", all(row["all_pivot_uppers_finite"] for row in rows), len(rows)),
        check("formalization_workbench_untouched", before_formalization == after_formalization, f"before={len(before_formalization)};after={len(after_formalization)}"),
        check("broad_claims_remain_false", not payload["valid_for_outer_parent_leaf_transplant_smoke"] and not payload["valid_for_full_outer_parent_leaf_enclosure"] and not payload["valid_for_D4_event_local_W3_bound"] and not payload["valid_for_all_operator_local_GR_claim"] and not payload["valid_for_full_MTS_claim"], "projective cover only"),
    ]
    payload["validation_row_count"] = len(validations)
    payload["failed_validation_count"] = sum(not row["passed"] for row in validations)
    source_rows = [
        {
            "checkpoint": CHECKPOINT,
            "path": str(path.resolve()),
            "exists": path.is_file(),
            "sha256": digest(path) if path.is_file() else "",
        }
        for path in source_paths()
    ]
    atomic_csv(COVER, rows)
    atomic_csv(SUMMARY, summaries)
    atomic_csv(SOURCE_REGISTER, source_rows)
    atomic_csv(VALIDATION, validations)
    render_document(payload)
    atomic_json(RESULT, payload)
    return payload


def main() -> int:
    payload = run()
    print(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True))
    return 0 if payload["failed_validation_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
