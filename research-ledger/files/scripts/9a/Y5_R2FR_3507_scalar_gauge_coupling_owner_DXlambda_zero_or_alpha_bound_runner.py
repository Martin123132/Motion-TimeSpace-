from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3507-Y5-R2FR-scalar-gauge-coupling-owner-DXlambda-zero-or-alpha-bound-runner.md"
CANONICAL_ALPHA_RESIDUAL = OUT / "P8_EM_scalar_coupling_owner_alpha_residual.csv"

SOURCES: dict[str, dict[str, Any]] = {
    "script_3507": {"path": Path(__file__).resolve(), "role": "generator"},
    "doc_3506": {
        "path": ROOT / "3506-Y5-R2FR-parent-visible-EM-generator-signature-or-first-constitutive-bound-runner.md",
        "role": "3506 EM generator handoff",
    },
    "reduction_3506": {
        "path": OUT / "P8_Y5_R2FR_3506_RESIDUAL_REDUCTION_MAP.csv",
        "role": "3506 residual reduction map",
    },
    "runner_3506": {
        "path": OUT / "P8_Y5_R2FR_3506_CONSTITUTIVE_BOUND_RUNNER_RESULTS.csv",
        "role": "3506 first constitutive runner results",
    },
    "alpha_contract_1055": {
        "path": ROOT / "1055-Y5-R10-alpha-owner-and-matter-functor-parent-action-contract.md",
        "role": "alpha owner and matter-functor contract",
    },
    "alpha_norm_1056": {
        "path": ROOT / "1056-Y5-R10-alpha-owner-from-vertical-generator-norm-or-topological-level.md",
        "role": "alpha owner from vertical generator norm/topology attempt",
    },
    "alpha_owner_764": {
        "path": OUT / "P8_Y5_R10_764_ALPHA_EM_OWNER_AUDIT.csv",
        "role": "alpha EM owner audit",
    },
    "vertical_norm_765": {
        "path": OUT / "P8_Y5_R10_765_VERTICAL_GENERATOR_NORM_THEOREM_ATTEMPT.csv",
        "role": "vertical generator norm theorem attempt",
    },
    "radiative_1051": {
        "path": OUT / "P8_Y5_R10_1051_ALPHA_OWNER_RADIATIVE_CLOSURE_AUDIT.csv",
        "role": "alpha/radiative closure audit",
    },
    "clock_bound_1052": {
        "path": OUT / "P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv",
        "role": "alpha clock product bound ledger",
    },
    "r10_bound_candidate": {
        "path": ROOT / "source-intake" / "local_bounds" / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
        "role": "R10 alpha-lambda review candidate non-claim curve",
    },
}


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def source_register_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(metadata["path"]),
            "exists": bool_text(Path(metadata["path"]).exists()),
            "role": metadata["role"],
            "valid_for_claim": "False",
        }
        for source_id, metadata in SOURCES.items()
    ]


