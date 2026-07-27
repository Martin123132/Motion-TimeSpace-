import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3801"
BRANCH = "MTS_R2FR_Y5_QOBS_QSHEAR_SPECTRAL_OWNERSHIP_OR_SELECTOR_LEAKAGE_FILL_3801"
ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework"
    r"\Motion-TimeSpace--main"
)
PCW = ROOT / "post-checkpoint-work"
FWB = ROOT / "formalization-workbench"
RESIDUALS = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3801-Y5-R2FR-qobs-Qshear-spectral-ownership-or-selector-leakage-fill.md"

P_3765 = PCW / "3765-Y5-R2FR-construct-qobs-parent-quotient-or-frame-residual-map.md"
P_3766 = PCW / "3766-Y5-R2FR-prove-qobs-kernel-presymplectic-null-or-first-frame-residual-bound.md"
P_3792 = PCW / "3792-Y5-R2FR-same-current-Ward-Hilbert-stress-owner-or-epsilonJ-bound.md"
P_3796 = PCW / "3796-Y5-R2FR-Qshear-eigenframe-chart-or-first-Bperp-arena-fill.md"
P_3800 = PCW / "3800-Y5-R2FR-Clebsch-basicness-from-parent-Qshear-or-hU-bound-source.md"
P_SPINE = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

C_3800_BOUND = RESIDUALS / "P8_Y5_R2FR_3800_HU_SELECTOR_LEAKAGE_BOUND_ROWS.csv"
C_3800_GATE = RESIDUALS / "P8_Y5_R2FR_3800_SELECTOR_KERNEL_ALIGNMENT_GATE.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3801_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_3801_QOBS_QSHEAR_REFINEMENT_THEOREM.csv",
    "contract": RESIDUALS / "P8_Y5_R2FR_3801_QOBS_XQ_OWNERSHIP_CONTRACT.csv",
    "audit": RESIDUALS / "P8_Y5_R2FR_3801_CURRENT_CORPUS_QOBS_XQ_AUDIT.csv",
    "fill_rows": RESIDUALS / "P8_Y5_R2FR_3801_SELECTOR_LEAKAGE_FILL_ROWS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3801_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3801_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3801_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3801_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3801_VALIDATION.csv",
}

