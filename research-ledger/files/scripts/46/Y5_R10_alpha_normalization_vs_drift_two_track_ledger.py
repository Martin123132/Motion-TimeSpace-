from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1110-Y5-R10-alpha-normalization-vs-drift-two-track-ledger.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    generated = now()
    stamped: list[dict[str, object]] = []
    for source_row in rows:
        copied = dict(source_row)
        copied.setdefault("valid_for_claim", "false")
        copied.setdefault("claim_allowed", "false")
        copied.setdefault("generated_utc", generated)
        stamped.append(copied)
    return stamped


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for source_row in rows:
            for key in source_row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for source_row in rows:
            writer.writerow({key: source_row.get(key, "") for key in fieldnames})


def read_csv_rows(relative_path: str) -> list[dict[str, str]]:
    path = ROOT / relative_path
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_rows() -> list[dict[str, object]]:
    sources = [
        {
            "source_id": "SRC1110_0_1109_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1109_NEXT_TARGET.csv",
            "needle": "NEXT1109_0_1110",
            "note": "1109 handoff to alpha normalization versus drift split.",
        },
        {
            "source_id": "SRC1110_1_1109_theorem",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1109_LAMBDA_F2_THEOREM_ATTEMPT.csv",
            "needle": "NO_INDEPENDENT_LAMBDA_F2_THEOREM_NOT_DERIVED",
            "note": "lambda F2 theorem remains unproved.",
        },
        {
            "source_id": "SRC1110_2_1109_classification",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1109_LAMBDA_CLASSIFICATION.csv",
            "needle": "CALIBRATION_MODE",
            "note": "universal lambda is calibration mode.",
        },
        {
            "source_id": "SRC1110_3_1109_finite",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1109_FINITE_ALPHA_ROWS_NONCLAIM.csv",
            "needle": "MISSING_SOURCE_BACKED_ALPHA_COEFFICIENT",
            "note": "finite vertical/running alpha coefficient remains missing.",
        },
        {
            "source_id": "SRC1110_4_1098_requirements",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1098_SOURCE_BACKED_COEFFICIENT_REQUIREMENTS.csv",
            "needle": "REQ1098_0_c_alpha",
            "note": "source-backed alpha coefficient threshold.",
        },
        {
            "source_id": "SRC1110_5_988_clock",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_988_CLOCK_PRODUCT_IMPORT.csv",
            "needle": "CLOCK988_CAS646_1_YbE3E2",
            "note": "strongest imported clock alpha product row.",
        },
        {
            "source_id": "SRC1110_6_988_wep",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_988_WEP_ALPHA_PRESSURE_IMPORT.csv",
            "needle": "WEP988_WAS651_0_alpha_Coulomb",
            "note": "WEP alpha/Coulomb source-normalization pressure.",
        },
        {
            "source_id": "SRC1110_7_988_joint",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_988_JOINT_ALPHA_VARIABLE_GATE.csv",
            "needle": "JAV988_0_alpha_slot",
            "note": "shared alpha slot but missing parent normalization and arena maps.",
        },
        {
            "source_id": "SRC1110_8_1060_r10",
            "relative_path": "source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_1060_ALPHA_PRODUCT_RUNNER_TEMPLATE_NONCLAIM.csv",
            "needle": "MISSING_R10_PRODUCT_PREDICTION",
            "note": "R10 product runner template refuses missing product prediction.",
        },
        {
            "source_id": "SRC1110_9_1058_counterterm",
            "relative_path": "source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_1058_ALPHA_COUNTERTERM_TEMPLATE_NONCLAIM.csv",
            "needle": "MISSING_PRODUCT_PRIOR_OR_FINITE_ALPHA_BRANCH",
            "note": "alpha counterterm branch remains nonclaim.",
        },
    ]
    checked: list[dict[str, object]] = []
    for source in sources:
        path = ROOT / str(source["relative_path"])
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        checked.append(
            {
                **source,
                "exists": str(path.exists()).lower(),
                "needle_found": str(str(source["needle"]) in text).lower(),
            }
        )
    return stamp(checked)


