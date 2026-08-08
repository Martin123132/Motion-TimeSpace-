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
QUARANTINE = MICROSCOPE / "quarantine" / "1695"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_SOURCE = MICROSCOPE / "branch_locked_wep" / "source"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "1695-Y5-R2FR-no-source-only-slot-theorem-or-tau-WEP-projection-current-branch.md"

SOURCE_FILES = {
    "1694_doc": ROOT / "1694-Y5-R2FR-action-weight-exclusion-or-first-source-backed-beta-current-branch.md",
    "1694_validation": OUT / "P8_Y5_BRR545_1694_VALIDATION.csv",
    "1694_next": OUT / "P8_Y5_PARENT_QLOC_1694_NEXT_TARGET.csv",
    "1596_doc": ROOT / "1596-Y5-R2FR-tau-WEP-source-projection-or-action-measure-owner-last-gate.md",
    "1596_validation": OUT / "P8_Y5_BRR545_1596_VALIDATION.csv",
    "1596_tau_law": OUT / "P8_Y5_PARENT_QLOC_1596_TAU_WEP_CONTRACTION_LAW.csv",
    "1596_tau_factors": OUT / "P8_Y5_PARENT_QLOC_1596_TAU_FACTOR_AUDIT.csv",
    "1596_tau_acquisition": OUT / "P8_Y5_PARENT_QLOC_1596_TAU_SOURCE_ACQUISITION_ROWS.csv",
    "1596_action_last_gate": OUT / "P8_Y5_PARENT_QLOC_1596_ACTION_MEASURE_OWNER_LAST_GATE.csv",
    "1596_next": OUT / "P8_Y5_PARENT_QLOC_1596_NEXT_TARGET.csv",
    "1065_parent_grammar": OUT / "P8_Y5_R10_1065_PARENT_GRAMMAR_AUDIT.csv",
    "1065_zero_clauses": OUT / "P8_Y5_R10_1065_WA_THEOREM_ZERO_CLAUSES.csv",
    "1066_typing": OUT / "P8_Y5_R10_1066_OBJECT_LANGUAGE_TYPING_AUDIT.csv",
    "1066_field_measure": OUT / "P8_Y5_R10_1066_FIELD_MEASURE_QUANTUM_NORMALIZATION_AUDIT.csv",
    "1066_decision": OUT / "P8_Y5_R10_1066_DECISION_LEDGER.csv",
    "1067_tau_schema": OUT / "P8_Y5_R10_1067_TAU_WEP_ACQUISITION_SCHEMA.csv",
    "1067_decision": OUT / "P8_Y5_R10_1067_DECISION_LEDGER.csv",
    "1476_source_label": MICROSCOPE / "quarantine" / "1476" / "SOURCE_LABEL_FORGETTING_PROOF_ATTEMPT.csv",
    "1479_no_source_typing": MICROSCOPE / "quarantine" / "1479" / "NO_SOURCE_ONLY_ACTION_PREFACTOR_TYPING_THEOREM_ATTEMPT_NONCLAIM.csv",
    "1482_wep_parser_status": BRANCH_SOURCE / "P_WEP_R_source_status_1482.csv",
    "local_bound_claims": ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv",
}

