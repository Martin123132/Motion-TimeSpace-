import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3800"
BRANCH = "MTS_R2FR_Y5_CLEBSCH_BASICNESS_FROM_PARENT_QSHEAR_OR_HU_BOUND_SOURCE_3800"
ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework"
    r"\Motion-TimeSpace--main"
)
PCW = ROOT / "post-checkpoint-work"
FWB = ROOT / "formalization-workbench"
RESIDUALS = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3800-Y5-R2FR-Clebsch-basicness-from-parent-Qshear-or-hU-bound-source.md"

P_3765 = PCW / "3765-Y5-R2FR-construct-qobs-parent-quotient-or-frame-residual-map.md"
P_3766 = PCW / "3766-Y5-R2FR-prove-qobs-kernel-presymplectic-null-or-first-frame-residual-bound.md"
P_3794 = PCW / "3794-Y5-R2FR-parent-BQ-owner-constructor-two-pair-CP2-or-finite-profile.md"
P_3796 = PCW / "3796-Y5-R2FR-Qshear-eigenframe-chart-or-first-Bperp-arena-fill.md"
P_3798 = PCW / "3798-Y5-R2FR-minimal-Bperp-Hperp-profile-ansatz-or-parent-zero.md"
P_3799 = PCW / "3799-Y5-R2FR-Hperp-curvature-descent-zero-or-first-hU-source-row.md"
P_SPINE = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

C_3799_THEOREM = RESIDUALS / "P8_Y5_R2FR_3799_HPERP_CURVATURE_DESCENT_THEOREM.csv"
C_3799_HU = RESIDUALS / "P8_Y5_R2FR_3799_FIRST_HU_SOURCE_ROWS.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3800_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_3800_FULL_RANK_CLEBSCH_BASICNESS_THEOREM.csv",
    "selector_gate": RESIDUALS / "P8_Y5_R2FR_3800_SELECTOR_KERNEL_ALIGNMENT_GATE.csv",
    "audit": RESIDUALS / "P8_Y5_R2FR_3800_CURRENT_CORPUS_QSHEAR_BASICNESS_AUDIT.csv",
    "bound_rows": RESIDUALS / "P8_Y5_R2FR_3800_HU_SELECTOR_LEAKAGE_BOUND_ROWS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3800_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3800_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3800_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3800_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3800_VALIDATION.csv",
}

