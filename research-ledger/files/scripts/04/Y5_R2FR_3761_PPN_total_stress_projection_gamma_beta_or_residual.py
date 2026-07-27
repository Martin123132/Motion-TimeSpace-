import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3761"
BRANCH = "MTS_R2FR_Y5_PPN_TOTAL_STRESS_PROJECTION_GAMMA_BETA_OR_RESIDUAL_3761"
PCW = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work"
)
RESIDUALS = PCW / "source-intake" / "mts_residuals"
FORMALIZATION = PCW.parent / "formalization-workbench"
DOC_PATH = PCW / "3761-Y5-R2FR-PPN-total-stress-projection-gamma-beta-or-residual.md"


OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3761_SOURCE_REGISTER.csv",
    "ppn_theorem": RESIDUALS / "P8_Y5_R2FR_3761_PPN_TOTAL_STRESS_PROJECTION_THEOREM.csv",
    "gamma_beta": RESIDUALS / "P8_Y5_R2FR_3761_GAMMA_BETA_BOUND_EVALUATION.csv",
    "ppn_residual": RESIDUALS / "P8_Y5_R2FR_3761_PPN_RESIDUAL_BUDGET.csv",
    "runner_patch": RESIDUALS / "P8_Y5_R2FR_3761_COUPLING_RUNNER_PATCH.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_3761_CLAIM_GATES.csv",
    "decision_rows": RESIDUALS / "P8_Y5_R2FR_3761_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3761_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3761_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3761_VALIDATION.csv",
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
        "SRC3761_0_3760_doc": PCW / "3760-Y5-R2FR-Maxwell-EM-stress-same-source-current-or-residual.md",
        "SRC3761_1_3760_next": RESIDUALS / "P8_Y5_R2FR_3760_NEXT_TARGET.csv",
        "SRC3761_2_3760_em_theorem": RESIDUALS / "P8_Y5_R2FR_3760_MAXWELL_EM_STRESS_SOURCE_THEOREM.csv",
        "SRC3761_3_3760_em_residual": RESIDUALS / "P8_Y5_R2FR_3760_EM_SOURCE_RESIDUAL_BUDGET.csv",
        "SRC3761_4_3760_ppn_interface": RESIDUALS / "P8_Y5_R2FR_3760_EM_TO_PPN_INTERFACE.csv",
        "SRC3761_5_3760_runner": RESIDUALS / "P8_Y5_R2FR_3760_COUPLING_RUNNER_PATCH.csv",
        "SRC3761_6_3758_kappa_law": RESIDUALS / "P8_Y5_R2FR_3758_KAPPA_QUOTIENT_FLUX_LAW.csv",
        "SRC3761_7_3759_universality": RESIDUALS / "P8_Y5_R2FR_3759_SOURCE_UNIVERSALITY_THEOREM.csv",
        "SRC3761_8_gm_matrix": RESIDUALS / "P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv",
    }


def source_register(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "source_id": source_id,
            "source_path": str(path),
            "source_exists": path.exists(),
            "role": "3761 PPN total-stress projection input",
        }
        for source_id, path in source_paths().items()
    ]


def runner_row(residual_id: str) -> dict[str, str]:
    rows = read_csv(source_paths()["SRC3761_5_3760_runner"])
    return next(row for row in rows if row["residual_id"] == residual_id)


def numeric_bound(residual_id: str) -> float:
    row = runner_row(residual_id)
    value = float(row["bound_value"])
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"invalid bound for {residual_id}: {row['bound_value']}")
    return value


