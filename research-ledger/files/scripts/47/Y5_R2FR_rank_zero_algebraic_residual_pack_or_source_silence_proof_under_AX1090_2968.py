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

CHECKPOINT = "2968"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2968-Y5-R2FR-rank-zero-algebraic-residual-pack-or-source-silence-proof-under-AX1090.md"

SRC_2967_DOC = ROOT / "2967-Y5-R2FR-response-doublet-parent-density-adoption-or-rank-zero-switch-under-AX1090.md"
SRC_2967_NEXT = RESIDUALS / "P8_Y5_R2FR_2967_NEXT_TARGET.csv"
SRC_2967_REQUIREMENTS = RESIDUALS / "P8_Y5_R2FR_2967_RANK_ZERO_RESIDUAL_PACK_REQUIREMENTS.csv"
SRC_2967_DECISION = RESIDUALS / "P8_Y5_R2FR_2967_DECISION_LEDGER.csv"
SRC_2967_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2967_VALIDATION.csv"

SRC_2213_RANK_ZERO = BETA_SOURCE / "PARENT_QLOC_RANK_ZERO_SOURCE_CURRENT_2213_NONCLAIM.csv"
SRC_2912_CONSTRAINT = PARENT_ACTION / "Constraint_first_Z_elimination_2912_NONCLAIM.csv"
SRC_2892_NEUTRAL = SOURCE_WEIGHT / "RAB_PARENT_ACTION_SOURCE_NEUTRALITY_SCHEMA_2892_NONCLAIM.csv"
SRC_2676_OWNER = WEP_SOURCES / "action_scale_measure_owner_wip_nonclaim_2676.csv"
SRC_2677_GRAMMAR = WEP_SOURCES / "no_species_action_weight_object_language_wip_2677.csv"
SRC_2800_RESPONSE = BETA_SOURCE / "RESPONSE_DOUBLET_QLOC_BOUND_2800_NONCLAIM.csv"
SRC_2914_COBS = PARENT_ACTION / "Cobs_no_shadow_head_audit_2914_NONCLAIM.csv"
SRC_2915_SHADOW = PARENT_ACTION / "Cshadow_zero_theorem_attempt_2915_NONCLAIM.csv"
SRC_2939_CTAU = PARENT_ACTION / "Ctau_residual_decomposition_2939_NONCLAIM.csv"
SRC_2543_SPLIT = BETA_SOURCE / "Residual_split_under_private_SRNG_2543_NONCLAIM.csv"
SRC_2472_BOUNDARY = LOCAL_BOUNDS / "Boundary_topology_nohair_blocker_2472_NONCLAIM.csv"
SRC_2562_BOUNDARY = LOCAL_BOUNDS / "Boundary_topology_nohair_blocker_2562_NONCLAIM.csv"
SRC_ALPHA3_NOFLUX = RESIDUALS / "P8_BOUNDARY_ALPHA3_NOFLUX_THEOREM_ATTEMPT.csv"
SRC_ALPHA3_PREMISE = RESIDUALS / "P8_BOUNDARY_ALPHA3_PREMISE_OWNERSHIP.csv"
SRC_ALPHA3_OWNER = RESIDUALS / "P8_BOUNDARY_SCALAR_ACTION_OWNER_ATTEMPT.csv"
SRC_2699_VECTOR = LOCAL_BOUNDS / "GammaKhat_q_loc_official_residual_vector_2699_NONCLAIM.csv"
SRC_2733_BOUND = LOCAL_BOUNDS / "Khat_q_loc_residual_bound_2733_NONCLAIM.csv"
SRC_2809_DELTAK = BETA_SOURCE / "DELTAK_COMPONENT_BOUND_2809_NONCLAIM.csv"
SRC_2812_QDELTAK = BETA_SOURCE / "CPLOC_CCOMM_QDELTAK_BOUND_2812_NONCLAIM.csv"
SRC_516_TRIGGER = RESIDUALS / "P8_QLOC_BOUND_TRIGGER_LEDGER.csv"
SRC_516_SPEC = RESIDUALS / "P8_QLOC_BOUND_RUNNER_SPEC.csv"
SRC_2963_PROMOTION = PARENT_ACTION / "bconf_promotion_rules_2963_NONCLAIM.csv"
SRC_2211_ZM = BETA_SOURCE / "PARENT_QLOC_ZM_OWNER_AUDIT_2211_NONCLAIM.csv"
SRC_2411_ZMJ = BETA_SOURCE / "PARENT_QLOC_ZMJ_OWNER_AUDIT_2411_NONCLAIM.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2968_SOURCE_REGISTER.csv",
    "identity": RESIDUALS / "P8_Y5_R2FR_2968_ALGEBRAIC_IDENTITY_LEDGER.csv",
    "silence": RESIDUALS / "P8_Y5_R2FR_2968_SOURCE_SILENCE_ATTEMPT.csv",
    "terms": RESIDUALS / "P8_Y5_R2FR_2968_RANK_ZERO_TERM_STATUS.csv",
    "envelope": RESIDUALS / "P8_Y5_R2FR_2968_RESIDUAL_ENVELOPE_ROWS_NONCLAIM.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2968_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2968_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2968_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2968_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2968_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "rank_zero_pack_copy": PARENT_ACTION / "rank_zero_algebraic_residual_pack_2968_NONCLAIM.csv",
    "residual_envelope_copy": LOCAL_BOUNDS / "rank_zero_residual_envelope_2968_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2968_DqZ_JA_source_silence_next_NONCLAIM.csv",
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
        ("SRC2968_00_2967_doc", SRC_2967_DOC, "RZ2967_4_verdict;NEXT2967_0_2968", "2967 rank-zero handoff"),
        ("SRC2968_01_2967_next", SRC_2967_NEXT, "NEXT2967_0_2968", "machine-readable 2968 target"),
        ("SRC2968_02_2967_requirements", SRC_2967_REQUIREMENTS, "ALG2967_0_MAB_signature;ALG2967_7_total", "rank-zero residual pack requirements"),
        ("SRC2968_03_2967_decision", SRC_2967_DECISION, "DEC2967_2_rank_zero;DEC2967_3_local_GR", "decision input"),
        ("SRC2968_04_2967_validation", SRC_2967_VALIDATION, "VAL2967_OVERALL", "2967 validation"),
        ("SRC2968_05_2213_rank_zero", SRC_2213_RANK_ZERO, "RZS2213_0_strict_euler_identity;RZS2213_2_rank_zero_silence_theorem;RZS2213_4_verdict", "rank-zero algebraic identity"),
        ("SRC2968_06_2912_constraint", SRC_2912_CONSTRAINT, "CFP2912_0_exact_conditional;CFP2912_4_rank_zero_algebraic;CFP2912_5_current_verdict", "constraint-first Dq_Z source"),
        ("SRC2968_07_2892_neutral", SRC_2892_NEUTRAL, "PAS2892_1_quotient_action;PAS2892_5_result", "source-neutral parent action schema"),
        ("SRC2968_08_2676_owner", SRC_2676_OWNER, "OWN2676_2_hilbert_current_sublemma;OWN2676_4_verdict", "Hilbert current owner audit"),
        ("SRC2968_09_2677_grammar", SRC_2677_GRAMMAR, "GRM2677_3_species_blind_measure;GRM2677_6_verdict", "species/source grammar audit"),
        ("SRC2968_10_2800_response", SRC_2800_RESPONSE, "RDT2800_3_source_current_zero;RDT2800_4_boundary_zero;RDT2800_7_verdict", "source-current and boundary zero attempts"),
        ("SRC2968_11_2914_cobs", SRC_2914_COBS, "COBS2914_2_chain_zero_against_Z;COBS2914_5_verdict", "observed coframe chain-zero audit"),
        ("SRC2968_12_2915_shadow", SRC_2915_SHADOW, "ZTH2915_0_exact_conditional;ZTH2915_6_verdict", "shadow zero conditional theorem"),
        ("SRC2968_13_2939_ctau", SRC_2939_CTAU, "CTA2939_0_master;CTA2939_7_C_Dq;CTA2939_8_C_units", "tau/readout/Dq residual decomposition"),
        ("SRC2968_14_2543_split", SRC_2543_SPLIT, "RSL2543_2_boundary;RSL2543_4_verdict", "boundary residual split"),
        ("SRC2968_15_2472_boundary", SRC_2472_BOUNDARY, "2472", "boundary topology no-hair blocker"),
        ("SRC2968_16_2562_boundary", SRC_2562_BOUNDARY, "2562", "boundary topology no-hair blocker update"),
        ("SRC2968_17_alpha3_noflux", SRC_ALPHA3_NOFLUX, "T1_scalar_boundary_action;T7_conclusion", "conditional alpha3 boundary no-flux attempt"),
        ("SRC2968_18_alpha3_premise", SRC_ALPHA3_PREMISE, "P0_scalar_only_boundary_data;P4_Ward_flux_closure", "boundary premise ownership"),
        ("SRC2968_19_alpha3_owner", SRC_ALPHA3_OWNER, "O0_representation_zero;O2_scalar_not_enough_warning", "scalar boundary owner warning"),
        ("SRC2968_20_2699_vector", SRC_2699_VECTOR, "QLOC2699_0_q_loc_vector;QLOC2699_7_total", "official local residual vector"),
        ("SRC2968_21_2733_bound", SRC_2733_BOUND, "QB2733_0_vector_envelope;QB2733_3_verdict", "local q bound interface"),
        ("SRC2968_22_2809_deltak", SRC_2809_DELTAK, "DKB2809_0_DeltaK00;DKB2809_6_envelope", "DeltaK component residuals"),
        ("SRC2968_23_2812_qdeltak", SRC_2812_QDELTAK, "QBR2812_1_finite_bound_branch;QBR2812_3_score_gate", "qDeltaK bound gate"),
        ("SRC2968_24_516_trigger", SRC_516_TRIGGER, "BT517_0_owner_match_fails;BT517_4_PPN_lock_missing", "q_loc bound trigger ledger"),
        ("SRC2968_25_516_spec", SRC_516_SPEC, "QB516_3_PPN_metric_tail;QB516_4_R11_operator", "q_loc arena runner spec"),
        ("SRC2968_26_2963_promotion", SRC_2963_PROMOTION, "PROM2963_5_PPN_clock_source;PROM2963_6_verdict", "PPN/clock promotion gate"),
        ("SRC2968_27_2211_ZM", SRC_2211_ZM, "ZMO2211_3_Khat_metric_response_route;ZMO2211_5_verdict", "Khat metric-response blocker"),
        ("SRC2968_28_2411_ZMJ", SRC_2411_ZMJ, "2411", "Z/M/J owner audit"),
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


