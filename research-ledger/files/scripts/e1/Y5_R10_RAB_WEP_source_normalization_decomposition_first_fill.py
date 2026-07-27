from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1325"
TITLE = "1325-Y5-R10-RAB-WEP-source-normalization-decomposition-first-fill"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
PRODUCT_DECOMPOSITION_PATH = OUT_DIR / f"{PACK_ID}_WEP_PRODUCT_DECOMPOSITION.csv"
INPUT_MATRIX_PATH = OUT_DIR / f"{PACK_ID}_FIRST_FILL_INPUT_MATRIX.csv"
RUNNER_PATH = OUT_DIR / f"{PACK_ID}_WEP_DECOMPOSITION_RUNNER.csv"
BLOCKER_PATH = OUT_DIR / f"{PACK_ID}_BLOCKER_LEDGER.csv"
ANTI_SHORTCUT_PATH = OUT_DIR / f"{PACK_ID}_ANTI_SHORTCUT_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1325_VALIDATION.csv"


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
    return {"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "details": details}


def is_false(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no"}


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    return all(
        is_false(row.get("valid_for_claim", False)) and is_false(row.get("claim_allowed", False))
        for rows in tables
        for row in rows
    )


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        PRODUCT_DECOMPOSITION_PATH,
        INPUT_MATRIX_PATH,
        RUNNER_PATH,
        BLOCKER_PATH,
        ANTI_SHORTCUT_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def first(rows: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    return next(row for row in rows if row.get(key) == value)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1325_0_1324_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1324_NEXT_TARGET.csv",
            "needle": "NEXT1324_0_1325",
            "role": "handoff into WEP source-normalization decomposition",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1325_1_1324_route",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1324_WEP_SOURCE_NORMALIZATION_ROUTE.csv",
            "needle": "WEP1324_0_beta_source_alpha",
            "role": "WEP route fields selected by 1324",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1325_2_1316_formula",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1316_P0_PRODUCT_FORMULA_REQUIREMENTS.csv",
            "needle": "FORM1316_2_wep",
            "role": "canonical WEP product formula requirements",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1325_3_1317_runner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1317_PRIORITY_RUNNER_REFUSAL_TABLE.csv",
            "needle": "RUN1317_2_run1314_2_wep",
            "role": "prior refused WEP runner row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1325_4_1053_beta",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1053_BETA_SOURCE_ALPHA_DERIVATION_AUDIT.csv",
            "needle": "BSA1053_1_alpha_marker_source",
            "role": "beta_source_alpha source-chain audit",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1325_5_1053_tau",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1053_TAU_WEP_R10_PROJECTION_AUDIT.csv",
            "needle": "TPR1053_1_tau_WEP_definition",
            "role": "tau_WEP projection audit",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1325_6_1053_material",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1053_WEP_COMPOSITION_CHARGE_MATRIX.csv",
            "needle": "WCM1053_4",
            "role": "Ti/Pt alpha-Coulomb smoke material delta",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1325_7_1094_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1094_DIRECT_WEP_PRODUCT_CONTRACT.csv",
            "needle": "DWP1094_4_required_prediction",
            "role": "direct WEP alpha product contract",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1325_8_1224_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1224_FINITE_SOURCE_WEIGHT_INPUT_CONTRACT.csv",
            "needle": "FSW1224_1_delta_w",
            "role": "finite source-weight input contract",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1325_9_1224_product",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1224_SOURCE_WEIGHT_PRODUCT_LAW.csv",
            "needle": "PROD1224_0_source_weight",
            "role": "source-weight product law",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1325_10_1225_tau",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1225_TAU_WEP_SOURCE_ACQUISITION_TABLE.csv",
            "needle": "ACQ1225_0_official_readout_arrays",
            "role": "tau_WEP acquisition blockers",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1325_11_1080_pack",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1080_FINITE_WEP_INPUT_PACK_NONCLAIM.csv",
            "needle": "FIP1080_0_product_formula",
            "role": "finite WEP product formula and input pack",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1325_12_983_material",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_983_MATERIAL_CONSTITUENTS.csv",
            "needle": "WEB983_0_MICROSCOPE_CQG_COMPOSITION",
            "role": "MICROSCOPE alloy composition context",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    dwp_rows = read_csv(source_path("source-intake/mts_residuals/P8_Y5_R10_1094_DIRECT_WEP_PRODUCT_CONTRACT.csv"))
    dwp_bound = first(dwp_rows, "contract_id", "DWP1094_3_direct_product_bound")
    dwp_required = first(dwp_rows, "contract_id", "DWP1094_4_required_prediction")
    source_weight_rows = read_csv(source_path("source-intake/mts_residuals/P8_Y5_R10_1224_SOURCE_WEIGHT_PRODUCT_LAW.csv"))
    source_weight_law = first(source_weight_rows, "product_id", "PROD1224_0_source_weight")
    material_rows = read_csv(source_path("source-intake/mts_residuals/P8_Y5_R10_1053_WEP_COMPOSITION_CHARGE_MATRIX.csv"))
    alpha_delta = first(material_rows, "matrix_id", "WCM1053_4")
    surface_delta = first(material_rows, "matrix_id", "WCM1053_5")

    product_decomposition = [
        {
            "decomp_id": "DECOMP1325_0_alpha_coulomb_factorized",
            "branch": "alpha_Coulomb_smoke",
            "product_law": "P_WEP_alpha = abs(beta_source_alpha * b_alpha * tau_WEP * DeltaQ_alpha_AB)",
            "threshold": dwp_bound["numeric_value"],
            "threshold_units": dwp_bound["units"],
            "available_inputs": "DeltaQ_alpha_AB smoke value; eta/product threshold",
            "missing_inputs": "beta_source_alpha;b_alpha_or_zero_certificate;tau_WEP;source_worldtube;readout_kernel",
            "current_status": "DECOMPOSED_NOT_SCOREABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decomp_id": "DECOMP1325_1_alpha_coulomb_direct",
            "branch": "alpha_Coulomb_direct",
            "product_law": "P_WEP_alpha_direct = abs(parent predicted eta_AB residual / unit_source_eta_prediction)",
            "threshold": dwp_bound["numeric_value"],
            "threshold_units": dwp_bound["units"],
            "available_inputs": "comparison threshold only",
            "missing_inputs": dwp_required["numeric_value"],
            "current_status": "MISSING_DIRECT_PRODUCT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decomp_id": "DECOMP1325_2_source_weight_relative",
            "branch": "relative_source_weight",
            "product_law": source_weight_law["formula"],
            "threshold": "2.8e-15",
            "threshold_units": "dimensionless_eta",
            "available_inputs": "eta Ti/Pt bound anchor",
            "missing_inputs": source_weight_law["missing_inputs"],
            "current_status": source_weight_law["current_numeric_status"],
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decomp_id": "DECOMP1325_3_full_finite_tensor",
            "branch": "full_parent_basis",
            "product_law": "P_WEP = sum_I C_parent^I * R_source_I^Earth * DeltaR_material_I projected by K_MICROSCOPE",
            "threshold": "2.8e-15 or branch-specific normalized product threshold",
            "threshold_units": "dimensionless_eta",
            "available_inputs": "composition context; DD smoke alpha/surface deltas; readout structure source-backed",
            "missing_inputs": "C_parent vector; same-basis Earth source vector; full material tensor; official arrays/product convention",
            "current_status": "FORMULA_READY_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    input_matrix = [
        {
            "input_id": "IN1325_0_eta_bound",
            "object": "eta_TiPt_bound",
            "current_value_or_status": "2.8e-15",
            "units": "dimensionless",
            "source": "P8_Y5_R10_1094_DIRECT_WEP_PRODUCT_CONTRACT.csv:DWP1094_0_observable",
            "fill_status": "BOUND_ANCHOR_AVAILABLE",
            "usable_role": "comparison fence only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "IN1325_1_alpha_product_threshold",
            "object": "P_WEP_alpha_direct threshold",
            "current_value_or_status": dwp_bound["numeric_value"],
            "units": dwp_bound["units"],
            "source": "P8_Y5_R10_1094_DIRECT_WEP_PRODUCT_CONTRACT.csv:DWP1094_3_direct_product_bound",
            "fill_status": "THRESHOLD_AVAILABLE_NONCLAIM",
            "usable_role": "private pressure target",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "IN1325_2_deltaQ_alpha_smoke",
            "object": "DeltaQ_alpha_AB",
            "current_value_or_status": alpha_delta["delta_Q_abs_for_pair"],
            "units": "dimensionless",
            "source": "P8_Y5_R10_1053_WEP_COMPOSITION_CHARGE_MATRIX.csv:WCM1053_4",
            "fill_status": "SMOKE_NUMERIC_AVAILABLE",
            "usable_role": "external DD alpha/Coulomb smoke convention only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "IN1325_3_deltaQ_surface_smoke",
            "object": "DeltaQ_surface_binding",
            "current_value_or_status": surface_delta["delta_Q_abs_for_pair"],
            "units": "dimensionless",
            "source": "P8_Y5_R10_1053_WEP_COMPOSITION_CHARGE_MATRIX.csv:WCM1053_5",
            "fill_status": "SMOKE_NUMERIC_AVAILABLE",
            "usable_role": "external DD surface/binding smoke convention only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "IN1325_4_beta_source_alpha",
            "object": "beta_source_alpha",
            "current_value_or_status": "MISSING_SOURCE_NORMALIZATION",
            "units": "dimensionless_or_branch_convention",
            "source": "P8_Y5_R10_1053_BETA_SOURCE_ALPHA_DERIVATION_AUDIT.csv:BSA1053_5_verdict",
            "fill_status": "MISSING",
            "usable_role": "required alpha/source coupling input",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "IN1325_5_balpha",
            "object": "b_alpha_or_zero_certificate",
            "current_value_or_status": "MISSING_SOURCE_BACKED_COEFFICIENT_OR_PARENT_PRIMITIVE",
            "units": "dimensionless",
            "source": "P8_Y5_R10_1316_P0_SOURCE_REQUIREMENT_LEDGER.csv:REQ1316_0_balpha",
            "fill_status": "MISSING",
            "usable_role": "required alpha branch coefficient unless direct product bypass is sourced",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "IN1325_6_tau_WEP",
            "object": "tau_WEP",
            "current_value_or_status": "MISSING_LAB_SOURCE_ORBIT_PROJECTION",
            "units": "dimensionless",
            "source": "P8_Y5_R10_1225_SYMBOLIC_TAU_WEP_FORMULA.csv:FORM1225_0_tau_WEP_functional",
            "fill_status": "SYMBOLIC_ONLY_NONCLAIM",
            "usable_role": "required WEP projection/readout factor",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "IN1325_7_delta_w",
            "object": "Delta_w_TiPt",
            "current_value_or_status": "MISSING_NUMERIC_PRIOR_WIDTH",
            "units": "dimensionless",
            "source": "P8_Y5_R10_1224_FINITE_SOURCE_WEIGHT_INPUT_CONTRACT.csv:FSW1224_1_delta_w",
            "fill_status": "MISSING",
            "usable_role": "required relative source-weight coupling input",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "IN1325_8_readout_arrays",
            "object": "K_MICROSCOPE/source-weight readout kernel",
            "current_value_or_status": "OFFICIAL_ARRAYS_NOT_IMPORTED",
            "units": "eta projection convention",
            "source": "P8_Y5_R10_1225_TAU_WEP_SOURCE_ACQUISITION_TABLE.csv:ACQ1225_0_official_readout_arrays",
            "fill_status": "MISSING",
            "usable_role": "required for claim-grade tau_WEP/readout normalization",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "IN1325_9_direct_product",
            "object": "MTS P_WEP_alpha_direct",
            "current_value_or_status": dwp_required["numeric_value"],
            "units": dwp_required["units"],
            "source": "P8_Y5_R10_1094_DIRECT_WEP_PRODUCT_CONTRACT.csv:DWP1094_4_required_prediction",
            "fill_status": "MISSING",
            "usable_role": "preferred bypass if parent variation gives observable directly",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner = [
        {
            "runner_id": "RUN1325_0_alpha_coulomb_factorized",
            "product_branch": "alpha_Coulomb_smoke",
            "comparison_threshold": dwp_bound["numeric_value"],
            "threshold_units": dwp_bound["units"],
            "predicted_value": "MISSING_BETA_SOURCE_ALPHA_B_ALPHA_TAU_WEP_PRODUCT",
            "available_inputs": "DeltaQ_alpha_AB_smoke;threshold",
            "missing_inputs": "beta_source_alpha;b_alpha_or_zero_certificate;tau_WEP;source_worldtube;readout_kernel",
            "runner_status": "REFUSED",
            "refusal_reason": "required coupling/readout inputs missing; smoke material delta is not a prediction",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN1325_1_source_weight_relative",
            "product_branch": "relative_source_weight",
            "comparison_threshold": "2.8e-15",
            "threshold_units": "dimensionless_eta",
            "predicted_value": "MISSING_DELTA_W_TIPT_TIMES_TAU_WEP",
            "available_inputs": "eta_bound",
            "missing_inputs": source_weight_law["missing_inputs"],
            "runner_status": "REFUSED",
            "refusal_reason": "Delta_w_TiPt and tau_WEP/readout/source profile not sourced",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN1325_2_direct_wep_product",
            "product_branch": "direct_parent_observable",
            "comparison_threshold": dwp_bound["numeric_value"],
            "threshold_units": dwp_bound["units"],
            "predicted_value": dwp_required["numeric_value"],
            "available_inputs": "comparison_threshold_only",
            "missing_inputs": "parent predicted eta residual;source path;readout convention;sign convention",
            "runner_status": "REFUSED",
            "refusal_reason": "direct parent product not derived or sourced",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    blocker = [
        {
            "blocker_id": "BLK1325_0_beta_source_alpha",
            "blocks_runner": "RUN1325_0_alpha_coulomb_factorized",
            "missing_object": "beta_source_alpha",
            "current_status": "MISSING_SOURCE_NORMALIZATION",
            "required_resolution": "derive source-normalization zero/finite coefficient or source numeric prior",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "BLK1325_1_balpha",
            "blocks_runner": "RUN1325_0_alpha_coulomb_factorized",
            "missing_object": "b_alpha_or_zero_certificate",
            "current_status": "MISSING_SOURCE_BACKED_COEFFICIENT_OR_PARENT_PRIMITIVE",
            "required_resolution": "source coefficient or signed no-hidden/radiative/readout theorem-zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "BLK1325_2_tau_WEP",
            "blocks_runner": "RUN1325_0_alpha_coulomb_factorized;RUN1325_1_source_weight_relative",
            "missing_object": "tau_WEP",
            "current_status": "SYMBOLIC_ONLY_NONCLAIM",
            "required_resolution": "source worldtube/orbit/readout functional with normalization or direct observable bypass",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "BLK1325_3_delta_w",
            "blocks_runner": "RUN1325_1_source_weight_relative",
            "missing_object": "Delta_w_TiPt",
            "current_status": "MISSING_NUMERIC_PRIOR_WIDTH",
            "required_resolution": "prove source-weight zero or source finite Ti/Pt relative weight prior",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "BLK1325_4_readout_arrays",
            "blocks_runner": "RUN1325_0_alpha_coulomb_factorized;RUN1325_1_source_weight_relative",
            "missing_object": "official MICROSCOPE readout arrays/product convention",
            "current_status": "OFFICIAL_ARRAYS_NOT_IMPORTED",
            "required_resolution": "import official arrays/export or use a source-backed averaged kernel",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "BLK1325_5_direct_product",
            "blocks_runner": "RUN1325_2_direct_wep_product",
            "missing_object": "MTS P_WEP_alpha_direct",
            "current_status": "MISSING_DIRECT_PRODUCT",
            "required_resolution": "derive parent variation to eta_AB observable or source numeric direct product",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    anti_shortcut = [
        {
            "gate_id": "SHORT1325_0_no_unity_couplings",
            "shortcut": "set beta_source_alpha, b_alpha, tau_WEP, or Delta_w_TiPt to unity/zero by taste",
            "enforcement": "REFUSED unless parent theorem or source-backed value exists",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1325_1_no_threshold_prediction",
            "shortcut": "use eta or normalized threshold as the MTS prediction",
            "enforcement": "REFUSED; thresholds are comparison fences only",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1325_2_no_smoke_tensor_claim",
            "shortcut": "treat DD alpha/surface smoke deltas as the full MTS material tensor",
            "enforcement": "REFUSED; smoke rows remain external nonclaim context",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1325_3_no_cancellation_pass",
            "shortcut": "claim WEP pass through signed material/source cancellation",
            "enforcement": "REFUSED without full signed material/source/readout model",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1325_4_no_cross_arena_transfer",
            "shortcut": "reuse clock/R10 rows as WEP evidence",
            "enforcement": "REFUSED until a parent branch/readout functor is signed",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1325_0_wep_decomposed",
            "decision": "WEP route is decomposed into factorized alpha, source-weight, and direct-product branches",
            "because": "clock wait-state showed the coupling/readout product is the real missing object",
            "effect": "WEP now has explicit runnable refusal rows instead of one vague missing-coupling row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1325_1_no_score",
            "decision": "no WEP score or pass/fail is claimed",
            "because": "all branches still miss source-normalization, tau/readout, direct product, or full material/source inputs",
            "effect": "private pressure targets remain useful but nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1325_2_best_next",
            "decision": "attack source-weight owner or finite Delta_w prior next",
            "because": "Delta_w/source-weight is the clean coupling bottleneck and less dependent on cosmological/clock assumptions",
            "effect": "1326 should try theorem-zero first, otherwise create a finite prior-width source row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1325_0_1326",
            "target_file": "1326-Y5-R10-RAB-WEP-source-weight-owner-zero-or-finite-Delta-w-prior.md",
            "target_script": "scripts/Y5_R10_RAB_WEP_source_weight_owner_zero_or_finite_Delta_w_prior.py",
            "task": "try to prove Delta_w_TiPt=0 from parent source-weight ownership; if that fails, stage a finite Delta_w prior-width row with source/provenance and keep WEP nonclaim",
            "success_condition": "source-weight branch either gains a parent-signed zero certificate or an explicit finite Delta_w input contract without unity/cancellation shortcuts",
            "do_not": "do not set Delta_w=0 by naturality alone; do not use smoke material deltas as full tensor; do not claim WEP pass",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(PRODUCT_DECOMPOSITION_PATH, product_decomposition)
    write_csv(INPUT_MATRIX_PATH, input_matrix)
    write_csv(RUNNER_PATH, runner)
    write_csv(BLOCKER_PATH, blocker)
    write_csv(ANTI_SHORTCUT_PATH, anti_shortcut)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)

    validations: list[dict[str, object]] = []
    sources_ok = all(row["exists"] and row["needle_found"] for row in source_register)
    validations.append(
        validation_row(
            "VAL1325_0_sources_exist",
            "registered source paths exist and anchors are found",
            sources_ok,
            f"{sum(1 for row in source_register if row['exists'] and row['needle_found'])}/{len(source_register)} source anchors found",
        )
    )
    branches = {row["branch"] for row in product_decomposition}
    validations.append(
        validation_row(
            "VAL1325_1_branches_decomposed",
            "WEP decomposition covers alpha factorized, alpha direct, source-weight, and full tensor branches",
            branches >= {"alpha_Coulomb_smoke", "alpha_Coulomb_direct", "relative_source_weight", "full_parent_basis"},
            ";".join(sorted(branches)),
        )
    )
    required_inputs = {row["object"] for row in input_matrix}
    validations.append(
        validation_row(
            "VAL1325_2_input_matrix_covers_coupling_gap",
            "first-fill matrix includes available anchors and missing coupling/readout inputs",
            {"beta_source_alpha", "b_alpha_or_zero_certificate", "tau_WEP", "Delta_w_TiPt", "MTS P_WEP_alpha_direct"} <= required_inputs,
            ";".join(row["input_id"] for row in input_matrix),
        )
    )
    runner_refuses = all(row["runner_status"] == "REFUSED" and not row["score_ready"] for row in runner)
    validations.append(
        validation_row(
            "VAL1325_3_runner_refuses_all_branches",
            "runner refuses all current WEP branches and scores nothing",
            runner_refuses,
            ";".join(f"{row['runner_id']}={row['refusal_reason']}" for row in runner),
        )
    )
    blocker_ok = {row["missing_object"] for row in blocker} >= {
        "beta_source_alpha",
        "b_alpha_or_zero_certificate",
        "tau_WEP",
        "Delta_w_TiPt",
        "official MICROSCOPE readout arrays/product convention",
        "MTS P_WEP_alpha_direct",
    }
    validations.append(
        validation_row(
            "VAL1325_4_blockers_recorded",
            "blocker ledger records coupling, tau, readout, and direct-product missing objects",
            blocker_ok,
            ";".join(row["blocker_id"] for row in blocker),
        )
    )
    shortcut_ok = all(row["status"] == "ENFORCED" for row in anti_shortcut)
    validations.append(
        validation_row(
            "VAL1325_5_shortcuts_enforced",
            "anti-shortcut gates are enforced",
            shortcut_ok,
            ";".join(row["gate_id"] for row in anti_shortcut),
        )
    )
    nonclaim_ok = all_nonclaim(
        [
            source_register,
            product_decomposition,
            input_matrix,
            runner,
            blocker,
            anti_shortcut,
            decision,
            next_target,
        ]
    )
    validations.append(
        validation_row(
            "VAL1325_6_nonclaim_policy",
            "all generated rows remain nonclaim",
            nonclaim_ok,
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    formal_outputs = generated_inside_formalization()
    validations.append(
        validation_row(
            "VAL1325_7_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not formal_outputs,
            f"formalization_generated_output_count={len(formal_outputs)}",
        )
    )
    next_ok = next_target[0]["target_file"].startswith("1326-Y5-R10-RAB-WEP-source-weight-owner")
    validations.append(
        validation_row(
            "VAL1325_8_next_target_1326",
            "next target routes to source-weight owner zero or finite Delta_w prior",
            next_ok,
            str(next_target[0]["target_file"]),
        )
    )
    validations.append(
        validation_row(
            "VAL1325_9_overall",
            "overall 1325 validation",
            all(row["status"] == "PASS" for row in validations),
            "1325 decomposes WEP source-normalization, refuses all branches, and selects source-weight owner/Delta_w next",
        )
    )
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# 1325: RAB WEP Source-Normalization Decomposition First Fill

**Current verdict:** 1325 decomposes the WEP/coupling route but does not score it. The branch is sharper now: alpha/Coulomb, source-weight, full-tensor, and direct-product paths are separate refusal rows.

**Main progress:** WEP is no longer one blob called "missing coupling." We now know which pieces are available as pressure/context rows and which pieces still block an actual prediction.

**Decision:** go after `Delta_w_TiPt`/source-weight ownership next. That is the cleanest coupling bottleneck: either prove it is zero from the parent matter/source grammar, or source a finite prior-width row without pretending.

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## WEP Product Decomposition
{markdown_table(product_decomposition, ["decomp_id", "branch", "product_law", "threshold", "threshold_units", "available_inputs", "missing_inputs", "current_status", "valid_for_claim", "claim_allowed"])}

## First-Fill Input Matrix
{markdown_table(input_matrix, ["input_id", "object", "current_value_or_status", "units", "source", "fill_status", "usable_role", "valid_for_claim", "claim_allowed"])}

## WEP Decomposition Runner
{markdown_table(runner, ["runner_id", "product_branch", "comparison_threshold", "threshold_units", "predicted_value", "available_inputs", "missing_inputs", "runner_status", "refusal_reason", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])}

## Blocker Ledger
{markdown_table(blocker, ["blocker_id", "blocks_runner", "missing_object", "current_status", "required_resolution", "valid_for_claim", "claim_allowed"])}

## Anti-Shortcut Gates
{markdown_table(anti_shortcut, ["gate_id", "shortcut", "enforcement", "status", "valid_for_claim", "claim_allowed"])}

## Decision Ledger
{markdown_table(decision, ["decision_id", "decision", "because", "effect", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validations, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
