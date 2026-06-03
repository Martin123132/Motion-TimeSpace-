from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "no-species-source-charge-one-coframe-theorem-attempt"
CHECKPOINT_DOC = "447-no-species-source-charge-one-coframe-theorem-attempt.md"
STATUS = "no_species_source_charge_one_coframe_theorem_attempt_written_one_coframe_insufficient_species_source_charge_not_parent_derived_R1_retained_no_WEP_Newton_or_local_GR_pass"
CLAIM_CEILING = "no_species_source_charge_conditional_theorem_only_no_R1_WEP_measured_GM_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "448-constant-sector-universality-theorem-attempt.md"
NO_SPECIES_CONTRACT_PATH = Path("source-intake/mts_residuals/P8_no_species_source_charge_CONTRACT.csv")
R1_CHANNEL_POLICY_PATH = Path("source-intake/mts_residuals/R1_source_charge_channel_policy_CONTRACT.csv")


NO_SPECIES_CONTRACT_COLUMNS = [
    "contract_id",
    "required_identity",
    "mathematical_form",
    "closes_component",
    "affected_rows",
    "current_status",
    "evidence_needed",
    "fallback_if_missing",
]


R1_CHANNEL_POLICY_COLUMNS = [
    "channel",
    "role",
    "direct_WEP_subscore",
    "full_R1_guardrail",
    "source_lock",
    "units",
    "theorem_zero_condition",
    "current_status",
    "fallback_if_missing",
]


SOURCE_DOCS = [
    {
        "path": "382-parent-local-action-minimal-contract.md",
        "role": "one-coframe, matter/coframe, and species-charge parent-action contract",
    },
    {
        "path": "392-EH-operator-selection-under-identity-closure.md",
        "role": "identity coframe closure and closure-zero caveat",
    },
    {
        "path": "402-EH-source-normalization-parent-pair.md",
        "role": "same-frame source-normalization obstruction",
    },
    {
        "path": "412-v4-source-charge-channel-map-review.md",
        "role": "R1 source-charge channel split and direct/full guardrail policy",
    },
    {
        "path": "413-no-marker-parent-action-theorem-attempt.md",
        "role": "no-marker partial theorem and material-marker counterexamples",
    },
    {
        "path": "428-MTS-local-residual-vector-input-contract.md",
        "role": "R0/R1 residual-vector definitions and source-charge row",
    },
    {
        "path": "439-EH-only-exterior-parent-premise-ladder.md",
        "role": "P1/P8 premise ladder and R1 retained state",
    },
    {
        "path": "444-source-normalization-residual-vector-refinement.md",
        "role": "P8_species_source_charge residual component",
    },
    {
        "path": "446-source-owner-current-parent-action-contract.md",
        "role": "A6 selector-blind source-action contract and next target",
    },
    {
        "path": "runs/20260602-055500-quotient-matter-functor-theorem-attempt/results/matter_argument_audit.csv",
        "role": "matter arguments and species/source hazards",
    },
    {
        "path": "runs/20260602-055500-quotient-matter-functor-theorem-attempt/results/functor_requirements.csv",
        "role": "functor factorization and constant-sector independence requirements",
    },
    {
        "path": "runs/20260602-055500-quotient-matter-functor-theorem-attempt/results/counterexample_functors.csv",
        "role": "species constants and marker-extended quotient counterexamples",
    },
    {
        "path": "runs/20260602-062500-v4-source-charge-channel-map-review/results/R1_channel_review.csv",
        "role": "R1 direct/full channel map",
    },
    {
        "path": "runs/20260602-062500-v4-source-charge-channel-map-review/results/channel_count_policy.csv",
        "role": "R1 channel policy and no-promotion rule",
    },
    {
        "path": "runs/20260602-062500-v4-source-charge-channel-map-review/results/R1_subscore_check.csv",
        "role": "R1 stress subscore examples",
    },
    {
        "path": "runs/20260602-063500-no-marker-parent-action-theorem-attempt/results/marker_definitions.csv",
        "role": "marker classification",
    },
    {
        "path": "runs/20260602-063500-no-marker-parent-action-theorem-attempt/results/no_marker_theorem_chain.csv",
        "role": "no-marker theorem chain status",
    },
    {
        "path": "runs/20260602-063500-no-marker-parent-action-theorem-attempt/results/counterexample_markers.csv",
        "role": "material marker/species marker counterexamples",
    },
    {
        "path": "runs/20260602-143000-source-normalization-residual-vector-refinement/results/P8_source_residual_template_rows.csv",
        "role": "P8_species_source_charge and frame calibration residual rows",
    },
    {
        "path": "runs/20260602-150000-source-owner-current-parent-action-contract/results/parent_action_blocks.csv",
        "role": "A6 selector-blind source-action parent block",
    },
    {
        "path": "source-intake/local_bounds/local_bound_claims.csv",
        "role": "R0/R1 WEP source locks",
    },
    {
        "path": "source-intake/mts_residuals/P8_source_normalization_residual_vector_TEMPLATE.csv",
        "role": "P8 source residual template",
    },
]


