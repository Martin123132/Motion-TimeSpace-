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
QUARANTINE = MICROSCOPE / "quarantine" / "1641"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1641-Y5-R2FR-boundary-object-language-from-parent-variation-or-PiR-source-row.md"

SOURCE_FILES = {
    "1640_doc": ROOT / "1640-Y5-R2FR-PiR-zero-boundary-silence-or-normalized-PPN-bound-runner.md",
    "1640_validation": OUT / "P8_Y5_BRR545_1640_VALIDATION.csv",
    "1640_next": OUT / "P8_Y5_PARENT_QLOC_1640_NEXT_TARGET.csv",
    "1640_theorem": OUT / "P8_Y5_PARENT_QLOC_1640_PIR_ZERO_BOUNDARY_SILENCE_THEOREM_AUDIT.csv",
    "1640_inputs": OUT / "P8_Y5_PARENT_QLOC_1640_NORMALIZED_PPN_BOUND_INPUTS.csv",
    "05_reciprocity": ROOT / "05-reciprocity-theorem-attempt.md",
    "06_source_neutrality": ROOT / "06-reciprocal-charge-source-neutrality.md",
    "1636_doc": ROOT / "1636-Y5-R2FR-RAB-parent-object-language-or-PiR-residual-bound-pack.md",
    "1637_doc": ROOT / "1637-Y5-R2FR-no-independent-RAB-slot-grammar-or-first-PiR-bound-row.md",
    "1015_worldtube": ROOT / "1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md",
    "1016_selector": ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
    "parent_worldtube_clauses": OUT / "P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv",
    "hwt_attempt": OUT / "P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv",
    "hwt_certificate": OUT / "P8_Y5_HILBERT_WORLDTUBE_GLUE_CERTIFICATE.csv",
}

