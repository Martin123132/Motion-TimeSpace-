from __future__ import annotations

import csv
import math
from pathlib import Path


PACK_ID = "P8_Y5_R10_1329"
TITLE = "1329-Y5-R10-RAB-electron-fraction-extractor-dryrun-or-DD-basis-map-demotion"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
COMPONENT_ROOT = ROOT / "source-intake" / "component-fractions"
COMPONENT_RAW = COMPONENT_ROOT / "raw"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
INPUT_CONSTANTS_PATH = OUT_DIR / f"{PACK_ID}_ELECTRON_FRACTION_INPUT_CONSTANTS.csv"
ELEMENT_CONTRIB_PATH = OUT_DIR / f"{PACK_ID}_ELECTRON_FRACTION_ELEMENT_CONTRIBUTIONS.csv"
ELECTRON_DRYRUN_PATH = OUT_DIR / f"{PACK_ID}_ELECTRON_FRACTION_DRYRUN_ROWS.csv"
RAW_CANDIDATE_PATH = COMPONENT_RAW / f"{PACK_ID}_ELECTRON_FRACTION_CANDIDATE_NONCLAIM.csv"
DELTA_PATH = OUT_DIR / f"{PACK_ID}_ELECTRON_FRACTION_DELTA_VECTOR.csv"
ACCEPTANCE_PATH = OUT_DIR / f"{PACK_ID}_ELECTRON_FRACTION_ACCEPTANCE_LEDGER.csv"
DD_DEMOTION_PATH = OUT_DIR / f"{PACK_ID}_DD_BASIS_MAP_DEMOTION_LEDGER.csv"
RUNNER_PATH = OUT_DIR / f"{PACK_ID}_DELTA_W_RUNNER_UPDATE.csv"
ANTI_SHORTCUT_PATH = OUT_DIR / f"{PACK_ID}_ANTI_SHORTCUT_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1329_VALIDATION.csv"

M_E_U = 0.000548579909065
M_E_U_SOURCE = "CODATA/NIST electron mass in atomic mass units; manual dry-run constant"

STANDARD_ATOMIC_WEIGHTS = {
    "Ti": 47.867,
    "Al": 26.9815385,
    "V": 50.9415,
    "Pt": 195.084,
    "Rh": 102.90550,
}

MATERIAL_ID_MAP = {
    "M983_0_PtRh10": "PtRh10",
    "M983_1_TiAlloy": "TA6V",
}


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
    return str(value).strip().lower() == "false"


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    for table in tables:
        for row in table:
            if "valid_for_claim" in row and not is_false(row.get("valid_for_claim", False)):
                return False
            if "claim_allowed" in row and not is_false(row.get("claim_allowed", False)):
                return False
    return True


def generated_inside_formalization() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    return [path for path in FORMALIZATION.rglob("*1329*") if path.is_file()]


def finite_positive(value: object) -> bool:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return False
    return math.isfinite(number) and number > 0.0


def finite_nonnegative(value: object) -> bool:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return False
    return math.isfinite(number) and number >= 0.0


def fmt(value: float) -> str:
    return f"{value:.12e}"


