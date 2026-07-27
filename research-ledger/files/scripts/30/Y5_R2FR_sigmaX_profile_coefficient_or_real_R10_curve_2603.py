from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_SIGMAX_PROFILE_REBASE_2603"
CHECKPOINT_ID = "2603"

DOC = ROOT / "2603-Y5-R2FR-sigmaX-profile-coefficient-or-real-R10-curve.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_SIGMAX_PROFILE_REBASE_2603_SOURCE_REGISTER.csv",
    "lineage_ledger": OUT / "P8_Y5_SIGMAX_PROFILE_REBASE_2603_LINEAGE_LEDGER.csv",
    "profile_gate": OUT / "P8_Y5_SIGMAX_PROFILE_REBASE_2603_PROFILE_GATE_STATUS.csv",
    "tail_law_bridge": OUT / "P8_Y5_SIGMAX_PROFILE_REBASE_2603_TAIL_LAW_BRIDGE.csv",
    "runner_refusal": OUT / "P8_Y5_SIGMAX_PROFILE_REBASE_2603_RUNNER_REFUSAL.csv",
    "claim_gates": OUT / "P8_Y5_SIGMAX_PROFILE_REBASE_2603_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_SIGMAX_PROFILE_REBASE_2603_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_SIGMAX_PROFILE_REBASE_2603_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_SIGMAX_PROFILE_REBASE_2603_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2603_VALIDATION.csv",
}

COPY_TARGETS = {
    "profile_gate": LOCAL_BOUNDS / "SigmaX_profile_gate_2603_NONCLAIM.csv",
    "tail_law_bridge": LOCAL_BOUNDS / "SigmaX_tail_law_bridge_2603_NONCLAIM.csv",
    "next_target": QUEUE / "JR2603_SCREENED_TAIL_DERIVATIVE_OR_TRANSITION_WALL_NEXT.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def with_stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": utc_now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        **row,
    }


def row_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (list, tuple, set)):
        return ";".join(str(item) for item in value)
    if value is None:
        return ""
    return str(value)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row_value(row.get(field, "")) for field in fields})


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), len(rows), ""
    except Exception as exc:
        return False, 0, str(exc)


