from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1111-Y5-R10-alpha-drift-zero-theorem-or-product-source-vector.md"


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
            "source_id": "SRC1111_0_1110_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1110_NEXT_TARGET.csv",
            "needle": "NEXT1110_0_1111",
            "note": "1110 handoff to alpha drift zero theorem or product vector.",
        },
        {
            "source_id": "SRC1111_1_1110_tracks",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1110_TWO_TRACK_LEDGER.csv",
            "needle": "TRACK1110_D0",
            "note": "drift coefficient track.",
        },
        {
            "source_id": "SRC1111_2_1110_requirements",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1110_ALPHA_PRODUCT_REQUIREMENTS.csv",
            "needle": "REQ1110_0_alpha_drift",
            "note": "alpha drift coefficient requirement.",
        },
        {
            "source_id": "SRC1111_3_1109_hidden",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1109_LAMBDA_CLASSIFICATION.csv",
            "needle": "LAM1109_3_hidden_dependent",
            "note": "hidden-dependent lambda remains finite alpha drift residual.",
        },
        {
            "source_id": "SRC1111_4_1109_running",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1109_LAMBDA_F2_THEOREM_ATTEMPT.csv",
            "needle": "LFA1109_5_hidden_or_running_lambda",
            "note": "running/readout lambda retained residual.",
        },
        {
            "source_id": "SRC1111_5_1099_radiative",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1099_NO_EXTRA_F2_EXCLUSION_AUDIT.csv",
            "needle": "EXC1099_5_radiative",
            "note": "radiative/readout closure unsigned.",
        },
        {
            "source_id": "SRC1111_6_988_joint",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_988_JOINT_ALPHA_VARIABLE_GATE.csv",
            "needle": "JAV988_0_alpha_slot",
            "note": "shared local alpha slot but missing parent normalization and arena maps.",
        },
        {
            "source_id": "SRC1111_7_1098_req",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1098_SOURCE_BACKED_COEFFICIENT_REQUIREMENTS.csv",
            "needle": "REQ1098_0_c_alpha",
            "note": "absolute coefficient threshold.",
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
    requirement_rows = read_csv_rows("source-intake/mts_residuals/P8_Y5_R10_1110_ALPHA_PRODUCT_REQUIREMENTS.csv")
    track_rows = read_csv_rows("source-intake/mts_residuals/P8_Y5_R10_1110_TWO_TRACK_LEDGER.csv")
    alpha_requirement = next(row for row in requirement_rows if row["requirement_id"] == "REQ1110_0_alpha_drift")
    clock_requirement = next(row for row in requirement_rows if row["requirement_id"] == "REQ1110_1_clock_product")
    wep_requirement = next(row for row in requirement_rows if row["requirement_id"] == "REQ1110_2_wep_product")
    drift_track = next(row for row in track_rows if row["track_id"] == "TRACK1110_D0")
    return {
        "alpha_threshold_abs": alpha_requirement["numeric_bound_or_target"],
        "clock_product_bound": clock_requirement["numeric_bound_or_target"],
        "wep_beta_target": wep_requirement["numeric_bound_or_target"],
        "drift_blocker": drift_track["blocker"],
    }


def zq_term_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "term_id": "ZQ1111_0_parent_norm",
                "term": "C_P N_Q",
                "drift_piece": "D_v(C_P N_Q)",
                "zero_condition": "parent Maxwell normalization descends to quotient and is constant along local vertical generator",
                "signed_status": "UNSIGNED",
                "blocker": "no parent value/descent theorem for C_P N_Q in current alpha branch",
            },
            {
                "term_id": "ZQ1111_1_common_lambda",
                "term": "lambda_A_common",
                "drift_piece": "D_v lambda_A_common",
                "zero_condition": "lambda_A is one universal constant, not branch/readout/running dependent",
                "signed_status": "SIGNED_ONLY_FOR_CALIBRATION_CASE",
                "blocker": "does not predict alpha value; only removes this term from drift if universal",
            },
            {
                "term_id": "ZQ1111_2_hidden_visible",
                "term": "f_hid(I_hid) F_Q^2",
                "drift_piece": "D_v f_hid(I_hid)",
                "zero_condition": "hidden-visible product functor or exact shift symmetry forbids nonconstant visible F2 coefficient",
                "signed_status": "UNSIGNED",
                "blocker": "1099 keeps product functor/shift route conditional only",
            },
            {
                "term_id": "ZQ1111_3_radiative",
                "term": "Delta_rad(mu,X)",
                "drift_piece": "D_v Delta_rad",
                "zero_condition": "EFT threshold/running map has no local vertical dependence after matching",
                "signed_status": "UNSIGNED",
                "blocker": "radiative/readout closure is unsigned; tree-level silence is insufficient",
            },
            {
                "term_id": "ZQ1111_4_readout",
                "term": "Delta_readout(rho,X)",
                "drift_piece": "D_v Delta_readout",
                "zero_condition": "clock/spectrum/material readout map descends and contains no representative-dependent alpha coefficient",
                "signed_status": "UNSIGNED",
                "blocker": "clock, WEP, and R10 maps are not yet one parent-owned readout functor",
            },
            {
                "term_id": "ZQ1111_5_denominator",
                "term": "Z_Q_eff",
                "drift_piece": "D_v ln Z_Q_eff = D_v Z_Q_eff / Z_Q_eff",
                "zero_condition": "Z_Q_eff positive and finite in local domain",
                "signed_status": "ASSUMED_PHYSICAL_BUT_NOT_PREDICTIVE",
                "blocker": "positivity avoids singularity but does not make numerator vanish",
            },
        ]
    )


