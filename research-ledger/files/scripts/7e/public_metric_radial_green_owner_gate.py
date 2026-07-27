from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, Iterable, List


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


def radial_green_theorem_rows(two_epsilon: float) -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "RGT4483_0_public_static_operator",
            "object": "exterior_public_l2_metric_channel",
            "hypothesis": "Outside compact support, the already-public weak-field metric potential obeys the source-free Laplace/linearized-EH exterior equation.",
            "derivation_step": "Project the static exterior equation onto a single spherical harmonic mode.",
            "formula": "Delta[R_l(r)Y_lm(theta,phi)]=0 -> r^2 R_l'' + 2r R_l' - l(l+1)R_l=0",
            "conclusion": "The radial profile theorem is a public-channel theorem, not yet a parent MTS coupling theorem.",
            "ownership_status": "CONDITIONAL_PUBLIC_OPERATOR_ASSUMPTION",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "RGT4483_1_power_law_solution",
            "object": "radial_Euler_equation",
            "hypothesis": "The exterior mode is source-free and separable.",
            "derivation_step": "Insert R_l=r^s into r^2 R_l'' + 2r R_l' - l(l+1)R_l=0.",
            "formula": "s(s-1)+2s-l(l+1)=0 -> s=l or s=-(l+1)",
            "conclusion": "R_l(r)=a_l r^l + b_l r^(-l-1).",
            "ownership_status": "DERIVED_RADIAL_GREEN_POWER_LAW",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "RGT4483_2_l2_profile_selection",
            "object": "l_equals_2_exterior_profile",
            "hypothesis": "The source is isolated and asymptotically flat, so no growing public quadrupole branch is allowed at infinity.",
            "derivation_step": "Set l=2 and remove the growing r^2 branch by the boundary condition.",
            "formula": "R_2(r)=a r^2 + b r^-3; asymptotic flatness -> a=0",
            "conclusion": "The public exterior quadrupole profile is proportional to r^-3.",
            "ownership_status": "DERIVED_PUBLIC_R_MINUS_3_PROFILE",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "RGT4483_3_surface_transport",
            "object": "surface_amplitude_to_radius",
            "hypothesis": "A public l=2 metric amplitude A_surface is already owned at the solar surface R_s.",
            "derivation_step": "Normalize the decaying branch by R_2(R_s)=A_surface.",
            "formula": "A_metric(r)=A_surface*(R_s/r)^3 = A_surface*rho^-3",
            "conclusion": "The radial Green transport factor is 1 at the surface and rho^-3 away from it.",
            "ownership_status": "CONDITIONAL_GREEN_FACTOR_CLOSED_AFTER_A_SURFACE_EXISTS",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "RGT4483_4_public_J2_normalization",
            "object": "J2_to_public_metric_amplitude",
            "hypothesis": "Use the standard weak-field public metric convention g00=-(1+2Phi/c^2) and Phi_Q=(GM/r)J2(R_s/r)^2P2.",
            "derivation_step": "Read off the dimensionless P2 coefficient in g00.",
            "formula": "A_metric(r)=2*epsilon_sun_surface*J2*rho^-3",
            "conclusion": f"At rho=1, A_surface={two_epsilon:.15e}*J2, so J2_eff=A_surface/(2*epsilon_sun_surface).",
            "ownership_status": "DERIVED_PUBLIC_METRIC_NORMALIZATION_IMPORTED_FROM_3170",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "RGT4483_5_verdict",
            "object": "Green_profile_owner_status",
            "hypothesis": "The MTS residual has not yet been proven to enter the same public metric channel.",
            "derivation_step": "Separate public radial mathematics from parent coupling/projection ownership.",
            "formula": "G_ext_l2_surface=1 only after A_surface is owned; Upsilon_J2=Pi_J2_metric*T_source*G_ext_l2_surface",
            "conclusion": "The radial r^-3 factor is no longer the mysterious part; Pi_J2_metric and T_source are the hard owner clauses.",
            "ownership_status": "PUBLIC_GREEN_THEOREM_DERIVED_PARENT_OWNER_UNSIGNED",
            "valid_for_claim": False,
        },
    ]


