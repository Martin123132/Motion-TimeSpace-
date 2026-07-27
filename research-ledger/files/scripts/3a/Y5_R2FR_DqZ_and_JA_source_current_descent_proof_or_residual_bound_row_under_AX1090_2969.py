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
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_SOURCE = ROOT / "source-intake" / "beta-source" / "docs"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
WEP_SOURCES = ROOT / "source-intake" / "wep-sources"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2969"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2969-Y5-R2FR-DqZ-and-JA-source-current-descent-proof-or-residual-bound-row-under-AX1090.md"

SRC_2968_DOC = ROOT / "2968-Y5-R2FR-rank-zero-algebraic-residual-pack-or-source-silence-proof-under-AX1090.md"
SRC_2968_NEXT = RESIDUALS / "P8_Y5_R2FR_2968_NEXT_TARGET.csv"
SRC_2968_SILENCE = RESIDUALS / "P8_Y5_R2FR_2968_SOURCE_SILENCE_ATTEMPT.csv"
SRC_2968_TERMS = RESIDUALS / "P8_Y5_R2FR_2968_RANK_ZERO_TERM_STATUS.csv"
SRC_2968_ENVELOPE = RESIDUALS / "P8_Y5_R2FR_2968_RESIDUAL_ENVELOPE_ROWS_NONCLAIM.csv"
SRC_2968_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2968_VALIDATION.csv"

