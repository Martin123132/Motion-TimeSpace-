from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1696"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_SOURCE = MICROSCOPE / "branch_locked_wep" / "source"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "1696-Y5-R2FR-parent-object-language-owner-or-tau-min-current-branch.md"

SOURCE_FILES = {
    "1695_doc": ROOT / "1695-Y5-R2FR-no-source-only-slot-theorem-or-tau-WEP-projection-current-branch.md",
    "1695_validation": OUT / "P8_Y5_BRR545_1695_VALIDATION.csv",
    "1695_next": OUT / "P8_Y5_PARENT_QLOC_1695_NEXT_TARGET.csv",
    "1450_label_forgetting": OUT / "P8_Y5_R10_1450_HILBERT_SOURCE_LABEL_FORGETTING_THEOREM_ATTEMPT.csv",
    "1452_measure_current": OUT / "P8_Y5_R10_1452_COMMON_MEASURE_CURRENT_THEOREM_ATTEMPT.csv",
    "1453_current_owner": OUT / "P8_Y5_R10_1453_CURRENT_SOURCE_NORMALIZATION_OWNER_THEOREM_ATTEMPT.csv",
    "1462_measure_signature": OUT / "P8_Y5_R10_1462_COMMON_MEASURE_CURRENT_SIGNATURE_ATTEMPT.csv",
    "1464_connected_category": OUT / "P8_Y5_R10_1464_CONNECTED_MATTER_CATEGORY_PROOF_ATTEMPT.csv",
    "1477_graph_certificate": MICROSCOPE / "quarantine" / "1477" / "CONNECTED_MATTER_GRAPH_CERTIFICATE_NONCLAIM.csv",
    "1478_action_line": MICROSCOPE / "quarantine" / "1478" / "SINGLE_ACTION_DENSITY_LINE_PROOF_ATTEMPT_NONCLAIM.csv",
    "1479_no_source_typing": MICROSCOPE / "quarantine" / "1479" / "NO_SOURCE_ONLY_ACTION_PREFACTOR_TYPING_THEOREM_ATTEMPT_NONCLAIM.csv",
    "1480_hom_exclusion": MICROSCOPE / "quarantine" / "1480" / "COEFFICIENT_DOMAIN_HOM_EXCLUSION_ATTEMPT_NONCLAIM.csv",
    "1482_tau_readiness": OUT / "P8_Y5_R10_1482_TAU_WEP_READINESS_UPDATE.csv",
    "1083_source_vector": OUT / "P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv",
    "1084_readout_gate": OUT / "P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv",
    "1225_tau_attempt": OUT / "P8_Y5_R10_1225_TAU_WEP_PROJECTION_ATTEMPT.csv",
    "1482_parser_status": BRANCH_SOURCE / "P_WEP_R_source_status_1482.csv",
}

