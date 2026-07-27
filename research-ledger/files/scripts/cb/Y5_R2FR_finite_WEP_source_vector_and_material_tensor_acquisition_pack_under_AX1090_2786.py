from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_STARTED_UTC = datetime.now(timezone.utc)
ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
WORK = ROOT / "post-checkpoint-work"
MTS = WORK / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = WORK / "source-intake" / "local_bounds"
RAB_QUEUE = WORK / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = WORK / "source-intake" / "beta-source" / "docs"
MICROSCOPE_DIR = WORK / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SCRIPTS = WORK / "scripts"
FORMALIZATION = ROOT / "formalization-workbench"
DOC = WORK / "2786-Y5-R2FR-finite-WEP-source-vector-and-material-tensor-acquisition-pack-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2786_SOURCE_REGISTER.csv",
    "web_sources": MTS / "P8_Y5_R2FR_2786_WEB_SOURCE_CANDIDATE_REGISTER.csv",
    "earth_source": MTS / "P8_Y5_R2FR_2786_EARTH_SOURCE_VECTOR_CANDIDATES.csv",
    "material": MTS / "P8_Y5_R2FR_2786_MATERIAL_COMPOSITION_AND_TENSOR_CANDIDATES.csv",
    "c_parent": MTS / "P8_Y5_R2FR_2786_C_PARENT_COEFFICIENT_CONTRACT.csv",
    "readout": MTS / "P8_Y5_R2FR_2786_MICROSCOPE_READOUT_GATE.csv",
    "basis_gate": MTS / "P8_Y5_R2FR_2786_SAME_BASIS_CLOSURE_GATE.csv",
    "acquisition": MTS / "P8_Y5_R2FR_2786_ACQUISITION_PRIORITY_LEDGER.csv",
    "input_pack": MTS / "P8_Y5_R2FR_2786_FINITE_WEP_INPUT_PACK_NONCLAIM.csv",
    "candidate": MTS / "P8_Y5_R2FR_2786_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv",
    "bounds": MTS / "P8_Y5_R2FR_2786_WEP_BOUND_IMPORT.csv",
    "runner": MTS / "P8_Y5_R2FR_2786_PRODUCT_RUNNER_STATUS.csv",
    "comparisons": MTS / "P8_Y5_R2FR_2786_PRODUCT_COMPARISON_ROWS.csv",
    "gates": MTS / "P8_Y5_R2FR_2786_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2786_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2786_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2786_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2786_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "input_pack_queue": RAB_QUEUE / "JR2786_FINITE_WEP_INPUT_PACK_NONCLAIM.csv",
    "earth_queue": RAB_QUEUE / "JR2786_EARTH_SOURCE_VECTOR_ACQUISITION_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "MICROSCOPE_FINITE_WEP_INPUT_PACK_2786_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_finite_wep_input_pack_2786_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2786_PARENT_WEP_BASIS_NEXT.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def find_row(path: Path, key: str, value: str) -> dict[str, str]:
    for row in read_csv_rows(path):
        if row.get(key) == value:
            return row
    return {}


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["valid_for_claim"] = False
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def csv_row_count(path: Path) -> int:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        cells = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def is_numeric(value: Any) -> bool:
    try:
        float(str(value))
    except (TypeError, ValueError):
        return False
    return True


def has_missing_marker(row: dict[str, Any]) -> bool:
    return "MISSING" in " ".join(str(value) for value in row.values()).upper()


