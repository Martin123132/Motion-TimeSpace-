from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MTS_DIR = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "630-Y5-R10-cg-projection-parent-input-derivation-or-source-prior-envelope.md"
SCRIPT = ROOT / "scripts" / "Y5_R10_cg_projection_parent_input_derivation_or_source_prior_envelope.py"

STATUS = "Y5_R10_coupling_derivation_gate_built_cg_zero_not_proven_finite_projection_envelope_written"
CLAIM_CEILING = "coupling_derivation_checkpoint_only_no_R10_WEP_PPN_clock_or_local_GR_pass"
NEXT_TARGET = "631-Y5-R10-matter-frame-variation-cg-zero-or-source-test-charge-law.md"

PRIOR_629_DOC = ROOT / "629-Y5-R10-R10-bound-curve-digitization-or-cg-projection-smoke-runner.md"
PRIOR_629_VALIDATION = MTS_DIR / "P8_Y5_BRR545_629_VALIDATION.csv"
PRIOR_629_PRESSURE = MTS_DIR / "P8_Y5_R10_629_REVIEW_CURVE_PRESSURE_SAMPLES.csv"
PRIOR_629_CONTRACT = MTS_DIR / "P8_Y5_R10_629_CG_PROJECTION_CONTRACT.csv"
PRIOR_628_DOC = ROOT / "628-Y5-R10-real-local-bound-input-sources-for-cg-or-Zcg-proof.md"
PRIOR_627_DOC = ROOT / "627-Y5-R10-cg-bound-source-acquisition-or-local-geometry-zero-proof.md"
PRIOR_627_ZERO_AUDIT = MTS_DIR / "P8_Y5_R10_627_ZERO_PROOF_AUDIT.csv"
PRIOR_627_ACQUISITION = MTS_DIR / "P8_Y5_R10_627_CG_ACQUISITION_LEDGER.csv"
PRIOR_626_DOC = ROOT / "626-Y5-R10-quotient-invariant-matter-action-signature-or-cg-bound-input.md"
PRIOR_625_DOC = ROOT / "625-Y5-R10-no-representative-Weyl-disformal-coupling-or-cg-prior.md"

SOURCE_REGISTER = MTS_DIR / "P8_Y5_R10_630_SOURCE_REGISTER.csv"
ZERO_AUDIT = MTS_DIR / "P8_Y5_R10_630_ZERO_COUPLING_THEOREM_AUDIT.csv"
FINITE_DERIVATION = MTS_DIR / "P8_Y5_R10_630_FINITE_COUPLING_DERIVATION.csv"
PARENT_INPUT_TARGETS = MTS_DIR / "P8_Y5_R10_630_PARENT_INPUT_TARGETS.csv"
PRESSURE_ENVELOPE = MTS_DIR / "P8_Y5_R10_630_R10_PRODUCT_PRESSURE_ENVELOPE.csv"
COUPLING_AMBIGUITY = MTS_DIR / "P8_Y5_R10_630_SCALAR_COUPLING_AMBIGUITY_LEDGER.csv"
NEXT_CONTRACT = MTS_DIR / "P8_Y5_R10_630_NEXT_DERIVATION_CONTRACT.csv"
NONCLAIM_SUMMARY = MTS_DIR / "P8_Y5_R10_630_NONCLAIM_SUMMARY.csv"
DECISION = MTS_DIR / "P8_Y5_BRR545_630_DECISION.csv"
ROUTE_UPDATE = MTS_DIR / "P8_Y5_BRR545_630_ROUTE_UPDATE.csv"
VALIDATION = MTS_DIR / "P8_Y5_BRR545_630_VALIDATION.csv"


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
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
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def parse_float(value: Any) -> float | None:
    try:
        parsed = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def is_true(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (PRIOR_629_DOC, "immediate R10 c_g projection smoke runner"),
        (PRIOR_629_VALIDATION, "629 validation gate"),
        (PRIOR_629_PRESSURE, "review-candidate R10 pressure samples"),
        (PRIOR_629_CONTRACT, "c_g projection contract from 629"),
        (PRIOR_628_DOC, "real local bound source acquisition"),
        (PRIOR_627_DOC, "c_g zero-proof attempt and acquisition ledger"),
        (PRIOR_627_ZERO_AUDIT, "prior zero-proof clause audit"),
        (PRIOR_627_ACQUISITION, "prior c_g/tau acquisition ledger"),
        (PRIOR_626_DOC, "quotient-invariant matter action signature attempt"),
        (PRIOR_625_DOC, "representative Weyl/disformal exclusion attempt"),
        (SCRIPT, "this checkpoint generator"),
    ]
    return [
        {
            "source_id": f"SRC630_{index}",
            "source_path": rel(path),
            "exists": bool_text(path.exists()),
            "role": role,
            "valid_for_claim": "false",
        }
        for index, (path, role) in enumerate(sources)
    ]


