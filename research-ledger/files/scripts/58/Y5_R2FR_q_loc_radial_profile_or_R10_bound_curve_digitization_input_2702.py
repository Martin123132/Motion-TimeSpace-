from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "2702"
BRANCH_ID = "Y5_R2FR_Q_LOC_RADIAL_PROFILE_OR_R10_BOUND_CURVE_DIGITIZATION_INPUT_2702"

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"
LOCAL_BOUNDS = SOURCE_INTAKE / "local_bounds"
WEP_RESIDUALS = SOURCE_INTAKE / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT = SOURCE_INTAKE / "source-weight"
RAB_QUEUE = SOURCE_INTAKE / "rab-sector" / "acquisition-queue"

DOC_PATH = ROOT / "2702-Y5-R2FR-q-loc-radial-profile-or-R10-bound-curve-digitization-input.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2702_SOURCE_REGISTER.csv",
    "profile_asset_audit": RESIDUALS / "P8_Y5_R2FR_2702_QLOC_PROFILE_ASSET_AUDIT.csv",
    "profile_input_schema": RESIDUALS / "P8_Y5_R2FR_2702_QLOC_R10_PROFILE_INPUT_SCHEMA_NONCLAIM.csv",
    "r10_bound_digitization_contract": RESIDUALS / "P8_Y5_R2FR_2702_R10_BOUND_CURVE_DIGITIZATION_CONTRACT.csv",
    "acquisition_queue": RESIDUALS / "P8_Y5_R2FR_2702_ACQUISITION_QUEUE.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2702_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2702_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2702_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2702_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2702_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_profile_schema": LOCAL_BOUNDS / "q_loc_R10_profile_input_schema_2702_NONCLAIM.csv",
    "local_bound_contract": LOCAL_BOUNDS / "R10_bound_curve_digitization_contract_2702_NONCLAIM.csv",
    "wep_profile_schema": WEP_RESIDUALS / "q_loc_R10_profile_input_schema_2702_NONCLAIM.csv",
    "source_weight_profile_schema": SOURCE_WEIGHT / "QLOC_R10_PROFILE_INPUT_SCHEMA_2702_NONCLAIM.csv",
    "rab_next": RAB_QUEUE / "JR2702_QLOC_PROFILE_OR_BOUND_CURVE_EXECUTION_NEXT.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2702_2701_NEXT",
        "relative_path": "2701-Y5-R2FR-q-loc-PPN-kernel-or-R10-alpha-response-operator-fill.md",
        "required_needles": ["R10OP2701_0_QLOC_YUKAWA_ALPHA_RESPONSE", "MISS2701_0_q_loc_profile", "NEXT2701_0_selected", "VAL2701_OVERALL"],
        "purpose": "imports the R10 alpha operator and selected profile/bound-curve target",
    },
    {
        "source_id": "SRC2702_1712_PROFILE_TEMPLATE",
        "relative_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1712_FIRST_QLOC_PROFILE_ROW.csv",
        "required_needles": ["QPROF1712_0_parent_residual_vector", "QPROF1712_1_R10_projection"],
        "purpose": "imports first q_loc profile template rows",
    },
    {
        "source_id": "SRC2702_1790_PROFILE_FALLBACK",
        "relative_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1790_QLOC_PROFILE_FALLBACK.csv",
        "required_needles": ["QLP1790_1_profile_values", "MISSING_NUMERIC_PROFILE"],
        "purpose": "imports q_loc fallback profile status",
    },
    {
        "source_id": "SRC2702_2038_FIRST_REAL_ROW",
        "relative_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2038_FIRST_REAL_ROW_ACQUISITION.csv",
        "required_needles": ["ACQ2038_0_C_R_norm_bound_target", "ACQ2038_1_Q_R_prediction_value"],
        "purpose": "imports real external PPN bound target and missing prediction row status",
    },
    {
        "source_id": "SRC2702_563_R10",
        "relative_path": "563-Y5-R10-real-bound-curve-acquisition-and-alpha-row-smoke-runner.md",
        "required_needles": ["E563_1_full_curve_missing", "B563_0_no_full_bound_curve", "RU563_0_data_route"],
        "purpose": "imports R10 full-curve missing status",
    },
    {
        "source_id": "SRC2702_DIGITIZATION_CONTRACT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_BOUND_CURVE_DIGITIZATION_CONTRACT.csv",
        "required_needles": ["BDC559_0_required_columns", "BDC559_2_source_provenance", "BDC559_3_interpolation_policy"],
        "purpose": "imports existing bound-curve digitization contract",
    },
    {
        "source_id": "SRC2702_LIVE_BOUND_PLACEHOLDER",
        "relative_path": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
        "required_needles": ["R10_BOUND_PLACEHOLDER_0", "MISSING_NUMERIC_LAMBDA"],
        "purpose": "imports live placeholder bound curve status",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def as_bool(value: bool) -> str:
    return "true" if value else "false"


def path_for(relative_path: str) -> Path:
    return ROOT / relative_path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            if not reader.fieldnames:
                return False, 0, "missing_header"
            return True, len(rows), "parsed"
    except Exception as exc:  # pragma: no cover
        return False, 0, f"{type(exc).__name__}: {exc}"


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        cells = [str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = path_for(spec["relative_path"])
        text = read_text(path)
        needles = list(spec["required_needles"])
        found = [needle for needle in needles if needle in text]
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "source_id": spec["source_id"],
                "relative_path": spec["relative_path"],
                "absolute_path": str(path),
                "exists": as_bool(path.exists()),
                "required_needles": ";".join(needles),
                "found_needles": ";".join(found),
                "missing_needles": ";".join(missing),
                "purpose": spec["purpose"],
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def profile_asset_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("PA2702_0_1712_vector", "P8_Y5_PARENT_QLOC_1712_FIRST_QLOC_PROFILE_ROW.csv", "q_loc^nu finite residual vector", "template_only_not_scoreable", "MISSING_COMPONENT_LOCK;MISSING_JZ_BZ;MISSING_DELTA_K;MISSING_PLOC_OWNER;MISSING_UNITS", "not a numeric radial/range profile"),
        ("PA2702_1_1712_R10", "P8_Y5_PARENT_QLOC_1712_FIRST_QLOC_PROFILE_ROW.csv", "q_loc/B_mem -> alpha(lambda)", "template_only_not_scoreable", "MISSING_PARENT_COEFFICIENTS;MISSING_NUMERIC_PROFILE", "not usable for 2701 alpha operator"),
        ("PA2702_2_1790_values", "P8_Y5_PARENT_QLOC_1790_QLOC_PROFILE_FALLBACK.csv", "q_loc^nu(r,material,domain)", "TEMPLATE_ONLY_NOT_SCOREABLE", "MISSING_NUMERIC_PROFILE;MISSING_UNITS;MISSING_SOURCE_PATH", "confirms profile row is absent"),
        ("PA2702_3_2038_bound", "P8_Y5_PARENT_QLOC_2038_FIRST_REAL_ROW_ACQUISITION.csv", "C_R_norm Cassini/PPN external bound target", "ACQUIRED_REAL_BOUND_TARGET_NONCLAIM", "MTS prediction Q_R/C_R_norm is missing", "real ruler but not an R10 q_loc profile"),
        ("PA2702_4_verdict", "profile asset audit", "q_loc radial/range profile for alpha_q(lambda)", "PROFILE_NOT_FOUND_CURRENT_CORPUS", "must derive/source profile or choose bound-curve data path", "stage profile schema and bound-curve contract"),
    ]
    return [
        {
            "audit_id": audit_id,
            "asset": asset,
            "object": obj,
            "status": status,
            "blocking_gap": gap,
            "decision_note": note,
            "profile_found": "false",
            "score_ready": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for audit_id, asset, obj, status, gap, note in rows
    ]


def profile_input_schema_rows() -> list[dict[str, Any]]:
    return [
        {
            "schema_id": "QPROF2702_0_required_prediction_row",
            "row_type": "q_loc_R10_profile_prediction",
            "required_columns": "profile_id;component_id;source_body;test_body;frame;r_value;r_units;lambda_value;lambda_units;q_loc_value;q_loc_units;converted_a_q_value;converted_a_q_units;a_N_value;a_N_units;alpha_q_value;alpha_q_units;normalization;source_paths;equation_refs;assumptions;valid_for_claim",
            "formula": "alpha_q(lambda;r)=a_q(r,lambda)/a_N(r)*exp(r/lambda)/(1+r/lambda)",
            "acceptance_rule": "valid_for_claim may become true only when q_loc_value/converted_a_q/a_N/lambda/r are numeric, units are SI-convertible, source_paths exist, and no MISSING markers remain",
            "current_row_status": "SCHEMA_ONLY_NO_NUMERIC_PROFILE",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "schema_id": "QPROF2702_1_theorem_zero_certificate",
            "row_type": "q_loc_R10_theorem_zero_replacement",
            "required_columns": "certificate_id;theorem_statement;premises;source_paths;covers_components;covers_range;covers_source_frame;boundary_no_flux;P_loc_owner;valid_for_claim",
            "formula": "q_loc^nu=0 for all compact local R10 test configurations implies alpha_q(lambda)=0",
            "acceptance_rule": "valid_for_claim may become true only if the parent theorem covers Gamma/Khat metric response, Euler/source zero, boundary no-flux, P_loc owner and source-frame normalization",
            "current_row_status": "SCHEMA_ONLY_NO_THEOREM",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
    ]


def r10_bound_digitization_contract_rows() -> list[dict[str, Any]]:
    rows = [
        ("BDC2702_0_target_file", "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv", "replace placeholder rows with source-backed numeric rows only after extraction QA", "bound_id;dataset_id;lambda_value;lambda_units;alpha_bound;alpha_bound_source;digitization_method;source_file;valid_for_claim;notes", "placeholder_invalid"),
        ("BDC2702_1_primary_source", "Eot-Wash 2020 PRL 124 101101 / arXiv:2002.11761", "extract full alpha(lambda) bound curve or locate machine-readable table", "source URL/DOI, figure/table id, extraction method, confidence, point count", "not_acquired"),
        ("BDC2702_2_continuity_source", "Eot-Wash 2007 PRL 98 021101 / arXiv:hep-ph/0611184", "optional continuity curve/anchor, not modern primary score unless full curve extracted", "source URL/DOI and extraction method", "anchor_only_present"),
        ("BDC2702_3_numeric_rule", "positive numeric curve rows", "lambda_value>0 in meters and alpha_bound>0 dimensionless with no MISSING markers", "unit conversion and parse validation", "required_before_claim"),
        ("BDC2702_4_interpolation_rule", "log-log interpolation", "allow only within sampled lambda range and only when both bracketing rows are valid_for_claim=true", "do not extrapolate anchor-only thresholds", "required_before_claim"),
        ("BDC2702_5_claim_policy", "claim validity", "bound curve alone never proves MTS; it only supplies comparison target after alpha_q prediction row exists", "valid MTS prediction and valid bound row both required", "guardrail_active"),
    ]
    return [
        {
            "contract_id": contract_id,
            "artifact_or_source": artifact,
            "requirement": requirement,
            "required_metadata": metadata,
            "current_status": status,
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
        for contract_id, artifact, requirement, metadata, status in rows
    ]


def acquisition_queue_rows() -> list[dict[str, Any]]:
    rows = [
        ("ACQ2702_0_profile_derivation", "derive q_loc profile from parent GK residual", "q_loc^r(r,lambda,source,frame) or theorem-zero certificate", "highest", "theory_path", "MISSING_PARENT_GK_PROFILE"),
        ("ACQ2702_1_source_normalization", "lock a_N denominator", "M_source/H_tau/Pi_M same-frame source mass and test-body normalization", "high", "theory_path", "MISSING_SOURCE_MEASURE"),
        ("ACQ2702_2_bound_curve", "digitize/acquire full R10 alpha(lambda) bound curve", "positive numeric lambda/alpha rows from 2020 Eot-Wash or official table", "high", "data_path", "MISSING_FULL_BOUND_CURVE"),
        ("ACQ2702_3_runner_dryrun", "wire alpha_q rows into existing comparator", "dry-run only with valid_for_claim=false until prediction and bound both valid", "medium", "pipeline_path", "MISSING_SCORE_INPUTS"),
    ]
    return [
        {
            "queue_id": queue_id,
            "task": task,
            "deliverable": deliverable,
            "priority": priority,
            "route": route,
            "blocking_status": status,
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
        for queue_id, task, deliverable, priority, route, status in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2702_0_profile", "source-backed q_loc radial/range profile exists", "BLOCKED_NONCLAIM", "false", "false", "only templates exist"),
        ("CG2702_1_bound_curve", "full R10 alpha(lambda) bound curve exists", "BLOCKED_NONCLAIM", "false", "false", "live curve is placeholder; anchors are noncurve"),
        ("CG2702_2_schema", "profile and bound schemas are executable", "PASS_NONCLAIM_SCHEMA", "true", "false", "input contract now exists"),
        ("CG2702_3_score", "R10 score can be run for claim", "BLOCKED_NONCLAIM", "false", "false", "prediction row and bound curve are missing"),
        ("CG2702_4_local_GR", "local GR/Newton can be claimed", "BLOCKED_NONCLAIM", "false", "false", "q_loc remains unbounded finite residual"),
        ("CG2702_5_public", "public/GitHub readiness", "BLOCKED_PRIVATE_WORK", "false", "false", "private input checkpoint only"),
    ]
    return [
        {
            "claim_gate_id": gate_id,
            "gate": gate,
            "status": status,
            "gate_passed": passed,
            "claim_allowed": allowed,
            "reason": reason,
            "timestamp_utc": stamp(),
        }
        for gate_id, gate, status, passed, allowed, reason in rows
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2702_0_profile_audit", "NO_QLOC_PROFILE_FOUND", "current profile assets are templates or external bound targets, not a q_loc radial/range prediction", "do not score alpha_q"),
        ("DEC2702_1_schema", "QLOC_R10_PROFILE_SCHEMA_WRITTEN", "future profile rows now have exact columns, units and claim gates", "use before any R10 comparator run"),
        ("DEC2702_2_bound_curve", "FULL_BOUND_CURVE_DIGITIZATION_CONTRACT_WRITTEN", "placeholder/anchor-only rows cannot support a real R10 score", "digitize or source table before claim"),
        ("DEC2702_3_next", "PROFILE_OR_DIGITIZATION_EXECUTION_NEXT", "one of the two missing inputs must move before more R10 theory-score work is meaningful", "run 2703"),
    ]
    return [
        {
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "next_action": next_action,
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
        for decision_id, decision, rationale, next_action in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2702_0_selected",
            "selection": "selected_primary",
            "target_doc": "2703-Y5-R2FR-R10-bound-curve-digitization-dryrun-or-q-loc-profile-source-hunt.md",
            "target_script": "scripts/Y5_R2FR_R10_bound_curve_digitization_dryrun_or_q_loc_profile_source_hunt_2703.py",
            "task": "attempt a dry-run acquisition path for the full R10 bound curve and a targeted q_loc profile source hunt; write blockers rather than score placeholders",
            "success_condition": "either a candidate digitization workflow produces nonclaim numeric rows requiring QA, or the q_loc profile source hunt records exact missing parent inputs and source paths",
            "forbidden_shortcuts": "anchor-only scoring; invented profile; symbolic alpha as number; local-GR/R10 claim; GitHub action; formalization-workbench edits",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("STATUS2702_0_q_loc_profile", "q_loc profile", "MISSING_BUT_SCHEMA_READY", "no source-backed q_loc(r,lambda) row exists, but the required row schema is now explicit", "source/derive profile"),
        ("STATUS2702_1_R10_bound", "R10 bound curve", "MISSING_FULL_CURVE", "anchors exist but live digitized curve is placeholder invalid", "digitize or source full curve"),
        ("STATUS2702_2_testing", "R10 testing", "BLOCKED_INPUTS_EXPLICIT", "operator exists, but both prediction and bound assets are missing for claim", "2703 acquisition path"),
        ("STATUS2702_3_local_GR", "local GR/Newton", "STILL_BLOCKED_BUT_TEST_PATH_CLEARER", "local q_loc residual can be tested once inputs exist", "fill inputs"),
        ("STATUS2702_4_public", "public/GitHub", "NO_ACTION_PRIVATE", "private nonclaim checkpoint only", "keep private"),
    ]
    return [
        {
            "status_id": status_id,
            "topic": topic,
            "status": status,
            "meaning": meaning,
            "next_action": next_action,
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for status_id, topic, status, meaning, next_action in rows
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": "BC2702_0_local_profile_schema",
            "source_csv": str(OUTPUTS["profile_input_schema"]),
            "branch_csv": str(BRANCH_OUTPUTS["local_profile_schema"]),
            "purpose": "local-bound branch receives q_loc R10 profile input schema",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2702_1_local_bound_contract",
            "source_csv": str(OUTPUTS["r10_bound_digitization_contract"]),
            "branch_csv": str(BRANCH_OUTPUTS["local_bound_contract"]),
            "purpose": "local-bound branch receives full bound-curve digitization contract",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2702_2_wep_profile_schema",
            "source_csv": str(OUTPUTS["profile_input_schema"]),
            "branch_csv": str(BRANCH_OUTPUTS["wep_profile_schema"]),
            "purpose": "WEP branch receives q_loc profile schema",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2702_3_source_weight_profile_schema",
            "source_csv": str(OUTPUTS["profile_input_schema"]),
            "branch_csv": str(BRANCH_OUTPUTS["source_weight_profile_schema"]),
            "purpose": "source-weight branch receives q_loc/source-normalization profile schema",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2702_4_rab_next",
            "source_csv": str(OUTPUTS["next_target"]),
            "branch_csv": str(BRANCH_OUTPUTS["rab_next"]),
            "purpose": "RAB queue receives 2703 acquisition target",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    all_sources_exist = all(row["exists"] == "true" for row in source_rows)
    all_needles_found = all(row["missing_needles"] == "" for row in source_rows)

    parse_targets = {key: path for key, path in OUTPUTS.items() if key != "validation"}
    parse_targets.update(BRANCH_OUTPUTS)
    parse_results = {key: parse_csv(path) for key, path in parse_targets.items()}
    all_csv_parse = all(ok and count > 0 for ok, count, _ in parse_results.values())

    profile_audit = rows_by_name["profile_asset_audit"]
    profile_schema = rows_by_name["profile_input_schema"]
    bound_contract = rows_by_name["r10_bound_digitization_contract"]
    queue_rows = rows_by_name["acquisition_queue"]
    claim_gates = rows_by_name["claim_gates"]
    next_targets = rows_by_name["next_target"]

    profile_not_found = any(row["audit_id"] == "PA2702_4_verdict" and row["status"] == "PROFILE_NOT_FOUND_CURRENT_CORPUS" for row in profile_audit)
    profile_schema_ready = any(row["schema_id"] == "QPROF2702_0_required_prediction_row" and "alpha_q(lambda" in row["formula"] for row in profile_schema)
    bound_contract_ready = len(bound_contract) >= 5 and all(row["valid_for_claim"] == "false" for row in bound_contract)
    acquisition_queue_ready = len(queue_rows) >= 4 and all(row["valid_for_claim"] == "false" for row in queue_rows)
    no_claims = all(row["claim_allowed"] == "false" for row in claim_gates)
    next_2703 = any(row["next_id"] == "NEXT2702_0_selected" and "2703-" in row["target_doc"] for row in next_targets)
    no_formalization_outputs = all("formalization-workbench" not in str(path).lower() for path in parse_targets.values())
    no_github_outputs = all(".git" not in str(path).lower() and "github" not in path.name.lower() for path in parse_targets.values())

    checks = [
        ("VAL2702_0_sources_exist", all_sources_exist, "all cited source paths exist"),
        ("VAL2702_1_needles_found", all_needles_found, "all required source needles were found"),
        ("VAL2702_2_csv_parse", all_csv_parse, "all generated CSVs and branch copies parse with at least one row"),
        ("VAL2702_3_profile_not_found", profile_not_found, "profile audit confirms no source-backed q_loc profile exists"),
        ("VAL2702_4_profile_schema_ready", profile_schema_ready, "q_loc R10 profile schema includes alpha_q(lambda) formula"),
        ("VAL2702_5_bound_contract_ready", bound_contract_ready, "full R10 bound-curve digitization contract is staged"),
        ("VAL2702_6_acquisition_queue_ready", acquisition_queue_ready, "profile/bound acquisition queue is explicit"),
        ("VAL2702_7_no_claims", no_claims, "all claim gates keep claim_allowed=false"),
        ("VAL2702_8_next_2703", next_2703, "2703 acquisition target selected"),
        ("VAL2702_9_no_formalization_outputs", no_formalization_outputs, "no output path points into formalization-workbench"),
        ("VAL2702_10_no_github_outputs", no_github_outputs, "no GitHub/public-output path was written"),
    ]

    rows: list[dict[str, Any]] = []
    for check_id, passed, detail in checks:
        rows.append(
            {
                "check_id": check_id,
                "passed": as_bool(passed),
                "detail": detail,
                "timestamp_utc": stamp(),
            }
        )
    for key, (ok, count, message) in parse_results.items():
        rows.append(
            {
                "check_id": f"VAL2702_PARSE_{key}",
                "passed": as_bool(ok and count > 0),
                "detail": f"{message}; rows={count}",
                "timestamp_utc": stamp(),
            }
        )
    overall = all(row["passed"] == "true" for row in rows)
    rows.append(
        {
            "check_id": "VAL2702_OVERALL",
            "passed": as_bool(overall),
            "detail": "2702 confirms no source-backed q_loc R10 profile exists, writes the q_loc profile schema and full R10 bound-curve digitization contract, and selects 2703 acquisition execution",
            "timestamp_utc": stamp(),
        }
    )
    return rows


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    verdict = (
        "2702 confirms the missing input rather than pretending it exists. The corpus has profile templates and one real external PPN ruler, "
        "but no source-backed q_loc radial/range profile usable for alpha_q(lambda). The live R10 bound curve is also still a placeholder. "
        "So this checkpoint writes the exact q_loc R10 profile schema and the full bound-curve digitization contract needed before any honest R10 score."
    )
    text = f"""# 2702: q_loc Radial Profile Or R10 Bound-Curve Digitization Input

**Branch:** `{BRANCH_ID}`

## Private Verdict

{verdict}

## Profile Asset Audit

{markdown_table(rows_by_name["profile_asset_audit"])}

## q_loc R10 Profile Input Schema

{markdown_table(rows_by_name["profile_input_schema"])}

## R10 Bound-Curve Digitization Contract

{markdown_table(rows_by_name["r10_bound_digitization_contract"])}

## Acquisition Queue

{markdown_table(rows_by_name["acquisition_queue"])}

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Claim Gates

{markdown_table(rows_by_name["claim_gates"])}

## Decisions

{markdown_table(rows_by_name["decision_ledger"])}

## Next Target

{markdown_table(rows_by_name["next_target"])}

## Project Status

{markdown_table(rows_by_name["project_status"])}

## Validation

{markdown_table(rows_by_name["validation"])}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    profile_rows = profile_asset_audit_rows()
    schema_rows = profile_input_schema_rows()
    bound_rows = r10_bound_digitization_contract_rows()
    queue_rows = acquisition_queue_rows()
    claim_rows = claim_gate_rows()
    decision_rows = decision_ledger_rows()
    next_rows = next_target_rows()
    status_rows = project_status_rows()
    branch_rows = branch_copy_rows()

    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_rows,
        "profile_asset_audit": profile_rows,
        "profile_input_schema": schema_rows,
        "r10_bound_digitization_contract": bound_rows,
        "acquisition_queue": queue_rows,
        "claim_gates": claim_rows,
        "decision_ledger": decision_rows,
        "next_target": next_rows,
        "project_status": status_rows,
        "branch_copies": branch_rows,
    }

    for key, rows in rows_by_name.items():
        write_csv(OUTPUTS[key], rows)

    write_csv(BRANCH_OUTPUTS["local_profile_schema"], schema_rows)
    write_csv(BRANCH_OUTPUTS["local_bound_contract"], bound_rows)
    write_csv(BRANCH_OUTPUTS["wep_profile_schema"], schema_rows)
    write_csv(BRANCH_OUTPUTS["source_weight_profile_schema"], schema_rows)
    write_csv(BRANCH_OUTPUTS["rab_next"], next_rows)

    validation = validation_rows(rows_by_name)
    rows_by_name["validation"] = validation
    write_csv(OUTPUTS["validation"], validation)
    write_doc(rows_by_name)

    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
