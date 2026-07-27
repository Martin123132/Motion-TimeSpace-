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
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2959"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2959-Y5-R2FR-single-observed-frame-parent-action-clause-or-bconf-bound-intake-under-AX1090.md"

SRC_2958_DOC = ROOT / "2958-Y5-R2FR-b-conf-b-marker-bound-row-or-hidden-domain-theorem-under-AX1090.md"
SRC_2958_NEXT = RESIDUALS / "P8_Y5_R2FR_2958_NEXT_TARGET.csv"
SRC_2958_BCONF = RESIDUALS / "P8_Y5_R2FR_2958_BCONF_NO_SHADOW_THEOREM_GATE.csv"
SRC_2958_BOUNDS = RESIDUALS / "P8_Y5_R2FR_2958_COMPONENT_BOUND_ROWS_NONCLAIM.csv"
SRC_2958_ARENAS = RESIDUALS / "P8_Y5_R2FR_2958_ARENA_PROJECTION_REQUIREMENTS.csv"
SRC_1046_NOSHADOW = RESIDUALS / "P8_Y5_R10_1046_NO_SHADOW_FRAME_THEOREM_ATTEMPT.csv"
SRC_1046_FORBIDDEN = RESIDUALS / "P8_Y5_R10_1046_FORBIDDEN_VERTEX_CATALOG.csv"
SRC_736_CONTRACT = RESIDUALS / "P8_Y5_R10_736_MATTER_NO_MARKER_CONTRACT.csv"
SRC_2571_COFRAME = RESIDUALS / "P8_Y5_OBS_COFRAME_2571_DOBS_KERNEL_GATE.csv"
SRC_2611_CHAIN = RESIDUALS / "P8_Y5_MATTER_DESCENT_GATE_2611_CHAIN_RULE_DECOMPOSITION.csv"
SRC_2659_HOM = RESIDUALS / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_PROOF_REDUCTION_MATRIX.csv"
SRC_2673_JX = RESIDUALS / "P8_Y5_R2FR_JX_QBARXT_2673_SOURCE_ZERO_AUDIT.csv"
SRC_LOCAL_BOUNDS = LOCAL_BOUNDS / "local_bound_claims.csv"
SRC_R10_CURVE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv"
SRC_CLOCK_ALPHA = RESIDUALS / "P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2959_SOURCE_REGISTER.csv",
    "frame_gate": RESIDUALS / "P8_Y5_R2FR_2959_SINGLE_OBSERVED_FRAME_PARENT_ACTION_GATE.csv",
    "bconf_intake": RESIDUALS / "P8_Y5_R2FR_2959_BCONF_BOUND_INTAKE_NONCLAIM.csv",
    "projection": RESIDUALS / "P8_Y5_R2FR_2959_BCONF_PROJECTION_MAP_REQUIREMENTS.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2959_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2959_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2959_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2959_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2959_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "frame_copy": PARENT_ACTION / "single_observed_frame_parent_action_gate_2959_NOT_DERIVED.csv",
    "bconf_copy": LOCAL_BOUNDS / "b_conf_bound_intake_2959_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2959_BCONF_TAU_PROJECTION_OR_SINGLE_FRAME_AXIOM_NEXT_NONCLAIM.csv",
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
        ("SRC2959_00_2958_doc", SRC_2958_DOC, "NEXT2958_0_2959;Validation overall: `True`", "2958 handoff"),
        ("SRC2959_01_2958_next", SRC_2958_NEXT, "NEXT2958_0_2959", "machine-readable 2959 target"),
        ("SRC2959_02_2958_bconf", SRC_2958_BCONF, "BCONF2958_1_chain_rule_zero;BCONF2958_5_verdict", "b_conf theorem gate"),
        ("SRC2959_03_2958_bounds", SRC_2958_BOUNDS, "BOUND2958_0_b_conf;BOUND2958_2_joint_envelope", "component bound rows"),
        ("SRC2959_04_2958_arenas", SRC_2958_ARENAS, "ARENA2958_0_R10_b_conf;ARENA2958_2_PPN_b_conf;ARENA2958_3_clock_b_conf", "arena projection requirements"),
        ("SRC2959_05_1046_noshadow", SRC_1046_NOSHADOW, "NSF1046_1_conditional_chain_rule_zero;NSF1046_2_no_extra_frame_slot;NSF1046_5_verdict", "no-shadow frame theorem"),
        ("SRC2959_06_1046_forbidden", SRC_1046_FORBIDDEN, "FV1046_0_conformal_frame;FV1046_1_disformal_frame;FV1046_6_source_only_weight", "forbidden vertex catalog"),
        ("SRC2959_07_736_contract", SRC_736_CONTRACT, "NMC736_1_one_observed_coframe;NMC736_3_shadow_frame_forbidden;NMC736_5_limit", "single coframe contract"),
        ("SRC2959_08_2571_coframe", SRC_2571_COFRAME, "DOK2571_0_exact_kernel;DOK2571_4_current_verdict", "observed coframe kernel"),
        ("SRC2959_09_2611_chain", SRC_2611_CHAIN, "CR2611_0_variation_identity;CR2611_6_direct_vertex", "matter variation chain-rule decomposition"),
        ("SRC2959_10_2659_hom", SRC_2659_HOM, "RED2659_3_single_frame_slot;RED2659_7_verdict", "single-frame domain signature"),
        ("SRC2959_11_2673_jx", SRC_2673_JX, "JX2673_4_hidden_frame;JX2673_7_verdict", "hidden-frame source-zero audit"),
        ("SRC2959_12_local_bounds", SRC_LOCAL_BOUNDS, "R1_WEP_source_charge;R2_clock_redshift;R3_gamma", "local WEP/clock/PPN bounds"),
        ("SRC2959_13_r10_curve", SRC_R10_CURVE, "R10_VECTOR_2020_REVIEW_0000;review_candidate_only", "R10 curve nonclaim source"),
        ("SRC2959_14_clock_alpha", SRC_CLOCK_ALPHA, "CAS646_0_AlHg;CAS646_1_YbE3E2", "clock alpha sensitivity source"),
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


