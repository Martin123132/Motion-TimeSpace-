from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1598"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1598-Y5-R2FR-official-MICROSCOPE-readout-or-parent-nondegeneracy.md"

SOURCE_FILES = {
    "1597_doc": ROOT / "1597-Y5-R2FR-tau-lower-bound-or-coupling-zero-proof.md",
    "1597_validation": OUT / "P8_Y5_BRR545_1597_VALIDATION.csv",
    "1597_theorem": OUT / "P8_Y5_PARENT_QLOC_1597_TAU_LOWER_BOUND_THEOREM_AUDIT.csv",
    "1597_countermodel": OUT / "P8_Y5_PARENT_QLOC_1597_NULL_SPACE_COUNTERMODEL.csv",
    "1597_nondegen_inputs": OUT / "P8_Y5_PARENT_QLOC_1597_REQUIRED_NONDEGENERACY_INPUTS.csv",
    "1597_next_target": OUT / "P8_Y5_PARENT_QLOC_1597_NEXT_TARGET.csv",
    "1462_probe": OUT / "P8_Y5_R10_1462_CMSM_PORTAL_PROBE_LEDGER.csv",
    "1463_filelist": OUT / "P8_Y5_R10_1463_CMSM_ACCESS_AND_FILELIST_LEDGER.csv",
    "1465_probe": OUT / "P8_Y5_R10_1465_CMSM_SESSION_PROBE_RESULT.csv",
    "1466_capture": OUT / "P8_Y5_R10_1466_CMSM_SESSION_CAPTURE_RESULT_NONCLAIM.csv",
    "1467_endpoint": OUT / "P8_Y5_R10_1467_CMSM_ENDPOINT_PROBE_NONCLAIM.csv",
    "1467_evidence": OUT / "P8_Y5_R10_1467_CMSM_CAPTURE_EVIDENCE_REQUIREMENTS.csv",
    "1084_kernel": OUT / "P8_Y5_R10_1084_SOURCE_PROFILE_KERNEL_DERIVATION_LEDGER.csv",
    "1084_profile_gate": OUT / "P8_Y5_R10_1084_PROFILE_CLOSURE_GATES.csv",
    "1084_readout_gate": OUT / "P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv",
}

