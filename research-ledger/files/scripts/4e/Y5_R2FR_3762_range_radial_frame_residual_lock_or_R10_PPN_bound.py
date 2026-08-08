import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3762"
BRANCH = "MTS_R2FR_Y5_RANGE_RADIAL_FRAME_RESIDUAL_LOCK_OR_R10_PPN_BOUND_3762"
PCW = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work"
)
RESIDUALS = PCW / "source-intake" / "mts_residuals"
FORMALIZATION = PCW.parent / "formalization-workbench"
DOC_PATH = PCW / "3762-Y5-R2FR-range-radial-frame-residual-lock-or-R10-PPN-bound.md"


OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3762_SOURCE_REGISTER.csv",
    "locks": RESIDUALS / "P8_Y5_R2FR_3762_RANGE_RADIAL_FRAME_LOCKS.csv",
    "budgets": RESIDUALS / "P8_Y5_R2FR_3762_RANGE_RADIAL_FRAME_RESIDUAL_BUDGET.csv",
    "runner_patch": RESIDUALS / "P8_Y5_R2FR_3762_COUPLING_RUNNER_PATCH.csv",
    "claim_matrix": RESIDUALS / "P8_Y5_R2FR_3762_LOCAL_GR_CLAIM_MATRIX.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_3762_CLAIM_GATES.csv",
    "decision_rows": RESIDUALS / "P8_Y5_R2FR_3762_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3762_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3762_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3762_VALIDATION.csv",
}


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(timestamp: str, valid_for_claim: bool = False) -> dict[str, object]:
    return {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH,
        "checkpoint_id": CHECKPOINT,
        "valid_for_claim": valid_for_claim,
    }


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_paths() -> dict[str, Path]:
    return {
        "SRC3762_0_3761_doc": PCW / "3761-Y5-R2FR-PPN-total-stress-projection-gamma-beta-or-residual.md",
        "SRC3762_1_3761_next": RESIDUALS / "P8_Y5_R2FR_3761_NEXT_TARGET.csv",
        "SRC3762_2_3761_ppn_theorem": RESIDUALS / "P8_Y5_R2FR_3761_PPN_TOTAL_STRESS_PROJECTION_THEOREM.csv",
        "SRC3762_3_3761_gamma_beta": RESIDUALS / "P8_Y5_R2FR_3761_GAMMA_BETA_BOUND_EVALUATION.csv",
        "SRC3762_4_3761_ppn_residual": RESIDUALS / "P8_Y5_R2FR_3761_PPN_RESIDUAL_BUDGET.csv",
        "SRC3762_5_3761_runner": RESIDUALS / "P8_Y5_R2FR_3761_COUPLING_RUNNER_PATCH.csv",
        "SRC3762_6_3760_em_residual": RESIDUALS / "P8_Y5_R2FR_3760_EM_SOURCE_RESIDUAL_BUDGET.csv",
        "SRC3762_7_3758_kappa_law": RESIDUALS / "P8_Y5_R2FR_3758_KAPPA_QUOTIENT_FLUX_LAW.csv",
        "SRC3762_8_3759_wep_bound": RESIDUALS / "P8_Y5_R2FR_3759_WEP_BOUND_EVALUATION.csv",
        "SRC3762_9_gm_matrix": RESIDUALS / "P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv",
        "SRC3762_10_delta_kappa_exchange": RESIDUALS / "P8_delta_kappa_source_exchange_residual.csv",
    }


def source_register(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "source_id": source_id,
            "source_path": str(path),
            "source_exists": path.exists(),
            "role": "3762 range/radial/frame local-GR residual input",
        }
        for source_id, path in source_paths().items()
    ]


