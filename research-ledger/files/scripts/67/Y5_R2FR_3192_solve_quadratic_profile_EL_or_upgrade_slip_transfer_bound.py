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

INPUTS = OUT / "P8_Y5_R2FR_3192_INPUTS.csv"
EL_OPERATOR = OUT / "P8_Y5_R2FR_3192_EL_OPERATOR_DERIVATION.csv"
SMOOTHSTEP_RESIDUAL = OUT / "P8_Y5_R2FR_3192_SMOOTHSTEP_EL_RESIDUAL_SCAN.csv"
STATIONARY_SCAN = OUT / "P8_Y5_R2FR_3192_EL_STATIONARY_TRANSITION_SCAN.csv"
STATIONARY_SELECTION = OUT / "P8_Y5_R2FR_3192_EL_STATIONARY_SELECTION.csv"
DECISION = OUT / "P8_Y5_R2FR_3192_PROFILE_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3192_VALIDATION.csv"

SELECTION_3190 = OUT / "P8_Y5_R2FR_3190_PROFILE_SELECTION_CANDIDATE.csv"
PH_MARGIN_3186 = OUT / "P8_Y5_R2FR_3186_PH_AMPLITUDE_MARGIN_RUNNER.csv"


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


def selected_smoothstep_width() -> float:
    rows = read_csv(SELECTION_3190)
    selected = next(row for row in rows if row["selection_id"] == "SEL3190_0_min_N4_candidate")
    return float(selected["selected_width"])


def tightest_ph_bound() -> float:
    rows = read_csv(PH_MARGIN_3186)
    tight = min(rows, key=lambda row: float(row["P_H_bound_from_slip"]))
    return float(tight["P_H_bound_from_slip"])


def d2_power_coefficient(power: float) -> float:
    return (2.0 / 5.0) * (power + 1.0) * (power + 3.0)


def d2_adjoint_power_coefficient(power: float) -> float:
    return (2.0 / 5.0) * (power - 2.0) * (power - 4.0)


def normal_power_coefficient(power: float) -> float:
    return d2_power_coefficient(power) * d2_adjoint_power_coefficient(power + 2.0)


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


def stationary_fpp(constant: float, quadratic: float, inverse: float, inverse_cubed: float, x_value: float) -> float:
    del constant
    return 2.0 * quadratic + 2.0 * inverse * x_value**-3 + 12.0 * inverse_cubed * x_value**-5


def stationary_d2(constant: float, quadratic: float, x_value: float) -> float:
    return 6.0 * quadratic + 1.2 * constant * x_value**-2


def stationary_integrals(width: float) -> dict[str, float]:
    left = 1.0 - width
    right = 1.0 + width
    constant, quadratic, inverse, inverse_cubed = stationary_coefficients(width)
    core_signed = 6.0 * left**5 / 5.0
    transition_signed = transition_primitive(constant, quadratic, right) - transition_primitive(constant, quadratic, left)
    transition_abs = transition_abs_integral(constant, quadratic, left, right)
    signed = core_signed + transition_signed
    absolute = abs(core_signed) + transition_abs
    core_fpp_jump = stationary_fpp(constant, quadratic, inverse, inverse_cubed, left) - 2.0
    exterior_fpp_jump = stationary_fpp(constant, quadratic, inverse, inverse_cubed, right) - 12.0 * right**-5
    core_d2_jump = stationary_d2(constant, quadratic, left) - 6.0
    exterior_d2_jump = stationary_d2(constant, quadratic, right)
    root_square = -0.2 * constant / quadratic if abs(quadratic) > 1.0e-300 else float("nan")
    sign_change = math.sqrt(root_square) if root_square > 0.0 and left < math.sqrt(root_square) < right else float("nan")
    return {
        "width": width,
        "left": left,
        "right": right,
        "constant": constant,
        "quadratic": quadratic,
        "inverse": inverse,
        "inverse_cubed": inverse_cubed,
        "I4_D2": signed,
        "N4_D2": absolute,
        "c_ext_est": -5.0 * signed / 4.0,
        "sign_change_x": sign_change,
        "core_Fpp_jump": core_fpp_jump,
        "exterior_Fpp_jump": exterior_fpp_jump,
        "max_abs_Fpp_jump": max(abs(core_fpp_jump), abs(exterior_fpp_jump)),
        "core_D2_jump": core_d2_jump,
        "exterior_D2_jump": exterior_d2_jump,
        "max_abs_D2_jump": max(abs(core_d2_jump), abs(exterior_d2_jump)),
    }


