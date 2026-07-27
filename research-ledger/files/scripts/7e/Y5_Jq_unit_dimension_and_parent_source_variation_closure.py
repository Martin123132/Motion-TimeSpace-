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
DOC = ROOT / "1549-Y5-Jq-unit-dimension-and-parent-source-variation-closure.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1548_doc": ROOT / "1548-Y5-shared-worldtube-profile-symbolic-runner-or-source-data-acquisition.md",
    "1548_validation": OUT / "P8_Y5_BRR545_1548_VALIDATION.csv",
    "1548_next": OUT / "P8_Y5_PARENT_QLOC_1548_NEXT_TARGET.csv",
    "1548_symbolic": OUT / "P8_Y5_PARENT_QLOC_1548_SHARED_SYMBOLIC_PROFILE_CANDIDATES.csv",
    "1548_dimension": OUT / "P8_Y5_PARENT_QLOC_1548_DIMENSION_AND_NORMALIZATION_CONTRACT.csv",
    "1548_acquisition": OUT / "P8_Y5_PARENT_QLOC_1548_SOURCE_ACQUISITION_LEDGER.csv",
    "1548_arena": OUT / "P8_Y5_PARENT_QLOC_1548_ARENA_SYMBOLIC_RUNNER_NONCLAIM.csv",
    "1547_profile": OUT / "P8_Y5_PARENT_QLOC_1547_COMPACT_PROFILE_TEMPLATE.csv",
    "1547_support": OUT / "P8_Y5_PARENT_QLOC_1547_SUPPORT_DOMAIN_CONVENTIONS.csv",
    "1547_guard": OUT / "P8_Y5_PARENT_QLOC_1547_NO_RETUNING_GUARD.csv",
    "1546_tsource_def": OUT / "P8_Y5_PARENT_QLOC_1546_TSOURCE_DEFINITION_CANDIDATES.csv",
    "1544_projection": OUT / "P8_Y5_PARENT_QLOC_1544_LOCAL_PROJECTION_CONTRACT.csv",
    "source_current": OUT / "P8_source_current_Ward_universality_CONTRACT.csv",
    "source_owner": OUT / "P8_source_owner_parent_action_terms_CONTRACT.csv",
    "source_measure_flux": OUT / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv",
    "local_bound_claims": LOCAL_BOUNDS / "local_bound_claims.csv",
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1549_SOURCE_REGISTER.csv"
VARIATIONAL_LAW = OUT / "P8_Y5_PARENT_QLOC_1549_VARIATIONAL_SOURCE_CURRENT_LAW.csv"
UNIT_LAW = OUT / "P8_Y5_PARENT_QLOC_1549_UNIT_PAIRING_THEOREM_CONDITIONAL.csv"
PAIRING_REQUIREMENTS = OUT / "P8_Y5_PARENT_QLOC_1549_CQM_PAIRING_REQUIREMENTS.csv"
REFUSAL_RUNNER = OUT / "P8_Y5_PARENT_QLOC_1549_SOURCE_VARIATION_REFUSAL_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1549_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1549_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1549_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1549_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1549"
QUAR_VARIATIONAL = QUARANTINE / "VARIATIONAL_SOURCE_CURRENT_LAW_NONCLAIM.csv"
QUAR_UNIT = QUARANTINE / "UNIT_PAIRING_THEOREM_CONDITIONAL_NONCLAIM.csv"
QUAR_PAIRING = QUARANTINE / "CQM_PAIRING_REQUIREMENTS_NONCLAIM.csv"
QUAR_RUNNER = QUARANTINE / "SOURCE_VARIATION_REFUSAL_RUNNER_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "DECISION_NONCLAIM.csv"
BRANCH_VARIATIONAL = BRANCH_RESIDUALS / "variational_source_current_law_nonclaim_1549.csv"
BRANCH_UNIT = BRANCH_RESIDUALS / "unit_pairing_theorem_conditional_nonclaim_1549.csv"
BRANCH_PAIRING = BRANCH_RESIDUALS / "Cqm_pairing_requirements_nonclaim_1549.csv"
BRANCH_RUNNER = BRANCH_RESIDUALS / "source_variation_refusal_runner_nonclaim_1549.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "source_variation_decision_nonclaim_1549.csv"


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
            "source_id": f"SRC1549_{index}_{key}",
            "source_path": rel(path),
            "exists": path.exists(),
            "purpose": "input evidence for J_q unit/dimension and parent source-variation closure",
            **flags(),
        }
        for index, (key, path) in enumerate(SOURCE_FILES.items())
    ]