def identity_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "ID2968_0_rank_zero_balance",
            "rank-zero algebraic balance",
            "M_AB Z^B = J_A + B_A + C_A^CDB + R_A^src/readout/projector",
            "EXACT_CONDITIONAL_NORMAL_FORM",
            "This is the live local-GR route after rejecting unsourced finite-range lambda language.",
            SRC_2213_RANK_ZERO,
        ),
        (
            "ID2968_1_silence_condition",
            "local silence theorem condition",
            "If M_AB is invertible and J_A=B_A=C_A^CDB=R_A=0 with Dq_Z=0, then Z^A=0 and the local observed residual is silent.",
            "CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "Good theorem shape; not yet a proof because invertibility, boundary and projection clauses remain open.",
            SRC_2213_RANK_ZERO,
        ),
        (
            "ID2968_2_no_plateau",
            "no plateau axiom policy",
            "q_loc -> 0 must follow from algebraic descent or residual bounds; no inserted local vacuum plateau or post-readout cancellation is allowed.",
            "POLICY_ENFORCED",
            "Keeps the GR reduction route honest and derivable.",
            SRC_2967_REQUIREMENTS,
        ),
        (
            "ID2968_3_absolute_envelope",
            "no-cancellation residual norm",
            "|Z| <= ||M^-1|| (|J|+|B|+|CDB|+|R_src/readout/projector|)",
            "BOUND_INTERFACE_ONLY",
            "This can become test-ready only when every term has a sourced zero or sourced bound in arena units.",
            SRC_2733_BOUND,
        ),
        (
            "ID2968_4_no_claim",
            "claim ceiling",
            "No R10, PPN, clock, orbital, local-GR, Newton or public claim follows from 2968.",
            "NONCLAIM_CHECKPOINT",
            "The pack narrows the missing clauses; it does not close them.",
            SRC_2967_DECISION,
        ),
    ]
    return [
        add_common(
            {
                "identity_id": identity_id,
                "target": target,
                "statement": statement,
                "status": status,
                "evidence_summary": summary,
                "source_path": str(path),
                "source_path_exists": path.exists(),
                "accepted_as_proof": status in {"POLICY_ENFORCED"},
                "accepted_for_scoring": False,
            }
        )
        for identity_id, target, statement, status, summary, path in rows
    ]


