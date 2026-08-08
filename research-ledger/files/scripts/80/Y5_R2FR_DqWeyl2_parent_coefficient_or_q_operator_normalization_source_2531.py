from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BRANCH_ID = "MTS_R2FR_DQWEYL2_COEFFICIENT_OR_Q_OPERATOR_2531"
CHECKPOINT_ID = "2531"
DOC = ROOT / "2531-Y5-R2FR-DqWeyl2-parent-coefficient-or-q-operator-normalization-source.md"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2531_SOURCE_REGISTER.csv",
    "coefficient_audit": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2531_DQWEYL2_COEFFICIENT_AUDIT.csv",
    "q_operator_audit": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2531_Q_OPERATOR_NORMALIZATION_AUDIT.csv",
    "finite_formula": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2531_FINITE_RESIDUAL_FORMULA_LEDGER.csv",
    "branch_decision": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2531_BRANCH_DECISION.csv",
    "claim_gates": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2531_CLAIM_GATES.csv",
    "refusal_runner": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2531_REFUSAL_RUNNER.csv",
    "next_target": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2531_NEXT_TARGET.csv",
    "branch_copies": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2531_BRANCH_COPIES.csv",
    "validation": MTS_RESIDUALS / "P8_Y5_BRR545_2531_VALIDATION.csv",
}

BRANCH_COPIES = {
    "coefficient_audit": ROOT
    / "source-intake"
    / "beta-source"
    / "docs"
    / "DqWeyl2_coefficient_audit_2531_NONCLAIM.csv",
    "q_operator_audit": ROOT
    / "source-intake"
    / "local_bounds"
    / "q_operator_normalization_2531_NONCLAIM.csv",
    "finite_formula": ROOT
    / "source-intake"
    / "rab-sector"
    / "acquisition-queue"
    / "DqWeyl2_finite_formula_2531_NONCLAIM.csv",
    "next_target": ROOT
    / "source-intake"
    / "rab-sector"
    / "acquisition-queue"
    / "JQ2531_NEXT_TARGET_NONCLAIM.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": utc_now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": "False",
        "claim_allowed": "False",
        **row,
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def contains(path: Path, needle: str) -> bool:
    return needle in read_text(path)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


SOURCE_SPECS = [
    {
        "source_id": "SRC2531_0_2530_doc",
        "source_path": "2530-Y5-R2FR-q-representation-no-Weyl-spurion-or-BqWeyl-bound-row.md",
        "needle": "NEXT2530_0_selected",
        "role": "current handoff selecting quadratic Weyl coefficient/operator target",
    },
    {
        "source_id": "SRC2531_1_2530_validation",
        "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2530_VALIDATION.csv",
        "needle": "VAL2530_OVERALL,PASS",
        "role": "2530 validation anchor",
    },
    {
        "source_id": "SRC2531_2_2366_doc",
        "source_path": "2366-Y5-R2FR-DqWeyl2-parent-coefficient-or-q-operator-normalization-source.md",
        "needle": "DQC2366_4_verdict",
        "role": "quadratic Weyl coefficient precedent",
    },
    {
        "source_id": "SRC2531_3_2366_validation",
        "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2366_VALIDATION.csv",
        "needle": "VAL2366_OVERALL,PASS",
        "role": "2366 validation anchor",
    },
    {
        "source_id": "SRC2531_4_2366_coeff",
        "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2366_DQWEYL2_COEFFICIENT_AUDIT.csv",
        "needle": "DQC2366_4_verdict",
        "role": "D_qWeyl2 coefficient audit",
    },
    {
        "source_id": "SRC2531_5_2366_qop",
        "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2366_Q_OPERATOR_NORMALIZATION_AUDIT.csv",
        "needle": "QON2366_5_verdict",
        "role": "q operator normalization audit",
    },
    {
        "source_id": "SRC2531_6_2366_formula",
        "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2366_FINITE_RESIDUAL_FORMULA_LEDGER.csv",
        "needle": "FRF2366_5_verdict",
        "role": "finite residual formula ledger",
    },
    {
        "source_id": "SRC2531_7_2367_doc",
        "source_path": "2367-Y5-R2FR-jq-source-leg-zero-theorem-or-finite-source-pack.md",
        "needle": "JQZ2367_4_verdict",
        "role": "next source numerator precedent",
    },
    {
        "source_id": "SRC2531_8_2367_validation",
        "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2367_VALIDATION.csv",
        "needle": "VAL2367_OVERALL,PASS",
        "role": "2367 validation anchor",
    },
]


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = ROOT / spec["source_path"]
        rows.append(
            stamp(
                {
                    **spec,
                    "path_exists": str(path.exists()),
                    "needle_found": str(contains(path, spec["needle"])),
                    "status": "SOURCE_OK" if path.exists() and contains(path, spec["needle"]) else "SOURCE_BLOCKED",
                }
            )
        )
    return rows


def coefficient_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "DQC2531_0_definition",
            "coefficient": "D_qWeyl2",
            "status": "DEFINED_REQUIRED_INPUT",
            "effect": "q C_abcd C^abcd branch is explicit",
        },
        {
            "row_id": "DQC2531_1_zero_route",
            "coefficient": "D_qWeyl2=0",
            "status": "ZERO_ROUTE_NOT_DERIVED",
            "effect": "no-higher-curvature/no-regeneration theorem remains unsigned",
        },
        {
            "row_id": "DQC2531_2_numeric_route",
            "coefficient": "finite D_qWeyl2",
            "status": "NO_NUMERIC_SOURCE_FOUND",
            "effect": "no inspected source supplies a parent coefficient value",
        },
        {
            "row_id": "DQC2531_3_kernel",
            "coefficient": "C2 exterior source kernel",
            "status": "ANALYTIC_KERNEL_READY_NONCLAIM",
            "effect": "kernel is plumbing only without D_qWeyl2 and q operator normalization",
        },
        {
            "row_id": "DQC2531_4_verdict",
            "coefficient": "DqWeyl2 coefficient status",
            "status": "COEFFICIENT_UNSOURCED",
            "effect": "cannot score R10/PPN/orbital/clock/local-GR branch",
        },
    ]
    return [stamp(row) for row in rows]