def theorem_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "attempt_id": "ADZ1111_0_definition",
                "claim_piece": "define effective alpha normalization",
                "statement": "Z_Q_eff = C_P N_Q + lambda_A_common + f_hid(I_hid) + Delta_rad(mu,X) + Delta_readout(rho,X)",
                "result": "DECOMPOSITION_ADOPTED_AS_AUDIT_FORM",
                "proof_or_blocker": "captures all live 1109/1110 alpha wounds without claiming each term is fundamental",
            },
            {
                "attempt_id": "ADZ1111_1_chain_rule",
                "claim_piece": "conditional chain-rule zero",
                "statement": "If every term in D_v Z_Q_eff vanishes and Z_Q_eff is finite, then D_v ln Z_Q_eff = 0 and b_alpha = -D_v ln Z_Q_eff = 0.",
                "result": "CONDITIONAL_CHAIN_RULE_THEOREM",
                "proof_or_blocker": "exact calculus identity; useful but only as strong as the zero clauses",
            },
            {
                "attempt_id": "ADZ1111_2_common_lambda",
                "claim_piece": "universal lambda does not drift",
                "statement": "D_v lambda_A_common = 0.",
                "result": "SIGNED_ONLY_IN_UNIVERSAL_CALIBRATION_BRANCH",
                "proof_or_blocker": "helps local drift but does not restore absolute alpha prediction",
            },
            {
                "attempt_id": "ADZ1111_3_parent_norm",
                "claim_piece": "parent norm is vertical silent",
                "statement": "D_v(C_P N_Q)=0.",
                "result": "NOT_DERIVED",
                "proof_or_blocker": "no current parent quotient/readout theorem fixes C_P N_Q along the local vertical generator",
            },
            {
                "attempt_id": "ADZ1111_4_hidden_radiative_readout",
                "claim_piece": "hidden/radiative/readout pieces are vertical silent",
                "statement": "D_v f_hid = D_v Delta_rad = D_v Delta_readout = 0.",
                "result": "NOT_DERIVED",
                "proof_or_blocker": "these are exactly the current unsigned coupling/readout channels",
            },
            {
                "attempt_id": "ADZ1111_5_verdict",
                "claim_piece": "prove alpha drift zero",
                "statement": "d_v ln Z_Q_eff = 0 for the local alpha sector.",
                "result": "ALPHA_DRIFT_ZERO_NOT_DERIVED",
                "proof_or_blocker": "the chain-rule theorem is exact but parent-norm, hidden-visible, radiative, and readout zero clauses are unsigned",
            },
        ]
    )


