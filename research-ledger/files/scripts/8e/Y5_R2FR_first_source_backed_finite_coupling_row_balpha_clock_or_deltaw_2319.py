from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_FIRST_SOURCE_BACKED_FINITE_COUPLING_ROWS_2319"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2319-Y5-R2FR-first-source-backed-finite-coupling-row-balpha-clock-or-deltaw.md"

PATHS = {
    "2318_doc": ROOT / "2318-Y5-R2FR-parent-coefficient-functor-construction-or-finite-coupling-prior-runner.md",
    "2318_validation": OUT / "P8_Y5_BRR545_2318_VALIDATION.csv",
    "2318_schema": OUT / "P8_Y5_PARENT_QLOC_2318_FINITE_COUPLING_PRIOR_RUNNER_SCHEMA.csv",
    "2318_smoke": OUT / "P8_Y5_PARENT_QLOC_2318_FINITE_COUPLING_PRIOR_RUNNER_SMOKE_NONCLAIM.csv",
    "1052_clock": OUT / "P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv",
    "1052_tau": OUT / "P8_Y5_R10_1052_TAU_CLOCK_XHAT_NORMALIZATION_AUDIT.csv",
    "1052_transfer": OUT / "P8_Y5_R10_1052_TRANSFER_CLAIM_GATES.csv",
    "1052_validation": OUT / "P8_Y5_BRR545_1052_VALIDATION.csv",
    "1092_clock": OUT / "P8_Y5_R10_1092_BALPHA_TAU_PROJECTION_FALLBACK.csv",
    "1092_transfer": OUT / "P8_Y5_R10_1092_WEP_R10_TRANSFER_GATES.csv",
    "1092_claims": OUT / "P8_Y5_R10_1092_CLAIM_GATES.csv",
    "1092_validation": OUT / "P8_Y5_BRR545_1092_VALIDATION.csv",
    "1092_doc": ROOT / "1092-Y5-R10-hidden-invariant-algebra-triviality-or-balpha-tau-projection.md",
    "2200_ppn_source": OUT / "P8_Y5_PARENT_QLOC_2200_PPN_VECTOR_SOURCE_ROW.csv",
    "2200_components": OUT / "P8_Y5_PARENT_QLOC_2200_PPN_COMPONENT_CONTRACT.csv",
    "2200_claims": OUT / "P8_Y5_PARENT_QLOC_2200_CLAIM_GATE.csv",
    "2200_validation": OUT / "P8_Y5_BRR545_2200_VALIDATION.csv",
    "2200_doc": ROOT / "2200-Y5-R2FR-hidden-invariant-algebra-triviality-or-PPN-vector-source-row.md",
    "1489_delta_w": OUT / "P8_Y5_R10_1489_DELTA_W_BOUND_INTERFACE_NONCLAIM.csv",
    "1490_delta_w": OUT / "P8_Y5_R10_1490_DELTA_W_REAL_INPUT_REQUIREMENTS.csv",
    "1092_wep_bound": OUT / "P8_Y5_R10_1092_WEP_BOUND_IMPORT.csv",
    "local_bounds": LOCAL_BOUNDS,
}

