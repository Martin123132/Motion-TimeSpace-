from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, Iterable, List


EPSILON_SUN_SURFACE = 2.122502570145357e-6
J2_HALF_RANGE_A_BOUND = 1.400851696295935e-13
GAMMA_BOUND = 2.3e-5
ORBIT_COMBO_BOUND = 4.666666666666667e-5
CLOCK_ALPHA_BOUND = 5.15e-5


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


def bound_input_pack_rows() -> List[Dict[str, object]]:
    gamma_surface = GAMMA_BOUND * EPSILON_SUN_SURFACE
    orbit_surface = ORBIT_COMBO_BOUND * EPSILON_SUN_SURFACE
    return [
        {
            "bound_id": "TB4491_0_J2_surface_half_range",
            "arena": "solar_orbital_J2",
            "observable": "surface_l2_metric_amplitude",
            "bound_on_A_total_l2": f"{J2_HALF_RANGE_A_BOUND:.15e}",
            "units": "dimensionless",
            "transfer_assumption": "beta_g00=1; rho=1; A_total_l2 directly compared to public J2 surface P2 amplitude",
            "source_anchor": "PHB4487_solar_J2_half_range_proxy; J2T4482_2_corrected_J2eff",
            "claim_scope": "tight pressure proxy; not a public J2 pass",
            "valid_for_claim": False,
        },
        {
            "bound_id": "TB4491_1_PPN_gamma_surface_proxy",
            "arena": "PPN_gamma_STF",
            "observable": "gamma_like_anisotropic_slip_at_solar_surface",
            "bound_on_A_total_l2": f"{gamma_surface:.15e}",
            "units": "dimensionless",
            "transfer_assumption": "delta_gamma_eff~A_total_l2/U_N_surface with U_N_surface=GM/(c^2R)",
            "source_anchor": "B4173_00_gamma; BND4085_0_gamma_cassini",
            "claim_scope": "surface normalization proxy; experiment geometry still needed",
            "valid_for_claim": False,
        },
        {
            "bound_id": "TB4491_2_light_time_surface_proxy",
            "arena": "light_time_lensing",
            "observable": "Cassini_gamma_like_light_time_slip",
            "bound_on_A_total_l2": f"{gamma_surface:.15e}",
            "units": "dimensionless",
            "transfer_assumption": "same surface gamma proxy before path integral factor; beta_light=1",
            "source_anchor": "B4173_00_gamma; Cassini Shapiro source row",
            "claim_scope": "line-of-sight integral not yet evaluated",
            "valid_for_claim": False,
        },
        {
            "bound_id": "TB4491_3_clock_redshift_unit_proxy",
            "arena": "clock_redshift",
            "observable": "redshift_violation_alpha_unit_potential",
            "bound_on_A_total_l2": f"{CLOCK_ALPHA_BOUND:.15e}",
            "units": "dimensionless",
            "transfer_assumption": "unit beta_clock and unit normalized P2 potential coefficient; physical clock path factor still required",
            "source_anchor": "B4173_13_clock",
            "claim_scope": "unit-transfer proxy only",
            "valid_for_claim": False,
        },
        {
            "bound_id": "TB4491_4_orbital_combo_surface_proxy",
            "arena": "orbital_dynamics",
            "observable": "perihelion_combo_surface_proxy",
            "bound_on_A_total_l2": f"{orbit_surface:.15e}",
            "units": "dimensionless",
            "transfer_assumption": "((2+2gamma-beta)/3)-1 surface proxy multiplied by U_N_surface",
            "source_anchor": "B4173_14_orbit_combo",
            "claim_scope": "orbital element/ephemeris transfer not yet integrated",
            "valid_for_claim": False,
        },
    ]