def variational_source_current_rows() -> list[dict[str, Any]]:
    law_rows = [
        {
            "law_id": "VAR1549_0_variational_definition",
            "object": "J_q^A",
            "formula": "delta S_matter|_{psi,e_obs}=int_W dV_e J_A delta q^A + boundary",
            "derivation_status": "CONDITIONAL_THEOREM",
            "required_parent_input": "S_matter must explicitly depend on q or q(Phi) in the same observed frame",
            "result": "if this input exists, J_q is the variational source current dual to q",
            "failure_mode": "without owned q-dependence, J_q cannot be invented from data readouts",
            "source_paths": source_list("1548_dimension", "1548_acquisition", "source_owner"),
        },
        {
            "law_id": "VAR1549_1_derivative_couplings",
            "object": "Euler-Lagrange q-source",
            "formula": "J_A=partial L_m/partial q^A - nabla_mu(partial L_m/partial(nabla_mu q^A)) + higher-derivative terms",
            "derivation_status": "CONDITIONAL_AFTER_INTEGRATION_BY_PARTS",
            "required_parent_input": "derivative couplings and boundary terms must be declared",
            "result": "bulk current is well-defined only with boundary ledger retained",
            "failure_mode": "dropping boundary terms would smuggle source silence",
            "source_paths": source_list("1547_support", "1548_acquisition", "source_measure_flux"),
        },
        {
            "law_id": "VAR1549_2_chain_rule_from_parent_fields",
            "object": "q(Phi) chain rule",
            "formula": "delta S_matter/delta Phi^I includes (delta q^A/delta Phi^I) J_A",
            "derivation_status": "MISSING_PARENT_Q_MAP",
            "required_parent_input": "q(Phi) map, Dq, and vertical generator relation",
            "result": "can connect J_q to parent fields only after q map is signed",
            "failure_mode": "Dq[v_m] and C_qm remain formal rather than owned",
            "source_paths": source_list("1548_symbolic", "1544_projection", "source_owner"),
        },
        {
            "law_id": "VAR1549_3_Hilbert_proxy_limit",
            "object": "Hilbert stress proxy",
            "formula": "J_A=P_A^{mu_nu} T_{mu_nu} only if parent action derives P_A^{mu_nu}",
            "derivation_status": "MISSING_PARENT_COUPLING_PROJECTOR",
            "required_parent_input": "owned projector from q-variation to Hilbert stress",
            "result": "Hilbert current cannot be reused as J_q without the projector",
            "failure_mode": "otherwise WEP/GR source conservation is being smuggled into q coupling",
            "source_paths": source_list("source_current", "source_owner", "1548_symbolic"),
        },
        {
            "law_id": "VAR1549_4_no_readout_definition",
            "object": "forbidden source definition",
            "formula": "J_q != fitted GM, alpha(lambda), gamma-1, beta-1, delta ln nu, or orbital residual",
            "derivation_status": "REJECTED_SHORTCUT",
            "required_parent_input": "source current must come before arena projection",
            "result": "arena data can test J_q-derived predictions but cannot define J_q",
            "failure_mode": "using readouts would make MTS a patchwork fit rather than a field theory",
            "source_paths": source_list("1547_guard", "1548_arena", "local_bound_claims"),
        },
        {
            "law_id": "VAR1549_5_current_verdict",
            "object": "J_q status",
            "formula": "variational law exists conditionally; parent-specific J_q is still absent",
            "derivation_status": "NOT_SCORE_READY",
            "required_parent_input": "q dimension, S_matter[q], q(Phi), norm, and boundary terms",
            "result": "the route is formal and disciplined, not yet empirical",
            "failure_mode": "local branch remains blocked until parent source variation is signed",
            "source_paths": source_list("1548_dimension", "1548_acquisition", "source_owner"),
        },
    ]
    return [{**{"same_parent_branch_id": BRANCH_ID}, **row, **flags()} for row in law_rows]