def ppn_theorem_rows(timestamp: str) -> list[dict[str, object]]:
    entries = [
        (
            "PPN3761_0_local_EH_limit",
            "Assume the local parent action reduces to Einstein-Hilbert metric/coframe gravity plus the same total Hilbert source T_total.",
            "This is the central parent action signature; without it gamma/beta cannot be claimed.",
            "REQUIRED_PARENT_ACTION_SIGNATURE",
            False,
        ),
        (
            "PPN3761_1_same_observed_metric",
            "Matter, clocks, light, and EM all read the same observed weak-field metric/coframe g_eff.",
            "Prevents a hidden frame split from faking gamma/beta.",
            "REQUIRED_FRAME_SIGNATURE",
            False,
        ),
        (
            "PPN3761_2_linearized_projection",
            "In harmonic/Newtonian gauge the EH weak-field equation gives a single potential U sourcing both g_00 and g_ij at first PPN order when no unscreened extra scalar/vector/tensor channel is present.",
            "This is the standard GR gamma route.",
            "EXACT_CONDITIONAL_GR_LIMIT_PROJECTION",
            False,
        ),
        (
            "PPN3761_3_gamma_zero",
            "If PPN3761_0-2 hold, gamma-1=0; EM stress contributes through T_total rather than a separate gamma source.",
            "Conditional zero against the Cassini/Shapiro row.",
            "EXACT_CONDITIONAL_ZERO_THEOREM",
            False,
        ),
        (
            "PPN3761_4_beta_zero",
            "If the local second-order field equation is the EH nonlinear self-coupling with the same T_total and no extra nonlinear source residue, beta-1=0.",
            "Conditional zero against the PPN beta row.",
            "EXACT_CONDITIONAL_ZERO_THEOREM",
            False,
        ),
        (
            "PPN3761_5_residual_budget",
            "If any parent signature is unsigned, gamma and beta become absolute residual sums over left-hand operator error, source projection error, frame split, EM residuals, and extra-field/range channels.",
            "This is the no-smuggling fallback.",
            "BOUND_INTERFACE_DERIVED",
            True,
        ),
    ]
    return [
        {
            **base(timestamp),
            "theorem_id": theorem_id,
            "statement": statement,
            "premise_or_note": premise_or_note,
            "status": status,
            "derived_inside_3761": derived,
            "parent_signed": False if not derived else "residual_interface",
            "claim_allowed": False,
        }
        for theorem_id, statement, premise_or_note, status, derived in entries
    ]


def gamma_beta_rows(timestamp: str) -> list[dict[str, object]]:
    gamma_bound = numeric_bound("KRV3755_6_gamma")
    beta_bound = numeric_bound("KRV3755_7_beta")
    return [
        {
            **base(timestamp),
            "evaluation_id": "PGB3761_0_gamma_conditional_zero",
            "observable": "gamma_minus_1",
            "arena": "Cassini/Shapiro",
            "prediction_formula": "gamma - 1 = 0",
            "prediction_value": 0.0,
            "bound_value": gamma_bound,
            "units": "dimensionless",
            "score_status": "CONDITIONAL_NUMERIC_PASS_IF_LOCAL_EH_TOTAL_SOURCE_SIGNED",
            "required_parent_signatures": "PPN3761_0_local_EH_limit;PPN3761_1_same_observed_metric;PPN3761_2_linearized_projection;EMT3760_5_conditional_result",
            "valid_prediction_row": False,
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "evaluation_id": "PGB3761_1_beta_conditional_zero",
            "observable": "beta_minus_1",
            "arena": "PPN beta",
            "prediction_formula": "beta - 1 = 0",
            "prediction_value": 0.0,
            "bound_value": beta_bound,
            "units": "dimensionless",
            "score_status": "CONDITIONAL_NUMERIC_PASS_IF_SECOND_ORDER_EH_TOTAL_SOURCE_SIGNED",
            "required_parent_signatures": "PPN3761_0_local_EH_limit;PPN3761_1_same_observed_metric;PPN3761_4_beta_zero",
            "valid_prediction_row": False,
            "claim_allowed": False,
        },
    ]


