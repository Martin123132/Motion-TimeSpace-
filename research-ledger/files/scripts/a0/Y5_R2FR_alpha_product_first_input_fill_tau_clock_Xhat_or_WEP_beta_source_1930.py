from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
MICROSCOPE_COEFFS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1930"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1930-Y5-R2FR-alpha-product-first-input-fill-tau-clock-Xhat-or-WEP-beta-source.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()

SOURCES = {
    "1929_next": OUT / "P8_Y5_PARENT_QLOC_1929_NEXT_TARGET.csv",
    "1929_doc": ROOT / "1929-Y5-R2FR-parent-TQ-owner-fixed-charge-lattice-and-gauge-norm-signature.md",
    "1929_validation": OUT / "P8_Y5_BRR545_1929_VALIDATION.csv",
    "1929_alpha_fallback": OUT / "P8_Y5_PARENT_QLOC_1929_ALPHA_PRODUCT_FALLBACK_ROWS_NONCLAIM.csv",
    "1102_input_status": OUT / "P8_Y5_R10_1102_ALPHA_PRODUCT_INPUT_STATUS.csv",
    "1102_path_decision": OUT / "P8_Y5_R10_1102_ALPHA_PRODUCT_PATH_DECISION.csv",
    "1102_predictions": OUT / "P8_Y5_R10_1102_ALPHA_PRODUCT_PREDICTION_ATTEMPT_NONCLAIM.csv",
    "1102_bounds": OUT / "P8_Y5_R10_1102_ALPHA_PRODUCT_BOUND_IMPORT.csv",
    "1102_claims": OUT / "P8_Y5_R10_1102_CLAIM_GATES.csv",
    "1102_runner": OUT / "P8_Y5_R10_1102_PRODUCT_RUNNER_STATUS.csv",
    "1102_validation": OUT / "P8_Y5_BRR545_1102_VALIDATION.csv",
    "1102_next": OUT / "P8_Y5_R10_1102_NEXT_TARGET.csv",
    "1103_loop": OUT / "P8_Y5_R10_1103_LOOP_RECONCILIATION.csv",
    "1103_debts": OUT / "P8_Y5_R10_1103_LIVE_DEBT_MATRIX.csv",
    "1103_decisions": OUT / "P8_Y5_R10_1103_DECISION_LEDGER.csv",
    "1103_validation": OUT / "P8_Y5_BRR545_1103_VALIDATION.csv",
    "1103_next": OUT / "P8_Y5_R10_1103_NEXT_TARGET.csv",
}

NEEDLES = {
    "1929_next": ["NEXT1929_0_primary", "alpha-product-first-input"],
    "1929_doc": ["STAT1929_1_route", "VAL1929_OVERALL"],
    "1929_validation": ["VAL1929_OVERALL", "PASS"],
    "1929_alpha_fallback": ["AFP1929_0_clock_alpha_missing_tau", "AFP1929_2_c_alpha_missing"],
    "1102_input_status": ["IN1102_1_tau_clock_Xhat", "IN1102_7_direct_product"],
    "1102_path_decision": ["PATH1102_0_clock", "PATH1102_2_best_next"],
    "1102_predictions": ["PRED1102_0_clock_alpha_bound_not_prediction", "PRED1102_2_c_alpha_DD_threshold_not_prediction"],
    "1102_bounds": ["BOUND1102_0_clock_product", "BOUND1102_2_c_alpha_DD_threshold"],
    "1102_claims": ["CG1102_0_clock_prediction", "CG1102_2_source_label"],
    "1102_runner": ["valid_prediction_rows", "reject product rows"],
    "1102_validation": ["V1102_SUMMARY", "pass"],
    "1102_next": ["NEXT1102_0_1103", "source-label-forgetting"],
    "1103_loop": ["REC1103_0_loop_detected", "REC1103_5_EM_branch_result"],
    "1103_debts": ["DEBT1103_0_parent_ordinary_sector_signature", "DEBT1103_5_hidden_invariants"],
    "1103_decisions": ["DEC1103_0_no_loop", "DEC1103_1_live_edge"],
    "1103_validation": ["V1103_SUMMARY", "pass"],
    "1103_next": ["NEXT1103_0_1104", "parent-ordinary-sector-action-signature"],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1930_SOURCE_REGISTER.csv",
    "input_status": OUT / "P8_Y5_PARENT_QLOC_1930_ALPHA_PRODUCT_INPUT_STATUS_AUDIT.csv",
    "path_decision": OUT / "P8_Y5_PARENT_QLOC_1930_ALPHA_PRODUCT_PATH_DECISION.csv",
    "no_loop": OUT / "P8_Y5_PARENT_QLOC_1930_NO_LOOP_RECONCILIATION.csv",
    "live_debts": OUT / "P8_Y5_PARENT_QLOC_1930_LIVE_DEBT_MATRIX.csv",
    "predictions": OUT / "P8_Y5_PARENT_QLOC_1930_ALPHA_PRODUCT_PREDICTION_ATTEMPT_NONCLAIM.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1930_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1930_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1930_NEXT_TARGET.csv",
    "snapshot": OUT / "P8_Y5_PARENT_QLOC_1930_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1930_VALIDATION.csv",
}