SOURCES = [
    ("SRC2319_00_2318_doc", "2318_doc", PATHS["2318_doc"], ["NEXT2318_0", "first-source-backed-finite-coupling-row"], "2318 handoff to first source-backed finite coupling rows"),
    ("SRC2319_01_2318_validation", "2318_validation", PATHS["2318_validation"], ["VAL2318_OVERALL", "PASS"], "2318 validation"),
    ("SRC2319_02_2318_schema", "2318_schema", PATHS["2318_schema"], ["SCHEMA2318_0_required_columns", "valid_for_claim"], "finite coupling runner schema"),
    ("SRC2319_03_2318_smoke", "2318_smoke", PATHS["2318_smoke"], ["SMOKE2318_1_b_alpha_tau_clock", "SMOKE2318_4_claim_gate"], "2318 smoke rows"),
    ("SRC2319_04_1052_clock", "1052_clock", PATHS["1052_clock"], ["ACB1052_2", "2.1e-18"], "best clock product bound"),
    ("SRC2319_05_1052_tau", "1052_tau", PATHS["1052_tau"], ["TCN1052_4_verdict", "FAIL_CURRENT_CLAIM_TAU_NOT_DERIVED"], "tau clock normalization block"),
    ("SRC2319_06_1052_transfer", "1052_transfer", PATHS["1052_transfer"], ["TG1052_0_clock_product_retained", "true_nonclaim_only"], "clock transfer gates"),
    ("SRC2319_07_1052_validation", "1052_validation", PATHS["1052_validation"], ["V1052_3_clock_product_retained", "pass"], "1052 validation"),
    ("SRC2319_08_1092_clock", "1092_clock", PATHS["1092_clock"], ["BTP1092_0_best_clock_product", "source-backed nonclaim product bound"], "1092 product fallback"),
    ("SRC2319_09_1092_transfer", "1092_transfer", PATHS["1092_transfer"], ["TRG1092_0_clock_product", "true_nonclaim_only"], "1092 transfer gates"),
    ("SRC2319_10_1092_claims", "1092_claims", PATHS["1092_claims"], ["CG1092_2_clock_product", "standalone b_alpha"], "1092 claim gates"),
    ("SRC2319_11_1092_validation", "1092_validation", PATHS["1092_validation"], ["V1092_5_clock_product_numeric_nonclaim", "pass"], "1092 validation"),
    ("SRC2319_12_1092_doc", "1092_doc", PATHS["1092_doc"], ["|b_alpha*tau_clock_time| <= 2.1e-18 yr^-1", "source-backed nonclaim"], "human-readable clock product summary"),
    ("SRC2319_13_2200_ppn_source", "2200_ppn_source", PATHS["2200_ppn_source"], ["PVS2200_2_vector_contract", "0.005788015401465051"], "PPN vector source row"),
    ("SRC2319_14_2200_components", "2200_components", PATHS["2200_components"], ["PCC2200_6_total", "sum_abs(all_components)"], "PPN component contract"),
    ("SRC2319_15_2200_claims", "2200_claims", PATHS["2200_claims"], ["CG2200_2_ppn_prediction", "BLOCKED_NONCLAIM"], "PPN claim gates"),
    ("SRC2319_16_2200_validation", "2200_validation", PATHS["2200_validation"], ["VAL2200_OVERALL", "PASS"], "2200 validation"),
    ("SRC2319_17_2200_doc", "2200_doc", PATHS["2200_doc"], ["NONCLAIM_VECTOR_TARGET", "not a local GR/Newton recovery claim"], "human-readable PPN vector summary"),
    ("SRC2319_18_1489_delta_w", "1489_delta_w", PATHS["1489_delta_w"], ["DWI1489_6_claim_gate", "NONCLAIM_INTERFACE_ONLY"], "delta_w interface"),
    ("SRC2319_19_1490_delta_w", "1490_delta_w", PATHS["1490_delta_w"], ["DWR1490_6_claim_gate", "MISSING_SOURCE_BACKED_VALUE"], "delta_w real input requirements"),
    ("SRC2319_20_1092_wep_bound", "1092_wep_bound", PATHS["1092_wep_bound"], ["BOUND1092_0_MICROSCOPE_WEP", "2.8000000000000001e-15"], "source-backed WEP comparator bound"),
    ("SRC2319_21_local_bounds", "local_bounds", PATHS["local_bounds"], ["R1_WEP_source_charge", "2.8e-15"], "local empirical bound ledger"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2319_SOURCE_REGISTER.csv",
    "runner_rows": OUT / "P8_Y5_PARENT_QLOC_2319_SOURCE_BACKED_FINITE_COUPLING_ROWS_NONCLAIM.csv",
    "acceptance": OUT / "P8_Y5_PARENT_QLOC_2319_RUNNER_ACCEPTANCE_MATRIX.csv",
    "delta_w": OUT / "P8_Y5_PARENT_QLOC_2319_DELTA_W_ACQUISITION_STATUS.csv",
    "ppn": OUT / "P8_Y5_PARENT_QLOC_2319_PPN_VECTOR_SOURCE_IMPORT.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2319_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2319_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2319_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2319_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2319_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2319_0_runner_rows", OUTPUTS["runner_rows"], RAB_QUEUE / "JR2319_SOURCE_BACKED_FINITE_COUPLING_ROWS_NONCLAIM.csv"),
    ("COPY2319_1_delta_w", OUTPUTS["delta_w"], RAB_QUEUE / "JR2319_DELTA_W_ACQUISITION_STATUS_NONCLAIM.csv"),
    ("COPY2319_2_ppn", OUTPUTS["ppn"], BETA_DOCS / "PPN_VECTOR_SOURCE_IMPORT_2319_NONCLAIM.csv"),
    ("COPY2319_3_wep", OUTPUTS["runner_rows"], MICRO_RESIDUALS / "source_backed_finite_coupling_rows_nonclaim_2319.csv"),
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


def build_runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "FCR2319_0_clock_product_best",
            "symbol": "b_alpha*tau_clock_time",
            "sector": "clock_product",
            "row_kind": "source_backed_product_constraint",
            "numeric_value": "2.1e-18",
            "uncertainty_or_limit": "1sigma product upper/envelope from best Yb+ E3/E2 clock row; 2sigma companion 3.2e-18 in 1052",
            "units": "yr^-1",
            "source_path": str(PATHS["1052_clock"]),
            "source_row_id": "ACB1052_2;BTP1092_0_best_clock_product",
            "theory_interpretation": "bounds only the product b_alpha*tau_clock_time; standalone b_alpha is not derived",
            "arena_projection": "clock product only",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FCR2319_1_ppn_vector_ceiling",
            "symbol": "alpha_PPN_total_abs_vector",
            "sector": "PPN_vector",
            "row_kind": "source_backed_proxy_vector_ceiling",
            "numeric_value": "0.005788015401465051",
            "uncertainty_or_limit": "Cassini gamma/scalar-tensor proxy converted to vector ceiling by 2200",
            "units": "dimensionless",
            "source_path": str(PATHS["2200_ppn_source"]),
            "source_row_id": "PVS2200_2_vector_contract",
            "theory_interpretation": "ceiling for an absolute PPN residual vector; not a raw c_g or MTS component bound",
            "arena_projection": "PPN/local-GR vector target",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FCR2319_2_wep_comparator_bound",
            "symbol": "eta_WEP_source_charge_bound",
            "sector": "WEP_comparator",
            "row_kind": "source_backed_comparator_bound_not_prediction",
            "numeric_value": "2.8e-15",
            "uncertainty_or_limit": "MICROSCOPE source-charge proxy upper bound",
            "units": "dimensionless",
            "source_path": str(LOCAL_BOUNDS),
            "source_row_id": "R1_WEP_source_charge;BOUND1092_0_MICROSCOPE_WEP",
            "theory_interpretation": "real comparator bound; no delta_w prediction row exists yet",
            "arena_projection": "WEP comparator only",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FCR2319_3_delta_w_missing_prediction",
            "symbol": "delta_w_A",
            "sector": "source_weight",
            "row_kind": "required_prediction_missing",
            "numeric_value": "MISSING_SOURCE_BACKED_VALUE",
            "uncertainty_or_limit": "MISSING_SOURCE_BACKED_UNCERTAINTY",
            "units": "dimensionless",
            "source_path": str(PATHS["1490_delta_w"]),
            "source_row_id": "DWR1490_6_claim_gate",
            "theory_interpretation": "delta_w cannot be inferred from comparator bounds without material/source/tau projection",
            "arena_projection": "WEP;Newton;R10 acquisition target",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def build_acceptance_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "ACCEPT2319_0_clock_product",
            "input_row": "FCR2319_0_clock_product_best",
            "source_backed": "true",
            "direct_MTS_prediction": "false",
            "accepted_for": "nonclaim product constraint only",
            "blocked_transfer": "standalone b_alpha; WEP; R10; local GR",
            "missing_for_score": "tau_clock_time parent derivation; Xhat/chi_X normalization; shared WEP/R10 projection",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ACCEPT2319_1_ppn_vector",
            "input_row": "FCR2319_1_ppn_vector_ceiling",
            "source_backed": "true",
            "direct_MTS_prediction": "false",
            "accepted_for": "nonclaim vector ceiling/proxy only",
            "blocked_transfer": "raw c_g; individual PPN components; local GR pass",
            "missing_for_score": "component owner matrix, tau/range/source/current/support/boundary/readout projections",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ACCEPT2319_2_wep_bound",
            "input_row": "FCR2319_2_wep_comparator_bound",
            "source_backed": "true",
            "direct_MTS_prediction": "false",
            "accepted_for": "comparator bound only",
            "blocked_transfer": "delta_w inference",
            "missing_for_score": "official material/source response vector, tau_eff, readout transfer, no-cancellation grouping",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ACCEPT2319_3_delta_w",
            "input_row": "FCR2319_3_delta_w_missing_prediction",
            "source_backed": "false",
            "direct_MTS_prediction": "false",
            "accepted_for": "acquisition queue only",
            "blocked_transfer": "WEP/Newton/R10 source-weight scoring",
            "missing_for_score": "numeric delta_w_i or theorem-zero plus source path, units, and arena projection",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def build_delta_w_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DW2319_0_core_model",
            "quantity": "delta_w_AB",
            "arena": "core",
            "current_status": "MISSING_SOURCE_BACKED_INPUTS",
            "required_next_input": "eta_AB ~= sum_i DeltaQ_i(AB) delta_w_i tau_i with material/source basis and readout transfer",
            "source_basis": "DWR1490_0_core;DWI1489_0_core_formula",
            "priority": "high",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DW2319_1_MICROSCOPE",
            "quantity": "delta_w_TiPt",
            "arena": "MICROSCOPE_TiPt",
            "current_status": "COMPARATOR_BOUND_EXISTS_PREDICTION_MISSING",
            "required_next_input": "official Ti/Pt/PtRh/TA6V material vector, Earth/source kernel, accepted readout, tau_eff",
            "source_basis": "R1_WEP_source_charge;DWR1490_1_MICROSCOPE",
            "priority": "high",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DW2319_2_R10",
            "quantity": "delta_w_R10",
            "arena": "R10_short_range",
            "current_status": "MISSING_BOUND_CURVE_AND_PROFILE",
            "required_next_input": "real alpha(lambda) bound curve, source/test composition, lambda/range map, parent profile",
            "source_basis": "DWR1490_3_R10;RAP1052_0_product_law",
            "priority": "medium",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DW2319_3_claim_gate",
            "quantity": "delta_w_runner_gate",
            "arena": "all_delta_w",
            "current_status": "NONCLAIM_REQUIREMENTS_ONLY",
            "required_next_input": "no delta_w row can score until numeric/theorem-zero row has source path, units, projection, and no-cancellation group",
            "source_basis": "DWR1490_6_claim_gate;DWI1489_6_claim_gate",
            "priority": "guard",
            "valid_for_claim": "false",
        },
    ]


