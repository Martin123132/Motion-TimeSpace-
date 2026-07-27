from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path


RUN_STARTED = datetime.now(timezone.utc)
RUN_STARTED_TS = RUN_STARTED.timestamp()

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3193_INPUTS.csv"
INTERFACE_CONDITIONS = OUT / "P8_Y5_R2FR_3193_INTERFACE_CONDITION_DERIVATION.csv"
NO_GO = OUT / "P8_Y5_R2FR_3193_EXTERIOR_NATURAL_MATCH_NO_GO.csv"
BOUNDARY_SCAN = OUT / "P8_Y5_R2FR_3193_BOUNDARY_MOMENTUM_RESIDUAL_SCAN.csv"
BOUNDARY_SELECTION = OUT / "P8_Y5_R2FR_3193_BOUNDARY_MOMENTUM_SELECTION.csv"
BOUNDARY_LAYER = OUT / "P8_Y5_R2FR_3193_REQUIRED_BOUNDARY_LAYER_COUNTERMOMENTA.csv"
DECISION = OUT / "P8_Y5_R2FR_3193_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3193_VALIDATION.csv"

SCAN_3192 = OUT / "P8_Y5_R2FR_3192_EL_STATIONARY_TRANSITION_SCAN.csv"
SELECTION_3192 = OUT / "P8_Y5_R2FR_3192_EL_STATIONARY_SELECTION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def resolve(base: str, relative: str) -> Path:
    if base == "post_checkpoint":
        return ROOT / relative
    if base == "formalization":
        return FW / relative
    raise ValueError(base)


def solve_linear_4(matrix: list[list[float]], vector: list[float]) -> list[float]:
    rows = [row[:] + [value] for row, value in zip(matrix, vector)]
    size = 4
    for pivot_index in range(size):
        pivot_row = max(range(pivot_index, size), key=lambda row_index: abs(rows[row_index][pivot_index]))
        rows[pivot_index], rows[pivot_row] = rows[pivot_row], rows[pivot_index]
        pivot = rows[pivot_index][pivot_index]
        if abs(pivot) < 1.0e-14:
            raise ValueError("singular stationary transition system")
        for column in range(pivot_index, size + 1):
            rows[pivot_index][column] /= pivot
        for row_index in range(size):
            if row_index == pivot_index:
                continue
            factor = rows[row_index][pivot_index]
            for column in range(pivot_index, size + 1):
                rows[row_index][column] -= factor * rows[pivot_index][column]
    return [rows[index][size] for index in range(size)]


def stationary_coefficients(width: float) -> tuple[float, float, float, float]:
    left = 1.0 - width
    right = 1.0 + width
    matrix = [
        [1.0, left**2, left**-1, left**-3],
        [0.0, 2.0 * left, -left**-2, -3.0 * left**-4],
        [1.0, right**2, right**-1, right**-3],
        [0.0, 2.0 * right, -right**-2, -3.0 * right**-4],
    ]
    vector = [left**2, 2.0 * left, right**-3, -3.0 * right**-4]
    constant, quadratic, inverse, inverse_cubed = solve_linear_4(matrix, vector)
    return constant, quadratic, inverse, inverse_cubed


def transition_u(constant: float, quadratic: float, x_value: float) -> float:
    return 6.0 * quadratic * x_value**4 + 1.2 * constant * x_value**2


def transition_u_prime(constant: float, quadratic: float, x_value: float) -> float:
    return 24.0 * quadratic * x_value**3 + 2.4 * constant * x_value


def pi_1_from_u(u_value: float) -> float:
    return 0.8 * u_value


def pi_0_from_u(x_value: float, u_value: float, u_prime_value: float) -> float:
    return 4.0 * u_value / x_value - 0.8 * u_prime_value


def core_u(x_value: float) -> float:
    return 6.0 * x_value**4


def core_u_prime(x_value: float) -> float:
    return 24.0 * x_value**3


def transition_primitive(constant: float, quadratic: float, x_value: float) -> float:
    return 0.4 * constant * x_value**3 + 1.2 * quadratic * x_value**5


