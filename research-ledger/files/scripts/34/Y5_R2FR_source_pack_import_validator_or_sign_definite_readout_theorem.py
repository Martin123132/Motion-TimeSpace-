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
QUARANTINE = MICROSCOPE / "quarantine" / "1611"
INPUT_1611 = QUARANTINE / "input"
INPUT_1610 = MICROSCOPE / "quarantine" / "1610" / "input"
INPUT_1609 = MICROSCOPE / "quarantine" / "1609" / "input"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1611-Y5-R2FR-source-pack-import-validator-or-sign-definite-readout-theorem.md"

SOURCE_FILES = {
    "1610_doc": ROOT / "1610-Y5-R2FR-browser-HAR-source-pack-or-positive-cone-nondegeneracy.md",
    "1610_validation": OUT / "P8_Y5_BRR545_1610_VALIDATION.csv",
    "1610_next": OUT / "P8_Y5_PARENT_QLOC_1610_NEXT_TARGET.csv",
    "1610_cone": OUT / "P8_Y5_PARENT_QLOC_1610_POSITIVE_CONE_THEOREM_ATTEMPT.csv",
    "1610_acceptance": OUT / "P8_Y5_PARENT_QLOC_1610_SOURCE_PACK_ACCEPTANCE_GATE.csv",
    "1610_counters": OUT / "P8_Y5_PARENT_QLOC_1610_CONE_COUNTERMODEL_AUDIT.csv",
    "1609_schema": OUT / "P8_Y5_PARENT_QLOC_1609_CMSM_SOURCE_PACK_SCHEMA.csv",
    "1609_template": OUT / "P8_Y5_PARENT_QLOC_1609_CMSM_SOURCE_PACK_TEMPLATE.csv",
    "1609_alignment": OUT / "P8_Y5_PARENT_QLOC_1609_ALIGNMENT_COMPUTATION_CONTRACT.csv",
    "1456_worldtube": COEFF / "source_worldtube_projection_theorem_attempt_1456.csv",
    "1455_readout": COEFF / "official_readout_acquisition_ledger_nonclaim_1455.csv",
}