BRANCH_COPIES = [
    (OUTPUTS["input_status"], SOURCE_WEIGHT_DOCS / "ALPHA_PRODUCT_INPUT_STATUS_AUDIT_1930_NONCLAIM.csv"),
    (OUTPUTS["predictions"], MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1930_ALPHA_PRODUCT_PREDICTION_ATTEMPT_NONCLAIM.csv"),
    (OUTPUTS["live_debts"], QUEUE / "JR1930_ORDINARY_SECTOR_SIGNATURE_LIVE_DEBT_QUEUE.csv"),
    (OUTPUTS["claim_gate"], QUARANTINE / "P8_Y5_PARENT_QLOC_1930_CLAIM_GATE.csv"),
]


def ensure_dirs() -> None:
    for path in [OUT, SOURCE_WEIGHT_DOCS, MICROSCOPE_COEFFS, QUEUE, QUARANTINE]:
        path.mkdir(parents=True, exist_ok=True)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, path in SOURCES.items():
        text = read_text(path) if path.exists() else ""
        missing = [needle for needle in NEEDLES[key] if needle not in text]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_key": key,
                "source_path": str(path),
                "needed_for": "1930 alpha product first input fill and no-loop selector",
                "needles": ";".join(NEEDLES[key]),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing else "MISSING_OR_NEEDLE_FAILED",
                "missing_needles": ";".join(missing),
                "valid_for_claim": False,
                "claim_allowed": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def input_status_rows() -> list[dict[str, Any]]:
    specs = [
        ("IN1930_0_clock_product_bound", "clock", "abs(b_alpha*tau_clock_time) bound", "2.1000000000000000e-18", "yr^-1", "SOURCE_BACKED_BOUND_AVAILABLE_NOT_PREDICTION", "tau_clock_time and Xhat/chi_X normalization missing; b_alpha theorem-zero absent"),
        ("IN1930_1_tau_clock_Xhat", "clock", "tau_clock_time / Xhat normalization", "MISSING_PARENT_TAU_CLOCK_XHAT_MAP", "yr^-1 per normalized Xhat unit", "not_filled", "clock product bound cannot become standalone b_alpha or MTS prediction"),
        ("IN1930_2_WEP_material_pair", "MICROSCOPE_WEP", "material pair convention", "TA6V_minus_PtRh10", "dimensionless convention", "filled_for_smoke_only", "full material/source/readout tensor missing"),
        ("IN1930_3_delta_Q_alpha", "MICROSCOPE_WEP", "Delta_Q_alpha_Coulomb_abs", "1.989808886825000e-03", "dimensionless", "filled_for_smoke_only", "source-backed smoke estimate, not full MICROSCOPE material tensor"),
        ("IN1930_4_WEP_product_target", "MICROSCOPE_WEP", "abs(P_WEP_alpha) target", "4.7977805227320001e-05", "dimensionless", "target_filled_not_prediction", "threshold is not an MTS predicted product"),
        ("IN1930_5_beta_source_alpha", "MICROSCOPE_WEP", "beta_source_alpha", "MISSING_PARENT_SOURCE_NORMALIZATION_OWNER", "dimensionless", "not_filled", "cannot set beta_source_alpha to 1 or 0 without source-label/Noether owner theorem"),
        ("IN1930_6_tau_WEP", "MICROSCOPE_WEP", "tau_WEP", "MISSING_LAB_SOURCE_ORBIT_PROJECTION", "dimensionless projection factor", "not_filled", "cannot set tau_WEP to 1; needs local source/orbit/readout map"),
        ("IN1930_7_direct_product", "MICROSCOPE_WEP", "P_WEP_alpha", "MISSING_DIRECT_PARENT_PRODUCT_OR_NUMERIC_VALUE", "dimensionless", "not_filled", "runner must refuse until direct product or all factors are sourced"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "input_id": input_id,
            "arena": arena,
            "input": input_name,
            "value_or_status": value,
            "units": units,
            "filled_status": filled,
            "blocks_claim": blocks,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for input_id, arena, input_name, value, units, filled, blocks in specs
    ]


def path_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "path_id": "PATH1930_0_clock",
            "path": "clock finite-alpha product",
            "available_now": "source-backed product bound |b_alpha*tau_clock_time| <= 2.1e-18 yr^-1",
            "missing": "tau_clock_time; Xhat/chi_X normalization; alpha owner or numeric b_alpha product prediction",
            "decision": "retain as strongest product bound, not a scoreable prediction",
            "next_requirement": "derive tau_clock/Xhat map only after alpha owner or ordinary-sector signature is narrowed",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "path_id": "PATH1930_1_WEP",
            "path": "WEP alpha product",
            "available_now": "MICROSCOPE material smoke pair, Delta_Q_alpha, eta bound, product target",
            "missing": "beta_source_alpha; tau_WEP; direct P_WEP_alpha theorem or numeric value; full material/readout tensor",
            "decision": "best source-normalization physics, but old source-label branch already looped and failed to parent-sign",
            "next_requirement": "synthesize ordinary-sector action signature instead of duplicating source-label branch",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "path_id": "PATH1930_2_no_loop",
            "path": "ordinary-sector parent action signature",
            "available_now": "1103 reconciles source-label loop and live debts",
            "missing": "single signed parent contract covering source weights, no-extra-F2, hidden invariants, constants, tau/readout, and radiative closure",
            "decision": "selected next live edge",
            "next_requirement": "write minimal signed/unsigned ordinary-sector parent action signature ledger",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def no_loop_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "recon_id": "REC1930_0_loop_detected",
            "finding": "1102 next target matches already-built source-label/Noether branch",
            "evidence": "NEXT1102_0_1103 plus 1103 loop reconciliation; older 1063 through 1066 kept parent_signed=false",
            "decision": "do not duplicate the source-label derivation",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "recon_id": "REC1930_1_source_label_result",
            "finding": "source-label forgetting is a clean conditional theorem but not parent-derived",
            "evidence": "REC1103_1_source_label_result",
            "decision": "retain w_A/source-scalar as live coupling debt",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "recon_id": "REC1930_2_tau_WEP_result",
            "finding": "tau_WEP decomposes into source-worldtube/orbit/readout pieces but is not derived",
            "evidence": "REC1103_2_tau_WEP_result",
            "decision": "never set tau_WEP=1",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "recon_id": "REC1930_3_direct_WEP_result",
            "finding": "direct WEP alpha threshold exists but MTS has no direct product prediction",
            "evidence": "REC1103_3_direct_WEP_result; PRED1102_1_WEP_material_target_not_prediction",
            "decision": "thresholds are bound-side pressure only",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "recon_id": "REC1930_4_live_edge",
            "finding": "ordinary constants, source weights, hidden invariants, EM norm, and readout closure are one action-language problem",
            "evidence": "REC1103_4_constant_owner_result; REC1103_5_EM_branch_result",
            "decision": "route to ordinary-sector parent action signature synthesis",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def live_debt_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEBT1930_0_parent_ordinary_sector_signature", "parent_action", "single ordinary-sector owner signature", "GR/Newton source coupling; alpha stability; WEP products; R10 transfer", "NOT_SYNTHESIZED_AS_ONE_SIGNED_PARENT_CONTRACT"),
        ("DEBT1930_1_source_weight", "source_coupling", "parent-derived no w_A / source-scalar exclusion", "beta_source_alpha; relative WEP/source products; measured-G absorption guard", "CONDITIONAL_SOURCE_SCALAR_EXCLUSION_NOT_PARENT_DERIVED"),
        ("DEBT1930_2_EM_alpha", "EM", "unique EM kinetic owner and fixed gauge norm", "b_alpha theorem-zero; standalone clock alpha; WEP/R10 alpha transfer", "GAUGE_NORM_OWNER_NOT_DERIVED"),
        ("DEBT1930_3_tau_clock", "clock", "tau_clock/Xhat normalization", "turning |b_alpha*tau_clock| bound into MTS b_alpha prediction", "BOUND_AVAILABLE_NOT_PREDICTION"),
        ("DEBT1930_4_tau_WEP", "WEP", "tau_WEP source-worldtube/orbit/readout functional", "finite WEP relative-source and alpha products", "PROJECTION_CONTRACT_WRITTEN_NOT_DERIVED"),
        ("DEBT1930_5_hidden_invariants", "operator_domain", "no hidden-visible hom / invariant algebra triviality", "constant-sector universality; scalar F2; source-weight return", "TRIVIALITY_NOT_DERIVED"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "debt_id": debt_id,
            "sector": sector,
            "missing_object": missing,
            "blocks": blocks,
            "best_status": status,
            "best_next": "fold into minimal ordinary-sector parent action signature",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": GENERATED_UTC,
        }
        for debt_id, sector, missing, blocks, status in specs
    ]


def prediction_rows() -> list[dict[str, Any]]:
    specs = [
        ("PRED1930_0_clock_alpha_bound_not_prediction", "clock", "P_clock_alpha", "MISSING_MTS_B_ALPHA_TAU_CLOCK_PREDICTION", "yr^-1", "clock product bound only", "tau_clock_time; Xhat normalization; b_alpha theorem-zero or direct product prediction", "BOUND_AVAILABLE_PREDICTION_MISSING"),
        ("PRED1930_1_WEP_material_target_not_prediction", "MICROSCOPE_WEP", "P_WEP_alpha", "MISSING_PARENT_DERIVED_BETA_SOURCE_ALPHA_B_ALPHA_TAU_WEP_PRODUCT", "dimensionless", "Delta_Q_alpha; eta_bound; WEP product target", "beta_source_alpha; tau_WEP; b_alpha or direct P_WEP_alpha theorem", "MATERIAL_TARGET_FILLED_PRODUCT_MISSING"),
        ("PRED1930_2_c_alpha_DD_threshold_not_prediction", "MICROSCOPE_WEP", "c_alpha_DD", "MISSING_SOURCE_BACKED_C_ALPHA_OR_THEOREM_ZERO", "dimensionless", "DD alpha threshold only", "source-backed c_alpha_DD value or signed zero theorem", "THRESHOLD_AVAILABLE_COEFFICIENT_MISSING"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "prediction_id": prediction_id,
            "arena": arena,
            "product_symbol": symbol,
            "product_value": value,
            "product_units": units,
            "inputs_present": inputs_present,
            "required_inputs": required,
            "derivation_status": status,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for prediction_id, arena, symbol, value, units, inputs_present, required, status in specs
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1930_0_clock_prediction",
            "requirement": "clock alpha product is predicted by MTS",
            "status": "FAIL_TAU_CLOCK_XHAT_AND_PRODUCT_MISSING",
            "evidence": "IN1930_1_tau_clock_Xhat; PRED1930_0_clock_alpha_bound_not_prediction",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1930_1_WEP_product",
            "requirement": "WEP alpha product is predicted by MTS",
            "status": "FAIL_BETA_TAU_DIRECT_PRODUCT_MISSING",
            "evidence": "IN1930_5_beta_source_alpha; IN1930_6_tau_WEP; IN1930_7_direct_product",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1930_2_no_loop",
            "requirement": "next target avoids duplicating source-label/Noether branch",
            "status": "PASS_NO_LOOP_ROUTE_SELECTED_NONCLAIM",
            "evidence": "REC1930_0_loop_detected; PATH1930_2_no_loop",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1930_3_product_runner",
            "requirement": "product runner has valid predictions",
            "status": "FAIL_VALID_PREDICTION_ROWS_ZERO",
            "evidence": "PRED1930_0_clock_alpha_bound_not_prediction through PRED1930_2_c_alpha_DD_threshold_not_prediction",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1930_4_alpha_claim",
            "requirement": "alpha sector supports local-GR/WEP/R10/clock claim",
            "status": "CLAIM_BLOCKED",
            "evidence": "CG1930_0_clock_prediction; CG1930_1_WEP_product; CG1930_3_product_runner",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1930_0_input_fill_result",
            "decision": "NO_SCOREABLE_ALPHA_PRODUCT_YET",
            "why": "clock has a source-backed bound but not a prediction; WEP has material/target rows but beta_source_alpha, tau_WEP, and direct product are missing",
            "next_action": "do not claim alpha products; retain target rows as pressure tests",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1930_1_no_loop_result",
            "decision": "DO_NOT_DUPLICATE_SOURCE_LABEL_BRANCH",
            "why": "1103 shows the source-label/Noether route already loops back to old 1063-1066 attempts",
            "next_action": "synthesize a minimal ordinary-sector parent action signature instead",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1930_2_next_route",
            "decision": "MOVE_TO_ORDINARY_SECTOR_PARENT_ACTION_SIGNATURE",
            "why": "source weight, no-extra-F2, hidden invariant, mass/binding, tau/readout, and radiative debts are one coupled action-language problem",
            "next_action": "1931 should write the minimal ordinary-sector signature and mark derivable vs closure clauses",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1930_0_primary",
            "selection_status": "selected",
            "target_doc": "1931-Y5-R2FR-parent-ordinary-sector-action-signature-or-explicit-closure-ledger.md",
            "target_script": "scripts/Y5_R2FR_parent_ordinary_sector_action_signature_or_explicit_closure_ledger_1931.py",
            "objective": "synthesize source-weight, EM gauge-norm, hidden-invariant, mass/binding, clock/readout, and radiative clauses into one minimal ordinary-sector parent action signature; mark derivable, closure, and blocked clauses",
            "success_condition": "a minimal parent ordinary-sector signature ledger that separates signed theorems from explicit closures and keeps WEP/R10/clock claims blocked where closure remains",
            "do_not": "do not rerun source-label loop, set tau=1, use standalone b_alpha, absorb relative weights into measured G, invent coefficients, or make public/local-GR claims",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
    ]


def snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "STAT1930_0_gain",
            "area": "alpha product testing",
            "summary": "1930 confirms the current alpha products are target/bound rows only: clock bound exists, WEP material target exists, but no MTS prediction row exists.",
            "status": "TARGETS_READY_PREDICTION_MISSING",
            "what_it_means": "we can pressure-test future coefficients, but cannot score or claim today",
            "next": "ordinary-sector parent action signature",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "STAT1930_1_no_loop",
            "area": "route control",
            "summary": "1930 prevents a source-label loop and promotes the broader parent-action signature as the live edge.",
            "status": "NO_LOOP_SYNTHESIS_SELECTED",
            "what_it_means": "we stop slicing the same coupling wound into separate repeats",
            "next": "minimal ordinary-sector contract",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "input_status": input_status_rows(),
        "path_decision": path_decision_rows(),
        "no_loop": no_loop_rows(),
        "live_debts": live_debt_rows(),
        "predictions": prediction_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "snapshot": snapshot_rows(),
    }


def copy_branch_artifacts() -> None:
    for source, destination in BRANCH_COPIES:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)


