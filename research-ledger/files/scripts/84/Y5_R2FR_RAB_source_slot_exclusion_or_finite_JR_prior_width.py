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
QUARANTINE = MICROSCOPE / "quarantine" / "1629"
INPUT_1629 = QUARANTINE / "input"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1629-Y5-R2FR-RAB-source-slot-exclusion-or-finite-JR-prior-width.md"

SOURCE_FILES = {
    "1628_doc": ROOT / "1628-Y5-R2FR-matter-descent-source-owner-certificate-or-JR-bound-acquisition.md",
    "1628_validation": OUT / "P8_Y5_BRR545_1628_VALIDATION.csv",
    "1628_next": OUT / "P8_Y5_PARENT_QLOC_1628_NEXT_TARGET.csv",
    "1628_certificate": OUT / "P8_Y5_PARENT_QLOC_1628_SOURCE_OWNER_CERTIFICATE_ATTEMPT.csv",
    "1628_acquisition": OUT / "P8_Y5_PARENT_QLOC_1628_JR_BOUND_ACQUISITION_LEDGER.csv",
    "1027_qbar": ROOT / "1027-Y5-R10-qbarXT-source-zero-or-bounded-coupling-row.md",
    "1030_single_public": ROOT / "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md",
    "1065_no_source_slot": ROOT / "1065-Y5-R10-no-source-only-slot-parent-grammar-or-first-relative-weight-numeric-row.md",
    "1066_source_scalar": ROOT / "1066-Y5-R10-parent-action-syntax-source-scalar-exclusion-or-WEP-Delta-w-prior-width.md",
    "1079_current_owner": ROOT / "1079-Y5-R10-parent-current-owner-narrow-proof-or-finite-WEP-source-vector.md",
    "1087_matter_descent": ROOT / "1087-Y5-R10-parent-matter-descent-zero-current-or-DD-coefficient-source-pack.md",
}