SRC_2213_RANK_ZERO = BETA_SOURCE / "PARENT_QLOC_RANK_ZERO_SOURCE_CURRENT_2213_NONCLAIM.csv"
SRC_2912_CONSTRAINT = PARENT_ACTION / "Constraint_first_Z_elimination_2912_NONCLAIM.csv"
SRC_2892_NEUTRAL = SOURCE_WEIGHT / "RAB_PARENT_ACTION_SOURCE_NEUTRALITY_SCHEMA_2892_NONCLAIM.csv"
SRC_2676_OWNER = WEP_SOURCES / "action_scale_measure_owner_wip_nonclaim_2676.csv"
SRC_2677_GRAMMAR = WEP_SOURCES / "no_species_action_weight_object_language_wip_2677.csv"
SRC_2914_COBS = PARENT_ACTION / "Cobs_no_shadow_head_audit_2914_NONCLAIM.csv"
SRC_2915_SHADOW = PARENT_ACTION / "Cshadow_zero_theorem_attempt_2915_NONCLAIM.csv"
SRC_2939_CTAU = PARENT_ACTION / "Ctau_residual_decomposition_2939_NONCLAIM.csv"
SRC_2800_RESPONSE = BETA_SOURCE / "RESPONSE_DOUBLET_QLOC_BOUND_2800_NONCLAIM.csv"
SRC_2699_VECTOR = LOCAL_BOUNDS / "GammaKhat_q_loc_official_residual_vector_2699_NONCLAIM.csv"
SRC_2733_BOUND = LOCAL_BOUNDS / "Khat_q_loc_residual_bound_2733_NONCLAIM.csv"
SRC_516_SPEC = RESIDUALS / "P8_QLOC_BOUND_RUNNER_SPEC.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2969_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_2969_COMBINED_DESCENT_THEOREM_LEDGER.csv",
    "dqz": RESIDUALS / "P8_Y5_R2FR_2969_DQZ_CLAUSE_AUDIT.csv",
    "ja": RESIDUALS / "P8_Y5_R2FR_2969_JA_SOURCE_CURRENT_AUDIT.csv",
    "readout": RESIDUALS / "P8_Y5_R2FR_2969_READOUT_SHADOW_CONSEQUENCE.csv",
    "bounds": RESIDUALS / "P8_Y5_R2FR_2969_DQZ_JA_RESIDUAL_BOUND_ROWS_NONCLAIM.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2969_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2969_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2969_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2969_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2969_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "descent_attempt_copy": PARENT_ACTION / "DqZ_JA_descent_theorem_attempt_2969_NONCLAIM.csv",
    "bound_rows_copy": LOCAL_BOUNDS / "DqZ_JA_residual_bound_rows_2969_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2969_parent_quotient_basic_matter_next_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv_rows(path)
        return True
    except Exception:
        return False


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": RUN_UTC,
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    selected = columns or list(rows[0].keys())
    header = "| " + " | ".join(selected) + " |"
    separator = "| " + " | ".join("---" for _ in selected) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in selected) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2969_00_2968_doc", SRC_2968_DOC, "Best live proof route;NEXT2968_0_2969", "2968 handoff"),
        ("SRC2969_01_2968_next", SRC_2968_NEXT, "NEXT2968_0_2969", "machine-readable 2969 target"),
        ("SRC2969_02_2968_silence", SRC_2968_SILENCE, "SS2968_0_DqZ_constraint;SS2968_1_JA_chain_rule;SS2968_7_verdict", "Dq_Z/J_A source silence selection"),
        ("SRC2969_03_2968_terms", SRC_2968_TERMS, "TERM2968_1_J_A;TERM2968_5_DqZ;TERM2968_7_total", "rank-zero term status"),
        ("SRC2969_04_2968_envelope", SRC_2968_ENVELOPE, "ENV2968_0_master;ENV2968_1_q_loc", "rank-zero residual envelope"),
        ("SRC2969_05_2968_validation", SRC_2968_VALIDATION, "VAL2968_OVERALL", "2968 validation"),
        ("SRC2969_06_2213_rank_zero", SRC_2213_RANK_ZERO, "RZS2213_1_chain_rule_zero_condition;RZS2213_2_rank_zero_silence_theorem;RZS2213_4_verdict", "rank-zero chain-rule theorem skeleton"),
        ("SRC2969_07_2912_constraint", SRC_2912_CONSTRAINT, "CFP2912_0_exact_conditional;CFP2912_2_second_class_route;CFP2912_5_current_verdict", "constraint-first Dq_Z theorem"),
        ("SRC2969_08_2892_neutral", SRC_2892_NEUTRAL, "PAS2892_1_quotient_action;PAS2892_2_no_pole_parent;PAS2892_5_result", "quotient-invariant matter/source action"),
        ("SRC2969_09_2676_owner", SRC_2676_OWNER, "OWN2676_2_hilbert_current_sublemma;OWN2676_4_verdict", "Hilbert current owner sublemma"),
        ("SRC2969_10_2677_grammar", SRC_2677_GRAMMAR, "GRM2677_3_species_blind_measure;GRM2677_4_source_label_forgetting;GRM2677_6_verdict", "species-blind action grammar"),
        ("SRC2969_11_2914_cobs", SRC_2914_COBS, "COBS2914_2_chain_zero_against_Z;COBS2914_4_matter_interface;COBS2914_5_verdict", "observed coframe consequence"),
        ("SRC2969_12_2915_shadow", SRC_2915_SHADOW, "ZTH2915_0_exact_conditional;ZTH2915_4_nonHilbert;ZTH2915_6_verdict", "shadow/no-Hilbert consequence"),
        ("SRC2969_13_2939_ctau", SRC_2939_CTAU, "CTA2939_5_C_matter_source;CTA2939_7_C_Dq;CTA2939_8_C_units", "tau/current/Dq residual decomposition"),
        ("SRC2969_14_2800_response", SRC_2800_RESPONSE, "RDT2800_3_source_current_zero;RDT2800_7_verdict", "source-current zero failed branch"),
        ("SRC2969_15_2699_vector", SRC_2699_VECTOR, "QLOC2699_3_euler_source;QLOC2699_5_projector;QLOC2699_7_total", "official q_loc residual channels"),
        ("SRC2969_16_2733_bound", SRC_2733_BOUND, "QB2733_0_vector_envelope;QB2733_2_observable_projection;QB2733_3_verdict", "bound interface"),
        ("SRC2969_17_516_spec", SRC_516_SPEC, "QB516_3_PPN_metric_tail;QB516_4_R11_operator", "arena projection gate"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_path, anchors, role in specs:
        found, missing = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_type": "local_file",
                    "source_path": str(source_path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": source_path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def theorem_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "THM2969_0_combined_descent",
            "combined Dq_Z/J_A descent theorem",
            "If q is parent-owned, v_Z is vertical with Dq[v_Z]=0, theta/dmu/Obs_e are q-basic, and S_matter descends to Sbar[q(Phi),Psi,theta(q)] with no direct Z/source slot, then Dq_Z=0 and J_A^bulk=delta_Z S_matter=0.",
            "EXACT_CONDITIONAL_THEOREM",
            "This is the cleanest derivation route: geometry descent and source-current silence are the same chain-rule statement.",
            "parent q;v_Z in ker(Dq);q-basic theta/dmu/Obs_e;quotient matter action;no direct Z/source prefactor",
            SRC_2213_RANK_ZERO,
        ),
        (
            "THM2969_1_boundary_separation",
            "bulk J_A only",
            "The theorem may zero the bulk/source-current component of J_A, but it does not zero B_A or CDB; those remain separate rank-zero forcing terms.",
            "SCOPE_GUARD_ACTIVE",
            "Prevents falsely treating source-current descent as a full local-GR proof.",
            "boundary no-flux and CDB closure excluded from 2969",
            SRC_2968_TERMS,
        ),
        (
            "THM2969_2_readout_consequence",
            "observed-map chain-zero consequence",
            "If Dq_Z=0 and Obs_e is q-basic, D_Z Obs_e=D Obs_e[Dq(v_Z)]=0; this suppresses the coframe/readout shadow component but only conditionally.",
            "CONDITIONAL_COROLLARY",
            "This helps the readout/projector residual but cannot be claimed without parent-unique observed coframe.",
            "Dq_Z theorem;terminal observed coframe;source/readout uniqueness",
            SRC_2914_COBS,
        ),
        (
            "THM2969_3_current_application",
            "current MTS application",
            "Current corpus does not parent-sign all combined descent premises in one branch.",
            "NOT_DERIVED_CURRENT_MTS",
            "Dq_Z and J_A stay as explicit nonclaim residual-bound rows.",
            "parent q signature;basic matter action;measure/coframe descent;source-current owner",
            SRC_2968_SILENCE,
        ),
    ]
    return [
        add_common(
            {
                "theorem_id": theorem_id,
                "target": target,
                "statement": statement,
                "current_status": status,
                "evidence_summary": summary,
                "required_premises": premises,
                "source_path": str(path),
                "source_path_exists": path.exists(),
                "theorem_zero_adopted": False,
                "accepted_for_scoring": False,
            }
        )
        for theorem_id, target, statement, status, summary, premises, path in rows
    ]


