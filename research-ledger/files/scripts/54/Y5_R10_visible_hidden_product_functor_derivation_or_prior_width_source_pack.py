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
DOC = ROOT / "1050-Y5-R10-visible-hidden-product-functor-derivation-or-prior-width-source-pack.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1050-R10-product-functor-prior-pack-smoke" / "results"
MTS_TEMPLATE = OUT / "R10_alpha_lambda_curve_MTS_1050_PRODUCT_FUNCTOR_PRIOR_PACK_TEMPLATE_NONCLAIM.csv"
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
            "SRC1050_0_1049_next",
            "source-intake/mts_residuals/P8_Y5_R10_1049_NEXT_TARGET.csv",
            "1050-Y5-R10-visible-hidden-product-functor-derivation-or-prior-width-source-pack.md",
            "1049 handoff to visible/hidden product functor.",
        ),
        (
            "SRC1050_1_1049_operator",
            "source-intake/mts_residuals/P8_Y5_R10_1049_OPERATOR_CLASSIFICATION_RULE_ATTEMPT.csv",
            "OCR1049_2_product_sequestration",
            "1049 product/sequester operator rule attempt.",
        ),
        (
            "SRC1050_2_1049_symmetry",
            "source-intake/mts_residuals/P8_Y5_R10_1049_SYMMETRY_BAN_THEOREM_ATTEMPT.csv",
            "SBT1049_4_product_functor",
            "1049 symmetry-ban result identifying product functor as clean route.",
        ),
        (
            "SRC1050_3_1049_priors",
            "source-intake/mts_residuals/P8_Y5_R10_1049_RESIDUAL_PRIOR_SLOTS.csv",
            "RP1049_0_b_alpha",
            "1049 residual prior slots.",
        ),
        (
            "SRC1050_4_1045_matter_functor",
            "source-intake/mts_residuals/P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
            "MFS1045_6_verdict",
            "Parent matter functor signature audit.",
        ),
        (
            "SRC1050_5_980_no_marker_functor",
            "source-intake/mts_residuals/P8_Y5_R10_980_NO_MARKER_FUNCTOR_THEOREM_ATTEMPT.csv",
            "NMF980_7_verdict",
            "No-marker functor obstruction and scalar-invariant counterexample.",
        ),
        (
            "SRC1050_6_642_maxwell_descent",
            "source-intake/mts_residuals/P8_Y5_R10_642_MAXWELL_DESCENT_ATTEMPT.csv",
            "MD642_4_alpha_constant",
            "Maxwell descent attempt and alpha constant blocker.",
        ),
        (
            "SRC1050_7_953_source_functor",
            "source-intake/mts_residuals/P8_Y5_R10_953_SOURCE_FUNCTOR_THEOREM_ATTEMPT.csv",
            "NSF953_5_verdict",
            "Source functor label-forgetting theorem attempt.",
        ),
        (
            "SRC1050_8_1048_bound_matrix",
            "source-intake/mts_residuals/P8_Y5_R10_1048_ALPHA_MASS_CLOCK_BOUND_MATRIX.csv",
            "BM1048_3_R10_yukawa",
            "1048 alpha/mass/clock bound matrix.",
        ),
        (
            "SRC1050_9_clock_sensitivity",
            "source-intake/mts_residuals/P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv",
            "CAS646_1_YbE3E2",
            "Clock alpha sensitivity source rows.",
        ),
        (
            "SRC1050_10_local_bounds",
            "source-intake/local_bounds/local_bound_claims.csv",
            "R1_WEP_source_charge",
            "Local WEP/source, clock, PPN, and Gdot anchors.",
        ),
        (
            "SRC1050_11_R10_bound_candidate",
            "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "R10_VECTOR_2020_REVIEW_0000",
            "R10 nonclaim review-candidate curve for smoke only.",
        ),
        (
            "SRC1050_12_R10_runner",
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


def product_functor_rows() -> list[dict[str, str]]:
    return [
        {
            "theorem_id": "PFT1050_0_define_product_domain",
            "claim_piece": "visible/hidden product domain",
            "mathematical_form": "C_parent -> C_vis x C_hid with C_vis pulled back from q_loc(Phi) and representation labels theta_rep; hidden fields Xhat live only in C_hid",
            "derivation_step": "This is the categorical form of sequestering: visible EM/matter functors are not allowed to take Xhat as an argument.",
            "current_status": "DEFINITION_SHARP_NOT_PARENT_DERIVED",
            "missing_for_claim": "parent construction of the product category and projection functors",
            "if_missing": "Xhat can still feed visible coefficients through legal scalar functions",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "PFT1050_1_visible_action_pullback",
            "claim_piece": "visible action is quotient pullback",
            "mathematical_form": "S_vis = S_EM[A_Q,q_loc(Phi),T_Q,theta_rep] + S_matter[Psi,e_obs(q),omega(q),theta_rep]",
            "derivation_step": "If S_vis factors only through q_loc and representation data, then vertical variations in ker(Dq_loc) cannot alter visible coefficients.",
            "current_status": "EXACT_CONDITIONAL_THEOREM",
            "missing_for_claim": "signed parent matter functor, Maxwell/gauge normalization owner, and source label-forgetting",
            "if_missing": "b_alpha, b_mA, b_mu, b_nuc, b_clock_i remain retained",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "PFT1050_2_forbidden_mixed_hom",
            "claim_piece": "no visible-hidden mixed coefficient morphisms",
            "mathematical_form": "Hom(C_hid, Coeff(O_vis)) = Const or absent; Forbidden: Xhat -> f_X, m_A, y_A, B_A, nu_i",
            "derivation_step": "This is the exact condition that kills f_X F^2 and mass/clock Xhat vertices.",
            "current_status": "POWERFUL_BUT_UNSIGNED",
            "missing_for_claim": "proof that the parent observable algebra has no nonconstant hidden-to-visible coefficient morphisms",
            "if_missing": "980 scalar-obstruction lemma reopens the functor with any surviving invariant scalar",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "PFT1050_3_radiative_readout_closure",
            "claim_piece": "sequestering survives EFT and clock/readout reduction",
            "mathematical_form": "Renormalized/effective S_vis^eff and readout maps still factor through q_loc and theta_rep",
            "derivation_step": "Tree-level product form is not enough if loops or readout maps regenerate Xhat-dependent coefficients.",
            "current_status": "UNSIGNED",
            "missing_for_claim": "radiative closure or explicit effective-action/readout functor theorem",
            "if_missing": "b_alpha and b_clock_i remain live even if the bare action is clean",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "PFT1050_4_source_forgetfulness",
            "claim_piece": "source functor forgets species labels before coupling selection",
            "mathematical_form": "F_src: Obj(C_matter)->T_total rather than Obj(C_matter)->(T_A,A); then only kappa_univ is available",
            "derivation_step": "Product functor must also prevent source/test labels from becoming relative coupling slots.",
            "current_status": "CONDITIONAL_PROOF_NOT_PARENT_DERIVED",
            "missing_for_claim": "parent-signed label-forgetting quotient",
            "if_missing": "relative source weights and WEP/R10 source charge remain retained",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "PFT1050_5_verdict",
            "claim_piece": "visible-hidden product functor closes constant sector",
            "mathematical_form": "PFT1050_0 through PFT1050_4 signed => b_alpha=b_mu=b_mA=b_nuc=b_clock_i=qbar_source_label=0",
            "derivation_step": "The theorem target is exact, but the current corpus has not derived the product functor or radiative/readout closure.",
            "current_status": "FAIL_CURRENT_CLAIM_PRIOR_WIDTH_PACK_REQUIRED",
            "missing_for_claim": "parent product functor construction or source-backed residual prior widths",
            "if_missing": "build prior-width source pack and keep all local claims blocked",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def visible_algebra_rows() -> list[dict[str, str]]:
    return [
        {
            "algebra_id": "VA1050_0_geometry",
            "visible_object": "observed coframe/metric/connection",
            "allowed_arguments": "q_loc(Phi)",
            "forbidden_arguments": "Xhat representative; hidden profile labels; material marker",
            "current_evidence": "1045 gives observed coframe functor as sufficient signature but parent-signed status is open",
            "status": "CONDITIONAL",
            "residual_if_open": "qbar_geom; shadow-frame terms",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "algebra_id": "VA1050_1_EM",
            "visible_object": "EM connection and gauge kinetic normalization",
            "allowed_arguments": "A_Q,T_Q,q_loc(Phi),fixed inner product/charge lattice",
            "forbidden_arguments": "f_X(Xhat), lambda_A branch coefficient, post-readout alpha_X",
            "current_evidence": "642 blocks alpha constant because g_EM/source current/Hodge owner is missing",
            "status": "BLOCKED",
            "residual_if_open": "b_alpha",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "algebra_id": "VA1050_2_matter",
            "visible_object": "matter masses/Yukawas/binding data",
            "allowed_arguments": "theta_rep or theta_bar(q_loc(Phi))",
            "forbidden_arguments": "m_A(Xhat), y_A(Xhat), B_A(Xhat), Lambda_QCD(Xhat)",
            "current_evidence": "1045/1049 mark matter functor and constants split unsigned",
            "status": "BLOCKED",
            "residual_if_open": "b_mu;b_mA;b_nuc",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "algebra_id": "VA1050_3_clocks",
            "visible_object": "clock transition/readout map",
            "allowed_arguments": "q_loc(Phi), theta_rep, quotient-owned alpha/mass/nuclear constants",
            "forbidden_arguments": "nu_i(Xhat), clock-frame Xhat, hidden readout marker",
            "current_evidence": "clock sensitivity rows exist, but MTS tau_clock/readout closure is missing",
            "status": "BLOCKED",
            "residual_if_open": "b_clock_i",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "algebra_id": "VA1050_4_source",
            "visible_object": "source/test mass and coupling functor",
            "allowed_arguments": "T_total in one observed coframe; one common kappa/G_ref",
            "forbidden_arguments": "species labels A in coupling choice; kappa_A(Xhat); source preparation marker",
            "current_evidence": "953 gives a clean conditional source functor theorem but no parent label-forgetting proof",
            "status": "BLOCKED",
            "residual_if_open": "qbar_source_label; beta_source",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def obstruction_rows() -> list[dict[str, str]]:
    return [
        {
            "obstruction_id": "OBS1050_0_scalar_invariant",
            "obstruction": "any surviving nonconstant local invariant scalar can feed a visible coefficient",
            "example": "theta(I)=theta0+epsilon I or f_X(I)F^2",
            "source_evidence": "P8_Y5_R10_980_NO_MARKER_FUNCTOR_THEOREM_ATTEMPT.csv:NMF980_2",
            "effect": "product functor fails unless hidden-to-visible coefficient morphisms are forbidden",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "obstruction_id": "OBS1050_1_alpha_owner",
            "obstruction": "Maxwell descent does not fix g_EM or alpha_EM owner",
            "example": "g_EM or alpha_EM may remain an independent visible coefficient",
            "source_evidence": "P8_Y5_R10_642_MAXWELL_DESCENT_ATTEMPT.csv:MD642_4_alpha_constant",
            "effect": "b_alpha remains live",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "obstruction_id": "OBS1050_2_matter_category",
            "obstruction": "parent matter category and constants split are not parent-constructed",
            "example": "m_A(Xhat), y_A(Xhat), B_A(Xhat)",
            "source_evidence": "P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv:MFS1045_6_verdict",
            "effect": "b_mu,b_mA,b_nuc remain live",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "obstruction_id": "OBS1050_3_source_labels",
            "obstruction": "source functor does not yet prove label-forgetting",
            "example": "F((T_A,A))=kappa_A T_A remains additive and covariant",
            "source_evidence": "P8_Y5_R10_953_SOURCE_FUNCTOR_THEOREM_ATTEMPT.csv:NSF953_5_verdict",
            "effect": "WEP/R10 source charge remains retained",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "obstruction_id": "OBS1050_4_radiative_readout",
            "obstruction": "bare action product form does not automatically survive EFT/readout reductions",
            "example": "loop-induced f_X F^2 or clock readout residual",
            "source_evidence": "1049 symmetry/readout closure gate",
            "effect": "b_alpha,b_clock_i remain live unless closure is signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def prior_width_source_rows() -> list[dict[str, str]]:
    return [
        {
            "pack_id": "PWP1050_0_b_alpha",
            "symbol": "b_alpha",
            "source_pack_target": "dimensionless EM/gauge kinetic/readout coefficient prior width",
            "candidate_sources_in_hand": "P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv; local_bound_claims.csv:R1_WEP_source_charge; R10 review candidate",
            "still_missing": "actual b_alpha prior width or theorem-zero; tau_clock/tau_WEP/tau_R10; composition alpha charge; promoted R10 bound curve",
            "units": "Xhat^-1 or arena-projected dimensionless product",
            "promotion_status": "MISSING_PRIOR_WIDTH",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "pack_id": "PWP1050_1_b_mu",
            "symbol": "b_mu",
            "source_pack_target": "mass-ratio coefficient prior width",
            "candidate_sources_in_hand": "1047/1049 residual slot only",
            "still_missing": "clock K_mu sensitivities; mass-ratio drift constraints; parent Xhat normalization",
            "units": "Xhat^-1 or clock-projected product",
            "promotion_status": "MISSING_SOURCE_ROWS",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "pack_id": "PWP1050_2_b_mA",
            "symbol": "b_mA",
            "source_pack_target": "material/species mass-response prior width",
            "candidate_sources_in_hand": "local_bound_claims.csv:R1_WEP_source_charge; R10 review candidate",
            "still_missing": "composition sensitivity matrix; source/test material charge vectors; tau_WEP/tau_R10",
            "units": "Xhat^-1 or composition-projected dimensionless product",
            "promotion_status": "MISSING_COMPOSITION_MATRIX",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "pack_id": "PWP1050_3_b_nuc",
            "symbol": "b_nuc",
            "source_pack_target": "nuclear/QCD/binding-response prior width",
            "candidate_sources_in_hand": "WEP/R10 anchors only",
            "still_missing": "nuclear sensitivity coefficients; material binding fractions; clock nuclear sensitivity rows",
            "units": "Xhat^-1 or sensitivity-projected product",
            "promotion_status": "MISSING_NUCLEAR_SENSITIVITY_SOURCES",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "pack_id": "PWP1050_4_b_clock_i",
            "symbol": "b_clock_i",
            "source_pack_target": "direct clock/readout residual prior width",
            "candidate_sources_in_hand": "P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv; local_bound_claims.csv:R2_clock_redshift",
            "still_missing": "direct readout residual model; tau_clock; separation from alpha/mass/nuclear sensitivity terms",
            "units": "Xhat^-1 or clock-projected product",
            "promotion_status": "MISSING_CLOCK_READOUT_MODEL",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "pack_id": "PWP1050_5_qbar_source_label",
            "symbol": "qbar_source_label",
            "source_pack_target": "source/species label leakage prior width",
            "candidate_sources_in_hand": "P8_Y5_R10_953_SOURCE_FUNCTOR_THEOREM_ATTEMPT.csv; local_bound_claims.csv:R1_WEP_source_charge",
            "still_missing": "label-forgetting theorem-zero or relative source-weight prior; source/test projection",
            "units": "dimensionless source charge product",
            "promotion_status": "MISSING_SOURCE_LABEL_PRIOR",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def projection_readiness_rows() -> list[dict[str, str]]:
    return [
        {
            "readiness_id": "PR1050_0_clock",
            "arena": "clock",
            "ready_inputs": "DeltaK_alpha for Al/Hg and Yb+ E3/E2; Galileo redshift anchor",
            "missing_inputs": "K_mu/K_nuc; tau_clock; b_alpha/b_mu/b_nuc/b_clock_i theorem-zero or prior width",
            "status": "PARTIAL_NOT_SCORE_READY",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "readiness_id": "PR1050_1_WEP",
            "arena": "MICROSCOPE/WEP",
            "ready_inputs": "eta bound anchor",
            "missing_inputs": "composition sensitivity matrix; source/test beta vectors; tau_WEP; residual widths",
            "status": "ANCHOR_ONLY_NOT_SCORE_READY",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "readiness_id": "PR1050_2_R10",
            "arena": "short-range fifth force",
            "ready_inputs": "R10 review-candidate nonclaim bound curve; runner schema",
            "missing_inputs": "promoted bound curve; lambda_X; Z_X; K_X; Q_source/Q_test; residual widths",
            "status": "SMOKE_ONLY_NOT_SCORE_READY",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "readiness_id": "PR1050_3_PPN",
            "arena": "local GR/PPN/source",
            "ready_inputs": "local bound anchors R3-R9",
            "missing_inputs": "weak-field solution; Hamiltonian source owner; readout/source projection of residuals",
            "status": "NOT_SCORE_READY",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def mts_template_rows() -> list[dict[str, str]]:
    return [
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "product_functor_or_prior_width_template",
            "curve_id": "MTS_1050_PRODUCT_FUNCTOR_PRIOR_PACK_TEMPLATE",
            "lambda_value": "MISSING_LAMBDA_X",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_PRODUCT_FUNCTOR_ZERO_OR_PRIOR_WIDTH_PROJECTION",
            "alpha_bound": "MISSING_PROMOTED_BOUND_CURVE",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "force_law_form": "R10 alpha(lambda) is zero only if product functor signs; otherwise residual-prior vector projects through source/test charges",
            "derivation_status": "template_invalid_product_functor_unsigned_and_prior_widths_missing",
            "formula_reference": "1050-Y5-R10-visible-hidden-product-functor-derivation-or-prior-width-source-pack.md::PFT1050_5",
            "source_file": "MISSING_PRODUCT_FUNCTOR_OR_PRIOR_WIDTH_SOURCE_FILE",
            "assumptions": "private nonclaim; no cancellation; no local-GR/R10/WEP/clock pass",
            "valid_for_claim": "false",
            "notes": "Runner must reject until product functor theorem-zero or source-backed prior widths and projections exist.",
        }
    ]


def placeholder_refusal_rows(runner_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "refusal_id": "REF1050_0_product_functor",
            "object": "visible-hidden product functor theorem",
            "current_status": "FAIL_CURRENT_CLAIM_PRIOR_WIDTH_PACK_REQUIRED",
            "refusal_status": "blocked",
            "failure_reasons": "product category not parent-constructed; mixed hidden-visible morphisms not forbidden; Maxwell alpha owner missing; radiative/readout closure unsigned",
            "score_eligible": "false",
            "claim_allowed": "false",
            "generated_utc": stamp(),
        },
        {
            "refusal_id": "REF1050_1_prior_width_pack",
            "object": "residual prior-width source pack",
            "current_status": "MISSING_PRIOR_WIDTHS_AND_LOCAL_PROJECTIONS",
            "refusal_status": "blocked",
            "failure_reasons": "PWP1050_0_b_alpha;PWP1050_1_b_mu;PWP1050_2_b_mA;PWP1050_3_b_nuc;PWP1050_4_b_clock_i;PWP1050_5_qbar_source_label",
            "score_eligible": "false",
            "claim_allowed": "false",
            "generated_utc": stamp(),
        },
        {
            "refusal_id": "REF1050_2_R10_runner",
            "object": "R10 product/prior placeholder smoke row",
            "current_status": "runner_refusal_expected",
            "refusal_status": "blocked",
            "failure_reasons": f"valid_mts_rows={runner_status.get('valid_mts_rows')}; valid_bound_rows={runner_status.get('valid_bound_rows')}",
            "score_eligible": "false",
            "claim_allowed": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1050_0_product_functor",
            "claim": "visible matter and EM depend only on q_loc and representation data",
            "gate_pass": "false",
            "reason": "product category, no mixed morphisms, and radiative/readout closure are not parent-signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1050_1_constant_zero",
            "claim": "b_alpha,b_mu,b_mA,b_nuc,b_clock_i vanish by product functor",
            "gate_pass": "false",
            "reason": "Maxwell alpha owner, matter spectrum owner, and clock readout closure remain unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1050_2_prior_width_score",
            "claim": "prior-width pack can score WEP/R10/clock/PPN",
            "gate_pass": "false",
            "reason": "source pack is checklist-level only; prior widths and local projections are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1050_3_local_GR",
            "claim": "local-GR/Newton branch closes from 1050",
            "gate_pass": "false",
            "reason": "constant-sector product functor would help, but source Hamiltonian and weak-field PPN derivations remain separate gates",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1050_0_theorem_shape",
            "decision": "product functor theorem shape is exact",
            "because": "if visible action is a pullback through q_loc and representation data, vertical hidden variations cannot create visible constants",
            "next_action": "do not claim until parent category/no-mixed-morphism and readout closure are signed",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1050_1_current_failure",
            "decision": "current corpus does not prove product functor",
            "because": "nonconstant invariant scalar, alpha owner, matter functor, source labels, and radiative/readout closure remain open",
            "next_action": "use prior-width source pack or derive no-mixed-morphism lemma",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1050_2_prior_pack",
            "decision": "prior-width pack is useful but not score-ready",
            "because": "candidate anchors exist for clock/WEP/R10, but coefficient widths and projections are missing",
            "next_action": "source one coefficient-width chain or derive a no-mixed-morphism theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1050_3_best_next",
            "decision": "target no-mixed-morphism lemma before numerical priors",
            "because": "it is the last clean derivation route for killing the constant-sector residuals without fitting many coefficients",
            "next_action": "1051-Y5-R10-no-mixed-hidden-visible-morphism-lemma-or-first-prior-width-chain.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1051-Y5-R10-no-mixed-hidden-visible-morphism-lemma-or-first-prior-width-chain.md",
            "objective": "try to prove that no nonconstant hidden-to-visible coefficient morphism exists in the parent observable algebra; if it fails, build the first source-backed prior-width chain, starting with b_alpha because clock alpha sensitivities already exist",
            "include": "no-mixed-morphism lemma, invariant-scalar obstruction audit, alpha owner/radiative closure, b_alpha prior-width chain, clock/WEP/R10 projection readiness",
            "exclude": "unit-rescaling cheat, cancellation, public local-GR/R10/WEP/clock claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validation_rows(
    source_rows: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    algebra_rows: list[dict[str, str]],
    obstruction_rows_in: list[dict[str, str]],
    prior_rows: list[dict[str, str]],
    readiness_rows: list[dict[str, str]],
    mts_rows: list[dict[str, str]],
    runner_status: dict[str, Any],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
    generated_paths: list[Path],
) -> list[dict[str, str]]:
    def status(result: bool) -> str:
        return "pass" if result else "fail"

    def no_claim(rows: list[dict[str, str]]) -> bool:
        return all(not flag(row.get("valid_for_claim", "false")) for row in rows)

    source_ok = all(flag(row["exists"]) and flag(row["needle_found"]) for row in source_rows)
    theorem_ok = any(row["theorem_id"] == "PFT1050_1_visible_action_pullback" and row["current_status"] == "EXACT_CONDITIONAL_THEOREM" for row in theorem_rows) and any(
        row["theorem_id"] == "PFT1050_5_verdict" and row["current_status"].startswith("FAIL_CURRENT_CLAIM") for row in theorem_rows
    )
    algebra_ok = {"VA1050_1_EM", "VA1050_2_matter", "VA1050_3_clocks", "VA1050_4_source"}.issubset({row["algebra_id"] for row in algebra_rows})
    obstruction_ok = {"OBS1050_0_scalar_invariant", "OBS1050_1_alpha_owner", "OBS1050_4_radiative_readout"}.issubset({row["obstruction_id"] for row in obstruction_rows_in})
    prior_ok = no_claim(prior_rows) and any(row["pack_id"] == "PWP1050_0_b_alpha" and "MISSING" in row["promotion_status"] for row in prior_rows)
    readiness_ok = no_claim(readiness_rows) and {"PR1050_0_clock", "PR1050_1_WEP", "PR1050_2_R10", "PR1050_3_PPN"}.issubset({row["readiness_id"] for row in readiness_rows})
    mts_schema_ok = all(column in mts_rows[0] for column in MTS_REQUIRED_COLUMNS) if mts_rows else False
    mts_nonclaim_ok = no_claim(mts_rows) and any("MISSING" in row["alpha_predicted"] for row in mts_rows)
    runner_ok = runner_status.get("claim_allowed") is False and runner_status.get("valid_mts_rows") == 0
    gates_ok = all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claim_rows)
    next_ok = bool(next_rows) and "1051" in next_rows[0]["next_target"]
    generated_ok = all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in generated_paths)
    formalization_changed = 0
    if FORMALIZATION.exists():
        formalization_changed = sum(
            1
            for path in FORMALIZATION.rglob("*")
            if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED
        )
    checks = [
        ("V1050_SUMMARY", True, "1050 visible-hidden product functor or prior-width source pack validation summary"),
        ("V1050_1_sources_exist_and_needles", source_ok, "every cited source path exists and every source needle was found"),
        ("V1050_2_product_theorem_blocked", theorem_ok, "product functor has exact conditional piece but current claim remains blocked"),
        ("V1050_3_visible_algebra_audited", algebra_ok, "geometry/EM/matter/clock/source visible algebra rows are present"),
        ("V1050_4_obstructions_recorded", obstruction_ok, "scalar invariant, alpha owner, and radiative/readout obstructions are recorded"),
        ("V1050_5_prior_width_pack_nonclaim", prior_ok, "prior-width source pack is staged as nonclaim"),
        ("V1050_6_projection_readiness_nonclaim", readiness_ok, "clock/WEP/R10/PPN readiness rows are staged as nonclaim"),
        ("V1050_7_mts_template_schema_nonclaim", mts_schema_ok and mts_nonclaim_ok, "MTS R10 template has runner schema and no claim-valid rows"),
        ("V1050_8_runner_smoke_refuses_claim", runner_ok, "existing R10 runner refuses the 1050 placeholder rows"),
        ("V1050_9_claim_gates_blocked", gates_ok, "all product/prior/local-GR claim gates remain blocked"),
        ("V1050_10_next_target_written", next_ok, "next target row is present"),
        ("V1050_11_generated_files_in_post_checkpoint", generated_ok, "all generated files are under post-checkpoint-work"),
        ("V1050_12_formalization_untouched", formalization_changed == 0, f"formalization-workbench modified-file count since script start is {formalization_changed}"),
    ]
    return [
        {
            "check_id": check_id,
            "result": status(result),
            "detail": detail,
            "generated_utc": stamp(),
        }
        for check_id, result, detail in checks
    ]


def write_doc(sections: list[tuple[str, list[dict[str, object]], list[str]]]) -> None:
    lines = [
        "# 1050 Y5 R10 visible hidden product functor derivation or prior width source pack",
        "",
        "**Progress:** the product-functor theorem is now exact as a conditional. If visible EM, matter, clocks, and source coupling are pullbacks through `q_loc` plus representation data, hidden representative variations cannot generate `f_X F^2`, mass, binding, or clock-readout vertices.",
        "",
        "**Current verdict:** not parent-signed. The current corpus still permits nonconstant invariant scalars, has an unsigned Maxwell/alpha owner, an unsigned matter functor, open source-label forgetting, and no radiative/readout closure.",
        "",
        "**Fallback:** a prior-width source pack is staged for `b_alpha`, `b_mu`, `b_mA`, `b_nuc`, `b_clock_i`, and `qbar_source_label`. It is checklist-ready, not score-ready.",
        "",
    ]
    for title, rows, columns in sections:
        lines.extend([f"## {title}", md_table(rows, columns), ""])
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    theorem_rows = product_functor_rows()
    algebra_rows = visible_algebra_rows()
    obstructions = obstruction_rows()
    prior_rows = prior_width_source_rows()
    readiness_rows = projection_readiness_rows()
    mts_rows = mts_template_rows()
    write_csv(MTS_TEMPLATE, mts_rows, MTS_REQUIRED_COLUMNS)
    runner_result = run_runner(MTS_TEMPLATE, BOUND_CANDIDATE, RUN_DIR)
    runner_status = runner_result["status"]
    runner_rows = [
        {
            "smoke_id": "SMOKE1050_0_R10_runner_refusal",
            "valid_mts_rows": runner_status.get("valid_mts_rows"),
            "valid_bound_rows": runner_status.get("valid_bound_rows"),
            "comparison_rows": runner_status.get("comparison_rows"),
            "R10_pass_for_claim": str(runner_status.get("R10_pass_for_claim")).lower(),
            "claim_allowed": str(runner_status.get("claim_allowed")).lower(),
            "expected_result": "reject placeholders and keep claim false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]
    refusal_rows = placeholder_refusal_rows(runner_status)
    claim_rows = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_map: list[tuple[Path, list[dict[str, object]]]] = [
        (OUT / "P8_Y5_R10_1050_SOURCE_REGISTER.csv", source_rows),
        (OUT / "P8_Y5_R10_1050_PRODUCT_FUNCTOR_THEOREM_ATTEMPT.csv", theorem_rows),
        (OUT / "P8_Y5_R10_1050_VISIBLE_ALGEBRA_AUDIT.csv", algebra_rows),
        (OUT / "P8_Y5_R10_1050_PRODUCT_FUNCTOR_OBSTRUCTION_LEDGER.csv", obstructions),
        (OUT / "P8_Y5_R10_1050_PRIOR_WIDTH_SOURCE_PACK.csv", prior_rows),
        (OUT / "P8_Y5_R10_1050_PROJECTION_READINESS.csv", readiness_rows),
        (OUT / "P8_Y5_R10_1050_RUNNER_SMOKE_STATUS.csv", runner_rows),
        (OUT / "P8_Y5_R10_1050_PLACEHOLDER_REFUSAL_RUNNER.csv", refusal_rows),
        (OUT / "P8_Y5_R10_1050_CLAIM_GATES.csv", claim_rows),
        (OUT / "P8_Y5_R10_1050_DECISION_LEDGER.csv", decisions),
        (OUT / "P8_Y5_R10_1050_NEXT_TARGET.csv", next_rows),
    ]
    for path, rows in generated_map:
        write_csv(path, rows)
    validation = validation_rows(
        source_rows,
        theorem_rows,
        algebra_rows,
        obstructions,
        prior_rows,
        readiness_rows,
        mts_rows,
        runner_status,
        claim_rows,
        next_rows,
        [path for path, _ in generated_map] + [MTS_TEMPLATE, DOC],
    )
    validation_path = OUT / "P8_Y5_BRR545_1050_VALIDATION.csv"
    write_csv(validation_path, validation)
    write_doc(
        [
            ("Source register", source_rows, ["source_id", "source_path", "exists", "needle_found", "role"]),
            ("Product functor theorem attempt", theorem_rows, ["theorem_id", "claim_piece", "mathematical_form", "current_status", "missing_for_claim", "if_missing", "valid_for_claim"]),
            ("Visible algebra audit", algebra_rows, ["algebra_id", "visible_object", "allowed_arguments", "forbidden_arguments", "status", "residual_if_open", "valid_for_claim"]),
            ("Product functor obstruction ledger", obstructions, ["obstruction_id", "obstruction", "example", "source_evidence", "effect", "claim_allowed", "valid_for_claim"]),
            ("Prior-width source pack", prior_rows, ["pack_id", "symbol", "source_pack_target", "candidate_sources_in_hand", "still_missing", "promotion_status", "valid_for_claim"]),
            ("Projection readiness", readiness_rows, ["readiness_id", "arena", "ready_inputs", "missing_inputs", "status", "valid_for_claim"]),
            ("MTS R10 smoke template", mts_rows, ["model_id", "branch_id", "lambda_value", "alpha_predicted", "force_law_form", "derivation_status", "valid_for_claim"]),
            ("Runner smoke status", runner_rows, ["smoke_id", "valid_mts_rows", "valid_bound_rows", "comparison_rows", "R10_pass_for_claim", "claim_allowed", "expected_result"]),
            ("Placeholder refusal runner", refusal_rows, ["refusal_id", "object", "current_status", "refusal_status", "failure_reasons", "score_eligible", "claim_allowed"]),
            ("Claim gates", claim_rows, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            ("Decision ledger", decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            ("Validation", validation, ["check_id", "result", "detail", "generated_utc"]),
            ("Next target", next_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
        ]
    )
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    failed = [row for row in validation if row["result"] != "pass"]
    if failed:
        raise SystemExit(f"1050 validation failed: {failed}")
    print(f"Wrote {DOC}")
    print(f"Wrote {validation_path}")
    print(f"Runner claim_allowed={runner_status.get('claim_allowed')} valid_mts_rows={runner_status.get('valid_mts_rows')}")


if __name__ == "__main__":
    main()
