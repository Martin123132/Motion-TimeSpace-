from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1328"
TITLE = "1328-Y5-R10-RAB-component-fraction-source-acquisition-or-EM-QCD-edge-owner-reentry"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
COMPONENT_ROOT = ROOT / "source-intake" / "component-fractions"
COMPONENT_DOCS = COMPONENT_ROOT / "docs"
COMPONENT_RAW = COMPONENT_ROOT / "raw"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
PUBLIC_SOURCE_PATH = OUT_DIR / f"{PACK_ID}_PUBLIC_SOURCE_CANDIDATE_REGISTER.csv"
ROUTE_MATRIX_PATH = OUT_DIR / f"{PACK_ID}_COMPONENT_SOURCE_ROUTE_MATRIX.csv"
FORMULA_CONTRACT_PATH = OUT_DIR / f"{PACK_ID}_EXTRACTION_FORMULA_CONTRACT.csv"
ACCEPTANCE_PRECHECK_PATH = OUT_DIR / f"{PACK_ID}_COMPONENT_FRACTION_ACCEPTANCE_PRECHECK.csv"
GRAPH_REENTRY_PATH = OUT_DIR / f"{PACK_ID}_GRAPH_EDGE_OWNER_REENTRY_BLOCKERS.csv"
RUNNER_PATH = OUT_DIR / f"{PACK_ID}_DELTA_W_RUNNER_UPDATE.csv"
ANTI_SHORTCUT_PATH = OUT_DIR / f"{PACK_ID}_ANTI_SHORTCUT_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1328_VALIDATION.csv"
COMPONENT_CANDIDATE_PACK_PATH = COMPONENT_DOCS / f"{PACK_ID}_COMPONENT_SOURCE_CANDIDATE_PACK_NONCLAIM.csv"


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
            if not is_false(row.get("valid_for_claim", False)):
                return False
            if "claim_allowed" in row and not is_false(row.get("claim_allowed", False)):
                return False
    return True


def generated_inside_formalization() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    return [path for path in FORMALIZATION.rglob("*1328*") if path.is_file()]


def raw_1328_candidates() -> list[Path]:
    if not COMPONENT_RAW.exists():
        return []
    return [path for path in COMPONENT_RAW.rglob("*1328*") if path.is_file()]


