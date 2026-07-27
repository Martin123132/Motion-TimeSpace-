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
DOC = ROOT / "1534-Y5-local-memory-locking-nohair-or-leakage-bound.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1533_doc": ROOT / "1533-Y5-vacuum-subtracted-stationary-source-double-zero-contract.md",
    "1533_validation": OUT / "P8_Y5_BRR545_1533_VALIDATION.csv",
    "1533_locking": OUT / "P8_Y5_PARENT_QLOC_1533_LOCAL_LOCKING_REQUIREMENTS.csv",
    "1533_derivation": OUT / "P8_Y5_PARENT_QLOC_1533_DOUBLE_ZERO_DERIVATION.csv",
    "1533_parent": OUT / "P8_Y5_PARENT_QLOC_1533_PARENT_ACTION_DOUBLE_ZERO_CONTRACT.csv",
    "positive_nohair": OUT / "P8_Y5_R10_POSITIVE_OPERATOR_NOHAIR_ATTEMPT.csv",
    "energy_identity": OUT / "P8_EXTRA_SECTOR_SILENCE_ENERGY_IDENTITY.csv",
    "gamma_expansion": OUT / "P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
    "local_lock_map": OUT / "P8_Y5_BRR545_LOCAL_LOCK_MAP.csv",
    "first_lock": OUT / "P8_Y5_BRR545_FIRST_LOCAL_LOCK_ATTEMPT.csv",
    "boundary_certificate": OUT / "P8_Y5_PARENT_QLOC_1529_BOUNDARY_CERTIFICATE_AUDIT.csv",
    "kernel_audit": OUT / "P8_Y5_PARENT_QLOC_1531_KMETRIC_KERNEL_NORM_SOURCE_AUDIT.csv",
    "kernel_envelope": OUT / "P8_Y5_PARENT_QLOC_1531_DELTAG_SGAMMA_BOUND_ENVELOPE.csv",
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1534_SOURCE_REGISTER.csv"
NOHAIR_THEOREM = OUT / "P8_Y5_PARENT_QLOC_1534_LOCAL_LOCKING_NOHAIR_THEOREM.csv"
LEAKAGE_BOUND = OUT / "P8_Y5_PARENT_QLOC_1534_QUADRATIC_LEAKAGE_BOUND_CONTRACT.csv"
INPUT_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1534_LOCKING_INPUT_LEDGER.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1534_LOCKING_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1534_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1534_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1534_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1534_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1534"
QUAR_NOHAIR = QUARANTINE / "LOCAL_LOCKING_NOHAIR_THEOREM_NONCLAIM.csv"
QUAR_LEAKAGE = QUARANTINE / "QUADRATIC_LEAKAGE_BOUND_CONTRACT_NONCLAIM.csv"
QUAR_INPUTS = QUARANTINE / "LOCKING_INPUT_LEDGER_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "DECISION_NONCLAIM.csv"
BRANCH_NOHAIR = BRANCH_RESIDUALS / "local_locking_nohair_theorem_nonclaim_1534.csv"
BRANCH_LEAKAGE = BRANCH_RESIDUALS / "quadratic_leakage_bound_contract_nonclaim_1534.csv"
BRANCH_INPUTS = BRANCH_RESIDUALS / "locking_input_ledger_nonclaim_1534.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "locking_decision_nonclaim_1534.csv"


def flags() -> dict[str, bool]:
    return {
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
            "source_id": f"SRC1534_{index}_{key}",
            "source_path": rel(path),
            "exists": path.exists(),
            "purpose": "input evidence for local memory locking/no-hair or leakage-bound gate",
            **flags(),
        }
        for index, (key, path) in enumerate(SOURCE_FILES.items())
    ]


