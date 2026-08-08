import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3799"
BRANCH = "MTS_R2FR_Y5_HPERP_CURVATURE_DESCENT_ZERO_OR_FIRST_HU_SOURCE_ROW_3799"
ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework"
    r"\Motion-TimeSpace--main"
)
PCW = ROOT / "post-checkpoint-work"
FWB = ROOT / "formalization-workbench"
RESIDUALS = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3799-Y5-R2FR-Hperp-curvature-descent-zero-or-first-hU-source-row.md"

P_3789 = PCW / "3789-Y5-R2FR-BQ-first-norm-and-patch-convention-or-field-map-fill.md"
P_3793 = PCW / "3793-Y5-R2FR-BQ-descent-amplitude-or-eps-dBQ-bound.md"
P_3794 = PCW / "3794-Y5-R2FR-parent-BQ-owner-constructor-two-pair-CP2-or-finite-profile.md"
P_3796 = PCW / "3796-Y5-R2FR-Qshear-eigenframe-chart-or-first-Bperp-arena-fill.md"
P_3797 = PCW / "3797-Y5-R2FR-first-Bperp-Hperp-profile-source-acquisition-R10-clock.md"
P_3798 = PCW / "3798-Y5-R2FR-minimal-Bperp-Hperp-profile-ansatz-or-parent-zero.md"
P_SPINE = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

C_3797_R10 = RESIDUALS / "P8_Y5_R2FR_3797_R10_BOUND_JOIN_LEDGER.csv"
C_3797_CLOCK = RESIDUALS / "P8_Y5_R2FR_3797_CLOCK_JOIN_LEDGER.csv"
C_3798_BOUND = RESIDUALS / "P8_Y5_R2FR_3798_BPERP_FROM_HPERP_BOUND_ROWS.csv"
C_3798_JOIN = RESIDUALS / "P8_Y5_R2FR_3798_R10_CLOCK_NUMERATOR_UPDATE.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3799_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_3799_HPERP_CURVATURE_DESCENT_THEOREM.csv",
    "audit": RESIDUALS / "P8_Y5_R2FR_3799_CURRENT_CORPUS_HPERP_AUDIT.csv",
    "hu_rows": RESIDUALS / "P8_Y5_R2FR_3799_FIRST_HU_SOURCE_ROWS.csv",
    "join_update": RESIDUALS / "P8_Y5_R2FR_3799_R10_CLOCK_JOIN_UPDATE.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3799_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3799_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3799_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3799_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3799_VALIDATION.csv",
}

