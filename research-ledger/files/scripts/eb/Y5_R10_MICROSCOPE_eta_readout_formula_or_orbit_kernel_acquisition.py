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
DOC = ROOT / "1070-Y5-R10-MICROSCOPE-eta-readout-formula-or-orbit-kernel-acquisition.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1070-MICROSCOPE-eta-readout-or-orbit-kernel" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_R10_1070_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1070_WEP_BOUND_IMPORT.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def source_path(path_text: str) -> Path:
    candidate = Path(path_text)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


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
        ("SRC1070_0_1069_next", "source-intake/mts_residuals/P8_Y5_R10_1069_NEXT_TARGET.csv", "1070-Y5-R10-MICROSCOPE-eta-readout-formula", "1069 handoff selecting eta/readout acquisition."),
        ("SRC1070_1_1069_first_tau", "source-intake/mts_residuals/P8_Y5_R10_1069_FIRST_REAL_TAU_SOURCE_ROW.csv", "WTS1069_0_MICROSCOPE_eta_source_charge_proxy", "first source-backed WEP bound/readout anchor."),
        ("SRC1070_2_1069_provenance", "source-intake/mts_residuals/P8_Y5_R10_1069_MICROSCOPE_PROVENANCE_LEDGER.csv", "PROV1069_0_R1_source_charge", "MICROSCOPE provenance ledger."),
        ("SRC1070_3_1069_fill", "source-intake/mts_residuals/P8_Y5_R10_1069_READOUT_FILL_MATRIX.csv", "RFM1069_1_eta_formula", "eta formula remained partial in 1069."),
        ("SRC1070_4_1069_requirements", "source-intake/mts_residuals/P8_Y5_R10_1069_REMAINING_TAU_REQUIREMENTS.csv", "REQ1069_1_readout_formula", "remaining tau/readout requirements."),
        ("SRC1070_5_1068_orbit", "source-intake/mts_residuals/P8_Y5_R10_1068_MICROSCOPE_ORBIT_READOUT_REQUIREMENTS.csv", "ORB1068_2_eta_convention", "MICROSCOPE orbit/readout requirements."),
        ("SRC1070_6_1068_force", "source-intake/mts_residuals/P8_Y5_R10_1068_OBSERVED_FRAME_FORCE_MAP.csv", "FRM1068_1_eta_mapping", "observed-frame eta map requirement."),
        ("SRC1070_7_1068_tau_pack", "source-intake/mts_residuals/P8_Y5_R10_1068_TAU_WEP_ACQUISITION_PACK.csv", "TAP1068_1_orbit_average", "tau_WEP acquisition pack."),
        ("SRC1070_8_1068_worldtube", "source-intake/mts_residuals/P8_Y5_R10_1068_SOURCE_WORLDTUBE_REQUIREMENTS.csv", "SWT1068_5_verdict", "source worldtube gap."),
        ("SRC1070_9_1061_material", "source-intake/mts_residuals/P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv", "MCON1061_0_test_pair", "Ti/Pt material convention."),
        ("SRC1070_10_local_bounds", "source-intake/local_bounds/local_bound_claims.csv", "R1_WEP_source_charge", "local MICROSCOPE bound source rows."),
        ("SRC1070_11_708_wep", "source-intake/mts_residuals/P8_Y5_R10_708_PPN_GDOT_WEP_MAP.csv", "PGW708_0_R1_WEP", "WEP source/test charge vector gap."),
        ("SRC1070_12_1062_parent", "source-intake/mts_residuals/P8_Y5_R10_1062_PARENT_PRODUCT_THEOREM_ATTEMPT.csv", "THM1062_4_tau_WEP_projection", "prior parent product theorem blocker."),
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