SOURCE_SPECS = [
    {
        "source_id": "SRC3800_0_3799_handoff",
        "path": P_3799,
        "needle": "i_v H_Q=sum_i[(v C_i)dD_i-(v D_i)dC_i]",
        "role": "3799 gives the vertical contraction target for Hperp",
    },
    {
        "source_id": "SRC3800_1_3794_clebsch_rank",
        "path": P_3794,
        "needle": "H_Q=dC1 wedge dD1+dC2 wedge dD2",
        "role": "two-pair Clebsch constructor and generic rank condition",
    },
    {
        "source_id": "SRC3800_2_3796_selector",
        "path": P_3796,
        "needle": "rank(dY_Q)=4",
        "role": "Q-shear selector full-rank condition",
    },
    {
        "source_id": "SRC3800_3_3798_hodge",
        "path": P_3798,
        "needle": "Bperp_norm_over_Aref <= Lambda_U*Hperp_norm_over_Fref",
        "role": "Hperp feeds Bperp through 3798 bound",
    },
    {
        "source_id": "SRC3800_4_3765_qobs",
        "path": P_3765,
        "needle": "q_obs_candidate",
        "role": "current q_obs candidate and quotient ownership guard",
    },
    {
        "source_id": "SRC3800_5_3766_kernel",
        "path": P_3766,
        "needle": "ker(Dq_obs)",
        "role": "vertical kernel/null theorem context",
    },
    {
        "source_id": "SRC3800_6_3799_theorem_csv",
        "path": C_3799_THEOREM,
        "needle": "HCD3799_2_clebsch_contraction_law",
        "role": "machine-readable 3799 contraction theorem",
    },
    {
        "source_id": "SRC3800_7_3799_hu_rows",
        "path": C_3799_HU,
        "needle": "HU3799_0_hU_profile",
        "role": "first h_U fallback source rows",
    },
    {
        "source_id": "SRC3800_8_spine",
        "path": P_SPINE,
        "needle": "3800-Y5-R2FR-Clebsch-basicness-from-parent-Qshear-or-hU-bound-source.md",
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
            "CBT3800_0_pullback_symplectic_form",
            "Clebsch curvature as pullback",
            "Let Y_Q=(C1,D1,C2,D2) and omega_0=dC1 wedge dD1+dC2 wedge dD2 on the four-dimensional Clebsch target. Then H_Q=Y_Q^*omega_0.",
            "EXACT_DIFFERENTIAL_FORM_IDENTITY",
            "The Hperp zero problem can be studied through dY_Q and the nondegenerate target symplectic form.",
            "current corpus still needs parent ownership of Y_Q",
        ),
        (
            "CBT3800_1_full_rank_no_cancellation",
            "rank-four cancellation rejection",
            "At any point where rank(dY_Q)=4, i_v H_Q=0 for a vertical v is equivalent to dY_Q(v)=0. Proof: i_v H_Q(w)=omega_0(dY_Q(v),dY_Q(w)); dY_Q is onto and omega_0 is nondegenerate, so only dY_Q(v)=0 can pair to zero against every dY_Q(w).",
            "EXACT_LOCAL_THEOREM",
            "In the generic Maxwell-rank branch, a hidden Clebsch cancellation cannot replace scalar basicness.",
            "strict current corpus has not proved dY_Q(v)=0",
        ),
        (
            "CBT3800_2_low_rank_exception",
            "rank-deficient exception",
            "If rank(dY_Q)<4, a nonzero dY_Q(v) can lie in the symplectic orthogonal of the image, so contraction cancellation is possible but the branch no longer owns generic local EM rank.",
            "EXACT_RANK_CASE_SPLIT",
            "A cancellation route is allowed only as a simple/degenerate sector, not as generic Maxwell closure.",
            "degeneracy support and sector status are not sourced",
        ),
        (
            "CBT3800_3_qshear_chain_rule",
            "Q-shear selector vertical derivative",
            "For X_Q=(s1,s2,alpha,beta,gamma) and Y_Q=Pi4(X_Q), dY_Q(v)=D Pi4_X . dX_Q(v).",
            "EXACT_CHAIN_RULE",
            "Clebsch basicness becomes the selector-kernel alignment condition D Pi4_X.dX_Q[V]=0.",
            "Pi4 and dX_Q on ker(Dq_obs) are not parent-sourced",
        ),
        (
            "CBT3800_4_selector_kernel_dimension",
            "rank-four Pi4 kernel law",
            "If dim X_Q=5 and rank(D Pi4)=4, then ker(D Pi4) is one-dimensional. Therefore every vertical Q-shear variation must lie in the same Pi4-null line to make Y_Q basic.",
            "EXACT_LINEAR_ALGEBRA_GATE",
            "A single unobserved/gauge shear direction could be harmless; two independent vertical shear directions generically force h_U nonzero.",
            "vertical image rank rho_VX is missing",
        ),
        (
            "CBT3800_5_qobs_ownership_route",
            "quotient ownership route",
            "If the parent quotient q_obs is extended or proved to already include Y_Q or the full Q-shear spectral class X_Q as pre-EM data, then dY_Q(v)=0 follows tautologically for v in ker(Dq_obs).",
            "VALID_PARENT_EXTENSION_ROUTE",
            "This can close Hperp, but only if source/current/frame descent is rechecked with the enlarged quotient.",
            "current q_obs candidate has not parent-signed Q-shear spectral ownership",
        ),
        (
            "CBT3800_6_hU_selector_bound",
            "finite selector-leakage numerator",
            "If D Pi4_X.dX_Q[V] is not zero, define epsilon_YV=max_A||D Pi4_X.dX_Q(E_A)||/Y_ref. Then h_U_response is bounded by C_HY epsilon_YV plus chart-transition and degeneracy leakage.",
            "DERIVED_BOUND_INTERFACE",
            "The finite branch can now source selector leakage instead of an opaque h_U.",
            "epsilon_YV, C_HY, eta_chart, and eta_degen are missing",
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


def selector_gate_rows(timestamp):
    specs = [
        (
            "SKG3800_0_full_rank_zero_gate",
            "generic rank-four branch",
            "rank(dY_Q)=4 and omega_0 nondegenerate",
            "Hperp_zero iff dY_Q[V]=0",
            "EXACT_EQUIVALENCE",
            "MISSING_DYQ_VERTICAL_ZERO_PROOF",
        ),
        (
            "SKG3800_1_chain_rule_gate",
            "Q-shear Pi4 branch",
            "Y_Q=Pi4(X_Q), X_Q=(s1,s2,alpha,beta,gamma)",
            "dY_Q[V]=D Pi4_X.dX_Q[V]",
            "EXACT_SELECTOR_FORM",
            "MISSING_PARENT_PI4_AND_DXQ_VERTICAL",
        ),
        (
            "SKG3800_2_kernel_alignment_gate",
            "five-to-four selector branch",
            "dim X_Q=5, rank(D Pi4)=4",
            "image(dX_Q[V]) subset ker(D Pi4), with dim ker(D Pi4)=1",
            "EXACT_LINEAR_ALIGNMENT_CONDITION",
            "MISSING_VERTICAL_IMAGE_RANK_AND_ALIGNMENT_ANGLE",
        ),
        (
            "SKG3800_3_qobs_ownership_gate",
            "quotient ownership branch",
            "Y_Q or X_Q is a parent-owned component/class of q_obs before EM readout",
            "dY_Q[V]=0 by quotient definition",
            "CONDITIONAL_EXTENSION_ROUTE",
            "MISSING_QOBS_QSHEAR_OWNERSHIP_AND_SOURCE_RECHECK",
        ),
        (
            "SKG3800_4_finite_bound_gate",
            "finite nonzero selector leakage branch",
            "epsilon_YV=max_A||D Pi4_X.dX_Q(E_A)||/Y_ref",
            "h_U_response <= C_HY epsilon_YV + eta_chart + eta_degen",
            "BOUND_READY_SYMBOLIC",
            "MISSING_EPSILON_YV_AND_TRANSFER_COEFFICIENTS",
        ),
    ]
    rows = []
    for gate_id, branch, assumptions, condition, status, missing in specs:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "gate_id": gate_id,
                "branch": branch,
                "assumptions": assumptions,
                "condition_or_bound": condition,
                "status": status,
                "missing_for_claim": missing,
                "valid_for_claim": "false",
            }
        )
    return rows