def metric_owner_clause_rows() -> List[Dict[str, object]]:
    return [
        {
            "clause_id": "MOC4483_0_parent_EH_operator",
            "owner_clause": "parent exterior operator match",
            "required_signature": "linearized local parent equations reduce, in the visible exterior l=2 channel, to the same source-free Laplace/linearized-EH operator used by the public theorem",
            "current_result": "the public theorem is derived, but this parent operator match is not signed",
            "blocking_symbol": "L_parent_l2 - L_EH_l2",
            "status": "MISSING_PARENT_OPERATOR_SIGNATURE",
            "claim_effect": "blocks promoting r^-3 theorem into an MTS local-GR/J2 pass",
            "valid_for_claim": False,
        },
        {
            "clause_id": "MOC4483_1_public_metric_projection",
            "owner_clause": "Pi_J2_metric",
            "required_signature": "explicit projection from the finite MTS l=2 residual lane into the public metric P2 amplitude",
            "current_result": "3171 and 4482 identify the missing projection kernel; no parent-owned value exists",
            "blocking_symbol": "Pi_J2_metric",
            "status": "MISSING_PUBLIC_METRIC_PROJECTION_KERNEL",
            "claim_effect": "blocks identifying K2*C_K2_unit with A_metric_solar_surface",
            "valid_for_claim": False,
        },
        {
            "clause_id": "MOC4483_2_source_domain_transfer",
            "owner_clause": "T_source",
            "required_signature": "either build K2 directly in the solar source domain or prove universality from the local/Earth K2 lane to the solar exterior l=2 source",
            "current_result": "existing K2 bookkeeping is internal/local; solar transfer remains unsigned",
            "blocking_symbol": "T_source",
            "status": "MISSING_SOURCE_DOMAIN_TRANSFER",
            "claim_effect": "blocks using solar J2/Shapiro/PPN pressure rows as a direct K2 bound",
            "valid_for_claim": False,
        },
        {
            "clause_id": "MOC4483_3_boundary_selection",
            "owner_clause": "no growing or incoming l2 boundary branch",
            "required_signature": "parent boundary conditions remove r^2, incoming, external-tidal, or hidden boundary l=2 pieces from the extra MTS channel",
            "current_result": "public asymptotic flatness removes the public r^2 branch; parent extra-sector boundary silence is not signed",
            "blocking_symbol": "B_l2_extra",
            "status": "MISSING_PARENT_BOUNDARY_SILENCE",
            "claim_effect": "blocks no-cancellation local residual claim",
            "valid_for_claim": False,
        },
        {
            "clause_id": "MOC4483_4_extra_sector_silence",
            "owner_clause": "no extra l2 residual after GR baseline",
            "required_signature": "same-source GR baseline plus zero or bounded extra-sector l=2 residuals in PPN, clock, Shapiro and orbital readouts",
            "current_result": "1955 supplies the fair residual-l2 scorer shape, not the numeric envelopes",
            "blocking_symbol": "DeltaJ2, P2R_extra, Deltah2, W_STF",
            "status": "MISSING_RESIDUAL_L2_ENVELOPES",
            "claim_effect": "blocks finite branch scoring even if the public Green theorem is available",
            "valid_for_claim": False,
        },
        {
            "clause_id": "MOC4483_5_verdict",
            "owner_clause": "MTS-to-public J2 channel",
            "required_signature": "MOC4483_0 through MOC4483_4 must close together",
            "current_result": "G_ext_l2_surface is conditionally closed, but parent operator/projection/source/residual clauses remain unsigned",
            "blocking_symbol": "Upsilon_J2 = Pi_J2_metric*T_source*G_ext_l2_surface",
            "status": "GREEN_DERIVED_PARENT_CHANNEL_NOT_CLOSED",
            "claim_effect": "local-GR, J2, PPN, clock and orbital pass remains blocked",
            "valid_for_claim": False,
        },
    ]


