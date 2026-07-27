from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1745"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1745 - Fixed Point Double Zero For pL pT Or DeltaK Component Row"
UTC = datetime.now(timezone.utc).isoformat()


def yesno(value: bool) -> str:
    return "True" if value else "False"


def no() -> str:
    return "False"


SOURCES = [
    {
        "source_id": "SRC1745_0_1744_doc",
        "source_key": "1744_handoff",
        "source_path": ROOT / "1744-Y5-R2FR-support-powers-pS-pL-pT-or-Khat-scalar-profile.md",
        "needles": ["NEXT1744_0_primary", "DEC1744_3_best_next_domino"],
    },
    {
        "source_id": "SRC1745_1_1744_support_gate",
        "source_key": "1744_support_power_gate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1744_SUPPORT_POWER_GATE.csv",
        "needles": ["SP1744_1_pL", "TRACE_DOUBLE_ZERO_NOT_DERIVED"],
    },
    {
        "source_id": "SRC1745_2_800_support_audit",
        "source_key": "800_support_power_derivation",
        "source_path": RESIDUALS / "P8_Y5_R10_800_SUPPORT_POWER_DERIVATION_AUDIT.csv",
        "needles": ["SPD800_1_pL_generic", "SPD800_2_pT_generic"],
    },
    {
        "source_id": "SRC1745_3_801_double_zero",
        "source_key": "801_ZL_norm_evenness_theorem",
        "source_path": ROOT / "801-Y5-R10-double-zero-fixed-point-parent-mechanism-or-local-branch-closure-ledger.md",
        "needles": ["DZ801_1_norm_evenness", "gradient_gate_still_open"],
    },
    {
        "source_id": "SRC1745_4_1291_strict_clause",
        "source_key": "1291_strict_double_zero_clause",
        "source_path": ROOT / "1291-Y5-R10-RAB-strict-double-zero-parent-clause-or-chain-kernel-residual-bound.md",
        "needles": ["F(m)=(m-m_*)^2 H(m)", "VP1291_2_gradient_variation"],
    },
    {
        "source_id": "SRC1745_5_1533_locking",
        "source_key": "1533_locking_guard",
        "source_path": ROOT / "1533-Y5-vacuum-subtracted-stationary-source-double-zero-contract.md",
        "needles": ["VAC1533_6_verdict", "NEXT_LOCKING_GATE"],
    },
    {
        "source_id": "SRC1745_6_1287_Khat_component",
        "source_key": "1287_Khat_component",
        "source_path": RESIDUALS / "P8_Y5_R10_1287_FIRST_KHAT_COMPONENT_ROW_NONCLAIM.csv",
        "needles": ["KTC1287_0_flat_Ricci_scalar_KL00", "valid_for_claim"],
    },
    {
        "source_id": "SRC1745_7_1289_DeltaK_template",
        "source_key": "1289_DeltaK00_template",
        "source_path": RESIDUALS / "P8_Y5_R10_1289_DELTAK00_COMPARISON_TEMPLATE.csv",
        "needles": ["DTC1289_2_DeltaK00_template", "MISSING_FULL_KMETRIC"],
    },
    {
        "source_id": "SRC1745_8_1367_Kmetric_kernel",
        "source_key": "1367_Kmetric_chain_kernel",
        "source_path": RESIDUALS / "P8_Y5_R10_1367_KMETRIC_CHAIN_KERNEL_ATTEMPT.csv",
        "needles": ["KER1367_5_DeltaK00_template", "KERNELS_NOT_COMPUTABLE_CURRENTLY"],
    },
    {
        "source_id": "SRC1745_9_1523_Pigamma",
        "source_key": "1523_Pigamma_projector",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1523_PIGAMMA_PROJECTOR_LEDGER.csv",
        "needles": ["PIG1523_1_scalar_channel_map", "PIGAMMA_NOT_PROMOTED"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1745_SOURCE_REGISTER.csv",
    "fixed_point_theorem": RESIDUALS / "P8_Y5_PARENT_QLOC_1745_FIXED_POINT_DOUBLE_ZERO_THEOREM.csv",
    "gradient_tail_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1745_GRADIENT_TAIL_GATE.csv",
    "pL_pT_status": RESIDUALS / "P8_Y5_PARENT_QLOC_1745_PL_PT_STATUS.csv",
    "deltak_component": RESIDUALS / "P8_Y5_PARENT_QLOC_1745_DELTAK_COMPONENT_ROW.csv",
    "runner_refusal": RESIDUALS / "P8_Y5_PARENT_QLOC_1745_RUNNER_REFUSAL.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1745_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1745_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1745_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1745_VALIDATION.csv",
}


COPY_MAP = {
    "fixed_point_theorem": "R2FR_1745_FIXED_POINT_DOUBLE_ZERO_THEOREM.csv",
    "gradient_tail_gate": "R2FR_1745_GRADIENT_TAIL_GATE.csv",
    "pL_pT_status": "R2FR_1745_PL_PT_STATUS.csv",
    "deltak_component": "R2FR_1745_DELTAK_COMPONENT_ROW.csv",
    "runner_refusal": "R2FR_1745_RUNNER_REFUSAL.csv",
    "decision": "R2FR_1745_DECISION_LEDGER.csv",
    "claim_gate": "R2FR_1745_CLAIM_GATE.csv",
    "next_target": "R2FR_1745_NEXT_TARGET.csv",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def source_rows() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCES:
        path = source["source_path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": yesno(exists),
                "needles": ";".join(needles),
                "needles_present": yesno(exists and all(needle in text for needle in needles)),
                "checked_utc": UTC,
            }
        )
    return rows


def fixed_point_theorem_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "theorem_id": "FZD1745_0_generic_linear_countermodel",
            "claim": "generic smooth local readout gives p=1, not p=2",
            "assumptions": "f(Z_L)=a_A Z_L^A+O(||Z_L||^2), Z_L=O(U_B)",
            "derivation": "unless a_A=0, f=O(U_B) and nabla f generically has a first-order term",
            "result": "double_zero_not_generic",
            "status": "NO_GO_GUARD",
            "missing_to_promote": "MISSING_PARENT_EVENNESS_OR_ZERO_LINEAR_COVECTOR",
        },
        {
            "theorem_id": "FZD1745_1_norm_square_amplitude",
            "claim": "norm-only scalar readout gives quadratic amplitude",
            "assumptions": "R_L=G_AB Z_L^A Z_L^B; f=F(R_L); F(0)=0; F smooth; ||Z_L||<=C_Z U_B",
            "derivation": "F(R_L)=F_prime(0)R_L+O(R_L^2), so |f|<=C_f U_B^2+O(U_B^4)",
            "result": "amplitude_p2_conditional_theorem",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "missing_to_promote": "MISSING_PARENT_ZL_MAP;MISSING_PARENT_GAB;MISSING_EVENNESS_SYMMETRY;MISSING_U_B_BOUND",
        },
        {
            "theorem_id": "FZD1745_2_gradient_tail_requirement",
            "claim": "gradient p=2 needs a screened-tail derivative law, not amplitude double-zero alone",
            "assumptions": "|nabla Z_L|<=C_grad U_B/L_tr and bounded nabla G_AB",
            "derivation": "nabla f=F_prime(R_L)nabla R_L and nabla R_L=O(Z_L nabla Z_L)=O(U_B^2/L_tr)",
            "result": "gradient_p2_if_tail_law_signed",
            "status": "EXACT_CONDITIONAL_THEOREM_INPUT_MISSING",
            "missing_to_promote": "MISSING_SCREENED_TAIL_DERIVATIVE_LAW;MISSING_TRANSITION_PROFILE;MISSING_GRADIENT_CONTROL",
        },
        {
            "theorem_id": "FZD1745_3_transition_wall_countermodel",
            "claim": "a sharp transition profile can destroy p=2 gradients",
            "assumptions": "Z_L=U_B H_L, H_L bounded, but |nabla U_B|=O(1/L_tr)",
            "derivation": "nabla f=O(U_B/L_tr), so the q_loc gradient source is only first order even though f=O(U_B^2)",
            "result": "amplitude_p2_gradient_p1_countermodel",
            "status": "NO_GO_GUARD",
            "missing_to_promote": "MISSING_NO_SHARP_WALL_OR_TAIL_EIGENMODE_PROOF",
        },
        {
            "theorem_id": "FZD1745_4_pL_pT_verdict",
            "claim": "pL=pT=2 is derivable only as a two-part theorem",
            "assumptions": "norm-square/even readouts plus screened-tail derivative law",
            "derivation": "amplitude double zero supplies f=O(U_B^2); tail derivative supplies nabla f=O(U_B^2/L_tr)",
            "result": "best_route_identified_not_parent_signed",
            "status": "THEOREM_SHAPE_ADVANCES_NONCLAIM",
            "missing_to_promote": "MISSING_PARENT_SIGNATURES_AND_TAIL_LAW",
        },
    ]
    for row in rows:
        row.update(
            {
                "branch_id": BRANCH_ID,
                "valid_for_claim": no(),
                "claim_allowed": no(),
                "score_ready": no(),
            }
        )
    return rows