def lock_rows(timestamp: str) -> list[dict[str, object]]:
    entries = [
        (
            "RRF3762_0_no_range_mediator",
            "If the local branch has no unscreened propagating scalar/vector/tensor mediator outside the EH metric/coframe and same total source, then alpha(lambda)=0 for all finite lambda.",
            "Requires parent spectrum/no-hair signature; otherwise R10 curve is required.",
            "EXACT_CONDITIONAL_ZERO_THEOREM",
        ),
        (
            "RRF3762_1_alpha_curve_fallback",
            "If any finite-range mediator remains, R10 scoring requires table rows (lambda, alpha_predicted) compared against alpha_bound(lambda).",
            "Scalar placeholders or a single alpha value are not enough.",
            "EXECUTABLE_BOUND_INTERFACE_REQUIRED",
        ),
        (
            "RRF3762_2_no_radial_hair",
            "If kappa_eff, source charge, Poisson calibration, and extra-field amplitudes are constant outside a compact local source, then partial_r ln mu_obs=0.",
            "This is the radial version of the local no-hair/source-conservation route.",
            "EXACT_CONDITIONAL_ZERO_THEOREM",
        ),
        (
            "RRF3762_3_radial_profile_fallback",
            "If radial hair remains, score partial_r ln mu_obs by an explicit profile: partial_r ln mu_obs = partial_r ln kappa_eff + partial_r ln C_M + partial_r ln Z_Poisson + partial_r ln Z_extra.",
            "The profile must be mapped to R10/orbital/PPN bounds.",
            "PROFILE_BOUND_INTERFACE_REQUIRED",
        ),
        (
            "RRF3762_4_single_observed_frame",
            "If matter, light, clocks, EM, and source readout all descend to one observed metric/coframe and one local time generator, then delta_frame_source=0.",
            "This prevents a hidden source-frame or preferred-frame coupling.",
            "EXACT_CONDITIONAL_ZERO_THEOREM",
        ),
        (
            "RRF3762_5_frame_residual_fallback",
            "If frame descent is unsigned, delta_frame_source must be decomposed into clock drift, light-cone split, source-frame split, and preferred-frame PPN residuals.",
            "This feeds WEP, clocks, gamma/beta, and preferred-frame tests.",
            "FRAME_BOUND_INTERFACE_REQUIRED",
        ),
    ]
    return [
        {
            **base(timestamp),
            "lock_id": lock_id,
            "statement": statement,
            "premise_or_fallback": premise_or_fallback,
            "status": status,
            "parent_signed": False,
            "claim_allowed": False,
        }
        for lock_id, statement, premise_or_fallback, status in entries
    ]


def budget_rows(timestamp: str) -> list[dict[str, object]]:
    entries = [
        (
            "RRF_BUD3762_0_alpha_lambda",
            "alpha(lambda)",
            "R10 inverse-square",
            "sum_X |A_X|^2 |Q_X|^2 exp(-r/lambda_X) projected into alpha_predicted(lambda)",
            "alpha_bound(lambda)",
            "range-dependent",
            "zero if RRF3762_0_no_range_mediator is parent-signed",
            "BOUND_CURVE_REQUIRED_NUMERIC_COMPONENTS_MISSING",
        ),
        (
            "RRF_BUD3762_1_radial_hair",
            "partial_r_ln_mu_obs",
            "orbital/R10/radial source profile",
            "|partial_r ln kappa_eff| + |partial_r ln C_M| + |partial_r ln Z_Poisson| + |partial_r ln Z_extra|",
            "zero_or_mapped_bound",
            "inverse_length_or_dimensionless_envelope",
            "zero if RRF3762_2_no_radial_hair is parent-signed",
            "PROFILE_BOUND_REQUIRED_NUMERIC_COMPONENTS_MISSING",
        ),
        (
            "RRF_BUD3762_2_frame_split",
            "delta_frame_source",
            "WEP/clock/preferred-frame",
            "|delta_clock_frame| + |delta_light_cone| + |delta_source_frame| + |delta_preferred_frame|",
            "zero_or_row_locks",
            "dimensionless",
            "zero if RRF3762_4_single_observed_frame is parent-signed",
            "FRAME_BOUND_REQUIRED_NUMERIC_COMPONENTS_MISSING",
        ),
    ]
    return [
        {
            **base(timestamp),
            "budget_id": budget_id,
            "symbol": symbol,
            "arena": arena,
            "residual_formula": residual_formula,
            "bound_or_target": bound_or_target,
            "units": units,
            "zero_condition": zero_condition,
            "score_status": score_status,
            "prediction_value": "MISSING_NUMERIC_COMPONENTS_OR_PARENT_ZERO_SIGNATURE",
            "valid_prediction_row": False,
            "claim_allowed": False,
        }
        for budget_id, symbol, arena, residual_formula, bound_or_target, units, zero_condition, score_status in entries
    ]


