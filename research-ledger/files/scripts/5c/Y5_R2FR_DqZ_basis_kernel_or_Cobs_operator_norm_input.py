from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1671"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1671-Y5-R2FR-DqZ-basis-kernel-or-Cobs-operator-norm-input.md"

SOURCE_FILES = {
    "1670_doc": ROOT / "1670-Y5-R2FR-Cqm-DqZ-observed-coframe-zero-or-first-finite-bound-row.md",
    "1670_validation": OUT / "P8_Y5_BRR545_1670_VALIDATION.csv",
    "1670_product": OUT / "P8_Y5_PARENT_QLOC_1670_PRODUCT_BOUND_CONTRACT.csv",
    "1667_dq_tests": OUT / "P8_Y5_PARENT_QLOC_1667_DQ_ON_ZPHI_TESTS.csv",
    "1667_quotient": OUT / "P8_Y5_PARENT_QLOC_1667_QUOTIENT_MAP_AUDIT.csv",
    "1665_z_audit": OUT / "P8_Y5_PARENT_QLOC_1665_Z_ROUTE_SIGNATURE_AUDIT.csv",
    "1665_signature": OUT / "P8_Y5_PARENT_QLOC_1665_PARENT_SIGNATURE_CLAUSE_AUDIT.csv",
    "1619_normal_form": OUT / "P8_Y5_PARENT_QLOC_1619_POSITIVE_AUXILIARY_NORMAL_FORM.csv",
    "response_contract": OUT / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv",
    "response_variation": OUT / "P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv",
    "response_obstruction": OUT / "P8_RESPONSE_DOUBLET_OBSTRUCTION_LEDGER.csv",
    "757_physical_lock": OUT / "P8_Y5_R10_757_PHYSICAL_LOCK_CONTRACT.csv",
    "1282_component_map": OUT / "P8_Y5_R10_1282_RESPONSE_DOUBLET_COMPONENT_MAP_AUDIT.csv",
    "1282_validation": OUT / "P8_Y5_BRR545_1282_VALIDATION.csv",
}

