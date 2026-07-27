from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
DOC_NAME = "922-Y5-R10-KBFH-parent-units-and-normalization-or-local-bound-smoke-runner.md"
STATUS = "Y5_R10_922_KBFH_unit_branches_audited_no_parent_convention_strict_local_bound_smoke_blocks_all_scores_nonclaim"
CLAIM_CEILING = "KBFH_units_audit_and_fail_closed_smoke_runner_only_no_R10_WEP_PPN_clock_orbital_or_local_GR_claim"
NEXT_TARGET = "923-Y5-R10-parent-selects-mass-gauge-normalization-or-run-first-real-FM-bound-row.md"
GENERATED = datetime.now(timezone.utc).isoformat()
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def md_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        cells = [str(row.get(field, "")).replace("|", "\\|").replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def b(value: bool) -> str:
    return "true" if value else "false"


def source_specs() -> list[dict[str, str]]:
    return [
        {
            "source_id": "921_doc",
            "path": "921-Y5-R10-FM-force-weak-field-map-and-KBFH-units-bound-runner.md",
            "role": "weak-field map and KBFH units blocker handoff",
            "needle": "weak-field/bounds interface",
        },
        {
            "source_id": "921_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_921_VALIDATION.csv",
            "role": "proves 921 was generated and nonclaim",
            "needle": "V921_11_validation_rows_ready",
        },
        {
            "source_id": "921_units",
            "path": "source-intake/mts_residuals/P8_Y5_R10_921_UNITS_CONVENTION_AUDIT.csv",
            "role": "unit blockers for KBFH/A_M/dPiMJ/lambda/projection coefficients",
            "needle": "MISSING_PARENT_UNITS",
        },
        {
            "source_id": "921_arena_map",
            "path": "source-intake/mts_residuals/P8_Y5_R10_921_LOCAL_BOUND_ARENA_MAP.csv",
            "role": "local-bound join rows for WEP, clocks, PPN, preferred-frame, Gdot, and R10",
            "needle": "BAM921_9_R10",
        },
        {
            "source_id": "921_smoke_rows",
            "path": "source-intake/mts_residuals/P8_Y5_R10_921_NONCLAIM_SMOKE_ROWS.csv",
            "role": "nonclaim smoke inputs that should block scoring",
            "needle": "blocked_missing_parent_units",
        },
        {
            "source_id": "916_BF_candidate",
            "path": "916-Y5-R10-parent-BF-mass-current-sector-or-Delta-HT-bound-input.md",
            "role": "BF mass-current candidate and k_M level blocker",
            "needle": "S_BF,M = k_M integral B_M wedge F_M",
        },
        {
            "source_id": "918_BF_source_coupling",
            "path": "918-Y5-R10-nonpropagating-mass-gauge-constraint-sector-or-DeltaHT-scorepack.md",
            "role": "candidate S_BF source coupling form",
            "needle": "S_BF = integral k_M B_M wedge dA_M + A_M wedge",
        },
        {
            "source_id": "local_bound_claims",
            "path": "source-intake/local_bounds/local_bound_claims.csv",
            "role": "external/local bound source intake",
            "needle": "R10_fifth_force",
        },
        {
            "source_id": "R10_curve",
            "path": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
            "role": "R10 alpha-lambda curve remains digitization-blocked",
            "needle": "MISSING_DIGITIZED_ALPHA_BOUND",
        },
        {
            "source_id": "local_runner_smoke_doc",
            "path": "427-local-bound-runner-v4-evaluate-smoke.md",
            "role": "prior local-bound evaluate smoke discipline",
            "needle": "claim_allowed_rows",
        },
    ]


def build_sources() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in source_specs():
        path = ROOT / spec["path"]
        exists = path.exists()
        needle_found = exists and spec["needle"] in read_text(path)
        rows.append(
            {
                **spec,
                "absolute_path": str(path),
                "exists": b(exists),
                "needle_found": b(needle_found),
                "valid_for_claim": "false",
                "generated_utc": GENERATED,
            }
        )
    return rows


def summary_rows() -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "current_result": "dimensional branches can be written, but no parent-selected convention fixes K_BF_H; strict smoke runner blocks every local-bound score",
            "practical_meaning": "the framework now has an executable gate that prevents fake R10/WEP/PPN passes from missing coupling data",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        }
    ]


