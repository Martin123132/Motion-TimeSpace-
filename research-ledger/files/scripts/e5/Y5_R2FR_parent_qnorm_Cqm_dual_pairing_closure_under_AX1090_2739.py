from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2739-Y5-R2FR-parent-qnorm-Cqm-dual-pairing-closure-under-AX1090.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2739_SOURCE_REGISTER.csv",
    "hunt": RESIDUALS / "P8_Y5_R2FR_2739_PARENT_QNORM_SOURCE_HUNT.csv",
    "dual": RESIDUALS / "P8_Y5_R2FR_2739_DUAL_PAIRING_STATUS.csv",
    "demotion": RESIDUALS / "P8_Y5_R2FR_2739_LOCAL_CLOSURE_DEMOTION_GATE.csv",
    "reentry": RESIDUALS / "P8_Y5_R2FR_2739_QNORM_REENTRY_CONDITIONS.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_2739_DECISION_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2739_CLAIM_GATES.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2739_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2739_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2739_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "closure": LOCAL_BOUNDS / "qnorm_closure_status_2739_NONCLAIM.csv",
    "reentry": SOURCE_WEIGHT / "qnorm_reentry_conditions_2739_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2739_PARENT_QSECTOR_ACTION_TEMPLATE_NEXT.csv",
}

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()}:
        path.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def md(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], cols: list[str]) -> str:
    header = "| " + " | ".join(cols) + " |"
    sep = "| " + " | ".join("---" for _ in cols) + " |"
    body = ["| " + " | ".join(md(row.get(col, "")) for col in cols) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def local_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["score_ready"] = False
    row["valid_prediction_row"] = False
    row["valid_for_claim"] = False
    row["claim_allowed"] = False
    return row


def source_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": "SRC2739_0_2738_doc",
            "description": "2738 selects parent q-norm/Cqm dual-pairing closure.",
            "source_path": "2738-Y5-R2FR-worldtube-source-profile-and-inner-charge-template-under-AX1090.md",
            "required_needles": "NEXT2738_0_2739;CORE2738_2_qnorm;TR2738_5_first_pair_insert;VAL2738_OVERALL",
        },
        {
            "source_id": "SRC2739_1_1550_doc",
            "description": "1550 states same-norm dual pairing and candidate q-norm routes.",
            "source_path": "1550-Y5-qnorm-Cqm-dual-pairing-and-envelope-closure.md",
            "required_needles": "QN1550_0_parent_kinetic_energy_norm;DUAL1550_3_holder_bound;NMN1550_0_single_E;NEXT1550_0_1551",
        },
        {
            "source_id": "SRC2739_2_1551_doc",
            "description": "1551 hunts for q-norm source and demotes finite local route to closure-only.",
            "source_path": "1551-Y5-parent-qnorm-source-or-local-closure-demotion.md",
            "required_needles": "HUNT1551_5_current_verdict;DEM1551_0_scope;RE1551_1_norm;NEXT1551_0_1552",
        },
        {
            "source_id": "SRC2739_3_1552_doc",
            "description": "1552 gives parent q-sector action/norm extraction contract for reentry.",
            "source_path": "1552-Y5-parent-q-sector-action-norm-extraction-template.md",
            "required_needles": "ACT1552_0_q_field;ALG1552_2_extract_E;FAIL1552_0_arena_norm;NEXT1552_0_1553",
        },
        {
            "source_id": "SRC2739_4_1550_qnorm_csv",
            "description": "machine-readable q-norm candidate audit.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1550_QNORM_CANDIDATE_AUDIT.csv",
            "required_needles": "QN1550_0_parent_kinetic_energy_norm;QN1550_1_linearized_hessian_norm;QN1550_4_current_verdict",
        },
        {
            "source_id": "SRC2739_5_1550_dual_csv",
            "description": "machine-readable same-norm dual-pairing contract.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1550_DUAL_PAIRING_CONTRACT.csv",
            "required_needles": "DUAL1550_1_source_dual;DUAL1550_2_cqm_primal;DUAL1550_5_no_mixed_norm",
        },
        {
            "source_id": "SRC2739_6_1551_hunt_csv",
            "description": "machine-readable parent q-norm source hunt.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1551_PARENT_QNORM_SOURCE_HUNT.csv",
            "required_needles": "HUNT1551_0_parent_operator_metric;HUNT1551_5_current_verdict;ABSENT_CURRENTLY",
        },
        {
            "source_id": "SRC2739_7_1551_demotion_csv",
            "description": "machine-readable closure demotion gate.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1551_LOCAL_CLOSURE_DEMOTION_GATE.csv",
            "required_needles": "DEM1551_0_scope;DEM1551_3_GR_Newton;DEM1551_4_reentry",
        },
        {
            "source_id": "SRC2739_8_1552_action_csv",
            "description": "machine-readable parent q-sector action template.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1552_PARENT_QSECTOR_ACTION_TEMPLATE.csv",
            "required_needles": "ACT1552_0_q_field;ACT1552_1_quadratic_form;ACT1552_6_parent_action_verdict",
        },
        {
            "source_id": "SRC2739_9_1552_filters_csv",
            "description": "machine-readable failure filters for q-sector extraction.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1552_ACTION_FAILURE_FILTERS.csv",
            "required_needles": "FAIL1552_0_arena_norm;FAIL1552_1_mixed_norm;FAIL1552_6_long_range_hair",
        },
    ]
    for row in rows:
        path = local_path(row["source_path"])
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        needles = [needle for needle in row["required_needles"].split(";") if needle]
        missing = [needle for needle in needles if needle not in text]
        row["exists"] = path.exists()
        row["needles_present"] = len(missing) == 0
        row["missing_needles"] = ";".join(missing)
        nonclaim(row)
    return rows


