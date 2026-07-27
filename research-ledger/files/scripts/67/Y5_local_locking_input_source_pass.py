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
DOC = ROOT / "1535-Y5-local-locking-input-source-pass.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1534_doc": ROOT / "1534-Y5-local-memory-locking-nohair-or-leakage-bound.md",
    "1534_validation": OUT / "P8_Y5_BRR545_1534_VALIDATION.csv",
    "1534_inputs": OUT / "P8_Y5_PARENT_QLOC_1534_LOCKING_INPUT_LEDGER.csv",
    "1534_nohair": OUT / "P8_Y5_PARENT_QLOC_1534_LOCAL_LOCKING_NOHAIR_THEOREM.csv",
    "1534_leakage": OUT / "P8_Y5_PARENT_QLOC_1534_QUADRATIC_LEAKAGE_BOUND_CONTRACT.csv",
    "1533_parent": OUT / "P8_Y5_PARENT_QLOC_1533_PARENT_ACTION_DOUBLE_ZERO_CONTRACT.csv",
    "1533_derivation": OUT / "P8_Y5_PARENT_QLOC_1533_DOUBLE_ZERO_DERIVATION.csv",
    "1531_kernel_audit": OUT / "P8_Y5_PARENT_QLOC_1531_KMETRIC_KERNEL_NORM_SOURCE_AUDIT.csv",
    "1531_envelope": OUT / "P8_Y5_PARENT_QLOC_1531_DELTAG_SGAMMA_BOUND_ENVELOPE.csv",
    "1529_boundary": OUT / "P8_Y5_PARENT_QLOC_1529_BOUNDARY_CERTIFICATE_AUDIT.csv",
    "positive_nohair": OUT / "P8_Y5_R10_POSITIVE_OPERATOR_NOHAIR_ATTEMPT.csv",
    "energy_identity": OUT / "P8_EXTRA_SECTOR_SILENCE_ENERGY_IDENTITY.csv",
    "gamma_expansion": OUT / "P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
    "local_lock_map": OUT / "P8_Y5_BRR545_LOCAL_LOCK_MAP.csv",
    "first_lock": OUT / "P8_Y5_BRR545_FIRST_LOCAL_LOCK_ATTEMPT.csv",
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1535_SOURCE_REGISTER.csv"
INPUT_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1535_LOCKING_INPUT_SOURCE_AUDIT.csv"
EXACT_NOHAIR_STATUS = OUT / "P8_Y5_PARENT_QLOC_1535_EXACT_NOHAIR_STATUS.csv"
LEAKAGE_SCORE_STATUS = OUT / "P8_Y5_PARENT_QLOC_1535_LEAKAGE_SCORE_STATUS.csv"
PRIORITY = OUT / "P8_Y5_PARENT_QLOC_1535_NEXT_INPUT_PRIORITY.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1535_INPUT_SOURCE_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1535_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1535_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1535_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1535_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1535"
QUAR_INPUT_AUDIT = QUARANTINE / "LOCKING_INPUT_SOURCE_AUDIT_NONCLAIM.csv"
QUAR_NOHAIR = QUARANTINE / "EXACT_NOHAIR_STATUS_NONCLAIM.csv"
QUAR_LEAKAGE = QUARANTINE / "LEAKAGE_SCORE_STATUS_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "DECISION_NONCLAIM.csv"
BRANCH_INPUT_AUDIT = BRANCH_RESIDUALS / "locking_input_source_audit_nonclaim_1535.csv"
BRANCH_NOHAIR = BRANCH_RESIDUALS / "exact_nohair_status_nonclaim_1535.csv"
BRANCH_LEAKAGE = BRANCH_RESIDUALS / "leakage_score_status_nonclaim_1535.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "locking_input_decision_nonclaim_1535.csv"


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
            "source_id": f"SRC1535_{index}_{key}",
            "source_path": rel(path),
            "exists": path.exists(),
            "purpose": "input evidence for local-locking input source pass",
            **flags(),
        }
        for index, (key, path) in enumerate(SOURCE_FILES.items())
    ]


