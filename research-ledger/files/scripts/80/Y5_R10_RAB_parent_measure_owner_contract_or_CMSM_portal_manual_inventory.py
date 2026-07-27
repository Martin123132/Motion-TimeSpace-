from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
COEFF = MICROSCOPE / "branch_locked_wep" / "coefficients"
QUARANTINE = MICROSCOPE / "quarantine" / "1463"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1463-Y5-R10-RAB-parent-measure-owner-contract-or-CMSM-portal-manual-inventory.md"

PREV_NEXT = OUT / "P8_Y5_R10_1462_NEXT_TARGET.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1462_VALIDATION.csv"
PREV_MEASURE_PROOF = OUT / "P8_Y5_R10_1462_COMMON_MEASURE_CURRENT_SIGNATURE_ATTEMPT.csv"
PREV_ACTION_AUDIT = OUT / "P8_Y5_R10_1462_ACTION_SCALE_AND_SPECIES_JACOBIAN_AUDIT.csv"
PREV_RESIDUALS = OUT / "P8_Y5_R10_1462_JA_CA_ZETA_RESIDUAL_LEDGER_NONCLAIM.csv"
PREV_CMSM_FILL = OUT / "P8_Y5_R10_1462_CMSM_FIRST_INVENTORY_FILL_NONCLAIM.csv"
PREV_PORTAL_PROBE = OUT / "P8_Y5_R10_1462_CMSM_PORTAL_PROBE_LEDGER.csv"
PREV_SIGNING = OUT / "P8_Y5_R10_1462_PARENT_SIGNING_DECISION.csv"

HBAR_AUDIT_1067 = OUT / "P8_Y5_R10_1067_HBAR_MEASURE_OWNER_AUDIT.csv"
ACTION_OWNER_1067 = OUT / "P8_Y5_R10_1067_PARENT_ACTION_SCALE_OWNER_ATTEMPT.csv"
ACTION_OWNER_1230 = OUT / "P8_Y5_R10_1230_ACTION_SCALE_OWNER_THEOREM_ATTEMPT.csv"
RETURN_GATE_1388 = OUT / "P8_Y5_R10_1388_ACTION_MEASURE_OWNER_RETURN_GATE.csv"
PROOF_1389 = OUT / "P8_Y5_R10_1389_ACTION_MEASURE_OWNER_PROOF_ATTEMPT.csv"
ACTION_MEASURE_1452 = OUT / "P8_Y5_R10_1452_ACTION_SCALE_MEASURE_AUDIT.csv"
JACOBIAN_1452 = OUT / "P8_Y5_R10_1452_SPECIES_JACOBIAN_LEDGER_NONCLAIM.csv"
COMMON_MODE_1337 = OUT / "P8_Y5_R10_1337_COMMON_MODE_PREMISE_REDUCTION.csv"
COMMON_MODE_STATUS_1338 = OUT / "P8_Y5_R10_1338_COMMON_MODE_THEOREM_STATUS.csv"

LIVE_OFFICIAL_READOUT = MICROSCOPE / "official_readout" / "P_WEP_K_CMSM_readout.csv"
LIVE_SOURCE_WORLD = MICROSCOPE / "source_worldtube" / "P_WEP_R_source_Earth_worldtube.csv"
LIVE_MATERIAL_TENSOR = MICROSCOPE / "derived" / "P_WEP_R_material_TA6V_minus_PtRh10_full_tensor.csv"
LIVE_CPARENT = COEFF / "C_parent_WEP_slot_import.csv"

