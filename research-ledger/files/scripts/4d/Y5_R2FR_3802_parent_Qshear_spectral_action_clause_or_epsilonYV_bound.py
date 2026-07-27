import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3802"
BRANCH = "MTS_R2FR_Y5_PARENT_QSHEAR_SPECTRAL_ACTION_CLAUSE_OR_EPSILONYV_BOUND_3802"
ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework"
    r"\Motion-TimeSpace--main"
)
PCW = ROOT / "post-checkpoint-work"
FWB = ROOT / "formalization-workbench"
RESIDUALS = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3802-Y5-R2FR-parent-Qshear-spectral-action-clause-or-epsilonYV-bound.md"

P_3784 = PCW / "3784-Y5-R2FR-parent-U1-action-clause-or-EM-finite-bound-mode.md"
P_3792 = PCW / "3792-Y5-R2FR-same-current-Ward-Hilbert-stress-owner-or-epsilonJ-bound.md"
P_3795 = PCW / "3795-Y5-R2FR-Qflow-two-pair-lift-or-Bperp-profile-first-input.md"
P_3796 = PCW / "3796-Y5-R2FR-Qshear-eigenframe-chart-or-first-Bperp-arena-fill.md"
P_3801 = PCW / "3801-Y5-R2FR-qobs-Qshear-spectral-ownership-or-selector-leakage-fill.md"
P_SPINE = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

C_3801_FILL = RESIDUALS / "P8_Y5_R2FR_3801_SELECTOR_LEAKAGE_FILL_ROWS.csv"
C_3801_CONTRACT = RESIDUALS / "P8_Y5_R2FR_3801_QOBS_XQ_OWNERSHIP_CONTRACT.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3802_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_3802_PARENT_QSHEAR_SPECTRAL_ACTION_THEOREM.csv",
    "contract": RESIDUALS / "P8_Y5_R2FR_3802_PARENT_ACTION_SIGNATURE_CONTRACT.csv",
    "audit": RESIDUALS / "P8_Y5_R2FR_3802_CURRENT_CORPUS_ACTION_AUDIT.csv",
    "bound_rows": RESIDUALS / "P8_Y5_R2FR_3802_EPSILON_YV_BOUND_FILL_ROWS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3802_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3802_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3802_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3802_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3802_VALIDATION.csv",
}

SOURCE_SPECS = [
    {
        "source_id": "SRC3802_0_3801_handoff",
        "path": P_3801,
        "needle": "Try to write a parent action/signature clause",
        "role": "3801 selected parent Q-shear action clause or epsilonYV fill",
    },
    {
        "source_id": "SRC3802_1_3796_qshear_chart",
        "path": P_3796,
        "needle": "S=R diag(s1,s2,-s1-s2) R^T",
        "role": "conditional tracefree-shear spectral chart",
    },
    {
        "source_id": "SRC3802_2_3795_qflow_split",
        "path": P_3795,
        "needle": "Q_coh^i_j=(N_D/u3) delta^i_j",
        "role": "Qcoh isotropic split and shear fork",
    },
    {
        "source_id": "SRC3802_3_3784_action_grammar",
        "path": P_3784,
        "needle": "S_U1=int sqrt(-g_eff)",
        "role": "parent U1 action grammar that exposes B_Q owner slot",
    },
    {
        "source_id": "SRC3802_4_3792_same_source",
        "path": P_3792,
        "needle": "Assume S_src=S_charged[psi,g_obs,A_Q,theta]+S_EM",
        "role": "same-source/Hilbert stress contract",
    },
    {
        "source_id": "SRC3802_5_3801_fill_rows",
        "path": C_3801_FILL,
        "needle": "SLF3801_2_epsilon_YV",
        "role": "selector leakage finite fill rows inherited from 3801",
    },
    {
        "source_id": "SRC3802_6_3801_contract",
        "path": C_3801_CONTRACT,
        "needle": "QXC3801_5_same_source_EM",
        "role": "q_X ownership contract inherited from 3801",
    },
    {
        "source_id": "SRC3802_7_spine",
        "path": P_SPINE,
        "needle": "3802-Y5-R2FR-parent-Qshear-spectral-action-clause-or-epsilonYV-bound.md",
        "role": "live spine target for this checkpoint",
    },
]


def read_text(path):
    return path.read_text(encoding="utf-8", errors="replace")


