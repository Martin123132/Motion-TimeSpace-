from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
COEFF = MICROSCOPE / "branch_locked_wep" / "coefficients"
QUARANTINE = MICROSCOPE / "quarantine" / "1609"
INPUT = QUARANTINE / "input"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1609-Y5-R2FR-CMSM-source-pack-capture-or-parent-nondegeneracy-theorem.md"

SOURCE_FILES = {
    "1608_doc": ROOT / "1608-Y5-R2FR-tau-WEP-readout-kernel-or-material-tensor-source-file.md",
    "1608_validation": OUT / "P8_Y5_BRR545_1608_VALIDATION.csv",
    "1608_next": OUT / "P8_Y5_PARENT_QLOC_1608_NEXT_TARGET.csv",
    "1608_inventory": OUT / "P8_Y5_PARENT_QLOC_1608_INPUT_INVENTORY.csv",
    "1608_nondeg": OUT / "P8_Y5_PARENT_QLOC_1608_NONDEGENERACY_THEOREM_STATUS.csv",
    "1608_tau": OUT / "P8_Y5_PARENT_QLOC_1608_TAU_LOWER_BOUND_STATUS.csv",
    "1598_probe": OUT / "P8_Y5_PARENT_QLOC_1598_CMSM_PORTAL_PROBE_SYNTHESIS.csv",
    "1598_requirements": OUT / "P8_Y5_PARENT_QLOC_1598_ALIGNMENT_IMPORT_REQUIREMENTS.csv",
    "1597_null": OUT / "P8_Y5_PARENT_QLOC_1597_NULL_SPACE_COUNTERMODEL.csv",
    "1597_inputs": OUT / "P8_Y5_PARENT_QLOC_1597_REQUIRED_NONDEGENERACY_INPUTS.csv",
    "1465_capture_plan": COEFF / "CMSM_session_filelist_capture_plan_nonclaim_1465.csv",
    "1466_capture_workflow": COEFF / "CMSM_browser_session_capture_workflow_nonclaim_1466.csv",
    "1464_regards": COEFF / "REGARDS_api_filelist_route_nonclaim_1464.csv",
    "1462_inventory": COEFF / "CMSM_first_inventory_fill_nonclaim_1462.csv",
    "1600_har": OUT / "P8_Y5_PARENT_QLOC_1600_HAR_INTAKE_STATUS.csv",
}

