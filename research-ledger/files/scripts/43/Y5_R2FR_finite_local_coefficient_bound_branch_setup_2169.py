from __future__ import annotations

import json
import subprocess
import sys
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


DOC = ROOT / "2169-Y5-R2FR-finite-local-coefficient-bound-branch-setup.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUNNER = ROOT / "scripts" / "R10_alpha_lambda_bound_prediction_runner.py"
R10_BOUND = ROOT / "source-intake" / "local_bounds" / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"
DRYRUN_DIR = ROOT / "runs" / "2169-R10-template-dryrun" / "results"

DOCS = {
    "2168": ROOT / "2168-Y5-R2FR-object-language-radial-cell-constraint-or-finite-ZRJR-intake.md",
    "2168_validation": OUT / "P8_Y5_BRR545_2168_VALIDATION.csv",
    "2168_next": OUT / "P8_Y5_PARENT_QLOC_2168_NEXT_TARGET.csv",
    "1869": ROOT / "1869-Y5-R2FR-finite-local-coefficient-bound-branch-setup.md",
    "1869_validation": OUT / "P8_Y5_BRR545_1869_VALIDATION.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2169_SOURCE_REGISTER.csv",
    "components": OUT / "P8_Y5_PARENT_QLOC_2169_FINITE_LOCAL_COMPONENT_SCHEMA.csv",
    "arena_map": OUT / "P8_Y5_PARENT_QLOC_2169_ARENA_PROJECTION_MAP.csv",
    "r10_template": OUT / "P8_Y5_PARENT_QLOC_2169_R10_MTS_ALPHA_TEMPLATE_NONCLAIM.csv",
    "runner_command": OUT / "P8_Y5_PARENT_QLOC_2169_R10_DRYRUN_COMMAND.csv",
    "dryrun_status": OUT / "P8_Y5_PARENT_QLOC_2169_R10_DRYRUN_STATUS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2169_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2169_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2169_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2169_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2169_VALIDATION.csv",
}

BRANCH_COPIES = {
    "source_weight": SOURCE_WEIGHT_DOCS / "AFRAME_FINITE_LOCAL_COEFFICIENTS_2169_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2169_FINITE_LOCAL_BRANCH_NONCLAIM.csv",
    "queue": QUEUE / "JR2169_QR_ZR_MR2_FIRST_FILL_QUEUE.csv",
}


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid"}


def has_any(text: str, alternatives: list[str]) -> bool:
    return any(item in text for item in alternatives)


def find_line(path: Path, alternatives: list[str]) -> tuple[int, str]:
    text = read_text(path) if path.exists() else ""
    for line_number, line in enumerate(text.splitlines(), start=1):
        if has_any(line, alternatives):
            return line_number, line.strip()
    return 0, "MISSING_NEEDLE"


def formalization_has_2169_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2169-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2169*",
        "*P8_Y5_BRR545_2169*",
        "*Y5_R2FR_finite_local_coefficient_bound_branch_setup_2169*",
        "*AFRAME_FINITE_LOCAL_COEFFICIENTS_2169*",
        "*JR2169*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC2169_00_2168_handoff", DOCS["2168"], [["NEXT2168_0_2169"], ["CBB2168_0_ZR"], ["VAL2168_OVERALL"]], "2168 selects finite local coefficient-bound branch setup."),
        ("SRC2169_01_2168_validation", DOCS["2168_validation"], [["VAL2168_OVERALL"], ["PASS"]], "2168 validation passed as nonclaim."),
        ("SRC2169_02_2168_next_csv", DOCS["2168_next"], [["NEXT2168_0_2169"], ["Z_R"], ["R10"]], "machine-readable 2169 handoff."),
        ("SRC2169_03_1869_precedent", DOCS["1869"], [["FLC1869_0_qRhat"], ["R10DRY1869_0_template_runner"], ["VAL1869_OVERALL"]], "precedent finite coefficient schema and runner dryrun."),
        ("SRC2169_04_1869_validation", DOCS["1869_validation"], [["VAL1869_OVERALL"], ["PASS"]], "1869 validation passed as nonclaim."),
        ("SRC2169_05_R10_runner", RUNNER, [["MTS_REQUIRED_COLUMNS"], ["R10_pass_for_claim"]], "existing R10 alpha/lambda runner."),
        ("SRC2169_06_R10_bound_placeholder", R10_BOUND, [["valid_for_claim"], ["alpha_bound"]], "live bound file remains placeholder/QA-gated unless valid rows exist."),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle_groups, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles_found = exists and all(has_any(text, group) for group in needle_groups)
        rows.append(row(source_id=source_id, source_path=str(path), path_exists=exists, needles_found=needles_found, expected_needles="; ".join(" OR ".join(group) for group in needle_groups), role=role))
    return rows