def load_csv(path):
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path):
    try:
        load_csv(path)
        return True
    except Exception:
        return False


def bool_text(value):
    return "true" if value else "false"


def source_register(timestamp):
    rows = []
    for spec in SOURCE_SPECS:
        exists = spec["path"].exists()
        needle_found = False
        if exists:
            needle_found = spec["needle"] in read_text(spec["path"])
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "source_id": spec["source_id"],
                "source_path": str(spec["path"]),
                "exists": bool_text(exists),
                "needle": spec["needle"],
                "needle_found": bool_text(needle_found),
                "role": spec["role"],
                "valid_for_claim": "false",
            }
        )
    return rows


def theorem_rows(timestamp):
    specs = [
        (
            "QSA3802_0_spectral_functor",
            "spectral functional calculus owner",
            "If S is a parent-owned h_eff-self-adjoint tracefree endomorphism and the discriminant Delta_S=prod_{a<b}(s_a-s_b)^2 is positive on U_reg, then the eigenvalues s_a and spectral projectors P_a=prod_{b!=a}(S-s_b I)/(s_a-s_b) are smooth functorial functions of S.",
            "EXACT_LOCAL_SPECTRAL_THEOREM",
            "Q-shear spectral data can be parent-owned without inserting raw eigenframe angles by hand.",
            "current corpus has not parent-signed S, U_reg, projector ownership, or degeneracy support",
        ),
        (
            "QSA3802_1_chart_replacement",
            "chart-covariant X_Q",
            "The physical object is the spectral class Xhat_Q=(s_a,P_a) with local coordinate charts X_Q=(s1,s2,alpha,beta,gamma); angle coordinates are chart representatives, not invariant parent fields.",
            "NO_SMUGGLE_REPAIR",
            "Pi4 must be a chart-covariant map from the spectral bundle, not a post-hoc angle choice.",
            "no current source supplies chart transitions or Pi4 covariance",
        ),
        (
            "QSA3802_2_parent_constraint_action",
            "parent Q-shear action signature",
            "A valid extension clause may add L_Qspec=lambda_X.(X_Q-Spec(S[Q]))+lambda_Y.(Y_Q-Pi4(X_Q))+L_degen+L_domain before EM readout, with Pi4 fixed by parent data and no dependence on A_obs,F_obs,or fitted alpha/R10 data.",
            "CONDITIONAL_PARENT_ACTION_GRAMMAR",
            "This owns X_Q and Y_Q as parent variables rather than fitted EM variables.",
            "the clause is written here but not found in the strict current corpus",
        ),
        (
            "QSA3802_3_action_to_qX_zero",
            "action clause to Hperp zero",
            "If QSA3802_0-2 are parent-signed and q_X=(q_obs,X_Q) is the observed quotient, then DX_Q[V_X]=0, dY_Q[V_X]=0, H_Q is q_X-basic, and 3799/3800 give Hperp=0 relative to q_X.",
            "EXACT_CONDITIONAL_ZERO_CHAIN",
            "This is the cleanest derivation route for the Q-shear branch.",
            "q_X, Pi4, same-source, no-extra-force, and calibration companion clauses remain unsigned",
        ),
        (
            "QSA3802_4_same_source_no_force_condition",
            "source safety condition",
            "The action clause is local-GR safe only if X_Q and Y_Q enter matter/gravity through the B_Q/EM sector inside one same-source Hilbert action, with partial L_matter/partial X_Q=0 outside declared EM response terms or a bounded epsilon_source_XQ.",
            "REQUIRED_CONSISTENCY_THEOREM",
            "Prevents Q-shear spectral ownership from becoming a hidden fifth force or source-normalization leak.",
            "epsilon_source_XQ and q_X same-source proof are missing",
        ),
        (
            "QSA3802_5_degeneracy_boundary_guard",
            "degeneracy support guard",
            "The action must either exclude Delta_S=0 from U_good, replace raw eigenframes by a smooth projector/CP-style multiplet, or carry eta_degen and eta_chart_transition into h_U.",
            "REQUIRED_REGULARITY_GATE",
            "Prevents fake smooth eigenframe ownership at the coherent/isotropic limit.",
            "degeneracy support and chart transition bounds remain missing",
        ),
        (
            "QSA3802_6_finite_bound_branch",
            "epsilonYV finite branch",
            "If the parent action signature is not signed, use epsilon_YV=max_A||D Pi4_X.DX_Q(E_A)||/Y_ref and h_U_response <= C_HY*epsilon_YV + eta_chart_transition + eta_degen, plus epsilon_source_XQ for direct source leakage.",
            "DERIVED_BOUND_BRANCH",
            "The finite path is explicit and testable instead of another missing-coupling sentence.",
            "epsilon_YV, C_HY, eta_chart_transition, eta_degen, and epsilon_source_XQ are unfilled",
        ),
    ]
    rows = []
    for theorem_id, claim_piece, mathematical_form, derivation_status, result_if_signed, missing in specs:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "theorem_id": theorem_id,
                "claim_piece": claim_piece,
                "mathematical_form": mathematical_form,
                "derivation_status": derivation_status,
                "result_if_signed": result_if_signed,
                "missing_for_current_claim": missing,
                "valid_for_claim": "false",
            }
        )
    return rows


