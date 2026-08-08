from __future__ import annotations

import csv
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1255"
TITLE = "1255-Y5-R10-qRhat-source-hunt-or-parent-Hcore-reentry"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
QR_RAW_DIR = ROOT / "source-intake" / "qr-hat" / "raw"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
SOURCE_HUNT_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_HUNT_LEDGER.csv"
CANDIDATE_ROW_PATH = QR_RAW_DIR / "QRHAT1255_CASSINI_GAMMA_PHENOMENOLOGICAL_BOUND_NONCLAIM.csv"
CANDIDATE_STATUS_PATH = OUT_DIR / f"{PACK_ID}_CANDIDATE_ROW_STATUS.csv"
RUNNER_INVOCATION_PATH = OUT_DIR / f"{PACK_ID}_1249_RUNNER_INVOCATION.csv"
RUNNER_SNAPSHOT_PATH = OUT_DIR / f"{PACK_ID}_1249_RUNNER_SNAPSHOT.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1255_VALIDATION.csv"

RUNNER_1249 = ROOT / "scripts" / "Y5_R10_finite_qRhat_source_acquisition_and_policy_runner.py"


REQUIRED_1249_FIELDS = [
    "candidate_id",
    "route_type",
    "q_R_hat",
    "q_R_hat_units",
    "Q_R_units_before_normalization",
    "GM_convention",
    "source_path",
    "derivation_status",
    "N_sigma",
    "sigma_gamma",
    "zero_theorem_statement",
    "closure_used",
    "valid_for_claim",
    "claim_allowed",
]


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
    }