def component_rows() -> list[dict[str, object]]:
    data = [
        ("FLC2169_0_qRhat", "q_R_hat_or_Q_R", "local reciprocal hair amplitude", "PPN;orbital;local_GR", "MISSING_QR_VALUE_OR_ZERO_THEOREM", "parent no-charge theorem or numeric Q_R/q_R_hat with source denominator"),
        ("FLC2169_1_ZR", "Z_R", "reciprocal gradient stiffness", "R10;PPN;clock;orbital;local_GR", "MISSING_PARENT_OPERATOR_ZR", "parent Hessian/operator extraction with action normalization"),
        ("FLC2169_2_MR2", "M_R^2", "mass gap/range owner", "R10;clock;orbital", "MISSING_PARENT_OPERATOR_MR2", "parent mass-gap extraction; lambda_R=sqrt(Z_R/M_R^2) only after same-normalization"),
        ("FLC2169_3_lambdaR", "lambda_R", "finite interaction range", "R10;clock;orbital", "MISSING_RANGE_RELATION", "derive from Z_R/M_R^2 or source independent parent range law"),
        ("FLC2169_4_beta_source", "beta_source_R", "source-leg reciprocal matter charge", "R10;WEP;clock", "MISSING_SOURCE_CHARGE_OR_ZERO_THEOREM", "source material charge or parent matter descent zero theorem"),
        ("FLC2169_5_beta_test", "beta_test_R", "test-leg reciprocal matter charge", "R10;WEP;clock", "MISSING_TEST_CHARGE_OR_ZERO_THEOREM", "test material/readout charge or parent matter descent zero theorem"),
        ("FLC2169_6_JR", "J_R", "bulk reciprocal source current", "PPN;orbital;local_GR", "MISSING_SOURCE_CURRENT", "source-current density with compact support/worldtube convention"),
        ("FLC2169_7_boundary", "B_R_or_Pi_Rn_or_epsilon_tail", "boundary/readout tail", "R10;PPN;clock;orbital;local_GR", "MISSING_BOUNDARY_TAIL_OR_ZERO_THEOREM", "absolute boundary tail or theorem-zero; no cancellation against bulk"),
        ("FLC2169_8_tau_R10", "tau_R10_or_K_R", "R10 alpha(lambda) projection", "R10", "MISSING_R10_PROJECTION_OR_ACCEPTED_CURVE", "R10 source/test support kernel plus accepted bound curve"),
        ("FLC2169_9_tau_PPN", "tau_PPN_or_C_QR", "PPN residual projection", "PPN;local_GR", "MISSING_PPN_PROJECTION", "q_R_hat/Q_R to gamma/beta/light-time mapping with same source frame"),
        ("FLC2169_10_tau_clock", "tau_clock", "clock/redshift projection", "clock;WEP", "MISSING_CLOCK_PROJECTION", "fractional-frequency/material sensitivity kernel"),
        ("FLC2169_11_tau_orbital", "tau_orbital", "orbital residual projection", "orbital;local_GR", "MISSING_ORBITAL_PROJECTION", "acceleration/precession/timing kernel in PPN-compatible frame"),
        ("FLC2169_12_SR_total", "S_R_total", "source side of D_R=partial_r C_R-S_R", "local_GR;PPN;orbital", "MISSING_SOURCE_MAP", "no-cancellation sum of q_loc, matter, boundary, readout, current and reciprocal slots"),
    ]
    return [row(component_id=component_id, symbol=symbol, role=role, arenas=arenas, status=status, required_input=required_input) for component_id, symbol, role, arenas, status, required_input in data]