def contract_rows(timestamp):
    specs = [
        (
            "PAC3802_0_Q_parent",
            "parent Q and coframe owner",
            "Q, h_eff, local spatial coframe/domain, and the trace/coherent split Q=Q_coh+S are parent fields or functors before smoothing/readout.",
            "MISSING_PARENT_Q_PROJECTOR_AND_DOMAIN",
        ),
        (
            "PAC3802_1_S_selfadjoint",
            "self-adjoint tracefree shear",
            "S must be h_eff-self-adjoint and tracefree so the spectral theorem applies on U_reg.",
            "MISSING_S_SELFADJOINT_PARENT_CERTIFICATE",
        ),
        (
            "PAC3802_2_Ureg_discriminant",
            "regular spectral domain",
            "Delta_S>0 on U_reg, or a declared defect/degeneracy support measure is supplied.",
            "MISSING_DEGENERACY_SUPPORT_CERTIFICATE",
        ),
        (
            "PAC3802_3_projector_atlas",
            "projector-based atlas",
            "Use spectral projectors P_a and transition-covariant charts, not naked eigenframe angles as parent variables.",
            "MISSING_PROJECTOR_ATLAS_AND_TRANSITIONS",
        ),
        (
            "PAC3802_4_Pi4_parent",
            "fixed parent Pi4",
            "Pi4:Xhat_Q->Y_Q is fixed by parent action/symmetry, rank-four where generic EM rank is claimed, and independent of A_obs/F_obs/data fits.",
            "MISSING_PARENT_PI4_SELECTOR",
        ),
        (
            "PAC3802_5_constraint_clause",
            "constraint action clause",
            "lambda_X.(X_Q-Spec(S[Q])) and lambda_Y.(Y_Q-Pi4(X_Q)) or equivalent constraints are present before EM readout.",
            "MISSING_QSPEC_ACTION_CLAUSE_IN_STRICT_CORPUS",
        ),
        (
            "PAC3802_6_qX_quotient",
            "q_X quotient signature",
            "q_X=(q_obs,X_Q) or q_Y=(q_obs,Y_Q) is the selected parent quotient with projection back to q_obs.",
            "MISSING_QX_PARENT_QUOTIENT_SIGNATURE",
        ),
        (
            "PAC3802_7_same_source",
            "same-source EM/Hilbert action",
            "B_Q[Y_Q], A_Q, J_Q, EM Hilbert stress, binding/apparatus stress, and boundary/domain terms remain inside one descended source action.",
            "MISSING_QX_SAME_SOURCE_RECHECK",
        ),
        (
            "PAC3802_8_no_extra_XQ_force",
            "no independent X_Q force",
            "No direct matter/source-normalization coupling to X_Q outside the declared EM/Hilbert sector, or epsilon_source_XQ is bounded.",
            "MISSING_NO_EXTRA_XQ_FORCE_CERTIFICATE",
        ),
        (
            "PAC3802_9_calibration",
            "calibration companions",
            "q_*, Z_EM, lambda_A, epsilon_J_Q, theta/material markers, and boundary/domain rows are zeroed or bounded under the same q_X branch.",
            "MISSING_QX_CALIBRATION_COMPANIONS",
        ),
    ]
    rows = []
    for clause_id, clause, requirement, current_status in specs:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "clause_id": clause_id,
                "clause": clause,
                "requirement": requirement,
                "current_status": current_status,
                "valid_for_claim": "false",
                "blocks_claim": "true",
            }
        )
    return rows


