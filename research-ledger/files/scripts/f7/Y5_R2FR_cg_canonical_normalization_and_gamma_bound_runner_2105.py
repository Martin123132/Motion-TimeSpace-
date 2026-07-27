from __future__ import annotations

from pathlib import Path

from Y5_R2FR_Dq_vX_observed_metric_zero_or_finite_DObs_leak_row_2025 import (
    BRANCH_WEP,
    OUT,
    QUEUE,
    ROOT,
    SOURCE_WEIGHT_DOCS,
    base_row,
    count_formalization_modified,
    csv_rows_parse,
    md_table,
    read_text,
    remove_pycache,
    write_csv,
)


DOC = ROOT / "2105-Y5-R2FR-cg-canonical-normalization-and-gamma-bound-runner.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()

SRC_2104_DOC = ROOT / "2104-Y5-R2FR-cg-to-PPN-projection-matrix-or-measured-frame-degeneracy.md"
CSV_2104_PROJ = OUT / "P8_Y5_PARENT_QLOC_2104_CG_PPN_PROJECTION.csv"
CSV_2104_BOUNDS = OUT / "P8_Y5_PARENT_QLOC_2104_SCALAR_TENSOR_BOUND_ROWS.csv"
CSV_2104_GUARDS = OUT / "P8_Y5_PARENT_QLOC_2104_GUARD_CLOSURE_ROWS.csv"
CSV_2104_DEC = OUT / "P8_Y5_PARENT_QLOC_2104_DECISION_LEDGER.csv"
CSV_2104_NEXT = OUT / "P8_Y5_PARENT_QLOC_2104_NEXT_TARGET.csv"
CSV_2104_VAL = OUT / "P8_Y5_BRR545_2104_VALIDATION.csv"

SRC_1847_DOC = ROOT / "1847-Y5-R2FR-parent-Xhat-owner-and-Hessian-ZX-MX2-range-or-alpha-source-row.md"
CSV_1847_HESSIAN = OUT / "P8_Y5_PARENT_QLOC_1847_PARENT_HESSIAN_AUDIT.csv"
SRC_1848_DOC = ROOT / "1848-Y5-R2FR-parent-metric-ZXfX2-beta-eigenvalue-or-source-zero-return.md"
CSV_1848_SOURCE_ZERO = OUT / "P8_Y5_PARENT_QLOC_1848_SOURCE_ZERO_RETURN.csv"
SRC_1854_DOC = ROOT / "1854-Y5-R2FR-parent-Hessian-input-extraction-for-ZX-MX2.md"
CSV_1853_GATE = OUT / "P8_Y5_PARENT_QLOC_1853_ZX_MX2_INPUT_GATE.csv"
CSV_1854_RESULT = OUT / "P8_Y5_PARENT_QLOC_1854_ZX_MX2_EXTRACTION_RESULT.csv"
CSV_2023_SCHEMA = OUT / "P8_Y5_PARENT_QLOC_2023_ZX_MX2_FIRST_ROW_SCHEMA.csv"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid", "claim_allowed", "selected"}


