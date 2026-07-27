from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

DOC = ROOT / "2827-Y5-R2FR-vertical-generator-Dqvm-and-q-normalization-derivation-contract-under-AX1090.md"

SRC_2826_NEXT = RESIDUALS / "P8_Y5_R2FR_2826_NEXT_TARGET.csv"
SRC_2826_MICRO = RESIDUALS / "P8_Y5_R2FR_2826_FIRST_FILL_MICRO_CONTRACT.csv"
SRC_2826_RANKING = RESIDUALS / "P8_Y5_R2FR_2826_PRIORITY_RANKING.csv"
SRC_2826_BLOCKERS = RESIDUALS / "P8_Y5_R2FR_2826_BLOCKER_DEPENDENCY_MAP.csv"
SRC_2825_FORMULAS = RESIDUALS / "P8_Y5_R2FR_2825_LOCAL_LOCK_CONTROL_FORMULAS.csv"
SRC_2823_UNITS = RESIDUALS / "P8_Y5_R2FR_2823_Q_NORMALIZATION_AND_DUAL_UNITS_GATE.csv"
SRC_2270_MAP = RESIDUALS / "P8_Y5_PARENT_QLOC_2270_PSI_COVARIANCE_TO_PHIQ_MAP.csv"
SRC_2271_PULLBACK = RESIDUALS / "P8_Y5_PARENT_QLOC_2271_COVARIANCE_PULLBACK_FORMULAS.csv"
SRC_2272_LIFT = RESIDUALS / "P8_Y5_PARENT_QLOC_2272_Q_TANGENT_LIFT_ATTEMPT.csv"
SRC_2281_OPERATOR = RESIDUALS / "P8_Y5_PARENT_QLOC_2281_Q_OPERATOR_CONTRACT.csv"
SRC_2281_STIFFNESS = RESIDUALS / "P8_Y5_PARENT_QLOC_2281_Q_STIFFNESS_DERIVATION_AUDIT.csv"
SRC_2281_SELECTOR = RESIDUALS / "P8_Y5_PARENT_QLOC_2281_COVARIANCE_MANIFOLD_SELECTOR_GAP.csv"
SRC_2486_DQ = RESIDUALS / "P8_Y5_FIELD_QUOTIENT_2486_DQ_VERTICAL_GENERATOR_LEDGER.csv"
SRC_2486_THEOREM = RESIDUALS / "P8_Y5_FIELD_QUOTIENT_2486_THEOREM_ATTEMPT.csv"
SRC_2486_MATTER = RESIDUALS / "P8_Y5_FIELD_QUOTIENT_2486_MATTER_DESCENT_GATE.csv"
SRC_2486_RESIDUAL = RESIDUALS / "P8_Y5_FIELD_QUOTIENT_2486_RESIDUAL_OWNER_SPLIT.csv"
SRC_2527_OPEN = RESIDUALS / "P8_Y5_NO_SHADOW_2527_Q_VERTICAL_OPEN_BRANCH_REENTRY_AUDIT.csv"
SRC_2527_DQ = RESIDUALS / "P8_Y5_NO_SHADOW_2527_DQ_KERNEL_GATE_MATRIX.csv"
SRC_2528_CHART = RESIDUALS / "P8_Y5_NO_SHADOW_2528_FIELD_CHART_EQUIVALENCE_AUDIT.csv"
SRC_2528_NOPOLE = RESIDUALS / "P8_Y5_NO_SHADOW_2528_NOPOLE_SELECTOR_GATE.csv"
SRC_2529_DET = RESIDUALS / "P8_Y5_NO_SHADOW_2529_PSI_DETERMINANT_QUOTIENT_GATE.csv"
SRC_2529_LIFT = RESIDUALS / "P8_Y5_NO_SHADOW_2529_PSI_LIFT_AND_CARRIER_AUDIT.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2827_SOURCE_REGISTER.csv",
    "normalization": RESIDUALS / "P8_Y5_R2FR_2827_Q_NORMALIZATION_ALIAS_AUDIT.csv",
    "derivation": RESIDUALS / "P8_Y5_R2FR_2827_DQVM_DERIVATION_LEDGER.csv",
    "kernel": RESIDUALS / "P8_Y5_R2FR_2827_VERTICAL_KERNEL_CONDITION.csv",
    "outcomes": RESIDUALS / "P8_Y5_R2FR_2827_ZERO_NONZERO_DEMOTION_OUTCOME_LEDGER.csv",
    "cqm": RESIDUALS / "P8_Y5_R2FR_2827_CQM_AND_LOCAL_LOCK_REENTRY_STATUS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2827_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2827_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2827_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2827_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2827_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "derivation_copy": SOURCE_WEIGHT / "Dqvm_q_normalization_derivation_2827_NONCLAIM.csv",
    "kernel_copy": LOCAL_BOUNDS / "Dqvm_kernel_condition_2827_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2827_Q_SOURCE_OWNER_MATTER_GENERATOR_NEXT.csv",
}

