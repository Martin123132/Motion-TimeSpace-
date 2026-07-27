from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"

DOC_PATH = ROOT / "583-Y5-R10-parent-momentum-map-owner-or-edge-residual-demotion.md"

PRIOR_582_VALIDATION = RESIDUALS / "P8_Y5_BRR545_582_VALIDATION.csv"
PRIOR_582_SUMMARY = RESIDUALS / "P8_Y5_R10_582_NONCLAIM_SUMMARY.csv"
MOMENTUM_582 = RESIDUALS / "P8_Y5_R10_582_MOMENTUM_MAP_CLOSURE_THEOREM.csv"
DIRAC_582 = RESIDUALS / "P8_Y5_R10_582_DIRAC_BRACKET_AUDIT.csv"
BOUNDARY_582 = RESIDUALS / "P8_Y5_R10_582_BOUNDARY_DIFFERENTIABILITY_AUDIT.csv"
NOPOLE_582 = RESIDUALS / "P8_Y5_R10_582_NOPOLE_GATE_STATUS.csv"
FAILURE_582 = RESIDUALS / "P8_Y5_R10_582_FAILURE_ROUTER_TO_RESIDUALS.csv"
SOURCE_CHARGE_579 = RESIDUALS / "P8_Y5_R10_579_SOURCE_CHARGE_DECOMPOSITION.csv"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_583_SOURCE_REGISTER.csv"
OWNER_ATTEMPT_PATH = RESIDUALS / "P8_Y5_R10_583_PARENT_MOMENTUM_MAP_OWNER_ATTEMPT.csv"
NOETHER_CONTRACT_PATH = RESIDUALS / "P8_Y5_R10_583_NOETHER_MOMENTUM_MAP_CONTRACT.csv"
EDGE_DEMOTION_PATH = RESIDUALS / "P8_Y5_R10_583_EDGE_RESIDUAL_DEMOTION.csv"
ALPHA_TEMPLATE_PATH = RESIDUALS / "P8_Y5_R10_583_EDGE_ALPHA_TEMPLATE.csv"
OWNER_GATE_PATH = RESIDUALS / "P8_Y5_R10_583_OWNER_GATE_STATUS.csv"
REPAIR_QUEUE_PATH = RESIDUALS / "P8_Y5_R10_583_REPAIR_QUEUE.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_BRR545_583_DECISION.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_BRR545_583_ROUTE_UPDATE.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_583_VALIDATION.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_583_NONCLAIM_SUMMARY.csv"

STATUS = "Y5_R10_parent_momentum_map_owner_not_derived_edge_residual_demotion_template_written"
CLAIM_CEILING = "momentum_map_owner_attempt_and_edge_template_only_no_R10_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "584-Y5-R10-edge-residual-alpha-envelope-or-owner-repair.md"

