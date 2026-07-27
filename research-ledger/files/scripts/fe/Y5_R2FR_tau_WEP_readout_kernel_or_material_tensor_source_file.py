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
QUARANTINE = MICROSCOPE / "quarantine" / "1608"
INPUT = QUARANTINE / "input"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1608-Y5-R2FR-tau-WEP-readout-kernel-or-material-tensor-source-file.md"

SOURCE_FILES = {
    "1607_doc": ROOT / "1607-Y5-R2FR-Delta_w-material-tensor-import-or-parent-edge-certificate.md",
    "1607_validation": OUT / "P8_Y5_BRR545_1607_VALIDATION.csv",
    "1607_next": OUT / "P8_Y5_PARENT_QLOC_1607_NEXT_TARGET.csv",
    "1607_bound": OUT / "P8_Y5_PARENT_QLOC_1607_BOUND_INVERSION_AUDIT.csv",
    "1596_law": OUT / "P8_Y5_PARENT_QLOC_1596_TAU_WEP_CONTRACTION_LAW.csv",
    "1596_audit": OUT / "P8_Y5_PARENT_QLOC_1596_TAU_FACTOR_AUDIT.csv",
    "1596_acq": OUT / "P8_Y5_PARENT_QLOC_1596_TAU_SOURCE_ACQUISITION_ROWS.csv",
    "1597_tau": OUT / "P8_Y5_PARENT_QLOC_1597_TAU_LOWER_BOUND_THEOREM_AUDIT.csv",
    "1597_null": OUT / "P8_Y5_PARENT_QLOC_1597_NULL_SPACE_COUNTERMODEL.csv",
    "1597_inputs": OUT / "P8_Y5_PARENT_QLOC_1597_REQUIRED_NONDEGENERACY_INPUTS.csv",
    "1598_kernel": OUT / "P8_Y5_PARENT_QLOC_1598_MEASUREMENT_KERNEL_STATUS.csv",
    "1598_requirements": OUT / "P8_Y5_PARENT_QLOC_1598_ALIGNMENT_IMPORT_REQUIREMENTS.csv",
    "1598_probe": OUT / "P8_Y5_PARENT_QLOC_1598_CMSM_PORTAL_PROBE_SYNTHESIS.csv",
    "1598_nondeg": OUT / "P8_Y5_PARENT_QLOC_1598_PARENT_NONDEGENERACY_AUDIT.csv",
    "1455_readout": COEFF / "official_readout_acquisition_ledger_nonclaim_1455.csv",
    "1456_kinputs": COEFF / "official_KCMSM_bound_inputs_nonclaim_1456.csv",
    "1456_worldtube": COEFF / "source_worldtube_projection_theorem_attempt_1456.csv",
    "1457_pilot": COEFF / "source_worldtube_pilot_ledger_nonclaim_1457.csv",
    "1465_capture_plan": COEFF / "CMSM_session_filelist_capture_plan_nonclaim_1465.csv",
    "1466_capture_workflow": COEFF / "CMSM_browser_session_capture_workflow_nonclaim_1466.csv",
    "1600_har": OUT / "P8_Y5_PARENT_QLOC_1600_HAR_INTAKE_STATUS.csv",
}

