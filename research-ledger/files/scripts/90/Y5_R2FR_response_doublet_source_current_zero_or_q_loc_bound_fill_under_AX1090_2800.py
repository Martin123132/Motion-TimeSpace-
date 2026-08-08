from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_STARTED_UTC = datetime.now(timezone.utc)
ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
WORK = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
MTS = WORK / "source-intake" / "mts_residuals"
RAB_QUEUE = WORK / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = WORK / "source-intake" / "beta-source" / "docs"
MICROSCOPE_DIR = WORK / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SCRIPTS = WORK / "scripts"
DOC = WORK / "2800-Y5-R2FR-response-doublet-source-current-zero-or-q_loc-bound-fill-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2800_SOURCE_REGISTER.csv",
    "theorem": MTS / "P8_Y5_R2FR_2800_RESPONSE_DOUBLET_THEOREM_ATTEMPT.csv",
    "bound_fill": MTS / "P8_Y5_R2FR_2800_QLOC_BOUND_FILL_ROWS.csv",
    "bound_runner": MTS / "P8_Y5_R2FR_2800_QLOC_BOUND_RUNNER.csv",
    "even_debt": MTS / "P8_Y5_R2FR_2800_EVEN_DEBT_LEDGER.csv",
    "product_candidate": MTS / "P8_Y5_R2FR_2800_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv",
    "product_runner": MTS / "P8_Y5_R2FR_2800_PRODUCT_RUNNER_STATUS.csv",
    "comparisons": MTS / "P8_Y5_R2FR_2800_PRODUCT_COMPARISON_ROWS.csv",
    "gates": MTS / "P8_Y5_R2FR_2800_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2800_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2800_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2800_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2800_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "theorem_queue": RAB_QUEUE / "JR2800_RESPONSE_DOUBLET_THEOREM_ATTEMPT_NONCLAIM.csv",
    "bound_queue": RAB_QUEUE / "JR2800_QLOC_BOUND_FILL_ROWS_NONCLAIM.csv",
    "even_debt_queue": RAB_QUEUE / "JR2800_EVEN_DEBT_LEDGER_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "RESPONSE_DOUBLET_QLOC_BOUND_2800_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_response_doublet_qloc_bound_2800_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2800_QLOC_OBSERVABLE_MAP_OR_FIRST_NUMERIC_BOUND_NEXT.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except csv.Error:
        return False


def source_entries() -> list[tuple[str, Path, str]]:
    return [
        ("2799_next", MTS / "P8_Y5_R2FR_2799_NEXT_TARGET.csv", "authoritative 2800 target"),
        ("2799_residual", MTS / "P8_Y5_R2FR_2799_QLOC_RESIDUAL_RETENTION_LEDGER.csv", "retained q_loc residual"),
        ("2799_bound_interface", MTS / "P8_Y5_R2FR_2799_QLOC_BOUND_INTERFACE_ROLLED_FORWARD.csv", "rolled-forward bound interface"),
        ("1011_theorem_analogue", MTS / "P8_Y5_R10_1011_RESPONSED_DOUBLET_THEOREM_ATTEMPT.csv", "R10 response-doublet theorem analogue"),
        ("1011_bound_analogue", MTS / "P8_Y5_R10_1011_QLOC_BOUND_FILL_ROWS.csv", "R10 q_loc bound-fill analogue"),
        ("1011_runner_analogue", MTS / "P8_Y5_R10_1011_QLOC_BOUND_RUNNER.csv", "R10 q_loc runner analogue"),
        ("2728_JX_audit", MTS / "P8_Y5_R2FR_2728_JX_ZERO_COMPONENT_AUDIT.csv", "R2FR J_X component audit"),
        ("2729_memory_signature", MTS / "P8_Y5_R2FR_2729_PARENT_MEMORY_SIGNATURE_CONTRACT.csv", "R2FR memory signature contract"),
        ("2733_bound_interface", MTS / "P8_Y5_R2FR_2733_QLOC_RESIDUAL_BOUND_INTERFACE.csv", "R2FR q_loc bound interface"),
    ]