def input_audit_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "LIA1535_0_D_m",
            "D_m",
            "positive kinetic/diffusion coefficient",
            "FORMAL_SLOT_ONLY",
            "energy identities require D_m>0, but current rows do not provide a parent value/sign for the m-sector",
            "parent kinetic term with units/sign or theorem fixing D_m>0",
            "operator",
            source_list("1534_inputs", "positive_nohair", "energy_identity"),
        ),
        (
            "LIA1535_1_Mscr",
            "M_scr^2",
            "screening/mass-gap coefficient",
            "FORMAL_SLOT_ONLY",
            "GSE798 gives schematic M_scr^2~Pi_B/(D_m tau_L) or mu_B/D_m, but Pi_B/tau_L/mu_B are not parent-sourced",
            "source-backed positive mass gap or zero-mode-safe massless branch",
            "operator",
            source_list("gamma_expansion", "1534_inputs", "positive_nohair"),
        ),
        (
            "LIA1535_2_domain",
            "A,h,n,dmu",
            "domain/measure/collar geometry",
            "BLOCKED_BY_DOMAIN_CERTIFICATE",
            "1529 found no parent compact local domain/no-flux certificate",
            "parent domain and measure plus Poincare/Sobolev constants",
            "domain",
            source_list("1529_boundary", "1534_nohair"),
        ),
        (
            "LIA1535_3_zero_mode",
            "zero-mode/gauge handling",
            "constant/gauge-mode exclusion",
            "BLOCKED_BY_ZERO_MODE_CERTIFICATE",
            "zero mode remains dangerous in Neumann/no-flux branches and was explicitly missing in 1529",
            "mean/reference/gauge condition owned by parent action",
            "domain",
            source_list("1529_boundary", "1534_nohair"),
        ),
        (
            "LIA1535_4_Jeff",
            "J_eff",
            "source+drift+history+transition-current forcing",
            "PRIMARY_SOURCE_BLOCKER",
            "GSE798 decomposes local forcing into screened source, drift, baseline, and boundary terms, but no zero theorem or H^-1 norm is live",
            "J_eff=0 theorem or finite dual norm with component decomposition",
            "source",
            source_list("gamma_expansion", "positive_nohair", "1534_nohair"),
        ),
        (
            "LIA1535_5_Bm",
            "B_m",
            "boundary/inner flux/history injection",
            "PRIMARY_BOUNDARY_BLOCKER",
            "positive no-hair attempts warn inner compact-source boundary can carry charge; 1529 found no no-flux certificate",
            "boundary no-flux theorem or finite boundary norm",
            "boundary",
            source_list("positive_nohair", "1529_boundary", "1534_nohair"),
        ),
        (
            "LIA1535_6_Cemb",
            "C_emb",
            "Poincare/Sobolev constant",
            "DOMAIN_CONSTANT_MISSING",
            "cannot convert energy norm N_lock to field amplitude U_m without a parent domain constant",
            "domain geometry or conservative analytic bound",
            "leakage",
            source_list("1534_leakage", "1529_boundary"),
        ),
        (
            "LIA1535_7_Vcurv",
            "V2_max,V3_max",
            "source potential curvature/remainder",
            "PARENT_POTENTIAL_MISSING",
            "1533 gives the clean V(m)-V(m*) contract but no actual V''/V''' bounds",
            "parent potential or finite local remainder bound",
            "leakage",
            source_list("1533_parent", "1533_derivation", "1534_leakage"),
        ),
        (
            "LIA1535_8_Kchain",
            "C_sign,L_cg,M_m,M_L",
            "Kmetric leakage conversion",
            "KMETRIC_INPUTS_MISSING",
            "1531 left sign, L_cg, M_m, and M_L nonclaim/missing, so leakage cannot be scored in delta_g S_Gamma yet",
            "same-frame Kmetric conversion factors or theorem-zero alternatives",
            "kmetric",
            source_list("1531_kernel_audit", "1531_envelope", "1534_leakage"),
        ),
        (
            "LIA1535_9_projection",
            "Pi_gamma,C_op,PPN/R10 map",
            "observable projection of leakage",
            "OBSERVABLE_PROJECTION_MISSING",
            "local-lock leakage has no live map to q_loc, PPN, or R10 scores yet",
            "projection constants and test-arena normalization",
            "projection",
            source_list("local_lock_map", "first_lock", "1534_inputs"),
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "symbol": symbol,
            "role": role,
            "status": status,
            "finding": finding,
            "missing_to_promote": missing,
            "category": category,
            "source_paths": sources,
            **flags(),
        }
        for audit_id, symbol, role, status, finding, missing, category, sources in rows
    ]


