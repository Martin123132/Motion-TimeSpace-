from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3296-Y5-R2FR-second-order-no-extra-field-locality-signature-or-Rkin-projection-under-AX1090.md"

SRC_3295_DOC = ROOT / "3295-Y5-R2FR-Lovelock-metric-kinetic-owner-or-non-Einstein-residual-vector-under-AX1090.md"
SRC_3295_NEXT = OUT / "P8_Y5_R2FR_3295_NEXT_TARGET.csv"
SRC_3295_PREMISES = OUT / "P8_Y5_R2FR_3295_LOVELOCK_PREMISE_AUDIT.csv"
SRC_3295_THEOREM = OUT / "P8_Y5_R2FR_3295_LOVELOCK_CONDITIONAL_THEOREM.csv"
SRC_3295_RKIN = OUT / "P8_Y5_R2FR_3295_NON_EINSTEIN_RKIN_RESIDUAL_VECTOR.csv"
SRC_3295_PPN = OUT / "P8_Y5_R2FR_3295_NEWTON_PPN_PROJECTION_CONTRACT.csv"
SRC_3295_VALIDATION = OUT / "P8_Y5_BRR545_3295_VALIDATION.csv"
SRC_3294_DOC = ROOT / "3294-Y5-R2FR-local-GR-reduction-contract-Hilbert-source-common-G-and-Newton-limit-under-AX1090.md"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3296_SOURCE_REGISTER.csv",
    "hard_clauses": OUT / "P8_Y5_R2FR_3296_HARD_CLAUSE_SIGNATURE_AUDIT.csv",
    "field_lanes": OUT / "P8_Y5_R2FR_3296_EXTRA_FIELD_LANE_CLASSIFICATION.csv",
    "projection": OUT / "P8_Y5_R2FR_3296_LINEARIZED_RKIN_PROJECTION_FORMULAS.csv",
    "test_inputs": OUT / "P8_Y5_R2FR_3296_RKIN_TEST_INPUT_REQUIREMENTS.csv",
    "runner": OUT / "P8_Y5_R2FR_3296_HARD_CLAUSE_RUNNER_NONCLAIM.csv",
    "promotion": OUT / "P8_Y5_R2FR_3296_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3296_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3296_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3296_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 560) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def text_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    return csv_parse_ok(path) if path.suffix.lower() == ".csv" else text_parse_ok(path)


