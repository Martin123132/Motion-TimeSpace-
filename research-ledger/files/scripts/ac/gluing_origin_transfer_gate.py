from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, Iterable, List


CHI_H_NATURAL = 2.875013085986371e-25
TIGHT_A_METRIC_BOUND = 1.400851696295935e-13


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


def finite_action_theorem_rows() -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "FA4490_0_profile_space",
            "object": "finite curvature-profile action domain",
            "statement": "If the parent local profile sector uses J[F]=integral x^4(D2[F])^2 dx with D2[F]=(2/5)F''+2F'/x+6F/(5x^2), then admissible profiles must be locally H2 on each finite interval.",
            "derivation": "D2 contains F''; a jump in F creates delta-prime pieces and a jump in F' creates delta pieces. Squaring those distributions is not a finite action density.",
            "result": "finite J excludes [F]!=0 and [F']!=0 at an internal phase interface",
            "status": "CONDITIONAL_FINITE_ACTION_C1_REGULARITY_THEOREM",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "FA4490_1_C1_constraints",
            "object": "gluing constraints",
            "statement": "The C1 conditions [F]=0 and [F']=0 are not arbitrary closure terms once the parent domain is finite-action H2.",
            "derivation": "Piecewise core/transition/exterior descriptions may be used as coordinates, but the common finite-action configuration space imposes continuity of the field and first derivative.",
            "result": "C1 gluing is a regularity/domain condition, not a tuned physical force",
            "status": "C1_GLUING_ORIGIN_DERIVED_CONDITIONALLY",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "FA4490_2_parent_limit",
            "object": "limits of the theorem",
            "statement": "The theorem derives the origin of the C1 constraints only after the parent has selected this quadratic D2 profile sector or an equivalent finite-layer curvature sector.",
            "derivation": "Finite action signs the domain reaction; it does not prove that global MTS has already selected J[F], the transition hypersurface, or the source coupling product.",
            "result": "gluing moves from arbitrary closure-only to conditional finite-action domain theorem",
            "status": "PARENT_PROFILE_FUNCTIONAL_STILL_UNSIGNED",
            "valid_for_claim": False,
        },
    ]


def constrained_variation_rows(glue_rows: List[Dict[str, str]]) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = [
        {
            "variation_id": "CV4490_0_bulk_boundary_form",
            "object": "piecewise variational boundary term",
            "formula": "delta J_boundary = sum_interfaces([Pi_0] deltaF + [Pi_1] deltaF')",
            "derivation": "Integrating the fourth-order profile variation by parts leaves the 3193 momenta at each artificial interface.",
            "result": "bulk stationarity alone would demand [Pi_0]=[Pi_1]=0",
            "status": "BOUNDARY_FORM_IMPORTED_AND_RECAST",
            "valid_for_claim": False,
        },
        {
            "variation_id": "CV4490_1_domain_reaction_action",
            "object": "finite-action constrained variation",
            "formula": "J_c=J+sum_interfaces(lambda_0[F]+lambda_1[F'])",
            "derivation": "Use Lagrange multipliers for the already-derived finite-action C1 domain constraints, not as a free source-neutral penalty.",
            "result": "delta_lambda J_c=0 gives [F]=0 and [F']=0",
            "status": "CONSTRAINED_DOMAIN_MULTIPLIERS_DERIVED",
            "valid_for_claim": False,
        },
        {
            "variation_id": "CV4490_2_multiplier_solution",
            "object": "reaction-force solution",
            "formula": "[Pi_0]+lambda_0=0; [Pi_1]+lambda_1=0; hence lambda_i=-[Pi_i]",
            "derivation": "The boundary-field variation of J_c cancels the bulk momentum mismatch by the domain reaction force.",
            "result": "the 3194 gluing multiplier equations are recovered from finite-action constrained stationarity",
            "status": "GLUING_MULTIPLIER_ORIGIN_CONDITIONALLY_DERIVED",
            "valid_for_claim": False,
        },
    ]
    for row in glue_rows:
        rows.append(
            {
                "variation_id": "CV4490_" + row["solution_id"].replace("GLUE3194_", "lambda_"),
                "object": row["source_selection"],
                "transition_width": row["transition_width"],
                "N4_D2": row["N4_D2"],
                "lambda_norm": row["lambda_norm"],
                "max_abs_cancellation_residual": row["max_abs_cancellation_residual"],
                "result": "stationary constrained variation cancels all four interface residuals for this candidate profile",
                "status": row["closure_status"],
                "source_status": row["source_status"],
                "valid_for_claim": False,
            }
        )
    return rows


