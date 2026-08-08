from __future__ import annotations

import csv
import math
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
DOC = ROOT / "1095-Y5-R10-parent-Xhat-WEP-product-action-clause-or-direct-product-numeric-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1095-parent-Xhat-WEP-product-action-clause" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_R10_1095_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1095_WEP_PRODUCT_BOUND_IMPORT.csv"
ETA_BOUND = 2.8e-15
DD_ALPHA_PRODUCT_ABS = 3.365285544434638e-06
DD_SURFACE_PRODUCT_ABS = 4.007154691040701e-05
DD_COMBINED_PRODUCT_ABS = 4.343683245484165e-05
DD_ALPHA_COEFF_MAX = ETA_BOUND / DD_ALPHA_PRODUCT_ABS
DD_SURFACE_COEFF_MAX = ETA_BOUND / DD_SURFACE_PRODUCT_ABS
DD_COMBINED_COEFF_MAX = ETA_BOUND / DD_COMBINED_PRODUCT_ABS


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


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


def parse_float(value: object) -> float | None:
    try:
        parsed = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


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


def count_formalization_modified_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED
    )


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1095_0_1094_next", "source-intake/mts_residuals/P8_Y5_R10_1094_NEXT_TARGET.csv", "NEXT1094_0_1095", "1094 handoff."),
        ("SRC1095_1_1094_contract", "source-intake/mts_residuals/P8_Y5_R10_1094_DIRECT_WEP_PRODUCT_CONTRACT.csv", "DWP1094_4_required_prediction", "direct WEP product contract."),
        ("SRC1095_2_1094_action", "source-intake/mts_residuals/P8_Y5_R10_1094_PARENT_XHAT_ACTION_CLAUSE_ATTEMPT.csv", "PX1094_3_verdict", "parent Xhat action clause gap."),
        ("SRC1095_3_1077_owner", "source-intake/mts_residuals/P8_Y5_R10_1077_PARENT_WEP_COUPLING_OWNER_THEOREM_ATTEMPT.csv", "WCO1077_5_verdict", "WEP coupling-owner theorem attempt."),
        ("SRC1095_4_1081_basis", "source-intake/mts_residuals/P8_Y5_R10_1081_PARENT_WEP_BASIS_DERIVATION_ATTEMPT.csv", "PB1081_4_verdict", "parent WEP basis derivation attempt."),
        ("SRC1095_5_1083_DD_product", "source-intake/mts_residuals/P8_Y5_R10_1083_DD_SOURCE_MATERIAL_PRODUCT_NONCLAIM.csv", "DD_PRODUCT1083_0_alpha", "DD source-material product rows."),
        ("SRC1095_6_1087_no_cancel", "source-intake/mts_residuals/P8_Y5_R10_1087_ALL_MATERIAL_NO_CANCELLATION_POLICY.csv", "AMC1087_0_pair_line_forbidden", "all-material no-cancellation policy."),
        ("SRC1095_7_1088_MOMS", "source-intake/mts_residuals/P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv", "MOMS1088_7_verdict", "minimal ordinary matter signature failure."),
        ("SRC1095_8_1061_material", "source-intake/mts_residuals/P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv", "MCON1061_3_screened_product_target", "WEP material convention threshold."),
        ("SRC1095_9_local_bounds", "source-intake/local_bounds/local_bound_claims.csv", "R1_WEP_source_charge", "MICROSCOPE WEP bound anchor."),
    ]
    rows: list[dict[str, str]] = []
    for source_id, relative_path, needle, note in specs:
        path = source_path(relative_path)
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "relative_path": relative_path,
                "absolute_path": str(path),
                "exists": str(exists).lower(),
                "needle": needle,
                "needle_found": str(needle in text).lower(),
                "note": note,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def action_clause_rows() -> list[dict[str, str]]:
    return [
        {
            "clause_id": "PAC1095_0_field_owner",
            "parent_action_clause": "Xhat is a parent-owned varied field, not an after-the-fact closure coordinate",
            "required_form": "S_parent contains Xhat with fixed units/normalization and a declared quotient role",
            "current_status": "NOT_DERIVED",
            "failure_reason": "current chi_X/Xhat rows define product coordinates and theorem targets, not a signed parent field",
            "if_signed": "same Xhat can feed nohair, clock, WEP, and R10 branches",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "PAC1095_1_matter_response",
            "parent_action_clause": "ordinary matter response is either quotient-invariant or has a finite coefficient vector c_I",
            "required_form": "delta_X S_matter = 0, or delta_X ln m_A^eff = sum_I c_I Q_A^I delta Xhat with source/readout map",
            "current_status": "CONDITIONAL_NOT_SIGNED",
            "failure_reason": "MOMS/WEP coupling-owner clauses remain unsigned",
            "if_signed": "the branch becomes theorem-zero or a finite DD/source-product score",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "PAC1095_2_source_readout",
            "parent_action_clause": "Earth source and MICROSCOPE readout use the same observed-frame Hilbert source map as the GR baseline",
            "required_form": "P_WEP = K_readout[e_obs,orbit] * sum_I c_I Q_source^I Delta Q_test^I",
            "current_status": "SOURCE_READOUT_NOT_DERIVED",
            "failure_reason": "source worldtube, orbit/readout kernel, and no measured-G absorption remain missing",
            "if_signed": "direct P_WEP row can be numeric without standalone beta/tau division",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "PAC1095_3_no_cancellation",
            "parent_action_clause": "coefficient vector is parent-derived or zero, not fitted to a material-pair cancellation line",
            "required_form": "c_I fixed before material choice; all-material basis policy applies",
            "current_status": "POLICY_ONLY_NOT_PARENT_DERIVED",
            "failure_reason": "no-cancellation policy is written but not a parent coefficient theorem",
            "if_signed": "prevents WEP pass-by-cancellation",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "PAC1095_4_verdict",
            "parent_action_clause": "parent Xhat WEP product action clause is derived",
            "required_form": "PAC1095_0 through PAC1095_3 all parent-signed",
            "current_status": "ACTION_CLAUSE_NOT_DERIVED",
            "failure_reason": "field owner, matter response, source/readout, and coefficient-vector owner are not all signed",
            "if_signed": "would yield theorem-zero or numeric direct product prediction",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def theorem_zero_rows() -> list[dict[str, str]]:
    return [
        {
            "theorem_id": "WZ1095_0_assume_signature",
            "step": "assume quotient-invariant ordinary matter action",
            "mathematical_statement": "Lie_Xhat S_matter = 0 up to gauge/boundary/readout terms",
            "status": "ASSUMPTION_NOT_SIGNED",
            "consequence": "would imply no source/material WEP residual from Xhat",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "WZ1095_1_chain_rule_zero",
            "step": "differentiate the matter action along Xhat",
            "mathematical_statement": "delta_X S_matter = (delta S/delta q)Dq[Xhat] + gauge/boundary = 0 if Dq[Xhat]=0 and MOMS holds",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "consequence": "P_WEP_alpha_direct=0 under the full parent signature",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "WZ1095_2_countermodels",
            "step": "allow any unsigned clause",
            "mathematical_statement": "species weights, alpha coefficients, source labels, boundary/domain markers, or readout projectors can generate finite P_WEP",
            "status": "FINITE_COUNTERMODELS_RETAINED",
            "consequence": "theorem-zero cannot be promoted from current corpus",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "WZ1095_3_verdict",
            "step": "apply theorem-zero to MTS",
            "mathematical_statement": "P_WEP_alpha_direct=0 is derivable only after parent action clause is signed",
            "status": "THEOREM_ZERO_NOT_PROMOTED",
            "consequence": "continue finite direct-product row acquisition",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def direct_formula_rows() -> list[dict[str, str]]:
    return [
        {
            "formula_id": "DPF1095_0_direct_observable",
            "object": "direct WEP product formula",
            "formula": "P_WEP_alpha_direct := K_MICROSCOPE[e_obs,orbit,readout] * sum_I c_I Q_source^I DeltaQ_TiPt^I",
            "current_status": "FORMULA_CONTRACT_ONLY",
            "missing_for_numeric": "K_MICROSCOPE/source/readout owner and parent coefficient vector c_I",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "formula_id": "DPF1095_1_DD_alpha",
            "object": "single alpha/Coulomb DD component",
            "formula": "eta_alpha = c_alpha * Q_source_alpha * DeltaQ_alpha_TiPt",
            "current_status": "NUMERIC_SOURCE_MATERIAL_PRODUCT_NONCLAIM",
            "missing_for_numeric": "parent c_alpha",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "formula_id": "DPF1095_2_DD_surface",
            "object": "single surface/binding DD component",
            "formula": "eta_surface = c_surface * Q_source_surface * DeltaQ_surface_TiPt",
            "current_status": "NUMERIC_SOURCE_MATERIAL_PRODUCT_NONCLAIM",
            "missing_for_numeric": "parent c_surface",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "formula_id": "DPF1095_3_vector_policy",
            "object": "multi-component vector",
            "formula": "eta = c dot p_DD with p_DD fixed before choosing material pair",
            "current_status": "NO_CANCELLATION_POLICY_ACTIVE",
            "missing_for_numeric": "parent coefficient vector and all-material basis coverage",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def coefficient_threshold_rows() -> list[dict[str, str]]:
    specs = [
        ("THR1095_0_alpha", "c_alpha_DD", DD_ALPHA_PRODUCT_ABS, DD_ALPHA_COEFF_MAX, "DD_PRODUCT1083_0_alpha"),
        ("THR1095_1_surface", "c_surface_DD", DD_SURFACE_PRODUCT_ABS, DD_SURFACE_COEFF_MAX, "DD_PRODUCT1083_1_surface"),
        ("THR1095_2_combined_abs", "c_common_abs_if_single_combined_scale", DD_COMBINED_PRODUCT_ABS, DD_COMBINED_COEFF_MAX, "DD_PRODUCT1083_2_combined_abs"),
    ]
    return [
        {
            "threshold_id": threshold_id,
            "coefficient": coefficient,
            "source_material_product_abs": f"{product_abs:.16e}",
            "eta_bound": f"{ETA_BOUND:.16e}",
            "required_abs_coefficient_max": f"{coefficient_max:.16e}",
            "source_row": source_row,
            "status": "NUMERIC_THRESHOLD_NONCLAIM",
            "claim_policy": "threshold only until parent coefficient is derived or sourced",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for threshold_id, coefficient, product_abs, coefficient_max, source_row in specs
    ]


def numeric_row_requirement_rows() -> list[dict[str, str]]:
    return [
        {
            "requirement_id": "NR1095_0_coefficient_owner",
            "field_needed": "parent coefficient vector c_I or theorem-zero",
            "required_type": "numeric_or_exact_zero_with_source_path",
            "why_needed": "turns the DD/source-material product into an MTS prediction rather than a bound-side threshold",
            "current_status": "MISSING_PARENT_COEFFICIENT_VECTOR",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "requirement_id": "NR1095_1_source_vector",
            "field_needed": "Earth/source vector Q_source^I in same basis",
            "required_type": "numeric_vector_with_units_and_source",
            "why_needed": "sets source leg of WEP product",
            "current_status": "SMOKE_DD_VECTOR_ONLY",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "requirement_id": "NR1095_2_material_delta",
            "field_needed": "Ti/Pt material response DeltaQ^I",
            "required_type": "full material tensor or declared DD smoke convention",
            "why_needed": "sets test-body leg without cancellation games",
            "current_status": "SMOKE_DELTA_PRESENT_NOT_FULL_TENSOR",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "requirement_id": "NR1095_3_readout_kernel",
            "field_needed": "observed-frame MICROSCOPE readout/orbit kernel K_MICROSCOPE",
            "required_type": "numeric_kernel_or_theorem_reducing_to_eta",
            "why_needed": "maps source/material residual into measured eta_AB",
            "current_status": "MISSING_READOUT_KERNEL",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "requirement_id": "NR1095_4_no_rescale",
            "field_needed": "no measured-G/source-weight absorption proof",
            "required_type": "theorem_or_policy_with_parent_signature",
            "why_needed": "prevents hiding relative source weights in calibration",
            "current_status": "POLICY_ONLY",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1095_0_missing_parent_coefficient_vector",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "c_alpha_DD",
            "product_value": "MISSING_PARENT_COEFFICIENT_VECTOR_OR_THEOREM_ZERO",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1095_PARENT_XHAT_ACTION_CLAUSE_ATTEMPT.csv",
            "inputs_present": "DD source-material product thresholds; WEP coupling-owner conditional theorem; MICROSCOPE bound",
            "required_inputs": "parent c_alpha_DD numeric value or signed theorem-zero",
            "derivation_status": "MISSING_SCOREABLE_MTS_COEFFICIENT",
            "valid_for_claim": "false",
            "notes": "runner must refuse; no standalone beta/tau division or material-pair cancellation",
        }
    ]


def bound_import_rows() -> list[dict[str, str]]:
    return [
        {
            "bound_id": "BOUND1095_0_c_alpha_DD_threshold",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "c_alpha_DD",
            "bound_value": f"{DD_ALPHA_COEFF_MAX:.16e}",
            "bound_units": "dimensionless",
            "bound_source": "source-intake/mts_residuals/P8_Y5_R10_1083_DD_SOURCE_MATERIAL_PRODUCT_NONCLAIM.csv",
            "source_row": "DD_PRODUCT1083_0_alpha",
            "bound_type": "absolute_single_component_coefficient_threshold_nonclaim",
            "valid_for_claim": "false",
            "notes": "private threshold only; not claim-ready because DD row is smoke/source-material convention and MTS coefficient is missing",
        }
    ]


def product_status_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "runner_id": "APR1095_0_parent_coefficient_stub",
            "prediction_rows": str(product_status.get("prediction_rows", "")),
            "bound_rows": str(product_status.get("bound_rows", "")),
            "valid_prediction_rows": str(product_status.get("valid_prediction_rows", "")),
            "valid_bound_rows": str(product_status.get("valid_bound_rows", "")),
            "comparison_rows": str(product_status.get("comparison_rows", "")),
            "claim_allowed": str(product_status.get("claim_allowed", "")).lower(),
            "expected_result": "threshold exists but parent coefficient/theorem-zero is missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def claim_gate_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1095_0_action_clause",
            "claim_component": "parent Xhat WEP product action clause",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "PAC1095_4_verdict=ACTION_CLAUSE_NOT_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1095_1_theorem_zero",
            "claim_component": "P_WEP_alpha_direct=0 theorem-zero",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "WZ1095_3_verdict=THEOREM_ZERO_NOT_PROMOTED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1095_2_numeric_threshold",
            "claim_component": "DD coefficient thresholds exist",
            "gate_pass": "true_nonclaim_only",
            "claim_allowed": "false",
            "reason": "thresholds are numeric but coefficient vector is missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1095_3_product_runner",
            "claim_component": "coefficient product runner",
            "gate_pass": str(product_status.get("valid_prediction_rows") == 0).lower(),
            "claim_allowed": "false",
            "reason": f"valid_prediction_rows={product_status.get('valid_prediction_rows')}",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1095_0_action_clause",
            "decision": "parent Xhat WEP action clause is not derived",
            "because": "field owner, matter response, source/readout, and coefficient-vector ownership are not all parent-signed",
            "next_action": "do not claim theorem-zero; keep exact clause as future parent-action contract",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1095_1_thresholds",
            "decision": "DD source-material thresholds are now sharper than the generic direct-product threshold",
            "because": "single alpha threshold requires |c_alpha_DD| <= 8.32e-10 and surface requires |c_surface_DD| <= 6.99e-11",
            "next_action": "derive/source coefficient vector or prove it zero",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1095_2_best_next",
            "decision": "try coefficient-vector theorem-zero before more bound-side work",
            "because": "WEP bound side is already sharp; missing object is the MTS coefficient vector",
            "next_action": "1096-Y5-R10-parent-coefficient-vector-zero-theorem-or-DD-coefficient-prior-row.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1095_0_1096",
            "next_target": "1096-Y5-R10-parent-coefficient-vector-zero-theorem-or-DD-coefficient-prior-row.md",
            "objective": "derive c_I=0 for the WEP DD/material coefficient vector from the parent action, or stage a source-backed nonclaim coefficient prior row against the 1095 thresholds",
            "include": "parent coefficient-vector owner; alpha/surface DD basis; no-cancellation/all-material policy; single-component thresholds; product runner refusal/pass gates",
            "exclude": "pair-cancellation fit; tau_WEP=1; clock transfer; unsourced coefficient priors; local-GR/WEP claim; GitHub; formalization edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def csv_outputs_parse(paths: list[Path]) -> bool:
    try:
        for path in paths:
            with path.open(newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        return True
    except csv.Error:
        return False


def validate_outputs(
    outputs: dict[str, Path],
    source_rows: list[dict[str, str]],
    action_rows: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    formula_rows: list[dict[str, str]],
    threshold_rows: list[dict[str, str]],
    requirement_rows: list[dict[str, str]],
    prediction_rows_: list[dict[str, str]],
    bound_rows_: list[dict[str, str]],
    product_status: dict[str, Any],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V1095_0_local_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in source_rows), "all cited source paths and needles are present"))
    checks.append(("V1095_1_action_clause_not_derived", any(row["clause_id"] == "PAC1095_4_verdict" and row["current_status"] == "ACTION_CLAUSE_NOT_DERIVED" for row in action_rows), "parent action clause verdict is explicit"))
    checks.append(("V1095_2_theorem_zero_not_promoted", any(row["theorem_id"] == "WZ1095_3_verdict" and row["status"] == "THEOREM_ZERO_NOT_PROMOTED" for row in theorem_rows), "conditional WEP theorem-zero is not promoted"))
    checks.append(("V1095_3_formula_contract_present", any(row["formula_id"] == "DPF1095_0_direct_observable" for row in formula_rows), "direct WEP formula contract is present"))
    checks.append(("V1095_4_thresholds_numeric", len(threshold_rows) == 3 and all(parse_float(row["required_abs_coefficient_max"]) is not None and float(row["required_abs_coefficient_max"]) > 0 for row in threshold_rows), "DD coefficient thresholds are positive numeric"))
    checks.append(("V1095_5_alpha_threshold_sharp", abs(DD_ALPHA_COEFF_MAX - 8.320244933243532e-10) < 1e-22, "alpha DD coefficient threshold matches 1083 source-material product"))
    checks.append(("V1095_6_numeric_requirements_blocked", requirement_rows and all(row["valid_for_claim"] == "false" for row in requirement_rows), "numeric row requirements remain nonclaim and explicit"))
    checks.append(("V1095_7_prediction_missing_nonclaim", any("MISSING_PARENT_COEFFICIENT_VECTOR" in row["product_value"] and row["valid_for_claim"] == "false" for row in prediction_rows_), "prediction row remains missing coefficient vector and nonclaim"))
    checks.append(("V1095_8_bound_threshold_positive", bool(bound_rows_) and parse_float(bound_rows_[0]["bound_value"]) is not None and float(bound_rows_[0]["bound_value"]) > 0, "coefficient bound threshold is positive numeric"))
    checks.append(("V1095_9_product_runner_refuses", product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False, "generic product runner reports no valid prediction rows and claim false"))
    checks.append(("V1095_10_claim_gates_safe", claim_rows and all(row["claim_allowed"] == "false" for row in claim_rows), "all claim gates deny WEP/local claim"))
    checks.append(("V1095_11_next_target", any(row["next_target"].startswith("1096-Y5-R10-parent-coefficient-vector-zero") for row in next_rows), "1096 handoff written"))
    generated_paths = list(outputs.values()) + [DOC]
    checks.append(("V1095_12_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in generated_paths), "all generated outputs are under post-checkpoint-work"))
    checks.append(("V1095_13_csv_parse", csv_outputs_parse([path for key, path in outputs.items() if key != "validation"]), "all 1095 CSV outputs parse cleanly"))
    checks.append(("V1095_14_formalization_untouched", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains zero"))
    checks.append(("V1095_SUMMARY", True, "parent action clause not derived; theorem-zero conditional only; DD coefficient thresholds sharpen finite WEP route"))
    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for check_id, passed, detail in checks
    ]


def write_doc(
    source_rows: list[dict[str, str]],
    action_rows: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    formula_rows: list[dict[str, str]],
    threshold_rows: list[dict[str, str]],
    requirement_rows: list[dict[str, str]],
    product_status_rows_: list[dict[str, str]],
    product_comparisons: list[dict[str, Any]],
    claim_rows: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1095-Y5-R10 parent Xhat WEP product action clause or direct product numeric row",
            "",
            "## Current verdict",
            "1095 pins the coupling problem down. The clean derivation route is an exact conditional theorem: if the parent action owns `Xhat`, ordinary matter is quotient-invariant or has a parent-derived finite coefficient vector, and the observed-frame source/readout map is fixed, then WEP is either theorem-zero or a direct finite product. The current corpus does not sign that action clause. The finite route is now sharper: using the DD source-material rows, a single alpha/Coulomb coefficient would need `|c_alpha_DD| <= 8.320244933e-10`; the surface/binding coefficient would need `|c_surface_DD| <= 6.987501646e-11`. These are thresholds, not claims, because the MTS coefficient vector is still missing.",
            "",
            "## Source register",
            md_table(source_rows, ["source_id", "relative_path", "exists", "needle_found", "note"]),
            "## Parent Xhat action clause attempt",
            md_table(action_rows, ["clause_id", "parent_action_clause", "required_form", "current_status", "failure_reason", "if_signed"]),
            "## Conditional WEP theorem-zero",
            md_table(theorem_rows, ["theorem_id", "step", "mathematical_statement", "status", "consequence"]),
            "## Direct WEP formula ledger",
            md_table(formula_rows, ["formula_id", "object", "formula", "current_status", "missing_for_numeric"]),
            "## DD coefficient thresholds",
            md_table(threshold_rows, ["threshold_id", "coefficient", "source_material_product_abs", "eta_bound", "required_abs_coefficient_max", "source_row", "status"]),
            "## Numeric row requirements",
            md_table(requirement_rows, ["requirement_id", "field_needed", "required_type", "why_needed", "current_status"]),
            "## Product runner status",
            md_table(product_status_rows_, ["runner_id", "valid_prediction_rows", "valid_bound_rows", "comparison_rows", "claim_allowed", "expected_result"]),
            "## Product comparison rows",
            md_table(product_comparisons, ["comparison_id", "arena", "product_symbol", "product_value", "bound_value", "comparison_status", "pass_for_claim", "issues"]),
            "## Claim gates",
            md_table(claim_rows, ["gate_id", "claim_component", "gate_pass", "claim_allowed", "reason"]),
            "## Decision ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action"]),
            "## Validation",
            md_table(validation_rows, ["check_id", "result", "detail"]),
            "## Next target",
            md_table(next_rows, ["next_id", "next_target", "objective", "include", "exclude"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    action_rows = action_clause_rows()
    theorem_rows = theorem_zero_rows()
    formula_rows = direct_formula_rows()
    threshold_rows = coefficient_threshold_rows()
    requirement_rows = numeric_row_requirement_rows()
    prediction_rows_ = prediction_rows()
    bound_rows_ = bound_import_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R10_1095_SOURCE_REGISTER.csv",
        "action_clause": OUT / "P8_Y5_R10_1095_PARENT_XHAT_ACTION_CLAUSE_ATTEMPT.csv",
        "theorem_zero": OUT / "P8_Y5_R10_1095_CONDITIONAL_WEP_THEOREM_ZERO.csv",
        "formula": OUT / "P8_Y5_R10_1095_DIRECT_WEP_FORMULA_LEDGER.csv",
        "thresholds": OUT / "P8_Y5_R10_1095_DD_COEFFICIENT_THRESHOLDS.csv",
        "requirements": OUT / "P8_Y5_R10_1095_NUMERIC_ROW_REQUIREMENTS.csv",
        "prediction": PREDICTION_TEMPLATE,
        "bound": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_R10_1095_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_R10_1095_PRODUCT_COMPARISON_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_R10_1095_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1095_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1095_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1095_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["action_clause"], action_rows)
    write_csv(outputs["theorem_zero"], theorem_rows)
    write_csv(outputs["formula"], formula_rows)
    write_csv(outputs["thresholds"], threshold_rows)
    write_csv(outputs["requirements"], requirement_rows)
    write_csv(outputs["prediction"], prediction_rows_, PRODUCT_REQUIRED_COLUMNS)
    write_csv(outputs["bound"], bound_rows_, BOUND_REQUIRED_COLUMNS)

    product_result = run_product_runner(PREDICTION_TEMPLATE, BOUND_IMPORT, PRODUCT_RUN_DIR)
    product_status = product_result["status"]
    product_status_rows_ = product_status_rows(product_status)
    product_comparisons = product_result["comparisons"]
    claim_rows = claim_gate_rows(product_status)
    decisions = decision_rows()

    write_csv(outputs["product_status"], product_status_rows_)
    write_csv(outputs["product_comparison"], product_comparisons)
    write_csv(outputs["claim_gates"], claim_rows)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next_target"], next_rows)

    validation_rows = validate_outputs(
        outputs,
        source_rows,
        action_rows,
        theorem_rows,
        formula_rows,
        threshold_rows,
        requirement_rows,
        prediction_rows_,
        bound_rows_,
        product_status,
        claim_rows,
        next_rows,
    )
    write_csv(outputs["validation"], validation_rows)
    write_doc(
        source_rows,
        action_rows,
        theorem_rows,
        formula_rows,
        threshold_rows,
        requirement_rows,
        product_status_rows_,
        product_comparisons,
        claim_rows,
        decisions,
        validation_rows,
        next_rows,
    )
    remove_pycache()

    failed = [row for row in validation_rows if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
