from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3715"
BRANCH_ID = "MTS_R2FR_Y5_KERNEL_PROJECTED_LOCAL_OPERATOR_COMPATIBILITY_OR_COMMUTATOR_LEAK_3715"
DOC = ROOT / "3715-Y5-R2FR-kernel-projected-local-operator-compatibility-or-commutator-leak.md"

DOC_3714 = ROOT / "3714-Y5-R2FR-PH-kernel-selector-owner-or-epsilon-qH-coefficient-pack.md"
NEXT_3714 = RESIDUALS / "P8_Y5_R2FR_3714_NEXT_TARGET.csv"
PROJECTOR_3714 = RESIDUALS / "P8_Y5_R2FR_3714_KERNEL_PROJECTOR_DERIVATION_ROWS.csv"
EPSILON_3714 = RESIDUALS / "P8_Y5_R2FR_3714_EPSILON_QH_COEFFICIENT_PACK.csv"
HYPOTHESIS_3714 = RESIDUALS / "P8_Y5_R2FR_3714_REQUIRED_HYPOTHESIS_ROWS.csv"
BUDGET_3714 = RESIDUALS / "P8_Y5_R2FR_3714_BUDGET_IMPACT_ROWS.csv"
FISHER_3708 = RESIDUALS / "P8_Y5_R2FR_3708_FISHER_GAP_DERIVATION_ROWS.csv"
SUPPRESSION_3693 = RESIDUALS / "P8_Y5_R2FR_3693_LOCAL_SUPPRESSION_LAW_ROWS.csv"
RESIDUAL_3700 = RESIDUALS / "P8_Y5_R2FR_3700_RESIDUAL_TENSOR_ROWS.csv"
NQ_670 = RESIDUALS / "P8_Y5_R10_670_NO_POLE_QUOTIENT_PROOF_CHAIN.csv"
DOC_1038 = ROOT / "1038-Y5-R10-parent-Omega-DCX-vertical-generator-closure-or-beta-bound-acquisition.md"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(timestamp: str) -> dict[str, object]:
    return {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_register(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("doc_3714", DOC_3714, "[L_H,P_ker]", "3714 selected local-operator compatibility target"),
        ("next_3714", NEXT_3714, "[L_H,P_ker]=0", "3714 declared 3715 target"),
        ("projector_3714", PROJECTOR_3714, "PROJ3714_3_kernel_projector", "P_ker construction rows"),
        ("epsilon_3714", EPSILON_3714, "EP3714_4_dynamic_commutator", "epsilon_LP coefficient row seed"),
        ("hypothesis_3714", HYPOTHESIS_3714, "HYP3714_4_operator_compatibility", "L_H compatibility hypothesis"),
        ("budget_3714", BUDGET_3714, "finite_mismatch_condition", "matter budget impact rows"),
        ("fisher_3708", FISHER_3708, "FGD3708_5_second_order_bridge", "Xi_H/Fisher local operator bridge"),
        ("suppression_3693", SUPPRESSION_3693, "SPL3693_1_norm_bound", "operator-norm suppression law"),
        ("residual_3700", RESIDUAL_3700, "RT3700_3_amplitude_bound", "second-order local residual amplitude bound"),
        ("nq_670", NQ_670, "NQ670_4_no_bulk_hessian_block", "quotient action/Hessian no-pole conditional route"),
        ("doc_1038", DOC_1038, "MISSING_DCX_OPERATOR", "parent Omega/DCX operator obstruction"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append({
            **base(timestamp),
            "source_id": source_id,
            "role": role,
            "path": str(path),
            "needle": needle,
            "exists": exists,
            "needle_found": needle in text if exists else False,
            "claim_allowed": False,
        })
    return rows


def block_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "BLK3715_0_decomposition",
            "H = K direct_sum O with K:=ker(Dq_obs), P:=P_ker, and O:=(I-P)H",
            "kernel/complement split induced by the 3714 quotient-kernel selector",
            "SETUP",
        ),
        (
            "BLK3715_1_local_operator",
            "L_H := d2 S_parent|_0 on the local horizontal sector",
            "local Hessian/response operator whose inverse gives the Green/Yukawa response",
            "REQUIRES_PARENT_OPERATOR_OWNER",
        ),
        (
            "BLK3715_2_block_matrix",
            "L_H = [[L_KK,L_KO],[L_OK,L_OO]] relative to K direct_sum O",
            "off-diagonal blocks are the only way kernel-selected sources dynamically leak into observed directions",
            "DERIVED_BLOCK_SPLIT",
        ),
        (
            "BLK3715_3_commutator",
            "C_LP := [L_H,P] = L_H P - P L_H",
            "C_LP=0 iff L_H preserves K and O for a self-adjoint local Hessian",
            "DERIVED_COMPATIBILITY_OBJECT",
        ),
        (
            "BLK3715_4_offdiag_bound",
            "max(||L_OK||,||L_KO||) <= ||[L_H,P]|| := epsilon_LP",
            "commutator norm bounds the dangerous off-diagonal Hessian blocks",
            "DERIVED_BOUND",
        ),
    ]
    return [
        {
            **base(timestamp),
            "block_id": row_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "claim_allowed": False,
        }
        for row_id, formula, meaning, status in specs
    ]


def theorem_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "THM3715_0_exact_invariance",
            "If [L_H,P_ker]=0 and P_ker is parent-owned, then L_H ker(Dq_obs) subset ker(Dq_obs).",
            "For y in K, P y=y. [L,P]=0 gives P L y=L P y=L y, so L y in K.",
            "DERIVED_EXACT_CONDITIONAL",
            "requires parent-owned L_H, P_ker, domain, and self-adjointness/closed-range controls",
        ),
        (
            "THM3715_1_inverse_invariance",
            "If [L_H,P_ker]=0 and L_H is invertible/coercive on the local branch, then [L_H^-1,P_ker]=0.",
            "Commuting bounded functional calculus or block diagonal inverse preserves the kernel split.",
            "DERIVED_EXACT_CONDITIONAL",
            "requires gap/coercivity and inverse domain control",
        ),
        (
            "THM3715_2_dynamic_silence",
            "If J in ker(Dq_obs) and [L_H,P_ker]=0, then y=L_H^-1 J lies in ker(Dq_obs), hence Dq_obs y=0.",
            "kernel-selected matter/source silence remains dynamically stable under the local Green response",
            "DERIVED_EXACT_CONDITIONAL",
            "requires exact kernel source and exact operator compatibility",
        ),
        (
            "THM3715_3_finite_leak",
            "If epsilon_LP:=||[L_H,P_ker]|| is nonzero, the observed leakage is bounded by the off-diagonal response.",
            "the exact zero route demotes to a scored dynamics-leak coefficient instead of hidden closure",
            "DERIVED_BOUND_ROUTE",
            "requires m_O, Xi_H, ||Dq_obs||, and source norm inputs",
        ),
    ]
    return [
        {
            **base(timestamp),
            "theorem_id": row_id,
            "statement": statement,
            "proof_sketch": proof,
            "status": status,
            "remaining_gap": gap,
            "claim_allowed": False,
        }
        for row_id, statement, proof, status, gap in specs
    ]


