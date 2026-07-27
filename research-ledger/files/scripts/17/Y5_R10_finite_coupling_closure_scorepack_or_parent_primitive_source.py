from __future__ import annotations

import csv
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path


PACK_ID = "P8_Y5_R10_1221"
TITLE = "1221-Y5-R10-finite-coupling-closure-scorepack-or-parent-primitive-source"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
INPUT_SCHEMA_PATH = OUT_DIR / f"{PACK_ID}_FINITE_CLOSURE_INPUT_SCHEMA.csv"
ACQUISITION_LEDGER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_ACQUISITION_LEDGER.csv"
RUNNER_ROWS_PATH = OUT_DIR / f"{PACK_ID}_RUNNER_READY_NONCLAIM_ROWS.csv"
PARENT_PRIMITIVE_PATH = OUT_DIR / f"{PACK_ID}_PARENT_PRIMITIVE_ESCAPE_HATCH.csv"
ARENA_MAP_PATH = OUT_DIR / f"{PACK_ID}_EMPIRICAL_ARENA_MAP.csv"
SCOREPACK_DECISION_PATH = OUT_DIR / f"{PACK_ID}_SCOREPACK_DECISION_MATRIX.csv"
FEED_PATH = OUT_DIR / f"{PACK_ID}_FEED_UPDATE.csv"
RUNNER_STUB_PATH = OUT_DIR / f"{PACK_ID}_PRODUCT_RUNNER_STUB.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1221_VALIDATION.csv"


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


def is_true(row: dict[str, object], key: str) -> bool:
    value = row.get(key, False)
    if isinstance(value, bool):
        return value is True
    return str(value).strip().lower() == "true"


def positive_decimal(value: object) -> bool:
    try:
        return Decimal(str(value)) > 0
    except (InvalidOperation, ValueError):
        return False


def has_missing(row: dict[str, object]) -> bool:
    return "MISSING" in " ".join(str(value) for value in row.values()).upper()


