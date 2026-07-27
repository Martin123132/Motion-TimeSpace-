from __future__ import annotations

import csv
import shutil
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB = ROOT / "source-intake" / "rab-sector"
RAB_RAW = RAB / "raw"
RAB_ACCEPTED = RAB / "accepted"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1590"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1590-Y5-R2FR-Gamma-Khat-Ploc-owner-bundle-or-cR2-finite-coefficient-row.md"

SOURCE_FILES = {
    "1589_doc": ROOT / "1589-Y5-R2FR-parent-coefficient-source-hunt-or-curve-QA-promotion.md",
    "1589_validation": OUT / "P8_Y5_BRR545_1589_VALIDATION.csv",
    "1589_law": OUT / "P8_Y5_PARENT_QLOC_1589_EFFECTIVE_COEFFICIENT_LAW.csv",
    "1589_owner_status": OUT / "P8_Y5_PARENT_QLOC_1589_MEMORY_FIBRE_OWNER_STATUS.csv",
    "1351_doc": ROOT / "1351-Y5-R10-RAB-Gamma-Khat-Ploc-owner-bundle-or-q_loc-bound-row-fill.md",
    "1351_owner_audit": OUT / "P8_Y5_R10_1351_OWNER_BUNDLE_AUDIT.csv",
    "1366_doc": ROOT / "1366-Y5-R10-RAB-Gamma-eff-scalar-density-definition-hunt-or-q_loc-envelope.md",
    "1366_gamma_hunt": OUT / "P8_Y5_R10_1366_GAMMA_EFF_SCALAR_DENSITY_HUNT_LEDGER.csv",
    "1366_khat_match": OUT / "P8_Y5_R10_1366_KMETRIC_KHAT_MATCH_LEDGER.csv",
    "1367_kernel": OUT / "P8_Y5_R10_1367_KMETRIC_CHAIN_KERNEL_ATTEMPT.csv",
    "1368_kernel": OUT / "P8_Y5_R10_1368_M_LCG_KERNEL_HUNT.csv",
    "1369_lcg_hunt": OUT / "P8_Y5_R10_1369_LCG_PARENT_DEFINITION_HUNT.csv",
    "1370_lcg_contract": OUT / "P8_Y5_R10_1370_PARENT_LCG_CONTRACT_CANDIDATE.csv",
    "1370_cqgamma": OUT / "P8_Y5_R10_1370_WARD_SAFE_CQGAMMA_DERIVATION.csv",
    "1371_doc": ROOT / "1371-Y5-R10-RAB-fixed-Lcg-parent-action-insertion-or-Cqgamma-norm-bound.md",
    "1371_action": OUT / "P8_Y5_R10_1371_FIXED_L0_PARENT_ACTION_INSERTION.csv",
    "1371_residuals": OUT / "P8_Y5_R10_1371_LOCAL_RESIDUAL_ZERO_OR_BOUND_LEDGER.csv",
    "1371_cqgamma_norm": OUT / "P8_Y5_R10_1371_CQGAMMA_NORM_BOUND_INPUT_TABLE.csv",
    "1372_doc": ROOT / "1372-Y5-R10-RAB-fixed-L0-double-zero-local-residual-theorem-or-Qnorm-bound.md",
    "1372_theorem": OUT / "P8_Y5_R10_1372_LOCAL_RESIDUAL_THEOREM_ATTEMPT.csv",
    "1372_qnorm": OUT / "P8_Y5_R10_1372_QNORM_DECOMPOSITION_BOUND.csv",
    "1372_runner_feed": OUT / "P8_Y5_R10_1372_CQGAMMA_RUNNER_FEED.csv",
}