def dqz_clause_rows() -> list[dict[str, Any]]:
    rows = [
        ("DQZ2969_0_parent_q", "parent quotient map q(Phi)", "q is parent-owned before matter/readout", "MISSING_PARENT_Q_SIGNATURE", "not signed in 2912/2914", SRC_2912_CONSTRAINT),
        ("DQZ2969_1_vertical_generator", "v_Z in ker(Dq)", "Dq[v_Z]=0 by constraint/quotient verticality", "CONDITIONAL_NOT_PARENT_SIGNED", "requires parent constraint image and tangent proof", SRC_2912_CONSTRAINT),
        ("DQZ2969_2_constraint_first", "constraint-first elimination", "C_Z(Phi)=0 eliminates Z before q/matter/readout", "EXACT_CONDITIONAL_NOT_ADOPTED", "all premise rows must close in one parent branch", SRC_2912_CONSTRAINT),
        ("DQZ2969_3_q_factorization", "q|C_Z=qbar(Q_vis)", "visible quotient map does not retain Z representative labels", "MISSING_FACTORISATION_CERTIFICATE", "q_candidate and Q_vis constructor remain unsigned", SRC_2914_COBS),
        ("DQZ2969_4_theta_measure", "theta/dmu basicness", "theta and measure are functions of q or parent constants, not Z", "MISSING_BASICNESS_CERTIFICATE", "measure/coframe owner not parent-signed", SRC_2676_OWNER),
        ("DQZ2969_5_readout_shadow", "D_Z Obs_e consequence", "D_Z Obs_e=0 if Dq_Z=0 and Obs_e is q-basic", "CONDITIONAL_CHAIN_ZERO_ONLY", "observed coframe not parent-unique", SRC_2914_COBS),
        ("DQZ2969_6_verdict", "Dq_Z=0 current claim", "Dq_Z is theorem-zero in current MTS", "NOT_DERIVED_RESIDUAL_BOUND_ROW_REQUIRED", "parent q, verticality, factorization and readout descent do not all close", SRC_2968_TERMS),
    ]
    return [
        add_common(
            {
                "dqz_clause_id": clause_id,
                "clause": clause,
                "would_need": need,
                "current_status": status,
                "blocking_gap": blocker,
                "source_path": str(path),
                "source_path_exists": path.exists(),
                "theorem_zero_adopted": False,
                "fallback_bound_required": True,
            }
        )
        for clause_id, clause, need, status, blocker, path in rows
    ]


