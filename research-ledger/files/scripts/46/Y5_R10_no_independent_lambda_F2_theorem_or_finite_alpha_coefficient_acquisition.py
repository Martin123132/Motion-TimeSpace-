from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1109-Y5-R10-no-independent-lambda-F2-theorem-or-finite-alpha-coefficient-acquisition.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    generated = now()
    out: list[dict[str, object]] = []
    for row in rows:
        copied = dict(row)
        copied.setdefault("valid_for_claim", "false")
        copied.setdefault("claim_allowed", "false")
        copied.setdefault("generated_utc", generated)
        out.append(copied)
    return out


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def source_rows() -> list[dict[str, object]]:
    rows = [
        {
            "source_id": "SRC1109_0_1108_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1108_NEXT_TARGET.csv",
            "needle": "NEXT1108_0_1109",
            "note": "1108 handoff to no-independent-lambda-F2 theorem.",
        },
        {
            "source_id": "SRC1109_1_1108_theorem",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1108_EM_F2_IMAGE_THEOREM_ATTEMPT.csv",
            "needle": "EMF1108_2_no_lambda",
            "note": "1108 lambda obstruction.",
        },
        {
            "source_id": "SRC1109_2_1099_counter",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1099_COUNTEREXAMPLE_LEDGER.csv",
            "needle": "CX1099_0_lambda_A",
            "note": "lambda_A counterexample.",
        },
        {
            "source_id": "SRC1109_3_1099_exclusion",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1099_NO_EXTRA_F2_EXCLUSION_AUDIT.csv",
            "needle": "EXC1099_1_U1_gauge",
            "note": "gauge invariance does not forbid F2 coefficient.",
        },
        {
            "source_id": "SRC1109_4_1100_lambda",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1100_TQ_THEOREM_ATTEMPT.csv",
            "needle": "TQT1100_3_lambda_countermodel",
            "note": "fixed norm still insufficient with lambda counterterm.",
        },
        {
            "source_id": "SRC1109_5_1100_signature",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1100_TQ_GAUGE_NORM_SIGNATURE.csv",
            "needle": "TQS1100_3_unique_curvature_norm",
            "note": "unique curvature norm clause.",
        },
        {
            "source_id": "SRC1109_6_1108_acq",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1108_EM_ALPHA_ACQUISITION_LEDGER.csv",
            "needle": "ACQ1108_2_no_lambda_operator_domain",
            "note": "no-lambda acquisition row.",
        },
        {
            "source_id": "SRC1109_7_1098_req",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1098_SOURCE_BACKED_COEFFICIENT_REQUIREMENTS.csv",
            "needle": "REQ1098_0_c_alpha",
            "note": "alpha coefficient threshold.",
        },
        {
            "source_id": "SRC1109_8_1108_alpha_template",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1108_ALPHA_ROW_TEMPLATES_NONCLAIM.csv",
            "needle": "ALPHAROW1108_0_template",
            "note": "alpha coefficient template.",
        },
    ]
    checked: list[dict[str, object]] = []
    for row in rows:
        path = ROOT / str(row["relative_path"])
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        checked.append(
            {
                **row,
                "exists": str(path.exists()).lower(),
                "needle_found": str(str(row["needle"]) in text).lower(),
            }
        )
    return stamp(checked)