def frame_gate_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "SFRAME2959_0_target_clause",
            "single observed frame parent action clause",
            "S_matter = S_ord[Psi_A, e_obs(q), omega[e_obs], gauge_obs, theta_A] with no A_A(Xhat)e_obs, B_A(Xhat), source-only frame, or post-readout frame slot.",
            "CLAUSE_SHARP",
            "If signed, the hidden conformal frame coefficient is absent by action-domain typing.",
            True,
            False,
        ),
        (
            "SFRAME2959_1_chain_rule",
            "b_conf chain-rule zero",
            "a_A(Phi)=abar_A(q(Phi)) and Dq[v_X]=0 imply D_vX a_A=0.",
            "EXACT_CONDITIONAL_THEOREM",
            "The math is clean once a_A is quotient-owned rather than an independent hidden frame.",
            True,
            False,
        ),
        (
            "SFRAME2959_2_covariance_test",
            "covariance alone",
            "A conformally hidden frame S_A[psi_A, exp(2 epsilon Xhat)g_obs] is diffeomorphism covariant.",
            "INSUFFICIENT",
            "General covariance does not forbid the slot.",
            False,
            False,
        ),
        (
            "SFRAME2959_3_WEP_test",
            "universality/free fall",
            "A universal b_conf can be leading-order WEP-safe while still changing trace coupling, source normalization, PPN and clocks.",
            "INSUFFICIENT",
            "WEP can constrain species differences but does not kill a universal conformal coupling.",
            False,
            False,
        ),
        (
            "SFRAME2959_4_Bianchi_test",
            "Bianchi/conservation",
            "Diffeomorphism invariance can move the hidden-frame term into scalar exchange/current balance instead of erasing it.",
            "INSUFFICIENT",
            "Conservation must be specified in the observed frame as a parent clause, not inferred from covariance alone.",
            False,
            False,
        ),
        (
            "SFRAME2959_5_calibration_test",
            "common calibration",
            "A constant common frame factor is unit/G calibration, but an X-dependent factor has D_vX ln A_A and remains physical.",
            "CONDITIONAL_ONLY",
            "Readout/source-order silence is needed before calibration can erase anything.",
            True,
            False,
        ),
        (
            "SFRAME2959_6_existing_contract",
            "736/1046/2659 contract status",
            "Existing files state the single-frame/no-shadow contract but mark it as conditional or not parent-signed.",
            "CONTRACT_AVAILABLE_NOT_DERIVED",
            "The current corpus contains the right clause shape, not its parent derivation.",
            True,
            False,
        ),
        (
            "SFRAME2959_7_verdict",
            "single-frame parent action derivation",
            "SFRAME2959_2 through SFRAME2959_6 jointly force the clause from deeper MTS primitives.",
            "SINGLE_FRAME_CLAUSE_NOT_DERIVED",
            "The clause is a valid closure candidate, but not derived from existing parent primitives.",
            False,
            False,
        ),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "object": obj,
                "statement": statement,
                "current_status": status,
                "evidence_summary": evidence,
                "conditional_math_available": conditional,
                "parent_signed": signed,
                "theorem_zero_credit": signed,
            }
        )
        for gate_id, obj, statement, status, evidence, conditional, signed in rows
    ]


