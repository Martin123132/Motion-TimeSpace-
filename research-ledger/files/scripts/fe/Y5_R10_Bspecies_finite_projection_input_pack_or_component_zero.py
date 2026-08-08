from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1215"
TITLE = "1215-Y5-R10-Bspecies-finite-projection-input-pack-or-component-zero"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
COMPONENT_ZERO_PATH = OUT_DIR / f"{PACK_ID}_COMPONENT_ZERO_AUDIT.csv"
WEP_INTAKE_PATH = OUT_DIR / f"{PACK_ID}_WEP_NUMERIC_SUBCOMPONENT_INTAKE.csv"
SAME_NORM_PATH = OUT_DIR / f"{PACK_ID}_SAME_NORM_PRODUCT_CONTRACT.csv"
FEED_PATH = OUT_DIR / f"{PACK_ID}_BSPECIES_FEED_UPDATE.csv"
RUNNER_PATH = OUT_DIR / f"{PACK_ID}_PRODUCT_RUNNER_STUB.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1215_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


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


def as_false(row: dict[str, object], key: str) -> bool:
    value = row.get(key, False)
    if isinstance(value, bool):
        return not value
    return str(value).strip().lower() == "false"


def local_bound(row_id: str) -> dict[str, str]:
    for row in read_csv(LOCAL_BOUNDS):
        if row.get("row_id") == row_id:
            return row
    raise ValueError(f"missing local bound row {row_id}")