THEOREM_STATEMENT = [
    {
        "part": "conditional_theorem",
        "statement": "If the parent action selects one observed coframe and the active matter/source action is selector-blind, marker-free, constant-sector universal, and source-normalized by a common calibrated current, then the species derivative of measured source strength vanishes.",
        "mathematical_form": "S_m+S_source=sum_A S_A[Psi_A,e_obs,omega[e_obs],theta_univ]+S_source[J_univ]; no m,I_Q,P_active,q_A => partial_A mu_obs=0",
        "status": "proved_as_conditional_chain_rule",
    },
    {
        "part": "one_coframe_limit",
        "statement": "One coframe removes the direct matter-geometry pullback ambiguity, but it does not by itself remove species constants, material markers, bulk/boundary composition charge, or source-normalization species split.",
        "mathematical_form": "e_A=e_obs does not imply partial_A theta_A=0 or partial_A mu_obs=0",
        "status": "blocks_R1_promotion",
    },
    {
        "part": "current_corpus_status",
        "statement": "The current corpus has conditional one-coframe/functor routes and a partial no-marker theorem for fixed spurions, but it does not derive full source-charge blindness.",
        "mathematical_form": "P8_species_source_charge remains active",
        "status": "not_parent_derived",
    },
]


PROOF_STEPS = [
    {
        "step": 1,
        "claim": "Parent action selects one observed coframe before readout.",
        "mathematical_step": "e_A=e_obs for all A",
        "status": "conditional_not_parent_derived",
        "gap": "current one-coframe branch is closure-labelled, not a parent theorem",
    },
    {
        "step": 2,
        "claim": "Matter action factors only through that coframe and universal constants.",
        "mathematical_step": "S_m=sum_A S_A[Psi_A,e_obs,omega[e_obs],theta_univ]",
        "status": "sufficient_if_assumed",
        "gap": "theta_A and source constants can still be species or class dependent",
    },
    {
        "step": 3,
        "claim": "No material marker or post-readout mask enters the parent bulk matter/source action.",
        "mathematical_step": "partial_m S_parent=0 and P_active not in S_parent",
        "status": "partial_only",
        "gap": "fixed spurions are conditionally excluded, but co-moving material markers remain legal",
    },
    {
        "step": 4,
        "claim": "Source normalization uses one universal calibrated source current, not species charges.",
        "mathematical_step": "J_A -> J_univ and partial_A M_eff=0",
        "status": "not_parent_derived",
        "gap": "A6 selector-blind source action is a contract, not a derivation",
    },
    {
        "step": 5,
        "claim": "No bulk, boundary, torsion/projective, class, or finite-range sector carries composition charge.",
        "mathematical_step": "q_XA=q_BA=q_connection,A=q_range,A=0",
        "status": "not_parent_derived",
        "gap": "R1 channel review keeps these channels visible",
    },
    {
        "step": 6,
        "claim": "Then the species derivative of measured source strength vanishes.",
        "mathematical_step": "partial_A mu_obs = partial_A(G_eff M_eff + mu_extra)=0",
        "status": "valid_conditional_math",
        "gap": "premises are not all parent-derived",
    },
    {
        "step": 7,
        "claim": "Only then can R1 source-charge move from retained to theorem-zero.",
        "mathematical_step": "eta_source_AB=0 by theorem, not by direct-WEP proxy",
        "status": "conditional_R1_route",
        "gap": "R1 remains retained because the theorem premises are open",
    },
]