NEEDLES = {
    "1597_doc": ["NEXT_1598_OFFICIAL_READOUT_OR_PARENT_NONDEGENERACY", "readout kernel"],
    "1597_validation": ["VAL1597_OVERALL", "PASS"],
    "1597_theorem": ["TLB1597_1_sufficient_lower_bound", "c_min>0"],
    "1597_countermodel": ["NSC1597_0_linear_space_model", "ker(K)"],
    "1597_nondegen_inputs": ["NDI1597_3_alignment", "MISSING_CRITICAL"],
    "1597_next_target": ["1598-Y5-R2FR-official-MICROSCOPE-readout-or-parent-nondegeneracy", "c_min>0"],
    "1462_probe": ["PROBE1462_0_ONERA_page", "HTTP_200_TEXT_HTML"],
    "1463_filelist": ["ACC1463_2_CMSM_module_7", "BLOCKED_NO_FILE_LIST"],
    "1465_probe": ["PROBE1465_0_shell_443", "CONNECT_BLOCKED_OR_NO_FILE_ROWS"],
    "1466_capture": ["PROBE1466_0_browser_session", "NOT_EXECUTED_NO_AUTHENTICATED_BROWSER_CAPTURE_ATTACHED"],
    "1467_endpoint": ["PROBE1467_3_dataobjects_options", "NETWORK_ERROR_NO_CLAIM"],
    "1467_evidence": ["EV1467_1_filelist_rows", "MISSING"],
    "1084_kernel": ["K1084_4_orbit_factor", "time-dependent gx/gz/Sxx/Sxz/masks"],
    "1084_profile_gate": ["PCG1084_1_finite_range_profile", "MISSING_PREM_IMPORT_AND_LAMBDA_OWNER"],
    "1084_readout_gate": ["RIG1084_0_CMSM_arrays", "OFFICIAL_ARRAYS_NOT_IMPORTED"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1598_SOURCE_REGISTER.csv"
PORTAL_SYNTHESIS = OUT / "P8_Y5_PARENT_QLOC_1598_CMSM_PORTAL_PROBE_SYNTHESIS.csv"
KERNEL_STATUS = OUT / "P8_Y5_PARENT_QLOC_1598_MEASUREMENT_KERNEL_STATUS.csv"
NONDEG_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1598_PARENT_NONDEGENERACY_AUDIT.csv"
ALIGNMENT_REQUIREMENTS = OUT / "P8_Y5_PARENT_QLOC_1598_ALIGNMENT_IMPORT_REQUIREMENTS.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1598_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1598_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1598_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1598_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1598_VALIDATION.csv"

COPY_TARGETS = {
    PORTAL_SYNTHESIS: [
        QUARANTINE / "CMSM_PORTAL_PROBE_SYNTHESIS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_CMSM_portal_probe_synthesis_nonclaim_1598.csv",
    ],
    KERNEL_STATUS: [
        QUARANTINE / "MEASUREMENT_KERNEL_STATUS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_measurement_kernel_status_nonclaim_1598.csv",
    ],
    NONDEG_AUDIT: [
        QUARANTINE / "PARENT_NONDEGENERACY_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_parent_nondegeneracy_audit_nonclaim_1598.csv",
    ],
    ALIGNMENT_REQUIREMENTS: [
        QUARANTINE / "ALIGNMENT_IMPORT_REQUIREMENTS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_alignment_import_requirements_nonclaim_1598.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE_CLOSED.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_closed_1598.csv",
    ],
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (source_id, path) in enumerate(SOURCE_FILES.items()):
        text = read_text(path) if path.exists() else ""
        needles = NEEDLES[source_id]
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1598_{index}_{source_id}",
                "source_path": path.relative_to(ROOT).as_posix() if path.exists() else str(path),
                "exists": path.exists(),
                "needle_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "source_role": "1598_official_readout_or_parent_nondegeneracy_input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def portal_synthesis_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "probe_id": "CPS1598_0_ONERA_pointer",
            "url_or_path": "https://microscope.onera.fr/fr/publication/microscope-data-are-available",
            "evidence_status": "OFFICIAL_POINTER_AVAILABLE",
            "evidence_detail": "ONERA page and 1462 probe establish a CMSM portal route for MICROSCOPE mission data",
            "filelist_acquired": False,
            "checksums_acquired": False,
            "download_urls_acquired": False,
            "claim_impact": "supports acquisition route only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "probe_id": "CPS1598_1_CMSM_portal_route",
            "url_or_path": "https://cmsm-ds.onera.fr/user/microscope",
            "evidence_status": "REGARDS_PORTAL_ROUTE_EXISTS_NO_FILELIST",
            "evidence_detail": "local/web evidence resolves a REGARDS route/title but no parseable file inventory",
            "filelist_acquired": False,
            "checksums_acquired": False,
            "download_urls_acquired": False,
            "claim_impact": "blocks official K_CMSM import",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "probe_id": "CPS1598_2_module7_route",
            "url_or_path": "https://cmsm-ds.onera.fr/user/microscope/modules/7",
            "evidence_status": "MODULE_ROUTE_BLOCKED_NO_FILELIST",
            "evidence_detail": "1463/1465/1467 evidence reports no dataset rows, no download URLs and no checksums",
            "filelist_acquired": False,
            "checksums_acquired": False,
            "download_urls_acquired": False,
            "claim_impact": "requires authenticated browser/HAR or official API response",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "probe_id": "CPS1598_3_current_shell_probe",
            "url_or_path": "CMSM user/module/API shell probes on 2026-06-17",
            "evidence_status": "TIMEOUT_OR_NO_USABLE_FILELIST",
            "evidence_detail": "ONERA pointer loaded but CMSM portal/API routes did not provide a source-pack file list from shell",
            "filelist_acquired": False,
            "checksums_acquired": False,
            "download_urls_acquired": False,
            "claim_impact": "1598 remains source-acquisition, not live import",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def kernel_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "kernel_id": "MKS1598_0_published_measurement_equation",
            "object": "symbolic MICROSCOPE WEP readout kernel",
            "status": "SYMBOLIC_KERNEL_STRUCTURE_AVAILABLE",
            "evidence": "published analysis describes differential acceleration readout, Earth gravity modulation, sensitivity matrices and gravity-gradient terms",
            "source": "https://arxiv.org/abs/2012.06484; P8_Y5_R10_1084_SOURCE_PROFILE_KERNEL_DERIVATION_LEDGER.csv:K1084_4_orbit_factor",
            "claim_impact": "helps define K symbolically but does not import numeric arrays",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "kernel_id": "MKS1598_1_official_CMSM_arrays",
            "object": "K_CMSM numeric readout/design matrix",
            "status": "OFFICIAL_ARRAYS_NOT_IMPORTED",
            "evidence": "RIG1084_0_CMSM_arrays and CMSM portal probes show no official time/session/gx/gz/Sxx/Sxz/mask/calibration file imported",
            "source": "P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv:RIG1084_0_CMSM_arrays",
            "claim_impact": "blocks tau_WEP numeric value and c_min",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "kernel_id": "MKS1598_2_source_profile",
            "object": "Earth/source profile vector",
            "status": "PROFILE_SMOKE_ONLY_NONCLAIM",
            "evidence": "1084 has finite-range profile algebra and two-layer smoke rows, but PREM/source composition and lambda owner remain missing",
            "source": "P8_Y5_R10_1084_PROFILE_CLOSURE_GATES.csv:PCG1084_1_finite_range_profile",
            "claim_impact": "cannot provide sourced S_Earth norm or alignment",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "kernel_id": "MKS1598_3_alignment",
            "object": "c_min = lower bound for |cos(theta)| between K_CMSM and source-material vector",
            "status": "MISSING_CRITICAL_ALIGNMENT",
            "evidence": "1597 null-space countermodel survives unless official data or parent theorem excludes K-orthogonality",
            "source": "P8_Y5_PARENT_QLOC_1597_REQUIRED_NONDEGENERACY_INPUTS.csv:NDI1597_3_alignment",
            "claim_impact": "no tau_min and no Delta_w number",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def parent_nondegeneracy_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "PNA1598_0_sufficient_parent_theorem",
            "target": "force c_min>0 without CMSM data",
            "required_statement": "parent matter/source/readout geometry maps the branch source-material vector into a non-null readout subspace with a positive alignment lower bound",
            "current_status": "THEOREM_NOT_IN_CORPUS",
            "result": "PARENT_NONDEGENERACY_NOT_PROVEN",
            "effect": "null-space countermodel remains",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "PNA1598_1_symbolic_K_limit",
            "target": "use published measurement equation alone",
            "required_statement": "symbolic K plus parent restrictions exclude all orthogonal source-material vectors",
            "current_status": "SYMBOLIC_K_ONLY",
            "result": "INSUFFICIENT_FOR_C_MIN",
            "effect": "measurement equation structure is not an alignment proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "PNA1598_2_data_theorem_equivalence",
            "target": "decide whether theorem route avoids data",
            "required_statement": "parent theorem must identify the same non-null object that official data would compute",
            "current_status": "ROUTES_CONVERGE_ON_ALIGNMENT_OBJECT",
            "result": "OFFICIAL_READOUT_OR_PARENT_ALIGNMENT_STILL_REQUIRED",
            "effect": "1599 should build capture/parser gate or derive alignment",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def alignment_requirement_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "requirement_id": "AIR1598_0_filelist",
            "needed_object": "CMSM official file list",
            "required_fields": "dataset_id; product_id; file_name; file_role; byte_count; row_count; download_url; access/licence",
            "source_route": "authenticated browser/HAR capture or official unauthenticated REGARDS API response",
            "current_status": "MISSING_FILELIST",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "requirement_id": "AIR1598_1_checksums",
            "needed_object": "download/hash ledger",
            "required_fields": "official checksum or local sha256 after official download URL; byte count; timestamp",
            "source_route": "quarantine download verification",
            "current_status": "MISSING_CHECKSUMS",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "requirement_id": "AIR1598_2_K_CMSM",
            "needed_object": "official readout/design matrix",
            "required_fields": "time; session/orbit; gx; gz; Sxx; Sxz; masks; calibration flags; attitude/sign convention",
            "source_route": "CMSM raw/calibrated/auxiliary files mapped to parser schema",
            "current_status": "MISSING_OFFICIAL_ARRAYS",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "requirement_id": "AIR1598_3_source_material_vector",
            "needed_object": "branch source-material vector V",
            "required_fields": "Earth/source profile; Ti/Pt material response; parent source-weight convention; uncertainty",
            "source_route": "PREM/source composition plus material tensor or parent theorem",
            "current_status": "MISSING_VECTOR",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "requirement_id": "AIR1598_4_alignment",
            "needed_object": "c_min lower bound or nonzero projection row",
            "required_fields": "inner product convention; K norm; V norm; projection value; uncertainty; sign/absolute convention",
            "source_route": "official data computation or parent nondegeneracy theorem",
            "current_status": "MISSING_CRITICAL_ALIGNMENT",
            "claim_allowed": False,
        },
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1598_0_pointer",
            "acceptance_rule": "ONERA pointer may support acquisition route only",
            "input_state": "official page exists but file list absent",
            "runner_result": "ACCEPT_POINTER_ONLY",
            "effect": "no readout import",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1598_1_symbolic_kernel",
            "acceptance_rule": "published measurement-equation structure may define symbolic K",
            "input_state": "no official arrays/checksums/schema",
            "runner_result": "ACCEPT_SYMBOLIC_K_ONLY",
            "effect": "no tau_WEP numeric projection",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1598_2_alignment",
            "acceptance_rule": "c_min requires data projection or parent nondegeneracy theorem",
            "input_state": "null-space countermodel survives",
            "runner_result": "REJECT_ALIGNMENT_CLAIM",
            "effect": "no tau_min or Delta_w bound",
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    claims = [
        ("CG1598_0_CMSM", "official CMSM readout imported", "no file list/download/checksum/schema imported"),
        ("CG1598_1_tau", "tau_WEP computed or lower-bounded", "K_CMSM and alignment missing"),
        ("CG1598_2_parent", "parent nondegeneracy forces c_min>0", "no theorem in corpus"),
        ("CG1598_3_WEP", "MTS passes MICROSCOPE/WEP", "product anchor only"),
        ("CG1598_4_local_GR", "derived local GR branch", "coupling/source readout residual remains open"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": "BLOCKED",
            "reason": reason,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim, reason in claims
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1598_0_data_route",
            "decision": "OFFICIAL_POINTER_CONFIRMED_BUT_READOUT_NOT_IMPORTED",
            "reason": "ONERA pointer exists; CMSM route did not expose file list/checksums/download URLs to current shell/local ledgers",
            "next_action": "use authenticated browser/HAR or official API response",
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1598_1_theory_route",
            "decision": "PARENT_NONDEGENERACY_NOT_PROVEN",
            "reason": "symbolic measurement equation does not exclude readout-kernel orthogonality",
            "next_action": "derive parent alignment theorem only if new parent action structure is supplied",
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1598_2_next",
            "decision": "NEXT_1599_CMSM_CAPTURE_OR_SYMBOLIC_K_BRIDGE",
            "reason": "the next useful work is a capture/parser package or a stricter symbolic K-to-MTS projection bridge",
            "next_action": "build a HAR/filelist parser and symbolic measurement-kernel bridge without claims",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1599-Y5-R2FR-CMSM-capture-parser-or-symbolic-K-bridge.md",
            "script": "scripts/Y5_R2FR_CMSM_capture_parser_or_symbolic_K_bridge.py",
            "objective": "create a quarantine parser for authenticated CMSM/HAR/filelist evidence and a symbolic K bridge from MICROSCOPE measurement equation to MTS tau_WEP contract",
            "success_condition": "either parse real filelist/checksum rows from official evidence, or produce a strict symbolic bridge showing exactly which K components MTS must source",
            "do_not": "do not claim WEP/local GR, do not promote portal pointers to official arrays, do not set tau_WEP=1",
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
    truthy = {"true", "1", "yes", "y"}
    for path in paths:
        for row in read_csv(path):
            for field in ("score_ready", "valid_prediction_row", "claim_allowed"):
                if row.get(field, "").strip().lower() in truthy:
                    return False
    return True


def no_formalization_1598() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*1598*"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    portal = read_csv(PORTAL_SYNTHESIS)
    kernels = read_csv(KERNEL_STATUS)
    nondeg = read_csv(NONDEG_AUDIT)
    requirements = read_csv(ALIGNMENT_REQUIREMENTS)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    copies = [target for targets in COPY_TARGETS.values() for target in targets]
    checks = [
        ("VAL1598_0_sources_exist", all(row["exists"] == "True" or row["exists"] is True for row in sources), "all cited 1598 local source paths exist"),
        ("VAL1598_1_needles_found", all(row["needle_found"] == "True" or row["needle_found"] is True for row in sources), "all required 1598 source needles found"),
        ("VAL1598_2_ONERA_pointer", any(row["probe_id"] == "CPS1598_0_ONERA_pointer" and row["evidence_status"] == "OFFICIAL_POINTER_AVAILABLE" for row in portal), "ONERA CMSM pointer retained"),
        ("VAL1598_3_no_filelist", any(row["probe_id"] == "CPS1598_2_module7_route" and row["filelist_acquired"].lower() == "false" for row in portal), "CMSM module/filelist remains unavailable"),
        ("VAL1598_4_symbolic_kernel_only", any(row["kernel_id"] == "MKS1598_0_published_measurement_equation" and row["status"] == "SYMBOLIC_KERNEL_STRUCTURE_AVAILABLE" for row in kernels), "symbolic measurement-kernel structure recorded"),
        ("VAL1598_5_official_arrays_missing", any(row["kernel_id"] == "MKS1598_1_official_CMSM_arrays" and row["status"] == "OFFICIAL_ARRAYS_NOT_IMPORTED" for row in kernels), "official K_CMSM arrays still missing"),
        ("VAL1598_6_parent_nondeg_missing", any(row["audit_id"] == "PNA1598_0_sufficient_parent_theorem" and row["result"] == "PARENT_NONDEGENERACY_NOT_PROVEN" for row in nondeg), "parent nondegeneracy theorem not proven"),
        ("VAL1598_7_alignment_required", any(row["requirement_id"] == "AIR1598_4_alignment" and row["current_status"] == "MISSING_CRITICAL_ALIGNMENT" for row in requirements), "alignment/c_min remains critical missing object"),
        ("VAL1598_8_runner_blocks_alignment", any(row["runner_id"] == "RUN1598_2_alignment" and row["runner_result"] == "REJECT_ALIGNMENT_CLAIM" for row in runner), "runner rejects alignment claim"),
        ("VAL1598_9_claim_gates_closed", gates and all(row["claim_allowed"].lower() == "false" for row in gates), "all 1598 claim gates remain closed"),
        ("VAL1598_10_decision_next", any(row["decision"] == "NEXT_1599_CMSM_CAPTURE_OR_SYMBOLIC_K_BRIDGE" for row in decisions), "decision selects 1599 capture/parser or symbolic K bridge"),
        ("VAL1598_11_csv_parse", csv_parses(generated_csvs), "all generated 1598 CSVs parse"),
        ("VAL1598_12_claim_safety_flags", no_claim_flags(generated_csvs), "no generated 1598 rows are score-ready, prediction rows, or claim-allowed"),
        ("VAL1598_13_branch_copies", all(path.exists() for path in copies), "branch/quarantine nonclaim copies exist"),
        ("VAL1598_14_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1598_15_formalization_untouched", no_formalization_1598(), "no 1598 outputs found under formalization-workbench"),
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
            "check_id": "VAL1598_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1598 official MICROSCOPE readout or parent nondegeneracy validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, Any]],
    portal: list[dict[str, Any]],
    kernels: list[dict[str, Any]],
    nondeg: list[dict[str, Any]],
    requirements: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1598 - R2/fR Official MICROSCOPE Readout Or Parent Nondegeneracy",
                "## Verdict\n"
                "- 1598 confirms the official ONERA/CMSM route exists, but the current shell/local evidence still has no official file list, checksums, download URLs, or parsed CMSM arrays.\n"
                "- The published MICROSCOPE measurement equation gives a symbolic readout-kernel structure; that is useful, but it is not a numeric `K_CMSM` import.\n"
                "- The parent nondegeneracy route also remains unproved: symbolic `K` does not exclude the 1597 readout-kernel null-space countermodel.\n"
                "- The missing object is still `c_min`: a sourced lower bound for the alignment/projection between official `K_CMSM` and the branch source-material vector.\n"
                "- No WEP, local-GR, Newton, PPN, R10, clock, orbital, beta/coupling, or public claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## CMSM Portal Probe Synthesis",
                md_table(portal, ["probe_id", "url_or_path", "evidence_status", "filelist_acquired", "checksums_acquired", "download_urls_acquired", "claim_impact"]),
                "## Measurement Kernel Status",
                md_table(kernels, ["kernel_id", "object", "status", "source", "claim_impact"]),
                "## Parent Nondegeneracy Audit",
                md_table(nondeg, ["audit_id", "target", "current_status", "result", "effect"]),
                "## Alignment Import Requirements",
                md_table(requirements, ["requirement_id", "needed_object", "required_fields", "source_route", "current_status"]),
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
    sources = source_register_rows()
    portal = portal_synthesis_rows()
    kernels = kernel_status_rows()
    nondeg = parent_nondegeneracy_rows()
    requirements = alignment_requirement_rows()
    runner = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        PORTAL_SYNTHESIS,
        KERNEL_STATUS,
        NONDEG_AUDIT,
        ALIGNMENT_REQUIREMENTS,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(PORTAL_SYNTHESIS, portal)
    write_csv(KERNEL_STATUS, kernels)
    write_csv(NONDEG_AUDIT, nondeg)
    write_csv(ALIGNMENT_REQUIREMENTS, requirements)
    write_csv(RUNNER, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, portal, kernels, nondeg, requirements, runner, gates, decisions, next_rows, validation)


if __name__ == "__main__":
    main()
