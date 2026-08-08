from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
DOC = ROOT / "3409-Y5-R2FR-nonEH-residue-bound-pack-relative-to-GR-pole-under-AX1090.md"

SOURCES = {
    "doc_3408": ROOT / "3408-Y5-R2FR-minimum-GR-pole-Hhh-Rh-Jh-derivation-under-AX1090.md",
    "min_gr_pole_3408": OUT / "P8_Y5_R2FR_3408_MINIMUM_GR_POLE_ROW.csv",
    "blockers_3408": OUT / "P8_Y5_R2FR_3408_CLAIM_BLOCKER_AUDIT.csv",
    "next_3408": OUT / "P8_Y5_R2FR_3408_NEXT_TARGET.csv",
    "residue_bound_interface_3406": OUT / "P8_Y5_R2FR_3406_RESIDUE_BOUND_INTERFACE.csv",
    "mode_family_triage_3406": OUT / "P8_Y5_R2FR_3406_MODE_FAMILY_TRIAGE.csv",
    "derivative_order_law_3405": OUT / "P8_Y5_R2FR_3405_DERIVATIVE_ORDER_BOUND_LAW.csv",
    "qloc_guard_3403": OUT / "P8_Y5_R2FR_3403_QLOC_BETA_ALPHA_GUARD.csv",
    "beta_envelope_531": OUT / "P8_Y5_BETA_ENVELOPE_COMPONENTS.csv",
    "r11_beta_vector_530": OUT / "P8_Y5_R11_BETA_COMPONENT_VECTOR.csv",
    "local_bound_claims": LOCAL_BOUNDS / "local_bound_claims.csv",
    "r10_alpha_digitized": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3409_SOURCE_REGISTER.csv",
    "gr_pole_denominator": OUT / "P8_Y5_R2FR_3409_GR_POLE_DENOMINATOR.csv",
    "non_eh_residue_channels": OUT / "P8_Y5_R2FR_3409_NON_EH_RESIDUE_CHANNELS.csv",
    "bound_formulas": OUT / "P8_Y5_R2FR_3409_BOUND_FORMULAS.csv",
    "empirical_locks": OUT / "P8_Y5_R2FR_3409_EMPIRICAL_LOCKS.csv",
    "no_cancellation_score_rule": OUT / "P8_Y5_R2FR_3409_NO_CANCELLATION_SCORE_RULE.csv",
    "input_readiness": OUT / "P8_Y5_R2FR_3409_INPUT_READINESS.csv",
    "local_gr_impact": OUT / "P8_Y5_R2FR_3409_LOCAL_GR_IMPACT.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3409_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3409_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3409_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3409_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3409_VALIDATION.csv",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    fields = list(rows[0].keys())
    clean = lambda value: str(value).replace("\n", " ").replace("|", "/")
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(clean(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def load_optional(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    return read_csv(path)


def first_row(rows: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    for row in rows:
        if row.get(key) == value:
            return row
    return {}


QL0 = first_row(load_optional(SOURCES["qloc_guard_3403"]), "guard_id", "QG3403_0_beta_projection")
QL1 = first_row(load_optional(SOURCES["qloc_guard_3403"]), "guard_id", "QG3403_1_alpha3_warning")
QL2 = first_row(load_optional(SOURCES["qloc_guard_3403"]), "guard_id", "QG3403_2_acceptance")


def source_register() -> list[dict[str, Any]]:
    roles = {
        "doc_3408": "narrative derivation of the conditional GR pole row",
        "min_gr_pole_3408": "conditional GR-pole denominator",
        "blockers_3408": "claim blockers that remain live after denominator construction",
        "next_3408": "declared handoff into 3409",
        "residue_bound_interface_3406": "formula-ready residue bounds for spin0, massive spin2, connection and domain/memory channels",
        "mode_family_triage_3406": "R11 family-to-channel triage",
        "derivative_order_law_3405": "four-derivative, extra-field, connection and boundary residual laws",
        "qloc_guard_3403": "q_loc beta-only provisional budget and preferred-frame warning",
        "beta_envelope_531": "local beta envelope components and q_loc warning carry-through",
        "r11_beta_vector_530": "component vector for source/readout/q_loc/vector/domain/boundary risks",
        "local_bound_claims": "local PPN bound source register, used only as nonclaim lock context here",
        "r10_alpha_digitized": "R10 alpha(lambda) candidate/digitized file; must remain nonclaim unless provenance is complete",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": bool_text(path.exists()),
            "role": roles[source_id],
            "valid_for_claim": False,
        }
        for source_id, path in SOURCES.items()
    ]


def gr_pole_denominator() -> list[dict[str, Any]]:
    return [
        {
            "denominator_id": "DGR3409_0_conditional_massless_spin2",
            "definition": "D_GR(k):=abs(R_h H_hh^{-1} J_h)",
            "symbolic_value": "abs(G_ref P^(2)/k^2) after EH second variation, gauge fixing and conserved Hilbert source projection",
            "source_path": str(SOURCES["min_gr_pole_3408"]),
            "current_status": "EXACT_CONDITIONAL_DENOMINATOR_NOT_PARENT_SIGNED",
            "why_nonclaim": "parent action reduction, readout identity, Hilbert+EM adoption, boundary/gauge class and extra residues are not all signed",
            "valid_for_claim": False,
        },
        {
            "denominator_id": "DGR3409_1_common_Gref_lock",
            "definition": "same G_ref must normalize the GR denominator and measured mu=G_ref M_H[Pi_M J_H]",
            "symbolic_value": "kappa0=8*pi*G_ref/c^4",
            "source_path": str(SOURCES["min_gr_pole_3408"]),
            "current_status": "REFERENCE_LOCK_REQUIRED",
            "why_nonclaim": "numeric G derivation is not required, but common-branch ownership of G_ref is required",
            "valid_for_claim": False,
        },
    ]


def non_eh_residue_channels() -> list[dict[str, Any]]:
    denominator = "D_GR(k)=abs(R_h H_hh^{-1} J_h)"
    return [
        {
            "channel_id": "NEH3409_0_spin0_scalar",
            "residue_symbol": "B_0(lambda_0)",
            "mode_families": "R2_fR_scalar_mode; scalar_tensor_class_metric",
            "numerator_definition": "abs(R_0 H_00^{-1} J_0) after source/readout projection",
            "denominator": denominator,
            "required_bound": "min(PPN_gamma_scalar, beta_scalar, R10_alpha(lambda_0), clock/WEP if sourced)",
            "live_risk": "scalar fifth-force or PPN slip if parent does not zero/gap/source-silence it",
            "current_numeric_input": "MISSING_SCALAR_POLE_MASS_RESIDUE_SOURCE_OVERLAP_SCREENING_PROFILE",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "channel_id": "NEH3409_1_massive_spin2_four_derivative",
            "residue_symbol": "B_2(lambda_2)",
            "mode_families": "Ricci_Weyl_squared; four_derivative_metric",
            "numerator_definition": "abs(R_2 H_22^{-1} J_2) including sign/stability/ghost guard",
            "denominator": denominator,
            "required_bound": "min(PPN_gamma_beta, finite_range_spin2, stability_or_ghost_exclusion)",
            "live_risk": "massive spin-2 residue, wrong sign, or finite-range force",
            "current_numeric_input": "MISSING_WEYL_RICCI_COEFFICIENT_POLE_RESIDUE_SIGN_STABILITY_RULE",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "channel_id": "NEH3409_2_connection",
            "residue_symbol": "B_conn",
            "mode_families": "torsion_nonmetricity; metric_affine_connection",
            "numerator_definition": "abs(R_conn H_conn^{-1} J_conn) plus algebraic/projective source leakage",
            "denominator": denominator,
            "required_bound": "min(clock, WEP, lightcone, spin, PPN_connection_projection)",
            "live_risk": "independent connection may affect clocks/light/matter even when metric pole looks GR-like",
            "current_numeric_input": "MISSING_CONNECTION_HESSIAN_HYPERMOMENTUM_READOUT_OVERLAP",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "channel_id": "NEH3409_3_vector_preferred_frame",
            "residue_symbol": "B_V",
            "mode_families": "vector_preferred_frame; domain_aether_like_leakage",
            "numerator_definition": "abs(R_V H_VV^{-1} J_V) projected to alpha1/alpha2/alpha3/xi before beta",
            "denominator": denominator,
            "required_bound": "preferred-frame alpha_i/xi locks before beta promotion",
            "live_risk": "q_loc/domain/vector leakage can look harmless in beta but catastrophic in preferred-frame projections",
            "current_numeric_input": "MISSING_VECTOR_PROFILE_ALPHA_VECTOR_MAP",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "channel_id": "NEH3409_4_domain_memory_bulk",
            "residue_symbol": "B_X(lambda_X)",
            "mode_families": "projector_domain_stress; nonlocal_memory_kernel; bulk_X_force_law",
            "numerator_definition": "abs(R_X H_XX^{-1} J_X) plus boundary flux/local profile/arena projection",
            "denominator": denominator,
            "required_bound": "arena-specific beta/gamma/Gdot/R10/WEP/clock locks with no cancellation credit",
            "live_risk": "cosmology-useful memory/domain variables cannot be imported into local GR unless source-silent, gapped, screened or bounded",
            "current_numeric_input": "MISSING_HX_RX_JX_BOUNDARY_FLUX_LOCAL_PROFILE_ARENA_PROJECTION",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "channel_id": "NEH3409_5_boundary_projector",
            "residue_symbol": "B_boundary",
            "mode_families": "boundary_topological_terms; projector_domain_stress",
            "numerator_definition": "abs(boundary/reference/projector stress response) relative to the EH denominator",
            "denominator": denominator,
            "required_bound": "zero-flux/topological/source-blind theorem or beta/alpha3/xi bound",
            "live_risk": "edge or reference terms can re-enter as monopole, flux, stress, or readout terms",
            "current_numeric_input": "MISSING_BOUNDARY_NO_FLUX_NO_STRESS_THEOREM_OR_COEFFICIENT",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "channel_id": "NEH3409_6_source_readout",
            "residue_symbol": "B_source_readout",
            "mode_families": "source_normalization_operator; observed_readout_frame",
            "numerator_definition": "abs(source/readout mismatch residue) after measured-GM normalization",
            "denominator": denominator,
            "required_bound": "same observed coframe/readout theorem through O(U^2), or explicit beta/gamma/source bound",
            "live_risk": "the theory can have the right EH pole but compare the wrong public metric/source normalization",
            "current_numeric_input": "MISSING_A_SOURCE_B_SOURCE_SAME_READOUT_THEOREM_THROUGH_OU2",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "channel_id": "NEH3409_7_q_loc",
            "residue_symbol": "B_q_loc",
            "mode_families": "q_loc_Gamma_Khat; source_readout_q_loc",
            "numerator_definition": "physical projection of P_loc(nabla Gamma_eff - div Khat) into beta and preferred-frame vectors",
            "denominator": denominator,
            "required_bound": "beta below bound is not enough; alpha1/alpha2/alpha3/xi projections must be signed",
            "live_risk": "current beta-only value is small but the stored alpha3 warning is enormous if the same projection leaks",
            "current_numeric_input": f"delta_beta={QL0.get('value', 'MISSING')}; alpha3_warning={QL1.get('value', 'MISSING')}; acceptance={QL2.get('status', 'MISSING')}",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def bound_formulas() -> list[dict[str, Any]]:
    return [
        {
            "formula_id": "BF3409_0_spin0",
            "applies_to": "B_0(lambda_0)",
            "inequality": "abs(B_0(lambda_0)) <= min(B_gamma_scalar, B_beta_scalar, B_R10_alpha(lambda_0), B_clock_WEP_if_sourced)",
            "source_path": str(SOURCES["residue_bound_interface_3406"]),
            "required_inputs": "scalar pole mass; residue sign; source/readout overlap; screening/local profile",
            "promotion_guard": "no scalar claim unless numerator and every active empirical lock are numeric, sourced and same-readout",
            "valid_for_claim": False,
        },
        {
            "formula_id": "BF3409_1_massive_spin2",
            "applies_to": "B_2(lambda_2)",
            "inequality": "abs(B_2(lambda_2)) <= min(B_gamma_beta, B_finite_range_spin2, B_stability_ghost)",
            "source_path": str(SOURCES["residue_bound_interface_3406"]),
            "required_inputs": "Weyl/Ricci coefficient; massive spin2 pole; residue; sign/stability rule",
            "promotion_guard": "wrong-sign or ghost residue is not rescued by fitting; it must be excluded or demoted",
            "valid_for_claim": False,
        },
        {
            "formula_id": "BF3409_2_connection",
            "applies_to": "B_conn",
            "inequality": "abs(B_conn) <= min(B_clock, B_WEP, B_lightcone, B_spin, B_PPN_connection)",
            "source_path": str(SOURCES["residue_bound_interface_3406"]),
            "required_inputs": "torsion/nonmetricity Hessian; hypermomentum/source coupling; clock/light/readout overlap",
            "promotion_guard": "Levi-Civita reduction must be proved or connection residue must be bounded in each local arena",
            "valid_for_claim": False,
        },
        {
            "formula_id": "BF3409_3_domain_memory_bulk",
            "applies_to": "B_X(lambda_X)",
            "inequality": "abs(B_X(lambda_X)) := abs(R_X H_X^{-1} J_X) / abs(R_h H_hh^{-1} J_h) <= B_arena_X",
            "source_path": str(SOURCES["residue_bound_interface_3406"]),
            "required_inputs": "H_X; R_X; J_X; boundary flux; local profile; arena projection",
            "promotion_guard": "cosmology memory success does not prove local silence; local compact limit must be separately signed",
            "valid_for_claim": False,
        },
        {
            "formula_id": "BF3409_4_four_derivative",
            "applies_to": "metric four-derivative residue",
            "inequality": "abs(E_4)/abs(E_EH) <= C_4*(ell_4/L_local)^2 after source/readout projection",
            "source_path": str(SOURCES["derivative_order_law_3405"]),
            "required_inputs": "C_4 sign/norm; ell_4 or mass scale; weak-field projection; boundary status",
            "promotion_guard": "if not exactly absent/topological, the scale suppression must be numeric and source-backed",
            "valid_for_claim": False,
        },
        {
            "formula_id": "BF3409_5_extra_fields",
            "applies_to": "scalar/vector/bulk-X/memory/domain residue",
            "inequality": "abs(E_X)/abs(E_EH) <= abs(Q_X)*abs(K_X)/(M_X^2 L_local^2)+contact/readout terms",
            "source_path": str(SOURCES["derivative_order_law_3405"]),
            "required_inputs": "Q_X; K_X; M_X^2; source charge; local profile; PPN/fifth-force projection",
            "promotion_guard": "this is the source-backed version of the coupling hunt; no parent-owned numbers means no claim",
            "valid_for_claim": False,
        },
        {
            "formula_id": "BF3409_6_q_loc",
            "applies_to": "B_q_loc",
            "inequality": "beta lane may use abs(delta_beta_q_loc)<=7.8e-5, but promotion requires alpha-vector projection silence",
            "source_path": str(SOURCES["qloc_guard_3403"]),
            "required_inputs": "physical q_loc profile; U^2 conversion; projection/readout normalization; alpha1/alpha2/alpha3/xi vector split",
            "promotion_guard": "stored alpha3 warning blocks local-GR promotion until the q_loc vector split is derived",
            "valid_for_claim": False,
        },
    ]


def empirical_locks() -> list[dict[str, Any]]:
    beta_value = QL0.get("value", "")
    beta_bound = QL0.get("beta_bound", "7.8e-05")
    bound_fraction = QL0.get("bound_fraction", "")
    alpha_warning = QL1.get("value", "")
    return [
        {
            "lock_id": "LOCK3409_0_beta_PPN",
            "arena": "local_PPN_beta",
            "lock_quantity": "abs(beta-1)",
            "numeric_value": beta_bound,
            "units": "dimensionless",
            "source_path": str(SOURCES["qloc_guard_3403"]),
            "status": "BOUND_CONTEXT_AVAILABLE_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "lock_id": "LOCK3409_1_q_loc_beta_budget",
            "arena": "q_loc_beta_lane",
            "lock_quantity": "delta_beta_q_loc",
            "numeric_value": beta_value,
            "units": "dimensionless",
            "source_path": str(SOURCES["qloc_guard_3403"]),
            "status": f"PROVISIONAL_BELOW_BETA_BOUND_fraction_{bound_fraction}",
            "valid_for_claim": False,
        },
        {
            "lock_id": "LOCK3409_2_q_loc_alpha3_warning",
            "arena": "preferred_frame_alpha3_guard",
            "lock_quantity": "q_loc_alpha3_projection_warning",
            "numeric_value": alpha_warning,
            "units": "dimensionless_projection_warning",
            "source_path": str(SOURCES["qloc_guard_3403"]),
            "status": "SEVERE_WARNING_IF_SAME_PROJECTION_APPLIES",
            "valid_for_claim": False,
        },
        {
            "lock_id": "LOCK3409_3_kappa_v_target",
            "arena": "q_loc_normalization",
            "lock_quantity": "kappav_target",
            "numeric_value": QL0.get("kappav_target", "0.000156"),
            "units": "dimensionless_internal_normalization",
            "source_path": str(SOURCES["qloc_guard_3403"]),
            "status": "INTERNAL_TARGET_NOT_CLAIM_INPUT",
            "valid_for_claim": False,
        },
        {
            "lock_id": "LOCK3409_4_R10_alpha_lambda",
            "arena": "short_range_inverse_square",
            "lock_quantity": "alpha_bound(lambda)",
            "numeric_value": "SEE_SOURCE_FILE_IF_PROVENANCE_COMPLETE",
            "units": "dimensionless_alpha_vs_length_lambda",
            "source_path": str(SOURCES["r10_alpha_digitized"]),
            "status": "BOUND_FILE_EXISTS_BUT_3409_TREATS_AS_NONCLAIM_UNTIL_FULL_PROVENANCE_AND_MTS_NUMERATOR_EXIST",
            "valid_for_claim": False,
        },
        {
            "lock_id": "LOCK3409_5_clock_WEP_orbital",
            "arena": "clock_WEP_orbital",
            "lock_quantity": "arena-specific residual upper bounds",
            "numeric_value": "MISSING_CHANNEL_SPECIFIC_PROJECTION",
            "units": "mixed",
            "source_path": str(SOURCES["local_bound_claims"]),
            "status": "SOURCE_REGISTER_CONTEXT_ONLY_NOT_BOUND_TO_RESIDUES",
            "valid_for_claim": False,
        },
    ]


def no_cancellation_score_rule() -> list[dict[str, Any]]:
    return [
        {
            "rule_id": "NCR3409_0_absolute_residue_envelope",
            "rule": "Do not score local GR by cancellation between unrelated non-EH channels.",
            "formula": "Delta_local_abs <= sum_i abs(B_i projected_to_arena)",
            "claim_effect": "A local-GR pass requires every active B_i to be zero, source-silent, gapped/screened, or individually below the relevant lock.",
            "valid_for_claim": False,
        },
        {
            "rule_id": "NCR3409_1_beta_not_enough",
            "rule": "A small beta projection does not promote a branch if alpha_i/xi/source/readout projections are unsigned.",
            "formula": "score_ready_i = numeric_residue_i and sourced_i and same_readout_i and all_active_locks_pass_i",
            "claim_effect": "q_loc remains blocked even though its stored beta-only number is below the beta bound.",
            "valid_for_claim": False,
        },
        {
            "rule_id": "NCR3409_2_GR_pole_denominator_only",
            "rule": "The conditional EH/GR pole is used only as a denominator for residue ratios.",
            "formula": "B_i=lambda -> abs(R_i H_i^{-1} J_i)/D_GR",
            "claim_effect": "3409 does not claim EH parent ownership, Newtonian reduction, PPN pass, WEP pass, or R10 pass.",
            "valid_for_claim": False,
        },
    ]


def input_readiness() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "IR3409_0_spin0",
            "channel_id": "NEH3409_0_spin0_scalar",
            "H_input": "MISSING_H_00_OR_SCALAR_MASS",
            "R_input": "MISSING_SCALAR_READOUT_OVERLAP",
            "J_input": "MISSING_SCALAR_SOURCE_CHARGE",
            "lambda_or_mass": "MISSING_lambda_0_or_M_0",
            "projection": "MISSING_gamma_beta_R10_clock_WEP_MAP",
            "source_path": str(SOURCES["residue_bound_interface_3406"]),
            "ready_numeric": False,
            "blocker": "MISSING_PARENT_INPUT",
            "valid_for_claim": False,
        },
        {
            "input_id": "IR3409_1_massive_spin2",
            "channel_id": "NEH3409_1_massive_spin2_four_derivative",
            "H_input": "MISSING_H_22_OR_MASSIVE_SPIN2_POLE",
            "R_input": "MISSING_SPIN2_READOUT_OVERLAP",
            "J_input": "MISSING_SPIN2_SOURCE_COUPLING",
            "lambda_or_mass": "MISSING_lambda_2_or_M_2",
            "projection": "MISSING_gamma_beta_FINITE_RANGE_STABILITY_MAP",
            "source_path": str(SOURCES["residue_bound_interface_3406"]),
            "ready_numeric": False,
            "blocker": "MISSING_PARENT_INPUT",
            "valid_for_claim": False,
        },
        {
            "input_id": "IR3409_2_connection",
            "channel_id": "NEH3409_2_connection",
            "H_input": "MISSING_CONNECTION_HESSIAN_OR_CONSTRAINT_CLASS",
            "R_input": "MISSING_CLOCK_LIGHT_READOUT_OVERLAP",
            "J_input": "MISSING_HYPERMOMENTUM_SOURCE_COUPLING",
            "lambda_or_mass": "MISSING_CONNECTION_SCALE_OR_ALGEBRAIC_ZERO",
            "projection": "MISSING_CLOCK_WEP_LIGHTCONE_PPN_MAP",
            "source_path": str(SOURCES["residue_bound_interface_3406"]),
            "ready_numeric": False,
            "blocker": "MISSING_PARENT_INPUT",
            "valid_for_claim": False,
        },
        {
            "input_id": "IR3409_3_vector",
            "channel_id": "NEH3409_3_vector_preferred_frame",
            "H_input": "MISSING_VECTOR_HESSIAN_OR_GAUGE_ZERO",
            "R_input": "MISSING_PREFERRED_FRAME_READOUT",
            "J_input": "MISSING_VECTOR_SOURCE_CURRENT",
            "lambda_or_mass": "MISSING_VECTOR_MASS_OR_ALIGNMENT_RULE",
            "projection": "MISSING_ALPHA1_ALPHA2_ALPHA3_XI_MAP",
            "source_path": str(SOURCES["r11_beta_vector_530"]),
            "ready_numeric": False,
            "blocker": "MISSING_ARENA_PROJECTION",
            "valid_for_claim": False,
        },
        {
            "input_id": "IR3409_4_domain_memory_bulk",
            "channel_id": "NEH3409_4_domain_memory_bulk",
            "H_input": "MISSING_H_X",
            "R_input": "MISSING_R_X",
            "J_input": "MISSING_J_X",
            "lambda_or_mass": "MISSING_lambda_X_OR_M_X",
            "projection": "MISSING_LOCAL_COMPACT_PROFILE_AND_ARENA_MAP",
            "source_path": str(SOURCES["residue_bound_interface_3406"]),
            "ready_numeric": False,
            "blocker": "MISSING_PARENT_INPUT",
            "valid_for_claim": False,
        },
        {
            "input_id": "IR3409_5_boundary_projector",
            "channel_id": "NEH3409_5_boundary_projector",
            "H_input": "MISSING_EDGE_OR_PROJECTOR_CLASS",
            "R_input": "MISSING_BOUNDARY_READOUT_SILENCE",
            "J_input": "MISSING_SOURCE_WORLD_TUBE_BOUNDARY_FLUX",
            "lambda_or_mass": "MISSING_BOUNDARY_SCALE_OR_TOPOLOGICAL_ZERO",
            "projection": "MISSING_BETA_ALPHA3_XI_MAP",
            "source_path": str(SOURCES["derivative_order_law_3405"]),
            "ready_numeric": False,
            "blocker": "MISSING_PARENT_INPUT",
            "valid_for_claim": False,
        },
        {
            "input_id": "IR3409_6_source_readout",
            "channel_id": "NEH3409_6_source_readout",
            "H_input": "NOT_A_PROPAGATING_HESSIAN_ONLY",
            "R_input": "MISSING_SAME_OBSERVED_READOUT_THROUGH_OU2",
            "J_input": "MISSING_A_SOURCE_B_SOURCE_MEASURED_GM_LOCK",
            "lambda_or_mass": "not_applicable",
            "projection": "MISSING_BETA_GAMMA_SOURCE_NORMALIZATION_MAP",
            "source_path": str(SOURCES["r11_beta_vector_530"]),
            "ready_numeric": False,
            "blocker": "MISSING_ARENA_PROJECTION",
            "valid_for_claim": False,
        },
        {
            "input_id": "IR3409_7_q_loc",
            "channel_id": "NEH3409_7_q_loc",
            "H_input": "PARTIAL_PROVISIONAL_COMPACT_BUDGET_ONLY",
            "R_input": "MISSING_PHYSICAL_U2_AND_ALPHA_VECTOR_READOUT_SPLIT",
            "J_input": "MISSING_PARENT_SOURCE_CURRENT_SPLIT",
            "lambda_or_mass": "not_yet_isolated",
            "projection": "beta_only_value_present_alpha_vector_unsigned",
            "source_path": str(SOURCES["qloc_guard_3403"]),
            "ready_numeric": False,
            "blocker": "MISSING_ARENA_PROJECTION",
            "valid_for_claim": False,
        },
    ]


def local_gr_impact() -> list[dict[str, Any]]:
    return [
        {
            "impact_id": "IM3409_0_good_news",
            "finding": "The GR denominator is now explicit enough to compare non-EH residues against it.",
            "effect_on_project": "This is movement toward a field-theoretic local-GR gate, not just another missing-list.",
            "severity": "POSITIVE_CONDITIONAL",
            "next_fix": "populate or zero the residue numerators channel by channel",
            "valid_for_claim": False,
        },
        {
            "impact_id": "IM3409_1_main_blocker",
            "finding": "Non-EH residues are not yet numerically owned by the parent action.",
            "effect_on_project": "local-GR reduction remains blocked even with a good EH pole",
            "severity": "HARD_BLOCKER",
            "next_fix": "derive H_X,R_X,J_X or prove source/readout zero for the most dangerous channels",
            "valid_for_claim": False,
        },
        {
            "impact_id": "IM3409_2_q_loc",
            "finding": "q_loc has a beta-only number below the beta lock but a severe preferred-frame warning.",
            "effect_on_project": "q_loc is the best next target because it has partial numbers and obvious risk",
            "severity": "HIGH_PRIORITY",
            "next_fix": "split q_loc into beta/gamma/alpha1/alpha2/alpha3/xi projections instead of treating it as one scalar budget",
            "valid_for_claim": False,
        },
        {
            "impact_id": "IM3409_3_coupling_hunt",
            "finding": "The live mathematical problem is coupling ownership: Q_X, K_X, M_X^2 and readout/source overlap.",
            "effect_on_project": "this matches the user's instinct that the coupling is where the theory is underdetermined",
            "severity": "CENTRAL_TARGET",
            "next_fix": "choose one residue lane and derive the coupling from the parent action, not by post-hoc fitting",
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PG3409_0_bound_pack_written",
            "gate": "non-EH residue channels use the 3408 GR pole as denominator",
            "current_result": "PASS_AS_NONCLAIM_INTERFACE",
            "promotes_if": "not a claim gate",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3409_1_parent_residues_numeric",
            "gate": "every active non-EH channel has H_i, R_i, J_i, mass/range and projection",
            "current_result": "FAIL_MISSING_PARENT_INPUTS",
            "promotes_if": "all residue inputs are source-backed and numeric or theorem-zero",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3409_2_empirical_locks",
            "gate": "every active channel is checked against beta/gamma/alpha_i/xi/R10/WEP/clock/orbital locks",
            "current_result": "FAIL_MISSING_ARENA_PROJECTIONS",
            "promotes_if": "each channel passes without cancellation credit",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3409_3_q_loc_alpha_vector",
            "gate": "q_loc beta/gamma/preferred-frame vector split is signed",
            "current_result": "FAIL_ALPHA3_WARNING_LIVE",
            "promotes_if": "alpha-vector leakage is zero, source-silent, or bounded by sourced projections",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3409_4_local_GR_reduction",
            "gate": "local GR/PPN branch claim",
            "current_result": "BLOCKED",
            "promotes_if": "PG3409_1, PG3409_2 and PG3409_3 all pass, plus 3408 parent-action/readout/Hilbert/boundary gates",
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DL3409_0",
            "decision": "Use the 3408 conditional massless spin-2 pole only as the denominator.",
            "rationale": "This lets us push forward constructively while keeping the EH/local-GR claim blocked.",
            "claim_effect": "NO_LOCAL_GR_CLAIM",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DL3409_1",
            "decision": "Convert all surviving non-EH sectors into absolute residue ratios.",
            "rationale": "This is the fair boxing-match scorecard: each extra channel must stand or be bounded, not win by cancellation.",
            "claim_effect": "BOUND_INTERFACE_READY",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DL3409_2",
            "decision": "Prioritize q_loc beta/alpha vector split next.",
            "rationale": "q_loc is the only lane with a partial number and the clearest known failure mode.",
            "claim_effect": "NEXT_DERIVATION_TARGET_SELECTED",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3410-Y5-R2FR-q_loc-beta-alpha-vector-residue-split-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3410_q_loc_beta_alpha_vector_residue_split.py",
            "objective": "derive the physical projection split of q_loc into beta/gamma/alpha1/alpha2/alpha3/xi lanes, using the 3409 residue denominator and no-cancellation rule",
            "why_next": "q_loc has a promising beta-only number but a severe preferred-frame warning; this is the fastest route to either rescue or reject that local branch",
            "valid_for_claim": False,
        },
        {
            "target_id": "3411-Y5-R2FR-scalar-R2FR-residue-input-pack-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3411_scalar_R2FR_residue_input_pack.py",
            "objective": "populate the scalar/R2/fR B_0(lambda_0) numerator and real alpha(lambda)/PPN locks",
            "why_next": "if q_loc is not rescuable, scalar residue sourcing is the next cleanest local bound route",
            "valid_for_claim": False,
        },
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3409_0",
            "script": str(Path(__file__).resolve()),
            "writes": ";".join(str(path) for path in OUTPUTS.values()) + ";" + str(DOC),
            "claim_status": "NONCLAIM_INTERFACE_ONLY",
            "scope_guard": "post-checkpoint-work only; no formalization-workbench writes",
            "valid_for_claim": False,
        }
    ]


def validation_rows(generated: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = generated["source_register"]
    channels = generated["non_eh_residue_channels"]
    gates = generated["promotion_gates"]
    locks = generated["empirical_locks"]
    next_rows = generated["next_target"]
    output_paths = list(OUTPUTS.values()) + [DOC]
    source_exists = all(str(row["exists"]) == "True" for row in source_rows)
    no_workbench = all("formalization-workbench" not in str(path) for path in output_paths)
    all_nonclaim = all(
        str(row.get("valid_for_claim", "False")).lower() == "false"
        for rows in generated.values()
        for row in rows
    )
    no_score_ready = all(str(row.get("score_ready", "False")).lower() == "false" for row in channels)
    local_gr_blocked = any(
        row.get("gate_id") == "PG3409_4_local_GR_reduction" and row.get("current_result") == "BLOCKED"
        for row in gates
    )
    qloc_lock_present = any(row.get("lock_id") == "LOCK3409_2_q_loc_alpha3_warning" for row in locks)
    beta_lock_present = any(row.get("lock_id") == "LOCK3409_0_beta_PPN" for row in locks)
    next_qloc = any("q_loc" in row.get("target_id", "") for row in next_rows)
    rows = [
        {
            "check_id": "VAL3409_0_sources_exist",
            "check": "every cited local source path exists",
            "passed": source_exists,
            "detail": f"{sum(str(row['exists']) == 'True' for row in source_rows)}/{len(source_rows)} source paths exist",
        },
        {
            "check_id": "VAL3409_1_scope",
            "check": "no output path targets formalization-workbench",
            "passed": no_workbench,
            "detail": "all outputs are under post-checkpoint-work",
        },
        {
            "check_id": "VAL3409_2_denominator",
            "check": "conditional GR pole denominator exists and remains nonclaim",
            "passed": bool(generated["gr_pole_denominator"]),
            "detail": generated["gr_pole_denominator"][0]["current_status"],
        },
        {
            "check_id": "VAL3409_3_channel_count",
            "check": "non-EH residue channel pack includes at least eight channels",
            "passed": len(channels) >= 8,
            "detail": f"{len(channels)} channels written",
        },
        {
            "check_id": "VAL3409_4_no_score_ready",
            "check": "no non-EH channel is score-ready by accident",
            "passed": no_score_ready,
            "detail": "all score_ready fields are false",
        },
        {
            "check_id": "VAL3409_5_all_nonclaim",
            "check": "all generated rows keep valid_for_claim=false",
            "passed": all_nonclaim,
            "detail": "3409 is a bound interface, not a local-GR claim",
        },
        {
            "check_id": "VAL3409_6_beta_lock",
            "check": "beta PPN lock context is present",
            "passed": beta_lock_present,
            "detail": "beta bound row imported from q_loc guard context",
        },
        {
            "check_id": "VAL3409_7_alpha_warning",
            "check": "q_loc preferred-frame warning is carried forward",
            "passed": qloc_lock_present,
            "detail": "alpha3 warning prevents beta-only promotion",
        },
        {
            "check_id": "VAL3409_8_local_GR_blocked",
            "check": "local-GR promotion remains blocked",
            "passed": local_gr_blocked,
            "detail": "PG3409_4_local_GR_reduction is BLOCKED",
        },
        {
            "check_id": "VAL3409_9_next_target",
            "check": "next target selects a constructive q_loc split rather than another missing ledger",
            "passed": next_qloc,
            "detail": next_rows[0]["target_id"],
        },
    ]
    overall = all(row["passed"] for row in rows)
    rows.append(
        {
            "check_id": "VAL3409_10_overall",
            "check": "3409 bound pack is internally valid",
            "passed": overall,
            "detail": "PASS" if overall else "FAIL",
        }
    )
    return rows


def build_doc(generated: dict[str, list[dict[str, Any]]]) -> str:
    return "\n\n".join(
        [
            "# 3409 - Non-EH Residue Bound Pack Relative To The GR Pole",
            "## Summary\n"
            "- This checkpoint moves the local-GR route forward by using the 3408 conditional EH/GR pole as a denominator.\n"
            "- It does not claim local GR, PPN, WEP, R10, clock, or orbital success.\n"
            "- The useful output is a no-cancellation residue scorecard: every surviving non-EH channel must be zero, source-silent, gapped/screened, or individually bounded.\n"
            "- The sharpest next target is q_loc, because its beta lane is promising but its preferred-frame warning is lethal until split.",
            "## GR Denominator\n" + md_table(generated["gr_pole_denominator"]),
            "## Non-EH Channels\n" + md_table(generated["non_eh_residue_channels"]),
            "## Bound Formulas\n" + md_table(generated["bound_formulas"]),
            "## Empirical Locks\n" + md_table(generated["empirical_locks"]),
            "## No-Cancellation Rule\n" + md_table(generated["no_cancellation_score_rule"]),
            "## Input Readiness\n" + md_table(generated["input_readiness"]),
            "## Local-GR Impact\n" + md_table(generated["local_gr_impact"]),
            "## Promotion Gates\n" + md_table(generated["promotion_gates"]),
            "## Decision Ledger\n" + md_table(generated["decision_ledger"]),
            "## Next Target\n" + md_table(generated["next_target"]),
            "## Runner Nonclaim\n" + md_table(generated["runner_nonclaim"]),
            "## Validation\n" + md_table(generated["validation"]),
            "## Bottom Line\n"
            "We are not stuck at the same missing-input loop: 3409 creates the bridge from the conditional GR pole to scoreable non-EH residue ratios. "
            "The grim part is that the local branch is still not claimable. The useful part is that the next proof target is now narrow and physical: "
            "split q_loc into beta/gamma/preferred-frame projections, then either rescue it by deriving zero leakage or reject that route cleanly.",
        ]
    ) + "\n"


def main() -> None:
    if "formalization-workbench" in str(ROOT):
        raise RuntimeError(f"Refusing to run from formalization-workbench: {ROOT}")

    generated: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register(),
        "gr_pole_denominator": gr_pole_denominator(),
        "non_eh_residue_channels": non_eh_residue_channels(),
        "bound_formulas": bound_formulas(),
        "empirical_locks": empirical_locks(),
        "no_cancellation_score_rule": no_cancellation_score_rule(),
        "input_readiness": input_readiness(),
        "local_gr_impact": local_gr_impact(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    generated["validation"] = validation_rows(generated)

    for key, rows in generated.items():
        write_csv(OUTPUTS[key], rows)

    DOC.write_text(build_doc(generated), encoding="utf-8")

    validation = generated["validation"]
    if not all(str(row["passed"]).lower() == "true" for row in validation):
        failed = [row for row in validation if str(row["passed"]).lower() != "true"]
        raise SystemExit(f"3409 validation failed: {failed}")

    print(f"wrote {len(generated)} CSV artefacts and {DOC}")


if __name__ == "__main__":
    main()