NEEDLES = {
    "1607_doc": ["DEC1607_2_next", "NEXT_1608_TAU_WEP_READOUT_KERNEL_OR_MATERIAL_TENSOR_SOURCE_FILE"],
    "1607_validation": ["VAL1607_OVERALL", "PASS"],
    "1607_next": ["1608-Y5-R2FR-tau-WEP-readout-kernel-or-material-tensor-source-file.md", "tau_WEP"],
    "1607_bound": ["BIA1607_0_electron_proxy_product", "BOUND_INVERSION_PROXY_DETECTED"],
    "1596_law": ["TCL1596_2_delta_w_amplitude_law", "EXACT_CONDITIONAL_AMPLITUDE_LAW"],
    "1596_audit": ["TFA1596_4_readout_matrix", "OFFICIAL_ARRAYS_NOT_IMPORTED"],
    "1596_acq": ["TSA1596_0_readout_matrix", "SOURCE_NEEDED"],
    "1597_tau": ["TLB1597_3_current_corpus_verdict", "TAU_LOWER_BOUND_NOT_DERIVED"],
    "1597_null": ["NSC1597_0_linear_space_model", "tau_WEP can vanish"],
    "1597_inputs": ["NDI1597_3_alignment", "MISSING_CRITICAL"],
    "1598_kernel": ["MKS1598_1_official_CMSM_arrays", "OFFICIAL_ARRAYS_NOT_IMPORTED"],
    "1598_requirements": ["AIR1598_2_K_CMSM", "MISSING_OFFICIAL_ARRAYS"],
    "1598_probe": ["CPS1598_3_current_shell_probe", "TIMEOUT_OR_NO_USABLE_FILELIST"],
    "1598_nondeg": ["PNA1598_2_data_theorem_equivalence", "OFFICIAL_READOUT_OR_PARENT_ALIGNMENT_STILL_REQUIRED"],
    "1455_readout": ["KC1455_6_parser_gate", "NONCLAIM_ONLY"],
    "1456_kinputs": ["KBI1456_6_data_portal", "POINTER_ONLY_ACCESS_UNVERIFIED"],
    "1456_worldtube": ["SWP1456_6_verdict", "THEOREM_CONDITIONAL_NOT_PROMOTED"],
    "1457_pilot": ["PILOT1457_7_verdict", "PILOT_BLOCKED_NONCLAIM"],
    "1465_capture_plan": ["CAP1465_1_filelist_fields", "MISSING_FILELIST"],
    "1466_capture_workflow": ["CAP1466_5_import_guard", "GUARD_ACTIVE_NONCLAIM"],
    "1600_har": ["HAR1600_0_input_folder_empty", "NO_HAR_JSON_CSV_EVIDENCE_PRESENT"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1608_SOURCE_REGISTER.csv"
TAU_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_1608_TAU_WEP_READOUT_CONTRACT.csv"
IMPORT_SCHEMA = OUT / "P8_Y5_PARENT_QLOC_1608_OFFICIAL_INPUT_IMPORT_SCHEMA.csv"
INPUT_TEMPLATES = OUT / "P8_Y5_PARENT_QLOC_1608_OFFICIAL_INPUT_TEMPLATES.csv"
INPUT_INVENTORY = OUT / "P8_Y5_PARENT_QLOC_1608_INPUT_INVENTORY.csv"
MATERIAL_PASSTHROUGH = OUT / "P8_Y5_PARENT_QLOC_1608_MATERIAL_TENSOR_PASSTHROUGH.csv"
NONDEGENERACY = OUT / "P8_Y5_PARENT_QLOC_1608_NONDEGENERACY_THEOREM_STATUS.csv"
TAU_STATUS = OUT / "P8_Y5_PARENT_QLOC_1608_TAU_LOWER_BOUND_STATUS.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1608_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1608_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1608_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1608_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1608_VALIDATION.csv"

COPY_TARGETS = {
    TAU_CONTRACT: [
        QUARANTINE / "TAU_WEP_READOUT_CONTRACT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_tau_WEP_readout_contract_nonclaim_1608.csv",
    ],
    IMPORT_SCHEMA: [
        QUARANTINE / "OFFICIAL_INPUT_IMPORT_SCHEMA_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_official_input_import_schema_nonclaim_1608.csv",
    ],
    INPUT_TEMPLATES: [
        INPUT / "OFFICIAL_INPUT_TEMPLATES.csv",
        BRANCH_RESIDUALS / "R2FR_official_input_templates_nonclaim_1608.csv",
    ],
    INPUT_INVENTORY: [
        QUARANTINE / "INPUT_INVENTORY_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_input_inventory_nonclaim_1608.csv",
    ],
    NONDEGENERACY: [
        QUARANTINE / "NONDEGENERACY_THEOREM_STATUS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_nondegeneracy_theorem_status_nonclaim_1608.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE_CLOSED.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_closed_1608.csv",
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
                "source_id": f"SRC1608_{index}_{source_id}",
                "source_path": rel(path) if path.exists() else str(path),
                "exists": path.exists(),
                "needle_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "source_role": "1608_tau_WEP_readout_kernel_or_material_tensor_source_file_input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def tau_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": "TAU1608_0_definition",
            "object": "tau_WEP",
            "statement": "tau_WEP := N_eta^{-1}<K_CMSM, S_Earth x M_TiPt> in one branch-locked linear readout convention.",
            "status": "FORMAL_DEFINITION_ONLY",
            "needed_to_promote": "K_CMSM, S_Earth, M_TiPt, N_eta, units/sign convention and source anchors",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": "TAU1608_1_amplitude_law",
            "object": "Delta_w_TiPt",
            "statement": "if |tau_WEP| >= tau_min > 0, then |Delta_w_TiPt| <= 2.8e-15/tau_min.",
            "status": "EXACT_CONDITIONAL_LAW",
            "needed_to_promote": "strictly positive tau_min with official data or parent nondegeneracy theorem",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": "TAU1608_2_null_space_guard",
            "object": "tau_min",
            "statement": "nonzero source/material/readout factors do not imply nonzero tau because S_Earth x M_TiPt can lie in ker(K_CMSM).",
            "status": "NO_SHORTCUT_LEMMA_RETAINED",
            "needed_to_promote": "alignment lower bound c_min or direct nonzero projection computation",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": "TAU1608_3_no_unity",
            "object": "tau_eff=1 shortcut",
            "statement": "tau_WEP cannot be set to 1 by convention; it is an arena/source/readout/material projection functional.",
            "status": "SHORTCUT_FORBIDDEN",
            "needed_to_promote": "real tau calculation or parent theorem",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": "TAU1608_4_verdict",
            "object": "tau_WEP lower-bound status",
            "statement": "tau_WEP remains formal/nonclaim because official readout, source worldtube, material tensor and alignment are not imported.",
            "status": "TAU_WEP_NOT_EVALUATED",
            "needed_to_promote": "official input import or parent nondegeneracy theorem",
            "claim_allowed": False,
        },
    ]


def import_schema_rows() -> list[dict[str, Any]]:
    fields = [
        ("file_role", "K_CMSM_readout|source_worldtube|material_tensor|normalization|alignment_result|filelist"),
        ("source_path_or_url", "official local path, URL, DOI, or parent theorem path"),
        ("checksum_or_theorem_id", "sha256/checksum for files or theorem id for exact parent proof"),
        ("required_columns", "time/session/orbit/masks/gx/gz/Sxx/Sxz/material/source/tau fields as role requires"),
        ("units", "declared SI/dimensionless units"),
        ("sign_convention", "MICROSCOPE axis, TA6V-minus-PtRh10, eta sign and absolute convention"),
        ("basis", "same MTS parent WEP/source basis"),
        ("no_bound_inversion", "true for claim-grade import"),
        ("no_tau_unity", "true for claim-grade import"),
        ("valid_for_claim", "false until all gates pass"),
        ("claim_allowed", "false until full branch validation passes"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "schema_id": f"OIS1608_{index}_{field}",
            "field": field,
            "required_policy": policy,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for index, (field, policy) in enumerate(fields)
    ]


def input_template_rows() -> list[dict[str, Any]]:
    templates = [
        ("TPL1608_0_K_CMSM_readout", "K_CMSM_readout", "time_s;session_id;orbit_phase;gx;gz;Sxx;Sxz;mask_flag;calibration_flag;axis_sign;units", "official MICROSCOPE/CMSM readout/design matrix"),
        ("TPL1608_1_source_worldtube", "source_worldtube", "radius_or_depth;density_or_stress_proxy;source_response;orbit_kernel;units;source_anchor", "Earth/source profile in observed local frame"),
        ("TPL1608_2_material_tensor", "material_tensor", "component;sensitivity_value;uncertainty;units;sign_convention;basis;source_anchor", "Ti/Pt parent material-response tensor"),
        ("TPL1608_3_normalization", "normalization", "N_eta;eta_convention;absolute_or_signed;units;source_anchor", "reported Eotvos product convention"),
        ("TPL1608_4_alignment_result", "alignment_result", "K_norm;V_norm;projection_value;c_min;tau_min;uncertainty;assumptions", "alignment/non-null projection row"),
        ("TPL1608_5_filelist", "filelist", "dataset_id;product_id;file_name;file_role;byte_count;checksum;download_url;licence", "official source-pack provenance"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "template_id": template_id,
            "file_role": file_role,
            "required_columns": required_columns,
            "purpose": purpose,
            "target_input_path": f"source-intake/microscope/quarantine/1608/input/{file_role}.csv",
            "parser_status": "TEMPLATE_ONLY_NOT_IMPORTABLE",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for template_id, file_role, required_columns, purpose in templates
    ]


def expected_input_paths() -> list[tuple[str, Path]]:
    return [
        ("K_CMSM_readout", INPUT / "K_CMSM_readout.csv"),
        ("source_worldtube", INPUT / "source_worldtube.csv"),
        ("material_tensor", INPUT / "material_tensor.csv"),
        ("normalization", INPUT / "normalization.csv"),
        ("alignment_result", INPUT / "alignment_result.csv"),
        ("filelist", INPUT / "filelist.csv"),
        ("1607_material_tensor_passthrough", MICROSCOPE / "quarantine" / "1607" / "input" / "TiPt_parent_material_response_tensor.csv"),
    ]


def input_inventory_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (role, path) in enumerate(expected_input_paths()):
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
                "inventory_id": f"INV1608_{index}_{role}",
                "file_role": role,
                "path": rel(path) if exists else str(path),
                "exists": exists,
                "row_count": row_count,
                "status": status,
                "claim_allowed": False,
            }
        )
    return rows


def material_passthrough_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "passthrough_id": "MTP1608_0_1607_template",
            "source": "source-intake/microscope/quarantine/1607/input/TiPt_parent_material_response_tensor_TEMPLATE.csv",
            "status": "TEMPLATE_EXISTS_NONIMPORTABLE",
            "reason": "1607 created schema/template only; no live Ti/Pt parent tensor file was supplied",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "passthrough_id": "MTP1608_1_live_1607_file",
            "source": "source-intake/microscope/quarantine/1607/input/TiPt_parent_material_response_tensor.csv",
            "status": "LIVE_FILE_MISSING",
            "reason": "no source-backed material tensor file exists to import into tau_WEP",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def nondegeneracy_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "NDG1608_0_target",
            "statement": "prove |<K_CMSM,V_source_material>| >= c_min ||K_CMSM|| ||V_source_material|| with c_min>0",
            "current_status": "THEOREM_NOT_IN_CORPUS",
            "missing_input": "parent geometry/readout theorem or official alignment computation",
            "effect": "tau_min cannot be derived",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "NDG1608_1_symbolic_K_limit",
            "statement": "published measurement equation gives symbolic kernel shape but not alignment lower bound",
            "current_status": "SYMBOLIC_KERNEL_INSUFFICIENT",
            "missing_input": "numeric K_CMSM arrays or parent non-null projection theorem",
            "effect": "null-space countermodel survives",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "NDG1608_2_data_theorem_equivalence",
            "statement": "official-data route and parent-theorem route converge on the same nonzero projection object",
            "current_status": "OFFICIAL_READOUT_OR_PARENT_ALIGNMENT_REQUIRED",
            "missing_input": "filelist/checksums/arrays/material/source vector or theorem",
            "effect": "1609 should target source-pack capture or nondegeneracy proof",
            "claim_allowed": False,
        },
    ]