def audit_rows(timestamp):
    specs = [
        (
            "AUD3800_0_rank_dY",
            "rank(dY_Q)=4",
            "3796 gives this as a conditional selector requirement on U_reg.",
            "CONDITIONAL_THEOREM",
            "not a current signed parent fact",
            "MISSING_PARENT_PI4_AND_UREG_CERTIFICATE",
        ),
        (
            "AUD3800_1_Pi4",
            "parent Pi4 selector",
            "No source currently fixes Pi4 from the parent action before EM readout.",
            "FAIL_CURRENT_ZERO_CLAIM",
            "cannot evaluate D Pi4 or its kernel",
            "MISSING_PARENT_PI4_SELECTOR",
        ),
        (
            "AUD3800_2_DXQ_vertical",
            "vertical Q-shear variation dX_Q[V]",
            "No source currently gives Lie_EA(s1,s2,alpha,beta,gamma).",
            "FAIL_CURRENT_ZERO_CLAIM",
            "cannot prove D Pi4.dX_Q[V]=0",
            "MISSING_VERTICAL_QSHEAR_GENERATOR_ACTION",
        ),
        (
            "AUD3800_3_kernel_alignment",
            "selector-kernel alignment",
            "The exact condition is image(dX_Q[V]) subset ker(D Pi4), but neither image nor kernel is sourced.",
            "REQUIRED_NOT_FILLED",
            "cannot close Hperp zero",
            "MISSING_ALIGNMENT_ANGLE_OR_ZERO_THEOREM",
        ),
        (
            "AUD3800_4_qobs_spectral_ownership",
            "q_obs owns Q-shear spectral class",
            "Current q_obs candidate has observed frame/classes, but no signed clause that Y_Q or X_Q is quotient-owned pre-EM data.",
            "POSSIBLE_EXTENSION_NOT_CURRENT_DERIVATION",
            "tautological zero would require quotient/source recheck",
            "MISSING_QOBS_QSHEAR_EXTENSION_CONTRACT",
        ),
        (
            "AUD3800_5_degeneracy",
            "eigenframe degeneracy support",
            "Near isotropic/coherent local silence the eigenframe degenerates; 3796 already flagged this as unsigned.",
            "REQUIRED_NOT_FILLED",
            "rank-four branch may fail or need defect/domain split",
            "MISSING_DEGENERACY_SUPPORT_CERTIFICATE",
        ),
    ]
    rows = []
    for audit_id, requirement, current_evidence, status, consequence, missing in specs:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "audit_id": audit_id,
                "requirement": requirement,
                "current_evidence": current_evidence,
                "status": status,
                "consequence": consequence,
                "missing_for_claim": missing,
                "valid_for_claim": "false",
            }
        )
    return rows