def formalization_has_2105_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2105-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2105*",
        "*Y5_R2FR_cg_canonical_normalization_and_gamma_bound_runner_2105*",
        "*AFRAME_CG_CANONICAL_2105*",
        "*JR2105_ZX_MX2*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs: list[tuple[str, Path, list[str], str]] = [
        (
            "SRC2105_00_2104_doc",
            SRC_2104_DOC,
            ["NEXT2104_0_2105", "CG_CANONICAL_NORMALIZATION_AND_RANGE_RESPONSE_NEXT", "VAL2104_OVERALL"],
            "2104 selects canonical normalization and range response as the next missing object.",
        ),
        (
            "SRC2105_01_2104_projection",
            CSV_2104_PROJ,
            ["PRJ2104_1_common_conformal_branch", "alpha_eff=N_X c_g", "PROJECTION_TEMPLATE_DERIVED_NOT_SCOREABLE"],
            "2104 projection table says raw c_g must become canonical alpha_eff.",
        ),
        (
            "SRC2105_02_2104_bounds",
            CSV_2104_BOUNDS,
            ["STB2104_1_alpha_eff_conservative", "alpha_eff^2 * Y_gamma <= 3.35e-05", "MISSING_CANONICAL_NORMALIZATION"],
            "2104 bound rows give the nonclaim Cassini alpha_eff diagnostic scale.",
        ),
        (
            "SRC2105_03_2104_guards",
            CSV_2104_GUARDS,
            ["GRD2104_0_canonical_norm", "GRD2104_1_range_profile", "MISSING_RANGE_RESPONSE"],
            "2104 guard rows identify N_X/Z_X and Y_gamma as blockers.",
        ),
        (
            "SRC2105_04_2104_decision",
            CSV_2104_DEC,
            ["DEC2104_2_best_next", "CG_CANONICAL_NORMALIZATION_AND_RANGE_RESPONSE_NEXT"],
            "2104 decision says to derive canonical normalization before scoring.",
        ),
        (
            "SRC2105_05_2104_next",
            CSV_2104_NEXT,
            ["NEXT2104_0_2105", "2105-Y5-R2FR-cg-canonical-normalization-and-gamma-bound-runner.md"],
            "2104 next-target row points exactly at this checkpoint.",
        ),
        (
            "SRC2105_06_2104_validation",
            CSV_2104_VAL,
            ["VAL2104_OVERALL", "PASS", "canonical normalization/range response next"],
            "2104 validation is clean and nonclaim.",
        ),
        (
            "SRC2105_07_1847_doc",
            SRC_1847_DOC,
            ["lambda_X=sqrt(Z_X/M_X^2)", "Z_X>0", "current MTS does not yet own"],
            "1847 derives the second-variation/range relation but does not own the inputs.",
        ),
        (
            "SRC2105_08_1847_hessian",
            CSV_1847_HESSIAN,
            ["PHA1847_1_ZX_positive", "PHA1847_2_MX2_positive", "PHA1847_8_verdict"],
            "1847 Hessian audit lists Z_X/M_X^2 ownership requirements.",
        ),
        (
            "SRC2105_09_1848_doc",
            SRC_1848_DOC,
            ["Z_X f_X^2", "NOT_PARENT_SIGNED", "finite range route"],
            "1848 tries the parent metric/eigenvalue route and demotes finite range.",
        ),
        (
            "SRC2105_10_1848_source_zero",
            CSV_1848_SOURCE_ZERO,
            ["SZR1848_0_route_trigger", "SZR1848_5_verdict", "SOURCE_ZERO_OR_BOUNDED_COUPLING_ROW"],
            "1848 returns from finite metric/eigenvalue to source-zero/bounded coupling rows.",
        ),
        (
            "SRC2105_11_1853_gate",
            CSV_1853_GATE,
            ["ZMG1853_1_ZX_positive", "MISSING_ZX", "ZMG1853_5_verdict"],
            "1853 canonical input gate records missing Z_X/M_X^2/range transfer.",
        ),
        (
            "SRC2105_12_1854_doc",
            SRC_1854_DOC,
            ["N_X=1/sqrt(Z_X)", "NO_CLAIM_GRADE_ZX_OR_MX2_FOUND", "Current verdict"],
            "1854 extraction finds formulae but no claim-grade Z_X or M_X^2.",
        ),
        (
            "SRC2105_13_1854_result",
            CSV_1854_RESULT,
            ["EXT1854_0_ZX", "MISSING_ZX", "EXT1854_3_NX"],
            "1854 result table explicitly leaves N_X relation-only and Z_X missing.",
        ),
        (
            "SRC2105_14_2023_schema",
            CSV_2023_SCHEMA,
            ["ZMR2023_3_ZX", "ZMR2023_4_MX2", "ZMR2023_10_acceptance"],
            "2023 first-row schema lists the source fields needed for future extraction.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, use in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            row(
                source_id=source_id,
                source_kind="2105_cg_canonical_normalization",
                source_path=str(path),
                path_exists=exists,
                needles="; ".join(needles),
                needle_found=exists and all(needle in text for needle in needles),
                use_in_2105=use,
                valid_for_claim=False,
            )
        )
    return rows