def gradient_tail_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GT1745_0_ZL_parent_map",
            "requirement": "parent-owned leakage vector Z_L^A and fixed surface Sigma_L={Z_L=0}",
            "needed_formula": "Z_L=q_local_leak(Phi), not an arena label or fitted switch",
            "current_status": "BLOCKED_PARENT_MAP_UNSIGNED",
            "effect": "without Z_L, norm-square theorem is closure-only",
        },
        {
            "gate_id": "GT1745_1_norm_evenness",
            "requirement": "scalar readouts depend on R_L=G_AB Z_L^A Z_L^B only",
            "needed_formula": "m_L-m_*=M(R_L), T_L=L_cg^-2F_L-Lambda_loc=T(R_L)",
            "current_status": "BLOCKED_EVENNESS_UNSIGNED",
            "effect": "linear covector a_A Z_L^A remains legal and p=1 returns",
        },
        {
            "gate_id": "GT1745_2_tail_derivative",
            "requirement": "screened local tail derivative law",
            "needed_formula": "|nabla Z_L|<=C_Zgrad U_B/L_tr or |nabla U_B|<=C_U U_B/L_tr with bounded H_L",
            "current_status": "BLOCKED_TAIL_LAW_MISSING",
            "effect": "amplitude p=2 does not imply gradient p=2 for q_loc",
        },
        {
            "gate_id": "GT1745_3_transition_width",
            "requirement": "transition layer cannot sit inside local PPN/clock/orbital support with sharp |nabla U_B|",
            "needed_formula": "local test support lies in asymptotic screened tail or transition contribution is separately bounded",
            "current_status": "BLOCKED_SUPPORT_DOMAIN_MISSING",
            "effect": "wall gradients can dominate the local source profile",
        },
        {
            "gate_id": "GT1745_4_Kperp_separate",
            "requirement": "tensor/transverse Kperp is zero, suppressed, or bounded independently",
            "needed_formula": "L_T K_perp=S_perp with coercive operator/no zero mode/boundary data, or explicit response bound",
            "current_status": "BLOCKED_TENSOR_GATE_UNTOUCHED",
            "effect": "scalar pL/pT theorem cannot by itself prove local GR/PPN",
        },
    ]
    for row in rows:
        row.update(
            {
                "branch_id": BRANCH_ID,
                "valid_for_claim": no(),
                "claim_allowed": no(),
                "score_ready": no(),
            }
        )
    return rows