def ja_clause_rows() -> list[dict[str, Any]]:
    rows = [
        ("JA2969_0_quotient_action", "S_matter descends through q", "S_matter=Sbar[q(Phi),Psi,theta(q)]", "EXACT_CONDITIONAL_SCHEMA_NOT_PARENT_SIGNED", "action-domain/no-shadow exclusion is unsigned", SRC_2892_NEUTRAL),
        ("JA2969_1_no_direct_Z", "no direct Z/source prefactor", "no R/Z, partial Z, endpoint Z, J_Z Z, or source prefactor slot", "CONDITIONAL_NO_POLE_SCHEMA_ONLY", "could be closure unless parent grammar explains why Z is quotient/auxiliary", SRC_2892_NEUTRAL),
        ("JA2969_2_hilbert_current", "Hilbert source-current uniqueness", "same action varied before readout gives unique Hilbert current", "EXACT_SUBTHEOREM_CONDITIONAL", "common S_matter and variation order not parent-signed", SRC_2676_OWNER),
        ("JA2969_3_measure_grammar", "species-blind measure", "parent measure is functorial and species/source blind", "CONTRACT_TARGET_NOT_SIGNED", "species measure Jacobians and source weights remain countermodels", SRC_2677_GRAMMAR),
        ("JA2969_4_source_label_forgetting", "source/readout label forgetting", "source/readout functor forgets source species before normalization", "UNSIGNED_DEPENDENCY", "post-quotient spurion return not excluded", SRC_2677_GRAMMAR),
        ("JA2969_5_nonHilbert_bypass", "non-Hilbert current bypass", "no independent active source current survives improvement/boundary/readout tails", "NOT_DERIVED_RESIDUAL_ROW_RETAINED", "Cshadow keeps non-Hilbert current residual live", SRC_2915_SHADOW),
        ("JA2969_6_boundary_projector_scope", "boundary/projector separation", "J_A^bulk zero does not zero B_A or projector commutators", "SCOPE_GUARD_ACTIVE", "boundary/projector are separate residual channels", SRC_2699_VECTOR),
        ("JA2969_7_verdict", "J_A=0 current claim", "bulk source-current forcing is theorem-zero in current MTS", "NOT_DERIVED_RESIDUAL_BOUND_ROW_REQUIRED", "matter action descent, current owner, measure and no-spurion clauses do not all close", SRC_2968_TERMS),
    ]
    return [
        add_common(
            {
                "ja_clause_id": clause_id,
                "clause": clause,
                "would_need": need,
                "current_status": status,
                "blocking_gap": blocker,
                "source_path": str(path),
                "source_path_exists": path.exists(),
                "theorem_zero_adopted": False,
                "fallback_bound_required": True,
            }
        )
        for clause_id, clause, need, status, blocker, path in rows
    ]