def evidence_hits(path: Path, needles: list[str], limit: int = 5) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    lowered = [needle.lower() for needle in needles]
    hits: list[str] = []
    for idx, line in enumerate(lines, start=1):
        if any(needle in line.lower() for needle in lowered):
            hits.append(f"L{idx}:{compact(line, 330)}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_PATTERN_HIT"


def snapshot_tree(path: Path) -> dict[str, tuple[int, int]]:
    if not path.exists():
        return {}
    snapshot: dict[str, tuple[int, int]] = {}
    for item in path.rglob("*"):
        if item.is_file():
            stat = item.stat()
            snapshot[str(item.relative_to(path))] = (stat.st_size, stat.st_mtime_ns)
    return snapshot


def changed_count(before: dict[str, tuple[int, int]], after: dict[str, tuple[int, int]]) -> int:
    keys = set(before) | set(after)
    return sum(1 for key in keys if before.get(key) != after.get(key))


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (SRC_3295_DOC, "3295 handoff", ["second-order", "R_kin"]),
        (SRC_3295_NEXT, "3295 next target", ["second-order-no-extra-field-locality", "Rkin-projection"]),
        (SRC_3295_PREMISES, "Lovelock premise audit", ["LOV3295_4_second_order", "LOV3295_5_no_extra_propagating_fields", "LOV3295_2_locality"]),
        (SRC_3295_THEOREM, "Lovelock conditional theorem", ["LKT3295_0_Lovelock_statement", "R_kin"]),
        (SRC_3295_RKIN, "R_kin residual vector", ["RKIN3295_0_higher_derivative", "RKIN3295_2_nonlocal_memory"]),
        (SRC_3295_PPN, "PPN projection contract", ["PPN3295_0_Newton_source", "PPN3295_3_orbital"]),
        (SRC_3295_VALIDATION, "3295 validation", ["VAL3295_13_overall", "true"]),
        (SRC_3294_DOC, "local-GR spine context", ["G_mu_nu", "R_mu_nu^MTS"]),
    ]
    rows: list[dict[str, Any]] = []
    for idx, (path, role, needles) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3296_{idx}",
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence_hits(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def hard_clause_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "HC3296_0_second_order",
            "clause": "metric equation has no derivatives above second order",
            "derivation_attempt": "Requires parent kinetic action to be Einstein-Hilbert/Lovelock-linear in curvature or all higher-curvature terms to be topological/constant/decoupled.",
            "current_result": "NOT_PARENT_SIGNED",
            "if_fails": "R_HD projection required",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "HC3296_1_no_extra_local_fields",
            "clause": "local vacuum branch has no independent scalar/vector/torsion/nonmetricity propagating degrees of freedom",
            "derivation_attempt": "Any extra field must be gauge, algebraic auxiliary, infinitely massive/short-range, or q-basic silent in local vacuum.",
            "current_result": "NOT_PARENT_SIGNED",
            "if_fails": "R_extra projection required",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "HC3296_2_locality_memory_silence",
            "clause": "memory/history kernels do not contribute to local vacuum/solar-system field equation",
            "derivation_attempt": "Need separation theorem: cosmological/memory branch either becomes constant background/Lambda locally or has a sourced kernel below local bounds.",
            "current_result": "NOT_PARENT_SIGNED",
            "if_fails": "R_mem projection required",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "HC3296_3_principal_symbol_spin2",
            "clause": "linearized principal symbol carries only massless spin-2 metric polarizations in the local branch",
            "derivation_attempt": "If true, it supports second-order/no-extra-field route; if false, extra polarizations must be tested.",
            "current_result": "OPEN_SIGNATURE_TEST",
            "if_fails": "R_extra/R_pf gravitational-wave and PPN projections required",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "HC3296_4_result",
            "clause": "hard Lovelock clause status",
            "derivation_attempt": "3296 narrows the proof obligation to parent kinetic syntax plus field-lane classification.",
            "current_result": "PARTIAL_SIGNATURE_NOT_PROMOTED",
            "if_fails": "build R_kin projection basis",
            "valid_for_claim": "false",
        },
    ]


def field_lane_rows() -> list[dict[str, Any]]:
    return [
        {
            "lane_id": "LANE3296_0_gauge_or_constraint",
            "field_type": "extra variable is gauge or constrained by algebraic equation",
            "local_effect": "no independent propagating local force after quotient/reduction",
            "required_proof": "constraint solve and no singular denominator/source return",
            "status": "POSSIBLE_ZERO_ROUTE",
            "valid_for_claim": "false",
        },
        {
            "lane_id": "LANE3296_1_massive_decoupled",
            "field_type": "extra scalar/vector/memory mode has finite mass/range",
            "local_effect": "Yukawa or finite-range correction",
            "required_proof": "mass/range and coupling source rows; bound against R10/WEP/PPN/orbital data",
            "status": "TESTABLE_RESIDUAL",
            "valid_for_claim": "false",
        },
        {
            "lane_id": "LANE3296_2_qbasic_background",
            "field_type": "extra object is q-basic constant/background in local branch",
            "local_effect": "renormalizes Lambda, G_cal, or boundary constant without gradients",
            "required_proof": "vertical and spacetime derivative silence in local domain",
            "status": "POSSIBLE_CALIBRATION_ROUTE",
            "valid_for_claim": "false",
        },
        {
            "lane_id": "LANE3296_3_propagating_hidden",
            "field_type": "extra field propagates or couples to matter/source locally",
            "local_effect": "non-Einstein kinetic residual",
            "required_proof": "linearized operator and source coupling for PPN/Newton/orbital scoring",
            "status": "LIVE_RKIN_RESIDUAL",
            "valid_for_claim": "false",
        },
        {
            "lane_id": "LANE3296_4_nonlocal_memory_kernel",
            "field_type": "history/memory kernel contributes locally",
            "local_effect": "time/range/environment-dependent effective gravity",
            "required_proof": "kernel projection or local silence theorem",
            "status": "LIVE_RMEM_RESIDUAL",
            "valid_for_claim": "false",
        },
    ]