NEEDLES = {
    "1628_doc": ["NEXT_1629_RAB_SOURCE_SLOT_EXCLUSION_OR_FINITE_JR_PRIOR_WIDTH", "VAL1628_OVERALL"],
    "1628_validation": ["VAL1628_OVERALL", "PASS"],
    "1628_next": ["1629-Y5-R2FR-RAB-source-slot-exclusion-or-finite-JR-prior-width.md", "R_AB source-slot exclusion"],
    "1628_certificate": ["SOC1628_2_no_RAB_argument", "SOURCE_OWNER_CERTIFICATE_NOT_CLOSED_CURRENT_CORPUS"],
    "1628_acquisition": ["JRA1628_1_finite_JR_bound", "MISSING_NUMERIC_JR_SOURCE_BOUND"],
    "1027_qbar": ["QZ1027_3_matter_functor", "EXACT_CONTRACT_NOT_PARENT_SIGNED"],
    "1030_single_public": ["SPM1030_1_matter_functor_domain", "CONTRACT_WRITTEN_NOT_PARENT_SIGNED"],
    "1065_no_source_slot": ["PGG1065_1_no_inert_species_scalar", "CONDITIONAL_GRAMMAR_NOT_PARENT_SIGNED"],
    "1066_source_scalar": ["SSE1066_5_verdict", "CONDITIONAL_SOURCE_SCALAR_EXCLUSION_NOT_PARENT_DERIVED"],
    "1079_current_owner": ["NCO1079_5_species_action_weight", "SURVIVES_PRE_VARIATION"],
    "1087_matter_descent": ["PMD1087_4_pre_action_weights", "PRE_ACTION_WEIGHT_LEAK_SURVIVES"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1629_SOURCE_REGISTER.csv"
RAB_SLOT_EXCLUSION = OUT / "P8_Y5_PARENT_QLOC_1629_RAB_SOURCE_SLOT_EXCLUSION_ATTEMPT.csv"
OBSTRUCTION_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1629_RAB_SLOT_OBSTRUCTION_LEDGER.csv"
FINITE_PRIOR_WIDTHS = OUT / "P8_Y5_PARENT_QLOC_1629_FINITE_JR_PIR_PRIOR_WIDTH_ROWS.csv"
RUNNER_GATES = OUT / "P8_Y5_PARENT_QLOC_1629_PRIOR_WIDTH_RUNNER_GATES.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1629_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1629_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1629_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1629_VALIDATION.csv"

COPY_TARGETS = {
    RAB_SLOT_EXCLUSION: [
        QUARANTINE / "RAB_SOURCE_SLOT_EXCLUSION_ATTEMPT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_RAB_source_slot_exclusion_attempt_nonclaim_1629.csv",
    ],
    OBSTRUCTION_LEDGER: [
        QUARANTINE / "RAB_SLOT_OBSTRUCTION_LEDGER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_RAB_slot_obstruction_ledger_nonclaim_1629.csv",
    ],
    FINITE_PRIOR_WIDTHS: [
        QUARANTINE / "FINITE_JR_PIR_PRIOR_WIDTH_ROWS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_finite_JR_PiR_prior_width_rows_nonclaim_1629.csv",
        QUEUE / "JR1629_FINITE_JR_PIR_PRIOR_WIDTH_ROWS_NONCLAIM.csv",
    ],
    RUNNER_GATES: [
        QUARANTINE / "PRIOR_WIDTH_RUNNER_GATES_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_prior_width_runner_gates_nonclaim_1629.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE_CLOSED.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_closed_1629.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_1629.csv",
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
    for directory in [OUT, INPUT_1629, BRANCH_RESIDUALS, QUEUE]:
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
    for field in ["score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed", "parent_signed", "accepted_as_zero"]:
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
            "role": "1629 R_AB source-slot exclusion provenance",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for source_id, path in SOURCE_FILES.items()
    ]


def rab_slot_exclusion_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "RSE1629_0_target",
            "exclude independent R_AB/source-only slot",
            "ordinary matter/source actions cannot contain R_AB, F(R_AB), or epsilon_RAB_source unless it is an observed/measureable quotient variable",
            "TARGET_SHARPENED",
            "this is the exact theorem that would make delta S_matter/delta R_AB=0",
        ),
        (
            "RSE1629_1_typed_object_language",
            "typed parent object language",
            "allowed matter arguments are observed quotient geometry, matter fields, gauge/current data, measured representation constants, and universal constants",
            "CONDITIONAL_TYPING_LEMMA",
            "1066 gives the syntax route, but parent object language is not derived from MTS primitives",
        ),
        (
            "RSE1629_2_no_inert_source_scalar",
            "no inert source-only reciprocal scalar",
            "epsilon_RAB_source is forbidden if it changes active source strength but no nongravitational observable or representation label",
            "EXACT_IF_PARENT_SYNTAX_ACCEPTED",
            "same structure as 1065/1066 no-source-only scalar, specialized to R_AB",
        ),
        (
            "RSE1629_3_variation_before_readout",
            "variation before readout",
            "J_R is extracted from parent variation before post-readout/source selectors can be applied",
            "CLEAN_IF_PARENT_VARIATION_ORDER_SIGNED",
            "helps kill post-variation selectors, but does not kill pre-action coefficients",
        ),
        (
            "RSE1629_4_action_scale_owner",
            "universal action-scale/measure owner",
            "multipliers of S_A or source-only R_AB terms are fixed as common calibration, not species/source-local freedoms",
            "ACTION_SCALE_OWNER_NOT_PARENT_SIGNED",
            "1066 says quantum/action-scale normalization obstruction survives",
        ),
        (
            "RSE1629_5_boundary_slot",
            "no independent boundary Pi_R slot",
            "source boundary action cannot contain reciprocal momentum Pi_R unless observed/bounded",
            "BOUNDARY_SLOT_NOT_PARENT_SIGNED",
            "needed to turn Q_R=-Pi_R into Q_R=0",
        ),
        (
            "RSE1629_6_hidden_tail",
            "no hidden non-Hilbert/source-support R_AB tail",
            "support shifts, marker constants, non-Hilbert tails, and domain terms are absent or bounded",
            "HIDDEN_TAIL_NOT_CLOSED",
            "visible object-language exclusion is not enough for total local source silence",
        ),
        (
            "RSE1629_7_verdict",
            "R_AB source-slot exclusion theorem",
            "RSE1629_1 through RSE1629_6 all parent-signed",
            "RAB_SOURCE_SLOT_EXCLUSION_NOT_DERIVED_CURRENT_CORPUS",
            "finite J_R/Pi_R/Q_R prior widths remain required as fallback",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "attempt_id": attempt_id,
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
        for attempt_id, claim_piece, statement, status, effect in rows
    ]


def obstruction_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "OBS1629_0_parent_object_language",
            "the exact parent object language is not derived",
            "without it, R_AB/source-only arguments cannot be syntactically forbidden",
            "1065/1066/1087",
        ),
        (
            "OBS1629_1_action_scale",
            "action-scale or measure multipliers can change Hilbert source while leaving classical EOM shape familiar",
            "blocks treating source-only scalar as harmless normalization",
            "1066 quantum action-scale obstruction",
        ),
        (
            "OBS1629_2_pre_action_weight",
            "pre-action source weights survive current-owner proof",
            "Hilbert variation inherits coefficients inserted before variation",
            "1079/1087",
        ),
        (
            "OBS1629_3_boundary_PiR",
            "boundary reciprocal momentum Pi_R is not syntactically excluded",
            "Q_R=-Pi_R can leave reciprocal hair",
            "06/1627/1628",
        ),
        (
            "OBS1629_4_hidden_tail",
            "hidden/source/domain tails can bypass visible matter functor",
            "J_R visible zero would not be total source zero",
            "1027/1628",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "obstruction_id": obstruction_id,
            "obstruction": obstruction,
            "why_it_matters": why,
            "source_anchor": anchor,
            "status": "ACTIVE_OBSTRUCTION",
            "required_to_close": "parent-signed theorem or finite prior/source row",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for obstruction_id, obstruction, why, anchor in rows
    ]


def finite_prior_width_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PW1629_0_epsilon_RAB_source",
            "epsilon_RAB_source",
            "dimensionless source-only reciprocal scalar",
            "abs(epsilon_RAB_source) <= MISSING_PRIOR_WIDTH",
            "MISSING_RAB_SOURCE_SLOT_ZERO_OR_PRIOR_WIDTH",
            "all",
        ),
        (
            "PW1629_1_JR",
            "J_R",
            "source-current units after R_AB equation normalization",
            "abs(J_R) <= MISSING_JR_WIDTH",
            "MISSING_JR_PRIOR_WIDTH",
            "R10;PPN;clock;orbital",
        ),
        (
            "PW1629_2_PiR",
            "Pi_R",
            "boundary reciprocal momentum units",
            "abs(Pi_R) <= MISSING_PIR_WIDTH",
            "MISSING_PIR_PRIOR_WIDTH",
            "R10;PPN;orbital",
        ),
        (
            "PW1629_3_QR",
            "Q_R",
            "reciprocal charge units",
            "abs(Q_R) <= MISSING_QR_WIDTH",
            "MISSING_QR_PRIOR_WIDTH",
            "R10;PPN",
        ),
        (
            "PW1629_4_tau_R10_width",
            "tau_R10[J_R/Pi_R/Q_R]",
            "dimensionless alpha(lambda) projection",
            "abs(alpha_R(lambda)) <= alpha_bound(lambda)",
            "MISSING_R10_WIDTH_KERNEL",
            "R10",
        ),
        (
            "PW1629_5_tau_PPN_width",
            "tau_PPN[J_R/Pi_R/Q_R]",
            "PPN residual units",
            "abs(residual_vector) <= sourced PPN bounds",
            "MISSING_PPN_WIDTH_KERNEL",
            "PPN;local_GR",
        ),
        (
            "PW1629_6_tau_clock_orbital_width",
            "tau_clock/tau_orbital[J_R/Pi_R/Q_R]",
            "clock/orbital residual units",
            "abs(clock/orbital residual) <= sourced bounds",
            "MISSING_CLOCK_ORBITAL_WIDTH_KERNEL",
            "clock;orbital",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "prior_width_id": prior_id,
            "quantity": quantity,
            "units": units,
            "formula_or_requirement": formula,
            "status": status,
            "arena_projection": arena,
            "source_path": "MISSING_LOCAL_SOURCE_PATH",
            "source_anchor": "MISSING_SOURCE_ANCHOR",
            "numeric_value_present": False,
            "source_backed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for prior_id, quantity, units, formula, status, arena in rows
    ]