SOURCE_SPECS = [
    {
        "source_id": "SRC3799_0_3798_handoff",
        "path": P_3798,
        "needle": "Hperp=0 follows if H_Q=dB_Q is q_obs-basic",
        "role": "3798 reduces Bperp to Hperp and selects curvature descent as next target",
    },
    {
        "source_id": "SRC3799_1_3794_clebsch",
        "path": P_3794,
        "needle": "H_Q=dC1 wedge dD1+dC2 wedge dD2",
        "role": "two-pair Clebsch curvature formula and descent test",
    },
    {
        "source_id": "SRC3799_2_3796_qshear",
        "path": P_3796,
        "needle": "rank(dY_Q)=4",
        "role": "Q-shear/eigenframe selector remains unsigned",
    },
    {
        "source_id": "SRC3799_3_3793_decomposition",
        "path": P_3793,
        "needle": "H_Q=dB_Q=q_obs^*Hbar_Q+dB_perp",
        "role": "exact Hperp and dBQ amplitude definitions",
    },
    {
        "source_id": "SRC3799_4_3789_Ugood",
        "path": P_3789,
        "needle": "H1(U)=0",
        "role": "local patch and Wilson/harmonic guard",
    },
    {
        "source_id": "SRC3799_5_3797_R10",
        "path": C_3797_R10,
        "needle": "R10J3797_0_bound_curve_candidate",
        "role": "R10 bound-side hook waiting for numerator",
    },
    {
        "source_id": "SRC3799_6_3797_clock",
        "path": C_3797_CLOCK,
        "needle": "CLKJ3797_0_best_clock_product",
        "role": "clock alpha hook waiting for numerator",
    },
    {
        "source_id": "SRC3799_7_3798_bound_rows",
        "path": C_3798_BOUND,
        "needle": "BHB3798_4_epsilon_Bperp_bound",
        "role": "Bperp-from-Hperp bound rows inherited from 3798",
    },
    {
        "source_id": "SRC3799_8_3798_join",
        "path": C_3798_JOIN,
        "needle": "JOIN3798_0_R10_alpha",
        "role": "R10/clock numerator update inherited from 3798",
    },
    {
        "source_id": "SRC3799_9_spine",
        "path": P_SPINE,
        "needle": "3799-Y5-R2FR-Hperp-curvature-descent-zero-or-first-hU-source-row.md",
        "role": "live spine handoff target",
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
            "HCD3799_0_target_identity",
            "Hperp curvature target",
            "Hperp := H_Q - q_obs^*Hbar_Q on U_good. A local zero follows if H_Q is a q_obs-basic closed two-form and defect/Wilson/boundary sectors are silent.",
            "EXACT_TARGET_REDUCTION",
            "If signed, Hperp=0 and 3798 then gives Bperp=0 after gauge projection.",
            "current corpus has not parent-signed H_Q basicness or boundary silence",
        ),
        (
            "HCD3799_1_basicness_criterion",
            "closed two-form basicness criterion",
            "For V=ker(Dq_obs), a closed two-form H_Q descends locally as H_Q=q_obs^*Hbar_Q if i_v H_Q=0 for every vertical v. Since dH_Q=0, Lie_v H_Q=d(i_v H_Q)+i_v dH_Q=0 once horizontality holds.",
            "MATHEMATICAL_LOCAL_THEOREM",
            "H_Q=q_obs^*Hbar_Q exists on a regular quotient patch.",
            "requires regular q_obs patch and parent proof of horizontal curvature",
        ),
        (
            "HCD3799_2_clebsch_contraction_law",
            "two-pair Clebsch vertical contraction",
            "For H_Q=sum_i dC_i wedge dD_i, i_v H_Q=sum_i[(v C_i)dD_i-(v D_i)dC_i].",
            "EXACT_DIFFERENTIAL_FORM_CALCULATION",
            "The Hperp problem becomes a vertical-derivative problem for the parent Clebsch scalars.",
            "current Q-shear route has not sourced vC_i and vD_i",
        ),
        (
            "HCD3799_3_scalar_basicness_zero",
            "sufficient Clebsch scalar zero",
            "If vC_i=0 and vD_i=0 for every vertical v and both Clebsch pairs, then i_v H_Q=0 and H_Q descends through q_obs.",
            "EXACT_SUFFICIENT_ZERO_THEOREM",
            "This would close Hperp without fitting a finite profile.",
            "must derive Clebsch scalar basicness from parent Q/shear data, not assert it",
        ),
        (
            "HCD3799_4_selector_pushforward_gate",
            "Q-shear selector vertical derivative gate",
            "If Y_Q=Pi4(s1,s2,alpha,beta,gamma), then vY_Q=D(Pi4).v(s1,s2,alpha,beta,gamma) plus chart transition terms.",
            "EXACT_CHAIN_RULE_GATE",
            "A parent-owned Pi4 with D(Pi4).vQ_shear=0 would prove scalar basicness.",
            "Pi4, eigenframe atlas, degeneracy handling, and projector ownership remain unsigned",
        ),
        (
            "HCD3799_5_no_unprotected_cancellation",
            "cancellation guard",
            "The weaker condition sum_i[(v C_i)dD_i-(v D_i)dC_i]=0 is allowed only if the parent action or symmetry forces it.",
            "NO_SMUGGLE_RULE",
            "Prevents a hand-chosen cancellation from being mistaken for a derived EM descent.",
            "no parent symplectic/isotropic-fibre cancellation source is present",
        ),
        (
            "HCD3799_6_hU_fallback_definition",
            "first finite curvature amplitude",
            "If H_Q basicness is not signed, define h_U_profile=||P_F Hperp||_F/F_ref and h_U_response=max_A||q_star^-1 Lie_EA Hperp||_F/F_ref.",
            "DERIVED_FALLBACK_DEFINITION",
            "h_U becomes the first shared finite numerator for R10, clock, PPN, and orbital tests.",
            "numeric h_U profile or parent zero theorem is still missing",
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


def audit_rows(timestamp):
    specs = [
        (
            "HCA3799_0_qobs_patch",
            "regular q_obs patch",
            "q_obs must be a regular local quotient with V=ker(Dq_obs) and U_good outside defect support.",
            "U_good/H1(U)=0 exists as a patch convention; full q_obs regularity remains conditional.",
            "PARTIAL_CONDITIONAL",
            "MISSING_ARENA_QOBS_REGULAR_PATCH",
            "basicness theorem cannot be promoted to arena claim",
        ),
        (
            "HCA3799_1_HQ_formula",
            "parent H_Q formula",
            "H_Q must be a parent-owned closed two-form before EM readout.",
            "3794 supplies conditional H_Q=dC1 wedge dD1+dC2 wedge dD2 if Y_Q is parent-owned.",
            "EXACT_CONDITIONAL_FORMULA",
            "MISSING_PARENT_YQ_OWNERSHIP",
            "curvature formula is usable but not yet current-MTS-owned",
        ),
        (
            "HCA3799_2_clebsch_basicness",
            "Clebsch scalar q_obs-basicness",
            "Every C_i,D_i must be vertical-silent or have a parent-signed cancellation.",
            "No source yet proves Lie_EA C_i=Lie_EA D_i=0 for the Q-shear selector.",
            "FAIL_CURRENT_ZERO_CLAIM",
            "MISSING_LIE_EA_CLEBSCH_ZERO",
            "Hperp=0 is not claimed",
        ),
        (
            "HCA3799_3_qshear_selector",
            "Q-shear Pi4 selector",
            "Pi4 must be fixed by parent action, rank-four on U_good, transition-covariant, and no post-hoc EM readout.",
            "3796 shows the conditional chart but says Pi4/projector/eigenframe/degen support remain unsigned.",
            "FAIL_CURRENT_ZERO_CLAIM",
            "MISSING_PARENT_PI4_PROJECTOR_EIGENFRAME",
            "cannot infer vY_Q=0 from current corpus",
        ),
        (
            "HCA3799_4_boundary_harmonic",
            "boundary and harmonic silence",
            "Even with Hperp=0 locally, eta_boundary and eta_harmonic must vanish or be bounded.",
            "3798 names the leakages but does not source arena values.",
            "REQUIRED_NOT_FILLED",
            "MISSING_BOUNDARY_HARMONIC_CERTIFICATES",
            "3798 Bperp zero remains conditional",
        ),
        (
            "HCA3799_5_R10_clock_hooks",
            "R10/clock bound-side hooks",
            "R10 and clock tests need h_U plus transfer coefficients/projections, not only bounds.",
            "3797 has bound-side hooks; numerator and projection coefficients remain missing.",
            "BOUND_SIDE_READY_NUMERATOR_MISSING",
            "MISSING_HU_AND_TRANSFER_COEFFICIENTS",
            "test branches stay blocked/nonclaim",
        ),
    ]
    rows = []
    for audit_id, clause, requirement, current_evidence, status, missing, consequence in specs:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "audit_id": audit_id,
                "clause": clause,
                "requirement": requirement,
                "current_evidence": current_evidence,
                "status": status,
                "missing_for_claim": missing,
                "consequence": consequence,
                "valid_for_claim": "false",
            }
        )
    return rows