def zero_coupling_theorem_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "ZC630_0_parent_matter_frame",
            "zero_clause": "matter frame depends only on quotient geometry",
            "formal_condition": "g_m = g_m[q(Phi), Psi_m, theta] with no representative X dependence",
            "derivation_status": "not_parent_signed",
            "if_signed": "partial_X S_matter = 0 and c_g=0 follows at the matter-frame level",
            "if_unsigned": "representative common-frame leakage remains possible",
            "supports_cg_zero": "necessary_not_sufficient",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "ZC630_1_vertical_generator",
            "zero_clause": "local residual X is vertical in the quotient fibre",
            "formal_condition": "Dq[v_X]=0 on the local matter branch before variation",
            "derivation_status": "conditional_not_parent_signed",
            "if_signed": "X shifts are gauge/representative changes, not matter charges",
            "if_unsigned": "X can remain a physical scalar/local geometric datum",
            "supports_cg_zero": "necessary_not_sufficient",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "ZC630_2_action_descent",
            "zero_clause": "matter action descends to the quotient",
            "formal_condition": "Lie_vX S_matter = 0 up to owned gauge/boundary terms",
            "derivation_status": "not_parent_signed",
            "if_signed": "test and source legs both vanish for vertical X",
            "if_unsigned": "c_g must be derived or bounded as a physical coupling",
            "supports_cg_zero": "central_clause",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "ZC630_3_no_representative_weyl_disformal",
            "zero_clause": "no fixed representative Weyl/disformal matter coefficient",
            "formal_condition": "A_g(X), B_g(X), and disformal Pi terms are absent, quotient-owned, or auxiliary",
            "derivation_status": "not_parent_signed",
            "if_signed": "no hidden c_g re-enters through rods/clocks",
            "if_unsigned": "c_g or disformal residue can reappear in local tests",
            "supports_cg_zero": "necessary_not_sufficient",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "ZC630_4_boundary_projection_silence",
            "zero_clause": "vertical boundary/exact terms have zero R10/local projection",
            "formal_condition": "boundary contribution to Lie_vX S_matter has no source/test observable leg",
            "derivation_status": "not_parent_signed",
            "if_signed": "edge terms cannot fake a finite R10 coupling",
            "if_unsigned": "boundary/non-Hilbert residual can source a finite projection",
            "supports_cg_zero": "necessary_not_sufficient",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "ZC630_5_zero_verdict",
            "zero_clause": "c_g=0 theorem",
            "formal_condition": "ZC630_0..ZC630_4 jointly signed by parent action",
            "derivation_status": "not_proven",
            "if_signed": "alpha_MTS_R10(lambda)=0 for all lambda and local GR route gets a serious boost",
            "if_unsigned": "finite projection envelope is required",
            "supports_cg_zero": "false",
            "valid_for_claim": "false",
        },
    ]


