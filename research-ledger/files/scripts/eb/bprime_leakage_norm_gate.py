from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Tuple


def write_csv(path: Path, rows: Iterable[Dict[str, object]]) -> None:
    row_list = list(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not row_list:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: List[str] = []
    for row in row_list:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(row_list)


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def solve_linear_4(matrix: List[List[float]], vector: List[float]) -> List[float]:
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


def stationary_coefficients(width: float) -> Tuple[float, float, float, float]:
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


def smoothstep(t_value: float) -> float:
    return 6.0 * t_value**5 - 15.0 * t_value**4 + 10.0 * t_value**3


def smoothstep_prime(t_value: float) -> float:
    return 30.0 * t_value**4 - 60.0 * t_value**3 + 30.0 * t_value**2


def smoothstep_profile(x_value: float, width: float) -> Tuple[float, float]:
    left = 1.0 - width
    t_value = (x_value - left) / (2.0 * width)
    blend = smoothstep(t_value)
    blend_x = smoothstep_prime(t_value) / (2.0 * width)
    core = x_value**2
    core_x = 2.0 * x_value
    exterior = x_value**-3
    exterior_x = -3.0 * x_value**-4
    value = core + blend * (exterior - core)
    derivative = core_x + blend_x * (exterior - core) + blend * (exterior_x - core_x)
    return value, derivative


def exact_el_profile(x_value: float, width: float) -> Tuple[float, float]:
    constant, quadratic, inverse, inverse_cubed = stationary_coefficients(width)
    value = constant + quadratic * x_value**2 + inverse * x_value**-1 + inverse_cubed * x_value**-3
    derivative = 2.0 * quadratic * x_value - inverse * x_value**-2 - 3.0 * inverse_cubed * x_value**-4
    return value, derivative


def x_bprime_from_profile(value: float, derivative: float, x_value: float) -> float:
    return 1.5 * (derivative / x_value - 2.0 * value / x_value**2)


def exterior_tail_norms(right: float) -> Dict[str, float]:
    return {
        "exterior_tail_L1": 1.875 * right**-4,
        "exterior_tail_L2": math.sqrt(6.25 * right**-9),
        "exterior_tail_Linf": 7.5 * right**-5,
    }


def profile_norm(profile_type: str, width: float, steps: int = 40000) -> Dict[str, float]:
    left = 1.0 - width
    right = 1.0 + width
    step = (right - left) / steps
    collar_l1 = 0.0
    collar_l2_square = 0.0
    collar_linf = 0.0
    use_smoothstep = profile_type == "C2_smoothstep_ansatz"
    for index in range(steps + 1):
        x_value = left + index * step
        if use_smoothstep:
            value, derivative = smoothstep_profile(x_value, width)
        else:
            value, derivative = exact_el_profile(x_value, width)
        leakage = abs(x_bprime_from_profile(value, derivative, x_value))
        coefficient = 0.5 if index in (0, steps) else 1.0
        collar_l1 += coefficient * leakage * step
        collar_l2_square += coefficient * leakage * leakage * step
        collar_linf = max(collar_linf, leakage)
    tail = exterior_tail_norms(right)
    full_l1 = collar_l1 + tail["exterior_tail_L1"]
    full_l2 = math.sqrt(collar_l2_square + tail["exterior_tail_L2"] ** 2)
    full_linf = max(collar_linf, tail["exterior_tail_Linf"])
    gate_norm = max(full_l1, full_l2, full_linf)
    return {
        "left_edge": left,
        "right_edge": right,
        "N_Bprime_collar_L1": collar_l1,
        "N_Bprime_collar_L2": math.sqrt(collar_l2_square),
        "N_Bprime_collar_Linf": collar_linf,
        "N_Bprime_exterior_tail_L1": tail["exterior_tail_L1"],
        "N_Bprime_exterior_tail_L2": tail["exterior_tail_L2"],
        "N_Bprime_exterior_tail_Linf": tail["exterior_tail_Linf"],
        "N_Bprime_full_L1": full_l1,
        "N_Bprime_full_L2": full_l2,
        "N_Bprime_full_Linf": full_linf,
        "N_Bprime_gate": gate_norm,
    }


def selected_profile_rows(profile_rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    profile_ids = {
        "PSEL4489_0_smoothstep_minN4_candidate",
        "PSEL4489_1_min_N4_exact_EL_scan",
        "PSEL4489_1_balanced_Fpp_jump",
    }
    return [row for row in profile_rows if row.get("selection_id") in profile_ids]


def bprime_norm_rows(profile_rows: List[Dict[str, str]]) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for row in selected_profile_rows(profile_rows):
        width = float(row["transition_width"])
        profile_type = row["profile_type"]
        norm = profile_norm(profile_type, width)
        rows.append(
            {
                "norm_id": f"NB4493_{row['selection_id']}",
                "profile_id": row["selection_id"],
                "profile_type": profile_type,
                "transition_width": f"{width:.15e}",
                "left_edge": f"{norm['left_edge']:.15e}",
                "right_edge": f"{norm['right_edge']:.15e}",
                "definition": "B=(3/2)F/x^2; leakage envelope uses |x B'| over collar plus analytic r^-3 exterior tail",
                "N_Bprime_collar_L1": f"{norm['N_Bprime_collar_L1']:.15e}",
                "N_Bprime_collar_L2": f"{norm['N_Bprime_collar_L2']:.15e}",
                "N_Bprime_collar_Linf": f"{norm['N_Bprime_collar_Linf']:.15e}",
                "N_Bprime_exterior_tail_L1": f"{norm['N_Bprime_exterior_tail_L1']:.15e}",
                "N_Bprime_exterior_tail_L2": f"{norm['N_Bprime_exterior_tail_L2']:.15e}",
                "N_Bprime_exterior_tail_Linf": f"{norm['N_Bprime_exterior_tail_Linf']:.15e}",
                "N_Bprime_full_L1": f"{norm['N_Bprime_full_L1']:.15e}",
                "N_Bprime_full_L2": f"{norm['N_Bprime_full_L2']:.15e}",
                "N_Bprime_full_Linf": f"{norm['N_Bprime_full_Linf']:.15e}",
                "N_Bprime_gate": f"{norm['N_Bprime_gate']:.15e}",
                "profile_scale_verdict": "ORDER_UNITY_OR_LARGER_LEAKAGE_NOT_PROFILE_SUPPRESSED",
                "valid_for_claim": False,
            }
        )
    return rows


def deltak_requirement_scorer_rows(bprime_bound_rows: List[Dict[str, str]], norm_rows: List[Dict[str, object]]) -> List[Dict[str, object]]:
    norm_by_profile = {str(row["profile_id"]): row for row in norm_rows}
    rows: List[Dict[str, object]] = []
    for bound in bprime_bound_rows:
        profile_id = bound["profile_id"]
        norm = norm_by_profile[profile_id]
        required_product = float(bound["required_CDeltaKTF_times_NBprime_max"])
        gate_norm = float(norm["N_Bprime_gate"])
        required_cdelta = required_product / gate_norm if gate_norm > 0.0 else 0.0
        pass_unit_cdelta = gate_norm <= required_product
        if required_product == 0.0:
            status = "EXACT_ZERO_OR_SMALLER_BETA_REQUIRED"
        elif pass_unit_cdelta:
            status = "UNIT_CDELTAKTF_PASS"
        else:
            status = "CDELTAKTF_SUPPRESSION_REQUIRED"
        rows.append(
            {
                "score_id": f"DBS4493_{profile_id}_{bound['abs_sK2_kappaSTF']}",
                "profile_id": profile_id,
                "abs_sK2_kappaSTF": bound["abs_sK2_kappaSTF"],
                "hardest_arena": bound["hardest_arena"],
                "required_CDeltaKTF_times_NBprime_max": bound["required_CDeltaKTF_times_NBprime_max"],
                "N_Bprime_gate": norm["N_Bprime_gate"],
                "required_CDeltaKTF_max_given_profile_norm": f"{required_cdelta:.15e}",
                "pass_if_CDeltaKTF_equals_one": pass_unit_cdelta,
                "status": status,
                "interpretation": "profile shaping alone does not close DeltaKTF unless this row passes; otherwise parent projection/transfer coefficient must suppress the channel",
                "valid_for_claim": False,
            }
        )
    return rows


def parent_projection_audit_rows() -> List[Dict[str, object]]:
    return [
        {
            "audit_id": "PPA4493_0_public_metric_projection",
            "route": "prove C_DeltaKTF=0 because public metric readout equals P_Y[K_L]",
            "current_evidence": "4492 leaves parent projection/solder route open; 4487 identity-readout branch says metric-null fails without such a map",
            "verdict": "OPEN_NOT_PROVEN",
            "needed_contract": "parent action must define the public metric map and show non-Y_a Hessian tensor footprint is vertical, pure gauge, or boundary silent",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PPA4493_1_profile_suppression",
            "route": "make N_Bprime tiny by profile selection",
            "current_evidence": "computed profile norms are order unity or larger for smoothstep/exact-EL candidates",
            "verdict": "REJECTED_AS_PRIMARY_ROUTE",
            "needed_contract": "a new parent-selected profile would need a dramatically smaller leakage norm and still preserve exterior matching",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PPA4493_2_finite_bound",
            "route": "keep finite leakage and bound it",
            "current_evidence": "4493 converts requirements into C_DeltaKTF maxima after inserting actual N_Bprime",
            "verdict": "FORMULA_READY_PARENT_COEFFICIENT_REQUIRED",
            "needed_contract": "derive/source C_DeltaKTF or a sharper observable Green/readout operator norm",
            "valid_for_claim": False,
        },
    ]


def decision_ledger_rows(next_target: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4493_0_norm_computed",
            "finding": "actual Bprime leakage norms are computed for the active profile family cells",
            "reason": "B=(3/2)F/x^2 gives |xB'| order unity or larger once the nonzero exterior tail and transition collar are included",
            "effect": "DeltaKTF cannot be hidden by profile smoothness alone",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4493_1_balanced_profile_best",
            "finding": "balanced exact-EL width is the best of the tested cells for Bprime leakage",
            "reason": "its gate norm is around order unity while min-N4 exact-EL has a large left-edge spike",
            "effect": "profile optimization helps but not by the twenty-plus orders needed for local bounds",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4493_2_parent_projection_priority",
            "finding": "best route is now parent projection zero or a derived tiny C_DeltaKTF",
            "reason": "moderate 1e9 smoothstep still requires C_DeltaKTF below the 1e-23 scale under the current gate norm",
            "effect": "4494 should attack the parent public-metric projection map rather than continue profile-only tuning",
            "next_action": next_target,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(
    sources: List[Dict[str, object]],
    norm_rows: List[Dict[str, object]],
    score_rows: List[Dict[str, object]],
    parent_rows: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    smooth_1e9 = [
        row
        for row in score_rows
        if row.get("profile_id") == "PSEL4489_0_smoothstep_minN4_candidate"
        and row.get("abs_sK2_kappaSTF") == "1.000000000000000e+09"
    ]
    balanced = [row for row in norm_rows if row.get("profile_id") == "PSEL4489_1_balanced_Fpp_jump"]
    return [
        {
            "gate_id": "CG4493_0_sources",
            "requirement": "all cited source paths exist and needles are found",
            "passed": all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources),
            "claim_allowed": False,
            "reason": "private derivation/numeric-gate checkpoint only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4493_1_norm_rows",
            "requirement": "Bprime leakage norms are computed for active profiles",
            "passed": len(norm_rows) >= 3 and all(float(row["N_Bprime_gate"]) > 0.0 for row in norm_rows),
            "claim_allowed": False,
            "reason": "norm rows are profile-scale inputs, not local-GR closure",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4493_2_balanced_order_unity",
            "requirement": "balanced profile has order-unity leakage rather than a zero",
            "passed": bool(balanced) and 1.0 < float(balanced[0]["N_Bprime_gate"]) < 2.0,
            "claim_allowed": False,
            "reason": "profile helps but does not zero DeltaKTF",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4493_3_smoothstep_1e9_Cdelta_bound",
            "requirement": "smoothstep 1e9 C_DeltaKTF maximum is computed and tiny",
            "passed": bool(smooth_1e9) and float(smooth_1e9[0]["required_CDeltaKTF_max_given_profile_norm"]) < 4.0e-23,
            "claim_allowed": False,
            "reason": "finite route needs parent coefficient suppression",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4493_4_unit_Cdelta_fails",
            "requirement": "no active finite row passes with C_DeltaKTF=1",
            "passed": all(str(row.get("pass_if_CDeltaKTF_equals_one")).lower() == "false" for row in score_rows),
            "claim_allowed": False,
            "reason": "profile-only local safety is rejected",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4493_5_parent_projection_audit",
            "requirement": "parent projection route is classified",
            "passed": len(parent_rows) >= 3 and any(row.get("verdict") == "OPEN_NOT_PROVEN" for row in parent_rows),
            "claim_allowed": False,
            "reason": "C_DeltaKTF=0 theorem is still the priority but not claimed",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4493_6_local_GR",
            "requirement": "local-GR/J2/PPN claim",
            "passed": False,
            "claim_allowed": False,
            "reason": "C_DeltaKTF zero/suppression and full arena transfer remain unclosed",
            "valid_for_claim": False,
        },
    ]