SOURCE_FILES = [
    {
        "source_file": "582-Y5-R10-boundary-charge-and-constraint-algebra-no-pole-audit.md",
        "role": "immediate momentum-map gate and edge router",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BRR545_582_VALIDATION.csv",
        "role": "prior validation gate",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_582_NONCLAIM_SUMMARY.csv",
        "role": "prior nonclaim summary",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_582_MOMENTUM_MAP_CLOSURE_THEOREM.csv",
        "role": "momentum-map closure theorem template",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_582_DIRAC_BRACKET_AUDIT.csv",
        "role": "Dirac bracket/degree-count blockers",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_582_BOUNDARY_DIFFERENTIABILITY_AUDIT.csv",
        "role": "boundary differentiability and edge term blockers",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_582_NOPOLE_GATE_STATUS.csv",
        "role": "no-pole gate status",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_582_FAILURE_ROUTER_TO_RESIDUALS.csv",
        "role": "failure routes to residuals",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_579_SOURCE_CHARGE_DECOMPOSITION.csv",
        "role": "source/test charge rows that receive edge demotion",
    },
    {
        "source_file": "222-parent-X-sector-degree-count-and-boundary-action.md",
        "role": "boundary momentum B_X=n_mu P^{mu nu}",
    },
    {
        "source_file": "223-X-constraint-algebra-and-Khat-Gamma-constitutive-owner.md",
        "role": "P[Y] owner and constraint algebra blocker",
    },
    {
        "source_file": "235-projector-stress-variation-or-nohair-constraint-algebra.md",
        "role": "projector stress and P_mem owner conditions",
    },
    {
        "source_file": "scripts/Y5_R10_parent_momentum_map_owner_or_edge_residual_demotion.py",
        "role": "this checkpoint generator",
    },
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values: list[str] = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", "<br>").replace("|", "\\|")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_register() -> list[dict[str, object]]:
    return [
        {
            "source_file": item["source_file"],
            "exists": str((ROOT / str(item["source_file"])).exists()),
            "role": item["role"],
        }
        for item in SOURCE_FILES
    ]


def make_owner_attempt() -> list[dict[str, object]]:
    return [
        {
            "attempt_id": "OMA583_0_zero_momentum_map",
            "owner_route": "strict quotient action",
            "candidate_identity": "S_parent=S_red[pi(Phi)] so i_vX Omega=0 and G_X[epsilon]=0",
            "what_it_would_buy": "K_X=0, Q_edge=0, no R10 alpha row",
            "test_result": "best_if_parent_projection_derived",
            "blocker": "pi and the universal/minimal parent quotient are still not constructed",
            "demotion_if_fails": "continue to edge residual template",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "OMA583_1_noether_current_owner",
            "owner_route": "vertical Noether symmetry",
            "candidate_identity": "delta_epsilon L = E_i delta_epsilon Y^i + d theta(delta_epsilon Y) = d mu_epsilon; J_epsilon=theta-mu",
            "what_it_would_buy": "C_X becomes the bulk Noether charge density and boundary charge is the Noether surface term",
            "test_result": "contract_written",
            "blocker": "parent Lagrangian, symplectic potential theta, and mu_epsilon are not specified",
            "demotion_if_fails": "Q_edge from the uncancelled Noether surface term",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "OMA583_2_defect_potential_owner",
            "owner_route": "defect potential V_def",
            "candidate_identity": "P^{mu nu}[Y]=partial V_def/partial Z_{mu nu}; C_X^nu=-nabla_mu P^{mu nu}[Y]+J_eff^nu[Y]",
            "what_it_would_buy": "P is not free and the source identity comes from one parent variational object",
            "test_result": "promising_contract_not_derived",
            "blocker": "V_def, Z_{mu nu}, and J_eff source variation are not supplied",
            "demotion_if_fails": "P-owner missing; retain edge/projector residuals",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "OMA583_3_relative_cohomology_owner",
            "owner_route": "relative memory/current momentum map",
            "candidate_identity": "J_eff=S_L+d_rel(P_mem J_rel) with P_mem a parent-owned projector and boundary primitive exact/pure gauge",
            "what_it_would_buy": "boundary flux becomes exact or topological-zero on compact local shells",
            "test_result": "not_closed",
            "blocker": "P_mem stress and relative boundary primitive remain conditional",
            "demotion_if_fails": "Q_boundary_memory(lambda), epsilon_PiM_X(lambda)",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "OMA583_4_independent_P_rejected",
            "owner_route": "independent P^{mu nu}",
            "candidate_identity": "treat P as a free parent tensor and set C_X=-nabla P+J",
            "what_it_would_buy": "formal C_X expression only",
            "test_result": "rejected",
            "blocker": "moves the insertion from X to P and does not derive a parent identity",
            "demotion_if_fails": "not allowed as theorem route",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "OMA583_5_verdict",
            "owner_route": "owner-or-edge fork",
            "candidate_identity": "parent momentum map owner or explicit edge residual",
            "what_it_would_buy": "honest branch decision",
            "test_result": "owner_not_derived_edge_template_required",
            "blocker": "no parent Omega/theta/V_def/P_mem owner yet",
            "demotion_if_fails": "write Q_edge and alpha_edge template",
            "valid_for_claim": "false",
        },
    ]


def make_noether_contract() -> list[dict[str, object]]:
    return [
        {
            "contract_id": "NMC583_0_symplectic_potential",
            "needed_object": "parent symplectic potential",
            "mathematical_form": "delta L_parent = E_i delta Y^i + d theta_Y(delta Y)",
            "pass_condition": "theta_Y is explicit for the parent variables that own P,J_eff,P_mem",
            "current_status": "missing",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "NMC583_1_vertical_generator",
            "needed_object": "vertical transformation v_epsilon",
            "mathematical_form": "delta_epsilon Y^i = v_epsilon^i[Y], with d pi(v_epsilon)=0",
            "pass_condition": "transformation law is given for all parent fields and boundary fields",
            "current_status": "missing",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "NMC583_2_Noether_current",
            "needed_object": "Noether current",
            "mathematical_form": "J_epsilon = theta_Y(v_epsilon)-mu_epsilon",
            "pass_condition": "dJ_epsilon=-E_i v_epsilon^i and J decomposes into epsilon C_X + dQ_epsilon",
            "current_status": "template_only",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "NMC583_3_momentum_map",
            "needed_object": "Hamiltonian generator",
            "mathematical_form": "i_{v_epsilon} Omega_Y = delta G[epsilon]",
            "pass_condition": "G[epsilon]=int epsilon C_X + Q_boundary is differentiable",
            "current_status": "not_derived",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "NMC583_4_equivariance",
            "needed_object": "constraint algebra",
            "mathematical_form": "{G[epsilon],G[eta]}=G[[epsilon,eta]]+K_boundary[epsilon,eta]",
            "pass_condition": "K_boundary=0 or is forbidden/proper-gauge on compact local branch",
            "current_status": "not_computed",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "NMC583_5_boundary_zero",
            "needed_object": "edge charge silence",
            "mathematical_form": "Q_X[epsilon]=int_boundary epsilon_nu B_X^nu=0",
            "pass_condition": "epsilon proper, B_X exact/pure gauge/zero, or Pi_M^H Q_X=0 by theorem",
            "current_status": "not_derived",
            "valid_for_claim": "false",
        },
    ]


def make_edge_demotion() -> list[dict[str, object]]:
    return [
        {
            "edge_id": "ED583_0_edge_charge_definition",
            "object": "Q_edge^H(lambda)",
            "definition": "Q_edge^H(lambda)=int_{partial H} dS F_lambda(s) epsilon_nu B_X^nu(s)",
            "enters": "Q_X^H(lambda) and Qbar_XH(lambda)",
            "zero_condition": "B_X=0/exact/pure gauge or proper-gauge epsilon|boundary=0",
            "current_status": "symbolic_residual",
            "valid_for_claim": "false",
        },
        {
            "edge_id": "ED583_1_projected_edge_charge",
            "object": "Qbar_edge_XH(lambda)",
            "definition": "Qbar_edge_XH(lambda)=Pi_M^H[Q_edge^H(lambda)]/M_H",
            "enters": "alpha_edge(lambda)",
            "zero_condition": "Pi_M^H[Q_edge^H]=0 including reference-boundary terms",
            "current_status": "symbolic_residual",
            "valid_for_claim": "false",
        },
        {
            "edge_id": "ED583_2_edge_cocycle",
            "object": "K_boundary[epsilon,eta]",
            "definition": "central/boundary term in {G[epsilon],G[eta]}",
            "enters": "edge-mode/no-pole failure diagnosis",
            "zero_condition": "equivariant momentum map with no central extension on compact branch",
            "current_status": "uncomputed_residual",
            "valid_for_claim": "false",
        },
        {
            "edge_id": "ED583_3_projector_leak",
            "object": "epsilon_PiM_X(lambda)",
            "definition": "Pi_M leakage from edge/projector/source charge into measured mass channel",
            "enters": "Qbar_XH(lambda)",
            "zero_condition": "projector stress owned and mass channel orthogonal to edge charge",
            "current_status": "symbolic_residual",
            "valid_for_claim": "false",
        },
        {
            "edge_id": "ED583_4_test_charge_pair",
            "object": "qbar_XT",
            "definition": "test-body response remains needed if edge exchange couples to ordinary matter",
            "enters": "alpha_edge(lambda)=K_edge Qbar_edge_XH(lambda) qbar_XT",
            "zero_condition": "matter quotient blindness/no-marker theorem",
            "current_status": "retained_from_579",
            "valid_for_claim": "false",
        },
    ]


def make_alpha_template() -> list[dict[str, object]]:
    return [
        {
            "template_id": "EAT583_0_edge_alpha",
            "branch_id": "MTS_X_edge_residual_branch",
            "lambda_value": "MISSING_PARENT_EDGE_RANGE_OR_ENVELOPE",
            "alpha_predicted": "K_edge(lambda)*Qbar_edge_XH(lambda)*qbar_XT",
            "required_bound": "alpha_bound(lambda)",
            "source_terms": "Q_edge^H;epsilon_PiM_X;qbar_XT;K_boundary_if_dynamic",
            "valid_for_claim": "false",
            "notes": "edge residual only; do not write to live claim curve until numeric/source-backed",
        },
        {
            "template_id": "EAT583_1_no_pole_success_row",
            "branch_id": "MTS_parent_momentum_map_no_pole",
            "lambda_value": "not_applicable",
            "alpha_predicted": "0 by parent momentum-map owner plus Q_boundary=0",
            "required_bound": "not_needed_after_certificate",
            "source_terms": "owner certificate",
            "valid_for_claim": "false",
            "notes": "certificate unfilled, so not claimable",
        },
        {
            "template_id": "EAT583_2_bulk_plus_edge_fallback",
            "branch_id": "MTS_X_bulk_and_edge_residual_branch",
            "lambda_value": "lambda_X or edge envelope support",
            "alpha_predicted": "K_X*(Qbar_bulk_XH(lambda)+Qbar_edge_XH(lambda))*qbar_XT",
            "required_bound": "alpha_bound(lambda)",
            "source_terms": "bulk source;edge source;projector leak;test charge",
            "valid_for_claim": "false",
            "notes": "fallback if no-pole fails and physical/edge exchange remains",
        },
    ]


def make_owner_gate() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "OG583_0_parent_Omega",
            "gate": "parent symplectic form Omega_Y specified",
            "status": "missing",
            "gate_result": "fail_current_claim",
        },
        {
            "gate_id": "OG583_1_vertical_action",
            "gate": "vertical generator v_X acts on all parent and boundary fields",
            "status": "missing",
            "gate_result": "fail_current_claim",
        },
        {
            "gate_id": "OG583_2_momentum_map_identity",
            "gate": "i_vX Omega_Y = delta G_X",
            "status": "not_derived",
            "gate_result": "fail_current_claim",
        },
        {
            "gate_id": "OG583_3_P_J_owner",
            "gate": "P[Y], J_eff[Y], and P_mem[Y] are owned by one parent variational structure",
            "status": "not_derived",
            "gate_result": "fail_current_claim",
        },
        {
            "gate_id": "OG583_4_boundary_zero",
            "gate": "Q_boundary and K_boundary vanish or are proper-gauge on compact branch",
            "status": "not_derived",
            "gate_result": "fail_current_claim",
        },
        {
            "gate_id": "OG583_5_owner_claim",
            "gate": "all owner gates pass",
            "status": "not_passed",
            "gate_result": "no_claim",
        },
    ]