NEEDLES = {
    "1608_doc": ["TAU1608_4_verdict", "TAU_WEP_NOT_EVALUATED"],
    "1608_validation": ["VAL1608_OVERALL", "PASS"],
    "1608_next": ["1609-Y5-R2FR-CMSM-source-pack-capture-or-parent-nondegeneracy-theorem.md", "c_min>0"],
    "1608_inventory": ["INV1608_0_K_CMSM_readout", "MISSING_INPUT_FILE"],
    "1608_nondeg": ["NDG1608_2_data_theorem_equivalence", "OFFICIAL_READOUT_OR_PARENT_ALIGNMENT_REQUIRED"],
    "1608_tau": ["TLS1608_6_verdict", "official input or parent nondegeneracy missing"],
    "1598_probe": ["CPS1598_3_current_shell_probe", "TIMEOUT_OR_NO_USABLE_FILELIST"],
    "1598_requirements": ["AIR1598_4_alignment", "MISSING_CRITICAL_ALIGNMENT"],
    "1597_null": ["NSC1597_0_linear_space_model", "tau_WEP can vanish"],
    "1597_inputs": ["NDI1597_3_alignment", "MISSING_CRITICAL"],
    "1465_capture_plan": ["CAP1465_1_filelist_fields", "MISSING_FILELIST"],
    "1466_capture_workflow": ["CAP1466_5_import_guard", "GUARD_ACTIVE_NONCLAIM"],
    "1464_regards": ["REG1464_2_CMSM_shell_probe", "BLOCKED_NO_FILE_ROWS"],
    "1462_inventory": ["CMSM1462_0_ONERA_data_available_page", "portal_pointer_not_dataset_file"],
    "1600_har": ["HAR1600_0_input_folder_empty", "NO_HAR_JSON_CSV_EVIDENCE_PRESENT"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1609_SOURCE_REGISTER.csv"
WEB_PROBE = OUT / "P8_Y5_PARENT_QLOC_1609_WEB_PROBE_LEDGER.csv"
SOURCE_PACK_SCHEMA = OUT / "P8_Y5_PARENT_QLOC_1609_CMSM_SOURCE_PACK_SCHEMA.csv"
SOURCE_PACK_TEMPLATE = OUT / "P8_Y5_PARENT_QLOC_1609_CMSM_SOURCE_PACK_TEMPLATE.csv"
SOURCE_PACK_INVENTORY = OUT / "P8_Y5_PARENT_QLOC_1609_CMSM_SOURCE_PACK_INVENTORY.csv"
NONDEG_NO_GO = OUT / "P8_Y5_PARENT_QLOC_1609_PARENT_NONDEGENERACY_NO_GO.csv"
ALIGNMENT_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_1609_ALIGNMENT_COMPUTATION_CONTRACT.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1609_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1609_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1609_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1609_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1609_VALIDATION.csv"

COPY_TARGETS = {
    WEB_PROBE: [
        QUARANTINE / "WEB_PROBE_LEDGER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_web_probe_ledger_nonclaim_1609.csv",
    ],
    SOURCE_PACK_SCHEMA: [
        QUARANTINE / "CMSM_SOURCE_PACK_SCHEMA_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_CMSM_source_pack_schema_nonclaim_1609.csv",
    ],
    SOURCE_PACK_TEMPLATE: [
        INPUT / "CMSM_source_pack_TEMPLATE.csv",
        BRANCH_RESIDUALS / "R2FR_CMSM_source_pack_template_nonclaim_1609.csv",
    ],
    SOURCE_PACK_INVENTORY: [
        QUARANTINE / "CMSM_SOURCE_PACK_INVENTORY_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_CMSM_source_pack_inventory_nonclaim_1609.csv",
    ],
    NONDEG_NO_GO: [
        QUARANTINE / "PARENT_NONDEGENERACY_NO_GO_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_parent_nondegeneracy_no_go_nonclaim_1609.csv",
    ],
    ALIGNMENT_CONTRACT: [
        QUARANTINE / "ALIGNMENT_COMPUTATION_CONTRACT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_alignment_computation_contract_nonclaim_1609.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE_CLOSED.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_closed_1609.csv",
    ],
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (source_id, path) in enumerate(SOURCE_FILES.items()):
        text = read_text(path) if path.exists() else ""
        needles = NEEDLES[source_id]
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1609_{index}_{source_id}",
                "source_path": rel(path) if path.exists() else str(path),
                "exists": path.exists(),
                "needle_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "source_role": "1609_CMSM_source_pack_or_parent_nondegeneracy_input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def web_probe_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "probe_id": "WEB1609_0_ONERA_data_page",
            "url": "https://microscope.onera.fr/fr/publication/microscope-data-are-available",
            "method": "GET via local PowerShell probe plus web search",
            "status": "HTTP_200_POINTER_ONLY",
            "evidence": "page metadata says mission data are available at https://cmsm-ds.onera.fr/user/microscope",
            "filelist_acquired": False,
            "checksums_acquired": False,
            "download_urls_acquired": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "probe_id": "WEB1609_1_CMSM_root",
            "url": "https://cmsm-ds.onera.fr/",
            "method": "HEAD via local PowerShell probe",
            "status": "TIMEOUT_FROM_SHELL",
            "evidence": "no parseable file list, checksum or download URL acquired",
            "filelist_acquired": False,
            "checksums_acquired": False,
            "download_urls_acquired": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "probe_id": "WEB1609_2_CMSM_user_microscope",
            "url": "https://cmsm-ds.onera.fr/user/microscope",
            "method": "GET/HEAD via local PowerShell probe",
            "status": "TIMEOUT_FROM_SHELL",
            "evidence": "route remains a portal pointer in this environment",
            "filelist_acquired": False,
            "checksums_acquired": False,
            "download_urls_acquired": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "probe_id": "WEB1609_3_CMSM_module_7",
            "url": "https://cmsm-ds.onera.fr/user/microscope/modules/7",
            "method": "GET/HEAD via local PowerShell probe",
            "status": "TIMEOUT_FROM_SHELL",
            "evidence": "authenticated/browser session or HAR capture still required",
            "filelist_acquired": False,
            "checksums_acquired": False,
            "download_urls_acquired": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "probe_id": "WEB1609_4_dataobjects_search",
            "url": "https://cmsm-ds.onera.fr/user/microscope/api/v1/rs-access-project/dataobjects/search",
            "method": "GET/HEAD via local PowerShell probe",
            "status": "TIMEOUT_FROM_SHELL",
            "evidence": "no REGARDS dataobject rows acquired",
            "filelist_acquired": False,
            "checksums_acquired": False,
            "download_urls_acquired": False,
            "claim_allowed": False,
        },
    ]


def source_pack_schema_rows() -> list[dict[str, Any]]:
    fields = [
        ("dataset_id", "official CMSM/REGARDS dataset id"),
        ("product_id", "official product/dataobject id"),
        ("file_name", "official file name"),
        ("file_role", "K_CMSM_readout|orbit_attitude|masks|source_worldtube|material_tensor|normalization|alignment_result|other"),
        ("download_url", "official download URL or access route"),
        ("checksum", "official checksum or local sha256 after official download"),
        ("byte_count", "official or locally verified byte count"),
        ("row_count", "parsed row count if tabular"),
        ("metadata_schema", "declared schema/format"),
        ("licence_access", "licence/access note"),
        ("required_columns_found", "true only if role-specific columns are present"),
        ("units_sign_basis_found", "true only if units, signs and branch basis are declared"),
        ("quarantine_path", "local quarantine file path"),
        ("no_surrogate", "true for official or exact equivalent; false rejects claim promotion"),
        ("valid_for_claim", "false until all branch gates pass"),
        ("claim_allowed", "false until full branch validation passes"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "schema_id": f"CSP1609_{index}_{field}",
            "field": field,
            "required_policy": policy,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for index, (field, policy) in enumerate(fields)
    ]


def source_pack_template_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "template_id": "CSPT1609_0_source_pack_template",
            "dataset_id": "MISSING_DATASET_ID",
            "product_id": "MISSING_PRODUCT_ID",
            "file_name": "MISSING_FILE_NAME",
            "file_role": "MISSING_FILE_ROLE",
            "download_url": "MISSING_DOWNLOAD_URL",
            "checksum": "MISSING_CHECKSUM",
            "byte_count": "MISSING_BYTE_COUNT",
            "row_count": "MISSING_ROW_COUNT",
            "metadata_schema": "MISSING_SCHEMA",
            "licence_access": "MISSING_ACCESS_NOTE",
            "required_columns_found": False,
            "units_sign_basis_found": False,
            "quarantine_path": "source-intake/microscope/quarantine/1609/input/MISSING_FILE",
            "no_surrogate": False,
            "parser_status": "TEMPLATE_ONLY_NOT_IMPORTABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def expected_source_pack_paths() -> list[tuple[str, Path]]:
    return [
        ("source_pack_filelist", INPUT / "CMSM_source_pack_filelist.csv"),
        ("download_hash_ledger", INPUT / "CMSM_download_hash_ledger.csv"),
        ("K_CMSM_readout", INPUT / "K_CMSM_readout.csv"),
        ("orbit_attitude", INPUT / "orbit_attitude.csv"),
        ("masks_segments", INPUT / "masks_segments.csv"),
        ("source_worldtube", INPUT / "source_worldtube.csv"),
        ("material_tensor", INPUT / "material_tensor.csv"),
        ("alignment_result", INPUT / "alignment_result.csv"),
    ]


def source_pack_inventory_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (role, path) in enumerate(expected_source_pack_paths()):
        exists = path.exists()
        row_count = 0
        status = "MISSING_INPUT_FILE"
        if exists:
            try:
                row_count = len(read_csv(path))
                status = "PRESENT_NEEDS_VALIDATION" if row_count else "PRESENT_EMPTY_REJECT"
            except Exception:
                status = "PRESENT_PARSE_ERROR_REJECT"
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "inventory_id": f"CSPI1609_{index}_{role}",
                "file_role": role,
                "path": rel(path) if exists else str(path),
                "exists": exists,
                "row_count": row_count,
                "status": status,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def nondeg_no_go_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "NDG1609_0_vector_space_no_go",
            "statement": "For any nonzero linear functional K on a vector space with dimension >=2, ker(K) contains nonzero vectors V, so K!=0 and V!=0 do not imply <K,V>!=0.",
            "proof_status": "EXACT_NO_GO_COUNTERMODEL",
            "effect": "generic parent nondegeneracy cannot be inferred from nonzero factors",
            "needed_to_escape": "restrict V_source_material to a cone/subspace disjoint from ker(K), or compute official alignment",
            "theorem_closed": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "NDG1609_1_positive_cone_route",
            "statement": "A positive lower bound could follow if K is strictly positive on the allowed source-material cone and V is constrained to that cone with a norm lower bound.",
            "proof_status": "CONDITIONAL_ROUTE_IDENTIFIED",
            "effect": "possible parent theorem target",
            "needed_to_escape": "parent-signed positivity/cone theorem for K_CMSM and V_source_material",
            "theorem_closed": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "NDG1609_2_data_route",
            "statement": "Official data can close the branch by directly computing projection value, norms, c_min, tau_min and uncertainty.",
            "proof_status": "DATA_ROUTE_REMAINS_PRIMARY",
            "effect": "source-pack capture/import is the cleanest next empirical step",
            "needed_to_escape": "official filelist/checksums/readout/source/material/alignment rows",
            "theorem_closed": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "NDG1609_3_verdict",
            "statement": "Parent nondegeneracy c_min>0 is not derived in 1609; the exact no-go clarifies the missing positivity/alignment assumption.",
            "proof_status": "PARENT_NONDEGENERACY_NOT_DERIVED",
            "effect": "tau_min remains missing",
            "needed_to_escape": "official alignment computation or parent cone/non-null theorem",
            "theorem_closed": False,
            "claim_allowed": False,
        },
    ]