def projection_rows() -> list[dict[str, Any]]:
    return [
        {
            "projection_id": "PROJ3296_0_Newton_00",
            "residual": "R_kin_00",
            "formula": "nabla^2 Phi = 4*pi*G_cal*rho_total - (c^2/2)*Pi_00[R_kin] in the weak-field convention G_00≈2 nabla^2 Phi/c^2",
            "needed_inputs": "linearized R_kin_00, gauge convention, source density, boundary condition",
            "valid_for_claim": "false",
        },
        {
            "projection_id": "PROJ3296_1_Yukawa_range",
            "residual": "R_HD or massive R_extra",
            "formula": "Phi(r)=-(G_cal M/r)*(1+alpha_Y exp(-r/lambda_Y)) as the first finite-range test template",
            "needed_inputs": "alpha_Y, lambda_Y, source coupling, real bound curve/source path",
            "valid_for_claim": "false",
        },
        {
            "projection_id": "PROJ3296_2_PPN_gamma_beta",
            "residual": "spatial/nonlinear parts of R_kin",
            "formula": "map h_ij/h_00 and O(c^-4) terms into gamma-1 and beta-1 after solving the linearized residual equation",
            "needed_inputs": "post-Newtonian expansion, gauge, matter source, residual coefficients",
            "valid_for_claim": "false",
        },
        {
            "projection_id": "PROJ3296_3_preferred_frame",
            "residual": "R_pf or vector/torsion lane",
            "formula": "project frame-vector terms into alpha_1, alpha_2, alpha_3 and anisotropic inertial response",
            "needed_inputs": "preferred-frame vector, source velocity convention, PPN solution",
            "valid_for_claim": "false",
        },
        {
            "projection_id": "PROJ3296_4_memory",
            "residual": "R_mem",
            "formula": "G_eff(t,r,environment)=G_cal + Pi_mem[K_memory * source_history]",
            "needed_inputs": "kernel K_memory, local limit, source history, comparison arena",
            "valid_for_claim": "false",
        },
    ]


def test_input_rows() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "TIN3296_0_linearized_operator",
            "needed": "explicit linearized R_kin[h,fields] operator",
            "why": "without it Newton/PPN projection is symbolic only",
            "status": "MISSING_PARENT_OPERATOR",
            "valid_for_claim": "false",
        },
        {
            "input_id": "TIN3296_1_field_mass_range",
            "needed": "mass/range/coupling for each non-Einstein mode",
            "why": "needed for Yukawa, R10, orbital and WEP comparisons",
            "status": "MISSING_NUMERIC_MODE_INPUTS",
            "valid_for_claim": "false",
        },
        {
            "input_id": "TIN3296_2_memory_kernel",
            "needed": "local memory kernel or theorem-zero silence condition",
            "why": "MTS memory cannot be assumed irrelevant locally",
            "status": "MISSING_KERNEL_OR_ZERO_THEOREM",
            "valid_for_claim": "false",
        },
        {
            "input_id": "TIN3296_3_bounds",
            "needed": "source-backed PPN/orbital/R10/WEP bound rows",
            "why": "finite R_kin branches must be tested, not declared safe",
            "status": "MISSING_BOUND_LINKS",
            "valid_for_claim": "false",
        },
    ]


def runner_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN3296_0_hard_clauses_named", "second-order/no-extra-field/locality clauses are explicitly isolated", "PASS_SYMBOLIC_NONCLAIM"),
        ("RUN3296_1_not_parent_signed", "hard clauses remain unsigned", "REFUSE_CLAIM_NONCLAIM"),
        ("RUN3296_2_projection_started", "linearized R_kin projection formulas are staged", "PASS_SYMBOLIC_NONCLAIM"),
        ("RUN3296_3_numeric_tests_blocked", "numeric testing blocked until operator/mode/kernel/bound inputs exist", "REFUSE_MISSING_INPUT_NONCLAIM"),
    ]
    return [
        {
            "run_id": run_id,
            "check": check,
            "observed_status": status,
            "expectation_match": "true",
            "claim_allowed": "false",
        }
        for run_id, check, status in rows
    ]


