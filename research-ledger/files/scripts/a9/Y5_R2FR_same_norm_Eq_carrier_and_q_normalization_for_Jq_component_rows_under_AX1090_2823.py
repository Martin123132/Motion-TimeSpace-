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

DOC = ROOT / "2823-Y5-R2FR-same-norm-Eq-carrier-and-q-normalization-for-Jq-component-rows-under-AX1090.md"

SRC_2822_NEXT = RESIDUALS / "P8_Y5_R2FR_2822_NEXT_TARGET.csv"
SRC_2822_DECISION = RESIDUALS / "P8_Y5_R2FR_2822_DECISION_LEDGER.csv"
SRC_2822_FIRST_ROW = RESIDUALS / "P8_Y5_R2FR_2822_FIRST_SAME_NORM_JQ_COMPONENT_ROW.csv"
SRC_2822_FALLBACK = RESIDUALS / "P8_Y5_R2FR_2822_COMPONENT_BOUND_FALLBACK_VECTOR.csv"
SRC_2822_IMPACT = RESIDUALS / "P8_Y5_R2FR_2822_LOCAL_LOCK_IMPACT_GATE.csv"
SRC_2820_EXTRACTION = RESIDUALS / "P8_Y5_R2FR_2820_EQ_MU_GAB_EXTRACTION_STATUS.csv"
SRC_2739_HUNT = RESIDUALS / "P8_Y5_R2FR_2739_PARENT_QNORM_SOURCE_HUNT.csv"
SRC_2739_REENTRY = RESIDUALS / "P8_Y5_R2FR_2739_QNORM_REENTRY_CONDITIONS.csv"
SRC_2740_ALGO = RESIDUALS / "P8_Y5_R2FR_2740_QNORM_EXTRACTION_ALGORITHM.csv"
SRC_2741_SMOKE = RESIDUALS / "P8_Y5_R2FR_2741_QNORM_EXTRACTION_SMOKE.csv"
SRC_1550_CANDIDATE = RESIDUALS / "P8_Y5_PARENT_QLOC_1550_QNORM_CANDIDATE_AUDIT.csv"
SRC_1550_REFUSAL = RESIDUALS / "P8_Y5_PARENT_QLOC_1550_QNORM_REFUSAL_RUNNER_NONCLAIM.csv"
SRC_1551_HUNT = RESIDUALS / "P8_Y5_PARENT_QLOC_1551_PARENT_QNORM_SOURCE_HUNT.csv"
SRC_1552_ALGO = RESIDUALS / "P8_Y5_PARENT_QLOC_1552_QNORM_EXTRACTION_ALGORITHM.csv"
SRC_1553_SMOKE = RESIDUALS / "P8_Y5_PARENT_QLOC_1553_QNORM_EXTRACTION_SMOKE_NONCLAIM.csv"
SRC_2281_OPERATOR = RESIDUALS / "P8_Y5_PARENT_QLOC_2281_Q_OPERATOR_CONTRACT.csv"
SRC_2281_STIFFNESS = RESIDUALS / "P8_Y5_PARENT_QLOC_2281_Q_STIFFNESS_DERIVATION_AUDIT.csv"
SRC_2281_SELECTOR = RESIDUALS / "P8_Y5_PARENT_QLOC_2281_COVARIANCE_MANIFOLD_SELECTOR_GAP.csv"
SRC_2281_DECISION = RESIDUALS / "P8_Y5_PARENT_QLOC_2281_DECISION_LEDGER.csv"
SRC_2282_EQUIV = RESIDUALS / "P8_Y5_PARENT_QLOC_2282_Q_OBSERVER_CELL_EQUIVALENCE.csv"
SRC_2282_SELECTOR = RESIDUALS / "P8_Y5_PARENT_QLOC_2282_SELECTOR_ROUTE_AUDIT.csv"
SRC_2282_CLOSURE = RESIDUALS / "P8_Y5_PARENT_QLOC_2282_Q_CLOSURE_DECLARATION.csv"
SRC_2308_NORMAL = RESIDUALS / "P8_Y5_PARENT_QLOC_2308_Q_LOCAL_ACTION_NORMAL_FORM_CONTRACT.csv"
SRC_2308_OPERATOR = RESIDUALS / "P8_Y5_PARENT_QLOC_2308_Q_OPERATOR_X_BRIDGE_AUDIT.csv"
SRC_2308_GATES = RESIDUALS / "P8_Y5_PARENT_QLOC_2308_ACCEPTANCE_GATES.csv"
SRC_2314_HUNT = RESIDUALS / "P8_Y5_PARENT_QLOC_2314_HESSIAN_SOURCE_HUNT.csv"
SRC_2755_PACK = RESIDUALS / "P8_Y5_R2FR_2755_INDEPENDENT_Q_HESSIAN_SOURCE_PACK.csv"
SRC_2756_PACK = RESIDUALS / "P8_Y5_R2FR_2756_INDEPENDENT_Q_HESSIAN_SOURCE_PACK.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2823_SOURCE_REGISTER.csv",
    "carrier_audit": RESIDUALS / "P8_Y5_R2FR_2823_EQ_CARRIER_CANDIDATE_AUDIT.csv",
    "conditional_carrier": RESIDUALS / "P8_Y5_R2FR_2823_COVARIANCE_HESSIAN_CONDITIONAL_EQ_ROW.csv",
    "normalization_gate": RESIDUALS / "P8_Y5_R2FR_2823_Q_NORMALIZATION_AND_DUAL_UNITS_GATE.csv",
    "reentry_impact": RESIDUALS / "P8_Y5_R2FR_2823_COMPONENT_ROW_REENTRY_IMPACT.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2823_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2823_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2823_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2823_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2823_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "carrier_copy": SOURCE_WEIGHT / "covariance_hessian_Eq_carrier_2823_NONCLAIM.csv",
    "local_copy": LOCAL_BOUNDS / "Eq_carrier_component_reentry_2823_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2823_COVARIANCE_HESSIAN_SOURCE_EXTRACTION_NEXT.csv",
}

