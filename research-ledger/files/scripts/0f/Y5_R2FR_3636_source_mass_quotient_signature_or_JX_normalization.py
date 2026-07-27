from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3636"
BRANCH_ID = "MTS_R2FR_Y5_SOURCE_MASS_QUOTIENT_SIGNATURE_OR_JX_NORMALIZATION_3636"
DOC = ROOT / "3636-Y5-R2FR-source-mass-quotient-signature-or-JX-normalization.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="replace")


def out_paths() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3636_SOURCE_REGISTER.csv",
        "quotient_signature": RESIDUALS / "P8_Y5_R2FR_3636_SOURCE_MASS_QUOTIENT_SIGNATURE.csv",
        "signature_audit": RESIDUALS / "P8_Y5_R2FR_3636_PARENT_SIGNATURE_AUDIT.csv",
        "jx_normalization": RESIDUALS / "P8_Y5_R2FR_3636_JX_NORMALIZATION_GATE.csv",
        "comparator_channel": RESIDUALS / "P8_Y5_R2FR_3636_FIRST_COMPARATOR_CHANNEL.csv",
        "decision_gates": RESIDUALS / "P8_Y5_R2FR_3636_DECISION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3636_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3636_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_source_mass_quotient_or_JX_normalization_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3636_VALIDATION.csv",
    }


def source_rows(t: str) -> list[dict[str, object]]:
    sources = [
        (
            "handoff_3635",
            RESIDUALS / "P8_Y5_R2FR_3635_NEXT_TARGET.csv",
            "source-mass quotient signature",
            "3635 selected source-mass quotient signature versus JX normalization.",
        ),
        (
            "jx_row_3635",
            RESIDUALS / "P8_Y5_R2FR_3635_JX_SOURCE_RESIDUAL_ROW.csv",
            "not_scoreable_until_field_normalization_projection_and_units",
            "symbolic JX source row that 3636 normalizes.",
        ),
        (
            "component_gate_3635",
            RESIDUALS / "P8_Y5_R2FR_3635_SOURCE_READOUT_COMPONENT_GATE.csv",
            "partial_Z(GM_obs)",
            "source/readout subcomponent gate.",
        ),
        (
            "constant_gm_zero_attempt",
            RESIDUALS / "P8_CONSTANT_GM_ZERO_THEOREM_ATTEMPT.csv",
            "mu_obs = G_eff M_eff",
            "measured-GM identity and open derivative-hair premises.",
        ),
        (
            "constant_gm_runner",
            RESIDUALS / "P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv",
            "P8_species_source_charge",
            "existing source-normalization residual runner rows.",
        ),
        (
            "source_norm_template",
            RESIDUALS / "P8_source_normalization_residual_vector_TEMPLATE.csv",
            "P8_species_source_charge",
            "template definitions for source-normalization comparator channels.",
        ),
        (
            "charge_current_attempt",
            RESIDUALS / "P8_charge_current_equality_DIRECT_ATTEMPT.csv",
            "CC3_projected_mass_current",
            "charge-current route for source mass and measured GM.",
        ),
        (
            "charge_current_residuals",
            RESIDUALS / "P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv",
            "Delta_PiM",
            "residual decomposition if charge-current equality fails.",
        ),
        (
            "mass_flux_contract",
            RESIDUALS / "P8_mass_flux_projector_Euler_calibration_CONTRACT.csv",
            "MF5_absolute_calibration",
            "mass flux, PiM, and absolute measured-GM calibration contract.",
        ),
        (
            "pim_contract",
            RESIDUALS / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
            "PM6_flux_closure_requires_Ward_or_Euler",
            "Pi_M algebra and flux-closure contract.",
        ),
        (
            "hamiltonian_measure_contract",
            RESIDUALS / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
            "HSM541_5_Gauss_orbital_readout",
            "Hamiltonian source-measure and Gauss/orbital readout contract.",
        ),
    ]
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "needle": needle,
            "needle_found": contains(path, needle),
            "role": role,
        }
        for source_id, path, needle, role in sources
    ]


