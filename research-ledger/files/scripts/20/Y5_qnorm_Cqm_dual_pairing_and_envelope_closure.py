from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1550-Y5-qnorm-Cqm-dual-pairing-and-envelope-closure.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1549_doc": ROOT / "1549-Y5-Jq-unit-dimension-and-parent-source-variation-closure.md",
    "1549_validation": OUT / "P8_Y5_BRR545_1549_VALIDATION.csv",
    "1549_next": OUT / "P8_Y5_PARENT_QLOC_1549_NEXT_TARGET.csv",
    "1549_variational": OUT / "P8_Y5_PARENT_QLOC_1549_VARIATIONAL_SOURCE_CURRENT_LAW.csv",
    "1549_unit": OUT / "P8_Y5_PARENT_QLOC_1549_UNIT_PAIRING_THEOREM_CONDITIONAL.csv",
    "1549_pairing": OUT / "P8_Y5_PARENT_QLOC_1549_CQM_PAIRING_REQUIREMENTS.csv",
    "1548_dimension": OUT / "P8_Y5_PARENT_QLOC_1548_DIMENSION_AND_NORMALIZATION_CONTRACT.csv",
    "1548_symbolic": OUT / "P8_Y5_PARENT_QLOC_1548_SHARED_SYMBOLIC_PROFILE_CANDIDATES.csv",
    "1548_arena": OUT / "P8_Y5_PARENT_QLOC_1548_ARENA_SYMBOLIC_RUNNER_NONCLAIM.csv",
    "1547_support": OUT / "P8_Y5_PARENT_QLOC_1547_SUPPORT_DOMAIN_CONVENTIONS.csv",
    "1547_guard": OUT / "P8_Y5_PARENT_QLOC_1547_NO_RETUNING_GUARD.csv",
    "1545_scg": OUT / "P8_Y5_PARENT_QLOC_1545_SCG_ENVELOPE_STATUS_NONCLAIM.csv",
    "1544_projection": OUT / "P8_Y5_PARENT_QLOC_1544_LOCAL_PROJECTION_CONTRACT.csv",
    "1544_cqm_zero": OUT / "P8_Y5_PARENT_QLOC_1544_CQM_ZERO_THEOREM_AUDIT.csv",
    "1544_cqm_finite": OUT / "P8_Y5_PARENT_QLOC_1544_CQM_FINITE_PROVENANCE_REQUIREMENTS.csv",
    "1542_cqm_source": OUT / "P8_Y5_PARENT_QLOC_1542_CQM_SOURCE_PACK_NONCLAIM.csv",
    "1541_dqvm": OUT / "P8_Y5_PARENT_QLOC_1541_DQVM_FINITE_COUPLING_ROW_NONCLAIM.csv",
    "source_owner": OUT / "P8_source_owner_parent_action_terms_CONTRACT.csv",
    "local_bound_claims": LOCAL_BOUNDS / "local_bound_claims.csv",
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1550_SOURCE_REGISTER.csv"
QNORM_CANDIDATES = OUT / "P8_Y5_PARENT_QLOC_1550_QNORM_CANDIDATE_AUDIT.csv"
DUAL_PAIRING = OUT / "P8_Y5_PARENT_QLOC_1550_DUAL_PAIRING_CONTRACT.csv"
ENVELOPE_GATE = OUT / "P8_Y5_PARENT_QLOC_1550_SCG_ENVELOPE_UNIT_GATE.csv"
NO_MIXED_NORM = OUT / "P8_Y5_PARENT_QLOC_1550_NO_MIXED_NORM_GUARD.csv"
REFUSAL_RUNNER = OUT / "P8_Y5_PARENT_QLOC_1550_QNORM_REFUSAL_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1550_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1550_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1550_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1550_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1550"
QUAR_QNORM = QUARANTINE / "QNORM_CANDIDATE_AUDIT_NONCLAIM.csv"
QUAR_DUAL = QUARANTINE / "DUAL_PAIRING_CONTRACT_NONCLAIM.csv"
QUAR_ENVELOPE = QUARANTINE / "SCG_ENVELOPE_UNIT_GATE_NONCLAIM.csv"
QUAR_GUARD = QUARANTINE / "NO_MIXED_NORM_GUARD_NONCLAIM.csv"
QUAR_RUNNER = QUARANTINE / "QNORM_REFUSAL_RUNNER_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "DECISION_NONCLAIM.csv"
BRANCH_QNORM = BRANCH_RESIDUALS / "qnorm_candidate_audit_nonclaim_1550.csv"
BRANCH_DUAL = BRANCH_RESIDUALS / "dual_pairing_contract_nonclaim_1550.csv"
BRANCH_ENVELOPE = BRANCH_RESIDUALS / "Scg_envelope_unit_gate_nonclaim_1550.csv"
BRANCH_GUARD = BRANCH_RESIDUALS / "no_mixed_norm_guard_nonclaim_1550.csv"
BRANCH_RUNNER = BRANCH_RESIDUALS / "qnorm_refusal_runner_nonclaim_1550.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "qnorm_decision_nonclaim_1550.csv"


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
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "source_id": f"SRC1550_{index}_{key}",
            "source_path": rel(path),
            "exists": path.exists(),
            "purpose": "input evidence for q-norm/C_qm dual-pairing and S_cg envelope unit closure",
            **flags(),
        }
        for index, (key, path) in enumerate(SOURCE_FILES.items())
    ]