NEEDLES = {
    "1589_doc": ["NEXT_1590_GAMMA_KHAT_PLOC_OWNER_OR_FINITE_CR2_ROW", "PARENT_COEFFICIENT_OWNER_STILL_MISSING"],
    "1589_validation": ["VAL1589_OVERALL", "PASS"],
    "1589_law": ["LAW1589_0_integrated_hidden_modes", "c_R2_eff(k)"],
    "1589_owner_status": ["OWN1589_4_response_bundle", "MISSING_GAMMA_KHAT_PLOC_OWNER"],
    "1351_doc": ["OWNER_BUNDLE_NOT_CLOSED", "THM1351_3_verdict"],
    "1351_owner_audit": ["OB1351_7_verdict", "OWNER_BUNDLE_NOT_CLOSED"],
    "1366_doc": ["Gamma_eff=L_cg^-2F(m)", "CLAIM_BLOCKED"],
    "1366_gamma_hunt": ["HUNT1366_0_memory_scalar_formula_shape", "FOUND_FORMULA_SHAPE_NOT_CLAIMABLE_SCALAR_DENSITY"],
    "1366_khat_match": ["MATCH1366_4_acceptance", "CLAIM_BLOCKED"],
    "1367_kernel": ["KER1367_6_verdict", "KERNELS_NOT_COMPUTABLE_CURRENTLY"],
    "1368_kernel": ["KERN1368_5_chain_kernel_verdict", "M_M_PARTIAL_CONDITIONAL_M_L_MISSING"],
    "1369_lcg_hunt": ["LCGH1369_1_fixed_parameter_route", "EXACT_CONDITIONAL_SILENCE_LEMMA_UNSIGNED"],
    "1370_lcg_contract": ["LCC1370_4_metric_silence_result", "DERIVED_UNDER_CLOSURE_CONTRACT"],
    "1370_cqgamma": ["CQG1370_3_gamma_projection_coefficient", "SYMBOLIC_WARD_SAFE_COEFFICIENT_DERIVED"],
    "1371_doc": ["Fixed `L_cg=L0` closes the `M_L` chain", "Q_norm"],
    "1371_action": ["PAI1371_5_action_insertion_verdict", "CLOSURE_BRANCH_READY_NOT_LIVE_CLAIM"],
    "1371_residuals": ["LRZ1371_4_cdb_terms", "OPEN_RETAINED_RESIDUAL"],
    "1371_cqgamma_norm": ["CQN1371_7_pass_threshold", "SYMBOLIC_ACCEPTANCE_RULE_READY"],
    "1372_doc": ["Q_norm <= Q_alg + Q_cdb + Q_mem + Q_bdy + Q_trans + Q_proj", "ZERO_THEOREM_NOT_DERIVED"],
    "1372_theorem": ["LRT1372_5_zero_theorem_verdict", "ZERO_THEOREM_NOT_DERIVED"],
    "1372_qnorm": ["QNB1372_7_no_cancellation_policy", "GUARD_READY"],
    "1372_runner_feed": ["QGF1372_1_gamma_bound", "SYMBOLIC_CASSINI_BOUND_READY"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1590_SOURCE_REGISTER.csv"
OWNER_SYNTHESIS = OUT / "P8_Y5_PARENT_QLOC_1590_OWNER_BUNDLE_SYNTHESIS.csv"
FIXED_L0_GATE = OUT / "P8_Y5_PARENT_QLOC_1590_FIXED_L0_DOUBLE_ZERO_CONTRACT_GATE.csv"
CR2_IMPLICATIONS = OUT / "P8_Y5_PARENT_QLOC_1590_CR2_COEFFICIENT_IMPLICATIONS.csv"
FINITE_TEMPLATE = OUT / "P8_Y5_PARENT_QLOC_1590_FINITE_COEFFICIENT_ROW_TEMPLATE.csv"
QGAMMA_BRIDGE = OUT / "P8_Y5_PARENT_QLOC_1590_QGAMMA_QNORM_RUNNER_BRIDGE.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1590_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1590_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1590_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1590_VALIDATION.csv"

COPY_TARGETS = {
    OWNER_SYNTHESIS: [
        QUARANTINE / "OWNER_BUNDLE_SYNTHESIS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_owner_bundle_synthesis_nonclaim_1590.csv",
    ],
    FIXED_L0_GATE: [
        QUARANTINE / "FIXED_L0_DOUBLE_ZERO_CONTRACT_GATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_fixed_L0_double_zero_gate_nonclaim_1590.csv",
    ],
    CR2_IMPLICATIONS: [
        QUARANTINE / "CR2_COEFFICIENT_IMPLICATIONS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_cR2_coefficient_implications_nonclaim_1590.csv",
    ],
    FINITE_TEMPLATE: [
        QUARANTINE / "FINITE_COEFFICIENT_ROW_TEMPLATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_finite_coefficient_row_template_nonclaim_1590.csv",
    ],
    QGAMMA_BRIDGE: [
        QUARANTINE / "QGAMMA_QNORM_RUNNER_BRIDGE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_qgamma_qnorm_runner_bridge_nonclaim_1590.csv",
    ],
    DECISION: [
        QUARANTINE / "DECISION_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_Gamma_Khat_Ploc_or_cR2_decision_nonclaim_1590.csv",
    ],
}


def false_flags() -> dict[str, bool]:
    return {
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def file_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    return all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for source_index, (source_key, source_path) in enumerate(SOURCE_FILES.items()):
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1590_{source_index}_{source_key}",
                "source_path": rel(source_path),
                "exists": source_path.exists(),
                "needle_found": file_contains(source_path, NEEDLES[source_key]),
                "needles": "; ".join(NEEDLES[source_key]),
                "purpose": "Gamma/Khat/Ploc owner bundle or finite cR2 coefficient row",
                **false_flags(),
            }
        )
    return rows


def owner_synthesis_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "OBS1590_0_conditional_theorem",
            "S_GK + K_hat metric response + P_loc owner",
            "1351 proves the clean conditional identity: one covariant scalar-density action with K_hat as its metric response can turn q_loc into an on-shell Ward/Euler residual.",
            "CONDITIONAL_THEOREM_SHARP_NOT_PARENT_SIGNED",
            "needs S_GK source, Gamma_eff formula, Khat=Kmetric match, P_loc owner, Euler/source/boundary closure",
        ),
        (
            "OBS1590_1_live_scalar_seed",
            "Gamma_eff=L_cg^-2 F(m)",
            "1366 finds a useful nonclaim formula shape, but units, q-owned m/L_cg profiles, local domain and Kmetric/Khat match are incomplete.",
            "FORMULA_SHAPE_FOUND_NOT_CLAIMABLE_DENSITY",
            "needs m and L_cg parent definitions plus Kmetric kernels",
        ),
        (
            "OBS1590_2_kernel_chain",
            "Kmetric_chain",
            "1367/1368/1369/1370 progressively isolate M_m, M_L, K_conn, K_domain and K_boundary. M_m has a conditional fixed-field zero branch; L_cg has a fixed-L0 conditional silence route.",
            "PARTIAL_CONDITIONAL_KERNEL_PROGRESS",
            "live Khat comparison and cdb kernels remain open",
        ),
        (
            "OBS1590_3_fixed_L0_branch",
            "fixed L0 + vacuum-subtracted double-zero",
            "1371 writes S_GK^0=-int sqrt(-g)L0^-2 Fhat(m;m*) with fixed L0 and Fhat(m*)=Fhat_prime(m*)=0; this closes algebraic volume/m/L pieces under closure clauses.",
            "BEST_LOCAL_CLOSURE_BRANCH_NOT_LIVE_CLAIM",
            "needs parent adoption, universal m*, sign convention and residual bounds",
        ),
        (
            "OBS1590_4_residual_norm",
            "Q_norm",
            "1372 shows the full zero theorem still fails, but converts the remaining debt into Q_norm <= Q_alg+Q_cdb+Q_mem+Q_bdy+Q_trans+Q_proj with no cancellation.",
            "ZERO_THEOREM_BLOCKED_BOUND_LANE_ACTIVE",
            "needs component bounds or theorem-zero certificates",
        ),
        (
            "OBS1590_5_owner_verdict",
            "Gamma/Khat/Ploc owner bundle",
            "The owner route has a serious candidate branch, but not a claim-grade parent owner. It can guide derivation and bound rows, not local-GR promotion.",
            "OWNER_BUNDLE_NOT_CLOSED_CURRENT_CORPUS",
            "do not use private closure as proof; continue with residual theorem or finite coefficient row",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "synthesis_id": synthesis_id,
            "bundle_piece": bundle_piece,
            "evidence_summary": evidence_summary,
            "status": status,
            "blocking_gap": blocking_gap,
            "evidence_backed": True,
            "parent_signed": False,
            "numeric_value_present": False,
            **false_flags(),
        }
        for synthesis_id, bundle_piece, evidence_summary, status, blocking_gap in rows
    ]