def arena_rows() -> list[dict[str, object]]:
    data = [
        ("APM2169_0_R10", "R10_fifth_force", "alpha_R(lambda)=K_R^R10(lambda)*beta_source_R*beta_test_R+epsilon_tail_R", "lambda_R,Z_R,M_R^2,K_R^R10,beta_source_R,beta_test_R,epsilon_tail_R,accepted alpha_bound(lambda)", "BLOCKED_NONCLAIM"),
        ("APM2169_1_PPN", "PPN_gamma_beta_light_time", "gamma_minus_1=q_R_hat+delta_gauge+delta_source+delta_boundary+delta_readout+O(U_N)", "q_R_hat/Q_R,kappa_W,source denominator,gauge/readout tails,beta/conservation/common-matter gates", "BLOCKED_NONCLAIM"),
        ("APM2169_2_clock", "clock_redshift_constants", "delta_nu/nu=tau_clock*q_R_hat+clock_tail_R", "tau_clock,clock material sensitivities,source frame,constant-superselection or finite material coefficients", "BLOCKED_NONCLAIM"),
        ("APM2169_3_orbital", "orbital_precession_acceleration", "delta_orbit=tau_orbital*q_R_hat+orbital_tail_R", "tau_orbital,source denominator,acceleration/precession/timing kernel,boundary tail", "BLOCKED_NONCLAIM"),
        ("APM2169_4_local_GR", "local_GR_Newton_reduction", "local pass requires q_R_hat=Z_R=J_R=Q_R=boundary/readout/source tails=0 or finite residuals below local sensitivity", "typed grammar/no-charge theorem or complete finite residual bounds across R10/PPN/clock/orbital", "BLOCKED_NONCLAIM"),
    ]
    return [row(arena_id=arena_id, arena=arena, model_equation=model_equation, required_inputs=required_inputs, status=status) for arena_id, arena, model_equation, required_inputs, status in data]


def r10_template_rows() -> list[dict[str, object]]:
    return [
        {
            "model_id": "MTS_R2FR_2169_finite_RAB_template",
            "branch_id": base_row()["branch_id"],
            "curve_id": "R10_ALPHA_2169_TEMPLATE_NONCLAIM",
            "lambda_value": "MISSING_LAMBDA_R_FROM_ZR_MR2",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_KR_BETA_SOURCE_BETA_TEST_EPSILON_TAIL",
            "alpha_bound": "MISSING_JOINED_BOUND",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
            "force_law_form": "alpha_R(lambda)=K_R^R10(lambda)*beta_source_R*beta_test_R+epsilon_tail_R",
            "derivation_status": "TEMPLATE_INVALID_MISSING_PARENT_COEFFICIENTS",
            "formula_reference": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2169_ARENA_PROJECTION_MAP.csv",
            "source_file": "MISSING_SOURCE_FILE",
            "assumptions": "no single-coupling shortcut; no cancellation; beta_source and beta_test are separate legs",
            "valid_for_claim": "false",
            "notes": "schema-compatible placeholder for R10_alpha_lambda_bound_prediction_runner.py; expected to fail until parent coefficients and accepted bound curve exist",
        }
    ]