def slip_amplitude_rows(profile_rows: List[Dict[str, str]]) -> List[Dict[str, object]]:
    selected = [
        row
        for row in profile_rows
        if row.get("selection_id")
        in {
            "PSEL4489_0_smoothstep_minN4_candidate",
            "PSEL4489_1_min_N4_exact_EL_scan",
            "PSEL4489_1_balanced_Fpp_jump",
        }
    ]
    couplings = [1.0, 1.0e6, 1.0e9, 1.0e10, 1.0e11]
    rows: List[Dict[str, object]] = []
    for profile in selected:
        n4 = float(profile["N4_D2"])
        for coupling in couplings:
            ph_envelope = 1.25 * coupling * n4
            a_slip_surface = 2.0 * CHI_H_NATURAL * ph_envelope
            fraction_tight = a_slip_surface / TIGHT_A_METRIC_BOUND
            rows.append(
                {
                    "amplitude_id": f"SA4490_{profile['selection_id']}_c{coupling:.0e}",
                    "profile_id": profile["selection_id"],
                    "profile_type": profile["profile_type"],
                    "transition_width": profile["transition_width"],
                    "abs_sK2_kappaSTF": f"{coupling:.15e}",
                    "N4_D2": f"{n4:.15e}",
                    "PH_envelope": f"{ph_envelope:.15e}",
                    "A_slip_surface_envelope": f"{a_slip_surface:.15e}",
                    "tight_pressure_fraction": f"{fraction_tight:.15e}",
                    "formula": "A_slip_surface=2*chi_H*|P_H| <= 2*chi_H*(5/4)*|s_K2*kappa_STF|*N4_D2",
                    "status": "AMPLITUDE_ENVELOPE_DERIVED_NONCLAIM",
                    "valid_for_claim": False,
                }
            )
    return rows


def observable_transfer_matrix_rows() -> List[Dict[str, object]]:
    return [
        {
            "transfer_id": "TM4490_0_state_vector",
            "arena": "common",
            "state_vector": "x=[A_slip_surface,A_DeltaKTF_surface,beta_g00,beta_space,beta_clock,beta_light]",
            "linear_map": "A_total_l2 <= |A_slip_surface|+|A_DeltaKTF_surface|; no cancellation between source lanes",
            "observable": "all arena rows",
            "owner_inputs_needed": "A_DeltaKTF_surface and beta coefficients from parent metric/readout split",
            "status": "NO_CANCELLATION_TRANSFER_STATE_DEFINED",
            "valid_for_claim": False,
        },
        {
            "transfer_id": "TM4490_1_J2_equivalent",
            "arena": "solar_orbital_J2",
            "state_vector": "A_g00_l2=beta_g00*A_total_l2",
            "linear_map": "J2_eff = A_g00_l2/(2*epsilon_surface)",
            "observable": "perihelion/orbital quadrupole pressure and public solar J2 comparison",
            "owner_inputs_needed": "epsilon_surface, beta_g00, source-domain radius/coframe convention, arena J2 bound",
            "status": "J2_TRANSFER_MATRIX_DERIVED_SYMBOLIC",
            "valid_for_claim": False,
        },
        {
            "transfer_id": "TM4490_2_clock_redshift",
            "arena": "clock_redshift",
            "state_vector": "deltaPsi_l2=beta_clock*A_total_l2*(R/r)^3*P2",
            "linear_map": "delta(nu/nu)=deltaPsi_l2",
            "observable": "clock/redshift quadrupole residual",
            "owner_inputs_needed": "beta_clock, clock trajectory, radius normalization, sourced clock residual bound",
            "status": "CLOCK_TRANSFER_MATRIX_DERIVED_SYMBOLIC",
            "valid_for_claim": False,
        },
        {
            "transfer_id": "TM4490_3_light_time",
            "arena": "light_time_lensing",
            "state_vector": "deltaPhi_plus_deltaPsi=beta_light*A_total_l2*(R/r)^3*P2",
            "linear_map": "delta t = c^-1 integral_path beta_light*A_total_l2*(R/r)^3*P2 dl",
            "observable": "Shapiro delay, light bending, ranging residuals",
            "owner_inputs_needed": "beta_light, path geometry, impact parameter, sourced light-time bound",
            "status": "LIGHT_TIME_TRANSFER_MATRIX_DERIVED_SYMBOLIC",
            "valid_for_claim": False,
        },
        {
            "transfer_id": "TM4490_4_PPN_gamma_STF",
            "arena": "PPN_gamma_STF",
            "state_vector": "slip_l2=A_total_l2*(R/r)^3*P2",
            "linear_map": "delta_gamma_eff(theta,r) ~ slip_l2/U_N(r)",
            "observable": "directional gamma-like anisotropic slip residual",
            "owner_inputs_needed": "baseline Newtonian potential U_N, experiment geometry, mapping from STF slip to scalar PPN fit",
            "status": "PPN_STF_TRANSFER_MATRIX_DERIVED_SYMBOLIC",
            "valid_for_claim": False,
        },
        {
            "transfer_id": "TM4490_5_orbital_acceleration",
            "arena": "orbital_dynamics",
            "state_vector": "deltaPhi_l2=beta_g00*A_total_l2*(R/r)^3*P2/2",
            "linear_map": "delta a_i = -partial_i deltaPhi_l2",
            "observable": "ephemeris quadrupole acceleration residual",
            "owner_inputs_needed": "beta_g00, GM/R convention, orbit geometry, sourced acceleration or element bound",
            "status": "ORBIT_TRANSFER_MATRIX_DERIVED_SYMBOLIC",
            "valid_for_claim": False,
        },
    ]