def find_row(rows: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    for row in rows:
        if row.get(key) == value:
            return row
    raise ValueError(f"missing row {key}={value}")


def local_source_ref(relative_path: str, needle: str) -> str:
    return f"{relative_path}:{needle}"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1221_0_1220_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1220_NEXT_TARGET.csv",
            "needle": "1221-Y5-R10-finite-coupling-closure-scorepack-or-parent-primitive-source.md",
            "purpose": "1220 handoff to finite closure scorepack / parent primitive source target",
        },
        {
            "source_id": "SRC1221_1_1220_closure_register",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1220_FINITE_COUPLING_CLOSURE_REGISTER.csv",
            "needle": "FCCR1220_0_alpha",
            "purpose": "explicit finite coupling closure debts",
        },
        {
            "source_id": "SRC1221_2_1220_counterexamples",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1220_COUNTEREXAMPLE_LOCK_UPDATE.csv",
            "needle": "CELOCK1220_0_hidden_scalar",
            "purpose": "counterexample locks retained on finite rows",
        },
        {
            "source_id": "SRC1221_3_1220_demotion",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1220_NO_HIDDEN_VISIBLE_ROUTE_DEMOTION.csv",
            "needle": "DEM1220_0_route_status",
            "purpose": "no-hidden-visible route demoted to closure debt",
        },
        {
            "source_id": "SRC1221_4_1220_gates",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1220_CLAIM_GATES.csv",
            "needle": "GATE1220_4_finite_closure",
            "purpose": "finite closure gate remains blocked",
        },
        {
            "source_id": "SRC1221_5_1219_debt_rows",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1219_FINITE_COUPLING_CLOSURE_DEBT_ROWS.csv",
            "needle": "FC1219_0_alpha",
            "purpose": "pre-1220 finite coupling debt rows",
        },
        {
            "source_id": "SRC1221_6_1218_thresholds",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1218_THRESHOLD_CARRY_FORWARD_NONCLAIM.csv",
            "needle": "TCF1218_0_alpha",
            "purpose": "nonclaim threshold carry-forward rows",
        },
        {
            "source_id": "SRC1221_7_1216_pressure",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1216_DD_SOURCE_MATERIAL_PRODUCT_PRESSURE.csv",
            "needle": "DDP1216_2_combined_abs",
            "purpose": "combined alpha/surface product pressure that set the tight common scale",
        },
        {
            "source_id": "SRC1221_8_1098_requirements",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1098_SOURCE_BACKED_COEFFICIENT_REQUIREMENTS.csv",
            "needle": "REQ1098_0_c_alpha",
            "purpose": "source-backed coefficient requirements and thresholds",
        },
        {
            "source_id": "SRC1221_9_1052_wep_alpha",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv",
            "needle": "AWP1052_0_alpha_Coulomb",
            "purpose": "alpha/surface WEP projection pressure rows",
        },
        {
            "source_id": "SRC1221_10_1052_clock",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv",
            "needle": "ACB1052_2",
            "purpose": "clock product bound is product-only unless tau_clock is derived",
        },
        {
            "source_id": "SRC1221_11_1066_tau_wep",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1066_TAU_WEP_PROJECTION_CONTRACT.csv",
            "needle": "TWP1066_7_verdict",
            "purpose": "tau_WEP projection contract not derived",
        },
        {
            "source_id": "SRC1221_12_1066_prior_width",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1066_WEP_DELTA_W_PRIOR_WIDTH_SCHEMA.csv",
            "needle": "DWP1066_3_finite_prior_width",
            "purpose": "relative source-weight finite prior width schema",
        },
        {
            "source_id": "SRC1221_13_1083_source_vector",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv",
            "needle": "SCG1083_0_profile_weighting",
            "purpose": "source-profile/worldtube weighting caveat",
        },
        {
            "source_id": "SRC1221_14_1084_readout",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv",
            "needle": "RIG1084_0_CMSM_arrays",
            "purpose": "official MICROSCOPE readout arrays not imported",
        },
        {
            "source_id": "SRC1221_15_local_bound",
            "local_path": "source-intake/local_bounds/local_bound_claims.csv",
            "needle": "R1_WEP_source_charge",
            "purpose": "local WEP source-charge proxy bound anchor",
        },
    ]

    source_register = []
    for spec in source_specs:
        path_exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_register.append(
            {
                **spec,
                "absolute_path": str(source_path(spec["local_path"])),
                "path_exists": path_exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    closure_rows = read_csv(OUT_DIR / "P8_Y5_R10_1220_FINITE_COUPLING_CLOSURE_REGISTER.csv")
    closure_by_id = {row["closure_id"]: row for row in closure_rows}
    source_weight_aux = {
        "closure_id": "FCCR1220_aux_source_weight",
        "from_debt_row": "DWP1066_3_finite_prior_width;TWP1066_7_verdict;CELOCK1220_2_source_weight",
        "coefficient_or_debt": "Delta_w_TiPt * tau_WEP source-weight product",
        "retained_counterexample": "HSC1219_4_source_weight;CELOCK1220_2_source_weight",
        "threshold_or_source": "2.8e-15",
        "closure_status": "FINITE_CLOSURE_DEBT_EXPLICIT_AUXILIARY",
        "required_to_promote": "source worldtube/profile weighting, tau_WEP readout kernel, and parent action-scale/current owner",
        "valid_for_claim": "False",
        "claim_allowed": "False",
    }
    all_closure_rows = [*closure_rows, source_weight_aux]

    input_schema = [
        {
            "schema_id": "SCHEMA1221_0_coefficient_value",
            "input_name": "coefficient_value",
            "required_for": "alpha;surface;common_norm;tail;readout;source_weight",
            "minimum_usable_form": "finite numeric value with sign/absolute convention and units",
            "refusal_if_missing": "row remains score_ready=false and valid_for_claim=false",
            "current_status": "MISSING_FOR_ALL_PHYSICAL_CLOSURE_ROWS",
            "source_basis": local_source_ref("source-intake/mts_residuals/P8_Y5_R10_1220_FINITE_COUPLING_CLOSURE_REGISTER.csv", "FCCR1220_0_alpha"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "schema_id": "SCHEMA1221_1_parent_primitive_or_source_prior",
            "input_name": "primitive_or_prior_source",
            "required_for": "every finite closure promotion",
            "minimum_usable_form": "signed parent primitive theorem, or a sourced finite coefficient/prior with provenance",
            "refusal_if_missing": "absence/minimality cannot be used as proof",
            "current_status": "MISSING_PARENT_PRIMITIVE_AND_MISSING_SOURCE_PRIOR",
            "source_basis": local_source_ref("source-intake/mts_residuals/P8_Y5_R10_1220_NO_HIDDEN_VISIBLE_ROUTE_DEMOTION.csv", "DEM1220_0_route_status"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "schema_id": "SCHEMA1221_2_threshold_bound",
            "input_name": "threshold_or_empirical_bound",
            "required_for": "runner comparison",
            "minimum_usable_form": "positive numeric bound or explicit sourced nonnumeric blocker",
            "refusal_if_missing": "no pass/fail scoring",
            "current_status": "NUMERIC_FOR_ALPHA_SURFACE_COMMON_SOURCE_WEIGHT;MISSING_FOR_TAIL_READOUT",
            "source_basis": local_source_ref("source-intake/mts_residuals/P8_Y5_R10_1098_SOURCE_BACKED_COEFFICIENT_REQUIREMENTS.csv", "REQ1098_0_c_alpha"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "schema_id": "SCHEMA1221_3_source_profile",
            "input_name": "source_profile_or_worldtube",
            "required_for": "WEP;local_GR;PPN;R10 finite-source comparisons",
            "minimum_usable_form": "profile-weighted source vector in the same convention as the observable readout",
            "refusal_if_missing": "no measured-G absorption and no unity shortcut",
            "current_status": "MISSING_SOURCE_PROFILE_WEIGHTING",
            "source_basis": local_source_ref("source-intake/mts_residuals/P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv", "SCG1083_0_profile_weighting"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "schema_id": "SCHEMA1221_4_readout_kernel",
            "input_name": "readout_kernel",
            "required_for": "MICROSCOPE_WEP;clock;R10 transfer;observable alpha_eff",
            "minimum_usable_form": "official/sourced kernel mapping parent residual to the reported observable",
            "refusal_if_missing": "surrogate kernels remain nonclaim smoke data only",
            "current_status": "OFFICIAL_ARRAYS_OR_READOUT_FUNCTOR_MISSING",
            "source_basis": local_source_ref("source-intake/mts_residuals/P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv", "RIG1084_0_CMSM_arrays"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "schema_id": "SCHEMA1221_5_counterexample_disposition",
            "input_name": "counterexample_status",
            "required_for": "claim promotion",
            "minimum_usable_form": "counterexample closed by theorem/source, or retained as finite nuisance with bound",
            "refusal_if_missing": "counterexample lock blocks claim even when a threshold exists",
            "current_status": "COUNTEREXAMPLES_ACTIVE",
            "source_basis": local_source_ref("source-intake/mts_residuals/P8_Y5_R10_1220_COUNTEREXAMPLE_LOCK_UPDATE.csv", "CELOCK1220_0_hidden_scalar"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    acquisition_rows = [
        {
            "acquisition_id": "ACQ1221_0_alpha",
            "closure_id": "FCCR1220_0_alpha",
            "debt": "source-backed alpha coefficient c_alpha_DD/b_alpha or no-extra-F2 parent primitive",
            "arena": "WEP;clock;R10;EM",
            "source_to_acquire": "signed coefficient value/prior or parent theorem forbidding f(I_hid)F_Q^2",
            "minimum_usable_form": "numeric abs(c_alpha_DD/b_alpha) <= 8.320244933243531978e-10 with provenance, or theorem-zero",
            "current_best_local_source": local_source_ref("source-intake/mts_residuals/P8_Y5_R10_1098_SOURCE_BACKED_COEFFICIENT_REQUIREMENTS.csv", "REQ1098_0_c_alpha"),
            "missing_or_status": "MISSING_SOURCE_BACKED_COEFFICIENT_OR_PARENT_PRIMITIVE",
            "blocker_class": "hidden_scalar_alpha_F2",
            "scorepack_priority": "P0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "acquisition_id": "ACQ1221_1_surface",
            "closure_id": "FCCR1220_1_surface",
            "debt": "source-backed surface/binding coefficient c_surface_DD or no-binding-vertex parent primitive",
            "arena": "WEP;clock;nuclear",
            "source_to_acquire": "signed coefficient value/prior or parent matter-functor theorem fixing binding/surface response",
            "minimum_usable_form": "numeric abs(c_surface_DD) <= 6.987501646143863402e-11 with provenance, or theorem-zero",
            "current_best_local_source": local_source_ref("source-intake/mts_residuals/P8_Y5_R10_1098_SOURCE_BACKED_COEFFICIENT_REQUIREMENTS.csv", "REQ1098_1_c_surface"),
            "missing_or_status": "MISSING_SOURCE_BACKED_COEFFICIENT_OR_PARENT_PRIMITIVE",
            "blocker_class": "surface_binding_counterexample",
            "scorepack_priority": "P0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "acquisition_id": "ACQ1221_2_source_weight",
            "closure_id": "FCCR1220_aux_source_weight",
            "debt": "relative source-weight product Delta_w_TiPt * tau_WEP",
            "arena": "MICROSCOPE_WEP;local_GR_source;PPN",
            "source_to_acquire": "Earth/source worldtube, source profile weighting, tau_WEP readout kernel, and parent action-scale/current owner",
            "minimum_usable_form": "abs(Delta_w_TiPt * tau_WEP) <= 2.8e-15, no cancellation shortcut",
            "current_best_local_source": local_source_ref("source-intake/mts_residuals/P8_Y5_R10_1066_WEP_DELTA_W_PRIOR_WIDTH_SCHEMA.csv", "DWP1066_3_finite_prior_width"),
            "missing_or_status": "MISSING_NUMERIC_PRIOR_WIDTH_AND_MISSING_LAB_SOURCE_ORBIT_PROJECTION",
            "blocker_class": "source_weight_current_owner",
            "scorepack_priority": "P0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "acquisition_id": "ACQ1221_3_readout",
            "closure_id": "FCCR1220_4_readout",
            "debt": "effective/readout coefficient drift",
            "arena": "MICROSCOPE_WEP;clocks;spectroscopy",
            "source_to_acquire": "renormalized/readout functor closure or official readout arrays and residual prior",
            "minimum_usable_form": "readout kernel with units/convention and bounded coefficient drift; no surrogate-as-claim",
            "current_best_local_source": local_source_ref("source-intake/mts_residuals/P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv", "RIG1084_0_CMSM_arrays"),
            "missing_or_status": "MISSING_RADIOUT_CLOSURE_AND_OFFICIAL_ARRAYS",
            "blocker_class": "readout_regeneration",
            "scorepack_priority": "P0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "acquisition_id": "ACQ1221_4_common_norm",
            "closure_id": "FCCR1220_2_common_norm",
            "debt": "C_parent vector norm across alpha/surface/source channels",
            "arena": "WEP material vector;local source branch",
            "source_to_acquire": "same-branch finite vector norm and channel weights before choosing a material/readout projection",
            "minimum_usable_form": "norm(C_parent) <= 6.446142229433907306e-11 in a sourced coefficient basis",
            "current_best_local_source": local_source_ref("source-intake/mts_residuals/P8_Y5_R10_1216_DD_SOURCE_MATERIAL_PRODUCT_PRESSURE.csv", "DDP1216_2_combined_abs"),
            "missing_or_status": "MISSING_PARENT_OPERATOR_BASIS_MAP",
            "blocker_class": "generic_hidden_scalar",
            "scorepack_priority": "P1",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "acquisition_id": "ACQ1221_5_tail",
            "closure_id": "FCCR1220_3_tail",
            "debt": "q_tail(A) unmodelled material/source tail",
            "arena": "WEP material diversity;R10 finite-source;local_GR source",
            "source_to_acquire": "basis completeness theorem or empirical all-material tail envelope",
            "minimum_usable_form": "positive numeric tail envelope in the same source/readout convention as the scored arena",
            "current_best_local_source": local_source_ref("source-intake/mts_residuals/P8_Y5_R10_1220_FINITE_COUPLING_CLOSURE_REGISTER.csv", "FCCR1220_3_tail"),
            "missing_or_status": "MISSING_TAIL_ENVELOPE",
            "blocker_class": "material_basis_tail",
            "scorepack_priority": "P1",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner_rows = [
        {
            "runner_row_id": "RUN1221_0_alpha",
            "closure_id": "FCCR1220_0_alpha",
            "observable_product": "abs(c_alpha_DD/b_alpha)",
            "threshold_abs": closure_by_id["FCCR1220_0_alpha"]["threshold_or_source"],
            "threshold_units": "dimensionless",
            "required_numeric_inputs": "c_alpha_DD,b_alpha or theorem_zero flag",
            "available_numeric_inputs": "threshold_abs_only",
            "missing_inputs": "MISSING_SOURCE_BACKED_ALPHA_COEFFICIENT;MISSING_PARENT_PRIMITIVE",
            "counterexample_lock": closure_by_id["FCCR1220_0_alpha"]["retained_counterexample"],
            "arena": "WEP;clock;R10;EM",
            "source_rows": "ACQ1221_0_alpha;REQ1098_0_c_alpha",
            "schema_valid": True,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_row_id": "RUN1221_1_surface",
            "closure_id": "FCCR1220_1_surface",
            "observable_product": "abs(c_surface_DD)",
            "threshold_abs": closure_by_id["FCCR1220_1_surface"]["threshold_or_source"],
            "threshold_units": "dimensionless",
            "required_numeric_inputs": "c_surface_DD or theorem_zero flag",
            "available_numeric_inputs": "threshold_abs_only",
            "missing_inputs": "MISSING_SOURCE_BACKED_SURFACE_COEFFICIENT;MISSING_PARENT_PRIMITIVE",
            "counterexample_lock": closure_by_id["FCCR1220_1_surface"]["retained_counterexample"],
            "arena": "WEP;clock;nuclear",
            "source_rows": "ACQ1221_1_surface;REQ1098_1_c_surface",
            "schema_valid": True,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_row_id": "RUN1221_2_source_weight",
            "closure_id": "FCCR1220_aux_source_weight",
            "observable_product": "abs(Delta_w_TiPt * tau_WEP)",
            "threshold_abs": "2.8e-15",
            "threshold_units": "dimensionless_eta",
            "required_numeric_inputs": "Delta_w_TiPt,tau_WEP,readout_kernel,source_profile",
            "available_numeric_inputs": "eta_bound_only",
            "missing_inputs": "MISSING_NUMERIC_PRIOR_WIDTH;MISSING_LAB_SOURCE_ORBIT_PROJECTION;MISSING_SOURCE_PROFILE_WEIGHTING",
            "counterexample_lock": source_weight_aux["retained_counterexample"],
            "arena": "MICROSCOPE_WEP;local_GR_source;PPN",
            "source_rows": "ACQ1221_2_source_weight;DWP1066_3_finite_prior_width;TWP1066_7_verdict",
            "schema_valid": True,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_row_id": "RUN1221_3_readout",
            "closure_id": "FCCR1220_4_readout",
            "observable_product": "abs(delta_readout_coefficient)",
            "threshold_abs": "MISSING_RADIOUT_CLOSURE",
            "threshold_units": "arena_dependent",
            "required_numeric_inputs": "official_readout_kernel,coefficient_drift_bound",
            "available_numeric_inputs": "none",
            "missing_inputs": "MISSING_RADIOUT_CLOSURE;OFFICIAL_ARRAYS_NOT_IMPORTED",
            "counterexample_lock": closure_by_id["FCCR1220_4_readout"]["retained_counterexample"],
            "arena": "MICROSCOPE_WEP;clocks;spectroscopy",
            "source_rows": "ACQ1221_3_readout;RIG1084_0_CMSM_arrays",
            "schema_valid": True,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_row_id": "RUN1221_4_common_norm",
            "closure_id": "FCCR1220_2_common_norm",
            "observable_product": "norm(C_parent)",
            "threshold_abs": closure_by_id["FCCR1220_2_common_norm"]["threshold_or_source"],
            "threshold_units": "dimensionless_in_DD_basis",
            "required_numeric_inputs": "coefficient_vector,operator_basis_map,channel_weights",
            "available_numeric_inputs": "threshold_abs_only",
            "missing_inputs": "MISSING_PARENT_OPERATOR_BASIS_MAP;MISSING_COEFFICIENT_VECTOR",
            "counterexample_lock": closure_by_id["FCCR1220_2_common_norm"]["retained_counterexample"],
            "arena": "WEP material vector;local source branch",
            "source_rows": "ACQ1221_4_common_norm;DDP1216_2_combined_abs",
            "schema_valid": True,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_row_id": "RUN1221_5_tail",
            "closure_id": "FCCR1220_3_tail",
            "observable_product": "abs(q_tail(A))",
            "threshold_abs": "MISSING_TAIL_ENVELOPE",
            "threshold_units": "arena_dependent",
            "required_numeric_inputs": "basis_completeness_or_tail_envelope",
            "available_numeric_inputs": "none",
            "missing_inputs": "MISSING_TAIL_ENVELOPE",
            "counterexample_lock": closure_by_id["FCCR1220_3_tail"]["retained_counterexample"],
            "arena": "WEP material diversity;R10 finite-source;local_GR source",
            "source_rows": "ACQ1221_5_tail;FCCR1220_3_tail",
            "schema_valid": True,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    primitive_rows = [
        {
            "primitive_id": "PESC1221_0_parent_grammar",
            "would_reopen_route": "parent typed object-language/action-domain certificate",
            "minimum_signature": "one parent grammar that forbids hidden scalar arguments in visible coefficients before readout",
            "current_source_candidate": "P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv:PTOL1220_7_verdict",
            "current_status": "NOT_FOUND_IN_CURRENT_CORPUS",
            "effect_if_found": "reopen no-hidden-visible theorem route",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "primitive_id": "PESC1221_1_alpha_F2_domain",
            "would_reopen_route": "EM F2 coefficient-domain primitive",
            "minimum_signature": "proof f(I_hid)F_Q^2 is ill-typed or quotient-trivial, not merely absent",
            "current_source_candidate": "P8_Y5_R10_1220_COUNTEREXAMPLE_LOCK_UPDATE.csv:CELOCK1220_1_alpha_F2",
            "current_status": "COUNTEREXAMPLE_ACTIVE",
            "effect_if_found": "close alpha hidden-scalar closure debt",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "primitive_id": "PESC1221_2_matter_constant_superselection",
            "would_reopen_route": "surface/binding fixed-constant primitive",
            "minimum_signature": "species-complete matter functor fixes binding/surface constants or exposes residuals",
            "current_source_candidate": "P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv:PTOL1220_2_matter_bundle_constants",
            "current_status": "NOT_PARENT_SIGNED",
            "effect_if_found": "close surface/binding finite coefficient row or turn it into sourced residual",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "primitive_id": "PESC1221_3_source_weight_owner",
            "would_reopen_route": "action-scale/current/source-label forgetting primitive",
            "minimum_signature": "source-only species weights are syntactically impossible or quotient-gauge redundant",
            "current_source_candidate": "P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv:SSE1066_5_verdict",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "effect_if_found": "turn source-weight WEP branch into theorem-zero after projection closure",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "primitive_id": "PESC1221_4_readout_functor",
            "would_reopen_route": "radiative/readout grammar-preservation primitive",
            "minimum_signature": "S_eff, loops, spectroscopy, and MICROSCOPE readout preserve the same coefficient domain",
            "current_source_candidate": "P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv:PTOL1220_5_radiative_readout_closure",
            "current_status": "UNSIGNED",
            "effect_if_found": "block readout regeneration counterexample",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
    ]

    arena_rows = [
        {
            "arena_id": "ARENA1221_0_MICROSCOPE_WEP",
            "arena": "MICROSCOPE WEP",
            "finite_debts": "alpha;surface;common_norm;source_weight;readout;tail",
            "observable_bound": "eta_TiPt <= 2.8e-15",
            "needed_before_claim": "official readout kernel, source profile weighting, material responses, coefficient values",
            "current_status": "BEST_PRESSURE_ARENA_BUT_NOT_SCORE_CLAIM_READY",
            "source_rows": "R1_WEP_source_charge;AWP1052_0_alpha_Coulomb;TWP1066_7_verdict;RIG1084_0_CMSM_arrays",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "arena_id": "ARENA1221_1_R10",
            "arena": "R10 short-range",
            "finite_debts": "alpha;tail;source_profile;lambda_X",
            "observable_bound": "alpha(lambda) bound curve",
            "needed_before_claim": "lambda_X, K_X(lambda), source/test charges, finite-source correction, promoted bound curve",
            "current_status": "SCHEMA_ONLY_NONCLAIM",
            "source_rows": "RAP1052_0_product_law;FCCR1220_3_tail",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "arena_id": "ARENA1221_2_CLOCKS",
            "arena": "atomic clocks/spectroscopy",
            "finite_debts": "alpha;readout",
            "observable_bound": "b_alpha * tau_clock product only",
            "needed_before_claim": "tau_clock_time relation to the parent residual and readout closure",
            "current_status": "PRODUCT_BOUND_ONLY",
            "source_rows": "ACB1052_2;FCCR1220_4_readout",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "arena_id": "ARENA1221_3_LOCAL_GR_PPN",
            "arena": "local GR/Newton/PPN",
            "finite_debts": "source_weight;common_norm;tail",
            "observable_bound": "PPN/local residual vector",
            "needed_before_claim": "source Hamiltonian/EH limit plus finite source-weight closure",
            "current_status": "INDEPENDENTLY_BLOCKED",
            "source_rows": "CELOCK1220_2_source_weight;DWP1066_3_finite_prior_width",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "arena_id": "ARENA1221_4_EM_CHARGE",
            "arena": "EM/charge sector",
            "finite_debts": "alpha/F2 coefficient",
            "observable_bound": "fine-structure/charge consistency",
            "needed_before_claim": "parent EM F2 coefficient-domain theorem or sourced residual prior",
            "current_status": "THEOREM_ROUTE_BLOCKED_BY_ALPHA_F2_COUNTEREXAMPLE",
            "source_rows": "CELOCK1220_1_alpha_F2;ACQ1221_0_alpha",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    scorepack_rows = []
    for runner_row in runner_rows:
        threshold = runner_row["threshold_abs"]
        threshold_ok = positive_decimal(threshold)
        can_score = threshold_ok and not has_missing(runner_row) and is_true(runner_row, "score_ready")
        scorepack_rows.append(
            {
                "score_id": runner_row["runner_row_id"].replace("RUN", "SCORE"),
                "runner_row_id": runner_row["runner_row_id"],
                "threshold_numeric_positive": threshold_ok,
                "has_missing_inputs": has_missing(runner_row),
                "counterexample_retained": bool(runner_row["counterexample_lock"]),
                "score_ready": can_score,
                "decision": "REFUSE_CLAIM_ROW_UNTIL_INPUTS_SOURCED",
                "reason": runner_row["missing_inputs"] if has_missing(runner_row) else "score_ready flag still false",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    feed_rows = [
        {
            "feed_id": "FEED1221_0_to_1220",
            "target_row": "FCCR1220 finite closure register",
            "update": "closure rows now have acquisition schemas and runner-ready nonclaim score rows",
            "source_rows": "ACQ1221_*;RUN1221_*",
            "current_status": "SCOREPACK_STAGED_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "feed_id": "FEED1221_1_to_WEP",
            "target_row": "MICROSCOPE/WEP source-side route",
            "update": "source_weight/readout/source_profile are P0 acquisition rows; no WEP pass is claimed",
            "source_rows": "ACQ1221_2_source_weight;ACQ1221_3_readout;ARENA1221_0_MICROSCOPE_WEP",
            "current_status": "WEP_SCOREPACK_BLOCKED_BY_INPUTS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "feed_id": "FEED1221_2_to_parent_primitive",
            "target_row": "no-hidden-visible theorem escape hatch",
            "update": "route can reopen only if a genuinely new primitive source signs the grammar/readout/action-scale clauses",
            "source_rows": "PESC1221_*",
            "current_status": "ESCAPE_HATCH_RECORDED_NOT_FOUND",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner_stub = [
        {
            "runner_id": "APR1221_0_closure_scorepack_stub",
            "closure_rows_imported": len(closure_rows),
            "auxiliary_source_weight_rows": 1,
            "runner_nonclaim_rows": len(runner_rows),
            "numeric_threshold_rows": sum(1 for row in runner_rows if positive_decimal(row["threshold_abs"])),
            "score_ready_rows": sum(1 for row in runner_rows if is_true(row, "score_ready")),
            "valid_prediction_rows": sum(1 for row in runner_rows if is_true(row, "valid_for_claim")),
            "claim_allowed": False,
            "expected_result": "refuse every physical claim and provide source-acquisition targets",
            "reason": "thresholds exist for some rows, but coefficients/source profile/readout/parent primitive are missing",
            "valid_for_claim": False,
        }
    ]

    decision_rows = [
        {
            "decision_id": "DEC1221_0_scorepack_not_claim",
            "decision": "convert finite closure debts into scorepack rows, not claims",
            "because": "the 1220 theorem route is demoted and all physical coefficient rows lack sourced inputs",
            "next_action": "write a first nonclaim runner that refuses claims until fields are filled",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1221_1_parent_primitive_escape",
            "decision": "keep parent primitive route open but empty",
            "because": "a new source could still sign the typed grammar, EM F2, source-weight, or readout clauses",
            "next_action": "only reopen theorem route if a genuinely new primitive source is supplied",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1221_2_prioritize_WEP_readout",
            "decision": "make source_weight/readout/profile acquisition P0 beside alpha/surface coefficients",
            "because": "local-GR/WEP pressure is now a coupling/readout problem, not just a coefficient-number problem",
            "next_action": "build a refusal runner and then source the official inputs or derive the parent closure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1221_0_sources",
            "gate": "source path and needle audit",
            "status": "PASS",
            "reason": "all local sources used by 1221 are traceable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1221_1_closure_register",
            "gate": "finite closure register imported",
            "status": "PASS",
            "reason": "five 1220 closure rows plus source-weight auxiliary row are represented",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1221_2_parent_primitive",
            "gate": "new parent primitive source found",
            "status": "BLOCKED",
            "reason": "PESC1221 rows retain NOT_FOUND/UNSIGNED/COUNTEREXAMPLE_ACTIVE status",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1221_3_source_acquisition",
            "gate": "finite coefficient/source/readout inputs acquired",
            "status": "BLOCKED",
            "reason": "ACQ1221 rows are schemas with missing inputs, not sourced values",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1221_4_runner_claim",
            "gate": "runner rows scoreable for claim",
            "status": "BLOCKED",
            "reason": "RUN1221 rows are schema-valid but score_ready=false and valid_for_claim=false",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1221_5_local_GR_WEP_R10",
            "gate": "local GR/WEP/R10 claim permission",
            "status": "BLOCKED",
            "reason": "scorepack rows are private nonclaim plumbing only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_rows = [
        {
            "next_id": "NEXT1221_0_1222",
            "target_file": "1222-Y5-R10-closure-scorepack-runner-first-nonclaim-table.md",
            "target_script": "scripts/Y5_R10_closure_scorepack_runner_first_nonclaim_table.py",
            "task": "build the first mechanical scorepack runner that reads the 1221 rows and refuses claims until every coefficient/source/readout field is numeric and sourced",
            "success_condition": "runner produces an explicit nonclaim table with positive thresholds, missing-input blockers, and zero valid prediction rows",
            "do_not_do": "do not source-fill coefficients by assumption, do not use unity shortcuts, do not claim WEP/local-GR/R10, do not edit formalization-workbench or push GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_tables = [
        (SOURCE_REGISTER_PATH, source_register),
        (INPUT_SCHEMA_PATH, input_schema),
        (ACQUISITION_LEDGER_PATH, acquisition_rows),
        (RUNNER_ROWS_PATH, runner_rows),
        (PARENT_PRIMITIVE_PATH, primitive_rows),
        (ARENA_MAP_PATH, arena_rows),
        (SCOREPACK_DECISION_PATH, scorepack_rows),
        (FEED_PATH, feed_rows),
        (RUNNER_STUB_PATH, runner_stub),
        (DECISION_PATH, decision_rows),
        (CLAIM_GATES_PATH, claim_gates),
        (NEXT_PATH, next_rows),
    ]
    for path, rows in generated_tables:
        write_csv(path, rows)

    validation_rows = []
    validation_rows.append(
        validation_row(
            "VAL1221_0_sources_exist",
            "all cited local sources exist",
            all(is_true(row, "path_exists") for row in source_register),
            f"{sum(1 for row in source_register if is_true(row, 'path_exists'))}/{len(source_register)} sources exist",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1221_1_needles_found",
            "all cited source needles found",
            all(is_true(row, "needle_found") for row in source_register),
            f"{sum(1 for row in source_register if is_true(row, 'needle_found'))}/{len(source_register)} needles found",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1221_2_closure_register_imported",
            "1220 closure register imported",
            len(closure_rows) == 5 and all(row.get("closure_id", "").startswith("FCCR1220_") for row in closure_rows),
            "; ".join(row["closure_id"] for row in closure_rows),
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1221_3_acquisition_coverage",
            "alpha/surface/readout/source-weight acquisition rows exist",
            {"ACQ1221_0_alpha", "ACQ1221_1_surface", "ACQ1221_2_source_weight", "ACQ1221_3_readout"}.issubset(
                {row["acquisition_id"] for row in acquisition_rows}
            ),
            "; ".join(row["acquisition_id"] for row in acquisition_rows),
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1221_4_runner_rows_nonclaim",
            "runner rows remain nonclaim",
            all(is_false(row, "score_ready") and is_false(row, "valid_for_claim") and is_false(row, "claim_allowed") for row in runner_rows),
            f"{len(runner_rows)} runner rows are score_ready=false and valid_for_claim=false",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1221_5_positive_numeric_thresholds",
            "known numeric thresholds are positive",
            all(positive_decimal(row["threshold_abs"]) for row in runner_rows if row["runner_row_id"] in {"RUN1221_0_alpha", "RUN1221_1_surface", "RUN1221_2_source_weight", "RUN1221_4_common_norm"}),
            "alpha/surface/source_weight/common_norm thresholds are positive",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1221_6_missing_rows_nonclaim",
            "rows with MISSING markers are not valid for claim",
            all(is_false(row, "valid_for_claim") and is_false(row, "claim_allowed") for row in runner_rows if has_missing(row)),
            "every MISSING runner row remains nonclaim",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1221_7_parent_primitive_not_found",
            "no escape-hatch primitive is falsely promoted",
            all(str(row["current_status"]) != "FOUND_SIGNED_PRIMITIVE" and is_false(row, "claim_allowed_now") for row in primitive_rows),
            "; ".join(f"{row['primitive_id']}={row['current_status']}" for row in primitive_rows),
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1221_8_scorepack_refuses",
            "scorepack decision rows refuse claims",
            all(is_false(row, "score_ready") and row["decision"] == "REFUSE_CLAIM_ROW_UNTIL_INPUTS_SOURCED" for row in scorepack_rows),
            f"{len(scorepack_rows)} scorepack rows refused",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1221_9_runner_stub_refuses",
            "runner stub has zero valid prediction rows",
            runner_stub[0]["valid_prediction_rows"] == 0 and runner_stub[0]["score_ready_rows"] == 0 and is_false(runner_stub[0], "claim_allowed"),
            "valid_prediction_rows=0; score_ready_rows=0; claim_allowed=false",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1221_10_claim_gates_blocked",
            "claim gates keep physical claims blocked",
            all(row["status"] in {"PASS", "BLOCKED"} and is_false(row, "valid_for_claim") for row in claim_gates)
            and any(row["status"] == "BLOCKED" for row in claim_gates),
            "source/import gates pass; primitive/source/runner/local claim gates blocked",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1221_11_nonclaim_policy",
            "all generated rows remain nonclaim",
            all(
                is_false(row, "valid_for_claim") and is_false(row, "claim_allowed")
                for _, rows in generated_tables
                for row in rows
                if "valid_for_claim" in row and "claim_allowed" in row
            ),
            "valid_for_claim=false and claim_allowed=false throughout claim-bearing tables",
        )
    )

    csv_parse_details = []
    csv_parse_ok = True
    for path, _ in generated_tables:
        try:
            parsed = read_csv(path)
            csv_parse_details.append(f"{path.name}:{len(parsed)}")
        except Exception as exc:  # pragma: no cover - validation reports the failure.
            csv_parse_ok = False
            csv_parse_details.append(f"{path.name}:FAIL:{exc}")
    validation_rows.append(
        validation_row(
            "VAL1221_12_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(csv_parse_details),
        )
    )

    formalization_recent = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*"):
            if path.is_file():
                modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
                if modified >= RUN_STARTED_UTC:
                    formalization_recent.append(path)
    validation_rows.append(
        validation_row(
            "VAL1221_13_formalization_untouched",
            "formalization-workbench untouched during run",
            len(formalization_recent) == 0,
            f"formalization_recent_after_run_start_count={len(formalization_recent)}",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1221_14_next_target",
            "next target is staged",
            next_rows[0]["target_file"] == "1222-Y5-R10-closure-scorepack-runner-first-nonclaim-table.md",
            next_rows[0]["target_file"],
        )
    )

    overall_before = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        validation_row(
            "VAL1221_15_overall",
            "overall 1221 validation",
            overall_before,
            "1221 scorepack/acquisition checkpoint is reproducible, nonclaim, and formalization-safe",
        )
    )
    write_csv(VALIDATION_PATH, validation_rows)

    doc = f"""# 1221 Y5/R10 Finite Coupling Closure Scorepack Or Parent Primitive Source

**Current verdict:** 1221 does **not** close the coupling problem. It turns the finite coupling debts into source-acquisition schemas and runner-ready nonclaim rows, while preserving a narrow escape hatch for a genuinely new parent primitive.

**Main progress:** the missing coupling is now a concrete scorepack interface rather than a foggy objection. Alpha, surface, source-weight, readout, common-norm, and tail rows each have required inputs, provenance hooks, and refusal rules.

**Practical consequence:** no WEP/local-GR/R10/EM claim is allowed yet. The next runner should mechanically refuse every row until coefficients, source profiles, readout kernels, and/or parent primitive certificates are actually sourced.

## Source Register

{markdown_table(source_register, ["source_id", "local_path", "needle", "purpose", "absolute_path", "path_exists", "needle_found", "valid_for_claim", "claim_allowed"])}

## Finite Closure Input Schema

{markdown_table(input_schema, ["schema_id", "input_name", "required_for", "minimum_usable_form", "refusal_if_missing", "current_status", "source_basis", "valid_for_claim", "claim_allowed"])}

## Source Acquisition Ledger

{markdown_table(acquisition_rows, ["acquisition_id", "closure_id", "debt", "arena", "source_to_acquire", "minimum_usable_form", "missing_or_status", "blocker_class", "scorepack_priority", "valid_for_claim", "claim_allowed"])}

## Runner-Ready Nonclaim Rows

{markdown_table(runner_rows, ["runner_row_id", "closure_id", "observable_product", "threshold_abs", "required_numeric_inputs", "available_numeric_inputs", "missing_inputs", "counterexample_lock", "arena", "schema_valid", "score_ready", "valid_for_claim", "claim_allowed"])}

## Parent Primitive Escape Hatch

{markdown_table(primitive_rows, ["primitive_id", "would_reopen_route", "minimum_signature", "current_source_candidate", "current_status", "effect_if_found", "claim_allowed_now", "valid_for_claim"])}

## Empirical Arena Map

{markdown_table(arena_rows, ["arena_id", "arena", "finite_debts", "observable_bound", "needed_before_claim", "current_status", "source_rows", "valid_for_claim", "claim_allowed"])}

## Scorepack Decision Matrix

{markdown_table(scorepack_rows, ["score_id", "runner_row_id", "threshold_numeric_positive", "has_missing_inputs", "counterexample_retained", "score_ready", "decision", "reason", "valid_for_claim", "claim_allowed"])}

## Feed Update

{markdown_table(feed_rows, ["feed_id", "target_row", "update", "source_rows", "current_status", "valid_for_claim", "claim_allowed"])}

## Product Runner Stub

{markdown_table(runner_stub, ["runner_id", "closure_rows_imported", "auxiliary_source_weight_rows", "runner_nonclaim_rows", "numeric_threshold_rows", "score_ready_rows", "valid_prediction_rows", "claim_allowed", "expected_result", "reason", "valid_for_claim"])}

## Decision Ledger

{markdown_table(decision_rows, ["decision_id", "decision", "because", "next_action", "valid_for_claim", "claim_allowed"])}

## Claim Gates

{markdown_table(claim_gates, ["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"])}

## Next Target

{markdown_table(next_rows, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not_do", "valid_for_claim", "claim_allowed"])}

## Validation

{markdown_table(validation_rows, ["check_id", "check", "status", "details", "valid_for_claim", "claim_allowed"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
