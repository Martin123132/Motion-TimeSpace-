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
DOC = ROOT / "1054-Y5-R10-beta-source-alpha-zero-theorem-or-first-numeric-prior-width.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1054-R10-beta-source-alpha-zero-theorem-or-prior-smoke" / "results"
MTS_TEMPLATE = OUT / "R10_alpha_lambda_curve_MTS_1054_ZERO_THEOREM_OR_PRIOR_TEMPLATE_NONCLAIM.csv"
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
        ("SRC1054_0_1053_next", "source-intake/mts_residuals/P8_Y5_R10_1053_NEXT_TARGET.csv", "1054-Y5-R10-beta-source-alpha-zero-theorem-or-first-numeric-prior-width.md", "1053 handoff to zero theorem or first numeric prior-width."),
        ("SRC1054_1_1053_beta", "source-intake/mts_residuals/P8_Y5_R10_1053_BETA_SOURCE_ALPHA_DERIVATION_AUDIT.csv", "BSA1053_4_zero_theorem_route", "beta_source_alpha zero route and missing clauses."),
        ("SRC1054_2_1053_cross_arena", "source-intake/mts_residuals/P8_Y5_R10_1053_CROSS_ARENA_ALPHA_CHAIN.csv", "CAC1053_1_WEP_alpha", "cross-arena alpha chain and WEP target."),
        ("SRC1054_3_980_no_marker", "source-intake/mts_residuals/P8_Y5_R10_980_NO_MARKER_FUNCTOR_THEOREM_ATTEMPT.csv", "NMF980_2_scalar_obstruction_lemma", "no-marker functor obstruction."),
        ("SRC1054_4_1050_product", "source-intake/mts_residuals/P8_Y5_R10_1050_PRODUCT_FUNCTOR_THEOREM_ATTEMPT.csv", "PFT1050_2_forbidden_mixed_hom", "visible-hidden product functor theorem attempt."),
        ("SRC1054_5_1050_obstruction", "source-intake/mts_residuals/P8_Y5_R10_1050_PRODUCT_FUNCTOR_OBSTRUCTION_LEDGER.csv", "OBS1050_0_scalar_invariant", "product functor obstruction ledger."),
        ("SRC1054_6_642_maxwell", "source-intake/mts_residuals/P8_Y5_R10_642_MAXWELL_DESCENT_ATTEMPT.csv", "MD642_4_alpha_constant", "Maxwell/alpha owner blocker."),
        ("SRC1054_7_1045_matter", "source-intake/mts_residuals/P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv", "MFS1045_6_verdict", "parent matter functor signature audit."),
        ("SRC1054_8_953_source", "source-intake/mts_residuals/P8_Y5_R10_953_SOURCE_FUNCTOR_THEOREM_ATTEMPT.csv", "NSF953_5_verdict", "source-label forgetting/source functor theorem."),
        ("SRC1054_9_1049_symmetry", "source-intake/mts_residuals/P8_Y5_R10_1049_SYMMETRY_BAN_THEOREM_ATTEMPT.csv", "SBT1049_4_product_functor", "ordinary symmetries versus product sequestering."),
        ("SRC1054_10_1049_operator", "source-intake/mts_residuals/P8_Y5_R10_1049_OPERATOR_CLASSIFICATION_RULE_ATTEMPT.csv", "OCR1049_5_verdict", "operator classification rule attempt."),
        ("SRC1054_11_1052_wep", "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv", "AWP1052_0_alpha_Coulomb", "WEP alpha pressure target."),
        ("SRC1054_12_1053_tau", "source-intake/mts_residuals/P8_Y5_R10_1053_TAU_WEP_R10_PROJECTION_AUDIT.csv", "TPR1053_1_tau_WEP_definition", "tau_WEP/tau_R10 missing projection audit."),
        ("SRC1054_13_1053_KX", "source-intake/mts_residuals/P8_Y5_R10_1053_KX_ZX_PLACEHOLDER_LEDGER.csv", "KZ1053_3_KX_R10", "K_X/Z_X/lambda placeholders."),
        ("SRC1054_14_R10_bound_candidate", "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv", "R10_VECTOR_2020_REVIEW_0000", "R10 review-candidate bound curve for smoke only."),
        ("SRC1054_15_R10_runner", "scripts/R10_alpha_lambda_bound_prediction_runner.py", "MTS_REQUIRED_COLUMNS", "Existing R10 runner and schema."),
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