def bconf_intake_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "BCI2959_0_definition",
            "b_conf",
            "dimensionless",
            "b_conf := D_vX ln A_A for a hidden conformal matter/source frame g_A=A_A(Xhat)^2 g_obs",
            "MISSING_THEOREM_ZERO_OR_NUMERIC_VALUE",
            "source-intake/mts_residuals/P8_Y5_R10_1046_QBAR_MARKER_COEFFICIENT_ROWS.csv",
        ),
        (
            "BCI2959_1_tau_R10_conf",
            "tau_R10_conf",
            "dimensionless_projection",
            "projection from b_conf and lambda_X into Yukawa alpha(lambda) or equivalent short-range strength",
            "MISSING_PROJECTION_MAP",
            str(SRC_R10_CURVE),
        ),
        (
            "BCI2959_2_tau_PPN_gamma_conf",
            "tau_PPN_gamma_conf",
            "dimensionless_projection",
            "projection from b_conf into Cassini/PPN gamma_minus_1 or equivalent source-normalization residual",
            "MISSING_PPN_MAP",
            str(SRC_LOCAL_BOUNDS),
        ),
        (
            "BCI2959_3_tau_clock_conf",
            "tau_clock_conf",
            "dimensionless_projection",
            "projection from b_conf and local Xhat state into redshift/LPI or clock-ratio observable",
            "MISSING_CLOCK_MAP",
            str(SRC_LOCAL_BOUNDS),
        ),
        (
            "BCI2959_4_tau_source_conf",
            "tau_source_conf",
            "dimensionless_projection",
            "projection from b_conf into source-normalization/current response used by WEP/R10 source-charge rows",
            "MISSING_SOURCE_NORMALIZATION_MAP",
            str(SRC_LOCAL_BOUNDS),
        ),
        (
            "BCI2959_5_B_conf_envelope",
            "B_conf",
            "dimensionless",
            "|b_conf| <= min(B_R10/|tau_R10_conf|, B_PPN/|tau_PPN_gamma_conf|, B_clock/|tau_clock_conf|, B_source/|tau_source_conf|)",
            "MISSING_TAU_PROJECTIONS",
            ";".join(str(path) for path in [SRC_2958_BOUNDS, SRC_LOCAL_BOUNDS, SRC_R10_CURVE]),
        ),
    ]
    return [
        add_common(
            {
                "row_id": row_id,
                "symbol": symbol,
                "units": units,
                "definition_or_bound": definition,
                "numeric_or_theorem_value": value,
                "source_path": source_path,
                "source_path_exists": all((ROOT / path).exists() if not Path(path).is_absolute() else Path(path).exists() for path in source_path.split(";")),
                "source_backed_value": False,
                "accepted_for_scoring": False,
                "no_cancellation_policy": True,
            }
        )
        for row_id, symbol, units, definition, value, source_path in rows
    ]