BRANCH_ID = "MTS_R2FR_VERTICAL_GENERATOR_DQVM_Q_NORMALIZATION_2827"


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    paths = {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["score_ready"] = False
    row["valid_prediction_row"] = False
    row["valid_for_claim"] = False
    row["claim_allowed"] = False
    row["generated_utc"] = ts()
    return row


def source_row(source_id: str, path: Path, anchors: str, role: str) -> dict[str, Any]:
    text = read_text(path)
    anchor_list = [anchor for anchor in anchors.split(";") if anchor]
    missing = [anchor for anchor in anchor_list if anchor not in text]
    return nonclaim(
        {
            "source_id": source_id,
            "source_path": str(path),
            "anchors": anchors,
            "role": role,
            "path_exists": path.exists(),
            "anchors_found": not missing,
            "missing_anchors": ";".join(missing),
        }
    )


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2827_0_2826_next", SRC_2826_NEXT, "NEXT2826_0_2827", "2826 selected vertical-generator/q-normalization target"),
        ("SRC2827_1_2826_micro", SRC_2826_MICRO, "MC2826_0_target;MC2826_5_fail_case", "2827 micro-contract: zero, nonzero, or demotion"),
        ("SRC2827_2_2826_ranking", SRC_2826_RANKING, "PRI2826_1", "Dq[v_m] plus q-normalization selected first"),
        ("SRC2827_3_2826_blockers", SRC_2826_BLOCKERS, "BLK2826_0_norm;BLK2826_1_Dqvm", "normalization and Dq[v_m] blockers"),
        ("SRC2827_4_2825_formulas", SRC_2825_FORMULAS, "FORM2825_5_Scg;FORM2825_9_Delta", "local-lock chain depending on C_qm/Dq[v_m]"),
        ("SRC2827_5_2823_units", SRC_2823_UNITS, "QNG2823_2_Eq_units;QNG2823_4_Cqm_units", "E_q and C_qm units remain unresolved"),
        ("SRC2827_6_2270_map", SRC_2270_MAP, "PCM2270_0_covariance_definition;PCM2270_1_component_projection", "exact q=ln(AB) and weak covariance channel"),
        ("SRC2827_7_2271_pullback", SRC_2271_PULLBACK, "PBF2271_0_inverse_map;PBF2271_1_q_tangent", "Phi/q inverse map and q tangent"),
        ("SRC2827_8_2272_lift", SRC_2272_LIFT, "QTL2272_0_target;QTL2272_2_q_zero_readout", "q tangent lift and q=0 surface"),
        ("SRC2827_9_2281_operator", SRC_2281_OPERATOR, "QOC2281_0_action_term;QOC2281_4_newton_limit", "q operator and Newton debt"),
        ("SRC2827_10_2281_stiffness", SRC_2281_STIFFNESS, "QSD2281_0_covariance_variable;QSD2281_6_no_smuggling_test", "covariance q alias and selector gap"),
        ("SRC2827_11_2281_selector", SRC_2281_SELECTOR, "CSG2281_1_metric_compatibility;CSG2281_4_direct_penalty", "selector alternatives and closure-only penalty warning"),
        ("SRC2827_12_2486_dq", SRC_2486_DQ, "DQ2486_0_chain_rule_template;DQ2486_2_q_private", "conditional Dq kernel and q-private residual"),
        ("SRC2827_13_2486_theorem", SRC_2486_THEOREM, "THM2486_0_chain_rule_descent;THM2486_2_current_signature_application", "conditional quotient theorem and failed current application"),
        ("SRC2827_14_2486_matter", SRC_2486_MATTER, "MD2486_0_chain_rule;MD2486_1_no_source_prefactor", "matter descent gate"),
        ("SRC2827_15_2486_residual", SRC_2486_RESIDUAL, "RS2486_1_q_source;RS2486_8_source_normalization", "residual owners if q verticality/source not closed"),
        ("SRC2827_16_2527_open", SRC_2527_OPEN, "QVA2527_2_q_map;QVA2527_5_local_generator_decomposition", "open-branch q/v theorem blockers"),
        ("SRC2827_17_2527_dq", SRC_2527_DQ, "DQM2527_0_q_component_formula;DQM2527_4_local_generator_projection", "Dq matrix and generator projection missing"),
        ("SRC2827_18_2528_chart", SRC_2528_CHART, "FCE2528_3_computable_q;FCE2528_5_chart_verdict", "q field-chart/equivalence not derived"),
        ("SRC2827_19_2528_nopole", SRC_2528_NOPOLE, "NPS2528_3_absent_nonprimitive;NPS2528_5_selector_verdict", "absent/nonprimitive route and psi determinant next"),
        ("SRC2827_20_2529_det", SRC_2529_DET, "DQG2529_0_channel_definition;DQG2529_5_verdict", "psi determinant target retained but not closed"),
        ("SRC2827_21_2529_lift", SRC_2529_LIFT, "PLA2529_2_lift_exactness;PLA2529_4_verdict", "psi lift exactness and matter/readout silence unsigned"),
    ]
    return [source_row(*spec) for spec in specs]