NEEDLES = {
    "1694_doc": ["NEXT1694_0_primary", "no-source-only-slot"],
    "1694_validation": ["VAL1694_OVERALL", "PASS"],
    "1694_next": ["NEXT1694_0_primary", "no-source-only-slot"],
    "1596_doc": ["tau_WEP", "VAL1596_OVERALL"],
    "1596_validation": ["VAL1596_OVERALL", "PASS"],
    "1596_tau_law": ["TCL1596_1_product_bound", "2.8e-15"],
    "1596_tau_factors": ["TFA1596_0_source_worldtube", "TFA1596_6_parent_coupling_slot"],
    "1596_tau_acquisition": ["TSA1596_0_readout_matrix", "TSA1596_3_tau_min"],
    "1596_action_last_gate": ["AMG1596_3_last_gate_verdict", "ACTION_MEASURE_OWNER_LAST_GATE_NOT_CLOSED"],
    "1596_next": ["1597-Y5-R2FR-tau-lower-bound-or-coupling-zero-proof.md", "tau_min>0"],
    "1065_parent_grammar": ["PGG1065_1_no_inert_species_scalar", "CONDITIONAL_GRAMMAR_NOT_PARENT_SIGNED"],
    "1065_zero_clauses": ["WTZ1065_4_verdict", "THEOREM_ZERO_NOT_PARENT_SIGNED"],
    "1066_typing": ["OLT1066_4_inert_source_scalar", "conditional_not_parent_derived"],
    "1066_field_measure": ["FMQ1066_4_verdict", "NOT_PARENT_SIGNED"],
    "1066_decision": ["DEC1066_2_best_next", "tau_WEP local projection"],
    "1067_tau_schema": ["TAQ1067_1_tau_numeric_option", "TAQ1067_4_refusal_rule"],
    "1067_decision": ["DEC1067_1_tau_status", "tau_WEP must become a real projection functional"],
    "1476_source_label": ["SLF1476_4_verdict", "NOT_PARENT_DERIVED_EMIT_DELTA_W_INPUT_ROW"],
    "1479_no_source_typing": ["NST1479_4_verdict", "PROOF_NOT_CLOSED_BOUND_PACK_REQUIRED"],
    "1482_wep_parser_status": ["ACCEPT1482_5_overall_parser_permission", "BLOCKED"],
    "local_bound_claims": ["R1_WEP_source_charge", "2.8e-15"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1695_SOURCE_REGISTER.csv"
NO_SLOT_THEOREM = OUT / "P8_Y5_PARENT_QLOC_1695_NO_SOURCE_ONLY_SLOT_THEOREM_AUDIT.csv"
TAU_PROJECTION = OUT / "P8_Y5_PARENT_QLOC_1695_TAU_WEP_PROJECTION_READINESS.csv"
PRODUCT_BOUND = OUT / "P8_Y5_PARENT_QLOC_1695_PRODUCT_BOUND_INTERPRETATION.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1695_RUNNER_REFUSAL.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1695_NEXT_TARGET.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1695_CLAIM_GATE.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1695_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    NO_SLOT_THEOREM,
    TAU_PROJECTION,
    PRODUCT_BOUND,
    RUNNER,
    NEXT_TARGET,
    CLAIM_GATE,
]

CLAIM_CHECKED = [
    NO_SLOT_THEOREM,
    TAU_PROJECTION,
    PRODUCT_BOUND,
    RUNNER,
    NEXT_TARGET,
    CLAIM_GATE,
]

COPY_TARGETS = {
    NO_SLOT_THEOREM: [
        QUARANTINE / "NO_SOURCE_ONLY_SLOT_THEOREM_AUDIT.csv",
        BRANCH_RESIDUALS / "R2FR_no_source_only_slot_theorem_audit_1695.csv",
        QUEUE / "JR1695_NO_SOURCE_ONLY_SLOT_THEOREM_AUDIT.csv",
    ],
    TAU_PROJECTION: [
        QUARANTINE / "TAU_WEP_PROJECTION_READINESS.csv",
        BRANCH_RESIDUALS / "R2FR_tau_WEP_projection_readiness_1695.csv",
        QUEUE / "JR1695_TAU_WEP_PROJECTION_READINESS.csv",
    ],
    PRODUCT_BOUND: [
        QUARANTINE / "PRODUCT_BOUND_INTERPRETATION.csv",
        BRANCH_RESIDUALS / "R2FR_product_bound_interpretation_1695.csv",
        QUEUE / "JR1695_PRODUCT_BOUND_INTERPRETATION.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_1695.csv",
        QUEUE / "JR1695_NEXT_TARGET.csv",
    ],
}


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def bool_cell(value: object) -> bool:
    return str(value).strip().lower() == "true"


def list_cell(values: list[object] | tuple[object, ...]) -> str:
    return ";".join(str(value) for value in values)


def markdown_table(rows: list[dict[str, object]], headers: list[str]) -> str:
    if not rows:
        return "_No rows._"
    table = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        table.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(table)


def source_register_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for key, path in SOURCE_FILES.items():
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles = NEEDLES[key]
        needles_present = exists and all(needle in text for needle in needles)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_key": key,
                "source_path": str(path),
                "exists": exists,
                "needles_present": needles_present,
                "required_needles": list_cell(needles),
                "use_in_1695": "no-source-only-slot theorem audit and tau_WEP projection readiness",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def no_slot_theorem_rows() -> list[dict[str, object]]:
    rows = [
        (
            "NST1695_0_target",
            "no source-only action/source prefactor slot",
            "Hom_parent(species_label or hidden_marker, R_+^active-source-prefactor) is empty or common-constant only",
            "EXACT_TARGET",
            "Delta_w_A theorem-zero modulo common calibration",
            "parent object language and admissible coefficient targets",
            "not_signed",
        ),
        (
            "NST1695_1_admissible_arguments",
            "typed parent matter arguments",
            "Arg(S_matter) contains observed geometry, dynamical matter fields, gauge/current data, representation constants and universal constants",
            "EXACT_CONDITIONAL_META_THEOREM",
            "inert w_A has no legal slot if this grammar is parent-owned",
            "derive grammar from MTS quotient/category primitives",
            "not_signed",
        ),
        (
            "NST1695_2_inert_source_scalar",
            "reject w_A as inert source scalar",
            "w_A changes T_source but has no independent nongravitational observable, representation label or geometry role",
            "REJECTED_BY_CANDIDATE_TYPING",
            "would kill relative source/action weights",
            "typing theorem must be parent-derived, not adopted",
            "not_signed",
        ),
        (
            "NST1695_3_same_action_no_go",
            "same action/covariance/additivity are insufficient",
            "S_matter=sum_A w_A S_A is still a same covariant additive action but gives T_source=sum_A w_A T_A",
            "NO_GO_GUARD",
            "prevents fake proof by classical EOM or Hilbert-source words alone",
            "no shortcut",
            "guard_active",
        ),
        (
            "NST1695_4_hidden_source_hom",
            "no hidden/source marker Hom into coefficient target",
            "hidden invariant or species label cannot feed w_A, kappa_A, source readout, mass, clock or current coefficients",
            "POWERFUL_IF_SIGNED_NOT_REDUCED",
            "would stop source-only reentry under another name",
            "hidden-visible Hom exclusion and readout/no-spurion closure",
            "not_signed",
        ),
        (
            "NST1695_5_measure_current_owner",
            "single action-measure/current owner",
            "one hbar/action measure and one Hilbert/coframe current owner before variation",
            "COMMON_ROUTE_CLEAN_NOT_CLOSED",
            "would remove species-dependent action weights and Jacobians",
            "parent action-scale/measure theorem",
            "not_signed",
        ),
        (
            "NST1695_6_common_mode_guard",
            "common constant mode only",
            "w_A=w_common, constant and species-blind, is calibration; Delta_w_AB and beta_w,A are not calibration",
            "GUARD_ACTIVE",
            "measured-G absorption cannot hide relative or phi-dependent source weights",
            "keep finite rows unless theorem-zero",
            "guard_active",
        ),
        (
            "NST1695_7_verdict",
            "no-source-only-slot theorem status",
            "the theorem is exact as a typing/grammar condition but not derived from current parent MTS primitives",
            "NO_SOURCE_ONLY_SLOT_NOT_DERIVED_TAU_ROUTE_RETAINED",
            "do not claim Delta_w_A=0; keep tau/product finite branch",
            "parent object-language owner or tau_min source projection",
            "not_signed",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": theorem_id,
            "claim_piece": claim_piece,
            "formal_statement": statement,
            "status": status,
            "if_signed": if_signed,
            "missing_for_claim": missing,
            "parent_signature": signature,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for theorem_id, claim_piece, statement, status, if_signed, missing, signature in rows
    ]


def tau_projection_rows() -> list[dict[str, object]]:
    rows = [
        (
            "TAU1695_0_contraction_law",
            "eta_TiPt = Delta_w_TiPt * tau_WEP + higher order",
            "CONDITIONAL_LINEAR_CONTRACTION_DERIVED_NONCLAIM",
            "same branch, weak finite-source residual, no cancellation, no measured-G absorption",
            "source-backed product bound exists but not a prediction",
            "P8_Y5_PARENT_QLOC_1596_TAU_WEP_CONTRACTION_LAW.csv:TCL1596_0_linearized_observable",
            "false",
        ),
        (
            "TAU1695_1_readout_matrix",
            "P_WEP_K_CMSM_readout.csv",
            "OFFICIAL_ARRAYS_NOT_IMPORTED",
            "time, segments, masks, calibration flags, orbit/attitude convention and units",
            "tau_WEP cannot be numeric",
            "P8_Y5_PARENT_QLOC_1596_TAU_SOURCE_ACQUISITION_ROWS.csv:TSA1596_0_readout_matrix",
            "false",
        ),
        (
            "TAU1695_2_source_worldtube",
            "P_WEP_R_source_Earth_worldtube.csv",
            "MISSING_SOURCE_PROFILE_WEIGHTING",
            "Earth stress/source profile in observed local frame with kernel convention",
            "tau_WEP and source leg cannot be evaluated",
            "P8_Y5_PARENT_QLOC_1596_TAU_FACTOR_AUDIT.csv:TFA1596_0_source_worldtube",
            "false",
        ),
        (
            "TAU1695_3_material_tensor",
            "P_WEP_TiPt_material_response_tensor.csv",
            "MISSING_FULL_MATERIAL_TENSOR",
            "TA6V and PtRh10 response tensor in same source-weight convention",
            "Delta_w_TiPt material map incomplete",
            "P8_Y5_PARENT_QLOC_1596_TAU_FACTOR_AUDIT.csv:TFA1596_3_material_tensor",
            "false",
        ),
        (
            "TAU1695_4_product_convention",
            "eta product normalization",
            "NORMALIZATION_NOT_FILLED",
            "map source response x material response x readout kernel to reported eta",
            "tau_WEP=1 shortcut forbidden",
            "P8_Y5_PARENT_QLOC_1596_TAU_FACTOR_AUDIT.csv:TFA1596_5_product_convention",
            "false",
        ),
        (
            "TAU1695_5_parent_coupling_slot",
            "C_parent/action-measure owner",
            "MISSING_C_PARENT_IMPORT",
            "theorem-zero route or finite parent coefficient in the same branch",
            "finite branch cannot become local-GR derivation",
            "P8_Y5_PARENT_QLOC_1596_TAU_FACTOR_AUDIT.csv:TFA1596_6_parent_coupling_slot",
            "false",
        ),
        (
            "TAU1695_6_tau_min",
            "strictly positive tau lower bound",
            "DERIVATION_OR_SOURCE_NEEDED",
            "prove |tau_WEP| >= tau_min > 0 with source/readout paths and assumptions",
            "without tau_min the product anchor gives no finite Delta_w bound",
            "P8_Y5_PARENT_QLOC_1596_TAU_SOURCE_ACQUISITION_ROWS.csv:TSA1596_3_tau_min",
            "false",
        ),
        (
            "TAU1695_7_parser_status",
            "branch parser permission",
            "BLOCKED",
            "requires official arrays, source worldtube, product convention, C_parent, material tensor and branch rows",
            "no WEP score or tau evaluation",
            "P_WEP_R_source_status_1482.csv:ACCEPT1482_5_overall_parser_permission",
            "false",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "projection_id": projection_id,
            "object": obj,
            "current_status": status,
            "required_input": required,
            "effect": effect,
            "source_anchor": source,
            "tau_numeric": tau_numeric,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for projection_id, obj, status, required, effect, source, tau_numeric in rows
    ]


def product_bound_rows() -> list[dict[str, object]]:
    rows = [
        (
            "PBI1695_0_bound_anchor",
            "abs(Delta_w_TiPt * tau_WEP)",
            "<= 2.8e-15",
            "source-backed external bound anchor",
            "available",
            "source-intake/local_bounds/local_bound_claims.csv:R1_WEP_source_charge",
            "not an MTS prediction",
        ),
        (
            "PBI1695_1_delta_w_amplitude_law",
            "abs(Delta_w_TiPt)",
            "<= 2.8e-15/tau_min if |tau_WEP| >= tau_min > 0",
            "exact conditional amplitude law",
            "symbolic_only_tau_min_missing",
            "P8_Y5_PARENT_QLOC_1596_TAU_WEP_CONTRACTION_LAW.csv:TCL1596_2_delta_w_amplitude_law",
            "no numeric Delta_w bound yet",
        ),
        (
            "PBI1695_2_tau_null_escape",
            "tau_WEP",
            "if tau_WEP can vanish or be arbitrarily small, product bound gives no finite Delta_w bound",
            "no-shortcut theorem",
            "active",
            "P8_Y5_PARENT_QLOC_1596_TAU_WEP_CONTRACTION_LAW.csv:TCL1596_3_tau_null_escape",
            "must derive tau_min or theorem-zero Delta_w",
        ),
        (
            "PBI1695_3_zero_route",
            "Delta_w_TiPt=0",
            "requires parent-signed no-source-only-slot/common-measure theorem",
            "theorem-zero route",
            "not_parent_signed",
            "P8_Y5_R10_1065_WA_THEOREM_ZERO_CLAUSES.csv:WTZ1065_4_verdict",
            "no zero claim",
        ),
        (
            "PBI1695_4_verdict",
            "MICROSCOPE product bound",
            "kept as pressure data only",
            "nonclaim current branch status",
            "usable_as_external_bound_only",
            "P8_Y5_PARENT_QLOC_1694_SOURCE_BACKED_BETA_DELTAW_CURRENT_ROWS.csv:BDW1694_0_MICROSCOPE_Delta_w_tau_bound_anchor",
            "no local-GR/WEP/R10/PPN claim",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "bound_id": bound_id,
            "quantity": quantity,
            "statement": statement,
            "bound_type": bound_type,
            "current_status": status,
            "source_anchor": source,
            "interpretation": interpretation,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for bound_id, quantity, statement, bound_type, status, source, interpretation in rows
    ]


def runner_rows() -> list[dict[str, object]]:
    rows = [
        ("RUN1695_0_no_slot_zero", "claim no-source-only-slot theorem", "REJECT_THEOREM_ZERO_CLAIM", "typing theorem exact but parent object language is not derived"),
        ("RUN1695_1_delta_w_zero", "set Delta_w_TiPt=0", "REJECT_DELTA_W_ZERO_CLAIM", "no-source-only slot and action-measure owner are unsigned"),
        ("RUN1695_2_tau_numeric", "evaluate tau_WEP", "REJECT_TAU_NUMERIC_SCORE", "readout, source worldtube, material tensor and product convention missing"),
        ("RUN1695_3_tau_unity", "set tau_WEP=1", "REJECT_UNITY_SHORTCUT", "tau is a physical contraction, not a convention"),
        ("RUN1695_4_delta_w_bound", "convert product anchor to finite Delta_w bound", "REJECT_DELTA_W_AMPLITUDE_SCORE", "no tau_min>0 lower bound"),
        ("RUN1695_5_local_GR", "claim local GR/Newton/common matter", "BLOCKED_NO_CLAIM", "source-side theorem and left-hand GR bridge remain unsigned"),
        ("RUN1695_6_arena_export", "export to WEP/R10/PPN/clock/orbit score", "REJECT_ARENA_EXPORT", "finite branch lacks tau/product and arena kernels"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "case": case,
            "status": status,
            "reason": reason,
            "can_score": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for runner_id, case, status, reason in rows
    ]


def next_target_rows() -> list[dict[str, object]]:
    rows = [
        (
            "NEXT1695_0_primary",
            "1696-Y5-R2FR-parent-object-language-owner-or-tau-min-current-branch.md",
            "scripts/Y5_R2FR_parent_object_language_owner_or_tau_min_current_branch.py",
            "derive the parent object-language/action-measure owner that forbids source-only w_A; if not, derive a strictly positive tau_min lower bound from source/readout geometry so the MICROSCOPE product anchor becomes a usable nonclaim Delta_w constraint",
            "this keeps derivation-first pressure while making the finite branch empirically executable",
            "selected",
        ),
        (
            "NEXT1695_1_fallback",
            "1696b-Y5-R2FR-WEP-readout-source-worldtube-acquisition-pack.md",
            "scripts/Y5_R2FR_WEP_readout_source_worldtube_acquisition_pack.py",
            "start acquiring official/validated readout matrices, source worldtube rows and material tensors for tau_WEP",
            "use only if parent object-language owner cannot be derived next",
            "held_fallback",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": route_id,
            "next_target": target,
            "script": script,
            "objective": objective,
            "reason": reason,
            "selection_status": status,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for route_id, target, script, objective, reason, status in rows
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    rows = [
        ("CG1695_0_no_slot_theorem", "source-only w_A forbidden", "BLOCKED_NO_CLAIM", "exact typing theorem is not parent-derived"),
        ("CG1695_1_delta_w_zero", "Delta_w_TiPt theorem-zero", "BLOCKED_NO_CLAIM", "no-source-only/action-measure owner unsigned"),
        ("CG1695_2_tau_numeric", "tau_WEP numeric or lower bounded", "BLOCKED_NO_CLAIM", "readout/source/material/product inputs missing"),
        ("CG1695_3_delta_w_bound", "finite Delta_w constraint", "BLOCKED_NO_CLAIM", "product anchor lacks tau_min>0"),
        ("CG1695_4_WEP_score", "WEP source-weight score", "BLOCKED_NO_CLAIM", "parser permission blocked"),
        ("CG1695_5_local_GR", "derived local GR/Newton reduction", "BLOCKED_NO_CLAIM", "source-side common matter and left-hand GR bridge remain open"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": claim_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for claim_id, claim, status, reason in rows
    ]


def all_claim_flags_false(paths: list[Path]) -> bool:
    for path in paths:
        for row in read_csv(path):
            for field in ("can_score", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if field in row and bool_cell(row[field]):
                    return False
    return True


def copy_outputs() -> None:
    for source_path, target_paths in COPY_TARGETS.items():
        for target_path in target_paths:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, target_path)


def cleanup_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validate(
    source_rows: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    tau_rows: list[dict[str, object]],
    bound_rows: list[dict[str, object]],
    runner_rows_: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    sources_ok = all(bool_cell(row["exists"]) and bool_cell(row["needles_present"]) for row in source_rows)
    theorem_exact_nonclaim = any(
        row["theorem_id"] == "NST1695_7_verdict"
        and row["status"] == "NO_SOURCE_ONLY_SLOT_NOT_DERIVED_TAU_ROUTE_RETAINED"
        for row in theorem_rows
    )
    no_go_guard = any(row["theorem_id"] == "NST1695_3_same_action_no_go" and row["status"] == "NO_GO_GUARD" for row in theorem_rows)
    tau_requirements = {"P_WEP_K_CMSM_readout.csv", "P_WEP_R_source_Earth_worldtube.csv", "P_WEP_TiPt_material_response_tensor.csv", "strictly positive tau lower bound"}.issubset(
        {str(row["object"]) for row in tau_rows}
    )
    tau_blocked = all(str(row["tau_numeric"]).lower() == "false" for row in tau_rows)
    product_anchor = any(
        row["bound_id"] == "PBI1695_0_bound_anchor"
        and row["statement"] == "<= 2.8e-15"
        and row["current_status"] == "available"
        for row in bound_rows
    )
    tau_null_guard = any(row["bound_id"] == "PBI1695_2_tau_null_escape" and row["current_status"] == "active" for row in bound_rows)
    runner_blocks = all(not bool_cell(row["can_score"]) for row in runner_rows_)
    next_selected = any(
        row["route_id"] == "NEXT1695_0_primary"
        and row["selection_status"] == "selected"
        and "parent-object-language-owner-or-tau-min" in row["next_target"]
        for row in next_rows
    )
    local_gr_blocked = any(row["claim"] == "derived local GR/Newton reduction" and row["status"] == "BLOCKED_NO_CLAIM" for row in claim_rows)
    no_claim_flags = all_claim_flags_false(CLAIM_CHECKED)
    csv_parse = True
    for path in GENERATED:
        try:
            read_csv(path)
        except Exception:
            csv_parse = False
    branch_copies = all(target.exists() for targets in COPY_TARGETS.values() for target in targets)
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_untouched = len(list(FORMALIZATION.rglob("*1695*"))) == 0 if FORMALIZATION.exists() else True

    checks = [
        ("VAL1695_0_sources_exist", sources_ok, "all cited source paths exist and required needles are present"),
        ("VAL1695_1_theorem_exact_nonclaim", theorem_exact_nonclaim, "no-source-only-slot theorem is exact as condition but not parent-derived"),
        ("VAL1695_2_no_go_guard", no_go_guard, "same-action/covariance/classical-EOM shortcut is explicitly rejected"),
        ("VAL1695_3_tau_requirements", tau_requirements, "tau projection rows include readout, source worldtube, material tensor and tau_min"),
        ("VAL1695_4_tau_blocked", tau_blocked, "no tau_WEP numeric row is admitted"),
        ("VAL1695_5_product_anchor", product_anchor, "MICROSCOPE 2.8e-15 product anchor is retained"),
        ("VAL1695_6_tau_null_guard", tau_null_guard, "tau-null escape blocks finite Delta_w bound"),
        ("VAL1695_7_runner_blocks", runner_blocks, "runner blocks zero claims, tau score, Delta_w bound and arena export"),
        ("VAL1695_8_next_selected", next_selected, "next target selects parent object-language owner or tau_min branch"),
        ("VAL1695_9_local_gr_blocked", local_gr_blocked, "local GR/Newton claim remains blocked"),
        ("VAL1695_10_no_claim_flags", no_claim_flags, "all generated scoring and claim flags remain false"),
        ("VAL1695_11_csv_parse", csv_parse, "all generated 1695 CSVs parse"),
        ("VAL1695_12_branch_copies", branch_copies, "branch/quarantine/queue copies exist"),
        ("VAL1695_13_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL1695_14_formalization_untouched", formalization_untouched, "no 1695 outputs found under formalization-workbench"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1695_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1695 no-source-only-slot theorem or tau-WEP projection current-branch validation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def write_doc(
    source_rows: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    tau_rows: list[dict[str, object]],
    bound_rows: list[dict[str, object]],
    runner_rows_: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    body = f"""# 1695 - No-Source-Only Slot Theorem Or Tau-WEP Projection Current Branch

## Verdict

1695 is the cleanest statement of the source-side problem so far. The `w_A` gremlin can be killed if the parent object language really has no source-only coefficient slot: no `Hom(species_label or hidden_marker, active-source-prefactor)` except a common constant calibration mode. That is an exact theorem **if** the parent grammar is signed.

But the current corpus still does not derive that grammar from deeper MTS primitives. Same-action, covariance, additivity, classical equations and post-variation current ownership are not enough: `S_matter=sum_A w_A S_A` remains a legal countermodel unless the parent syntax forbids it before variation.

So the finite route stays alive. The MICROSCOPE anchor remains `abs(Delta_w_TiPt * tau_WEP) <= 2.8e-15`; it becomes a finite `Delta_w_TiPt` constraint only if `|tau_WEP| >= tau_min > 0` is derived or sourced. `tau_WEP=1` is still forbidden.

## Source Register

{markdown_table(source_rows, ["source_key", "source_path", "exists", "needles_present", "use_in_1695"])}

## No-Source-Only Slot Theorem Audit

{markdown_table(theorem_rows, ["theorem_id", "claim_piece", "status", "if_signed", "missing_for_claim"])}

## Tau-WEP Projection Readiness

{markdown_table(tau_rows, ["projection_id", "object", "current_status", "required_input", "effect"])}

## Product Bound Interpretation

{markdown_table(bound_rows, ["bound_id", "quantity", "statement", "current_status", "interpretation"])}

## Runner Refusal

{markdown_table(runner_rows_, ["runner_id", "case", "status", "reason"])}

## Next Target

{markdown_table(next_rows, ["route_id", "next_target", "objective", "selection_status"])}

## Claim Gates

{markdown_table(claim_rows, ["claim_id", "claim", "status", "reason"])}

## Validation

{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Working Interpretation

This keeps us on the Mayweather route: no haymaker claim, no fake knockout, just cleaner footwork. The path to GR is now pinned to a precise parent-language theorem; the fallback is also precise, because the finite WEP branch needs `tau_min` rather than a hand-set unity factor.
"""
    DOC.write_text(body, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    source_rows = source_register_rows()
    theorem_rows = no_slot_theorem_rows()
    tau_rows = tau_projection_rows()
    bound_rows = product_bound_rows()
    runner_rows_ = runner_rows()
    next_rows = next_target_rows()
    claim_rows = claim_gate_rows()

    write_csv(SOURCE_REGISTER, source_rows, ["branch_id", "source_key", "source_path", "exists", "needles_present", "required_needles", "use_in_1695", "valid_for_claim", "claim_allowed"])
    write_csv(NO_SLOT_THEOREM, theorem_rows, ["branch_id", "theorem_id", "claim_piece", "formal_statement", "status", "if_signed", "missing_for_claim", "parent_signature", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(TAU_PROJECTION, tau_rows, ["branch_id", "projection_id", "object", "current_status", "required_input", "effect", "source_anchor", "tau_numeric", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(PRODUCT_BOUND, bound_rows, ["branch_id", "bound_id", "quantity", "statement", "bound_type", "current_status", "source_anchor", "interpretation", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(RUNNER, runner_rows_, ["branch_id", "runner_id", "case", "status", "reason", "can_score", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(NEXT_TARGET, next_rows, ["branch_id", "route_id", "next_target", "script", "objective", "reason", "selection_status", "valid_for_claim", "claim_allowed"])
    write_csv(CLAIM_GATE, claim_rows, ["branch_id", "claim_id", "claim", "status", "reason", "valid_for_claim", "claim_allowed"])

    copy_outputs()
    cleanup_pycache()
    validation_rows = validate(source_rows, theorem_rows, tau_rows, bound_rows, runner_rows_, next_rows, claim_rows)
    write_csv(VALIDATION, validation_rows, ["check_id", "result", "detail", "valid_for_claim", "claim_allowed"])
    write_doc(source_rows, theorem_rows, tau_rows, bound_rows, runner_rows_, next_rows, claim_rows, validation_rows)

    failed = [row for row in validation_rows if row["result"] != "PASS"]
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("1695 validation PASS")


if __name__ == "__main__":
    main()
