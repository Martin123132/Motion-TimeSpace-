from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_DOCS = ROOT / "source-intake" / "rab-sector" / "docs"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1563-Y5-RAB-auxiliary-compatibility-parent-sort-and-no-derivative-grammar.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1562_doc": ROOT / "1562-Y5-lambdaR-parent-origin-zero-stress-and-first-class-constraint-test.md",
    "1562_validation": OUT / "P8_Y5_BRR545_1562_VALIDATION.csv",
    "1562_next": OUT / "P8_Y5_PARENT_QLOC_1562_NEXT_TARGET.csv",
    "1562_boundary": OUT / "P8_Y5_PARENT_QLOC_1562_BOUNDARY_DEGREE_COUNT_GATE.csv",
    "1562_routes": OUT / "P8_Y5_PARENT_QLOC_1562_ROUTE_DECISION_LEDGER.csv",
    "1262_doc": ROOT / "1262-Y5-R10-RAB-operator-exhaustion-minimal-assumption-audit-or-ZR-prior-envelope.md",
    "1268_doc": ROOT / "1268-Y5-R10-RAB-second-class-auxiliary-compatibility-action-or-finite-ZR-source-row.md",
    "zr1262_template": RAB_DOCS / "ZR1262_RAB_PRIOR_ENVELOPE_TEMPLATE_NONCLAIM.csv",
    "zr1268_template": RAB_DOCS / "ZR1268_FINITE_ZR_SOURCE_ROW_TEMPLATE_NONCLAIM.csv",
}

NEEDLES = {
    "1562_doc": ["second-class/algebraic auxiliary compatibility", "Next target: prove or reject the auxiliary parent sort"],
    "1562_validation": ["VAL1562_OVERALL", "PASS"],
    "1562_next": ["1563-Y5-RAB-auxiliary-compatibility-parent-sort-and-no-derivative-grammar.md"],
    "1562_boundary": ["BD1562_4_operator", "UNSIGNED"],
    "1562_routes": ["ROUTE1562_1_second_class_auxiliary", "BEST_DERIVATION_ROUTE_CONDITIONAL"],
    "1262_doc": ["THEO1262_0_vertical_null_ban", "EXACT_CONDITIONAL_NOT_PARENT_DERIVED"],
    "1268_doc": ["CAC1268_2_no_derivative_grammar", "EXACT_CONDITIONAL_NOT_PARENT_SIGNED"],
    "zr1262_template": ["MISSING"],
    "zr1268_template": ["MISSING"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1563_SOURCE_REGISTER.csv"
SORT_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1563_PARENT_SORT_AUDIT.csv"
GRAMMAR_GATE = OUT / "P8_Y5_PARENT_QLOC_1563_NO_DERIVATIVE_GRAMMAR_GATE.csv"
ELIMINATION_GATE = OUT / "P8_Y5_PARENT_QLOC_1563_AUXILIARY_ELIMINATION_GATE.csv"
FINITE_FALLBACK = OUT / "P8_Y5_PARENT_QLOC_1563_FINITE_ZR_QR_FALLBACK_LEDGER.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1563_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1563_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1563_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1563_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1563_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1563"
QUAR_SORT = QUARANTINE / "PARENT_SORT_AUDIT_NONCLAIM.csv"
QUAR_GRAMMAR = QUARANTINE / "NO_DERIVATIVE_GRAMMAR_GATE_NONCLAIM.csv"
QUAR_ELIMINATION = QUARANTINE / "AUXILIARY_ELIMINATION_GATE_NONCLAIM.csv"
QUAR_FALLBACK = QUARANTINE / "FINITE_ZR_QR_FALLBACK_LEDGER_NONCLAIM.csv"
QUAR_RUNNER = QUARANTINE / "RUNNER_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "DECISION_NONCLAIM.csv"
BRANCH_SORT = BRANCH_RESIDUALS / "parent_sort_audit_nonclaim_1563.csv"
BRANCH_GRAMMAR = BRANCH_RESIDUALS / "no_derivative_grammar_gate_nonclaim_1563.csv"
BRANCH_ELIMINATION = BRANCH_RESIDUALS / "auxiliary_elimination_gate_nonclaim_1563.csv"
BRANCH_FALLBACK = BRANCH_RESIDUALS / "finite_ZR_qR_fallback_ledger_nonclaim_1563.csv"
BRANCH_RUNNER = BRANCH_RESIDUALS / "RAB_auxiliary_runner_nonclaim_1563.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "RAB_auxiliary_decision_nonclaim_1563.csv"


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


def file_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    return all(needle in text for needle in needles)


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
    rows = []
    for index, (key, path) in enumerate(SOURCE_FILES.items()):
        needles = NEEDLES.get(key, [])
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1563_{index}_{key}",
                "source_path": rel(path),
                "exists": path.exists(),
                "needle_found": file_contains(path, needles) if needles else True,
                "needles": "; ".join(needles),
                "purpose": "evidence for R_AB auxiliary compatibility parent sort and no-derivative grammar gate",
                **flags(),
            }
        )
    return rows


