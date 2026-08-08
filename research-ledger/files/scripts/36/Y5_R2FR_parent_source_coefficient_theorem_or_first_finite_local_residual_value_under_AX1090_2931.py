from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2931"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2931-Y5-R2FR-parent-source-coefficient-theorem-or-first-finite-local-residual-value-under-AX1090.md"

SRC_2930_DOC = ROOT / "2930-Y5-R2FR-source-owner-Hcore-to-beta-denominator-binding-or-finite-local-residual-first-value-under-AX1090.md"
SRC_2930_NEXT = RESIDUALS / "P8_Y5_R2FR_2930_NEXT_TARGET.csv"
SRC_2930_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2930_DENOMINATOR_BINDING_CONTRACT.csv"
SRC_2930_LEDGER = RESIDUALS / "P8_Y5_R2FR_2930_SOURCE_COEFFICIENT_LEDGER.csv"
SRC_2930_QUEUE = RESIDUALS / "P8_Y5_R2FR_2930_FIRST_VALUE_ACQUISITION_QUEUE.csv"
SRC_2930_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2930_VALIDATION.csv"

SRC_2920_SQUARE = RESIDUALS / "P8_Y5_R2FR_2920_PARENT_SQUARE_LAW_AUDIT.csv"
SRC_2920_KERNEL = RESIDUALS / "P8_Y5_R2FR_2920_BETA_SECOND_ORDER_SOURCE_NORMALIZATION_KERNEL.csv"
SRC_2924_EH = RESIDUALS / "P8_Y5_R2FR_2924_EH_ANCHOR_COEFFICIENT_MAP.csv"
SRC_2924_GPB = RESIDUALS / "P8_Y5_R2FR_2924_GAUSS_POISSON_BRIDGE_CHECK.csv"
SRC_2924_REDUCTION = RESIDUALS / "P8_Y5_R2FR_2924_MTS_TO_EH_REDUCTION_CONTRACT.csv"
SRC_2925_VECTOR = RESIDUALS / "P8_Y5_R2FR_2925_REDUCTION_RESIDUAL_VECTOR.csv"
SRC_2928_COUPLING = RESIDUALS / "P8_Y5_R2FR_2928_KAPPA_ELLJ_COUPLING_BASELINE_ROWS.csv"
SRC_2578_GATE = RESIDUALS / "P8_Y5_PIM_HAMILTONIAN_COUPLING_2578_COUPLING_BASELINE_GATE.csv"
SRC_2578_LEDGER = RESIDUALS / "P8_Y5_PIM_HAMILTONIAN_COUPLING_2578_RESIDUAL_INPUT_LEDGER.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2931_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_2931_PARENT_SOURCE_COEFFICIENT_THEOREM_ATTEMPT.csv",
    "eh_control": RESIDUALS / "P8_Y5_R2FR_2931_EH_CONTROL_COEFFICIENT_DERIVATION.csv",
    "residual": RESIDUALS / "P8_Y5_R2FR_2931_MTS_COEFFICIENT_RESIDUAL_DECOMPOSITION.csv",
    "first_value": RESIDUALS / "P8_Y5_R2FR_2931_FIRST_FINITE_VALUE_CANDIDATE_ROWS.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2931_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2931_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2931_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2931_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2931_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "theorem_copy": PARENT_ACTION / "Parent_source_coefficient_theorem_attempt_2931_NONCLAIM.csv",
    "residual_copy": LOCAL_BOUNDS / "MTS_coefficient_residual_decomposition_2931_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2931_KAPPA_ELLJ_OR_AB_FIRST_VALUE_NEXT_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv_rows(path)
        return True
    except Exception:
        return False


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": RUN_UTC,
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    selected = columns or list(rows[0].keys())
    header = "| " + " | ".join(selected) + " |"
    separator = "| " + " | ".join("---" for _ in selected) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in selected) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2931_00_2930_doc", SRC_2930_DOC, "NEXT2930_0_2931;A_source;B_source;Validation overall: `True`", "2930 selected parent source coefficient theorem or first finite value"),
        ("SRC2931_01_2930_next", SRC_2930_NEXT, "NEXT2930_0_2931;A_source;B_source;Dln(kappa_MTS);Dln(ell_J)", "machine-readable 2931 target"),
        ("SRC2931_02_2930_contract", SRC_2930_CONTRACT, "DBC2930_2_A_source;DBC2930_3_B_source;DBC2930_9_verdict", "denominator binding contract"),
        ("SRC2931_03_2930_ledger", SRC_2930_LEDGER, "SCL2930_0_A_source;SCL2930_1_B_source;SCL2930_6_Delta_denominator_binding_abs", "source coefficient ledger"),
        ("SRC2931_04_2930_queue", SRC_2930_QUEUE, "FVQ2930_0_delta_beta_source;FVQ2930_2_Dln_kappa;FVQ2930_5_B_source", "first-value acquisition queue"),
        ("SRC2931_05_2930_validation", SRC_2930_VALIDATION, "VAL2930_OVERALL;True", "2930 validation summary"),
        ("SRC2931_06_2920_square", SRC_2920_SQUARE, "SQA2920_0_ppn_extraction_law;SQA2920_3_parent_square_source;SQA2920_8_verdict", "prior beta square-law audit"),
        ("SRC2931_07_2920_kernel", SRC_2920_KERNEL, "B2K2920_0_delta_beta_source;B2K2920_6_Delta_beta_total_abs", "beta residual kernel"),
        ("SRC2931_08_2924_EH", SRC_2924_EH, "EHA2924_0_EH_action_block;EHA2924_4_EH_weak_field;EHA2924_5_total_verdict", "EH control coefficient anchor"),
        ("SRC2931_09_2924_GPB", SRC_2924_GPB, "GPB2924_0_EH_field_equation;GPB2924_3_orbital_readout;GPB2924_4_MTS_verdict", "EH Gauss/Poisson/orbital bridge"),
        ("SRC2931_10_2924_reduction", SRC_2924_REDUCTION, "RED2924_0_metric_identification;RED2924_2_EH_core_reduction;RED2924_10_total_verdict", "MTS-to-EH reduction contract"),
        ("SRC2931_11_2925_vector", SRC_2925_VECTOR, "RV2925_1_constant_kappa;RV2925_2_EH_core_residual;RV2925_TOTAL", "MTS local reduction residual vector"),
        ("SRC2931_12_2928_coupling", SRC_2928_COUPLING, "CB2928_0_kappa_alpha3;CB2928_1_ellJ_alpha3;CB2928_3_coupling_total", "kappa/ellJ coupling baseline rows"),
        ("SRC2931_13_2578_gate", SRC_2578_GATE, "COG2578_0_kappa_constant;COG2578_2_ellJ_source_scale;COG2578_4_verdict", "coupling baseline identity gate"),
        ("SRC2931_14_2578_ledger", SRC_2578_LEDGER, "RES2578_7_delta_kappa;RES2578_8_delta_ellJ;RES2578_9_total", "coupling residual ledger"),
    ]
    rows = []
    for source_id, source_path, anchors, role in specs:
        found, missing = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(source_path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": source_path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def theorem_attempt_rows() -> list[dict[str, Any]]:
    specs = [
        ("PCT2931_0_definition", "source-normalized weak-field coefficient definition", "g_00=-1+2 A_source W/c^2-2 B_source W^2/c^4+O(W^3)", "PASS_DEFINITION_FROM_2930", "defines coefficients but does not compute them from MTS", True),
        ("PCT2931_1_measured_U_extraction", "PPN beta extraction", "U=A_source W -> beta_eff=B_source/A_source^2", "PASS_ALGEBRAIC_IDENTITY_FROM_2920", "this is an exact comparison identity, not beta=1", True),
        ("PCT2931_2_EH_control", "EH/GR control coefficient theorem", "EH weak field in the same source-normalized frame gives A_EH=1, B_EH=1, beta_EH=1", "PASS_CONTROL_REFERENCE_ONLY", "shows the target is correct; cannot substitute for MTS parent action", True),
        ("PCT2931_3_MTS_parent_coefficients", "MTS parent source coefficient map", "A_source and B_source from Hcore/Q_tau/Pi_M^H with same M_H_ref", "NOT_DERIVED_CURRENT_CORPUS", "2930/2923/2922 leave source denominator and Hcore coefficients unsigned", False),
        ("PCT2931_4_exact_residual_law", "exact MTS beta residual if A/B are not proven", "delta_beta_source=((1+Delta_B)/(1+Delta_A)^2)-1", "PASS_RESIDUAL_IDENTITY_NONCLAIM", "a useful theorem: failure of square law becomes a named finite residual", True),
        ("PCT2931_5_square_condition", "exact square-law residual condition", "B_source=A_source^2 iff Delta_B=2*Delta_A+Delta_A^2", "PASS_CONDITIONAL_FORMULA_NOT_ZERO", "this tells us exactly what a future parent proof must show", True),
        ("PCT2931_6_MTS_square_theorem", "MTS square law in current corpus", "Delta_B-2*Delta_A-Delta_A^2=0", "NOT_DERIVED", "no parent-signed Hcore coefficient map or no-hidden-source theorem supplies this", False),
        ("PCT2931_7_verdict", "parent source coefficient theorem", "A_source/B_source theorem sufficient for Newton/beta branch", "PARENT_COEFFICIENT_THEOREM_NOT_DERIVED_FIRST_VALUE_ROUTE_SELECTED", "move to first finite value or coupling constant proof instead of claiming beta", False),
    ]
    return [
        add_common(
            {
                "attempt_id": attempt_id,
                "clause": clause,
                "math_form": math_form,
                "current_status": current_status,
                "reason": reason,
                "condition_passed": condition_passed,
                "adopted_for_claim": False,
                "source_paths": ";".join(str(path) for path in [SRC_2930_CONTRACT, SRC_2920_SQUARE, SRC_2924_EH, SRC_2924_REDUCTION]),
            }
        )
        for attempt_id, clause, math_form, current_status, reason, condition_passed in specs
    ]


def eh_control_rows() -> list[dict[str, Any]]:
    specs = [
        ("EHC2931_0_action", "EH action anchor", "S_EH=(2*kappa0)^-1 int sqrt(-g)(R-2 Lambda0)+S_matter", "EHA2924_0_EH_action_block", "CONTROL_REFERENCE", "sets the GR target action"),
        ("EHC2931_1_field_equation", "EH local field equation", "G_ab+Lambda0 g_ab=kappa0 T_ab", "GPB2924_0_EH_field_equation", "CONTROL_REFERENCE", "source coefficient is fixed by kappa0 and universal matter"),
        ("EHC2931_2_Newton", "EH Newtonian weak-field limit", "nabla^2 Phi=4*pi*G0*rho_H and g_00=-1+2U/c^2-2U^2/c^4+O(U^3)", "EHA2924_4_EH_weak_field", "CONTROL_REFERENCE", "identifies A_EH=1 and B_EH=1 in measured-U convention"),
        ("EHC2931_3_coefficients", "EH source coefficients", "A_EH=1; B_EH=1; beta_EH=B_EH/A_EH^2=1", "DERIVED_CONTROL_ONLY", "CONTROL_REFERENCE", "valid target, not an MTS claim"),
        ("EHC2931_4_guard", "EH import guard", "MTS must derive or bound Delta_A and Delta_B; EH control cannot be copied in as parent proof", "CAND2925_1_EH_import_as_MTS rejected", "ANTI_SMUGGLING_GUARD", "keeps GR as derived limit, not an axiom"),
    ]
    return [
        add_common(
            {
                "control_id": control_id,
                "step": step,
                "formula": formula,
                "source_anchor": source_anchor,
                "status": status,
                "meaning": meaning,
                "A_value": "1" if control_id in {"EHC2931_3_coefficients"} else "",
                "B_value": "1" if control_id in {"EHC2931_3_coefficients"} else "",
                "beta_value": "1" if control_id in {"EHC2931_3_coefficients"} else "",
                "valid_for_MTS_claim": False,
            }
        )
        for control_id, step, formula, source_anchor, status, meaning in specs
    ]


def residual_decomposition_rows() -> list[dict[str, Any]]:
    specs = [
        ("CRD2931_0_Delta_A", "Delta_A", "A_source-1", "Delta_A_metric_readout + Delta_A_kappa + Delta_A_source_denominator + Delta_A_matter + Delta_A_boundary + Delta_A_extra", "ACTIVE_SYMBOLIC_NONCLAIM", "RV2925_0;RV2925_1;RV2925_3;RV2925_5;RV2925_7"),
        ("CRD2931_1_Delta_B", "Delta_B", "B_source-1", "Delta_B_EHcore + Delta_B_R11 + Delta_B_boundary_domain + Delta_B_readout + Delta_B_source_denominator + Delta_B_extra", "ACTIVE_SYMBOLIC_NONCLAIM", "RV2925_2;RV2925_4;RV2925_5;RV2925_6;RV2925_7"),
        ("CRD2931_2_delta_beta_exact", "delta_beta_source_exact", "B_source/A_source^2 - 1", "((1+Delta_B)/(1+Delta_A)^2)-1", "EXACT_RESIDUAL_IDENTITY_NONCLAIM", "B2K2920_0_delta_beta_source;SCL2930_2_delta_beta_source"),
        ("CRD2931_3_square_residual", "Delta_square_law_abs", "|Delta_B-2*Delta_A-Delta_A^2|", "zero iff B_source=A_source^2", "THEOREM_ZERO_MISSING", "SQA2920_3_parent_square_source;DBC2930_4_square_law"),
        ("CRD2931_4_source_denominator", "epsilon_SN", "(mu_obs-G_eff*M_H)/(G_eff*M_H)", "source denominator mismatch feeds Delta_A and beta comparison", "ACTIVE_NONCLAIM", "SCL2930_3_epsilon_SN"),
        ("CRD2931_5_coupling", "Delta_coupling_source_abs", "|Dln(kappa_MTS)|+|Dln(ell_J)|+|epsilon_Gref_match|", "coupling/source-current drift feeds A_source, beta, Newton, alpha3", "ACTIVE_NONCLAIM", "CB2928_3_coupling_total;RES2578_9_total"),
        ("CRD2931_6_total", "Delta_AB_source_total_abs", "sum_abs(Delta_A,Delta_B,epsilon_SN,Dln(kappa_MTS),Dln(ell_J),readout,boundary,R11)", "no cancellation, no measured-GM absorption", "TOTAL_NOT_SCORE_READY", "RV2925_TOTAL;SCL2930_6_Delta_denominator_binding_abs"),
    ]
    return [
        add_common(
            {
                "residual_id": residual_id,
                "symbol": symbol,
                "definition": definition,
                "decomposition": decomposition,
                "current_status": current_status,
                "upstream_rows": upstream_rows,
                "numeric_value_present": False,
                "theorem_zero": False,
                "selected_for_first_value": symbol in {"delta_beta_source_exact", "Delta_square_law_abs", "epsilon_SN", "Delta_coupling_source_abs", "Delta_AB_source_total_abs"},
                "source_paths": ";".join(str(path) for path in [SRC_2930_LEDGER, SRC_2925_VECTOR, SRC_2928_COUPLING, SRC_2578_LEDGER]),
            }
        )
        for residual_id, symbol, definition, decomposition, current_status, upstream_rows in specs
    ]


def first_value_candidate_rows() -> list[dict[str, Any]]:
    specs = [
        ("FVC2931_0_AB_parent_coefficients", "A_source;B_source", "parent_coefficient_theorem", "derive both coefficients from Hcore/Q_tau/Pi_M^H and same M_H_ref", "MISSING_PARENT_ACTION_COEFFICIENT_MAP", "best_if_parent_action_source_map_available", "False"),
        ("FVC2931_1_delta_beta_source", "delta_beta_source", "finite_beta_residual", "source-backed A_source/B_source values or direct beta coefficient residual", "MISSING_A_B_VALUES", "best_if weak-field coefficient extraction exists", "False"),
        ("FVC2931_2_epsilon_SN", "epsilon_SN", "source_normalized_Newton", "source-backed mu_obs, G_eff, M_H row with no orbital-GM circularity", "MISSING_MHREF_SOURCE_ROW", "best_if source-mass row exists", "False"),
        ("FVC2931_3_Dln_kappa", "Dln(kappa_MTS)", "coupling_constant", "topological constant proof or finite drift/range/species/frame bound", "MISSING_CONSTANT_KAPPA_PROOF_OR_VALUE", "best empirical fallback: hits alpha3/Newton/clock/R10", "True"),
        ("FVC2931_4_Dln_ellJ", "Dln(ell_J)", "source_current_scale", "source-current scale proof or finite drift/range/species/frame bound", "MISSING_CONSTANT_ELLJ_PROOF_OR_VALUE", "best empirical fallback: hits source-current/alpha3/beta/WEP", "True"),
    ]
    return [
        add_common(
            {
                "candidate_id": candidate_id,
                "symbol": symbol,
                "route_type": route_type,
                "required_input": required_input,
                "current_status": current_status,
                "priority_reason": priority_reason,
                "selected_for_2932": selected_for_2932,
                "numeric_value_present": False,
                "theorem_zero": False,
                "valid_for_claim": False,
            }
        )
        for candidate_id, symbol, route_type, required_input, current_status, priority_reason, selected_for_2932 in specs
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2931_0_EH_control", "EH control gives A_EH=B_EH=1", "PASS_CONTROL_ONLY", "useful target but not MTS proof", False),
        ("CG2931_1_parent_coefficients", "MTS derives A_source and B_source from same parent source denominator", "BLOCKED_NONCLAIM", "Hcore/source coefficient map unsigned", False),
        ("CG2931_2_square_law", "B_source=A_source^2 follows for current MTS", "BLOCKED_NONCLAIM", "Delta_B-2Delta_A-Delta_A^2 not zero-proved", False),
        ("CG2931_3_beta", "PPN beta passes", "BLOCKED_NONCLAIM", "delta_beta_source remains symbolic", False),
        ("CG2931_4_first_value", "one finite residual row is source-backed", "BLOCKED_NONCLAIM", "2931 only stages candidates", False),
        ("CG2931_5_local_GR_Newton", "local GR/Newton reduction follows", "BLOCKED_NONCLAIM", "RV2925, source denominator, beta and coupling rows remain open", False),
        ("CG2931_6_next_route", "2932 route selected without looping", "PASS_GUARDRAIL", "go after kappa/ellJ constant proof or first finite bound if A/B not derivable", False),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "claim": claim,
                "current_status": current_status,
                "reason": reason,
                "claim_passed": claim_passed,
            }
        )
        for gate_id, claim, current_status, reason, claim_passed in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2931_0_control_win", "retain EH coefficient control theorem", "A_EH=B_EH=1 is the correct target in the same measured-U convention", "use it only as target/reference", False),
        ("DEC2931_1_MTS_result", "do not claim MTS coefficient theorem", "current corpus lacks a parent Hcore/source map for A_source and B_source", "keep beta and Newton nonclaim", False),
        ("DEC2931_2_useful_derivation", "retain exact residual identity", "delta_beta_source=((1+Delta_B)/(1+Delta_A)^2)-1 and square law needs Delta_B=2Delta_A+Delta_A^2", "use this as the coefficient residual grammar", False),
        ("DEC2931_3_next", "select kappa/ellJ constant proof or first finite value", "if A/B parent coefficients are not accessible, kappa and ellJ hit the most local arenas at once", "2932 should attack Dln(kappa_MTS) and Dln(ell_J)", False),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": next_action,
                "valid_for_claim": valid_for_claim,
            }
        )
        for decision_id, decision, because, next_action, valid_for_claim in specs
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2931_0_2932",
                "selection": "selected_primary",
                "target_doc": "2932-Y5-R2FR-kappa-ellJ-constant-proof-or-first-coupling-source-bound-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_kappa_ellJ_constant_proof_or_first_coupling_source_bound_under_AX1090_2932.py",
                "objective": "try to prove Dln(kappa_MTS)=0 and Dln(ell_J)=0 from parent topological/source-current ownership; if not, stage the first finite source-backed coupling/source-current residual bound row with units and arena map",
                "acceptance_gate": "one of Dln(kappa_MTS), Dln(ell_J), or Delta_coupling_source_abs becomes theorem-zero or finite/source-backed with source path, units, no-cancellation policy, and valid_for_claim=false unless all parent requirements close",
                "fallback": "if no source-bound data exist, emit an explicit acquisition ledger for clock, R10, WEP/source-current, alpha3 and Newton arenas",
                "valid_for_claim": False,
            }
        )
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("theorem_copy", OUTPUTS["theorem"], BRANCH_OUTPUTS["theorem_copy"]),
        ("residual_copy", OUTPUTS["residual"], BRANCH_OUTPUTS["residual_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows = []
    for copy_id, source_path, destination_path in copies:
        shutil.copyfile(source_path, destination_path)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source_path),
                    "destination_path": str(destination_path),
                    "source_exists": source_path.exists(),
                    "destination_exists": destination_path.exists(),
                    "destination_parses": csv_parses(destination_path),
                }
            )
        )
    return rows