def smoothstep(t_value: float) -> float:
    return 6.0 * t_value**5 - 15.0 * t_value**4 + 10.0 * t_value**3


def smoothstep_prime(t_value: float) -> float:
    return 30.0 * t_value**4 - 60.0 * t_value**3 + 30.0 * t_value**2


def smoothstep_second(t_value: float) -> float:
    return 120.0 * t_value**3 - 180.0 * t_value**2 + 60.0 * t_value


def smoothstep_d2_transition(x_value: float, width: float) -> float:
    left = 1.0 - width
    t_value = (x_value - left) / (2.0 * width)
    blend = smoothstep(t_value)
    blend_x = smoothstep_prime(t_value) / (2.0 * width)
    blend_xx = smoothstep_second(t_value) / (4.0 * width**2)
    gap = x_value**-3 - x_value**2
    gap_x = -3.0 * x_value**-4 - 2.0 * x_value
    gap_xx = 12.0 * x_value**-5 - 2.0
    value = x_value**2 + blend * gap
    first = 2.0 * x_value + blend_x * gap + blend * gap_x
    second = 2.0 + blend_xx * gap + 2.0 * blend_x * gap_x + blend * gap_xx
    return 0.4 * second + 2.0 * first / x_value + 1.2 * value / x_value**2


def simpson_transition(width: float, absolute: bool, steps: int = 4000) -> float:
    if steps % 2:
        steps += 1
    left = 1.0 - width
    right = 1.0 + width
    step = (right - left) / steps
    total = 0.0
    for index in range(steps + 1):
        x_value = left + index * step
        value = smoothstep_d2_transition(x_value, width) * x_value**4
        if absolute:
            value = abs(value)
        coefficient = 1 if index in (0, steps) else (4 if index % 2 else 2)
        total += coefficient * value
    return total * step / 3.0


def smoothstep_integrals(width: float) -> dict[str, float]:
    left = 1.0 - width
    core_signed = 6.0 * left**5 / 5.0
    transition_signed = simpson_transition(width, absolute=False)
    transition_abs = simpson_transition(width, absolute=True)
    signed = core_signed + transition_signed
    absolute = abs(core_signed) + transition_abs
    return {
        "I4_D2": signed,
        "N4_D2": absolute,
        "c_ext_est": -5.0 * signed / 4.0,
    }


def smoothstep_residual(width: float, points: int = 4001, trim: int = 20) -> dict[str, float]:
    left = 1.0 - width
    right = 1.0 + width
    step = (right - left) / (points - 1)
    grid = [left + index * step for index in range(points)]
    u_values = [x_value**4 * smoothstep_d2_transition(x_value, width) for x_value in grid]
    residuals: list[float] = []
    residual_grid: list[float] = []
    source_values: list[float] = []
    for index in range(trim, points - trim):
        x_value = grid[index]
        u_second = (u_values[index + 1] - 2.0 * u_values[index] + u_values[index - 1]) / step**2
        two_u_over_x_next = 2.0 * u_values[index + 1] / grid[index + 1]
        two_u_over_x_prev = 2.0 * u_values[index - 1] / grid[index - 1]
        two_u_over_x_first = (two_u_over_x_next - two_u_over_x_prev) / (2.0 * step)
        residual = 0.4 * u_second - two_u_over_x_first + 1.2 * u_values[index] / x_value**2
        residuals.append(residual)
        residual_grid.append(x_value)
        source_values.append(u_values[index])
    residual_l2 = trapezoid_square_root(residual_grid, residuals)
    source_l2 = trapezoid_square_root(residual_grid, source_values)
    return {
        "residual_L2_trimmed": residual_l2,
        "residual_Linf_trimmed": max(abs(value) for value in residuals),
        "source_L2_trimmed": source_l2,
        "relative_residual_to_source_L2": residual_l2 / source_l2 if source_l2 else float("inf"),
        "trimmed_points": float(len(residuals)),
        "grid_step": step,
    }


def trapezoid_square_root(grid: list[float], values: list[float]) -> float:
    total = 0.0
    for index in range(len(values) - 1):
        total += 0.5 * (values[index] ** 2 + values[index + 1] ** 2) * (grid[index + 1] - grid[index])
    return math.sqrt(total)


