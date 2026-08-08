from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_DELTAW_OR_PPN_COMPONENT_OWNER_2320"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2320-Y5-R2FR-delta-w-material-source-vector-or-PPN-component-owner-row.md"

PATHS = {
    "2319_doc": ROOT / "2319-Y5-R2FR-first-source-backed-finite-coupling-row-balpha-clock-or-deltaw.md",
    "2319_validation": OUT / "P8_Y5_BRR545_2319_VALIDATION.csv",
    "2319_runner": OUT / "P8_Y5_PARENT_QLOC_2319_SOURCE_BACKED_FINITE_COUPLING_ROWS_NONCLAIM.csv",
    "2319_delta_w": OUT / "P8_Y5_PARENT_QLOC_2319_DELTA_W_ACQUISITION_STATUS.csv",
    "2319_ppn": OUT / "P8_Y5_PARENT_QLOC_2319_PPN_VECTOR_SOURCE_IMPORT.csv",
    "2201_matrix": OUT / "P8_Y5_PARENT_QLOC_2201_PPN_COMPONENT_OWNER_MATRIX.csv",
    "2201_alpha_source": OUT / "P8_Y5_PARENT_QLOC_2201_ALPHA_CG_SOURCE_ROW.csv",
    "2201_projection": OUT / "P8_Y5_PARENT_QLOC_2201_ALPHA_CG_PROJECTION_GATE.csv",
    "2201_claims": OUT / "P8_Y5_PARENT_QLOC_2201_CLAIM_GATE.csv",
    "2201_validation": OUT / "P8_Y5_BRR545_2201_VALIDATION.csv",
    "2202_projection": OUT / "P8_Y5_PARENT_QLOC_2202_ALPHA_CG_PROJECTION_ATTEMPT.csv",
    "2202_claims": OUT / "P8_Y5_PARENT_QLOC_2202_CLAIM_GATE.csv",
    "2202_validation": OUT / "P8_Y5_BRR545_2202_VALIDATION.csv",
    "1606_delta_schema": OUT / "P8_Y5_PARENT_QLOC_1606_DELTA_W_COMPONENT_BOUND_SCHEMA.csv",
    "1606_delta_pack": OUT / "P8_Y5_PARENT_QLOC_1606_DELTA_W_COMPONENT_BOUND_PACK.csv",
    "1606_delta_ready": OUT / "P8_Y5_PARENT_QLOC_1606_DELTA_W_SCORE_READINESS.csv",
    "1694_delta_rows": OUT / "P8_Y5_PARENT_QLOC_1694_SOURCE_BACKED_BETA_DELTAW_CURRENT_ROWS.csv",
    "1762_delta_interface": OUT / "P8_Y5_PARENT_QLOC_1762_DELTAW_BOUND_INTERFACE.csv",
    "1763_delta_acquisition": OUT / "P8_Y5_PARENT_QLOC_1763_DELTAW_SOURCE_ACQUISITION_LEDGER.csv",
}

