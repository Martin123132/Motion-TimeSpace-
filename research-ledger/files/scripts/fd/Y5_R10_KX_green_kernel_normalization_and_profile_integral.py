from __future__ import annotations

import csv
import json
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path

from R10_alpha_lambda_bound_prediction_runner import MTS_REQUIRED_COLUMNS, run_runner


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
DOC = ROOT / "1035-Y5-R10-KX-green-kernel-normalization-and-profile-integral.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1035-R10-KX-profile-nonclaim-smoke" / "results"
MTS_TEMPLATE = OUT / "R10_alpha_lambda_curve_MTS_1035_KX_PROFILE_TEMPLATE_NONCLAIM.csv"
BOUND_CANDIDATE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: object) -> bool:
    return str(value).strip().lower() == "true"


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        (
            "SRC1035_0_1034_next",
            "source-intake/mts_residuals/P8_Y5_R10_1034_NEXT_TARGET.csv",
            "1035-Y5-R10-KX-green-kernel-normalization-and-profile-integral.md",
            "1034 handoff selecting K_X/profile-integral target.",
        ),
        (
            "SRC1035_1_1034_projection",
            "source-intake/mts_residuals/P8_Y5_R10_1034_PROJECTION_INPUT_PACK.csv",
            "R10P1034_1_KX_lambda",
            "1034 missing K_X/Qbar/tau/c_g/tail projection pack.",
        ),
        (
            "SRC1035_2_1034_convention",
            "source-intake/mts_residuals/P8_Y5_R10_1034_SOURCE_TEST_PROFILE_CONVENTION.csv",
            "R10C1034_2_source_profile",
            "1034 source/test profile placeholders.",
        ),
        (
            "SRC1035_3_1034_bound_candidate",
            "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "R10_VECTOR_2020_REVIEW_0000",
            "1034 external curve review candidate, not a live claim curve.",
        ),
        (
            "SRC1035_4_1034_alpha_rows",
            "source-intake/mts_residuals/P8_Y5_R10_1034_ALPHA_BOUND_CANDIDATE_ROWS.csv",
            "R10B1034_3_vector_review_candidate_summary",
            "1034 alpha-bound summary and anchor rows.",
        ),
        (
            "SRC1035_5_1033_tau_audit",
            "source-intake/mts_residuals/P8_Y5_R10_1033_TAU_R10_DERIVATION_AUDIT.csv",
            "TAUR1033_1_factorization",
            "1033 factorization into K_X, Qbar_XH, tau_R10, c_g, and retained tails.",
        ),
        (
            "SRC1035_6_631_charge_law",
            "source-intake/mts_residuals/P8_Y5_R10_631_SOURCE_TEST_CHARGE_LAW.csv",
            "Q631_0_universal_weyl_charge",
            "631 source/test charge law showing universal branch gives alpha proportional to c_g squared.",
        ),
        (
            "SRC1035_7_live_mts_placeholder",
            "source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_source_normalization.csv",
            "MISSING_SOURCE_NORMALIZED_ALPHA_PREDICTION",
            "Live MTS alpha(lambda) prediction remains placeholder-only.",
        ),
        (
            "SRC1035_8_bound_runner",
            "scripts/R10_alpha_lambda_bound_prediction_runner.py",
            "MTS_REQUIRED_COLUMNS",
            "Existing R10 runner used for nonclaim smoke validation.",
        ),
    ]
    rows: list[dict[str, str]] = []
    for source_id, path_text, needle, role in specs:
        path = source_path(path_text)
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(exists).lower(),
                "needle": needle,
                "needle_found": str(needle in text).lower(),
                "role": role,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def kernel_derivation_rows() -> list[dict[str, str]]:
    return [
        {
            "derivation_id": "KXD1035_0_parent_quadratic_operator",
            "step": "isolate the finite local response mode",
            "assumptions": "weak-field static limit; one finite scalar-like response X; parent action supplies Z_X>0 and lambda_X",
            "mathematical_result": "S_X^(2)=-1/2 int [Z_X (partial X)^2 + Z_X lambda_X^-2 X^2] + int X J_X",
            "status": "CONDITIONAL_OPERATOR_FORM",
            "missing_for_claim": "parent-signed Z_X, range/mass relation, X normalization, and source-current definition",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "derivation_id": "KXD1035_1_static_green_function",
            "step": "invert the static operator",
            "assumptions": "flat local lab limit; boundary terms and hidden components silent; source compact compared with lab scale",
            "mathematical_result": "(nabla^2-lambda_X^-2) X = -J_X/Z_X; G_lambda(r)=exp(-r/lambda)/(4 pi r)",
            "status": "DERIVED_CONDITIONAL_GREEN_KERNEL",
            "missing_for_claim": "proof that MTS local finite branch really reduces to this operator and not derivative/disformal/tensor response",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "derivation_id": "KXD1035_2_point_body_yukawa_match",
            "step": "match the Green solution to the R10 Yukawa convention",
            "assumptions": "point bodies; source/test charges beta_s,beta_t are mass-normalized in the same parent convention",
            "mathematical_result": "alpha_X(lambda_X)=K_X^pt beta_s beta_t with K_X^pt fixed by the parent normalization; in canonical mass-normalized units K_X^pt=1/(4 pi G_N Z_X)",
            "status": "CONDITIONAL_NORMALIZATION_LAW",
            "missing_for_claim": "whether beta_i already absorbs sqrt(4 pi G_N Z_X), and SI/hbar/c conversion convention",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "derivation_id": "KXD1035_3_extended_body_overlap",
            "step": "replace point bodies by source/test support integrals",
            "assumptions": "finite source and detector densities; same Yukawa profile convention as R10",
            "mathematical_result": "F_ST(lambda,R)=R exp(R/lambda)/(M_s M_t) int rho_s(x) rho_t(y) exp(-|R+x-y|/lambda)/|R+x-y| d^3x d^3y",
            "status": "DERIVED_PROFILE_FORM_FACTOR_CONTRACT",
            "missing_for_claim": "actual R10 geometry/material density/support and harmonic torque projection",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "derivation_id": "KXD1035_4_R10_harmonic_projection",
            "step": "map potential energy to the measured R10 torque harmonics",
            "assumptions": "R10 compares Yukawa torques at 18 omega and 120 omega against the same alpha(lambda) convention",
            "mathematical_result": "K_X^R10(lambda)=K_X^pt * F_ST(lambda) * Pi_R10, with Pi_R10 the experiment-specific torque/readout projection",
            "status": "CONDITIONAL_R10_PROJECTION_CONTRACT",
            "missing_for_claim": "Fourier-Bessel R10 geometry or official torque kernels for the MTS source current",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "derivation_id": "KXD1035_5_verdict",
            "step": "decide whether K_X(lambda) is numeric",
            "assumptions": "use only current corpus and 1034 data plumbing",
            "mathematical_result": "K_X(lambda) has a derived shape contract but no numeric parent-signed value",
            "status": "NOT_NUMERIC_CURRENT_CORPUS",
            "missing_for_claim": "Z_X, lambda_X, beta_s, beta_t, R10 profile/harmonic projection, and retained-tail envelope",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def charge_split_rows() -> list[dict[str, str]]:
    return [
        {
            "charge_id": "BETA1035_0_product_law",
            "branch": "generic finite X exchange",
            "source_charge": "beta_s(lambda)",
            "test_charge": "beta_t(lambda)",
            "alpha_law": "alpha_X(lambda)=K_X^R10(lambda) beta_s(lambda) beta_t(lambda) + epsilon_tail(lambda)",
            "status": "REQUIRED_PRODUCT_FORM",
            "missing_for_claim": "source/test charge definitions from parent matter action",
            "valid_for_claim": "false",
            "notes": "This prevents accidentally treating a two-body exchange as linear in one coupling.",
            "generated_utc": stamp(),
        },
        {
            "charge_id": "BETA1035_1_universal_weyl",
            "branch": "universal conformal matter-frame response",
            "source_charge": "beta_s=c_g times source profile if source matter mass depends on X",
            "test_charge": "beta_t=c_g times test/readout profile if test mass depends on X",
            "alpha_law": "alpha_X proportional to K_X^R10 c_g^2, not K_X c_g, unless Qbar_XH explicitly already contains one c_g",
            "status": "CONDITIONAL_CG_SQUARED_WARNING",
            "missing_for_claim": "parent-signed matter-frame mass dependence and profile factors",
            "valid_for_claim": "false",
            "notes": "Refines the 1033 shorthand: Qbar_XH must be interpreted as the source leg, not a free magic prefactor.",
            "generated_utc": stamp(),
        },
        {
            "charge_id": "BETA1035_2_quotient_zero",
            "branch": "quotient-only matter action",
            "source_charge": "beta_s=0",
            "test_charge": "beta_t=0",
            "alpha_law": "alpha_X=0 if and only if the quotient-zero premises are parent-signed",
            "status": "CONDITIONAL_ZERO_BRANCH",
            "missing_for_claim": "signed no-shadow/no-extra-frame theorem for matter masses and readout",
            "valid_for_claim": "false",
            "notes": "A zero branch would beat R10 cleanly, but it is not available as a naked assumption.",
            "generated_utc": stamp(),
        },
        {
            "charge_id": "BETA1035_3_composition_or_disformal",
            "branch": "composition/disformal/stress response",
            "source_charge": "beta_s plus stress/support terms",
            "test_charge": "beta_t plus material/readout terms",
            "alpha_law": "alpha_X requires extra composition, WEP, clock, and stress projection rows",
            "status": "MIXED_BRANCH_BLOCKED",
            "missing_for_claim": "material sensitivities, stress projection, and WEP-compatible source/test law",
            "valid_for_claim": "false",
            "notes": "This branch cannot be scored by a scalar Yukawa row alone.",
            "generated_utc": stamp(),
        },
    ]


def profile_integral_rows() -> list[dict[str, str]]:
    return [
        {
            "profile_id": "PROF1035_0_source_support",
            "required_object": "rho_s^X(x)",
            "definition": "source-body X charge density normalized to the same mass/current convention as beta_s",
            "formula": "Q_s(lambda)=int_source rho_s^X(x) d^3x with finite-size corrections entering F_ST",
            "status": "MISSING_SOURCE_SUPPORT",
            "needed_for_score": "R10 attractor/test-body material density and parent X charge density rule",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "profile_id": "PROF1035_1_test_support",
            "required_object": "rho_t^X(y)",
            "definition": "test-body/readout X charge density normalized to beta_t",
            "formula": "Q_t(lambda)=int_test rho_t^X(y) d^3y with torsion readout projection",
            "status": "MISSING_TEST_SUPPORT",
            "needed_for_score": "pendulum/detector support, readout convention, and material trace law",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "profile_id": "PROF1035_2_pair_overlap",
            "required_object": "F_ST(lambda,R)",
            "definition": "extended-body correction that reduces to 1 in the point-body limit under the chosen convention",
            "formula": "R exp(R/lambda)/(M_s M_t) int rho_s rho_t exp(-r_xy/lambda)/r_xy d^3x d^3y",
            "status": "SYMBOLIC_FORM_FACTOR_ONLY",
            "needed_for_score": "geometry/material integrals or official Fourier-Bessel kernel",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "profile_id": "PROF1035_3_R10_harmonic",
            "required_object": "Pi_R10(lambda)",
            "definition": "maps the source/test potential overlap to the 18 omega and 120 omega torque harmonics used by Eot-Wash",
            "formula": "Pi_R10 = projected_torque_kernel[MTS source current] / projected_torque_kernel[unit-alpha Yukawa]",
            "status": "MISSING_R10_HARMONIC_KERNEL",
            "needed_for_score": "R10 geometry kernel, harmonic weights, and separation distribution",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "profile_id": "PROF1035_4_measured_G_calibration",
            "required_object": "Newton normalization",
            "definition": "same G_N and mass normalization used by the experiment and by the MTS weak-field limit",
            "formula": "alpha is dimensionless only after dividing the X interaction by -G_N M_s M_t/r or its torque equivalent",
            "status": "MISSING_PARENT_NEWTON_MATCH",
            "needed_for_score": "MTS-to-Newton local limit and measured-G calibration convention",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def kx_factorization_rows() -> list[dict[str, str]]:
    return [
        {
            "factor_id": "KXF1035_0_KX_point",
            "factor": "K_X^pt",
            "symbolic_value": "1/(4 pi G_N Z_X) if beta_i are mass-normalized parent charges that do not already absorb Z_X or G_N",
            "units": "dimensionless after parent charge convention; otherwise parent-declared",
            "status": "SYMBOLIC_CONDITIONAL",
            "missing_for_claim": "Z_X and charge-unit convention",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "factor_id": "KXF1035_1_range",
            "factor": "lambda_X",
            "symbolic_value": "lambda_X = 1/m_X in natural units, or hbar/(m_X c) in SI mass units",
            "units": "m",
            "status": "MISSING_PARENT_RANGE_RELATION",
            "missing_for_claim": "parent mass/kinetic row for finite X mode",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "factor_id": "KXF1035_2_profile",
            "factor": "F_ST(lambda)",
            "symbolic_value": "extended-body Yukawa overlap normalized to the point-body alpha convention",
            "units": "dimensionless",
            "status": "SYMBOLIC_ONLY",
            "missing_for_claim": "R10 source/test support and material density rule",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "factor_id": "KXF1035_3_harmonic",
            "factor": "Pi_R10(lambda)",
            "symbolic_value": "R10 torque harmonic projection ratio for MTS current versus unit-alpha Yukawa current",
            "units": "dimensionless",
            "status": "MISSING_EXPERIMENTAL_PROJECTION",
            "missing_for_claim": "Fourier-Bessel torque kernel or official numerical kernel",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "factor_id": "KXF1035_4_total",
            "factor": "K_X^R10(lambda)",
            "symbolic_value": "K_X^pt * F_ST(lambda) * Pi_R10(lambda)",
            "units": "dimensionless alpha-normalized factor",
            "status": "NOT_NUMERIC_CURRENT_CORPUS",
            "missing_for_claim": "all KXF1035_0 through KXF1035_3 inputs",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def mts_template_rows() -> list[dict[str, str]]:
    return [
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "KX_profile_product_template",
            "curve_id": "R10_alpha_lambda_curve_MTS_1035_KX_PROFILE_TEMPLATE_NONCLAIM",
            "lambda_value": "MISSING_PARENT_LAMBDA_X",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_KX_BETA_SOURCE_BETA_TEST_TAILS",
            "alpha_bound": "MISSING_PROMOTED_R10_ALPHA_BOUND_CURVE",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv is review-only",
            "force_law_form": "V(r)=V_N(r)[1+alpha exp(-r/lambda)]",
            "derivation_status": "template_invalid_missing_parent_ZX_lambda_beta_profile_and_promoted_bound",
            "formula_reference": "1035-Y5-R10-KX-green-kernel-normalization-and-profile-integral.md::KXD1035_2",
            "source_file": "MISSING_PARENT_SOURCE_FILE",
            "assumptions": "alpha_X=K_X^R10 beta_s beta_t + epsilon_tail; no unity tau shortcut; no cancellation credit",
            "valid_for_claim": "false",
            "notes": "Skeleton row only; do not score.",
        },
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "universal_weyl_cg_squared_template",
            "curve_id": "R10_alpha_lambda_curve_MTS_1035_KX_PROFILE_TEMPLATE_NONCLAIM",
            "lambda_value": "MISSING_PARENT_LAMBDA_X",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_NUMERIC_KX_TIMES_CG_SQUARED",
            "alpha_bound": "MISSING_PROMOTED_R10_ALPHA_BOUND_CURVE",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv is review-only",
            "force_law_form": "universal source/test exchange gives alpha proportional to c_g^2 under mass-normalized beta convention",
            "derivation_status": "template_invalid_missing_cg_ZX_profile_and_source_test_charge_signoff",
            "formula_reference": "1035-Y5-R10-KX-green-kernel-normalization-and-profile-integral.md::BETA1035_1",
            "source_file": "MISSING_PARENT_SOURCE_FILE",
            "assumptions": "Qbar_XH must carry the source leg if shorthand alpha=K_X Qbar_XH(tau c_g) is used",
            "valid_for_claim": "false",
            "notes": "This row blocks accidental linear-c_g scoring.",
        },
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "quotient_zero_template",
            "curve_id": "R10_alpha_lambda_curve_MTS_1035_KX_PROFILE_TEMPLATE_NONCLAIM",
            "lambda_value": "ALL_LOCAL_R10_RANGE",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_SIGNED_ZERO_THEOREM",
            "alpha_bound": "not_applicable_until_zero_theorem_signed",
            "alpha_bound_source": "not_applicable_until_zero_theorem_signed",
            "force_law_form": "alpha_X=0 only if beta_s=beta_t=0 from quotient-only matter action",
            "derivation_status": "template_invalid_missing_no_shadow_matter_action_zero_theorem",
            "formula_reference": "1035-Y5-R10-KX-green-kernel-normalization-and-profile-integral.md::BETA1035_2",
            "source_file": "MISSING_PARENT_SOURCE_FILE",
            "assumptions": "zero cannot be asserted by taste; it needs parent-signed descent/no-shadow theorem",
            "valid_for_claim": "false",
            "notes": "Closure-only until the parent action proves the quotient-zero branch.",
        },
    ]


def join_readiness_rows() -> list[dict[str, str]]:
    return [
        {
            "join_id": "JOIN1035_0_bound_curve",
            "side": "external",
            "object": "alpha_bound(lambda)",
            "current_status": "REVIEW_CANDIDATE_NONCLAIM",
            "source": relative(BOUND_CANDIDATE),
            "ready_for_join": "false",
            "needed": "official supplement table or human QA promotion",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "join_id": "JOIN1035_1_KX",
            "side": "theory",
            "object": "K_X^R10(lambda)",
            "current_status": "SYMBOLIC_CONDITIONAL",
            "source": "P8_Y5_R10_1035_KX_FACTORIZATION_ROWS.csv",
            "ready_for_join": "false",
            "needed": "Z_X, lambda_X, G_N convention, profile, and harmonic projection",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "join_id": "JOIN1035_2_beta_source",
            "side": "theory",
            "object": "beta_s(lambda)",
            "current_status": "MISSING_SOURCE_CHARGE",
            "source": "P8_Y5_R10_1035_SOURCE_TEST_CHARGE_SPLIT.csv",
            "ready_for_join": "false",
            "needed": "parent matter action source-leg charge",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "join_id": "JOIN1035_3_beta_test",
            "side": "theory",
            "object": "beta_t(lambda)",
            "current_status": "MISSING_TEST_CHARGE",
            "source": "P8_Y5_R10_1035_SOURCE_TEST_CHARGE_SPLIT.csv",
            "ready_for_join": "false",
            "needed": "tau_R10/readout projection and parent c_g or zero theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "join_id": "JOIN1035_4_tail_envelope",
            "side": "theory",
            "object": "epsilon_tail(lambda)",
            "current_status": "MISSING_ABSOLUTE_ENVELOPE",
            "source": "P8_Y5_R10_1035_PROFILE_INTEGRAL_CONTRACT.csv",
            "ready_for_join": "false",
            "needed": "no-cancellation absolute envelope for all retained components",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def runner_smoke_rows(status: dict[str, object]) -> list[dict[str, str]]:
    return [
        {
            "smoke_id": "SMOKE1035_0_runner_status",
            "runner_output_dir": str(RUN_DIR),
            "mts_rows": str(status.get("mts_rows")),
            "bound_rows": str(status.get("bound_rows")),
            "valid_mts_rows": str(status.get("valid_mts_rows")),
            "valid_bound_rows": str(status.get("valid_bound_rows")),
            "comparison_rows": str(status.get("comparison_rows")),
            "R10_pass_for_claim": str(status.get("R10_pass_for_claim")).lower(),
            "claim_allowed": str(status.get("claim_allowed")).lower(),
            "expected_result": "blocked_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def placeholder_refusal_rows(join_rows: list[dict[str, str]], smoke_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, row in enumerate(join_rows):
        reasons = []
        if "MISSING" in row["current_status"]:
            reasons.append(row["current_status"])
        if not flag(row["ready_for_join"]):
            reasons.append("NOT_READY_FOR_JOIN")
        if not flag(row["valid_for_claim"]):
            reasons.append("CLAIM_POLICY_FALSE")
        rows.append(
            {
                "refusal_id": f"REF1035_{index}_{row['object'].replace('(', '').replace(')', '').replace(' ', '_')}",
                "object": row["object"],
                "current_status": row["current_status"],
                "refusal_status": "rejected_missing_or_nonclaim_join_input",
                "failure_reasons": ";".join(reasons),
                "score_eligible": "false",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    if smoke_rows and not flag(smoke_rows[0]["claim_allowed"]):
        rows.append(
            {
                "refusal_id": "REF1035_runner_smoke",
                "object": "R10 existing runner smoke",
                "current_status": "blocked_nonclaim",
                "refusal_status": "runner_correctly_refused_claim",
                "failure_reasons": "NO_VALID_MTS_ROWS_OR_NONCLAIM_BOUND_ROWS",
                "score_eligible": "false",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE1035_0_green_kernel",
            "claim": "K_X(lambda) is derived numerically",
            "gate_pass": "false",
            "reason": "Green kernel form is conditional but Z_X/range/source-current normalization are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1035_1_charge_product",
            "claim": "R10 alpha is linear in c_g",
            "gate_pass": "false",
            "reason": "two-body exchange requires beta_source beta_test; universal branch is proportional to c_g^2 unless source leg already includes c_g",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1035_2_profile_integral",
            "claim": "R10 finite-size/profile projection is ready",
            "gate_pass": "false",
            "reason": "source/test support, material charge, and R10 harmonic projection are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1035_3_runner_claim",
            "claim": "existing R10 runner grants a pass",
            "gate_pass": "false",
            "reason": "nonclaim smoke has no valid MTS rows and no promoted bound curve rows",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1035_4_zero_branch",
            "claim": "local R10 is zero by quotient descent",
            "gate_pass": "false",
            "reason": "zero branch remains conditional until no-shadow matter action theorem is signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1035_0_kernel_status",
            "decision": "K_X has a derived conditional Green-kernel form but no numeric value.",
            "because": "the static Yukawa inverse is fixed once Z_X and lambda_X exist, but the parent action has not supplied them.",
            "next_action": "derive/source the parent X quadratic row: Z_X, M_X/lambda_X, source current J_X, and beta normalization",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1035_1_coupling_status",
            "decision": "The R10 coupling must be source-test product beta_s beta_t.",
            "because": "a fifth-force Yukawa exchange couples two bodies; universal c_g generally enters twice.",
            "next_action": "split Qbar_XH and tau_R10 into explicit beta_source and beta_test rows",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1035_2_score_status",
            "decision": "R10 scoring remains blocked, correctly.",
            "because": "the external curve is still nonclaim and the MTS alpha prediction is symbolic.",
            "next_action": "use 1035 template only for schema smoke, not evidence",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1035_3_next_target",
            "decision": "Next target is parent X quadratic action and beta source/test split.",
            "because": "that is the shortest route to making K_X and c_g/c_g^2 mathematically owned rather than fitted or guessed.",
            "next_action": "1036-Y5-R10-parent-X-quadratic-action-and-beta-source-test-split.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1036-Y5-R10-parent-X-quadratic-action-and-beta-source-test-split.md",
            "objective": "derive or demote the parent finite-X quadratic action row that supplies Z_X, lambda_X/M_X, J_X, beta_source, beta_test, and the c_g versus c_g^2 coupling law",
            "include": "parent action coefficient, kinetic residue sign, range relation, source current, source/test charge split, quotient-zero alternative, disformal/composition tail routing, R10 alpha template update",
            "exclude": "invented numeric K_X, invented c_g, unity tau shortcut, linear-c_g scoring without source leg, R10 pass claim, formalization-workbench edits, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validate(
    source_rows: list[dict[str, str]],
    kernel_rows: list[dict[str, str]],
    charge_rows: list[dict[str, str]],
    profile_rows: list[dict[str, str]],
    kx_rows: list[dict[str, str]],
    mts_rows: list[dict[str, str]],
    join_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(
        (
            "V1035_0_sources_exist",
            all(flag(row["exists"]) and flag(row["needle_found"]) for row in source_rows),
            "all 1035 source paths exist and expected needles are present",
        )
    )
    checks.append(
        (
            "V1035_1_green_kernel_contract",
            any(row["derivation_id"] == "KXD1035_1_static_green_function" and "G_lambda" in row["mathematical_result"] for row in kernel_rows),
            "static Yukawa Green-kernel form is written",
        )
    )
    checks.append(
        (
            "V1035_2_no_numeric_KX_claim",
            any(row["status"] == "NOT_NUMERIC_CURRENT_CORPUS" for row in kernel_rows)
            and all(not flag(row["valid_for_claim"]) for row in kernel_rows),
            "K_X remains explicitly nonnumeric/nonclaim",
        )
    )
    checks.append(
        (
            "V1035_3_charge_product_law",
            any("beta_s" in row["alpha_law"] and "beta_t" in row["alpha_law"] for row in charge_rows)
            and any("c_g^2" in row["alpha_law"] for row in charge_rows),
            "source-test product law and universal c_g-squared warning are present",
        )
    )
    checks.append(
        (
            "V1035_4_profile_missing_explicit",
            any(row["status"] == "MISSING_R10_HARMONIC_KERNEL" for row in profile_rows)
            and any(row["status"] == "MISSING_PARENT_NEWTON_MATCH" for row in profile_rows),
            "R10 harmonic/profile and Newton normalization gaps are explicit",
        )
    )
    checks.append(
        (
            "V1035_5_kx_factorization_blocked",
            any(row["factor"] == "K_X^R10(lambda)" and row["score_ready"] == "false" for row in kx_rows)
            and all(not flag(row["valid_for_claim"]) for row in kx_rows),
            "K_X factorization rows refuse scoring",
        )
    )
    checks.append(
        (
            "V1035_6_mts_template_schema",
            set(MTS_REQUIRED_COLUMNS).issubset(set(mts_rows[0].keys())) if mts_rows else False,
            "MTS nonclaim template has the runner-required schema",
        )
    )
    checks.append(
        (
            "V1035_7_mts_template_nonclaim",
            bool(mts_rows) and all(not flag(row["valid_for_claim"]) for row in mts_rows),
            "MTS template rows remain valid_for_claim=false",
        )
    )
    checks.append(
        (
            "V1035_8_join_readiness_blocked",
            all(not flag(row["ready_for_join"]) and not flag(row["valid_for_claim"]) for row in join_rows),
            "all join inputs remain blocked/nonclaim",
        )
    )
    checks.append(
        (
            "V1035_9_runner_smoke_refuses_claim",
            bool(smoke_rows)
            and smoke_rows[0]["R10_pass_for_claim"] == "false"
            and smoke_rows[0]["claim_allowed"] == "false",
            "existing runner refuses the nonclaim 1035 smoke rows",
        )
    )
    checks.append(
        (
            "V1035_10_claim_gates_blocked",
            all(not flag(row["claim_allowed"]) and not flag(row["valid_for_claim"]) for row in claim_rows),
            "all claim gates remain closed",
        )
    )
    checks.append(
        (
            "V1035_11_next_target_written",
            bool(next_rows)
            and next_rows[0]["next_target"] == "1036-Y5-R10-parent-X-quadratic-action-and-beta-source-test-split.md",
            "next target row is present",
        )
    )
    generated_files = [
        DOC,
        OUT / "P8_Y5_R10_1035_SOURCE_REGISTER.csv",
        OUT / "P8_Y5_R10_1035_KERNEL_DERIVATION_AUDIT.csv",
        OUT / "P8_Y5_R10_1035_SOURCE_TEST_CHARGE_SPLIT.csv",
        OUT / "P8_Y5_R10_1035_PROFILE_INTEGRAL_CONTRACT.csv",
        OUT / "P8_Y5_R10_1035_KX_FACTORIZATION_ROWS.csv",
        OUT / "P8_Y5_R10_1035_JOIN_READINESS.csv",
        OUT / "P8_Y5_R10_1035_RUNNER_SMOKE_STATUS.csv",
        OUT / "P8_Y5_R10_1035_PLACEHOLDER_REFUSAL_RUNNER.csv",
        OUT / "P8_Y5_R10_1035_CLAIM_GATES.csv",
        OUT / "P8_Y5_R10_1035_DECISION_LEDGER.csv",
        OUT / "P8_Y5_R10_1035_NEXT_TARGET.csv",
        OUT / "P8_Y5_BRR545_1035_VALIDATION.csv",
        MTS_TEMPLATE,
    ]
    checks.append(
        (
            "V1035_12_generated_files_in_post_checkpoint",
            all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in generated_files if path.exists() or path.parent.exists()),
            "all generated files are under post-checkpoint-work",
        )
    )
    formalization_touches = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*"):
            if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED:
                formalization_touches.append(path)
    checks.append(
        (
            "V1035_13_formalization_untouched",
            not formalization_touches,
            f"formalization-workbench modified-file count since script start is {len(formalization_touches)}",
        )
    )
    rows = [
        {
            "check_id": "V1035_SUMMARY",
            "result": "pass" if all(result for _, result, _ in checks) else "fail",
            "detail": "1035 K_X Green-kernel/profile-integral validation summary",
            "generated_utc": stamp(),
        }
    ]
    for check_id, result, detail in checks:
        rows.append(
            {
                "check_id": check_id,
                "result": "pass" if result else "fail",
                "detail": detail,
                "generated_utc": stamp(),
            }
        )
    return rows


def write_doc(
    source_rows: list[dict[str, str]],
    kernel_rows: list[dict[str, str]],
    charge_rows: list[dict[str, str]],
    profile_rows: list[dict[str, str]],
    kx_rows: list[dict[str, str]],
    mts_rows: list[dict[str, str]],
    join_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
    refusal_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    sections = [
        "# 1035 Y5 R10 K_X Green-kernel normalization and profile integral",
        "",
        "**Status:** The R10 theory-side kernel is now reduced to a clean conditional law: a finite local mode with quadratic residue `Z_X` gives a Yukawa Green kernel, and the observable coefficient is a **source-test product** `alpha_X = K_X^R10 beta_s beta_t + epsilon_tail`. This is useful progress, but not a claim: `Z_X`, `lambda_X`, `beta_s`, `beta_t`, the R10 harmonic profile, and the retained-tail envelope are still missing.",
        "",
        "**Important correction:** the universal coupling branch is not naturally linear in `c_g`. A two-body fifth-force exchange uses source and test charges. If both legs are universal Weyl legs, the leading Yukawa coefficient is proportional to `c_g^2` unless the source leg has already been explicitly packed into `Qbar_XH`.",
        "",
        "**Claim ceiling:** no numeric `K_X`, no R10 pass, no `alpha=0` local claim, no linear-`c_g` score, no unity `tau_R10` shortcut, and no GitHub/formalization-workbench action is allowed from 1035.",
        "",
        "## Source register",
        md_table(source_rows, ["source_id", "source_path", "exists", "needle_found", "role"]),
        "## Kernel derivation audit",
        md_table(kernel_rows, ["derivation_id", "step", "mathematical_result", "status", "missing_for_claim", "valid_for_claim"]),
        "## Source/test charge split",
        md_table(charge_rows, ["charge_id", "branch", "source_charge", "test_charge", "alpha_law", "status", "valid_for_claim", "notes"]),
        "## Profile integral contract",
        md_table(profile_rows, ["profile_id", "required_object", "definition", "formula", "status", "needed_for_score", "valid_for_claim"]),
        "## K_X factorization rows",
        md_table(kx_rows, ["factor_id", "factor", "symbolic_value", "units", "status", "missing_for_claim", "score_ready", "valid_for_claim"]),
        "## MTS alpha prediction template",
        md_table(mts_rows, ["model_id", "branch_id", "lambda_value", "alpha_predicted", "derivation_status", "valid_for_claim", "notes"]),
        "## Join readiness",
        md_table(join_rows, ["join_id", "side", "object", "current_status", "ready_for_join", "needed", "valid_for_claim"]),
        "## Runner smoke status",
        md_table(smoke_rows, ["smoke_id", "valid_mts_rows", "valid_bound_rows", "comparison_rows", "R10_pass_for_claim", "claim_allowed", "expected_result"]),
        "## Placeholder refusal runner",
        md_table(refusal_rows, ["refusal_id", "object", "current_status", "refusal_status", "failure_reasons", "score_eligible", "claim_allowed"]),
        "## Claim gates",
        md_table(claim_rows, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
        "## Decision ledger",
        md_table(decision, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
        "## Validation",
        md_table(validation_rows, ["check_id", "result", "detail", "generated_utc"]),
        "## Next target",
        md_table(next_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if RUN_DIR.exists():
        shutil.rmtree(RUN_DIR)
    RUN_DIR.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    kernel_rows = kernel_derivation_rows()
    charge_rows = charge_split_rows()
    profile_rows = profile_integral_rows()
    kx_rows = kx_factorization_rows()
    mts_rows = mts_template_rows()
    write_csv(MTS_TEMPLATE, mts_rows, MTS_REQUIRED_COLUMNS)

    runner_result = run_runner(MTS_TEMPLATE, BOUND_CANDIDATE, RUN_DIR)
    smoke_rows = runner_smoke_rows(runner_result["status"])
    join_rows = join_readiness_rows()
    refusal_rows = placeholder_refusal_rows(join_rows, smoke_rows)
    claim_rows = claim_gate_rows()
    decision = decision_rows()
    next_rows = next_target_rows()
    validation = validate(
        source_rows,
        kernel_rows,
        charge_rows,
        profile_rows,
        kx_rows,
        mts_rows,
        join_rows,
        smoke_rows,
        claim_rows,
        next_rows,
    )

    write_csv(OUT / "P8_Y5_R10_1035_SOURCE_REGISTER.csv", source_rows)
    write_csv(OUT / "P8_Y5_R10_1035_KERNEL_DERIVATION_AUDIT.csv", kernel_rows)
    write_csv(OUT / "P8_Y5_R10_1035_SOURCE_TEST_CHARGE_SPLIT.csv", charge_rows)
    write_csv(OUT / "P8_Y5_R10_1035_PROFILE_INTEGRAL_CONTRACT.csv", profile_rows)
    write_csv(OUT / "P8_Y5_R10_1035_KX_FACTORIZATION_ROWS.csv", kx_rows)
    write_csv(OUT / "P8_Y5_R10_1035_JOIN_READINESS.csv", join_rows)
    write_csv(OUT / "P8_Y5_R10_1035_RUNNER_SMOKE_STATUS.csv", smoke_rows)
    write_csv(OUT / "P8_Y5_R10_1035_PLACEHOLDER_REFUSAL_RUNNER.csv", refusal_rows)
    write_csv(OUT / "P8_Y5_R10_1035_CLAIM_GATES.csv", claim_rows)
    write_csv(OUT / "P8_Y5_R10_1035_DECISION_LEDGER.csv", decision)
    write_csv(OUT / "P8_Y5_R10_1035_NEXT_TARGET.csv", next_rows)
    write_csv(OUT / "P8_Y5_BRR545_1035_VALIDATION.csv", validation)
    write_doc(
        source_rows,
        kernel_rows,
        charge_rows,
        profile_rows,
        kx_rows,
        mts_rows,
        join_rows,
        smoke_rows,
        refusal_rows,
        claim_rows,
        decision,
        validation,
        next_rows,
    )

    if validation[0]["result"] != "pass":
        failed = [row for row in validation if row["result"] == "fail"]
        raise SystemExit(f"1035 validation failed: {failed}")


if __name__ == "__main__":
    main()