def fixed_l0_gate_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "FLG1590_0_parent_action_branch",
            "S_GK^0=-int sqrt(-g)L0^-2 Fhat(m;m*)",
            "PARENT_ACTION_CLOSURE_BRANCH_WRITTEN",
            "fixed L0 and vacuum subtraction expose the volume stress and prevent the old M_L-only mistake",
            "parent adoption; sign convention; universal/non-fitted m*; global subtraction policy",
        ),
        (
            "FLG1590_1_double_zero",
            "Fhat(m*)=0 and Fhat_prime(m*)=0",
            "STRICT_DOUBLE_ZERO_CONTRACT_WRITTEN",
            "volume and first chain variations vanish at the local branch under fixed-field conditions",
            "parent law selecting m* and proof that m* is source-independent",
        ),
        (
            "FLG1590_2_algebraic_closure",
            "volume + m-chain + L-chain",
            "CLOSED_UNDER_CLOSURE_ONLY",
            "fixed L0 plus double-zero closes the algebraic Gamma_eff contribution, not the full local residual",
            "parent signature plus K_conn/K_domain/K_boundary and memory stress closure",
        ),
        (
            "FLG1590_3_cdb_residuals",
            "K_conn;K_domain;K_boundary",
            "OPEN_RETAINED_RESIDUAL",
            "connection/domain/boundary response is independent of the algebraic m/L closure",
            "no-flux/commutator theorem or component bounds",
        ),
        (
            "FLG1590_4_memory_stress",
            "kinetic/source/bath/boundary memory stress",
            "OPEN_RETAINED_RESIDUAL",
            "algebraic background subtraction cannot delete kinetic, source, bath or boundary stress",
            "constant-m no-hair/source silence/bath and boundary theorem or finite bounds",
        ),
        (
            "FLG1590_5_verdict",
            "fixed-L0 double-zero local residual theorem",
            "ZERO_THEOREM_NOT_DERIVED",
            "best branch closes algebraic sector but not cdb/memory residuals",
            "carry Q_norm bound or derive residual theorem",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "object": obj,
            "status": status,
            "what_it_proves": proves,
            "still_missing": missing,
            "parent_signed": False,
            **false_flags(),
        }
        for gate_id, obj, status, proves, missing in rows
    ]