def path_has_needles(path: Path, needles: list[str]) -> list[str]:
    if not path.exists():
        return needles
    text = path.read_text(encoding="utf-8", errors="replace")
    return [needle for needle in needles if needle not in text]


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        {
            "source_id": "SRC2603_00_2602_handoff",
            "source_path": ROOT / "2602-Y5-R2FR-current-descent-lemma-Dq-tau-projectability-or-theta-leak-row.md",
            "needles": ["BGB2602_3_gamma_response", "NEXT2602_0_selected", "VAL2602_OVERALL"],
            "role": "current branch handoff selecting sigmaX profile or real R10 curve",
        },
        {
            "source_id": "SRC2603_01_1742_doc",
            "source_path": ROOT / "1742-Y5-R2FR-sigmaX-profile-coefficient-or-real-R10-curve.md",
            "needles": ["SXP1742_0_definition", "R10CURVE1742_0", "NEXT1742_0_primary", "VAL1742_OVERALL"],
            "role": "sigmaX profile coefficient contract and R10 placeholder status",
        },
        {
            "source_id": "SRC2603_02_1742_contract",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1742_SIGMAX_PROFILE_CONTRACT.csv",
            "needles": ["SXP1742_0_definition", "SXP1742_1_xU_profile", "SXP1742_2_gamma_prediction"],
            "role": "s_X=b_g x_U profile contract",
        },
        {
            "source_id": "SRC2603_03_1743_doc",
            "source_path": ROOT / "1743-Y5-R2FR-weak-field-source-profile-first-row-or-R10-digitization-workflow.md",
            "needles": ["WFP1743_0_Gamma_gradient_shape", "WFP1743_1_screened_scaling_shape", "NEXT1743_0_primary", "VAL1743_OVERALL"],
            "role": "weak-field formula-shape row and R10 digitization workflow status",
        },
        {
            "source_id": "SRC2603_04_1743_profile_row",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1743_WEAK_FIELD_PROFILE_FIRST_ROW.csv",
            "needles": ["WFP1743_0_Gamma_gradient_shape", "WFP1743_2_sigmaX_first_row"],
            "role": "source-backed nonclaim weak-field profile shape",
        },
        {
            "source_id": "SRC2603_05_1744_doc",
            "source_path": ROOT / "1744-Y5-R2FR-support-powers-pS-pL-pT-or-Khat-scalar-profile.md",
            "needles": ["SP1744_0_pS", "KSP1744_0_scalar_DeltaK_channel", "NEXT1744_0_primary", "VAL1744_OVERALL"],
            "role": "support power and Khat scalar profile gate",
        },
        {
            "source_id": "SRC2603_06_1744_support_power",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1744_SUPPORT_POWER_GATE.csv",
            "needles": ["SP1744_0_pS", "SP1744_1_pL", "SP1744_2_pT"],
            "role": "pS/pL/pT support power rows",
        },
        {
            "source_id": "SRC2603_07_1744_khat",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1744_KHAT_SCALAR_PROFILE_ROW.csv",
            "needles": ["KSP1744_0_scalar_DeltaK_channel", "KSP1744_1_Khat_amplitude_guard"],
            "role": "Khat scalar subtraction rows",
        },
        {
            "source_id": "SRC2603_08_1745_doc",
            "source_path": ROOT / "1745-Y5-R2FR-fixed-point-double-zero-for-pL-pT-or-DeltaK-component-row.md",
            "needles": ["FZD1745_2_gradient_tail_requirement", "DKC1745_0_DeltaK00_template", "NEXT1745_0_primary", "VAL1745_OVERALL"],
            "role": "double-zero sharpener and DeltaK fallback",
        },
        {
            "source_id": "SRC2603_09_1745_tail_gate",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1745_GRADIENT_TAIL_GATE.csv",
            "needles": ["GT1745_2_tail_derivative", "GT1745_3_transition_width"],
            "role": "screened-tail derivative law blockers",
        },
        {
            "source_id": "SRC2603_10_1745_DeltaK",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1745_DELTAK_COMPONENT_ROW.csv",
            "needles": ["DKC1745_0_DeltaK00_template", "DKC1745_1_scalar_projection"],
            "role": "DeltaK/Khat finite fallback rows",
        },
        {
            "source_id": "SRC2603_11_1745_next",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1745_NEXT_TARGET.csv",
            "needles": ["NEXT1745_0_primary", "screened-tail-derivative-law-or-finite-transition-wall-bound"],
            "role": "selected screened-tail derivative law next target",
        },
        {
            "source_id": "SRC2603_12_1741_R10_status",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1741_R10_CURVE_STATUS.csv",
            "needles": ["R10CURVE1741_0", "PLACEHOLDER_NONCLAIM"],
            "role": "R10 curve still placeholder; held parallel",
        },
    ]
    rows: list[dict[str, Any]] = []
    for spec in specs:
        missing_needles = path_has_needles(spec["source_path"], spec["needles"])
        rows.append(
            with_stamp(
                {
                    "source_id": spec["source_id"],
                    "source_path": spec["source_path"],
                    "exists": spec["source_path"].exists(),
                    "missing_needles": missing_needles,
                    "source_pass": spec["source_path"].exists() and not missing_needles,
                    "role": spec["role"],
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def lineage_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "step_id": "LIN2603_0_2602",
            "checkpoint": "2602",
            "question": "What is missing after the b_g to gamma bridge?",
            "result": "s_X=b_g,X x_U profile coefficient or real R10 curve",
            "status": "HANDOFF_REBASED",
            "next_dependency": "sigmaX profile coefficient",
        },
        {
            "step_id": "LIN2603_1_1742",
            "checkpoint": "1742",
            "question": "Can s_X be scored?",
            "result": "contract staged; b_g value and x_U profile missing; R10 curve placeholder",
            "status": "PROFILE_CONTRACT_NONCLAIM",
            "next_dependency": "weak-field source/profile row",
        },
        {
            "step_id": "LIN2603_2_1743",
            "checkpoint": "1743",
            "question": "Can x_U be derived from weak-field shape?",
            "result": "source-backed formula shape and screened scaling shape staged; projectors, units, support powers and Khat missing",
            "status": "PROFILE_SHAPE_SOURCE_BACKED_NUMERIC_MISSING",
            "next_dependency": "support powers or Khat scalar subtraction",
        },
        {
            "step_id": "LIN2603_3_1744",
            "checkpoint": "1744",
            "question": "Can support powers promote x_U?",
            "result": "pS conditional only; pL/pT double zeros, pB/pK and Khat scalar profile remain unsigned",
            "status": "XU_NOT_PROMOTED",
            "next_dependency": "fixed-point double zero or DeltaK component",
        },
        {
            "step_id": "LIN2603_4_1745",
            "checkpoint": "1745",
            "question": "Do pL/pT double zeros give gradient suppression?",
            "result": "amplitude double-zero is conditional, but q_loc sees gradients; screened-tail derivative law is required",
            "status": "TAIL_DERIVATIVE_LAW_REQUIRED",
            "next_dependency": "screened-tail derivative law or transition-wall bound",
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False, "claim_allowed": False}) for row in rows]