def audit_rows(timestamp):
    specs = [
        (
            "AUD3802_0_Qsplit",
            "Qcoh/shear split",
            "3795/3796 identify Q_coh and S, but parent-owned projector/domain remains unsigned.",
            "PARTIAL_CONDITIONAL",
            "MISSING_PARENT_Q_PROJECTOR_AND_DOMAIN",
        ),
        (
            "AUD3802_1_spectral_theorem",
            "spectral chart",
            "3796 proves conditional S=R diag(s1,s2,-s1-s2) R^T on U_reg.",
            "MATHEMATICAL_CONDITIONAL_ONLY",
            "MISSING_U_REG_AND_ATLAS_CERTIFICATE",
        ),
        (
            "AUD3802_2_action_clause",
            "Qspec action clause",
            "3802 writes the clause, but it is not present in the strict current corpus.",
            "PARENT_EXTENSION_NOT_CURRENT_DERIVATION",
            "MISSING_QSPEC_ACTION_IN_SOURCE_CORPUS",
        ),
        (
            "AUD3802_3_Pi4",
            "Pi4 selector",
            "No source fixes Pi4 by parent symmetry/action before EM readout.",
            "FAIL_CURRENT_ZERO_CLAIM",
            "MISSING_PARENT_PI4_SELECTOR",
        ),
        (
            "AUD3802_4_qX",
            "q_X quotient",
            "3801 gives exact q_X refinement theorem, but q_X is not parent-signed.",
            "FAIL_CURRENT_ZERO_CLAIM",
            "MISSING_QX_PARENT_SIGNATURE",
        ),
        (
            "AUD3802_5_same_source",
            "same-source/no-extra-force",
            "3792 gives the same-source theorem shape; q_X-specific same-source and no-extra-XQ-force clauses remain unsigned.",
            "REQUIRED_NOT_FILLED",
            "MISSING_QX_SAME_SOURCE_AND_NO_FORCE",
        ),
        (
            "AUD3802_6_finite_values",
            "finite epsilonYV branch",
            "3801 fill rows exist, but epsilon_YV, epsilon_source_XQ, eta_chart, eta_degen, and C_HY have no source values.",
            "REQUIRED_NOT_FILLED",
            "MISSING_EPSILONYV_NUMERIC_OR_ZERO_VALUES",
        ),
    ]
    rows = []
    for audit_id, item, current_evidence, status, missing in specs:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "audit_id": audit_id,
                "item": item,
                "current_evidence": current_evidence,
                "status": status,
                "missing_for_claim": missing,
                "valid_for_claim": "false",
            }
        )
    return rows


def bound_rows(timestamp):
    specs = [
        (
            "EYB3802_0_epsilon_Qprojector",
            "epsilon_Qprojector",
            "failure of parent Q->Qcoh+S projector/domain rule",
            "dimensionless_or_certificate",
            "MISSING_PARENT_Q_PROJECTOR_AND_DOMAIN",
        ),
        (
            "EYB3802_1_eta_degen",
            "eta_degen",
            "measure/amplitude of Delta_S=0 or repeated-eigenvalue support touching U_good",
            "dimensionless",
            "MISSING_DEGENERACY_SUPPORT_BOUND",
        ),
        (
            "EYB3802_2_eta_chart",
            "eta_chart_transition",
            "spectral atlas transition leakage for local X_Q charts",
            "dimensionless",
            "MISSING_PROJECTOR_ATLAS_TRANSITION_BOUND",
        ),
        (
            "EYB3802_3_epsilon_Pi4",
            "epsilon_Pi4_selector",
            "failure or variation of parent-fixed Pi4 selector before EM readout",
            "dimensionless_or_certificate",
            "MISSING_PARENT_PI4_SELECTOR",
        ),
        (
            "EYB3802_4_epsilon_YV",
            "epsilon_YV",
            "max_A||D Pi4_X.DX_Q(E_A)||/Y_ref for old q_obs verticals",
            "dimensionless",
            "MISSING_PARENT_PI4_AND_VERTICAL_QSHEAR_ACTION",
        ),
        (
            "EYB3802_5_C_HY",
            "C_HY",
            "operator norm transferring epsilon_YV to h_U_response",
            "dimensionless",
            "MISSING_HQ_PULLBACK_NORM_TRANSFER",
        ),
        (
            "EYB3802_6_epsilon_source_XQ",
            "epsilon_source_XQ",
            "non-EM source-action or matter-force leakage from X_Q after q_X refinement",
            "dimensionless",
            "MISSING_NO_EXTRA_XQ_FORCE_CERTIFICATE",
        ),
        (
            "EYB3802_7_hU_response_bound",
            "h_U_response_bound",
            "h_U_response <= C_HY*epsilon_YV + eta_chart_transition + eta_degen",
            "dimensionless",
            "BOUND_FORM_READY_NUMERIC_INPUTS_MISSING",
        ),
        (
            "EYB3802_8_local_claim_abs",
            "N_Qspec_local_abs",
            "epsilon_Qprojector+epsilon_Pi4_selector+C_HY*epsilon_YV+eta_chart_transition+eta_degen+epsilon_source_XQ",
            "dimensionless",
            "ABS_SUM_BOUND_READY_VALUES_MISSING",
        ),
    ]
    rows = []
    for row_id, symbol, formula, units, current_value in specs:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "row_id": row_id,
                "symbol": symbol,
                "formula": formula,
                "units": units,
                "current_value": current_value,
                "status": "REQUIRED_NOT_FILLED",
                "valid_for_claim": "false",
                "blocks_claim": "true",
            }
        )
    return rows