def first(rows: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    for row in rows:
        if row.get(key) == value:
            return row
    return {}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    COMPONENT_DOCS.mkdir(parents=True, exist_ok=True)
    COMPONENT_RAW.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1328_0_1327_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1327_NEXT_TARGET.csv",
            "needle": "NEXT1327_0_1328",
            "role": "selected 1328 target",
        },
        {
            "source_id": "SRC1328_1_1327_intake",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1327_DELTA_W_COMPONENT_INTAKE_MATRIX.csv",
            "needle": "CFI1327_TA6V_electron",
            "role": "twelve row component intake matrix",
        },
        {
            "source_id": "SRC1328_2_1327_validation",
            "local_path": "source-intake/mts_residuals/P8_Y5_BRR545_1327_VALIDATION.csv",
            "needle": "VAL1327_10_overall",
            "role": "1327 pass gate",
        },
        {
            "source_id": "SRC1328_3_1233_schema",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1233_COMPONENT_FRACTION_SCHEMA.csv",
            "needle": "fraction_value",
            "role": "component-fraction candidate schema",
        },
        {
            "source_id": "SRC1328_4_1233_dryrun",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1233_COMPONENT_FRACTION_VALIDATOR_DRYRUN.csv",
            "needle": "NO_CANDIDATE_FILES_PRESENT",
            "role": "current accepted-row baseline",
        },
        {
            "source_id": "SRC1328_5_1232_source_pack",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1232_TIPT_COMPONENT_FRACTION_SOURCE_PACK.csv",
            "needle": "FSP1232_3_light_quark_fraction",
            "role": "component-source blockers",
        },
        {
            "source_id": "SRC1328_6_1232_quarantine",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1232_TOY_PROXY_QUARANTINE.csv",
            "needle": "QUAR1232_0_983_proxy_vectors",
            "role": "proxy/toy quarantine",
        },
        {
            "source_id": "SRC1328_7_1236_edges",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1236_GRAPH_EDGE_STATUS_UPDATE.csv",
            "needle": "EDGE1232_2_quark_gluon",
            "role": "latest graph-edge blockers",
        },
        {
            "source_id": "SRC1328_8_1232_graph_certificate",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1232_INTERACTION_GRAPH_CERTIFICATE_ATTEMPT.csv",
            "needle": "IGC1232_4_verdict",
            "role": "parent graph certificate conditional theorem",
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

    intake_rows = read_csv(source_path("source-intake/mts_residuals/P8_Y5_R10_1327_DELTA_W_COMPONENT_INTAKE_MATRIX.csv"))
    schema_rows = read_csv(source_path("source-intake/mts_residuals/P8_Y5_R10_1233_COMPONENT_FRACTION_SCHEMA.csv"))
    dryrun_rows = read_csv(source_path("source-intake/mts_residuals/P8_Y5_R10_1233_COMPONENT_FRACTION_VALIDATOR_DRYRUN.csv"))
    edge_rows = read_csv(source_path("source-intake/mts_residuals/P8_Y5_R10_1236_GRAPH_EDGE_STATUS_UPDATE.csv"))

    public_sources = [
        {
            "public_source_id": "PSRC1328_0_microscope_final_results",
            "target": "MICROSCOPE final WEP result and test-mass context",
            "url_or_doi": "https://arxiv.org/abs/2209.15487",
            "usable_for": "measure_readout;tau_WEP;material_context",
            "extraction_plan": "record final tau/eta context and link readout only after source-worldtube normalization is signed",
            "source_status": "SOURCE_CANDIDATE_NOT_EXTRACTED",
            "confidence": "high_for_context_low_for_MTS_projection",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "public_source_id": "PSRC1328_1_microscope_materials_summary",
            "target": "PtRh10 and TA6V alloy composition cross-check",
            "url_or_doi": "https://proceedings.sf2a.eu/2023/2023sf2a.conf..31M.pdf",
            "usable_for": "electron;alloy_context;isotope_weighting",
            "extraction_plan": "cross-check PtRh10 90/10 and TA6V Ti/Al/V composition against local 983/1080 rows",
            "source_status": "SOURCE_CANDIDATE_NOT_EXTRACTED",
            "confidence": "medium_corrob_source",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "public_source_id": "PSRC1328_2_CIAAW_isotopic_abundances_2024",
            "target": "natural isotopic compositions for Ti, Al, V, Pt, Rh",
            "url_or_doi": "https://www.ciaaw.org/isotopic-abundances.htm",
            "usable_for": "electron;light_quark;QCD_gluon;EM_Coulomb;nuclear_surface",
            "extraction_plan": "extract isotope abundances with uncertainties before any alloy-averaged mass budget",
            "source_status": "SOURCE_CANDIDATE_NOT_EXTRACTED",
            "confidence": "high_for_isotope_abundances",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "public_source_id": "PSRC1328_3_NIST_atomic_weights_isotopic_compositions",
            "target": "relative atomic masses and standard atomic weights",
            "url_or_doi": "https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl",
            "usable_for": "electron;isotope_weighting;material_mass_normalization",
            "extraction_plan": "extract Z, isotope masses, natural compositions, and atomic-weight normalization with provenance",
            "source_status": "SOURCE_CANDIDATE_NOT_EXTRACTED",
            "confidence": "high_for_mass_normalization",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "public_source_id": "PSRC1328_4_AME2020_atomic_masses",
            "target": "claim-grade nuclide masses and mass uncertainties",
            "url_or_doi": "https://www-nds.iaea.org/amdc/",
            "usable_for": "electron;light_quark;QCD_gluon;EM_Coulomb;nuclear_surface",
            "extraction_plan": "download or manually extract AME2020 atomic masses only in a later audited extractor",
            "source_status": "SOURCE_CANDIDATE_NOT_EXTRACTED",
            "confidence": "high_for_atomic_mass_table",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "public_source_id": "PSRC1328_5_Damour_Donoghue_dilaton_charges",
            "target": "external DD source-charge decomposition",
            "url_or_doi": "https://arxiv.org/abs/1007.2792",
            "usable_for": "light_quark;EM_Coulomb;nuclear_surface;external_comparator",
            "extraction_plan": "use only as external phenomenological basis unless parent MTS map to DD charges is derived",
            "source_status": "SOURCE_CANDIDATE_NOT_EXTRACTED_EXTERNAL_BASIS_ONLY",
            "confidence": "high_for_external_DD_low_for_parent_MTS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "public_source_id": "PSRC1328_6_Damour_Donoghue_DOI",
            "target": "published DOI for DD decomposition provenance",
            "url_or_doi": "https://link.aps.org/doi/10.1103/PhysRevD.82.084033",
            "usable_for": "light_quark;EM_Coulomb;nuclear_surface;external_comparator",
            "extraction_plan": "mirror arXiv extraction with DOI provenance; do not promote to MTS parent basis",
            "source_status": "SOURCE_CANDIDATE_NOT_EXTRACTED_EXTERNAL_BASIS_ONLY",
            "confidence": "high_for_external_DD_low_for_parent_MTS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "public_source_id": "PSRC1328_7_Damour_material_charge_table_secondary",
            "target": "rough material-charge sanity table only",
            "url_or_doi": "https://www.ihes.fr/~damour/Conferences/ONERA29Jan2013.pdf",
            "usable_for": "sanity_check_only",
            "extraction_plan": "secondary presentation only; cannot replace primary formula extraction",
            "source_status": "SECONDARY_SOURCE_CANDIDATE_NOT_FOR_CLAIM",
            "confidence": "medium_for_sanity_low_for_claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    component_source_map = {
        "electron": {
            "source_ids": "PSRC1328_1_microscope_materials_summary;PSRC1328_2_CIAAW_isotopic_abundances_2024;PSRC1328_3_NIST_atomic_weights_isotopic_compositions;PSRC1328_4_AME2020_atomic_masses",
            "candidate_formula": "F_e(B)=sum_elements w_i * (Z_i*m_e)/(atomic_or_nuclear_mass_i) after choosing atomic/nuclear and chemical-binding convention",
            "parent_gap": "MTS must sign the mass-normalization convention and whether electron rest mass, chemical binding, or both enter delta_w_e",
            "route_status": "SOURCE_CANDIDATE_STAGED_EXTRACTION_REQUIRED",
        },
        "light_quark": {
            "source_ids": "PSRC1328_5_Damour_Donoghue_dilaton_charges;PSRC1328_6_Damour_Donoghue_DOI",
            "candidate_formula": "external DD q_hatm/sigma-term style charge, not yet an MTS parent component fraction",
            "parent_gap": "derive parent map from MTS source weights to DD light-quark charge or demote to comparator",
            "route_status": "EXTERNAL_BASIS_ONLY_PARENT_MAP_MISSING",
        },
        "QCD_gluon": {
            "source_ids": "PSRC1328_4_AME2020_atomic_masses;PSRC1328_5_Damour_Donoghue_dilaton_charges",
            "candidate_formula": "bulk residual after signed mass-budget convention; must avoid double-counting quark, EM, and surface terms",
            "parent_gap": "no parent no-double-counting rule and no signed QCD source owner",
            "route_status": "RESIDUAL_BASIS_ONLY_NO_DOUBLE_COUNT_RULE_MISSING",
        },
        "EM_Coulomb": {
            "source_ids": "PSRC1328_5_Damour_Donoghue_dilaton_charges;PSRC1328_6_Damour_Donoghue_DOI",
            "candidate_formula": "external DD Coulomb/electromagnetic binding charge or SEMF Coulomb term after isotope/alloy averaging",
            "parent_gap": "MTS EM owner and alpha/Coulomb map remain unsigned",
            "route_status": "EXTERNAL_BASIS_ONLY_PARENT_EM_OWNER_MISSING",
        },
        "nuclear_surface": {
            "source_ids": "PSRC1328_5_Damour_Donoghue_dilaton_charges;PSRC1328_6_Damour_Donoghue_DOI;PSRC1328_4_AME2020_atomic_masses",
            "candidate_formula": "external DD surface/asymmetry charge or SEMF residual after isotope/alloy averaging",
            "parent_gap": "MTS nuclear-binding owner and residual convention remain unsigned",
            "route_status": "EXTERNAL_BASIS_ONLY_PARENT_NUCLEAR_OWNER_MISSING",
        },
        "measure_readout": {
            "source_ids": "PSRC1328_0_microscope_final_results",
            "candidate_formula": "DeltaK_TiPt/tau_WEP readout residual only after source-worldtube/readout projection is signed",
            "parent_gap": "readout projection from accelerometer data to MTS source worldtube not derived",
            "route_status": "DATA_SOURCE_CANDIDATE_STAGED_MTS_PROJECTION_MISSING",
        },
    }

    route_matrix: list[dict[str, object]] = []
    for intake in intake_rows:
        component_id = intake["component_id"]
        route = component_source_map[component_id]
        route_matrix.append(
            {
                "route_id": intake["intake_id"].replace("CFI1327", "ROUTE1328"),
                "material_id": intake["material_id"],
                "component_id": component_id,
                "source_candidate_ids": route["source_ids"],
                "candidate_formula": route["candidate_formula"],
                "parent_gap": route["parent_gap"],
                "current_status": route["route_status"],
                "candidate_pack_location": str(COMPONENT_CANDIDATE_PACK_PATH),
                "raw_candidate_created": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    candidate_pack = [
        {
            "row_id": row["route_id"].replace("ROUTE1328", "CFI1328"),
            "material_id": row["material_id"],
            "component_id": row["component_id"],
            "fraction_value": "MISSING_NUMERIC_EXTRACTION",
            "fraction_uncertainty": "MISSING_NUMERIC_EXTRACTION",
            "basis_convention": "source_candidate_only_nonclaim",
            "source_path_or_url": row["source_candidate_ids"],
            "extraction_method": "candidate_formula_contract_not_extracted",
            "status": row["current_status"],
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for row in route_matrix
    ]

    formula_contract = [
        {
            "formula_id": "FORM1328_0_alloy_average",
            "component_id": "all_components",
            "symbolic_contract": "F_B,c = sum_i mass_or_number_weight(B,i) * F_i,c under one declared basis convention",
            "minimum_inputs": "official MICROSCOPE material composition; isotope abundances; atomic or nuclear masses; basis convention",
            "source_candidates": "PSRC1328_1;PSRC1328_2;PSRC1328_3;PSRC1328_4",
            "current_blocker": "material composition exists only as context until mass/number weighting and isotope convention are fixed",
            "output_allowed": "nonclaim source candidate only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "formula_id": "FORM1328_1_electron_fraction",
            "component_id": "electron",
            "symbolic_contract": "F_B,e = electron rest-energy contribution divided by declared material mass-energy normalization",
            "minimum_inputs": "Z, isotope/alloy weights, m_e, atomic/nuclear mass convention, chemical-binding subtraction rule",
            "source_candidates": "PSRC1328_1;PSRC1328_2;PSRC1328_3;PSRC1328_4",
            "current_blocker": "normalization convention not parent-signed",
            "output_allowed": "first numeric dry-run in 1329, still nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "formula_id": "FORM1328_2_external_DD_map",
            "component_id": "light_quark;EM_Coulomb;nuclear_surface",
            "symbolic_contract": "external DD charges may be used as comparator rows only until a parent map MTS_delta_w -> DD charge vector is derived",
            "minimum_inputs": "DD formulas, isotope/alloy averaging, explicit declaration of external_DD basis",
            "source_candidates": "PSRC1328_5;PSRC1328_6",
            "current_blocker": "external basis is not a parent MTS derivation",
            "output_allowed": "comparator/demotion ledger only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "formula_id": "FORM1328_3_QCD_residual",
            "component_id": "QCD_gluon",
            "symbolic_contract": "F_B,g = residual mass-budget term only after quark, EM, surface, electron, and binding conventions are fixed",
            "minimum_inputs": "atomic masses, nuclear binding convention, no-double-counting rule, parent QCD owner",
            "source_candidates": "PSRC1328_4;PSRC1328_5",
            "current_blocker": "residual term would absorb convention errors and cannot be scored as parent-owned",
            "output_allowed": "blocker row only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "formula_id": "FORM1328_4_readout_projection",
            "component_id": "measure_readout",
            "symbolic_contract": "DeltaK_TiPt enters only after official MICROSCOPE readout quantities are projected into the MTS source-worldtube operator",
            "minimum_inputs": "official final result/readout context, accelerometer model, source-worldtube projection, tau_WEP convention",
            "source_candidates": "PSRC1328_0",
            "current_blocker": "MTS readout/worldtube projection not derived",
            "output_allowed": "waitstate/source candidate only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    dryrun = first(dryrun_rows, "dryrun_id", "DRY1233_0_candidate_scan")
    acceptance_precheck = [
        {
            "precheck_id": "PRE1328_0_public_sources_present",
            "target": "public source URLs/provenance",
            "status": "STAGED_NONCLAIM",
            "details": f"public_source_rows={len(public_sources)}",
            "blocks_claim": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "precheck_id": "PRE1328_1_component_coverage",
            "target": "six components for TA6V and PtRh10",
            "status": "COVERED",
            "details": f"route_rows={len(route_matrix)}",
            "blocks_claim": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "precheck_id": "PRE1328_2_raw_candidate_gate",
            "target": "do not place placeholder candidate rows in raw acceptance directory",
            "status": "ENFORCED",
            "details": f"raw_1328_candidate_files={len(raw_1328_candidates())};candidate_pack_location=docs",
            "blocks_claim": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "precheck_id": "PRE1328_3_existing_validator_baseline",
            "target": "1233 validator accepted rows",
            "status": dryrun.get("status", "MISSING_DRYRUN_ROW"),
            "details": f"candidate_csv_count={dryrun.get('candidate_csv_count', 'MISSING')};accepted_rows={dryrun.get('accepted_rows', 'MISSING')}",
            "blocks_claim": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "precheck_id": "PRE1328_4_parent_basis_map",
            "target": "MTS parent map from source weights to external component charges",
            "status": "MISSING_PARENT_MAP",
            "details": "DD/SEMF-style rows can be comparator inputs only until the parent action signs the basis map",
            "blocks_claim": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    edge_lookup = {row["edge_id"]: row for row in edge_rows}
    graph_reentry = [
        {
            "edge_id": "EDGE1232_0_electron_photon",
            "route": "EM/current edge owner",
            "latest_status": edge_lookup.get("EDGE1232_0_electron_photon", {}).get("new_status", "MISSING_EDGE_ROW"),
            "best_reentry_clause": "derive unique parent EM owner/current normalization so electron source and photon/Coulomb source are one quotient-owned morphism",
            "missing_parent_signature": "unique F2/current owner; no hidden representative branch; readout branch silence",
            "would_close_if": "parent action signs EM current owner and forbids independent electron/photon source weights",
            "counts_for_connected_graph": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "edge_id": "EDGE1232_1_quark_photon",
            "route": "charge assignment edge owner",
            "latest_status": edge_lookup.get("EDGE1232_1_quark_photon", {}).get("new_status", "MISSING_EDGE_ROW"),
            "best_reentry_clause": "derive quark electric charge assignment as part of same parent current functor rather than imported Standard Model bookkeeping",
            "missing_parent_signature": "charge lattice/current functor owner; EM normalization; confinement-to-hadron transfer",
            "would_close_if": "quark charge and photon current are parent-derived in the same source functor",
            "counts_for_connected_graph": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "edge_id": "EDGE1232_2_quark_gluon",
            "route": "QCD/color edge owner",
            "latest_status": edge_lookup.get("EDGE1232_2_quark_gluon", {}).get("new_status", "MISSING_EDGE_ROW"),
            "best_reentry_clause": "derive bound-state QCD source-label forgetting, so light-quark and gluon residual weights cannot vary independently in ordinary matter",
            "missing_parent_signature": "color current owner; bound-state transfer; residual no-double-counting rule",
            "would_close_if": "parent action signs color-source owner and unique mass-budget residual map",
            "counts_for_connected_graph": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "edge_id": "EDGE1328_3_readout_matter",
            "route": "measure/readout owner",
            "latest_status": "REENTRY_STAGED_NOT_SIGNED",
            "best_reentry_clause": "derive the source-worldtube/readout projection so measured differential acceleration is not an independent source-weight component",
            "missing_parent_signature": "accelerometer/readout projection; local source worldtube; tau_WEP normalization",
            "would_close_if": "readout residual is shown to descend from the same parent matter/source action",
            "counts_for_connected_graph": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner = [
        {
            "runner_id": "RUN1328_0_source_acquisition",
            "target": "finite Delta_w_TiPt component branch",
            "input_status": "SOURCE_CANDIDATES_STAGED_NO_NUMERIC_EXTRACTION",
            "runner_status": "REFUSED_NOT_SCOREABLE",
            "reason": "candidate URLs and formula contracts exist, but no accepted numeric component rows and no parent basis map",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN1328_1_graph_reentry",
            "target": "Delta_w_TiPt=0 via parent interaction graph",
            "input_status": "EDGE_OWNER_BLOCKERS_NARROWED",
            "runner_status": "REFUSED_NO_CONNECTED_GRAPH",
            "reason": "electron-photon, quark-photon, quark-gluon, and readout-matter edges are not parent-signed",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    anti_shortcut = [
        {
            "gate_id": "SHORT1328_0_no_source_url_as_fraction",
            "shortcut": "treat source candidate URL as component fraction evidence",
            "enforcement": "REFUSED",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1328_1_no_external_DD_as_parent_MTS",
            "shortcut": "use Damour-Donoghue charges as if they are derived MTS source weights",
            "enforcement": "REFUSED until parent basis map is derived",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1328_2_no_placeholder_raw_rows",
            "shortcut": "put MISSING_NUMERIC_EXTRACTION rows in raw validator intake",
            "enforcement": "candidate pack is written to docs only",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1328_3_no_template_edge_count",
            "shortcut": "count ordinary-matter template edges as graph proof",
            "enforcement": "REFUSED by graph reentry blockers",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1328_4_no_local_GR_claim",
            "shortcut": "promote source acquisition to WEP/local-GR pass",
            "enforcement": "REFUSED",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1328_0_best_route",
            "decision": "take the source-acquisition route first",
            "because": "electron fraction and material/isotope data are lower scrutiny than forcing a parent graph proof immediately",
            "effect": "stage source URLs and formula contracts, but keep all rows nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1328_1_graph_route",
            "decision": "keep graph route alive but narrowed",
            "because": "a true parent connectedness proof would be stronger than a component fit, but current EM/QCD/readout owners remain unsigned",
            "effect": "edge owner reentry blockers are explicit; no connected edge counts",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1328_0_1329",
            "target_file": "1329-Y5-R10-RAB-electron-fraction-extractor-dryrun-or-DD-basis-map-demotion.md",
            "target_script": "scripts/Y5_R10_RAB_electron_fraction_extractor_dryrun_or_DD_basis_map_demotion.py",
            "task": "do the first bounded numeric nonclaim dry-run for the electron fraction from material/isotope/mass sources, while demoting DD rows unless a parent basis map is derived",
            "success_condition": "electron rows become sourced numeric dry-run rows with uncertainty/provenance but still valid_for_claim=false, or the extractor records the exact source blocker",
            "do_not": "do not score WEP, do not use DD as parent MTS, do not put placeholders in raw, and do not claim Delta_w=0 or local GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    tables_for_nonclaim = [
        source_register,
        public_sources,
        route_matrix,
        candidate_pack,
        formula_contract,
        acceptance_precheck,
        graph_reentry,
        runner,
        anti_shortcut,
        decision,
        next_target,
    ]

    source_anchor_count = sum(1 for row in source_register if row["exists"] and row["needle_found"])
    public_sources_present = all(str(row["url_or_doi"]).startswith("https://") for row in public_sources)
    route_covers_components = len(route_matrix) == 12 and sorted({row["component_id"] for row in route_matrix}) == [
        "EM_Coulomb",
        "QCD_gluon",
        "electron",
        "light_quark",
        "measure_readout",
        "nuclear_surface",
    ]
    no_raw_candidate = len(raw_1328_candidates()) == 0
    dryrun_zero = dryrun.get("accepted_rows") == "0" and dryrun.get("status") == "NO_CANDIDATE_FILES_PRESENT"
    no_edges_count = all(is_false(row["counts_for_connected_graph"]) for row in graph_reentry)
    runner_refuses = all(str(row["runner_status"]).startswith("REFUSED") for row in runner)
    shortcuts_enforced = all(row["status"] == "ENFORCED" for row in anti_shortcut)
    nonclaim = all_nonclaim(tables_for_nonclaim)
    formal_clean = len(generated_inside_formalization()) == 0
    next_is_1329 = next_target[0]["target_file"].startswith("1329-")

    validations = [
        validation_row(
            "VAL1328_0_sources_exist",
            "registered local source paths exist and anchors are found",
            source_anchor_count == len(source_register),
            f"{source_anchor_count}/{len(source_register)} source anchors found",
        ),
        validation_row(
            "VAL1328_1_public_sources_staged",
            "public source candidate rows have URL/DOI provenance",
            public_sources_present and len(public_sources) >= 7,
            f"public_source_rows={len(public_sources)}",
        ),
        validation_row(
            "VAL1328_2_route_matrix_coverage",
            "component source route matrix covers six components for both materials",
            route_covers_components,
            f"route_rows={len(route_matrix)}",
        ),
        validation_row(
            "VAL1328_3_no_raw_placeholders",
            "placeholder candidate rows are not placed in raw validator intake",
            no_raw_candidate,
            f"raw_1328_candidate_files={len(raw_1328_candidates())};candidate_pack=docs",
        ),
        validation_row(
            "VAL1328_4_existing_validator_zero",
            "existing component validator remains at zero accepted rows",
            dryrun_zero,
            f"dryrun_status={dryrun.get('status', 'MISSING')};accepted_rows={dryrun.get('accepted_rows', 'MISSING')}",
        ),
        validation_row(
            "VAL1328_5_graph_edges_refused",
            "graph edge owner reentry records no connected graph edge counts",
            no_edges_count,
            ";".join(f"{row['edge_id']}={row['latest_status']}" for row in graph_reentry),
        ),
        validation_row(
            "VAL1328_6_runner_refuses",
            "Delta_w runner remains refused for source and graph routes",
            runner_refuses,
            ";".join(f"{row['runner_id']}={row['runner_status']}" for row in runner),
        ),
        validation_row(
            "VAL1328_7_shortcuts_enforced",
            "anti-shortcut gates are enforced",
            shortcuts_enforced,
            ";".join(row["gate_id"] for row in anti_shortcut),
        ),
        validation_row(
            "VAL1328_8_nonclaim_policy",
            "all generated rows remain nonclaim",
            nonclaim,
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        ),
        validation_row(
            "VAL1328_9_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            formal_clean,
            f"formalization_generated_output_count={len(generated_inside_formalization())}",
        ),
        validation_row(
            "VAL1328_10_next_target_1329",
            "next target routes to electron fraction extractor or DD basis demotion",
            next_is_1329,
            str(next_target[0]["target_file"]),
        ),
    ]
    validations.append(
        validation_row(
            "VAL1328_11_overall",
            "overall 1328 validation",
            all(row["status"] == "PASS" for row in validations),
            "1328 stages source acquisition and narrows graph reentry while preserving nonclaim gates",
        )
    )

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(PUBLIC_SOURCE_PATH, public_sources)
    write_csv(ROUTE_MATRIX_PATH, route_matrix)
    write_csv(COMPONENT_CANDIDATE_PACK_PATH, candidate_pack)
    write_csv(FORMULA_CONTRACT_PATH, formula_contract)
    write_csv(ACCEPTANCE_PRECHECK_PATH, acceptance_precheck)
    write_csv(GRAPH_REENTRY_PATH, graph_reentry)
    write_csv(RUNNER_PATH, runner)
    write_csv(ANTI_SHORTCUT_PATH, anti_shortcut)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# {TITLE}

**Current verdict:** 1328 does not produce a WEP, `Delta_w=0`, or local-GR claim. It does make the next route less blurry: real source candidates are now staged for component fractions, and the graph route is narrowed to the exact unsigned EM/QCD/readout owner clauses.

**Main progress:** the lowest-scrutiny branch is now the electron-fraction extractor dry-run: material composition, isotope/mass tables, and formula convention can be attacked directly before touching the harder DD/QCD parent-basis map.

**Decision:** keep Damour-Donoghue-style charges as external comparator rows only unless a parent MTS basis map is derived. Do not let an external phenomenology shortcut masquerade as a parent action derivation.

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Public Source Candidate Register
{markdown_table(public_sources, ["public_source_id", "target", "url_or_doi", "usable_for", "extraction_plan", "source_status", "confidence", "valid_for_claim", "claim_allowed"])}

## Component Source Route Matrix
{markdown_table(route_matrix, ["route_id", "material_id", "component_id", "source_candidate_ids", "candidate_formula", "parent_gap", "current_status", "candidate_pack_location", "raw_candidate_created", "valid_for_claim", "claim_allowed"])}

## Component Candidate Pack
Candidate pack written outside the raw validator intake:

`{COMPONENT_CANDIDATE_PACK_PATH}`

{markdown_table(candidate_pack, ["row_id", "material_id", "component_id", "fraction_value", "fraction_uncertainty", "basis_convention", "source_path_or_url", "extraction_method", "status", "valid_for_claim", "claim_allowed"])}

## Extraction Formula Contract
{markdown_table(formula_contract, ["formula_id", "component_id", "symbolic_contract", "minimum_inputs", "source_candidates", "current_blocker", "output_allowed", "valid_for_claim", "claim_allowed"])}

## Component Fraction Acceptance Precheck
{markdown_table(acceptance_precheck, ["precheck_id", "target", "status", "details", "blocks_claim", "valid_for_claim", "claim_allowed"])}

## Graph Edge Owner Reentry Blockers
{markdown_table(graph_reentry, ["edge_id", "route", "latest_status", "best_reentry_clause", "missing_parent_signature", "would_close_if", "counts_for_connected_graph", "valid_for_claim", "claim_allowed"])}

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
    print(f"Wrote component candidate pack {COMPONENT_CANDIDATE_PACK_PATH}")


if __name__ == "__main__":
    main()