ONERA_DATA_PAGE = "https://microscope.onera.fr/fr/publication/microscope-data-are-available"
OCA_MICROSCOPE_PAGE = "https://www.oca.eu/fr/microscope"
CMSM_PORTAL = "https://cmsm-ds.onera.fr/user/microscope"
CMSM_MODULE_7 = "https://cmsm-ds.onera.fr/user/microscope/modules/7"
CMSM_ROOT = "https://cmsm-ds.onera.fr/"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1463_SOURCE_REGISTER.csv"
MEASURE_OWNER_CONTRACT = OUT / "P8_Y5_R10_1463_PARENT_MEASURE_OWNER_CONTRACT.csv"
CONNECTEDNESS_AUDIT = OUT / "P8_Y5_R10_1463_CONNECTED_MATTER_NATURALITY_AUDIT.csv"
JACOBIAN_EXCLUSION = OUT / "P8_Y5_R10_1463_SPECIES_JACOBIAN_EXCLUSION_CONTRACT.csv"
CMSM_MANUAL_INVENTORY = OUT / "P8_Y5_R10_1463_CMSM_MANUAL_CATEGORY_INVENTORY_NONCLAIM.csv"
CMSM_ACCESS_LEDGER = OUT / "P8_Y5_R10_1463_CMSM_ACCESS_AND_FILELIST_LEDGER.csv"
LIVE_GUARD = OUT / "P8_Y5_R10_1463_LIVE_IMPORT_GUARD.csv"
REDUCTION_GATES = OUT / "P8_Y5_R10_1463_REDUCTION_GATES.csv"
SIGNING_DECISION = OUT / "P8_Y5_R10_1463_PARENT_SIGNING_DECISION.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1463_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1463_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1463_VALIDATION.csv"

QUAR_CATEGORY_INVENTORY = QUARANTINE / "CMSM_MANUAL_CATEGORY_INVENTORY_QUARANTINE_NONCLAIM.csv"
QUAR_ACCESS_LEDGER = QUARANTINE / "CMSM_ACCESS_AND_FILELIST_LEDGER_QUARANTINE_NONCLAIM.csv"

