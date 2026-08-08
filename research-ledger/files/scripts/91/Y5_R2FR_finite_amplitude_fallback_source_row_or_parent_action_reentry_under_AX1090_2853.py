from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = PROJECT / "formalization-workbench"

DOC = ROOT / "2853-Y5-R2FR-finite-amplitude-fallback-source-row-or-parent-action-reentry-under-AX1090.md"

SRC_2852_DOC = ROOT / "2852-Y5-R2FR-source-doublet-symmetry-owner-or-closure-demotion-under-AX1090.md"
SRC_2852_FALLBACK = RESIDUALS / "P8_Y5_R2FR_2852_FINITE_AMPLITUDE_FALLBACK_CONTRACT.csv"
SRC_2852_DEMOTION = RESIDUALS / "P8_Y5_R2FR_2852_CLOSURE_DEMOTION_LEDGER.csv"
SRC_2852_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2852_VALIDATION.csv"
SRC_2849_SCHEMA = RESIDUALS / "P8_Y5_R2FR_2849_FINITE_ROW_ACCEPTANCE_SCHEMA.csv"
SRC_2847_MAP = RESIDUALS / "P8_Y5_R2FR_2847_DRY_RUN_BOUND_MAP.csv"
SRC_2846_FORMULA = RESIDUALS / "P8_Y5_R2FR_2846_LOCAL_PPN_FORMULA_PACK_NONCLAIM.csv"
SRC_2844_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2844_PARENT_AMPLITUDE_CONTRACT.csv"
SRC_2844_FLUX = RESIDUALS / "P8_Y5_R2FR_2844_CAB_GREEN_FLUX_IDENTITY.csv"
SRC_2631 = ROOT / "2631-Y5-R2FR-current-branch-no-shadow-full-PPN-vector-or-residual-kernel-fill.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2853_SOURCE_REGISTER.csv",
    "schema": RESIDUALS / "P8_Y5_R2FR_2853_FINITE_AMPLITUDE_INPUT_SCHEMA.csv",
    "candidate": RESIDUALS / "P8_Y5_R2FR_2853_CANDIDATE_INPUT_ROWS.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2853_STRICT_RUNNER_RESULTS.csv",
    "reentry": RESIDUALS / "P8_Y5_R2FR_2853_PARENT_ACTION_REENTRY_HOOK.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2853_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2853_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2853_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2853_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2853_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "candidate_copy": LOCAL_BOUNDS / "RAB_FINITE_AMPLITUDE_CANDIDATE_ROWS_2853_NONCLAIM.csv",
    "runner_copy": SOURCE_WEIGHT / "RAB_FINITE_AMPLITUDE_STRICT_RUNNER_2853_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2853_first_real_amplitude_source_acquisition_NEXT.csv",
    "reentry_copy": BETA_DOCS / "RAB_PARENT_ACTION_REENTRY_HOOK_2853_NONCLAIM.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["score_ready"] = False
    row["valid_prediction_row"] = False
    row["valid_for_claim"] = False
    row["claim_allowed"] = False
    row["generated_utc"] = ts()
    return row


