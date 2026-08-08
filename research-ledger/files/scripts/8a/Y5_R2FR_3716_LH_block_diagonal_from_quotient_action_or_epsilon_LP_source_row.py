from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3716"
BRANCH_ID = "MTS_R2FR_Y5_LH_BLOCK_DIAGONAL_FROM_QUOTIENT_ACTION_OR_EPSILON_LP_SOURCE_ROW_3716"
DOC = ROOT / "3716-Y5-R2FR-LH-block-diagonal-from-quotient-action-or-epsilon-LP-source-row.md"

DOC_3715 = ROOT / "3715-Y5-R2FR-kernel-projected-local-operator-compatibility-or-commutator-leak.md"
NEXT_3715 = RESIDUALS / "P8_Y5_R2FR_3715_NEXT_TARGET.csv"
BLOCK_3715 = RESIDUALS / "P8_Y5_R2FR_3715_OPERATOR_BLOCK_SPLIT_ROWS.csv"
THEOREM_3715 = RESIDUALS / "P8_Y5_R2FR_3715_COMMUTATOR_THEOREM_ROWS.csv"
LEAK_3715 = RESIDUALS / "P8_Y5_R2FR_3715_DYNAMIC_LEAK_ROWS.csv"
ARENA_3715 = RESIDUALS / "P8_Y5_R2FR_3715_ARENA_EXTENSION_ROWS.csv"
FISHER_3708 = RESIDUALS / "P8_Y5_R2FR_3708_FISHER_GAP_DERIVATION_ROWS.csv"
NQ_670 = RESIDUALS / "P8_Y5_R10_670_NO_POLE_QUOTIENT_PROOF_CHAIN.csv"
NORMAL_FORM_3519 = RESIDUALS / "P8_EM_vq_parent_object_language_normal_form_candidate.csv"
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
        ("doc_3715", DOC_3715, "ADVANCE_TO_BLOCK_DIAGONAL_PROOF", "3715 selected block diagonal proof target"),
        ("next_3715", NEXT_3715, "block diagonal local dynamics", "3715 declared 3716 target"),
        ("block_3715", BLOCK_3715, "BLK3715_2_block_matrix", "local operator block split"),
        ("theorem_3715", THEOREM_3715, "THM3715_0_exact_invariance", "commutator exact-invariance theorem"),
        ("leak_3715", LEAK_3715, "LEAK3715_0_offdiag", "epsilon_LP dynamic leak row"),
        ("arena_3715", ARENA_3715, "ARENA3715_0_master_update", "arena extension for dynamic leakage"),
        ("fisher_3708", FISHER_3708, "FGD3708_0_parent_bath", "kernel/fibre bath and Fisher gap route"),
        ("nq_670", NQ_670, "NQ670_3_action_descent", "quotient action descent route"),
        ("normal_form_3519", NORMAL_FORM_3519, "NF3519_1_quotient_visible_stack", "parent object-language normal-form candidate"),
        ("doc_1038", DOC_1038, "MISSING_DCX_OPERATOR", "operator-owner obstruction"),
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