SOURCES = [
    ("SRC2320_00_2319_doc", "2319_doc", PATHS["2319_doc"], ["NEXT2319_0", "delta-w-material-source-vector"], "2319 handoff to delta_w or PPN component owner"),
    ("SRC2320_01_2319_validation", "2319_validation", PATHS["2319_validation"], ["VAL2319_OVERALL", "PASS"], "2319 validation"),
    ("SRC2320_02_2319_runner", "2319_runner", PATHS["2319_runner"], ["FCR2319_1_ppn_vector_ceiling", "FCR2319_3_delta_w_missing_prediction"], "current finite-coupling runner rows"),
    ("SRC2320_03_2319_delta_w", "2319_delta_w", PATHS["2319_delta_w"], ["DW2319_1_MICROSCOPE", "COMPARATOR_BOUND_EXISTS_PREDICTION_MISSING"], "current delta_w acquisition status"),
    ("SRC2320_04_2319_ppn", "2319_ppn", PATHS["2319_ppn"], ["PPN2319_2_vector_contract", "NONCLAIM_VECTOR_TARGET"], "current PPN vector import"),
    ("SRC2320_05_2201_matrix", "2201_matrix", PATHS["2201_matrix"], ["PCM2201_0_alpha_cg", "True"], "PPN component owner matrix"),
    ("SRC2320_06_2201_alpha_source", "2201_alpha_source", PATHS["2201_alpha_source"], ["ACS2201_0_alpha_cg_target", "6.7e-05"], "alpha_cg source target"),
    ("SRC2320_07_2201_projection", "2201_projection", PATHS["2201_projection"], ["ACG2201_6_verdict", "BLOCKED_NONCLAIM_SOURCE_ROW_ONLY"], "alpha_cg projection blockers"),
    ("SRC2320_08_2201_claims", "2201_claims", PATHS["2201_claims"], ["CG2201_2_alpha_cg_prediction", "BLOCKED_NONCLAIM"], "2201 claim gates"),
    ("SRC2320_09_2201_validation", "2201_validation", PATHS["2201_validation"], ["VAL2201_03_alpha_source_row", "PASS"], "2201 validation"),
    ("SRC2320_10_2202_projection", "2202_projection", PATHS["2202_projection"], ["APA2202_6_verdict", "ALPHA_CG_PROJECTION_NOT_DERIVED"], "alpha_cg projection attempt"),
    ("SRC2320_11_2202_claims", "2202_claims", PATHS["2202_claims"], ["CG2202_1_alpha_prediction", "BLOCKED_NONCLAIM"], "2202 claim gates"),
    ("SRC2320_12_2202_validation", "2202_validation", PATHS["2202_validation"], ["VAL2202_OVERALL", "PASS"], "2202 validation"),
    ("SRC2320_13_1606_delta_schema", "1606_delta_schema", PATHS["1606_delta_schema"], ["DWS1606_1_quantity", "delta_w_e"], "delta_w component schema"),
    ("SRC2320_14_1606_delta_pack", "1606_delta_pack", PATHS["1606_delta_pack"], ["DWB1606_1_delta_w_e", "8.948213306283e-11"], "delta_w component pack"),
    ("SRC2320_15_1606_delta_ready", "1606_delta_ready", PATHS["1606_delta_ready"], ["READY1606_5_verdict", "False"], "delta_w score readiness"),
    ("SRC2320_16_1694_delta_rows", "1694_delta_rows", PATHS["1694_delta_rows"], ["BDW1694_0_MICROSCOPE_Delta_w_tau_bound_anchor", "2.8e-15"], "source-backed delta_w product anchor"),
    ("SRC2320_17_1762_delta_interface", "1762_delta_interface", PATHS["1762_delta_interface"], ["DW1762_1_delta_w_A", "MISSING_COMPONENT_BASIS_OR_THEOREM_ZERO"], "delta_w bound interface"),
    ("SRC2320_18_1763_delta_acquisition", "1763_delta_acquisition", PATHS["1763_delta_acquisition"], ["DWA1763_0_delta_w_species", "MISSING_HOM_SPECIES_EXCLUSION_OR_NUMERIC_BOUND"], "delta_w acquisition ledger"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2320_SOURCE_REGISTER.csv",
    "route": OUT / "P8_Y5_PARENT_QLOC_2320_ROUTE_SELECTION.csv",
    "ppn_import": OUT / "P8_Y5_PARENT_QLOC_2320_PPN_COMPONENT_OWNER_IMPORT.csv",
    "alpha_status": OUT / "P8_Y5_PARENT_QLOC_2320_ALPHA_CG_COMPONENT_STATUS.csv",
    "delta_status": OUT / "P8_Y5_PARENT_QLOC_2320_DELTAW_MATERIAL_SOURCE_VECTOR_STATUS.csv",
    "readiness": OUT / "P8_Y5_PARENT_QLOC_2320_LOCAL_GR_TEST_READINESS_MATRIX.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2320_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2320_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2320_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2320_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2320_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2320_0_ppn_import", OUTPUTS["ppn_import"], BETA_DOCS / "PPN_COMPONENT_OWNER_IMPORT_2320_NONCLAIM.csv"),
    ("COPY2320_1_alpha_status", OUTPUTS["alpha_status"], RAB_QUEUE / "JR2320_ALPHA_CG_COMPONENT_STATUS_NONCLAIM.csv"),
    ("COPY2320_2_delta_status", OUTPUTS["delta_status"], RAB_QUEUE / "JR2320_DELTAW_MATERIAL_SOURCE_VECTOR_STATUS_NONCLAIM.csv"),
    ("COPY2320_3_readiness", OUTPUTS["readiness"], MICRO_RESIDUALS / "local_gr_test_readiness_matrix_nonclaim_2320.csv"),
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def relative_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def needle_status(path: Path, needles: list[str]) -> tuple[bool, str]:
    if not path.exists():
        return False, "missing_file"
    text = read_text(path)
    missing_needles = [needle for needle in needles if needle not in text]
    if missing_needles:
        return False, "missing_needles=" + ";".join(missing_needles)
    return True, "all_needles_found"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
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
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ").replace("|", "\\|") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_sources() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, key, path, needles, role in SOURCES:
        needles_found, note = needle_status(path, needles)
        rows.append(
            {
                "timestamp_utc": timestamp(),
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_key": key,
                "source_path": str(path),
                "exists": bool_text(path.exists()),
                "needles": ";".join(needles),
                "needles_found": bool_text(needles_found),
                "source_role": role,
                "valid_for_claim": "false",
                "notes": note,
            }
        )
    return rows


def build_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "ROUTE2320_0_delta_w",
            "candidate_route": "delta_w material/source vector",
            "evidence_status": "COMPARATOR_AND_PRODUCT_ANCHORS_ONLY",
            "strength": "MICROSCOPE bound and delta_w_e proxy/product rows exist",
            "blocker": "material/source response vector, tau_eff, readout transfer, and complete component vector are missing",
            "decision": "defer to acquisition lane",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ROUTE2320_1_ppn_component",
            "candidate_route": "PPN component owner row",
            "evidence_status": "OWNER_MATRIX_AND_ALPHA_CG_SOURCE_TARGET_EXIST",
            "strength": "2201 already stages alpha_cg as first component and attaches Cassini source ceiling",
            "blocker": "projection clauses remain blocked, but the row is structurally closer to local-GR testing",
            "decision": "select PPN component owner import for 2320",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ROUTE2320_2_verdict",
            "candidate_route": "2320 route selection",
            "evidence_status": "PPN_IMPORT_SELECTED_DELTAW_RETAINED",
            "strength": "imports one concrete component owner/source target while preserving delta_w acquisition gaps",
            "blocker": "no score-ready local-GR prediction follows",
            "decision": "write alpha_cg component status and delta_w acquisition status side by side",
            "valid_for_claim": "false",
        },
    ]