def build_ppn_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "PPN2319_0_gamma_source",
            "imported_source_row": "PVS2200_0_cassini_gamma_source",
            "observable": "gamma_minus_1",
            "numeric_value": "6.7e-05",
            "units": "dimensionless",
            "translation_status": "SOURCE_BACKED_BUT_NOT_MTS_COMPONENT",
            "missing_for_claim": "map from MTS residual vector to gamma_minus_1 with all tails accounted",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PPN2319_1_alpha_proxy",
            "imported_source_row": "PVS2200_1_alpha_eff_proxy",
            "observable": "alpha_PPN_proxy",
            "numeric_value": "0.005788015401465051",
            "units": "dimensionless",
            "translation_status": "SCALAR_TENSOR_PROXY_ONLY",
            "missing_for_claim": "prove proxy is the MTS PPN residual observable",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PPN2319_2_vector_contract",
            "imported_source_row": "PVS2200_2_vector_contract",
            "observable": "alpha_PPN_total_abs_vector",
            "numeric_value": "0.005788015401465051",
            "units": "dimensionless",
            "translation_status": "NONCLAIM_VECTOR_TARGET",
            "missing_for_claim": "numeric/theorem-zero rows for every vector component and no pair-cancellation assumption",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def build_claim_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2319_0_sources",
            "gate": "source paths and needles valid",
            "passed": "true",
            "claim_effect": "audit reproducible",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2319_1_clock_product_import",
            "gate": "b_alpha*tau_clock_time source-backed product imported",
            "passed": "true",
            "claim_effect": "runner has first real product constraint but no standalone b_alpha",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2319_2_ppn_vector_import",
            "gate": "PPN vector ceiling imported",
            "passed": "true",
            "claim_effect": "runner has real vector ceiling but no component prediction",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2319_3_delta_w_prediction",
            "gate": "delta_w source-weight prediction row exists",
            "passed": "false",
            "claim_effect": "WEP/Newton/R10 source-weight scoring blocked",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2319_4_runner_score_ready",
            "gate": "finite coupling runner can score local tests",
            "passed": "false",
            "claim_effect": "all rows remain nonclaim/non-score-ready",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2319_5_local_GR_Newton",
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
            "row_id": "REF2319_0_standalone_balpha",
            "claim": "clock row gives standalone b_alpha",
            "allowed": "false",
            "reason": "1052/1092 both state tau_clock_time and Xhat/chi_X normalization are not parent-derived",
            "blocking_rows": "ACCEPT2319_0_clock_product;CG2319_1_clock_product_import",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2319_1_delta_w_bound_inference",
            "claim": "MICROSCOPE comparator bound gives delta_w prediction",
            "allowed": "false",
            "reason": "material/source response vector, tau_eff, and readout transfer are missing",
            "blocking_rows": "DW2319_1_MICROSCOPE;CG2319_3_delta_w_prediction",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2319_2_ppn_component",
            "claim": "PPN vector ceiling bounds raw c_g or an individual MTS PPN component",
            "allowed": "false",
            "reason": "2200 explicitly stages the row as vector/proxy target; component owner matrix is missing",
            "blocking_rows": "PPN2319_2_vector_contract;ACCEPT2319_1_ppn_vector",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2319_3_local_GR",
            "claim": "source-backed rows imply local GR/Newton recovery",
            "allowed": "false",
            "reason": "first rows are constraints/proxies only and no MTS residual vector is complete",
            "blocking_rows": "CG2319_4_runner_score_ready;CG2319_5_local_GR_Newton",
            "valid_for_claim": "false",
        },
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2319_0",
            "next_target": "2320-Y5-R2FR-delta-w-material-source-vector-or-PPN-component-owner-row.md",
            "why": "2319 imported the first real nonclaim constraints; the runner now needs either a delta_w material/source projection row or one PPN component owner row to become closer to actual local-GR testing",
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


