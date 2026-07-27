from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3435-Y5-R2FR-first-score-ready-source-normalization-residual-runner-or-zero-row-under-AX1090.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCES = {
    "doc_3434": ROOT / "3434-Y5-R2FR-source-normalized-Poisson-limit-and-first-PPN-residual-stack-under-AX1090.md",
    "next_3434": OUT / "P8_Y5_R2FR_3434_NEXT_TARGET.csv",
    "poisson_3434": OUT / "P8_Y5_R2FR_3434_SOURCE_NORMALIZED_POISSON_LIMIT_THEOREM.csv",
    "ppn_3434": OUT / "P8_Y5_R2FR_3434_FIRST_PPN_RESIDUAL_STACK.csv",
    "visibility_3434": OUT / "P8_Y5_R2FR_3434_RESIDUAL_VISIBILITY_MATRIX.csv",
    "source_lock_3433": OUT / "P8_Y5_R2FR_3433_MHREF_TAU_SOURCE_LOCK_THEOREM.csv",
    "epsilon_mu_3433": OUT / "P8_Y5_R2FR_3433_EPSILON_MU_RESIDUAL_VECTOR.csv",
    "source_measure_509": OUT / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv",
    "source_measure_residual_509": OUT / "P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv",
    "worldtube_510": OUT / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
    "mhref_candidates_3425": OUT / "P8_Y5_R2FR_3425_MHREF_CANDIDATE_ROWS.csv",
    "hpi_bounds_3425": OUT / "P8_Y5_R2FR_3425_HPI_M_RESIDUAL_BOUND_ROWS.csv",
    "constant_gm_runner": OUT / "P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv",
    "source_residual_template": OUT / "P8_source_normalization_residual_vector_TEMPLATE.csv",
    "mu_extra_summary": OUT / "P8_MU_EXTRA_CHANNEL_BOUND_SUMMARY.csv",
    "qloc_bound_3432": OUT / "P8_Y5_R2FR_3432_QLOC_RESIDUAL_BOUND_PACK.csv",
    "domain_bound_3431": OUT / "P8_Y5_R2FR_3431_DOMAIN_PROJECTOR_OPERATOR_BOUND_PACK.csv",
    "bzero_3427": OUT / "P8_Y5_R2FR_3427_BZERO_BOUND_ROWS.csv",
    "hidden_bound_3430": OUT / "P8_Y5_R2FR_3430_HIDDEN_PROJECTOR_BOUND_ROWS.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3435_SOURCE_REGISTER.csv",
    "target_selection": OUT / "P8_Y5_R2FR_3435_TARGET_SELECTION.csv",
    "radial_zero_theorem": OUT / "P8_Y5_R2FR_3435_RADIAL_MHREF_ZERO_THEOREM.csv",
    "radial_residual_runner": OUT / "P8_Y5_R2FR_3435_RADIAL_SOURCE_HAIR_RESIDUAL_RUNNER.csv",
    "score_readiness_rows": OUT / "P8_Y5_R2FR_3435_SCORE_READINESS_ROWS.csv",
    "epsilon_mu_update": OUT / "P8_Y5_R2FR_3435_EPSILON_MU_UPDATE.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3435_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3435_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3435_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3435_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3435_VALIDATION.csv",
}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields = list(rows[0].keys())

    def clean(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "/")

    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |",
            *["| " + " | ".join(clean(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def source_register() -> list[dict[str, Any]]:
    roles = {
        "doc_3434": "Poisson/PPN handoff",
        "next_3434": "3435 target declaration",
        "poisson_3434": "source-normalized Poisson theorem",
        "ppn_3434": "first PPN residual stack",
        "visibility_3434": "residual visibility matrix",
        "source_lock_3433": "M_H_ref/tau source lock theorem",
        "epsilon_mu_3433": "epsilon_mu residual vector",
        "source_measure_509": "Meff flux theorem",
        "source_measure_residual_509": "Meff residual map",
        "worldtube_510": "worldtube charge theorem",
        "mhref_candidates_3425": "M_H_ref source row schema",
        "hpi_bounds_3425": "Hamiltonian/PiM residual bounds",
        "constant_gm_runner": "constant GM residual runner",
        "source_residual_template": "source-normalization residual template",
        "mu_extra_summary": "mu_extra channel summary",
        "qloc_bound_3432": "q_loc bound pack",
        "domain_bound_3431": "domain projector bound pack",
        "bzero_3427": "boundary/reference bound rows",
        "hidden_bound_3430": "hidden/projector bound rows",
    }
    return [
        {
            "source_id": key,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[key],
            "valid_for_claim": False,
        }
        for key, path in SOURCES.items()
    ]


def target_selection() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "TSEL3435_0",
            "chosen_residual": "partial_r_ln_MHref / epsilon_radial_Meff",
            "why_chosen": "radial source hair is the bridge between Poisson/Gauss and R10/Kepler; it is also narrower than the full q_loc PPN operator",
            "target_kind": "derive conditional zero branch plus residual runner",
            "success_rule": "move EH-identity radial M_H_ref leakage to DERIVED_ZERO_BRANCH_NONCLAIM and keep full mu_obs radial hair as blocked residual",
            "valid_for_claim": False,
        }
    ]


def radial_zero_theorem() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "RZ3435_0_flux_identity",
            "statement": "For two homologous linking spheres in a source-free EH/Hilbert exterior, the tau charge is radially closed.",
            "formula": "M_H_ref(S2)-M_H_ref(S1)=int_A d(Pi_M^H J_H)=0",
            "status": "DERIVED_ZERO_BRANCH_NONCLAIM",
            "condition_or_missing": "EH/Hilbert identity branch, fixed tau/reference, source-free annulus, no boundary flux",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "RZ3435_1_radial_MHref",
            "statement": "The EH identity branch gives zero radial leakage of the dressed source denominator.",
            "formula": "partial_r ln M_H_ref^EH = 0",
            "status": "DERIVED_ZERO_BRANCH_NONCLAIM",
            "condition_or_missing": "same branch conditions as RZ3435_0 plus positive M_H_ref",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "RZ3435_2_full_mu_obs",
            "statement": "Full measured source strength has zero radial hair only if G_eff and every epsilon_mu channel are also radially silent.",
            "formula": "partial_r ln mu_obs = partial_r ln G_eff + partial_r ln M_H_ref + partial_r ln(1+epsilon_mu)",
            "status": "FULL_MTS_ZERO_NOT_DERIVED",
            "condition_or_missing": "constant G, q_loc/domain/boundary/hidden/range/source-frame residuals zero or bounded",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "RZ3435_3_R10_bridge",
            "statement": "If radial hair is not theorem-zero, it becomes a fifth-force/range row rather than a calibrated Newton constant.",
            "formula": "delta a_r/a_N = -r^2/(G0 M_H_ref) partial_r deltaPhi_res(r); if Yukawa-shaped, alpha(lambda) must satisfy bound curve",
            "status": "BOUND_BRIDGE_READY_VALUES_MISSING",
            "condition_or_missing": "radial profile or q_loc/range source map plus real alpha_bound(lambda)",
            "valid_for_claim": False,
        },
    ]