def build_ppn_import_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "PPNI2320_0_matrix",
            "imported_object": "PPN component owner matrix",
            "source_row": "PCM2201_0 through PCM2201_6",
            "imported_value": "seven component rows; alpha_cg selected first",
            "source_path": str(PATHS["2201_matrix"]),
            "current_status": "SOURCE_BACKED_STRUCTURE_NONCLAIM",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PPNI2320_1_alpha_cg_source",
            "imported_object": "alpha_cg source target",
            "source_row": "ACS2201_0_alpha_cg_target",
            "imported_value": "gamma_minus_1 Cassini/Shapiro ceiling = 6.7e-05 dimensionless",
            "source_path": str(PATHS["2201_alpha_source"]),
            "current_status": "SOURCE_BACKED_TARGET_NOT_MTS_PREDICTION",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PPNI2320_2_raw_cg_refusal",
            "imported_object": "raw c_g refusal",
            "source_row": "ACS2201_1_raw_cg_refusal;CG2201_3_raw_cg",
            "imported_value": "raw c_g remains non-invariant under normalization",
            "source_path": str(PATHS["2201_alpha_source"]),
            "current_status": "RAW_COMPONENT_BOUND_FORBIDDEN",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def build_alpha_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "ACG2320_0_common_frame",
            "projection_clause": "universal common matter frame",
            "needed_statement": "ordinary matter sees one conformal frame at Cassini order",
            "current_status": "NOT_PARENT_SIGNED",
            "blocks_score": "true",
            "source_basis": "ACG2201_0_common_frame;APA2202_0_common_frame",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ACG2320_1_same_branch",
            "projection_clause": "same-branch owner",
            "needed_statement": "same Xhat owns c_g, Z_X, M_X^2, lambda_X, tau_PPN, source, and readout",
            "current_status": "MISSING_PARENT_OWNER",
            "blocks_score": "true",
            "source_basis": "ACG2201_1_same_branch_owner;APA2202_1_same_branch",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ACG2320_2_ZX",
            "projection_clause": "canonical normalization",
            "needed_statement": "Z_X is parent-owned, positive, unit-fixed, and same-branch",
            "current_status": "MISSING_ZX",
            "blocks_score": "true",
            "source_basis": "ACG2201_2_normalization;APA2202_2_ZX",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ACG2320_3_lambda_SPPN",
            "projection_clause": "range/screening transfer",
            "needed_statement": "lambda_X and S_PPN(lambda_X,env) are derived for Cassini geometry",
            "current_status": "MISSING_LAMBDA_X_AND_S_PPN",
            "blocks_score": "true",
            "source_basis": "ACG2201_3_range_screening;APA2202_3_lambda_SPPN",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ACG2320_4_tau_PPN",
            "projection_clause": "PPN projection coefficient",
            "needed_statement": "tau_PPN maps parent residual to observed Cassini gamma/Shapiro readout",
            "current_status": "MISSING_TAU_PPN",
            "blocks_score": "true",
            "source_basis": "ACG2201_4_tau_PPN;APA2202_4_tau_PPN",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ACG2320_5_vector_tails",
            "projection_clause": "other vector tails",
            "needed_statement": "disformal, non-Hilbert, support/domain, boundary, and readout tails are theorem-zero or separately bounded",
            "current_status": "VECTOR_TAILS_UNCONTROLLED",
            "blocks_score": "true",
            "source_basis": "ACG2201_5_vector_tails;APA2202_5_vector_tails",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ACG2320_6_verdict",
            "projection_clause": "alpha_cg score-ready component",
            "needed_statement": "all alpha_cg projection clauses pass",
            "current_status": "ALPHA_CG_COMPONENT_OWNER_IMPORTED_NOT_SCORE_READY",
            "blocks_score": "true",
            "source_basis": "ACG2201_6_verdict;APA2202_6_verdict",
            "valid_for_claim": "false",
        },
    ]