NEEDLES = {
    "1640_doc": ["proper/free boundary silence", "It refuses to score"],
    "1640_validation": ["VAL1640_OVERALL", "PASS"],
    "1640_next": ["1641-Y5-R2FR-boundary-object-language-from-parent-variation-or-PiR-source-row.md", "do not claim Pi_R=0"],
    "1640_theorem": ["PIR_ZERO_NOT_PROVED_BOUNDARY_SILENCE_UNSIGNED", "EXACT_LOCAL_GR_CHAIN_IDENTIFIED"],
    "1640_inputs": ["M_star_same_frame", "MISSING_SAME_FRAME_PARENT_SOURCE_MASS"],
    "05_reciprocity": ["W R_AB' = 0", "finite exterior energy + infinity boundary are not enough"],
    "06_source_neutrality": ["delta S_boundary", "fixed source R_AB boundary"],
    "1636_doc": ["BOUNDARY_OBJECT_LANGUAGE_MISSING", "OBJECT_LANGUAGE_NOT_DERIVED_CURRENT_CORPUS"],
    "1637_doc": ["BOUNDARY_SLOT_NOT_PARENT_SIGNED", "NO_INDEPENDENT_RAB_SLOT_NOT_DERIVED_CURRENT_CORPUS"],
    "1015_worldtube": ["conditional_reference_lemma", "current MTS lacks parent worldtube"],
    "1016_selector": ["W_source = closure(supp J_H[tau])", "Current MTS has not yet signed"],
    "parent_worldtube_clauses": ["W504_4_worldtube_source_measure_glue", "not_yet_derived_core_missing_piece"],
    "hwt_attempt": ["HWT536_0_parent_worldtube_fixed", "not_derived_for_current_MTS"],
    "hwt_certificate": ["HWG535_0_worldtube_fixed_before_readout", "missing_certificate"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1641_SOURCE_REGISTER.csv"
THEOREM_ATTEMPT = OUT / "P8_Y5_PARENT_QLOC_1641_BOUNDARY_OBJECT_LANGUAGE_THEOREM_ATTEMPT.csv"
CLAUSE_MAP = OUT / "P8_Y5_PARENT_QLOC_1641_PARENT_VARIATION_CLAUSE_MAP.csv"
PIR_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_1641_PIR_ZERO_CONTRACT.csv"
SOURCE_ROWS = OUT / "P8_Y5_PARENT_QLOC_1641_PIR_MSTAR_SOURCE_ACQUISITION_ROWS.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1641_DECISION.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1641_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1641_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1641_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    THEOREM_ATTEMPT,
    CLAUSE_MAP,
    PIR_CONTRACT,
    SOURCE_ROWS,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    THEOREM_ATTEMPT,
    CLAUSE_MAP,
    PIR_CONTRACT,
    SOURCE_ROWS,
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
                "role": "1641 boundary object-language from parent variation or source row",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def theorem_attempt_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "BOL1641_0_parent_variation_form",
            "theorem_clause": "a single covariant parent action gives delta L = E_A delta Phi^A + dTheta with boundary terms fixed before readout",
            "status": "CONDITIONAL_PARENT_VARIATION_FORM_AVAILABLE",
            "would_close": "defines the object-language in which boundary momentum must be generated",
            "why_not_closed": "current MTS still lacks a full parent Lagrangian/current derivation for this R_AB branch",
            "source_paths": ";".join([str(SOURCE_FILES["1016_selector"]), str(SOURCE_FILES["parent_worldtube_clauses"])]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "BOL1641_1_worldtube_selector",
            "theorem_clause": "W_source = closure(supp J_H[tau]) is selected before readout/fitting",
            "status": "CONDITIONAL_SELECTOR_AVAILABLE_NOT_SIGNED",
            "would_close": "prevents the boundary domain from being chosen after the local/PPN fit",
            "why_not_closed": "same-frame J_H[tau], tau, compactness, and source measure are unsigned",
            "source_paths": ";".join([str(SOURCE_FILES["1016_selector"]), str(SOURCE_FILES["hwt_attempt"])]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "BOL1641_2_no_boundary_RAB_slot",
            "theorem_clause": "B_boundary depends only on quotient/source data and contains no independent R_AB or Pi_R slot",
            "status": "BOUNDARY_NO_SLOT_CONTRACT_ONLY",
            "would_close": "removes the direct Pi_R boundary momentum source",
            "why_not_closed": "1636/1637 identify this as missing object-language, not a derivation",
            "source_paths": ";".join([str(SOURCE_FILES["1636_doc"]), str(SOURCE_FILES["1637_doc"])]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "BOL1641_3_vertical_exact_boundary",
            "theorem_clause": "i_vR Theta_matter + delta_vR B_matter is exact/proper with zero integral on linked source boundaries",
            "status": "ZERO_PROJECTION_CLAUSE_UNSIGNED",
            "would_close": "forces Pi_R_boundary_abs=0 even if bulk descent is already silent",
            "why_not_closed": "no parent certificate for exact boundary improvement or zero linked-boundary flux",
            "source_paths": ";".join([str(SOURCE_FILES["1640_theorem"]), str(SOURCE_FILES["hwt_certificate"])]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "BOL1641_4_hidden_tail_silence",
            "theorem_clause": "readout/domain/EFT boundary tails have no independent R_AB local projection",
            "status": "HIDDEN_TAIL_THEOREM_UNSIGNED",
            "would_close": "prevents a post-boundary Pi_R residual from re-entering local PPN observables",
            "why_not_closed": "hidden tail was an active obstruction in 1637 and remains unbounded",
            "source_paths": ";".join([str(SOURCE_FILES["1637_doc"]), str(SOURCE_FILES["1640_theorem"])]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "BOL1641_5_verdict",
            "theorem_clause": "boundary object-language from parent variation proves Pi_R=0",
            "status": "BOUNDARY_OBJECT_LANGUAGE_NOT_PARENT_DERIVED_CURRENT_CORPUS",
            "would_close": "would promote Pi_R=0 -> Q_R=0 -> q_R=0 -> local reciprocal-hair GR safety",
            "why_not_closed": "parent variation, worldtube selector, no-boundary-slot, exact boundary, and hidden-tail clauses are not jointly signed",
            "source_paths": ";".join([str(SOURCE_FILES["1640_doc"]), str(SOURCE_FILES["1016_selector"]), str(SOURCE_FILES["1637_doc"])]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def clause_map_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PVC1641_0_covariant_parent_action",
            "required_parent_clause": "explicit parent Lagrangian and symplectic potential before readout",
            "current_evidence": "contract exists in worldtube/source-measure machinery",
            "status": "CONTRACT_ONLY_NO_FULL_CURRENT_LAGRANGIAN",
            "observable_risk": "boundary momentum can be postulated rather than derived",
            "source_paths": ";".join([str(SOURCE_FILES["1016_selector"]), str(SOURCE_FILES["parent_worldtube_clauses"])]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PVC1641_1_fixed_worldtube",
            "required_parent_clause": "source worldtube fixed by Hilbert support before orbital/readout fitting",
            "current_evidence": "W_source selector is written as a conditional lemma",
            "status": "FORMAL_SELECTOR_CONDITIONAL",
            "observable_risk": "domain choice can hide residual mass or Pi_R flux",
            "source_paths": ";".join([str(SOURCE_FILES["1016_selector"]), str(SOURCE_FILES["hwt_attempt"])]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PVC1641_2_no_independent_RAB_boundary_slot",
            "required_parent_clause": "boundary action has no independent R_AB/Pi_R representative argument",
            "current_evidence": "1636/1637 identify the needed grammar",
            "status": "UNSIGNED_BOUNDARY_OBJECT_LANGUAGE",
            "observable_risk": "Pi_R can remain nonzero even when bulk source is silent",
            "source_paths": ";".join([str(SOURCE_FILES["1636_doc"]), str(SOURCE_FILES["1637_doc"])]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PVC1641_3_exact_boundary_improvement",
            "required_parent_clause": "exact/proper boundary improvement integrates to zero on compact linked boundaries",
            "current_evidence": "worldtube certificate marks exact term zero as missing",
            "status": "MISSING_CERTIFICATE_OR_BOUND",
            "observable_risk": "reference/boundary bookkeeping shifts the local source charge",
            "source_paths": str(SOURCE_FILES["hwt_certificate"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PVC1641_4_same_frame_mass",
            "required_parent_clause": "same-frame M_star source mass is derived before PPN/orbital comparison",
            "current_evidence": "1640/1016 require M_star/M_H_ref but do not fill it",
            "status": "MISSING_SOURCE_MASS_CALIBRATION",
            "observable_risk": "using orbital GM would circularly assume the Newtonian limit",
            "source_paths": ";".join([str(SOURCE_FILES["1640_inputs"]), str(SOURCE_FILES["1016_selector"])]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PVC1641_5_all_clauses",
            "required_parent_clause": "all boundary object-language clauses jointly close",
            "current_evidence": "no current source signs the full stack",
            "status": "FAIL_CURRENT_PROOF",
            "observable_risk": "Pi_R=0 remains a closure/theorem target, not a result",
            "source_paths": ";".join([str(SOURCE_FILES["1640_doc"]), str(SOURCE_FILES["1640_theorem"])]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def pir_contract_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "contract_id": "PZC1641_0_if_signed",
            "contract_statement": "If the parent action owns the worldtube selector, no independent R_AB/Pi_R boundary slot exists, and the vertical boundary term is exact/proper with zero local projection, then Pi_R=0.",
            "proof_role": "exact local-GR reciprocal-hair route",
            "current_status": "CONDITIONAL_THEOREM_CONTRACT",
            "failure_mode": "any unsigned boundary slot or hidden tail leaves Q_R/r hair alive",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "PZC1641_1_chain",
            "contract_statement": "Pi_R=0 -> Q_R=0 -> q_R=0 -> Delta gamma=0 after the 1639 amplitude law.",
            "proof_role": "maps boundary silence into local PPN silence",
            "current_status": "CHAIN_VALID_THEOREM_INPUT_UNSIGNED",
            "failure_mode": "Pi_R zero theorem is missing, so the chain cannot be claimed",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "PZC1641_2_fallback",
            "contract_statement": "If Pi_R=0 is not proved, retain |q_R| = k_W |Pi_R| c^2/(2GM_*) and acquire real source rows.",
            "proof_role": "finite residual/empirical fallback",
            "current_status": "SOURCE_ACQUISITION_REQUIRED",
            "failure_mode": "placeholder Pi_R/M_star rows cannot be scored",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
    ]


def source_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SRC1641_0_PiR_boundary_abs",
            "quantity": "Pi_R_boundary_abs",
            "formula_role": "|q_R| = k_W |Pi_R| c^2/(2 G M_*)",
            "required_source": "parent boundary-zero theorem or empirical absolute boundary-tail coefficient",
            "current_value": "MISSING_BOUND_VALUE",
            "units": "reciprocal-tail length units after worldtube projection",
            "source_path": "MISSING_PARENT_OR_EMPIRICAL_SOURCE_PATH",
            "status": "MISSING_SOURCE_ROW",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SRC1641_1_Mstar_same_frame",
            "quantity": "M_star_same_frame",
            "formula_role": "N_R = c^2/(2 G M_*)",
            "required_source": "parent Hilbert/Noether source mass or same-frame M_H_ref calibration before orbital fitting",
            "current_value": "MISSING_SAME_FRAME_PARENT_SOURCE_MASS",
            "units": "mass",
            "source_path": "MISSING_PARENT_SOURCE_MASS_PATH",
            "status": "MISSING_SOURCE_ROW",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SRC1641_2_kW_tail",
            "quantity": "k_W_tail",
            "formula_role": "R_AB = k_W Q_R/r",
            "required_source": "parent W(r) radial equation showing the corpus k_W=1 normalization",
            "current_value": "CONDITIONAL_k_W_EQUALS_1_FROM_CORPUS_NOT_PARENT_SIGNED",
            "units": "dimensionless",
            "source_path": str(SOURCE_FILES["05_reciprocity"]),
            "status": "CONDITIONAL_SOURCE_ROW",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SRC1641_3_gamma_bound",
            "quantity": "Delta_gamma_abs_max",
            "formula_role": "|Pi_R| <= (2 G M_*/(k_W c^2)) |Delta gamma|_max",
            "required_source": "current external PPN gamma bound with citation/extraction method",
            "current_value": "MISSING_CURRENT_EXTERNAL_PPN_GAMMA_BOUND",
            "units": "dimensionless",
            "source_path": "MISSING_EXTERNAL_PPN_SOURCE_PATH",
            "status": "MISSING_SOURCE_ROW",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SRC1641_4_no_cancellation",
            "quantity": "absolute_local_residual_vector",
            "formula_role": "no cancellation credit for Pi_R against unrelated local residuals",
            "required_source": "absolute residual-vector ledger covering Pi_R, GK/q_loc, readout, frame, and source-mass channels",
            "current_value": "MISSING_ABSOLUTE_VECTOR_GUARD",
            "units": "dimensionless residual budget",
            "source_path": "MISSING_RESIDUAL_VECTOR_SOURCE_PATH",
            "status": "MISSING_SOURCE_ROW",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1641_0_boundary_language",
            "decision": "BOUNDARY_OBJECT_LANGUAGE_CONTRACT_REFINED_NOT_DERIVED",
            "reason": "worldtube and parent-variation clauses give a clean contract but not a parent-signed R_AB boundary theorem",
            "next_action": "attack the minimal boundary variation clause directly",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1641_1_selector",
            "decision": "WORLDTUBE_SELECTOR_CONDITIONAL_IMPORTED",
            "reason": "1016 supplies W_source=closure(supp J_H[tau]) as the right selector but leaves parent ownership unsigned",
            "next_action": "reuse selector as a requirement, not as a claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1641_2_PiR_zero",
            "decision": "PIR_ZERO_NOT_PARENT_SIGNED",
            "reason": "no-boundary-slot, exact boundary, hidden-tail, and same-frame mass clauses remain open",
            "next_action": "keep local GR blocked; do not promote closure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1641_3_source_rows",
            "decision": "PIR_MSTAR_SOURCE_ROWS_STAGED_NONCLAIM",
            "reason": "fallback normalized PPN runner now has explicit missing inputs",
            "next_action": "fill only with parent-signed/source-backed rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1641_0_boundary_language",
            "claim": "boundary object-language proves Pi_R=0",
            "status": "BLOCKED",
            "blocker": "contract refined but not derived from parent variation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1641_1_local_GR",
            "claim": "local GR recovered through reciprocal-hair branch",
            "status": "BLOCKED",
            "blocker": "Pi_R zero theorem and finite source rows are not claim-valid",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1641_2_normalized_PPN",
            "claim": "normalized PPN runner can score",
            "status": "BLOCKED",
            "blocker": "Pi_R_boundary_abs, M_star, gamma bound, and absolute vector remain missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1641_3_R10",
            "claim": "massless reciprocal tail is finite-range R10 evidence",
            "status": "BLOCKED",
            "blocker": "massless Q_R/r remains PPN/local/orbital, not R10 alpha(lambda)",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1642-Y5-R2FR-minimal-boundary-variation-clause-or-PiR-Mstar-source-fill.md",
            "script": "scripts/Y5_R2FR_minimal_boundary_variation_clause_or_PiR_Mstar_source_fill.py",
            "objective": "try to derive the minimal boundary variation clause i_vR Theta_matter + delta_vR B_matter = dC_R with zero linked-boundary integral; if it fails, fill strict nonclaim Pi_R_boundary_abs and M_star acquisition rows",
            "success_condition": "either the exact/proper boundary zero-projection clause is parent-signed, or Pi_R/M_star source rows remain explicit missing-input rows with no scoring",
            "guardrails": "do not claim Pi_R=0 from contract language, do not use orbital GM as M_star, do not score placeholders, do not route massless Q_R/r through R10",
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
    shutil.copy2(THEOREM_ATTEMPT, QUEUE / "JR1641_BOUNDARY_OBJECT_LANGUAGE_THEOREM_ATTEMPT_NONCLAIM.csv")
    shutil.copy2(SOURCE_ROWS, QUEUE / "JR1641_PIR_MSTAR_SOURCE_ACQUISITION_ROWS_NONCLAIM.csv")
    shutil.copy2(NEXT_TARGET, QUEUE / "JR1641_NEXT_TARGET_NONCLAIM.csv")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows() -> list[dict[str, object]]:
    source_rows = csv_rows(SOURCE_REGISTER)
    theorem = csv_rows(THEOREM_ATTEMPT)
    clauses = csv_rows(CLAUSE_MAP)
    contract = csv_rows(PIR_CONTRACT)
    source_rows_needed = csv_rows(SOURCE_ROWS)
    decisions = csv_rows(DECISION)
    gates = csv_rows(CLAIM_GATE)
    next_targets = csv_rows(NEXT_TARGET)

    checks = [
        (
            "VAL1641_0_sources_exist",
            all(bool_string(row["path_exists"]) == "true" for row in source_rows),
            "all 1641 cited source paths exist",
        ),
        (
            "VAL1641_1_needles_found",
            all(bool_string(row["needles_found"]) == "true" for row in source_rows),
            "all 1641 source needles found",
        ),
        (
            "VAL1641_2_theorem_sources_exist",
            all(source_paths_exist(row["source_paths"]) for row in theorem),
            "all boundary object-language theorem source paths exist",
        ),
        (
            "VAL1641_3_final_verdict_unpromoted",
            any(row["status"] == "BOUNDARY_OBJECT_LANGUAGE_NOT_PARENT_DERIVED_CURRENT_CORPUS" for row in theorem),
            "boundary object-language theorem remains unpromoted",
        ),
        (
            "VAL1641_4_clause_map_complete",
            all(
                required in {row["clause_id"] for row in clauses}
                for required in [
                    "PVC1641_0_covariant_parent_action",
                    "PVC1641_1_fixed_worldtube",
                    "PVC1641_2_no_independent_RAB_boundary_slot",
                    "PVC1641_3_exact_boundary_improvement",
                    "PVC1641_4_same_frame_mass",
                    "PVC1641_5_all_clauses",
                ]
            ),
            "parent variation clause map covers all required clauses",
        ),
        (
            "VAL1641_5_contract_chain_present",
            any("Pi_R=0 -> Q_R=0 -> q_R=0 -> Delta gamma=0" in row["contract_statement"] for row in contract),
            "Pi_R zero to local gamma chain remains explicitly staged",
        ),
        (
            "VAL1641_6_source_rows_complete_nonclaim",
            all(
                required in {row["quantity"] for row in source_rows_needed}
                for required in [
                    "Pi_R_boundary_abs",
                    "M_star_same_frame",
                    "k_W_tail",
                    "Delta_gamma_abs_max",
                    "absolute_local_residual_vector",
                ]
            )
            and all(bool_string(row["valid_for_claim"]) == "false" and bool_string(row["score_allowed"]) == "false" for row in source_rows_needed),
            "Pi_R/Mstar/kW/gamma/no-cancellation source rows are staged as nonclaim",
        ),
        (
            "VAL1641_7_decisions_recorded",
            all(
                required in {row["decision"] for row in decisions}
                for required in [
                    "BOUNDARY_OBJECT_LANGUAGE_CONTRACT_REFINED_NOT_DERIVED",
                    "WORLDTUBE_SELECTOR_CONDITIONAL_IMPORTED",
                    "PIR_ZERO_NOT_PARENT_SIGNED",
                    "PIR_MSTAR_SOURCE_ROWS_STAGED_NONCLAIM",
                ]
            ),
            "required 1641 decisions are recorded",
        ),
        (
            "VAL1641_8_claim_gates_closed",
            all(row["status"] == "BLOCKED" for row in gates),
            "all 1641 claim gates remain blocked",
        ),
        (
            "VAL1641_9_next_target_selected",
            next_targets[0]["next_target"] == "1642-Y5-R2FR-minimal-boundary-variation-clause-or-PiR-Mstar-source-fill.md",
            "next target selects minimal boundary variation clause or PiR/Mstar source fill",
        ),
        (
            "VAL1641_10_csv_parse",
            all(len(csv_rows(path)) > 0 for path in GENERATED),
            "all generated 1641 CSVs parse",
        ),
        (
            "VAL1641_11_nonclaim_flags",
            all_claim_flags_false(CLAIM_CHECKED),
            "all 1641 generated rows remain nonclaim/no-score",
        ),
        (
            "VAL1641_12_branch_copies",
            all((QUARANTINE / path.name).exists() and (BRANCH_RESIDUALS / path.name).exists() for path in GENERATED),
            "branch/quarantine copies exist",
        ),
        (
            "VAL1641_13_queue_copies",
            all(
                path.exists()
                for path in [
                    QUEUE / "JR1641_BOUNDARY_OBJECT_LANGUAGE_THEOREM_ATTEMPT_NONCLAIM.csv",
                    QUEUE / "JR1641_PIR_MSTAR_SOURCE_ACQUISITION_ROWS_NONCLAIM.csv",
                    QUEUE / "JR1641_NEXT_TARGET_NONCLAIM.csv",
                ]
            ),
            "acquisition queue nonclaim copies exist",
        ),
        (
            "VAL1641_14_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
        ),
        (
            "VAL1641_15_formalization_untouched",
            not any(FORMALIZATION.rglob("*1641*")) if FORMALIZATION.exists() else True,
            "no 1641 outputs found under formalization-workbench",
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
            "check_id": "VAL1641_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1641 boundary object-language or Pi_R source row validation",
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
    source_rows_data = csv_rows(SOURCE_REGISTER)
    theorem = csv_rows(THEOREM_ATTEMPT)
    clauses = csv_rows(CLAUSE_MAP)
    contract = csv_rows(PIR_CONTRACT)
    source_rows_data_needed = csv_rows(SOURCE_ROWS)
    decisions = csv_rows(DECISION)
    gates = csv_rows(CLAIM_GATE)
    next_targets = csv_rows(NEXT_TARGET)
    validation = csv_rows(VALIDATION)

    content = f"""# 1641 - Boundary Object-Language From Parent Variation Or Pi_R Source Row

**Private status:** nonclaim checkpoint. No `Pi_R=0`, `Q_R=0`, local-GR, PPN, Newton, orbital, WEP, clock, EM, or R10 pass is claimed.

## Verdict

The boundary route is now a precise parent-action contract, but it is still not a derived theorem. The clean win would be:

```text
parent-owned W_source
+ no independent R_AB/Pi_R boundary slot
+ exact/proper vertical boundary term with zero linked-boundary integral
+ no hidden readout/EFT tail
=> Pi_R = 0
=> Q_R = 0
=> q_R = 0
=> Delta gamma = 0
```

The corpus has enough worldtube/source-measure machinery to state the right selector, especially `W_source = closure(supp J_H[tau])`, but it has not parent-signed the source current, same-frame mass, boundary zero, or hidden-tail clauses. So 1641 does **not** promote local GR. It narrows the next derivation target to the minimal boundary variation clause.

## Source Register

{markdown_table(source_rows_data, ["source_id", "path", "path_exists", "needles_found", "role"])}

## Boundary Object-Language Theorem Attempt

{markdown_table(theorem, ["attempt_id", "theorem_clause", "status", "would_close", "why_not_closed"])}

## Parent Variation Clause Map

{markdown_table(clauses, ["clause_id", "required_parent_clause", "current_evidence", "status", "observable_risk"])}

## Pi_R Zero Contract

{markdown_table(contract, ["contract_id", "contract_statement", "proof_role", "current_status", "failure_mode"])}

## Source Acquisition Rows

{markdown_table(source_rows_data_needed, ["row_id", "quantity", "formula_role", "current_value", "status"])}

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
        THEOREM_ATTEMPT: theorem_attempt_rows(),
        CLAUSE_MAP: clause_map_rows(),
        PIR_CONTRACT: pir_contract_rows(),
        SOURCE_ROWS: source_rows(),
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
