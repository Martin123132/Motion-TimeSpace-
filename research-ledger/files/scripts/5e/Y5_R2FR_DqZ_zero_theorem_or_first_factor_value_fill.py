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
QUARANTINE = MICROSCOPE / "quarantine" / "1673"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1673-Y5-R2FR-DqZ-zero-theorem-or-first-factor-value-fill.md"

SOURCE_FILES = {
    "1672_doc": ROOT / "1672-Y5-R2FR-Z-physical-lock-map-or-first-DqZ-factor-source-row.md",
    "1672_validation": OUT / "P8_Y5_BRR545_1672_VALIDATION.csv",
    "1672_first_dqz": OUT / "P8_Y5_PARENT_QLOC_1672_FIRST_DQZ_FACTOR_SOURCE_ROW_NONCLAIM.csv",
    "1672_lock_map": OUT / "P8_Y5_PARENT_QLOC_1672_Z_TO_RPHYS_LOCK_MAP_ATTEMPT.csv",
    "1672_rank_gate": OUT / "P8_Y5_PARENT_QLOC_1672_FULL_RANK_COERCIVITY_GATE.csv",
    "1671_dqz_rows": OUT / "P8_Y5_PARENT_QLOC_1671_DQZ_FACTOR_INPUT_ROWS.csv",
    "1667_dq_tests": OUT / "P8_Y5_PARENT_QLOC_1667_DQ_ON_ZPHI_TESTS.csv",
    "1665_signature": OUT / "P8_Y5_PARENT_QLOC_1665_PARENT_SIGNATURE_CLAUSE_AUDIT.csv",
    "1282_component_map": OUT / "P8_Y5_R10_1282_RESPONSE_DOUBLET_COMPONENT_MAP_AUDIT.csv",
    "757_contract": OUT / "P8_Y5_R10_757_PHYSICAL_LOCK_CONTRACT.csv",
    "777_rank_gate": OUT / "P8_Y5_R10_777_LOCK_RANK_AND_NULLSPACE_GATE.csv",
}

