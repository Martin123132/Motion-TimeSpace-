from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "2714"
BRANCH_ID = "Y5_R2FR_LAMBDA_PHI_ZERO_BOUND_OR_KHAT_ADOPTION_UNDER_AX1090_CLOSURE_2714"
START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"
LOCAL_BOUNDS = SOURCE_INTAKE / "local_bounds"
SOURCE_WEIGHT = SOURCE_INTAKE / "source-weight"
RAB_QUEUE = SOURCE_INTAKE / "rab-sector" / "acquisition-queue"
FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"

DOC_PATH = ROOT / "2714-Y5-R2FR-lambda-phi-zero-bound-or-Khat-adoption-under-AX1090-closure.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2714_SOURCE_REGISTER.csv",
    "lambda_zero_attempt": RESIDUALS / "P8_Y5_R2FR_2714_LAMBDA_PHI_ZERO_ATTEMPT.csv",
    "bound_rollforward": RESIDUALS / "P8_Y5_R2FR_2714_MULTIPLIER_BOUND_ROLLFORWARD.csv",
    "source_coupling_handoff": RESIDUALS / "P8_Y5_R2FR_2714_SOURCE_COUPLING_HANDOFF.csv",
    "khat_adoption_gate": RESIDUALS / "P8_Y5_R2FR_2714_KHAT_ADOPTION_GATE.csv",
    "weak_field_reentry": RESIDUALS / "P8_Y5_R2FR_2714_WEAK_FIELD_REENTRY_DECISION.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2714_CLAIM_GATES.csv",
    "blocker_stack": RESIDUALS / "P8_Y5_R2FR_2714_CURRENT_BLOCKER_STACK.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2714_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2714_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2714_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2714_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_bounds_gate": LOCAL_BOUNDS / "lambda_phi_zero_bound_gate_2714_NONCLAIM.csv",
    "source_weight_gate": SOURCE_WEIGHT / "Khat_adoption_lambda_gate_2714_NONCLAIM.csv",
    "rab_next": RAB_QUEUE / "JR2714_WEAK_FIELD_AUXILIARY_CONSTRAINT_NEXT.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2714_2713_HANDOFF",
        "relative_path": "2713-Y5-R2FR-KL00-phiR-improvement-or-lambda-boundary-gate-under-AX1090-closure.md",
        "required_needles": ["LPG2713_4_verdict", "DKS2713_1_Khat_adoption", "NEXT2713_0_selected", "VAL2713_OVERALL"],
        "purpose": "imports the R2FR handoff: lambda_phi zero/bound before Khat adoption",
    },
    {
        "source_id": "SRC2714_1530_BOUND_ALGEBRA",
        "relative_path": "1530-Y5-lambda-phi-bound-input-source-pass.md",
        "required_needles": ["ABC1530_3_abs_envelope", "DGS1530_5_verdict", "RUN1530_2_Khat_promotion", "VAL1530_15_overall"],
        "purpose": "imports the multiplier-stress bound algebra and delta_g S_Gamma reduction to Kmetric kernels",
    },
    {
        "source_id": "SRC2714_1539_FIRST_PAIR_INPUTS",
        "relative_path": "1539-Y5-source-support-power-and-inner-charge-input-acquisition.md",
        "required_needles": ["LEMMA1539_2_pair_no_cancellation", "LEMMA1539_3_exact_selector_payoff", "VAL1539_15_overall"],
        "purpose": "imports the four-input source/inner first-pair obstruction",
    },
    {
        "source_id": "SRC2714_1540_SELECTOR_THEOREM",
        "relative_path": "1540-Y5-parent-coupling-selector-source-silence-attempt.md",
        "required_needles": ["CSEL1540_0_candidate_theorem", "CSEL1540_6_current_verdict", "VAL1540_15_overall"],
        "purpose": "imports the conditional coupling-selector theorem and its unsigned premises",
    },
    {
        "source_id": "SRC2714_1549_SOURCE_CURRENT_UNITS",
        "relative_path": "1549-Y5-Jq-unit-dimension-and-parent-source-variation-closure.md",
        "required_needles": ["VAR1549_5_current_verdict", "UNIT1549_5_product_law", "VAL1549_14_overall"],
        "purpose": "imports the conditional source-current unit law and the missing parent q-dependence",
    },
    {
        "source_id": "SRC2714_1550_QNORM",
        "relative_path": "1550-Y5-qnorm-Cqm-dual-pairing-and-envelope-closure.md",
        "required_needles": ["DUAL1550_2_cqm_primal", "ENV1550_2_npair", "VAL1550_14_overall"],
        "purpose": "imports the same-q-norm guard for T_source_norm and C_qm",
    },
    {
        "source_id": "SRC2714_1560_WEAK_FIELD_DEMOTION",
        "relative_path": "1560-Y5-parent-weak-field-zero-condition-derivation-or-demotion.md",
        "required_needles": ["WF1560_6_verdict", "DEM1560_0_local_GR_branch", "VAL1560_OVERALL"],
        "purpose": "imports the failed current weak-field zero theorem and bounded-closure demotion",
    },
    {
        "source_id": "SRC2714_1561_MINIMAL_ANSATZ",
        "relative_path": "1561-Y5-minimal-parent-weak-field-action-ansatz-and-Euler-Ward-PPN-gate.md",
        "required_needles": ["ANS1561_A_EH_lambdaR_silent", "RUN1561_4_claim", "VAL1561_OVERALL"],
        "purpose": "imports the minimal EH + lambda_R R_AB weak-field repair ansatz",
    },
    {
        "source_id": "SRC2714_1562_LAMBDAR_GATE",
        "relative_path": "1562-Y5-lambdaR-parent-origin-zero-stress-and-first-class-constraint-test.md",
        "required_needles": ["ROUTE1562_1_second_class_auxiliary", "STR1562_5_current", "VAL1562_OVERALL"],
        "purpose": "imports lambda_R parent-origin/zero-stress failure and the auxiliary compatibility route",
    },
    {
        "source_id": "SRC2714_1568_PRIMITIVE_CONTRACT_RECHECK",
        "relative_path": "1568-Y5-RAB-parent-contract-derivation-from-MTS-primitives-or-first-live-ZR-row.md",
        "required_needles": ["PRIM1568_3_parent_contract", "RUN1568_1_primitive_contract", "VAL1568_OVERALL"],
        "purpose": "imports the failed primitive derivation of the parent protection contract and the finite residual fallback",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def as_bool(value: bool) -> str:
    return "true" if value else "false"


def path_for(relative_path: str) -> Path:
    return ROOT / relative_path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            if not reader.fieldnames:
                return False, 0, "missing_header"
            return True, len(rows), "parsed"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        cells = [str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = path_for(spec["relative_path"])
        text = read_text(path)
        needles = list(spec["required_needles"])
        found = [needle for needle in needles if needle in text]
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "source_id": spec["source_id"],
                "relative_path": spec["relative_path"],
                "absolute_path": str(path),
                "exists": as_bool(path.exists()),
                "required_needles": ";".join(needles),
                "found_needles": ";".join(found),
                "missing_needles": ";".join(missing),
                "purpose": spec["purpose"],
                "valid_for_claim": "false",
                "claim_allowed": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def lambda_zero_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "LZA2714_0_direct_boundary_zero",
            "target": "lambda_phi=0 from parent boundary/no-flux/zero-mode",
            "required_premises": "parent local domain; boundary/no-flux or Dirichlet; zero-mode reference; static elliptic branch; source-boundary matching",
            "current_evidence": "1529 and 1530 name the clauses but do not source them",
            "result": "ZERO_THEOREM_NOT_CLOSED",
            "residual_if_failed": "T_lambda_phi retained in S_total/q_loc/DeltaK",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "attempt_id": "LZA2714_1_fixed_point_shortcut",
            "target": "delta_g S_Gamma=0 from fixed-point language",
            "required_premises": "F(m_*)=F_prime(m_*)=0 plus L_cg metric silence plus hidden connection/domain/boundary silence",
            "current_evidence": "1530 rejects fixed-point-only zero because hidden Kmetric kernels remain",
            "result": "SHORTCUT_REJECTED",
            "residual_if_failed": "delta_g S_Gamma norm feeds multiplier stress bound",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "attempt_id": "LZA2714_2_coupling_selector_exact_payoff",
            "target": "S_cg_norm=0 and Q_m^H=0 from matter/source selector blindness",
            "required_premises": "matter/source action descends through q(Phi); v_m in ker(Dq); source-normalization descent; boundary charge silence",
            "current_evidence": "1540 writes the conditional theorem but marks q map, vertical generator, source norm and boundary flux unsigned",
            "result": "CONDITIONAL_ROUTE_UNSIGNED",
            "residual_if_failed": "N_pair <= U_B_max*S_cg_norm + C_inner*|Q_m^H|",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "attempt_id": "LZA2714_3_current_verdict",
            "target": "lambda_phi/Khat promotion gate",
            "required_premises": "one of lambda_phi zero theorem or score-ready finite multiplier bound",
            "current_evidence": "no zero theorem and no numeric/source-backed finite bound exist",
            "result": "KHAT_ADOPTION_STAYS_BLOCKED",
            "residual_if_failed": "DeltaK/q_loc/local-GR remain nonclaim",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
    ]


def bound_rollforward_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "MBR2714_0_epsilon_lambda_phi",
            "quantity": "epsilon_lambda_phi",
            "bound_form": "epsilon_lambda_phi <= |C_T|*(C_E*A)^2 + |C_T|*C_P*C_E*A*||delta_g S_Gamma||, A=|c_I| ||R|| + boundary_source_norm + initial_data_norm",
            "known_status": "COMPOSITE_BOUND_FORM_ONLY",
            "missing_inputs": "C_P;C_E;C_T;R_norm;boundary_source_norm;initial_data_or_static_exclusion;delta_g_SGamma_norm;observable_projection",
            "source_anchor": "1530 ABC1530_3_abs_envelope",
            "score_ready": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "bound_id": "MBR2714_1_delta_g_SGamma",
            "quantity": "||delta_g S_Gamma||",
            "bound_form": "||delta_g S_Gamma|| <= (2/3)(L_cg^-2||F'|| ||M_m|| + 2L_cg^-3||F|| ||M_L|| + ||K_conn|| + ||K_domain|| + ||K_boundary||)",
            "known_status": "REDUCED_TO_KMETRIC_KERNEL_NORMS",
            "missing_inputs": "M_m;M_L;K_conn;K_domain;K_boundary;L_cg;F;F_prime;sign_units",
            "source_anchor": "1530 DGS1530_3_norm_envelope; 1530 DGS1530_5_verdict",
            "score_ready": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "bound_id": "MBR2714_2_first_pair",
            "quantity": "N_pair",
            "bound_form": "N_pair <= U_B_max*S_cg_norm + C_inner*|Q_m^H|",
            "known_status": "CONDITIONAL_NO_CANCELLATION_SCHEMA",
            "missing_inputs": "U_B_max;S_cg_norm;C_inner;Q_mH_abs",
            "source_anchor": "1539 LEMMA1539_2_pair_no_cancellation",
            "score_ready": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "bound_id": "MBR2714_3_source_norm_pairing",
            "quantity": "T_source_norm*C_qm contribution to S_cg_norm",
            "bound_form": "S_geom_m <= 1/2*T_source_norm*C_qm using one parent q-norm E",
            "known_status": "UNIT_LEGAL_CONDITIONAL_NOT_NUMERIC",
            "missing_inputs": "parent q-dependence; q(Phi); q-norm E; Dq[v_m]; T_source_norm value; source/boundary terms",
            "source_anchor": "1549 UNIT1549_5_product_law; 1550 DUAL1550_2_cqm_primal",
            "score_ready": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
    ]