def normal_form_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "NF3716_0_coordinates",
            "local quotient/fibre coordinates",
            "Phi -> (q,z), with q=q_obs(Phi), z=P_ker(Phi-Phi_0), and Dq z=0",
            "sets the local variables needed to discuss mixed Hessian blocks",
            "SETUP",
        ),
        (
            "NF3716_1_pure_quotient_warning",
            "pure quotient action",
            "S_parent=S_obs(q)",
            "gives mixed Hessian zero but also gives L_KK=0, so it kills the local mass-gap branch unless extra constrained/gauge structure is supplied",
            "WARNING_NOT_SUFFICIENT_FOR_MASSIVE_LOCAL_BRANCH",
        ),
        (
            "NF3716_2_viable_fibre_gap_form",
            "quotient plus fibre gap action",
            "S_parent=S_obs(q)+1/2 <z,M_K(q)z>_G + O(||z||^3)+S_boundary",
            "allows matter/readout quotient silence while retaining a kernel-sector mass gap",
            "VIABLE_CONDITIONAL_NORMAL_FORM",
        ),
        (
            "NF3716_3_F1_zero",
            "local fibre extremum",
            "F_1:=partial_z S_parent|_{z=0}=0",
            "removes the linear kernel source before solving the local response",
            "REQUIRED_ZERO_CLAUSE",
        ),
        (
            "NF3716_4_mixed_zero",
            "mixed Hessian silence",
            "B_QK:=partial_q partial_z S_parent|_{z=0}=0",
            "for the quadratic fibre-gap form, q-dependence of M_K(q) does not create a q-z mixed Hessian at z=0",
            "DERIVED_IF_NORMAL_FORM_SIGNED",
        ),
        (
            "NF3716_5_kernel_gap",
            "kernel mass gap",
            "M_K(q_0) >= m_K G_K, with m_K identified with Xi_H only after sector matching",
            "keeps the hidden/kernel mode locally short-ranged without coupling it linearly to q_obs",
            "REQUIRES_GAP_OWNER",
        ),
    ]
    return [
        {
            **base(timestamp),
            "normal_form_id": row_id,
            "object": obj,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "claim_allowed": False,
        }
        for row_id, obj, formula, meaning, status in specs
    ]


def mixed_hessian_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "MH3716_0_block_owner",
            "B_QK",
            "(I-P_ker)L_H P_ker",
            "local Hessian/operator units",
            "observed/complement response sourced by kernel motion",
            "MISSING_ZERO_THEOREM_OR_NUMERIC_BOUND",
        ),
        (
            "MH3716_1_adjoint_block",
            "B_KQ",
            "P_ker L_H (I-P_ker)",
            "local Hessian/operator units",
            "kernel response sourced by observed/complement motion",
            "MISSING_SELFADJOINT_OR_NUMERIC_BOUND",
        ),
        (
            "MH3716_2_commutator_equivalence",
            "epsilon_LP",
            "||[L_H,P_ker]|| = ||B_QK - B_KQ|| in block form; for self-adjoint L_H this is controlled by the mixed block norm",
            "local Hessian/operator units",
            "turns the 3715 commutator into a concrete mixed-Hessian coefficient",
            "DERIVED_BLOCK_EQUIVALENCE",
        ),
        (
            "MH3716_3_safe_bound",
            "epsilon_LP_bound",
            "epsilon_LP <= ||B_QK|| + ||B_KQ||",
            "local Hessian/operator units",
            "fallback bound if self-adjointness or exact block equality is not signed",
            "DERIVED_SAFE_BOUND",
        ),
        (
            "MH3716_4_exact_zero",
            "epsilon_LP_zero_branch",
            "B_QK=0 and B_KQ=0 => [L_H,P_ker]=0",
            "local Hessian/operator units",
            "exact dynamic compatibility branch",
            "CONDITIONAL_ZERO_BRANCH_NOT_PROMOTED",
        ),
    ]
    return [
        {
            **base(timestamp),
            "mixed_id": row_id,
            "quantity": quantity,
            "formula_or_value": formula,
            "units": units,
            "use": use,
            "status": status,
            "claim_allowed": False,
        }
        for row_id, quantity, formula, units, use, status in specs
    ]