def source_row(source_id: str, path: Path, anchors: str, role: str) -> dict[str, Any]:
    text = read_text(path)
    needles = [anchor for anchor in anchors.split(";") if anchor]
    missing = [anchor for anchor in needles if anchor not in text]
    return nonclaim(
        {
            "source_id": source_id,
            "source_path": str(path),
            "anchors": anchors,
            "role": role,
            "path_exists": path.exists(),
            "anchors_found": not missing,
            "missing_anchors": ";".join(missing),
            "control_only": True,
        }
    )


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2853_0_2852_doc", SRC_2852_DOC, "NEXT2852_0_2853;VAL2852_OVERALL", "2852 handoff to finite amplitude fallback"),
        ("SRC2853_1_2852_fallback", SRC_2852_FALLBACK, "FB2852_0_Q_CAB;FB2852_3_A_total;FB2852_4_GM", "finite amplitude fallback contract"),
        ("SRC2853_2_2852_demotion", SRC_2852_DEMOTION, "DEM2852_1_reject_claim;DEM2852_3_retain_fallback", "shared-current closure demotion"),
        ("SRC2853_3_2852_validation", SRC_2852_VALIDATION, "VAL2852_OVERALL", "2852 validation"),
        ("SRC2853_4_2849_schema", SRC_2849_SCHEMA, "SCH2849_1_value;SCH2849_5_green_convention;SCH2849_8_GM_convention", "strict row acceptance schema"),
        ("SRC2853_5_2847_map", SRC_2847_MAP, "BM2847_0_gamma;BM2847_9_total", "local PPN comparator dry-run map"),
        ("SRC2853_6_2846_formula", SRC_2846_FORMULA, "FORM2846_0_A_total;FORM2846_1_delta_p;FORM2846_4_finite_score_rule", "local PPN amplitude formula pack"),
        ("SRC2853_7_2844_contract", SRC_2844_CONTRACT, "CONTRACT2844_1_source_current;CONTRACT2844_5_sign;CONTRACT2844_6_measured_GM", "parent amplitude contract gaps"),
        ("SRC2853_8_2844_flux", SRC_2844_FLUX, "FLUX2844_5_local_suppression_condition;Q_CAB=-sigma_R*q_R_eff", "symbolic suppression condition remains closure-only"),
        ("SRC2853_9_2631_vector", SRC_2631, "PPNV2631_8_total_abs;RG2631_0_no_gamma_only", "full PPN vector guard"),
    ]
    return [source_row(*spec) for spec in specs]


def schema_rows() -> list[dict[str, Any]]:
    specs = [
        ("FS2853_0_Q_CAB", "Q_CAB_value", "finite real charge or parent-signed theorem-zero row", "numeric_or_theorem", "MISSING_Q_CAB;placeholder;closure-only zero"),
        ("FS2853_1_q_R_eff", "q_R_eff_value", "finite real charge or parent-signed theorem-zero row", "numeric_or_theorem", "MISSING_q_R_eff;placeholder;closure-only zero"),
        ("FS2853_2_sigma_R", "sigma_R_value", "finite nonzero sign or parent operator sign theorem", "numeric_or_theorem", "MISSING_sigma_R;implicit sign"),
        ("FS2853_3_GM", "GM_value", "positive measured source GM or mass convention tied to U=GM/r", "numeric_or_theorem", "MISSING_GM;bare mass;orbital fit as proof"),
        ("FS2853_4_A_total", "A_total_value", "computed only by runner from accepted Q_CAB/q_R_eff/sigma_R", "computed", "user-supplied A_total without inputs;tuned cancellation"),
        ("FS2853_5_delta_p", "delta_p_value", "computed only by runner from A_total and GM", "computed", "computed with missing or nonpositive GM"),
        ("FS2853_6_sources", "source_path/equation_anchor", "every accepted input needs existing local source path and exact anchor", "provenance", "web-only;generic citation;missing file"),
        ("FS2853_7_vector", "full_vector_status", "gamma lane cannot promote local GR without full PPN vector closure", "guard", "gamma-only pass"),
    ]
    return [
        nonclaim(
            {
                "schema_id": schema_id,
                "field": field,
                "acceptance_rule": rule,
                "input_type": input_type,
                "rejection_rule": rejection,
                "control_only": True,
            }
        )
        for schema_id, field, rule, input_type, rejection in specs
    ]