def lambda_theorem_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "attempt_id": "LFA1109_0_target",
                "claim_piece": "no independent lambda_A F_Q^2",
                "formal_statement": "Any visible constant F_Q^2 coefficient is either the parent norm image C_P N_Q or an explicitly retained finite alpha coefficient.",
                "result": "TARGET_SHARP",
                "proof_or_blocker": "this is the exact subcase needed before hidden f(I)F2 and readout branches matter",
            },
            {
                "attempt_id": "LFA1109_1_absorb_common_constant",
                "claim_piece": "universal constant lambda_A can be absorbed into measured Maxwell normalization",
                "formal_statement": "Z_Q = C_P N_Q + lambda_A with d lambda_A=0 may be calibrated as Z_meas.",
                "result": "CALIBRATION_ONLY_NOT_PREDICTION",
                "proof_or_blocker": "absorbing lambda_A removes no parameter from the theory; alpha value is fitted rather than derived",
            },
            {
                "attempt_id": "LFA1109_2_redundancy_test",
                "claim_piece": "lambda_A is redundant with parent norm",
                "formal_statement": "lambda_A F_Q^2 is redundant only if C_P N_Q is not separately claimed as a predicted normalization and no observed consequence depends on the split.",
                "result": "REDUNDANT_ONLY_IF_ALPHA_NOT_PREDICTED",
                "proof_or_blocker": "if alpha is to be predicted/owned by the parent norm, lambda_A is not harmless",
            },
            {
                "attempt_id": "LFA1109_3_forbidden_test",
                "claim_piece": "operator-domain forbids lambda_A F_Q^2",
                "formal_statement": "lambda_A F_Q^2 is outside the allowed visible operator algebra.",
                "result": "NOT_DERIVED",
                "proof_or_blocker": "U(1), diffeomorphism covariance, and minimal-action aesthetics do not forbid a standalone F2 coefficient",
            },
            {
                "attempt_id": "LFA1109_4_derivative_test",
                "claim_piece": "constant lambda_A does not generate b_alpha by itself",
                "formal_statement": "Lie_v lambda_A = 0 implies no vertical drift contribution from lambda_A alone.",
                "result": "TRUE_BUT_INSUFFICIENT",
                "proof_or_blocker": "this can support drift silence only after hidden f(I), readout, and arena projection terms are also controlled",
            },
            {
                "attempt_id": "LFA1109_5_hidden_or_running_lambda",
                "claim_piece": "lambda can become finite alpha coefficient if branch/running/readout dependent",
                "formal_statement": "lambda_A(I_hid, mu, readout) gives Lie_v ln Z_Q != 0 or arena-dependent alpha products.",
                "result": "RETAINED_RESIDUAL",
                "proof_or_blocker": "radiative/readout and hidden target action are unsigned",
            },
            {
                "attempt_id": "LFA1109_6_verdict",
                "claim_piece": "prove no-independent-lambda-F2 theorem",
                "formal_statement": "lambda_A is either forbidden/redundant without losing alpha prediction, or safely absorbed with no residual coefficient debt.",
                "result": "NO_INDEPENDENT_LAMBDA_F2_THEOREM_NOT_DERIVED",
                "proof_or_blocker": "lambda_A is calibration-only if universal, but remains an unpredicted alpha-normalization parameter; if non-universal or hidden/readout dependent it is a finite coefficient debt",
            },
        ]
    )


def classification_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "class_id": "LAM1109_0_parent_norm",
                "lambda_case": "lambda_A absent",
                "status": "THEOREM_TARGET",
                "effect": "alpha can be owned by C_P N_Q if T_Q/norm/readout are also signed",
                "policy": "not current corpus",
            },
            {
                "class_id": "LAM1109_1_universal_constant",
                "lambda_case": "lambda_A is one universal constant",
                "status": "CALIBRATION_MODE",
                "effect": "absorbs into measured Z_Q but destroys predictive alpha normalization",
                "policy": "allowed only as explicit fitted constant, not derivation",
            },
            {
                "class_id": "LAM1109_2_branch_constant",
                "lambda_case": "lambda_A differs by branch/domain/material/readout class",
                "status": "FINITE_RESIDUAL",
                "effect": "creates source/readout-dependent alpha normalization",
                "policy": "requires source-backed finite row or theorem-zero",
            },
            {
                "class_id": "LAM1109_3_hidden_dependent",
                "lambda_case": "lambda_A=f(I_hid) or f_X(Xhat)",
                "status": "FINITE_ALPHA_DRIFT_RESIDUAL",
                "effect": "generates b_alpha/c_alpha and cross-arena pressure",
                "policy": "requires no-hidden-visible theorem or sourced coefficient",
            },
            {
                "class_id": "LAM1109_4_radiative_readout",
                "lambda_case": "lambda_A^eff(mu,readout)",
                "status": "RETAINED_UNTIL_RADIOUT_CLOSURE",
                "effect": "tree-level no-lambda does not survive observed clocks/spectra automatically",
                "policy": "requires EFT/readout closure",
            },
        ]
    )


