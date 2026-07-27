from __future__ import annotations

import csv
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
DOC = ROOT / "1086-Y5-R10-WEP-source-current-zero-or-parent-DD-map-first-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1086-WEP-source-current-zero-or-parent-DD-map-first-row" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_R10_1086_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1086_WEP_BOUND_IMPORT.csv"
ETA_BOUND = 2.8e-15


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


def parse_float(value: object) -> float | None:
    try:
        return float(str(value).strip())
    except ValueError:
        return None


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
        ("SRC1086_0_1085_next", "source-intake/mts_residuals/P8_Y5_R10_1085_NEXT_TARGET.csv", "1086-Y5-R10-WEP-source-current-zero-or-parent-DD-map-first-row.md", "1085 handoff."),
        ("SRC1086_1_1085_validation", "source-intake/mts_residuals/P8_Y5_BRR545_1085_VALIDATION.csv", "V1085_SUMMARY", "1085 validation summary."),
        ("SRC1086_2_1085_range", "source-intake/mts_residuals/P8_Y5_R10_1085_RANGE_OWNER_THEOREM_ATTEMPT.csv", "ROW1085_4_verdict", "range owner not derived."),
        ("SRC1086_3_618_source_zero", "source-intake/mts_residuals/P8_Y5_R10_618_SOURCE_ZERO_CERTIFICATE_AUDIT.csv", "SZ618_0_qbar_XT_chain_rule", "source-zero certificate audit."),
        ("SRC1086_4_1079_current_owner", "source-intake/mts_residuals/P8_Y5_R10_1079_NARROW_CURRENT_OWNER_THEOREM_ATTEMPT.csv", "NCO1079_6_verdict", "narrow current-owner theorem attempt."),
        ("SRC1086_5_1079_premises", "source-intake/mts_residuals/P8_Y5_R10_1079_CURRENT_OWNER_PREMISE_LEDGER.csv", "PR1079_4_no_pre_action_species_weight", "pre-action species weight premise."),
        ("SRC1086_6_1080_Cparent", "source-intake/mts_residuals/P8_Y5_R10_1080_C_PARENT_COEFFICIENT_CONTRACT.csv", "CP1080_2_DD_basis_external", "C_parent coefficient contract."),
        ("SRC1086_7_1081_basis", "source-intake/mts_residuals/P8_Y5_R10_1081_DD_BASIS_SCHEMA.csv", "DDB1081_0_alpha_Coulomb", "external DD basis schema."),
        ("SRC1086_8_1081_delta", "source-intake/mts_residuals/P8_Y5_R10_1081_DD_MATERIAL_DELTA_IMPORT.csv", "DDM1081_0_delta_alpha", "DD test-material deltas."),
        ("SRC1086_9_1082_parent_to_DD", "source-intake/mts_residuals/P8_Y5_R10_1082_PARENT_TO_DD_COEFFICIENT_MAP_ATTEMPT.csv", "PTD1082_4_verdict", "parent-to-DD map remains unsigned."),
        ("SRC1086_10_1082_units", "source-intake/mts_residuals/P8_Y5_R10_1082_COEFFICIENT_UNITS_CONTRACT.csv", "CUC1082_3_C_parent", "coefficient units contract."),
        ("SRC1086_11_1083_products", "source-intake/mts_residuals/P8_Y5_R10_1083_DD_SOURCE_MATERIAL_PRODUCT_NONCLAIM.csv", "DD_PRODUCT1083_2_combined_abs", "bulk Earth DD source-material product."),
        ("SRC1086_12_1025_alpha_schema", "source-intake/mts_residuals/P8_Y5_R10_1025_ALPHA_SOURCE_ROW_TEMPLATE.csv", "ASR1025_2_source_current", "alpha/source row template."),
        ("SRC1086_13_local_bounds", "source-intake/local_bounds/local_bound_claims.csv", "R1_WEP_source_charge", "MICROSCOPE WEP bound row."),
    ]
    rows: list[dict[str, str]] = []
    for source_id, relative_path, needle, note in specs:
        path = source_path(relative_path)
        exists = path.exists()
        text = read_text(path) if exists else ""
        needle_found = exists and needle.lower() in text.lower()
        rows.append(
            {
                "source_id": source_id,
                "relative_path": relative_path,
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


def material_delta_values() -> tuple[float, float]:
    rows = {row["delta_id"]: row for row in read_csv(OUT / "P8_Y5_R10_1081_DD_MATERIAL_DELTA_IMPORT.csv")}
    return float(rows["DDM1081_0_delta_alpha"]["delta_value"]), float(rows["DDM1081_1_delta_surface"]["delta_value"])


def source_current_zero_attempt_rows() -> list[dict[str, str]]:
    delta_alpha, delta_surface = material_delta_values()
    cancellation_ratio = -delta_alpha / delta_surface
    return [
        {
            "attempt_id": "SCZ1086_0_chain_rule_zero",
            "claim": "qbar_XT=0 from matter descent",
            "mathematical_statement": "if S_matter descends through observed quotient variables and Lie_vX(theta_A)=0, then delta_X S_matter has no material-composition source current",
            "current_evidence": "SZ618_0 gives exactly this as a conditional theorem, not parent-signed",
            "result": "CONDITIONAL_NOT_PARENT_SIGNED",
            "missing_for_claim": "parent matter descent; coframe/material constants silence; hidden/source/domain terms",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "SCZ1086_1_Hilbert_current_owner",
            "claim": "Hilbert variation kills post-variation source rescaling",
            "mathematical_statement": "after one common matter action is fixed, the source tensor is the Hilbert variation and cannot be rescaled by a later material selector",
            "current_evidence": "NCO1079_1 through NCO1079_4 give a conditional subtheorem",
            "result": "POST_VARIATION_TRICK_CONDITIONALLY_KILLED",
            "missing_for_claim": "common action and variation-before-readout premises; no pre-action species weights",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "SCZ1086_2_pre_action_weight_leak",
            "claim": "current ownership alone kills species weights inside S_matter",
            "mathematical_statement": "S_matter=sum_A w_A S_A would still Hilbert-vary to a weighted source if w_A is inserted before variation",
            "current_evidence": "NCO1079_5 and PR1079_4 leave pre-action species weights unsigned",
            "result": "ZERO_PROOF_FAILS_ON_PRE_ACTION_WEIGHTS",
            "missing_for_claim": "object-language/action-measure clause forbidding species/material weights before variation",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "SCZ1086_3_DD_decomposition_test_pair",
            "claim": "DD alpha/surface composition current vanishes for TA6V-PtRh10",
            "mathematical_statement": "Delta q_X = c_alpha Delta Q_alpha + c_surface Delta Q_surface + Delta q_tail; both selected Delta Q rows are nonzero",
            "current_evidence": f"Delta Q_alpha={delta_alpha:.15e}, Delta Q_surface={delta_surface:.15e}",
            "result": "NONZERO_COMPOSITION_DELTAS_BLOCK_AUTOMATIC_ZERO",
            "missing_for_claim": "c_alpha=0, c_surface=0, tail zero; or parent-signed common-mode/no-pole theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "SCZ1086_4_one_pair_cancellation",
            "claim": "one material pair can be silenced by coefficient ratio",
            "mathematical_statement": "for this pair alone, Delta q_X=0 if c_surface/c_alpha=-Delta Q_alpha/Delta Q_surface",
            "current_evidence": f"ratio={cancellation_ratio:.15e}",
            "result": "FORBIDDEN_CANCELLATION_NOT_THEOREM",
            "missing_for_claim": "all-material theorem or parent coefficient derivation; one-pair cancellation cannot be used",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "SCZ1086_5_verdict",
            "claim": "WEP source/test composition current is theorem-zero",
            "mathematical_statement": "qbar_XT=0 or DD coefficient vector vanishes from parent action",
            "current_evidence": "conditional descent exists, but pre-action weights, DD coefficients, no-pole, and common-mode routes remain unsigned",
            "result": "SOURCE_CURRENT_ZERO_NOT_DERIVED",
            "missing_for_claim": "parent matter descent zero or parent-to-DD zero/coefficients",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def parent_dd_map_first_row_attempt_rows() -> list[dict[str, str]]:
    return [
        {
            "map_id": "PDM1086_0_mass_response_decomposition",
            "parent_object": "composition-dependent mass response",
            "candidate_formula": "partial_X ln m_A = q_0 + c_alpha Q_alpha_Coulomb(A) + c_surface Q_surface_binding(A) + q_tail(A)",
            "needed_parent_evidence": "same-branch derivative of ordinary matter masses with respect to X",
            "current_status": "DECOMPOSITION_CONTRACT_ONLY",
            "gap": "no parent matter-mass functional m_A[X] exists in the corpus",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "map_id": "PDM1086_1_alpha_slot",
            "parent_object": "c_alpha",
            "candidate_formula": "c_alpha := N_X * partial_X ln alpha_EM in the DD Q_alpha_Coulomb convention",
            "needed_parent_evidence": "signed MTS EM/fine-structure action dependence on X plus field normalization N_X",
            "current_status": "MISSING_PARENT_EM_DERIVATIVE",
            "gap": "PTD1082_1_alpha_channel remains NOT_SIGNED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "map_id": "PDM1086_2_surface_slot",
            "parent_object": "c_surface",
            "candidate_formula": "c_surface := N_X * partial_X ln a_surface_or_binding in the DD Q_surface_binding convention",
            "needed_parent_evidence": "signed nuclear/binding/surface response operator and normalization",
            "current_status": "MISSING_PARENT_BINDING_DERIVATIVE",
            "gap": "PTD1082_2_surface_channel remains NOT_SIGNED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "map_id": "PDM1086_3_same_branch_units",
            "parent_object": "C_parent units and signs",
            "candidate_formula": "C_parent -> (c_alpha,c_surface,q_tail) with one X normalization, one lambda_X, and one source/readout convention",
            "needed_parent_evidence": "Z_X/M_X^2 normalization, K_X, source profile, and MICROSCOPE readout convention",
            "current_status": "MISSING_SAME_BRANCH_NORMALIZATION",
            "gap": "range owner, profile/readout, and coefficient units are all missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "map_id": "PDM1086_4_verdict",
            "parent_object": "first parent-to-DD coefficient row",
            "candidate_formula": "C_parent first row can be filled numerically or symbolically from parent action",
            "needed_parent_evidence": "real c_alpha or c_surface source path with units/signs",
            "current_status": "PARENT_DD_FIRST_ROW_NOT_FILLED",
            "gap": "1086 sharpens the exact row but supplies no parent coefficient",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def composition_delta_obstruction_rows() -> list[dict[str, str]]:
    delta_alpha, delta_surface = material_delta_values()
    cancellation_ratio = -delta_alpha / delta_surface
    return [
        {
            "obstruction_id": "CDO1086_0_alpha_delta",
            "component": "Q_alpha_Coulomb",
            "test_pair": "TA6V_minus_PtRh10",
            "delta_value": f"{delta_alpha:.15e}",
            "delta_abs": f"{abs(delta_alpha):.15e}",
            "meaning": "nonzero DD alpha/Coulomb composition lever",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "obstruction_id": "CDO1086_1_surface_delta",
            "component": "Q_surface_binding",
            "test_pair": "TA6V_minus_PtRh10",
            "delta_value": f"{delta_surface:.15e}",
            "delta_abs": f"{abs(delta_surface):.15e}",
            "meaning": "nonzero DD surface/binding composition lever",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "obstruction_id": "CDO1086_2_cancellation_line",
            "component": "c_alpha/c_surface two-component plane",
            "test_pair": "TA6V_minus_PtRh10",
            "delta_value": f"c_surface/c_alpha={cancellation_ratio:.15e}",
            "delta_abs": "",
            "meaning": "one-pair zero line exists algebraically but is a forbidden cancellation unless parent-derived for all relevant materials",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def coefficient_pressure_rows() -> list[dict[str, str]]:
    product_rows = {row["product_id"]: row for row in read_csv(OUT / "P8_Y5_R10_1083_DD_SOURCE_MATERIAL_PRODUCT_NONCLAIM.csv")}
    return [
        {
            "pressure_id": "CPR1086_0_alpha_bulk_Earth",
            "component": "Q_alpha_Coulomb",
            "source_material_product_abs": product_rows["DD_PRODUCT1083_0_alpha"]["product_abs"],
            "eta_bound": f"{ETA_BOUND:.15e}",
            "required_abs_coefficient_max": product_rows["DD_PRODUCT1083_0_alpha"]["required_abs_coefficient_max_if_single_component"],
            "status": "NUMERIC_PRESSURE_NONCLAIM",
            "claim_blocker": "bulk Earth vector, DD basis, and readout are not parent-owned",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "pressure_id": "CPR1086_1_surface_bulk_Earth",
            "component": "Q_surface_binding",
            "source_material_product_abs": product_rows["DD_PRODUCT1083_1_surface"]["product_abs"],
            "eta_bound": f"{ETA_BOUND:.15e}",
            "required_abs_coefficient_max": product_rows["DD_PRODUCT1083_1_surface"]["required_abs_coefficient_max_if_single_component"],
            "status": "NUMERIC_PRESSURE_NONCLAIM",
            "claim_blocker": "bulk Earth vector, DD basis, and readout are not parent-owned",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "pressure_id": "CPR1086_2_equal_two_component_bulk_Earth",
            "component": "Q_alpha_Coulomb + Q_surface_binding",
            "source_material_product_abs": product_rows["DD_PRODUCT1083_2_combined_abs"]["product_abs"],
            "eta_bound": f"{ETA_BOUND:.15e}",
            "required_abs_coefficient_max": product_rows["DD_PRODUCT1083_2_combined_abs"]["required_abs_coefficient_max_if_equal_component"],
            "status": "NUMERIC_PRESSURE_NONCLAIM",
            "claim_blocker": "equal-component assumption is not parent-derived and profile/readout gates remain live",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def no_cancellation_guard_rows() -> list[dict[str, str]]:
    return [
        {
            "guard_id": "NCG1086_0_no_pair_tuning",
            "forbidden_shortcut": "choose c_alpha/c_surface to cancel TA6V-PtRh10 only",
            "reason": "one-pair cancellation is not a parent theorem and would fail as soon as another material pair is tested",
            "required_safe_route": "derive c_alpha=c_surface=tail=0 or provide a parent coefficient vector and score all rows",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "guard_id": "NCG1086_1_no_measured_G_absorption",
            "forbidden_shortcut": "hide source response in measured G",
            "reason": "finite composition-dependent source/test products must be explicit or theorem-zero",
            "required_safe_route": "source common-mode theorem or explicit source-profile/readout product",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "guard_id": "NCG1086_2_no_unit_proxy_claim",
            "forbidden_shortcut": "use unit source/readout proxy as physical tau_WEP",
            "reason": "unit rows are algebra smoke only",
            "required_safe_route": "official MICROSCOPE readout normalization and source profile",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "guard_id": "NCG1086_3_same_branch_lock",
            "forbidden_shortcut": "derive lambda from one branch and amplitude from another",
            "reason": "range, coefficient, source, and readout must come from one parent normalization",
            "required_safe_route": "same-branch Z_X/M_X^2, C_parent, K_X, Qbar_XH, qbar_XT",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def acquisition_schema_rows() -> list[dict[str, str]]:
    return [
        {
            "schema_id": "AS1086_0_matter_descent_zero",
            "needed_object": "qbar_XT=0 theorem",
            "required_columns": "branch_id;S_matter_descends;Lie_vX_theta_A;hidden_terms_zero;source_path;valid_for_claim",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "claim_blocker": "SZ618_0 has theorem shape but no parent signature",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "schema_id": "AS1086_1_alpha_coefficient",
            "needed_object": "c_alpha",
            "required_columns": "branch_id;field_id;c_alpha;definition;units;sign;source_path;valid_for_claim",
            "current_status": "MISSING_PARENT_EM_DERIVATIVE",
            "claim_blocker": "alpha/EM parent operator pullback missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "schema_id": "AS1086_2_surface_coefficient",
            "needed_object": "c_surface",
            "required_columns": "branch_id;field_id;c_surface;definition;units;sign;source_path;valid_for_claim",
            "current_status": "MISSING_PARENT_BINDING_DERIVATIVE",
            "claim_blocker": "nuclear/binding parent operator missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "schema_id": "AS1086_3_tail_envelope",
            "needed_object": "q_tail(A) absolute envelope",
            "required_columns": "branch_id;tail_basis;tail_bound;materials_covered;source_path;valid_for_claim",
            "current_status": "MISSING_TAIL_BASIS",
            "claim_blocker": "two DD rows are not a full material basis",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "schema_id": "AS1086_4_physical_product",
            "needed_object": "finite WEP product",
            "required_columns": "branch_id;lambda_WEP;K_MICROSCOPE;Q_source_eff;c_alpha;c_surface;q_tail;eta_pred;source_paths;valid_for_claim",
            "current_status": "MISSING_RANGE_PROFILE_READOUT_AND_COEFFICIENTS",
            "claim_blocker": "1083-1085 gates remain live",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1086_0_source_current_or_DD_map_missing",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_SOURCE_CURRENT_ZERO_OR_PARENT_DD_COEFFICIENT_MAP",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1086_SOURCE_CURRENT_ZERO_THEOREM_ATTEMPT.csv",
            "inputs_present": "conditional source-zero theorem; DD deltas; nonclaim coefficient pressure rows; MICROSCOPE bound",
            "required_inputs": "parent matter descent zero or parent c_alpha/c_surface/tail coefficients; same-branch range/profile/readout",
            "derivation_status": "COUPLING_GATE_SHARPENED_BUT_NOT_CLOSED",
            "valid_for_claim": "false",
            "notes": "runner must refuse; 1086 does not produce a physical WEP prediction",
        }
    ]


def bound_import_rows() -> list[dict[str, str]]:
    return [
        {
            "bound_id": "BOUND1086_0_MICROSCOPE_WEP_source_charge",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "bound_value": f"{ETA_BOUND:.15e}",
            "bound_units": "dimensionless",
            "bound_source": "https://arxiv.org/abs/2209.15487",
            "source_row": "MICROSCOPE_final_TiPt_source_charge_proxy:R1_WEP_source_charge;doi:10.1103/PhysRevLett.129.121102",
            "bound_type": "upper_abs_WEP_proxy_bound",
            "valid_for_claim": "true",
            "notes": "source-backed numeric bound only; MTS prediction remains invalid",
        }
    ]


def product_status_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "runner_id": "APR1086_0_coupling_gate_product_stub",
            "prediction_rows": str(product_status.get("prediction_rows", "")),
            "bound_rows": str(product_status.get("bound_rows", "")),
            "valid_prediction_rows": str(product_status.get("valid_prediction_rows", "")),
            "valid_bound_rows": str(product_status.get("valid_bound_rows", "")),
            "comparison_rows": str(product_status.get("comparison_rows", "")),
            "passed_rows": str(product_status.get("passed_rows", "")),
            "claim_allowed": str(product_status.get("claim_allowed", "")).lower(),
            "expected_result": "reject missing source-current zero or parent-DD coefficient map",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def claim_gate_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1086_0_source_current_zero",
            "claim_component": "qbar_XT=0",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "SCZ1086_5_verdict=SOURCE_CURRENT_ZERO_NOT_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1086_1_parent_DD_map",
            "claim_component": "C_parent -> DD coefficients",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "PDM1086_4_verdict=PARENT_DD_FIRST_ROW_NOT_FILLED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1086_2_composition_obstruction",
            "claim_component": "automatic WEP composition silence",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "DD alpha and surface material deltas are nonzero",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1086_3_same_branch_product",
            "claim_component": "physical WEP product",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "range/profile/readout/coefficient same-branch lock remains missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1086_4_product_runner",
            "claim_component": "WEP product runner",
            "gate_pass": "false",
            "claim_allowed": str(product_status.get("claim_allowed", "")).lower(),
            "reason": f"valid_prediction_rows={product_status.get('valid_prediction_rows')}",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DECISION1086_0",
            "decision": "coupling bottleneck is confirmed",
            "because": "source-current zero remains conditional and DD material deltas are nonzero",
            "next_action": "try to parent-sign matter descent or fill real c_alpha/c_surface coefficients",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DECISION1086_1",
            "decision": "first parent-to-DD row is not fillable from current corpus",
            "because": "no parent EM derivative, nuclear binding derivative, or same-branch normalization exists",
            "next_action": "attack parent matter action descent before any empirical WEP claim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1086_0_1087",
            "next_target": "1087-Y5-R10-parent-matter-descent-zero-current-or-DD-coefficient-source-pack.md",
            "objective": "try to parent-sign S_matter descent and Lie_vX material silence for qbar_XT=0; if that fails, build a source-pack contract for c_alpha, c_surface, and tail coefficients with units and no-cancellation guards",
            "include": "matter action object-language; coframe/material parameter descent; hidden/source/domain terms; DD coefficient source schema; all-material no-cancellation policy",
            "exclude": "measured-G absorption; fitted cancellation line; unit source proxy; DD smoke as MTS claim; GitHub; formalization edits",
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
    source_current_rows: list[dict[str, str]],
    map_rows: list[dict[str, str]],
    delta_rows: list[dict[str, str]],
    pressure_rows: list[dict[str, str]],
    guard_rows: list[dict[str, str]],
    schema_rows: list[dict[str, str]],
    prediction_rows_: list[dict[str, str]],
    bound_rows_: list[dict[str, str]],
    product_status: dict[str, Any],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V1086_0_local_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in source_rows), "all cited local source paths and needles are present"))
    checks.append(("V1086_1_source_current_attempt_complete", any(row["attempt_id"] == "SCZ1086_5_verdict" and row["result"] == "SOURCE_CURRENT_ZERO_NOT_DERIVED" for row in source_current_rows), "source-current zero attempt ends in explicit nonclaim verdict"))
    checks.append(("V1086_2_parent_DD_map_first_row_blocked", any(row["map_id"] == "PDM1086_4_verdict" and row["current_status"] == "PARENT_DD_FIRST_ROW_NOT_FILLED" for row in map_rows), "parent-to-DD first row remains unfilled"))
    checks.append(("V1086_3_composition_deltas_nonzero", len(delta_rows) == 3 and all(parse_float(row["delta_abs"]) is None or parse_float(row["delta_abs"]) > 0 for row in delta_rows), "composition delta obstruction rows are present and nonclaim"))
    checks.append(("V1086_4_pressure_rows_numeric_nonclaim", len(pressure_rows) == 3 and all(parse_float(row["required_abs_coefficient_max"]) is not None and row["valid_for_claim"] == "false" for row in pressure_rows), "coefficient pressure rows are numeric and nonclaim"))
    checks.append(("V1086_5_no_cancellation_guards", len(guard_rows) == 4 and all(row["valid_for_claim"] == "false" for row in guard_rows), "no-cancellation guards are present"))
    checks.append(("V1086_6_acquisition_schema_nonclaim", len(schema_rows) == 5 and all(row["valid_for_claim"] == "false" for row in schema_rows), "source/current and coefficient acquisition schema remains nonclaim"))
    checks.append(("V1086_7_prediction_missing_nonclaim", any("MISSING_SOURCE_CURRENT_ZERO" in row["product_value"] and row["valid_for_claim"] == "false" for row in prediction_rows_), "generic prediction row remains missing coupling inputs"))
    checks.append(("V1086_8_bound_numeric", bool(bound_rows_) and parse_float(bound_rows_[0]["bound_value"]) is not None and float(bound_rows_[0]["bound_value"]) > 0 and bound_rows_[0]["valid_for_claim"] == "true", "MICROSCOPE bound import is positive numeric"))
    checks.append(("V1086_9_product_runner_refuses", product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False, "generic product runner reports no valid prediction rows and claim false"))
    checks.append(("V1086_10_claim_gates_safe", claim_rows and all(row["claim_allowed"] == "false" for row in claim_rows), "all claim gates deny WEP/local-GR claim"))
    checks.append(("V1086_11_next_target", any(row["next_target"].startswith("1087-Y5-R10-parent-matter-descent") for row in next_rows), "1087 handoff written"))
    generated_paths = list(outputs.values()) + [DOC]
    checks.append(("V1086_12_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in generated_paths), "all generated outputs are under post-checkpoint-work"))
    checks.append(("V1086_13_csv_parse", csv_outputs_parse([path for key, path in outputs.items() if key != "validation"]), "all 1086 CSV outputs parse cleanly"))
    checks.append(("V1086_14_formalization_untouched", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains zero"))
    checks.append(("V1086_SUMMARY", True, "source-current zero and parent-to-DD first row both remain unclosed; coupling bottleneck is now the next derivation target"))
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
    source_current_rows: list[dict[str, str]],
    map_rows: list[dict[str, str]],
    delta_rows: list[dict[str, str]],
    pressure_rows: list[dict[str, str]],
    guard_rows: list[dict[str, str]],
    schema_rows: list[dict[str, str]],
    product_status_rows_: list[dict[str, str]],
    product_comparisons: list[dict[str, Any]],
    claim_rows: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1086-Y5-R10 WEP source-current zero or parent-DD map first row",
            "",
            "## Current verdict",
            "1086 confirms the coupling bottleneck. The clean zero route would be qbar_XT=0 from parent matter descent, but the current corpus only has that as a conditional theorem. The first parent-to-DD coefficient row is also not fillable: c_alpha needs a parent EM derivative, c_surface needs a parent binding derivative, and both need the same X normalization/range/readout branch. Since the DD material deltas are nonzero, WEP silence cannot be assumed.",
            "",
            "## Local source register",
            md_table(source_rows, ["source_id", "relative_path", "exists", "needle_found", "note"]),
            "## Source-current zero theorem attempt",
            md_table(source_current_rows, ["attempt_id", "claim", "mathematical_statement", "result", "missing_for_claim"]),
            "## Parent-to-DD first-row attempt",
            md_table(map_rows, ["map_id", "parent_object", "candidate_formula", "current_status", "gap"]),
            "## Composition delta obstruction",
            md_table(delta_rows, ["obstruction_id", "component", "test_pair", "delta_value", "delta_abs", "meaning"]),
            "## Coefficient pressure rows",
            md_table(pressure_rows, ["pressure_id", "component", "source_material_product_abs", "required_abs_coefficient_max", "status", "claim_blocker"]),
            "## No-cancellation guard",
            md_table(guard_rows, ["guard_id", "forbidden_shortcut", "reason", "required_safe_route"]),
            "## Acquisition schema",
            md_table(schema_rows, ["schema_id", "needed_object", "current_status", "claim_blocker"]),
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
    source_current_rows = source_current_zero_attempt_rows()
    map_rows = parent_dd_map_first_row_attempt_rows()
    delta_rows = composition_delta_obstruction_rows()
    pressure_rows = coefficient_pressure_rows()
    guard_rows = no_cancellation_guard_rows()
    schema_rows = acquisition_schema_rows()
    prediction_rows_ = prediction_rows()
    bound_rows_ = bound_import_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R10_1086_SOURCE_REGISTER.csv",
        "source_current": OUT / "P8_Y5_R10_1086_SOURCE_CURRENT_ZERO_THEOREM_ATTEMPT.csv",
        "parent_DD_map": OUT / "P8_Y5_R10_1086_DD_PARENT_MAP_FIRST_ROW_ATTEMPT.csv",
        "composition_delta": OUT / "P8_Y5_R10_1086_COMPOSITION_DELTA_OBSTRUCTION.csv",
        "coefficient_pressure": OUT / "P8_Y5_R10_1086_NONCLAIM_COEFFICIENT_PRESSURE_ROWS.csv",
        "no_cancellation": OUT / "P8_Y5_R10_1086_NO_CANCELLATION_GUARD.csv",
        "acquisition_schema": OUT / "P8_Y5_R10_1086_ACQUISITION_SCHEMA.csv",
        "prediction": PREDICTION_TEMPLATE,
        "bound": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_R10_1086_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_R10_1086_PRODUCT_COMPARISON_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_R10_1086_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1086_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1086_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1086_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["source_current"], source_current_rows)
    write_csv(outputs["parent_DD_map"], map_rows)
    write_csv(outputs["composition_delta"], delta_rows)
    write_csv(outputs["coefficient_pressure"], pressure_rows)
    write_csv(outputs["no_cancellation"], guard_rows)
    write_csv(outputs["acquisition_schema"], schema_rows)
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
        source_current_rows,
        map_rows,
        delta_rows,
        pressure_rows,
        guard_rows,
        schema_rows,
        prediction_rows_,
        bound_rows_,
        product_status,
        claim_rows,
        next_rows,
    )
    write_csv(outputs["validation"], validation_rows)
    write_doc(
        source_rows,
        source_current_rows,
        map_rows,
        delta_rows,
        pressure_rows,
        guard_rows,
        schema_rows,
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