def nohair_theorem_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "NH1534_0_field",
            "Let u=delta m=m-m_* on a parent-owned compact local exterior/collar A.",
            "domain A, local branch, measure, and zero-mode convention are fixed by the parent action",
            "SETUP_UNSIGNED",
            "domain and zero-mode ownership remain live blockers",
        ),
        (
            "NH1534_1_operator",
            "Assume L_m u=(-D_m Delta_h+M_scr^2)u with D_m>0 and M_scr^2>=0 after gauge/constraint zero modes are removed.",
            "self-adjoint positive operator in the local branch",
            "CONDITIONAL_POSITIVE_OPERATOR",
            "operator sign and mass gap are not parent-signed",
        ),
        (
            "NH1534_2_energy_identity",
            "Multiplying by u and integrating gives int_A[D_m|grad u|^2+M_scr^2 u^2]=<u,J_eff>+B_m.",
            "J_eff collects source, drift, history, and transition-current terms; B_m is boundary/inner flux",
            "ENERGY_IDENTITY_WRITTEN",
            "source and boundary terms are not proven zero",
        ),
        (
            "NH1534_3_exact_nohair",
            "If J_eff=0, B_m=0, and the positive operator has no unsuppressed zero mode, then u=0.",
            "left side is a positive norm, so it can vanish only on the zero/gauge class",
            "CONDITIONAL_NOHAIR_THEOREM",
            "all premises are unsigned in the current local branch",
        ),
        (
            "NH1534_4_source_warning",
            "Positive operator alone is not enough: compact-source inner charge or boundary injection can support nonzero u.",
            "retains the 562 warning against declaring fifth-force safety from mass gap alone",
            "GUARDRAIL_RETAINED",
            "need source silence or finite source charge bound",
        ),
        (
            "NH1534_5_double_zero_impact",
            "If the theorem closes, F_vac and F_vac' are evaluated at m_* and the algebraic M_m/M_L chain is zero.",
            "combines 1533 double-zero with u=0",
            "CONDITIONAL_CHAIN_LOCK",
            "does not remove hidden K_conn/K_domain/K_boundary/delta_g C/active stress",
        ),
        (
            "NH1534_6_verdict",
            "The exact no-hair theorem is written but not live-proved.",
            "current evidence lacks parent-signed source silence, boundary/no-flux, zero-mode, and operator constants",
            "THEOREM_CONDITIONAL_NOT_CLAIMED",
            "fallback to leakage bound inputs",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": theorem_id,
            "statement": statement,
            "math_or_proof": math_or_proof,
            "status": status,
            "missing_to_promote": missing,
            "source_paths": source_list("1533_locking", "positive_nohair", "energy_identity", "boundary_certificate"),
            **flags(),
        }
        for theorem_id, statement, math_or_proof, status, missing in rows
    ]


def leakage_bound_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "LEAK1534_0_energy_norm",
            "Define E_m(u)^2=int_A[D_m|grad u|^2+M_scr^2 u^2].",
            "positive local memory energy norm",
            "CONDITIONAL_NORM_FORM",
            "D_m, M_scr, A, and zero-mode convention missing",
        ),
        (
            "LEAK1534_1_forcing_bound",
            "If |<u,J_eff>+B_m| <= N_lock E_m(u), then E_m(u) <= N_lock.",
            "Cauchy/dual-norm estimate in the energy norm",
            "CONDITIONAL_LEAKAGE_BOUND",
            "N_lock is not sourced",
        ),
        (
            "LEAK1534_2_field_bound",
            "With embedding/Poincare constant C_emb, ||u||_sup or ||u||_2 <= C_emb N_lock.",
            "turns energy leakage into field-amplitude leakage",
            "CONDITIONAL_FIELD_BOUND",
            "C_emb/domain constants missing",
        ),
        (
            "LEAK1534_3_F_bound",
            "For |u|<=U_m, |F_vac| <= 1/2 V2_max U_m^2 + 1/6 V3_max U_m^3.",
            "Taylor remainder around the stationary vacuum",
            "QUADRATIC_SOURCE_LEAKAGE_FORM",
            "V2_max, V3_max, and U_m missing",
        ),
        (
            "LEAK1534_4_Fprime_bound",
            "For |u|<=U_m, |F_vac'| <= V2_max U_m + 1/2 V3_max U_m^2.",
            "derivative leakage is linear in the field leakage",
            "LINEAR_DERIVATIVE_LEAKAGE_FORM",
            "V2_max, V3_max, and U_m missing",
        ),
        (
            "LEAK1534_5_Kchain_bound",
            "||K_chain_alg|| <= |C_sign|[L_cg^-2 |F_vac'| ||M_m|| + 2L_cg^-3 |F_vac| ||M_L||].",
            "feeds the leakage law into the 1531 Kmetric envelope",
            "CONDITIONAL_KMETRIC_LEAKAGE_FORM",
            "C_sign, L_cg lower bound, M_m, M_L, and units missing",
        ),
        (
            "LEAK1534_6_verdict",
            "If exact no-hair fails, the leakage route is still testable but not currently numeric.",
            "requires source/boundary/operator/domain/potential/Kmetric inputs",
            "NOT_SCORE_READY",
            "source the input ledger next",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "leakage_id": leakage_id,
            "bound_piece": piece,
            "formula_or_rule": formula,
            "status": status,
            "missing_to_promote": missing,
            "source_paths": source_list("1533_derivation", "gamma_expansion", "kernel_envelope", "kernel_audit"),
            **flags(),
        }
        for leakage_id, piece, formula, status, missing in rows
    ]