def normalization_rows() -> list[dict[str, Any]]:
    specs = [
        ("QN2827_0_log_q", "q_log", "q := ln(A B)", "SELECT_FOR_2827_DERIVATION", "A and B are dimensionless metric/cell factors, so q is dimensionless in this branch", "fixes the coordinate used for Dq algebra; still does not fix E_q carrier units", SRC_2270_MAP, "PCM2270_0_covariance_definition"),
        ("QN2827_1_phi_q_inverse", "Phi/q inverse", "A=exp(2 Phi + q/2), B=exp(-2 Phi + q/2)", "EXACT_LOCAL_CHART_FORMULA", "Phi and q dimensionless logarithmic chart variables", "separates Newton-potential direction from reciprocal/determinant direction", SRC_2271_PULLBACK, "PBF2271_0_inverse_map"),
        ("QN2827_2_weak_covariance", "weak covariance channel", "q = (C_rr - C_tt) + O(C^2)", "WEAK_DIAGNOSTIC_ONLY", "dimensionless if C_tt,C_rr are normalized covariance ratios", "usable as a check but not a replacement for exact log branch", SRC_2270_MAP, "PCM2270_1_component_projection"),
        ("QN2827_3_cov_ratio_alias", "q_cov_ratio", "q(C)=C_R-C_T/(1-C_T)", "ALIAS_DEBT_NOT_MIXED", "conditional dimension only; parent normalization unsigned", "do not mix this row with q_log/E_q until conversion map and parentheses convention are signed", SRC_2281_STIFFNESS, "QSD2281_0_covariance_variable"),
        ("QN2827_4_Eq_units", "E_q carrier units", "E_q[delta q]^2 needs H_AB, xi_q, dV_e, and branch normalization", "UNRESOLVED", "q_log coordinate is dimensionless but the norm scale is not fixed", "C_qm and J_q dual units remain nonclaim", SRC_2823_UNITS, "QNG2823_2_Eq_units"),
    ]
    return [
        nonclaim(
            {
                "normalization_id": normalization_id,
                "object": obj,
                "formula": formula,
                "status": status,
                "unit_statement": unit_statement,
                "effect": effect,
                "source_path": str(source_path),
                "source_anchor": anchor,
                "anchor_found": anchor in read_text(source_path),
                "selected_for_derivation": normalization_id in {"QN2827_0_log_q", "QN2827_1_phi_q_inverse"},
                "mixed_norm_allowed": False,
                "control_only": True,
            }
        )
        for normalization_id, obj, formula, status, unit_statement, effect, source_path, anchor in specs
    ]