def hunt_rows() -> list[dict[str, Any]]:
    specs = [
        ("HUNT2739_0_operator_metric", "parent kinetic/operator metric G_AB", "||delta q||_E^2=int_W delta q^A G_AB delta q^B dV_e", "MISSING_PARENT_OPERATOR_METRIC", "no positive parent G_AB source row exists", "would be the cleanest same-norm source/Cqm route"),
        ("HUNT2739_1_hessian", "linearized Hessian norm", "||delta q||_H^2=delta^2 S_parent[delta q,delta q] after quotient/gauge fixing", "MISSING_PARENT_HESSIAN", "second variation/domain/boundary/coercivity not parent-signed", "would supply E if positive after zero-mode quotient"),
        ("HUNT2739_2_regulator", "worldtube regulator norm", "E_epsilon[delta q;W_src] from a parent regulator/excision law", "MISSING_REGULATOR_AND_DOMAIN", "epsilon_reg/support/boundary flux and limiting procedure absent", "could share W_src profile with all arenas if sourced"),
        ("HUNT2739_3_quotient_reduced", "quotient-reduced norm", "E on reduced q variables after q/v_X/action descent", "CONDITIONAL_FUTURE_ROUTE_ONLY", "q map, action descent, matter descent, and boundary silence do not close together", "future clean route if full quotient certificate is signed"),
        ("HUNT2739_4_rejected_RAB", "old kinetic R_AB route", "reuse demoted reciprocal kinetic route as q-norm", "REJECTED_FOR_CURRENT_QNORM", "reintroduces exterior reciprocal hair and contradicts prior demotion", "not admissible without new parent action"),
        ("HUNT2739_5_verdict", "accepted parent q-norm E_q", "none accepted", "ABSENT_CURRENTLY", "all live candidates are missing, conditional, or rejected", "finite q-norm local branch cannot be called derived"),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "hunt_id": hunt_id,
                "route": route,
                "candidate_norm": formula,
                "evidence_status": status,
                "reason": reason,
                "effect_if_supplied": effect,
                "accepted_parent_norm": False,
                "source_paths": "1550-Y5-qnorm-Cqm-dual-pairing-and-envelope-closure.md; 1551-Y5-parent-qnorm-source-or-local-closure-demotion.md; 1552-Y5-parent-q-sector-action-norm-extraction-template.md",
            }
        )
        for hunt_id, route, formula, status, reason, effect in specs
    ]