def source_coupling_handoff_rows() -> list[dict[str, Any]]:
    return [
        {
            "handoff_id": "SCH2714_0_selector_theorem",
            "object": "matter/source selector blindness",
            "payoff": "S_cg_norm=0 and Q_m^H=0",
            "current_status": "CONDITIONAL_UNSIGNED",
            "missing": "q(Phi) map; v_m in ker(Dq); source-normalization descent; boundary/excision silence",
            "best_next_use": "do not chase loose numeric bounds before trying the parent selector/auxiliary route",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "handoff_id": "SCH2714_1_qnorm_guard",
            "object": "single parent q-norm E",
            "payoff": "legal product bound T_source_norm*C_qm",
            "current_status": "CONDITIONAL_MISSING_PARENT_NORM",
            "missing": "kinetic/Hessian/regulator norm from parent q-sector action",
            "best_next_use": "keep finite branch as closure unless E is parent-owned",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "handoff_id": "SCH2714_2_primitive_contract",
            "object": "parent protection contract from MTS primitives",
            "payoff": "theorem-zero protection for finite R_AB/q_R residuals",
            "current_status": "FAILED_CURRENT_PARENT_PROOF",
            "missing": "typed parent sorts; total action image; matter descent; boundary silence; readout closure; operator exclusion",
            "best_next_use": "route through explicit weak-field ansatz/auxiliary compatibility rather than claiming primitives already derive it",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
    ]


def khat_adoption_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "KAG2714_0_lambda_phi",
            "required_condition": "lambda_phi is theorem-zero or finite bounded below all local channels",
            "current_status": "FAIL_NOT_ZERO_NOT_BOUNDED",
            "effect_on_Khat": "staged phiR Khat adoption cannot be promoted",
            "source_anchor": "2713 DKS2713_1_Khat_adoption; 1530 RUN1530_2_Khat_promotion",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "KAG2714_1_phiR_identity",
            "required_condition": "current MTS Khat explicitly adopts the trace-free phiR response with coefficient/sign/boundary convention",
            "current_status": "PASS_CONDITIONAL_SHAPE_ONLY",
            "effect_on_Khat": "explains the K_L shape but does not yet make it live",
            "source_anchor": "2713 IR2713_1; 1526 VAR1526_5_verdict",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "KAG2714_2_DeltaK",
            "required_condition": "Khat adoption plus Kmetric fallback kernels are zero/bounded",
            "current_status": "BLOCKED",
            "effect_on_Khat": "DeltaK remains retained",
            "source_anchor": "1525 KER1525_7_verdict; 2713 DKS2713_4_local_GR",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
    ]


