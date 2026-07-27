from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1551-Y5-parent-qnorm-source-or-local-closure-demotion.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1550_doc": ROOT / "1550-Y5-qnorm-Cqm-dual-pairing-and-envelope-closure.md",
    "1550_validation": OUT / "P8_Y5_BRR545_1550_VALIDATION.csv",
    "1550_next": OUT / "P8_Y5_PARENT_QLOC_1550_NEXT_TARGET.csv",
    "1550_qnorm": OUT / "P8_Y5_PARENT_QLOC_1550_QNORM_CANDIDATE_AUDIT.csv",
    "1550_dual": OUT / "P8_Y5_PARENT_QLOC_1550_DUAL_PAIRING_CONTRACT.csv",
    "1550_envelope": OUT / "P8_Y5_PARENT_QLOC_1550_SCG_ENVELOPE_UNIT_GATE.csv",
    "1550_guard": OUT / "P8_Y5_PARENT_QLOC_1550_NO_MIXED_NORM_GUARD.csv",
    "1549_unit": OUT / "P8_Y5_PARENT_QLOC_1549_UNIT_PAIRING_THEOREM_CONDITIONAL.csv",
    "1549_pairing": OUT / "P8_Y5_PARENT_QLOC_1549_CQM_PAIRING_REQUIREMENTS.csv",
    "1548_symbolic": OUT / "P8_Y5_PARENT_QLOC_1548_SHARED_SYMBOLIC_PROFILE_CANDIDATES.csv",
    "1547_support": OUT / "P8_Y5_PARENT_QLOC_1547_SUPPORT_DOMAIN_CONVENTIONS.csv",
    "1545_scg": OUT / "P8_Y5_PARENT_QLOC_1545_SCG_ENVELOPE_STATUS_NONCLAIM.csv",
    "1023_doc": ROOT / "1023-Y5-R10-q-vX-action-descent-certificate-or-scalar-nohair-demotion.md",
    "1022_doc": ROOT / "1022-Y5-R10-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md",
    "07_doc": ROOT / "07-nonpropagating-reciprocity-constraint.md",
    "source_owner": OUT / "P8_source_owner_parent_action_terms_CONTRACT.csv",
}

