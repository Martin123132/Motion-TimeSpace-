import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3793"
BRANCH = "MTS_R2FR_Y5_BQ_DESCENT_AMPLITUDE_OR_EPS_DBQ_BOUND_3793"
ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework"
    r"\Motion-TimeSpace--main"
)
PCW = ROOT / "post-checkpoint-work"
RESIDUALS = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3793-Y5-R2FR-BQ-descent-amplitude-or-eps-dBQ-bound.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3793_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_3793_BQ_DESCENT_AMPLITUDE_THEOREM.csv",
    "zero_conditions": RESIDUALS / "P8_Y5_R2FR_3793_LOCAL_ZERO_CONDITIONS.csv",
    "audit": RESIDUALS / "P8_Y5_R2FR_3793_CURRENT_CORPUS_BQ_DESCENT_AUDIT.csv",
    "components": RESIDUALS / "P8_Y5_R2FR_3793_EPS_BQ_DESCENT_COMPONENTS.csv",
    "ra_update": RESIDUALS / "P8_Y5_R2FR_3793_RA_DRA_REDUCTION_UPDATE.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_3793_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3793_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3793_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3793_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3793_VALIDATION.csv",
}

SOURCE_PATHS = [
    PCW / "3792-Y5-R2FR-same-current-Ward-Hilbert-stress-owner-or-epsilonJ-bound.md",
    PCW / "3791-Y5-R2FR-ZEM-fixed-normalization-or-betaZ-bound.md",
    PCW / "3790-Y5-R2FR-charge-unit-superselection-or-betaq-bound.md",
    PCW / "3789-Y5-R2FR-BQ-first-norm-and-patch-convention-or-field-map-fill.md",
    PCW / "3788-Y5-R2FR-BQ-first-coefficient-source-pack-RA-dRA.md",
    PCW / "3786-Y5-R2FR-parent-internal-multiplet-owner-or-BQ-finite-demotion.md",
    PCW / "3785-Y5-R2FR-derive-BQ-flow-one-form-from-vorticity-defects-or-demote-EM.md",
    PCW / "3784-Y5-R2FR-parent-U1-action-clause-or-EM-finite-bound-mode.md",
    PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md",
]


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    headers = sorted({key for row in rows for key in row})
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def source_register(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "checkpoint_id": CHECKPOINT,
            "branch_id": BRANCH,
            "source_path": str(path),
            "exists": path.exists(),
            "source_role": "BQ_descent_amplitude_RA_dRA_context",
            "valid_for_claim": False,
        }
        for path in SOURCE_PATHS
    ]