def finite_coupling_derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "FD630_0_matter_frame_expansion",
            "derivation_step": "Introduce local representative matter-frame response",
            "equation": "g_m = A_g(X)^2 g_q + disformal_terms; A_g(X)=1+c_g Xhat+O(Xhat^2)",
            "meaning": "c_g is the first derivative of the matter-frame scale with respect to the normalized local residual mode",
            "status": "conditional_definition_not_parent_value",
            "needed_parent_input": "matter frame functional A_g or proof A_g independent of Xhat",
            "valid_for_claim": "false",
        },
        {
            "step_id": "FD630_1_source_test_current",
            "derivation_step": "Vary the matter action with respect to Xhat",
            "equation": "delta S_matter/delta Xhat = c_g tau_A T_matter + disformal/current terms",
            "meaning": "ordinary nonrelativistic matter sources the residual through its trace unless descent kills the derivative",
            "status": "conditional_projection_form",
            "needed_parent_input": "source and test current normalization plus tau_A for each arena",
            "valid_for_claim": "false",
        },
        {
            "step_id": "FD630_2_static_mode_equation",
            "derivation_step": "Linearize the residual mode around the local vacuum",
            "equation": "Z_eff (nabla^2 - lambda_X^-2) Xhat = -J_X",
            "meaning": "Z_eff and lambda_X set the strength/range of any local Yukawa-like exchange",
            "status": "conditional_linear_response",
            "needed_parent_input": "Z_eff, M_X^2, lambda_X=sqrt(Z_eff/M_X^2), source current J_X",
            "valid_for_claim": "false",
        },
        {
            "step_id": "FD630_3_green_function_projection",
            "derivation_step": "Solve the static Green-function response",
            "equation": "Xhat(r) proportional to J_X exp(-r/lambda_X)/(4 pi Z_eff r)",
            "meaning": "the residual appears as a finite-range Yukawa correction if its source/test legs survive",
            "status": "formal_shape_derived_inputs_missing",
            "needed_parent_input": "apparatus/source profile Qbar_XH(lambda;lambda_X) and boundary condition",
            "valid_for_claim": "false",
        },
        {
            "step_id": "FD630_4_observable_alpha_linear_product",
            "derivation_step": "Match the response to the R10 Yukawa alpha convention",
            "equation": "alpha_MTS_R10(lambda)=abs(c_g tau_R10(lambda) K_X Qbar_XH(lambda;lambda_X) qbar_XT/Z_eff)",
            "meaning": "this is the previous linear-product formula if source-leg physics is already absorbed into K_X Qbar_XH qbar_XT",
            "status": "derived_as_contract_not_numeric",
            "needed_parent_input": "c_g,tau_R10,K_X,Qbar_XH,qbar_XT,Z_eff,lambda_X",
            "valid_for_claim": "false",
        },
        {
            "step_id": "FD630_5_observable_alpha_two_leg_branch",
            "derivation_step": "Keep source and test legs separate",
            "equation": "alpha_MTS_R10(lambda)=abs(beta_source(lambda) beta_test(lambda))/(4 pi G_eff Z_eff) times profile factors",
            "meaning": "if c_g controls both source and test legs then the bound pressures c_g squared, not c_g linearly",
            "status": "ambiguity_explicit",
            "needed_parent_input": "whether c_g is a one-leg readout coefficient or a universal two-leg matter coupling",
            "valid_for_claim": "false",
        },
        {
            "step_id": "FD630_6_claim_gate",
            "derivation_step": "Score against R10 only after both theory and bound rows are promoted",
            "equation": "abs(alpha_MTS_R10(lambda_i)) <= alpha_bound(lambda_i) for every source-backed lambda_i",
            "meaning": "629 pressure samples are coefficient targets, not evidence of a pass",
            "status": "blocked_for_claim",
            "needed_parent_input": "physical alpha rows plus promoted source-backed R10 curve",
            "valid_for_claim": "false",
        },
    ]


