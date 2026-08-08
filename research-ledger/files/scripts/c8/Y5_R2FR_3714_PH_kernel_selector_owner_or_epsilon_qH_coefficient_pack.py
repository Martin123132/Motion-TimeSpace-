from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3714"
BRANCH_ID = "MTS_R2FR_Y5_PH_KERNEL_SELECTOR_OWNER_OR_EPSILON_QH_COEFFICIENT_PACK_3714"
DOC = ROOT / "3714-Y5-R2FR-PH-kernel-selector-owner-or-epsilon-qH-coefficient-pack.md"

DOC_3713 = ROOT / "3713-Y5-R2FR-DqH-matter-horizontal-silence-certificate-or-epsilon-qH-row.md"
NEXT_3713 = RESIDUALS / "P8_Y5_R2FR_3713_NEXT_TARGET.csv"
CERT_3713 = RESIDUALS / "P8_Y5_R2FR_3713_DQH_ZERO_CERTIFICATE_ROWS.csv"
EPS_3713 = RESIDUALS / "P8_Y5_R2FR_3713_EPSILON_QH_ROWS.csv"
BUDGET_3713 = RESIDUALS / "P8_Y5_R2FR_3713_MATTER_BUDGET_SUBGATE_ROWS.csv"
FISHER_3708 = RESIDUALS / "P8_Y5_R2FR_3708_FISHER_GAP_DERIVATION_ROWS.csv"
NQ_670 = RESIDUALS / "P8_Y5_R10_670_NO_POLE_QUOTIENT_PROOF_CHAIN.csv"
MFS_1045 = RESIDUALS / "P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv"
MPD_1044 = RESIDUALS / "P8_Y5_R10_1044_MATTER_PULLBACK_DERIVATION.csv"
DOC_1038 = ROOT / "1038-Y5-R10-parent-Omega-DCX-vertical-generator-closure-or-beta-bound-acquisition.md"
DOC_1055 = ROOT / "1055-Y5-R10-alpha-owner-and-matter-functor-parent-action-contract.md"


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
        ("doc_3713", DOC_3713, "im(P_H) subset ker(Dq_obs)", "3713 kernel certificate target"),
        ("next_3713", NEXT_3713, "PH-kernel-selector", "3713 declared 3714 target"),
        ("cert_3713", CERT_3713, "CERT3713_1_PH_kernel_selector", "DqH zero certificate rows"),
        ("eps_3713", EPS_3713, "EPS3713_0_epsilon_qH", "epsilon_qH coefficient rows"),
        ("budget_3713", BUDGET_3713, "T_matter*epsilon_qH", "matter budget subgates"),
        ("fisher_3708", FISHER_3708, "G_H^-1/2", "Fisher/Hessian metric used for kernel projection"),
        ("nq_670", NQ_670, "NQ670_1_canonical_quotient", "canonical quotient construction route"),
        ("mfs_1045", MFS_1045, "MFS1045_0_parent_field_quotient", "parent quotient/readout signature"),
        ("mpd_1044", MPD_1044, "MPD1044_2_geometry_pullback_zero", "matter pullback geometry zero condition"),
        ("doc_1038", DOC_1038, "MISSING_DCX_OPERATOR", "operator/vertical generator compatibility obstruction"),
        ("doc_1055", DOC_1055, "PAC1055_0_configuration_and_quotient", "parent action quotient/readout contract"),
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