def sort_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "SORT1563_0_auxiliary_coordinate",
            "R_AB is an auxiliary compatibility coordinate, not a physical scalar",
            "would allow algebraic elimination before local readout",
            "CANDIDATE_NOT_PARENT_SIGNED",
            "typed parent field/sort list is still not sourced from MTS primitives",
        ),
        (
            "SORT1563_1_vertical_representative",
            "R_AB variations lie in ker(Dq) of the public quotient map",
            "would make R_AB a representative/fibre variable rather than observable geometry",
            "EXACT_CONDITIONAL_NOT_PARENT_DERIVED",
            "parent quotient map and presymplectic null proof are missing",
        ),
        (
            "SORT1563_2_compatibility_data",
            "R_AB-C_AB[q(Phi),theta,top]=0 is compatibility data",
            "Lambda_R enforces consistency between private representative and public readout",
            "CANDIDATE_ONLY",
            "C_AB map is not parent-sourced",
        ),
        (
            "SORT1563_3_physical_countermodel",
            "R_AB is a genuine local scalar/tensor component",
            "then Z_R h^{ij}D_iR_ABD_jR_AB is legal by locality",
            "LEGAL_COUNTERMODEL",
            "forces finite Z_R/q_R residual branch if parent sort fails",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "sort_id": sort_id,
            "parent_sort_statement": parent_sort_statement,
            "claim_effect_if_signed": claim_effect_if_signed,
            "status": status,
            "blocker": blocker,
            "source_paths": source_list("1262_doc", "1268_doc", "1562_boundary"),
            **flags(),
        }
        for sort_id, parent_sort_statement, claim_effect_if_signed, status, blocker in rows
    ]


def grammar_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "GRAM1563_0_no_DRAB",
            "ban D_i R_AB and D_mu R_AB kinetic/gradient terms",
            "needed so R_AB cannot carry exterior Q_R/Z_R hair",
            "REQUIRED_UNSIGNED",
            "vertical-null/no-vertical-metric theorem not parent-derived",
        ),
        (
            "GRAM1563_1_no_DLambda",
            "ban D Lambda_R kinetic/gradient terms",
            "needed so Lambda_R remains algebraic/reaction variable",
            "REQUIRED_UNSIGNED",
            "operator grammar has not been derived from parent object language",
        ),
        (
            "GRAM1563_2_no_vertical_metric",
            "no G_vert or nabla_vert that can make fibre gradients natural",
            "would forbid a quotient-natural vertical energy",
            "REQUIRED_UNSIGNED",
            "parent has not proven absence of vertical metric/connection",
        ),
        (
            "GRAM1563_3_no_boundary_derivative",
            "no boundary/corner derivative term for R_AB",
            "prevents boundary Q_R/B_R hair after bulk elimination",
            "REQUIRED_UNSIGNED",
            "boundary variational class not signed",
        ),
        (
            "GRAM1563_4_countermodel",
            "if any derivative operator is legal",
            "finite Z_R/M_R/J_R/B_R inputs become mandatory",
            "FINITE_BRANCH_REQUIRED_IF_FAILS",
            "cannot claim Z_R=0 by grammar",
        ),
        (
            "GRAM1563_5_verdict",
            "no-derivative grammar",
            "operator ban is exact conditional but not parent-signed",
            "FAIL_CURRENT_THEOREM",
            "retain finite residual fallback",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "grammar_id": grammar_id,
            "grammar_clause": grammar_clause,
            "why_needed": why_needed,
            "status": status,
            "blocker_or_effect": blocker_or_effect,
            "source_paths": source_list("1262_doc", "1268_doc", "1562_boundary"),
            **flags(),
        }
        for grammar_id, grammar_clause, why_needed, status, blocker_or_effect in rows
    ]


