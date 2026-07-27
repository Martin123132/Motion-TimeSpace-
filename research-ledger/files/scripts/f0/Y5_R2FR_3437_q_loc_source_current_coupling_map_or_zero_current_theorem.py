from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3437-Y5-R2FR-q_loc-source-current-coupling-map-or-zero-current-theorem-under-AX1090.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCES = {
    "doc_3436": ROOT / "3436-Y5-R2FR-R10-alpha-lambda-runner-real-curve-or-q_loc-range-zero-under-AX1090.md",
    "next_3436": OUT / "P8_Y5_R2FR_3436_NEXT_TARGET.csv",
    "source_map_3436": OUT / "P8_Y5_R2FR_3436_MTS_ALPHA_SOURCE_MAP_STATUS.csv",
    "range_zero_3436": OUT / "P8_Y5_R2FR_3436_QLOC_RANGE_ZERO_AUDIT.csv",
    "runner_contract_3436": OUT / "P8_Y5_R2FR_3436_ALPHA_LAMBDA_RUNNER_CONTRACT.csv",
    "source_current_449": ROOT / "449-source-current-Ward-universality-theorem-attempt.md",
    "source_current_contract": OUT / "P8_source_current_Ward_universality_CONTRACT.csv",
    "source_owner_contract": OUT / "P8_source_owner_parent_action_terms_CONTRACT.csv",
    "source_measure_clauses": OUT / "P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv",
    "hilbert_monopole_contract": OUT / "P8_Hilbert_monopole_calibration_CONTRACT.csv",
    "source_normalization_stack": OUT / "P8_SOURCE_NORMALIZATION_THEOREM_STACK.csv",
    "constant_gm_hair_gate": OUT / "P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv",
    "exchange_component_score": OUT / "P8_EXCHANGE_COMPONENT_MAP_SCORE.csv",
    "response_doublet_source_ledger": OUT / "P8_RESPONSE_DOUBLET_EULER_SOURCE_LEDGER.csv",
    "positive_x_nohair_1042": OUT / "P8_Y5_R10_1042_POSITIVE_X_NOHAIR_IDENTITY.csv",
    "qloc_owner_3432": OUT / "P8_Y5_R2FR_3432_QLOC_HILBERT_OWNER_THEOREM.csv",
    "qloc_ppn_r10_3432": OUT / "P8_Y5_R2FR_3432_QLOC_PPN_R10_OPERATOR_UPDATE.csv",
    "ppn_stack_3434": OUT / "P8_Y5_R2FR_3434_FIRST_PPN_RESIDUAL_STACK.csv",
    "identity_coframe_script": ROOT / "scripts" / "identity_coframe_parent_selection_principle.py",
    "identity_or_class_script": ROOT / "scripts" / "identity_coframe_or_class_metric_fork.py",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3437_SOURCE_REGISTER.csv",
    "coupling_branch_fork": OUT / "P8_Y5_R2FR_3437_COUPLING_BRANCH_FORK.csv",
    "direct_matter_source_current_theorem": OUT / "P8_Y5_R2FR_3437_DIRECT_MATTER_SOURCE_CURRENT_THEOREM.csv",
    "jx_chain_rule_audit": OUT / "P8_Y5_R2FR_3437_JX_CHAIN_RULE_AUDIT.csv",
    "r10_alpha_numerator_status": OUT / "P8_Y5_R2FR_3437_R10_ALPHA_NUMERATOR_STATUS.csv",
    "zero_current_impact_on_3436": OUT / "P8_Y5_R2FR_3437_ZERO_CURRENT_IMPACT_ON_3436.csv",
    "retained_coupling_counterexamples": OUT / "P8_Y5_R2FR_3437_RETAINED_COUPLING_COUNTEREXAMPLES.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3437_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3437_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3437_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3437_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3437_VALIDATION.csv",
}


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
        return "_No rows._"
    fields = list(rows[0].keys())

    def clean(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "/")

    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |",
            *["| " + " | ".join(clean(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def source_register() -> list[dict[str, Any]]:
    roles = {
        "doc_3436": "R10/range-zero handoff",
        "next_3436": "3437 target declaration",
        "source_map_3436": "missing alpha numerator/source map",
        "range_zero_3436": "q_loc/range zero clauses",
        "runner_contract_3436": "R10 runner input contract",
        "source_current_449": "conditional Hilbert source-current theorem",
        "source_current_contract": "SC0-SC8 source-current contract",
        "source_owner_contract": "parent source-owner action blocks",
        "source_measure_clauses": "source measure/M_eff flux clauses",
        "hilbert_monopole_contract": "Hilbert source to measured monopole contract",
        "source_normalization_stack": "source-normalization theorem stack",
        "constant_gm_hair_gate": "derivative/range/species hair identity",
        "exchange_component_score": "exchange-component source-current warnings",
        "response_doublet_source_ledger": "response-doublet source problems",
        "positive_x_nohair_1042": "positive-X nohair theorem",
        "qloc_owner_3432": "q_loc owner/zero theorem",
        "qloc_ppn_r10_3432": "q_loc PPN/R10 operator update",
        "ppn_stack_3434": "R10/PPN residual stack",
        "identity_coframe_script": "identity-coframe selection theorem attempt",
        "identity_or_class_script": "identity coframe/class metric fork",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[source_id],
            "valid_for_claim": False,
        }
        for source_id, path in SOURCES.items()
    ]


def coupling_branch_fork() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": "CB3437_A_identity_coframe_nonmetric_X",
            "matter_action": "S_m=sum_A S_A[Psi_A,e_obs,omega[e_obs],theta_A]",
            "X_entry": "X_i is independent nonmetric sector data and does not enter e_obs, omega[e_obs], or theta_A",
            "source_current_result": "J_i^matter=delta S_m/delta X_i=0",
            "status": "DIRECT_MATTER_CURRENT_ZERO_DERIVED_CONDITIONAL",
            "what_remains": "parent must select identity coframe branch; metric mixing/boundary/projector sources still need zero or bounds",
            "valid_for_claim": False,
        },
        {
            "branch_id": "CB3437_B_universal_class_metric",
            "matter_action": "S_m=sum_A S_A[Psi_A,exp(F(X_i))e_obs,omega[ehat],theta_A]",
            "X_entry": "X_i enters the common matter metric/coframe",
            "source_current_result": "J_i^matter approximately (1/2)sqrt(-g) T_m F_i'(X) plus spin/connection pullback terms",
            "status": "NONZERO_COMMON_TRACE_CURRENT_UNLESS_F_PRIME_ZERO",
            "what_remains": "derive F_i'=0 locally, pure gauge, or counterstress/nohair bound",
            "valid_for_claim": False,
        },
        {
            "branch_id": "CB3437_C_species_class_metric",
            "matter_action": "sum_A S_A[Psi_A,exp(F_A(X_i))e_obs,omega[ehat_A],theta_A(X_i)]",
            "X_entry": "X_i enters matter geometry or constants in a species-dependent way",
            "source_current_result": "J_i^matter has species-dependent trace/constant terms",
            "status": "DEMOTE_FOR_LOCAL_GR_UNLESS_PARENT_SPECIES_SYMMETRY_PROVES_COMMON_OR_ZERO",
            "what_remains": "would activate WEP/source-charge/R10 rows",
            "valid_for_claim": False,
        },
        {
            "branch_id": "CB3437_D_gravity_sector_mixing",
            "matter_action": "S_m independent of X_i, but S_grav has g-X mixing",
            "X_entry": "X_i couples indirectly through field equations and metric response",
            "source_current_result": "direct J_i^matter=0 but alpha_i may survive through metric-mixing source",
            "status": "DIRECT_ZERO_ONLY_FULL_ALPHA_BLOCKED",
            "what_remains": "diagonalize the local g-X operator and show no sourced eigenmode or compute alpha numerator",
            "valid_for_claim": False,
        },
        {
            "branch_id": "CB3437_E_boundary_projector_entry",
            "matter_action": "S_m independent of bulk X_i, but boundary/projector/domain choices carry charge",
            "X_entry": "X_i or P_loc enters boundary/collar/readout structure",
            "source_current_result": "bulk direct J_i^matter can vanish while boundary/projector source survives",
            "status": "BOUNDARY_PROJECTOR_RESIDUAL_RETAINED",
            "what_remains": "zero compact boundary flux and parent-owned projector theorem",
            "valid_for_claim": False,
        },
    ]