BRANCH_ID = "MTS_R2FR_EQ_CARRIER_Q_NORMALIZATION_2823"


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
        path.mkdir(parents=True, exist_ok=True)


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


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


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
        ("SRC2823_0_2822_next", SRC_2822_NEXT, "NEXT2822_0_2823", "2822 handoff to E_q carrier/q-normalization"),
        ("SRC2823_1_2822_decision", SRC_2822_DECISION, "DEC2822_2_blocker;DEC2822_3_next", "same-norm carrier bottleneck"),
        ("SRC2823_2_2822_first_row", SRC_2822_FIRST_ROW, "JQC2822_0_j_matter_first_row;MISSING_PARENT_EQ_NORM", "first Jq component row awaiting carrier"),
        ("SRC2823_3_2822_fallback", SRC_2822_FALLBACK, "FB2822_0_total;FB2822_7_curvature", "component vector awaiting carrier"),
        ("SRC2823_4_2822_impact", SRC_2822_IMPACT, "IMP2822_2_Eq;IMP2822_4_Nlock", "local-lock blocked by E_q"),
        ("SRC2823_5_2820_extraction", SRC_2820_EXTRACTION, "EXT2820_1_GAB;EXT2820_2_muq;EXT2820_3_Eq", "missing G_AB/mu_q/E_q status"),
        ("SRC2823_6_2739_hunt", SRC_2739_HUNT, "HUNT2739_0_operator_metric;HUNT2739_5_verdict", "R2FR qnorm source hunt"),
        ("SRC2823_7_2739_reentry", SRC_2739_REENTRY, "RE2739_1_Eq;RE2739_8_claim_policy", "qnorm reentry requirements"),
        ("SRC2823_8_2740_algo", SRC_2740_ALGO, "ALG2740_2_second_variation;ALG2740_3_extract_E", "qnorm extraction algorithm"),
        ("SRC2823_9_2741_smoke", SRC_2741_SMOKE, "SMOKE2741_0_auxiliary_E;SMOKE2741_5_phase_volume_E", "qnorm smoke routes"),
        ("SRC2823_10_1550_candidate", SRC_1550_CANDIDATE, "QN1550_0_parent_kinetic_energy_norm;QN1550_4_current_verdict", "original qnorm candidates"),
        ("SRC2823_11_1550_refusal", SRC_1550_REFUSAL, "RUN1550_0_parent_norm;RUN1550_4_holder", "original refusal runner"),
        ("SRC2823_12_1551_hunt", SRC_1551_HUNT, "HUNT1551_0_parent_operator_metric;HUNT1551_5_current_verdict", "original parent norm hunt"),
        ("SRC2823_13_1552_algo", SRC_1552_ALGO, "ALG1552_1_second_variation;ALG1552_2_extract_E", "original extraction algorithm"),
        ("SRC2823_14_1553_smoke", SRC_1553_SMOKE, "SMOKE1553_0_auxiliary_E;SMOKE1553_4_kinetic_E", "original qnorm smoke"),
        ("SRC2823_15_2281_operator", SRC_2281_OPERATOR, "QOC2281_0_action_term;QOC2281_4_newton_limit", "q operator contract"),
        ("SRC2823_16_2281_stiffness", SRC_2281_STIFFNESS, "QSD2281_2_transverse_q_mass;QSD2281_4_operator", "conditional covariance Hessian derivation"),
        ("SRC2823_17_2281_selector", SRC_2281_SELECTOR, "CSG2281_1_metric_compatibility;CSG2281_4_direct_penalty", "selector gap"),
        ("SRC2823_18_2281_decision", SRC_2281_DECISION, "DEC2281_0_real_gain;DEC2281_2_local_branch_status", "conditional gain and no-claim status"),
        ("SRC2823_19_2282_equiv", SRC_2282_EQUIV, "QOE2282_1_q_zero_to_reciprocity;QOE2282_3_strain_relation", "q/observer-cell equivalence"),
        ("SRC2823_20_2282_selector", SRC_2282_SELECTOR, "SEL2282_1_metric_compatibility;SEL2282_6_direct_q_penalty", "selector route audit"),
        ("SRC2823_21_2282_closure", SRC_2282_CLOSURE, "QCD2282_0_status;QCD2282_1_equivalence_gain", "closure declaration"),
        ("SRC2823_22_2308_normal", SRC_2308_NORMAL, "NF2308_0_minimal_action;NF2308_2_range", "local q action normal form"),
        ("SRC2823_23_2308_operator", SRC_2308_OPERATOR, "QOP2308_1_positive_operator_contract;QOP2308_4_verdict", "operator bridge audit"),
        ("SRC2823_24_2308_gates", SRC_2308_GATES, "ACC2308_2_operator;ACC2308_4_projection_runner", "operator acceptance gates"),
        ("SRC2823_25_2314_hunt", SRC_2314_HUNT, "HUNT2314_1_conditional_mass;HUNT2314_5_verdict", "independent q Hessian first fill"),
        ("SRC2823_26_2755_pack", SRC_2755_PACK, "IQH2755_0_Zq;IQH2755_5_claim_gate", "R2FR independent q Hessian source pack"),
        ("SRC2823_27_2756_pack", SRC_2756_PACK, "FB2756_1_Zq;FB2756_8_score_gate", "R2FR q-removal/Hessian fallback pack"),
    ]
    return [source_row(*spec) for spec in specs]