def leak_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "LEAK3715_0_offdiag",
            "epsilon_LP",
            "||[L_H,P_ker]||",
            "local Hessian/operator units",
            "zero iff local operator block-diagonalizes the quotient-kernel split",
            "MISSING_ZERO_THEOREM_OR_NUMERIC_OPERATOR_NORM",
        ),
        (
            "LEAK3715_1_complement_gap",
            "m_O",
            "lower spectral gap of L_OO on O=(I-P_ker)H",
            "same units as L_H, typically m^-2 in the local massive branch",
            "controls inverse response in observed/complement directions",
            "MISSING_COMPLEMENT_GAP",
        ),
        (
            "LEAK3715_2_kernel_gap",
            "m_K_or_Xi_H",
            "lower local response gap for the kernel-projected source sector",
            "same units as L_H; Xi_H may be used only if it is the correct sector gap",
            "controls total source response before off-diagonal leakage",
            "MISSING_SECTOR_GAP_MATCH",
        ),
        (
            "LEAK3715_3_dynamic_q_leak",
            "epsilon_q_dyn",
            "||Dq_obs|| epsilon_LP ||J_K||/(m_O*m_K_or_Xi_H)",
            "observed quotient/readout units",
            "finite leakage of a kernel-selected source through off-diagonal local dynamics",
            "DERIVED_NONCLAIM_BOUND",
        ),
        (
            "LEAK3715_4_zero_branch",
            "epsilon_q_dyn_zero",
            "epsilon_LP=0 => epsilon_q_dyn=0",
            "observed quotient/readout units",
            "exact dynamics stability branch",
            "CONDITIONAL_ZERO_BRANCH_NOT_PROMOTED",
        ),
    ]
    return [
        {
            **base(timestamp),
            "leak_id": row_id,
            "quantity": quantity,
            "formula_or_value": formula,
            "units": units,
            "use": use,
            "status": status,
            "claim_allowed": False,
        }
        for row_id, quantity, formula, units, use, status in specs
    ]