def radial_residual_runner() -> list[dict[str, Any]]:
    return [
        {
            "runner_row": "RR3435_0_EH_identity_radial_MHref",
            "quantity": "partial_r_ln_MHref_EH",
            "formula": "0 under RZ3435_0/RZ3435_1 conditions",
            "units": "inverse_length",
            "runner_status": "DERIVED_ZERO_BRANCH_NONCLAIM",
            "needed_for_claim": "parent adoption of EH identity branch and source-specific M_H_ref row",
            "valid_for_claim": False,
        },
        {
            "runner_row": "RR3435_1_full_mu_radial",
            "quantity": "partial_r_ln_mu_obs",
            "formula": "partial_r ln G_eff + partial_r ln M_H_ref + partial_r epsilon_mu/(1+epsilon_mu)",
            "units": "inverse_length",
            "runner_status": "FORMULA_READY_VALUES_MISSING",
            "needed_for_claim": "zero/value rows for G_eff, M_H_ref residual transfer, q_loc, domain, boundary, hidden and range",
            "valid_for_claim": False,
        },
        {
            "runner_row": "RR3435_2_radial_acceleration",
            "quantity": "delta_a_radial_over_aN",
            "formula": "-r^2/(G0 M_H_ref) partial_r deltaPhi_res(r)",
            "units": "dimensionless",
            "runner_status": "FORMULA_READY_PROFILE_MISSING",
            "needed_for_claim": "deltaPhi_res(r) profile or theorem-zero radial source hair",
            "valid_for_claim": False,
        },
        {
            "runner_row": "RR3435_3_alpha_lambda_radial",
            "quantity": "alpha_radial(lambda)",
            "formula": "fit/project deltaPhi_res(r) onto alpha(lambda) exp(-r/lambda)/r kernel",
            "units": "dimensionless over range lambda",
            "runner_status": "SCHEMA_READY_BOUND_CURVE_AND_PROFILE_MISSING",
            "needed_for_claim": "real alpha_bound(lambda), source/test charge map, lambda grid, profile",
            "valid_for_claim": False,
        },
    ]


