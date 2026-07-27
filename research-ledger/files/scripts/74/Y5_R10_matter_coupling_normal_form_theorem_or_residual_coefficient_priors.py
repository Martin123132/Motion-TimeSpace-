from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "621-Y5-R10-matter-coupling-normal-form-theorem-or-residual-coefficient-priors.md"
SCRIPT_REL = "scripts/Y5_R10_matter_coupling_normal_form_theorem_or_residual_coefficient_priors.py"
STATUS = "Y5_R10_matter_coupling_normal_form_written_as_contract_not_parent_derived_coefficient_priors_selected"
CLAIM_CEILING = "private_normal_form_gate_only_no_matter_zero_R10_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "622-Y5-R10-parent-matter-sector-contract-or-residual-prior-runner.md"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = fieldnames or (list(rows[0].keys()) if rows else [])
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_bool(value: object) -> bool:
    return str(value).strip().lower() == "true"


def md_table(rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    fields = fieldnames or list(rows[0].keys())

    def cell(value: object) -> str:
        return str(value).replace("|", "\\|").replace("\n", " ")

    lines = [
        "| " + " | ".join(cell(field) for field in fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def build_source_register() -> list[dict[str, object]]:
    sources = [
        ("620-Y5-R10-qbarXT-residual-envelope-after-no-marker-failure.md", "immediate handoff: qbarXT residual vector"),
        ("source-intake/mts_residuals/P8_Y5_BRR545_620_VALIDATION.csv", "prior validation gate"),
        ("source-intake/mts_residuals/P8_Y5_R10_620_RESIDUAL_BASIS.csv", "six-component residual basis"),
        ("source-intake/mts_residuals/P8_Y5_R10_620_INPUT_TEMPLATE.csv", "prior input template"),
        ("source-intake/mts_residuals/P8_Y5_R10_620_ZERO_OR_BOUND_GATE.csv", "zero-or-bound gates"),
        ("source-intake/mts_residuals/P8_Y5_R10_620_OBSERVABLE_PROJECTION_MATRIX.csv", "observable projection matrix"),
        ("619-Y5-R10-no-marker-minimal-quotient-theorem-or-qbarXT-residual-fill.md", "no-marker theorem failure"),
        ("613-Y5-R10-parent-matter-selector-theorem-or-finite-CX-envelope-lock.md", "selector theorem and finite envelope lock"),
        ("576-Y5-R10-constant-source-current-universality-or-qbar-envelope.md", "constant/source-current universality attempt"),
        ("565-Y5-R10-coframe-pullback-zero-or-finite-alpha-coefficient.md", "coframe pullback zero route"),
        ("410-quotient-matter-functor-theorem-attempt.md", "quotient matter functor theorem attempt"),
        ("423-parent-action-minimality-no-extension-theorem-attempt.md", "minimal/no-extension theorem attempt"),
        (SCRIPT_REL, "this checkpoint generator"),
    ]
    return [
        {"source_file": source_file, "exists": (ROOT / source_file).exists(), "role": role}
        for source_file, role in sources
    ]


def build_normal_form_rows() -> list[dict[str, object]]:
    return [
        {
            "theorem_clause": "NMF621_0_parent_matter_domain",
            "required_statement": "ordinary matter fields are sections over the observed MTS geometry, with local diffeomorphism/Lorentz covariance",
            "normal_form_role": "defines the allowed ordinary-matter category",
            "current_corpus_status": "admissible_contract_not_final_parent_theorem",
            "if_owned_then": "matter variations can be organized by observed coframe and representation labels",
            "if_missing_then": "extra local structures can enter qbarXT",
            "zero_components_supported": "none_alone",
            "promote_zero": "false",
            "valid_for_claim": "false",
        },
        {
            "theorem_clause": "NMF621_1_observed_coframe_only",
            "required_statement": "S_matter depends on geometry only through e_obs(Q_MTS) and its compatible connection",
            "normal_form_role": "kills direct common metric/coframe X-dependence",
            "current_corpus_status": "conditional_from_565_613_not_parent_signed",
            "if_owned_then": "Lie_vX(e_obs)=0 and b_g=0",
            "if_missing_then": "hat_g_ab=A_g(X)^2 g_ab or equivalent common metric mode remains legal",
            "zero_components_supported": "b_g",
            "promote_zero": "false",
            "valid_for_claim": "false",
        },
        {
            "theorem_clause": "NMF621_2_no_material_marker",
            "required_statement": "no matter-visible marker m exists except absent, pure gauge, or source-independent auxiliary",
            "normal_form_role": "kills marker coupling channel",
            "current_corpus_status": "not_derived_transforming_markers_remain_legal",
            "if_owned_then": "b_m=0",
            "if_missing_then": "Q_tilde=(Q,m)/G_rel can source material dependence",
            "zero_components_supported": "b_m",
            "promote_zero": "false",
            "valid_for_claim": "false",
        },
        {
            "theorem_clause": "NMF621_3_constant_triviality",
            "required_statement": "ordinary constants theta_A are selector-trivial representation/superselection data",
            "normal_form_role": "kills constant derivative channel",
            "current_corpus_status": "not_parent_derived",
            "if_owned_then": "Lie_vX(theta_A)=0 and b_theta=0",
            "if_missing_then": "clock, EM, mass-ratio, and composition residuals remain",
            "zero_components_supported": "b_theta",
            "promote_zero": "false",
            "valid_for_claim": "false",
        },
        {
            "theorem_clause": "NMF621_4_universal_source_current",
            "required_statement": "one Hilbert/coframe source current and one universal kappa source all ordinary matter",
            "normal_form_role": "kills species/source weighting channel",
            "current_corpus_status": "not_parent_derived",
            "if_owned_then": "kappa_A=kappa and b_kappa=0",
            "if_missing_then": "WEP/composition and material-source residuals remain",
            "zero_components_supported": "b_kappa",
            "promote_zero": "false",
            "valid_for_claim": "false",
        },
        {
            "theorem_clause": "NMF621_5_no_independent_nonHilbert_current",
            "required_statement": "torsion, spin, topological, edge, or non-Hilbert currents are absent, exact, or separately constrained with zero local projection",
            "normal_form_role": "kills non-Hilbert current channel",
            "current_corpus_status": "not_parent_derived",
            "if_owned_then": "b_NH=0",
            "if_missing_then": "spin/torsion/topological/edge residual survives",
            "zero_components_supported": "b_NH",
            "promote_zero": "false",
            "valid_for_claim": "false",
        },
        {
            "theorem_clause": "NMF621_6_no_post_readout_EFT",
            "required_statement": "the parent-derived branch contains no after-the-fact matter counterterms",
            "normal_form_role": "removes post-readout phenomenological contamination from the fundamental branch",
            "current_corpus_status": "branch_policy_pass_not_positive_theorem_evidence",
            "if_owned_then": "b_EFT is absent from the parent-derived theory branch",
            "if_missing_then": "counterterm branch must be labelled phenomenology, not fundamental derivation",
            "zero_components_supported": "b_EFT_policy_exclusion",
            "promote_zero": "false",
            "valid_for_claim": "false",
        },
        {
            "theorem_clause": "NMF621_7_normal_form_verdict",
            "required_statement": "all clauses jointly imply S_m=sum_A int det(e_obs)L_A(Psi_A,D[e_obs]Psi_A;theta_A)",
            "normal_form_role": "would close qbarXT_vec for ordinary matter",
            "current_corpus_status": "not_closed_contract_only",
            "if_owned_then": "qbarXT_vec=0 for ordinary matter before edge/range checks",
            "if_missing_then": "use residual coefficient priors",
            "zero_components_supported": "qbarXT_vec",
            "promote_zero": "false",
            "valid_for_claim": "false",
        },
    ]


def build_parent_clause_ledger() -> list[dict[str, object]]:
    return [
        {
            "clause_id": "PCL621_0_geometry_functor",
            "parent_object_needed": "Obs_e: Q_MTS -> coframe/metric bundle",
            "proof_obligation": "show ordinary matter receives no geometry except Obs_e(Q_MTS)",
            "available_evidence": "565/613 conditional pullback theorems",
            "status": "conditional_not_owned",
            "next_derivation_attempt": "define parent ordinary-matter category and unique geometry functor",
            "blocks_components": "b_g",
        },
        {
            "clause_id": "PCL621_1_marker_classifier",
            "parent_object_needed": "classification of every additional matter-visible m",
            "proof_obligation": "absent/gauge/auxiliary/retained-field trichotomy from parent variation",
            "available_evidence": "619 marker counterexamples",
            "status": "not_owned",
            "next_derivation_attempt": "prove no natural nonconstant marker functor or retain marker coefficient",
            "blocks_components": "b_m",
        },
        {
            "clause_id": "PCL621_2_constant_superselection",
            "parent_object_needed": "theta_A as representation/superselection labels",
            "proof_obligation": "Lie_vX(theta_A)=0 and no class/species X dependence",
            "available_evidence": "576 premise ledger says not parent-derived",
            "status": "not_owned",
            "next_derivation_attempt": "derive constants from matter representation data or fill derivative priors",
            "blocks_components": "b_theta",
        },
        {
            "clause_id": "PCL621_3_source_universality",
            "parent_object_needed": "one current J_Hilbert and one universal coupling kappa",
            "proof_obligation": "exclude sum_A kappa_A T_A and nonuniversal source charges",
            "available_evidence": "576 conditional theorem only",
            "status": "not_owned",
            "next_derivation_attempt": "derive source current from parent Noether/Ward identity",
            "blocks_components": "b_kappa",
        },
        {
            "clause_id": "PCL621_4_nonHilbert_current",
            "parent_object_needed": "current decomposition and boundary/flux certificate",
            "proof_obligation": "prove spin/torsion/topological/edge currents are absent/exact/zero-projection",
            "available_evidence": "620 residual basis; earlier edge rows still open",
            "status": "not_owned",
            "next_derivation_attempt": "separate local matter current from boundary/edge sector",
            "blocks_components": "b_NH",
        },
        {
            "clause_id": "PCL621_5_no_EFT_counterterms",
            "parent_object_needed": "strict parent-derived branch policy",
            "proof_obligation": "ban after-readout counterterms from fundamental evidence",
            "available_evidence": "619/620 route discipline",
            "status": "policy_owned_for_private_branch",
            "next_derivation_attempt": "keep counterterms outside theorem branch unless parent-derived",
            "blocks_components": "b_EFT",
        },
    ]


def build_component_status_rows() -> list[dict[str, object]]:
    return [
        {
            "component": "b_g",
            "normal_form_zero_condition": "observed coframe only: Lie_vX(e_obs)=0",
            "current_status_after_621": "open",
            "reason_not_closed": "unique observed geometry functor not parent-derived",
            "coefficient_prior_needed": "common_frame_log_derivative",
            "claim_zero_now": "false",
            "valid_for_claim": "false",
        },
        {
            "component": "b_theta",
            "normal_form_zero_condition": "constant superselection: Lie_vX(theta_A)=0",
            "current_status_after_621": "open",
            "reason_not_closed": "constant triviality not parent-derived",
            "coefficient_prior_needed": "d_ln_alpha_EM_dXhat; d_ln_mass_ratio_dXhat; other theta derivatives",
            "claim_zero_now": "false",
            "valid_for_claim": "false",
        },
        {
            "component": "b_m",
            "normal_form_zero_condition": "no material marker or marker classified gauge/auxiliary",
            "current_status_after_621": "open",
            "reason_not_closed": "transforming material marker remains legal",
            "coefficient_prior_needed": "marker_coupling_projection",
            "claim_zero_now": "false",
            "valid_for_claim": "false",
        },
        {
            "component": "b_kappa",
            "normal_form_zero_condition": "one universal source current and kappa",
            "current_status_after_621": "open",
            "reason_not_closed": "species/source universality not parent-derived",
            "coefficient_prior_needed": "species_source_weight_splitting",
            "claim_zero_now": "false",
            "valid_for_claim": "false",
        },
        {
            "component": "b_NH",
            "normal_form_zero_condition": "non-Hilbert currents absent/exact/zero-flux",
            "current_status_after_621": "open",
            "reason_not_closed": "current decomposition and boundary/flux certificate not derived",
            "coefficient_prior_needed": "nonHilbert_current_projection",
            "claim_zero_now": "false",
            "valid_for_claim": "false",
        },
        {
            "component": "b_EFT",
            "normal_form_zero_condition": "post-readout EFT excluded from parent-derived branch",
            "current_status_after_621": "excluded_by_branch_policy_not_theorem_evidence",
            "reason_not_closed": "policy avoids contamination but does not prove other components zero",
            "coefficient_prior_needed": "none_if_absent; else phenomenology_only",
            "claim_zero_now": "false",
            "valid_for_claim": "false",
        },
        {
            "component": "qbarXT_vec",
            "normal_form_zero_condition": "all components zero-derived",
            "current_status_after_621": "not_passed",
            "reason_not_closed": "five physical residual channels remain open",
            "coefficient_prior_needed": "full coefficient-prior template",
            "claim_zero_now": "false",
            "valid_for_claim": "false",
        },
    ]


def build_coefficient_prior_rows() -> list[dict[str, object]]:
    return [
        {
            "prior_id": "CP621_0_common_frame",
            "parameter": "common_frame_log_derivative",
            "component": "b_g",
            "symbolic_definition": "d ln A_g/dXhat or 0.5*T^ab*Lie_vX(hat_g_ab)/rho_ref",
            "allowed_status_values": "derive_zero,numeric_bound,symbolic_placeholder",
            "current_value": "MISSING_PARENT_INPUT",
            "units": "dimensionless",
            "sign_policy": "signed",
            "source_required": "parent geometry functor proof or local-gravity bound source",
            "valid_for_claim": "false",
        },
        {
            "prior_id": "CP621_1_alpha_EM",
            "parameter": "d_ln_alpha_EM_dXhat",
            "component": "b_theta",
            "symbolic_definition": "Lie_vX(alpha_EM)/alpha_EM",
            "allowed_status_values": "derive_zero,numeric_bound,symbolic_placeholder",
            "current_value": "MISSING_PARENT_INPUT",
            "units": "dimensionless",
            "sign_policy": "signed",
            "source_required": "EM normal-form theorem, clock/fine-structure source, or parent charge derivation",
            "valid_for_claim": "false",
        },
        {
            "prior_id": "CP621_2_mass_ratios",
            "parameter": "d_ln_mass_ratio_dXhat",
            "component": "b_theta",
            "symbolic_definition": "Lie_vX(mu_i)/mu_i for ordinary mass-ratio constants",
            "allowed_status_values": "derive_zero,numeric_bound,symbolic_placeholder",
            "current_value": "MISSING_PARENT_INPUT",
            "units": "dimensionless",
            "sign_policy": "signed",
            "source_required": "particle/mass normal-form theorem or composition/clock source",
            "valid_for_claim": "false",
        },
        {
            "prior_id": "CP621_3_marker_projection",
            "parameter": "marker_coupling_projection",
            "component": "b_m",
            "symbolic_definition": "(partial L_m/partial m)*Lie_vX(m)/rho_ref",
            "allowed_status_values": "derive_zero,numeric_bound,symbolic_placeholder",
            "current_value": "MISSING_PARENT_INPUT",
            "units": "dimensionless",
            "sign_policy": "signed",
            "source_required": "marker classifier theorem or material-contrast bound",
            "valid_for_claim": "false",
        },
        {
            "prior_id": "CP621_4_source_weight",
            "parameter": "species_source_weight_splitting",
            "component": "b_kappa",
            "symbolic_definition": "sum_A ((kappa_A-kappa)/kappa)*T_A/T_ref",
            "allowed_status_values": "derive_zero,numeric_bound,symbolic_placeholder",
            "current_value": "MISSING_PARENT_INPUT",
            "units": "dimensionless",
            "sign_policy": "signed",
            "source_required": "universal source-current theorem or WEP/composition bound",
            "valid_for_claim": "false",
        },
        {
            "prior_id": "CP621_5_nonHilbert",
            "parameter": "nonHilbert_current_projection",
            "component": "b_NH",
            "symbolic_definition": "J_XT_nonHilbert/J_ref",
            "allowed_status_values": "derive_zero,numeric_bound,symbolic_placeholder",
            "current_value": "MISSING_PARENT_INPUT",
            "units": "dimensionless",
            "sign_policy": "signed",
            "source_required": "current decomposition theorem or spin/torsion/edge bound",
            "valid_for_claim": "false",
        },
        {
            "prior_id": "CP621_6_post_readout_EFT",
            "parameter": "post_readout_counterterm_projection",
            "component": "b_EFT",
            "symbolic_definition": "delta_X L_EFT_after_readout/rho_ref",
            "allowed_status_values": "absent_from_parent_branch,phenomenology_only",
            "current_value": "absent_from_parent_branch",
            "units": "dimensionless",
            "sign_policy": "not_used_for_theorem_claim",
            "source_required": "N/A unless intentionally demoted to phenomenology",
            "valid_for_claim": "false",
        },
        {
            "prior_id": "CP621_7_total_projection",
            "parameter": "P_A_qbarXT_vec",
            "component": "qbarXT_vec",
            "symbolic_definition": "observable projection matrix applied to coefficient vector",
            "allowed_status_values": "derive_zero,numeric_projection,symbolic_placeholder",
            "current_value": "MISSING_PARENT_INPUT",
            "units": "dimensionless",
            "sign_policy": "signed_or_norm_bound_by_arena",
            "source_required": "arena-specific projection source plus all component statuses",
            "valid_for_claim": "false",
        },
    ]


def build_arena_prior_rows() -> list[dict[str, object]]:
    return [
        {
            "arena_id": "AP621_0_R10",
            "arena": "R10 inverse-square",
            "required_coefficients": "common_frame_log_derivative, marker_coupling_projection, species_source_weight_splitting, nonHilbert_current_projection, K_X, Qbar_XH, lambda_X",
            "normal_form_shortcut": "b_g=b_m=b_kappa=b_NH=0 plus K/edge zero would close this matter source route",
            "if_not_zero": "run alpha_X(lambda)=K_X Qbar_XH P_R10 qbarXT_vec against real bound curve",
            "status": "blocked_until_coefficients_sourced",
            "valid_for_claim": "false",
        },
        {
            "arena_id": "AP621_1_WEP",
            "arena": "composition/WEP",
            "required_coefficients": "d_ln_mass_ratio_dXhat, marker_coupling_projection, species_source_weight_splitting",
            "normal_form_shortcut": "b_theta=b_m=b_kappa=0",
            "if_not_zero": "build composition charge model and compare to baseline GR/free-fall",
            "status": "blocked_until_coefficients_sourced",
            "valid_for_claim": "false",
        },
        {
            "arena_id": "AP621_2_PPN",
            "arena": "PPN/local solar gravity",
            "required_coefficients": "common_frame_log_derivative plus range/projection matrix",
            "normal_form_shortcut": "b_g=0 or exponential/range suppression with sourced lambda_X",
            "if_not_zero": "compute r_PPN=M_PPN*qbarXT_vec",
            "status": "blocked_until_coefficients_sourced",
            "valid_for_claim": "false",
        },
        {
            "arena_id": "AP621_3_clocks_EM",
            "arena": "clocks and EM/fine structure",
            "required_coefficients": "d_ln_alpha_EM_dXhat, d_ln_mass_ratio_dXhat, environmental X profile",
            "normal_form_shortcut": "b_theta=0",
            "if_not_zero": "use clock and spectra sensitivity coefficients",
            "status": "blocked_until_coefficients_sourced",
            "valid_for_claim": "false",
        },
        {
            "arena_id": "AP621_4_orbital",
            "arena": "orbital and binary systems",
            "required_coefficients": "common_frame_log_derivative, species_source_weight_splitting, nonHilbert_current_projection, range/radiation channel",
            "normal_form_shortcut": "b_g=b_kappa=b_NH=0 or short-range suppression with sourced lambda_X",
            "if_not_zero": "compare against GR/Newton orbital residuals and radiation bounds",
            "status": "blocked_until_coefficients_sourced",
            "valid_for_claim": "false",
        },
    ]


def build_decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D621_0_main_verdict",
            "status": STATUS,
            "decision": "normal-form theorem is written but not parent-derived",
            "meaning": "the exact theorem contract is now explicit; it cannot be used as a local-GR derivation until parent clauses are owned",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D621_1_partial_policy",
            "status": "post_readout_EFT_excluded_by_branch_policy",
            "decision": "keep b_EFT absent from parent-derived branch",
            "meaning": "this avoids post-hoc contamination but is not positive evidence for qbarXT=0",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D621_2_residual_priors",
            "status": "coefficient_priors_selected_for_open_components",
            "decision": "open components require derive-zero proofs or sourced priors",
            "meaning": "b_g, b_theta, b_m, b_kappa, and b_NH remain the active local matter gaps",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D621_3_claim_ceiling",
            "status": CLAIM_CEILING,
            "decision": "no R10/WEP/PPN/local-GR pass",
            "meaning": "no component zero was promoted and all numeric priors remain private placeholders",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def build_route_rows() -> list[dict[str, object]]:
    return [
        {
            "route_id": "RU621_0_allowed",
            "allowed_after_621": "cite the matter normal-form theorem only as a conditional contract",
            "forbidden_after_621": "say ordinary matter coupling has been derived from the parent action",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU621_1_allowed",
            "allowed_after_621": "treat b_EFT as absent from the parent-derived branch",
            "forbidden_after_621": "use that branch policy as proof that qbarXT_vec=0",
            "next_action": "keep b_EFT out of theorem scoring unless parent-derived",
        },
        {
            "route_id": "RU621_2_allowed",
            "allowed_after_621": "build a residual-prior runner with explicit MISSING_PARENT_INPUT gates",
            "forbidden_after_621": "score R10/WEP/PPN while coefficient priors are placeholders",
            "next_action": "choose parent contract derivation or smoke-runner schema",
        },
    ]


def build_nonclaim_summary() -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "normal_form_contract_written": "true",
            "normal_form_parent_derived": "false",
            "b_g_zero_promoted": "false",
            "b_theta_zero_promoted": "false",
            "b_m_zero_promoted": "false",
            "b_kappa_zero_promoted": "false",
            "b_NH_zero_promoted": "false",
            "b_EFT_parent_branch_absent": "true",
            "qbarXT_vec_zero_promoted": "false",
            "coefficient_priors_selected": "true",
            "R10_pass": "false",
            "WEP_pass": "false",
            "PPN_pass": "false",
            "local_GR_pass": "false",
            "next_target": NEXT_TARGET,
        }
    ]


def build_validation_rows(
    source_register: list[dict[str, object]],
    normal_form_rows: list[dict[str, object]],
    parent_clause_rows: list[dict[str, object]],
    component_rows: list[dict[str, object]],
    prior_rows: list[dict[str, object]],
    arena_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    nonclaim_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    missing_sources = [row["source_file"] for row in source_register if not parse_bool(row["exists"])]
    prior_path = OUT / "P8_Y5_BRR545_620_VALIDATION.csv"
    prior_validation_rows = read_csv(prior_path) if prior_path.exists() else []
    prior_failures = [row for row in prior_validation_rows if row.get("result") != "pass"]

    required_clauses = {
        "NMF621_1_observed_coframe_only",
        "NMF621_2_no_material_marker",
        "NMF621_3_constant_triviality",
        "NMF621_4_universal_source_current",
        "NMF621_5_no_independent_nonHilbert_current",
        "NMF621_6_no_post_readout_EFT",
        "NMF621_7_normal_form_verdict",
    }
    clause_ids = {row["theorem_clause"] for row in normal_form_rows}
    no_zero_promoted = all(not parse_bool(row["promote_zero"]) for row in normal_form_rows)
    parent_clause_complete = len(parent_clause_rows) >= 6 and all(row["status"] for row in parent_clause_rows)
    component_names = {row["component"] for row in component_rows}
    required_components = {"b_g", "b_theta", "b_m", "b_kappa", "b_NH", "b_EFT", "qbarXT_vec"}
    component_status_complete = required_components.issubset(component_names) and all(not parse_bool(row["claim_zero_now"]) for row in component_rows)
    prior_parameters = {row["parameter"] for row in prior_rows}
    required_prior_parameters = {
        "common_frame_log_derivative",
        "d_ln_alpha_EM_dXhat",
        "d_ln_mass_ratio_dXhat",
        "marker_coupling_projection",
        "species_source_weight_splitting",
        "nonHilbert_current_projection",
        "post_readout_counterterm_projection",
        "P_A_qbarXT_vec",
    }
    priors_safe = required_prior_parameters.issubset(prior_parameters) and all(
        not parse_bool(row["valid_for_claim"]) for row in prior_rows
    )
    arenas_safe = len(arena_rows) >= 5 and all(row["status"] == "blocked_until_coefficients_sourced" for row in arena_rows)
    all_nonclaim = all(
        not parse_bool(row.get("valid_for_claim", "false"))
        for row in normal_form_rows + component_rows + prior_rows + arena_rows + decision_rows
    )
    nonclaim = nonclaim_rows[0]

    return [
        {
            "check_id": "V621_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": "missing=" + str(len(missing_sources)) + ("; " + json.dumps(missing_sources) if missing_sources else ""),
        },
        {
            "check_id": "V621_1_prior_620_clean",
            "result": "pass" if prior_path.exists() and not prior_failures else "fail",
            "detail": f"prior_exists={prior_path.exists()};prior_rows={len(prior_validation_rows)};prior_failures={len(prior_failures)}",
        },
        {
            "check_id": "V621_2_normal_form_clauses_present",
            "result": "pass" if required_clauses.issubset(clause_ids) else "fail",
            "detail": f"clauses={','.join(sorted(clause_ids))}",
        },
        {
            "check_id": "V621_3_no_zero_promotion",
            "result": "pass" if no_zero_promoted else "fail",
            "detail": f"no_zero_promoted={no_zero_promoted}",
        },
        {
            "check_id": "V621_4_parent_clause_ledger_complete",
            "result": "pass" if parent_clause_complete else "fail",
            "detail": f"parent_clause_rows={len(parent_clause_rows)}",
        },
        {
            "check_id": "V621_5_component_status_complete",
            "result": "pass" if component_status_complete else "fail",
            "detail": f"components={','.join(sorted(component_names))};all_claim_zero_false={component_status_complete}",
        },
        {
            "check_id": "V621_6_coefficient_priors_safe",
            "result": "pass" if priors_safe else "fail",
            "detail": f"prior_parameters={','.join(sorted(prior_parameters))};all_valid_for_claim_false={priors_safe}",
        },
        {
            "check_id": "V621_7_arena_priors_blocked",
            "result": "pass" if arenas_safe else "fail",
            "detail": f"arena_rows={len(arena_rows)};blocked_until_coefficients_sourced={arenas_safe}",
        },
        {
            "check_id": "V621_8_all_claim_flags_false",
            "result": "pass" if all_nonclaim else "fail",
            "detail": f"all_valid_for_claim_false={all_nonclaim}",
        },
        {
            "check_id": "V621_9_no_local_claim",
            "result": "pass"
            if nonclaim["R10_pass"] == "false"
            and nonclaim["WEP_pass"] == "false"
            and nonclaim["PPN_pass"] == "false"
            and nonclaim["local_GR_pass"] == "false"
            and nonclaim["qbarXT_vec_zero_promoted"] == "false"
            else "fail",
            "detail": "qbarXT_vec_zero=false;R10=false;WEP=false;PPN=false;local_GR=false",
        },
    ]


def write_doc(
    source_register: list[dict[str, object]],
    normal_form_rows: list[dict[str, object]],
    parent_clause_rows: list[dict[str, object]],
    component_rows: list[dict[str, object]],
    prior_rows: list[dict[str, object]],
    arena_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    route_rows: list[dict[str, object]],
    nonclaim_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    generated = utc_now()
    content = f"""# 621 Y5 R10 matter coupling normal form theorem or residual coefficient priors

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`

## Verdict
- I tried to turn the 620 residual vector into a matter-coupling normal-form theorem.
- The theorem is clean as a conditional statement: if ordinary matter only sees `e_obs(Q_MTS)`, constants are selector-trivial, no material markers exist, the source current is universal, non-Hilbert currents vanish, and no post-readout EFT is allowed, then the ordinary-matter contribution to `qbarXT_vec` vanishes.
- The current corpus does not yet derive those premises from the parent action. So this checkpoint writes the exact parent-action contract, but does not promote any physical zero.
- One useful hygiene gain is retained: post-readout EFT is excluded from the parent-derived branch as a policy guardrail, not as positive evidence. The remaining five components become explicit coefficient priors.

## Conditional Normal Form
The target normal form is:

```text
S_matter = sum_A int det(e_obs) L_A(Psi_A, D[e_obs]Psi_A; theta_A)
```

with:

```text
e_obs = Obs_e(Q_MTS)
Lie_vX(e_obs) = 0
Lie_vX(theta_A) = 0
no matter-visible marker m
one universal Hilbert/coframe current
no independent non-Hilbert local current
no post-readout EFT counterterm
```

Then the 620 envelope collapses:

```text
qbarXT_vec = (b_g,b_theta,b_m,b_kappa,b_NH,b_EFT) = 0
```

This is a good theorem target. It is not yet a theorem owned by the parent action.

## Source Register
{md_table(source_register)}

## Normal Form Theorem Attempt
{md_table(normal_form_rows)}

## Parent Clause Ledger
{md_table(parent_clause_rows)}

## Component Status Matrix
{md_table(component_rows)}

## Coefficient Prior Template
{md_table(prior_rows)}

## Arena Prior Schema
{md_table(arena_rows)}

## Decision
{md_table(decision_rows)}

## Route Update
{md_table(route_rows)}

## Nonclaim Summary
{md_table(nonclaim_rows)}

## Validation
{md_table(validation_rows)}

## Practical Read
This is not grim; it is disciplined. We now know exactly what must be proven for the clean local-GR matter route. If the parent action can own the normal form, the local branch gets much stronger. If it cannot, the same rows become a fair coefficient-prior runner instead of a hidden assumption.
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    source_register = build_source_register()
    normal_form_rows = build_normal_form_rows()
    parent_clause_rows = build_parent_clause_ledger()
    component_rows = build_component_status_rows()
    prior_rows = build_coefficient_prior_rows()
    arena_rows = build_arena_prior_rows()
    decision_rows = build_decision_rows()
    route_rows = build_route_rows()
    nonclaim_rows = build_nonclaim_summary()
    validation_rows = build_validation_rows(
        source_register,
        normal_form_rows,
        parent_clause_rows,
        component_rows,
        prior_rows,
        arena_rows,
        decision_rows,
        nonclaim_rows,
    )

    outputs = [
        ("P8_Y5_R10_621_SOURCE_REGISTER.csv", source_register),
        ("P8_Y5_R10_621_NORMAL_FORM_THEOREM_ATTEMPT.csv", normal_form_rows),
        ("P8_Y5_R10_621_PARENT_CLAUSE_LEDGER.csv", parent_clause_rows),
        ("P8_Y5_R10_621_COMPONENT_STATUS_MATRIX.csv", component_rows),
        ("P8_Y5_R10_621_COEFFICIENT_PRIOR_TEMPLATE.csv", prior_rows),
        ("P8_Y5_R10_621_ARENA_PRIOR_SCHEMA.csv", arena_rows),
        ("P8_Y5_BRR545_621_DECISION.csv", decision_rows),
        ("P8_Y5_BRR545_621_ROUTE_UPDATE.csv", route_rows),
        ("P8_Y5_R10_621_NONCLAIM_SUMMARY.csv", nonclaim_rows),
        ("P8_Y5_BRR545_621_VALIDATION.csv", validation_rows),
    ]
    for filename, rows in outputs:
        write_csv(OUT / filename, rows)

    write_doc(
        source_register,
        normal_form_rows,
        parent_clause_rows,
        component_rows,
        prior_rows,
        arena_rows,
        decision_rows,
        route_rows,
        nonclaim_rows,
        validation_rows,
    )

    failed = [row for row in validation_rows if row["result"] != "pass"]
    print(json.dumps({"status": STATUS, "doc": str(DOC), "failed_checks": failed}, indent=2))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