def derivation_rows() -> list[dict[str, Any]]:
    specs = [
        ("DER2827_0_definition", "start from exact log branch", "q = ln(A B)", "definition", "q_log is the selected local branch coordinate", SRC_2270_MAP, "PCM2270_0_covariance_definition"),
        ("DER2827_1_general_variation", "take any tangent v", "Dq[v] = v(A)/A + v(B)/B = v(ln A) + v(ln B)", "EXACT_FORMULA", "this is the exact local coupling readout before choosing a generator", SRC_2271_PULLBACK, "PBF2271_0_inverse_map"),
        ("DER2827_2_covariance_variation", "use A=1-C_tt and B=1+C_rr", "Dq[v] = -v(C_tt)/(1-C_tt) + v(C_rr)/(1+C_rr)", "EXACT_FORMULA_IN_C_COMPONENTS", "weakly Dq[v] = v(C_rr)-v(C_tt)+O(C vC)", SRC_2270_MAP, "PCM2270_1_component_projection"),
        ("DER2827_3_phi_q_chart", "use A=exp(2Phi+q/2), B=exp(-2Phi+q/2)", "Dq[v] = v(q)", "EXACT_COORDINATE_IDENTITY", "the Phi/Newton tangent cancels from Dq; the q-coordinate tangent survives", SRC_2271_PULLBACK, "PBF2271_1_q_tangent"),
        ("DER2827_4_phi_direction", "Newton-potential direction", "if v=v_Phi partial_Phi then Dq[v]=0", "EXACT_ZERO_FOR_PHI_ONLY_DIRECTION", "local Newton-potential motion can be q-silent if it stays in the Phi tangent", SRC_2271_PULLBACK, "PBF2271_2_phi_tangent"),
        ("DER2827_5_q_direction", "reciprocal/determinant direction", "if v=v_q partial_q then Dq[v]=v_q", "EXACT_NONZERO_UNLESS_VQ_ZERO", "a q-residual generator is not vertical by name; it is vertical only if its q-component vanishes", SRC_2272_LIFT, "QTL2272_0_target"),
        ("DER2827_6_matter_generator_condition", "actual matter/local generator v_m", "Dq[v_m]=0 iff v_m(ln A)+v_m(ln B)=0 iff v_m^q=0 in the Phi/q chart", "EXACT_KERNEL_CONDITION_DERIVED", "this is the clean condition the corpus must prove; current files do not prove v_m^q=0", SRC_2527_DQ, "DQM2527_4_local_generator_projection"),
        ("DER2827_7_current_evidence", "apply current corpus evidence", "v_m^q is not parent-signed; Dq[v_m] cannot be evaluated or zeroed", "ZERO_THEOREM_NOT_PROVED_CURRENT_CORPUS", "2486/2527/2528/2529 all leave q map, vertical basis, local generator decomposition, or matter descent unsigned", SRC_2486_THEOREM, "THM2486_2_current_signature_application"),
    ]
    return [
        nonclaim(
            {
                "derivation_id": derivation_id,
                "step": step,
                "formula": formula,
                "status": status,
                "implication": implication,
                "source_path": str(source_path),
                "source_anchor": anchor,
                "anchor_found": anchor in read_text(source_path),
                "derived_in_2827": status.startswith("EXACT"),
                "claim_promoted": False,
                "control_only": True,
            }
        )
        for derivation_id, step, formula, status, implication, source_path, anchor in specs
    ]


def kernel_rows() -> list[dict[str, Any]]:
    specs = [
        ("KER2827_0_exact_kernel", "exact q-kernel", "Dq[v]=0", "v(A)/A + v(B)/B = 0", "the tangent preserves AB, i.e. the reciprocal/determinant branch is silent", "DERIVED_CONDITION"),
        ("KER2827_1_covariance_kernel", "covariance component kernel", "Dq[v]=0", "v(C_rr)/(1+C_rr) = v(C_tt)/(1-C_tt)", "temporal and radial covariance variations must satisfy the exact reciprocal relation", "DERIVED_CONDITION"),
        ("KER2827_2_weak_kernel", "weak-field diagnostic", "Dq[v]=0 + O(C vC)", "v(C_rr)=v(C_tt)", "linear channel check only; not a full theorem", "DERIVED_WEAK_TEST"),
        ("KER2827_3_phi_kernel", "Newton/Phi tangent", "v=v_Phi partial_Phi", "Dq[v]=0", "pure Newton-potential deformation is q-silent in the exact Phi/q chart", "DERIVED_ZERO_FOR_SUBDIRECTION"),
        ("KER2827_4_q_nonkernel", "q tangent", "v=v_q partial_q", "Dq[v]=v_q", "the q-residual direction is visible unless its coefficient is zero", "DERIVED_NONZERO_CONDITION"),
        ("KER2827_5_matter_kernel", "matter/local generator", "v_m in ker(Dq)", "v_m^q=0", "must be sourced from matter descent/generator decomposition; currently unsigned", "NOT_PROVED_FOR_VM"),
    ]
    return [
        nonclaim(
            {
                "kernel_id": kernel_id,
                "object": obj,
                "zero_statement": zero_statement,
                "equivalent_condition": condition,
                "meaning": meaning,
                "status": status,
                "applies_to_v_m": kernel_id == "KER2827_5_matter_kernel",
                "satisfied_for_v_m": False,
                "control_only": True,
            }
        )
        for kernel_id, obj, zero_statement, condition, meaning, status in specs
    ]