def normalization_contract_rows() -> list[dict[str, object]]:
    specs = [
        (
            "NC2105_0_raw_to_canonical",
            "alpha_eff = N_X c_g",
            "raw c_g is a derivative with respect to Xhat; alpha_eff is the canonical dimensionless scalar-tensor coupling entering PPN gamma",
            "N_X required",
            "RELATION_DERIVED_INPUT_MISSING",
        ),
        (
            "NC2105_1_NX_from_ZX",
            "N_X = 1/sqrt(Z_X)",
            "for dimensionless Xhat and the local quadratic block normalized as 1/2 Z_X (grad Xhat)^2; include M_Pl/unit factors if the parent convention differs",
            "Z_X with units and same Xhat branch required",
            "RELATION_ONLY",
        ),
        (
            "NC2105_2_range",
            "lambda_X = sqrt(Z_X/M_X^2)",
            "same-branch kinetic and mass Hessian coefficients determine scalar range and hence Y_gamma(lambda, profile)",
            "Z_X, M_X^2 and unit convention required",
            "RELATION_ONLY",
        ),
        (
            "NC2105_3_gamma_template",
            "gamma-1 = -2 alpha_eff^2 Y_gamma/(1+alpha_eff^2 Y_gamma)+tails",
            "long-range weak-coupling branch reduces to |gamma-1| ~= 2 alpha_eff^2 if Y_gamma=1 and tails vanish",
            "Y_gamma and tail vector required",
            "BOUND_TEMPLATE_READY_NONCLAIM",
        ),
        (
            "NC2105_4_cg_bound",
            "c_g <= alpha_eff/(N_X sqrt(Y_gamma))",
            "a raw c_g bound exists only after N_X and Y_gamma are known or bounded away from zero",
            "N_X and Y_gamma missing",
            "RAW_CG_BOUND_BLOCKED",
        ),
        (
            "NC2105_5_verdict",
            "canonical normalization gate",
            "the algebraic bridge is now exact enough for a runner, but no current source provides claim-grade Z_X, M_X^2 or Y_gamma",
            "source Z_X/M_X^2 or derive parent Hessian",
            "RUNNER_REFUSES_SCORE",
        ),
    ]
    return [
        row(
            contract_id=contract_id,
            formula=formula,
            meaning=meaning,
            required_input=required,
            status=status,
            score_ready=False,
            valid_for_claim=False,
        )
        for contract_id, formula, meaning, required, status in specs
    ]


def input_extraction_rows() -> list[dict[str, object]]:
    specs = [
        ("IN2105_0_ZX", "Z_X", "kinetic Hessian coefficient in same Xhat normalization as c_g", "MISSING_ZX", "1847/1854 formula rows only", "blocks N_X and alpha_eff"),
        ("IN2105_1_MX2", "M_X^2", "local mass/range Hessian coefficient", "MISSING_MX2", "1847 relation only; 1854 not extracted", "blocks lambda_X and Y_gamma"),
        ("IN2105_2_NX", "N_X", "canonical Jacobian converting c_g to alpha_eff", "RELATION_ONLY_NX_EQ_1_OVER_SQRT_ZX", "requires Z_X", "blocks raw c_g bound"),
        ("IN2105_3_lambda_X", "lambda_X", "range entering Cassini response and R10 split", "RELATION_ONLY_SQRT_ZX_OVER_MX2", "requires Z_X/M_X^2", "blocks Y_gamma and R10/PPN fork"),
        ("IN2105_4_Ygamma", "Y_gamma(lambda, profile)", "Cassini/Shapiro finite-range response factor", "MISSING_RANGE_RESPONSE", "requires lambda_X and geometry/profile convention", "blocks gamma runner score"),
        ("IN2105_5_tail_vector", "tail_abs", "absolute sum of b_dis/q_nonH/gauge/readout/boundary PPN tails", "MISSING_TAIL_ZERO_OR_BOUNDS", "requires guard closure rows", "blocks isolated c_g score"),
    ]
    return [
        row(
            input_id=input_id,
            quantity=quantity,
            definition=definition,
            current_value=value,
            evidence=evidence,
            blocks=blocks,
            score_ready=False,
            valid_for_claim=False,
        )
        for input_id, quantity, definition, value, evidence, blocks in specs
    ]