NEEDLES = {
    "1550_qnorm": ["MISSING_PARENT_OPERATOR_METRIC", "MISSING_PARENT_HESSIAN", "MISSING_REGULATOR_AND_DOMAIN"],
    "1550_dual": ["CONDITIONAL_THEOREM", "PASS_GUARD_NONCLAIM"],
    "1023_doc": ["MISSING_PARENT_INPUT", "fail_current_claim_demote_current_branch"],
    "1022_doc": ["template_only", "MISSING_PARENT_INPUT", "conditional_math_valid"],
    "07_doc": ["kinetic R_AB route = demoted", "not yet a full parent derivation"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1551_SOURCE_REGISTER.csv"
PARENT_NORM_HUNT = OUT / "P8_Y5_PARENT_QLOC_1551_PARENT_QNORM_SOURCE_HUNT.csv"
DEMOTION_GATE = OUT / "P8_Y5_PARENT_QLOC_1551_LOCAL_CLOSURE_DEMOTION_GATE.csv"
REENTRY_CONDITIONS = OUT / "P8_Y5_PARENT_QLOC_1551_QNORM_REENTRY_CONDITIONS.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1551_PARENT_QNORM_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1551_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1551_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1551_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1551_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1551"
QUAR_HUNT = QUARANTINE / "PARENT_QNORM_SOURCE_HUNT_NONCLAIM.csv"
QUAR_DEMOTION = QUARANTINE / "LOCAL_CLOSURE_DEMOTION_GATE_NONCLAIM.csv"
QUAR_REENTRY = QUARANTINE / "QNORM_REENTRY_CONDITIONS_NONCLAIM.csv"
QUAR_RUNNER = QUARANTINE / "PARENT_QNORM_RUNNER_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "DECISION_NONCLAIM.csv"
BRANCH_HUNT = BRANCH_RESIDUALS / "parent_qnorm_source_hunt_nonclaim_1551.csv"
BRANCH_DEMOTION = BRANCH_RESIDUALS / "local_closure_demotion_gate_nonclaim_1551.csv"
BRANCH_REENTRY = BRANCH_RESIDUALS / "qnorm_reentry_conditions_nonclaim_1551.csv"
BRANCH_RUNNER = BRANCH_RESIDUALS / "parent_qnorm_runner_nonclaim_1551.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "qnorm_decision_nonclaim_1551.csv"


def flags() -> dict[str, bool]:
    return {
        "numeric_value_present": False,
        "source_backed": False,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def source_list(*keys: str) -> str:
    return "; ".join(rel(SOURCE_FILES[key]) for key in keys)


def file_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    return all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    claim_keys = [
        "numeric_value_present",
        "source_backed",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "accepted_for_scoring",
        "passes_for_claim",
    ]
    for path in paths:
        for row in read_csv(path):
            for key in claim_keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for index, (key, path) in enumerate(SOURCE_FILES.items()):
        needles = NEEDLES.get(key, [])
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1551_{index}_{key}",
                "source_path": rel(path),
                "exists": path.exists(),
                "needle_found": file_contains(path, needles) if needles else True,
                "needles": "; ".join(needles),
                "purpose": "evidence for parent q-norm hunt or local closure demotion",
                **flags(),
            }
        )
    return rows


def parent_norm_hunt_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "hunt_id": "HUNT1551_0_parent_operator_metric",
            "route": "parent kinetic/operator metric G_AB",
            "evidence_found": "1550 identifies this as the best q-norm route",
            "evidence_status": "MISSING_PARENT_OPERATOR_METRIC",
            "reason": "no source row provides a positive parent G_AB on q variations",
            "claim_effect": "if supplied, T_source_norm and C_qm can use the same E",
            "source_paths": source_list("1550_qnorm", "1549_pairing", "source_owner"),
        },
        {
            "hunt_id": "HUNT1551_1_parent_hessian",
            "route": "linearized Hessian of parent action",
            "evidence_found": "1022/1023 scalar no-hair rows require positive kinetic Hessian but mark it missing",
            "evidence_status": "MISSING_PARENT_HESSIAN",
            "reason": "second variation, field units, domain, and self-adjoint boundary conditions are not parent-signed",
            "claim_effect": "if supplied, E could be the coercive quadratic form after gauge quotient",
            "source_paths": source_list("1550_qnorm", "1022_doc", "1023_doc"),
        },
        {
            "hunt_id": "HUNT1551_2_worldtube_regulator",
            "route": "regularized worldtube norm",
            "evidence_found": "1547/1548 have a compact-profile template but no regulator law",
            "evidence_status": "MISSING_REGULATOR_AND_DOMAIN",
            "reason": "epsilon_reg, support, boundary flux, and source profile normalization remain unsourced",
            "claim_effect": "if supplied, E could be a worldtube/regulator norm shared by all arenas",
            "source_paths": source_list("1550_qnorm", "1548_symbolic", "1547_support"),
        },
        {
            "hunt_id": "HUNT1551_3_kinetic_RAB_route",
            "route": "old kinetic R_AB norm",
            "evidence_found": "07 explicitly demotes the kinetic R_AB route because it creates exterior reciprocal hair",
            "evidence_status": "REJECTED_FOR_CURRENT_QNORM",
            "reason": "a propagating R_AB kinetic term is the wrong local route for the current finite q-norm gate",
            "claim_effect": "cannot be reused as the parent q-norm without reversing the nonpropagating-constraint decision",
            "source_paths": source_list("07_doc", "1550_qnorm"),
        },
        {
            "hunt_id": "HUNT1551_4_quotient_reduced_norm",
            "route": "reduced quotient norm after v_X/q descent",
            "evidence_found": "1023 says q/v_X/action certificate fails and demotes the current branch",
            "evidence_status": "CONDITIONAL_FUTURE_ROUTE_ONLY",
            "reason": "q map, action descent, matter descent, boundary silence, and degree count do not close together",
            "claim_effect": "could become a clean reduced norm only if the full quotient certificate is parent-signed",
            "source_paths": source_list("1022_doc", "1023_doc", "1550_qnorm"),
        },
        {
            "hunt_id": "HUNT1551_5_current_verdict",
            "route": "accepted parent q-norm",
            "evidence_found": "no accepted source found in current state",
            "evidence_status": "ABSENT_CURRENTLY",
            "reason": "all candidate routes are missing, conditional, or rejected",
            "claim_effect": "finite local branch must be demoted to closure-only until a parent norm is added",
            "source_paths": source_list("1550_qnorm", "1550_dual", "1550_envelope"),
        },
    ]
    return [{**{"same_parent_branch_id": BRANCH_ID}, **row, **flags()} for row in rows]