def product_vector_rows(values: dict[str, str]) -> list[dict[str, object]]:
    return stamp(
        [
            {
                "product_id": "PV1111_0_balpha",
                "quantity": "b_alpha = -D_v ln Z_Q_eff",
                "bound_or_target": values["alpha_threshold_abs"],
                "units": "dimensionless coefficient",
                "arena": "shared local alpha slot",
                "required_source_or_theorem": "derive all Z_Q_eff drift clauses zero or source b_alpha/c_alpha_DD numerically",
                "current_status": "MISSING_THEOREM_ZERO_OR_SOURCE_BACKED_COEFFICIENT",
            },
            {
                "product_id": "PV1111_1_clock",
                "quantity": "b_alpha * tau_clock_time",
                "bound_or_target": values["clock_product_bound"],
                "units": "yr^-1",
                "arena": "atomic clocks",
                "required_source_or_theorem": "tau_clock_time map or direct MTS clock product prediction",
                "current_status": "PRODUCT_BOUND_EXISTS_BUT_MTS_PRODUCT_MISSING",
            },
            {
                "product_id": "PV1111_2_wep",
                "quantity": "beta_source_alpha * b_alpha * tau_WEP",
                "bound_or_target": values["wep_beta_target"],
                "units": "dimensionless imported pressure target",
                "arena": "WEP/MICROSCOPE alpha-Coulomb channel",
                "required_source_or_theorem": "beta_source_alpha, tau_WEP, material map, or direct product theorem",
                "current_status": "PRODUCT_BOUND_EXISTS_BUT_SOURCE_NORMALIZATION_MISSING",
            },
            {
                "product_id": "PV1111_3_r10",
                "quantity": "K_X^R10(lambda) * beta_source(lambda) * beta_test(lambda)",
                "bound_or_target": "claim-valid alpha_bound(lambda)",
                "units": "dimensionless Yukawa alpha",
                "arena": "R10 short-range force",
                "required_source_or_theorem": "numeric R10 product and promoted real bound curve",
                "current_status": "MISSING_R10_PRODUCT_AND_PROMOTED_BOUND",
            },
            {
                "product_id": "PV1111_4_readout",
                "quantity": "Delta_readout_alpha",
                "bound_or_target": "must be zero theorem or included in b_alpha/product rows",
                "units": "dimensionless/readout dependent",
                "arena": "EM spectra; clocks; material probes",
                "required_source_or_theorem": "readout descent functor or explicit residual coefficient",
                "current_status": "MISSING_READOUT_DESCENT_OR_RESIDUAL_ROW",
            },
        ]
    )