def finite_scorer_input_rows(corrected_half: float, c_k2_unit: float, two_epsilon: float) -> List[Dict[str, object]]:
    return [
        {
            "input_id": "FSI4483_0_G_ext_l2_surface",
            "symbol": "G_ext_l2_surface",
            "definition": "exterior l=2 radial Green transport from an already-owned public surface amplitude to the same surface",
            "formula_or_value": "1 at rho=1; rho^-3 at r=rho*R_s",
            "status": "CONDITIONAL_MATH_CLOSED_AFTER_A_SURFACE_EXISTS",
            "needed_before_claim": "A_surface must first be parent-owned",
            "source_ref": "RGT4483_1 through RGT4483_5",
            "valid_for_claim": False,
        },
        {
            "input_id": "FSI4483_1_Pi_J2_metric",
            "symbol": "Pi_J2_metric",
            "definition": "projection kernel from MTS finite l=2 residual variables into the public metric P2 amplitude",
            "formula_or_value": "MISSING",
            "status": "MISSING_PUBLIC_METRIC_PROJECTION_KERNEL",
            "needed_before_claim": "derive from parent metric/coframe/readout variation, not by setting it to one",
            "source_ref": "P8_Y5_R2FR_3171_PROFILE_OWNER_AUDIT.csv; P8_Y5_R2FR_4482_OWNER_INPUT_ROWS.csv",
            "valid_for_claim": False,
        },
        {
            "input_id": "FSI4483_2_T_source",
            "symbol": "T_source",
            "definition": "source-domain transfer/universality map from the existing K2 lane to the solar exterior l=2 source lane",
            "formula_or_value": "MISSING",
            "status": "MISSING_SOURCE_DOMAIN_TRANSFER_OR_SOLAR_K2_CONSTRUCTION",
            "needed_before_claim": "direct solar construction or source-universality theorem",
            "source_ref": "P8_Y5_R2FR_3169_SOLAR_J2_EQUIVALENT_TRANSFER.csv; P8_Y5_R2FR_4482_OWNER_INPUT_ROWS.csv",
            "valid_for_claim": False,
        },
        {
            "input_id": "FSI4483_3_Upsilon_J2",
            "symbol": "Upsilon_J2",
            "definition": "composite transfer from K2*C_K2_unit to solar-surface public metric P2 amplitude",
            "formula_or_value": "Upsilon_J2 = Pi_J2_metric*T_source*G_ext_l2_surface",
            "status": "PARTLY_SIMPLIFIED_GREEN_FACTOR_NOT_PARENT_OWNED",
            "needed_before_claim": "Pi_J2_metric and T_source still need parent signatures or source-backed bounds",
            "source_ref": "P8_Y5_R2FR_3171_UPSILON_J2_TRANSFER_CONTRACT.csv",
            "valid_for_claim": False,
        },
        {
            "input_id": "FSI4483_4_J2eff_transfer",
            "symbol": "J2_eff",
            "definition": "solar quadrupole equivalent after the composite transfer is supplied",
            "formula_or_value": f"J2_eff = Upsilon_J2*K2*{c_k2_unit:.15e}*rho^3/{two_epsilon:.15e}",
            "status": "DERIVED_SYMBOLIC_TRANSFER_NONCLAIM",
            "needed_before_claim": "Upsilon_J2 value or bound",
            "source_ref": "P8_Y5_R2FR_4482_UPSILON_J2_TRANSFER_SCORER.csv",
            "valid_for_claim": False,
        },
        {
            "input_id": "FSI4483_5_K2_half_range_bound",
            "symbol": "K2_bound_half_range",
            "definition": "3170 rough half-range pressure row with explicit composite transfer kernel",
            "formula_or_value": f"K2 <= {corrected_half:.15e}*rho^-3/|Pi_J2_metric*T_source*G_ext_l2_surface|",
            "status": "CONDITIONAL_PRESSURE_ROW_ONLY",
            "needed_before_claim": "cannot score while Pi_J2_metric*T_source is missing",
            "source_ref": "P8_Y5_R2FR_3170_CORRECTED_J2EFF_K2_BOUNDS.csv",
            "valid_for_claim": False,
        },
        {
            "input_id": "FSI4483_6_residual_l2_vector",
            "symbol": "S_TF_extra",
            "definition": "fair finite l=2 residual after GR baseline subtraction",
            "formula_or_value": "abs(S_TF_extra)<=||W_STF||_1(||K2||||DeltaJ2||+||K2X||||P2R_extra||+||H2||||Deltah2||)",
            "status": "SCORER_SHAPE_IMPORTED_INPUTS_MISSING",
            "needed_before_claim": "W_STF, DeltaJ2, P2R_extra and Deltah2 envelopes",
            "source_ref": "P8_Y5_PARENT_QLOC_1955_RESIDUAL_L2_BOUND_LEDGER.csv",
            "valid_for_claim": False,
        },
        {
            "input_id": "FSI4483_7_no_smuggling_rule",
            "symbol": "claim_guardrail",
            "definition": "do not replace a missing parent owner by a convenient normalization",
            "formula_or_value": "Pi_J2_metric=1, T_source=1, or Upsilon_J2=1 are claims unless parent-signed",
            "status": "GUARDRAIL_ACTIVE",
            "needed_before_claim": "all owner clauses close or every surviving residual is separately bounded",
            "source_ref": "MOC4483_0 through MOC4483_5",
            "valid_for_claim": False,
        },
    ]