def transition_abs_integral(constant: float, quadratic: float, left: float, right: float) -> float:
    points = [left, right]
    if abs(quadratic) > 1.0e-300:
        root_square = -0.2 * constant / quadratic
        if root_square > 0.0:
            root = math.sqrt(root_square)
            if left < root < right:
                points.append(root)
    points = sorted(points)
    total = 0.0
    for start, end in zip(points, points[1:]):
        midpoint = 0.5 * (start + end)
        value = 1.2 * constant * midpoint**2 + 6.0 * quadratic * midpoint**4
        sign = 1.0 if value >= 0.0 else -1.0
        total += sign * (
            transition_primitive(constant, quadratic, end)
            - transition_primitive(constant, quadratic, start)
        )
    return total


def n4_for_transition(width: float, constant: float, quadratic: float) -> float:
    left = 1.0 - width
    right = 1.0 + width
    core_signed = 6.0 * left**5 / 5.0
    return abs(core_signed) + transition_abs_integral(constant, quadratic, left, right)


def boundary_data(width: float) -> dict[str, float]:
    left = 1.0 - width
    right = 1.0 + width
    constant, quadratic, inverse, inverse_cubed = stationary_coefficients(width)
    u_left = transition_u(constant, quadratic, left)
    up_left = transition_u_prime(constant, quadratic, left)
    u_right = transition_u(constant, quadratic, right)
    up_right = transition_u_prime(constant, quadratic, right)
    pi1_left_transition = pi_1_from_u(u_left)
    pi0_left_transition = pi_0_from_u(left, u_left, up_left)
    pi1_left_core = pi_1_from_u(core_u(left))
    pi0_left_core = pi_0_from_u(left, core_u(left), core_u_prime(left))
    pi1_right_transition = pi_1_from_u(u_right)
    pi0_right_transition = pi_0_from_u(right, u_right, up_right)
    pi1_right_exterior = 0.0
    pi0_right_exterior = 0.0
    jump_left_pi1 = pi1_left_transition - pi1_left_core
    jump_left_pi0 = pi0_left_transition - pi0_left_core
    jump_right_pi1 = pi1_right_exterior - pi1_right_transition
    jump_right_pi0 = pi0_right_exterior - pi0_right_transition
    norm = math.sqrt(jump_left_pi1**2 + jump_left_pi0**2 + jump_right_pi1**2 + jump_right_pi0**2)
    return {
        "width": width,
        "left_join": left,
        "right_join": right,
        "A_constant": constant,
        "B_quadratic": quadratic,
        "C_inverse": inverse,
        "D_inverse_cubed": inverse_cubed,
        "N4_D2": n4_for_transition(width, constant, quadratic),
        "left_jump_Pi1": jump_left_pi1,
        "left_jump_Pi0": jump_left_pi0,
        "right_jump_Pi1": jump_right_pi1,
        "right_jump_Pi0": jump_right_pi0,
        "boundary_momentum_norm": norm,
        "max_abs_boundary_momentum": max(
            abs(jump_left_pi1),
            abs(jump_left_pi0),
            abs(jump_right_pi1),
            abs(jump_right_pi0),
        ),
    }


def selected_widths_from_3192() -> dict[str, float]:
    rows = read_csv(SELECTION_3192)
    return {
        row["selection_id"]: float(row["transition_width"])
        for row in rows
    }