def demotion_gate_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEM1551_0_scope",
            "finite local q-norm route",
            "demote_to_explicit_closure_until_parent_norm_exists",
            "the route is mathematically legal but not parent-sourced",
            "closure may be used as a bookkeeping hypothesis, not as derived GR/Newton reduction",
        ),
        (
            "DEM1551_1_Scg",
            "S_cg_norm source envelope",
            "schema_ready_unit_routable_not_computable",
            "same-norm theorem exists but E, J_q, Dq[v_m], and other residual inputs are missing",
            "keep envelope rows nonclaim",
        ),
        (
            "DEM1551_2_arenas",
            "R10/PPN/clock/orbital projections",
            "blocked_no_claim",
            "arena kernels cannot score from a closure-only source norm",
            "no local test pass follows",
        ),
        (
            "DEM1551_3_GR_Newton",
            "GR/Newton local reduction",
            "blocked_no_claim",
            "source norm and residual vector are not derivable from current parent action",
            "do not describe local GR as derived",
        ),
        (
            "DEM1551_4_reentry",
            "future reentry",
            "allowed_only_with_parent_norm_certificate",
            "a future parent action can reopen the route if it supplies E and passes the reentry checklist",
            "avoid killing the route; quarantine it properly",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "demotion_id": demotion_id,
            "object": object_name,
            "demotion": demotion,
            "reason": reason,
            "surviving_use": surviving_use,
            "source_paths": source_list("1550_envelope", "1550_dual", "1550_guard"),
            **flags(),
        }
        for demotion_id, object_name, demotion, reason, surviving_use in rows
    ]