def qnorm_candidate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "candidate_id": "QN1550_0_parent_kinetic_energy_norm",
            "candidate_norm": "||delta q||_E^2 := int_W delta q^A G_AB[q,e_obs] delta q^B dV_e",
            "parent_origin_required": "positive parent kinetic/operator metric G_AB",
            "acceptance_test": "G_AB must be sourced, positive on the allowed variation class, and shared by J_q and Dq[v_m]",
            "current_status": "MISSING_PARENT_OPERATOR_METRIC",
            "verdict": "best route if parent action supplies G_AB",
            "source_paths": source_list("1549_pairing", "1548_dimension", "source_owner"),
        },
        {
            "candidate_id": "QN1550_1_linearized_hessian_norm",
            "candidate_norm": "||delta q||_H^2 := second variation Hessian of S_parent around local branch",
            "parent_origin_required": "coercive second variation or quadratic local operator",
            "acceptance_test": "Hessian must be gauge-quotiented, positive/coercive, and not fitted to arena residuals",
            "current_status": "MISSING_PARENT_HESSIAN",
            "verdict": "strong mathematical route but currently unsigned",
            "source_paths": source_list("1549_variational", "1549_pairing", "1544_cqm_finite"),
        },
        {
            "candidate_id": "QN1550_2_regularized_worldtube_norm",
            "candidate_norm": "||delta q||_W,epsilon from compact profile regulator and worldtube measure",
            "parent_origin_required": "regulator/excision and compact support law from parent geometry",
            "acceptance_test": "same epsilon_reg and W_src must feed T_source_norm, C_qm, and all arena projections",
            "current_status": "MISSING_REGULATOR_AND_DOMAIN",
            "verdict": "possible only after worldtube regulator is parent-owned",
            "source_paths": source_list("1548_symbolic", "1547_support", "1549_pairing"),
        },
        {
            "candidate_id": "QN1550_3_arena_convenience_norm",
            "candidate_norm": "norm chosen to make R10/PPN/clock/orbital residuals small",
            "parent_origin_required": "none",
            "acceptance_test": "rejected by construction",
            "current_status": "REJECTED_SHORTCUT",
            "verdict": "would make the local branch a fitted patchwork",
            "source_paths": source_list("1547_guard", "1548_arena", "local_bound_claims"),
        },
        {
            "candidate_id": "QN1550_4_current_verdict",
            "candidate_norm": "no accepted q-norm yet",
            "parent_origin_required": "parent G_AB, Hessian, or regulator law",
            "acceptance_test": "must use one norm for both source dual norm and C_qm",
            "current_status": "NOT_SCORE_READY",
            "verdict": "S_cg envelope is structurally unit-routable but not closed",
            "source_paths": source_list("1549_unit", "1549_pairing", "1545_scg"),
        },
    ]
    return [{**{"same_parent_branch_id": BRANCH_ID}, **row, **flags()} for row in rows]