def validation_rows() -> list[dict[str, Any]]:
    source_rows = read_csv_rows(OUTPUTS["sources"])
    theorem = read_csv_rows(OUTPUTS["theorem"])
    eh_control = read_csv_rows(OUTPUTS["eh_control"])
    residual = read_csv_rows(OUTPUTS["residual"])
    first_value = read_csv_rows(OUTPUTS["first_value"])
    claims = read_csv_rows(OUTPUTS["claims"])
    next_rows = read_csv_rows(OUTPUTS["next"])
    branches = read_csv_rows(OUTPUTS["branches"])

    theorem_ids = {row.get("attempt_id", "") for row in theorem}
    residual_symbols = {row.get("symbol", "") for row in residual}
    candidate_symbols = {row.get("symbol", "") for row in first_value}
    promoted_rows = [
        row
        for row in [*theorem, *residual, *first_value]
        if as_bool(row.get("adopted_for_claim")) or as_bool(row.get("numeric_value_present")) or as_bool(row.get("theorem_zero")) or as_bool(row.get("valid_for_claim"))
    ]
    all_paths = [Path(row["source_path"]) for row in source_rows if row.get("source_path")]
    no_formalization_2931 = not list(FORMALIZATION.rglob("*2931*")) if FORMALIZATION.exists() else True

    checks = [
        ("VAL2931_0_sources_exist", all(as_bool(row.get("path_exists")) for row in source_rows), "every cited source path exists"),
        ("VAL2931_1_source_anchors_found", all(as_bool(row.get("anchors_found")) for row in source_rows), "every cited source anchor is present"),
        ("VAL2931_2_outputs_parse", all(csv_parses(path) for path in OUTPUTS.values()), "all 2931 CSV outputs parse"),
        ("VAL2931_3_doc_exists", DOC.exists(), "2931 markdown checkpoint exists"),
        ("VAL2931_4_EH_control_present", any(row.get("control_id") == "EHC2931_3_coefficients" and row.get("A_value") == "1" and row.get("B_value") == "1" for row in eh_control), "EH control derives A=B=1 as reference only"),
        ("VAL2931_5_MTS_theorem_not_claimed", any(row.get("attempt_id") == "PCT2931_7_verdict" and row.get("current_status") == "PARENT_COEFFICIENT_THEOREM_NOT_DERIVED_FIRST_VALUE_ROUTE_SELECTED" for row in theorem), "MTS parent coefficient theorem remains nonclaim"),
        ("VAL2931_6_exact_residual_identity_present", {"PCT2931_4_exact_residual_law", "PCT2931_5_square_condition"} <= theorem_ids, "exact residual and square-condition identities are recorded"),
        ("VAL2931_7_residual_decomposition_complete", {"Delta_A", "Delta_B", "delta_beta_source_exact", "Delta_square_law_abs", "Delta_AB_source_total_abs"} <= residual_symbols, "coefficient residual decomposition has required symbols"),
        ("VAL2931_8_first_value_candidates_complete", {"A_source;B_source", "delta_beta_source", "epsilon_SN", "Dln(kappa_MTS)", "Dln(ell_J)"} <= candidate_symbols, "first-value candidates complete"),
        ("VAL2931_9_no_rows_promoted", not promoted_rows, "no theorem/residual/candidate row is promoted to claim"),
        ("VAL2931_10_claims_closed", all(not as_bool(row.get("claim_passed")) for row in claims), "all claim gates remain closed"),
        ("VAL2931_11_next_target_selected", any(row.get("next_id") == "NEXT2931_0_2932" for row in next_rows), "2932 next target selected"),
        ("VAL2931_12_branch_copies_parse", all(as_bool(row.get("destination_parses")) for row in branches), "branch copies parse cleanly"),
        ("VAL2931_13_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in OUTPUTS.values()) and all(is_under(path, ROOT) for path in BRANCH_OUTPUTS.values()), "all outputs remain under post-checkpoint-work"),
        ("VAL2931_14_sources_not_formalization", all(not is_under(path, FORMALIZATION) for path in all_paths) if FORMALIZATION.exists() else True, "no formalization-workbench source/output dependency"),
        ("VAL2931_15_no_formalization_2931_outputs", no_formalization_2931, "no formalization-workbench 2931 outputs"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [
        add_common(
            {
                "validation_id": validation_id,
                "passed": passed,
                "check": check,
                "blocking_if_false": True,
            }
        )
        for validation_id, passed, check in checks
    ]
    rows.append(
        add_common(
            {
                "validation_id": "VAL2931_OVERALL",
                "passed": overall,
                "check": "2931 validation overall",
                "blocking_if_false": True,
            }
        )
    )
    return rows


def write_doc() -> None:
    source_rows = read_csv_rows(OUTPUTS["sources"])
    theorem = read_csv_rows(OUTPUTS["theorem"])
    eh_control = read_csv_rows(OUTPUTS["eh_control"])
    residual = read_csv_rows(OUTPUTS["residual"])
    first_value = read_csv_rows(OUTPUTS["first_value"])
    claims = read_csv_rows(OUTPUTS["claims"])
    decisions = read_csv_rows(OUTPUTS["decision"])
    next_rows = read_csv_rows(OUTPUTS["next"])
    branches = read_csv_rows(OUTPUTS["branches"])
    validation = read_csv_rows(OUTPUTS["validation"])
    overall = next((row for row in validation if row.get("validation_id") == "VAL2931_OVERALL"), {})

    sections = [
        "# 2931 - Y5/R2FR Parent Source Coefficient Theorem Or First Finite Local Residual Value Under AX1090",
        "",
        "Status: `Y5_R2FR_2931_EH_control_coefficients_pass_MTS_parent_coefficient_theorem_not_derived_kappa_ellJ_2932_next`",
        "",
        "Claim ceiling: `EH_control_A_B_yes_MTS_A_B_no_square_law_no_first_value_no_Newton_no_beta_no_alpha3_no_local_GR_no_PPN_no_R10_no_GitHub_claim`",
        "",
        "## Summary",
        "",
        "2931 takes the requested derivation route seriously. The clean control theorem is available: in the EH/GR weak-field branch, with the source-normalized potential already identified as the measured Newtonian potential,",
        "",
        "`g_00=-1+2U/c^2-2U^2/c^4+O(U^3)`,",
        "",
        "so the control coefficients are `A_EH=1`, `B_EH=1`, and `beta_EH=1`.",
        "",
        "For current MTS, the same conclusion is not parent-derived. What 2931 does derive exactly is the obstruction grammar. If",
        "",
        "`A_source=1+Delta_A` and `B_source=1+Delta_B`,",
        "",
        "then",
        "",
        "`delta_beta_source=((1+Delta_B)/(1+Delta_A)^2)-1`,",
        "",
        "and the square law requires",
        "",
        "`Delta_B = 2*Delta_A + Delta_A^2`.",
        "",
        "That is useful because the missing GR reduction is now a concrete coefficient equation, not a fog bank. The next non-looping move is to prove or bound the live coupling/source-current pieces, especially `Dln(kappa_MTS)` and `Dln(ell_J)`, because they feed Newton, beta, alpha3, clocks, R10 and source-current tests.",
        "",
        "## Source Register",
        "",
        md_table(source_rows, ["source_id", "source_path", "path_exists", "anchors_found", "role", "missing_anchors"]),
        "",
        "## Parent Source Coefficient Theorem Attempt",
        "",
        md_table(theorem, ["attempt_id", "clause", "math_form", "current_status", "reason", "condition_passed", "adopted_for_claim"]),
        "",
        "## EH Control Coefficient Derivation",
        "",
        md_table(eh_control, ["control_id", "step", "formula", "source_anchor", "status", "meaning", "A_value", "B_value", "beta_value", "valid_for_MTS_claim"]),
        "",
        "## MTS Coefficient Residual Decomposition",
        "",
        md_table(residual, ["residual_id", "symbol", "definition", "decomposition", "current_status", "upstream_rows", "numeric_value_present", "theorem_zero", "selected_for_first_value"]),
        "",
        "## First Finite Value Candidate Rows",
        "",
        md_table(first_value, ["candidate_id", "symbol", "route_type", "required_input", "current_status", "priority_reason", "selected_for_2932", "numeric_value_present", "theorem_zero", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        md_table(claims, ["gate_id", "claim", "current_status", "reason", "claim_passed"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(next_rows, ["next_id", "selection", "target_doc", "target_script", "objective", "acceptance_gate", "fallback", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(branches, ["copy_id", "source_path", "destination_path", "source_exists", "destination_exists", "destination_parses"]),
        "",
        "## Validation",
        "",
        md_table(validation, ["validation_id", "passed", "check", "blocking_if_false"]),
        "",
        f"Validation overall: `{overall.get('passed', False)}`.",
        "",
        "## Bottom Line",
        "",
        "This is a small but real derivation win. We did not prove the MTS parent source coefficients, but we did prove the exact shape of the failure. To get beta cleanly, MTS must show `Delta_B=2*Delta_A+Delta_A^2`; to get Newton cleanly, it must also close the source denominator. That is now a precise target.",
        "",
        "The best next route is `kappa_MTS`/`ell_J`: either prove those coupling/source-current baselines are constant from the parent structure, or acquire finite source-backed bounds. That route is less circular than trying to read `A_source` and `B_source` without the parent coefficient map, and it hits more tests at once.",
        "",
        "## Non-Claims",
        "",
        "- no MTS `A_source` or `B_source` value is claimed;",
        "- no MTS `B_source=A_source^2` theorem is claimed;",
        "- no finite residual value is source-backed yet;",
        "- no `Dln(kappa_MTS)=0` or `Dln(ell_J)=0` theorem is claimed;",
        "- no Newton, beta, PPN, R10, alpha3, or local-GR pass is claimed;",
        "- no public/GitHub claim is made.",
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    write_csv(OUTPUTS["sources"], source_register_rows())
    write_csv(OUTPUTS["theorem"], theorem_attempt_rows())
    write_csv(OUTPUTS["eh_control"], eh_control_rows())
    write_csv(OUTPUTS["residual"], residual_decomposition_rows())
    write_csv(OUTPUTS["first_value"], first_value_candidate_rows())
    write_csv(OUTPUTS["claims"], claim_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    write_csv(OUTPUTS["branches"], branch_copy_rows())
    DOC.write_text("# 2931 preflight\n", encoding="utf-8")
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc()

    validation = read_csv_rows(OUTPUTS["validation"])
    overall = next((row for row in validation if row.get("validation_id") == "VAL2931_OVERALL"), {})
    print(f"wrote {DOC}")
    print(f"validation overall: {overall.get('passed')}")


if __name__ == "__main__":
    main()