def input_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = [
        (
            "post_checkpoint",
            "3192-Y5-R2FR-solve-quadratic-profile-EL-or-upgrade-slip-transfer-bound-under-AX1090.md",
            "3192 exact interior EL solution and boundary gate",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3192_EL_OPERATOR_DERIVATION.csv",
            "3192 normal-mode derivation",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3192_EL_STATIONARY_SELECTION.csv",
            "3192 selected exact EL profile widths",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3192_VALIDATION.csv",
            "3192 validation evidence",
        ),
        (
            "formalization",
            "83-parent-equations-v1.md",
            "current parent equation scaffold",
        ),
    ]
    return [
        {
            "input_id": f"IN3193_{index}",
            "base": base,
            "path": str(resolve(base, relative).resolve()),
            "exists": str(resolve(base, relative).exists()).lower(),
            "role": role,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for index, (base, relative, role) in enumerate(rows)
    ]


def interface_condition_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = [
        {
            "condition_id": "IC3193_0_quadratic_density",
            "object": "action_density",
            "statement": "Use the 3191/3192 toy quadratic projected-source functional.",
            "formula": "L=x^4 Q^2, Q=D2[F]",
            "status": "CANDIDATE_PARENT_FUNCTIONAL_NOT_PARENT_SIGNED",
        },
        {
            "condition_id": "IC3193_1_boundary_u",
            "object": "boundary_variable",
            "statement": "Define the compact source momentum variable.",
            "formula": "u=x^4 Q=x^4D2[F]",
            "status": "DERIVED",
        },
        {
            "condition_id": "IC3193_2_boundary_variation",
            "object": "variation_boundary_term",
            "statement": "Varying a second-derivative functional gives boundary terms multiplying deltaF and deltaFprime.",
            "formula": "deltaJ_boundary=[Pi_1 deltaFprime + Pi_0 deltaF]",
            "status": "DERIVED",
        },
        {
            "condition_id": "IC3193_3_Pi1",
            "object": "momentum_conjugate_to_Fprime",
            "statement": "The momentum multiplying deltaFprime is proportional to u.",
            "formula": "Pi_1=dL/dF''=(4/5)u",
            "status": "DERIVED",
        },
        {
            "condition_id": "IC3193_4_Pi0",
            "object": "momentum_conjugate_to_F",
            "statement": "The momentum multiplying deltaF is dL/dFprime minus the derivative of dL/dF''.",
            "formula": "Pi_0=dL/dF' - d(Pi_1)/dx = 4u/x-(4/5)u'",
            "status": "DERIVED",
        },
        {
            "condition_id": "IC3193_5_interface_condition",
            "object": "natural_interface_matching",
            "statement": "With no localized interface action and no fixed representative boundary data, both boundary momenta must be continuous across each join.",
            "formula": "[Pi_1]=0 and [Pi_0]=0",
            "status": "INTERFACE_CONDITION_DERIVED",
        },
    ]
    return [{**row, "valid_for_claim": "false", "generated_utc": now} for row in rows]


def no_go_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = [
        {
            "proof_id": "NG3193_0_exterior_has_zero_u",
            "step": "For exterior F=x^-3, D2[F]=0 because p=-3 is a normal zero of D2.",
            "formula": "u_ext=0 and u_ext'=0",
            "implication": "Exterior natural momenta vanish.",
            "status": "PROVEN",
        },
        {
            "proof_id": "NG3193_1_transition_u",
            "step": "For exact interior EL transition F=A+B*x^2+C/x+D/x^3, only A and B contribute to D2.",
            "formula": "u_tr=6B*x^4+(6/5)A*x^2",
            "implication": "The exterior natural join at x=b depends only on A and B.",
            "status": "PROVEN",
        },
        {
            "proof_id": "NG3193_2_exterior_Pi1_zero",
            "step": "Continuity of Pi_1 at exterior join requires u_tr(b)=0.",
            "formula": "6B*b^4+(6/5)A*b^2=0",
            "implication": "A=-5B*b^2.",
            "status": "PROVEN",
        },
        {
            "proof_id": "NG3193_3_exterior_Pi0_zero",
            "step": "With u_tr(b)=0, continuity of Pi_0 requires u_tr'(b)=0.",
            "formula": "24B*b^3+(12/5)A*b=0",
            "implication": "Substituting A=-5B*b^2 gives 12B*b^3=0, so B=0 and A=0.",
            "status": "PROVEN",
        },
        {
            "proof_id": "NG3193_4_transition_collapses",
            "step": "If A=B=0, the transition is F=C/x+D/x^3. Matching exterior F and Fprime at b forces C=0 and D=1.",
            "formula": "F_tr=x^-3",
            "implication": "The transition is identical to the exterior mode.",
            "status": "PROVEN",
        },
        {
            "proof_id": "NG3193_5_core_incompatibility",
            "step": "The exterior-only transition cannot also match the finite core F=x^2 and Fprime=2x at a=1-w for any finite transition width.",
            "formula": "x^-3 != x^2 and -3x^-4 != 2x at the same positive x",
            "implication": "Pure natural matching of core -> exact EL transition -> exterior is impossible for this toy functional.",
            "status": "NO_GO_FOR_PURE_NATURAL_INTERFACE_MATCHING",
        },
    ]
    return [{**row, "valid_for_claim": "false", "generated_utc": now} for row in rows]


def boundary_scan_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = []
    selected_widths = set(round(value, 3) for value in selected_widths_from_3192().values())
    widths = sorted({round(index / 1000.0, 3) for index in range(20, 951)} | selected_widths)
    for width in widths:
        data = boundary_data(width)
        rows.append(
            {
                "scan_id": f"BM3193_w{width:.3f}",
                "profile_family": "C1_exact_interior_EL_solution",
                "transition_width": f"{width:.15e}",
                "left_join": f"{data['left_join']:.15e}",
                "right_join": f"{data['right_join']:.15e}",
                "A_constant": f"{data['A_constant']:.15e}",
                "B_quadratic": f"{data['B_quadratic']:.15e}",
                "C_inverse": f"{data['C_inverse']:.15e}",
                "D_inverse_cubed": f"{data['D_inverse_cubed']:.15e}",
                "N4_D2": f"{data['N4_D2']:.15e}",
                "left_jump_Pi1": f"{data['left_jump_Pi1']:.15e}",
                "left_jump_Pi0": f"{data['left_jump_Pi0']:.15e}",
                "right_jump_Pi1": f"{data['right_jump_Pi1']:.15e}",
                "right_jump_Pi0": f"{data['right_jump_Pi0']:.15e}",
                "boundary_momentum_norm": f"{data['boundary_momentum_norm']:.15e}",
                "max_abs_boundary_momentum": f"{data['max_abs_boundary_momentum']:.15e}",
                "natural_interface_pass": "false",
                "status": "BOUNDARY_MOMENTA_NONZERO_BOUNDARY_LAYER_REQUIRED",
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )
    return rows


def boundary_selection_rows(scan: list[dict[str, object]]) -> list[dict[str, object]]:
    now = stamp()
    widths = selected_widths_from_3192()

    def by_width(width: float) -> dict[str, object]:
        return next(row for row in scan if abs(float(row["transition_width"]) - width) < 1.0e-12)

    same_width = by_width(widths["SEL3192_0_3190_width_exact_EL_comparison"])
    balanced = by_width(widths["SEL3192_2_balanced_boundary_jump_exact_EL"])
    min_n4 = by_width(widths["SEL3192_1_min_N4_exact_EL_scan"])
    min_momentum = min(scan, key=lambda row: float(row["boundary_momentum_norm"]))
    rows = [
        ("SEL3193_0_3190_width", "3190/3192 same-width exact EL row", same_width, "REFERENCE_WIDTH_BOUNDARY_MOMENTUM_NONZERO"),
        ("SEL3193_1_balanced_Fpp_jump", "3192 balanced Fpp-jump row", balanced, "BALANCED_CURVATURE_STILL_HAS_BOUNDARY_MOMENTUM"),
        ("SEL3193_2_min_N4", "3192 minimum N4 row", min_n4, "MIN_N4_HAS_SMALLER_MOMENTUM_BUT_BAD_CORE_CURVATURE_JUMP"),
        ("SEL3193_3_min_boundary_momentum_scan", "minimum boundary momentum norm over scanned widths", min_momentum, "MINIMUM_AT_SCAN_EDGE_STILL_NONZERO"),
    ]
    return [
        {
            "selection_id": selection_id,
            "criterion": criterion,
            "transition_width": row["transition_width"],
            "N4_D2": row["N4_D2"],
            "left_jump_Pi1": row["left_jump_Pi1"],
            "left_jump_Pi0": row["left_jump_Pi0"],
            "right_jump_Pi1": row["right_jump_Pi1"],
            "right_jump_Pi0": row["right_jump_Pi0"],
            "boundary_momentum_norm": row["boundary_momentum_norm"],
            "max_abs_boundary_momentum": row["max_abs_boundary_momentum"],
            "natural_interface_pass": row["natural_interface_pass"],
            "status": status,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for selection_id, criterion, row, status in rows
    ]


def boundary_layer_rows(selection: list[dict[str, object]]) -> list[dict[str, object]]:
    now = stamp()
    rows = []
    for selected in selection:
        if selected["selection_id"] not in {
            "SEL3193_0_3190_width",
            "SEL3193_1_balanced_Fpp_jump",
            "SEL3193_3_min_boundary_momentum_scan",
        }:
            continue
        rows.append(
            {
                "layer_id": selected["selection_id"].replace("SEL3193", "BL3193"),
                "source_selection": selected["selection_id"],
                "transition_width": selected["transition_width"],
                "required_tau_left_Pi1": f"{-float(selected['left_jump_Pi1']):.15e}",
                "required_tau_left_Pi0": f"{-float(selected['left_jump_Pi0']):.15e}",
                "required_tau_right_Pi1": f"{-float(selected['right_jump_Pi1']):.15e}",
                "required_tau_right_Pi0": f"{-float(selected['right_jump_Pi0']):.15e}",
                "interpretation": "a localized boundary/interface action must vary to these counter-momenta if this exact EL branch is kept",
                "source_status": "BOUNDARY_LAYER_ACTION_NOT_PARENT_DERIVED",
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )
    return rows


def decision_rows(selection: list[dict[str, object]]) -> list[dict[str, object]]:
    now = stamp()
    same_width = next(row for row in selection if row["selection_id"] == "SEL3193_0_3190_width")
    min_momentum = next(row for row in selection if row["selection_id"] == "SEL3193_3_min_boundary_momentum_scan")
    return [
        {
            "decision_id": "DEC3193_0_interface_conditions_derived",
            "finding": "Derived natural interface conditions for the quadratic profile functional: continuity of Pi_1=(4/5)u and Pi_0=4u/x-(4/5)u'.",
            "claim_status": "INTERFACE_CONDITIONS_DERIVED_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3193_1_no_go",
            "finding": "Pure natural matching to the exterior x^-3 branch forces A=B=0 in the exact transition, collapsing it to exterior-only and making the core match impossible.",
            "claim_status": "PURE_NATURAL_INTERFACE_ROUTE_REJECTED_FOR_TOY_FUNCTIONAL",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3193_2_same_width_countermomenta",
            "finding": f"At the 3190/3192 same width, the boundary momentum norm is {same_width['boundary_momentum_norm']}; a sourced interface layer is required.",
            "claim_status": "BOUNDARY_LAYER_REQUIRED_AT_REFERENCE_WIDTH",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3193_3_minimum_countermomenta",
            "finding": f"The smallest scanned boundary momentum norm is {min_momentum['boundary_momentum_norm']} at width {min_momentum['transition_width']}, still nonzero and at the scan edge.",
            "claim_status": "WIDTH_TUNING_DOES_NOT_CLOSE_INTERFACE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3193_4_next_target",
            "finding": "3194-Y5-R2FR-source-owned-boundary-layer-action-or-modified-parent-profile-functional-under-AX1090",
            "claim_status": "NEXT_TARGET",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def formalization_recent_file_count() -> int:
    if not FW.exists():
        return -1
    count = 0
    for path in FW.rglob("*"):
        if path.is_file() and path.stat().st_mtime >= RUN_STARTED_TS:
            count += 1
    return count


def validation_rows(rows_by_path: dict[Path, list[dict[str, object]]]) -> list[dict[str, object]]:
    now = stamp()
    inputs = rows_by_path[INPUTS]
    interface = rows_by_path[INTERFACE_CONDITIONS]
    no_go = rows_by_path[NO_GO]
    scan = rows_by_path[BOUNDARY_SCAN]
    selection = rows_by_path[BOUNDARY_SELECTION]
    layer = rows_by_path[BOUNDARY_LAYER]
    decisions = rows_by_path[DECISION]
    all_rows = [row for rows in rows_by_path.values() for row in rows]
    recent_fw = formalization_recent_file_count()
    minimum = min(scan, key=lambda row: float(row["boundary_momentum_norm"]))
    return [
        {
            "check_id": "VAL3193_0_inputs_exist",
            "check": "all cited input paths exist",
            "pass": str(all(row["exists"] == "true" for row in inputs)).lower(),
            "detail": "; ".join(row["input_id"] for row in inputs if row["exists"] != "true") or "all inputs resolved",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3193_1_interface_conditions_present",
            "check": "Pi_1 and Pi_0 interface conditions are recorded",
            "pass": str(
                any(row["object"] == "momentum_conjugate_to_Fprime" for row in interface)
                and any(row["object"] == "momentum_conjugate_to_F" for row in interface)
                and any(row["object"] == "natural_interface_matching" for row in interface)
            ).lower(),
            "detail": "Pi_1=(4/5)u and Pi_0=4u/x-(4/5)u'",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3193_2_no_go_recorded",
            "check": "exterior natural matching no-go proof reaches explicit no-go status",
            "pass": str(any(row["status"] == "NO_GO_FOR_PURE_NATURAL_INTERFACE_MATCHING" for row in no_go)).lower(),
            "detail": "pure natural exterior matching collapses transition to exterior-only",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3193_3_scan_shape",
            "check": "boundary momentum residual scan is dense and finite",
            "pass": str(len(scan) >= 900 and all(math.isfinite(float(row["boundary_momentum_norm"])) for row in scan)).lower(),
            "detail": f"scan_rows={len(scan)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3193_4_no_width_closes_interface",
            "check": "no scanned width has zero natural interface residual",
            "pass": str(float(minimum["boundary_momentum_norm"]) > 1.0e-9).lower(),
            "detail": f"min_width={minimum['transition_width']}; min_norm={minimum['boundary_momentum_norm']}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3193_5_selection_rows",
            "check": "selection table includes reference, balanced, min-N4, and min-boundary-momentum rows",
            "pass": str(len(selection) == 4 and all(row["natural_interface_pass"] == "false" for row in selection)).lower(),
            "detail": f"selection_rows={len(selection)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3193_6_boundary_layer_rows",
            "check": "required counter-momentum rows are generated and remain unsourced",
            "pass": str(len(layer) == 3 and all(row["source_status"] == "BOUNDARY_LAYER_ACTION_NOT_PARENT_DERIVED" for row in layer)).lower(),
            "detail": f"boundary_layer_rows={len(layer)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3193_7_next_target_selected",
            "check": "decision selects source-owned boundary layer or modified parent functional",
            "pass": str(any("3194-Y5-R2FR-source-owned-boundary-layer-action" in row["finding"] for row in decisions)).lower(),
            "detail": "next target is 3194",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3193_8_no_claim_leak",
            "check": "no generated row sets valid_for_claim=true",
            "pass": str(not any(str(row.get("valid_for_claim", "")).lower() == "true" for row in all_rows)).lower(),
            "detail": "all rows are private/nonclaim",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3193_9_formalization_workbench_untouched",
            "check": "formalization-workbench files modified during this run remain zero",
            "pass": str(recent_fw == 0).lower(),
            "detail": f"formalization_recent_file_count={recent_fw}",
            "generated_utc": now,
        },
    ]


def all_output_rows() -> dict[Path, list[dict[str, object]]]:
    inputs = input_rows()
    interface = interface_condition_rows()
    no_go = no_go_rows()
    scan = boundary_scan_rows()
    selection = boundary_selection_rows(scan)
    layer = boundary_layer_rows(selection)
    decisions = decision_rows(selection)
    return {
        INPUTS: inputs,
        INTERFACE_CONDITIONS: interface,
        NO_GO: no_go,
        BOUNDARY_SCAN: scan,
        BOUNDARY_SELECTION: selection,
        BOUNDARY_LAYER: layer,
        DECISION: decisions,
    }


def main() -> None:
    rows_by_path = all_output_rows()
    rows_by_path[VALIDATION] = validation_rows(rows_by_path)
    for path, rows in rows_by_path.items():
        write_csv(path, rows)
    for path in rows_by_path:
        print(path)


if __name__ == "__main__":
    main()