def theorem_rows(timestamp):
    rows = [
        {
            "theorem_id": "BDA3793_0_connection_decomposition",
            "claim_piece": "local B_Q descent split",
            "mathematical_form": "On U_good, write B_Q=q_obs^*Bbar_Q+dchi+B_perp, with H_Q=dB_Q=q_obs^*Hbar_Q+dB_perp. B_perp is the q_obs-vertical, non-gauge connection residue.",
            "derivation_status": "EXACT_LOCAL_DECOMPOSITION_DEFINITION",
            "zero_result_if_signed": "B_perp=0 makes B_Q a descended connection up to local gauge",
            "missing_for_current_claim": "parent-owned Bbar_Q/Y_Q/z and a proof that the current B_Q has no vertical residue",
        },
        {
            "theorem_id": "BDA3793_1_vertical_derivative_law",
            "claim_piece": "vertical residue law",
            "mathematical_form": "For E_A in ker(Dq_obs), Lie_EA B_Q=d(Lie_EA chi)+Lie_EA B_perp because Lie_EA q_obs^*Bbar_Q=0.",
            "derivation_status": "EXACT_FROM_DQOBS_EA_ZERO",
            "zero_result_if_signed": "only the exact gauge part remains when B_perp=0",
            "missing_for_current_claim": "explicit q_obs pullback connection and vertical-kernel proof for B_Q",
        },
        {
            "theorem_id": "BDA3793_2_RA_amplitude_definition",
            "claim_piece": "eps_BQ_descent_A",
            "mathematical_form": "eps_BQ_descent_A(E_A):=||q_*^-1 P_A Lie_EA B_perp||_A/A_ref, where P_A removes exact local gauge pieces on U_good.",
            "derivation_status": "EXACT_NORMALIZED_AMPLITUDE_DEFINITION",
            "zero_result_if_signed": "eps_BQ_descent_A=0 if B_Q descends modulo gauge and q_* is fixed",
            "missing_for_current_claim": "field-valued B_perp profile or parent theorem B_perp=0",
        },
        {
            "theorem_id": "BDA3793_3_dRA_amplitude_definition",
            "claim_piece": "eps_dBQ_A",
            "mathematical_form": "eps_dBQ_A(E_A):=||q_*^-1 Lie_EA dB_perp||_F/F_ref = ||q_*^-1 Lie_EA H_Q^perp||_F/F_ref.",
            "derivation_status": "EXACT_NORMALIZED_CURVATURE_AMPLITUDE_DEFINITION",
            "zero_result_if_signed": "eps_dBQ_A=0 if H_Q descends through q_obs",
            "missing_for_current_claim": "field-valued H_Q^perp profile or parent theorem H_Q=q_obs^*Hbar_Q",
        },
        {
            "theorem_id": "BDA3793_4_local_RA_DRA_reduction",
            "claim_piece": "R_A and dR_A reduction",
            "mathematical_form": "With U_good chart/Wilson silence and q_* superselection, RA_normed <= eps_BQ_descent_A and dRA_normed <= eps_dBQ_A.",
            "derivation_status": "EXACT_REDUCTION_FROM_3788_3789_3790",
            "zero_result_if_signed": "R_A=0 modulo gauge and dR_A=0 if both amplitudes vanish",
            "missing_for_current_claim": "signed q_* branch plus B_Q descent amplitudes zero or bounded",
        },
        {
            "theorem_id": "BDA3793_5_total_local_zero",
            "claim_piece": "local EM basicness from B_Q descent",
            "mathematical_form": "If B_Q=q_obs^*Bbar_Q+dchi, H1(U_good)=0, q_* is fixed, defects/Wilson data are outside or owned, and Z_EM/lambda are separately closed, then Lie_EA A_obs=dLambda_A and Lie_EA F_obs=0 locally.",
            "derivation_status": "EXACT_CONDITIONAL_ZERO_THEOREM",
            "zero_result_if_signed": "eps_BQ_descent_A=eps_dBQ_A=R_A=dR_A=0 on U_good",
            "missing_for_current_claim": "parent B_Q owner/descent and separate Z_EM/lambda closure",
        },
        {
            "theorem_id": "BDA3793_6_failure_mode",
            "claim_piece": "finite branch if descent fails",
            "mathematical_form": "If B_perp is not parent-zero, the finite local EM source residual is controlled by eps_BQ_descent_A, eps_dBQ_A, beta_Z,A, lambda_A, epsilon_J_Q, and domain/tail terms.",
            "derivation_status": "EXACT_BOUND_INTERFACE",
            "zero_result_if_signed": "no local EM/local-GR source claim until the finite vector is zeroed or arena-bounded",
            "missing_for_current_claim": "numeric field profiles/projection coefficients or parent zero theorem",
        },
    ]
    for row in rows:
        row["timestamp_utc"] = timestamp
        row["valid_for_claim"] = False
    return rows