def arena_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "ARENA3715_0_master_update",
            "local master residual",
            "epsilon_i^MTS <= old_bound_i + C_i_dyn * epsilon_q_dyn",
            "adds dynamics-kernel leakage to the existing 3700 local residual bound",
            "NONCLAIM_BOUND_EXTENSION",
        ),
        (
            "ARENA3715_1_R10",
            "R10/Newton",
            "alpha_dyn(lambda_H) <= K_dyn,R10 * epsilon_q_dyn",
            "keeps kernel compatibility separate from source-product P_N until K_dyn is sourced",
            "NONCLAIM_ARENA_TEMPLATE",
        ),
        (
            "ARENA3715_2_PPN_orbit",
            "PPN/orbital",
            "Delta_PPN_or_orbit <= K_dyn,PPN/orbit * epsilon_q_dyn",
            "prevents silent promotion from R10 into Solar-System tests",
            "NONCLAIM_ARENA_TEMPLATE",
        ),
        (
            "ARENA3715_3_EM_clock_WEP",
            "EM/clocks/WEP",
            "Delta_EM/clock/WEP <= K_dyn,EM/clock/WEP * epsilon_q_dyn",
            "keeps Maxwell/clock/material readout leakage visible",
            "NONCLAIM_ARENA_TEMPLATE",
        ),
    ]
    return [
        {
            **base(timestamp),
            "arena_id": row_id,
            "arena": arena,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "claim_allowed": False,
        }
        for row_id, arena, formula, meaning, status in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("DEC3715_0_commutator_gate", "The dynamic stability condition is exactly [L_H,P_ker]=0.", "This turns kernel silence into an operator compatibility theorem rather than another closure axiom.", "COMMUTATOR_GATE_DERIVED"),
        ("DEC3715_1_zero_conditional", "If the commutator vanishes and the local operator is coercive, kernel-selected sources stay invisible to q_obs under the Green response.", "This is the cleanest route to preserving matter silence after dynamics.", "DYNAMIC_ZERO_BRANCH_CONDITIONAL"),
        ("DEC3715_2_bound_route", "If the commutator does not vanish, retain epsilon_q_dyn <= ||Dq_obs|| epsilon_LP ||J_K||/(m_O*m_K_or_Xi_H).", "The failure mode becomes a measured/scored leakage row, not a hidden fudge factor.", "FINITE_LEAK_BOUND_DERIVED"),
        ("DEC3715_3_next", "Next target should derive L_H block diagonalization from a quotient-descended parent action, or source epsilon_LP.", "That is the remaining bridge between kernel projection and actual local-GR/Newton dynamics.", "ADVANCE_TO_BLOCK_DIAGONAL_PROOF"),
    ]
    return [
        {
            **base(timestamp),
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "status": status,
            "claim_allowed": False,
        }
        for decision_id, decision, rationale, status in specs
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("CG3715_0_LH_owner", "L_H is parent-owned as the local Hessian/response operator with declared domain"),
        ("CG3715_1_selfadjoint", "L_H is self-adjoint/coercive in the G_H metric or the non-selfadjoint correction is retained"),
        ("CG3715_2_commutator", "[L_H,P_ker]=0 is proved, or epsilon_LP has a finite source-backed norm"),
        ("CG3715_3_gaps", "m_O and m_K_or_Xi_H are source-owned sector gaps with units"),
        ("CG3715_4_arenas", "epsilon_q_dyn is mapped into R10/PPN/orbit/EM/clock/WEP residual budgets"),
        ("CG3715_5_public", "kernel-projected local-GR/Newton dynamic-silence claim allowed"),
    ]
    return [
        {
            **base(timestamp),
            "claim_gate_id": gate_id,
            "requirement": requirement,
            "status": "BLOCKED",
            "claim_allowed": False,
        }
        for gate_id, requirement in specs
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "status_id": "STATUS3715_0",
            "status": "LH_KERNEL_COMPATIBILITY_COMMUTATOR_GATE_AND_DYNAMIC_LEAK_BOUND_DERIVED_NONCLAIM",
            "summary": (
                "3715 derives the operator compatibility gate [L_H,P_ker]=0. "
                "If it holds, kernel-selected sources remain in ker(Dq_obs) under L_H^-1. "
                "If it fails, the dynamics leakage is bounded by ||Dq_obs|| epsilon_LP ||J_K||/(m_O*m_K_or_Xi_H) and must be scored as a nonclaim arena residual."
            ),
            "claim_allowed": False,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "next_id": "NEXT3715_0",
            "target_doc": "3716-Y5-R2FR-LH-block-diagonal-from-quotient-action-or-epsilon-LP-source-row.md",
            "target_script": "scripts/Y5_R2FR_3716_LH_block_diagonal_from_quotient_action_or_epsilon_LP_source_row.py",
            "objective": "try to derive [L_H,P_ker]=0 from quotient-descended parent action/Hessian structure, or retain epsilon_LP with domain, units, sector gaps, and arena-budget projections",
            "success_gate": "either block diagonal local dynamics is parent-signed or epsilon_LP becomes an explicit finite nonclaim input row suitable for local arena scoring",
            "claim_allowed": False,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    blocks: list[dict[str, object]],
    theorems: list[dict[str, object]],
    leaks: list[dict[str, object]],
    arenas: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3715 Y5 R2FR Kernel-Projected Local Operator Compatibility Or Commutator Leak",
        "",
        "Private checkpoint. No GitHub action. No public claim.",
        "",
        "## Status",
        "",
        f"- `{status[0]['status']}`",
        f"- {status[0]['summary']}",
        "",
        "## Main Result",
        "",
        "- Decompose the local field space as `H = K direct_sum O`, with `K:=ker(Dq_obs)` and `P:=P_ker`.",
        "- The exact dynamic-stability condition is `[L_H,P_ker]=0`.",
        "- If `[L_H,P_ker]=0`, then `L_H ker(Dq_obs) subset ker(Dq_obs)` and, when invertible, `L_H^-1` preserves the kernel too.",
        "- Therefore a kernel-selected source remains quotient-invisible under the local Green response: `Dq_obs L_H^-1 J_K=0`.",
        "- If the commutator is nonzero, retain `epsilon_q_dyn <= ||Dq_obs|| epsilon_LP ||J_K||/(m_O*m_K_or_Xi_H)`.",
        "- `valid_for_claim=false`: the commutator theorem is derived, but `L_H`, sector gaps, and arena maps are not parent-owned yet.",
        "",
        "## Block Split",
        "",
    ]
    for row in blocks:
        lines.append(f"- `{row['block_id']}` `{row['status']}`: `{row['formula']}` | {row['meaning']}")
    lines.extend(["", "## Theorems", ""])
    for row in theorems:
        lines.append(f"- `{row['theorem_id']}` `{row['status']}`: {row['statement']} | gap: {row['remaining_gap']}")
    lines.extend(["", "## Dynamic Leak Rows", ""])
    for row in leaks:
        lines.append(f"- `{row['leak_id']}` `{row['quantity']}`: `{row['formula_or_value']}` | {row['status']} | {row['use']}")
    lines.extend(["", "## Arena Extensions", ""])
    for row in arenas:
        lines.append(f"- `{row['arena_id']}` `{row['arena']}`: `{row['formula']}` | {row['meaning']}")
    lines.extend(["", "## Decisions", ""])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: `{row['status']}` | {row['decision']}")
    lines.extend(["", "## Claim Gates", ""])
    for row in claim_gates:
        lines.append(f"- `{row['claim_gate_id']}`: `{row['status']}` | {row['requirement']}")
    lines.extend(["", "## Source Register", ""])
    for row in sources:
        lines.append(f"- `{row['source_id']}`: exists={row['exists']} needle_found={row['needle_found']} path=`{row['path']}`")
    lines.extend(["", "## Next Target", ""])
    lines.append(f"- `{next_target[0]['target_doc']}`")
    lines.append(f"- Objective: {next_target[0]['objective']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(
    generated_paths: list[Path],
    sources: list[dict[str, object]],
    blocks: list[dict[str, object]],
    theorems: list[dict[str, object]],
    leaks: list[dict[str, object]],
    arenas: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    timestamp = stamp()
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("sources_exist", "all cited local sources exist", all(bool(row["exists"]) for row in sources), ""))
    checks.append(("needles_found", "all source needles found", all(bool(row["needle_found"]) for row in sources), ""))
    checks.append(("outputs_exist", "all generated paths exist", all(path.exists() for path in generated_paths), ""))
    csv_parse_ok = True
    csv_error = ""
    try:
        for path in [path for path in generated_paths if path.suffix.lower() == ".csv"]:
            if not parse_csv(path):
                csv_parse_ok = False
                csv_error = f"empty csv: {path}"
                break
    except Exception as exc:  # pragma: no cover
        csv_parse_ok = False
        csv_error = str(exc)
    checks.append(("csv_parse", "all generated CSV files parse and are nonempty", csv_parse_ok, csv_error))
    block_text = "\n".join(str(row["formula"]) for row in blocks)
    checks.append(("commutator_object", "commutator object C_LP is defined", "C_LP := [L_H,P]" in block_text, ""))
    theorem_text = "\n".join(str(row["statement"]) for row in theorems)
    checks.append(("inverse_invariance", "inverse invariance theorem is present", "[L_H^-1,P_ker]=0" in theorem_text, ""))
    quantities = {row["quantity"] for row in leaks}
    checks.append(("leak_pack", "epsilon_LP, sector gaps, and dynamic leak rows are present", {"epsilon_LP", "m_O", "m_K_or_Xi_H", "epsilon_q_dyn"} <= quantities, ""))
    arena_names = {row["arena"] for row in arenas}
    checks.append(("arena_templates", "R10, PPN/orbit, and EM/clock/WEP arena templates are present", {"R10/Newton", "PPN/orbital", "EM/clocks/WEP"} <= arena_names, ""))
    checks.append(("nonclaim_decisions", "all decisions are nonclaim", all(row["claim_allowed"] is False for row in decisions), ""))
    checks.append(("claim_gates_blocked", "all claim gates blocked", all(row["status"] == "BLOCKED" and row["claim_allowed"] is False for row in claim_gates), ""))
    checks.append(("next_target_3716", "next target advances to block diagonal proof", str(next_target[0]["target_doc"]).startswith("3716-") and "block-diagonal" in str(next_target[0]["target_doc"]), ""))
    doc_text = read_text(DOC) if DOC.exists() else ""
    checks.append(("doc_core_terms", "doc contains core 3715 terms", all(term in doc_text for term in ["[L_H,P_ker]=0", "Dq_obs L_H^-1 J_K=0", "epsilon_q_dyn <=", "valid_for_claim=false"]), ""))
    formalization_leaks = list(FORMALIZATION.rglob("*3715*")) if FORMALIZATION.exists() else []
    checks.append(("no_formalization_leak", "no 3715 files were written into formalization-workbench", len(formalization_leaks) == 0, "; ".join(str(path) for path in formalization_leaks)))
    return [
        {
            **base(timestamp),
            "validation_id": check_id,
            "description": description,
            "result": "PASS" if passed else "FAIL",
            "details": details,
        }
        for check_id, description, passed, details in checks
    ]


