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
QUARANTINE = MICROSCOPE / "quarantine" / "1610"
INPUT = QUARANTINE / "input"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1610-Y5-R2FR-browser-HAR-source-pack-or-positive-cone-nondegeneracy.md"

SOURCE_FILES = {
    "1609_doc": ROOT / "1609-Y5-R2FR-CMSM-source-pack-capture-or-parent-nondegeneracy-theorem.md",
    "1609_validation": OUT / "P8_Y5_BRR545_1609_VALIDATION.csv",
    "1609_next": OUT / "P8_Y5_PARENT_QLOC_1609_NEXT_TARGET.csv",
    "1609_web": OUT / "P8_Y5_PARENT_QLOC_1609_WEB_PROBE_LEDGER.csv",
    "1609_inventory": OUT / "P8_Y5_PARENT_QLOC_1609_CMSM_SOURCE_PACK_INVENTORY.csv",
    "1609_no_go": OUT / "P8_Y5_PARENT_QLOC_1609_PARENT_NONDEGENERACY_NO_GO.csv",
    "1609_alignment": OUT / "P8_Y5_PARENT_QLOC_1609_ALIGNMENT_COMPUTATION_CONTRACT.csv",
    "1597_null": OUT / "P8_Y5_PARENT_QLOC_1597_NULL_SPACE_COUNTERMODEL.csv",
    "1456_worldtube": COEFF / "source_worldtube_projection_theorem_attempt_1456.csv",
    "1465_capture_plan": COEFF / "CMSM_session_filelist_capture_plan_nonclaim_1465.csv",
    "1466_capture_workflow": COEFF / "CMSM_browser_session_capture_workflow_nonclaim_1466.csv",
}