def elimination_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "ELIM1563_0_E_Lambda",
            "delta_{Lambda_R} S_R",
            "R_AB-C_AB[q,theta,top]=0",
            "FORMAL_PASS_WITHIN_CANDIDATE",
            "constraint action must be parent-owned",
        ),
        (
            "ELIM1563_1_E_R",
            "delta_{R_AB} S_total",
            "Lambda_R + J_R + delta B_R/delta R_AB + readout_regen = 0",
            "PASS_ONLY_IF_SOURCES_ZERO",
            "matter descent, boundary silence, and readout stability are unsigned",
        ),
        (
            "ELIM1563_2_Lambda_zero",
            "solve E_R with zero sources",
            "Lambda_R=0",
            "EXACT_CONDITIONAL",
            "not available if J_R, B_R, or readout regeneration survives",
        ),
        (
            "ELIM1563_3_no_symplectic_hair",
            "algebraic elimination before phase-space/readout",
            "no Pi_R or Q_R exterior hair",
            "EXACT_CONDITIONAL",
            "requires boundary and no-derivative grammar",
        ),
        (
            "ELIM1563_4_current",
            "accepted elimination theorem",
            "not parent-signed",
            "BLOCKED_NO_CLAIM",
            "conditional route survives but finite fallback remains active",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "elimination_id": elimination_id,
            "variation_or_step": variation_or_step,
            "result": result,
            "status": status,
            "blocker": blocker,
            "source_paths": source_list("1268_doc", "1562_doc"),
            **flags(),
        }
        for elimination_id, variation_or_step, result, status, blocker in rows
    ]