def readout_rows() -> list[dict[str, Any]]:
    rows = [
        ("RO2969_0_C_Dq", "C_Dq", "Dq_Z=0 would remove quotient-map/current leakage into charge/source readout", "CONDITIONAL_ONLY", "CTA2939_7 says explicit q, Dq and observed-map descent are still unsigned", SRC_2939_CTAU),
        ("RO2969_1_Cobs", "D_Z Obs_e", "D_Z Obs_e=D Obs_e[Dq(v_Z)] vanishes if Dq[v_Z]=0", "CONDITIONAL_CHAIN_RULE_VALID", "COBS functor is not parent unique", SRC_2914_COBS),
        ("RO2969_2_Cshadow", "C_shadow_abs", "terminal public coframe plus no shadow slots would set shadow response to zero", "EXACT_CONDITIONAL_NOT_CURRENT", "component zero clauses do not close in one parent branch", SRC_2915_SHADOW),
        ("RO2969_3_C_matter_source", "C_matter_source", "same-action Hilbert current and source measure glue would suppress source readout drift", "SOURCE_GLUE_NOT_SIGNED", "current owner and measure/coframe descent missing", SRC_2939_CTAU),
        ("RO2969_4_arena", "Pi_arena consequence", "arena residuals inherit any Dq_Z/J_A bound only after projection operators are sourced", "MISSING_ARENA_OPERATOR", "PPN/R10/clock/orbital maps stay blocked", SRC_516_SPEC),
    ]
    return [
        add_common(
            {
                "readout_id": readout_id,
                "component": component,
                "conditional_consequence": consequence,
                "current_status": status,
                "blocking_gap": blocker,
                "source_path": str(path),
                "source_path_exists": path.exists(),
                "accepted_for_scoring": False,
            }
        )
        for readout_id, component, consequence, status, blocker, path in rows
    ]