ONE_COFRAME_LIMITS = [
    {
        "limit_id": "L0_direct_geometry_only",
        "one_coframe_closes": "direct matter/coframe pullback ambiguity",
        "does_not_close": "source charge hidden in constants, source normalization, boundary/bulk/domain, or connection sectors",
        "example": "theta_A(I_Q) with common e_obs",
        "affected_rows": "R1;R2;R11",
    },
    {
        "limit_id": "L1_common_metric_class_coupling",
        "one_coframe_closes": "species frame mismatch if all species use the same rescaled frame",
        "does_not_close": "common class scalar can still affect clocks, gamma, beta, or fifth-force rows",
        "example": "S_A[Psi_A, exp(F(I_Q)) e_obs, theta_A]",
        "affected_rows": "R2;R3;R4;R10;R11",
    },
    {
        "limit_id": "L2_source_normalization_cross_channel",
        "one_coframe_closes": "direct differential acceleration from different coframes",
        "does_not_close": "measured GM can carry species/source normalization split",
        "example": "partial_A mu_obs != 0 while e_A=e_obs",
        "affected_rows": "R1;R4;R9;R11",
    },
    {
        "limit_id": "L3_connection_source_charge",
        "one_coframe_closes": "metric/coframe identity branch",
        "does_not_close": "independent connection, torsion, projective, or hypermomentum source charges",
        "example": "matter uses e_obs but also an independent projective source coupling",
        "affected_rows": "R0;R1;R2;R11",
    },
    {
        "limit_id": "L4_bulk_boundary_composition",
        "one_coframe_closes": "ordinary matter geometry label",
        "does_not_close": "bulk-X or boundary source charges coupled to composition",
        "example": "q_XA rho_A or boundary_species_charge",
        "affected_rows": "R1;R3;R4;R10;R11",
    },
]


SOURCE_CHARGE_COUNTEREXAMPLES = [
    {
        "counterexample": "species_internal_constants",
        "construction": "theta_A=theta_A(I_Q) or q_A(I_Q) while all species use e_obs",
        "why_one_coframe_does_not_block": "constants are not part of the coframe pullback",
        "required_blocker": "constant-sector universality theorem",
        "affected_rows": "R1;R2;R11",
    },
    {
        "counterexample": "co_moving_material_marker",
        "construction": "Q_tilde=(x,m)/G_rel with S_matter[Psi_A,e_obs,m]",
        "why_one_coframe_does_not_block": "m descends to quotient data and can label material/source response",
        "required_blocker": "parent no-extension/no-material-marker theorem",
        "affected_rows": "R1;R5;R11",
    },
    {
        "counterexample": "source_normalization_species_split",
        "construction": "mu_obs(A)=G_eff M_eff(A)+mu_extra(A)",
        "why_one_coframe_does_not_block": "measured source strength can depend on composition even in one matter frame",
        "required_blocker": "selector-blind source-normalization current",
        "affected_rows": "R1;R4;R9;R11",
    },
    {
        "counterexample": "bulk_X_composition_charge",
        "construction": "(-Delta+m_X^2)X=q_XA rho_A",
        "why_one_coframe_does_not_block": "finite-range auxiliary source charge is not removed by frame identity",
        "required_blocker": "q_XA=0 theorem or alpha(lambda) curve below bound",
        "affected_rows": "R1;R3;R4;R10;R11",
    },
    {
        "counterexample": "boundary_species_charge",
        "construction": "boundary/class term sources species-dependent monopole or flux",
        "why_one_coframe_does_not_block": "boundary/source data can be species-sensitive while matter geometry is common",
        "required_blocker": "class-only zero-flux boundary theorem",
        "affected_rows": "R1;R7;R9;R11",
    },
    {
        "counterexample": "connection_projective_source_charge",
        "construction": "projective/torsion/hypermomentum source coupling distinguishes matter species",
        "why_one_coframe_does_not_block": "coframe identity does not derive Levi-Civita/source-connection universality",
        "required_blocker": "P4 compatibility plus no-Gamma source-charge theorem",
        "affected_rows": "R0;R1;R2;R11",
    },
]