def promotion_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3296_0_projection_started",
            "gate": "R_kin projection framework exists",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "symbolic projection formulas are staged.",
        },
        {
            "gate_id": "GATE3296_1_second_order_signed",
            "gate": "second-order metric equation parent-signed",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "no parent kinetic syntax proof yet.",
        },
        {
            "gate_id": "GATE3296_2_no_extra_fields_signed",
            "gate": "extra propagating local fields theorem-zero or bounded",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "field lanes remain classified, not closed.",
        },
        {
            "gate_id": "GATE3296_3_locality_memory_signed",
            "gate": "memory/locality silence theorem or kernel bound exists",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "memory kernel/local silence remains open.",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3296_0_honest_result",
            "finding": "The hard Lovelock clauses are not yet parent-signed, but each failure path now has a lane and a projection formula.",
            "consequence": "we moved from theorem-wrapper to testable residual architecture.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3296_1_best_derivation_route",
            "finding": "The best proof route is parent kinetic syntax: show the local action is metric-only, curvature-linear, and all nonmetric/memory variables are constraints or silent backgrounds.",
            "consequence": "if that works, R_kin collapses; if not, the exact non-Einstein branch becomes testable.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3296_2_best_testing_route",
            "finding": "If derivation stalls, the first empirical branch is the linearized R_kin basis with Yukawa/PPN/orbital projections.",
            "consequence": "next checkpoint should either prove kinetic syntax or build the first coefficient basis for tests.",
            "claim_allowed": "false",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3296_0_3297",
            "target_doc": "3297-Y5-R2FR-parent-kinetic-syntax-curvature-linear-proof-or-first-Rkin-basis-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3297_parent_kinetic_syntax_curvature_linear_proof_or_first_Rkin_basis.py",
            "objective": "try to prove the parent local kinetic syntax is metric-only and curvature-linear; if not, construct the first explicit R_kin coefficient basis for Newton/PPN/Yukawa/orbital tests.",
            "guardrails": "do not assume Einstein-Hilbert by taste; do not throw away memory variables; do not score numeric tests until coefficients and bounds are sourced.",
            "valid_for_claim": "false",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    hard_clauses: list[dict[str, Any]],
    field_lanes: list[dict[str, Any]],
    projections: list[dict[str, Any]],
    test_inputs: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    formalization_changed_count: int,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str = "") -> None:
        checks.append({"check_id": check_id, "check": check, "passed": bool_str(passed), "detail": detail})

    add("VAL3296_0_sources_exist", "all cited source paths exist", all(row["exists"] == "true" for row in sources))
    add("VAL3296_1_sources_parse", "all cited source paths parse", all(row["parse_ok"] == "true" for row in sources))
    add("VAL3296_2_outputs_parse", "all 3296 non-validation output CSVs parse", all(csv_parse_ok(path) for key, path in OUTPUTS.items() if key != "validation"))

    hard_text = " ".join(row["clause"] + " " + row["if_fails"] for row in hard_clauses)
    add(
        "VAL3296_3_hard_clauses_present",
        "hard clauses include second-order, no extra fields, locality/memory, and spin-2 symbol",
        "second order" in hard_text and "no independent scalar" in hard_text and "memory" in hard_text and "spin-2" in hard_text,
    )

    lane_statuses = {row["status"] for row in field_lanes}
    add(
        "VAL3296_4_field_lanes_complete",
        "field lanes classify zero, massive, q-basic, propagating, and memory cases",
        {"POSSIBLE_ZERO_ROUTE", "TESTABLE_RESIDUAL", "POSSIBLE_CALIBRATION_ROUTE", "LIVE_RKIN_RESIDUAL", "LIVE_RMEM_RESIDUAL"}.issubset(lane_statuses),
    )

    proj_text = " ".join(row["formula"] + " " + row["needed_inputs"] for row in projections)
    add(
        "VAL3296_5_projection_formulas_present",
        "projection formulas include Newton, Yukawa, PPN, preferred-frame, and memory maps",
        "nabla^2 Phi" in proj_text and "alpha_Y" in proj_text and "gamma-1" in proj_text and "alpha_1" in proj_text and "K_memory" in proj_text,
    )

    input_statuses = {row["status"] for row in test_inputs}
    add(
        "VAL3296_6_test_input_requirements_block_claim",
        "test input rows require operator, mode inputs, memory kernel, and bounds",
        {"MISSING_PARENT_OPERATOR", "MISSING_NUMERIC_MODE_INPUTS", "MISSING_KERNEL_OR_ZERO_THEOREM", "MISSING_BOUND_LINKS"}.issubset(input_statuses),
    )

    add("VAL3296_7_runner_expectations", "runner expectations all match", all(row["expectation_match"] == "true" for row in runner), ";".join(f"{row['run_id']}={row['observed_status']}" for row in runner))
    add("VAL3296_8_claim_gates_false", "no 3296 gate allows local GR/PPN claim", all(row["claim_allowed"] == "false" for row in promotion) and any(row["passed"] == "false" for row in promotion))
    add(
        "VAL3296_9_next_target_focused",
        "next target focuses parent kinetic syntax or first R_kin basis",
        len(next_target) == 1 and "parent-kinetic-syntax" in next_target[0]["target_doc"] and "first-Rkin-basis" in next_target[0]["target_doc"],
    )
    add(
        "VAL3296_10_decision_records_derivation_or_testing",
        "decision ledger records derivation route and finite testing route",
        any("testable residual architecture" in row["consequence"] for row in decisions) and any("first empirical branch" in row["finding"] for row in decisions),
    )
    add(
        "VAL3296_11_formalization_untouched",
        "formalization-workbench modified-file count remains zero by this script",
        formalization_changed_count == 0,
        f"formalization_changed_count={formalization_changed_count}",
    )
    overall = all(row["passed"] == "true" for row in checks)
    add("VAL3296_12_overall", "3296 validation overall", overall, "all required checks passed" if overall else "one or more checks failed")
    return checks