SOURCE_SPECS = [
    {
        "source_id": "SRC3801_0_3800_handoff",
        "path": P_3800,
        "needle": "dY_Q[V]=D Pi4_X.dX_Q[V]=0",
        "role": "3800 selected q_obs Q-shear ownership or selector leakage fill",
    },
    {
        "source_id": "SRC3801_1_3765_qobs_candidate",
        "path": P_3765,
        "needle": "q_obs_candidate",
        "role": "current observed quotient candidate",
    },
    {
        "source_id": "SRC3801_2_3766_kernel",
        "path": P_3766,
        "needle": "ker(Dq_obs)",
        "role": "vertical-kernel theorem and refinement context",
    },
    {
        "source_id": "SRC3801_3_3796_qshear",
        "path": P_3796,
        "needle": "S=R diag(s1,s2,-s1-s2) R^T",
        "role": "Q-shear spectral chart theorem",
    },
    {
        "source_id": "SRC3801_4_3792_same_current",
        "path": P_3792,
        "needle": "Assume S_src=S_charged[psi,g_obs,A_Q,theta]+S_EM",
        "role": "same-source/Hilbert stress recheck for any refined quotient",
    },
    {
        "source_id": "SRC3801_5_3800_bound_rows",
        "path": C_3800_BOUND,
        "needle": "HUB3800_0_epsilon_YV",
        "role": "selector leakage rows inherited from 3800",
    },
    {
        "source_id": "SRC3801_6_3800_selector_gate",
        "path": C_3800_GATE,
        "needle": "SKG3800_3_qobs_ownership_gate",
        "role": "q_obs ownership gate inherited from 3800",
    },
    {
        "source_id": "SRC3801_7_spine",
        "path": P_SPINE,
        "needle": "3801-Y5-R2FR-qobs-Qshear-spectral-ownership-or-selector-leakage-fill.md",
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
            "QXR3801_0_refined_quotient_map",
            "q_obs refinement map",
            "Define q_X(Phi)=(q_obs(Phi),X_Q(Phi)) with projection pi_X(q_X)=q_obs. Then ker(Dq_X)=ker(Dq_obs) cap ker(DX_Q).",
            "EXACT_DIFFERENTIAL_MAP_IDENTITY",
            "Vertical directions of the refined quotient cannot move X_Q.",
            "q_X must be parent-selected, not introduced after EM fitting",
        ),
        (
            "QXR3801_1_existing_readout_preservation",
            "old readouts survive refinement",
            "If an old sector readout r_s=F_s(q_obs), then r_s=(F_s o pi_X)(q_X). The same projection argument preserves any source term that already depended only on q_obs.",
            "EXACT_FACTORISATION_LEMMA",
            "Refinement does not break previously descended sectors by itself.",
            "new X_Q-dependent EM/source terms still need separate same-source checks",
        ),
        (
            "QXR3801_2_Hperp_zero_by_qX",
            "Hperp zero under q_X",
            "If X_Q is q_X-owned, Y_Q=Pi4(X_Q), Pi4 is parent-owned, and v in ker(Dq_X), then dY_Q(v)=D Pi4_X.DX_Q(v)=0; by 3800 and 3799, H_Q is q_X-basic.",
            "EXACT_CONDITIONAL_ZERO_THEOREM",
            "This closes Hperp relative to the refined quotient q_X.",
            "current corpus has not signed X_Q ownership, Pi4, or q_X as the physical quotient",
        ),
        (
            "QXR3801_3_not_free_lunch",
            "not original q_obs proof",
            "Refining q_obs to q_X does not prove H_Q was basic for the older quotient. It changes the vertical equivalence relation by declaring Q-shear spectral data physical or quotient-owned.",
            "NO_SMUGGLE_RULE",
            "A valid q_X route is allowed, but it is a parent quotient choice, not a retroactive cancellation.",
            "must recheck observed-frame, source, calibration, and no-extra-force clauses",
        ),
        (
            "QXR3801_4_source_frame_recheck",
            "same-source/frame recheck",
            "The refined quotient is safe only if X_Q enters through the parent EM/B_Q sector inside the same descended source action, does not create an independent matter/frame scalar force, and keeps q_*, Z_EM, and J_Q bookkeeping closed or bounded.",
            "REQUIRED_CONSISTENCY_GATE",
            "Prevents Q-shear ownership from becoming an unbounded extra field hidden inside local GR.",
            "same-current, Z_EM, q_*, and source-domain clauses remain unsigned",
        ),
        (
            "QXR3801_5_failure_to_selector_leakage",
            "finite leakage if q_X not signed",
            "If q_X ownership is not signed, keep the original q_obs verticals and use epsilon_YV=max_A||D Pi4_X.dX_Q(E_A)||/Y_ref, with h_U_response <= C_HY epsilon_YV + eta_chart + eta_degen.",
            "DERIVED_BOUND_BRANCH",
            "The finite route now has explicit selector-leakage inputs instead of an opaque h_U.",
            "epsilon_YV, C_HY, eta_chart, eta_degen, rho_VX, and theta_align remain missing",
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
            "QXC3801_0_parent_XQ",
            "parent X_Q construction",
            "X_Q=(s1,s2,alpha,beta,gamma) must be built from MTS Q/Qcoh/S/eigenframe data before EM readout.",
            "MISSING_PARENT_QSHEAR_SPECTRAL_OWNER",
            "prevents arbitrary EM variables being relabelled as Q-shear",
        ),
        (
            "QXC3801_1_smooth_atlas",
            "smooth spectral atlas",
            "Eigenframe angles and transitions must be smooth/covariant on U_reg, with repeated-eigenvalue support excluded or bounded.",
            "MISSING_QSHEAR_ATLAS_AND_DEGENERACY_CERTIFICATE",
            "keeps Pi4 from hiding discontinuous chart choices",
        ),
        (
            "QXC3801_2_parent_Pi4",
            "parent Pi4 selector",
            "Pi4:X_Q->Y_Q must be fixed by the parent action or symmetry before EM data/readout, with rank(DPi4)=4 where generic EM rank is claimed.",
            "MISSING_PARENT_PI4_SELECTOR",
            "keeps the four Clebsch scalars from being fitted post hoc",
        ),
        (
            "QXC3801_3_qX_selection",
            "q_X quotient selection",
            "q_X=(q_obs,X_Q) or q_Y=(q_obs,Y_Q) must be declared as the actual parent observed quotient/refinement, with projection back to the old q_obs.",
            "MISSING_QX_PARENT_QUOTIENT_SIGNATURE",
            "makes dY_Q[V]=0 legitimate rather than a kernel trick",
        ),
        (
            "QXC3801_4_readout_projection",
            "old readout projection",
            "All old sector readouts must factor through q_X by ignoring X_Q, or explicitly declare safe dependence on X_Q.",
            "MISSING_QX_READOUT_RECHECK",
            "prevents a new hidden preferred-frame/readout channel",
        ),
        (
            "QXC3801_5_same_source_EM",
            "same-source EM/source action",
            "The B_Q[X_Q] EM sector, charged current, EM Hilbert stress, binding/apparatus stress, and boundary terms must remain one descended source-action object.",
            "MISSING_QX_SAME_SOURCE_RECHECK",
            "prevents EM stress from becoming an unaccounted source leak",
        ),
        (
            "QXC3801_6_no_extra_scalar_force",
            "no independent X_Q matter force",
            "X_Q must not couple directly to matter/source normalization outside the accounted EM/Hilbert sector, unless that coupling is separately bounded.",
            "MISSING_NO_EXTRA_XQ_FORCE_CERTIFICATE",
            "prevents Q-shear ownership from acting like a fifth force",
        ),
        (
            "QXC3801_7_calibration_companions",
            "calibration companions",
            "q_*, Z_EM, lambda_A, epsilon_J_Q, boundary/domain, and clock/material markers must be zeroed or bounded under the same q_X branch.",
            "MISSING_QX_CALIBRATION_COMPANION_ROWS",
            "keeps alpha/R10/clock claims closed until the whole local EM coupling is calibrated",
        ),
    ]
    rows = []
    for clause_id, clause, requirement, current_status, reason in specs:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "clause_id": clause_id,
                "clause": clause,
                "requirement": requirement,
                "current_status": current_status,
                "reason": reason,
                "valid_for_claim": "false",
                "blocks_claim": "true",
            }
        )
    return rows