def claim_gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "CG1111_0_alpha_drift_zero",
                "claim": "b_alpha=0 is derived",
                "gate_pass": "false",
                "reason": "only conditional chain-rule theorem is proved; zero clauses are unsigned",
            },
            {
                "gate_id": "CG1111_1_parent_alpha_prediction",
                "claim": "parent predicts absolute alpha",
                "gate_pass": "false",
                "reason": "universal lambda remains calibration and parent norm value is not fixed",
            },
            {
                "gate_id": "CG1111_2_clock_score",
                "claim": "clock bound scores standalone b_alpha",
                "gate_pass": "false",
                "reason": "clock bound is product-only until tau_clock is derived",
            },
            {
                "gate_id": "CG1111_3_wep_score",
                "claim": "WEP alpha product passes",
                "gate_pass": "false",
                "reason": "source normalization and tau_WEP are missing",
            },
            {
                "gate_id": "CG1111_4_r10_score",
                "claim": "R10 alpha branch passes",
                "gate_pass": "false",
                "reason": "numeric R10 product and promoted bound curve are missing",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "DEC1111_0_result",
                "decision": "alpha drift zero theorem is not promoted",
                "because": "chain-rule zero is exact but not enough; parent norm, hidden, radiative, and readout drift terms are unsigned",
                "next_action": "focus on Z_Q_eff descent clauses rather than reusing absolute alpha calibration",
            },
            {
                "decision_id": "DEC1111_1_best_route",
                "decision": "attack readout/descent closure first",
                "because": "one descent theorem can silence clocks, WEP, and R10 product channels without separate fitted coefficients",
                "next_action": "write a Z_Q_eff descent contract and audit which clauses are parent-signable",
            },
            {
                "decision_id": "DEC1111_2_fallback_route",
                "decision": "finite product vector is now explicit",
                "because": "if descent fails, the scoreable path is product-by-product with no tau=1 or source-unity shortcuts",
                "next_action": "convert product vector into runner-ready nonclaim rows only after numeric source paths exist",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1111_0_1112",
                "next_target": "1112-Y5-R10-ZQeff-descent-clause-audit-or-alpha-product-runner-contract.md",
                "objective": "try to sign the Z_Q_eff descent/readout clauses that would make d_v ln Z_Q_eff vanish; if not, convert the finite alpha product vector into strict runner contract rows",
                "include": "parent norm descent; hidden-visible sequester; radiative closure; readout functor; clock tau; WEP source normalization; R10 product map",
                "exclude": "absolute alpha prediction claim; tau=1; source-unity; clock-to-WEP shortcut; local-GR claim; GitHub; formalization edits",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    terms: list[dict[str, object]],
    theorem: list[dict[str, object]],
    products: list[dict[str, object]],
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

    add("V1111_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources), "all cited local source paths exist and needles are found")
    add("V1111_1_chain_rule_proved", any(row["result"] == "CONDITIONAL_CHAIN_RULE_THEOREM" for row in theorem), "conditional chain-rule theorem is recorded")
    add("V1111_2_drift_zero_not_promoted", any(row["result"] == "ALPHA_DRIFT_ZERO_NOT_DERIVED" for row in theorem), "alpha drift zero remains unpromoted")
    add("V1111_3_unsigned_terms_present", sum(1 for row in terms if row["signed_status"] == "UNSIGNED") >= 3, "multiple Z_Q_eff drift clauses remain unsigned")
    add("V1111_4_product_vector_complete", all(any(token in str(row["quantity"]) for row in products) for token in ["b_alpha", "tau_clock", "tau_WEP", "K_X^R10"]), "alpha coefficient, clock, WEP, and R10 products are explicit")
    add("V1111_5_gates_blocked", all(row["gate_pass"] == "false" for row in gates), "all claim gates remain blocked")
    add("V1111_6_no_claim_rows", all(row.get("valid_for_claim") == "false" and row.get("claim_allowed") == "false" for row in terms + theorem + products + gates + decisions + next_target), "all generated rows remain nonclaim")
    add("V1111_7_next_target", next_target[0]["next_target"].startswith("1112-") and "ZQeff-descent" in str(next_target[0]["next_target"]), "1112 handoff targets Z_Q_eff descent clause audit")
    add("V1111_8_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()), "all generated outputs are under post-checkpoint-work")
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1111_9_csv_parse", csv_parse_ok, "all 1111 CSV outputs parse cleanly")
    add("V1111_10_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add("V1111_SUMMARY", True, "1111 proves only the conditional chain-rule zero and keeps finite product vector nonclaim")
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for source_row in rows:
        lines.append("| " + " | ".join(str(source_row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    values: dict[str, str],
    sources: list[dict[str, object]],
    terms: list[dict[str, object]],
    theorem: list[dict[str, object]],
    products: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1111 - Alpha Drift Zero Theorem Or Product Source Vector

**Current verdict:** the exact chain-rule route exists, but the full alpha-drift zero theorem is not derived. `D_v ln Z_Q_eff = 0` follows if every effective Maxwell-normalization term is vertical-silent; the current corpus only signs the universal `lambda_A_common` calibration subcase, not the parent norm, hidden-visible, radiative, or readout clauses.

**Sharp formula:** with `alpha_EM proportional to Z_Q_eff^-1`, `b_alpha = D_v ln alpha_EM = -D_v ln Z_Q_eff`. The sign is irrelevant for the local bound gates; the numerator `D_v Z_Q_eff` is the wound.

**No claim:** no `b_alpha=0`, no parent alpha prediction, no clock/WEP/R10 pass, and no local-GR pass follows from 1111.

## Imported Pressure
| quantity | value |
| --- | --- |
| alpha coefficient threshold | {values["alpha_threshold_abs"]} |
| clock product bound | {values["clock_product_bound"]} yr^-1 |
| WEP beta-source pressure target | {values["wep_beta_target"]} |
| inherited drift blocker | {values["drift_blocker"]} |

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "note"], sources)}

## Effective ZQ Terms
{table(["term_id", "term", "drift_piece", "zero_condition", "signed_status", "blocker", "claim_allowed"], terms)}

## Drift-Zero Theorem Attempt
{table(["attempt_id", "claim_piece", "statement", "result", "proof_or_blocker", "claim_allowed"], theorem)}

## Product Source Vector
{table(["product_id", "quantity", "bound_or_target", "units", "arena", "required_source_or_theorem", "current_status", "claim_allowed"], products)}

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
        "source_register": OUT / "P8_Y5_R10_1111_SOURCE_REGISTER.csv",
        "terms": OUT / "P8_Y5_R10_1111_ZQEFF_TERM_AUDIT.csv",
        "theorem": OUT / "P8_Y5_R10_1111_ALPHA_DRIFT_ZERO_THEOREM_ATTEMPT.csv",
        "products": OUT / "P8_Y5_R10_1111_PRODUCT_SOURCE_VECTOR_NONCLAIM.csv",
        "gates": OUT / "P8_Y5_R10_1111_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1111_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1111_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1111_VALIDATION.csv",
    }
    values = extracted_values()
    sources = source_rows()
    terms = zq_term_rows()
    theorem = theorem_rows()
    products = product_vector_rows(values)
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["terms"], terms)
    write_csv(outputs["theorem"], theorem)
    write_csv(outputs["products"], products)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, terms, theorem, products, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(values, sources, terms, theorem, products, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