def weak_field_reentry_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "WFR2714_0_current_weak_field_status",
            "object": "local weak-field GR/Newton branch",
            "status": "BOUNDED_CLOSURE_CONTROL_NOT_DERIVED",
            "reason": "1560 failed to derive q_R=0 and delta_beta=0 from current parent variation",
            "repair_route": "construct an explicit minimal parent weak-field action and test Euler/Ward/PPN gates",
            "source_anchor": "1560 WF1560_6_verdict; 1560 DEM1560_0_local_GR_branch",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "WFR2714_1_minimal_ansatz",
            "object": "S_EH + S_matter + int sqrt(-g) lambda_R R_AB + S_silent + S_boundary",
            "status": "BEST_CONDITIONAL_ANSATZ_NOT_ADOPTED",
            "reason": "formal q_R=0 and beta=1 route exists only if lambda_R parent origin/zero-stress and source/readout ownership close",
            "repair_route": "test lambda_R/auxiliary compatibility under AX1090 closure rather than importing EH as finished MTS",
            "source_anchor": "1561 ANS1561_A_EH_lambdaR_silent; 1561 RUN1561_4_claim",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "WFR2714_2_lambdaR_auxiliary",
            "object": "lambda_R / R_AB auxiliary compatibility",
            "status": "SECOND_CLASS_AUXILIARY_BEST_CONDITIONAL_BUT_UNSIGNED",
            "reason": "first-class route is missing brackets/generator/degree count; auxiliary route still needs parent sort, no-derivative grammar, matter, boundary and readout gates",
            "repair_route": "make the 2715 target an AX1090-aware minimal weak-field auxiliary-constraint test",
            "source_anchor": "1562 ROUTE1562_1_second_class_auxiliary; 1568 PRIM1568_3_parent_contract",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG2714_0_lambda_zero", "lambda_phi=0 theorem", "BLOCKED", "boundary/no-flux/zero-mode/source-boundary certificate missing"),
        ("CG2714_1_lambda_bound", "lambda_phi finite bound score-ready", "BLOCKED", "bound form exists but constants, Kmetric norms and observable projection are missing"),
        ("CG2714_2_Khat_adoption", "current Khat adopts phiR response", "BLOCKED", "lambda_phi gate and live adoption remain unresolved"),
        ("CG2714_3_DeltaK", "DeltaK zero or computable", "BLOCKED", "Khat adoption and Kmetric fallback kernels unresolved"),
        ("CG2714_4_source_selector", "source/coupling first-pair exact silence", "BLOCKED", "selector theorem premises unsigned"),
        ("CG2714_5_weak_field", "q_R=0 and beta=1 parent-derived", "BLOCKED", "minimal ansatz is conditional and lambda_R/auxiliary gate unsigned"),
        ("CG2714_6_local_GR", "local GR/Newton/PPN reduction", "BLOCKED_NO_CLAIM", "current status is bounded closure control, not derivation"),
        ("CG2714_7_public_or_github", "public/GitHub action", "BLOCKED", "private checkpoint only"),
    ]
    return [
        {
            "claim_gate_id": gate_id,
            "gate": gate,
            "status": status,
            "gate_passed": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "reason": reason,
            "timestamp_utc": stamp(),
        }
        for gate_id, gate, status, reason in gates
    ]