def dual_rows() -> list[dict[str, Any]]:
    rows = [
        ("DUAL2739_0_variation_space", "E_q", "one parent-owned q-variation norm/domain used before arena projection", "CONDITIONAL_THEOREM_INPUT_MISSING", "E_q absent"),
        ("DUAL2739_1_source_dual", "T_source_norm", "T_source_norm:=sup_{||delta q||_E<=1}|int_W J_A delta q^A dV_e|", "FORMULA_LEGAL_IF_E_AND_JQ_EXIST", "E_q and J_q absent"),
        ("DUAL2739_2_cqm_primal", "C_qm", "C_qm:=||Dq[v_m]||_E in the same E_q", "FORMULA_LEGAL_IF_E_AND_DQVM_EXIST", "E_q and Dq[v_m] norm absent"),
        ("DUAL2739_3_holder", "source-Cqm product", "|int_W J_A Dq[v_m]^A dV_e| <= T_source_norm*C_qm", "DERIVED_CONDITIONAL_SAME_NORM_ONLY", "cannot score without E_q/J_q/Dq[v_m]"),
        ("DUAL2739_4_envelope", "S_geom_m", "S_geom_m <= 1/2*T_source_norm*C_qm", "UNIT_ROUTABLE_NOT_COMPUTABLE", "same-norm product legal but values absent"),
        ("DUAL2739_5_no_mixed_norm", "mixed norm veto", "E_source != E_Cqm invalidates the product bound", "PASS_GUARD_NONCLAIM", "guard remains active"),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "dual_id": dual_id,
                "object": obj,
                "contract": contract,
                "current_status": status,
                "blocker": blocker,
                "same_norm_required": True,
                "source_paths": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1550_DUAL_PAIRING_CONTRACT.csv; source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1549_UNIT_PAIRING_THEOREM_CONDITIONAL.csv",
            }
        )
        for dual_id, obj, contract, status, blocker in rows
    ]


def demotion_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEM2739_0_scope", "finite local q-norm route", "demote_to_explicit_closure_until_parent_norm_exists", "same-norm theorem exists but parent E_q is absent", "may be used only as a named closure/hypothesis, not as GR/Newton derivation"),
        ("DEM2739_1_Npair", "N_pair source/profile branch", "closure_only_first_pair_until_Eq_and_inputs_exist", "N_pair depends on S_cg,total and Q_m^H terms whose source norm uses E_q", "keep first-pair rows as acquisition templates"),
        ("DEM2739_2_Nlock", "N_lock local-lock branch", "not_score_ready", "N_pair plus N_rest are nonnumeric and closure-dependent", "no q_loc-zero or local residual score"),
        ("DEM2739_3_GR_Newton", "local GR/Newton reduction", "blocked_no_claim", "a closure-only source norm is not a derivation of GR recovery", "do not call local GR derived from this route"),
        ("DEM2739_4_reentry", "future reentry", "allowed_with_parent_qsector_action_certificate", "1552 gives the action/norm extraction contract", "route can reopen if parent action supplies E_q/J_q/Dq[v_m]"),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "demotion_id": demotion_id,
                "object": obj,
                "demotion": demotion,
                "reason": reason,
                "surviving_use": use,
                "source_paths": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1551_LOCAL_CLOSURE_DEMOTION_GATE.csv; 2738-Y5-R2FR-worldtube-source-profile-and-inner-charge-template-under-AX1090.md",
            }
        )
        for demotion_id, obj, demotion, reason, use in rows
    ]