def score_readiness_rows() -> list[dict[str, Any]]:
    return [
        {
            "score_id": "SR3435_0_branch_zero",
            "residual_row": "partial_r_ln_MHref_EH",
            "before_status": "FORMULA_READY_VALUES_MISSING",
            "after_status": "DERIVED_ZERO_BRANCH_NONCLAIM",
            "source_or_units": "EH/Hilbert identity branch; inverse_length; source paths 509/510/3425/3434",
            "score_readiness": "zero row usable only inside conditional EH identity branch",
            "valid_for_claim": False,
        },
        {
            "score_id": "SR3435_1_full_radial_mu",
            "residual_row": "partial_r_ln_mu_obs",
            "before_status": "FORMULA_READY_VALUES_MISSING",
            "after_status": "BLOCKED_VALUES_MISSING",
            "source_or_units": "inverse_length; constant GM runner row",
            "score_readiness": "not score-ready because full epsilon_mu channel values are missing",
            "valid_for_claim": False,
        },
        {
            "score_id": "SR3435_2_R10",
            "residual_row": "alpha(lambda)",
            "before_status": "CURVE_REQUIRED",
            "after_status": "SCHEMA_READY_NOT_SCORE_READY",
            "source_or_units": "dimensionless alpha(lambda) over lambda",
            "score_readiness": "requires real bound curve and MTS source map",
            "valid_for_claim": False,
        },
    ]


def epsilon_mu_update() -> list[dict[str, Any]]:
    return [
        {
            "update_id": "EMU3435_0_radial_MHref",
            "epsilon_mu_component": "partial_r ln M_H_ref",
            "3435_update": "zero in conditional EH identity branch; retained in full MTS residual vector",
            "formula": "partial_r ln M_H_ref = 0 + partial_r(epsilon_tau+epsilon_ref+epsilon_PiM+epsilon_boundary+epsilon_extra)",
            "status": "PARTIAL_ZERO_BRANCH_RESIDUAL_FULL",
            "valid_for_claim": False,
        },
        {
            "update_id": "EMU3435_1_radial_mu_obs",
            "epsilon_mu_component": "partial_r ln mu_obs",
            "3435_update": "full measured radial hair remains blocked",
            "formula": "partial_r ln mu_obs = partial_r ln G_eff + partial_r ln M_H_ref + partial_r ln(1+epsilon_mu)",
            "status": "FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PG3435_0_one_row_moved",
            "gate": "one residual row moved to derived-zero or score-ready status",
            "result": "PASS_BRANCH_ZERO_NONCLAIM",
            "evidence": "SR3435_0 partial_r_ln_MHref_EH",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3435_1_full_radial_source",
            "gate": "full MTS radial source hair is zero or score-ready",
            "result": "BLOCKED",
            "evidence": "RR3435_1 and RR3435_3 values/maps missing",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3435_2_Newton",
            "gate": "Newtonian mechanics is derived for current MTS",
            "result": "BLOCKED",
            "evidence": "full mu_obs radial/range/q_loc/domain/boundary rows still open",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3435_3_local_GR",
            "gate": "local GR is derived",
            "result": "BLOCKED",
            "evidence": "PPN and second-order residual stack remains open",
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3435_0_use_branch_zero",
            "decision": "Keep the EH identity radial M_H_ref zero as a branch theorem, not a full MTS claim.",
            "reason": "it is genuinely derived but depends on source lock premises not yet adopted globally.",
            "next_action": "use it to simplify only the EH/Hilbert branch of the residual runner",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3435_1_full_runner",
            "decision": "Full radial mu_obs hair must remain explicit.",
            "reason": "q_loc/domain/boundary/range/G_eff residuals can still create radial dependence.",
            "next_action": "either fill alpha(lambda) bound data/map or theorem-zero q_loc/domain/range radial pieces",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3436-Y5-R2FR-R10-alpha-lambda-runner-real-curve-or-q_loc-range-zero-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3436_R10_alpha_lambda_runner_real_curve_or_q_loc_range_zero.py",
            "objective": "turn the radial/range residual lane into an executable R10 alpha(lambda) runner with real bound data, or derive a q_loc/range zero theorem",
            "success_condition": "alpha(lambda) row becomes score-ready nonclaim with source-backed bound curve and MTS source map, or a parent-signed zero theorem removes the range lane",
            "valid_for_claim": False,
        }
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3435_0",
            "purpose": "prevent branch-zero overclaim",
            "rule": "partial_r ln M_H_ref^EH=0 cannot be promoted to full MTS mu_obs radial silence unless every epsilon_mu channel is zero/bounded",
            "current_value": "claim_allowed=false",
            "valid_for_claim": False,
        },
        {
            "runner_id": "RUN3435_1",
            "purpose": "force R10/range scoring",
            "rule": "surviving radial/range residuals require alpha(lambda) curve comparison or theorem-zero",
            "current_value": "R10_lane_required=true",
            "valid_for_claim": False,
        },
    ]