def bound_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "BND2969_0_DqZ_norm",
            "Dq_Z_norm",
            "||Dq[v_Z]||",
            "||Dq[v_Z]|| <= eps_q_parent + eps_constraint + eps_factorization",
            "eps_q_parent;eps_constraint;eps_factorization;norm convention",
            SRC_2912_CONSTRAINT,
        ),
        (
            "BND2969_1_DqZ_readout",
            "DqZ_readout_shadow",
            "||D_Z Obs_e|| + C_shadow_abs",
            "DqZ_readout <= C_Obs ||Dq[v_Z]|| + C_shadow_abs",
            "C_Obs;C_shadow_abs;terminal observed coframe certificate",
            SRC_2914_COBS,
        ),
        (
            "BND2969_2_JA_bulk",
            "J_A_bulk",
            "|delta_Z S_matter|",
            "|J_A_bulk| <= C_matter||Dq[v_Z]|| + C_theta||Lie_v theta|| + C_mu||Lie_v dmu|| + |J_direct| + |J_nonH| + |J_spurion|",
            "C_matter;C_theta;C_mu;J_direct;J_nonH;J_spurion;units",
            SRC_2892_NEUTRAL,
        ),
        (
            "BND2969_3_current_owner_countermodels",
            "J_A_countermodel_tail",
            "|w_A|+|Jac_A|+|zeta_nonH|",
            "|J_A_countermodel_tail| <= K_w|w_A| + K_Jac|Jac_A| + K_nonH|zeta_nonH|",
            "species action weights;measure Jacobians;non-Hilbert current coefficients",
            SRC_2676_OWNER,
        ),
        (
            "BND2969_4_rank_zero_insert",
            "R_alg_DqZ_JA_insert",
            "partial rank-zero residual contribution",
            "|Z| <= ||M^-1|| (|J_A_bulk| + |J_A_countermodel_tail| + |B_A| + |CDB| + |R_A|)",
            "M_inv;J_A bounds;B_A;CDB;R_A;arena projections",
            SRC_2968_ENVELOPE,
        ),
        (
            "BND2969_5_q_loc_insert",
            "q_loc_DqZ_JA_insert",
            "local residual projection",
            "||q_loc|| <= K_Z |Z| + K_Dq DqZ_readout + retained DeltaK/boundary/projector terms",
            "K_Z;K_Dq;DeltaK;boundary;projector;arena maps",
            SRC_2733_BOUND,
        ),
    ]
    return [
        add_common(
            {
                "bound_id": bound_id,
                "quantity": quantity,
                "symbolic_norm": norm,
                "bound_form": bound_form,
                "missing_inputs": missing,
                "source_path": str(path),
                "source_path_exists": path.exists(),
                "numeric_bound_present": False,
                "source_backed_coefficients": False,
                "accepted_for_scoring": False,
                "no_cancellation_policy": True,
            }
        )
        for bound_id, quantity, norm, bound_form, missing, path in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2969_0_DqZ", "Dq_Z theorem-zero adopted", False, "Dq_Z_NOT_PARENT_SIGNED"),
        ("CG2969_1_JA", "J_A theorem-zero adopted", False, "J_A_NOT_PARENT_SIGNED"),
        ("CG2969_2_combined", "combined Dq_Z/J_A descent proof closes", False, "COMBINED_PREMISES_OPEN"),
        ("CG2969_3_bounds", "Dq_Z/J_A residual bounds source-backed numeric", False, "SYMBOLIC_BOUND_ROWS_ONLY"),
        ("CG2969_4_readout", "readout/shadow consequence adopted", False, "OBSERVED_FRAME_NOT_PARENT_UNIQUE"),
        ("CG2969_5_rank_zero", "rank-zero residual pack score-ready", False, "BOUNDARY_CDB_MAB_ARENA_STILL_OPEN"),
        ("CG2969_6_local_GR", "derived local GR/Newton reduction claimed", False, "NO_LOCAL_GR_OR_NEWTON_CLAIM"),
    ]
    return [
        add_common(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "condition_passed": passed,
                "status": status,
            }
        )
        for gate_id, claim, passed, status in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC2969_0_theorem_shape",
            "combined Dq_Z/J_A theorem shape is strong",
            "both zeros follow from the same parent q-basic chain rule if the action and readout descend",
            "keep this as the preferred derivation route",
        ),
        (
            "DEC2969_1_no_adoption",
            "do not adopt the zeros yet",
            "parent q, verticality, basic matter action, measure/coframe descent and current-owner clauses are not signed in one branch",
            "emit Dq_Z and J_A residual-bound rows",
        ),
        (
            "DEC2969_2_upstream_lock",
            "the upstream lock is object-language signature",
            "without a parent-owned quotient map and q-basic ordinary matter action, the proof remains a closure contract",
            "target parent quotient/basic-matter action signature next",
        ),
        (
            "DEC2969_3_claims",
            "no local-GR, R10, PPN, clock, WEP or orbital claim",
            "2969 only narrows two forcing channels and records fallback rows",
            "keep all outputs private nonclaim",
        ),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": action,
            }
        )
        for decision_id, decision, because, action in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2969_0_2970",
                "priority": "selected_primary",
                "next_doc": "2970-Y5-R2FR-parent-quotient-map-and-basic-matter-action-signature-or-DqZ-JA-coefficient-row-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_parent_quotient_map_and_basic_matter_action_signature_or_DqZ_JA_coefficient_row_under_AX1090_2970.py",
                "objective": "Try to parent-sign the quotient map q, the vertical generator v_Z in ker(Dq), and the q-basic ordinary matter action S_matter=Sbar[q(Phi),Psi,theta(q)]; if this fails, create first finite coefficient rows for eps_q_parent, eps_constraint, J_direct and J_spurion.",
                "include": "parent object language;q(Phi);v_Z;ker(Dq);constraint image;Q_vis constructor;theta/dmu basicness;ordinary matter domain;no direct Z/source prefactor;first residual coefficients",
                "exclude": "boundary no-flux proof;CDB closure;M_AB signature proof;arena scoring;R10 alpha claim;PPN claim;clock/orbital claim;local-GR claim;GitHub action;formalization-workbench edits",
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = [
        ("descent_attempt_copy", OUTPUTS["theorem"], BRANCH_OUTPUTS["descent_attempt_copy"]),
        ("bound_rows_copy", OUTPUTS["bounds"], BRANCH_OUTPUTS["bound_rows_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copies:
        shutil.copyfile(source, target)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source),
                    "copy_path": str(target),
                    "source_exists": source.exists(),
                    "copy_exists": target.exists(),
                }
            )
        )
    return rows