def compute_rows(material_rows: list[dict[str, str]]) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    by_material: dict[str, list[dict[str, str]]] = {}
    for row in material_rows:
        material_id = MATERIAL_ID_MAP.get(row["material_id"], row["material_id"])
        by_material.setdefault(material_id, []).append(row)

    input_constants: list[dict[str, object]] = [
        {
            "constant_id": "CONST1329_0_m_e_u",
            "symbol": "m_e/u",
            "value": fmt(M_E_U),
            "units": "dimensionless atomic-mass-unit ratio",
            "source": M_E_U_SOURCE,
            "status": "MANUAL_DRYRUN_CONSTANT_NOT_CLAIM_GRADE",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]
    for element, atomic_weight in STANDARD_ATOMIC_WEIGHTS.items():
        input_constants.append(
            {
                "constant_id": f"CONST1329_{element}_atomic_weight",
                "symbol": f"A_std({element})",
                "value": str(atomic_weight),
                "units": "u",
                "source": "PSRC1328_3_NIST_atomic_weights_isotopic_compositions",
                "status": "MANUAL_DRYRUN_VALUE_NOT_AUDITED_EXTRACTION",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    element_contrib: list[dict[str, object]] = []
    dryrun_rows: list[dict[str, object]] = []
    for material_id in ["TA6V", "PtRh10"]:
        material = by_material[material_id]
        nist_fraction = 0.0
        microscope_a_fraction = 0.0
        for row in material:
            element = row["element"]
            mass_fraction = float(row["mass_fraction"])
            charge_z = float(row["Z"])
            microscope_a = float(row["A"])
            nist_a = STANDARD_ATOMIC_WEIGHTS[element]
            microscope_contribution = mass_fraction * charge_z * M_E_U / microscope_a
            nist_contribution = mass_fraction * charge_z * M_E_U / nist_a
            microscope_a_fraction += microscope_contribution
            nist_fraction += nist_contribution
            element_contrib.append(
                {
                    "contribution_id": f"EFC1329_{material_id}_{element}",
                    "material_id": material_id,
                    "element": element,
                    "mass_fraction": row["mass_fraction"],
                    "Z": row["Z"],
                    "A_microscope_context": row["A"],
                    "A_nist_standard_weight": str(nist_a),
                    "microscope_A_contribution": fmt(microscope_contribution),
                    "nist_weight_contribution": fmt(nist_contribution),
                    "source": row["source"] + ";PSRC1328_3_NIST_atomic_weights_isotopic_compositions",
                    "status": "DRYRUN_CONTRIBUTION_NOT_CLAIM_GRADE",
                    "valid_for_claim": False,
                    "claim_allowed": False,
                }
            )

        crosscheck_spread = abs(nist_fraction - microscope_a_fraction)
        uncertainty = max(0.01 * nist_fraction, crosscheck_spread)
        dryrun_rows.append(
            {
                "row_id": f"CFI1329_{material_id}_electron",
                "material_id": material_id,
                "component_id": "electron",
                "fraction_value": fmt(nist_fraction),
                "fraction_uncertainty": fmt(uncertainty),
                "basis_convention": "other_with_source",
                "source_path_or_url": "source-intake/mts_residuals/P8_Y5_R10_983_MATERIAL_CONSTITUENTS.csv;source-intake/mts_residuals/P8_Y5_R10_1080_MATERIAL_COMPOSITION_AND_TENSOR_CANDIDATES.csv;PSRC1328_3_NIST_atomic_weights_isotopic_compositions",
                "extraction_method": "formula",
                "microscope_A_crosscheck_fraction": fmt(microscope_a_fraction),
                "uncertainty_model": "max(1_percent_dryrun_envelope, abs(NIST_standard_weight_fraction - MICROSCOPE_A_context_fraction))",
                "status": "SCHEMA_VALID_NUMERIC_DRYRUN_NONCLAIM",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return input_constants, element_contrib, dryrun_rows


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    COMPONENT_RAW.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1329_0_1328_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1328_NEXT_TARGET.csv",
            "needle": "NEXT1328_0_1329",
            "role": "selected 1329 target",
        },
        {
            "source_id": "SRC1329_1_1328_public_sources",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1328_PUBLIC_SOURCE_CANDIDATE_REGISTER.csv",
            "needle": "PSRC1328_3_NIST_atomic_weights_isotopic_compositions",
            "role": "electron source candidate provenance",
        },
        {
            "source_id": "SRC1329_2_1328_route_matrix",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1328_COMPONENT_SOURCE_ROUTE_MATRIX.csv",
            "needle": "ROUTE1328_TA6V_electron",
            "role": "electron route matrix",
        },
        {
            "source_id": "SRC1329_3_1233_schema",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1233_COMPONENT_FRACTION_SCHEMA.csv",
            "needle": "fraction_value",
            "role": "component fraction schema",
        },
        {
            "source_id": "SRC1329_4_983_material_constituents",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_983_MATERIAL_CONSTITUENTS.csv",
            "needle": "M983_1_TiAlloy",
            "role": "local MICROSCOPE constituent rows",
        },
        {
            "source_id": "SRC1329_5_1080_material_context",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1080_MATERIAL_COMPOSITION_AND_TENSOR_CANDIDATES.csv",
            "needle": "MAT1080_1_TA6V_MICROSCOPE",
            "role": "source-backed material context and nonclaim gate",
        },
        {
            "source_id": "SRC1329_6_1328_validation",
            "local_path": "source-intake/mts_residuals/P8_Y5_BRR545_1328_VALIDATION.csv",
            "needle": "VAL1328_11_overall",
            "role": "1328 pass gate",
        },
    ]
    source_register: list[dict[str, object]] = []
    for spec in source_specs:
        exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_register.append(
            {
                **spec,
                "exists": exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    material_rows = read_csv(source_path("source-intake/mts_residuals/P8_Y5_R10_983_MATERIAL_CONSTITUENTS.csv"))
    input_constants, element_contrib, dryrun_rows = compute_rows(material_rows)

    raw_candidate_rows = [
        {
            "row_id": row["row_id"],
            "material_id": row["material_id"],
            "component_id": row["component_id"],
            "fraction_value": row["fraction_value"],
            "fraction_uncertainty": row["fraction_uncertainty"],
            "basis_convention": row["basis_convention"],
            "source_path_or_url": row["source_path_or_url"],
            "extraction_method": row["extraction_method"],
            "valid_for_claim": row["valid_for_claim"],
        }
        for row in dryrun_rows
    ]

    by_material = {row["material_id"]: row for row in dryrun_rows}
    ta6v_fraction = float(by_material["TA6V"]["fraction_value"])
    ptrh_fraction = float(by_material["PtRh10"]["fraction_value"])
    ta6v_uncertainty = float(by_material["TA6V"]["fraction_uncertainty"])
    ptrh_uncertainty = float(by_material["PtRh10"]["fraction_uncertainty"])
    delta = ta6v_fraction - ptrh_fraction
    delta_uncertainty = math.sqrt(ta6v_uncertainty**2 + ptrh_uncertainty**2)
    delta_rows = [
        {
            "delta_id": "DELTA1329_0_TA6V_minus_PtRh10_electron",
            "component_id": "electron",
            "left_material": "TA6V",
            "right_material": "PtRh10",
            "delta_fraction": fmt(delta),
            "abs_delta_fraction": fmt(abs(delta)),
            "delta_uncertainty": fmt(delta_uncertainty),
            "interpretation": "electron rest-mass fraction contrast only; not WEP and not full Delta_w_TiPt",
            "status": "NUMERIC_DRYRUN_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    acceptance = [
        {
            "acceptance_id": "ACC1329_0_schema_rows",
            "target": "raw electron candidate rows",
            "status": "SCHEMA_VALID_NUMERIC_NONCLAIM",
            "details": f"raw_path={RAW_CANDIDATE_PATH};rows={len(raw_candidate_rows)}",
            "blocks_claim": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "acceptance_id": "ACC1329_1_numeric_values",
            "target": "fraction_value and fraction_uncertainty",
            "status": "FINITE_NUMERIC",
            "details": "all electron dry-run rows finite; uncertainty is dry-run envelope not source-grade",
            "blocks_claim": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "acceptance_id": "ACC1329_2_parent_normalization",
            "target": "MTS parent mass-normalization convention",
            "status": "MISSING_PARENT_SIGNATURE",
            "details": "electron rest mass is measurable, but parent must still sign whether this is the source-weight component used in Delta_w",
            "blocks_claim": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "acceptance_id": "ACC1329_3_component_completeness",
            "target": "full Delta_w_TiPt component vector",
            "status": "INCOMPLETE_ONE_COMPONENT_ONLY",
            "details": "light_quark, QCD_gluon, EM_Coulomb, nuclear_surface, and measure_readout remain unresolved",
            "blocks_claim": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    dd_demotion = [
        {
            "demotion_id": "DD1329_0_parent_basis_map",
            "object": "Damour-Donoghue charge basis",
            "status": "DEMOTED_TO_EXTERNAL_COMPARATOR",
            "reason": "DD charges are valuable physics, but not derived from the MTS parent action in the current corpus",
            "needed_for_promotion": "explicit parent basis map from MTS source weights to DD charge vector with no double counting",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "demotion_id": "DD1329_1_alpha_surface_smoke",
            "object": "existing alpha/surface smoke deltas",
            "status": "KEEP_QUARANTINED",
            "reason": "smoke deltas are useful comparator pressure, not a full material response tensor",
            "needed_for_promotion": "source-backed component fractions and parent coefficient map",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner = [
        {
            "runner_id": "RUN1329_0_electron_component",
            "target": "electron component of finite Delta_w_TiPt",
            "input_status": "NUMERIC_DRYRUN_AVAILABLE_NONCLAIM",
            "runner_status": "PARTIAL_COMPONENT_READY_NOT_SCOREABLE",
            "reason": "electron contrast is numeric, but one component cannot score WEP or close local GR",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN1329_1_full_Delta_w",
            "target": "full Delta_w_TiPt source vector",
            "input_status": "MISSING_NON_ELECTRON_COMPONENTS_AND_PARENT_MAP",
            "runner_status": "REFUSED_NOT_SCOREABLE",
            "reason": "quark/QCD/EM/nuclear/readout components and parent basis map remain missing",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    anti_shortcut = [
        {
            "gate_id": "SHORT1329_0_no_electron_only_WEP",
            "shortcut": "score WEP from electron fraction contrast alone",
            "enforcement": "REFUSED",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1329_1_no_NIST_manual_as_claim",
            "shortcut": "treat manually entered atomic weights as audited claim-grade extraction",
            "enforcement": "REFUSED until a table/digitization extractor is audited",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1329_2_no_DD_parent_basis_shortcut",
            "shortcut": "promote DD charges to MTS parent basis",
            "enforcement": "REFUSED by DD demotion ledger",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1329_3_no_local_GR_claim",
            "shortcut": "turn one component dry-run into local-GR pass",
            "enforcement": "REFUSED",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1329_0_electron_progress",
            "decision": "electron component is now numeric in dry-run form",
            "because": "composition and mass-normalization inputs are concrete enough for a nonclaim formula pass",
            "effect": "we have the first real component contrast, but no full Delta_w or WEP score",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1329_1_next_bottleneck",
            "decision": "next bottleneck is parent basis mapping or audited extraction",
            "because": "electron fraction alone is clean but too small a slice of the source vector",
            "effect": "move to either audited atomic/isotope extraction or parent DD/QCD map gate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1329_0_1330",
            "target_file": "1330-Y5-R10-RAB-audited-electron-source-extractor-or-parent-DD-map-gate.md",
            "target_script": "scripts/Y5_R10_RAB_audited_electron_source_extractor_or_parent_DD_map_gate.py",
            "task": "replace manual atomic-weight constants with an audited source extractor, or attempt the parent map from MTS source weights to external DD charges",
            "success_condition": "electron fraction rows become audit-extracted nonclaim inputs, or DD remains explicitly demoted with a sharper parent-map theorem blocker",
            "do_not": "do not score WEP, do not promote DD to parent MTS, do not claim Delta_w=0, and do not claim local GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    schema_fields = [
        "row_id",
        "material_id",
        "component_id",
        "fraction_value",
        "fraction_uncertainty",
        "basis_convention",
        "source_path_or_url",
        "extraction_method",
        "valid_for_claim",
    ]
    write_csv(RAW_CANDIDATE_PATH, raw_candidate_rows, schema_fields)

    tables_for_nonclaim = [
        source_register,
        input_constants,
        element_contrib,
        dryrun_rows,
        raw_candidate_rows,
        delta_rows,
        acceptance,
        dd_demotion,
        runner,
        anti_shortcut,
        decision,
        next_target,
    ]

    source_anchor_count = sum(1 for row in source_register if row["exists"] and row["needle_found"])
    raw_exists = RAW_CANDIDATE_PATH.exists()
    raw_rows = read_csv(RAW_CANDIDATE_PATH) if raw_exists else []
    raw_schema_ok = len(raw_rows) == 2 and all(set(schema_fields).issubset(row.keys()) for row in raw_rows)
    raw_numeric_ok = all(
        finite_positive(row.get("fraction_value")) and finite_nonnegative(row.get("fraction_uncertainty"))
        for row in raw_rows
    )
    raw_nonclaim = all(is_false(row.get("valid_for_claim", False)) for row in raw_rows)
    dryrun_numeric_ok = all(finite_positive(row["fraction_value"]) for row in dryrun_rows) and finite_positive(delta_rows[0]["abs_delta_fraction"])
    one_component_only = sorted({row["component_id"] for row in dryrun_rows}) == ["electron"]
    runner_not_scoreable = all(not bool(row["score_ready"]) and row["runner_status"] != "SCORE_READY" for row in runner)
    shortcuts_enforced = all(row["status"] == "ENFORCED" for row in anti_shortcut)
    nonclaim = all_nonclaim(tables_for_nonclaim)
    formal_clean = len(generated_inside_formalization()) == 0
    next_is_1330 = next_target[0]["target_file"].startswith("1330-")

    validations = [
        validation_row(
            "VAL1329_0_sources_exist",
            "registered local source paths exist and anchors are found",
            source_anchor_count == len(source_register),
            f"{source_anchor_count}/{len(source_register)} source anchors found",
        ),
        validation_row(
            "VAL1329_1_raw_candidate_schema",
            "raw electron candidate file exists with 1233 schema fields",
            raw_exists and raw_schema_ok,
            f"raw_path={RAW_CANDIDATE_PATH};raw_rows={len(raw_rows)}",
        ),
        validation_row(
            "VAL1329_2_numeric_rows",
            "electron fraction rows and delta are finite numeric dry-run values",
            raw_numeric_ok and dryrun_numeric_ok,
            f"TA6V={by_material['TA6V']['fraction_value']};PtRh10={by_material['PtRh10']['fraction_value']};delta={delta_rows[0]['delta_fraction']}",
        ),
        validation_row(
            "VAL1329_3_raw_rows_nonclaim",
            "raw candidate rows remain valid_for_claim=false",
            raw_nonclaim,
            "raw electron candidate rows are schema-valid but nonclaim",
        ),
        validation_row(
            "VAL1329_4_one_component_only",
            "dry-run is explicitly electron component only",
            one_component_only,
            "non-electron source components remain unresolved",
        ),
        validation_row(
            "VAL1329_5_DD_demoted",
            "DD basis remains external comparator only",
            all(row["status"].startswith(("DEMOTED", "KEEP")) for row in dd_demotion),
            ";".join(f"{row['demotion_id']}={row['status']}" for row in dd_demotion),
        ),
        validation_row(
            "VAL1329_6_runner_not_scoreable",
            "Delta_w and WEP runners are not score-ready",
            runner_not_scoreable,
            ";".join(f"{row['runner_id']}={row['runner_status']}" for row in runner),
        ),
        validation_row(
            "VAL1329_7_shortcuts_enforced",
            "anti-shortcut gates are enforced",
            shortcuts_enforced,
            ";".join(row["gate_id"] for row in anti_shortcut),
        ),
        validation_row(
            "VAL1329_8_nonclaim_policy",
            "all generated rows remain nonclaim",
            nonclaim,
            "valid_for_claim=false and claim_allowed=false where present",
        ),
        validation_row(
            "VAL1329_9_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            formal_clean,
            f"formalization_generated_output_count={len(generated_inside_formalization())}",
        ),
        validation_row(
            "VAL1329_10_next_target_1330",
            "next target routes to audited electron extractor or parent DD map gate",
            next_is_1330,
            str(next_target[0]["target_file"]),
        ),
    ]
    validations.append(
        validation_row(
            "VAL1329_11_overall",
            "overall 1329 validation",
            all(row["status"] == "PASS" for row in validations),
            "1329 produces the first numeric nonclaim electron component dry-run and refuses WEP/local-GR promotion",
        )
    )

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(INPUT_CONSTANTS_PATH, input_constants)
    write_csv(ELEMENT_CONTRIB_PATH, element_contrib)
    write_csv(ELECTRON_DRYRUN_PATH, dryrun_rows)
    write_csv(DELTA_PATH, delta_rows)
    write_csv(ACCEPTANCE_PATH, acceptance)
    write_csv(DD_DEMOTION_PATH, dd_demotion)
    write_csv(RUNNER_PATH, runner)
    write_csv(ANTI_SHORTCUT_PATH, anti_shortcut)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# {TITLE}

**Current verdict:** 1329 gets the first real numeric component dry-run into the source pipeline: the electron rest-mass fraction contrast between TA6V and PtRh10 is finite, schema-shaped, and nonclaim. This is progress, not a WEP or local-GR pass.

**Main progress:** the electron component is now concrete enough to inspect. The dry-run gives `Delta F_e(TA6V-PtRh10) = {delta_rows[0]["delta_fraction"]}` with a deliberately conservative nonclaim envelope `{delta_rows[0]["delta_uncertainty"]}`.

**Decision:** keep the calculation as a partial component row. The full `Delta_w_TiPt` branch still needs light-quark, QCD/gluon, EM/Coulomb, nuclear surface, measure/readout, and the parent basis map.

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Electron Fraction Input Constants
{markdown_table(input_constants, ["constant_id", "symbol", "value", "units", "source", "status", "valid_for_claim", "claim_allowed"])}

## Element Contributions
{markdown_table(element_contrib, ["contribution_id", "material_id", "element", "mass_fraction", "Z", "A_microscope_context", "A_nist_standard_weight", "microscope_A_contribution", "nist_weight_contribution", "source", "status", "valid_for_claim", "claim_allowed"])}

## Electron Fraction Dry-Run Rows
{markdown_table(dryrun_rows, ["row_id", "material_id", "component_id", "fraction_value", "fraction_uncertainty", "basis_convention", "source_path_or_url", "extraction_method", "microscope_A_crosscheck_fraction", "uncertainty_model", "status", "valid_for_claim", "claim_allowed"])}

## Raw Candidate File
Schema-shaped nonclaim candidate written to:

`{RAW_CANDIDATE_PATH}`

{markdown_table(raw_candidate_rows, ["row_id", "material_id", "component_id", "fraction_value", "fraction_uncertainty", "basis_convention", "source_path_or_url", "extraction_method", "valid_for_claim"])}

## Electron Delta Vector
{markdown_table(delta_rows, ["delta_id", "component_id", "left_material", "right_material", "delta_fraction", "abs_delta_fraction", "delta_uncertainty", "interpretation", "status", "valid_for_claim", "claim_allowed"])}

## Acceptance Ledger
{markdown_table(acceptance, ["acceptance_id", "target", "status", "details", "blocks_claim", "valid_for_claim", "claim_allowed"])}

## DD Basis Map Demotion Ledger
{markdown_table(dd_demotion, ["demotion_id", "object", "status", "reason", "needed_for_promotion", "valid_for_claim", "claim_allowed"])}

## Delta-w Runner Update
{markdown_table(runner, ["runner_id", "target", "input_status", "runner_status", "reason", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])}

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

    print(f"Wrote {DOC_PATH}")
    print(f"Wrote validation {VALIDATION_PATH}")
    print(f"Wrote raw nonclaim electron candidate {RAW_CANDIDATE_PATH}")


if __name__ == "__main__":
    main()