def unit_pairing_rows() -> list[dict[str, Any]]:
    unit_rows = [
        ("UNIT1549_0_action_pairing", "[J_A][delta q^A][dV_e]=[S]", "from delta S=int J_A delta q^A dV_e", "CONDITIONAL_UNIT_IDENTITY"),
        ("UNIT1549_1_source_current_units", "[J_A]=[S]/([dV_e][q^A])", "valid after the parent fixes q dimension and observed-frame measure", "CONDITIONAL_MISSING_Q_DIMENSION"),
        ("UNIT1549_2_derivative_terms", "[J_A] unchanged after integration by parts", "derivative couplings move derivatives onto coefficients but preserve variational units", "CONDITIONAL_BOUNDARY_TERMS_RETAINED"),
        ("UNIT1549_3_dual_norm", "T_source_norm=sup_{||delta q||_E<=1}|int_W J_A delta q^A dV_e|", "dual norm defines source strength relative to a chosen q-norm", "CONDITIONAL_MISSING_NORM_CHOICE"),
        ("UNIT1549_4_Cqm_norm", "C_qm=||Dq[v_m]||_E", "same q-norm must be used by C_qm and T_source_norm", "CONDITIONAL_MISSING_DQ_INPUT"),
        ("UNIT1549_5_product_law", "T_source_norm*C_qm has units of the source-action variation envelope", "this is the legal unit pairing for 1/2*T_source_norm*C_qm inside S_cg_norm", "CONDITIONAL_THEOREM_NOT_NUMERIC"),
        ("UNIT1549_6_claim_status", "no numeric source strength follows", "unit law is formal until q dimension, norm, and parent variation are sourced", "NOT_SCORE_READY"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "unit_id": unit_id,
            "unit_statement": unit_statement,
            "derivation_note": derivation_note,
            "current_status": current_status,
            "source_paths": source_list("1548_dimension", "1547_support", "1546_tsource_def", "source_owner"),
            **flags(),
        }
        for unit_id, unit_statement, derivation_note, current_status in unit_rows
    ]


def pairing_requirement_rows() -> list[dict[str, Any]]:
    requirement_rows = [
        ("PAIR1549_0_q_norm", "choose or derive q-norm E", "the norm must come from the parent kinetic/energy/operator structure, not arena convenience", "MISSING_PARENT_NORM"),
        ("PAIR1549_1_variation_class", "declare allowed delta q variations", "compact support, boundary behavior, and regularity class must be fixed", "MISSING_VARIATION_DOMAIN"),
        ("PAIR1549_2_Dqvm_norm", "compute C_qm in the same norm", "Dq[v_m] must be evaluated in E and cannot use a different arena norm", "MISSING_DQVM_NORM"),
        ("PAIR1549_3_boundary_terms", "retain boundary contribution", "integration-by-parts boundary terms must be zero-proved or included as S_boundary_m", "MISSING_BOUNDARY_CLOSURE"),
        ("PAIR1549_4_dimension_closure", "derive dim(q_loc)", "q dimension must come from parent field/action term", "MISSING_PARENT_FIELD_DIMENSION"),
        ("PAIR1549_5_arena_unit_maps", "derive Pi_arena unit maps", "arena kernels convert N_pair/N_lock into observable units only after source norm is legal", "MISSING_ARENA_KERNEL_UNITS"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "pairing_id": pairing_id,
            "needed_step": needed_step,
            "acceptance_requirement": acceptance_requirement,
            "current_status": current_status,
            "source_paths": source_list("1548_dimension", "1548_arena", "1547_support", "1544_projection"),
            **flags(),
        }
        for pairing_id, needed_step, acceptance_requirement, current_status in requirement_rows
    ]