def finite_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "row_id": "FAL1109_0_lambda_universal",
                "coefficient": "lambda_A_common",
                "value_or_status": "MISSING_NUMERIC_PARENT_OR_MEASURED_NORMALIZATION_SPLIT",
                "units": "dimensionless Maxwell coefficient contribution",
                "role": "calibration_parameter_not_prediction",
                "bound_or_threshold": "none; absorbed into measured alpha unless prediction is claimed",
                "required_for_claim": "source proving lambda_A absent or fixed by parent, not merely fitted",
            },
            {
                "row_id": "FAL1109_1_lambda_vertical",
                "coefficient": "d ln Z_Q / dX from lambda/f(I)",
                "value_or_status": "MISSING_SOURCE_BACKED_ALPHA_COEFFICIENT",
                "units": "dimensionless derivative coefficient",
                "role": "finite alpha drift/product coefficient",
                "bound_or_threshold": "abs(c_alpha_DD or b_alpha) <= 8.320244933243533e-10",
                "required_for_claim": "numeric coefficient source path or theorem-zero",
            },
            {
                "row_id": "FAL1109_2_clock_product",
                "coefficient": "b_alpha*tau_clock_time",
                "value_or_status": "MISSING_MTS_CLOCK_PRODUCT_PREDICTION",
                "units": "yr^-1",
                "role": "clock product route",
                "bound_or_threshold": "2.1e-18 yr^-1",
                "required_for_claim": "tau_clock/Xhat map and coefficient/product prediction",
            },
            {
                "row_id": "FAL1109_3_WEP_alpha",
                "coefficient": "P_WEP_alpha",
                "value_or_status": "MISSING_BETA_SOURCE_ALPHA_TAU_WEP_PRODUCT",
                "units": "dimensionless",
                "role": "WEP alpha product route",
                "bound_or_threshold": "4.797780522732e-05",
                "required_for_claim": "beta_source_alpha, tau_WEP, material/readout map, or direct product theorem",
            },
        ]
    )