def quotient_signature_rows(t: str) -> list[dict[str, object]]:
    rows = [
        {
            "signature_id": "SMQ3636_0_decomposition",
            "object": "measured source monopole",
            "required_identity": "mu_obs = G_eff M_eff(1+epsilon_mu)",
            "derivation": "This is the source-normalization identity already present in the constant-GM runner; it separates coupling, conserved source charge, and extra mass-channel hair.",
            "quotient_zero_condition": "partial_X ln G_eff = partial_X ln M_eff = partial_X ln(1+epsilon_mu) = 0 componentwise",
            "status": "IDENTITY_AVAILABLE_NOT_ZERO",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "signature_id": "SMQ3636_1_dimensionless_source_charge",
            "object": "beta_X_source",
            "required_identity": "beta_X^H := partial_{X_N} ln mu_obs = partial_{X_N} ln G_eff + partial_{X_N} ln M_eff + partial_{X_N} ln(1+epsilon_mu)",
            "derivation": "Normalize the X/Z direction to a dimensionless coordinate X_N. Then beta_X is the source coupling that feeds J_X and source-charge residuals.",
            "quotient_zero_condition": "beta_X^H=0 for every source body/material/channel, with no cancellation credit unless parent identity proves it",
            "status": "DERIVED_NORMALIZED_COUPLING_DEFINITION",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "signature_id": "SMQ3636_2_projected_mass",
            "object": "M_eff",
            "required_identity": "M_eff = integral_{S or Sigma} Pi_M J_H with Pi_M parent-derived before readout",
            "derivation": "This is the charge-current route: the mass used in Newtonian/orbital calibration must be the same parent Hilbert/Ward source charge, not a fitted orbital denominator.",
            "quotient_zero_condition": "partial_X Pi_M=0, partial_X J_H=0 in the fibre direction, and d(Pi_M J_H)=0 in the compact exterior",
            "status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "signature_id": "SMQ3636_3_GM_Gauss_readout",
            "object": "GM_obs",
            "required_identity": "mu_obs=G_eff M_eff equals the Poisson/Gauss/orbital monopole in the same observed frame",
            "derivation": "A closed Hamiltonian/source charge is not enough; it must calibrate to the slow-particle inverse-square readout without importing orbital GM as a premise.",
            "quotient_zero_condition": "constant universal G_eff, absolute calibration, no radial/range hair, and no extra mass-channel charge",
            "status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "signature_id": "SMQ3636_4_source_zero_theorem",
            "object": "J_X_source",
            "required_identity": "J_X_source = rho_H beta_X^H plus geometry/boundary terms after normalization",
            "derivation": "If beta_X^H=0 and geometry/boundary components vanish, the source current from 3635 is zero.",
            "quotient_zero_condition": "M_obs=M_bar(q), G_obs=G_bar(q), B_obs=B_bar(q) or proper/exact",
            "status": "THEOREM_CONDITIONAL_NOT_LIVE",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            **row,
        }
        for row in rows
    ]


def signature_audit_rows(t: str) -> list[dict[str, object]]:
    rows = [
        {
            "audit_id": "SMA3636_0_Geff",
            "required_clause": "G_eff/kappa_eff is parent-fixed, universal, derivative-silent, and range-blind",
            "source_anchor": "Z1_global_coupling_superselection; HSM541_6_constant_universal_G",
            "current_result": "OPEN_NOT_PARENT_DERIVED",
            "residual_if_failed": "dln_Geff_dt; eta_source_AB; alpha(lambda); delta_frame_source",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "SMA3636_1_Meff_flux",
            "required_clause": "M_eff is a parent projected Hilbert/Ward source charge with d(Pi_M J_H)=0",
            "source_anchor": "Z2_calibrated_PiM_flux_conservation; CC3; MF2; PM6",
            "current_result": "OPEN_NOT_PARENT_DERIVED",
            "residual_if_failed": "dln_Meff_dt; partial_r_ln_mu_obs; Delta_PiM; Delta_flux",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "SMA3636_2_mu_extra",
            "required_clause": "epsilon_mu=0 or universal derivative-free calibration with no active boundary/bulk/domain/memory/non-EH mass charge",
            "source_anchor": "Z3_mu_extra_zero_or_universal_constant; CC6; MF6",
            "current_result": "FAILED_MISSING_COEFFICIENT_VECTOR",
            "residual_if_failed": "mu_extra_boundary_bulk_domain; R11_source_normalization_operator; alpha3; xi",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "SMA3636_3_species",
            "required_clause": "source charge is species/material blind",
            "source_anchor": "Z4_species_blind_source_action; P8_species_source_charge",
            "current_result": "OPEN_NOT_PARENT_DERIVED",
            "residual_if_failed": "eta_source_AB",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "SMA3636_4_radial_range",
            "required_clause": "measured source strength has no radial/range-dependent hair",
            "source_anchor": "Z5_no_radial_or_range_hair; P8_radial_source_hair; P8_range_dependence",
            "current_result": "OPEN_NOT_PARENT_DERIVED",
            "residual_if_failed": "partial_r_ln_mu_obs; alpha(lambda)",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "SMA3636_5_frame_calibration",
            "required_clause": "source variation and matter/orbit readout use one observed frame",
            "source_anchor": "Z6_same_frame_source_pullback; CC1; Delta_frame",
            "current_result": "PARTIAL_CONDITIONAL_ONLY",
            "residual_if_failed": "delta_frame_source; clock/source calibration split",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "SMA3636_6_absolute_Gauss",
            "required_clause": "Hamiltonian/source charge equals Poisson/Gauss/orbital monopole without circular orbital-GM import",
            "source_anchor": "CC7; MF5; HSM541_5",
            "current_result": "OPEN_NOT_PARENT_DERIVED",
            "residual_if_failed": "Delta_cal; partial_r_ln_mu_obs; alpha(lambda)",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "SMA3636_7_verdict",
            "required_clause": "M_obs=M_bar(q) is parent-signed for rest mass, GM, Hamiltonian source, and orbit readout",
            "source_anchor": "3635 next target",
            "current_result": "SOURCE_MASS_QUOTIENT_NOT_SIGNED_JX_NORMALIZATION_REQUIRED",
            "residual_if_failed": "J_X_source normalized source-charge row active",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            **row,
        }
        for row in rows
    ]