NEEDLES = {
    "1609_doc": ["NDG1609_3_verdict", "PARENT_NONDEGENERACY_NOT_DERIVED"],
    "1609_validation": ["VAL1609_OVERALL", "PASS"],
    "1609_next": ["1610-Y5-R2FR-browser-HAR-source-pack-or-positive-cone-nondegeneracy.md", "positive-cone"],
    "1609_web": ["WEB1609_0_ONERA_data_page", "HTTP_200_POINTER_ONLY"],
    "1609_inventory": ["CSPI1609_0_source_pack_filelist", "MISSING_INPUT_FILE"],
    "1609_no_go": ["NDG1609_1_positive_cone_route", "CONDITIONAL_ROUTE_IDENTIFIED"],
    "1609_alignment": ["ALI1609_3_c_min", "MISSING_CRITICAL"],
    "1597_null": ["NSC1597_1_cancellation_model", "positive and negative pieces can cancel"],
    "1456_worldtube": ["SWP1456_4_mask_orbit_limit", "DOMAIN_SELECTOR_COUNTERMODEL_RETAINED"],
    "1465_capture_plan": ["CAP1465_0_browser_session", "PLAN_ONLY_NOT_EXECUTED"],
    "1466_capture_workflow": ["CAP1466_0_auth_browser", "WORKFLOW_WRITTEN_NOT_EXECUTED_BY_1466"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1610_SOURCE_REGISTER.csv"
BROWSER_HAR_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_1610_BROWSER_HAR_CAPTURE_CONTRACT.csv"
BROWSER_HAR_STATUS = OUT / "P8_Y5_PARENT_QLOC_1610_BROWSER_HAR_CAPTURE_STATUS.csv"
POSITIVE_CONE = OUT / "P8_Y5_PARENT_QLOC_1610_POSITIVE_CONE_THEOREM_ATTEMPT.csv"
CONE_COUNTERMODEL = OUT / "P8_Y5_PARENT_QLOC_1610_CONE_COUNTERMODEL_AUDIT.csv"
SOURCE_PACK_ACCEPTANCE = OUT / "P8_Y5_PARENT_QLOC_1610_SOURCE_PACK_ACCEPTANCE_GATE.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1610_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1610_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1610_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1610_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1610_VALIDATION.csv"

COPY_TARGETS = {
    BROWSER_HAR_CONTRACT: [
        QUARANTINE / "BROWSER_HAR_CAPTURE_CONTRACT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_browser_HAR_capture_contract_nonclaim_1610.csv",
    ],
    BROWSER_HAR_STATUS: [
        QUARANTINE / "BROWSER_HAR_CAPTURE_STATUS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_browser_HAR_capture_status_nonclaim_1610.csv",
    ],
    POSITIVE_CONE: [
        QUARANTINE / "POSITIVE_CONE_THEOREM_ATTEMPT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_positive_cone_theorem_attempt_nonclaim_1610.csv",
    ],
    CONE_COUNTERMODEL: [
        QUARANTINE / "CONE_COUNTERMODEL_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_cone_countermodel_audit_nonclaim_1610.csv",
    ],
    SOURCE_PACK_ACCEPTANCE: [
        QUARANTINE / "SOURCE_PACK_ACCEPTANCE_GATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_source_pack_acceptance_gate_nonclaim_1610.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE_CLOSED.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_closed_1610.csv",
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
                "source_id": f"SRC1610_{index}_{source_id}",
                "source_path": rel(path) if path.exists() else str(path),
                "exists": path.exists(),
                "needle_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "source_role": "1610_browser_HAR_source_pack_or_positive_cone_input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def browser_har_contract_rows() -> list[dict[str, Any]]:
    rows = [
        ("HAR1610_0_auth_session", "authenticated CMSM browser session", "open https://cmsm-ds.onera.fr/user/microscope/modules/7 and confirm module identity/session", "page title, module id, authenticated network calls"),
        ("HAR1610_1_network_filter", "REGARDS network capture", "filter rs-catalog, rs-access-project, datasets, dataobjects, download calls", "request URL/method/status/payload/response shape"),
        ("HAR1610_2_filelist", "dataset/dataobject filelist", "capture dataset_id, product_id, file_name, role, byte_count, row_count, checksum, download_url, metadata_schema, licence", "machine-readable CSV/JSON source-pack rows"),
        ("HAR1610_3_hash_download", "quarantine download/hash", "download only official readout/source files to quarantine and compute sha256", "download hash ledger; no live coefficient promotion"),
        ("HAR1610_4_parser_gate", "source-pack parser gate", "validate file roles/columns/units/sign/basis before branch import", "no MISSING_FILELIST/CHECKSUM/DOWNLOAD_URL markers"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": contract_id,
            "object": obj,
            "required_action": action,
            "accepted_evidence": evidence,
            "current_status": "CONTRACT_READY_NOT_EXECUTED",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for contract_id, obj, action, evidence in rows
    ]


def browser_har_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": "HST1610_0_execution",
            "route": "browser/HAR CMSM capture",
            "execution_status": "NOT_EXECUTED_IN_1610",
            "reason": "no authenticated CMSM browser/HAR artifact is present in quarantine/1610/input",
            "filelist_acquired": False,
            "checksums_acquired": False,
            "download_urls_acquired": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": "HST1610_1_shell_probe_context",
            "route": "shell/web probe",
            "execution_status": "POINTER_ONLY_TIMEOUTS_RETAINED",
            "reason": "1609 reached ONERA pointer but CMSM shell/API routes timed out and produced no rows",
            "filelist_acquired": False,
            "checksums_acquired": False,
            "download_urls_acquired": False,
            "claim_allowed": False,
        },
    ]


def positive_cone_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "PCN1610_0_target",
            "statement": "prove K_CMSM[V] >= c_min ||K_CMSM|| ||V|| for every parent-allowed V=S_Earth x M_TiPt in a positive source-material cone",
            "status": "TARGET_SHARPENED",
            "what_is_exact": "this would bypass official alignment data if parent-signed",
            "blocking_gap": "allowed cone and positivity of K_CMSM are not parent-signed",
            "theorem_closed": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "PCN1610_1_positive_functional_lemma",
            "statement": "If V is restricted to a compact normalized cone C with dist(C,ker K)>=c_min>0, then |<K,V>|>=c_min||K||||V||.",
            "status": "EXACT_CONDITIONAL_LEMMA",
            "what_is_exact": "positive-cone/non-null theorem structure is mathematically valid",
            "blocking_gap": "current corpus does not prove compact cone, distance bound, or sign-definite readout",
            "theorem_closed": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "PCN1610_2_readout_sign_problem",
            "statement": "orbit masks, differential-axis sign, gradient corrections and calibration windows may introduce sign-changing weights in K_CMSM.",
            "status": "SIGN_DEFINITE_READOUT_NOT_PROVEN",
            "what_is_exact": "sign-changing K breaks strict positivity on a broad positive source cone",
            "blocking_gap": "official K arrays or parent sign theorem missing",
            "theorem_closed": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "PCN1610_3_source_cone_problem",
            "statement": "source-material vectors can have cancellation directions unless parent material/source response is restricted to a cone disjoint from ker(K).",
            "status": "SOURCE_CONE_NOT_PARENT_SIGNED",
            "what_is_exact": "positivity of mass density alone is insufficient after differential material/readout projection",
            "blocking_gap": "material tensor, source profile and no-cancellation covariance rule missing",
            "theorem_closed": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "PCN1610_4_verdict",
            "statement": "positive-cone nondegeneracy remains a clean conditional route but is not derived in 1610.",
            "status": "POSITIVE_CONE_THEOREM_NOT_DERIVED",
            "what_is_exact": "the missing assumptions are now explicit: sign-definite readout and parent-restricted source-material cone",
            "blocking_gap": "requires official K/source/material data or parent sign/cone theorem",
            "theorem_closed": False,
            "claim_allowed": False,
        },
    ]


def cone_countermodel_rows() -> list[dict[str, Any]]:
    rows = [
        ("PCM1610_0_kernel_vector", "choose nonzero V in ker(K)", "even if V is nonzero, <K,V>=0", "blocks tau_min without cone restriction"),
        ("PCM1610_1_sign_changing_readout", "K has positive and negative orbit/mask weights", "positive source components can cancel in the readout average", "blocks positivity from bulk source density"),
        ("PCM1610_2_material_difference", "Ti/Pt differential response has signed components", "source-material vector is not purely positive in component space", "blocks positive cone unless component basis/covariance is signed"),
        ("PCM1610_3_domain_selector", "masks/windows select data samples and can act as sign/domain filters if not downstream-only", "readout domain can change projection support", "blocks parent theorem unless variation/readout order is signed"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": countermodel_id,
            "construction": construction,
            "math_result": result,
            "blocked_claim": blocked,
            "status": "COUNTERMODEL_RETAINED",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for countermodel_id, construction, result, blocked in rows
    ]


def source_pack_acceptance_rows() -> list[dict[str, Any]]:
    rows = [
        ("SPA1610_0_filelist", "CMSM_source_pack_filelist.csv", "dataset/product/file/checksum/download/role rows", False, "missing"),
        ("SPA1610_1_HAR", "CMSM_network_capture.har or parsed JSON", "authenticated REGARDS dataobject/download responses", False, "missing"),
        ("SPA1610_2_K_CMSM", "K_CMSM_readout.csv", "time/session/orbit/gx/gz/Sxx/Sxz/masks/calibration/sign/units", False, "missing"),
        ("SPA1610_3_alignment", "alignment_result.csv", "K_norm,V_norm,projection,c_min,tau_min,uncertainty", False, "missing"),
        ("SPA1610_4_verdict", "source-pack acceptance", "all required source-pack rows validated", False, "not accepted"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "acceptance_id": acceptance_id,
            "target_file": target_file,
            "required_content": required_content,
            "accepted": accepted,
            "status": status,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for acceptance_id, target_file, required_content, accepted, status in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1610_0_browser_HAR",
            "acceptance_rule": "browser/HAR route requires authenticated network capture or source-pack rows with filelist/checksums/download URLs",
            "input_state": "no HAR/source-pack rows in quarantine input",
            "runner_result": "NO_BROWSER_HAR_SOURCE_PACK_ACCEPTED",
            "effect": "official CMSM route remains open but not imported",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1610_1_positive_cone",
            "acceptance_rule": "positive-cone theorem requires sign-definite K and parent-restricted source-material cone disjoint from ker(K)",
            "input_state": "sign/cone/no-cancellation clauses unsigned",
            "runner_result": "REJECT_POSITIVE_CONE_THEOREM",
            "effect": "no tau_min theorem-zero",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1610_2_shortcuts",
            "acceptance_rule": "tau_eff=1, symbolic K alone, surrogate arrays, bound inversion and measured-G absorption remain forbidden",
            "input_state": "no official data or parent theorem",
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
        ("CG1610_0_HAR", "browser/HAR source-pack capture", "BLOCKED", "not executed; no HAR/source-pack file present"),
        ("CG1610_1_positive_cone", "positive-cone nondegeneracy theorem", "BLOCKED", "sign-definite readout and parent cone not signed"),
        ("CG1610_2_tau_min", "positive tau_min", "BLOCKED", "no official alignment and no parent cone theorem"),
        ("CG1610_3_K_arrays", "official K_CMSM arrays", "BLOCKED", "filelist/checksum/download rows missing"),
        ("CG1610_4_delta_w_bound", "numeric Delta_w bound", "BLOCKED", "tau_min missing"),
        ("CG1610_5_WEP_local_GR", "WEP/Newton/local-GR claim", "BLOCKED", "source-pack/tau/coupling gates open"),
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
            "decision_id": "DEC1610_0_browser_HAR",
            "decision": "BROWSER_HAR_SOURCE_PACK_NOT_EXECUTED",
            "reason": "no authenticated HAR/source-pack artifact is present in quarantine input",
            "next_action": "use browser operator or manual export to create CMSM_source_pack_filelist.csv/HAR rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1610_1_positive_cone",
            "decision": "POSITIVE_CONE_THEOREM_NOT_DERIVED",
            "reason": "sign-changing readout and source/material cancellation countermodels survive",
            "next_action": "derive sign-definite K/source cone theorem or compute alignment from official data",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1610_2_next",
            "decision": "NEXT_1611_SOURCE_PACK_IMPORT_VALIDATOR_OR_SIGN_DEFINITE_READOUT_THEOREM",
            "reason": "the next useful step is either validate a supplied CMSM source pack or attack sign-definiteness directly",
            "next_action": "build a validator for quarantine/1610 input files, or derive sign-definite readout/source cone conditions",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1611-Y5-R2FR-source-pack-import-validator-or-sign-definite-readout-theorem.md",
            "script": "scripts/Y5_R2FR_source_pack_import_validator_or_sign_definite_readout_theorem.py",
            "objective": "validate any supplied CMSM source-pack/HAR rows or derive sign-definite readout/source cone conditions needed for c_min>0",
            "success_condition": "quarantine source-pack validator accepts real filelist/checksum/readout rows as nonclaim input, or parent-signed sign/cone theorem closes the positive-cone route",
            "do_not": "do not use tau_eff=1, symbolic K alone, surrogate arrays, bound inversion, closure-only zero, measured-G absorption, or public/local-GR claims",
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


def no_formalization_1610() -> bool:
    if not FORMALIZATION.exists():
        return True
    artifact_markers = (
        "1610-Y5",
        "P8_Y5_PARENT_QLOC_1610",
        "P8_Y5_BRR545_1610",
        "Y5_R2FR_browser_HAR_source_pack_or_positive_cone_nondegeneracy",
        "R2FR_browser_HAR",
    )
    return not any(any(marker in path.name for marker in artifact_markers) for path in FORMALIZATION.rglob("*"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    contract = read_csv(BROWSER_HAR_CONTRACT)
    status = read_csv(BROWSER_HAR_STATUS)
    cone = read_csv(POSITIVE_CONE)
    counters = read_csv(CONE_COUNTERMODEL)
    source_pack = read_csv(SOURCE_PACK_ACCEPTANCE)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    copies = [target for targets in COPY_TARGETS.values() for target in targets]
    checks = [
        ("VAL1610_0_sources_exist", all(truthy(row["exists"]) for row in sources), "all cited 1610 local source paths exist"),
        ("VAL1610_1_needles_found", all(truthy(row["needle_found"]) for row in sources), "all required 1610 source needles found"),
        ("VAL1610_2_HAR_contract", len(contract) >= 5 and any(row["contract_id"] == "HAR1610_2_filelist" for row in contract), "browser/HAR source-pack contract written"),
        ("VAL1610_3_HAR_not_executed", any(row["status_id"] == "HST1610_0_execution" and row["execution_status"] == "NOT_EXECUTED_IN_1610" for row in status), "browser/HAR source-pack not falsely claimed"),
        ("VAL1610_4_positive_cone_lemma", any(row["theorem_id"] == "PCN1610_1_positive_functional_lemma" and row["status"] == "EXACT_CONDITIONAL_LEMMA" for row in cone), "positive-cone lemma recorded"),
        ("VAL1610_5_positive_cone_not_derived", any(row["theorem_id"] == "PCN1610_4_verdict" and row["status"] == "POSITIVE_CONE_THEOREM_NOT_DERIVED" for row in cone), "positive-cone theorem not promoted"),
        ("VAL1610_6_countermodels_retained", len(counters) >= 4 and all(row["status"] == "COUNTERMODEL_RETAINED" for row in counters), "cone/readout countermodels retained"),
        ("VAL1610_7_source_pack_not_accepted", any(row["acceptance_id"] == "SPA1610_4_verdict" and row["accepted"].lower() == "false" for row in source_pack), "source-pack acceptance remains false"),
        ("VAL1610_8_runner_rejects", any(row["runner_id"] == "RUN1610_1_positive_cone" and row["runner_result"] == "REJECT_POSITIVE_CONE_THEOREM" for row in runner), "runner rejects positive-cone theorem"),
        ("VAL1610_9_claim_gates_closed", gates and all(row["claim_allowed"].lower() == "false" and row["status"] == "BLOCKED" for row in gates), "all 1610 claim gates remain closed"),
        ("VAL1610_10_decision_next", any(row["decision"] == "NEXT_1611_SOURCE_PACK_IMPORT_VALIDATOR_OR_SIGN_DEFINITE_READOUT_THEOREM" for row in decisions), "decision selects 1611 source-pack validator or sign-definite theorem"),
        ("VAL1610_11_csv_parse", csv_parses(generated_csvs), "all generated 1610 CSVs parse"),
        ("VAL1610_12_claim_safety_flags", no_claim_flags(generated_csvs), "no generated 1610 rows are score-ready, prediction rows, valid-for-claim, or claim-allowed"),
        ("VAL1610_13_branch_copies", all(path.exists() for path in copies), "branch/quarantine nonclaim copies exist"),
        ("VAL1610_14_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1610_15_formalization_untouched", no_formalization_1610(), "no 1610 outputs found under formalization-workbench"),
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
            "check_id": "VAL1610_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1610 browser/HAR source-pack or positive-cone nondegeneracy validation",
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
    status: list[dict[str, Any]],
    cone: list[dict[str, Any]],
    counters: list[dict[str, Any]],
    source_pack: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1610 - R2/fR Browser/HAR Source Pack Or Positive-Cone Nondegeneracy",
                "## Verdict\n"
                "- 1610 formalizes the authenticated CMSM browser/HAR capture route but does not execute or claim it.\n"
                "- The positive-cone theorem route is mathematically clean as a conditional lemma: if the allowed source-material cone stays a positive distance from `ker(K_CMSM)`, then `c_min>0` follows.\n"
                "- The theorem is not derived because sign-definite readout, parent-restricted source cone, material covariance, and no-cancellation clauses are not signed.\n"
                "- The countermodels are retained: sign-changing orbit/readout weights and signed Ti/Pt differential material components can still cancel.\n"
                "- No WEP, R10, PPN, clock, orbital, Newton, local-GR, beta/coupling, or public claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## Browser/HAR Capture Contract",
                md_table(contract, ["contract_id", "object", "required_action", "accepted_evidence", "current_status"]),
                "## Browser/HAR Capture Status",
                md_table(status, ["status_id", "route", "execution_status", "reason", "filelist_acquired"]),
                "## Positive-Cone Theorem Attempt",
                md_table(cone, ["theorem_id", "status", "what_is_exact", "blocking_gap", "theorem_closed"]),
                "## Cone Countermodel Audit",
                md_table(counters, ["countermodel_id", "construction", "math_result", "blocked_claim"]),
                "## Source-Pack Acceptance Gate",
                md_table(source_pack, ["acceptance_id", "target_file", "accepted", "status"]),
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
    contract = browser_har_contract_rows()
    status = browser_har_status_rows()
    cone = positive_cone_rows()
    counters = cone_countermodel_rows()
    source_pack = source_pack_acceptance_rows()
    runner = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        BROWSER_HAR_CONTRACT,
        BROWSER_HAR_STATUS,
        POSITIVE_CONE,
        CONE_COUNTERMODEL,
        SOURCE_PACK_ACCEPTANCE,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(BROWSER_HAR_CONTRACT, contract)
    write_csv(BROWSER_HAR_STATUS, status)
    write_csv(POSITIVE_CONE, cone)
    write_csv(CONE_COUNTERMODEL, counters)
    write_csv(SOURCE_PACK_ACCEPTANCE, source_pack)
    write_csv(RUNNER, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, contract, status, cone, counters, source_pack, runner, gates, decisions, next_rows, validation)


if __name__ == "__main__":
    main()