def run_r10_dryrun() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    command = [
        sys.executable,
        str(RUNNER),
        "--mts-curve",
        str(OUTPUTS["r10_template"]),
        "--bound-curve",
        str(R10_BOUND),
        "--output-dir",
        str(DRYRUN_DIR),
    ]
    completed = subprocess.run(command, check=False, capture_output=True, text=True)
    status_path = DRYRUN_DIR / "R10_runner_status.json"
    status: dict[str, object] = {}
    if status_path.exists():
        status = json.loads(status_path.read_text(encoding="utf-8"))
    command_rows = [
        row(
            dryrun_id="RCM2169_0_R10_template_dryrun",
            runner_path=str(RUNNER),
            command=" ".join(f'"{part}"' if " " in part else part for part in command),
            return_code=completed.returncode,
            stdout_tail=completed.stdout[-1000:],
            stderr_tail=completed.stderr[-1000:],
            claim_allowed=False,
        )
    ]
    status_rows = [
        row(
            dryrun_id="R10DRY2169_0_template_runner",
            return_code=completed.returncode,
            valid_mts_rows=status.get("valid_mts_rows", "MISSING_STATUS"),
            valid_bound_rows=status.get("valid_bound_rows", "MISSING_STATUS"),
            comparison_rows=status.get("comparison_rows", "MISSING_STATUS"),
            R10_pass_for_claim=status.get("R10_pass_for_claim", False),
            claim_allowed=status.get("claim_allowed", False),
            valid_for_claim=False,
        )
    ]
    return command_rows, status_rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("CG2169_0_component_values", "finite local coefficients are sourced", "BLOCKED", "MISSING_NUMERIC_VALUES_SOURCE_PATHS_UNITS", "fill component rows with theorem-zero or numeric source-backed values"),
        ("CG2169_1_R10", "R10 alpha(lambda) branch passes", "BLOCKED", "R10_TEMPLATE_INVALID_AND_BOUND_CURVE_PLACEHOLDER", "valid MTS alpha rows plus accepted alpha_bound(lambda) curve and runner pass"),
        ("CG2169_2_PPN_clock_orbital", "PPN/clock/orbital finite residuals are below bounds", "BLOCKED", "MISSING_ARENA_PROJECTIONS_AND_NUMERIC_COMPONENTS", "source tau_PPN, tau_clock, tau_orbital and run no-cancellation residual vector"),
        ("CG2169_3_local_GR", "finite branch establishes local GR/Newton reduction", "BLOCKED", "FINITE_BOUND_SETUP_NOT_A_DERIVATION", "theorem-zero branch or complete cross-arena finite-bound demonstration required"),
    ]
    return [row(gate_id=gate_id, claim=claim, status=status, blocked_by=blocked_by, next_action=next_action) for gate_id, claim, status, blocked_by, next_action in data]


def decision_rows() -> list[dict[str, object]]:
    data = [
        ("DEC2169_0_schema", "FINITE_LOCAL_COEFFICIENT_SCHEMA_READY_NONCLAIM", "all local reciprocal residual quantities needed for R10/PPN/clock/orbital/local-GR checks have source-or-missing rows", "use as first-fill queue, not evidence"),
        ("DEC2169_1_R10_dryrun", "R10_TEMPLATE_DRYRUN_BLOCKS_AS_EXPECTED", "existing R10 runner returns no claim pass on placeholder MTS and live placeholder bound files", "pipeline failure mode is executable and safe"),
        ("DEC2169_2_next", "FIRST_FILL_TARGET_QR_ZR_MR2_SOURCE_CHAIN", "R10 and PPN both need range/amplitude/charge normalization before arena scoring", "attack Q_R/Z_R/M_R^2 and source denominator first, then tau projections"),
    ]
    return [row(decision_id=decision_id, decision=decision, because=because, next_action=next_action) for decision_id, decision, because, next_action in data]