def hu_rows(timestamp):
    specs = [
        (
            "HU3799_0_hU_profile",
            "R10_lab;clock_lab;PPN_solar;orbital_source",
            "h_U_profile",
            "||P_F Hperp||_F/F_ref on selected U_good",
            "MISSING_PARENT_HPERP_ZERO_OR_NUMERIC_PROFILE",
            "dimensionless",
            "finite curvature profile amplitude",
        ),
        (
            "HU3799_1_hU_response",
            "R10_lab;clock_lab;PPN_solar;orbital_source",
            "h_U_response",
            "max_A ||q_star^-1 Lie_EA Hperp||_F/F_ref",
            "MISSING_VERTICAL_HPERP_RESPONSE_PROFILE",
            "dimensionless",
            "vertical response numerator used by eps_dBQ_A",
        ),
        (
            "HU3799_2_Lambda_U",
            "R10_lab;clock_lab",
            "Lambda_U",
            "C_U F_ref/A_ref for the chosen domain and norm",
            "MISSING_PATCH_POINCARE_CONSTANT_AND_REF_RATIO",
            "dimensionless",
            "turns h_U into the Bperp envelope from 3798",
        ),
        (
            "HU3799_3_eta_boundary",
            "R10_lab;clock_lab",
            "eta_boundary",
            "relative-boundary/support residue in Green primitive",
            "MISSING_BOUNDARY_SUPPORT_CERTIFICATE_OR_BOUND",
            "dimensionless",
            "prevents hidden boundary primitive",
        ),
        (
            "HU3799_4_eta_harmonic",
            "R10_lab;clock_lab",
            "eta_harmonic",
            "harmonic/Wilson residue if H1(U) or defect support is not silent",
            "MISSING_HARMONIC_WILSON_ZERO_OR_BOUND",
            "dimensionless",
            "keeps global cycles out of local zero claim",
        ),
        (
            "HU3799_5_C_R10_H",
            "R10_lab",
            "C_R10_H(lambda)",
            "arena transfer from h_U curvature amplitude into alpha_predicted(lambda)",
            "MISSING_R10_HPERP_TRANSFER_COEFFICIENT",
            "dimensionless",
            "needed to compare against alpha_bound(lambda)",
        ),
        (
            "HU3799_6_C_CLK_H",
            "clock_lab",
            "C_CLK_H",
            "clock transfer from h_U curvature amplitude into alpha-clock product",
            "MISSING_CLOCK_HPERP_TRANSFER_COEFFICIENT",
            "dimensionless",
            "needed to compare against clock product bound",
        ),
        (
            "HU3799_7_Ugood_arena_domain",
            "R10_lab;clock_lab",
            "U_good_domain",
            "actual local patch, support weight, metric/coframe, and defect exclusion certificate",
            "MISSING_ARENA_DOMAIN_DEFINITION",
            "domain_descriptor",
            "needed before any numerical h_U is meaningful",
        ),
    ]
    rows = []
    for row_id, arena, symbol, formula, current_value, units, role in specs:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "row_id": row_id,
                "arena": arena,
                "symbol": symbol,
                "formula": formula,
                "current_value": current_value,
                "units": units,
                "status": "REQUIRED_NOT_FILLED",
                "role": role,
                "valid_for_claim": "false",
                "blocks_claim": "true",
            }
        )
    return rows


