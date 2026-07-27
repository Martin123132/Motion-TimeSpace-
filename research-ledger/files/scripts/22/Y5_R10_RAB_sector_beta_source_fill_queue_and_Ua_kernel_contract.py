from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path("source-intake/mts_residuals")

DOC_PATH = Path("1408-Y5-R10-RAB-sector-beta-source-fill-queue-and-Ua-kernel-contract.md")
SOURCE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1408_SOURCE_REGISTER.csv"
FILL_QUEUE_PATH = SRC_DIR / "P8_Y5_R10_1408_SECTOR_BETA_SOURCE_FILL_QUEUE.csv"
UA_KERNEL_CONTRACT_PATH = SRC_DIR / "P8_Y5_R10_1408_UA_KERNEL_CONTRACT.csv"
TEMPLATE_ROWS_PATH = SRC_DIR / "P8_Y5_R10_1408_SOURCE_READY_TEMPLATE_ROWS.csv"
PRIORITY_MATRIX_PATH = SRC_DIR / "P8_Y5_R10_1408_PRIORITY_DECISION_MATRIX.csv"
CLAIM_GATE_PATH = SRC_DIR / "P8_Y5_R10_1408_CLAIM_GATE.csv"
NEXT_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1408_NEXT_TARGET.csv"
VALIDATION_PATH = SRC_DIR / "P8_Y5_BRR545_1408_VALIDATION.csv"

STATUS = (
    "Y5_R10_1408_sector_beta_source_fill_queue_and_Ua_kernel_contract_"
    "written_nonclaim"
)
CLAIM_CEILING = (
    "fill_queue_and_Ua_kernel_contract_only_no_WEP_pass_no_clock_transfer_"
    "no_R10_transfer_no_PPN_no_Newton_no_local_GR_pass"
)

SCHEMA_COLUMNS = (
    "coefficient_id;quantity;parent_definition;units;dimension_basis;value;uncertainty;"
    "sign_convention;source_path;source_anchor;arena_projection;lambda_or_domain;"
    "fill_status;valid_for_claim;claim_allowed"
)


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").replace("\r", " ").strip()


def md_cell(value: Any) -> str:
    return clean(value).replace("|", "\\|")


def write_csv(relative_path: Path, rows: list[dict[str, Any]]) -> None:
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows supplied for {relative_path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: clean(row.get(key, "")) for key in fieldnames})


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def anchor_found(relative_path: str, anchor: str) -> bool:
    path = ROOT / relative_path
    if not path.exists():
        return False
    return anchor in path.read_text(encoding="utf-8", errors="ignore")


