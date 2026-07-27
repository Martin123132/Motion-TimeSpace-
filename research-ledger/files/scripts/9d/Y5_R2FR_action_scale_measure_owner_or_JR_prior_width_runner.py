from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1630"
INPUT_1630 = QUARANTINE / "input"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1630-Y5-R2FR-action-scale-measure-owner-or-JR-prior-width-runner.md"

SOURCE_FILES = {
    "1629_doc": ROOT / "1629-Y5-R2FR-RAB-source-slot-exclusion-or-finite-JR-prior-width.md",
    "1629_validation": OUT / "P8_Y5_BRR545_1629_VALIDATION.csv",
    "1629_next": OUT / "P8_Y5_PARENT_QLOC_1629_NEXT_TARGET.csv",
    "1629_slot_attempt": OUT / "P8_Y5_PARENT_QLOC_1629_RAB_SOURCE_SLOT_EXCLUSION_ATTEMPT.csv",
    "1629_prior_widths": OUT / "P8_Y5_PARENT_QLOC_1629_FINITE_JR_PIR_PRIOR_WIDTH_ROWS.csv",
    "1067_action_scale": OUT / "P8_Y5_R10_1067_PARENT_ACTION_SCALE_OWNER_ATTEMPT.csv",
    "1088_minimal_signature": OUT / "P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv",
    "1088_conditional_zero": OUT / "P8_Y5_R10_1088_CONDITIONAL_ZERO_THEOREM.csv",
    "1090_synthesis": OUT / "P8_Y5_R10_1090_SYNTHESIS_ATTEMPT.csv",
    "1090_missing_axioms": OUT / "P8_Y5_R10_1090_MISSING_AXIOM_LEDGER.csv",
    "1090_closure": OUT / "P8_Y5_R10_1090_CLOSURE_DEMOTION_REGISTER.csv",
    "1447_parent_object": OUT / "P8_Y5_R10_1447_AX1090_PARENT_OBJECT_PROOF_ATTEMPT.csv",
    "1214_no_source_slot": ROOT / "1214-Y5-R10-no-source-only-slot-parent-signature-or-Delta-species-bound-fill.md",
}