def claim_gate_rows(timestamp, grouped):
    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in grouped["sources"])
    specs = [
        (
            "CG3802_0_sources",
            sources_ok,
            False,
            "all source paths and needles found" if sources_ok else "one or more source paths/needles missing",
        ),
        (
            "CG3802_1_spectral_functor",
            True,
            False,
            "spectral projector functor theorem emitted",
        ),
        (
            "CG3802_2_action_clause_written",
            True,
            False,
            "conditional parent Qspec action clause written",
        ),
        (
            "CG3802_3_current_parent_signed",
            False,
            False,
            "strict current corpus does not contain signed Qspec action/Pi4/qX clauses",
        ),
        (
            "CG3802_4_same_source_no_force",
            False,
            False,
            "same-source/no-extra-XQ-force/calibration recheck remains open",
        ),
        (
            "CG3802_5_finite_rows",
            True,
            False,
            "finite epsilonYV/source leakage rows emitted but values are missing",
        ),
    ]
    rows = []
    for gate_id, passed, claim_allowed, details in specs:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "gate_id": gate_id,
                "pass": bool_text(passed),
                "claim_allowed": bool_text(claim_allowed),
                "details": details,
                "valid_for_claim": "false",
            }
        )
    return rows


def decision_rows(timestamp):
    specs = [
        (
            "DEC3802_0_progress",
            "A legitimate parent Q-shear spectral action clause now exists as a conditional extension.",
            "Spectral projectors are functorial in a parent-owned nondegenerate S, and constraint fields can own X_Q/Y_Q before EM readout.",
            "Use this as the exact parent-extension route, not as a strict-current claim.",
        ),
        (
            "DEC3802_1_chart_repair",
            "Raw eigenframe angles should be treated as local chart representatives, not parent objects.",
            "Projectors P_a and transition-covariant spectral bundle data avoid fake angle/eigenframe ownership.",
            "Route future Pi4 work through chart-covariant spectral data.",
        ),
        (
            "DEC3802_2_nonclaim",
            "No local-GR/R10/clock/PPN/orbital claim follows from 3802.",
            "The action clause is not in the strict corpus and same-source/no-extra-force/calibration companions are unsigned.",
            "Keep all claim gates closed.",
        ),
        (
            "DEC3802_3_next",
            "The next target should test whether the Qspec action clause is source-safe.",
            "If variation introduces a direct matter/source force from X_Q, q_X cannot be treated as local-GR silent without epsilon_source_XQ.",
            "Move to 3803 qX same-source/no-extra-force closure or epsilon_source_XQ bound.",
        ),
    ]
    rows = []
    for decision_id, decision, rationale, action in specs:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "decision_id": decision_id,
                "decision": decision,
                "rationale": rationale,
                "action": action,
                "valid_for_claim": "false",
            }
        )
    return rows


