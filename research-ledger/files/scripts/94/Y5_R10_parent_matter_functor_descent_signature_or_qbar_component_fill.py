from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from R10_alpha_lambda_bound_prediction_runner import MTS_REQUIRED_COLUMNS, run_runner


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
DOC = ROOT / "1045-Y5-R10-parent-matter-functor-descent-signature-or-qbar-component-fill.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1045-R10-parent-matter-functor-qbar-component-nonclaim-smoke" / "results"
MTS_TEMPLATE = OUT / "R10_alpha_lambda_curve_MTS_1045_QBAR_COMPONENT_TEMPLATE_NONCLAIM.csv"
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


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        (
            "SRC1045_0_1044_next",
            "source-intake/mts_residuals/P8_Y5_R10_1044_NEXT_TARGET.csv",
            "1045-Y5-R10-parent-matter-functor-descent-signature-or-qbar-component-fill.md",
            "1044 handoff to parent matter functor descent.",
        ),
        (
            "SRC1045_1_1044_derivation",
            "source-intake/mts_residuals/P8_Y5_R10_1044_MATTER_PULLBACK_DERIVATION.csv",
            "MPD1044_7_exact_theorem_if_signed",
            "Exact conditional matter-pullback theorem from 1044.",
        ),
        (
            "SRC1045_2_1044_qbar_components",
            "source-intake/mts_residuals/P8_Y5_R10_1044_QBARXT_COMPONENT_ENVELOPE.csv",
            "QBC1044_0_qbar_geom",
            "1044 qbar_geom placeholder requiring a descent certificate or numeric bound.",
        ),
        (
            "SRC1045_3_410_functor",
            "410-quotient-matter-functor-theorem-attempt.md",
            "Conditional Functor Theorem",
            "Early quotient-matter functor theorem attempt.",
        ),
        (
            "SRC1045_4_626_descent",
            "626-Y5-R10-quotient-invariant-matter-action-signature-or-cg-bound-input.md",
            "Descent Criterion",
            "Quotient-invariant matter action descent criterion.",
        ),
        (
            "SRC1045_5_710_descent_clause",
            "source-intake/mts_residuals/P8_Y5_R10_710_DESCENT_PARENT_ACTION_CLAUSE.csv",
            "DPC710_3_matter_functor_blind",
            "Candidate parent action clause for matter blindness.",
        ),
        (
            "SRC1045_6_711_audit",
            "source-intake/mts_residuals/P8_Y5_R10_711_QUOTIENT_DESCENT_DERIVATION_AUDIT.csv",
            "QDA711_4_matter_functor_factorization",
            "Quotient descent derivation audit.",
        ),
        (
            "SRC1045_7_761_vertical",
            "source-intake/mts_residuals/P8_Y5_R10_761_PARENT_MATTER_VERTICAL_ACTION_CONTRACT.csv",
            "MVA761_5_evaluability_verdict",
            "Vertical action on matter-domain contract.",
        ),
        (
            "SRC1045_8_767_reaudit",
            "source-intake/mts_residuals/P8_Y5_R10_767_PARENT_MATTER_FUNCTOR_REAUDIT.csv",
            "PMR767_0_explicit_parent_matter_functor",
            "Reaudit of parent matter functor signature.",
        ),
        (
            "SRC1045_9_898_signature",
            "source-intake/mts_residuals/P8_Y5_R10_898_MATTER_DESCENT_SIGNATURE.csv",
            "MDS898_5_verdict",
            "Matter descent source-cokernel verdict.",
        ),
        (
            "SRC1045_10_594_blindness",
            "source-intake/mts_residuals/P8_Y5_R10_594_MATTER_BLINDNESS_GATE.csv",
            "MBG594_0_metric_blindness",
            "Matter blindness gate and universal conformal counterexample.",
        ),
        (
            "SRC1045_11_622_contract",
            "source-intake/mts_residuals/P8_Y5_R10_622_PARENT_MATTER_CONTRACT.csv",
            "PMC622_8_contract_verdict",
            "Parent matter contract verdict.",
        ),
        (
            "SRC1045_12_736_no_marker",
            "source-intake/mts_residuals/P8_Y5_R10_736_MATTER_NO_MARKER_CONTRACT.csv",
            "NMC736_3_shadow_frame_forbidden",
            "No hidden conformal/disformal frame guard.",
        ),
        (
            "SRC1045_13_955_minimal",
            "source-intake/mts_residuals/P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv",
            "MMA955_6_verdict",
            "Minimal matter action lemma.",
        ),
        (
            "SRC1045_14_1027_qbar_schema",
            "source-intake/mts_residuals/P8_Y5_R10_1027_BOUNDED_QBARXT_ROW_SCHEMA.csv",
            "BQT1027_0_visible_geometry",
            "Bounded qbarXT visible-geometry schema.",
        ),
        (
            "SRC1045_15_local_bounds",
            "source-intake/local_bounds/local_bound_claims.csv",
            "R1_WEP_source_charge",
            "WEP source-charge bound anchor.",
        ),
        (
            "SRC1045_16_R10_bound_candidate",
            "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "R10_VECTOR_2020_REVIEW_0000",
            "R10 nonclaim review-candidate curve for smoke only.",
        ),
        (
            "SRC1045_17_R10_runner",
            "scripts/R10_alpha_lambda_bound_prediction_runner.py",
            "MTS_REQUIRED_COLUMNS",
            "Existing R10 runner and schema.",
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


def functor_signature_rows() -> list[dict[str, str]]:
    return [
        {
            "signature_id": "MFS1045_0_parent_field_quotient",
            "required_signature": "q_loc: Phi_parent -> Q_loc exists and v_X in ker(Dq_loc)",
            "mathematical_effect": "Dq_loc[v_X]=0 is the only legal reason a representative motion is invisible to observed matter.",
            "current_evidence": "410/626/711 give the criterion and older quotient route, but not a fully parent-derived quotient object for all local sectors.",
            "current_status": "CONDITIONAL_SUPPORT_NOT_PARENT_COMPLETE",
            "if_signed": "feeds geometry descent and qbar_geom zero theorem",
            "if_unsigned": "qbar_geom remains a live frame-leak component",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "signature_id": "MFS1045_1_observed_coframe_functor",
            "required_signature": "e_obs = Obs_e(q_loc(Phi)); g_obs = eta_ab e_obs^a e_obs^b; omega_obs = omega[e_obs] or owned connection",
            "mathematical_effect": "Lie_v e_obs = D Obs_e[Dq_loc[v_X]] = 0 and Lie_v g_obs = 0 for vertical representative v_X.",
            "current_evidence": "1044 states this as the geometry-pullback zero condition; 898 keeps the geometry stack descent unsigned.",
            "current_status": "SUFFICIENT_SIGNATURE_NOT_PARENT_SIGNED",
            "if_signed": "qbar_geom visible-geometry component is theorem-zero",
            "if_unsigned": "hidden conformal/disformal or connection re-entry remains legal",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "signature_id": "MFS1045_2_matter_bundle_functor",
            "required_signature": "Psi_A in Gamma(E_A[e_obs]) and S_A = S_A[Psi_A,e_obs,omega[e_obs],theta_A]",
            "mathematical_effect": "defines the matter domain before coupling tests and prevents a fitted/readout matter frame from being inserted later.",
            "current_evidence": "761 says this is admissible but not parent-constructed; 767 says explicit parent matter functor remains unsigned.",
            "current_status": "MATTER_CATEGORY_NOT_PARENT_CONSTRUCTED",
            "if_signed": "vertical action on matter becomes evaluable",
            "if_unsigned": "matter frame/source split can be smuggled as a physical residual",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "signature_id": "MFS1045_3_vertical_lift",
            "required_signature": "delta_v Psi_A = 0, or delta_v Psi_A is an owned gauge/local Lorentz/diffeomorphism lift with boundary-only variation",
            "mathematical_effect": "E_Psi terms vanish on shell and gauge/lift terms cannot create physical qbar charge.",
            "current_evidence": "761 gives clean fixed/gauge options but says no parent map assigns v_X to every ordinary species.",
            "current_status": "VERTICAL_LIFT_NOT_PARENT_SIGNED",
            "if_signed": "matter field variation cannot reopen qbar_geom",
            "if_unsigned": "fixed-Psi choice is convention rather than theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "signature_id": "MFS1045_4_no_shadow_frame",
            "required_signature": "no hidden A_A(X)^2 g_obs, B_A(X) disformal frame, source-only metric, post-readout EFT frame, or material marker enters S_A",
            "mathematical_effect": "rules out universal-but-nonzero fifth force and species-dependent source charge counterexamples.",
            "current_evidence": "594 and 736 identify the exact shadow-frame loophole; 767 says no alpha/mass vertex remains hard-blocked.",
            "current_status": "GUARD_WRITTEN_NOT_PARENT_DERIVED",
            "if_signed": "qbar_marker can be theorem-zero for shadow-frame channel",
            "if_unsigned": "qbar_marker and qbar_geom coefficient rows stay mandatory",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "signature_id": "MFS1045_5_constants_split",
            "required_signature": "theta_A are fixed representation/superselection data or explicitly retained residual fields; Lie_v theta_A=0 for ordinary matter",
            "mathematical_effect": "prevents masses, charges, alpha_EM, and clock constants from sourcing qbar_XT.",
            "current_evidence": "1044 and 898 preserve the constant/superselection route but mark it unsigned.",
            "current_status": "CONSTANT_SUPERSELECTION_UNSIGNED",
            "if_signed": "qbar_constants/qbar_marker components narrow sharply",
            "if_unsigned": "clock/WEP/fine-structure rows remain active",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "signature_id": "MFS1045_6_verdict",
            "required_signature": "MFS1045_0 through MFS1045_5 are parent-derived in one action signature",
            "mathematical_effect": "would prove qbar_geom=0 and supply the ordinary-matter piece needed by MPD1044_7.",
            "current_evidence": "All pieces exist as contracts/conditional lemmas; no current source signs them as a single parent action.",
            "current_status": "FAIL_CURRENT_CLAIM_PARENT_MATTER_FUNCTOR_NOT_SIGNED",
            "if_signed": "qbar_geom zero can be promoted for ordinary matter only",
            "if_unsigned": "fill qbar_geom/qbar_marker component rows as nonclaim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def vertical_lift_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "VLG1045_0_fixed_lift",
            "lift_option": "fixed ordinary matter",
            "condition": "delta_v Phi=v_X, Dq[v_X]=0, delta_v Psi_A=0, delta_v theta_A=0",
            "derives": "Lie_v S_A reduces to geometry/constant/boundary terms",
            "current_status": "CLEAN_OPTION_NOT_PARENT_SIGNED",
            "risk_if_used": "freezing matter is a convention unless v_X is a redundancy of the parent matter bundle",
            "gate_pass": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "VLG1045_1_gauge_lift",
            "lift_option": "owned gauge lift",
            "condition": "delta_v Psi_A = rho_A(lambda_v)Psi_A or L_xi Psi_A with delta_v S_A boundary/gauge only",
            "derives": "vertical motion is observable-trivial without hand-freezing Psi_A",
            "current_status": "STANDARD_FORM_ALLOWED_NOT_PARENT_SIGNED",
            "risk_if_used": "no parent map currently assigns v_X to a gauge lift for every matter species",
            "gate_pass": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "VLG1045_2_physical_lift_forbidden",
            "lift_option": "exclude physical species/material lift",
            "condition": "vertical representative motion may not change mass ratios, charges, clocks, or material markers unless retained as residuals",
            "derives": "prevents qbar_marker from hiding under the functor theorem",
            "current_status": "NOT_PARENT_SIGNED",
            "risk_if_used": "direct clock/EM/source marker spurions can fake descent",
            "gate_pass": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "VLG1045_3_boundary_lift",
            "lift_option": "matter-domain boundary behaviour",
            "condition": "delta_v S_A boundary term is compact-support zero, owned gauge exact, or separately retained with a source-backed projection",
            "derives": "descent does not hide source-worldtube/edge charge",
            "current_status": "OPEN",
            "risk_if_used": "qbar_nonH/support-shift channel remains possible",
            "gate_pass": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "VLG1045_4_verdict",
            "lift_option": "vertical lift descent",
            "condition": "one fixed/gauge lift plus no physical species lift plus boundary silence is parent-signed",
            "derives": "the matter-domain part of Lie_v S_A is zero or owned",
            "current_status": "FAIL_CURRENT_CLAIM_VERTICAL_LIFT_NOT_SIGNED",
            "risk_if_used": "qbar_geom zero would be overclaimed",
            "gate_pass": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def qbar_geom_attempt_rows() -> list[dict[str, str]]:
    return [
        {
            "attempt_id": "QG1045_0_definition",
            "object": "visible geometry charge",
            "formula": "qbar_geom = (2 M_T)^-1 int_T sqrt(-g_hat) T_T^{mu nu} Lie_v ghat_munu",
            "zero_route": "if ghat = g_obs(q_loc(Phi)) and Dq_loc[v_X]=0, then Lie_v ghat=0",
            "current_status": "FORMULA_RESTATED",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "QG1045_1_functor_chain_rule",
            "object": "coframe functor derivative",
            "formula": "Lie_v e_obs = D Obs_e|_{q_loc(Phi)}[Dq_loc(v_X)]",
            "zero_route": "Dq_loc(v_X)=0 implies Lie_v e_obs=0",
            "current_status": "EXACT_CONDITIONAL_SUBLEMMA",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "QG1045_2_connection_stack",
            "object": "omega/connection descent",
            "formula": "Lie_v omega[e_obs]=0 if omega is Levi-Civita/coframe-owned; independent connection requires its own descent row",
            "zero_route": "coframe descent plus no independent connection source",
            "current_status": "CONDITIONAL_CONNECTION_CAVEAT",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "QG1045_3_shadow_countermodel",
            "object": "universal conformal/disformal leakage",
            "formula": "g_hat_A = exp(2 b_A X) g_obs + d_A(X) u_mu u_nu + ... gives qbar_geom != 0 even if b_A is universal",
            "zero_route": "exclude shadow frame by parent action or retain b_A,d_A component rows",
            "current_status": "COUNTERMODEL_RETAINED",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "QG1045_4_current_verdict",
            "object": "qbar_geom=0",
            "formula": "qbar_geom=0 iff MFS1045_0 through MFS1045_4 and VLG1045 gates are signed",
            "zero_route": "parent functor descent theorem",
            "current_status": "FAIL_CURRENT_CLAIM_QBAR_GEOM_ZERO_NOT_SIGNED",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def qbar_component_fill_rows() -> list[dict[str, str]]:
    return [
        {
            "component_id": "QCF1045_0_qbar_geom_zero_candidate",
            "symbol": "qbar_geom",
            "value": "0_IF_PARENT_MATTER_FUNCTOR_DESCENT_SIGNED",
            "units": "dimensionless",
            "formula": "qbar_geom = (2 M_T)^-1 int sqrt(-g_hat) T_T^{mu nu} Lie_v ghat_munu",
            "required_source": "P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv::MFS1045_6_verdict must become signed",
            "bound_link": "R10;PPN;clock;WEP_direct_geometry",
            "current_status": "THEOREM_ZERO_CANDIDATE_BLOCKED",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "component_id": "QCF1045_1_qbar_geom_numeric_placeholder",
            "symbol": "qbar_geom",
            "value": "MISSING_LIE_V_GHAT_OR_FRAME_LEAK_COEFFICIENT",
            "units": "MISSING_UNITS",
            "formula": "|qbar_geom| <= 1/2 sup_T |T^{mu nu} Lie_v ghat_munu|/M_T with declared normalization",
            "required_source": "MISSING_SOURCE_FILE",
            "bound_link": "R10 alpha_X(lambda); PPN frame leakage; clock/frame tests",
            "current_status": "NUMERIC_TEMPLATE_ONLY",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "component_id": "QCF1045_2_qbar_marker_shadow_frame",
            "symbol": "qbar_marker",
            "value": "MISSING_B_CONF_B_DIS_MARKER_COEFFICIENTS",
            "units": "dimensionless_after_sensitivity_normalization",
            "formula": "|qbar_marker| <= |b_conf| + |b_dis| + sum_A |s_A b_A| + post-readout marker terms",
            "required_source": "parent no-shadow-frame theorem or source-backed coefficients",
            "bound_link": "WEP_source_charge;clock;R10;R11",
            "current_status": "SHADOW_FRAME_COMPONENT_TEMPLATE_ONLY",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "component_id": "QCF1045_3_no_cancellation_guard",
            "symbol": "qbar_component_total_policy",
            "value": "not_numeric",
            "units": "policy",
            "formula": "|qbar_XT| <= |qbar_geom| + |qbar_constants| + |qbar_marker| + |qbar_source_weight| + |qbar_nonH|",
            "required_source": "P8_Y5_R10_1044_QBARXT_COMPONENT_ENVELOPE.csv::QBC1044_5_total_abs_guard",
            "bound_link": "all local arenas",
            "current_status": "NO_CANCELLATION_GUARD_RETAINED",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def bound_anchor_rows() -> list[dict[str, str]]:
    return [
        {
            "anchor_id": "BA1045_0_WEP_source",
            "observable": "eta_WEP_source_charge",
            "bound_source": "source-intake/local_bounds/local_bound_claims.csv:R1_WEP_source_charge",
            "bound_value": "2.8e-15",
            "link_to_component": "qbar_marker; qbar_source_weight; qbar_constants",
            "score_status": "ANCHOR_AVAILABLE_COMPONENTS_MISSING",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "anchor_id": "BA1045_1_R10",
            "observable": "alpha_X(lambda_X)",
            "bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "bound_value": "review_candidate_curve_only",
            "link_to_component": "qbar_geom; qbar_marker; qbar_XT",
            "score_status": "BOUND_AND_COMPONENTS_NOT_CLAIM_READY",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "anchor_id": "BA1045_2_clock",
            "observable": "clock/frame/constant response",
            "bound_source": "source-intake/local_bounds/local_bound_claims.csv:R2_clock_redshift plus future fine-structure rows",
            "bound_value": "observable_specific",
            "link_to_component": "qbar_constants; qbar_marker",
            "score_status": "TEMPLATE_ONLY",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def mts_template_rows() -> list[dict[str, str]]:
    return [
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "qbar_geom_functor_descent_template",
            "curve_id": "MTS_1045_QBAR_GEOM_TEMPLATE",
            "lambda_value": "MISSING_LAMBDA_X",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_K_X_QBAR_XH_QBAR_GEOM_OVER_4PI_ZX_G",
            "alpha_bound": "MISSING_PROMOTED_BOUND_CURVE",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "force_law_form": "alpha_X(lambda_X) includes K_X Qbar_XH(lambda_X) qbar_geom/(4*pi*Z_X*G_obs) unless qbar_geom=0 theorem is signed",
            "derivation_status": "template_invalid_parent_matter_functor_unsigned",
            "formula_reference": "1045-Y5-R10-parent-matter-functor-descent-signature-or-qbar-component-fill.md::QCF1045_1",
            "source_file": "MISSING_QBAR_GEOM_SOURCE_FILE",
            "assumptions": "private nonclaim qbar_geom fallback; no cancellation; no local-GR pass",
            "valid_for_claim": "false",
            "notes": "Runner must reject this row until the frame-leak coefficient or theorem-zero certificate is real.",
        },
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "qbar_marker_shadow_frame_template",
            "curve_id": "MTS_1045_QBAR_MARKER_TEMPLATE",
            "lambda_value": "MISSING_LAMBDA_X",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_SHADOW_FRAME_OR_MARKER_COMPONENT",
            "alpha_bound": "MISSING_PROMOTED_BOUND_CURVE",
            "alpha_bound_source": "source-intake/local_bounds/local_bound_claims.csv:R1_WEP_source_charge; source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "force_law_form": "qbar_marker enters WEP/R10/clock projections through declared marker sensitivities",
            "derivation_status": "template_invalid_no_marker_theorem_or_coefficients_missing",
            "formula_reference": "1045-Y5-R10-parent-matter-functor-descent-signature-or-qbar-component-fill.md::QCF1045_2",
            "source_file": "MISSING_QBAR_MARKER_SOURCE_FILE",
            "assumptions": "private nonclaim shadow-frame/marker fallback",
            "valid_for_claim": "false",
            "notes": "No source-backed marker coefficients are present.",
        },
    ]


def runner_smoke_rows(status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "smoke_id": "SMOKE1045_0_R10_runner_refusal",
            "valid_mts_rows": str(status.get("valid_mts_rows", "")),
            "valid_bound_rows": str(status.get("valid_bound_rows", "")),
            "comparison_rows": str(status.get("comparison_rows", "")),
            "R10_pass_for_claim": str(status.get("R10_pass_for_claim", "")).lower(),
            "claim_allowed": str(status.get("claim_allowed", "")).lower(),
            "expected_result": "reject placeholders and keep claim false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def placeholder_refusal_rows(
    signature_rows: list[dict[str, str]],
    lift_rows: list[dict[str, str]],
    qbar_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    signature_blockers = [row["signature_id"] for row in signature_rows if row["current_status"].endswith("UNSIGNED") or "NOT_PARENT" in row["current_status"]]
    lift_blockers = [row["gate_id"] for row in lift_rows if row["gate_pass"] == "false"]
    qbar_blockers = [row["component_id"] for row in qbar_rows if row["score_ready"] == "false"]
    return [
        {
            "refusal_id": "REF1045_0_parent_functor",
            "object": "parent matter functor descent",
            "current_status": "FAIL_CURRENT_CLAIM_PARENT_MATTER_FUNCTOR_NOT_SIGNED",
            "refusal_status": "blocked",
            "failure_reasons": ";".join(signature_blockers),
            "score_eligible": "false",
            "claim_allowed": "false",
            "generated_utc": stamp(),
        },
        {
            "refusal_id": "REF1045_1_vertical_lift",
            "object": "vertical lift descent",
            "current_status": "FAIL_CURRENT_CLAIM_VERTICAL_LIFT_NOT_SIGNED",
            "refusal_status": "blocked",
            "failure_reasons": ";".join(lift_blockers),
            "score_eligible": "false",
            "claim_allowed": "false",
            "generated_utc": stamp(),
        },
        {
            "refusal_id": "REF1045_2_qbar_components",
            "object": "qbar_geom/qbar_marker component values",
            "current_status": "COMPONENT_VALUES_MISSING",
            "refusal_status": "blocked",
            "failure_reasons": ";".join(qbar_blockers),
            "score_eligible": "false",
            "claim_allowed": "false",
            "generated_utc": stamp(),
        },
        {
            "refusal_id": "REF1045_3_R10_runner",
            "object": "R10 qbar component placeholder smoke rows",
            "current_status": "runner_refusal_expected",
            "refusal_status": "blocked",
            "failure_reasons": "valid_mts_rows=" + smoke_rows[0]["valid_mts_rows"],
            "score_eligible": "false",
            "claim_allowed": smoke_rows[0]["claim_allowed"],
            "generated_utc": stamp(),
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1045_0_parent_functor_signed",
            "claim": "ordinary matter functor descends to Q_loc",
            "gate_pass": "false",
            "reason": "signature is written but not parent-derived as one action object",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1045_1_qbar_geom_zero",
            "claim": "qbar_geom=0",
            "gate_pass": "false",
            "reason": "observed coframe functor, matter bundle functor, vertical lift, and no-shadow-frame clauses remain unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1045_2_qbar_marker_zero_or_bound",
            "claim": "qbar_marker is zero or source-backed bounded",
            "gate_pass": "false",
            "reason": "no-shadow-frame/no-marker theorem and coefficients are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1045_3_R10_or_WEP_score",
            "claim": "R10/WEP score can use qbar component rows",
            "gate_pass": "false",
            "reason": "MTS component rows contain MISSING markers and are invalid for claim",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1045_4_local_GR",
            "claim": "matter functor closes local-GR source side",
            "gate_pass": "false",
            "reason": "even a signed qbar_geom would not close constants, source normalization, boundary, domain, and positive-X gates",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1045_0_theorem_shape",
            "decision": "parent matter functor theorem shape is exact",
            "because": "e_obs=Obs_e(q_loc(Phi)) and v_X in ker(Dq_loc) would force Lie_v e_obs=0 and therefore qbar_geom=0, provided the matter lift and no-shadow-frame clauses also hold",
            "next_action": "do not claim; seek the parent owner of Obs_e or fill frame-leak coefficients",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1045_1_current_status",
            "decision": "functor descent is not currently signed",
            "because": "the corpus supplies conditional contracts and counterexample guards, not a parent action deriving the ordinary matter category and observed coframe functor",
            "next_action": "retain qbar_geom/qbar_marker rows",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1045_2_fallback",
            "decision": "qbar_geom and qbar_marker component rows filled as templates",
            "because": "R10/WEP anchors exist, but MTS-side frame-leak and marker coefficients are missing",
            "next_action": "either source frame-leak coefficients or derive no-shadow-frame/constant-sector theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1045_3_best_next",
            "decision": "target no-shadow-frame and constant/marker split",
            "because": "even a clean Obs_e functor fails if matter can see exp(2bX)g_obs, disformal slots, m_A(X), alpha_EM(X), or marker coefficients",
            "next_action": "1046-Y5-R10-no-shadow-frame-constant-marker-theorem-or-qbar-marker-coefficients.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1046-Y5-R10-no-shadow-frame-constant-marker-theorem-or-qbar-marker-coefficients.md",
            "objective": "try to prove no hidden conformal/disformal matter frame, no direct alpha/mass/clock vertex, and no material marker dependence; if this fails, fill nonclaim qbar_marker/qbar_constants coefficient rows",
            "include": "shadow-frame countermodels, constant superselection, alpha_EM and mass vertices, material markers, clock sensitivities, WEP/R10/clock links, source paths",
            "exclude": "closure axiom, post-readout EFT proof credit, cancellation with qbar_geom or qbar_source_weight, local-GR claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validate(
    source_rows: list[dict[str, str]],
    signature_rows: list[dict[str, str]],
    lift_rows: list[dict[str, str]],
    qbar_attempt_rows: list[dict[str, str]],
    qbar_fill_rows: list[dict[str, str]],
    bound_rows: list[dict[str, str]],
    mts_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(
        (
            "V1045_1_sources_exist_and_needles",
            all(flag(row["exists"]) and flag(row["needle_found"]) for row in source_rows),
            "every cited source path exists and every source needle was found",
        )
    )
    checks.append(
        (
            "V1045_2_functor_signature_blocked",
            any(row["signature_id"] == "MFS1045_6_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM_PARENT_MATTER_FUNCTOR_NOT_SIGNED" for row in signature_rows)
            and all(not flag(row["valid_for_claim"]) for row in signature_rows),
            "parent matter functor signature is audited and remains unsigned",
        )
    )
    checks.append(
        (
            "V1045_3_vertical_lift_blocked",
            any(row["gate_id"] == "VLG1045_4_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM_VERTICAL_LIFT_NOT_SIGNED" for row in lift_rows)
            and all(row["gate_pass"] == "false" and not flag(row["valid_for_claim"]) for row in lift_rows),
            "vertical lift gates are explicit and blocked",
        )
    )
    checks.append(
        (
            "V1045_4_qbar_geom_attempt_blocked",
            any(row["attempt_id"] == "QG1045_1_functor_chain_rule" and row["current_status"] == "EXACT_CONDITIONAL_SUBLEMMA" for row in qbar_attempt_rows)
            and any(row["attempt_id"] == "QG1045_4_current_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM_QBAR_GEOM_ZERO_NOT_SIGNED" for row in qbar_attempt_rows),
            "qbar_geom chain-rule sublemma is exact but not promotable",
        )
    )
    checks.append(
        (
            "V1045_5_component_rows_nonclaim",
            any(row["component_id"] == "QCF1045_1_qbar_geom_numeric_placeholder" and "MISSING" in row["value"] for row in qbar_fill_rows)
            and any(row["component_id"] == "QCF1045_2_qbar_marker_shadow_frame" and "MISSING" in row["value"] for row in qbar_fill_rows)
            and all(row["score_ready"] == "false" and not flag(row["valid_for_claim"]) for row in qbar_fill_rows),
            "qbar_geom/qbar_marker component rows are filled as nonclaim templates",
        )
    )
    checks.append(
        (
            "V1045_6_bound_anchors_nonclaim",
            any(row["anchor_id"] == "BA1045_0_WEP_source" and row["bound_value"] == "2.8e-15" for row in bound_rows)
            and any(row["anchor_id"] == "BA1045_1_R10" for row in bound_rows)
            and all(not flag(row["valid_for_claim"]) for row in bound_rows),
            "WEP/R10/clock anchors are linked but nonclaim",
        )
    )
    checks.append(
        (
            "V1045_7_mts_template_schema_nonclaim",
            bool(mts_rows)
            and set(MTS_REQUIRED_COLUMNS).issubset(set(mts_rows[0].keys()))
            and all(not flag(row["valid_for_claim"]) for row in mts_rows),
            "MTS smoke template has runner schema and no claim-valid rows",
        )
    )
    checks.append(
        (
            "V1045_8_runner_smoke_refuses_claim",
            bool(smoke_rows)
            and smoke_rows[0]["R10_pass_for_claim"] == "false"
            and smoke_rows[0]["claim_allowed"] == "false"
            and smoke_rows[0]["valid_mts_rows"] == "0",
            "existing R10 runner refuses the 1045 placeholder rows",
        )
    )
    checks.append(
        (
            "V1045_9_claim_gates_blocked",
            all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" and not flag(row["valid_for_claim"]) for row in claim_rows),
            "all matter-functor/qbar/local-GR claim gates remain blocked",
        )
    )
    checks.append(
        (
            "V1045_10_next_target_written",
            bool(next_rows)
            and next_rows[0]["next_target"] == "1046-Y5-R10-no-shadow-frame-constant-marker-theorem-or-qbar-marker-coefficients.md",
            "next target row is present",
        )
    )
    generated_files = [
        DOC,
        OUT / "P8_Y5_R10_1045_SOURCE_REGISTER.csv",
        OUT / "P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
        OUT / "P8_Y5_R10_1045_VERTICAL_LIFT_DESCENT_GATE.csv",
        OUT / "P8_Y5_R10_1045_QBAR_GEOM_ZERO_ATTEMPT.csv",
        OUT / "P8_Y5_R10_1045_QBAR_COMPONENT_FILL_ROWS.csv",
        OUT / "P8_Y5_R10_1045_BOUND_ANCHOR_LINKS.csv",
        OUT / "P8_Y5_R10_1045_RUNNER_SMOKE_STATUS.csv",
        OUT / "P8_Y5_R10_1045_PLACEHOLDER_REFUSAL_RUNNER.csv",
        OUT / "P8_Y5_R10_1045_CLAIM_GATES.csv",
        OUT / "P8_Y5_R10_1045_DECISION_LEDGER.csv",
        OUT / "P8_Y5_R10_1045_NEXT_TARGET.csv",
        OUT / "P8_Y5_BRR545_1045_VALIDATION.csv",
        MTS_TEMPLATE,
    ]
    checks.append(
        (
            "V1045_11_generated_files_in_post_checkpoint",
            all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in generated_files if path.exists() or path.parent.exists()),
            "all generated files are under post-checkpoint-work",
        )
    )
    formalization_touches: list[Path] = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*"):
            if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED:
                formalization_touches.append(path)
    checks.append(
        (
            "V1045_12_formalization_untouched",
            not formalization_touches,
            f"formalization-workbench modified-file count since script start is {len(formalization_touches)}",
        )
    )
    rows = [
        {
            "check_id": "V1045_SUMMARY",
            "result": "pass" if all(result for _, result, _ in checks) else "fail",
            "detail": "1045 parent matter functor descent signature or qbar component fill validation summary",
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
    signature_rows: list[dict[str, str]],
    lift_rows: list[dict[str, str]],
    qbar_attempt_rows: list[dict[str, str]],
    qbar_fill_rows: list[dict[str, str]],
    bound_rows: list[dict[str, str]],
    mts_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
    refusal_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows_: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    sections = [
        "# 1045 Y5 R10 parent matter functor descent signature or qbar component fill",
        "",
        "**Progress:** the parent matter functor contract is now exact: if `e_obs=Obs_e(q_loc(Phi))`, `v_X in ker(Dq_loc)`, and the ordinary matter lift is fixed/gauge-owned, then `Lie_v e_obs=0` and the visible-geometry charge `qbar_geom` vanishes.",
        "",
        "**Current verdict:** the corpus still has this as a contract/conditional theorem, not a signed parent action. The ordinary matter category, observed coframe functor, vertical lift, no-shadow-frame guard, and constants split remain unsigned.",
        "",
        "**Fallback:** `qbar_geom` and `qbar_marker` rows are filled as nonclaim templates. No R10, WEP, clock, Newton, or local-GR claim is made.",
        "",
        "## Source register",
        md_table(source_rows, ["source_id", "source_path", "exists", "needle_found", "role"]),
        "## Parent matter functor signature audit",
        md_table(signature_rows, ["signature_id", "required_signature", "mathematical_effect", "current_status", "if_signed", "if_unsigned", "valid_for_claim"]),
        "## Vertical lift descent gate",
        md_table(lift_rows, ["gate_id", "lift_option", "condition", "derives", "current_status", "risk_if_used", "gate_pass", "valid_for_claim"]),
        "## qbar geom zero attempt",
        md_table(qbar_attempt_rows, ["attempt_id", "object", "formula", "zero_route", "current_status", "claim_allowed", "valid_for_claim"]),
        "## qbar component fill rows",
        md_table(qbar_fill_rows, ["component_id", "symbol", "value", "units", "formula", "required_source", "current_status", "score_ready", "valid_for_claim"]),
        "## Bound anchor links",
        md_table(bound_rows, ["anchor_id", "observable", "bound_source", "bound_value", "link_to_component", "score_status", "valid_for_claim"]),
        "## MTS R10 smoke template",
        md_table(mts_rows, ["model_id", "branch_id", "lambda_value", "alpha_predicted", "force_law_form", "derivation_status", "valid_for_claim"]),
        "## Runner smoke status",
        md_table(smoke_rows, ["smoke_id", "valid_mts_rows", "valid_bound_rows", "comparison_rows", "R10_pass_for_claim", "claim_allowed", "expected_result"]),
        "## Placeholder refusal runner",
        md_table(refusal_rows, ["refusal_id", "object", "current_status", "refusal_status", "failure_reasons", "score_eligible", "claim_allowed"]),
        "## Claim gates",
        md_table(claim_rows, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
        "## Decision ledger",
        md_table(decision_rows_, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
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
    signature_rows = functor_signature_rows()
    lift_rows = vertical_lift_gate_rows()
    qbar_attempt_rows = qbar_geom_attempt_rows()
    qbar_fill_rows = qbar_component_fill_rows()
    bound_rows = bound_anchor_rows()
    mts_rows = mts_template_rows()
    write_csv(MTS_TEMPLATE, mts_rows, MTS_REQUIRED_COLUMNS)
    runner_result = run_runner(MTS_TEMPLATE, BOUND_CANDIDATE, RUN_DIR)
    smoke_rows = runner_smoke_rows(runner_result["status"])
    refusal_rows = placeholder_refusal_rows(signature_rows, lift_rows, qbar_fill_rows, smoke_rows)
    claim_rows_ = claim_gate_rows()
    decision_rows_ = decision_rows()
    next_rows = next_target_rows()
    validation = validate(
        source_rows,
        signature_rows,
        lift_rows,
        qbar_attempt_rows,
        qbar_fill_rows,
        bound_rows,
        mts_rows,
        smoke_rows,
        claim_rows_,
        next_rows,
    )

    write_csv(OUT / "P8_Y5_R10_1045_SOURCE_REGISTER.csv", source_rows)
    write_csv(OUT / "P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv", signature_rows)
    write_csv(OUT / "P8_Y5_R10_1045_VERTICAL_LIFT_DESCENT_GATE.csv", lift_rows)
    write_csv(OUT / "P8_Y5_R10_1045_QBAR_GEOM_ZERO_ATTEMPT.csv", qbar_attempt_rows)
    write_csv(OUT / "P8_Y5_R10_1045_QBAR_COMPONENT_FILL_ROWS.csv", qbar_fill_rows)
    write_csv(OUT / "P8_Y5_R10_1045_BOUND_ANCHOR_LINKS.csv", bound_rows)
    write_csv(OUT / "P8_Y5_R10_1045_RUNNER_SMOKE_STATUS.csv", smoke_rows)
    write_csv(OUT / "P8_Y5_R10_1045_PLACEHOLDER_REFUSAL_RUNNER.csv", refusal_rows)
    write_csv(OUT / "P8_Y5_R10_1045_CLAIM_GATES.csv", claim_rows_)
    write_csv(OUT / "P8_Y5_R10_1045_DECISION_LEDGER.csv", decision_rows_)
    write_csv(OUT / "P8_Y5_R10_1045_NEXT_TARGET.csv", next_rows)
    write_csv(OUT / "P8_Y5_BRR545_1045_VALIDATION.csv", validation)
    write_doc(
        source_rows,
        signature_rows,
        lift_rows,
        qbar_attempt_rows,
        qbar_fill_rows,
        bound_rows,
        mts_rows,
        smoke_rows,
        refusal_rows,
        claim_rows_,
        decision_rows_,
        validation,
        next_rows,
    )

    if validation[0]["result"] != "pass":
        failed = [row for row in validation if row["result"] == "fail"]
        raise SystemExit(f"1045 validation failed: {failed}")


if __name__ == "__main__":
    main()