def q_operator_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "QON2531_0_qX_bridge",
            "object": "q=aX identity bridge",
            "status": "BRIDGE_FORMULA_EXACT_IF_SIGNED_NOT_SIGNED",
            "missing": "scale a, shared domain, X coefficients and same-branch proof",
        },
        {
            "row_id": "QON2531_1_independent_q",
            "object": "independent physical q Hessian",
            "status": "FALLBACK_BRANCH_ACTIVE_NONCLAIM",
            "missing": "Z_q, M_q^2, D_qWeyl2, J_q and boundary/source rows",
        },
        {
            "row_id": "QON2531_2_conditional_mass",
            "object": "M_q^2",
            "status": "CONDITIONAL_FORMULA_IMPORTED",
            "missing": "selector/parent Hessian is not signed or numeric",
        },
        {
            "row_id": "QON2531_3_conditional_stiffness",
            "object": "Z_q",
            "status": "CONDITIONAL_FORMULA_IMPORTED",
            "missing": "xi_q and domain are not source-backed",
        },
        {
            "row_id": "QON2531_4_range",
            "object": "lambda_q",
            "status": "EXACT_CONDITIONAL_RATIO_NONCLAIM",
            "missing": "range not free, but xi_q is unsourced",
        },
        {
            "row_id": "QON2531_5_verdict",
            "object": "q operator normalization",
            "status": "PARTIAL_CONDITIONAL_OPERATOR_NOT_CLAIM_GRADE",
            "missing": "next bottleneck is the source numerator/coupling vector",
        },
    ]
    return [stamp(row) for row in rows]


