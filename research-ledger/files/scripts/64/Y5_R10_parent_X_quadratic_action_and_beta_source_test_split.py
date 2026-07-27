from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path

from R10_alpha_lambda_bound_prediction_runner import MTS_REQUIRED_COLUMNS, run_runner


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
DOC = ROOT / "1036-Y5-R10-parent-X-quadratic-action-and-beta-source-test-split.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1036-R10-parent-X-beta-nonclaim-smoke" / "results"
MTS_TEMPLATE = OUT / "R10_alpha_lambda_curve_MTS_1036_PARENT_X_BETA_TEMPLATE_NONCLAIM.csv"
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
            "SRC1036_0_1035_next",
            "source-intake/mts_residuals/P8_Y5_R10_1035_NEXT_TARGET.csv",
            "1036-Y5-R10-parent-X-quadratic-action-and-beta-source-test-split.md",
            "1035 handoff to parent X quadratic action and beta split.",
        ),
        (
            "SRC1036_1_1035_kernel",
            "source-intake/mts_residuals/P8_Y5_R10_1035_KERNEL_DERIVATION_AUDIT.csv",
            "KXD1035_2_point_body_yukawa_match",
            "1035 conditional Green-kernel and point-body match.",
        ),
        (
            "SRC1036_2_1035_charge_split",
            "source-intake/mts_residuals/P8_Y5_R10_1035_SOURCE_TEST_CHARGE_SPLIT.csv",
            "BETA1035_1_universal_weyl",
            "1035 source/test product law and c_g-squared warning.",
        ),
        (
            "SRC1036_3_1025_hessian",
            "1025-Y5-R10-parent-Hessian-ZX-MX2-range-or-alpha-source-row.md",
            "SV1025_3_range_relation",
            "1025 exact second-variation/range contract.",
        ),
        (
            "SRC1036_4_1026_metric_fail",
            "1026-Y5-R10-parent-metric-ZXfX2-beta-eigenvalue-or-source-zero-return.md",
            "FAIL_CURRENT_CLAIM",
            "1026 parent metric/eigenvalue route failed.",
        ),
        (
            "SRC1036_5_1027_source_zero_fail",
            "1027-Y5-R10-qbarXT-source-zero-or-bounded-coupling-row.md",
            "FAIL_CURRENT_CLAIM",
            "1027 qbar_XT/J_X source-zero theorem failed current claim.",
        ),
        (
            "SRC1036_6_1028_no_marker_fail",
            "1028-Y5-R10-frame-marker-coupling-bound-input-pack-or-no-marker-theorem.md",
            "NM1028_6_verdict",
            "1028 no-marker/no-shadow coupling theorem remains unsigned.",
        ),
        (
            "SRC1036_7_617_field_space",
            "source-intake/mts_residuals/P8_Y5_R10_617_FIELD_SPACE_NORMALIZATION_ATTEMPT.csv",
            "FS617_5_finite_branch_ceiling",
            "617 finite-branch metric/normalization ceiling.",
        ),
        (
            "SRC1036_8_618_source_zero",
            "source-intake/mts_residuals/P8_Y5_R10_618_SOURCE_ZERO_CERTIFICATE_AUDIT.csv",
            "SZ618_5_full_source_zero_certificate",
            "618 source-zero certificate audit.",
        ),
        (
            "SRC1036_9_669_owner_gates",
            "source-intake/mts_residuals/P8_Y5_R10_669_LX_OWNER_GATE_TESTS.csv",
            "G669_0_branch_extremum",
            "669 L_X owner gates.",
        ),
        (
            "SRC1036_10_955_matter_lemma",
            "source-intake/mts_residuals/P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv",
            "MMA955_6_verdict",
            "955 minimal matter action lemma remains a contract, not a parent derivation.",
        ),
        (
            "SRC1036_11_bound_candidate",
            "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "R10_VECTOR_2020_REVIEW_0000",
            "1034 R10 bound review candidate, nonclaim.",
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


def parent_x_action_audit_rows() -> list[dict[str, str]]:
    return [
        {
            "audit_id": "PX1036_0_branch_extremum",
            "required_parent_object": "E_X|0=0",
            "candidate_formula": "delta S_parent/delta X evaluated on the local GR/Newton branch",
            "current_evidence": "1025/669 keep branch-extremum ownership missing",
            "result": "MISSING_PARENT_EULER_ZERO",
            "if_missing": "X=0 is not a stationary local vacuum; finite residual branch remains live",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "PX1036_1_quadratic_residue",
            "required_parent_object": "Z_X",
            "candidate_formula": "Z_X = coefficient of h^{ij} partial_i X partial_j X in delta^2 S_parent",
            "current_evidence": "1025 derives the role of Z_X, 617 says field-space metric is not parent-owned",
            "result": "MISSING_PARENT_KINETIC_RESIDUE",
            "if_missing": "K_X cannot be numeric and ghost/anti-elliptic branches are not excluded by theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "PX1036_2_mass_gap_range",
            "required_parent_object": "M_X^2 and lambda_X",
            "candidate_formula": "lambda_X=sqrt(Z_X/M_X^2), M_X^2=second derivative of parent potential in same normalization",
            "current_evidence": "1025 derives exact relation; 1026 fails to sign metric/eigenvalue",
            "result": "RELATION_DERIVED_VALUES_MISSING",
            "if_missing": "finite-range prediction is closure-only, not a parent prediction",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "PX1036_3_source_current",
            "required_parent_object": "J_X",
            "candidate_formula": "J_X = -delta_X S_matter - hidden/source/domain currents",
            "current_evidence": "618/1027/1028/955 give conditional descent/minimality lemmas but no parent signature",
            "result": "MISSING_SOURCE_ZERO_OR_SOURCE_LAW",
            "if_missing": "ordinary matter may source a finite X mode; R10/PPN/clock/orbital rows stay active",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "PX1036_4_source_test_betas",
            "required_parent_object": "beta_s and beta_t",
            "candidate_formula": "beta_i = partial_Xhat ln m_i^eff plus material/frame/readout terms",
            "current_evidence": "631/1035 define branches; no numeric or zero beta row is parent-signed",
            "result": "MISSING_BETA_SOURCE_TEST_SPLIT",
            "if_missing": "alpha(lambda) cannot be scored and c_g cannot be treated as a single linear coefficient",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "PX1036_5_no_pole_alternative",
            "required_parent_object": "physical X pole absent",
            "candidate_formula": "X is quotient/gauge/constraint-only before local inversion; no propagating Green kernel exists",
            "current_evidence": "618 no-green-function and 1022 quotient route are conditional, not parent-signed",
            "result": "NO_POLE_ROUTE_NOT_SIGNED",
            "if_missing": "must retain the finite pole template and bound it",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "PX1036_6_verdict",
            "required_parent_object": "single parent finite-X row",
            "candidate_formula": "parent_signed(E_X=0, Z_X>0, M_X^2>0, J_X/beta law, boundary/tails)",
            "current_evidence": "no inspected source closes all objects from one parent branch",
            "result": "FAIL_CURRENT_CLAIM_PARENT_ROW_NOT_OWNED",
            "if_missing": "demote finite-X R10 branch to explicit closure/nonclaim template",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def beta_derivation_rows() -> list[dict[str, str]]:
    return [
        {
            "derivation_id": "BETA1036_0_point_particle_source",
            "premise": "ordinary body i has effective rest mass m_i(Xhat)",
            "derivation": "S_i=-int m_i(Xhat) ds_i; delta_X S_i=-int m_i beta_i delta Xhat ds_i",
            "result": "beta_i := partial_Xhat ln m_i^eff; J_X contains beta_i m_i delta^3(x-x_i)",
            "status": "CONDITIONAL_STANDARD_VARIATION",
            "missing_for_claim": "parent-owned Xhat normalization and matter/readout mass functional",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "derivation_id": "BETA1036_1_two_body_exchange",
            "premise": "finite scalar-like X mode has static Green kernel",
            "derivation": "integrate out X between source and test currents",
            "result": "V_X(r)=-s_X beta_s beta_t m_s m_t exp(-r/lambda)/(4*pi Z_X r)",
            "status": "CONDITIONAL_EXCHANGE_LAW",
            "missing_for_claim": "sign s_X, Z_X, source/test beta rows, and profile projection",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "derivation_id": "BETA1036_2_R10_alpha_match",
            "premise": "R10 uses V=V_N[1+alpha exp(-r/lambda)]",
            "derivation": "divide V_X by -G_N m_s m_t exp(-r/lambda)/r under the same G calibration",
            "result": "alpha_X=s_X beta_s beta_t/(4*pi G_N Z_X) in nonabsorbed beta units; otherwise alpha_X=s_X beta_s beta_t by canonical scalar-tensor beta convention",
            "status": "CONDITIONAL_NORMALIZATION_SPLIT",
            "missing_for_claim": "which beta convention the parent action uses",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "derivation_id": "BETA1036_3_common_Weyl_cg",
            "premise": "m_i^eff=A_g(Xhat)m_i and A_g is universal",
            "derivation": "beta_s=partial_Xhat ln A_g=c_g and beta_t=c_g, up to profile/readout factors",
            "result": "alpha_X proportional to c_g^2 for universal source and test legs",
            "status": "CG_SQUARED_UNLESS_SOURCE_LEG_PACKED",
            "missing_for_claim": "parent-signed A_g branch, Xhat normalization, and source/test profile factors",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "derivation_id": "BETA1036_4_quotient_zero",
            "premise": "S_matter and constants descend through q and Lie_vX theta_A=0",
            "derivation": "chain rule gives delta_X S_matter=0 along v_X",
            "result": "beta_s=beta_t=0 and alpha_X=0 only if the descent/no-shadow/no-marker clauses are parent-signed together",
            "status": "CONDITIONAL_ZERO_NOT_SIGNED",
            "missing_for_claim": "parent q-kernel, matter functor, no-shadow frame, no-marker constants, and hidden-tail silence",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "derivation_id": "BETA1036_5_verdict",
            "premise": "current corpus only",
            "derivation": "compare available parent evidence to required source/test law",
            "result": "beta law is derived as a contract, but no numeric or zero beta source/test row is claim-ready",
            "status": "BETA_ROWS_UNOWNED",
            "missing_for_claim": "parent action schema or sourced beta bounds",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def branch_classification_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": "BR1036_0_no_physical_X_pole",
            "branch": "quotient/gauge/constraint X",
            "required_parent_signature": "X absent from physical quotient or first-class/constraint-only with no invertible local Green kernel",
            "R10_alpha_form": "alpha_X=0 or not_applicable",
            "current_status": "BEST_LOCAL_GR_ROUTE_BUT_UNSIGNED",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "next_action": "try no-physical-X-pole theorem before accepting finite residual branch",
            "generated_utc": stamp(),
        },
        {
            "branch_id": "BR1036_1_sourcefree_massive_nohair",
            "branch": "massive scalar-like X with no local source",
            "required_parent_signature": "Z_X>0, M_X^2>0, J_X=0, boundary_flux_X=0 from one parent branch",
            "R10_alpha_form": "alpha_X=0 in local exterior by energy identity",
            "current_status": "CONDITIONAL_NOHAIR_UNSIGNED",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "next_action": "only revive if source-zero and boundary flux close together",
            "generated_utc": stamp(),
        },
        {
            "branch_id": "BR1036_2_sourced_finite_exchange",
            "branch": "physical finite X exchange",
            "required_parent_signature": "Z_X, lambda_X, beta_s, beta_t, profile, sign, and tail envelope",
            "R10_alpha_form": "alpha_X=K_X^R10(lambda) beta_s beta_t + epsilon_tail",
            "current_status": "SCOREABLE_STRUCTURE_BUT_INPUTS_MISSING",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "next_action": "if no-pole fails, build bounded beta_s/beta_t rows without cancellation",
            "generated_utc": stamp(),
        },
        {
            "branch_id": "BR1036_3_shadow_frame_marker",
            "branch": "Weyl/disformal/marker leakage",
            "required_parent_signature": "A_g'(0), B_g'(0), b_A, b_alpha, q_nonH, support shifts are theorem-zero or bounded",
            "R10_alpha_form": "sum of absolute source/test leakage channels, not a single clean scalar alpha",
            "current_status": "RETAINED_TAIL_BRANCH",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "next_action": "route into no-cancellation tail envelope and cross-check WEP/clock/PPN",
            "generated_utc": stamp(),
        },
    ]


def parent_action_template_rows() -> list[dict[str, str]]:
    return [
        {
            "row_id": "PXA1036_0_finite_X_parent_row",
            "system_id": "MTS_local_R10_parent_action",
            "field_id": "X",
            "branch": "physical_finite_X_exchange",
            "action_density": "sqrt(-g)[-1/2 Z_X (partial X)^2 -1/2 M_X^2 X^2 + X J_X] plus declared boundary/tail terms",
            "Z_X": "MISSING_PARENT_KINETIC_RESIDUE",
            "M_X2": "MISSING_PARENT_MASS_GAP",
            "lambda_X": "MISSING_PARENT_RANGE",
            "J_X": "MISSING_SOURCE_CURRENT_OR_ZERO_THEOREM",
            "beta_source": "MISSING_BETA_SOURCE",
            "beta_test": "MISSING_BETA_TEST",
            "sign_sX": "MISSING_EXCHANGE_SIGN",
            "normalization": "MISSING_XHAT_AND_GN_CONVENTION",
            "tail_envelope": "MISSING_ABSOLUTE_TAIL_ENVELOPE",
            "source_paths": "1025;1026;1027;1028;1035",
            "current_status": "TEMPLATE_ONLY_PARENT_ROW_NOT_OWNED",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "PXA1036_1_no_pole_parent_row",
            "system_id": "MTS_local_R10_parent_action",
            "field_id": "X",
            "branch": "no_physical_X_pole",
            "action_density": "X is absent, pure quotient/gauge, or algebraic constraint with no propagating local pole",
            "Z_X": "not_applicable_if_no_pole_signed",
            "M_X2": "not_applicable_if_no_pole_signed",
            "lambda_X": "not_applicable_if_no_pole_signed",
            "J_X": "zero_or_constraint_current_only_if_parent_signed",
            "beta_source": "0_if_matter_descends_and_no_shadow_signed",
            "beta_test": "0_if_matter_descends_and_no_shadow_signed",
            "sign_sX": "not_applicable",
            "normalization": "quotient_owned_observable_only",
            "tail_envelope": "hidden_tails_zero_or_bounded_required",
            "source_paths": "618;1022;1027;1028;1031",
            "current_status": "BEST_THEOREM_ROUTE_UNSIGNED",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def mts_template_rows() -> list[dict[str, str]]:
    return [
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "parent_X_beta_product_template",
            "curve_id": "R10_alpha_lambda_curve_MTS_1036_PARENT_X_BETA_TEMPLATE_NONCLAIM",
            "lambda_value": "MISSING_PARENT_LAMBDA_X",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_KX_BETA_SOURCE_BETA_TEST_TAIL_ENVELOPE",
            "alpha_bound": "MISSING_PROMOTED_R10_ALPHA_BOUND_CURVE",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv is review-only",
            "force_law_form": "alpha_X(lambda)=K_X^R10(lambda) beta_s(lambda) beta_t(lambda)+epsilon_tail(lambda)",
            "derivation_status": "template_invalid_missing_parent_action_row_and_beta_split",
            "formula_reference": "1036-Y5-R10-parent-X-quadratic-action-and-beta-source-test-split.md::BETA1036_2",
            "source_file": "MISSING_PARENT_SOURCE_FILE",
            "assumptions": "two-body source-test product; no linear-c_g shortcut; no cancellation credit",
            "valid_for_claim": "false",
            "notes": "Updated 1036 template blocks any single-coupling alpha scoring.",
        },
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "universal_weyl_cg_squared_template",
            "curve_id": "R10_alpha_lambda_curve_MTS_1036_PARENT_X_BETA_TEMPLATE_NONCLAIM",
            "lambda_value": "MISSING_PARENT_LAMBDA_X",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_NUMERIC_KX_TIMES_CG_SQUARED_AND_PROFILE",
            "alpha_bound": "MISSING_PROMOTED_R10_ALPHA_BOUND_CURVE",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv is review-only",
            "force_law_form": "universal Weyl finite exchange: alpha_X proportional to K_X^R10 c_g^2",
            "derivation_status": "template_invalid_missing_parent_cg_ZX_lambda_and_profile",
            "formula_reference": "1036-Y5-R10-parent-X-quadratic-action-and-beta-source-test-split.md::BETA1036_3",
            "source_file": "MISSING_PARENT_SOURCE_FILE",
            "assumptions": "source and test legs both carry c_g unless source leg is explicitly packed into Qbar_XH",
            "valid_for_claim": "false",
            "notes": "This is the corrected coupling law, still not a claim row.",
        },
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "no_physical_X_pole_template",
            "curve_id": "R10_alpha_lambda_curve_MTS_1036_PARENT_X_BETA_TEMPLATE_NONCLAIM",
            "lambda_value": "ALL_LOCAL_R10_RANGE",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_NO_PHYSICAL_X_POLE_THEOREM",
            "alpha_bound": "not_applicable_until_no_pole_theorem_signed",
            "alpha_bound_source": "not_applicable_until_no_pole_theorem_signed",
            "force_law_form": "no finite Yukawa alpha if X has no physical pole and hidden tails are zero/bounded",
            "derivation_status": "template_invalid_missing_no_pole_parent_action_signature",
            "formula_reference": "1036-Y5-R10-parent-X-quadratic-action-and-beta-source-test-split.md::BR1036_0",
            "source_file": "MISSING_PARENT_SOURCE_FILE",
            "assumptions": "strongest local-GR route, but not signed",
            "valid_for_claim": "false",
            "notes": "Do not report alpha=0 until no-pole and hidden-tail clauses close.",
        },
    ]


def join_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "JOIN1036_0_parent_row",
            "object": "parent finite-X row",
            "required_for_claim": "E_X=0, Z_X, M_X2, lambda_X, J_X/beta law, sign, boundary/tails from one parent branch",
            "current_status": "MISSING_PARENT_ROW",
            "ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "JOIN1036_1_beta_product",
            "object": "beta_s beta_t",
            "required_for_claim": "numeric/source-backed or zero-theorem beta_source and beta_test rows",
            "current_status": "MISSING_BETA_SOURCE_TEST_SPLIT",
            "ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "JOIN1036_2_cg_law",
            "object": "c_g versus c_g^2 policy",
            "required_for_claim": "explicit declaration whether Qbar_XH already contains the source leg",
            "current_status": "LAW_CORRECTED_NO_NUMERIC_INPUTS",
            "ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "JOIN1036_3_external_bound",
            "object": "R10 alpha_bound(lambda)",
            "required_for_claim": "promoted digitized/official bound curve",
            "current_status": "REVIEW_CANDIDATE_NONCLAIM",
            "ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "JOIN1036_4_no_cancellation",
            "object": "absolute tail envelope",
            "required_for_claim": "all hidden/marker/disformal/non-Hilbert/support terms zero or bounded in absolute sum",
            "current_status": "MISSING_ABSOLUTE_TAIL_ENVELOPE",
            "ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def runner_smoke_rows(status: dict[str, object]) -> list[dict[str, str]]:
    return [
        {
            "smoke_id": "SMOKE1036_0_runner_status",
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


def placeholder_refusal_rows(template_rows: list[dict[str, str]], join_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, row in enumerate(template_rows):
        rows.append(
            {
                "refusal_id": f"REF1036_TEMPLATE_{index}",
                "object": row["row_id"],
                "current_status": row["current_status"],
                "refusal_status": "rejected_parent_action_template_only",
                "failure_reasons": "MISSING_PARENT_INPUTS;NOT_SCORE_READY;CLAIM_POLICY_FALSE",
                "score_eligible": "false",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    for index, row in enumerate(join_rows):
        rows.append(
            {
                "refusal_id": f"REF1036_JOIN_{index}",
                "object": row["object"],
                "current_status": row["current_status"],
                "refusal_status": "rejected_join_gate_not_ready",
                "failure_reasons": f"{row['current_status']};READY_FALSE;CLAIM_POLICY_FALSE",
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
            "gate_id": "CGATE1036_0_parent_action_row",
            "claim": "single parent action supplies the finite-X row",
            "gate_pass": "false",
            "reason": "E_X, Z_X, M_X2/lambda_X, J_X, beta split, and tails are not parent-signed together",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1036_1_numeric_alpha",
            "claim": "MTS has numeric alpha_predicted(lambda)",
            "gate_pass": "false",
            "reason": "K_X, beta_s, beta_t, lambda_X, profile, and promoted bound curve are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1036_2_linear_cg",
            "claim": "R10 alpha may be scored as linear in c_g",
            "gate_pass": "false",
            "reason": "source-test exchange gives c_g squared for universal Weyl legs unless source leg is explicitly included elsewhere",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1036_3_no_pole",
            "claim": "no physical X pole is derived",
            "gate_pass": "false",
            "reason": "no-pole/quotient route remains conditional in 618/1022/1027/1028",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1036_4_local_GR_R10",
            "claim": "local GR/R10 pass is established",
            "gate_pass": "false",
            "reason": "parent-action row and empirical score inputs remain nonclaim",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1036_0_parent_row_status",
            "decision": "The parent finite-X quadratic row is not owned by the current corpus.",
            "because": "the necessary pieces exist only as conditional contracts spread across 1025, 1026, 1027, 1028, and 1035.",
            "next_action": "keep the finite-X branch as a closure/nonclaim template unless a parent action signs all pieces",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1036_1_coupling_law_status",
            "decision": "The corrected coupling law is beta_source times beta_test.",
            "because": "two-body exchange forbids a single naked coupling coefficient; universal c_g enters twice.",
            "next_action": "update future R10 templates to require beta_s, beta_t, and a declaration of whether Qbar_XH already includes a source leg",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1036_2_best_route",
            "decision": "The least-scrutiny route is still no physical X pole; the fallback is bounded beta rows.",
            "because": "a derived no-pole/constraint branch gives GR reduction cleaner than tuning a short-range scalar; if it fails, empirical bound rows are honest.",
            "next_action": "try no-physical-X-pole theorem first, then bounded beta_s/beta_t acquisition",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1036_3_next_target",
            "decision": "Next target is no physical X pole or first bounded beta source/test runner.",
            "because": "this is the fork that decides whether local GR is derived structurally or tested as a finite residual.",
            "next_action": "1037-Y5-R10-no-physical-X-pole-theorem-or-bounded-beta-runner.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1037-Y5-R10-no-physical-X-pole-theorem-or-bounded-beta-runner.md",
            "objective": "try to prove the finite local X mode has no physical pole in the GR/Newton branch; if not, build a bounded beta_source/beta_test acquisition runner with no-cancellation tails",
            "include": "quotient/gauge/constraint pole audit, Hessian degeneracy or first-class certificate, algebraic constraint alternative, beta_s/beta_t row schema, c_g^2 convention, R10/PPN/clock/WEP routing",
            "exclude": "asserted alpha=0, invented beta/c_g values, linear-c_g R10 score, cancellation between unknown tails, R10 pass claim, formalization-workbench edits, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validate(
    source_rows: list[dict[str, str]],
    action_rows: list[dict[str, str]],
    beta_rows: list[dict[str, str]],
    branch_rows: list[dict[str, str]],
    parent_template: list[dict[str, str]],
    mts_rows: list[dict[str, str]],
    join_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(
        (
            "V1036_0_sources_exist",
            all(flag(row["exists"]) and flag(row["needle_found"]) for row in source_rows),
            "all 1036 source paths exist and expected needles are present",
        )
    )
    checks.append(
        (
            "V1036_1_parent_action_audit_complete",
            len(action_rows) >= 7
            and any(row["result"] == "FAIL_CURRENT_CLAIM_PARENT_ROW_NOT_OWNED" for row in action_rows),
            "parent action audit covers all required finite-X owner objects and verdict",
        )
    )
    checks.append(
        (
            "V1036_2_beta_product_law",
            any("beta_s beta_t" in row["result"] for row in beta_rows)
            and any("c_g^2" in row["result"] for row in beta_rows),
            "beta source/test product and c_g-squared law are explicit",
        )
    )
    checks.append(
        (
            "V1036_3_branch_fork_complete",
            {row["branch_id"] for row in branch_rows}
            == {"BR1036_0_no_physical_X_pole", "BR1036_1_sourcefree_massive_nohair", "BR1036_2_sourced_finite_exchange", "BR1036_3_shadow_frame_marker"},
            "branch classification covers no-pole, nohair, finite exchange, and tail branches",
        )
    )
    checks.append(
        (
            "V1036_4_parent_templates_nonclaim",
            all(row["score_ready"] == "false" and not flag(row["valid_for_claim"]) for row in parent_template),
            "parent action templates are nonclaim and unscoreable",
        )
    )
    checks.append(
        (
            "V1036_5_mts_template_schema",
            bool(mts_rows) and set(MTS_REQUIRED_COLUMNS).issubset(set(mts_rows[0].keys())),
            "MTS R10 alpha template has the existing runner schema",
        )
    )
    checks.append(
        (
            "V1036_6_mts_template_nonclaim",
            bool(mts_rows) and all(not flag(row["valid_for_claim"]) for row in mts_rows),
            "MTS R10 alpha rows remain nonclaim",
        )
    )
    checks.append(
        (
            "V1036_7_join_gates_blocked",
            all(row["ready"] == "false" and not flag(row["valid_for_claim"]) for row in join_rows),
            "all join gates remain blocked",
        )
    )
    checks.append(
        (
            "V1036_8_runner_smoke_refuses_claim",
            bool(smoke_rows)
            and smoke_rows[0]["R10_pass_for_claim"] == "false"
            and smoke_rows[0]["claim_allowed"] == "false",
            "existing R10 runner refuses the 1036 nonclaim smoke rows",
        )
    )
    checks.append(
        (
            "V1036_9_claim_gates_blocked",
            all(not flag(row["claim_allowed"]) and not flag(row["valid_for_claim"]) for row in claim_rows),
            "all claim gates refuse promotion",
        )
    )
    checks.append(
        (
            "V1036_10_next_target_written",
            bool(next_rows)
            and next_rows[0]["next_target"] == "1037-Y5-R10-no-physical-X-pole-theorem-or-bounded-beta-runner.md",
            "next target row is present",
        )
    )
    generated_files = [
        DOC,
        OUT / "P8_Y5_R10_1036_SOURCE_REGISTER.csv",
        OUT / "P8_Y5_R10_1036_PARENT_X_ACTION_AUDIT.csv",
        OUT / "P8_Y5_R10_1036_BETA_SOURCE_TEST_DERIVATION.csv",
        OUT / "P8_Y5_R10_1036_BRANCH_CLASSIFICATION.csv",
        OUT / "P8_Y5_R10_1036_PARENT_ACTION_ROW_TEMPLATE.csv",
        OUT / "P8_Y5_R10_1036_JOIN_GATES.csv",
        OUT / "P8_Y5_R10_1036_RUNNER_SMOKE_STATUS.csv",
        OUT / "P8_Y5_R10_1036_PLACEHOLDER_REFUSAL_RUNNER.csv",
        OUT / "P8_Y5_R10_1036_CLAIM_GATES.csv",
        OUT / "P8_Y5_R10_1036_DECISION_LEDGER.csv",
        OUT / "P8_Y5_R10_1036_NEXT_TARGET.csv",
        OUT / "P8_Y5_BRR545_1036_VALIDATION.csv",
        MTS_TEMPLATE,
    ]
    checks.append(
        (
            "V1036_11_generated_files_in_post_checkpoint",
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
            "V1036_12_formalization_untouched",
            not formalization_touches,
            f"formalization-workbench modified-file count since script start is {len(formalization_touches)}",
        )
    )
    rows = [
        {
            "check_id": "V1036_SUMMARY",
            "result": "pass" if all(result for _, result, _ in checks) else "fail",
            "detail": "1036 parent X action and beta source/test validation summary",
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
    action_rows: list[dict[str, str]],
    beta_rows: list[dict[str, str]],
    branch_rows: list[dict[str, str]],
    parent_template: list[dict[str, str]],
    mts_rows: list[dict[str, str]],
    join_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
    refusal_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    sections = [
        "# 1036 Y5 R10 parent X quadratic action and beta source/test split",
        "",
        "**Status:** The parent finite-`X` action row is **not owned** by the current corpus. The exact contract is now explicit: a claim-grade finite local branch needs `E_X|0=0`, `Z_X`, `M_X^2/lambda_X`, `J_X`, `beta_s`, `beta_t`, exchange sign, profile projection, and retained-tail envelope from one parent branch.",
        "",
        "**Main physics correction retained:** the R10 coefficient is a two-body exchange product. In a universal Weyl branch, `beta_s=beta_t=c_g` up to profile factors, so `alpha_X` scales like `c_g^2`, not a single linear `c_g`, unless `Qbar_XH` explicitly already contains the source leg.",
        "",
        "**Claim ceiling:** no numeric `K_X`, no finite `lambda_X`, no `alpha=0`, no linear-`c_g` R10 score, no R10/local-GR pass, no GitHub action, and no `formalization-workbench` edit is allowed from 1036.",
        "",
        "## Source register",
        md_table(source_rows, ["source_id", "source_path", "exists", "needle_found", "role"]),
        "## Parent X action audit",
        md_table(action_rows, ["audit_id", "required_parent_object", "candidate_formula", "result", "if_missing", "valid_for_claim"]),
        "## Beta source/test derivation",
        md_table(beta_rows, ["derivation_id", "premise", "result", "status", "missing_for_claim", "valid_for_claim"]),
        "## Branch classification",
        md_table(branch_rows, ["branch_id", "branch", "required_parent_signature", "R10_alpha_form", "current_status", "next_action", "valid_for_claim"]),
        "## Parent action row template",
        md_table(parent_template, ["row_id", "branch", "action_density", "Z_X", "M_X2", "lambda_X", "J_X", "beta_source", "beta_test", "current_status", "score_ready", "valid_for_claim"]),
        "## R10 alpha template update",
        md_table(mts_rows, ["model_id", "branch_id", "lambda_value", "alpha_predicted", "force_law_form", "derivation_status", "valid_for_claim"]),
        "## Join gates",
        md_table(join_rows, ["gate_id", "object", "required_for_claim", "current_status", "ready", "valid_for_claim"]),
        "## Runner smoke status",
        md_table(smoke_rows, ["smoke_id", "valid_mts_rows", "valid_bound_rows", "comparison_rows", "R10_pass_for_claim", "claim_allowed", "expected_result"]),
        "## Placeholder refusal runner",
        md_table(refusal_rows, ["refusal_id", "object", "current_status", "refusal_status", "failure_reasons", "score_eligible", "claim_allowed"]),
        "## Claim gates",
        md_table(claim_rows, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
        "## Decision ledger",
        md_table(decision_rows, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
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
    action_rows = parent_x_action_audit_rows()
    beta_rows = beta_derivation_rows()
    branch_rows = branch_classification_rows()
    parent_template = parent_action_template_rows()
    mts_rows = mts_template_rows()
    join_rows = join_gate_rows()

    write_csv(MTS_TEMPLATE, mts_rows, MTS_REQUIRED_COLUMNS)
    runner_result = run_runner(MTS_TEMPLATE, BOUND_CANDIDATE, RUN_DIR)
    smoke_rows = runner_smoke_rows(runner_result["status"])
    refusal_rows = placeholder_refusal_rows(parent_template, join_rows)
    claim_rows = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    validation = validate(
        source_rows,
        action_rows,
        beta_rows,
        branch_rows,
        parent_template,
        mts_rows,
        join_rows,
        smoke_rows,
        claim_rows,
        next_rows,
    )

    write_csv(OUT / "P8_Y5_R10_1036_SOURCE_REGISTER.csv", source_rows)
    write_csv(OUT / "P8_Y5_R10_1036_PARENT_X_ACTION_AUDIT.csv", action_rows)
    write_csv(OUT / "P8_Y5_R10_1036_BETA_SOURCE_TEST_DERIVATION.csv", beta_rows)
    write_csv(OUT / "P8_Y5_R10_1036_BRANCH_CLASSIFICATION.csv", branch_rows)
    write_csv(OUT / "P8_Y5_R10_1036_PARENT_ACTION_ROW_TEMPLATE.csv", parent_template)
    write_csv(OUT / "P8_Y5_R10_1036_JOIN_GATES.csv", join_rows)
    write_csv(OUT / "P8_Y5_R10_1036_RUNNER_SMOKE_STATUS.csv", smoke_rows)
    write_csv(OUT / "P8_Y5_R10_1036_PLACEHOLDER_REFUSAL_RUNNER.csv", refusal_rows)
    write_csv(OUT / "P8_Y5_R10_1036_CLAIM_GATES.csv", claim_rows)
    write_csv(OUT / "P8_Y5_R10_1036_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_1036_NEXT_TARGET.csv", next_rows)
    write_csv(OUT / "P8_Y5_BRR545_1036_VALIDATION.csv", validation)
    write_doc(
        source_rows,
        action_rows,
        beta_rows,
        branch_rows,
        parent_template,
        mts_rows,
        join_rows,
        smoke_rows,
        refusal_rows,
        claim_rows,
        decisions,
        validation,
        next_rows,
    )

    if validation[0]["result"] != "pass":
        failed = [row for row in validation if row["result"] == "fail"]
        raise SystemExit(f"1036 validation failed: {failed}")


if __name__ == "__main__":
    main()