def exact_nohair_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("EH1535_0_operator", "operator positivity", "BLOCKED", "D_m and M_scr^2 not parent-signed"),
        ("EH1535_1_domain", "domain/zero-mode", "BLOCKED", "domain and zero-mode certificates missing"),
        ("EH1535_2_source", "J_eff=0", "BLOCKED", "source/drift/history forcing not zeroed"),
        ("EH1535_3_boundary", "B_m=0", "BLOCKED", "boundary/inner flux certificate missing"),
        ("EH1535_4_verdict", "delta m=0 exact no-hair", "NOT_PROVED", "exact theorem premises all remain unsigned"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": status_id,
            "requirement": requirement,
            "status": status,
            "reason": reason,
            "source_paths": source_list("1534_nohair", "1534_inputs", "positive_nohair", "1529_boundary"),
            **flags(),
        }
        for status_id, requirement, status, reason in rows
    ]


def leakage_score_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("LS1535_0_Nlock", "N_lock", "MISSING", "needs J_eff and B_m dual/boundary norms"),
        ("LS1535_1_Um", "U_m", "MISSING", "needs C_emb and N_lock"),
        ("LS1535_2_F", "F_vac/F_vac_prime leakage", "MISSING", "needs V2/V3 and U_m"),
        ("LS1535_3_Kchain", "K_chain_alg leakage", "MISSING", "needs Kmetric conversion factors"),
        ("LS1535_4_projection", "observable leakage", "MISSING", "needs projection/test normalization"),
        ("LS1535_5_verdict", "leakage scoring", "NOT_SCORE_READY", "source/boundary and Kmetric/projection inputs missing"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": status_id,
            "quantity": quantity,
            "status": status,
            "reason": reason,
            "source_paths": source_list("1534_leakage", "1531_kernel_audit", "local_lock_map"),
            **flags(),
        }
        for status_id, quantity, status, reason in rows
    ]