def outcome_rows() -> list[dict[str, Any]]:
    specs = [
        ("OUT2827_0_exact_formula", "derive Dq[v] formula", "CLOSED_CONDITIONAL", "Dq[v]=v(ln A)+v(ln B)=v(q)", "the coupling readout is no longer vague"),
        ("OUT2827_1_zero_case", "prove Dq[v_m]=0", "REJECT_CURRENT_EVIDENCE", "requires v_m^q=0 or a q-basic matter/visible quotient theorem; 2486/2527/2528/2529 leave this unsigned", "no exact zero theorem for the actual matter/local generator"),
        ("OUT2827_2_nonzero_case", "derive sourced nonzero Dq[v_m]", "NOT_AVAILABLE_CURRENT_EVIDENCE", "the exact formula says Dq[v_m]=v_m^q, but no parent source gives v_m^q or its norm", "cannot compute C_qm or a local-lock amplitude"),
        ("OUT2827_3_fail_case", "representative-dependent coupling", "LIVE_FAILURE_MODE", "if v_m^q depends on representative/Weyl/disformal/readout choice, the local-lock route is closure-only", "must be resolved by source owner / matter generator audit"),
        ("OUT2827_4_project_status", "local-lock reentry", "DEMOTE_TO_CONDITIONAL_KERNEL_GATE", "the condition is derived, but v_m is not proved in the kernel", "do not claim local GR/Newton/PPN/R10"),
    ]
    return [
        nonclaim(
            {
                "outcome_id": outcome_id,
                "question": question,
                "status": status,
                "result": result,
                "effect": effect,
                "control_only": True,
                "promotion_allowed": False,
            }
        )
        for outcome_id, question, status, result, effect in specs
    ]


def cqm_rows() -> list[dict[str, Any]]:
    specs = [
        ("CQM2827_0_definition", "C_qm", "C_qm := ||Dq[v_m]|| in the selected E_q/q-response norm", "FORMAL_DEFINITION_ONLY", "E_q units, v_m normalization, and v_m^q are unsigned", SRC_2823_UNITS, "QNG2823_4_Cqm_units"),
        ("CQM2827_1_formula", "Dq[v_m]", "Dq[v_m]=v_m^q=-v_m(C_tt)/(1-C_tt)+v_m(C_rr)/(1+C_rr)", "EXACT_SYMBOLIC_FORMULA", "symbolic formula only; no source-backed v_m components", SRC_2270_MAP, "PCM2270_1_component_projection"),
        ("CQM2827_2_Scg", "S_cg control chain", "S_cg,total_control <= 1/2 T_source_norm_control C_qm + S_direct + S_boundary + S_extra", "REENTRY_BLOCKED", "C_qm and T_source_norm remain nonclaim", SRC_2825_FORMULAS, "FORM2825_5_Scg"),
        ("CQM2827_3_Nlock", "local lock", "N_lock and Delta_m cannot be promoted from the control chain", "REENTRY_BLOCKED", "Dq[v_m] zero/nonzero status is not sourced for actual v_m", SRC_2825_FORMULAS, "FORM2825_9_Delta"),
        ("CQM2827_4_next_input", "first missing source owner", "source or theorem-zero v_m^q", "NEXT_REQUIRED", "must decide whether Hilbert matter/local generator has a q-component", SRC_2486_MATTER, "MD2486_0_chain_rule"),
    ]
    return [
        nonclaim(
            {
                "cqm_id": cqm_id,
                "object": obj,
                "formula": formula,
                "status": status,
                "blocker": blocker,
                "source_path": str(source_path),
                "source_anchor": anchor,
                "anchor_found": anchor in read_text(source_path),
                "numeric_value_present": False,
                "source_backed_value": False,
                "control_only": True,
            }
        )
        for cqm_id, obj, formula, status, blocker, source_path, anchor in specs
    ]