def source_register_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": "SRC1408_0_1407_doc",
            "source_path": "1407-Y5-R10-RAB-NoSourceOnlySpeciesSlot-proof-or-sector-beta-source-schema.md",
            "anchor": "NEXT1407_0_1408",
            "role": "prior checkpoint selecting sector beta fill queue and U_a kernel contract",
        },
        {
            "source_id": "SRC1408_1_1407_schema",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1407_SECTOR_BETA_SOURCE_SCHEMA.csv",
            "anchor": "SCHEMA1407_8_verdict",
            "role": "strict coefficient schema with missing nonclaim values",
        },
        {
            "source_id": "SRC1408_2_1407_gate",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1407_SCHEMA_ACCEPTANCE_GATE.csv",
            "anchor": "SG1407_5_verdict",
            "role": "schema acceptance remains blocked until values/sources exist",
        },
        {
            "source_id": "SRC1408_3_1406_acquisition",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1406_SECTOR_BETA_SOURCE_ACQUISITION.csv",
            "anchor": "SBAQ1406_7_verdict",
            "role": "sector beta acquisition pack",
        },
        {
            "source_id": "SRC1408_4_1405_vector",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1405_SECTOR_RESPONSE_VECTOR_MAP.csv",
            "anchor": "SVP1405_6_vector_verdict",
            "role": "sector response vector map requiring P_s values",
        },
        {
            "source_id": "SRC1408_5_1225_tau_attempt",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1225_TAU_WEP_PROJECTION_ATTEMPT.csv",
            "anchor": "TAU1225_6_verdict",
            "role": "tau_WEP/U_a projection not derived",
        },
        {
            "source_id": "SRC1408_6_1225_formula",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1225_SYMBOLIC_TAU_WEP_FORMULA.csv",
            "anchor": "FORM1225_0_tau_WEP_functional",
            "role": "symbolic WEP source/readout functional",
        },
        {
            "source_id": "SRC1408_7_1225_acquisition",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1225_TAU_WEP_SOURCE_ACQUISITION_TABLE.csv",
            "anchor": "ACQ1225_0_official_readout_arrays",
            "role": "official readout arrays and product convention acquisition rows",
        },
        {
            "source_id": "SRC1408_8_1225_shortcuts",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1225_TAU_WEP_ANTI_SHORTCUT_GATES.csv",
            "anchor": "SHORT1225_0_no_tau_unity",
            "role": "forbids tau_WEP=1 and surrogate kernel shortcuts",
        },
        {
            "source_id": "SRC1408_9_1325_fill",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1325_FIRST_FILL_INPUT_MATRIX.csv",
            "anchor": "IN1325_6_tau_WEP",
            "role": "first fill matrix showing tau_WEP/readout arrays missing",
        },
        {
            "source_id": "SRC1408_10_1325_decomp",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1325_WEP_PRODUCT_DECOMPOSITION.csv",
            "anchor": "DECOMP1325_3_full_finite_tensor",
            "role": "full finite tensor formula-ready but not scoreable",
        },
        {
            "source_id": "SRC1408_11_1395_sector_pack",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1395_BINDING_SECTOR_BETA_SOURCE_PACK.csv",
            "anchor": "SBP1395_5_pack_verdict",
            "role": "sector beta rows explicit but unfilled",
        },
        {
            "source_id": "SRC1408_12_1396_beta_EM",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1396_BETA_EM_SOURCE_BOUND_TEMPLATE.csv",
            "anchor": "BEM1396_6_template_verdict",
            "role": "beta_EM finite source-bound template ready nonclaim",
        },
        {
            "source_id": "SRC1408_13_material_tensor",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1079_MATERIAL_TENSOR_CONTRACT.csv",
            "anchor": "MTC1079_3_uncertainty",
            "role": "full material tensor basis/uncertainty contract still missing",
        },
        {
            "source_id": "SRC1408_14_no_cancel",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1087_ALL_MATERIAL_NO_CANCELLATION_POLICY.csv",
            "anchor": "AMC1087_0_pair_line_forbidden",
            "role": "one-pair cancellation forbidden",
        },
        {
            "source_id": "SRC1408_15_1402_isolation",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1402_ARENA_ISOLATION_LEDGER.csv",
            "anchor": "ISO1402_1_WEP",
            "role": "arena isolation still blocks transfer",
        },
        {
            "source_id": "SRC1408_16_this_script",
            "source_path": "scripts/Y5_R10_RAB_sector_beta_source_fill_queue_and_Ua_kernel_contract.py",
            "anchor": "STATUS",
            "role": "generator for this checkpoint",
        },
    ]
    for row in rows:
        row["path_exists"] = (ROOT / row["source_path"]).exists()
        row["anchor_found"] = anchor_found(row["source_path"], row["anchor"])
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def fill_queue_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "queue_id": "FQ1408_0_Ua_kernel",
            "priority": "P0",
            "quantity": "U_a := K_ab(lambda,lab) alpha_source^b",
            "why_first": "all finite WEP sector coefficients P_s=beta_s^a U_a need the same WEP source/kernel contraction",
            "current_status": "MISSING_SOURCE_KERNEL_AND_READOUT",
            "source_basis": "TAU1225_6_verdict;FORM1225_0_tau_WEP_functional;ACQ1225_0_official_readout_arrays",
            "next_action": "derive/source official kernel, source worldtube, orbit average, product normalization, and observed-frame convention",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "queue_id": "FQ1408_1_beta_EM",
            "priority": "P1",
            "quantity": "beta_EM^a",
            "why_first": "EM binding touches WEP, clocks, R10, alpha_EM, and the local EM residual vector",
            "current_status": "MISSING_BETA_EM_ZERO_OR_BOUND",
            "source_basis": "BEM1396_6_template_verdict;SBP1395_2_beta_EM",
            "next_action": "derive EM-lock/unique normalization or fill finite beta_EM source-bound template",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "queue_id": "FQ1408_2_beta_nuc",
            "priority": "P1",
            "quantity": "beta_nuc^a",
            "why_first": "nuclear/QCD binding controls WEP material contrast and orbital/source-mass residuals",
            "current_status": "MISSING_NUCLEAR_SECTOR_BETA_ZERO_OR_BOUND",
            "source_basis": "SBP1395_1_beta_nuc;SBZ1395_1_nuclear_zero",
            "next_action": "derive QCD/nuclear binding owner or create finite beta_nuc bound row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "queue_id": "FQ1408_3_Delta_f_tensor",
            "priority": "P1",
            "quantity": "Delta f_s,AB",
            "why_first": "without full material contrast tensor, sector betas cannot be contracted into eta_AB honestly",
            "current_status": "MISSING_FULL_MATERIAL_TENSOR",
            "source_basis": "MTC1079_3_uncertainty;MAT1068_2_full_tensor;MPM1404_6_full_material_tensor",
            "next_action": "declare parent basis and source material fractions/uncertainties or keep smoke rows nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "queue_id": "FQ1408_4_beta_e",
            "priority": "P2",
            "quantity": "beta_e^a",
            "why_first": "electronic/atomic sector couples to clocks and WEP but is less central than U_a/EM/nuclear blockers",
            "current_status": "MISSING_ELECTRONIC_SECTOR_BETA_ZERO_OR_BOUND",
            "source_basis": "SBP1395_0_beta_e;SBZ1395_0_electronic_zero",
            "next_action": "derive electron/readout owner or source finite beta_e bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "queue_id": "FQ1408_5_beta_other",
            "priority": "P2",
            "quantity": "beta_other^a",
            "why_first": "guard for omitted material/readout sectors; needed for conservative residual envelope",
            "current_status": "MISSING_SECTOR_COMPLETENESS_OR_RESIDUAL_ENVELOPE",
            "source_basis": "SBP1395_3_beta_other_guard",
            "next_action": "prove sector inventory complete or define beta_other envelope",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "queue_id": "FQ1408_6_Ps_products",
            "priority": "P3",
            "quantity": "P_s := beta_s^a U_a",
            "why_first": "derived product rows are only meaningful after U_a and beta_s rows exist",
            "current_status": "DEPENDENT_ON_FQ1408_0_THROUGH_FQ1408_5",
            "source_basis": "SVP1405_6_vector_verdict;SCHEMA1407_6_P_s",
            "next_action": "compute only in a runner after source rows are complete and nonclaim gates pass",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "queue_id": "FQ1408_7_slot_certificate",
            "priority": "PARALLEL_THEOREM_ROUTE",
            "quantity": "NoSourceOnlySpeciesSlot_certificate",
            "why_first": "if proved, it can demote source-only weight branch without coefficient fitting",
            "current_status": "NOT_PROVED_CLOSURE_CONDITION",
            "source_basis": "NSS1407_7_current_verdict",
            "next_action": "continue proof route separately; do not use it as data-row shortcut",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return rows