def alignment_contract_rows() -> list[dict[str, Any]]:
    rows = [
        ("ALI1609_0_K_norm", "K_norm", "||K_CMSM||", "positive numeric norm with units and source file", "MISSING"),
        ("ALI1609_1_V_norm", "V_norm", "||S_Earth x M_TiPt||", "positive source-material vector norm in same basis", "MISSING"),
        ("ALI1609_2_projection", "projection_value", "<K_CMSM,V_source_material>", "signed/absolute projection value with uncertainty", "MISSING"),
        ("ALI1609_3_c_min", "c_min", "|projection|/(||K|| ||V||)", "strictly positive lower bound with confidence/assumptions", "MISSING_CRITICAL"),
        ("ALI1609_4_tau_min", "tau_min", "c_min*K_min*S_min*M_min/N_max or direct tau lower bound", "strictly positive lower bound", "MISSING_CRITICAL"),
        ("ALI1609_5_no_cancellation", "no_cancellation", "signed kernel/covariance rule", "no silent orbit/material cancellation", "MISSING"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "alignment_id": alignment_id,
            "object": obj,
            "formula_or_field": formula,
            "required_evidence": evidence,
            "current_status": status,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for alignment_id, obj, formula, evidence, status in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1609_0_source_pack",
            "acceptance_rule": "source-pack import requires filelist, checksums/download URLs, official readout/source/material files and role-specific columns",
            "input_state": "ONERA pointer only; CMSM shell probes timeout; local input files missing",
            "runner_result": "NO_SOURCE_PACK_ACCEPTED",
            "effect": "official data route remains open but not imported",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1609_1_nondegeneracy",
            "acceptance_rule": "parent theorem must exclude nonzero V in ker(K) and provide c_min>0",
            "input_state": "exact no-go countermodel applies without positivity/alignment restriction",
            "runner_result": "REJECT_PARENT_NONDEGENERACY_THEOREM",
            "effect": "tau_min remains missing",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1609_2_shortcuts",
            "acceptance_rule": "tau_eff=1, surrogate arrays, symbolic K alone, bound inversion and measured-G absorption are forbidden",
            "input_state": "no official alignment or parent theorem",
            "runner_result": "SHORTCUTS_REJECTED",
            "effect": "no WEP/local-GR promotion",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG1609_0_filelist", "CMSM official filelist", "BLOCKED", "no filelist/checksum/download URL acquired"),
        ("CG1609_1_readout", "K_CMSM readout arrays", "BLOCKED", "no official readout/design matrix imported"),
        ("CG1609_2_alignment", "c_min/tau_min alignment lower bound", "BLOCKED", "null-space countermodel remains"),
        ("CG1609_3_parent_theorem", "parent nondegeneracy theorem", "BLOCKED", "exact vector-space no-go unless extra positivity/cone restriction is signed"),
        ("CG1609_4_delta_w_bound", "Delta_w_TiPt numeric bound", "BLOCKED", "tau_min missing"),
        ("CG1609_5_WEP_local_GR", "WEP/Newton/local-GR claim", "BLOCKED", "source-pack/tau/material/coupling gates open"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim, status, reason in gates
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1609_0_source_pack",
            "decision": "CMSM_SOURCE_PACK_NOT_CAPTURED",
            "reason": "ONERA pointer is reachable, but CMSM routes timed out from shell and no filelist/checksum/download URL was acquired",
            "next_action": "use browser/HAR authenticated capture or manually supply CMSM source-pack rows to quarantine/1609/input",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1609_1_nondegeneracy",
            "decision": "PARENT_NONDEGENERACY_NOT_DERIVED_NO_GO_RECORDED",
            "reason": "nonzero factors do not exclude V in ker(K); a positive cone/alignment theorem or official computation is required",
            "next_action": "attempt parent positivity/cone theorem or compute alignment from official K/V data",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1609_2_next",
            "decision": "NEXT_1610_BROWSER_HAR_SOURCE_PACK_OR_POSITIVE_CONE_NONDEGENERACY",
            "reason": "the remaining decisive routes are authenticated source-pack capture or a parent positivity theorem for the readout pairing",
            "next_action": "operate browser/HAR capture against CMSM module 7, or prove K is positive on the allowed source-material cone",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1610-Y5-R2FR-browser-HAR-source-pack-or-positive-cone-nondegeneracy.md",
            "script": "scripts/Y5_R2FR_browser_HAR_source_pack_or_positive_cone_nondegeneracy.py",
            "objective": "capture CMSM source-pack via browser/HAR or prove K_CMSM is positive/non-null on the parent-allowed source-material cone",
            "success_condition": "quarantine source-pack rows with filelist/checksums/download URLs, or parent-signed positive-cone theorem giving c_min>0; no WEP/local-GR claim until all gates pass",
            "do_not": "do not use tau_eff=1, surrogate arrays, symbolic K alone, bound inversion, closure-only zero, measured-G absorption, or public/local-GR claims",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def csv_parses(paths: list[Path]) -> bool:
    try:
        for path in paths:
            read_csv(path)
    except Exception:
        return False
    return True


def no_claim_flags(paths: list[Path]) -> bool:
    for path in paths:
        for row in read_csv(path):
            for field in ("score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if truthy(row.get(field, "")):
                    return False
    return True


def no_formalization_1609() -> bool:
    if not FORMALIZATION.exists():
        return True
    artifact_markers = (
        "1609-Y5",
        "P8_Y5_PARENT_QLOC_1609",
        "P8_Y5_BRR545_1609",
        "Y5_R2FR_CMSM_source_pack_capture_or_parent_nondegeneracy_theorem",
        "R2FR_CMSM_source_pack",
    )
    return not any(any(marker in path.name for marker in artifact_markers) for path in FORMALIZATION.rglob("*"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    probes = read_csv(WEB_PROBE)
    schema = read_csv(SOURCE_PACK_SCHEMA)
    template = read_csv(SOURCE_PACK_TEMPLATE)
    inventory = read_csv(SOURCE_PACK_INVENTORY)
    no_go = read_csv(NONDEG_NO_GO)
    alignment = read_csv(ALIGNMENT_CONTRACT)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    copies = [target for targets in COPY_TARGETS.values() for target in targets]
    checks = [
        ("VAL1609_0_sources_exist", all(truthy(row["exists"]) for row in sources), "all cited 1609 local source paths exist"),
        ("VAL1609_1_needles_found", all(truthy(row["needle_found"]) for row in sources), "all required 1609 source needles found"),
        ("VAL1609_2_probe_pointer_only", any(row["probe_id"] == "WEB1609_0_ONERA_data_page" and row["status"] == "HTTP_200_POINTER_ONLY" for row in probes), "ONERA pointer recorded without filelist promotion"),
        ("VAL1609_3_no_filelist", probes and all(row["filelist_acquired"].lower() == "false" for row in probes), "no web probe acquired filelist rows"),
        ("VAL1609_4_schema_written", len(schema) >= 10 and any(row["field"] == "no_surrogate" for row in schema), "CMSM source-pack schema written"),
        ("VAL1609_5_template_nonimportable", any(row["parser_status"] == "TEMPLATE_ONLY_NOT_IMPORTABLE" for row in template), "source-pack template remains nonimportable"),
        ("VAL1609_6_inventory_empty", inventory and all(row["exists"].lower() == "false" for row in inventory), "all live 1609 source-pack input files are missing"),
        ("VAL1609_7_no_go_recorded", any(row["theorem_id"] == "NDG1609_0_vector_space_no_go" and row["proof_status"] == "EXACT_NO_GO_COUNTERMODEL" for row in no_go), "parent nondegeneracy no-go recorded"),
        ("VAL1609_8_nondeg_not_derived", any(row["theorem_id"] == "NDG1609_3_verdict" and row["proof_status"] == "PARENT_NONDEGENERACY_NOT_DERIVED" for row in no_go), "parent nondegeneracy remains unproved"),
        ("VAL1609_9_alignment_missing", any(row["alignment_id"] == "ALI1609_3_c_min" and row["current_status"] == "MISSING_CRITICAL" for row in alignment), "critical alignment lower bound remains missing"),
        ("VAL1609_10_runner_rejects", any(row["runner_id"] == "RUN1609_1_nondegeneracy" and row["runner_result"] == "REJECT_PARENT_NONDEGENERACY_THEOREM" for row in runner), "runner rejects nondegeneracy theorem"),
        ("VAL1609_11_claim_gates_closed", gates and all(row["claim_allowed"].lower() == "false" and row["status"] == "BLOCKED" for row in gates), "all 1609 claim gates remain closed"),
        ("VAL1609_12_decision_next", any(row["decision"] == "NEXT_1610_BROWSER_HAR_SOURCE_PACK_OR_POSITIVE_CONE_NONDEGENERACY" for row in decisions), "decision selects 1610 browser/HAR or positive-cone nondegeneracy"),
        ("VAL1609_13_csv_parse", csv_parses(generated_csvs), "all generated 1609 CSVs parse"),
        ("VAL1609_14_claim_safety_flags", no_claim_flags(generated_csvs), "no generated 1609 rows are score-ready, prediction rows, valid-for-claim, or claim-allowed"),
        ("VAL1609_15_branch_copies", all(path.exists() for path in copies), "branch/quarantine nonclaim copies exist"),
        ("VAL1609_16_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1609_17_formalization_untouched", no_formalization_1609(), "no 1609 outputs found under formalization-workbench"),
    ]
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if ok else "FAIL",
            "detail": detail,
        }
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1609_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1609 CMSM source-pack capture or parent nondegeneracy theorem validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "/") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, Any]],
    probes: list[dict[str, Any]],
    schema: list[dict[str, Any]],
    template: list[dict[str, Any]],
    inventory: list[dict[str, Any]],
    no_go: list[dict[str, Any]],
    alignment: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1609 - R2/fR CMSM Source-Pack Capture Or Parent Nondegeneracy Theorem",
                "## Verdict\n"
                "- 1609 probes the official-data route and the theorem route for `tau_WEP`/alignment.\n"
                "- The ONERA data-availability pointer is reachable, but CMSM routes timed out from the local shell and no filelist/checksum/download URL was acquired.\n"
                "- The source-pack schema/template is now explicit for future browser/HAR or manual import, but remains quarantine-only and nonclaim.\n"
                "- The parent nondegeneracy theorem is not derived: an exact vector-space no-go shows nonzero `K_CMSM` and nonzero source-material vector do not imply nonzero pairing.\n"
                "- No WEP, R10, PPN, clock, orbital, Newton, local-GR, beta/coupling, or public claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## Web Probe Ledger",
                md_table(probes, ["probe_id", "url", "status", "evidence", "filelist_acquired", "checksums_acquired", "download_urls_acquired"]),
                "## CMSM Source-Pack Schema",
                md_table(schema, ["schema_id", "field", "required_policy"]),
                "## CMSM Source-Pack Template",
                md_table(template, ["template_id", "dataset_id", "file_name", "file_role", "parser_status"]),
                "## CMSM Source-Pack Inventory",
                md_table(inventory, ["inventory_id", "file_role", "exists", "row_count", "status"]),
                "## Parent Nondegeneracy No-Go",
                md_table(no_go, ["theorem_id", "proof_status", "effect", "needed_to_escape"]),
                "## Alignment Computation Contract",
                md_table(alignment, ["alignment_id", "object", "formula_or_field", "current_status"]),
                "## Runner Refusal",
                md_table(runner, ["runner_id", "acceptance_rule", "input_state", "runner_result", "effect"]),
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "reason", "next_action"]),
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "success_condition", "do_not"]),
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    INPUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    probes = web_probe_rows()
    schema = source_pack_schema_rows()
    template = source_pack_template_rows()
    inventory = source_pack_inventory_rows()
    no_go = nondeg_no_go_rows()
    alignment = alignment_contract_rows()
    runner = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        WEB_PROBE,
        SOURCE_PACK_SCHEMA,
        SOURCE_PACK_TEMPLATE,
        SOURCE_PACK_INVENTORY,
        NONDEG_NO_GO,
        ALIGNMENT_CONTRACT,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(WEB_PROBE, probes)
    write_csv(SOURCE_PACK_SCHEMA, schema)
    write_csv(SOURCE_PACK_TEMPLATE, template)
    write_csv(SOURCE_PACK_INVENTORY, inventory)
    write_csv(NONDEG_NO_GO, no_go)
    write_csv(ALIGNMENT_CONTRACT, alignment)
    write_csv(RUNNER, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, probes, schema, template, inventory, no_go, alignment, runner, gates, decisions, next_rows, validation)


if __name__ == "__main__":
    main()
