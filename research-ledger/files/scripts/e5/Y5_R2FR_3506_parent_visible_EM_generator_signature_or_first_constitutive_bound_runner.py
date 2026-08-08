from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3506-Y5-R2FR-parent-visible-EM-generator-signature-or-first-constitutive-bound-runner.md"
RUNNER_RESULTS = OUT / "P8_EM_first_constitutive_bound_runner_results.csv"

SOURCES: dict[str, dict[str, Any]] = {
    "script_3506": {"path": Path(__file__).resolve(), "role": "generator"},
    "doc_3505": {
        "path": ROOT / "3505-Y5-R2FR-visible-EM-action-domain-exhaustion-no-chiEM-no-hidden-Hodge-or-bound.md",
        "role": "3505 action-domain theorem handoff",
    },
    "theorem_3505": {
        "path": OUT / "P8_Y5_R2FR_3505_VISIBLE_EM_ACTION_DOMAIN_THEOREM.csv",
        "role": "3505 visible EM theorem table",
    },
    "bound_3505": {
        "path": OUT / "P8_EM_visible_action_domain_exhaustion_no_chiEM_bound_vector.csv",
        "role": "3505 visible EM residual vector",
    },
    "maxwell_inheritance": {
        "path": OUT / "P8_Y5_R10_765_MAXWELL_KINETIC_INHERITANCE_GATE.csv",
        "role": "Maxwell kinetic inheritance gate",
    },
    "unique_maxwell_1057": {
        "path": ROOT / "1057-Y5-R10-unique-Maxwell-subblock-no-independent-F2-ban-or-balpha-retention.md",
        "role": "unique Maxwell subblock/no independent F2 attempt",
    },
    "operator_domain_1058": {
        "path": ROOT / "1058-Y5-R10-visible-operator-domain-exhaustion-or-alpha-counterterm-prior.md",
        "role": "visible operator-domain exhaustion attempt",
    },
    "hodge_3504": {
        "path": OUT / "P8_EM_Hodge_flow_rule_bound_or_zero.csv",
        "role": "3504 Hodge flow residual vector",
    },
    "readout_2637": {
        "path": OUT / "P8_Y5_READOUT_EREADOUT_CERTIFICATE_2637_CONDITIONAL_READOUT_LEMMA.csv",
        "role": "readout-after-variation lemma",
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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


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


def generator_signature_rows() -> list[dict[str, Any]]:
    return [
        {
            "signature_id": "GEN3506_0_visible_U1_connection",
            "object": "A_Q",
            "parent_requirement": "The visible EM variable is a quotient-visible U(1) connection on the observed bundle.",
            "derivation_attempt": "Gauge invariance and locality force the kinetic variable to be the curvature F_Q=dA_Q; A_Q itself can appear only through the conserved source pairing A_Q.J_Q plus boundary/gauge fixing.",
            "mathematical_form": "A_Q in Omega^1(M_Q,u(1)); F_Q=dA_Q; dJ_Q=0",
            "closes_coefficients": "readout counterterms only if A_Q is the observed connection, not a reduced-action proxy",
            "residual_if_unsigned": "C_Hodge_readout; C_JQ; source-normalization leakage",
            "status": "DERIVED_CONDITIONAL_ON_VISIBLE_U1_OWNER",
            "source_path": str(SOURCES["maxwell_inheritance"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "signature_id": "GEN3506_1_no_extra_tensor_domain",
            "object": "Args(S_EM)",
            "parent_requirement": "The parent visible EM action has no argument slot beyond {A_Q,F_Q,e_obs(q),orientation,theta_rep,fixed constants}.",
            "derivation_attempt": "Once the action arguments are exhausted, independent chi_EM, hidden/disformal Hodge maps and medium/readout tensors are absent by type rather than tuned small.",
            "mathematical_form": "Args(S_EM) cap {chi_EM,g_hidden,f_H(Phi),chi_readout}=empty",
            "closes_coefficients": "Delta_chi_principal; C_Hodge_hidden; C_Hodge_readout",
            "residual_if_unsigned": "hidden Hodge or independent constitutive tensor remains legal",
            "status": "EXACT_IF_PARENT_DOMAIN_SIGNED",
            "source_path": str(SOURCES["theorem_3505"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "signature_id": "GEN3506_2_Lorentz_natural_quadratic_block",
            "object": "chi_EM principal block",
            "parent_requirement": "The only local tensors available to the visible quadratic EM kinetic term are e_obs(q), orientation and constants.",
            "derivation_attempt": "A local quadratic two-form action natural under the observed frame has only F_Q wedge *_obs F_Q and F_Q wedge F_Q as Lorentz-scalar four-forms. Any anisotropic principal chi requires an extra tensor slot.",
            "mathematical_form": "S_kin = -lambda_A/2 int F_Q wedge *_obs F_Q + theta_A/2 int F_Q wedge F_Q",
            "closes_coefficients": "Delta_chi_principal except scalar lambda_A and topological/axion theta_A",
            "residual_if_unsigned": "Delta_chi_principal; Delta_chi_axion_gradient; C_XF2",
            "status": "DERIVED_IF_NATURALITY_AND_NO_EXTRA_TENSOR_SIGNED",
            "source_path": str(SOURCES["unique_maxwell_1057"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "signature_id": "GEN3506_3_action_reciprocity_skewon_zero",
            "object": "Delta_chi_skewon",
            "parent_requirement": "The local visible EM response is generated by a reciprocal conservative action, not by a dissipative medium law inserted after variation.",
            "derivation_attempt": "The skewon part is antisymmetric in the pair exchange needed for a quadratic Lagrangian bilinear; it contributes to response laws but not to a symmetric local action Hessian.",
            "mathematical_form": "delta^2 S_EM / delta F_I delta F_J = delta^2 S_EM / delta F_J delta F_I => chi_skewon=0",
            "closes_coefficients": "Delta_chi_skewon",
            "residual_if_unsigned": "dissipative/readout medium counterbranch",
            "status": "ZERO_IF_RECIPROCAL_ACTION_SIGNED",
            "source_path": str(SOURCES["hodge_3504"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "signature_id": "GEN3506_4_constant_axion_or_absent_pseudoscalar",
            "object": "theta_A",
            "parent_requirement": "The parent action has no quotient-visible pseudoscalar that can vary the coefficient of F_Q wedge F_Q.",
            "derivation_attempt": "A constant theta_A is a boundary/topological term in local source-free Maxwell variation; only dtheta_A acts as a physical axion-gradient residual.",
            "mathematical_form": "d theta_A = 0 => delta int theta_A F_Q wedge F_Q is boundary",
            "closes_coefficients": "Delta_chi_axion_gradient",
            "residual_if_unsigned": "polarization rotation/effective-current residual",
            "status": "ZERO_IF_NO_VISIBLE_PSEUDOSCALAR_SIGNED",
            "source_path": str(SOURCES["bound_3505"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "signature_id": "GEN3506_5_scalar_gauge_kinetic_owner",
            "object": "lambda_A or e_obs normalization",
            "parent_requirement": "The scalar prefactor of F_Q wedge *_obs F_Q is a fixed parent constant or is locked to the same charge/current normalization used by matter clocks.",
            "derivation_attempt": "Lorentz/gauge/naturality do not remove a scalar multiplier. If it is field-dependent, it is exactly the alpha/current/source coupling channel the local branch has been missing.",
            "mathematical_form": "lambda_A(q)=const or D_X ln(lambda_A/e_obs^2)=0",
            "closes_coefficients": "C_XF2; Delta_conformal_scale; w_EM only if source normalization also closes",
            "residual_if_unsigned": "alpha_EM drift, WEP/R10/clock/source-normalization leakage",
            "status": "NOT_DERIVED_CORE_COUPLING_TARGET",
            "source_path": str(SOURCES["operator_domain_1058"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "signature_id": "GEN3506_6_rank_reduction_verdict",
            "object": "visible EM residual vector",
            "parent_requirement": "Combine visible U(1), no-extra-tensor domain, Lorentz naturality, reciprocal action, no visible pseudoscalar and fixed scalar coupling.",
            "derivation_attempt": "The 3505 vector is not random anymore: the principal/skewon/hidden/readout pieces collapse if the generator signature is signed, leaving the hard scalar coupling and axion/source-normalization owners as the real frontier.",
            "mathematical_form": "Delta_Hodge_EM -> {D_X ln lambda_A, dtheta_A, C_hidden if domain unsigned, C_readout if readout unsigned}",
            "closes_coefficients": "organizes the EM branch into exact zeros versus two parent-owned coupling residues",
            "residual_if_unsigned": "no claim-grade local GR/Maxwell pass",
            "status": "FRONTIER_SHARPENED_NOT_CLAIMED",
            "source_path": str(SOURCES["bound_3505"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def residual_reduction_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "RED3506_0_Delta_chi_principal",
            "coefficient": "Delta_chi_principal",
            "3505_status": "RETAINED_BOUND_COMPONENT",
            "3506_result": "conditional zero of anisotropic principal part",
            "proof_or_bound_rule": "Lorentz-natural quadratic two-form action from e_obs has only F wedge *_obs F plus F wedge F; anisotropic chi needs an extra tensor.",
            "remaining_owner": "scalar lambda_A and axion theta_A",
            "observable_gate": "vacuum_birefringence; light_cone; Shapiro/lensing consistency",
            "claim_allowed": "False",
        },
        {
            "row_id": "RED3506_1_Delta_chi_skewon",
            "coefficient": "Delta_chi_skewon",
            "3505_status": "RETAINED_BOUND_COMPONENT",
            "3506_result": "conditional zero from reciprocal local action Hessian",
            "proof_or_bound_rule": "A skewon is not generated by a symmetric quadratic action Hessian; it re-enters only as medium/readout/dissipation.",
            "remaining_owner": "readout-after-variation and non-conservative branch exclusion",
            "observable_gate": "dispersion; polarization; Poynting flux nonconservation",
            "claim_allowed": "False",
        },
        {
            "row_id": "RED3506_2_Delta_chi_axion_gradient",
            "coefficient": "Delta_chi_axion_gradient",
            "3505_status": "RETAINED_BOUND_COMPONENT",
            "3506_result": "constant axion is harmless, gradient remains",
            "proof_or_bound_rule": "F wedge F is a total derivative only when theta_A is constant; dtheta_A is a physical effective current.",
            "remaining_owner": "no visible pseudoscalar or sourced dtheta_A bound",
            "observable_gate": "polarization_rotation; effective_current; spectroscopy",
            "claim_allowed": "False",
        },
        {
            "row_id": "RED3506_3_C_Hodge_hidden",
            "coefficient": "C_Hodge_hidden",
            "3505_status": "RETAINED_BOUND_COMPONENT",
            "3506_result": "zero only if the parent generator has no hidden tensor slot",
            "proof_or_bound_rule": "No-extra-tensor action grammar excludes hidden/disformal Hodge maps by type; ordinary covariance alone does not.",
            "remaining_owner": "parent-visible generator signature",
            "observable_gate": "preferred_frame; light_speed_anisotropy; clock",
            "claim_allowed": "False",
        },
        {
            "row_id": "RED3506_4_C_Hodge_readout",
            "coefficient": "C_Hodge_readout",
            "3505_status": "RETAINED_BOUND_COMPONENT",
            "3506_result": "zero only if observables are read after variation using the same A_Q,e_obs pair",
            "proof_or_bound_rule": "Reduced-action/readout medium branches can fake a Hodge shift unless readout is explicitly outside the variational domain.",
            "remaining_owner": "readout-domain certificate",
            "observable_gate": "clock; spectroscopy; alpha_EM; binding_response",
            "claim_allowed": "False",
        },
        {
            "row_id": "RED3506_5_C_XF2",
            "coefficient": "C_XF2",
            "3505_status": "RETAINED_BOUND_COMPONENT",
            "3506_result": "not killed by symmetry; becomes the core scalar coupling problem",
            "proof_or_bound_rule": "Gauge/Lorentz/naturality allow lambda_A F wedge *F. It must be parent-fixed, derived from charge normalization, or empirically bounded.",
            "remaining_owner": "D_X ln lambda_A or D_X ln(lambda_A/e_obs^2)",
            "observable_gate": "alpha_EM; WEP; R10; clock; source_normalization",
            "claim_allowed": "False",
        },
        {
            "row_id": "RED3506_6_Delta_conformal_scale",
            "coefficient": "Delta_conformal_scale",
            "3505_status": "SEPARATE_SCALE_GATE_RETAINED",
            "3506_result": "not visible in 4D source-free Maxwell kinetic; must be fixed by matter/current/clocks",
            "proof_or_bound_rule": "The 4D Hodge star on two-forms is conformally invariant, so light propagation alone cannot set the scale.",
            "remaining_owner": "mass/current/clock normalization",
            "observable_gate": "clock_redshift; source_normalization; alpha_EM; Newton_G",
            "claim_allowed": "False",
        },
    ]


def bound_input_template_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for reduction in residual_reduction_rows():
        coefficient = reduction["coefficient"]
        rows.append(
            {
                "row_id": reduction["row_id"].replace("RED", "BIN"),
                "coefficient": coefficient,
                "reduced_owner": reduction["remaining_owner"],
                "predicted_value": "MISSING_PARENT_COEFFICIENT",
                "predicted_units": "dimensionless_or_declared_by_owner",
                "bound_value": "MISSING_OBSERVATIONAL_BOUND",
                "bound_units": "dimensionless_or_declared_by_arena",
                "arena": reduction["observable_gate"],
                "parent_source_path": str(SOURCES["bound_3505"]["path"]),
                "bound_source_path": "MISSING_SOURCE_PATH",
                "valid_for_claim": "False",
            }
        )
    return rows


def parse_float(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def run_bound_rows(input_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output_rows: list[dict[str, Any]] = []
    for row in input_rows:
        predicted = parse_float(str(row["predicted_value"]))
        bound = parse_float(str(row["bound_value"]))
        valid_input = row["valid_for_claim"] == "True"
        source_ok = row["bound_source_path"] != "MISSING_SOURCE_PATH"
        numeric_ok = predicted is not None and bound is not None and bound > 0
        if not valid_input:
            verdict = "BLOCKED_INPUT_NOT_VALID_FOR_CLAIM"
            passes = "False"
        elif not source_ok:
            verdict = "BLOCKED_MISSING_BOUND_SOURCE"
            passes = "False"
        elif not numeric_ok:
            verdict = "BLOCKED_MISSING_NUMERIC_VALUES"
            passes = "False"
        else:
            passes = bool_text(abs(predicted) <= bound)
            verdict = "PASS_NUMERIC_BOUND" if passes == "True" else "FAIL_NUMERIC_BOUND"
        output_rows.append(
            {
                "row_id": row["row_id"].replace("BIN", "BRUN"),
                "coefficient": row["coefficient"],
                "predicted_value": row["predicted_value"],
                "bound_value": row["bound_value"],
                "arena": row["arena"],
                "pass_condition": "abs(predicted_value) <= bound_value with sourced numeric rows",
                "runner_verdict": verdict,
                "passes_bound": passes,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return output_rows


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3506_0_real_progress",
            "decision": "Do not treat the EM branch as a shapeless missing list anymore.",
            "rationale": "3506 gives an actual reduction theorem: visible U(1)+observed coframe+naturality+reciprocal action collapses the principal/skewon chaos to Maxwell plus scalar coupling and possible axion/source/readout owners.",
            "effect": "Next derivation should hunt the scalar coupling owner, not re-audit every EM coefficient from scratch.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3506_1_no_public_claim",
            "decision": "No local-GR/Maxwell pass is claimed from 3506.",
            "rationale": "The parent has not yet signed no-extra-tensor domain, fixed lambda_A, no dtheta_A, and readout/source normalization.",
            "effect": "Bound runner remains smoke-ready with placeholder rows blocked.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3506_2_best_next_target",
            "decision": "Attack the scalar gauge coupling owner directly.",
            "rationale": "C_XF2/lambda_A is the surviving coupling throat that can feed alpha_EM, WEP/R10, clocks, and source mass normalization.",
            "effect": "Move to deriving D_X ln(lambda_A/e_obs^2)=0 or producing first numeric alpha/coupling bound rows.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3507-Y5-R2FR-scalar-gauge-coupling-owner-DXlambda-zero-or-alpha-bound-runner.md",
            "next_script": "scripts/Y5_R2FR_3507_scalar_gauge_coupling_owner_DXlambda_zero_or_alpha_bound_runner.py",
            "objective": "Try to derive the scalar gauge coupling owner D_X ln(lambda_A/e_obs^2)=0 from parent charge/current normalization; if not, create first numeric-ready alpha_EM/WEP/R10/clock bound rows.",
            "success_gate": "Either lambda_A is parent-fixed by the same quotient source normalization as matter, or every surviving alpha/coupling row has a sourced arena and remains non-claim until numeric.",
            "forbidden_shortcuts": "Do not set lambda_A constant by convention if charge/current/mass normalization still moves.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    signatures: list[dict[str, Any]],
    reductions: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    required_coefficients = {
        "Delta_chi_principal",
        "Delta_chi_skewon",
        "Delta_chi_axion_gradient",
        "C_Hodge_hidden",
        "C_Hodge_readout",
        "C_XF2",
        "Delta_conformal_scale",
    }
    reduced_coefficients = {row["coefficient"] for row in reductions}
    runner_coefficients = {row["coefficient"] for row in runners}
    all_claim_false = all(row.get("valid_for_claim") == "False" for table in [sources, signatures, inputs, runners, decisions, next_rows] for row in table)
    blocked_placeholders = all("BLOCKED" in row["runner_verdict"] for row in runners)
    scalar_target_present = any(row["coefficient"] == "C_XF2" and "scalar coupling" in row["3506_result"] for row in reductions)
    validation = [
        {
            "check_id": "VAL3506_0_sources_exist",
            "passed": bool_text(all(row["exists"] == "True" for row in sources)),
            "detail": "all cited local source paths exist",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL3506_1_signature_rows_present",
            "passed": bool_text(len(signatures) >= 7),
            "detail": f"{len(signatures)} generator-signature rows written",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL3506_2_required_coefficients_reduced",
            "passed": bool_text(required_coefficients.issubset(reduced_coefficients)),
            "detail": ";".join(sorted(required_coefficients - reduced_coefficients)) or "all required coefficients mapped",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL3506_3_bound_runner_covers_required_coefficients",
            "passed": bool_text(required_coefficients.issubset(runner_coefficients)),
            "detail": ";".join(sorted(required_coefficients - runner_coefficients)) or "runner covers all required coefficients",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL3506_4_placeholder_rows_block_claim",
            "passed": bool_text(blocked_placeholders),
            "detail": "all template rows remain blocked until numeric parent and bound sources exist",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL3506_5_no_claim_flags",
            "passed": bool_text(all_claim_false),
            "detail": "no 3506 output row is valid_for_claim=True",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL3506_6_scalar_coupling_frontier_selected",
            "passed": bool_text(scalar_target_present and next_rows[0]["next_doc"].startswith("3507")),
            "detail": "C_XF2/lambda_A selected as next coupling throat",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL3506_7_formalization_workbench_not_targeted",
            "passed": bool_text(FORMALIZATION.exists() and str(DOC).startswith(str(ROOT))),
            "detail": str(FORMALIZATION),
            "valid_for_claim": "False",
        },
    ]
    validation.append(
        {
            "check_id": "VAL3506_SUMMARY",
            "passed": bool_text(all(row["passed"] == "True" for row in validation)),
            "detail": "PASS" if all(row["passed"] == "True" for row in validation) else "FAIL",
            "valid_for_claim": "False",
        }
    )
    return validation


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _ in fields) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join([header, separator, *body])


def write_doc(
    signatures: list[dict[str, Any]],
    reductions: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 3506 - Parent Visible EM Generator Signature Or First Constitutive Bound Runner",
                "",
                "## Summary",
                "- **Actual derivation gain:** if the visible EM field is a quotient U(1) connection and the only visible tensors are `e_obs(q)` plus orientation, the local reciprocal quadratic action is forced to the Maxwell block plus scalar `lambda_A` and possible topological/axion `theta_A`.",
                "- **Residual vector reduced:** principal anisotropy and skewon pieces are no longer equally mysterious; they are conditional zeros under visible naturality/reciprocity. The hard throat is now the scalar coupling/source-normalization owner.",
                "- **Still not claim-grade:** the parent action has not yet signed no-extra-tensor domain, fixed `lambda_A`, no `dtheta_A`, and readout/source normalization, so all rows remain private/non-claim.",
                "- **Executable bound path:** a first constitutive-bound runner now exists; placeholder rows intentionally block until numeric parent coefficients and sourced arena bounds are supplied.",
                "",
                "## Generator Signature Attempt",
                markdown_table(
                    signatures,
                    [
                        "signature_id",
                        "object",
                        "parent_requirement",
                        "derivation_attempt",
                        "status",
                        "valid_for_claim",
                    ],
                ),
                "",
                "## Residual Reduction Map",
                markdown_table(
                    reductions,
                    [
                        "row_id",
                        "coefficient",
                        "3506_result",
                        "proof_or_bound_rule",
                        "remaining_owner",
                        "claim_allowed",
                    ],
                ),
                "",
                "## Bound Input Template",
                markdown_table(
                    inputs,
                    [
                        "row_id",
                        "coefficient",
                        "reduced_owner",
                        "predicted_value",
                        "bound_value",
                        "arena",
                        "valid_for_claim",
                    ],
                ),
                "",
                "## Runner Results",
                markdown_table(
                    runners,
                    [
                        "row_id",
                        "coefficient",
                        "pass_condition",
                        "runner_verdict",
                        "passes_bound",
                        "claim_allowed",
                    ],
                ),
                "",
                "## Decisions",
                markdown_table(decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"]),
                "",
                "## Next Target",
                markdown_table(
                    next_rows,
                    [
                        "next_doc",
                        "next_script",
                        "objective",
                        "success_gate",
                        "forbidden_shortcuts",
                        "claim_allowed",
                    ],
                ),
                "",
                "## Validation",
                markdown_table(validation, ["check_id", "passed", "detail", "valid_for_claim"]),
                "",
                f"Generated: {now_utc()}",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    sources = source_register_rows()
    signatures = generator_signature_rows()
    reductions = residual_reduction_rows()
    inputs = bound_input_template_rows()
    runners = run_bound_rows(inputs)
    decisions = decision_rows()
    next_rows = next_target_rows()
    validation_rows = validate(sources, signatures, reductions, inputs, runners, decisions, next_rows)

    write_csv(OUT / "P8_Y5_R2FR_3506_SOURCE_REGISTER.csv", sources, ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(
        OUT / "P8_Y5_R2FR_3506_PARENT_VISIBLE_EM_GENERATOR_SIGNATURE.csv",
        signatures,
        [
            "signature_id",
            "object",
            "parent_requirement",
            "derivation_attempt",
            "mathematical_form",
            "closes_coefficients",
            "residual_if_unsigned",
            "status",
            "source_path",
            "valid_for_claim",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3506_RESIDUAL_REDUCTION_MAP.csv",
        reductions,
        [
            "row_id",
            "coefficient",
            "3505_status",
            "3506_result",
            "proof_or_bound_rule",
            "remaining_owner",
            "observable_gate",
            "claim_allowed",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3506_CONSTITUTIVE_BOUND_INPUT_TEMPLATE.csv",
        inputs,
        [
            "row_id",
            "coefficient",
            "reduced_owner",
            "predicted_value",
            "predicted_units",
            "bound_value",
            "bound_units",
            "arena",
            "parent_source_path",
            "bound_source_path",
            "valid_for_claim",
        ],
    )
    runner_fields = [
        "row_id",
        "coefficient",
        "predicted_value",
        "bound_value",
        "arena",
        "pass_condition",
        "runner_verdict",
        "passes_bound",
        "claim_allowed",
        "valid_for_claim",
    ]
    write_csv(OUT / "P8_Y5_R2FR_3506_CONSTITUTIVE_BOUND_RUNNER_RESULTS.csv", runners, runner_fields)
    write_csv(RUNNER_RESULTS, runners, runner_fields)
    write_csv(
        OUT / "P8_Y5_R2FR_3506_DECISION_LEDGER.csv",
        decisions,
        ["decision_id", "decision", "rationale", "effect", "claim_allowed", "valid_for_claim"],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3506_NEXT_TARGET.csv",
        next_rows,
        ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"],
    )
    write_csv(OUT / "P8_Y5_BRR545_3506_VALIDATION.csv", validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(signatures, reductions, inputs, runners, decisions, next_rows, validation_rows)


if __name__ == "__main__":
    main()