NO_SPECIES_CONTRACT = [
    {
        "contract_id": "S0_one_observed_coframe_parent_selected",
        "required_identity": "one observed coframe is selected before readout for all matter/source standards",
        "mathematical_form": "e_A=e_obs and omega_A=omega[e_obs]",
        "closes_component": "direct frame/source calibration split only",
        "affected_rows": "R0;R2;R11",
        "current_status": "conditional_not_parent_derived",
        "evidence_needed": "parent-selected observed-frame theorem",
        "fallback_if_missing": "R0/R2 frame residuals remain active",
    },
    {
        "contract_id": "S1_matter_factorization",
        "required_identity": "matter action factors through e_obs, omega[e_obs], and universal constants only",
        "mathematical_form": "S_m=sum_A S_A[Psi_A,e_obs,omega[e_obs],theta_univ]",
        "closes_component": "selector-blind matter chain rule",
        "affected_rows": "R0;R1;R2;R11",
        "current_status": "sufficient_axiom_not_parent_derived",
        "evidence_needed": "quotient matter functor theorem with constant-sector independence",
        "fallback_if_missing": "R1 source charge and R2 clock rows retained",
    },
    {
        "contract_id": "S2_constant_sector_universality",
        "required_identity": "species constants and source charges do not depend on markers, quotient invariants, or species labels",
        "mathematical_form": "partial_A theta_A=partial_m theta_A=partial_IQ theta_A=0",
        "closes_component": "P8_species_source_charge",
        "affected_rows": "R1;R2;R11",
        "current_status": "not_derived",
        "evidence_needed": "constant-sector universality theorem",
        "fallback_if_missing": "species_internal_constants counterexample remains legal",
    },
    {
        "contract_id": "S3_no_material_marker_extension",
        "required_identity": "material markers and post-readout masks are absent from S_parent",
        "mathematical_form": "partial_m S_parent=0; P_active notin args(S_parent)",
        "closes_component": "material-marker source charge",
        "affected_rows": "R0;R1;R5;R11",
        "current_status": "partial_fixed_spurion_only",
        "evidence_needed": "no-extension theorem for co-moving material markers",
        "fallback_if_missing": "co_moving_material_marker remains legal",
    },
    {
        "contract_id": "S4_source_normalization_species_blind",
        "required_identity": "active measured-GM source current is species independent",
        "mathematical_form": "partial_A mu_obs=0 and J_A -> J_univ",
        "closes_component": "P8_species_source_charge;source_normalization_species_split",
        "affected_rows": "R1;R4;R9;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "selector-blind source-normalization variation",
        "fallback_if_missing": "source_normalization_species_split remains visible",
    },
    {
        "contract_id": "S5_no_bulk_boundary_composition_charge",
        "required_identity": "bulk, boundary, class, and domain sectors carry no composition charge",
        "mathematical_form": "q_XA=q_BA=q_DA=0",
        "closes_component": "bulk_X_composition_charge;boundary_species_charge",
        "affected_rows": "R1;R3;R4;R7;R9;R10;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "bulk no-source theorem and boundary class-only theorem",
        "fallback_if_missing": "direct R1 source channels remain retained",
    },
    {
        "contract_id": "S6_no_connection_source_charge",
        "required_identity": "connection/torsion/projective/hypermomentum sectors do not carry species source charge",
        "mathematical_form": "partial_A q_connection=0 and Gamma=Gamma_LC or mapped P4 row",
        "closes_component": "connection_projective_source_charge",
        "affected_rows": "R0;R1;R2;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "P4 compatibility plus no-Gamma source theorem",
        "fallback_if_missing": "P4/P8 R11 connection-source rows remain active",
    },
    {
        "contract_id": "S7_R1_empirical_fallback",
        "required_identity": "if any species/source charge remains nonzero, it becomes executable R1 data",
        "mathematical_form": "eta_source_AB with source path, units, bound, and direct/full channel policy",
        "closes_component": "none; retained branch only",
        "affected_rows": "R1;R11",
        "current_status": "template_policy_only",
        "evidence_needed": "numeric residual or derived bound",
        "fallback_if_missing": "no R1/WEP/local-GR claim",
    },
]