def next_target_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "target_doc": "3803-Y5-R2FR-qX-same-source-no-extra-force-closure-or-epsilon-sourceXQ-bound.md",
            "target_script": "scripts/Y5_R2FR_3803_qX_same_source_no_extra_force_closure_or_epsilon_sourceXQ_bound.py",
            "objective": "Vary the Qspec/q_X parent clause against matter/source variables: prove X_Q enters only through B_Q inside one same-source Hilbert action, or emit epsilon_source_XQ and companion PPN/WEP/R10/clock/orbital bound rows.",
            "avoid": "do not claim q_X local-GR closure while X_Q can act as an independent matter/source force",
            "valid_for_claim": "false",
        }
    ]


def status_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "status": "PASS_NONCLAIM_PARENT_QSHEAR_ACTION_CLAUSE_WRITTEN",
            "headline": "A conditional parent Q-shear spectral action clause is written; strict current corpus still lacks signatures and source-safety proof.",
            "claim_allowed": "false",
            "next_target": "3803 qX same-source/no-extra-force closure or epsilon_source_XQ bound",
        }
    ]


def validation_rows(timestamp, grouped):
    sources_ok = all(row["exists"] == "true" for row in grouped["sources"])
    needles_ok = all(row["needle_found"] == "true" for row in grouped["sources"])
    csv_ok = all(csv_parses(path) for key, path in OUTPUTS.items() if key != "validation")
    theorem_text = "\n".join(row["mathematical_form"] for row in grouped["theorem"])
    contract_text = "\n".join(row["requirement"] for row in grouped["contract"])
    bound_nonclaim = all(row["valid_for_claim"] == "false" and row["blocks_claim"] == "true" for row in grouped["bound_rows"])
    gates_closed = all(row["claim_allowed"] == "false" for row in grouped["gates"])
    fwb_patterns = ("*Y5_R2FR_3802*", "*3802-Y5*", "*P8_Y5*3802*")
    fwb_hits = []
    if FWB.exists():
        for pattern in fwb_patterns:
            fwb_hits.extend(FWB.rglob(pattern))
    fwb_clean = not fwb_hits
    pycache_clean = not (PCW / "scripts" / "__pycache__").exists()
    checks = [
        ("sources_exist", sources_ok, "every cited source path exists"),
        ("needles_found", needles_ok, "every cited source needle was found"),
        ("csv_outputs_parse", csv_ok, "all generated CSV outputs exist and parse"),
        ("doc_written", DOC_PATH.exists(), "3802 markdown document written"),
        (
            "spectral_functor_present",
            "spectral projectors" in theorem_text and "functorial functions of S" in theorem_text,
            "spectral functional calculus owner theorem emitted",
        ),
        (
            "action_clause_present",
            "lambda_X.(X_Q-Spec(S[Q]))" in theorem_text and "lambda_Y.(Y_Q-Pi4(X_Q))" in theorem_text,
            "parent Qspec constraint action clause emitted",
        ),
        (
            "source_safety_present",
            "partial L_matter/partial X_Q=0" in theorem_text,
            "same-source/no-extra-XQ-force condition emitted",
        ),
        (
            "contract_complete",
            "q_X=(q_obs,X_Q)" in contract_text and "B_Q[Y_Q]" in contract_text,
            "qX/action/source contract clauses emitted",
        ),
        ("bound_rows_nonclaim", bound_nonclaim, "all epsilonYV/source leakage rows remain nonclaim blockers"),
        ("claims_closed", gates_closed, "no claim gate allows a claim"),
        ("formalization_clean", fwb_clean, "no 3802 files written under formalization-workbench"),
        ("pycache_removed", pycache_clean, "scripts __pycache__ removed"),
    ]
    rows = []
    for check_id, passed, detail in checks:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "check_id": check_id,
                "result": "PASS" if passed else "FAIL",
                "detail": detail,
            }
        )
    return rows


def row_bullet(row, key_fields):
    label = " ".join(f"`{row[field]}`" for field in key_fields if field in row and row[field])
    rest = "; ".join(
        f"{key}: {value}"
        for key, value in row.items()
        if key not in key_fields and key not in {"timestamp_utc", "branch_id", "checkpoint_id"}
    )
    return f"- {label}: {rest}"