def unit_branch_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": "KBU922_0_form_degree",
            "assumption": "4D source coupling has S_src = K_BF_H integral A_M wedge J_Pi with A_M a 1-form and J_Pi a 3-form",
            "dimension_condition": "[K_BF_H] [A_M] [J_Pi] [L]^4 = [action]",
            "what_it_fixes": "form degree only",
            "blocker": "does not determine [A_M], [J_Pi], or whether K_BF_H is dimensionless",
            "parent_selected": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "branch_id": "KBU922_1_connection_normalization",
            "assumption": "A_M is a dimensionless/topological connection and holonomies are dimensionless",
            "dimension_condition": "[K_BF_H J_Pi] supplies action density as a 3-form source charge",
            "what_it_fixes": "A_M_holonomy can be dimensionless",
            "blocker": "K_BF_H is then a source-charge normalization and still needs parent calibration to M_eff/G_ref",
            "parent_selected": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "branch_id": "KBU922_2_gauge_field_normalization",
            "assumption": "A_M has inverse-length units like an ordinary gauge potential in natural units",
            "dimension_condition": "[K_BF_H J_Pi] carries remaining length/action units",
            "what_it_fixes": "can resemble a force-potential coupling",
            "blocker": "requires a kinetic/range convention that the nonpropagating branch explicitly avoided",
            "parent_selected": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "branch_id": "KBU922_3_BF_level",
            "assumption": "S_BF = k_M integral B_M wedge dA_M fixes the relative normalization of B_M and A_M",
            "dimension_condition": "[k_M] [B_M] [dA_M] [L]^4 = [action]",
            "what_it_fixes": "relative BF-sector dimensions",
            "blocker": "does not fix coupling to Hilbert source unless J_Pi equality and k_M calibration are parent-signed",
            "parent_selected": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "branch_id": "KBU922_4_measured_GM_calibration",
            "assumption": "closed mass charge is calibrated by integral_S Q_M = M_eff and Poisson/Gauss normalization",
            "dimension_condition": "K_BF_H must reduce to fixed universal G_ref/M_eff normalization in weak field",
            "what_it_fixes": "would connect coupling units to measured Newtonian source strength",
            "blocker": "this is exactly the unproved source-measure glue; cannot be used to choose units post hoc",
            "parent_selected": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def load_arena_rows() -> list[dict[str, str]]:
    return read_csv(OUT / "P8_Y5_R10_921_LOCAL_BOUND_ARENA_MAP.csv")


def smoke_inputs() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for arena in load_arena_rows():
        rows.append(
            {
                "smoke_id": f"SMK922_{arena['map_id'].split('_')[-1]}",
                "local_bound_row": arena["local_bound_row"],
                "observable": arena["observable"],
                "upper_bound": arena["upper_bound"],
                "FM_residual": arena["FM_residual"],
                "predicted_value": "MISSING_NUMERIC_RESIDUAL",
                "units": arena["units"],
                "required_inputs": "K_BF_H;A_M_norm;dPiMJ_leak;projection_coefficient;source_path",
                "expected_status": "blocked",
                "valid_for_claim": "false",
                "generated_utc": GENERATED,
            }
        )
    return rows


def strict_eval_status(row: dict[str, object]) -> tuple[str, str]:
    missing_tokens = ["MISSING", "symbolic", "alpha(lambda)", "range-dependent"]
    joined = " ".join(str(value) for value in row.values())
    if any(token in joined for token in missing_tokens):
        return "blocked", "missing_numeric_or_symbolic_bound_input"
    if not str(row.get("valid_for_claim", "")).lower() == "true":
        return "blocked", "valid_for_claim_false"
    return "candidate", "all_required_fields_present"