def make_repair_queue() -> list[dict[str, object]]:
    return [
        {
            "queue_id": "RQ583_0_parent_symplectic_potential",
            "missing_item": "theta_Y and Omega_Y",
            "why_needed": "turn C_X into a Hamiltonian momentum map rather than an imposed constraint",
            "acceptable_fill": "explicit parent action variation with boundary term",
            "fallback": "edge residual demotion",
        },
        {
            "queue_id": "RQ583_1_vertical_generator",
            "missing_item": "v_X on Y, P_mem, boundary fields, and matter/readout fields",
            "why_needed": "prove quotient verticality before variation",
            "acceptable_fill": "transformation law plus d pi(v_X)=0",
            "fallback": "qbar_XT/Qbar_XH retained",
        },
        {
            "queue_id": "RQ583_2_defect_potential",
            "missing_item": "V_def owner for P[Y] and source identity",
            "why_needed": "avoid free P tensor and hand-inserted C_X",
            "acceptable_fill": "P=partial V_def/partial Z and J_eff from same parent variation",
            "fallback": "P-owner blocker stays",
        },
        {
            "queue_id": "RQ583_3_boundary_charge",
            "missing_item": "Q_boundary and K_boundary calculation",
            "why_needed": "decide no-pole versus edge hair",
            "acceptable_fill": "zero/exact/pure-gauge proof or numeric/source-backed edge coefficient",
            "fallback": "Qbar_edge_XH(lambda)",
        },
        {
            "queue_id": "RQ583_4_edge_alpha_envelope",
            "missing_item": "edge range/envelope and coupling normalization",
            "why_needed": "score edge residual if owner route fails",
            "acceptable_fill": "edge kernel or bounded support plus K_edge and qbar_XT",
            "fallback": NEXT_TARGET,
        },
    ]