def carrier_audit_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "EQA2823_0_covariance_hessian",
            "covariance Hessian operator carrier",
            "E_q[delta q]^2 = int_W (Z_q |nabla delta q|^2 + M_q^2 delta q^2) dV_e",
            "CONDITIONAL_CARRIER_SHAPE_DERIVED",
            "requires parent-selected q=0 equilibrium, positive H_AB, xi_q, units, and boundary domain",
            SRC_2281_STIFFNESS,
            "QSD2281_4_operator",
        ),
        (
            "EQA2823_1_auxiliary_algebraic",
            "auxiliary algebraic q norm",
            "E_aux[delta q]^2 = int_W mu_q^2 delta q^A G_AB delta q^B dV_e",
            "FORMALLY_EXTRACTABLE_IF_GAB_SOURCED",
            "G_AB, mu_q, q map, and matter coupling are missing",
            SRC_2741_SMOKE,
            "SMOKE2741_0_auxiliary_E",
        ),
        (
            "EQA2823_2_parent_operator_metric",
            "direct parent operator metric G_AB",
            "||delta q||_E^2 = int_W delta q^A G_AB[q,e_obs] delta q^B dV_e",
            "MISSING_PARENT_OPERATOR_METRIC",
            "best direct route but no source row provides positive G_AB",
            SRC_1550_CANDIDATE,
            "QN1550_0_parent_kinetic_energy_norm",
        ),
        (
            "EQA2823_3_worldtube_regulator",
            "regularized worldtube norm",
            "E_epsilon[delta q;W_src] from parent regulator/excision law",
            "MISSING_REGULATOR_AND_DOMAIN",
            "epsilon_reg, support, boundary flux, and limiting procedure absent",
            SRC_2739_HUNT,
            "HUNT2739_2_regulator",
        ),
        (
            "EQA2823_4_constraint_no_pole",
            "pure constraint/no-pole route",
            "q absent or first-class removed before a Green operator is needed",
            "BETTER_IF_SIGNED_BUT_NOT_PARENT_SIGNED",
            "first-class/vertical removal and boundary/source silence are unsigned",
            SRC_2308_OPERATOR,
            "QOP2308_3_no_pole_route",
        ),
        (
            "EQA2823_5_kinetic_RAB",
            "old kinetic R_AB route",
            "propagating R_AB norm",
            "REJECTED_FOR_CURRENT_QNORM",
            "reintroduces exterior reciprocal hair and contradicts nonpropagating route",
            SRC_2739_HUNT,
            "HUNT2739_4_rejected_RAB",
        ),
        (
            "EQA2823_6_verdict",
            "accepted parent E_q carrier",
            "none accepted as parent-signed",
            "NO_ACCEPTED_PARENT_CARRIER",
            "conditional Hessian carrier is staged but cannot feed claims",
            SRC_2822_IMPACT,
            "IMP2822_2_Eq",
        ),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "carrier_id": carrier_id,
                "candidate": candidate,
                "formula": formula,
                "status": status,
                "blocker": blocker,
                "source_path": str(source_path),
                "source_anchor": anchor,
                "anchor_found": anchor in read_text(source_path),
                "parent_signed": False,
                "conditional_shape_available": carrier_id == "EQA2823_0_covariance_hessian",
                "feeds_2818_reentry": False,
            }
        )
        for carrier_id, candidate, formula, status, blocker, source_path, anchor in specs
    ]