def blocker_stack_rows() -> list[dict[str, Any]]:
    blockers = [
        ("BLK2714_0_lambda_phi_zero", "lambda_phi zero theorem missing", "Khat adoption blocked", "derive parent no-flux/zero-mode certificate or retain finite bound"),
        ("BLK2714_1_lambda_phi_bound", "finite multiplier bound not score-ready", "local tests cannot use it", "source C_P/C_E/C_T/R/boundary/Kmetric/projection inputs"),
        ("BLK2714_2_kmetric_norms", "delta_g S_Gamma reduced to Kmetric kernels", "lambda_phi and DeltaK share same bottleneck", "fill or zero M_m/M_L/K_conn/K_domain/K_boundary"),
        ("BLK2714_3_source_pair", "S_cg_norm and Q_m^H not zero or numeric", "local memory leakage not bounded", "prove selector blindness or source four-input pair"),
        ("BLK2714_4_qnorm", "single parent q-norm missing", "T_source_norm*C_qm product cannot score", "derive q-sector norm from parent action"),
        ("BLK2714_5_weak_field_parent", "q_R=0/beta=1 not parent-derived", "local GR remains closure control", "test minimal weak-field auxiliary action under AX1090 closure"),
    ]
    return [
        {
            "blocker_id": blocker_id,
            "blocker": blocker,
            "effect": effect,
            "next_action": next_action,
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for blocker_id, blocker, effect, next_action in blockers
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2714_0_lambda_result",
            "decision": "Do not promote lambda_phi silence or finite bound.",
            "rationale": "the zero theorem lacks parent boundary/no-flux/zero-mode certification and the finite bound lacks constants, Kmetric norms, and observable projection",
            "next_action": "keep lambda_phi as explicit residual until those inputs exist",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2714_1_khat_result",
            "decision": "Do not promote staged Khat adoption.",
            "rationale": "the phiR identity explains the K_L shape conditionally, but the auxiliary route has unresolved multiplier stress",
            "next_action": "return to Khat only after lambda_phi or weak-field auxiliary gate moves",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2714_2_best_next",
            "decision": "Pivot the next R2FR checkpoint to the minimal weak-field auxiliary action gate.",
            "rationale": "older chain shows lambda_phi bounds reduce to the same source/coupling/norm and parent weak-field obligations; the most direct GR route is now q_R/beta parent action testing",
            "next_action": "build 2715 minimal weak-field action ansatz under AX1090 closure",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2714_3_claim_policy",
            "decision": "Keep local GR/Newton/PPN/R10/clock/orbital claims blocked.",
            "rationale": "this checkpoint improves the map of obligations; it does not prove the obligations",
            "next_action": "continue private derivation-first workflow",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2714_0_selected",
            "status": "selected_primary",
            "target_doc": "2715-Y5-R2FR-minimal-weak-field-auxiliary-action-gate-under-AX1090-closure.md",
            "target_script": "scripts/Y5_R2FR_minimal_weak_field_auxiliary_action_gate_under_AX1090_closure_2715.py",
            "purpose": "construct the AX1090-aware minimal weak-field parent ansatz with EH core, lambda_R/R_AB or auxiliary compatibility sector, source normalization, matter descent, boundary charge and beta completion, then decide whether q_R=0 and delta_beta=0 are derivable or remain bounded closure controls",
            "acceptance_condition": "one weak-field zero premise becomes parent-signed, or the exact missing clauses are promoted to explicit nonclaim residual/acquisition rows without claiming local GR",
            "forbidden_shortcuts": "import EH as MTS proof; treat lambda_R closure as derivation; ignore lambda_R/lambda_phi stress; use fitted GM/source readout; score local tests from closure controls; GitHub action; edit formalization-workbench",
            "ready_to_run": "true",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STATUS2714_0_lambda_phi",
            "topic": "lambda_phi",
            "status": "EXPLICIT_RESIDUAL_NOT_ZERO_NOT_BOUNDED",
            "meaning": "the multiplier-stress problem is now well structured but not solved",
            "next_action": "carry residual unless parent boundary theorem or source-backed bound appears",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "STATUS2714_1_Khat",
            "topic": "Khat adoption",
            "status": "STAGED_NOT_LIVE",
            "meaning": "phiR route is still valuable, but Khat cannot be promoted while lambda stress remains",
            "next_action": "wait for lambda/auxiliary gate",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "STATUS2714_2_GR",
            "topic": "local GR/Newton",
            "status": "BOUNDED_CLOSURE_CONTROL_NOT_DERIVED",
            "meaning": "the right next leap is a parent weak-field action test, not another broad audit",
            "next_action": "run 2715 weak-field auxiliary action gate",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "STATUS2714_3_private",
            "topic": "public/GitHub",
            "status": "NO_ACTION_PRIVATE",
            "meaning": "no public or GitHub work performed",
            "next_action": "continue in post-checkpoint-work",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": "BC2714_0_local_bounds",
            "source_table": "P8_Y5_R2FR_2714_MULTIPLIER_BOUND_ROLLFORWARD.csv",
            "copy_path": str(BRANCH_OUTPUTS["local_bounds_gate"]),
            "purpose": "quarantine nonclaim lambda_phi local-bound gate",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2714_1_source_weight",
            "source_table": "P8_Y5_R2FR_2714_KHAT_ADOPTION_GATE.csv",
            "copy_path": str(BRANCH_OUTPUTS["source_weight_gate"]),
            "purpose": "quarantine nonclaim Khat adoption gate",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2714_2_rab_queue",
            "source_table": "P8_Y5_R2FR_2714_NEXT_TARGET.csv",
            "copy_path": str(BRANCH_OUTPUTS["rab_next"]),
            "purpose": "queue 2715 weak-field auxiliary gate",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
    ]


def formalization_recent_change_count() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return 0
    count = 0
    threshold = START_UTC.timestamp() - 1.0
    for path in FORMALIZATION_WORKBENCH.rglob("*"):
        try:
            if path.is_file() and path.stat().st_mtime >= threshold:
                count += 1
        except OSError:
            continue
    return count


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], generated_paths: dict[str, Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(validation_id: str, passed: bool, details: str) -> None:
        rows.append(
            {
                "validation_id": validation_id,
                "passed": as_bool(passed),
                "details": details,
                "timestamp_utc": stamp(),
            }
        )

    sources = rows_by_name["source_register"]
    add("VAL2714_0_sources_exist", all(row["exists"] == "true" and row["missing_needles"] == "" for row in sources), f"sources_checked={len(sources)}")
    add(
        "VAL2714_1_lambda_zero_rejected",
        any(row["attempt_id"] == "LZA2714_3_current_verdict" and row["result"] == "KHAT_ADOPTION_STAYS_BLOCKED" for row in rows_by_name["lambda_zero_attempt"]),
        "lambda_phi zero/bound gate blocks Khat promotion",
    )
    add(
        "VAL2714_2_bound_form_nonclaim",
        any(row["bound_id"] == "MBR2714_0_epsilon_lambda_phi" and row["score_ready"] == "false" for row in rows_by_name["bound_rollforward"]),
        "multiplier bound form exists but remains non-score-ready",
    )
    add(
        "VAL2714_3_source_handoff_present",
        any(row["handoff_id"] == "SCH2714_0_selector_theorem" and row["current_status"] == "CONDITIONAL_UNSIGNED" for row in rows_by_name["source_coupling_handoff"]),
        "source/coupling selector theorem retained as unsigned route",
    )
    add(
        "VAL2714_4_Khat_staged",
        any(row["gate_id"] == "KAG2714_0_lambda_phi" and row["current_status"] == "FAIL_NOT_ZERO_NOT_BOUNDED" for row in rows_by_name["khat_adoption_gate"]),
        "Khat adoption remains staged/nonclaim",
    )
    add(
        "VAL2714_5_weak_field_next",
        any(row["row_id"] == "WFR2714_1_minimal_ansatz" and "NOT_ADOPTED" in row["status"] for row in rows_by_name["weak_field_reentry"]),
        "minimal weak-field ansatz is retained as next repair target",
    )
    add(
        "VAL2714_6_claims_blocked",
        all(row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" for row in rows_by_name["claim_gates"]),
        "all claim gates remain blocked",
    )
    add(
        "VAL2714_7_next_target_selected",
        any(row["next_id"] == "NEXT2714_0_selected" and "2715" in row["target_doc"] for row in rows_by_name["next_target"]),
        "2715 weak-field auxiliary action gate selected",
    )
    add("VAL2714_8_branch_copies_declared", len(rows_by_name["branch_copies"]) == len(BRANCH_OUTPUTS), f"branch_copy_rows={len(rows_by_name['branch_copies'])}")

    parse_ok = True
    parse_details = []
    for path in generated_paths.values():
        if path.suffix.lower() != ".csv" or path == OUTPUTS["validation"]:
            continue
        ok, row_count, detail = parse_csv(path)
        parse_ok = parse_ok and ok
        parse_details.append(f"{path.name}:{row_count}:{detail}")
    add("VAL2714_9_csv_parse", parse_ok, "; ".join(parse_details))

    add("VAL2714_10_no_formalization_outputs", not any("formalization-workbench" in str(path).lower() for path in generated_paths.values()), "no output path points into formalization-workbench")
    recent_formalization = formalization_recent_change_count()
    add("VAL2714_11_no_formalization_recent_changes", recent_formalization == 0, f"formalization_recent_changed_count={recent_formalization}")
    add("VAL2714_12_no_github_outputs", not any(".git" in str(path).lower() or "github" in str(path).lower() for path in generated_paths.values()), "no GitHub/public-output path was written")
    add(
        "VAL2714_13_nonclaim_policy",
        all(
            row.get("valid_for_claim") == "false" and row.get("claim_allowed", "false") == "false"
            for table in rows_by_name.values()
            for row in table
            if "valid_for_claim" in row
        ),
        "all generated tables keep valid_for_claim=false and claim_allowed=false",
    )

    overall = all(row["passed"] == "true" for row in rows)
    add(
        "VAL2714_OVERALL",
        overall,
        "2714 rejects lambda_phi zero/bound promotion, keeps Khat/DeltaK/local-GR nonclaim, rolls forward source/coupling/norm blockers, and selects 2715 minimal weak-field auxiliary action gate",
    )
    return rows


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2714 Y5 R2FR lambda phi zero bound or Khat adoption under AX1090 closure",
        "",
        f"**Branch:** `{BRANCH_ID}`",
        "",
        "## Private Verdict",
        "",
        "2714 tries the promised `lambda_phi` gate and does not pretend it closes. The zero route still needs parent-owned domain, boundary/no-flux, zero-mode, and source-boundary certificates. The finite-bound route is real as algebra, but it still needs constants, Kmetric kernel norms, source/coupling norms, and observable projection before it can score anything.",
        "",
        "So `Khat` adoption remains staged. The useful advance is that the obstruction is now mapped into two precise downstream gates: source/coupling/norm closure for the multiplier residual, and the minimal weak-field parent-action ansatz for `q_R=0` and `beta=1`. The next R2FR move should be the weak-field auxiliary action gate, not another broad recap.",
        "",
        "## Source Register",
        markdown_table(rows_by_name["source_register"]),
        "",
        "## Lambda Phi Zero Attempt",
        markdown_table(rows_by_name["lambda_zero_attempt"]),
        "",
        "## Multiplier Bound Rollforward",
        markdown_table(rows_by_name["bound_rollforward"]),
        "",
        "## Source Coupling Handoff",
        markdown_table(rows_by_name["source_coupling_handoff"]),
        "",
        "## Khat Adoption Gate",
        markdown_table(rows_by_name["khat_adoption_gate"]),
        "",
        "## Weak Field Reentry Decision",
        markdown_table(rows_by_name["weak_field_reentry"]),
        "",
        "## Claim Gates",
        markdown_table(rows_by_name["claim_gates"]),
        "",
        "## Current Blocker Stack",
        markdown_table(rows_by_name["blocker_stack"]),
        "",
        "## Decision Ledger",
        markdown_table(rows_by_name["decision_ledger"]),
        "",
        "## Next Target",
        markdown_table(rows_by_name["next_target"]),
        "",
        "## Project Status Snapshot",
        markdown_table(rows_by_name["project_status"]),
        "",
        "## Branch Copies",
        markdown_table(rows_by_name["branch_copies"]),
        "",
        "## Validation",
        markdown_table(rows_by_name["validation"]),
        "",
        "## Plain-English Read",
        "",
        "- The `phi R` route is still good mathematics, but `lambda_phi` is not silent yet.",
        "- The finite bound route is useful, but it is still a shopping list of inputs, not a number.",
        "- `Khat` adoption cannot be promoted until `lambda_phi` or the weak-field auxiliary gate moves.",
        "- The next serious leap is a minimal weak-field parent action/auxiliary constraint gate under the current AX1090 closure label.",
    ]
    DOC_PATH.write_text("\n".join(sections) + "\n", encoding="utf-8")


def main() -> None:
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "lambda_zero_attempt": lambda_zero_attempt_rows(),
        "bound_rollforward": bound_rollforward_rows(),
        "source_coupling_handoff": source_coupling_handoff_rows(),
        "khat_adoption_gate": khat_adoption_gate_rows(),
        "weak_field_reentry": weak_field_reentry_rows(),
        "claim_gates": claim_gate_rows(),
        "blocker_stack": blocker_stack_rows(),
        "decision_ledger": decision_ledger_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
        "branch_copies": branch_copy_rows(),
    }

    generated_paths = dict(OUTPUTS)
    generated_paths.update(BRANCH_OUTPUTS)
    generated_paths["doc"] = DOC_PATH

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        write_csv(path, rows_by_name[key])

    write_csv(BRANCH_OUTPUTS["local_bounds_gate"], rows_by_name["bound_rollforward"])
    write_csv(BRANCH_OUTPUTS["source_weight_gate"], rows_by_name["khat_adoption_gate"])
    write_csv(BRANCH_OUTPUTS["rab_next"], rows_by_name["next_target"])

    rows_by_name["validation"] = validation_rows(rows_by_name, generated_paths)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)

    overall = next(row for row in rows_by_name["validation"] if row["validation_id"] == "VAL2714_OVERALL")
    print(f"2714 complete: {overall['passed']} - {overall['details']}")
    print(DOC_PATH)


if __name__ == "__main__":
    main()