def build_delta_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DWV2320_0_bound_anchor",
            "delta_w_piece": "MICROSCOPE product/comparator anchor",
            "current_value": "2.8e-15 product/comparator ceiling",
            "current_status": "SOURCE_BACKED_ANCHOR_NOT_PREDICTION",
            "missing_for_score": "delta_w material/source vector and tau_WEP projection",
            "source_basis": "BDW1694_0;FCR2319_2;FCR2319_3",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DWV2320_1_component_pack",
            "delta_w_piece": "component vector",
            "current_value": "delta_w_e proxy numeric exists; most components missing/proxy",
            "current_status": "COMPONENT_VECTOR_INCOMPLETE",
            "missing_for_score": "all components numeric/theorem-zero with uncertainties, basis, units, sign convention",
            "source_basis": "DWB1606_0 through DWB1606_8;READY1606_0",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DWV2320_2_material_tensor",
            "delta_w_piece": "Ti/Pt material-source response tensor",
            "current_value": "MISSING_PARENT_MATERIAL_RESPONSE_TENSOR",
            "current_status": "MATERIAL_VECTOR_MISSING",
            "missing_for_score": "official material/source response vector and source/test convention",
            "source_basis": "READY1606_1_material_tensor;DW2319_1_MICROSCOPE",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DWV2320_3_tau_readout",
            "delta_w_piece": "tau_WEP/readout transfer",
            "current_value": "MISSING_TAU_WEP_AND_READOUT_TRANSFER",
            "current_status": "PROJECTION_MISSING",
            "missing_for_score": "tau/source/readout projection and no-cancellation group",
            "source_basis": "READY1606_2_tau_projection;DWA1763_1_delta_w_readout",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DWV2320_4_verdict",
            "delta_w_piece": "delta_w material/source vector row",
            "current_value": "NOT_SCORE_READY",
            "current_status": "DEFERRED_TO_ACQUISITION",
            "missing_for_score": "component vector, material tensor, tau/readout transfer, no-cancellation covariance, or theorem-zero",
            "source_basis": "READY1606_5_verdict;DWR1490_6_claim_gate",
            "valid_for_claim": "false",
        },
    ]


