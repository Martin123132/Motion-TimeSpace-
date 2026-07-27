from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "2221-Y5-R2FR-delta-g-SGamma-Kmetric-kernel-norm-source-pass.md"
BRANCH_ID = "MTS_R2FR_PARENT_QLOC_KMETRIC_KERNEL_BRIDGE_2221"
START_TS = datetime.now(timezone.utc).timestamp()


SOURCE_FILES = {
    "2220_doc": ROOT / "2220-Y5-R2FR-tracefree-improvement-Khat-birth-certificate-or-DeltaKhat-coefficient-runner.md",
    "2220_validation": OUT / "P8_Y5_BRR545_2220_VALIDATION.csv",
    "2220_envelope": OUT / "P8_Y5_PARENT_QLOC_2220_DELTAKHAT_COEFFICIENT_ENVELOPE.csv",
    "1531_doc": ROOT / "1531-Y5-delta-g-SGamma-Kmetric-kernel-norm-source-pass.md",
    "1531_validation": OUT / "P8_Y5_BRR545_1531_VALIDATION.csv",
    "1531_kernel_audit": OUT / "P8_Y5_PARENT_QLOC_1531_KMETRIC_KERNEL_NORM_SOURCE_AUDIT.csv",
    "1531_envelope": OUT / "P8_Y5_PARENT_QLOC_1531_DELTAG_SGAMMA_BOUND_ENVELOPE.csv",
    "1531_zero": OUT / "P8_Y5_PARENT_QLOC_1531_ZERO_ROUTE_AUDIT.csv",
    "1531_runner": OUT / "P8_Y5_PARENT_QLOC_1531_KERNEL_NORM_RUNNER.csv",
    "1532_doc": ROOT / "1532-Y5-Lcg-parent-ownership-and-fixed-scale-silence-audit.md",
    "1532_validation": OUT / "P8_Y5_BRR545_1532_VALIDATION.csv",
    "1532_lcg_audit": OUT / "P8_Y5_PARENT_QLOC_1532_LCG_OWNERSHIP_AUDIT.csv",
    "1532_double_zero_contract": OUT / "P8_Y5_PARENT_QLOC_1532_DOUBLE_ZERO_SOURCE_CONTRACT.csv",
    "1533_doc": ROOT / "1533-Y5-vacuum-subtracted-stationary-source-double-zero-contract.md",
    "1533_validation": OUT / "P8_Y5_BRR545_1533_VALIDATION.csv",
    "1533_parent_contract": OUT / "P8_Y5_PARENT_QLOC_1533_PARENT_ACTION_DOUBLE_ZERO_CONTRACT.csv",
    "1533_derivation": OUT / "P8_Y5_PARENT_QLOC_1533_DOUBLE_ZERO_DERIVATION.csv",
    "1533_locking": OUT / "P8_Y5_PARENT_QLOC_1533_LOCAL_LOCKING_REQUIREMENTS.csv",
    "1534_doc": ROOT / "1534-Y5-local-memory-locking-nohair-or-leakage-bound.md",
    "1534_validation": OUT / "P8_Y5_BRR545_1534_VALIDATION.csv",
    "1534_nohair": OUT / "P8_Y5_PARENT_QLOC_1534_LOCAL_LOCKING_NOHAIR_THEOREM.csv",
    "1534_leakage": OUT / "P8_Y5_PARENT_QLOC_1534_QUADRATIC_LEAKAGE_BOUND_CONTRACT.csv",
    "1534_inputs": OUT / "P8_Y5_PARENT_QLOC_1534_LOCKING_INPUT_LEDGER.csv",
    "1535_doc": ROOT / "1535-Y5-local-locking-input-source-pass.md",
    "1535_validation": OUT / "P8_Y5_BRR545_1535_VALIDATION.csv",
    "1535_input_audit": OUT / "P8_Y5_PARENT_QLOC_1535_LOCKING_INPUT_SOURCE_AUDIT.csv",
    "1535_priority": OUT / "P8_Y5_PARENT_QLOC_1535_NEXT_INPUT_PRIORITY.csv",
    "1536_doc": ROOT / "1536-Y5-Jeff-Bm-source-boundary-silence-or-bound.md",
    "1536_validation": OUT / "P8_Y5_BRR545_1536_VALIDATION.csv",
    "1536_jeff": OUT / "P8_Y5_PARENT_QLOC_1536_JEFF_COMPONENT_SPLIT.csv",
    "1536_bm": OUT / "P8_Y5_PARENT_QLOC_1536_BM_COMPONENT_SPLIT.csv",
    "1536_nlock": OUT / "P8_Y5_PARENT_QLOC_1536_NLOCK_ENVELOPE_CONTRACT.csv",
    "1537_doc": ROOT / "1537-Y5-Jeff-Bm-component-norm-input-pack.md",
    "1538_doc": ROOT / "1538-Y5-source-support-and-inner-charge-theorem-or-bound.md",
    "1539_doc": ROOT / "1539-Y5-source-support-power-and-inner-charge-input-acquisition.md",
}


SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_2221_SOURCE_REGISTER.csv"
CHAIN_AUDIT = OUT / "P8_Y5_PARENT_QLOC_2221_EXISTING_CHAIN_AUDIT.csv"
KERNEL_AUDIT = OUT / "P8_Y5_PARENT_QLOC_2221_KMETRIC_KERNEL_NORM_SOURCE_AUDIT.csv"
REDUCTION_LEDGER = OUT / "P8_Y5_PARENT_QLOC_2221_ALGEBRAIC_CHAIN_REDUCTION_LEDGER.csv"
LOCKING_HANDOFF = OUT / "P8_Y5_PARENT_QLOC_2221_LOCAL_LOCKING_HANDOFF.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_2221_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_2221_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_2221_NEXT_TARGET.csv"
BRANCH_COPIES = OUT / "P8_Y5_PARENT_QLOC_2221_BRANCH_COPIES.csv"
VALIDATION = OUT / "P8_Y5_BRR545_2221_VALIDATION.csv"


COPY_TARGETS = {
    "queue": QUEUE / "JR2221_DELTAG_SGAMMA_KMETRIC_KERNEL_FRONTIER_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "delta_g_sgamma_kmetric_kernel_frontier_nonclaim_2221.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_DELTAG_SGAMMA_KMETRIC_KERNEL_FRONTIER_2221_NONCLAIM.csv",
}


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


def validation_pass(path: Path) -> bool:
    if not path.exists():
        return False
    rows = read_csv(path)
    if not rows:
        return False
    id_key = "check_id" if "check_id" in rows[0] else "validation_id"
    result_key = "result" if "result" in rows[0] else "status"
    overall_rows = [row for row in rows if "overall" in row.get(id_key, "").lower()]
    if overall_rows:
        return all(row.get(result_key) == "PASS" for row in overall_rows)
    return all(row.get(result_key) == "PASS" for row in rows)


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    keys = ["score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed", "passes_for_claim"]
    for path in paths:
        for row in read_csv(path):
            for key in keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_2221_artifacts_absent() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(path.is_file() and "2221" in path.name for path in FORMALIZATION.rglob("*"))


def formalization_untouched_since_start() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(path.is_file() and path.stat().st_mtime >= START_TS for path in FORMALIZATION.rglob("*"))


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (key, path) in enumerate(SOURCE_FILES.items()):
        role = "input evidence"
        if key.startswith("2220"):
            role = "current R2FR handoff selecting Kmetric kernel norm pass"
        elif key.startswith("1531"):
            role = "existing kernel norm pass matching 2220 selected blocker"
        elif key.startswith(("1532", "1533")):
            role = "existing algebraic chain/double-zero follow-up"
        elif key.startswith(("1534", "1535", "1536")):
            role = "existing local-locking and source-boundary follow-up"
        elif key.startswith(("1537", "1538", "1539")):
            role = "known later frontier to inspect before new derivation"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": f"SRC2221_{index}_{key}",
                "source_path": rel(path),
                "path_exists": path.exists(),
                "validation_overall_pass": validation_pass(path) if key.endswith("validation") else "",
                "role": role,
                **flags(),
            }
        )
    return rows


