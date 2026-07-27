from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3431-Y5-R2FR-domain-projector-no-stress-theorem-or-operator-bound-under-AX1090.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCES = {
    "doc_3430": ROOT / "3430-Y5-R2FR-hidden-projector-channelwise-bound-or-exclusion-under-AX1090.md",
    "channel_audit_3430": OUT / "P8_Y5_R2FR_3430_CHANNELWISE_EXCLUSION_AUDIT.csv",
    "bound_rows_3430": OUT / "P8_Y5_R2FR_3430_HIDDEN_PROJECTOR_BOUND_ROWS.csv",
    "validation_3430": OUT / "P8_Y5_BRR545_3430_VALIDATION.csv",
    "projector_stress_2407": OUT / "P8_Y5_PARENT_QLOC_2407_PROJECTOR_VARIATION_STRESS_AUDIT.csv",
    "domain_projector_coeffs": OUT / "P8_mu_extra_domain_projector_coefficients.csv",
    "qcoh_projector_algebra": OUT / "P8_QCOH_PROJECTOR_ALGEBRA_THEOREM.csv",
    "qcoh_parent_projector_sources": OUT / "P8_QCOH_PARENT_PROJECTOR_SOURCE_REGISTER.csv",
    "domain_selector_novector_sources": OUT / "P8_DOMAIN_SELECTOR_NOVECTOR_SOURCE_REGISTER.csv",
    "domain_selector_parent_sources": OUT / "P8_DOMAIN_SELECTOR_PARENT_ACTION_SOURCE_REGISTER.csv",
    "domain_alpha3_sources": OUT / "P8_DOMAIN_ALPHA3_SOURCE_REGISTER.csv",
    "local_zero_premises": OUT / "P8_LOCAL_ZERO_EXTRA_PREMISE_REQUIREMENTS.csv",
    "local_gr_domain_vector": OUT / "P8_LOCAL_GR_RESIDUAL_VECTOR_FROM_DOMAIN_SOURCE.csv",
    "source_normalization_audit": OUT / "P8_SOURCE_NORMALIZATION_CHANNEL_AUDIT.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3431_SOURCE_REGISTER.csv",
    "projector_variation_theorem": OUT / "P8_Y5_R2FR_3431_PROJECTOR_VARIATION_NO_STRESS_THEOREM.csv",
    "branch_verdicts": OUT / "P8_Y5_R2FR_3431_DOMAIN_PROJECTOR_BRANCH_VERDICTS.csv",
    "operator_bound_pack": OUT / "P8_Y5_R2FR_3431_DOMAIN_PROJECTOR_OPERATOR_BOUND_PACK.csv",
    "ppn_coefficient_update": OUT / "P8_Y5_R2FR_3431_DOMAIN_PROJECTOR_PPN_COEFFICIENT_UPDATE.csv",
    "pc3400_4_update": OUT / "P8_Y5_R2FR_3431_PC3400_4_UPDATE.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3431_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3431_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3431_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3431_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3431_VALIDATION.csv",
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
        "doc_3430": "hidden/projector handoff",
        "channel_audit_3430": "domain/projector channel audit",
        "bound_rows_3430": "symbolic hidden/projector bound rows",
        "validation_3430": "prior checkpoint validation",
        "projector_stress_2407": "exact projector variation identity and stress warning",
        "domain_projector_coeffs": "PPN coefficient products for domain projector",
        "qcoh_projector_algebra": "trace projector algebra and parent-ownership warning",
        "qcoh_parent_projector_sources": "projector/domain source register",
        "domain_selector_novector_sources": "domain selector/no-vector source register",
        "domain_selector_parent_sources": "parent action route/source register",
        "domain_alpha3_sources": "alpha3/domain source register",
        "local_zero_premises": "why local zero alone is insufficient",
        "local_gr_domain_vector": "domain residual vector rows blocking local GR",
        "source_normalization_audit": "source-normalization hard target rows",
    }
    return [
        {
            "source_id": key,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[key],
            "valid_for_claim": False,
        }
        for key, path in SOURCES.items()
    ]