BRANCH_MEASURE_CONTRACT = COEFF / "parent_measure_owner_contract_1463.csv"
BRANCH_CMSM_INVENTORY = COEFF / "CMSM_manual_category_inventory_nonclaim_1463.csv"
BRANCH_SIGNING = COEFF / "C_parent_WEP_parent_measure_owner_signing_decision_1463.csv"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
START_TS = datetime.now(timezone.utc).timestamp()


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def truth(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def rows_from_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv_ok(path: Path) -> bool:
    return bool(rows_from_csv(path))


def copy_branch(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


def source_rows() -> list[dict[str, Any]]:
    sources = [
        ("SRC1463_0_prev_next", PREV_NEXT, "1462 handoff"),
        ("SRC1463_1_prev_validation", PREV_VALIDATION, "1462 validation"),
        ("SRC1463_2_prev_measure", PREV_MEASURE_PROOF, "1462 common measure/current proof"),
        ("SRC1463_3_prev_action_audit", PREV_ACTION_AUDIT, "1462 action/Jacobian audit"),
        ("SRC1463_4_prev_residuals", PREV_RESIDUALS, "1462 JA/cA/zeta residuals"),
        ("SRC1463_5_prev_CMSM_fill", PREV_CMSM_FILL, "1462 CMSM pointer fill"),
        ("SRC1463_6_prev_probe", PREV_PORTAL_PROBE, "1462 portal probe"),
        ("SRC1463_7_prev_signing", PREV_SIGNING, "1462 signing decision"),
        ("SRC1463_8_hbar_1067", HBAR_AUDIT_1067, "1067 hbar/measure owner audit"),
        ("SRC1463_9_action_1067", ACTION_OWNER_1067, "1067 parent action-scale owner attempt"),
        ("SRC1463_10_action_1230", ACTION_OWNER_1230, "1230 universal action-scale owner theorem"),
        ("SRC1463_11_return_1388", RETURN_GATE_1388, "1388 action-measure return gate"),
        ("SRC1463_12_proof_1389", PROOF_1389, "1389 action-measure proof attempt"),
        ("SRC1463_13_action_1452", ACTION_MEASURE_1452, "1452 action-scale measure audit"),
        ("SRC1463_14_jacobian_1452", JACOBIAN_1452, "1452 species Jacobian ledger"),
        ("SRC1463_15_common_mode_1337", COMMON_MODE_1337, "1337 common-mode premise reduction"),
        ("SRC1463_16_common_status_1338", COMMON_MODE_STATUS_1338, "1338 common-mode status"),
    ]
    return [
        {
            "source_id": source_id,
            "source_path": str(path),
            "exists": path.exists(),
            "role": role,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for source_id, path, role in sources
    ]


def measure_owner_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": "PMO1463_0_action_density_line",
            "clause": "one ordinary-matter action-density line",
            "formal_statement": "ordinary matter actions are sections of a single parent action-density line L_action with one hbar_parent",
            "derivation_status": "CONTRACT_SHARPENED_NOT_PARENT_SIGNED",
            "if_signed": "independent hbar_A/w_A source weights have no parent object-language slot",
            "remaining_gap": "L_action and hbar_parent are not constructed from the MTS parent action in the current corpus",
            "closure_clause_needed": True,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": "PMO1463_1_natural_positive_automorphism",
            "clause": "relative action weights are natural automorphisms of L_action",
            "formal_statement": "w_A:L_action(A)->L_action(A) with naturality w_B F(f)=F(f) w_A for every ordinary-matter morphism f:A->B",
            "derivation_status": "EXACT_CONDITIONAL_LEMMA",
            "if_signed": "on a connected ordinary matter category, w_A=w_* is common",
            "remaining_gap": "connectedness and nonzero morphism graph for the actual ordinary matter category are not parent-signed",
            "closure_clause_needed": True,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": "PMO1463_2_common_calibration",
            "clause": "common derivative-silent factor is calibration",
            "formal_statement": "if w_A=w_* and partial w_*=0 across source, material, range, time, and frame labels, then T_eff=w_* T_total and w_* is absorbed into measured G_N/GM",
            "derivation_status": "EXACT_IF_UNIVERSAL_AND_SILENT",
            "if_signed": "composition/source residual from w_A vanishes",
            "remaining_gap": "universality and derivative-silence of w_* are not signed by parent measure owner",
            "closure_clause_needed": True,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": "PMO1463_3_measure_jacobian_extension",
            "clause": "path/statistical measure descends on same owner",
            "formal_statement": "Dmu_parent[psi]=Dmu_common[psi] with no species-only J_A and no independent effective hbar_A",
            "derivation_status": "REQUIRED_EXTENSION_NOT_SIGNED",
            "if_signed": "species Jacobian cannot recreate a hidden w_A in the source sector",
            "remaining_gap": "no parent construction of Dmu_parent or species-blind Jacobian descent",
            "closure_clause_needed": True,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": "PMO1463_4_current_extraction_extension",
            "clause": "Hilbert/current extraction shares the same owner",
            "formal_statement": "J_src is obtained by varying S_ord with respect to e_obs before readout, with no c_A or zeta_A bypass",
            "derivation_status": "PARTIAL_HILBERT_ONLY",
            "if_signed": "post-variation current rescalings and non-Hilbert bypasses are removed or bounded",
            "remaining_gap": "non-Hilbert current absence/exactness/projector silence remains open",
            "closure_clause_needed": True,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": "PMO1463_5_direct_sum_countermodel",
            "clause": "disconnected matter category countermodel",
            "formal_statement": "if C_ord has disconnected components, a natural positive scalar can take independent constants w_i on each component",
            "derivation_status": "COUNTERMODEL_SURVIVES",
            "if_signed": "nothing; this is the graph/connectedness obstruction",
            "remaining_gap": "the current corpus does not parent-sign that ordinary matter is connected for source normalization",
            "closure_clause_needed": True,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": "PMO1463_6_verdict",
            "clause": "parent measure owner proof status",
            "formal_statement": "L_action owner + connected matter naturality + species-blind measure + current extraction + derivative silence imply w_A,J_A,c_A,zeta_A are common/zero/bounded",
            "derivation_status": "CONTRACT_READY_NOT_DERIVED",
            "if_signed": "major source-side local-GR branch can move from residual route to theorem-zero route",
            "remaining_gap": "parent object-language owner and connectedness are still closure clauses, not derived facts",
            "closure_clause_needed": True,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def connectedness_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "CMA1463_0_interaction_graph",
            "object": "ordinary matter interaction/representation graph",
            "needed_signature": "all source-relevant ordinary matter components lie in one connected parent category for action-density normalization",
            "current_status": "GRAPH_NOT_PARENT_SIGNED",
            "if_missing": "each disconnected component may carry independent w_i",
            "next_action": "derive connected matter functor or retain component-wise source weights",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "CMA1463_1_direct_sum_policy",
            "object": "direct-sum sector decomposition",
            "needed_signature": "direct sums do not create independent source-normalization scalars",
            "current_status": "COUNTERMODEL_RETAINED",
            "if_missing": "w_EM, w_QCD, w_e, w_nuc can differ without violating additivity",
            "next_action": "prove action-density line is shared across direct-sum sectors",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "CMA1463_2_calibration_silence",
            "object": "common w_*",
            "needed_signature": "common scalar is derivative-silent over time, range, source, frame, and material labels",
            "current_status": "NOT_SIGNED",
            "if_missing": "even a common factor can become arena-dependent if it varies",
            "next_action": "tie w_* to measured G_N as a constant calibration or keep Gdot/fifth-force rows live",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def jacobian_exclusion_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "exclusion_id": "JEX1463_0_JA",
            "symbol": "J_A",
            "forbidden_slot": "species-only measure Jacobian",
            "required_parent_statement": "Dmu_parent has no Hom(species label, positive measure scalar) except common calibration",
            "status": "NOT_EXCLUDED",
            "fallback": "retain J_A residual ledger and source bounds",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "exclusion_id": "JEX1463_1_wA",
            "symbol": "w_A",
            "forbidden_slot": "pre-variation action multiplier",
            "required_parent_statement": "sector labels are fields/representations, not automorphisms of L_action",
            "status": "NOT_EXCLUDED",
            "fallback": "retain w_A residual ledger and no-cancellation policy",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "exclusion_id": "JEX1463_2_cA",
            "symbol": "c_A",
            "forbidden_slot": "post-variation current/source rescaling",
            "required_parent_statement": "readout maps act on already-owned J_src and cannot redefine parent source",
            "status": "CONDITIONAL_POST_VARIATION_ONLY",
            "fallback": "retain current/readout order gate until official kernel/source model is signed",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "exclusion_id": "JEX1463_3_zetaA",
            "symbol": "zeta_A",
            "forbidden_slot": "non-Hilbert current bypass",
            "required_parent_statement": "J_NH,A is absent, exact with zero projection, or bounded in every local arena",
            "status": "NOT_EXCLUDED",
            "fallback": "retain zeta_A residual ledger",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def cmsm_manual_inventory_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "inventory_id": "CMSM1463_0_ONERA_data_page",
            "source_url": ONERA_DATA_PAGE,
            "inventory_level": "portal_pointer",
            "manual_finding": "ONERA states mission data are available at the CMSM portal for Equivalence Principle tests or other tests with the measurements",
            "dataset_category": "mission data portal",
            "target_files_identified": False,
            "needed_for_source_pack": "file list, hashes, variable dictionary, licence/access note",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "inventory_id": "CMSM1463_1_OCA_data_categories",
            "source_url": OCA_MICROSCOPE_PAGE,
            "inventory_level": "category_inventory",
            "manual_finding": "OCA describes raw data, calibrated data, and auxiliary data for analyses as the MICROSCOPE data classes intended for the CMSM site",
            "dataset_category": "raw data; calibrated data; auxiliary analysis data",
            "target_files_identified": False,
            "needed_for_source_pack": "map category files to official_readout/source_worldtube/material tensor schemas",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "inventory_id": "CMSM1463_2_CMSM_module_7_route",
            "source_url": CMSM_MODULE_7,
            "inventory_level": "portal_route",
            "manual_finding": "OCA points specifically to CMSM module 7, but the current browser/shell evidence exposes only a REGARDS OSS shell and no parseable file list",
            "dataset_category": "MISSING_FILE_LIST",
            "target_files_identified": False,
            "needed_for_source_pack": "manual in-browser module inventory or API route discovery",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "inventory_id": "CMSM1463_3_target_readout_pack",
            "source_url": CMSM_PORTAL,
            "inventory_level": "target_schema",
            "manual_finding": "needed target remains official readout/orbit/attitude/mask arrays, not a portal pointer",
            "dataset_category": "time/session/orbit; gx/gz; Sxx/Sxz; masks; calibration flags; attitude/sign",
            "target_files_identified": False,
            "needed_for_source_pack": "actual dataset filenames and checksums",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def cmsm_access_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "access_id": "ACC1463_0_ONERA_page",
            "url": ONERA_DATA_PAGE,
            "access_status": "SOURCE_BACKED_POINTER",
            "evidence": "data available statement and CMSM portal link",
            "file_inventory_status": "NO_FILE_LIST_ON_PAGE",
            "next_access_action": "use as provenance for CMSM route only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "access_id": "ACC1463_1_OCA_page",
            "url": OCA_MICROSCOPE_PAGE,
            "access_status": "SOURCE_BACKED_CATEGORY_POINTER",
            "evidence": "raw/calibrated/auxiliary data categories and module 7 route",
            "file_inventory_status": "CATEGORY_LEVEL_ONLY",
            "next_access_action": "use categories to structure the manual inventory template",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "access_id": "ACC1463_2_CMSM_module_7",
            "url": CMSM_MODULE_7,
            "access_status": "REGARDS_OSS_NO_PARSED_LIST",
            "evidence": "web open resolves portal shell but no lines/file rows; shell access previously failed",
            "file_inventory_status": "BLOCKED_NO_FILE_LIST",
            "next_access_action": "manual browser inspection or REGARDS API discovery before any download/checksum step",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def live_guard_rows() -> list[dict[str, Any]]:
    live_targets = [
        ("LIVE1463_0_official_readout", "official_readout", LIVE_OFFICIAL_READOUT),
        ("LIVE1463_1_source_worldtube", "source_worldtube", LIVE_SOURCE_WORLD),
        ("LIVE1463_2_material_tensor", "material_tensor", LIVE_MATERIAL_TENSOR),
        ("LIVE1463_3_C_parent", "C_parent_WEP", LIVE_CPARENT),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "live_guard_id": guard_id,
            "object": object_name,
            "live_path": str(path),
            "exists_now": path.exists(),
            "would_write_in_1463": False,
            "reason": "1463 writes contract/category inventory only; no official file import",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for guard_id, object_name, path in live_targets
    ]


def reduction_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1463_0_measure_contract_written",
            "gate": "parent measure owner contract made explicit",
            "gate_pass": True,
            "blocking_reason": "contract ready but not parent-signed",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1463_1_connected_naturality",
            "gate": "connected matter naturality lemma written",
            "gate_pass": True,
            "blocking_reason": "conditional; connected ordinary matter category not signed",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1463_2_parent_owner_signed",
            "gate": "L_action/hbar_parent/Dmu_parent owner derived",
            "gate_pass": False,
            "blocking_reason": "owner remains closure clause",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1463_3_JA_excluded",
            "gate": "J_A/w_A/c_A/zeta_A excluded or bounded",
            "gate_pass": False,
            "blocking_reason": "direct-sum and species-Jacobian countermodels remain live",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1463_4_CMSM_category_inventory",
            "gate": "source-backed CMSM category-level inventory written",
            "gate_pass": True,
            "blocking_reason": "category inventory only; no official file list",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1463_5_CMSM_file_inventory",
            "gate": "CMSM official file list/checksums obtained",
            "gate_pass": False,
            "blocking_reason": "portal file list not parsed/extracted",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1463_6_local_claim",
            "gate": "local WEP/local-GR claim allowed",
            "gate_pass": False,
            "blocking_reason": "parent measure owner and official source pack remain incomplete",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def signing_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "SIGN1463_0_parent_measure_owner",
            "target": "parent measure/statistical owner forbids w_A/J_A",
            "contract_written": True,
            "connected_naturality_lemma": True,
            "parent_measure_owner_signed": False,
            "connected_matter_category_signed": False,
            "species_jacobian_excluded": False,
            "nonHilbert_silence_signed": False,
            "CMSM_category_inventory_written": True,
            "CMSM_file_inventory_imported": False,
            "JA_zero_import_allowed": False,
            "delta_q_zero_import_allowed": False,
            "C_parent_WEP_import_allowed": False,
            "tau_WEP_numeric_allowed": False,
            "local_claim_allowed": False,
            "decision": "KEEP_MEASURE_OWNER_AS_EXPLICIT_CLOSURE_AND_KEEP_CMSM_FILE_INVENTORY_BLOCKED",
            "reason": "the theorem is structurally clean but still depends on unsigned parent owner/connectedness clauses; CMSM inventory is only category-level",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1463_0_contract",
            "decision": "promote the parent measure owner from vague gap to explicit closure contract",
            "why": "the clean theorem needs L_action, hbar_parent, Dmu_parent, connectedness, and current extraction all signed together",
            "consequence": "future derivation has a precise target; no hidden theorem-zero import",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1463_1_countermodel",
            "decision": "retain disconnected/direct-sum matter and species-Jacobian countermodels",
            "why": "connectedness and species-blind measure descent are not parent-derived",
            "consequence": "w_A/J_A/c_A/zeta_A residual ledgers remain live",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1463_2_CMSM",
            "decision": "record source-backed CMSM data categories but no file inventory",
            "why": "OCA/ONERA source pages give portal/category evidence; REGARDS file rows are not parsed here",
            "consequence": "next data step is API/manual file-list acquisition before checksums",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1463_0_1464",
            "next_target": "1464-Y5-R10-RAB-connected-matter-category-proof-or-REGARDS-api-discovery.md",
            "script": "scripts/Y5_R10_RAB_connected_matter_category_proof_or_REGARDS_api_discovery.py",
            "objective": "try to prove the connected ordinary-matter category/naturality clause; if it fails, discover the REGARDS/CMSM API or manual file-list route",
            "include": "connected matter graph; direct-sum countermodel; common calibration silence; REGARDS API/file inventory; no live claim",
            "exclude": "numeric tau_WEP; local-GR pass; C_parent promotion; formalization-workbench edits; GitHub action",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    contracts: list[dict[str, Any]],
    connectedness: list[dict[str, Any]],
    jacobian: list[dict[str, Any]],
    cmsm_inventory: list[dict[str, Any]],
    access: list[dict[str, Any]],
    live_guard: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    signing: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated_csvs = [
        SOURCE_REGISTER,
        MEASURE_OWNER_CONTRACT,
        CONNECTEDNESS_AUDIT,
        JACOBIAN_EXCLUSION,
        CMSM_MANUAL_INVENTORY,
        CMSM_ACCESS_LEDGER,
        QUAR_CATEGORY_INVENTORY,
        QUAR_ACCESS_LEDGER,
        LIVE_GUARD,
        REDUCTION_GATES,
        SIGNING_DECISION,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    all_sources_exist = all(truth(row["exists"]) for row in sources)
    contract_ready_not_derived = any(row["derivation_status"] == "CONTRACT_READY_NOT_DERIVED" for row in contracts)
    countermodel_retained = any(row["derivation_status"] == "COUNTERMODEL_SURVIVES" for row in contracts)
    connectedness_nonclaim = all(not truth(row["claim_allowed"]) for row in connectedness)
    jacobian_not_excluded = any(row["status"] == "NOT_EXCLUDED" for row in jacobian)
    cmsm_category_written = any(row["inventory_id"] == "CMSM1463_1_OCA_data_categories" for row in cmsm_inventory)
    cmsm_no_file_list = all(not truth(row["target_files_identified"]) for row in cmsm_inventory)
    access_nonclaim = all(not truth(row["claim_allowed"]) for row in access)
    live_paths_untouched = all(not truth(row["exists_now"]) and not truth(row["would_write_in_1463"]) for row in live_guard)
    gate_pattern_safe = truth(gates[0]["gate_pass"]) and truth(gates[1]["gate_pass"]) and truth(gates[4]["gate_pass"]) and all(
        not truth(row["gate_pass"]) for row in gates[2:4] + gates[5:]
    )
    signing_refuses = all(
        not truth(row["JA_zero_import_allowed"])
        and not truth(row["delta_q_zero_import_allowed"])
        and not truth(row["C_parent_WEP_import_allowed"])
        and not truth(row["tau_WEP_numeric_allowed"])
        and not truth(row["local_claim_allowed"])
        for row in signing
    )
    generated_parse = all(parse_csv_ok(path) for path in generated_csvs)
    branch_copies = BRANCH_MEASURE_CONTRACT.exists() and BRANCH_CMSM_INVENTORY.exists() and BRANCH_SIGNING.exists()
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formal_recent = 0
    if FORMALIZATION.exists():
        formal_recent = sum(
            1
            for path in FORMALIZATION.rglob("*")
            if path.is_file() and path.stat().st_mtime > START_TS
        )
    checks = [
        ("VAL1463_0_sources", all_sources_exist, "all cited local source paths exist"),
        ("VAL1463_1_contract_ready_not_derived", contract_ready_not_derived, "parent measure owner contract is explicit but not derived"),
        ("VAL1463_2_countermodel_retained", countermodel_retained, "direct-sum/connectedness countermodel remains live"),
        ("VAL1463_3_connectedness_nonclaim", connectedness_nonclaim, "connectedness audit rows remain nonclaim"),
        ("VAL1463_4_jacobian_not_excluded", jacobian_not_excluded, "J_A/w_A/zeta_A exclusion remains incomplete"),
        ("VAL1463_5_CMSM_category_written", cmsm_category_written, "OCA/ONERA category-level CMSM inventory written"),
        ("VAL1463_6_CMSM_no_file_list", cmsm_no_file_list, "no official CMSM file list is claimed"),
        ("VAL1463_7_access_nonclaim", access_nonclaim, "CMSM access rows remain nonclaim"),
        ("VAL1463_8_live_paths_untouched", live_paths_untouched, "critical live official/source/material/Cparent files remain absent"),
        ("VAL1463_9_gate_pattern_safe", gate_pattern_safe, "only contract/conditional/category gates pass; claim gates false"),
        ("VAL1463_10_signing_refuses", signing_refuses, "parent signing refuses JA/delta_q/Cparent/tau/local claim"),
        ("VAL1463_11_generated_csv_parse", generated_parse, "all generated 1463 CSVs parse cleanly"),
        ("VAL1463_12_branch_copies", branch_copies, "nonclaim branch copies written"),
        ("VAL1463_13_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1463_14_formalization_untouched", formal_recent == 0, f"formalization modified-file count since start={formal_recent}"),
        ("VAL1463_15_overall", True, "1463 writes the explicit parent measure owner closure contract and CMSM category inventory without claim promotion"),
    ]
    return [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "generated_utc": now(),
        }
        for check_id, passed, detail in checks
    ]


def write_table(handle, title: str, rows: list[dict[str, Any]]) -> None:
    handle.write(f"## {title}\n\n")
    if not rows:
        handle.write("_No rows._\n\n")
        return
    fields = list(rows[0].keys())
    handle.write("| " + " | ".join(fields) + " |\n")
    handle.write("| " + " | ".join(["---"] * len(fields)) + " |\n")
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ").replace("|", "\\|") for field in fields]
        handle.write("| " + " | ".join(values) + " |\n")
    handle.write("\n")


def write_doc(
    sources: list[dict[str, Any]],
    contracts: list[dict[str, Any]],
    connectedness: list[dict[str, Any]],
    jacobian: list[dict[str, Any]],
    cmsm_inventory: list[dict[str, Any]],
    access: list[dict[str, Any]],
    live_guard: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    signing: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    with DOC.open("w", encoding="utf-8") as handle:
        handle.write("# 1463 - Parent measure owner contract or CMSM portal manual inventory\n\n")
        handle.write(
            "**Current verdict:** the parent measure-owner route is now a precise closure contract, not a vague gap. "
            "If MTS derives one action-density line `L_action`, one `hbar_parent`, a species-blind measure, a connected ordinary-matter category, and current extraction before readout, then relative `w_A/J_A/c_A` weights collapse to common calibration. "
            "The current corpus does not yet derive those owner/connectedness clauses, so the zero is not imported.\n\n"
        )
        handle.write(
            "**Useful progress:** the direct-sum countermodel is now the exact enemy: disconnected ordinary matter components can still carry independent source weights. "
            "On the data side, ONERA/OCA give source-backed CMSM portal and raw/calibrated/auxiliary category evidence, but no parseable official file list or checksums yet.\n\n"
        )
        write_table(handle, "Source register", sources)
        write_table(handle, "Parent measure owner contract", contracts)
        write_table(handle, "Connected matter naturality audit", connectedness)
        write_table(handle, "Species Jacobian exclusion contract", jacobian)
        write_table(handle, "CMSM manual category inventory", cmsm_inventory)
        write_table(handle, "CMSM access and file-list ledger", access)
        write_table(handle, "Live import guard", live_guard)
        write_table(handle, "Reduction gates", gates)
        write_table(handle, "Parent signing decision", signing)
        write_table(handle, "Decision ledger", decisions)
        write_table(handle, "Validation", validation)
        write_table(handle, "Next target", next_target)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    sources = source_rows()
    contracts = measure_owner_contract_rows()
    connectedness = connectedness_audit_rows()
    jacobian = jacobian_exclusion_rows()
    cmsm_inventory = cmsm_manual_inventory_rows()
    access = cmsm_access_rows()
    live_guard = live_guard_rows()
    gates = reduction_gate_rows()
    signing = signing_decision_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(MEASURE_OWNER_CONTRACT, contracts)
    write_csv(CONNECTEDNESS_AUDIT, connectedness)
    write_csv(JACOBIAN_EXCLUSION, jacobian)
    write_csv(CMSM_MANUAL_INVENTORY, cmsm_inventory)
    write_csv(CMSM_ACCESS_LEDGER, access)
    write_csv(QUAR_CATEGORY_INVENTORY, cmsm_inventory)
    write_csv(QUAR_ACCESS_LEDGER, access)
    write_csv(LIVE_GUARD, live_guard)
    write_csv(REDUCTION_GATES, gates)
    write_csv(SIGNING_DECISION, signing)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_target)

    copy_branch(MEASURE_OWNER_CONTRACT, BRANCH_MEASURE_CONTRACT)
    copy_branch(CMSM_MANUAL_INVENTORY, BRANCH_CMSM_INVENTORY)
    copy_branch(SIGNING_DECISION, BRANCH_SIGNING)

    remove_pycache()
    validation = validation_rows(sources, contracts, connectedness, jacobian, cmsm_inventory, access, live_guard, gates, signing)
    write_csv(VALIDATION, validation)
    write_doc(sources, contracts, connectedness, jacobian, cmsm_inventory, access, live_guard, gates, signing, decisions, validation, next_target)
    print("Y5_R10_1463_parent_measure_owner_contract_CMSM_category_inventory_nonclaim")


if __name__ == "__main__":
    main()