def finite_formula_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "FRF2531_0_dynamic_kernel",
            "formula_piece": "dynamic massive q branch",
            "status": "FORMAL_KERNEL_CONDITIONAL",
            "missing": "xi_q, Z_q normalization, boundary/domain, source vector and P_obs",
        },
        {
            "row_id": "FRF2531_1_source_vector",
            "formula_piece": "quadratic Weyl plus source legs",
            "status": "SOURCE_VECTOR_SYMBOLIC",
            "missing": "each source component must be zero-proved or bounded absolutely",
        },
        {
            "row_id": "FRF2531_2_compact_source_response",
            "formula_piece": "compact source far field",
            "status": "PROFILE_SHAPE_READY_INPUTS_MISSING",
            "missing": "Q_q_eff is unsourced because D_qWeyl2 and J_q are missing",
        },
        {
            "row_id": "FRF2531_3_algebraic_limit",
            "formula_piece": "auxiliary/algebraic q branch",
            "status": "EXACT_CONDITIONAL_FORMULA_INPUTS_MISSING",
            "missing": "j_q and Hessian denominator are not source-backed",
        },
        {
            "row_id": "FRF2531_4_closure_control",
            "formula_piece": "q=0 benchmark",
            "status": "BENCHMARK_ONLY",
            "missing": "not a derivation of GR/Newton",
        },
        {
            "row_id": "FRF2531_5_verdict",
            "formula_piece": "local residual formula status",
            "status": "SELECT_NUMERATOR_SOURCE_LEG_NEXT",
            "missing": "j_q controls whether finite q branch is harmless or testable",
        },
    ]
    return [stamp(row) for row in rows]


def branch_decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "BRD2531_0_no_tower",
            "route": "no-higher-curvature/no-regeneration theorem",
            "priority": "1",
            "decision": "KEEP_OPEN_UNSIGNED",
            "reason": "would kill D_qWeyl2, but no parent object-language source signs it",
        },
        {
            "row_id": "BRD2531_1_kernel_plumbing",
            "route": "analytic exterior Weyl2 kernel",
            "priority": "2",
            "decision": "RETAIN_NONCLAIM_PLUMBING",
            "reason": "useful only after D_qWeyl2 and L_q/G_q are sourced",
        },
        {
            "row_id": "BRD2531_2_independent_q",
            "route": "independent q Hessian/bound runner",
            "priority": "2",
            "decision": "ACTIVE_FALLBACK_NONCLAIM",
            "reason": "finite bound lane stays active while qX bridge and selector remain unsigned",
        },
        {
            "row_id": "BRD2531_3_DqWeyl2",
            "route": "quadratic Weyl coefficient scoring",
            "priority": "4",
            "decision": "BLOCKED_INPUTS_MISSING",
            "reason": "D_qWeyl2 and operator/projection rows are not source-backed",
        },
        {
            "row_id": "BRD2531_4_jq",
            "route": "source numerator j_q",
            "priority": "1",
            "decision": "SELECT_NEXT",
            "reason": "denominator/kernel shape is conditionally sharpened; numerator decides harmless vs testable branch",
        },
        {
            "row_id": "BRD2531_5_empirical",
            "route": "R10/PPN/clock/orbital scoring",
            "priority": "5",
            "decision": "DEFER",
            "reason": "no claim-grade prediction vector exists",
        },
    ]
    return [stamp(row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "CG2531_0_DqWeyl2_zero",
            "claim": "D_qWeyl2 theorem-zero",
            "allowed": "False",
            "blocked_by": "DQC2531_1_zero_route;BRD2531_0_no_tower",
        },
        {
            "row_id": "CG2531_1_DqWeyl2_numeric",
            "claim": "D_qWeyl2 finite coefficient is score-ready",
            "allowed": "False",
            "blocked_by": "DQC2531_2_numeric_route;QON2531_5_verdict",
        },
        {
            "row_id": "CG2531_2_q_operator",
            "claim": "q operator normalization is claim-grade",
            "allowed": "False",
            "blocked_by": "QON2531_0_qX_bridge;QON2531_1_independent_q;QON2531_3_conditional_stiffness",
        },
        {
            "row_id": "CG2531_3_local_GR_Newton",
            "claim": "local GR/Newton branch derived",
            "allowed": "False",
            "blocked_by": "CG2531_0_DqWeyl2_zero;CG2531_1_DqWeyl2_numeric;j_q_source_leg",
        },
        {
            "row_id": "CG2531_4_public_or_github",
            "claim": "public/GitHub update recommended from 2531",
            "allowed": "False",
            "blocked_by": "D_qWeyl2, q operator and j_q source rows remain nonclaim",
        },
    ]
    return [stamp(row) for row in rows]