def coupling_identity_rows() -> list[dict[str, Any]]:
    return [
        {
            "identity_id": "ALPHA3507_0_canonical_normalization_identity",
            "object": "physical EM coupling",
            "statement": "For S_EM=-lambda_A/4 int F^2 + g_J int A.J, the locally measured charge after canonical normalization is g_eff=g_J/sqrt(lambda_A).",
            "derivation": "Set A_c=sqrt(lambda_A) A pointwise in a local patch. The kinetic term is canonical and the source term becomes (g_J/sqrt(lambda_A)) A_c.J; gradients of lambda_A are separate derivative-coupling residuals.",
            "mathematical_form": "alpha_eff proportional to g_eff^2 = g_J^2/lambda_A",
            "closes_if": "g_J and lambda_A are fixed by one parent quotient owner, or 2 D_X ln g_J = D_X ln lambda_A",
            "remaining_residual": "b_alpha_X = D_X ln(g_J^2/lambda_A)",
            "status": "EXACT_LOCAL_IDENTITY",
            "source_path": str(SOURCES["reduction_3506"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "identity_id": "ALPHA3507_1_vertical_residual_law",
            "object": "hidden/local vertical variation",
            "statement": "The scalar coupling leak seen by alpha, clocks, WEP/R10, and source normalization is the single vertical residual b_alpha_X.",
            "derivation": "Taking D_X ln of alpha_eff gives the invariant product rule; no convention can remove it unless the same convention also fixes current and matter readout.",
            "mathematical_form": "D_X ln alpha_eff = 2 D_X ln g_J - D_X ln lambda_A",
            "closes_if": "Z_alpha := 2 z_g - z_lambda = 0 with z_g=D_X ln g_J and z_lambda=D_X ln lambda_A",
            "remaining_residual": "Z_alpha",
            "status": "EXACT_DERIVATIVE_IDENTITY",
            "source_path": str(SOURCES["alpha_contract_1055"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "identity_id": "ALPHA3507_2_fixed_generator_norm_route",
            "object": "parent fibre metric / generator norm",
            "statement": "A fixed parent generator norm can own lambda_A only if it also fixes the current generator normalization and forbids independent rescaling A_Q -> s A_Q.",
            "derivation": "Compact charge labels quantize representation weights, but the continuous Maxwell kinetic coefficient remains free unless the parent fibre metric or topological level is itself a fixed quotient datum.",
            "mathematical_form": "lambda_A=C_P N_Q and g_J=C_J sqrt(N_Q) or equivalent shared-owner relation",
            "closes_if": "D_X ln C_P = D_X ln C_J = D_X ln N_Q = 0 and no independent F_Q^2 counterterm",
            "remaining_residual": "independent lambda_A F_Q^2 and current/readout rescaling",
            "status": "ROUTE_CONSTRUCTED_NOT_PARENT_SIGNED",
            "source_path": str(SOURCES["alpha_norm_1056"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "identity_id": "ALPHA3507_3_convention_trap",
            "object": "field rescaling freedom",
            "statement": "Setting lambda_A=1 by field convention is not a physics proof if g_J, matter masses, clock readout, and source normalization are not transformed and fixed together.",
            "derivation": "A rescaling can move the coupling between kinetic and source terms, but alpha_eff and Coulomb binding observables depend on the invariant ratio g_J^2/lambda_A.",
            "mathematical_form": "A -> s A: lambda_A -> lambda_A/s^2, g_J -> s g_J, g_J^2/lambda_A invariant when the same observable current is tracked",
            "closes_if": "the parent action supplies a fixed normalization of both the gauge field and current functor",
            "remaining_residual": "source-current normalization ambiguity",
            "status": "GUARD_AGAINST_FALSE_ZERO",
            "source_path": str(SOURCES["alpha_owner_764"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "identity_id": "ALPHA3507_4_derivative_lambda_warning",
            "object": "field-dependent lambda_A",
            "statement": "If lambda_A varies in spacetime or along local vertical directions, canonical normalization generates derivative interactions in addition to alpha drift.",
            "derivation": "F(A_c/sqrt(lambda_A)) contains dln(lambda_A) wedge A_c terms; these are not removed by calling lambda_A a unit convention.",
            "mathematical_form": "F(A)=lambda_A^(-1/2)[F_c - 1/2 dln(lambda_A) wedge A_c]",
            "closes_if": "d lambda_A=0 in the local branch or derivative terms are separately bounded",
            "remaining_residual": "dlnlambda derivative coupling",
            "status": "DERIVATIVE_RESIDUAL_RETAINED",
            "source_path": str(SOURCES["radiative_1051"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def owner_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3507_0_same_parent_owner",
            "gate": "same parent owner for kinetic and current normalization",
            "required_signature": "lambda_A, g_J, charge labels and current J_Q descend from one fixed quotient representation/fibre metric datum",
            "mathematical_test": "2 D_X ln g_J - D_X ln lambda_A = 0",
            "current_status": "NOT_PARENT_SIGNED",
            "failure_mode": "alpha_EM drift and C_XF2/source-normalization branch remain",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3507_1_no_independent_F2_counterterm",
            "gate": "ban independent scalar gauge-kinetic function",
            "required_signature": "no f_X(Phi) F_Q wedge *_obs F_Q slot beyond the parent-owned lambda_A",
            "mathematical_test": "D_X ln lambda_A is inherited, not freely specifiable",
            "current_status": "NOT_PARENT_SIGNED",
            "failure_mode": "C_XF2 survives exactly where 3506 isolated it",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3507_2_current_readout_locked",
            "gate": "source current and measured charge readout share normalization",
            "required_signature": "J_Q is the variation of the same matter action that defines clocks/masses/binding, not a separately scaled source current",
            "mathematical_test": "D_X ln g_J equals the charge-readout derivative used in alpha_eff",
            "current_status": "CONDITIONAL_FROM_MATTER_FUNCTOR",
            "failure_mode": "rescaling convention hides a physical alpha/source leak",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE3507_3_derivative_coupling_silent",
            "gate": "no derivative-lambda local force term",
            "required_signature": "d lambda_A=0 or derivative terms project out of the local source/PPN/clock arenas",
            "mathematical_test": "dlnlambda wedge A_c term absent or bounded",
            "current_status": "NOT_CLOSED",
            "failure_mode": "Maxwell form passes but local force/current residual remains",
            "valid_for_claim": "False",
        },
    ]


def alpha_residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "ARE3507_0_b_alpha_X",
            "residual": "b_alpha_X",
            "definition": "D_X ln alpha_eff",
            "formula": "2 D_X ln g_J - D_X ln lambda_A",
            "zero_condition": "2 z_g = z_lambda",
            "observable_links": "alpha_EM; clocks; spectroscopy; Coulomb_binding; WEP; R10",
            "status": "EXACT_IDENTITY_NOT_NUMERIC",
            "source_path": str(SOURCES["alpha_contract_1055"]["path"]),
            "next_action": "derive same-owner relation or bound b_alpha_X",
            "valid_for_claim": "False",
        },
        {
            "row_id": "ARE3507_1_C_XF2",
            "residual": "C_XF2",
            "definition": "independent scalar multiplier of F_Q wedge *_obs F_Q",
            "formula": "delta lambda_A/lambda_A or D_X ln lambda_A",
            "zero_condition": "no independent f_X(Phi)F^2 slot",
            "observable_links": "alpha_EM; clock; WEP; R10; source_normalization",
            "status": "CORE_COUPLING_THROAT",
            "source_path": str(SOURCES["reduction_3506"]["path"]),
            "next_action": "prove no independent F2 counterterm from parent action",
            "valid_for_claim": "False",
        },
        {
            "row_id": "ARE3507_2_z_g",
            "residual": "z_g",
            "definition": "D_X ln current/charge normalization",
            "formula": "D_X ln g_J",
            "zero_condition": "fixed charge representation and readout functor",
            "observable_links": "charge_readout; matter_current; WEP; alpha_EM",
            "status": "CURRENT_OWNER_UNSIGNED",
            "source_path": str(SOURCES["alpha_owner_764"]["path"]),
            "next_action": "derive current normalization from quotient matter functor",
            "valid_for_claim": "False",
        },
        {
            "row_id": "ARE3507_3_z_lambda",
            "residual": "z_lambda",
            "definition": "D_X ln Maxwell kinetic normalization",
            "formula": "D_X ln lambda_A",
            "zero_condition": "fixed vertical generator norm/topological level/fibre metric",
            "observable_links": "alpha_EM; derivative_EM_force; clocks",
            "status": "KINETIC_OWNER_UNSIGNED",
            "source_path": str(SOURCES["vertical_norm_765"]["path"]),
            "next_action": "derive fixed N_Q or retain bound",
            "valid_for_claim": "False",
        },
        {
            "row_id": "ARE3507_4_dlnlambda_force",
            "residual": "dlnlambda_force",
            "definition": "derivative coupling from field-dependent canonical normalization",
            "formula": "dln(lambda_A) wedge A_c",
            "zero_condition": "d lambda_A=0 or projection/bound removes term",
            "observable_links": "PPN; clocks; EM_wave_propagation; local_force",
            "status": "DERIVATIVE_BOUND_REQUIRED_IF_UNSIGNED",
            "source_path": str(SOURCES["radiative_1051"]["path"]),
            "next_action": "derive local silence or add numeric bound row",
            "valid_for_claim": "False",
        },
    ]


def bound_input_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "ABIN3507_0_alpha_clock",
            "arena": "clock/spectroscopy",
            "residual": "b_alpha_X",
            "predicted_value": "MISSING_2zg_minus_zlambda",
            "predicted_units": "dimensionless_derivative_or_declared_scale",
            "bound_value": "MISSING_CLOCK_BOUND",
            "bound_units": "same_as_prediction",
            "source_path": str(SOURCES["clock_bound_1052"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "row_id": "ABIN3507_1_R10",
            "arena": "R10 short-range alpha product",
            "residual": "b_alpha_X or C_XF2 projection",
            "predicted_value": "MISSING_R10_PROJECTION",
            "predicted_units": "alpha_lambda_projection",
            "bound_value": "MISSING_REVIEWED_BOUND_ROW",
            "bound_units": "alpha_bound",
            "source_path": str(SOURCES["r10_bound_candidate"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "row_id": "ABIN3507_2_WEP",
            "arena": "WEP/source composition",
            "residual": "beta_source_alpha",
            "predicted_value": "MISSING_SOURCE_COMPOSITION_MAP",
            "predicted_units": "dimensionless",
            "bound_value": "MISSING_WEP_BOUND",
            "bound_units": "dimensionless",
            "source_path": str(SOURCES["alpha_contract_1055"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "row_id": "ABIN3507_3_derivative_lambda",
            "arena": "local PPN/EM force",
            "residual": "dlnlambda_force",
            "predicted_value": "MISSING_DLN_LAMBDA_PROFILE",
            "predicted_units": "inverse_length_or_projected_dimensionless",
            "bound_value": "MISSING_LOCAL_FORCE_BOUND",
            "bound_units": "same_as_prediction",
            "source_path": str(SOURCES["radiative_1051"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def parse_float(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def run_alpha_bound_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for row in rows:
        predicted = parse_float(str(row["predicted_value"]))
        bound = parse_float(str(row["bound_value"]))
        if row["valid_for_claim"] != "True":
            verdict = "BLOCKED_INPUT_NOT_VALID_FOR_CLAIM"
            passes = "False"
        elif predicted is None or bound is None or bound <= 0:
            verdict = "BLOCKED_MISSING_NUMERIC_PREDICTION_OR_BOUND"
            passes = "False"
        else:
            passes = bool_text(abs(predicted) <= bound)
            verdict = "PASS_NUMERIC_ALPHA_BOUND" if passes == "True" else "FAIL_NUMERIC_ALPHA_BOUND"
        results.append(
            {
                "row_id": row["row_id"].replace("ABIN", "ARUN"),
                "arena": row["arena"],
                "residual": row["residual"],
                "predicted_value": row["predicted_value"],
                "bound_value": row["bound_value"],
                "pass_condition": "abs(predicted_value) <= bound_value with sourced numeric rows",
                "runner_verdict": verdict,
                "passes_bound": passes,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return results


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3507_0_identity_derived",
            "decision": "The scalar EM coupling problem is now an exact product-rule residual, not a vague coupling worry.",
            "rationale": "alpha_eff is controlled by g_J^2/lambda_A, so the whole local EM leak is b_alpha_X=2D_X ln g_J-D_X ln lambda_A plus derivative-lambda force terms.",
            "effect": "Future derivations can attack z_g and z_lambda separately and cannot hide behind field-rescaling conventions.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3507_1_no_zero_claim",
            "decision": "Do not claim b_alpha_X=0 yet.",
            "rationale": "The same-owner relation between kinetic normalization, current normalization, clocks, masses, and source readout is still not parent-signed.",
            "effect": "Alpha/clock/WEP/R10 rows remain blocked until either derived or numerically sourced.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3507_2_best_next_target",
            "decision": "Go after the current/source normalization Ward identity next.",
            "rationale": "If J_Q is varied from the same matter functor that defines clocks and mass, z_g may be locked; then only z_lambda/generator norm remains.",
            "effect": "This is the cleanest derivation-first route toward local GR source universality.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3508-Y5-R2FR-current-source-normalization-Ward-identity-or-alpha-source-bound.md",
            "next_script": "scripts/Y5_R2FR_3508_current_source_normalization_Ward_identity_or_alpha_source_bound.py",
            "objective": "Derive whether J_Q, charge readout, matter clocks, and Hilbert source normalization are locked by one quotient matter functor; if not, fill alpha-source/WEP/R10 bound rows.",
            "success_gate": "Either z_g is forced to the same owner as matter/current readout, or beta_source_alpha gets numeric-ready bound inputs without claim flags.",
            "forbidden_shortcuts": "Do not choose a charge convention that fixes z_g while leaving source/current/mass readout independent.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    identities: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    bound_inputs: list[dict[str, Any]],
    runner_results: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    residual_names = {row["residual"] for row in residuals}
    identity_ids = {row["identity_id"] for row in identities}
    all_claim_false = all(
        row.get("valid_for_claim") == "False"
        for table in [sources, identities, gates, residuals, bound_inputs, runner_results, decisions, next_rows]
        for row in table
    )
    blocked_inputs = all("BLOCKED" in row["runner_verdict"] for row in runner_results)
    validation = [
        {
            "check_id": "VAL3507_0_sources_exist",
            "passed": bool_text(all(row["exists"] == "True" for row in sources)),
            "detail": "all cited local source paths exist",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL3507_1_canonical_identity_present",
            "passed": bool_text("ALPHA3507_0_canonical_normalization_identity" in identity_ids and "ALPHA3507_1_vertical_residual_law" in identity_ids),
            "detail": "alpha_eff and D_X ln alpha identities written",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL3507_2_required_residuals_present",
            "passed": bool_text({"b_alpha_X", "C_XF2", "z_g", "z_lambda", "dlnlambda_force"}.issubset(residual_names)),
            "detail": "scalar coupling residual vector complete",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL3507_3_bound_runner_blocks_placeholders",
            "passed": bool_text(blocked_inputs),
            "detail": "all alpha bound rows remain blocked until numeric sourced inputs exist",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL3507_4_no_claim_flags",
            "passed": bool_text(all_claim_false),
            "detail": "no 3507 output row is valid_for_claim=True",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL3507_5_next_target_current_Ward_identity",
            "passed": bool_text(
                next_rows[0]["next_doc"].startswith("3508")
                and ("Ward" in next_rows[0]["next_doc"] or "matter functor" in next_rows[0]["objective"])
            ),
            "detail": "current/source normalization selected as next derivation target",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL3507_6_formalization_workbench_not_targeted",
            "passed": bool_text(FORMALIZATION.exists() and str(DOC).startswith(str(ROOT))),
            "detail": str(FORMALIZATION),
            "valid_for_claim": "False",
        },
    ]
    validation.append(
        {
            "check_id": "VAL3507_SUMMARY",
            "passed": bool_text(all(row["passed"] == "True" for row in validation)),
            "detail": "PASS" if all(row["passed"] == "True" for row in validation) else "FAIL",
            "valid_for_claim": "False",
        }
    )
    return validation


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def write_doc(
    identities: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    bound_inputs: list[dict[str, Any]],
    runner_results: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 3507 - Scalar Gauge Coupling Owner: DX Lambda Zero Or Alpha Bound Runner",
                "",
                "## Summary",
                "- **Exact identity derived:** `alpha_eff` is controlled by the invariant ratio `g_J^2/lambda_A`, so `D_X ln alpha_eff = 2 D_X ln g_J - D_X ln lambda_A`.",
                "- **What this fixes:** the EM coupling problem is no longer vague; `C_XF2`, clock alpha drift, WEP/R10 alpha-source products, and source normalization all pass through `b_alpha_X` unless a separate derivative-lambda force is active.",
                "- **What still blocks the claim:** the same parent owner for kinetic normalization, current normalization, charge readout, clocks, and Hilbert source has not yet been derived.",
                "- **Next best move:** derive the current/source normalization Ward identity before chasing more observational rows.",
                "",
                "## Coupling Identities",
                markdown_table(
                    identities,
                    ["identity_id", "object", "statement", "mathematical_form", "remaining_residual", "status"],
                ),
                "",
                "## Parent Owner Gates",
                markdown_table(
                    gates,
                    ["gate_id", "gate", "required_signature", "mathematical_test", "current_status", "failure_mode"],
                ),
                "",
                "## Alpha Residual Vector",
                markdown_table(
                    residuals,
                    ["row_id", "residual", "definition", "formula", "zero_condition", "observable_links", "status"],
                ),
                "",
                "## Bound Input Template",
                markdown_table(
                    bound_inputs,
                    ["row_id", "arena", "residual", "predicted_value", "bound_value", "source_path", "valid_for_claim"],
                ),
                "",
                "## Runner Results",
                markdown_table(
                    runner_results,
                    ["row_id", "arena", "residual", "pass_condition", "runner_verdict", "passes_bound", "claim_allowed"],
                ),
                "",
                "## Decisions",
                markdown_table(decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"]),
                "",
                "## Next Target",
                markdown_table(
                    next_rows,
                    ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed"],
                ),
                "",
                "## Validation",
                markdown_table(validation_rows, ["check_id", "passed", "detail", "valid_for_claim"]),
                "",
                f"Generated: {now_utc()}",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    sources = source_register_rows()
    identities = coupling_identity_rows()
    gates = owner_gate_rows()
    residuals = alpha_residual_rows()
    bound_inputs = bound_input_rows()
    runner_results = run_alpha_bound_rows(bound_inputs)
    decisions = decision_rows()
    next_rows = next_target_rows()
    validation_rows = validate(sources, identities, gates, residuals, bound_inputs, runner_results, decisions, next_rows)

    write_csv(OUT / "P8_Y5_R2FR_3507_SOURCE_REGISTER.csv", sources, ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(
        OUT / "P8_Y5_R2FR_3507_ALPHA_COUPLING_IDENTITY.csv",
        identities,
        [
            "identity_id",
            "object",
            "statement",
            "derivation",
            "mathematical_form",
            "closes_if",
            "remaining_residual",
            "status",
            "source_path",
            "valid_for_claim",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3507_PARENT_OWNER_GATE.csv",
        gates,
        ["gate_id", "gate", "required_signature", "mathematical_test", "current_status", "failure_mode", "valid_for_claim"],
    )
    residual_fields = [
        "row_id",
        "residual",
        "definition",
        "formula",
        "zero_condition",
        "observable_links",
        "status",
        "source_path",
        "next_action",
        "valid_for_claim",
    ]
    write_csv(OUT / "P8_Y5_R2FR_3507_ALPHA_RESIDUAL_VECTOR.csv", residuals, residual_fields)
    write_csv(CANONICAL_ALPHA_RESIDUAL, residuals, residual_fields)
    write_csv(
        OUT / "P8_Y5_R2FR_3507_ALPHA_BOUND_INPUT_TEMPLATE.csv",
        bound_inputs,
        ["row_id", "arena", "residual", "predicted_value", "predicted_units", "bound_value", "bound_units", "source_path", "valid_for_claim"],
    )
    runner_fields = [
        "row_id",
        "arena",
        "residual",
        "predicted_value",
        "bound_value",
        "pass_condition",
        "runner_verdict",
        "passes_bound",
        "claim_allowed",
        "valid_for_claim",
    ]
    write_csv(OUT / "P8_Y5_R2FR_3507_ALPHA_BOUND_RUNNER_RESULTS.csv", runner_results, runner_fields)
    write_csv(OUT / "P8_EM_alpha_coupling_bound_runner_results.csv", runner_results, runner_fields)
    write_csv(
        OUT / "P8_Y5_R2FR_3507_DECISION_LEDGER.csv",
        decisions,
        ["decision_id", "decision", "rationale", "effect", "claim_allowed", "valid_for_claim"],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3507_NEXT_TARGET.csv",
        next_rows,
        ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"],
    )
    write_csv(OUT / "P8_Y5_BRR545_3507_VALIDATION.csv", validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(identities, gates, residuals, bound_inputs, runner_results, decisions, next_rows, validation_rows)


if __name__ == "__main__":
    main()