def reentry_condition_rows() -> list[dict[str, Any]]:
    rows = [
        ("RE1551_0_q_field", "parent q/q_loc field definition", "field dimension and observed-frame descent are explicit", "MISSING"),
        ("RE1551_1_norm", "parent-owned q-norm E", "kinetic/operator metric, Hessian, or regulator norm is sourced and positive/coercive", "MISSING"),
        ("RE1551_2_variation_domain", "allowed variation class", "compact support, boundary, quotient/gauge, and regularity domain are declared", "MISSING"),
        ("RE1551_3_Jq", "source current J_q", "delta S_matter/delta q is parent-derived in the same frame", "MISSING"),
        ("RE1551_4_Dqvm", "C_qm in same norm", "Dq[v_m] is computed in E with no norm switch", "MISSING"),
        ("RE1551_5_boundary", "boundary/source residuals", "boundary terms are zero-proved or included in S_boundary_m", "MISSING"),
        ("RE1551_6_envelope", "S_cg envelope", "all terms in S_cg_norm have compatible units and no hidden cancellation", "MISSING"),
        ("RE1551_7_arenas", "arena projection kernels", "Pi_R10/Pi_PPN/Pi_clock/Pi_orbital/Pi_local map the same norm to observables", "MISSING"),
        ("RE1551_8_claim_policy", "claim policy", "no local claim until all previous conditions pass", "PASS_GUARD_NONCLAIM"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "reentry_id": reentry_id,
            "needed_input": needed_input,
            "acceptance_requirement": acceptance_requirement,
            "current_status": current_status,
            "source_paths": source_list("1550_qnorm", "1550_dual", "1550_envelope", "1549_unit"),
            **flags(),
        }
        for reentry_id, needed_input, acceptance_requirement, current_status in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN1551_0_operator_metric", "parent kinetic/operator metric", "REFUSED_MISSING_PARENT_OPERATOR_METRIC", "no positive G_AB source found"),
        ("RUN1551_1_hessian", "parent Hessian norm", "REFUSED_MISSING_PARENT_HESSIAN", "scalar/no-hair Hessian rows remain missing parent input"),
        ("RUN1551_2_regulator", "worldtube regulator norm", "REFUSED_MISSING_REGULATOR", "compact profile regulator/domain not sourced"),
        ("RUN1551_3_RAB", "old kinetic R_AB route", "REFUSED_DEMOTED_ROUTE", "07 demoted kinetic R_AB because it creates exterior hair"),
        ("RUN1551_4_quotient", "quotient reduced norm", "REFUSED_CONDITIONAL_ONLY", "1023 says q/v_X/action certificate fails for current MTS"),
        ("RUN1551_5_closure_demotion", "local closure demotion", "PASS_NONCLAIM", "finite local route is quarantined as closure-only"),
        ("RUN1551_6_score_status", "local GR/Newton score", "REFUSED_NOT_SCORE_READY", "no parent q-norm exists"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "check": check,
            "current_status": current_status,
            "reason": reason,
            "accepted_for_scoring": False,
            "passes_for_claim": False,
            **flags(),
        }
        for runner_id, check, current_status, reason in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1551_0_hunt", "parent q-norm source hunt", "PASS_NONCLAIM", "candidate routes audited against current evidence"),
        ("GATE1551_1_demotion", "local finite branch closure demotion", "PASS_NONCLAIM", "closure-only status is explicit"),
        ("GATE1551_2_reentry", "reentry checklist", "PASS_NONCLAIM", "future parent norm requirements written"),
        ("GATE1551_3_parent_norm", "accepted parent q-norm", "BLOCKED", "no source found"),
        ("GATE1551_4_Scg", "S_cg_norm computable", "BLOCKED", "closure-only branch cannot compute envelope"),
        ("GATE1551_5_local_tests", "R10/PPN/clock/orbital/local test pass", "BLOCKED_NO_CLAIM", "no local score from missing norm"),
        ("GATE1551_6_GR_Newton", "derived GR/Newton local limit", "BLOCKED_NO_CLAIM", "route remains closure-only"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for gate_id, claim, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC1551_0_result", "No parent-owned q-norm is found in current evidence.", "NO_ACCEPTED_QNORM_SOURCE", "candidate routes are missing, conditional, or rejected"),
        ("DEC1551_1_demotion", "Demote the finite local q-norm route to explicit closure-only.", "LOCAL_BRANCH_CLOSURE_ONLY", "this preserves the route without pretending it derives local GR"),
        ("DEC1551_2_best_next", "Next target is a parent q-sector action/norm extraction template.", "NEXT_1552_PARENT_QSECTOR_ACTION", "derive a minimal parent-owned q-sector or declare the needed parent action slot"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "result": result,
            "rationale": rationale,
            **flags(),
        }
        for decision_id, decision, result, rationale in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1551_0_1552",
            "next_target": "1552-Y5-parent-q-sector-action-norm-extraction-template.md",
            "script": "scripts/Y5_parent_q_sector_action_norm_extraction_template.py",
            "objective": "write the exact parent q-sector action/norm extraction contract needed to reopen the local GR/Newton derivation route",
            "do_not": "do not claim the closure as derivation; do not choose a norm by arena fit; do not edit formalization-workbench",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (PARENT_NORM_HUNT, QUAR_HUNT),
        (DEMOTION_GATE, QUAR_DEMOTION),
        (REENTRY_CONDITIONS, QUAR_REENTRY),
        (RUNNER, QUAR_RUNNER),
        (DECISION, QUAR_DECISION),
        (PARENT_NORM_HUNT, BRANCH_HUNT),
        (DEMOTION_GATE, BRANCH_DEMOTION),
        (REENTRY_CONDITIONS, BRANCH_REENTRY),
        (RUNNER, BRANCH_RUNNER),
        (DECISION, BRANCH_DECISION),
    ]
    for source, destination in copies:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_modified_count_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= START_TS)


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    hunt_rows = read_csv(PARENT_NORM_HUNT)
    demotion_rows = read_csv(DEMOTION_GATE)
    reentry_rows = read_csv(REENTRY_CONDITIONS)
    run_rows = read_csv(RUNNER)
    gate_rows = read_csv(CLAIM_GATE)
    decision_items = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    checks = [
        ("VAL1551_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1551 source paths exist"),
        ("VAL1551_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all registered evidence needles found"),
        ("VAL1551_2_hunt_verdict", any(row["hunt_id"] == "HUNT1551_5_current_verdict" and row["evidence_status"] == "ABSENT_CURRENTLY" for row in hunt_rows), "parent q-norm hunt records no accepted source"),
        ("VAL1551_3_demote_closure", any(row["demotion_id"] == "DEM1551_0_scope" and row["demotion"] == "demote_to_explicit_closure_until_parent_norm_exists" for row in demotion_rows), "finite local route demoted to explicit closure-only"),
        ("VAL1551_4_reentry_conditions", len(reentry_rows) >= 9 and any(row["reentry_id"] == "RE1551_8_claim_policy" for row in reentry_rows), "q-norm reentry checklist written"),
        ("VAL1551_5_runner_refuses_score", any(row["runner_id"] == "RUN1551_6_score_status" and row["current_status"] == "REFUSED_NOT_SCORE_READY" for row in run_rows), "parent q-norm runner refuses local scoring"),
        ("VAL1551_6_claim_gates_block", any(row["gate_id"] == "GATE1551_6_GR_Newton" and row["status"] == "BLOCKED_NO_CLAIM" for row in gate_rows), "GR/Newton claim remains blocked"),
        ("VAL1551_7_decision_next", any(row["result"] == "NEXT_1552_PARENT_QSECTOR_ACTION" for row in decision_items), "decision selects parent q-sector action/norm extraction next"),
        ("VAL1551_8_next_target", any("1552-Y5-parent-q-sector" in row["next_target"] for row in next_rows), "next target is parent q-sector action/norm extraction template"),
        ("VAL1551_9_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1551 CSVs parse cleanly"),
        ("VAL1551_10_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1551_11_branch_copies", all(path.exists() for path in [QUAR_HUNT, QUAR_DEMOTION, QUAR_REENTRY, QUAR_RUNNER, QUAR_DECISION, BRANCH_HUNT, BRANCH_DEMOTION, BRANCH_REENTRY, BRANCH_RUNNER, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1551_12_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1551_13_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1551_14_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1551 finds no accepted parent q-norm in current evidence, demotes the finite local route to explicit closure-only, and writes reentry conditions"
            if overall
            else "1551 validation failed; inspect failed rows before continuing",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    output = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        output.append(
            "| "
            + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns)
            + " |"
        )
    return "\n".join(output)


def write_doc(
    sources: list[dict[str, Any]],
    hunt_rows: list[dict[str, Any]],
    demotion_rows: list[dict[str, Any]],
    reentry_rows: list[dict[str, Any]],
    run_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    decision_items: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1551 - Parent q-norm Source or Local Closure Demotion",
                "",
                "## Verdict",
                "- No accepted parent-owned `q` norm is found in the current evidence.",
                "- The kinetic/operator, Hessian, worldtube-regulator, and quotient-reduced norm routes remain useful future routes, but they are not currently source-backed.",
                "- The old kinetic `R_AB` route is explicitly not reused because it was already demoted for creating exterior reciprocal hair.",
                "- Therefore the finite local `q`-norm route is demoted to explicit closure-only until a parent q-sector supplies `E`, `J_q`, and `Dq[v_m]` in one norm.",
                "- This is not a failure of the whole framework; it is a disciplined quarantine of the local-GR derivation route.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "",
                "## Parent q-norm Source Hunt",
                md_table(hunt_rows, ["hunt_id", "route", "evidence_status", "reason", "claim_effect"]),
                "",
                "## Local Closure Demotion Gate",
                md_table(demotion_rows, ["demotion_id", "object", "demotion", "reason", "surviving_use"]),
                "",
                "## q-norm Reentry Conditions",
                md_table(reentry_rows, ["reentry_id", "needed_input", "acceptance_requirement", "current_status"]),
                "",
                "## Runner",
                md_table(run_rows, ["runner_id", "check", "current_status", "reason"]),
                "",
                "## Claim Gates",
                md_table(gate_rows, ["gate_id", "claim", "status", "reason"]),
                "",
                "## Decision",
                md_table(decision_items, ["decision_id", "decision", "result", "rationale"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_id", "next_target", "script", "objective", "do_not"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    sources = source_register_rows()
    hunt_rows = parent_norm_hunt_rows()
    demotion_rows = demotion_gate_rows()
    reentry_rows = reentry_condition_rows()
    run_rows = runner_rows()
    gate_rows = claim_gate_rows()
    decision_items = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(PARENT_NORM_HUNT, hunt_rows)
    write_csv(DEMOTION_GATE, demotion_rows)
    write_csv(REENTRY_CONDITIONS, reentry_rows)
    write_csv(RUNNER, run_rows)
    write_csv(CLAIM_GATE, gate_rows)
    write_csv(DECISION, decision_items)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        PARENT_NORM_HUNT,
        DEMOTION_GATE,
        REENTRY_CONDITIONS,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, hunt_rows, demotion_rows, reentry_rows, run_rows, gate_rows, decision_items, validation, next_rows)


if __name__ == "__main__":
    main()