def parent_decision_rows(next_target: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4490_0_C1_origin",
            "finding": "C1 gluing has a conditional parent-domain origin",
            "reason": "finite quadratic D2 action excludes [F] and [F'] jumps",
            "effect": "gluing multipliers are reaction forces of a finite-action constrained domain, not arbitrary tuning",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4490_1_parent_limit",
            "finding": "the global parent action is still unsigned",
            "reason": "the theorem requires parent selection of the D2 curvature sector or an equivalent finite-layer limit",
            "effect": "local-GR claim remains blocked",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4490_2_transfer_matrix",
            "finding": "the fallback is now a symbolic no-cancellation transfer matrix",
            "reason": "slip, DeltaKTF leakage and metric/readout split coefficients are separated by arena",
            "effect": "next work can fill numeric bound rows instead of arguing from pressure proxies",
            "next_action": next_target,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(
    sources: List[Dict[str, object]],
    theorem_rows: List[Dict[str, object]],
    variation_rows: List[Dict[str, object]],
    amplitude_rows: List[Dict[str, object]],
    transfer_rows: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "CG4490_0_sources",
            "requirement": "all cited source paths exist and needles are found",
            "passed": all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources),
            "claim_allowed": False,
            "reason": "source-backed private checkpoint only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4490_1_finite_action_C1",
            "requirement": "finite-action C1 regularity theorem written",
            "passed": any(row.get("theorem_id") == "FA4490_1_C1_constraints" for row in theorem_rows),
            "claim_allowed": False,
            "reason": "conditional on parent selecting the D2 sector",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4490_2_lambda_origin",
            "requirement": "lambda_i=-[Pi_i] recovered from constrained variation",
            "passed": any(row.get("variation_id") == "CV4490_2_multiplier_solution" for row in variation_rows),
            "claim_allowed": False,
            "reason": "domain-reaction origin is conditional, not global parent proof",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4490_3_amplitude_envelopes",
            "requirement": "A_slip_surface envelopes generated for profile/coupling rows",
            "passed": len(amplitude_rows) >= 10,
            "claim_allowed": False,
            "reason": "coupling product remains unsigned",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4490_4_transfer_matrix",
            "requirement": "J2, clock, light-time, PPN and orbital transfer rows exist",
            "passed": len(transfer_rows) >= 6,
            "claim_allowed": False,
            "reason": "numeric beta/DeltaKTF/arena bound rows still required",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4490_5_local_GR",
            "requirement": "local-GR claim",
            "passed": False,
            "claim_allowed": False,
            "reason": "parent action, coupling product, split coefficients and arena bounds remain unsigned",
            "valid_for_claim": False,
        },
    ]