def cR2_implication_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CR2I1590_0_base_law",
            "c_R2_eff(k)=c_bare+1/2 B^T L^-1(k)B+c_measure+c_boundary",
            "1590 keeps 1589 coefficient law as the R2/fR accounting spine",
            "DERIVED_SYMBOLIC_LAW",
            "not numeric; not theorem-zero",
        ),
        (
            "CR2I1590_1_fixed_L0_effect",
            "fixed-L0 double-zero branch can suppress algebraic memory contribution to B^T L^-1 B",
            "under fixed L0, fixed/locked m*, and strict double-zero, the algebraic Gamma_eff source becomes quadratic in displacement",
            "THEOREM_ZERO_CONDITIONAL_NOT_LIVE",
            "does not remove c_bare, fibre B_h, measure/boundary, K_cdb or memory stress",
        ),
        (
            "CR2I1590_2_Qnorm_to_coefficient_bound",
            "finite residual may be bounded through Q_norm",
            "Q_norm component bounds can feed PPN/R10 constraints before a public local-GR theorem exists",
            "BOUND_ROUTE_SYMBOLIC_NO_NUMERIC_INPUTS",
            "needs Q_i values, operator norms and arena projections",
        ),
        (
            "CR2I1590_3_no_claim",
            "R2/fR local-GR promotion",
            "owner bundle progress is real but insufficient for c_R2/fRR=0 or finite alpha/lambda prediction",
            "CLAIM_BLOCKED",
            "no scalaron R10 score, no beta/PPN pass, no local-GR claim",
        ),
        (
            "CR2I1590_4_finite_row_trigger",
            "if residual theorem fails",
            "fill c_R2_eff/B_mem/B_h/K_cdb/Q_norm rows with units and sources instead of using closure",
            "FINITE_ROW_REQUIRED_IF_RESIDUALS_RETAINED",
            "finite coefficient row must remain nonclaim until values and maps are real",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "implication_id": implication_id,
            "coefficient_target": target,
            "meaning": meaning,
            "status": status,
            "blocking_gap": gap,
            "parent_signed": False,
            "numeric_value_present": False,
            **false_flags(),
        }
        for implication_id, target, meaning, status, gap in rows
    ]