def gate_rows(rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    sources_ok = all(row["path_exists"] and row["anchors_found"] for row in rows["sources"])
    normalization_ok = all(row["anchor_found"] for row in rows["normalization"])
    derivation_formula_ok = all(row["anchor_found"] for row in rows["derivation"]) and any(
        row["derivation_id"] == "DER2827_6_matter_generator_condition"
        and row["status"] == "EXACT_KERNEL_CONDITION_DERIVED"
        for row in rows["derivation"]
    )
    zero_not_overclaimed = any(row["outcome_id"] == "OUT2827_1_zero_case" and row["status"] == "REJECT_CURRENT_EVIDENCE" for row in rows["outcomes"])
    nonzero_not_overclaimed = any(row["outcome_id"] == "OUT2827_2_nonzero_case" and row["status"] == "NOT_AVAILABLE_CURRENT_EVIDENCE" for row in rows["outcomes"])
    cqm_blocked = all(not row["numeric_value_present"] and not row["source_backed_value"] for row in rows["cqm"])
    specs = [
        ("CG2827_0_sources", "source anchors present", sources_ok, "all imported ledgers are reproducible"),
        ("CG2827_1_q_normalization", "q_log normalization selected without mixed-norm promotion", normalization_ok, "q_log is selected for Dq algebra but E_q units remain unresolved"),
        ("CG2827_2_Dq_formula", "exact Dq[v] formula derived", derivation_formula_ok, "Dq[v]=v(ln A)+v(ln B)=v(q) and matter-kernel condition is explicit"),
        ("CG2827_3_zero_theorem", "Dq[v_m]=0 theorem proved", False, "actual v_m^q is not parent-signed"),
        ("CG2827_4_zero_not_overclaimed", "zero theorem not overclaimed", zero_not_overclaimed, "current evidence rejects the zero theorem for actual v_m"),
        ("CG2827_5_nonzero_value", "sourced nonzero Dq[v_m] value obtained", False, "no source-backed v_m^q or C_qm"),
        ("CG2827_6_nonzero_not_overclaimed", "nonzero value not overclaimed", nonzero_not_overclaimed, "symbolic formula does not become a coefficient"),
        ("CG2827_7_Cqm", "C_qm numeric/source-backed", False, "E_q norm and v_m normalization are unsigned"),
        ("CG2827_8_Cqm_blocked", "C_qm block retained", cqm_blocked, "no numeric/source-backed C_qm row exists"),
        ("CG2827_9_GR_Newton", "local GR/Newton claim allowed", False, "q=0 selector, Newton-source normalization, and v_m kernel proof remain missing"),
        ("CG2827_10_PPN_R10", "PPN/R10/clock/orbital claim allowed", False, "arena projections and source vector remain nonclaim"),
    ]
    return [
        nonclaim(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "gate_passed": passed,
                "status": "PASS_NONCLAIM" if passed else "BLOCKED",
                "reason": reason,
            }
        )
        for gate_id, claim, passed, reason in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2827_0_formula", "The exact coupling readout is derived.", "Dq[v]=v(ln A)+v(ln B)=v(q)", "this turns the coupling hunt into a concrete q-component problem", "use q_log branch for local Dq algebra"),
        ("DEC2827_1_zero", "The zero theorem for actual v_m is not proved.", "ZERO_REJECTED_CURRENT_EVIDENCE", "current corpus does not show the matter/local generator has v_m^q=0", "do not claim local-lock silence"),
        ("DEC2827_2_nonzero", "A sourced nonzero coefficient is also not obtained.", "NONZERO_VALUE_MISSING", "the formula needs source-backed v_m^q and E_q normalization", "do not compute C_qm"),
        ("DEC2827_3_demote", "The local-lock route stays conditional.", "CONDITIONAL_KERNEL_GATE", "we derived the gate but not the generator membership", "route must next source or zero the q-component of matter/local generator"),
        ("DEC2827_4_next", "Next target is q-source owner / matter-generator q-component.", "NEXT_2828_Q_SOURCE_OWNER", "this is the minimum missing step between the exact Dq formula and local-lock reentry", "derive v_m^q=0 from matter descent or stage a finite q-source row"),
    ]
    return [
        nonclaim(
            {
                "decision_id": decision_id,
                "decision": decision,
                "result": result,
                "because": because,
                "next_action": next_action,
            }
        )
        for decision_id, decision, result, because, next_action in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2827_0_2828",
                "status": "selected_primary",
                "target_doc": "2828-Y5-R2FR-q-source-owner-and-matter-generator-vmq-zero-or-finite-row-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_q_source_owner_and_matter_generator_vmq_zero_or_finite_row_under_AX1090_2828.py",
                "mission": "try to prove v_m^q=0 from matter descent/source-owner structure; if it fails, stage a finite nonclaim q-source component row for Dq[v_m] and C_qm without promoting local GR/Newton/PPN/R10",
                "acceptance": "must cite 2827 exact Dq formula, 2486 matter descent gate, and q-source residual owners; no numeric placeholders; all claim flags false; formalization-workbench untouched",
                "forbidden": "do not call v_m vertical by declaration; do not mix q aliases; do not compute C_qm without E_q and v_m normalization",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("BR2827_0_derivation_copy", OUTPUTS["derivation"], BRANCH_OUTPUTS["derivation_copy"], "source-weight copy of exact Dq[v] derivation"),
        ("BR2827_1_kernel_copy", OUTPUTS["kernel"], BRANCH_OUTPUTS["kernel_copy"], "local-bounds copy of q-kernel condition"),
        ("BR2827_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB acquisition queue for q-source owner / matter-generator target"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_table, copy_path, purpose in specs:
        copy_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_table, copy_path)
        rows.append(
            nonclaim(
                {
                    "copy_id": copy_id,
                    "source_table": str(source_table),
                    "copy_path": str(copy_path),
                    "purpose": purpose,
                    "exists": copy_path.exists(),
                }
            )
        )
    return rows


def iter_cited_paths(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[Path]:
    keys = {"source_path", "source_paths", "source_table", "copy_path"}
    paths: list[Path] = []
    for rows in rows_by_name.values():
        for row in rows:
            for key in keys:
                value = row.get(key)
                if value is None:
                    continue
                for token in str(value).split(";"):
                    item = token.strip()
                    if not item or item.startswith("http") or item.startswith("MISSING_"):
                        continue
                    path = Path(item)
                    if not path.is_absolute():
                        path = ROOT / item
                    paths.append(path)
    return paths


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for name, rows in rows_by_name.items():
        if name == "validation":
            continue
        for row in rows:
            for key in ("score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if str(row.get(key, "")).lower() == "true":
                    return False
    return True


def no_numeric_insertions(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    forbidden_numeric_keys = {"numeric_value", "coefficient", "alpha", "beta", "lambda_value"}
    for rows in rows_by_name.values():
        for row in rows:
            for key, value in row.items():
                if key in forbidden_numeric_keys and str(value).strip():
                    return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    start = SCRIPT_START_UTC.timestamp()
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            try:
                if path.stat().st_mtime >= start:
                    return False
            except OSError:
                return False
    return True


def under_root(paths: list[Path]) -> bool:
    root_text = str(ROOT.resolve()).lower()
    return all(str(path.resolve()).lower().startswith(root_text) for path in paths)


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_paths = [path for path in OUTPUTS.values() if path != OUTPUTS["validation"]]
    branch_paths = list(BRANCH_OUTPUTS.values())
    cited_paths = iter_cited_paths(rows_by_name)
    checks = [
        ("VAL2827_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2827_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2827_2_normalization_anchors", all(row["anchor_found"] for row in rows_by_name["normalization"]), "all q-normalization rows cite found anchors"),
        ("VAL2827_3_log_q_selected", any(row["normalization_id"] == "QN2827_0_log_q" and row["selected_for_derivation"] for row in rows_by_name["normalization"]), "q_log selected for Dq algebra"),
        ("VAL2827_4_no_mixed_norm", not any(row["mixed_norm_allowed"] for row in rows_by_name["normalization"]), "no q alias mixing allowed"),
        ("VAL2827_5_derivation_anchors", all(row["anchor_found"] for row in rows_by_name["derivation"]), "all derivation rows cite found anchors"),
        ("VAL2827_6_exact_kernel_condition", any(row["derivation_id"] == "DER2827_6_matter_generator_condition" and row["status"] == "EXACT_KERNEL_CONDITION_DERIVED" for row in rows_by_name["derivation"]), "exact matter-generator kernel condition derived"),
        ("VAL2827_7_zero_not_claimed", any(row["outcome_id"] == "OUT2827_1_zero_case" and row["status"] == "REJECT_CURRENT_EVIDENCE" for row in rows_by_name["outcomes"]), "Dq[v_m]=0 theorem is not overclaimed"),
        ("VAL2827_8_nonzero_not_claimed", any(row["outcome_id"] == "OUT2827_2_nonzero_case" and row["status"] == "NOT_AVAILABLE_CURRENT_EVIDENCE" for row in rows_by_name["outcomes"]), "nonzero coefficient is not overclaimed"),
        ("VAL2827_9_Cqm_blocked", all(not row["numeric_value_present"] and not row["source_backed_value"] for row in rows_by_name["cqm"]), "C_qm remains unsourced/non-numeric"),
        ("VAL2827_10_claims_blocked", not any(row["claim_allowed"] for row in rows_by_name["gates"]), "no claim gate allows local GR/Newton/PPN/R10"),
        ("VAL2827_11_no_numeric_insertions", no_numeric_insertions(rows_by_name), "no numeric coefficients or prediction values inserted"),
        ("VAL2827_12_next_target_2828", any(row["next_id"] == "NEXT2827_0_2828" and row["selected"] for row in rows_by_name["next"]), "q-source owner / matter-generator target selected next"),
        ("VAL2827_13_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2827_14_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2827_15_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2827_16_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2827_17_no_claim_flags", no_claim_flags(rows_by_name), "no score_ready, valid_prediction_row, valid_for_claim, or claim_allowed flag is true"),
        ("VAL2827_18_generated_under_post_checkpoint", under_root(output_paths + branch_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2827_19_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2827_20_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [
        {
            "validation_id": validation_id,
            "passed": passed,
            "detail": detail,
            "timestamp_utc": ts(),
        }
        for validation_id, passed, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2827_OVERALL",
            "passed": overall,
            "detail": "2827 derives the exact Dq[v] and matter-generator kernel condition on the q_log branch, rejects a current Dq[v_m]=0 theorem, refuses a sourced nonzero C_qm, and selects q-source-owner/matter-generator v_m^q next.",
            "timestamp_utc": ts(),
        }
    )
    return rows


def md(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    content = f"""# 2827 - Y5 R2FR Vertical Generator Dqvm And q Normalization Derivation Contract Under AX1090

Status: `Y5_R2FR_2827_exact_Dq_kernel_condition_derived_actual_vm_zero_not_proved`

## Private Verdict

2827 gets a real derivation, but not yet the victory condition.

On the selected local log branch,

`q := ln(A B)`

so for any tangent/generator `v`,

`Dq[v] = v(A)/A + v(B)/B = v(ln A) + v(ln B)`.

Using `A=exp(2 Phi + q/2)` and `B=exp(-2 Phi + q/2)`, this becomes:

`Dq[v] = v(q)`.

Therefore a pure Newton/Phi deformation is q-silent, but an actual q-residual deformation is not. The exact condition for the matter/local generator is:

`Dq[v_m]=0  iff  v_m^q=0  iff  v_m(ln A)+v_m(ln B)=0`.

That is the gate. Current evidence does **not** prove the actual matter/local generator `v_m` satisfies it, and it also does not give a sourced nonzero `v_m^q` coefficient. So the coupling is no longer vague, but local-lock reentry remains blocked.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## q Normalization Alias Audit

{markdown_table(rows["normalization"], ["normalization_id", "object", "formula", "status", "unit_statement", "effect", "selected_for_derivation", "mixed_norm_allowed", "valid_for_claim"])}

## Dqvm Derivation Ledger

{markdown_table(rows["derivation"], ["derivation_id", "step", "formula", "status", "implication", "derived_in_2827", "valid_for_claim"])}

## Vertical Kernel Condition

{markdown_table(rows["kernel"], ["kernel_id", "object", "zero_statement", "equivalent_condition", "meaning", "status", "satisfied_for_v_m", "valid_for_claim"])}

## Zero Nonzero Demotion Outcome Ledger

{markdown_table(rows["outcomes"], ["outcome_id", "question", "status", "result", "effect", "promotion_allowed", "valid_for_claim"])}

## Cqm And Local Lock Reentry Status

{markdown_table(rows["cqm"], ["cqm_id", "object", "formula", "status", "blocker", "numeric_value_present", "source_backed_value", "valid_for_claim"])}

## Claim Gates

{markdown_table(rows["gates"], ["claim_gate_id", "claim", "gate_passed", "status", "reason", "claim_allowed"])}

## Decision Ledger

{markdown_table(rows["decision"], ["decision_id", "decision", "result", "because", "next_action", "valid_for_claim"])}

## Next Target

{markdown_table(rows["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(rows["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(rows["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows: dict[str, list[dict[str, Any]]] = {}
    rows["sources"] = source_rows()
    rows["normalization"] = normalization_rows()
    rows["derivation"] = derivation_rows()
    rows["kernel"] = kernel_rows()
    rows["outcomes"] = outcome_rows()
    rows["cqm"] = cqm_rows()
    rows["gates"] = gate_rows(rows)
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "normalization", "derivation", "kernel", "outcomes", "cqm", "gates", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])

    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2827_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2827_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
