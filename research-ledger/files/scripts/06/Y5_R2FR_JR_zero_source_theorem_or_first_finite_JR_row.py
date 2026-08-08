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
QUARANTINE = MICROSCOPE / "quarantine" / "1627"
INPUT_1627 = QUARANTINE / "input"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1627-Y5-R2FR-JR-zero-source-theorem-or-first-finite-JR-row.md"

SOURCE_FILES = {
    "1626_doc": ROOT / "1626-Y5-R2FR-finite-ZR-live-source-row-validator-and-first-prior-hunt.md",
    "1626_validation": OUT / "P8_Y5_BRR545_1626_VALIDATION.csv",
    "1626_next": OUT / "P8_Y5_PARENT_QLOC_1626_NEXT_TARGET.csv",
    "1626_blocker": OUT / "P8_Y5_PARENT_QLOC_1626_BLOCKER_LEDGER.csv",
    "1626_hunt": OUT / "P8_Y5_PARENT_QLOC_1626_CORPUS_SYMBOL_HUNT.csv",
    "1625_runner_gates": OUT / "P8_Y5_PARENT_QLOC_1625_RUNNER_REFUSAL_GATES.csv",
    "04_vacuum_contract": ROOT / "04-vacuum-reciprocity-action-contract.md",
    "05_reciprocity_attempt": ROOT / "05-reciprocity-theorem-attempt.md",
    "06_source_neutrality": ROOT / "06-reciprocal-charge-source-neutrality.md",
    "07_constraint": ROOT / "07-nonpropagating-reciprocity-constraint.md",
}