def bound_rows(timestamp):
    specs = [
        (
            "HUB3800_0_epsilon_YV",
            "epsilon_YV",
            "max_A||D Pi4_X.dX_Q(E_A)||/Y_ref",
            "dimensionless",
            "MISSING_PARENT_PI4_AND_VERTICAL_QSHEAR_ACTION",
            "primary selector leakage replacing opaque h_U_response",
        ),
        (
            "HUB3800_1_C_HY",
            "C_HY",
            "operator norm from selector leakage epsilon_YV to h_U_response",
            "dimensionless",
            "MISSING_HQ_PULLBACK_NORM_TRANSFER",
            "turns vertical scalar leakage into curvature leakage",
        ),
        (
            "HUB3800_2_rho_VX",
            "rho_VX",
            "rank span{dX_Q(E_A): E_A in ker(Dq_obs)}",
            "integer",
            "MISSING_VERTICAL_IMAGE_RANK",
            "if rho_VX>1, one-dimensional Pi4 kernel cannot generically silence all vertical variations",
        ),
        (
            "HUB3800_3_theta_align",
            "theta_align",
            "angle/distance between image(dX_Q[V]) and ker(D Pi4)",
            "dimensionless",
            "MISSING_SELECTOR_KERNEL_ALIGNMENT_MEASURE",
            "quantifies nonzero h_U when exact zero fails",
        ),
        (
            "HUB3800_4_eta_chart",
            "eta_chart_transition",
            "chart transition residue for eigenframe/angle coordinates",
            "dimensionless",
            "MISSING_QSHEAR_CHART_TRANSITION_CERTIFICATE",
            "keeps local selector changes from being hidden",
        ),
        (
            "HUB3800_5_eta_degen",
            "eta_degen",
            "measure or amplitude of eigenvalue degeneracy/undefined eigenframe support",
            "dimensionless",
            "MISSING_DEGENERACY_SUPPORT_BOUND",
            "blocks rank-four selector claim near repeated eigenvalues",
        ),
        (
            "HUB3800_6_hU_bound",
            "h_U_response_bound",
            "h_U_response <= C_HY*epsilon_YV + eta_chart_transition + eta_degen",
            "dimensionless",
            "BOUND_FORM_READY_NUMERIC_INPUTS_MISSING",
            "derived replacement for opaque h_U_response",
        ),
        (
            "HUB3800_7_qobs_XQ",
            "qobs_XQ_ownership",
            "boolean/certificate that X_Q or Y_Q is parent-owned quotient data before EM readout",
            "certificate",
            "MISSING_QOBS_QSHEAR_OWNERSHIP_CERTIFICATE",
            "would zero epsilon_YV if paired with source/readout recheck",
        ),
    ]
    rows = []
    for row_id, symbol, formula, units, current_value, role in specs:
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
                "role": role,
                "valid_for_claim": "false",
                "blocks_claim": "true",
            }
        )
    return rows