def gamma_runner_rows() -> list[dict[str, object]]:
    specs = [
        (
            "RUN2105_0_missing_ZX",
            "c_g_gamma_bound",
            "c_g=MISSING_PARENT_INPUT; Z_X=MISSING_ZX; Y_gamma=MISSING_RANGE_RESPONSE",
            "REJECTED",
            "cannot convert raw c_g to alpha_eff",
        ),
        (
            "RUN2105_1_relation_only_NX",
            "alpha_eff_bound",
            "N_X=1/sqrt(Z_X) relation exists but Z_X is missing",
            "REJECTED",
            "relation-only rows cannot be scored",
        ),
        (
            "RUN2105_2_missing_range",
            "finite_range_gamma",
            "lambda_X=sqrt(Z_X/M_X^2) relation exists but M_X^2/Y_gamma are missing",
            "REJECTED",
            "long-range Y_gamma=1 cannot be assumed",
        ),
        (
            "RUN2105_3_missing_tails",
            "isolated_cg_gamma",
            "b_dis/q_nonH/gauge/readout/tail vector not zero or bounded",
            "REJECTED",
            "no cancellation or tail omission allowed",
        ),
        (
            "RUN2105_VERDICT",
            "gamma_bound_runner",
            "all candidate score paths contain missing parent inputs",
            "REFUSES_SCORE",
            "strict runner is ready; physics inputs are not",
        ),
    ]
    return [
        row(
            run_id=run_id,
            attempted_score=attempted_score,
            input_state=input_state,
            runner_result=result,
            reason=reason,
            accepted_for_scoring=False,
            claim_allowed=False,
            valid_for_claim=False,
        )
        for run_id, attempted_score, input_state, result, reason in specs
    ]


def gate_rows() -> list[dict[str, object]]:
    specs = [
        ("GATE2105_0_contract", "canonical normalization contract is written", True, "alpha_eff=N_X c_g and lambda_X relations are explicit"),
        ("GATE2105_1_ZX", "Z_X source exists", False, "Z_X remains MISSING_ZX / relation-only"),
        ("GATE2105_2_MX2", "M_X^2/range source exists", False, "M_X^2 and Y_gamma remain missing"),
        ("GATE2105_3_tail_zero", "PPN tail vector is zero/bounded", False, "b_dis/q_nonH/gauge/readout tails remain open"),
        ("GATE2105_4_runner", "gamma bound runner accepts a score", False, "strict runner rejects all placeholder paths"),
        ("GATE2105_5_local_GR", "local GR/Newton reduction follows", False, "canonical normalization is only one piece of the full GR route"),
    ]
    return [
        row(
            gate_id=gate_id,
            gate=gate,
            gate_pass=gate_pass,
            reason=reason,
            claim_allowed=False,
            valid_for_claim=False,
        )
        for gate_id, gate, gate_pass, reason in specs
    ]


def decision_rows() -> list[dict[str, object]]:
    specs = [
        (
            "DEC2105_0_contract_result",
            "CANONICAL_BRIDGE_DERIVED_BUT_INPUTS_MISSING",
            "The equations needed to score c_g against Cassini are now explicit, but Z_X/M_X^2/Y_gamma are not claim-grade.",
            "do not score raw c_g; use the strict runner as a blocker",
        ),
        (
            "DEC2105_1_best_next",
            "ZX_MX2_PARENT_HESSIAN_SOURCE_ROW_NEXT",
            "Every route now bottlenecks at the same parent Hessian ownership: Z_X, M_X^2, range response, and tail vector.",
            "attempt to extract/fill first claim-grade Z_X/M_X^2 row from parent action; otherwise keep c_g finite branch nonclaim",
        ),
    ]
    return [
        row(
            decision_id=decision_id,
            decision=decision,
            because=because,
            next_action=next_action,
            valid_for_claim=False,
        )
        for decision_id, decision, because, next_action in specs
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2105_0_2106",
            next_target="2106-Y5-R2FR-ZX-MX2-parent-Hessian-source-row-or-no-pole-return.md",
            script="scripts/Y5_R2FR_ZX_MX2_parent_Hessian_source_row_or_no_pole_return_2106.py",
            objective="Try to extract a claim-grade parent Hessian row for Z_X/M_X^2 in the same Xhat normalization as c_g; if it fails, return to no-pole/source-zero rather than scoring finite c_g.",
            forbidden_shortcuts="invented Z_X or M_X^2; assume Y_gamma=1; raw c_g Cassini score; local-GR claim; cancellation against PPN tails",
            valid_for_claim=False,
        )
    ]