def projector_variation_theorem() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "DP3431_0_variation_identity",
            "claim": "A domain/projector acting on a source current obeys an exact product variation identity.",
            "formula": "delta(P_D J_H)=P_D delta J_H + (delta_g P_D)J_H + (D_D P_D)[delta D]J_H",
            "status": "EXACT_FROM_2407",
            "consequence": "Only P_D delta J_H is public-Hilbert; the derivative terms are hidden projector stress unless zero/bounded.",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "DP3431_1_no_go",
            "claim": "If P_D has nonzero metric/domain derivative on any allowed perturbation and J_H is not annihilated, projector stress cannot vanish identically.",
            "formula": "exists h: <A,(delta_g P_D[h])J_H> != 0 or <A,(D_D P_D[delta D])J_H> != 0 => T_proj != 0",
            "status": "NO_GO_LEMMA",
            "consequence": "Bianchi/covariance cannot by itself delete the domain/projector channel.",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "DP3431_2_fixed_topological_zero",
            "claim": "A fixed topological projector has no local bulk stress if it is metric independent, domain independent, and boundary-silent.",
            "formula": "delta_g P_top=0, D_D P_top=0, Phi_boundary=0 => T_proj=0 and epsilon_domain_projector=0",
            "status": "CONDITIONAL_ZERO_THEOREM",
            "consequence": "This is the clean zero route, but it requires a parent selector and physical Hilbert equality.",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "DP3431_3_analysis_only_projector",
            "claim": "The trace/coherent projector is stress-free only when it is analysis/readout bookkeeping outside the action, not a dynamical source term.",
            "formula": "P_coh used after solving as representation split => delta S/delta g has no P_coh term",
            "status": "SAFE_IF_NOT_IN_ACTION",
            "consequence": "Algebraic trace/STF cleanup is allowed, but it cannot be used to erase an action-level hidden source.",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "DP3431_4_trace_projector_trap",
            "claim": "The SO(3) trace projector is algebraically unique but metric/frame dependent when inserted into a variational term.",
            "formula": "P_coh(Q)_ij=(1/3)h_ij h^ab Q_ab, so delta_g P_coh generally contains delta h terms",
            "status": "ZERO_NOT_AUTOMATIC",
            "consequence": "Trace projection can kill STF leakage, but not source-normalization/monopole stress unless parent-owned.",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "DP3431_5_scalar_selector_partial",
            "claim": "A scalar stationary domain selector can suppress preferred vectors, but it does not automatically remove monopole/source-normalization stress.",
            "formula": "chi_D=chi(scalars), stationarity, no vector marker => alpha_i_vector channel may vanish; c_domain_source_norm still audited",
            "status": "PARTIAL_ZERO_ROUTE",
            "consequence": "Good for alpha1/alpha2/alpha3/xi if signed; insufficient for Newtonian source calibration.",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "DP3431_6_operator_bound",
            "claim": "If the zero route fails, domain/projector stress is bounded by metric/domain derivative operator norms and source size.",
            "formula": "epsilon_D <= M_H_ref^-1 (C_g||delta_g P_D||op||J_H|| + C_D||D_D P_D||op||delta D||||J_H|| + C_chi||delta_g chi_D|| + |Phi_D|)",
            "status": "BOUND_THEOREM_READY_VALUES_MISSING",
            "consequence": "This is the non-cheat route to PPN/R10 scoring.",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "DP3431_7_verdict",
            "claim": "Current MTS cannot claim domain/projector silence except on an unsigned fixed-topological or analysis-only branch.",
            "formula": "domain_projector_zero_current=false; epsilon_domain_projector_abs retained",
            "status": "ZERO_REJECTED_FOR_ACTIVE_BRANCH_BOUND_RETAINED",
            "consequence": "Local GR remains blocked, but the domain channel now has a concrete theorem/bound split.",
            "valid_for_claim": False,
        },
    ]