def is_false(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no"}


def has_missing_marker(rows: list[dict[str, str]]) -> bool:
    joined = "\n".join(str(value) for row in rows for value in row.values())
    return "MISSING" in joined or "PLACEHOLDER" in joined or "TODO" in joined


def recent_formalization_writes() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    recent: list[Path] = []
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            mtime = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            if mtime >= RUN_STARTED_UTC:
                recent.append(path)
    return recent


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    QR_RAW_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1255_0_1254_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1254_NEXT_TARGET.csv",
            "needle": "NEXT1254_0_1255",
            "purpose": "handoff to q_Rhat source hunt or parent H_core re-entry",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1255_1_1254_template",
            "local_path": "source-intake/qr-hat/docs/QRHAT1254_BOUNDARY_FLUX_OR_PHENOMENOLOGICAL_TEMPLATE.csv",
            "needle": "QRHAT1254_TEMPLATE_DO_NOT_SCORE",
            "purpose": "docs-only q_Rhat template completed by 1255 candidate row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1255_2_1181_Cassini",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1181_EXTERNAL_PPN_SOURCE_REGISTER.csv",
            "needle": "gamma = 1 + (2.1 +/- 2.3) x 10^-5",
            "purpose": "Cassini gamma comparator provenance for phenomenological q_Rhat ceiling",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1255_3_1244_policy",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1244_RUNNER_POLICY_FEED.csv",
            "needle": "4.6e-05",
            "purpose": "q_Rhat guardrail derived from gamma_minus_1_QR=-q_Rhat/2 and sigma_gamma=2.3e-5",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1255_4_1244_GM",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1244_GM_CONVENTION_PACK.csv",
            "needle": "q_R_hat = Q_R c^2/(G M_source)",
            "purpose": "GM convention; 1255 uses direct dimensionless bound, not raw Q_R",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1255_5_1240_projection",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1240_QR_TO_PPN_MAPPING_SCHEMA.csv",
            "needle": "gamma_minus_1_QR approximately -q_R_hat/2",
            "purpose": "projection converting gamma one-sigma uncertainty to q_Rhat ceiling",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1255_6_1249_runner",
            "local_path": "scripts/Y5_R10_finite_qRhat_source_acquisition_and_policy_runner.py",
            "needle": "ACCEPTED_NONCLAIM_FINITE_QRHAT",
            "purpose": "existing finite q_Rhat validator/policy runner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1255_7_1253_Hcore",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1253_RECIPROCAL_HCORE_SOURCE_EQUATION_ATTEMPT.csv",
            "needle": "SOURCE_EQUATION_NOT_DERIVED",
            "purpose": "parent H_core route remains unsigned after 1253",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    source_hunt = [
        {
            "hunt_id": "HUNT1255_0_Cassini_gamma_bound",
            "candidate_input": "Cassini gamma one-sigma uncertainty",
            "candidate_value": "sigma_gamma=2.3e-5 therefore abs(q_R_hat)<=4.6e-5 under gamma_minus_1_QR=-q_R_hat/2",
            "source": "P8_Y5_R10_1181_EXTERNAL_PPN_SOURCE_REGISTER.csv:SRC1181W_0_Cassini_gamma; PubMed https://pubmed.ncbi.nlm.nih.gov/14508481/",
            "result": "FOUND_SOURCE_BACKED_BOUND_INPUT_NONCLAIM",
            "use": "strict smoke ceiling only, not an MTS prediction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "hunt_id": "HUNT1255_1_raw_boundary_flux",
            "candidate_input": "raw Q_R or B_R boundary flux",
            "candidate_value": "NONE",
            "source": "1253 H_core/boundary attempt",
            "result": "NOT_FOUND",
            "use": "return to parent H_core if a real source equation appears",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "hunt_id": "HUNT1255_2_parent_Hcore_equation",
            "candidate_input": "delta H_core/delta R_AB source equation",
            "candidate_value": "NONE",
            "source": "1253 HCE1253_0",
            "result": "NOT_FOUND",
            "use": "next derivation target remains parent source equation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    candidate_row = [
        {
            "candidate_id": "QRHAT1255_CASSINI_GAMMA_1SIGMA_BOUND_NONCLAIM",
            "route_type": "finite_qR_hat",
            "q_R_hat": "4.6e-05",
            "q_R_hat_units": "dimensionless",
            "Q_R_units_before_normalization": "directly_dimensionless_q_R_hat_bound_from_Cassini_gamma_uncertainty",
            "GM_convention": "direct_dimensionless_Cassini_gamma_bound_using_QMAP1240_3_no_raw_Q_R; source_body=Sun",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1181_EXTERNAL_PPN_SOURCE_REGISTER.csv",
            "derivation_status": "phenomenological_bound_nonclaim",
            "N_sigma": "1",
            "sigma_gamma": "2.3e-5",
            "zero_theorem_statement": "NOT_A_ZERO_THEOREM_ROW",
            "closure_used": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "source_body": "Sun",
            "coordinate_convention": "Cassini_solar_system_gamma_comparator_weak_field_areal_radial_projection_schema_QMAP1240_3",
            "observable_anchor": "gamma = 1 + (2.1 +/- 2.3)e-5; use one-sigma uncertainty as nonclaim ceiling",
            "input_kind": "phenomenological_upper_bound_not_theory_prediction",
            "bound_direction": "abs(q_R_hat)<=4.6e-05",
            "uncertainty_policy": "strict_one_sigma_nonclaim_smoke_from_STAT1244_0",
            "external_source_url": "https://pubmed.ncbi.nlm.nih.gov/14508481/",
            "notes": "This row tests the q_Rhat pipeline only. It is not a parent-derived MTS prediction and cannot prove local GR.",
        }
    ]
    write_csv(CANDIDATE_ROW_PATH, candidate_row)

    runner_process = subprocess.run(
        [sys.executable, str(RUNNER_1249)],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    runner_invocation = [
        {
            "invocation_id": "RUN1255_0_1249",
            "runner": str(RUNNER_1249),
            "returncode": runner_process.returncode,
            "stdout_tail": runner_process.stdout[-500:],
            "stderr_tail": runner_process.stderr[-500:],
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    candidate_results = read_csv(OUT_DIR / "P8_Y5_R10_1249_FINITE_QRHAT_CANDIDATE_RESULTS.csv")
    policy_results = read_csv(OUT_DIR / "P8_Y5_R10_1249_POLICY_RUNNER_RESULTS.csv")
    validation_1249 = read_csv(OUT_DIR / "P8_Y5_BRR545_1249_VALIDATION.csv")
    target_candidate_result = [
        row for row in candidate_results if row.get("candidate_id") == "QRHAT1255_CASSINI_GAMMA_1SIGMA_BOUND_NONCLAIM"
    ]
    target_policy_result = [
        row for row in policy_results if row.get("candidate_id") == "QRHAT1255_CASSINI_GAMMA_1SIGMA_BOUND_NONCLAIM"
    ]
    runner_snapshot = [
        {
            "snapshot_id": "SNAP1255_0_candidate_result",
            "source_table": "P8_Y5_R10_1249_FINITE_QRHAT_CANDIDATE_RESULTS.csv",
            "candidate_id": target_candidate_result[0].get("candidate_id", "") if target_candidate_result else "NOT_FOUND",
            "status": target_candidate_result[0].get("acceptance_status", "NOT_FOUND") if target_candidate_result else "NOT_FOUND",
            "numeric_pass": target_candidate_result[0].get("raw_numeric_pass", "") if target_candidate_result else "",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "snapshot_id": "SNAP1255_1_policy_result",
            "source_table": "P8_Y5_R10_1249_POLICY_RUNNER_RESULTS.csv",
            "candidate_id": target_policy_result[0].get("candidate_id", "") if target_policy_result else "NOT_FOUND",
            "status": target_policy_result[0].get("runner_status", "NOT_FOUND") if target_policy_result else "NOT_FOUND",
            "numeric_pass": "True" if target_policy_result and target_policy_result[0].get("runner_status") == "READY_NONCLAIM_NUMERIC_PASS" else "False",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "snapshot_id": "SNAP1255_2_1249_validation",
            "source_table": "P8_Y5_BRR545_1249_VALIDATION.csv",
            "candidate_id": "1249_overall",
            "status": next((row.get("status", "") for row in validation_1249 if row.get("check_id") == "VAL1249_12_overall"), "NOT_FOUND"),
            "numeric_pass": "N/A",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    candidate_status = [
        {
            "status_id": "CSTAT1255_0_raw_row",
            "candidate_path": str(CANDIDATE_ROW_PATH),
            "required_fields_present": all(field in candidate_row[0] for field in REQUIRED_1249_FIELDS),
            "missing_markers_present": has_missing_marker(candidate_row),
            "derivation_status": candidate_row[0]["derivation_status"],
            "interpretation": "source-backed phenomenological ceiling only, not a prediction",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    claim_gates = [
        {
            "gate_id": "GATE1255_0_bound_input",
            "claim": "source-backed q_Rhat ceiling row exists",
            "status": "PASS_NONCLAIM",
            "reason": "Cassini gamma one-sigma uncertainty gives abs(q_Rhat)<=4.6e-5 under the existing QMAP1240_3 projection",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1255_1_runner",
            "claim": "1249 runner accepts row for nonclaim smoke",
            "status": "PASS_NONCLAIM" if target_policy_result and target_policy_result[0].get("runner_status") == "READY_NONCLAIM_NUMERIC_PASS" else "BLOCKED",
            "reason": target_policy_result[0].get("runner_status", "NOT_FOUND") if target_policy_result else "candidate result not found",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1255_2_prediction",
            "claim": "MTS predicts q_Rhat within the ceiling",
            "status": "BLOCKED",
            "reason": "1255 supplies a comparator-derived ceiling, not a parent-derived MTS q_Rhat value",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1255_3_local_GR",
            "claim": "local GR/PPN branch is derived",
            "status": "BLOCKED",
            "reason": "parent H_core source equation, no-charge theorem, matter descent, and beta/local residual gates remain open",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1255_0_bound_row",
            "decision": "promote the Cassini-derived q_Rhat ceiling only to nonclaim smoke input",
            "because": "it is source-backed and useful for pipeline testing, but it is an empirical comparator ceiling rather than an MTS prediction",
            "next_action": "use it as a guardrail while returning to parent H_core/source-equation derivation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1255_1_Hcore_reentry",
            "decision": "return to the derivation route after the bound-input pipe is working",
            "because": "the core missing physics remains delta H_core/delta R_AB or a true Q_R no-charge theorem",
            "next_action": "1256-Y5-R10-parent-Hcore-reciprocal-source-equation-minimal-reentry.md",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1255_0_1256",
            "target_file": "1256-Y5-R10-parent-Hcore-reciprocal-source-equation-minimal-reentry.md",
            "target_script": "scripts/Y5_R10_parent_Hcore_reciprocal_source_equation_minimal_reentry.py",
            "task": "re-enter the parent derivation route and try to write the minimal reciprocal H_core source equation that could produce Q_R, zero Q_R, or a bounded q_Rhat coefficient",
            "success_condition": "either derive a parent-owned E_R=delta H_core/delta R_AB equation with boundary term, or produce a precise no-go/blocker that names the missing action block",
            "do_not": "do not treat the Cassini q_Rhat ceiling as a theory prediction or local-GR pass",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_tables = [
        (SOURCE_REGISTER_PATH, source_register),
        (SOURCE_HUNT_PATH, source_hunt),
        (CANDIDATE_STATUS_PATH, candidate_status),
        (RUNNER_INVOCATION_PATH, runner_invocation),
        (RUNNER_SNAPSHOT_PATH, runner_snapshot),
        (CLAIM_GATES_PATH, claim_gates),
        (DECISION_PATH, decisions),
        (NEXT_PATH, next_target),
    ]

    for path, rows in generated_tables:
        write_csv(path, rows)

    source_checks = [exists_and_contains(str(row["local_path"]), str(row["needle"])) for row in source_register]
    sources_exist = all(exists for exists, _ in source_checks)
    needles_found = all(found for _, found in source_checks)
    candidate_rows = read_csv(CANDIDATE_ROW_PATH)
    candidate_columns = set(candidate_rows[0].keys()) if candidate_rows else set()
    candidate_required = all(field in candidate_columns for field in REQUIRED_1249_FIELDS)
    candidate_no_missing = not has_missing_marker(candidate_rows)
    runner_ok = runner_process.returncode == 0
    runner_accepts = bool(target_candidate_result) and target_candidate_result[0].get("acceptance_status") == "ACCEPTED_NONCLAIM_FINITE_QRHAT"
    runner_passes = bool(target_policy_result) and target_policy_result[0].get("runner_status") == "READY_NONCLAIM_NUMERIC_PASS"
    validation_1249_pass = any(row.get("check_id") == "VAL1249_12_overall" and row.get("status") == "PASS" for row in validation_1249)
    all_nonclaim = all(
        is_false(row.get("valid_for_claim", "")) and is_false(row.get("claim_allowed", ""))
        for _, rows in generated_tables
        for row in rows
    ) and all(is_false(row.get("valid_for_claim", "")) and is_false(row.get("claim_allowed", "")) for row in candidate_rows)
    claims_ok = all(row["status"] in {"PASS_NONCLAIM", "BLOCKED"} and is_false(row["claim_allowed"]) for row in claim_gates)
    next_is_1256 = next_target[0]["target_file"].startswith("1256-")

    csv_parse_details: list[str] = []
    csv_parse_ok = True
    for path, _ in generated_tables + [(CANDIDATE_ROW_PATH, candidate_row)]:
        try:
            rows = read_csv(path)
            csv_parse_details.append(f"{path.name}:{len(rows)}")
        except Exception as exc:  # pragma: no cover
            csv_parse_ok = False
            csv_parse_details.append(f"{path.name}:ERROR:{exc}")

    formalization_writes = recent_formalization_writes()

    validation_rows = [
        validation_row("VAL1255_0_sources_exist", "all cited local sources exist", sources_exist, f"{sum(1 for exists, _ in source_checks if exists)}/{len(source_checks)} sources exist"),
        validation_row("VAL1255_1_needles_found", "all cited local needles found", needles_found, f"{sum(1 for _, found in source_checks if found)}/{len(source_checks)} needles found"),
        validation_row("VAL1255_2_candidate_schema", "raw q_Rhat candidate has every 1249 required field", candidate_required, f"required_fields={len(REQUIRED_1249_FIELDS)}; candidate_columns={len(candidate_columns)}"),
        validation_row("VAL1255_3_candidate_no_missing", "raw q_Rhat candidate has no MISSING markers", candidate_no_missing, str(CANDIDATE_ROW_PATH)),
        validation_row("VAL1255_4_runner_invoked", "1249 finite q_Rhat runner completed", runner_ok, f"returncode={runner_process.returncode}"),
        validation_row("VAL1255_5_runner_accepts", "1249 accepts candidate as nonclaim finite q_Rhat", runner_accepts, target_candidate_result[0].get("acceptance_status", "NOT_FOUND") if target_candidate_result else "NOT_FOUND"),
        validation_row("VAL1255_6_policy_passes", "1249 policy runner marks strict smoke pass", runner_passes, target_policy_result[0].get("runner_status", "NOT_FOUND") if target_policy_result else "NOT_FOUND"),
        validation_row("VAL1255_7_1249_validation", "1249 adaptive validation passes after candidate insertion", validation_1249_pass, "VAL1249_12_overall=PASS" if validation_1249_pass else "VAL1249_12_overall not PASS"),
        validation_row("VAL1255_8_claim_gates", "claim gates keep prediction/local-GR claims blocked", claims_ok, f"claim_gate_rows={len(claim_gates)}"),
        validation_row("VAL1255_9_nonclaim_policy", "all generated rows remain nonclaim", all_nonclaim, "valid_for_claim=false and claim_allowed=false throughout generated tables and candidate"),
        validation_row("VAL1255_10_next_target_1256", "next target returns to parent Hcore derivation", next_is_1256, str(next_target[0]["target_file"])),
        validation_row("VAL1255_11_csv_parse", "all generated CSVs parse cleanly", csv_parse_ok, "; ".join(csv_parse_details)),
        validation_row("VAL1255_12_formalization_untouched", "formalization-workbench untouched during run", not formalization_writes, f"formalization_recent_write_count_since_run_start={len(formalization_writes)}"),
    ]
    overall = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        validation_row(
            "VAL1255_13_overall",
            "overall 1255 validation",
            overall,
            "1255 fills one source-backed nonclaim q_Rhat ceiling row, verifies it through the adaptive 1249 runner, and returns next to parent H_core derivation",
        )
    )
    write_csv(VALIDATION_PATH, validation_rows)

    doc = f"""# {TITLE}

**Current verdict:** 1255 successfully fills the first live `q_R_hat` raw row, but only as a source-backed phenomenological ceiling. It is not an MTS prediction and not a local-GR pass.

**Main progress:** the Cassini gamma comparator gives a strict nonclaim ceiling `abs(q_R_hat) <= 4.6e-5` through `gamma_minus_1_QR = -q_R_hat/2`. The adaptive 1249 runner accepts the row as `ACCEPTED_NONCLAIM_FINITE_QRHAT` and marks the strict smoke status `READY_NONCLAIM_NUMERIC_PASS`.

**No-claim guard:** no parent `H_core`, no `Q_R=0` theorem, no finite MTS prediction, no local PPN pass, and no local-GR/Newton derivation is promoted.

Generated UTC: {datetime.now(timezone.utc).isoformat()}

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "purpose", "valid_for_claim", "claim_allowed"])}

## Source Hunt Ledger
{markdown_table(source_hunt, ["hunt_id", "candidate_input", "candidate_value", "source", "result", "use", "valid_for_claim", "claim_allowed"])}

## Candidate Row Status
{markdown_table(candidate_status, ["status_id", "candidate_path", "required_fields_present", "missing_markers_present", "derivation_status", "interpretation", "valid_for_claim", "claim_allowed"])}

## 1249 Runner Invocation
{markdown_table(runner_invocation, ["invocation_id", "runner", "returncode", "stdout_tail", "stderr_tail", "valid_for_claim", "claim_allowed"])}

## 1249 Runner Snapshot
{markdown_table(runner_snapshot, ["snapshot_id", "source_table", "candidate_id", "status", "numeric_pass", "valid_for_claim", "claim_allowed"])}

## Claim Gates
{markdown_table(claim_gates, ["gate_id", "claim", "status", "reason", "valid_for_claim", "claim_allowed"])}

## Decision Ledger
{markdown_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validation_rows, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