def trueish(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def source_row(row_id: str, source_key: str, path: Path, needle: str, role: str) -> dict[str, Any]:
    text = read_text(path)
    exists = path.exists()
    return nonclaim({
        "row_id": row_id,
        "source_key": source_key,
        "source_path": str(path),
        "exists": exists,
        "needle": needle,
        "needle_found": exists and needle in text,
        "source_role": role,
    })


def get_local_bound(row_id: str) -> dict[str, str]:
    for row in read_csv_rows(LOCAL_BOUNDS / "local_bound_claims.csv"):
        if row.get("row_id") == row_id:
            return row
    return {}


def build_sources() -> list[dict[str, Any]]:
    specs = [
        ("SRC2786_00_2785_next", "2785_next", MTS / "P8_Y5_R2FR_2785_NEXT_TARGET.csv", "NEXT2785_0_2786", "current handoff into finite WEP acquisition pack"),
        ("SRC2786_01_2785_validation", "2785_validation", MTS / "P8_Y5_BRR545_2785_VALIDATION.csv", "VAL2785_OVERALL", "2785 validation baseline"),
        ("SRC2786_02_2785_narrow", "2785_narrow", MTS / "P8_Y5_R2FR_2785_NARROW_CURRENT_OWNER_THEOREM_ATTEMPT.csv", "NCO2785_6_verdict", "narrow current-owner partial verdict"),
        ("SRC2786_03_2785_contract", "2785_contract", MTS / "P8_Y5_R2FR_2785_FINITE_WEP_SOURCE_VECTOR_CONTRACT.csv", "FWSC2785_0_formula", "finite WEP source-vector contract"),
        ("SRC2786_04_2785_material_contract", "2785_material_contract", MTS / "P8_Y5_R2FR_2785_MATERIAL_TENSOR_CONTRACT.csv", "MTC2785_5_claim_gate", "material tensor contract"),
        ("SRC2786_05_1080_web", "1080_web", MTS / "P8_Y5_R10_1080_WEB_SOURCE_CANDIDATE_REGISTER.csv", "WEB1080_0_MICROSCOPE_SF2A_2023", "R10 web/source candidate register"),
        ("SRC2786_06_1080_earth", "1080_earth", MTS / "P8_Y5_R10_1080_EARTH_SOURCE_VECTOR_CANDIDATES.csv", "EARTH1080_1_bulk_composition_reference", "R10 Earth/source vector acquisition status"),
        ("SRC2786_07_1080_material", "1080_material", MTS / "P8_Y5_R10_1080_MATERIAL_COMPOSITION_AND_TENSOR_CANDIDATES.csv", "MAT1080_4_full_tensor_upgrade", "R10 material tensor acquisition status"),
        ("SRC2786_08_1080_cparent", "1080_cparent", MTS / "P8_Y5_R10_1080_C_PARENT_COEFFICIENT_CONTRACT.csv", "CP1080_0_definition", "R10 C_parent contract"),
        ("SRC2786_09_1080_readout", "1080_readout", MTS / "P8_Y5_R10_1080_MICROSCOPE_READOUT_GATE.csv", "READ1080_3_physical_tau", "R10 MICROSCOPE readout gate"),
        ("SRC2786_10_1081_basis", "1081_basis", MTS / "P8_Y5_R10_1081_PARENT_WEP_BASIS_DERIVATION_ATTEMPT.csv", "PB1081_4_verdict", "R10 parent-basis derivation obstruction"),
        ("SRC2786_11_1081_dd_delta", "1081_dd_delta", MTS / "P8_Y5_R10_1081_DD_MATERIAL_DELTA_IMPORT.csv", "DDM1081_0_delta_alpha", "external DD smoke material deltas"),
        ("SRC2786_12_2781_tau_shape", "2781_tau_shape", MTS / "P8_Y5_R2FR_2781_TAU_SHAPE_STATUS.csv", "TAUSHAPE2781_2_physics_tau", "R2FR surrogate tau shape status"),
        ("SRC2786_13_2780_cmsm", "2780_cmsm", MTS / "P8_Y5_R2FR_2780_CMSM_EXPORT_INVENTORY_CHECK.csv", "INV2780_0_search_root", "R2FR official CMSM export check"),
        ("SRC2786_14_local_bounds", "local_bounds", LOCAL_BOUNDS / "local_bound_claims.csv", "R1_WEP_source_charge", "MICROSCOPE WEP bound row"),
    ]
    return [source_row(*spec) for spec in specs]


def build_web_sources() -> list[dict[str, Any]]:
    generated = ts()
    return [
        nonclaim({
            "web_source_id": "WEB2786_0_MICROSCOPE_SF2A_2023",
            "role": "MICROSCOPE test-mass composition and measurement model",
            "source_url": "https://inspirehep.net/files/9a51796b3d7d940b16bd170876e35e4e",
            "source_title": "The MICROSCOPE space mission to test the Equivalence Principle",
            "evidence_used": "PtRh10 and TA6V mass-fraction composition; SUEP/SUREF role; differential acceleration/readout equation with gx, gz, Sxx, Sxz; final Ti/Pt result context",
            "extraction_status": "SOURCE_IDENTIFIED_AND_SUMMARIZED_FROM_1080",
            "generated_utc": generated,
        }),
        nonclaim({
            "web_source_id": "WEB2786_1_DAMOUR_DONOGHUE_2010",
            "role": "external phenomenological material-charge basis",
            "source_url": "https://arxiv.org/abs/1007.2792",
            "source_title": "Equivalence Principle Violations and Couplings of a Light Dilaton",
            "evidence_used": "alpha/Coulomb and surface/binding smoke components already used by 1053/1081 comparator rows",
            "extraction_status": "SOURCE_IDENTIFIED_FOR_PHENOMENOLOGICAL_BASIS_ONLY",
            "generated_utc": generated,
        }),
        nonclaim({
            "web_source_id": "WEB2786_2_MCDONOUGH_SUN_1995",
            "role": "Earth/source composition reference candidate",
            "source_url": "https://earthref.org/ERR/n%3A3%2Cb%3Aaaaa0000003tab05/",
            "source_title": "McDonough and Sun 1995, Composition of the Earth",
            "evidence_used": "bulk Earth composition reference and DOI for source-vector acquisition",
            "extraction_status": "REFERENCE_IDENTIFIED_NOT_VECTORIZED",
            "generated_utc": generated,
        }),
        nonclaim({
            "web_source_id": "WEB2786_3_MICROSCOPE_RESULTS_2023",
            "role": "official analysis/readout/data-portal context",
            "source_url": "https://moriond.in2p3.fr/2023/Gravitation/transparencies/06_friday/01_morning/02_metris.pdf",
            "source_title": "Analysis and results from MICROSCOPE",
            "evidence_used": "operational measurement model, segment/session context, 4 Hz accelerations, CMSM data portal pointer",
            "extraction_status": "SOURCE_IDENTIFIED_ARRAYS_NOT_IMPORTED",
            "generated_utc": generated,
        }),
    ]


def build_earth_source_rows() -> list[dict[str, Any]]:
    generated = ts()
    return [
        nonclaim({
            "source_vector_id": "EARTH2786_0_source_role",
            "object": "R_source^Earth",
            "candidate_source": "WEB2786_0_MICROSCOPE_SF2A_2023",
            "basis": "observed MICROSCOPE source leg",
            "candidate_components": "Earth is the source body for the MICROSCOPE WEP signal",
            "status": "SOURCE_ROLE_IDENTIFIED",
            "missing_for_claim": "composition/profile vector in the same parent basis as R_material and C_parent",
            "generated_utc": generated,
        }),
        nonclaim({
            "source_vector_id": "EARTH2786_1_bulk_composition_reference",
            "object": "R_source^Earth",
            "candidate_source": "WEB2786_2_MCDONOUGH_SUN_1995",
            "basis": "bulk Earth composition reference candidate",
            "candidate_components": "reference identified but not transformed into MTS response components",
            "status": "REFERENCE_IDENTIFIED_NOT_VECTORIZED",
            "missing_for_claim": "extract elemental/geophysical composition table and map to parent/source basis",
            "generated_utc": generated,
        }),
        nonclaim({
            "source_vector_id": "EARTH2786_2_parent_basis_block",
            "object": "R_source^Earth",
            "candidate_source": "2785 finite source-vector contract",
            "basis": "MISSING_MTS_PARENT_BASIS",
            "candidate_components": "MISSING_SOURCE_VECTOR",
            "status": "MISSING_FOR_CLAIM",
            "missing_for_claim": "MTS must choose/derive the basis before Earth composition becomes a source vector",
            "generated_utc": generated,
        }),
        nonclaim({
            "source_vector_id": "EARTH2786_3_common_mode_alternative",
            "object": "R_source^Earth common-mode theorem",
            "candidate_source": "Hilbert-current subtheorem plus source-common-mode route",
            "basis": "THEOREM_ROUTE",
            "candidate_components": "source leg may cancel only if parent proves universal common mode",
            "status": "THEOREM_ROUTE_NOT_SIGNED",
            "missing_for_claim": "parent theorem that source response is universal/common-mode without measured-G absorption",
            "generated_utc": generated,
        }),
        nonclaim({
            "source_vector_id": "EARTH2786_4_acquisition_task",
            "object": "R_source^Earth acquisition task",
            "candidate_source": "WEB2786_2_MCDONOUGH_SUN_1995 plus parent basis target",
            "basis": "PENDING_PARENT_OR_DD_BASIS",
            "candidate_components": "extract composition vector only after basis owner is selected",
            "status": "ACTIONABLE_BUT_NONCLAIM",
            "missing_for_claim": "same-basis map into C_parent and DeltaR_material",
            "generated_utc": generated,
        }),
    ]


def build_material_rows() -> list[dict[str, Any]]:
    generated = ts()
    toy_delta = find_row(MTS / "P8_Y5_R2FR_2782_TOY_MATERIAL_VECTOR_FROM_651.csv", "material_vector_id", "MV2782_delta_TA6V_minus_PtRh10")
    dd_alpha = find_row(MTS / "P8_Y5_R10_1081_DD_MATERIAL_DELTA_IMPORT.csv", "delta_id", "DDM1081_0_delta_alpha")
    dd_surface = find_row(MTS / "P8_Y5_R10_1081_DD_MATERIAL_DELTA_IMPORT.csv", "delta_id", "DDM1081_1_delta_surface")
    toy_components = (
        f"Delta_q_Z_over_A_toy={toy_delta.get('q_Z_over_A_toy', 'MISSING')};"
        f"Delta_q_neutron_excess_toy={toy_delta.get('q_neutron_excess_toy', 'MISSING')}"
    )
    return [
        nonclaim({
            "material_id": "MAT2786_0_PtRh10_MICROSCOPE",
            "object": "PtRh10",
            "mass_fraction_or_composition": "Pt=0.90;Rh=0.10",
            "atomic_context": "Pt(A=195.1,Z=78);Rh(A=102.9,Z=45)",
            "source": "WEB2786_0_MICROSCOPE_SF2A_2023",
            "mapped_basis": "MICROSCOPE_COMPOSITION_CONTEXT_ONLY",
            "numeric_components": "composition_context_numeric",
            "status": "SOURCE_BACKED_COMPOSITION_CONTEXT",
            "missing_for_claim": "parent response basis and full material tensor",
            "generated_utc": generated,
        }),
        nonclaim({
            "material_id": "MAT2786_1_TA6V_MICROSCOPE",
            "object": "TA6V",
            "mass_fraction_or_composition": "Ti=0.90;Al=0.06;V=0.04",
            "atomic_context": "Ti(A=47.9,Z=22);Al(A=27.0,Z=13);V(A=50.9,Z=23)",
            "source": "WEB2786_0_MICROSCOPE_SF2A_2023",
            "mapped_basis": "MICROSCOPE_COMPOSITION_CONTEXT_ONLY",
            "numeric_components": "composition_context_numeric",
            "status": "SOURCE_BACKED_COMPOSITION_CONTEXT",
            "missing_for_claim": "parent response basis and full material tensor",
            "generated_utc": generated,
        }),
        nonclaim({
            "material_id": "MAT2786_2_R2FR_toy_delta",
            "object": "R_TA6V_minus_PtRh10 toy components",
            "mass_fraction_or_composition": "computed from 2782 nominal alloy toy rows",
            "atomic_context": "Z/A and neutron-excess toy basis only",
            "source": "P8_Y5_R2FR_2782_TOY_MATERIAL_VECTOR_FROM_651.csv:MV2782_delta_TA6V_minus_PtRh10",
            "mapped_basis": "TOY_Z_OVER_A_NEUTRON_EXCESS_NOT_PARENT",
            "numeric_components": toy_components,
            "status": "TOY_NUMERIC_NOT_CLAIM_BASIS",
            "missing_for_claim": "parent response basis; uncertainty; source vector; coefficient owner",
            "generated_utc": generated,
        }),
        nonclaim({
            "material_id": "MAT2786_3_delta_alpha_smoke",
            "object": "R_TA6V_minus_PtRh10 alpha/Coulomb smoke component",
            "mass_fraction_or_composition": "computed from 1053/1081 smoke matrix",
            "atomic_context": "Damour-Donoghue alpha/Coulomb smoke formula",
            "source": "P8_Y5_R10_1081_DD_MATERIAL_DELTA_IMPORT.csv:DDM1081_0_delta_alpha",
            "mapped_basis": "DD_ALPHA_COULOMB_EXTERNAL_PHENOMENOLOGICAL",
            "numeric_components": f"Delta_Q_alpha_Coulomb={dd_alpha.get('delta_value', 'MISSING')};abs={dd_alpha.get('delta_abs', 'MISSING')}",
            "status": "SMOKE_NUMERIC_NOT_FULL_TENSOR",
            "missing_for_claim": "MTS parent basis; source vector; tau/readout; coefficient owner",
            "generated_utc": generated,
        }),
        nonclaim({
            "material_id": "MAT2786_4_delta_surface_smoke",
            "object": "R_TA6V_minus_PtRh10 surface/binding smoke component",
            "mass_fraction_or_composition": "computed from 1053/1081 smoke matrix",
            "atomic_context": "Damour-Donoghue simplified surface/binding smoke formula",
            "source": "P8_Y5_R10_1081_DD_MATERIAL_DELTA_IMPORT.csv:DDM1081_1_delta_surface",
            "mapped_basis": "DD_SURFACE_BINDING_EXTERNAL_PHENOMENOLOGICAL",
            "numeric_components": f"Delta_Q_surface_binding={dd_surface.get('delta_value', 'MISSING')};abs={dd_surface.get('delta_abs', 'MISSING')}",
            "status": "SMOKE_NUMERIC_NOT_FULL_TENSOR",
            "missing_for_claim": "MTS parent basis; source vector; tau/readout; coefficient owner",
            "generated_utc": generated,
        }),
        nonclaim({
            "material_id": "MAT2786_5_full_tensor_upgrade",
            "object": "R_TA6V_minus_PtRh10 full material tensor",
            "mass_fraction_or_composition": "requires all relevant mass, EM, binding, nuclear, and parent-source sensitivities",
            "atomic_context": "not reducible to two smoke components unless parent basis selects them",
            "source": "P8_Y5_R2FR_2785_MATERIAL_TENSOR_CONTRACT.csv:MTC2785_5_claim_gate",
            "mapped_basis": "MISSING_MTS_PARENT_BASIS",
            "numeric_components": "MISSING_FULL_MATERIAL_TENSOR",
            "status": "MISSING_FOR_CLAIM",
            "missing_for_claim": "parent basis and full response map",
            "generated_utc": generated,
        }),
    ]


def build_c_parent_rows() -> list[dict[str, Any]]:
    generated = ts()
    return [
        nonclaim({
            "coefficient_id": "CP2786_0_definition",
            "object": "C_parent",
            "definition": "parent finite WEP coupling coefficient vector multiplying Earth/source and test-mass response vectors",
            "candidate_basis": "MISSING_MTS_PARENT_BASIS",
            "value": "MISSING_PARENT_COEFFICIENT",
            "units": "basis-dependent",
            "status": "MISSING_FOR_CLAIM",
            "missing_for_claim": "derive from parent action or explicitly source as finite phenomenological coefficient",
            "generated_utc": generated,
        }),
        nonclaim({
            "coefficient_id": "CP2786_1_current_owner_partial",
            "object": "C_parent",
            "definition": "Hilbert-current owner fixes post-variation source definition but not coupling magnitude",
            "candidate_basis": "current-owner subtheorem",
            "value": "NO_NUMERIC_COEFFICIENT_SUPPLIED",
            "units": "not_applicable",
            "status": "PARTIAL_THEOREM_NOT_COEFFICIENT",
            "missing_for_claim": "pre-variation action/species weights or finite coefficient still unresolved",
            "generated_utc": generated,
        }),
        nonclaim({
            "coefficient_id": "CP2786_2_DD_basis_external",
            "object": "C_parent in Damour-Donoghue basis",
            "definition": "external phenomenological coefficients can be bounded but are not MTS-derived parent coefficients",
            "candidate_basis": "DD_ALPHA_SURFACE_EXTERNAL",
            "value": "MISSING_DD_COEFFICIENT_VECTOR",
            "units": "dimensionless per selected charge convention",
            "status": "PHENOMENOLOGICAL_BASIS_AVAILABLE_NONCLAIM",
            "missing_for_claim": "MTS-to-DD basis map and coefficient derivation",
            "generated_utc": generated,
        }),
        nonclaim({
            "coefficient_id": "CP2786_3_finite_source_option",
            "object": "C_parent finite sourced-input route",
            "definition": "if derivation fails, a phenomenological coefficient vector may be fitted/bounded only as an explicit non-fundamental closure",
            "candidate_basis": "PENDING_PARENT_OR_EXTERNAL_BASIS",
            "value": "MISSING_SOURCED_FINITE_COEFFICIENT",
            "units": "basis-dependent",
            "status": "ACQUISITION_CONTRACT_ONLY",
            "missing_for_claim": "source path, prior, units, sign convention, and non-fundamental label",
            "generated_utc": generated,
        }),
    ]


def build_readout_rows() -> list[dict[str, Any]]:
    generated = ts()
    return [
        nonclaim({
            "readout_id": "READ2786_0_measurement_equation",
            "object": "K_MICROSCOPE readout model",
            "source": "WEB2786_0_MICROSCOPE_SF2A_2023",
            "content": "projected differential acceleration model uses gx, gz, Sxx, Sxz, offsets, and polynomial drift terms",
            "status": "MODEL_STRUCTURE_SOURCE_BACKED",
            "missing_for_claim": "official arrays/masks or validated reconstruction in the same product convention",
            "generated_utc": generated,
        }),
        nonclaim({
            "readout_id": "READ2786_1_CMSM_portal",
            "object": "official CMSM data portal",
            "source": "WEB2786_3_MICROSCOPE_RESULTS_2023; P8_Y5_R2FR_2780_CMSM_EXPORT_INVENTORY_CHECK.csv",
            "content": "data/documentation portal identified; local export search found no user-supplied CMSM export",
            "status": "OFFICIAL_PORTAL_IDENTIFIED_ARRAYS_NOT_IMPORTED",
            "missing_for_claim": "download/import gx,gz,Sxx,Sxz/masks or user-assisted official export",
            "generated_utc": generated,
        }),
        nonclaim({
            "readout_id": "READ2786_2_surrogate_matrix",
            "object": "surrogate K_MICROSCOPE",
            "source": "P8_Y5_R2FR_2781_TAU_SHAPE_STATUS.csv:TAUSHAPE2781_0_matrix_available",
            "content": "surrogate design matrix exists and recovered synthetic tau-shape coefficients",
            "status": "SURROGATE_AVAILABLE_NONCLAIM",
            "missing_for_claim": "official arrays and parent material/source map",
            "generated_utc": generated,
        }),
        nonclaim({
            "readout_id": "READ2786_3_physical_tau",
            "object": "physical tau_WEP",
            "source": "P8_Y5_R2FR_2781_TAU_SHAPE_STATUS.csv:TAUSHAPE2781_2_physics_tau",
            "content": "physical tau not acquired",
            "status": "NOT_ACQUIRED",
            "missing_for_claim": "official arrays plus C_parent/R_source/R_material product basis",
            "generated_utc": generated,
        }),
    ]


def build_basis_gate_rows() -> list[dict[str, Any]]:
    generated = ts()
    return [
        nonclaim({
            "basis_gate_id": "BASIS2786_0_same_basis_formula",
            "object": "same-basis finite WEP product",
            "required_condition": "C_parent^I, R_source_I^Earth, DeltaR_material_I, and K_MICROSCOPE projection are defined in one declared basis with units",
            "current_status": "NOT_CLOSED",
            "blocking_input": "MISSING_MTS_PARENT_BASIS",
            "claim_allowed": False,
            "generated_utc": generated,
        }),
        nonclaim({
            "basis_gate_id": "BASIS2786_1_external_DD_basis",
            "object": "Damour-Donoghue alpha/surface basis",
            "required_condition": "MTS-to-DD coefficient map derives C_parent -> (c_alpha,c_surface)",
            "current_status": "EXTERNAL_SMOKE_ONLY",
            "blocking_input": "PARENT_TO_DD_MAP_MISSING",
            "claim_allowed": False,
            "generated_utc": generated,
        }),
        nonclaim({
            "basis_gate_id": "BASIS2786_2_source_common_mode",
            "object": "source common-mode theorem",
            "required_condition": "parent action proves Earth/source leg cancels or is universal without measured-G absorption",
            "current_status": "THEOREM_NOT_SIGNED",
            "blocking_input": "SOURCE_VECTOR_OR_COMMON_MODE_PROOF_MISSING",
            "claim_allowed": False,
            "generated_utc": generated,
        }),
        nonclaim({
            "basis_gate_id": "BASIS2786_3_readout_projection",
            "object": "MICROSCOPE arena projection",
            "required_condition": "official/validated readout maps the finite product to eta_WEP with declared tau_WEP",
            "current_status": "SURROGATE_ONLY",
            "blocking_input": "OFFICIAL_ARRAYS_OR_VALIDATED_RECONSTRUCTION_MISSING",
            "claim_allowed": False,
            "generated_utc": generated,
        }),
    ]


def build_acquisition_rows() -> list[dict[str, Any]]:
    generated = ts()
    rows = [
        ("ACQ2786_0_parent_basis", "derive or select finite WEP basis", "MTS parent action slots -> response basis I", "FIRST", "basis controls every other row"),
        ("ACQ2786_1_C_parent", "derive/source coefficient vector", "C_parent^I with units, sign convention, source path", "SECOND", "coefficient owner is the coupling gap"),
        ("ACQ2786_2_R_source", "vectorize Earth/source", "R_source_I^Earth from source composition/worldtube or theorem common-mode proof", "THIRD", "source leg cannot be set to one by taste"),
        ("ACQ2786_3_DeltaR_material", "build full material tensor", "R_TA6V_I - R_PtRh10_I with uncertainty and composition provenance", "THIRD", "toy/DD smoke rows are not parent tensor evidence"),
        ("ACQ2786_4_K_readout", "import/validate MICROSCOPE readout", "gx,gz,Sxx,Sxz,masks and tau_WEP projection", "FOURTH", "surrogate matrix is a smoke runner only"),
        ("ACQ2786_5_runner", "run finite WEP product comparator", "numeric same-basis product against eta bound", "LAST", "must refuse until all upstream rows are claim-valid"),
    ]
    return [
        nonclaim({
            "acquisition_id": row_id,
            "task": task,
            "required_artifact": artifact,
            "priority": priority,
            "reason": reason,
            "status": "PENDING_SOURCE_OR_DERIVATION",
            "generated_utc": generated,
        })
        for row_id, task, artifact, priority, reason in rows
    ]


def build_input_pack_rows() -> list[dict[str, Any]]:
    generated = ts()
    return [
        nonclaim({
            "input_id": "FIP2786_0_product_formula",
            "object": "P_WEP finite product",
            "candidate_value": "P_WEP = sum_I C_parent^I * R_source_I^Earth * DeltaR_material_I projected by K_MICROSCOPE",
            "units": "dimensionless eta convention",
            "status": "FORMULA_READY_NONCLAIM",
            "source_or_basis": "2785 finite WEP contract",
            "blocks_claim": "all numeric input rows still required",
            "generated_utc": generated,
        }),
        nonclaim({
            "input_id": "FIP2786_1_C_parent",
            "object": "C_parent",
            "candidate_value": "MISSING_PARENT_COEFFICIENT",
            "units": "basis-dependent",
            "status": "MISSING_FOR_CLAIM",
            "source_or_basis": "CP2786 rows",
            "blocks_claim": "no MTS coupling magnitude or basis owner",
            "generated_utc": generated,
        }),
        nonclaim({
            "input_id": "FIP2786_2_R_source",
            "object": "R_source^Earth",
            "candidate_value": "REFERENCE_IDENTIFIED_NOT_VECTORIZED",
            "units": "basis-dependent",
            "status": "MISSING_FOR_CLAIM",
            "source_or_basis": "McDonough-Sun candidate plus MICROSCOPE Earth-source role",
            "blocks_claim": "no same-basis Earth source vector",
            "generated_utc": generated,
        }),
        nonclaim({
            "input_id": "FIP2786_3_R_material",
            "object": "R_TA6V - R_PtRh10",
            "candidate_value": "R2FR toy vector and DD smoke deltas available; full tensor missing",
            "units": "basis-dependent",
            "status": "PARTIAL_SMOKE_NUMERIC_NONCLAIM",
            "source_or_basis": "MAT2786 rows",
            "blocks_claim": "external smoke/toy basis not parent MTS basis; full tensor missing",
            "generated_utc": generated,
        }),
        nonclaim({
            "input_id": "FIP2786_4_K_readout",
            "object": "K_MICROSCOPE",
            "candidate_value": "surrogate available; official portal identified; arrays not imported",
            "units": "eta projection convention",
            "status": "SURROGATE_ONLY_NONCLAIM",
            "source_or_basis": "READ2786 rows",
            "blocks_claim": "official arrays or validated reconstruction required",
            "generated_utc": generated,
        }),
        nonclaim({
            "input_id": "FIP2786_5_tau_WEP",
            "object": "tau_WEP",
            "candidate_value": "MISSING_PHYSICAL_TAU",
            "units": "dimensionless",
            "status": "MISSING_FOR_CLAIM",
            "source_or_basis": "TAUSHAPE2781_2_physics_tau",
            "blocks_claim": "tau cannot be set to one or absorbed into measured G",
            "generated_utc": generated,
        }),
    ]


def build_candidate_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "prediction_id": "PRED2786_0_WEP_finite_input_pack_nonclaim",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_C_PARENT_R_SOURCE_R_MATERIAL_K_READOUT_TAU_NUMERIC_PRODUCT",
            "product_units": "dimensionless",
            "derivation_status": "ACQUISITION_PACK_READY_PRODUCT_MISSING",
            "notes": "source candidates and smoke components are staged, but no same-basis finite MTS product exists",
        })
    ]