def runner_patch_rows(timestamp: str) -> list[dict[str, object]]:
    rows = []
    for source_row in read_csv(source_paths()["SRC3762_5_3761_runner"]):
        patched = {
            **base(timestamp),
            "patched_runner_row_id": f"RUN3762_{source_row['residual_id']}",
            "source_runner_row": source_row["patched_runner_row_id"],
            "residual_id": source_row["residual_id"],
            "symbol": source_row["symbol"],
            "arena": source_row["arena"],
            "bound_value": source_row["bound_value"],
            "units": source_row["units"],
            "prediction_status_3761": source_row["prediction_status_3761"],
            "score_status_3761": source_row["score_status_3761"],
            "prediction_status_3762": source_row["prediction_status_3761"],
            "score_status_3762": source_row["score_status_3761"],
            "prediction_or_bound_formula_3762": source_row["prediction_or_bound_formula_3761"],
            "conditional_score_ready": source_row["conditional_score_ready"],
            "valid_prediction_row": False,
            "claim_allowed": False,
            "notes": "unchanged from 3761",
        }
        if source_row["residual_id"] == "KRV3755_2_range":
            patched.update(
                {
                    "prediction_status_3762": "ZERO_IF_NO_RANGE_MEDIATOR_OR_ALPHA_LAMBDA_CURVE_REQUIRED",
                    "score_status_3762": "CONDITIONAL_ZERO_OR_R10_CURVE_BOUND_REQUIRED",
                    "prediction_or_bound_formula_3762": "alpha(lambda)=0 if no unscreened finite-range mediator/hair is parent-signed; otherwise require executable alpha_predicted(lambda) curve against alpha_bound(lambda)",
                    "conditional_score_ready": True,
                    "notes": "range row now has zero theorem route plus executable curve fallback",
                }
            )
        if source_row["residual_id"] == "KRV3755_3_radial":
            patched.update(
                {
                    "prediction_status_3762": "ZERO_IF_NO_RADIAL_HAIR_OR_PROFILE_BOUND_REQUIRED",
                    "score_status_3762": "CONDITIONAL_ZERO_OR_RADIAL_PROFILE_BOUND_REQUIRED",
                    "prediction_or_bound_formula_3762": "partial_r ln mu_obs=0 if no radial hair/source drift is parent-signed; otherwise |partial_r ln kappa_eff|+|partial_r ln C_M|+|partial_r ln Z_Poisson|+|partial_r ln Z_extra| must be mapped to bounds",
                    "conditional_score_ready": True,
                    "notes": "radial row now has no-hair zero route plus profile fallback",
                }
            )
        if source_row["residual_id"] == "KRV3755_5_frame":
            patched.update(
                {
                    "prediction_status_3762": "ZERO_IF_SINGLE_OBSERVED_FRAME_OR_FRAME_RESIDUAL_BOUND_REQUIRED",
                    "score_status_3762": "CONDITIONAL_ZERO_OR_FRAME_BOUND_REQUIRED",
                    "prediction_or_bound_formula_3762": "delta_frame_source=0 if matter/light/clocks/EM/source use one observed metric/coframe and time generator; otherwise decompose clock/light/source/preferred-frame residuals",
                    "conditional_score_ready": True,
                    "notes": "frame row now has single-frame zero route plus residual decomposition fallback",
                }
            )
        rows.append(patched)
    return rows