def direct_matter_source_current_theorem() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "JZ3437_0_chain_rule",
            "statement": "The direct finite-mode matter current is the functional derivative of the matter action with respect to X_i.",
            "formula": "J_i^matter := delta S_matter / delta X_i",
            "status": "DEFINITION",
            "condition_or_missing": "requires branch choice for how X_i enters S_matter",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "JZ3437_1_identity_coframe_zero",
            "statement": "If matter depends only on the observed coframe and species representation data, and X_i is not an argument of either, then the direct matter current vanishes.",
            "formula": "S_matter[Psi,e_obs,omega[e_obs],theta] with partial_X e_obs=partial_X theta=0 => J_i^matter=0",
            "status": "DERIVED_ZERO_BRANCH_NONCLAIM",
            "condition_or_missing": "identity coframe / selector-blind matter branch must be parent-selected",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "JZ3437_2_test_response_zero",
            "statement": "The same branch gives zero direct test-body response to X_i.",
            "formula": "q_i^{T,direct}=delta ln m_T / delta X_i = 0 if m_T and local rods/clocks use only e_obs and theta_T",
            "status": "DERIVED_ZERO_BRANCH_NONCLAIM",
            "condition_or_missing": "clock/rod constants must be representation data, not X_i fields",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "JZ3437_3_class_metric_obstruction",
            "statement": "If X_i changes the matter coframe, the source current is generically proportional to matter stress and does not vanish.",
            "formula": "delta S_m/delta X_i = (1/2)sqrt(-g) T^{mu nu} delta ghat_{mu nu}/delta X_i + spin/connection terms",
            "status": "NO_GO_FOR_CLASS_METRIC_WITHOUT_F_PRIME_ZERO",
            "condition_or_missing": "must prove delta ghat/delta X_i=0, pure gauge, or nohair/counterstress",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "JZ3437_4_full_alpha_not_zeroed",
            "statement": "Direct matter-current zero does not by itself zero the full R10/q_loc alpha numerator.",
            "formula": "alpha_i = alpha_i^direct + alpha_i^gX_mix + alpha_i^boundary + alpha_i^projector + alpha_i^class_metric + alpha_i^tail",
            "status": "FULL_ALPHA_RETAINED",
            "condition_or_missing": "metric mixing, boundary/projector/domain, and class-metric terms still need zero or bounds",
            "valid_for_claim": False,
        },
    ]