def runner_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("RG1629_0_no_slot_theorem", "do not set J_R/Pi_R/Q_R zero unless RSE1629_1-6 are parent-signed", "RAB_SOURCE_SLOT_EXCLUSION_MISSING"),
        ("RG1629_1_no_current_owner_shortcut", "current/source owner does not kill pre-action R_AB source scalars", "CURRENT_OWNER_TOO_NARROW"),
        ("RG1629_2_no_action_scale_shortcut", "classical normalization arguments do not fix action-scale/measure multipliers", "ACTION_SCALE_OWNER_MISSING"),
        ("RG1629_3_no_prior_scoring", "prior-width rows with MISSING markers are hard rejected", "PRIOR_WIDTH_MISSING"),
        ("RG1629_4_no_arena_scoring", "no R10/PPN/clock/orbital scoring without tau kernels and sourced bounds", "ARENA_KERNEL_MISSING"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "rule": rule,
            "failure_status": failure,
            "severity": "hard_reject",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, rule, failure in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    claims = [
        ("CG1629_0_slot_exclusion", "R_AB source-slot exclusion theorem", "BLOCKED", "parent object-language/action-scale/boundary clauses are unsigned"),
        ("CG1629_1_JR_zero", "J_R=0/Pi_R=0/Q_R=0", "BLOCKED", "source-slot exclusion not derived"),
        ("CG1629_2_prior_widths", "finite J_R/Pi_R/Q_R prior-width rows claim-ready", "BLOCKED", "rows contain MISSING widths and no source paths"),
        ("CG1629_3_arena", "R10/PPN/clock/orbital comparisons", "BLOCKED", "tau kernels missing"),
        ("CG1629_4_local_GR", "derived local GR/Newton recovery", "BLOCKED", "reciprocal source/boundary finite branch remains open"),
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
            "decision_id": "DEC1629_0_theorem",
            "decision": "RAB_SOURCE_SLOT_EXCLUSION_NOT_DERIVED_CURRENT_CORPUS",
            "reason": "the exact clause is sharp, but parent object-language, action-scale, boundary, and hidden-tail clauses remain unsigned",
            "next_action": "do not promote J_R/Pi_R/Q_R zeros",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1629_1_prior_widths",
            "decision": "FINITE_JR_PIR_PRIOR_WIDTH_ROWS_STAGED_NONCLAIM",
            "reason": "the fallback now has named widths for epsilon_RAB_source, J_R, Pi_R, Q_R, and tau projections",
            "next_action": "only score after numeric/source-backed widths and arena kernels exist",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1629_2_next",
            "decision": "NEXT_1630_ACTION_SCALE_MEASURE_OWNER_OR_JR_PRIOR_RUNNER",
            "reason": "the remaining derivation bottleneck is action-scale/measure ownership; the finite fallback needs a runner if derivation fails",
            "next_action": "try action-scale/measure owner once; otherwise build executable prior-width refusal runner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1630-Y5-R2FR-action-scale-measure-owner-or-JR-prior-width-runner.md",
            "script": "scripts/Y5_R2FR_action_scale_measure_owner_or_JR_prior_width_runner.py",
            "objective": "try to derive a universal parent action-scale/measure owner that forbids inert R_AB source-only multipliers; if it fails, build an executable prior-width refusal runner for epsilon_RAB_source, J_R, Pi_R, Q_R, and tau projections",
            "success_condition": "either action-scale/measure ownership closes the source-slot exclusion as nonclaim, or finite prior-width rows get a runner that refuses claims until numeric/source-backed inputs and arena kernels exist",
            "do_not": "do not use classical field normalization as proof, do not score missing prior widths, do not claim local GR/Newton/R10/PPN/clock/orbital pass",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def generated_paths() -> list[Path]:
    return [
        SOURCE_REGISTER,
        RAB_SLOT_EXCLUSION,
        OBSTRUCTION_LEDGER,
        FINITE_PRIOR_WIDTHS,
        RUNNER_GATES,
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
            shutil.copyfile(source, INPUT_1629 / f"{source_id}{source.suffix}")


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows() -> list[dict[str, Any]]:
    paths = generated_paths()
    slot_rows = read_csv(RAB_SLOT_EXCLUSION)
    obstruction_data = read_csv(OBSTRUCTION_LEDGER)
    prior_rows = read_csv(FINITE_PRIOR_WIDTHS)
    runner_rows = read_csv(RUNNER_GATES)
    claim_rows = read_csv(CLAIM_GATE)
    decision_text = file_text(DECISION)
    next_text = file_text(NEXT_TARGET)
    all_rows: list[dict[str, Any]] = []
    for path in paths:
        all_rows.extend(read_csv(path))

    source_ok = all(path.exists() for path in SOURCE_FILES.values())
    needles_ok = all(all_needles_found(source_id) for source_id in SOURCE_FILES)
    theorem_blocked = any(row["attempt_id"] == "RSE1629_7_verdict" and row["status"] == "RAB_SOURCE_SLOT_EXCLUSION_NOT_DERIVED_CURRENT_CORPUS" for row in slot_rows)
    exact_clause_present = any(row["attempt_id"] == "RSE1629_2_no_inert_source_scalar" and row["status"] == "EXACT_IF_PARENT_SYNTAX_ACCEPTED" for row in slot_rows)
    obstructions_active = len(obstruction_data) == 5 and all(row["status"] == "ACTIVE_OBSTRUCTION" for row in obstruction_data)
    prior_coverage = {row["quantity"] for row in prior_rows} == {
        "epsilon_RAB_source",
        "J_R",
        "Pi_R",
        "Q_R",
        "tau_R10[J_R/Pi_R/Q_R]",
        "tau_PPN[J_R/Pi_R/Q_R]",
        "tau_clock/tau_orbital[J_R/Pi_R/Q_R]",
    }
    prior_nonclaim = all(row["source_path"] == "MISSING_LOCAL_SOURCE_PATH" and not row_has_true_claim_flag(row) for row in prior_rows)
    runner_hard = all(row["severity"] == "hard_reject" for row in runner_rows)
    claim_closed = all(row["status"] == "BLOCKED" and not row_has_true_claim_flag(row) for row in claim_rows)
    nonclaim_ok = all(not row_has_true_claim_flag(row) for row in all_rows)
    decision_next = "NEXT_1630_ACTION_SCALE_MEASURE_OWNER_OR_JR_PRIOR_RUNNER" in decision_text
    next_selected = "1630-Y5-R2FR-action-scale-measure-owner-or-JR-prior-width-runner.md" in next_text
    branch_copies = all(target.exists() for targets in COPY_TARGETS.values() for target in targets)
    csv_ok = all(csv_parses(path) for path in paths)
    pycache_absent = not (Path(__file__).resolve().parent / "__pycache__").exists()
    formalization_clean = not any((FORMALIZATION / path.name).exists() for path in [DOC, *paths]) if FORMALIZATION.exists() else True

    checks = [
        ("VAL1629_0_sources_exist", source_ok, "all cited 1629 local source paths exist"),
        ("VAL1629_1_needles_found", needles_ok, "all required 1629 source needles found"),
        ("VAL1629_2_exact_clause_present", exact_clause_present, "exact R_AB no-source-slot clause is staged conditionally"),
        ("VAL1629_3_theorem_blocked", theorem_blocked, "R_AB source-slot theorem remains not derived"),
        ("VAL1629_4_obstructions_active", obstructions_active, "obstruction ledger remains active"),
        ("VAL1629_5_prior_coverage", prior_coverage, "finite prior-width rows cover epsilon_RAB_source, J_R, Pi_R, Q_R, and tau projections"),
        ("VAL1629_6_prior_nonclaim", prior_nonclaim, "prior-width rows remain MISSING-marker nonclaim rows"),
        ("VAL1629_7_runner_hard", runner_hard, "runner gates are hard rejects"),
        ("VAL1629_8_claim_gates_closed", claim_closed, "all claim gates remain blocked"),
        ("VAL1629_9_nonclaim_flags", nonclaim_ok, "all generated 1629 rows remain nonclaim/non-score-ready"),
        ("VAL1629_10_decision_next", decision_next, "decision selects action-scale/measure owner or prior runner next"),
        ("VAL1629_11_next_target_selected", next_selected, "next target selected"),
        ("VAL1629_12_branch_copies", branch_copies, "branch/quarantine/acquisition queue nonclaim copies exist"),
        ("VAL1629_13_csv_parse", csv_ok, "all generated 1629 CSVs parse"),
        ("VAL1629_14_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL1629_15_formalization_untouched", formalization_clean, "no 1629 outputs found under formalization-workbench"),
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
            "check_id": "VAL1629_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1629 R_AB source-slot exclusion or finite J_R prior-width validation",
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
    slot_rows = read_csv(RAB_SLOT_EXCLUSION)
    obstruction_data = read_csv(OBSTRUCTION_LEDGER)
    prior_rows = read_csv(FINITE_PRIOR_WIDTHS)
    runner_rows = read_csv(RUNNER_GATES)
    claim_rows = read_csv(CLAIM_GATE)
    decision_rows_data = read_csv(DECISION)
    next_target = read_csv(NEXT_TARGET)
    validation = read_csv(VALIDATION)

    content = f"""# 1629 — `R_AB` Source-Slot Exclusion Or Finite `J_R` Prior Width

## Status

Private checkpoint. No `R_AB` source-slot exclusion theorem, `J_R=0`, `Pi_R=0`, local-GR/Newton, R10, PPN, clock, orbital, or finite-prior claim is made.

## Outcome

The exact theorem target is now sharp: if the parent object language forbids independent `R_AB` source-only slots, pre-action reciprocal scalars, and boundary `Pi_R` slots, then the `J_R=0` route can close. Current corpus does not derive that parent syntax/action-scale owner. Finite `J_R/Pi_R/Q_R` prior-width rows are staged as nonclaim fallback.

## Source Register

{markdown_table(source_rows, ["source_id", "source_path", "exists", "needles_found"])}

## `R_AB` Source-Slot Exclusion Attempt

{markdown_table(slot_rows, ["attempt_id", "claim_piece", "status", "effect"])}

## Obstruction Ledger

{markdown_table(obstruction_data, ["obstruction_id", "obstruction", "status", "required_to_close"])}

## Finite Prior-Width Rows

{markdown_table(prior_rows, ["prior_width_id", "quantity", "status", "units", "arena_projection"])}

## Runner Gates

{markdown_table(runner_rows, ["gate_id", "failure_status", "severity", "rule"])}

## Claim Gates

{markdown_table(claim_rows, ["gate_id", "claim", "status", "reason"])}

## Decision

{markdown_table(decision_rows_data, ["decision_id", "decision", "reason", "next_action"])}

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
        RAB_SLOT_EXCLUSION: rab_slot_exclusion_rows(),
        OBSTRUCTION_LEDGER: obstruction_rows(),
        FINITE_PRIOR_WIDTHS: finite_prior_width_rows(),
        RUNNER_GATES: runner_gate_rows(),
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