def ppn_residual_rows(timestamp: str) -> list[dict[str, object]]:
    gamma_bound = numeric_bound("KRV3755_6_gamma")
    beta_bound = numeric_bound("KRV3755_7_beta")
    entries = [
        (
            "PPR3761_0_gamma_budget",
            "gamma_minus_1",
            "Cassini/Shapiro",
            "|Delta_EH_linear| + |Delta_source_projection| + |Delta_frame_light_matter| + |delta_gamma_EM| + |delta_gamma_extra_field|",
            gamma_bound,
            "dimensionless",
        ),
        (
            "PPR3761_1_beta_budget",
            "beta_minus_1",
            "PPN beta",
            "|Delta_EH_second_order| + |Delta_source_nonlinear| + |Delta_frame_second_order| + |delta_beta_EM| + |delta_beta_extra_field|",
            beta_bound,
            "dimensionless",
        ),
        (
            "PPR3761_2_range_hair_coupling",
            "delta_gamma_beta_range",
            "PPN/R10/range",
            "|alpha(lambda)_local| + |partial_r ln mu_obs| + |preferred_frame_residual|",
            "zero_or_bound_by_R10_and_PPN",
            "mixed",
        ),
    ]
    return [
        {
            **base(timestamp),
            "residual_id": residual_id,
            "symbol": symbol,
            "arena": arena,
            "residual_formula": formula,
            "bound_value": bound_value,
            "units": units,
            "prediction_value": "MISSING_NUMERIC_PPN_COMPONENTS",
            "score_status": "BOUND_FORMULA_READY_NUMERIC_COMPONENTS_MISSING",
            "valid_prediction_row": False,
            "claim_allowed": False,
        }
        for residual_id, symbol, arena, formula, bound_value, units in entries
    ]


def runner_patch_rows(timestamp: str) -> list[dict[str, object]]:
    rows = []
    for source_row in read_csv(source_paths()["SRC3761_5_3760_runner"]):
        patched = {
            **base(timestamp),
            "patched_runner_row_id": f"RUN3761_{source_row['residual_id']}",
            "source_runner_row": source_row["patched_runner_row_id"],
            "residual_id": source_row["residual_id"],
            "symbol": source_row["symbol"],
            "arena": source_row["arena"],
            "bound_value": source_row["bound_value"],
            "units": source_row["units"],
            "prediction_status_3760": source_row["prediction_status_3760"],
            "score_status_3760": source_row["score_status_3760"],
            "prediction_status_3761": source_row["prediction_status_3760"],
            "score_status_3761": source_row["score_status_3760"],
            "prediction_or_bound_formula_3761": source_row["prediction_or_bound_formula_3760"],
            "conditional_score_ready": source_row["conditional_score_ready"],
            "valid_prediction_row": False,
            "claim_allowed": False,
            "notes": "unchanged from 3760",
        }
        if source_row["residual_id"] == "KRV3755_6_gamma":
            patched.update(
                {
                    "prediction_status_3761": "CONDITIONAL_ZERO_OR_PPN_GAMMA_RESIDUAL_BUDGET",
                    "score_status_3761": "CONDITIONAL_PASS_UNSIGNED_LOCAL_EH_TOTAL_SOURCE_PREMISES",
                    "prediction_or_bound_formula_3761": "gamma-1=0 if local EH + same observed metric + same total source are parent-signed; otherwise |Delta_EH_linear|+|Delta_source_projection|+|Delta_frame|+|delta_gamma_EM|+|delta_gamma_extra_field| <= 2.3e-05",
                    "conditional_score_ready": True,
                    "notes": "gamma row is now conditionally scoreable, but nonclaim until local EH/source/frame signatures are signed",
                }
            )
        if source_row["residual_id"] == "KRV3755_7_beta":
            patched.update(
                {
                    "prediction_status_3761": "CONDITIONAL_ZERO_OR_PPN_BETA_RESIDUAL_BUDGET",
                    "score_status_3761": "CONDITIONAL_PASS_UNSIGNED_SECOND_ORDER_EH_TOTAL_SOURCE_PREMISES",
                    "prediction_or_bound_formula_3761": "beta-1=0 if second-order EH self-coupling + same total source are parent-signed; otherwise |Delta_EH_second_order|+|Delta_source_nonlinear|+|Delta_frame2|+|delta_beta_EM|+|delta_beta_extra_field| <= 7.8e-05",
                    "conditional_score_ready": True,
                    "notes": "beta row is now conditionally scoreable, but nonclaim until second-order local EH/source signatures are signed",
                }
            )
        rows.append(patched)
    return rows