def pl_pt_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "status_id": "PLPT1745_0_amplitude",
            "quantity": "m_L-m_* and trace baseline amplitude",
            "candidate_power": "2",
            "status": "CONDITIONAL_THEOREM_FROM_NORM_SQUARE",
            "why": "norm/even scalar readout gives quadratic amplitude if parent signatures are signed",
            "missing_to_promote": "MISSING_PARENT_ZL_GAB_EVENNESS",
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_ready": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "PLPT1745_1_gradient",
            "quantity": "nabla m_L and nabla trace baseline entering q_loc",
            "candidate_power": "2_if_tail_law_else_1",
            "status": "BLOCKED_BY_SCREENED_TAIL_DERIVATIVE_LAW",
            "why": "q_loc uses gradients; amplitude double-zero alone permits a transition-wall p=1 gradient",
            "missing_to_promote": "MISSING_SCREENED_TAIL_DERIVATIVE_LAW",
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_ready": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "PLPT1745_2_local_branch",
            "quantity": "local PPN/Newton branch",
            "candidate_power": "not_promoted",
            "status": "LOCAL_GR_CLAIM_BLOCKED",
            "why": "pL/pT, Kperp, DeltaK, projector, boundary and response gates are not all signed",
            "missing_to_promote": "MISSING_ALL_LOCAL_GATES",
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_ready": no(),
        },
    ]