def source_silence_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "SS2968_0_DqZ_constraint",
            "Dq_Z",
            "constraint-first quotient descent gives Dq[v_Z]=0",
            "PROMISING_CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "parent constraint origin, no magic multiplier guard and readout descent must close together",
            SRC_2912_CONSTRAINT,
            "try to prove Dq_Z=0 first because it also suppresses readout shadow terms",
        ),
        (
            "SS2968_1_JA_chain_rule",
            "J_A",
            "quotient-invariant matter/source action gives delta S_matter / delta Z^A = 0",
            "PROMISING_CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "matter/source-current owner, measure/coframe descent and species-blind grammar are still unsigned",
            SRC_2892_NEUTRAL,
            "pair with Dq_Z so source-current descent and quotient descent are one theorem",
        ),
        (
            "SS2968_2_Hilbert_current",
            "source-current owner",
            "Hilbert current uniqueness would prevent an independent non-Hilbert Z source",
            "CONDITIONAL_SCHEMA_ONLY",
            "owner audit gives a sublemma, not a parent-signed action owner",
            SRC_2676_OWNER,
            "promote only if the parent matter action and observed coframe are fixed",
        ),
        (
            "SS2968_3_boundary",
            "B_A",
            "compact collar/no-flux boundary would zero the boundary forcing",
            "HARD_OPEN_CHANNEL",
            "available alpha3 scalar no-flux proofs are narrower than the full rank-zero boundary term",
            SRC_2543_SPLIT,
            "if zero-proof fails, build explicit boundary flux bound rows",
        ),
        (
            "SS2968_4_CDB",
            "C_A^CDB",
            "domain/connection/commutator defects vanish if the local carrier is quotient-silent",
            "NO_ZERO_PROOF_CURRENT_CORPUS",
            "CDB, DeltaK and Khat metric-response residuals remain live channels",
            SRC_2699_VECTOR,
            "do not hide CDB inside a readout normalization",
        ),
        (
            "SS2968_5_readout_projector",
            "R_A^readout/projector",
            "observed coframe functor gives D_Z Obs=0 when Z is absent from q or vertical",
            "CONDITIONAL_CHAIN_ZERO_ONLY",
            "C_obs and C_shadow attempts are strong but not parent-unique or fully source silent",
            SRC_2914_COBS,
            "needs the same Dq_Z theorem plus terminal observed-frame uniqueness",
        ),
        (
            "SS2968_6_arena_projection",
            "Pi_arena[R_alg]",
            "PPN/R10/clock/orbital projections inherit zero only if every upstream term is zero or bounded",
            "MISSING_ARENA_PROJECTION",
            "runner specs explicitly block scoring without PPN metric tail, R10 operator and clock/source maps",
            SRC_516_SPEC,
            "leave all local-test rows invalid until arena maps are sourced",
        ),
        (
            "SS2968_7_verdict",
            "rank-zero source silence",
            "source silence not closed in 2968",
            "NONCLAIM_SOURCE_PACK_REQUIRED",
            "Dq_Z and J_A are the best next proof targets; boundary, CDB and arena maps remain later hard locks",
            SRC_2967_REQUIREMENTS,
            "2969 should attack Dq_Z and J_A together",
        ),
    ]
    return [
        add_common(
            {
                "silence_id": silence_id,
                "term": term,
                "candidate_zero_or_bound": candidate,
                "status": status,
                "blocking_clause": blocker,
                "source_path": str(path),
                "source_path_exists": path.exists(),
                "next_action": action,
                "theorem_zero_claimed": False,
                "accepted_for_scoring": False,
            }
        )
        for silence_id, term, candidate, status, blocker, path, action in rows
    ]