NEEDLES = {
    "1629_doc": ["NEXT_1630_ACTION_SCALE_MEASURE_OWNER_OR_JR_PRIOR_RUNNER", "VAL1629_OVERALL"],
    "1629_validation": ["VAL1629_OVERALL", "PASS"],
    "1629_next": ["1630-Y5-R2FR-action-scale-measure-owner-or-JR-prior-width-runner.md", "action-scale/measure owner"],
    "1629_slot_attempt": ["RSE1629_4_action_scale_owner", "ACTION_SCALE_OWNER_NOT_PARENT_SIGNED"],
    "1629_prior_widths": ["PW1629_0_epsilon_RAB_source", "MISSING_RAB_SOURCE_SLOT_ZERO_OR_PRIOR_WIDTH"],
    "1067_action_scale": ["ASO1067_5_verdict", "CONDITIONAL_NOT_PARENT_DERIVED"],
    "1088_minimal_signature": ["MOMS1088_7_verdict", "MINIMAL_PARENT_ORDINARY_MATTER_SIGNATURE_NOT_DERIVED"],
    "1088_conditional_zero": ["THM1088_6_current_corpus_verdict", "CONDITIONAL_ZERO_THEOREM_NOT_PROMOTED"],
    "1090_synthesis": ["SYN1090_8_verdict", "SYNTHESIS_FAILS_MISSING_AXIOMS"],
    "1090_missing_axioms": ["AX1090_2_common_quantum_measure", "MISSING_AXIOM_NOT_ADOPTED"],
    "1090_closure": ["CLOS1090_0_MOMS", "closure_candidate_not_adopted"],
    "1447_parent_object": ["AXP1447_3_verdict", "PARENT_OBJECT_NOT_PROVEN"],
    "1214_no_source_slot": ["NSS1214_2_action_measure_owner", "NOT_PARENT_SIGNED"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1630_SOURCE_REGISTER.csv"
ACTION_SCALE_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1630_ACTION_SCALE_MEASURE_OWNER_AUDIT.csv"
AXIOM_REDUCTION_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1630_AX1090_REDUCTION_STATUS.csv"
PRIOR_WIDTH_INPUTS = OUT / "P8_Y5_PARENT_QLOC_1630_PRIOR_WIDTH_RUNNER_INPUTS.csv"
REFUSAL_RUNNER = OUT / "P8_Y5_PARENT_QLOC_1630_PRIOR_WIDTH_REFUSAL_RUNNER.csv"
BLOCKER_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1630_BLOCKER_LEDGER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1630_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1630_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1630_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1630_VALIDATION.csv"

COPY_TARGETS = {
    ACTION_SCALE_AUDIT: [
        QUARANTINE / "ACTION_SCALE_MEASURE_OWNER_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_action_scale_measure_owner_audit_nonclaim_1630.csv",
    ],
    AXIOM_REDUCTION_AUDIT: [
        QUARANTINE / "AX1090_REDUCTION_STATUS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_AX1090_reduction_status_nonclaim_1630.csv",
    ],
    PRIOR_WIDTH_INPUTS: [
        QUARANTINE / "PRIOR_WIDTH_RUNNER_INPUTS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_prior_width_runner_inputs_nonclaim_1630.csv",
    ],
    REFUSAL_RUNNER: [
        QUARANTINE / "PRIOR_WIDTH_REFUSAL_RUNNER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_prior_width_refusal_runner_nonclaim_1630.csv",
        QUEUE / "JR1630_PRIOR_WIDTH_REFUSAL_RUNNER_NONCLAIM.csv",
    ],
    BLOCKER_LEDGER: [
        QUARANTINE / "BLOCKER_LEDGER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_blocker_ledger_nonclaim_1630.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE_CLOSED.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_closed_1630.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_1630.csv",
    ],
}


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def file_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def all_needles_found(source_id: str) -> bool:
    text = file_text(SOURCE_FILES[source_id])
    return all(needle in text for needle in NEEDLES[source_id])


def ensure_dirs() -> None:
    for directory in [OUT, INPUT_1630, BRANCH_RESIDUALS, QUEUE]:
        directory.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv(path)
    except Exception:
        return False
    return True


def bool_str(value: Any) -> str:
    return str(value).strip().lower()


def row_has_true_claim_flag(row: dict[str, Any]) -> bool:
    for field in ["score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed", "parent_signed", "accepted_as_zero", "accepted_for_scoring"]:
        if field in row and bool_str(row[field]) == "true":
            return True
    return False


def source_register_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "source_id": source_id,
            "source_path": rel(path),
            "exists": path.exists(),
            "required_needles": "; ".join(NEEDLES[source_id]),
            "needles_found": all_needles_found(source_id),
            "role": "1630 action-scale/measure owner and prior-width runner provenance",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for source_id, path in SOURCE_FILES.items()
    ]


def action_scale_audit_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "ASR1630_0_target",
            "universal parent action-scale/measure owner",
            "one hbar/action measure/current normalization applies to all ordinary matter sectors and source couplings",
            "TARGET_SHARPENED",
            "would make inert R_AB source-only multipliers impossible or common-calibrated",
        ),
        (
            "ASR1630_1_classical_scaling",
            "classical EOM scaling is not enough",
            "delta(w_A S_A)/delta Psi_A can preserve matter EOM while delta(w_A S_A)/delta e_obs rescales Hilbert source",
            "OBSTRUCTION_EXPLICIT",
            "reuses ASO1067_1; field equations alone cannot prove source coupling silence",
        ),
        (
            "ASR1630_2_quantum_measure",
            "quantum/statistical path measure owner",
            "exp(i sum_A w_A S_A/hbar_parent) is physically distinct unless the parent measure quotients it",
            "AX1090_2_MISSING",
            "the exact missing axiom is common quantum/action measure ownership",
        ),
        (
            "ASR1630_3_field_redefinition",
            "field redefinition loophole",
            "canonical rescaling must preserve interactions, composite parameters, Hilbert source, and measure simultaneously",
            "NOT_CLOSED_BY_RESCALING",
            "source-only weights cannot be dismissed as notation",
        ),
        (
            "ASR1630_4_MOMS",
            "minimal ordinary-matter signature",
            "MOMS would close no source weights, no shadow/domain, and matter descent together",
            "CLOSURE_CANDIDATE_NOT_ADOPTED",
            "MOMS1088 is exact as a closure branch but not parent-derived",
        ),
        (
            "ASR1630_5_parent_object",
            "single parent action object",
            "one parent object must fix fields, variation domain, symplectic potential, matter/source/readout coupling before projection",
            "PARENT_OBJECT_NOT_PROVEN",
            "AX1090_0 remains unproved in 1447",
        ),
        (
            "ASR1630_6_verdict",
            "action-scale/measure owner theorem",
            "ASR1630_0 through ASR1630_5 all parent-signed",
            "ACTION_SCALE_MEASURE_OWNER_NOT_DERIVED_CURRENT_CORPUS",
            "switch to executable finite-prior refusal runner",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "claim_piece": claim_piece,
            "formal_statement": statement,
            "status": status,
            "effect": effect,
            "parent_signed": False,
            "accepted_as_zero": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for audit_id, claim_piece, statement, status, effect in rows
    ]