def write_markdown(grouped):
    lines = [
        "# 3802 - Parent Q-shear Spectral Action Clause or epsilonYV Bound",
        "",
        "## Status",
        "",
        "`PASS_NONCLAIM_PARENT_QSHEAR_ACTION_CLAUSE_WRITTEN`.",
        "",
        "3802 writes the clean parent-extension route for the Q-shear branch. The important repair is that raw eigenframe angles are not treated as fundamental parent objects. If `S` is parent-owned, self-adjoint, tracefree, and nondegenerate on `U_reg`, then its eigenvalues and spectral projectors are functorial functions of `S`.",
        "",
        "A valid action clause can then constrain local chart variables by",
        "",
        "`L_Qspec=lambda_X.(X_Q-Spec(S[Q]))+lambda_Y.(Y_Q-Pi4(X_Q))+L_degen+L_domain`.",
        "",
        "This owns `X_Q` and `Y_Q` before EM readout only if `Pi4` is fixed by the parent action/symmetry and the same-source/no-extra-force/calibration checks survive.",
        "",
        "## Result In Plain Terms",
        "",
        "We now have a proper parent-action doorway, but it is not a current claim. If MTS adds or identifies this Q-shear spectral clause as parent data, the q_X route can close `Hperp`. If not, the finite branch is explicit: `epsilon_YV`, chart/degen leakage, and `epsilon_source_XQ` must be filled.",
        "",
        "Current verdict: action grammar yes; strict corpus signature no; claims remain closed.",
        "",
        "## Compact Result",
        "",
        "`S -> (s_a,P_a)` is functorial on nondegenerate `U_reg`; angle charts are local coordinates only.",
        "",
        "`Y_Q=Pi4(X_Q)` is parent-owned only if `Pi4` is fixed before EM readout and chart-covariant.",
        "",
        "`q_X` local closure still needs same-source EM stress, no independent X_Q force, q-star/Z_EM/current calibration, and degeneracy/atlas certificates.",
        "",
    ]
    sections = [
        ("Source Register", "sources", ["source_id"]),
        ("Parent Qshear Spectral Action Theorem", "theorem", ["theorem_id", "claim_piece"]),
        ("Parent Action Signature Contract", "contract", ["clause_id", "clause"]),
        ("Current Corpus Action Audit", "audit", ["audit_id", "item"]),
        ("epsilonYV Bound Fill Rows", "bound_rows", ["row_id", "symbol"]),
        ("Claim Gates", "gates", ["gate_id"]),
        ("Decisions", "decisions", ["decision_id"]),
        ("Next Target", "next_target", ["target_doc"]),
        ("Validation", "validation", ["check_id", "result"]),
    ]
    for title, key, key_fields in sections:
        lines.append(f"## {title}")
        for row in grouped[key]:
            lines.append(row_bullet(row, key_fields))
    DOC_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def cleanup_pycache():
    pycache = PCW / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main():
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    grouped = {
        "sources": source_register(timestamp),
        "theorem": theorem_rows(timestamp),
        "contract": contract_rows(timestamp),
        "audit": audit_rows(timestamp),
        "bound_rows": bound_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
    }
    grouped["gates"] = claim_gate_rows(timestamp, grouped)

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["theorem"], grouped["theorem"])
    write_csv(OUTPUTS["contract"], grouped["contract"])
    write_csv(OUTPUTS["audit"], grouped["audit"])
    write_csv(OUTPUTS["bound_rows"], grouped["bound_rows"])
    write_csv(OUTPUTS["gates"], grouped["gates"])
    write_csv(OUTPUTS["decisions"], grouped["decisions"])
    write_csv(OUTPUTS["next_target"], grouped["next_target"])
    write_csv(OUTPUTS["status"], grouped["status"])

    grouped["validation"] = [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "check_id": "pending",
            "result": "PASS",
            "detail": "placeholder before final validation",
        }
    ]
    write_markdown(grouped)
    cleanup_pycache()
    grouped["validation"] = validation_rows(timestamp, grouped)
    write_csv(OUTPUTS["validation"], grouped["validation"])
    write_markdown(grouped)
    cleanup_pycache()

    failed = [row for row in grouped["validation"] if row["result"] != "PASS"]
    print(grouped["status"][0]["status"])
    print(f"wrote {DOC_PATH}")
    if failed:
        raise SystemExit(f"validation failed: {failed}")


if __name__ == "__main__":
    main()