def deltak_component_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "component_id": "DKC1745_0_DeltaK00_template",
            "quantity": "Delta_K^{00}",
            "formula": "Delta_K^{00}=K_L^{00}-[Kmetric_volume^{00}+Kmetric_chain^{00}+K_conn^{00}+K_domain^{00}+K_boundary^{00}]",
            "source_anchor": "DTC1289_2_DeltaK00_template;KER1367_5_DeltaK00_template",
            "status": "TEMPLATE_SOURCE_BACKED_NOT_COMPUTABLE",
            "needed_to_promote": "MISSING_CURRENT_KHAT_MATCH;MISSING_FULL_KMETRIC;MISSING_BOUNDARY_AND_RESPONSE_LIMITS",
            "value_or_formula": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_ready": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "DKC1745_1_scalar_projection",
            "quantity": "S_Delta",
            "formula": "S_Delta^nu=-Pi_gamma[P_loc nabla_mu Delta_K^{mu nu}]",
            "source_anchor": "PIG1523_1_scalar_channel_map;KDS1524_3_scalar_DeltaK_channel",
            "status": "PROJECTION_SCHEMA_WRITTEN_NOT_LIVE",
            "needed_to_promote": "MISSING_PIGAMMA_OPERATOR;MISSING_PLOC;MISSING_COMPONENTS;MISSING_UNITS",
            "value_or_formula": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_ready": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "DKC1745_2_bound_form",
            "quantity": "||S_Delta||",
            "formula": "||S_Delta|| <= C_Pi C_loc (||nabla K_L||+||nabla Kmetric_volume||+||nabla R_chain||+||nabla K_cdb||)",
            "source_anchor": "KDS1524_4_total_scalar_source;KRB1291_3_residual_verdict",
            "status": "BOUND_FORM_ONLY_NONCLAIM",
            "needed_to_promote": "MISSING_OPERATOR_NORMS;MISSING_COMPONENT_BOUNDS;MISSING_RESPONSE_LIMITS",
            "value_or_formula": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_ready": no(),
        },
    ]