def tau_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("TLS1608_0_K_CMSM", "official readout/design matrix", False, "MKS1598_1 and KBI1456_2/3 missing official arrays"),
        ("TLS1608_1_source_worldtube", "Earth/source worldtube vector", False, "TFA1596_0 and PILOT1457 missing source profile/orbit weighting"),
        ("TLS1608_2_material_tensor", "Ti/Pt material tensor", False, "1607 full parent tensor missing"),
        ("TLS1608_3_normalization", "eta product normalization N_eta", False, "TFA1596_5 normalization not filled"),
        ("TLS1608_4_alignment", "c_min or nonzero projection", False, "NDI1597_3 MISSING_CRITICAL"),
        ("TLS1608_5_tau_min", "strictly positive tau_min", False, "no K/source/material/alignment package"),
        ("TLS1608_6_verdict", "tau_WEP score-ready", False, "official input or parent nondegeneracy missing"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "tau_status_id": status_id,
            "requirement": requirement,
            "ready": ready,
            "blocker": blocker,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for status_id, requirement, ready, blocker in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1608_0_tau_import",
            "acceptance_rule": "tau_WEP requires official K_CMSM, source worldtube, material tensor, normalization and alignment in one basis",
            "input_state": "all live input files missing",
            "runner_result": "TAU_WEP_NOT_EVALUATED",
            "effect": "no Delta_w bound or WEP score",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1608_1_nondegeneracy",
            "acceptance_rule": "parent theorem must exclude K_CMSM null-space countermodel with c_min>0",
            "input_state": "no parent nondegeneracy theorem present",
            "runner_result": "REJECT_TAU_MIN_THEOREM",
            "effect": "tau lower bound remains missing",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1608_2_shortcut_firewall",
            "acceptance_rule": "tau_eff=1, bound inversion, surrogate arrays and symbolic K alone cannot score WEP",
            "input_state": "only symbolic/proxy/workflow rows exist",
            "runner_result": "SHORTCUTS_REJECTED",
            "effect": "all local/WEP claims stay blocked",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG1608_0_K_CMSM", "official readout/design matrix", "BLOCKED", "no official arrays/filelist/checksums imported"),
        ("CG1608_1_tau_min", "positive tau_WEP lower bound", "BLOCKED", "alignment/nondegeneracy missing"),
        ("CG1608_2_material_tensor", "live material tensor import", "BLOCKED", "1607 live file missing"),
        ("CG1608_3_bound_conversion", "convert product bound to Delta_w bound", "BLOCKED", "tau_min missing"),
        ("CG1608_4_WEP_score", "MICROSCOPE/WEP score", "BLOCKED", "K/source/material/tau/readout gates open"),
        ("CG1608_5_local_GR", "Newton/local-GR source claim", "BLOCKED", "coupling/material/tau branch unresolved"),
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
            "decision_id": "DEC1608_0_tau_route",
            "decision": "TAU_WEP_IMPORT_CONTRACT_READY_NO_LIVE_INPUTS",
            "reason": "schema/templates exist, but official K/source/material/normalization/alignment files are missing",
            "next_action": "capture/import official CMSM source pack or provide equivalent source-backed files",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1608_1_theorem_route",
            "decision": "PARENT_NONDEGENERACY_NOT_DERIVED",
            "reason": "symbolic readout structure does not exclude the null-space countermodel",
            "next_action": "derive c_min>0 alignment theorem or compute c_min from official data",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1608_2_next",
            "decision": "NEXT_1609_CMSM_SOURCE_PACK_CAPTURE_OR_PARENT_NONDEGENERACY_THEOREM",
            "reason": "the next decisive object is either official filelist/checksum/source-pack capture or parent non-null projection proof",
            "next_action": "build/import CMSM source-pack capture rows, or attempt the parent nondegeneracy theorem directly",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1609-Y5-R2FR-CMSM-source-pack-capture-or-parent-nondegeneracy-theorem.md",
            "script": "scripts/Y5_R2FR_CMSM_source_pack_capture_or_parent_nondegeneracy_theorem.py",
            "objective": "capture/import official CMSM source-pack metadata/checksums/readout files, or derive parent nondegeneracy c_min>0 for the WEP readout pairing",
            "success_condition": "source-pack filelist/checksum/readout rows accepted as nonclaim input, or parent theorem excluding the tau_WEP null-space countermodel; no WEP/local-GR claim until all gates pass",
            "do_not": "do not use tau_eff=1, surrogate arrays, bound inversion, symbolic K alone, closure-only zero, measured-G absorption, or public/local-GR claims",
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


def no_formalization_1608() -> bool:
    if not FORMALIZATION.exists():
        return True
    artifact_markers = (
        "1608-Y5",
        "P8_Y5_PARENT_QLOC_1608",
        "P8_Y5_BRR545_1608",
        "Y5_R2FR_tau_WEP_readout_kernel_or_material_tensor_source_file",
        "R2FR_tau_WEP",
    )
    return not any(any(marker in path.name for marker in artifact_markers) for path in FORMALIZATION.rglob("*"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    contract = read_csv(TAU_CONTRACT)
    schema = read_csv(IMPORT_SCHEMA)
    templates = read_csv(INPUT_TEMPLATES)
    inventory = read_csv(INPUT_INVENTORY)
    passthrough = read_csv(MATERIAL_PASSTHROUGH)
    nondeg = read_csv(NONDEGENERACY)
    tau = read_csv(TAU_STATUS)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    copies = [target for targets in COPY_TARGETS.values() for target in targets]
    checks = [
        ("VAL1608_0_sources_exist", all(truthy(row["exists"]) for row in sources), "all cited 1608 local source paths exist"),
        ("VAL1608_1_needles_found", all(truthy(row["needle_found"]) for row in sources), "all required 1608 source needles found"),
        ("VAL1608_2_tau_contract", any(row["contract_id"] == "TAU1608_4_verdict" and row["status"] == "TAU_WEP_NOT_EVALUATED" for row in contract), "tau_WEP contract recorded and not evaluated"),
        ("VAL1608_3_import_schema", len(schema) >= 10 and any(row["field"] == "no_tau_unity" for row in schema), "official input import schema written"),
        ("VAL1608_4_templates_nonimportable", templates and all(row["parser_status"] == "TEMPLATE_ONLY_NOT_IMPORTABLE" for row in templates), "official input templates remain nonimportable"),
        ("VAL1608_5_live_inputs_missing", inventory and all(row["exists"].lower() == "false" for row in inventory), "all live 1608/1607 input files are missing"),
        ("VAL1608_6_material_passthrough_blocked", any(row["passthrough_id"] == "MTP1608_1_live_1607_file" and row["status"] == "LIVE_FILE_MISSING" for row in passthrough), "1607 material tensor live file is missing"),
        ("VAL1608_7_nondegeneracy_missing", any(row["theorem_id"] == "NDG1608_2_data_theorem_equivalence" and row["current_status"] == "OFFICIAL_READOUT_OR_PARENT_ALIGNMENT_REQUIRED" for row in nondeg), "nondegeneracy route remains open"),
        ("VAL1608_8_tau_not_ready", any(row["tau_status_id"] == "TLS1608_6_verdict" and row["ready"].lower() == "false" for row in tau), "tau branch remains not score-ready"),
        ("VAL1608_9_runner_rejects_shortcuts", any(row["runner_id"] == "RUN1608_2_shortcut_firewall" and row["runner_result"] == "SHORTCUTS_REJECTED" for row in runner), "runner rejects tau/readout shortcuts"),
        ("VAL1608_10_claim_gates_closed", gates and all(row["claim_allowed"].lower() == "false" and row["status"] == "BLOCKED" for row in gates), "all 1608 claim gates remain closed"),
        ("VAL1608_11_decision_next", any(row["decision"] == "NEXT_1609_CMSM_SOURCE_PACK_CAPTURE_OR_PARENT_NONDEGENERACY_THEOREM" for row in decisions), "decision selects 1609 CMSM source-pack or nondegeneracy theorem"),
        ("VAL1608_12_csv_parse", csv_parses(generated_csvs), "all generated 1608 CSVs parse"),
        ("VAL1608_13_claim_safety_flags", no_claim_flags(generated_csvs), "no generated 1608 rows are score-ready, prediction rows, valid-for-claim, or claim-allowed"),
        ("VAL1608_14_branch_copies", all(path.exists() for path in copies), "branch/quarantine nonclaim copies exist"),
        ("VAL1608_15_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1608_16_formalization_untouched", no_formalization_1608(), "no 1608 outputs found under formalization-workbench"),
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
            "check_id": "VAL1608_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1608 tau_WEP readout kernel or material tensor source-file validation",
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
    contract: list[dict[str, Any]],
    schema: list[dict[str, Any]],
    templates: list[dict[str, Any]],
    inventory: list[dict[str, Any]],
    passthrough: list[dict[str, Any]],
    nondeg: list[dict[str, Any]],
    tau: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1608 - R2/fR tau_WEP Readout Kernel Or Material Tensor Source File",
                "## Verdict\n"
                "- 1608 turns the WEP/tau problem into a strict input contract: `tau_WEP = N_eta^{-1}<K_CMSM, S_Earth x M_TiPt>` in one branch-locked convention.\n"
                "- The exact amplitude law remains conditional: `|Delta_w_TiPt| <= 2.8e-15/tau_min` only after a sourced `tau_min>0` exists.\n"
                "- No live official CMSM/readout/source/material/alignment files are present; templates are written only as quarantine input contracts.\n"
                "- The parent nondegeneracy theorem is not in the corpus; symbolic readout structure alone does not exclude the null-space countermodel.\n"
                "- No WEP, R10, PPN, clock, orbital, Newton, local-GR, beta/coupling, or public claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## tau_WEP Readout Contract",
                md_table(contract, ["contract_id", "object", "status", "needed_to_promote"]),
                "## Official Input Import Schema",
                md_table(schema, ["schema_id", "field", "required_policy"]),
                "## Official Input Templates",
                md_table(templates, ["template_id", "file_role", "required_columns", "parser_status"]),
                "## Input Inventory",
                md_table(inventory, ["inventory_id", "file_role", "exists", "row_count", "status"]),
                "## Material Tensor Passthrough",
                md_table(passthrough, ["passthrough_id", "source", "status", "reason"]),
                "## Nondegeneracy Theorem Status",
                md_table(nondeg, ["theorem_id", "current_status", "missing_input", "effect"]),
                "## tau Lower-Bound Status",
                md_table(tau, ["tau_status_id", "requirement", "ready", "blocker"]),
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
    contract = tau_contract_rows()
    schema = import_schema_rows()
    templates = input_template_rows()
    inventory = input_inventory_rows()
    passthrough = material_passthrough_rows()
    nondeg = nondegeneracy_rows()
    tau = tau_status_rows()
    runner = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        TAU_CONTRACT,
        IMPORT_SCHEMA,
        INPUT_TEMPLATES,
        INPUT_INVENTORY,
        MATERIAL_PASSTHROUGH,
        NONDEGENERACY,
        TAU_STATUS,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(TAU_CONTRACT, contract)
    write_csv(IMPORT_SCHEMA, schema)
    write_csv(INPUT_TEMPLATES, templates)
    write_csv(INPUT_INVENTORY, inventory)
    write_csv(MATERIAL_PASSTHROUGH, passthrough)
    write_csv(NONDEGENERACY, nondeg)
    write_csv(TAU_STATUS, tau)
    write_csv(RUNNER, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, contract, schema, templates, inventory, passthrough, nondeg, tau, runner, gates, decisions, next_rows, validation)


if __name__ == "__main__":
    main()