def zero_condition_rows(timestamp):
    rows = [
        {
            "condition_id": "ZC3793_0_Ugood",
            "condition": "U_good is defect-free, contractible, compactly weighted, and uses the 3789 positive h_eff norm.",
            "role": "removes local Wilson/chart ambiguity from R_A and makes amplitudes scoreable",
            "current_status": "CONDITIONALLY_DEFINED_NOT_ARENA_SELECTED",
            "valid_for_claim": False,
        },
        {
            "condition_id": "ZC3793_1_qstar",
            "condition": "q_* is quotient-owned or compact charge-lattice superselected.",
            "role": "removes beta_q,A and d beta_q,A terms from 3788 response laws",
            "current_status": "EXACT_THEOREM_CONDITIONAL_CURRENT_CORPUS_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "condition_id": "ZC3793_2_pullback_BQ",
            "condition": "B_Q=q_obs^*Bbar_Q+dchi on U_good.",
            "role": "zeros eps_BQ_descent_A after local gauge projection",
            "current_status": "NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "condition_id": "ZC3793_3_pullback_HQ",
            "condition": "H_Q=dB_Q=q_obs^*Hbar_Q.",
            "role": "zeros eps_dBQ_A and therefore dR_A",
            "current_status": "NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "condition_id": "ZC3793_4_owner_constructor",
            "condition": "Bbar_Q is built from parent-owned two-pair Clebsch fields Y_Q=(C1,D1,C2,D2) or CP2/Berry multiplet z before EM readout.",
            "role": "prevents arbitrary one-form smuggling",
            "current_status": "CURRENT_MTS_SOURCE_OWNER_MISSING",
            "valid_for_claim": False,
        },
        {
            "condition_id": "ZC3793_5_ZEM_domain",
            "condition": "Z_EM/lambda, same-current, total-system domain, and tail/flux gates are closed or bounded.",
            "role": "prevents false local-GR claim from B_Q descent alone",
            "current_status": "PARTLY_DERIVED_THEOREM_SHAPES_UNSIGNED",
            "valid_for_claim": False,
        },
    ]
    for row in rows:
        row["timestamp_utc"] = timestamp
    return rows


def audit_rows(timestamp):
    rows = [
        {
            "audit_id": "BQA3793_0_3788",
            "source_signal": "3788 normalized the R_A/dR_A coefficients to 1 once residual norms are defined.",
            "current_result": "COEFFICIENTS_CLOSED_NOT_AMPLITUDES",
            "impact": "3793 no longer hunts coefficients; it defines the amplitudes themselves.",
            "valid_for_claim": False,
        },
        {
            "audit_id": "BQA3793_1_3789",
            "source_signal": "3789 defined U_good, A_ref/F_ref, and local chart/Wilson zero conditions.",
            "current_result": "LOCAL_PATCH_READY",
            "impact": "exact local gauge pieces can be removed; global defects remain explicit.",
            "valid_for_claim": False,
        },
        {
            "audit_id": "BQA3793_2_3790",
            "source_signal": "3790 conditionally zeroes q_* drift in the signed charge-lattice branch.",
            "current_result": "QSTAR_TERMS_REMOVABLE_CONDITIONALLY",
            "impact": "the strict remaining local A/F obstruction is B_Q descent if q_* branch is accepted.",
            "valid_for_claim": False,
        },
        {
            "audit_id": "BQA3793_3_3792",
            "source_signal": "3792 turns same-current into an exact theorem plus epsilon_J_Q vector.",
            "current_result": "CURRENT_MISMATCH_SEPARATED",
            "impact": "B_Q descent can be attacked without mixing it with Lorentz-force/source bookkeeping.",
            "valid_for_claim": False,
        },
        {
            "audit_id": "BQA3793_4_3785_3786",
            "source_signal": "3785/3786 give Darboux/Clebsch and Berry/internal-multiplet routes but current MTS sources do not own the two-pair/CP2 fields.",
            "current_result": "OWNER_STILL_HARD_BLOCKER",
            "impact": "B_perp cannot be declared zero from the current corpus; next work must build or source the owner.",
            "valid_for_claim": False,
        },
        {
            "audit_id": "BQA3793_5_verdict",
            "source_signal": "the local amplitude law is derivable; the actual amplitude value is not yet derived.",
            "current_result": "EXACT_AMPLITUDE_LAW_NONCLAIM",
            "impact": "the branch has moved from missing coupling to a precise zero-or-bound field profile problem.",
            "valid_for_claim": False,
        },
    ]
    for row in rows:
        row["timestamp_utc"] = timestamp
    return rows