def jx_chain_rule_audit() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "CR3437_0_explicit_X",
            "term": "explicit matter vertex",
            "chain_rule_piece": "partial L_m / partial X_i",
            "identity_branch_value": "0",
            "open_branch_value": "nonzero if matter constants, masses, EM coupling, class variables, or source labels depend on X_i",
            "status": "ZERO_IN_IDENTITY_BRANCH_RETAIN_OTHERWISE",
            "valid_for_claim": False,
        },
        {
            "audit_id": "CR3437_1_coframe_pullback",
            "term": "observed coframe pullback",
            "chain_rule_piece": "(delta S_m/delta e_obs) (delta e_obs/delta X_i)",
            "identity_branch_value": "0",
            "open_branch_value": "active common trace/stress current if ehat=e_obs(X_i)",
            "status": "ZERO_ONLY_IF_IDENTITY_COFRAME_SELECTED",
            "valid_for_claim": False,
        },
        {
            "audit_id": "CR3437_2_connection_pullback",
            "term": "spin/connection pullback",
            "chain_rule_piece": "(delta S_m/delta omega_obs) (delta omega_obs/delta X_i)",
            "identity_branch_value": "0 for Levi-Civita omega[e_obs] independent of X_i",
            "open_branch_value": "hypermomentum/projective source current if independent connection contains X_i",
            "status": "ZERO_IN_MINIMAL_METRIC_BRANCH_RETAIN_IF_CONNECTION_INDEPENDENT",
            "valid_for_claim": False,
        },
        {
            "audit_id": "CR3437_3_species_constants",
            "term": "matter constants and representation labels",
            "chain_rule_piece": "sum_A (partial L_A/partial theta_A) partial_X theta_A",
            "identity_branch_value": "0 if theta_A are representation data",
            "open_branch_value": "species/source charge if masses/couplings/constants run with X_i",
            "status": "ZERO_IN_SUPERSELECTION_BRANCH_RETAIN_OTHERWISE",
            "valid_for_claim": False,
        },
        {
            "audit_id": "CR3437_4_readout_source_norm",
            "term": "source-normalization/readout mask",
            "chain_rule_piece": "delta S_source_norm/delta X_i, Pi_M(X_i), M_eff(X_i), or tau_R10(X_i)",
            "identity_branch_value": "not killed by direct S_matter zero",
            "open_branch_value": "radial/range/source-normalization residual",
            "status": "RETAINED",
            "valid_for_claim": False,
        },
    ]