def dual_pairing_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DUAL1550_0_variation_space",
            "variation space E",
            "E is the allowed compact/local q-variation class with boundary and gauge quotient fixed",
            "MISSING_VARIATION_DOMAIN",
        ),
        (
            "DUAL1550_1_source_dual",
            "T_source_norm",
            "T_source_norm := sup_{||delta q||_E<=1} |int_W J_A delta q^A dV_e|",
            "CONDITIONAL_REQUIRES_E_AND_JQ",
        ),
        (
            "DUAL1550_2_cqm_primal",
            "C_qm",
            "C_qm := ||Dq[v_m]||_E in the same q-norm used by T_source_norm",
            "CONDITIONAL_REQUIRES_DQVM_AND_E",
        ),
        (
            "DUAL1550_3_holder_bound",
            "dual pairing inequality",
            "|int_W J_A Dq[v_m]^A dV_e| <= T_source_norm*C_qm",
            "CONDITIONAL_THEOREM",
        ),
        (
            "DUAL1550_4_envelope_insertion",
            "S_cg source term",
            "S_geom_m <= 1/2*T_source_norm*C_qm only if both terms use the same E",
            "CONDITIONAL_NOT_NUMERIC",
        ),
        (
            "DUAL1550_5_no_mixed_norm",
            "mixed norm veto",
            "using E_source for T_source_norm and E_cqm for C_qm invalidates the product bound",
            "PASS_GUARD_NONCLAIM",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "pairing_id": pairing_id,
            "object": object_name,
            "contract": contract,
            "current_status": current_status,
            "source_paths": source_list("1549_unit", "1549_pairing", "1544_projection", "1545_scg"),
            **flags(),
        }
        for pairing_id, object_name, contract, current_status in rows
    ]


def envelope_gate_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "ENV1550_0_sgeom_units",
            "S_geom_m <= 1/2*T_source_norm*C_qm",
            "unit-routable by dual pairing, not score-ready",
            "CONDITIONAL_UNIT_ROUTABLE",
            "requires accepted E, J_q, Dq[v_m], boundary treatment",
        ),
        (
            "ENV1550_1_scg_envelope",
            "S_cg_norm <= 1/2*T_source_norm*C_qm + S_direct_m + S_source_norm_extra + S_boundary_m",
            "same-norm source term can enter envelope only after other residual terms remain explicit",
            "SCHEMA_READY_NOT_COMPUTABLE",
            "S_direct_m, S_source_norm_extra, and S_boundary_m are still unsigned",
        ),
        (
            "ENV1550_2_npair",
            "N_pair <= U_B_max*S_cg_norm + C_inner*|Q_m^H|",
            "downstream lock remains blocked until S_cg_norm and first-pair inputs are computable",
            "BLOCKED_INPUTS_MISSING",
            "U_B_max, C_inner, Q_m^H, and S_cg_norm not claim-grade",
        ),
        (
            "ENV1550_3_local_tests",
            "R10/PPN/clock/orbital/local_GR projections",
            "arena projections cannot score from a conditional norm gate",
            "BLOCKED_NO_CLAIM",
            "Pi_arena kernels and legal source norm missing",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "formula": formula,
            "unit_result": unit_result,
            "current_status": current_status,
            "blocker": blocker,
            "source_paths": source_list("1545_scg", "1544_projection", "1542_cqm_source"),
            **flags(),
        }
        for gate_id, formula, unit_result, current_status, blocker in rows
    ]