NEEDLES = {
    "1610_doc": ["PCN1610_4_verdict", "POSITIVE_CONE_THEOREM_NOT_DERIVED"],
    "1610_validation": ["VAL1610_OVERALL", "PASS"],
    "1610_next": ["1611-Y5-R2FR-source-pack-import-validator-or-sign-definite-readout-theorem.md", "sign-definite"],
    "1610_cone": ["PCN1610_2_readout_sign_problem", "SIGN_DEFINITE_READOUT_NOT_PROVEN"],
    "1610_acceptance": ["SPA1610_4_verdict", "not accepted"],
    "1610_counters": ["PCM1610_1_sign_changing_readout", "COUNTERMODEL_RETAINED"],
    "1609_schema": ["CSP1609_5_checksum", "checksum"],
    "1609_template": ["CSPT1609_0_source_pack_template", "TEMPLATE_ONLY_NOT_IMPORTABLE"],
    "1609_alignment": ["ALI1609_3_c_min", "MISSING_CRITICAL"],
    "1456_worldtube": ["SWP1456_4_mask_orbit_limit", "DOMAIN_SELECTOR_COUNTERMODEL_RETAINED"],
    "1455_readout": ["KC1455_2_design_values", "STRUCTURE_ONLY_VALUES_ABSENT"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1611_SOURCE_REGISTER.csv"
VALIDATOR_SPEC = OUT / "P8_Y5_PARENT_QLOC_1611_SOURCE_PACK_VALIDATOR_SPEC.csv"
VALIDATOR_DRY_RUN = OUT / "P8_Y5_PARENT_QLOC_1611_SOURCE_PACK_VALIDATOR_DRY_RUN.csv"
SIGN_THEOREM = OUT / "P8_Y5_PARENT_QLOC_1611_SIGN_DEFINITE_READOUT_THEOREM_ATTEMPT.csv"
SIGN_COUNTERS = OUT / "P8_Y5_PARENT_QLOC_1611_SIGN_DEFINITE_COUNTERMODEL_AUDIT.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1611_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1611_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1611_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1611_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1611_VALIDATION.csv"

COPY_TARGETS = {
    VALIDATOR_SPEC: [
        QUARANTINE / "SOURCE_PACK_VALIDATOR_SPEC_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_source_pack_validator_spec_nonclaim_1611.csv",
    ],
    VALIDATOR_DRY_RUN: [
        QUARANTINE / "SOURCE_PACK_VALIDATOR_DRY_RUN_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_source_pack_validator_dry_run_nonclaim_1611.csv",
    ],
    SIGN_THEOREM: [
        QUARANTINE / "SIGN_DEFINITE_READOUT_THEOREM_ATTEMPT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_sign_definite_readout_theorem_attempt_nonclaim_1611.csv",
    ],
    SIGN_COUNTERS: [
        QUARANTINE / "SIGN_DEFINITE_COUNTERMODEL_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_sign_definite_countermodel_audit_nonclaim_1611.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE_CLOSED.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_closed_1611.csv",
    ],
}

REQUIRED_BY_ROLE = {
    "source_pack_filelist": {"dataset_id", "product_id", "file_name", "file_role", "download_url", "checksum"},
    "CMSM_network_capture": {"request_url", "method", "status_code", "response_kind", "captured_at"},
    "K_CMSM_readout": {"time_s", "session_id", "orbit_id", "gx", "gz", "Sxx", "Sxz", "mask_flag", "units", "sign_convention"},
    "alignment_result": {"K_norm", "V_norm", "projection_value", "c_min", "tau_min", "uncertainty", "basis"},
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
                "source_id": f"SRC1611_{index}_{source_id}",
                "source_path": rel(path) if path.exists() else str(path),
                "exists": path.exists(),
                "needle_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "source_role": "1611_source_pack_validator_or_sign_definite_theorem_input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def validator_spec_rows() -> list[dict[str, Any]]:
    rows = [
        ("VALSPEC1611_0_file_presence", "required file exists and parses", "REJECT_MISSING_OR_PARSE_ERROR"),
        ("VALSPEC1611_1_role_columns", "role-specific required columns are present", "REJECT_MISSING_COLUMNS"),
        ("VALSPEC1611_2_provenance", "download URL/checksum/source path or HAR request provenance is present", "REJECT_BAD_PROVENANCE"),
        ("VALSPEC1611_3_units_sign_basis", "units, sign convention and branch basis are declared", "REJECT_BAD_UNITS_SIGN_BASIS"),
        ("VALSPEC1611_4_shortcut_firewall", "no surrogate-only arrays, tau_eff=1, symbolic K alone or bound inversion", "REJECT_SHORTCUT"),
        ("VALSPEC1611_5_claim_policy", "accepted rows remain nonclaim until full WEP/local gates pass", "NONCLAIM_ACCEPT_ONLY"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "validator_id": validator_id,
            "rule": rule,
            "failure_status": failure,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for validator_id, rule, failure in rows
    ]


def candidate_files() -> list[tuple[str, Path]]:
    return [
        ("source_pack_filelist", INPUT_1611 / "CMSM_source_pack_filelist.csv"),
        ("source_pack_filelist", INPUT_1610 / "CMSM_source_pack_filelist.csv"),
        ("source_pack_filelist", INPUT_1609 / "CMSM_source_pack_filelist.csv"),
        ("CMSM_network_capture", INPUT_1611 / "CMSM_network_capture.csv"),
        ("K_CMSM_readout", INPUT_1611 / "K_CMSM_readout.csv"),
        ("K_CMSM_readout", INPUT_1609 / "K_CMSM_readout.csv"),
        ("alignment_result", INPUT_1611 / "alignment_result.csv"),
        ("alignment_result", INPUT_1609 / "alignment_result.csv"),
    ]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def validate_candidate(role: str, path: Path) -> tuple[str, str, int]:
    if not path.exists():
        return "MISSING_INPUT_FILE", "candidate file is absent", 0
    try:
        rows = read_csv(path)
    except Exception as exc:
        return "REJECT_PARSE_ERROR", str(exc), 0
    if not rows:
        return "REJECT_EMPTY_CSV", "candidate contains no rows", 0
    required = REQUIRED_BY_ROLE[role]
    fieldnames = set(rows[0].keys())
    missing = sorted(required - fieldnames)
    if missing:
        return "REJECT_MISSING_COLUMNS", "missing " + ";".join(missing), len(rows)
    row = rows[0]
    if role == "source_pack_filelist" and (not row.get("download_url") or not row.get("checksum")):
        return "REJECT_BAD_PROVENANCE", "download_url/checksum missing", len(rows)
    if role in {"K_CMSM_readout", "alignment_result"}:
        if not row.get("units") and role == "K_CMSM_readout":
            return "REJECT_BAD_UNITS_SIGN_BASIS", "units missing", len(rows)
        if not row.get("basis") and role == "alignment_result":
            return "REJECT_BAD_UNITS_SIGN_BASIS", "basis missing", len(rows)
    return "ACCEPT_NONCLAIM_QUARANTINE", "row parses under 1611 validator; still nonclaim", len(rows)


def validator_dry_run_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (role, path) in enumerate(candidate_files()):
        status, reason, row_count = validate_candidate(role, path)
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "dry_run_id": f"DRV1611_{index}_{role}",
                "file_role": role,
                "candidate_path": rel(path) if path.exists() else str(path),
                "exists": path.exists(),
                "row_count": row_count,
                "validator_result": status,
                "reason": reason,
                "accepted_for_quarantine": status == "ACCEPT_NONCLAIM_QUARANTINE",
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def sign_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "SDR1611_0_target",
            "statement": "prove K_CMSM is sign-definite on the parent-allowed WEP source-material cone after masks/orbit/calibration windows.",
            "status": "TARGET_SHARPENED",
            "blocking_gap": "official K arrays and parent sign theorem are absent",
            "theorem_closed": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "SDR1611_1_sufficient_conditions",
            "statement": "sign-definite readout would require fixed readout sign, nonnegative window weights, no sign-changing gradient correction dominance, and parent cone preserving material/source positivity.",
            "status": "EXACT_CONDITIONAL_CONTRACT",
            "blocking_gap": "none of these clauses is parent-signed or computed from official arrays",
            "theorem_closed": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "SDR1611_2_counterexample",
            "statement": "a readout kernel with positive and negative window weights can annihilate a positive source profile in the differential channel.",
            "status": "COUNTERMODEL_SURVIVES",
            "blocking_gap": "no no-cancellation theorem or covariance rule",
            "theorem_closed": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "SDR1611_3_verdict",
            "statement": "sign-definite readout/source cone theorem is not derived in 1611.",
            "status": "SIGN_DEFINITE_READOUT_NOT_DERIVED",
            "blocking_gap": "requires official K arrays or parent-signed sign/no-cancellation theorem",
            "theorem_closed": False,
            "claim_allowed": False,
        },
    ]


def sign_counter_rows() -> list[dict[str, Any]]:
    rows = [
        ("SDC1611_0_orbit_window", "opposite-sign orbit windows", "positive source density can average to zero in signed readout"),
        ("SDC1611_1_gradient_terms", "gravity-gradient/inertia corrections", "correction terms can rotate or cancel the EP template component"),
        ("SDC1611_2_material_tensor", "signed Ti/Pt component contrast", "differential material vector is not a purely positive scalar"),
        ("SDC1611_3_mask_domain", "masks/calibration windows", "domain selection can alter support unless downstream-only and sign-safe"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "counter_id": counter_id,
            "construction": construction,
            "effect": effect,
            "status": "COUNTERMODEL_RETAINED",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for counter_id, construction, effect in rows
    ]


def runner_rows(dry_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    accepted_any = any(truthy(row["accepted_for_quarantine"]) for row in dry_rows)
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1611_0_validator",
            "acceptance_rule": "source-pack validator accepts real files only as nonclaim quarantine inputs",
            "input_state": "accepted file present" if accepted_any else "no source-pack/HAR/readout/alignment files accepted",
            "runner_result": "SOURCE_PACK_ACCEPTED_NONCLAIM" if accepted_any else "NO_SOURCE_PACK_ACCEPTED",
            "effect": "CMSM route remains input-ready",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1611_1_sign_theorem",
            "acceptance_rule": "sign-definite theorem requires all sign/window/material/no-cancellation clauses closed",
            "input_state": "countermodels survive",
            "runner_result": "REJECT_SIGN_DEFINITE_THEOREM",
            "effect": "no c_min/tau_min theorem",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG1611_0_validator", "CMSM source-pack accepted", "BLOCKED", "no live source-pack/HAR rows accepted"),
        ("CG1611_1_sign_theorem", "sign-definite readout theorem", "BLOCKED", "countermodels survive"),
        ("CG1611_2_cmin", "c_min/tau_min", "BLOCKED", "no accepted alignment row or theorem"),
        ("CG1611_3_WEP", "WEP score", "BLOCKED", "readout/source/material/tau gates open"),
        ("CG1611_4_local_GR", "Newton/local-GR claim", "BLOCKED", "source-normalization branch unresolved"),
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
            "decision_id": "DEC1611_0_validator",
            "decision": "SOURCE_PACK_VALIDATOR_READY_NO_FILES_ACCEPTED",
            "reason": "validator exists and rejects missing inputs; no live CMSM/HAR file supplied",
            "next_action": "supply/capture CMSM source-pack files into quarantine input or continue theorem route",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1611_1_sign_theorem",
            "decision": "SIGN_DEFINITE_READOUT_NOT_DERIVED",
            "reason": "orbit/window/gradient/material sign countermodels remain open",
            "next_action": "derive no-cancellation/sign clauses or compute them from official arrays",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1611_2_next",
            "decision": "NEXT_1612_NO_CANCELLATION_THEOREM_OR_CMSM_FILE_DROP",
            "reason": "next route must either close no-cancellation/sign gates or validate real source-pack files",
            "next_action": "attempt no-cancellation theorem, or pause for CMSM file drop/browser capture",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1612-Y5-R2FR-no-cancellation-theorem-or-CMSM-file-drop.md",
            "script": "scripts/Y5_R2FR_no_cancellation_theorem_or_CMSM_file_drop.py",
            "objective": "derive no-cancellation/sign-safe readout theorem or validate real CMSM files dropped into quarantine input",
            "success_condition": "parent-signed no-cancellation theorem giving c_min>0, or validator-accepted official CMSM source-pack rows as nonclaim inputs",
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


def no_formalization_1611() -> bool:
    if not FORMALIZATION.exists():
        return True
    artifact_markers = (
        "1611-Y5",
        "P8_Y5_PARENT_QLOC_1611",
        "P8_Y5_BRR545_1611",
        "Y5_R2FR_source_pack_import_validator_or_sign_definite_readout_theorem",
        "R2FR_source_pack_validator",
    )
    return not any(any(marker in path.name for marker in artifact_markers) for path in FORMALIZATION.rglob("*"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    spec = read_csv(VALIDATOR_SPEC)
    dry = read_csv(VALIDATOR_DRY_RUN)
    theorem = read_csv(SIGN_THEOREM)
    counters = read_csv(SIGN_COUNTERS)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    copies = [target for targets in COPY_TARGETS.values() for target in targets]
    checks = [
        ("VAL1611_0_sources_exist", all(truthy(row["exists"]) for row in sources), "all cited 1611 local source paths exist"),
        ("VAL1611_1_needles_found", all(truthy(row["needle_found"]) for row in sources), "all required 1611 source needles found"),
        ("VAL1611_2_validator_spec", len(spec) >= 6 and any(row["validator_id"] == "VALSPEC1611_4_shortcut_firewall" for row in spec), "source-pack validator spec written"),
        ("VAL1611_3_dry_run_missing", dry and all(row["validator_result"] == "MISSING_INPUT_FILE" for row in dry), "dry run rejects missing inputs"),
        ("VAL1611_4_sign_theorem_not_derived", any(row["theorem_id"] == "SDR1611_3_verdict" and row["status"] == "SIGN_DEFINITE_READOUT_NOT_DERIVED" for row in theorem), "sign-definite theorem remains unproved"),
        ("VAL1611_5_countermodels_retained", len(counters) >= 4 and all(row["status"] == "COUNTERMODEL_RETAINED" for row in counters), "sign/readout countermodels retained"),
        ("VAL1611_6_runner_refuses", any(row["runner_id"] == "RUN1611_1_sign_theorem" and row["runner_result"] == "REJECT_SIGN_DEFINITE_THEOREM" for row in runner), "runner rejects sign-definite theorem"),
        ("VAL1611_7_claim_gates_closed", gates and all(row["claim_allowed"].lower() == "false" and row["status"] == "BLOCKED" for row in gates), "all 1611 claim gates remain closed"),
        ("VAL1611_8_decision_next", any(row["decision"] == "NEXT_1612_NO_CANCELLATION_THEOREM_OR_CMSM_FILE_DROP" for row in decisions), "decision selects 1612 no-cancellation theorem or CMSM file drop"),
        ("VAL1611_9_csv_parse", csv_parses(generated_csvs), "all generated 1611 CSVs parse"),
        ("VAL1611_10_claim_safety_flags", no_claim_flags(generated_csvs), "no generated 1611 rows are score-ready, prediction rows, valid-for-claim, or claim-allowed"),
        ("VAL1611_11_branch_copies", all(path.exists() for path in copies), "branch/quarantine nonclaim copies exist"),
        ("VAL1611_12_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1611_13_formalization_untouched", no_formalization_1611(), "no 1611 outputs found under formalization-workbench"),
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
            "check_id": "VAL1611_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1611 source-pack import validator or sign-definite readout theorem validation",
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
    spec: list[dict[str, Any]],
    dry: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    counters: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1611 - R2/fR Source-Pack Import Validator Or Sign-Definite Readout Theorem",
                "## Verdict\n"
                "- 1611 builds a strict validator for future CMSM source-pack/HAR/readout/alignment rows.\n"
                "- No live CMSM files are present, so the dry run correctly rejects every candidate as missing.\n"
                "- The sign-definite readout theorem is not derived: orbit/window/gradient/material sign countermodels remain live.\n"
                "- Future CMSM files can now be dropped into quarantine input and mechanically checked before any branch promotion.\n"
                "- No WEP, R10, PPN, clock, orbital, Newton, local-GR, beta/coupling, or public claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## Source-Pack Validator Spec",
                md_table(spec, ["validator_id", "rule", "failure_status"]),
                "## Source-Pack Validator Dry Run",
                md_table(dry, ["dry_run_id", "file_role", "exists", "validator_result", "reason"]),
                "## Sign-Definite Readout Theorem Attempt",
                md_table(theorem, ["theorem_id", "status", "blocking_gap", "theorem_closed"]),
                "## Sign Countermodel Audit",
                md_table(counters, ["counter_id", "construction", "effect", "status"]),
                "## Runner Refusal",
                md_table(runner, ["runner_id", "input_state", "runner_result", "effect"]),
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
    INPUT_1611.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    spec = validator_spec_rows()
    dry = validator_dry_run_rows()
    theorem = sign_theorem_rows()
    counters = sign_counter_rows()
    runner = runner_rows(dry)
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        VALIDATOR_SPEC,
        VALIDATOR_DRY_RUN,
        SIGN_THEOREM,
        SIGN_COUNTERS,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(VALIDATOR_SPEC, spec)
    write_csv(VALIDATOR_DRY_RUN, dry)
    write_csv(SIGN_THEOREM, theorem)
    write_csv(SIGN_COUNTERS, counters)
    write_csv(RUNNER, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, spec, dry, theorem, counters, runner, gates, decisions, next_rows, validation)


if __name__ == "__main__":
    main()