def r10_alpha_numerator_status() -> list[dict[str, Any]]:
    return [
        {
            "numerator_id": "AN3437_0_direct_source_charge",
            "quantity": "Q_i^{S,direct}",
            "formula": "integral_source J_i^matter",
            "3437_status": "DERIVED_ZERO_BRANCH_NONCLAIM",
            "remaining_terms": "none inside identity-coframe nonmetric-X branch",
            "valid_for_claim": False,
        },
        {
            "numerator_id": "AN3437_1_direct_test_charge",
            "quantity": "q_i^{T,direct}",
            "formula": "delta ln m_T / delta X_i",
            "3437_status": "DERIVED_ZERO_BRANCH_NONCLAIM",
            "remaining_terms": "clock/rod constants must be X-independent",
            "valid_for_claim": False,
        },
        {
            "numerator_id": "AN3437_2_class_metric_trace",
            "quantity": "Q_i^{S,class}",
            "formula": "(1/2) integral sqrt(-g) T^{mu nu} partial_X ghat_{mu nu}",
            "3437_status": "RETAINED_OR_ZERO_IF_F_PRIME_ZERO",
            "remaining_terms": "requires class-metric exclusion or F_i'=0 theorem",
            "valid_for_claim": False,
        },
        {
            "numerator_id": "AN3437_3_metric_mixing",
            "quantity": "Q_i^{S,gX}",
            "formula": "source stress drives metric; metric mixes into X_i through parent operator matrix",
            "3437_status": "RETAINED",
            "remaining_terms": "requires g-X diagonalization and no sourced finite eigenmode",
            "valid_for_claim": False,
        },
        {
            "numerator_id": "AN3437_4_boundary_projector_tail",
            "quantity": "Q_i^{S,boundary/projector}",
            "formula": "boundary flux, projector commutator, domain stress and tail terms",
            "3437_status": "RETAINED",
            "remaining_terms": "requires boundary/projector zero or absolute alpha envelope",
            "valid_for_claim": False,
        },
        {
            "numerator_id": "AN3437_5_total_alpha",
            "quantity": "alpha_i",
            "formula": "alpha_i = K_i tau_R10_i (Q_i^{S,direct}+Q_i^{S,gX}+Q_i^{S,boundary}+...)(q_i^{T,direct}+q_i^{T,metric}+...)",
            "3437_status": "NOT_SCORE_READY",
            "remaining_terms": "direct matter vertex improved, but full numerator and lambda_i remain missing",
            "valid_for_claim": False,
        },
    ]


def zero_current_impact_on_3436() -> list[dict[str, Any]]:
    return [
        {
            "impact_id": "IMP3437_0_source_current_silence",
            "3436_row": "RZ3436_3_source_current_silence",
            "before_status": "MISSING_COUPLING_MAP",
            "after_status": "DIRECT_MATTER_CURRENT_ZERO_IN_IDENTITY_BRANCH",
            "impact": "one sub-piece of J_X is theorem-zeroed conditionally",
            "still_blocking": "parent branch selection and indirect metric/boundary/projector currents",
            "valid_for_claim": False,
        },
        {
            "impact_id": "IMP3437_1_mts_alpha_prediction",
            "3436_row": "ARC3436_2_mts_prediction",
            "before_status": "BLOCKED_SOURCE_MAP_MISSING",
            "after_status": "DIRECT_NUMERATOR_ZERO_PARTIAL",
            "impact": "alpha_direct can be set to zero in the identity-coframe branch",
            "still_blocking": "alpha_total not zero and lambda_i/Z_i/M_i^2 absent",
            "valid_for_claim": False,
        },
        {
            "impact_id": "IMP3437_2_best_route",
            "3436_row": "MSM3436_1_source_current",
            "before_status": "MISSING_COUPLING_MAP",
            "after_status": "COUPLING_FORK_SPLIT",
            "impact": "the route is now a fork: identity coframe gives direct zero; class metric gives trace current; g-X mixing remains",
            "still_blocking": "metric-mixing diagonalization or class-metric exclusion",
            "valid_for_claim": False,
        },
    ]