def validation_rows(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = all_rows["sources"]
    generated_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
    csv_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())
    checks = [
        ("VAL2969_0_sources_exist", all(row["path_exists"] for row in source_rows), "all cited local source paths exist", True),
        ("VAL2969_1_anchors_found", all(row["anchors_found"] for row in source_rows), "all cited source anchors found", True),
        ("VAL2969_2_theorem_nonclaim", all(row["theorem_zero_adopted"] is False and row["valid_for_claim"] is False for row in all_rows["theorem"]), "combined theorem not adopted as claim", True),
        ("VAL2969_3_dqz_not_zero", any(row["dqz_clause_id"] == "DQZ2969_6_verdict" and row["current_status"] == "NOT_DERIVED_RESIDUAL_BOUND_ROW_REQUIRED" for row in all_rows["dqz"]), "Dq_Z zero not derived and bound row required", True),
        ("VAL2969_4_ja_not_zero", any(row["ja_clause_id"] == "JA2969_7_verdict" and row["current_status"] == "NOT_DERIVED_RESIDUAL_BOUND_ROW_REQUIRED" for row in all_rows["ja"]), "J_A zero not derived and bound row required", True),
        ("VAL2969_5_bounds_nonclaim", all(row["numeric_bound_present"] is False and row["accepted_for_scoring"] is False and row["valid_for_claim"] is False for row in all_rows["bounds"]), "Dq_Z/J_A bound rows remain symbolic nonclaim", True),
        ("VAL2969_6_bound_paths_exist", all(row["source_path_exists"] is True for row in all_rows["bounds"]), "bound rows cite existing paths", True),
        ("VAL2969_7_readout_nonclaim", all(row["accepted_for_scoring"] is False and row["valid_for_claim"] is False for row in all_rows["readout"]), "readout consequences remain nonclaim", True),
        ("VAL2969_8_claims_blocked", all(row["condition_passed"] is False and row["claim_allowed"] is False for row in all_rows["claims"]), "all claim gates remain blocked", True),
        ("VAL2969_9_next_target_written", any(row["next_id"] == "NEXT2969_0_2970" for row in all_rows["next"]), "2970 quotient/basic-matter next target selected", True),
        ("VAL2969_10_branches_exist", all(Path(row["copy_path"]).exists() for row in all_rows["branches"]), "branch copy files exist", True),
        ("VAL2969_11_csvs_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV files parse", True),
        ("VAL2969_12_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in generated_paths), "all generated outputs are under post-checkpoint-work", True),
        ("VAL2969_13_formalization_clean", not any(is_under(path, FORMALIZATION) for path in generated_paths), "no 2969 outputs were written to formalization-workbench", True),
        ("VAL2969_14_doc_written", DOC.exists(), "2969 markdown checkpoint exists", True),
    ]
    overall = all(passed == required for _, passed, _, required in checks)
    rows = [
        add_common(
            {
                "validation_id": validation_id,
                "passed": passed,
                "check": check,
                "required": required,
            }
        )
        for validation_id, passed, check, required in checks
    ]
    rows.append(add_common({"validation_id": "VAL2969_OVERALL", "passed": overall, "check": "2969 validation overall", "required": True}))
    return rows


def write_markdown(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2969 - Y5 R2FR: DqZ and JA source-current descent proof or residual bound row under AX1090

Status: `Y5_R2FR_2969_combined_DqZ_JA_descent_theorem_conditional_not_parent_signed_bound_rows_emitted_nonclaim`

Claim ceiling: `no_DqZ_zero_claim_no_JA_zero_claim_no_R10_no_PPN_no_clock_no_orbital_no_WEP_no_local_GR_no_Newton_no_public_claim`

2969 tried the best derivation route for two rank-zero forcing channels at once.

- The theorem shape is strong: if `q` is parent-owned, `v_Z in ker(Dq)`, `theta/dmu/Obs_e` are q-basic, and ordinary matter descends as `S_matter=Sbar[q(Phi),Psi,theta(q)]`, then `Dq_Z=0` and `J_A^bulk=0`.
- The proof is not adopted for current MTS because those parent signatures do not close in one branch.
- Boundary, CDB, `M_AB` and arena projections are deliberately not touched here; zeroing `J_A^bulk` would not by itself prove local GR.
- Result: emit explicit symbolic nonclaim bound rows for `Dq_Z` and `J_A`; next target is the parent quotient/basic-matter action signature.

## Source Register

{md_table(all_rows["sources"], ["source_id", "source_path", "path_exists", "anchors_found", "role"])}

## Combined Descent Theorem Ledger

{md_table(all_rows["theorem"], ["theorem_id", "target", "statement", "current_status", "theorem_zero_adopted", "required_premises"])}

## DqZ Clause Audit

{md_table(all_rows["dqz"], ["dqz_clause_id", "clause", "would_need", "current_status", "blocking_gap", "fallback_bound_required"])}

## JA Source-Current Audit

{md_table(all_rows["ja"], ["ja_clause_id", "clause", "would_need", "current_status", "blocking_gap", "fallback_bound_required"])}

## Readout Shadow Consequence

{md_table(all_rows["readout"], ["readout_id", "component", "conditional_consequence", "current_status", "blocking_gap"])}

## Residual Bound Rows

{md_table(all_rows["bounds"], ["bound_id", "quantity", "bound_form", "missing_inputs", "numeric_bound_present", "accepted_for_scoring"])}

## Claim Gates

{md_table(all_rows["claims"], ["claim_gate_id", "claim", "condition_passed", "status", "claim_allowed"])}

## Decision Ledger

{md_table(all_rows["decision"], ["decision_id", "decision", "because", "next_action"])}

## Next Target

{md_table(all_rows["next"], ["next_id", "priority", "next_doc", "next_script", "objective", "exclude"])}

## Branch Copies

{md_table(all_rows["branches"], ["copy_id", "source_path", "copy_path", "source_exists", "copy_exists", "valid_for_claim"])}

## Validation

{md_table(all_rows["validation"], ["validation_id", "passed", "check", "required"])}

Validation overall: `{all_rows["validation"][-1]["passed"]}`.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    all_rows: dict[str, list[dict[str, Any]]] = {
        "sources": source_register_rows(),
        "theorem": theorem_rows(),
        "dqz": dqz_clause_rows(),
        "ja": ja_clause_rows(),
        "readout": readout_rows(),
        "bounds": bound_rows(),
        "claims": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_target_rows(),
    }

    for key, path in OUTPUTS.items():
        if key in {"branches", "validation"}:
            continue
        write_csv(path, all_rows[key])

    all_rows["branches"] = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], all_rows["branches"])

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)

    print(f"2969 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()