def smoke_eval_rows(inputs: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in inputs:
        status, reason = strict_eval_status(row)
        rows.append(
            {
                "eval_id": row["smoke_id"].replace("SMK", "EVAL"),
                "local_bound_row": row["local_bound_row"],
                "observable": row["observable"],
                "predicted_value": row["predicted_value"],
                "upper_bound": row["upper_bound"],
                "runner_status": status,
                "block_reason": reason,
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": GENERATED,
            }
        )
    return rows


def blocker_rows() -> list[dict[str, object]]:
    return [
        {
            "blocker_id": "BLK922_0_parent_convention",
            "missing_input": "parent-selected K_BF_H/A_M/J_Pi normalization convention",
            "why_it_blocks": "same algebraic action supports inequivalent unit assignments",
            "next_action": "derive from parent BF/mass-gauge action or select a convention as explicit closure",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "blocker_id": "BLK922_1_projection_coefficients",
            "missing_input": "C_eta,C_clock,C_gamma,C_beta,C_alpha_i,C_xi",
            "why_it_blocks": "epsilon_FM cannot be compared to arena bounds without weak-field projection",
            "next_action": "linearize the parent local branch or keep residual unscored",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "blocker_id": "BLK922_2_R10_range_law",
            "missing_input": "lambda_FM and alpha_FM(lambda)",
            "why_it_blocks": "R10 requires a range-dependent Yukawa-equivalent force law",
            "next_action": "derive range law or keep R10 symbolic",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "blocker_id": "BLK922_3_real_bound_curve",
            "missing_input": "valid digitized alpha(lambda) curve",
            "why_it_blocks": "current R10 digitized file contains MISSING_DIGITIZED_ALPHA_BOUND",
            "next_action": "use only source-backed anchors/nonclaim until real curve is available",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "BD922_0_units",
            "branch": "derive_KBFH_units",
            "verdict": "dimension_equations_written_no_parent_selection",
            "reason": "form degrees constrain but do not choose the physical normalization",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "decision_id": "BD922_1_smoke_runner",
            "branch": "strict_local_bound_smoke",
            "verdict": "all_scores_blocked_as_expected",
            "reason": "every arena row lacks numeric residuals/units/projection or has symbolic R10 bounds",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "decision_id": "BD922_2_next",
            "branch": "parent_normalization_or_first_real_bound_row",
            "verdict": "selected",
            "reason": "the next useful move is to derive the normalization or deliberately create one source-backed nonclaim row",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "CGATE922_0_KBFH_units",
            "claim": "K_BF_H units are parent-derived",
            "blocker": "multiple dimensional conventions remain legal",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "gate_id": "CGATE922_1_bound_scoring",
            "claim": "local-bound smoke runner scores the FM branch",
            "blocker": "strict runner blocks every row due missing numeric/source-backed inputs",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "gate_id": "CGATE922_2_R10",
            "claim": "R10 alpha(lambda) comparison is valid",
            "blocker": "no alpha_FM(lambda), no lambda_FM, and R10 digitized curve still placeholder",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "gate_id": "CGATE922_3_local_GR",
            "claim": "FM branch supports a local-GR/PPN pass",
            "blocker": "unit/projection/source-measure blockers remain open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "try to make the parent action select one mass-gauge normalization convention; if it cannot, create the first real nonclaim FM bound row with sourced units/placeholders clearly blocked",
            "include": "A_M connection choice, J_H 3-form normalization, k_M/K_BF_H relation, measured-GM calibration, first source-backed local-bound row",
            "exclude": "claiming a pass, choosing units after seeing bounds, free G/M absorption, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        }
    ]


def formalization_changed_count() -> int:
    formalization = ROOT.parent / "formalization-workbench"
    if not formalization.exists():
        return 0
    return sum(
        1
        for path in formalization.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def all_false(rows: list[dict[str, object]], fields: tuple[str, ...]) -> bool:
    return all(str(row.get(field, "")).strip().lower() != "true" for row in rows for field in fields)


def validation_rows(
    src: list[dict[str, object]],
    unit_branches: list[dict[str, object]],
    smoke_in: list[dict[str, object]],
    smoke_eval: list[dict[str, object]],
    blockers: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
) -> list[dict[str, object]]:
    source_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in src)
    prior = OUT / "P8_Y5_BRR545_921_VALIDATION.csv"
    prior_ok = prior.exists() and "V921_11_validation_rows_ready" in read_text(prior)
    false_fields = ("parent_selected", "claim_allowed", "valid_for_claim")
    all_blocked = all(row["runner_status"] == "blocked" for row in smoke_eval)
    changed = formalization_changed_count()
    generated = unit_branches + smoke_in + smoke_eval + blockers + decisions + gates
    return [
        {
            "check_id": "V922_0_sources_exist_and_needles",
            "result": "pass" if source_ok else "fail",
            "detail": "all source paths exist and needles are present" if source_ok else "missing source or needle",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V922_1_prior_921_clean",
            "result": "pass" if prior_ok else "fail",
            "detail": "P8_Y5_BRR545_921_VALIDATION.csv clean" if prior_ok else "921 validation missing or incomplete",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V922_2_unit_branches_not_parent_selected",
            "result": "pass" if all_false(unit_branches, false_fields) else "fail",
            "detail": "dimensional branches are audited but none is parent-selected",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V922_3_smoke_inputs_cover_arenas",
            "result": "pass" if len(smoke_in) >= 10 else "fail",
            "detail": "strict smoke inputs cover local-bound arena rows from 921",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V922_4_strict_runner_blocks_all_scores",
            "result": "pass" if all_blocked else "fail",
            "detail": "all smoke evaluations are blocked as expected",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V922_5_blockers_explicit",
            "result": "pass" if all_false(blockers, ("valid_for_claim",)) and len(blockers) >= 4 else "fail",
            "detail": "unit, projection, R10 range, and R10 curve blockers are explicit",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V922_6_claim_gates_false",
            "result": "pass" if all_false(gates, false_fields) else "fail",
            "detail": "KBFH units, bound scoring, R10, and local-GR gates remain false",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V922_7_decisions_nonclaim",
            "result": "pass" if all_false(decisions, false_fields) else "fail",
            "detail": "decisions select parent normalization or first nonclaim row without promotion",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V922_8_all_generated_rows_nonclaim",
            "result": "pass" if all_false(generated, false_fields) else "fail",
            "detail": "all generated rows keep guarded claim fields false",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V922_9_formalization_workbench_untouched",
            "result": "pass" if changed == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={changed}",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V922_10_next_target_selected",
            "result": "pass" if NEXT_TARGET.startswith("923-") else "fail",
            "detail": NEXT_TARGET,
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V922_11_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
            "generated_utc": GENERATED,
        },
    ]


def write_doc(
    src: list[dict[str, object]],
    summary: list[dict[str, object]],
    unit_branches: list[dict[str, object]],
    smoke_in: list[dict[str, object]],
    smoke_eval: list[dict[str, object]],
    blockers: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    body = f"""# 922 - Y5/R10 KBFH Parent Units And Normalization Or Local Bound Smoke Runner

Private unit/runner checkpoint. This is not a public R10, WEP, clock, PPN, orbital, local-GR, or unified-field claim.

Status: `{STATUS}`

Claim ceiling: `{CLAIM_CEILING}`

Current result: **the action fixes form-degree bookkeeping, but not the physical normalization.**

The coupling has the schematic form:

```text
S_src = K_BF_H integral A_M wedge J_Pi.
```

So:

```text
[K_BF_H] [A_M] [J_Pi] [L]^4 = [action].
```

That equation is useful, but it does not decide whether `A_M` is a dimensionless topological connection, an inverse-length gauge potential, or a normalized mass-charge connection. Because those branches produce different `K_BF_H`, the theory is not allowed to score local bounds yet.

The strict smoke runner therefore does the right boring thing: every row blocks.

## Non-Claim Summary

{md_table(summary, ["status", "claim_ceiling", "current_result", "practical_meaning", "next_target", "valid_for_claim", "generated_utc"])}

## Source Register

{md_table(src, ["source_id", "path", "role", "needle", "exists", "needle_found", "valid_for_claim", "generated_utc"])}

## KBFH Unit Branch Audit

{md_table(unit_branches, ["branch_id", "assumption", "dimension_condition", "what_it_fixes", "blocker", "parent_selected", "valid_for_claim", "generated_utc"])}

## Strict Smoke Inputs

{md_table(smoke_in, ["smoke_id", "local_bound_row", "observable", "upper_bound", "FM_residual", "predicted_value", "required_inputs", "expected_status", "valid_for_claim", "generated_utc"])}

## Strict Smoke Evaluation

{md_table(smoke_eval, ["eval_id", "local_bound_row", "observable", "predicted_value", "upper_bound", "runner_status", "block_reason", "claim_allowed", "valid_for_claim", "generated_utc"])}

## Blocker Ledger

{md_table(blockers, ["blocker_id", "missing_input", "why_it_blocks", "next_action", "valid_for_claim", "generated_utc"])}

## Branch Decision

{md_table(decisions, ["decision_id", "branch", "verdict", "reason", "claim_allowed", "valid_for_claim", "generated_utc"])}

## Claim Gate

{md_table(gates, ["gate_id", "claim", "blocker", "claim_allowed", "valid_for_claim", "generated_utc"])}

## Next Target

{md_table(next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])}

## Validation

{md_table(validation, ["check_id", "result", "detail", "generated_utc"])}
"""
    (ROOT / DOC_NAME).write_text(body, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    src = build_sources()
    summary = summary_rows()
    unit_branches = unit_branch_rows()
    smoke_in = smoke_inputs()
    smoke_eval = smoke_eval_rows(smoke_in)
    blockers = blocker_rows()
    decisions = decision_rows()
    gates = gate_rows()
    next_target = next_rows()
    validation = validation_rows(src, unit_branches, smoke_in, smoke_eval, blockers, decisions, gates)

    write_csv(OUT / "P8_Y5_R10_922_SOURCE_REGISTER.csv", src, ["source_id", "path", "absolute_path", "role", "needle", "exists", "needle_found", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_922_NONCLAIM_SUMMARY.csv", summary, ["status", "claim_ceiling", "current_result", "practical_meaning", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_922_KBFH_UNIT_BRANCH_AUDIT.csv", unit_branches, ["branch_id", "assumption", "dimension_condition", "what_it_fixes", "blocker", "parent_selected", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_922_STRICT_SMOKE_INPUTS.csv", smoke_in, ["smoke_id", "local_bound_row", "observable", "upper_bound", "FM_residual", "predicted_value", "units", "required_inputs", "expected_status", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_922_STRICT_SMOKE_EVALUATION.csv", smoke_eval, ["eval_id", "local_bound_row", "observable", "predicted_value", "upper_bound", "runner_status", "block_reason", "claim_allowed", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_922_BLOCKER_LEDGER.csv", blockers, ["blocker_id", "missing_input", "why_it_blocks", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_922_BRANCH_DECISION.csv", decisions, ["decision_id", "branch", "verdict", "reason", "claim_allowed", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_922_CLAIM_GATE.csv", gates, ["gate_id", "claim", "blocker", "claim_allowed", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_922_NEXT_TARGET.csv", next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_BRR545_922_VALIDATION.csv", validation, ["check_id", "result", "detail", "generated_utc"])
    write_doc(src, summary, unit_branches, smoke_in, smoke_eval, blockers, decisions, gates, next_target, validation)

    failed = [row for row in validation if row["result"] != "pass"]
    if failed:
        raise SystemExit(f"validation failed: {failed}")
    print(STATUS)
    print(f"wrote {ROOT / DOC_NAME}")
    print(f"next target: {NEXT_TARGET}")


if __name__ == "__main__":
    main()
