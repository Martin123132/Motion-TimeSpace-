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
QUARANTINE = MICROSCOPE / "quarantine" / "1640"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1640-Y5-R2FR-PiR-zero-boundary-silence-or-normalized-PPN-bound-runner.md"

SOURCE_FILES = {
    "1639_doc": ROOT / "1639-Y5-R2FR-qR-normalization-denominator-or-PiR-source-acquisition.md",
    "1639_validation": OUT / "P8_Y5_BRR545_1639_VALIDATION.csv",
    "1639_next": OUT / "P8_Y5_PARENT_QLOC_1639_NEXT_TARGET.csv",
    "1639_law": OUT / "P8_Y5_PARENT_QLOC_1639_NR_LAW_CONDITIONAL.csv",
    "1639_templates": OUT / "P8_Y5_PARENT_QLOC_1639_PIR_QR_QRLOCAL_BOUND_TEMPLATE.csv",
    "05_reciprocity": ROOT / "05-reciprocity-theorem-attempt.md",
    "06_source_neutrality": ROOT / "06-reciprocal-charge-source-neutrality.md",
    "1635_doc": ROOT / "1635-Y5-R2FR-parent-matter-descent-signature-for-PiR-zero.md",
    "1636_doc": ROOT / "1636-Y5-R2FR-RAB-parent-object-language-or-PiR-residual-bound-pack.md",
    "1637_doc": ROOT / "1637-Y5-R2FR-no-independent-RAB-slot-grammar-or-first-PiR-bound-row.md",
    "1635_residual": OUT / "P8_Y5_PARENT_QLOC_1635_PIR_RESIDUAL_ENVELOPE.csv",
    "1636_bound_pack": OUT / "P8_Y5_PARENT_QLOC_1636_PIR_BOUND_INPUT_PACK.csv",
    "1637_obstructions": OUT / "P8_Y5_PARENT_QLOC_1637_NO_SLOT_OBSTRUCTION_LEDGER.csv",
    "1639_blockers": OUT / "P8_Y5_PARENT_QLOC_1639_SOURCE_MASS_AND_TAIL_BLOCKERS.csv",
}