def build_readiness_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "READY2320_0_ppn_component_owner",
            "test_object": "alpha_cg PPN component",
            "has_source_backed_target": "true",
            "has_mts_prediction": "false",
            "main_blocker": "projection clauses ACG2320_0 through ACG2320_5",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "READY2320_1_delta_w_vector",
            "test_object": "delta_w material/source vector",
            "has_source_backed_target": "true",
            "has_mts_prediction": "false",
            "main_blocker": "material tensor, tau_WEP/readout transfer, component vector",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "READY2320_2_local_GR_vector",
            "test_object": "full local-GR residual vector",
            "has_source_backed_target": "true",
            "has_mts_prediction": "false",
            "main_blocker": "every PPN/vector/coupling component must be theorem-zero or source-backed; no pair cancellation",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def build_claim_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2320_0_sources",
            "gate": "source paths and needles valid",
            "passed": "true",
            "claim_effect": "audit reproducible",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2320_1_ppn_owner_import",
            "gate": "PPN component owner/source target imported",
            "passed": "true",
            "claim_effect": "alpha_cg has a nonclaim source target",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2320_2_alpha_prediction",
            "gate": "alpha_cg component score-ready",
            "passed": "false",
            "claim_effect": "projection blockers prevent scoring",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2320_3_delta_w_vector",
            "gate": "delta_w material/source vector score-ready",
            "passed": "false",
            "claim_effect": "delta_w remains acquisition-only",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2320_4_local_GR_Newton",
            "gate": "local GR/Newton recovery derived",
            "passed": "false",
            "claim_effect": "still a target, not a result",
            "valid_for_claim": "false",
        },
    ]


def build_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2320_0_raw_cg",
            "claim": "Cassini source target bounds raw c_g",
            "allowed": "false",
            "reason": "raw c_g is non-invariant under field normalization; alpha_cg projection needs Z_X, lambda_X, tau_PPN, and same-branch owner",
            "blocking_rows": "PPNI2320_2_raw_cg_refusal;ACG2320_1_same_branch;ACG2320_2_ZX",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2320_1_alpha_score",
            "claim": "alpha_cg is score-ready",
            "allowed": "false",
            "reason": "all six alpha projection clauses remain blocked",
            "blocking_rows": "ACG2320_0_common_frame through ACG2320_6_verdict",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2320_2_delta_w_score",
            "claim": "delta_w can be scored from MICROSCOPE/product anchors",
            "allowed": "false",
            "reason": "anchors are not predictions; material/source/tau/readout projection is missing",
            "blocking_rows": "DWV2320_0_bound_anchor;DWV2320_4_verdict",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2320_3_local_GR",
            "claim": "2320 derives local GR/Newton",
            "allowed": "false",
            "reason": "2320 imports a component owner target but no complete MTS residual vector prediction",
            "blocking_rows": "READY2320_2_local_GR_vector;CG2320_4_local_GR_Newton",
            "valid_for_claim": "false",
        },
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2320_0",
            "next_target": "2321-Y5-R2FR-alpha-cg-projection-owner-fill-or-deltaw-material-vector-acquisition.md",
            "why": "2320 selects the PPN component route as the sharper current local-GR test object; next either fill one alpha_cg projection blocker (tau_PPN, Z_X, lambda_X/S_PPN, same-branch owner) or acquire the missing delta_w material/source vector",
            "claim_status": "nonclaim_private_next_step",
            "valid_for_claim": "false",
        }
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, source_path, destination_path in BRANCH_COPY_SPECS:
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, destination_path)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_csv": relative_path(source_path),
                "branch_copy_path": str(destination_path),
                "copy_exists": bool_text(destination_path.exists()),
                "row_count": len(read_csv_rows(destination_path)),
                "valid_for_claim": "false",
            }
        )
    return rows


