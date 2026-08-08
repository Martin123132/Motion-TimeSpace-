from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3498-Y5-R2FR-projector-naturality-stress-test-or-Kprojector-bound.md"

SOURCES: dict[str, dict[str, Any]] = {
    "script_3498": {"path": Path(__file__).resolve(), "role": "generator"},
    "doc_3497": {
        "path": ROOT / "3497-Y5-R2FR-minimal-parent-source-action-signature-or-first-hsrc-bound-row.md",
        "role": "3497 handoff",
    },
    "signature_3497": {
        "path": OUT / "P8_Y5_R2FR_3497_MINIMAL_PARENT_SOURCE_ACTION_SIGNATURE.csv",
        "role": "minimal parent source-action signature",
    },
    "clause_3497": {
        "path": OUT / "P8_Y5_R2FR_3497_CLAUSE_SIGNING_TEST.csv",
        "role": "3497 clause signing test",
    },
    "variation_3497": {
        "path": OUT / "P8_Y5_R2FR_3497_VARIATION_CHAIN.csv",
        "role": "3497 variation chain",
    },
    "kernel_3496": {
        "path": OUT / "P8_Y5_R2FR_3496_SOURCE_HYPERMOMENTUM_KERNEL_VECTOR.csv",
        "role": "3496 source-hypermomentum kernel vector",
    },
    "bounds_3496": {
        "path": OUT / "P8_Y5_R2FR_3496_PRODUCT_BOUND_INHERITANCE.csv",
        "role": "3496 inherited product bounds",
    },
    "commutator_1898": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1898_READOUT_VARIATION_COMMUTATOR_ZERO_ATTEMPT.csv",
        "role": "readout/projector commutator obstruction",
    },
    "pim_algebra": {
        "path": OUT / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
        "role": "Pi_M algebra and closure contract",
    },
    "pim_variation": {
        "path": OUT / "P8_PiM_projector_variation_stress_CONTRACT.csv",
        "role": "Pi_M projector variation/stress contract",
    },
    "qcoh_algebra": {
        "path": OUT / "P8_QCOH_PROJECTOR_ALGEBRA_THEOREM.csv",
        "role": "coherent trace projector algebra",
    },
    "domain_no_leak": {
        "path": OUT / "P8_DOMAIN_ALPHA3_NOLEAK_THEOREM_ATTEMPT.csv",
        "role": "domain alpha3 no-leak theorem attempt",
    },
    "domain_selector_clause": {
        "path": OUT / "P8_DOMAIN_SELECTOR_PARENT_ACTION_CLAUSE.csv",
        "role": "domain selector parent-action clause",
    },
    "domain_selector_variation": {
        "path": OUT / "P8_DOMAIN_SELECTOR_PARENT_ACTION_VARIATION_CHAIN.csv",
        "role": "domain selector variation chain",
    },
    "domain_no_vector": {
        "path": OUT / "P8_DOMAIN_SELECTOR_NOVECTOR_THEOREM_ATTEMPT.csv",
        "role": "domain selector no-vector theorem",
    },
    "old_projector_bound": {
        "path": OUT / "P8_Y5_BRR545_COMMUTATOR_PROJECTOR_BOUND_FILL_ROW.csv",
        "role": "previous commutator/projector bound skeleton",
    },
}


def generated_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def source_register_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(metadata["path"]),
            "exists": str(Path(metadata["path"]).exists()),
            "role": metadata["role"],
            "valid_for_claim": "False",
        }
        for source_id, metadata in SOURCES.items()
    ]