def profile_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "PG2603_0_sigma_contract",
            "object": "s_X=b_g,X x_U",
            "current_status": "CONTRACT_STAGED_VALUE_MISSING",
            "blocking_gap": "MISSING_BG_VALUE;MISSING_X_U_PROFILE;MISSING_SOURCE_NORMALIZATION;MISSING_NO_OTHER_CHANNELS",
            "effect": "Cassini gamma bridge remains nonclaim",
        },
        {
            "gate_id": "PG2603_1_weak_field_shape",
            "object": "S_X weak-field source shape",
            "current_status": "FORMULA_SHAPE_SOURCE_BACKED_INPUTS_MISSING",
            "blocking_gap": "MISSING_PROJECTORS;MISSING_UNITS;MISSING_KHAT_PROFILE;MISSING_SUPPORT_DOMAIN",
            "effect": "x_U can be targeted but not scored",
        },
        {
            "gate_id": "PG2603_2_support_powers",
            "object": "pS,pL,pT,pB,pK",
            "current_status": "PS_CONDITIONAL_PL_PT_PB_PK_UNSIGNED",
            "blocking_gap": "MISSING_PL_PT_DOUBLE_ZERO_GRADIENT_LAW;MISSING_BOUNDARY_POWER;MISSING_TENSOR_CONTROL",
            "effect": "screened scaling cannot promote x_U",
        },
        {
            "gate_id": "PG2603_3_Khat_subtraction",
            "object": "S_Delta=-Pi_gamma[P_loc div Delta_K]",
            "current_status": "SCHEMA_WRITTEN_COMPONENTS_MISSING",
            "blocking_gap": "MISSING_DELTAK_COMPONENTS;MISSING_PROJECTORS;MISSING_OPERATOR_NORMS;MISSING_UNITS",
            "effect": "retained DeltaK/Khat channel blocks PPN scoring",
        },
        {
            "gate_id": "PG2603_4_R10_curve",
            "object": "R10 alpha(lambda) curve",
            "current_status": "PLACEHOLDER_NONCLAIM",
            "blocking_gap": "MISSING_DIGITIZED_ALPHA_BOUND;MISSING_NUMERIC_LAMBDA;MISSING_ALPHA_PREDICTION",
            "effect": "R10 route remains held parallel",
        },
    ]
    return [with_stamp({**row, "score_ready": False, "valid_for_claim": False, "claim_allowed": False}) for row in rows]