def build_bound_rows() -> list[dict[str, Any]]:
    bound = get_local_bound("R1_WEP_source_charge")
    return [
        nonclaim({
            "bound_id": "BOUND2786_0_MICROSCOPE_WEP_source_charge",
            "arena": "MICROSCOPE_WEP",
            "observable": "eta_WEP_source_charge",
            "upper_bound": bound.get("upper_bound", "2.8e-15"),
            "units": bound.get("units", "dimensionless"),
            "source_path_or_url": bound.get("reference_path_or_url", "https://arxiv.org/abs/2209.15487; doi:10.1103/PhysRevLett.129.121102"),
            "source_row": "source-intake/local_bounds/local_bound_claims.csv:R1_WEP_source_charge",
            "valid_bound_row": True,
        })
    ]


def build_runner_rows(candidate_rows: list[dict[str, Any]], bound_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    valid_prediction_rows = [
        row for row in candidate_rows
        if trueish(row.get("valid_for_claim")) and is_numeric(row.get("product_value")) and not has_missing_marker(row)
    ]
    valid_bound_rows = [
        row for row in bound_rows
        if trueish(row.get("valid_bound_row")) and is_numeric(row.get("upper_bound")) and float(row.get("upper_bound", 0)) > 0
    ]
    return [
        nonclaim({
            "runner_id": "APR2786_0_WEP_finite_input_pack_product_stub",
            "prediction_rows": len(candidate_rows),
            "bound_rows": len(bound_rows),
            "valid_prediction_rows": len(valid_prediction_rows),
            "valid_bound_rows": len(valid_bound_rows),
            "comparison_rows": 1,
            "passed_rows": 0,
            "claim_allowed": False,
            "expected_result": "reject acquisition-pack rows until same-basis numeric product exists",
        })
    ]


def build_comparison_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "comparison_id": "COMP2786_0_MICROSCOPE_WEP",
            "prediction_id": "PRED2786_0_WEP_finite_input_pack_nonclaim",
            "bound_id": "BOUND2786_0_MICROSCOPE_WEP_source_charge",
            "abs_prediction": "MISSING_C_PARENT_R_SOURCE_R_MATERIAL_K_READOUT_TAU_NUMERIC_PRODUCT",
            "upper_bound": "2.8e-15",
            "passes_bound": False,
            "comparison_status": "NOT_RUN_NUMERICALLY",
            "reason": "prediction is not numeric and same-basis finite WEP product is missing",
        })
    ]