NEEDLES = {
    "1639_doc": ["q_R = Q_R c^2/(2GM_*) = -Pi_R c^2/(2GM_*)", "EXACT_GR_ROUTE_REDUCES_TO_Pi_R_ZERO"],
    "1639_validation": ["VAL1639_OVERALL", "PASS"],
    "1639_next": ["1640-Y5-R2FR-PiR-zero-boundary-silence-or-normalized-PPN-bound-runner.md", "do not use orbital GM"],
    "1639_law": ["N_R = c^2/(2 G M_*)", "no orbital-GM backfill"],
    "1639_templates": ["Pi_R=0 -> Q_R=0 -> q_R=0 -> Delta gamma=0", "MISSING_PARENT_Pi_R_ZERO_THEOREM"],
    "05_reciprocity": ["W R_AB' = 0", "derive or reject Q_R=0"],
    "06_source_neutrality": ["delta S_boundary", "Pi_R = 0 -> Q_R = 0", "free source-boundary variation"],
    "1635_doc": ["PIR_ZERO_THEOREM_SHAPE_VALID", "PIR_ZERO_NOT_PARENT_SIGNED"],
    "1636_doc": ["BOUNDARY_OBJECT_LANGUAGE_MISSING", "OBJECT_LANGUAGE_NOT_DERIVED_CURRENT_CORPUS"],
    "1637_doc": ["BOUNDARY_SLOT_NOT_PARENT_SIGNED", "NO_INDEPENDENT_RAB_SLOT_NOT_DERIVED_CURRENT_CORPUS"],
    "1635_residual": ["PIRRES1635_4_boundary", "MISSING_BOUNDARY_ZERO_OR_ABSOLUTE_TAIL"],
    "1636_bound_pack": ["PIRBP1636_4_boundary", "MISSING_BOUNDARY_ZERO_OR_ABSOLUTE_TAIL"],
    "1637_obstructions": ["OBS1637_3_boundary_PiR", "ACTIVE_OBSTRUCTION"],
    "1639_blockers": ["Pi_R_BOUNDARY_TO_Q_R_PROJECTION", "SAME_FRAME_PARENT_SOURCE_MASS_M_STAR"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1640_SOURCE_REGISTER.csv"
THEOREM_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1640_PIR_ZERO_BOUNDARY_SILENCE_THEOREM_AUDIT.csv"
CLAUSE_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1640_BOUNDARY_SILENCE_CLAUSE_LEDGER.csv"
PPN_INPUTS = OUT / "P8_Y5_PARENT_QLOC_1640_NORMALIZED_PPN_BOUND_INPUTS.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1640_NORMALIZED_PPN_BOUND_RUNNER.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1640_DECISION.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1640_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1640_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1640_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    THEOREM_AUDIT,
    CLAUSE_LEDGER,
    PPN_INPUTS,
    RUNNER,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    THEOREM_AUDIT,
    CLAUSE_LEDGER,
    PPN_INPUTS,
    RUNNER,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]


def ensure_dirs() -> None:
    for directory_path in [OUT, QUARANTINE, BRANCH_RESIDUALS, QUEUE]:
        directory_path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


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


def source_paths_exist(value: str) -> bool:
    if value.startswith("MISSING_") or value == "":
        return False
    paths = [Path(part.strip()) for part in value.split(";") if part.strip() and not part.strip().startswith("MISSING_")]
    return bool(paths) and all(path.exists() for path in paths)


def source_register_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
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
                "role": "1640 Pi_R zero boundary-silence theorem or normalized PPN bound runner",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def theorem_audit_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "PZB1640_0_boundary_variation_relation",
            "claim_piece": "delta S_boundary = [W R_AB' + Pi_R] delta R_AB at source boundary",
            "status": "CORPUS_RELATION_FOUND",
            "would_imply": "stationarity links exterior reciprocal charge to boundary reciprocal momentum",
            "missing_piece": "none for symbolic relation; normalization/projection still guarded",
            "source_paths": str(SOURCE_FILES["06_source_neutrality"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "PZB1640_1_free_boundary_variation",
            "claim_piece": "free/proper boundary variation gives W R_AB'=0",
            "status": "CONDITIONAL_ROUTE_FOUND",
            "would_imply": "Q_R=0 when the exterior charge is W R_AB'",
            "missing_piece": "boundary variation class is not parent-signed for physical sources",
            "source_paths": ";".join([str(SOURCE_FILES["05_reciprocity"]), str(SOURCE_FILES["06_source_neutrality"])]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "PZB1640_2_zero_chain",
            "claim_piece": "Pi_R=0 -> Q_R=0 -> q_R=0 -> Delta gamma=0",
            "status": "EXACT_LOCAL_GR_CHAIN_IDENTIFIED",
            "would_imply": "reciprocal-hair contribution to PPN gamma vanishes exactly",
            "missing_piece": "Pi_R=0 theorem is not parent-signed",
            "source_paths": ";".join([str(SOURCE_FILES["06_source_neutrality"]), str(SOURCE_FILES["1639_templates"])]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "PZB1640_3_boundary_object_language",
            "claim_piece": "boundary/worldtube/readout terms contain no independent R_AB or Pi_R slot",
            "status": "BOUNDARY_OBJECT_LANGUAGE_UNSIGNED",
            "would_imply": "no boundary reciprocal momentum can source Q_R/r hair",
            "missing_piece": "boundary object-language derived from parent MTS primitives",
            "source_paths": ";".join([str(SOURCE_FILES["1636_doc"]), str(SOURCE_FILES["1637_doc"])]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "PZB1640_4_hidden_tail",
            "claim_piece": "hidden domain/readout/EFT boundary tails have zero local projection",
            "status": "HIDDEN_TAIL_UNSIGNED",
            "would_imply": "bulk and visible-boundary silence survive readout/local projection",
            "missing_piece": "hidden-tail theorem or absolute residual bound",
            "source_paths": ";".join([str(SOURCE_FILES["1635_doc"]), str(SOURCE_FILES["1637_doc"])]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "PZB1640_5_verdict",
            "claim_piece": "Pi_R zero boundary-silence theorem",
            "status": "PIR_ZERO_NOT_PROVED_BOUNDARY_SILENCE_UNSIGNED",
            "would_imply": "would close Q_R=0 and the reciprocal-hair local-GR branch",
            "missing_piece": "boundary object-language, worldtube projection, hidden-tail silence, and parent variation class",
            "source_paths": ";".join([str(SOURCE_FILES["1635_doc"]), str(SOURCE_FILES["1636_doc"]), str(SOURCE_FILES["1637_doc"])]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def clause_ledger_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "clause_id": "BSC1640_0_variational_relation",
            "required_clause": "source boundary variation has the corpus form W R_AB' + Pi_R",
            "status": "SIGNED_AS_SYMBOLIC_RELATION",
            "failure_mode_if_missing": "cannot link Pi_R to exterior Q_R",
            "close_requirement": "already staged; still needs parent normalization for claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "BSC1640_1_free_or_proper_boundary_class",
            "required_clause": "physical source boundary variation is free/proper/exact rather than fixed R_AB",
            "status": "UNSIGNED",
            "failure_mode_if_missing": "fixed source boundary can retain nonzero Pi_R/Q_R hair",
            "close_requirement": "parent boundary class theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "BSC1640_2_no_boundary_slot",
            "required_clause": "B_matter/worldtube/readout has no independent R_AB or Pi_R argument",
            "status": "UNSIGNED",
            "failure_mode_if_missing": "boundary reciprocal momentum remains a legal local source",
            "close_requirement": "boundary object-language derived from MTS primitives",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "BSC1640_3_zero_projection",
            "required_clause": "i_vR Theta_matter + delta_vR B_matter has zero local projection",
            "status": "UNSIGNED_OR_UNBOUNDED",
            "failure_mode_if_missing": "Pi_R_boundary_abs remains live",
            "close_requirement": "zero-projection certificate or source-backed absolute Pi_R row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "BSC1640_4_no_hidden_tail",
            "required_clause": "no hidden source-support/domain/readout/EFT R_AB tail survives",
            "status": "UNSIGNED",
            "failure_mode_if_missing": "visible no-slot proof can be bypassed after local projection",
            "close_requirement": "hidden-tail theorem or retained absolute residual vector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "BSC1640_5_all_clauses",
            "required_clause": "all boundary-silence clauses close together",
            "status": "FAIL_CURRENT_PROOF",
            "failure_mode_if_missing": "Pi_R=0 cannot be claimed",
            "close_requirement": "derive every unsigned clause or keep normalized bound runner nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def ppn_input_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "input_id": "NPPN1640_0_PiR_abs",
            "quantity": "Pi_R_boundary_abs",
            "required_for_formula": "|q_R| = k_W |Pi_R| c^2/(2 G M_*)",
            "current_value": "MISSING_BOUND_VALUE",
            "units": "length-equivalent reciprocal tail units after boundary projection",
            "source_path": "MISSING_PARENT_OR_EMPIRICAL_SOURCE_PATH",
            "status": "MISSING_SOURCE_BOUND",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "NPPN1640_1_kW",
            "quantity": "k_W_tail",
            "required_for_formula": "R_AB = k_W Q_R/r",
            "current_value": "CONDITIONAL_k_W_EQUALS_1_FROM_CORPUS_R_AB~Q_R/r",
            "units": "dimensionless",
            "source_path": str(SOURCE_FILES["05_reciprocity"]),
            "status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "NPPN1640_2_Mstar",
            "quantity": "M_star_same_frame",
            "required_for_formula": "N_R = c^2/(2 G M_*)",
            "current_value": "MISSING_SAME_FRAME_PARENT_SOURCE_MASS",
            "units": "mass",
            "source_path": "MISSING_PARENT_SOURCE_MASS_PATH",
            "status": "MISSING_SOURCE_MASS_CALIBRATION",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "NPPN1640_3_gamma_bound",
            "quantity": "Delta_gamma_abs_max",
            "required_for_formula": "|Pi_R| <= (2 G M_*/(k_W c^2)) |Delta gamma|_max",
            "current_value": "MISSING_CURRENT_EXTERNAL_PPN_GAMMA_BOUND",
            "units": "dimensionless",
            "source_path": "MISSING_EXTERNAL_PPN_SOURCE_PATH",
            "status": "MISSING_BOUND_SOURCE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "NPPN1640_4_no_cancellation",
            "quantity": "absolute_local_residual_vector",
            "required_for_formula": "Pi_R contribution must pass without cancellation credit",
            "current_value": "MISSING_ABSOLUTE_VECTOR_GUARD",
            "units": "dimensionless residual budget",
            "source_path": "MISSING_RESIDUAL_VECTOR_SOURCE_PATH",
            "status": "MISSING_NO_CANCELLATION_GUARD",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
    ]


def runner_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "run_id": "NPBR1640_0_exact_zero_branch",
            "formula": "Pi_R=0 -> Q_R=0 -> q_R=0 -> Delta gamma=0",
            "input_status": "MISSING_PARENT_Pi_R_ZERO_THEOREM",
            "runner_status": "NOT_SCORED_THEOREM_UNSIGNED",
            "result": "BLOCKED",
            "reason": "boundary object-language and worldtube projection are unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "NPBR1640_1_finite_bound_branch",
            "formula": "|q_R| = k_W |Pi_R| c^2/(2 G M_*)",
            "input_status": "MISSING_Pi_R_BOUND;MISSING_M_STAR;CONDITIONAL_k_W;MISSING_NO_CANCELLATION",
            "runner_status": "NOT_SCORED_MISSING_INPUTS",
            "result": "BLOCKED",
            "reason": "finite residual branch cannot be scored with placeholder inputs",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "NPBR1640_2_gamma_bound_inversion",
            "formula": "|Pi_R| <= (2 G M_*/(k_W c^2)) |Delta gamma|_max",
            "input_status": "MISSING_EXTERNAL_GAMMA_BOUND;MISSING_M_STAR;CONDITIONAL_k_W",
            "runner_status": "NOT_SCORED_MISSING_INPUTS",
            "result": "BLOCKED",
            "reason": "bound inversion is ready as a formula but has no claim-valid inputs",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1640_0_theorem",
            "decision": "PIR_ZERO_THEOREM_SHAPE_VALID_BUT_UNSIGNED",
            "reason": "free/proper boundary silence would force Pi_R=0, but source boundary class and object-language are not derived",
            "next_action": "derive boundary object-language from parent variation or keep Pi_R boundary bound row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1640_1_runner",
            "decision": "NORMALIZED_PPN_RUNNER_STAGED_NOT_SCORED",
            "reason": "1639 supplied the amplitude law, but Pi_R, M_*, k_W, gamma bound, and no-cancellation inputs are not claim-valid",
            "next_action": "fill inputs only with parent-signed/source-backed rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1640_2_best_next",
            "decision": "NEXT_BOUNDARY_OBJECT_LANGUAGE_OR_PIR_BOUND_SOURCE_ROW",
            "reason": "exact GR route is more valuable than finite bound filling, but fallback rows are now formula-ready",
            "next_action": "try to derive boundary/worldtube no-slot grammar; if it fails, acquire real Pi_R/M_* source rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1640_0_PiR_zero",
            "claim": "Pi_R=0 theorem",
            "status": "BLOCKED",
            "blocker": "boundary object-language, free/proper boundary class, and zero-projection clauses are unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1640_1_local_GR",
            "claim": "local GR recovered from R_AB/Pi_R branch",
            "status": "BLOCKED",
            "blocker": "Pi_R zero theorem is unsigned and finite branch is not source-bounded",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1640_2_PPN_runner",
            "claim": "normalized PPN runner score",
            "status": "BLOCKED",
            "blocker": "runner refuses missing Pi_R, M_*, gamma-bound, and no-cancellation inputs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1640_3_R10",
            "claim": "use massless reciprocal tail as finite-range R10 evidence",
            "status": "BLOCKED",
            "blocker": "massless Q_R/r branch remains local/PPN/orbital, not R10 alpha(lambda)",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1641-Y5-R2FR-boundary-object-language-from-parent-variation-or-PiR-source-row.md",
            "script": "scripts/Y5_R2FR_boundary_object_language_from_parent_variation_or_PiR_source_row.py",
            "objective": "derive the boundary/worldtube object-language that forbids independent R_AB/Pi_R slots and makes Pi_R=0 parent-signed; if impossible, acquire real nonclaim Pi_R_boundary_abs and M_star source rows for the normalized PPN runner",
            "success_condition": "either boundary no-slot/properness/zero-projection clauses are parent-signed, or Pi_R/M_star/k_W/gamma-bound inputs remain explicit source-acquisition rows with no scoring",
            "guardrails": "do not claim Pi_R=0 from closure, do not use orbital GM as M_star, do not score missing placeholders, do not route massless Q_R/r through R10",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        }
    ]


def all_claim_flags_false(paths: list[Path]) -> bool:
    for path in paths:
        for row in csv_rows(path):
            for column_name in ["valid_for_claim", "claim_allowed", "score_allowed"]:
                if column_name in row and bool_string(row[column_name]) == "true":
                    return False
    return True


def copy_outputs() -> None:
    paths = GENERATED + ([VALIDATION] if VALIDATION.exists() else [])
    for path in paths:
        for target_dir in [QUARANTINE, BRANCH_RESIDUALS]:
            shutil.copy2(path, target_dir / path.name)
    shutil.copy2(THEOREM_AUDIT, QUEUE / "JR1640_PIR_ZERO_BOUNDARY_SILENCE_THEOREM_AUDIT_NONCLAIM.csv")
    shutil.copy2(PPN_INPUTS, QUEUE / "JR1640_NORMALIZED_PPN_BOUND_INPUTS_NONCLAIM.csv")
    shutil.copy2(NEXT_TARGET, QUEUE / "JR1640_NEXT_TARGET_NONCLAIM.csv")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows() -> list[dict[str, object]]:
    source_rows = csv_rows(SOURCE_REGISTER)
    theorem = csv_rows(THEOREM_AUDIT)
    clauses = csv_rows(CLAUSE_LEDGER)
    ppn_inputs = csv_rows(PPN_INPUTS)
    runner = csv_rows(RUNNER)
    decisions = csv_rows(DECISION)
    gates = csv_rows(CLAIM_GATE)
    next_targets = csv_rows(NEXT_TARGET)

    checks = [
        (
            "VAL1640_0_sources_exist",
            all(bool_string(row["path_exists"]) == "true" for row in source_rows),
            "all 1640 cited source paths exist",
        ),
        (
            "VAL1640_1_needles_found",
            all(bool_string(row["needles_found"]) == "true" for row in source_rows),
            "all 1640 source needles found",
        ),
        (
            "VAL1640_2_theorem_sources_exist",
            all(source_paths_exist(row["source_paths"]) for row in theorem),
            "all theorem audit source paths exist",
        ),
        (
            "VAL1640_3_exact_chain_identified",
            any(row["claim_piece"] == "Pi_R=0 -> Q_R=0 -> q_R=0 -> Delta gamma=0" for row in theorem),
            "exact Pi_R zero to local gamma chain is identified",
        ),
        (
            "VAL1640_4_verdict_unsigned",
            any(row["status"] == "PIR_ZERO_NOT_PROVED_BOUNDARY_SILENCE_UNSIGNED" for row in theorem),
            "Pi_R zero theorem remains unsigned, not promoted",
        ),
        (
            "VAL1640_5_clause_failure_present",
            any(row["status"] == "FAIL_CURRENT_PROOF" for row in clauses)
            and any(row["required_clause"].startswith("B_matter/worldtube/readout") for row in clauses),
            "boundary silence clause ledger includes current proof failure",
        ),
        (
            "VAL1640_6_ppn_inputs_nonclaim",
            all(bool_string(row["valid_for_claim"]) == "false" and bool_string(row["score_allowed"]) == "false" for row in ppn_inputs),
            "normalized PPN input rows remain nonclaim/no-score",
        ),
        (
            "VAL1640_7_runner_refuses_missing_inputs",
            all(row["result"] == "BLOCKED" and row["runner_status"].startswith("NOT_SCORED") for row in runner),
            "normalized PPN runner refuses unsigned/missing inputs",
        ),
        (
            "VAL1640_8_decisions_recorded",
            all(
                required in {row["decision"] for row in decisions}
                for required in [
                    "PIR_ZERO_THEOREM_SHAPE_VALID_BUT_UNSIGNED",
                    "NORMALIZED_PPN_RUNNER_STAGED_NOT_SCORED",
                    "NEXT_BOUNDARY_OBJECT_LANGUAGE_OR_PIR_BOUND_SOURCE_ROW",
                ]
            ),
            "required 1640 decisions are recorded",
        ),
        (
            "VAL1640_9_claim_gates_closed",
            all(row["status"] == "BLOCKED" for row in gates),
            "all 1640 claim gates remain blocked",
        ),
        (
            "VAL1640_10_next_target_selected",
            next_targets[0]["next_target"] == "1641-Y5-R2FR-boundary-object-language-from-parent-variation-or-PiR-source-row.md",
            "next target selects boundary object-language or Pi_R source row",
        ),
        (
            "VAL1640_11_csv_parse",
            all(len(csv_rows(path)) > 0 for path in GENERATED),
            "all generated 1640 CSVs parse",
        ),
        (
            "VAL1640_12_nonclaim_flags",
            all_claim_flags_false(CLAIM_CHECKED),
            "all 1640 generated rows remain nonclaim/no-score",
        ),
        (
            "VAL1640_13_branch_copies",
            all((QUARANTINE / path.name).exists() and (BRANCH_RESIDUALS / path.name).exists() for path in GENERATED),
            "branch/quarantine copies exist",
        ),
        (
            "VAL1640_14_queue_copies",
            all(
                path.exists()
                for path in [
                    QUEUE / "JR1640_PIR_ZERO_BOUNDARY_SILENCE_THEOREM_AUDIT_NONCLAIM.csv",
                    QUEUE / "JR1640_NORMALIZED_PPN_BOUND_INPUTS_NONCLAIM.csv",
                    QUEUE / "JR1640_NEXT_TARGET_NONCLAIM.csv",
                ]
            ),
            "acquisition queue nonclaim copies exist",
        ),
        (
            "VAL1640_15_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
        ),
        (
            "VAL1640_16_formalization_untouched",
            not any(FORMALIZATION.rglob("*1640*")) if FORMALIZATION.exists() else True,
            "no 1640 outputs found under formalization-workbench",
        ),
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
            "check_id": "VAL1640_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1640 Pi_R zero boundary-silence theorem or normalized PPN runner validation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        cells = [str(row.get(column, "")).replace("\n", " ") for column in columns]
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body])


def write_doc() -> None:
    source_rows = csv_rows(SOURCE_REGISTER)
    theorem = csv_rows(THEOREM_AUDIT)
    clauses = csv_rows(CLAUSE_LEDGER)
    ppn_inputs = csv_rows(PPN_INPUTS)
    runner = csv_rows(RUNNER)
    decisions = csv_rows(DECISION)
    gates = csv_rows(CLAIM_GATE)
    next_targets = csv_rows(NEXT_TARGET)
    validation = csv_rows(VALIDATION)

    content = f"""# 1640 - Pi_R Zero Boundary Silence Or Normalized PPN Bound Runner

**Private status:** nonclaim checkpoint. No `Pi_R=0`, `Q_R=0`, local-GR, PPN, Newton, orbital, WEP, clock, EM, or R10 pass is claimed.

## Verdict

The exact route is now crisp:

```text
proper/free boundary silence -> Pi_R=0 -> Q_R=0 -> q_R=0 -> Delta gamma=0
```

That would be the clean GR-style win for the reciprocal-hair branch. But 1640 does **not** close it. The proof still needs a parent-derived boundary/worldtube object-language: no independent `R_AB`/`Pi_R` boundary slot, proper or exact boundary variation, zero local projection, and no hidden readout/EFT tail.

The finite fallback runner is also staged:

```text
|q_R| = k_W |Pi_R| c^2/(2 G M_*)
|Pi_R| <= (2 G M_*/(k_W c^2)) |Delta gamma|_max
```

It refuses to score because `Pi_R`, same-frame `M_*`, external gamma bound, and the no-cancellation vector are not source-backed.

## Source Register

{markdown_table(source_rows, ["source_id", "path", "path_exists", "needles_found", "role"])}

## Boundary-Silence Theorem Audit

{markdown_table(theorem, ["audit_id", "claim_piece", "status", "would_imply", "missing_piece"])}

## Clause Ledger

{markdown_table(clauses, ["clause_id", "required_clause", "status", "failure_mode_if_missing", "close_requirement"])}

## Normalized PPN Inputs

{markdown_table(ppn_inputs, ["input_id", "quantity", "required_for_formula", "current_value", "status"])}

## Normalized PPN Runner

{markdown_table(runner, ["run_id", "formula", "input_status", "runner_status", "result", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "claim", "status", "blocker"])}

## Next Target

{markdown_table(next_targets, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    outputs = {
        SOURCE_REGISTER: source_register_rows(),
        THEOREM_AUDIT: theorem_audit_rows(),
        CLAUSE_LEDGER: clause_ledger_rows(),
        PPN_INPUTS: ppn_input_rows(),
        RUNNER: runner_rows(),
        DECISION: decision_rows(),
        CLAIM_GATE: claim_gate_rows(),
        NEXT_TARGET: next_target_rows(),
    }
    for path, rows in outputs.items():
        write_csv(path, rows)

    copy_outputs()
    remove_pycache()
    write_csv(VALIDATION, validation_rows())
    copy_outputs()
    write_doc()
    remove_pycache()
    print(f"wrote {rel(DOC)}")
    print(f"validation {rel(VALIDATION)}")


if __name__ == "__main__":
    main()