def projector_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "PROJ3714_0_linear_map",
            "A := Dq_obs|_0",
            "linearized observed-readout map from local parent field variations to observed quotient/readout variations",
            "SETUP",
        ),
        (
            "PROJ3714_1_metric",
            "G_H",
            "positive local field/Fisher metric used to define adjoints and the orthogonal kernel projector",
            "REQUIRES_PARENT_METRIC_OWNER",
        ),
        (
            "PROJ3714_2_weighted_adjoint",
            "A_G^dagger := G_H^-1 A^* (A G_H^-1 A^*)^+",
            "Moore-Penrose right inverse on ran(A), when the range is closed and the quotient norm is fixed",
            "DERIVED_FUNCTIONAL_FORM",
        ),
        (
            "PROJ3714_3_kernel_projector",
            "P_ker := I - A_G^dagger A",
            "G_H-orthogonal projector onto ker(A)=ker(Dq_obs) under the standard closed-range hypotheses",
            "DERIVED_PROJECTOR_FORM",
        ),
        (
            "PROJ3714_4_zero_property",
            "Dq_obs P_ker = A P_ker = 0",
            "because A A_G^dagger is the identity on ran(A), so A(I-A_G^dagger A)=0",
            "DERIVED_EXACT_IF_HYPOTHESES_SIGNED",
        ),
        (
            "PROJ3714_5_selector_choice",
            "P_H := P_ker",
            "if the local horizontal source projector is defined as this parent-owned kernel projector, epsilon_qH=0 by construction",
            "BEST_ZERO_BRANCH_CONDITIONAL",
        ),
    ]
    return [
        {
            **base(timestamp),
            "projector_id": row_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "claim_allowed": False,
        }
        for row_id, formula, meaning, status in specs
    ]


def hypothesis_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("HYP3714_0_qobs", "q_obs and A=Dq_obs are parent-owned before fitting", "MFS1045_0;PAC1055_0;NQ670_1", "MISSING_PARENT_QOBS_OWNER"),
        ("HYP3714_1_metric", "G_H is parent-owned, positive on the local field tangent space, and gives the adjoint A^*", "FGD3708_2;FGD3708_3", "MISSING_GH_OWNER_AND_UNITS"),
        ("HYP3714_2_closed_range", "A has closed range or a regulated finite-dimensional approximation with documented pseudoinverse", "functional-analysis condition", "MISSING_CLOSED_RANGE_OR_REGULATOR"),
        ("HYP3714_3_selector_adoption", "P_H is selected as P_ker before local tests, not adjusted after seeing bounds", "CERT3713_1", "MISSING_PH_PARENT_SELECTOR"),
        ("HYP3714_4_operator_compatibility", "the local response operator L_H preserves ker(Dq_obs), or commutator leakage is retained", "ODC1038_1;FGD3708_5", "MISSING_LH_KERNEL_COMPATIBILITY"),
        ("HYP3714_5_matter_contract", "matter functor/constant/lift/no-shadow clauses from 3713 are signed", "CERT3713_2-CERT3713_5;MPD1044_7", "MISSING_MATTER_FUNCTOR_SIGNATURE"),
    ]
    return [
        {
            **base(timestamp),
            "hypothesis_id": row_id,
            "requirement": requirement,
            "source_clauses": clauses,
            "status": "REQUIRED_NOT_FULLY_SIGNED",
            "remaining_gap": gap,
            "claim_allowed": False,
        }
        for row_id, requirement, clauses, gap in specs
    ]


def epsilon_pack_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "EP3714_0_exact_kernel",
            "epsilon_qH_exact",
            "0",
            "dimensionless",
            "if P_H=P_ker and HYP3714_0 through HYP3714_3 are signed",
            "CONDITIONAL_ZERO_VALUE_NOT_CLAIMED",
        ),
        (
            "EP3714_1_projector_mismatch",
            "Delta_P_H",
            "P_H-P_ker",
            "operator on local field tangent space",
            "measures how far the actually used horizontal projector is from the quotient-kernel projector",
            "RETAINED_MISMATCH_OBJECT",
        ),
        (
            "EP3714_2_epsilon_from_mismatch",
            "epsilon_qH_bound",
            "epsilon_qH <= ||Dq_obs|| ||Delta_P_H||",
            "Q_units/H_units or dimensionless after norm convention",
            "fallback if P_H is not exactly P_ker",
            "DERIVED_FINITE_BOUND",
        ),
        (
            "EP3714_3_qobs_uncertainty",
            "epsilon_qH_bound_with_Dq_error",
            "epsilon_qH <= epsilon_Dq + ||Dq_obs|| ||Delta_P_H||",
            "Q_units/H_units or dimensionless after norm convention",
            "fallback if Dq_obs itself has a retained parent/readout uncertainty",
            "DERIVED_FINITE_BOUND",
        ),
        (
            "EP3714_4_dynamic_commutator",
            "epsilon_LP",
            "||[L_H,P_ker]||",
            "operator units of local response",
            "not a matter-coupling term, but a necessary local dynamics compatibility row if P_ker is used as P_H",
            "NEXT_COMPATIBILITY_OBJECT",
        ),
    ]
    return [
        {
            **base(timestamp),
            "epsilon_pack_id": row_id,
            "quantity": quantity,
            "formula_or_value": formula,
            "units": units,
            "use": use,
            "status": status,
            "claim_allowed": False,
        }
        for row_id, quantity, formula, units, use, status in specs
    ]