def projection_rows() -> list[dict[str, Any]]:
    rows = [
        ("PROJ2959_0_R10", "R10", "tau_R10_conf", "requires lambda_X, Xhat normalization and mapping from conformal frame to alpha(lambda)", "MISSING_LAMBDA_AND_ALPHA_MAP", str(SRC_R10_CURVE)),
        ("PROJ2959_1_PPN", "PPN/Cassini", "tau_PPN_gamma_conf", "requires metric-frame relation and b_conf-to-gamma_minus_1 map", "MISSING_METRIC_PPN_MAP", str(SRC_LOCAL_BOUNDS)),
        ("PROJ2959_2_clock_redshift", "clock/redshift", "tau_clock_conf", "requires local Xhat profile and coupling to clock/redshift observable", "MISSING_CLOCK_LOCAL_STATE_MAP", str(SRC_LOCAL_BOUNDS)),
        ("PROJ2959_3_source_charge", "WEP/source normalization", "tau_source_conf", "requires source-current normalization and test/source response split", "MISSING_SOURCE_CURRENT_MAP", str(SRC_LOCAL_BOUNDS)),
        ("PROJ2959_4_joint_policy", "joint envelope", "no_cancellation_policy", "requires all projections evaluated without cancellation between arenas or coefficients", "POLICY_READY_VALUES_MISSING", str(SRC_2958_BOUNDS)),
    ]
    return [
        add_common(
            {
                "projection_id": projection_id,
                "arena": arena,
                "symbol": symbol,
                "requirement": requirement,
                "current_status": status,
                "source_path": source_path,
                "source_path_exists": Path(source_path).exists(),
                "ready_for_score": False,
            }
        )
        for projection_id, arena, symbol, requirement, status, source_path in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2959_0_single_frame", "single-observed-frame parent action clause derived", False, "NOT_DERIVED_FROM_EXISTING_PRIMITIVES"),
        ("CG2959_1_bconf_zero", "b_conf=0 theorem-zero", False, "SINGLE_FRAME_CLAUSE_UNSIGNED"),
        ("CG2959_2_bconf_bound", "b_conf bound intake score-ready", False, "TAU_PROJECTIONS_MISSING"),
        ("CG2959_3_qbarXT", "qbarXT hidden-frame channel score-ready", False, "BCONF_ROW_NONCLAIM"),
        ("CG2959_4_R10_PPN_clock", "R10/PPN/clock arena scoring allowed", False, "PROJECTION_MAPS_MISSING"),
        ("CG2959_5_local_GR", "local GR/Newton reduction allowed", False, "NO_LOCAL_GR_CLAIM"),
        ("CG2959_6_public", "public claim allowed", False, "PRIVATE_NONCLAIM_CHECKPOINT"),
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
            "DEC2959_0_derivation",
            "single-frame clause is not derived by current corpus",
            "covariance, WEP, Bianchi conservation and calibration arguments each leave a universal hidden conformal frame countermodel alive",
            "do not claim b_conf=0 from existing parent primitives",
        ),
        (
            "DEC2959_1_closure_option",
            "single-frame clause is an exact closure candidate",
            "if adopted as parent action grammar, b_conf=0 follows immediately by domain typing and chain rule",
            "label it as closure/axiom unless a deeper parent derivation is found",
        ),
        (
            "DEC2959_2_bound_option",
            "b_conf bound intake is now explicit but nonclaim",
            "the local bound anchors exist but tau_R10/tau_PPN/tau_clock/tau_source projections are not derived",
            "derive projection maps before any local arena score",
        ),
        (
            "DEC2959_3_next",
            "next target should derive tau projections or adopt a clearly labelled action-domain closure",
            "this is the fork: either make b_conf vanish by action grammar or quantify it as a residual",
            "build 2960 b_conf tau projection map or single-frame closure declaration",
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
                "next_id": "NEXT2959_0_2960",
                "priority": "selected_primary",
                "next_doc": "2960-Y5-R2FR-bconf-tau-projection-map-or-single-frame-closure-declaration-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_bconf_tau_projection_map_or_single_frame_closure_declaration_under_AX1090_2960.py",
                "objective": "Either derive the b_conf arena projection maps tau_R10_conf, tau_PPN_gamma_conf, tau_clock_conf and tau_source_conf from the retained local state, or formally demote the single-observed-frame rule to an explicit closure/axiom with no local-GR claim.",
                "include": "tau_R10_conf;tau_PPN_gamma_conf;tau_clock_conf;tau_source_conf;lambda_X;Xhat normalization;scalar-tensor countermodel;single-frame closure label;nonclaim policy",
                "exclude": "b_marker full taxonomy;quotient/vertical no-pole rerun;beta prediction;direct lambda closure;alpha(lambda) scoring;I_X scoring;local-GR claim;public claim;formalization-workbench edits;GitHub action",
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = [
        ("frame_copy", OUTPUTS["frame_gate"], BRANCH_OUTPUTS["frame_copy"]),
        ("bconf_copy", OUTPUTS["bconf_intake"], BRANCH_OUTPUTS["bconf_copy"]),
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
        ("VAL2959_0_sources_exist", all(row["path_exists"] for row in source_rows), "all cited local source paths exist", True),
        ("VAL2959_1_anchors_found", all(row["anchors_found"] for row in source_rows), "all cited source anchors found", True),
        ("VAL2959_2_single_frame_blocked", any(row["gate_id"] == "SFRAME2959_7_verdict" and row["theorem_zero_credit"] is False for row in all_rows["frame_gate"]), "single-frame parent clause remains not derived", True),
        ("VAL2959_3_bconf_intake_nonclaim", all(row["accepted_for_scoring"] is False and row["valid_for_claim"] is False for row in all_rows["bconf_intake"]), "b_conf intake rows remain nonclaim", True),
        ("VAL2959_4_bconf_paths_exist", all(row["source_path_exists"] is True for row in all_rows["bconf_intake"]), "b_conf intake rows cite existing paths", True),
        ("VAL2959_5_projections_blocked", all(row["ready_for_score"] is False and row["valid_for_claim"] is False for row in all_rows["projection"]), "projection maps remain blocked", True),
        ("VAL2959_6_claims_blocked", all(row["condition_passed"] is False and row["claim_allowed"] is False for row in all_rows["claims"]), "all claim gates remain blocked", True),
        ("VAL2959_7_next_target_written", any(row["next_id"] == "NEXT2959_0_2960" for row in all_rows["next"]), "2960 next target selected", True),
        ("VAL2959_8_branches_exist", all(Path(row["copy_path"]).exists() for row in all_rows["branches"]), "branch copy files exist", True),
        ("VAL2959_9_csvs_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV files parse", True),
        ("VAL2959_10_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in generated_paths), "all generated outputs are under post-checkpoint-work", True),
        ("VAL2959_11_formalization_clean", not any(is_under(path, FORMALIZATION) for path in generated_paths), "no 2959 outputs were written to formalization-workbench", True),
        ("VAL2959_12_doc_written", DOC.exists(), "2959 markdown checkpoint exists", True),
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
    rows.append(add_common({"validation_id": "VAL2959_OVERALL", "passed": overall, "check": "2959 validation overall", "required": True}))
    return rows


def write_markdown(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2959 - Y5 R2FR: single-observed-frame parent action clause or bconf bound intake under AX1090

Status: `Y5_R2FR_2959_single_frame_clause_not_derived_bconf_bound_intake_emitted_nonclaim`

Claim ceiling: `no_single_frame_parent_derivation_no_b_conf_zero_no_bconf_arena_score_no_qbarXT_closure_no_local_GR_no_Newton_no_public_claim`

2959 asks whether the single-observed-frame rule can be derived rather than adopted. The result is:

- The desired parent action clause is now exact: ordinary matter may depend on `e_obs(q)` and fixed representation data, but not on `A_A(Xhat)e_obs` or source-specific hidden frame slots.
- If that clause is signed, `b_conf=0` follows immediately by domain typing and the existing chain rule.
- Current evidence does not derive the clause: covariance, WEP, Bianchi/conservation and calibration tests all leave a universal hidden conformal frame countermodel alive.
- Therefore `b_conf` is either an explicit closure/axiom if the clause is adopted, or a nonclaim residual requiring `tau_R10`, `tau_PPN`, `tau_clock` and `tau_source` projection maps.

## Source Register

{md_table(all_rows["sources"], ["source_id", "source_path", "path_exists", "anchors_found", "role"])}

## Single Observed Frame Parent Action Gate

{md_table(all_rows["frame_gate"], ["gate_id", "object", "current_status", "conditional_math_available", "parent_signed", "theorem_zero_credit", "evidence_summary"])}

## b_conf Bound Intake

{md_table(all_rows["bconf_intake"], ["row_id", "symbol", "numeric_or_theorem_value", "units", "source_path_exists", "accepted_for_scoring", "definition_or_bound"])}

## b_conf Projection Map Requirements

{md_table(all_rows["projection"], ["projection_id", "arena", "symbol", "current_status", "source_path_exists", "requirement"])}

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
        "frame_gate": frame_gate_rows(),
        "bconf_intake": bconf_intake_rows(),
        "projection": projection_rows(),
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

    print(f"2959 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()