NEEDLES = {
    "1672_doc": ["Dq_Z_norm", "No `q_loc=0`"],
    "1672_validation": ["VAL1672_OVERALL", "PASS"],
    "1672_first_dqz": ["DQZ1672_0_first_factor_row", "MISSING_NUMERIC_OR_THEOREM_ZERO"],
    "1672_lock_map": ["LOCK1672_6_verdict", "PHYSICAL_LOCK_NOT_PROVED"],
    "1672_rank_gate": ["RG1672_5_verdict", "FULL_RANK_COERCIVITY_NOT_PROVED"],
    "1671_dqz_rows": ["DQZ1671_2_derivative", "MISSING_DQ_DERIVATIVE_OR_THEOREM_ZERO"],
    "1667_dq_tests": ["DQT1667_5_constraint_first_escape", "BEST_DERIVATION_ROUTE_UNSIGNED"],
    "1665_signature": ["PSC1665_1_quotient_map", "MISSING_DQ_COMPUTATION"],
    "1282_component_map": ["RCM1282_6_verdict", "COMPONENT_MAP_NOT_CLOSED"],
    "757_contract": ["PLC757_1_lock_map", "not_shown"],
    "777_rank_gate": ["RNG777_0_full_rank_required", "not_satisfied"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1673_SOURCE_REGISTER.csv"
ZERO_CONDITIONS = OUT / "P8_Y5_PARENT_QLOC_1673_DQZ_ZERO_THEOREM_CONDITIONS.csv"
ZERO_ATTEMPT = OUT / "P8_Y5_PARENT_QLOC_1673_DQZ_ZERO_THEOREM_ATTEMPT.csv"
FACTOR_VALUE = OUT / "P8_Y5_PARENT_QLOC_1673_DQZ_FACTOR_VALUE_FILL_NONCLAIM.csv"
BLOCKER_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1673_DQZ_FACTOR_BLOCKER_LEDGER.csv"
ARENA_REQUIREMENTS = OUT / "P8_Y5_PARENT_QLOC_1673_ARENA_FACTOR_REQUIREMENTS_NONCLAIM.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1673_DECISION.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1673_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1673_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1673_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    ZERO_CONDITIONS,
    ZERO_ATTEMPT,
    FACTOR_VALUE,
    BLOCKER_LEDGER,
    ARENA_REQUIREMENTS,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    ZERO_CONDITIONS,
    ZERO_ATTEMPT,
    FACTOR_VALUE,
    BLOCKER_LEDGER,
    ARENA_REQUIREMENTS,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

COPY_TARGETS = {
    ZERO_ATTEMPT: [
        QUARANTINE / "DQZ_ZERO_THEOREM_ATTEMPT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_DqZ_zero_theorem_attempt_nonclaim_1673.csv",
        QUEUE / "JR1673_DQZ_ZERO_THEOREM_ATTEMPT_NONCLAIM.csv",
    ],
    FACTOR_VALUE: [
        QUARANTINE / "DQZ_FACTOR_VALUE_FILL_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_DqZ_factor_value_fill_nonclaim_1673.csv",
        QUEUE / "JR1673_DQZ_FACTOR_VALUE_FILL_NONCLAIM.csv",
    ],
    BLOCKER_LEDGER: [
        QUARANTINE / "DQZ_FACTOR_BLOCKER_LEDGER.csv",
        BRANCH_RESIDUALS / "R2FR_DqZ_factor_blocker_ledger_1673.csv",
        QUEUE / "JR1673_DQZ_FACTOR_BLOCKER_LEDGER.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_nonclaim_1673.csv",
        QUEUE / "JR1673_NEXT_TARGET_NONCLAIM.csv",
    ],
}


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def file_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def bool_cell(value: str | bool) -> bool:
    if isinstance(value, bool):
        return value
    return value.strip().lower() == "true"


def missing_marker(value: object) -> bool:
    return "MISSING_" in str(value) or "NOT_SOURCE_BACKED" in str(value)


def source_register_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for key, path in SOURCE_FILES.items():
        exists = path.exists()
        text = file_text(path) if exists else ""
        needles = NEEDLES[key]
        needles_present = all(needle in text for needle in needles)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_key": key,
                "source_path": str(path),
                "exists": exists,
                "needles_present": needles_present,
                "required_needles": "; ".join(needles),
                "use_in_1673": "Dq_Z zero theorem/factor-fill source input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def zero_conditions_rows() -> list[dict[str, object]]:
    common = {
        "branch_id": BRANCH_ID,
        "theorem_label": "Dq_Z_zero_theorem",
        "formal_statement": "If q(Phi) factorizes through a quotient chart independent of every selected Z direction, and every selected Z tangent is constraint-tangent and in ker(Dq), then Dq_Z_norm=0.",
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    condition_data = [
        (
            "ZC1673_0_parent_chart",
            "Phi_parent=(q-sector, Z-sector, gauge, matter/source/readout, boundary) is declared field-by-field.",
            "PSC1665_0 says candidate bundle exists but q and ker(Dq) are not parent-defined.",
            "MISSING_PARENT_FIELD_CHART",
            "define parent variables before quotient projection",
        ),
        (
            "ZC1673_1_quotient_map",
            "q: Phi_parent -> Q_loc is differentiable and computable on selected tangent directions.",
            "PSC1665_1 records MISSING_DQ_COMPUTATION.",
            "MISSING_COMPUTABLE_Q_MAP",
            "write q(Phi) explicitly enough to take Dq",
        ),
        (
            "ZC1673_2_Z_basis",
            "Z^A are live parent tangent directions or constraint-eliminated fields, not only auxiliary normal-form labels.",
            "DQT1667_1 records MISSING_UNIFIED_Z_BASIS_AND_COMPONENT_LOCK.",
            "MISSING_UNIFIED_Z_BASIS",
            "map Z components to q_loc/Y5/Y6/PPN/boundary/coupling channels",
        ),
        (
            "ZC1673_3_constraint_tangent",
            "selected partial_Z directions preserve constraints or are eliminated before matter/readout q is built.",
            "DQT1667_5 says constraint-first escape is best route but unsigned.",
            "MISSING_CONSTRAINT_ELIMINATION_THEOREM",
            "prove Z is removed by parent constraints or retained as source-backed physical factor",
        ),
        (
            "ZC1673_4_source_readout_silence",
            "matter, clocks, photons, sources, orbit readouts, and measured-GM data do not depend on Z except through q.",
            "PSC1665_3 and PSC1665_5 keep matter/source descent and source-current zero missing.",
            "MISSING_SOURCE_READOUT_DESCENT",
            "derive quotient-invariant matter/source/readout action",
        ),
        (
            "ZC1673_5_boundary_silence",
            "boundary/projector/symplectic flux terms vanish or are included in q before Dq_Z is set to zero.",
            "PSC1665_6 keeps boundary/projector open.",
            "MISSING_BOUNDARY_PROJECTOR_NO_FLUX",
            "prove no-flux theorem or retain finite boundary projection",
        ),
        (
            "ZC1673_6_norms",
            "q and Z norms are declared so ||Dq[partial_Z]|| is a real operator norm.",
            "DQZ1671_1 and DQZ1671_2 leave N_Z and Dq_Z_norm missing.",
            "MISSING_Q_Z_NORMS",
            "declare local branch norm conventions",
        ),
    ]
    return [
        {
            **common,
            "condition_id": condition_id,
            "condition": condition,
            "current_evidence": evidence,
            "status": status,
            "next_action": action,
            "condition_met": False,
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "accepted_for_scoring": False,
            "score_ready": False,
        }
        for condition_id, condition, evidence, status, action in condition_data
    ]


def zero_attempt_rows() -> list[dict[str, object]]:
    rows = [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "ZTA1673_0_kernel_route",
            "route": "ker(Dq) route",
            "candidate_derivation": "Show partial_ZA in ker(Dq) for all selected Z^A, then Dq_Z_norm=0.",
            "required_inputs": "computable q(Phi); selected Z basis; q/Z norms; source/readout/boundary silence",
            "current_result": "REJECT_CURRENT_PROOF",
            "blocking_issue": "q and Z basis are not parent-signed, so ker(Dq) cannot be evaluated",
            "theorem_zero_adopted": False,
            "finite_value_present": False,
            "prediction_source_backed": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "ZTA1673_1_factorization_route",
            "route": "quotient-factorization route",
            "candidate_derivation": "Prove q(Phi)=qbar(pi(Phi)) with pi deleting Z after constraints; then partial_Z q=0.",
            "required_inputs": "parent quotient map; constraint elimination; matter/source/readout descent through qbar",
            "current_result": "CONDITIONAL_ONLY",
            "blocking_issue": "constraint-first escape is identified as best route but unsigned",
            "theorem_zero_adopted": False,
            "finite_value_present": False,
            "prediction_source_backed": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "ZTA1673_2_physical_lock_route",
            "route": "physical-lock route",
            "candidate_derivation": "If Z=0 full-rank/coercive locks all physical residuals, Dq_Z can be demoted to observed-null branch.",
            "required_inputs": "full-rank L^I_A; physical nullspace control; no linear work in each observed channel",
            "current_result": "REJECT_CURRENT_PROOF",
            "blocking_issue": "1672 records FULL_RANK_COERCIVITY_NOT_PROVED and PHYSICAL_LOCK_NOT_PROVED",
            "theorem_zero_adopted": False,
            "finite_value_present": False,
            "prediction_source_backed": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "ZTA1673_3_verdict",
            "route": "Dq_Z_norm=0 verdict",
            "candidate_derivation": "Dq_Z_norm=0 is not derivable from current source state.",
            "required_inputs": "ZTA1673_0 through ZTA1673_2 all closed",
            "current_result": "ZERO_THEOREM_NOT_CLOSED",
            "blocking_issue": "cannot promote local-GR/Newton reduction through Dq_Z silence",
            "theorem_zero_adopted": False,
            "finite_value_present": False,
            "prediction_source_backed": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return rows


def factor_value_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQZVAL1673_0_first_factor_value",
            "symbol": "Dq_Z_norm",
            "definition": "operator norm ||Dq[partial_Z]||_q/||partial_Z||_Z for the selected local response direction",
            "units": "dimensionless after q and Z norm conventions",
            "value_type": "theorem_zero_or_source_backed_interval_required",
            "candidate_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "lower_bound": "0",
            "upper_bound": "MISSING_SOURCE_BACKED_UPPER_BOUND",
            "source_paths": "P8_Y5_PARENT_QLOC_1672_FIRST_DQZ_FACTOR_SOURCE_ROW_NONCLAIM.csv; P8_Y5_PARENT_QLOC_1667_DQ_ON_ZPHI_TESTS.csv; P8_Y5_PARENT_QLOC_1665_PARENT_SIGNATURE_CLAUSE_AUDIT.csv",
            "required_source_inputs": "q(Phi); Z basis; Dq matrix; q norm; Z norm; source/readout descent; boundary/no-flux clause",
            "projection_formula": "C_qm_Z <= C_Obs_e * Dq_Z_norm * N_Z",
            "current_status": "BLOCKED_NO_THEOREM_ZERO_OR_FINITE_VALUE",
            "promotion_rule": "promote only if Dq_Z_norm=0 is parent-proved or a finite numeric/interval upper bound is source-backed and no MISSING_* markers remain",
            "theorem_zero_adopted": False,
            "finite_value_present": False,
            "prediction_source_backed": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def blocker_rows() -> list[dict[str, object]]:
    data = [
        (
            "BLK1673_0_parent_q",
            "q(Phi)",
            "MISSING_COMPUTABLE_Q_MAP",
            "write the local observable quotient map, including coframe/metric/source/readout/boundary arguments",
        ),
        (
            "BLK1673_1_Z_basis",
            "partial_ZA",
            "MISSING_UNIFIED_Z_BASIS",
            "choose live Z directions and map them to physical residual channels",
        ),
        (
            "BLK1673_2_Dq_matrix",
            "Dq[partial_ZA]",
            "MISSING_DQ_DERIVATIVE_MATRIX",
            "differentiate q along each selected Z tangent or prove factorization removes it",
        ),
        (
            "BLK1673_3_norms",
            "||.||_q and ||.||_Z",
            "MISSING_OPERATOR_NORM_CONVENTIONS",
            "declare units and normalization so Dq_Z_norm is not a symbol with hidden dimensions",
        ),
        (
            "BLK1673_4_constraint_elimination",
            "constraint-first deletion",
            "MISSING_CONSTRAINT_ELIMINATION_THEOREM",
            "derive that Z is eliminated before matter/source/readout coupling, not patched away after",
        ),
        (
            "BLK1673_5_source_readout",
            "matter/source/readout descent",
            "MISSING_SOURCE_READOUT_DESCENT",
            "derive the quotient-invariant matter/source/readout action or retain finite leak",
        ),
        (
            "BLK1673_6_boundary",
            "boundary/projector flux",
            "MISSING_BOUNDARY_PROJECTOR_NO_FLUX",
            "prove no-flux or include boundary factor in the product bound",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "blocker_id": blocker_id,
            "missing_object": missing_object,
            "status": status,
            "why_it_matters": "without this object Dq_Z_norm cannot be zero-proved or source-bounded",
            "next_action": action,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for blocker_id, missing_object, status, action in data
    ]


def arena_requirement_rows() -> list[dict[str, object]]:
    data = [
        (
            "R0_identity_coframe_direct",
            "eta_WEP_direct_geometry",
            "eta_geom_AB <= Pi_R0*C_Obs_e*Dq_Z_norm*N_Z + retained source/readout terms",
            "needs Pi_R0, C_Obs_e, Dq_Z_norm, N_Z, and source/readout silence",
        ),
        (
            "R3_gamma",
            "gamma_minus_1",
            "|gamma-1| <= Pi_gamma*C_Obs_e*Dq_Z_norm*N_Z + calibration/RAB terms",
            "needs weak-field metric response matrix and q/Z norm conventions",
        ),
        (
            "R4_beta",
            "beta_minus_1",
            "|beta-1| <= Pi_beta*C_Obs_e*Dq_Z_norm*N_Z + source-normalization terms",
            "needs post-Newtonian response and Y5 source-current owner",
        ),
        (
            "R10_fifth_force",
            "alpha_pred(lambda)",
            "|alpha_pred(lambda)| <= Pi_R10(lambda)*C_Obs_e*Dq_Z_norm*N_Z plus sourced Yukawa coefficient chain",
            "needs R10 field map, source-backed bound curve, and Dq_Z_norm value",
        ),
        (
            "R11_EH_operator_ledger",
            "non_EH_local_operator_residual",
            "operator_residual <= Pi_R11*C_Obs_e*Dq_Z_norm*N_Z plus finite local operator factors",
            "needs EH limit operator basis and finite projection coefficients",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "arena": arena,
            "observable": observable,
            "factor_formula": formula,
            "required_inputs": required,
            "current_status": "BLOCKED_BY_DQZ_FACTOR_VALUE",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for arena, observable, formula, required in data
    ]


def decision_rows() -> list[dict[str, object]]:
    data = [
        (
            "D1673_0_zero_theorem",
            "ZERO_THEOREM_NOT_CLOSED",
            "Dq_Z_norm=0 needs q/Z/kernel/source/boundary clauses that are still unsigned",
            "do not use Dq_Z silence in any local-GR/Newton/PPN/R10 claim",
        ),
        (
            "D1673_1_factor_fill",
            "FINITE_VALUE_NOT_AVAILABLE",
            "no source-backed numeric or interval upper bound exists for Dq_Z_norm",
            "stage blocker ledger rather than fabricate a number",
        ),
        (
            "D1673_2_best_route",
            "BUILD_PARENT_Q_Z_BASIS",
            "the missing object is structural rather than a data table",
            "next build the minimal parent quotient map and Z basis, then compute Dq[Z]",
        ),
        (
            "D1673_3_safety",
            "NO_GR_NEWTON_CLAIM",
            "without Dq_Z_norm zero/value, the local branch remains closure-only",
            "keep claim gates false",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": action,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for decision_id, decision, reason, action in data
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        (
            "CG1673_0_zero",
            "Dq_Z_norm=0 theorem is parent-signed",
            False,
            "BLOCKED",
            "zero theorem remains conditional only",
        ),
        (
            "CG1673_1_value",
            "Dq_Z_norm finite value/interval is source-backed",
            False,
            "BLOCKED",
            "upper bound remains MISSING_SOURCE_BACKED_UPPER_BOUND",
        ),
        (
            "CG1673_2_local_GR",
            "local GR/Newton reduction follows through q/Z factor",
            False,
            "BLOCKED",
            "no q_loc, PPN, source, boundary, or coupling pass follows from current factor state",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate": gate,
            "gate_pass": gate_pass,
            "status": status,
            "reason": reason,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for gate_id, gate, gate_pass, status, reason in data
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1674-Y5-R2FR-parent-q-Z-basis-minimal-ansatz-and-Dq-computation.md",
            "script": "scripts/Y5_R2FR_parent_q_Z_basis_minimal_ansatz_and_Dq_computation.py",
            "objective": "construct the minimal local parent quotient map q(Phi), select the Z basis, declare q/Z norms, and compute or reject Dq[Z]",
            "success_condition": "Dq_Z_norm becomes theorem-zero from a parent-signed q/Z construction, or a finite nonclaim factor row becomes source-backed with no MISSING_* markers",
            "why_next": "1673 shows the missing piece is not another downstream test; it is the parent q and Z basis itself",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)


def validate() -> list[dict[str, object]]:
    source_register = read_csv(SOURCE_REGISTER)
    zero_conditions = read_csv(ZERO_CONDITIONS)
    zero_attempt = read_csv(ZERO_ATTEMPT)
    factor_value = read_csv(FACTOR_VALUE)
    blockers = read_csv(BLOCKER_LEDGER)
    arena = read_csv(ARENA_REQUIREMENTS)
    decision = read_csv(DECISION)
    claim = read_csv(CLAIM_GATE)
    next_targets = read_csv(NEXT_TARGET)

    sources_ok = all(bool_cell(row["exists"]) and bool_cell(row["needles_present"]) for row in source_register)
    zero_not_adopted = all(not bool_cell(row["theorem_zero_adopted"]) for row in zero_attempt)
    zero_verdict = any(row["attempt_id"] == "ZTA1673_3_verdict" and row["current_result"] == "ZERO_THEOREM_NOT_CLOSED" for row in zero_attempt)
    conditions_unsigned = all(not bool_cell(row["condition_met"]) and not bool_cell(row["parent_signed"]) for row in zero_conditions)
    factor_staged = (
        len(factor_value) == 1
        and factor_value[0]["symbol"] == "Dq_Z_norm"
        and factor_value[0]["candidate_value"] == "MISSING_NUMERIC_OR_THEOREM_ZERO"
        and factor_value[0]["upper_bound"] == "MISSING_SOURCE_BACKED_UPPER_BOUND"
    )
    blockers_complete = {"q(Phi)", "partial_ZA", "Dq[partial_ZA]", "||.||_q and ||.||_Z", "constraint-first deletion", "matter/source/readout descent", "boundary/projector flux"} == {row["missing_object"] for row in blockers}
    arena_complete = {"R0_identity_coframe_direct", "R3_gamma", "R4_beta", "R10_fifth_force", "R11_EH_operator_ledger"} == {row["arena"] for row in arena}
    decision_next = any(row["decision"] == "BUILD_PARENT_Q_Z_BASIS" for row in decision)
    claim_gate_safe = all(not bool_cell(row["gate_pass"]) and not bool_cell(row["claim_allowed"]) for row in claim)
    next_target_selected = next_targets[0]["next_target"] == "1674-Y5-R2FR-parent-q-Z-basis-minimal-ansatz-and-Dq-computation.md"
    csv_parse = all(path.exists() and len(read_csv(path)) >= 1 for path in GENERATED)
    branch_copies = all(target.exists() for targets in COPY_TARGETS.values() for target in targets)
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_clean = not any(FORMALIZATION.rglob("*1673*")) if FORMALIZATION.exists() else True

    no_claim_flags = True
    missing_not_claimed = True
    for path in CLAIM_CHECKED:
        for row in read_csv(path):
            if row.get("valid_for_claim", "False").lower() == "true" or row.get("claim_allowed", "False").lower() == "true":
                no_claim_flags = False
            if any(missing_marker(value) for value in row.values()):
                bad_keys = [
                    "valid_for_claim",
                    "claim_allowed",
                    "score_ready",
                    "accepted_for_scoring",
                    "prediction_source_backed",
                    "valid_prediction_row",
                ]
                for key in bad_keys:
                    if key in row and bool_cell(row[key]):
                        missing_not_claimed = False

    checks = [
        ("VAL1673_0_sources_exist", sources_ok, "all cited 1673 source paths exist and needles are present"),
        ("VAL1673_1_conditions_unsigned", conditions_unsigned, "zero theorem clauses remain unsigned"),
        ("VAL1673_2_zero_not_adopted", zero_not_adopted, "Dq_Z theorem-zero is not adopted"),
        ("VAL1673_3_zero_verdict", zero_verdict, "zero theorem verdict remains not closed"),
        ("VAL1673_4_factor_value_staged", factor_staged, "Dq_Z_norm factor value row is staged as missing"),
        ("VAL1673_5_blockers_complete", blockers_complete, "blocker ledger covers q/Z/Dq/norm/constraint/source/boundary"),
        ("VAL1673_6_arena_requirements", arena_complete, "arena requirements include R0/R3/R4/R10/R11"),
        ("VAL1673_7_decision_next", decision_next, "decision selects parent q/Z basis construction"),
        ("VAL1673_8_claim_gate_safe", claim_gate_safe, "all claim gates keep local claims false"),
        ("VAL1673_9_no_claim_flags", no_claim_flags, "all generated rows keep claim flags false"),
        ("VAL1673_10_missing_not_ready", missing_not_claimed, "no MISSING row is marked claim/scoring/source ready"),
        ("VAL1673_11_next_target_selected", next_target_selected, "next target selects parent q/Z basis and Dq computation"),
        ("VAL1673_12_csv_parse", csv_parse, "all generated 1673 CSVs parse"),
        ("VAL1673_13_branch_copies", branch_copies, "branch/quarantine/queue copies exist"),
        ("VAL1673_14_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL1673_15_formalization_untouched", formalization_clean, "no 1673 outputs found under formalization-workbench"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1673_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1673 Dq_Z zero theorem or first factor value-fill validation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    source_rows: list[dict[str, object]],
    condition_rows: list[dict[str, object]],
    attempt_rows: list[dict[str, object]],
    factor_rows: list[dict[str, object]],
    blocker_rows_: list[dict[str, object]],
    arena_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    text = f"""# 1673 - DqZ Zero Theorem Or First Factor Value Fill

**Private status:** derivation-first checkpoint. No `q_loc=0`, local-GR pass, Newton pass, PPN pass, R10 pass, WEP pass, clock pass, orbital pass, or public claim is made.

## Verdict

`Dq_Z_norm=0` is **not proved** from the current source state.

The useful theorem shape is now exact:

```text
If q(Phi) factorizes through variables independent of every selected Z direction,
and selected partial_ZA are constraint-tangent elements of ker(Dq),
and matter/source/readout/boundary data descend through that same quotient,
then Dq_Z_norm = 0.
```

The current corpus does not yet supply the parent `q(Phi)`, the live `Z` basis, the `Dq[partial_Z]` matrix, or the matter/source/boundary silence needed to sign it.

The fallback value row is also **not filled**: `Dq_Z_norm` remains `MISSING_NUMERIC_OR_THEOREM_ZERO`, with upper bound `MISSING_SOURCE_BACKED_UPPER_BOUND`.

## Source Register

{markdown_table(source_rows, ["source_key", "source_path", "exists", "needles_present", "use_in_1673"])}

## Zero-Theorem Conditions

{markdown_table(condition_rows, ["condition_id", "condition", "current_evidence", "status", "next_action"])}

## Zero-Theorem Attempt

{markdown_table(attempt_rows, ["attempt_id", "route", "current_result", "blocking_issue"])}

## DqZ Factor Value Fill

{markdown_table(factor_rows, ["row_id", "symbol", "definition", "candidate_value", "upper_bound", "current_status"])}

## Blocker Ledger

{markdown_table(blocker_rows_, ["blocker_id", "missing_object", "status", "next_action"])}

## Arena Requirements

{markdown_table(arena_rows, ["arena", "observable", "factor_formula", "current_status"])}

## Decisions

{markdown_table(decision_rows_, ["decision_id", "decision", "reason", "next_action"])}

## Claim Gates

{markdown_table(claim_rows, ["gate_id", "gate", "gate_pass", "status", "reason"])}

## Next Target

{markdown_table(next_rows, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Working Interpretation

This is not a defeat; it is the trapdoor under the floorboards finally labelled. `Dq_Z_norm` cannot be magicked to zero, and it cannot be scored as a finite empirical factor yet. The cleanest attack is upstream: build the parent quotient map and the actual `Z` basis, then compute `Dq[Z]`. If that computation gives zero, the local branch gets teeth. If it does not, we stop pretending it is silent and bound the leak honestly.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    sources = source_register_rows()
    conditions = zero_conditions_rows()
    attempts = zero_attempt_rows()
    factors = factor_value_rows()
    blockers = blocker_rows()
    arenas = arena_requirement_rows()
    decisions = decision_rows()
    claims = claim_gate_rows()
    next_targets = next_target_rows()

    write_csv(
        SOURCE_REGISTER,
        sources,
        ["branch_id", "source_key", "source_path", "exists", "needles_present", "required_needles", "use_in_1673", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        ZERO_CONDITIONS,
        conditions,
        ["branch_id", "theorem_label", "formal_statement", "condition_id", "condition", "current_evidence", "status", "next_action", "condition_met", "parent_signed", "theorem_closed_for_claim", "accepted_for_scoring", "score_ready", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        ZERO_ATTEMPT,
        attempts,
        ["branch_id", "attempt_id", "route", "candidate_derivation", "required_inputs", "current_result", "blocking_issue", "theorem_zero_adopted", "finite_value_present", "prediction_source_backed", "accepted_for_scoring", "score_ready", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        FACTOR_VALUE,
        factors,
        ["branch_id", "row_id", "symbol", "definition", "units", "value_type", "candidate_value", "lower_bound", "upper_bound", "source_paths", "required_source_inputs", "projection_formula", "current_status", "promotion_rule", "theorem_zero_adopted", "finite_value_present", "prediction_source_backed", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        BLOCKER_LEDGER,
        blockers,
        ["branch_id", "blocker_id", "missing_object", "status", "why_it_matters", "next_action", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        ARENA_REQUIREMENTS,
        arenas,
        ["branch_id", "arena", "observable", "factor_formula", "required_inputs", "current_status", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        DECISION,
        decisions,
        ["branch_id", "decision_id", "decision", "reason", "next_action", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        CLAIM_GATE,
        claims,
        ["branch_id", "gate_id", "gate", "gate_pass", "status", "reason", "claim_allowed", "valid_for_claim"],
    )
    write_csv(
        NEXT_TARGET,
        next_targets,
        ["branch_id", "next_target", "script", "objective", "success_condition", "why_next", "valid_for_claim", "claim_allowed"],
    )

    copy_outputs()
    validation = validate()
    write_csv(VALIDATION, validation, ["check_id", "result", "detail", "valid_for_claim", "claim_allowed"])
    write_doc(sources, conditions, attempts, factors, blockers, arenas, decisions, claims, next_targets, validation)

    failed = [row for row in validation if row["result"] != "PASS"]
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("1673 validation PASS")


if __name__ == "__main__":
    main()