def ua_kernel_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "UAK1408_0_definition",
            "component": "U_a",
            "required_object": "U_a := K_ab(lambda,lab) alpha_source^b",
            "current_status": "SYMBOLIC_ONLY",
            "source": "FORM1225_0_tau_WEP_functional",
            "claim_effect": "cannot compute P_s without U_a",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "UAK1408_1_source_worldtube",
            "component": "alpha_source^b",
            "required_object": "Earth/source stress-current worldtube in observed local frame",
            "current_status": "MISSING_SOURCE_PROFILE_WEIGHTING",
            "source": "TAU1225_0_source_worldtube;ACQ1225_2_source_worldtube",
            "claim_effect": "source side of U_a unavailable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "UAK1408_2_readout_kernel",
            "component": "K_ab(lambda,lab)",
            "required_object": "official or exactly equivalent WEP readout/kernel arrays",
            "current_status": "OFFICIAL_ARRAYS_NOT_IMPORTED",
            "source": "TAU1225_4_force_readout;ACQ1225_0_official_readout_arrays",
            "claim_effect": "no surrogate kernel can promote a claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "UAK1408_3_orbit_average",
            "component": "lab/orbit average",
            "required_object": "time/session/orbit average matched to the reported eta_AB channel",
            "current_status": "MISSING_ORBIT_AVERAGE_ARRAYS",
            "source": "TAU1225_1_orbit_average;ACQ1225_3_orbit_average",
            "claim_effect": "kernel cannot be normalized to the experiment",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "UAK1408_4_product_normalization",
            "component": "N_eta/product convention",
            "required_object": "map from source response x material response x readout kernel to reported Eotvos eta",
            "current_status": "NORMALIZATION_NOT_FILLED",
            "source": "TAU1225_5_normalization;ACQ1225_1_product_convention",
            "claim_effect": "U_a cannot be compared to eta_AB bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "UAK1408_5_observed_frame",
            "component": "e_obs/source frame",
            "required_object": "same observed frame for force law, source variation, clocks, and readout",
            "current_status": "CONDITIONAL_FROM_PRIOR_SPINE",
            "source": "TAU1225_2_observed_coframe",
            "claim_effect": "frame consistency remains conditional",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "UAK1408_6_material_tensor_domain",
            "component": "Delta f_s,AB/R_material",
            "required_object": "material tensor in the same basis as U_a and beta_s",
            "current_status": "MISSING_FULL_MATERIAL_TENSOR",
            "source": "MTC1079_0_basis;MTC1079_2_response_map",
            "claim_effect": "U_a cannot be safely contracted with material rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "UAK1408_7_anti_shortcuts",
            "component": "shortcut guards",
            "required_object": "no tau_WEP=1, no surrogate kernel claim, no sign/material cancellation",
            "current_status": "ENFORCED",
            "source": "SHORT1225_0_no_tau_unity;SHORT1225_1_no_surrogate_claim;SHORT1225_3_no_cancellation",
            "claim_effect": "prevents fake WEP pass",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "UAK1408_8_verdict",
            "component": "U_a contract status",
            "required_object": "all UAK1408_1 through UAK1408_6 complete without MISSING markers",
            "current_status": "UA_KERNEL_CONTRACT_READY_VALUES_MISSING",
            "source": "1408 checkpoint",
            "claim_effect": "U_a remains nonclaim and blocks P_s products",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def template_rows() -> list[dict[str, Any]]:
    templates = [
        ("TEMPLATE1408_0_beta_e", "beta_e^a", "partial ln E_e / partial X_a", "X_a^-1 or dimensionless per parent coordinate", "clock/fine-structure;WEP;R10", "FQ1408_4_beta_e"),
        ("TEMPLATE1408_1_beta_nuc", "beta_nuc^a", "partial ln E_nuc / partial X_a", "X_a^-1 or dimensionless per parent coordinate", "WEP;orbital;R10", "FQ1408_2_beta_nuc"),
        ("TEMPLATE1408_2_beta_EM", "beta_EM^a", "partial ln E_EM / partial X_a", "X_a^-1 or dimensionless per parent coordinate", "WEP;clock;R10", "FQ1408_1_beta_EM"),
        ("TEMPLATE1408_3_beta_other", "beta_other^a", "partial ln E_other / partial X_a", "X_a^-1 or dimensionless per parent coordinate", "WEP;PPN;readout", "FQ1408_5_beta_other"),
        ("TEMPLATE1408_4_Ua", "U_a", "K_ab(lambda,lab) alpha_source^b", "inverse response-coordinate or arena-normalized source factor", "WEP only until transfer theorem", "FQ1408_0_Ua_kernel"),
        ("TEMPLATE1408_5_Delta_f", "Delta f_s,AB", "f_s,A - f_s,B for each material pair and sector", "dimensionless fraction", "WEP material scoring", "FQ1408_3_Delta_f_tensor"),
        ("TEMPLATE1408_6_Ps", "P_s", "P_s := beta_s^a U_a", "dimensionless Eotvos-response coefficient", "WEP pressure only", "FQ1408_6_Ps_products"),
    ]
    rows = []
    for template_id, quantity, parent_definition, units, arena_projection, fill_queue_ref in templates:
        rows.append(
            {
                "template_id": template_id,
                "quantity": quantity,
                "parent_definition": parent_definition,
                "required_columns": SCHEMA_COLUMNS,
                "units": units,
                "dimension_basis": "MISSING_PARENT_COORDINATE_BASIS",
                "value": "MISSING_SOURCE_VALUE",
                "uncertainty": "MISSING_UNCERTAINTY",
                "sign_convention": "MISSING_SIGN_CONVENTION",
                "source_path": "MISSING_SOURCE_PATH",
                "source_anchor": "MISSING_SOURCE_ANCHOR",
                "arena_projection": arena_projection,
                "lambda_or_domain": "WEP_LOCAL_DOMAIN_ONLY_UNTIL_TRANSFER",
                "fill_queue_ref": fill_queue_ref,
                "valid_for_claim": False,
                "claim_allowed": False,
                "status": "SOURCE_READY_TEMPLATE_NONCLAIM",
            }
        )
    rows.append(
        {
            "template_id": "TEMPLATE1408_7_verdict",
            "quantity": "source_ready_template_pack",
            "parent_definition": "schema rows are ready for later fill; no numeric claim values are present",
            "required_columns": SCHEMA_COLUMNS,
            "units": "declared_per_future_row",
            "dimension_basis": "declared_per_future_row",
            "value": "TEMPLATE_ONLY",
            "uncertainty": "not_applicable",
            "sign_convention": "declared_per_future_row",
            "source_path": "not_applicable",
            "source_anchor": "not_applicable",
            "arena_projection": "WEP pressure only until transfer gates close",
            "lambda_or_domain": "not_applicable",
            "fill_queue_ref": "FQ1408_0_through_FQ1408_6",
            "valid_for_claim": False,
            "claim_allowed": False,
            "status": "TEMPLATE_PACK_READY_NO_VALUES",
        }
    )
    return rows