def refusal_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "REF2531_0_kernel_as_evidence",
            "shortcut": "treat analytic Weyl2 kernel as evidence of a prediction",
            "verdict": "REJECT",
            "reason": "kernel needs D_qWeyl2, q operator and source normalization",
        },
        {
            "row_id": "REF2531_1_linear_kill_erases_quadratic",
            "shortcut": "use linear Weyl index lemma to kill q C^2",
            "verdict": "REJECT",
            "reason": "quadratic Weyl scalars are legal unless higher-curvature/no-regeneration grammar forbids them",
        },
        {
            "row_id": "REF2531_2_free_lambda_q",
            "shortcut": "treat lambda_q as a free fit knob",
            "verdict": "REJECT",
            "reason": "lambda_q is a conditional ratio from Z_q/M_q^2 or xi_q; it needs source-backed normalization",
        },
        {
            "row_id": "REF2531_3_skip_jq",
            "shortcut": "score denominator/kernel before source numerator",
            "verdict": "REJECT",
            "reason": "j_q controls whether the finite branch is harmless or observable",
        },
        {
            "row_id": "REF2531_4_public_claim",
            "shortcut": "present DqWeyl2 plumbing as local-GR derivation",
            "verdict": "REJECT",
            "reason": "plumbing is not a zero theorem or a sourced prediction vector",
        },
    ]
    return [stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "NEXT2531_0_selected",
            "priority": "selected",
            "next_target": "2532-Y5-R2FR-jq-source-leg-zero-theorem-or-finite-source-pack.md",
            "script": "scripts/Y5_R2FR_jq_source_leg_zero_theorem_or_finite_source_pack_2532.py",
            "objective": "derive j_q=0 from parent matter/source/current descent in the same observed coframe, or stage finite j_q/body/boundary/tail rows with units and arena projections",
            "acceptance_gate": "j_q source numerator is theorem-zero or every surviving source leg is explicit finite nonclaim with source paths, units and no-cancellation guard",
            "do_not": "do not skip numerator; do not claim local GR/Newton; do not score symbolic j_q placeholders",
        },
        {
            "row_id": "NEXT2531_1_parallel",
            "priority": "parallel_nonclaim",
            "next_target": "2532b-Y5-R2FR-no-higher-curvature-object-language-adoption-certificate.md",
            "script": "scripts/Y5_R2FR_no_higher_curvature_object_language_adoption_certificate_2532b.py",
            "objective": "attempt direct parent adoption of no-Weyl2/no-regeneration grammar",
            "acceptance_gate": "parent action object-language excludes q C^2, q C*Cdual and regenerated hidden-visible coefficient morphisms",
            "do_not": "do not ban higher curvature by taste",
        },
    ]
    return [stamp(row) for row in rows]


def branch_copy_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    copies = [
        ("coefficient_audit", OUTPUTS["coefficient_audit"], BRANCH_COPIES["coefficient_audit"]),
        ("q_operator_audit", OUTPUTS["q_operator_audit"], BRANCH_COPIES["q_operator_audit"]),
        ("finite_formula", OUTPUTS["finite_formula"], BRANCH_COPIES["finite_formula"]),
        ("next_target", OUTPUTS["next_target"], BRANCH_COPIES["next_target"]),
    ]
    for copy_id, source, destination in copies:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            stamp(
                {
                    "copy_id": copy_id,
                    "source_path": str(source.relative_to(ROOT)),
                    "destination_path": str(destination.relative_to(ROOT)),
                    "destination_exists": str(destination.exists()),
                    "status": "COPIED_NONCLAIM",
                }
            )
        )
    return rows