def select_amplitude_rows(amplitude_rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    allowed_profiles = {
        "PSEL4489_0_smoothstep_minN4_candidate",
        "PSEL4489_1_min_N4_exact_EL_scan",
        "PSEL4489_1_balanced_Fpp_jump",
    }
    allowed_couplings = {
        "1.000000000000000e+00",
        "1.000000000000000e+09",
        "1.000000000000000e+11",
    }
    return [
        row
        for row in amplitude_rows
        if row.get("profile_id") in allowed_profiles and row.get("abs_sK2_kappaSTF") in allowed_couplings
    ]


def no_cancellation_scorer_rows(amplitude_rows: List[Dict[str, str]], bound_rows: List[Dict[str, object]]) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for amp in select_amplitude_rows(amplitude_rows):
        a_slip = float(amp["A_slip_surface_envelope"])
        for bound in bound_rows:
            threshold = float(bound["bound_on_A_total_l2"])
            delta_allowance = max(0.0, threshold - a_slip)
            pass_slip_only = a_slip <= threshold
            rows.append(
                {
                    "score_id": f"NC4491_{amp['profile_id']}_{amp['abs_sK2_kappaSTF']}_{bound['bound_id']}",
                    "profile_id": amp["profile_id"],
                    "arena": bound["arena"],
                    "abs_sK2_kappaSTF": amp["abs_sK2_kappaSTF"],
                    "A_slip_surface_envelope": f"{a_slip:.15e}",
                    "bound_on_A_total_l2": bound["bound_on_A_total_l2"],
                    "fraction_of_bound_slip_only": f"{(a_slip / threshold):.15e}",
                    "remaining_A_DeltaKTF_allowance_no_cancellation": f"{delta_allowance:.15e}",
                    "pass_if_A_DeltaKTF_zero_and_beta_proxy_one": pass_slip_only,
                    "no_cancellation_rule": "|A_slip|+|A_DeltaKTF| <= bound; destructive cancellation forbidden",
                    "status": "SLIP_ONLY_SMOKE_PASS" if pass_slip_only else "SLIP_ONLY_SMOKE_FAIL",
                    "valid_for_claim": False,
                }
            )
    return rows


def deltak_allowance_summary_rows(score_rows: List[Dict[str, object]]) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    grouped: Dict[str, List[Dict[str, object]]] = {}
    for row in score_rows:
        key = f"{row['profile_id']}|{row['abs_sK2_kappaSTF']}"
        grouped.setdefault(key, []).append(row)
    for key, group in grouped.items():
        profile_id, coupling = key.split("|", 1)
        fractions = [float(row["fraction_of_bound_slip_only"]) for row in group]
        allowances = [float(row["remaining_A_DeltaKTF_allowance_no_cancellation"]) for row in group]
        hardest = max(group, key=lambda row: float(row["fraction_of_bound_slip_only"]))
        rows.append(
            {
                "allowance_id": f"DA4491_{profile_id}_{coupling}",
                "profile_id": profile_id,
                "abs_sK2_kappaSTF": coupling,
                "hardest_arena": hardest["arena"],
                "max_fraction_of_bound": f"{max(fractions):.15e}",
                "min_remaining_A_DeltaKTF_allowance": f"{min(allowances):.15e}",
                "all_slip_only_smoke_rows_pass": all(str(row["pass_if_A_DeltaKTF_zero_and_beta_proxy_one"]).lower() == "true" for row in group),
                "interpretation": "positive allowance means finite DeltaKTF leakage can still be bounded; zero allowance means this coupling/profile already fails the tightest proxy unless a zero theorem or smaller beta coefficient exists",
                "valid_for_claim": False,
            }
        )
    return rows


def coupling_zero_audit_rows() -> List[Dict[str, object]]:
    return [
        {
            "zero_id": "Z4491_0_sK2",
            "quantity": "s_K2",
            "zero_condition": "parent variation makes the Hessian source coefficient vanish",
            "current_status": "UNSIGNED",
            "effect_if_zero": "P_H=0 and the slip lane closes independent of profile",
            "fallback_if_not_zero": "use no-cancellation bound rows for each sourced coupling product",
            "valid_for_claim": False,
        },
        {
            "zero_id": "Z4491_1_kappa_STF",
            "quantity": "kappa_STF",
            "zero_condition": "source profile has no tracefree Hessian projection in the public metric channel",
            "current_status": "UNSIGNED",
            "effect_if_zero": "P_H=0 and l2 slip branch closes",
            "fallback_if_not_zero": "derive/source numeric kappa_STF or keep envelope scorer",
            "valid_for_claim": False,
        },
        {
            "zero_id": "Z4491_2_I4_D2",
            "quantity": "I4_D2",
            "zero_condition": "profile cancellation gives I4_D2=0 while preserving exterior matching",
            "current_status": "REJECTED_FOR_CURRENT_MATCHED_EXTERIOR_BRANCH",
            "effect_if_zero": "P_H=0",
            "fallback_if_not_zero": "finite N4_D2 envelope controls magnitude",
            "valid_for_claim": False,
        },
        {
            "zero_id": "Z4491_3_DeltaKTF",
            "quantity": "A_DeltaKTF_surface",
            "zero_condition": "DeltaK_TF is quotient-vertical, same-source silent, or killed by parent metric projection",
            "current_status": "UNSIGNED",
            "effect_if_zero": "slip-only smoke rows become the active transfer test",
            "fallback_if_not_zero": "must satisfy remaining_A_DeltaKTF_allowance_no_cancellation in every arena",
            "valid_for_claim": False,
        },
        {
            "zero_id": "Z4491_4_beta_coefficients",
            "quantity": "beta_g00,beta_space,beta_clock,beta_light",
            "zero_condition": "readout split suppresses a given arena coefficient",
            "current_status": "UNSIGNED",
            "effect_if_zero": "corresponding arena transfer row relaxes or closes",
            "fallback_if_not_zero": "beta=1 proxy is retained as conservative first smoke row",
            "valid_for_claim": False,
        },
    ]


def decision_ledger_rows(next_target: str, allowance_rows: List[Dict[str, object]]) -> List[Dict[str, object]]:
    one_e9 = [row for row in allowance_rows if row["profile_id"] == "PSEL4489_0_smoothstep_minN4_candidate" and row["abs_sK2_kappaSTF"] == "1.000000000000000e+09"]
    one_e11 = [row for row in allowance_rows if row["profile_id"] == "PSEL4489_0_smoothstep_minN4_candidate" and row["abs_sK2_kappaSTF"] == "1.000000000000000e+11"]
    return [
        {
            "decision_id": "DEC4491_0_numeric_pack",
            "finding": "first no-cancellation numeric transfer-bound pack is built",
            "reason": "source-backed/local bound rows now map to A_total_l2 thresholds",
            "effect": "DeltaKTF allowance can be scored instead of hand-waved",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4491_1_moderate_coupling",
            "finding": "smoothstep 1e9 coupling survives the tight J2 surface proxy if DeltaKTF is zero",
            "reason": f"max_fraction={one_e9[0]['max_fraction_of_bound'] if one_e9 else 'missing'}",
            "effect": "moderate finite branch is not instantly killed by the first no-cancellation scorer",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4491_2_huge_coupling",
            "finding": "smoothstep 1e11 coupling fails the tight J2 surface proxy under beta=1 and DeltaKTF=0",
            "reason": f"max_fraction={one_e11[0]['max_fraction_of_bound'] if one_e11 else 'missing'}",
            "effect": "large coupling products require zero theorem, smaller beta coefficient, or a different sourced profile",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4491_3_no_claim",
            "finding": "local-GR remains unclaimed",
            "reason": "parent D2 selection, coupling product, DeltaKTF and arena beta/path coefficients are still unsigned",
            "effect": "4492 must target DeltaKTF/coupling ownership or source-backed coefficient rows",
            "next_action": next_target,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(
    sources: List[Dict[str, object]],
    bound_rows: List[Dict[str, object]],
    score_rows: List[Dict[str, object]],
    allowance_rows: List[Dict[str, object]],
    zero_rows: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    one_e9 = [row for row in allowance_rows if row["profile_id"] == "PSEL4489_0_smoothstep_minN4_candidate" and row["abs_sK2_kappaSTF"] == "1.000000000000000e+09"]
    one_e11 = [row for row in allowance_rows if row["profile_id"] == "PSEL4489_0_smoothstep_minN4_candidate" and row["abs_sK2_kappaSTF"] == "1.000000000000000e+11"]
    return [
        {
            "gate_id": "CG4491_0_sources",
            "requirement": "all cited source paths exist and needles are found",
            "passed": all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources),
            "claim_allowed": False,
            "reason": "source-backed private scorer only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4491_1_bound_rows_numeric",
            "requirement": "all bound rows have positive numeric A_total_l2 thresholds",
            "passed": all(float(row["bound_on_A_total_l2"]) > 0 for row in bound_rows),
            "claim_allowed": False,
            "reason": "numeric proxies are not full arena integrations",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4491_2_no_cancellation_scores",
            "requirement": "no-cancellation scorer rows exist",
            "passed": len(score_rows) >= 40,
            "claim_allowed": False,
            "reason": "DeltaKTF and beta coefficients not sourced",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4491_3_1e9_smoke_survives",
            "requirement": "smoothstep 1e9 slip-only smoke survives every proxy row",
            "passed": bool(one_e9) and str(one_e9[0]["all_slip_only_smoke_rows_pass"]).lower() == "true",
            "claim_allowed": False,
            "reason": "smoke pass assumes A_DeltaKTF=0 and beta=1 proxy normalization",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4491_4_1e11_failure_demonstrator",
            "requirement": "smoothstep 1e11 exhibits a failure in the tight proxy",
            "passed": bool(one_e11) and str(one_e11[0]["all_slip_only_smoke_rows_pass"]).lower() == "false",
            "claim_allowed": False,
            "reason": "shows scorer can reject oversized coupling products",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4491_5_zero_audit",
            "requirement": "coupling and DeltaKTF zero routes are explicitly audited",
            "passed": len(zero_rows) >= 5,
            "claim_allowed": False,
            "reason": "zero theorem not yet signed",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4491_6_local_GR",
            "requirement": "local-GR/J2/PPN claim",
            "passed": False,
            "claim_allowed": False,
            "reason": "numeric scorer is smoke-only until parent coefficients and arena transfer factors are sourced",
            "valid_for_claim": False,
        },
    ]