def claim_matrix_rows(timestamp: str) -> list[dict[str, object]]:
    entries = [
        ("CM3762_0_Gdot", "dln_Geff_dt", "conditionally scoreable from 3758", "parent kappa/no-flux signatures unsigned"),
        ("CM3762_1_WEP", "eta_source_AB", "conditionally scoreable from 3759", "same-action/source-universality signatures unsigned"),
        ("CM3762_2_EM", "eta_EM_AB/delta_gamma_EM/delta_beta_EM", "same-source or residual interface from 3760", "MTS EM descent unsigned"),
        ("CM3762_3_gamma", "gamma_minus_1", "conditionally scoreable from 3761", "local EH/same-frame signatures unsigned"),
        ("CM3762_4_beta", "beta_minus_1", "conditionally scoreable from 3761", "second-order EH/source signatures unsigned"),
        ("CM3762_5_range", "alpha(lambda)", "zero-or-curve interface from 3762", "no-range mediator theorem or curve missing"),
        ("CM3762_6_radial", "partial_r_ln_mu_obs", "zero-or-profile interface from 3762", "no-radial-hair theorem or profile missing"),
        ("CM3762_7_frame", "delta_frame_source", "zero-or-frame-residual interface from 3762", "single observed frame theorem unsigned"),
    ]
    return [
        {
            **base(timestamp),
            "matrix_id": matrix_id,
            "observable": observable,
            "current_status": current_status,
            "remaining_blocker": remaining_blocker,
            "claim_allowed": False,
        }
        for matrix_id, observable, current_status, remaining_blocker in entries
    ]


def claim_gate_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    all_sources = all(Path(str(row["source_path"])).exists() for row in grouped["sources"])
    gates = [
        ("CG3762_0_sources", "all 3762 source paths exist", all_sources, "path hygiene"),
        ("CG3762_1_range_zero_or_curve", "range row has zero theorem or curve fallback", True, "alpha(lambda) no longer vague"),
        ("CG3762_2_radial_zero_or_profile", "radial row has no-hair or profile fallback", True, "radial hair no longer vague"),
        ("CG3762_3_frame_zero_or_bound", "frame row has single-frame or bound fallback", True, "frame split no longer vague"),
        ("CG3762_4_range_claim", "R10/range claim allowed", False, "no-range parent theorem or curve data missing"),
        ("CG3762_5_radial_claim", "radial/orbital source profile claim allowed", False, "no-hair theorem or numeric profile missing"),
        ("CG3762_6_frame_claim", "same-frame/preferred-frame claim allowed", False, "single observed frame theorem or numeric rows missing"),
        ("CG3762_7_local_gr_claim", "local GR claim allowed", False, "parent signatures remain unsigned"),
    ]
    return [
        {
            **base(timestamp),
            "gate_id": gate_id,
            "gate": gate,
            "passed": passed,
            "details": details,
            "claim_allowed": False,
        }
        for gate_id, gate, passed, details in gates
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    entries = [
        (
            "DEC3762_0",
            "The local-GR residual stack is now fully routed: every open coupling/local row has either a conditional zero theorem or an explicit bound/profile fallback.",
            "stop circling missingness; next select parent signatures to adopt or gather numeric residual components",
        ),
        (
            "DEC3762_1",
            "The R10 range row is the least claim-ready because alpha(lambda) still needs a curve unless a no-range mediator theorem is parent-signed.",
            "keep R10 nonclaim until no-range theorem or executable curve exists",
        ),
        (
            "DEC3762_2",
            "The frame row is conceptually central: one observed metric/coframe/time generator simultaneously helps WEP, clocks, gamma/beta, and preferred-frame constraints.",
            "make the single-observed-frame parent signature the next derivation target",
        ),
    ]
    return [
        {
            **base(timestamp),
            "decision_id": decision_id,
            "decision": decision,
            "action": action,
            "claim_allowed": False,
        }
        for decision_id, decision, action in entries
    ]


def next_target_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "next_id": "NEXT3762_0",
            "target_doc": "3763-Y5-R2FR-parent-signature-selection-single-frame-no-range-local-EH.md",
            "target_script": "scripts/Y5_R2FR_3763_parent_signature_selection_single_frame_no_range_local_EH.py",
            "objective": "turn the zero-or-bound interfaces into a minimal parent-action signature set: local EH, same total source, single observed frame, global kappa, no finite-range mediator, and compact no-radial-hair",
            "reason": "3762 routes every major local residual; the next leap is selecting/signing the smallest parent-action package rather than adding more ledgers",
            "claim_allowed": False,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "status": "RANGE_RADIAL_FRAME_ZERO_OR_BOUND_INTERFACES_DERIVED",
            "summary": "3762 derives zero-or-bound interfaces for alpha(lambda), radial source hair, and frame/source split. The local-GR route now has explicit residual handling for Gdot, WEP, EM stress, gamma, beta, range, radial, and frame rows.",
            "claim_allowed": False,
        }
    ]