def branch_verdicts() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": "DPB3431_0_fixed_topological",
            "branch": "fixed topological projector",
            "zero_status": "CONDITIONAL_ZERO",
            "required_parent_signature": "P_D is fixed cohomology/linking representative, metric/domain independent, with zero boundary flux",
            "what_survives": "nothing local if physical Hilbert equality and same source denominator also hold",
            "current_verdict": "BEST_ZERO_ROUTE_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": "DPB3431_1_analysis_only_trace",
            "branch": "trace/STF analysis-only projector",
            "zero_status": "SAFE_BOOKKEEPING",
            "required_parent_signature": "P_coh is not varied inside S_parent and is used only to classify a solved tensor",
            "what_survives": "action-level hidden/domain source remains unaudited if P_coh is promoted to dynamics",
            "current_verdict": "ALLOWED_AS_DIAGNOSTIC_NOT_SOURCE_ZERO",
            "valid_for_claim": False,
        },
        {
            "branch_id": "DPB3431_2_dynamic_trace",
            "branch": "dynamic trace projector in action/current",
            "zero_status": "NOT_ZERO",
            "required_parent_signature": "parent Ward/Euler law must cancel delta h terms or make multiplier/current zero",
            "what_survives": "metric variation of h_ij/h^ij and source-normalization monopole",
            "current_verdict": "BOUND_REQUIRED",
            "valid_for_claim": False,
        },
        {
            "branch_id": "DPB3431_3_hodge_domain",
            "branch": "Hodge/DeWitt/Green/domain projector",
            "zero_status": "NOT_ZERO",
            "required_parent_signature": "operator derivative zero theorem or finite operator norm bound",
            "what_survives": "delta_g Green/Hodge pieces, moving support, linking surface response",
            "current_verdict": "BOUND_REQUIRED",
            "valid_for_claim": False,
        },
        {
            "branch_id": "DPB3431_4_scalar_selector",
            "branch": "scalar stationary domain selector",
            "zero_status": "PARTIAL",
            "required_parent_signature": "parent scalar Euler equation selects compact local comoving domain without marker vector",
            "what_survives": "source-normalization and boundary/collar stress unless separately zeroed",
            "current_verdict": "PPN_VECTOR_HELPFUL_BUT_NOT_LOCAL_GR",
            "valid_for_claim": False,
        },
    ]


def operator_bound_pack() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "DPOB3431_0_projector_derivative",
            "object": "metric derivative of domain projector",
            "symbol": "C_Pi_g||delta_g P_D||op",
            "bound_formula": "epsilon_Pi_g <= C_Pi_g||delta_g P_D||op||J_H||*/M_H_ref",
            "needed_inputs": "operator norm of delta_g P_D; dual source norm ||J_H||*; M_H_ref",
            "status": "SOURCE_BACKED_FORMULA_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "DPOB3431_1_domain_motion",
            "object": "domain/support/linking surface motion",
            "symbol": "C_Pi_D||D_D P_D||op||delta D||",
            "bound_formula": "epsilon_Pi_D <= C_Pi_D||D_D P_D||op||delta D||||J_H||*/M_H_ref",
            "needed_inputs": "domain derivative norm; support motion amplitude; source norm; M_H_ref",
            "status": "SOURCE_BACKED_FORMULA_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "DPOB3431_2_selector_metric_stress",
            "object": "selector/coframe metric stress",
            "symbol": "C_chi||delta_g chi_D||",
            "bound_formula": "epsilon_chi <= C_chi||delta_g chi_D|| + |tau_wall_anisotropic|/M_H_ref",
            "needed_inputs": "selector action; wall stress; isotropy certificate; M_H_ref",
            "status": "SOURCE_BACKED_FORMULA_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "DPOB3431_3_boundary_flux",
            "object": "domain boundary/collar flux",
            "symbol": "Phi_D/M_H_ref",
            "bound_formula": "epsilon_D_boundary <= |Phi_D|/M_H_ref",
            "needed_inputs": "no-flux theorem or boundary flux integral; same linking surface; M_H_ref",
            "status": "SOURCE_BACKED_FORMULA_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "DPOB3431_4_total_domain_projector",
            "object": "domain/projector total",
            "symbol": "epsilon_domain_projector_abs",
            "bound_formula": "epsilon_domain_projector_abs <= sum(abs(DPOB3431_0..DPOB3431_3))",
            "needed_inputs": "all sub-bounds or zero certificates",
            "status": "ABSOLUTE_SUM_GUARD",
            "valid_for_claim": False,
        },
    ]