def next_target_rows() -> list[dict[str, object]]:
    data = [
        ("NEXT2169_0_2170", "2170-Y5-R2FR-QR-ZR-MR2-source-chain-first-fill-or-no-charge-return.md", "scripts/Y5_R2FR_QR_ZR_MR2_source_chain_first_fill_or_no_charge_return_2170.py", "try to derive/source the minimal Q_R, Z_R, M_R^2, lambda_R and source-denominator chain needed by both R10 and PPN; if not, keep rows blocked", "selected", "first theorem-zero or source-backed numeric row for range/amplitude/charge normalization, or explicit blocker ledger proving no arena score is possible yet"),
        ("NEXT2169_1_parallel_R10_bound", "2170b-Y5-R2FR-accepted-R10-bound-curve-promotion-or-blocker.md", "scripts/Y5_R2FR_accepted_R10_bound_curve_promotion_or_blocker_2170b.py", "separately promote a real accepted R10 bound curve or keep the live bound file placeholder-blocked", "held", "claim-safe alpha_bound(lambda) curve or clear source/QA blocker"),
    ]
    return [row(route_id=route_id, next_target=next_target, script=script, objective=objective, selection_status=selection_status, success_condition=success_condition) for route_id, next_target, script, objective, selection_status, success_condition in data]