def jx_normalization_rows(t: str) -> list[dict[str, object]]:
    rows = [
        {
            "norm_id": "JXN3636_0_field_coordinate",
            "quantity": "X_N",
            "definition": "X_N := X / X_* is the dimensionless normalized fibre/source-coupling coordinate",
            "units": "dimensionless",
            "needed_input": "field scale X_* or parent canonical normalization from the X/Z kinetic term",
            "score_status": "symbolic_normalization_declared_scale_missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "norm_id": "JXN3636_1_source_charge",
            "quantity": "beta_X^H",
            "definition": "beta_X^H := partial_{X_N} ln mu_obs = partial_{X_N} ln G_eff + partial_{X_N} ln M_eff + partial_{X_N} ln(1+epsilon_mu)",
            "units": "dimensionless",
            "needed_input": "component derivatives or theorem-zero certificates for G_eff, M_eff, epsilon_mu",
            "score_status": "formula_ready_components_missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "norm_id": "JXN3636_2_source_current_density",
            "quantity": "J_X_source",
            "definition": "J_X_source = rho_H beta_X^H / X_* for dimensional X, or rho_H beta_X^H for dimensionless X_N",
            "units": "energy_density_per_X or energy_density_for_dimensionless_XN",
            "needed_input": "rho_H convention, X_* or canonical field units, source support/worldtube",
            "score_status": "symbolic_current_law_units_not_fixed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "norm_id": "JXN3636_3_test_charge",
            "quantity": "beta_X^T",
            "definition": "beta_X^T := partial_{X_N} ln m_test_obs for the test body/clock/matter readout",
            "units": "dimensionless",
            "needed_input": "test-body matter pullback and species/material marker map",
            "score_status": "needed_for_force_comparison_missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "norm_id": "JXN3636_4_force_projection",
            "quantity": "alpha_X(lambda_X)",
            "definition": "alpha_X(lambda_X) = K_X beta_X^H beta_X^T with lambda_X=sqrt(Z_X/M_X^2), after parent Green-function normalization",
            "units": "dimensionless function of range",
            "needed_input": "K_X, beta_X^H, beta_X^T, lambda_X, R10 bound curve",
            "score_status": "not_scoreable_until_operator_and_charges_numeric_or_zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "norm_id": "JXN3636_5_source_normalization_vector",
            "quantity": "D_a ln mu_obs",
            "definition": "D_a ln mu_obs = D_a ln G_eff + D_a ln M_eff + D_a ln(1+epsilon_mu) for a in {t,r,A,lambda,frame}",
            "units": "yr^-1, inverse_length, dimensionless, or range-dependent by channel",
            "needed_input": "channel derivatives and no-cancellation parent identity if terms are combined",
            "score_status": "runner_skeleton_ready_but_values_missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            **row,
        }
        for row in rows
    ]