def conditional_carrier_rows() -> list[dict[str, Any]]:
    specs = [
        ("CCR2823_0_q_variable", "q", "q = C_R - C_T/(1-C_T); q=0 iff T^2 S=1 iff R_AB=0", "EXACT_EQUIVALENCE_CONDITIONAL_MAP", "parent covariance normalization and selector still unsigned", SRC_2282_EQUIV, "QOE2282_1_q_zero_to_reciprocity"),
        ("CCR2823_1_Mq2", "M_q^2", "M_q^2 = n_q^A H_AB n_q^B", "DERIVED_IF_H_POSITIVE_AND_Q_NORMAL_NONZERO", "H_AB and q=0 equilibrium selector not parent-signed", SRC_2281_STIFFNESS, "QSD2281_2_transverse_q_mass"),
        ("CCR2823_2_Zq", "Z_q", "Z_q = xi_q^2 n_q^A H_AB n_q^B", "DERIVED_IF_XI_Q_POSITIVE", "smoothing kernel/correlation length xi_q not sourced", SRC_2281_STIFFNESS, "QSD2281_3_gradient_expansion"),
        ("CCR2823_3_lambda", "lambda_q", "lambda_q = sqrt(Z_q/M_q^2) = xi_q", "EXACT_CONDITIONAL_RATIO", "same normalization, positive M_q^2, and xi_q source required", SRC_2314_HUNT, "HUNT2314_3_range_ratio"),
        ("CCR2823_4_Eq_form", "E_q", "E_q[delta q]^2 = int_W (Z_q |nabla delta q|^2 + M_q^2 delta q^2) dV_e plus boundary terms", "CONDITIONAL_CARRIER_FORM_READY", "not parent-signed; boundary/domain/units unresolved", SRC_2281_STIFFNESS, "QSD2281_4_operator"),
        ("CCR2823_5_positive", "coercivity", "Z_q>=Z_min>0 and M_q^2>=M_min^2>0 after quotient/gauge reduction", "CONDITIONAL_FROM_HESSIAN_ONLY", "positive Hessian proof and zero-mode audit missing", SRC_2281_OPERATOR, "QOC2281_1_positivity"),
        ("CCR2823_6_boundary", "boundary", "int_boundary Z_q q n^i nabla_i q = 0 or <= epsilon_boundary", "UNSIGNED", "local cell boundary class/no-flux theorem/matching missing", SRC_2281_OPERATOR, "QOC2281_2_boundary"),
    ]
    return [
        nonclaim(
            {
                "carrier_row_id": row_id,
                "object": obj,
                "formula": formula,
                "status": status,
                "blocker": blocker,
                "source_path": str(source_path),
                "source_anchor": anchor,
                "anchor_found": anchor in read_text(source_path),
                "numeric_value_present": False,
                "source_backed": False,
                "parent_signed": False,
                "usable_for_control_only": True,
                "feeds_2818_reentry": False,
            }
        )
        for row_id, obj, formula, status, blocker, source_path, anchor in specs
    ]