NEEDLES = {
    "1695_doc": ["NEXT1695_0_primary", "tau_min"],
    "1695_validation": ["VAL1695_OVERALL", "PASS"],
    "1695_next": ["NEXT1695_0_primary", "parent-object-language-owner-or-tau-min"],
    "1450_label_forgetting": ["HT1450_6_verdict", "CONDITIONAL_THEOREM_NOT_PARENT_DERIVED"],
    "1452_measure_current": ["CMT1452_6_verdict", "FAIL_CURRENT_PROOF_NOT_PARENT_SIGNED"],
    "1453_current_owner": ["CSO1453_5_pre_variation_weight", "SURVIVES_PRE_VARIATION"],
    "1462_measure_signature": ["CMC1462_6_verdict", "PROOF_NOT_CLOSED"],
    "1464_connected_category": ["CON1464_5_verdict", "PROOF_NOT_CLOSED"],
    "1477_graph_certificate": ["GRC1477_2_action_density_line", "FAIL_LINE_OWNER_UNSIGNED"],
    "1478_action_line": ["SAL1478_4_verdict", "PROOF_NOT_CLOSED_COMPONENT_VECTOR_REQUIRED"],
    "1479_no_source_typing": ["NST1479_4_verdict", "PROOF_NOT_CLOSED_BOUND_PACK_REQUIRED"],
    "1480_hom_exclusion": ["CDH1480_5_verdict", "PROOF_NOT_CLOSED_SMOKE_RUNNER_REQUIRED"],
    "1482_tau_readiness": ["TAU1482_0_formula", "MISSING_LIVE_READOUT_MATRIX"],
    "1083_source_vector": ["SCG1083_0_profile_weighting", "MISSING_SOURCE_PROFILE_WEIGHTING"],
    "1084_readout_gate": ["RIG1084_0_CMSM_arrays", "OFFICIAL_ARRAYS_NOT_IMPORTED"],
    "1225_tau_attempt": ["TAU1225_6_verdict", "TAU_WEP_PROJECTION_NOT_DERIVED"],
    "1482_parser_status": ["ACCEPT1482_5_overall_parser_permission", "BLOCKED"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1696_SOURCE_REGISTER.csv"
OWNER_STACK = OUT / "P8_Y5_PARENT_QLOC_1696_PARENT_OBJECT_LANGUAGE_OWNER_STACK.csv"
TAU_MIN_GATE = OUT / "P8_Y5_PARENT_QLOC_1696_TAU_MIN_LOWER_BOUND_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1696_DECISION.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1696_RUNNER_REFUSAL.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1696_NEXT_TARGET.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1696_CLAIM_GATE.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1696_VALIDATION.csv"

GENERATED = [SOURCE_REGISTER, OWNER_STACK, TAU_MIN_GATE, DECISION, RUNNER, NEXT_TARGET, CLAIM_GATE]
CLAIM_CHECKED = [OWNER_STACK, TAU_MIN_GATE, DECISION, RUNNER, NEXT_TARGET, CLAIM_GATE]

COPY_TARGETS = {
    OWNER_STACK: [
        QUARANTINE / "PARENT_OBJECT_LANGUAGE_OWNER_STACK.csv",
        BRANCH_RESIDUALS / "R2FR_parent_object_language_owner_stack_1696.csv",
        QUEUE / "JR1696_PARENT_OBJECT_LANGUAGE_OWNER_STACK.csv",
    ],
    TAU_MIN_GATE: [
        QUARANTINE / "TAU_MIN_LOWER_BOUND_GATE.csv",
        BRANCH_RESIDUALS / "R2FR_tau_min_lower_bound_gate_1696.csv",
        QUEUE / "JR1696_TAU_MIN_LOWER_BOUND_GATE.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_1696.csv",
        QUEUE / "JR1696_NEXT_TARGET.csv",
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
    table = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
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
                "use_in_1696": "parent object-language owner stack and tau_min lower-bound gate",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def owner_stack_rows() -> list[dict[str, object]]:
    rows = [
        ("OBJ1696_0_typed_language", "typed parent object language", "Arg(S_ord) excludes inert source-only coefficients", "EXACT_IF_PARENT_OWNED", "w_A ill-typed except common calibration", "primitive parent object language not derived"),
        ("OBJ1696_1_label_forgetting", "Hilbert source label forgetting", "source functor domain is T_total, not labelled {(T_A,A)}", "CONDITIONAL_THEOREM_NOT_PARENT_DERIVED", "relative kappa_A/w_A cannot be formed after variation", "no-source-only slot must already be absent"),
        ("OBJ1696_2_action_density_line", "single action-density line", "S_ord has one parent measure, hbar/action scale and one ordinary-matter L_action owner", "PROOF_NOT_CLOSED_COMPONENT_VECTOR_REQUIRED", "relative source/action weights collapse to common mode", "L_action, hbar, measure and syntax owner unsigned"),
        ("OBJ1696_3_connected_category", "connected ordinary-matter category", "naturality on a parent-owned connected graph forces w_A=w_*", "PROOF_NOT_CLOSED", "component weights cannot vary by material sector", "ordinary matter graph/morphisms not parent-owned"),
        ("OBJ1696_4_common_measure_current", "common measure/current owner", "single measure/current owner plus no non-Hilbert bypass kills J_A,c_A,zeta_A", "PROOF_NOT_CLOSED", "pre-variation source normalization residuals vanish", "action-scale owner, Jacobian exclusion and non-Hilbert silence unsigned"),
        ("OBJ1696_5_current_owner_limit", "current owner alone is insufficient", "T_H inherits w_A if w_A is inserted before variation", "SURVIVES_PRE_VARIATION", "prevents false source-owner proof", "needs object-language/action-measure theorem"),
        ("OBJ1696_6_hom_exclusion", "coefficient-domain Hom exclusion", "Hom(C_hid or source labels, Coeff_source) is absent/constant", "PROOF_NOT_CLOSED_SMOKE_RUNNER_REQUIRED", "hidden/source markers cannot regenerate w_A", "trivial hidden algebra or forbidden coefficient target not parent-derived"),
        ("OBJ1696_7_verdict", "parent object-language owner stack", "all owner clauses would kill source-only w_A together", "PARENT_OBJECT_LANGUAGE_OWNER_NOT_DERIVED_TAU_MIN_ROUTE_RETAINED", "no Delta_w theorem-zero yet", "derive owner stack or continue tau_min geometry"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "owner_id": owner_id,
            "clause": clause,
            "formal_statement": statement,
            "current_status": status,
            "if_signed": if_signed,
            "current_blocker": blocker,
            "parent_signed": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for owner_id, clause, statement, status, if_signed, blocker in rows
    ]


def tau_min_rows() -> list[dict[str, object]]:
    rows = [
        ("TAUMIN1696_0_formula", "tau_eff_e := branch_locked_orbit_average(K_CMSM * R_source * readout_mask)", "SYMBOLIC_FORMULA_ONLY", "K_CMSM/readout matrix; R_source; masks; orbit weights; units/sign", "not_evaluated"),
        ("TAUMIN1696_1_readout", "official MICROSCOPE CMSM/export arrays", "OFFICIAL_ARRAYS_NOT_IMPORTED", "time, segments, gx/gz/Sxx/Sxz, masks, calibration flags, attitude/orbit convention", "blocks_tau_numeric"),
        ("TAUMIN1696_2_source_worldtube", "Earth/source worldtube", "MISSING_SOURCE_PROFILE_WEIGHTING", "profile-weighted source vector seen by MICROSCOPE", "blocks_tau_numeric"),
        ("TAUMIN1696_3_material_tensor", "TA6V/PtRh10 material response tensor", "MISSING_FULL_MATERIAL_TENSOR", "same source-weight convention and uncertainties", "blocks_delta_w_mapping"),
        ("TAUMIN1696_4_product_convention", "eta_AB product normalization", "NORMALIZATION_NOT_FILLED", "source response x material response x readout kernel -> eta", "forbids_tau_unity"),
        ("TAUMIN1696_5_parent_coupling", "C_parent or action-measure owner", "MISSING_C_PARENT_IMPORT", "theorem-zero route or finite coefficient in same branch", "blocks_parent_local_GR"),
        ("TAUMIN1696_6_lower_bound", "|tau_WEP| >= tau_min > 0", "NO_TAU_MIN_SOURCE", "nonvanishing theorem or sourced lower bound with assumptions", "no_finite_delta_w_bound"),
        ("TAUMIN1696_7_parser_permission", "branch-locked WEP parser", "BLOCKED", "requires official arrays, worldtube, product convention, C_parent, material tensor and branch rows", "no_WEP_score"),
        ("TAUMIN1696_8_verdict", "tau_min lower-bound gate", "TAU_MIN_NOT_DERIVED_OR_SOURCED", "all tau factors must close before product anchor becomes Delta_w constraint", "finite_branch_retained_nonclaim"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "tau_id": tau_id,
            "object": obj,
            "current_status": status,
            "required_for_tau_min": required,
            "effect": effect,
            "tau_min_positive": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for tau_id, obj, status, required, effect in rows
    ]


def decision_rows() -> list[dict[str, object]]:
    rows = [
        ("DEC1696_0_owner_status", "PARENT_OBJECT_LANGUAGE_OWNER_NOT_DERIVED", "the stack is exact but too many clauses remain parent-unsigned", "do not set Delta_w_A=0"),
        ("DEC1696_1_tau_status", "TAU_MIN_NOT_DERIVED_OR_SOURCED", "no official readout/source/material/product pack and no nonvanishing theorem", "do not convert product bound to Delta_w bound"),
        ("DEC1696_2_best_next", "NEXT_1697_READOUT_SOURCE_PACK_OR_OWNER_AXIOM_CANDIDATE", "theorem route needs a parent-owner axiom candidate; finite route needs actual WEP projection inputs", "build explicit owner axiom candidate plus data-acquisition checklist"),
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


def runner_rows() -> list[dict[str, object]]:
    rows = [
        ("RUN1696_0_owner_claim", "claim parent object-language owner", "REJECT_OWNER_CLAIM", "owner stack exact but not parent-derived"),
        ("RUN1696_1_delta_w_zero", "claim Delta_w_A=0", "REJECT_DELTA_W_ZERO", "w_A source-only slot not forbidden by signed parent theorem"),
        ("RUN1696_2_tau_min", "claim tau_min>0", "REJECT_TAU_MIN_CLAIM", "no readout/source/material/product nonvanishing proof"),
        ("RUN1696_3_product_to_delta_w", "convert MICROSCOPE product bound to Delta_w bound", "REJECT_DELTA_W_BOUND", "tau_min missing"),
        ("RUN1696_4_wep_score", "run WEP source score", "REJECT_WEP_SCORE", "parser permission blocked"),
        ("RUN1696_5_local_gr", "claim local GR/Newton", "BLOCKED_NO_CLAIM", "source owner and left-hand GR bridge remain open"),
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
        ("NEXT1696_0_primary", "1697-Y5-R2FR-owner-axiom-candidate-and-WEP-readout-source-pack.md", "scripts/Y5_R2FR_owner_axiom_candidate_and_WEP_readout_source_pack.py", "write the minimal parent-owner axiom candidate that would forbid source-only w_A, and in parallel create the concrete WEP readout/source-worldtube/material acquisition checklist needed for tau_min", "selected"),
        ("NEXT1696_1_theorem_only", "1697a-Y5-R2FR-parent-object-language-axiom-minimality-proof.md", "scripts/Y5_R2FR_parent_object_language_axiom_minimality_proof.py", "attempt to derive the owner axiom from MTS quotient/category primitives only", "held_fallback"),
        ("NEXT1696_2_data_only", "1697b-Y5-R2FR-WEP-tau-min-data-acquisition-runner.md", "scripts/Y5_R2FR_WEP_tau_min_data_acquisition_runner.py", "prepare external readout/source/material data acquisition for tau_min without claiming physics", "held_fallback"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": route_id,
            "next_target": target,
            "script": script,
            "objective": objective,
            "selection_status": status,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for route_id, target, script, objective, status in rows
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    rows = [
        ("CG1696_0_owner", "parent object-language owner", "BLOCKED_NO_CLAIM", "owner stack not parent-signed"),
        ("CG1696_1_delta_w_zero", "Delta_w theorem-zero", "BLOCKED_NO_CLAIM", "source-only w_A not forbidden"),
        ("CG1696_2_tau_min", "tau_min positive lower bound", "BLOCKED_NO_CLAIM", "readout/source/material/product inputs missing"),
        ("CG1696_3_WEP", "WEP finite source score", "BLOCKED_NO_CLAIM", "parser permission blocked"),
        ("CG1696_4_local_GR", "derived local GR/Newton reduction", "BLOCKED_NO_CLAIM", "source-side and left-hand GR gates still open"),
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
    owner_rows: list[dict[str, object]],
    tau_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    runner_rows_: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    sources_ok = all(bool_cell(row["exists"]) and bool_cell(row["needles_present"]) for row in source_rows)
    owner_stack_complete = {"typed parent object language", "Hilbert source label forgetting", "single action-density line", "connected ordinary-matter category", "common measure/current owner", "coefficient-domain Hom exclusion"}.issubset({str(row["clause"]) for row in owner_rows})
    owner_not_derived = any(row["owner_id"] == "OBJ1696_7_verdict" and row["current_status"] == "PARENT_OBJECT_LANGUAGE_OWNER_NOT_DERIVED_TAU_MIN_ROUTE_RETAINED" for row in owner_rows)
    tau_gate_complete = {"official MICROSCOPE CMSM/export arrays", "Earth/source worldtube", "TA6V/PtRh10 material response tensor", "|tau_WEP| >= tau_min > 0", "branch-locked WEP parser"}.issubset({str(row["object"]) for row in tau_rows})
    tau_not_positive = all(not bool_cell(row["tau_min_positive"]) for row in tau_rows)
    decision_next = any(row["decision_id"] == "DEC1696_2_best_next" for row in decision_rows_)
    runner_blocks = all(not bool_cell(row["can_score"]) for row in runner_rows_)
    next_selected = any(row["route_id"] == "NEXT1696_0_primary" and row["selection_status"] == "selected" and "owner-axiom-candidate" in row["next_target"] for row in next_rows)
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
    formalization_untouched = len(list(FORMALIZATION.rglob("*1696*"))) == 0 if FORMALIZATION.exists() else True
    checks = [
        ("VAL1696_0_sources_exist", sources_ok, "all cited source paths exist and required needles are present"),
        ("VAL1696_1_owner_stack_complete", owner_stack_complete, "owner stack includes typing, label forgetting, action line, connected graph, measure/current and Hom exclusion"),
        ("VAL1696_2_owner_not_derived", owner_not_derived, "parent object-language owner remains unsigned"),
        ("VAL1696_3_tau_gate_complete", tau_gate_complete, "tau_min gate includes readout, source worldtube, material tensor, tau_min and parser"),
        ("VAL1696_4_tau_not_positive", tau_not_positive, "no tau_min positive lower bound is admitted"),
        ("VAL1696_5_decision_next", decision_next, "decision selects owner axiom candidate plus WEP source pack"),
        ("VAL1696_6_runner_blocks", runner_blocks, "runner blocks owner, Delta_w, tau_min, WEP and local-GR claims"),
        ("VAL1696_7_next_selected", next_selected, "next target selects owner axiom candidate and WEP readout/source pack"),
        ("VAL1696_8_local_gr_blocked", local_gr_blocked, "local GR/Newton claim remains blocked"),
        ("VAL1696_9_no_claim_flags", no_claim_flags, "all generated scoring and claim flags remain false"),
        ("VAL1696_10_csv_parse", csv_parse, "all generated 1696 CSVs parse"),
        ("VAL1696_11_branch_copies", branch_copies, "branch/quarantine/queue copies exist"),
        ("VAL1696_12_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL1696_13_formalization_untouched", formalization_untouched, "no 1696 outputs found under formalization-workbench"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [
        {"check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail, "valid_for_claim": False, "claim_allowed": False}
        for check_id, passed, detail in checks
    ]
    rows.append({"check_id": "VAL1696_OVERALL", "result": "PASS" if overall else "FAIL", "detail": "1696 parent object-language owner or tau-min current-branch validation", "valid_for_claim": False, "claim_allowed": False})
    return rows


def write_doc(source_rows, owner_rows, tau_rows, decision_rows_, runner_rows_, next_rows, claim_rows, validation_rows) -> None:
    body = f"""# 1696 - Parent Object-Language Owner Or Tau-Min Current Branch

## Verdict

1696 assembles the full owner stack needed to kill `w_A`: typed parent language, label forgetting, one action-density line, connected ordinary-matter category, common measure/current owner, and Hom exclusion for hidden/source coefficient targets.

The stack is mathematically coherent, but it is still not parent-derived. The exact obstruction is no longer vague: unless MTS owns the ordinary-matter object language before variation, `S_matter=sum_A w_A S_A` survives as a countermodel.

The finite route also remains blocked but well-posed. A useful `tau_min` needs live readout arrays, source worldtube, material tensor, product convention, parent coupling slot and parser permission. None are admitted as numeric in 1696.

## Source Register

{markdown_table(source_rows, ["source_key", "source_path", "exists", "needles_present", "use_in_1696"])}

## Parent Object-Language Owner Stack

{markdown_table(owner_rows, ["owner_id", "clause", "current_status", "if_signed", "current_blocker"])}

## Tau-Min Lower-Bound Gate

{markdown_table(tau_rows, ["tau_id", "object", "current_status", "required_for_tau_min", "effect"])}

## Decision

{markdown_table(decision_rows_, ["decision_id", "decision", "reason", "next_action"])}

## Runner Refusal

{markdown_table(runner_rows_, ["runner_id", "case", "status", "reason"])}

## Next Target

{markdown_table(next_rows, ["route_id", "next_target", "objective", "selection_status"])}

## Claim Gates

{markdown_table(claim_rows, ["claim_id", "claim", "status", "reason"])}

## Validation

{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Working Interpretation

This is a good narrowing. We are not “missing Python” here; we are missing either a parent syntax theorem or a real projection lower bound. That is exactly the kind of missing piece a serious field-theory programme should expose rather than bury.
"""
    DOC.write_text(body, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    source_rows = source_register_rows()
    owner_rows = owner_stack_rows()
    tau_rows = tau_min_rows()
    decision_rows_ = decision_rows()
    runner_rows_ = runner_rows()
    next_rows = next_target_rows()
    claim_rows = claim_gate_rows()
    write_csv(SOURCE_REGISTER, source_rows, ["branch_id", "source_key", "source_path", "exists", "needles_present", "required_needles", "use_in_1696", "valid_for_claim", "claim_allowed"])
    write_csv(OWNER_STACK, owner_rows, ["branch_id", "owner_id", "clause", "formal_statement", "current_status", "if_signed", "current_blocker", "parent_signed", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(TAU_MIN_GATE, tau_rows, ["branch_id", "tau_id", "object", "current_status", "required_for_tau_min", "effect", "tau_min_positive", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(DECISION, decision_rows_, ["branch_id", "decision_id", "decision", "reason", "next_action", "valid_for_claim", "claim_allowed"])
    write_csv(RUNNER, runner_rows_, ["branch_id", "runner_id", "case", "status", "reason", "can_score", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(NEXT_TARGET, next_rows, ["branch_id", "route_id", "next_target", "script", "objective", "selection_status", "valid_for_claim", "claim_allowed"])
    write_csv(CLAIM_GATE, claim_rows, ["branch_id", "claim_id", "claim", "status", "reason", "valid_for_claim", "claim_allowed"])
    copy_outputs()
    cleanup_pycache()
    validation_rows = validate(source_rows, owner_rows, tau_rows, decision_rows_, runner_rows_, next_rows, claim_rows)
    write_csv(VALIDATION, validation_rows, ["check_id", "result", "detail", "valid_for_claim", "claim_allowed"])
    write_doc(source_rows, owner_rows, tau_rows, decision_rows_, runner_rows_, next_rows, claim_rows, validation_rows)
    failed = [row for row in validation_rows if row["result"] != "PASS"]
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("1696 validation PASS")


if __name__ == "__main__":
    main()