def make_decisions() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D583_0_owner_attempt_result",
            "decision": "parent momentum-map owner not derived",
            "meaning": "current corpus lacks Omega_Y, theta_Y, vertical generator, V_def/P owner, and boundary charge proof",
            "status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D583_1_edge_residual_demoted",
            "decision": "write edge residual template",
            "meaning": "nonzero boundary charge now has explicit Q_edge/Qbar_edge/alpha_edge placeholders instead of hiding inside gauge language",
            "status": "residual_template_written",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D583_2_no_pole_not_promoted",
            "decision": "do not promote no-pole/R10/local-GR",
            "meaning": "owner gates fail current claim and edge charge is not zeroed",
            "status": "no_claim",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D583_3_next_best_target",
            "decision": "build edge residual alpha envelope or repair owner",
            "meaning": "the next useful move is either actual edge scoring infrastructure or a concrete V_def/Omega owner proposal",
            "status": "next_derivation_target",
            "next_target": NEXT_TARGET,
        },
    ]


def make_route_update() -> list[dict[str, object]]:
    return [
        {
            "route_id": "RU583_0_allowed",
            "allowed_after_583": "cite parent momentum-map owner as an exact requirement",
            "forbidden_after_583": "claim C_X is owned without Omega/theta/v_X/V_def and boundary proof",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU583_1_allowed",
            "allowed_after_583": "route boundary hair into Qbar_edge_XH(lambda)",
            "forbidden_after_583": "drop edge charge because it is inconvenient",
            "next_action": "construct edge residual envelope",
        },
        {
            "route_id": "RU583_2_allowed",
            "allowed_after_583": "keep no-pole as conditional theorem if owner is later supplied",
            "forbidden_after_583": "treat edge residual demotion as a failed theory; it is a testable branch",
            "next_action": "edge alpha envelope or V_def repair",
        },
    ]