def find_row(rows: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    for row in rows:
        if row.get(key) == value:
            return row
    raise ValueError(f"missing row {key}={value}")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1215_0_1214_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1214_NEXT_TARGET.csv",
            "needle": "1215-Y5-R10-Bspecies-finite-projection-input-pack-or-component-zero.md",
            "purpose": "1214 handoff to B_species finite projection input pack",
        },
        {
            "source_id": "SRC1215_1_1214_bound",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1214_DELTA_SPECIES_BOUND_FILL.csv",
            "needle": "DSB1214_0_B_species_weight_total",
            "purpose": "B_species decomposition to refine",
        },
        {
            "source_id": "SRC1215_2_1214_arena",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1214_ARENA_PROJECTION_LEDGER.csv",
            "needle": "ARENA1214_0_WEP",
            "purpose": "WEP projection selected as best source-backed arena",
        },
        {
            "source_id": "SRC1215_3_1081_dd_delta",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1081_DD_MATERIAL_DELTA_IMPORT.csv",
            "needle": "DDM1081_0_delta_alpha",
            "purpose": "numeric DD material delta rows",
        },
        {
            "source_id": "SRC1215_4_1081_dd_unit",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1081_DD_UNIT_RESPONSE_SMOKE_RUNNER.csv",
            "needle": "DDS1081_2_equal_two_component_unit",
            "purpose": "numeric coefficient-normalized smoke sensitivity rows",
        },
        {
            "source_id": "SRC1215_5_1081_parent_gate",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1081_PARENT_TO_DD_GATE.csv",
            "needle": "PDD1081_1_coefficient_map",
            "purpose": "MTS-to-DD coefficient map still missing",
        },
        {
            "source_id": "SRC1215_6_1080_finite_pack",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1080_FINITE_WEP_INPUT_PACK_NONCLAIM.csv",
            "needle": "FIP1080_0_product_formula",
            "purpose": "finite WEP product formula and missing inputs",
        },
        {
            "source_id": "SRC1215_7_1080_Cparent",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1080_C_PARENT_COEFFICIENT_CONTRACT.csv",
            "needle": "CP1080_0_definition",
            "purpose": "C_parent coefficient contract",
        },
        {
            "source_id": "SRC1215_8_1080_readout",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1080_MICROSCOPE_READOUT_GATE.csv",
            "needle": "READ1080_3_physical_tau",
            "purpose": "MICROSCOPE readout/physical tau gate",
        },
        {
            "source_id": "SRC1215_9_1080_material",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1080_MATERIAL_COMPOSITION_AND_TENSOR_CANDIDATES.csv",
            "needle": "MAT1080_4_full_tensor_upgrade",
            "purpose": "material tensor candidate and full tensor missing row",
        },
        {
            "source_id": "SRC1215_10_1091_residuals",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1091_FINITE_RESIDUAL_ROUTE_MAP.csv",
            "needle": "FR1091_5_qbar_source_label",
            "purpose": "finite residual/source-label route",
        },
        {
            "source_id": "SRC1215_11_1091_operator",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1091_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv",
            "needle": "ODH1091_6_verdict",
            "purpose": "operator-domain theorem not derived",
        },
        {
            "source_id": "SRC1215_12_1088_conditional_zero",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1088_CONDITIONAL_ZERO_THEOREM.csv",
            "needle": "THM1088_6_current_corpus_verdict",
            "purpose": "conditional zero theorem not promoted",
        },
        {
            "source_id": "SRC1215_13_local_bounds",
            "local_path": "source-intake/local_bounds/local_bound_claims.csv",
            "needle": "R1_WEP_source_charge",
            "purpose": "MICROSCOPE WEP eta bound anchor",
        },
        {
            "source_id": "SRC1215_14_1053_charge_matrix",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1053_WEP_COMPOSITION_CHARGE_MATRIX.csv",
            "needle": "WCM1053_4",
            "purpose": "source rows behind DD alpha/surface deltas",
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

    dd_delta_rows = read_csv(OUT_DIR / "P8_Y5_R10_1081_DD_MATERIAL_DELTA_IMPORT.csv")
    dd_unit_rows = read_csv(OUT_DIR / "P8_Y5_R10_1081_DD_UNIT_RESPONSE_SMOKE_RUNNER.csv")
    eta_bound_row = local_bound("R1_WEP_source_charge")
    eta_bound = float(eta_bound_row["upper_bound"])

    alpha_delta = find_row(dd_delta_rows, "delta_id", "DDM1081_0_delta_alpha")
    surface_delta = find_row(dd_delta_rows, "delta_id", "DDM1081_1_delta_surface")
    alpha_unit = find_row(dd_unit_rows, "smoke_id", "DDS1081_0_alpha_unit")
    surface_unit = find_row(dd_unit_rows, "smoke_id", "DDS1081_1_surface_unit")
    equal_unit = find_row(dd_unit_rows, "smoke_id", "DDS1081_2_equal_two_component_unit")

    component_zero_rows = [
        {
            "zero_id": "CZ1215_0_no_source_only_slot",
            "target_component": "B_pre_action_weight",
            "zero_attempt": "use MOMS/action-measure owner to set all source-only species weights to zero",
            "result": "ZERO_NOT_PARENT_SIGNED",
            "evidence": "1214/1088/1090 keep MOMS/action-measure as closure-only or missing axiom",
            "fallback": "retain C_w*||Delta w_A|| envelope",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "zero_id": "CZ1215_1_source_label",
            "target_component": "B_source_label",
            "zero_attempt": "derive source-label forgetting / no-source-only-slot theorem",
            "result": "ZERO_NOT_PARENT_SIGNED",
            "evidence": "1091 keeps qbar_source_label as retained prior missing",
            "fallback": "require qbar_source_label prior or theorem-zero plus tau_source_projection",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "zero_id": "CZ1215_2_WEP_material_delta",
            "target_component": "WEP material response subcomponent",
            "zero_attempt": "test whether Ti/Pt DD alpha/surface material deltas vanish",
            "result": "ZERO_REJECTED_IN_DD_SMOKE_BASIS",
            "evidence": f"abs(alpha_delta)={alpha_delta['delta_abs']}; abs(surface_delta)={surface_delta['delta_abs']}",
            "fallback": "use numeric nonclaim material subcomponents; coefficient/source/readout still missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "zero_id": "CZ1215_3_constant_sector",
            "target_component": "B_constant_sector",
            "zero_attempt": "use operator-domain no-hidden-visible-hom theorem to kill alpha/mass/nuclear/clock coefficient leakage",
            "result": "ZERO_NOT_PARENT_SIGNED",
            "evidence": "1091 records scalar obstruction and retains finite residual coefficients",
            "fallback": "keep clock b_alpha product as source-backed clock-only bound; no WEP/R10 transfer",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "zero_id": "CZ1215_4_verdict",
            "target_component": "first B_species component",
            "zero_attempt": "either theorem-zero or source-backed finite row",
            "result": "NUMERIC_SUBCOMPONENT_AVAILABLE_NOT_CLAIM_COMPONENT",
            "evidence": "DD material deltas and unit-response rows are numeric; same-basis MTS product remains missing",
            "fallback": "advance via same-norm WEP C_parent/R_source/K_readout pack",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    wep_intake_rows = [
        {
            "intake_id": "WEP1215_0_material_delta_alpha",
            "feeds_component": "B_projection_map.WEP.R_material_alpha",
            "quantity": "DeltaQ_alpha_Coulomb(TA6V_minus_PtRh10)",
            "value": alpha_delta["delta_value"],
            "abs_value": alpha_delta["delta_abs"],
            "units": "DD_charge_convention_dimensionless",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1081_DD_MATERIAL_DELTA_IMPORT.csv",
            "source_row": "DDM1081_0_delta_alpha",
            "basis_status": "EXTERNAL_DD_SMOKE_NOT_MTS_PARENT_BASIS",
            "missing_for_claim": "MTS-to-DD coefficient map; Earth source vector; official/validated readout; full tensor",
            "current_status": "NUMERIC_SUBCOMPONENT_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "intake_id": "WEP1215_1_material_delta_surface",
            "feeds_component": "B_projection_map.WEP.R_material_surface",
            "quantity": "DeltaQ_surface_binding(TA6V_minus_PtRh10)",
            "value": surface_delta["delta_value"],
            "abs_value": surface_delta["delta_abs"],
            "units": "DD_charge_convention_dimensionless",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1081_DD_MATERIAL_DELTA_IMPORT.csv",
            "source_row": "DDM1081_1_delta_surface",
            "basis_status": "EXTERNAL_DD_SMOKE_NOT_MTS_PARENT_BASIS",
            "missing_for_claim": "MTS-to-DD coefficient map; Earth source vector; official/validated readout; full tensor",
            "current_status": "NUMERIC_SUBCOMPONENT_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "intake_id": "WEP1215_2_alpha_unit_response",
            "feeds_component": "coefficient_normalized_sensitivity.alpha",
            "quantity": "|c_alpha_proxy|max if unit source/readout proxies are imposed",
            "value": alpha_unit["required_abs_coefficient_max"],
            "abs_value": alpha_unit["required_abs_coefficient_max"],
            "units": "dimensionless_proxy_coefficient",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1081_DD_UNIT_RESPONSE_SMOKE_RUNNER.csv",
            "source_row": "DDS1081_0_alpha_unit",
            "basis_status": "UNIT_PROXY_NONPHYSICAL",
            "missing_for_claim": "physical source/readout normalization and MTS-to-DD map",
            "current_status": "NUMERIC_SMOKE_BOUND_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "intake_id": "WEP1215_3_surface_unit_response",
            "feeds_component": "coefficient_normalized_sensitivity.surface",
            "quantity": "|c_surface_proxy|max if unit source/readout proxies are imposed",
            "value": surface_unit["required_abs_coefficient_max"],
            "abs_value": surface_unit["required_abs_coefficient_max"],
            "units": "dimensionless_proxy_coefficient",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1081_DD_UNIT_RESPONSE_SMOKE_RUNNER.csv",
            "source_row": "DDS1081_1_surface_unit",
            "basis_status": "UNIT_PROXY_NONPHYSICAL",
            "missing_for_claim": "physical source/readout normalization and MTS-to-DD map",
            "current_status": "NUMERIC_SMOKE_BOUND_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "intake_id": "WEP1215_4_equal_two_component_unit_response",
            "feeds_component": "coefficient_normalized_sensitivity.alpha_plus_surface",
            "quantity": "|c_equal_proxy|max if unit source/readout proxies are imposed",
            "value": equal_unit["required_abs_coefficient_max"],
            "abs_value": equal_unit["required_abs_coefficient_max"],
            "units": "dimensionless_proxy_coefficient",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1081_DD_UNIT_RESPONSE_SMOKE_RUNNER.csv",
            "source_row": "DDS1081_2_equal_two_component_unit",
            "basis_status": "UNIT_PROXY_NONPHYSICAL",
            "missing_for_claim": "physical source/readout normalization and MTS-to-DD map",
            "current_status": "NUMERIC_SMOKE_BOUND_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "intake_id": "WEP1215_5_MICROSCOPE_eta_bound",
            "feeds_component": "WEP_product_bound_anchor",
            "quantity": "|eta_TA6V_PtRh10| upper bound",
            "value": eta_bound_row["upper_bound"],
            "abs_value": eta_bound_row["upper_bound"],
            "units": eta_bound_row["units"],
            "source_path": "source-intake/local_bounds/local_bound_claims.csv",
            "source_row": "R1_WEP_source_charge",
            "basis_status": "SOURCE_BACKED_BOUND_ANCHOR_NOT_MTS_PREDICTION",
            "missing_for_claim": "MTS prediction product; same-basis finite inputs",
            "current_status": "NUMERIC_BOUND_ANCHOR_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "intake_id": "WEP1215_6_C_parent",
            "feeds_component": "B_projection_map.WEP.C_parent",
            "quantity": "C_parent finite WEP coupling coefficient vector",
            "value": "MISSING_C_PARENT",
            "abs_value": "MISSING",
            "units": "basis_dependent",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1080_C_PARENT_COEFFICIENT_CONTRACT.csv",
            "source_row": "CP1080_0_definition",
            "basis_status": "MISSING_MTS_PARENT_BASIS",
            "missing_for_claim": "derive from parent action or source explicit finite coefficient with provenance",
            "current_status": "MISSING_FOR_CLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "intake_id": "WEP1215_7_R_source_Earth",
            "feeds_component": "B_projection_map.WEP.R_source",
            "quantity": "R_source^Earth in same basis",
            "value": "MISSING_EARTH_SOURCE_VECTOR",
            "abs_value": "MISSING",
            "units": "basis_dependent",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1080_FINITE_WEP_INPUT_PACK_NONCLAIM.csv",
            "source_row": "FIP1080_2_R_source",
            "basis_status": "REFERENCE_IDENTIFIED_NOT_VECTORIZED",
            "missing_for_claim": "Earth/source vector in same parent/DD convention",
            "current_status": "MISSING_FOR_CLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "intake_id": "WEP1215_8_K_MICROSCOPE",
            "feeds_component": "B_projection_map.WEP.K_readout",
            "quantity": "official or validated MICROSCOPE readout kernel",
            "value": "MISSING_OFFICIAL_OR_VALIDATED_READOUT",
            "abs_value": "MISSING",
            "units": "eta_projection_convention",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1080_MICROSCOPE_READOUT_GATE.csv",
            "source_row": "READ1080_1_CMSM_portal",
            "basis_status": "PORTAL_IDENTIFIED_ARRAYS_NOT_IMPORTED",
            "missing_for_claim": "official arrays/masks or validated reconstruction",
            "current_status": "MISSING_FOR_CLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    same_norm_rows = [
        {
            "contract_id": "SNP1215_0_WEP_formula",
            "object": "same-norm WEP B_species product",
            "requirement": "B_species,WEP <= |K_MICROSCOPE| * sum_I |C_parent^I| |R_source_I^Earth| |DeltaR_TA6V-PtRh10_I|",
            "current_evidence": "DD material deltas numeric; eta bound numeric; C_parent, R_source, K_MICROSCOPE missing",
            "status": "FORMULA_READY_NUMERIC_SUBCOMPONENTS_PRODUCT_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "SNP1215_1_basis_lock",
            "object": "basis/norm lock",
            "requirement": "C_parent, R_source, R_material, and K_readout must share the same basis, branch id, range convention, and units",
            "current_evidence": "DD smoke basis is external; MTS-to-DD map missing in PDD1081_1",
            "status": "MISSING_SAME_BASIS_OWNER",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "SNP1215_2_no_unit_proxy",
            "object": "source/readout normalization",
            "requirement": "unit source/readout proxies may debug algebra but cannot be tau_WEP, measured G, or physical readout",
            "current_evidence": "DDS1081 rows are numeric only under nonphysical unit proxies",
            "status": "UNIT_PROXY_BLOCKS_CLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "SNP1215_3_no_cancellation",
            "object": "absolute-sum rule",
            "requirement": "component signs cannot be tuned against each other; use absolute products unless a full sourced covariance model exists",
            "current_evidence": "1213/1214 no-cancellation policy",
            "status": "NO_CANCELLATION_GUARD_ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "SNP1215_4_claim_verdict",
            "object": "first B_species component",
            "requirement": "claim-valid row needs numeric same-basis product or theorem-zero certificate",
            "current_evidence": "numeric subcomponents exist, but product factors and parent basis are missing",
            "status": "NOT_CLAIM_VALID",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    feed_rows = [
        {
            "feed_id": "BFEED1215_0_to_DSB1214_5_projection_map",
            "target_row": "DSB1214_5_projection_map",
            "field_to_fill": "WEP_material_subcomponent",
            "source_row": "WEP1215_0_material_delta_alpha;WEP1215_1_material_delta_surface",
            "update_value": "numeric DD material subcomponents available; same-basis product still missing",
            "claim_policy": "nonclaim subcomponent feed only; does not make B_projection_map or B_species_weight numeric",
            "current_status": "PARTIAL_NUMERIC_SUBCOMPONENT_PRODUCT_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "feed_id": "BFEED1215_1_to_DSB1214_0_total",
            "target_row": "DSB1214_0_B_species_weight_total",
            "field_to_fill": "B_projection_map",
            "source_row": "SNP1215_0_WEP_formula",
            "update_value": "formula plus numeric DD subcomponents, but missing C_parent/R_source/K_readout",
            "claim_policy": "keeps total B_species_weight blocked until all same-norm product factors exist",
            "current_status": "SOURCE_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner_rows = [
        {
            "runner_id": "APR1215_0_Bspecies_WEP_subcomponent_stub",
            "prediction_rows": 1,
            "valid_prediction_rows": 0,
            "numeric_subcomponent_rows": 5,
            "valid_bound_rows": 1,
            "claim_allowed": False,
            "expected_result": "accept numeric nonclaim subcomponents but reject missing same-basis product",
            "reason": "C_parent, R_source^Earth, K_MICROSCOPE, and MTS-to-DD map are missing",
            "valid_for_claim": False,
        }
    ]

    decisions = [
        {
            "decision_id": "DEC1215_0_component_zero",
            "decision": "do not claim a component zero",
            "because": "no-source-only-slot/MOMS/operator-domain routes remain unsigned and DD material deltas are nonzero in the smoke basis",
            "next_action": "route through finite same-basis WEP product inputs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1215_1_numeric_progress",
            "decision": "retain DD material deltas and coefficient-normalized rows as useful numeric nonclaim scaffolding",
            "because": "they test algebra, signs, and rough coefficient pressure without pretending to be MTS-derived",
            "next_action": "derive or source C_parent, R_source^Earth, and K_MICROSCOPE in one basis",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1215_2_next_route",
            "decision": "target the same-norm WEP product lock next",
            "because": "it is the shortest path from numeric subcomponents to a real bounded local test row",
            "next_action": "1216 should try C_parent/source/readout acquisition or a narrow zero theorem for one missing factor",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1215_0_component_zero",
            "gate": "one B_species component theorem-zero",
            "status": "BLOCKED",
            "reason": "MOMS/no-hidden/operator-domain/action-measure zero routes remain unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1215_1_numeric_material",
            "gate": "WEP material subcomponent numeric",
            "status": "PASS_NONCLAIM",
            "reason": "DD alpha/surface material deltas are numeric but external and not same-norm MTS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1215_2_same_basis_product",
            "gate": "same-basis WEP product complete",
            "status": "BLOCKED",
            "reason": "C_parent, Earth source vector, K_MICROSCOPE, and MTS-to-DD map are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1215_3_Bspecies_bound",
            "gate": "B_species_weight numeric/source-backed",
            "status": "BLOCKED",
            "reason": "1215 adds numeric subcomponents only, not full B_species component value",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1215_4_local_GR_R10_WEP",
            "gate": "local-GR/R10/WEP pass",
            "status": "BLOCKED",
            "reason": "no valid prediction rows and no theorem-zero certificate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_rows = [
        {
            "next_id": "NEXT1215_0_1216",
            "target_file": "1216-Y5-R10-WEP-same-norm-Cparent-source-readout-or-component-zero.md",
            "target_script": "scripts/Y5_R10_WEP_same_norm_Cparent_source_readout_or_component_zero.py",
            "task": "try to derive or source one same-norm missing WEP factor: C_parent coefficient map, R_source^Earth, K_MICROSCOPE/readout, or a theorem-zero certificate for that factor",
            "success_condition": "one missing same-basis factor becomes source-backed/numeric or theorem-zero while DD smoke rows remain nonclaim unless the full product is completed",
            "do_not_do": "do not use unit proxies as tau_WEP; do not absorb relative weights into measured G; do not tune cancellations; do not claim local GR/WEP/R10; do not edit formalization-workbench or push GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    source_fields = ["source_id", "local_path", "needle", "purpose", "absolute_path", "path_exists", "needle_found", "valid_for_claim", "claim_allowed"]
    zero_fields = ["zero_id", "target_component", "zero_attempt", "result", "evidence", "fallback", "valid_for_claim", "claim_allowed"]
    intake_fields = ["intake_id", "feeds_component", "quantity", "value", "abs_value", "units", "source_path", "source_row", "basis_status", "missing_for_claim", "current_status", "valid_for_claim", "claim_allowed"]
    contract_fields = ["contract_id", "object", "requirement", "current_evidence", "status", "valid_for_claim", "claim_allowed"]
    feed_fields = ["feed_id", "target_row", "field_to_fill", "source_row", "update_value", "claim_policy", "current_status", "valid_for_claim", "claim_allowed"]
    runner_fields = ["runner_id", "prediction_rows", "valid_prediction_rows", "numeric_subcomponent_rows", "valid_bound_rows", "claim_allowed", "expected_result", "reason", "valid_for_claim"]
    decision_fields = ["decision_id", "decision", "because", "next_action", "valid_for_claim", "claim_allowed"]
    gate_fields = ["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"]
    next_fields = ["next_id", "target_file", "target_script", "task", "success_condition", "do_not_do", "valid_for_claim", "claim_allowed"]

    write_csv(SOURCE_REGISTER_PATH, source_rows, source_fields)
    write_csv(COMPONENT_ZERO_PATH, component_zero_rows, zero_fields)
    write_csv(WEP_INTAKE_PATH, wep_intake_rows, intake_fields)
    write_csv(SAME_NORM_PATH, same_norm_rows, contract_fields)
    write_csv(FEED_PATH, feed_rows, feed_fields)
    write_csv(RUNNER_PATH, runner_rows, runner_fields)
    write_csv(DECISION_PATH, decisions, decision_fields)
    write_csv(CLAIM_GATES_PATH, claim_gates, gate_fields)
    write_csv(NEXT_PATH, next_rows, next_fields)

    csvs_to_parse = [
        SOURCE_REGISTER_PATH,
        COMPONENT_ZERO_PATH,
        WEP_INTAKE_PATH,
        SAME_NORM_PATH,
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
        except Exception as exc:  # noqa: BLE001
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
    numeric_material_rows = [
        row for row in wep_intake_rows
        if row["intake_id"] in {"WEP1215_0_material_delta_alpha", "WEP1215_1_material_delta_surface"}
    ]
    numeric_material_positive = all(float(row["abs_value"]) > 0 for row in numeric_material_rows)
    numeric_smoke_bounds = [
        row for row in wep_intake_rows
        if row["intake_id"] in {"WEP1215_2_alpha_unit_response", "WEP1215_3_surface_unit_response", "WEP1215_4_equal_two_component_unit_response"}
    ]
    numeric_smoke_positive = all(float(row["abs_value"]) > 0 for row in numeric_smoke_bounds)
    eta_bound_positive = eta_bound > 0
    zero_not_claimed = any(row["zero_id"] == "CZ1215_4_verdict" and row["result"] == "NUMERIC_SUBCOMPONENT_AVAILABLE_NOT_CLAIM_COMPONENT" for row in component_zero_rows)
    same_norm_blocked = any(row["contract_id"] == "SNP1215_4_claim_verdict" and row["status"] == "NOT_CLAIM_VALID" for row in same_norm_rows)
    runner_refuses = runner_rows[0]["valid_prediction_rows"] == 0 and not runner_rows[0]["claim_allowed"]
    feed_present = any(row["feed_id"] == "BFEED1215_0_to_DSB1214_5_projection_map" for row in feed_rows)
    no_missing_claim_rows = all(
        not (not as_false(row, "valid_for_claim") and "MISSING" in " ".join(str(value) for value in row.values()))
        for row in wep_intake_rows + feed_rows
    )
    no_claim = all(
        as_false(row, "valid_for_claim") and as_false(row, "claim_allowed")
        for row in component_zero_rows + wep_intake_rows + same_norm_rows + feed_rows + runner_rows + decisions + claim_gates + next_rows
    )
    formalization_untouched = len(formalization_recent) == 0
    next_1216 = next_rows[0]["target_file"].startswith("1216-")

    validation_rows = [
        validation_row("VAL1215_0_sources_exist", "all cited local sources exist", all_sources_exist, f"{sum(bool(row['path_exists']) for row in source_rows)}/{len(source_rows)} sources exist"),
        validation_row("VAL1215_1_needles_found", "all cited source needles found", all_needles_found, f"{sum(bool(row['needle_found']) for row in source_rows)}/{len(source_rows)} needles found"),
        validation_row("VAL1215_2_numeric_material_subcomponents", "DD material subcomponents are numeric positive magnitudes", numeric_material_positive, "; ".join(f"{row['intake_id']}={row['abs_value']}" for row in numeric_material_rows)),
        validation_row("VAL1215_3_numeric_smoke_bounds", "unit-response smoke coefficient bounds are numeric positive", numeric_smoke_positive, "; ".join(f"{row['intake_id']}={row['abs_value']}" for row in numeric_smoke_bounds)),
        validation_row("VAL1215_4_eta_bound_positive", "MICROSCOPE eta bound anchor positive", eta_bound_positive, f"R1_WEP_source_charge={eta_bound}"),
        validation_row("VAL1215_5_zero_not_claimed", "component zero is not overclaimed", zero_not_claimed, "CZ1215_4 keeps numeric subcomponent nonclaim"),
        validation_row("VAL1215_6_same_norm_blocked", "same-norm product remains blocked", same_norm_blocked, "SNP1215_4 status NOT_CLAIM_VALID"),
        validation_row("VAL1215_7_runner_refuses", "runner stub refuses missing product", runner_refuses, "valid_prediction_rows=0 and claim_allowed=false"),
        validation_row("VAL1215_8_feed_present", "Bspecies feed update exists", feed_present, "BFEED1215_0_to_DSB1214_5_projection_map present"),
        validation_row("VAL1215_9_no_missing_claim_rows", "no row with MISSING is valid for claim", no_missing_claim_rows, "missing factor rows remain nonclaim"),
        validation_row("VAL1215_10_nonclaim_policy", "all generated rows remain nonclaim", no_claim, "valid_for_claim=false and claim_allowed=false throughout"),
        validation_row("VAL1215_11_csv_parse", "all generated CSVs parse cleanly", csv_parse_ok, "; ".join(parse_details)),
        validation_row("VAL1215_12_formalization_untouched", "formalization-workbench untouched during run", formalization_untouched, f"formalization_recent_after_run_start_count={len(formalization_recent)}"),
        validation_row("VAL1215_13_next_target", "next target is staged", next_1216, next_rows[0]["target_file"]),
    ]
    validation_pass = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        validation_row(
            "VAL1215_14_overall",
            "overall 1215 validation",
            validation_pass,
            "1215 Bspecies finite projection input pack is reproducible, numeric-subcomponent-backed, and nonclaim" if validation_pass else "one or more validation checks failed",
        )
    )
    validation_fields = ["check_id", "check", "status", "details", "valid_for_claim", "claim_allowed"]
    write_csv(VALIDATION_PATH, validation_rows, validation_fields)

    doc = f"""# 1215 Y5/R10 Bspecies Finite Projection Input Pack Or Component Zero

**Current verdict:** 1215 does **not** prove any `B_species_weight` component is zero. It does make the first useful finite WEP/material subcomponent numeric: the DD alpha/surface Ti/Pt deltas and coefficient-normalized smoke rows are now explicitly imported into the `B_species` chain.

**Main progress:** `B_projection_map.WEP` now has numeric nonclaim material subcomponents, but the same-norm product is still missing `C_parent`, `R_source^Earth`, `K_MICROSCOPE`, and the MTS-to-DD map.

**Why this matters:** the coupling problem is no longer just “missing coupling.” We now know which part is numerically available and which lock prevents promotion to evidence.

## Source Register

{markdown_table(source_rows, source_fields)}

## Component Zero Audit

{markdown_table(component_zero_rows, zero_fields)}

## WEP Numeric Subcomponent Intake

{markdown_table(wep_intake_rows, intake_fields)}

## Same-Norm Product Contract

{markdown_table(same_norm_rows, contract_fields)}

## Bspecies Feed Update

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
    print("B_species_component_zero_claimed=false")
    print("numeric_subcomponent_rows=5")


if __name__ == "__main__":
    main()