def parent_input_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "PI630_0_c_g",
            "symbol": "c_g",
            "definition": "d ln A_g/dXhat at the local vacuum, or zero by quotient descent",
            "units": "dimensionless",
            "current_status": "unsourced",
            "required_derivation": "vary the parent matter frame with respect to the local residual representative",
            "failure_if_missing": "no R10/PPN/clock/orbital coupling can be scored",
            "valid_for_claim": "false",
        },
        {
            "input_id": "PI630_1_tau_R10",
            "symbol": "tau_R10(lambda)",
            "definition": "dimensionless source/test projection for Eot-Wash geometry and material response",
            "units": "dimensionless",
            "current_status": "unsourced",
            "required_derivation": "map local residual current into the R10 Yukawa-alpha observable",
            "failure_if_missing": "R10 data cannot be used as a physical MTS test",
            "valid_for_claim": "false",
        },
        {
            "input_id": "PI630_2_K_X",
            "symbol": "K_X",
            "definition": "parent kernel/normalization converting residual source current to observable potential strength",
            "units": "schema_required",
            "current_status": "unsourced",
            "required_derivation": "read off from the parent quadratic action and normalization convention",
            "failure_if_missing": "linear-product alpha is symbolic",
            "valid_for_claim": "false",
        },
        {
            "input_id": "PI630_3_Qbar_XH",
            "symbol": "Qbar_XH(lambda;lambda_X)",
            "definition": "source/profile response of the local residual mode in the experimental geometry",
            "units": "schema_required",
            "current_status": "unsourced",
            "required_derivation": "solve/profile-average the residual Green-function response",
            "failure_if_missing": "source leg remains a placeholder",
            "valid_for_claim": "false",
        },
        {
            "input_id": "PI630_4_qbar_XT",
            "symbol": "qbar_XT",
            "definition": "test-body/readout charge or projection of the local residual onto matter",
            "units": "schema_required",
            "current_status": "unsourced",
            "required_derivation": "derive test-leg charge from matter variation or prove it vanishes",
            "failure_if_missing": "cannot tell linear from two-leg coupling branch",
            "valid_for_claim": "false",
        },
        {
            "input_id": "PI630_5_Z_eff",
            "symbol": "Z_eff",
            "definition": "effective kinetic normalization of the local residual mode",
            "units": "action_normalization",
            "current_status": "unsourced",
            "required_derivation": "extract from parent quadratic Hessian in the local sector",
            "failure_if_missing": "alpha normalization is arbitrary",
            "valid_for_claim": "false",
        },
        {
            "input_id": "PI630_6_lambda_X",
            "symbol": "lambda_X",
            "definition": "residual range, sqrt(Z_eff/M_X^2)",
            "units": "m",
            "current_status": "unsourced",
            "required_derivation": "derive M_X^2 from parent Hessian/eigenvalue or prove no finite range",
            "failure_if_missing": "cannot place the residual on the R10 curve",
            "valid_for_claim": "false",
        },
    ]


def pressure_envelope_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(read_csv(PRIOR_629_PRESSURE)):
        alpha_bound = parse_float(row.get("alpha_bound_review_candidate"))
        lambda_value = parse_float(row.get("lambda_value"))
        sqrt_bound = math.sqrt(alpha_bound) if alpha_bound is not None and alpha_bound >= 0 else None
        rows.append(
            {
                "envelope_id": f"PE630_{index}",
                "sample_id": row.get("sample_id", f"PS629_{index}"),
                "lambda_value": row.get("lambda_value", ""),
                "lambda_units": row.get("lambda_units", "m"),
                "alpha_bound_review_candidate": row.get("alpha_bound_review_candidate", ""),
                "linear_product_bound": "" if alpha_bound is None else f"{alpha_bound:.12g}",
                "linear_product": "abs(c_g*tau_R10*K_X*Qbar_XH*qbar_XT/Z_eff)",
                "two_leg_unit_profile_coupling_bound": "" if sqrt_bound is None else f"{sqrt_bound:.12g}",
                "two_leg_note": "if alpha roughly c_eff^2 with unit profile, then abs(c_eff)<=sqrt(alpha_bound); profile factors still missing",
                "pressure_class": row.get("pressure_class", ""),
                "diagnostic_weight": "tightest_sample" if alpha_bound is not None and alpha_bound < 0.01 else "pressure_sample",
                "source": rel(PRIOR_629_PRESSURE),
                "lambda_numeric_positive": bool_text(lambda_value is not None and lambda_value > 0),
                "valid_for_claim": "false",
            }
        )
    return rows