def validate(
    source_rows: list[dict[str, Any]],
    route_rows: list[dict[str, Any]],
    ppn_rows: list[dict[str, Any]],
    alpha_rows: list[dict[str, Any]],
    delta_rows: list[dict[str, Any]],
    readiness_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    tables = [source_rows, route_rows, ppn_rows, alpha_rows, delta_rows, readiness_rows, claim_rows, refusal_rows, next_rows, copy_rows]
    formalization_output_markers = (
        "2320-Y5-R2FR",
        "P8_Y5_PARENT_QLOC_2320",
        "P8_Y5_BRR545_2320",
        "JR2320_",
        "PPN_COMPONENT_OWNER_IMPORT_2320",
        "local_gr_test_readiness_matrix_nonclaim_2320",
        "Y5_R2FR_delta_w_material_source_vector_or_PPN_component_owner_row_2320",
    )
    formalization_hits = [
        path
        for path in FORMALIZATION.rglob("*")
        if any(marker in path.name for marker in formalization_output_markers)
    ] if FORMALIZATION.exists() else []

    route_ids = {row["row_id"] for row in route_rows}
    alpha_statuses = {row["current_status"] for row in alpha_rows}
    delta_statuses = {row["current_status"] for row in delta_rows}

    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2320_00_sources_exist", all(row["exists"] == "true" for row in source_rows), "every cited source path exists"))
    checks.append(("VAL2320_01_needles_found", all(row["needles_found"] == "true" for row in source_rows), "all source needles were found"))
    checks.append(("VAL2320_02_route_selected", "ROUTE2320_1_ppn_component" in route_ids and any(row["row_id"] == "ROUTE2320_2_verdict" and "PPN_IMPORT_SELECTED" in row["evidence_status"] for row in route_rows), "PPN component route selected and delta_w retained"))
    checks.append(("VAL2320_03_ppn_import", any(row["row_id"] == "PPNI2320_1_alpha_cg_source" and "6.7e-05" in row["imported_value"] for row in ppn_rows), "alpha_cg source target imported"))
    checks.append(("VAL2320_04_alpha_blockers", {"NOT_PARENT_SIGNED", "MISSING_PARENT_OWNER", "MISSING_ZX", "MISSING_LAMBDA_X_AND_S_PPN", "MISSING_TAU_PPN", "VECTOR_TAILS_UNCONTROLLED", "ALPHA_CG_COMPONENT_OWNER_IMPORTED_NOT_SCORE_READY"}.issubset(alpha_statuses), "alpha_cg projection blockers preserved"))
    checks.append(("VAL2320_05_delta_deferred", "DEFERRED_TO_ACQUISITION" in delta_statuses and "MATERIAL_VECTOR_MISSING" in delta_statuses, "delta_w remains acquisition-only"))
    checks.append(("VAL2320_06_readiness_blocks_score", all(row["score_ready"] == "false" for row in readiness_rows), "all readiness rows remain non-score-ready"))
    checks.append(("VAL2320_07_claim_gates_block", any(row["row_id"] == "CG2320_4_local_GR_Newton" and row["passed"] == "false" for row in claim_rows), "local GR/Newton claim remains blocked"))
    checks.append(("VAL2320_08_refusals_block", all(row["allowed"] == "false" for row in refusal_rows), "refusal runner blocks premature claims"))
    checks.append(("VAL2320_09_next_target", any(row["row_id"] == "NEXT2320_0" and "alpha-cg-projection-owner-fill" in row["next_target"] for row in next_rows), "next target selected"))
    checks.append(("VAL2320_10_branch_copies_parse", all(Path(row["branch_copy_path"]).exists() and int(row["row_count"]) > 0 for row in copy_rows), "branch copies exist and parse"))
    checks.append(("VAL2320_11_no_claim_flags", not any(row.get("valid_for_claim") == "true" for table in tables for row in table), "no generated row is valid_for_claim=true"))
    checks.append(("VAL2320_12_formalization_untouched_by_2320", len(formalization_hits) == 0, "no 2320 checkpoint output appears in formalization-workbench"))

    rows = [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": "false",
        }
        for row_id, passed, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2320_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "2320 selects the PPN component owner route because 2201 already provides an alpha_cg component/source target, imports that target into the current runner, preserves all alpha_cg projection blockers, keeps delta_w as acquisition-only because material/source/tau/readout inputs remain missing, and blocks raw c_g, delta_w scoring, and local-GR/Newton claims.",
            "valid_for_claim": "false",
        }
    )
    return rows