def candidate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "candidate_id": "CAND2853_0_placeholder_current_corpus",
            "branch_id": "R2FR_local_PPN_constant_limit",
            "Q_CAB_value": "MISSING_Q_CAB",
            "q_R_eff_value": "MISSING_q_R_eff",
            "sigma_R_value": "MISSING_sigma_R",
            "GM_value": "MISSING_GM",
            "b_R_value": "MISSING_b_R",
            "tail_status": "MISSING_TAIL_PROFILE",
            "full_vector_status": "MISSING_FULL_VECTOR",
            "Q_CAB_source_path": "",
            "q_R_eff_source_path": "",
            "sigma_R_source_path": "",
            "GM_source_path": "",
            "green_convention": "MISSING_GREEN_CONVENTION",
            "sign_convention": "MISSING_SIGN_CONVENTION",
            "GM_convention": "MISSING_GM_CONVENTION",
            "parent_theorem_zero": False,
            "theorem_zero_authority": "MISSING_PARENT_SIGNATURE",
            "valid_for_claim": False,
        }
    ]
    return [
        nonclaim(
            {
                **row,
                "numeric_value_present": False,
                "control_only": True,
            }
        )
        for row in rows
    ]


def is_missing(value: Any) -> bool:
    if value is None:
        return True
    text = str(value).strip()
    return text == "" or "MISSING" in text.upper() or "PLACEHOLDER" in text.upper()