def coupling_ambiguity_rows() -> list[dict[str, Any]]:
    return [
        {
            "ambiguity_id": "AMB630_0_zero_branch",
            "branch": "quotient-descent zero coupling",
            "alpha_law": "alpha_MTS_R10(lambda)=0",
            "when_valid": "matter action descends to quotient and X is purely vertical with silent boundary terms",
            "risk": "currently not parent-signed",
            "next_resolution": "prove matter-frame variation has no Xhat derivative",
            "valid_for_claim": "false",
        },
        {
            "ambiguity_id": "AMB630_1_linear_source_absorbed",
            "branch": "linear product with source leg absorbed",
            "alpha_law": "alpha=abs(c_g*tau_R10*K_X*Qbar_XH*qbar_XT/Z_eff)",
            "when_valid": "K_X Qbar_XH qbar_XT already contains the source charge while c_g is the test/readout coupling",
            "risk": "can hide a second matter leg unless source/test definitions are explicit",
            "next_resolution": "derive source and test currents separately",
            "valid_for_claim": "false",
        },
        {
            "ambiguity_id": "AMB630_2_two_leg_universal",
            "branch": "standard scalar-like two-leg coupling",
            "alpha_law": "alpha proportional to beta_source*beta_test; universal matter coupling gives alpha proportional to c_g^2",
            "when_valid": "the same common-frame derivative controls both source and test bodies",
            "risk": "R10 pressure on c_g is sqrt(alpha_bound/profile), not alpha_bound directly",
            "next_resolution": "derive whether c_g belongs to one leg, both legs, or neither",
            "valid_for_claim": "false",
        },
        {
            "ambiguity_id": "AMB630_3_disformal_residue",
            "branch": "Weyl/disformal mixed coupling",
            "alpha_law": "alpha receives c_g plus d_g_Pi/profile terms",
            "when_valid": "representative disformal channel survives matter-frame descent",
            "risk": "conformal c_g scoring understates the local-test channel",
            "next_resolution": "keep disformal branch blocked until matter frame is varied",
            "valid_for_claim": "false",
        },
    ]


def next_derivation_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "NDC630_0_define_matter_frame",
            "required_output": "explicit g_matter[q(Phi),Xhat,Psi,theta] or proof of no Xhat dependence",
            "success_condition": "partial g_matter/partial Xhat is zero or a symbolic expression with units/source",
            "if_success": "c_g zero theorem or finite c_g expression becomes possible",
            "if_fail": "coupling branch remains closure-only",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "NDC630_1_vary_matter_action",
            "required_output": "delta S_matter/delta Xhat and source/test currents",
            "success_condition": "source and test legs are separated instead of hidden in K_X/Qbar/qbar",
            "if_success": "linear-vs-squared ambiguity is resolved",
            "if_fail": "R10 pressure envelope remains only diagnostic",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "NDC630_2_match_to_yukawa_alpha",
            "required_output": "normalization map from Xhat Green function to Eot-Wash alpha(lambda)",
            "success_condition": "all factors in alpha_MTS_R10 have owner equations and units",
            "if_success": "nonclaim numeric/prior scans can be meaningful",
            "if_fail": "no local empirical score is legitimate",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "NDC630_3_cross_arena_consistency",
            "required_output": "same c_g/tau_A branch mapped to R10, PPN, clocks, and orbital tests",
            "success_condition": "one coupling choice does not solve R10 while breaking PPN/clocks by construction",
            "if_success": "local-GR reduction can be tested as a coupled system",
            "if_fail": "route is phenomenological patchwork and must be demoted",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D630_0_main_verdict",
            "decision": STATUS,
            "meaning": "the coupling problem is now explicitly isolated as the next theory bottleneck",
            "status": "progress_but_not_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D630_1_zero_route",
            "decision": "c_g_zero_not_proven",
            "meaning": "quotient descent would be beautiful but remains unsigned at the parent matter-frame level",
            "status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D630_2_finite_route",
            "decision": "finite_projection_envelope_written",
            "meaning": "if coupling survives, R10 constrains the effective product strongly around the review-curve tight spots",
            "status": "diagnostic_pressure_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D630_3_branch_ambiguity",
            "decision": "linear_vs_two_leg_coupling_must_be_resolved",
            "meaning": "this is probably the missing gearbox: source/test coupling ownership decides whether local tests are safe",
            "status": "next_required",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D630_4_claim_ceiling",
            "decision": CLAIM_CEILING,
            "meaning": "no local-GR, R10, WEP, PPN, clock, or orbital pass follows from 630",
            "status": "hard_guardrail",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def route_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU630_0_allowed",
            "allowed_after_630": "Treat coupling as the primary local-theory bottleneck.",
            "forbidden_after_630": "Claim local GR reduction before deriving matter-frame variation.",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU630_1_allowed",
            "allowed_after_630": "Use R10 pressure envelope as a private target for the effective product.",
            "forbidden_after_630": "Use review-candidate pressure samples as public exclusion/pass evidence.",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU630_2_allowed",
            "allowed_after_630": "Resolve whether c_g is zero, one-leg, two-leg, or disformal-mixed.",
            "forbidden_after_630": "Hide source/test legs inside a single fitted symbol.",
            "next_action": NEXT_TARGET,
        },
    ]