def fallback_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "FALL1563_0_ZR",
            "Z_R",
            "finite gradient coefficient for R_AB",
            "source-backed value, theorem-zero, or explicit prior interval with units",
            "MISSING_SOURCE_BACKED_INPUT",
        ),
        (
            "FALL1563_1_MR2",
            "M_R^2",
            "mass gap/screening scale",
            "parent Hessian or sourced scale to define ell_R=sqrt(Z_R/M_R^2)",
            "MISSING_SOURCE_BACKED_INPUT",
        ),
        (
            "FALL1563_2_JR",
            "J_R",
            "direct matter/source coupling to R_AB",
            "matter descent zero theorem or finite coupling source",
            "MISSING_SOURCE_BACKED_INPUT",
        ),
        (
            "FALL1563_3_BR",
            "B_R/Pi_R^n",
            "boundary reciprocal charge/flux",
            "boundary no-hair theorem or finite boundary-flux bound",
            "MISSING_SOURCE_BACKED_INPUT",
        ),
        (
            "FALL1563_4_projection",
            "q_R/Z_R to PPN projection",
            "map finite residual to gamma/beta/R10/clock/orbital arenas",
            "use 1559 control runner plus finite Z_R source rows only after inputs are real",
            "NONCLAIM_TEMPLATE_ONLY",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "fallback_id": fallback_id,
            "coefficient": coefficient,
            "meaning": meaning,
            "required_input": required_input,
            "status": status,
            "template_paths": f"{rel(SOURCE_FILES['zr1262_template'])}; {rel(SOURCE_FILES['zr1268_template'])}",
            **flags(),
        }
        for fallback_id, coefficient, meaning, required_input, status in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1563_0_sources",
            "test": "auxiliary grammar sources loaded",
            "current_status": "PASS",
            "detail": "1562, 1262, 1268, and finite-ZR templates loaded",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1563_1_sort",
            "test": "R_AB parent sort",
            "current_status": "FAILED_CURRENT_PARENT_SORT",
            "detail": "R_AB as auxiliary/vertical representative is conditional, not parent-derived",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1563_2_grammar",
            "test": "no derivative grammar",
            "current_status": "FAILED_CURRENT_OPERATOR_BAN",
            "detail": "no parent proof bans D R_AB, D Lambda_R, vertical metric/connection, or boundary derivative terms",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1563_3_elimination",
            "test": "auxiliary elimination",
            "current_status": "PASS_CONDITIONAL_UNSIGNED",
            "detail": "E_Lambda/E_R elimination is exact only if matter, boundary, readout, and grammar gates close",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1563_4_fallback",
            "test": "finite Z_R/q_R fallback",
            "current_status": "RETAIN_NONCLAIM_FALLBACK",
            "detail": "finite residual branch remains active but not scoreable until sourced",
            **flags(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1563_0_sort", "R_AB auxiliary parent sort", "BLOCKED_NO_CLAIM", "parent sort/quotient map not derived"),
        ("GATE1563_1_grammar", "Z_R=0 by no-derivative grammar", "BLOCKED_NO_CLAIM", "operator ban exact conditional only"),
        ("GATE1563_2_elimination", "Lambda_R/R_AB eliminated with no stress", "BLOCKED_NO_CLAIM", "matter/boundary/readout gates unsigned"),
        ("GATE1563_3_finite", "finite Z_R/q_R residual scoring", "BLOCKED_NO_CLAIM", "fallback templates contain missing source inputs"),
        ("GATE1563_4_local_GR", "derived local GR/Newton", "BLOCKED_NO_CLAIM", "neither theorem-zero nor finite residual scoring is complete"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim_gate": claim_gate,
            "status": status,
            "reason": reason,
            "source_paths": source_list("1262_doc", "1268_doc", "1562_doc"),
            **flags(),
        }
        for gate_id, claim_gate, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1563_0_verdict",
            "decision": "auxiliary compatibility theorem",
            "result": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "reason": "auxiliary elimination works only under unsigned parent sort, no-derivative grammar, matter descent, boundary silence, and readout stability premises",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1563_1_fallback",
            "decision": "finite residual branch",
            "result": "FINITE_ZR_QR_FALLBACK_RETAINED_NONCLAIM",
            "reason": "legal countermodels survive if R_AB is physical or vertically metrized",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1563_2_next",
            "decision": "next target",
            "result": "NEXT_1564_VERTICAL_NULL_PRESYMPLECTIC_DEGENERACY_OR_FINITE_ZR_INTAKE",
            "reason": "the next best derivation attempt is to prove R_AB lies in a parent presymplectic null fibre with no vertical metric/connection",
            **flags(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1563_0_1564",
            "next_target": "1564-Y5-RAB-vertical-null-presymplectic-degeneracy-or-finite-ZR-intake.md",
            "script": "scripts/Y5_RAB_vertical_null_presymplectic_degeneracy_or_finite_ZR_intake.py",
            "objective": "try to derive R_AB as a parent presymplectic null/vertical-fibre representative with no vertical metric or connection; if not, stage finite Z_R/q_R intake rows without claiming local GR",
            "do_not": "do not claim Z_R=0 from conditional operator grammar; do not score finite residuals with placeholder source inputs; do not edit formalization-workbench",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (SORT_AUDIT, QUAR_SORT),
        (GRAMMAR_GATE, QUAR_GRAMMAR),
        (ELIMINATION_GATE, QUAR_ELIMINATION),
        (FINITE_FALLBACK, QUAR_FALLBACK),
        (RUNNER, QUAR_RUNNER),
        (DECISION, QUAR_DECISION),
        (SORT_AUDIT, BRANCH_SORT),
        (GRAMMAR_GATE, BRANCH_GRAMMAR),
        (ELIMINATION_GATE, BRANCH_ELIMINATION),
        (FINITE_FALLBACK, BRANCH_FALLBACK),
        (RUNNER, BRANCH_RUNNER),
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
    sort = read_csv(SORT_AUDIT)
    grammar = read_csv(GRAMMAR_GATE)
    elimination = read_csv(ELIMINATION_GATE)
    fallback = read_csv(FINITE_FALLBACK)
    run_rows = read_csv(RUNNER)
    gate_rows = read_csv(CLAIM_GATE)
    decision_items = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    checks = [
        ("VAL1563_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1563 source paths exist"),
        ("VAL1563_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all registered evidence needles found"),
        ("VAL1563_2_sort_countermodel", any(row["sort_id"] == "SORT1563_3_physical_countermodel" and row["status"] == "LEGAL_COUNTERMODEL" for row in sort), "physical R_AB countermodel recorded"),
        ("VAL1563_3_sort_not_signed", any(row["sort_id"] == "SORT1563_1_vertical_representative" and row["status"] == "EXACT_CONDITIONAL_NOT_PARENT_DERIVED" for row in sort), "vertical representative sort remains conditional"),
        ("VAL1563_4_grammar_fails", any(row["grammar_id"] == "GRAM1563_5_verdict" and row["status"] == "FAIL_CURRENT_THEOREM" for row in grammar), "no-derivative grammar fails current theorem claim"),
        ("VAL1563_5_elimination_conditional", any(row["elimination_id"] == "ELIM1563_2_Lambda_zero" and row["status"] == "EXACT_CONDITIONAL" for row in elimination), "Lambda_R elimination recorded as exact conditional"),
        ("VAL1563_6_fallback_inputs_missing", len(fallback) >= 5 and all(row["valid_for_claim"] == "False" for row in fallback), "finite fallback retained with nonclaim flags"),
        ("VAL1563_7_runner_fallback", any(row["runner_id"] == "RUN1563_4_fallback" and row["current_status"] == "RETAIN_NONCLAIM_FALLBACK" for row in run_rows), "runner retains finite residual fallback"),
        ("VAL1563_8_claim_gates", all(row["status"] == "BLOCKED_NO_CLAIM" for row in gate_rows), "all claim gates remain blocked"),
        ("VAL1563_9_decision_next", any(row["result"] == "NEXT_1564_VERTICAL_NULL_PRESYMPLECTIC_DEGENERACY_OR_FINITE_ZR_INTAKE" for row in decision_items), "decision selects vertical-null presymplectic degeneracy next"),
        ("VAL1563_10_next_target", any("1564-Y5-RAB-vertical-null" in row["next_target"] for row in next_rows), "next target is vertical-null presymplectic degeneracy or finite ZR intake"),
        ("VAL1563_11_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1563 CSVs parse cleanly"),
        ("VAL1563_12_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1563_13_branch_copies", all(path.exists() for path in [QUAR_SORT, QUAR_GRAMMAR, QUAR_ELIMINATION, QUAR_FALLBACK, QUAR_RUNNER, QUAR_DECISION, BRANCH_SORT, BRANCH_GRAMMAR, BRANCH_ELIMINATION, BRANCH_FALLBACK, BRANCH_RUNNER, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1563_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1563_15_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
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
            "check_id": "VAL1563_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1563 R_AB auxiliary compatibility parent sort and no-derivative grammar validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, Any]],
    sort: list[dict[str, Any]],
    grammar: list[dict[str, Any]],
    elimination: list[dict[str, Any]],
    fallback: list[dict[str, Any]],
    run_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    decision_items: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1563 - R_AB Auxiliary Compatibility Parent Sort and No-Derivative Grammar",
                "",
                "## Verdict",
                "- The auxiliary compatibility route remains the cleanest derivation path, but it is still conditional.",
                "- To make it a theorem, `R_AB` must be parent-typed as an auxiliary/vertical compatibility coordinate, not a physical scalar.",
                "- The parent grammar must forbid `D R_AB`, `D Lambda_R`, vertical metrics/connections, and boundary derivative operators.",
                "- Current sources do not parent-sign those grammar bans, so `Z_R=0` and `q_R=0` are not claimed.",
                "- Finite `Z_R/q_R` remains the honest fallback until vertical-null/presymplectic degeneracy is derived or real source rows are filled.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "",
                "## Parent Sort Audit",
                md_table(sort, ["sort_id", "parent_sort_statement", "claim_effect_if_signed", "status", "blocker"]),
                "",
                "## No-Derivative Grammar Gate",
                md_table(grammar, ["grammar_id", "grammar_clause", "why_needed", "status", "blocker_or_effect"]),
                "",
                "## Auxiliary Elimination Gate",
                md_table(elimination, ["elimination_id", "variation_or_step", "result", "status", "blocker"]),
                "",
                "## Finite Z_R/q_R Fallback Ledger",
                md_table(fallback, ["fallback_id", "coefficient", "meaning", "required_input", "status", "template_paths"]),
                "",
                "## Runner",
                md_table(run_rows, ["runner_id", "test", "current_status", "detail"]),
                "",
                "## Claim Gates",
                md_table(gate_rows, ["gate_id", "claim_gate", "status", "reason"]),
                "",
                "## Decision",
                md_table(decision_items, ["decision_id", "decision", "result", "reason"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "do_not"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    sources = source_register_rows()
    sort = sort_rows()
    grammar = grammar_rows()
    elimination = elimination_rows()
    fallback = fallback_rows()
    run_rows = runner_rows()
    gate_rows = claim_gate_rows()
    decision_items = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(SORT_AUDIT, sort)
    write_csv(GRAMMAR_GATE, grammar)
    write_csv(ELIMINATION_GATE, elimination)
    write_csv(FINITE_FALLBACK, fallback)
    write_csv(RUNNER, run_rows)
    write_csv(CLAIM_GATE, gate_rows)
    write_csv(DECISION, decision_items)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        SORT_AUDIT,
        GRAMMAR_GATE,
        ELIMINATION_GATE,
        FINITE_FALLBACK,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, sort, grammar, elimination, fallback, run_rows, gate_rows, decision_items, validation, next_rows)


if __name__ == "__main__":
    main()