def tail_law_bridge_rows() -> list[dict[str, Any]]:
    source_paths = [
        OUT / "P8_Y5_PARENT_QLOC_1742_SIGMAX_PROFILE_CONTRACT.csv",
        OUT / "P8_Y5_PARENT_QLOC_1743_WEAK_FIELD_PROFILE_FIRST_ROW.csv",
        OUT / "P8_Y5_PARENT_QLOC_1744_SUPPORT_POWER_GATE.csv",
        OUT / "P8_Y5_PARENT_QLOC_1744_KHAT_SCALAR_PROFILE_ROW.csv",
        OUT / "P8_Y5_PARENT_QLOC_1745_GRADIENT_TAIL_GATE.csv",
        OUT / "P8_Y5_PARENT_QLOC_1745_DELTAK_COMPONENT_ROW.csv",
    ]
    rows = [
        {
            "row_id": "TLB2603_0_sX",
            "symbol": "s_X",
            "formula": "s_X=b_g,X x_U",
            "current_status": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "missing_inputs": "MISSING_BG_VALUE;MISSING_X_U_PROFILE;MISSING_NO_OTHER_CHANNELS",
            "next_owner": "weak-field profile/tail law",
        },
        {
            "row_id": "TLB2603_1_xU_shape",
            "symbol": "x_U",
            "formula": "x_U=O(U_B^(2pS),U_B^pL,U_B^pT) times operator/support constants",
            "current_status": "SCALING_SHAPE_SOURCE_BACKED_POWERS_MISSING",
            "missing_inputs": "MISSING_UB;MISSING_PL_PT_GRADIENT_POWER;MISSING_OPERATOR_CONSTANTS;MISSING_BOUNDARY_DECAY",
            "next_owner": "support powers and screened-tail derivative law",
        },
        {
            "row_id": "TLB2603_2_tail_derivative",
            "symbol": "tail_derivative_law",
            "formula": "|nabla Z_L|<=C_Zgrad U_B/L_tr or |nabla U_B|<=C_U U_B/L_tr",
            "current_status": "BLOCKED_TAIL_LAW_MISSING",
            "missing_inputs": "MISSING_PARENT_LOCAL_OPERATOR;MISSING_ASYMPTOTIC_TAIL;MISSING_TRANSITION_PROFILE;MISSING_GRADIENT_CONTROL",
            "next_owner": "2604 screened-tail derivative law",
        },
        {
            "row_id": "TLB2603_3_transition_wall",
            "symbol": "transition_wall_bound",
            "formula": "finite bound for local support intersecting sharp transition region",
            "current_status": "FALLBACK_REQUIRED_IF_TAIL_LAW_FAILS",
            "missing_inputs": "MISSING_SUPPORT_DOMAIN;MISSING_WALL_WIDTH;MISSING_PROFILE_AMPLITUDE;MISSING_LOCAL_BOUND_PROJECTION",
            "next_owner": "finite transition-wall residual",
        },
        {
            "row_id": "TLB2603_4_DeltaK",
            "symbol": "S_Delta",
            "formula": "S_Delta^nu=-Pi_gamma[P_loc nabla_mu Delta_K^{mu nu}]",
            "current_status": "PROJECTION_SCHEMA_WRITTEN_NOT_LIVE",
            "missing_inputs": "MISSING_PIGAMMA_OPERATOR;MISSING_PLOC;MISSING_COMPONENTS;MISSING_UNITS",
            "next_owner": "DeltaK component/operator norm fallback",
        },
    ]
    return [
        with_stamp(
            {
                **row,
                "source_paths": source_paths,
                "source_paths_exist": all(path.exists() for path in source_paths),
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        for row in rows
    ]


def runner_refusal_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "runner_id": "RUN2603_0_gamma_score",
            "target": "sigmaX to Cassini gamma score",
            "verdict": "REFUSE_CLAIM_RUN",
            "failure_reasons": "MISSING_SX_VALUE;MISSING_XU_PROFILE;MISSING_BG_VALUE;MISSING_NO_OTHER_CHANNELS",
        },
        {
            "runner_id": "RUN2603_1_support_power",
            "target": "x_U support-power calculator",
            "verdict": "REFUSE_CLAIM_RUN",
            "failure_reasons": "MISSING_PL_PT_GRADIENT_POWER;MISSING_PB_PK;MISSING_TAIL_DERIVATIVE_LAW;MISSING_OPERATOR_CONSTANTS",
        },
        {
            "runner_id": "RUN2603_2_Khat",
            "target": "DeltaK/Khat scalar subtraction",
            "verdict": "REFUSE_CLAIM_RUN",
            "failure_reasons": "MISSING_DELTAK_COMPONENTS;MISSING_PROJECTORS;MISSING_UNITS;MISSING_RESPONSE_LIMITS",
        },
        {
            "runner_id": "RUN2603_3_R10",
            "target": "R10 alpha(lambda) score",
            "verdict": "REFUSE_CLAIM_RUN",
            "failure_reasons": "MISSING_REAL_R10_CURVE;MISSING_ALPHA_PREDICTION",
        },
        {
            "runner_id": "RUN2603_4_local_GR",
            "target": "local GR/Newton recovery",
            "verdict": "BLOCKED_NO_CLAIM",
            "failure_reasons": "NO_SX_PROFILE;NO_TAIL_LAW;NO_DELTAK_BOUND;NO_FULL_PPN_VECTOR",
        },
    ]
    return [with_stamp({**row, "accepted_for_scoring": False, "claim_allowed": False, "valid_for_claim": False}) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "CG2603_0_profile_shape",
            "claim": "weak-field profile formula shape exists",
            "gate_status": "PASS_NONCLAIM_ONLY",
            "reason": "1743 stages source-backed S_X formula shape",
            "gate_pass": True,
        },
        {
            "gate_id": "CG2603_1_sX_score",
            "claim": "s_X profile coefficient is known",
            "gate_status": "BLOCKED_NO_CLAIM",
            "reason": "b_g, x_U, source normalization and no-other-channel proof are missing",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2603_2_tail_law",
            "claim": "screened-tail derivative gives gradient p=2",
            "gate_status": "BLOCKED_NO_CLAIM",
            "reason": "1745 shows amplitude double-zero does not control q_loc gradients without tail law",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2603_3_DeltaK",
            "claim": "DeltaK/Khat scalar subtraction is bounded or zero",
            "gate_status": "BLOCKED_NO_CLAIM",
            "reason": "DeltaK component/projector/operator norm rows are missing",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2603_4_local_GR",
            "claim": "local GR/Newton branch is derived",
            "gate_status": "BLOCKED_NO_CLAIM",
            "reason": "profile, tail, Khat and full PPN/local residual vector remain open",
            "gate_pass": False,
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False, "claim_allowed": False}) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2603_0_profile_route",
            "decision": "keep sigmaX profile route as primary",
            "reason": "1743 gives a source-backed formula shape while R10 curve remains placeholder",
            "effect": "use weak-field profile instead of pretending R10 is ready",
        },
        {
            "decision_id": "DEC2603_1_tail_law",
            "decision": "select screened-tail derivative law as next theorem",
            "reason": "1745 shows amplitude double-zero is not enough because q_loc uses gradients",
            "effect": "next target is |nabla U_B|<=C U_B/L_tr or transition-wall bound",
        },
        {
            "decision_id": "DEC2603_2_fallback",
            "decision": "retain DeltaK/Khat finite fallback",
            "reason": "Khat scalar subtraction remains a live retained source channel",
            "effect": "if tail law fails, fill DeltaK component/operator norm rows",
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False}) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2603_0_selected",
            "selection_status": "selected",
            "target_file": "2604-Y5-R2FR-screened-tail-derivative-law-or-finite-transition-wall-bound.md",
            "target_script": "scripts/Y5_R2FR_screened_tail_derivative_law_or_transition_wall_bound_2604.py",
            "task": "derive |nabla U_B|<=C U_B/L_tr from a parent local operator/tail law, or stage a finite transition-wall residual bound",
            "success_condition": "tail derivative theorem signed, or transition-wall bound rows produced with local support/domain inputs explicit",
            "fallback_condition": "keep x_U and sigmaX profile nonclaim; fill DeltaK/Khat component row if tail law fails",
            "guardrails": "no amplitude-to-gradient shortcut; no numeric gamma claim; no R10 claim from placeholder curve; no local-GR claim; no GitHub; no formalization-workbench edits",
        },
        {
            "route_id": "NEXT2603_1_DeltaK_fallback",
            "selection_status": "held_fallback",
            "target_file": "2604b-Y5-R2FR-DeltaK-component-operator-norm-bound.md",
            "target_script": "scripts/Y5_R2FR_DeltaK_component_operator_norm_bound_2604b.py",
            "task": "source the first live DeltaK component/projector/operator norm bound if tail-law derivation fails",
            "success_condition": "S_Delta rows carry sourced components, units, operator norms, and remain nonclaim until numeric/test limits exist",
            "fallback_condition": "retain DeltaK as explicit finite residual",
            "guardrails": "no Khat silence by assertion; no component deletion; no local-GR claim",
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False}) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for copy_id, target_path in COPY_TARGETS.items():
        source_path = OUTPUTS[copy_id]
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        rows.append(
            with_stamp(
                {
                    "copy_id": f"COPY2603_{copy_id}",
                    "source_path": source_path,
                    "target_path": target_path,
                    "source_exists": source_path.exists(),
                    "target_exists": target_path.exists(),
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def generated_rows_have_no_claim_flags(data: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in data.values():
        for row in rows:
            if row.get("valid_for_claim") is True or row.get("claim_allowed") is True:
                return False
            if row.get("score_ready") is True or row.get("accepted_for_scoring") is True:
                return False
    return True


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, condition: bool, notes: str, detail: str = "") -> None:
        rows.append(
            with_stamp(
                {
                    "check_id": check_id,
                    "status": "PASS" if condition else "FAIL",
                    "notes": notes,
                    "detail": detail,
                    "valid_for_claim": False,
                }
            )
        )

    add("VAL2603_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and needles are present")
    expected_lineage = {f"LIN2603_{idx}_{suffix}" for idx, suffix in enumerate(["2602", "1742", "1743", "1744", "1745"])}
    add("VAL2603_01_lineage_complete", expected_lineage == {row["step_id"] for row in data["lineage"]}, "lineage ledger covers 2602 and 1742-1745")
    expected_objects = {"s_X=b_g,X x_U", "S_X weak-field source shape", "pS,pL,pT,pB,pK", "S_Delta=-Pi_gamma[P_loc div Delta_K]", "R10 alpha(lambda) curve"}
    add("VAL2603_02_profile_gate_complete", expected_objects.issubset({row["object"] for row in data["profile_gate"]}), "profile gate covers sigma contract, weak-field shape, support powers, Khat and R10")
    expected_symbols = {"s_X", "x_U", "tail_derivative_law", "transition_wall_bound", "S_Delta"}
    add("VAL2603_03_tail_bridge_complete", expected_symbols.issubset({row["symbol"] for row in data["tail_bridge"]}), "tail-law bridge rows cover sX, xU, tail law, wall fallback and DeltaK")
    add("VAL2603_04_tail_sources_exist", all(row["source_paths_exist"] is True for row in data["tail_bridge"]), "tail bridge rows cite existing local sources")
    add("VAL2603_05_runner_refuses", all(row["accepted_for_scoring"] is False and row["claim_allowed"] is False for row in data["runner_refusal"]), "runners refuse gamma, support, Khat, R10 and local-GR claims")
    add("VAL2603_06_claim_gates_safe", all(row["claim_allowed"] is False for row in data["claim_gates"]) and any(row["gate_id"] == "CG2603_0_profile_shape" and row["gate_status"] == "PASS_NONCLAIM_ONLY" for row in data["claim_gates"]), "claim gates allow only nonclaim profile-shape result")
    add("VAL2603_07_no_claim_flags", generated_rows_have_no_claim_flags(data), "no generated row promotes scoring or claim flags")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in (
            "*2603-Y5-R2FR-sigmaX*",
            "*Y5_R2FR_sigmaX*2603*",
            "*P8_Y5_SIGMAX_PROFILE_REBASE_2603*",
            "*JR2603*",
        ):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add("VAL2603_08_no_formalization_artifacts", not formalization_artifacts, "no 2603 artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_artifacts))
    add("VAL2603_09_next_selected", any(row["route_id"] == "NEXT2603_0_selected" and "2604-Y5-R2FR-screened-tail-derivative-law" in row["target_file"] for row in data["next"]), "2604 screened-tail derivative law target selected")
    add("VAL2603_10_branch_copies", all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]), "nonclaim branch copies exist")

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2603_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2603_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2603_OVERALL",
        overall,
        "2603 rebases the sigmaX profile chain, keeps gamma/R10/local claims blocked, and selects screened-tail derivative law or transition-wall bound next",
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for row in rows:
        values = [row_value(row.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2603 Y5 R2FR sigmaX profile coefficient or real R10 curve",
        "",
        "**Status:** private nonclaim rebase checkpoint. The `s_X=b_g,X x_U` profile target selected by 2602 is preserved, and the prior 1742-1745 chain shows the live missing theorem is now a screened-tail derivative law, with DeltaK/Khat retained as fallback.",
        "",
        "**Main result:** the PPN gamma bridge is concrete but still not scoreable. `s_X=b_g,X x_U` has a source-backed response map to Cassini gamma, and the weak-field source profile shape is staged, but `x_U` still lacks support powers, projectors, units, Khat subtraction, and especially the gradient tail law. The key red-team catch survives: amplitude double-zero does not imply `q_loc` gradient suppression unless `|nabla U_B|<=C U_B/L_tr` or an equivalent screened-tail law is signed. No numeric PPN, R10, Newton, or local-GR claim is made.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role", "valid_for_claim"]),
        "",
        "## Lineage Ledger",
        markdown_table(data["lineage"], ["step_id", "checkpoint", "question", "result", "status", "next_dependency", "valid_for_claim", "claim_allowed"]),
        "",
        "## Profile Gate Status",
        markdown_table(data["profile_gate"], ["gate_id", "object", "current_status", "blocking_gap", "effect", "score_ready", "valid_for_claim", "claim_allowed"]),
        "",
        "## Tail Law Bridge",
        markdown_table(data["tail_bridge"], ["row_id", "symbol", "formula", "current_status", "missing_inputs", "next_owner", "source_paths", "source_paths_exist", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Runner Refusal",
        markdown_table(data["runner_refusal"], ["runner_id", "target", "verdict", "failure_reasons", "accepted_for_scoring", "claim_allowed", "valid_for_claim"]),
        "",
        "## Claim Gates",
        markdown_table(data["claim_gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "valid_for_claim", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect", "valid_for_claim"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "success_condition", "fallback_condition", "guardrails", "valid_for_claim"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists", "valid_for_claim"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail", "valid_for_claim"]),
        "",
        "## Practical Status",
        "",
        "This is a real sharpening. We are not stuck at 'maybe it screens'; the current claim lives or dies on a differential tail law. If the tail law closes, the `x_U` profile and Cassini bridge become much more serious. If it fails, we keep the transition-wall/DeltaK finite-residual branch and do not smuggle a local-GR pass.",
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)

    data = {
        "sources": source_register_rows(),
        "lineage": lineage_rows(),
        "profile_gate": profile_gate_rows(),
        "tail_bridge": tail_law_bridge_rows(),
        "runner_refusal": runner_refusal_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["lineage_ledger"], data["lineage"])
    write_csv(OUTPUTS["profile_gate"], data["profile_gate"])
    write_csv(OUTPUTS["tail_law_bridge"], data["tail_bridge"])
    write_csv(OUTPUTS["runner_refusal"], data["runner_refusal"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])

    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row for row in data["validations"] if row["check_id"] == "VAL2603_OVERALL")
    print(f"{overall['check_id']} {overall['status']}: {overall['notes']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