R1_CHANNEL_POLICY = [
    {
        "channel": "source_charge_species_split",
        "role": "direct_WEP_source_charge",
        "direct_WEP_subscore": "true",
        "full_R1_guardrail": "true",
        "source_lock": "2.8e-15",
        "units": "dimensionless",
        "theorem_zero_condition": "partial_A ordinary source/test charge = 0",
        "current_status": "retained",
        "fallback_if_missing": "direct R1 source-charge row",
    },
    {
        "channel": "bulk_X_composition_charge",
        "role": "direct_WEP_bulk_composition",
        "direct_WEP_subscore": "true",
        "full_R1_guardrail": "true",
        "source_lock": "2.8e-15",
        "units": "dimensionless",
        "theorem_zero_condition": "q_XA=0 or executable alpha_X(lambda) below bounds",
        "current_status": "retained",
        "fallback_if_missing": "bulk-X R1/R10 residual rows",
    },
    {
        "channel": "boundary_species_charge",
        "role": "direct_WEP_boundary_composition",
        "direct_WEP_subscore": "true",
        "full_R1_guardrail": "true",
        "source_lock": "2.8e-15",
        "units": "dimensionless",
        "theorem_zero_condition": "boundary/class sector has no species charge or flux hair",
        "current_status": "retained",
        "fallback_if_missing": "boundary R1/R7/R9 residual rows",
    },
    {
        "channel": "source_normalization_species_split",
        "role": "source_normalization_cross_channel",
        "direct_WEP_subscore": "false",
        "full_R1_guardrail": "true",
        "source_lock": "2.8e-15",
        "units": "dimensionless",
        "theorem_zero_condition": "partial_A mu_obs=0 from source-normalization theorem",
        "current_status": "retained_cross_channel",
        "fallback_if_missing": "P8_species_source_charge remains visible beside direct WEP",
    },
]


GATE_TESTS = [
    {
        "gate": "conditional_theorem_written",
        "pass_condition": "one-coframe plus selector-blind universal source implies partial_A mu_obs=0",
        "current_result": "pass_conditional",
        "evidence": "conditional proof chain recorded",
    },
    {
        "gate": "one_coframe_overclaim_blocked",
        "pass_condition": "one coframe is not treated as source-charge theorem-zero",
        "current_result": "pass",
        "evidence": "one-coframe limit rows recorded",
    },
    {
        "gate": "counterexamples_retained",
        "pass_condition": "species constants, markers, bulk/boundary/connection charges remain visible",
        "current_result": "pass",
        "evidence": "6 counterexamples recorded",
    },
    {
        "gate": "source_blindness_parent_derived",
        "pass_condition": "contracts S0-S6 are parent-derived",
        "current_result": "fail",
        "evidence": "constant-sector, material-marker, source-normalization, bulk/boundary, and P4 source-charge theorems are open",
    },
    {
        "gate": "R1_source_charge_promoted",
        "pass_condition": "eta_source_AB=0 by theorem or residual data below sourced bound",
        "current_result": "fail",
        "evidence": "contract only; no numeric residual or theorem-zero",
    },
    {
        "gate": "local_GR_promoted",
        "pass_condition": "R0-R11 full vector and parent premises resolved",
        "current_result": "fail",
        "evidence": "source-charge theorem attempt only",
    },
]