def main() -> int:
    timestamp = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(timestamp)
    blocks = block_rows(timestamp)
    theorems = theorem_rows(timestamp)
    leaks = leak_rows(timestamp)
    arenas = arena_rows(timestamp)
    decisions = decision_rows(timestamp)
    claim_gates = claim_gate_rows(timestamp)
    status = status_rows(timestamp)
    next_target = next_rows(timestamp)

    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3715_SOURCE_REGISTER.csv",
        "blocks": RESIDUALS / "P8_Y5_R2FR_3715_OPERATOR_BLOCK_SPLIT_ROWS.csv",
        "theorems": RESIDUALS / "P8_Y5_R2FR_3715_COMMUTATOR_THEOREM_ROWS.csv",
        "leaks": RESIDUALS / "P8_Y5_R2FR_3715_DYNAMIC_LEAK_ROWS.csv",
        "arenas": RESIDUALS / "P8_Y5_R2FR_3715_ARENA_EXTENSION_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3715_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3715_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3715_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3715_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3715_VALIDATION.csv",
    }

    write_csv(outputs["sources"], sources)
    write_csv(outputs["blocks"], blocks)
    write_csv(outputs["theorems"], theorems)
    write_csv(outputs["leaks"], leaks)
    write_csv(outputs["arenas"], arenas)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["claim_gates"], claim_gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, blocks, theorems, leaks, arenas, decisions, claim_gates, status, next_target)

    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(generated_paths, sources, blocks, theorems, leaks, arenas, decisions, claim_gates, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3715 validation failed: {failures}", file=sys.stderr)
        return 1
    print("wrote 3715 checkpoint: L_H kernel compatibility commutator gate and dynamic leak bound generated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