def theorem_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "THM3716_0_normal_form_to_block_diagonal",
            "If the local parent action has quotient plus fibre gap normal form and F_1=0 at z=0, then B_QK=B_KQ=0 at the local branch.",
            "Differentiate S_obs(q)+1/2<z,M_K(q)z> twice: every q-z derivative of the quadratic fibre term is proportional to z and vanishes at z=0.",
            "DERIVED_EXACT_CONDITIONAL",
            "requires parent-signed coordinates, fibre extremum, boundary silence, and Hessian domain",
        ),
        (
            "THM3716_1_block_diagonal_to_commutator",
            "B_QK=B_KQ=0 implies [L_H,P_ker]=0.",
            "The block matrix becomes diagonal relative to K direct_sum O, so multiplication by P_ker commutes with L_H.",
            "DERIVED_EXACT_CONDITIONAL",
            "requires P_ker and L_H to use the same G_H/domain split",
        ),
        (
            "THM3716_2_gap_not_sacrificed",
            "The fibre-gap normal form can keep m_K>0 while setting B_QK=0.",
            "Unlike pure quotient descent, the fibre quadratic term supplies L_KK=M_K(q_0) without a linear q-observed coupling.",
            "DERIVED_CONDITIONAL_ROUTE",
            "requires M_K(q_0) to be parent-owned and matched to Xi_H/m_K",
        ),
        (
            "THM3716_3_failure_bound",
            "If the normal form fails, epsilon_LP is retained as ||B_QK||+||B_KQ|| and fed into the 3715 dynamic leak bound.",
            "This preserves falsifiability: mixed Hessian leakage becomes a scored coefficient rather than a hidden closure.",
            "DERIVED_NONCLAIM_BOUND_ROUTE",
            "requires numeric/source bounds for mixed blocks",
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


def coefficient_pack_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "COEF3716_0_F1",
            "F_1",
            "partial_z S_parent|_{z=0}",
            "action per fibre coordinate",
            "must be zero for the local branch to be a fibre extremum",
            "MISSING_PARENT_EXTREMUM_CERTIFICATE",
        ),
        (
            "COEF3716_1_MK",
            "M_K",
            "partial_z partial_z S_parent|_{z=0}",
            "local Hessian/operator units",
            "kernel/fibre mass-gap operator",
            "MISSING_KERNEL_GAP_OWNER",
        ),
        (
            "COEF3716_2_BQK",
            "B_QK",
            "partial_q partial_z S_parent|_{z=0}",
            "local Hessian/operator units",
            "mixed observed-kernel Hessian; should vanish in fibre normal form",
            "MISSING_MIXED_HESSIAN_ZERO_OR_BOUND",
        ),
        (
            "COEF3716_3_boundary_mixed",
            "B_boundary,QK",
            "partial_q partial_z S_boundary|_{z=0}",
            "local boundary Hessian/operator units",
            "boundary can reintroduce mixed leakage even when the bulk normal form works",
            "MISSING_BOUNDARY_MIXED_ZERO_OR_BOUND",
        ),
        (
            "COEF3716_4_epsilon_LP",
            "epsilon_LP",
            "epsilon_LP <= ||B_QK||+||B_KQ||+||B_boundary,QK||",
            "local Hessian/operator units",
            "safe source row for 3715 if exact block diagonalization is not signed",
            "DERIVED_COEFFICIENT_PACK",
        ),
    ]
    return [
        {
            **base(timestamp),
            "coefficient_id": row_id,
            "quantity": quantity,
            "formula_or_value": formula,
            "units": units,
            "use": use,
            "status": status,
            "claim_allowed": False,
        }
        for row_id, quantity, formula, units, use, status in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("DEC3716_0_pure_quotient_warning", "Pure quotient descent alone is not the desired local branch.", "It can erase the physical pole, but it also makes the kernel Hessian zero unless extra gauge/constrained structure is supplied.", "PURE_QUOTIENT_NOT_ENOUGH"),
        ("DEC3716_1_fibre_normal_form", "The viable route is quotient-visible variables plus a fibre quadratic gap with F_1=0 and B_QK=0 at z=0.", "This preserves matter/readout silence while allowing a massive local hidden/kernel response.", "FIBRE_GAP_ROUTE_SELECTED"),
        ("DEC3716_2_mixed_block_target", "The actual coefficient to kill or bound is B_QK=partial_q partial_z S_parent|_0, plus boundary mixed leakage.", "This is more concrete than asking vaguely whether the operator commutes.", "MIXED_HESSIAN_TARGET_EXPOSED"),
        ("DEC3716_3_next", "Next target should try to parent-sign F_1=0 and B_QK=0 from a fibre-normal-form action clause, or write their finite coefficient rows.", "That is the shortest route from the current derivation to local-GR/Newton dynamic silence.", "ADVANCE_TO_F1_BQK_OWNER"),
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
        ("CG3716_0_coordinates", "local q,z coordinates and P_ker are parent-owned"),
        ("CG3716_1_F1", "F_1=0 is derived as a parent local fibre extremum, not imposed after testing"),
        ("CG3716_2_mixed", "B_QK and B_KQ vanish, or finite source-backed bounds exist"),
        ("CG3716_3_gap", "M_K/q0 sector gap is parent-owned and matched to m_K_or_Xi_H"),
        ("CG3716_4_boundary", "boundary mixed Hessian leakage is zero or bounded"),
        ("CG3716_5_public", "block diagonal local dynamics/local-GR silence claim allowed"),
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
            "status_id": "STATUS3716_0",
            "status": "LH_COMMUTATOR_REDUCED_TO_MIXED_HESSIAN_FIBRE_NORMAL_FORM_ROUTE_NONCLAIM",
            "summary": (
                "3716 reduces [L_H,P_ker]=0 to a mixed Hessian target. "
                "Pure quotient descent is flagged as insufficient for a massive local branch. "
                "The viable route is S_parent=S_obs(q)+1/2<z,M_K(q)z>+O(z^3) with F_1=0 and B_QK=0 at z=0; otherwise epsilon_LP is bounded by mixed Hessian coefficients."
            ),
            "claim_allowed": False,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "next_id": "NEXT3716_0",
            "target_doc": "3717-Y5-R2FR-fibre-normal-form-F1-zero-and-BQK-mixed-Hessian-owner.md",
            "target_script": "scripts/Y5_R2FR_3717_fibre_normal_form_F1_zero_and_BQK_mixed_Hessian_owner.py",
            "objective": "try to parent-sign the fibre-normal-form clauses F_1=0 and B_QK=0, or retain explicit F_1/B_QK/B_boundary_QK coefficient rows with units and local arena impact",
            "success_gate": "F_1 and B_QK are either theorem-zero from a parent action normal form or retained as finite nonclaim coefficient rows feeding epsilon_LP",
            "claim_allowed": False,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    normal_forms: list[dict[str, object]],
    mixed: list[dict[str, object]],
    theorems: list[dict[str, object]],
    coefficients: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3716 Y5 R2FR L_H Block Diagonal From Quotient Action Or epsilon_LP Source Row",
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
        "- Pure quotient descent `S_parent=S_obs(q)` is not enough for the target branch because it also removes the kernel mass gap.",
        "- The viable local branch is a quotient plus fibre-gap normal form: `S_parent=S_obs(q)+1/2 <z,M_K(q)z>_G+O(||z||^3)+S_boundary`.",
        "- At `z=0`, that form gives `F_1:=partial_z S_parent|_0=0` and `B_QK:=partial_q partial_z S_parent|_0=0`.",
        "- Therefore the commutator target `[L_H,P_ker]=0` reduces to proving or bounding the mixed Hessian blocks `B_QK`, `B_KQ`, and boundary mixed leakage.",
        "- If exact block diagonalization fails, retain `epsilon_LP <= ||B_QK||+||B_KQ||+||B_boundary,QK||`.",
        "- `valid_for_claim=false`: this is a derivation route and coefficient pack, not a local-GR/Newton pass.",
        "",
        "## Normal Form Audit",
        "",
    ]
    for row in normal_forms:
        lines.append(f"- `{row['normal_form_id']}` `{row['status']}`: `{row['formula']}` | {row['meaning']}")
    lines.extend(["", "## Mixed Hessian Rows", ""])
    for row in mixed:
        lines.append(f"- `{row['mixed_id']}` `{row['quantity']}`: `{row['formula_or_value']}` | {row['status']} | {row['use']}")
    lines.extend(["", "## Theorems", ""])
    for row in theorems:
        lines.append(f"- `{row['theorem_id']}` `{row['status']}`: {row['statement']} | gap: {row['remaining_gap']}")
    lines.extend(["", "## Coefficient Pack", ""])
    for row in coefficients:
        lines.append(f"- `{row['coefficient_id']}` `{row['quantity']}`: `{row['formula_or_value']}` | {row['status']} | {row['use']}")
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
    normal_forms: list[dict[str, object]],
    mixed: list[dict[str, object]],
    theorems: list[dict[str, object]],
    coefficients: list[dict[str, object]],
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
    nf_text = "\n".join(str(row["formula"]) for row in normal_forms)
    checks.append(("fibre_normal_form", "fibre gap normal form is present", "S_parent=S_obs(q)+1/2 <z,M_K(q)z>_G" in nf_text, ""))
    checks.append(("pure_quotient_warning", "pure quotient warning is present", any(row["status"] == "WARNING_NOT_SUFFICIENT_FOR_MASSIVE_LOCAL_BRANCH" for row in normal_forms), ""))
    quantities = {row["quantity"] for row in mixed}
    checks.append(("mixed_rows", "B_QK, B_KQ, epsilon_LP rows are present", {"B_QK", "B_KQ", "epsilon_LP"} <= quantities, ""))
    theorem_text = "\n".join(str(row["statement"]) for row in theorems)
    checks.append(("block_diagonal_theorem", "normal-form to block-diagonal theorem is present", "B_QK=B_KQ=0" in theorem_text and "[L_H,P_ker]=0" in theorem_text, ""))
    coeffs = {row["quantity"] for row in coefficients}
    checks.append(("coefficient_pack", "F_1, M_K, B_QK, boundary mixed, epsilon_LP coefficient pack present", {"F_1", "M_K", "B_QK", "B_boundary,QK", "epsilon_LP"} <= coeffs, ""))
    checks.append(("nonclaim_decisions", "all decisions are nonclaim", all(row["claim_allowed"] is False for row in decisions), ""))
    checks.append(("claim_gates_blocked", "all claim gates blocked", all(row["status"] == "BLOCKED" and row["claim_allowed"] is False for row in claim_gates), ""))
    checks.append(("next_target_3717", "next target advances to F1/BQK owner", str(next_target[0]["target_doc"]).startswith("3717-") and "F1" in str(next_target[0]["target_doc"]), ""))
    doc_text = read_text(DOC) if DOC.exists() else ""
    checks.append(("doc_core_terms", "doc contains core 3716 terms", all(term in doc_text for term in ["Pure quotient descent", "F_1:=partial_z", "B_QK:=partial_q partial_z", "epsilon_LP <=", "valid_for_claim=false"]), ""))
    formalization_leaks = list(FORMALIZATION.rglob("*3716*")) if FORMALIZATION.exists() else []
    checks.append(("no_formalization_leak", "no 3716 files were written into formalization-workbench", len(formalization_leaks) == 0, "; ".join(str(path) for path in formalization_leaks)))
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
    normal_forms = normal_form_rows(timestamp)
    mixed = mixed_hessian_rows(timestamp)
    theorems = theorem_rows(timestamp)
    coefficients = coefficient_pack_rows(timestamp)
    decisions = decision_rows(timestamp)
    claim_gates = claim_gate_rows(timestamp)
    status = status_rows(timestamp)
    next_target = next_rows(timestamp)

    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3716_SOURCE_REGISTER.csv",
        "normal_forms": RESIDUALS / "P8_Y5_R2FR_3716_NORMAL_FORM_AUDIT_ROWS.csv",
        "mixed": RESIDUALS / "P8_Y5_R2FR_3716_MIXED_HESSIAN_ROWS.csv",
        "theorems": RESIDUALS / "P8_Y5_R2FR_3716_BLOCK_DIAGONAL_THEOREM_ROWS.csv",
        "coefficients": RESIDUALS / "P8_Y5_R2FR_3716_COEFFICIENT_PACK_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3716_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3716_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3716_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3716_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3716_VALIDATION.csv",
    }

    write_csv(outputs["sources"], sources)
    write_csv(outputs["normal_forms"], normal_forms)
    write_csv(outputs["mixed"], mixed)
    write_csv(outputs["theorems"], theorems)
    write_csv(outputs["coefficients"], coefficients)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["claim_gates"], claim_gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, normal_forms, mixed, theorems, coefficients, decisions, claim_gates, status, next_target)

    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(generated_paths, sources, normal_forms, mixed, theorems, coefficients, decisions, claim_gates, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3716 validation failed: {failures}", file=sys.stderr)
        return 1
    print("wrote 3716 checkpoint: L_H commutator reduced to mixed Hessian/fibre normal form gate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
