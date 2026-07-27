from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1216"
TITLE = "1216-Y5-R10-WEP-same-norm-Cparent-source-readout-or-component-zero"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
FACTOR_ZERO_PATH = OUT_DIR / f"{PACK_ID}_SAME_NORM_FACTOR_ZERO_AUDIT.csv"
SOURCE_FACTOR_PATH = OUT_DIR / f"{PACK_ID}_EARTH_SOURCE_FACTOR_IMPORT.csv"
PRODUCT_PRESSURE_PATH = OUT_DIR / f"{PACK_ID}_DD_SOURCE_MATERIAL_PRODUCT_PRESSURE.csv"
SAME_NORM_UPDATE_PATH = OUT_DIR / f"{PACK_ID}_SAME_NORM_PRODUCT_UPDATE.csv"
FEED_PATH = OUT_DIR / f"{PACK_ID}_WEP_FACTOR_FEED_UPDATE.csv"
RUNNER_PATH = OUT_DIR / f"{PACK_ID}_PRODUCT_RUNNER_STUB.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1216_VALIDATION.csv"


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


def find_row(rows: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    for row in rows:
        if row.get(key) == value:
            return row
    raise ValueError(f"missing row {key}={value}")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1216_0_1215_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1215_NEXT_TARGET.csv",
            "needle": "1216-Y5-R10-WEP-same-norm-Cparent-source-readout-or-component-zero.md",
            "purpose": "1215 handoff to same-norm missing WEP factor",
        },
        {
            "source_id": "SRC1216_1_1215_intake",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1215_WEP_NUMERIC_SUBCOMPONENT_INTAKE.csv",
            "needle": "WEP1215_7_R_source_Earth",
            "purpose": "R_source^Earth missing row to update",
        },
        {
            "source_id": "SRC1216_2_1215_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1215_SAME_NORM_PRODUCT_CONTRACT.csv",
            "needle": "SNP1215_4_claim_verdict",
            "purpose": "same-norm WEP product contract",
        },
        {
            "source_id": "SRC1216_3_1083_source_vector",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1083_DD_EARTH_SOURCE_VECTOR_FIRST_ROW_NONCLAIM.csv",
            "needle": "DD_EARTH1083_0_bulk_weighted",
            "purpose": "numeric bulk Earth DD source vector",
        },
        {
            "source_id": "SRC1216_4_1083_source_products",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1083_DD_SOURCE_MATERIAL_PRODUCT_NONCLAIM.csv",
            "needle": "DD_PRODUCT1083_2_combined_abs",
            "purpose": "numeric DD source-material products",
        },
        {
            "source_id": "SRC1216_5_1083_caveats",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv",
            "needle": "SCG1083_0_profile_weighting",
            "purpose": "source-vector claim caveats",
        },
        {
            "source_id": "SRC1216_6_1083_web",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1083_WEB_SOURCE_REGISTER.csv",
            "needle": "WEB1083_0_MCDONOUGH_2003_TABLE5",
            "purpose": "bulk Earth composition provenance",
        },
        {
            "source_id": "SRC1216_7_1082_parent_map",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1082_PARENT_TO_DD_COEFFICIENT_MAP_ATTEMPT.csv",
            "needle": "PTD1082_4_verdict",
            "purpose": "parent-to-DD coefficient map still unsigned",
        },
        {
            "source_id": "SRC1216_8_1082_readout",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1082_PHYSICAL_MICROSCOPE_READOUT_FILL_ROWS.csv",
            "needle": "ROF1082_1_surrogate_reuse",
            "purpose": "readout fill/source gate",
        },
        {
            "source_id": "SRC1216_9_1080_Cparent",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1080_C_PARENT_COEFFICIENT_CONTRACT.csv",
            "needle": "CP1080_0_definition",
            "purpose": "C_parent still missing",
        },
        {
            "source_id": "SRC1216_10_1081_parent_gate",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1081_PARENT_TO_DD_GATE.csv",
            "needle": "PDD1081_1_coefficient_map",
            "purpose": "MTS-to-DD map gate",
        },
        {
            "source_id": "SRC1216_11_1214_bound",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1214_DELTA_SPECIES_BOUND_FILL.csv",
            "needle": "DSB1214_5_projection_map",
            "purpose": "B_species projection-map row receiving WEP factor update",
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

    earth_source = find_row(
        read_csv(OUT_DIR / "P8_Y5_R10_1083_DD_EARTH_SOURCE_VECTOR_FIRST_ROW_NONCLAIM.csv"),
        "source_vector_id",
        "DD_EARTH1083_0_bulk_weighted",
    )
    source_products = read_csv(OUT_DIR / "P8_Y5_R10_1083_DD_SOURCE_MATERIAL_PRODUCT_NONCLAIM.csv")
    alpha_product = find_row(source_products, "product_id", "DD_PRODUCT1083_0_alpha")
    surface_product = find_row(source_products, "product_id", "DD_PRODUCT1083_1_surface")
    combined_product = find_row(source_products, "product_id", "DD_PRODUCT1083_2_combined_abs")

    factor_zero_rows = [
        {
            "audit_id": "FZ1216_0_Cparent_zero",
            "factor": "C_parent",
            "zero_or_fill_attempt": "derive C_parent=0 for the WEP DD alpha/surface channel",
            "result": "ZERO_NOT_DERIVED",
            "evidence": "1080/1082 keep C_parent and parent-to-DD map missing",
            "claim_effect": "finite coefficient remains required",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "FZ1216_1_Earth_source_zero",
            "factor": "R_source^Earth",
            "zero_or_fill_attempt": "prove Earth source leg is universal common mode or zero",
            "result": "ZERO_NOT_SIGNED_BUT_NUMERIC_BULK_DD_FACTOR_AVAILABLE",
            "evidence": "1083 common-mode route is not signed; bulk DD source vector is numeric",
            "claim_effect": "source leg becomes numeric nonclaim, not theorem-zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "FZ1216_2_Kreadout_zero",
            "factor": "K_MICROSCOPE",
            "zero_or_fill_attempt": "use surrogate or unit readout proxy as K_MICROSCOPE",
            "result": "REFUSED",
            "evidence": "unit/surrogate readout is nonphysical and official arrays remain missing",
            "claim_effect": "readout remains a locked factor",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "FZ1216_3_parent_to_DD_map",
            "factor": "MTS-to-DD map",
            "zero_or_fill_attempt": "identify DD alpha/surface basis with MTS parent basis",
            "result": "NOT_SIGNED",
            "evidence": "PTD1082_4 verdict keeps parent-to-DD map unsigned",
            "claim_effect": "DD products stay external comparator/nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "FZ1216_4_verdict",
            "factor": "one same-norm WEP factor",
            "zero_or_fill_attempt": "fill the Earth-source leg or prove it zero",
            "result": "NUMERIC_BULK_DD_SOURCE_FACTOR_FILLED_NONCLAIM",
            "evidence": "DD_EARTH1083_0 supplies Q_alpha_Earth and Q_surface_Earth; caveats block physical claim",
            "claim_effect": "WEP factor pack improves; full product remains blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    source_factor_rows = [
        {
            "factor_id": "RS1216_0_Earth_DD_bulk_vector",
            "target": "WEP1215_7_R_source_Earth",
            "basis": earth_source["basis"],
            "Q_alpha_Coulomb_Earth": earth_source["Q_alpha_Coulomb_Earth"],
            "Q_surface_binding_Earth": earth_source["Q_surface_binding_Earth"],
            "source_rows": earth_source["source_rows"],
            "status": "NUMERIC_BULK_EARTH_DD_SOURCE_FACTOR_NONCLAIM",
            "claim_blocker": earth_source["claim_blocker"],
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "factor_id": "RS1216_1_source_profile_gate",
            "target": "WEP1215_7_R_source_Earth.profile_weighting",
            "basis": "MICROSCOPE_orbit_worldtube_profile",
            "Q_alpha_Coulomb_Earth": "MISSING_PROFILE_WEIGHTED_VALUE",
            "Q_surface_binding_Earth": "MISSING_PROFILE_WEIGHTED_VALUE",
            "source_rows": "P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv:SCG1083_0_profile_weighting",
            "status": "MISSING_PROFILE_WEIGHTING_FOR_CLAIM",
            "claim_blocker": "bulk Earth vector is not shell/profile/worldtube weighted",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    product_pressure_rows = [
        {
            "pressure_id": "DDP1216_0_alpha",
            "component": alpha_product["component"],
            "source_value": alpha_product["source_value"],
            "material_delta_abs": alpha_product["material_delta_abs"],
            "source_material_product_abs": alpha_product["product_abs"],
            "eta_bound": alpha_product["eta_bound"],
            "required_abs_coefficient_max_if_single_component": alpha_product["required_abs_coefficient_max_if_single_component"],
            "required_abs_coefficient_max_if_equal_component": "",
            "status": "NUMERIC_DD_SOURCE_MATERIAL_PRESSURE_NONCLAIM",
            "claim_blocker": "C_parent/MTS-to-DD map and K_MICROSCOPE are missing; bulk source not profile-weighted",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pressure_id": "DDP1216_1_surface",
            "component": surface_product["component"],
            "source_value": surface_product["source_value"],
            "material_delta_abs": surface_product["material_delta_abs"],
            "source_material_product_abs": surface_product["product_abs"],
            "eta_bound": surface_product["eta_bound"],
            "required_abs_coefficient_max_if_single_component": surface_product["required_abs_coefficient_max_if_single_component"],
            "required_abs_coefficient_max_if_equal_component": "",
            "status": "NUMERIC_DD_SOURCE_MATERIAL_PRESSURE_NONCLAIM",
            "claim_blocker": "C_parent/MTS-to-DD map and K_MICROSCOPE are missing; bulk source not profile-weighted",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pressure_id": "DDP1216_2_combined_abs",
            "component": combined_product["component"],
            "source_value": combined_product["source_value"],
            "material_delta_abs": combined_product["material_delta_abs"],
            "source_material_product_abs": combined_product["product_abs"],
            "eta_bound": combined_product["eta_bound"],
            "required_abs_coefficient_max_if_single_component": "",
            "required_abs_coefficient_max_if_equal_component": combined_product["required_abs_coefficient_max_if_equal_component"],
            "status": "NUMERIC_DD_SOURCE_MATERIAL_PRESSURE_NONCLAIM",
            "claim_blocker": "C_parent/MTS-to-DD map and K_MICROSCOPE are missing; bulk source not profile-weighted",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    same_norm_rows = [
        {
            "update_id": "SNU1216_0_formula_update",
            "object": "same-norm WEP product",
            "previous_status": "C_parent, R_source, K_MICROSCOPE missing",
            "new_status": "R_source bulk DD factor numeric nonclaim; C_parent, K_MICROSCOPE, profile weighting, and parent-to-DD map still missing",
            "formula": "B_species,WEP <= |K_MICROSCOPE| * (|C_alpha| |Q_E_alpha| |DeltaQ_alpha| + |C_surface| |Q_E_surface| |DeltaQ_surface| + tail)",
            "claim_policy": "numeric pressure row only; not a prediction until C_parent/MTS-to-DD and readout/profile locks close",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "update_id": "SNU1216_1_claim_verdict",
            "object": "first same-norm missing factor",
            "previous_status": "WEP1215_7_R_source_Earth missing",
            "new_status": "filled as DD bulk source factor, not physical claim source vector",
            "formula": "R_source^Earth_DD_bulk = (1.691260686750872e-03, -1.211918219995745e-02)",
            "claim_policy": "counts as numeric scaffold progress, not local-GR/WEP evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    feed_rows = [
        {
            "feed_id": "WFEED1216_0_to_WEP1215_7",
            "target_row": "WEP1215_7_R_source_Earth",
            "field_to_fill": "value",
            "source_row": "RS1216_0_Earth_DD_bulk_vector",
            "update_value": "Q_alpha_Earth=1.691260686750872e-03;Q_surface_Earth=-1.211918219995745e-02",
            "claim_policy": "nonclaim bulk-DD source factor only; profile/readout/parent map still required",
            "current_status": "PARTIAL_NUMERIC_SOURCE_FACTOR_PRODUCT_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "feed_id": "WFEED1216_1_to_SNP1215_0",
            "target_row": "SNP1215_0_WEP_formula",
            "field_to_fill": "R_source",
            "source_row": "DDP1216_0_alpha;DDP1216_1_surface;DDP1216_2_combined_abs",
            "update_value": "numeric DD source-material pressure rows available",
            "claim_policy": "does not create valid prediction rows until C_parent and K_MICROSCOPE are sourced or derived",
            "current_status": "NUMERIC_PRESSURE_ROWS_CLAIM_LOCKED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "feed_id": "WFEED1216_2_to_DSB1214_5",
            "target_row": "DSB1214_5_projection_map",
            "field_to_fill": "WEP_R_source",
            "source_row": "RS1216_0_Earth_DD_bulk_vector",
            "update_value": "bulk DD Earth source vector numeric",
            "claim_policy": "projection map still missing C_parent/K/readout/profile and cannot score B_species",
            "current_status": "PARTIAL_NUMERIC_SUBCOMPONENT_PRODUCT_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner_rows = [
        {
            "runner_id": "APR1216_0_WEP_same_norm_source_factor_stub",
            "prediction_rows": 1,
            "valid_prediction_rows": 0,
            "numeric_source_factor_rows": 1,
            "numeric_pressure_rows": 3,
            "claim_allowed": False,
            "expected_result": "accept bulk DD source factor as nonclaim scaffold and reject full product",
            "reason": "C_parent/MTS-to-DD map, K_MICROSCOPE, and source profile weighting remain missing",
            "valid_for_claim": False,
        }
    ]

    decisions = [
        {
            "decision_id": "DEC1216_0_source_factor_progress",
            "decision": "promote R_source^Earth from missing to numeric bulk-DD nonclaim factor",
            "because": "1083 already built a numeric Earth source vector and source-material product rows with provenance",
            "next_action": "use this as a pressure scaffold while keeping profile/readout/parent-map locks explicit",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1216_1_no_claim",
            "decision": "do not call this a WEP/local-GR prediction",
            "because": "bulk composition is not shell/worldtube weighted and DD basis is not MTS-derived",
            "next_action": "target C_parent or K_MICROSCOPE next; profile weighting remains a parallel data lock",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1216_2_next_route",
            "decision": "go after C_parent / parent-to-DD coefficient map next",
            "because": "without C_parent, even a perfect source vector and readout kernel cannot become an MTS prediction",
            "next_action": "1217 should try a narrow C_parent coefficient-map theorem or explicit finite coefficient prior row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1216_0_R_source_bulk_numeric",
            "gate": "R_source^Earth bulk DD factor numeric",
            "status": "PASS_NONCLAIM",
            "reason": "DD_EARTH1083_0 supplies numeric Q_alpha and Q_surface values",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1216_1_R_source_physical",
            "gate": "R_source^Earth physical/profile-weighted claim vector",
            "status": "BLOCKED",
            "reason": "bulk composition is not shell/profile/worldtube weighted for MICROSCOPE orbit",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1216_2_Cparent",
            "gate": "C_parent or MTS-to-DD coefficient map",
            "status": "BLOCKED",
            "reason": "parent coefficient vector and operator pullback remain unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1216_3_Kreadout",
            "gate": "K_MICROSCOPE official/validated readout",
            "status": "BLOCKED",
            "reason": "official arrays/masks/readout normalization not imported",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1216_4_product",
            "gate": "claim-valid same-norm WEP product",
            "status": "BLOCKED",
            "reason": "valid_prediction_rows=0; numeric pressure rows are nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_rows = [
        {
            "next_id": "NEXT1216_0_1217",
            "target_file": "1217-Y5-R10-WEP-Cparent-coefficient-map-or-finite-prior-row.md",
            "target_script": "scripts/Y5_R10_WEP_Cparent_coefficient_map_or_finite_prior_row.py",
            "task": "try to derive the MTS-to-DD C_parent coefficient map for the alpha/surface WEP branch; if it fails, stage an explicit finite coefficient-prior row with units/provenance and no claim",
            "success_condition": "C_parent becomes theorem-zero, source-backed/numeric in the DD branch, or explicitly retained as the next missing claim lock with a stricter prior-row contract",
            "do_not_do": "do not treat DD products as MTS coefficients; do not use unit readout/source proxies as physical normalization; do not tune cancellation; do not claim local GR/WEP/R10; do not edit formalization-workbench or push GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    source_fields = ["source_id", "local_path", "needle", "purpose", "absolute_path", "path_exists", "needle_found", "valid_for_claim", "claim_allowed"]
    zero_fields = ["audit_id", "factor", "zero_or_fill_attempt", "result", "evidence", "claim_effect", "valid_for_claim", "claim_allowed"]
    factor_fields = ["factor_id", "target", "basis", "Q_alpha_Coulomb_Earth", "Q_surface_binding_Earth", "source_rows", "status", "claim_blocker", "valid_for_claim", "claim_allowed"]
    pressure_fields = ["pressure_id", "component", "source_value", "material_delta_abs", "source_material_product_abs", "eta_bound", "required_abs_coefficient_max_if_single_component", "required_abs_coefficient_max_if_equal_component", "status", "claim_blocker", "valid_for_claim", "claim_allowed"]
    update_fields = ["update_id", "object", "previous_status", "new_status", "formula", "claim_policy", "valid_for_claim", "claim_allowed"]
    feed_fields = ["feed_id", "target_row", "field_to_fill", "source_row", "update_value", "claim_policy", "current_status", "valid_for_claim", "claim_allowed"]
    runner_fields = ["runner_id", "prediction_rows", "valid_prediction_rows", "numeric_source_factor_rows", "numeric_pressure_rows", "claim_allowed", "expected_result", "reason", "valid_for_claim"]
    decision_fields = ["decision_id", "decision", "because", "next_action", "valid_for_claim", "claim_allowed"]
    gate_fields = ["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"]
    next_fields = ["next_id", "target_file", "target_script", "task", "success_condition", "do_not_do", "valid_for_claim", "claim_allowed"]

    write_csv(SOURCE_REGISTER_PATH, source_rows, source_fields)
    write_csv(FACTOR_ZERO_PATH, factor_zero_rows, zero_fields)
    write_csv(SOURCE_FACTOR_PATH, source_factor_rows, factor_fields)
    write_csv(PRODUCT_PRESSURE_PATH, product_pressure_rows, pressure_fields)
    write_csv(SAME_NORM_UPDATE_PATH, same_norm_rows, update_fields)
    write_csv(FEED_PATH, feed_rows, feed_fields)
    write_csv(RUNNER_PATH, runner_rows, runner_fields)
    write_csv(DECISION_PATH, decisions, decision_fields)
    write_csv(CLAIM_GATES_PATH, claim_gates, gate_fields)
    write_csv(NEXT_PATH, next_rows, next_fields)

    csvs_to_parse = [
        SOURCE_REGISTER_PATH,
        FACTOR_ZERO_PATH,
        SOURCE_FACTOR_PATH,
        PRODUCT_PRESSURE_PATH,
        SAME_NORM_UPDATE_PATH,
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
    source_vector_numeric = float(earth_source["Q_alpha_Coulomb_Earth"]) > 0 and abs(float(earth_source["Q_surface_binding_Earth"])) > 0
    pressure_rows_numeric = all(float(row["source_material_product_abs"]) > 0 for row in product_pressure_rows)
    coefficient_bounds_positive = all(
        float(row["required_abs_coefficient_max_if_single_component"] or row["required_abs_coefficient_max_if_equal_component"]) > 0
        for row in product_pressure_rows
    )
    zero_not_overclaimed = any(row["audit_id"] == "FZ1216_4_verdict" and row["result"] == "NUMERIC_BULK_DD_SOURCE_FACTOR_FILLED_NONCLAIM" for row in factor_zero_rows)
    runner_refuses = runner_rows[0]["valid_prediction_rows"] == 0 and not runner_rows[0]["claim_allowed"]
    source_gate_pass_nonclaim = any(row["gate_id"] == "GATE1216_0_R_source_bulk_numeric" and row["status"] == "PASS_NONCLAIM" for row in claim_gates)
    claim_locks_blocked = all(
        any(row["gate_id"] == gate_id and row["status"] == "BLOCKED" for row in claim_gates)
        for gate_id in ["GATE1216_1_R_source_physical", "GATE1216_2_Cparent", "GATE1216_3_Kreadout", "GATE1216_4_product"]
    )
    no_missing_claim_rows = all(
        not (not as_false(row, "valid_for_claim") and "MISSING" in " ".join(str(value) for value in row.values()))
        for row in source_factor_rows + feed_rows
    )
    no_claim = all(
        as_false(row, "valid_for_claim") and as_false(row, "claim_allowed")
        for row in factor_zero_rows + source_factor_rows + product_pressure_rows + same_norm_rows + feed_rows + runner_rows + decisions + claim_gates + next_rows
    )
    formalization_untouched = len(formalization_recent) == 0
    next_1217 = next_rows[0]["target_file"].startswith("1217-")

    validation_rows = [
        validation_row("VAL1216_0_sources_exist", "all cited local sources exist", all_sources_exist, f"{sum(bool(row['path_exists']) for row in source_rows)}/{len(source_rows)} sources exist"),
        validation_row("VAL1216_1_needles_found", "all cited source needles found", all_needles_found, f"{sum(bool(row['needle_found']) for row in source_rows)}/{len(source_rows)} needles found"),
        validation_row("VAL1216_2_source_vector_numeric", "bulk Earth DD source factor is numeric", source_vector_numeric, f"Q_alpha={earth_source['Q_alpha_Coulomb_Earth']};Q_surface={earth_source['Q_surface_binding_Earth']}"),
        validation_row("VAL1216_3_pressure_rows_numeric", "source-material pressure rows numeric", pressure_rows_numeric, "; ".join(f"{row['pressure_id']}={row['source_material_product_abs']}" for row in product_pressure_rows)),
        validation_row("VAL1216_4_coefficient_bounds_positive", "derived coefficient pressure bounds positive", coefficient_bounds_positive, "; ".join(f"{row['pressure_id']}={row['required_abs_coefficient_max_if_single_component'] or row['required_abs_coefficient_max_if_equal_component']}" for row in product_pressure_rows)),
        validation_row("VAL1216_5_zero_not_overclaimed", "factor zero is not overclaimed", zero_not_overclaimed, "source factor filled nonclaim rather than theorem-zero"),
        validation_row("VAL1216_6_runner_refuses", "runner stub refuses missing full product", runner_refuses, "valid_prediction_rows=0 and claim_allowed=false"),
        validation_row("VAL1216_7_source_gate_nonclaim", "source factor gate passes only as nonclaim", source_gate_pass_nonclaim, "GATE1216_0 status PASS_NONCLAIM"),
        validation_row("VAL1216_8_claim_locks_blocked", "remaining claim locks blocked", claim_locks_blocked, "profile/source, Cparent, Kreadout, product gates blocked"),
        validation_row("VAL1216_9_no_missing_claim_rows", "no row with MISSING is valid for claim", no_missing_claim_rows, "missing profile/feed rows remain nonclaim"),
        validation_row("VAL1216_10_nonclaim_policy", "all generated rows remain nonclaim", no_claim, "valid_for_claim=false and claim_allowed=false throughout"),
        validation_row("VAL1216_11_csv_parse", "all generated CSVs parse cleanly", csv_parse_ok, "; ".join(parse_details)),
        validation_row("VAL1216_12_formalization_untouched", "formalization-workbench untouched during run", formalization_untouched, f"formalization_recent_after_run_start_count={len(formalization_recent)}"),
        validation_row("VAL1216_13_next_target", "next target is staged", next_1217, next_rows[0]["target_file"]),
    ]
    validation_pass = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        validation_row(
            "VAL1216_14_overall",
            "overall 1216 validation",
            validation_pass,
            "1216 WEP same-norm source-factor pack is reproducible, numeric-source-backed, and nonclaim" if validation_pass else "one or more validation checks failed",
        )
    )
    validation_fields = ["check_id", "check", "status", "details", "valid_for_claim", "claim_allowed"]
    write_csv(VALIDATION_PATH, validation_rows, validation_fields)

    doc = f"""# 1216 Y5/R10 WEP Same-Norm Cparent Source Readout Or Component Zero

**Current verdict:** 1216 does **not** close the WEP same-norm product or prove a component zero. It does upgrade `R_source^Earth` from missing to a numeric bulk-Earth DD source factor, with source-material pressure rows imported as nonclaim scaffolding.

**Main progress:** the WEP branch now has numeric DD material deltas, a numeric bulk Earth DD source vector, and numeric source-material products. The remaining locks are `C_parent`/MTS-to-DD map, `K_MICROSCOPE` readout, and source profile/worldtube weighting.

**Why this matters:** we are no longer only saying “source vector missing.” We have an explicit numeric source leg and can now focus the derivation pressure on the actual coupling coefficient owner.

## Source Register

{markdown_table(source_rows, source_fields)}

## Same-Norm Factor Zero Audit

{markdown_table(factor_zero_rows, zero_fields)}

## Earth Source Factor Import

{markdown_table(source_factor_rows, factor_fields)}

## DD Source-Material Product Pressure

{markdown_table(product_pressure_rows, pressure_fields)}

## Same-Norm Product Update

{markdown_table(same_norm_rows, update_fields)}

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
    print("R_source_Earth_numeric_nonclaim=true")
    print("valid_prediction_rows=0")


if __name__ == "__main__":
    main()