def runner_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1745_0_support_power_calculator",
            "runner": "x_U support-power calculator",
            "current_status": "REFUSE_CLAIM_RUN",
            "reason": "pL/pT gradient p=2 requires parent signatures plus screened-tail derivative law",
            "claim_allowed": no(),
            "score_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1745_1_DeltaK_component_runner",
            "runner": "DeltaK scalar component profile",
            "current_status": "REFUSE_CLAIM_RUN",
            "reason": "DeltaK rows are formula/bound forms only with missing projectors, components, units and response limits",
            "claim_allowed": no(),
            "score_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1745_2_PPN_gamma_runner",
            "runner": "Cassini/PPN gamma response",
            "current_status": "REFUSE_CLAIM_RUN",
            "reason": "sigma_X/x_U remains nonnumeric and Khat/DeltaK channels are retained",
            "claim_allowed": no(),
            "score_allowed": no(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1745_0_double_zero_result",
            "decision": "AMPLITUDE_DOUBLE_ZERO_DERIVED_CONDITIONALLY",
            "reason": "norm-square/even readout proves quadratic amplitude if parent-owned",
            "next_action": "do not promote to q_loc gradient suppression until tail derivative law is signed",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1745_1_gradient_result",
            "decision": "TAIL_DERIVATIVE_LAW_IS_NEXT_DOMINO",
            "reason": "q_loc sees gradients, and transition-wall countermodel reduces p=2 amplitude to p=1 gradient",
            "next_action": "attempt to derive |nabla U_B|<=C U_B/L_tr from local positive operator/asymptotic tail",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1745_2_fallback",
            "decision": "DELTAK_COMPONENT_BOUND_ROW_STAGED",
            "reason": "if tail law fails, retained DeltaK/Khat channel must be bounded rather than erased",
            "next_action": "fill operator/source pieces for S_Delta or keep claim runners blocked",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    claims = [
        ("GATE1745_0_pL_pT_amplitude", "pL/pT amplitude double-zero theorem is parent-signed", "BLOCKED_PARENT_SIGNATURES"),
        ("GATE1745_1_pL_pT_gradient", "pL/pT gradient power reaches 2 for q_loc source", "BLOCKED_TAIL_DERIVATIVE_LAW"),
        ("GATE1745_2_DeltaK", "DeltaK/Khat scalar channel is zero or bounded", "BLOCKED_COMPONENTS_PROJECTORS_UNITS"),
        ("GATE1745_3_PPN", "PPN/Newton/local GR recovery is claimable", "BLOCKED_RESIDUAL_VECTOR_INCOMPLETE"),
        ("GATE1745_4_R10_WEP_clock_orbital", "local empirical tests can be scored", "BLOCKED_NONNUMERIC_NONCLAIM_INPUTS"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": blocker,
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_ready": no(),
        }
        for gate_id, claim, blocker in claims
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1745_0_primary",
            "next_target": "1746-Y5-R2FR-screened-tail-derivative-law-or-finite-transition-wall-bound.md",
            "script": "scripts/Y5_R2FR_screened_tail_derivative_law_or_transition_wall_bound.py",
            "objective": "derive |nabla U_B|<=C U_B/L_tr from a parent local operator/tail law, or stage a finite transition-wall residual bound",
            "success_condition": "tail derivative theorem signed, or transition-wall bound rows produced with local support/domain inputs explicit",
            "selection_status": "selected",
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1745_1_DeltaK_components",
            "next_target": "1746b-Y5-R2FR-DeltaK-component-operator-norm-bound.md",
            "script": "scripts/Y5_R2FR_DeltaK_component_operator_norm_bound.py",
            "objective": "source the first live DeltaK component/projector/operator norm bound if tail-law derivation fails",
            "success_condition": "S_Delta rows carry sourced components, units, operator norms, and remain nonclaim until numeric/test limits exist",
            "selection_status": "held_fallback",
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_allowed": no(),
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_rows(),
        "fixed_point_theorem": fixed_point_theorem_rows(),
        "gradient_tail_gate": gradient_tail_gate_rows(),
        "pL_pT_status": pl_pt_status_rows(),
        "deltak_component": deltak_component_rows(),
        "runner_refusal": runner_refusal_rows(),
        "decision": decision_rows(),
        "claim_gate": claim_gate_rows(),
        "next_target": next_target_rows(),
    }


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    def cell(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "\\|")

    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def cleanup_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def copy_outputs() -> None:
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1745_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1745_{key.upper()}.csv")


def generated_csv_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    flag_fields = {
        "claim_allowed",
        "gate_pass",
        "score_allowed",
        "score_ready",
        "valid_for_claim",
        "valid_prediction_row",
    }
    for rows in rows_map.values():
        for row in rows:
            for key, value in row.items():
                if key in flag_fields and str(value).lower() != "false":
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    readiness = {
        "claim_allowed",
        "gate_pass",
        "score_ready",
        "valid_for_claim",
        "valid_prediction_row",
    }
    for rows in rows_map.values():
        for row in rows:
            contains_missing = any("MISSING_" in str(value) for value in row.values())
            if contains_missing and any(str(row.get(flag, "")).lower() == "true" for flag in readiness):
                return False
    return True


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1745_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1745_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1745*"):
        path_text = str(path)
        if "\\.venv\\" in path_text or "\\__pycache__\\" in path_text:
            continue
        if path.is_file():
            return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    def check(check_id: str, result: bool, detail_pass: str, detail_fail: str) -> dict[str, Any]:
        return {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail_pass if result else detail_fail,
        }

    parsed_ok = True
    try:
        for path in generated_csv_paths():
            read_csv(path)
    except Exception:
        parsed_ok = False

    source_register = rows_map["source_register"]
    theorem = rows_map["fixed_point_theorem"]
    tail = rows_map["gradient_tail_gate"]
    status_rows = rows_map["pL_pT_status"]
    deltak = rows_map["deltak_component"]
    runner = rows_map["runner_refusal"]
    decision = rows_map["decision"]
    claim_rows = rows_map["claim_gate"]
    next_rows = rows_map["next_target"]

    validation = [
        check("VAL1745_0_sources_exist", all(row["exists"] == "True" for row in source_register), "all cited source paths exist", "one or more cited source paths missing"),
        check("VAL1745_1_needles_present", all(row["needles_present"] == "True" for row in source_register), "required source needles are present", "one or more required source needles missing"),
        check("VAL1745_2_generic_countermodel", any(row["theorem_id"] == "FZD1745_0_generic_linear_countermodel" and row["status"] == "NO_GO_GUARD" for row in theorem), "generic p=1 countermodel recorded", "generic p=1 countermodel missing"),
        check("VAL1745_3_amplitude_theorem", any(row["theorem_id"] == "FZD1745_1_norm_square_amplitude" and row["result"] == "amplitude_p2_conditional_theorem" for row in theorem), "norm-square amplitude theorem written", "norm-square amplitude theorem missing"),
        check("VAL1745_4_gradient_tail_gate", any(row["theorem_id"] == "FZD1745_2_gradient_tail_requirement" and row["status"] == "EXACT_CONDITIONAL_THEOREM_INPUT_MISSING" for row in theorem), "gradient p=2 tail-law gate is explicit", "gradient tail-law gate missing"),
        check("VAL1745_5_transition_wall_guard", any(row["theorem_id"] == "FZD1745_3_transition_wall_countermodel" for row in theorem), "transition-wall p=1 guard recorded", "transition-wall guard missing"),
        check("VAL1745_6_tail_requirements_blocked", all(row["current_status"].startswith("BLOCKED") for row in tail), "tail/signature gates remain blocked", "one or more tail gates unexpectedly opened"),
        check("VAL1745_7_pL_pT_not_promoted", all(row["claim_allowed"] == "False" and row["score_ready"] == "False" for row in status_rows), "pL/pT rows remain nonclaim", "pL/pT row became claim-ready"),
        check("VAL1745_8_DeltaK_fallback_present", any(row["component_id"] == "DKC1745_0_DeltaK00_template" for row in deltak) and all(row["valid_for_claim"] == "False" for row in deltak), "DeltaK component fallback rows written and nonclaim", "DeltaK fallback missing or promoted"),
        check("VAL1745_9_runners_refuse", all(row["current_status"] == "REFUSE_CLAIM_RUN" and row["claim_allowed"] == "False" for row in runner), "all claim runners refuse", "one or more runners opened a claim"),
        check("VAL1745_10_decision_next_domino", any(row["decision_id"] == "DEC1745_1_gradient_result" and row["decision"] == "TAIL_DERIVATIVE_LAW_IS_NEXT_DOMINO" for row in decision), "decision selects screened-tail derivative law", "decision did not select tail derivative law"),
        check("VAL1745_11_claim_gates_safe", all(row["gate_pass"] == "False" and row["claim_allowed"] == "False" for row in claim_rows), "all claim gates keep local claims false", "one or more claim gates opened"),
        check("VAL1745_12_no_claim_flags", no_claim_flags(rows_map), "all generated rows keep claim/no-score flags false", "one or more generated flags enabled a claim"),
        check("VAL1745_13_missing_not_ready", missing_rows_not_ready(rows_map), "no row containing MISSING_* is marked claim-ready or score-ready", "a missing row is marked ready"),
        check("VAL1745_14_next_selected", any(row["route_id"] == "NEXT1745_0_primary" and row["selection_status"] == "selected" for row in next_rows), "next target selects screened-tail derivative law", "next target missing selected primary route"),
        check("VAL1745_15_csv_parse", parsed_ok, "all generated 1745 CSVs parse", "one or more generated 1745 CSVs failed to parse"),
        check("VAL1745_16_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "one or more branch/quarantine/queue copies missing"),
        check("VAL1745_17_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check("VAL1745_18_formalization_untouched", formalization_untouched(), "no 1745 outputs found under formalization-workbench", "1745 output leaked into formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1745_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1745 fixed-point double-zero or DeltaK component validation" if overall else "one or more 1745 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- The scalar double-zero idea is mathematically real: norm-square/even readouts give quadratic **amplitudes** for `m_L-m_*` and the trace baseline.",
        "- The catch is sharp: `q_loc` uses gradients, so amplitude double-zero does **not** prove `pL=pT=2` unless the screened local tail also satisfies `|nabla Z_L|=O(U_B/L_tr)`.",
        "- A transition-wall countermodel remains live: `f=O(U_B^2)` but `nabla f=O(U_B/L_tr)` if `|nabla U_B|=O(1/L_tr)`.",
        "- Therefore the next derivation target is the screened-tail derivative law; if it fails, the honest route is a finite transition-wall/DeltaK residual bound.",
        "- No local-GR, Newton, PPN, WEP, clock, orbital, R10, or `q_loc=0` claim is made.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Fixed-Point Double-Zero Theorem",
        markdown_table(rows_map["fixed_point_theorem"], ["theorem_id", "claim", "result", "status", "missing_to_promote"]),
        "",
        "## Gradient Tail Gates",
        markdown_table(rows_map["gradient_tail_gate"], ["gate_id", "requirement", "needed_formula", "current_status", "effect"]),
        "",
        "## pL pT Status",
        markdown_table(rows_map["pL_pT_status"], ["status_id", "quantity", "candidate_power", "status", "missing_to_promote"]),
        "",
        "## DeltaK Fallback Rows",
        markdown_table(rows_map["deltak_component"], ["component_id", "quantity", "formula", "status", "needed_to_promote"]),
        "",
        "## Runner Refusal",
        markdown_table(rows_map["runner_refusal"], ["runner_id", "runner", "current_status", "reason"]),
        "",
        "## Decisions",
        markdown_table(rows_map["decision"], ["decision_id", "decision", "reason", "next_action"]),
        "",
        "## Claim Gates",
        markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "status", "blocker"]),
        "",
        "## Next Target",
        markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status"]),
        "",
        "## Validation",
        markdown_table(validation_rows, ["check_id", "result", "detail"]),
        "",
        "## Working Interpretation",
        "This is a proper Grossmann move, not a retreat: the double-zero route survives, but it has been sharpened. The missing piece is no longer vague `screening`; it is the exact differential condition that makes a small local amplitude stay small after a gradient hits it. Prove the tail law and the scalar local branch becomes much more serious. Fail it, and we still have a disciplined finite residual branch instead of a hidden axiom.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    cleanup_pycache()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    doc_path = ROOT / "1745-Y5-R2FR-fixed-point-double-zero-for-pL-pT-or-DeltaK-component-row.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1745_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1745 validation FAIL")
    print("1745 validation PASS")


if __name__ == "__main__":
    main()