def comparator_rows(t: str) -> list[dict[str, object]]:
    rows = [
        {
            "comparator_id": "CMP3636_0_first_channel_species_source_charge",
            "rank": 1,
            "channel": "P8_species_source_charge",
            "observable_link": "eta_source_AB;eta_WEP_source_charge",
            "prediction_formula": "eta_source_AB = 2|beta_X^A-beta_X^B|/|2+beta_X^A+beta_X^B|, small-charge limit approx |beta_X^A-beta_X^B|",
            "bound_or_target": "2.8e-15 or derived universal source charge from existing template",
            "why_first": "dimensionless source-charge channel tests whether beta_X is species/material blind without needing an R10 curve first",
            "missing_to_score": "beta_X^A, beta_X^B, test/source material map, parent field normalization if beta defined from dimensional X",
            "source_paths": f"{RESIDUALS / 'P8_source_normalization_residual_vector_TEMPLATE.csv'};{RESIDUALS / 'P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv'}",
            "score_status": "comparator_selected_not_numeric",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "comparator_id": "CMP3636_1_second_channel_Gdot",
            "rank": 2,
            "channel": "P8_Geff_time_drift plus P8_Meff_conservation",
            "observable_link": "Gdot_over_G",
            "prediction_formula": "d_t ln mu_obs = d_t ln G_eff + d_t ln M_eff + d_t ln(1+epsilon_mu)",
            "bound_or_target": "9.6e-15 yr^-1 or derived zero from existing template",
            "why_first": "time drift can score a source-normalization leak even when composition maps are unavailable",
            "missing_to_score": "time derivative profile and separation of G_eff, M_eff, epsilon_mu",
            "source_paths": f"{RESIDUALS / 'P8_source_normalization_residual_vector_TEMPLATE.csv'};{RESIDUALS / 'P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv'}",
            "score_status": "comparator_available_values_missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "comparator_id": "CMP3636_2_third_channel_R10",
            "rank": 3,
            "channel": "P8_range_dependence",
            "observable_link": "delta_G_or_fifth_force_yukawa",
            "prediction_formula": "alpha_X(lambda_X)=K_X beta_X^H beta_X^T",
            "bound_or_target": "verified alpha(lambda) curve or derived zero",
            "why_first": "this is the direct R10/fifth-force channel, but it needs more machinery than eta_source_AB",
            "missing_to_score": "K_X, lambda_X, beta_X charges, real bound curve",
            "source_paths": f"{RESIDUALS / 'P8_source_normalization_residual_vector_TEMPLATE.csv'};{RESIDUALS / 'P8_Y5_R10_669_R10_R11_RESIDUAL_VECTOR.csv'}",
            "score_status": "deferred_curve_and_operator_missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            **row,
        }
        for row in rows
    ]


def decision_rows(t: str) -> list[dict[str, object]]:
    rows = [
        {
            "decision_id": "DEC3636_0_source_quotient",
            "decision": "Measured source mass/GM/Hamiltonian readout is not parent-signed as q-data in the live corpus.",
            "status": "SOURCE_MASS_QUOTIENT_NOT_SIGNED",
            "next_action": "do not claim Newton/local-GR source normalization from source descent alone",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3636_1_jx_normalization",
            "decision": "J_X_source now has a normalized charge language: beta_X=partial_XN ln mu_obs and J_X_source=rho_H beta_X / X_*.",
            "status": "JX_NORMALIZATION_SYMBOLICALLY_DEFINED",
            "next_action": "fill beta_X component derivatives or prove beta_X=0 from parent quotient data",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3636_2_first_comparator",
            "decision": "The first comparator channel should be source-charge WEP eta_source_AB, with Gdot second and R10 alpha(lambda) third.",
            "status": "FIRST_COMPARATOR_SELECTED",
            "next_action": "next target should derive species/material blindness or fill beta_X^A-beta_X^B row",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            **row,
        }
        for row in rows
    ]