def term_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("TERM2968_0_MAB_signature", "M_AB", "algebraic Hessian/signature/invertibility", "MISSING_PARENT_SIGNATURE", "not_zero", "MISSING_SOURCE_BACKED_INVERTIBILITY", SRC_2213_RANK_ZERO, "derive signature or carry ||M^-1|| as sourced bound"),
        ("TERM2968_1_J_A", "J_A", "matter/source-current forcing", "CONDITIONAL_ZERO_NOT_PARENT_SIGNED", "conditional_zero", "MISSING_PARENT_SOURCE_CURRENT_OWNER", SRC_2892_NEUTRAL, "prove quotient-invariant matter/source-current descent"),
        ("TERM2968_2_B_A", "B_A", "boundary/corner/no-flux forcing", "MISSING_BOUNDARY_ZERO_OR_BOUND", "not_zero", "MISSING_NOFLUX_THEOREM_OR_FLUX_BOUND", SRC_2543_SPLIT, "bound boundary flux or prove parent no-flux"),
        ("TERM2968_3_CDB", "C_A^CDB", "connection/domain/commutator defect", "MISSING_CDB_ZERO_OR_BOUND", "not_zero", "MISSING_CDB_COMPONENT_BOUND", SRC_2699_VECTOR, "extract CDB component rows from DeltaK/Khat residuals"),
        ("TERM2968_4_R_src_readout_projector", "R_A", "source/readout/projector residual", "MISSING_READOUT_PROJECTOR_MAP", "not_zero", "MISSING_TERMINAL_OBSERVED_FRAME_MAP", SRC_2939_CTAU, "lock observed-frame functor and projector commutator"),
        ("TERM2968_5_DqZ", "Dq_Z", "vertical quotient leakage", "CONDITIONAL_ZERO_NOT_PARENT_SIGNED", "conditional_zero", "MISSING_PARENT_CONSTRAINT_DESCENT", SRC_2912_CONSTRAINT, "prove Dq_Z=0 under parent quotient map"),
        ("TERM2968_6_arena_projection", "Pi_arena", "R10/PPN/clock/orbital/WEP readout", "MISSING_ARENA_PROJECTION", "not_zero", "MISSING_ARENA_OPERATOR", SRC_516_SPEC, "do not score until every arena operator is sourced"),
        ("TERM2968_7_total", "R_alg_abs_total", "absolute no-cancellation rank-zero residual", "NONCLAIM_SOURCE_PACK_REQUIRED", "not_zero", "ALL_FORCING_TERMS_NOT_CLOSED", SRC_2967_REQUIREMENTS, "next route is Dq_Z + J_A proof, then boundary/CDB bounds"),
    ]
    return [
        add_common(
            {
                "term_id": term_id,
                "symbol": symbol,
                "role": role,
                "current_status": status,
                "zero_status": zero_status,
                "bound_status": bound_status,
                "source_path": str(path),
                "source_path_exists": path.exists(),
                "accepted_for_scoring": False,
                "no_cancellation_policy": True,
                "next_action": action,
            }
        )
        for term_id, symbol, role, status, zero_status, bound_status, path, action in rows
    ]