def reentry_rows() -> list[dict[str, Any]]:
    specs = [
        ("RE2739_0_q_field", "parent q/q_loc field", "field identity, dimension, observed-frame descent, quotient/gauge status", "MISSING"),
        ("RE2739_1_Eq", "parent q-norm E_q", "kinetic/operator metric, Hessian, or regulator norm positive/coercive after quotienting nulls", "MISSING"),
        ("RE2739_2_variation_domain", "allowed variation domain", "compact support, boundary behavior, regularity, and zero-mode convention", "MISSING"),
        ("RE2739_3_Jq", "source current J_q", "delta S_matter/delta q in same observed frame and same variation domain", "MISSING"),
        ("RE2739_4_Dqvm", "C_qm in E_q", "Dq[v_m] computed in E_q with no norm switch", "MISSING"),
        ("RE2739_5_boundary", "boundary/source residuals", "boundary terms zero-proved or retained in S_boundary_m/N_inner rows", "MISSING"),
        ("RE2739_6_envelope", "S_cg,total envelope", "all source/direct/boundary/affine/block terms compatible in units and no hidden cancellation", "MISSING"),
        ("RE2739_7_arena_kernels", "Pi_arena maps", "R10/PPN/clock/orbital/local kernels from same profile and norm into observables", "MISSING"),
        ("RE2739_8_claim_policy", "claim policy", "no local claim until every prior reentry condition passes", "PASS_GUARD_NONCLAIM"),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "reentry_id": reentry_id,
                "needed_input": needed,
                "acceptance_requirement": requirement,
                "current_status": status,
                "source_paths": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1551_QNORM_REENTRY_CONDITIONS.csv; 1552-Y5-parent-q-sector-action-norm-extraction-template.md",
            }
        )
        for reentry_id, needed, requirement, status in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2739_0_same_norm", "Keep the same-norm dual-pairing theorem.", "it is mathematically right and prevents source/Cqm norm cheating", "T_source_norm*C_qm remains legal only inside one E_q"),
        ("DEC2739_1_no_parent_norm", "No parent E_q is currently accepted.", "kinetic, Hessian, regulator, and quotient-reduced routes are missing/conditional/rejected", "finite q-norm route cannot be called derived"),
        ("DEC2739_2_demote", "Demote this local branch to explicit closure-only for now.", "closure is better than a fake GR-reduction claim", "N_pair/Nlock rows survive as acquisition contracts"),
        ("DEC2739_3_next", "Next target is parent q-sector action/norm extraction.", "1552 already states the exact action slots; current branch needs that contract refreshed under AX1090", "2740 should write the parent action/norm extraction contract for reentry"),
    ]
    return [nonclaim({"decision_id": decision_id, "decision": decision, "because": because, "effect": effect}) for decision_id, decision, because, effect in rows]


def gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2739_0_same_norm", "same-norm dual-pairing theorem", True, "PASS_CONDITIONAL_NONCLAIM", "Holder/dual pairing is legal if parent E_q exists"),
        ("GATE2739_1_no_mixed_norm", "mixed norm veto", True, "PASS_GUARD", "source and C_qm cannot use different norms"),
        ("GATE2739_2_parent_norm", "accepted parent q-norm E_q", False, "BLOCKED", "no source-backed kinetic/Hessian/regulator/reduced norm found"),
        ("GATE2739_3_closure_demotion", "local qnorm route closure-only", True, "PASS_NONCLAIM", "demotion is explicit and nonclaim"),
        ("GATE2739_4_Npair_score", "numeric N_pair/Nlock", False, "BLOCKED", "closure-only E_q and missing source/profile values"),
        ("GATE2739_5_local_GR", "derived local GR/Newton limit", False, "BLOCKED_NO_CLAIM", "closure-only route is not a derivation"),
        ("GATE2739_6_arena_scores", "R10/PPN/clock/orbital pass", False, "BLOCKED_NO_CLAIM", "no legal source norm or arena kernels"),
    ]
    return [
        nonclaim(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "gate_passed": passed,
                "status": status,
                "claim_allowed": False,
                "reason": reason,
            }
        )
        for gate_id, claim, passed, status, reason in rows
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2739_0_2740",
                "status": "selected_primary",
                "target_doc": "2740-Y5-R2FR-parent-qsector-action-norm-extraction-contract-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_parent_qsector_action_norm_extraction_contract_under_AX1090_2740.py",
                "mission": "write the exact parent q-sector action/norm extraction contract needed to reopen the local GR/Newton derivation route: q field, positive quadratic form/regulator, J_q, C_qm in one norm, boundary terms, and failure filters",
                "acceptance": "action slots and extraction algorithm are explicit; all failure filters active; no claim reopens without supplied parent action data",
                "forbidden": "do not claim the closure as derivation; do not choose norms by arena fit; do not mix source/Cqm norms",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"copy_id": "BR2739_0_closure", "source_table": rel(OUTPUTS["demotion"]), "copy_path": rel(BRANCH_OUTPUTS["closure"]), "purpose": "local-bound nonclaim closure status for q-norm route", "exists": BRANCH_OUTPUTS["closure"].exists()}),
        nonclaim({"copy_id": "BR2739_1_reentry", "source_table": rel(OUTPUTS["reentry"]), "copy_path": rel(BRANCH_OUTPUTS["reentry"]), "purpose": "source-weight qnorm reentry conditions", "exists": BRANCH_OUTPUTS["reentry"].exists()}),
        nonclaim({"copy_id": "BR2739_2_next_queue", "source_table": rel(OUTPUTS["next"]), "copy_path": rel(BRANCH_OUTPUTS["next_queue"]), "purpose": "RAB acquisition queue for parent q-sector action/norm contract", "exists": BRANCH_OUTPUTS["next_queue"].exists()}),
    ]