def build_sources() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "role": role,
            "contains_text": bool(read_text(path).strip()) if path.exists() else False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for source_id, path, role in source_entries()
    ]


def build_theorem_rows() -> list[dict[str, Any]]:
    rows = [
        ("RDT2800_0_parent_doublets", "R_+^A,R_-^A exist for every physical local residual channel", "Z^A=(R_+^A-R_-^A)/2 and R_even^A=(R_+^A+R_-^A)/2", "R2FR response/memory rows are contracts, not species/channel complete parent doublets", "NOT_DERIVED"),
        ("RDT2800_1_exchange_symmetry", "exchange is exact parent symmetry", "E: R_+^A <-> R_-^A forbids linear Z source terms", "exchange exactness is only conditional and does not own all source/readout channels", "CONDITIONAL_TEMPLATE"),
        ("RDT2800_2_even_matter_readout", "matter/clocks/source measures couple only to even quotient variables", "S_matter=S_matter[Psi,e_obs(R_even)] and delta_Z S_matter=0", "MOMS/source-normalization rows show even channels can remain nonzero", "NOT_DERIVED_HARD_FOR_Y5"),
        ("RDT2800_3_source_current_zero", "J_Z=0 on compact local branch", "Euler: L_AB Z^B = J_A + boundary/source terms; J_A=0", "2728 total J_X verdict remains JX_ZERO_NOT_PROVED", "FAIL_CURRENT_CLAIM"),
        ("RDT2800_4_boundary_zero", "B_Z=0/no odd boundary charge", "boundary/source work vanishes in local compact collar", "2729 boundary/domain clauses remain unsigned", "CONDITIONAL_NOT_CLOSED"),
        ("RDT2800_5_positive_operator", "L_AB positive after gauge/constraint removal", "int Z^A L_AB Z^B = boundary_flux + source_work", "positive theorem cannot activate without J_Z=B_Z=0", "FORMAL_CANDIDATE_ONLY"),
        ("RDT2800_6_PPN_WEP_lock", "Z^A equals physical q_loc/PPN/WEP/source-normalization residual vector", "Z^A maps to beta/gamma/alpha_i/xi/WEP/source-normalization order", "2799 keeps q_loc observable projection missing", "NOT_DERIVED"),
        ("RDT2800_7_verdict", "response-doublet source-current/boundary zero theorem", "RDT2800_0 through RDT2800_6 all parent-signed", "formal double-zero survives, but Y5 even debt, source-current zero, boundary terms, and PPN/WEP lock block promotion", "FAIL_CURRENT_CLAIM"),
    ]
    return [
        {
            "clause_id": row[0],
            "claim_piece": row[1],
            "mathematical_form": row[2],
            "current_evidence": row[3],
            "status": row[4],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_bound_rows() -> list[dict[str, Any]]:
    rows = [
        ("QBF2800_0_compact_shell_budget", "max |P_loc d_rel J_rel| or equivalent q_loc leakage", "7.432631961576971e-06", "dimensionless_proxy", "requires mapping into PPN/WEP/source-normalization units", "P8_Y5_R2FR_2733_QLOC_RESIDUAL_BOUND_INTERFACE.csv", "anchor_proxy_not_claim_curve"),
        ("QBF2800_1_alpha3_pressure", "alpha3-equivalent q_loc channel", "MISSING_QLOC_TO_ALPHA3_COEFFICIENT", "dimensionless", "abs(alpha3) <= official bound only after map exists", "P8_Y5_R2FR_2799_QLOC_BOUND_INTERFACE_ROLLED_FORWARD.csv", "mapping_missing"),
        ("QBF2800_2_WEP_eta_channel", "WEP eta-equivalent q_loc channel", "MISSING_QLOC_TO_ETA_COEFFICIENT", "dimensionless", "MICROSCOPE-like eta only after source/readout projection exists", "P8_Y5_R2FR_2799_QLOC_BOUND_INTERFACE_ROLLED_FORWARD.csv", "WEP_mapping_missing"),
        ("QBF2800_3_Gdot_GMdot", "dln_mu_obs_dt or dln_Meff_dt", "MISSING_TIME_COMPONENT_AND_UNITS", "yr^-1", "use Gdot/source-normalization ledgers after time component is derived", "P8_Y5_R2FR_2799_QLOC_BOUND_INTERFACE_ROLLED_FORWARD.csv", "time_projection_missing"),
        ("QBF2800_4_PPN_metric_tail", "Delta_PPN from q_loc", "MISSING_WEAK_FIELD_METRIC_SOLUTION", "dimensionless_vector", "gamma,beta,alpha_i,xi local gates", "P8_Y5_R2FR_2733_QLOC_RESIDUAL_BOUND_INTERFACE.csv", "PPN_mapping_missing"),
        ("QBF2800_5_R11_operator", "c_GK_operator_vector", "MISSING_OPERATOR_VECTOR", "operator_family_units_required", "R11/non-EH operator ledgers", "P8_Y5_R2FR_2798_UNCERTIFIED_SECTOR_RESIDUAL_MAP.csv", "operator_vector_missing"),
        ("QBF2800_6_Y5_source_normalization", "c_domain_source_normalization_operator or measured-GM residual", "MISSING_Y5_OWNER_OR_NUMERIC_COEFFICIENT", "dimensionless_or_operator_units", "source-normalized Newton/R11 gate", "P8_Y5_R2FR_2728_JX_ZERO_COMPONENT_AUDIT.csv", "Y5_hard_fail_current"),
        ("QBF2800_7_Y6_extra_stress", "T_extra residual vector", "MISSING_Y6_STRESS_BOUND", "stress_or_PPN_units_required", "extra stress topological/invisible or PPN bounded", "P8_Y5_R2FR_2729_PARENT_MEMORY_SIGNATURE_CONTRACT.csv", "retained_debt"),
    ]
    return [
        {
            "bound_id": row[0],
            "quantity": row[1],
            "candidate_value": row[2],
            "units": row[3],
            "bound_or_gate": row[4],
            "source_path": row[5],
            "status": row[6],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_bound_runner_rows(bound_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for index, row in enumerate(bound_rows):
        score_ready = row["bound_id"] == "QBF2800_0_compact_shell_budget"
        rows.append(
            {
                "runner_id": f"QBR2800_{index}",
                "bound_id": row["bound_id"],
                "quantity": row["quantity"],
                "verdict": "RETAINED_NONCLAIM_QLOC_BOUND_ROW",
                "score_ready": score_ready,
                "claim_allowed": False,
                "failure_reasons": "VALID_FOR_CLAIM_FALSE" if score_ready else f"MISSING_NUMERIC_OR_THEOREM_ZERO_VALUE;{row['status'].upper()}_BLOCKS_CLAIM;VALID_FOR_CLAIM_FALSE",
                "valid_for_claim": False,
                "generated_utc": utc_now(),
            }
        )
    return rows


def build_even_debt_rows() -> list[dict[str, Any]]:
    rows = [
        ("EVEN2800_0_Y5_source_normalization", "source-normalization / measured-GM channel", "exchange-even channel can survive odd-doublet symmetry", "hard_fail_current", "derive source equality or bound coefficient"),
        ("EVEN2800_1_Y6_extra_stress", "extra stress/topological sector", "conserved nonzero extra stress can survive doublet symmetry", "retained_debt", "prove invisible/topological or bound PPN stress vector"),
        ("EVEN2800_2_matter_readout", "ordinary matter/readout coupling", "even readout can be universal but still nonzero", "MOMS_parent_object_unsigned", "derive MOMS/current-owner or keep finite WEP/DD rows"),
    ]
    return [
        {
            "debt_id": row[0],
            "even_channel": row[1],
            "why_doublet_does_not_kill_it": row[2],
            "status": row[3],
            "repair_path": row[4],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_product_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "prediction_id": "WEP2800_0_no_claim_product",
            "observable": "local WEP/PPN/source response from q_loc",
            "prediction_status": "NO_NUMERIC_PREDICTION",
            "claim_blocker": "response-doublet zero theorem fails and bound rows are nonclaim templates/proxies",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def build_product_runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN2800_0_refuse_q_loc_bound_claim",
            "valid_prediction_rows": 0,
            "claim_allowed": False,
            "expected_result": "RUNNER_REFUSES_WEP_LOCAL_GR_CLAIM",
            "reason": "q_loc bound rows lack mappings/units/source-backed coefficients",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def build_comparison_rows() -> list[dict[str, Any]]:
    return [
        {
            "comparison_id": "CMP2800_0_no_numeric_local_response",
            "baseline": "local-GR/WEP/PPN compatibility",
            "prediction": "MTS q_loc response-doublet residual",
            "comparison_status": "NOT_RUN_NUMERICALLY",
            "reason": "q_loc bound rows are templates/proxies without observable maps",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def build_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2800_0_response_doublet_zero", "response-doublet source-current/boundary zero theorem passes", False, False, "Y5/Y6, PPN/WEP lock, and boundary source terms remain unsigned"),
        ("CG2800_1_Y5_source_normalization", "source-normalization even scalar is zero by exchange symmetry", False, False, "Y5 is exchange-even and hard-fail current"),
        ("CG2800_2_Y6_extra_stress", "extra stress is invisible/topological by doublet symmetry", False, False, "Y6 can be conserved and nonzero"),
        ("CG2800_3_q_loc_bound_claim", "q_loc residual bounds are claim-ready", False, False, "bound rows are templates/proxies without coefficient mappings"),
        ("CG2800_4_local_GR_reopen", "local-GR/WEP/PPN gates can reopen", False, False, "q_loc and source-normalization remain retained residuals"),
        ("CG2800_5_bound_branch_ready", "q_loc bound branch is staged as nonclaim", True, False, "bound rows exist but do not claim pass"),
        ("CG2800_6_guardrail", "response-doublet proof-or-bound guardrail is installed", True, False, "zero theorem is not promoted and bound rows stay nonclaim"),
    ]
    return [
        {
            "gate_id": row[0],
            "claim": row[1],
            "gate_pass": row[2],
            "claim_allowed": row[3],
            "reason": row[4],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2800_0_theorem_not_promoted", "response-doublet theorem is not promoted", "odd exchange symmetry does not kill even Y5/Y6/source-normalization debts", "keep q_loc residual explicit"),
        ("DEC2800_1_bound_rows_staged", "q_loc bound-fill rows are staged but nonclaim", "only compact-shell proxy has a value and it lacks observable mapping", "fill q_loc-to-observable maps next"),
        ("DEC2800_2_best_next", "next attack is observable map or first numeric bound", "without K_PPN/K_WEP/K_clock/K_orbital/source-normalization maps, no residual can be compared", "build q_loc observable projection coefficients"),
    ]
    return [
        {
            "decision_id": row[0],
            "decision": row[1],
            "because": row[2],
            "next_action": row[3],
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for row in rows
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2800_0_2801",
            "next_target": "2801-Y5-R2FR-q_loc-observable-map-or-first-numeric-bound-row-under-AX1090.md",
            "script": "scripts/Y5_R2FR_q_loc_observable_map_or_first_numeric_bound_row_under_AX1090_2801.py",
            "objective": "build q_loc observable projection maps for PPN/WEP/clock/orbital/source-normalization, or fill the first numeric bound row with units and source-backed coefficients",
            "include": "K_PPN; K_WEP; K_clock; K_orbital; K_source; alpha3/eta/Gdot mappings; q_loc units; source paths; no-cancellation policy",
            "exclude": "claiming bound pass from proxy row; fitted cancellation; measured-G absorption; local-GR/WEP claim; GitHub; formalization edits",
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
    ]


def copy_branches() -> list[dict[str, Any]]:
    copy_plan = [
        (OUTPUTS["theorem"], BRANCH_OUTPUTS["theorem_queue"], "theorem_queue"),
        (OUTPUTS["bound_fill"], BRANCH_OUTPUTS["bound_queue"], "bound_queue"),
        (OUTPUTS["even_debt"], BRANCH_OUTPUTS["even_debt_queue"], "even_debt_queue"),
        (OUTPUTS["theorem"], BRANCH_OUTPUTS["beta_doc"], "beta_doc"),
        (OUTPUTS["gates"], BRANCH_OUTPUTS["microscope_copy"], "microscope_copy"),
        (OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next_queue"),
    ]
    rows = []
    for source, destination, label in copy_plan:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append({"copy_id": f"BC2800_{label}", "source": str(source), "destination": str(destination), "exists": destination.exists(), "valid_for_claim": False, "generated_utc": utc_now()})
    return rows


def formalization_untouched_since_run() -> bool:
    if not FORMALIZATION.exists():
        return True
    threshold = RUN_STARTED_UTC.timestamp()
    return not any(path.is_file() and path.stat().st_mtime >= threshold for path in FORMALIZATION.rglob("*"))


def claim_flags_true(sections: dict[str, list[dict[str, Any]]]) -> bool:
    for key, rows in sections.items():
        if key == "validation":
            continue
        for row in rows:
            if str(row.get("valid_for_claim", "false")).lower() == "true":
                return True
            if str(row.get("claim_allowed", "false")).lower() == "true":
                return True
    return False


def build_validation(sections: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    checks = [
        ("VAL2800_0_sources_exist", all(row["exists"] for row in sections["sources"]), "all cited local source paths exist"),
        ("VAL2800_1_theorem_attempted", any(row["clause_id"] == "RDT2800_7_verdict" for row in sections["theorem"]), "response-doublet theorem attempt exists"),
        ("VAL2800_2_zero_not_promoted", any(row["clause_id"] == "RDT2800_7_verdict" and row["status"] == "FAIL_CURRENT_CLAIM" for row in sections["theorem"]), "zero theorem is not promoted"),
        ("VAL2800_3_bound_rows_written", len(sections["bound_fill"]) >= 8, "q_loc bound-fill rows are staged"),
        ("VAL2800_4_even_debts_recorded", {row["debt_id"] for row in sections["even_debt"]} >= {"EVEN2800_0_Y5_source_normalization", "EVEN2800_1_Y6_extra_stress"}, "Y5/Y6 even debts are recorded"),
        ("VAL2800_5_bound_runner_nonclaim", all(str(row["claim_allowed"]).lower() == "false" for row in sections["bound_runner"]), "bound runner keeps rows nonclaim"),
        ("VAL2800_6_proxy_not_claim", any(row["bound_id"] == "QBF2800_0_compact_shell_budget" and row["status"] == "anchor_proxy_not_claim_curve" for row in sections["bound_fill"]), "compact shell proxy is labelled nonclaim"),
        ("VAL2800_7_product_runner_refuses", any(row["expected_result"] == "RUNNER_REFUSES_WEP_LOCAL_GR_CLAIM" and str(row["claim_allowed"]).lower() == "false" for row in sections["product_runner"]), "product runner refuses claim"),
        ("VAL2800_8_claim_gates_safe", all(str(row["claim_allowed"]).lower() == "false" for row in sections["gates"]), "all claim gates keep claims blocked"),
        ("VAL2800_9_next_target_2801", any(row["next_id"] == "NEXT2800_0_2801" for row in sections["next"]), "next target is 2801"),
        ("VAL2800_10_branch_outputs_exist", all(path.exists() for path in BRANCH_OUTPUTS.values()), "branch copies were written"),
        ("VAL2800_11_outputs_exist", all(path.exists() for path in generated_paths), "all generated output paths exist"),
        ("VAL2800_12_csv_parse", all(csv_parses(path) for path in generated_paths), "all generated CSV outputs parse"),
        ("VAL2800_13_no_claim_flags", not claim_flags_true(sections), "no valid_for_claim or claim_allowed flag is true"),
        ("VAL2800_14_generated_under_post_checkpoint", all(str(path).startswith(str(WORK)) for path in generated_paths + [DOC]), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2800_15_formalization_untouched", formalization_untouched_since_run(), "formalization-workbench was not modified during this run"),
        ("VAL2800_16_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ absent before compile step"),
    ]
    rows = [{"validation_id": check_id, "passed": bool(passed), "detail": detail, "generated_utc": utc_now()} for check_id, passed, detail in checks]
    rows.append({"validation_id": "VAL2800_OVERALL", "passed": all(row["passed"] for row in rows), "detail": "2800 attempts the response-doublet source-current/boundary zero route, refuses promotion because even Y5/Y6 debts and boundary/source maps remain, and stages q_loc bound-fill rows as nonclaim.", "generated_utc": utc_now()})
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def build_doc(sections: dict[str, list[dict[str, Any]]]) -> str:
    lines = [
        "# 2800 — Y5 R2FR Response Doublet Source Current Zero Or q_loc Bound Fill Under AX1090",
        "",
        "## Private Verdict",
        "",
        "2800 tries the cleanest available route for killing the retained `q_loc` residual: response doublets with exact exchange symmetry, zero odd source current, zero boundary work, and a positive operator.",
        "",
        "That route still does not promote. Exchange symmetry can kill odd channels, but Y5 source normalization and Y6 extra stress can survive as exchange-even debts. The response-doublet zero theorem therefore remains conditional, and `q_loc` stays explicit.",
        "",
        "The fallback is useful: q_loc bound-fill rows are staged, but they are nonclaim templates/proxies until observable maps, units, and source-backed coefficients exist.",
        "",
        "## Response Doublet Theorem Attempt",
        markdown_table(sections["theorem"], ["clause_id", "claim_piece", "status", "current_evidence"]),
        "",
        "## q_loc Bound Fill Rows",
        markdown_table(sections["bound_fill"], ["bound_id", "quantity", "candidate_value", "units", "status"]),
        "",
        "## q_loc Bound Runner",
        markdown_table(sections["bound_runner"], ["runner_id", "bound_id", "verdict", "score_ready", "claim_allowed", "failure_reasons"]),
        "",
        "## Even Debt Ledger",
        markdown_table(sections["even_debt"], ["debt_id", "even_channel", "why_doublet_does_not_kill_it", "status", "repair_path"]),
        "",
        "## Claim Gates",
        markdown_table(sections["gates"], ["gate_id", "claim", "gate_pass", "claim_allowed", "reason"]),
        "",
        "## Decision Ledger",
        markdown_table(sections["decision"], ["decision_id", "decision", "because", "next_action"]),
        "",
        "## Validation",
        markdown_table(sections["validation"], ["validation_id", "passed", "detail"]),
        "",
        "## Next Target",
        markdown_table(sections["next"], ["next_id", "next_target", "objective", "include", "exclude"]),
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    ensure_dirs()
    if (SCRIPTS / "__pycache__").exists():
        shutil.rmtree(SCRIPTS / "__pycache__")

    sections: dict[str, list[dict[str, Any]]] = {
        "sources": build_sources(),
        "theorem": build_theorem_rows(),
        "bound_fill": build_bound_rows(),
    }
    sections["bound_runner"] = build_bound_runner_rows(sections["bound_fill"])
    sections["even_debt"] = build_even_debt_rows()
    sections["product_candidate"] = build_product_candidate_rows()
    sections["product_runner"] = build_product_runner_rows()
    sections["comparisons"] = build_comparison_rows()
    sections["gates"] = build_gate_rows()
    sections["decision"] = build_decision_rows()
    sections["next"] = build_next_rows()

    for key, rows in sections.items():
        if key in OUTPUTS:
            write_csv(OUTPUTS[key], rows)
    sections["branches"] = copy_branches()
    write_csv(OUTPUTS["branches"], sections["branches"])
    sections["validation"] = build_validation(sections)
    write_csv(OUTPUTS["validation"], sections["validation"])
    DOC.write_text(build_doc(sections), encoding="utf-8")
    print(f"wrote {DOC}")
    print(f"validation overall: {sections['validation'][-1]['passed']}")


if __name__ == "__main__":
    main()