def chain_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "CHAIN2221_0_1531",
            "1531 kernel pass",
            "delta_g S_Gamma reduced to explicit Kmetric kernels; M_m partial fixed-field route; L_cg and hidden kernels open",
            "USE_AS_CURRENT_2221_BASE",
            "do not rerun blind duplicate; bridge into current numbering",
            "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1531_KMETRIC_KERNEL_NORM_SOURCE_AUDIT.csv",
        ),
        (
            "CHAIN2221_1_1532",
            "1532 L_cg ownership",
            "fixed L_cg is sufficient but unsigned; better route is F(m_*)=0 plus F_prime(m_*)=0",
            "USE_AS_ALGEBRAIC_REDUCTION",
            "do not use F_prime alone to erase the L_cg term",
            "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1532_LCG_OWNERSHIP_AUDIT.csv",
        ),
        (
            "CHAIN2221_2_1533",
            "1533 double-zero contract",
            "F_vac(m)=V(m)-V(m_*) gives conditional F_vac(m_*)=0 and F_vac_prime(m_*)=0",
            "CONDITIONAL_THEOREM_TARGET",
            "parent V, local lock, and hidden kernels still unsigned",
            "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1533_DOUBLE_ZERO_DERIVATION.csv",
        ),
        (
            "CHAIN2221_3_1534",
            "1534 local no-hair/leakage",
            "positive source-free operator with zero boundary flux and no zero mode forces delta m=0; fallback leakage laws are written",
            "USE_AS_LOCKING_GATE",
            "positivity alone is not enough",
            "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1534_LOCAL_LOCKING_NOHAIR_THEOREM.csv",
        ),
        (
            "CHAIN2221_4_1535",
            "1535 locking input pass",
            "finite input list identified; J_eff and B_m are primary blockers",
            "USE_AS_INPUT_PRIORITY",
            "no exact no-hair or leakage score from missing inputs",
            "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1535_LOCKING_INPUT_SOURCE_AUDIT.csv",
        ),
        (
            "CHAIN2221_5_1536",
            "1536 J_eff/B_m split",
            "source, drift, history, transition-current, boundary, inner-charge, zero-mode and domain pieces split; N_lock absolute envelope written",
            "USE_AS_CURRENT_LOCAL_LOCK_FRONTIER",
            "no cancellation between source and boundary pieces",
            "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1536_NLOCK_ENVELOPE_CONTRACT.csv",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "chain_id": chain_id,
            "checkpoint": checkpoint,
            "finding": finding,
            "current_2221_use": use,
            "guardrail": guardrail,
            "source_path": source_path,
            **flags(),
        }
        for chain_id, checkpoint, finding, use, guardrail, source_path in entries
    ]