def axiom_reduction_rows() -> list[dict[str, Any]]:
    rows = [
        ("AX1630_0_parent_object", "AX1090_0_parent_object", "one parent action object before readout", "PARENT_OBJECT_NOT_PROVEN", "1447 says sector/MOMS reductions fail"),
        ("AX1630_1_no_hidden_visible_hom", "AX1090_1_no_hidden_visible_hom", "no hidden-to-visible coefficient morphism", "MISSING_AXIOM_NOT_ADOPTED", "needed to forbid shadow/source slots"),
        ("AX1630_2_common_quantum_measure", "AX1090_2_common_quantum_measure", "one hbar/action measure/current normalization", "MISSING_AXIOM_NOT_ADOPTED", "the direct action-scale bottleneck"),
        ("AX1630_3_fixed_constant_sector", "AX1090_3_fixed_constant_sector", "ordinary constants fixed or retained explicitly", "MISSING_AXIOM_NOT_ADOPTED", "prevents hidden matter constants from acting as source currents"),
        ("AX1630_4_variation_domain_order", "AX1090_4_variation_domain_order", "variation before readout/projection/fitting", "MISSING_AXIOM_NOT_ADOPTED", "prevents post-variation source selectors"),
        ("AX1630_5_verdict", "AX1090 bundle", "derive all AX1090 clauses from MTS primitives", "AX1090_BUNDLE_NOT_REDUCED", "MOMS remains closure-only, not a theorem"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "reduction_id": reduction_id,
            "axiom": axiom,
            "role": role,
            "status": status,
            "effect": effect,
            "parent_signed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for reduction_id, axiom, role, status, effect in rows
    ]


def prior_width_input_rows() -> list[dict[str, Any]]:
    rows = []
    for row in read_csv(SOURCE_FILES["1629_prior_widths"]):
        missing_fields = []
        if "MISSING" in row.get("formula_or_requirement", ""):
            missing_fields.append("formula_or_requirement")
        if "MISSING" in row.get("status", ""):
            missing_fields.append("status")
        if "MISSING" in row.get("source_path", ""):
            missing_fields.append("source_path")
        if "MISSING" in row.get("source_anchor", ""):
            missing_fields.append("source_anchor")
        if row.get("numeric_value_present") != "True":
            missing_fields.append("numeric_value_present")
        if row.get("source_backed") != "True":
            missing_fields.append("source_backed")
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "runner_input_id": row["prior_width_id"].replace("PW1629", "PWI1630"),
                "source_prior_width_id": row["prior_width_id"],
                "quantity": row["quantity"],
                "units": row["units"],
                "formula_or_requirement": row["formula_or_requirement"],
                "arena_projection": row["arena_projection"],
                "source_path": row["source_path"],
                "source_anchor": row["source_anchor"],
                "missing_fields": ";".join(missing_fields),
                "input_status": "MISSING_INPUT_REJECTED",
                "accepted_for_scoring": False,
                "numeric_value_present": False,
                "source_backed": False,
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def refusal_runner_rows() -> list[dict[str, Any]]:
    rows = []
    for row in prior_width_input_rows():
        reasons = []
        if "source_path" in row["missing_fields"]:
            reasons.append("MISSING_LOCAL_SOURCE_PATH")
        if "source_anchor" in row["missing_fields"]:
            reasons.append("MISSING_SOURCE_ANCHOR")
        if "numeric_value_present" in row["missing_fields"]:
            reasons.append("MISSING_NUMERIC_OR_THEOREM_ZERO_VALUE")
        if "source_backed" in row["missing_fields"]:
            reasons.append("MISSING_SOURCE_BACKING")
        if row["quantity"].startswith("tau_") and "MISSING" in row["formula_or_requirement"]:
            reasons.append("MISSING_ARENA_KERNEL_OR_BOUND")
        if row["quantity"] in {"epsilon_RAB_source", "J_R", "Pi_R", "Q_R"}:
            reasons.append("MISSING_ZERO_THEOREM_OR_FINITE_PRIOR_WIDTH")
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "runner_row_id": row["runner_input_id"].replace("PWI", "RUN"),
                "quantity": row["quantity"],
                "runner_decision": "REFUSE_SCORING",
                "refusal_reasons": ";".join(sorted(set(reasons))),
                "required_to_accept": "numeric/theorem-zero value; units; source_path; source_anchor; normalization; arena kernel when applicable",
                "observable_gate": row["arena_projection"],
                "accepted_for_scoring": False,
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_row_id": "RUN1630_7_local_GR_lock",
            "quantity": "local_GR_Newton_recovery",
            "runner_decision": "REFUSE_SCORING",
            "refusal_reasons": "ACTION_SCALE_MEASURE_OWNER_NOT_DERIVED;RAB_SOURCE_SLOT_EXCLUSION_NOT_DERIVED;FINITE_PRIOR_WIDTHS_MISSING",
            "required_to_accept": "parent theorem-zero or complete finite-prior arena comparison branch",
            "observable_gate": "local_GR;Newton;PPN;R10;clock;orbital",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def blocker_rows() -> list[dict[str, Any]]:
    blockers = [
        ("BLK1630_0_action_scale", "action-scale/measure owner", "ACTION_SCALE_MEASURE_OWNER_NOT_DERIVED_CURRENT_CORPUS", "AX1090_2_common_quantum_measure remains missing", "derive from parent primitives or keep closure-only"),
        ("BLK1630_1_parent_object", "single parent action object", "PARENT_OBJECT_NOT_PROVEN", "AX1090_0 and 1447 parent-object proof remain failed", "derive one parent object before readout"),
        ("BLK1630_2_MOMS", "MOMS ordinary-matter signature", "CLOSURE_CANDIDATE_NOT_ADOPTED", "MOMS1088_7 is exact but not parent-derived", "do not use as theorem-zero"),
        ("BLK1630_3_prior_widths", "finite prior-width branch", "PRIOR_WIDTH_RUNNER_REFUSES_ALL_ROWS", "all 1629 widths lack numeric/source-backed values and source anchors", "source first real width/kernel row"),
        ("BLK1630_4_arena_kernels", "tau projection kernels", "MISSING_ARENA_KERNELS", "tau_R10/tau_PPN/tau_clock/tau_orbital maps remain missing", "derive or source projection kernels"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "blocker_id": blocker_id,
            "target": target,
            "status": status,
            "missing_for_claim": missing,
            "next_action": next_action,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for blocker_id, target, status, missing, next_action in blockers
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    claims = [
        ("CG1630_0_action_scale", "action-scale/measure owner theorem", "BLOCKED", "AX1090_2 and parent object are missing"),
        ("CG1630_1_RAB_slot", "R_AB source-slot exclusion", "BLOCKED", "action-scale and object-language clauses unsigned"),
        ("CG1630_2_prior_runner", "finite prior-width rows scoreable", "BLOCKED", "runner refuses all missing/source-unbacked rows"),
        ("CG1630_3_arena", "R10/PPN/clock/orbital comparisons", "BLOCKED", "tau kernels and numeric widths missing"),
        ("CG1630_4_local_GR", "derived local GR/Newton recovery", "BLOCKED", "neither theorem-zero nor finite comparison branch is closed"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim, status, reason in claims
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1630_0_theorem",
            "decision": "ACTION_SCALE_MEASURE_OWNER_NOT_DERIVED_CURRENT_CORPUS",
            "reason": "1067/1090/1214 already isolate the missing common quantum/action-measure owner and keep it unsigned",
            "next_action": "do not recycle MOMS as proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1630_1_runner",
            "decision": "PRIOR_WIDTH_REFUSAL_RUNNER_BUILT",
            "reason": "finite epsilon_RAB_source/J_R/Pi_R/Q_R/tau rows now have an executable refusal ledger",
            "next_action": "source real prior-width or tau-kernel rows before any scoring",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1630_2_next",
            "decision": "NEXT_1631_JR_PRIOR_WIDTH_SOURCE_ACQUISITION_OR_TAU_KERNEL_FIRST_ROW",
            "reason": "the theorem route is stalled at a named missing axiom; the empirical finite branch needs first source-backed input",
            "next_action": "hunt for source-backed prior widths or derive/source tau_R10 first",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1631-Y5-R2FR-JR-prior-width-source-acquisition-or-tau-kernel-first-row.md",
            "script": "scripts/Y5_R2FR_JR_prior_width_source_acquisition_or_tau_kernel_first_row.py",
            "objective": "hunt for the first source-backed finite input for epsilon_RAB_source, J_R, Pi_R, Q_R, or tau_R10/tau_PPN/tau_clock/tau_orbital; if none exists, write a precise acquisition blocker ledger without scoring",
            "success_condition": "at least one source-backed nonclaim row passes 1630 refusal gates, or the missing source/kernel is identified exactly",
            "do_not": "do not adopt MOMS closure as proof, do not score missing widths, do not invent numeric priors, do not claim local GR/Newton/R10/PPN/clock/orbital pass",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def generated_paths() -> list[Path]:
    return [
        SOURCE_REGISTER,
        ACTION_SCALE_AUDIT,
        AXIOM_REDUCTION_AUDIT,
        PRIOR_WIDTH_INPUTS,
        REFUSAL_RUNNER,
        BLOCKER_LEDGER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
    for source_id, source in SOURCE_FILES.items():
        if source.exists():
            shutil.copyfile(source, INPUT_1630 / f"{source_id}{source.suffix}")


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows() -> list[dict[str, Any]]:
    paths = generated_paths()
    action_rows = read_csv(ACTION_SCALE_AUDIT)
    axiom_rows = read_csv(AXIOM_REDUCTION_AUDIT)
    input_rows = read_csv(PRIOR_WIDTH_INPUTS)
    runner_rows = read_csv(REFUSAL_RUNNER)
    blocker_data = read_csv(BLOCKER_LEDGER)
    claim_rows = read_csv(CLAIM_GATE)
    decision_text = file_text(DECISION)
    next_text = file_text(NEXT_TARGET)
    all_rows: list[dict[str, Any]] = []
    for path in paths:
        all_rows.extend(read_csv(path))

    source_ok = all(path.exists() for path in SOURCE_FILES.values())
    needles_ok = all(all_needles_found(source_id) for source_id in SOURCE_FILES)
    theorem_blocked = any(row["audit_id"] == "ASR1630_6_verdict" and row["status"] == "ACTION_SCALE_MEASURE_OWNER_NOT_DERIVED_CURRENT_CORPUS" for row in action_rows)
    ax1090_blocked = any(row["reduction_id"] == "AX1630_5_verdict" and row["status"] == "AX1090_BUNDLE_NOT_REDUCED" for row in axiom_rows)
    inputs_cover = {row["quantity"] for row in input_rows} == {
        "epsilon_RAB_source",
        "J_R",
        "Pi_R",
        "Q_R",
        "tau_R10[J_R/Pi_R/Q_R]",
        "tau_PPN[J_R/Pi_R/Q_R]",
        "tau_clock/tau_orbital[J_R/Pi_R/Q_R]",
    }
    all_inputs_rejected = all(row["input_status"] == "MISSING_INPUT_REJECTED" and row["accepted_for_scoring"] == "False" for row in input_rows)
    runner_refuses_all = len(runner_rows) == 8 and all(row["runner_decision"] == "REFUSE_SCORING" and row["accepted_for_scoring"] == "False" for row in runner_rows)
    blocker_cover = {row["target"] for row in blocker_data} == {
        "action-scale/measure owner",
        "single parent action object",
        "MOMS ordinary-matter signature",
        "finite prior-width branch",
        "tau projection kernels",
    }
    claim_closed = all(row["status"] == "BLOCKED" and not row_has_true_claim_flag(row) for row in claim_rows)
    nonclaim_ok = all(not row_has_true_claim_flag(row) for row in all_rows)
    decision_next = "NEXT_1631_JR_PRIOR_WIDTH_SOURCE_ACQUISITION_OR_TAU_KERNEL_FIRST_ROW" in decision_text
    next_selected = "1631-Y5-R2FR-JR-prior-width-source-acquisition-or-tau-kernel-first-row.md" in next_text
    branch_copies = all(target.exists() for targets in COPY_TARGETS.values() for target in targets)
    csv_ok = all(csv_parses(path) for path in paths)
    pycache_absent = not (Path(__file__).resolve().parent / "__pycache__").exists()
    formalization_clean = not any((FORMALIZATION / path.name).exists() for path in [DOC, *paths]) if FORMALIZATION.exists() else True

    checks = [
        ("VAL1630_0_sources_exist", source_ok, "all cited 1630 local source paths exist"),
        ("VAL1630_1_needles_found", needles_ok, "all required 1630 source needles found"),
        ("VAL1630_2_theorem_blocked", theorem_blocked, "action-scale/measure owner remains not derived"),
        ("VAL1630_3_ax1090_blocked", ax1090_blocked, "AX1090 bundle remains unreduced"),
        ("VAL1630_4_inputs_cover", inputs_cover, "runner inputs cover epsilon_RAB_source, J_R, Pi_R, Q_R, and tau projections"),
        ("VAL1630_5_all_inputs_rejected", all_inputs_rejected, "all prior-width inputs are rejected as missing/source-unbacked"),
        ("VAL1630_6_runner_refuses_all", runner_refuses_all, "refusal runner blocks all rows plus local-GR lock"),
        ("VAL1630_7_blocker_coverage", blocker_cover, "blocker ledger covers theorem and finite branch blockers"),
        ("VAL1630_8_claim_gates_closed", claim_closed, "all claim gates remain blocked"),
        ("VAL1630_9_nonclaim_flags", nonclaim_ok, "all generated 1630 rows remain nonclaim/non-score-ready"),
        ("VAL1630_10_decision_next", decision_next, "decision selects source acquisition or tau-kernel first row next"),
        ("VAL1630_11_next_target_selected", next_selected, "next target selected"),
        ("VAL1630_12_branch_copies", branch_copies, "branch/quarantine/acquisition queue nonclaim copies exist"),
        ("VAL1630_13_csv_parse", csv_ok, "all generated 1630 CSVs parse"),
        ("VAL1630_14_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL1630_15_formalization_untouched", formalization_clean, "no 1630 outputs found under formalization-workbench"),
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
            "check_id": "VAL1630_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1630 action-scale measure owner or J_R prior-width runner validation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, str]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines)


def write_doc() -> None:
    source_rows = read_csv(SOURCE_REGISTER)
    action_rows = read_csv(ACTION_SCALE_AUDIT)
    axiom_rows = read_csv(AXIOM_REDUCTION_AUDIT)
    input_rows = read_csv(PRIOR_WIDTH_INPUTS)
    runner_rows = read_csv(REFUSAL_RUNNER)
    blockers = read_csv(BLOCKER_LEDGER)
    claims = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_target = read_csv(NEXT_TARGET)
    validation = read_csv(VALIDATION)

    content = f"""# 1630 — Action-Scale Measure Owner Or `J_R` Prior-Width Runner

## Status

Private checkpoint. No action-scale theorem, `R_AB` source-slot theorem, `J_R=0`, finite prior-width score, local-GR/Newton, R10, PPN, clock, or orbital claim is made.

## Outcome

The theorem route is named and blocked: a universal parent action-scale/measure owner would forbid inert `R_AB` source-only multipliers, but current corpus keeps `AX1090_2_common_quantum_measure` and the parent action object unsigned. `MOMS` remains a closure candidate, not a theorem. The finite branch now has an executable refusal runner: every `epsilon_RAB_source/J_R/Pi_R/Q_R/tau` row from `1629` is rejected until it has numeric/theorem-zero value, units, source path, source anchor, normalization, and arena kernels.

## Source Register

{markdown_table(source_rows, ["source_id", "source_path", "exists", "needles_found"])}

## Action-Scale Measure Owner Audit

{markdown_table(action_rows, ["audit_id", "claim_piece", "status", "effect"])}

## AX1090 Reduction Status

{markdown_table(axiom_rows, ["reduction_id", "axiom", "status", "effect"])}

## Prior-Width Runner Inputs

{markdown_table(input_rows, ["runner_input_id", "quantity", "input_status", "missing_fields"])}

## Refusal Runner

{markdown_table(runner_rows, ["runner_row_id", "quantity", "runner_decision", "refusal_reasons"])}

## Blocker Ledger

{markdown_table(blockers, ["blocker_id", "target", "status", "missing_for_claim"])}

## Claim Gates

{markdown_table(claims, ["gate_id", "claim", "status", "reason"])}

## Decision

{markdown_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Next Target

{markdown_table(next_target, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    outputs = {
        SOURCE_REGISTER: source_register_rows(),
        ACTION_SCALE_AUDIT: action_scale_audit_rows(),
        AXIOM_REDUCTION_AUDIT: axiom_reduction_rows(),
        PRIOR_WIDTH_INPUTS: prior_width_input_rows(),
        REFUSAL_RUNNER: refusal_runner_rows(),
        BLOCKER_LEDGER: blocker_rows(),
        CLAIM_GATE: claim_gate_rows(),
        DECISION: decision_rows(),
        NEXT_TARGET: next_target_rows(),
    }
    for path, rows in outputs.items():
        write_csv(path, rows)

    copy_outputs()
    remove_pycache()
    write_csv(VALIDATION, validation_rows())
    write_doc()
    remove_pycache()
    print(f"wrote {rel(DOC)}")
    print(f"validation {rel(VALIDATION)}")


if __name__ == "__main__":
    main()