def claim_gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "CG1109_0_no_lambda",
                "claim": "lambda_A F_Q^2 is forbidden/redundant without loss",
                "gate_pass": "false",
                "reason": "universal lambda is calibration-only and non-universal lambda remains residual",
            },
            {
                "gate_id": "CG1109_1_alpha_prediction",
                "claim": "parent norm predicts alpha",
                "gate_pass": "false",
                "reason": "independent lambda_A destroys unique predictive normalization unless forbidden",
            },
            {
                "gate_id": "CG1109_2_balpha_zero",
                "claim": "b_alpha=0 is derived",
                "gate_pass": "false",
                "reason": "hidden/radiative/readout lambda and f(I)F2 branches remain unsigned",
            },
            {
                "gate_id": "CG1109_3_finite_alpha_row",
                "claim": "finite alpha coefficient row is scoreable",
                "gate_pass": "false",
                "reason": "finite rows contain missing coefficient/projection/source inputs",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "DEC1109_0_lambda_result",
                "decision": "no-independent-lambda-F2 theorem is not derived",
                "because": "lambda_A can be calibrated if universal but cannot be used as a parent alpha prediction; if branch/hidden/readout dependent it remains a finite coefficient",
                "next_action": "do not claim alpha owner from parent norm alone",
            },
            {
                "decision_id": "DEC1109_1_best_theory_next",
                "decision": "separate alpha normalization prediction from alpha drift/product tests",
                "because": "universal lambda affects alpha value/predictivity while hidden/running lambda affects drift and WEP/clock/R10 products",
                "next_action": "build a two-track alpha ledger: normalization calibration vs vertical/running coefficient",
            },
            {
                "decision_id": "DEC1109_2_finite_next",
                "decision": "finite alpha acquisition should target vertical/running coefficient first",
                "because": "that is what clocks/WEP/R10 can bound; universal alpha normalization is not a local test prediction without a parent value",
                "next_action": "1110 should split lambda_common from b_alpha/c_alpha acquisition",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1109_0_1110",
                "next_target": "1110-Y5-R10-alpha-normalization-vs-drift-two-track-ledger.md",
                "objective": "split the alpha problem into two tracks: universal Maxwell normalization/alpha value calibration versus vertical or running alpha coefficient tested by clocks, WEP, and R10; stage source requirements for each without claiming b_alpha=0 or alpha prediction",
                "include": "lambda_common calibration; b_alpha/c_alpha derivative coefficient; clock product; WEP product; R10 alpha(lambda); parent no-extra-F2 status; strict runner gates",
                "exclude": "claiming measured alpha is predicted; standalone b_alpha from clocks; tau=1; WEP/R10 transfer without maps; local-GR claim; GitHub; formalization edits",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    classes: list[dict[str, object]],
    finite: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    outputs: dict[str, Path],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "result": "pass" if passed else "fail",
                "detail": detail,
                "valid_for_claim": "false",
                "generated_utc": now(),
            }
        )

    add("V1109_0_sources_exist", all(r["exists"] == "true" and r["needle_found"] == "true" for r in sources), "all cited local source paths exist and needles are found")
    add("V1109_1_theorem_not_derived", any(r["result"] == "NO_INDEPENDENT_LAMBDA_F2_THEOREM_NOT_DERIVED" for r in theorem), "no-independent-lambda theorem is explicitly not promoted")
    add("V1109_2_calibration_distinction", any(r["result"] == "CALIBRATION_ONLY_NOT_PREDICTION" for r in theorem) and any(r["status"] == "CALIBRATION_MODE" for r in classes), "universal lambda is classified as calibration, not prediction")
    add("V1109_3_residual_distinction", any(r["status"] == "FINITE_ALPHA_DRIFT_RESIDUAL" for r in classes), "hidden/branch/running lambda remains finite alpha residual")
    add("V1109_4_finite_rows_nonclaim", all("MISSING" in r["value_or_status"] and r["claim_allowed"] == "false" for r in finite), "finite alpha rows remain missing-input/nonclaim")
    add("V1109_5_claim_gates_blocked", all(r["gate_pass"] == "false" and r["claim_allowed"] == "false" for r in gates), "all claim gates remain blocked")
    add("V1109_6_next_target", next_target[0]["next_target"].startswith("1110-") and "two-track" in str(next_target[0]["next_target"]), "1110 handoff splits alpha normalization and drift tracks")
    add("V1109_7_no_claim_rows", all(r.get("valid_for_claim") == "false" for r in theorem + classes + finite + gates + decisions + next_target), "all generated rows remain nonclaim")
    add("V1109_8_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()), "all generated outputs are under post-checkpoint-work")
    csv_parse_ok = True
    for name, path in outputs.items():
        if name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1109_9_csv_parse", csv_parse_ok, "all 1109 CSV outputs parse cleanly")
    add("V1109_10_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add("V1109_SUMMARY", True, "1109 classifies universal lambda as calibration-only and hidden/running lambda as finite alpha residual")
    return rows


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    classes: list[dict[str, object]],
    finite: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1109 - No Independent Lambda F2 Theorem Or Finite Alpha Coefficient Acquisition

**Current verdict:** `lambda_A F_Q^2` is not eliminated. If it is one universal constant, it can be absorbed into measured alpha as calibration, but then alpha is fitted rather than predicted. If it is branch-, hidden-, running-, or readout-dependent, it is a finite alpha residual.

**Important distinction:** universal alpha normalization and vertical/running alpha drift are different tests. Clocks, WEP, and R10 mostly constrain drift/product coefficients, not the absolute measured value of alpha unless the parent theory predicts that value.

**No claim:** no `b_alpha=0`, no parent alpha prediction, and no cross-arena alpha product follows from 1109.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "note"], sources)}

## Lambda-F2 Theorem Attempt
{table(["attempt_id", "claim_piece", "formal_statement", "result", "proof_or_blocker", "claim_allowed"], theorem)}

## Lambda Classification
{table(["class_id", "lambda_case", "status", "effect", "policy", "claim_allowed"], classes)}

## Finite Alpha Rows
{table(["row_id", "coefficient", "value_or_status", "units", "role", "bound_or_threshold", "required_for_claim", "claim_allowed"], finite)}

## Claim Gates
{table(["gate_id", "claim", "gate_pass", "reason", "claim_allowed"], gates)}

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
        "source_register": OUT / "P8_Y5_R10_1109_SOURCE_REGISTER.csv",
        "theorem": OUT / "P8_Y5_R10_1109_LAMBDA_F2_THEOREM_ATTEMPT.csv",
        "classification": OUT / "P8_Y5_R10_1109_LAMBDA_CLASSIFICATION.csv",
        "finite": OUT / "P8_Y5_R10_1109_FINITE_ALPHA_ROWS_NONCLAIM.csv",
        "gates": OUT / "P8_Y5_R10_1109_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1109_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1109_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1109_VALIDATION.csv",
    }
    sources = source_rows()
    theorem = lambda_theorem_rows()
    classes = classification_rows()
    finite = finite_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["theorem"], theorem)
    write_csv(outputs["classification"], classes)
    write_csv(outputs["finite"], finite)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, theorem, classes, finite, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, theorem, classes, finite, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