def build_gate_rows() -> list[dict[str, Any]]:
    generated = ts()
    rows = [
        ("CG2786_0_sources", "source candidates identified", True, False, "paper/source roles are staged but not transformed into final vectors"),
        ("CG2786_1_parent_basis", "MTS parent finite WEP basis", False, False, "basis not derived"),
        ("CG2786_2_C_parent", "C_parent coefficient vector", False, False, "coefficient missing"),
        ("CG2786_3_R_source", "R_source^Earth vector", False, False, "Earth composition/reference not vectorized in parent basis"),
        ("CG2786_4_R_material", "R_TA6V - R_PtRh10 full material tensor", False, False, "only composition context, toy vector, and external smoke deltas exist"),
        ("CG2786_5_K_readout_tau", "K_MICROSCOPE and tau_WEP", False, False, "surrogate readout only; physical tau not acquired"),
        ("CG2786_6_product_runner", "finite WEP product runner", False, False, "valid_prediction_rows=0"),
    ]
    return [
        nonclaim({
            "gate_id": gate_id,
            "gate": gate,
            "supporting_context_present": context_present,
            "claim_allowed": claim_allowed,
            "reason": reason,
            "generated_utc": generated,
        })
        for gate_id, gate, context_present, claim_allowed, reason in rows
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    generated = ts()
    rows = [
        ("DEC2786_0_pack_value", "finite WEP acquisition pack is now source-anchored but not score-ready", "MICROSCOPE material/readout references, DD material charge basis, Earth composition reference, and R2FR surrogate status are named", "do not claim; instantiate a basis only as a nonclaim smoke runner"),
        ("DEC2786_1_key_gap", "the coupling/basis gap is now the bottleneck", "C_parent and the MTS parent response basis determine whether material/source rows are physics or just bookkeeping", "try parent-basis derivation before treating DD rows as anything more than a comparator"),
        ("DEC2786_2_next_route", "build a parent-basis derivation or DD smoke runner as the next practical scaffold", "the pack can test pipeline algebra once a basis policy is explicit", "2787 should derive MTS parent WEP basis first; if unsigned, instantiate DD alpha/surface smoke runner with strict nonclaim gates"),
    ]
    return [
        nonclaim({
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "generated_utc": generated,
        })
        for decision_id, decision, reason, next_action in rows
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "next_id": "NEXT2786_0_2787",
            "next_target": "2787-Y5-R2FR-parent-WEP-basis-derivation-or-DD-finite-WEP-smoke-runner-under-AX1090.md",
            "script": "scripts/Y5_R2FR_parent_WEP_basis_derivation_or_DD_finite_WEP_smoke_runner_under_AX1090_2787.py",
            "objective": "try to derive the MTS parent WEP response basis and coefficient map; if it remains unsigned, instantiate a Damour-Donoghue alpha/surface finite-WEP smoke runner with explicit source/readout policy and strict nonclaim gates",
            "include": "parent response basis; C_parent units; MTS-to-DD map; Earth source policy; TA6V/PtRh10 smoke deltas; MICROSCOPE readout gate; product runner refusal",
            "exclude": "DD smoke as MTS claim; unit source/readout as tau_WEP; measured-G absorption; tau=1; public claim; GitHub; formalization edits",
        })
    ]