THEOREM_STATUS = [
    {
        "claim": "one-coframe/source-blind conditional theorem written",
        "status": "pass_conditional",
        "evidence": "proof steps show sufficient premises for partial_A mu_obs=0",
    },
    {
        "claim": "one-coframe alone rejected as R1 proof",
        "status": "pass",
        "evidence": "one-coframe limit and counterexample rows",
    },
    {
        "claim": "no-species/source-charge contract written",
        "status": "pass",
        "evidence": str(NO_SPECIES_CONTRACT_PATH),
    },
    {
        "claim": "R1 channel policy written",
        "status": "pass",
        "evidence": str(R1_CHANNEL_POLICY_PATH),
    },
    {
        "claim": "species/source-charge theorem-zero parent-derived",
        "status": "fail",
        "evidence": "constant-sector universality, material-marker no-extension, and selector-blind source-normalization remain open",
    },
    {
        "claim": "R1/WEP/Newton/local-GR promoted",
        "status": "fail",
        "evidence": "theorem attempt only; no source residual data or full parent proof",
    },
]


GATE_RESULTS_TEMPLATE = [
    {
        "gate": "theorem_statement_written",
        "status": "pass",
        "evidence": "conditional theorem and one-coframe limit recorded",
    },
    {
        "gate": "proof_steps_written",
        "status": "pass",
        "evidence": "7 proof steps recorded",
    },
    {
        "gate": "one_coframe_limits_written",
        "status": "pass",
        "evidence": "5 limits recorded",
    },
    {
        "gate": "source_charge_counterexamples_written",
        "status": "pass",
        "evidence": "6 counterexamples recorded",
    },
    {
        "gate": "no_species_contract_written",
        "status": "pass",
        "evidence": str(NO_SPECIES_CONTRACT_PATH),
    },
    {
        "gate": "R1_channel_policy_written",
        "status": "pass",
        "evidence": str(R1_CHANNEL_POLICY_PATH),
    },
    {
        "gate": "source_blindness_parent_derived",
        "status": "fail",
        "evidence": "contracts S0-S6 not all parent-derived",
    },
    {
        "gate": "R1_source_charge_theorem_zero",
        "status": "fail",
        "evidence": "P8_species_source_charge remains retained",
    },
    {
        "gate": "measured_GM_parent_derived",
        "status": "fail",
        "evidence": "source-normalization species split remains open",
    },
    {
        "gate": "local_GR_promoted",
        "status": "fail",
        "evidence": "R1/P8 source-charge checkpoint only",
    },
    {
        "gate": "claim_ceiling_enforced",
        "status": "pass",
        "evidence": CLAIM_CEILING,
    },
]


