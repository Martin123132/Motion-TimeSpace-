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
QUARANTINE = MICROSCOPE / "quarantine" / "1642"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1642-Y5-R2FR-minimal-boundary-variation-clause-or-PiR-Mstar-source-fill.md"

SOURCE_FILES = {
    "1641_doc": ROOT / "1641-Y5-R2FR-boundary-object-language-from-parent-variation-or-PiR-source-row.md",
    "1641_validation": OUT / "P8_Y5_BRR545_1641_VALIDATION.csv",
    "1641_next": OUT / "P8_Y5_PARENT_QLOC_1641_NEXT_TARGET.csv",
    "1641_contract": OUT / "P8_Y5_PARENT_QLOC_1641_PIR_ZERO_CONTRACT.csv",
    "1641_source_rows": OUT / "P8_Y5_PARENT_QLOC_1641_PIR_MSTAR_SOURCE_ACQUISITION_ROWS.csv",
    "05_reciprocity": ROOT / "05-reciprocity-theorem-attempt.md",
    "06_source_neutrality": ROOT / "06-reciprocal-charge-source-neutrality.md",
    "545_first_status": OUT / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv",
    "545_minimal_contract": OUT / "P8_Y5_BOUNDARY_REFERENCE_MINIMAL_ACTION_CONTRACT.csv",
    "545_ownership": OUT / "P8_Y5_BOUNDARY_REFERENCE_PARENT_OWNERSHIP_AUDIT.csv",
    "672_boundary_exactness": ROOT / "672-Y5-R10-boundary-exactness-projector-orthogonality-or-edge-coefficient-source-plan.md",
    "671_boundary_owner": ROOT / "671-Y5-R10-parent-Omega-DCX-boundary-charge-owner-or-edge-residual-vector.md",
    "1015_worldtube": ROOT / "1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md",
    "1016_selector": ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
}