def retained_coupling_counterexamples() -> list[dict[str, Any]]:
    return [
        {
            "counterexample_id": "CE3437_0_universal_class_metric",
            "construction": "all matter sees ehat=exp(F(X))e_obs",
            "why_direct_zero_fails": "delta ehat/delta X is nonzero, producing trace current",
            "required_blocker": "F'(X)=0 locally, pure gauge, or counterstress/nohair theorem",
            "valid_for_claim": False,
        },
        {
            "counterexample_id": "CE3437_1_species_constants",
            "construction": "m_A=m_A(X) or alpha_EM=alpha_EM(X)",
            "why_direct_zero_fails": "partial_X theta_A creates species/source charge",
            "required_blocker": "constant-sector superselection theorem",
            "valid_for_claim": False,
        },
        {
            "counterexample_id": "CE3437_2_independent_connection",
            "construction": "matter couples to an independent connection containing X_i",
            "why_direct_zero_fails": "hypermomentum or projective current sources X_i",
            "required_blocker": "Levi-Civita/metric-compatibility parent selection or connection no-source theorem",
            "valid_for_claim": False,
        },
        {
            "counterexample_id": "CE3437_3_metric_mixing",
            "construction": "matter does not couple to X_i, but X_i mixes with metric perturbations sourced by T_m",
            "why_direct_zero_fails": "finite X_i exchange can be induced by the gravitational operator matrix",
            "required_blocker": "g-X block diagonalization or positive nohair for sourced eigenmodes",
            "valid_for_claim": False,
        },
        {
            "counterexample_id": "CE3437_4_boundary_source",
            "construction": "bulk J_i=0 but boundary/projector/readout terms carry compact source charge",
            "why_direct_zero_fails": "R10/PPN sees the exterior flux, not only the bulk matter vertex",
            "required_blocker": "zero compact boundary flux and parent-owned projector theorem",
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PG3437_0_direct_current",
            "gate": "direct matter current for nonmetric X is zero in identity-coframe branch",
            "result": "PASS_BRANCH_ZERO_NONCLAIM",
            "evidence": "JZ3437_1 and CR3437_0/1/2/3",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3437_1_full_source_current",
            "gate": "full J_X source current is zero",
            "result": "BLOCKED",
            "evidence": "metric mixing, boundary/projector and class-metric counterexamples remain",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3437_2_r10_alpha",
            "gate": "alpha(lambda) numerator is score-ready",
            "result": "BLOCKED_PARTIAL_NUMERATOR_ONLY",
            "evidence": "AN3437_5 retains full alpha and lambda_i missing",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3437_3_newton",
            "gate": "Newton inverse-square source branch is derived",
            "result": "BLOCKED",
            "evidence": "range/metric-mixing/source-normalization residuals remain",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3437_4_local_GR",
            "gate": "local GR/PPN is derived",
            "result": "BLOCKED",
            "evidence": "PPN residual stack and second-order source stability remain open",
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3437_0_keep_identity_branch",
            "decision": "Keep the identity-coframe nonmetric-X branch as the clean local-GR route.",
            "reason": "It gives an actual conditional zero theorem for the direct matter source current.",
            "next_action": "derive parent selection of identity coframe or treat it as an explicit closure premise",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3437_1_do_not_claim_R10",
            "decision": "Do not promote R10/local-GR from direct current zero.",
            "reason": "Full alpha can still arise through metric mixing, boundary/projector tails, class metric pullback, or source-normalization drift.",
            "next_action": "diagonalize g-X metric mixing or prove nonmetric decoupling",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3437_2_next_best_leap",
            "decision": "Attack metric mixing next.",
            "reason": "After direct matter coupling is zeroed, the biggest remaining way matter sources finite X is through the gravitational operator matrix.",
            "next_action": "3438 metric-mixing-to-alpha-numerator or nonmetric decoupling proof",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3438-Y5-R2FR-metric-mixing-to-alpha-numerator-or-nonmetric-decoupling-proof-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3438_metric_mixing_to_alpha_numerator_or_nonmetric_decoupling_proof.py",
            "objective": "derive whether matter can still source finite-range X through the metric/X operator matrix after direct matter current is zeroed",
            "success_condition": "prove the local g-X block diagonal/nonmetric decoupling branch, or write the first explicit alpha_i metric-mixing numerator template with operator entries and source paths",
            "valid_for_claim": False,
        }
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3437_0",
            "status": "DIRECT_MATTER_COUPLING_ZEROED_CONDITIONAL_FULL_R10_RETAINED",
            "claim_allowed": False,
            "reason": "the theorem moves one coupling row, but full alpha(lambda), Newton and local GR remain blocked",
            "next_safe_action": "attack metric mixing before any empirical R10 score language",
            "valid_for_claim": False,
        }
    ]