def write_markdown(
    source_rows: list[dict[str, Any]],
    route_rows: list[dict[str, Any]],
    ppn_rows: list[dict[str, Any]],
    alpha_rows: list[dict[str, Any]],
    delta_rows: list[dict[str, Any]],
    readiness_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    lines = [
        "# 2320 - delta_w Material Source Vector Or PPN Component Owner Row",
        "",
        "## Summary",
        "",
        "2320 chooses the PPN component-owner route for the current local-GR testing lane. The reason is practical: `delta_w` has real comparator/product anchors, but still lacks the material/source vector, `tau_eff`, and readout transfer needed for a prediction. The PPN route already has a component owner matrix and an `alpha_cg` source target from 2201.",
        "",
        "The import is still nonclaim. `alpha_cg` gets a Cassini/Shapiro source target, but the projection clause is not derived: common frame, same-branch owner, `Z_X`, `lambda_X/S_PPN`, `tau_PPN`, and vector-tail control all remain missing.",
        "",
        "So the local-GR fight has a sharper next object, not a win. Raw `c_g` is still forbidden; `delta_w` is still acquisition-only; and local GR/Newton recovery remains blocked until a full residual vector has theorem-zero or source-backed components.",
        "",
        "## Source Register",
        "",
        markdown_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"]),
        "",
        "## Route Selection",
        "",
        markdown_table(route_rows, ["row_id", "candidate_route", "evidence_status", "strength", "blocker", "decision", "valid_for_claim"]),
        "",
        "## PPN Component Owner Import",
        "",
        markdown_table(ppn_rows, ["row_id", "imported_object", "source_row", "imported_value", "source_path", "current_status", "score_ready", "valid_for_claim"]),
        "",
        "## alpha_cg Component Status",
        "",
        markdown_table(alpha_rows, ["row_id", "projection_clause", "needed_statement", "current_status", "blocks_score", "source_basis", "valid_for_claim"]),
        "",
        "## delta_w Material Source Vector Status",
        "",
        markdown_table(delta_rows, ["row_id", "delta_w_piece", "current_value", "current_status", "missing_for_score", "source_basis", "valid_for_claim"]),
        "",
        "## Local GR Test Readiness Matrix",
        "",
        markdown_table(readiness_rows, ["row_id", "test_object", "has_source_backed_target", "has_mts_prediction", "main_blocker", "score_ready", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        markdown_table(claim_rows, ["row_id", "gate", "passed", "claim_effect", "valid_for_claim"]),
        "",
        "## Refusal Runner",
        "",
        markdown_table(refusal_rows, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        markdown_table(next_rows, ["row_id", "next_target", "why", "claim_status", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        markdown_table(copy_rows, ["row_id", "source_csv", "branch_copy_path", "copy_exists", "row_count", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        markdown_table(validation_rows, ["row_id", "status", "detail", "valid_for_claim"]),
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    source_rows = build_sources()
    route_rows = build_route_rows()
    ppn_rows = build_ppn_import_rows()
    alpha_rows = build_alpha_status_rows()
    delta_rows = build_delta_status_rows()
    readiness_rows = build_readiness_rows()
    claim_rows = build_claim_rows()
    refusal_rows = build_refusal_rows()
    next_rows = build_next_rows()

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["route"], route_rows)
    write_csv(OUTPUTS["ppn_import"], ppn_rows)
    write_csv(OUTPUTS["alpha_status"], alpha_rows)
    write_csv(OUTPUTS["delta_status"], delta_rows)
    write_csv(OUTPUTS["readiness"], readiness_rows)
    write_csv(OUTPUTS["claims"], claim_rows)
    write_csv(OUTPUTS["refusal"], refusal_rows)
    write_csv(OUTPUTS["next"], next_rows)

    copy_rows = copy_branch_outputs()
    write_csv(OUTPUTS["copies"], copy_rows)

    validation_rows = validate(
        source_rows,
        route_rows,
        ppn_rows,
        alpha_rows,
        delta_rows,
        readiness_rows,
        claim_rows,
        refusal_rows,
        next_rows,
        copy_rows,
    )
    write_csv(OUTPUTS["validation"], validation_rows)
    write_markdown(
        source_rows,
        route_rows,
        ppn_rows,
        alpha_rows,
        delta_rows,
        readiness_rows,
        claim_rows,
        refusal_rows,
        next_rows,
        copy_rows,
        validation_rows,
    )

    overall = next(row for row in validation_rows if row["row_id"] == "VAL2320_OVERALL")
    print(f"{overall['row_id']}={overall['status']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