def component_rows(timestamp):
    rows = [
        {
            "component_id": "EBQD3793_0_Bperp",
            "symbol": "B_perp",
            "definition": "non-gauge q_obs-vertical residue in B_Q=q_obs^*Bbar_Q+dchi+B_perp",
            "zero_if": "B_Q is a pullback connection modulo local gauge on U_good",
            "fallback_value": "MISSING_BQ_PULLBACK_PROFILE_OR_ZERO_THEOREM",
            "feeds": "eps_BQ_descent_A;eps_dBQ_A;R_A;dR_A",
            "status": "FIELD_RESIDUE_DEFINED_NOT_ZEROED",
            "valid_for_claim": False,
        },
        {
            "component_id": "EBQD3793_1_epsA",
            "symbol": "eps_BQ_descent_A",
            "definition": "||q_*^-1 P_A Lie_EA B_perp||_A/A_ref",
            "zero_if": "B_perp=0 or Lie_EA B_perp is exact local gauge",
            "fallback_value": "MISSING_EPS_BQ_DESCENT_A_VALUE",
            "feeds": "RA_normed;delta_A_S_EM;alpha_source",
            "status": "EXACT_DEFINITION_VALUE_MISSING",
            "valid_for_claim": False,
        },
        {
            "component_id": "EBQD3793_2_epsF",
            "symbol": "eps_dBQ_A",
            "definition": "||q_*^-1 Lie_EA dB_perp||_F/F_ref",
            "zero_if": "H_Q=dB_Q descends through q_obs",
            "fallback_value": "MISSING_EPS_DBQ_A_VALUE",
            "feeds": "dRA_normed;delta_A_S_EM;PPN;R10;clock",
            "status": "EXACT_DEFINITION_VALUE_MISSING",
            "valid_for_claim": False,
        },
        {
            "component_id": "EBQD3793_3_owner",
            "symbol": "eps_BQ_owner_map",
            "definition": "distance from current B_Q candidate to a parent-owned two-pair/CP2 constructor class before EM readout",
            "zero_if": "MTS owns Y_Q or z and B_Q is functorially built from it without A_obs/F_obs/Maxwell input",
            "fallback_value": "MISSING_PARENT_BQ_OWNER_CONSTRUCTOR",
            "feeds": "B_perp;eps_BQ_descent_A;eps_dBQ_A",
            "status": "HARD_BLOCKER",
            "valid_for_claim": False,
        },
        {
            "component_id": "EBQD3793_4_defect",
            "symbol": "eps_BQ_defect_Wilson",
            "definition": "nonlocal defect/Wilson residue outside contractible U_good or crossing source/support boundaries",
            "zero_if": "defect/Wilson data are q_obs-owned, outside the arena, or included as boundary data",
            "fallback_value": "MISSING_DEFECT_WILSON_SUPPORT_CERTIFICATE",
            "feeds": "R_A;dR_A;clock;R10;orbital",
            "status": "GLOBAL_PATCH_RESIDUAL",
            "valid_for_claim": False,
        },
        {
            "component_id": "EBQD3793_5_total",
            "symbol": "eps_BQ_descent_total_abs",
            "definition": "sum_abs(eps_BQ_descent_A,eps_dBQ_A,eps_BQ_owner_map,eps_BQ_defect_Wilson)",
            "zero_if": "pullback connection, pullback curvature, parent owner, and defect/Wilson support all close",
            "fallback_value": "MISSING_BQ_DESCENT_TOTAL_COMPONENT_VALUES",
            "feeds": "local_EM_basicness;local_GR_gate;PPN;WEP;R10;clock;orbital",
            "status": "FINITE_VECTOR_RETAINED",
            "valid_for_claim": False,
        },
    ]
    for row in rows:
        row["timestamp_utc"] = timestamp
    return rows