def parse_float(value: Any) -> float | None:
    if is_missing(value):
        return None
    try:
        parsed = float(str(value))
    except ValueError:
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def candidate_refusal_reasons(row: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    required_numeric = ["Q_CAB_value", "q_R_eff_value", "sigma_R_value", "GM_value"]
    for key in required_numeric:
        if parse_float(row.get(key)) is None:
            reasons.append(f"{key}_NOT_FINITE_NUMERIC")
    for key in ["Q_CAB_source_path", "q_R_eff_source_path", "sigma_R_source_path", "GM_source_path"]:
        source_path = str(row.get(key, "")).strip()
        if not source_path:
            reasons.append(f"{key}_MISSING")
        elif not Path(source_path).exists():
            reasons.append(f"{key}_DOES_NOT_EXIST")
    for key in ["green_convention", "sign_convention", "GM_convention"]:
        if is_missing(row.get(key)):
            reasons.append(f"{key}_MISSING")
    if is_missing(row.get("b_R_value")):
        reasons.append("b_R_MISSING_FOR_GAMMA_COMBO")
    if is_missing(row.get("tail_status")):
        reasons.append("TAIL_PROFILE_MISSING")
    if is_missing(row.get("full_vector_status")):
        reasons.append("FULL_VECTOR_MISSING")
    if row.get("parent_theorem_zero") is True and row.get("theorem_zero_authority") != "PARENT_SIGNED_TRUE":
        reasons.append("THEOREM_ZERO_WITHOUT_PARENT_SIGNATURE")
    return reasons


def runner_rows(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in candidates:
        refusals = candidate_refusal_reasons(row)
        q_cab = parse_float(row.get("Q_CAB_value"))
        q_r_eff = parse_float(row.get("q_R_eff_value"))
        sigma_r = parse_float(row.get("sigma_R_value"))
        gm = parse_float(row.get("GM_value"))
        computed_a_total = ""
        computed_delta_p = ""
        computed_q_r_hat = ""
        if not refusals and q_cab is not None and q_r_eff is not None and sigma_r is not None and gm is not None and gm > 0:
            a_total = (sigma_r * q_r_eff + q_cab) / (4.0 * math.pi)
            computed_a_total = repr(a_total)
            computed_delta_p = "REQUIRES_C_AND_G_UNITS_LOCK"
            computed_q_r_hat = "REQUIRES_C_AND_G_UNITS_LOCK"
        rows.append(
            nonclaim(
                {
                    "runner_id": f"RUN2853_{row['candidate_id']}",
                    "candidate_id": row["candidate_id"],
                    "runner_status": "REFUSED_MISSING_PROVENANCE_OR_INPUTS" if refusals else "COMPUTABLE_BUT_NONCLAIM_UNITS_REVIEW_REQUIRED",
                    "refusal_reasons": ";".join(refusals),
                    "A_total_formula": "A_total=(sigma_R*q_R_eff+Q_CAB)/(4*pi)",
                    "A_total_computed": computed_a_total,
                    "delta_p_formula": "delta_p_const=c^2*A_total/(2*G*M_source)",
                    "delta_p_computed": computed_delta_p,
                    "q_R_hat_formula": "q_R_hat_const=-c^2*A_total/(G*M_source)",
                    "q_R_hat_computed": computed_q_r_hat,
                    "gamma_bound_available": True,
                    "gamma_bound": "2.3e-05",
                    "score_attempted": False,
                    "numeric_prediction_present": False,
                    "control_only": True,
                }
            )
        )
    return rows


def reentry_rows() -> list[dict[str, Any]]:
    specs = [
        ("RE2853_0_parent_source_equation", "If a parent equation supplies L_CAB C_AB and L_R R_delta with a shared source current, route back to theorem mode.", "requires source_path, equation_anchor, operator signs, boundary policy, and no independent rescaling", "OPEN_REENTRY_NOT_ACTIVE"),
        ("RE2853_1_symmetry_owner", "If a symmetry fixes (a_C,a_R)=kappa_star*(-sigma_R,1), replace finite fallback with theorem-zero certificate.", "requires parent-signed object-language/current owner and sigma_R sign", "OPEN_REENTRY_NOT_ACTIVE"),
        ("RE2853_2_GM_glue", "If T509/T510 measured-GM charge glue closes, runner may compute delta_p/q_R_hat in a source-normalized way.", "requires same charge controlling U=GM/r and metric 1/r readout", "OPEN_REENTRY_NOT_ACTIVE"),
        ("RE2853_3_full_vector", "If full PPN vector closes, gamma lane may be interpreted as part of local GR rather than isolated comparator.", "requires beta/preferred/source/endpoint/clock/orbital/q_loc rows", "OPEN_REENTRY_NOT_ACTIVE"),
    ]
    return [
        nonclaim(
            {
                "reentry_id": reentry_id,
                "trigger": trigger,
                "required_evidence": evidence,
                "status": status,
                "control_only": True,
            }
        )
        for reentry_id, trigger, evidence, status in specs
    ]


def claim_gate_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_control = all(row["path_exists"] and row["anchors_found"] for row in rows_by_name["sources"])
    any_runner_score = any(row["score_attempted"] for row in rows_by_name["runner"])
    specs = [
        ("CG2853_0_source_register", "source register valid", "PASS_CONTROL_ONLY" if source_control else "BLOCKED", "control source check only", source_control),
        ("CG2853_1_inputs_accepted", "finite amplitude inputs accepted", "BLOCKED", "candidate row still contains MISSING_* values and source gaps", False),
        ("CG2853_2_runner_scored", "strict runner produced a score", "BLOCKED", "runner refused placeholder row", any_runner_score),
        ("CG2853_3_parent_reentry", "parent-action reentry activated", "BLOCKED", "no new parent source equation/symmetry/GM glue supplied", False),
        ("CG2853_4_local_GR_Newton", "local GR/Newton reduction claimed", "BLOCKED", "full PPN vector and measured-GM bridge remain open", False),
    ]
    return [
        nonclaim(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "status": status,
                "reason": reason,
                "control_check_passed": control_passed,
                "gate_passed": False,
                "control_only": True,
            }
        )
        for gate_id, claim, status, reason, control_passed in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2853_0_runner", "Strict finite-amplitude fallback runner installed.", "CREATED_NONCLAIM", "it refuses placeholders before computing A_total or any PPN score"),
        ("DEC2853_1_current_row", "Current corpus candidate row is rejected.", "REFUSED", "Q_CAB, q_R_eff, sigma_R, GM, b_R, tail and full-vector inputs remain missing"),
        ("DEC2853_2_reentry", "Parent-action reentry hook is preserved.", "OPEN_NOT_ACTIVE", "real source equations or symmetry owners can still supersede the finite fallback"),
        ("DEC2853_3_next", "Next target is first real amplitude source acquisition.", "SELECTED_2854", "the runner exists; now it needs actual sourced rows or a blocker ledger"),
        ("DEC2853_4_no_claim", "No local-GR/Newton/PPN/R10 claim.", "LOCKED", "this checkpoint is infrastructure and refusal, not evidence"),
    ]
    return [
        nonclaim(
            {
                "decision_id": decision_id,
                "decision": decision,
                "result": result,
                "because": because,
                "control_only": True,
            }
        )
        for decision_id, decision, result, because in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2853_0_2854",
                "status": "selected_primary",
                "target_doc": "2854-Y5-R2FR-first-real-amplitude-source-acquisition-or-blocker-ledger-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_first_real_amplitude_source_acquisition_or_blocker_ledger_under_AX1090_2854.py",
                "mission": "try to locate or ingest real source-backed rows for Q_CAB, q_R_eff, sigma_R, b_R, tail, GM and full-vector local channels; if absent, write the blocker ledger without fabricating values",
                "selected": True,
                "control_only": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    copies = [
        ("COPY2853_0_candidate", OUTPUTS["candidate"], BRANCH_OUTPUTS["candidate_copy"], "finite amplitude candidate rows nonclaim copy"),
        ("COPY2853_1_runner", OUTPUTS["runner"], BRANCH_OUTPUTS["runner_copy"], "strict runner results nonclaim copy"),
        ("COPY2853_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue handoff to 2854"),
        ("COPY2853_3_reentry", OUTPUTS["reentry"], BRANCH_OUTPUTS["reentry_copy"], "parent action reentry hook nonclaim copy"),
    ]
    rows = []
    for copy_id, src, dst, purpose in copies:
        shutil.copyfile(src, dst)
        rows.append(nonclaim({"copy_id": copy_id, "source_table": str(src), "copy_path": str(dst), "purpose": purpose, "exists": dst.exists(), "control_only": True}))
    return rows


def iter_cited_paths(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[Path]:
    keys = {"source_path", "copy_path", "source_table"}
    paths: list[Path] = []
    for rows in rows_by_name.values():
        for row in rows:
            for key in keys:
                value = row.get(key)
                if isinstance(value, str) and value:
                    path = Path(value)
                    if path.is_absolute():
                        paths.append(path)
    return paths


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    claim_keys = {
        "valid_for_claim",
        "claim_allowed",
        "score_ready",
        "valid_prediction_row",
        "accepted_ready",
        "numeric_value_present",
        "numeric_prediction_present",
        "score_attempted",
        "gate_passed",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key in claim_keys:
                if key in row and row[key] is True:
                    return False
    return True


def no_numeric_predictions(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    numeric_keys = {"numeric_prediction", "prediction_value", "mts_prediction_value", "delta_p_value", "q_R_hat_value"}
    for rows in rows_by_name.values():
        for row in rows:
            if row.get("numeric_prediction_present") is True:
                return False
            for key in numeric_keys:
                value = row.get(key)
                if value not in (None, "", "MISSING"):
                    return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    start = SCRIPT_START_UTC.timestamp()
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        try:
            if path.stat().st_mtime >= start:
                return False
        except OSError:
            return False
    return True


def under_root(paths: list[Path]) -> bool:
    root_text = str(ROOT.resolve()).lower()
    return all(str(path.resolve()).lower().startswith(root_text) for path in paths)


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_paths = [path for path in OUTPUTS.values() if path != OUTPUTS["validation"]]
    branch_paths = list(BRANCH_OUTPUTS.values())
    cited_paths = iter_cited_paths(rows_by_name)
    checks = [
        ("VAL2853_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2853_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2853_2_candidate_placeholder_refused", all(row["runner_status"].startswith("REFUSED") for row in rows_by_name["runner"]), "strict runner refused the placeholder candidate row"),
        ("VAL2853_3_schema_present", len(rows_by_name["schema"]) >= 8, "finite amplitude input schema is present"),
        ("VAL2853_4_reentry_hook_present", len(rows_by_name["reentry"]) >= 4, "parent-action reentry hook is present"),
        ("VAL2853_5_claim_gates_blocked", not any(row["gate_passed"] for row in rows_by_name["claim_gates"]), "all claim gates remain blocked"),
        ("VAL2853_6_next_target_2854", any(row["next_id"] == "NEXT2853_0_2854" and row["selected"] for row in rows_by_name["next"]), "2854 first real amplitude source acquisition target selected"),
        ("VAL2853_7_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2853_8_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2853_9_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2853_10_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2853_11_no_claim_flags", no_claim_flags(rows_by_name), "no claim/score/prediction flags are true"),
        ("VAL2853_12_no_numeric_predictions", no_numeric_predictions(rows_by_name), "no MTS numeric prediction rows inserted"),
        ("VAL2853_13_generated_under_post_checkpoint", under_root(output_paths + branch_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2853_14_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2853_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [{"validation_id": validation_id, "passed": passed, "detail": detail, "timestamp_utc": ts()} for validation_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2853_OVERALL",
            "passed": overall,
            "detail": "2853 installs a strict finite-amplitude fallback runner, refuses the current placeholder row, preserves parent-action reentry, and selects real amplitude source acquisition for 2854.",
            "timestamp_utc": ts(),
        }
    )
    return rows


def md(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    content = f"""# 2853 - Y5 R2FR Finite Amplitude Fallback Source Row Or Parent Action Reentry Under AX1090

Status: `Y5_R2FR_2853_strict_finite_amplitude_runner_installed_placeholder_refused_nonclaim`

## Private Verdict

2853 installs the finite-amplitude fallback runner and refuses the current corpus row.

The runner accepts no hand-waving:

```text
A_total=(sigma_R*q_R_eff+Q_CAB)/(4*pi)
delta_p_const=c^2*A_total/(2*G*M_source)
q_R_hat_const=-c^2*A_total/(G*M_source)
```

It will not compute or score unless `Q_CAB`, `q_R_eff`, `sigma_R`, `GM`, conventions, source paths, and full-vector guards are present. The current row is therefore rejected, as it should be.

This is useful infrastructure: the moment real amplitude rows exist, they can be routed through the same gate instead of being interpreted by vibes. Parent-action reentry is also preserved, so a future symmetry/source equation can still supersede the finite fallback.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Finite Amplitude Input Schema

{markdown_table(rows["schema"], ["schema_id", "field", "acceptance_rule", "rejection_rule", "valid_for_claim"])}

## Candidate Input Rows

{markdown_table(rows["candidate"], ["candidate_id", "Q_CAB_value", "q_R_eff_value", "sigma_R_value", "GM_value", "green_convention", "valid_for_claim"])}

## Strict Runner Results

{markdown_table(rows["runner"], ["runner_id", "runner_status", "refusal_reasons", "A_total_formula", "score_attempted", "valid_for_claim"])}

## Parent Action Reentry Hook

{markdown_table(rows["reentry"], ["reentry_id", "trigger", "required_evidence", "status", "valid_for_claim"])}

## Claim Gates

{markdown_table(rows["claim_gates"], ["claim_gate_id", "claim", "status", "reason", "gate_passed", "valid_for_claim"])}

## Decision Ledger

{markdown_table(rows["decision"], ["decision_id", "decision", "result", "because", "valid_for_claim"])}

## Next Target

{markdown_table(rows["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(rows["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(rows["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows: dict[str, list[dict[str, Any]]] = {}
    rows["sources"] = source_rows()
    rows["schema"] = schema_rows()
    rows["candidate"] = candidate_rows()
    rows["runner"] = runner_rows(rows["candidate"])
    rows["reentry"] = reentry_rows()
    rows["claim_gates"] = claim_gate_rows(rows)
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "schema", "candidate", "runner", "reentry", "claim_gates", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])
    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2853_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2853_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