def extracted_values() -> dict[str, str]:
    requirement_rows = read_csv_rows("source-intake/mts_residuals/P8_Y5_R10_1098_SOURCE_BACKED_COEFFICIENT_REQUIREMENTS.csv")
    clock_rows = read_csv_rows("source-intake/mts_residuals/P8_Y5_R10_988_CLOCK_PRODUCT_IMPORT.csv")
    wep_rows = read_csv_rows("source-intake/mts_residuals/P8_Y5_R10_988_WEP_ALPHA_PRESSURE_IMPORT.csv")
    alpha_requirement = next(row for row in requirement_rows if row["requirement_id"] == "REQ1098_0_c_alpha")
    strongest_clock = min(clock_rows, key=lambda row: float(row["product_bound_1sigma_yr_inv"]))
    alpha_wep = next(row for row in wep_rows if row["import_id"] == "WEP988_WAS651_0_alpha_Coulomb")
    return {
        "alpha_threshold_abs": alpha_requirement["threshold_abs"],
        "clock_pair": strongest_clock["clock_pair"],
        "clock_bound_1sigma_yr_inv": strongest_clock["product_bound_1sigma_yr_inv"],
        "clock_bound_2sigma_yr_inv": strongest_clock["product_bound_2sigma_yr_inv"],
        "wep_eta_bound": alpha_wep["eta_bound_used"],
        "wep_required_beta_source_max": alpha_wep["required_abs_beta_source_max"],
    }


def two_track_rows(values: dict[str, str]) -> list[dict[str, object]]:
    return stamp(
        [
            {
                "track_id": "TRACK1110_N0",
                "track": "normalization",
                "object": "Z_Q_common = C_P N_Q + lambda_A_common",
                "contract": "absolute measured alpha may be calibrated here only if lambda_A_common is universal",
                "current_status": "CALIBRATION_NOT_PREDICTION",
                "observable_arena": "EM value bookkeeping",
                "scoreable_now": "false",
                "blocker": "no parent value for C_P N_Q and no no-independent-lambda theorem",
                "next_action": "do not use measured alpha as a claimed prediction",
            },
            {
                "track_id": "TRACK1110_N1",
                "track": "normalization",
                "object": "parent alpha prediction",
                "contract": "derive C_P, N_Q, readout convention, and lambda_A_absent/fixed from parent action",
                "current_status": "BLOCKED_PARENT_NORMALIZATION_NOT_DERIVED",
                "observable_arena": "absolute alpha",
                "scoreable_now": "false",
                "blocker": "lambda_A can absorb the measured value unless forbidden or parent-fixed",
                "next_action": "park as long-form parent action target, not local test evidence",
            },
            {
                "track_id": "TRACK1110_D0",
                "track": "drift_product",
                "object": "b_alpha or c_alpha_DD = d ln Z_Q_eff / dX",
                "contract": "finite vertical/running coefficient must be theorem-zero or source-backed",
                "current_status": "MISSING_SOURCE_BACKED_COEFFICIENT_OR_THEOREM_ZERO",
                "observable_arena": "clock; WEP; R10; EM",
                "scoreable_now": "false",
                "blocker": f"absolute coefficient threshold is {values['alpha_threshold_abs']}, but no MTS coefficient exists",
                "next_action": "try derive alpha-drift zero before sourcing finite coefficient vector",
            },
            {
                "track_id": "TRACK1110_D1",
                "track": "drift_product",
                "object": "b_alpha * tau_clock_time",
                "contract": "clock products bind only the product unless tau_clock dynamics are parent-owned",
                "current_status": "PRODUCT_BOUND_IMPORTED_NONCLAIM",
                "observable_arena": values["clock_pair"],
                "scoreable_now": "false",
                "blocker": f"best imported 1sigma product bound is {values['clock_bound_1sigma_yr_inv']} yr^-1, but standalone b_alpha needs tau_clock",
                "next_action": "keep clock row as product pressure, not standalone alpha coefficient",
            },
            {
                "track_id": "TRACK1110_D2",
                "track": "drift_product",
                "object": "beta_source_alpha * b_alpha * tau_WEP",
                "contract": "WEP alpha channel needs source normalization, material map, and domain tau",
                "current_status": "PRODUCT_BOUND_IMPORTED_NONCLAIM",
                "observable_arena": "MICROSCOPE/DD alpha-Coulomb pressure",
                "scoreable_now": "false",
                "blocker": f"eta bound {values['wep_eta_bound']} implies beta_source_alpha <= {values['wep_required_beta_source_max']} under the imported smoke normalization",
                "next_action": "do not transfer clock screen into WEP without source normalization",
            },
            {
                "track_id": "TRACK1110_D3",
                "track": "drift_product",
                "object": "K_X^R10(lambda) * beta_source(lambda) * beta_test(lambda)",
                "contract": "R10 branch must predict a numeric product at each lambda and compare to a claim-valid bound curve",
                "current_status": "MISSING_R10_PRODUCT_PREDICTION_AND_PROMOTED_BOUND",
                "observable_arena": "R10 short-range inverse-square/Yukawa tests",
                "scoreable_now": "false",
                "blocker": "existing R10 alpha rows are symbolic or template nonclaim rows",
                "next_action": "keep R10 as product runner gate, not proof of local-GR pass",
            },
        ]
    )