def join_update_rows(timestamp):
    specs = [
        (
            "JOIN3799_0_R10_alpha_hU",
            "R10_lab",
            "alpha_predicted(lambda)",
            "alpha_predicted <= C_R10_H(lambda)*h_U_response + C_R10_B(lambda)*(Lambda_U*h_U_profile+eta_boundary+eta_harmonic) + C_R10_lambda*abs(lambda_A) + C_R10_J*epsilon_J_Q",
            "MISSING_HU_AND_R10_TRANSFER_COEFFICIENTS",
        ),
        (
            "JOIN3799_1_clock_alpha_hU",
            "clock_lab",
            "clock_alpha_product",
            "abs(DeltaK_alpha)*abs(tau_clock_time)*(C_CLK_H*h_U_response + C_CLK_B*(Lambda_U*h_U_profile+eta_boundary+eta_harmonic) + abs(beta_ZA) + abs(lambda_A) + epsilon_J_Q) <= clock_product_bound",
            "MISSING_HU_CLOCK_TRANSFER_AND_TAU_ROWS",
        ),
        (
            "JOIN3799_2_PPN_hU",
            "PPN_solar",
            "PPN_residual_envelope",
            "delta_PPN <= C_PPN_H*h_U_response + C_PPN_B*(Lambda_U*h_U_profile+eta_boundary+eta_harmonic) + C_PPN_src*epsilon_J_Q + C_PPN_Z*abs(beta_ZA)",
            "MISSING_PPN_HPERP_SOURCE_PROJECTION",
        ),
        (
            "JOIN3799_3_orbital_hU",
            "orbital_source",
            "delta_mu_extra_envelope",
            "delta_mu_extra <= C_mu_H*h_U_response + C_mu_B*(Lambda_U*h_U_profile+eta_boundary+eta_harmonic) + C_mu_src*epsilon_J_Q + C_mu_domain*epsilon_domain",
            "MISSING_ORBITAL_SOURCE_PROJECTION",
        ),
        (
            "JOIN3799_4_shared_hU_numerator",
            "R10_lab;clock_lab;PPN_solar;orbital_source",
            "N_H_local",
            "N_H_local := h_U_response + Lambda_U*h_U_profile + eta_boundary + eta_harmonic + abs(lambda_A) + abs(beta_ZA) + epsilon_J_Q",
            "MISSING_SHARED_NUMERATOR_VALUES",
        ),
    ]
    rows = []
    for row_id, arena, observable, formula, current_status in specs:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "row_id": row_id,
                "arena": arena,
                "observable": observable,
                "formula": formula,
                "current_status": current_status,
                "valid_for_claim": "false",
                "blocks_claim": "true",
            }
        )
    return rows