def kernel_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "KNA2221_0_delta_g_SGamma",
            "delta_g S_Gamma",
            "shared residual controlling lambda_phi stress and Delta_Khat computability",
            "REDUCED_TO_KERNEL_PACK_NOT_BOUND",
            "1531 confirms the exact pack; 2220 confirms this is the current shared blocker",
            "theorem-zero or finite norm for every live kernel",
        ),
        (
            "KNA2221_1_M_m",
            "M_m",
            "m-channel metric response",
            "PARTIAL_CONDITIONAL_ZERO",
            "can vanish if m is parent-owned independent scalar held fixed in same Hilbert variation; active stress and readout branches remain",
            "parent choice of m plus exclusion/bound of active memory stress",
        ),
        (
            "KNA2221_2_M_L",
            "M_L",
            "L_cg metric response",
            "ALGEBRAIC_COEFFICIENT_CAN_BE_CONDITIONALLY_ZEROED",
            "1532/1533 show F_vac(m_*)=0 deletes this coefficient without fixed-scale axiom, but only if local lock holds",
            "parent V, vacuum subtraction, and local locking or leakage bound",
        ),
        (
            "KNA2221_3_F_Fprime",
            "F_vac and F_vac_prime",
            "source coefficients multiplying M_L and M_m",
            "DOUBLE_ZERO_CONDITIONAL_NOT_LIVE",
            "stationary vacuum subtraction gives clean algebraic double-zero; not yet parent-signed/live",
            "actual parent potential V(m), stable vacuum m_*, and same-branch adoption",
        ),
        (
            "KNA2221_4_local_lock",
            "delta m",
            "whether the local exterior evaluates F_vac at m_*",
            "NOHAIR_CONDITIONAL_LEAKAGE_FORMULA_READY",
            "1534 writes exact no-hair theorem and quadratic leakage fallback",
            "D_m, M_scr, J_eff, B_m, zero-mode, domain and source/boundary controls",
        ),
        (
            "KNA2221_5_JB",
            "J_eff and B_m",
            "source/boundary forcing of local memory hair",
            "COMPONENT_SPLIT_NO_NORMS",
            "1536 splits the forcing and writes N_lock=N_J+N_B as an absolute envelope",
            "component norms or zero theorems, starting with N_src and N_inner",
        ),
        (
            "KNA2221_6_hidden",
            "K_conn, K_domain, K_boundary, K_C",
            "hidden connection/domain/boundary/background metric-response kernels",
            "OPEN_RETAINED_RESIDUALS",
            "double-zero only attacks algebraic M_m/M_L terms, not hidden kernels",
            "separate zero theorem or finite absolute norm for each hidden kernel",
        ),
        (
            "KNA2221_7_units_projection",
            "operator norm, units, Pi_gamma/C_op/PPN/R10 map",
            "convert formal residual into arena scores",
            "MISSING_SCORE_MAP",
            "source-bound local residual still lacks same-frame norm and observable projection",
            "single tensor norm, volume measure, local frame, and test-arena normalization",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "quantity": quantity,
            "role": role,
            "status": status,
            "finding": finding,
            "missing_to_promote": missing,
            **flags(),
        }
        for audit_id, quantity, role, status, finding, missing in entries
    ]


def reduction_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "RED2221_0_base_envelope",
            "||delta_g S_Gamma|| <= (2/3)(L_cg^-2|F'| ||M_m|| + 2L_cg^-3|F| ||M_L|| + ||K_conn|| + ||K_domain|| + ||K_boundary|| + ||K_C||)",
            "base no-cancellation envelope after importing the 1531 background guard",
            "FORMULA_READY_NOT_NUMERIC",
            "M_m/M_L/hidden kernels and K_C remain unbounded",
        ),
        (
            "RED2221_1_double_zero",
            "F_vac(m)=V(m)-V(m_*), V'(m_*)=0 => F_vac(m_*)=0 and F_vac_prime(m_*)=0",
            "deletes algebraic M_L and M_m coefficients at the locked vacuum",
            "CONDITIONAL_DERIVATION",
            "parent V and local locking are unsigned",
        ),
        (
            "RED2221_2_leakage",
            "F_vac=O(delta m^2), F_vac_prime=O(delta m)",
            "if exact lock fails, algebraic leakage is quadratic/linear rather than arbitrary",
            "BOUND_ROUTE_WRITTEN",
            "U_m, V2/V3, Kmetric conversion, and projection missing",
        ),
        (
            "RED2221_3_Nlock",
            "E_m(delta m) <= N_lock := N_J + N_B",
            "source-boundary forcing controls leakage amplitude",
            "ABSOLUTE_ENVELOPE_NOT_SCORED",
            "component norms for J_eff/B_m missing",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "ledger_id": ledger_id,
            "formula_or_rule": formula,
            "meaning": meaning,
            "status": status,
            "missing_to_promote": missing,
            **flags(),
        }
        for ledger_id, formula, meaning, status, missing in entries
    ]