NEEDLES = {
    "1670_doc": ["C_Obs_e * Dq_Z_norm * N_Z", "least-scrutiny route"],
    "1670_validation": ["VAL1670_OVERALL", "PASS"],
    "1670_product": ["PB1670_3_CqmZ", "PRODUCT_BOUND_SCHEMA_READY_INPUTS_MISSING"],
    "1667_dq_tests": ["DQT1667_1_Z_normal_form", "MISSING_UNIFIED_Z_BASIS_AND_COMPONENT_LOCK"],
    "1667_quotient": ["QMA1667_6_verdict", "Q_NOT_COMPUTABLE_CURRENT_CORPUS"],
    "1665_z_audit": ["ZRA1665_8_verdict", "DO_NOT_ADOPT_LIVE_NONCLAIM"],
    "1665_signature": ["PSC1665_7_residual_vector_lock", "PHYSICAL_LOCK_NOT_DERIVED"],
    "1619_normal_form": ["NF1619_6_verdict", "FORMAL_MECHANISM_EXISTS_NOT_PARENT_SIGNED"],
    "response_contract": ["RD516_5_PPN_lock", "not_derived"],
    "response_variation": ["AV517_3_double_zero", "conditional_pass_not_MTS_promotion"],
    "response_obstruction": ["OB517_2_PPN_lock", "component lock ledger through PPN order"],
    "757_physical_lock": ["PLC757_5_zero_theorem", "conditional_theorem_not_current_MTS_claim"],
    "1282_component_map": ["RCM1282_6_verdict", "COMPONENT_MAP_NOT_CLOSED"],
    "1282_validation": ["VAL1282_10_overall", "PASS"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1671_SOURCE_REGISTER.csv"
Z_BASIS_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1671_Z_BASIS_COMPONENT_LOCK_AUDIT.csv"
KERNEL_ATTEMPT = OUT / "P8_Y5_PARENT_QLOC_1671_DQZ_KERNEL_THEOREM_ATTEMPT.csv"
CONSTRAINT_ROUTE = OUT / "P8_Y5_PARENT_QLOC_1671_CONSTRAINT_ELIMINATION_ROUTE.csv"
COBS_FACTOR = OUT / "P8_Y5_PARENT_QLOC_1671_COBS_FACTOR_INPUT_ROWS.csv"
DQZ_FACTOR = OUT / "P8_Y5_PARENT_QLOC_1671_DQZ_FACTOR_INPUT_ROWS.csv"
PRODUCT_QUEUE = OUT / "P8_Y5_PARENT_QLOC_1671_PRODUCT_FACTOR_QUEUE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1671_DECISION.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1671_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1671_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1671_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    Z_BASIS_AUDIT,
    KERNEL_ATTEMPT,
    CONSTRAINT_ROUTE,
    COBS_FACTOR,
    DQZ_FACTOR,
    PRODUCT_QUEUE,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    Z_BASIS_AUDIT,
    KERNEL_ATTEMPT,
    CONSTRAINT_ROUTE,
    COBS_FACTOR,
    DQZ_FACTOR,
    PRODUCT_QUEUE,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

COPY_TARGETS = {
    Z_BASIS_AUDIT: [
        QUARANTINE / "Z_BASIS_COMPONENT_LOCK_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_Z_basis_component_lock_audit_nonclaim_1671.csv",
        QUEUE / "JR1671_Z_BASIS_COMPONENT_LOCK_AUDIT_NONCLAIM.csv",
    ],
    KERNEL_ATTEMPT: [
        QUARANTINE / "DQZ_KERNEL_THEOREM_ATTEMPT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_DqZ_kernel_theorem_attempt_nonclaim_1671.csv",
        QUEUE / "JR1671_DQZ_KERNEL_THEOREM_ATTEMPT_NONCLAIM.csv",
    ],
    COBS_FACTOR: [
        QUARANTINE / "COBS_FACTOR_INPUT_ROWS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_Cobs_factor_input_rows_nonclaim_1671.csv",
        QUEUE / "JR1671_COBS_FACTOR_INPUT_ROWS_NONCLAIM.csv",
    ],
    DQZ_FACTOR: [
        QUARANTINE / "DQZ_FACTOR_INPUT_ROWS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_DqZ_factor_input_rows_nonclaim_1671.csv",
        QUEUE / "JR1671_DQZ_FACTOR_INPUT_ROWS_NONCLAIM.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_nonclaim_1671.csv",
        QUEUE / "JR1671_NEXT_TARGET_NONCLAIM.csv",
    ],
}


def ensure_dirs() -> None:
    for directory_path in [OUT, QUARANTINE, BRANCH_RESIDUALS, QUEUE]:
        directory_path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def bool_string(value: object) -> str:
    return str(value).strip().lower()


def source_register_rows() -> list[dict[str, object]]:
    rows = []
    for source_id, path in SOURCE_FILES.items():
        text = read_text(path)
        needles = NEEDLES[source_id]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needles_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "role": "1671 Dq_Z basis/kernel or C_Obs/Dq_Z product-factor input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def z_basis_rows() -> list[dict[str, object]]:
    rows = [
        (
            "ZB1671_0_formal_Z",
            "Z^A=(R_+^A-R_-^A)/2 exists as a formal exchange-odd normal-form coordinate",
            "NF1619/AV517 give a coherent auxiliary construction",
            "FORMAL_MECHANISM_EXISTS",
            "useful derivation scaffold, not a live component basis",
        ),
        (
            "ZB1671_1_doublet_coverage",
            "R_+^A,R_-^A exist for every physical local residual channel",
            "RD516_0/ZRA1665_1 say component coverage is partial/conditional",
            "NOT_PARENT_DERIVED",
            "Dq_Z cannot be universal across q_loc/Y5/Y6/PPN/boundary/coupling",
        ),
        (
            "ZB1671_2_component_lock",
            "Z is full-rank over R_phys through tested weak-field order",
            "PLC757_1 and RCM1282_6 keep the lock unproved",
            "COMPONENT_LOCK_NOT_CLOSED",
            "formal Z=0 can zero a shadow while observed residuals survive",
        ),
        (
            "ZB1671_3_norm_equivalence",
            "Z quadratic norm coercively controls the physical residual vector",
            "PLC757_2 not shown; 1670 still missing N_Z",
            "NORM_EQUIVALENCE_MISSING",
            "cannot turn positive auxiliary energy into physical residual silence",
        ),
        (
            "ZB1671_4_source_boundary_work",
            "no linear source or boundary work drives Z",
            "RD516_4/RD516_6 and OB517 keep Y5/Y6/boundary channels open",
            "SOURCE_BOUNDARY_ZERO_NOT_DERIVED",
            "positive operator does not imply zero if J_Z or B_Z survives",
        ),
        (
            "ZB1671_5_visible_quotient_sort",
            "Z is either absent from q or eliminated before q/readout",
            "QMA1667_6 says q is not computable; DQT1667_1 says Dq[partial_Z] missing",
            "Q_DQ_SORT_NOT_COMPUTABLE",
            "Dq_Z zero cannot be parent-signed",
        ),
        (
            "ZB1671_6_verdict",
            "adopt Z basis as live Dq_Z theorem object",
            "ZB1671_1 through ZB1671_5 do not close",
            "Z_BASIS_COMPONENT_LOCK_NOT_CLOSED",
            "stage Dq_Z and C_Obs_e product-factor rows",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "basis_id": basis_id,
            "required_clause": required_clause,
            "evidence": evidence,
            "status": status,
            "effect": effect,
            "parent_signed": False,
            "theorem_zero_adopted": False,
            "finite_value_present": False,
            "prediction_source_backed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for basis_id, required_clause, evidence, status, effect in rows
    ]


def kernel_attempt_rows() -> list[dict[str, object]]:
    rows = [
        (
            "KT1671_0_kernel_theorem_statement",
            "If q=q(Q_even, matter labels owned by Q_even, boundary data independent of Z) and v_Z is tangent only to Z, then Dq[v_Z]=0.",
            "exact chain-rule/coordinate theorem",
            "requires a parent-owned q and Z/even sort",
            "EXACT_CONDITIONAL_THEOREM",
        ),
        (
            "KT1671_1_independence_clause",
            "partial_Z q = 0 for observed geometry, source/readout, constants, and projector data",
            "would kill Dq_Z directly",
            "not in current corpus; q is partial prior only",
            "NOT_PARENT_SIGNED",
        ),
        (
            "KT1671_2_constraint_clause",
            "Z is constrained/solved to zero before q and matter action are formed",
            "cleaner than quotient invisibility because it removes Z from the local branch",
            "1668 selected constraint-first as best route but unsigned",
            "CONSTRAINT_ROUTE_UNSIGNED",
        ),
        (
            "KT1671_3_auxiliary_guard",
            "Dq_Z=0 for an auxiliary Z does not prove local GR unless physical residual lock also closes",
            "prevents coframe-only victory lap",
            "757/1282 block physical lock",
            "GUARD_ACTIVE",
        ),
        (
            "KT1671_4_source_readout_guard",
            "Dq_Z=0 for e_obs does not kill hidden source/readout/marker/boundary factors",
            "prevents beta/source/clock/orbit leakage",
            "1667 retained Dsource/Dtheta/boundary leak rows",
            "GUARD_ACTIVE",
        ),
        (
            "KT1671_5_verdict",
            "Dq_Z_norm=0 current theorem",
            "verdict",
            "no parent q, Z basis, independence clause, or constraint route is signed together",
            "DQZ_ZERO_NOT_PARENT_SIGNED",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "kernel_id": kernel_id,
            "statement": statement,
            "math_role": math_role,
            "evidence_or_required_input": evidence_or_required_input,
            "status": status,
            "parent_signed": False,
            "theorem_zero_adopted": False,
            "finite_value_present": False,
            "prediction_source_backed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for kernel_id, statement, math_role, evidence_or_required_input, status in rows
    ]


def constraint_route_rows() -> list[dict[str, object]]:
    rows = [
        (
            "CE1671_0_normal_form",
            "positive exchange-even normal form exists",
            "NF1619 gives calculable formal action, metric response by definition, and double-zero",
            "FORMAL_PASS_ONLY",
            "good mechanism, not live MTS",
        ),
        (
            "CE1671_1_euler_zero",
            "Euler equation L_AB Z^B=0 on compact local branch",
            "requires J_Z=0, B_Z=0, positive operator, and source/boundary silence",
            "BLOCKED_SOURCE_BOUNDARY",
            "cannot solve Z=0 from positivity alone",
        ),
        (
            "CE1671_2_pre_q_elimination",
            "Z=0 is solved before q/matter/readout construction",
            "would make Dq_Z irrelevant rather than small",
            "NOT_PARENT_SIGNED",
            "best derivation route still open",
        ),
        (
            "CE1671_3_physical_lock",
            "constraint eliminates the actual measured residual vector, not only auxiliary Z",
            "requires full-rank/coercive Z-to-R_phys map",
            "COMPONENT_MAP_NOT_CLOSED",
            "cannot promote to GR/Newton reduction",
        ),
        (
            "CE1671_4_verdict",
            "constraint-elimination route closes now",
            "normal form formal pass, but live source/boundary/physical-lock gates fail",
            "CONSTRAINT_ELIMINATION_NOT_DERIVED",
            "route retained; product factors staged",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": route_id,
            "required_clause": required_clause,
            "evidence": evidence,
            "status": status,
            "effect": effect,
            "parent_signed": False,
            "theorem_zero_adopted": False,
            "finite_value_present": False,
            "prediction_source_backed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for route_id, required_clause, evidence, status, effect in rows
    ]


def cobs_factor_rows() -> list[dict[str, object]]:
    rows = [
        (
            "COBS1671_0_operator_norm",
            "C_Obs_e",
            "||DObs_e||_{q->e}",
            "dimensionless after q/e norms are declared",
            "MISSING_OBS_E_FUNCTOR_AND_OPERATOR_NORM",
            "Obs_e(q), q norm, e norm, no-shadow-frame certificate",
            "R0;R2;R3;R4;R10",
        ),
        (
            "COBS1671_1_annihilator",
            "C_Obs_e_on_im_DqZ",
            "||DObs_e restricted to im(Dq[v_Z])||",
            "dimensionless coframe response factor",
            "MISSING_IMAGE_DQZ_AND_ANNIHILATOR_CERTIFICATE",
            "image basis for Dq_Z and proof DObs_e kills it or finite bound",
            "R0;R3;R4;R10",
        ),
        (
            "COBS1671_2_shadow_frame_guard",
            "C_shadow",
            "operator norm for representative Weyl/disformal/source/readout frame leakage",
            "dimensionless",
            "MISSING_NO_SHADOW_FRAME_OR_BOUND",
            "no-shadow theorem or finite c_g/b_dis/source-frame coefficient",
            "R0;R2;R3;R4;R5;R6;R10",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "factor_id": factor_id,
            "symbol": symbol,
            "definition": definition,
            "units": units,
            "current_status": current_status,
            "needed_source_inputs": needed_source_inputs,
            "priority_arenas": priority_arenas,
            "candidate_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "theorem_zero_adopted": False,
            "finite_value_present": False,
            "prediction_source_backed": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for factor_id, symbol, definition, units, current_status, needed_source_inputs, priority_arenas in rows
    ]


def dqz_factor_rows() -> list[dict[str, object]]:
    rows = [
        (
            "DQZ1671_0_basis",
            "Z_basis",
            "basis vectors partial_ZA and physical-channel labels",
            "basis/unit convention",
            "MISSING_UNIFIED_Z_BASIS",
            "component map from formal doublet variables to local residual/channel basis",
            "all",
        ),
        (
            "DQZ1671_1_norm",
            "N_Z",
            "||v_Z||_Z or unit-normalized selected direction",
            "dimensionless if unit-normalized",
            "MISSING_Z_DIRECTION_NORMALIZATION",
            "Z field units, tangent vector convention, local branch norm",
            "R0;R3;R4;R10",
        ),
        (
            "DQZ1671_2_derivative",
            "Dq_Z_norm",
            "||Dq[partial_Z]||_q",
            "dimensionless after q/Z norms are declared",
            "MISSING_DQ_DERIVATIVE_OR_THEOREM_ZERO",
            "parent q(Phi), derivative on Z direction, q norm, quotient sort",
            "R0;R3;R4;R10;R11",
        ),
        (
            "DQZ1671_3_zero_candidate",
            "Dq_Z_zero",
            "Dq[partial_Z]=0 or Z eliminated before q",
            "theorem-zero",
            "MISSING_PARENT_KERNEL_OR_CONSTRAINT_PROOF",
            "q independence theorem or constraint-elimination theorem",
            "R0;R3;R4;R10;R11",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "factor_id": factor_id,
            "symbol": symbol,
            "definition": definition,
            "units": units,
            "current_status": current_status,
            "needed_source_inputs": needed_source_inputs,
            "priority_arenas": priority_arenas,
            "candidate_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "theorem_zero_adopted": False,
            "finite_value_present": False,
            "prediction_source_backed": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for factor_id, symbol, definition, units, current_status, needed_source_inputs, priority_arenas in rows
    ]


def product_queue_rows() -> list[dict[str, object]]:
    rows = [
        (
            "PFQ1671_0_clean_kill",
            "Dq_Z_norm=0 via q-independence or pre-q constraint elimination",
            "MISSING_PARENT_KERNEL_OR_CONSTRAINT_PROOF",
            "highest",
            "kills C_qm_Z without numeric fitting",
        ),
        (
            "PFQ1671_1_annihilator",
            "C_Obs_e_on_im_DqZ=0",
            "MISSING_OBS_E_ANNIHILATOR_CERTIFICATE",
            "medium",
            "kills coframe leak but still requires source/readout guard rows",
        ),
        (
            "PFQ1671_2_finite_product",
            "C_qm_Z <= C_Obs_e * Dq_Z_norm * N_Z",
            "MISSING_COBS_AND_DQZ_FACTOR_ROWS",
            "fallback",
            "scoreable only after all factors and arena Pi maps are sourced",
        ),
        (
            "PFQ1671_3_physical_lock",
            "Z=0 controls R_phys with full rank/coercive norm",
            "MISSING_PHYSICAL_LOCK_MAP",
            "highest_for_GR",
            "needed before response-doublet double-zero can become local GR/Newton reduction",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "queue_id": queue_id,
            "route": route,
            "current_status": current_status,
            "priority": priority,
            "why_it_matters": why_it_matters,
            "required_inputs": "parent q; Z basis; observed coframe functor; no-shadow-frame; source/readout/boundary guards; arena Pi maps",
            "theorem_zero_adopted": False,
            "finite_value_present": False,
            "prediction_source_backed": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for queue_id, route, current_status, priority, why_it_matters in rows
    ]


def decision_rows() -> list[dict[str, object]]:
    rows = [
        (
            "D1671_0_DqZ_zero",
            "DQZ_ZERO_NOT_PARENT_SIGNED",
            "formal Z exists, but q is not computable and Z basis/component lock is not parent-signed",
            "do not claim Dq_Z_norm=0",
        ),
        (
            "D1671_1_formal_route",
            "RESPONSE_DOUBLET_RETAINED_AS_DERIVATION_TARGET",
            "NF1619/AV517 prove a real formal double-zero mechanism if physical lock/source/boundary gates close",
            "keep it as the cleanest theorem route, not a current result",
        ),
        (
            "D1671_2_product_factors",
            "COBS_AND_DQZ_FACTOR_ROWS_STAGED",
            "1670 product law is now split into separate acquisition factors",
            "fill or derive C_Obs_e, Dq_Z_norm, and N_Z before arena scoring",
        ),
        (
            "D1671_3_next",
            "TARGET_PHYSICAL_LOCK_OR_FIRST_FACTOR",
            "local GR needs the physical lock; empirical accountability needs product factors if lock fails",
            "try the full-rank Z-to-R_phys map first, then fill Dq_Z/C_Obs_e factor rows if it fails",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for decision_id, decision, reason, next_action in rows
    ]


def claim_rows() -> list[dict[str, object]]:
    rows = [
        ("CG1671_0_DqZ_zero", "Dq_Z_norm=0 is proved", False, "NO_CLAIM", "q, Z basis, and kernel/constraint route are not parent-signed"),
        ("CG1671_1_response_doublet_GR", "response-doublet formal double-zero proves local GR/Newton", False, "NO_CLAIM", "physical residual lock and source/boundary zero gates remain open"),
        ("CG1671_2_factor_score", "C_qm_Z product factor row is score-ready", False, "BLOCKED", "C_Obs_e, Dq_Z_norm, N_Z, and arena Pi are missing"),
        ("CG1671_3_R10_PPN_WEP", "R10/PPN/WEP/clock/orbit claims follow", False, "NO_CLAIM", "arena projections remain nonclaim and coefficient inputs missing"),
        ("CG1671_4_public_claim", "public local claim safe", False, "NO_CLAIM", "private derivation/audit checkpoint only"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": gate_pass,
            "status": status,
            "blocker": blocker,
            "local_gr_claim_allowed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim, gate_pass, status, blocker in rows
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1672-Y5-R2FR-Z-physical-lock-map-or-first-DqZ-factor-source-row.md",
            "script": "scripts/Y5_R2FR_Z_physical_lock_map_or_first_DqZ_factor_source_row.py",
            "objective": "attempt the full-rank/coercive Z-to-R_phys lock needed for local GR/Newton; if it fails, fill the first source-ready Dq_Z or C_Obs_e product-factor row without scoring",
            "success_condition": "either a parent-signed physical-lock map from Z to q_loc/Y5/Y6/PPN/boundary/coupling residuals, or one finite nonclaim factor row with units, source path, and arena projections",
            "forbidden_shortcuts": "no formal-Z-to-physical-residual leap; no invented Dq_Z/C_Obs value; no cancellation; no local-GR/R10/PPN/WEP claim; no GitHub action",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        }
    ]


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)


def all_claim_flags_false(paths: list[Path]) -> bool:
    flag_names = {
        "accepted_for_scoring",
        "claim_allowed",
        "claim_ready",
        "comparison_ready",
        "finite_value_present",
        "local_gr_claim_allowed",
        "numeric_value_present",
        "parent_signed",
        "prediction_source_backed",
        "score_allowed",
        "score_ready",
        "source_backed",
        "theorem_zero_adopted",
        "valid_for_claim",
        "valid_for_mts_claim",
        "valid_prediction_row",
    }
    for path in paths:
        for row in csv_rows(path):
            for flag_name in flag_names.intersection(row):
                if bool_string(row[flag_name]) == "true":
                    return False
    return True


def no_missing_marked_ready(paths: list[Path]) -> bool:
    readiness_flags = {
        "accepted_for_scoring",
        "claim_allowed",
        "comparison_ready",
        "finite_value_present",
        "prediction_source_backed",
        "score_ready",
        "valid_for_claim",
        "valid_prediction_row",
    }
    for path in paths:
        for row in csv_rows(path):
            contains_missing = any("MISSING_" in value for value in row.values())
            if contains_missing and any(bool_string(row.get(flag, False)) == "true" for flag in readiness_flags):
                return False
    return True


def validation_rows(
    source_rows: list[dict[str, object]],
    z_basis: list[dict[str, object]],
    kernel: list[dict[str, object]],
    constraint: list[dict[str, object]],
    cobs: list[dict[str, object]],
    dqz: list[dict[str, object]],
    queue: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim: list[dict[str, object]],
    next_targets: list[dict[str, object]],
) -> list[dict[str, object]]:
    generated_csv_parse = True
    try:
        for generated_path in GENERATED:
            csv_rows(generated_path)
    except Exception:
        generated_csv_parse = False

    formalization_dirty = (
        any("1671" in path.name for path in FORMALIZATION.rglob("*1671*"))
        if FORMALIZATION.exists()
        else False
    )
    sources_ok = all(row["path_exists"] and row["needles_found"] for row in source_rows)
    z_lock_failed = any(row["basis_id"] == "ZB1671_6_verdict" and row["status"] == "Z_BASIS_COMPONENT_LOCK_NOT_CLOSED" for row in z_basis)
    dqz_zero_failed = any(row["kernel_id"] == "KT1671_5_verdict" and row["status"] == "DQZ_ZERO_NOT_PARENT_SIGNED" for row in kernel)
    constraint_failed = any(row["route_id"] == "CE1671_4_verdict" and row["status"] == "CONSTRAINT_ELIMINATION_NOT_DERIVED" for row in constraint)
    cobs_staged = {row["symbol"] for row in cobs} >= {"C_Obs_e", "C_Obs_e_on_im_DqZ", "C_shadow"}
    dqz_staged = {row["symbol"] for row in dqz} >= {"Z_basis", "N_Z", "Dq_Z_norm", "Dq_Z_zero"}
    queue_has_kill_and_fallback = {row["queue_id"] for row in queue} >= {"PFQ1671_0_clean_kill", "PFQ1671_2_finite_product", "PFQ1671_3_physical_lock"}
    decision_next = any(row["decision"] == "TARGET_PHYSICAL_LOCK_OR_FIRST_FACTOR" for row in decisions)
    claim_gate_safe = all(row["gate_pass"] is False and row["claim_allowed"] is False for row in claim)
    next_target_selected = next_targets[0]["next_target"] == "1672-Y5-R2FR-Z-physical-lock-map-or-first-DqZ-factor-source-row.md"
    branch_copies = all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" not in str(target))
    queue_copies = all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" in str(target))

    checks = [
        ("VAL1671_0_sources_exist", sources_ok, "all cited 1671 source paths exist and needles are present"),
        ("VAL1671_1_z_lock_failed", z_lock_failed, "Z basis/component physical lock is not promoted"),
        ("VAL1671_2_dqz_zero_failed", dqz_zero_failed, "Dq_Z zero theorem remains unsigned"),
        ("VAL1671_3_constraint_failed", constraint_failed, "constraint-elimination route remains not derived"),
        ("VAL1671_4_cobs_factor_rows", cobs_staged, "C_Obs_e factor rows are staged"),
        ("VAL1671_5_dqz_factor_rows", dqz_staged, "Dq_Z factor rows are staged"),
        ("VAL1671_6_queue_routes", queue_has_kill_and_fallback, "product-factor queue has theorem-kill and finite fallback routes"),
        ("VAL1671_7_decision_next", decision_next, "decision selects physical lock or first product factor"),
        ("VAL1671_8_claim_gate_safe", claim_gate_safe, "all claim gates keep local claims false"),
        ("VAL1671_9_no_mts_claim_flags", all_claim_flags_false(CLAIM_CHECKED), "all 1671 generated rows keep claim/no-score flags false"),
        ("VAL1671_10_missing_not_ready", no_missing_marked_ready(CLAIM_CHECKED), "no row containing MISSING_* is marked source-backed, claim-ready, or score-ready"),
        ("VAL1671_11_next_target_selected", next_target_selected, "next target selects Z physical-lock map or first Dq_Z factor row"),
        ("VAL1671_12_csv_parse", generated_csv_parse, "all generated 1671 CSVs parse"),
        ("VAL1671_13_branch_copies", branch_copies, "branch/quarantine copies exist"),
        ("VAL1671_14_queue_copies", queue_copies, "acquisition queue nonclaim copies exist"),
        ("VAL1671_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1671_16_formalization_untouched", not formalization_dirty, "no 1671 outputs found under formalization-workbench"),
    ]
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1671_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1671 Dq_Z basis/kernel or C_Obs operator-norm input validation",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row[column]).replace("\n", " ") for column in columns) + " |")
    return "\n".join(lines)


def write_doc(
    source_rows: list[dict[str, object]],
    z_basis: list[dict[str, object]],
    kernel: list[dict[str, object]],
    constraint: list[dict[str, object]],
    cobs: list[dict[str, object]],
    dqz: list[dict[str, object]],
    queue: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 1671 - DqZ Basis Kernel Or Cobs Operator Norm Input

**Private status:** Dq_Z theorem attempt plus nonclaim factor acquisition pack. No `q_loc=0`, local-GR pass, Newton pass, PPN pass, R10 pass, WEP pass, clock pass, orbital pass, or public claim is made.

## Verdict

`Dq_Z=0` is not parent-signed in the current corpus.

The exact theorem route is simple:

```text
if q = q(Q_even, owned matter/readout/boundary data)
and v_Z is tangent only to Z,
then Dq[v_Z] = 0.
```

But the corpus does not yet supply the parent-owned `q`, the unified `Z` basis, the physical residual lock, or the source/boundary silence needed to use this as a GR/Newton reduction. The response-doublet remains a serious formal mechanism, but not a live local branch proof.

So `1671` splits the 1670 product into acquisition factors:

```text
C_qm_Z <= C_Obs_e * Dq_Z_norm * N_Z
```

## Source Register

{markdown_table(source_rows, ["source_id", "path", "path_exists", "needles_found", "role"])}

## Z Basis And Component Lock Audit

{markdown_table(z_basis, ["basis_id", "required_clause", "evidence", "status", "effect"])}

## DqZ Kernel Theorem Attempt

{markdown_table(kernel, ["kernel_id", "statement", "math_role", "evidence_or_required_input", "status"])}

## Constraint-Elimination Route

{markdown_table(constraint, ["route_id", "required_clause", "evidence", "status", "effect"])}

## Cobs Factor Rows

{markdown_table(cobs, ["factor_id", "symbol", "definition", "units", "current_status", "needed_source_inputs", "candidate_value"])}

## DqZ Factor Rows

{markdown_table(dqz, ["factor_id", "symbol", "definition", "units", "current_status", "needed_source_inputs", "candidate_value"])}

## Product Factor Queue

{markdown_table(queue, ["queue_id", "route", "current_status", "priority", "why_it_matters"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Claim Gates

{markdown_table(claim, ["gate_id", "claim", "gate_pass", "status", "blocker"])}

## Next Target

{markdown_table(next_targets, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Working Interpretation

This is the right kind of failure. The response-doublet is not dead; it is too powerful to use loosely. If `Z` is only auxiliary, it can be invisible without proving the measured residuals vanish. If `Z` is physical, it needs the full-rank/coercive lock to `R_phys`. That is now the next pressure point. If the lock fails again, the fallback is no longer vague: acquire `Dq_Z_norm`, `C_Obs_e`, and `N_Z` as separate nonclaim factors and let the arenas judge them.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    source_rows = source_register_rows()
    z_basis = z_basis_rows()
    kernel = kernel_attempt_rows()
    constraint = constraint_route_rows()
    cobs = cobs_factor_rows()
    dqz = dqz_factor_rows()
    queue = product_queue_rows()
    decisions = decision_rows()
    claim = claim_rows()
    next_targets = next_rows()

    for path, rows in [
        (SOURCE_REGISTER, source_rows),
        (Z_BASIS_AUDIT, z_basis),
        (KERNEL_ATTEMPT, kernel),
        (CONSTRAINT_ROUTE, constraint),
        (COBS_FACTOR, cobs),
        (DQZ_FACTOR, dqz),
        (PRODUCT_QUEUE, queue),
        (DECISION, decisions),
        (CLAIM_GATE, claim),
        (NEXT_TARGET, next_targets),
    ]:
        write_csv(path, rows)

    copy_outputs()
    validation = validation_rows(source_rows, z_basis, kernel, constraint, cobs, dqz, queue, decisions, claim, next_targets)
    write_csv(VALIDATION, validation)
    write_doc(source_rows, z_basis, kernel, constraint, cobs, dqz, queue, decisions, claim, next_targets, validation)

    if any(row["result"] == "FAIL" for row in validation):
        raise SystemExit("1671 validation failed; see P8_Y5_BRR545_1671_VALIDATION.csv")

    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    print("1671 validation PASS")


if __name__ == "__main__":
    main()