def validation_rows(
    source_rows: list[dict[str, Any]],
    zero_rows: list[dict[str, Any]],
    finite_rows: list[dict[str, Any]],
    input_rows: list[dict[str, Any]],
    pressure_rows: list[dict[str, Any]],
    ambiguity_rows: list[dict[str, Any]],
    contract_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = [row for row in source_rows if row["exists"] != "true"]
    prior_629_rows = read_csv(PRIOR_629_VALIDATION)
    prior_629_fail = [row for row in prior_629_rows if row.get("result") != "pass"]
    zero_verdict = next((row for row in zero_rows if row["clause_id"] == "ZC630_5_zero_verdict"), {})
    pressure_numeric = [
        row
        for row in pressure_rows
        if parse_float(row.get("alpha_bound_review_candidate")) is not None
        and parse_float(row.get("lambda_value")) is not None
        and row.get("valid_for_claim") == "false"
    ]
    tightest = min((parse_float(row.get("alpha_bound_review_candidate")) for row in pressure_rows if parse_float(row.get("alpha_bound_review_candidate")) is not None), default=None)
    input_claim_rows = [row for row in input_rows if row.get("valid_for_claim") == "true"]
    return [
        {
            "check_id": "V630_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V630_1_prior_629_clean",
            "result": "pass" if prior_629_rows and not prior_629_fail else "fail",
            "detail": f"prior_rows={len(prior_629_rows)};prior_fails={len(prior_629_fail)}",
        },
        {
            "check_id": "V630_2_zero_theorem_attempted_not_promoted",
            "result": "pass" if len(zero_rows) == 6 and zero_verdict.get("supports_cg_zero") == "false" else "fail",
            "detail": f"zero_rows={len(zero_rows)};zero_verdict={zero_verdict.get('derivation_status', '')}",
        },
        {
            "check_id": "V630_3_finite_projection_law_written",
            "result": "pass" if len(finite_rows) == 7 and any("alpha_MTS_R10" in row["equation"] for row in finite_rows) else "fail",
            "detail": f"finite_rows={len(finite_rows)}",
        },
        {
            "check_id": "V630_4_parent_inputs_remain_nonclaim",
            "result": "pass" if len(input_rows) == 7 and not input_claim_rows else "fail",
            "detail": f"input_rows={len(input_rows)};claim_rows={len(input_claim_rows)}",
        },
        {
            "check_id": "V630_5_pressure_envelope_numeric_nonclaim",
            "result": "pass" if len(pressure_rows) == 9 and len(pressure_numeric) == 9 and tightest is not None and tightest < 0.01 else "fail",
            "detail": f"pressure_rows={len(pressure_rows)};numeric_nonclaim={len(pressure_numeric)};tightest={tightest}",
        },
        {
            "check_id": "V630_6_coupling_ambiguity_explicit",
            "result": "pass" if len(ambiguity_rows) == 4 and any("c_g^2" in row["alpha_law"] for row in ambiguity_rows) else "fail",
            "detail": f"ambiguity_rows={len(ambiguity_rows)}",
        },
        {
            "check_id": "V630_7_next_derivation_contract_written",
            "result": "pass" if len(contract_rows) == 4 else "fail",
            "detail": f"contract_rows={len(contract_rows)}",
        },
        {
            "check_id": "V630_8_no_local_claim",
            "result": "pass",
            "detail": "c_g_zero=false;finite_coupling_numeric=false;R10=false;WEP=false;PPN=false;clock=false;orbital=false;local_GR=false",
        },
    ]


def nonclaim_summary_rows(pressure_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    numeric_rows = [row for row in pressure_rows if parse_float(row.get("alpha_bound_review_candidate")) is not None]
    tightest_row = min(numeric_rows, key=lambda row: parse_float(row["alpha_bound_review_candidate"])) if numeric_rows else {}
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "c_g_zero_proven": "false",
            "finite_cg_numeric": "false",
            "linear_vs_two_leg_resolved": "false",
            "pressure_rows": len(pressure_rows),
            "tightest_review_alpha_bound": tightest_row.get("alpha_bound_review_candidate", ""),
            "tightest_review_lambda_m": tightest_row.get("lambda_value", ""),
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        }
    ]


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ") for header in headers) + " |")
    return "\n".join(lines)