def audit_rows(timestamp):
    specs = [
        (
            "AUD3801_0_current_qobs",
            "current q_obs candidate",
            "3765 gives q_obs_candidate but it does not parent-sign Q-shear spectral ownership.",
            "PARTIAL_CONTEXT_ONLY",
            "MISSING_QOBS_QSHEAR_COMPONENT",
        ),
        (
            "AUD3801_1_kernel_theorem",
            "vertical kernel theorem",
            "3766 uses ker(Dq_obs), but does not prove ker(Dq_obs) subset ker(DX_Q).",
            "DOES_NOT_CLOSE_XQ",
            "MISSING_DXQ_KERNEL_NULL_PROOF",
        ),
        (
            "AUD3801_2_qshear_chart",
            "Q-shear spectral chart",
            "3796 gives conditional S=R diag(s1,s2,-s1-s2) R^T on U_reg.",
            "CONDITIONAL_ONLY",
            "MISSING_PARENT_ATLAS_AND_DEGEN_SUPPORT",
        ),
        (
            "AUD3801_3_Pi4",
            "Pi4 selector",
            "3800 requires D Pi4_X.dX_Q[V]=0, but no parent Pi4 exists in the current strict corpus.",
            "FAIL_CURRENT_ZERO_CLAIM",
            "MISSING_PARENT_PI4_SELECTOR",
        ),
        (
            "AUD3801_4_same_source",
            "same source recheck",
            "3792 supplies the contract for a same-current/Hilbert source, but q_X-specific EM/source ownership is not signed.",
            "REQUIRED_NOT_FILLED",
            "MISSING_QX_SAME_SOURCE_RECHECK",
        ),
        (
            "AUD3801_5_finite_fill",
            "selector leakage finite branch",
            "3800 bound rows exist, but epsilon_YV, rho_VX, theta_align, eta_chart, eta_degen, and C_HY have no numeric/source values.",
            "REQUIRED_NOT_FILLED",
            "MISSING_SELECTOR_LEAKAGE_VALUES",
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


def fill_rows(timestamp):
    specs = [
        (
            "SLF3801_0_qX_signature",
            "qX_parent_signature",
            "certificate that q_X=(q_obs,X_Q) or q_Y=(q_obs,Y_Q) is parent-selected before EM readout",
            "certificate",
            "MISSING_QX_PARENT_QUOTIENT_SIGNATURE",
        ),
        (
            "SLF3801_1_DXQ_kernel",
            "epsilon_XV",
            "max_A||DX_Q(E_A)||/X_ref for E_A in ker(Dq_obs)",
            "dimensionless",
            "MISSING_VERTICAL_QSHEAR_ACTION",
        ),
        (
            "SLF3801_2_epsilon_YV",
            "epsilon_YV",
            "max_A||D Pi4_X.DX_Q(E_A)||/Y_ref",
            "dimensionless",
            "MISSING_PARENT_PI4_AND_VERTICAL_QSHEAR_ACTION",
        ),
        (
            "SLF3801_3_rho_VX",
            "rho_VX",
            "rank span{DX_Q(E_A): E_A in ker(Dq_obs)}",
            "integer",
            "MISSING_VERTICAL_IMAGE_RANK",
        ),
        (
            "SLF3801_4_theta_align",
            "theta_align",
            "distance/angle from image(DX_Q[V]) to ker(D Pi4)",
            "dimensionless",
            "MISSING_SELECTOR_KERNEL_ALIGNMENT_MEASURE",
        ),
        (
            "SLF3801_5_eta_chart",
            "eta_chart_transition",
            "chart-transition leakage for Q-shear eigenframe angles",
            "dimensionless",
            "MISSING_QSHEAR_CHART_TRANSITION_CERTIFICATE",
        ),
        (
            "SLF3801_6_eta_degen",
            "eta_degen",
            "support/amplitude of repeated-eigenvalue or undefined-eigenframe regions",
            "dimensionless",
            "MISSING_DEGENERACY_SUPPORT_BOUND",
        ),
        (
            "SLF3801_7_C_HY",
            "C_HY",
            "operator norm from epsilon_YV to h_U_response",
            "dimensionless",
            "MISSING_HQ_PULLBACK_NORM_TRANSFER",
        ),
        (
            "SLF3801_8_epsilon_source_XQ",
            "epsilon_source_XQ",
            "non-EM source-action leakage from X_Q after q_X refinement",
            "dimensionless",
            "MISSING_NO_EXTRA_XQ_FORCE_CERTIFICATE",
        ),
        (
            "SLF3801_9_hU_bound",
            "h_U_response_bound",
            "h_U_response <= C_HY*epsilon_YV + eta_chart_transition + eta_degen",
            "dimensionless",
            "BOUND_FORM_READY_NUMERIC_INPUTS_MISSING",
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
            "CG3801_0_sources",
            sources_ok,
            False,
            "all source paths and needles found" if sources_ok else "one or more source paths/needles missing",
        ),
        (
            "CG3801_1_refinement_theorem",
            True,
            False,
            "q_X refinement theorem emitted",
        ),
        (
            "CG3801_2_current_qX_zero",
            False,
            False,
            "q_X is not parent-signed and current q_obs does not own Q-shear spectral data",
        ),
        (
            "CG3801_3_same_source_recheck",
            False,
            False,
            "same-source, no-extra-force, and calibration companion clauses are not closed",
        ),
        (
            "CG3801_4_selector_leakage_fill",
            True,
            False,
            "finite selector-leakage rows emitted but remain empty blockers",
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
            "DEC3801_0_progress",
            "The quotient route is now exact and policed.",
            "Refining to q_X makes dY_Q[V]=0 by kernel identity, but only if X_Q is a parent-selected quotient component before EM readout.",
            "Use q_X as a legitimate derivation route, not a retroactive cancellation.",
        ),
        (
            "DEC3801_1_current_nonclaim",
            "The current strict corpus still cannot claim Hperp zero.",
            "q_X, parent Pi4, Q-shear atlas/degeneracy, same-source recheck, and calibration companion rows are unsigned.",
            "Keep local-GR/R10/clock/PPN/orbital claims closed.",
        ),
        (
            "DEC3801_2_next",
            "The next target should try to source a parent Q-shear action/signature before giving up to numeric leakage.",
            "If an action clause owns X_Q/Pi4 and keeps same-source descent, q_X becomes real; otherwise epsilon_YV rows are the correct finite branch.",
            "Move to 3802 parent Q-shear spectral action clause or epsilon_YV bound fill.",
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
            "target_doc": "3802-Y5-R2FR-parent-Qshear-spectral-action-clause-or-epsilonYV-bound.md",
            "target_script": "scripts/Y5_R2FR_3802_parent_Qshear_spectral_action_clause_or_epsilonYV_bound.py",
            "objective": "Try to write a parent action/signature clause that owns X_Q/Pi4 before EM readout and preserves same-source descent; if that fails, fill epsilon_YV, epsilon_source_XQ, eta_chart, eta_degen, C_HY, and h_U bound rows as finite inputs.",
            "avoid": "do not treat quotient refinement as proof unless q_X is parent-selected and the same-source/no-extra-force checks pass",
            "valid_for_claim": "false",
        }
    ]


def status_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "status": "PASS_NONCLAIM_QOBS_QSHEAR_REFINEMENT_GATE",
            "headline": "q_X refinement would zero selector leakage by kernel identity, but current corpus has not parent-signed q_X or its source checks.",
            "claim_allowed": "false",
            "next_target": "3802 parent Q-shear spectral action clause or epsilon_YV bound",
        }
    ]