def formalization_recent_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    start = SCRIPT_START_UTC.timestamp()
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= start)


def validation_rows(
    sources: list[dict[str, Any]],
    hunt: list[dict[str, Any]],
    dual: list[dict[str, Any]],
    demotion: list[dict[str, Any]],
    reentry: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_ok = all(row["exists"] is True and row["needles_present"] is True for row in sources)
    hunt_ok = any(row["hunt_id"] == "HUNT2739_5_verdict" and row["evidence_status"] == "ABSENT_CURRENTLY" for row in hunt)
    dual_ok = any(row["dual_id"] == "DUAL2739_3_holder" for row in dual) and any(row["dual_id"] == "DUAL2739_5_no_mixed_norm" for row in dual)
    demotion_ok = any(row["demotion_id"] == "DEM2739_0_scope" for row in demotion) and any(row["demotion_id"] == "DEM2739_3_GR_Newton" for row in demotion)
    reentry_ok = len(reentry) == 9 and any(row["reentry_id"] == "RE2739_8_claim_policy" for row in reentry)
    gates_ok = any(row["claim_gate_id"] == "GATE2739_3_closure_demotion" and row["gate_passed"] is True for row in gates) and all(row["claim_allowed"] is False for row in gates)
    next_ok = next_target[0]["selected"] is True and "qsector-action" in next_target[0]["target_doc"]
    branch_ok = all(path.exists() for path in BRANCH_OUTPUTS.values())
    formalization_ok = formalization_recent_count() == 0
    csv_ok = True
    csv_bits: list[str] = []
    for key, path in {**OUTPUTS, **BRANCH_OUTPUTS}.items():
        if key == "validation":
            continue
        try:
            rows = read_csv(path)
            csv_bits.append(f"{path.name}:{len(rows)}:ok")
        except Exception as exc:
            csv_ok = False
            csv_bits.append(f"{path.name}:ERROR:{exc}")
    rows = [
        {"validation_id": "VAL2739_0_sources", "passed": source_ok, "detail": "all source paths exist and required anchors/needles are present", "timestamp_utc": ts()},
        {"validation_id": "VAL2739_1_hunt_verdict", "passed": hunt_ok, "detail": "no accepted parent q-norm found in current evidence", "timestamp_utc": ts()},
        {"validation_id": "VAL2739_2_dual_pairing", "passed": dual_ok, "detail": "same-norm dual-pairing theorem and mixed-norm veto are recorded", "timestamp_utc": ts()},
        {"validation_id": "VAL2739_3_closure_demotion", "passed": demotion_ok, "detail": "finite qnorm local route is demoted to explicit closure-only", "timestamp_utc": ts()},
        {"validation_id": "VAL2739_4_reentry_conditions", "passed": reentry_ok, "detail": "q-norm reentry checklist is complete", "timestamp_utc": ts()},
        {"validation_id": "VAL2739_5_claim_gates", "passed": gates_ok, "detail": "nonclaim/guard gates pass while all local claims remain blocked", "timestamp_utc": ts()},
        {"validation_id": "VAL2739_6_next_target", "passed": next_ok, "detail": "next target is parent q-sector action/norm extraction contract", "timestamp_utc": ts()},
        {"validation_id": "VAL2739_7_branch_outputs", "passed": branch_ok, "detail": "branch copies exist", "timestamp_utc": ts()},
        {"validation_id": "VAL2739_8_csv_parse", "passed": csv_ok, "detail": "; ".join(csv_bits), "timestamp_utc": ts()},
        {"validation_id": "VAL2739_9_formalization_untouched", "passed": formalization_ok, "detail": f"formalization-workbench recent modified-file count since script start = {formalization_recent_count()}", "timestamp_utc": ts()},
    ]
    rows.append(
        {
            "validation_id": "VAL2739_OVERALL",
            "passed": all(row["passed"] is True for row in rows),
            "detail": "2739 preserves the same-norm theorem, finds no accepted parent q-norm, demotes the finite local qnorm route to closure-only, and selects parent q-sector action extraction next",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        f"""# 2739 - Y5 R2/f(R): Parent qnorm / Cqm Dual-Pairing Closure Under AX1090

Status: `Y5_R2FR_2739_same_norm_theorem_kept_parent_qnorm_absent_local_route_closure_only`

## Private Verdict

2739 is the discipline checkpoint.

The good part survives:

`T_source_norm := sup_{{||delta q||_E<=1}} |int_W J_A delta q^A dV_e|`,

`C_qm := ||Dq[v_m]||_E`,

and therefore

`|int_W J_A Dq[v_m]^A dV_e| <= T_source_norm C_qm`

**only** if both use one parent-owned norm `E_q`.

The hard result is that no accepted parent `E_q` is found in the current evidence. Kinetic/operator, Hessian, worldtube-regulator, and quotient-reduced norm routes are all missing or conditional; the old `R_AB` kinetic route is rejected for this branch.

So this local finite q-norm route is now explicit closure-only until a parent q-sector action supplies `E_q`, `J_q`, `Dq[v_m]`, boundary terms, and arena kernels. That blocks a derived local-GR/Newton claim from this route, but it also gives us the exact reentry contract.

## Source Register

{markdown_table(data["sources"], ["source_id", "description", "source_path", "exists", "needles_present", "missing_needles", "valid_for_claim"])}

## Parent qnorm Source Hunt

{markdown_table(data["hunt"], ["hunt_id", "route", "candidate_norm", "evidence_status", "reason", "effect_if_supplied", "accepted_parent_norm", "valid_for_claim"])}

## Dual Pairing Status

{markdown_table(data["dual"], ["dual_id", "object", "contract", "current_status", "blocker", "same_norm_required", "valid_for_claim"])}

## Local Closure Demotion Gate

{markdown_table(data["demotion"], ["demotion_id", "object", "demotion", "reason", "surviving_use", "valid_for_claim"])}

## qnorm Reentry Conditions

{markdown_table(data["reentry"], ["reentry_id", "needed_input", "acceptance_requirement", "current_status", "valid_for_claim"])}

## Decision Ledger

{markdown_table(data["decisions"], ["decision_id", "decision", "because", "effect", "valid_for_claim"])}

## Claim Gates

{markdown_table(data["gates"], ["claim_gate_id", "claim", "gate_passed", "status", "claim_allowed", "valid_for_claim", "reason"])}

## Next Target

{markdown_table(data["next"], ["next_id", "status", "target_doc", "target_script", "mission", "acceptance", "forbidden", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(data["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(data["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}

## Plain-English Read

This does not kill MTS. It kills one tempting shortcut: pretending a source norm exists before the parent theory owns it. The next move is to write the exact q-sector action/norm extraction contract, then try a minimal ansatz with the failure filters already loaded.
""",
        encoding="utf-8",
    )


def main() -> None:
    ensure_dirs()
    sources = source_rows()
    hunt = hunt_rows()
    dual = dual_rows()
    demotion = demotion_rows()
    reentry = reentry_rows()
    decisions = decision_rows()
    gates = gate_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["hunt"], hunt)
    write_csv(OUTPUTS["dual"], dual)
    write_csv(OUTPUTS["demotion"], demotion)
    write_csv(OUTPUTS["reentry"], reentry)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["next"], next_target)

    write_csv(BRANCH_OUTPUTS["closure"], demotion)
    write_csv(BRANCH_OUTPUTS["reentry"], reentry)
    write_csv(BRANCH_OUTPUTS["next_queue"], next_target)
    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    validation = validation_rows(sources, hunt, dual, demotion, reentry, gates, next_target)
    write_csv(OUTPUTS["validation"], validation)

    data = {
        "sources": sources,
        "hunt": hunt,
        "dual": dual,
        "demotion": demotion,
        "reentry": reentry,
        "decisions": decisions,
        "gates": gates,
        "next": next_target,
        "branches": branches,
        "validation": validation,
    }
    write_doc(data)

    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    if not all(row["passed"] is True for row in validation):
        failed = [row for row in validation if row["passed"] is not True]
        raise SystemExit(f"2739 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