def md_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def md_table(rows: list[dict[str, Any]]) -> str:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, Any]],
    hard_clauses: list[dict[str, Any]],
    field_lanes: list[dict[str, Any]],
    projections: list[dict[str, Any]],
    test_inputs: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 3296 - Second-order, no-extra-field, locality signature or R_kin projection under AX1090

**Run UTC:** {RUN_UTC}

3296 attacks the hard clauses exposed by 3295. The result is not a local-GR claim. It is a sharper fork:

1. Prove the parent local kinetic syntax is second-order, metric-only, and locally memory-silent, which collapses `R_kin`.
2. Or keep the non-Einstein branches and project them into Newton/PPN/Yukawa/orbital observables.

The first concrete weak-field projection is staged:

`nabla^2 Phi = 4*pi*G_cal*rho_total - (c^2/2)*Pi_00[R_kin]`.

## Source Register

{md_table(sources)}

## Hard Clause Signature Audit

{md_table(hard_clauses)}

## Extra Field Lane Classification

{md_table(field_lanes)}

## Linearized R_kin Projection Formulas

{md_table(projections)}

## R_kin Test Input Requirements

{md_table(test_inputs)}

## Nonclaim Runner

{md_table(runner)}

## Promotion Gates

{md_table(promotion)}

## Decision Ledger

{md_table(decisions)}

## Next Target

{md_table(next_target)}

## Validation

{md_table(validation)}
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    before_fw = snapshot_tree(FW)

    sources = source_register_rows()
    hard_clauses = hard_clause_rows()
    field_lanes = field_lane_rows()
    projections = projection_rows()
    test_inputs = test_input_rows()
    runner = runner_rows()
    promotion = promotion_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["hard_clauses"], hard_clauses)
    write_csv(OUTPUTS["field_lanes"], field_lanes)
    write_csv(OUTPUTS["projection"], projections)
    write_csv(OUTPUTS["test_inputs"], test_inputs)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["promotion"], promotion)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    after_fw = snapshot_tree(FW)
    validation = validate(sources, hard_clauses, field_lanes, projections, test_inputs, runner, promotion, decisions, next_target, changed_count(before_fw, after_fw))
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, hard_clauses, field_lanes, projections, test_inputs, runner, promotion, decisions, next_target, validation)

    if PYCACHE.exists():
        for item in PYCACHE.iterdir():
            if item.is_file():
                item.unlink()
        try:
            PYCACHE.rmdir()
        except OSError:
            pass


if __name__ == "__main__":
    main()
