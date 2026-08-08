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
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv"
DOC = ROOT / "1080-Y5-R10-finite-WEP-source-vector-and-material-tensor-acquisition-pack.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1080-finite-WEP-source-vector-and-material-tensor-acquisition-pack" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_R10_1080_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1080_WEP_BOUND_IMPORT.csv"


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


def local_bound_row(row_id: str) -> dict[str, str]:
    for row in read_csv(LOCAL_BOUNDS):
        if row.get("row_id") == row_id:
            return row
    raise ValueError(f"missing local bound row {row_id}")


def split_reference(reference: str) -> tuple[str, str]:
    parts = [part.strip() for part in reference.split(";")]
    url = next((part for part in parts if part.startswith("http")), "")
    doi = next((part.replace("doi:", "").strip() for part in parts if part.lower().startswith("doi:")), "")
    return url, doi


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1080_0_1079_next", "source-intake/mts_residuals/P8_Y5_R10_1079_NEXT_TARGET.csv", "1080-Y5-R10-finite-WEP-source-vector-and-material-tensor-acquisition-pack.md", "1079 handoff."),
        ("SRC1080_1_1079_validation", "source-intake/mts_residuals/P8_Y5_BRR545_1079_VALIDATION.csv", "V1079_SUMMARY", "1079 validation summary."),
        ("SRC1080_2_1079_contract", "source-intake/mts_residuals/P8_Y5_R10_1079_FINITE_WEP_SOURCE_VECTOR_CONTRACT.csv", "FSV1079_3_source_vector", "finite WEP contract."),
        ("SRC1080_3_1079_vector", "source-intake/mts_residuals/P8_Y5_R10_1079_FINITE_VECTOR_TEMPLATE_NONCLAIM.csv", "VT1079_0_R_source_Earth", "finite vector template."),
        ("SRC1080_4_1079_material", "source-intake/mts_residuals/P8_Y5_R10_1079_MATERIAL_TENSOR_CONTRACT.csv", "MTC1079_2_response_map", "material tensor contract."),
        ("SRC1080_5_1061_material_convention", "source-intake/mts_residuals/P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv", "MCON1061_0_test_pair", "MICROSCOPE material convention."),
        ("SRC1080_6_1053_charge_matrix", "source-intake/mts_residuals/P8_Y5_R10_1053_WEP_COMPOSITION_CHARGE_MATRIX.csv", "WCM1053_6", "smoke composition charge matrix."),
        ("SRC1080_7_1052_projection", "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv", "AWP1052_0_alpha_Coulomb", "WEP alpha/surface projection thresholds."),
        ("SRC1080_8_1075_tau_shape", "source-intake/mts_residuals/P8_Y5_R10_1075_TAU_SHAPE_STATUS.csv", "TAUSHAPE1075_2_physics_tau", "surrogate readout status."),
        ("SRC1080_9_local_bounds", "source-intake/local_bounds/local_bound_claims.csv", "R1_WEP_source_charge", "MICROSCOPE WEP bound row."),
    ]
    rows: list[dict[str, str]] = []
    for source_id, relative_path, needle, note in specs:
        path = source_path(relative_path)
        exists = path.exists()
        needle_found = exists and needle in read_text(path)
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