def ra_update_rows(timestamp):
    rows = [
        {
            "update_id": "RAD3793_0_full_law",
            "branch": "general_finite",
            "formula": "RA_normed <= eps_BQ_descent_A + eps_BQ_chart_A + eps_qA; dRA_normed <= eps_dBQ_A + eps_dchart_A + eps_betaqF + eps_dbetaqA",
            "conditions": "before accepting q_* and U_good simplifications",
            "impact": "keeps every old residual visible",
            "valid_for_claim": False,
        },
        {
            "update_id": "RAD3793_1_local_simplified",
            "branch": "U_good_plus_qstar",
            "formula": "RA_normed <= eps_BQ_descent_A; dRA_normed <= eps_dBQ_A",
            "conditions": "U_good chart/Wilson silence and parent-signed q_* superselection",
            "impact": "the remaining local EM readout obstruction is exactly B_Q descent amplitude",
            "valid_for_claim": False,
        },
        {
            "update_id": "RAD3793_2_zero_branch",
            "branch": "pullback_BQ",
            "formula": "B_Q=q_obs^*Bbar_Q+dchi and H_Q=q_obs^*Hbar_Q imply R_A=dLambda_A and dR_A=0 on U_good",
            "conditions": "parent-owned Bbar_Q plus fixed q_* and defect/Wilson support silence",
            "impact": "local A/F basicness follows without inserting a plateau axiom",
            "valid_for_claim": False,
        },
        {
            "update_id": "RAD3793_3_action_feed",
            "branch": "finite_action_bound",
            "formula": "|delta_A S_EM| <= C_Z |beta_Z,A| + C_dBQ eps_dBQ_A + C_J eps_BQ_descent_A + C_lambda |lambda_A| + C_JQ epsilon_J_Q",
            "conditions": "symbolic until coefficients and amplitude values are sourced or theorem-zero",
            "impact": "feeds alpha/source leakage, PPN, WEP, R10, clock, and orbital rows",
            "valid_for_claim": False,
        },
    ]
    for row in rows:
        row["timestamp_utc"] = timestamp
    return rows


def claim_gate_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3793_0_sources",
            "pass": True,
            "claim_allowed": False,
            "details": "all cited source paths resolve",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3793_1_amplitude_law",
            "pass": True,
            "claim_allowed": False,
            "details": "exact B_Q descent amplitude law emitted",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3793_2_local_reduction",
            "pass": True,
            "claim_allowed": False,
            "details": "U_good plus qstar branch reduces RA/dRA to eps_BQ_descent_A/eps_dBQ_A",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3793_3_parent_BQ_owner",
            "pass": False,
            "claim_allowed": False,
            "details": "current corpus has no parent-owned two-pair/CP2 B_Q constructor",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3793_4_zero_claim",
            "pass": False,
            "claim_allowed": False,
            "details": "eps_BQ_descent_A and eps_dBQ_A are defined, not proven zero or numerically bounded",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3793_5_local_GR_claim",
            "pass": False,
            "claim_allowed": False,
            "details": "no local-GR claim; B_Q owner, Z_EM/lambda, same-current, and total-domain gates remain open",
        },
    ]


def decision_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3793_0_real_progress",
            "decision": "The remaining B_Q problem is not a vague coupling gap; it is the amplitude of B_perp and dB_perp after exact local gauge/qstar reductions.",
            "action": "Use eps_BQ_descent_A and eps_dBQ_A as the official local EM descent targets.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3793_1_no_fake_zero",
            "decision": "A local chart can kill gauge/Wilson clutter, but it cannot invent a parent-owned B_Q.",
            "action": "Keep owner constructor as the next hard derivation target.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3793_2_next",
            "decision": "The next leap should be constructive: hunt for a parent-owned two-pair/CP2/Berry B_Q source from MTS flow/vorticity/node/Poynting primitives.",
            "action": "Build or reject the parent B_Q owner constructor rather than adding more audit rows.",
            "valid_for_claim": False,
        },
    ]