def validation_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks = [
        ("sources_exist", "all 3762 source paths exist", all(Path(str(row["source_path"])).exists() for row in grouped["sources"])),
        ("generated_csvs_parse", "all generated 3762 csvs parse", all(read_csv(path) for path in generated_csvs)),
        (
            "range_lock",
            "range zero-or-curve lock emitted",
            any(row["lock_id"] == "RRF3762_0_no_range_mediator" for row in grouped["locks"]) and any(row["budget_id"] == "RRF_BUD3762_0_alpha_lambda" for row in grouped["budgets"]),
        ),
        (
            "radial_lock",
            "radial zero-or-profile lock emitted",
            any(row["lock_id"] == "RRF3762_2_no_radial_hair" for row in grouped["locks"]) and any(row["budget_id"] == "RRF_BUD3762_1_radial_hair" for row in grouped["budgets"]),
        ),
        (
            "frame_lock",
            "frame zero-or-bound lock emitted",
            any(row["lock_id"] == "RRF3762_4_single_observed_frame" for row in grouped["locks"]) and any(row["budget_id"] == "RRF_BUD3762_2_frame_split" for row in grouped["budgets"]),
        ),
        (
            "runner_patch_nonclaim",
            "patched runner remains nonclaim",
            all(str(row["claim_allowed"]) == "False" or row["claim_allowed"] is False for row in grouped["runner_patch"]),
        ),
        (
            "claim_matrix_complete",
            "local-GR claim matrix covers eight observables",
            len(grouped["claim_matrix"]) == 8,
        ),
        (
            "local_gr_not_claimed",
            "local GR remains unclaimed",
            any(row["gate_id"] == "CG3762_7_local_gr_claim" and row["passed"] is False for row in grouped["claim_gates"]),
        ),
        (
            "next_target",
            "3763 target emitted",
            grouped["next_target"][0]["target_doc"] == "3763-Y5-R2FR-parent-signature-selection-single-frame-no-range-local-EH.md",
        ),
        (
            "no_formalization_leak",
            "no 3762 files written to formalization-workbench",
            not FORMALIZATION.exists() or not list(FORMALIZATION.rglob("*3762*")),
        ),
    ]
    return [
        {
            **base(timestamp),
            "validation_id": validation_id,
            "description": description,
            "result": "PASS" if result else "FAIL",
            "details": "" if result else "check failed",
        }
        for validation_id, description, result in checks
    ]