def input_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = [
        (
            "post_checkpoint",
            "3191-Y5-R2FR-selected-profile-transfer-runner-or-parent-action-profile-equation-under-AX1090.md",
            "3191 selected the quadratic parent-profile EL contract",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3191_PARENT_PROFILE_EQUATION_CONTRACT.csv",
            "3191 EL operator contract",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3190_PROFILE_SELECTION_CANDIDATE.csv",
            "3190 selected C2 smoothstep candidate",
        ),
        (
            "post_checkpoint",
            "source-intake/mts_residuals/P8_Y5_R2FR_3186_PH_AMPLITUDE_MARGIN_RUNNER.csv",
            "3186 tight P_H pressure ceiling",
        ),
        (
            "formalization",
            "83-parent-equations-v1.md",
            "current parent equation scaffold still not source-owned",
        ),
    ]
    return [
        {
            "input_id": f"IN3192_{index}",
            "base": base,
            "path": str(resolve(base, relative).resolve()),
            "exists": str(resolve(base, relative).exists()).lower(),
            "role": role,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for index, (base, relative, role) in enumerate(rows)
    ]


def el_operator_rows() -> list[dict[str, object]]:
    now = stamp()
    mode_rows = [
        {
            "derivation_id": "EL3192_3_normal_mode_constant",
            "object": "normal_mode",
            "formula": "F=x^0",
            "coefficient": f"{normal_power_coefficient(0.0):.15e}",
            "status": "NORMAL_MODE",
        },
        {
            "derivation_id": "EL3192_4_normal_mode_quadratic",
            "object": "normal_mode",
            "formula": "F=x^2",
            "coefficient": f"{normal_power_coefficient(2.0):.15e}",
            "status": "NORMAL_MODE",
        },
        {
            "derivation_id": "EL3192_5_normal_mode_inverse",
            "object": "normal_mode",
            "formula": "F=x^-1",
            "coefficient": f"{normal_power_coefficient(-1.0):.15e}",
            "status": "NORMAL_MODE",
        },
        {
            "derivation_id": "EL3192_6_normal_mode_inverse_cubed",
            "object": "normal_mode",
            "formula": "F=x^-3",
            "coefficient": f"{normal_power_coefficient(-3.0):.15e}",
            "status": "NORMAL_MODE",
        },
    ]
    rows = [
        {
            "derivation_id": "EL3192_0_D2_power_law",
            "object": "operator_identity",
            "formula": "D2[x^p]=(2/5)(p+1)(p+3)x^(p-2)",
            "coefficient": "symbolic",
            "status": "DERIVED",
        },
        {
            "derivation_id": "EL3192_1_adjoint_power_law",
            "object": "operator_identity",
            "formula": "D2dagger[x^q]=(2/5)(q-2)(q-4)x^(q-2)",
            "coefficient": "symbolic",
            "status": "DERIVED",
        },
        {
            "derivation_id": "EL3192_2_normal_power_law",
            "object": "operator_identity",
            "formula": "D2dagger[x^4D2[x^p]]=(4/25)p(p-2)(p+1)(p+3)x^p",
            "coefficient": "symbolic",
            "status": "DERIVED",
        },
        *mode_rows,
        {
            "derivation_id": "EL3192_7_general_transition_solution",
            "object": "EL_solution_family",
            "formula": "F_EL(x)=A+B*x^2+C/x+D/x^3 between fixed core/exterior boundary data",
            "coefficient": "four constants fixed by F,Fprime at x=1-w and x=1+w",
            "status": "INTERIOR_EL_SOLVED_NOT_PARENT_SIGNED",
        },
    ]
    return [{**row, "valid_for_claim": "false", "generated_utc": now} for row in rows]


def smoothstep_residual_rows() -> list[dict[str, object]]:
    now = stamp()
    selected_width = selected_smoothstep_width()
    widths = [0.2, 0.3, selected_width, 0.5, 0.7, 0.8]
    rows = []
    for width in widths:
        integrals = smoothstep_integrals(width)
        residual = smoothstep_residual(width)
        rows.append(
            {
                "scan_id": f"SMOOTH3192_w{width:.3f}",
                "profile_family": "C2_smoothstep_core_x2_to_exterior_xminus3",
                "transition_width": f"{width:.15e}",
                "is_3190_selected_width": str(abs(width - selected_width) < 1.0e-12).lower(),
                "I4_D2": f"{integrals['I4_D2']:.15e}",
                "N4_D2": f"{integrals['N4_D2']:.15e}",
                "c_ext_est": f"{integrals['c_ext_est']:.15e}",
                "residual_L2_trimmed": f"{residual['residual_L2_trimmed']:.15e}",
                "residual_Linf_trimmed": f"{residual['residual_Linf_trimmed']:.15e}",
                "source_L2_trimmed": f"{residual['source_L2_trimmed']:.15e}",
                "relative_residual_to_source_L2": f"{residual['relative_residual_to_source_L2']:.15e}",
                "grid_step": f"{residual['grid_step']:.15e}",
                "trimmed_points": f"{residual['trimmed_points']:.0f}",
                "status": "SMOOTHSTEP_NOT_EL_STATIONARY_INTERIOR_NONCLAIM",
                "endpoint_status": "C2_PROFILE_EL_USES_FOURTH_DERIVATIVES_ENDPOINT_WEAK_TERMS_NOT_CLOSED",
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )
    return rows


def stationary_scan_rows() -> list[dict[str, object]]:
    now = stamp()
    selected_width = selected_smoothstep_width()
    ph_bound = tightest_ph_bound()
    source_norm_limit = 0.8 * ph_bound
    widths = sorted({round(index / 1000.0, 3) for index in range(20, 951)} | {round(selected_width, 3)})
    rows = []
    for width in widths:
        data = stationary_integrals(width)
        rows.append(
            {
                "scan_id": f"ELSTAT3192_w{width:.3f}",
                "profile_family": "C1_exact_interior_EL_solution",
                "transition_width": f"{width:.15e}",
                "left_join": f"{data['left']:.15e}",
                "right_join": f"{data['right']:.15e}",
                "A_constant": f"{data['constant']:.15e}",
                "B_quadratic": f"{data['quadratic']:.15e}",
                "C_inverse": f"{data['inverse']:.15e}",
                "D_inverse_cubed": f"{data['inverse_cubed']:.15e}",
                "I4_D2": f"{data['I4_D2']:.15e}",
                "N4_D2": f"{data['N4_D2']:.15e}",
                "c_ext_est": f"{data['c_ext_est']:.15e}",
                "sign_change_x": "" if math.isnan(data["sign_change_x"]) else f"{data['sign_change_x']:.15e}",
                "PH_envelope_per_abs_sK2_kappaSTF": f"{1.25 * data['N4_D2']:.15e}",
                "critical_abs_sK2_kappaSTF_for_tight_proxy": f"{source_norm_limit / data['N4_D2']:.15e}",
                "core_Fpp_jump": f"{data['core_Fpp_jump']:.15e}",
                "exterior_Fpp_jump": f"{data['exterior_Fpp_jump']:.15e}",
                "max_abs_Fpp_jump": f"{data['max_abs_Fpp_jump']:.15e}",
                "core_D2_jump": f"{data['core_D2_jump']:.15e}",
                "exterior_D2_jump": f"{data['exterior_D2_jump']:.15e}",
                "max_abs_D2_jump": f"{data['max_abs_D2_jump']:.15e}",
                "interior_EL_residual_status": "ZERO_BY_NORMAL_MODE_CONSTRUCTION",
                "boundary_status": "C1_MATCHED_ONLY_BOUNDARY_LAYER_OR_NATURAL_BOUNDARY_CONDITIONS_REQUIRED",
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )
    return rows


def stationary_selection_rows(scan: list[dict[str, object]], smooth: list[dict[str, object]]) -> list[dict[str, object]]:
    now = stamp()
    selected_width = selected_smoothstep_width()
    selected_el = next(row for row in scan if abs(float(row["transition_width"]) - selected_width) < 1.0e-12)
    selected_smooth = next(row for row in smooth if row["is_3190_selected_width"] == "true")
    min_n4 = min(scan, key=lambda row: float(row["N4_D2"]))
    min_jump = min(scan, key=lambda row: float(row["max_abs_Fpp_jump"]))
    core_jump_zero_candidate = min(scan, key=lambda row: abs(float(row["core_Fpp_jump"])))
    return [
        {
            "selection_id": "SEL3192_0_3190_width_exact_EL_comparison",
            "criterion": "replace smoothstep transition by exact interior EL transition at same width",
            "transition_width": selected_el["transition_width"],
            "smoothstep_N4_D2": selected_smooth["N4_D2"],
            "exact_EL_N4_D2": selected_el["N4_D2"],
            "N4_improvement_factor": f"{float(selected_smooth['N4_D2']) / float(selected_el['N4_D2']):.15e}",
            "max_abs_Fpp_jump": selected_el["max_abs_Fpp_jump"],
            "critical_abs_sK2_kappaSTF_for_tight_proxy": selected_el["critical_abs_sK2_kappaSTF_for_tight_proxy"],
            "status": "EXACT_INTERIOR_EL_PROFILE_BEATS_SMOOTHSTEP_BUT_BOUNDARY_NOT_CLOSED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "selection_id": "SEL3192_1_min_N4_exact_EL_scan",
            "criterion": "minimize N4_D2 over C1 exact interior EL scan width in [0.020,0.950]",
            "transition_width": min_n4["transition_width"],
            "smoothstep_N4_D2": selected_smooth["N4_D2"],
            "exact_EL_N4_D2": min_n4["N4_D2"],
            "N4_improvement_factor": f"{float(selected_smooth['N4_D2']) / float(min_n4['N4_D2']):.15e}",
            "max_abs_Fpp_jump": min_n4["max_abs_Fpp_jump"],
            "critical_abs_sK2_kappaSTF_for_tight_proxy": min_n4["critical_abs_sK2_kappaSTF_for_tight_proxy"],
            "status": "MIN_N4_PUSHES_WIDE_TRANSITION_AND_LARGE_CORE_BOUNDARY_JUMP",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "selection_id": "SEL3192_2_balanced_boundary_jump_exact_EL",
            "criterion": "minimize maximum absolute Fpp jump over exact interior EL scan",
            "transition_width": min_jump["transition_width"],
            "smoothstep_N4_D2": selected_smooth["N4_D2"],
            "exact_EL_N4_D2": min_jump["N4_D2"],
            "N4_improvement_factor": f"{float(selected_smooth['N4_D2']) / float(min_jump['N4_D2']):.15e}",
            "max_abs_Fpp_jump": min_jump["max_abs_Fpp_jump"],
            "critical_abs_sK2_kappaSTF_for_tight_proxy": min_jump["critical_abs_sK2_kappaSTF_for_tight_proxy"],
            "status": "BALANCED_BOUNDARY_JUMP_CANDIDATE_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "selection_id": "SEL3192_3_core_curvature_jump_zero_candidate",
            "criterion": "nearly zero core-side Fpp jump, accepting exterior-side jump",
            "transition_width": core_jump_zero_candidate["transition_width"],
            "smoothstep_N4_D2": selected_smooth["N4_D2"],
            "exact_EL_N4_D2": core_jump_zero_candidate["N4_D2"],
            "N4_improvement_factor": f"{float(selected_smooth['N4_D2']) / float(core_jump_zero_candidate['N4_D2']):.15e}",
            "max_abs_Fpp_jump": core_jump_zero_candidate["max_abs_Fpp_jump"],
            "critical_abs_sK2_kappaSTF_for_tight_proxy": core_jump_zero_candidate["critical_abs_sK2_kappaSTF_for_tight_proxy"],
            "status": "CORE_JUMP_CAN_BE_TUNED_SMALL_EXTERIOR_JUMP_REMAINS",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows(selection: list[dict[str, object]], smooth: list[dict[str, object]]) -> list[dict[str, object]]:
    now = stamp()
    same_width = next(row for row in selection if row["selection_id"] == "SEL3192_0_3190_width_exact_EL_comparison")
    balanced = next(row for row in selection if row["selection_id"] == "SEL3192_2_balanced_boundary_jump_exact_EL")
    selected_smooth = next(row for row in smooth if row["is_3190_selected_width"] == "true")
    return [
        {
            "decision_id": "DEC3192_0_toy_EL_solved",
            "finding": "The quadratic toy profile equation is not just a blocker: its interior normal equation has exact modes F=A+B*x^2+C/x+D/x^3.",
            "claim_status": "INTERIOR_PROFILE_EQUATION_SOLVED_FOR_TOY_FUNCTIONAL_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3192_1_smoothstep_demoted",
            "finding": f"The 3190 smoothstep width has trimmed EL residual L2 {selected_smooth['residual_L2_trimmed']}; it is pressure-friendly but not stationary.",
            "claim_status": "SMOOTHSTEP_IS_ANSATZ_NOT_PARENT_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3192_2_exact_branch_improves_pressure",
            "finding": f"At the same width, exact interior EL gives N4 improvement factor {same_width['N4_improvement_factor']} but keeps boundary jump {same_width['max_abs_Fpp_jump']}.",
            "claim_status": "PRESSURE_MARGIN_IMPROVED_BOUNDARY_NOT_CLOSED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3192_3_boundary_regularization_gate",
            "finding": f"Best balanced boundary-jump row is width {balanced['transition_width']} with N4 {balanced['exact_EL_N4_D2']} and max Fpp jump {balanced['max_abs_Fpp_jump']}.",
            "claim_status": "PARENT_BOUNDARY_CONDITION_OR_BOUNDARY_LAYER_NOW_REQUIRED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3192_4_next_target",
            "finding": "3193-Y5-R2FR-parent-boundary-regularity-or-natural-boundary-layer-under-AX1090",
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
    el_rows = rows_by_path[EL_OPERATOR]
    smooth = rows_by_path[SMOOTHSTEP_RESIDUAL]
    scan = rows_by_path[STATIONARY_SCAN]
    selection = rows_by_path[STATIONARY_SELECTION]
    decisions = rows_by_path[DECISION]
    all_rows = [row for rows in rows_by_path.values() for row in rows]
    selected_smooth = next(row for row in smooth if row["is_3190_selected_width"] == "true")
    same_width = next(row for row in selection if row["selection_id"] == "SEL3192_0_3190_width_exact_EL_comparison")
    mode_formulas = {row["formula"] for row in el_rows if row["object"] == "normal_mode"}
    recent_fw = formalization_recent_file_count()
    return [
        {
            "check_id": "VAL3192_0_inputs_exist",
            "check": "all cited input paths exist",
            "pass": str(all(row["exists"] == "true" for row in inputs)).lower(),
            "detail": "; ".join(row["input_id"] for row in inputs if row["exists"] != "true") or "all inputs resolved",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3192_1_normal_modes_present",
            "check": "normal equation records the four expected power-law modes",
            "pass": str({"F=x^0", "F=x^2", "F=x^-1", "F=x^-3"}.issubset(mode_formulas)).lower(),
            "detail": "; ".join(sorted(mode_formulas)),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3192_2_stationary_scan_shape",
            "check": "stationary scan has dense finite width rows",
            "pass": str(len(scan) >= 900 and all(math.isfinite(float(row["N4_D2"])) for row in scan)).lower(),
            "detail": f"stationary_rows={len(scan)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3192_3_I4_identity_preserved",
            "check": "exact stationary transition preserves I4_D2=-4/5 across scan",
            "pass": str(all(abs(float(row["I4_D2"]) + 0.8) < 1.0e-10 for row in scan)).lower(),
            "detail": "c_ext_est remains unity for c_ext=1 exterior normalization",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3192_4_exact_branch_beats_smoothstep_N4",
            "check": "exact EL transition at 3190 width has smaller N4 than selected smoothstep",
            "pass": str(float(same_width["exact_EL_N4_D2"]) < float(same_width["smoothstep_N4_D2"])).lower(),
            "detail": f"improvement_factor={same_width['N4_improvement_factor']}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3192_5_smoothstep_residual_detected",
            "check": "selected smoothstep has finite nonzero interior EL residual",
            "pass": str(float(selected_smooth["residual_L2_trimmed"]) > 0.0 and math.isfinite(float(selected_smooth["residual_L2_trimmed"]))).lower(),
            "detail": f"selected_residual_L2={selected_smooth['residual_L2_trimmed']}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3192_6_boundary_gate_not_claimed",
            "check": "decision rows keep boundary regularity open instead of claiming local GR",
            "pass": str(any(row["claim_status"] == "PARENT_BOUNDARY_CONDITION_OR_BOUNDARY_LAYER_NOW_REQUIRED" for row in decisions)).lower(),
            "detail": "boundary layer/natural boundary condition is the next gate",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3192_7_no_claim_leak",
            "check": "no generated row sets valid_for_claim=true",
            "pass": str(not any(str(row.get("valid_for_claim", "")).lower() == "true" for row in all_rows)).lower(),
            "detail": "all rows are private/nonclaim",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3192_8_formalization_workbench_untouched",
            "check": "formalization-workbench files modified during this run remain zero",
            "pass": str(recent_fw == 0).lower(),
            "detail": f"formalization_recent_file_count={recent_fw}",
            "generated_utc": now,
        },
    ]


def all_output_rows() -> dict[Path, list[dict[str, object]]]:
    inputs = input_rows()
    el = el_operator_rows()
    smooth = smoothstep_residual_rows()
    scan = stationary_scan_rows()
    selection = stationary_selection_rows(scan, smooth)
    decisions = decision_rows(selection, smooth)
    return {
        INPUTS: inputs,
        EL_OPERATOR: el,
        SMOOTHSTEP_RESIDUAL: smooth,
        STATIONARY_SCAN: scan,
        STATIONARY_SELECTION: selection,
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