def finite_template_rows() -> list[dict[str, Any]]:
    rows = [
        ("FCR1590_0_cR2_eff", "c_R2_eff", "length^2_or_inverse_mass_squared_after_EH_normalization", "c_bare + 1/2 B^T L^-1 B + c_measure + c_boundary", "MISSING_NUMERIC_OR_THEOREM_ZERO", "R10;PPN;R11"),
        ("FCR1590_1_Bmem", "B_mem", "parent_memory_curvature_vertex_units", "memory curvature-linear vertex after fixed-L0/double-zero split", "MISSING_ZERO_OR_FINITE_VALUE", "R10;PPN;Q_norm"),
        ("FCR1590_2_Bh", "B_h", "parent_fibre_curvature_vertex_units", "fibre curvature-linear vertex contribution to R2/fR-like residual", "MISSING_ZERO_OR_FINITE_VALUE", "R10;WEP;PPN"),
        ("FCR1590_3_Kcdb", "K_conn;K_domain;K_boundary", "stress_response_or_divergence_norm_units", "connection/domain/boundary residual response after algebraic closure", "MISSING_COMPONENT_BOUNDS", "Q_norm;PPN;clock;orbital"),
        ("FCR1590_4_Qnorm_components", "Q_alg;Q_cdb;Q_mem;Q_bdy;Q_trans;Q_proj", "dimensionless_or_declared_acceleration_normalized_norm", "componentwise no-cancellation bound feeding C_qgamma", "MISSING_NUMERIC_COMPONENTS", "PPN_gamma;R10;clock;orbital"),
        ("FCR1590_5_Cqgamma_inputs", "U_min;N_G;N_D;Q_norm", "SI_or_dimensionless_with_declared_c_convention", "B_gamma <= (c^2/(2U_min)) N_G N_D Q_norm", "MISSING_NUMERIC_OPERATOR_INPUTS", "PPN_gamma"),
        ("FCR1590_6_source_paths", "source_file;normalization;arena_map", "path_and_convention", "every finite row needs a source path and observable projection", "MISSING_SOURCE_PATHS_AND_MAPS", "all_local_arenas"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "row_id": row_id,
            "quantity": quantity,
            "required_units": units,
            "required_expression_or_role": expression,
            "current_status": status,
            "observable_links": links,
            "runner_verdict": "REJECT_CURRENT_ROW",
            "failure_reasons": "valid_for_claim_false;claim_allowed_false;" + status,
            "parent_signed": False,
            "numeric_value_present": False,
            **false_flags(),
        }
        for row_id, quantity, units, expression, status, links in rows
    ]