def claim_gate_rows(timestamp, grouped):
    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in grouped["sources"])
    specs = [
        (
            "CG3800_0_sources",
            sources_ok,
            False,
            "all source paths and needles found" if sources_ok else "one or more source paths/needles missing",
        ),
        (
            "CG3800_1_full_rank_theorem",
            True,
            False,
            "full-rank Clebsch no-cancellation theorem emitted",
        ),
        (
            "CG3800_2_current_basicness_zero",
            False,
            False,
            "dY_Q[V]=0 is not parent-signed because Pi4 and vertical Q-shear action are missing",
        ),
        (
            "CG3800_3_qobs_extension",
            False,
            False,
            "q_obs spectral ownership remains a possible extension route, not current evidence",
        ),
        (
            "CG3800_4_hU_bound",
            True,
            False,
            "h_U is now bounded by selector leakage symbolically, but numeric inputs are missing",
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
            "DEC3800_0_progress",
            "The generic-rank Clebsch branch cannot hide behind a cancellation story.",
            "Because omega_0 is nondegenerate and dY_Q has rank four, i_v H_Q=0 forces dY_Q(v)=0.",
            "Treat scalar basicness/selector-kernel alignment as the real proof target.",
        ),
        (
            "DEC3800_1_current_nonclaim",
            "The strict current corpus still does not close Hperp.",
            "Pi4, dX_Q[V], q_obs spectral ownership, degeneracy support, and h_U transfer coefficients are not sourced.",
            "Keep local-GR/R10/clock/PPN/orbital claims closed.",
        ),
        (
            "DEC3800_2_next",
            "The next target should try the quotient route explicitly before numeric h_U sourcing.",
            "If q_obs can parent-own the Q-shear spectral class without circular EM readout, dY_Q[V]=0 follows; otherwise the finite branch has concrete selector-leakage rows to fill.",
            "Move to 3801 q_obs-Qshear spectral ownership or selector leakage source fill.",
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
            "target_doc": "3801-Y5-R2FR-qobs-Qshear-spectral-ownership-or-selector-leakage-fill.md",
            "target_script": "scripts/Y5_R2FR_3801_qobs_Qshear_spectral_ownership_or_selector_leakage_fill.py",
            "objective": "Try to prove X_Q or Y_Q is parent-owned q_obs data before EM readout, which zeroes dY_Q[V]; if not, fill epsilon_YV, rho_VX, theta_align, eta_chart, eta_degen, and C_HY source rows.",
            "avoid": "do not declare Q-shear quotient-owned just to close EM; recheck same-source/frame descent if q_obs is enlarged",
            "valid_for_claim": "false",
        }
    ]


def status_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "status": "PASS_NONCLAIM_FULL_RANK_CLEBSCH_BASICNESS_GATE",
            "headline": "Full-rank Clebsch cancellation collapses to dY_Q[V]=0; current corpus still lacks the selector-kernel proof.",
            "claim_allowed": "false",
            "next_target": "3801 q_obs Q-shear spectral ownership or selector leakage fill",
        }
    ]