DECISION = [
    {
        "decision": "The no-species/source-charge theorem has been attempted. It gives a clean conditional result: one observed coframe plus factorized selector-blind matter, universal constants, no material markers, source-blind measured-GM current, and no bulk/boundary/connection composition charge would imply partial_A mu_obs=0. But one coframe alone is insufficient, and the current corpus does not derive the constant-sector universality, no-marker no-extension, source-normalization species-blindness, or bulk/boundary/connection no-charge theorems. Therefore R1 and P8_species_source_charge remain retained; no WEP, measured-GM, Newton, or local-GR promotion is allowed.",
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "rank": 1,
        "target": "448-constant-sector-universality-theorem-attempt.md",
        "why_next": "theta_A/q_A universality is the sharpest remaining source-charge subcondition",
    },
    {
        "rank": 2,
        "target": "derive material-marker no-extension or keep S3 as closure",
        "why_next": "co-moving material markers are the strongest no-marker counterexample",
    },
    {
        "rank": 3,
        "target": "map R1_source_charge_channel_policy_CONTRACT.csv into evaluator",
        "why_next": "direct WEP and full R1 guardrail must stay separated in tests",
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCE_DOCS:
        source_path = ROOT / source["path"]
        rows.append(
            {
                "source_file": source["path"],
                "exists": source_path.exists(),
                "role": source["role"],
            }
        )
    return rows


def gate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    source_gate = {
        "gate": "source_paths_exist",
        "status": "pass" if not missing_sources else "fail",
        "evidence": "all cited source paths exist" if not missing_sources else ";".join(missing_sources),
    }
    no_species_schema_gate = {
        "gate": "no_species_contract_schema_matches",
        "status": "pass" if list(NO_SPECIES_CONTRACT[0].keys()) == NO_SPECIES_CONTRACT_COLUMNS else "fail",
        "evidence": "no-species contract columns match schema"
        if list(NO_SPECIES_CONTRACT[0].keys()) == NO_SPECIES_CONTRACT_COLUMNS
        else "no-species contract schema mismatch",
    }
    r1_schema_gate = {
        "gate": "R1_channel_policy_schema_matches",
        "status": "pass" if list(R1_CHANNEL_POLICY[0].keys()) == R1_CHANNEL_POLICY_COLUMNS else "fail",
        "evidence": "R1 channel policy columns match schema"
        if list(R1_CHANNEL_POLICY[0].keys()) == R1_CHANNEL_POLICY_COLUMNS
        else "R1 channel policy schema mismatch",
    }
    return [source_gate, no_species_schema_gate, r1_schema_gate, *GATE_RESULTS_TEMPLATE]


def write_checkpoint_markdown(run_dir: Path, gate_result_rows: list[dict[str, Any]]) -> None:
    source_rows = source_register_rows()
    text = f"""# 447 - No-Species Source-Charge One-Coframe Theorem Attempt

Private R1/P8 source-charge checkpoint. This is not a public WEP, Einstein-Hilbert, measured-GM, Newtonian-limit, PPN, fifth-force, R10/R11, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 446 made `A6_selector_blind_source_action` the crispest P8 subcondition. This checkpoint asks whether one observed coframe plus source-blind matter/source structure derives `partial_A mu_obs=0`, or whether species/source charge remains retained.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/no_species_source_charge_one_coframe_theorem_attempt.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| No-species contract | `{NO_SPECIES_CONTRACT_PATH}` |
| R1 channel policy | `{R1_CHANNEL_POLICY_PATH}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(source_rows, ["source_file", "exists", "role"])}

## 4. Theorem Statement

{markdown_table(THEOREM_STATEMENT, ["part", "statement", "mathematical_form", "status"])}

## 5. Conditional Proof Steps

{markdown_table(PROOF_STEPS, ["step", "claim", "mathematical_step", "status", "gap"])}

## 6. One-Coframe Limits

{markdown_table(ONE_COFRAME_LIMITS, ["limit_id", "one_coframe_closes", "does_not_close", "example", "affected_rows"])}

## 7. Source-Charge Counterexamples

{markdown_table(SOURCE_CHARGE_COUNTEREXAMPLES, ["counterexample", "construction", "why_one_coframe_does_not_block", "required_blocker", "affected_rows"])}

## 8. No-Species Source-Charge Contract

The no-species/source-charge contract has been written to `{NO_SPECIES_CONTRACT_PATH}`.

{markdown_table(NO_SPECIES_CONTRACT, NO_SPECIES_CONTRACT_COLUMNS)}

## 9. R1 Channel Policy

The R1 source-charge channel policy has been written to `{R1_CHANNEL_POLICY_PATH}`.

{markdown_table(R1_CHANNEL_POLICY, R1_CHANNEL_POLICY_COLUMNS)}

## 10. Gate Tests

{markdown_table(GATE_TESTS, ["gate", "pass_condition", "current_result", "evidence"])}

## 11. Theorem Status

{markdown_table(THEOREM_STATUS, ["claim", "status", "evidence"])}

## 12. Gate Results

{markdown_table(gate_result_rows, ["gate", "status", "evidence"])}

## 13. Decision

{DECISION[0]["decision"]}

Practical read: one coframe is necessary footwork, not the knockout. It stops one kind of direct WEP slip, but the source-charge channel can still punch through constants, markers, source normalization, bulk fields, boundary charge, or connection charge. The next useful target is the constant sector: prove `theta_A` and source charges are genuinely universal, or keep R1 retained.

## 14. Next Queue

{markdown_table(NEXT_QUEUE, ["rank", "target", "why_next"])}
"""
    (ROOT / CHECKPOINT_DOC).write_text(text, encoding="utf-8")


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()
    gate_result_rows = gate_rows(source_rows)

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "theorem_statement.csv", THEOREM_STATEMENT)
    write_csv(results_dir / "proof_steps.csv", PROOF_STEPS)
    write_csv(results_dir / "one_coframe_limits.csv", ONE_COFRAME_LIMITS)
    write_csv(results_dir / "source_charge_counterexamples.csv", SOURCE_CHARGE_COUNTEREXAMPLES)
    write_csv(results_dir / "no_species_source_charge_contract.csv", NO_SPECIES_CONTRACT, NO_SPECIES_CONTRACT_COLUMNS)
    write_csv(results_dir / "R1_channel_policy.csv", R1_CHANNEL_POLICY, R1_CHANNEL_POLICY_COLUMNS)
    write_csv(results_dir / "gate_tests.csv", GATE_TESTS)
    write_csv(results_dir / "theorem_status.csv", THEOREM_STATUS)
    write_csv(results_dir / "gate_results.csv", gate_result_rows)
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)
    write_csv(ROOT / NO_SPECIES_CONTRACT_PATH, NO_SPECIES_CONTRACT, NO_SPECIES_CONTRACT_COLUMNS)
    write_csv(ROOT / R1_CHANNEL_POLICY_PATH, R1_CHANNEL_POLICY, R1_CHANNEL_POLICY_COLUMNS)

    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "conditional_theorem_written": True,
        "one_coframe_alone_sufficient": False,
        "source_charge_counterexamples": len(SOURCE_CHARGE_COUNTEREXAMPLES),
        "no_species_contract_rows": len(NO_SPECIES_CONTRACT),
        "R1_channel_policy_rows": len(R1_CHANNEL_POLICY),
        "source_blindness_parent_derived": False,
        "P8_species_source_charge_derived_zero": False,
        "R1_source_charge_promoted": False,
        "WEP_promoted": False,
        "measured_GM_parent_derived": False,
        "Newtonian_reduction_promoted": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "no_species_contract_path": str(ROOT / NO_SPECIES_CONTRACT_PATH),
        "R1_channel_policy_path": str(ROOT / R1_CHANNEL_POLICY_PATH),
        "checkpoint_doc": CHECKPOINT_DOC,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    write_checkpoint_markdown(run_dir, gate_result_rows)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 447 no-species source-charge one-coframe theorem attempt artifacts."
    )
    parser.add_argument(
        "--timestamp",
        default=datetime.now().strftime("%Y%m%d-%H%M%S"),
        help="Run timestamp prefix.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_dir = write_run(args.timestamp)
    print(json.dumps({"status": STATUS, "run_dir": str(run_dir)}, indent=2))


if __name__ == "__main__":
    main()