NEEDLES = {
    "1641_doc": ["minimal boundary variation clause", "BOUNDARY_OBJECT_LANGUAGE_NOT_PARENT_DERIVED_CURRENT_CORPUS"],
    "1641_validation": ["VAL1641_OVERALL", "PASS"],
    "1641_next": ["1642-Y5-R2FR-minimal-boundary-variation-clause-or-PiR-Mstar-source-fill.md", "do not use orbital GM"],
    "1641_contract": ["Pi_R=0 -> Q_R=0 -> q_R=0 -> Delta gamma=0", "SOURCE_ACQUISITION_REQUIRED"],
    "1641_source_rows": ["Pi_R_boundary_abs", "M_star_same_frame", "MISSING_BOUND_VALUE"],
    "05_reciprocity": ["W R_AB' = 0", "finite exterior energy + infinity boundary are not enough"],
    "06_source_neutrality": ["delta S_boundary", "Pi_R = 0 -> Q_R = 0"],
    "545_first_status": ["B_zero_flux", "missing_claim_valid_source_or_zero_theorem"],
    "545_minimal_contract": ["MAC545_3_boundary_exact_cohomology_zero", "current corpus warns exact/topological labels alone are not enough"],
    "545_ownership": ["POA545_3_boundary", "boundary scalar/no-flux statements are conditional"],
    "672_boundary_exactness": ["BE672_1_BX_exact_form", "not_parent_derived"],
    "671_boundary_owner": ["BCG671_2_exact_boundary_form", "not_derived"],
    "1015_worldtube": ["SOL1015_4_boundary_zero", "not_signed_for_current_MTS"],
    "1016_selector": ["PSC1016_8_boundary_reference_lock", "missing_theorem_or_source_input"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1642_SOURCE_REGISTER.csv"
MINIMAL_ATTEMPT = OUT / "P8_Y5_PARENT_QLOC_1642_MINIMAL_BOUNDARY_VARIATION_ATTEMPT.csv"
EXACTNESS_GATES = OUT / "P8_Y5_PARENT_QLOC_1642_EXACT_BOUNDARY_ZERO_GATES.csv"
SOURCE_FILL = OUT / "P8_Y5_PARENT_QLOC_1642_PIR_MSTAR_SOURCE_FILL_ROWS.csv"
PPN_RULE = OUT / "P8_Y5_PARENT_QLOC_1642_NORMALIZED_PPN_SCORE_RULE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1642_DECISION.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1642_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1642_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1642_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    MINIMAL_ATTEMPT,
    EXACTNESS_GATES,
    SOURCE_FILL,
    PPN_RULE,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    MINIMAL_ATTEMPT,
    EXACTNESS_GATES,
    SOURCE_FILL,
    PPN_RULE,
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
                "role": "1642 minimal boundary variation clause or Pi_R/Mstar source fill",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def minimal_attempt_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MBV1642_0_target_clause",
            "clause": "i_vR Theta_matter + delta_vR B_matter = d_boundary C_R",
            "status": "MINIMAL_CLAUSE_IDENTIFIED",
            "would_imply": "vertical boundary momentum is an exact boundary improvement",
            "missing_or_conditional": "explicit parent C_R primitive and allowed v_R domain",
            "source_paths": ";".join([str(SOURCE_FILES["1641_next"]), str(SOURCE_FILES["672_boundary_exactness"])]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MBV1642_1_zero_flux_condition",
            "clause": "integral_linked_boundary d_boundary C_R = 0",
            "status": "MATHEMATICAL_IF_CLOSED_OR_MATCHED_BOUNDARY",
            "would_imply": "Pi_R_boundary_abs=0 after projection onto the local source boundary",
            "missing_or_conditional": "closed shell or matched S_inner/S_outer values plus no corner/reference term",
            "source_paths": ";".join([str(SOURCE_FILES["545_minimal_contract"]), str(SOURCE_FILES["1015_worldtube"])]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MBV1642_2_worldtube_domain",
            "clause": "W_source and linked surfaces are fixed before readout/fitting",
            "status": "CONDITIONAL_SELECTOR_AVAILABLE_NOT_PARENT_SIGNED",
            "would_imply": "the zero-flux integral is evaluated on the same compact source worldtube",
            "missing_or_conditional": "same-frame J_H[tau], tau, compactness, and source measure",
            "source_paths": str(SOURCE_FILES["1016_selector"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MBV1642_3_exact_not_enough",
            "clause": "exact/topological labels cannot by themselves kill physical source flux",
            "status": "EXACTNESS_WARNING_ACTIVE",
            "would_imply": "prevents treating dC_R as a magic zero",
            "missing_or_conditional": "cohomology-zero, corner-zero, projector/reference-zero, and physical-mass orthogonality certificates",
            "source_paths": ";".join([str(SOURCE_FILES["545_minimal_contract"]), str(SOURCE_FILES["672_boundary_exactness"])]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MBV1642_4_verdict",
            "clause": "minimal boundary variation clause proves Pi_R=0",
            "status": "MINIMAL_BOUNDARY_VARIATION_CLAUSE_NOT_PARENT_SIGNED",
            "would_imply": "would close Pi_R=0 -> Q_R=0 -> q_R=0 -> Delta gamma=0",
            "missing_or_conditional": "C_R primitive, boundary class, zero linked-boundary flux, fixed worldtube, same-frame source mass",
            "source_paths": ";".join([str(SOURCE_FILES["1641_contract"]), str(SOURCE_FILES["545_ownership"]), str(SOURCE_FILES["1016_selector"])]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def exactness_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "EBZ1642_0_parent_primitive",
            "required_gate": "parent-derived C_R primitive for i_vR Theta_matter + delta_vR B_matter",
            "current_status": "MISSING_PARENT_PRIMITIVE",
            "why_needed": "without C_R, exactness is named but not constructed",
            "repair": "derive C_R from the parent matter/boundary action or fill Pi_R residual",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "EBZ1642_1_boundary_class",
            "required_gate": "closed compact shell or homologous linked surfaces with matched C_R",
            "current_status": "BOUNDARY_CLASS_CONDITIONAL",
            "why_needed": "exact forms can carry finite corner/reference shifts if the domain is not fixed",
            "repair": "parent-sign W_source and linked-surface class before readout",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "EBZ1642_2_corner_reference",
            "required_gate": "corner, reference, and counterterm flux vanish or are fixed once",
            "current_status": "MISSING_CERTIFICATE_OR_BOUND",
            "why_needed": "boundary bookkeeping can move measured mass or Pi_R flux",
            "repair": "source B_zero_flux/Delta_symp/H_ref rows or derive fixed reference",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "EBZ1642_3_projector_orthogonality",
            "required_gate": "local source/PPN projector is orthogonal to exact boundary edge charge",
            "current_status": "NOT_DERIVED",
            "why_needed": "an exact edge term may still be seen by the measured source projector",
            "repair": "derive projector orthogonality or retain edge/Pi_R residual",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "EBZ1642_4_same_frame_mass",
            "required_gate": "M_star or M_H_ref is parent-owned before orbital/PPN comparison",
            "current_status": "MISSING_SAME_FRAME_PARENT_SOURCE_MASS",
            "why_needed": "finite Pi_R bounds need a non-circular denominator",
            "repair": "derive M_star from Hilbert/Noether source measure or keep source row missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "EBZ1642_5_all_gates",
            "required_gate": "all exact/proper boundary gates close together",
            "current_status": "FAIL_CURRENT_PROOF",
            "why_needed": "Pi_R=0 cannot be claimed from any one conditional clause",
            "repair": "continue derivation or source Pi_R/Mstar rows as finite residuals",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def source_fill_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SF1642_0_PiR_boundary_abs",
            "quantity": "Pi_R_boundary_abs",
            "formula_role": "|q_R| = k_W |Pi_R| c^2/(2 G M_*)",
            "required_source": "parent zero theorem or absolute boundary-tail value after worldtube projection",
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
            "row_id": "SF1642_1_Bzero_flux",
            "quantity": "B_zero_flux",
            "formula_role": "linked-boundary flux of dC_R/exact improvement contributing to Pi_R",
            "required_source": "theorem-zero or finite boundary/reference flux with units and surface class",
            "current_value": "MISSING_B_ZERO_FLUX",
            "units": "GM-flux or reciprocal-boundary units before normalization",
            "source_path": "MISSING_BOUNDARY_REFERENCE_SOURCE_PATH",
            "status": "MISSING_SOURCE_ROW",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SF1642_2_Mstar_same_frame",
            "quantity": "M_star_same_frame",
            "formula_role": "N_R = c^2/(2 G M_*)",
            "required_source": "parent Hilbert/Noether source mass or same-frame M_H_ref before orbital fitting",
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
            "row_id": "SF1642_3_kW_tail",
            "quantity": "k_W_tail",
            "formula_role": "R_AB = k_W Q_R/r",
            "required_source": "parent W(r) radial equation and integration convention",
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
            "row_id": "SF1642_4_Delta_gamma_bound",
            "quantity": "Delta_gamma_abs_max",
            "formula_role": "|Pi_R| <= (2 G M_*/(k_W c^2)) |Delta gamma|_max",
            "required_source": "external PPN gamma bound with citation/extraction method",
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
            "row_id": "SF1642_5_absolute_vector",
            "quantity": "absolute_local_residual_vector",
            "formula_role": "no cancellation credit across Pi_R, boundary, source-mass, readout, and q_loc residuals",
            "required_source": "absolute residual-vector ledger with all local channels included",
            "current_value": "MISSING_ABSOLUTE_VECTOR_GUARD",
            "units": "dimensionless residual budget",
            "source_path": "MISSING_RESIDUAL_VECTOR_SOURCE_PATH",
            "status": "MISSING_SOURCE_ROW",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
    ]


def ppn_rule_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "rule_id": "PPR1642_0_exact_branch",
            "rule": "If EBZ1642 all pass, set Pi_R=Q_R=q_R=Delta_gamma=0 for this reciprocal-hair branch.",
            "status": "BLOCKED_BY_EXACT_BOUNDARY_GATES",
            "allowed_to_score": False,
            "reason": "minimal boundary variation clause is not parent-signed",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "rule_id": "PPR1642_1_finite_branch",
            "rule": "|q_R| = k_W |Pi_R| c^2/(2 G M_*) and |Delta_gamma| ~= |q_R|",
            "status": "BLOCKED_BY_MISSING_SOURCE_ROWS",
            "allowed_to_score": False,
            "reason": "Pi_R, M_star, gamma bound, and absolute vector are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "rule_id": "PPR1642_2_R10_guard",
            "rule": "Do not route massless Q_R/r through finite-range R10 alpha(lambda).",
            "status": "GUARDRAIL_ACTIVE",
            "allowed_to_score": False,
            "reason": "this branch is local/PPN/orbital unless a finite carrier is separately derived",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1642_0_minimal_clause",
            "decision": "MINIMAL_BOUNDARY_VARIATION_CLAUSE_IDENTIFIED_NOT_DERIVED",
            "reason": "i_vR Theta + delta_vR B = dC_R is sufficient only after C_R, boundary class, and zero-flux are parent-signed",
            "next_action": "do not promote exactness; either derive C_R or fill residual rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1642_1_zero_theorem",
            "decision": "PIR_ZERO_REMAINS_BLOCKED",
            "reason": "all exact/proper boundary gates do not close together",
            "next_action": "keep local GR blocked in the reciprocal-hair branch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1642_2_source_fill",
            "decision": "PIR_MSTAR_BZERO_SOURCE_ROWS_STAGED_NONCLAIM",
            "reason": "finite residual fallback now has explicit Pi_R, B_zero, Mstar, kW, gamma, and no-cancellation rows",
            "next_action": "fill rows only from parent-signed/source-backed inputs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1642_0_minimal_boundary",
            "claim": "minimal exact/proper boundary clause proves Pi_R=0",
            "status": "BLOCKED",
            "blocker": "C_R primitive, boundary class, zero-flux, and same-frame source clauses are unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1642_1_local_GR",
            "claim": "local GR recovered through reciprocal-hair branch",
            "status": "BLOCKED",
            "blocker": "Pi_R zero theorem is unsigned and finite rows are unfilled",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1642_2_PPN_score",
            "claim": "normalized PPN score can run",
            "status": "BLOCKED",
            "blocker": "Pi_R/Mstar/Bzero/gamma/no-cancellation source rows are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1642_3_R10",
            "claim": "massless reciprocal tail is finite-range R10 evidence",
            "status": "BLOCKED",
            "blocker": "massless Q_R/r remains local/PPN/orbital, not R10 alpha(lambda)",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1643-Y5-R2FR-PiR-Mstar-source-acquisition-and-current-PPN-bound-runner.md",
            "script": "scripts/Y5_R2FR_PiR_Mstar_source_acquisition_and_current_PPN_bound_runner.py",
            "objective": "fill the finite residual branch only with source-backed Pi_R_boundary_abs, B_zero_flux, M_star, k_W, current PPN gamma bound, and no-cancellation inputs; if source acquisition fails, keep a blocker ledger",
            "success_condition": "either claim-valid source rows exist for every normalized PPN runner input, or the runner explicitly refuses scoring with exact missing inputs",
            "guardrails": "do not use orbital GM as M_star, do not claim Pi_R=0 from exactness labels, do not score placeholders, do not route massless Q_R/r through R10",
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
    shutil.copy2(MINIMAL_ATTEMPT, QUEUE / "JR1642_MINIMAL_BOUNDARY_VARIATION_ATTEMPT_NONCLAIM.csv")
    shutil.copy2(SOURCE_FILL, QUEUE / "JR1642_PIR_MSTAR_SOURCE_FILL_ROWS_NONCLAIM.csv")
    shutil.copy2(NEXT_TARGET, QUEUE / "JR1642_NEXT_TARGET_NONCLAIM.csv")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows() -> list[dict[str, object]]:
    source_rows = csv_rows(SOURCE_REGISTER)
    attempt = csv_rows(MINIMAL_ATTEMPT)
    gates = csv_rows(EXACTNESS_GATES)
    fill = csv_rows(SOURCE_FILL)
    rules = csv_rows(PPN_RULE)
    decisions = csv_rows(DECISION)
    claim_gates = csv_rows(CLAIM_GATE)
    next_targets = csv_rows(NEXT_TARGET)

    checks = [
        (
            "VAL1642_0_sources_exist",
            all(bool_string(row["path_exists"]) == "true" for row in source_rows),
            "all 1642 cited source paths exist",
        ),
        (
            "VAL1642_1_needles_found",
            all(bool_string(row["needles_found"]) == "true" for row in source_rows),
            "all 1642 source needles found",
        ),
        (
            "VAL1642_2_attempt_sources_exist",
            all(source_paths_exist(row["source_paths"]) for row in attempt),
            "all minimal boundary attempt source paths exist",
        ),
        (
            "VAL1642_3_minimal_clause_present",
            any(row["clause"] == "i_vR Theta_matter + delta_vR B_matter = d_boundary C_R" for row in attempt),
            "minimal boundary variation clause is present",
        ),
        (
            "VAL1642_4_verdict_unproved",
            any(row["status"] == "MINIMAL_BOUNDARY_VARIATION_CLAUSE_NOT_PARENT_SIGNED" for row in attempt),
            "minimal boundary variation clause remains unproved",
        ),
        (
            "VAL1642_5_exactness_gates_complete",
            all(
                required in {row["gate_id"] for row in gates}
                for required in [
                    "EBZ1642_0_parent_primitive",
                    "EBZ1642_1_boundary_class",
                    "EBZ1642_2_corner_reference",
                    "EBZ1642_3_projector_orthogonality",
                    "EBZ1642_4_same_frame_mass",
                    "EBZ1642_5_all_gates",
                ]
            ),
            "exact boundary zero gates cover primitive, class, reference, projector, mass, and all-gate checks",
        ),
        (
            "VAL1642_6_source_rows_complete_nonclaim",
            all(
                required in {row["quantity"] for row in fill}
                for required in [
                    "Pi_R_boundary_abs",
                    "B_zero_flux",
                    "M_star_same_frame",
                    "k_W_tail",
                    "Delta_gamma_abs_max",
                    "absolute_local_residual_vector",
                ]
            )
            and all(bool_string(row["valid_for_claim"]) == "false" and bool_string(row["score_allowed"]) == "false" for row in fill),
            "PiR/Bzero/Mstar/kW/gamma/no-cancellation rows are staged as nonclaim",
        ),
        (
            "VAL1642_7_score_rules_blocked",
            all(bool_string(row["allowed_to_score"]) == "false" and bool_string(row["score_allowed"]) == "false" for row in rules),
            "normalized PPN score rules remain blocked",
        ),
        (
            "VAL1642_8_decisions_recorded",
            all(
                required in {row["decision"] for row in decisions}
                for required in [
                    "MINIMAL_BOUNDARY_VARIATION_CLAUSE_IDENTIFIED_NOT_DERIVED",
                    "PIR_ZERO_REMAINS_BLOCKED",
                    "PIR_MSTAR_BZERO_SOURCE_ROWS_STAGED_NONCLAIM",
                ]
            ),
            "required 1642 decisions are recorded",
        ),
        (
            "VAL1642_9_claim_gates_closed",
            all(row["status"] == "BLOCKED" for row in claim_gates),
            "all 1642 claim gates remain blocked",
        ),
        (
            "VAL1642_10_next_target_selected",
            next_targets[0]["next_target"] == "1643-Y5-R2FR-PiR-Mstar-source-acquisition-and-current-PPN-bound-runner.md",
            "next target selects PiR/Mstar source acquisition and current PPN bound runner",
        ),
        (
            "VAL1642_11_csv_parse",
            all(len(csv_rows(path)) > 0 for path in GENERATED),
            "all generated 1642 CSVs parse",
        ),
        (
            "VAL1642_12_nonclaim_flags",
            all_claim_flags_false(CLAIM_CHECKED),
            "all 1642 generated rows remain nonclaim/no-score",
        ),
        (
            "VAL1642_13_branch_copies",
            all((QUARANTINE / path.name).exists() and (BRANCH_RESIDUALS / path.name).exists() for path in GENERATED),
            "branch/quarantine copies exist",
        ),
        (
            "VAL1642_14_queue_copies",
            all(
                path.exists()
                for path in [
                    QUEUE / "JR1642_MINIMAL_BOUNDARY_VARIATION_ATTEMPT_NONCLAIM.csv",
                    QUEUE / "JR1642_PIR_MSTAR_SOURCE_FILL_ROWS_NONCLAIM.csv",
                    QUEUE / "JR1642_NEXT_TARGET_NONCLAIM.csv",
                ]
            ),
            "acquisition queue nonclaim copies exist",
        ),
        (
            "VAL1642_15_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
        ),
        (
            "VAL1642_16_formalization_untouched",
            not any(FORMALIZATION.rglob("*1642*")) if FORMALIZATION.exists() else True,
            "no 1642 outputs found under formalization-workbench",
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
            "check_id": "VAL1642_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1642 minimal boundary variation clause or PiR/Mstar source fill validation",
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
    attempt = csv_rows(MINIMAL_ATTEMPT)
    gates = csv_rows(EXACTNESS_GATES)
    fill = csv_rows(SOURCE_FILL)
    rules = csv_rows(PPN_RULE)
    decisions = csv_rows(DECISION)
    claim_gates = csv_rows(CLAIM_GATE)
    next_targets = csv_rows(NEXT_TARGET)
    validation = csv_rows(VALIDATION)

    content = f"""# 1642 - Minimal Boundary Variation Clause Or Pi_R Mstar Source Fill

**Private status:** nonclaim checkpoint. No `Pi_R=0`, `Q_R=0`, local-GR, PPN, Newton, orbital, WEP, clock, EM, or R10 pass is claimed.

## Verdict

The minimal exact-boundary route is now precise:

```text
i_vR Theta_matter + delta_vR B_matter = d_boundary C_R
integral_linked_boundary d_boundary C_R = 0
=> Pi_R_boundary_abs = 0
=> Pi_R = 0
=> Q_R = 0
=> q_R = 0
=> Delta gamma = 0
```

But 1642 does **not** prove it. The corpus has conditional exact/proper boundary machinery, yet it does not parent-sign the primitive `C_R`, the compact linked-boundary class, corner/reference silence, projector orthogonality, or same-frame source mass. Exactness is therefore useful mathematics, not evidence by itself.

## Source Register

{markdown_table(source_rows_data, ["source_id", "path", "path_exists", "needles_found", "role"])}

## Minimal Boundary Variation Attempt

{markdown_table(attempt, ["attempt_id", "clause", "status", "would_imply", "missing_or_conditional"])}

## Exact Boundary Zero Gates

{markdown_table(gates, ["gate_id", "required_gate", "current_status", "why_needed", "repair"])}

## Source Fill Rows

{markdown_table(fill, ["row_id", "quantity", "formula_role", "current_value", "status"])}

## Normalized PPN Score Rule

{markdown_table(rules, ["rule_id", "rule", "status", "allowed_to_score", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Claim Gates

{markdown_table(claim_gates, ["gate_id", "claim", "status", "blocker"])}

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
        MINIMAL_ATTEMPT: minimal_attempt_rows(),
        EXACTNESS_GATES: exactness_gate_rows(),
        SOURCE_FILL: source_fill_rows(),
        PPN_RULE: ppn_rule_rows(),
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