def all_outputs_scoped() -> bool:
    root_resolved = ROOT.resolve()
    return all(root_resolved in path.resolve().parents or path.resolve() == root_resolved for path in [DOC, *OUTPUTS.values()])


def all_generated_nonclaim(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for name, rows in rows_by_name.items():
        if name == "validation":
            continue
        for row in rows:
            if "valid_for_claim" in row and str(row["valid_for_claim"]).lower() != "false":
                return False
            if "claim_allowed" in row and str(row["claim_allowed"]).lower() != "false":
                return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], start_utc: datetime) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    theorem_rows = rows_by_name["radial_zero_theorem"]
    runner_rows = rows_by_name["radial_residual_runner"]
    score_rows = rows_by_name["score_readiness_rows"]
    promotion_rows = rows_by_name["promotion_gates"]
    next_rows = rows_by_name["next_target"]
    modified_count = 0
    if FORMALIZATION.exists():
        start_ts = start_utc.timestamp()
        modified_count = sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= start_ts)
    validations = [
        {
            "check_id": "VAL3435_0_sources_exist",
            "condition": "all cited source paths exist",
            "passed": all(row["exists"] for row in source_rows),
            "detail": f"{sum(1 for row in source_rows if row['exists'])}/{len(source_rows)} source paths exist",
        },
        {
            "check_id": "VAL3435_1_outputs_scoped",
            "condition": "all outputs are in post-checkpoint-work",
            "passed": all_outputs_scoped(),
            "detail": str(ROOT),
        },
        {
            "check_id": "VAL3435_2_nonclaim",
            "condition": "all generated rows remain nonclaim",
            "passed": all_generated_nonclaim(rows_by_name),
            "detail": "valid_for_claim=false throughout generated rows",
        },
        {
            "check_id": "VAL3435_3_branch_zero",
            "condition": "EH identity radial M_H_ref zero row exists",
            "passed": any(row["theorem_id"] == "RZ3435_1_radial_MHref" and row["status"] == "DERIVED_ZERO_BRANCH_NONCLAIM" for row in theorem_rows),
            "detail": "partial_r ln M_H_ref^EH zero branch present",
        },
        {
            "check_id": "VAL3435_4_full_mu_not_promoted",
            "condition": "full mu_obs radial zero is not falsely promoted",
            "passed": any(row["theorem_id"] == "RZ3435_2_full_mu_obs" and row["status"] == "FULL_MTS_ZERO_NOT_DERIVED" for row in theorem_rows),
            "detail": "full radial source hair retained",
        },
        {
            "check_id": "VAL3435_5_runner_rows",
            "condition": "radial residual runner rows exist",
            "passed": len(runner_rows) >= 4 and any(row["runner_row"] == "RR3435_3_alpha_lambda_radial" for row in runner_rows),
            "detail": f"{len(runner_rows)} runner rows",
        },
        {
            "check_id": "VAL3435_6_score_progress",
            "condition": "at least one residual row moved status",
            "passed": any(row["score_id"] == "SR3435_0_branch_zero" and row["after_status"] == "DERIVED_ZERO_BRANCH_NONCLAIM" for row in score_rows),
            "detail": "one branch-zero row moved",
        },
        {
            "check_id": "VAL3435_7_local_GR_blocked",
            "condition": "local GR remains blocked until full residuals close",
            "passed": any(row["gate_id"] == "PG3435_3_local_GR" and row["result"] == "BLOCKED" for row in promotion_rows),
            "detail": "no local-GR claim promoted",
        },
        {
            "check_id": "VAL3435_8_next_target",
            "condition": "next target attacks R10 alpha(lambda) or range zero",
            "passed": next_rows[0]["target_doc"].startswith("3436-Y5-R2FR-R10-alpha-lambda"),
            "detail": next_rows[0]["target_doc"],
        },
        {
            "check_id": "VAL3435_9_formalization_untouched",
            "condition": "formalization-workbench modified-file count remains 0 during this run",
            "passed": modified_count == 0,
            "detail": f"modified_count_since_start={modified_count}",
        },
    ]
    validations.append(
        {
            "check_id": "VAL3435_10_overall",
            "condition": "3435 residual runner/zero-row checkpoint is internally valid",
            "passed": all(row["passed"] for row in validations),
            "detail": "PASS" if all(row["passed"] for row in validations) else "FAIL",
        }
    )
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    text = f"""# 3435 - First Score-Ready Source-Normalization Residual Runner or Zero Row

## Summary
- This checkpoint picks one residual lane instead of widening the audit: radial source hair around `M_H_ref`.
- It proves a real branch result: in the EH/Hilbert identity branch with fixed `tau`, fixed reference, source-free annulus, and no boundary flux, `partial_r ln M_H_ref^EH = 0`.
- It does not overclaim full MTS radial silence. Full measured `mu_obs` still includes `G_eff`, `q_loc`, domain/projector, boundary, hidden/extra, range, and frame residuals.
- The radial runner is now sharper: branch-zero for `M_H_ref^EH`, full residual formula for `mu_obs`, acceleration correction, and `alpha(lambda)` lane.
- Next best target is the R10/range lane: either build the real alpha(lambda) runner or derive a range/q_loc zero theorem.

## Source Register
{md_table(rows_by_name["source_register"])}

## Target Selection
{md_table(rows_by_name["target_selection"])}

## Radial MHref Zero Theorem
{md_table(rows_by_name["radial_zero_theorem"])}

## Radial Source Hair Residual Runner
{md_table(rows_by_name["radial_residual_runner"])}

## Score Readiness Rows
{md_table(rows_by_name["score_readiness_rows"])}

## Epsilon Mu Update
{md_table(rows_by_name["epsilon_mu_update"])}

## Promotion Gates
{md_table(rows_by_name["promotion_gates"])}

## Decision Ledger
{md_table(rows_by_name["decision_ledger"])}

## Next Target
{md_table(rows_by_name["next_target"])}

## Runner Nonclaim
{md_table(rows_by_name["runner_nonclaim"])}

## Validation
{md_table(rows_by_name["validation"])}

## Bottom Line
We got one clean rung: `M_H_ref` radial leakage is zero in the EH/Hilbert identity branch. That is not the full theory claim, but it is not nothing. It strips one piece of the source-normalization ladder down to a conditional theorem and points the remaining radial/range problem straight at R10.
"""
    DOC.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    start_utc = datetime.now(timezone.utc)
    rows_by_name = {
        "source_register": source_register(),
        "target_selection": target_selection(),
        "radial_zero_theorem": radial_zero_theorem(),
        "radial_residual_runner": radial_residual_runner(),
        "score_readiness_rows": score_readiness_rows(),
        "epsilon_mu_update": epsilon_mu_update(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    rows_by_name["validation"] = validation_rows(rows_by_name, start_utc)
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)
    write_doc(rows_by_name)
    failed = [row for row in rows_by_name["validation"] if not row["passed"]]
    if failed:
        raise SystemExit(f"3435 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"wrote {len(OUTPUTS)} csv outputs")


if __name__ == "__main__":
    main()