def normalization_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("QNG2823_0_q_definition", "q variable", "q=C_R-C_T/(1-C_T)", "EXACT_WITHIN_COVARIANCE_MAP", "covariance-to-observer definitions imported", True, False),
        ("QNG2823_1_q_dimension", "dim(q)", "dimensionless if C_R and C_T are normalized covariance ratios", "CONDITIONAL_DIMENSION", "parent normalization of covariance components not signed", False, False),
        ("QNG2823_2_Eq_units", "E_q units", "action/free-energy density norm over W_src", "UNRESOLVED", "H_AB, xi_q, dV_e, and q normalization source missing", False, False),
        ("QNG2823_3_dual_units", "J_q dual units", "J_q pairs with delta q in same E_q dual", "CONDITIONAL_ONLY", "cannot type B_matter^q until E_q carrier is owned", False, False),
        ("QNG2823_4_Cqm_units", "Dq[v_m] units", "C_qm=||Dq[v_m]||_{E_q}", "CONDITIONAL_ONLY", "Dq[v_m] and v_m normalization not computable in E_q", False, False),
        ("QNG2823_5_branch_lock", "same branch lock", "numerator, denominator, q normalization, and projection share one parent branch", "PASS_GUARD_NONCLAIM", "active guard; no mixed norms allowed", True, False),
        ("QNG2823_6_Newton_source", "Newton/source normalization", "same parent source must recover Newtonian mechanics", "SEPARATE_DEBT_RETAINED", "worldtube/Hilbert source equality and measured-GM pullback remain unsolved", False, False),
    ]
    return [
        nonclaim(
            {
                "gate_id": gate_id,
                "object": obj,
                "requirement": req,
                "status": status,
                "blocker": blocker,
                "conditional_piece_available": conditional,
                "accepted_for_reentry": accepted,
                "source_path": str(SRC_2281_OPERATOR),
            }
        )
        for gate_id, obj, req, status, blocker, conditional, accepted in specs
    ]


def reentry_impact_rows() -> list[dict[str, Any]]:
    specs = [
        ("RI2823_0_component_rows", "J_q component rows", "CONTROL_ONLY", "conditional E_q shape helps organize rows but does not make them source-backed", False),
        ("RI2823_1_jmatter", "j_matter first row", "STILL_NONCLAIM", "B_matter^q lacks E_q units and numeric/source-backed value", False),
        ("RI2823_2_Tsource", "T_source_norm", "UNCOMPUTABLE", "dual norm cannot be evaluated without source-backed E_q and J_q rows", False),
        ("RI2823_3_Cqm", "C_qm", "UNCOMPUTABLE", "Dq[v_m] not evaluated in E_q", False),
        ("RI2823_4_Nlock", "2818 N_lock", "NO_REENTRY", "S_cg,total remains closure/control-only", False),
        ("RI2823_5_claims", "local GR/Newton/PPN/R10", "BLOCKED_NO_CLAIM", "conditional carrier is not a derived local branch", False),
    ]
    return [
        nonclaim(
            {
                "impact_id": impact_id,
                "object": obj,
                "status": status,
                "reason": reason,
                "reentry_allowed": reentry_allowed,
            }
        )
        for impact_id, obj, status, reason, reentry_allowed in specs
    ]