def external_source_rows() -> list[dict[str, str]]:
    arxiv_cqg = "https://arxiv.org/abs/2209.15488"
    pdf_cqg = "https://elib.dlr.de/193667/2/Touboul_2022_Class._Quantum_Grav._39_204009.pdf"
    arxiv_prl = "https://arxiv.org/abs/2209.15487"
    return [
        {
            "external_id": "EXT1070_0_CQG_eta_formula",
            "title": "Result of the MICROSCOPE Weak Equivalence Principle test",
            "url": arxiv_cqg,
            "pdf_url": pdf_cqg,
            "doi": "10.1088/1361-6382/ac84be",
            "paper_year": "2022",
            "source_lines": "arXiv abstract; DLR/IOP PDF front matter",
            "extracted_item": "eta(A,B)=2(a_A-a_B)/(a_A+a_B)",
            "extraction_method": "text source; formula transcription",
            "confidence": "high",
            "source_backed": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "external_id": "EXT1070_1_CQG_result_readout",
            "title": "MICROSCOPE final readout convention",
            "url": arxiv_cqg,
            "pdf_url": pdf_cqg,
            "doi": "10.1088/1361-6382/ac84be",
            "paper_year": "2022",
            "source_lines": "PDF lines 1216-1223",
            "extracted_item": "eta(Ti,Pt) is identified with delta_x; final value is [-1.5 +/- 2.3(stat) +/- 1.5(syst)]e-15",
            "extraction_method": "text source; result transcription",
            "confidence": "high",
            "source_backed": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "external_id": "EXT1070_2_CQG_measurement_axis",
            "title": "MICROSCOPE acceleration readout axis",
            "url": arxiv_cqg,
            "pdf_url": pdf_cqg,
            "doi": "10.1088/1361-6382/ac84be",
            "paper_year": "2022",
            "source_lines": "PDF lines 341-346",
            "extracted_item": "test-mass accelerations are sampled at 4 Hz and the differential acceleration is computed along the sensitive X axis",
            "extraction_method": "text source; readout metadata",
            "confidence": "high",
            "source_backed": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "external_id": "EXT1070_3_CQG_orbit_segments",
            "title": "MICROSCOPE orbit/segment exposure",
            "url": arxiv_cqg,
            "pdf_url": pdf_cqg,
            "doi": "10.1088/1361-6382/ac84be",
            "paper_year": "2022",
            "source_lines": "PDF lines 1226-1231",
            "extracted_item": "SUREF Pt/Pt used 13 segments/598 orbits/41 days; SUEP Pt/Ti used 19 segments/1362 orbits/94 days",
            "extraction_method": "text source; orbit/segment metadata",
            "confidence": "high",
            "source_backed": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "external_id": "EXT1070_4_CQG_analysis_band",
            "title": "MICROSCOPE analysis frequency bands",
            "url": arxiv_cqg,
            "pdf_url": pdf_cqg,
            "doi": "10.1088/1361-6382/ac84be",
            "paper_year": "2022",
            "source_lines": "PDF lines 918-924",
            "extracted_item": "parameter estimation uses bands around f_EP and 2 f_EP; a wider-domain check increases uncertainty but does not noticeably shift parameters",
            "extraction_method": "text source; analysis-kernel metadata",
            "confidence": "medium_high",
            "source_backed": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "external_id": "EXT1070_5_CQG_data_availability",
            "title": "MICROSCOPE data portal statement",
            "url": arxiv_cqg,
            "pdf_url": pdf_cqg,
            "doi": "10.1088/1361-6382/ac84be",
            "paper_year": "2022",
            "source_lines": "PDF lines 1274-1276",
            "extracted_item": "science data are available from https://cmsm-ds.onera.fr/",
            "extraction_method": "text source; portal metadata",
            "confidence": "high",
            "source_backed": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "external_id": "EXT1070_6_PRL_eta_bound_anchor",
            "title": "MICROSCOPE final results",
            "url": arxiv_prl,
            "pdf_url": "",
            "doi": "10.1103/PhysRevLett.129.121102",
            "paper_year": "2022",
            "source_lines": "PRL/arXiv abstract and 1069 local bound row",
            "extracted_item": "Ti/Pt final result supplies the source-backed 2.8e-15 WEP bound anchor already imported in 1069",
            "extraction_method": "text source plus local bound row",
            "confidence": "high",
            "source_backed": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def eta_readout_rows() -> list[dict[str, str]]:
    r0 = local_bound_row("R0_identity_coframe_direct")
    r1 = local_bound_row("R1_WEP_source_charge")
    return [
        {
            "eta_id": "ETA1070_0_formula",
            "formula_or_item": "eta_AB = 2(a_A-a_B)/(a_A+a_B)",
            "units": "dimensionless",
            "source_id": "EXT1070_0_CQG_eta_formula",
            "status": "SOURCE_BACKED_FORMULA_FILLED",
            "filled_prior_gap": "RFM1069_1_eta_formula",
            "MTS_impact": "observable convention acquired; not a tau_WEP prediction",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "eta_id": "ETA1070_1_delta_x_identification",
            "formula_or_item": "eta(Ti,Pt) approximately equals measured delta_x in the MICROSCOPE convention",
            "units": "dimensionless",
            "source_id": "EXT1070_1_CQG_result_readout",
            "status": "SOURCE_BACKED_READOUT_IDENTIFICATION_FILLED",
            "filled_prior_gap": "eta_to_delta_x readout link",
            "MTS_impact": "links the official eta observable to the instrument differential channel",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "eta_id": "ETA1070_2_result_value",
            "formula_or_item": f"Ti/Pt eta measured={r1['measured_value']}; one_sigma={r1['one_sigma']}; upper_bound={r1['upper_bound']}",
            "units": r1["units"],
            "source_id": "EXT1070_6_PRL_eta_bound_anchor; source-intake/local_bounds/local_bound_claims.csv::R1_WEP_source_charge",
            "status": "SOURCE_BACKED_RESULT_CONTEXT_FILLED",
            "filled_prior_gap": "R1 source-charge proxy bound anchor",
            "MTS_impact": f"bound row remains a nonclaim comparator; direct row {r0['row_id']} remains separate",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "eta_id": "ETA1070_3_sign_pair_convention",
            "formula_or_item": "A/B sign is source-backed for eta_AB, but not yet mapped onto MTS TA6V_minus_PtRh10 sign convention",
            "units": "dimensionless",
            "source_id": "EXT1070_0_CQG_eta_formula; source-intake/mts_residuals/P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv",
            "status": "PARTIAL_SIGN_CONTEXT_ONLY",
            "filled_prior_gap": "sign convention partially filled",
            "MTS_impact": "absolute-value score can use the bound, but signed model comparison still needs material/readout orientation",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "eta_id": "ETA1070_4_verdict",
            "formula_or_item": "eta formula and delta_x readout are filled; tau_WEP and direct product are not",
            "units": "dimensionless",
            "source_id": "ETA1070_0_formula; ETA1070_1_delta_x_identification",
            "status": "FORMULA_FILLED_NOT_TAU",
            "filled_prior_gap": "readout formula only",
            "MTS_impact": "this upgrades data plumbing, not local-GR/WEP closure",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def orbit_kernel_rows() -> list[dict[str, str]]:
    return [
        {
            "orbit_id": "ORK1070_0_sampling_axis",
            "component": "sample/readout axis",
            "source_id": "EXT1070_2_CQG_measurement_axis",
            "source_backed_value": "4 Hz acceleration sampling; differential acceleration along sensitive X axis",
            "units": "Hz; axis_label",
            "status": "SOURCE_BACKED_PARTIAL_READOUT_ROW",
            "missing_for_tau": "full map from parent residual to X-axis eta channel",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "orbit_id": "ORK1070_1_segments_orbits",
            "component": "segment/orbit exposure",
            "source_id": "EXT1070_3_CQG_orbit_segments",
            "source_backed_value": "SUEP Pt/Ti 19 segments, 1362 orbits, 94 days; SUREF Pt/Pt 13 segments, 598 orbits, 41 days",
            "units": "count; orbit; day",
            "status": "SOURCE_BACKED_PARTIAL_ORBIT_ROW",
            "missing_for_tau": "time-dependent orbit/attitude weights and source line-of-sight kernel",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "orbit_id": "ORK1070_2_spin_session",
            "component": "spin/session planning",
            "source_id": "EXT1070_4_CQG_analysis_band",
            "source_backed_value": "analysis is organized around f_EP and 2f_EP bands; earlier session metadata references V2/V3 spin rates and long sessions",
            "units": "frequency-band metadata",
            "status": "SOURCE_BACKED_PARTIAL_SPIN_ROW",
            "missing_for_tau": "machine-readable attitude/spin kernel",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "orbit_id": "ORK1070_3_frequency_band",
            "component": "frequency-domain analysis band",
            "source_id": "EXT1070_4_CQG_analysis_band",
            "source_backed_value": "fit bands around f_EP and 2f_EP",
            "units": "frequency-band metadata",
            "status": "SOURCE_BACKED_PARTIAL_ANALYSIS_KERNEL",
            "missing_for_tau": "exact weighting/filter operator for an MTS predicted signal",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "orbit_id": "ORK1070_4_data_availability",
            "component": "data portal",
            "source_id": "EXT1070_5_CQG_data_availability",
            "source_backed_value": "https://cmsm-ds.onera.fr/",
            "units": "url",
            "status": "SOURCE_BACKED_DATA_PORTAL",
            "missing_for_tau": "downloaded data products, schema, and reproducible kernel extraction",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "orbit_id": "ORK1070_5_verdict",
            "component": "orbit/averaging kernel verdict",
            "source_id": "ORK1070_0_sampling_axis; ORK1070_1_segments_orbits; ORK1070_3_frequency_band",
            "source_backed_value": "partial metadata acquired, not a full orbit/attitude/averaging kernel",
            "units": "not_applicable",
            "status": "PARTIAL_ORBIT_METADATA_NOT_TAU_KERNEL",
            "missing_for_tau": "full kernel or source-worldtube row",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def fill_matrix_rows() -> list[dict[str, str]]:
    return [
        {
            "fill_id": "RFM1070_0_eta_bound",
            "component": "MICROSCOPE eta bound",
            "prior_status": "FILLED_IN_1069",
            "current_status": "SOURCE_BACKED_BOUND_ANCHOR_PRESENT",
            "evidence_rows": "WTS1069_0; ETA1070_2",
            "blocks_claim": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "fill_id": "RFM1070_1_eta_formula",
            "component": "eta_AB formula",
            "prior_status": "PARTIAL",
            "current_status": "SOURCE_BACKED_FORMULA_FILLED",
            "evidence_rows": "ETA1070_0",
            "blocks_claim": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "fill_id": "RFM1070_2_delta_x",
            "component": "eta to delta_x readout identification",
            "prior_status": "MISSING_OR_IMPLICIT",
            "current_status": "SOURCE_BACKED_READOUT_IDENTIFICATION_FILLED",
            "evidence_rows": "ETA1070_1",
            "blocks_claim": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "fill_id": "RFM1070_3_sampling_axis",
            "component": "4 Hz X-axis measurement row",
            "prior_status": "MISSING",
            "current_status": "SOURCE_BACKED_PARTIAL_READOUT_ROW",
            "evidence_rows": "ORK1070_0",
            "blocks_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "fill_id": "RFM1070_4_orbit_metadata",
            "component": "orbit/segment metadata",
            "prior_status": "MISSING",
            "current_status": "SOURCE_BACKED_PARTIAL_ORBIT_ROW",
            "evidence_rows": "ORK1070_1; ORK1070_3",
            "blocks_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "fill_id": "RFM1070_5_full_orbit_kernel",
            "component": "full orbit/attitude/averaging kernel",
            "prior_status": "MISSING",
            "current_status": "MISSING_FULL_KERNEL",
            "evidence_rows": "none",
            "blocks_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "fill_id": "RFM1070_6_source_worldtube",
            "component": "Earth/source worldtube",
            "prior_status": "MISSING",
            "current_status": "MISSING_SOURCE_WORLDTUBE",
            "evidence_rows": "SWT1068_5_verdict",
            "blocks_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "fill_id": "RFM1070_7_material_tensor",
            "component": "Ti/Pt material response tensor",
            "prior_status": "PAIR_CONTEXT_ONLY",
            "current_status": "MISSING_MATERIAL_TENSOR",
            "evidence_rows": "MCON1061_0_test_pair",
            "blocks_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "fill_id": "RFM1070_8_direct_product",
            "component": "direct P_WEP product",
            "prior_status": "MISSING",
            "current_status": "MISSING_DIRECT_PRODUCT_OR_TAU_WEP_KERNEL",
            "evidence_rows": "THM1062_4_tau_WEP_projection",
            "blocks_claim": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def tau_impact_rows() -> list[dict[str, str]]:
    return [
        {
            "impact_id": "TAI1070_0_formula_does_not_define_tau",
            "new_input": "eta_AB formula",
            "impact": "defines the observable normalization only",
            "remaining_gap": "tau_WEP/source product still absent",
            "claim_policy": "no scoreable MTS prediction",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "impact_id": "TAI1070_1_readout_axis_partial",
            "new_input": "4 Hz X-axis readout row",
            "impact": "constrains the observed channel",
            "remaining_gap": "no parent residual to X-axis projection operator",
            "claim_policy": "partial kernel only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "impact_id": "TAI1070_2_orbit_partial",
            "new_input": "segment/orbit/frequency metadata",
            "impact": "identifies exposure and analysis bands",
            "remaining_gap": "no machine-readable orbit/attitude/averaging kernel",
            "claim_policy": "partial source-backed acquisition",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "impact_id": "TAI1070_3_no_unity_shortcut",
            "new_input": "bound plus formula",
            "impact": "does not license tau_WEP=1 or Delta_w=0",
            "remaining_gap": "direct product theorem or full projection kernel",
            "claim_policy": "shortcut forbidden",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "impact_id": "TAI1070_4_verdict",
            "new_input": "1070 acquisition pack",
            "impact": "readout plumbing improved",
            "remaining_gap": "tau_WEP remains missing",
            "claim_policy": "WEP/local-GR claim remains blocked",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def product_prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1070_0_WEP_eta_formula_or_orbit_kernel_product",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_DIRECT_PRODUCT_OR_TAU_WEP_KERNEL",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1070_ETA_READOUT_FORMULA_ROWS.csv",
            "inputs_present": "eta_formula;delta_x_identification;R1_bound;4Hz_X_axis_row;segment_orbit_metadata",
            "required_inputs": "direct parent product OR source worldtube+full orbit/attitude/averaging kernel+material tensor+Xhat normalization",
            "derivation_status": "MISSING_DIRECT_PRODUCT_OR_TAU_WEP_KERNEL",
            "valid_for_claim": "false",
            "notes": "eta/readout formula is sourced, but this is not a numeric MTS prediction",
        }
    ]


def bound_rows() -> list[dict[str, str]]:
    row = local_bound_row("R1_WEP_source_charge")
    url, doi = split_reference(row["reference_path_or_url"])
    return [
        {
            "bound_id": "BOUND1070_0_MICROSCOPE_R1_eta_source_charge",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "bound_value": row["upper_bound"],
            "bound_units": row["units"],
            "bound_source": url,
            "source_row": f"source-intake/local_bounds/local_bound_claims.csv::{row['row_id']}; doi:{doi}",
            "bound_type": "source_backed_upper_bound_anchor",
            "valid_for_claim": "true",
            "notes": "valid bound anchor only; no MTS prediction row is valid yet",
        }
    ]


def product_status_rows(status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "runner_id": "APR1070_0_WEP_product_stub",
            "prediction_rows": str(status.get("prediction_rows", "")),
            "bound_rows": str(status.get("bound_rows", "")),
            "valid_prediction_rows": str(status.get("valid_prediction_rows", "")),
            "valid_bound_rows": str(status.get("valid_bound_rows", "")),
            "comparison_rows": str(status.get("comparison_rows", "")),
            "passed_rows": str(status.get("passed_rows", "")),
            "claim_allowed": str(status.get("claim_allowed", "")).lower(),
            "expected_result": "reject eta/readout-only placeholder prediction and keep claim false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def claim_gate_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1070_0_eta_formula_acquired",
            "claim_component": "eta formula",
            "gate_pass": "true",
            "claim_allowed": "false",
            "reason": "source-backed observable definition, not an MTS prediction",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1070_1_orbit_metadata_partial",
            "claim_component": "orbit/readout metadata",
            "gate_pass": "true",
            "claim_allowed": "false",
            "reason": "partial metadata only; full kernel missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1070_2_full_orbit_kernel",
            "claim_component": "full orbit/attitude/averaging kernel",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "MISSING_FULL_KERNEL",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1070_3_tau_WEP_numeric",
            "claim_component": "tau_WEP numeric/direct product",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "MISSING_DIRECT_PRODUCT_OR_TAU_WEP_KERNEL",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1070_4_product_runner",
            "claim_component": "WEP product runner",
            "gate_pass": "false",
            "claim_allowed": str(product_status.get("claim_allowed", "")).lower(),
            "reason": f"valid_prediction_rows={product_status.get('valid_prediction_rows')}",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1070_5_local_GR_WEP_claim",
            "claim_component": "local-GR/WEP pass",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "eta formula acquired but WEP product remains unscored",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1070_0_readout_acquired",
            "decision": "eta formula and delta_x identification are now source-backed nonclaim rows",
            "evidence": "ETA1070_0_formula; ETA1070_1_delta_x_identification",
            "consequence": "readout convention no longer the first blocker",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1070_1_orbit_partial_only",
            "decision": "orbit/readout metadata is useful but not a tau kernel",
            "evidence": "ORK1070_5_verdict",
            "consequence": "do not score MTS against MICROSCOPE yet",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1070_2_best_next",
            "decision": "move to full orbit kernel or source-worldtube acquisition",
            "evidence": "RFM1070_5_full_orbit_kernel; RFM1070_6_source_worldtube",
            "consequence": "1071 should try the first tau_WEP projection component",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1070_0_1071",
            "next_target": "1071-Y5-R10-MICROSCOPE-full-orbit-kernel-or-source-worldtube-row.md",
            "objective": "acquire or derive the first full tau_WEP projection component: either an official MICROSCOPE orbit/attitude/averaging kernel usable in the eta readout map, or an Earth/source-worldtube row; keep product scoring blocked until all required tau/direct-product components exist.",
            "include": "orbit ephemeris/attitude/averaging kernel; source worldtube profile; eta formula integration; material tensor; Xhat normalization; URL/DOI/data portal provenance; refusal gates",
            "exclude": "tau=1; Delta_w=0 by taste; measured-G absorption of relative weights; cancellation; public WEP/local-GR claim; GitHub; formalization edits",
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
    external_rows: list[dict[str, str]],
    eta_rows: list[dict[str, str]],
    orbit_rows: list[dict[str, str]],
    fill_rows: list[dict[str, str]],
    tau_rows: list[dict[str, str]],
    prediction_rows: list[dict[str, str]],
    bound_rows_: list[dict[str, str]],
    product_status: dict[str, Any],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V1070_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in source_rows), "all cited local paths and needles are present"))
    checks.append(("V1070_1_external_provenance", any(row["doi"] == "10.1088/1361-6382/ac84be" for row in external_rows) and any("cmsm-ds.onera.fr" in row["extracted_item"] for row in external_rows), "CQG DOI and data portal recorded"))
    checks.append(("V1070_2_eta_formula_dimensionless", any(row["eta_id"] == "ETA1070_0_formula" and row["units"] == "dimensionless" and row["status"] == "SOURCE_BACKED_FORMULA_FILLED" for row in eta_rows), "eta formula filled as dimensionless"))
    checks.append(("V1070_3_bound_numeric", bool(bound_rows_) and float(bound_rows_[0]["bound_value"]) > 0 and bound_rows_[0]["valid_for_claim"] == "true", "bound import has positive numeric value"))
    checks.append(("V1070_4_orbit_partial_not_kernel", any(row["orbit_id"] == "ORK1070_5_verdict" and row["status"] == "PARTIAL_ORBIT_METADATA_NOT_TAU_KERNEL" for row in orbit_rows), "orbit acquisition remains partial"))
    checks.append(("V1070_5_full_kernel_still_missing", any(row["fill_id"] == "RFM1070_5_full_orbit_kernel" and row["current_status"] == "MISSING_FULL_KERNEL" for row in fill_rows), "full kernel is not silently filled"))
    checks.append(("V1070_6_tau_still_missing", any(row["impact_id"] == "TAI1070_4_verdict" and "tau_WEP remains missing" in row["remaining_gap"] for row in tau_rows), "tau verdict remains blocked"))
    checks.append(("V1070_7_prediction_nonclaim_missing", any("MISSING_DIRECT_PRODUCT_OR_TAU_WEP_KERNEL" in row["product_value"] and row["valid_for_claim"] == "false" for row in prediction_rows), "prediction row stays nonclaim and missing"))
    checks.append(("V1070_8_runner_refuses", product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False, "runner reports no valid prediction rows and claim false"))
    checks.append(("V1070_9_claim_gates_safe", all(row["claim_allowed"] == "false" for row in claim_rows), "all claim gates deny public/local-GR/WEP claim"))
    checks.append(("V1070_10_next_target", any("1071-Y5-R10-MICROSCOPE-full-orbit-kernel-or-source-worldtube-row.md" in row["next_target"] for row in next_rows), "1071 handoff written"))
    generated_paths = list(outputs.values()) + [DOC]
    checks.append(("V1070_11_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in generated_paths), "all generated outputs are under post-checkpoint-work"))
    csv_paths = [path for key, path in outputs.items() if key != "validation"]
    checks.append(("V1070_12_csv_parse", all(path.exists() and csv_rows_parse(path) for path in csv_paths), "all 1070 CSV outputs parse cleanly"))
    checks.append(("V1070_13_formalization_untouched", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains zero"))
    checks.append(("V1070_SUMMARY", True, "formula acquired; orbit metadata partial; tau/product claim blocked"))
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
    external_rows: list[dict[str, str]],
    eta_rows: list[dict[str, str]],
    orbit_rows: list[dict[str, str]],
    fill_rows: list[dict[str, str]],
    tau_rows: list[dict[str, str]],
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
            "# 1070 - MICROSCOPE eta readout formula or orbit-kernel acquisition",
            "",
            "## Current verdict",
            "1070 closes a real plumbing gap: the official MICROSCOPE eta definition and delta_x readout identification are now source-backed. It does **not** close the WEP/local-GR branch, because the full tau_WEP projection, source worldtube, material tensor, and direct parent product are still absent.",
            "",
            "## Local source register",
            md_table(source_rows, ["source_id", "relative_path", "exists", "needle_found", "note"]),
            "## External MICROSCOPE source ledger",
            md_table(external_rows, ["external_id", "doi", "source_lines", "extracted_item", "source_backed", "valid_for_claim"]),
            "## Eta readout rows",
            md_table(eta_rows, ["eta_id", "formula_or_item", "units", "status", "MTS_impact", "valid_for_claim"]),
            "## Orbit/readout kernel source rows",
            md_table(orbit_rows, ["orbit_id", "component", "source_backed_value", "status", "missing_for_tau", "valid_for_claim"]),
            "## Readout fill matrix update",
            md_table(fill_rows, ["fill_id", "component", "current_status", "evidence_rows", "blocks_claim"]),
            "## Tau impact ledger",
            md_table(tau_rows, ["impact_id", "new_input", "impact", "remaining_gap", "claim_policy"]),
            "## Nonclaim product candidate",
            md_table(prediction_rows, ["prediction_id", "arena", "product_symbol", "product_value", "derivation_status", "valid_for_claim"]),
            "## Bound import",
            md_table(bound_rows_, ["bound_id", "arena", "product_symbol", "bound_value", "bound_units", "bound_type", "valid_for_claim"]),
            "## Product runner status",
            md_table(product_status_rows_, ["runner_id", "prediction_rows", "bound_rows", "valid_prediction_rows", "valid_bound_rows", "claim_allowed", "expected_result"]),
            "## Product comparison rows",
            md_table(product_comparison_rows, ["comparison_id", "comparison_status", "pass_for_claim", "issues"]),
            "## Claim gates",
            md_table(claim_rows, ["gate_id", "claim_component", "gate_pass", "claim_allowed", "reason"]),
            "## Decision ledger",
            md_table(decisions, ["decision_id", "decision", "evidence", "consequence"]),
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
    external_rows = external_source_rows()
    eta_rows = eta_readout_rows()
    orbit_rows = orbit_kernel_rows()
    fill_rows = fill_matrix_rows()
    tau_rows = tau_impact_rows()
    prediction_rows = product_prediction_rows()
    bound_rows_ = bound_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R10_1070_SOURCE_REGISTER.csv",
        "external_ledger": OUT / "P8_Y5_R10_1070_EXTERNAL_MICROSCOPE_READOUT_SOURCE_LEDGER.csv",
        "eta_rows": OUT / "P8_Y5_R10_1070_ETA_READOUT_FORMULA_ROWS.csv",
        "orbit_rows": OUT / "P8_Y5_R10_1070_ORBIT_KERNEL_SOURCE_ROWS.csv",
        "fill_matrix": OUT / "P8_Y5_R10_1070_READOUT_FILL_MATRIX_UPDATE.csv",
        "tau_impact": OUT / "P8_Y5_R10_1070_TAU_IMPACT_LEDGER.csv",
        "prediction": PREDICTION_TEMPLATE,
        "bound": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_R10_1070_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_R10_1070_PRODUCT_COMPARISON_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_R10_1070_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1070_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1070_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1070_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["external_ledger"], external_rows)
    write_csv(outputs["eta_rows"], eta_rows)
    write_csv(outputs["orbit_rows"], orbit_rows)
    write_csv(outputs["fill_matrix"], fill_rows)
    write_csv(outputs["tau_impact"], tau_rows)
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
        external_rows,
        eta_rows,
        orbit_rows,
        fill_rows,
        tau_rows,
        prediction_rows,
        bound_rows_,
        product_status,
        claim_rows,
        next_rows,
    )
    write_csv(outputs["validation"], validation_rows)
    write_doc(
        source_rows,
        external_rows,
        eta_rows,
        orbit_rows,
        fill_rows,
        tau_rows,
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