def positive_number(value: str) -> bool:
    try:
        return float(value) > 0
    except ValueError:
        return False


def validate(
    source_rows: list[dict[str, Any]],
    runner_rows: list[dict[str, Any]],
    acceptance_rows: list[dict[str, Any]],
    delta_w_rows: list[dict[str, Any]],
    ppn_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    tables = [source_rows, runner_rows, acceptance_rows, delta_w_rows, ppn_rows, claim_rows, refusal_rows, next_rows, copy_rows]
    formalization_output_markers = (
        "2319-Y5-R2FR",
        "P8_Y5_PARENT_QLOC_2319",
        "P8_Y5_BRR545_2319",
        "JR2319_",
        "PPN_VECTOR_SOURCE_IMPORT_2319",
        "source_backed_finite_coupling_rows_nonclaim_2319",
        "Y5_R2FR_first_source_backed_finite_coupling_row_balpha_clock_or_deltaw_2319",
    )
    formalization_hits = [
        path
        for path in FORMALIZATION.rglob("*")
        if any(marker in path.name for marker in formalization_output_markers)
    ] if FORMALIZATION.exists() else []

    runner_by_id = {row["row_id"]: row for row in runner_rows}
    acceptance_by_id = {row["row_id"]: row for row in acceptance_rows}
    ppn_ids = {row["row_id"] for row in ppn_rows}

    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2319_00_sources_exist", all(row["exists"] == "true" for row in source_rows), "every cited source path exists"))
    checks.append(("VAL2319_01_needles_found", all(row["needles_found"] == "true" for row in source_rows), "all source needles were found"))
    checks.append(("VAL2319_02_clock_product_imported", "FCR2319_0_clock_product_best" in runner_by_id and positive_number(runner_by_id["FCR2319_0_clock_product_best"]["numeric_value"]), "clock product row imported with positive numeric value"))
    checks.append(("VAL2319_03_ppn_vector_imported", "FCR2319_1_ppn_vector_ceiling" in runner_by_id and positive_number(runner_by_id["FCR2319_1_ppn_vector_ceiling"]["numeric_value"]), "PPN vector ceiling imported with positive numeric value"))
    checks.append(("VAL2319_04_wep_bound_imported", "FCR2319_2_wep_comparator_bound" in runner_by_id and positive_number(runner_by_id["FCR2319_2_wep_comparator_bound"]["numeric_value"]), "WEP comparator bound imported with positive numeric value"))
    checks.append(("VAL2319_05_delta_w_missing", "FCR2319_3_delta_w_missing_prediction" in runner_by_id and runner_by_id["FCR2319_3_delta_w_missing_prediction"]["numeric_value"] == "MISSING_SOURCE_BACKED_VALUE", "delta_w prediction remains explicitly missing"))
    checks.append(("VAL2319_06_acceptance_blocks_score", all(row["score_ready"] == "false" for row in acceptance_rows), "all acceptance rows remain non-score-ready"))
    checks.append(("VAL2319_07_clock_not_standalone", acceptance_by_id.get("ACCEPT2319_0_clock_product", {}).get("blocked_transfer", "").startswith("standalone b_alpha"), "clock product blocks standalone b_alpha transfer"))
    checks.append(("VAL2319_08_ppn_rows_complete", {"PPN2319_0_gamma_source", "PPN2319_1_alpha_proxy", "PPN2319_2_vector_contract"}.issubset(ppn_ids), "PPN source/proxy/vector rows imported"))
    checks.append(("VAL2319_09_claim_gates_block", any(row["row_id"] == "CG2319_5_local_GR_Newton" and row["passed"] == "false" for row in claim_rows), "local GR/Newton claim remains blocked"))
    checks.append(("VAL2319_10_refusals_block", all(row["allowed"] == "false" for row in refusal_rows), "refusal runner blocks premature claims"))
    checks.append(("VAL2319_11_next_target", any(row["row_id"] == "NEXT2319_0" and "delta-w-material-source-vector" in row["next_target"] for row in next_rows), "next target selected"))
    checks.append(("VAL2319_12_branch_copies_parse", all(Path(row["branch_copy_path"]).exists() and int(row["row_count"]) > 0 for row in copy_rows), "branch copies exist and parse"))
    checks.append(("VAL2319_13_no_claim_flags", not any(row.get("valid_for_claim") == "true" for table in tables for row in table), "no generated row is valid_for_claim=true"))
    checks.append(("VAL2319_14_formalization_untouched_by_2319", len(formalization_hits) == 0, "no 2319 checkpoint output appears in formalization-workbench"))

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
            "row_id": "VAL2319_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "2319 imports the first source-backed nonclaim finite-coupling runner rows: the b_alpha*tau_clock_time clock product, the Cassini-derived PPN vector ceiling, and the MICROSCOPE WEP comparator bound. It refuses standalone b_alpha, delta_w inference, raw PPN component claims, and local-GR/Newton recovery because required tau/projection/material/source/component rows remain missing.",
            "valid_for_claim": "false",
        }
    )
    return rows