def status_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "SOURCE_MASS_QUOTIENT_UNSIGNED_JX_NORMALIZATION_DEFINED_FIRST_COMPARATOR_SELECTED",
            "summary": "3636 attempts the source-mass quotient signature and finds the live corpus still does not parent-sign measured source mass/GM/Hamiltonian/orbit readout as q-data. The fallback is now sharper: normalize the source coupling with beta_X=partial_XN ln mu_obs and J_X_source=rho_H beta_X/X_*. The first comparator channel is source-charge WEP eta_source_AB, before Gdot and R10 alpha(lambda).",
            "claim_ceiling": "no source-zero, Newton, local-GR, R10/R11, WEP, or PPN claim is allowed from 3636",
            "useful_result": "source coupling is now a beta_X charge problem with a selected first comparator, not just a missing coupling",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3636_0",
            "target_doc": "3637-Y5-R2FR-species-blind-source-charge-zero-or-betaX-row.md",
            "target_script": "scripts/Y5_R2FR_3637_species_blind_source_charge_zero_or_betaX_row.py",
            "objective": "try to derive beta_X^A=beta_X^B for source/test species from parent matter/source quotient data; if not, create a beta_X species-difference row for eta_source_AB with units, material map, and bound target",
            "success_gate": "either species/material blindness is theorem-zero from q-data, or eta_source_AB has a nonclaim executable beta_X difference skeleton tied to the 2.8e-15 target",
            "reason": "3636 selects source-charge WEP as the first comparator for normalized J_X_source.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def canonical_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "canonical_object": "source_mass_quotient_or_JX_normalization",
            "canonical_status": "SOURCE_MASS_QUOTIENT_UNSIGNED_BETAX_DEFINED",
            "usable_result": "beta_X^H := partial_XN ln mu_obs = partial_XN ln G_eff + partial_XN ln M_eff + partial_XN ln(1+epsilon_mu); J_X_source=rho_H beta_X^H/X_*; first comparator eta_source_AB.",
            "hard_block": "derive species/material blind beta_X or fill beta_X^A-beta_X^B row",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def md(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def table(rows: list[dict[str, object]], cols: list[str]) -> str:
    output = ["| " + " | ".join(cols) + " |", "| " + " | ".join("---" for _ in cols) + " |"]
    for row in rows:
        output.append("| " + " | ".join(md(row.get(col, "")) for col in cols) + " |")
    return "\n".join(output)


def write_doc(
    src: list[dict[str, object]],
    signature: list[dict[str, object]],
    audit: list[dict[str, object]],
    normalization: list[dict[str, object]],
    comparators: list[dict[str, object]],
    decisions: list[dict[str, object]],
    status: list[dict[str, object]],
    nxt: list[dict[str, object]],
) -> None:
    text = "\n\n".join(
        [
            "# 3636 Y5 R2FR source-mass quotient signature or JX normalization",
            f"**Status:** {status[0]['summary']}",
            f"**Claim ceiling:** {status[0]['claim_ceiling']}.",
            "## Main result",
            (
                "The source-mass route now has a clean signature:\n\n"
                "```text\n"
                "mu_obs = G_eff M_eff(1+epsilon_mu)\n"
                "beta_X^H := partial_{X_N} ln(mu_obs)\n"
                "          = partial_{X_N} ln(G_eff)\n"
                "          + partial_{X_N} ln(M_eff)\n"
                "          + partial_{X_N} ln(1+epsilon_mu)\n"
                "J_X_source = rho_H beta_X^H / X_*.\n"
                "```\n\n"
                "If `M_obs` is truly quotient-owned, `beta_X^H=0`. If not, `beta_X` is the normalized source charge to test. The least machinery comparator is now source-charge WEP, not R10 first."
            ),
            "## Source register",
            table(src, ["source_id", "path", "exists", "needle_found", "role"]),
            "## Source-mass quotient signature",
            table(signature, ["signature_id", "object", "required_identity", "derivation", "quotient_zero_condition", "status"]),
            "## Parent signature audit",
            table(audit, ["audit_id", "required_clause", "source_anchor", "current_result", "residual_if_failed"]),
            "## JX normalization gate",
            table(normalization, ["norm_id", "quantity", "definition", "units", "needed_input", "score_status"]),
            "## First comparator channel",
            table(comparators, ["comparator_id", "rank", "channel", "observable_link", "prediction_formula", "bound_or_target", "why_first", "missing_to_score", "score_status"]),
            "## Decisions",
            table(decisions, ["decision_id", "decision", "status", "next_action"]),
            "## Next target",
            table(nxt, ["target_doc", "target_script", "objective", "success_gate"]),
        ]
    )
    DOC.write_text(text + "\n", encoding="utf-8")


def validate(outputs: dict[str, Path], src: list[dict[str, object]]) -> list[dict[str, object]]:
    t = now()
    rows: list[dict[str, object]] = []

    def add(validation_id: str, ok: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": t,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "validation_id": validation_id,
                "result": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )

    add("VAL3636_0_sources_exist", all(bool(row["exists"]) for row in src), "all cited source paths exist")
    add("VAL3636_1_needles_found", all(bool(row["needle_found"]) for row in src), "all source needles found")
    pre = {name: path for name, path in outputs.items() if name != "validation"}
    add("VAL3636_2_outputs_exist", all(path.exists() for path in pre.values()) and DOC.exists(), "all pre-validation outputs and doc written")

    details = []
    parse_ok = True
    for name, path in pre.items():
        try:
            count = len(read_csv(path))
            details.append(f"{name}:{count}")
            parse_ok = parse_ok and count > 0
        except Exception as exc:
            details.append(f"{name}:ERR:{exc}")
            parse_ok = False
    add("VAL3636_3_csv_parse", parse_ok, "; ".join(details))

    signature = read_csv(outputs["quotient_signature"])
    audit = read_csv(outputs["signature_audit"])
    normalization = read_csv(outputs["jx_normalization"])
    comparators = read_csv(outputs["comparator_channel"])
    decisions = read_csv(outputs["decision_gates"])
    status = read_csv(outputs["status"])
    nxt = read_csv(outputs["next_target"])

    add("VAL3636_4_betax_definition_present", any("beta_X^H" in row["required_identity"] and "partial_{X_N} ln mu_obs" in row["required_identity"] for row in signature), "beta_X source-charge definition present")
    add("VAL3636_5_audit_blocks_source_quotient", any(row["current_result"] == "SOURCE_MASS_QUOTIENT_NOT_SIGNED_JX_NORMALIZATION_REQUIRED" for row in audit), "parent signature audit blocks source quotient claim")
    add("VAL3636_6_jx_current_units_gate", any(row["quantity"] == "J_X_source" and "rho_H" in row["definition"] for row in normalization), "JX source current normalization row present")
    add("VAL3636_7_force_projection_deferred", any(row["quantity"] == "alpha_X(lambda_X)" and "not_scoreable" in row["score_status"] for row in normalization), "R10 force projection correctly deferred")
    add("VAL3636_8_first_comparator_species", bool(comparators) and comparators[0]["channel"] == "P8_species_source_charge" and "eta_source_AB" in comparators[0]["observable_link"], "source-charge WEP selected as first comparator")
    add("VAL3636_9_decisions_record_progress", any(row["status"] == "JX_NORMALIZATION_SYMBOLICALLY_DEFINED" for row in decisions), "decision table records JX normalization progress")
    add("VAL3636_10_nonclaim_all_outputs", all(row["valid_for_claim"].lower() == "false" for row in signature + audit + normalization + comparators + decisions + status + nxt), "all generated rows remain nonclaim")
    leaks = list(FORMALIZATION.rglob("*3636*")) if FORMALIZATION.exists() else []
    add("VAL3636_11_no_formalization_leak", not leaks, "no 3636 files in formalization-workbench")
    add("VAL3636_12_next_target_written", bool(nxt) and "3637" in nxt[0]["target_doc"], "3637 species-blind/betaX target written")
    add("VAL3636_13_doc_written", DOC.exists() and "beta_X" in DOC.read_text(encoding="utf-8", errors="replace"), "checkpoint doc written with beta_X source charge")
    add("VAL3636_14_canonical_status_written", outputs["canonical_status"].exists() and "SOURCE_MASS_QUOTIENT_UNSIGNED_BETAX_DEFINED" in outputs["canonical_status"].read_text(encoding="utf-8", errors="replace"), "canonical source mass/JX status written")
    return rows


def main() -> None:
    t = now()
    outputs = out_paths()
    src = source_rows(t)
    signature = quotient_signature_rows(t)
    audit = signature_audit_rows(t)
    normalization = jx_normalization_rows(t)
    comparators = comparator_rows(t)
    decisions = decision_rows(t)
    status = status_rows(t)
    nxt = next_rows(t)
    canonical = canonical_rows(t)

    write_csv(outputs["source_register"], src)
    write_csv(outputs["quotient_signature"], signature)
    write_csv(outputs["signature_audit"], audit)
    write_csv(outputs["jx_normalization"], normalization)
    write_csv(outputs["comparator_channel"], comparators)
    write_csv(outputs["decision_gates"], decisions)
    write_csv(outputs["status"], status)
    write_csv(outputs["next_target"], nxt)
    write_csv(outputs["canonical_status"], canonical)
    write_doc(src, signature, audit, normalization, comparators, decisions, status, nxt)

    validation = validate(outputs, src)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3636 validation failed: {failures}")
    print(f"wrote 3636 checkpoint with {len(validation)} validation checks")


if __name__ == "__main__":
    main()