def input_ledger_rows() -> list[dict[str, Any]]:
    rows = [
        ("IN1534_0_D_m", "D_m", "positive kinetic/diffusion coefficient", "MISSING_PARENT_VALUE_OR_SIGN", "operator sign and units"),
        ("IN1534_1_Mscr", "M_scr^2", "screening/mass-gap coefficient", "MISSING_PARENT_VALUE_OR_SIGN", "mass gap or zero-mode-safe branch"),
        ("IN1534_2_domain", "A,h,n,dmu", "local collar/domain geometry", "MISSING_PARENT_DOMAIN_CERTIFICATE", "domain/measure/Poincare constants"),
        ("IN1534_3_zero_mode", "zero-mode/gauge handling", "exclusion of constant/gauge modes", "MISSING_ZERO_MODE_CERTIFICATE", "mean/reference/gauge condition"),
        ("IN1534_4_Jeff", "J_eff", "source+drift+history+transition-current forcing", "MISSING_SOURCE_SILENCE_OR_BOUND", "zero theorem or finite H^-1 norm"),
        ("IN1534_5_boundary", "B_m", "boundary/inner flux/history injection", "MISSING_BOUNDARY_NOFLUX_OR_BOUND", "zero theorem or finite boundary norm"),
        ("IN1534_6_Cemb", "C_emb", "Poincare/Sobolev embedding constant", "MISSING_DOMAIN_CONSTANT", "maps energy norm to field amplitude"),
        ("IN1534_7_Vcurv", "V2_max,V3_max", "potential curvature/remainder bounds", "MISSING_PARENT_POTENTIAL_BOUNDS", "quadratic/cubic leakage constants"),
        ("IN1534_8_Kchain", "C_sign,L_cg,M_m,M_L", "Kmetric chain conversion factors", "MISSING_KMETRIC_INPUTS", "propagates leakage to delta_g S_Gamma"),
        ("IN1534_9_projection", "Pi_gamma,C_op,PPN/R10 map", "observable projection of leakage", "MISSING_OBSERVABLE_PROJECTION", "turns leakage into test comparison"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "input_id": input_id,
            "symbol": symbol,
            "role": role,
            "status": status,
            "needed_for": needed_for,
            "source_paths": source_list("1533_locking", "positive_nohair", "boundary_certificate", "kernel_audit", "local_lock_map"),
            **flags(),
        }
        for input_id, symbol, role, status, needed_for in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "RUN1534_0_exact_nohair",
            "prove delta m=0",
            "D_m>0; M_scr^2>=0; J_eff=0; B_m=0; zero modes removed; parent domain",
            "energy identity written, premises unsigned",
            "BLOCKED_NOHAIR_PREMISES_UNSIGNED",
        ),
        (
            "RUN1534_1_leakage_bound",
            "bound delta m leakage",
            "N_lock, C_emb, V2/V3, Kmetric conversion factors",
            "symbolic bound form only",
            "BLOCKED_LEAKAGE_INPUTS_MISSING",
        ),
        (
            "RUN1534_2_double_zero_promotion",
            "promote double-zero chain silence",
            "exact no-hair or leakage small enough for local tests",
            "no exact lock and no numeric leakage bound",
            "BLOCKED_DOUBLE_ZERO_NOT_LIVE",
        ),
        (
            "RUN1534_3_local_GR",
            "promote GR/Newton/PPN recovery",
            "double-zero lock plus hidden kernel cleanup plus projection/source normalization",
            "multiple gates remain open",
            "BLOCKED_NO_LOCAL_GR_CLAIM",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "route": route,
            "required_inputs": required,
            "current_inputs": current,
            "result": result,
            "source_paths": source_list("1533_locking", "positive_nohair", "energy_identity", "local_lock_map"),
            **flags(),
        }
        for runner_id, route, required, current, result in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1534_0_theorem_written", "local no-hair theorem form is written", "PASS_NONCLAIM", "energy identity and exact-lock conditions are explicit"),
        ("GATE1534_1_operator", "positive operator is parent-signed", "BLOCKED", "D_m/M_scr/domain/zero mode unsigned"),
        ("GATE1534_2_source", "local forcing vanishes or is bounded", "BLOCKED", "J_eff source/drift/history terms missing"),
        ("GATE1534_3_boundary", "boundary/inner flux vanishes or is bounded", "BLOCKED", "boundary/no-flux certificate missing"),
        ("GATE1534_4_exact_lock", "delta m=0 is proved", "BLOCKED", "no-hair premises unsigned"),
        ("GATE1534_5_leakage", "finite leakage bound is score-ready", "BLOCKED", "N_lock and conversion constants missing"),
        ("GATE1534_6_double_zero", "double-zero algebraic chain is live", "BLOCKED", "requires exact lock or scored leakage"),
        ("GATE1534_7_local_GR", "local GR/Newton/PPN recovery is claimable", "BLOCKED_NO_CLAIM", "hidden kernels/projection/source-normalization remain open"),
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
        (
            "DEC1534_0_progress",
            "Keep the exact no-hair theorem as a conditional route.",
            "NOHAIR_THEOREM_FORM_WRITTEN",
            "it cleanly proves delta m=0 if source, boundary, positivity, and zero-mode clauses close.",
        ),
        (
            "DEC1534_1_fallback",
            "Keep the leakage route alive.",
            "QUADRATIC_LEAKAGE_BOUND_FORM_WRITTEN",
            "if no-hair fails, the double-zero still gives quadratic/linear leakage laws that can be tested.",
        ),
        (
            "DEC1534_2_no_claim",
            "Do not promote the double-zero or local-GR branch.",
            "CLAIM_BLOCKED",
            "the source/boundary/operator inputs are not live and hidden Kmetric kernels remain.",
        ),
        (
            "DEC1534_3_next",
            "Next target is source/boundary/operator input acquisition for local lock.",
            "NEXT_1535_LOCKING_INPUT_SOURCE_PASS",
            "the bottleneck is now a concrete finite list: D_m, M_scr, J_eff, B_m, zero mode, C_emb, V2/V3, and Kmetric conversion.",
        ),
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
            "next_id": "NEXT1534_0_1535",
            "next_target": "1535-Y5-local-locking-input-source-pass.md",
            "script": "scripts/Y5_local_locking_input_source_pass.py",
            "objective": "source or bound the finite local-locking inputs D_m, M_scr^2, J_eff, B_m, zero-mode/domain constants, V2/V3, C_emb, and Kmetric conversion factors; decide whether exact no-hair or leakage scoring can progress",
            "do_not": "do not claim delta m=0 from positivity alone; do not use unsourced boundary silence; do not promote local GR",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (NOHAIR_THEOREM, QUAR_NOHAIR),
        (LEAKAGE_BOUND, QUAR_LEAKAGE),
        (INPUT_LEDGER, QUAR_INPUTS),
        (DECISION, QUAR_DECISION),
        (NOHAIR_THEOREM, BRANCH_NOHAIR),
        (LEAKAGE_BOUND, BRANCH_LEAKAGE),
        (INPUT_LEDGER, BRANCH_INPUTS),
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
    theorem = read_csv(NOHAIR_THEOREM)
    leakage = read_csv(LEAKAGE_BOUND)
    inputs = read_csv(INPUT_LEDGER)
    runners = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    required_inputs = {"D_m", "M_scr^2", "A,h,n,dmu", "zero-mode/gauge handling", "J_eff", "B_m", "C_emb", "V2_max,V3_max", "C_sign,L_cg,M_m,M_L", "Pi_gamma,C_op,PPN/R10 map"}
    input_symbols = {row["symbol"] for row in inputs}
    checks = [
        ("VAL1534_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1534 input source paths exist"),
        ("VAL1534_1_nohair_written", any(row["theorem_id"] == "NH1534_3_exact_nohair" and row["status"] == "CONDITIONAL_NOHAIR_THEOREM" for row in theorem), "conditional exact no-hair theorem written"),
        ("VAL1534_2_positive_warning", any(row["theorem_id"] == "NH1534_4_source_warning" for row in theorem), "positive-operator-alone warning retained"),
        ("VAL1534_3_leakage_bound_written", any(row["leakage_id"] == "LEAK1534_5_Kchain_bound" for row in leakage), "quadratic leakage propagated into Kmetric chain bound"),
        ("VAL1534_4_input_ledger_complete", required_inputs.issubset(input_symbols), "all requested local-locking input slots recorded"),
        ("VAL1534_5_runners_blocked", all(row["result"].startswith("BLOCKED") for row in runners), "all exact-lock/claim runners remain blocked"),
        ("VAL1534_6_claim_gates_block", any(row["gate_id"] == "GATE1534_7_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates), "local GR claim remains blocked"),
        ("VAL1534_7_decision_next", any(row["result"] == "NEXT_1535_LOCKING_INPUT_SOURCE_PASS" for row in decisions), "decision selects local-locking input source pass next"),
        ("VAL1534_8_next_target", any("1535-Y5-local-locking-input" in row["next_target"] for row in next_rows), "next target is local-locking input source pass"),
        ("VAL1534_9_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1534 CSVs parse cleanly"),
        ("VAL1534_10_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1534_11_branch_copies", all(path.exists() for path in [QUAR_NOHAIR, QUAR_LEAKAGE, QUAR_INPUTS, QUAR_DECISION, BRANCH_NOHAIR, BRANCH_LEAKAGE, BRANCH_INPUTS, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1534_12_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1534_13_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
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
            "check_id": "VAL1534_14_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1534 writes the exact local-locking/no-hair theorem, keeps positive-operator guardrails, adds a quadratic leakage bound, keeps claims blocked, and selects input sourcing next"
            if overall
            else "1534 validation failed; inspect failed rows before continuing",
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
    theorem: list[dict[str, Any]],
    leakage: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1534 - Local Memory Locking Nohair or Leakage Bound",
                "",
                "## Verdict",
                "- The exact local-lock theorem is now explicit: a positive source-free operator with zero boundary flux and no zero mode forces `delta m=0`.",
                "- Positivity alone is not enough; source charge, drift/history forcing, and inner-boundary flux can keep local hair alive.",
                "- If exact no-hair fails, the double-zero route still gives a useful leakage hierarchy: `F_vac=O(delta m^2)` and `F_vac'=O(delta m)`.",
                "- The leakage has been propagated into the algebraic Kmetric chain, but no numeric score is possible yet.",
                "- Next target is sourcing/bounding the finite input list for exact locking or leakage scoring.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "purpose"]),
                "",
                "## Local Locking Nohair Theorem",
                md_table(theorem, ["theorem_id", "statement", "math_or_proof", "status", "missing_to_promote"]),
                "",
                "## Quadratic Leakage Bound Contract",
                md_table(leakage, ["leakage_id", "bound_piece", "formula_or_rule", "status", "missing_to_promote"]),
                "",
                "## Locking Input Ledger",
                md_table(inputs, ["input_id", "symbol", "role", "status", "needed_for"]),
                "",
                "## Locking Runner",
                md_table(runners, ["runner_id", "route", "required_inputs", "current_inputs", "result"]),
                "",
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
                "",
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "result", "rationale"]),
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
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    theorem = nohair_theorem_rows()
    leakage = leakage_bound_rows()
    inputs = input_ledger_rows()
    runners = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(NOHAIR_THEOREM, theorem)
    write_csv(LEAKAGE_BOUND, leakage)
    write_csv(INPUT_LEDGER, inputs)
    write_csv(RUNNER, runners)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        NOHAIR_THEOREM,
        LEAKAGE_BOUND,
        INPUT_LEDGER,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, theorem, leakage, inputs, runners, gates, decisions, validation, next_rows)


if __name__ == "__main__":
    main()