def claim_gate_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    all_sources = all(Path(str(row["source_path"])).exists() for row in grouped["sources"])
    gates = [
        ("CG3761_0_sources", "all 3761 source paths exist", all_sources, "path hygiene"),
        ("CG3761_1_gamma_conditional", "gamma conditional zero row emitted", True, "conditional numeric pass exists"),
        ("CG3761_2_beta_conditional", "beta conditional zero row emitted", True, "conditional numeric pass exists"),
        ("CG3761_3_local_EH_parent_signed", "local EH metric/coframe limit parent-signed", False, "parent action signature still open"),
        ("CG3761_4_same_metric_parent_signed", "same observed metric/frame parent-signed", False, "frame split still open"),
        ("CG3761_5_numeric_ppn_residuals", "numeric PPN residual components filled", False, "component values missing"),
        ("CG3761_6_gamma_beta_claim", "gamma/beta claim allowed", False, "conditional zero or residual budget not fully sourced"),
        ("CG3761_7_local_gr_claim", "local GR claim allowed", False, "R10/range/frame/source signatures remain open"),
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
            "DEC3761_0",
            "The PPN gamma/beta rows are now in the same disciplined form as Gdot and WEP: zero in the local EH/same-source limit, otherwise explicit residual budgets.",
            "do not claim PPN yet; use it as the next parent-action signature gate",
        ),
        (
            "DEC3761_1",
            "EM stress is no longer a floating exception: it either belongs to T_total in the PPN source projection or appears as delta_gamma_EM/delta_beta_EM.",
            "carry EM residual rows forward into future PPN/R10 scoring",
        ),
        (
            "DEC3761_2",
            "The remaining local-GR blockers are now mostly extra-channel/range/frame locks rather than undefined coupling language.",
            "next attack R10/range/radial/preferred-frame residuals",
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
            "next_id": "NEXT3761_0",
            "target_doc": "3762-Y5-R2FR-range-radial-frame-residual-lock-or-R10-PPN-bound.md",
            "target_script": "scripts/Y5_R2FR_3762_range_radial_frame_residual_lock_or_R10_PPN_bound.py",
            "objective": "derive zero locks or bound formulas for alpha(lambda), radial source hair, and frame residual rows after the Gdot/WEP/EM/PPN conditional route",
            "reason": "3761 conditionally scores gamma/beta; remaining local-GR blockers are finite-range/radial/preferred-frame residual channels",
            "claim_allowed": False,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "status": "PPN_GAMMA_BETA_ZERO_OR_RESIDUAL_BUDGET_DERIVED",
            "summary": "3761 derives conditional gamma-1=0 and beta-1=0 in the local EH/same-total-source limit and emits gamma/beta residual budgets if the parent signatures are not signed.",
            "claim_allowed": False,
        }
    ]