def write_markdown(
    source_rows: list[dict[str, Any]],
    runner_rows: list[dict[str, Any]],
    acceptance_rows: list[dict[str, Any]],
    delta_w_rows: list[dict[str, Any]],
    ppn_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    lines = [
        "# 2319 - First Source-Backed Finite Coupling Row: b_alpha Clock Or delta_w",
        "",
        "## Summary",
        "",
        "2319 makes the finite-coupling runner real, but still honest. The first source-backed nonclaim row is the clock product `|b_alpha*tau_clock_time| <= 2.1e-18 yr^-1`. This is a real constraint row, not a standalone `b_alpha` value.",
        "",
        "The second useful import is the Cassini-derived PPN vector ceiling from 2200. It is a source-backed proxy/vector target, not a bound on raw `c_g` and not a proof of local GR/Newton recovery.",
        "",
        "`delta_w` does not get promoted. MICROSCOPE gives a real comparator bound, but the MTS prediction row still needs material/source response vectors, `tau_eff`, readout transfer, units, source paths, and no-cancellation grouping.",
        "",
        "## Source Register",
        "",
        markdown_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"]),
        "",
        "## Source-Backed Finite Coupling Rows",
        "",
        markdown_table(runner_rows, ["row_id", "symbol", "sector", "row_kind", "numeric_value", "uncertainty_or_limit", "units", "source_path", "source_row_id", "theory_interpretation", "arena_projection", "score_ready", "valid_for_claim"]),
        "",
        "## Runner Acceptance Matrix",
        "",
        markdown_table(acceptance_rows, ["row_id", "input_row", "source_backed", "direct_MTS_prediction", "accepted_for", "blocked_transfer", "missing_for_score", "score_ready", "valid_for_claim"]),
        "",
        "## delta_w Acquisition Status",
        "",
        markdown_table(delta_w_rows, ["row_id", "quantity", "arena", "current_status", "required_next_input", "source_basis", "priority", "valid_for_claim"]),
        "",
        "## PPN Vector Source Import",
        "",
        markdown_table(ppn_rows, ["row_id", "imported_source_row", "observable", "numeric_value", "units", "translation_status", "missing_for_claim", "score_ready", "valid_for_claim"]),
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
    runner_rows = build_runner_rows()
    acceptance_rows = build_acceptance_rows()
    delta_w_rows = build_delta_w_rows()
    ppn_rows = build_ppn_rows()
    claim_rows = build_claim_rows()
    refusal_rows = build_refusal_rows()
    next_rows = build_next_rows()

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["runner_rows"], runner_rows)
    write_csv(OUTPUTS["acceptance"], acceptance_rows)
    write_csv(OUTPUTS["delta_w"], delta_w_rows)
    write_csv(OUTPUTS["ppn"], ppn_rows)
    write_csv(OUTPUTS["claims"], claim_rows)
    write_csv(OUTPUTS["refusal"], refusal_rows)
    write_csv(OUTPUTS["next"], next_rows)

    copy_rows = copy_branch_outputs()
    write_csv(OUTPUTS["copies"], copy_rows)

    validation_rows = validate(
        source_rows,
        runner_rows,
        acceptance_rows,
        delta_w_rows,
        ppn_rows,
        claim_rows,
        refusal_rows,
        next_rows,
        copy_rows,
    )
    write_csv(OUTPUTS["validation"], validation_rows)
    write_markdown(
        source_rows,
        runner_rows,
        acceptance_rows,
        delta_w_rows,
        ppn_rows,
        claim_rows,
        refusal_rows,
        next_rows,
        copy_rows,
        validation_rows,
    )

    overall = next(row for row in validation_rows if row["row_id"] == "VAL2319_OVERALL")
    print(f"{overall['row_id']}={overall['status']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