def all_generated_nonclaim(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for output_name, rows in rows_by_name.items():
        if output_name == "validation":
            continue
        for row in rows:
            if "valid_for_claim" in row and str(row["valid_for_claim"]).lower() != "false":
                return False
            if "claim_allowed" in row and str(row["claim_allowed"]).lower() != "false":
                return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], start_utc: datetime) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    theorem_rows = rows_by_name["direct_matter_source_current_theorem"]
    numerator_rows = rows_by_name["r10_alpha_numerator_status"]
    impact_rows = rows_by_name["zero_current_impact_on_3436"]
    promotion_rows = rows_by_name["promotion_gates"]
    next_rows = rows_by_name["next_target"]
    modified_count = 0
    if FORMALIZATION.exists():
        start_timestamp = start_utc.timestamp()
        modified_count = sum(
            1 for checked_path in FORMALIZATION.rglob("*") if checked_path.is_file() and checked_path.stat().st_mtime >= start_timestamp
        )
    validations = [
        {
            "check_id": "VAL3437_0_sources_exist",
            "condition": "all cited source paths exist",
            "passed": all(row["exists"] for row in source_rows),
            "detail": f"{sum(1 for row in source_rows if row['exists'])}/{len(source_rows)} source paths exist",
        },
        {
            "check_id": "VAL3437_1_outputs_scoped",
            "condition": "all outputs are in post-checkpoint-work",
            "passed": all(str(path).startswith(str(ROOT)) for path in OUTPUTS.values()),
            "detail": str(ROOT),
        },
        {
            "check_id": "VAL3437_2_nonclaim",
            "condition": "all generated rows remain nonclaim",
            "passed": all_generated_nonclaim(rows_by_name),
            "detail": "valid_for_claim=false and claim_allowed=false throughout generated rows",
        },
        {
            "check_id": "VAL3437_3_direct_zero_row",
            "condition": "direct matter source-current zero theorem exists",
            "passed": any(row["theorem_id"] == "JZ3437_1_identity_coframe_zero" and row["status"] == "DERIVED_ZERO_BRANCH_NONCLAIM" for row in theorem_rows),
            "detail": "J_i^matter=0 in identity-coframe nonmetric-X branch",
        },
        {
            "check_id": "VAL3437_4_full_alpha_not_promoted",
            "condition": "full alpha(lambda) remains blocked",
            "passed": any(row["numerator_id"] == "AN3437_5_total_alpha" and row["3437_status"] == "NOT_SCORE_READY" for row in numerator_rows),
            "detail": "direct numerator moved but full alpha retained",
        },
        {
            "check_id": "VAL3437_5_3436_updated",
            "condition": "3436 missing coupling map is refined, not falsely closed",
            "passed": any(row["impact_id"] == "IMP3437_0_source_current_silence" and row["after_status"] == "DIRECT_MATTER_CURRENT_ZERO_IN_IDENTITY_BRANCH" for row in impact_rows),
            "detail": "source current split into direct zero plus retained indirect channels",
        },
        {
            "check_id": "VAL3437_6_local_GR_blocked",
            "condition": "local GR remains blocked",
            "passed": any(row["gate_id"] == "PG3437_4_local_GR" and row["result"] == "BLOCKED" for row in promotion_rows),
            "detail": "PPN/source/range stack still open",
        },
        {
            "check_id": "VAL3437_7_next_target",
            "condition": "next target attacks metric mixing",
            "passed": "metric-mixing" in next_rows[0]["target_doc"],
            "detail": next_rows[0]["target_doc"],
        },
        {
            "check_id": "VAL3437_8_formalization_untouched",
            "condition": "formalization-workbench modified-file count remains 0 during this run",
            "passed": modified_count == 0,
            "detail": f"modified_count_since_start={modified_count}",
        },
    ]
    validations.append(
        {
            "check_id": "VAL3437_9_overall",
            "condition": "3437 coupling checkpoint is internally valid",
            "passed": all(row["passed"] for row in validations),
            "detail": "PASS" if all(row["passed"] for row in validations) else "FAIL",
        }
    )
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    text = f"""# 3437 - q_loc Source-Current Coupling Map or Zero-Current Theorem

## Summary
- This checkpoint does take a leap: it proves a conditional zero theorem for the direct matter coupling to finite nonmetric `X_i` modes.
- In the identity-coframe branch, if matter sees only `e_obs`, `omega[e_obs]`, and species representation data, then `J_i^matter = delta S_matter/delta X_i = 0`.
- That is a real row movement from “missing coupling map” to “direct current zero branch”.
- It does not zero the full R10/PPN alpha numerator, because metric mixing, class-metric pullback, boundary/projector tails, and source-normalization readout can still source the same finite mode.
- The next best target is therefore the metric/X operator matrix: either prove block-diagonal nonmetric decoupling, or write the first explicit metric-mixing alpha numerator.

## Source Register
{md_table(rows_by_name["source_register"])}

## Coupling Branch Fork
{md_table(rows_by_name["coupling_branch_fork"])}

## Direct Matter Source-Current Theorem
{md_table(rows_by_name["direct_matter_source_current_theorem"])}

## JX Chain-Rule Audit
{md_table(rows_by_name["jx_chain_rule_audit"])}

## R10 Alpha Numerator Status
{md_table(rows_by_name["r10_alpha_numerator_status"])}

## Zero-Current Impact on 3436
{md_table(rows_by_name["zero_current_impact_on_3436"])}

## Retained Coupling Counterexamples
{md_table(rows_by_name["retained_coupling_counterexamples"])}

## Promotion Gates
{md_table(rows_by_name["promotion_gates"])}

## Decision Ledger
{md_table(rows_by_name["decision_ledger"])}

## Next Target
{md_table(rows_by_name["next_target"])}

## Runner Nonclaim
{md_table(rows_by_name["runner_nonclaim"])}

## Validation
{md_table(rows_by_name["validation"])}

## Bottom Line
This is not just another “missing” ledger: the direct matter vertex is now conditionally zeroed in the clean branch. The remaining fight is sharper and more physical: does the finite mode still get sourced indirectly through metric mixing or boundary/projector readout? That is the next punch.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    start_utc = datetime.now(timezone.utc)
    rows_by_name = {
        "source_register": source_register(),
        "coupling_branch_fork": coupling_branch_fork(),
        "direct_matter_source_current_theorem": direct_matter_source_current_theorem(),
        "jx_chain_rule_audit": jx_chain_rule_audit(),
        "r10_alpha_numerator_status": r10_alpha_numerator_status(),
        "zero_current_impact_on_3436": zero_current_impact_on_3436(),
        "retained_coupling_counterexamples": retained_coupling_counterexamples(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    rows_by_name["validation"] = validation_rows(rows_by_name, start_utc)
    for output_name, rows in rows_by_name.items():
        write_csv(OUTPUTS[output_name], rows)
    write_doc(rows_by_name)
    failed_rows = [row for row in rows_by_name["validation"] if not row["passed"]]
    if failed_rows:
        raise SystemExit(f"3437 validation failed: {failed_rows}")
    print(f"wrote {DOC}")
    print(f"wrote {len(OUTPUTS)} csv outputs")


if __name__ == "__main__":
    main()