def decision_ledger_rows(next_target: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4483_0_radial_green",
            "finding": "the public exterior l=2 radial Green/profile theorem is derived",
            "reason": "Laplace/linearized-EH exterior equation gives r^2 and r^-3; asymptotic flatness selects r^-3",
            "effect": "Green_profile is no longer a vague missing object; it is conditional on owning A_surface",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4483_1_owner_split",
            "finding": "the missing coupling is now split into exact parent owner clauses",
            "reason": "Pi_J2_metric and T_source cannot be set to one without proving metric projection and source-domain transfer",
            "effect": "Upsilon_J2 reduces to Pi_J2_metric*T_source on the surface once the public Green amplitude is owned",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4483_2_finite_branch",
            "finding": "the finite scorer input pack is sharper but still nonclaim",
            "reason": "K2 half-range pressure has the exact composite-transfer denominator and residual-l2 scorer shape",
            "effect": "next work should attack parent exterior operator/metric projection before collecting more bound tables",
            "next_action": next_target,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(
    sources: List[Dict[str, object]],
    green_rows: List[Dict[str, object]],
    owner_rows: List[Dict[str, object]],
    scorer_rows: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "CG4483_0_sources",
            "gate": "all cited source paths and needles exist",
            "gate_pass": all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources),
            "claim_allowed": False,
            "detail": "source hygiene only; does not make a physics claim",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4483_1_public_green_theorem",
            "gate": "public exterior r^-3 theorem is derived",
            "gate_pass": any(row.get("theorem_id") == "RGT4483_5_verdict" for row in green_rows),
            "claim_allowed": False,
            "detail": "conditional math pass in public channel",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4483_2_parent_operator_signed",
            "gate": "MTS parent exterior operator matches public l=2 Laplace/EH channel",
            "gate_pass": False,
            "claim_allowed": False,
            "detail": "MOC4483_0 remains missing",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4483_3_projection_and_source_signed",
            "gate": "Pi_J2_metric and T_source are parent-owned or source-bounded",
            "gate_pass": False,
            "claim_allowed": False,
            "detail": "Pi_J2_metric and T_source remain explicit missing owner rows",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4483_4_finite_residual_inputs_ready",
            "gate": "residual-l2 envelopes are numeric/source-backed",
            "gate_pass": False,
            "claim_allowed": False,
            "detail": "W_STF, DeltaJ2, P2R_extra and Deltah2 remain missing",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4483_5_no_generated_claim_rows",
            "gate": "generated rows remain private nonclaim",
            "gate_pass": all(
                str(row.get("valid_for_claim")).lower() == "false"
                for group in [sources, green_rows, owner_rows, scorer_rows]
                for row in group
            ),
            "claim_allowed": False,
            "detail": "no local-GR, PPN, J2, clock, orbital, R10 or EM claim is promoted",
            "valid_for_claim": False,
        },
    ]