def claim_gate_rows(timestamp, grouped):
    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in grouped["sources"])
    specs = [
        (
            "CG3799_0_sources",
            sources_ok,
            False,
            "all cited source paths and needles found" if sources_ok else "one or more source paths/needles missing",
        ),
        (
            "CG3799_1_basicness_theorem",
            True,
            False,
            "exact closed-two-form basicness and Clebsch contraction theorem emitted",
        ),
        (
            "CG3799_2_current_Hperp_zero",
            False,
            False,
            "Hperp=0 is not parent-signed because Pi4/projector/eigenframe/Clebsch vertical silence remain unsigned",
        ),
        (
            "CG3799_3_hU_rows",
            True,
            False,
            "first h_U/Lambda_U/boundary/harmonic source rows emitted as required nonclaim inputs",
        ),
        (
            "CG3799_4_R10_clock_PPN_orbital",
            False,
            False,
            "all local arena claims remain blocked until h_U and transfer coefficients are real",
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
            "DEC3799_0_progress",
            "Hperp has been reduced to a basicness/vertical-contraction theorem.",
            "For closed H_Q, horizontality i_v H_Q=0 is enough to produce quotient descent on a regular patch.",
            "Use the contraction law as the next hard derivation target.",
        ),
        (
            "DEC3799_1_nonclaim",
            "No local-GR, R10, clock, PPN, or orbital claim follows from 3799.",
            "The strict corpus does not derive Clebsch scalar vertical silence, Pi4 ownership, boundary silence, or h_U values.",
            "Keep all arena rows nonclaim.",
        ),
        (
            "DEC3799_2_next",
            "The next route is Clebsch-basicness from parent Q-shear, not another broad missing-ledger pass.",
            "The exact formula now says what to prove: vC_i=vD_i=0, or parent-forced cancellation in i_v H_Q.",
            "Move to 3800 and try to derive the vertical generator action on Y_Q.",
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
            "target_doc": "3800-Y5-R2FR-Clebsch-basicness-from-parent-Qshear-or-hU-bound-source.md",
            "target_script": "scripts/Y5_R2FR_3800_Clebsch_basicness_from_parent_Qshear_or_hU_bound_source.py",
            "objective": "Try to derive vC_i=vD_i=0, or a parent-forced cancellation of i_v H_Q, from the Q-shear/Pi4 vertical generator; if not, source h_U/projection coefficients for R10 and clocks.",
            "avoid": "do not assert scalar basicness; do not use post-hoc EM readout to choose Pi4; do not promote local claims while h_U is missing",
            "valid_for_claim": "false",
        }
    ]


def status_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "status": "PASS_NONCLAIM_HPERP_REDUCED_TO_BASICNESS",
            "headline": "Hperp zero is exactly a q_obs-basic closed-curvature problem; current corpus does not yet sign it.",
            "claim_allowed": "false",
            "next_target": "3800 Clebsch basicness from parent Q-shear or h_U bound source",
        }
    ]