def build_doc(
    source_rows: list[dict[str, Any]],
    zero_rows: list[dict[str, Any]],
    finite_rows: list[dict[str, Any]],
    input_rows: list[dict[str, Any]],
    pressure_rows: list[dict[str, Any]],
    ambiguity_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 630 Y5 R10 cg projection parent input derivation or source prior envelope",
            f"Status: `{STATUS}`  \nClaim ceiling: `{CLAIM_CEILING}`  \nNext target: `{NEXT_TARGET}`",
            "## Verdict\n"
            "- The gut feeling was right: the coupling is now isolated as the local-theory bottleneck.\n"
            "- A clean `c_g=0` route exists in principle, but it still requires a parent-signed matter-frame descent proof.\n"
            "- If coupling survives, the finite projection law must separate source and test legs before R10/PPN/clocks can mean anything.\n"
            "- This checkpoint therefore writes a nonclaim pressure envelope, not a pass.",
            "## Source Register\n" + markdown_table(source_rows),
            "## Zero-Coupling Theorem Audit\n" + markdown_table(zero_rows),
            "## Finite Coupling Derivation\n" + markdown_table(finite_rows),
            "## Parent Input Targets\n" + markdown_table(input_rows),
            "## R10 Product Pressure Envelope\n" + markdown_table(pressure_rows),
            "## Scalar Coupling Ambiguity Ledger\n" + markdown_table(ambiguity_rows),
            "## Next Derivation Contract\n" + markdown_table(next_rows),
            "## Nonclaim Summary\n" + markdown_table(summary_rows),
            "## Decision\n" + markdown_table(decisions),
            "## Route Update\n" + markdown_table(routes),
            "## Validation\n" + markdown_table(validations),
        ]
    )


def main() -> None:
    source_rows = source_register_rows()
    zero_rows = zero_coupling_theorem_audit_rows()
    finite_rows = finite_coupling_derivation_rows()
    input_rows = parent_input_target_rows()
    pressure_rows = pressure_envelope_rows()
    ambiguity_rows = coupling_ambiguity_rows()
    next_rows = next_derivation_contract_rows()
    summary_rows = nonclaim_summary_rows(pressure_rows)
    decisions = decision_rows()
    routes = route_update_rows()
    validations = validation_rows(source_rows, zero_rows, finite_rows, input_rows, pressure_rows, ambiguity_rows, next_rows)

    write_csv(SOURCE_REGISTER, source_rows)
    write_csv(ZERO_AUDIT, zero_rows)
    write_csv(FINITE_DERIVATION, finite_rows)
    write_csv(PARENT_INPUT_TARGETS, input_rows)
    write_csv(PRESSURE_ENVELOPE, pressure_rows)
    write_csv(COUPLING_AMBIGUITY, ambiguity_rows)
    write_csv(NEXT_CONTRACT, next_rows)
    write_csv(NONCLAIM_SUMMARY, summary_rows)
    write_csv(DECISION, decisions)
    write_csv(ROUTE_UPDATE, routes)
    write_csv(VALIDATION, validations)
    DOC.write_text(
        build_doc(
            source_rows,
            zero_rows,
            finite_rows,
            input_rows,
            pressure_rows,
            ambiguity_rows,
            next_rows,
            summary_rows,
            decisions,
            routes,
            validations,
        )
        + "\n",
        encoding="utf-8",
    )
    failed = [row for row in validations if row["result"] != "pass"]
    print(json.dumps({"status": STATUS, "doc": str(DOC), "failed_checks": failed}, indent=2))


if __name__ == "__main__":
    main()