def refusal_runner_rows() -> list[dict[str, Any]]:
    runner_rows = [
        ("RUN1549_0_parent_q_dependence", "S_matter owns q-dependence", "REFUSED_MISSING_PARENT_ACTION_TERM", "source-owner contract does not yet provide explicit q dependence"),
        ("RUN1549_1_q_dimension", "q_loc dimension known", "REFUSED_MISSING_FIELD_DIMENSION", "dim(q_loc) is not parent-derived"),
        ("RUN1549_2_variational_law", "formal variational law", "PASS_CONDITIONAL_NONCLAIM", "delta S=int J delta q dV is legal only if parent q-dependence exists"),
        ("RUN1549_3_boundary_ledger", "boundary terms closed", "REFUSED_MISSING_BOUNDARY_CLOSURE", "derivative coupling boundary terms remain active"),
        ("RUN1549_4_dual_norm", "T_source/C_qm norm pairing", "REFUSED_MISSING_PARENT_NORM", "no q-norm E is selected by parent kinetic/operator structure"),
        ("RUN1549_5_readout_shortcuts", "readout-defined source rejected", "PASS_GUARD", "GM/R10/PPN/clock/orbital data cannot define J_q"),
        ("RUN1549_6_score_status", "J_q/T_source score-ready", "REFUSED_NOT_SCORE_READY", "conditional unit theorem is not a numeric or claim-grade source profile"),
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
        for runner_id, check, current_status, reason in runner_rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gate_rows = [
        ("GATE1549_0_variational_law", "variational source-current law", "PASS_CONDITIONAL_NONCLAIM", "formal law is derived if parent q-dependence exists"),
        ("GATE1549_1_unit_pairing", "unit pairing theorem", "PASS_CONDITIONAL_NONCLAIM", "T_source_norm*C_qm unit law is written but not numeric"),
        ("GATE1549_2_readout_guard", "arena readout source definitions rejected", "PASS_GUARD", "local data cannot define J_q"),
        ("GATE1549_3_parent_source", "parent-specific J_q", "BLOCKED", "explicit S_matter[q] or q(Phi) projector missing"),
        ("GATE1549_4_norm", "q-norm and C_qm closure", "BLOCKED", "parent norm/variation class is missing"),
        ("GATE1549_5_arena_scores", "R10/PPN/clock/orbital score readiness", "BLOCKED_NO_CLAIM", "arena projections need a legal source norm first"),
        ("GATE1549_6_local_GR", "local GR/Newton reduction claim", "BLOCKED_NO_CLAIM", "local branch still lacks source norm and finite residual closure"),
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
        for gate_id, claim, status, reason in gate_rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    decision_items = [
        ("DEC1549_0_progress", "The source-current unit law is now conditionally derived.", "CONDITIONAL_UNIT_THEOREM_WRITTEN", "if parent matter action owns q, J_q and T_source_norm have a clean variational definition"),
        ("DEC1549_1_blocker", "The parent-specific source current is still missing.", "PARENT_Q_DEPENDENCE_NOT_SIGNED", "source-owner inputs do not yet provide S_matter[q] or a coupling projector"),
        ("DEC1549_2_best_next", "Next target is q-norm/C_qm dual-pairing closure.", "NEXT_1550_QNORM_CQM_PAIRING", "the formal unit law needs a parent norm before any local arena can score"),
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
        for decision_id, decision, result, rationale in decision_items
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1549_0_1550",
            "next_target": "1550-Y5-qnorm-Cqm-dual-pairing-and-envelope-closure.md",
            "script": "scripts/Y5_qnorm_Cqm_dual_pairing_and_envelope_closure.py",
            "objective": "derive or select the parent-owned q-norm used by both T_source_norm and C_qm, then state whether the S_cg envelope becomes unit-closed or remains a missing-input closure",
            "do_not": "do not choose a norm because it makes an arena pass; do not mix different norms for source and C_qm; do not claim local tests",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (VARIATIONAL_LAW, QUAR_VARIATIONAL),
        (UNIT_LAW, QUAR_UNIT),
        (PAIRING_REQUIREMENTS, QUAR_PAIRING),
        (REFUSAL_RUNNER, QUAR_RUNNER),
        (DECISION, QUAR_DECISION),
        (VARIATIONAL_LAW, BRANCH_VARIATIONAL),
        (UNIT_LAW, BRANCH_UNIT),
        (PAIRING_REQUIREMENTS, BRANCH_PAIRING),
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
    variational_rows = read_csv(VARIATIONAL_LAW)
    unit_rows = read_csv(UNIT_LAW)
    pairing_rows = read_csv(PAIRING_REQUIREMENTS)
    runner_rows = read_csv(REFUSAL_RUNNER)
    gate_rows = read_csv(CLAIM_GATE)
    decision_items = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    checks = [
        ("VAL1549_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1549 source paths exist"),
        ("VAL1549_1_variational_law", any(row["law_id"] == "VAR1549_0_variational_definition" and row["derivation_status"] == "CONDITIONAL_THEOREM" for row in variational_rows), "conditional variational source-current law written"),
        ("VAL1549_2_readout_rejected", any(row["law_id"] == "VAR1549_4_no_readout_definition" and row["derivation_status"] == "REJECTED_SHORTCUT" for row in variational_rows), "readout-defined J_q shortcuts rejected"),
        ("VAL1549_3_unit_pairing", any(row["unit_id"] == "UNIT1549_5_product_law" and row["current_status"] == "CONDITIONAL_THEOREM_NOT_NUMERIC" for row in unit_rows), "T_source_norm*C_qm unit law recorded as conditional"),
        ("VAL1549_4_pairing_requirements", len(pairing_rows) >= 6 and any(row["pairing_id"] == "PAIR1549_0_q_norm" for row in pairing_rows), "q-norm/C_qm pairing requirements written"),
        ("VAL1549_5_runner_refuses_score", any(row["runner_id"] == "RUN1549_6_score_status" and row["current_status"] == "REFUSED_NOT_SCORE_READY" for row in runner_rows), "source variation runner refuses scoring"),
        ("VAL1549_6_claim_gates_block", any(row["gate_id"] == "GATE1549_6_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in gate_rows), "local GR claim remains blocked"),
        ("VAL1549_7_decision_next", any(row["result"] == "NEXT_1550_QNORM_CQM_PAIRING" for row in decision_items), "decision selects q-norm/C_qm dual-pairing next"),
        ("VAL1549_8_next_target", any("1550-Y5-qnorm-Cqm" in row["next_target"] for row in next_rows), "next target is q-norm C_qm dual-pairing closure"),
        ("VAL1549_9_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1549 CSVs parse cleanly"),
        ("VAL1549_10_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1549_11_branch_copies", all(path.exists() for path in [QUAR_VARIATIONAL, QUAR_UNIT, QUAR_PAIRING, QUAR_RUNNER, QUAR_DECISION, BRANCH_VARIATIONAL, BRANCH_UNIT, BRANCH_PAIRING, BRANCH_RUNNER, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1549_12_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1549_13_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
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
            "check_id": "VAL1549_14_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1549 conditionally derives J_q and T_source_norm units from parent variation, rejects readout-defined source currents, and selects q-norm/C_qm closure next"
            if overall
            else "1549 validation failed; inspect failed rows before continuing",
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
    variational_rows: list[dict[str, Any]],
    unit_rows: list[dict[str, Any]],
    pairing_rows: list[dict[str, Any]],
    runner_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    decision_items: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1549 - J_q Unit Dimension and Parent Source Variation Closure",
                "",
                "## Verdict",
                "- The exact variational unit law is now written: if `S_matter` owns `q`, then `delta S_matter = int J_q delta q dV` defines the source current dual to `q`.",
                "- This gives the clean conditional unit rule `[J_q][q][dV]=[S]` and makes `T_source_norm*C_qm` a legal source-action variation envelope when both use the same `q` norm.",
                "- The law is not yet a claim because the parent-specific `S_matter[q]`, `q(Phi)` map, `dim(q_loc)`, boundary terms, and `q` norm are still unsigned.",
                "- Arena readouts such as orbital `GM`, R10 `alpha(lambda)`, PPN residuals, or clock calibration are explicitly rejected as definitions of `J_q`.",
                "- Next target is the parent-owned `q` norm and `C_qm` dual-pairing closure.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "purpose"]),
                "",
                "## Variational Source Current Law",
                md_table(variational_rows, ["law_id", "object", "formula", "derivation_status", "required_parent_input", "failure_mode"]),
                "",
                "## Unit Pairing Theorem",
                md_table(unit_rows, ["unit_id", "unit_statement", "derivation_note", "current_status"]),
                "",
                "## C_qm Pairing Requirements",
                md_table(pairing_rows, ["pairing_id", "needed_step", "acceptance_requirement", "current_status"]),
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
    variational_rows = variational_source_current_rows()
    unit_rows = unit_pairing_rows()
    pairing_rows = pairing_requirement_rows()
    runner_rows = refusal_runner_rows()
    gate_rows = claim_gate_rows()
    decision_items = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(VARIATIONAL_LAW, variational_rows)
    write_csv(UNIT_LAW, unit_rows)
    write_csv(PAIRING_REQUIREMENTS, pairing_rows)
    write_csv(REFUSAL_RUNNER, runner_rows)
    write_csv(CLAIM_GATE, gate_rows)
    write_csv(DECISION, decision_items)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        VARIATIONAL_LAW,
        UNIT_LAW,
        PAIRING_REQUIREMENTS,
        REFUSAL_RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, variational_rows, unit_rows, pairing_rows, runner_rows, gate_rows, decision_items, validation, next_rows)


if __name__ == "__main__":
    main()