def envelope_rows() -> list[dict[str, Any]]:
    rows = [
        ("ENV2968_0_master", "rank_zero_master", "|Z| <= ||M^-1|| (|J_A|+|B_A|+|C_A^CDB|+|R_A|)", "M_AB_inv_norm;J_A_bound;B_A_bound;CDB_bound;R_A_bound", "NOT_SCORE_READY", SRC_2733_BOUND),
        ("ENV2968_1_q_loc", "q_loc_abs", "|q_loc| <= C_qZ |Z| + R_q_metric + R_q_boundary + R_q_projector", "C_qZ;DeltaK;boundary;projector", "NOT_SCORE_READY", SRC_2699_VECTOR),
        ("ENV2968_2_R10", "alpha_R10_projection", "|alpha_R10| <= Pi_R10[rank_zero_master]", "Pi_R10 operator;lambda replacement policy;source/test normalization", "VALID_FOR_CLAIM_FALSE", SRC_516_TRIGGER),
        ("ENV2968_3_PPN", "PPN_residual_vector", "||delta gamma, delta beta, alpha_i|| <= Pi_PPN[rank_zero_master]", "PPN metric tail;source frame;clock frame", "VALID_FOR_CLAIM_FALSE", SRC_516_SPEC),
        ("ENV2968_4_clock", "clock_residual", "|delta nu/nu| <= Pi_clock[rank_zero_master]", "clock transition map;alpha_EM/mass response;source-current owner", "VALID_FOR_CLAIM_FALSE", SRC_2963_PROMOTION),
        ("ENV2968_5_orbital", "orbital_residual", "|delta a_orb| <= Pi_orbital[rank_zero_master]", "orbital force map;boundary support;mass/source normalization", "VALID_FOR_CLAIM_FALSE", SRC_2733_BOUND),
        ("ENV2968_6_WEP", "WEP_residual", "|eta| <= Pi_WEP[rank_zero_master]", "species-blind grammar;source charge basis;Hilbert current owner", "VALID_FOR_CLAIM_FALSE", SRC_2677_GRAMMAR),
    ]
    return [
        add_common(
            {
                "envelope_id": envelope_id,
                "arena": arena,
                "formula": formula,
                "requires": requires,
                "status": status,
                "source_path": str(path),
                "source_path_exists": path.exists(),
                "numeric_bound_present": False,
                "accepted_for_scoring": False,
                "no_cancellation_policy": True,
            }
        )
        for envelope_id, arena, formula, requires, status, path in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2968_0_MAB", "M_AB invertible/signature parent-signed", False, "MISSING_PARENT_SIGNATURE"),
        ("CG2968_1_all_forcing_zero", "J_A, B_A, CDB and R_A theorem-zero", False, "FORCING_TERMS_OPEN"),
        ("CG2968_2_all_forcing_bounded", "all forcing terms source-backed bounded in common units", False, "BOUND_ROWS_MISSING"),
        ("CG2968_3_DqZ_JA", "Dq_Z and J_A parent descent closed", False, "PROMISING_BUT_UNSIGNED"),
        ("CG2968_4_boundary", "boundary no-flux closed for full rank-zero pack", False, "BOUNDARY_HARD_OPEN"),
        ("CG2968_5_CDB", "CDB/domain/connection defect closed", False, "CDB_HARD_OPEN"),
        ("CG2968_6_arena", "R10/PPN/clock/orbital projection operators sourced", False, "ARENA_PROJECTIONS_MISSING"),
        ("CG2968_7_local_GR", "derived local GR/Newton reduction claimed", False, "NO_LOCAL_GR_OR_NEWTON_CLAIM"),
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
            "DEC2968_0_rank_zero_pack",
            "rank-zero residual pack is the active local-GR route",
            "it converts the vague local plateau problem into named forcing terms",
            "keep the pack and require every term to zero or bound",
        ),
        (
            "DEC2968_1_DqZ_JA",
            "Dq_Z and J_A are the best next proof targets",
            "they share the same quotient/matter-action descent structure and would suppress readout/source leakage together",
            "build 2969 around a combined descent theorem",
        ),
        (
            "DEC2968_2_boundary_CDB",
            "boundary and CDB remain the hard later locks",
            "existing no-flux material is too narrow and CDB remains a retained residual vector",
            "defer until the cleaner descent terms are tested",
        ),
        (
            "DEC2968_3_claims",
            "no local-GR, R10, PPN, clock, WEP or orbital claim",
            "the residual envelope is an interface, not a sourced prediction",
            "keep all rows nonclaim and invalid for scoring",
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
                "next_id": "NEXT2968_0_2969",
                "priority": "selected_primary",
                "next_doc": "2969-Y5-R2FR-DqZ-and-JA-source-current-descent-proof-or-residual-bound-row-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_DqZ_and_JA_source_current_descent_proof_or_residual_bound_row_under_AX1090_2969.py",
                "objective": "Try to close Dq_Z=0 and J_A=0 together through parent quotient-map descent plus matter/source-current action descent; if either clause fails, emit explicit Dq_Z and J_A residual bound rows.",
                "include": "parent quotient map q;vertical generator v_Z;constraint-first elimination;matter action descent;source-current owner;measure/coframe descent;species-blind grammar;readout shadow consequence;fallback residual bounds",
                "exclude": "boundary no-flux proof;CDB closure;R10 alpha claim;PPN claim;clock/orbital claim;local-GR claim;GitHub action;formalization-workbench edits;plateau axiom",
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = [
        ("rank_zero_pack_copy", OUTPUTS["terms"], BRANCH_OUTPUTS["rank_zero_pack_copy"]),
        ("residual_envelope_copy", OUTPUTS["envelope"], BRANCH_OUTPUTS["residual_envelope_copy"]),
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
        ("VAL2968_0_sources_exist", all(row["path_exists"] for row in source_rows), "all cited local source paths exist", True),
        ("VAL2968_1_anchors_found", all(row["anchors_found"] for row in source_rows), "all cited source anchors found", True),
        ("VAL2968_2_identity_nonclaim", all(row["valid_for_claim"] is False and row["accepted_for_scoring"] is False for row in all_rows["identity"]), "identity ledger remains nonclaim and not score-ready", True),
        ("VAL2968_3_no_plateau_policy", any(row["identity_id"] == "ID2968_2_no_plateau" and row["status"] == "POLICY_ENFORCED" for row in all_rows["identity"]), "plateau axiom explicitly excluded", True),
        ("VAL2968_4_terms_not_scoring", all(row["accepted_for_scoring"] is False and row["valid_for_claim"] is False for row in all_rows["terms"]), "no rank-zero term is accepted for scoring", True),
        ("VAL2968_5_term_paths_exist", all(row["source_path_exists"] is True for row in all_rows["terms"]), "term status rows cite existing paths", True),
        ("VAL2968_6_envelope_nonclaim", all(row["accepted_for_scoring"] is False and row["numeric_bound_present"] is False and row["valid_for_claim"] is False for row in all_rows["envelope"]), "residual envelope rows remain nonclaim", True),
        ("VAL2968_7_envelope_paths_exist", all(row["source_path_exists"] is True for row in all_rows["envelope"]), "envelope rows cite existing paths", True),
        ("VAL2968_8_claims_blocked", all(row["condition_passed"] is False and row["claim_allowed"] is False for row in all_rows["claims"]), "all claim gates remain blocked", True),
        ("VAL2968_9_next_target_written", any(row["next_id"] == "NEXT2968_0_2969" for row in all_rows["next"]), "2969 Dq_Z/J_A next target selected", True),
        ("VAL2968_10_branches_exist", all(Path(row["copy_path"]).exists() for row in all_rows["branches"]), "branch copy files exist", True),
        ("VAL2968_11_csvs_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV files parse", True),
        ("VAL2968_12_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in generated_paths), "all generated outputs are under post-checkpoint-work", True),
        ("VAL2968_13_formalization_clean", not any(is_under(path, FORMALIZATION) for path in generated_paths), "no 2968 outputs were written to formalization-workbench", True),
        ("VAL2968_14_doc_written", DOC.exists(), "2968 markdown checkpoint exists", True),
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
    rows.append(add_common({"validation_id": "VAL2968_OVERALL", "passed": overall, "check": "2968 validation overall", "required": True}))
    return rows


def write_markdown(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2968 - Y5 R2FR: rank-zero algebraic residual pack or source-silence proof under AX1090

Status: `Y5_R2FR_2968_rank_zero_pack_built_DqZ_JA_promising_boundary_CDB_open_nonclaim`

Claim ceiling: `no_R10_no_PPN_no_clock_no_orbital_no_WEP_no_local_GR_no_Newton_no_public_claim`

2968 converts the local-vacuum problem into a named algebraic residual pack rather than inserting a plateau axiom.

- Active balance: `M_AB Z^B = J_A + B_A + C_A^CDB + R_A^src/readout/projector`.
- Best live proof route: close `Dq_Z=0` and `J_A=0` together by parent quotient descent plus matter/source-current descent.
- Hard open channels: `M_AB` signature/invertibility, boundary no-flux, CDB/domain/connection defects, readout/projector maps and arena projections.
- Result: local GR/Newton reduction remains alive but not claimable; 2969 should attack the shared `Dq_Z/J_A` descent theorem first.

## Source Register

{md_table(all_rows["sources"], ["source_id", "source_path", "path_exists", "anchors_found", "role"])}

## Algebraic Identity Ledger

{md_table(all_rows["identity"], ["identity_id", "target", "statement", "status", "accepted_as_proof", "accepted_for_scoring"])}

## Source Silence Attempt

{md_table(all_rows["silence"], ["silence_id", "term", "candidate_zero_or_bound", "status", "blocking_clause", "next_action"])}

## Rank-Zero Term Status

{md_table(all_rows["terms"], ["term_id", "symbol", "current_status", "zero_status", "bound_status", "accepted_for_scoring", "next_action"])}

## Residual Envelope Rows

{md_table(all_rows["envelope"], ["envelope_id", "arena", "formula", "requires", "status", "numeric_bound_present", "accepted_for_scoring"])}

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
        "identity": identity_rows(),
        "silence": source_silence_rows(),
        "terms": term_status_rows(),
        "envelope": envelope_rows(),
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

    print(f"2968 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()