def web_source_rows() -> list[dict[str, str]]:
    return [
        {
            "web_source_id": "WEB1080_0_MICROSCOPE_SF2A_2023",
            "role": "MICROSCOPE test-mass composition and measurement model",
            "source_url": "https://inspirehep.net/files/9a51796b3d7d940b16bd170876e35e4e",
            "source_title": "The MICROSCOPE space mission to test the Equivalence Principle",
            "evidence_used": "PtRh10 and TA6V mass-fraction composition; SUEP/SUREF role; differential acceleration/readout equation with gx, gz, Sxx, Sxz; final Ti/Pt result context",
            "extraction_status": "SOURCE_IDENTIFIED_AND_SUMMARIZED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "web_source_id": "WEB1080_1_DAMOUR_DONOGHUE_2010",
            "role": "external phenomenological material-charge basis",
            "source_url": "https://arxiv.org/abs/1007.2792",
            "source_title": "Equivalence Principle Violations and Couplings of a Light Dilaton",
            "evidence_used": "dilaton-like composition-charge framework used by existing 1053 smoke matrix",
            "extraction_status": "SOURCE_IDENTIFIED_FOR_PHENOMENOLOGICAL_BASIS_ONLY",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "web_source_id": "WEB1080_2_MCDONOUGH_SUN_1995",
            "role": "Earth/source composition reference candidate",
            "source_url": "https://earthref.org/ERR/n%3A3%2Cb%3Aaaaa0000003tab05/",
            "source_title": "McDonough and Sun 1995, Composition of the Earth",
            "evidence_used": "bulk Earth composition reference and DOI for source-vector acquisition",
            "extraction_status": "REFERENCE_IDENTIFIED_NOT_VECTORIZED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "web_source_id": "WEB1080_3_MICROSCOPE_RESULTS_2023",
            "role": "official analysis/readout/data-portal context",
            "source_url": "https://moriond.in2p3.fr/2023/Gravitation/transparencies/06_friday/01_morning/02_metris.pdf",
            "source_title": "Analysis and results from MICROSCOPE",
            "evidence_used": "operational measurement model, segment/session context, 4 Hz accelerations, CMSM data portal pointer",
            "extraction_status": "SOURCE_IDENTIFIED_ARRAYS_NOT_IMPORTED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def material_composition_rows() -> list[dict[str, str]]:
    return [
        {
            "material_id": "MAT1080_0_PtRh10_MICROSCOPE",
            "object": "PtRh10",
            "mass_fraction_or_composition": "Pt=0.90;Rh=0.10",
            "atomic_context": "Pt(A=195.1,Z=78);Rh(A=102.9,Z=45)",
            "source": "WEB1080_0_MICROSCOPE_SF2A_2023",
            "mapped_basis": "MICROSCOPE_COMPOSITION_CONTEXT_ONLY",
            "numeric_components": "composition_context_numeric",
            "status": "SOURCE_BACKED_COMPOSITION_CONTEXT",
            "missing_for_claim": "parent response basis and full material tensor",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "material_id": "MAT1080_1_TA6V_MICROSCOPE",
            "object": "TA6V",
            "mass_fraction_or_composition": "Ti=0.90;Al=0.06;V=0.04",
            "atomic_context": "Ti(A=47.9,Z=22);Al(A=27.0,Z=13);V(A=50.9,Z=23)",
            "source": "WEB1080_0_MICROSCOPE_SF2A_2023",
            "mapped_basis": "MICROSCOPE_COMPOSITION_CONTEXT_ONLY",
            "numeric_components": "composition_context_numeric",
            "status": "SOURCE_BACKED_COMPOSITION_CONTEXT",
            "missing_for_claim": "parent response basis and full material tensor",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "material_id": "MAT1080_2_delta_alpha_smoke",
            "object": "R_TA6V_minus_PtRh10 alpha/Coulomb smoke component",
            "mass_fraction_or_composition": "computed from 1053 smoke matrix",
            "atomic_context": "Damour-Donoghue alpha/Coulomb smoke formula",
            "source": "P8_Y5_R10_1053_WEP_COMPOSITION_CHARGE_MATRIX.csv:WCM1053_4",
            "mapped_basis": "DD_ALPHA_COULOMB_EXTERNAL_PHENOMENOLOGICAL",
            "numeric_components": "Delta_Q_alpha_Coulomb=-1.989808886825e-03;abs=1.989808886825e-03",
            "status": "SMOKE_NUMERIC_NOT_FULL_TENSOR",
            "missing_for_claim": "MTS parent basis; source vector; tau/readout; coefficient owner",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "material_id": "MAT1080_3_delta_surface_smoke",
            "object": "R_TA6V_minus_PtRh10 surface/binding smoke component",
            "mass_fraction_or_composition": "computed from 1053 smoke matrix",
            "atomic_context": "Damour-Donoghue simplified surface/binding smoke formula",
            "source": "P8_Y5_R10_1053_WEP_COMPOSITION_CHARGE_MATRIX.csv:WCM1053_5",
            "mapped_basis": "DD_SURFACE_BINDING_EXTERNAL_PHENOMENOLOGICAL",
            "numeric_components": "Delta_Q_surface_binding=-3.306456347405e-03;abs=3.306456347405e-03",
            "status": "SMOKE_NUMERIC_NOT_FULL_TENSOR",
            "missing_for_claim": "MTS parent basis; source vector; tau/readout; coefficient owner",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "material_id": "MAT1080_4_full_tensor_upgrade",
            "object": "R_TA6V_minus_PtRh10 full material tensor",
            "mass_fraction_or_composition": "requires all relevant mass, EM, binding, nuclear, and parent-source sensitivities",
            "atomic_context": "not reducible to two smoke components unless parent basis selects them",
            "source": "P8_Y5_R10_1053_WEP_COMPOSITION_CHARGE_MATRIX.csv:WCM1053_6",
            "mapped_basis": "MISSING_MTS_PARENT_BASIS",
            "numeric_components": "MISSING_FULL_MATERIAL_TENSOR",
            "status": "MISSING_FOR_CLAIM",
            "missing_for_claim": "parent basis and full response map",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def earth_source_rows() -> list[dict[str, str]]:
    return [
        {
            "source_vector_id": "EARTH1080_0_source_role",
            "object": "R_source^Earth",
            "candidate_source": "WEB1080_0_MICROSCOPE_SF2A_2023",
            "basis": "observed MICROSCOPE source leg",
            "candidate_components": "Earth is the source body for the WEP signal",
            "status": "SOURCE_ROLE_IDENTIFIED",
            "missing_for_claim": "composition/profile vector in the same parent basis as R_material and C_parent",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "source_vector_id": "EARTH1080_1_bulk_composition_reference",
            "object": "R_source^Earth",
            "candidate_source": "WEB1080_2_MCDONOUGH_SUN_1995",
            "basis": "bulk Earth composition reference candidate",
            "candidate_components": "reference identified but not transformed into MTS response components",
            "status": "REFERENCE_IDENTIFIED_NOT_VECTORIZED",
            "missing_for_claim": "extract elemental/geophysical composition table and map to parent/source basis",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "source_vector_id": "EARTH1080_2_parent_basis_block",
            "object": "R_source^Earth",
            "candidate_source": "1079 finite source-vector contract",
            "basis": "MISSING_MTS_PARENT_BASIS",
            "candidate_components": "MISSING_SOURCE_VECTOR",
            "status": "MISSING_FOR_CLAIM",
            "missing_for_claim": "MTS must choose/derive the basis before Earth composition becomes a source vector",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "source_vector_id": "EARTH1080_3_common_mode_alternative",
            "object": "R_source^Earth common-mode theorem",
            "candidate_source": "Hilbert-current subtheorem plus source-common-mode route",
            "basis": "THEOREM_ROUTE",
            "candidate_components": "source leg may cancel only if parent proves universal common mode",
            "status": "THEOREM_ROUTE_NOT_SIGNED",
            "missing_for_claim": "parent theorem that source response is universal/common-mode without measured-G absorption",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def c_parent_rows() -> list[dict[str, str]]:
    return [
        {
            "coefficient_id": "CP1080_0_definition",
            "object": "C_parent",
            "definition": "parent finite WEP coupling coefficient multiplying source and test response vectors",
            "candidate_basis": "MISSING_MTS_PARENT_BASIS",
            "value": "MISSING_PARENT_COEFFICIENT",
            "units": "basis-dependent",
            "status": "MISSING_FOR_CLAIM",
            "missing_for_claim": "derive from parent action or explicitly source as finite phenomenological coefficient",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "coefficient_id": "CP1080_1_current_owner_partial",
            "object": "C_parent",
            "definition": "Hilbert-current owner fixes post-variation source definition but not coupling magnitude",
            "candidate_basis": "current-owner subtheorem",
            "value": "NO_NUMERIC_COEFFICIENT_SUPPLIED",
            "units": "not_applicable",
            "status": "PARTIAL_THEOREM_NOT_COEFFICIENT",
            "missing_for_claim": "pre-variation action/species weights or finite coefficient still unresolved",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "coefficient_id": "CP1080_2_DD_basis_external",
            "object": "C_parent in Damour-Donoghue basis",
            "definition": "external phenomenological coefficients can be bounded but are not MTS-derived parent coefficients",
            "candidate_basis": "DD_ALPHA_SURFACE_EXTERNAL",
            "value": "MISSING_DD_COEFFICIENT_VECTOR",
            "units": "dimensionless per selected charge convention",
            "status": "PHENOMENOLOGICAL_BASIS_AVAILABLE_NONCLAIM",
            "missing_for_claim": "MTS-to-DD basis map and coefficient derivation",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def readout_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "readout_id": "READ1080_0_measurement_equation",
            "object": "K_MICROSCOPE readout model",
            "source": "WEB1080_0_MICROSCOPE_SF2A_2023",
            "content": "projected differential acceleration model uses gx, gz, Sxx, Sxz, offsets, and polynomial drift terms",
            "status": "MODEL_STRUCTURE_SOURCE_BACKED",
            "missing_for_claim": "official arrays/masks or validated reconstruction in the same product convention",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "readout_id": "READ1080_1_CMSM_portal",
            "object": "official CMSM data portal",
            "source": "WEB1080_3_MICROSCOPE_RESULTS_2023",
            "content": "data/documentation portal identified; arrays not imported by this checkpoint",
            "status": "OFFICIAL_PORTAL_IDENTIFIED_ARRAYS_NOT_IMPORTED",
            "missing_for_claim": "download/import gx,gz,Sxx,Sxz/masks or user-assisted official export",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "readout_id": "READ1080_2_surrogate_matrix",
            "object": "surrogate K_MICROSCOPE",
            "source": "P8_Y5_R10_1075_TAU_SHAPE_STATUS.csv:TAUSHAPE1075_0_matrix_available",
            "content": "surrogate design matrix exists and recovered synthetic tau-shape coefficients",
            "status": "SURROGATE_AVAILABLE_NONCLAIM",
            "missing_for_claim": "official arrays and parent material/source map",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "readout_id": "READ1080_3_physical_tau",
            "object": "physical tau_WEP",
            "source": "P8_Y5_R10_1075_TAU_SHAPE_STATUS.csv:TAUSHAPE1075_2_physics_tau",
            "content": "physical tau not acquired",
            "status": "NOT_ACQUIRED",
            "missing_for_claim": "official arrays plus C_parent/R_source/R_material product basis",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def finite_input_pack_rows() -> list[dict[str, str]]:
    return [
        {
            "input_id": "FIP1080_0_product_formula",
            "object": "P_WEP finite product",
            "candidate_value": "P_WEP = sum_I C_parent^I * R_source_I^Earth * DeltaR_material_I projected by K_MICROSCOPE",
            "units": "dimensionless eta convention",
            "status": "FORMULA_READY_NONCLAIM",
            "source_or_basis": "1079 finite WEP contract",
            "blocks_claim": "all numeric input rows still required",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "FIP1080_1_C_parent",
            "object": "C_parent",
            "candidate_value": "MISSING_PARENT_COEFFICIENT",
            "units": "basis-dependent",
            "status": "MISSING_FOR_CLAIM",
            "source_or_basis": "CP1080 rows",
            "blocks_claim": "no MTS coupling magnitude or basis owner",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "FIP1080_2_R_source",
            "object": "R_source^Earth",
            "candidate_value": "REFERENCE_IDENTIFIED_NOT_VECTORIZED",
            "units": "basis-dependent",
            "status": "MISSING_FOR_CLAIM",
            "source_or_basis": "McDonough-Sun candidate plus MICROSCOPE Earth-source role",
            "blocks_claim": "no same-basis Earth source vector",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "FIP1080_3_R_material",
            "object": "R_TA6V - R_PtRh10",
            "candidate_value": "DD smoke delta alpha/surface rows available; full tensor missing",
            "units": "basis-dependent",
            "status": "PARTIAL_SMOKE_NUMERIC_NONCLAIM",
            "source_or_basis": "WCM1053_4;WCM1053_5",
            "blocks_claim": "external smoke basis not parent MTS basis; full tensor missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "FIP1080_4_K_readout",
            "object": "K_MICROSCOPE",
            "candidate_value": "surrogate available; official portal identified; arrays not imported",
            "units": "eta projection convention",
            "status": "SURROGATE_ONLY_NONCLAIM",
            "source_or_basis": "READ1080 rows",
            "blocks_claim": "official arrays or validated reconstruction required",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def product_prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1080_0_WEP_finite_input_pack_nonclaim",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_C_PARENT_R_SOURCE_R_MATERIAL_K_READOUT_NUMERIC_PRODUCT",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1080_FINITE_WEP_INPUT_PACK_NONCLAIM.csv",
            "inputs_present": "MICROSCOPE composition context; DD smoke material deltas; Earth composition reference; readout model source; bound row",
            "required_inputs": "numeric C_parent; same-basis numeric R_source^Earth; full R_TA6V_minus_PtRh10 tensor; official/validated K_MICROSCOPE",
            "derivation_status": "ACQUISITION_PACK_READY_PRODUCT_MISSING",
            "valid_for_claim": "false",
            "notes": "all candidate rows are acquisition scaffolding, not an MTS prediction",
        }
    ]


def bound_rows() -> list[dict[str, str]]:
    row = local_bound_row("R1_WEP_source_charge")
    url, doi = split_reference(row.get("reference_path_or_url", ""))
    return [
        {
            "bound_id": "BOUND1080_0_MICROSCOPE_WEP_source_charge",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "bound_value": row["upper_bound"],
            "bound_units": row["units"],
            "bound_source": url,
            "source_row": f"{row['dataset_id']}:{row['row_id']};doi:{doi}",
            "bound_type": "upper_abs_WEP_proxy_bound",
            "valid_for_claim": "true",
            "notes": "source-backed numeric bound only; prediction remains invalid",
        }
    ]


def product_status_rows(status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "runner_id": "APR1080_0_WEP_finite_input_pack_product_stub",
            "prediction_rows": str(status.get("prediction_rows", "")),
            "bound_rows": str(status.get("bound_rows", "")),
            "valid_prediction_rows": str(status.get("valid_prediction_rows", "")),
            "valid_bound_rows": str(status.get("valid_bound_rows", "")),
            "comparison_rows": str(status.get("comparison_rows", "")),
            "passed_rows": str(status.get("passed_rows", "")),
            "claim_allowed": str(status.get("claim_allowed", "")).lower(),
            "expected_result": "reject acquisition-pack rows until same-basis numeric product exists",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def claim_gate_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1080_0_source_references",
            "claim_component": "external source references",
            "gate_pass": "true",
            "claim_allowed": "false",
            "reason": "web/local source references are identified, but references are not same-basis MTS vectors",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1080_1_material_context",
            "claim_component": "MICROSCOPE material composition context",
            "gate_pass": "true",
            "claim_allowed": "false",
            "reason": "TA6V/PtRh10 compositions and smoke deltas are available, but full parent tensor is missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1080_2_source_vector",
            "claim_component": "R_source^Earth",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "Earth composition reference is not vectorized in MTS/DD basis",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1080_3_C_parent",
            "claim_component": "C_parent",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "parent coupling coefficient and basis owner are missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1080_4_readout",
            "claim_component": "K_MICROSCOPE",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "official arrays not imported; surrogate remains nonclaim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1080_5_product_runner",
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
            "decision_id": "DEC1080_0_pack_value",
            "decision": "finite WEP acquisition pack is now source-anchored but not score-ready",
            "because": "MICROSCOPE material/readout references, DD material charge basis, and Earth composition reference are named",
            "next_action": "do not claim; instantiate a basis only as a nonclaim smoke runner",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1080_1_main_blocker",
            "decision": "main missing object is same-basis ownership",
            "because": "C_parent, R_source, R_material, and K_readout must share one basis/convention",
            "next_action": "either derive MTS parent basis or explicitly adopt DD basis as external nonclaim comparator",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1080_2_next_route",
            "decision": "build a DD-basis finite WEP smoke runner as the next practical test scaffold",
            "because": "it can test pipeline algebra without pretending it is MTS-derived",
            "next_action": "1081 should instantiate DD alpha/surface rows, source proxy policy, and runner refusal gates",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1080_0_1081",
            "next_target": "1081-Y5-R10-DD-basis-finite-WEP-smoke-runner-or-parent-basis-derivation.md",
            "objective": "try to derive the MTS parent WEP basis; if it remains unsigned, instantiate a Damour-Donoghue alpha/surface finite-WEP smoke runner with explicit source-proxy policy and strict nonclaim gates.",
            "include": "MTS parent basis attempt; DD alpha/surface basis; Earth source proxy policy; TA6V/PtRh10 smoke deltas; MICROSCOPE readout gate; product runner refusal",
            "exclude": "MTS claim from DD basis; toy vector as evidence; measured-G absorption; tau=1; public claim; GitHub; formalization edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def csv_rows_parse(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
    except csv.Error:
        return False
    return True


def validate_outputs(
    outputs: dict[str, Path],
    source_rows: list[dict[str, str]],
    web_rows: list[dict[str, str]],
    material_rows: list[dict[str, str]],
    earth_rows: list[dict[str, str]],
    c_parent_rows_: list[dict[str, str]],
    readout_rows: list[dict[str, str]],
    input_pack_rows: list[dict[str, str]],
    prediction_rows: list[dict[str, str]],
    bound_rows_: list[dict[str, str]],
    product_status: dict[str, Any],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V1080_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in source_rows), "all cited local source paths and needles are present"))
    checks.append(("V1080_1_web_sources_identified", len(web_rows) == 4 and all(row["source_url"].startswith("https://") for row in web_rows), "web source candidates are recorded with URLs"))
    checks.append(("V1080_2_material_context", any(row["material_id"] == "MAT1080_0_PtRh10_MICROSCOPE" and row["status"] == "SOURCE_BACKED_COMPOSITION_CONTEXT" for row in material_rows) and any(row["material_id"] == "MAT1080_1_TA6V_MICROSCOPE" and row["status"] == "SOURCE_BACKED_COMPOSITION_CONTEXT" for row in material_rows), "MICROSCOPE material compositions are recorded"))
    checks.append(("V1080_3_material_smoke_nonclaim", any(row["material_id"] == "MAT1080_2_delta_alpha_smoke" and row["status"] == "SMOKE_NUMERIC_NOT_FULL_TENSOR" for row in material_rows) and any(row["material_id"] == "MAT1080_4_full_tensor_upgrade" and row["status"] == "MISSING_FOR_CLAIM" for row in material_rows), "material smoke rows remain nonclaim and full tensor is missing"))
    checks.append(("V1080_4_earth_source_not_vectorized", any(row["source_vector_id"] == "EARTH1080_1_bulk_composition_reference" and row["status"] == "REFERENCE_IDENTIFIED_NOT_VECTORIZED" for row in earth_rows) and any(row["source_vector_id"] == "EARTH1080_2_parent_basis_block" and row["status"] == "MISSING_FOR_CLAIM" for row in earth_rows), "Earth/source reference is identified but not vectorized"))
    checks.append(("V1080_5_C_parent_missing", any(row["coefficient_id"] == "CP1080_0_definition" and row["status"] == "MISSING_FOR_CLAIM" for row in c_parent_rows_), "C_parent remains missing"))
    checks.append(("V1080_6_readout_gate", any(row["readout_id"] == "READ1080_1_CMSM_portal" and row["status"] == "OFFICIAL_PORTAL_IDENTIFIED_ARRAYS_NOT_IMPORTED" for row in readout_rows) and any(row["readout_id"] == "READ1080_2_surrogate_matrix" and row["status"] == "SURROGATE_AVAILABLE_NONCLAIM" for row in readout_rows), "readout gate records official portal and surrogate nonclaim"))
    checks.append(("V1080_7_input_pack_nonclaim", len(input_pack_rows) == 5 and all(row["valid_for_claim"] == "false" for row in input_pack_rows), "finite input pack remains nonclaim"))
    checks.append(("V1080_8_prediction_nonclaim_missing", any("MISSING_C_PARENT_R_SOURCE" in row["product_value"] and row["valid_for_claim"] == "false" for row in prediction_rows), "prediction row remains missing same-basis numeric product"))
    checks.append(("V1080_9_bound_numeric", bool(bound_rows_) and float(bound_rows_[0]["bound_value"]) > 0 and bound_rows_[0]["valid_for_claim"] == "true", "bound import is positive numeric"))
    checks.append(("V1080_10_runner_refuses", product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False, "runner reports no valid prediction rows and claim false"))
    checks.append(("V1080_11_claim_gates_safe", all(row["claim_allowed"] == "false" for row in claim_rows), "all claim gates deny WEP/local-GR claim"))
    checks.append(("V1080_12_next_target", any(row["next_target"].startswith("1081-Y5-R10-DD-basis") for row in next_rows), "1081 handoff written"))
    generated_paths = list(outputs.values()) + [DOC]
    checks.append(("V1080_13_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in generated_paths), "all generated outputs are under post-checkpoint-work"))
    checks.append(("V1080_14_csv_parse", all(path.exists() and csv_rows_parse(path) for path in outputs.values() if path.suffix == ".csv" and path.name != "P8_Y5_BRR545_1080_VALIDATION.csv"), "all 1080 CSV outputs parse cleanly"))
    checks.append(("V1080_15_formalization_untouched", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains zero"))
    checks.append(("V1080_SUMMARY", True, "finite WEP acquisition pack source-anchored; same-basis C_parent/R_source/R_material/K_readout still missing; claim blocked"))
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
    web_rows: list[dict[str, str]],
    material_rows: list[dict[str, str]],
    earth_rows: list[dict[str, str]],
    c_parent_rows_: list[dict[str, str]],
    readout_rows: list[dict[str, str]],
    input_pack_rows: list[dict[str, str]],
    prediction_rows: list[dict[str, str]],
    bound_rows_: list[dict[str, str]],
    product_status_rows_: list[dict[str, str]],
    product_comparison_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1080 - Finite WEP source-vector and material-tensor acquisition pack",
            "",
            "## Current verdict",
            "1080 turns the finite WEP route from a vague missing-input complaint into a source-anchored acquisition pack. MICROSCOPE gives the TA6V/PtRh10 composition context and readout model, Damour-Donoghue supplies an external phenomenological alpha/surface charge basis already used by the smoke rows, and McDonough-Sun identifies the Earth-composition reference. This is not a claim-ready MTS product: the same-basis objects C_parent, R_source^Earth, full R_TA6V - R_PtRh10, and K_MICROSCOPE are still missing or nonclaim.",
            "",
            "## Local source register",
            md_table(source_rows, ["source_id", "relative_path", "exists", "needle_found", "note"]),
            "## Web/source candidate register",
            md_table(web_rows, ["web_source_id", "role", "source_url", "extraction_status"]),
            "## Material composition and tensor candidates",
            md_table(material_rows, ["material_id", "object", "mapped_basis", "numeric_components", "status", "missing_for_claim"]),
            "## Earth source-vector candidates",
            md_table(earth_rows, ["source_vector_id", "object", "basis", "status", "missing_for_claim"]),
            "## C_parent coefficient contract",
            md_table(c_parent_rows_, ["coefficient_id", "object", "candidate_basis", "value", "status", "missing_for_claim"]),
            "## MICROSCOPE readout gate",
            md_table(readout_rows, ["readout_id", "object", "status", "missing_for_claim"]),
            "## Finite WEP input pack",
            md_table(input_pack_rows, ["input_id", "object", "candidate_value", "status", "blocks_claim"]),
            "## Nonclaim product candidate",
            md_table(prediction_rows, ["prediction_id", "product_symbol", "product_value", "derivation_status", "valid_for_claim"]),
            "## Bound import",
            md_table(bound_rows_, ["bound_id", "product_symbol", "bound_value", "bound_units", "valid_for_claim"]),
            "## Product runner status",
            md_table(product_status_rows_, ["runner_id", "valid_prediction_rows", "valid_bound_rows", "claim_allowed", "expected_result"]),
            "## Product comparison rows",
            md_table(product_comparison_rows, ["comparison_id", "comparison_status", "pass_for_claim", "issues"]),
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
    web_rows = web_source_rows()
    material_rows = material_composition_rows()
    earth_rows = earth_source_rows()
    c_parent_rows_ = c_parent_rows()
    readout_rows = readout_gate_rows()
    input_pack_rows = finite_input_pack_rows()
    prediction_rows = product_prediction_rows()
    bound_rows_ = bound_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R10_1080_SOURCE_REGISTER.csv",
        "web_sources": OUT / "P8_Y5_R10_1080_WEB_SOURCE_CANDIDATE_REGISTER.csv",
        "material": OUT / "P8_Y5_R10_1080_MATERIAL_COMPOSITION_AND_TENSOR_CANDIDATES.csv",
        "earth_source": OUT / "P8_Y5_R10_1080_EARTH_SOURCE_VECTOR_CANDIDATES.csv",
        "c_parent": OUT / "P8_Y5_R10_1080_C_PARENT_COEFFICIENT_CONTRACT.csv",
        "readout": OUT / "P8_Y5_R10_1080_MICROSCOPE_READOUT_GATE.csv",
        "input_pack": OUT / "P8_Y5_R10_1080_FINITE_WEP_INPUT_PACK_NONCLAIM.csv",
        "prediction": PREDICTION_TEMPLATE,
        "bound": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_R10_1080_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_R10_1080_PRODUCT_COMPARISON_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_R10_1080_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1080_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1080_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1080_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["web_sources"], web_rows)
    write_csv(outputs["material"], material_rows)
    write_csv(outputs["earth_source"], earth_rows)
    write_csv(outputs["c_parent"], c_parent_rows_)
    write_csv(outputs["readout"], readout_rows)
    write_csv(outputs["input_pack"], input_pack_rows)
    write_csv(outputs["prediction"], prediction_rows, PRODUCT_REQUIRED_COLUMNS)
    write_csv(outputs["bound"], bound_rows_, BOUND_REQUIRED_COLUMNS)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next_target"], next_rows)

    product_result = run_product_runner(PREDICTION_TEMPLATE, BOUND_IMPORT, PRODUCT_RUN_DIR)
    product_status = product_result["status"]
    product_status_rows_ = product_status_rows(product_status)
    claim_rows = claim_gate_rows(product_status)

    write_csv(outputs["product_status"], product_status_rows_)
    write_csv(outputs["product_comparison"], product_result["comparisons"])
    write_csv(outputs["claim_gates"], claim_rows)

    remove_pycache()
    validation_rows = validate_outputs(
        outputs,
        source_rows,
        web_rows,
        material_rows,
        earth_rows,
        c_parent_rows_,
        readout_rows,
        input_pack_rows,
        prediction_rows,
        bound_rows_,
        product_status,
        claim_rows,
        next_rows,
    )
    write_csv(outputs["validation"], validation_rows)
    write_doc(
        source_rows,
        web_rows,
        material_rows,
        earth_rows,
        c_parent_rows_,
        readout_rows,
        input_pack_rows,
        prediction_rows,
        bound_rows_,
        product_status_rows_,
        product_result["comparisons"],
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