def priority_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "PRI1408_0_Ua_first",
            "priority": "P0",
            "target": "U_a kernel/source contract",
            "reason": "shared multiplier for every finite WEP sector product",
            "decision": "derive/source U_a before any product scoring",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "PRI1408_1_EM_nuclear_next",
            "priority": "P1",
            "target": "beta_EM and beta_nuc",
            "reason": "largest cross-arena entanglement and active prior blockers",
            "decision": "target EM-lock/beta_EM and nuclear/QCD owner or finite bounds next",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "PRI1408_2_material_tensor_parallel",
            "priority": "P1",
            "target": "Delta f_s,AB full material tensor",
            "reason": "no sector beta can be contracted honestly without material tensor",
            "decision": "build material tensor in same basis as beta_s and U_a, not just alpha/surface smoke rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "PRI1408_3_e_other_later",
            "priority": "P2",
            "target": "beta_e and beta_other",
            "reason": "important for clocks/readout/completeness but depends less directly on current WEP kernel",
            "decision": "queue after U_a/EM/nuclear or handle as parallel theorem-zero attempts",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "PRI1408_4_products_last",
            "priority": "P3",
            "target": "P_s products and WEP pressure runner",
            "reason": "products are invalid until input rows are sourced/nonclaim-clean",
            "decision": "no runner/scoring until input gates clear",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "GATE1408_0_Ua",
            "claim": "U_a kernel/source contraction is derived or sourced",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "source worldtube, readout arrays, orbit average, product normalization, and material basis remain missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1408_1_sector_betas",
            "claim": "sector beta coefficients are claim-ready",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "beta_e, beta_nuc, beta_EM, beta_other templates contain no source values",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1408_2_material_tensor",
            "claim": "full material contrast tensor is available",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "Delta f_s,AB remains template-only and alpha/surface smoke rows are not a complete parent basis",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1408_3_WEP_pass",
            "claim": "WEP branch passes",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "1408 is fill queue/template only and contains no claim-ready products",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1408_4_transfer",
            "claim": "WEP coefficients transfer to clocks, R10, PPN, or orbital tests",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "1402 arena isolation remains active",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1408_5_local_GR",
            "claim": "local GR/Newton reduction can be claimed",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "fill queue does not close q_loc, lambda_A, EM residuals, source kernel, or PPN projection",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1408_0_1409",
            "target_doc": "1409-Y5-R10-RAB-Ua-kernel-first-fill-or-official-readout-blocker-ledger.md",
            "target_script": "scripts/Y5_R10_RAB_Ua_kernel_first_fill_or_official_readout_blocker_ledger.py",
            "task": "try to fill or bound the first U_a kernel pieces: official WEP readout arrays, source worldtube/profile, orbit average, product normalization, and observed-frame convention; if unavailable, write blocker ledger and keep all P_s products nonclaim",
            "success_condition": "U_a has either source-backed rows with units/sign/source anchors or a precise blocker ledger showing which official/readout data are missing",
            "do_not_claim": "WEP pass;clock pass;R10 pass;PPN pass;Newton limit;local GR;lambda_A=0;q_loc=0;GitHub-ready result",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    queue: list[dict[str, Any]],
    ua: list[dict[str, Any]],
    templates: list[dict[str, Any]],
    priorities: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    now = datetime.now(timezone.utc).isoformat()

    def row(check_id: str, status: bool, detail: str) -> dict[str, Any]:
        return {
            "check_id": check_id,
            "status": "PASS" if status else "FAIL",
            "detail": detail,
            "timestamp_utc": now,
        }

    all_sources_ok = all(r["path_exists"] and r["anchor_found"] for r in sources)
    queue_ok = (
        any(r["queue_id"] == "FQ1408_0_Ua_kernel" and r["priority"] == "P0" for r in queue)
        and any(r["queue_id"] == "FQ1408_1_beta_EM" and r["priority"] == "P1" for r in queue)
        and any(r["queue_id"] == "FQ1408_3_Delta_f_tensor" for r in queue)
        and all(str(r["claim_allowed"]) == "False" for r in queue)
    )
    ua_ok = (
        any(r["contract_id"] == "UAK1408_6_material_tensor_domain" and r["current_status"] == "MISSING_FULL_MATERIAL_TENSOR" for r in ua)
        and any(r["contract_id"] == "UAK1408_7_anti_shortcuts" and r["current_status"] == "ENFORCED" for r in ua)
        and any(r["contract_id"] == "UAK1408_8_verdict" and r["current_status"] == "UA_KERNEL_CONTRACT_READY_VALUES_MISSING" for r in ua)
        and all(str(r["valid_for_claim"]) == "False" for r in ua)
    )
    template_ok = (
        any(r["template_id"] == "TEMPLATE1408_4_Ua" and r["value"] == "MISSING_SOURCE_VALUE" for r in templates)
        and any(r["template_id"] == "TEMPLATE1408_2_beta_EM" and r["value"] == "MISSING_SOURCE_VALUE" for r in templates)
        and any(r["template_id"] == "TEMPLATE1408_7_verdict" and r["status"] == "TEMPLATE_PACK_READY_NO_VALUES" for r in templates)
        and all(str(r["claim_allowed"]) == "False" for r in templates)
    )
    priority_ok = (
        any(r["decision_id"] == "PRI1408_0_Ua_first" and r["priority"] == "P0" for r in priorities)
        and any(r["decision_id"] == "PRI1408_4_products_last" and r["priority"] == "P3" for r in priorities)
        and all(str(r["valid_for_claim"]) == "False" for r in priorities)
    )
    claim_ok = all(str(r["claim_allowed"]) == "False" and "NO_CLAIM" in r["status"] for r in gates)
    output_paths = [
        DOC_PATH,
        SOURCE_REGISTER_PATH,
        FILL_QUEUE_PATH,
        UA_KERNEL_CONTRACT_PATH,
        TEMPLATE_ROWS_PATH,
        PRIORITY_MATRIX_PATH,
        CLAIM_GATE_PATH,
        NEXT_TARGET_PATH,
        VALIDATION_PATH,
    ]
    scope_ok = all(str((ROOT / path).resolve()).startswith(str(ROOT.resolve())) for path in output_paths)

    checks = [
        row("VAL1408_0_sources", all_sources_ok, "all cited local source paths exist and anchors are present"),
        row("VAL1408_1_fill_queue", queue_ok, "fill queue prioritizes U_a, beta_EM/beta_nuc, and material tensor"),
        row("VAL1408_2_Ua_contract", ua_ok, "U_a kernel contract records missing source/readout/material inputs and anti-shortcuts"),
        row("VAL1408_3_templates", template_ok, "source-ready templates exist but values remain nonclaim missing"),
        row("VAL1408_4_priorities", priority_ok, "priority matrix keeps products last and U_a first"),
        row("VAL1408_5_claim_refusal", claim_ok, "U_a, sector beta, WEP, transfer, and local-GR claims are refused"),
        row("VAL1408_6_scope", scope_ok, "outputs are confined to post-checkpoint-work paths"),
    ]
    overall = all(check["status"] == "PASS" for check in checks)
    checks.append(
        row(
            "VAL1408_7_overall",
            overall,
            "1408 writes the nonclaim sector beta fill queue and U_a kernel contract without scoring WEP",
        )
    )
    return checks


