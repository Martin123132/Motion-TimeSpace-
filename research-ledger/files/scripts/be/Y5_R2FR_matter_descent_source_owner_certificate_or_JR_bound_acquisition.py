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
QUARANTINE = MICROSCOPE / "quarantine" / "1628"
INPUT_1628 = QUARANTINE / "input"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1628-Y5-R2FR-matter-descent-source-owner-certificate-or-JR-bound-acquisition.md"

SOURCE_FILES = {
    "1627_doc": ROOT / "1627-Y5-R2FR-JR-zero-source-theorem-or-first-finite-JR-row.md",
    "1627_validation": OUT / "P8_Y5_BRR545_1627_VALIDATION.csv",
    "1627_next": OUT / "P8_Y5_PARENT_QLOC_1627_NEXT_TARGET.csv",
    "1627_matter_audit": OUT / "P8_Y5_PARENT_QLOC_1627_MATTER_DESCENT_PREMISE_AUDIT.csv",
    "1627_finite_jr": OUT / "P8_Y5_PARENT_QLOC_1627_FIRST_FINITE_JR_ROW_CONTRACT_NONCLAIM.csv",
    "06_source_neutrality": ROOT / "06-reciprocal-charge-source-neutrality.md",
    "1027_qbar_source_zero": ROOT / "1027-Y5-R10-qbarXT-source-zero-or-bounded-coupling-row.md",
    "1030_single_public_metric": ROOT / "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md",
    "1065_no_source_slot": ROOT / "1065-Y5-R10-no-source-only-slot-parent-grammar-or-first-relative-weight-numeric-row.md",
    "1079_current_owner": ROOT / "1079-Y5-R10-parent-current-owner-narrow-proof-or-finite-WEP-source-vector.md",
    "1087_matter_descent": ROOT / "1087-Y5-R10-parent-matter-descent-zero-current-or-DD-coefficient-source-pack.md",
}