def write_branch_copies(
    contract: list[dict[str, object]],
    inputs: list[dict[str, object]],
    runner: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2105_0_source_weight_docs",
            SOURCE_WEIGHT_DOCS / "AFRAME_CG_CANONICAL_2105_NONCLAIM.csv",
            contract + inputs + decisions,
        ),
        (
            "COPY2105_1_branch_locked_wep",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2105_CG_CANONICAL_STATUS_NONCLAIM.csv",
            inputs + runner,
        ),
        (
            "COPY2105_2_acquisition_queue",
            QUEUE / "JR2105_ZX_MX2_PARENT_HESSIAN_QUEUE.csv",
            inputs + next_target,
        ),
    ]
    rows: list[dict[str, object]] = []
    for copy_id, path, copy_rows in copies:
        write_csv(path, copy_rows)
        rows.append(
            row(
                copy_id=copy_id,
                destination=str(path),
                path_exists=path.exists(),
                row_count=len(copy_rows),
                parse_ok=csv_rows_parse(path),
                valid_for_claim=False,
            )
        )
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    contract: list[dict[str, object]],
    inputs: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(source.get("path_exists")) and truthy(source.get("needle_found")) for source in sources)
    contract_ok = any(row_.get("contract_id") == "NC2105_5_verdict" and row_.get("status") == "RUNNER_REFUSES_SCORE" for row_ in contract)
    inputs_ok = any(row_.get("input_id") == "IN2105_0_ZX" and row_.get("current_value") == "MISSING_ZX" for row_ in inputs) and any(row_.get("input_id") == "IN2105_4_Ygamma" for row_ in inputs)
    runner_ok = any(row_.get("run_id") == "RUN2105_VERDICT" and row_.get("runner_result") == "REFUSES_SCORE" for row_ in runner) and all(not truthy(row_.get("accepted_for_scoring")) for row_ in runner)
    gates_ok = all(not truthy(row_.get("claim_allowed")) for row_ in gates) and any(not truthy(row_.get("gate_pass")) for row_ in gates)
    decision_ok = any(row_.get("decision") == "ZX_MX2_PARENT_HESSIAN_SOURCE_ROW_NEXT" for row_ in decisions)
    next_ok = any(row_.get("route_id") == "NEXT2105_0_2106" and "2106-Y5-R2FR" in str(row_.get("next_target")) for row_ in next_target)
    copies_ok = len(copies) == 3 and all(truthy(row_.get("path_exists")) and truthy(row_.get("parse_ok")) for row_ in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claims = all(
        not truthy(row_.get("valid_for_claim")) and not truthy(row_.get("claim_allowed")) and not truthy(row_.get("score_ready")) and not truthy(row_.get("accepted_for_scoring"))
        for collection in (sources, contract, inputs, runner, gates, decisions, next_target, copies)
        for row_ in collection
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2105_artifacts()
    no_pycache = not (SCRIPT_PATH.parent / "__pycache__").exists()
    checks = [
        ("VAL2105_00_sources", sources_ok, "2104 plus Hessian/Z_X source files exist with required needles"),
        ("VAL2105_01_contract", contract_ok, "canonical normalization contract is written and refuses score"),
        ("VAL2105_02_inputs", inputs_ok, "Z_X/M_X^2/Y_gamma missing inputs are explicit"),
        ("VAL2105_03_runner", runner_ok, "gamma runner rejects all placeholder paths"),
        ("VAL2105_04_claim_gates", gates_ok, "claim gates block raw c_g score and local-GR promotion"),
        ("VAL2105_05_decision", decision_ok, "decision selects Z_X/M_X^2 parent Hessian source row next"),
        ("VAL2105_06_next", next_ok, "next target is 2106 Z_X/M_X^2 parent Hessian source row"),
        ("VAL2105_07_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2105_08_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2105_09_no_claim_flags", no_claims, "no generated row allows a claim or score"),
        ("VAL2105_10_formalization_clean", formalization_clean, "formalization-workbench untouched by 2105"),
        ("VAL2105_11_no_pycache", no_pycache, "scripts __pycache__ removed"),
    ]
    overall = all(ok for _, ok, _ in checks)
    checks.append(
        (
            "VAL2105_OVERALL",
            overall,
            "2105 builds the c_g canonical-normalization runner, refuses placeholder scoring, and selects Z_X/M_X^2 parent Hessian next",
        )
    )
    return [
        row(
            check_id=check_id,
            status="PASS" if ok else "FAIL",
            detail=detail,
            claim_allowed=False,
            valid_for_claim=False,
        )
        for check_id, ok, detail in checks
    ]


def write_doc(
    sources: list[dict[str, object]],
    contract: list[dict[str, object]],
    inputs: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2105 - Y5/R2FR c_g Canonical Normalization And Gamma Bound Runner",
        "",
        "## Current Verdict",
        "",
        "2105 turns the `c_g -> Cassini/PPN` route into a strict runner. The mathematical bridge is clear: `alpha_eff=N_X c_g`, with `N_X=1/sqrt(Z_X)` in the simple dimensionless-Xhat normalization, and `lambda_X=sqrt(Z_X/M_X^2)` for the range response.",
        "",
        "The runner correctly refuses to score because current MTS still has no claim-grade `Z_X`, `M_X^2`, `Y_gamma(lambda, profile)`, or zero/bound certificate for the PPN tail vector. This is not bad news; it means the coupling route is no longer vague. The next bottleneck is the parent Hessian source row.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_path", "path_exists", "needle_found", "use_in_2105", "valid_for_claim"]),
        "## Normalization Contract",
        md_table(contract, ["contract_id", "formula", "status", "meaning", "required_input", "score_ready", "valid_for_claim"]),
        "## Input Extraction Rows",
        md_table(inputs, ["input_id", "quantity", "current_value", "definition", "evidence", "blocks", "score_ready", "valid_for_claim"]),
        "## Gamma Runner",
        md_table(runner, ["run_id", "attempted_score", "input_state", "runner_result", "reason", "accepted_for_scoring", "claim_allowed", "valid_for_claim"]),
        "## Claim Gates",
        md_table(gates, ["gate_id", "gate", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
        "## Decision Ledger",
        md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
        "## Next Target",
        md_table(next_target, ["route_id", "next_target", "script", "objective", "forbidden_shortcuts", "valid_for_claim"]),
        "## Branch Copies",
        md_table(copies, ["copy_id", "destination", "path_exists", "row_count", "parse_ok", "valid_for_claim"]),
        "## Validation",
        md_table(validation, ["check_id", "status", "detail", "claim_allowed", "valid_for_claim"]),
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    contract = normalization_contract_rows()
    inputs = input_extraction_rows()
    runner = gamma_runner_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2105_SOURCE_REGISTER.csv",
        "contract": OUT / "P8_Y5_PARENT_QLOC_2105_NORMALIZATION_CONTRACT.csv",
        "inputs": OUT / "P8_Y5_PARENT_QLOC_2105_INPUT_EXTRACTION_ROWS.csv",
        "runner": OUT / "P8_Y5_PARENT_QLOC_2105_GAMMA_RUNNER.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2105_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2105_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2105_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2105_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2105_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["contract"], contract)
    write_csv(paths["inputs"], inputs)
    write_csv(paths["runner"], runner)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_target)
    copies = write_branch_copies(contract, inputs, runner, decisions, next_target)
    write_csv(paths["branch"], copies)
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(r["destination"])) for r in copies]
    remove_pycache()
    validation = validation_rows(sources, contract, inputs, runner, gates, decisions, next_target, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, contract, inputs, runner, gates, decisions, next_target, copies, validation)
    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