NEEDLES = {
    "1626_doc": ["J_R_ZERO_OR_FINITE_SOURCE_ROW_IS_BEST_NEXT_TARGET", "VAL1626_OVERALL"],
    "1626_validation": ["VAL1626_OVERALL", "PASS"],
    "1626_next": ["1627-Y5-R2FR-JR-zero-source-theorem-or-first-finite-JR-row.md", "J_R=0"],
    "1626_blocker": ["BLK1626_2_JR", "J_R_EQUATION_FOUND_BUT_NOT_PARENT_SIGNED"],
    "1626_hunt": ["J_R", "THEORY_EQUATION_NOT_PARENT_SIGNED_SOURCE_ROW"],
    "1625_runner_gates": ["PLACEHOLDER_MARKER_PRESENT", "LOCAL_GR_CLAIM_BLOCKED"],
    "04_vacuum_contract": ["d/dr [ W(r,L,fields) dR_AB/dr ] = J_R", "J_R = 0 in local vacuum"],
    "05_reciprocity_attempt": ["S_R = integral dr [0.5 W(r) (R_AB')^2 + J_R R_AB]", "Q_R = integral J_R dr = 0"],
    "06_source_neutrality": ["Q_R = -Pi_R", "Pi_R = 0 -> Q_R = 0 -> R_AB = 0 -> AB = 1"],
    "07_constraint": ["no R_AB kinetic term", "constraint parent origin"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1627_SOURCE_REGISTER.csv"
JR_THEOREM_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1627_JR_ZERO_THEOREM_AUDIT.csv"
MATTER_DESCENT_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1627_MATTER_DESCENT_PREMISE_AUDIT.csv"
FINITE_JR_ROW = OUT / "P8_Y5_PARENT_QLOC_1627_FIRST_FINITE_JR_ROW_CONTRACT_NONCLAIM.csv"
JR_ARENA_PROJECTIONS = OUT / "P8_Y5_PARENT_QLOC_1627_JR_ARENA_PROJECTION_REQUIREMENTS.csv"
BLOCKER_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1627_BLOCKER_LEDGER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1627_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1627_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1627_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1627_VALIDATION.csv"

COPY_TARGETS = {
    JR_THEOREM_AUDIT: [
        QUARANTINE / "JR_ZERO_THEOREM_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_JR_zero_theorem_audit_nonclaim_1627.csv",
    ],
    MATTER_DESCENT_AUDIT: [
        QUARANTINE / "MATTER_DESCENT_PREMISE_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_matter_descent_premise_audit_nonclaim_1627.csv",
    ],
    FINITE_JR_ROW: [
        QUARANTINE / "FIRST_FINITE_JR_ROW_CONTRACT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_first_finite_JR_row_contract_nonclaim_1627.csv",
        QUEUE / "JR1627_FIRST_FINITE_SOURCE_ROW_CONTRACT_NONCLAIM.csv",
    ],
    JR_ARENA_PROJECTIONS: [
        QUARANTINE / "JR_ARENA_PROJECTION_REQUIREMENTS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_JR_arena_projection_requirements_nonclaim_1627.csv",
    ],
    BLOCKER_LEDGER: [
        QUARANTINE / "BLOCKER_LEDGER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_JR_blocker_ledger_nonclaim_1627.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE_CLOSED.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_closed_1627.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_1627.csv",
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
    for directory in [OUT, INPUT_1627, BRANCH_RESIDUALS, QUEUE]:
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
    for field in ["score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed", "accepted_for_scoring"]:
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
            "role": "1627 J_R zero theorem or finite source row provenance",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for source_id, path in SOURCE_FILES.items()
    ]


def jr_theorem_audit_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "JR1627_0_parent_variation_shape",
            "R_AB parent variation",
            "d/dr[W dR_AB/dr] = J_R",
            "04_vacuum_contract;05_reciprocity_attempt",
            "TOY_VARIATION_AVAILABLE_NOT_PARENT_ACTION",
            "gives the right equation form, but parent action owner/object language remains unsigned",
        ),
        (
            "JR1627_1_local_vacuum_silence",
            "local vacuum source silence",
            "J_R = 0 in local vacuum",
            "04_vacuum_contract;05_reciprocity_attempt",
            "STATED_NOT_PARENT_DERIVED",
            "this is the desired theorem statement, not yet a consequence of matter descent",
        ),
        (
            "JR1627_2_reciprocal_charge",
            "conserved reciprocal charge",
            "J_R=0 -> W R_AB' = Q_R",
            "05_reciprocity_attempt;06_source_neutrality",
            "DERIVED_CONDITIONAL_OBSTRUCTION",
            "J_R=0 alone leaves Q_R unless source/boundary neutrality also closes",
        ),
        (
            "JR1627_3_source_integral",
            "source matching",
            "Q_R = integral J_R dr = 0",
            "05_reciprocity_attempt",
            "SOURCE_MATCHING_REQUIRED_NOT_PROVED",
            "needs matter/source neutrality, not just exterior vacuum",
        ),
        (
            "JR1627_4_boundary_momentum",
            "boundary reciprocal charge",
            "Q_R = -Pi_R and Pi_R=0 -> Q_R=0",
            "06_source_neutrality",
            "BOUNDARY_NEUTRALITY_CONDITIONAL",
            "clean route if Pi_R=0 is parent-signed; current notes do not sign it",
        ),
        (
            "JR1627_5_nonpropagating_escape",
            "constraint route",
            "no R_AB kinetic term -> no Q_R hair mode",
            "07_constraint",
            "CLEAN_ALTERNATIVE_PARENT_ORIGIN_OPEN",
            "would avoid finite J_R, but parent origin of lambda_R R_AB remains open",
        ),
        (
            "JR1627_6_verdict",
            "J_R zero theorem",
            "J_R = 0 from parent matter descent",
            "04-07 plus 1626 blocker",
            "JR_ZERO_NOT_DERIVED_CURRENT_CORPUS",
            "stage finite J_R row contract while next target attacks matter descent/source owner",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "claim_piece": claim_piece,
            "mathematical_statement": statement,
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
        for audit_id, claim_piece, statement, anchors, status, effect in rows
    ]


def matter_descent_audit_rows() -> list[dict[str, Any]]:
    premises = [
        (
            "MD1627_0_matter_descent",
            "S_matter descends through quotient variables and has no independent R_AB representative coupling",
            "would set delta S_matter/delta R_AB = 0",
            "MISSING_PARENT_MATTER_DESCENT_CERTIFICATE",
        ),
        (
            "MD1627_1_source_support",
            "material source support couples to clock/load variables only, not reciprocal strain",
            "would justify source reciprocal neutrality",
            "MISSING_SOURCE_SUPPORT_OWNER",
        ),
        (
            "MD1627_2_boundary_momentum",
            "Pi_R = 0 at material/load boundary",
            "would kill Q_R via Q_R=-Pi_R",
            "MISSING_BOUNDARY_MOMENTUM_ZERO",
        ),
        (
            "MD1627_3_no_hidden_stress",
            "no anisotropic/radial routing stress contributes to J_R",
            "would block hidden fitted reciprocal source",
            "MISSING_NO_HIDDEN_RECIPROCAL_STRESS",
        ),
        (
            "MD1627_4_measure_coframe",
            "measure/coframe descent does not reintroduce R_AB dependence",
            "would protect J_R=0 after changing variables",
            "MISSING_MEASURE_COFRAME_DESCENT",
        ),
        (
            "MD1627_5_boundary_flux",
            "finite exterior reciprocal flux has natural no-flux or source-neutral boundary condition",
            "would stop finite Q_R hair",
            "MISSING_NO_FLUX_BOUNDARY_CERTIFICATE",
        ),
        (
            "MD1627_6_same_frame",
            "source, clock, and readout use the same observed frame in the local limit",
            "would stop frame mismatch from acting as J_R",
            "MISSING_SAME_FRAME_SOURCE_READOUT_LOCK",
        ),
        (
            "MD1627_7_verdict",
            "all matter-descent premises are parent-signed",
            "would promote J_R=0 theorem candidate",
            "MATTER_DESCENT_PREMISES_UNSIGNED",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "premise_id": premise_id,
            "premise": premise,
            "why_needed": why_needed,
            "status": status,
            "current_evidence": "conditional route in 04-07; not a parent-signed certificate",
            "parent_signed": False,
            "accepted_as_zero": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for premise_id, premise, why_needed, status in premises
    ]


def finite_jr_row_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "row_id": "FJR1627_0_first_finite_JR_contract",
            "row_type": "finite_source_current_contract_not_live",
            "coefficient_symbol": "J_R",
            "evidence_type": "MISSING_PARENT_SIGNED_ZERO_OR_NUMERIC_SOURCE_CURRENT",
            "coefficient_value": "MISSING_NUMERIC_VALUE_OR_ZERO_CERTIFICATE",
            "prior_lower": "MISSING_PRIOR_LOWER",
            "prior_upper": "MISSING_PRIOR_UPPER",
            "coefficient_units": "MISSING_SOURCE_CURRENT_UNITS",
            "normalization_convention": "MISSING_RAB_EQUATION_NORMALIZATION",
            "parent_action_block": "MISSING_PARENT_MATTER_DESCENT_OR_SOURCE_ACTION_BLOCK",
            "source_path": "MISSING_LOCAL_SOURCE_PATH",
            "source_anchor": "MISSING_SOURCE_ANCHOR",
            "arena_projection": "MISSING_R10_PPN_CLOCK_OR_ORBITAL_PROJECTION",
            "required_live_columns": "coefficient_symbol;coefficient_value;coefficient_units;normalization_convention;parent_action_block;source_path;source_anchor;arena_projection;evidence_type",
            "rejection_reason": "template/contract only; contains MISSING markers and cannot be scored",
            "current_status": "FINITE_JR_ROW_CONTRACT_STAGED_NONCLAIM",
            "accepted_as_live_row": False,
            "numeric_value_present": False,
            "source_backed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def jr_arena_projection_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "JAP1627_0_tau_R10",
            "tau_R10[J_R]",
            "map finite J_R/Q_R hair to alpha(lambda)",
            "need source profile, range law, q_Rhat normalization, and alpha(lambda) comparator",
            "MISSING_R10_JR_PROJECTION",
        ),
        (
            "JAP1627_1_tau_PPN",
            "tau_PPN[J_R]",
            "map R_AB = q_R L or equivalent residual to gamma/beta/preferred-frame vector",
            "need weak-field metric response and PPN residual vector",
            "MISSING_PPN_JR_PROJECTION",
        ),
        (
            "JAP1627_2_tau_clock",
            "tau_clock[J_R]",
            "map matter/source reciprocal coupling to clock/readout drift",
            "need clock sensitivity and same-frame source/readout rule",
            "MISSING_CLOCK_JR_PROJECTION",
        ),
        (
            "JAP1627_3_tau_orbital",
            "tau_orbital[J_R]",
            "map source reciprocal current to orbital/source-support residuals",
            "need orbital response kernel and source boundary condition",
            "MISSING_ORBITAL_JR_PROJECTION",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "projection_id": projection_id,
            "projection_symbol": symbol,
            "observable_map": observable_map,
            "required_inputs": required_inputs,
            "status": status,
            "accepted_as_live_row": False,
            "numeric_value_present": False,
            "source_backed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for projection_id, symbol, observable_map, required_inputs, status in rows
    ]


def blocker_rows() -> list[dict[str, Any]]:
    blockers = [
        (
            "BLK1627_0_JR_zero",
            "J_R=0 theorem",
            "JR_ZERO_NOT_DERIVED_CURRENT_CORPUS",
            "matter descent/source neutrality is stated conditionally but not parent-signed",
            "attack matter descent/source owner next",
        ),
        (
            "BLK1627_1_PiR_zero",
            "Pi_R=0 boundary momentum",
            "MISSING_BOUNDARY_MOMENTUM_ZERO",
            "Q_R=-Pi_R route needs parent boundary condition or finite flux bound",
            "derive natural boundary condition or create finite boundary/source row",
        ),
        (
            "BLK1627_2_finite_JR",
            "finite J_R live row",
            "FINITE_JR_ROW_CONTRACT_ONLY",
            "contract exists but no numeric value, units, normalization, source path, or source anchor exists",
            "use contract only after source evidence exists",
        ),
        (
            "BLK1627_3_arena",
            "J_R arena projections",
            "MISSING_JR_ARENA_PROJECTIONS",
            "tau_R10/tau_PPN/tau_clock/tau_orbital maps are requirements only",
            "defer scoring until projection kernels exist",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "blocker_id": blocker_id,
            "target": target,
            "status": status,
            "missing_for_claim": missing,
            "next_action": next_action,
            "accepted_as_live_row": False,
            "numeric_value_present": False,
            "source_backed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for blocker_id, target, status, missing, next_action in blockers
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    claims = [
        ("CG1627_0_JR_zero", "J_R=0 from parent matter descent", "BLOCKED", "matter descent/source neutrality premises are unsigned"),
        ("CG1627_1_QR_zero", "Q_R=0 reciprocal charge", "BLOCKED", "Pi_R=0/source matching not parent-derived"),
        ("CG1627_2_finite_JR", "finite J_R row claim-ready", "BLOCKED", "row is a MISSING-marker contract only"),
        ("CG1627_3_R10_PPN_clock_orbital", "J_R arena tests", "BLOCKED", "projection kernels missing"),
        ("CG1627_4_local_GR", "derived local GR/Newton recovery", "BLOCKED", "reciprocal source coupling remains open"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "accepted_as_live_row": False,
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
            "decision_id": "DEC1627_0_theorem",
            "decision": "JR_ZERO_THEOREM_NOT_PARENT_SIGNED",
            "reason": "04-07 derive a clean conditional route, but not parent matter descent/source neutrality",
            "next_action": "do not promote J_R=0 yet",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1627_1_contract",
            "decision": "FIRST_FINITE_JR_ROW_CONTRACT_STAGED_NONCLAIM",
            "reason": "if J_R is finite, it now has an explicit required row shape and rejection reason",
            "next_action": "fill only after source evidence supplies value/zero certificate, units, normalization, and arena map",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1627_2_best_next",
            "decision": "NEXT_1628_MATTER_DESCENT_SOURCE_OWNER_OR_JR_BOUND_ACQUISITION",
            "reason": "matter descent/source owner is the missing parent signature behind J_R=0",
            "next_action": "try source-owner theorem before numeric acquisition",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1628-Y5-R2FR-matter-descent-source-owner-certificate-or-JR-bound-acquisition.md",
            "script": "scripts/Y5_R2FR_matter_descent_source_owner_certificate_or_JR_bound_acquisition.py",
            "objective": "try to prove the parent matter action/source owner descends without independent R_AB coupling so J_R=0 and Pi_R=0 follow; if not, convert the 1627 finite J_R contract into an acquisition ledger for numeric/source-backed bounds",
            "success_condition": "either a parent-signed source-owner certificate closes the J_R/Pi_R zero route as nonclaim, or a finite J_R acquisition ledger identifies exact missing source inputs without scoring",
            "do_not": "do not use local-vacuum prose as proof, do not assume Pi_R=0, do not score finite J_R templates, do not claim local GR/Newton/R10/PPN/clock/orbital pass",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def generated_paths() -> list[Path]:
    return [
        SOURCE_REGISTER,
        JR_THEOREM_AUDIT,
        MATTER_DESCENT_AUDIT,
        FINITE_JR_ROW,
        JR_ARENA_PROJECTIONS,
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
            shutil.copyfile(source, INPUT_1627 / f"{source_id}{source.suffix}")


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows() -> list[dict[str, Any]]:
    paths = generated_paths()
    theorem_rows = read_csv(JR_THEOREM_AUDIT)
    matter_rows = read_csv(MATTER_DESCENT_AUDIT)
    finite_rows = read_csv(FINITE_JR_ROW)
    arena_rows = read_csv(JR_ARENA_PROJECTIONS)
    blocker_data = read_csv(BLOCKER_LEDGER)
    claim_rows = read_csv(CLAIM_GATE)
    decision_text = file_text(DECISION)
    next_text = file_text(NEXT_TARGET)
    all_rows: list[dict[str, Any]] = []
    for path in paths:
        all_rows.extend(read_csv(path))

    source_ok = all(path.exists() for path in SOURCE_FILES.values())
    needles_ok = all(all_needles_found(source_id) for source_id in SOURCE_FILES)
    theorem_blocked = any(row["audit_id"] == "JR1627_6_verdict" and row["status"] == "JR_ZERO_NOT_DERIVED_CURRENT_CORPUS" for row in theorem_rows)
    matter_unsigned = all(row["parent_signed"] == "False" and row["accepted_as_zero"] == "False" for row in matter_rows)
    finite_contract = (
        len(finite_rows) == 1
        and finite_rows[0]["current_status"] == "FINITE_JR_ROW_CONTRACT_STAGED_NONCLAIM"
        and "MISSING" in " ".join(finite_rows[0].values())
    )
    arena_missing = all(row["status"].startswith("MISSING_") for row in arena_rows)
    blockers_cover = {row["target"] for row in blocker_data} == {"J_R=0 theorem", "Pi_R=0 boundary momentum", "finite J_R live row", "J_R arena projections"}
    claim_closed = all(row["status"] == "BLOCKED" and not row_has_true_claim_flag(row) for row in claim_rows)
    nonclaim_ok = all(not row_has_true_claim_flag(row) for row in all_rows)
    next_selected = "1628-Y5-R2FR-matter-descent-source-owner-certificate-or-JR-bound-acquisition.md" in next_text
    decision_next = "NEXT_1628_MATTER_DESCENT_SOURCE_OWNER_OR_JR_BOUND_ACQUISITION" in decision_text
    branch_copies = all(target.exists() for targets in COPY_TARGETS.values() for target in targets)
    csv_ok = all(csv_parses(path) for path in paths)
    pycache_absent = not (Path(__file__).resolve().parent / "__pycache__").exists()
    formalization_clean = not any((FORMALIZATION / path.name).exists() for path in [DOC, *paths]) if FORMALIZATION.exists() else True

    checks = [
        ("VAL1627_0_sources_exist", source_ok, "all cited 1627 local source paths exist"),
        ("VAL1627_1_needles_found", needles_ok, "all required 1627 source needles found"),
        ("VAL1627_2_theorem_blocked", theorem_blocked, "J_R zero theorem remains not derived"),
        ("VAL1627_3_matter_unsigned", matter_unsigned, "matter descent premises remain unsigned"),
        ("VAL1627_4_finite_contract", finite_contract, "finite J_R source row contract staged as nonclaim MISSING-marker row"),
        ("VAL1627_5_arena_missing", arena_missing, "J_R arena projections remain missing"),
        ("VAL1627_6_blocker_coverage", blockers_cover, "blocker ledger covers J_R zero, Pi_R, finite J_R, and arena maps"),
        ("VAL1627_7_claim_gates_closed", claim_closed, "all claim gates remain blocked"),
        ("VAL1627_8_nonclaim_flags", nonclaim_ok, "all generated 1627 rows remain nonclaim/non-score-ready"),
        ("VAL1627_9_decision_next", decision_next, "decision selects matter descent/source owner next"),
        ("VAL1627_10_next_target_selected", next_selected, "next target selected"),
        ("VAL1627_11_branch_copies", branch_copies, "branch/quarantine/acquisition queue nonclaim copies exist"),
        ("VAL1627_12_csv_parse", csv_ok, "all generated 1627 CSVs parse"),
        ("VAL1627_13_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL1627_14_formalization_untouched", formalization_clean, "no 1627 outputs found under formalization-workbench"),
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
            "check_id": "VAL1627_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1627 J_R zero theorem or first finite J_R row validation",
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
    theorem_rows = read_csv(JR_THEOREM_AUDIT)
    matter_rows = read_csv(MATTER_DESCENT_AUDIT)
    finite_rows = read_csv(FINITE_JR_ROW)
    arena_rows = read_csv(JR_ARENA_PROJECTIONS)
    blockers = read_csv(BLOCKER_LEDGER)
    claims = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_target = read_csv(NEXT_TARGET)
    validation = read_csv(VALIDATION)

    content = f"""# 1627 — `J_R` Zero Source Theorem Or First Finite `J_R` Row

## Status

Private checkpoint. No local-GR/Newton, R10, PPN, clock, orbital, or finite-source claim is made.

## Outcome

The `J_R=0` route is mathematically clean but still conditional. The 04-07 notes give the desired equation, the conserved `Q_R` obstruction, and the boundary-neutrality route `Q_R=-Pi_R`; they do **not** parent-sign matter descent, `Pi_R=0`, or absence of hidden reciprocal stress. So `J_R=0` is not promoted. A first finite `J_R` row contract is staged as nonclaim fallback.

## Source Register

{markdown_table(source_rows, ["source_id", "source_path", "exists", "needles_found"])}

## `J_R` Theorem Audit

{markdown_table(theorem_rows, ["audit_id", "claim_piece", "mathematical_statement", "status", "effect"])}

## Matter Descent Premise Audit

{markdown_table(matter_rows, ["premise_id", "premise", "status", "why_needed"])}

## First Finite `J_R` Row Contract

{markdown_table(finite_rows, ["row_id", "coefficient_symbol", "current_status", "rejection_reason"])}

## `J_R` Arena Projection Requirements

{markdown_table(arena_rows, ["projection_id", "projection_symbol", "observable_map", "status"])}

## Blocker Ledger

{markdown_table(blockers, ["blocker_id", "target", "status", "missing_for_claim", "next_action"])}

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
        JR_THEOREM_AUDIT: jr_theorem_audit_rows(),
        MATTER_DESCENT_AUDIT: matter_descent_audit_rows(),
        FINITE_JR_ROW: finite_jr_row_contract_rows(),
        JR_ARENA_PROJECTIONS: jr_arena_projection_rows(),
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