def validation_rows(timestamp, grouped):
    sources_ok = all(row["exists"] == "true" for row in grouped["sources"])
    needles_ok = all(row["needle_found"] == "true" for row in grouped["sources"])
    csv_ok = all(csv_parses(path) for key, path in OUTPUTS.items() if key != "validation")
    theorem_text = "\n".join(row["mathematical_form"] for row in grouped["theorem"])
    hu_nonclaim = all(row["valid_for_claim"] == "false" and row["blocks_claim"] == "true" for row in grouped["hu_rows"])
    gates_closed = all(row["claim_allowed"] == "false" for row in grouped["gates"])
    fwb_clean = not list(FWB.rglob("*3799*")) if FWB.exists() else True
    pycache_clean = not (PCW / "scripts" / "__pycache__").exists()
    checks = [
        ("sources_exist", sources_ok, "every cited source path exists"),
        ("needles_found", needles_ok, "every cited source needle was found"),
        ("csv_outputs_parse", csv_ok, "all generated CSV outputs exist and parse"),
        ("doc_written", DOC_PATH.exists(), "3799 markdown document written"),
        (
            "basicness_theorem_present",
            "i_v H_Q=0" in theorem_text and "H_Q=q_obs^*Hbar_Q" in theorem_text,
            "closed-two-form q_obs basicness theorem emitted",
        ),
        (
            "clebsch_contraction_present",
            "sum_i[(v C_i)dD_i-(v D_i)dC_i]" in theorem_text,
            "Clebsch vertical contraction formula emitted",
        ),
        (
            "current_zero_blocked",
            any(row["status"] == "FAIL_CURRENT_ZERO_CLAIM" for row in grouped["audit"]),
            "strict corpus failure is explicit",
        ),
        ("hu_rows_nonclaim", hu_nonclaim, "all h_U source rows are nonclaim blockers"),
        ("claims_closed", gates_closed, "no claim gate allows a claim"),
        ("formalization_clean", fwb_clean, "no 3799 files written under formalization-workbench"),
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
        "# 3799 - Hperp Curvature Descent Zero or First h_U Source Row",
        "",
        "## Status",
        "",
        "`PASS_NONCLAIM_HPERP_REDUCED_TO_BASICNESS`.",
        "",
        "3799 derives the exact local descent gate for `Hperp`: the problem is not a free profile if `H_Q` is a closed `q_obs`-basic two-form. For the two-pair Clebsch route, the hard test is now the vertical contraction law",
        "",
        "`i_v H_Q=sum_i[(v C_i)dD_i-(v D_i)dC_i]`.",
        "",
        "If the parent theory proves `vC_i=vD_i=0` for all vertical generators, or proves the contraction cancellation by symmetry, then `Hperp=0` and 3798 collapses `Bperp` as well. The current corpus does not yet prove that, so the first `h_U` source rows are emitted as nonclaim inputs.",
        "",
        "## Result In Plain Terms",
        "",
        "This is the cleanest version of the coupling throat so far: local EM leakage has been pushed down to whether the parent-owned curvature is horizontal along the invisible `q_obs` fibre. If the Clebsch scalars do not move when you move vertically in the unobserved fibre, the curvature descends and the local residue vanishes. If they do move, the size of that motion is the `h_U` numerator we must bound.",
        "",
        "Current verdict: exact theorem yes; current zero proof no; finite `h_U` source rows now exist but remain empty/nonclaim.",
        "",
        "## Compact Result",
        "",
        "`Hperp := H_Q-q_obs^*Hbar_Q`.",
        "",
        "`H_Q` descends locally if `i_v H_Q=0` for all `v in ker(Dq_obs)`; because `dH_Q=0`, this also gives `Lie_v H_Q=0`.",
        "",
        "For `H_Q=dC1 wedge dD1+dC2 wedge dD2`, the obstruction is `i_v H_Q=sum_i[(v C_i)dD_i-(v D_i)dC_i]`.",
        "",
    ]
    sections = [
        ("Source Register", "sources", ["source_id"]),
        ("Hperp Curvature Descent Theorem", "theorem", ["theorem_id", "claim_piece"]),
        ("Current Corpus Hperp Audit", "audit", ["audit_id", "clause"]),
        ("First h_U Source Rows", "hu_rows", ["row_id", "arena", "symbol"]),
        ("R10 Clock PPN Orbital Join Update", "join_update", ["row_id", "arena", "observable"]),
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
        "audit": audit_rows(timestamp),
        "hu_rows": hu_rows(timestamp),
        "join_update": join_update_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
    }
    grouped["gates"] = claim_gate_rows(timestamp, grouped)

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["theorem"], grouped["theorem"])
    write_csv(OUTPUTS["audit"], grouped["audit"])
    write_csv(OUTPUTS["hu_rows"], grouped["hu_rows"])
    write_csv(OUTPUTS["join_update"], grouped["join_update"])
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