def ppn_coefficient_update() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DPPN3431_0_alpha1",
            "observable": "alpha1",
            "formula": "alpha1_domain = W_domain_alpha1 * epsilon_domain_vector",
            "3431_effect": "zero only if scalar/topological no-vector domain selector is parent signed; otherwise bound by DPOB3431",
            "target_bound": "1e-4",
            "status": "NOT_SCOREABLE_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "row_id": "DPPN3431_1_alpha2",
            "observable": "alpha2",
            "formula": "alpha2_domain = W_domain_alpha2 * epsilon_domain_vector",
            "3431_effect": "same no-vector gate as alpha1, but tighter target",
            "target_bound": "2e-9",
            "status": "NOT_SCOREABLE_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "row_id": "DPPN3431_2_alpha3",
            "observable": "alpha3",
            "formula": "alpha3_domain = W_domain_alpha3 * epsilon_domain_flux",
            "3431_effect": "requires no vector, no flux, topological projector, and R11 silence; scalar selector alone is insufficient",
            "target_bound": "4e-20",
            "status": "CONDITIONAL_NOT_SCOREABLE",
            "valid_for_claim": False,
        },
        {
            "row_id": "DPPN3431_3_xi",
            "observable": "xi",
            "formula": "xi_domain = W_domain_xi * epsilon_domain_anisotropy",
            "3431_effect": "trace projector removes STF only as algebra/diagnostic; action-level STF stress needs parent no-stress theorem",
            "target_bound": "4e-9",
            "status": "NOT_SCOREABLE_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "row_id": "DPPN3431_4_R11_source_norm",
            "observable": "non_EH_operator_coefficients",
            "formula": "c_domain_source_normalization_operator",
            "3431_effect": "domain source-normalization is not killed by vector/STF symmetry and remains the Newtonian source-calibration blocker",
            "target_bound": "symbolic",
            "status": "HARD_NEXT_INPUT",
            "valid_for_claim": False,
        },
    ]


def pc3400_4_update() -> list[dict[str, Any]]:
    return [
        {
            "pc_id": "PC3400_4",
            "requirement": "no extra compact-source mass from hidden/domain/projector channels",
            "3431_result": "domain/projector zero theorem is conditional only; active metric/domain projector branch is rejected as zero and retained as bound",
            "best_signed_progress": "exact no-go/variation identity plus fixed-topological zero theorem plus operator-bound pack",
            "remaining_blocker": "parent selection of fixed topological projector or numeric operator norms for active projector branch",
            "status": "PARTIAL_NOT_PROMOTED",
            "valid_for_claim": False,
        }
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PG3431_0_variation_identity",
            "gate": "projector variation product rule is explicit",
            "result": "PASS",
            "evidence": "DP3431_0",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3431_1_zero_route",
            "gate": "domain/projector stress is zero for current MTS",
            "result": "FAIL_CURRENT",
            "evidence": "DP3431_7; DPB3431_2/3 require bounds",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3431_2_topological_route",
            "gate": "fixed-topological no-stress theorem exists",
            "result": "PASS_CONDITIONAL_UNSIGNED",
            "evidence": "DP3431_2",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3431_3_operator_bound",
            "gate": "operator-bound fallback exists",
            "result": "PASS_SYMBOLIC_VALUES_MISSING",
            "evidence": "DPOB3431_0 through DPOB3431_4",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3431_4_PPN_ready",
            "gate": "domain/projector PPN rows are score-ready",
            "result": "FAIL_VALUES_MISSING",
            "evidence": "DPPN3431 rows still lack W coefficients and epsilon inputs",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3431_5_local_GR",
            "gate": "local GR/Newton branch is derived",
            "result": "BLOCKED",
            "evidence": "domain projector, q_loc, source normalization, and M_H_ref/tau remain open",
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3431_0_trace_projector",
            "decision": "Keep trace/coherent projection as a diagnostic unless parent action owns it.",
            "reason": "P_coh is algebraically clean but metric/frame dependent if varied inside the action.",
            "next_action": "do not use P_coh alone as a local-GR zero proof",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3431_1_best_zero",
            "decision": "The cleanest zero branch is fixed/topological projector plus boundary silence.",
            "reason": "it makes delta_g P_D and D_D P_D vanish before source/PPN scoring.",
            "next_action": "only promote if parent selector signs this branch and Hilbert equality holds",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3431_2_best_progress",
            "decision": "For the active branch, proceed by operator bound rather than pretending zero.",
            "reason": "Hodge/domain/dynamic trace projectors carry explicit derivative stress.",
            "next_action": "either fill DPOB3431 inputs or move to q_loc owner proof",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3432-Y5-R2FR-GammaKhat-q_loc-Hilbert-owner-or-residual-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3432_GammaKhat_q_loc_Hilbert_owner_or_residual_bound.py",
            "objective": "attack the next high-leverage hidden channel: derive an S_GK Hilbert owner for Gamma/Khat/q_loc or turn q_loc into an explicit residual norm/vector bound",
            "success_condition": "q_loc is either on-shell Hilbert-owned with double zero, or HBR3430_2 gains a concrete residual-bound contract",
            "valid_for_claim": False,
        }
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3431_0",
            "purpose": "prevent projector cheat",
            "rule": "domain/projector stress may be set to zero only on fixed-topological or analysis-only non-action branch with signed parent clauses",
            "current_value": "claim_allowed=false",
            "valid_for_claim": False,
        },
        {
            "runner_id": "RUN3431_1",
            "purpose": "force bound route for active projector",
            "rule": "dynamic trace, Hodge, Green, and moving-domain projectors must use DPOB3431 bound rows",
            "current_value": "bound_required=true",
            "valid_for_claim": False,
        },
    ]