def make_validation(
    source_rows: list[dict[str, object]],
    prior_validation: list[dict[str, str]],
    prior_summary: list[dict[str, str]],
    owner_attempt: list[dict[str, object]],
    noether_contract: list[dict[str, object]],
    edge_demotion: list[dict[str, object]],
    alpha_template: list[dict[str, object]],
    owner_gate: list[dict[str, object]],
    repair_queue: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    missing_sources = [row["source_file"] for row in source_rows if row["exists"] != "True"]
    prior_failures = [row for row in prior_validation if row.get("result") != "pass"]
    prior_claim_allowed = any(row.get("claim_allowed") == "true" for row in prior_summary)
    has_owner_verdict = any(row["attempt_id"] == "OMA583_5_verdict" for row in owner_attempt)
    contract_all_nonclaim = all(row["valid_for_claim"] == "false" for row in noether_contract)
    has_edge_q = any(row["object"] == "Qbar_edge_XH(lambda)" for row in edge_demotion)
    has_alpha_edge = any(row["template_id"] == "EAT583_0_edge_alpha" for row in alpha_template)
    owner_gate_no_pass = all(row["gate_result"] != "pass" for row in owner_gate)
    has_boundary_repair = any(row["missing_item"] == "Q_boundary and K_boundary calculation" for row in repair_queue)
    claim_decisions = [row for row in decisions if "pass" in str(row["status"]).lower()]

    return [
        {
            "check_id": "V583_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V583_1_prior_582_clean",
            "result": "pass" if not prior_failures and not prior_claim_allowed else "fail",
            "detail": f"prior_rows={len(prior_validation)};prior_failures={len(prior_failures)};prior_claim_allowed={prior_claim_allowed}",
        },
        {
            "check_id": "V583_2_owner_attempt_verdict_written",
            "result": "pass" if has_owner_verdict else "fail",
            "detail": f"owner_rows={len(owner_attempt)};verdict={has_owner_verdict}",
        },
        {
            "check_id": "V583_3_noether_contract_nonclaim",
            "result": "pass" if contract_all_nonclaim else "fail",
            "detail": f"contract_rows={len(noether_contract)};claim_rows=0",
        },
        {
            "check_id": "V583_4_edge_residual_template_written",
            "result": "pass" if has_edge_q and has_alpha_edge else "fail",
            "detail": f"edge_rows={len(edge_demotion)};alpha_templates={len(alpha_template)}",
        },
        {
            "check_id": "V583_5_owner_gates_not_promoted",
            "result": "pass" if owner_gate_no_pass else "fail",
            "detail": f"owner_gate_rows={len(owner_gate)};pass_rows=0",
        },
        {
            "check_id": "V583_6_repair_queue_targets_boundary",
            "result": "pass" if has_boundary_repair else "fail",
            "detail": f"repair_rows={len(repair_queue)};boundary_repair={has_boundary_repair}",
        },
        {
            "check_id": "V583_7_no_R10_or_local_GR_claim",
            "result": "pass" if not claim_decisions else "fail",
            "detail": "claim_allowed=false;R10_pass=false;WEP=false;PPN=false;local_GR=false",
        },
    ]


def write_markdown(
    generated: str,
    source_rows: list[dict[str, object]],
    owner_attempt: list[dict[str, object]],
    noether_contract: list[dict[str, object]],
    edge_demotion: list[dict[str, object]],
    alpha_template: list[dict[str, object]],
    owner_gate: list[dict[str, object]],
    repair_queue: list[dict[str, object]],
    decisions: list[dict[str, object]],
    route_update: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    body = f"""# 583 Y5 R10 parent momentum-map owner or edge residual demotion

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`

## Verdict
- I tried to make `C_X` parent-owned as a true momentum map. The theorem shape is exact, but the current corpus does not yet supply the parent symplectic potential, vertical generator, `V_def`/`P[Y]` owner, or boundary charge proof.
- Therefore no-pole is not promoted.
- The edge term is now demoted honestly: if `Q_boundary` or `K_boundary` survives, it becomes `Qbar_edge_XH(lambda)` and feeds an explicit `alpha_edge(lambda)` residual row.

## Owner Equation
```text
delta L_parent = E_i delta Y^i + d theta_Y(delta Y)
delta_epsilon Y = v_epsilon[Y]
J_epsilon = theta_Y(v_epsilon) - mu_epsilon
G[epsilon] = int_Sigma epsilon_nu C_X^nu + Q_boundary[epsilon]
i_{{v_epsilon}} Omega_Y = delta G[epsilon]
```

No-pole credit requires this owner equation plus:

```text
Q_boundary[epsilon]=0,
K_boundary[epsilon,eta]=0,
P[Y], J_eff[Y], P_mem[Y] owned by the same parent variational structure.
```

That is not derived yet. The edge-hair fallback is therefore:

```text
Qbar_edge_XH(lambda)=Pi_M^H[Q_edge^H(lambda)]/M_H
alpha_edge(lambda)=K_edge(lambda) Qbar_edge_XH(lambda) qbar_XT.
```

## Source Register
{markdown_table(source_rows, ["source_file", "exists", "role"])}

## Parent Momentum-Map Owner Attempt
{markdown_table(owner_attempt, ["attempt_id", "owner_route", "candidate_identity", "what_it_would_buy", "test_result", "blocker", "demotion_if_fails", "valid_for_claim"])}

## Noether Momentum-Map Contract
{markdown_table(noether_contract, ["contract_id", "needed_object", "mathematical_form", "pass_condition", "current_status", "valid_for_claim"])}

## Edge Residual Demotion
{markdown_table(edge_demotion, ["edge_id", "object", "definition", "enters", "zero_condition", "current_status", "valid_for_claim"])}

## Edge Alpha Template
{markdown_table(alpha_template, ["template_id", "branch_id", "lambda_value", "alpha_predicted", "required_bound", "source_terms", "valid_for_claim", "notes"])}

## Owner Gate Status
{markdown_table(owner_gate, ["gate_id", "gate", "status", "gate_result"])}

## Repair Queue
{markdown_table(repair_queue, ["queue_id", "missing_item", "why_needed", "acceptable_fill", "fallback"])}

## Decision
{markdown_table(decisions, ["decision_id", "decision", "meaning", "status", "next_target"])}

## Route Update
{markdown_table(route_update, ["route_id", "allowed_after_583", "forbidden_after_583", "next_action"])}

## Validation
{markdown_table(validation, ["check_id", "result", "detail"])}

## Practical Read
This checkpoint is the honest fork. The elegant win is still possible, but it needs a real parent momentum map, not a symbolic `C_X`. Until then, the edge term is not swept under the rug: it is promoted to a named residual coefficient. That is good discipline. It means the theory either earns no-pole, or it becomes testable through an edge `alpha(lambda)` envelope.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    generated = datetime.now(timezone.utc).isoformat()
    source_rows = source_register()
    prior_validation = read_csv(PRIOR_582_VALIDATION)
    prior_summary = read_csv(PRIOR_582_SUMMARY)
    momentum_582 = read_csv(MOMENTUM_582)
    dirac_582 = read_csv(DIRAC_582)
    boundary_582 = read_csv(BOUNDARY_582)
    nopole_582 = read_csv(NOPOLE_582)
    failure_582 = read_csv(FAILURE_582)
    source_charge_579 = read_csv(SOURCE_CHARGE_579)

    owner_attempt = make_owner_attempt()
    noether_contract = make_noether_contract()
    edge_demotion = make_edge_demotion()
    alpha_template = make_alpha_template()
    owner_gate = make_owner_gate()
    repair_queue = make_repair_queue()
    decisions = make_decisions()
    route_update = make_route_update()
    validation = make_validation(
        source_rows,
        prior_validation,
        prior_summary,
        owner_attempt,
        noether_contract,
        edge_demotion,
        alpha_template,
        owner_gate,
        repair_queue,
        decisions,
    )

    summary_rows = [
        {
            "summary_id": "S583_0_result",
            "status": STATUS,
            "parent_momentum_map_owner_derived": "false",
            "edge_residual_template_written": "true",
            "no_pole_theorem_claim": "false",
            "finite_branch_retained": "true",
            "claim_allowed": "false",
            "R10_pass_for_claim": "false",
            "WEP_pass": "false",
            "PPN_pass": "false",
            "local_GR_pass": "false",
            "momentum_rows_reused": len(momentum_582),
            "dirac_rows_reused": len(dirac_582),
            "boundary_rows_reused": len(boundary_582),
            "nopole_gate_rows_reused": len(nopole_582),
            "failure_router_rows_reused": len(failure_582),
            "source_charge_rows_reused": len(source_charge_579),
            "next_target": NEXT_TARGET,
        }
    ]

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_file", "exists", "role"])
    write_csv(
        OWNER_ATTEMPT_PATH,
        owner_attempt,
        ["attempt_id", "owner_route", "candidate_identity", "what_it_would_buy", "test_result", "blocker", "demotion_if_fails", "valid_for_claim"],
    )
    write_csv(
        NOETHER_CONTRACT_PATH,
        noether_contract,
        ["contract_id", "needed_object", "mathematical_form", "pass_condition", "current_status", "valid_for_claim"],
    )
    write_csv(
        EDGE_DEMOTION_PATH,
        edge_demotion,
        ["edge_id", "object", "definition", "enters", "zero_condition", "current_status", "valid_for_claim"],
    )
    write_csv(
        ALPHA_TEMPLATE_PATH,
        alpha_template,
        ["template_id", "branch_id", "lambda_value", "alpha_predicted", "required_bound", "source_terms", "valid_for_claim", "notes"],
    )
    write_csv(OWNER_GATE_PATH, owner_gate, ["gate_id", "gate", "status", "gate_result"])
    write_csv(REPAIR_QUEUE_PATH, repair_queue, ["queue_id", "missing_item", "why_needed", "acceptable_fill", "fallback"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "meaning", "status", "next_target"])
    write_csv(ROUTE_UPDATE_PATH, route_update, ["route_id", "allowed_after_583", "forbidden_after_583", "next_action"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_csv(
        SUMMARY_PATH,
        summary_rows,
        [
            "summary_id",
            "status",
            "parent_momentum_map_owner_derived",
            "edge_residual_template_written",
            "no_pole_theorem_claim",
            "finite_branch_retained",
            "claim_allowed",
            "R10_pass_for_claim",
            "WEP_pass",
            "PPN_pass",
            "local_GR_pass",
            "momentum_rows_reused",
            "dirac_rows_reused",
            "boundary_rows_reused",
            "nopole_gate_rows_reused",
            "failure_router_rows_reused",
            "source_charge_rows_reused",
            "next_target",
        ],
    )

    write_markdown(
        generated,
        source_rows,
        owner_attempt,
        noether_contract,
        edge_demotion,
        alpha_template,
        owner_gate,
        repair_queue,
        decisions,
        route_update,
        validation,
    )

    all_passed = all(row["result"] == "pass" for row in validation)
    print(
        json.dumps(
            {
                "generated_at_utc": generated,
                "status": STATUS,
                "claim_ceiling": CLAIM_CEILING,
                "doc": str(DOC_PATH.relative_to(ROOT)),
                "validation": str(VALIDATION_PATH.relative_to(ROOT)),
                "next_target": NEXT_TARGET,
                "all_validation_passed": all_passed,
                "parent_momentum_map_owner_derived": False,
                "edge_residual_template_written": True,
                "claim_allowed": False,
            },
            indent=2,
        )
    )
    if not all_passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