def validation_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks = [
        ("sources_exist", "all 3761 source paths exist", all(Path(str(row["source_path"])).exists() for row in grouped["sources"])),
        ("generated_csvs_parse", "all generated 3761 csvs parse", all(read_csv(path) for path in generated_csvs)),
        (
            "gamma_zero",
            "gamma conditional zero emitted",
            any(row["evaluation_id"] == "PGB3761_0_gamma_conditional_zero" and str(row["prediction_value"]) in {"0", "0.0"} for row in grouped["gamma_beta"]),
        ),
        (
            "beta_zero",
            "beta conditional zero emitted",
            any(row["evaluation_id"] == "PGB3761_1_beta_conditional_zero" and str(row["prediction_value"]) in {"0", "0.0"} for row in grouped["gamma_beta"]),
        ),
        (
            "gamma_bound",
            "gamma bound uses 2.3e-05",
            any(str(row["bound_value"]) == "2.3e-05" for row in grouped["gamma_beta"]),
        ),
        (
            "beta_bound",
            "beta bound uses 7.8e-05",
            any(str(row["bound_value"]) == "7.8e-05" for row in grouped["gamma_beta"]),
        ),
        (
            "ppn_residuals",
            "PPN residual budgets emitted",
            any(row["residual_id"] == "PPR3761_0_gamma_budget" for row in grouped["ppn_residual"]) and any(row["residual_id"] == "PPR3761_1_beta_budget" for row in grouped["ppn_residual"]),
        ),
        (
            "runner_patch_nonclaim",
            "patched runner remains nonclaim",
            all(str(row["claim_allowed"]) == "False" or row["claim_allowed"] is False for row in grouped["runner_patch"]),
        ),
        (
            "gamma_beta_claim_blocked",
            "gamma/beta claim remains false",
            any(row["gate_id"] == "CG3761_6_gamma_beta_claim" and row["passed"] is False for row in grouped["claim_gates"]),
        ),
        (
            "next_target",
            "3762 target emitted",
            grouped["next_target"][0]["target_doc"] == "3762-Y5-R2FR-range-radial-frame-residual-lock-or-R10-PPN-bound.md",
        ),
        (
            "no_formalization_leak",
            "no 3761 files written to formalization-workbench",
            not FORMALIZATION.exists() or not list(FORMALIZATION.rglob("*3761*")),
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
        "# 3761 — PPN Total-Stress Projection Gamma/Beta Or Residual",
        "",
        "## Status",
        "",
        f"`{grouped['status'][0]['status']}`.",
        "",
        grouped["status"][0]["summary"],
        "",
        "## Derivation",
        "",
        "This checkpoint turns the PPN rows into the same zero-or-bound structure as Gdot and WEP. If the local parent action reduces to metric/coframe Einstein-Hilbert gravity, all sectors read the same observed metric, and the source is the same total Hilbert stress, the GR weak-field projection gives `gamma-1=0` and the EH second-order self-coupling gives `beta-1=0`.",
        "",
        "If any clause is unsigned, the row does not die; it becomes an explicit residual budget. EM stress enters through `T_total` when same-source, or through `delta_gamma_EM`/`delta_beta_EM` when not.",
        "",
        "## PPN Projection Clauses",
    ]
    for row in grouped["ppn_theorem"]:
        lines.append(f"- `{row['theorem_id']}` `{row['status']}`: {row['statement']}")
    lines.extend(["", "## Gamma/Beta Bound Evaluation"])
    for row in grouped["gamma_beta"]:
        lines.append(
            f"- `{row['evaluation_id']}` `{row['score_status']}`: `{row['prediction_formula']}` versus `{row['bound_value']} {row['units']}` claim=`{row['claim_allowed']}`"
        )
    lines.extend(["", "## PPN Residual Budgets"])
    for row in grouped["ppn_residual"]:
        lines.append(
            f"- `{row['residual_id']}` `{row['score_status']}`: `{row['symbol']}` formula `{row['residual_formula']}` bound `{row['bound_value']} {row['units']}`"
        )
    lines.extend(["", "## Runner Patch"])
    for row in grouped["runner_patch"]:
        lines.append(f"- `{row['patched_runner_row_id']}` `{row['score_status_3761']}`: {row['prediction_or_bound_formula_3761']}")
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
        "ppn_theorem": ppn_theorem_rows(timestamp),
        "gamma_beta": gamma_beta_rows(timestamp),
        "ppn_residual": ppn_residual_rows(timestamp),
        "runner_patch": runner_patch_rows(timestamp),
        "decision_rows": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
    }
    grouped["claim_gates"] = claim_gate_rows(timestamp, grouped)

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["ppn_theorem"], grouped["ppn_theorem"])
    write_csv(OUTPUTS["gamma_beta"], grouped["gamma_beta"])
    write_csv(OUTPUTS["ppn_residual"], grouped["ppn_residual"])
    write_csv(OUTPUTS["runner_patch"], grouped["runner_patch"])
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
        raise SystemExit(f"3761 validation failed: {failures}")
    print("wrote 3761 checkpoint: PPN gamma/beta zero or residual budget derived")


if __name__ == "__main__":
    main()
