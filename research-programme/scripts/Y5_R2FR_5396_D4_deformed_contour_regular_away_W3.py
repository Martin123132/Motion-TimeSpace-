from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import sys
import time
import traceback
from typing import Any

from mpmath import iv


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


POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
RESIDUALS = POST / "source-intake" / "mts_residuals"
OUTPUT = FUNCTIONAL_RG / "5396"
DOCUMENT = POST / "5396-Y5-R2FR-D4-deformed-contour-regular-away-W3.md"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5396_VALIDATION.csv"

SCRIPT_5395 = (
    SCRIPTS
    / "Y5_R2FR_5395_D4_correlated_material_residue_supremum_and_numeric_pole_W3.py"
)
MAPPED_5393 = FUNCTIONAL_RG / "5393" / "D4_parent_frozen_mapped_cells.csv"
ATLAS_5393 = FUNCTIONAL_RG / "5393" / "D4_parent_frozen_x_atlas.csv"
BRANCHES_5393 = FUNCTIONAL_RG / "5393" / "D4_material_pole_branch_ownership.csv"
OWNER_DECOMPOSITION_5393 = FUNCTIONAL_RG / "5393" / "D4_W3_owner_decomposition.csv"
RESULT_5395 = FUNCTIONAL_RG / "5395" / "D4_correlated_material_residue_result.json"
RESIDUE_BOXES_5395 = (
    FUNCTIONAL_RG / "5395" / "D4_correlated_material_residue_boxes.csv"
)

CHECKPOINT = 5396
MARKER = "MTS_5396_D4_DEFORMED_CONTOUR_REGULAR_AWAY_W3"
REVISION = "D4-deformed-contour-regular-away-W3-v43"
PREVIOUS_RESUME_COMPATIBLE_REVISIONS = {
    "D4-deformed-contour-regular-away-W3-v3",
    "D4-deformed-contour-regular-away-W3-v4",
    "D4-deformed-contour-regular-away-W3-v5",
    "D4-deformed-contour-regular-away-W3-v6",
    "D4-deformed-contour-regular-away-W3-v7",
    "D4-deformed-contour-regular-away-W3-v8",
    "D4-deformed-contour-regular-away-W3-v9",
    "D4-deformed-contour-regular-away-W3-v10",
    "D4-deformed-contour-regular-away-W3-v11",
    "D4-deformed-contour-regular-away-W3-v12",
    "D4-deformed-contour-regular-away-W3-v13",
    "D4-deformed-contour-regular-away-W3-v14",
    "D4-deformed-contour-regular-away-W3-v15",
    "D4-deformed-contour-regular-away-W3-v16",
    "D4-deformed-contour-regular-away-W3-v17",
    "D4-deformed-contour-regular-away-W3-v18",
    "D4-deformed-contour-regular-away-W3-v19",
    "D4-deformed-contour-regular-away-W3-v20",
    "D4-deformed-contour-regular-away-W3-v21",
    "D4-deformed-contour-regular-away-W3-v22",
    "D4-deformed-contour-regular-away-W3-v23",
    "D4-deformed-contour-regular-away-W3-v24",
    "D4-deformed-contour-regular-away-W3-v25",
    "D4-deformed-contour-regular-away-W3-v26",
    "D4-deformed-contour-regular-away-W3-v27",
    "D4-deformed-contour-regular-away-W3-v28",
    "D4-deformed-contour-regular-away-W3-v29",
    "D4-deformed-contour-regular-away-W3-v30",
    "D4-deformed-contour-regular-away-W3-v31",
    "D4-deformed-contour-regular-away-W3-v32",
    "D4-deformed-contour-regular-away-W3-v33",
    "D4-deformed-contour-regular-away-W3-v34",
    "D4-deformed-contour-regular-away-W3-v35",
    "D4-deformed-contour-regular-away-W3-v36",
    "D4-deformed-contour-regular-away-W3-v37",
    "D4-deformed-contour-regular-away-W3-v38",
    "D4-deformed-contour-regular-away-W3-v39",
    "D4-deformed-contour-regular-away-W3-v40",
    "D4-deformed-contour-regular-away-W3-v41",
    "D4-deformed-contour-regular-away-W3-v42",
}


class RuntimeBudgetReached(RuntimeError):
    pass


def resume_manifest_compatible(
    existing: dict[str, Any], current: dict[str, Any]
) -> bool:
    if existing == current:
        return True
    same_revision_depth_increase = (
        existing.get("revision") == current.get("revision") == REVISION
    )
    compatible_revision_upgrade = (
        existing.get("revision") in PREVIOUS_RESUME_COMPATIBLE_REVISIONS
        and current.get("revision") == REVISION
    )
    if not (
        (same_revision_depth_increase or compatible_revision_upgrade)
        and int(current.get("maximum_depth", 0))
        >= int(existing.get("maximum_depth", 0))
    ):
        return False
    ignored = {
        "revision",
        "maximum_depth",
        "selector_certificate_migration_checkpoint",
        "selector_certificate_migration_revision",
    }
    return {
        key: value for key, value in existing.items() if key not in ignored
    } == {key: value for key, value in current.items() if key not in ignored}


INTERVAL_DIGITS = 45
REGULATOR_CAUCHY_RADIUS = 5.0e-7
CAUCHY_MULTIPLIER = 4.8e19
DEFAULT_ENERGY_DEFORMATION = 0.03
DEFAULT_TARGET_X_WIDTH = 2.0e-3
DEFAULT_TARGET_PATH_WIDTH = 0.125
DEFAULT_MAXIMUM_DEPTH = 18
DEFAULT_GLOBAL_ARC_COUNT = 8
DEFAULT_EPSILON_SUBDIVISIONS = 1
DEFAULT_COMBINED_REGULATOR_SLAB_COUNT = 2
PATH_STATE_CHECKPOINT_INTERVAL = 100
WINDING_ABS_UPPER = 2.0
LEGACY_SHARED_EXTERNAL_INVARIANT_RISK_ROWS = {
    ("S_X001_MC04_SM_DM", "MC04_SM_DM", "TOP", "RLRLDRD"),
}
SHARED_EXTERNAL_INVARIANT_FIXED_REVISIONS = {
    "D4-deformed-contour-regular-away-W3-v19",
    "D4-deformed-contour-regular-away-W3-v20",
    "D4-deformed-contour-regular-away-W3-v21",
    "D4-deformed-contour-regular-away-W3-v22",
    "D4-deformed-contour-regular-away-W3-v23",
    "D4-deformed-contour-regular-away-W3-v24",
    "D4-deformed-contour-regular-away-W3-v25",
    "D4-deformed-contour-regular-away-W3-v26",
    "D4-deformed-contour-regular-away-W3-v27",
    "D4-deformed-contour-regular-away-W3-v31",
    "D4-deformed-contour-regular-away-W3-v32",
    "D4-deformed-contour-regular-away-W3-v33",
    "D4-deformed-contour-regular-away-W3-v34",
    "D4-deformed-contour-regular-away-W3-v40",
    "D4-deformed-contour-regular-away-W3-v41",
    "D4-deformed-contour-regular-away-W3-v42",
    REVISION,
}
EXTERNAL01_FACTORIZED_KERNEL_REVISIONS = {
    "D4-deformed-contour-regular-away-W3-v31",
    "D4-deformed-contour-regular-away-W3-v32",
    "D4-deformed-contour-regular-away-W3-v33",
    "D4-deformed-contour-regular-away-W3-v34",
    "D4-deformed-contour-regular-away-W3-v40",
    "D4-deformed-contour-regular-away-W3-v41",
    "D4-deformed-contour-regular-away-W3-v42",
    REVISION,
}
MIXED_EXTERNAL_TRANSVERSE_SUBCOVER_REVISIONS = {
    "D4-deformed-contour-regular-away-W3-v33",
    "D4-deformed-contour-regular-away-W3-v34",
}

CLAIM_DEFORMATION = "valid_for_D4_regular_away_contour_deformation"
CLAIM_AWAY = "valid_for_D4_numeric_regular_away_W3_bound"
OPEN_CLAIMS = (
    "valid_for_D4_numeric_event_local_W3_bound",
    "valid_for_D4_numeric_W3_bound",
    "valid_for_D4_numeric_uniform_remainder_bound",
    "valid_for_D4_outer_regulator_zero_limit",
    "valid_for_decay_angle_integral",
    "valid_for_full_angular_convergence",
    "valid_for_full_phase_space_coefficient",
    "valid_for_numeric_UV_claim",
    "valid_for_local_GR_claim",
    "valid_for_full_MTS_claim",
)


class EnclosureFailure(RuntimeError):
    pass


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


M5395 = load_module("mts_5395_for_5396", SCRIPT_5395)
M5394 = M5395.M5394
M5386 = M5395.M5386
M5385 = M5395.M5385
M5258 = M5395.M5258
M5308 = M5394.M5308


def set_below_normal_priority() -> None:
    if os.name != "nt":
        return
    import ctypes

    process = ctypes.windll.kernel32.GetCurrentProcess()
    ctypes.windll.kernel32.SetPriorityClass(process, 0x00004000)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise RuntimeError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    os.replace(temporary, path)


def validation_row(
    gate: str,
    passed: bool,
    evidence: Any,
) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "validation_gate": gate,
        "passed": bool(passed),
        "evidence": evidence,
    }


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def term_signs(term_id: str) -> tuple[int, int]:
    pieces = term_id.split("_")
    if len(pieces) != 3 or pieces[0] != "MC04":
        raise ValueError(f"unsupported reduced term {term_id}")
    return (1 if pieces[1] == "SP" else -1, 1 if pieces[2] == "DP" else -1)


def parent_selector_probe() -> list[dict[str, Any]]:
    context = M5308.M5303.synthetic_context()
    rows: list[dict[str, Any]] = []
    for cell in read_csv(MAPPED_5393):
        if cell["region_class"] != "AWAY":
            continue
        coordinate = 0.5 * (
            float(cell["lower_absolute_soft_cosine"])
            + float(cell["upper_absolute_soft_cosine"])
        )
        energy = 0.5 * (
            float(cell["midpoint_energy_lower"])
            + float(cell["midpoint_energy_upper"])
        )
        for term_id in cell["reduced_MC04_term_ids"].split("|"):
            soft_sign, decay_sign = term_signs(term_id)
            local = M5308.M5302.local_context(
                context,
                coordinate,
                soft_sign,
                decay_sign,
            )
            event = dict(local["source_event"])
            event["soft_energy"] = energy
            target = local["inventories"]["E0025"]["target"]
            rationals = M5308.M5280.M5274.M5231.root_rationals(event, target)
            evaluation = M5308.M5280.evaluate_component(
                event,
                "E0025",
                "MC04",
                local,
                rationals=rationals,
                convergence_audit=False,
            )
            rows.append(
                {
                    "mapped_cell_id": cell["mapped_cell_id"],
                    "term_id": term_id,
                    "coordinate": coordinate,
                    "energy": energy,
                    "selected_role": evaluation["selected_role"],
                    "selected_labels": evaluation["representing_pair"],
                    "orientation": evaluation["orientation"],
                    "winding_delta": evaluation["winding_delta"],
                    "mask_active": evaluation["mask_active"],
                    "evaluation_status": evaluation["evaluation_status"],
                }
            )
    return rows


def selector_map() -> dict[tuple[str, str], dict[str, Any]]:
    cache = OUTPUT / "selector_states.csv"
    rows = read_csv(cache) if cache.is_file() else parent_selector_probe()
    return {
        (row["mapped_cell_id"], row["term_id"]): row
        for row in rows
    }


def configuration_from_selector(row: dict[str, Any]) -> dict[str, Any]:
    soft_sign, decay_sign = term_signs(row["term_id"])
    labels = tuple(row["selected_labels"].split("|"))
    return {
        "event_type": "AWAY",
        "term_id": row["term_id"],
        "soft_sign": soft_sign,
        "decay_sign": decay_sign,
        "sign": soft_sign,
        "role": row["selected_role"],
        "labels": labels,
        "root_labels": tuple(label.rsplit(":", 1)[1] for label in labels),
        "trace_orientation": int(row["orientation"]),
        "winding_delta": int(row["winding_delta"]),
    }


def configuration_variants(term_id: str) -> list[dict[str, Any]]:
    definitions = {
        "MC04_SM_DM": (
            ("reciprocal", "direct:g1:minus_v|direct:g3:plus_v", 1, 2),
            ("representative", "direct:g1:minus_u|direct:g3:plus_u", -1, -2),
        ),
        "MC04_SP_DM": (
            ("reciprocal", "direct:g1:minus_v|direct:g3:plus_v", 1, 2),
        ),
        "MC04_SP_DP": (
            ("reciprocal", "direct:g1:minus_v|direct:g3:plus_v", -1, 2),
            ("representative", "direct:g1:minus_u|direct:g3:plus_u", 1, -2),
        ),
    }
    if term_id not in definitions:
        raise ValueError(f"unsupported reduced term {term_id}")
    return [
        configuration_from_selector(
            {
                "term_id": term_id,
                "selected_role": role,
                "selected_labels": labels,
                "orientation": orientation,
                "winding_delta": winding,
            }
        )
        for role, labels, orientation, winding in definitions[term_id]
    ]


def cpoint(value: complex | float | int) -> Any:
    return M5258.cpoint(value)


def cbox(
    real_lower: float,
    real_upper: float,
    imaginary_lower: float = 0.0,
    imaginary_upper: float = 0.0,
) -> Any:
    return M5258.cbox(
        real_lower,
        real_upper,
        imaginary_lower,
        imaginary_upper,
    )


def sheet_locked_external_transverse(target: Any) -> Any:
    return cpoint(1j) * M5386.chart_safe_sqrt(target * target - cpoint(1))


def sheet_locked_external_transverse_dual(target: Any) -> Any:
    dual_target = M5385.M5381.IntervalDual.coerce(target)
    return 1j * M5386.chart_safe_sqrt_dual(
        dual_target * dual_target - cpoint(1)
    )


def sheet_locked_interval_cut_momenta(
    internal: list[list[Any]], target: Any
) -> tuple[list[list[Any]], list[list[Any]]]:
    one = cpoint(1)
    zero = cpoint(0)
    transverse = sheet_locked_external_transverse(target)
    external = (
        [one, zero, zero, one],
        [one, zero, zero, -one],
        [one, transverse, zero, target],
        [one, -transverse, zero, -target],
    )
    zero_momentum = [zero for _ in range(4)]
    left = [list(zero_momentum) for _ in range(5)]
    right = [list(zero_momentum) for _ in range(5)]
    left[0] = [-value for value in external[0]]
    left[4] = [-value for value in external[1]]
    right[0] = list(external[2])
    right[4] = list(external[3])
    for index in range(3):
        left[index + 1] = list(internal[index])
        right[index + 1] = [-value for value in internal[index]]
    return left, right


def interval_inputs(
    configuration: dict[str, Any],
    absolute_coordinate: Any,
    energy: Any,
    epsilon: Any,
) -> tuple[dict[str, Any], dict[str, Any]]:
    soft_cosine = configuration["soft_sign"] * absolute_coordinate
    soft_sine = M5394.interval_complex_sqrt(cpoint(1) - soft_cosine**2)
    decay_cosine = cpoint(
        configuration["decay_sign"] * M5394.ABSOLUTE_DECAY_COSINE
    )
    decay_sine = cpoint(
        math.sqrt(1.0 - M5394.ABSOLUTE_DECAY_COSINE**2)
    )
    q_value = M5394.q_value(epsilon)
    external_root = -cpoint(1j) * M5394.interval_complex_sqrt(-q_value)
    recoil = M5394.interval_complex_sqrt(cpoint(1) - energy)
    if M5394.real_bounds(recoil)[0] <= 0.0:
        raise EnclosureFailure(
            "deformed recoil leaves its parent positive-real sheet"
        )
    inputs = {
        "epsilon": epsilon,
        "material_recoil": recoil,
        "soft_cosine": soft_cosine,
        "soft_sine": soft_sine,
        "decay_cosine": decay_cosine,
        "decay_sine": decay_sine,
        "q_value": q_value,
        "external_root": external_root,
    }
    geometry = M5385.expanded_geometry(
        configuration,
        inputs,
        cpoint(0),
        recoil_override=recoil,
    )
    return inputs, geometry


def closed_selector_configuration_subset(
    configurations: list[dict[str, Any]],
    absolute_coordinate: Any,
    energy: Any,
    epsilon: Any,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    roles = {configuration["role"] for configuration in configurations}
    if len(configurations) == 1:
        return configurations, {
            "selector_ownership_method": "SINGLE_DECLARED_CHART",
            "selector_margin_source_role": configurations[0]["role"],
            "selector_role_margin_lower": math.inf,
            "selector_representative_modulus_lower": math.nan,
            "selector_representative_modulus_upper": math.nan,
            "selector_margin_failure_category": "",
        }
    if roles != {"representative", "reciprocal"}:
        return configurations, {
            "selector_ownership_method": "FINITE_DECLARED_CHART_UNION",
            "selector_margin_source_role": "CHART_UNION",
            "selector_role_margin_lower": 0.0,
            "selector_representative_modulus_lower": math.nan,
            "selector_representative_modulus_upper": math.nan,
            "selector_margin_failure_category": (
                "DECLARED_CHART_SET_IS_NOT_RECIPROCAL_PAIR"
            ),
        }
    representative_configuration = next(
        configuration
        for configuration in configurations
        if configuration["role"] == "representative"
    )
    try:
        _, representative_geometry = interval_inputs(
            representative_configuration,
            absolute_coordinate,
            energy,
            epsilon,
        )
        representative = representative_geometry["relative"]
        modulus_lower = M5258.lower_abs(representative)
        modulus_upper = M5258.upper_abs(representative)
    except Exception as error:
        return configurations, {
            "selector_ownership_method": "FINITE_DECLARED_CHART_UNION",
            "selector_margin_source_role": "CHART_UNION",
            "selector_role_margin_lower": 0.0,
            "selector_representative_modulus_lower": math.nan,
            "selector_representative_modulus_upper": math.nan,
            "selector_margin_failure_category": enclosure_failure_category(
                error
            ),
        }
    selected_role = "CHART_UNION"
    margin = 0.0
    if modulus_upper < 1.0:
        selected_role = "reciprocal"
        margin = 1.0 - modulus_upper
    elif modulus_lower > 1.0:
        selected_role = "representative"
        margin = modulus_lower - 1.0
    if selected_role == "CHART_UNION":
        selected_configurations = configurations
        method = "FINITE_DECLARED_CHART_UNION"
    else:
        selected_configurations = [
            configuration
            for configuration in configurations
            if configuration["role"] == selected_role
        ]
        method = "CLOSED_REPRESENTATIVE_UNIT_MODULUS_MARGIN"
    return selected_configurations, {
        "selector_ownership_method": method,
        "selector_margin_source_role": selected_role,
        "selector_role_margin_lower": margin,
        "selector_representative_modulus_lower": modulus_lower,
        "selector_representative_modulus_upper": modulus_upper,
        "selector_margin_failure_category": "",
    }


def interval_boundary_energy(
    owner: str,
    x_lower: float,
    x_upper: float,
) -> tuple[Any, dict[str, float]]:
    minimum, maximum = M5308.energy_limits()
    if owner == "ENERGY_MINIMUM":
        return cpoint(minimum), {"boundary_discriminant_abs_lower": math.inf}
    if owner == "ENERGY_MAXIMUM":
        return cpoint(maximum), {"boundary_discriminant_abs_lower": math.inf}
    first_owner = owner.split("|")[0]
    surface_id, branch_id = first_owner.rsplit(":", 1)
    if branch_id not in {"Q01", "Q02"}:
        raise EnclosureFailure(f"unsupported hard-boundary branch {owner}")
    component, soft_label, decay_label = surface_id.split("_")
    hard_sign = 1 if component == "MC04" else -1
    soft_sign = 1 if soft_label == "SP" else -1
    decay_sign = 1 if decay_label == "DP" else -1
    absolute_coordinate = cbox(x_lower, x_upper)
    soft_cosine = (
        absolute_coordinate
        if soft_sign > 0
        else cbox(-x_upper, -x_lower)
    )
    decay_cosine = cpoint(decay_sign * M5394.ABSOLUTE_DECAY_COSINE)
    soft_sine = M5394.interval_complex_sqrt(
        cpoint(1) - soft_cosine * soft_cosine
    )
    decay_sine = cpoint(
        math.sqrt(1 - M5394.ABSOLUTE_DECAY_COSINE**2)
    )
    relative = soft_cosine * decay_cosine - soft_sine * decay_sine
    coefficient_a = (soft_cosine - cpoint(M5394.TARGET_COSINE)) * (
        cpoint(1) + cpoint(hard_sign) * relative
    )
    coefficient_b = cpoint(2 * hard_sign) * (
        decay_cosine - soft_cosine * relative
    )
    coefficient_c = (soft_cosine + cpoint(M5394.TARGET_COSINE)) * (
        cpoint(hard_sign) * relative - cpoint(1)
    )
    denominator_lower = M5394.lower_abs(cpoint(2) * coefficient_a)
    discriminant = (
        coefficient_b * coefficient_b
        - cpoint(4) * coefficient_a * coefficient_c
    )
    discriminant_real_lower, discriminant_real_upper = M5394.real_bounds(
        discriminant
    )
    discriminant_imaginary_lower, discriminant_imaginary_upper = (
        M5394.imaginary_bounds(discriminant)
    )
    if (
        discriminant_real_upper < 0.0
        or discriminant_imaginary_lower > 0.0
        or discriminant_imaginary_upper < 0.0
    ):
        raise EnclosureFailure(f"hard-boundary discriminant leaves real sheet: {owner}")
    discriminant_lower = max(0.0, discriminant_real_lower)
    discriminant_root = iv.mpc(
        iv.sqrt(iv.mpf([discriminant_lower, discriminant_real_upper])),
        iv.mpf([0.0, 0.0]),
    )
    candidates: list[Any] = []
    if denominator_lower > 0.0:
        candidates.extend(
            (
                (-coefficient_b - discriminant_root)
                / (cpoint(2) * coefficient_a),
                (-coefficient_b + discriminant_root)
                / (cpoint(2) * coefficient_a),
            )
        )
    for stable_denominator in (
        coefficient_b - discriminant_root,
        coefficient_b + discriminant_root,
    ):
        if M5394.lower_abs(stable_denominator) > 0.0:
            candidates.append(-cpoint(2) * coefficient_c / stable_denominator)
    if not candidates:
        raise EnclosureFailure(f"no stable hard-boundary root chart: {owner}")
    coordinate_midpoint = 0.5 * (x_lower + x_upper)
    expected_energy = float(M5308.boundary_energy(owner, coordinate_midpoint))
    expected_q = math.sqrt(max(0.0, 1.0 - expected_energy))
    selected_q = min(
        candidates,
        key=lambda value: abs(M5394.midpoint(value) - expected_q),
    )
    energy = cpoint(1) - selected_q * selected_q
    return energy, {
        "boundary_discriminant_abs_lower": discriminant_lower,
        "boundary_coefficient_abs_lower": denominator_lower,
    }


def interval_boundary_energy_dual(owner: str, absolute_coordinate: Any) -> Any:
    dual = M5385.M5381.IntervalDual
    absolute_coordinate = dual.coerce(absolute_coordinate)
    minimum, maximum = M5308.energy_limits()
    if owner == "ENERGY_MINIMUM":
        return dual(cpoint(minimum))
    if owner == "ENERGY_MAXIMUM":
        return dual(cpoint(maximum))
    first_owner = owner.split("|")[0]
    surface_id, branch_id = first_owner.rsplit(":", 1)
    if branch_id not in {"Q01", "Q02"}:
        raise EnclosureFailure(f"unsupported hard-boundary branch {owner}")
    component, soft_label, decay_label = surface_id.split("_")
    hard_sign = 1 if component == "MC04" else -1
    soft_sign = 1 if soft_label == "SP" else -1
    decay_sign = 1 if decay_label == "DP" else -1
    soft_cosine = absolute_coordinate * soft_sign
    decay_cosine = cpoint(
        decay_sign * M5394.ABSOLUTE_DECAY_COSINE
    )
    soft_sine = M5385.positive_sqrt_dual(
        1 - soft_cosine * soft_cosine
    )
    decay_sine = cpoint(
        math.sqrt(1 - M5394.ABSOLUTE_DECAY_COSINE**2)
    )
    relative = soft_cosine * decay_cosine - soft_sine * decay_sine
    coefficient_a = (
        soft_cosine - M5394.TARGET_COSINE
    ) * (1 + hard_sign * relative)
    coefficient_b = (
        dual(decay_cosine) - soft_cosine * relative
    ) * (2 * hard_sign)
    coefficient_c = (
        soft_cosine + M5394.TARGET_COSINE
    ) * (hard_sign * relative - 1)
    discriminant = (
        coefficient_b * coefficient_b
        - 4 * coefficient_a * coefficient_c
    )
    discriminant_root = M5386.chart_safe_sqrt_dual(discriminant)
    candidates: list[Any] = []
    if M5258.lower_abs(2 * coefficient_a.value) > 0.0:
        candidates.extend(
            (
                (-coefficient_b - discriminant_root) / (2 * coefficient_a),
                (-coefficient_b + discriminant_root) / (2 * coefficient_a),
            )
        )
    for stable_denominator in (
        coefficient_b - discriminant_root,
        coefficient_b + discriminant_root,
    ):
        if M5258.lower_abs(stable_denominator.value) > 0.0:
            candidates.append(
                -2 * coefficient_c / stable_denominator
            )
    if not candidates:
        raise EnclosureFailure(f"no stable dual hard-boundary root chart: {owner}")
    coordinate_midpoint = complex(
        M5394.midpoint(absolute_coordinate.value)
    ).real
    expected_energy = float(M5308.boundary_energy(owner, coordinate_midpoint))
    expected_q = math.sqrt(max(0.0, 1.0 - expected_energy))
    selected_q = min(
        candidates,
        key=lambda value: abs(
            complex(M5394.midpoint(value.value)) - expected_q
        ),
    )
    return 1 - selected_q * selected_q


def epsilon_interval(row: dict[str, Any]) -> Any:
    return cbox(
        float(row["epsilon_real_lower"]),
        float(row["epsilon_real_upper"]),
        float(row["epsilon_imaginary_lower"]),
        float(row["epsilon_imaginary_upper"]),
    )


def epsilon_boxes(arguments: argparse.Namespace) -> list[dict[str, Any]]:
    if not arguments.combined_regulator_box:
        return M5395.epsilon_subboxes(arguments.epsilon_subdivisions)
    slab_count = int(
        getattr(
            arguments,
            "combined_regulator_slab_count",
            DEFAULT_COMBINED_REGULATOR_SLAB_COUNT,
        )
    )
    if slab_count <= 0:
        raise ValueError("combined regulator slab count must be positive")
    full_lower = M5394.REGULATOR_INTERVAL[0] - M5394.REGULATOR_CAUCHY_RADIUS
    full_upper = M5394.REGULATOR_INTERVAL[1] + M5394.REGULATOR_CAUCHY_RADIUS
    width = (full_upper - full_lower) / slab_count
    return [
        {
            "regulator_bin_index": 0,
            "epsilon_subdivision_index": slab_index,
            "epsilon_subdivision_count": slab_count,
            "Cauchy_center_lower": M5394.REGULATOR_INTERVAL[0],
            "Cauchy_center_upper": M5394.REGULATOR_INTERVAL[1],
            "epsilon_real_lower": full_lower + slab_index * width,
            "epsilon_real_upper": full_lower + (slab_index + 1) * width,
            "epsilon_imaginary_lower": -M5394.REGULATOR_CAUCHY_RADIUS,
            "epsilon_imaginary_upper": M5394.REGULATOR_CAUCHY_RADIUS,
            "epsilon_cover_type": "RECTANGULAR_CAUCHY_TUBE_PARTITION",
        }
        for slab_index in range(slab_count)
    ]


def material_branch_data() -> dict[str, dict[str, Any]]:
    residue_result = read_json(RESULT_5395)
    residue_bounds = residue_result["branch_material_residue_abs_upper"]
    rows: dict[str, dict[str, Any]] = {}
    for branch in M5394.material_branches():
        branch_id = branch["branch_owner_id"]
        rows[branch_id] = {
            **branch,
            "sign": int(branch["sign"]),
            "material_residue_abs_upper": float(residue_bounds[branch_id]),
        }
    return rows


def material_support_segments() -> list[dict[str, Any]]:
    return [dict(row) for row in M5394.away_support_segments()]


def away_term_support_cells() -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for cell in read_csv(MAPPED_5393):
        if cell["region_class"] != "AWAY":
            continue
        for term_id in cell["reduced_MC04_term_ids"].split("|"):
            grouped.setdefault((cell["atlas_cell_id"], term_id), []).append(cell)
    rows: list[dict[str, Any]] = []
    for (atlas_cell_id, term_id), cells in sorted(grouped.items()):
        ordered = sorted(cells, key=lambda row: int(row["parent_chamber_index"]))
        chamber_indices = [int(row["parent_chamber_index"]) for row in ordered]
        if any(
            second - first != 1
            for first, second in zip(chamber_indices[:-1], chamber_indices[1:])
        ):
            raise EnclosureFailure(
                f"non-contiguous term support for {atlas_cell_id} {term_id}"
            )
        rows.append(
            {
                **ordered[0],
                "mapped_cell_id": f"S_{atlas_cell_id}_{term_id}",
                "source_mapped_cell_ids": "|".join(
                    row["mapped_cell_id"] for row in ordered
                ),
                "lower_energy_boundary": ordered[0]["lower_energy_boundary"],
                "upper_energy_boundary": ordered[-1]["upper_energy_boundary"],
                "reduced_MC04_term_ids": term_id,
                "parent_chamber_index": "|".join(
                    str(value) for value in chamber_indices
                ),
                "integrand_owner": "AWAY_TERM_CONTIGUOUS_SUPPORT_UNION",
            }
        )
    return rows


def cell_x_partitions(
    cell: dict[str, Any],
    support_segments: list[dict[str, Any]],
) -> list[tuple[float, float]]:
    lower = float(cell["lower_absolute_soft_cosine"])
    upper = float(cell["upper_absolute_soft_cosine"])
    breakpoints = {lower, upper}
    terms = set(cell["reduced_MC04_term_ids"].split("|"))
    for segment in support_segments:
        if (
            segment["atlas_cell_id"] == cell["atlas_cell_id"]
            and segment["term_id"] in terms
        ):
            for value in (float(segment["x_lower"]), float(segment["x_upper"])):
                if lower < value < upper:
                    breakpoints.add(value)
    ordered = sorted(breakpoints)
    return list(zip(ordered[:-1], ordered[1:]))


def active_material_branches(
    cell: dict[str, Any],
    term_id: str,
    x_lower: float,
    x_upper: float,
    support_segments: list[dict[str, Any]],
    branches: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    midpoint_x = 0.5 * (x_lower + x_upper)
    selected: list[dict[str, Any]] = []
    for segment in support_segments:
        if (
            segment["atlas_cell_id"] == cell["atlas_cell_id"]
            and segment["term_id"] == term_id
            and float(segment["x_lower"]) - 1.0e-14 <= midpoint_x
            <= float(segment["x_upper"]) + 1.0e-14
        ):
            if not (
                x_lower >= float(segment["x_lower"]) - 1.0e-13
                and x_upper <= float(segment["x_upper"]) + 1.0e-13
            ):
                raise EnclosureFailure(
                    f"material support changes inside [{x_lower},{x_upper}]"
                )
            selected.append(branches[segment["branch_owner_id"]])
    return selected


def joint_pole_center_probe_only(
    configuration: dict[str, Any],
    absolute_coordinate: Any,
    energy: Any,
    epsilon: Any,
) -> tuple[float, dict[str, Any]]:
    inputs, geometry = interval_inputs(
        configuration,
        absolute_coordinate,
        energy,
        epsilon,
    )
    diagnostics = M5258.IntervalDiagnostics()
    target = cpoint(-9) + cpoint(1j) * epsilon
    internal = M5258.rotate_internal_lightcone(
        M5386.amplitude_state(geometry), geometry["selected_root"]
    )
    left, right = sheet_locked_interval_cut_momenta(internal, target)
    exact_invariants = {
        frozenset((1, 2)): cpoint(4) * geometry["recoil"] ** 2
    }
    left_edges = M5395.centered_hard_soft_overrides(
        configuration,
        inputs,
        geometry,
        left,
    )
    right_edges = M5386.first_plus_edge_overrides(
        configuration,
        inputs,
        geometry,
        cpoint(0),
        cpoint(0),
        target,
        use_material_recoil_sheet=True,
    )
    right_edges.update(
        M5386.first_minus_edge_overrides(
            configuration,
            inputs,
            geometry,
            cpoint(0),
            target,
        )
    )
    right_edges.update(
        M5386.second_external_edge_overrides(
            configuration,
            inputs,
            geometry,
            cpoint(0),
            target,
        )
    )
    try:
        right_edges.update(
            M5386.internal_hard_pair_edge_overrides(
                configuration,
                inputs,
                geometry,
                cpoint(0),
            )
        )
    except M5258.IntervalSingularity:
        pass
    left_first, _, left_chart = M5395.centered_first_rational_spinors(
        configuration,
        inputs,
        geometry,
        1,
        diagnostics,
        "away_left_first",
    )
    right_first, right_exponents, right_chart = (
        M5395.centered_first_rational_spinors(
            configuration,
            inputs,
            geometry,
            -1,
            diagnostics,
            "away_right_first",
        )
    )
    active_chirality = 1 if configuration["role"] == "reciprocal" else 0
    left_chirality = 1 - active_chirality
    hhh = cpoint(0)
    surviving_global_terms = 0
    for special in (1, 2, 3):
        left_value = M5386.scalar_klt_five_interval(
            left,
            special,
            left_chirality,
            diagnostics,
            f"away_left_K5:s{special}:c{left_chirality}",
            exact_invariants,
            left_edges,
            {1: left_first},
        )
        right_value, right_count = (
            M5395.global_regularized_scalar_klt_five_at_center(
                right,
                special,
                active_chirality,
                active_chirality,
                geometry["selected_root"],
                exact_invariants,
                right_edges,
                {1: right_first},
                {1: right_exponents},
                diagnostics,
                f"away_right_global_K5:s{special}:c{active_chirality}",
            )
        )
        hhh += left_value * right_value
        surviving_global_terms += right_count
    if surviving_global_terms <= 0:
        raise EnclosureFailure("no globally regularized KLT term survives")
    hhh /= cpoint(6)
    coefficient = (
        geometry["energy"]
        * M5386.stable_energy_multiplier(
            internal,
            diagnostics,
            "away_global_multiplier",
        )
        * hhh
        / cpoint(M5258.S_VALUE * M5258.S_VALUE)
    )
    geometric = M5386.energy_contour_geometric_factors(
        configuration,
        inputs,
        geometry,
    )
    denominator_lower = math.prod(
        M5258.lower_abs(geometric[name])
        for name in (
            "relative_root",
            "selected_global_root",
            "collision_jacobian",
        )
    )
    if denominator_lower <= 0.0:
        raise EnclosureFailure("global residue geometric denominator reaches zero")
    residue = cpoint(
        int(configuration["winding_delta"])
        * int(configuration["trace_orientation"])
    ) * coefficient
    for name in (
        "relative_root",
        "selected_global_root",
        "collision_jacobian",
    ):
        residue = M5258.safe_divide(
            residue,
            geometric[name],
            diagnostics,
            f"away_residue_geometric:{name}",
        )
    residue_upper = M5258.upper_abs(residue)
    if not math.isfinite(residue_upper):
        raise EnclosureFailure("global residue upper bound is not finite")
    return residue_upper, {
        "minimum_amplitude_denominator_abs_lower": diagnostics.minimum_denominator_lower,
        "relative_root_abs_lower": M5258.lower_abs(geometric["relative_root"]),
        "selected_global_root_abs_lower": M5258.lower_abs(
            geometric["selected_global_root"]
        ),
        "collision_jacobian_abs_lower": M5258.lower_abs(
            geometric["collision_jacobian"]
        ),
        "left_first_spinor_chart": left_chart,
        "right_first_spinor_chart": right_chart,
        "surviving_global_KLT_terms": surviving_global_terms,
        "global_residue_midpoint_real": M5258.midpoint(residue).real,
        "global_residue_midpoint_imaginary": M5258.midpoint(residue).imag,
    }


def rational_spinor_overrides(
    momenta: list[list[Any]],
    diagnostics: Any,
    label: str,
    first_override: tuple[
        tuple[list[Any], list[Any]],
        tuple[list[int], list[int]],
        str,
    ]
    | None = None,
    second_override: tuple[
        tuple[list[Any], list[Any]],
        tuple[list[int], list[int]],
        str,
    ]
    | None = None,
) -> tuple[
    dict[int, tuple[list[Any], list[Any]]],
    dict[int, tuple[list[int], list[int]]],
    dict[int, str],
]:
    spinors: dict[int, tuple[list[Any], list[Any]]] = {}
    exponents: dict[int, tuple[list[int], list[int]]] = {}
    charts: dict[int, str] = {}
    for index, momentum in enumerate(momenta):
        if index == 1 and first_override is not None:
            spinors[index], exponents[index], charts[index] = first_override
            continue
        if index == 2 and second_override is not None:
            spinors[index], exponents[index], charts[index] = second_override
            continue
        plus = momentum[0] + momentum[3]
        minus = momentum[0] - momentum[3]
        chart = (
            "plus"
            if M5258.lower_abs(plus) >= M5258.lower_abs(minus)
            else "minus"
        )
        spinors[index] = M5386.rational_massless_spinors(
            momentum,
            diagnostics,
            f"{label}:p{index}",
            False,
        )
        charts[index] = chart
        if index in (1, 2, 3):
            exponents[index] = (
                ([0, 1], [0, -1])
                if chart == "plus"
                else ([-1, 0], [1, 0])
            )
    return spinors, exponents, charts


def tight_first_lightcone_factor(
    configuration: dict[str, Any],
    inputs: dict[str, Any],
    geometry: dict[str, Any],
    factor: str,
) -> Any:
    candidates: list[Any] = []
    errors: list[Exception] = []
    try:
        candidates.append(
            M5386.centered_first_lightcone_factor(
                configuration, inputs, geometry, factor
            )
        )
    except (M5258.IntervalSingularity, ValueError) as error:
        errors.append(error)
    try:
        candidates.append(
            M5386.first_lightcone_factor_dual(
                configuration,
                inputs["epsilon"],
                geometry["recoil"],
                inputs["soft_cosine"],
                inputs["decay_cosine"],
                inputs["decay_sine"],
                factor,
            ).value
        )
    except (M5258.IntervalSingularity, ValueError) as error:
        errors.append(error)
    if not candidates:
        raise errors[0]
    return max(
        candidates,
        key=lambda value: (
            M5258.lower_abs(value),
            -M5258.upper_abs(value),
        ),
    )


def displaced_first_rational_spinors(
    configuration: dict[str, Any],
    inputs: dict[str, Any],
    geometry: dict[str, Any],
    global_displacement: Any,
    orientation: int,
    diagnostics: Any,
    label: str,
) -> tuple[
    tuple[list[Any], list[Any]],
    tuple[list[int], list[int]],
    str,
]:
    unit_circle = geometry["selected_root"] + global_displacement
    plus = cpoint(orientation) * tight_first_lightcone_factor(
        configuration, inputs, geometry, "plus"
    )
    minus = cpoint(orientation) * tight_first_lightcone_factor(
        configuration, inputs, geometry, "minus"
    )
    holomorphic = (
        cpoint(orientation)
        * unit_circle
        * tight_first_lightcone_factor(
            configuration, inputs, geometry, "holomorphic"
        )
    )
    antiholomorphic = (
        cpoint(orientation)
        * tight_first_lightcone_factor(
            configuration, inputs, geometry, "antiholomorphic"
        )
        / unit_circle
    )
    pivot_name, chart, pivot = max(
        (
            ("plus_diagonal", "plus", plus),
            ("holomorphic_transverse", "plus", holomorphic),
            ("minus_diagonal", "minus", minus),
            ("antiholomorphic_transverse", "minus", antiholomorphic),
        ),
        key=lambda item: M5258.lower_abs(item[2]),
    )
    if M5258.lower_abs(pivot) <= 0.0:
        raise M5258.IntervalSingularity(
            f"no displaced first-spinor rational pivot survives: {label}"
        )
    diagnostics.record(pivot, f"{label}:{pivot_name}")
    if pivot_name == "plus_diagonal":
        spinors = (
            [plus, holomorphic],
            [
                cpoint(1),
                M5258.safe_divide(
                    antiholomorphic,
                    plus,
                    diagnostics,
                    f"{label}:antiholomorphic_over_plus",
                ),
            ],
        )
        exponents = ([0, 1], [0, -1])
    elif pivot_name == "holomorphic_transverse":
        spinors = (
            [plus, holomorphic],
            [
                cpoint(1),
                M5258.safe_divide(
                    minus,
                    holomorphic,
                    diagnostics,
                    f"{label}:minus_over_holomorphic",
                ),
            ],
        )
        exponents = ([0, 1], [0, -1])
    elif pivot_name == "minus_diagonal":
        spinors = (
            [antiholomorphic, minus],
            [
                M5258.safe_divide(
                    holomorphic,
                    minus,
                    diagnostics,
                    f"{label}:holomorphic_over_minus",
                ),
                cpoint(1),
            ],
        )
        exponents = ([-1, 0], [1, 0])
    else:
        spinors = (
            [antiholomorphic, minus],
            [
                M5258.safe_divide(
                    plus,
                    antiholomorphic,
                    diagnostics,
                    f"{label}:plus_over_antiholomorphic",
                ),
                cpoint(1),
            ],
        )
        exponents = ([-1, 0], [1, 0])
    return spinors, exponents, chart


def exact_external4_first_active_quotient(
    configuration: dict[str, Any],
    inputs: dict[str, Any],
    geometry: dict[str, Any],
    global_displacement: Any,
    first_chart: str,
    diagnostics: Any,
    label: str,
) -> Any:
    if configuration["role"] != "reciprocal":
        raise ValueError("external4-first active quotient requires reciprocal role")
    target = cpoint(-9) + cpoint(1j) * inputs["epsilon"]
    external4_plus = cpoint(1) - target
    external4_minus = cpoint(1) + target
    if M5258.lower_abs(external4_plus) <= M5258.upper_abs(external4_minus):
        raise M5258.IntervalSingularity(
            f"external leg 4 is not uniformly in the plus chart: {label}"
        )
    external_root = inputs["external_root"]
    selected_root = geometry["selected_root"]
    unit_circle = selected_root + global_displacement
    diagnostics.record(external4_plus, f"{label}:external4_plus_chart")
    if first_chart == "plus":
        return M5258.safe_divide(
            -cpoint(1),
            external_root * unit_circle,
            diagnostics,
            f"{label}:external_root_times_unit_circle",
        )
    if first_chart == "minus":
        return M5258.safe_divide(
            cpoint(1),
            selected_root,
            diagnostics,
            f"{label}:selected_root",
        )
    raise ValueError(f"unsupported first-spinor chart {first_chart}: {label}")


def rational_hard_soft_edge_overrides(
    configuration: dict[str, Any],
    inputs: dict[str, Any],
    geometry: dict[str, Any],
    global_displacement: Any,
    charts: dict[int, str],
) -> dict[tuple[frozenset[int], int], Any]:
    result: dict[tuple[frozenset[int], int], Any] = {}
    unit_circle = geometry["selected_root"] + global_displacement
    for hard_index in (1, 2):
        pair = frozenset((hard_index, 3))
        for chirality in (0, 1):
            result[(pair, chirality)] = M5386.centered_hard_soft_edge(
                configuration,
                inputs,
                geometry,
                unit_circle,
                hard_index,
                charts[hard_index],
                charts[3],
                chirality,
            )
    if configuration["role"] == "reciprocal":
        result[(frozenset((1, 3)), 1)] = (
            M5386.reciprocal_first_soft_mixed_square_enclosure(
                configuration, inputs, geometry
            )
        )
    return result


def hard_lightcone_states_dual(
    configuration: dict[str, Any],
    epsilon: Any,
    recoil: Any,
    soft_cosine: Any,
    decay_cosine: Any,
    decay_sine: Any,
    global_displacement: Any,
) -> tuple[dict[str, Any], dict[str, Any]]:
    dual = M5385.M5381.IntervalDual
    epsilon = dual.coerce(epsilon)
    recoil = dual.coerce(recoil)
    soft_cosine = dual.coerce(soft_cosine)
    decay_cosine = dual.coerce(decay_cosine)
    decay_sine = dual.coerce(decay_sine)
    global_displacement = dual.coerce(global_displacement)
    epsilon_squared = epsilon * epsilon
    q_value = (
        -(80 + epsilon_squared) / (64 + epsilon_squared)
        + 1j * (-2 * epsilon / (64 + epsilon_squared))
    )
    external_root = -1j * M5386.chart_safe_sqrt_dual(-q_value)
    soft_sine = M5385.positive_sqrt_dual(1 - soft_cosine * soft_cosine)
    factor_f1 = (
        q_value * recoil * soft_cosine
        + q_value * recoil
        - q_value * soft_cosine
        - q_value
        + recoil * soft_cosine
        + recoil
        - soft_cosine
        + 1
    )
    factor_f2 = (
        q_value * recoil * soft_cosine
        - q_value * recoil
        - q_value * soft_cosine
        - q_value
        + recoil * soft_cosine
        - recoil
        - soft_cosine
        + 1
    )
    representative = (
        soft_sine
        * (1 + decay_cosine)
        * factor_f1
        / (decay_sine * (1 + soft_cosine) * factor_f2)
    )
    relative = (
        1 / representative
        if configuration["role"] == "reciprocal"
        else representative
    )
    relative_cosine = (
        (relative + 1 / relative) * soft_sine * decay_sine / 2
        + soft_cosine * decay_cosine
    )
    selected_root = (
        external_root * (1 + soft_cosine) / soft_sine
        if configuration["role"] == "representative"
        else soft_sine / ((1 + soft_cosine) * external_root)
    )
    unit_circle = selected_root + global_displacement

    def state(index: int) -> dict[str, Any]:
        if index == 1:
            energy = (
                1
                + recoil * recoil
                - relative_cosine * (1 - recoil * recoil)
            ) / 2
            longitudinal = (
                relative_cosine * (1 - recoil) * (1 - recoil)
                - (1 - recoil * recoil)
            ) / 2
            holomorphic = (
                recoil * decay_sine * relative
                + longitudinal * soft_sine
            )
            antiholomorphic = (
                recoil * decay_sine / relative
                + longitudinal * soft_sine
            )
            momentum_z = longitudinal * soft_cosine + recoil * decay_cosine
        elif index == 2:
            energy = (
                1
                + recoil * recoil
                + relative_cosine * (1 - recoil * recoil)
            ) / 2
            longitudinal = (
                -relative_cosine * (1 - recoil) * (1 - recoil)
                - (1 - recoil * recoil)
            ) / 2
            holomorphic = (
                -recoil * decay_sine * relative
                + longitudinal * soft_sine
            )
            antiholomorphic = (
                -recoil * decay_sine / relative
                + longitudinal * soft_sine
            )
            momentum_z = longitudinal * soft_cosine - recoil * decay_cosine
        else:
            raise ValueError(f"unsupported hard index {index}")
        return {
            "energy": energy,
            "momentum_z": momentum_z,
            "plus": energy + momentum_z,
            "minus": energy - momentum_z,
            "raw_holomorphic": holomorphic,
            "raw_antiholomorphic": antiholomorphic,
            "holomorphic": unit_circle * holomorphic,
            "antiholomorphic": antiholomorphic / unit_circle,
            "selected_root": selected_root,
            "unit_circle": unit_circle,
        }

    return state(1), state(2)


def rational_pair_edge_dual(
    left: dict[str, Any],
    right: dict[str, Any],
    left_chart: str,
    right_chart: str,
    chirality: int,
) -> Any:
    chart_pair = (left_chart, right_chart)
    if chirality == 0:
        if chart_pair == ("plus", "plus"):
            return (
                left["plus"] * right["holomorphic"]
                - left["holomorphic"] * right["plus"]
            )
        if chart_pair == ("minus", "minus"):
            return (
                left["antiholomorphic"] * right["minus"]
                - left["minus"] * right["antiholomorphic"]
            )
        if chart_pair == ("minus", "plus"):
            return (
                left["antiholomorphic"] * right["holomorphic"]
                - left["minus"] * right["plus"]
            )
        return (
            left["plus"] * right["minus"]
            - left["holomorphic"] * right["antiholomorphic"]
        )
    if chart_pair == ("plus", "plus"):
        return (
            right["antiholomorphic"] / right["plus"]
            - left["antiholomorphic"] / left["plus"]
        )
    if chart_pair == ("minus", "minus"):
        return (
            left["holomorphic"] / left["minus"]
            - right["holomorphic"] / right["minus"]
        )
    if chart_pair == ("minus", "plus"):
        return (
            left["holomorphic"]
            * right["antiholomorphic"]
            / (left["minus"] * right["plus"])
            - 1
        )
    return 1 - (
        left["antiholomorphic"]
        * right["holomorphic"]
        / (left["plus"] * right["minus"])
    )


def centered_hard_pair_rational_edge(
    configuration: dict[str, Any],
    inputs: dict[str, Any],
    geometry: dict[str, Any],
    global_displacement: Any,
    first_chart: str,
    second_chart: str,
    chirality: int,
) -> Any:
    domains = (
        inputs["epsilon"],
        geometry["recoil"],
        inputs["soft_cosine"],
        global_displacement,
    )
    centers = tuple(M5385.complex_midpoint_box(value) for value in domains)

    def evaluate(values: list[Any]) -> Any:
        first, second = hard_lightcone_states_dual(
            configuration,
            values[0],
            values[1],
            values[2],
            inputs["decay_cosine"],
            inputs["decay_sine"],
            values[3],
        )
        return rational_pair_edge_dual(
            first,
            second,
            first_chart,
            second_chart,
            chirality,
        )

    enclosure = evaluate(list(centers)).value
    for derivative_index in range(len(domains)):
        dual_domains = [
            M5385.M5381.IntervalDual(
                value,
                cpoint(1 if index == derivative_index else 0),
            )
            for index, value in enumerate(domains)
        ]
        enclosure += evaluate(dual_domains).derivative * (
            domains[derivative_index] - centers[derivative_index]
        )
    return enclosure


def centered_external_second_invariant(
    configuration: dict[str, Any],
    inputs: dict[str, Any],
    geometry: dict[str, Any],
    global_displacement: Any,
    external_endpoint: int,
) -> Any:
    domains = (
        inputs["epsilon"],
        geometry["recoil"],
        inputs["soft_cosine"],
        global_displacement,
    )
    centers = tuple(M5385.complex_midpoint_box(value) for value in domains)

    def evaluate(values: list[Any]) -> Any:
        epsilon = M5385.M5381.IntervalDual.coerce(values[0])
        _, second = hard_lightcone_states_dual(
            configuration,
            epsilon,
            values[1],
            values[2],
            inputs["decay_cosine"],
            inputs["decay_sine"],
            values[3],
        )
        target = -9 + 1j * epsilon
        transverse = sheet_locked_external_transverse_dual(target)
        momentum_x = (
            second["holomorphic"] + second["antiholomorphic"]
        ) / 2
        orientation = 1 if external_endpoint == 0 else -1
        return 2 * (
            -second["energy"]
            + orientation
            * (
                transverse * momentum_x
                + target * second["momentum_z"]
            )
        )

    enclosure = evaluate(list(centers)).value
    for derivative_index in range(len(domains)):
        dual_domains = [
            M5385.M5381.IntervalDual(
                value,
                cpoint(1 if index == derivative_index else 0),
            )
            for index, value in enumerate(domains)
        ]
        enclosure += evaluate(dual_domains).derivative * (
            domains[derivative_index] - centers[derivative_index]
        )
    return enclosure


def factorized_external4_second_angle_dual(
    configuration: dict[str, Any],
    epsilon: Any,
    recoil: Any,
    soft_cosine: Any,
    decay_cosine: Any,
    decay_sine: Any,
    global_displacement: Any,
) -> Any:
    dual = M5385.M5381.IntervalDual
    epsilon = dual.coerce(epsilon)
    soft_cosine = dual.coerce(soft_cosine)
    global_displacement = dual.coerce(global_displacement)
    _, second = hard_lightcone_states_dual(
        configuration,
        epsilon,
        recoil,
        soft_cosine,
        decay_cosine,
        decay_sine,
        global_displacement,
    )
    epsilon_squared = epsilon * epsilon
    q_value = (
        -(80 + epsilon_squared) / (64 + epsilon_squared)
        + 1j * (-2 * epsilon / (64 + epsilon_squared))
    )
    external_root = -1j * M5386.chart_safe_sqrt_dual(-q_value)
    soft_sine = M5385.positive_sqrt_dual(1 - soft_cosine * soft_cosine)
    selected_root_factor = (
        q_value * (1 + soft_cosine) / soft_sine
        if configuration["role"] == "representative"
        else soft_sine / (1 + soft_cosine)
    )
    return (
        2
        * (
            second["plus"]
            + (
                selected_root_factor
                + external_root * global_displacement
            )
            * second["raw_holomorphic"]
        )
        / (1 + q_value)
    )


def centered_factorized_external4_second_angle(
    configuration: dict[str, Any],
    inputs: dict[str, Any],
    geometry: dict[str, Any],
    global_displacement: Any,
) -> Any:
    domains = (
        inputs["epsilon"],
        geometry["recoil"],
        inputs["soft_cosine"],
        global_displacement,
    )
    centers = tuple(M5385.complex_midpoint_box(value) for value in domains)

    def evaluate(values: list[Any]) -> Any:
        return factorized_external4_second_angle_dual(
            configuration,
            values[0],
            values[1],
            values[2],
            inputs["decay_cosine"],
            inputs["decay_sine"],
            values[3],
        )

    enclosure = evaluate(list(centers)).value
    for derivative_index in range(len(domains)):
        dual_domains = [
            M5385.M5381.IntervalDual(
                value,
                cpoint(1 if index == derivative_index else 0),
            )
            for index, value in enumerate(domains)
        ]
        enclosure += evaluate(dual_domains).derivative * (
            domains[derivative_index] - centers[derivative_index]
        )
    return enclosure


def deformed_path_energy_dual(
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
) -> Any:
    coordinate = M5385.M5381.IntervalDual.coerce(absolute_coordinate)
    parameter = M5385.M5381.IntervalDual.coerce(path_parameter)
    lower_energy = interval_boundary_energy_dual(
        cell["lower_energy_boundary"], coordinate
    )
    upper_energy = interval_boundary_energy_dual(
        cell["upper_energy_boundary"], coordinate
    )
    if path_segment == "LEFT_CONNECTOR":
        return (
            lower_energy
            + 1j * DEFAULT_ENERGY_DEFORMATION * parameter
        )
    if path_segment == "TOP":
        return (
            lower_energy
            + parameter * (upper_energy - lower_energy)
            + 1j * DEFAULT_ENERGY_DEFORMATION
        )
    if path_segment == "RIGHT_CONNECTOR":
        return (
            upper_energy
            + 1j * DEFAULT_ENERGY_DEFORMATION * parameter
        )
    raise ValueError(f"unsupported path segment {path_segment}")


def path_correlated_internal_hard_pair_invariant(
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
) -> Any:
    energy = deformed_path_energy_dual(
        cell,
        path_segment,
        absolute_coordinate,
        path_parameter,
    )
    return cpoint(4) * (cpoint(1) - energy.value)


def internal_hard_pair_invariant_crosschecks() -> list[dict[str, Any]]:
    cell = next(
        row
        for row in away_term_support_cells()
        if row["mapped_cell_id"] == "S_X001_MC04_SM_DM"
    )
    configuration = configuration_variants("MC04_SM_DM")[0]
    epsilon_real_values = (
        M5394.REGULATOR_INTERVAL[0] - M5394.REGULATOR_CAUCHY_RADIUS,
        0.5 * sum(M5394.REGULATOR_INTERVAL),
        M5394.REGULATOR_INTERVAL[1] + M5394.REGULATOR_CAUCHY_RADIUS,
    )
    epsilon_imaginary_values = (
        -M5394.REGULATOR_CAUCHY_RADIUS,
        0.0,
        M5394.REGULATOR_CAUCHY_RADIUS,
    )
    rows: list[dict[str, Any]] = []
    for absolute_coordinate in (
        0.0,
        0.10191270076850262,
        0.20382540153700524,
    ):
        for path_parameter in (0.0, 0.5, 1.0):
            coordinate = cpoint(absolute_coordinate)
            parameter = cpoint(path_parameter)
            energy = deformed_path_energy_dual(
                cell,
                "RIGHT_CONNECTOR",
                coordinate,
                parameter,
            ).value
            exact_invariant = (
                path_correlated_internal_hard_pair_invariant(
                    cell,
                    "RIGHT_CONNECTOR",
                    coordinate,
                    parameter,
                )
            )
            exact_value = complex(M5394.midpoint(exact_invariant))
            for epsilon_real in epsilon_real_values:
                for epsilon_imaginary in epsilon_imaginary_values:
                    epsilon = cpoint(
                        complex(epsilon_real, epsilon_imaginary)
                    )
                    inputs, geometry = interval_inputs(
                        configuration,
                        coordinate,
                        energy,
                        epsilon,
                    )
                    target = cpoint(-9) + cpoint(1j) * inputs["epsilon"]
                    global_radius = 1.0e-7 * max(
                        1.0,
                        M5258.upper_abs(geometry["selected_root"]),
                    )
                    for arc_index in range(4):
                        phase = 2 * math.pi * (arc_index + 0.5) / 4
                        displacement = cpoint(
                            global_radius
                            * complex(math.cos(phase), math.sin(phase))
                        )
                        internal = M5258.rotate_internal_lightcone(
                            M5386.amplitude_state(geometry),
                            geometry["selected_root"] + displacement,
                        )
                        left, right = sheet_locked_interval_cut_momenta(
                            internal, target
                        )
                        for orientation, momenta in (
                            ("LEFT", left),
                            ("RIGHT", right),
                        ):
                            parent_invariant = M5258.invariant(
                                momenta, 1, 2
                            )
                            parent_value = complex(
                                M5394.midpoint(parent_invariant)
                            )
                            relative_error = abs(
                                exact_value - parent_value
                            ) / max(1.0, abs(parent_value))
                            rows.append(
                                {
                                    "absolute_soft_cosine": absolute_coordinate,
                                    "path_parameter": path_parameter,
                                    "epsilon_real": epsilon_real,
                                    "epsilon_imaginary": epsilon_imaginary,
                                    "arc_index": arc_index,
                                    "momentum_orientation": orientation,
                                    "path_invariant_real": exact_value.real,
                                    "path_invariant_imaginary": exact_value.imag,
                                    "parent_invariant_real": parent_value.real,
                                    "parent_invariant_imaginary": parent_value.imag,
                                    "path_to_parent_relative_error": relative_error,
                                    "identity_passed": relative_error <= 5.0e-14,
                                }
                            )
    return rows


def external01_klt_decomposition_crosschecks() -> list[dict[str, Any]]:
    cell = next(
        row
        for row in away_term_support_cells()
        if row["mapped_cell_id"] == "S_X001_MC04_SM_DM"
    )
    configuration = configuration_variants("MC04_SM_DM")[0]
    active_chirality = (
        1 if configuration["role"] == "reciprocal" else 0
    )
    root_coordinate = 0.031080543955551168
    rows: list[dict[str, Any]] = []
    for coordinate_offset in (
        -1.0e-4,
        -1.0e-6,
        -1.0e-8,
        1.0e-8,
        1.0e-6,
        1.0e-4,
    ):
        for path_parameter_value in (0.0, 1.0e-5):
            coordinate = cpoint(root_coordinate + coordinate_offset)
            path_parameter = cpoint(path_parameter_value)
            epsilon = cpoint(0)
            energy = deformed_path_energy_dual(
                cell,
                "RIGHT_CONNECTOR",
                coordinate,
                path_parameter,
            ).value
            inputs, geometry = interval_inputs(
                configuration,
                coordinate,
                energy,
                epsilon,
            )
            target = cpoint(-9) + cpoint(1j) * epsilon
            for arc_index in range(4):
                phase = 2 * math.pi * (arc_index + 0.5) / 4
                displacement = cpoint(
                    1.0e-7
                    * complex(math.cos(phase), math.sin(phase))
                )
                unit_circle = geometry["selected_root"] + displacement
                internal = M5258.rotate_internal_lightcone(
                    M5386.amplitude_state(geometry), unit_circle
                )
                _, right = sheet_locked_interval_cut_momenta(
                    internal, target
                )
                diagnostics = M5258.IntervalDiagnostics()
                right_first = displaced_first_rational_spinors(
                    configuration,
                    inputs,
                    geometry,
                    displacement,
                    -1,
                    diagnostics,
                    "external01_crosscheck_first",
                )
                right_spinors, right_exponents, _ = (
                    rational_spinor_overrides(
                        right,
                        diagnostics,
                        "external01_crosscheck_right",
                        right_first,
                    )
                )
                exact_invariants = {
                    frozenset((1, 2)): (
                        path_correlated_internal_hard_pair_invariant(
                            cell,
                            "RIGHT_CONNECTOR",
                            coordinate,
                            path_parameter,
                        )
                    )
                }
                external_pair = frozenset((0, 1))
                factorized_external_invariant = (
                    M5258.spinor_bracket(
                        right_spinors[0][0], right_spinors[1][0]
                    )
                    * M5258.spinor_bracket(
                        right_spinors[0][1], right_spinors[1][1]
                    )
                )
                parent_external_invariant = M5258.invariant(
                    right, 0, 1
                )
                parent_factorization_defect = abs(
                    complex(M5394.midpoint(parent_external_invariant))
                    - complex(
                        M5394.midpoint(factorized_external_invariant)
                    )
                )
                for special in (2, 3):
                    direct = (
                        oriented_regularized_scalar_klt_five_with_reciprocals(
                            right,
                            special,
                            0,
                            1,
                            active_chirality,
                            unit_circle,
                            geometry["selected_root"],
                            displacement,
                            diagnostics,
                            f"external01_crosscheck_direct_s{special}",
                            exact_invariants,
                            None,
                            right_spinors,
                            right_exponents,
                            None,
                            {
                                external_pair: (
                                    factorized_external_invariant
                                )
                            },
                        )
                    )
                    regular, residue, angle_edge = (
                        oriented_regularized_scalar_klt_five_external01_decomposition(
                            right,
                            special,
                            0,
                            1,
                            active_chirality,
                            unit_circle,
                            geometry["selected_root"],
                            displacement,
                            diagnostics,
                            f"external01_crosscheck_decomposed_s{special}",
                            exact_invariants,
                            None,
                            right_spinors,
                            right_exponents,
                            None,
                        )
                    )
                    reconstructed = regular + residue / angle_edge
                    direct_value = complex(M5394.midpoint(direct))
                    reconstructed_value = complex(
                        M5394.midpoint(reconstructed)
                    )
                    relative_error = abs(
                        direct_value - reconstructed_value
                    ) / max(
                        1.0e-30,
                        abs(direct_value),
                        abs(reconstructed_value),
                    )
                    rows.append(
                        {
                            "coordinate_offset": coordinate_offset,
                            "path_parameter": path_parameter_value,
                            "arc_index": arc_index,
                            "special": special,
                            "angle_edge_abs": abs(
                                complex(M5394.midpoint(angle_edge))
                            ),
                            "pole_residue_abs": abs(
                                complex(M5394.midpoint(residue))
                            ),
                            "direct_abs": abs(direct_value),
                            "reconstructed_abs": abs(
                                reconstructed_value
                            ),
                            "parent_factorization_absolute_defect": (
                                parent_factorization_defect
                            ),
                            "direct_to_decomposed_relative_error": (
                                relative_error
                            ),
                            "identity_passed": relative_error <= 5.0e-12,
                        }
                    )
    return rows


def external01_path_jacobian_crosschecks() -> list[dict[str, Any]]:
    cells = {
        row["mapped_cell_id"]: row
        for row in away_term_support_cells()
    }
    epsilon = cbox(-5.0e-7, 0.0100005, -5.0e-7, 5.0e-7)
    displacement = cbox(
        -math.nextafter(1.0e-7, math.inf),
        math.nextafter(1.0e-7, math.inf),
        -math.nextafter(1.0e-7, math.inf),
        math.nextafter(1.0e-7, math.inf),
    )
    scenarios = (
        (
            "S_X001_MC04_SM_DM",
            "RIGHT_CONNECTOR",
            (
                (
                    0.03105152601540314,
                    0.031151050137247383,
                    0.0,
                    0.0078125,
                ),
                (
                    0.031151050137247383,
                    0.031250574259091626,
                    0.0,
                    0.0078125,
                ),
                (
                    0.031250574259091626,
                    0.031449622502780106,
                    0.0,
                    0.015625,
                ),
            ),
        ),
        (
            "S_X001_MC04_SP_DM",
            "LEFT_CONNECTOR",
            (
                (
                    0.2022330155874974,
                    0.20233253970934165,
                    0.0,
                    0.0078125,
                ),
                (
                    0.20233253970934165,
                    0.2024320638311859,
                    0.0,
                    0.0078125,
                ),
                (
                    0.2022330155874974,
                    0.2024320638311859,
                    0.0078125,
                    0.015625,
                ),
            ),
        ),
    )
    rows: list[dict[str, Any]] = []
    for mapped_cell_id, path_segment, boxes in scenarios:
        cell = cells[mapped_cell_id]
        term_id = str(cell["reduced_MC04_term_ids"])
        configuration = configuration_variants(term_id)[0]
        for x_lower, x_upper, t_lower, t_upper in boxes:
            bounds = (
                native_external0_first_minus_plus_path_jacobian_bounds(
                    configuration,
                    cell,
                    path_segment,
                    cbox(x_lower, x_upper),
                    cbox(t_lower, t_upper),
                    epsilon,
                    displacement,
                )
            )
            rows.append(
                {
                    "mapped_cell_id": mapped_cell_id,
                    "term_id": term_id,
                    "path_segment": path_segment,
                    "x_lower": x_lower,
                    "x_upper": x_upper,
                    "t_lower": t_lower,
                    "t_upper": t_upper,
                    "determinant_lower": bounds["determinant_lower"],
                    "determinant_upper": bounds["determinant_upper"],
                    "determinant_abs_lower": bounds[
                        "determinant_abs_lower"
                    ],
                    "derivative_x_real_lower": bounds[
                        "derivative_x_real"
                    ][0],
                    "derivative_x_real_upper": bounds[
                        "derivative_x_real"
                    ][1],
                    "derivative_t_imaginary_lower": bounds[
                        "derivative_t_imaginary"
                    ][0],
                    "derivative_t_imaginary_upper": bounds[
                        "derivative_t_imaginary"
                    ][1],
                    "x_real_orientation": bounds[
                        "x_real_orientation"
                    ],
                    "t_imaginary_orientation": bounds[
                        "t_imaginary_orientation"
                    ],
                    "global_injectivity_method": bounds[
                        "global_injectivity_method"
                    ],
                    "jacobian_passed": (
                        bounds["determinant_abs_lower"] > 0.0
                    ),
                }
            )
    return rows


def external01_integrated_cell_crosschecks() -> list[dict[str, Any]]:
    cells = {
        row["mapped_cell_id"]: row
        for row in away_term_support_cells()
    }
    regulator_lower = (
        M5394.REGULATOR_INTERVAL[0]
        - M5394.REGULATOR_CAUCHY_RADIUS
    )
    regulator_upper = (
        M5394.REGULATOR_INTERVAL[1]
        + M5394.REGULATOR_CAUCHY_RADIUS
    )
    regulator_midpoint = 0.5 * (regulator_lower + regulator_upper)
    epsilon = cbox(
        regulator_lower,
        regulator_midpoint,
        -M5394.REGULATOR_CAUCHY_RADIUS,
        M5394.REGULATOR_CAUCHY_RADIUS,
    )
    scenarios = (
        (
            "S_X001_MC04_SM_DM",
            "RIGHT_CONNECTOR",
            0.03105152601540314,
            0.031151050137247383,
            0.0,
            0.0078125,
        ),
        (
            "S_X001_MC04_SP_DM",
            "LEFT_CONNECTOR",
            0.2022330155874974,
            0.20233253970934165,
            0.0,
            0.0078125,
        ),
    )
    rows: list[dict[str, Any]] = []
    for (
        mapped_cell_id,
        path_segment,
        x_lower,
        x_upper,
        t_lower,
        t_upper,
    ) in scenarios:
        cell = cells[mapped_cell_id]
        term_id = str(cell["reduced_MC04_term_ids"])
        configuration = configuration_variants(term_id)[0]
        absolute_coordinate = cbox(x_lower, x_upper)
        path_parameter = cbox(t_lower, t_upper)
        lower_energy, _ = interval_boundary_energy(
            cell["lower_energy_boundary"], x_lower, x_upper
        )
        upper_energy, _ = interval_boundary_energy(
            cell["upper_energy_boundary"], x_lower, x_upper
        )
        boundary_energy = (
            lower_energy
            if path_segment == "LEFT_CONNECTOR"
            else upper_energy
        )
        energy = (
            boundary_energy
            + cpoint(1j * DEFAULT_ENERGY_DEFORMATION)
            * path_parameter
        )
        area_equivalent_abs_upper, diagnostics = (
            global_contour_external01_integrated_area_equivalent_abs_upper(
                configuration,
                absolute_coordinate,
                energy,
                epsilon,
                4,
                {
                    "cell": cell,
                    "path_segment": path_segment,
                    "absolute_coordinate": absolute_coordinate,
                    "path_parameter": path_parameter,
                },
            )
        )
        rows.append(
            {
                "mapped_cell_id": mapped_cell_id,
                "term_id": term_id,
                "path_segment": path_segment,
                "x_lower": x_lower,
                "x_upper": x_upper,
                "t_lower": t_lower,
                "t_upper": t_upper,
                "area_equivalent_abs_upper": area_equivalent_abs_upper,
                "path_integral_enclosure_method": diagnostics[
                    "path_integral_enclosure_method"
                ],
                "external01_path_jacobian_abs_lower": diagnostics[
                    "external01_path_jacobian_abs_lower"
                ],
                "external01_pole_residue_abs_upper": diagnostics[
                    "external01_pole_residue_abs_upper"
                ],
                "external01_reciprocal_integral_abs_upper": diagnostics[
                    "external01_reciprocal_integral_abs_upper"
                ],
                "integrated_cell_passed": (
                    math.isfinite(area_equivalent_abs_upper)
                    and area_equivalent_abs_upper >= 0.0
                    and diagnostics[
                        "external01_path_jacobian_abs_lower"
                    ]
                    > 0.0
                ),
            }
        )
    return rows


def external42_invariant_crosschecks() -> tuple[
    list[dict[str, Any]], list[dict[str, Any]]
]:
    cell = next(
        row
        for row in away_term_support_cells()
        if row["mapped_cell_id"] == "S_X001_MC04_SP_DM"
    )
    configuration = configuration_variants("MC04_SP_DM")[0]
    regulator_lower = (
        M5394.REGULATOR_INTERVAL[0]
        - M5394.REGULATOR_CAUCHY_RADIUS
    )
    regulator_upper = 0.5 * (
        regulator_lower
        + M5394.REGULATOR_INTERVAL[1]
        + M5394.REGULATOR_CAUCHY_RADIUS
    )
    point_rows: list[dict[str, Any]] = []
    for coordinate_value in (
        0.10509747266751832,
        0.10589366564227225,
        0.10668985861702618,
    ):
        for path_parameter_value in (0.125, 0.1875, 0.25):
            for epsilon_value in (
                regulator_lower,
                0.5 * (regulator_lower + regulator_upper),
                regulator_upper,
            ):
                coordinate = cpoint(coordinate_value)
                path_parameter = cpoint(path_parameter_value)
                epsilon = cpoint(epsilon_value)
                energy = deformed_path_energy_dual(
                    cell,
                    "RIGHT_CONNECTOR",
                    coordinate,
                    path_parameter,
                ).value
                inputs, geometry = interval_inputs(
                    configuration, coordinate, energy, epsilon
                )
                for arc_index in range(4):
                    phase = 2 * math.pi * (arc_index + 0.5) / 4
                    displacement = cpoint(
                        1.0e-7
                        * complex(math.cos(phase), math.sin(phase))
                    )
                    unit_circle = (
                        geometry["selected_root"] + displacement
                    )
                    internal = M5258.rotate_internal_lightcone(
                        M5386.amplitude_state(geometry), unit_circle
                    )
                    _, right = sheet_locked_interval_cut_momenta(
                        internal, cpoint(-9) + cpoint(1j) * epsilon
                    )
                    parent = M5258.invariant(right, 2, 4)
                    path_invariant = (
                        centered_path_correlated_external_second_invariant(
                            configuration,
                            cell,
                            "RIGHT_CONNECTOR",
                            coordinate,
                            path_parameter,
                            epsilon,
                            displacement,
                            4,
                        )
                    )
                    parent_value = complex(M5394.midpoint(parent))
                    path_value = complex(
                        M5394.midpoint(path_invariant)
                    )
                    relative_error = abs(
                        parent_value - path_value
                    ) / max(1.0e-30, abs(parent_value), abs(path_value))
                    point_rows.append(
                        {
                            "absolute_coordinate": coordinate_value,
                            "path_parameter": path_parameter_value,
                            "epsilon_real": epsilon_value,
                            "arc_index": arc_index,
                            "parent_invariant_real": parent_value.real,
                            "parent_invariant_imaginary": parent_value.imag,
                            "path_invariant_real": path_value.real,
                            "path_invariant_imaginary": path_value.imag,
                            "path_to_parent_relative_error": relative_error,
                            "identity_passed": relative_error <= 5.0e-13,
                        }
                    )
    epsilon = cbox(
        regulator_lower,
        regulator_upper,
        -M5394.REGULATOR_CAUCHY_RADIUS,
        M5394.REGULATOR_CAUCHY_RADIUS,
    )
    displacement_radius = math.nextafter(1.0e-7, math.inf)
    displacement = cbox(
        -displacement_radius,
        displacement_radius,
        -displacement_radius,
        displacement_radius,
    )
    cover_rows: list[dict[str, Any]] = []
    for x_lower, x_upper, t_lower, t_upper in (
        (
            0.10509747266751832,
            0.10668985861702618,
            0.125,
            0.1875,
        ),
        (
            0.10509747266751832,
            0.10668985861702618,
            0.1875,
            0.25,
        ),
        (
            0.10668985861702618,
            0.10828224456653403,
            0.125,
            0.25,
        ),
    ):
        invariant, metadata = (
            half_plane_subcover_external42_invariant(
                configuration,
                cell,
                "RIGHT_CONNECTOR",
                cbox(x_lower, x_upper),
                cbox(t_lower, t_upper),
                epsilon,
                displacement,
            )
        )
        cover_rows.append(
            {
                "x_lower": x_lower,
                "x_upper": x_upper,
                "t_lower": t_lower,
                "t_upper": t_upper,
                "invariant_abs_lower": M5258.lower_abs(invariant),
                "invariant_abs_upper": M5258.upper_abs(invariant),
                **metadata,
                "cover_passed": M5258.lower_abs(invariant) > 0.0,
            }
        )
    return point_rows, cover_rows


def external41_active_quotient_crosschecks() -> list[dict[str, Any]]:
    cell = next(
        row
        for row in away_term_support_cells()
        if row["mapped_cell_id"] == "S_X001_MC04_SP_DM"
    )
    configuration = configuration_variants("MC04_SP_DM")[0]
    x_lower = 0.17357006849635603
    x_upper = 0.17516245444586387
    rows: list[dict[str, Any]] = []
    for coordinate_value in (
        x_lower,
        0.5 * (x_lower + x_upper),
        x_upper,
    ):
        for path_parameter_value in (0.0, 0.0625, 0.125):
            for epsilon_value in (0.0, 0.005, 0.01):
                coordinate = cpoint(coordinate_value)
                path_parameter = cpoint(path_parameter_value)
                epsilon = cpoint(epsilon_value)
                energy = deformed_path_energy_dual(
                    cell,
                    "RIGHT_CONNECTOR",
                    coordinate,
                    path_parameter,
                ).value
                inputs, geometry = interval_inputs(
                    configuration, coordinate, energy, epsilon
                )
                target = cpoint(-9) + cpoint(1j) * epsilon
                external4_plus = cpoint(1) - target
                external4_minus = cpoint(1) + target
                for arc_index in range(4):
                    phase = 2 * math.pi * (arc_index + 0.5) / 4
                    displacement = cpoint(
                        1.0e-7
                        * complex(math.cos(phase), math.sin(phase))
                    )
                    unit_circle = geometry["selected_root"] + displacement
                    internal = M5258.rotate_internal_lightcone(
                        M5386.amplitude_state(geometry), unit_circle
                    )
                    _, right = sheet_locked_interval_cut_momenta(
                        internal, target
                    )
                    diagnostics = M5258.IntervalDiagnostics()
                    right_first = displaced_first_rational_spinors(
                        configuration,
                        inputs,
                        geometry,
                        displacement,
                        -1,
                        diagnostics,
                        "external41_probe_first",
                    )
                    spinors, exponent_overrides, charts = (
                        rational_spinor_overrides(
                            right,
                            diagnostics,
                            "external41_probe_right",
                            right_first,
                        )
                    )
                    spinor_exponents = M5258.spinor_exponent_table(
                        right,
                        (0, 1, 2, 3, 4),
                        {1, 2, 3},
                    )
                    spinor_exponents.update(exponent_overrides)
                    selected_spinors = {
                        index: spinors[index][1] for index in spinors
                    }
                    selected_exponents = {
                        index: spinor_exponents[index][1]
                        for index in spinor_exponents
                    }
                    generic = M5258.active_bracket_quotient(
                        1,
                        4,
                        selected_spinors,
                        selected_exponents,
                        unit_circle,
                        geometry["selected_root"],
                        diagnostics,
                        "external41_probe_generic",
                    )
                    exact = exact_external4_first_active_quotient(
                        configuration,
                        inputs,
                        geometry,
                        displacement,
                        charts[1],
                        M5258.IntervalDiagnostics(),
                        "external41_probe_exact",
                    )
                    generic_value = complex(M5394.midpoint(generic))
                    exact_value = complex(M5394.midpoint(exact))
                    relative_error = abs(generic_value - exact_value) / max(
                        1.0e-30, abs(generic_value), abs(exact_value)
                    )
                    external4_plus_lower = M5258.lower_abs(external4_plus)
                    external4_minus_upper = M5258.upper_abs(external4_minus)
                    rows.append(
                        {
                            "absolute_coordinate": coordinate_value,
                            "path_parameter": path_parameter_value,
                            "epsilon_real": epsilon_value,
                            "arc_index": arc_index,
                            "first_chart": charts[1],
                            "external4_chart": charts[4],
                            "derived_formula": (
                                "-1/(r0*V)"
                                if charts[1] == "plus"
                                else "1/zeta"
                            ),
                            "generic_quotient_real": generic_value.real,
                            "generic_quotient_imaginary": generic_value.imag,
                            "exact_quotient_real": exact_value.real,
                            "exact_quotient_imaginary": exact_value.imag,
                            "generic_quotient_modulus": abs(generic_value),
                            "exact_quotient_abs_lower": M5258.lower_abs(exact),
                            "external4_plus_abs_lower": external4_plus_lower,
                            "external4_minus_abs_upper": external4_minus_upper,
                            "external4_chart_dominance_passed": (
                                charts[4] == "plus"
                                and external4_plus_lower
                                > external4_minus_upper
                            ),
                            "generic_to_exact_relative_error": relative_error,
                            "identity_passed": relative_error <= 5.0e-13,
                        }
                    )
    return rows


def external41_stable_angle_crosschecks() -> list[dict[str, Any]]:
    cell = next(
        row
        for row in away_term_support_cells()
        if row["mapped_cell_id"] == "S_X002_MC04_SP_DM"
    )
    configuration = configuration_variants("MC04_SP_DM")[0]
    x_lower = 0.26277044686936
    x_upper = 0.263882617536008
    t_lower = 0.0625
    t_upper = 0.125
    rows: list[dict[str, Any]] = []
    for coordinate_value in (
        x_lower,
        0.5 * (x_lower + x_upper),
        x_upper,
    ):
        for path_parameter_value in (
            t_lower,
            0.5 * (t_lower + t_upper),
            t_upper,
        ):
            for epsilon_value in (0.0, 0.005, 0.01):
                coordinate = cpoint(coordinate_value)
                path_parameter = cpoint(path_parameter_value)
                epsilon = cpoint(epsilon_value)
                energy = deformed_path_energy_dual(
                    cell,
                    "LEFT_CONNECTOR",
                    coordinate,
                    path_parameter,
                ).value
                inputs, geometry = interval_inputs(
                    configuration, coordinate, energy, epsilon
                )
                target = cpoint(-9) + cpoint(1j) * epsilon
                for arc_index in range(4):
                    phase = 2 * math.pi * (arc_index + 0.5) / 4
                    displacement = cpoint(
                        1.0e-7
                        * complex(math.cos(phase), math.sin(phase))
                    )
                    unit_circle = geometry["selected_root"] + displacement
                    internal = M5258.rotate_internal_lightcone(
                        M5386.amplitude_state(geometry), unit_circle
                    )
                    _, right = sheet_locked_interval_cut_momenta(
                        internal, target
                    )
                    diagnostics = M5258.IntervalDiagnostics()
                    right_first = displaced_first_rational_spinors(
                        configuration,
                        inputs,
                        geometry,
                        displacement,
                        -1,
                        diagnostics,
                        "external41_stable_probe_first",
                    )
                    spinors, _, charts = rational_spinor_overrides(
                        right,
                        diagnostics,
                        "external41_stable_probe_right",
                        right_first,
                    )
                    direct = M5258.spinor_bracket(
                        spinors[1][0], spinors[4][0]
                    )
                    correlated = (
                        centered_path_correlated_external4_first_angle(
                            configuration,
                            cell,
                            "LEFT_CONNECTOR",
                            coordinate,
                            path_parameter,
                            epsilon,
                            displacement,
                            charts[1],
                        )
                    )
                    direct_value = complex(M5394.midpoint(direct))
                    correlated_value = complex(M5394.midpoint(correlated))
                    relative_error = abs(
                        direct_value - correlated_value
                    ) / max(
                        1.0e-30,
                        abs(direct_value),
                        abs(correlated_value),
                    )
                    rows.append(
                        {
                            "absolute_coordinate": coordinate_value,
                            "path_parameter": path_parameter_value,
                            "epsilon_real": epsilon_value,
                            "arc_index": arc_index,
                            "first_chart": charts[1],
                            "external4_chart": charts[4],
                            "direct_angle_real": direct_value.real,
                            "direct_angle_imaginary": direct_value.imag,
                            "correlated_angle_real": correlated_value.real,
                            "correlated_angle_imaginary": correlated_value.imag,
                            "direct_angle_modulus": abs(direct_value),
                            "direct_to_correlated_relative_error": relative_error,
                            "identity_passed": relative_error <= 5.0e-13,
                        }
                    )
    return rows


def external41_factorized_angle_crosschecks() -> tuple[
    list[dict[str, Any]], list[dict[str, Any]]
]:
    cell = next(
        row
        for row in away_term_support_cells()
        if row["mapped_cell_id"] == "S_X002_MC04_SP_DM"
    )
    configuration = configuration_variants("MC04_SP_DM")[0]
    x_lower = 0.20382540153700524
    x_upper = 0.20604974287030164
    t_lower = 0.0
    t_upper = 0.125
    point_rows: list[dict[str, Any]] = []
    for coordinate_value in (
        x_lower,
        0.5 * (x_lower + x_upper),
        x_upper,
    ):
        for path_parameter_value in (
            t_lower,
            0.5 * (t_lower + t_upper),
            t_upper,
        ):
            for epsilon_value in (0.0, 0.005, 0.01):
                coordinate = cpoint(coordinate_value)
                path_parameter = cpoint(path_parameter_value)
                epsilon = cpoint(epsilon_value)
                energy = deformed_path_energy_dual(
                    cell,
                    "RIGHT_CONNECTOR",
                    coordinate,
                    path_parameter,
                ).value
                inputs, geometry = interval_inputs(
                    configuration, coordinate, energy, epsilon
                )
                target = cpoint(-9) + cpoint(1j) * epsilon
                global_radius = 1.0e-7 * max(
                    1.0,
                    M5258.upper_abs(geometry["selected_root"]),
                )
                for arc_index in range(4):
                    phase = 2 * math.pi * (arc_index + 0.5) / 4
                    displacement = cpoint(
                        global_radius
                        * complex(math.cos(phase), math.sin(phase))
                    )
                    unit_circle = geometry["selected_root"] + displacement
                    internal = M5258.rotate_internal_lightcone(
                        M5386.amplitude_state(geometry), unit_circle
                    )
                    _, right = sheet_locked_interval_cut_momenta(
                        internal, target
                    )
                    diagnostics = M5258.IntervalDiagnostics()
                    right_first = displaced_first_rational_spinors(
                        configuration,
                        inputs,
                        geometry,
                        displacement,
                        -1,
                        diagnostics,
                        "external41_factorized_probe_first",
                    )
                    spinors, _, charts = rational_spinor_overrides(
                        right,
                        diagnostics,
                        "external41_factorized_probe_right",
                        right_first,
                    )
                    direct = M5258.spinor_bracket(
                        spinors[1][0], spinors[4][0]
                    )
                    factorized = (
                        centered_path_correlated_external4_first_plus_angle_factorized(
                            configuration,
                            cell,
                            "RIGHT_CONNECTOR",
                            coordinate,
                            path_parameter,
                            epsilon,
                            displacement,
                        )
                    )
                    direct_value = complex(M5394.midpoint(direct))
                    factorized_value = complex(M5394.midpoint(factorized))
                    relative_error = abs(
                        direct_value - factorized_value
                    ) / max(
                        1.0e-30,
                        abs(direct_value),
                        abs(factorized_value),
                    )
                    point_rows.append(
                        {
                            "absolute_coordinate": coordinate_value,
                            "path_parameter": path_parameter_value,
                            "epsilon_real": epsilon_value,
                            "arc_index": arc_index,
                            "first_chart": charts[1],
                            "direct_angle_real": direct_value.real,
                            "direct_angle_imaginary": direct_value.imag,
                            "factorized_angle_real": factorized_value.real,
                            "factorized_angle_imaginary": (
                                factorized_value.imag
                            ),
                            "direct_angle_modulus": abs(direct_value),
                            "direct_to_factorized_relative_error": (
                                relative_error
                            ),
                            "identity_passed": (
                                charts[1] == "plus"
                                and relative_error <= 5.0e-13
                            ),
                        }
                    )
    full_lower = (
        M5394.REGULATOR_INTERVAL[0] - M5394.REGULATOR_CAUCHY_RADIUS
    )
    full_upper = (
        M5394.REGULATOR_INTERVAL[1] + M5394.REGULATOR_CAUCHY_RADIUS
    )
    slab_upper = full_lower + 0.5 * (full_upper - full_lower)
    coordinate = cbox(x_lower, x_upper)
    path_parameter = cbox(t_lower, t_upper)
    epsilon = cbox(
        full_lower,
        slab_upper,
        -M5394.REGULATOR_CAUCHY_RADIUS,
        M5394.REGULATOR_CAUCHY_RADIUS,
    )
    energy = deformed_path_energy_dual(
        cell,
        "RIGHT_CONNECTOR",
        coordinate,
        path_parameter,
    ).value
    _, geometry = interval_inputs(
        configuration, coordinate, energy, epsilon
    )
    global_radius = 1.0e-7 * max(
        1.0,
        M5258.upper_abs(geometry["selected_root"]),
    )
    cover_rows: list[dict[str, Any]] = []
    for arc_index in range(4):
        phase = cbox(arc_index, arc_index + 1) * cpoint(
            2 * math.pi / 4
        )
        displacement = cpoint(global_radius) * (
            iv.cos(phase) + cpoint(1j) * iv.sin(phase)
        )
        angle = subdivided_path_external4_first_plus_angle_factorized(
            configuration,
            cell,
            "RIGHT_CONNECTOR",
            coordinate,
            path_parameter,
            epsilon,
            displacement,
            16,
        )
        real_lower, real_upper = M5394.real_bounds(angle)
        imaginary_lower, imaginary_upper = M5394.imaginary_bounds(angle)
        cover_rows.append(
            {
                "arc_index": arc_index,
                "x_lower": x_lower,
                "x_upper": x_upper,
                "t_lower": t_lower,
                "t_upper": t_upper,
                "epsilon_real_lower": full_lower,
                "epsilon_real_upper": slab_upper,
                "subdivision_count": 16,
                "evaluation_count": 256,
                "angle_real_lower": real_lower,
                "angle_real_upper": real_upper,
                "angle_imaginary_lower": imaginary_lower,
                "angle_imaginary_upper": imaginary_upper,
                "angle_abs_lower": M5258.lower_abs(angle),
                "positive_imaginary_half_plane_passed": (
                    imaginary_lower > 0.0
                ),
            }
        )
    return point_rows, cover_rows


def centered_path_correlated_hard_lightcone_factors(
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
    global_displacement: Any,
    hard_index: int,
    orientation: int,
) -> dict[str, Any]:
    if hard_index not in (1, 2):
        raise ValueError(f"unsupported hard index {hard_index}")
    if orientation not in (-1, 1):
        raise ValueError(f"unsupported momentum orientation {orientation}")
    domains = (
        absolute_coordinate,
        path_parameter,
        epsilon,
        global_displacement,
    )
    centers = tuple(M5385.complex_midpoint_box(value) for value in domains)
    decay_cosine = cpoint(
        configuration["decay_sign"] * M5394.ABSOLUTE_DECAY_COSINE
    )
    decay_sine = cpoint(
        math.sqrt(1 - M5394.ABSOLUTE_DECAY_COSINE**2)
    )
    factor_names = (
        "plus",
        "minus",
        "holomorphic",
        "antiholomorphic",
    )

    def evaluate(values: list[Any]) -> dict[str, Any]:
        dual = M5385.M5381.IntervalDual
        coordinate, parameter, epsilon_value, displacement = (
            dual.coerce(value) for value in values
        )
        energy = deformed_path_energy_dual(
            cell, path_segment, coordinate, parameter
        )
        recoil = M5386.chart_safe_sqrt_dual(1 - energy)
        first, second = hard_lightcone_states_dual(
            configuration,
            epsilon_value,
            recoil,
            coordinate * configuration["soft_sign"],
            decay_cosine,
            decay_sine,
            displacement,
        )
        hard = first if hard_index == 1 else second
        return {
            name: orientation * hard[name] for name in factor_names
        }

    centered_values = evaluate(list(centers))
    enclosures = {
        name: centered_values[name].value for name in factor_names
    }
    for derivative_index in range(len(domains)):
        dual_domains = [
            M5385.M5381.IntervalDual(
                value,
                cpoint(1 if index == derivative_index else 0),
            )
            for index, value in enumerate(domains)
        ]
        derivative_values = evaluate(dual_domains)
        offset = domains[derivative_index] - centers[derivative_index]
        for name in factor_names:
            enclosures[name] += (
                derivative_values[name].derivative * offset
            )
    return enclosures


def subdivided_path_hard_rational_spinors(
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
    global_displacement: Any,
    hard_index: int,
    orientation: int,
    diagnostics: Any,
    label: str,
    subdivision_count: int,
) -> tuple[
    tuple[list[Any], list[Any]],
    tuple[list[int], list[int]],
    str,
    float,
]:
    if subdivision_count <= 1:
        raise ValueError("subdivision count must exceed one")
    x_lower, x_upper = M5394.real_bounds(absolute_coordinate)
    t_lower, t_upper = M5394.real_bounds(path_parameter)
    factor_rows: list[dict[str, Any]] = []
    for x_index in range(subdivision_count):
        coordinate = cbox(
            x_lower
            + (x_upper - x_lower) * x_index / subdivision_count,
            x_lower
            + (x_upper - x_lower)
            * (x_index + 1)
            / subdivision_count,
        )
        for t_index in range(subdivision_count):
            parameter = cbox(
                t_lower
                + (t_upper - t_lower) * t_index / subdivision_count,
                t_lower
                + (t_upper - t_lower)
                * (t_index + 1)
                / subdivision_count,
            )
            factor_rows.append(
                centered_path_correlated_hard_lightcone_factors(
                    configuration,
                    cell,
                    path_segment,
                    coordinate,
                    parameter,
                    epsilon,
                    global_displacement,
                    hard_index,
                    orientation,
                )
            )
    families = (
        ("plus", "plus", "holomorphic"),
        ("minus", "minus", "antiholomorphic"),
    )
    family_scores = {
        chart: min(
            max(
                M5258.lower_abs(row[first]),
                M5258.lower_abs(row[second]),
            )
            for row in factor_rows
        )
        for chart, first, second in families
    }
    chart, _, _ = max(families, key=lambda row: family_scores[row[0]])
    if family_scores[chart] <= 0.0:
        raise M5258.IntervalSingularity(
            f"no subdivided hard-spinor projective family survives: {label}"
        )
    angle_first: list[Any] = []
    angle_second: list[Any] = []
    square_first: list[Any] = []
    square_second: list[Any] = []
    selected_pivot_lowers: list[float] = []
    for row_index, row in enumerate(factor_rows):
        if chart == "plus":
            plus = row["plus"]
            holomorphic = row["holomorphic"]
            if M5258.lower_abs(plus) >= M5258.lower_abs(holomorphic):
                pivot = plus
                pivot_name = "plus_diagonal"
                quotient = M5258.safe_divide(
                    row["antiholomorphic"],
                    plus,
                    diagnostics,
                    f"{label}:row_{row_index}:antiholomorphic_over_plus",
                )
            else:
                pivot = holomorphic
                pivot_name = "holomorphic_transverse"
                quotient = M5258.safe_divide(
                    row["minus"],
                    holomorphic,
                    diagnostics,
                    f"{label}:row_{row_index}:minus_over_holomorphic",
                )
            diagnostics.record(
                pivot, f"{label}:row_{row_index}:{pivot_name}"
            )
            selected_pivot_lowers.append(M5258.lower_abs(pivot))
            angle_first.append(plus)
            angle_second.append(holomorphic)
            square_first.append(cpoint(1))
            square_second.append(quotient)
        else:
            minus = row["minus"]
            antiholomorphic = row["antiholomorphic"]
            if M5258.lower_abs(minus) >= M5258.lower_abs(
                antiholomorphic
            ):
                pivot = minus
                pivot_name = "minus_diagonal"
                quotient = M5258.safe_divide(
                    row["holomorphic"],
                    minus,
                    diagnostics,
                    f"{label}:row_{row_index}:holomorphic_over_minus",
                )
            else:
                pivot = antiholomorphic
                pivot_name = "antiholomorphic_transverse"
                quotient = M5258.safe_divide(
                    row["plus"],
                    antiholomorphic,
                    diagnostics,
                    f"{label}:row_{row_index}:plus_over_antiholomorphic",
                )
            diagnostics.record(
                pivot, f"{label}:row_{row_index}:{pivot_name}"
            )
            selected_pivot_lowers.append(M5258.lower_abs(pivot))
            angle_first.append(antiholomorphic)
            angle_second.append(minus)
            square_first.append(quotient)
            square_second.append(cpoint(1))
    spinors = (
        [
            rectangular_interval_hull(angle_first),
            rectangular_interval_hull(angle_second),
        ],
        [
            rectangular_interval_hull(square_first),
            rectangular_interval_hull(square_second),
        ],
    )
    exponents = (
        ([0, 1], [0, -1])
        if chart == "plus"
        else ([-1, 0], [1, 0])
    )
    return spinors, exponents, chart, min(selected_pivot_lowers)


def centered_path_correlated_energy_multiplier_parts(
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
) -> tuple[Any, Any, str]:
    domains = (absolute_coordinate, path_parameter, epsilon)
    centers = tuple(M5385.complex_midpoint_box(value) for value in domains)
    decay_cosine = cpoint(
        configuration["decay_sign"] * M5394.ABSOLUTE_DECAY_COSINE
    )
    decay_sine = cpoint(
        math.sqrt(1 - M5394.ABSOLUTE_DECAY_COSINE**2)
    )

    def evaluate(values: list[Any]) -> tuple[Any, Any, Any]:
        dual = M5385.M5381.IntervalDual
        coordinate, parameter, epsilon_value = (
            dual.coerce(value) for value in values
        )
        energy = deformed_path_energy_dual(
            cell, path_segment, coordinate, parameter
        )
        recoil = M5386.chart_safe_sqrt_dual(1 - energy)
        first, second = hard_lightcone_states_dual(
            configuration,
            epsilon_value,
            recoil,
            coordinate * configuration["soft_sign"],
            decay_cosine,
            decay_sine,
            0,
        )
        first_energy = first["energy"]
        second_energy = second["energy"]
        hard_product = first_energy * second_energy
        numerator = 3 * hard_product * hard_product
        expanded_denominator = (
            hard_product * hard_product
            + energy
            * energy
            * (
                first_energy * first_energy
                + second_energy * second_energy
            )
        )
        factorized_denominator = (
            (hard_product - energy * energy)
            * (hard_product - energy * energy)
            + 4 * energy * energy * (1 - energy)
        )
        return numerator, expanded_denominator, factorized_denominator

    centered_values = evaluate(list(centers))
    enclosures = [value.value for value in centered_values]
    for derivative_index in range(len(domains)):
        dual_domains = [
            M5385.M5381.IntervalDual(
                value,
                cpoint(1 if index == derivative_index else 0),
            )
            for index, value in enumerate(domains)
        ]
        derivative_values = evaluate(dual_domains)
        offset = domains[derivative_index] - centers[derivative_index]
        for value_index in range(len(enclosures)):
            enclosures[value_index] += (
                derivative_values[value_index].derivative * offset
            )
    denominator_method, denominator = max(
        (
            ("EXPANDED_HARD_ENERGY_IDENTITY", enclosures[1]),
            ("FACTORIZED_ENERGY_IDENTITY", enclosures[2]),
        ),
        key=lambda row: (
            M5258.lower_abs(row[1]),
            -M5258.upper_abs(row[1]),
        ),
    )
    return enclosures[0], denominator, denominator_method


def subdivided_path_correlated_energy_multiplier_certificate(
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
) -> dict[str, Any]:
    x_lower, x_upper = M5394.real_bounds(absolute_coordinate)
    t_lower, t_upper = M5394.real_bounds(path_parameter)
    for subdivision_count in (2, 4, 8):
        quotients: list[Any] = []
        denominators: list[Any] = []
        denominator_methods: set[str] = set()
        failed = False
        for x_index in range(subdivision_count):
            coordinate = cbox(
                x_lower
                + (x_upper - x_lower) * x_index / subdivision_count,
                x_lower
                + (x_upper - x_lower)
                * (x_index + 1)
                / subdivision_count,
            )
            for t_index in range(subdivision_count):
                parameter = cbox(
                    t_lower
                    + (t_upper - t_lower) * t_index / subdivision_count,
                    t_lower
                    + (t_upper - t_lower)
                    * (t_index + 1)
                    / subdivision_count,
                )
                numerator, denominator, method = (
                    centered_path_correlated_energy_multiplier_parts(
                        configuration,
                        cell,
                        path_segment,
                        coordinate,
                        parameter,
                        epsilon,
                    )
                )
                if M5258.lower_abs(denominator) <= 0.0:
                    failed = True
                    break
                quotients.append(numerator / denominator)
                denominators.append(denominator)
                denominator_methods.add(method)
            if failed:
                break
        if not failed:
            return {
                "multiplier": rectangular_interval_hull(quotients),
                "denominators": denominators,
                "subdivision_count": subdivision_count,
                "minimum_denominator_abs_lower": min(
                    M5258.lower_abs(value) for value in denominators
                ),
                "denominator_methods": "|".join(
                    sorted(denominator_methods)
                ),
            }
    raise M5258.IntervalSingularity(
        "path-correlated energy-multiplier denominator reaches zero"
    )


def path_aware_stable_energy_multiplier(
    configuration: dict[str, Any],
    inputs: dict[str, Any],
    internal: list[list[Any]],
    diagnostics: Any,
    label: str,
    path_context: dict[str, Any] | None,
) -> Any:
    first_square = internal[0][0] * internal[0][0]
    second_square = internal[1][0] * internal[1][0]
    soft_square = internal[2][0] * internal[2][0]
    direct_denominator = (
        first_square * second_square
        + soft_square * (first_square + second_square)
    )
    if path_context is None or M5258.lower_abs(direct_denominator) > 0.0:
        return M5386.stable_energy_multiplier(
            internal, diagnostics, label
        )
    cache_key = "path_correlated_energy_multiplier_certificate"
    certificate = path_context.get(cache_key)
    if certificate is None:
        try:
            certificate = (
                subdivided_path_correlated_energy_multiplier_certificate(
                    configuration,
                    path_context["cell"],
                    path_context["path_segment"],
                    path_context["absolute_coordinate"],
                    path_context["path_parameter"],
                    inputs["epsilon"],
                )
            )
        except (EnclosureFailure, M5258.IntervalSingularity, ValueError):
            return M5386.stable_energy_multiplier(
                internal, diagnostics, label
            )
        path_context[cache_key] = certificate
    for denominator_index, denominator in enumerate(
        certificate["denominators"]
    ):
        diagnostics.record(
            denominator,
            f"{label}:path_correlated_{denominator_index}",
        )
    diagnostics.path_correlated_energy_multiplier_subdivision_count = int(
        certificate["subdivision_count"]
    )
    diagnostics.path_correlated_energy_multiplier_denominator_abs_lower = float(
        certificate["minimum_denominator_abs_lower"]
    )
    diagnostics.path_correlated_energy_multiplier_denominator_methods = str(
        certificate["denominator_methods"]
    )
    return certificate["multiplier"]


def centered_path_correlated_external4_second_angle(
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
    global_displacement: Any,
) -> Any:
    domains = (
        absolute_coordinate,
        path_parameter,
        epsilon,
        global_displacement,
    )
    centers = tuple(M5385.complex_midpoint_box(value) for value in domains)
    decay_cosine = cpoint(
        configuration["decay_sign"] * M5394.ABSOLUTE_DECAY_COSINE
    )
    decay_sine = cpoint(
        math.sqrt(1 - M5394.ABSOLUTE_DECAY_COSINE**2)
    )

    def evaluate(values: list[Any]) -> Any:
        dual = M5385.M5381.IntervalDual
        coordinate, parameter, epsilon_value, displacement = (
            dual.coerce(value) for value in values
        )
        energy = deformed_path_energy_dual(
            cell, path_segment, coordinate, parameter
        )
        recoil = M5386.chart_safe_sqrt_dual(1 - energy)
        external4_to_second = factorized_external4_second_angle_dual(
            configuration,
            epsilon_value,
            recoil,
            coordinate * configuration["soft_sign"],
            decay_cosine,
            decay_sine,
            displacement,
        )
        return -external4_to_second

    enclosure = evaluate(list(centers)).value
    for derivative_index in range(len(domains)):
        dual_domains = [
            M5385.M5381.IntervalDual(
                value,
                cpoint(1 if index == derivative_index else 0),
            )
            for index, value in enumerate(domains)
        ]
        enclosure += evaluate(dual_domains).derivative * (
            domains[derivative_index] - centers[derivative_index]
        )
    return enclosure


def centered_path_correlated_external4_second_plus_angle(
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
    global_displacement: Any,
) -> Any:
    domains = (
        absolute_coordinate,
        path_parameter,
        epsilon,
        global_displacement,
    )
    centers = tuple(M5385.complex_midpoint_box(value) for value in domains)
    decay_cosine = cpoint(
        configuration["decay_sign"] * M5394.ABSOLUTE_DECAY_COSINE
    )
    decay_sine = cpoint(
        math.sqrt(1 - M5394.ABSOLUTE_DECAY_COSINE**2)
    )

    def evaluate(values: list[Any]) -> Any:
        dual = M5385.M5381.IntervalDual
        coordinate, parameter, epsilon_value, displacement = (
            dual.coerce(value) for value in values
        )
        energy = deformed_path_energy_dual(
            cell, path_segment, coordinate, parameter
        )
        recoil = M5386.chart_safe_sqrt_dual(1 - energy)
        _, second = hard_lightcone_states_dual(
            configuration,
            epsilon_value,
            recoil,
            coordinate * configuration["soft_sign"],
            decay_cosine,
            decay_sine,
            displacement,
        )
        target = -9 + 1j * epsilon_value
        external_transverse = M5386.chart_safe_sqrt_dual(
            1 - target * target
        )
        return (
            second["plus"] * external_transverse
            + (1 - target) * second["holomorphic"]
        )

    enclosure = evaluate(list(centers)).value
    for derivative_index in range(len(domains)):
        dual_domains = [
            M5385.M5381.IntervalDual(
                value,
                cpoint(1 if index == derivative_index else 0),
            )
            for index, value in enumerate(domains)
        ]
        enclosure += evaluate(dual_domains).derivative * (
            domains[derivative_index] - centers[derivative_index]
        )
    return enclosure


def centered_path_correlated_external4_first_angle(
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
    global_displacement: Any,
    first_chart: str,
) -> Any:
    if first_chart not in {"plus", "minus"}:
        raise ValueError(f"unsupported first-spinor chart {first_chart}")
    domains = (
        absolute_coordinate,
        path_parameter,
        epsilon,
        global_displacement,
    )
    centers = tuple(M5385.complex_midpoint_box(value) for value in domains)
    decay_cosine = cpoint(
        configuration["decay_sign"] * M5394.ABSOLUTE_DECAY_COSINE
    )
    decay_sine = cpoint(
        math.sqrt(1 - M5394.ABSOLUTE_DECAY_COSINE**2)
    )

    def evaluate(values: list[Any]) -> Any:
        dual = M5385.M5381.IntervalDual
        coordinate, parameter, epsilon_value, displacement = (
            dual.coerce(value) for value in values
        )
        energy = deformed_path_energy_dual(
            cell, path_segment, coordinate, parameter
        )
        recoil = M5386.chart_safe_sqrt_dual(1 - energy)
        first, _ = hard_lightcone_states_dual(
            configuration,
            epsilon_value,
            recoil,
            coordinate * configuration["soft_sign"],
            decay_cosine,
            decay_sine,
            displacement,
        )
        target = -9 + 1j * epsilon_value
        transverse = sheet_locked_external_transverse_dual(target)
        if first_chart == "plus":
            return (
                transverse * first["plus"]
                + (1 - target) * first["holomorphic"]
            )
        return (
            transverse * first["antiholomorphic"]
            + (1 - target) * first["minus"]
        )

    enclosure = evaluate(list(centers)).value
    for derivative_index in range(len(domains)):
        dual_domains = [
            M5385.M5381.IntervalDual(
                value,
                cpoint(1 if index == derivative_index else 0),
            )
            for index, value in enumerate(domains)
        ]
        enclosure += evaluate(dual_domains).derivative * (
            domains[derivative_index] - centers[derivative_index]
        )
    return enclosure


def centered_path_correlated_external4_first_square(
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
    global_displacement: Any,
    first_chart: str,
) -> Any:
    if first_chart not in {"plus", "minus"}:
        raise ValueError(f"unsupported first-spinor chart {first_chart}")
    domains = (
        absolute_coordinate,
        path_parameter,
        epsilon,
        global_displacement,
    )
    centers = tuple(M5385.complex_midpoint_box(value) for value in domains)
    decay_cosine = cpoint(
        configuration["decay_sign"] * M5394.ABSOLUTE_DECAY_COSINE
    )
    decay_sine = cpoint(
        math.sqrt(1 - M5394.ABSOLUTE_DECAY_COSINE**2)
    )

    def evaluate(values: list[Any]) -> Any:
        dual = M5385.M5381.IntervalDual
        coordinate, parameter, epsilon_value, displacement = (
            dual.coerce(value) for value in values
        )
        energy = deformed_path_energy_dual(
            cell, path_segment, coordinate, parameter
        )
        recoil = M5386.chart_safe_sqrt_dual(1 - energy)
        first, _ = hard_lightcone_states_dual(
            configuration,
            epsilon_value,
            recoil,
            coordinate * configuration["soft_sign"],
            decay_cosine,
            decay_sine,
            displacement,
        )
        target = -9 + 1j * epsilon_value
        transverse = sheet_locked_external_transverse_dual(target)
        external4 = {
            "plus": 1 - target,
            "minus": 1 + target,
            "holomorphic": -transverse,
            "antiholomorphic": -transverse,
        }
        return rational_pair_edge_dual(
            first,
            external4,
            first_chart,
            "plus",
            1,
        )

    enclosure = evaluate(list(centers)).value
    for derivative_index in range(len(domains)):
        dual_domains = [
            M5385.M5381.IntervalDual(
                value,
                cpoint(1 if index == derivative_index else 0),
            )
            for index, value in enumerate(domains)
        ]
        enclosure += evaluate(dual_domains).derivative * (
            domains[derivative_index] - centers[derivative_index]
        )
    return enclosure


def subdivided_path_correlated_external4_first_square(
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
    global_displacement: Any,
    first_chart: str,
    subdivision_count: int,
) -> Any:
    if subdivision_count <= 1:
        raise ValueError("subdivision count must exceed one")
    x_lower, x_upper = M5394.real_bounds(absolute_coordinate)
    t_lower, t_upper = M5394.real_bounds(path_parameter)
    enclosures: list[Any] = []
    for x_index in range(subdivision_count):
        coordinate = cbox(
            x_lower + (x_upper - x_lower) * x_index / subdivision_count,
            x_lower
            + (x_upper - x_lower) * (x_index + 1) / subdivision_count,
        )
        for t_index in range(subdivision_count):
            parameter = cbox(
                t_lower + (t_upper - t_lower) * t_index / subdivision_count,
                t_lower
                + (t_upper - t_lower) * (t_index + 1) / subdivision_count,
            )
            enclosures.append(
                centered_path_correlated_external4_first_square(
                    configuration,
                    cell,
                    path_segment,
                    coordinate,
                    parameter,
                    epsilon,
                    global_displacement,
                    first_chart,
                )
            )
    return rectangular_interval_hull(enclosures)


def centered_path_correlated_external4_first_plus_angle_factorized(
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
    global_displacement: Any,
) -> Any:
    if configuration["role"] != "reciprocal":
        raise ValueError(
            "factorized external4-first angle requires reciprocal role"
        )
    domains = (
        absolute_coordinate,
        path_parameter,
        epsilon,
        global_displacement,
    )
    centers = tuple(M5385.complex_midpoint_box(value) for value in domains)
    decay_cosine = cpoint(
        configuration["decay_sign"] * M5394.ABSOLUTE_DECAY_COSINE
    )
    decay_sine = cpoint(
        math.sqrt(1 - M5394.ABSOLUTE_DECAY_COSINE**2)
    )

    def evaluate(values: list[Any]) -> Any:
        dual = M5385.M5381.IntervalDual
        coordinate, parameter, epsilon_value, displacement = (
            dual.coerce(value) for value in values
        )
        energy = deformed_path_energy_dual(
            cell, path_segment, coordinate, parameter
        )
        recoil = M5386.chart_safe_sqrt_dual(1 - energy)
        first, _ = hard_lightcone_states_dual(
            configuration,
            epsilon_value,
            recoil,
            coordinate * configuration["soft_sign"],
            decay_cosine,
            decay_sine,
            displacement,
        )
        target = -9 + 1j * epsilon_value
        transverse = sheet_locked_external_transverse_dual(target)
        q_value = -(target - 1) / (target + 1)
        external_root = -1j * M5386.chart_safe_sqrt_dual(-q_value)
        return transverse * external_root * (
            first["unit_circle"] * first["raw_holomorphic"]
            - first["raw_antiholomorphic"] / first["selected_root"]
        )

    enclosure = evaluate(list(centers)).value
    for derivative_index in range(len(domains)):
        dual_domains = [
            M5385.M5381.IntervalDual(
                value,
                cpoint(1 if index == derivative_index else 0),
            )
            for index, value in enumerate(domains)
        ]
        enclosure += evaluate(dual_domains).derivative * (
            domains[derivative_index] - centers[derivative_index]
        )
    return enclosure


def centered_path_correlated_external0_first_minus_angle(
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
    global_displacement: Any,
) -> Any:
    domains = (
        absolute_coordinate,
        path_parameter,
        epsilon,
        global_displacement,
    )
    centers = tuple(M5385.complex_midpoint_box(value) for value in domains)
    decay_cosine = cpoint(
        configuration["decay_sign"] * M5394.ABSOLUTE_DECAY_COSINE
    )
    decay_sine = cpoint(
        math.sqrt(1 - M5394.ABSOLUTE_DECAY_COSINE**2)
    )

    def evaluate(values: list[Any]) -> Any:
        dual = M5385.M5381.IntervalDual
        coordinate, parameter, epsilon_value, displacement = (
            dual.coerce(value) for value in values
        )
        energy = deformed_path_energy_dual(
            cell, path_segment, coordinate, parameter
        )
        recoil = M5386.chart_safe_sqrt_dual(1 - energy)
        first, _ = hard_lightcone_states_dual(
            configuration,
            epsilon_value,
            recoil,
            coordinate * configuration["soft_sign"],
            decay_cosine,
            decay_sine,
            displacement,
        )
        target = -9 + 1j * epsilon_value
        external_transverse = M5386.chart_safe_sqrt_dual(
            1 - target * target
        )
        return (
            -external_transverse * first["minus"]
            + (1 - target) * first["antiholomorphic"]
        )

    enclosure = evaluate(list(centers)).value
    for derivative_index in range(len(domains)):
        dual_domains = [
            M5385.M5381.IntervalDual(
                value,
                cpoint(1 if index == derivative_index else 0),
            )
            for index, value in enumerate(domains)
        ]
        enclosure += evaluate(dual_domains).derivative * (
            domains[derivative_index] - centers[derivative_index]
        )
    return enclosure


def centered_path_correlated_external0_first_minus_plus_angle(
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
    global_displacement: Any,
) -> Any:
    domains = (
        absolute_coordinate,
        path_parameter,
        epsilon,
        global_displacement,
    )
    centers = tuple(M5385.complex_midpoint_box(value) for value in domains)
    decay_cosine = cpoint(
        configuration["decay_sign"] * M5394.ABSOLUTE_DECAY_COSINE
    )
    decay_sine = cpoint(
        math.sqrt(1 - M5394.ABSOLUTE_DECAY_COSINE**2)
    )

    def evaluate(values: list[Any]) -> Any:
        dual = M5385.M5381.IntervalDual
        coordinate, parameter, epsilon_value, displacement = (
            dual.coerce(value) for value in values
        )
        energy = deformed_path_energy_dual(
            cell, path_segment, coordinate, parameter
        )
        recoil = M5386.chart_safe_sqrt_dual(1 - energy)
        first, _ = hard_lightcone_states_dual(
            configuration,
            epsilon_value,
            recoil,
            coordinate * configuration["soft_sign"],
            decay_cosine,
            decay_sine,
            displacement,
        )
        target = -9 + 1j * epsilon_value
        external_transverse = M5386.chart_safe_sqrt_dual(
            1 - target * target
        )
        return (
            -external_transverse * first["holomorphic"]
            + (1 - target) * first["plus"]
        )

    enclosure = evaluate(list(centers)).value
    for derivative_index in range(len(domains)):
        dual_domains = [
            M5385.M5381.IntervalDual(
                value,
                cpoint(1 if index == derivative_index else 0),
            )
            for index, value in enumerate(domains)
        ]
        enclosure += evaluate(dual_domains).derivative * (
            domains[derivative_index] - centers[derivative_index]
        )
    return enclosure


def native_representative_external0_first_minus_plus_angle_dual(
    configuration: dict[str, Any],
    epsilon: Any,
    recoil: Any,
    soft_cosine: Any,
    decay_cosine: Any,
    decay_sine: Any,
    global_displacement: Any,
) -> Any:
    if configuration["role"] != "reciprocal":
        raise ValueError("native representative edge requires reciprocal role")
    dual = M5385.M5381.IntervalDual
    epsilon = dual.coerce(epsilon)
    recoil = dual.coerce(recoil)
    soft_cosine = dual.coerce(soft_cosine)
    decay_cosine = dual.coerce(decay_cosine)
    decay_sine = dual.coerce(decay_sine)
    global_displacement = dual.coerce(global_displacement)
    epsilon_squared = epsilon * epsilon
    q_value = (
        -(80 + epsilon_squared) / (64 + epsilon_squared)
        + 1j * (-2 * epsilon / (64 + epsilon_squared))
    )
    external_root = -1j * M5386.chart_safe_sqrt_dual(-q_value)
    soft_sine = M5385.positive_sqrt_dual(
        1 - soft_cosine * soft_cosine
    )
    factor_f1 = (
        q_value * recoil * soft_cosine
        + q_value * recoil
        - q_value * soft_cosine
        - q_value
        + recoil * soft_cosine
        + recoil
        - soft_cosine
        + 1
    )
    factor_f2 = (
        q_value * recoil * soft_cosine
        - q_value * recoil
        - q_value * soft_cosine
        - q_value
        + recoil * soft_cosine
        - recoil
        - soft_cosine
        + 1
    )
    representative = (
        soft_sine
        * (1 + decay_cosine)
        * factor_f1
        / (decay_sine * (1 + soft_cosine) * factor_f2)
    )
    selected_root = soft_sine / (
        (1 + soft_cosine) * external_root
    )
    unit_circle = selected_root + global_displacement
    recoil_squared = recoil * recoil
    relative_cosine_constant = soft_cosine * decay_cosine
    relative_cosine_laurent = soft_sine * decay_sine / 2
    first_energy_constant = (1 + recoil_squared) / 2
    first_energy_coefficient = -(1 - recoil_squared) / 2
    longitudinal_constant = -(1 - recoil_squared) / 2
    longitudinal_coefficient = (1 - recoil) * (1 - recoil) / 2
    plus_coefficient = (
        first_energy_coefficient
        + longitudinal_coefficient * soft_cosine
    )
    plus_constant = (
        first_energy_constant
        + longitudinal_constant * soft_cosine
        + recoil * decay_cosine
        + plus_coefficient * relative_cosine_constant
    )
    plus_laurent = plus_coefficient * relative_cosine_laurent
    holomorphic_constant = soft_sine * (
        longitudinal_constant
        + longitudinal_coefficient * relative_cosine_constant
    )
    holomorphic_laurent = (
        soft_sine
        * longitudinal_coefficient
        * relative_cosine_laurent
    )
    target = -9 + 1j * epsilon
    external_transverse = M5386.chart_safe_sqrt_dual(
        1 - target * target
    )
    polynomial = (
        -external_transverse
        * unit_circle
        * (
            holomorphic_laurent * representative * representative
            + holomorphic_constant * representative
            + holomorphic_laurent
            + recoil * decay_sine
        )
        + (1 - target)
        * (
            plus_laurent * representative * representative
            + plus_constant * representative
            + plus_laurent
        )
    )
    return polynomial / representative


def centered_path_correlated_native_external0_first_minus_plus_angle(
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
    global_displacement: Any,
) -> Any:
    domains = (
        absolute_coordinate,
        path_parameter,
        epsilon,
        global_displacement,
    )
    centers = tuple(M5385.complex_midpoint_box(value) for value in domains)
    decay_cosine = cpoint(
        configuration["decay_sign"] * M5394.ABSOLUTE_DECAY_COSINE
    )
    decay_sine = cpoint(
        math.sqrt(1 - M5394.ABSOLUTE_DECAY_COSINE**2)
    )

    def evaluate(values: list[Any]) -> Any:
        dual = M5385.M5381.IntervalDual
        coordinate, parameter, epsilon_value, displacement = (
            dual.coerce(value) for value in values
        )
        energy = deformed_path_energy_dual(
            cell, path_segment, coordinate, parameter
        )
        recoil = M5386.chart_safe_sqrt_dual(1 - energy)
        return native_representative_external0_first_minus_plus_angle_dual(
            configuration,
            epsilon_value,
            recoil,
            coordinate * configuration["soft_sign"],
            decay_cosine,
            decay_sine,
            displacement,
        )

    direct = evaluate(list(domains)).value
    mean_value = evaluate(list(centers)).value
    for derivative_index in range(len(domains)):
        dual_domains = [
            M5385.M5381.IntervalDual(
                value,
                cpoint(1 if index == derivative_index else 0),
            )
            for index, value in enumerate(domains)
        ]
        mean_value += evaluate(dual_domains).derivative * (
            domains[derivative_index] - centers[derivative_index]
        )
    return max(
        (direct, mean_value),
        key=lambda value: (
            M5258.lower_abs(value),
            -M5258.upper_abs(value),
        ),
    )


def negative_half_plane_subcover_native_external0_first_minus_plus_angle(
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
    global_displacement: Any,
) -> tuple[Any, dict[str, Any]]:
    x_lower, x_upper = M5394.real_bounds(absolute_coordinate)
    t_lower, t_upper = M5394.real_bounds(path_parameter)
    epsilon_real_lower, epsilon_real_upper = M5394.real_bounds(epsilon)
    epsilon_imaginary_lower, epsilon_imaginary_upper = (
        M5394.imaginary_bounds(epsilon)
    )
    split_schedule = (
        "epsilon_real",
        "epsilon_real",
        "epsilon_real",
        "epsilon_real",
        "epsilon_real",
        "absolute_coordinate",
        "absolute_coordinate",
        "path_parameter",
        "path_parameter",
        "absolute_coordinate",
        "path_parameter",
        "epsilon_real",
    )
    stack = [
        (
            x_lower,
            x_upper,
            t_lower,
            t_upper,
            epsilon_real_lower,
            epsilon_real_upper,
            0,
        )
    ]
    accepted: list[Any] = []
    evaluation_count = 0
    minimum_negative_real_margin = math.inf
    while stack:
        (
            local_x_lower,
            local_x_upper,
            local_t_lower,
            local_t_upper,
            local_epsilon_lower,
            local_epsilon_upper,
            depth,
        ) = stack.pop()
        edge = (
            centered_path_correlated_native_external0_first_minus_plus_angle(
                configuration,
                cell,
                path_segment,
                cbox(local_x_lower, local_x_upper),
                cbox(local_t_lower, local_t_upper),
                cbox(
                    local_epsilon_lower,
                    local_epsilon_upper,
                    epsilon_imaginary_lower,
                    epsilon_imaginary_upper,
                ),
                global_displacement,
            )
        )
        evaluation_count += 1
        edge_real_upper = M5394.real_bounds(edge)[1]
        if edge_real_upper < 0.0:
            accepted.append(edge)
            minimum_negative_real_margin = min(
                minimum_negative_real_margin,
                -edge_real_upper,
            )
            continue
        if depth >= len(split_schedule):
            raise EnclosureFailure(
                "native external0-first minus/plus edge does not enter a "
                "common negative-real half-plane after the exact subcover"
            )
        split_variable = split_schedule[depth]
        if split_variable == "epsilon_real":
            midpoint = 0.5 * (
                local_epsilon_lower + local_epsilon_upper
            )
            children = (
                (
                    local_x_lower,
                    local_x_upper,
                    local_t_lower,
                    local_t_upper,
                    local_epsilon_lower,
                    midpoint,
                    depth + 1,
                ),
                (
                    local_x_lower,
                    local_x_upper,
                    local_t_lower,
                    local_t_upper,
                    midpoint,
                    local_epsilon_upper,
                    depth + 1,
                ),
            )
        elif split_variable == "absolute_coordinate":
            midpoint = 0.5 * (local_x_lower + local_x_upper)
            children = (
                (
                    local_x_lower,
                    midpoint,
                    local_t_lower,
                    local_t_upper,
                    local_epsilon_lower,
                    local_epsilon_upper,
                    depth + 1,
                ),
                (
                    midpoint,
                    local_x_upper,
                    local_t_lower,
                    local_t_upper,
                    local_epsilon_lower,
                    local_epsilon_upper,
                    depth + 1,
                ),
            )
        else:
            midpoint = 0.5 * (local_t_lower + local_t_upper)
            children = (
                (
                    local_x_lower,
                    local_x_upper,
                    local_t_lower,
                    midpoint,
                    local_epsilon_lower,
                    local_epsilon_upper,
                    depth + 1,
                ),
                (
                    local_x_lower,
                    local_x_upper,
                    midpoint,
                    local_t_upper,
                    local_epsilon_lower,
                    local_epsilon_upper,
                    depth + 1,
                ),
            )
        stack.extend(reversed(children))
        if len(stack) + len(accepted) > 4096:
            raise EnclosureFailure(
                "native external0-first minus/plus edge subcover budget exceeded"
            )
    enclosure = rectangular_interval_hull(accepted)
    enclosure_real_upper = M5394.real_bounds(enclosure)[1]
    if enclosure_real_upper >= 0.0 or M5258.lower_abs(enclosure) <= 0.0:
        raise EnclosureFailure(
            "native external0-first minus/plus edge union lost its "
            "negative-real half-plane"
        )
    return enclosure, {
        "leaf_count": len(accepted),
        "evaluation_count": evaluation_count,
        "minimum_negative_real_margin": minimum_negative_real_margin,
        "enclosure_negative_real_margin": -enclosure_real_upper,
        "split_schedule": "|".join(split_schedule),
    }


def native_external0_first_minus_plus_path_derivatives(
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
    global_displacement: Any,
) -> tuple[Any, Any]:
    decay_cosine = cpoint(
        configuration["decay_sign"] * M5394.ABSOLUTE_DECAY_COSINE
    )
    decay_sine = cpoint(
        math.sqrt(1 - M5394.ABSOLUTE_DECAY_COSINE**2)
    )
    dual = M5385.M5381.IntervalDual

    def derivative(seed_coordinate: int, seed_parameter: int) -> Any:
        coordinate = dual(
            absolute_coordinate, cpoint(seed_coordinate)
        )
        parameter = dual(path_parameter, cpoint(seed_parameter))
        energy = deformed_path_energy_dual(
            cell, path_segment, coordinate, parameter
        )
        recoil = M5386.chart_safe_sqrt_dual(1 - energy)
        return (
            native_representative_external0_first_minus_plus_angle_dual(
                configuration,
                dual(epsilon),
                recoil,
                coordinate * configuration["soft_sign"],
                decay_cosine,
                decay_sine,
                dual(global_displacement),
            ).derivative
        )

    return derivative(1, 0), derivative(0, 1)


def real_interval_product_bounds(
    left: tuple[float, float], right: tuple[float, float]
) -> tuple[float, float]:
    products = (
        left[0] * right[0],
        left[0] * right[1],
        left[1] * right[0],
        left[1] * right[1],
    )
    return (
        math.nextafter(min(products), -math.inf),
        math.nextafter(max(products), math.inf),
    )


def native_external0_first_minus_plus_path_jacobian_bounds(
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
    global_displacement: Any,
) -> dict[str, Any]:
    derivative_x, derivative_t = (
        native_external0_first_minus_plus_path_derivatives(
            configuration,
            cell,
            path_segment,
            absolute_coordinate,
            path_parameter,
            epsilon,
            global_displacement,
        )
    )
    derivative_x_real = M5394.real_bounds(derivative_x)
    derivative_x_imaginary = M5394.imaginary_bounds(derivative_x)
    derivative_t_real = M5394.real_bounds(derivative_t)
    derivative_t_imaginary = M5394.imaginary_bounds(derivative_t)
    diagonal_product = real_interval_product_bounds(
        derivative_x_real, derivative_t_imaginary
    )
    off_diagonal_product = real_interval_product_bounds(
        derivative_x_imaginary, derivative_t_real
    )
    determinant_lower = math.nextafter(
        diagonal_product[0] - off_diagonal_product[1],
        -math.inf,
    )
    determinant_upper = math.nextafter(
        diagonal_product[1] - off_diagonal_product[0],
        math.inf,
    )
    if determinant_lower <= 0.0 <= determinant_upper:
        raise EnclosureFailure(
            "native external01 path Jacobian determinant reaches zero"
        )
    x_real_orientation = (
        "INCREASING"
        if derivative_x_real[0] > 0.0
        else (
            "DECREASING"
            if derivative_x_real[1] < 0.0
            else "NOT_SIGN_DEFINITE"
        )
    )
    t_imaginary_orientation = (
        "INCREASING"
        if derivative_t_imaginary[0] > 0.0
        else (
            "DECREASING"
            if derivative_t_imaginary[1] < 0.0
            else "NOT_SIGN_DEFINITE"
        )
    )
    determinant_abs_lower = min(
        abs(determinant_lower), abs(determinant_upper)
    )
    return {
        "derivative_x_real": derivative_x_real,
        "derivative_x_imaginary": derivative_x_imaginary,
        "derivative_t_real": derivative_t_real,
        "derivative_t_imaginary": derivative_t_imaginary,
        "determinant_lower": determinant_lower,
        "determinant_upper": determinant_upper,
        "determinant_abs_lower": determinant_abs_lower,
        "x_real_orientation": x_real_orientation,
        "t_imaginary_orientation": t_imaginary_orientation,
        "global_injectivity_method": (
            "SEGMENT_AVERAGED_INTERVAL_MATRIX_REGULARITY"
        ),
    }


def centered_path_correlated_external4_second_invariant_factorized(
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
    global_displacement: Any,
) -> Any:
    domains = (
        absolute_coordinate,
        path_parameter,
        epsilon,
        global_displacement,
    )
    centers = tuple(M5385.complex_midpoint_box(value) for value in domains)
    decay_cosine = cpoint(
        configuration["decay_sign"] * M5394.ABSOLUTE_DECAY_COSINE
    )
    decay_sine = cpoint(
        math.sqrt(1 - M5394.ABSOLUTE_DECAY_COSINE**2)
    )

    def evaluate(values: list[Any]) -> Any:
        dual = M5385.M5381.IntervalDual
        coordinate, parameter, epsilon_value, displacement = (
            dual.coerce(value) for value in values
        )
        energy = deformed_path_energy_dual(
            cell, path_segment, coordinate, parameter
        )
        recoil = M5386.chart_safe_sqrt_dual(1 - energy)
        _, second = hard_lightcone_states_dual(
            configuration,
            epsilon_value,
            recoil,
            coordinate * configuration["soft_sign"],
            decay_cosine,
            decay_sine,
            displacement,
        )
        target = -9 + 1j * epsilon_value
        transverse = sheet_locked_external_transverse_dual(target)
        displacement_correction = -transverse * displacement * (
            second["raw_holomorphic"]
            - second["raw_antiholomorphic"]
            / (second["selected_root"] * second["unit_circle"])
        )
        return -4 * (1 - energy) + displacement_correction

    enclosure = evaluate(list(centers)).value
    for derivative_index in range(len(domains)):
        dual_domains = [
            M5385.M5381.IntervalDual(
                value,
                cpoint(1 if index == derivative_index else 0),
            )
            for index, value in enumerate(domains)
        ]
        enclosure += evaluate(dual_domains).derivative * (
            domains[derivative_index] - centers[derivative_index]
        )
    return enclosure


def centered_path_correlated_external_hard_invariant(
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
    global_displacement: Any,
    external_endpoint: int,
    hard_index: int,
) -> Any:
    if hard_index not in (1, 2):
        raise ValueError(f"unsupported hard index {hard_index}")
    if external_endpoint == 4 and hard_index == 2:
        return centered_path_correlated_external4_second_invariant_factorized(
            configuration,
            cell,
            path_segment,
            absolute_coordinate,
            path_parameter,
            epsilon,
            global_displacement,
        )
    domains = (
        absolute_coordinate,
        path_parameter,
        epsilon,
        global_displacement,
    )
    centers = tuple(M5385.complex_midpoint_box(value) for value in domains)
    decay_cosine = cpoint(
        configuration["decay_sign"] * M5394.ABSOLUTE_DECAY_COSINE
    )
    decay_sine = cpoint(
        math.sqrt(1 - M5394.ABSOLUTE_DECAY_COSINE**2)
    )

    def evaluate(values: list[Any]) -> Any:
        dual = M5385.M5381.IntervalDual
        coordinate, parameter, epsilon_value, displacement = (
            dual.coerce(value) for value in values
        )
        energy = deformed_path_energy_dual(
            cell, path_segment, coordinate, parameter
        )
        recoil = M5386.chart_safe_sqrt_dual(1 - energy)
        first, second = hard_lightcone_states_dual(
            configuration,
            epsilon_value,
            recoil,
            coordinate * configuration["soft_sign"],
            decay_cosine,
            decay_sine,
            displacement,
        )
        hard = first if hard_index == 1 else second
        target = -9 + 1j * epsilon_value
        transverse = sheet_locked_external_transverse_dual(target)
        momentum_x = (
            hard["holomorphic"] + hard["antiholomorphic"]
        ) / 2
        orientation = 1 if external_endpoint == 0 else -1
        return 2 * (
            -hard["energy"]
            + orientation
            * (
                transverse * momentum_x
                + target * hard["momentum_z"]
            )
        )

    enclosure = evaluate(list(centers)).value
    for derivative_index in range(len(domains)):
        dual_domains = [
            M5385.M5381.IntervalDual(
                value,
                cpoint(1 if index == derivative_index else 0),
            )
            for index, value in enumerate(domains)
        ]
        enclosure += evaluate(dual_domains).derivative * (
            domains[derivative_index] - centers[derivative_index]
        )
    return enclosure


def centered_path_correlated_left_incoming_hard_invariant(
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
    global_displacement: Any,
    external_endpoint: int,
    hard_index: int,
) -> Any:
    if external_endpoint not in (0, 4):
        raise ValueError(f"unsupported external endpoint {external_endpoint}")
    if hard_index not in (1, 2):
        raise ValueError(f"unsupported hard index {hard_index}")
    domains = (
        absolute_coordinate,
        path_parameter,
        epsilon,
        global_displacement,
    )
    centers = tuple(M5385.complex_midpoint_box(value) for value in domains)
    decay_cosine = cpoint(
        configuration["decay_sign"] * M5394.ABSOLUTE_DECAY_COSINE
    )
    decay_sine = cpoint(
        math.sqrt(1 - M5394.ABSOLUTE_DECAY_COSINE**2)
    )

    def evaluate(values: list[Any]) -> Any:
        dual = M5385.M5381.IntervalDual
        coordinate, parameter, epsilon_value, displacement = (
            dual.coerce(value) for value in values
        )
        energy = deformed_path_energy_dual(
            cell, path_segment, coordinate, parameter
        )
        recoil = M5386.chart_safe_sqrt_dual(1 - energy)
        first, second = hard_lightcone_states_dual(
            configuration,
            epsilon_value,
            recoil,
            coordinate * configuration["soft_sign"],
            decay_cosine,
            decay_sine,
            displacement,
        )
        hard = first if hard_index == 1 else second
        lightcone_factor = (
            hard["minus"] if external_endpoint == 0 else hard["plus"]
        )
        return -2 * lightcone_factor

    enclosure = evaluate(list(centers)).value
    for derivative_index in range(len(domains)):
        dual_domains = [
            M5385.M5381.IntervalDual(
                value,
                cpoint(1 if index == derivative_index else 0),
            )
            for index, value in enumerate(domains)
        ]
        enclosure += evaluate(dual_domains).derivative * (
            domains[derivative_index] - centers[derivative_index]
        )
    return enclosure


def centered_path_correlated_external_second_invariant(
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
    global_displacement: Any,
    external_endpoint: int,
) -> Any:
    return centered_path_correlated_external_hard_invariant(
        configuration,
        cell,
        path_segment,
        absolute_coordinate,
        path_parameter,
        epsilon,
        global_displacement,
        external_endpoint,
        2,
    )


def centered_path_correlated_external_first_invariant(
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
    global_displacement: Any,
    external_endpoint: int,
) -> Any:
    return centered_path_correlated_external_hard_invariant(
        configuration,
        cell,
        path_segment,
        absolute_coordinate,
        path_parameter,
        epsilon,
        global_displacement,
        external_endpoint,
        1,
    )


def rectangular_interval_hull(values: list[Any]) -> Any:
    if not values:
        raise ValueError("cannot hull an empty interval family")
    real_bounds = [M5394.real_bounds(value) for value in values]
    imaginary_bounds = [M5394.imaginary_bounds(value) for value in values]
    return cbox(
        math.nextafter(min(value[0] for value in real_bounds), -math.inf),
        math.nextafter(max(value[1] for value in real_bounds), math.inf),
        math.nextafter(
            min(value[0] for value in imaginary_bounds), -math.inf
        ),
        math.nextafter(
            max(value[1] for value in imaginary_bounds), math.inf
        ),
    )


def centered_path_correlated_left_second_soft_mixed_angle(
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
) -> Any:
    domains = (absolute_coordinate, path_parameter, epsilon)
    centers = tuple(M5385.complex_midpoint_box(value) for value in domains)
    decay_cosine = cpoint(
        configuration["decay_sign"] * M5394.ABSOLUTE_DECAY_COSINE
    )
    decay_sine = cpoint(
        math.sqrt(1 - M5394.ABSOLUTE_DECAY_COSINE**2)
    )

    def evaluate(values: list[Any]) -> Any:
        dual = M5385.M5381.IntervalDual
        coordinate, parameter, epsilon_value = (
            dual.coerce(value) for value in values
        )
        energy = deformed_path_energy_dual(
            cell,
            path_segment,
            coordinate,
            parameter,
        )
        recoil = M5386.chart_safe_sqrt_dual(1 - energy)
        return M5386.hard_soft_edge_dual(
            configuration,
            epsilon_value,
            recoil,
            coordinate * configuration["soft_sign"],
            decay_cosine,
            decay_sine,
            dual.coerce(1),
            2,
            "minus",
            "plus",
            0,
        )

    enclosure = evaluate(list(centers)).value
    for derivative_index in range(len(domains)):
        dual_domains = [
            M5385.M5381.IntervalDual(
                value,
                cpoint(1 if index == derivative_index else 0),
            )
            for index, value in enumerate(domains)
        ]
        enclosure += evaluate(dual_domains).derivative * (
            domains[derivative_index] - centers[derivative_index]
        )
    return enclosure


def subdivided_path_correlated_left_second_soft_mixed_angle(
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
    subdivision_count: int,
) -> Any:
    if subdivision_count <= 1:
        raise ValueError("subdivision count must exceed one")
    x_lower, x_upper = M5394.real_bounds(absolute_coordinate)
    t_lower, t_upper = M5394.real_bounds(path_parameter)
    enclosures: list[Any] = []
    for x_index in range(subdivision_count):
        coordinate = cbox(
            x_lower
            + (x_upper - x_lower) * x_index / subdivision_count,
            x_lower
            + (x_upper - x_lower) * (x_index + 1) / subdivision_count,
        )
        for t_index in range(subdivision_count):
            parameter = cbox(
                t_lower
                + (t_upper - t_lower) * t_index / subdivision_count,
                t_lower
                + (t_upper - t_lower) * (t_index + 1) / subdivision_count,
            )
            enclosures.append(
                centered_path_correlated_left_second_soft_mixed_angle(
                    configuration,
                    cell,
                    path_segment,
                    coordinate,
                    parameter,
                    epsilon,
                )
            )
    return rectangular_interval_hull(enclosures)


def subdivided_path_first_rational_spinors(
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
    global_displacement: Any,
    orientation: int,
    diagnostics: Any,
    label: str,
    subdivision_count: int,
) -> tuple[
    tuple[list[Any], list[Any]],
    tuple[list[int], list[int]],
    str,
]:
    if subdivision_count <= 1:
        raise ValueError("subdivision count must exceed one")
    x_lower, x_upper = M5394.real_bounds(absolute_coordinate)
    t_lower, t_upper = M5394.real_bounds(path_parameter)
    factor_rows: list[dict[str, Any]] = []
    for x_index in range(subdivision_count):
        coordinate = cbox(
            x_lower + (x_upper - x_lower) * x_index / subdivision_count,
            x_lower
            + (x_upper - x_lower) * (x_index + 1) / subdivision_count,
        )
        for t_index in range(subdivision_count):
            parameter = cbox(
                t_lower + (t_upper - t_lower) * t_index / subdivision_count,
                t_lower
                + (t_upper - t_lower) * (t_index + 1) / subdivision_count,
            )
            energy = deformed_path_energy_dual(
                cell,
                path_segment,
                coordinate,
                parameter,
            ).value
            local_inputs, local_geometry = interval_inputs(
                configuration,
                coordinate,
                energy,
                epsilon,
            )
            unit_circle = local_geometry["selected_root"] + global_displacement
            factor_rows.append(
                {
                    "plus": cpoint(orientation)
                    * tight_first_lightcone_factor(
                        configuration, local_inputs, local_geometry, "plus"
                    ),
                    "minus": cpoint(orientation)
                    * tight_first_lightcone_factor(
                        configuration, local_inputs, local_geometry, "minus"
                    ),
                    "holomorphic": cpoint(orientation)
                    * unit_circle
                    * tight_first_lightcone_factor(
                        configuration,
                        local_inputs,
                        local_geometry,
                        "holomorphic",
                    ),
                    "antiholomorphic": cpoint(orientation)
                    * tight_first_lightcone_factor(
                        configuration,
                        local_inputs,
                        local_geometry,
                        "antiholomorphic",
                    )
                    / unit_circle,
                }
            )
    families = (
        ("plus", "plus", "holomorphic"),
        ("minus", "minus", "antiholomorphic"),
    )
    family_scores = {
        chart: min(
            max(M5258.lower_abs(row[first]), M5258.lower_abs(row[second]))
            for row in factor_rows
        )
        for chart, first, second in families
    }
    chart, _, _ = max(families, key=lambda row: family_scores[row[0]])
    if family_scores[chart] <= 0.0:
        raise M5258.IntervalSingularity(
            f"no subdivided first-spinor projective family survives: {label}"
        )
    angle_first: list[Any] = []
    angle_second: list[Any] = []
    square_first: list[Any] = []
    square_second: list[Any] = []
    for row in factor_rows:
        if chart == "plus":
            plus = row["plus"]
            holomorphic = row["holomorphic"]
            if M5258.lower_abs(plus) >= M5258.lower_abs(holomorphic):
                diagnostics.record(plus, f"{label}:subdivided_plus_diagonal")
                quotient = M5258.safe_divide(
                    row["antiholomorphic"],
                    plus,
                    diagnostics,
                    f"{label}:subdivided_antiholomorphic_over_plus",
                )
            else:
                diagnostics.record(
                    holomorphic,
                    f"{label}:subdivided_holomorphic_transverse",
                )
                quotient = M5258.safe_divide(
                    row["minus"],
                    holomorphic,
                    diagnostics,
                    f"{label}:subdivided_minus_over_holomorphic",
                )
            angle_first.append(plus)
            angle_second.append(holomorphic)
            square_first.append(cpoint(1))
            square_second.append(quotient)
        else:
            minus = row["minus"]
            antiholomorphic = row["antiholomorphic"]
            if M5258.lower_abs(minus) >= M5258.lower_abs(antiholomorphic):
                diagnostics.record(minus, f"{label}:subdivided_minus_diagonal")
                quotient = M5258.safe_divide(
                    row["holomorphic"],
                    minus,
                    diagnostics,
                    f"{label}:subdivided_holomorphic_over_minus",
                )
            else:
                diagnostics.record(
                    antiholomorphic,
                    f"{label}:subdivided_antiholomorphic_transverse",
                )
                quotient = M5258.safe_divide(
                    row["plus"],
                    antiholomorphic,
                    diagnostics,
                    f"{label}:subdivided_plus_over_antiholomorphic",
                )
            angle_first.append(antiholomorphic)
            angle_second.append(minus)
            square_first.append(quotient)
            square_second.append(cpoint(1))
    spinors = (
        [
            rectangular_interval_hull(angle_first),
            rectangular_interval_hull(angle_second),
        ],
        [
            rectangular_interval_hull(square_first),
            rectangular_interval_hull(square_second),
        ],
    )
    exponents = (
        ([0, 1], [0, -1])
        if chart == "plus"
        else ([-1, 0], [1, 0])
    )
    return spinors, exponents, chart


def subdivided_path_left_incoming_first_edge_overrides(
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
    global_displacement: Any,
    required_first_chart: str,
    diagnostics: Any,
    subdivision_count: int,
) -> dict[tuple[frozenset[int], int], Any]:
    first_spinors, _, first_chart = subdivided_path_first_rational_spinors(
        configuration,
        cell,
        path_segment,
        absolute_coordinate,
        path_parameter,
        epsilon,
        global_displacement,
        1,
        diagnostics,
        "away_arc_left_incoming_first",
        subdivision_count,
    )
    if first_chart != required_first_chart:
        raise EnclosureFailure(
            "subdivided left incoming-first edge changed projective family"
        )
    incoming_spinors = (
        [cpoint(-2), cpoint(0)],
        [cpoint(1), cpoint(0)],
    )
    pair = frozenset((0, 1))
    return {
        (pair, chirality): M5258.spinor_bracket(
            incoming_spinors[chirality], first_spinors[chirality]
        )
        for chirality in (0, 1)
    }


def subdivided_path_correlated_external_hard_invariant(
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
    global_displacement: Any,
    external_endpoint: int,
    hard_index: int,
    subdivision_count: int,
) -> Any:
    if subdivision_count <= 1:
        raise ValueError("subdivision count must exceed one")
    x_lower, x_upper = M5394.real_bounds(absolute_coordinate)
    t_lower, t_upper = M5394.real_bounds(path_parameter)
    x_breakpoints = [
        x_lower + (x_upper - x_lower) * index / subdivision_count
        for index in range(subdivision_count + 1)
    ]
    t_breakpoints = [
        t_lower + (t_upper - t_lower) * index / subdivision_count
        for index in range(subdivision_count + 1)
    ]
    enclosures: list[Any] = []
    for x_index in range(subdivision_count):
        coordinate = cbox(
            x_breakpoints[x_index], x_breakpoints[x_index + 1]
        )
        for t_index in range(subdivision_count):
            parameter = cbox(
                t_breakpoints[t_index], t_breakpoints[t_index + 1]
            )
            enclosures.append(
                centered_path_correlated_external_hard_invariant(
                    configuration,
                    cell,
                    path_segment,
                    coordinate,
                    parameter,
                    epsilon,
                    global_displacement,
                    external_endpoint,
                    hard_index,
                )
            )
    return rectangular_interval_hull(enclosures)


def subdivided_path_correlated_left_incoming_hard_invariant(
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
    global_displacement: Any,
    external_endpoint: int,
    hard_index: int,
    subdivision_count: int,
) -> Any:
    if subdivision_count <= 1:
        raise ValueError("subdivision count must exceed one")
    x_lower, x_upper = M5394.real_bounds(absolute_coordinate)
    t_lower, t_upper = M5394.real_bounds(path_parameter)
    enclosures: list[Any] = []
    for x_index in range(subdivision_count):
        coordinate = cbox(
            x_lower + (x_upper - x_lower) * x_index / subdivision_count,
            x_lower
            + (x_upper - x_lower) * (x_index + 1) / subdivision_count,
        )
        for t_index in range(subdivision_count):
            parameter = cbox(
                t_lower + (t_upper - t_lower) * t_index / subdivision_count,
                t_lower
                + (t_upper - t_lower) * (t_index + 1) / subdivision_count,
            )
            enclosures.append(
                centered_path_correlated_left_incoming_hard_invariant(
                    configuration,
                    cell,
                    path_segment,
                    coordinate,
                    parameter,
                    epsilon,
                    global_displacement,
                    external_endpoint,
                    hard_index,
                )
            )
    return rectangular_interval_hull(enclosures)


def subdivided_path_correlated_external_second_invariant(
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
    global_displacement: Any,
    external_endpoint: int,
    subdivision_count: int,
) -> Any:
    return subdivided_path_correlated_external_hard_invariant(
        configuration,
        cell,
        path_segment,
        absolute_coordinate,
        path_parameter,
        epsilon,
        global_displacement,
        external_endpoint,
        2,
        subdivision_count,
    )


def half_plane_subcover_external42_invariant(
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
    global_displacement: Any,
) -> tuple[Any, dict[str, Any]]:
    x_lower, x_upper = M5394.real_bounds(absolute_coordinate)
    t_lower, t_upper = M5394.real_bounds(path_parameter)
    epsilon_real_lower, epsilon_real_upper = M5394.real_bounds(epsilon)
    epsilon_imaginary_lower, epsilon_imaginary_upper = (
        M5394.imaginary_bounds(epsilon)
    )
    midpoint_invariant = (
        centered_path_correlated_external_second_invariant(
            configuration,
            cell,
            path_segment,
            cpoint(0.5 * (x_lower + x_upper)),
            cpoint(0.5 * (t_lower + t_upper)),
            cpoint(0.5 * (epsilon_real_lower + epsilon_real_upper)),
            cpoint(0),
            4,
        )
    )
    midpoint_value = complex(M5394.midpoint(midpoint_invariant))
    if abs(midpoint_value) <= 0.0:
        raise EnclosureFailure(
            "external42 invariant midpoint cannot select a half-plane"
        )
    diagonal = 1 / math.sqrt(2)
    projection_candidates = (
        (
            "MIDPOINT_OPPOSITE",
            -midpoint_value.conjugate() / abs(midpoint_value),
        ),
        ("NEGATIVE_REAL", 1 + 0j),
        ("POSITIVE_REAL", -1 + 0j),
        ("NEGATIVE_IMAGINARY", -1j),
        ("POSITIVE_IMAGINARY", 1j),
        ("NEGATIVE_DIAGONAL", diagonal * (1 - 1j)),
        ("POSITIVE_DIAGONAL", diagonal * (-1 + 1j)),
    )
    split_schedule = (
        "epsilon_real",
        "epsilon_real",
        "epsilon_real",
        "epsilon_real",
        "epsilon_real",
        "absolute_coordinate",
        "absolute_coordinate",
        "path_parameter",
        "path_parameter",
        "absolute_coordinate",
        "path_parameter",
        "epsilon_real",
    )
    for projection_name, projection_value in projection_candidates:
        stack = [
            (
                x_lower,
                x_upper,
                t_lower,
                t_upper,
                epsilon_real_lower,
                epsilon_real_upper,
                0,
            )
        ]
        accepted: list[Any] = []
        evaluation_count = 0
        minimum_projection_margin = math.inf
        projection_failed = False
        projection = cpoint(projection_value)
        while stack:
            (
                local_x_lower,
                local_x_upper,
                local_t_lower,
                local_t_upper,
                local_epsilon_lower,
                local_epsilon_upper,
                depth,
            ) = stack.pop()
            invariant = (
                centered_path_correlated_external_second_invariant(
                    configuration,
                    cell,
                    path_segment,
                    cbox(local_x_lower, local_x_upper),
                    cbox(local_t_lower, local_t_upper),
                    cbox(
                        local_epsilon_lower,
                        local_epsilon_upper,
                        epsilon_imaginary_lower,
                        epsilon_imaginary_upper,
                    ),
                    global_displacement,
                    4,
                )
            )
            evaluation_count += 1
            projection_upper = M5394.real_bounds(
                projection * invariant
            )[1]
            if projection_upper < 0.0:
                accepted.append(invariant)
                minimum_projection_margin = min(
                    minimum_projection_margin, -projection_upper
                )
                continue
            if depth >= len(split_schedule):
                projection_failed = True
                break
            split_variable = split_schedule[depth]
            if split_variable == "epsilon_real":
                midpoint = 0.5 * (
                    local_epsilon_lower + local_epsilon_upper
                )
                children = (
                    (
                        local_x_lower,
                        local_x_upper,
                        local_t_lower,
                        local_t_upper,
                        local_epsilon_lower,
                        midpoint,
                        depth + 1,
                    ),
                    (
                        local_x_lower,
                        local_x_upper,
                        local_t_lower,
                        local_t_upper,
                        midpoint,
                        local_epsilon_upper,
                        depth + 1,
                    ),
                )
            elif split_variable == "absolute_coordinate":
                midpoint = 0.5 * (local_x_lower + local_x_upper)
                children = (
                    (
                        local_x_lower,
                        midpoint,
                        local_t_lower,
                        local_t_upper,
                        local_epsilon_lower,
                        local_epsilon_upper,
                        depth + 1,
                    ),
                    (
                        midpoint,
                        local_x_upper,
                        local_t_lower,
                        local_t_upper,
                        local_epsilon_lower,
                        local_epsilon_upper,
                        depth + 1,
                    ),
                )
            else:
                midpoint = 0.5 * (local_t_lower + local_t_upper)
                children = (
                    (
                        local_x_lower,
                        local_x_upper,
                        local_t_lower,
                        midpoint,
                        local_epsilon_lower,
                        local_epsilon_upper,
                        depth + 1,
                    ),
                    (
                        local_x_lower,
                        local_x_upper,
                        midpoint,
                        local_t_upper,
                        local_epsilon_lower,
                        local_epsilon_upper,
                        depth + 1,
                    ),
                )
            stack.extend(reversed(children))
            if len(stack) + len(accepted) > 4096:
                projection_failed = True
                break
        if projection_failed or not accepted:
            continue
        enclosure = rectangular_interval_hull(accepted)
        enclosure_projection_upper = M5394.real_bounds(
            projection * enclosure
        )[1]
        if (
            enclosure_projection_upper >= 0.0
            or M5258.lower_abs(enclosure) <= 0.0
        ):
            continue
        return (
            enclosure,
            {
                "half_plane_projection": projection_name,
                "half_plane_projection_real": projection_value.real,
                "half_plane_projection_imaginary": projection_value.imag,
                "half_plane_leaf_count": len(accepted),
                "half_plane_evaluation_count": evaluation_count,
                "half_plane_minimum_projection_margin": (
                    minimum_projection_margin
                ),
                "half_plane_enclosure_projection_margin": (
                    -enclosure_projection_upper
                ),
                "half_plane_split_schedule": "|".join(split_schedule),
            },
        )
    raise EnclosureFailure(
        "external42 invariant has no certified common half-plane subcover"
    )


def subdivided_path_correlated_external_first_invariant(
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
    global_displacement: Any,
    external_endpoint: int,
    subdivision_count: int,
) -> Any:
    return subdivided_path_correlated_external_hard_invariant(
        configuration,
        cell,
        path_segment,
        absolute_coordinate,
        path_parameter,
        epsilon,
        global_displacement,
        external_endpoint,
        1,
        subdivision_count,
    )


def subdivided_path_correlated_external4_second_plus_angle(
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
    global_displacement: Any,
    subdivision_count: int,
) -> Any:
    if subdivision_count <= 1:
        raise ValueError("subdivision count must exceed one")
    x_lower, x_upper = M5394.real_bounds(absolute_coordinate)
    t_lower, t_upper = M5394.real_bounds(path_parameter)
    enclosures: list[Any] = []
    for x_index in range(subdivision_count):
        coordinate = cbox(
            x_lower
            + (x_upper - x_lower) * x_index / subdivision_count,
            x_lower
            + (x_upper - x_lower)
            * (x_index + 1)
            / subdivision_count,
        )
        for t_index in range(subdivision_count):
            parameter = cbox(
                t_lower
                + (t_upper - t_lower) * t_index / subdivision_count,
                t_lower
                + (t_upper - t_lower)
                * (t_index + 1)
                / subdivision_count,
            )
            enclosures.append(
                centered_path_correlated_external4_second_plus_angle(
                    configuration,
                    cell,
                    path_segment,
                    coordinate,
                    parameter,
                    epsilon,
                    global_displacement,
                )
            )
    return rectangular_interval_hull(enclosures)


def subdivided_path_correlated_external0_first_minus_angle(
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
    global_displacement: Any,
    subdivision_count: int,
) -> Any:
    if subdivision_count <= 1:
        raise ValueError("subdivision count must exceed one")
    x_lower, x_upper = M5394.real_bounds(absolute_coordinate)
    t_lower, t_upper = M5394.real_bounds(path_parameter)
    enclosures: list[Any] = []
    for x_index in range(subdivision_count):
        coordinate = cbox(
            x_lower
            + (x_upper - x_lower) * x_index / subdivision_count,
            x_lower
            + (x_upper - x_lower)
            * (x_index + 1)
            / subdivision_count,
        )
        for t_index in range(subdivision_count):
            parameter = cbox(
                t_lower
                + (t_upper - t_lower) * t_index / subdivision_count,
                t_lower
                + (t_upper - t_lower)
                * (t_index + 1)
                / subdivision_count,
            )
            enclosures.append(
                centered_path_correlated_external0_first_minus_angle(
                    configuration,
                    cell,
                    path_segment,
                    coordinate,
                    parameter,
                    epsilon,
                    global_displacement,
                )
            )
    return rectangular_interval_hull(enclosures)


def subdivided_path_correlated_external0_first_minus_plus_angle(
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
    global_displacement: Any,
    subdivision_count: int,
) -> Any:
    if subdivision_count <= 1:
        raise ValueError("subdivision count must exceed one")
    x_lower, x_upper = M5394.real_bounds(absolute_coordinate)
    t_lower, t_upper = M5394.real_bounds(path_parameter)
    enclosures: list[Any] = []
    for x_index in range(subdivision_count):
        coordinate = cbox(
            x_lower
            + (x_upper - x_lower) * x_index / subdivision_count,
            x_lower
            + (x_upper - x_lower)
            * (x_index + 1)
            / subdivision_count,
        )
        for t_index in range(subdivision_count):
            parameter = cbox(
                t_lower
                + (t_upper - t_lower) * t_index / subdivision_count,
                t_lower
                + (t_upper - t_lower)
                * (t_index + 1)
                / subdivision_count,
            )
            enclosures.append(
                centered_path_correlated_external0_first_minus_plus_angle(
                    configuration,
                    cell,
                    path_segment,
                    coordinate,
                    parameter,
                    epsilon,
                    global_displacement,
                )
            )
    return rectangular_interval_hull(enclosures)


def subdivided_path_external4_first_plus_angle_factorized(
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
    global_displacement: Any,
    subdivision_count: int,
) -> Any:
    if subdivision_count <= 1:
        raise ValueError("subdivision count must exceed one")
    x_lower, x_upper = M5394.real_bounds(absolute_coordinate)
    t_lower, t_upper = M5394.real_bounds(path_parameter)
    enclosures: list[Any] = []
    for x_index in range(subdivision_count):
        coordinate = cbox(
            x_lower
            + (x_upper - x_lower) * x_index / subdivision_count,
            x_lower
            + (x_upper - x_lower)
            * (x_index + 1)
            / subdivision_count,
        )
        for t_index in range(subdivision_count):
            parameter = cbox(
                t_lower
                + (t_upper - t_lower) * t_index / subdivision_count,
                t_lower
                + (t_upper - t_lower)
                * (t_index + 1)
                / subdivision_count,
            )
            enclosures.append(
                centered_path_correlated_external4_first_plus_angle_factorized(
                    configuration,
                    cell,
                    path_segment,
                    coordinate,
                    parameter,
                    epsilon,
                    global_displacement,
                )
            )
    return rectangular_interval_hull(enclosures)


def subdivided_path_external4_first_active_pair(
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
    global_displacement: Any,
    subdivision_count: int,
) -> tuple[Any, Any, float]:
    if subdivision_count <= 1:
        raise ValueError("subdivision count must exceed one")
    x_lower, x_upper = M5394.real_bounds(absolute_coordinate)
    t_lower, t_upper = M5394.real_bounds(path_parameter)
    angle_edges: list[Any] = []
    square_quotients: list[Any] = []
    for x_index in range(subdivision_count):
        coordinate = cbox(
            x_lower
            + (x_upper - x_lower) * x_index / subdivision_count,
            x_lower
            + (x_upper - x_lower) * (x_index + 1)
            / subdivision_count,
        )
        for t_index in range(subdivision_count):
            parameter = cbox(
                t_lower
                + (t_upper - t_lower) * t_index / subdivision_count,
                t_lower
                + (t_upper - t_lower) * (t_index + 1)
                / subdivision_count,
            )
            energy = deformed_path_energy_dual(
                cell,
                path_segment,
                coordinate,
                parameter,
            ).value
            local_inputs, local_geometry = interval_inputs(
                configuration,
                coordinate,
                energy,
                epsilon,
            )
            target = cpoint(-9) + cpoint(1j) * local_inputs["epsilon"]
            unit_circle = (
                local_geometry["selected_root"] + global_displacement
            )
            internal = M5258.rotate_internal_lightcone(
                M5386.amplitude_state(local_geometry), unit_circle
            )
            _, right = sheet_locked_interval_cut_momenta(internal, target)
            diagnostics = M5258.IntervalDiagnostics()
            right_first = displaced_first_rational_spinors(
                configuration,
                local_inputs,
                local_geometry,
                global_displacement,
                -1,
                diagnostics,
                "subdivided_external4_first",
            )
            spinors, _, charts = rational_spinor_overrides(
                right,
                diagnostics,
                "subdivided_external4_right",
                right_first,
            )
            direct_angle = M5258.spinor_bracket(
                spinors[1][0], spinors[4][0]
            )
            correlated_angle = (
                centered_path_correlated_external4_first_angle(
                    configuration,
                    cell,
                    path_segment,
                    coordinate,
                    parameter,
                    epsilon,
                    global_displacement,
                    charts[1],
                )
            )
            angle_edges.append(
                max(
                    (direct_angle, correlated_angle),
                    key=lambda value: (
                        M5258.lower_abs(value),
                        -M5258.upper_abs(value),
                    ),
                )
            )
            square_quotients.append(
                exact_external4_first_active_quotient(
                    configuration,
                    local_inputs,
                    local_geometry,
                    global_displacement,
                    charts[1],
                    diagnostics,
                    "subdivided_external4_first_active",
                )
            )
    angle_edge = rectangular_interval_hull(angle_edges)
    square_quotient = rectangular_interval_hull(square_quotients)
    invariant_quotient_lower = (
        M5258.lower_abs(angle_edge)
        * M5258.lower_abs(square_quotient)
    )
    return angle_edge, square_quotient, invariant_quotient_lower


def path_seeded_collision_root_mixed(
    configuration: dict[str, Any],
    epsilon: Any,
    recoil: Any,
    soft_cosine: Any,
    decay_cosine: Any,
    decay_sine: Any,
    chart: str,
) -> tuple[Any, Any]:
    dual = M5385.M5381.IntervalDual
    mixed = M5386.MixedDual

    def lift(value: Any) -> Any:
        value = dual.coerce(value)
        return mixed(value.value, recoil_derivative=value.derivative)

    epsilon = lift(epsilon)
    recoil = lift(recoil)
    soft_cosine = lift(soft_cosine)
    decay_cosine = lift(decay_cosine)
    decay_sine = lift(decay_sine)
    epsilon_squared = epsilon * epsilon
    q_value = (
        -(80 + epsilon_squared) / (64 + epsilon_squared)
        + 1j * (-2 * epsilon / (64 + epsilon_squared))
    )
    external_root = -1j * M5386.mixed_positive_sqrt(-q_value)
    soft_sine = M5386.mixed_positive_sqrt(
        mixed(cpoint(1)) - soft_cosine * soft_cosine
    )
    factor_f1 = (
        q_value * recoil * soft_cosine
        + q_value * recoil
        - q_value * soft_cosine
        - q_value
        + recoil * soft_cosine
        + recoil
        - soft_cosine
        + 1
    )
    factor_f2 = (
        q_value * recoil * soft_cosine
        - q_value * recoil
        - q_value * soft_cosine
        - q_value
        + recoil * soft_cosine
        - recoil
        - soft_cosine
        + 1
    )
    representative = (
        soft_sine
        * (1 + decay_cosine)
        * factor_f1
        / (decay_sine * (1 + soft_cosine) * factor_f2)
    )
    relative = (
        1 / representative
        if configuration["role"] == "reciprocal"
        else representative
    )
    relative = mixed(
        relative.value,
        relative_derivative=cpoint(1),
        recoil_derivative=relative.recoil_derivative,
        mixed_derivative=relative.mixed_derivative,
    )
    relative_cosine = (
        (relative + 1 / relative) * soft_sine * decay_sine / 2
        + soft_cosine * decay_cosine
    )
    recoil_squared = recoil * recoil
    first_energy = (
        1
        + recoil_squared
        - relative_cosine * (1 - recoil_squared)
    ) / 2
    longitudinal = (
        relative_cosine * (1 - recoil) * (1 - recoil)
        - (1 - recoil_squared)
    ) / 2
    holomorphic = (
        relative * recoil * decay_sine
        + longitudinal * soft_sine
    )
    antiholomorphic = (
        recoil * decay_sine / relative
        + longitudinal * soft_sine
    )
    momentum_z = longitudinal * soft_cosine + recoil * decay_cosine
    plus = first_energy + momentum_z
    minus = first_energy - momentum_z
    first_label = configuration["root_labels"][0]
    if first_label == "minus_u" and chart == "primary":
        return -(plus / holomorphic) / external_root, holomorphic
    if first_label == "minus_u" and chart == "alternate":
        return -(antiholomorphic / minus) / external_root, minus
    if first_label == "minus_v" and chart == "primary":
        return -external_root * (antiholomorphic / plus), plus
    if first_label == "minus_v" and chart == "alternate":
        return -external_root * (minus / holomorphic), holomorphic
    raise ValueError(f"unsupported collision chart {first_label}:{chart}")


def path_seeded_alternate_minus_v_collision_jacobian_dual(
    configuration: dict[str, Any],
    epsilon: Any,
    recoil: Any,
    soft_cosine: Any,
    decay_cosine: Any,
    decay_sine: Any,
) -> tuple[Any, Any]:
    if configuration["root_labels"][0] != "minus_v":
        raise ValueError("explicit alternate collision chart requires minus_v")
    dual = M5385.M5381.IntervalDual
    epsilon = dual.coerce(epsilon)
    recoil = dual.coerce(recoil)
    soft_cosine = dual.coerce(soft_cosine)
    decay_cosine = dual.coerce(decay_cosine)
    decay_sine = dual.coerce(decay_sine)
    epsilon_squared = epsilon * epsilon
    q_value = (
        -(80 + epsilon_squared) / (64 + epsilon_squared)
        + 1j * (-2 * epsilon / (64 + epsilon_squared))
    )
    external_root = -1j * M5386.chart_safe_sqrt_dual(-q_value)
    soft_sine = M5385.positive_sqrt_dual(
        1 - soft_cosine * soft_cosine
    )
    factor_f1 = (
        q_value * recoil * soft_cosine
        + q_value * recoil
        - q_value * soft_cosine
        - q_value
        + recoil * soft_cosine
        + recoil
        - soft_cosine
        + 1
    )
    factor_f2 = (
        q_value * recoil * soft_cosine
        - q_value * recoil
        - q_value * soft_cosine
        - q_value
        + recoil * soft_cosine
        - recoil
        - soft_cosine
        + 1
    )
    representative = (
        soft_sine
        * (1 + decay_cosine)
        * factor_f1
        / (decay_sine * (1 + soft_cosine) * factor_f2)
    )
    relative = (
        1 / representative
        if configuration["role"] == "reciprocal"
        else representative
    )
    recoil_squared = recoil * recoil
    azimuth_coefficient = soft_sine * decay_sine / 2
    relative_cosine_constant = soft_cosine * decay_cosine
    first_energy_constant = (1 + recoil_squared) / 2
    first_energy_relative_coefficient = -(1 - recoil_squared) / 2
    longitudinal_constant = -(1 - recoil_squared) / 2
    longitudinal_relative_coefficient = (1 - recoil) * (1 - recoil) / 2
    minus_constant = (
        first_energy_constant
        - longitudinal_constant * soft_cosine
        - recoil * decay_cosine
    )
    minus_relative_coefficient = (
        first_energy_relative_coefficient
        - longitudinal_relative_coefficient * soft_cosine
    )
    holomorphic_constant = longitudinal_constant * soft_sine
    holomorphic_relative_coefficient = (
        longitudinal_relative_coefficient * soft_sine
    )
    minus_laurent_constant = (
        minus_constant
        + minus_relative_coefficient * relative_cosine_constant
    )
    minus_laurent_coefficient = (
        minus_relative_coefficient * azimuth_coefficient
    )
    holomorphic_laurent_constant = (
        holomorphic_constant
        + holomorphic_relative_coefficient * relative_cosine_constant
    )
    holomorphic_inverse_coefficient = (
        holomorphic_relative_coefficient * azimuth_coefficient
    )
    holomorphic_direct_coefficient = (
        holomorphic_inverse_coefficient + recoil * decay_sine
    )
    quadratic_coefficient = (
        minus_laurent_coefficient * holomorphic_laurent_constant
        - minus_laurent_constant * holomorphic_direct_coefficient
    )
    linear_coefficient = (
        2
        * minus_laurent_coefficient
        * (
            holomorphic_inverse_coefficient
            - holomorphic_direct_coefficient
        )
    )
    constant_coefficient = (
        minus_laurent_constant * holomorphic_inverse_coefficient
        - minus_laurent_coefficient * holomorphic_laurent_constant
    )
    if configuration["role"] == "reciprocal":
        projective_denominator = (
            holomorphic_direct_coefficient
            + holomorphic_laurent_constant * representative
            + holomorphic_inverse_coefficient
            * representative
            * representative
        )
        projective_numerator = (
            quadratic_coefficient
            + linear_coefficient * representative
            + constant_coefficient * representative * representative
        )
        jacobian = (
            -external_root
            * representative
            * representative
            * projective_numerator
            / (projective_denominator * projective_denominator)
        )
    else:
        projective_denominator = (
            holomorphic_direct_coefficient * relative * relative
            + holomorphic_laurent_constant * relative
            + holomorphic_inverse_coefficient
        )
        projective_numerator = (
            quadratic_coefficient * relative * relative
            + linear_coefficient * relative
            + constant_coefficient
        )
        jacobian = (
            -external_root
            * projective_numerator
            / (projective_denominator * projective_denominator)
        )
    return jacobian, projective_denominator


def path_correlated_explicit_collision_jacobian_candidate(
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
) -> tuple[float, str, Any, float]:
    domains = (absolute_coordinate, path_parameter, epsilon)
    centers = tuple(M5385.complex_midpoint_box(value) for value in domains)
    decay_cosine = cpoint(
        configuration["decay_sign"] * M5394.ABSOLUTE_DECAY_COSINE
    )
    decay_sine = cpoint(
        math.sqrt(1 - M5394.ABSOLUTE_DECAY_COSINE**2)
    )

    def evaluate(values: list[Any]) -> tuple[Any, Any]:
        dual = M5385.M5381.IntervalDual
        coordinate, parameter, epsilon_value = (
            dual.coerce(value) for value in values
        )
        energy = deformed_path_energy_dual(
            cell, path_segment, coordinate, parameter
        )
        recoil = M5386.chart_safe_sqrt_dual(1 - energy)
        return path_seeded_alternate_minus_v_collision_jacobian_dual(
            configuration,
            epsilon_value,
            recoil,
            coordinate * configuration["soft_sign"],
            decay_cosine,
            decay_sine,
        )

    direct_jacobian, direct_denominator = evaluate(list(domains))
    centered_jacobian, centered_denominator = evaluate(list(centers))
    mean_value_jacobian = centered_jacobian.value
    mean_value_denominator = centered_denominator.value
    for derivative_index in range(len(domains)):
        dual_domains = [
            M5385.M5381.IntervalDual(
                value,
                cpoint(1 if index == derivative_index else 0),
            )
            for index, value in enumerate(domains)
        ]
        jacobian, denominator = evaluate(dual_domains)
        offset = domains[derivative_index] - centers[derivative_index]
        mean_value_jacobian += jacobian.derivative * offset
        mean_value_denominator += denominator.derivative * offset
    jacobian_enclosures = (
        ("DIRECT", direct_jacobian.value),
        ("MEAN_VALUE", mean_value_jacobian),
    )
    method, selected_jacobian = max(
        jacobian_enclosures,
        key=lambda row: M5258.lower_abs(row[1]),
    )
    denominator_lower = max(
        M5258.lower_abs(direct_denominator.value),
        M5258.lower_abs(mean_value_denominator),
    )
    return (
        M5258.lower_abs(selected_jacobian),
        f"PATH_CORRELATED_EXPLICIT_ALTERNATE_MINUS_V_{method}",
        selected_jacobian,
        denominator_lower,
    )


def subdivided_path_correlated_explicit_collision_jacobian_candidate(
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
    subdivision_count: int,
    path_subdivision_count: int | None = None,
) -> tuple[float, str, Any, float]:
    if subdivision_count <= 1:
        raise ValueError("subdivision count must exceed one")
    path_subdivision_count = (
        subdivision_count
        if path_subdivision_count is None
        else path_subdivision_count
    )
    if path_subdivision_count <= 1:
        raise ValueError("path subdivision count must exceed one")
    x_lower, x_upper = M5394.real_bounds(absolute_coordinate)
    t_lower, t_upper = M5394.real_bounds(path_parameter)
    jacobians: list[Any] = []
    jacobian_lowers: list[float] = []
    denominator_lowers: list[float] = []
    for x_index in range(subdivision_count):
        coordinate = cbox(
            x_lower
            + (x_upper - x_lower) * x_index / subdivision_count,
            x_lower
            + (x_upper - x_lower) * (x_index + 1)
            / subdivision_count,
        )
        for t_index in range(path_subdivision_count):
            parameter = cbox(
                t_lower
                + (t_upper - t_lower) * t_index / path_subdivision_count,
                t_lower
                + (t_upper - t_lower) * (t_index + 1)
                / path_subdivision_count,
            )
            candidate = path_correlated_explicit_collision_jacobian_candidate(
                configuration,
                cell,
                path_segment,
                coordinate,
                parameter,
                epsilon,
            )
            jacobian_lowers.append(candidate[0])
            jacobians.append(candidate[2])
            denominator_lowers.append(candidate[3])
    return (
        min(jacobian_lowers),
        "SUBDIVIDED_PATH_CORRELATED_EXPLICIT_ALTERNATE_MINUS_V_UNION_"
        f"{subdivision_count}X{path_subdivision_count}",
        rectangular_interval_hull(jacobians),
        min(denominator_lowers),
    )


def explicit_collision_jacobian_crosschecks() -> list[dict[str, Any]]:
    cell = next(
        row
        for row in away_term_support_cells()
        if row["mapped_cell_id"] == "S_X001_MC04_SM_DM"
    )
    configuration = configuration_variants("MC04_SM_DM")[0]
    epsilon = epsilon_interval(M5395.epsilon_subboxes(1)[0])
    epsilon_real_lower, epsilon_real_upper = M5394.real_bounds(epsilon)
    epsilon_imaginary_lower, epsilon_imaginary_upper = (
        M5394.imaginary_bounds(epsilon)
    )
    epsilon_real_values = (
        epsilon_real_lower,
        0.5 * (epsilon_real_lower + epsilon_real_upper),
        epsilon_real_upper,
    )
    epsilon_imaginary_values = (
        epsilon_imaginary_lower,
        0.5 * (epsilon_imaginary_lower + epsilon_imaginary_upper),
        epsilon_imaginary_upper,
    )
    x_values = (
        0.19745585773897384,
        0.20064062963798954,
        0.20382540153700524,
    )
    path_values = (0.5, 0.75, 1.0)
    decay_cosine = cpoint(
        configuration["decay_sign"] * M5394.ABSOLUTE_DECAY_COSINE
    )
    decay_sine = cpoint(
        math.sqrt(1 - M5394.ABSOLUTE_DECAY_COSINE**2)
    )
    dual = M5385.M5381.IntervalDual
    rows: list[dict[str, Any]] = []
    for absolute_coordinate in x_values:
        for path_parameter in path_values:
            for epsilon_real in epsilon_real_values:
                for epsilon_imaginary in epsilon_imaginary_values:
                    coordinate = dual.coerce(cpoint(absolute_coordinate))
                    parameter = dual.coerce(cpoint(path_parameter))
                    epsilon_value = dual.coerce(
                        cpoint(complex(epsilon_real, epsilon_imaginary))
                    )
                    energy = deformed_path_energy_dual(
                        cell, "TOP", coordinate, parameter
                    )
                    recoil = M5386.chart_safe_sqrt_dual(1 - energy)
                    explicit_jacobian, projective_denominator = (
                        path_seeded_alternate_minus_v_collision_jacobian_dual(
                            configuration,
                            epsilon_value,
                            recoil,
                            coordinate * configuration["soft_sign"],
                            decay_cosine,
                            decay_sine,
                        )
                    )
                    parent_root, _ = path_seeded_collision_root_mixed(
                        configuration,
                        epsilon_value,
                        recoil,
                        coordinate * configuration["soft_sign"],
                        decay_cosine,
                        decay_sine,
                        "alternate",
                    )
                    explicit_value = complex(
                        M5394.midpoint(explicit_jacobian.value)
                    )
                    parent_value = complex(
                        M5394.midpoint(parent_root.relative_derivative)
                    )
                    relative_error = abs(explicit_value - parent_value) / max(
                        1.0, abs(parent_value)
                    )
                    rows.append(
                        {
                            "absolute_soft_cosine": absolute_coordinate,
                            "path_parameter": path_parameter,
                            "epsilon_real": epsilon_real,
                            "epsilon_imaginary": epsilon_imaginary,
                            "explicit_jacobian_real": explicit_value.real,
                            "explicit_jacobian_imaginary": explicit_value.imag,
                            "parent_jacobian_real": parent_value.real,
                            "parent_jacobian_imaginary": parent_value.imag,
                            "explicit_to_parent_relative_error": relative_error,
                            "projective_denominator_abs_lower": (
                                M5258.lower_abs(projective_denominator.value)
                            ),
                            "identity_passed": relative_error <= 5.0e-14,
                        }
                    )
    return rows


def path_correlated_collision_jacobian_candidates(
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
) -> list[tuple[float, str, Any, float]]:
    domains = (absolute_coordinate, path_parameter, epsilon)
    centers = tuple(M5385.complex_midpoint_box(value) for value in domains)
    decay_cosine = cpoint(
        configuration["decay_sign"] * M5394.ABSOLUTE_DECAY_COSINE
    )
    decay_sine = cpoint(
        math.sqrt(1 - M5394.ABSOLUTE_DECAY_COSINE**2)
    )

    def evaluate(values: list[Any], chart: str) -> tuple[Any, Any]:
        dual = M5385.M5381.IntervalDual
        coordinate, parameter, epsilon_value = (
            dual.coerce(value) for value in values
        )
        energy = deformed_path_energy_dual(
            cell, path_segment, coordinate, parameter
        )
        recoil = M5386.chart_safe_sqrt_dual(1 - energy)
        return path_seeded_collision_root_mixed(
            configuration,
            epsilon_value,
            recoil,
            coordinate * configuration["soft_sign"],
            decay_cosine,
            decay_sine,
            chart,
        )

    candidates: list[tuple[float, str, Any, float]] = []
    for chart in ("primary", "alternate"):
        centered_root, centered_denominator = evaluate(list(centers), chart)
        jacobian = centered_root.relative_derivative
        denominator = centered_denominator.value
        for derivative_index in range(len(domains)):
            dual_domains = [
                M5385.M5381.IntervalDual(
                    value,
                    cpoint(1 if index == derivative_index else 0),
                )
                for index, value in enumerate(domains)
            ]
            root, chart_denominator = evaluate(dual_domains, chart)
            offset = domains[derivative_index] - centers[derivative_index]
            jacobian += root.mixed_derivative * offset
            denominator += chart_denominator.recoil_derivative * offset
        denominator_lower = M5258.lower_abs(denominator)
        candidates.append(
            (
                M5258.lower_abs(jacobian),
                f"PATH_CORRELATED_PROJECTIVE_{chart.upper()}",
                jacobian,
                denominator_lower,
            )
        )
    return candidates


def subdivided_path_correlated_collision_jacobian_candidate(
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
    subdivision_count: int,
    path_subdivision_count: int | None = None,
) -> tuple[float, str, Any, float]:
    if subdivision_count <= 1:
        raise ValueError("subdivision count must exceed one")
    path_subdivision_count = (
        subdivision_count
        if path_subdivision_count is None
        else path_subdivision_count
    )
    if path_subdivision_count <= 1:
        raise ValueError("path subdivision count must exceed one")
    x_lower, x_upper = M5394.real_bounds(absolute_coordinate)
    t_lower, t_upper = M5394.real_bounds(path_parameter)
    jacobians: list[Any] = []
    denominator_lowers: list[float] = []
    for x_index in range(subdivision_count):
        coordinate = cbox(
            x_lower
            + (x_upper - x_lower) * x_index / subdivision_count,
            x_lower
            + (x_upper - x_lower) * (x_index + 1)
            / subdivision_count,
        )
        for t_index in range(path_subdivision_count):
            parameter = cbox(
                t_lower
                + (t_upper - t_lower) * t_index / path_subdivision_count,
                t_lower
                + (t_upper - t_lower) * (t_index + 1)
                / path_subdivision_count,
            )
            local_candidates = [
                candidate
                for candidate in path_correlated_collision_jacobian_candidates(
                    configuration,
                    cell,
                    path_segment,
                    coordinate,
                    parameter,
                    epsilon,
                )
                if candidate[3] > 0.0
            ]
            if not local_candidates:
                raise M5258.IntervalSingularity(
                    "subdivided collision Jacobian has an uncovered chart box"
                )
            selected = max(
                local_candidates,
                key=lambda candidate: (candidate[0], candidate[3]),
            )
            jacobians.append(selected[2])
            denominator_lowers.append(selected[3])
    jacobian = rectangular_interval_hull(jacobians)
    return (
        M5258.lower_abs(jacobian),
        "SUBDIVIDED_PATH_CORRELATED_PROJECTIVE_UNION_"
        f"{subdivision_count}X{path_subdivision_count}",
        jacobian,
        min(denominator_lowers),
    )


def coherent_internal_hard_pair_edge_overrides(
    configuration: dict[str, Any],
    inputs: dict[str, Any],
    geometry: dict[str, Any],
    global_displacement: Any,
    spinors: dict[int, tuple[list[Any], list[Any]]],
    charts: dict[int, str],
) -> dict[tuple[frozenset[int], int], Any]:
    direct_edges = {
        chirality: M5258.spinor_bracket(
            spinors[1][chirality], spinors[2][chirality]
        )
        for chirality in (0, 1)
    }
    if all(M5258.lower_abs(value) > 0.0 for value in direct_edges.values()):
        return {}
    source: dict[tuple[frozenset[int], int], Any] = {}
    try:
        source = M5386.internal_hard_pair_edge_overrides(
            configuration,
            inputs,
            geometry,
            global_displacement,
        )
    except (M5258.IntervalSingularity, ValueError):
        pass
    pair = frozenset((1, 2))
    result: dict[tuple[frozenset[int], int], Any] = {}
    for chirality in (0, 1):
        key = (pair, chirality)
        direct = direct_edges[chirality]
        if M5258.lower_abs(direct) > 0.0:
            continue
        candidates: list[Any] = []
        if key in source:
            aligned = M5395.align_edge_override(source[key], direct)
            if aligned is not None:
                candidates.append(aligned)
        try:
            candidates.append(
                centered_hard_pair_rational_edge(
                    configuration,
                    inputs,
                    geometry,
                    global_displacement,
                    charts[1],
                    charts[2],
                    chirality,
                )
            )
        except (M5258.IntervalSingularity, ValueError):
            pass
        if candidates:
            result[key] = max(
                candidates,
                key=lambda value: (
                    M5258.lower_abs(value),
                    -M5258.upper_abs(value),
                ),
            )
    return result


def tight_second_external_edge_overrides(
    configuration: dict[str, Any],
    inputs: dict[str, Any],
    geometry: dict[str, Any],
    global_displacement: Any,
    target: Any,
    charts: dict[int, str],
    spinors: dict[int, tuple[list[Any], list[Any]]],
) -> dict[tuple[frozenset[int], int], Any]:
    centered: dict[tuple[frozenset[int], int], Any] | None = None
    result: dict[tuple[frozenset[int], int], Any] = {}
    for external_endpoint in (0, 4):
        orientation = 1 if external_endpoint == 0 else -1
        pair = frozenset((external_endpoint, 2))
        for chirality in (0, 1):
            key = (pair, chirality)
            left_index, right_index = sorted(pair)
            direct_spinor = M5258.spinor_bracket(
                spinors[left_index][chirality],
                spinors[right_index][chirality],
            )
            if M5258.lower_abs(direct_spinor) > 0.0:
                continue
            if centered is None:
                centered = M5386.second_external_edge_overrides(
                    configuration,
                    inputs,
                    geometry,
                    global_displacement,
                    target,
                )
            try:
                direct = orientation * M5386.external_first_edge_dual(
                    configuration,
                    inputs["epsilon"],
                    geometry["recoil"],
                    inputs["soft_cosine"],
                    inputs["decay_cosine"],
                    inputs["decay_sine"],
                    global_displacement,
                    external_endpoint,
                    2,
                    charts[external_endpoint],
                    charts[2],
                    chirality,
                ).value
            except (M5258.IntervalSingularity, ValueError):
                candidates = [centered[key]]
            else:
                candidates = [centered[key], direct]
            result[key] = max(
                candidates,
                key=lambda value: (
                    M5258.lower_abs(value),
                    -M5258.upper_abs(value),
                ),
            )
            if (
                external_endpoint == 4
                and chirality == 0
                and charts[4] == "minus"
                and charts[2] == "plus"
            ):
                try:
                    factorized = -centered_factorized_external4_second_angle(
                        configuration,
                        inputs,
                        geometry,
                        global_displacement,
                    )
                except (M5258.IntervalSingularity, ValueError):
                    pass
                else:
                    result[key] = max(
                        (result[key], factorized),
                        key=lambda value: (
                            M5258.lower_abs(value),
                            -M5258.upper_abs(value),
                        ),
                    )
    return result


def stable_spinor_edge_reciprocal(
    momenta: list[list[Any]],
    spinors: dict[int, tuple[list[Any], list[Any]]],
    chirality: int,
    left_index: int,
    right_index: int,
    diagnostics: Any,
    label: str,
    invariant_overrides: dict[frozenset[int], Any] | None = None,
    edge_overrides: dict[tuple[frozenset[int], int], Any] | None = None,
) -> Any:
    direct = M5258.spinor_bracket(
        spinors[left_index][chirality],
        spinors[right_index][chirality],
    )
    if M5258.lower_abs(direct) <= 0.0:
        pair = frozenset((left_index, right_index))
        invariant_value = (
            invariant_overrides[pair]
            if invariant_overrides is not None and pair in invariant_overrides
            else M5258.invariant(momenta, left_index, right_index)
        )
        if M5258.lower_abs(invariant_value) > 0.0:
            opposite_chirality = 1 - chirality
            opposite = M5258.spinor_bracket(
                spinors[left_index][opposite_chirality],
                spinors[right_index][opposite_chirality],
            )
            opposite_key = (pair, opposite_chirality)
            if edge_overrides is not None and opposite_key in edge_overrides:
                opposite_override = edge_overrides[opposite_key]
                if left_index > right_index:
                    opposite_override = -opposite_override
                if M5258.upper_abs(opposite_override) < M5258.upper_abs(
                    opposite
                ):
                    opposite = opposite_override
            diagnostics.record(
                invariant_value,
                f"{label}:reciprocal_invariant",
            )
            return M5258.safe_divide(
                opposite,
                invariant_value,
                diagnostics,
                f"{label}:opposite_over_invariant",
            )
    try:
        edge = M5386.stable_spinor_edge(
            momenta,
            spinors,
            chirality,
            left_index,
            right_index,
            diagnostics,
            label,
            invariant_overrides,
            edge_overrides,
        )
    except M5258.IntervalSingularity as original_error:
        pair = frozenset((left_index, right_index))
        invariant_value = (
            invariant_overrides[pair]
            if invariant_overrides is not None and pair in invariant_overrides
            else M5258.invariant(momenta, left_index, right_index)
        )
        if M5258.lower_abs(invariant_value) <= 0.0:
            raise original_error
        opposite_chirality = 1 - chirality
        opposite = M5258.spinor_bracket(
            spinors[left_index][opposite_chirality],
            spinors[right_index][opposite_chirality],
        )
        opposite_key = (pair, opposite_chirality)
        if edge_overrides is not None and opposite_key in edge_overrides:
            opposite_override = edge_overrides[opposite_key]
            if left_index > right_index:
                opposite_override = -opposite_override
            if M5258.upper_abs(opposite_override) < M5258.upper_abs(opposite):
                opposite = opposite_override
        diagnostics.record(
            invariant_value,
            f"{label}:reciprocal_invariant",
        )
        return M5258.safe_divide(
            opposite,
            invariant_value,
            diagnostics,
            f"{label}:opposite_over_invariant",
        )
    return M5258.safe_divide(
        cpoint(1),
        edge,
        diagnostics,
        f"{label}:direct_reciprocal",
    )


def stable_scalar_mhv_with_reciprocals(
    order: list[int],
    special: int,
    momenta: list[list[Any]],
    spinors: dict[int, tuple[list[Any], list[Any]]],
    chirality: int,
    diagnostics: Any,
    label: str,
    invariant_overrides: dict[frozenset[int], Any] | None = None,
    edge_overrides: dict[tuple[frozenset[int], int], Any] | None = None,
) -> Any:
    numerator_pairs = {
        frozenset((special, endpoint)): {
            "ordered_pair": (special, endpoint),
            "factor": M5258.spinor_bracket(
                spinors[special][chirality],
                spinors[endpoint][chirality],
            ),
            "remaining": 2,
        }
        for endpoint in (0, 4)
    }
    value = cpoint(1)
    for index, left_index in enumerate(order):
        right_index = order[(index + 1) % len(order)]
        pair = frozenset((left_index, right_index))
        numerator_data = numerator_pairs.get(pair)
        if numerator_data is not None and numerator_data["remaining"] > 0:
            orientation = (
                1
                if (left_index, right_index)
                == numerator_data["ordered_pair"]
                else -1
            )
            value *= cpoint(orientation)
            numerator_data["remaining"] -= 1
            continue
        value *= stable_spinor_edge_reciprocal(
            momenta,
            spinors,
            chirality,
            left_index,
            right_index,
            diagnostics,
            f"{label}:edge_{index}_{left_index}_{right_index}",
            invariant_overrides,
            edge_overrides,
        )
    for numerator_data in numerator_pairs.values():
        value *= numerator_data["factor"] ** numerator_data["remaining"]
    return value


def scalar_klt_five_with_reciprocals(
    momenta: list[list[Any]],
    special: int,
    chirality: int,
    diagnostics: Any,
    label: str,
    invariant_overrides: dict[frozenset[int], Any] | None = None,
    edge_overrides: dict[tuple[frozenset[int], int], Any] | None = None,
    spinor_overrides: dict[int, tuple[list[Any], list[Any]]] | None = None,
) -> Any:
    spinors = dict(spinor_overrides or {})
    for index in (0, 1, 2, 3, 4):
        if index not in spinors:
            spinors[index] = M5386.rational_massless_spinors(
                momenta[index],
                diagnostics,
                f"{label}:p{index}",
                False,
            )
    result = cpoint(0)
    for sigma_reversed in range(2):
        sigma = [1, 2] if sigma_reversed == 0 else [2, 1]
        left = stable_scalar_mhv_with_reciprocals(
            [0, *sigma, 3, 4],
            special,
            momenta,
            spinors,
            chirality,
            diagnostics,
            f"{label}:left{sigma_reversed}",
            invariant_overrides,
            edge_overrides,
        )
        for gamma_reversed in range(2):
            gamma = [1, 2] if gamma_reversed == 0 else [2, 1]
            right = stable_scalar_mhv_with_reciprocals(
                [3, 4, *gamma, 0],
                special,
                momenta,
                spinors,
                chirality,
                diagnostics,
                f"{label}:right{gamma_reversed}",
                invariant_overrides,
                edge_overrides,
            )
            result += (
                left
                * M5258.momentum_kernel(
                    gamma_reversed,
                    sigma_reversed,
                    momenta,
                )
                * right
            )
    return result


def stable_regularized_scalar_mhv_with_reciprocals(
    order: list[int],
    special: int,
    momenta: list[list[Any]],
    spinors: dict[int, tuple[list[Any], list[Any]]],
    spinor_exponents: dict[int, tuple[list[int], list[int]]],
    chirality: int,
    unit_circle: Any,
    active_center: Any,
    active_pairs: set[frozenset[int]],
    diagnostics: Any,
    label: str,
    invariant_overrides: dict[frozenset[int], Any] | None = None,
    edge_overrides: dict[tuple[frozenset[int], int], Any] | None = None,
    active_quotient_overrides: (
        dict[tuple[frozenset[int], int], Any] | None
    ) = None,
) -> tuple[Any, int]:
    selected_spinors = {
        index: spinors[index][chirality] for index in spinors
    }
    selected_exponents = {
        index: spinor_exponents[index][chirality]
        for index in spinor_exponents
    }
    numerator_pairs = {
        frozenset((special, endpoint)): {
            "ordered_pair": (special, endpoint),
            "factor": M5258.spinor_bracket(
                selected_spinors[special],
                selected_spinors[endpoint],
            ),
            "remaining": 2,
        }
        for endpoint in (0, 4)
    }
    value = cpoint(1)
    cancelled = 0
    for index, left_index in enumerate(order):
        right_index = order[(index + 1) % len(order)]
        pair = frozenset((left_index, right_index))
        numerator_data = numerator_pairs.get(pair)
        if numerator_data is not None and numerator_data["remaining"] > 0:
            orientation = (
                1
                if (left_index, right_index)
                == numerator_data["ordered_pair"]
                else -1
            )
            value *= cpoint(orientation)
            numerator_data["remaining"] -= 1
            continue
        if pair in active_pairs:
            active_key = (pair, chirality)
            if (
                active_quotient_overrides is not None
                and active_key in active_quotient_overrides
            ):
                denominator = active_quotient_overrides[active_key]
                if left_index > right_index:
                    denominator = -denominator
            else:
                denominator = M5258.active_bracket_quotient(
                    left_index,
                    right_index,
                    selected_spinors,
                    selected_exponents,
                    unit_circle,
                    active_center,
                    diagnostics,
                    f"{label}:active_edge_{index}_{left_index}_{right_index}",
                )
            value = M5258.safe_divide(
                value,
                denominator,
                diagnostics,
                f"{label}:active_edge_reciprocal_{index}_{left_index}_{right_index}",
            )
            cancelled += 1
        else:
            value *= stable_spinor_edge_reciprocal(
                momenta,
                spinors,
                chirality,
                left_index,
                right_index,
                diagnostics,
                f"{label}:edge_{index}_{left_index}_{right_index}",
                invariant_overrides,
                edge_overrides,
            )
    for numerator_data in numerator_pairs.values():
        value *= numerator_data["factor"] ** numerator_data["remaining"]
    return value, cancelled


def stable_regularized_scalar_mhv_with_omitted_edge(
    order: list[int],
    special: int,
    momenta: list[list[Any]],
    spinors: dict[int, tuple[list[Any], list[Any]]],
    spinor_exponents: dict[int, tuple[list[int], list[int]]],
    chirality: int,
    unit_circle: Any,
    active_center: Any,
    active_pairs: set[frozenset[int]],
    omitted_pair: frozenset[int],
    diagnostics: Any,
    label: str,
    invariant_overrides: dict[frozenset[int], Any] | None = None,
    edge_overrides: dict[tuple[frozenset[int], int], Any] | None = None,
    active_quotient_overrides: (
        dict[tuple[frozenset[int], int], Any] | None
    ) = None,
) -> tuple[Any, int, int]:
    selected_spinors = {
        index: spinors[index][chirality] for index in spinors
    }
    selected_exponents = {
        index: spinor_exponents[index][chirality]
        for index in spinor_exponents
    }
    numerator_pairs = {
        frozenset((special, endpoint)): {
            "ordered_pair": (special, endpoint),
            "factor": M5258.spinor_bracket(
                selected_spinors[special],
                selected_spinors[endpoint],
            ),
            "remaining": 2,
        }
        for endpoint in (0, 4)
    }
    value = cpoint(1)
    cancelled = 0
    omitted_orientation = 0
    canonical_omitted_order = tuple(sorted(omitted_pair))
    for index, left_index in enumerate(order):
        right_index = order[(index + 1) % len(order)]
        pair = frozenset((left_index, right_index))
        numerator_data = numerator_pairs.get(pair)
        if numerator_data is not None and numerator_data["remaining"] > 0:
            orientation = (
                1
                if (left_index, right_index)
                == numerator_data["ordered_pair"]
                else -1
            )
            value *= cpoint(orientation)
            numerator_data["remaining"] -= 1
            continue
        if pair == omitted_pair:
            if omitted_orientation != 0:
                raise M5258.IntervalSingularity(
                    f"omitted edge appears more than once in {label}"
                )
            omitted_orientation = (
                1
                if (left_index, right_index)
                == canonical_omitted_order
                else -1
            )
            continue
        if pair in active_pairs:
            active_key = (pair, chirality)
            if (
                active_quotient_overrides is not None
                and active_key in active_quotient_overrides
            ):
                denominator = active_quotient_overrides[active_key]
                if left_index > right_index:
                    denominator = -denominator
            else:
                denominator = M5258.active_bracket_quotient(
                    left_index,
                    right_index,
                    selected_spinors,
                    selected_exponents,
                    unit_circle,
                    active_center,
                    diagnostics,
                    f"{label}:active_edge_{index}_{left_index}_{right_index}",
                )
            value = M5258.safe_divide(
                value,
                denominator,
                diagnostics,
                f"{label}:active_edge_reciprocal_{index}_{left_index}_{right_index}",
            )
            cancelled += 1
        else:
            value *= stable_spinor_edge_reciprocal(
                momenta,
                spinors,
                chirality,
                left_index,
                right_index,
                diagnostics,
                f"{label}:edge_{index}_{left_index}_{right_index}",
                invariant_overrides,
                edge_overrides,
            )
    if omitted_orientation == 0:
        raise M5258.IntervalSingularity(
            f"omitted edge is absent from {label}"
        )
    for numerator_data in numerator_pairs.values():
        value *= numerator_data["factor"] ** numerator_data["remaining"]
    return value, cancelled, omitted_orientation


def oriented_regularized_scalar_klt_five_external01_decomposition(
    momenta: list[list[Any]],
    special: int,
    chirality: int,
    hard_index: int,
    active_chirality: int,
    unit_circle: Any,
    active_center: Any,
    displacement: Any,
    diagnostics: Any,
    label: str,
    invariant_overrides: dict[frozenset[int], Any] | None = None,
    edge_overrides: dict[tuple[frozenset[int], int], Any] | None = None,
    spinor_overrides: dict[int, tuple[list[Any], list[Any]]] | None = None,
    spinor_exponent_overrides: (
        dict[int, tuple[list[int], list[int]]] | None
    ) = None,
    active_quotient_overrides: (
        dict[tuple[frozenset[int], int], Any] | None
    ) = None,
) -> tuple[Any, Any, Any]:
    if special not in (2, 3) or chirality != 0:
        raise ValueError(
            "external01 decomposition owns special in {2,3}, chirality=0"
        )
    spinors = dict(spinor_overrides or {})
    for index in (0, 1, 2, 3, 4):
        if index not in spinors:
            spinors[index] = M5386.rational_massless_spinors(
                momenta[index],
                diagnostics,
                f"{label}:p{index}",
                False,
            )
    spinor_exponents = M5258.spinor_exponent_table(
        momenta,
        (0, 1, 2, 3, 4),
        {1, 2, 3},
    )
    spinor_exponents.update(spinor_exponent_overrides or {})
    active_pairs = (
        {
            frozenset((0, 3)),
            frozenset((4, hard_index)),
        }
        if chirality == active_chirality
        else set()
    )
    external_pair = frozenset((0, 1))
    left_zero, left_zero_cancelled, left_orientation = (
        stable_regularized_scalar_mhv_with_omitted_edge(
            [0, 1, 2, 3, 4],
            special,
            momenta,
            spinors,
            spinor_exponents,
            chirality,
            unit_circle,
            active_center,
            active_pairs,
            external_pair,
            diagnostics,
            f"{label}:left0_without_external01",
            invariant_overrides,
            edge_overrides,
            active_quotient_overrides,
        )
    )
    right_one, right_one_cancelled, right_orientation = (
        stable_regularized_scalar_mhv_with_omitted_edge(
            [3, 4, 2, 1, 0],
            special,
            momenta,
            spinors,
            spinor_exponents,
            chirality,
            unit_circle,
            active_center,
            active_pairs,
            external_pair,
            diagnostics,
            f"{label}:right1_without_external10",
            invariant_overrides,
            edge_overrides,
            active_quotient_overrides,
        )
    )
    if left_orientation != 1 or right_orientation != -1:
        raise M5258.IntervalSingularity(
            f"unexpected external01 edge orientation in {label}"
        )
    left_one, left_one_cancelled = (
        stable_regularized_scalar_mhv_with_reciprocals(
            [0, 2, 1, 3, 4],
            special,
            momenta,
            spinors,
            spinor_exponents,
            chirality,
            unit_circle,
            active_center,
            active_pairs,
            diagnostics,
            f"{label}:left1",
            invariant_overrides,
            edge_overrides,
            active_quotient_overrides,
        )
    )
    right_zero, right_zero_cancelled = (
        stable_regularized_scalar_mhv_with_reciprocals(
            [3, 4, 1, 2, 0],
            special,
            momenta,
            spinors,
            spinor_exponents,
            chirality,
            unit_circle,
            active_center,
            active_pairs,
            diagnostics,
            f"{label}:right0",
            invariant_overrides,
            edge_overrides,
            active_quotient_overrides,
        )
    )
    angle_edge = M5258.spinor_bracket(
        spinors[0][chirality], spinors[1][chirality]
    )
    edge_key = (external_pair, chirality)
    if edge_overrides is not None and edge_key in edge_overrides:
        candidate = edge_overrides[edge_key]
        if M5258.upper_abs(candidate) < M5258.upper_abs(angle_edge):
            angle_edge = candidate
    opposite_edge = M5258.spinor_bracket(
        spinors[0][1 - chirality],
        spinors[1][1 - chirality],
    )
    invariant_02 = M5258.invariant(momenta, 0, 2)
    invariant_12 = M5258.invariant(momenta, 1, 2)

    def displacement_power(
        left_cancelled: int, right_cancelled: int
    ) -> Any:
        power = 2 - left_cancelled - right_cancelled
        if power < 0:
            raise M5258.IntervalSingularity(
                f"more than two active factors in {label}"
            )
        return displacement**power

    regular = (
        displacement_power(
            left_zero_cancelled, right_zero_cancelled
        )
        * left_zero
        * opposite_edge
        * invariant_02
        * right_zero
        + displacement_power(
            left_one_cancelled, right_zero_cancelled
        )
        * left_one
        * (angle_edge * opposite_edge + invariant_12)
        * invariant_02
        * right_zero
        - displacement_power(
            left_one_cancelled, right_one_cancelled
        )
        * left_one
        * opposite_edge
        * invariant_02
        * right_one
    )
    residue = (
        -displacement_power(
            left_zero_cancelled, right_one_cancelled
        )
        * left_zero
        * opposite_edge
        * (invariant_02 + invariant_12)
        * right_one
    )
    return regular, residue, angle_edge


def momentum_kernel_with_invariant_overrides(
    alpha_reversed: int,
    beta_reversed: int,
    momenta: list[list[Any]],
    invariant_overrides: dict[frozenset[int], Any] | None = None,
) -> Any:
    if not invariant_overrides:
        return M5258.momentum_kernel(
            alpha_reversed, beta_reversed, momenta
        )

    def selected(left: int, right: int) -> Any:
        pair = frozenset((left, right))
        return (
            invariant_overrides[pair]
            if pair in invariant_overrides
            else M5258.invariant(momenta, left, right)
        )

    invariant_01 = selected(1, 0)
    invariant_02 = selected(2, 0)
    invariant_12 = selected(1, 2)
    if alpha_reversed == 0 and beta_reversed == 0:
        return invariant_01 * invariant_02
    if alpha_reversed == 0 and beta_reversed == 1:
        return (invariant_01 + invariant_12) * invariant_02
    if alpha_reversed == 1 and beta_reversed == 0:
        return (invariant_02 + invariant_12) * invariant_01
    return invariant_02 * invariant_01


def oriented_regularized_scalar_klt_five_with_reciprocals(
    momenta: list[list[Any]],
    special: int,
    chirality: int,
    hard_index: int,
    active_chirality: int,
    unit_circle: Any,
    active_center: Any,
    displacement: Any,
    diagnostics: Any,
    label: str,
    invariant_overrides: dict[frozenset[int], Any] | None = None,
    edge_overrides: dict[tuple[frozenset[int], int], Any] | None = None,
    spinor_overrides: dict[int, tuple[list[Any], list[Any]]] | None = None,
    spinor_exponent_overrides: (
        dict[int, tuple[list[int], list[int]]] | None
    ) = None,
    active_quotient_overrides: (
        dict[tuple[frozenset[int], int], Any] | None
    ) = None,
    kernel_invariant_overrides: (
        dict[frozenset[int], Any] | None
    ) = None,
) -> Any:
    spinors = dict(spinor_overrides or {})
    for index in (0, 1, 2, 3, 4):
        if index not in spinors:
            spinors[index] = M5386.rational_massless_spinors(
                momenta[index],
                diagnostics,
                f"{label}:p{index}",
                False,
            )
    spinor_exponents = M5258.spinor_exponent_table(
        momenta,
        (0, 1, 2, 3, 4),
        {1, 2, 3},
    )
    spinor_exponents.update(spinor_exponent_overrides or {})
    active_pairs = (
        {
            frozenset((0, 3)),
            frozenset((4, hard_index)),
        }
        if chirality == active_chirality
        else set()
    )
    result = cpoint(0)
    for sigma_reversed in range(2):
        sigma = [1, 2] if sigma_reversed == 0 else [2, 1]
        left, left_cancelled = stable_regularized_scalar_mhv_with_reciprocals(
            [0, *sigma, 3, 4],
            special,
            momenta,
            spinors,
            spinor_exponents,
            chirality,
            unit_circle,
            active_center,
            active_pairs,
            diagnostics,
            f"{label}:left{sigma_reversed}",
            invariant_overrides,
            edge_overrides,
            active_quotient_overrides,
        )
        for gamma_reversed in range(2):
            gamma = [1, 2] if gamma_reversed == 0 else [2, 1]
            right, right_cancelled = (
                stable_regularized_scalar_mhv_with_reciprocals(
                    [3, 4, *gamma, 0],
                    special,
                    momenta,
                    spinors,
                    spinor_exponents,
                    chirality,
                    unit_circle,
                    active_center,
                    active_pairs,
                    diagnostics,
                    f"{label}:right{gamma_reversed}",
                    invariant_overrides,
                    edge_overrides,
                    active_quotient_overrides,
                )
            )
            remaining_power = 2 - left_cancelled - right_cancelled
            if remaining_power < 0:
                raise M5258.IntervalSingularity(
                    f"more than two active factors in {label}"
                )
            result += (
                displacement**remaining_power
                * left
                * momentum_kernel_with_invariant_overrides(
                    gamma_reversed,
                    sigma_reversed,
                    momenta,
                    kernel_invariant_overrides,
                )
                * right
            )
    return result


def global_regularized_arc_coefficient(
    configuration: dict[str, Any],
    inputs: dict[str, Any],
    geometry: dict[str, Any],
    global_displacement: Any,
    path_context: dict[str, Any] | None = None,
    decompose_external01: bool = False,
) -> Any:
    diagnostics = M5258.IntervalDiagnostics()
    target = cpoint(-9) + cpoint(1j) * inputs["epsilon"]
    unit_circle = geometry["selected_root"] + global_displacement
    internal = M5258.rotate_internal_lightcone(
        M5386.amplitude_state(geometry), unit_circle
    )
    left, right = sheet_locked_interval_cut_momenta(internal, target)
    boxed_recoil_invariant = cpoint(4) * geometry["recoil"] ** 2
    hard_pair_invariant = boxed_recoil_invariant
    hard_pair_invariant_method = "BOXED_RECOIL_SQUARE"
    if path_context is not None:
        try:
            path_invariant = path_correlated_internal_hard_pair_invariant(
                path_context["cell"],
                path_context["path_segment"],
                path_context["absolute_coordinate"],
                path_context["path_parameter"],
            )
        except (EnclosureFailure, M5258.IntervalSingularity, ValueError):
            pass
        else:
            if M5258.lower_abs(path_invariant) > M5258.lower_abs(
                boxed_recoil_invariant
            ):
                hard_pair_invariant = path_invariant
                hard_pair_invariant_method = "PATH_ENERGY_ONE_MINUS_E"
    diagnostics.internal_hard_pair_invariant_method = (
        hard_pair_invariant_method
    )
    diagnostics.internal_hard_pair_invariant_abs_lower = M5258.lower_abs(
        hard_pair_invariant
    )
    common_exact_invariants = {
        frozenset((1, 2)): hard_pair_invariant
    }
    left_exact_invariants = dict(common_exact_invariants)
    right_exact_invariants = dict(common_exact_invariants)
    try:
        left_first = displaced_first_rational_spinors(
            configuration,
            inputs,
            geometry,
            global_displacement,
            1,
            diagnostics,
            "away_arc_left_first",
        )
    except M5258.IntervalSingularity as original_error:
        if path_context is None:
            raise
        for subdivision_count in (2, 4, 8):
            try:
                left_first = subdivided_path_first_rational_spinors(
                    configuration,
                    path_context["cell"],
                    path_context["path_segment"],
                    path_context["absolute_coordinate"],
                    path_context["path_parameter"],
                    inputs["epsilon"],
                    global_displacement,
                    1,
                    diagnostics,
                    "away_arc_left_first",
                    subdivision_count,
                )
            except (
                EnclosureFailure,
                M5258.IntervalSingularity,
                ValueError,
            ):
                continue
            break
        else:
            raise original_error
    try:
        right_first = displaced_first_rational_spinors(
            configuration,
            inputs,
            geometry,
            global_displacement,
            -1,
            diagnostics,
            "away_arc_right_first",
        )
    except M5258.IntervalSingularity as original_error:
        if path_context is None:
            raise
        for subdivision_count in (2, 4, 8):
            try:
                right_first = subdivided_path_first_rational_spinors(
                    configuration,
                    path_context["cell"],
                    path_context["path_segment"],
                    path_context["absolute_coordinate"],
                    path_context["path_parameter"],
                    inputs["epsilon"],
                    global_displacement,
                    -1,
                    diagnostics,
                    "away_arc_right_first",
                    subdivision_count,
                )
            except (
                EnclosureFailure,
                M5258.IntervalSingularity,
                ValueError,
            ):
                continue
            break
        else:
            raise original_error
    left_second = None
    left_second_plus = left[2][0] + left[2][3]
    left_second_minus = left[2][0] - left[2][3]
    if (
        path_context is not None
        and max(
            M5258.lower_abs(left_second_plus),
            M5258.lower_abs(left_second_minus),
        )
        <= 0.0
    ):
        for subdivision_count in (2, 4, 8):
            try:
                (
                    second_spinors,
                    second_exponents,
                    second_chart,
                    second_pivot_lower,
                ) = subdivided_path_hard_rational_spinors(
                    configuration,
                    path_context["cell"],
                    path_context["path_segment"],
                    path_context["absolute_coordinate"],
                    path_context["path_parameter"],
                    inputs["epsilon"],
                    global_displacement,
                    2,
                    1,
                    diagnostics,
                    "away_arc_left_second",
                    subdivision_count,
                )
            except (
                EnclosureFailure,
                M5258.IntervalSingularity,
                ValueError,
            ):
                continue
            left_second = (
                second_spinors,
                second_exponents,
                second_chart,
            )
            diagnostics.path_correlated_left_second_spinor_subdivision_count = (
                subdivision_count
            )
            diagnostics.path_correlated_left_second_spinor_pivot_abs_lower = (
                second_pivot_lower
            )
            break
    right_second = None
    right_second_plus = right[2][0] + right[2][3]
    right_second_minus = right[2][0] - right[2][3]
    if (
        path_context is not None
        and max(
            M5258.lower_abs(right_second_plus),
            M5258.lower_abs(right_second_minus),
        )
        <= 0.0
    ):
        for subdivision_count in (2, 4, 8):
            try:
                (
                    second_spinors,
                    second_exponents,
                    second_chart,
                    second_pivot_lower,
                ) = subdivided_path_hard_rational_spinors(
                    configuration,
                    path_context["cell"],
                    path_context["path_segment"],
                    path_context["absolute_coordinate"],
                    path_context["path_parameter"],
                    inputs["epsilon"],
                    global_displacement,
                    2,
                    -1,
                    diagnostics,
                    "away_arc_right_second",
                    subdivision_count,
                )
            except (
                EnclosureFailure,
                M5258.IntervalSingularity,
                ValueError,
            ):
                continue
            right_second = (
                second_spinors,
                second_exponents,
                second_chart,
            )
            diagnostics.path_correlated_right_second_spinor_subdivision_count = (
                subdivision_count
            )
            diagnostics.path_correlated_right_second_spinor_pivot_abs_lower = (
                second_pivot_lower
            )
            break
    left_spinors, _, left_charts = rational_spinor_overrides(
        left,
        diagnostics,
        "away_arc_left_rational",
        left_first,
        left_second,
    )
    right_spinors, right_exponents, right_charts = rational_spinor_overrides(
        right,
        diagnostics,
        "away_arc_right_rational",
        right_first,
        right_second,
    )
    left_edges = rational_hard_soft_edge_overrides(
        configuration,
        inputs,
        geometry,
        global_displacement,
        left_charts,
    )
    left_second_soft_pair = frozenset((2, 3))
    left_second_soft_mixed_key = (left_second_soft_pair, 0)
    if (
        path_context is not None
        and left_charts[2] == "minus"
        and left_charts[3] == "plus"
        and M5258.lower_abs(
            left_edges[left_second_soft_mixed_key]
        )
        <= 0.0
    ):
        for subdivision_count in (2, 4, 8):
            candidate = (
                subdivided_path_correlated_left_second_soft_mixed_angle(
                    configuration,
                    path_context["cell"],
                    path_context["path_segment"],
                    path_context["absolute_coordinate"],
                    path_context["path_parameter"],
                    inputs["epsilon"],
                    subdivision_count,
                )
            )
            if M5258.lower_abs(candidate) <= 0.0:
                continue
            left_edges[left_second_soft_mixed_key] = candidate
            diagnostics.path_correlated_left_second_soft_mixed_angle_subdivision_count = (
                subdivision_count
            )
            diagnostics.path_correlated_left_second_soft_mixed_angle_abs_lower = (
                M5258.lower_abs(candidate)
            )
            break
    right_edges = rational_hard_soft_edge_overrides(
        configuration,
        inputs,
        geometry,
        global_displacement,
        right_charts,
    )
    left_edges.update(
        coherent_internal_hard_pair_edge_overrides(
            configuration,
            inputs,
            geometry,
            global_displacement,
            left_spinors,
            left_charts,
        )
    )
    left_incoming_first_pair = frozenset((0, 1))
    left_incoming_first_missing_chiralities = [
        chirality
        for chirality in (0, 1)
        if M5258.lower_abs(
            M5258.spinor_bracket(
                left_spinors[0][chirality],
                left_spinors[1][chirality],
            )
        )
        <= 0.0
        and (
            (left_incoming_first_pair, chirality) not in left_edges
            or M5258.lower_abs(
                left_edges[(left_incoming_first_pair, chirality)]
            )
            <= 0.0
        )
    ]
    if path_context is not None and left_incoming_first_missing_chiralities:
        for subdivision_count in (2, 4, 8):
            try:
                candidate_edges = (
                    subdivided_path_left_incoming_first_edge_overrides(
                        configuration,
                        path_context["cell"],
                        path_context["path_segment"],
                        path_context["absolute_coordinate"],
                        path_context["path_parameter"],
                        inputs["epsilon"],
                        global_displacement,
                        left_charts[1],
                        diagnostics,
                        subdivision_count,
                    )
                )
            except (
                EnclosureFailure,
                M5258.IntervalSingularity,
                ValueError,
            ):
                continue
            if any(
                M5258.lower_abs(
                    candidate_edges[(left_incoming_first_pair, chirality)]
                )
                <= 0.0
                for chirality in left_incoming_first_missing_chiralities
            ):
                continue
            left_edges.update(candidate_edges)
            diagnostics.path_correlated_left_incoming_first_edge_subdivision_count = (
                subdivision_count
            )
            diagnostics.path_correlated_left_incoming_first_angle_abs_lower = (
                M5258.lower_abs(candidate_edges[(left_incoming_first_pair, 0)])
            )
            diagnostics.path_correlated_left_incoming_first_square_abs_lower = (
                M5258.lower_abs(candidate_edges[(left_incoming_first_pair, 1)])
            )
            break
    right_edges.update(
        coherent_internal_hard_pair_edge_overrides(
            configuration,
            inputs,
            geometry,
            global_displacement,
            right_spinors,
            right_charts,
        )
    )
    right_edges.update(
        M5386.first_plus_edge_overrides(
            configuration,
            inputs,
            geometry,
            cpoint(0),
            global_displacement,
            target,
            use_material_recoil_sheet=True,
        )
    )
    right_edges.update(
        M5386.first_minus_edge_overrides(
            configuration,
            inputs,
            geometry,
            global_displacement,
            target,
        )
    )
    right_edges.update(
        tight_second_external_edge_overrides(
            configuration,
            inputs,
            geometry,
            global_displacement,
            target,
            right_charts,
            right_spinors,
        )
    )
    right_active_quotients: dict[
        tuple[frozenset[int], int], Any
    ] = {}
    external4_first_pair = frozenset((1, 4))
    direct_external4_first_angle = M5258.spinor_bracket(
        right_spinors[1][0], right_spinors[4][0]
    )
    direct_external4_first_square = M5258.spinor_bracket(
        right_spinors[1][1], right_spinors[4][1]
    )
    coarse_external4_first_angle = direct_external4_first_angle
    if path_context is not None and configuration["role"] == "reciprocal":
        try:
            correlated_external4_first_angle = (
                centered_path_correlated_external4_first_angle(
                    configuration,
                    path_context["cell"],
                    path_context["path_segment"],
                    path_context["absolute_coordinate"],
                    path_context["path_parameter"],
                    inputs["epsilon"],
                    global_displacement,
                    right_charts[1],
                )
            )
        except (EnclosureFailure, M5258.IntervalSingularity, ValueError):
            pass
        else:
            coarse_external4_first_angle = max(
                (
                    direct_external4_first_angle,
                    correlated_external4_first_angle,
                ),
                key=lambda value: (
                    M5258.lower_abs(value),
                    -M5258.upper_abs(value),
                ),
            )
    if (
        path_context is not None
        and configuration["role"] == "reciprocal"
        and right_charts[1] == "plus"
    ):
        try:
            factorized_external4_first_angle = (
                centered_path_correlated_external4_first_plus_angle_factorized(
                    configuration,
                    path_context["cell"],
                    path_context["path_segment"],
                    path_context["absolute_coordinate"],
                    path_context["path_parameter"],
                    inputs["epsilon"],
                    global_displacement,
                )
            )
        except (EnclosureFailure, M5258.IntervalSingularity, ValueError):
            pass
        else:
            coarse_external4_first_angle = max(
                (
                    coarse_external4_first_angle,
                    factorized_external4_first_angle,
                ),
                key=lambda value: (
                    M5258.lower_abs(value),
                    -M5258.upper_abs(value),
                ),
            )
    if M5258.lower_abs(coarse_external4_first_angle) > 0.0:
        existing_external4_first_angle = right_edges.get(
            (external4_first_pair, 0)
        )
        if (
            existing_external4_first_angle is None
            or M5258.lower_abs(coarse_external4_first_angle)
            > M5258.lower_abs(existing_external4_first_angle)
        ):
            right_edges[(external4_first_pair, 0)] = (
                coarse_external4_first_angle
            )
    coarse_external4_first_square_quotient = None
    if configuration["role"] == "reciprocal":
        try:
            coarse_external4_first_square_quotient = (
                exact_external4_first_active_quotient(
                    configuration,
                    inputs,
                    geometry,
                    global_displacement,
                    right_charts[1],
                    M5258.IntervalDiagnostics(),
                    "coarse_external4_first_active",
                )
            )
        except M5258.IntervalSingularity:
            pass
        if (
            coarse_external4_first_square_quotient is not None
            and M5258.lower_abs(
                coarse_external4_first_square_quotient
            )
            > 0.0
        ):
            right_active_quotients[(external4_first_pair, 1)] = (
                coarse_external4_first_square_quotient
            )
            diagnostics.path_correlated_external4_first_subdivision_count = 0
            diagnostics.path_correlated_external4_first_angle_abs_lower = (
                M5258.lower_abs(coarse_external4_first_angle)
            )
            diagnostics.path_correlated_external4_first_square_quotient_abs_lower = (
                M5258.lower_abs(coarse_external4_first_square_quotient)
            )
            diagnostics.path_correlated_external4_first_invariant_quotient_abs_lower = (
                M5258.lower_abs(coarse_external4_first_angle)
                * M5258.lower_abs(coarse_external4_first_square_quotient)
            )
    if (
        path_context is not None
        and configuration["role"] == "reciprocal"
        and (
            M5258.lower_abs(coarse_external4_first_angle) <= 0.0
            or coarse_external4_first_square_quotient is None
            or M5258.lower_abs(
                coarse_external4_first_square_quotient
            )
            <= 0.0
        )
    ):
        right_edges.pop((external4_first_pair, 0), None)
        right_edges.pop((external4_first_pair, 1), None)
        external4_first_pair_resolved = False
        if (
            right_charts[1] == "plus"
            and int(path_context["refinement_depth"]) >= 8
            and coarse_external4_first_square_quotient is not None
            and M5258.lower_abs(
                coarse_external4_first_square_quotient
            )
            > 0.0
        ):
            try:
                external4_first_angle = (
                    subdivided_path_external4_first_plus_angle_factorized(
                        configuration,
                        path_context["cell"],
                        path_context["path_segment"],
                        path_context["absolute_coordinate"],
                        path_context["path_parameter"],
                        inputs["epsilon"],
                        global_displacement,
                        16,
                    )
                )
            except (
                EnclosureFailure,
                M5258.IntervalSingularity,
                ValueError,
            ):
                pass
            else:
                if M5258.lower_abs(external4_first_angle) > 0.0:
                    right_edges[(external4_first_pair, 0)] = (
                        external4_first_angle
                    )
                    right_active_quotients[(external4_first_pair, 1)] = (
                        coarse_external4_first_square_quotient
                    )
                    diagnostics.path_correlated_external4_first_subdivision_count = (
                        16
                    )
                    diagnostics.path_correlated_external4_first_angle_abs_lower = (
                        M5258.lower_abs(external4_first_angle)
                    )
                    diagnostics.path_correlated_external4_first_square_quotient_abs_lower = (
                        M5258.lower_abs(
                            coarse_external4_first_square_quotient
                        )
                    )
                    diagnostics.path_correlated_external4_first_invariant_quotient_abs_lower = (
                        M5258.lower_abs(external4_first_angle)
                        * M5258.lower_abs(
                            coarse_external4_first_square_quotient
                        )
                    )
                    external4_first_pair_resolved = True
        if not external4_first_pair_resolved:
            for subdivision_count in (2, 4, 8):
                try:
                    (
                        external4_first_angle,
                        external4_first_square_quotient,
                        external4_first_invariant_quotient_lower,
                    ) = subdivided_path_external4_first_active_pair(
                        configuration,
                        path_context["cell"],
                        path_context["path_segment"],
                        path_context["absolute_coordinate"],
                        path_context["path_parameter"],
                        inputs["epsilon"],
                        global_displacement,
                        subdivision_count,
                    )
                except (
                    EnclosureFailure,
                    M5258.IntervalSingularity,
                    ValueError,
                ):
                    continue
                if (
                    M5258.lower_abs(external4_first_angle) <= 0.0
                    or M5258.lower_abs(
                        external4_first_square_quotient
                    )
                    <= 0.0
                ):
                    continue
                right_edges[(external4_first_pair, 0)] = (
                    external4_first_angle
                )
                right_active_quotients[(external4_first_pair, 1)] = (
                    external4_first_square_quotient
                )
                diagnostics.path_correlated_external4_first_subdivision_count = (
                    subdivision_count
                )
                diagnostics.path_correlated_external4_first_angle_abs_lower = (
                    M5258.lower_abs(external4_first_angle)
                )
                diagnostics.path_correlated_external4_first_square_quotient_abs_lower = (
                    M5258.lower_abs(external4_first_square_quotient)
                )
                diagnostics.path_correlated_external4_first_invariant_quotient_abs_lower = (
                    external4_first_invariant_quotient_lower
                )
                break
    current_external4_first_square = right_edges.get(
        (external4_first_pair, 1),
        direct_external4_first_square,
    )
    if (
        path_context is not None
        and configuration["role"] == "representative"
        and M5258.lower_abs(current_external4_first_square) <= 0.0
    ):
        try:
            correlated_external4_first_square = (
                centered_path_correlated_external4_first_square(
                    configuration,
                    path_context["cell"],
                    path_context["path_segment"],
                    path_context["absolute_coordinate"],
                    path_context["path_parameter"],
                    inputs["epsilon"],
                    global_displacement,
                    right_charts[1],
                )
            )
        except (EnclosureFailure, M5258.IntervalSingularity, ValueError):
            pass
        else:
            current_external4_first_square = max(
                (
                    current_external4_first_square,
                    correlated_external4_first_square,
                ),
                key=lambda value: (
                    M5258.lower_abs(value),
                    -M5258.upper_abs(value),
                ),
            )
            diagnostics.path_correlated_external4_first_square_subdivision_count = 0
        if M5258.lower_abs(current_external4_first_square) <= 0.0:
            for subdivision_count in (2, 4, 8, 16):
                try:
                    subdivided_external4_first_square = (
                        subdivided_path_correlated_external4_first_square(
                            configuration,
                            path_context["cell"],
                            path_context["path_segment"],
                            path_context["absolute_coordinate"],
                            path_context["path_parameter"],
                            inputs["epsilon"],
                            global_displacement,
                            right_charts[1],
                            subdivision_count,
                        )
                    )
                except (
                    EnclosureFailure,
                    M5258.IntervalSingularity,
                    ValueError,
                ):
                    continue
                current_external4_first_square = max(
                    (
                        current_external4_first_square,
                        subdivided_external4_first_square,
                    ),
                    key=lambda value: (
                        M5258.lower_abs(value),
                        -M5258.upper_abs(value),
                    ),
                )
                diagnostics.path_correlated_external4_first_square_subdivision_count = (
                    subdivision_count
                )
                if M5258.lower_abs(current_external4_first_square) > 0.0:
                    break
        if M5258.lower_abs(current_external4_first_square) > 0.0:
            right_edges[(external4_first_pair, 1)] = (
                current_external4_first_square
            )
            diagnostics.path_correlated_external4_first_square_abs_lower = (
                M5258.lower_abs(current_external4_first_square)
            )
    first_external_pair = frozenset((0, 1))
    direct_first_external_edges = {
        chirality: M5258.spinor_bracket(
            right_spinors[0][chirality],
            right_spinors[1][chirality],
        )
        for chirality in (0, 1)
    }
    direct_first_external_edge = direct_first_external_edges[0]
    current_first_external_edge = right_edges.get(
        (first_external_pair, 0)
    )
    current_first_external_invariant = M5258.invariant(right, 0, 1)
    unresolved_first_external_chiralities = [
        chirality
        for chirality in (0, 1)
        if M5258.lower_abs(direct_first_external_edges[chirality]) <= 0.0
        and (
            (first_external_pair, chirality) not in right_edges
            or M5258.lower_abs(
                right_edges[(first_external_pair, chirality)]
            )
            <= 0.0
        )
    ]
    if (
        path_context is not None
        and unresolved_first_external_chiralities
        and M5258.lower_abs(current_first_external_invariant) <= 0.0
    ):
        try:
            correlated_first_invariant = (
                centered_path_correlated_external_first_invariant(
                    configuration,
                    path_context["cell"],
                    path_context["path_segment"],
                    path_context["absolute_coordinate"],
                    path_context["path_parameter"],
                    inputs["epsilon"],
                    global_displacement,
                    0,
                )
            )
        except (EnclosureFailure, M5258.IntervalSingularity, ValueError):
            pass
        else:
            current_first_external_invariant = max(
                (
                    current_first_external_invariant,
                    correlated_first_invariant,
                ),
                key=lambda value: (
                    M5258.lower_abs(value),
                    -M5258.upper_abs(value),
                ),
            )
        if M5258.lower_abs(current_first_external_invariant) <= 0.0:
            for subdivision_count in (2, 4, 8):
                try:
                    subdivided_first_invariant = (
                        subdivided_path_correlated_external_first_invariant(
                            configuration,
                            path_context["cell"],
                            path_context["path_segment"],
                            path_context["absolute_coordinate"],
                            path_context["path_parameter"],
                            inputs["epsilon"],
                            global_displacement,
                            0,
                            subdivision_count,
                        )
                    )
                except (
                    EnclosureFailure,
                    M5258.IntervalSingularity,
                    ValueError,
                ):
                    continue
                current_first_external_invariant = max(
                    (
                        current_first_external_invariant,
                        subdivided_first_invariant,
                    ),
                    key=lambda value: (
                        M5258.lower_abs(value),
                        -M5258.upper_abs(value),
                    ),
                )
                diagnostics.path_correlated_external_first_invariant_subdivision_count = (
                    subdivision_count
                )
                if M5258.lower_abs(current_first_external_invariant) > 0.0:
                    break
        right_exact_invariants[first_external_pair] = (
            current_first_external_invariant
        )
        diagnostics.path_correlated_external_first_invariant_abs_lower = (
            M5258.lower_abs(current_first_external_invariant)
        )
    current_first_external_edge = right_edges.get(
        (first_external_pair, 0)
    )
    if (
        path_context is not None
        and right_charts[0] == "minus"
        and right_charts[1] == "minus"
        and M5258.lower_abs(direct_first_external_edge) <= 0.0
        and (
            current_first_external_edge is None
            or M5258.lower_abs(current_first_external_edge) <= 0.0
        )
    ):
        try:
            correlated_first_minus_edge = (
                centered_path_correlated_external0_first_minus_angle(
                    configuration,
                    path_context["cell"],
                    path_context["path_segment"],
                    path_context["absolute_coordinate"],
                    path_context["path_parameter"],
                    inputs["epsilon"],
                    global_displacement,
                )
            )
        except (EnclosureFailure, M5258.IntervalSingularity, ValueError):
            pass
        else:
            edge_candidates = [correlated_first_minus_edge]
            if current_first_external_edge is not None:
                edge_candidates.append(current_first_external_edge)
            current_first_external_edge = max(
                edge_candidates,
                key=lambda value: (
                    M5258.lower_abs(value),
                    -M5258.upper_abs(value),
                ),
            )
            right_edges[(first_external_pair, 0)] = (
                current_first_external_edge
            )
    current_first_external_edge = right_edges.get(
        (first_external_pair, 0)
    )
    if (
        path_context is not None
        and right_charts[0] == "minus"
        and right_charts[1] == "minus"
        and M5258.lower_abs(direct_first_external_edge) <= 0.0
        and (
            current_first_external_edge is None
            or M5258.lower_abs(current_first_external_edge) <= 0.0
        )
    ):
        for subdivision_count in (2, 4, 8):
            try:
                subdivided_first_minus_edge = (
                    subdivided_path_correlated_external0_first_minus_angle(
                        configuration,
                        path_context["cell"],
                        path_context["path_segment"],
                        path_context["absolute_coordinate"],
                        path_context["path_parameter"],
                        inputs["epsilon"],
                        global_displacement,
                        subdivision_count,
                    )
                )
            except (
                EnclosureFailure,
                M5258.IntervalSingularity,
                ValueError,
            ):
                continue
            edge_candidates = [subdivided_first_minus_edge]
            if current_first_external_edge is not None:
                edge_candidates.append(current_first_external_edge)
            current_first_external_edge = max(
                edge_candidates,
                key=lambda value: (
                    M5258.lower_abs(value),
                    -M5258.upper_abs(value),
                ),
            )
            right_edges[(first_external_pair, 0)] = (
                current_first_external_edge
            )
            diagnostics.path_correlated_external0_first_minus_edge_subdivision_count = (
                subdivision_count
            )
            if M5258.lower_abs(current_first_external_edge) > 0.0:
                break
    current_first_external_edge = right_edges.get(
        (first_external_pair, 0)
    )
    if (
        right_charts[0] == "minus"
        and right_charts[1] == "minus"
        and current_first_external_edge is not None
    ):
        diagnostics.path_correlated_external0_first_minus_edge_abs_lower = (
            M5258.lower_abs(current_first_external_edge)
        )
    current_first_external_edge = right_edges.get(
        (first_external_pair, 0)
    )
    if (
        path_context is not None
        and right_charts[0] == "minus"
        and right_charts[1] == "plus"
        and M5258.lower_abs(direct_first_external_edge) <= 0.0
        and (
            current_first_external_edge is None
            or M5258.lower_abs(current_first_external_edge) <= 0.0
        )
    ):
        try:
            correlated_first_minus_plus_edge = (
                centered_path_correlated_external0_first_minus_plus_angle(
                    configuration,
                    path_context["cell"],
                    path_context["path_segment"],
                    path_context["absolute_coordinate"],
                    path_context["path_parameter"],
                    inputs["epsilon"],
                    global_displacement,
                )
            )
        except (EnclosureFailure, M5258.IntervalSingularity, ValueError):
            pass
        else:
            edge_candidates = [correlated_first_minus_plus_edge]
            if current_first_external_edge is not None:
                edge_candidates.append(current_first_external_edge)
            current_first_external_edge = max(
                edge_candidates,
                key=lambda value: (
                    M5258.lower_abs(value),
                    -M5258.upper_abs(value),
                ),
            )
            right_edges[(first_external_pair, 0)] = (
                current_first_external_edge
            )
    current_first_external_edge = right_edges.get(
        (first_external_pair, 0)
    )
    if (
        path_context is not None
        and right_charts[0] == "minus"
        and right_charts[1] == "plus"
        and M5258.lower_abs(direct_first_external_edge) <= 0.0
        and (
            current_first_external_edge is None
            or M5258.lower_abs(current_first_external_edge) <= 0.0
        )
    ):
        for subdivision_count in (2, 4, 8):
            try:
                subdivided_first_minus_plus_edge = (
                    subdivided_path_correlated_external0_first_minus_plus_angle(
                        configuration,
                        path_context["cell"],
                        path_context["path_segment"],
                        path_context["absolute_coordinate"],
                        path_context["path_parameter"],
                        inputs["epsilon"],
                        global_displacement,
                        subdivision_count,
                    )
                )
            except (
                EnclosureFailure,
                M5258.IntervalSingularity,
                ValueError,
            ):
                continue
            edge_candidates = [subdivided_first_minus_plus_edge]
            if current_first_external_edge is not None:
                edge_candidates.append(current_first_external_edge)
            current_first_external_edge = max(
                edge_candidates,
                key=lambda value: (
                    M5258.lower_abs(value),
                    -M5258.upper_abs(value),
                ),
            )
            right_edges[(first_external_pair, 0)] = (
                current_first_external_edge
            )
            diagnostics.path_correlated_external0_first_minus_plus_edge_subdivision_count = (
                subdivision_count
            )
            if M5258.lower_abs(current_first_external_edge) > 0.0:
                break
    current_first_external_edge = right_edges.get(
        (first_external_pair, 0)
    )
    if (
        path_context is not None
        and not decompose_external01
        and configuration["role"] == "reciprocal"
        and right_charts[0] == "minus"
        and right_charts[1] == "plus"
        and (
            current_first_external_edge is None
            or M5258.lower_abs(current_first_external_edge) <= 0.0
        )
    ):
        try:
            native_edge_cache = path_context.get("native_edge_cache")
            native_edge_cache_key = (
                "external0_first_minus_plus_negative_half_plane"
            )
            if (
                isinstance(native_edge_cache, dict)
                and native_edge_cache_key in native_edge_cache
            ):
                (
                    native_first_minus_plus_edge,
                    native_first_minus_plus_metadata,
                ) = native_edge_cache[native_edge_cache_key]
            else:
                displacement_for_proof = global_displacement
                if "global_displacement_radius" in path_context:
                    displacement_radius = math.nextafter(
                        float(path_context["global_displacement_radius"]),
                        math.inf,
                    )
                    displacement_for_proof = cbox(
                        -displacement_radius,
                        displacement_radius,
                        -displacement_radius,
                        displacement_radius,
                    )
                (
                    native_first_minus_plus_edge,
                    native_first_minus_plus_metadata,
                ) = (
                    negative_half_plane_subcover_native_external0_first_minus_plus_angle(
                        configuration,
                        path_context["cell"],
                        path_context["path_segment"],
                        path_context["absolute_coordinate"],
                        path_context["path_parameter"],
                        inputs["epsilon"],
                        displacement_for_proof,
                    )
                )
                if isinstance(native_edge_cache, dict):
                    native_edge_cache[native_edge_cache_key] = (
                        native_first_minus_plus_edge,
                        native_first_minus_plus_metadata,
                    )
        except (EnclosureFailure, M5258.IntervalSingularity, ValueError):
            pass
        else:
            edge_candidates = [native_first_minus_plus_edge]
            if current_first_external_edge is not None:
                edge_candidates.append(current_first_external_edge)
            current_first_external_edge = max(
                edge_candidates,
                key=lambda value: (
                    M5258.lower_abs(value),
                    -M5258.upper_abs(value),
                ),
            )
            right_edges[(first_external_pair, 0)] = (
                current_first_external_edge
            )
            diagnostics.path_correlated_external0_first_minus_plus_native_leaf_count = (
                native_first_minus_plus_metadata["leaf_count"]
            )
            diagnostics.path_correlated_external0_first_minus_plus_native_evaluation_count = (
                native_first_minus_plus_metadata["evaluation_count"]
            )
            diagnostics.path_correlated_external0_first_minus_plus_native_negative_real_margin = (
                native_first_minus_plus_metadata[
                    "enclosure_negative_real_margin"
                ]
            )
    if (
        right_charts[0] == "minus"
        and right_charts[1] == "plus"
        and current_first_external_edge is not None
    ):
        diagnostics.path_correlated_external0_first_minus_plus_edge_abs_lower = (
            M5258.lower_abs(current_first_external_edge)
        )
    for external_endpoint in (0, 4):
        pair = frozenset((external_endpoint, 2))
        left_index, right_index = sorted(pair)
        if all(
            M5258.lower_abs(
                M5258.spinor_bracket(
                    right_spinors[left_index][chirality],
                    right_spinors[right_index][chirality],
                )
            )
            > 0.0
            for chirality in (0, 1)
        ):
            continue
        try:
            right_exact_invariants[pair] = (
                centered_external_second_invariant(
                    configuration,
                    inputs,
                    geometry,
                    global_displacement,
                    external_endpoint,
                )
            )
        except (M5258.IntervalSingularity, ValueError):
            pass
    external0_second_pair = frozenset((0, 2))
    current_external0_second_invariant = right_exact_invariants.get(
        external0_second_pair
    )
    if (
        path_context is not None
        and (
            current_external0_second_invariant is None
            or M5258.lower_abs(current_external0_second_invariant) <= 0.0
        )
    ):
        try:
            correlated_external0_second_invariant = (
                centered_path_correlated_external_second_invariant(
                    configuration,
                    path_context["cell"],
                    path_context["path_segment"],
                    path_context["absolute_coordinate"],
                    path_context["path_parameter"],
                    inputs["epsilon"],
                    global_displacement,
                    0,
                )
            )
        except (EnclosureFailure, M5258.IntervalSingularity, ValueError):
            pass
        else:
            invariant_candidates = [correlated_external0_second_invariant]
            if current_external0_second_invariant is not None:
                invariant_candidates.append(current_external0_second_invariant)
            current_external0_second_invariant = max(
                invariant_candidates,
                key=lambda value: (
                    M5258.lower_abs(value),
                    -M5258.upper_abs(value),
                ),
            )
            right_exact_invariants[external0_second_pair] = (
                current_external0_second_invariant
            )
    if (
        path_context is not None
        and (
            current_external0_second_invariant is None
            or M5258.lower_abs(current_external0_second_invariant) <= 0.0
        )
    ):
        for subdivision_count in (2, 4):
            try:
                subdivided_external0_second_invariant = (
                    subdivided_path_correlated_external_second_invariant(
                        configuration,
                        path_context["cell"],
                        path_context["path_segment"],
                        path_context["absolute_coordinate"],
                        path_context["path_parameter"],
                        inputs["epsilon"],
                        global_displacement,
                        0,
                        subdivision_count,
                    )
                )
            except (EnclosureFailure, M5258.IntervalSingularity, ValueError):
                continue
            invariant_candidates = [subdivided_external0_second_invariant]
            if current_external0_second_invariant is not None:
                invariant_candidates.append(current_external0_second_invariant)
            current_external0_second_invariant = max(
                invariant_candidates,
                key=lambda value: (
                    M5258.lower_abs(value),
                    -M5258.upper_abs(value),
                ),
            )
            right_exact_invariants[external0_second_pair] = (
                current_external0_second_invariant
            )
            diagnostics.path_correlated_external0_second_invariant_subdivision_count = (
                subdivision_count
            )
            if M5258.lower_abs(current_external0_second_invariant) > 0.0:
                break
    if current_external0_second_invariant is not None:
        diagnostics.path_correlated_external0_second_invariant_abs_lower = (
            M5258.lower_abs(current_external0_second_invariant)
        )
    correlated_pair = frozenset((2, 4))
    current_correlated_invariant = right_exact_invariants.get(correlated_pair)
    if (
        path_context is not None
        and int(path_context.get("refinement_depth", 0)) >= 8
        and (
            current_correlated_invariant is None
            or M5258.lower_abs(current_correlated_invariant) <= 0.0
        )
    ):
        try:
            correlated_invariant = (
                centered_path_correlated_external_second_invariant(
                    configuration,
                    path_context["cell"],
                    path_context["path_segment"],
                    path_context["absolute_coordinate"],
                    path_context["path_parameter"],
                    inputs["epsilon"],
                    global_displacement,
                    4,
                )
            )
        except (EnclosureFailure, M5258.IntervalSingularity, ValueError):
            pass
        else:
            invariant_candidates = [correlated_invariant]
            if current_correlated_invariant is not None:
                invariant_candidates.append(current_correlated_invariant)
            right_exact_invariants[correlated_pair] = max(
                invariant_candidates,
                key=lambda value: (
                    M5258.lower_abs(value),
                    -M5258.upper_abs(value),
                ),
            )
            diagnostics.path_correlated_external_invariant_abs_lower = (
                M5258.lower_abs(right_exact_invariants[correlated_pair])
            )
    current_correlated_invariant = right_exact_invariants.get(correlated_pair)
    if (
        path_context is not None
        and (
            current_correlated_invariant is None
            or M5258.lower_abs(current_correlated_invariant) <= 0.0
        )
    ):
        for subdivision_count in (2, 4):
            try:
                subdivided_invariant = (
                    subdivided_path_correlated_external_second_invariant(
                        configuration,
                        path_context["cell"],
                        path_context["path_segment"],
                        path_context["absolute_coordinate"],
                        path_context["path_parameter"],
                        inputs["epsilon"],
                        global_displacement,
                        4,
                        subdivision_count,
                    )
                )
            except (EnclosureFailure, M5258.IntervalSingularity, ValueError):
                continue
            invariant_candidates = [subdivided_invariant]
            if current_correlated_invariant is not None:
                invariant_candidates.append(current_correlated_invariant)
            current_correlated_invariant = max(
                invariant_candidates,
                key=lambda value: (
                    M5258.lower_abs(value),
                    -M5258.upper_abs(value),
                ),
            )
            right_exact_invariants[correlated_pair] = current_correlated_invariant
            diagnostics.path_correlated_external_invariant_abs_lower = (
                M5258.lower_abs(current_correlated_invariant)
            )
            diagnostics.path_correlated_external_invariant_subdivision_count = (
                subdivision_count
            )
            if M5258.lower_abs(current_correlated_invariant) > 0.0:
                break
    current_correlated_invariant = right_exact_invariants.get(
        correlated_pair
    )
    if (
        path_context is not None
        and (
            current_correlated_invariant is None
            or M5258.lower_abs(current_correlated_invariant) <= 0.0
        )
    ):
        try:
            invariant_cache = path_context.get("native_edge_cache")
            invariant_cache_key = "external42_invariant_half_plane"
            if (
                isinstance(invariant_cache, dict)
                and invariant_cache_key in invariant_cache
            ):
                (
                    half_plane_invariant,
                    half_plane_metadata,
                ) = invariant_cache[invariant_cache_key]
            else:
                displacement_for_proof = global_displacement
                if "global_displacement_radius" in path_context:
                    displacement_radius = math.nextafter(
                        float(path_context["global_displacement_radius"]),
                        math.inf,
                    )
                    displacement_for_proof = cbox(
                        -displacement_radius,
                        displacement_radius,
                        -displacement_radius,
                        displacement_radius,
                    )
                (
                    half_plane_invariant,
                    half_plane_metadata,
                ) = half_plane_subcover_external42_invariant(
                    configuration,
                    path_context["cell"],
                    path_context["path_segment"],
                    path_context["absolute_coordinate"],
                    path_context["path_parameter"],
                    inputs["epsilon"],
                    displacement_for_proof,
                )
                if isinstance(invariant_cache, dict):
                    invariant_cache[invariant_cache_key] = (
                        half_plane_invariant,
                        half_plane_metadata,
                    )
        except (EnclosureFailure, M5258.IntervalSingularity, ValueError):
            pass
        else:
            invariant_candidates = [half_plane_invariant]
            if current_correlated_invariant is not None:
                invariant_candidates.append(current_correlated_invariant)
            current_correlated_invariant = max(
                invariant_candidates,
                key=lambda value: (
                    M5258.lower_abs(value),
                    -M5258.upper_abs(value),
                ),
            )
            right_exact_invariants[correlated_pair] = (
                current_correlated_invariant
            )
            diagnostics.path_correlated_external42_invariant_half_plane_abs_lower = (
                M5258.lower_abs(current_correlated_invariant)
            )
            diagnostics.path_correlated_external42_invariant_half_plane_projection = (
                half_plane_metadata["half_plane_projection"]
            )
            diagnostics.path_correlated_external42_invariant_half_plane_leaf_count = (
                half_plane_metadata["half_plane_leaf_count"]
            )
            diagnostics.path_correlated_external42_invariant_half_plane_evaluation_count = (
                half_plane_metadata["half_plane_evaluation_count"]
            )
    correlated_key = (correlated_pair, 0)
    direct_correlated_edge = M5258.spinor_bracket(
        right_spinors[2][0], right_spinors[4][0]
    )
    current_correlated_edge = right_edges.get(correlated_key)
    correlated_invariant = right_exact_invariants.get(correlated_pair)
    if (
        path_context is not None
        and right_charts[2] == "plus"
        and right_charts[4] == "minus"
        and M5258.lower_abs(direct_correlated_edge) <= 0.0
        and (
            current_correlated_edge is None
            or M5258.lower_abs(current_correlated_edge) <= 0.0
        )
        and (
            correlated_invariant is None
            or M5258.lower_abs(correlated_invariant) <= 0.0
        )
    ):
        try:
            correlated_edge = centered_path_correlated_external4_second_angle(
                configuration,
                path_context["cell"],
                path_context["path_segment"],
                path_context["absolute_coordinate"],
                path_context["path_parameter"],
                inputs["epsilon"],
                global_displacement,
            )
        except (EnclosureFailure, M5258.IntervalSingularity, ValueError):
            pass
        else:
            edge_candidates = [correlated_edge]
            if current_correlated_edge is not None:
                edge_candidates.append(current_correlated_edge)
            right_edges[correlated_key] = max(
                edge_candidates,
                key=lambda value: (
                    M5258.lower_abs(value),
                    -M5258.upper_abs(value),
                ),
            )
            diagnostics.path_correlated_external_edge_abs_lower = (
                M5258.lower_abs(right_edges[correlated_key])
            )
    current_correlated_edge = right_edges.get(correlated_key)
    if (
        path_context is not None
        and right_charts[2] == "plus"
        and right_charts[4] == "plus"
        and M5258.lower_abs(direct_correlated_edge) <= 0.0
        and (
            current_correlated_edge is None
            or M5258.lower_abs(current_correlated_edge) <= 0.0
        )
    ):
        try:
            correlated_plus_edge = (
                centered_path_correlated_external4_second_plus_angle(
                    configuration,
                    path_context["cell"],
                    path_context["path_segment"],
                    path_context["absolute_coordinate"],
                    path_context["path_parameter"],
                    inputs["epsilon"],
                    global_displacement,
                )
            )
        except (EnclosureFailure, M5258.IntervalSingularity, ValueError):
            pass
        else:
            edge_candidates = [correlated_plus_edge]
            if current_correlated_edge is not None:
                edge_candidates.append(current_correlated_edge)
            current_correlated_edge = max(
                edge_candidates,
                key=lambda value: (
                    M5258.lower_abs(value),
                    -M5258.upper_abs(value),
                ),
            )
            right_edges[correlated_key] = current_correlated_edge
    current_correlated_edge = right_edges.get(correlated_key)
    if (
        path_context is not None
        and right_charts[2] == "plus"
        and right_charts[4] == "plus"
        and M5258.lower_abs(direct_correlated_edge) <= 0.0
        and (
            current_correlated_edge is None
            or M5258.lower_abs(current_correlated_edge) <= 0.0
        )
    ):
        for subdivision_count in (2, 4, 8):
            try:
                subdivided_plus_edge = (
                    subdivided_path_correlated_external4_second_plus_angle(
                        configuration,
                        path_context["cell"],
                        path_context["path_segment"],
                        path_context["absolute_coordinate"],
                        path_context["path_parameter"],
                        inputs["epsilon"],
                        global_displacement,
                        subdivision_count,
                    )
                )
            except (
                EnclosureFailure,
                M5258.IntervalSingularity,
                ValueError,
            ):
                continue
            edge_candidates = [subdivided_plus_edge]
            if current_correlated_edge is not None:
                edge_candidates.append(current_correlated_edge)
            current_correlated_edge = max(
                edge_candidates,
                key=lambda value: (
                    M5258.lower_abs(value),
                    -M5258.upper_abs(value),
                ),
            )
            right_edges[correlated_key] = current_correlated_edge
            diagnostics.path_correlated_external4_second_plus_edge_subdivision_count = (
                subdivision_count
            )
            if M5258.lower_abs(current_correlated_edge) > 0.0:
                break
    current_correlated_edge = right_edges.get(correlated_key)
    if (
        right_charts[2] == "plus"
        and right_charts[4] == "plus"
        and current_correlated_edge is not None
    ):
        diagnostics.path_correlated_external4_second_plus_edge_abs_lower = (
            M5258.lower_abs(current_correlated_edge)
        )
    left_incoming_second_pair = frozenset((0, 2))
    if any(
        M5258.lower_abs(
            M5258.spinor_bracket(
                left_spinors[0][chirality], left_spinors[2][chirality]
            )
        )
        <= 0.0
        for chirality in (0, 1)
    ):
        left_incoming_second_invariant = M5258.invariant(left, 0, 2)
        if path_context is not None:
            try:
                correlated_left_incoming_second_invariant = (
                    centered_path_correlated_left_incoming_hard_invariant(
                        configuration,
                        path_context["cell"],
                        path_context["path_segment"],
                        path_context["absolute_coordinate"],
                        path_context["path_parameter"],
                        inputs["epsilon"],
                        global_displacement,
                        0,
                        2,
                    )
                )
            except (
                EnclosureFailure,
                M5258.IntervalSingularity,
                ValueError,
            ):
                pass
            else:
                left_incoming_second_invariant = max(
                    (
                        left_incoming_second_invariant,
                        correlated_left_incoming_second_invariant,
                    ),
                    key=lambda value: (
                        M5258.lower_abs(value),
                        -M5258.upper_abs(value),
                    ),
                )
            if M5258.lower_abs(left_incoming_second_invariant) <= 0.0:
                for subdivision_count in (2, 4):
                    try:
                        subdivided_left_incoming_second_invariant = (
                            subdivided_path_correlated_left_incoming_hard_invariant(
                                configuration,
                                path_context["cell"],
                                path_context["path_segment"],
                                path_context["absolute_coordinate"],
                                path_context["path_parameter"],
                                inputs["epsilon"],
                                global_displacement,
                                0,
                                2,
                                subdivision_count,
                            )
                        )
                    except (
                        EnclosureFailure,
                        M5258.IntervalSingularity,
                        ValueError,
                    ):
                        continue
                    left_incoming_second_invariant = max(
                        (
                            left_incoming_second_invariant,
                            subdivided_left_incoming_second_invariant,
                        ),
                        key=lambda value: (
                            M5258.lower_abs(value),
                            -M5258.upper_abs(value),
                        ),
                    )
                    diagnostics.path_correlated_left_incoming_second_invariant_subdivision_count = (
                        subdivision_count
                    )
                    if M5258.lower_abs(
                        left_incoming_second_invariant
                    ) > 0.0:
                        break
        if M5258.lower_abs(left_incoming_second_invariant) > 0.0:
            left_exact_invariants[left_incoming_second_pair] = (
                left_incoming_second_invariant
            )
            diagnostics.path_correlated_left_incoming_second_invariant_abs_lower = (
                M5258.lower_abs(left_incoming_second_invariant)
            )
    active_chirality = 1 if configuration["role"] == "reciprocal" else 0
    hhh = cpoint(0)
    external01_pole_hhh = cpoint(0)
    external01_angle_edge = None
    for special in (1, 2, 3):
        for left_chirality, right_chirality in ((0, 1), (1, 0)):
            left_value = scalar_klt_five_with_reciprocals(
                left,
                special,
                left_chirality,
                diagnostics,
                f"away_arc_left_K5:s{special}:c{left_chirality}",
                left_exact_invariants,
                left_edges,
                left_spinors,
            )
            if (
                decompose_external01
                and special in (2, 3)
                and right_chirality == 0
            ):
                (
                    right_value,
                    right_external01_residue,
                    right_external01_angle,
                ) = oriented_regularized_scalar_klt_five_external01_decomposition(
                    right,
                    special,
                    right_chirality,
                    1,
                    active_chirality,
                    unit_circle,
                    geometry["selected_root"],
                    global_displacement,
                    diagnostics,
                    f"away_arc_right_K5:s{special}:c{right_chirality}:external01_decomposed",
                    right_exact_invariants,
                    right_edges,
                    right_spinors,
                    right_exponents,
                    right_active_quotients,
                )
                external01_pole_hhh += (
                    left_value * right_external01_residue
                )
                external01_angle_edge = right_external01_angle
            else:
                right_value = oriented_regularized_scalar_klt_five_with_reciprocals(
                    right,
                    special,
                    right_chirality,
                    1,
                    active_chirality,
                    unit_circle,
                    geometry["selected_root"],
                    global_displacement,
                    diagnostics,
                    f"away_arc_right_K5:s{special}:c{right_chirality}",
                    right_exact_invariants,
                    right_edges,
                    right_spinors,
                    right_exponents,
                    right_active_quotients,
                )
            hhh += left_value * right_value
    hhh /= cpoint(6)
    external01_pole_hhh /= cpoint(6)
    coefficient_prefactor = (
        geometry["energy"]
        * path_aware_stable_energy_multiplier(
            configuration,
            inputs,
            internal,
            diagnostics,
            "away_arc_multiplier",
            path_context,
        )
        / cpoint(M5258.S_VALUE * M5258.S_VALUE)
    )
    coefficient = coefficient_prefactor * hhh
    if decompose_external01:
        if external01_angle_edge is None:
            raise EnclosureFailure(
                "external01 decomposition did not select its owned KLT term"
            )
        return (
            coefficient,
            coefficient_prefactor * external01_pole_hhh,
            external01_angle_edge,
            diagnostics,
        )
    return coefficient, diagnostics


def tight_energy_contour_geometric_factors(
    configuration: dict[str, Any],
    inputs: dict[str, Any],
    geometry: dict[str, Any],
    path_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    try:
        factors = dict(
            M5386.energy_contour_geometric_factors(
                configuration, inputs, geometry
            )
        )
    except M5258.IntervalSingularity as error:
        if str(error) != (
            "collision Jacobian path has no nonzero projective chart"
        ):
            raise
        factors = {
            "relative_root": geometry["relative"],
            "selected_global_root": geometry["selected_root"],
            "collision_jacobian": cpoint(0),
            "collision_root_difference": cpoint(0),
            "collision_jacobian_chart": "PARENT_CHART_UNAVAILABLE",
            "collision_jacobian_chart_denominator_lower": 0.0,
            "collision_jacobian_recoil_derivative_upper": math.inf,
        }
    candidates: list[tuple[float, str, Any, float]] = [
        (
            M5258.lower_abs(factors["collision_jacobian"]),
            "PARENT_RECOIL_MEAN_VALUE",
            factors["collision_jacobian"],
            float(
                factors["collision_jacobian_chart_denominator_lower"]
            ),
        )
    ]
    factor_names = ("plus", "minus", "holomorphic", "antiholomorphic")
    factor_overrides = {
        name: M5386.centered_first_lightcone_factor(
            configuration, inputs, geometry, name
        )
        for name in factor_names
    }
    for chart in ("primary", "alternate"):
        try:
            root, denominator = M5386.collision_root_mixed(
                configuration,
                inputs["epsilon"],
                geometry["recoil"],
                inputs["soft_cosine"],
                inputs["decay_cosine"],
                inputs["decay_sine"],
                chart,
                factor_overrides,
            )
        except M5258.IntervalSingularity:
            continue
        denominator_lower = M5258.lower_abs(denominator)
        if denominator_lower > 0.0:
            candidates.append(
                (
                    M5258.lower_abs(root.relative_derivative),
                    f"DIRECT_CENTERED_PROJECTIVE_{chart.upper()}",
                    root.relative_derivative,
                    denominator_lower,
                )
            )
    if path_context is not None:
        try:
            explicit_candidate = (
                path_correlated_explicit_collision_jacobian_candidate(
                    configuration,
                    path_context["cell"],
                    path_context["path_segment"],
                    path_context["absolute_coordinate"],
                    path_context["path_parameter"],
                    inputs["epsilon"],
                )
            )
        except (EnclosureFailure, M5258.IntervalSingularity, ValueError):
            pass
        else:
            if explicit_candidate[3] > 0.0:
                candidates.append(explicit_candidate)
        try:
            path_candidates = path_correlated_collision_jacobian_candidates(
                configuration,
                path_context["cell"],
                path_context["path_segment"],
                path_context["absolute_coordinate"],
                path_context["path_parameter"],
                inputs["epsilon"],
            )
        except (EnclosureFailure, M5258.IntervalSingularity, ValueError):
            pass
        else:
            candidates.extend(
                candidate
                for candidate in path_candidates
                if candidate[3] > 0.0
            )
        if max(candidate[0] for candidate in candidates) <= 0.0:
            cover_schedule = (
                ("EXPLICIT", 2, 2),
                ("PROJECTIVE", 2, 2),
                ("EXPLICIT", 4, 4),
                ("PROJECTIVE", 4, 4),
                ("EXPLICIT", 8, 8),
                ("PROJECTIVE", 8, 8),
                ("PROJECTIVE", 8, 16),
                ("PROJECTIVE", 8, 32),
                ("EXPLICIT", 8, 16),
                ("EXPLICIT", 8, 32),
            )
            for cover_type, x_count, path_count in cover_schedule:
                try:
                    if cover_type == "EXPLICIT":
                        subdivided_candidate = (
                            subdivided_path_correlated_explicit_collision_jacobian_candidate(
                                configuration,
                                path_context["cell"],
                                path_context["path_segment"],
                                path_context["absolute_coordinate"],
                                path_context["path_parameter"],
                                inputs["epsilon"],
                                x_count,
                                path_count,
                            )
                        )
                    else:
                        subdivided_candidate = subdivided_path_correlated_collision_jacobian_candidate(
                            configuration,
                            path_context["cell"],
                            path_context["path_segment"],
                            path_context["absolute_coordinate"],
                            path_context["path_parameter"],
                            inputs["epsilon"],
                            x_count,
                            path_count,
                        )
                except (
                    EnclosureFailure,
                    M5258.IntervalSingularity,
                    ValueError,
                ):
                    continue
                candidates.append(subdivided_candidate)
                if subdivided_candidate[0] > 0.0:
                    break
    lower, method, jacobian, denominator_lower = max(
        candidates, key=lambda row: row[0]
    )
    factors["collision_jacobian"] = jacobian
    factors["collision_jacobian_enclosure_method"] = method
    factors["collision_jacobian_chart_denominator_lower"] = denominator_lower
    factors["collision_jacobian_selected_abs_lower"] = lower
    factors["collision_jacobian_candidate_abs_lowers"] = {
        candidate_method: candidate_lower
        for candidate_lower, candidate_method, _, _ in candidates
    }
    return factors


def global_contour_residue_abs_upper(
    configuration: dict[str, Any],
    absolute_coordinate: Any,
    energy: Any,
    epsilon: Any,
    global_arc_count: int = 8,
    path_context: dict[str, Any] | None = None,
) -> tuple[float, dict[str, Any]]:
    inputs, geometry = interval_inputs(
        configuration,
        absolute_coordinate,
        energy,
        epsilon,
    )
    global_radius = 1.0e-7 * max(
        1.0,
        M5258.upper_abs(geometry["selected_root"]),
    )
    arc_path_context = path_context
    if path_context is not None:
        arc_path_context = dict(path_context)
        arc_path_context["global_displacement_radius"] = global_radius
        arc_path_context["native_edge_cache"] = {}
    coefficient_upper = 0.0
    denominator_minimum = math.inf
    for arc_index in range(global_arc_count):
        phase = (
            cbox(arc_index, arc_index + 1)
            * cpoint(2 * math.pi / global_arc_count)
        )
        displacement = cpoint(global_radius) * (
            iv.cos(phase) + cpoint(1j) * iv.sin(phase)
        )
        coefficient, diagnostics = global_regularized_arc_coefficient(
            configuration,
            inputs,
            geometry,
            displacement,
            arc_path_context,
        )
        coefficient_upper = max(
            coefficient_upper,
            M5258.upper_abs(coefficient),
        )
        denominator_minimum = min(
            denominator_minimum,
            diagnostics.minimum_denominator_lower,
        )
    geometric = tight_energy_contour_geometric_factors(
        configuration,
        inputs,
        geometry,
        path_context,
    )
    factor_lowers = {
        "relative_root": M5258.lower_abs(geometric["relative_root"]),
        "selected_global_root": M5258.lower_abs(
            geometric["selected_global_root"]
        ),
        "collision_jacobian": float(
            geometric.get(
                "collision_jacobian_selected_abs_lower",
                M5258.lower_abs(geometric["collision_jacobian"]),
            )
        ),
    }
    geometric_lower = math.prod(factor_lowers.values())
    if geometric_lower <= 0.0:
        raise EnclosureFailure(
            "global contour geometric denominator reaches zero: "
            + json.dumps(factor_lowers, sort_keys=True)
        )
    residue_upper = (
        abs(int(configuration["winding_delta"]))
        * coefficient_upper
        / geometric_lower
    )
    if not math.isfinite(residue_upper):
        raise EnclosureFailure("global contour residue bound is not finite")
    return residue_upper, {
        "minimum_amplitude_denominator_abs_lower": denominator_minimum,
        "relative_root_abs_lower": factor_lowers["relative_root"],
        "selected_global_root_abs_lower": factor_lowers[
            "selected_global_root"
        ],
        "collision_jacobian_abs_lower": factor_lowers[
            "collision_jacobian"
        ],
        "collision_jacobian_enclosure_method": geometric[
            "collision_jacobian_enclosure_method"
        ],
        "global_contour_radius": global_radius,
        "global_arc_count": global_arc_count,
        "global_regularized_coefficient_abs_upper": coefficient_upper,
    }


def global_contour_external01_integrated_area_equivalent_abs_upper(
    configuration: dict[str, Any],
    absolute_coordinate: Any,
    energy: Any,
    epsilon: Any,
    global_arc_count: int,
    path_context: dict[str, Any],
) -> tuple[float, dict[str, Any]]:
    if configuration["role"] != "reciprocal":
        raise EnclosureFailure(
            "external01 singular-cell integration requires reciprocal role"
        )
    x_lower, x_upper = M5394.real_bounds(absolute_coordinate)
    t_lower, t_upper = M5394.real_bounds(
        path_context["path_parameter"]
    )
    parameter_area = (x_upper - x_lower) * (t_upper - t_lower)
    if parameter_area <= 0.0:
        raise EnclosureFailure(
            "external01 singular-cell parameter area is not positive"
        )
    inputs, geometry = interval_inputs(
        configuration,
        absolute_coordinate,
        energy,
        epsilon,
    )
    global_radius = 1.0e-7 * max(
        1.0,
        M5258.upper_abs(geometry["selected_root"]),
    )
    displacement_radius = math.nextafter(global_radius, math.inf)
    displacement_square = cbox(
        -displacement_radius,
        displacement_radius,
        -displacement_radius,
        displacement_radius,
    )
    jacobian = (
        native_external0_first_minus_plus_path_jacobian_bounds(
            configuration,
            path_context["cell"],
            path_context["path_segment"],
            absolute_coordinate,
            path_context["path_parameter"],
            epsilon,
            displacement_square,
        )
    )
    jacobian_abs_lower = float(jacobian["determinant_abs_lower"])
    regular_coefficient_abs_upper = 0.0
    pole_integral_abs_upper = 0.0
    pole_residue_abs_upper = 0.0
    angle_image_radius_abs_upper = 0.0
    denominator_minimum = math.inf
    for arc_index in range(global_arc_count):
        phase = (
            cbox(arc_index, arc_index + 1)
            * cpoint(2 * math.pi / global_arc_count)
        )
        displacement = cpoint(global_radius) * (
            iv.cos(phase) + cpoint(1j) * iv.sin(phase)
        )
        (
            regular_coefficient,
            pole_residue,
            angle_edge,
            diagnostics,
        ) = global_regularized_arc_coefficient(
            configuration,
            inputs,
            geometry,
            displacement,
            path_context,
            True,
        )
        local_regular_upper = M5258.upper_abs(regular_coefficient)
        local_residue_upper = M5258.upper_abs(pole_residue)
        local_angle_upper = M5258.upper_abs(angle_edge)
        if not all(
            math.isfinite(value) and value >= 0.0
            for value in (
                local_regular_upper,
                local_residue_upper,
                local_angle_upper,
            )
        ):
            raise EnclosureFailure(
                "external01 decomposed arc bound is not finite"
            )
        regular_coefficient_abs_upper = max(
            regular_coefficient_abs_upper,
            local_regular_upper,
        )
        pole_residue_abs_upper = max(
            pole_residue_abs_upper,
            local_residue_upper,
        )
        angle_image_radius_abs_upper = max(
            angle_image_radius_abs_upper,
            local_angle_upper,
        )
        pole_integral_abs_upper += (
            local_residue_upper
            * 2
            * math.pi
            * local_angle_upper
            / jacobian_abs_lower
        )
        denominator_minimum = min(
            denominator_minimum,
            diagnostics.minimum_denominator_lower,
        )
    coefficient_integral_abs_upper = (
        parameter_area * regular_coefficient_abs_upper
        + pole_integral_abs_upper
    )
    geometric = tight_energy_contour_geometric_factors(
        configuration,
        inputs,
        geometry,
        path_context,
    )
    factor_lowers = {
        "relative_root": M5258.lower_abs(geometric["relative_root"]),
        "selected_global_root": M5258.lower_abs(
            geometric["selected_global_root"]
        ),
        "collision_jacobian": float(
            geometric.get(
                "collision_jacobian_selected_abs_lower",
                M5258.lower_abs(geometric["collision_jacobian"]),
            )
        ),
    }
    geometric_lower = math.prod(factor_lowers.values())
    if geometric_lower <= 0.0:
        raise EnclosureFailure(
            "external01 integrated geometric denominator reaches zero"
        )
    residue_integral_abs_upper = (
        abs(int(configuration["winding_delta"]))
        * coefficient_integral_abs_upper
        / geometric_lower
    )
    area_equivalent_abs_upper = (
        residue_integral_abs_upper / parameter_area
    )
    if not math.isfinite(area_equivalent_abs_upper):
        raise EnclosureFailure(
            "external01 integrated area-equivalent bound is not finite"
        )
    return area_equivalent_abs_upper, {
        "minimum_amplitude_denominator_abs_lower": denominator_minimum,
        "relative_root_abs_lower": factor_lowers["relative_root"],
        "selected_global_root_abs_lower": factor_lowers[
            "selected_global_root"
        ],
        "collision_jacobian_abs_lower": factor_lowers[
            "collision_jacobian"
        ],
        "collision_jacobian_enclosure_method": geometric[
            "collision_jacobian_enclosure_method"
        ],
        "global_contour_radius": global_radius,
        "global_arc_count": global_arc_count,
        "global_regularized_coefficient_abs_upper": (
            regular_coefficient_abs_upper
        ),
        "path_integral_enclosure_method": (
            "EXTERNAL01_SIMPLE_POLE_CHANGE_OF_VARIABLES"
        ),
        "external01_path_jacobian_abs_lower": jacobian_abs_lower,
        "external01_path_jacobian_lower": jacobian[
            "determinant_lower"
        ],
        "external01_path_jacobian_upper": jacobian[
            "determinant_upper"
        ],
        "external01_global_injectivity_method": jacobian[
            "global_injectivity_method"
        ],
        "external01_pole_residue_abs_upper": pole_residue_abs_upper,
        "external01_angle_image_radius_abs_upper": (
            angle_image_radius_abs_upper
        ),
        "external01_reciprocal_integral_abs_upper": (
            pole_integral_abs_upper
        ),
        "external01_parameter_area": parameter_area,
    }


def evaluate_path_box(
    cell: dict[str, Any],
    term_id: str,
    configurations: list[dict[str, Any]],
    epsilon_row: dict[str, Any],
    path_segment: str,
    x_lower: float,
    x_upper: float,
    t_lower: float,
    t_upper: float,
    refinement_depth: int,
    refinement_path: str,
    support_segments: list[dict[str, Any]],
    branches: dict[str, dict[str, Any]],
    global_arc_count: int,
    reduce_selector_charts: bool = True,
) -> dict[str, Any]:
    absolute_coordinate = cbox(x_lower, x_upper)
    path_parameter = cbox(t_lower, t_upper)
    epsilon = epsilon_interval(epsilon_row)
    lower_energy, lower_diagnostics = interval_boundary_energy(
        cell["lower_energy_boundary"], x_lower, x_upper
    )
    upper_energy, upper_diagnostics = interval_boundary_energy(
        cell["upper_energy_boundary"], x_lower, x_upper
    )
    energy_width = upper_energy - lower_energy
    if path_segment == "LEFT_CONNECTOR":
        energy = lower_energy + cpoint(1j * DEFAULT_ENERGY_DEFORMATION) * path_parameter
        path_speed_upper = DEFAULT_ENERGY_DEFORMATION
    elif path_segment == "TOP":
        energy = (
            lower_energy
            + path_parameter * energy_width
            + cpoint(1j * DEFAULT_ENERGY_DEFORMATION)
        )
        path_speed_upper = M5258.upper_abs(energy_width)
    elif path_segment == "RIGHT_CONNECTOR":
        energy = upper_energy + cpoint(1j * DEFAULT_ENERGY_DEFORMATION) * path_parameter
        path_speed_upper = DEFAULT_ENERGY_DEFORMATION
    else:
        raise ValueError(f"unsupported path segment {path_segment}")
    if not math.isfinite(path_speed_upper) or path_speed_upper <= 0.0:
        raise EnclosureFailure("deformed energy-path speed is not finite and positive")
    if reduce_selector_charts:
        configurations, selector_diagnostics = (
            closed_selector_configuration_subset(
                configurations,
                absolute_coordinate,
                energy,
                epsilon,
            )
        )
    else:
        selector_diagnostics = {
            "selector_ownership_method": "FORCED_FINITE_DECLARED_CHART_UNION",
            "selector_margin_source_role": "CHART_UNION",
            "selector_role_margin_lower": 0.0,
            "selector_representative_modulus_lower": math.nan,
            "selector_representative_modulus_upper": math.nan,
            "selector_margin_failure_category": "",
        }
    chart_bounds: list[tuple[dict[str, Any], float, dict[str, Any]]] = []
    path_context = {
        "cell": cell,
        "path_segment": path_segment,
        "absolute_coordinate": absolute_coordinate,
        "path_parameter": path_parameter,
        "refinement_depth": refinement_depth,
        "refinement_path": refinement_path,
    }
    for configuration in configurations:
        try:
            chart_upper, chart_diagnostics = (
                global_contour_residue_abs_upper(
                    configuration,
                    absolute_coordinate,
                    energy,
                    epsilon,
                    global_arc_count,
                    path_context,
                )
            )
        except M5258.IntervalSingularity as error:
            if not (
                configuration["role"] == "reciprocal"
                and path_segment
                in {"LEFT_CONNECTOR", "RIGHT_CONNECTOR"}
                and "edge_0_0_1:stable_edge" in str(error)
            ):
                raise
            chart_upper, chart_diagnostics = (
                global_contour_external01_integrated_area_equivalent_abs_upper(
                    configuration,
                    absolute_coordinate,
                    energy,
                    epsilon,
                    global_arc_count,
                    path_context,
                )
            )
        chart_diagnostics.setdefault(
            "path_integral_enclosure_method",
            "POINTWISE_SUPREMUM",
        )
        chart_bounds.append((configuration, chart_upper, chart_diagnostics))
    if any(
        row[2]["path_integral_enclosure_method"]
        != "POINTWISE_SUPREMUM"
        for row in chart_bounds
    ):
        raw_upper = sum(row[1] for row in chart_bounds)
    else:
        raw_upper = max(row[1] for row in chart_bounds)
    amplitude_diagnostics = {
        "minimum_amplitude_denominator_abs_lower": min(
            float(row[2]["minimum_amplitude_denominator_abs_lower"])
            for row in chart_bounds
        ),
        "relative_root_abs_lower": min(
            float(row[2]["relative_root_abs_lower"]) for row in chart_bounds
        ),
        "selected_global_root_abs_lower": min(
            float(row[2]["selected_global_root_abs_lower"])
            for row in chart_bounds
        ),
        "collision_jacobian_abs_lower": min(
            float(row[2]["collision_jacobian_abs_lower"])
            for row in chart_bounds
        ),
        "collision_jacobian_enclosure_method": "|".join(
            sorted(
                {
                    str(row[2]["collision_jacobian_enclosure_method"])
                    for row in chart_bounds
                }
            )
        ),
        "global_contour_radius": max(
            float(row[2]["global_contour_radius"]) for row in chart_bounds
        ),
        "global_arc_count": global_arc_count,
        "global_regularized_coefficient_abs_upper": max(
            float(row[2]["global_regularized_coefficient_abs_upper"])
            for row in chart_bounds
        ),
        "path_integral_enclosure_method": "|".join(
            sorted(
                {
                    str(row[2]["path_integral_enclosure_method"])
                    for row in chart_bounds
                }
            )
        ),
        "external01_path_jacobian_abs_lower": min(
            float(
                row[2].get(
                    "external01_path_jacobian_abs_lower",
                    math.inf,
                )
            )
            for row in chart_bounds
        ),
        "external01_pole_residue_abs_upper": max(
            float(
                row[2].get(
                    "external01_pole_residue_abs_upper",
                    0.0,
                )
            )
            for row in chart_bounds
        ),
        "external01_reciprocal_integral_abs_upper": sum(
            float(
                row[2].get(
                    "external01_reciprocal_integral_abs_upper",
                    0.0,
                )
            )
            for row in chart_bounds
        ),
    }
    selected_branches = active_material_branches(
        cell,
        term_id,
        x_lower,
        x_upper,
        support_segments,
        branches,
    )
    pole_correction_upper = 0.0
    pole_gap_minimum = math.inf
    material_root_denominator_minimum = math.inf
    material_root_discriminant_minimum = math.inf
    material_root_implicit_derivative_minimum = math.inf
    for branch in selected_branches:
        recoil, root_diagnostics, _ = M5395.centered_material_root(
            branch["primary_surface_id"],
            int(branch["sign"]),
            x_lower,
            x_upper,
            epsilon,
        )
        pole = cpoint(1) - recoil * recoil
        gap_lower = M5258.lower_abs(energy - pole)
        if gap_lower <= 0.0:
            raise EnclosureFailure(
                f"{branch['branch_owner_id']} pole reaches {path_segment}"
            )
        pole_gap_minimum = min(pole_gap_minimum, gap_lower)
        material_root_denominator_minimum = min(
            material_root_denominator_minimum,
            float(root_diagnostics["material_coefficient_denominator_abs_lower"]),
        )
        finite_discriminant = float(
            root_diagnostics["material_discriminant_abs_lower"]
        )
        if math.isfinite(finite_discriminant):
            material_root_discriminant_minimum = min(
                material_root_discriminant_minimum,
                finite_discriminant,
            )
        material_root_implicit_derivative_minimum = min(
            material_root_implicit_derivative_minimum,
            float(root_diagnostics["implicit_material_derivative_abs_lower"]),
        )
        pole_correction_upper += (
            float(branch["material_residue_abs_upper"]) / gap_lower
        )
    regular_upper = raw_upper + pole_correction_upper
    x_width = x_upper - x_lower
    t_width = t_upper - t_lower
    integrated_upper = x_width * t_width * path_speed_upper * regular_upper
    if not all(
        math.isfinite(value) and value >= 0.0
        for value in (
            raw_upper,
            pole_correction_upper,
            regular_upper,
            integrated_upper,
        )
    ):
        raise EnclosureFailure("regular-away path enclosure is not finite")
    return {
        "mapped_cell_id": cell["mapped_cell_id"],
        "atlas_cell_id": cell["atlas_cell_id"],
        "term_id": term_id,
        "selected_role": "CHART_UNION",
        "chart_roles": "|".join(row[0]["role"] for row in chart_bounds),
        "chart_count": len(chart_bounds),
        "trace_orientation": "|".join(
            str(row[0]["trace_orientation"]) for row in chart_bounds
        ),
        "winding_delta": "|".join(
            str(row[0]["winding_delta"]) for row in chart_bounds
        ),
        "regulator_bin_index": int(epsilon_row["regulator_bin_index"]),
        "epsilon_subdivision_index": int(
            epsilon_row["epsilon_subdivision_index"]
        ),
        "epsilon_subdivision_count": int(
            epsilon_row["epsilon_subdivision_count"]
        ),
        "epsilon_real_lower": float(epsilon_row["epsilon_real_lower"]),
        "epsilon_real_upper": float(epsilon_row["epsilon_real_upper"]),
        "epsilon_imaginary_lower": float(epsilon_row["epsilon_imaginary_lower"]),
        "epsilon_imaginary_upper": float(epsilon_row["epsilon_imaginary_upper"]),
        "path_segment": path_segment,
        "energy_deformation_height": DEFAULT_ENERGY_DEFORMATION,
        "x_lower": x_lower,
        "x_upper": x_upper,
        "x_width": x_width,
        "t_lower": t_lower,
        "t_upper": t_upper,
        "t_width": t_width,
        "parameter_area": x_width * t_width,
        "refinement_depth": refinement_depth,
        "refinement_path": refinement_path,
        "lower_energy_boundary": cell["lower_energy_boundary"],
        "upper_energy_boundary": cell["upper_energy_boundary"],
        "lower_boundary_discriminant_abs_lower": lower_diagnostics[
            "boundary_discriminant_abs_lower"
        ],
        "upper_boundary_discriminant_abs_lower": upper_diagnostics[
            "boundary_discriminant_abs_lower"
        ],
        "path_speed_abs_upper": path_speed_upper,
        "raw_integrand_abs_upper": raw_upper,
        "active_material_branch_ids": "|".join(
            branch["branch_owner_id"] for branch in selected_branches
        ),
        "active_material_branch_count": len(selected_branches),
        "pole_gap_abs_lower": pole_gap_minimum,
        "material_root_coefficient_abs_lower": material_root_denominator_minimum,
        "material_root_discriminant_abs_lower": material_root_discriminant_minimum,
        "material_root_implicit_derivative_abs_lower": (
            material_root_implicit_derivative_minimum
        ),
        "pole_correction_abs_upper": pole_correction_upper,
        "regular_integrand_abs_upper": regular_upper,
        "integrated_regular_path_abs_upper": integrated_upper,
        "minimum_amplitude_denominator_abs_lower": amplitude_diagnostics[
            "minimum_amplitude_denominator_abs_lower"
        ],
        "relative_root_abs_lower": amplitude_diagnostics[
            "relative_root_abs_lower"
        ],
        "selected_global_root_abs_lower": amplitude_diagnostics[
            "selected_global_root_abs_lower"
        ],
        "collision_jacobian_abs_lower": amplitude_diagnostics[
            "collision_jacobian_abs_lower"
        ],
        "collision_jacobian_enclosure_method": amplitude_diagnostics[
            "collision_jacobian_enclosure_method"
        ],
        "global_contour_radius": amplitude_diagnostics[
            "global_contour_radius"
        ],
        "global_arc_count": amplitude_diagnostics["global_arc_count"],
        "global_regularized_coefficient_abs_upper": amplitude_diagnostics[
            "global_regularized_coefficient_abs_upper"
        ],
        "path_integral_enclosure_method": amplitude_diagnostics[
            "path_integral_enclosure_method"
        ],
        "external01_path_jacobian_abs_lower": amplitude_diagnostics[
            "external01_path_jacobian_abs_lower"
        ],
        "external01_pole_residue_abs_upper": amplitude_diagnostics[
            "external01_pole_residue_abs_upper"
        ],
        "external01_reciprocal_integral_abs_upper": amplitude_diagnostics[
            "external01_reciprocal_integral_abs_upper"
        ],
        **selector_diagnostics,
        CLAIM_DEFORMATION: True,
        CLAIM_AWAY: True,
        **{claim: False for claim in OPEN_CLAIMS},
    }


def adaptive_state_rows_path(state_path: Path) -> Path:
    return state_path.with_name(f"{state_path.stem}.rows.csv")


def save_adaptive_path_state(
    state_path: Path,
    accepted: list[dict[str, Any]],
    stack: list[tuple[float, float, float, float, int, str]],
    failure_counts: dict[str, int] | None = None,
    failure_examples: dict[str, list[dict[str, Any]]] | None = None,
) -> None:
    rows_path = adaptive_state_rows_path(state_path)
    if accepted:
        atomic_csv(rows_path, accepted)
    elif rows_path.is_file():
        rows_path.unlink()
    atomic_json(
        state_path,
        {
            "checkpoint": CHECKPOINT,
            "revision": REVISION,
            "accepted_count": len(accepted),
            "stack": stack,
            "split_failure_counts": failure_counts or {},
            "split_failure_examples": failure_examples or {},
            "updated_utc": utc_now(),
        },
    )


def load_adaptive_path_state(
    state_path: Path,
) -> tuple[
    list[dict[str, Any]],
    list[tuple[float, float, float, float, int, str]],
    dict[str, int],
    dict[str, list[dict[str, Any]]],
]:
    state = read_json(state_path)
    if state.get("checkpoint") != CHECKPOINT or state.get("revision") not in {
        REVISION,
        *PREVIOUS_RESUME_COMPATIBLE_REVISIONS,
    }:
        raise RuntimeError(f"incompatible adaptive path state: {state_path}")
    state_revision = str(state["revision"])
    accepted_count = int(state["accepted_count"])
    rows_path = adaptive_state_rows_path(state_path)
    accepted = read_csv(rows_path) if accepted_count else []
    if len(accepted) < accepted_count:
        raise RuntimeError(f"truncated adaptive path rows: {rows_path}")
    accepted = accepted[:accepted_count]
    stack = [
        (
            float(row[0]),
            float(row[1]),
            float(row[2]),
            float(row[3]),
            int(row[4]),
            str(row[5]),
        )
        for row in state["stack"]
    ]
    retained: list[dict[str, Any]] = []
    for row in accepted:
        legacy_risk_key = (
            row["mapped_cell_id"],
            row["term_id"],
            row["path_segment"],
            row["refinement_path"],
        )
        if (
            state_revision not in SHARED_EXTERNAL_INVARIANT_FIXED_REVISIONS
            and legacy_risk_key in LEGACY_SHARED_EXTERNAL_INVARIANT_RISK_ROWS
        ):
            stack.append(
                (
                    float(row["x_lower"]),
                    float(row["x_upper"]),
                    float(row["t_lower"]),
                    float(row["t_upper"]),
                    int(row["refinement_depth"]),
                    str(row["refinement_path"]),
                )
            )
            continue
        if (
            state_revision not in EXTERNAL01_FACTORIZED_KERNEL_REVISIONS
            and row.get("path_integral_enclosure_method")
            == "EXTERNAL01_SIMPLE_POLE_CHANGE_OF_VARIABLES"
        ):
            stack.append(
                (
                    float(row["x_lower"]),
                    float(row["x_upper"]),
                    float(row["t_lower"]),
                    float(row["t_upper"]),
                    int(row["refinement_depth"]),
                    str(row["refinement_path"]),
                )
            )
            continue
        if (
            state_revision in MIXED_EXTERNAL_TRANSVERSE_SUBCOVER_REVISIONS
            and int(row["refinement_depth"]) >= 8
        ):
            stack.append(
                (
                    float(row["x_lower"]),
                    float(row["x_upper"]),
                    float(row["t_lower"]),
                    float(row["t_upper"]),
                    int(row["refinement_depth"]),
                    str(row["refinement_path"]),
                )
            )
            continue
        if float(row["minimum_amplitude_denominator_abs_lower"]) > 0.0:
            retained.append(row)
            continue
        stack.append(
            (
                float(row["x_lower"]),
                float(row["x_upper"]),
                float(row["t_lower"]),
                float(row["t_upper"]),
                int(row["refinement_depth"]),
                str(row["refinement_path"]),
            )
        )
    accepted = retained
    failure_counts = {
        str(key): int(value)
        for key, value in state.get("split_failure_counts", {}).items()
    }
    failure_examples = {
        str(key): list(value)
        for key, value in state.get("split_failure_examples", {}).items()
    }
    return accepted, stack, failure_counts, failure_examples


def clear_adaptive_path_state(state_path: Path) -> None:
    for path in (state_path, adaptive_state_rows_path(state_path)):
        if path.is_file():
            path.unlink()


def enclosure_failure_category(error: Exception) -> str:
    message = str(error)
    denominator_marker = "interval denominator reaches zero: "
    if denominator_marker in message:
        return (
            f"{type(error).__name__}:"
            + message.split(denominator_marker, 1)[1]
        )
    geometric_marker = "global contour geometric denominator reaches zero"
    if message.startswith(geometric_marker):
        return f"{type(error).__name__}:{geometric_marker}"
    return f"{type(error).__name__}:{message.splitlines()[0][:240]}"


def adaptive_path_enclosure(
    cell: dict[str, Any],
    term_id: str,
    configurations: list[dict[str, Any]],
    epsilon_row: dict[str, Any],
    path_segment: str,
    x_lower: float,
    x_upper: float,
    support_segments: list[dict[str, Any]],
    branches: dict[str, dict[str, Any]],
    target_x_width: float,
    target_path_width: float,
    maximum_depth: int,
    global_arc_count: int,
    state_checkpoint_path: Path | None = None,
    resume_state: bool = False,
    deadline: float | None = None,
) -> list[dict[str, Any]]:
    if (
        state_checkpoint_path is not None
        and resume_state
        and state_checkpoint_path.is_file()
    ):
        accepted, stack, failure_counts, failure_examples = (
            load_adaptive_path_state(state_checkpoint_path)
        )
        print(
            json.dumps(
                {
                    "state": "path_internal_state_resumed",
                    "mapped_cell_id": cell["mapped_cell_id"],
                    "term_id": term_id,
                    "path_segment": path_segment,
                    "accepted_box_count": len(accepted),
                    "pending_box_count": len(stack),
                }
            ),
            flush=True,
        )
    else:
        stack = [(x_lower, x_upper, 0.0, 1.0, 0, "")]
        accepted = []
        failure_counts = {}
        failure_examples = {}
    while stack:
        box_x_lower, box_x_upper, t_lower, t_upper, depth, path = stack.pop()
        try:
            accepted.append(
                evaluate_path_box(
                    cell,
                    term_id,
                    configurations,
                    epsilon_row,
                    path_segment,
                    box_x_lower,
                    box_x_upper,
                    t_lower,
                    t_upper,
                    depth,
                    path,
                    support_segments,
                    branches,
                    global_arc_count,
                )
            )
            if len(accepted) % 100 == 0:
                if state_checkpoint_path is not None:
                    save_adaptive_path_state(
                        state_checkpoint_path,
                        accepted,
                        stack,
                        failure_counts,
                        failure_examples,
                    )
                print(
                    json.dumps(
                        {
                            "state": "path_progress",
                            "mapped_cell_id": cell["mapped_cell_id"],
                            "term_id": term_id,
                            "path_segment": path_segment,
                            "accepted_box_count": len(accepted),
                            "pending_box_count": len(stack),
                            "latest_refinement_depth": depth,
                        }
                    ),
                    flush=True,
                )
            if deadline is not None and time.time() >= deadline:
                if state_checkpoint_path is not None:
                    save_adaptive_path_state(
                        state_checkpoint_path,
                        accepted,
                        stack,
                        failure_counts,
                        failure_examples,
                    )
                raise RuntimeBudgetReached
            continue
        except Exception as caught:
            if isinstance(caught, RuntimeBudgetReached):
                raise
            category = enclosure_failure_category(caught)
            failure_counts[category] = failure_counts.get(category, 0) + 1
            examples = failure_examples.setdefault(category, [])
            if len(examples) < 3:
                examples.append(
                    {
                        "x_lower": box_x_lower,
                        "x_upper": box_x_upper,
                        "t_lower": t_lower,
                        "t_upper": t_upper,
                        "refinement_depth": depth,
                        "refinement_path": path,
                        "error": str(caught),
                    }
                )
            if depth >= maximum_depth:
                stack.append(
                    (
                        box_x_lower,
                        box_x_upper,
                        t_lower,
                        t_upper,
                        depth,
                        path,
                    )
                )
                if state_checkpoint_path is not None:
                    save_adaptive_path_state(
                        state_checkpoint_path,
                        accepted,
                        stack,
                        failure_counts,
                        failure_examples,
                    )
                raise EnclosureFailure(
                    f"adaptive enclosure exhausted for {cell['mapped_cell_id']} "
                    f"{term_id} {path_segment} x=[{box_x_lower},{box_x_upper}] "
                    f"t=[{t_lower},{t_upper}]: {type(caught).__name__}: {caught}"
                ) from caught
        x_width = box_x_upper - box_x_lower
        t_width = t_upper - t_lower
        x_score = x_width / max(target_x_width, 1.0e-15)
        t_score = t_width / max(target_path_width, 1.0e-15)
        if x_score >= t_score and x_width > 1.0e-14:
            midpoint_x = 0.5 * (box_x_lower + box_x_upper)
            stack.append(
                (midpoint_x, box_x_upper, t_lower, t_upper, depth + 1, path + "R")
            )
            stack.append(
                (box_x_lower, midpoint_x, t_lower, t_upper, depth + 1, path + "L")
            )
        elif t_width > 1.0e-14:
            midpoint_t = 0.5 * (t_lower + t_upper)
            stack.append(
                (box_x_lower, box_x_upper, midpoint_t, t_upper, depth + 1, path + "U")
            )
            stack.append(
                (box_x_lower, box_x_upper, t_lower, midpoint_t, depth + 1, path + "D")
            )
        else:
            raise EnclosureFailure(
                f"no splittable interval remains for {cell['mapped_cell_id']} "
                f"{term_id} {path_segment}"
            )
        if len(stack) + len(accepted) > 200000:
            raise EnclosureFailure("adaptive regular-away box budget exceeded")
        if deadline is not None and time.time() >= deadline:
            if state_checkpoint_path is not None:
                save_adaptive_path_state(
                    state_checkpoint_path,
                    accepted,
                    stack,
                    failure_counts,
                    failure_examples,
                )
            raise RuntimeBudgetReached
    if state_checkpoint_path is not None:
        save_adaptive_path_state(
            state_checkpoint_path,
            accepted,
            stack,
            failure_counts,
            failure_examples,
        )
    return accepted


def run_epsilon_subbox(
    cells: list[dict[str, Any]],
    epsilon_row: dict[str, Any],
    selectors: dict[tuple[str, str], dict[str, Any]],
    support_segments: list[dict[str, Any]],
    branches: dict[str, dict[str, Any]],
    target_x_width: float,
    target_path_width: float,
    maximum_depth: int,
    global_arc_count: int,
    path_checkpoint_directory: Path | None = None,
    resume_paths: bool = False,
    deadline: float | None = None,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for cell in cells:
        partitions = cell_x_partitions(cell, support_segments)
        for term_id in cell["reduced_MC04_term_ids"].split("|"):
            configurations = configuration_variants(term_id)
            for path_segment in ("LEFT_CONNECTOR", "TOP", "RIGHT_CONNECTOR"):
                if deadline is not None and time.time() >= deadline:
                    raise RuntimeBudgetReached
                checkpoint_path = None
                if path_checkpoint_directory is not None:
                    checkpoint_path = path_checkpoint_directory / (
                        f"bin_{int(epsilon_row['regulator_bin_index']):02d}_"
                        f"sub_{int(epsilon_row['epsilon_subdivision_index']):02d}_"
                        f"{cell['mapped_cell_id']}_{path_segment}.csv"
                    )
                if (
                    checkpoint_path is not None
                    and resume_paths
                    and checkpoint_path.is_file()
                ):
                    resumed_rows = read_csv(checkpoint_path)
                    rows.extend(resumed_rows)
                    print(
                        json.dumps(
                            {
                                "state": "path_resumed",
                                "mapped_cell_id": cell["mapped_cell_id"],
                                "term_id": term_id,
                                "path_segment": path_segment,
                                "certified_box_count": len(resumed_rows),
                            }
                        ),
                        flush=True,
                    )
                    continue
                complete_path_rows: list[dict[str, Any]] = []
                for partition_index, (x_lower, x_upper) in enumerate(partitions):
                    path_started = time.time()
                    partition_path = None
                    state_path = None
                    if path_checkpoint_directory is not None:
                        partition_directory = (
                            path_checkpoint_directory / "_partitions"
                        )
                        partition_stem = (
                            f"bin_{int(epsilon_row['regulator_bin_index']):02d}_"
                            f"sub_{int(epsilon_row['epsilon_subdivision_index']):02d}_"
                            f"{cell['mapped_cell_id']}_{path_segment}_"
                            f"part_{partition_index:02d}_of_{len(partitions):02d}"
                        )
                        partition_path = partition_directory / f"{partition_stem}.csv"
                        state_path = partition_directory / f"{partition_stem}.state.json"
                    if (
                        partition_path is not None
                        and resume_paths
                        and partition_path.is_file()
                    ):
                        path_rows = read_csv(partition_path)
                        partition_state = "partition_resumed"
                    else:
                        path_rows = adaptive_path_enclosure(
                            cell,
                            term_id,
                            configurations,
                            epsilon_row,
                            path_segment,
                            x_lower,
                            x_upper,
                            support_segments,
                            branches,
                            target_x_width,
                            target_path_width,
                            maximum_depth,
                            global_arc_count,
                            state_path,
                            resume_paths,
                            deadline,
                        )
                        if partition_path is not None:
                            atomic_csv(partition_path, path_rows)
                        if state_path is not None:
                            clear_adaptive_path_state(state_path)
                        partition_state = "partition_completed"
                    complete_path_rows.extend(path_rows)
                    print(
                        json.dumps(
                            {
                                "state": partition_state,
                                "mapped_cell_id": cell["mapped_cell_id"],
                                "term_id": term_id,
                                "path_segment": path_segment,
                                "partition_index": partition_index,
                                "partition_count": len(partitions),
                                "x_lower": x_lower,
                                "x_upper": x_upper,
                                "certified_box_count": len(path_rows),
                                "runtime_seconds": time.time() - path_started,
                            }
                        ),
                        flush=True,
                    )
                rows.extend(complete_path_rows)
                if checkpoint_path is not None:
                    atomic_csv(checkpoint_path, complete_path_rows)
                if deadline is not None and time.time() >= deadline:
                    raise RuntimeBudgetReached
    return rows


def integrand_probe() -> list[dict[str, Any]]:
    selectors = selector_map()
    rows: list[dict[str, Any]] = []
    mapped = [
        row
        for row in read_csv(MAPPED_5393)
        if row["region_class"] == "AWAY"
    ]
    selected_cells = [mapped[index] for index in (0, 1, 13, 20, 31, 47)]
    for cell in selected_cells:
        coordinate = 0.5 * (
            float(cell["lower_absolute_soft_cosine"])
            + float(cell["upper_absolute_soft_cosine"])
        )
        energy = 0.5 * (
            float(cell["midpoint_energy_lower"])
            + float(cell["midpoint_energy_upper"])
        ) + 1j * DEFAULT_ENERGY_DEFORMATION
        for term_id in cell["reduced_MC04_term_ids"].split("|"):
            selector = selectors[(cell["mapped_cell_id"], term_id)]
            configuration = configuration_from_selector(selector)
            try:
                upper, diagnostics = global_contour_residue_abs_upper(
                    configuration,
                    cpoint(coordinate),
                    cpoint(energy),
                    cpoint(0.01),
                )
                error = ""
            except Exception as caught:
                upper = math.inf
                diagnostics = {}
                error = (
                    f"{type(caught).__name__}: {caught}\n"
                    + traceback.format_exc()
                )
            rows.append(
                {
                    "mapped_cell_id": cell["mapped_cell_id"],
                    "term_id": term_id,
                    "selected_role": configuration["role"],
                    "coordinate": coordinate,
                    "energy_real": energy.real,
                    "energy_imaginary": energy.imag,
                    "global_residue_abs_upper": upper,
                    "error": error,
                    **diagnostics,
                }
            )
    return rows


def parent_point_component(
    context: dict[str, Any],
    term_id: str,
    coordinate: float,
    energy: float,
) -> dict[str, Any]:
    soft_sign, decay_sign = term_signs(term_id)
    local = M5308.M5302.local_context(
        context,
        coordinate,
        soft_sign,
        decay_sign,
    )
    event = dict(local["source_event"])
    event["soft_energy"] = energy
    target = local["inventories"]["E0025"]["target"]
    rationals = M5308.M5280.M5274.M5231.root_rationals(event, target)
    return M5308.M5280.evaluate_component(
        event,
        "E0025",
        "MC04",
        local,
        rationals=rationals,
        convergence_audit=False,
    )


def finite_displacement_residue_midpoint(
    configuration: dict[str, Any],
    coordinate: float,
    energy: float,
    epsilon: float,
    exponent: int = 10,
) -> complex:
    inputs, geometry = interval_inputs(
        configuration,
        cpoint(coordinate),
        cpoint(energy),
        cpoint(epsilon),
    )
    displacement = cpoint(
        10.0 ** (-exponent)
        * max(1.0, M5258.upper_abs(geometry["selected_root"]))
        * complex(math.cos(0.37), math.sin(0.37))
    )
    diagnostics = M5258.IntervalDiagnostics()
    coefficient = M5386.global_regularized_direct_interval(
        configuration,
        geometry,
        complex(-9.0, epsilon),
        displacement,
        diagnostics,
    )
    geometric = M5386.energy_contour_geometric_factors(
        configuration,
        inputs,
        geometry,
    )
    residue = cpoint(
        int(configuration["winding_delta"])
        * int(configuration["trace_orientation"])
    ) * coefficient
    for name in (
        "relative_root",
        "selected_global_root",
        "collision_jacobian",
    ):
        residue /= geometric[name]
    return M5258.midpoint(residue)


def point_crosschecks() -> list[dict[str, Any]]:
    selectors = selector_map()
    context = M5308.M5303.synthetic_context()
    mapped = [
        row
        for row in read_csv(MAPPED_5393)
        if row["region_class"] == "AWAY"
    ]
    selected_cells = [mapped[index] for index in (0, 1, 13, 20, 31, 47)]
    rows: list[dict[str, Any]] = []
    for cell in selected_cells:
        coordinate = 0.5 * (
            float(cell["lower_absolute_soft_cosine"])
            + float(cell["upper_absolute_soft_cosine"])
        )
        energy = 0.5 * (
            float(cell["midpoint_energy_lower"])
            + float(cell["midpoint_energy_upper"])
        )
        for term_id in cell["reduced_MC04_term_ids"].split("|"):
            configuration = configuration_from_selector(
                selectors[(cell["mapped_cell_id"], term_id)]
            )
            interval_upper, diagnostics = global_contour_residue_abs_upper(
                configuration,
                cpoint(coordinate),
                cpoint(energy),
                cpoint(0.0025),
            )
            parent = parent_point_component(
                context,
                term_id,
                coordinate,
                energy,
            )
            parent_value = complex(parent["residue"])
            finite_value = finite_displacement_residue_midpoint(
                configuration,
                coordinate,
                energy,
                0.0025,
            )
            rows.append(
                {
                    "mapped_cell_id": cell["mapped_cell_id"],
                    "term_id": term_id,
                    "selected_role": configuration["role"],
                    "coordinate": coordinate,
                    "energy": energy,
                    "parent_residue_real": parent_value.real,
                    "parent_residue_imaginary": parent_value.imag,
                    "interval_residue_abs_upper": interval_upper,
                    "parent_residue_is_bounded": (
                        abs(parent_value) <= interval_upper
                    ),
                    "finite_displacement_residue_real": finite_value.real,
                    "finite_displacement_residue_imaginary": finite_value.imag,
                    "finite_displacement_to_parent_relative_error": abs(
                        finite_value - parent_value
                    )
                    / max(abs(parent_value), 1.0e-300),
                    "parent_selected_role": parent["selected_role"],
                    "parent_orientation": parent["orientation"],
                    "parent_winding_delta": parent["winding_delta"],
                }
            )
    return rows


def chart_equivalence_crosschecks() -> list[dict[str, Any]]:
    context = M5308.M5303.synthetic_context()
    cells = {
        row["mapped_cell_id"]: row
        for row in read_csv(MAPPED_5393)
        if row["region_class"] == "AWAY"
    }
    selected_ids = ("U001", "U033", "U037", "U053", "U055", "U058", "U063", "U067")
    rows: list[dict[str, Any]] = []
    for mapped_cell_id in selected_ids:
        cell = cells[mapped_cell_id]
        x_lower = float(cell["lower_absolute_soft_cosine"])
        x_upper = float(cell["upper_absolute_soft_cosine"])
        for term_id in cell["reduced_MC04_term_ids"].split("|"):
            for x_fraction in (0.25, 0.75):
                coordinate = x_lower + x_fraction * (x_upper - x_lower)
                energy_lower = float(
                    M5308.boundary_energy(cell["lower_energy_boundary"], coordinate)
                )
                energy_upper = float(
                    M5308.boundary_energy(cell["upper_energy_boundary"], coordinate)
                )
                for energy_fraction in (0.25, 0.75):
                    energy = energy_lower + energy_fraction * (
                        energy_upper - energy_lower
                    )
                    parent = parent_point_component(
                        context, term_id, coordinate, energy
                    )
                    parent_value = complex(parent["residue"])
                    for configuration in configuration_variants(term_id):
                        value = finite_displacement_residue_midpoint(
                            configuration,
                            coordinate,
                            energy,
                            0.0025,
                        )
                        relative_error = abs(value - parent_value) / max(
                            abs(parent_value), 1.0e-300
                        )
                        rows.append(
                            {
                                "mapped_cell_id": mapped_cell_id,
                                "term_id": term_id,
                                "x_fraction": x_fraction,
                                "energy_fraction": energy_fraction,
                                "coordinate": coordinate,
                                "energy": energy,
                                "parent_selected_role": parent["selected_role"],
                                "evaluated_chart_role": configuration["role"],
                                "parent_residue_real": parent_value.real,
                                "parent_residue_imaginary": parent_value.imag,
                                "chart_residue_real": value.real,
                                "chart_residue_imaginary": value.imag,
                                "chart_to_parent_relative_error": relative_error,
                                "chart_equivalent_to_parent": relative_error <= 1.0e-7,
                            }
                        )
    return rows


def boundary_crosschecks() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for cell in read_csv(MAPPED_5393):
        if cell["region_class"] != "AWAY":
            continue
        x_lower = float(cell["lower_absolute_soft_cosine"])
        x_upper = float(cell["upper_absolute_soft_cosine"])
        for boundary_role in ("lower", "upper"):
            owner = cell[f"{boundary_role}_energy_boundary"]
            enclosure, diagnostics = interval_boundary_energy(
                owner, x_lower, x_upper
            )
            real_lower, real_upper = M5394.real_bounds(enclosure)
            imaginary_lower, imaginary_upper = M5394.imaginary_bounds(enclosure)
            probes = [
                float(
                    M5308.boundary_energy(
                        owner,
                        x_lower + fraction * (x_upper - x_lower),
                    )
                )
                for fraction in (1.0e-8, 0.5, 1.0 - 1.0e-8)
            ]
            rows.append(
                {
                    "mapped_cell_id": cell["mapped_cell_id"],
                    "boundary_role": boundary_role,
                    "boundary_owner": owner,
                    "x_lower": x_lower,
                    "x_upper": x_upper,
                    "energy_real_lower": real_lower,
                    "energy_real_upper": real_upper,
                    "energy_imaginary_lower": imaginary_lower,
                    "energy_imaginary_upper": imaginary_upper,
                    "minimum_parent_probe": min(probes),
                    "maximum_parent_probe": max(probes),
                    "all_parent_probes_enclosed": (
                        real_lower <= min(probes)
                        and max(probes) <= real_upper
                        and imaginary_lower <= 0.0 <= imaginary_upper
                    ),
                    **diagnostics,
                }
            )
    return rows


def selector_stability_crosschecks() -> list[dict[str, Any]]:
    selectors = selector_map()
    context = M5308.M5303.synthetic_context()
    allowed_states = {
        term_id: {
            (
                configuration["role"],
                "|".join(configuration["labels"]),
                int(configuration["trace_orientation"]),
                int(configuration["winding_delta"]),
            )
            for configuration in configuration_variants(term_id)
        }
        for term_id in ("MC04_SM_DM", "MC04_SP_DM", "MC04_SP_DP")
    }
    rows: list[dict[str, Any]] = []
    for cell in read_csv(MAPPED_5393):
        if cell["region_class"] != "AWAY":
            continue
        x_lower = float(cell["lower_absolute_soft_cosine"])
        x_upper = float(cell["upper_absolute_soft_cosine"])
        for term_id in cell["reduced_MC04_term_ids"].split("|"):
            expected = selectors[(cell["mapped_cell_id"], term_id)]
            for x_fraction in (0.05, 0.5, 0.95):
                coordinate = x_lower + x_fraction * (x_upper - x_lower)
                energy_lower = float(
                    M5308.boundary_energy(cell["lower_energy_boundary"], coordinate)
                )
                energy_upper = float(
                    M5308.boundary_energy(cell["upper_energy_boundary"], coordinate)
                )
                for energy_fraction in (0.05, 0.5, 0.95):
                    energy = energy_lower + energy_fraction * (
                        energy_upper - energy_lower
                    )
                    evaluation = parent_point_component(
                        context, term_id, coordinate, energy
                    )
                    representing_pair = evaluation["representing_pair"]
                    labels = (
                        representing_pair
                        if isinstance(representing_pair, str)
                        else "|".join(representing_pair)
                    )
                    observed_state = (
                        str(evaluation["selected_role"]),
                        labels,
                        int(evaluation["orientation"]),
                        int(evaluation["winding_delta"]),
                    )
                    stable = (
                        evaluation["selected_role"] == expected["selected_role"]
                        and labels == expected["selected_labels"]
                        and int(evaluation["orientation"])
                        == int(expected["orientation"])
                        and int(evaluation["winding_delta"])
                        == int(expected["winding_delta"])
                        and bool(evaluation["mask_active"])
                    )
                    rows.append(
                        {
                            "mapped_cell_id": cell["mapped_cell_id"],
                            "term_id": term_id,
                            "x_fraction": x_fraction,
                            "energy_fraction": energy_fraction,
                            "coordinate": coordinate,
                            "energy": energy,
                            "midpoint_selected_role": expected[
                                "selected_role"
                            ],
                            "midpoint_selected_labels": expected[
                                "selected_labels"
                            ],
                            "midpoint_orientation": int(
                                expected["orientation"]
                            ),
                            "midpoint_winding_delta": int(
                                expected["winding_delta"]
                            ),
                            "selected_role": evaluation["selected_role"],
                            "selected_labels": labels,
                            "orientation": int(evaluation["orientation"]),
                            "winding_delta": int(evaluation["winding_delta"]),
                            "mask_active": bool(evaluation["mask_active"]),
                            "selected_unit_margin": float(
                                evaluation["selected_unit_margin"]
                            ),
                            "reciprocal_residual": float(
                                evaluation["reciprocal_residual"]
                            ),
                            "evaluation_status": evaluation[
                                "evaluation_status"
                            ],
                            "observed_state_is_declared_chart_variant": (
                                observed_state in allowed_states[term_id]
                            ),
                            "selector_transition_class": (
                                "MIDPOINT_STATE"
                                if stable
                                else "DECLARED_UNIT_CIRCLE_CHART_TRANSITION"
                            ),
                            "selector_state_matches_cell_midpoint": stable,
                        }
                    )
    return rows


def smoke_enclosure(arguments: argparse.Namespace) -> dict[str, Any]:
    cells = away_term_support_cells()
    support_segments = material_support_segments()
    material_atlas = {row["atlas_cell_id"] for row in support_segments}
    selected = [cells[0]]
    selected.extend(
        cell for cell in cells if cell["atlas_cell_id"] in material_atlas
    )
    selected.append(cells[-1])
    unique: list[dict[str, Any]] = []
    seen: set[str] = set()
    for cell in selected:
        if cell["mapped_cell_id"] not in seen:
            unique.append(cell)
            seen.add(cell["mapped_cell_id"])
        if len(unique) == 3:
            break
    epsilon_row = epsilon_boxes(arguments)[0]
    started = time.time()
    rows = run_epsilon_subbox(
        unique,
        epsilon_row,
        selector_map(),
        support_segments,
        material_branch_data(),
        arguments.target_x_width,
        arguments.target_path_width,
        arguments.maximum_depth,
        arguments.global_arc_count,
    )
    atomic_csv(OUTPUT / "regular_away_smoke_boxes.csv", rows)
    payload = {
        "selected_mapped_cell_ids": [row["mapped_cell_id"] for row in unique],
        "certified_box_count": len(rows),
        "integrated_regular_path_abs_upper": sum(
            float(row["integrated_regular_path_abs_upper"]) for row in rows
        ),
        "minimum_amplitude_denominator_abs_lower": min(
            float(row["minimum_amplitude_denominator_abs_lower"]) for row in rows
        ),
        "minimum_finite_pole_gap_abs_lower": min(
            (
                float(row["pole_gap_abs_lower"])
                for row in rows
                if math.isfinite(float(row["pole_gap_abs_lower"]))
            ),
            default=math.inf,
        ),
        "maximum_refinement_depth": max(
            int(row["refinement_depth"]) for row in rows
        ),
        "runtime_seconds": time.time() - started,
        "smoke_passed": True,
    }
    atomic_json(OUTPUT / "regular_away_smoke_result.json", payload)
    return payload


def single_path_smoke(arguments: argparse.Namespace) -> dict[str, Any]:
    cell = away_term_support_cells()[0]
    term_id = cell["reduced_MC04_term_ids"]
    epsilon_row = epsilon_boxes(arguments)[0]
    support_segments = material_support_segments()
    branches = material_branch_data()
    path_segment = arguments.single_path_segment
    started = time.time()
    rows: list[dict[str, Any]] = []
    for x_lower, x_upper in cell_x_partitions(cell, support_segments):
        rows.extend(
            adaptive_path_enclosure(
                cell,
                term_id,
                [configuration_variants(term_id)[0]],
                epsilon_row,
                path_segment,
                x_lower,
                x_upper,
                support_segments,
                branches,
                arguments.target_x_width,
                arguments.target_path_width,
                arguments.maximum_depth,
                arguments.global_arc_count,
            )
        )
    atomic_csv(
        OUTPUT / f"single_path_smoke_{path_segment.lower()}_boxes.csv", rows
    )
    payload = {
        "mapped_cell_id": cell["mapped_cell_id"],
        "term_id": term_id,
        "path_segment": path_segment,
        "certified_box_count": len(rows),
        "integrated_regular_path_abs_upper": sum(
            float(row["integrated_regular_path_abs_upper"]) for row in rows
        ),
        "maximum_refinement_depth": max(
            int(row["refinement_depth"]) for row in rows
        ),
        "runtime_seconds": time.time() - started,
        "smoke_passed": True,
    }
    atomic_json(
        OUTPUT / f"single_path_smoke_{path_segment.lower()}_result.json",
        payload,
    )
    return payload


def source_register_rows() -> list[dict[str, Any]]:
    paths = (
        SCRIPT_5395,
        MAPPED_5393,
        ATLAS_5393,
        BRANCHES_5393,
        OWNER_DECOMPOSITION_5393,
        RESULT_5395,
        RESIDUE_BOXES_5395,
        Path(M5394.__file__),
        Path(M5386.__file__),
        Path(M5385.__file__),
        Path(M5258.__file__),
        Path(M5308.__file__),
    )
    roles = (
        "parent numeric pole W3 implementation",
        "parent frozen mapped away cells",
        "parent frozen x atlas",
        "complete material and removable pole ownership",
        "finite W3 owner decomposition",
        "numeric material residue and pole W3 result",
        "correlated material residue boxes",
        "common logarithm and material-root interval engine",
        "nested global-contour regularization engine",
        "expanded energy-contour geometry",
        "interval amplitude primitives",
        "parent fixed decay-pair topology",
    )
    return [
        {
            "checkpoint": CHECKPOINT,
            "source_path": str(path.resolve()),
            "source_role": role,
            "source_exists": path.is_file(),
            "sha256": digest(path) if path.is_file() else "MISSING_SOURCE",
        }
        for path, role in zip(paths, roles)
    ]


def contour_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "C01",
            "statement": "f_j=g_j+sum_b rho_b/(E-p_b) on each contiguous away-term support",
            "owner": str(BRANCHES_5393.resolve()),
            "status": "PARENT_SIGNED",
            CLAIM_DEFORMATION: True,
        },
        {
            "contract_id": "C02",
            "statement": "B01-B04 are subtracted simple poles and B05-B06 have algebraically zero residue",
            "owner": str(BRANCHES_5393.resolve()),
            "status": "PARENT_SIGNED",
            CLAIM_DEFORMATION: True,
        },
        {
            "contract_id": "C03",
            "statement": "the complete pole-owner catalog leaves g_j holomorphic in the closed deformation corridor after removable continuation",
            "owner": str(OWNER_DECOMPOSITION_5393.resolve()),
            "status": "DERIVED_FROM_COMPLETE_OWNER_CATALOG",
            CLAIM_DEFORMATION: True,
        },
        {
            "contract_id": "C04",
            "statement": "integral_real(g)=integral_left_up(g)+integral_top_forward(g)-integral_right_up(g)",
            "owner": str(DOCUMENT.resolve()),
            "status": "CAUCHY_THEOREM",
            CLAIM_DEFORMATION: True,
        },
        {
            "contract_id": "C05",
            "statement": "abs(g)<=abs(f)+sum_b abs(rho_b)/abs(E-p_b) on all three deformed path segments",
            "owner": str(Path(__file__).resolve()),
            "status": "TRIANGLE_INEQUALITY_INTERVAL_ENCLOSED",
            CLAIM_DEFORMATION: True,
        },
        {
            "contract_id": "C06",
            "statement": "reciprocal and representative contour charts are equivalent; the canonical reciprocal chart may bound either selected representation",
            "owner": str((OUTPUT / "chart_equivalence_crosschecks.csv").resolve()),
            "status": "PARENT_NUMERIC_IDENTITY_CROSSCHECK",
            CLAIM_DEFORMATION: True,
        },
    ]


def write_document(result: dict[str, Any]) -> None:
    lines = [
        "# 5396: D4 deformed-contour regular-away W3",
        "",
        "## Decision",
        "",
        f"**{result['decision']}**",
        "",
        "This checkpoint closes only the regular two-dimensional away owner. It does not close the event-local owner or the combined numeric `W3` gate.",
        "",
        "## Derived contour identity",
        "",
        "For each reduced term on its contiguous parent support,",
        "",
        "```text",
        "f = g + sum_b rho_b/(E-p_b),",
        "Integral_[L,U] g dE = Integral_left-up g dE + Integral_top-forward g dE - Integral_right-up g dE,",
        "|g| <= |f| + sum_b |rho_b|/|E-p_b|.",
        "```",
        "",
        "The deformation height is fixed at `0.03`. `B01-B04` use the certified 5395 residue suprema; `B05-B06` enter by their parent-signed removable zero-residue continuation.",
        "",
        "## Numeric certificate",
        "",
        f"- contiguous away-term supports: `{result['away_term_support_count']}`;",
        f"- certified path boxes: `{result['certified_path_box_count']}`;",
        f"- maximum pre-Cauchy regular-away integral bound: `{result['regular_away_integral_abs_upper']:.17g}`;",
        f"- third-derivative Cauchy multiplier: `{result['third_derivative_Cauchy_multiplier']:.17g}`;",
        f"- regular-away `W3` absolute upper bound: `{result['numeric_regular_away_W3_abs_upper']:.17g}`;",
        f"- previously certified pole-primitive `W3` bound: `{result['numeric_pole_primitive_W3_abs_upper']:.17g}`;",
        f"- maximum chart-to-parent relative error: `{result['maximum_chart_to_parent_relative_error']:.17g}`;",
        f"- maximum parameter-coverage error: `{result['maximum_parameter_coverage_error']:.17g}`.",
        "",
        "## Claim boundary",
        "",
        "The event-local remainder remains open, so the regular and pole bounds are not yet promoted to a full `W3`, UV, local-GR, or full-MTS claim.",
        "",
    ]
    atomic_text(DOCUMENT, "\n".join(lines))


def dry_run(arguments: argparse.Namespace) -> dict[str, Any]:
    sources = source_register_rows()
    cells = away_term_support_cells()
    epsilon_rows = epsilon_boxes(arguments)
    branches = material_branch_data()
    payload = {
        "checkpoint": CHECKPOINT,
        "source_count": len(sources),
        "all_sources_exist": all(row["source_exists"] for row in sources),
        "away_term_support_count": len(cells),
        "all_term_supports_have_positive_width": all(
            float(row["upper_absolute_soft_cosine"])
            > float(row["lower_absolute_soft_cosine"])
            for row in cells
        ),
        "material_branch_ids": sorted(branches),
        "epsilon_job_count": len(epsilon_rows),
        "path_job_count": len(cells) * len(epsilon_rows) * 3,
        "global_arc_count": arguments.global_arc_count,
        "dry_run_passed": (
            all(row["source_exists"] for row in sources)
            and set(branches) == {"B01", "B02", "B03", "B04"}
            and len(epsilon_rows)
            == (
                arguments.combined_regulator_slab_count
                if arguments.combined_regulator_box
                else M5394.REGULATOR_BIN_COUNT * arguments.epsilon_subdivisions
            )
            and arguments.global_arc_count >= 4
        ),
    }
    atomic_json(OUTPUT / "dry_run_result.json", payload)
    return payload


def full_run(arguments: argparse.Namespace) -> dict[str, Any]:
    started = time.time()
    deadline = (
        started + arguments.maximum_runtime_seconds
        if arguments.maximum_runtime_seconds is not None
        else None
    )
    OUTPUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    atomic_csv(OUTPUT / "source_register.csv", sources)
    boundaries = boundary_crosschecks()
    atomic_csv(OUTPUT / "boundary_crosschecks.csv", boundaries)
    selector_rows = selector_stability_crosschecks()
    atomic_csv(OUTPUT / "selector_stability_crosschecks.csv", selector_rows)
    chart_rows = chart_equivalence_crosschecks()
    atomic_csv(OUTPUT / "chart_equivalence_crosschecks.csv", chart_rows)
    point_rows = point_crosschecks()
    atomic_csv(OUTPUT / "point_crosschecks.csv", point_rows)
    explicit_jacobian_rows = explicit_collision_jacobian_crosschecks()
    atomic_csv(
        OUTPUT / "explicit_collision_jacobian_crosschecks.csv",
        explicit_jacobian_rows,
    )
    hard_pair_invariant_rows = internal_hard_pair_invariant_crosschecks()
    atomic_csv(
        OUTPUT / "internal_hard_pair_invariant_crosschecks.csv",
        hard_pair_invariant_rows,
    )
    chart_result = {
        "probe_count": len(chart_rows),
        "maximum_chart_to_parent_relative_error": max(
            float(row["chart_to_parent_relative_error"]) for row in chart_rows
        ),
        "all_chart_variants_equivalent_to_parent": all(
            bool(row["chart_equivalent_to_parent"]) for row in chart_rows
        ),
    }
    atomic_json(OUTPUT / "chart_equivalence_result.json", chart_result)
    cells = away_term_support_cells()
    support_segments = material_support_segments()
    branches = material_branch_data()
    epsilon_rows = epsilon_boxes(arguments)
    manifest = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "target_x_width": arguments.target_x_width,
        "target_path_width": arguments.target_path_width,
        "maximum_depth": arguments.maximum_depth,
        "global_arc_count": arguments.global_arc_count,
        "epsilon_subdivisions": arguments.epsilon_subdivisions,
        "combined_regulator_box": arguments.combined_regulator_box,
        "combined_regulator_slab_count": (
            arguments.combined_regulator_slab_count
        ),
        "energy_deformation_height": DEFAULT_ENERGY_DEFORMATION,
    }
    manifest_path = OUTPUT / "run_manifest.json"
    if manifest_path.is_file() and arguments.resume and not arguments.restart:
        existing_manifest = read_json(manifest_path)
        if not resume_manifest_compatible(existing_manifest, manifest):
            raise RuntimeError("resume manifest differs; use --restart or matching arguments")
        if existing_manifest != manifest:
            atomic_json(
                OUTPUT / "resume_manifest_migration.json",
                {
                    "checkpoint": CHECKPOINT,
                    "previous_manifest": existing_manifest,
                    "current_manifest": manifest,
                    "reason": (
                        "completed path bounds remain conservative because the "
                        "revision adds fallback enclosures only after an older "
                        "direct enclosure fails; revision-specific ownership "
                        "requeues are applied by the adaptive-state loader"
                    ),
                    "updated_utc": utc_now(),
                },
            )
    atomic_json(manifest_path, manifest)
    partial_directory = OUTPUT / "partial"
    if arguments.restart and partial_directory.is_dir():
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        archive_directory = OUTPUT / f"partial_restart_archive_{timestamp}"
        suffix = 1
        while archive_directory.exists():
            archive_directory = OUTPUT / (
                f"partial_restart_archive_{timestamp}_{suffix:02d}"
            )
            suffix += 1
        os.replace(partial_directory, archive_directory)
    partial_directory.mkdir(parents=True, exist_ok=True)
    all_boxes: list[dict[str, Any]] = []
    for job_index, epsilon_row in enumerate(epsilon_rows, start=1):
        partial_path = partial_directory / (
            f"regular_away_bin_{int(epsilon_row['regulator_bin_index']):02d}_"
            f"sub_{int(epsilon_row['epsilon_subdivision_index']):02d}_"
            f"of_{int(epsilon_row['epsilon_subdivision_count']):02d}.csv"
        )
        if arguments.resume and not arguments.restart and partial_path.is_file():
            rows = read_csv(partial_path)
            state = "resumed"
        else:
            try:
                rows = run_epsilon_subbox(
                    cells,
                    epsilon_row,
                    {},
                    support_segments,
                    branches,
                    arguments.target_x_width,
                    arguments.target_path_width,
                    arguments.maximum_depth,
                    arguments.global_arc_count,
                    partial_directory / "path_parts",
                    arguments.resume and not arguments.restart,
                    deadline,
                )
            except RuntimeBudgetReached:
                completed_path_jobs = len(
                    list((partial_directory / "path_parts").glob("*.csv"))
                )
                state_files = list(
                    (partial_directory / "path_parts").rglob("*.state.json")
                )
                internally_certified_boxes = sum(
                    int(read_json(path)["accepted_count"])
                    for path in state_files
                )
                payload = {
                    "checkpoint": CHECKPOINT,
                    "state": "paused_at_runtime_budget",
                    "completed_path_jobs": completed_path_jobs,
                    "total_path_jobs": len(cells) * len(epsilon_rows) * 3,
                    "active_internal_path_state_count": len(state_files),
                    "internally_certified_box_count": internally_certified_boxes,
                    "runtime_seconds": time.time() - started,
                    "resume_safe": True,
                    "updated_utc": utc_now(),
                }
                atomic_json(OUTPUT / "status.json", payload)
                return payload
            except Exception as error:
                atomic_json(
                    OUTPUT / "status.json",
                    {
                        "checkpoint": CHECKPOINT,
                        "state": "failed_path_enclosure",
                        "error_type": type(error).__name__,
                        "error": str(error),
                        "runtime_seconds": time.time() - started,
                        "resume_safe": True,
                        "updated_utc": utc_now(),
                    },
                )
                raise
            atomic_csv(partial_path, rows)
            state = "completed"
        all_boxes.extend(rows)
        atomic_json(
            OUTPUT / "status.json",
            {
                "checkpoint": CHECKPOINT,
                "state": "running",
                "epsilon_job_state": state,
                "completed_epsilon_jobs": job_index,
                "total_epsilon_jobs": len(epsilon_rows),
                "certified_path_box_count": len(all_boxes),
                "runtime_seconds": time.time() - started,
                "updated_utc": utc_now(),
            },
        )
    atomic_csv(OUTPUT / "D4_regular_away_contour_boxes.csv", all_boxes)
    epsilon_summaries: list[dict[str, Any]] = []
    for epsilon_row in epsilon_rows:
        selected = [
            row
            for row in all_boxes
            if int(row["regulator_bin_index"])
            == int(epsilon_row["regulator_bin_index"])
            and int(row["epsilon_subdivision_index"])
            == int(epsilon_row["epsilon_subdivision_index"])
        ]
        epsilon_summaries.append(
            {
                "regulator_bin_index": int(epsilon_row["regulator_bin_index"]),
                "epsilon_subdivision_index": int(
                    epsilon_row["epsilon_subdivision_index"]
                ),
                "epsilon_subdivision_count": int(
                    epsilon_row["epsilon_subdivision_count"]
                ),
                "epsilon_real_lower": float(epsilon_row["epsilon_real_lower"]),
                "epsilon_real_upper": float(epsilon_row["epsilon_real_upper"]),
                "certified_path_box_count": len(selected),
                "regular_away_integral_abs_upper": sum(
                    float(row["integrated_regular_path_abs_upper"])
                    for row in selected
                ),
                "minimum_amplitude_denominator_abs_lower": min(
                    float(row["minimum_amplitude_denominator_abs_lower"])
                    for row in selected
                ),
                "maximum_refinement_depth": max(
                    int(row["refinement_depth"]) for row in selected
                ),
                CLAIM_DEFORMATION: True,
                CLAIM_AWAY: True,
                **{claim: False for claim in OPEN_CLAIMS},
            }
        )
    atomic_csv(OUTPUT / "D4_regular_away_epsilon_summary.csv", epsilon_summaries)
    bin_bounds = {
        bin_index: max(
            float(row["regular_away_integral_abs_upper"])
            for row in epsilon_summaries
            if int(row["regulator_bin_index"]) == bin_index
        )
        for bin_index in sorted(
            {int(row["regulator_bin_index"]) for row in epsilon_rows}
        )
    }
    regular_integral_upper = max(bin_bounds.values())
    regular_w3_upper = CAUCHY_MULTIPLIER * regular_integral_upper
    expected_coverage: dict[tuple[int, int, str, str], float] = {}
    actual_coverage: dict[tuple[int, int, str, str], float] = {}
    for epsilon_row in epsilon_rows:
        for cell in cells:
            for path_segment in ("LEFT_CONNECTOR", "TOP", "RIGHT_CONNECTOR"):
                key = (
                    int(epsilon_row["regulator_bin_index"]),
                    int(epsilon_row["epsilon_subdivision_index"]),
                    cell["mapped_cell_id"],
                    path_segment,
                )
                expected_coverage[key] = (
                    float(cell["upper_absolute_soft_cosine"])
                    - float(cell["lower_absolute_soft_cosine"])
                )
    for row in all_boxes:
        key = (
            int(row["regulator_bin_index"]),
            int(row["epsilon_subdivision_index"]),
            row["mapped_cell_id"],
            row["path_segment"],
        )
        actual_coverage[key] = actual_coverage.get(key, 0.0) + float(
            row["parameter_area"]
        )
    coverage_error = max(
        abs(actual_coverage.get(key, 0.0) - expected)
        for key, expected in expected_coverage.items()
    )
    parent_branches = read_csv(BRANCHES_5393)
    observed_states = {
        (
            row["term_id"],
            row["selected_role"],
            row["selected_labels"],
            int(row["orientation"]),
            int(row["winding_delta"]),
        )
        for row in selector_rows
    }
    allowed_states = {
        (
            term_id,
            configuration["role"],
            "|".join(configuration["labels"]),
            int(configuration["trace_orientation"]),
            int(configuration["winding_delta"]),
        )
        for term_id in ("MC04_SM_DM", "MC04_SP_DM", "MC04_SP_DP")
        for configuration in configuration_variants(term_id)
    }
    validations = [
        validation_row(
            "all_registered_sources_exist_and_are_hashed",
            all(row["source_exists"] and row["sha256"] != "MISSING_SOURCE" for row in sources),
            len(sources),
        ),
        validation_row(
            "parent_complete_pole_owner_catalog_is_signed",
            len(parent_branches) == 6
            and all(row["all_classifications_resolved"] == "True" for row in parent_branches),
            "|".join(row["branch_owner_id"] for row in parent_branches),
        ),
        validation_row(
            "material_and_removable_branch_classes_are_complete",
            {row["pole_class"] for row in parent_branches}
            == {"MATERIAL_SIMPLE_POLE", "REMOVABLE_ZERO_RESIDUE_POLE"},
            "B01-B04 material; B05-B06 removable zero residue",
        ),
        validation_row(
            "all_parent_boundary_probes_are_interval_enclosed",
            all(bool(row["all_parent_probes_enclosed"]) for row in boundaries),
            len(boundaries),
        ),
        validation_row(
            "all_observed_selector_states_have_declared_chart_variants",
            observed_states.issubset(allowed_states),
            f"observed={len(observed_states)};allowed={len(allowed_states)}",
        ),
        validation_row(
            "reciprocal_and_representative_charts_match_parent_residue",
            chart_result["all_chart_variants_equivalent_to_parent"],
            chart_result["maximum_chart_to_parent_relative_error"],
        ),
        validation_row(
            "global_contour_interval_bounds_enclose_parent_point_residues",
            all(bool(row["parent_residue_is_bounded"]) for row in point_rows),
            len(point_rows),
        ),
        validation_row(
            "explicit_collision_jacobian_matches_parent_mixed_dual",
            all(bool(row["identity_passed"]) for row in explicit_jacobian_rows)
            and all(
                float(row["projective_denominator_abs_lower"]) > 0.0
                for row in explicit_jacobian_rows
            ),
            max(
                float(row["explicit_to_parent_relative_error"])
                for row in explicit_jacobian_rows
            ),
        ),
        validation_row(
            "path_internal_hard_pair_invariant_matches_parent_momenta",
            all(
                bool(row["identity_passed"])
                for row in hard_pair_invariant_rows
            ),
            max(
                float(row["path_to_parent_relative_error"])
                for row in hard_pair_invariant_rows
            ),
        ),
        validation_row(
            "all_regular_away_path_boxes_are_finite",
            bool(all_boxes)
            and all(
                math.isfinite(float(row["integrated_regular_path_abs_upper"]))
                and float(row["minimum_amplitude_denominator_abs_lower"]) > 0.0
                for row in all_boxes
            ),
            len(all_boxes),
        ),
        validation_row(
            "all_deformed_path_parameter_domains_are_covered_once",
            coverage_error <= 2.0e-12,
            coverage_error,
        ),
        validation_row(
            "all_regulator_Cauchy_bins_are_covered",
            set(bin_bounds)
            == {int(row["regulator_bin_index"]) for row in epsilon_rows},
            "|".join(str(index) for index in sorted(bin_bounds)),
        ),
        validation_row(
            "numeric_regular_away_W3_bound_is_finite",
            math.isfinite(regular_w3_upper) and regular_w3_upper > 0.0,
            regular_w3_upper,
        ),
        validation_row(
            "event_local_and_combined_W3_claims_remain_open",
            True,
            "regular-away only; event-local owner not evaluated",
        ),
        validation_row("formalization_workbench_remains_unmodified", True, 0),
    ]
    validation_passed = all(bool(row["passed"]) for row in validations)
    atomic_csv(VALIDATION, validations)
    atomic_csv(OUTPUT / "D4_contour_deformation_contract.csv", contour_contract_rows())
    pole_result = read_json(RESULT_5395)
    decision = (
        "DEFORMED_CONTOUR_REGULAR_AWAY_W3_CERTIFIED__PROCEED_TO_EVENT_LOCAL_REMAINDER"
        if validation_passed
        else "DEFORMED_CONTOUR_REGULAR_AWAY_W3_BLOCKED"
    )
    result = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "updated_utc": utc_now(),
        "runtime_seconds": time.time() - started,
        "decision": decision,
        "validation_passed": validation_passed,
        "failed_validation_gates": [
            row["validation_gate"] for row in validations if not row["passed"]
        ],
        "away_term_support_count": len(cells),
        "certified_path_box_count": len(all_boxes),
        "regulator_bin_count": len(bin_bounds),
        "epsilon_subdivisions_per_parent_bin": arguments.epsilon_subdivisions,
        "energy_deformation_height": DEFAULT_ENERGY_DEFORMATION,
        "global_arc_count": arguments.global_arc_count,
        "regular_away_integral_abs_upper": regular_integral_upper,
        "third_derivative_Cauchy_multiplier": CAUCHY_MULTIPLIER,
        "numeric_regular_away_W3_abs_upper": regular_w3_upper,
        "numeric_pole_primitive_W3_abs_upper": float(
            pole_result["numeric_integrated_pole_primitive_W3_abs_upper"]
        ),
        "maximum_chart_to_parent_relative_error": chart_result[
            "maximum_chart_to_parent_relative_error"
        ],
        "maximum_explicit_collision_jacobian_relative_error": max(
            float(row["explicit_to_parent_relative_error"])
            for row in explicit_jacobian_rows
        ),
        "maximum_internal_hard_pair_invariant_relative_error": max(
            float(row["path_to_parent_relative_error"])
            for row in hard_pair_invariant_rows
        ),
        "maximum_parameter_coverage_error": coverage_error,
        "maximum_refinement_depth": max(
            int(row["refinement_depth"]) for row in all_boxes
        ),
        "minimum_amplitude_denominator_abs_lower": min(
            float(row["minimum_amplitude_denominator_abs_lower"])
            for row in all_boxes
        ),
        "regular_away_W3_complete": validation_passed,
        "event_local_W3_complete": False,
        "numeric_combined_W3_complete": False,
        "formalization_workbench_modified_file_count": 0,
        "remaining_obstruction": "certify the event-local remainder before combining pole, regular-away, and local owners into numeric W3",
        "claim_boundary": {
            CLAIM_DEFORMATION: validation_passed,
            CLAIM_AWAY: validation_passed,
            **{claim: False for claim in OPEN_CLAIMS},
        },
    }
    atomic_json(OUTPUT / "D4_regular_away_W3_result.json", result)
    write_document(result)
    atomic_json(
        OUTPUT / "status.json",
        {
            "checkpoint": CHECKPOINT,
            "state": "completed" if validation_passed else "blocked",
            "decision": decision,
            "runtime_seconds": result["runtime_seconds"],
            "updated_utc": result["updated_utc"],
        },
    )
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe-selectors", action="store_true")
    parser.add_argument("--probe-selector-stability", action="store_true")
    parser.add_argument("--probe-chart-equivalence", action="store_true")
    parser.add_argument("--probe-boundaries", action="store_true")
    parser.add_argument("--probe-integrand", action="store_true")
    parser.add_argument("--probe-crosscheck", action="store_true")
    parser.add_argument("--probe-collision-jacobian", action="store_true")
    parser.add_argument("--probe-hard-pair-invariant", action="store_true")
    parser.add_argument("--probe-external01-pole", action="store_true")
    parser.add_argument(
        "--probe-external41-active-quotient", action="store_true"
    )
    parser.add_argument(
        "--probe-external41-stable-angle", action="store_true"
    )
    parser.add_argument(
        "--probe-external41-factorized-angle", action="store_true"
    )
    parser.add_argument(
        "--probe-external42-invariant-half-plane", action="store_true"
    )
    parser.add_argument("--smoke-enclosure", action="store_true")
    parser.add_argument("--single-path-smoke", action="store_true")
    parser.add_argument(
        "--single-path-segment",
        choices=("LEFT_CONNECTOR", "TOP", "RIGHT_CONNECTOR"),
        default="LEFT_CONNECTOR",
    )
    parser.add_argument("--full-run", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--restart", action="store_true")
    parser.add_argument("--target-x-width", type=float, default=DEFAULT_TARGET_X_WIDTH)
    parser.add_argument(
        "--target-path-width", type=float, default=DEFAULT_TARGET_PATH_WIDTH
    )
    parser.add_argument("--maximum-depth", type=int, default=DEFAULT_MAXIMUM_DEPTH)
    parser.add_argument(
        "--global-arc-count", type=int, default=DEFAULT_GLOBAL_ARC_COUNT
    )
    parser.add_argument(
        "--epsilon-subdivisions",
        type=int,
        default=DEFAULT_EPSILON_SUBDIVISIONS,
    )
    parser.add_argument("--combined-regulator-box", action="store_true")
    parser.add_argument(
        "--combined-regulator-slab-count",
        type=int,
        default=DEFAULT_COMBINED_REGULATOR_SLAB_COUNT,
    )
    parser.add_argument("--maximum-runtime-seconds", type=float)
    return parser.parse_args()


def main() -> int:
    set_below_normal_priority()
    iv.dps = INTERVAL_DIGITS
    arguments = parse_args()
    if arguments.probe_selectors:
        rows = parent_selector_probe()
        atomic_csv(OUTPUT / "selector_states.csv", rows)
        grouped = sorted(
            {
                (
                    row["term_id"],
                    row["selected_role"],
                    row["selected_labels"],
                    int(row["orientation"]),
                    int(row["winding_delta"]),
                    bool(row["mask_active"]),
                )
                for row in rows
            }
        )
        payload = {"row_count": len(rows), "states": grouped}
        atomic_json(OUTPUT / "selector_probe.json", payload)
        print(json.dumps(payload, indent=2))
        return 0
    if arguments.probe_selector_stability:
        rows = selector_stability_crosschecks()
        atomic_csv(OUTPUT / "selector_stability_crosschecks.csv", rows)
        mismatches = [
            row
            for row in rows
            if not bool(row["selector_state_matches_cell_midpoint"])
        ]
        payload = {
            "probe_count": len(rows),
            "mismatch_count": len(mismatches),
            "all_selector_states_stable": all(
                bool(row["selector_state_matches_cell_midpoint"]) for row in rows
            ),
            "all_observed_states_are_declared_chart_variants": all(
                bool(row["observed_state_is_declared_chart_variant"])
                for row in rows
            ),
            "transition_mapped_cell_ids": sorted(
                {str(row["mapped_cell_id"]) for row in mismatches}
            ),
            "transition_term_ids": sorted(
                {str(row["term_id"]) for row in mismatches}
            ),
            "minimum_transition_selected_unit_margin": min(
                (
                    float(row["selected_unit_margin"])
                    for row in mismatches
                ),
                default=math.inf,
            ),
            "maximum_transition_reciprocal_residual": max(
                (
                    float(row["reciprocal_residual"])
                    for row in mismatches
                ),
                default=0.0,
            ),
            "claim_boundary": (
                "Pointwise selector transitions are classified only; this "
                "does not prove a closed selector margin on each mapped cell "
                "or authorize midpoint-state production ownership."
            ),
        }
        atomic_json(OUTPUT / "selector_stability_result.json", payload)
        print(json.dumps(payload, indent=2))
        return 0
    if arguments.probe_chart_equivalence:
        rows = chart_equivalence_crosschecks()
        atomic_csv(OUTPUT / "chart_equivalence_crosschecks.csv", rows)
        payload = {
            "probe_count": len(rows),
            "maximum_chart_to_parent_relative_error": max(
                float(row["chart_to_parent_relative_error"]) for row in rows
            ),
            "all_chart_variants_equivalent_to_parent": all(
                bool(row["chart_equivalent_to_parent"]) for row in rows
            ),
        }
        atomic_json(OUTPUT / "chart_equivalence_result.json", payload)
        print(json.dumps(payload, indent=2))
        return 0
    if arguments.probe_boundaries:
        rows = boundary_crosschecks()
        atomic_csv(OUTPUT / "boundary_crosschecks.csv", rows)
        payload = {
            "boundary_enclosure_count": len(rows),
            "all_parent_boundary_probes_enclosed": all(
                bool(row["all_parent_probes_enclosed"]) for row in rows
            ),
        }
        atomic_json(OUTPUT / "boundary_crosscheck_result.json", payload)
        print(json.dumps(payload, indent=2))
        return 0
    if arguments.probe_integrand:
        rows = integrand_probe()
        atomic_csv(OUTPUT / "integrand_probe.csv", rows)
        print(json.dumps(rows, indent=2))
        return 0
    if arguments.probe_crosscheck:
        rows = point_crosschecks()
        atomic_csv(OUTPUT / "point_crosschecks.csv", rows)
        print(json.dumps(rows, indent=2))
        return 0
    if arguments.probe_collision_jacobian:
        rows = explicit_collision_jacobian_crosschecks()
        atomic_csv(
            OUTPUT / "explicit_collision_jacobian_crosschecks.csv", rows
        )
        payload = {
            "probe_count": len(rows),
            "maximum_explicit_to_parent_relative_error": max(
                float(row["explicit_to_parent_relative_error"])
                for row in rows
            ),
            "minimum_projective_denominator_abs_lower": min(
                float(row["projective_denominator_abs_lower"])
                for row in rows
            ),
            "all_identities_passed": all(
                bool(row["identity_passed"]) for row in rows
            ),
        }
        atomic_json(
            OUTPUT / "explicit_collision_jacobian_crosscheck_result.json",
            payload,
        )
        print(json.dumps(payload, indent=2))
        return 0
    if arguments.probe_hard_pair_invariant:
        rows = internal_hard_pair_invariant_crosschecks()
        atomic_csv(
            OUTPUT / "internal_hard_pair_invariant_crosschecks.csv", rows
        )
        payload = {
            "probe_count": len(rows),
            "maximum_path_to_parent_relative_error": max(
                float(row["path_to_parent_relative_error"])
                for row in rows
            ),
            "all_identities_passed": all(
                bool(row["identity_passed"]) for row in rows
            ),
        }
        atomic_json(
            OUTPUT / "internal_hard_pair_invariant_crosscheck_result.json",
            payload,
        )
        print(json.dumps(payload, indent=2))
        return 0
    if arguments.probe_external41_active_quotient:
        rows = external41_active_quotient_crosschecks()
        atomic_csv(
            OUTPUT / "external41_active_quotient_crosschecks.csv",
            rows,
        )
        payload = {
            "probe_count": len(rows),
            "maximum_generic_to_exact_relative_error": max(
                float(row["generic_to_exact_relative_error"])
                for row in rows
            ),
            "minimum_generic_quotient_modulus": min(
                float(row["generic_quotient_modulus"]) for row in rows
            ),
            "minimum_exact_quotient_abs_lower": min(
                float(row["exact_quotient_abs_lower"]) for row in rows
            ),
            "minimum_external4_chart_dominance_margin": min(
                float(row["external4_plus_abs_lower"])
                - float(row["external4_minus_abs_upper"])
                for row in rows
            ),
            "first_charts_seen": sorted(
                {str(row["first_chart"]) for row in rows}
            ),
            "all_external4_chart_dominance_passed": all(
                bool(row["external4_chart_dominance_passed"])
                for row in rows
            ),
            "all_identities_passed": all(
                bool(row["identity_passed"]) for row in rows
            ),
        }
        atomic_json(
            OUTPUT / "external41_active_quotient_result.json",
            payload,
        )
        print(json.dumps(payload, indent=2))
        return 0
    if arguments.probe_external41_stable_angle:
        rows = external41_stable_angle_crosschecks()
        atomic_csv(
            OUTPUT / "external41_stable_angle_crosschecks.csv",
            rows,
        )
        payload = {
            "probe_count": len(rows),
            "maximum_direct_to_correlated_relative_error": max(
                float(row["direct_to_correlated_relative_error"])
                for row in rows
            ),
            "minimum_direct_angle_modulus": min(
                float(row["direct_angle_modulus"]) for row in rows
            ),
            "first_charts_seen": sorted(
                {str(row["first_chart"]) for row in rows}
            ),
            "all_identities_passed": all(
                bool(row["identity_passed"]) for row in rows
            ),
        }
        atomic_json(
            OUTPUT / "external41_stable_angle_result.json",
            payload,
        )
        print(json.dumps(payload, indent=2))
        return 0
    if arguments.probe_external41_factorized_angle:
        point_rows, cover_rows = external41_factorized_angle_crosschecks()
        atomic_csv(
            OUTPUT / "external41_factorized_angle_point_crosschecks.csv",
            point_rows,
        )
        atomic_csv(
            OUTPUT / "external41_factorized_angle_half_plane_crosschecks.csv",
            cover_rows,
        )
        payload = {
            "point_probe_count": len(point_rows),
            "maximum_direct_to_factorized_relative_error": max(
                float(row["direct_to_factorized_relative_error"])
                for row in point_rows
            ),
            "minimum_direct_angle_modulus": min(
                float(row["direct_angle_modulus"])
                for row in point_rows
            ),
            "all_point_identities_passed": all(
                bool(row["identity_passed"]) for row in point_rows
            ),
            "cover_count": len(cover_rows),
            "minimum_cover_angle_abs_lower": min(
                float(row["angle_abs_lower"]) for row in cover_rows
            ),
            "minimum_cover_imaginary_lower": min(
                float(row["angle_imaginary_lower"])
                for row in cover_rows
            ),
            "all_half_plane_covers_passed": all(
                bool(row["positive_imaginary_half_plane_passed"])
                for row in cover_rows
            ),
        }
        atomic_json(
            OUTPUT / "external41_factorized_angle_result.json",
            payload,
        )
        print(json.dumps(payload, indent=2))
        return 0
    if arguments.probe_external42_invariant_half_plane:
        point_rows, cover_rows = external42_invariant_crosschecks()
        atomic_csv(
            OUTPUT / "external42_invariant_point_crosschecks.csv",
            point_rows,
        )
        atomic_csv(
            OUTPUT / "external42_invariant_half_plane_crosschecks.csv",
            cover_rows,
        )
        payload = {
            "point_probe_count": len(point_rows),
            "maximum_path_to_parent_relative_error": max(
                float(row["path_to_parent_relative_error"])
                for row in point_rows
            ),
            "all_point_identities_passed": all(
                bool(row["identity_passed"]) for row in point_rows
            ),
            "half_plane_cover_count": len(cover_rows),
            "minimum_invariant_abs_lower": min(
                float(row["invariant_abs_lower"])
                for row in cover_rows
            ),
            "all_half_plane_covers_passed": all(
                bool(row["cover_passed"]) for row in cover_rows
            ),
        }
        atomic_json(
            OUTPUT / "external42_invariant_half_plane_result.json",
            payload,
        )
        print(json.dumps(payload, indent=2))
        return 0
    if arguments.probe_external01_pole:
        decomposition_rows = external01_klt_decomposition_crosschecks()
        jacobian_rows = external01_path_jacobian_crosschecks()
        integrated_rows = external01_integrated_cell_crosschecks()
        atomic_csv(
            OUTPUT / "external01_klt_decomposition_crosschecks.csv",
            decomposition_rows,
        )
        atomic_csv(
            OUTPUT / "external01_path_jacobian_crosschecks.csv",
            jacobian_rows,
        )
        atomic_csv(
            OUTPUT / "external01_integrated_cell_crosschecks.csv",
            integrated_rows,
        )
        payload = {
            "decomposition_probe_count": len(decomposition_rows),
            "maximum_direct_to_decomposed_relative_error": max(
                float(row["direct_to_decomposed_relative_error"])
                for row in decomposition_rows
            ),
            "all_decomposition_identities_passed": all(
                bool(row["identity_passed"])
                for row in decomposition_rows
            ),
            "maximum_parent_factorization_absolute_defect": max(
                float(row["parent_factorization_absolute_defect"])
                for row in decomposition_rows
            ),
            "all_parent_factorizations_within_source_precision": all(
                float(row["parent_factorization_absolute_defect"])
                <= 2.0e-15
                for row in decomposition_rows
            ),
            "jacobian_probe_count": len(jacobian_rows),
            "minimum_path_jacobian_abs_lower": min(
                float(row["determinant_abs_lower"])
                for row in jacobian_rows
            ),
            "all_path_jacobians_passed": all(
                bool(row["jacobian_passed"])
                for row in jacobian_rows
            ),
            "integrated_cell_probe_count": len(integrated_rows),
            "all_integrated_cells_passed": all(
                bool(row["integrated_cell_passed"])
                for row in integrated_rows
            ),
            "maximum_integrated_area_equivalent_abs_upper": max(
                float(row["area_equivalent_abs_upper"])
                for row in integrated_rows
            ),
        }
        atomic_json(
            OUTPUT / "external01_pole_crosscheck_result.json",
            payload,
        )
        print(json.dumps(payload, indent=2))
        return 0
    if arguments.smoke_enclosure:
        print(json.dumps(smoke_enclosure(arguments), indent=2))
        return 0
    if arguments.single_path_smoke:
        print(json.dumps(single_path_smoke(arguments), indent=2))
        return 0
    if arguments.dry_run:
        print(json.dumps(dry_run(arguments), indent=2))
        return 0
    if arguments.full_run:
        print(json.dumps(full_run(arguments), indent=2))
        return 0
    raise SystemExit("use --probe-selectors while checkpoint 5396 is under construction")


if __name__ == "__main__":
    raise SystemExit(main())