NEEDLES = {
    "1627_doc": ["NEXT_1628_MATTER_DESCENT_SOURCE_OWNER_OR_JR_BOUND_ACQUISITION", "VAL1627_OVERALL"],
    "1627_validation": ["VAL1627_OVERALL", "PASS"],
    "1627_next": ["1628-Y5-R2FR-matter-descent-source-owner-certificate-or-JR-bound-acquisition.md", "J_R=0 and Pi_R=0"],
    "1627_matter_audit": ["MD1627_7_verdict", "MATTER_DESCENT_PREMISES_UNSIGNED"],
    "1627_finite_jr": ["FJR1627_0_first_finite_JR_contract", "FINITE_JR_ROW_CONTRACT_STAGED_NONCLAIM"],
    "06_source_neutrality": ["Q_R = -Pi_R", "Pi_R = 0 -> Q_R = 0 -> R_AB = 0 -> AB = 1"],
    "1027_qbar_source_zero": ["QZ1027_3_matter_functor", "EXACT_CONTRACT_NOT_PARENT_SIGNED"],
    "1030_single_public_metric": ["SPM1030_3_total_Hilbert_source", "CONDITIONAL_FROM_954_955_956"],
    "1065_no_source_slot": ["PGG1065_5_verdict", "CONDITIONAL_GRAMMAR_NOT_PARENT_SIGNED"],
    "1079_current_owner": ["NCO1079_1_hilbert_variation", "SURVIVES_PRE_VARIATION"],
    "1087_matter_descent": ["PMD1087_6_verdict", "PARENT_MATTER_DESCENT_ZERO_NOT_SIGNED"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1628_SOURCE_REGISTER.csv"
SOURCE_OWNER_CERTIFICATE = OUT / "P8_Y5_PARENT_QLOC_1628_SOURCE_OWNER_CERTIFICATE_ATTEMPT.csv"
COUNTEREXAMPLE_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1628_SOURCE_OWNER_COUNTEREXAMPLE_LEDGER.csv"
JR_ACQUISITION_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1628_JR_BOUND_ACQUISITION_LEDGER.csv"
RUNNER_GATES = OUT / "P8_Y5_PARENT_QLOC_1628_RUNNER_GATES.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1628_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1628_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1628_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1628_VALIDATION.csv"

COPY_TARGETS = {
    SOURCE_OWNER_CERTIFICATE: [
        QUARANTINE / "SOURCE_OWNER_CERTIFICATE_ATTEMPT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_source_owner_certificate_attempt_nonclaim_1628.csv",
    ],
    COUNTEREXAMPLE_LEDGER: [
        QUARANTINE / "SOURCE_OWNER_COUNTEREXAMPLE_LEDGER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_source_owner_counterexample_ledger_nonclaim_1628.csv",
    ],
    JR_ACQUISITION_LEDGER: [
        QUARANTINE / "JR_BOUND_ACQUISITION_LEDGER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_JR_bound_acquisition_ledger_nonclaim_1628.csv",
        QUEUE / "JR1628_BOUND_ACQUISITION_LEDGER_NONCLAIM.csv",
    ],
    RUNNER_GATES: [
        QUARANTINE / "RUNNER_GATES_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_runner_gates_nonclaim_1628.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE_CLOSED.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_closed_1628.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_1628.csv",
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
    for directory in [OUT, INPUT_1628, BRANCH_RESIDUALS, QUEUE]:
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
    for field in ["score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed", "accepted_for_scoring", "parent_signed"]:
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
            "role": "1628 matter descent/source-owner certificate provenance",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for source_id, path in SOURCE_FILES.items()
    ]


def source_owner_certificate_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "SOC1628_0_common_action",
            "one common ordinary-matter action exists before readout",
            "S_matter is fixed before extracting Hilbert source/current",
            "1079_current_owner;1030_single_public_metric",
            "CONDITIONAL_NOT_PARENT_SIGNED",
            "needed before Hilbert source owner can be used against J_R",
        ),
        (
            "SOC1628_1_hilbert_owner",
            "Hilbert variation owns the source once common action is fixed",
            "T_total := delta S_matter/delta e_obs",
            "1079_current_owner;1030_single_public_metric",
            "EXACT_SUBTHEOREM_CONDITIONAL",
            "kills post-variation source rescaling, but only after common action/readout order premises",
        ),
        (
            "SOC1628_2_no_RAB_argument",
            "ordinary matter functor has no independent R_AB representative argument",
            "S_matter = Sbar[Psi,e_obs(q),omega(e_obs),theta] and not S_matter[R_AB,...]",
            "1027_qbar_source_zero;1087_matter_descent",
            "EXACT_CONTRACT_NOT_PARENT_SIGNED",
            "would make delta S_matter/delta R_AB vanish by chain rule",
        ),
        (
            "SOC1628_3_no_pre_action_weights",
            "no source-only/pre-action weights or reciprocal source scalars are legal",
            "exclude w_A S_A and any inert R_AB-source prefactor before variation",
            "1065_no_source_slot;1079_current_owner;1087_matter_descent",
            "PRE_ACTION_WEIGHT_LEAK_SURVIVES",
            "source owner alone does not kill coefficients already inserted into S_matter",
        ),
        (
            "SOC1628_4_no_hidden_tails",
            "hidden/source/domain/boundary tails are zero or separately bounded",
            "DeltaJ_hidden, support shifts, marker constants, and boundary charges vanish or have rows",
            "1027_qbar_source_zero;1087_matter_descent",
            "HIDDEN_SOURCE_TAILS_NOT_CLOSED",
            "even a visible matter descent proof would not silence non-Hilbert/source-support tails",
        ),
        (
            "SOC1628_5_PiR_boundary",
            "source boundary reciprocal momentum vanishes",
            "Pi_R=0 so Q_R=-Pi_R kills reciprocal hair",
            "06_source_neutrality;1627_matter_audit",
            "PIR_ZERO_NOT_PARENT_SIGNED",
            "boundary/source owner is the missing piece for Q_R=0",
        ),
        (
            "SOC1628_6_verdict",
            "J_R=0 and Pi_R=0 follow from source-owner certificate",
            "SOC1628_0 through SOC1628_5 all close from one parent action",
            "all 1628 sources",
            "SOURCE_OWNER_CERTIFICATE_NOT_CLOSED_CURRENT_CORPUS",
            "route remains exact target; fallback is finite J_R/Pi_R acquisition",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "certificate_id": certificate_id,
            "claim_piece": claim_piece,
            "formal_statement": statement,
            "source_anchors": anchors,
            "status": status,
            "effect": effect,
            "parent_signed": False,
            "accepted_as_zero": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for certificate_id, claim_piece, statement, anchors, status, effect in rows
    ]


def counterexample_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CE1628_0_pre_action_weight",
            "S_matter=sum_A w_A S_A or reciprocal source-only prefactor inserted before variation",
            "Hilbert source inherits w_A/J_R-like coefficient even with a unique source owner",
            "1065/1079/1087 say this survives until parent object-language excludes it",
        ),
        (
            "CE1628_1_direct_RAB_slot",
            "S_matter contains F(R_AB) or R_AB-sensitive source support term",
            "delta S_matter/delta R_AB produces finite J_R",
            "1027/1030 contracts forbid this only conditionally",
        ),
        (
            "CE1628_2_boundary_momentum",
            "source boundary has Pi_R != 0",
            "Q_R=-Pi_R leaves reciprocal hair even if exterior J_R=0",
            "06 source-neutrality makes this explicit",
        ),
        (
            "CE1628_3_hidden_nonHilbert_tail",
            "non-Hilbert/source-support/domain or marker tail contributes outside visible matter functor",
            "visible matter descent can pass while total source coupling remains finite",
            "1027/1087 retain hidden tail blocker",
        ),
        (
            "CE1628_4_frame_marker_return",
            "common frame, marker constants, or measured matter parameters carry vertical dependence",
            "chain-rule zero for geometry alone does not silence clocks/source readout",
            "1027/1030/1065 retain no-marker and frame-owner debts",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "counterexample_id": counterexample_id,
            "counterexample": counterexample,
            "why_it_blocks_JR_zero": why_blocks,
            "source_anchor": source_anchor,
            "current_status": "LEGAL_UNTIL_PARENT_OBJECT_LANGUAGE_EXCLUDES_OR_BOUNDS",
            "requires": "parent object-language/source-slot exclusion theorem or finite source/boundary row",
            "parent_signed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for counterexample_id, counterexample, why_blocks, source_anchor in rows
    ]


def jr_acquisition_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "JRA1628_0_zero_certificate",
            "J_R=0 certificate",
            "parent-signed source-owner/no-R_AB-slot theorem",
            "MISSING_SOURCE_OWNER_CERTIFICATE",
            "theorem_or_zero_certificate",
            "all",
        ),
        (
            "JRA1628_1_finite_JR_bound",
            "finite J_R source-current coefficient",
            "numeric value or prior interval with units and R_AB equation normalization",
            "MISSING_NUMERIC_JR_SOURCE_BOUND",
            "source-current units",
            "R10;PPN;clock;orbital",
        ),
        (
            "JRA1628_2_PiR_boundary",
            "Pi_R boundary momentum/charge",
            "zero theorem or finite boundary-flux bound with surface convention",
            "MISSING_PIR_ZERO_OR_BOUND",
            "boundary momentum/flux units",
            "R10;PPN;orbital",
        ),
        (
            "JRA1628_3_QR_charge",
            "Q_R reciprocal charge",
            "Q_R integral/source-matching value or bound",
            "MISSING_QR_CHARGE_BOUND",
            "reciprocal charge units",
            "PPN;R10",
        ),
        (
            "JRA1628_4_tau_R10_JR",
            "tau_R10[J_R]",
            "kernel mapping J_R/Q_R profile to alpha(lambda)",
            "MISSING_R10_JR_KERNEL",
            "dimensionless alpha mapping",
            "R10",
        ),
        (
            "JRA1628_5_tau_PPN_JR",
            "tau_PPN[J_R]",
            "weak-field map from reciprocal hair to gamma/beta/preferred-frame residual vector",
            "MISSING_PPN_JR_KERNEL",
            "PPN residual units",
            "PPN;local_GR",
        ),
        (
            "JRA1628_6_tau_clock_JR",
            "tau_clock[J_R]",
            "clock/readout sensitivity to reciprocal source coupling",
            "MISSING_CLOCK_JR_KERNEL",
            "clock residual units",
            "clock",
        ),
        (
            "JRA1628_7_tau_orbital_JR",
            "tau_orbital[J_R]",
            "orbital/source-support response to reciprocal source current",
            "MISSING_ORBITAL_JR_KERNEL",
            "orbital residual units",
            "orbital",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "acquisition_id": acquisition_id,
            "target": target,
            "required_evidence": evidence,
            "current_status": status,
            "required_units": units,
            "arena_projection": arena,
            "source_path": "MISSING_LOCAL_SOURCE_PATH",
            "source_anchor": "MISSING_SOURCE_ANCHOR",
            "accepted_as_live_row": False,
            "numeric_value_present": False,
            "source_backed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for acquisition_id, target, evidence, status, units, arena in rows
    ]