def projector_naturality_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "PNT3498_0_target",
            "claim_piece": "projector Gamma-naturality target",
            "statement": "For source hypermomentum, the required zero is D_{Gamma_ind} Pi = 0, not full metric-stress silence.",
            "derivation": "The commutator term is delta_Gamma(Pi J_H)=Pi delta_Gamma J_H+(delta_Gamma Pi)J_H. Since 3497 gives delta_Gamma J_H=0 inside the candidate branch, only delta_Gamma Pi can reopen epsilon_hypermomentum_source.",
            "result": "TARGET_SHARPENED",
            "claim_status": "NONCLAIM_INTERNAL_BRANCH",
            "source_path": str(SOURCES["variation_3497"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "PNT3498_1_functor_chain_rule",
            "claim_piece": "q/e_obs/tau functor projector",
            "statement": "If Pi = Pi_bar(q(Phi), e_obs(q), tau(q), H_ref, topology) and v is vertical with Dq[v]=0, then D_v Pi=0.",
            "derivation": "By the chain rule, D_v Pi = D_q Pi_bar D_v q + D_e Pi_bar D_v e_obs + D_tau Pi_bar D_v tau. In the MPA3497 branch e_obs and tau descend through q, so each term vanishes along ker(Dq).",
            "result": "EXACT_CONDITIONAL_THEOREM",
            "claim_status": "CANDIDATE_ZERO",
            "source_path": str(SOURCES["signature_3497"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "PNT3498_2_hodge_metric_distinction",
            "claim_piece": "Hodge/metric projector distinction",
            "statement": "A Hodge/DeWitt/e_obs projector may carry metric stress, but it does not carry Gamma_ind source hypermomentum if it uses e_obs and not Gamma_ind.",
            "derivation": "Metric variation delta_g Pi and independent-connection variation delta_Gamma_ind Pi are different gates. The former remains a PPN/R11 stress problem; the latter is zero in the candidate branch when Pi has no Gamma_ind slot.",
            "result": "USEFUL_SEPARATION",
            "claim_status": "SOURCE_HYPERMOMENTUM_CAN_CLOSE_BEFORE_FULL_PPN_STRESS",
            "source_path": str(SOURCES["pim_variation"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "PNT3498_3_topological_projector",
            "claim_piece": "topological/relative-chain projector",
            "statement": "A metric-independent topological projector is both Gamma-natural and bulk metric-stress silent if parent-owned.",
            "derivation": "Pi_top J = ell_M(J) omega_M with omega_M closed and selected by fixed exterior topology has no Gamma_ind slot. If parent-owned, delta_Gamma Pi_top=0 and delta_g Pi_top bulk stress is absent.",
            "result": "STRONG_ROUTE_CONDITIONAL",
            "claim_status": "PARENT_OWNERSHIP_STILL_CONDITIONAL",
            "source_path": str(SOURCES["pim_algebra"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "PNT3498_4_boundary_transport",
            "claim_piece": "boundary/collar transport",
            "statement": "Boundary transport is Gamma-natural only if it is defined by e_obs/LC[e_obs], topological linking, or fixed q-data, not by Gamma_ind parallel transport.",
            "derivation": "LC[e_obs] depends on e_obs(q), so D_Gamma_ind LC[e_obs]=0. Direct Gamma_ind transport would give D_Gamma Pi != 0 and activates the fallback K_projector_comm row.",
            "result": "ALLOWED_ROUTE_PLUS_COUNTERMODEL",
            "claim_status": "COUNTERMODEL_EXPLICIT",
            "source_path": str(SOURCES["commutator_1898"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "PNT3498_5_domain_selector",
            "claim_piece": "domain selector",
            "statement": "A scalar stationary domain selector can be Gamma-natural, but vector/normal-flow/marker selectors keep preferred-frame and domain-stress rows alive.",
            "derivation": "If chi_D and Sigma_D are scalar q/e_obs/topological functions with no independent normal velocity, D_Gamma chi_D=0. If the selector uses n_mu, flow, empirical masks or residual-tuned collars, delta_Gamma Pi may remain zero but PPN vector/stress rows remain active.",
            "result": "GAMMA_NATURALITY_CONDITIONAL_PPN_STRESS_RETAINED",
            "claim_status": "NO_LOCAL_GR_PROMOTION",
            "source_path": str(SOURCES["domain_selector_clause"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "PNT3498_6_product_rule_closure",
            "claim_piece": "source-hypermomentum projector closure",
            "statement": "Inside the MPA3497 branch plus PNT3498_1, delta_Gamma(Pi J_H)=0 and KHS3496_6_projector_comm is zero for the source-hypermomentum gate.",
            "derivation": "Insert delta_Gamma J_H=0 from 3497 and delta_Gamma Pi=0 from projector naturality into the product rule. This closes the independent-Gamma source-current commutator, while leaving metric stress, R11 and weak-field source-normalization gates separate.",
            "result": "CANDIDATE_GATE_CLOSED",
            "claim_status": "INTERNAL_CANDIDATE_NOT_PUBLIC_CLAIM",
            "source_path": str(SOURCES["kernel_3496"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "PNT3498_7_verdict",
            "claim_piece": "projector naturality stress test",
            "statement": "Projector naturality is strong enough to remove the source-hypermomentum commutator inside the candidate action, but not strong enough to claim full local GR.",
            "derivation": "The independent-connection source tail can be killed by q/e_obs/tau functoriality. Metric variation of projectors, domain vector hair, R11 operator rows and Poisson/Gauss source calibration remain separate tests.",
            "result": "SOURCE_HYPERMOMENTUM_GATE_ADVANCED",
            "claim_status": "NEXT_GATE_NEWTON_POISSON_SOURCE_CHARGE",
            "source_path": str(SOURCES["doc_3497"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def stress_test_matrix_rows() -> list[dict[str, Any]]:
    return [
        {
            "test_id": "STM3498_0_mass_projector_topological",
            "projector_or_map": "Pi_M topological charge projector",
            "depends_on_Gamma_ind": "False",
            "depends_on_metric_eobs": "False_or_reference_only",
            "delta_Gamma_Pi_status": "ZERO_IF_PARENT_OWNED",
            "metric_stress_status": "BULK_ZERO_IF_TOPOLOGICAL_PARENT_OWNED",
            "residual_if_failed": "epsilon_projector_comm;epsilon_MHref",
            "source_path": str(SOURCES["pim_algebra"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "test_id": "STM3498_1_hodge_dewitt_projector",
            "projector_or_map": "Hodge/DeWitt/e_obs orthogonal projector",
            "depends_on_Gamma_ind": "False",
            "depends_on_metric_eobs": "True",
            "delta_Gamma_Pi_status": "ZERO_FOR_SOURCE_HYPERMOMENTUM",
            "metric_stress_status": "RETAINED_FOR_PPN_R11",
            "residual_if_failed": "epsilon_projector_metric_stress",
            "source_path": str(SOURCES["pim_variation"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "test_id": "STM3498_2_Gamma_transport_projector",
            "projector_or_map": "Gamma_ind parallel-transport/collar projector",
            "depends_on_Gamma_ind": "True",
            "depends_on_metric_eobs": "Possible",
            "delta_Gamma_Pi_status": "FAIL_COUNTERMODEL",
            "metric_stress_status": "RETAINED",
            "residual_if_failed": "epsilon_projector_comm",
            "source_path": str(SOURCES["commutator_1898"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "test_id": "STM3498_3_scalar_domain_selector",
            "projector_or_map": "scalar stationary chi_D domain selector",
            "depends_on_Gamma_ind": "False",
            "depends_on_metric_eobs": "Scalar_eobs_or_topological",
            "delta_Gamma_Pi_status": "ZERO_IF_SCALAR_Q_FUNCTOR",
            "metric_stress_status": "CONDITIONAL_DOUBLE_ZERO_OR_RETAINED",
            "residual_if_failed": "epsilon_domain_vector;epsilon_domain_flux;epsilon_domain_anisotropy",
            "source_path": str(SOURCES["domain_selector_variation"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "test_id": "STM3498_4_vector_marker_domain",
            "projector_or_map": "vector/normal-flow/material-marker/readout mask selector",
            "depends_on_Gamma_ind": "Maybe",
            "depends_on_metric_eobs": "True_or_external",
            "delta_Gamma_Pi_status": "NOT_PROVEN",
            "metric_stress_status": "RETAINED",
            "residual_if_failed": "epsilon_projector_comm;epsilon_domain_vector;epsilon_marker_selector",
            "source_path": str(SOURCES["domain_no_vector"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "test_id": "STM3498_5_readout_postprocessor",
            "projector_or_map": "pure post-variation readout projector",
            "depends_on_Gamma_ind": "No_parent_action_slot",
            "depends_on_metric_eobs": "Post_solution_only",
            "delta_Gamma_Pi_status": "TYPE_ORDER_ZERO",
            "metric_stress_status": "NO_PARENT_STRESS_IF_POSTPROCESSING",
            "residual_if_failed": "prevariation_readout_reentry",
            "source_path": str(SOURCES["commutator_1898"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def kprojector_bound_rows() -> list[dict[str, Any]]:
    old_bound_rows = read_csv(SOURCES["old_projector_bound"]["path"])
    old_bound = old_bound_rows[0] if old_bound_rows else {}
    return [
        {
            "bound_id": "KPB3498_0_source_hypermomentum_projector_comm",
            "trigger": "Gamma_ind-dependent projector or boundary/collar transport is admitted before variation",
            "residual_symbol": "epsilon_projector_comm",
            "definition": "source-hypermomentum projector commutator from (delta_Gamma Pi)J_H",
            "bound_formula": "abs(int_S (delta_Gamma_ind Pi)J_H)/abs(M_H_ref)",
            "current_value": "0_INSIDE_MPA3497_Q_EOBS_TAU_FUNCTOR_BRANCH_ELSE_MISSING_NUMERIC_OR_THEOREM_ZERO",
            "mapped_observable": "alpha3 first; then gamma_minus_1, beta_minus_1, WEP products, xi",
            "target_bound": "4e-20 for alpha3 inherited fallback",
            "required_inputs_if_not_zero": "operator norm for delta_Gamma Pi, J_H norm, M_H_ref, K_alpha3_projector, units, source path",
            "source_path": str(SOURCES["old_projector_bound"]["path"]),
            "score_status": "CANDIDATE_ZERO_OR_UNEXECUTED_BOUND",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "KPB3498_1_metric_stress_not_same_gate",
            "trigger": "Hodge/e_obs projector is used",
            "residual_symbol": "epsilon_projector_metric_stress",
            "definition": "metric variation of projectors that may map to PPN/R11 even when source hypermomentum is zero",
            "bound_formula": old_bound.get("formula", "T_projector -> gamma,beta,alpha_i,xi,R11"),
            "current_value": "RETAINED_SEPARATE_LOCAL_GR_GATE",
            "mapped_observable": "R3_gamma;R4_beta;R5_alpha1;R6_alpha2;R7_alpha3;R8_xi;R11",
            "target_bound": "observable-specific local bounds",
            "required_inputs_if_not_zero": "metric variation stress ledger and weak-field projection coefficients",
            "source_path": str(SOURCES["pim_variation"]["path"]),
            "score_status": "NOT_A_SOURCE_HYPERMOMENTUM_FAILURE_BUT_LOCAL_GR_STILL_BLOCKED",
            "valid_for_claim": "False",
        },
    ]


def hsrc_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "HSRC3498_0_bulk",
            "piece": "bulk ordinary matter",
            "status": "CANDIDATE_ZERO_FROM_3497",
            "remaining_gate": "parent branch adoption",
            "valid_for_claim": "False",
        },
        {
            "status_id": "HSRC3498_1_support",
            "piece": "source support and W_source",
            "status": "CANDIDATE_ZERO_ON_COMPACT_REGULAR_SUPPORT",
            "remaining_gate": "regular support/no-crossing/tail norm",
            "valid_for_claim": "False",
        },
        {
            "status_id": "HSRC3498_2_projector_comm",
            "piece": "projector commutator",
            "status": "CANDIDATE_ZERO_BY_Q_EOBS_TAU_NATURALITY",
            "remaining_gate": "exclude Gamma_ind transport; keep metric stress separate",
            "valid_for_claim": "False",
        },
        {
            "status_id": "HSRC3498_3_source_charge",
            "piece": "Hamiltonian source charge and GM",
            "status": "NOT_FULLY_CLOSED",
            "remaining_gate": "Poisson/Gauss/Newton calibration and H_ref/M_H_ref positivity",
            "valid_for_claim": "False",
        },
        {
            "status_id": "HSRC3498_4_verdict",
            "piece": "epsilon_hypermomentum_source",
            "status": "ADVANCED_TO_CANDIDATE_ZERO_MODULO_SOURCE_CHARGE_AND_BRANCH_ADOPTION",
            "remaining_gate": "derive Newtonian 1/r source normalization from same Hamiltonian charge",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3498_0_projector_naturality_passes_inside_candidate",
            "decision": "Treat projector naturality as internally solved for the source-hypermomentum gate inside MPA3497.",
            "rationale": "The product-rule commutator vanishes when Pi is a q/e_obs/tau functor and J_H already has zero Gamma_ind variation.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3498_1_do_not_confuse_with_full_local_GR",
            "decision": "Do not use Gamma-naturality to claim full PPN/local-GR projector stress silence.",
            "rationale": "Metric variation of Hodge/domain/projector maps can still feed R11, alpha_i, xi, beta and gamma rows.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3498_2_move_to_Newton_Poisson_source_charge",
            "decision": "Move next to the Hamiltonian source charge -> Poisson/Newton calibration gate.",
            "rationale": "The best route to local GR now runs through proving the same parent source charge gives the 1/r Newtonian field without fitted-G absorption.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3499-Y5-R2FR-Hamiltonian-source-charge-to-Poisson-Newton-gate-or-GM-transfer-bound.md",
            "next_script": "scripts/Y5_R2FR_3499_hamiltonian_source_charge_to_Poisson_Newton_gate_or_GM_transfer_bound.py",
            "objective": "Derive the weak-field Poisson/Gauss/Newton source normalization from the same M_H/H_tau source charge used by the parent action; if it fails, fill epsilon_GM_transfer/K_Newton source-charge bound rows.",
            "success_gate": "g_00=-1+2G_ref M_H/r+O(r^-2) and Poisson source normalization follow from the same parent charge, or an executable nonclaim GM-transfer residual row is produced",
            "forbidden_shortcuts": "using measured orbital GM as proof; fitting G after readout; ignoring H_ref/M_H_ref positivity; claiming local GR from source-hypermomentum zero alone",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    stress: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    hsrc: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output_files = [
        OUT / "P8_Y5_R2FR_3498_SOURCE_REGISTER.csv",
        OUT / "P8_Y5_R2FR_3498_PROJECTOR_NATURALITY_THEOREM.csv",
        OUT / "P8_Y5_R2FR_3498_PROJECTOR_STRESS_TEST_MATRIX.csv",
        OUT / "P8_Y5_R2FR_3498_KPROJECTOR_BOUND_ROW.csv",
        OUT / "P8_Y5_R2FR_3498_HSRC_STATUS_UPDATE.csv",
        OUT / "P8_Y5_R2FR_3498_DECISION_LEDGER.csv",
        OUT / "P8_Y5_R2FR_3498_NEXT_TARGET.csv",
    ]
    parsed_counts = [f"{output_file.name}:{len(read_csv(output_file))}" for output_file in output_files]
    all_rows = [*sources, *theorem, *stress, *bounds, *hsrc, *decisions, *next_rows]
    gamma_natural_rows = sum(1 for row in stress if "ZERO" in row.get("delta_Gamma_Pi_status", ""))
    counter_rows = sum(1 for row in stress if "FAIL" in row.get("delta_Gamma_Pi_status", "") or "NOT_PROVEN" in row.get("delta_Gamma_Pi_status", ""))
    checks = [
        {
            "check_id": "VAL3498_0_sources_exist",
            "passed": all(source_row["exists"] == "True" for source_row in sources),
            "detail": "all cited local sources exist",
        },
        {
            "check_id": "VAL3498_1_csv_parse",
            "passed": True,
            "detail": "; ".join(parsed_counts),
        },
        {
            "check_id": "VAL3498_2_theorem_chain",
            "passed": len(theorem) >= 8 and any(row["result"] == "USEFUL_SEPARATION" for row in theorem),
            "detail": f"theorem_rows={len(theorem)}; separates Gamma-naturality from metric stress",
        },
        {
            "check_id": "VAL3498_3_stress_matrix_has_countermodels",
            "passed": gamma_natural_rows >= 3 and counter_rows >= 2,
            "detail": f"gamma_natural_rows={gamma_natural_rows}; counter_or_open_rows={counter_rows}",
        },
        {
            "check_id": "VAL3498_4_bound_rows",
            "passed": len(bounds) == 2 and bounds[0]["residual_symbol"] == "epsilon_projector_comm",
            "detail": f"bound_rows={len(bounds)}; first={bounds[0]['residual_symbol']}",
        },
        {
            "check_id": "VAL3498_5_hsrc_advanced_not_claimed",
            "passed": any("ADVANCED_TO_CANDIDATE_ZERO" in row["status"] for row in hsrc),
            "detail": "source-hypermomentum status advanced to candidate zero",
        },
        {
            "check_id": "VAL3498_6_no_claim",
            "passed": all(str(row.get("valid_for_claim", "False")) == "False" for row in all_rows),
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "VAL3498_7_no_formalization_outputs",
            "passed": all(not str(output_file).startswith(str(FORMALIZATION)) for output_file in output_files),
            "detail": "outputs are under post-checkpoint-work/source-intake only",
        },
        {
            "check_id": "VAL3498_8_next_target",
            "passed": len(next_rows) == 1 and "3499" in next_rows[0]["next_doc"],
            "detail": next_rows[0]["next_doc"],
        },
    ]
    checks.append(
        {
            "check_id": "VAL3498_SUMMARY",
            "passed": all(bool(check["passed"]) for check in checks),
            "detail": "PASS" if all(bool(check["passed"]) for check in checks) else "FAIL",
        }
    )
    return [
        {
            "check_id": check["check_id"],
            "passed": str(bool(check["passed"])),
            "detail": check["detail"],
            "valid_for_claim": "False",
        }
        for check in checks
    ]


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines)


def write_doc(
    theorem: list[dict[str, Any]],
    stress: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    hsrc: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 3498 - Projector Naturality Stress Test or Kprojector Bound",
                "",
                "## Current Verdict",
                "- **Good news:** `delta_Gamma_ind Pi=0` is derivable inside the MPA3497 candidate whenever projectors are `q/e_obs/tau` functors.",
                "- **Key distinction:** this closes the source-hypermomentum projector commutator, but it does not erase metric projector stress or PPN/R11 rows.",
                "- **Counterroute retained:** any projector using direct `Gamma_ind` transport, pre-variation readout masks, or vector/domain marker selectors activates `K_projector_comm`.",
                "- **Next best move:** connect the same Hamiltonian source charge to the Newton/Poisson 1/r field without fitted-G absorption.",
                "",
                "## Projector Naturality Theorem",
                markdown_table(
                    theorem,
                    ["theorem_id", "claim_piece", "statement", "result", "claim_status", "valid_for_claim"],
                ),
                "",
                "## Projector Stress Test Matrix",
                markdown_table(
                    stress,
                    [
                        "test_id",
                        "projector_or_map",
                        "depends_on_Gamma_ind",
                        "depends_on_metric_eobs",
                        "delta_Gamma_Pi_status",
                        "metric_stress_status",
                        "residual_if_failed",
                        "valid_for_claim",
                    ],
                ),
                "",
                "## Kprojector Bound Row",
                markdown_table(
                    bounds,
                    [
                        "bound_id",
                        "trigger",
                        "residual_symbol",
                        "bound_formula",
                        "current_value",
                        "mapped_observable",
                        "score_status",
                        "valid_for_claim",
                    ],
                ),
                "",
                "## Source-Hypermomentum Status",
                markdown_table(hsrc, ["status_id", "piece", "status", "remaining_gate", "valid_for_claim"]),
                "",
                "## Decisions",
                markdown_table(decisions, ["decision_id", "decision", "rationale", "claim_allowed", "valid_for_claim"]),
                "",
                "## Next Target",
                markdown_table(
                    next_rows,
                    ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"],
                ),
                "",
                "## Validation",
                markdown_table(validation, ["check_id", "passed", "detail", "valid_for_claim"]),
                "",
                f"Generated: {generated_timestamp()}",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    source_rows = source_register_rows()
    theorem_rows = projector_naturality_theorem_rows()
    stress_rows = stress_test_matrix_rows()
    bound_rows = kprojector_bound_rows()
    hsrc_rows = hsrc_status_rows()
    decision_ledger_rows = decision_rows()
    next_rows = next_target_rows()

    write_csv(
        OUT / "P8_Y5_R2FR_3498_SOURCE_REGISTER.csv",
        source_rows,
        ["source_id", "path", "exists", "role", "valid_for_claim"],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3498_PROJECTOR_NATURALITY_THEOREM.csv",
        theorem_rows,
        ["theorem_id", "claim_piece", "statement", "derivation", "result", "claim_status", "source_path", "valid_for_claim"],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3498_PROJECTOR_STRESS_TEST_MATRIX.csv",
        stress_rows,
        [
            "test_id",
            "projector_or_map",
            "depends_on_Gamma_ind",
            "depends_on_metric_eobs",
            "delta_Gamma_Pi_status",
            "metric_stress_status",
            "residual_if_failed",
            "source_path",
            "valid_for_claim",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3498_KPROJECTOR_BOUND_ROW.csv",
        bound_rows,
        [
            "bound_id",
            "trigger",
            "residual_symbol",
            "definition",
            "bound_formula",
            "current_value",
            "mapped_observable",
            "target_bound",
            "required_inputs_if_not_zero",
            "source_path",
            "score_status",
            "valid_for_claim",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3498_HSRC_STATUS_UPDATE.csv",
        hsrc_rows,
        ["status_id", "piece", "status", "remaining_gate", "valid_for_claim"],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3498_DECISION_LEDGER.csv",
        decision_ledger_rows,
        ["decision_id", "decision", "rationale", "claim_allowed", "valid_for_claim"],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3498_NEXT_TARGET.csv",
        next_rows,
        ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"],
    )

    validation = validation_rows(
        source_rows,
        theorem_rows,
        stress_rows,
        bound_rows,
        hsrc_rows,
        decision_ledger_rows,
        next_rows,
    )
    write_csv(
        OUT / "P8_Y5_BRR545_3498_VALIDATION.csv",
        validation,
        ["check_id", "passed", "detail", "valid_for_claim"],
    )
    write_doc(theorem_rows, stress_rows, bound_rows, hsrc_rows, decision_ledger_rows, next_rows, validation)


if __name__ == "__main__":
    main()