def gate_rows(rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    sources_ok = all(row["path_exists"] and row["anchors_found"] for row in rows["sources"])
    conditional_carrier = any(row["conditional_shape_available"] for row in rows["carrier_audit"])
    parent_carrier = any(row["parent_signed"] for row in rows["conditional_carrier"])
    all_coeffs = all(row["source_backed"] and row["numeric_value_present"] for row in rows["conditional_carrier"])
    accepted_units = any(row["accepted_for_reentry"] for row in rows["normalization_gate"])
    reentry = any(row["reentry_allowed"] for row in rows["reentry_impact"])
    specs = [
        ("CG2823_0_sources", "source anchors present", sources_ok, "all imported carrier ledgers are reproducible"),
        ("CG2823_1_conditional_carrier", "conditional covariance-Hessian carrier shape available", conditional_carrier, "operator form M_q^2/Z_q/lambda_q is staged"),
        ("CG2823_2_parent_carrier", "parent-signed E_q carrier accepted", parent_carrier, "selector/H_AB/xi_q/units/boundary remain unsigned"),
        ("CG2823_3_coefficients", "G_AB or H_AB, mu_q/Z_q/M_q^2, xi_q source-backed", all_coeffs, "no coefficient row has numeric/source-backed value"),
        ("CG2823_4_units", "q normalization and dual units accepted", accepted_units, "dimension/dual norm unresolved"),
        ("CG2823_5_local_lock_reentry", "component rows feed 2818 local-lock", reentry, "T_source_norm and C_qm remain uncomputable"),
        ("CG2823_6_local_claim", "local GR/Newton/PPN/R10 claim allowed", False, "no sourced local branch exists"),
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
        ("DEC2823_0_gain", "The covariance-Hessian route supplies the best conditional E_q carrier shape.", "CONDITIONAL_CARRIER_SHAPE_STAGED", "M_q^2, Z_q, lambda_q, and the E_q quadratic form are mathematically linked if q=0 is parent-selected", "use as control-only structure for now"),
        ("DEC2823_1_no_claim", "Do not promote E_q as parent-signed.", "PARENT_CARRIER_NOT_ACCEPTED", "selector, H_AB, xi_q, q units, boundary/domain, and Newton source normalization remain unsigned", "keep component rows nonclaim"),
        ("DEC2823_2_no_hand_norm", "Reject hand-inserted G_AB/mu_q or arena convenience norms.", "GUARD_ACTIVE", "that would turn the local branch into fitted patchwork", "require a covariance/Hessian/source path"),
        ("DEC2823_3_next", "Next target is covariance-Hessian source extraction or explicit E_q control demotion.", "NEXT_2824_COVARIANCE_HESSIAN_SOURCE", "we need H_AB, xi_q, q normalization, and selector evidence before any same-norm component row can feed tests", "derive/source the carrier inputs or demote them to control-only runner rows"),
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
                "next_id": "NEXT2823_0_2824",
                "status": "selected_primary",
                "target_doc": "2824-Y5-R2FR-covariance-Hessian-source-extraction-or-Eq-control-demotion-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_covariance_Hessian_source_extraction_or_Eq_control_demotion_under_AX1090_2824.py",
                "mission": "derive or source the covariance-Hessian carrier inputs H_AB, xi_q, q normalization, q=0 selector, and boundary/domain class; otherwise demote E_q to an explicit control-only carrier for nonclaim local-lock smoke rows",
                "acceptance": "either produce parent-signed/numeric source rows for the E_q carrier or write a control-only demotion ledger proving no component row can enter claims",
                "forbidden": "do not insert G_AB, mu_q, Z_q, M_q^2, xi_q, or q units by hand; do not import EH/GR AB=1 as proof; do not claim local GR/Newton/PPN/R10; do not edit formalization-workbench",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("BR2823_0_carrier_copy", OUTPUTS["conditional_carrier"], BRANCH_OUTPUTS["carrier_copy"], "source-weight copy of conditional covariance-Hessian E_q carrier row"),
        ("BR2823_1_local_copy", OUTPUTS["reentry_impact"], BRANCH_OUTPUTS["local_copy"], "local-bound copy of component reentry impact"),
        ("BR2823_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB acquisition queue for covariance-Hessian source extraction"),
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
                    if not item or item.startswith("http"):
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


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_paths = [path for path in OUTPUTS.values() if path != OUTPUTS["validation"]]
    branch_paths = list(BRANCH_OUTPUTS.values())
    cited_paths = iter_cited_paths(rows_by_name)
    checks = [
        ("VAL2823_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2823_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2823_2_conditional_carrier_shape", any(row["conditional_shape_available"] for row in rows_by_name["carrier_audit"]), "conditional covariance-Hessian carrier shape is recorded"),
        ("VAL2823_3_no_parent_carrier", not any(row["parent_signed"] for row in rows_by_name["conditional_carrier"]), "no parent-signed E_q carrier was accepted"),
        ("VAL2823_4_no_sourcebacked_coeffs", not any(row["source_backed"] or row["numeric_value_present"] for row in rows_by_name["conditional_carrier"]), "carrier coefficients remain unsourced/non-numeric"),
        ("VAL2823_5_units_blocked", not any(row["accepted_for_reentry"] for row in rows_by_name["normalization_gate"]), "q normalization and dual units remain blocked"),
        ("VAL2823_6_reentry_blocked", not any(row["reentry_allowed"] for row in rows_by_name["reentry_impact"]), "component rows cannot reenter 2818 local-lock"),
        ("VAL2823_7_next_target_2824", any(row["next_id"] == "NEXT2823_0_2824" and row["selected"] for row in rows_by_name["next"]), "covariance-Hessian source extraction selected next"),
        ("VAL2823_8_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2823_9_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2823_10_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2823_11_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2823_12_no_claim_flags", no_claim_flags(rows_by_name), "no score_ready, valid_prediction_row, valid_for_claim, or claim_allowed flag is true"),
        ("VAL2823_13_generated_under_post_checkpoint", all(str(path).startswith(str(ROOT)) for path in output_paths + branch_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2823_14_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2823_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
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
            "validation_id": "VAL2823_OVERALL",
            "passed": overall,
            "detail": "2823 stages the covariance-Hessian E_q carrier shape as the best conditional same-norm route, refuses parent promotion because selector/coefficient/unit inputs are unsigned, and selects covariance-Hessian source extraction or E_q control demotion next.",
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
    content = f"""# 2823 - Y5 R2FR Same-Norm Eq Carrier And Q Normalization For Jq Component Rows Under AX1090

Status: `Y5_R2FR_2823_covariance_Hessian_Eq_carrier_conditional_parent_carrier_not_signed`

## Private Verdict

2823 finds the best honest carrier route, but does not promote it.

The best route is the covariance-Hessian carrier:

`E_q[delta q]^2 = int_W (Z_q |nabla delta q|^2 + M_q^2 delta q^2) dV_e`

with `M_q^2 = n_q^A H_AB n_q^B`, `Z_q = xi_q^2 n_q^A H_AB n_q^B`, and therefore `lambda_q = xi_q` if the same normalization and positivity assumptions hold.

That is a real structural gain: the norm is no longer just a foggy placeholder. But it is not parent-signed because the q=0 selector, covariance Hessian source, smoothing length, q units, boundary/domain class, and Newton/source normalization are still not supplied. So the `j_matter` component row remains control-only and cannot feed the 2818 local-lock amplitude law yet.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Eq Carrier Candidate Audit

{markdown_table(rows["carrier_audit"], ["carrier_id", "candidate", "status", "blocker", "conditional_shape_available", "parent_signed", "feeds_2818_reentry", "valid_for_claim"])}

## Covariance Hessian Conditional Eq Row

{markdown_table(rows["conditional_carrier"], ["carrier_row_id", "object", "status", "formula", "blocker", "usable_for_control_only", "feeds_2818_reentry", "valid_for_claim"])}

## Q Normalization And Dual Units Gate

{markdown_table(rows["normalization_gate"], ["gate_id", "object", "status", "requirement", "blocker", "conditional_piece_available", "accepted_for_reentry", "valid_for_claim"])}

## Component Row Reentry Impact

{markdown_table(rows["reentry_impact"], ["impact_id", "object", "status", "reason", "reentry_allowed", "valid_for_claim"])}

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
    rows["carrier_audit"] = carrier_audit_rows()
    rows["conditional_carrier"] = conditional_carrier_rows()
    rows["normalization_gate"] = normalization_gate_rows()
    rows["reentry_impact"] = reentry_impact_rows()
    rows["gates"] = gate_rows(rows)
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "carrier_audit", "conditional_carrier", "normalization_gate", "reentry_impact", "gates", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])

    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2823_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2823_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