def no_mixed_norm_rows() -> list[dict[str, Any]]:
    rows = [
        ("NMN1550_0_single_E", "single q-norm", "one parent-owned E must define both T_source_norm and C_qm", "PASS_GUARD_NONCLAIM"),
        ("NMN1550_1_no_arena_norm", "no arena-selected E", "R10/PPN/clock/orbital residuals cannot select the norm", "PASS_GUARD_NONCLAIM"),
        ("NMN1550_2_no_unit_patch", "no unit patching", "dimension factors cannot be inserted after the fit to repair units", "PASS_GUARD_NONCLAIM"),
        ("NMN1550_3_no_hidden_boundary_drop", "no hidden boundary drop", "boundary terms must be included or zero-proved before dual pairing is scored", "PASS_GUARD_NONCLAIM"),
        ("NMN1550_4_failure_policy", "failure policy", "if no parent E exists, the finite local branch remains a closure rather than a derived GR route", "PASS_GUARD_NONCLAIM"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "guard_id": guard_id,
            "guard": guard,
            "statement": statement,
            "current_status": current_status,
            "source_paths": source_list("1549_pairing", "1547_guard", "1545_scg"),
            **flags(),
        }
        for guard_id, guard, statement, current_status in rows
    ]


def refusal_runner_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN1550_0_parent_norm", "parent-owned q-norm E exists", "REFUSED_MISSING_PARENT_NORM", "no kinetic/operator/Hessian/regulator norm is sourced"),
        ("RUN1550_1_single_norm", "same E used for source and C_qm", "PASS_GUARD", "mixed norms are explicitly forbidden"),
        ("RUN1550_2_Jq_source", "J_q source current exists", "REFUSED_MISSING_PARENT_VARIATION", "1549 law is conditional; parent S_matter[q] missing"),
        ("RUN1550_3_Dqvm", "Dq[v_m] in E exists", "REFUSED_MISSING_DQVM_NORM", "Dq[v_m] row is nonclaim and not norm-evaluated"),
        ("RUN1550_4_holder", "Holder/dual bound legal", "PASS_CONDITIONAL_NONCLAIM", "bound is mathematically legal once E, J_q, and Dq[v_m] exist"),
        ("RUN1550_5_envelope", "S_cg envelope computable", "REFUSED_NOT_COMPUTABLE", "source term plus direct/source-extra/boundary terms remain missing"),
        ("RUN1550_6_score_status", "local arena scoring", "REFUSED_NOT_SCORE_READY", "no R10/PPN/clock/orbital/local-GR claim follows"),
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
        ("GATE1550_0_dual_pairing", "dual pairing theorem", "PASS_CONDITIONAL_NONCLAIM", "T_source_norm*C_qm product bound is legal if one parent norm E exists"),
        ("GATE1550_1_no_mixed_norm", "mixed norm veto", "PASS_GUARD", "source and C_qm cannot use different norms"),
        ("GATE1550_2_parent_norm", "parent-owned q-norm", "BLOCKED", "no accepted kinetic/Hessian/regulator norm exists"),
        ("GATE1550_3_envelope_units", "S_cg source term unit closure", "CONDITIONAL_NOT_SCORE_READY", "unit-routable but not computable"),
        ("GATE1550_4_envelope_compute", "S_cg_norm computable", "BLOCKED", "C_qm, T_source_norm, direct/source-extra/boundary inputs missing"),
        ("GATE1550_5_arena_scores", "R10/PPN/clock/orbital score readiness", "BLOCKED_NO_CLAIM", "arena kernels and legal source norm missing"),
        ("GATE1550_6_local_GR", "local GR/Newton reduction claim", "BLOCKED_NO_CLAIM", "local residual vector cannot be derived from a conditional norm gate"),
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
        ("DEC1550_0_progress", "The same-norm dual-pairing theorem is now explicit.", "CONDITIONAL_DUAL_PAIRING_WRITTEN", "the product T_source_norm*C_qm is legal only in a single parent-owned q-norm"),
        ("DEC1550_1_no_score", "The local source envelope is still not computable.", "PARENT_NORM_AND_INPUTS_MISSING", "no accepted E, J_q, Dq[v_m], or remaining envelope terms are sourced"),
        ("DEC1550_2_best_next", "Next target is parent norm acquisition from kinetic/Hessian/regulator structure.", "NEXT_1551_PARENT_QNORM_SOURCE", "derive E from the parent action or demote finite local branch to explicit closure"),
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
            "next_id": "NEXT1550_0_1551",
            "next_target": "1551-Y5-parent-qnorm-source-or-local-closure-demotion.md",
            "script": "scripts/Y5_parent_qnorm_source_or_local_closure_demotion.py",
            "objective": "hunt for a parent-owned q-norm from kinetic, Hessian, or regulator structure; if absent, write the explicit local-closure demotion gate",
            "do_not": "do not choose an arena-convenience norm; do not mix source/C_qm norms; do not claim the GR/Newton limit",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (QNORM_CANDIDATES, QUAR_QNORM),
        (DUAL_PAIRING, QUAR_DUAL),
        (ENVELOPE_GATE, QUAR_ENVELOPE),
        (NO_MIXED_NORM, QUAR_GUARD),
        (REFUSAL_RUNNER, QUAR_RUNNER),
        (DECISION, QUAR_DECISION),
        (QNORM_CANDIDATES, BRANCH_QNORM),
        (DUAL_PAIRING, BRANCH_DUAL),
        (ENVELOPE_GATE, BRANCH_ENVELOPE),
        (NO_MIXED_NORM, BRANCH_GUARD),
        (REFUSAL_RUNNER, BRANCH_RUNNER),
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
    qnorm_rows = read_csv(QNORM_CANDIDATES)
    dual_rows = read_csv(DUAL_PAIRING)
    envelope_rows = read_csv(ENVELOPE_GATE)
    guard_rows = read_csv(NO_MIXED_NORM)
    runner_rows = read_csv(REFUSAL_RUNNER)
    gate_rows = read_csv(CLAIM_GATE)
    decision_items = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    checks = [
        ("VAL1550_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1550 source paths exist"),
        ("VAL1550_1_qnorm_candidates", len(qnorm_rows) >= 5 and any(row["candidate_id"] == "QN1550_3_arena_convenience_norm" and row["current_status"] == "REJECTED_SHORTCUT" for row in qnorm_rows), "q-norm candidates audited and arena-convenience norm rejected"),
        ("VAL1550_2_dual_pairing", any(row["pairing_id"] == "DUAL1550_3_holder_bound" and row["current_status"] == "CONDITIONAL_THEOREM" for row in dual_rows), "dual pairing theorem recorded conditionally"),
        ("VAL1550_3_no_mixed_norm", any(row["guard_id"] == "NMN1550_0_single_E" and row["current_status"] == "PASS_GUARD_NONCLAIM" for row in guard_rows), "single-norm guard active"),
        ("VAL1550_4_envelope_gate", any(row["gate_id"] == "ENV1550_1_scg_envelope" and row["current_status"] == "SCHEMA_READY_NOT_COMPUTABLE" for row in envelope_rows), "S_cg envelope remains schema-ready but not computable"),
        ("VAL1550_5_runner_refuses_score", any(row["runner_id"] == "RUN1550_6_score_status" and row["current_status"] == "REFUSED_NOT_SCORE_READY" for row in runner_rows), "q-norm runner refuses arena scoring"),
        ("VAL1550_6_claim_gates_block", any(row["gate_id"] == "GATE1550_6_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in gate_rows), "local GR claim remains blocked"),
        ("VAL1550_7_decision_next", any(row["result"] == "NEXT_1551_PARENT_QNORM_SOURCE" for row in decision_items), "decision selects parent q-norm source or closure demotion next"),
        ("VAL1550_8_next_target", any("1551-Y5-parent-qnorm" in row["next_target"] for row in next_rows), "next target is parent q-norm source or closure demotion"),
        ("VAL1550_9_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1550 CSVs parse cleanly"),
        ("VAL1550_10_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1550_11_branch_copies", all(path.exists() for path in [QUAR_QNORM, QUAR_DUAL, QUAR_ENVELOPE, QUAR_GUARD, QUAR_RUNNER, QUAR_DECISION, BRANCH_QNORM, BRANCH_DUAL, BRANCH_ENVELOPE, BRANCH_GUARD, BRANCH_RUNNER, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1550_12_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1550_13_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
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
            "check_id": "VAL1550_14_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1550 writes the parent-owned q-norm audit, same-norm dual-pairing theorem, S_cg unit gate, and no-mixed-norm guard while keeping local claims blocked"
            if overall
            else "1550 validation failed; inspect failed rows before continuing",
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
    qnorm_rows: list[dict[str, Any]],
    dual_rows: list[dict[str, Any]],
    envelope_rows: list[dict[str, Any]],
    guard_rows: list[dict[str, Any]],
    runner_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    decision_items: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1550 - q-norm, C_qm Dual Pairing, and Envelope Closure",
                "",
                "## Verdict",
                "- The local finite branch now has a precise same-norm theorem: `T_source_norm` is the dual norm of `J_q`, `C_qm = ||Dq[v_m]||_E`, and `|<J_q,Dq[v_m]>| <= T_source_norm*C_qm` only in one parent-owned `q` norm `E`.",
                "- This makes the `1/2*T_source_norm*C_qm` source term unit-routable in the `S_cg_norm` envelope, but not computable.",
                "- No parent-owned kinetic, Hessian, or regulator norm has been supplied yet, so the local GR/Newton route remains blocked rather than claimed.",
                "- The key anti-cheat guard is explicit: no arena-convenience norm, no mixed source/C_qm norms, and no unit patching after fits.",
                "- Next target is to hunt for the parent-owned `q` norm; if it cannot be found, the finite local branch must be demoted to an explicit closure.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "purpose"]),
                "",
                "## q-norm Candidate Audit",
                md_table(qnorm_rows, ["candidate_id", "candidate_norm", "parent_origin_required", "current_status", "verdict"]),
                "",
                "## Dual Pairing Contract",
                md_table(dual_rows, ["pairing_id", "object", "contract", "current_status"]),
                "",
                "## S_cg Envelope Unit Gate",
                md_table(envelope_rows, ["gate_id", "formula", "unit_result", "current_status", "blocker"]),
                "",
                "## No-Mixed-Norm Guard",
                md_table(guard_rows, ["guard_id", "guard", "statement", "current_status"]),
                "",
                "## Refusal Runner",
                md_table(runner_rows, ["runner_id", "check", "current_status", "reason"]),
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
    qnorm_rows = qnorm_candidate_rows()
    dual_rows = dual_pairing_rows()
    envelope_rows = envelope_gate_rows()
    guard_rows = no_mixed_norm_rows()
    runner_rows = refusal_runner_rows()
    gate_rows = claim_gate_rows()
    decision_items = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(QNORM_CANDIDATES, qnorm_rows)
    write_csv(DUAL_PAIRING, dual_rows)
    write_csv(ENVELOPE_GATE, envelope_rows)
    write_csv(NO_MIXED_NORM, guard_rows)
    write_csv(REFUSAL_RUNNER, runner_rows)
    write_csv(CLAIM_GATE, gate_rows)
    write_csv(DECISION, decision_items)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        QNORM_CANDIDATES,
        DUAL_PAIRING,
        ENVELOPE_GATE,
        NO_MIXED_NORM,
        REFUSAL_RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, qnorm_rows, dual_rows, envelope_rows, guard_rows, runner_rows, gate_rows, decision_items, validation, next_rows)


if __name__ == "__main__":
    main()