def priority_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PRI1535_0_first",
            "J_eff and B_m",
            "They decide exact no-hair and dominate the leakage norm N_lock.",
            "NEXT_1536_SOURCE_BOUNDARY_SILENCE_OR_BOUND",
        ),
        (
            "PRI1535_1_second",
            "domain/zero-mode constants",
            "They are required both for exact no-hair and for C_emb leakage conversion.",
            "AFTER_SOURCE_BOUNDARY",
        ),
        (
            "PRI1535_2_third",
            "D_m, M_scr^2, V2/V3",
            "They turn formal energy and Taylor bounds into source-backed numerical/theorem rows.",
            "AFTER_DOMAIN",
        ),
        (
            "PRI1535_3_parallel",
            "Kmetric/projection conversion",
            "Needed for scores, but premature until N_lock/U_m exists.",
            "PARALLEL_OR_LATER",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "priority_id": priority_id,
            "target": target,
            "rationale": rationale,
            "decision": decision,
            **flags(),
        }
        for priority_id, target, rationale, decision in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "RUN1535_0_exact_nohair",
            "attempt exact delta m=0",
            "D_m/M_scr/domain/zero-mode/J_eff=0/B_m=0",
            "operator, domain, source, and boundary inputs all missing",
            "BLOCKED_EXACT_NOHAIR_INPUTS_MISSING",
        ),
        (
            "RUN1535_1_leakage_score",
            "attempt finite leakage score",
            "N_lock,C_emb,V2/V3,Kmetric,projection",
            "N_lock cannot be computed without J_eff/B_m",
            "BLOCKED_LEAKAGE_SCORE_INPUTS_MISSING",
        ),
        (
            "RUN1535_2_double_zero_promotion",
            "promote algebraic double-zero",
            "exact lock or scored leakage",
            "neither route is live",
            "BLOCKED_DOUBLE_ZERO_NOT_LIVE",
        ),
        (
            "RUN1535_3_local_GR",
            "promote local GR/Newton/PPN",
            "all local residual and projection gates",
            "source/boundary plus hidden Kmetric kernels remain",
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
            "source_paths": source_list("1534_inputs", "1534_nohair", "1534_leakage"),
            **flags(),
        }
        for runner_id, route, required, current, result in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1535_0_input_audit", "local-locking inputs audited", "PASS_NONCLAIM", "finite input list reviewed against current source rows"),
        ("GATE1535_1_exact_nohair", "delta m=0 exact lock", "BLOCKED", "J_eff/B_m/operator/domain/zero-mode unsigned"),
        ("GATE1535_2_leakage_score", "finite leakage bound score", "BLOCKED", "N_lock/U_m/Kmetric/projection missing"),
        ("GATE1535_3_double_zero", "algebraic double-zero is live", "BLOCKED", "requires exact no-hair or scored leakage"),
        ("GATE1535_4_local_GR", "local GR/Newton/PPN recovery claim", "BLOCKED_NO_CLAIM", "local branch remains nonclaim"),
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
            "DEC1535_0_result",
            "No exact no-hair or leakage score can be promoted from current inputs.",
            "INPUTS_MISSING",
            "the theorem exists, but the source/boundary/operator/domain constants are not live.",
        ),
        (
            "DEC1535_1_primary_bottleneck",
            "Prioritize J_eff and B_m.",
            "SOURCE_BOUNDARY_FIRST",
            "they decide both exact no-hair and the leakage norm N_lock.",
        ),
        (
            "DEC1535_2_no_claim",
            "Keep double-zero and local-GR claims blocked.",
            "CLAIM_BLOCKED",
            "the route is promising but still conditional/non-score-ready.",
        ),
        (
            "DEC1535_3_next",
            "Next target is J_eff/B_m source-boundary silence or finite-bound derivation.",
            "NEXT_1536_JEFF_BM_SOURCE_BOUNDARY",
            "this is the shortest path to either exact local locking or a leakage number.",
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
            "next_id": "NEXT1535_0_1536",
            "next_target": "1536-Y5-Jeff-Bm-source-boundary-silence-or-bound.md",
            "script": "scripts/Y5_Jeff_Bm_source_boundary_silence_or_bound.py",
            "objective": "derive or bound the two primary local-lock forcing terms J_eff and B_m; split source, drift, history, transition-current, boundary, and inner-charge contributions; decide whether exact no-hair or finite N_lock can progress",
            "do_not": "do not claim source-free locking from positivity alone; do not import boundary silence without a parent certificate; do not promote local GR",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (INPUT_AUDIT, QUAR_INPUT_AUDIT),
        (EXACT_NOHAIR_STATUS, QUAR_NOHAIR),
        (LEAKAGE_SCORE_STATUS, QUAR_LEAKAGE),
        (DECISION, QUAR_DECISION),
        (INPUT_AUDIT, BRANCH_INPUT_AUDIT),
        (EXACT_NOHAIR_STATUS, BRANCH_NOHAIR),
        (LEAKAGE_SCORE_STATUS, BRANCH_LEAKAGE),
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
    audit = read_csv(INPUT_AUDIT)
    nohair = read_csv(EXACT_NOHAIR_STATUS)
    leakage = read_csv(LEAKAGE_SCORE_STATUS)
    priority = read_csv(PRIORITY)
    runners = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    required_symbols = {"D_m", "M_scr^2", "A,h,n,dmu", "zero-mode/gauge handling", "J_eff", "B_m", "C_emb", "V2_max,V3_max", "C_sign,L_cg,M_m,M_L", "Pi_gamma,C_op,PPN/R10 map"}
    symbols = {row["symbol"] for row in audit}
    checks = [
        ("VAL1535_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1535 input source paths exist"),
        ("VAL1535_1_all_inputs_audited", required_symbols.issubset(symbols), "all finite local-locking input slots audited"),
        ("VAL1535_2_primary_blockers", any(row["symbol"] == "J_eff" and row["status"] == "PRIMARY_SOURCE_BLOCKER" for row in audit) and any(row["symbol"] == "B_m" and row["status"] == "PRIMARY_BOUNDARY_BLOCKER" for row in audit), "J_eff and B_m identified as primary blockers"),
        ("VAL1535_3_exact_nohair_blocked", any(row["status_id"] == "EH1535_4_verdict" and row["status"] == "NOT_PROVED" for row in nohair), "exact no-hair remains not proved"),
        ("VAL1535_4_leakage_not_score_ready", any(row["status_id"] == "LS1535_5_verdict" and row["status"] == "NOT_SCORE_READY" for row in leakage), "leakage score remains not score-ready"),
        ("VAL1535_5_priority_next", any(row["decision"] == "NEXT_1536_SOURCE_BOUNDARY_SILENCE_OR_BOUND" for row in priority), "priority selects source/boundary silence or bound next"),
        ("VAL1535_6_runners_blocked", all(row["result"].startswith("BLOCKED") for row in runners), "all input-source runners remain blocked"),
        ("VAL1535_7_claim_gates_block", any(row["gate_id"] == "GATE1535_4_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates), "local GR claim remains blocked"),
        ("VAL1535_8_decision_next", any(row["result"] == "NEXT_1536_JEFF_BM_SOURCE_BOUNDARY" for row in decisions), "decision selects J_eff/B_m source-boundary target next"),
        ("VAL1535_9_next_target", any("1536-Y5-Jeff-Bm" in row["next_target"] for row in next_rows), "next target is J_eff/B_m source-boundary silence or bound"),
        ("VAL1535_10_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1535 CSVs parse cleanly"),
        ("VAL1535_11_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1535_12_branch_copies", all(path.exists() for path in [QUAR_INPUT_AUDIT, QUAR_NOHAIR, QUAR_LEAKAGE, QUAR_DECISION, BRANCH_INPUT_AUDIT, BRANCH_NOHAIR, BRANCH_LEAKAGE, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1535_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1535_14_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
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
            "check_id": "VAL1535_15_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1535 audits every local-locking input, identifies J_eff and B_m as the primary blockers, keeps exact no-hair/leakage/local-GR claims blocked, and selects source-boundary derivation next"
            if overall
            else "1535 validation failed; inspect failed rows before continuing",
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
    audit: list[dict[str, Any]],
    nohair: list[dict[str, Any]],
    leakage: list[dict[str, Any]],
    priority: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1535 - Local Locking Input Source Pass",
                "",
                "## Verdict",
                "- The exact local-lock theorem cannot be promoted yet: operator, domain, source, boundary, and zero-mode inputs are all unsigned.",
                "- The leakage route is also not score-ready because `N_lock`, `U_m`, Kmetric conversion, and observable projection are missing.",
                "- The primary blockers are now sharply identified as `J_eff` and `B_m`: they control both exact no-hair and the finite leakage norm.",
                "- This checkpoint makes no local-GR/Newton/PPN claim.",
                "- Next target is to derive or bound `J_eff` and `B_m` by splitting source, drift, history, transition-current, boundary, and inner-charge pieces.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "purpose"]),
                "",
                "## Locking Input Source Audit",
                md_table(audit, ["audit_id", "symbol", "role", "status", "finding", "missing_to_promote", "category"]),
                "",
                "## Exact Nohair Status",
                md_table(nohair, ["status_id", "requirement", "status", "reason"]),
                "",
                "## Leakage Score Status",
                md_table(leakage, ["status_id", "quantity", "status", "reason"]),
                "",
                "## Next Input Priority",
                md_table(priority, ["priority_id", "target", "rationale", "decision"]),
                "",
                "## Input Source Runner",
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
    audit = input_audit_rows()
    nohair = exact_nohair_status_rows()
    leakage = leakage_score_status_rows()
    priority = priority_rows()
    runners = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(INPUT_AUDIT, audit)
    write_csv(EXACT_NOHAIR_STATUS, nohair)
    write_csv(LEAKAGE_SCORE_STATUS, leakage)
    write_csv(PRIORITY, priority)
    write_csv(RUNNER, runners)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        INPUT_AUDIT,
        EXACT_NOHAIR_STATUS,
        LEAKAGE_SCORE_STATUS,
        PRIORITY,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, audit, nohair, leakage, priority, runners, gates, decisions, validation, next_rows)


if __name__ == "__main__":
    main()