def validation_rows(timestamp, grouped):
    sources_ok = all(row["exists"] == "true" for row in grouped["sources"])
    needles_ok = all(row["needle_found"] == "true" for row in grouped["sources"])
    csv_ok = all(csv_parses(path) for key, path in OUTPUTS.items() if key != "validation")
    theorem_text = "\n".join(row["mathematical_form"] for row in grouped["theorem"])
    contract_text = "\n".join(row["clause"] + " " + row["requirement"] for row in grouped["contract"])
    fill_nonclaim = all(row["valid_for_claim"] == "false" and row["blocks_claim"] == "true" for row in grouped["fill_rows"])
    gates_closed = all(row["claim_allowed"] == "false" for row in grouped["gates"])
    fwb_patterns = ("*Y5_R2FR_3801*", "*3801-Y5*", "*P8_Y5*3801*")
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
        ("doc_written", DOC_PATH.exists(), "3801 markdown document written"),
        (
            "refinement_kernel_identity_present",
            "ker(Dq_X)=ker(Dq_obs) cap ker(DX_Q)" in theorem_text,
            "q_X kernel identity emitted",
        ),
        (
            "dY_zero_present",
            "dY_Q(v)=D Pi4_X.DX_Q(v)=0" in theorem_text,
            "q_X zero theorem for selector leakage emitted",
        ),
        (
            "no_free_lunch_present",
            "does not prove H_Q was basic for the older quotient" in theorem_text,
            "refinement no-smuggle rule emitted",
        ),
        (
            "same_source_no_force_contract",
            "same-source" in contract_text and "no independent X_Q matter force" in contract_text,
            "same-source and no-extra-force clauses emitted",
        ),
        ("fill_rows_nonclaim", fill_nonclaim, "all selector-leakage fill rows remain nonclaim blockers"),
        ("claims_closed", gates_closed, "no claim gate allows a claim"),
        ("formalization_clean", fwb_clean, "no 3801 files written under formalization-workbench"),
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
        "# 3801 - q_obs Q-shear Spectral Ownership or Selector Leakage Fill",
        "",
        "## Status",
        "",
        "`PASS_NONCLAIM_QOBS_QSHEAR_REFINEMENT_GATE`.",
        "",
        "3801 proves the exact quotient-refinement route. If the real parent observed quotient is refined to `q_X=(q_obs,X_Q)`, then",
        "",
        "`ker(Dq_X)=ker(Dq_obs) cap ker(DX_Q)`.",
        "",
        "So any vertical direction of `q_X` automatically has `DX_Q(v)=0`, and if `Y_Q=Pi4(X_Q)`, then `dY_Q(v)=0`. This closes the 3800 selector-kernel obstruction relative to `q_X`.",
        "",
        "But this is not a free pass. Refining the quotient changes the equivalence relation. It is legitimate only if `X_Q` is parent-owned before EM readout and the source/frame/calibration checks survive.",
        "",
        "## Result In Plain Terms",
        "",
        "This gives us a real fork. Either Q-shear spectral data are part of the parent observed quotient, in which case the vertical leakage dies cleanly by definition, or they are not, in which case we stop pretending and fill `epsilon_YV` and companion leakage rows.",
        "",
        "Current verdict: exact refinement theorem yes; current zero claim no; selector-leakage fill rows are ready.",
        "",
        "## Compact Result",
        "",
        "`q_X=(q_obs,X_Q)` makes `dX_Q[V_X]=0` for `V_X=ker(Dq_X)`.",
        "",
        "`Y_Q=Pi4(X_Q)` then gives `dY_Q[V_X]=0`, hence `H_Q` is basic in the 3800/3799 sense.",
        "",
        "This is claimable only after parent `X_Q/Pi4` ownership, same-source EM stress, no-extra-force, and calibration companion gates are signed.",
        "",
    ]
    sections = [
        ("Source Register", "sources", ["source_id"]),
        ("q_obs Qshear Refinement Theorem", "theorem", ["theorem_id", "claim_piece"]),
        ("qobs XQ Ownership Contract", "contract", ["clause_id", "clause"]),
        ("Current Corpus qobs XQ Audit", "audit", ["audit_id", "item"]),
        ("Selector Leakage Fill Rows", "fill_rows", ["row_id", "symbol"]),
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
        "fill_rows": fill_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
    }
    grouped["gates"] = claim_gate_rows(timestamp, grouped)

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["theorem"], grouped["theorem"])
    write_csv(OUTPUTS["contract"], grouped["contract"])
    write_csv(OUTPUTS["audit"], grouped["audit"])
    write_csv(OUTPUTS["fill_rows"], grouped["fill_rows"])
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