def locking_rows() -> list[dict[str, Any]]:
    entries = [
        ("LH2221_0_exact_lock", "delta m=0", "requires positive operator, source silence, boundary silence, zero-mode removal, parent domain", "NOT_PROVED"),
        ("LH2221_1_leakage_score", "finite delta m leakage", "requires N_lock, domain embedding, potential curvature, Kmetric conversion and projection", "NOT_SCORE_READY"),
        ("LH2221_2_primary_forcing", "J_eff", "split into screened source, drifts, selector, history, transition and source-current pieces", "SPLIT_NO_ZERO_OR_BOUND"),
        ("LH2221_3_primary_boundary", "B_m", "split into inner charge, no-flux, zero-mode, outer, history and domain-motion pieces", "SPLIT_NO_ZERO_OR_BOUND"),
        ("LH2221_4_first_live_targets", "N_src and N_inner", "source-support norm and inner boundary charge are the first concrete norms named by the existing chain", "INSPECT_EXISTING_1537_1539_BEFORE_NEW_WORK"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "handoff_id": handoff_id,
            "object": obj,
            "contract": contract,
            "status": status,
            **flags(),
        }
        for handoff_id, obj, contract, status in entries
    ]


def claim_rows() -> list[dict[str, Any]]:
    entries = [
        ("CG2221_0_bridge", "2221 kernel pass completed by bridge/audit", "PASS_NONCLAIM", "existing 1531 pass is valid and now attached to the current 2220 handoff"),
        ("CG2221_1_delta_g_SGamma", "delta_g S_Gamma zero or finite bound", "BLOCKED_NONCLAIM", "kernel pack and local-lock forcing lack zero theorem/numeric norms"),
        ("CG2221_2_double_zero", "algebraic M_m/M_L chain deletion", "BLOCKED_NONCLAIM", "double-zero and local lock are conditional, not live"),
        ("CG2221_3_local_lock", "local memory no-hair or scored leakage", "BLOCKED_NONCLAIM", "J_eff/B_m component norms missing"),
        ("CG2221_4_hidden_kernels", "hidden Kmetric kernels zero/bounded", "BLOCKED_NONCLAIM", "K_conn/K_domain/K_boundary/K_C remain separate residuals"),
        ("CG2221_5_local_GR", "derived local GR/Newton/PPN recovery", "BLOCKED_NO_CLAIM", "q_loc residual branch is not closed"),
        ("CG2221_6_GitHub", "public/GitHub update", "BLOCKED_NONCLAIM", "private derivation branch remains mid-proof"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for gate_id, claim, status, reason in entries
    ]


def decision_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "DEC2221_0_no_duplication",
            "Do not redo 1531 as if it did not exist.",
            "BRIDGE_EXISTING_KERNEL_PASS",
            "the exact 2220 target already has a valid older pass; the useful move is continuity, not wheel-spinning",
        ),
        (
            "DEC2221_1_real_gain",
            "The route is better than a bare fixed-scale axiom.",
            "DOUBLE_ZERO_PLUS_LOCKING_IS_BEST_ROUTE",
            "F_vac(m_*)=F_vac_prime(m_*)=0 can silence algebraic M_m/M_L coefficients if parent V and local lock close",
        ),
        (
            "DEC2221_2_current_blocker",
            "The immediate physical blocker is source-boundary hair.",
            "JEFF_BM_COMPONENT_NORMS_FIRST",
            "without J_eff/B_m zero or N_lock, the double-zero cannot become a live local branch",
        ),
        (
            "DEC2221_3_no_claim",
            "Keep local GR blocked but not dead.",
            "CLAIM_BLOCKED_ROUTE_ALIVE",
            "we now know exactly what must be zeroed or bounded before PPN/R10 scoring makes sense",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "result": result,
            "rationale": rationale,
            **flags(),
        }
        for decision_id, decision, result, rationale in entries
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_id": "NEXT2221_0_2222",
            "target_file": "2222-Y5-R2FR-current-local-frontier-import-and-Jsrc-Binner-source-bound-gate.md",
            "target_script": "scripts/Y5_R2FR_current_local_frontier_import_and_Jsrc_Binner_source_bound_gate_2222.py",
            "objective": "inspect existing 1537-1539 frontier, import any valid source-support/inner-charge norm progress into the current R2FR numbering, then decide whether N_src=||U_B S_cg|| or N_inner can be theorem-zero/bounded",
            "success_condition": "a source-backed zero theorem or finite nonclaim bound exists for at least one first-priority J/B component, or the route is explicitly demoted to retained residual inputs",
            "do_not": "do not duplicate old checkpoints; do not claim local GR; do not cancel J_eff against B_m; do not erase hidden Kmetric kernels",
            **flags(),
        }
    ]