def validation_rows(timestamp, grouped):
    sources_ok = all(row["exists"] == "true" for row in grouped["sources"])
    needles_ok = all(row["needle_found"] == "true" for row in grouped["sources"])
    csv_ok = all(csv_parses(path) for key, path in OUTPUTS.items() if key != "validation")
    theorem_text = "\n".join(row["mathematical_form"] for row in grouped["theorem"])
    selector_text = "\n".join(row["condition_or_bound"] for row in grouped["selector_gate"])
    bound_nonclaim = all(row["valid_for_claim"] == "false" and row["blocks_claim"] == "true" for row in grouped["bound_rows"])
    gates_closed = all(row["claim_allowed"] == "false" for row in grouped["gates"])
    fwb_patterns = ("*Y5_R2FR_3800*", "*3800-Y5*", "*P8_Y5*3800*")
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
        ("doc_written", DOC_PATH.exists(), "3800 markdown document written"),
        (
            "full_rank_theorem_present",
            "rank(dY_Q)=4" in theorem_text and "dY_Q(v)=0" in theorem_text,
            "full-rank Clebsch no-cancellation theorem emitted",
        ),
        (
            "selector_kernel_gate_present",
            "image(dX_Q[V]) subset ker(D Pi4)" in selector_text,
            "selector-kernel alignment gate emitted",
        ),
        (
            "hU_bound_present",
            any(row["symbol"] == "h_U_response_bound" for row in grouped["bound_rows"]),
            "h_U selector leakage bound row emitted",
        ),
        ("bound_rows_nonclaim", bound_nonclaim, "all selector-leakage source rows remain nonclaim blockers"),
        ("claims_closed", gates_closed, "no claim gate allows a claim"),
        ("formalization_clean", fwb_clean, "no 3800 files written under formalization-workbench"),
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
        "# 3800 - Clebsch Basicness from Parent Q-shear or h_U Bound Source",
        "",
        "## Status",
        "",
        "`PASS_NONCLAIM_FULL_RANK_CLEBSCH_BASICNESS_GATE`.",
        "",
        "3800 takes the 3799 obstruction seriously and sharpens it. In the generic rank-four Clebsch branch, a protected-looking cancellation does not save the zero proof: because the Clebsch target two-form is symplectic, `i_v H_Q=0` forces `dY_Q(v)=0` whenever `rank(dY_Q)=4`.",
        "",
        "So the next proof is not vague. It is the selector-kernel equation",
        "",
        "`dY_Q[V]=D Pi4_X.dX_Q[V]=0`.",
        "",
        "For a five-coordinate Q-shear chart and a rank-four `Pi4`, the kernel is one-dimensional. That means every vertical Q-shear variation must lie in the same `Pi4`-null direction, or the finite `h_U` numerator is nonzero.",
        "",
        "## Result In Plain Terms",
        "",
        "This is a good tightening. If the EM-like Clebsch curvature is genuinely full rank, we cannot wave away vertical leakage by saying the two pairs cancel. Either the parent quotient already owns the selected Q-shear variables, so they do not move vertically, or we must measure/bound exactly how much they move through `epsilon_YV`.",
        "",
        "Current verdict: exact theorem yes; current MTS zero proof no; the finite branch now has a concrete selector-leakage bound instead of opaque `h_U`.",
        "",
        "## Compact Result",
        "",
        "`H_Q=Y_Q^*omega_0`, with `Y_Q=(C1,D1,C2,D2)` and `omega_0=dC1 wedge dD1+dC2 wedge dD2`.",
        "",
        "If `rank(dY_Q)=4`, then `i_v H_Q=0` iff `dY_Q(v)=0`.",
        "",
        "If `Y_Q=Pi4(X_Q)`, then `dY_Q(v)=D Pi4_X.dX_Q(v)`, so the zero proof is exactly selector-kernel alignment.",
        "",
    ]
    sections = [
        ("Source Register", "sources", ["source_id"]),
        ("Full Rank Clebsch Basicness Theorem", "theorem", ["theorem_id", "claim_piece"]),
        ("Selector Kernel Alignment Gate", "selector_gate", ["gate_id", "branch"]),
        ("Current Corpus Qshear Basicness Audit", "audit", ["audit_id", "requirement"]),
        ("h_U Selector Leakage Bound Rows", "bound_rows", ["row_id", "symbol"]),
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
        "selector_gate": selector_gate_rows(timestamp),
        "audit": audit_rows(timestamp),
        "bound_rows": bound_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
    }
    grouped["gates"] = claim_gate_rows(timestamp, grouped)

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["theorem"], grouped["theorem"])
    write_csv(OUTPUTS["selector_gate"], grouped["selector_gate"])
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