def copy_branches() -> list[dict[str, Any]]:
    copy_pairs = [
        (OUTPUTS["input_pack"], BRANCH_OUTPUTS["input_pack_queue"], "input_pack_queue"),
        (OUTPUTS["earth_source"], BRANCH_OUTPUTS["earth_queue"], "earth_queue"),
        (OUTPUTS["basis_gate"], BRANCH_OUTPUTS["beta_doc"], "beta_doc"),
        (OUTPUTS["readout"], BRANCH_OUTPUTS["microscope_copy"], "microscope_copy"),
        (OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next_queue"),
    ]
    rows = []
    for source, target, branch_key in copy_pairs:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(nonclaim({
            "branch_id": f"BR2786_{len(rows)}_{branch_key}",
            "source_path": str(source),
            "branch_path": str(target),
            "exists": target.exists(),
            "row_count": csv_row_count(target) if target.exists() else 0,
            "branch_role": branch_key,
        }))
    return rows


def no_claim_flags(paths: list[Path]) -> bool:
    flag_fields = {"valid_for_claim", "claim_allowed", "pass_for_claim"}
    for path in paths:
        for row in read_csv_rows(path):
            for field in flag_fields:
                if trueish(row.get(field)):
                    return False
    return True


def formalization_modified_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    started = RUN_STARTED_UTC.timestamp()
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and path.stat().st_mtime >= started:
            count += 1
    return count


def build_validation_rows(sections: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    checks = [
        ("VAL2786_0_sources", all(trueish(row["exists"]) and trueish(row["needle_found"]) for row in sections["sources"]), "every cited source path exists and source needle was found"),
        ("VAL2786_1_web_sources_identified", all(row["source_url"].startswith("http") for row in sections["web_sources"]), "web/source candidates are recorded with URLs"),
        ("VAL2786_2_earth_source_blocked", any(row["source_vector_id"] == "EARTH2786_2_parent_basis_block" and row["status"] == "MISSING_FOR_CLAIM" for row in sections["earth_source"]), "Earth/source vector reference exists but same-basis vector is missing"),
        ("VAL2786_3_material_context", any(row["material_id"] == "MAT2786_0_PtRh10_MICROSCOPE" and row["status"] == "SOURCE_BACKED_COMPOSITION_CONTEXT" for row in sections["material"]) and any(row["material_id"] == "MAT2786_1_TA6V_MICROSCOPE" and row["status"] == "SOURCE_BACKED_COMPOSITION_CONTEXT" for row in sections["material"]), "MICROSCOPE material compositions are recorded"),
        ("VAL2786_4_material_full_tensor_missing", any(row["material_id"] == "MAT2786_5_full_tensor_upgrade" and row["status"] == "MISSING_FOR_CLAIM" for row in sections["material"]), "full parent material tensor remains missing"),
        ("VAL2786_5_c_parent_missing", any(row["coefficient_id"] == "CP2786_0_definition" and row["value"] == "MISSING_PARENT_COEFFICIENT" for row in sections["c_parent"]), "C_parent coefficient remains missing"),
        ("VAL2786_6_readout_tau_missing", any(row["readout_id"] == "READ2786_3_physical_tau" and row["status"] == "NOT_ACQUIRED" for row in sections["readout"]), "physical tau_WEP remains missing"),
        ("VAL2786_7_same_basis_gate_blocks", all(not trueish(row["claim_allowed"]) for row in sections["basis_gate"]), "same-basis closure gates block claims"),
        ("VAL2786_8_acquisition_priority_written", len(sections["acquisition"]) >= 6 and sections["acquisition"][0]["priority"] == "FIRST", "acquisition priority ledger is written"),
        ("VAL2786_9_input_pack_nonclaim", all(not trueish(row["valid_for_claim"]) for row in sections["input_pack"]) and any(has_missing_marker(row) for row in sections["input_pack"]), "finite WEP input pack remains nonclaim and missing claim inputs"),
        ("VAL2786_10_prediction_nonclaim_missing", all(has_missing_marker(row) and not trueish(row.get("valid_for_claim")) for row in sections["candidate"]), "prediction row remains missing same-basis finite inputs"),
        ("VAL2786_11_bound_numeric", all(is_numeric(row["upper_bound"]) and float(row["upper_bound"]) > 0 for row in sections["bounds"]), "bound import is positive numeric"),
        ("VAL2786_12_runner_refuses", sections["runner"][0]["valid_prediction_rows"] == 0 and not trueish(sections["runner"][0]["claim_allowed"]), "runner reports no valid prediction rows and claim false"),
        ("VAL2786_13_claim_gates_safe", all(not trueish(row.get("claim_allowed")) for row in sections["gates"]), "all claim gates deny WEP/local-GR claim"),
        ("VAL2786_14_next_target", sections["next"][0]["next_target"].startswith("2787-Y5_R2FR".replace("_", "-")) or "2787-Y5-R2FR" in sections["next"][0]["next_target"], "2787 handoff written"),
        ("VAL2786_15_branch_outputs", all(trueish(row["exists"]) and int(row["row_count"]) > 0 for row in sections["branches"]), "branch copies exist and contain rows"),
        ("VAL2786_16_csv_parse", all(csv_parses(path) for path in generated_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2786_17_no_claim_flags", no_claim_flags(generated_paths), "no generated row is valid_for_claim=true/claim_allowed=true/pass_for_claim=true"),
        ("VAL2786_18_generated_under_post_checkpoint", all(WORK in path.parents or path == WORK for path in generated_paths + [DOC]), "all generated outputs are under post-checkpoint-work"),
        ("VAL2786_19_formalization_untouched", formalization_modified_count() == 0, "formalization-workbench modified-file count remains zero during this run"),
        ("VAL2786_20_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ absent at validation write"),
    ]
    rows = [
        {
            "validation_id": check_id,
            "passed": bool(passed),
            "detail": detail,
            "timestamp_utc": ts(),
        }
        for check_id, passed, detail in checks
    ]
    rows.append({
        "validation_id": "VAL2786_OVERALL",
        "passed": all(row["passed"] for row in rows),
        "detail": "2786 turns the finite WEP route into a source-anchored acquisition pack. MICROSCOPE composition/readout sources, Earth-source reference, R2FR toy and DD smoke material rows, C_parent contract, same-basis gates, and runner refusal are staged; no WEP/local-GR claim is allowed until a same-basis numeric product exists.",
        "timestamp_utc": ts(),
    })
    return rows


def build_doc(sections: dict[str, list[dict[str, Any]]]) -> str:
    lines = [
        "# 2786 - Finite WEP source-vector and material-tensor acquisition pack under AX1090",
        "",
        "## Private Verdict",
        "",
        "2786 makes the WEP route more usable without pretending it is solved. The source anchors are now staged: MICROSCOPE composition/readout references, Earth composition reference, R2FR toy material deltas, external DD smoke deltas, C_parent contract, same-basis gates, and runner refusal. The bottleneck is still the coupling/basis owner: without a parent response basis and C_parent, the material/source rows are bookkeeping, not a derived MTS WEP prediction.",
        "",
        "## Source Register",
        markdown_table(sections["sources"], ["row_id", "source_key", "exists", "needle_found", "source_role"]),
        "",
        "## Web/Source Candidate Register",
        markdown_table(sections["web_sources"], ["web_source_id", "role", "source_url", "extraction_status"]),
        "",
        "## Earth Source Vector Candidates",
        markdown_table(sections["earth_source"], ["source_vector_id", "object", "basis", "status", "missing_for_claim"]),
        "",
        "## Material Composition And Tensor Candidates",
        markdown_table(sections["material"], ["material_id", "object", "mapped_basis", "numeric_components", "status", "missing_for_claim"]),
        "",
        "## C_parent Coefficient Contract",
        markdown_table(sections["c_parent"], ["coefficient_id", "object", "candidate_basis", "value", "status", "missing_for_claim"]),
        "",
        "## MICROSCOPE Readout Gate",
        markdown_table(sections["readout"], ["readout_id", "object", "status", "missing_for_claim"]),
        "",
        "## Same-Basis Closure Gate",
        markdown_table(sections["basis_gate"], ["basis_gate_id", "object", "current_status", "blocking_input", "claim_allowed"]),
        "",
        "## Acquisition Priority Ledger",
        markdown_table(sections["acquisition"], ["acquisition_id", "task", "required_artifact", "priority", "status"]),
        "",
        "## Finite WEP Input Pack",
        markdown_table(sections["input_pack"], ["input_id", "object", "candidate_value", "status", "blocks_claim"]),
        "",
        "## Product Stub And Bound",
        markdown_table(sections["candidate"], ["prediction_id", "product_symbol", "product_value", "derivation_status", "valid_for_claim"]),
        "",
        markdown_table(sections["bounds"], ["bound_id", "observable", "upper_bound", "units", "valid_bound_row"]),
        "",
        markdown_table(sections["runner"], ["runner_id", "valid_prediction_rows", "valid_bound_rows", "claim_allowed", "expected_result"]),
        "",
        "## Claim Gates",
        markdown_table(sections["gates"], ["gate_id", "gate", "supporting_context_present", "claim_allowed", "reason"]),
        "",
        "## Decision Ledger",
        markdown_table(sections["decision"], ["decision_id", "decision", "reason", "next_action"]),
        "",
        "## Validation",
        markdown_table(sections["validation"], ["validation_id", "passed", "detail"]),
        "",
        "## Next Target",
        markdown_table(sections["next"], ["next_id", "next_target", "objective", "include", "exclude"]),
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    ensure_dirs()
    if (SCRIPTS / "__pycache__").exists():
        shutil.rmtree(SCRIPTS / "__pycache__")

    sections: dict[str, list[dict[str, Any]]] = {
        "sources": build_sources(),
        "web_sources": build_web_sources(),
        "earth_source": build_earth_source_rows(),
        "material": build_material_rows(),
        "c_parent": build_c_parent_rows(),
        "readout": build_readout_rows(),
        "basis_gate": build_basis_gate_rows(),
        "acquisition": build_acquisition_rows(),
        "input_pack": build_input_pack_rows(),
        "candidate": build_candidate_rows(),
        "bounds": build_bound_rows(),
    }
    sections["runner"] = build_runner_rows(sections["candidate"], sections["bounds"])
    sections["comparisons"] = build_comparison_rows()
    sections["gates"] = build_gate_rows()
    sections["decision"] = build_decision_rows()
    sections["next"] = build_next_rows()

    for key, rows in sections.items():
        if key in OUTPUTS:
            write_csv(OUTPUTS[key], rows)

    sections["branches"] = copy_branches()
    write_csv(OUTPUTS["branches"], sections["branches"])

    sections["validation"] = build_validation_rows(sections)
    write_csv(OUTPUTS["validation"], sections["validation"])

    DOC.write_text(build_doc(sections), encoding="utf-8")
    print(f"wrote {DOC}")
    print(f"validation overall: {sections['validation'][-1]['passed']}")


if __name__ == "__main__":
    main()