def validation_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    sources = parse_csv(OUTPUTS["source_register"])
    rows.append({"validation_id": "VAL1930_00_sources", "status": "PASS" if all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources) else "FAIL", "detail": "all local source paths exist and needles found", "valid_for_claim": False, "claim_allowed": False})
    inputs = parse_csv(OUTPUTS["input_status"])
    rows.append({"validation_id": "VAL1930_01_input_status", "status": "PASS" if len(inputs) == 8 and any(row["value_or_status"] == "MISSING_PARENT_TAU_CLOCK_XHAT_MAP" for row in inputs) and any(row["value_or_status"] == "MISSING_PARENT_SOURCE_NORMALIZATION_OWNER" for row in inputs) else "FAIL", "detail": "alpha input status records clock and WEP blockers", "valid_for_claim": False, "claim_allowed": False})
    predictions = parse_csv(OUTPUTS["predictions"])
    rows.append({"validation_id": "VAL1930_02_predictions_missing", "status": "PASS" if len(predictions) == 3 and all(row["valid_prediction_row"] == "False" and row["product_value"].startswith("MISSING") for row in predictions) else "FAIL", "detail": "all alpha prediction rows remain missing/nonclaim", "valid_for_claim": False, "claim_allowed": False})
    no_loop = parse_csv(OUTPUTS["no_loop"])
    rows.append({"validation_id": "VAL1930_03_no_loop", "status": "PASS" if any(row["recon_id"] == "REC1930_0_loop_detected" for row in no_loop) and any(row["recon_id"] == "REC1930_4_live_edge" for row in no_loop) else "FAIL", "detail": "source-label loop detected and ordinary-sector live edge selected", "valid_for_claim": False, "claim_allowed": False})
    debts = parse_csv(OUTPUTS["live_debts"])
    rows.append({"validation_id": "VAL1930_04_live_debts", "status": "PASS" if len(debts) == 6 and any(row["debt_id"] == "DEBT1930_0_parent_ordinary_sector_signature" for row in debts) else "FAIL", "detail": "six live debts recorded for ordinary-sector signature", "valid_for_claim": False, "claim_allowed": False})
    gates = parse_csv(OUTPUTS["claim_gate"])
    local_gate = next(row for row in gates if row["gate_id"] == "CG1930_4_alpha_claim")
    no_loop_gate = next(row for row in gates if row["gate_id"] == "CG1930_2_no_loop")
    rows.append({"validation_id": "VAL1930_05_claim_gate", "status": "PASS" if local_gate["status"] == "CLAIM_BLOCKED" and no_loop_gate["status"] == "PASS_NO_LOOP_ROUTE_SELECTED_NONCLAIM" else "FAIL", "detail": "alpha claims blocked and no-loop route selected as nonclaim", "valid_for_claim": False, "claim_allowed": False})
    decisions = parse_csv(OUTPUTS["decision"])
    rows.append({"validation_id": "VAL1930_06_decision", "status": "PASS" if any(row["decision"] == "MOVE_TO_ORDINARY_SECTOR_PARENT_ACTION_SIGNATURE" for row in decisions) else "FAIL", "detail": "ordinary-sector signature route selected", "valid_for_claim": False, "claim_allowed": False})
    next_rows = parse_csv(OUTPUTS["next_target"])
    rows.append({"validation_id": "VAL1930_07_next_target", "status": "PASS" if next_rows[0]["target_doc"].startswith("1931-Y5-R2FR-parent-ordinary-sector") else "FAIL", "detail": "1931 ordinary-sector parent action signature target selected", "valid_for_claim": False, "claim_allowed": False})
    generated = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_ok = True
    claim_safe = True
    for path in generated:
        try:
            parsed = parse_csv(path)
            csv_ok = csv_ok and bool(parsed)
            for row in parsed:
                if row.get("valid_for_claim", "False") != "False" or row.get("claim_allowed", "False") != "False":
                    claim_safe = False
        except Exception:
            csv_ok = False
    rows.append({"validation_id": "VAL1930_08_claim_flags_safe", "status": "PASS" if claim_safe else "FAIL", "detail": "claim flags all false", "valid_for_claim": False, "claim_allowed": False})
    rows.append({"validation_id": "VAL1930_09_csv_parse", "status": "PASS" if csv_ok else "FAIL", "detail": "all generated CSVs parse with rows", "valid_for_claim": False, "claim_allowed": False})
    rows.append({"validation_id": "VAL1930_10_branch_copies", "status": "PASS" if all(destination.exists() for _, destination in BRANCH_COPIES) else "FAIL", "detail": "; ".join(str(destination) for _, destination in BRANCH_COPIES), "valid_for_claim": False, "claim_allowed": False})
    pycache = ROOT / "scripts" / "__pycache__"
    rows.append({"validation_id": "VAL1930_11_pycache_absent", "status": "PASS" if not pycache.exists() else "FAIL", "detail": str(pycache), "valid_for_claim": False, "claim_allowed": False})
    formalization_count = 0
    if FORMALIZATION.exists():
        formalization_count = sum(1 for path in FORMALIZATION.rglob("*") if path.name.startswith("1930-") or "_1930" in path.name or "1930_" in path.name or "Y5_R2FR_alpha_product" in path.name)
    rows.append({"validation_id": "VAL1930_12_formalization_untouched", "status": "PASS" if formalization_count == 0 else "FAIL", "detail": f"formalization_1930_artifact_count={formalization_count}", "valid_for_claim": False, "claim_allowed": False})
    overall = all(row["status"] == "PASS" for row in rows)
    rows.append({"validation_id": "VAL1930_OVERALL", "status": "PASS" if overall else "FAIL", "detail": "1930 alpha product first input fill and no-loop selector", "valid_for_claim": False, "claim_allowed": False})
    return rows