def copy_outputs() -> list[dict[str, Any]]:
    copied: list[dict[str, Any]] = []
    for copy_id, destination in COPY_TARGETS.items():
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(KERNEL_AUDIT, destination)
        copied.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": copy_id,
                "source_path": rel(KERNEL_AUDIT),
                "target_path": rel(destination),
                "copied": destination.exists(),
                "parse_ok": parse_csv(destination),
                **flags(),
            }
        )
    return copied


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    chain = read_csv(CHAIN_AUDIT)
    kernel = read_csv(KERNEL_AUDIT)
    reduction = read_csv(REDUCTION_LEDGER)
    locking = read_csv(LOCKING_HANDOFF)
    claims = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_target = read_csv(NEXT_TARGET)
    copies = read_csv(BRANCH_COPIES)
    required_kernel_statuses = {"KNA2221_1_M_m", "KNA2221_2_M_L", "KNA2221_6_hidden", "KNA2221_7_units_projection"}
    checks = [
        ("VAL2221_00_sources_exist", all(row["path_exists"] == "True" for row in sources), "all cited 2221 source paths exist"),
        ("VAL2221_01_prior_validations", all(row["validation_overall_pass"] in {"", "True"} for row in sources), "all imported validation files pass overall"),
        ("VAL2221_02_chain_bridge", len(chain) == 6 and any(row["checkpoint"].startswith("1536") for row in chain), "1531-1536 chain bridged into current 2221 handoff"),
        ("VAL2221_03_kernel_slots", required_kernel_statuses.issubset({row["audit_id"] for row in kernel}), "critical Kmetric slots retained"),
        ("VAL2221_04_double_zero", any(row["ledger_id"] == "RED2221_1_double_zero" for row in reduction), "double-zero algebraic route recorded as conditional"),
        ("VAL2221_05_locking_frontier", any(row["handoff_id"] == "LH2221_4_first_live_targets" for row in locking), "first source-boundary targets identified"),
        ("VAL2221_06_claims_blocked", any(row["gate_id"] == "CG2221_5_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in claims), "local GR/Newton claim remains blocked"),
        ("VAL2221_07_decision_no_duplication", any(row["result"] == "BRIDGE_EXISTING_KERNEL_PASS" for row in decisions), "decision avoids duplicating 1531"),
        ("VAL2221_08_next_target", any("2222-Y5-R2FR-current-local-frontier" in row["target_file"] for row in next_target), "next target imports latest local frontier before new derivation"),
        ("VAL2221_09_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 2221 CSVs parse cleanly"),
        ("VAL2221_10_claim_flags_false", generated_flags_false(generated_csvs), "all generated flags remain nonclaim"),
        ("VAL2221_11_branch_copies", all(row["copied"] == "True" and row["parse_ok"] == "True" for row in copies), "branch copies written and parse"),
        ("VAL2221_12_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL2221_13_formalization_no_2221", formalization_2221_artifacts_absent(), "formalization-workbench has no 2221 artifacts"),
        ("VAL2221_14_formalization_untouched", formalization_untouched_since_start(), "formalization-workbench untouched during 2221 run"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            **flags(),
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2221_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "2221 bridges the existing 1531 kernel pass into the current R2FR branch, preserves the conditional double-zero/nohair route, keeps local-GR claims blocked, and selects source-boundary norm frontier import next"
            if overall
            else "2221 validation failed; inspect failed rows before continuing",
            **flags(),
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns)
            + " |"
        )
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, Any]],
    chain: list[dict[str, Any]],
    kernel: list[dict[str, Any]],
    reduction: list[dict[str, Any]],
    locking: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 2221 - Y5/R2FR delta_g S_Gamma Kmetric Kernel Norm Source Pass",
                "",
                "## Verdict",
                "- 2220 selected the Kmetric kernel norm pass; the current tree already contains a valid older implementation of that pass at 1531.",
                "- 2221 therefore bridges rather than duplicates: 1531 is adopted as the kernel-pack audit, with 1532-1536 treated as existing follow-through evidence.",
                "- The best route is not a bare fixed `L_cg` axiom. The clean conditional path is a vacuum-subtracted stationary source plus local locking.",
                "- That route is alive but not claimable: `J_eff`, `B_m`, hidden Kmetric kernels, units, and observable projections remain unsigned or unbounded.",
                "- Next work should inspect/import the existing 1537-1539 source-support and inner-charge frontier before doing any new derivation.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "path_exists", "validation_overall_pass", "role"]),
                "",
                "## Existing Chain Audit",
                md_table(chain, ["chain_id", "checkpoint", "finding", "current_2221_use", "guardrail", "source_path"]),
                "",
                "## Kmetric Kernel Norm Source Audit",
                md_table(kernel, ["audit_id", "quantity", "role", "status", "finding", "missing_to_promote"]),
                "",
                "## Algebraic Chain Reduction Ledger",
                md_table(reduction, ["ledger_id", "formula_or_rule", "meaning", "status", "missing_to_promote"]),
                "",
                "## Local Locking Handoff",
                md_table(locking, ["handoff_id", "object", "contract", "status"]),
                "",
                "## Claim Gate",
                md_table(claims, ["gate_id", "claim", "status", "reason"]),
                "",
                "## Decision Ledger",
                md_table(decisions, ["decision_id", "decision", "result", "rationale"]),
                "",
                "## Next Target",
                md_table(next_target, ["next_id", "target_file", "target_script", "objective", "success_condition", "do_not"]),
                "",
                "## Branch Copies",
                md_table(copies, ["copy_id", "source_path", "target_path", "copied", "parse_ok"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Working Interpretation",
                "",
                "This is not circling the same drain. The branch moved from a vague local residual to a concrete proof stack: Kmetric kernels -> algebraic double-zero -> local locking/no-hair -> source-boundary component norms. The grim bit is that none of this is a local-GR claim yet. The good bit is that the missing pieces are now named, finite, and attackable.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    chain = chain_rows()
    kernel = kernel_rows()
    reduction = reduction_rows()
    locking = locking_rows()
    claims = claim_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(CHAIN_AUDIT, chain)
    write_csv(KERNEL_AUDIT, kernel)
    write_csv(REDUCTION_LEDGER, reduction)
    write_csv(LOCKING_HANDOFF, locking)
    write_csv(CLAIM_GATE, claims)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_target)
    copies = copy_outputs()
    write_csv(BRANCH_COPIES, copies)
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        CHAIN_AUDIT,
        KERNEL_AUDIT,
        REDUCTION_LEDGER,
        LOCKING_HANDOFF,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
        BRANCH_COPIES,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, chain, kernel, reduction, locking, claims, decisions, next_target, copies, validation)


if __name__ == "__main__":
    main()