def write_branch_copies(components, arena, next_rows) -> list[dict[str, object]]:
    copies = [
        ("COPY2169_0_source_weight_docs", BRANCH_COPIES["source_weight"], components),
        ("COPY2169_1_branch_locked_wep", BRANCH_COPIES["branch_wep"], components + arena),
        ("COPY2169_2_acquisition_queue", BRANCH_COPIES["queue"], next_rows + components),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(sources, components, arena, template, command_rows, dryrun, gates, decisions, next_rows, copies, csv_paths):
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    components_ok = len(components) == 13 and any(item["component_id"] == "FLC2169_12_SR_total" for item in components)
    arena_ok = len(arena) == 5 and all(item["status"] == "BLOCKED_NONCLAIM" for item in arena)
    template_ok = bool(template) and template[0]["valid_for_claim"] == "false" and "MISSING" in json.dumps(template[0])
    dryrun_ok = bool(dryrun) and str(dryrun[0]["return_code"]) == "0" and str(dryrun[0]["R10_pass_for_claim"]).lower() == "false" and str(dryrun[0]["valid_mts_rows"]) == "0"
    gates_ok = all(item["status"] == "BLOCKED" and not truthy(item.get("claim_allowed", False)) for item in gates)
    decisions_ok = any(
        item["decision_id"] == "DEC2169_2_next"
        and "QR_ZR_MR2" in item["decision"]
        and "Q_R/Z_R/M_R^2" in item["next_action"]
        for item in decisions
    )
    next_ok = any(item["route_id"] == "NEXT2169_0_2170" and item["selection_status"] == "selected" for item in next_rows)
    copies_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False)) for group in (sources, components, arena, command_rows, dryrun, gates, decisions, next_rows, copies) for item in group)
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2169_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, components_ok, arena_ok, template_ok, dryrun_ok, gates_ok, decisions_ok, next_ok, copies_ok, csv_ok, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2169_00_sources", sources_ok, "2168/1869/R10 source paths and needles validate"),
        ("VAL2169_01_components", components_ok, "component schema covers Q_R/Z_R/M_R2/J_R/tau rows"),
        ("VAL2169_02_arena_map", arena_ok, "arena projection map covers R10/PPN/clock/orbital/local-GR"),
        ("VAL2169_03_R10_template", template_ok, "R10 alpha template has runner-required shape but remains invalid"),
        ("VAL2169_04_R10_dryrun_blocks", dryrun_ok, "existing R10 runner blocks placeholder template as expected"),
        ("VAL2169_05_claim_gates", gates_ok, "all finite branch claim gates remain blocked"),
        ("VAL2169_06_decision", decisions_ok, "decision ledger selects Q_R/Z_R/M_R2 chain next"),
        ("VAL2169_07_next", next_ok, "2170 next target selected"),
        ("VAL2169_08_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2169_09_csv_parse", csv_ok, "all generated 2169 CSVs parse cleanly"),
        ("VAL2169_10_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2169_11_formalization_clean", formalization_clean, "formalization-workbench untouched by 2169"),
        ("VAL2169_12_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2169_OVERALL", all_ok, "2169 builds finite local coefficient schema and fail-safe R10 template dryrun."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(sources, components, arena, template, command_rows, dryrun, gates, decisions, next_rows, copies, validation) -> None:
    line_2168, _ = find_line(DOCS["2168"], ["NEXT2168_0_2169"])
    line_1869, _ = find_line(DOCS["1869"], ["FLC1869_0_qRhat"])
    content = "\n\n".join(
        [
            "# 2169 - Y5/R2FR Finite Local Coefficient-Bound Branch Setup",
            "## Current Verdict",
            "2169 does **not** supply finite coefficient values, does **not** pass R10/PPN/clock/orbital tests, and does **not** claim local GR/Newton.",
            "It makes the finite branch runner-ready: `Q_R/q_R_hat`, `Z_R`, `M_R^2`, `lambda_R`, source/test charges, `J_R`, boundary tails and projection maps now have explicit source-or-missing rows.",
            "The R10 alpha template intentionally fails because parent coefficients and accepted bound-curve rows are still missing. That is the right fail-safe behavior.",
            f"This follows the 2168 handoff at line {line_2168} and imports the 1869 finite-branch precedent at line {line_1869}.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Finite Local Component Schema",
            md_table(components, ["component_id", "symbol", "role", "arenas", "status", "required_input", "valid_for_claim"]),
            "## Arena Projection Map",
            md_table(arena, ["arena_id", "arena", "model_equation", "required_inputs", "status", "valid_for_claim"]),
            "## R10 Alpha Template",
            md_table(template, ["model_id", "curve_id", "lambda_value", "alpha_predicted", "force_law_form", "derivation_status", "valid_for_claim"]),
            "## R10 Dryrun Command",
            md_table(command_rows, ["dryrun_id", "runner_path", "return_code", "claim_allowed", "valid_for_claim"]),
            "## R10 Dryrun Status",
            md_table(dryrun, ["dryrun_id", "return_code", "valid_mts_rows", "valid_bound_rows", "comparison_rows", "R10_pass_for_claim", "claim_allowed", "valid_for_claim"]),
            "## Claim Gates",
            md_table(gates, ["gate_id", "claim", "status", "blocked_by", "next_action", "claim_allowed", "valid_for_claim"]),
            "## Decision Ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "## Next Target",
            md_table(next_rows, ["route_id", "next_target", "script", "objective", "selection_status", "success_condition", "valid_for_claim"]),
            "## Branch Copies",
            md_table(copies, ["copy_id", "destination", "path_exists", "row_count", "parse_ok", "valid_for_claim"]),
            "## Validation",
            md_table(validation, ["check_id", "status", "detail", "claim_allowed", "valid_for_claim"]),
            "## Working Interpretation",
            "We have not won local GR by derivation, but the finite branch is now disciplined enough to test later. The first real fill target is the shared amplitude/range/source chain: `Q_R`, `Z_R`, `M_R^2`, `lambda_R`, and the source denominator. Without those, neither R10 nor PPN can honestly score the branch.",
        ]
    )
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    components = component_rows()
    arena = arena_rows()
    template = r10_template_rows()
    write_csv(OUTPUTS["r10_template"], template)
    command_rows, dryrun = run_r10_dryrun()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["components"], components)
    write_csv(OUTPUTS["arena_map"], arena)
    write_csv(OUTPUTS["runner_command"], command_rows)
    write_csv(OUTPUTS["dryrun_status"], dryrun)
    write_csv(OUTPUTS["claim_gate"], gates)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next_target"], next_rows)
    copies = write_branch_copies(components, arena, next_rows)
    write_csv(OUTPUTS["branch_copies"], copies)

    remove_pycache()
    csv_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    validation = validation_rows(sources, components, arena, template, command_rows, dryrun, gates, decisions, next_rows, copies, csv_paths)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, components, arena, template, command_rows, dryrun, gates, decisions, next_rows, copies, validation)
    remove_pycache()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"2169 validation {validation[-1]['status']}")


if __name__ == "__main__":
    main()