def write_doc(
    sources: list[dict[str, Any]],
    queue: list[dict[str, Any]],
    ua: list[dict[str, Any]],
    templates: list[dict[str, Any]],
    priorities: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    body = f"""# 1408 — Sector-Beta Source Fill Queue And U_a Kernel Contract

**Status:** `{STATUS}`

**Current verdict:** this checkpoint does not score WEP. It turns the finite WEP branch into a fill queue: `U_a := K_ab(lambda,lab) alpha_source^b` is first, then `beta_EM`, `beta_nuc`, the full `Delta f_s,AB` material tensor, then `beta_e`, `beta_other`, and only last the products `P_s := beta_s^a U_a`.

**Discipline move:** no `P_s` product, WEP pressure score, or cross-arena transfer is allowed until `U_a`, each required `beta_s`, and the material tensor have source-backed rows with units, sign conventions, source anchors, and arena projections. `tau_WEP=1`, surrogate kernels, and one-pair cancellation remain forbidden.

**Claim ceiling:** `{CLAIM_CEILING}`

## Source Register

{md_table(sources)}

## Sector-Beta Source Fill Queue

{md_table(queue)}

## U_a Kernel Contract

{md_table(ua)}

## Source-Ready Template Rows

{md_table(templates)}

## Priority Decision Matrix

{md_table(priorities)}

## Claim Gate

{md_table(gates)}

## Next Target

{md_table(next_target)}

## Validation

{md_table(validation)}
"""
    (ROOT / DOC_PATH).write_text(body, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    queue = fill_queue_rows()
    ua = ua_kernel_contract_rows()
    templates = template_rows()
    priorities = priority_rows()
    gates = claim_gate_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, queue, ua, templates, priorities, gates)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(FILL_QUEUE_PATH, queue)
    write_csv(UA_KERNEL_CONTRACT_PATH, ua)
    write_csv(TEMPLATE_ROWS_PATH, templates)
    write_csv(PRIORITY_MATRIX_PATH, priorities)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(NEXT_TARGET_PATH, next_target)
    write_csv(VALIDATION_PATH, validation)
    write_doc(sources, queue, ua, templates, priorities, gates, next_target, validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"1408 validation failed: {failed}")
    print(STATUS)
    print(ROOT / DOC_PATH)
    print(ROOT / VALIDATION_PATH)


if __name__ == "__main__":
    main()