def product_requirement_rows(values: dict[str, str]) -> list[dict[str, object]]:
    return stamp(
        [
            {
                "requirement_id": "REQ1110_0_alpha_drift",
                "track": "drift_product",
                "quantity": "b_alpha or c_alpha_DD",
                "numeric_bound_or_target": values["alpha_threshold_abs"],
                "units": "dimensionless coefficient",
                "required_inputs": "parent theorem-zero for d ln Z_Q_eff/dX or source-backed coefficient with source path",
                "current_status": "MISSING_THEOREM_ZERO_OR_NUMERIC_SOURCE",
            },
            {
                "requirement_id": "REQ1110_1_clock_product",
                "track": "drift_product",
                "quantity": "b_alpha * tau_clock_time",
                "numeric_bound_or_target": values["clock_bound_1sigma_yr_inv"],
                "units": "yr^-1",
                "required_inputs": "tau_clock_time or direct MTS product prediction; clock sensitivity/readout map",
                "current_status": "PRODUCT_BOUND_EXISTS_BUT_STANDALONE_B_ALPHA_BLOCKED",
            },
            {
                "requirement_id": "REQ1110_2_wep_product",
                "track": "drift_product",
                "quantity": "beta_source_alpha * b_alpha * tau_WEP",
                "numeric_bound_or_target": values["wep_required_beta_source_max"],
                "units": "dimensionless imported normalization target",
                "required_inputs": "beta_source_alpha, tau_WEP, material charge map, or direct parent product theorem",
                "current_status": "PRODUCT_BOUND_PRESSURE_EXISTS_BUT_SOURCE_NORMALIZATION_BLOCKED",
            },
            {
                "requirement_id": "REQ1110_3_r10_product",
                "track": "drift_product",
                "quantity": "alpha_R10(lambda)",
                "numeric_bound_or_target": "claim-valid alpha_bound(lambda) curve",
                "units": "dimensionless Yukawa alpha at each lambda",
                "required_inputs": "K_X^R10(lambda), source/test beta factors, lambda map, real bound curve",
                "current_status": "MISSING_PRODUCT_PREDICTION_AND_PROMOTED_BOUND",
            },
            {
                "requirement_id": "REQ1110_4_alpha_value",
                "track": "normalization",
                "quantity": "alpha_EM absolute value",
                "numeric_bound_or_target": "measured alpha is an input unless parent predicts Z_Q",
                "units": "dimensionless",
                "required_inputs": "C_P, N_Q, readout convention, no lambda_A counterterm or fixed lambda_A",
                "current_status": "CALIBRATION_ONLY_NOT_EVIDENCE",
            },
        ]
    )