def next_target_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "target_file": "3794-Y5-R2FR-parent-BQ-owner-constructor-two-pair-CP2-or-finite-profile.md",
            "target_script": "scripts/Y5_R2FR_3794_parent_BQ_owner_constructor_two_pair_CP2_or_finite_profile.py",
            "objective": "Try to construct a non-circular parent-owned B_Q from MTS flow/vorticity/node/Poynting primitives using two-pair Clebsch or CP2/Berry geometry; if construction fails, emit the finite B_perp/H_perp profile acquisition contract.",
            "valid_for_claim": False,
        }
    ]


def status_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "checkpoint_id": CHECKPOINT,
            "branch_id": BRANCH,
            "status": "BQ_DESCENT_AMPLITUDE_LAW_DERIVED_VALUES_AND_OWNER_UNSIGNED",
            "plain_verdict": "3793 derives the exact local B_Q descent amplitude law. On U_good with q_* fixed, R_A and dR_A reduce to eps_BQ_descent_A and eps_dBQ_A. If B_Q is a q_obs pullback connection modulo gauge, both vanish locally; the current corpus does not yet own that B_Q, so the zero claim is blocked and the next target is the parent owner constructor.",
            "valid_for_claim": False,
        }
    ]


def validation_rows(timestamp, grouped):
    def csv_parses(path):
        if not path.exists():
            return False
        with path.open(encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True

    checks = [
        (
            "sources_exist",
            all(Path(row["source_path"]).exists() for row in grouped["sources"]),
            "every cited source path exists",
        ),
        (
            "csv_outputs_parse",
            all(csv_parses(path) for key, path in OUTPUTS.items() if key != "validation"),
            "all generated CSV outputs exist and parse",
        ),
        ("doc_written", DOC_PATH.exists(), "3793 markdown document written"),
        (
            "amplitude_law",
            any(row["theorem_id"] == "BDA3793_4_local_RA_DRA_reduction" for row in grouped["theorem"]),
            "RA/dRA amplitude reduction theorem emitted",
        ),
        (
            "component_definitions",
            all(
                any(row["symbol"] == symbol for row in grouped["components"])
                for symbol in ["B_perp", "eps_BQ_descent_A", "eps_dBQ_A", "eps_BQ_descent_total_abs"]
            ),
            "B_Q descent components emitted",
        ),
        (
            "zero_claim_closed",
            any(row["gate_id"] == "CG3793_4_zero_claim" and row["pass"] is False for row in grouped["claim_gates"]),
            "zero claim remains closed",
        ),
        (
            "local_gr_closed",
            any(row["gate_id"] == "CG3793_5_local_GR_claim" and row["pass"] is False for row in grouped["claim_gates"]),
            "local-GR claim remains closed",
        ),
        (
            "next_target",
            grouped["next_target"][0]["target_file"].startswith("3794-"),
            "3794 parent B_Q owner target emitted",
        ),
        (
            "formalization_clean",
            not any("formalization-workbench" in str(path) for path in OUTPUTS.values()),
            "no 3793 files written under formalization-workbench",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "checkpoint_id": CHECKPOINT,
            "branch_id": BRANCH,
            "validation_id": check_id,
            "result": "PASS" if ok else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
        }
        for check_id, ok, detail in checks
    ]


def render_section(title, rows, key_fields):
    lines = [f"## {title}"]
    for row in rows:
        head = " ".join(f"`{row[field]}`" for field in key_fields if field in row)
        details = []
        for key, value in row.items():
            if key in key_fields or key in {"timestamp_utc", "checkpoint_id", "branch_id", "valid_for_claim"}:
                continue
            details.append(f"{key}: {value}")
        lines.append(f"- {head}: " + "; ".join(details))
    lines.append("")
    return "\n".join(lines)


def render_doc(grouped):
    status = grouped["status"][0]
    text = [
        "# 3793 - B_Q Descent Amplitude or eps_dBQ Bound",
        "",
        "## Status",
        "",
        f"`{status['status']}`.",
        "",
        status["plain_verdict"],
        "",
        "## Result In Plain Terms",
        "",
        "3793 turns the `B_Q` throat into a clean local amplitude law. On the good local patch, after chart/Wilson clutter and charge-unit drift are removed, the only remaining local `A/F` obstruction is whether `B_Q` really descends through `q_obs` modulo gauge. If it does, `R_A` is gauge and `dR_A=0`. If it does not, the failure is exactly the field residue `B_perp` and its curvature `dB_perp`.",
        "",
        "This is a push forward: `RA_normed <= eps_BQ_descent_A` and `dRA_normed <= eps_dBQ_A` are no longer vague placeholders. They are normalized amplitudes of a precise non-descended connection residue. The reason this is still nonclaim is simple: the current corpus does not yet own the parent two-pair/CP2 `B_Q` constructor.",
        "",
        "## Compact Derivation",
        "",
        "`B_Q=q_obs^*Bbar_Q+dchi+B_perp` on `U_good`.",
        "",
        "For `E_A in ker(Dq_obs)`, `Lie_EA B_Q=d(Lie_EA chi)+Lie_EA B_perp`.",
        "",
        "`eps_BQ_descent_A=||q_*^-1 P_A Lie_EA B_perp||_A/A_ref`.",
        "",
        "`eps_dBQ_A=||q_*^-1 Lie_EA dB_perp||_F/F_ref`.",
        "",
        "With `U_good` and fixed `q_*`: `RA_normed <= eps_BQ_descent_A` and `dRA_normed <= eps_dBQ_A`.",
        "",
        render_section("B_Q Descent Amplitude Theorem", grouped["theorem"], ["theorem_id", "claim_piece"]),
        render_section("Local Zero Conditions", grouped["zero_conditions"], ["condition_id"]),
        render_section("Current Corpus B_Q Descent Audit", grouped["audit"], ["audit_id"]),
        render_section("eps_BQ Descent Components", grouped["components"], ["component_id", "symbol"]),
        render_section("R_A/dR_A Reduction Update", grouped["ra_update"], ["update_id", "branch"]),
        render_section("Claim Gates", grouped["claim_gates"], ["gate_id"]),
        render_section("Decisions", grouped["decisions"], ["decision_id"]),
        render_section("Next Target", grouped["next_target"], ["target_file"]),
        render_section("Validation", grouped["validation"], ["validation_id", "result"]),
    ]
    return "\n".join(text).rstrip() + "\n"


def main():
    timestamp = datetime.now(timezone.utc).isoformat()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    grouped = {
        "sources": source_register(timestamp),
        "theorem": theorem_rows(timestamp),
        "zero_conditions": zero_condition_rows(timestamp),
        "audit": audit_rows(timestamp),
        "components": component_rows(timestamp),
        "ra_update": ra_update_rows(timestamp),
        "claim_gates": claim_gate_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
        "validation": [],
    }

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["theorem"], grouped["theorem"])
    write_csv(OUTPUTS["zero_conditions"], grouped["zero_conditions"])
    write_csv(OUTPUTS["audit"], grouped["audit"])
    write_csv(OUTPUTS["components"], grouped["components"])
    write_csv(OUTPUTS["ra_update"], grouped["ra_update"])
    write_csv(OUTPUTS["claim_gates"], grouped["claim_gates"])
    write_csv(OUTPUTS["decisions"], grouped["decisions"])
    write_csv(OUTPUTS["next_target"], grouped["next_target"])
    write_csv(OUTPUTS["status"], grouped["status"])

    DOC_PATH.write_text(render_doc(grouped), encoding="utf-8")
    grouped["validation"] = validation_rows(timestamp, grouped)
    write_csv(OUTPUTS["validation"], grouped["validation"])
    DOC_PATH.write_text(render_doc(grouped), encoding="utf-8")

    cache = Path(__file__).resolve().parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    failures = [row for row in grouped["validation"] if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3793 validation failed: {failures}")
    print("wrote 3793 checkpoint: B_Q descent amplitude law emitted")


if __name__ == "__main__":
    main()