def runner_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("RG1628_0_no_certificate", "do not set J_R=0 unless SOC1628_0-5 are parent-signed together", "SOURCE_OWNER_CERTIFICATE_MISSING"),
        ("RG1628_1_no_source_owner_shortcut", "Hilbert current owner alone cannot forbid pre-action source-only weights", "CURRENT_OWNER_TOO_NARROW"),
        ("RG1628_2_no_boundary_silence_shortcut", "do not set Pi_R=0 from exterior vacuum or asymptotic flatness", "PIR_BOUNDARY_CERTIFICATE_MISSING"),
        ("RG1628_3_no_template_scoring", "finite J_R/Pi_R/Q_R rows with MISSING markers are hard rejected", "PLACEHOLDER_MARKER_PRESENT"),
        ("RG1628_4_no_arena_without_kernel", "J_R rows do not score until tau_R10/tau_PPN/tau_clock/tau_orbital kernels exist", "ARENA_KERNEL_MISSING"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "rule": rule,
            "failure_status": failure,
            "severity": "hard_reject",
            "runner_action": "block claim and route to acquisition ledger",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, rule, failure in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    claims = [
        ("CG1628_0_source_owner", "source-owner certificate derives J_R=0", "BLOCKED", "certificate clauses do not close together"),
        ("CG1628_1_PiR", "Pi_R=0 boundary/source neutrality", "BLOCKED", "boundary/source reciprocal momentum zero is not parent-signed"),
        ("CG1628_2_finite_JR", "finite J_R bound row claim-ready", "BLOCKED", "acquisition ledger has no numeric/source-backed row"),
        ("CG1628_3_arena", "J_R arena projections", "BLOCKED", "tau kernels missing"),
        ("CG1628_4_local_GR", "derived local GR/Newton recovery", "BLOCKED", "source coupling and reciprocal boundary charge remain open"),
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
            "decision_id": "DEC1628_0_partial_win",
            "decision": "HILBERT_SOURCE_OWNER_IS_CONDITIONAL_SUBTHEOREM_ONLY",
            "reason": "inside a common action, source ownership is sharp, but it does not forbid pre-action/source-only slots",
            "next_action": "retain it as a premise, not a J_R zero proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1628_1_certificate",
            "decision": "SOURCE_OWNER_CERTIFICATE_NOT_CLOSED_CURRENT_CORPUS",
            "reason": "no-R_AB-slot, no pre-action weight, hidden-tail silence, and Pi_R=0 are not parent-signed",
            "next_action": "move from source-owner alone to explicit R_AB source-slot exclusion",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1628_2_acquisition",
            "decision": "JR_BOUND_ACQUISITION_LEDGER_STAGED_NONCLAIM",
            "reason": "finite J_R/Pi_R/Q_R and arena-kernel rows are now named, but unfilled",
            "next_action": "use the ledger only after source evidence appears",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1628_3_next",
            "decision": "NEXT_1629_RAB_SOURCE_SLOT_EXCLUSION_OR_FINITE_JR_PRIOR_WIDTH",
            "reason": "the least-scrutiny theorem target is now the parent grammar clause forbidding independent R_AB/source-only slots",
            "next_action": "try exact source-slot exclusion; otherwise define finite J_R/Pi_R prior widths",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1629-Y5-R2FR-RAB-source-slot-exclusion-or-finite-JR-prior-width.md",
            "script": "scripts/Y5_R2FR_RAB_source_slot_exclusion_or_finite_JR_prior_width.py",
            "objective": "try to derive the parent object-language rule that ordinary matter/source actions cannot contain an independent R_AB/source-only slot or pre-action reciprocal source scalar; if it fails, define finite J_R/Pi_R prior-width rows with units and arena-projection blockers",
            "success_condition": "either R_AB source-slot exclusion becomes a parent-signed nonclaim theorem candidate with counterexamples closed, or finite J_R/Pi_R prior-width acquisition rows are staged without scoring",
            "do_not": "do not claim source-owner alone proves J_R=0, do not assume Pi_R=0, do not score prior widths, do not claim local GR/Newton/R10/PPN/clock/orbital pass",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def generated_paths() -> list[Path]:
    return [
        SOURCE_REGISTER,
        SOURCE_OWNER_CERTIFICATE,
        COUNTEREXAMPLE_LEDGER,
        JR_ACQUISITION_LEDGER,
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
            shutil.copyfile(source, INPUT_1628 / f"{source_id}{source.suffix}")


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows() -> list[dict[str, Any]]:
    paths = generated_paths()
    cert_rows = read_csv(SOURCE_OWNER_CERTIFICATE)
    counter_rows = read_csv(COUNTEREXAMPLE_LEDGER)
    acq_rows = read_csv(JR_ACQUISITION_LEDGER)
    runner_rows = read_csv(RUNNER_GATES)
    claim_rows = read_csv(CLAIM_GATE)
    decision_text = file_text(DECISION)
    next_text = file_text(NEXT_TARGET)
    all_rows: list[dict[str, Any]] = []
    for path in paths:
        all_rows.extend(read_csv(path))

    source_ok = all(path.exists() for path in SOURCE_FILES.values())
    needles_ok = all(all_needles_found(source_id) for source_id in SOURCE_FILES)
    certificate_blocked = any(row["certificate_id"] == "SOC1628_6_verdict" and row["status"] == "SOURCE_OWNER_CERTIFICATE_NOT_CLOSED_CURRENT_CORPUS" for row in cert_rows)
    hilbert_partial = any(row["certificate_id"] == "SOC1628_1_hilbert_owner" and row["status"] == "EXACT_SUBTHEOREM_CONDITIONAL" for row in cert_rows)
    counterexamples_active = len(counter_rows) == 5 and all(row["current_status"] == "LEGAL_UNTIL_PARENT_OBJECT_LANGUAGE_EXCLUDES_OR_BOUNDS" for row in counter_rows)
    acq_coverage = {row["target"] for row in acq_rows} == {
        "J_R=0 certificate",
        "finite J_R source-current coefficient",
        "Pi_R boundary momentum/charge",
        "Q_R reciprocal charge",
        "tau_R10[J_R]",
        "tau_PPN[J_R]",
        "tau_clock[J_R]",
        "tau_orbital[J_R]",
    }
    acq_nonclaim = all(row["source_path"] == "MISSING_LOCAL_SOURCE_PATH" and not row_has_true_claim_flag(row) for row in acq_rows)
    runner_hard = all(row["severity"] == "hard_reject" for row in runner_rows)
    claim_closed = all(row["status"] == "BLOCKED" and not row_has_true_claim_flag(row) for row in claim_rows)
    nonclaim_ok = all(not row_has_true_claim_flag(row) for row in all_rows)
    decision_next = "NEXT_1629_RAB_SOURCE_SLOT_EXCLUSION_OR_FINITE_JR_PRIOR_WIDTH" in decision_text
    next_selected = "1629-Y5-R2FR-RAB-source-slot-exclusion-or-finite-JR-prior-width.md" in next_text
    branch_copies = all(target.exists() for targets in COPY_TARGETS.values() for target in targets)
    csv_ok = all(csv_parses(path) for path in paths)
    pycache_absent = not (Path(__file__).resolve().parent / "__pycache__").exists()
    formalization_clean = not any((FORMALIZATION / path.name).exists() for path in [DOC, *paths]) if FORMALIZATION.exists() else True

    checks = [
        ("VAL1628_0_sources_exist", source_ok, "all cited 1628 local source paths exist"),
        ("VAL1628_1_needles_found", needles_ok, "all required 1628 source needles found"),
        ("VAL1628_2_hilbert_partial", hilbert_partial, "Hilbert source owner retained as conditional subtheorem"),
        ("VAL1628_3_certificate_blocked", certificate_blocked, "source-owner certificate does not close current corpus"),
        ("VAL1628_4_counterexamples_active", counterexamples_active, "counterexample ledger remains active"),
        ("VAL1628_5_acquisition_coverage", acq_coverage, "J_R/Pi_R/Q_R and arena acquisition rows present"),
        ("VAL1628_6_acquisition_nonclaim", acq_nonclaim, "acquisition rows remain MISSING-marker nonclaim rows"),
        ("VAL1628_7_runner_hard", runner_hard, "runner gates are hard rejects"),
        ("VAL1628_8_claim_gates_closed", claim_closed, "all claim gates remain blocked"),
        ("VAL1628_9_nonclaim_flags", nonclaim_ok, "all generated 1628 rows remain nonclaim/non-score-ready"),
        ("VAL1628_10_decision_next", decision_next, "decision selects R_AB source-slot exclusion next"),
        ("VAL1628_11_next_target_selected", next_selected, "next target selected"),
        ("VAL1628_12_branch_copies", branch_copies, "branch/quarantine/acquisition queue nonclaim copies exist"),
        ("VAL1628_13_csv_parse", csv_ok, "all generated 1628 CSVs parse"),
        ("VAL1628_14_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL1628_15_formalization_untouched", formalization_clean, "no 1628 outputs found under formalization-workbench"),
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
            "check_id": "VAL1628_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1628 matter descent source-owner certificate or J_R bound acquisition validation",
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
    cert_rows = read_csv(SOURCE_OWNER_CERTIFICATE)
    counter_rows = read_csv(COUNTEREXAMPLE_LEDGER)
    acq_rows = read_csv(JR_ACQUISITION_LEDGER)
    runner_rows = read_csv(RUNNER_GATES)
    claim_rows = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_target = read_csv(NEXT_TARGET)
    validation = read_csv(VALIDATION)

    content = f"""# 1628 — Matter Descent Source Owner Certificate Or `J_R` Bound Acquisition

## Status

Private checkpoint. No `J_R=0`, `Pi_R=0`, local-GR/Newton, R10, PPN, clock, orbital, or finite-bound claim is made.

## Outcome

The source-owner route gives a narrow conditional win: once a common matter action and variation-before-readout are already fixed, Hilbert variation owns the source and kills post-variation source rescalings. It does **not** close `J_R=0`, because pre-action source-only slots, direct `R_AB` matter arguments, boundary `Pi_R`, and hidden source tails remain legal until the parent object language excludes or bounds them.

## Source Register

{markdown_table(source_rows, ["source_id", "source_path", "exists", "needles_found"])}

## Source Owner Certificate Attempt

{markdown_table(cert_rows, ["certificate_id", "claim_piece", "status", "effect"])}

## Counterexample Ledger

{markdown_table(counter_rows, ["counterexample_id", "counterexample", "current_status", "requires"])}

## `J_R` Bound Acquisition Ledger

{markdown_table(acq_rows, ["acquisition_id", "target", "current_status", "required_units", "arena_projection"])}

## Runner Gates

{markdown_table(runner_rows, ["gate_id", "failure_status", "severity", "rule"])}

## Claim Gates

{markdown_table(claim_rows, ["gate_id", "claim", "status", "reason"])}

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
        SOURCE_OWNER_CERTIFICATE: source_owner_certificate_rows(),
        COUNTEREXAMPLE_LEDGER: counterexample_rows(),
        JR_ACQUISITION_LEDGER: jr_acquisition_rows(),
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
