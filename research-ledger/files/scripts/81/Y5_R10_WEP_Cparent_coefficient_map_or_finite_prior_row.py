from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1217"
TITLE = "1217-Y5-R10-WEP-Cparent-coefficient-map-or-finite-prior-row"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
MAP_ATTEMPT_PATH = OUT_DIR / f"{PACK_ID}_CPARENT_MAP_ATTEMPT.csv"
ZERO_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_COEFFICIENT_ZERO_AUDIT.csv"
PRIOR_CONTRACT_PATH = OUT_DIR / f"{PACK_ID}_FINITE_COEFFICIENT_PRIOR_CONTRACT.csv"
PRESSURE_REUSE_PATH = OUT_DIR / f"{PACK_ID}_NUMERIC_PRESSURE_REUSE.csv"
CANCELLATION_GUARD_PATH = OUT_DIR / f"{PACK_ID}_NO_CANCELLATION_GUARD.csv"
FEED_PATH = OUT_DIR / f"{PACK_ID}_WEP_FACTOR_FEED_UPDATE.csv"
RUNNER_PATH = OUT_DIR / f"{PACK_ID}_PRODUCT_RUNNER_STUB.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1217_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def is_false(row: dict[str, object], key: str) -> bool:
    value = row.get(key, False)
    if isinstance(value, bool):
        return value is False
    return str(value).strip().lower() == "false"