def zero_clause_rows() -> list[dict[str, str]]:
    return [
        {
            "clause_id": "ZC1054_0_quotient_vertical",
            "required_clause": "q_loc exists and v_X is vertical",
            "mathematical_form": "Dq_loc[v_X]=0",
            "current_status": "CONDITIONAL_SUPPORT_NOT_PARENT_COMPLETE",
            "support": "MFS1045_0_parent_field_quotient",
            "if_signed": "hidden representative motion cannot change quotient-observed geometry",
            "if_unsigned": "geometry/source leakage can re-enter",
            "signed_now": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "ZC1054_1_visible_pullback",
            "required_clause": "visible EM/matter action is a quotient pullback",
            "mathematical_form": "S_vis=S_EM[A_Q,q_loc(Phi),theta_rep]+S_matter[Psi,e_obs(q),omega(q),theta_rep]",
            "current_status": "EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "support": "PFT1050_1_visible_action_pullback",
            "if_signed": "Lie_v of all visible pullback coefficients vanishes",
            "if_unsigned": "m_A(Xhat), f_X(Xhat), and binding/readout maps remain allowed",
            "signed_now": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "ZC1054_2_alpha_owner",
            "required_clause": "alpha_EM/gauge kinetic normalization is fixed by representation/topology or quotient data",
            "mathematical_form": "alpha_EM(Phi)=alpha_bar(q_loc(Phi),theta_top) so Lie_v alpha_EM=0",
            "current_status": "BLOCKED_OWNER_UNSIGNED",
            "support": "MD642_4_alpha_constant; OBS1050_1_alpha_owner",
            "if_signed": "b_alpha and beta_source_alpha alpha-marker vanish",
            "if_unsigned": "f_X(Xhat) F^2 is gauge/diffeomorphism allowed",
            "signed_now": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "ZC1054_3_no_hidden_visible_hom",
            "required_clause": "no hidden scalar may feed visible coefficients",
            "mathematical_form": "Hom(C_hid,Coeff(O_vis))=Const or absent",
            "current_status": "POWERFUL_BUT_UNSIGNED_WITH_COUNTEREXAMPLE",
            "support": "PFT1050_2_forbidden_mixed_hom; NMF980_2_scalar_obstruction_lemma",
            "if_signed": "all Xhat-to-alpha/mass/clock/source coefficient maps are killed",
            "if_unsigned": "any surviving invariant scalar I permits c=c0+epsilon I",
            "signed_now": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "ZC1054_4_matter_readout_functor",
            "required_clause": "ordinary matter/readout functor has no shadow frame or material marker",
            "mathematical_form": "S_A=S_A[Psi_A,e_obs(q),omega(q),theta_A] with Lie_v theta_A=0",
            "current_status": "MATTER_CATEGORY_NOT_PARENT_CONSTRUCTED",
            "support": "MFS1045_2_matter_bundle_functor; MFS1045_4_no_shadow_frame; MFS1045_5_constants_split",
            "if_signed": "material alpha/mass/readout charges cannot become hidden markers",
            "if_unsigned": "WEP/clock source-test charge survives",
            "signed_now": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "ZC1054_5_source_label_forgetting",
            "required_clause": "source functor forgets species labels before coupling selection",
            "mathematical_form": "Obj(C_matter)->T_total, not Obj(C_matter)->(T_A,A)",
            "current_status": "CONDITIONAL_PROOF_NOT_PARENT_DERIVATION",
            "support": "NSF953_5_verdict",
            "if_signed": "relative source weights and WEP beta_source_alpha slots are structurally unavailable",
            "if_unsigned": "kappa_A T_A and composition-sensitive source weights remain additive/covariant",
            "signed_now": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "ZC1054_6_radiative_readout_closure",
            "required_clause": "EFT, loops, and clock/readout reductions preserve sequestering",
            "mathematical_form": "S_vis^eff and readout maps still factor through q_loc and theta_rep",
            "current_status": "UNSIGNED",
            "support": "PFT1050_3_radiative_readout_closure; SBT1049_5_radiative_readout_closure",
            "if_signed": "tree-level zero is stable under effective reduction",
            "if_unsigned": "loop/readout induced f_X F^2 or clock residual can regenerate coupling",
            "signed_now": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def formal_proof_rows() -> list[dict[str, str]]:
    return [
        {
            "proof_id": "FP1054_0_theorem_statement",
            "step": "target theorem",
            "statement": "If clauses ZC1054_0 through ZC1054_6 are parent-signed, then beta_source_alpha=0 and the finite alpha-marker WEP/R10 branch has no source charge.",
            "derivation": "The theorem is conditional: all visible alpha/matter/source/readout coefficient maps are constant on the vertical hidden fiber.",
            "status": "EXACT_CONDITIONAL_TARGET",
            "claim_allowed_now": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "proof_id": "FP1054_1_pullback_derivative",
            "step": "vertical derivative",
            "statement": "For any visible coefficient c(Phi)=cbar(q_loc(Phi),theta_rep), Lie_v c = D cbar[Dq_loc[v]] = 0.",
            "derivation": "This is the clean quotient calculus move: vertical hidden motion cannot change pullback coefficients.",
            "status": "PROVED_IF_PULLBACK_CLAUSES_SIGNED",
            "claim_allowed_now": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "proof_id": "FP1054_2_alpha_beta",
            "step": "alpha coupling",
            "statement": "If alpha_EM is one of those pullback/topological coefficients, then b_alpha = Lie_v ln(alpha_EM)=0 and the alpha-marker beta_source_alpha slot is absent.",
            "derivation": "The WEP alpha channel uses a hidden derivative of an EM coefficient; the derivative vanishes when the coefficient descends.",
            "status": "BLOCKED_BY_ALPHA_OWNER_UNSIGNED",
            "claim_allowed_now": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "proof_id": "FP1054_3_source_charge",
            "step": "source/test charge",
            "statement": "If matter/source functors forget hidden and species-marker data, beta_s=beta_t=0 for the alpha-marker branch.",
            "derivation": "The standard beta_i=partial_Xhat ln(m_i^eff) has zero numerator when m_i^eff is not a function of Xhat.",
            "status": "BLOCKED_BY_MATTER_SOURCE_FUNCTOR_UNSIGNED",
            "claim_allowed_now": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "proof_id": "FP1054_4_WEP_consequence",
            "step": "WEP consequence",
            "statement": "eta_AB_alpha = DeltaQ_alpha_AB * beta_source_alpha * b_alpha * tau_WEP = 0 if the alpha-marker source or alpha coefficient derivative is theorem-zero.",
            "derivation": "This would beat the WEP pressure without tuning; however the zero premise is not signed.",
            "status": "CONDITIONAL_PASS_ONLY",
            "claim_allowed_now": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "proof_id": "FP1054_5_R10_consequence",
            "step": "R10 consequence",
            "statement": "alpha_X(lambda)=K_X^R10 beta_s beta_t + epsilon_tail gives zero alpha-marker exchange if beta_s=beta_t=epsilon_tail=0 by the same parent functor.",
            "derivation": "This is stronger than bounding K_X/Z_X, but it needs no-tail/no-marker clauses too.",
            "status": "CONDITIONAL_PASS_ONLY_TAIL_UNSIGNED",
            "claim_allowed_now": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "proof_id": "FP1054_6_verdict",
            "step": "current verdict",
            "statement": "The zero proof is valid as an exact parent-action contract, not as a current theorem of the corpus.",
            "derivation": "Several necessary clauses are explicitly unsigned and known counterexamples remain legal.",
            "status": "ZERO_THEOREM_NOT_CLOSED_CURRENT_CORPUS",
            "claim_allowed_now": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def obstruction_rows() -> list[dict[str, str]]:
    return [
        {
            "obstruction_id": "OBS1054_0_scalar_invariant",
            "counterexample": "surviving invariant scalar I feeds alpha or matter coefficients",
            "formula": "alpha_EM(I)=alpha_0 exp(epsilon I) or f_X(I)F^2",
            "source": "NMF980_2_scalar_obstruction_lemma; OBS1050_0_scalar_invariant",
            "effect": "kills unconditional no-marker/no-alpha theorem",
            "required_repair": "prove hidden invariant algebra trivial or forbid coefficient target by parent action",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "obstruction_id": "OBS1054_1_alpha_owner",
            "counterexample": "gauge kinetic function depends on Xhat",
            "formula": "S_EM=-1/4 f(Xhat) F_Q^2",
            "source": "MD642_4_alpha_constant; SBT1049_1_gauge_invariance",
            "effect": "gauge and diffeomorphism invariance do not ban b_alpha",
            "required_repair": "topological/representation owner for alpha_EM or product sequestering",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "obstruction_id": "OBS1054_2_shadow_matter_frame",
            "counterexample": "matter mass or readout frame carries Xhat",
            "formula": "m_A(Xhat) psi_bar_A psi_A or A_A(Xhat)^2 g_obs",
            "source": "MFS1045_4_no_shadow_frame; OBS1050_2_matter_category",
            "effect": "source/test beta charges survive despite quotient geometry",
            "required_repair": "parent matter functor with fixed representation constants and no shadow frame",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "obstruction_id": "OBS1054_3_source_labels",
            "counterexample": "species-labelled source functor remains additive and covariant",
            "formula": "F((T_A,A))=kappa_A T_A",
            "source": "NSF953_1_domain_fork; NSF953_3_additivity_limit",
            "effect": "relative WEP/R10 source weights remain legal",
            "required_repair": "parent category must forget species labels before source coupling selection",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "obstruction_id": "OBS1054_4_radiative_readout",
            "counterexample": "loop/readout reduction regenerates an Xhat-dependent coefficient",
            "formula": "S_vis^eff contains delta f_X(Xhat)F^2 or clock_Xhat readout term",
            "source": "PFT1050_3_radiative_readout_closure; SBT1049_5_radiative_readout_closure",
            "effect": "tree-level zero is not enough for claim-grade local tests",
            "required_repair": "radiative/readout closure theorem or retained residual prior",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def numeric_prior_width_rows() -> list[dict[str, str]]:
    return [
        {
            "prior_id": "NPW1054_0_alpha_WEP_product",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "C_alpha_WEP := beta_source_alpha*b_alpha*tau_WEP",
            "numeric_bound": "4.797780522732e-05",
            "units": "dimensionless under the 1052 smoke convention",
            "formula": "eta_bound/unit_source_eta_prediction for alpha/Coulomb channel",
            "source": "AWP1052_0_alpha_Coulomb; BSA1053_2_alpha_Coulomb_bound_target",
            "what_it_bounds": "only the combined alpha WEP product, not standalone beta_source_alpha",
            "missing_to_isolate_beta_source_alpha": "standalone b_alpha; tau_WEP; full material convention",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "prior_id": "NPW1054_1_surface_WEP_product",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "C_surface_WEP := beta_source_or_binding*b_A*tau_WEP",
            "numeric_bound": "2.887280314062e-05",
            "units": "dimensionless under the 1052 smoke convention",
            "formula": "eta_bound/unit_source_eta_prediction for surface/binding channel",
            "source": "AWP1052_1_surface_binding; BSA1053_3_surface_binding_target",
            "what_it_bounds": "robust finite branch if binding/surface response survives",
            "missing_to_isolate_beta_source_alpha": "binding coefficient owner; tau_WEP; full material convention",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "prior_id": "NPW1054_2_clock_product",
            "arena": "clock",
            "product_symbol": "C_alpha_clock := b_alpha*tau_clock_time",
            "numeric_bound": "2.1e-18",
            "units": "yr^-1",
            "formula": "best current Yb+ E3/E2 clock product row",
            "source": "ACB1052_2; CAC1053_0_clock",
            "what_it_bounds": "time-drift product only",
            "missing_to_isolate_beta_source_alpha": "not a source normalization; needs bridge to tau_WEP/R10",
            "score_ready": "true_nonclaim_only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "prior_id": "NPW1054_3_R10_product",
            "arena": "R10_short_range",
            "product_symbol": "C_R10(lambda):=K_X^R10(lambda)*beta_s(lambda)*beta_t(lambda)+epsilon_tail(lambda)",
            "numeric_bound": "MISSING_PROMOTED_ALPHA_BOUND_AND_MTS_FACTORS",
            "units": "dimensionless alpha(lambda)",
            "formula": "abs(C_R10(lambda)) <= alpha_bound(lambda)",
            "source": "CAC1053_3_R10; KZ1053_3_KX_R10",
            "what_it_bounds": "finite Yukawa-like exchange branch once all factors are sourced",
            "missing_to_isolate_beta_source_alpha": "lambda_X; Z_X; K_X(lambda); beta_s; beta_t; tau_R10; promoted bound curve",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def shared_normalization_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "SNG1054_0_no_rescale_escape",
            "requirement": "same parent Xhat/chi_X normalization feeds all arenas",
            "status": "UNSIGNED",
            "reason": "otherwise one can shrink WEP while keeping clock/R10 independent by convention",
            "blocked_claims": "standalone beta_source_alpha; WEP pass; R10 pass",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "SNG1054_1_clock_to_WEP",
            "requirement": "map tau_clock_time to tau_WEP or prove independent WEP zero",
            "status": "MISSING",
            "reason": "clock product is time drift; WEP is source/test force response",
            "blocked_claims": "using 2.1e-18 yr^-1 to pass MICROSCOPE",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "SNG1054_2_WEP_to_R10",
            "requirement": "map WEP source normalization to beta_s beta_t K_X/Z_X tau_R10",
            "status": "MISSING",
            "reason": "short-range torque needs profile/material kernel, not just composition DeltaQ",
            "blocked_claims": "R10 alpha(lambda) score",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "SNG1054_3_zero_beats_all",
            "requirement": "if the parent no-alpha/no-marker theorem closes, arena tau factors become irrelevant for that branch",
            "status": "CONDITIONAL_ONLY",
            "reason": "zero source charge makes alpha-marker WEP/R10 branch vanish before fitting",
            "blocked_claims": "currently still blocked because zero theorem is unsigned",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def promotion_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "PRG1054_0_zero_theorem",
            "claim_piece": "beta_source_alpha=0 theorem",
            "gate_pass": "false",
            "reason": "all theorem clauses are exact but unsigned; known scalar/alpha/matter/source counterexamples remain legal",
            "promotion_requirement": "parent action signs ZC1054_0 through ZC1054_6",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "PRG1054_1_first_numeric_prior",
            "claim_piece": "first numeric beta_source_alpha prior",
            "gate_pass": "false",
            "reason": "WEP gives product-width targets, not standalone beta_source_alpha",
            "promotion_requirement": "source tau_WEP and b_alpha in the same material convention or report only product prior",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "PRG1054_2_WEP",
            "claim_piece": "WEP alpha branch passes",
            "gate_pass": "false",
            "reason": "either zero theorem or product value <= target is required; neither is currently supplied by MTS",
            "promotion_requirement": "theorem-zero or numeric C_alpha_WEP prediction",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "PRG1054_3_R10",
            "claim_piece": "R10 finite branch passes",
            "gate_pass": "false",
            "reason": "zero theorem would pass structurally; finite branch still lacks K_X/Z_X/lambda/tau/beta and promoted bound curve",
            "promotion_requirement": "zero theorem or full alpha(lambda) prediction with claim-valid bound curve",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def mts_template_rows() -> list[dict[str, str]]:
    row = {
        "model_id": "MTS_source_normalized_Newton_branch",
        "branch_id": "zero_theorem_or_prior_width_template",
        "curve_id": "MTS_1054_zero_theorem_or_prior_nonclaim",
        "lambda_value": "MISSING_LAMBDA_X",
        "lambda_units": "m",
        "alpha_predicted": "MISSING_ZERO_THEOREM_OR_NUMERIC_C_R10",
        "alpha_bound": "MISSING_PROMOTED_BOUND",
        "alpha_bound_source": str(BOUND_CANDIDATE),
        "force_law_form": "zero theorem route gives alpha_marker(lambda)=0 only if parent no-alpha/no-marker clauses are signed; finite route needs K_X^R10 beta_s beta_t",
        "derivation_status": "template_invalid_zero_theorem_unsigned_and_numeric_prior_product_only",
        "formula_reference": "P8_Y5_R10_1054_FORMAL_ZERO_PROOF_ATTEMPT.csv",
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_1054_FORMAL_ZERO_PROOF_ATTEMPT.csv",
        "assumptions": "nonclaim placeholder; no unit-rescaling; no cancellation; no tau unity shortcut",
        "valid_for_claim": "false",
        "notes": "Runner must refuse this row until either the zero theorem is parent-signed or a full finite alpha(lambda) prediction is sourced.",
    }
    return [{column: row[column] for column in MTS_REQUIRED_COLUMNS}]


def runner_smoke_rows(status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "smoke_id": "SMOKE1054_0_R10_runner_refusal",
            "valid_mts_rows": str(status.get("valid_mts_rows", "")),
            "valid_bound_rows": str(status.get("valid_bound_rows", "")),
            "comparison_rows": str(status.get("comparison_rows", "")),
            "R10_pass_for_claim": str(status.get("R10_pass_for_claim", "")).lower(),
            "claim_allowed": str(status.get("claim_allowed", "")).lower(),
            "expected_result": "reject unsigned zero theorem and product-prior placeholders",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def refusal_rows(status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "refusal_id": "REF1054_0_zero_theorem",
            "object": "beta_source_alpha=0",
            "current_status": "ZERO_THEOREM_NOT_CLOSED_CURRENT_CORPUS",
            "refusal_status": "blocked",
            "failure_reasons": "alpha owner, hidden-visible hom ban, matter functor, source label forgetting, and radiative closure unsigned",
            "score_eligible": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "refusal_id": "REF1054_1_numeric_prior",
            "object": "standalone beta_source_alpha prior",
            "current_status": "PRODUCT_WIDTH_ONLY",
            "refusal_status": "blocked",
            "failure_reasons": "WEP gives beta_source_alpha*b_alpha*tau_WEP target, not beta_source_alpha alone",
            "score_eligible": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "refusal_id": "REF1054_2_R10_runner",
            "object": "R10 zero/prior placeholder smoke row",
            "current_status": "runner_refusal_expected",
            "refusal_status": "blocked",
            "failure_reasons": f"valid_mts_rows={status.get('valid_mts_rows')}; valid_bound_rows={status.get('valid_bound_rows')}",
            "score_eligible": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1054_0_beta_source_alpha_zero",
            "claim": "beta_source_alpha is theorem-zero",
            "gate_pass": "false",
            "reason": "conditional proof is exact but parent clauses are unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1054_1_numeric_beta_prior",
            "claim": "standalone numeric beta_source_alpha prior exists",
            "gate_pass": "false",
            "reason": "only product-width targets are available",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1054_2_WEP",
            "claim": "WEP alpha branch passes",
            "gate_pass": "false",
            "reason": "requires theorem-zero or a sourced product prediction below 4.797780522732e-05",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1054_3_R10",
            "claim": "R10 alpha(lambda) branch passes",
            "gate_pass": "false",
            "reason": "requires theorem-zero or full finite alpha(lambda) inputs",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1054_0_theorem_result",
            "decision": "zero theorem is exact as a contract but not proven by the current corpus",
            "because": "the proof works if pullback/no-alpha/no-marker/source/radiative clauses are parent-signed, and they are not",
            "next_action": "construct the parent action clause that owns alpha_EM and matter/readout constants",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1054_1_prior_result",
            "decision": "first numeric width is a product target, not standalone beta_source_alpha",
            "because": "WEP bounds C_alpha_WEP := beta_source_alpha*b_alpha*tau_WEP <= 4.797780522732e-05 in the smoke convention",
            "next_action": "do not call this a beta prior unless b_alpha and tau_WEP are sourced in the same convention",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1054_2_best_next",
            "decision": "go after the parent alpha-owner and matter-functor action contract",
            "because": "that is the clause most directly blocking beta_source_alpha=0 and therefore WEP/R10 survival",
            "next_action": "1055-Y5-R10-alpha-owner-and-matter-functor-parent-action-contract.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1055-Y5-R10-alpha-owner-and-matter-functor-parent-action-contract.md",
            "objective": "construct or reject the parent action clause that makes alpha_EM, masses, binding terms, and readout constants representation/topological quotient data rather than hidden-field functions",
            "include": "gauge kinetic owner, matter mass/readout functor, no hidden-visible coefficient hom, radiative closure, source-label forgetting, consequences for beta_source_alpha=0",
            "exclude": "aesthetic minimality as proof, unit-rescaling, cancellation, tau unity shortcut, public local-GR/R10/WEP/clock claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def count_formalization_modified_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    start_time = STARTED.timestamp()
    for path in FORMALIZATION.rglob("*"):
        try:
            if path.is_file() and path.stat().st_mtime > start_time:
                count += 1
        except OSError:
            continue
    return count


def validate_outputs(
    outputs: dict[str, Path],
    source_rows: list[dict[str, str]],
    clauses: list[dict[str, str]],
    proof_rows: list[dict[str, str]],
    obstructions: list[dict[str, str]],
    prior_rows: list[dict[str, str]],
    normalization_rows: list[dict[str, str]],
    template_rows: list[dict[str, str]],
    runner_status: dict[str, Any],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                "check_id": check_id,
                "result": "pass" if passed else "fail",
                "detail": detail,
                "generated_utc": stamp(),
            }
        )

    source_ok = all(flag(row.get("exists", "")) and flag(row.get("needle_found", "")) for row in source_rows)
    add("V1054_1_sources_exist_and_needles", source_ok, "every cited source path exists and every source needle was found")
    clauses_unsigned = clauses and all(row.get("signed_now") == "false" and row.get("valid_for_claim") == "false" for row in clauses)
    add("V1054_2_zero_clauses_unsigned", clauses_unsigned, "all zero-theorem clauses are audited as unsigned/nonclaim")
    proof_blocked = any(row.get("proof_id") == "FP1054_6_verdict" and row.get("status") == "ZERO_THEOREM_NOT_CLOSED_CURRENT_CORPUS" for row in proof_rows)
    add("V1054_3_formal_proof_conditional_only", proof_blocked, "formal proof is conditional only and not promoted")
    obstruction_ok = len(obstructions) >= 5 and all(row.get("claim_allowed") == "false" for row in obstructions)
    add("V1054_4_obstructions_retained", obstruction_ok, "known counterexamples remain retained and claim-blocking")
    product_width = any(row.get("prior_id") == "NPW1054_0_alpha_WEP_product" and row.get("numeric_bound") == "4.797780522732e-05" for row in prior_rows)
    no_standalone = all(row.get("valid_for_claim") == "false" for row in prior_rows)
    add("V1054_5_numeric_prior_product_only", product_width and no_standalone, "numeric prior-width rows are product targets only")
    normalization_blocked = normalization_rows and all(row.get("valid_for_claim") == "false" for row in normalization_rows)
    add("V1054_6_shared_normalization_blocked", normalization_blocked, "shared normalization gates remain blocked")
    template_schema = set(MTS_REQUIRED_COLUMNS).issubset(set(template_rows[0].keys())) if template_rows else False
    template_nonclaim = template_schema and all(row.get("valid_for_claim") == "false" for row in template_rows)
    add("V1054_7_mts_template_schema_nonclaim", template_nonclaim, "MTS template has runner schema and no claim-valid rows")
    runner_refused = runner_status.get("valid_mts_rows") == 0 and runner_status.get("claim_allowed") is False
    add("V1054_8_runner_smoke_refuses_claim", runner_refused, "existing R10 runner refuses the 1054 placeholder rows")
    claims_blocked = claim_rows and all(row.get("gate_pass") == "false" and row.get("claim_allowed") == "false" for row in claim_rows)
    add("V1054_9_claim_gates_blocked", claims_blocked, "all zero/prior/WEP/R10 claim gates remain blocked")
    next_ok = bool(next_rows) and next_rows[0].get("next_target", "").startswith("1055-Y5-R10-alpha-owner")
    add("V1054_10_next_target_written", next_ok, "next target row is present")
    generated_inside = all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in outputs.values())
    add("V1054_11_generated_files_in_post_checkpoint", generated_inside, "all generated files are under post-checkpoint-work")
    formalization_count = count_formalization_modified_since_start()
    add("V1054_12_formalization_untouched", formalization_count == 0, f"formalization-workbench modified-file count since script start is {formalization_count}")

    summary_pass = all(row["result"] == "pass" for row in checks)
    checks.insert(
        0,
        {
            "check_id": "V1054_SUMMARY",
            "result": "pass" if summary_pass else "fail",
            "detail": "1054 beta-source-alpha zero theorem or first numeric prior-width validation summary",
            "generated_utc": stamp(),
        },
    )
    return checks


def write_doc(
    source_rows: list[dict[str, str]],
    clauses: list[dict[str, str]],
    proof_rows: list[dict[str, str]],
    obstructions: list[dict[str, str]],
    prior_rows: list[dict[str, str]],
    normalization_rows: list[dict[str, str]],
    promotion_rows: list[dict[str, str]],
    template_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
    refusal_rows_: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1054 Y5 R10 beta source alpha zero theorem or first numeric prior width",
            "",
            "**Progress:** the zero route is now a precise theorem contract. If the parent action makes visible EM, matter, readout, and source coefficients quotient/representation data, then `beta_source_alpha=0` follows by vertical differentiation.",
            "",
            "**Current verdict:** the proof is not false, but it is not closed. The dangerous clauses are exactly the alpha owner, hidden-visible coefficient hom ban, matter/readout functor, source-label forgetting, and radiative/readout closure.",
            "",
            "**Numeric fallback:** the first real width is not a standalone coupling. It is the WEP product target `|beta_source_alpha*b_alpha*tau_WEP| <= 4.797780522732e-05` in the current smoke convention.",
            "",
            "## Source register",
            md_table(source_rows, ["source_id", "source_path", "exists", "needle_found", "role"]),
            "",
            "## Zero theorem clause audit",
            md_table(clauses, ["clause_id", "required_clause", "current_status", "mathematical_form", "if_signed", "if_unsigned", "signed_now", "valid_for_claim"]),
            "",
            "## Formal zero proof attempt",
            md_table(proof_rows, ["proof_id", "step", "statement", "status", "claim_allowed_now", "valid_for_claim"]),
            "",
            "## Counterexample obstruction ledger",
            md_table(obstructions, ["obstruction_id", "counterexample", "formula", "source", "effect", "required_repair", "claim_allowed"]),
            "",
            "## Numeric prior width ledger",
            md_table(prior_rows, ["prior_id", "arena", "product_symbol", "numeric_bound", "units", "what_it_bounds", "missing_to_isolate_beta_source_alpha", "valid_for_claim"]),
            "",
            "## Shared normalization gate",
            md_table(normalization_rows, ["gate_id", "requirement", "status", "reason", "blocked_claims", "valid_for_claim"]),
            "",
            "## Promotion refusal gates",
            md_table(promotion_rows, ["gate_id", "claim_piece", "gate_pass", "reason", "promotion_requirement", "claim_allowed", "valid_for_claim"]),
            "",
            "## MTS R10 smoke template",
            md_table(template_rows, ["model_id", "branch_id", "lambda_value", "alpha_predicted", "force_law_form", "derivation_status", "valid_for_claim"]),
            "",
            "## Runner smoke status",
            md_table(smoke_rows, ["smoke_id", "valid_mts_rows", "valid_bound_rows", "comparison_rows", "R10_pass_for_claim", "claim_allowed", "expected_result"]),
            "",
            "## Placeholder refusal runner",
            md_table(refusal_rows_, ["refusal_id", "object", "current_status", "refusal_status", "failure_reasons", "score_eligible", "claim_allowed"]),
            "",
            "## Claim gates",
            md_table(claim_rows, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "",
            "## Decision ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "",
            "## Validation",
            md_table(validation_rows, ["check_id", "result", "detail", "generated_utc"]),
            "",
            "## Next target",
            md_table(next_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    clauses = zero_clause_rows()
    proof_rows = formal_proof_rows()
    obstructions = obstruction_rows()
    prior_rows = numeric_prior_width_rows()
    normalization_rows = shared_normalization_rows()
    promotion_rows = promotion_gate_rows()
    template_rows = mts_template_rows()

    outputs: dict[str, Path] = {
        "source_register": OUT / "P8_Y5_R10_1054_SOURCE_REGISTER.csv",
        "zero_clauses": OUT / "P8_Y5_R10_1054_ZERO_THEOREM_CLAUSE_AUDIT.csv",
        "formal_proof": OUT / "P8_Y5_R10_1054_FORMAL_ZERO_PROOF_ATTEMPT.csv",
        "obstructions": OUT / "P8_Y5_R10_1054_COUNTEREXAMPLE_OBSTRUCTION_LEDGER.csv",
        "prior_width": OUT / "P8_Y5_R10_1054_NUMERIC_PRIOR_WIDTH_LEDGER.csv",
        "shared_normalization": OUT / "P8_Y5_R10_1054_SHARED_NORMALIZATION_GATE.csv",
        "promotion_gates": OUT / "P8_Y5_R10_1054_PROMOTION_REFUSAL_GATES.csv",
        "mts_template": MTS_TEMPLATE,
        "runner_smoke": OUT / "P8_Y5_R10_1054_RUNNER_SMOKE_STATUS.csv",
        "placeholder_refusal": OUT / "P8_Y5_R10_1054_PLACEHOLDER_REFUSAL_RUNNER.csv",
        "claim_gates": OUT / "P8_Y5_R10_1054_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1054_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1054_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1054_VALIDATION.csv",
        "doc": DOC,
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["zero_clauses"], clauses)
    write_csv(outputs["formal_proof"], proof_rows)
    write_csv(outputs["obstructions"], obstructions)
    write_csv(outputs["prior_width"], prior_rows)
    write_csv(outputs["shared_normalization"], normalization_rows)
    write_csv(outputs["promotion_gates"], promotion_rows)
    write_csv(outputs["mts_template"], template_rows, MTS_REQUIRED_COLUMNS)

    runner_result = run_runner(MTS_TEMPLATE, BOUND_CANDIDATE, RUN_DIR)
    runner_status = runner_result["status"]
    smoke_rows = runner_smoke_rows(runner_status)
    refusal_rows_ = refusal_rows(runner_status)
    claim_rows = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(outputs["runner_smoke"], smoke_rows)
    write_csv(outputs["placeholder_refusal"], refusal_rows_)
    write_csv(outputs["claim_gates"], claim_rows)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next_target"], next_rows)

    validation_rows = validate_outputs(
        outputs,
        source_rows,
        clauses,
        proof_rows,
        obstructions,
        prior_rows,
        normalization_rows,
        template_rows,
        runner_status,
        claim_rows,
        next_rows,
    )
    write_csv(outputs["validation"], validation_rows)
    write_doc(
        source_rows,
        clauses,
        proof_rows,
        obstructions,
        prior_rows,
        normalization_rows,
        promotion_rows,
        template_rows,
        smoke_rows,
        refusal_rows_,
        claim_rows,
        decisions,
        validation_rows,
        next_rows,
    )

    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