def all_outputs_scoped() -> bool:
    root_resolved = ROOT.resolve()
    return all(root_resolved in path.resolve().parents or path.resolve() == root_resolved for path in [DOC, *OUTPUTS.values()])


def all_generated_nonclaim(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for name, rows in rows_by_name.items():
        if name == "validation":
            continue
        for row in rows:
            if "valid_for_claim" in row and str(row["valid_for_claim"]).lower() != "false":
                return False
            if "claim_allowed" in row and str(row["claim_allowed"]).lower() != "false":
                return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], start_utc: datetime) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    theorem_rows = rows_by_name["projector_variation_theorem"]
    branch_rows = rows_by_name["branch_verdicts"]
    bound_rows = rows_by_name["operator_bound_pack"]
    ppn_rows = rows_by_name["ppn_coefficient_update"]
    promotion_rows = rows_by_name["promotion_gates"]
    next_rows = rows_by_name["next_target"]
    modified_count = 0
    if FORMALIZATION.exists():
        start_ts = start_utc.timestamp()
        modified_count = sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= start_ts)
    validations = [
        {
            "check_id": "VAL3431_0_sources_exist",
            "condition": "all cited source paths exist",
            "passed": all(row["exists"] for row in source_rows),
            "detail": f"{sum(1 for row in source_rows if row['exists'])}/{len(source_rows)} source paths exist",
        },
        {
            "check_id": "VAL3431_1_outputs_scoped",
            "condition": "all outputs are in post-checkpoint-work",
            "passed": all_outputs_scoped(),
            "detail": str(ROOT),
        },
        {
            "check_id": "VAL3431_2_nonclaim",
            "condition": "all generated rows remain nonclaim",
            "passed": all_generated_nonclaim(rows_by_name),
            "detail": "valid_for_claim=false throughout generated rows",
        },
        {
            "check_id": "VAL3431_3_no_go_present",
            "condition": "domain projector no-go lemma is explicit",
            "passed": any(row["theorem_id"] == "DP3431_1_no_go" for row in theorem_rows),
            "detail": "metric/domain derivative stress cannot be erased by covariance",
        },
        {
            "check_id": "VAL3431_4_zero_branch_present",
            "condition": "fixed-topological zero theorem is explicit",
            "passed": any(row["theorem_id"] == "DP3431_2_fixed_topological_zero" for row in theorem_rows),
            "detail": "conditional zero route exists",
        },
        {
            "check_id": "VAL3431_5_active_branch_not_zeroed",
            "condition": "dynamic trace/Hodge/domain branches are not promoted",
            "passed": any(row["branch_id"] == "DPB3431_2_dynamic_trace" and row["current_verdict"] == "BOUND_REQUIRED" for row in branch_rows)
            and any(row["branch_id"] == "DPB3431_3_hodge_domain" and row["current_verdict"] == "BOUND_REQUIRED" for row in branch_rows),
            "detail": "active projector branches retained as bounds",
        },
        {
            "check_id": "VAL3431_6_bound_pack",
            "condition": "domain/projector operator-bound pack exists",
            "passed": len(bound_rows) >= 5 and any(row["bound_id"] == "DPOB3431_4_total_domain_projector" for row in bound_rows),
            "detail": f"{len(bound_rows)} bound rows",
        },
        {
            "check_id": "VAL3431_7_ppn_rows",
            "condition": "PPN/source-normalization coefficient rows are updated",
            "passed": len(ppn_rows) >= 5 and any(row["row_id"] == "DPPN3431_4_R11_source_norm" for row in ppn_rows),
            "detail": f"{len(ppn_rows)} PPN/source rows",
        },
        {
            "check_id": "VAL3431_8_local_GR_blocked",
            "condition": "local GR remains blocked until domain/q_loc/source rows close",
            "passed": any(row["gate_id"] == "PG3431_5_local_GR" and row["result"] == "BLOCKED" for row in promotion_rows),
            "detail": "no local-GR claim promoted",
        },
        {
            "check_id": "VAL3431_9_next_target",
            "condition": "next target attacks q_loc owner or residual bound",
            "passed": next_rows[0]["target_doc"].startswith("3432-Y5-R2FR-GammaKhat-q_loc"),
            "detail": next_rows[0]["target_doc"],
        },
        {
            "check_id": "VAL3431_10_formalization_untouched",
            "condition": "formalization-workbench modified-file count remains 0 during this run",
            "passed": modified_count == 0,
            "detail": f"modified_count_since_start={modified_count}",
        },
    ]
    validations.append(
        {
            "check_id": "VAL3431_11_overall",
            "condition": "3431 domain/projector checkpoint is internally valid",
            "passed": all(row["passed"] for row in validations),
            "detail": "PASS" if all(row["passed"] for row in validations) else "FAIL",
        }
    )
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    text = f"""# 3431 - Domain Projector No-Stress Theorem or Operator Bound

## Summary
- This checkpoint tries to prove the domain/projector stress channel away, rather than merely recording it as missing.
- The proof succeeds only for a sharply restricted branch: a fixed/topological projector, or an analysis-only trace projector that never enters the action.
- It rejects the dangerous shortcut: a dynamic trace, Hodge, Green, or moving-domain projector is not automatically stress-free just because it is covariant or algebraically neat.
- The active branch therefore becomes an operator-bound problem with explicit `delta_g P_D`, `D_D P_D`, selector-stress, and boundary-flux terms.
- This narrows the local-GR obstacle: domain/projector silence is not impossible, but the current route must either sign the fixed-topological branch or fill operator-bound inputs.

## Source Register
{md_table(rows_by_name["source_register"])}

## Projector Variation No-Stress Theorem
{md_table(rows_by_name["projector_variation_theorem"])}

## Domain Projector Branch Verdicts
{md_table(rows_by_name["branch_verdicts"])}

## Domain Projector Operator Bound Pack
{md_table(rows_by_name["operator_bound_pack"])}

## Domain Projector PPN Coefficient Update
{md_table(rows_by_name["ppn_coefficient_update"])}

## PC3400_4 Update
{md_table(rows_by_name["pc3400_4_update"])}

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
This is a real derivation result, not just a missing-input note: the projector channel can be zero only in a fixed/topological or analysis-only branch. The active dynamic/domain projector branch must be bounded. That means we stop pretending this channel is harmless and either parent-sign the topological selector or pay the PPN/source-normalization coefficient bill.
"""
    DOC.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    start_utc = datetime.now(timezone.utc)
    rows_by_name = {
        "source_register": source_register(),
        "projector_variation_theorem": projector_variation_theorem(),
        "branch_verdicts": branch_verdicts(),
        "operator_bound_pack": operator_bound_pack(),
        "ppn_coefficient_update": ppn_coefficient_update(),
        "pc3400_4_update": pc3400_4_update(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    rows_by_name["validation"] = validation_rows(rows_by_name, start_utc)
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)
    write_doc(rows_by_name)
    failed = [row for row in rows_by_name["validation"] if not row["passed"]]
    if failed:
        raise SystemExit(f"3431 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"wrote {len(OUTPUTS)} csv outputs")


if __name__ == "__main__":
    main()