def qgamma_bridge_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "QGB1590_0_symbolic_feed",
            "B_gamma <= (c^2/(2U_min)) N_G N_D Q_norm",
            "1371/1372",
            "SYMBOLIC_CASSINI_BOUND_READY",
            "U_min;N_G;N_D;Q_norm component values",
        ),
        (
            "QGB1590_1_Qnorm_decomposition",
            "Q_norm <= Q_alg+Q_cdb+Q_mem+Q_bdy+Q_trans+Q_proj",
            "1372",
            "SYMBOLIC_DECOMPOSITION_DERIVED",
            "component norms, source paths, units and no-cancellation validation",
        ),
        (
            "QGB1590_2_acceptance",
            "Q_norm <= 2 U_min sigma_gamma/(c^2 N_G N_D)",
            "Cassini gamma policy through 1371/1372 feed",
            "POLICY_READY_INPUTS_MISSING",
            "numeric U_min, operator norms, Q_i values",
        ),
        (
            "QGB1590_3_proxy_guard",
            "old q_proxy/compact shell values",
            "1372 proxy guard",
            "PROXY_NOT_IMPORTED",
            "missing units/projection mapping prevents using proxy as claim value",
        ),
        (
            "QGB1590_4_runner_verdict",
            "PPN gamma nonclaim runner",
            "aggregate 1370-1372",
            "RUNNER_SYMBOLIC_NOT_NUMERIC",
            "still no PPN/Cassini pass",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "bridge_id": bridge_id,
            "formula_or_policy": formula,
            "source_basis": source_basis,
            "status": status,
            "missing_to_score": missing,
            **false_flags(),
        }
        for bridge_id, formula, source_basis, status, missing in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1590_0_owner_bundle", "Gamma/Khat/Ploc owner bundle", "BLOCKED_NO_CLAIM", "S_GK branch is closure candidate; live parent signature and residual closure are missing"),
        ("GATE1590_1_cR2_zero", "c_R2/fRR theorem-zero", "BLOCKED_NO_CLAIM", "fixed-L0 double-zero does not close c_bare, B_h, cdb, boundary, measure or memory stress"),
        ("GATE1590_2_finite_scalaron", "finite alpha/lambda scalaron row", "BLOCKED_NO_CLAIM", "no numeric c_R2/fRR or source-backed finite coefficient row exists"),
        ("GATE1590_3_Qnorm_bound", "Q_norm bound pass", "BLOCKED_NO_CLAIM", "symbolic decomposition exists but numeric/source-backed Q_i, U_min, N_G and N_D are missing"),
        ("GATE1590_4_PPN_gamma", "Cassini/PPN gamma score", "BLOCKED_NO_CLAIM", "Cqgamma feed is symbolic and q_loc norm is not numeric"),
        ("GATE1590_5_local_GR", "local GR / PPN / R10 reopening", "BLOCKED_NO_CLAIM", "zero theorem and empirical bound pass are both unavailable"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            **false_flags(),
        }
        for gate_id, claim, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC1590_0_best_branch",
            "FIXED_L0_DOUBLE_ZERO_IS_THE_BEST_CURRENT_LOCAL_BRANCH",
            "it closes the algebraic volume/m/L sector without covariance cheating if parent-adopted",
            "try to close cdb/memory residuals or bind Q_norm; do not promote branch yet",
        ),
        (
            "DEC1590_1_coupling_bottleneck",
            "COUPLING_AND_RESPONSE_REMAIN_THE_BOTTLENECK",
            "the question is no longer whether algebra can be written, but whether cdb/memory/source couplings are zero-derived or bounded",
            "attack K_conn/K_domain/K_boundary and memory stress component rows first",
        ),
        (
            "DEC1590_2_empirical_lane",
            "QGAMMA_QNORM_IS_THE_TESTING_LANE",
            "the PPN gamma comparator can become useful only after Q_norm components and operator norms are source-backed",
            "fill Q_i/U_min/N_G/N_D before any Cassini claim",
        ),
        (
            "DEC1590_3_next",
            "NEXT_1591_FIXED_L0_CDB_MEMORY_QNORM_FIRST_FILL_OR_CR2_BOUND_ROW",
            "the next best step is either a cdb/memory zero theorem or the first concrete Q_norm/cR2 finite coefficient rows",
            "derive residual theorem first; otherwise fill nonclaim rows with units/source paths",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            **false_flags(),
        }
        for decision_id, decision, reason, next_action in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1591-Y5-R2FR-fixed-L0-cdb-memory-Qnorm-first-fill-or-cR2-bound-row.md",
            "script": "scripts/Y5_R2FR_fixed_L0_cdb_memory_Qnorm_first_fill_or_cR2_bound_row.py",
            "objective": "attempt to close K_conn/K_domain/K_boundary and memory/source stress under the fixed-L0 double-zero branch; if not, create first-fill Q_norm and c_R2_eff finite coefficient rows with units, source paths and arena maps",
            "success_condition": "source-backed residual theorem for cdb/memory channels or complete nonclaim Q_norm/c_R2 bound rows ready for PPN/R10/clock/orbital runners",
            "do_not": "do not claim local GR, do not use fixed-L0 closure as live parent signature, do not score Cassini/R10 from symbolic rows, do not edit formalization-workbench or use GitHub",
            **false_flags(),
        }
    ]