def any_claim_enabled(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    truthy = {"true", "yes", "1", "claim_ready", "score_ready"}
    for rows in rows_by_name.values():
        for row in rows:
            for key, value in row.items():
                if key in {"path_exists", "needle_found", "destination_exists"}:
                    continue
                if key in {"valid_for_claim", "claim_allowed", "allowed", "claim_ready"} and str(value).strip().lower() in truthy:
                    return True
    return False


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = []
    sources = rows_by_name["source_register"]
    checks.append(("VAL2531_00_sources_exist", all(row["path_exists"] == "True" for row in sources), "every required source path exists"))
    checks.append(("VAL2531_01_source_needles", all(row["needle_found"] == "True" for row in sources), "all required source needles found"))
    checks.append(("VAL2531_02_coeff_unsourced", any(row["row_id"] == "DQC2531_4_verdict" and row["status"] == "COEFFICIENT_UNSOURCED" for row in rows_by_name["coefficient_audit"]), "DqWeyl2 coefficient remains unsourced"))
    checks.append(("VAL2531_03_operator_nonclaim", any(row["row_id"] == "QON2531_5_verdict" and row["status"] == "PARTIAL_CONDITIONAL_OPERATOR_NOT_CLAIM_GRADE" for row in rows_by_name["q_operator_audit"]), "q operator normalization remains nonclaim"))
    checks.append(("VAL2531_04_formula_selects_jq", any(row["row_id"] == "FRF2531_5_verdict" and row["status"] == "SELECT_NUMERATOR_SOURCE_LEG_NEXT" for row in rows_by_name["finite_formula"]), "finite formula selects source numerator next"))
    checks.append(("VAL2531_05_branch_selects_jq", any(row["row_id"] == "BRD2531_4_jq" and row["decision"] == "SELECT_NEXT" for row in rows_by_name["branch_decision"]), "branch decision selects j_q next"))
    checks.append(("VAL2531_06_claim_gates_blocked", all(row["allowed"] == "False" for row in rows_by_name["claim_gates"]), "all claim gates blocked"))
    checks.append(("VAL2531_07_refusals_cover_shortcuts", len(rows_by_name["refusal_runner"]) >= 5 and all("REJECT" in row["verdict"] for row in rows_by_name["refusal_runner"]), "shortcuts refused"))
    checks.append(("VAL2531_08_next_selected", any(row["row_id"] == "NEXT2531_0_selected" and "jq" in row["next_target"].lower() for row in rows_by_name["next_target"]), "j_q next target selected"))
    checks.append(("VAL2531_09_no_claim_flags", not any_claim_enabled(rows_by_name), "no generated row enables claim flags"))
    checks.append(("VAL2531_10_branch_copies", all(row["destination_exists"] == "True" for row in rows_by_name["branch_copies"]), "branch copies exist"))
    checks.append(("VAL2531_11_no_formalization_artifacts", not any("formalization-workbench" in str(path).lower() for path in [DOC, *OUTPUTS.values(), *BRANCH_COPIES.values()]), "no outputs target formalization-workbench"))
    checks.append(("VAL2531_12_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"))

    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        try:
            parsed = csv_rows(path)
            checks.append((f"VAL2531_CSV_{path.stem}", len(parsed) > 0, f"{path.name} parses"))
        except Exception as exc:
            checks.append((f"VAL2531_CSV_{path.stem}", False, f"{path.name} parse failed: {exc}"))
    for copy_id, path in BRANCH_COPIES.items():
        try:
            parsed = csv_rows(path)
            checks.append((f"VAL2531_COPY_CSV_{copy_id}", len(parsed) > 0, f"{path.name} parses"))
        except Exception as exc:
            checks.append((f"VAL2531_COPY_CSV_{copy_id}", False, f"{path.name} parse failed: {exc}"))

    overall = all(ok for _, ok, _ in checks)
    checks.append(
        (
            "VAL2531_OVERALL",
            overall,
            "2531 consolidates the quadratic Weyl branch: D_qWeyl2 is unsourced, q operator normalization is conditional/nonclaim, and the next live local-GR bottleneck is j_q source numerator.",
        )
    )
    return [stamp({"check_id": check_id, "status": "PASS" if ok else "FAIL", "details": detail}) for check_id, ok, detail in checks]


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def slim(rows: list[dict[str, Any]], columns: list[str]) -> list[dict[str, Any]]:
    return [{column: row.get(column, "") for column in columns} for row in rows]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 2531 - `D_qWeyl2` Parent Coefficient or q Operator Normalization Source",
                "**Current verdict:** the quadratic Weyl branch is consolidated but not closed. `D_qWeyl2` is defined as the required coefficient, but it is neither theorem-zero nor numerically sourced. The exterior Weyl-squared kernel is useful plumbing, not evidence.",
                "**Main gain:** the denominator/operator side is less foggy: `lambda_q` is not a free knob if `Z_q/M_q^2` or `xi_q` is parent-owned. But those inputs are still unsourced, so the next high-value blocker is the numerator/source leg `j_q`.",
                "**Claim discipline:** no local-GR/Newton/R10/PPN/clock/orbital/GitHub claim is allowed from 2531. This checkpoint keeps the quadratic Weyl and q-operator rows nonclaim and selects the source numerator next.",
                "## Source Register",
                markdown_table(
                    slim(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "needle_found", "status", "role"]),
                    ["source_id", "source_path", "path_exists", "needle_found", "status", "role"],
                ),
                "## `D_qWeyl2` Coefficient Audit",
                markdown_table(
                    slim(rows_by_name["coefficient_audit"], ["row_id", "coefficient", "status", "effect"]),
                    ["row_id", "coefficient", "status", "effect"],
                ),
                "## q Operator Normalization Audit",
                markdown_table(
                    slim(rows_by_name["q_operator_audit"], ["row_id", "object", "status", "missing"]),
                    ["row_id", "object", "status", "missing"],
                ),
                "## Finite Residual Formula Ledger",
                markdown_table(
                    slim(rows_by_name["finite_formula"], ["row_id", "formula_piece", "status", "missing"]),
                    ["row_id", "formula_piece", "status", "missing"],
                ),
                "## Branch Decision",
                markdown_table(
                    slim(rows_by_name["branch_decision"], ["row_id", "route", "priority", "decision", "reason"]),
                    ["row_id", "route", "priority", "decision", "reason"],
                ),
                "## Claim Gates",
                markdown_table(
                    slim(rows_by_name["claim_gates"], ["row_id", "claim", "allowed", "blocked_by"]),
                    ["row_id", "claim", "allowed", "blocked_by"],
                ),
                "## Refusal Runner",
                markdown_table(
                    slim(rows_by_name["refusal_runner"], ["row_id", "shortcut", "verdict", "reason"]),
                    ["row_id", "shortcut", "verdict", "reason"],
                ),
                "## Next Target",
                markdown_table(
                    slim(rows_by_name["next_target"], ["row_id", "priority", "next_target", "script", "objective", "acceptance_gate", "do_not"]),
                    ["row_id", "priority", "next_target", "script", "objective", "acceptance_gate", "do_not"],
                ),
                "## Branch Copies",
                markdown_table(
                    slim(rows_by_name["branch_copies"], ["copy_id", "source_path", "destination_path", "destination_exists", "status"]),
                    ["copy_id", "source_path", "destination_path", "destination_exists", "status"],
                ),
                "## Validation",
                markdown_table(
                    slim(rows_by_name["validation"], ["check_id", "status", "details"]),
                    ["check_id", "status", "details"],
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    remove_pycache()
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "coefficient_audit": coefficient_rows(),
        "q_operator_audit": q_operator_rows(),
        "finite_formula": finite_formula_rows(),
        "branch_decision": branch_decision_rows(),
        "claim_gates": claim_gate_rows(),
        "refusal_runner": refusal_rows(),
        "next_target": next_target_rows(),
    }
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    remove_pycache()

    print(f"wrote {DOC}")
    for name, path in OUTPUTS.items():
        print(f"wrote {name}: {path}")
    for key, path in BRANCH_COPIES.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