def budget_impact_rows(timestamp: str, budget_3713: list[dict[str, str]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for index, source_row in enumerate(budget_3713):
        right_piece = source_row["matter_only_pass_condition"].split("<=", 1)[1].strip()
        rows.append({
            **base(timestamp),
            "impact_id": f"BI3714_{index}_{source_row['budget_id']}",
            "budget_role": source_row["budget_role"],
            "lambda_um": source_row["lambda_um"],
            "exact_kernel_matter_result": "T_matter*epsilon_qH = 0",
            "finite_mismatch_condition": f"T_matter*(epsilon_Dq + ||Dq_obs|| ||Delta_P_H||) <= {right_piece}",
            "status": "NONCLAIM_BUDGET_IMPACT_READY",
            "claim_allowed": False,
        })
    return rows


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("DEC3714_0_projector_constructed", "A concrete kernel selector is now written: P_ker=I-A_G^dagger A.", "This is the non-smuggled way to make Dq_obs P_H=0: construct P_H as the quotient-kernel projector.", "KERNEL_PROJECTOR_FORM_DERIVED"),
        ("DEC3714_1_zero_conditional", "epsilon_qH=0 follows exactly if P_H=P_ker and the q_obs/G_H/closed-range/selector hypotheses are parent-signed.", "The zero is mathematical, but the owner clauses are still not all signed for current MTS.", "ZERO_VALUE_CONDITIONAL_ONLY"),
        ("DEC3714_2_finite_pack", "If P_H is not exactly P_ker, the finite row is epsilon_qH <= epsilon_Dq + ||Dq_obs|| ||Delta_P_H||.", "This makes leakage a real coefficient pack rather than a vague coupling worry.", "FINITE_EPSILON_PACK_DERIVED"),
        ("DEC3714_3_next", "Next target should test local dynamics compatibility: does L_H preserve the kernel projection?", "Matter silence is not enough; the local mass-gap/Green operator must not immediately drive the mode out of ker(Dq_obs).", "ADVANCE_TO_LH_KERNEL_COMPATIBILITY"),
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
        ("CG3714_0_qobs", "q_obs/Dq_obs are parent-owned with declared observed quotient norm"),
        ("CG3714_1_GH", "G_H is parent-owned and positive with units compatible with Dq_obs"),
        ("CG3714_2_closed_range", "A G_H^-1 A^* pseudoinverse is mathematically controlled"),
        ("CG3714_3_PH", "P_H=P_ker is parent-selected before empirical scoring"),
        ("CG3714_4_LH", "L_H preserves ker(Dq_obs) or commutator leakage epsilon_LP is bounded"),
        ("CG3714_5_public", "epsilon_qH=0 matter-coupling silence claim allowed"),
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
            "status_id": "STATUS3714_0",
            "status": "PH_KERNEL_PROJECTOR_CONSTRUCTED_EPSILON_QH_ZERO_CONDITIONAL_FINITE_PACK_READY",
            "summary": (
                "3714 constructs the canonical kernel projector P_ker=I-A_G^dagger A with A=Dq_obs. "
                "If P_H is parent-selected as P_ker, Dq_obs P_H=0 and epsilon_qH=0. "
                "If not, epsilon_qH is bounded by epsilon_Dq + ||Dq_obs|| ||Delta_P_H||. Claims remain blocked pending q_obs/G_H/closed-range/selector and L_H compatibility owners."
            ),
            "claim_allowed": False,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "next_id": "NEXT3714_0",
            "target_doc": "3715-Y5-R2FR-kernel-projected-local-operator-compatibility-or-commutator-leak.md",
            "target_script": "scripts/Y5_R2FR_3715_kernel_projected_local_operator_compatibility_or_commutator_leak.py",
            "objective": "test whether the local response operator L_H preserves ker(Dq_obs), i.e. [L_H,P_ker]=0, or retain epsilon_LP=||[L_H,P_ker]|| as the dynamics leakage row",
            "success_gate": "kernel-projected matter silence remains dynamically stable, or the commutator leakage is explicitly bounded as a nonclaim input",
            "claim_allowed": False,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    projectors: list[dict[str, object]],
    hypotheses: list[dict[str, object]],
    epsilon_pack: list[dict[str, object]],
    budget_impacts: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3714 Y5 R2FR P_H Kernel Selector Owner Or epsilon_qH Coefficient Pack",
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
        "- Let `A := Dq_obs|_0` and let `G_H` define the local field adjoint.",
        "- Define `A_G^dagger := G_H^-1 A^* (A G_H^-1 A^*)^+`.",
        "- Define the kernel selector `P_ker := I - A_G^dagger A`.",
        "- Then `Dq_obs P_ker = 0` under the standard closed-range/pseudoinverse hypotheses.",
        "- Therefore selecting `P_H := P_ker` gives `epsilon_qH=0` exactly, but only if the parent owns `q_obs`, `G_H`, and the selector before scoring.",
        "- If the exact selector is unavailable, the retained finite row is `epsilon_qH <= epsilon_Dq + ||Dq_obs|| ||Delta_P_H||`.",
        "- `valid_for_claim=false`: this is a kernel-construction route and coefficient pack, not a local-GR/R10 pass.",
        "",
        "## Projector Construction",
        "",
    ]
    for row in projectors:
        lines.append(f"- `{row['projector_id']}` `{row['status']}`: `{row['formula']}` | {row['meaning']}")
    lines.extend(["", "## Required Hypotheses", ""])
    for row in hypotheses:
        lines.append(f"- `{row['hypothesis_id']}` `{row['status']}`: {row['requirement']} | gap: {row['remaining_gap']}")
    lines.extend(["", "## epsilon_qH Coefficient Pack", ""])
    for row in epsilon_pack:
        lines.append(f"- `{row['epsilon_pack_id']}` `{row['quantity']}`: `{row['formula_or_value']}` | {row['status']} | {row['use']}")
    lines.extend(["", "## Budget Impact", ""])
    for row in budget_impacts:
        lines.append(f"- `{row['impact_id']}` `{row['budget_role']}`: exact `{row['exact_kernel_matter_result']}`; finite `{row['finite_mismatch_condition']}`")
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
    projectors: list[dict[str, object]],
    hypotheses: list[dict[str, object]],
    epsilon_pack: list[dict[str, object]],
    budget_impacts: list[dict[str, object]],
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
    formulas = "\n".join(str(row["formula"]) for row in projectors)
    checks.append(("projector_formula", "P_ker formula is written", "P_ker := I - A_G^dagger A" in formulas, ""))
    checks.append(("zero_property", "Dq_obs P_ker zero property is written", "Dq_obs P_ker" in formulas and "0" in formulas, ""))
    gaps = {row["remaining_gap"] for row in hypotheses}
    checks.append(("hypotheses", "q_obs, G_H, closed-range, selector, and L_H hypotheses represented", {"MISSING_PARENT_QOBS_OWNER", "MISSING_GH_OWNER_AND_UNITS", "MISSING_CLOSED_RANGE_OR_REGULATOR", "MISSING_PH_PARENT_SELECTOR", "MISSING_LH_KERNEL_COMPATIBILITY"} <= gaps, ""))
    quantities = {row["quantity"] for row in epsilon_pack}
    checks.append(("epsilon_pack", "exact and finite epsilon_qH pack rows are present", {"epsilon_qH_exact", "Delta_P_H", "epsilon_qH_bound", "epsilon_LP"} <= quantities, ""))
    checks.append(("budget_impacts", "three budget impacts are generated", len(budget_impacts) == 3 and all(row["status"] == "NONCLAIM_BUDGET_IMPACT_READY" for row in budget_impacts), ""))
    checks.append(("nonclaim_decisions", "all decisions are nonclaim", all(row["claim_allowed"] is False for row in decisions), ""))
    checks.append(("claim_gates_blocked", "all claim gates blocked", all(row["status"] == "BLOCKED" and row["claim_allowed"] is False for row in claim_gates), ""))
    checks.append(("next_target_3715", "next target advances to L_H kernel compatibility", str(next_target[0]["target_doc"]).startswith("3715-") and "operator" in str(next_target[0]["target_doc"]), ""))
    doc_text = read_text(DOC) if DOC.exists() else ""
    checks.append(("doc_core_terms", "doc contains core 3714 terms", all(term in doc_text for term in ["P_ker := I - A_G^dagger A", "Dq_obs P_ker = 0", "epsilon_qH <= epsilon_Dq", "valid_for_claim=false"]), ""))
    formalization_leaks = list(FORMALIZATION.rglob("*3714*")) if FORMALIZATION.exists() else []
    checks.append(("no_formalization_leak", "no 3714 files were written into formalization-workbench", len(formalization_leaks) == 0, "; ".join(str(path) for path in formalization_leaks)))
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
    budget_3713 = parse_csv(BUDGET_3713)
    sources = source_register(timestamp)
    projectors = projector_rows(timestamp)
    hypotheses = hypothesis_rows(timestamp)
    epsilon_pack = epsilon_pack_rows(timestamp)
    budget_impacts = budget_impact_rows(timestamp, budget_3713)
    decisions = decision_rows(timestamp)
    claim_gates = claim_gate_rows(timestamp)
    status = status_rows(timestamp)
    next_target = next_rows(timestamp)

    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3714_SOURCE_REGISTER.csv",
        "projectors": RESIDUALS / "P8_Y5_R2FR_3714_KERNEL_PROJECTOR_DERIVATION_ROWS.csv",
        "hypotheses": RESIDUALS / "P8_Y5_R2FR_3714_REQUIRED_HYPOTHESIS_ROWS.csv",
        "epsilon_pack": RESIDUALS / "P8_Y5_R2FR_3714_EPSILON_QH_COEFFICIENT_PACK.csv",
        "budget_impacts": RESIDUALS / "P8_Y5_R2FR_3714_BUDGET_IMPACT_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3714_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3714_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3714_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3714_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3714_VALIDATION.csv",
    }

    write_csv(outputs["sources"], sources)
    write_csv(outputs["projectors"], projectors)
    write_csv(outputs["hypotheses"], hypotheses)
    write_csv(outputs["epsilon_pack"], epsilon_pack)
    write_csv(outputs["budget_impacts"], budget_impacts)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["claim_gates"], claim_gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, projectors, hypotheses, epsilon_pack, budget_impacts, decisions, claim_gates, status, next_target)

    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(generated_paths, sources, projectors, hypotheses, epsilon_pack, budget_impacts, decisions, claim_gates, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3714 validation failed: {failures}", file=sys.stderr)
        return 1
    print("wrote 3714 checkpoint: P_H kernel selector and epsilon_qH coefficient pack generated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