def copy_outputs() -> None:
    for source_path, target_paths in COPY_TARGETS.items():
        for target_path in target_paths:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_path, target_path)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def generated_flags_false(generated_csvs: list[Path]) -> bool:
    flag_columns = {"score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"}
    for csv_path in generated_csvs:
        for row in read_csv(csv_path):
            for flag_column in flag_columns.intersection(row):
                if row[flag_column] != "False":
                    return False
    return True


def formalization_scope_clean(generated_csvs: list[Path]) -> bool:
    if any(FORMALIZATION in csv_path.parents for csv_path in generated_csvs):
        return False
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT.parent), "status", "--short", "--", "formalization-workbench"],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return True
    if result.returncode != 0:
        return True
    return len([line for line in result.stdout.splitlines() if line.strip()]) == 0


def has_1590_rows(folder: Path) -> bool:
    if not folder.exists():
        return False
    return any("1590" in csv_path.name for csv_path in folder.glob("*.csv"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    owner = read_csv(OWNER_SYNTHESIS)
    fixed = read_csv(FIXED_L0_GATE)
    cR2 = read_csv(CR2_IMPLICATIONS)
    finite = read_csv(FINITE_TEMPLATE)
    qgamma = read_csv(QGAMMA_BRIDGE)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    checks = [
        ("VAL1590_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1590 source paths exist"),
        ("VAL1590_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all 1590 source needles found"),
        (
            "VAL1590_2_owner_bundle_not_closed",
            any(row["synthesis_id"] == "OBS1590_5_owner_verdict" and row["status"] == "OWNER_BUNDLE_NOT_CLOSED_CURRENT_CORPUS" for row in owner),
            "Gamma/Khat/Ploc owner route remains nonclaim",
        ),
        (
            "VAL1590_3_fixed_L0_branch_captured",
            any(row["gate_id"] == "FLG1590_2_algebraic_closure" and row["status"] == "CLOSED_UNDER_CLOSURE_ONLY" for row in fixed)
            and any(row["gate_id"] == "FLG1590_5_verdict" and row["status"] == "ZERO_THEOREM_NOT_DERIVED" for row in fixed),
            "fixed-L0 double-zero closes algebraic sector but not full theorem",
        ),
        (
            "VAL1590_4_cR2_implication_nonclaim",
            any(row["implication_id"] == "CR2I1590_1_fixed_L0_effect" and row["status"] == "THEOREM_ZERO_CONDITIONAL_NOT_LIVE" for row in cR2)
            and any(row["implication_id"] == "CR2I1590_4_finite_row_trigger" and row["status"] == "FINITE_ROW_REQUIRED_IF_RESIDUALS_RETAINED" for row in cR2),
            "c_R2 implication is conditional; finite rows required if residuals remain",
        ),
        (
            "VAL1590_5_finite_template_rejects",
            all(row["runner_verdict"] == "REJECT_CURRENT_ROW" and row["valid_for_claim"] == "False" for row in finite)
            and any(row["quantity"] == "Q_alg;Q_cdb;Q_mem;Q_bdy;Q_trans;Q_proj" for row in finite),
            "finite coefficient template rows are present and nonclaim",
        ),
        (
            "VAL1590_6_qgamma_bridge_symbolic",
            any(row["bridge_id"] == "QGB1590_0_symbolic_feed" and row["status"] == "SYMBOLIC_CASSINI_BOUND_READY" for row in qgamma)
            and any(row["bridge_id"] == "QGB1590_4_runner_verdict" and row["status"] == "RUNNER_SYMBOLIC_NOT_NUMERIC" for row in qgamma),
            "Qgamma/Qnorm runner bridge is symbolic, not score-ready",
        ),
        (
            "VAL1590_7_claim_gates_closed",
            all(row["status"] == "BLOCKED_NO_CLAIM" and row["claim_allowed"] == "False" for row in gates),
            "all 1590 claim gates remain closed",
        ),
        (
            "VAL1590_8_decision_next",
            any(row["decision"] == "NEXT_1591_FIXED_L0_CDB_MEMORY_QNORM_FIRST_FILL_OR_CR2_BOUND_ROW" for row in decisions),
            "decision selects cdb/memory Qnorm first fill or cR2 bound row",
        ),
        ("VAL1590_9_csv_parse", all(len(read_csv(csv_path)) > 0 for csv_path in generated_csvs), "all generated 1590 CSVs parse cleanly"),
        ("VAL1590_10_claim_flags_false", generated_flags_false(generated_csvs), "all generated claim/prediction flags remain false"),
        ("VAL1590_11_no_raw_accepted", not has_1590_rows(RAB_RAW) and not has_1590_rows(RAB_ACCEPTED), "no 1590 rows written to raw/accepted finite directories"),
        ("VAL1590_12_branch_copies", all(target_path.exists() for target_paths in COPY_TARGETS.values() for target_path in target_paths), "branch/quarantine nonclaim copies written"),
        ("VAL1590_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1590_14_formalization_untouched", formalization_scope_clean(generated_csvs), "all generated 1590 paths are outside formalization-workbench; git status is clean when available"),
    ]
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1590_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1590 Gamma/Khat/Ploc owner bundle or finite cR2 coefficient row validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = ["| " + " | ".join(str(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def write_doc(
    sources: list[dict[str, Any]],
    owner: list[dict[str, Any]],
    fixed: list[dict[str, Any]],
    cR2: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    qgamma: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1590 - R2/fR Gamma-Khat-Ploc Owner Bundle Or cR2 Finite Coefficient Row",
                "## Verdict\n"
                "- 1590 identifies the best current local route: fixed `L0`, vacuum-subtracted `Fhat(m;m*)`, and strict double-zero `Fhat(m*)=Fhat_prime(m*)=0` close the algebraic volume/`m`/`L_cg` sector under closure clauses.\n"
                "- That still does **not** prove local GR: `K_conn`, `K_domain`, `K_boundary`, memory/source stress, transition support, and projector leakage remain live residual channels.\n"
                "- The R2/fR coefficient problem is therefore narrowed but not solved: the fixed-`L0` branch can only zero the relevant contribution after parent adoption and residual closure; otherwise finite `c_R2_eff/B_mem/Q_norm` rows must be filled.\n"
                "- The empirical fallback is now explicit: `B_gamma <= (c^2/(2U_min)) N_G N_D Q_norm`, with `Q_norm <= Q_alg+Q_cdb+Q_mem+Q_bdy+Q_trans+Q_proj`, no cancellation allowed.\n"
                "- No R2/fR, R10, beta, EH, Newton, PPN, local-GR, WEP, clock, orbital, conservation or common-matter claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## Owner Bundle Synthesis",
                md_table(owner, ["synthesis_id", "bundle_piece", "evidence_summary", "status", "blocking_gap"]),
                "## Fixed-L0 Double-Zero Contract Gate",
                md_table(fixed, ["gate_id", "object", "status", "what_it_proves", "still_missing"]),
                "## cR2 Coefficient Implications",
                md_table(cR2, ["implication_id", "coefficient_target", "meaning", "status", "blocking_gap"]),
                "## Finite Coefficient Row Template",
                md_table(finite, ["row_id", "quantity", "required_units", "required_expression_or_role", "current_status", "observable_links", "runner_verdict"]),
                "## Qgamma/Qnorm Runner Bridge",
                md_table(qgamma, ["bridge_id", "formula_or_policy", "source_basis", "status", "missing_to_score"]),
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "reason", "next_action"]),
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "success_condition", "do_not"]),
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    owner = owner_synthesis_rows()
    fixed = fixed_l0_gate_rows()
    cR2 = cR2_implication_rows()
    finite = finite_template_rows()
    qgamma = qgamma_bridge_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        OWNER_SYNTHESIS,
        FIXED_L0_GATE,
        CR2_IMPLICATIONS,
        FINITE_TEMPLATE,
        QGAMMA_BRIDGE,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(OWNER_SYNTHESIS, owner)
    write_csv(FIXED_L0_GATE, fixed)
    write_csv(CR2_IMPLICATIONS, cR2)
    write_csv(FINITE_TEMPLATE, finite)
    write_csv(QGAMMA_BRIDGE, qgamma)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, owner, fixed, cR2, finite, qgamma, gates, decisions, validation, next_rows)


if __name__ == "__main__":
    main()