def markdown_table(rows: list[dict[str, Any]]) -> str:
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers) + " |")
    return "\n".join(lines)


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = validation_rows()
    content = f"""# 1930 - Alpha Product First Input Fill Tau Clock Xhat Or WEP Beta Source

## Purpose

This checkpoint tries to make the finite alpha branch scoreable by filling the first missing input: either clock `tau_clock/Xhat` normalization or WEP `beta_source_alpha/tau_WEP/material` projection. It also checks whether the selected source-label route would duplicate already-failed work.

## Result

- No scoreable alpha product exists yet.
- The clock route has a strong source-backed bound, but not an MTS prediction.
- The WEP route has material/target smoke inputs, but beta/source, tau_WEP, and direct product are missing.
- The source-label/Noether route is a loop back to already-attempted 1063-1066 work.
- The live edge is now a minimal ordinary-sector parent action signature that covers source weights, no-extra-F2, hidden invariants, constants, tau/readout, and radiative closure together.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Alpha Product Input Status Audit

{markdown_table(rows_by_name["input_status"])}

## Alpha Product Path Decision

{markdown_table(rows_by_name["path_decision"])}

## No-Loop Reconciliation

{markdown_table(rows_by_name["no_loop"])}

## Live Debt Matrix

{markdown_table(rows_by_name["live_debts"])}

## Alpha Product Prediction Attempt

{markdown_table(rows_by_name["predictions"])}

## Claim Gate

{markdown_table(rows_by_name["claim_gate"])}

## Decision Ledger

{markdown_table(rows_by_name["decision"])}

## Next Target

{markdown_table(rows_by_name["next_target"])}

## Project Status Snapshot

{markdown_table(rows_by_name["snapshot"])}

## Validation

{markdown_table(validation)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    remove_pycache()
    rows_by_name = build_rows()
    for key, rows in rows_by_name.items():
        write_csv(OUTPUTS[key], rows)
    copy_branch_artifacts()
    remove_pycache()
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()