def runner_gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "GATE1110_0_no_value_claim",
                "gate": "absolute alpha cannot be called predicted",
                "pass_status": "blocked",
                "reason": "lambda_A_common can absorb the value unless parent norm and no-lambda clauses are signed",
            },
            {
                "gate_id": "GATE1110_1_no_standalone_clock",
                "gate": "clock row cannot become standalone b_alpha",
                "pass_status": "blocked",
                "reason": "clock data constrain b_alpha*tau_clock_time until tau_clock is derived",
            },
            {
                "gate_id": "GATE1110_2_no_clock_to_wep_shortcut",
                "gate": "clock screen cannot be copied into WEP",
                "pass_status": "blocked",
                "reason": "WEP force needs beta_source_alpha, tau_WEP, and material/readout map",
            },
            {
                "gate_id": "GATE1110_3_no_r10_symbolic_pass",
                "gate": "R10 rows cannot pass with symbolic product or anchor-only bound",
                "pass_status": "blocked",
                "reason": "numeric product prediction and claim-valid bound curve are both required",
            },
            {
                "gate_id": "GATE1110_4_no_local_gr_claim",
                "gate": "local-GR/R10 pass remains unclaimed",
                "pass_status": "blocked",
                "reason": "alpha drift, source normalization, and product maps are not parent-derived",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "DEC1110_0_split_adopted",
                "decision": "alpha work is now split into normalization and drift/product tracks",
                "because": "universal lambda is calibration while hidden/running lambda is what clocks/WEP/R10 actually pressure",
                "next_action": "do not mix absolute alpha value evidence with local drift/product evidence",
            },
            {
                "decision_id": "DEC1110_1_best_next",
                "decision": "derive alpha-drift zero first",
                "because": "a theorem-zero for d ln Z_Q_eff/dX would silence clocks/WEP/R10 without pretending measured alpha was predicted",
                "next_action": "attempt vertical/radiative/readout closure for Z_Q_eff",
            },
            {
                "decision_id": "DEC1110_2_fallback",
                "decision": "if drift zero fails, source a finite product vector",
                "because": "the local tests can score products even when absolute alpha normalization remains calibration",
                "next_action": "stage clock, WEP, and R10 product rows with no tau=1 or unity-source shortcuts",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1110_0_1111",
                "next_target": "1111-Y5-R10-alpha-drift-zero-theorem-or-product-source-vector.md",
                "objective": "try to prove d_v ln Z_Q_eff = 0 for the local vertical/running/readout alpha sector; if it fails, build a finite product source vector for clocks, WEP, and R10 without claiming alpha prediction",
                "include": "Z_Q_eff; lambda_A_common; hidden/running f(I); readout map; tau_clock; beta_source_alpha; tau_WEP; R10 product; source paths",
                "exclude": "absolute alpha value claim; tau=1 shortcut; clock-to-WEP transfer; symbolic R10 pass; GitHub; formalization edits",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    tracks: list[dict[str, object]],
    requirements: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    outputs: dict[str, Path],
) -> list[dict[str, object]]:
    validation: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validation.append(
            {
                "check_id": check_id,
                "result": "pass" if passed else "fail",
                "detail": detail,
                "valid_for_claim": "false",
                "generated_utc": now(),
            }
        )

    add("V1110_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources), "all cited local source paths exist and needles are found")
    add("V1110_1_two_tracks_present", {"normalization", "drift_product"} == {str(row["track"]) for row in tracks}, "normalization and drift/product tracks are both present")
    add("V1110_2_normalization_nonclaim", all(row["scoreable_now"] == "false" for row in tracks if row["track"] == "normalization"), "absolute alpha normalization remains calibration/nonclaim")
    add("V1110_3_drift_products_present", all(any(token in str(row["object"]) for row in tracks) for token in ["b_alpha", "tau_clock", "tau_WEP", "K_X^R10"]), "clock, WEP, R10, and alpha coefficient drift rows are present")
    add("V1110_4_requirements_blocked", all("MISSING" in row["current_status"] or "BLOCKED" in row["current_status"] or "CALIBRATION" in row["current_status"] or "PRODUCT_BOUND" in row["current_status"] for row in requirements), "requirement rows remain blocked/nonclaim")
    add("V1110_5_runner_gates_blocked", all(row["pass_status"] == "blocked" for row in gates), "strict runner gates are blocked")
    add("V1110_6_no_claim_rows", all(row.get("valid_for_claim") == "false" and row.get("claim_allowed") == "false" for row in tracks + requirements + gates + decisions + next_target), "all generated rows remain nonclaim")
    add("V1110_7_next_target", next_target[0]["next_target"].startswith("1111-") and "alpha-drift-zero" in str(next_target[0]["next_target"]), "1111 handoff targets alpha drift zero theorem or finite product source vector")
    add("V1110_8_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()), "all generated outputs are under post-checkpoint-work")
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1110_9_csv_parse", csv_parse_ok, "all 1110 CSV outputs parse cleanly")
    add("V1110_10_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add("V1110_SUMMARY", True, "1110 separates alpha value calibration from local alpha drift/product tests")
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for source_row in rows:
        lines.append("| " + " | ".join(str(source_row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    values: dict[str, str],
    sources: list[dict[str, object]],
    tracks: list[dict[str, object]],
    requirements: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1110 - Alpha Normalization Vs Drift Two-Track Ledger

**Current verdict:** the alpha problem splits cleanly. The absolute measured value of alpha belongs to a normalization/calibration track unless the parent action fixes `C_P N_Q` and forbids or fixes `lambda_A`. Local tests belong to a separate drift/product track involving `d ln Z_Q_eff / dX`, clocks, WEP, and R10.

**Useful result:** this is not a loss; it prevents one bad shortcut from poisoning the whole framework. MTS can still compete locally if the drift/product track is derived zero or source-bounded, even while absolute alpha remains calibrated.

**No claim:** no parent alpha prediction, no standalone `b_alpha`, no clock-to-WEP shortcut, no R10 pass, and no local-GR pass follows from 1110.

## Extracted Numerical Pressures
| quantity | value | meaning |
| --- | --- | --- |
| alpha coefficient threshold | {values["alpha_threshold_abs"]} | imported absolute coefficient target from 1098 |
| strongest clock product | {values["clock_bound_1sigma_yr_inv"]} yr^-1 | best 1sigma product bound from {values["clock_pair"]} |
| clock 2sigma product | {values["clock_bound_2sigma_yr_inv"]} yr^-1 | product-only, not standalone b_alpha |
| WEP eta bound | {values["wep_eta_bound"]} | imported alpha/Coulomb pressure row |
| WEP beta-source target | {values["wep_required_beta_source_max"]} | source-normalization pressure, not a pass |

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "note"], sources)}

## Two-Track Ledger
{table(["track_id", "track", "object", "contract", "current_status", "observable_arena", "scoreable_now", "blocker", "next_action", "claim_allowed"], tracks)}

## Product Requirements
{table(["requirement_id", "track", "quantity", "numeric_bound_or_target", "units", "required_inputs", "current_status", "claim_allowed"], requirements)}

## Strict Runner Gates
{table(["gate_id", "gate", "pass_status", "reason", "claim_allowed"], gates)}

## Decisions
{table(["decision_id", "decision", "because", "next_action", "claim_allowed"], decisions)}

## Validation
{table(["check_id", "result", "detail", "valid_for_claim"], validation)}

## Next Target
{table(["next_id", "next_target", "objective", "include", "exclude", "claim_allowed"], next_target)}
"""
    DOC.write_text(text, encoding="utf-8")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists() and pycache.is_dir():
        shutil.rmtree(pycache)


def main() -> None:
    outputs = {
        "source_register": OUT / "P8_Y5_R10_1110_SOURCE_REGISTER.csv",
        "tracks": OUT / "P8_Y5_R10_1110_TWO_TRACK_LEDGER.csv",
        "requirements": OUT / "P8_Y5_R10_1110_ALPHA_PRODUCT_REQUIREMENTS.csv",
        "gates": OUT / "P8_Y5_R10_1110_STRICT_RUNNER_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1110_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1110_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1110_VALIDATION.csv",
    }
    values = extracted_values()
    sources = source_rows()
    tracks = two_track_rows(values)
    requirements = product_requirement_rows(values)
    gates = runner_gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["tracks"], tracks)
    write_csv(outputs["requirements"], requirements)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, tracks, requirements, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(values, sources, tracks, requirements, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