def find_row(rows: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    for row in rows:
        if row.get(key) == value:
            return row
    raise ValueError(f"missing row {key}={value}")


def float_field(row: dict[str, str], *keys: str) -> float:
    for key in keys:
        value = row.get(key, "")
        if str(value).strip():
            return float(value)
    raise ValueError(f"missing numeric field in {keys}: {row}")


def has_missing(row: dict[str, object]) -> bool:
    return "MISSING" in " ".join(str(value) for value in row.values()).upper()


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1217_0_1216_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1216_NEXT_TARGET.csv",
            "needle": "1217-Y5-R10-WEP-Cparent-coefficient-map-or-finite-prior-row.md",
            "purpose": "1216 handoff to C_parent coefficient-map target",
        },
        {
            "source_id": "SRC1217_1_1216_pressure",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1216_DD_SOURCE_MATERIAL_PRODUCT_PRESSURE.csv",
            "needle": "DDP1216_2_combined_abs",
            "purpose": "numeric source-material coefficient pressure rows",
        },
        {
            "source_id": "SRC1217_2_1216_update",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1216_SAME_NORM_PRODUCT_UPDATE.csv",
            "needle": "SNU1216_0_formula_update",
            "purpose": "same-norm product formula with C_parent lock",
        },
        {
            "source_id": "SRC1217_3_1215_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1215_SAME_NORM_PRODUCT_CONTRACT.csv",
            "needle": "SNP1215_0_WEP_formula",
            "purpose": "absolute same-basis WEP product contract",
        },
        {
            "source_id": "SRC1217_4_1080_Cparent",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1080_C_PARENT_COEFFICIENT_CONTRACT.csv",
            "needle": "CP1080_0_definition",
            "purpose": "original C_parent missing coefficient contract",
        },
        {
            "source_id": "SRC1217_5_1082_map",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1082_PARENT_TO_DD_COEFFICIENT_MAP_ATTEMPT.csv",
            "needle": "PTD1082_4_verdict",
            "purpose": "prior parent-to-DD map failure",
        },
        {
            "source_id": "SRC1217_6_1086_first_row",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1086_DD_PARENT_MAP_FIRST_ROW_ATTEMPT.csv",
            "needle": "PDM1086_4_verdict",
            "purpose": "first DD coefficient row obstruction",
        },
        {
            "source_id": "SRC1217_7_1086_delta_obstruction",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1086_COMPOSITION_DELTA_OBSTRUCTION.csv",
            "needle": "CDO1086_2_cancellation_line",
            "purpose": "forbidden TA6V-PtRh10 cancellation line",
        },
        {
            "source_id": "SRC1217_8_1086_guard",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1086_NO_CANCELLATION_GUARD.csv",
            "needle": "NCG1086_0_no_pair_tuning",
            "purpose": "no pair tuning policy",
        },
        {
            "source_id": "SRC1217_9_1087_source_pack",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1087_DD_COEFFICIENT_SOURCE_PACK.csv",
            "needle": "DDSP1087_0_c_alpha",
            "purpose": "coefficient source requirements",
        },
        {
            "source_id": "SRC1217_10_1087_template",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1087_DD_COEFFICIENT_SOURCE_PACK_TEMPLATE_NONCLAIM.csv",
            "needle": "DDCOEFF1087_0_alpha",
            "purpose": "nonclaim coefficient template",
        },
        {
            "source_id": "SRC1217_11_1096_zero",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1096_COEFFICIENT_ZERO_THEOREM_ATTEMPT.csv",
            "needle": "CZ1096_4_verdict",
            "purpose": "coefficient-vector zero theorem attempt",
        },
        {
            "source_id": "SRC1217_12_1096_prior",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1096_DD_COEFFICIENT_PRIOR_TEMPLATE_NONCLAIM.csv",
            "needle": "PRI1096_0_alpha",
            "purpose": "threshold-bounded prior template",
        },
        {
            "source_id": "SRC1217_13_1097_requirements",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1097_SOURCE_PRIOR_REQUIREMENTS.csv",
            "needle": "FSR1097_1_external_prior",
            "purpose": "requirements for source-backed finite prior",
        },
        {
            "source_id": "SRC1217_14_1084_readout",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv",
            "needle": "RIG1084_0_CMSM_arrays",
            "purpose": "official readout still missing",
        },
        {
            "source_id": "SRC1217_15_1083_profile",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv",
            "needle": "SCG1083_0_profile_weighting",
            "purpose": "source-profile weighting still missing",
        },
        {
            "source_id": "SRC1217_16_1100_alpha_norm",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1100_ALPHA_NORMALIZATION_DECOMPOSITION.csv",
            "needle": "Z1100_4_total",
            "purpose": "alpha normalization remains finite-branch, not theorem-zero",
        },
        {
            "source_id": "SRC1217_17_1101_route",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1101_ALPHA_ROUTE_DECISION.csv",
            "needle": "ROUTE1101_2_finite_alpha_products",
            "purpose": "finite alpha product route discipline",
        },
    ]

    source_rows: list[dict[str, object]] = []
    for spec in source_specs:
        path_exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_rows.append(
            {
                **spec,
                "absolute_path": str(source_path(spec["local_path"])),
                "path_exists": path_exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    pressure_1216 = read_csv(OUT_DIR / "P8_Y5_R10_1216_DD_SOURCE_MATERIAL_PRODUCT_PRESSURE.csv")
    alpha_pressure = find_row(pressure_1216, "pressure_id", "DDP1216_0_alpha")
    surface_pressure = find_row(pressure_1216, "pressure_id", "DDP1216_1_surface")
    combined_pressure = find_row(pressure_1216, "pressure_id", "DDP1216_2_combined_abs")
    cancellation_line = find_row(
        read_csv(OUT_DIR / "P8_Y5_R10_1086_COMPOSITION_DELTA_OBSTRUCTION.csv"),
        "obstruction_id",
        "CDO1086_2_cancellation_line",
    )

    alpha_threshold = float_field(alpha_pressure, "required_abs_coefficient_max_if_single_component")
    surface_threshold = float_field(surface_pressure, "required_abs_coefficient_max_if_single_component")
    combined_threshold = float_field(combined_pressure, "required_abs_coefficient_max_if_equal_component")

    map_rows = [
        {
            "map_id": "CMAP1217_0_mass_response_formula",
            "target": "C_parent -> DD material response vector",
            "candidate_formula": "partial_X ln m_A = c_0 + c_alpha Q_alpha_Coulomb(A) + c_surface Q_surface_binding(A) + q_tail(A)",
            "needed_parent_object": "parent ordinary-matter mass functional m_A[q(Phi), X] and its vertical derivative",
            "attempt_result": "FORMULA_RETAINED_AS_EXTERNAL_DD_DECOMPOSITION",
            "gap": "the DD formula is a comparator basis until the MTS parent action supplies the derivative and basis map",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "CMAP1217_1_alpha_operator_owner",
            "target": "c_alpha",
            "candidate_formula": "c_alpha := N_X partial_X ln alpha_EM in the DD Q_alpha_Coulomb convention",
            "needed_parent_object": "signed EM/fine-structure operator owner, normalization N_X, and material charge pullback",
            "attempt_result": "NOT_DERIVED",
            "gap": "PTD1082_1 and PDM1086_1 keep the parent EM derivative unsigned; Z1100_4 retains finite alpha branch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "CMAP1217_2_surface_operator_owner",
            "target": "c_surface",
            "candidate_formula": "c_surface := N_X partial_X ln a_surface_or_binding in the DD Q_surface_binding convention",
            "needed_parent_object": "signed nuclear/surface/binding response operator and same normalization N_X",
            "attempt_result": "NOT_DERIVED",
            "gap": "PTD1082_2 and PDM1086_2 keep the parent binding derivative unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "CMAP1217_3_same_branch_normalization",
            "target": "basis, units, signs, range, and readout placement",
            "candidate_formula": "one branch supplies Z_X, M_X^2, lambda_X, N_X, K_MICROSCOPE, Qeff_E, c_alpha, c_surface, q_tail",
            "needed_parent_object": "single same-branch normalization and Green-kernel/readout convention",
            "attempt_result": "NOT_DERIVED",
            "gap": "range/readout/profile gates remain live; C_parent cannot be mixed with source/readout rows from different branches",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "CMAP1217_4_no_absorption_shortcut",
            "target": "avoid hiding C_parent inside measured G, unit proxy, or fitted normalization",
            "candidate_formula": "B_species,WEP <= |K| sum_I |C_I| |R_source,I| |DeltaR_I|",
            "needed_parent_object": "explicit coefficient vector or theorem-zero certificate",
            "attempt_result": "SHORTCUTS_REJECTED",
            "gap": "unit proxies, measured-G absorption, and pair cancellation are not parent derivations",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "CMAP1217_5_verdict",
            "target": "claim-valid C_parent coefficient map",
            "candidate_formula": "C_parent -> (c_alpha, c_surface, q_tail) in the same DD/MTS branch",
            "needed_parent_object": "source-backed or parent-derived coefficient vector with units, signs, basis, and normalization",
            "attempt_result": "CPARENT_MAP_NOT_DERIVED",
            "gap": "1217 sharpens the exact coefficient contract but supplies no sourced/derived coefficient value",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    zero_rows = [
        {
            "zero_id": "ZERO1217_0_alpha",
            "coefficient": "c_alpha",
            "zero_route": "no independent hidden-dependent F_Q^2 term plus fixed gauge norm plus radiative/readout closure",
            "status": "CONDITIONAL_NOT_SIGNED",
            "obstruction": "Z1100_4 keeps hidden counterterm and readout terms alive; no-extra-F2 theorem is not promoted",
            "claim_effect": "alpha coefficient remains finite/missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "zero_id": "ZERO1217_1_surface",
            "coefficient": "c_surface",
            "zero_route": "ordinary nuclear/binding constants are parent superselection data with no hidden-visible morphism",
            "status": "CONDITIONAL_NOT_SIGNED",
            "obstruction": "constant-sector universality and binding operator owner remain unsigned",
            "claim_effect": "surface/binding coefficient remains finite/missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "zero_id": "ZERO1217_2_tail",
            "coefficient": "q_tail(A)",
            "zero_route": "alpha/surface DD rows form a complete material response basis and all remaining channels vanish",
            "status": "NOT_DERIVED",
            "obstruction": "DD alpha/surface rows are useful dominant channels but not a parent-complete basis",
            "claim_effect": "tail envelope remains a required lock",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "zero_id": "ZERO1217_3_vector",
            "coefficient": "C_parent vector",
            "zero_route": "CZ1096_1 conditional theorem: constant-sector universality plus no hidden-visible hom",
            "status": "COEFFICIENT_ZERO_NOT_DERIVED",
            "obstruction": "CZ1096_4 remains active; parent signatures, basis ownership, and readout closure are unsigned",
            "claim_effect": "do not claim WEP/local-GR pass from zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    prior_rows = [
        {
            "prior_id": "CPRIOR1217_0_alpha",
            "branch_id": "MTS_WEP_finite_branch",
            "coefficient": "c_alpha_DD",
            "value": "MISSING_PARENT_EM_DERIVATIVE_OR_SOURCE_BACKED_PRIOR",
            "units": "dimensionless_after_parent_normalization_in_DD_convention",
            "allowed_abs_threshold_from_1216": f"{alpha_threshold:.18e}",
            "threshold_source_row": "DDP1216_0_alpha",
            "promotion_rule": "requires parent EM derivative or explicit external coefficient prior; threshold alone is not a theory prediction",
            "status": "FINITE_PRIOR_VALUE_MISSING_THRESHOLD_AVAILABLE_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "prior_id": "CPRIOR1217_1_surface",
            "branch_id": "MTS_WEP_finite_branch",
            "coefficient": "c_surface_DD",
            "value": "MISSING_PARENT_BINDING_DERIVATIVE_OR_SOURCE_BACKED_PRIOR",
            "units": "dimensionless_after_parent_normalization_in_DD_convention",
            "allowed_abs_threshold_from_1216": f"{surface_threshold:.18e}",
            "threshold_source_row": "DDP1216_1_surface",
            "promotion_rule": "requires parent binding derivative or explicit external coefficient prior; no pair tuning",
            "status": "FINITE_PRIOR_VALUE_MISSING_THRESHOLD_AVAILABLE_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "prior_id": "CPRIOR1217_2_common_abs",
            "branch_id": "MTS_WEP_finite_branch",
            "coefficient": "c_common_abs_if_single_combined_scale",
            "value": "MISSING_PARENT_VECTOR_NORM_OR_SOURCE_BACKED_PRIOR",
            "units": "dimensionless_after_parent_normalization_in_DD_convention",
            "allowed_abs_threshold_from_1216": f"{combined_threshold:.18e}",
            "threshold_source_row": "DDP1216_2_combined_abs",
            "promotion_rule": "requires parent coefficient-vector norm or source-backed prior; common scale is a diagnostic only",
            "status": "FINITE_PRIOR_VALUE_MISSING_THRESHOLD_AVAILABLE_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "prior_id": "CPRIOR1217_3_tail",
            "branch_id": "MTS_WEP_finite_branch",
            "coefficient": "q_tail_envelope",
            "value": "MISSING_MATERIAL_BASIS_TAIL_ENVELOPE",
            "units": "dimensionless_eta_contribution_or_charge_envelope",
            "allowed_abs_threshold_from_1216": "MISSING_TAIL_THRESHOLD",
            "threshold_source_row": "MISSING_PARENT_OR_EMPIRICAL_ENVELOPE",
            "promotion_rule": "requires basis completeness theorem or empirical all-material residual envelope",
            "status": "TAIL_LOCK_MISSING_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "prior_id": "CPRIOR1217_4_same_branch_packet",
            "branch_id": "MTS_WEP_finite_branch",
            "coefficient": "lambda_X;K_MICROSCOPE;Qeff_E;N_X",
            "value": "MISSING_SAME_BRANCH_RANGE_READOUT_PROFILE_NORMALIZATION",
            "units": "m;dimensionless;DD_charge;normalization",
            "allowed_abs_threshold_from_1216": "not_applicable",
            "threshold_source_row": "SNP1215_1_basis_lock;RIG1084_0_CMSM_arrays;SCG1083_0_profile_weighting",
            "promotion_rule": "all factors must share one branch before any coefficient row can be claim-valid",
            "status": "SAME_BRANCH_PACKET_MISSING_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    pressure_reuse_rows = [
        {
            "reuse_id": "PREUSE1217_0_alpha",
            "coefficient": "c_alpha_DD",
            "source_material_product_abs": alpha_pressure["source_material_product_abs"],
            "eta_bound": alpha_pressure["eta_bound"],
            "threshold_abs": f"{alpha_threshold:.18e}",
            "source_row": "DDP1216_0_alpha",
            "meaning": "if a real same-branch c_alpha exists in this DD convention, this is the approximate absolute scale it must sit below",
            "status": "NUMERIC_PRESSURE_REUSED_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "reuse_id": "PREUSE1217_1_surface",
            "coefficient": "c_surface_DD",
            "source_material_product_abs": surface_pressure["source_material_product_abs"],
            "eta_bound": surface_pressure["eta_bound"],
            "threshold_abs": f"{surface_threshold:.18e}",
            "source_row": "DDP1216_1_surface",
            "meaning": "if a real same-branch c_surface exists in this DD convention, this is the approximate absolute scale it must sit below",
            "status": "NUMERIC_PRESSURE_REUSED_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "reuse_id": "PREUSE1217_2_common_abs",
            "coefficient": "c_common_abs_if_single_combined_scale",
            "source_material_product_abs": combined_pressure["source_material_product_abs"],
            "eta_bound": combined_pressure["eta_bound"],
            "threshold_abs": f"{combined_threshold:.18e}",
            "source_row": "DDP1216_2_combined_abs",
            "meaning": "equal/common coefficient diagnostic only; not a derived coefficient-vector norm",
            "status": "NUMERIC_PRESSURE_REUSED_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    cancellation_rows = [
        {
            "guard_id": "NCG1217_0_forbidden_pair_line",
            "object": "TA6V_minus_PtRh10 two-channel cancellation line",
            "value": cancellation_line["delta_value"],
            "source_row": "CDO1086_2_cancellation_line",
            "policy": "recorded only as an algebraic line; forbidden as evidence unless parent-derived before material choice and checked across materials",
            "status": "FORBIDDEN_CANCELLATION_LINE_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "guard_id": "NCG1217_1_absolute_sum_rule",
            "object": "WEP coefficient pressure calculation",
            "value": "use |c_alpha product_alpha| + |c_surface product_surface| + |tail| unless a sourced covariance/correlation model exists",
            "source_row": "SNP1215_3_no_cancellation;NCG1086_0_no_pair_tuning;AMC1087_0_pair_line_forbidden",
            "policy": "no signs chosen after seeing the material pair",
            "status": "ACTIVE_GUARD",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    feed_rows = [
        {
            "feed_id": "WFEED1217_0_to_WEP1215_6",
            "target_row": "WEP1215_6_C_parent",
            "field_to_fill": "strict finite-prior contract",
            "source_row": "CPRIOR1217_0_alpha;CPRIOR1217_1_surface;CPRIOR1217_2_common_abs;CPRIOR1217_3_tail",
            "update_value": "C_parent remains missing; threshold-bounded nonclaim prior rows staged",
            "current_status": "MISSING_COEFFICIENT_VALUE_STRICT_PRIOR_CONTRACT_AVAILABLE",
            "claim_policy": "do not promote until coefficient values are parent-derived or source-backed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "feed_id": "WFEED1217_1_to_SNU1216_0",
            "target_row": "SNU1216_0_formula_update",
            "field_to_fill": "C_parent factor",
            "source_row": "CMAP1217_5_verdict",
            "update_value": "map not derived; same-norm product remains blocked",
            "current_status": "CPARENT_MAP_BLOCKED",
            "claim_policy": "numeric DD source-material pressure rows stay scaffolding",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "feed_id": "WFEED1217_2_to_DSB1214_5",
            "target_row": "DSB1214_5_projection_map",
            "field_to_fill": "WEP_C_parent",
            "source_row": "CPRIOR1217_0_alpha;CPRIOR1217_1_surface;CPRIOR1217_3_tail",
            "update_value": "coefficient owner isolated as active missing projection factor",
            "current_status": "MISSING_PARENT_OPERATOR_COEFFICIENT_MAP",
            "claim_policy": "no local-GR/WEP/R10 claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner_rows = [
        {
            "runner_id": "APR1217_0_Cparent_prior_stub",
            "prediction_rows": 1,
            "valid_prediction_rows": 0,
            "numeric_pressure_rows": 3,
            "finite_prior_contract_rows": 5,
            "claim_allowed": False,
            "expected_result": "reject full WEP product while preserving numeric pressure and prior-contract rows",
            "reason": "C_parent values, same-branch normalization, K_MICROSCOPE, and profile weighting remain missing",
            "valid_for_claim": False,
        }
    ]

    decisions = [
        {
            "decision_id": "DEC1217_0_derivation_attempt",
            "decision": "C_parent map is not derived at 1217",
            "because": "alpha owner, surface owner, same-branch normalization, and tail basis are unsigned",
            "next_action": "hunt the parent alpha/surface operator owner instead of assigning coefficient values",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1217_1_finite_prior_contract",
            "decision": "stage explicit finite-prior rows as nonclaim",
            "because": "numeric pressure thresholds are useful discipline but are not coefficient sources",
            "next_action": "require parent derivation or external coefficient-prior provenance before promotion",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1217_2_no_cancellation",
            "decision": "keep the cancellation line forbidden",
            "because": "single material-pair cancellation would be post-hoc and not a field-theory result",
            "next_action": "only allow coefficient vectors fixed before material choice and checked across arenas",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1217_0_sources",
            "gate": "source path and needle audit",
            "status": "PASS",
            "reason": "all local inputs used by 1217 are traceable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1217_1_Cparent_map",
            "gate": "C_parent -> DD coefficient map",
            "status": "BLOCKED",
            "reason": "CMAP1217_5_verdict=CPARENT_MAP_NOT_DERIVED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1217_2_coefficient_zero",
            "gate": "C_parent coefficient vector theorem-zero",
            "status": "BLOCKED",
            "reason": "ZERO1217_3_vector=COEFFICIENT_ZERO_NOT_DERIVED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1217_3_finite_prior",
            "gate": "claim-valid finite coefficient prior",
            "status": "BLOCKED",
            "reason": "thresholds exist, but coefficient values and provenance remain missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1217_4_no_cancellation",
            "gate": "no pair-tuned cancellation",
            "status": "PASS_NONCLAIM",
            "reason": "forbidden cancellation line is explicitly quarantined",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1217_5_WEP_product",
            "gate": "claim-valid WEP/local-GR product",
            "status": "BLOCKED",
            "reason": "valid_prediction_rows=0 and same-branch packet is missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_rows = [
        {
            "next_id": "NEXT1217_0_1218",
            "target_file": "1218-Y5-R10-parent-alpha-surface-operator-owner-or-coefficient-prior-source.md",
            "target_script": "scripts/Y5_R10_parent_alpha_surface_operator_owner_or_coefficient_prior_source.py",
            "task": "try to identify the parent operator owner for alpha/surface material response; if that fails, acquire or explicitly reject source-backed coefficient prior rows",
            "success_condition": "either c_alpha/c_surface become parent-derived/theorem-zero, or the missing coefficient-prior source requirement is tightened into a source-acquisition ledger",
            "do_not_do": "do not invent coefficient priors; do not use threshold bounds as predictions; do not tune cancellation; do not claim WEP/local-GR/R10; do not edit formalization-workbench or push GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    source_fields = ["source_id", "local_path", "needle", "purpose", "absolute_path", "path_exists", "needle_found", "valid_for_claim", "claim_allowed"]
    map_fields = ["map_id", "target", "candidate_formula", "needed_parent_object", "attempt_result", "gap", "valid_for_claim", "claim_allowed"]
    zero_fields = ["zero_id", "coefficient", "zero_route", "status", "obstruction", "claim_effect", "valid_for_claim", "claim_allowed"]
    prior_fields = ["prior_id", "branch_id", "coefficient", "value", "units", "allowed_abs_threshold_from_1216", "threshold_source_row", "promotion_rule", "status", "valid_for_claim", "claim_allowed"]
    pressure_fields = ["reuse_id", "coefficient", "source_material_product_abs", "eta_bound", "threshold_abs", "source_row", "meaning", "status", "valid_for_claim", "claim_allowed"]
    guard_fields = ["guard_id", "object", "value", "source_row", "policy", "status", "valid_for_claim", "claim_allowed"]
    feed_fields = ["feed_id", "target_row", "field_to_fill", "source_row", "update_value", "current_status", "claim_policy", "valid_for_claim", "claim_allowed"]
    runner_fields = ["runner_id", "prediction_rows", "valid_prediction_rows", "numeric_pressure_rows", "finite_prior_contract_rows", "claim_allowed", "expected_result", "reason", "valid_for_claim"]
    decision_fields = ["decision_id", "decision", "because", "next_action", "valid_for_claim", "claim_allowed"]
    gate_fields = ["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"]
    next_fields = ["next_id", "target_file", "target_script", "task", "success_condition", "do_not_do", "valid_for_claim", "claim_allowed"]

    write_csv(SOURCE_REGISTER_PATH, source_rows, source_fields)
    write_csv(MAP_ATTEMPT_PATH, map_rows, map_fields)
    write_csv(ZERO_AUDIT_PATH, zero_rows, zero_fields)
    write_csv(PRIOR_CONTRACT_PATH, prior_rows, prior_fields)
    write_csv(PRESSURE_REUSE_PATH, pressure_reuse_rows, pressure_fields)
    write_csv(CANCELLATION_GUARD_PATH, cancellation_rows, guard_fields)
    write_csv(FEED_PATH, feed_rows, feed_fields)
    write_csv(RUNNER_PATH, runner_rows, runner_fields)
    write_csv(DECISION_PATH, decisions, decision_fields)
    write_csv(CLAIM_GATES_PATH, claim_gates, gate_fields)
    write_csv(NEXT_PATH, next_rows, next_fields)

    csvs_to_parse = [
        SOURCE_REGISTER_PATH,
        MAP_ATTEMPT_PATH,
        ZERO_AUDIT_PATH,
        PRIOR_CONTRACT_PATH,
        PRESSURE_REUSE_PATH,
        CANCELLATION_GUARD_PATH,
        FEED_PATH,
        RUNNER_PATH,
        DECISION_PATH,
        CLAIM_GATES_PATH,
        NEXT_PATH,
    ]
    csv_parse_ok = True
    parse_details: list[str] = []
    for csv_path in csvs_to_parse:
        try:
            rows = read_csv(csv_path)
            parse_details.append(f"{csv_path.name}:{len(rows)}")
        except Exception as exc:
            csv_parse_ok = False
            parse_details.append(f"{csv_path.name}:ERROR:{exc}")

    formalization_recent = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*"):
            if path.is_file():
                mtime = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
                if mtime >= RUN_STARTED_UTC:
                    formalization_recent.append(path)

    all_sources_exist = all(bool(row["path_exists"]) for row in source_rows)
    all_needles_found = all(bool(row["needle_found"]) for row in source_rows)
    map_not_derived = any(row["map_id"] == "CMAP1217_5_verdict" and row["attempt_result"] == "CPARENT_MAP_NOT_DERIVED" for row in map_rows)
    zero_not_overclaimed = any(row["zero_id"] == "ZERO1217_3_vector" and row["status"] == "COEFFICIENT_ZERO_NOT_DERIVED" for row in zero_rows)
    thresholds_positive = alpha_threshold > 0 and surface_threshold > 0 and combined_threshold > 0
    prior_threshold_rows = [row for row in prior_rows if row["prior_id"] in {"CPRIOR1217_0_alpha", "CPRIOR1217_1_surface", "CPRIOR1217_2_common_abs"}]
    prior_rows_nonclaim = all(is_false(row, "valid_for_claim") and is_false(row, "claim_allowed") for row in prior_rows)
    missing_rows_nonclaim = all(not (has_missing(row) and not is_false(row, "valid_for_claim")) for row in prior_rows + feed_rows + source_rows)
    cancellation_forbidden = any(row["guard_id"] == "NCG1217_0_forbidden_pair_line" and row["status"] == "FORBIDDEN_CANCELLATION_LINE_NONCLAIM" for row in cancellation_rows)
    pressure_reuse_positive = all(float(row["threshold_abs"]) > 0 and float(row["source_material_product_abs"]) > 0 for row in pressure_reuse_rows)
    runner_refuses = runner_rows[0]["valid_prediction_rows"] == 0 and not runner_rows[0]["claim_allowed"]
    claim_locks_blocked = all(
        any(row["gate_id"] == gate_id and row["status"] == "BLOCKED" for row in claim_gates)
        for gate_id in ["GATE1217_1_Cparent_map", "GATE1217_2_coefficient_zero", "GATE1217_3_finite_prior", "GATE1217_5_WEP_product"]
    )
    no_claim = all(
        is_false(row, "valid_for_claim") and is_false(row, "claim_allowed")
        for row in map_rows + zero_rows + prior_rows + pressure_reuse_rows + cancellation_rows + feed_rows + runner_rows + decisions + claim_gates + next_rows
    )
    formalization_untouched = len(formalization_recent) == 0
    next_1218 = next_rows[0]["target_file"].startswith("1218-")

    validation_rows = [
        validation_row("VAL1217_0_sources_exist", "all cited local sources exist", all_sources_exist, f"{sum(bool(row['path_exists']) for row in source_rows)}/{len(source_rows)} sources exist"),
        validation_row("VAL1217_1_needles_found", "all cited source needles found", all_needles_found, f"{sum(bool(row['needle_found']) for row in source_rows)}/{len(source_rows)} needles found"),
        validation_row("VAL1217_2_map_not_overclaimed", "C_parent map failure is explicit", map_not_derived, "CMAP1217_5_verdict=CPARENT_MAP_NOT_DERIVED"),
        validation_row("VAL1217_3_zero_not_overclaimed", "coefficient zero is not overclaimed", zero_not_overclaimed, "ZERO1217_3_vector=COEFFICIENT_ZERO_NOT_DERIVED"),
        validation_row("VAL1217_4_thresholds_positive", "finite-prior thresholds are positive", thresholds_positive, "; ".join(f"{row['prior_id']}={row['allowed_abs_threshold_from_1216']}" for row in prior_threshold_rows)),
        validation_row("VAL1217_5_prior_rows_nonclaim", "prior rows remain nonclaim", prior_rows_nonclaim, "all finite prior rows valid_for_claim=false and claim_allowed=false"),
        validation_row("VAL1217_6_missing_rows_nonclaim", "no MISSING row is valid for claim", missing_rows_nonclaim, "missing coefficient/prior/source values are quarantined"),
        validation_row("VAL1217_7_cancellation_forbidden", "pair cancellation line is forbidden", cancellation_forbidden, cancellation_line["delta_value"]),
        validation_row("VAL1217_8_pressure_reuse_positive", "numeric pressure reuse rows are positive", pressure_reuse_positive, "; ".join(f"{row['reuse_id']}={row['threshold_abs']}" for row in pressure_reuse_rows)),
        validation_row("VAL1217_9_runner_refuses", "runner stub refuses missing full product", runner_refuses, "valid_prediction_rows=0 and claim_allowed=false"),
        validation_row("VAL1217_10_claim_locks_blocked", "claim locks remain blocked", claim_locks_blocked, "Cparent map, zero theorem, finite prior, and WEP product blocked"),
        validation_row("VAL1217_11_nonclaim_policy", "all generated rows remain nonclaim", no_claim, "valid_for_claim=false and claim_allowed=false throughout"),
        validation_row("VAL1217_12_csv_parse", "all generated CSVs parse cleanly", csv_parse_ok, "; ".join(parse_details)),
        validation_row("VAL1217_13_formalization_untouched", "formalization-workbench untouched during run", formalization_untouched, f"formalization_recent_after_run_start_count={len(formalization_recent)}"),
        validation_row("VAL1217_14_next_target", "next target is staged", next_1218, next_rows[0]["target_file"]),
    ]
    validation_pass = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        validation_row(
            "VAL1217_15_overall",
            "overall 1217 validation",
            validation_pass,
            "1217 C_parent map/prior pack is reproducible, nonclaim, and claim-locked" if validation_pass else "one or more validation checks failed",
        )
    )
    validation_fields = ["check_id", "check", "status", "details", "valid_for_claim", "claim_allowed"]
    write_csv(VALIDATION_PATH, validation_rows, validation_fields)

    doc = f"""# 1217 Y5/R10 WEP Cparent Coefficient Map Or Finite Prior Row

**Current verdict:** 1217 does **not** derive the `C_parent -> (c_alpha, c_surface, q_tail)` map and does **not** prove the coefficient vector zero. It tightens the exact coupling contract and stages finite coefficient-prior rows as nonclaim scaffolding.

**Main progress:** the missing object is now sharper: we need a parent-owned alpha operator, a parent-owned surface/binding operator, a tail/basis envelope, and one same-branch normalization tying coefficients to range, source profile, and MICROSCOPE readout. The coupling is the lock; the numeric WEP pressure rows only tell us the scale a future coefficient would have to survive.

**No-claim rule:** thresholds from WEP are not theory priors. A coefficient row becomes claim-valid only if the value is derived from the parent action or sourced externally with units, signs, branch, profile, and readout provenance.

## Source Register

{markdown_table(source_rows, source_fields)}

## Cparent Map Attempt

{markdown_table(map_rows, map_fields)}

## Coefficient Zero Audit

{markdown_table(zero_rows, zero_fields)}

## Finite Coefficient Prior Contract

{markdown_table(prior_rows, prior_fields)}

## Numeric Pressure Reuse

{markdown_table(pressure_reuse_rows, pressure_fields)}

## No-Cancellation Guard

{markdown_table(cancellation_rows, guard_fields)}

## WEP Factor Feed Update

{markdown_table(feed_rows, feed_fields)}

## Product Runner Stub

{markdown_table(runner_rows, runner_fields)}

## Decision Ledger

{markdown_table(decisions, decision_fields)}

## Claim Gates

{markdown_table(claim_gates, gate_fields)}

## Next Target

{markdown_table(next_rows, next_fields)}

## Validation

{markdown_table(validation_rows, validation_fields)}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")

    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"validation_pass={validation_pass}")
    print("C_parent_map_derived=false")
    print("valid_prediction_rows=0")


if __name__ == "__main__":
    main()