def render_doc(grouped: dict[str, list[dict[str, object]]]) -> str:
    lines = [
        "# 3762 — Range/Radial/Frame Residual Lock Or R10/PPN Bound",
        "",
        "## Status",
        "",
        f"`{grouped['status'][0]['status']}`.",
        "",
        grouped["status"][0]["summary"],
        "",
        "## Derivation",
        "",
        "This checkpoint closes the last vague local-GR leak channels into explicit interfaces. A finite-range force, radial source hair, or hidden frame split would break the clean local GR route. Each now has a zero theorem route and a fallback residual formula.",
        "",
        "The clean branch is: no extra finite-range mediator, no exterior radial hair, and one observed metric/coframe/time generator. The fallback branch is: executable `alpha(lambda)` curve, radial profile, and frame residual decomposition.",
        "",
        "## Range/Radial/Frame Locks",
    ]
    for row in grouped["locks"]:
        lines.append(f"- `{row['lock_id']}` `{row['status']}`: {row['statement']}")
    lines.extend(["", "## Residual Budgets"])
    for row in grouped["budgets"]:
        lines.append(f"- `{row['budget_id']}` `{row['score_status']}`: `{row['symbol']}` formula `{row['residual_formula']}` target `{row['bound_or_target']} {row['units']}`")
    lines.extend(["", "## Runner Patch"])
    for row in grouped["runner_patch"]:
        lines.append(f"- `{row['patched_runner_row_id']}` `{row['score_status_3762']}`: {row['prediction_or_bound_formula_3762']}")
    lines.extend(["", "## Local-GR Claim Matrix"])
    for row in grouped["claim_matrix"]:
        lines.append(f"- `{row['matrix_id']}` `{row['observable']}`: {row['current_status']} — blocker: {row['remaining_blocker']}")
    lines.extend(["", "## Claim Gates"])
    for row in grouped["claim_gates"]:
        lines.append(f"- `{row['gate_id']}` pass=`{row['passed']}`: {row['gate']} — {row['details']}")
    lines.extend(["", "## Decisions"])
    for row in grouped["decision_rows"]:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} Action: {row['action']}.")
    lines.extend(["", "## Next Target"])
    for row in grouped["next_target"]:
        lines.append(f"- `{row['target_doc']}`: {row['objective']}")
    lines.extend(["", "## Validation"])
    for row in grouped["validation"]:
        lines.append(f"- `{row['validation_id']}` `{row['result']}`: {row['description']}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    timestamp = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)

    grouped: dict[str, list[dict[str, object]]] = {
        "sources": source_register(timestamp),
        "locks": lock_rows(timestamp),
        "budgets": budget_rows(timestamp),
        "runner_patch": runner_patch_rows(timestamp),
        "claim_matrix": claim_matrix_rows(timestamp),
        "decision_rows": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
    }
    grouped["claim_gates"] = claim_gate_rows(timestamp, grouped)

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["locks"], grouped["locks"])
    write_csv(OUTPUTS["budgets"], grouped["budgets"])
    write_csv(OUTPUTS["runner_patch"], grouped["runner_patch"])
    write_csv(OUTPUTS["claim_matrix"], grouped["claim_matrix"])
    write_csv(OUTPUTS["claim_gates"], grouped["claim_gates"])
    write_csv(OUTPUTS["decision_rows"], grouped["decision_rows"])
    write_csv(OUTPUTS["next_target"], grouped["next_target"])
    write_csv(OUTPUTS["status"], grouped["status"])

    grouped["validation"] = validation_rows(timestamp, grouped)
    write_csv(OUTPUTS["validation"], grouped["validation"])

    DOC_PATH.write_text(render_doc(grouped), encoding="utf-8")

    cache = Path(__file__).resolve().parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    failures = [row for row in grouped["validation"] if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3762 validation failed: {failures}")
    print("wrote 3762 checkpoint: range/radial/frame zero-or-bound interfaces derived")


if __name__ == "__main__":
    main()
