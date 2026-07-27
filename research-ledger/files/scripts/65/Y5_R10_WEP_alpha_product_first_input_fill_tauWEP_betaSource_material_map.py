from __future__ import annotations

import csv
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from Y5_R10_alpha_product_prediction_stub_runner_and_required_inputs import (
    BOUND_REQUIRED_COLUMNS,
    PRODUCT_REQUIRED_COLUMNS,
    run_product_runner,
)


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1061-Y5-R10-WEP-alpha-product-first-input-fill-tauWEP-betaSource-material-map.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1061-WEP-alpha-product-first-input-fill" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_ATTEMPT = OUT / "P8_Y5_R10_1061_ALPHA_PRODUCT_PREDICTION_ATTEMPT_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1061_ALPHA_PRODUCT_BOUND_IMPORT.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def float_or_none(value: object) -> float | None:
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return None


def find_row(path: Path, key: str, value: str) -> dict[str, str]:
    for row in read_csv(path):
        if row.get(key) == value:
            return row
    return {}


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1061_0_1060_next", "source-intake/mts_residuals/P8_Y5_R10_1060_NEXT_TARGET.csv", "1061-Y5-R10-WEP-alpha-product-first-input-fill", "1060 handoff selecting WEP alpha product input fill."),
        ("SRC1061_1_1060_required", "source-intake/mts_residuals/P8_Y5_R10_1060_REQUIRED_INPUTS.csv", "REQ1060_1_WEP_alpha", "WEP alpha required inputs."),
        ("SRC1061_2_1060_prediction_template", "source-intake/mts_residuals/P8_Y5_R10_1060_ALPHA_PRODUCT_PREDICTION_TEMPLATE_NONCLAIM.csv", "PRED1060_1_WEP_alpha_template", "prior placeholder prediction row."),
        ("SRC1061_3_1060_bound", "source-intake/mts_residuals/P8_Y5_R10_1060_ALPHA_PRODUCT_BOUND_IMPORT.csv", "BOUND1060_1_WEP_alpha", "prior WEP product target bound import."),
        ("SRC1061_4_1059_pack", "source-intake/mts_residuals/P8_Y5_R10_1059_ALPHA_PRODUCT_PRIOR_PACK.csv", "APP1059_2_WEP_alpha_Coulomb", "alpha product prior pack row."),
        ("SRC1061_5_650_screen_rule", "source-intake/mts_residuals/P8_Y5_R10_650_ULTRA_SCREENED_RULE.csv", "USR650_0_shared_screen_variable", "shared local alpha screen rule."),
        ("SRC1061_6_650_cross_arena", "source-intake/mts_residuals/P8_Y5_R10_650_CROSS_ARENA_CONTRACT.csv", "R0_R1_WEP", "cross-arena WEP projection contract."),
        ("SRC1061_7_651_stress", "source-intake/mts_residuals/P8_Y5_R10_651_WEP_ALPHA_STRESS_TEST.csv", "WAS651_0_alpha_Coulomb", "WEP alpha/Coulomb stress-test target."),
        ("SRC1061_8_983_web", "source-intake/mts_residuals/P8_Y5_R10_983_WEB_SOURCE_REGISTER.csv", "WEB983_0_MICROSCOPE_CQG_COMPOSITION", "MICROSCOPE material composition source."),
        ("SRC1061_9_983_delta", "source-intake/mts_residuals/P8_Y5_R10_983_DIFFERENTIAL_PROXY_VECTOR.csv", "DEL983_coulomb_proxy", "MICROSCOPE proxy material contrast."),
        ("SRC1061_10_1053_matrix", "source-intake/mts_residuals/P8_Y5_R10_1053_WEP_COMPOSITION_CHARGE_MATRIX.csv", "WCM1053_4", "alpha/Coulomb differential charge row."),
        ("SRC1061_11_988_pressure", "source-intake/mts_residuals/P8_Y5_R10_988_WEP_ALPHA_PRESSURE_IMPORT.csv", "WEP988_WAS651_0_alpha_Coulomb", "pressure target imported after alpha screen policy."),
        ("SRC1061_12_1052_WEP", "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv", "AWP1052_0_alpha_Coulomb", "WEP alpha projection ledger."),
        ("SRC1061_13_1053_beta", "source-intake/mts_residuals/P8_Y5_R10_1053_BETA_SOURCE_ALPHA_DERIVATION_AUDIT.csv", "BSA1053_1_alpha_marker_source", "beta_source_alpha derivation audit."),
        ("SRC1061_14_1053_tau", "source-intake/mts_residuals/P8_Y5_R10_1053_TAU_WEP_R10_PROJECTION_AUDIT.csv", "TPR1053_1_tau_WEP_definition", "tau_WEP derivation audit."),
        ("SRC1061_15_989_owner", "source-intake/mts_residuals/P8_Y5_R10_989_BETA_SOURCE_OWNER_LEDGER.csv", "BSO989_0_definition", "beta source owner ledger."),
        ("SRC1061_16_990_contract", "source-intake/mts_residuals/P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv", "PAC990_3_EM_lock", "parent action EM/source-normalization contract."),
        ("SRC1061_17_local_bound", "source-intake/local_bounds/local_bound_claims.csv", "R1_WEP_source_charge", "MICROSCOPE WEP bound anchor."),
    ]
    rows: list[dict[str, str]] = []
    for source_id, rel_path, needle, note in specs:
        path = source_path(rel_path)
        exists = path.exists()
        needle_found = exists and needle in read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "relative_path": rel_path,
                "absolute_path": str(path),
                "exists": str(exists).lower(),
                "needle": needle,
                "needle_found": str(needle_found).lower(),
                "note": note,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def material_convention_rows() -> list[dict[str, str]]:
    matrix = find_row(OUT / "P8_Y5_R10_1053_WEP_COMPOSITION_CHARGE_MATRIX.csv", "matrix_id", "WCM1053_4")
    pressure = find_row(OUT / "P8_Y5_R10_988_WEP_ALPHA_PRESSURE_IMPORT.csv", "import_id", "WEP988_WAS651_0_alpha_Coulomb")
    bound = find_row(ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv", "row_id", "R1_WEP_source_charge")
    delta_q_abs = matrix.get("delta_Q_abs_for_pair") or pressure.get("delta_Q_abs", "")
    eta_bound = pressure.get("eta_bound_used") or bound.get("upper_bound", "")
    unit_source_eta = pressure.get("unit_source_eta_prediction", "")
    target = pressure.get("required_abs_beta_source_max", "")
    rows = [
        {
            "convention_id": "MCON1061_0_test_pair",
            "object": "MICROSCOPE Ti/Pt test-pair convention",
            "definition": "TA6V outer test mass minus PtRh10 inner test mass; eta_AB uses the same sign convention as the 983/1053 smoke rows.",
            "numeric_value": "not_applicable",
            "units": "dimensionless",
            "source_row": "WEB983_0_MICROSCOPE_CQG_COMPOSITION; WCM1053_4",
            "status": "material_pair_convention_filled_for_smoke",
            "blocks_claim": "full material tensor and parent source/readout convention still missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "convention_id": "MCON1061_1_delta_Q_alpha",
            "object": "Delta_Q_alpha_Coulomb_abs",
            "definition": "absolute alpha/Coulomb differential material charge in the Damour-Donoghue smoke convention.",
            "numeric_value": delta_q_abs,
            "units": "dimensionless",
            "source_row": "WCM1053_4",
            "status": "numeric_smoke_delta_filled",
            "blocks_claim": "source-backed smoke estimate, not full MICROSCOPE material tensor",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "convention_id": "MCON1061_2_eta_bound",
            "object": "eta_WEP_source_charge_bound",
            "definition": "MICROSCOPE Ti/Pt upper bound imported as the WEP product target anchor.",
            "numeric_value": eta_bound,
            "units": "dimensionless",
            "source_row": "R1_WEP_source_charge; WEP988_WAS651_0_alpha_Coulomb",
            "status": "numeric_bound_anchor_filled",
            "blocks_claim": "bound alone is not an MTS prediction",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "convention_id": "MCON1061_3_screened_product_target",
            "object": "abs_P_WEP_alpha_target",
            "definition": "under the 650/651 shared-screen smoke convention, |P_WEP_alpha| <= eta_bound/unit_source_eta_prediction.",
            "numeric_value": target,
            "units": "dimensionless",
            "source_row": "WEP988_WAS651_0_alpha_Coulomb; AWP1052_0_alpha_Coulomb",
            "status": "score_threshold_filled_not_prediction",
            "blocks_claim": "P_WEP_alpha itself still requires beta_source_alpha, b_alpha, and tau_WEP or a direct parent product derivation",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def derivation_attempt_rows() -> list[dict[str, str]]:
    return [
        {
            "attempt_id": "DER1061_0_product_definition",
            "target": "P_WEP_alpha",
            "attempted_derivation": "P_WEP_alpha := beta_source_alpha*b_alpha*tau_WEP, or directly as the parent variation of the alpha-sensitive source/test acceleration map.",
            "available_evidence": "material delta and screened product target are numeric in the 650/651/988/1052 smoke convention",
            "missing_premise": "parent source-normalization functional and WEP orbit/source projection",
            "result": "PRODUCT_CONTRACT_WRITTEN_NOT_DERIVED",
            "next_action": "derive the combined product from parent matter/source action instead of assigning beta_source_alpha=1 or tau_WEP=1",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "DER1061_1_beta_source_alpha",
            "target": "beta_source_alpha",
            "attempted_derivation": "beta_source_alpha as the alpha-channel source/force normalization from partial_Xhat ln(M_source^eff) or the same Noether owner that fixes charge/current normalization.",
            "available_evidence": "BSA1053_1 and BSO989_0 define the required owner",
            "missing_premise": "parent matter functional, Noether current normalization, and no-marker/no-alpha theorem are unsigned",
            "result": "OWNER_NOT_DERIVED",
            "next_action": "hunt parent source-normalization owner or prove beta_source_alpha=0 by EM-lock/no-alpha theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "DER1061_2_tau_WEP",
            "target": "tau_WEP",
            "attempted_derivation": "tau_WEP as the normalized lab/source/orbit projection converting the same Xhat variation used by clocks into differential acceleration.",
            "available_evidence": "TPR1053_1 defines the object; 650 requires the shared local alpha screen across clocks/WEP/R10",
            "missing_premise": "Earth/source worldtube, spacecraft/environment averaging, material tensor, parent Xhat normalization, and observed-force readout",
            "result": "PROJECTION_NOT_DERIVED",
            "next_action": "derive tau_WEP from local source geometry or replace split beta*tau by a direct P_WEP_alpha theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "DER1061_3_material_convention",
            "target": "MICROSCOPE alpha material map",
            "attempted_derivation": "use existing PtRh10/TA6V smoke alloy map and Delta_Q_alpha_Coulomb as the first product convention.",
            "available_evidence": "WEB983_0, WCM1053_4, WEP988_WAS651_0, and AWP1052_0",
            "missing_premise": "full material tensor and source/readout convention for a claim-grade MICROSCOPE prediction",
            "result": "PARTIAL_FILLED_SMOKE_CONVENTION_ONLY",
            "next_action": "use this as the first internal scoring convention, not public evidence",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def input_fill_rows() -> list[dict[str, str]]:
    material = material_convention_rows()
    target = next(row for row in material if row["convention_id"] == "MCON1061_3_screened_product_target")
    delta = next(row for row in material if row["convention_id"] == "MCON1061_1_delta_Q_alpha")
    return [
        {
            "input_id": "INF1061_0_material_pair",
            "required_input": "MICROSCOPE material convention",
            "value_or_status": "TA6V_minus_PtRh10",
            "source": "WEB983_0_MICROSCOPE_CQG_COMPOSITION; WCM1053_4",
            "filled_status": "filled_for_smoke_only",
            "why_not_claim": "full material/source/readout tensor missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "INF1061_1_delta_Q_alpha",
            "required_input": "Delta_Q_alpha_Coulomb_abs",
            "value_or_status": delta["numeric_value"],
            "source": "WCM1053_4; AWP1052_0_alpha_Coulomb",
            "filled_status": "filled_for_smoke_only",
            "why_not_claim": "smoke formula, not complete material model",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "INF1061_2_product_bound",
            "required_input": "abs_P_WEP_alpha_bound",
            "value_or_status": target["numeric_value"],
            "source": "WEP988_WAS651_0_alpha_Coulomb; BOUND1060_1_WEP_alpha",
            "filled_status": "target_filled_not_prediction",
            "why_not_claim": "a bound threshold is not an MTS-predicted product",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "INF1061_3_beta_source_alpha",
            "required_input": "beta_source_alpha",
            "value_or_status": "MISSING_PARENT_SOURCE_NORMALIZATION_OWNER",
            "source": "BSA1053_1_alpha_marker_source; BSO989_0_definition",
            "filled_status": "not_filled",
            "why_not_claim": "cannot set source normalization to unity; needs parent matter/Noether source owner or zero theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "INF1061_4_tau_WEP",
            "required_input": "tau_WEP",
            "value_or_status": "MISSING_LAB_SOURCE_ORBIT_PROJECTION",
            "source": "TPR1053_1_tau_WEP_definition; PR650_1_WEP",
            "filled_status": "not_filled",
            "why_not_claim": "cannot set tau_WEP to one; needs local geometry/source profile/readout map",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "INF1061_5_b_alpha_or_direct_product",
            "required_input": "b_alpha_counterterm or direct P_WEP_alpha",
            "value_or_status": "MISSING_PARENT_ALPHA_COUNTERTERM_PRODUCT",
            "source": "APP1059_2_WEP_alpha_Coulomb; PRED1060_1_WEP_alpha_template",
            "filled_status": "not_filled",
            "why_not_claim": "standalone b_alpha remains forbidden; only a directly derived product may be scored",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def prediction_attempt_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1061_0_WEP_alpha_material_convention_filled",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_alpha",
            "product_value": "MISSING_PARENT_DERIVED_BETA_SOURCE_ALPHA_B_ALPHA_TAU_WEP_PRODUCT",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1061_INPUT_FILL_LEDGER.csv",
            "inputs_present": "Delta_Q_alpha_abs;eta_bound;screened_product_target",
            "required_inputs": "beta_source_alpha;b_alpha_counterterm;tau_WEP OR directly derived P_WEP_alpha",
            "derivation_status": "MATERIAL_CONVENTION_FILLED_BETA_TAU_PRODUCT_MISSING",
            "valid_for_claim": "false",
            "notes": "The runner must refuse this row because the MTS product value is still missing.",
        }
    ]


def bound_import_rows() -> list[dict[str, str]]:
    return [
        {
            "bound_id": "BOUND1061_0_WEP_alpha_screened_product_target",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_alpha",
            "bound_value": "4.797780522732e-05",
            "bound_units": "dimensionless",
            "bound_source": "source-intake/mts_residuals/P8_Y5_R10_988_WEP_ALPHA_PRESSURE_IMPORT.csv",
            "source_row": "WEP988_WAS651_0_alpha_Coulomb",
            "bound_type": "screened_smoke_product_target_nonclaim",
            "valid_for_claim": "false",
            "notes": "Internal target only: uses 650/651 shared-screen smoke convention and cannot become a claim without a real MTS product prediction.",
        }
    ]


def failure_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "failure_id": "FAIL1061_0_no_beta_source_owner",
            "object": "beta_source_alpha",
            "expected_failure": "MISSING_PARENT_SOURCE_NORMALIZATION_OWNER",
            "observed_status": "not_filled",
            "meaning": "WEP alpha product cannot be predicted from a source/test coupling until the parent matter/Noether owner is signed.",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "failure_id": "FAIL1061_1_no_tau_WEP_projection",
            "object": "tau_WEP",
            "expected_failure": "MISSING_LAB_SOURCE_ORBIT_PROJECTION",
            "observed_status": "not_filled",
            "meaning": "The shared screen cannot be exported into WEP acceleration without a source geometry/readout projection.",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "failure_id": "FAIL1061_2_no_numeric_product",
            "object": "P_WEP_alpha",
            "expected_failure": "valid_prediction_rows=0",
            "observed_status": f"valid_prediction_rows={product_status.get('valid_prediction_rows')}",
            "meaning": "The product runner must refuse the row until a numeric parent-derived P_WEP_alpha exists.",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "failure_id": "FAIL1061_3_no_unity_shortcuts",
            "object": "beta_source_alpha;tau_WEP",
            "expected_failure": "no beta=1 or tau=1 replacement",
            "observed_status": "unity shortcuts absent",
            "meaning": "No coefficient is promoted by convention; the coupling must come from the theory.",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1061_0_material_convention_claim",
            "claim": "MICROSCOPE material convention is claim-grade",
            "gate_pass": "false",
            "reason": "only a smoke alloy/material charge convention is filled; full tensor/readout source map is missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1061_1_beta_source_alpha_claim",
            "claim": "beta_source_alpha is derived or bounded by MTS",
            "gate_pass": "false",
            "reason": "owner ledger still says source normalization is unowned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1061_2_tau_WEP_claim",
            "claim": "tau_WEP is derived",
            "gate_pass": "false",
            "reason": "tau_WEP remains a definition requiring lab/source/orbit projection",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1061_3_WEP_alpha_product_pass",
            "claim": "MTS passes WEP alpha/Coulomb product target",
            "gate_pass": "false",
            "reason": "product target exists but no numeric MTS product prediction exists",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1061_0_material_map",
            "decision": "material convention is partially filled",
            "because": "MICROSCOPE Ti/Pt composition and the alpha/Coulomb Delta_Q smoke row are already source-backed internally",
            "next_action": "use the convention as an internal target only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1061_1_product_prediction",
            "decision": "do not score WEP alpha yet",
            "because": "beta_source_alpha and tau_WEP remain unowned and the runner correctly refuses the product row",
            "next_action": "derive P_WEP_alpha directly from parent source-current geometry or prove a zero theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1061_2_best_next",
            "decision": "next target is combined parent source-normalization and tau_WEP product theorem",
            "because": "separating beta_source_alpha from tau_WEP may be gauge/convention-dependent; the product is what the WEP bound actually tests",
            "next_action": "1062-Y5-R10-parent-source-normalization-tauWEP-product-theorem-or-WEP-alpha-closure.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1062-Y5-R10-parent-source-normalization-tauWEP-product-theorem-or-WEP-alpha-closure.md",
            "objective": "derive or reject the combined parent WEP product P_WEP_alpha by mapping source normalization, alpha counterterm response, and tau_WEP projection from one parent matter/source action; if this cannot be signed, demote the WEP alpha route to closure-only.",
            "include": "parent source-current owner, tau_WEP local geometry/readout map, direct P_WEP_alpha theorem route, zero-theorem clauses, refusal row if any owner remains missing",
            "exclude": "beta_source_alpha=1, tau_WEP=1, cancellation, standalone b_alpha bound claim, public WEP/local-GR claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def product_status_rows(product_result: dict[str, Any]) -> list[dict[str, str]]:
    status = product_result["status"]
    return [
        {
            "runner_id": "APR1061_0_WEP_alpha_product_attempt",
            "prediction_rows": str(status.get("prediction_rows")),
            "bound_rows": str(status.get("bound_rows")),
            "valid_prediction_rows": str(status.get("valid_prediction_rows")),
            "valid_bound_rows": str(status.get("valid_bound_rows")),
            "comparison_rows": str(status.get("comparison_rows")),
            "claim_allowed": str(status.get("claim_allowed")).lower(),
            "expected_result": "reject_missing_parent_product",
            "status_path": str(PRODUCT_RUN_DIR / "alpha_product_runner_status.json"),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def count_formalization_modified_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    start_time = STARTED.timestamp()
    for path in FORMALIZATION.rglob("*"):
        try:
            if path.is_file() and path.stat().st_mtime > start_time:
                count += 1
        except OSError:
            continue
    return count


def validate_outputs(
    outputs: dict[str, Path],
    source_rows: list[dict[str, str]],
    material_rows: list[dict[str, str]],
    derivation_rows: list[dict[str, str]],
    input_rows: list[dict[str, str]],
    prediction_rows: list[dict[str, str]],
    bound_rows: list[dict[str, str]],
    product_result: dict[str, Any],
    failures: list[dict[str, str]],
    claims: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                "check_id": check_id,
                "result": "pass" if passed else "fail",
                "detail": detail,
                "generated_utc": stamp(),
            }
        )

    sources_ok = source_rows and all(row["exists"] == "true" and row["needle_found"] == "true" for row in source_rows)
    add("V1061_1_sources_exist_and_needles", sources_ok, "every cited local source path exists and every source needle was found")
    material_ok = any(row["convention_id"] == "MCON1061_1_delta_Q_alpha" and row["numeric_value"] == "0.001989808886825" for row in material_rows)
    add("V1061_2_material_delta_imported", material_ok, "alpha/Coulomb Delta_Q material convention imported")
    target_ok = any(row["convention_id"] == "MCON1061_3_screened_product_target" and row["numeric_value"] == "4.797780522732e-05" for row in material_rows)
    add("V1061_3_product_target_imported", target_ok, "screened WEP alpha product target imported")
    beta_blocked = any(row["attempt_id"] == "DER1061_1_beta_source_alpha" and row["result"] == "OWNER_NOT_DERIVED" for row in derivation_rows)
    add("V1061_4_beta_source_not_guessed", beta_blocked, "beta_source_alpha remains unguessed and owner-gated")
    tau_blocked = any(row["attempt_id"] == "DER1061_2_tau_WEP" and row["result"] == "PROJECTION_NOT_DERIVED" for row in derivation_rows)
    add("V1061_5_tau_WEP_not_guessed", tau_blocked, "tau_WEP remains unguessed and projection-gated")
    inputs_ok = len(input_rows) >= 6 and all(row["valid_for_claim"] == "false" for row in input_rows)
    add("V1061_6_input_fill_ledger_nonclaim", inputs_ok, "input fill ledger records filled and missing pieces without claims")
    prediction_nonclaim = prediction_rows and all(row.get("valid_for_claim") == "false" and "MISSING" in json.dumps(row) for row in prediction_rows)
    add("V1061_7_prediction_attempt_nonclaim", prediction_nonclaim, "prediction attempt row retains missing parent product")
    bound_ok = bound_rows and bound_rows[0].get("bound_value") == "4.797780522732e-05"
    add("V1061_8_bound_import_written", bound_ok, "WEP alpha product target bound row written")
    product_refused = product_result["status"].get("valid_prediction_rows") == 0 and product_result["status"].get("claim_allowed") is False
    add("V1061_9_product_runner_refuses", product_refused, "product runner refuses the material-filled but product-missing row")
    failures_ok = len(failures) >= 4 and all(row["valid_for_claim"] == "false" for row in failures)
    add("V1061_10_failures_written", failures_ok, "strict missing-input failure rows written")
    claims_blocked = claims and all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claims)
    add("V1061_11_claim_gates_blocked", claims_blocked, "claim gates remain blocked")
    next_ok = next_rows and next_rows[0]["next_target"].startswith("1062-Y5-R10-parent-source-normalization")
    add("V1061_12_next_target_written", bool(next_ok), "next target selects combined parent WEP product theorem")
    generated_inside = all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in outputs.values())
    add("V1061_13_generated_files_in_post_checkpoint", generated_inside, "all generated files are under post-checkpoint-work")
    formalization_count = count_formalization_modified_since_start()
    add("V1061_14_formalization_untouched", formalization_count == 0, f"formalization-workbench modified-file count since script start is {formalization_count}")

    summary_pass = all(row["result"] == "pass" for row in checks)
    checks.insert(0, {"check_id": "V1061_SUMMARY", "result": "pass" if summary_pass else "fail", "detail": "1061 WEP alpha product input-fill validation summary", "generated_utc": stamp()})
    return checks


def write_doc(
    source_rows: list[dict[str, str]],
    material_rows: list[dict[str, str]],
    derivation_rows: list[dict[str, str]],
    input_rows: list[dict[str, str]],
    prediction_rows: list[dict[str, str]],
    bound_rows: list[dict[str, str]],
    product_status: list[dict[str, str]],
    product_comparisons: list[dict[str, Any]],
    failures: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1061 - WEP Alpha Product First Input Fill: tau_WEP / beta_source / Material Map",
            "",
            "**Current verdict:** the MICROSCOPE WEP material convention and screened alpha-product target are filled for internal smoke testing, but the MTS product prediction is still absent.",
            "",
            "**Non-negotiable result:** no WEP alpha pass is allowed until `P_WEP_alpha = beta_source_alpha*b_alpha*tau_WEP` is derived directly or every factor is parent-owned. No `beta_source_alpha=1`; no `tau_WEP=1`; no clock-only transfer.",
            "",
            "**Next move:** derive the combined parent WEP product from one source-current/local-geometry map, or demote the WEP alpha route to closure-only.",
            "",
            "## Source Register",
            md_table(source_rows, ["source_id", "relative_path", "exists", "needle", "needle_found", "note"]),
            "",
            "## Material Convention",
            md_table(material_rows, ["convention_id", "object", "definition", "numeric_value", "units", "source_row", "status", "blocks_claim"]),
            "",
            "## Derivation Attempts",
            md_table(derivation_rows, ["attempt_id", "target", "attempted_derivation", "available_evidence", "missing_premise", "result", "next_action"]),
            "",
            "## Input Fill Ledger",
            md_table(input_rows, ["input_id", "required_input", "value_or_status", "source", "filled_status", "why_not_claim"]),
            "",
            "## Prediction Attempt",
            md_table(prediction_rows, ["prediction_id", "arena", "product_symbol", "product_value", "product_units", "inputs_present", "required_inputs", "derivation_status", "valid_for_claim"]),
            "",
            "## Bound Import",
            md_table(bound_rows, ["bound_id", "arena", "product_symbol", "bound_value", "bound_units", "bound_type", "valid_for_claim"]),
            "",
            "## Product Runner Status",
            md_table(product_status, ["runner_id", "prediction_rows", "bound_rows", "valid_prediction_rows", "valid_bound_rows", "comparison_rows", "claim_allowed", "expected_result"]),
            "",
            "## Product Comparison Rows",
            md_table(product_comparisons, ["comparison_id", "arena", "product_symbol", "product_value", "bound_value", "comparison_status", "pass_for_claim", "issues"]),
            "",
            "## Strict Failure Modes",
            md_table(failures, ["failure_id", "object", "expected_failure", "observed_status", "meaning", "valid_for_claim"]),
            "",
            "## Claim Gates",
            md_table(claims, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "",
            "## Decision Ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "",
            "## Validation",
            md_table(validation, ["check_id", "result", "detail", "generated_utc"]),
            "",
            "## Next Target",
            md_table(next_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    material_rows = material_convention_rows()
    derivation_rows = derivation_attempt_rows()
    input_rows = input_fill_rows()
    prediction_rows = prediction_attempt_rows()
    bound_rows = bound_import_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    outputs = {
        "sources": OUT / "P8_Y5_R10_1061_SOURCE_REGISTER.csv",
        "material": OUT / "P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv",
        "derivation": OUT / "P8_Y5_R10_1061_BETA_TAU_DERIVATION_ATTEMPT.csv",
        "input_fill": OUT / "P8_Y5_R10_1061_INPUT_FILL_LEDGER.csv",
        "prediction": PREDICTION_ATTEMPT,
        "bound": BOUND_IMPORT,
        "runner_status": OUT / "P8_Y5_R10_1061_PRODUCT_RUNNER_STATUS.csv",
        "comparisons": OUT / "P8_Y5_R10_1061_PRODUCT_COMPARISON_ROWS.csv",
        "failures": OUT / "P8_Y5_R10_1061_STRICT_FAILURE_MODES.csv",
        "claims": OUT / "P8_Y5_R10_1061_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1061_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1061_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1061_VALIDATION.csv",
        "doc": DOC,
    }

    write_csv(outputs["sources"], source_rows)
    write_csv(outputs["material"], material_rows)
    write_csv(outputs["derivation"], derivation_rows)
    write_csv(outputs["input_fill"], input_rows)
    write_csv(outputs["prediction"], prediction_rows, PRODUCT_REQUIRED_COLUMNS)
    write_csv(outputs["bound"], bound_rows, BOUND_REQUIRED_COLUMNS)
    write_csv(outputs["claims"], claims)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_rows)

    product_result = run_product_runner(PREDICTION_ATTEMPT, BOUND_IMPORT, PRODUCT_RUN_DIR)
    status_rows = product_status_rows(product_result)
    failures = failure_rows(product_result["status"])
    write_csv(outputs["runner_status"], status_rows)
    write_csv(outputs["comparisons"], product_result["comparisons"])
    write_csv(outputs["failures"], failures)

    validation = validate_outputs(
        outputs,
        source_rows,
        material_rows,
        derivation_rows,
        input_rows,
        prediction_rows,
        bound_rows,
        product_result,
        failures,
        claims,
        next_rows,
    )
    write_csv(outputs["validation"], validation)
    write_doc(
        source_rows,
        material_rows,
        derivation_rows,
        input_rows,
        prediction_rows,
        bound_rows,
        status_rows,
        product_result["comparisons"],
        failures,
        claims,
        decisions,
        validation,
        next_rows,
    )

    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
