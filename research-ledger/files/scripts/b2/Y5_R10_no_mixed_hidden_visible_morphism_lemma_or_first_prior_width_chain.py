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
DOC = ROOT / "1051-Y5-R10-no-mixed-hidden-visible-morphism-lemma-or-first-prior-width-chain.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1051-R10-no-mixed-or-balpha-chain-smoke" / "results"
MTS_TEMPLATE = OUT / "R10_alpha_lambda_curve_MTS_1051_B_ALPHA_CHAIN_TEMPLATE_NONCLAIM.csv"
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


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


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
            "SRC1051_0_1050_next",
            "source-intake/mts_residuals/P8_Y5_R10_1050_NEXT_TARGET.csv",
            "1051-Y5-R10-no-mixed-hidden-visible-morphism-lemma-or-first-prior-width-chain.md",
            "1050 handoff to no-mixed morphism or first prior chain.",
        ),
        (
            "SRC1051_1_1050_theorem",
            "source-intake/mts_residuals/P8_Y5_R10_1050_PRODUCT_FUNCTOR_THEOREM_ATTEMPT.csv",
            "PFT1050_2_forbidden_mixed_hom",
            "1050 product functor theorem attempt.",
        ),
        (
            "SRC1051_2_1050_obstructions",
            "source-intake/mts_residuals/P8_Y5_R10_1050_PRODUCT_FUNCTOR_OBSTRUCTION_LEDGER.csv",
            "OBS1050_0_scalar_invariant",
            "1050 product functor obstruction ledger.",
        ),
        (
            "SRC1051_3_1050_prior_pack",
            "source-intake/mts_residuals/P8_Y5_R10_1050_PRIOR_WIDTH_SOURCE_PACK.csv",
            "PWP1050_0_b_alpha",
            "1050 prior-width source pack.",
        ),
        (
            "SRC1051_4_980_no_marker_functor",
            "source-intake/mts_residuals/P8_Y5_R10_980_NO_MARKER_FUNCTOR_THEOREM_ATTEMPT.csv",
            "NMF980_2_scalar_obstruction_lemma",
            "Scalar invariant obstruction to no-marker/no-mixed functors.",
        ),
        (
            "SRC1051_5_642_maxwell",
            "source-intake/mts_residuals/P8_Y5_R10_642_MAXWELL_DESCENT_ATTEMPT.csv",
            "MD642_4_alpha_constant",
            "Maxwell descent alpha-owner blocker.",
        ),
        (
            "SRC1051_6_646_clock_sensitivity",
            "source-intake/mts_residuals/P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv",
            "CAS646_1_YbE3E2",
            "Clock alpha sensitivity source rows.",
        ),
        (
            "SRC1051_7_988_clock_product",
            "source-intake/mts_residuals/P8_Y5_R10_988_CLOCK_PRODUCT_IMPORT.csv",
            "CLOCK988_CAS646_1_YbE3E2",
            "Existing source-backed b_alpha*tau_clock product bound.",
        ),
        (
            "SRC1051_8_988_joint_alpha",
            "source-intake/mts_residuals/P8_Y5_R10_988_JOINT_ALPHA_VARIABLE_GATE.csv",
            "JAV988_1_clock_product",
            "Joint alpha variable gate and clock product warning.",
        ),
        (
            "SRC1051_9_local_bounds",
            "source-intake/local_bounds/local_bound_claims.csv",
            "R1_WEP_source_charge",
            "Local WEP/source, clock, PPN, and Gdot anchors.",
        ),
        (
            "SRC1051_10_R10_bound_candidate",
            "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "R10_VECTOR_2020_REVIEW_0000",
            "R10 nonclaim review-candidate curve for smoke only.",
        ),
        (
            "SRC1051_11_R10_runner",
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


def no_mixed_morphism_rows() -> list[dict[str, str]]:
    return [
        {
            "lemma_id": "NMM1051_0_target",
            "claim_piece": "no nonconstant hidden-to-visible coefficient morphism",
            "mathematical_form": "Hom(C_hid, Coeff(O_vis)) = Const or 0 for O_vis in {F^2,mass,Yukawa,binding,clock,source}",
            "proof_status": "TARGET_SHARP",
            "obstruction": "none at definition level",
            "if_true": "kills f_X F^2 and b_alpha/mass/clock/source coefficient maps",
            "if_false": "retain coefficient priors",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "lemma_id": "NMM1051_1_trivial_hidden_algebra_case",
            "claim_piece": "trivial hidden invariant algebra implies no mixed morphism",
            "mathematical_form": "O(C_hid)^inv = R => any natural scalar coefficient c:C_hid->R is constant",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "obstruction": "current corpus has not proved hidden invariant algebra triviality",
            "if_true": "product functor can close visible coefficients",
            "if_false": "nonconstant scalar can feed visible coefficient",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "lemma_id": "NMM1051_2_scalar_counterexample",
            "claim_piece": "surviving invariant scalar generates a mixed coefficient morphism",
            "mathematical_form": "I in O(C_hid)^inv, dI != 0 => c_I=c0+epsilon I and DeltaS = c_I O_vis is natural/covariant",
            "proof_status": "COUNTEREXAMPLE_PROVED",
            "obstruction": "980 scalar-obstruction lemma directly applies",
            "if_true": "no-mixed lemma fails unless I is forbidden or visible coefficients cannot take I",
            "if_false": "would need proof that all candidate I are absent",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "lemma_id": "NMM1051_3_quotient_kernel_limit",
            "claim_piece": "Dq[v]=0 does not by itself kill hidden-to-visible coefficient maps",
            "mathematical_form": "Dq[v]=0, c(Phi)=c0+epsilon I_hid(Phi), Lie_v c = epsilon Lie_v I_hid can be nonzero",
            "proof_status": "LIMIT_IDENTIFIED",
            "obstruction": "quotient invisibility of geometry is not enough; coefficient functor domain must also exclude hidden invariants",
            "if_true": "forces separate no-mixed-morphism or prior route",
            "if_false": "would incorrectly claim constants descend from q",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "lemma_id": "NMM1051_4_radiative_readout_limit",
            "claim_piece": "bare no-mixed morphism does not automatically survive EFT/readout",
            "mathematical_form": "S_bare no mixed terms does not imply S_eff/readout no mixed terms without symmetry or closure theorem",
            "proof_status": "UNSIGNED_CLOSURE",
            "obstruction": "alpha and clock readout can re-enter through renormalized/effective coefficients",
            "if_true": "needs radiative/readout closure before zero claim",
            "if_false": "b_alpha and b_clock_i remain live",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "lemma_id": "NMM1051_5_verdict",
            "claim_piece": "no-mixed-hidden-visible morphism lemma promotion",
            "mathematical_form": "NMM1051_1 plus no scalar counterexamples plus radiative/readout closure => no mixed visible coefficients",
            "proof_status": "FAIL_CURRENT_CLAIM_FIRST_PRIOR_CHAIN_REQUIRED",
            "obstruction": "scalar invariant obstruction and alpha/readout closure are open",
            "if_true": "constant-sector zero route revives",
            "if_false": "build first b_alpha clock-product prior chain",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def invariant_obstruction_rows() -> list[dict[str, str]]:
    return [
        {
            "obstruction_id": "ISO1051_0_hidden_scalar_I",
            "candidate_invariant": "generic hidden/local scalar I_hid",
            "mixed_coefficient": "c_I=c0+epsilon I_hid",
            "visible_operator": "F_Q^2, m_A psi_bar psi, clock readout, source weight",
            "status": "OBSTRUCTION_PROVED_IF_I_SURVIVES",
            "needed_to_close": "prove O(C_hid)^inv=R or forbid Coeff(O_vis) from taking hidden arguments",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "obstruction_id": "ISO1051_1_Xhat_value",
            "candidate_invariant": "Xhat or normalized hidden representative amplitude",
            "mixed_coefficient": "f_X(Xhat)",
            "visible_operator": "F_Q^2",
            "status": "LIVE_UNLESS_PRODUCT_FUNCTOR_SIGNED",
            "needed_to_close": "exact shift/sequester/product functor or Xhat=0 theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "obstruction_id": "ISO1051_2_gradient_norm",
            "candidate_invariant": "nabla Xhat squared or local hidden profile norm",
            "mixed_coefficient": "f((nabla Xhat)^2)",
            "visible_operator": "mass/binding/clock coefficient",
            "status": "EVEN_PARITY_SURVIVOR",
            "needed_to_close": "positive no-hair/profile-zero theorem or product functor",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "obstruction_id": "ISO1051_3_domain_marker",
            "candidate_invariant": "domain/source/material class marker",
            "mixed_coefficient": "theta_A(marker), kappa_A(marker)",
            "visible_operator": "source/test coupling and matter constants",
            "status": "LIVE_LABEL_OBSTRUCTION",
            "needed_to_close": "source label-forgetting and no-marker functor theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def alpha_owner_rows() -> list[dict[str, str]]:
    return [
        {
            "audit_id": "AOR1051_0_Maxwell_descent",
            "object": "Maxwell action descent",
            "current_evidence": "MD642_0-3 support Maxwell closure form, but MD642_4 blocks alpha constant owner",
            "status": "PARTIAL",
            "missing_for_balpha_zero": "g_EM/alpha owner, Hodge/readout owner, source current normalization",
            "fallback": "b_alpha clock-product prior chain",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "AOR1051_1_clock_product",
            "object": "clock product bound",
            "current_evidence": "988 imports |b_alpha*tau_clock_time| product bounds from clock rows",
            "status": "SOURCE_BACKED_PRODUCT_BOUND_NONCLAIM",
            "missing_for_balpha_zero": "tau_clock dynamics and Xhat normalization",
            "fallback": "retain product bound, not standalone b_alpha",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "AOR1051_2_cross_arena",
            "object": "shared alpha branch across clock/WEP/R10",
            "current_evidence": "JAV988_3 warns S_lab_alpha cannot be clock-only",
            "status": "POLICY_GATE_ACTIVE",
            "missing_for_balpha_zero": "shared local domain/projection rule and WEP/R10 source charge maps",
            "fallback": "do not transfer clock product to WEP/R10 without projections",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "AOR1051_3_verdict",
            "object": "b_alpha zero/provenance",
            "current_evidence": "no-mixed morphism fails current claim and alpha owner remains unsigned",
            "status": "RETAIN_B_ALPHA_PRODUCT_CHAIN",
            "missing_for_balpha_zero": "no mixed morphism theorem or alpha owner/radiative closure",
            "fallback": "source-backed b_alpha*tau_clock product bound only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def balpha_prior_chain_rows() -> list[dict[str, str]]:
    clock_products = read_csv(OUT / "P8_Y5_R10_988_CLOCK_PRODUCT_IMPORT.csv")
    sensitivity_rows = {row.get("clock_pair", ""): row for row in read_csv(OUT / "P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv")}
    rows: list[dict[str, str]] = []
    for row in clock_products:
        clock_pair = row.get("clock_pair", "")
        sensitivity = sensitivity_rows.get(clock_pair, {})
        rows.append(
            {
                "chain_id": f"BAP1051_{len(rows)}_{row.get('import_id', '')}",
                "clock_pair": clock_pair,
                "delta_K_alpha": sensitivity.get("delta_K_alpha_used", "MISSING_DELTA_K_ALPHA"),
                "drift_source_value": sensitivity.get("alpha_drift_source_value", "MISSING_DRIFT_SOURCE"),
                "product_bound_1sigma_yr_inv": row.get("product_bound_1sigma_yr_inv", "MISSING_PRODUCT_BOUND"),
                "product_bound_2sigma_yr_inv": row.get("product_bound_2sigma_yr_inv", "MISSING_PRODUCT_BOUND"),
                "H0_normalized_diagnostic": row.get("H0_normalized_1sigma_if_assumed", ""),
                "formula": "|b_alpha*tau_clock_time| <= |d ln R/dt|_bound / |DeltaK_alpha|",
                "source_urls": sensitivity.get("source_urls", ""),
                "standalone_balpha_ready": "false",
                "missing_for_standalone": "tau_clock_time; Xhat/chi_X normalization; clock domain map; shared WEP/R10 projection",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    rows.append(
        {
            "chain_id": "BAP1051_2_best_current_product",
            "clock_pair": "171Yb+ E3 / 171Yb+ E2",
            "delta_K_alpha": "-6.95",
            "drift_source_value": "PTB/Frontiers imported row",
            "product_bound_1sigma_yr_inv": "2.1e-18",
            "product_bound_2sigma_yr_inv": "3.2e-18",
            "H0_normalized_diagnostic": "2.93296e-08",
            "formula": "best current imported product bound; diagnostic H0 normalization not a theory claim",
            "source_urls": "source-intake/mts_residuals/P8_Y5_R10_988_CLOCK_PRODUCT_IMPORT.csv; source-intake/mts_residuals/P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv",
            "standalone_balpha_ready": "false",
            "missing_for_standalone": "derive tau_clock_time from MTS local state",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    )
    return rows


def projection_readiness_rows() -> list[dict[str, str]]:
    return [
        {
            "projection_id": "BAPR1051_0_clock",
            "arena": "clock",
            "current_status": "SOURCE_BACKED_PRODUCT_BOUND_AVAILABLE",
            "usable_now": "|b_alpha*tau_clock_time| <= 2.1e-18 yr^-1 best imported 1sigma product row",
            "missing_for_claim": "tau_clock_time from MTS; alpha owner or no-mixed theorem; separation from other constants",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "projection_id": "BAPR1051_1_WEP",
            "arena": "WEP/MICROSCOPE",
            "current_status": "ANCHOR_ONLY",
            "usable_now": "eta bound exists, but alpha composition charge and beta_source_alpha are missing",
            "missing_for_claim": "DeltaQ_alpha_AB; beta_source_alpha; tau_WEP; shared domain rule",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "projection_id": "BAPR1051_2_R10",
            "arena": "R10 short-range",
            "current_status": "SMOKE_ONLY",
            "usable_now": "review-candidate bound curve exists but not promoted",
            "missing_for_claim": "lambda_X; Z_X; K_X; source/test alpha charge; promoted bound curve",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "projection_id": "BAPR1051_3_PPN",
            "arena": "local GR/PPN",
            "current_status": "NOT_SCORE_READY",
            "usable_now": "no direct PPN b_alpha map",
            "missing_for_claim": "weak-field/source Hamiltonian solution plus constant-sector leakage map",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def mts_template_rows() -> list[dict[str, str]]:
    return [
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "b_alpha_product_chain_template",
            "curve_id": "MTS_1051_B_ALPHA_PRODUCT_CHAIN_TEMPLATE",
            "lambda_value": "MISSING_LAMBDA_X",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_B_ALPHA_TAU_TO_R10_SOURCE_TEST_PROJECTION",
            "alpha_bound": "MISSING_PROMOTED_BOUND_CURVE",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "force_law_form": "R10 alpha(lambda) from b_alpha branch requires source/test alpha charges and tau_R10; clock product bound alone is not an R10 prediction",
            "derivation_status": "template_invalid_no_mixed_morphism_failed_and_R10_projection_missing",
            "formula_reference": "1051-Y5-R10-no-mixed-hidden-visible-morphism-lemma-or-first-prior-width-chain.md::BAP1051",
            "source_file": "MISSING_B_ALPHA_R10_PROJECTION_SOURCE_FILE",
            "assumptions": "private nonclaim; no cancellation; clock product bound cannot be transferred to R10 without domain/projection",
            "valid_for_claim": "false",
            "notes": "Runner must reject until b_alpha/tau/projection and promoted bound curve exist.",
        }
    ]


def placeholder_refusal_rows(runner_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "refusal_id": "REF1051_0_no_mixed",
            "object": "no-mixed hidden-visible morphism lemma",
            "current_status": "FAIL_CURRENT_CLAIM_FIRST_PRIOR_CHAIN_REQUIRED",
            "refusal_status": "blocked",
            "failure_reasons": "scalar invariant counterexample; hidden invariant algebra not trivial; radiative/readout closure unsigned",
            "score_eligible": "false",
            "claim_allowed": "false",
            "generated_utc": stamp(),
        },
        {
            "refusal_id": "REF1051_1_balpha_chain",
            "object": "b_alpha clock-product prior chain",
            "current_status": "PRODUCT_BOUND_AVAILABLE_STANDALONE_B_ALPHA_BLOCKED",
            "refusal_status": "blocked_for_standalone_claim",
            "failure_reasons": "tau_clock_time; Xhat normalization; shared WEP/R10 projection; alpha owner",
            "score_eligible": "false",
            "claim_allowed": "false",
            "generated_utc": stamp(),
        },
        {
            "refusal_id": "REF1051_2_R10_runner",
            "object": "R10 b_alpha placeholder smoke row",
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
            "gate_id": "CG1051_0_no_mixed",
            "claim": "no nonconstant hidden-to-visible coefficient morphism exists",
            "gate_pass": "false",
            "reason": "scalar invariant counterexample survives unless hidden invariant algebra is trivial or product functor is parent-signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1051_1_balpha_standalone",
            "claim": "clock rows give a standalone b_alpha bound",
            "gate_pass": "false",
            "reason": "clock rows bound b_alpha*tau_clock_time only; tau_clock is not derived",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1051_2_balpha_product",
            "claim": "clock product bound can be retained as nonclaim source-backed prior input",
            "gate_pass": "true_nonclaim_only",
            "reason": "988 product rows supply numerical b_alpha*tau_clock_time bounds, but promotion remains blocked",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1051_3_R10_WEP_transfer",
            "claim": "clock b_alpha product bound can be transferred to WEP/R10",
            "gate_pass": "false",
            "reason": "shared domain, composition charges, source/test projection, and tau_R10/tau_WEP are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1051_0_lemma_result",
            "decision": "no-mixed lemma fails current promotion",
            "because": "a surviving hidden invariant scalar can form a visible coefficient morphism",
            "next_action": "either prove invariant algebra triviality or keep residual priors",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1051_1_balpha_progress",
            "decision": "first numerical prior chain exists for b_alpha*tau_clock_time",
            "because": "988 imports clock product bounds from 646 sensitivities",
            "next_action": "derive tau_clock_time or source alpha WEP/R10 projections",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1051_2_best_next",
            "decision": "target tau_clock/Xhat normalization before transferring to other arenas",
            "because": "the clock product bound is useful but cannot become b_alpha or R10/WEP evidence without tau/projection",
            "next_action": "1052-Y5-R10-tau-clock-Xhat-normalization-or-alpha-WEP-R10-projection-source.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1052-Y5-R10-tau-clock-Xhat-normalization-or-alpha-WEP-R10-projection-source.md",
            "objective": "derive tau_clock_time and Xhat/chi_X normalization for the b_alpha clock-product chain; if that fails, source the alpha WEP/R10 composition/projection inputs needed to prevent clock-only screening",
            "include": "tau_clock map, Xhat normalization, H0 diagnostic caveat, alpha composition charges, WEP/R10 projection ledger, no-claim transfer gate",
            "exclude": "unit-rescaling cheat, cancellation, public local-GR/R10/WEP/clock claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validation_rows(
    source_rows: list[dict[str, str]],
    lemma_rows: list[dict[str, str]],
    invariant_rows: list[dict[str, str]],
    alpha_rows: list[dict[str, str]],
    balpha_rows: list[dict[str, str]],
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
    lemma_ok = any(row["lemma_id"] == "NMM1051_1_trivial_hidden_algebra_case" and row["proof_status"] == "EXACT_CONDITIONAL_THEOREM" for row in lemma_rows) and any(
        row["lemma_id"] == "NMM1051_5_verdict" and row["proof_status"].startswith("FAIL_CURRENT_CLAIM") for row in lemma_rows
    )
    invariant_ok = any(row["obstruction_id"] == "ISO1051_0_hidden_scalar_I" and row["status"] == "OBSTRUCTION_PROVED_IF_I_SURVIVES" for row in invariant_rows)
    alpha_ok = any(row["audit_id"] == "AOR1051_3_verdict" and row["status"] == "RETAIN_B_ALPHA_PRODUCT_CHAIN" for row in alpha_rows)
    balpha_ok = no_claim(balpha_rows) and any(row["chain_id"] == "BAP1051_2_best_current_product" and row["product_bound_1sigma_yr_inv"] == "2.1e-18" for row in balpha_rows)
    readiness_ok = no_claim(readiness_rows) and any(row["projection_id"] == "BAPR1051_0_clock" and row["current_status"] == "SOURCE_BACKED_PRODUCT_BOUND_AVAILABLE" for row in readiness_rows)
    mts_schema_ok = all(column in mts_rows[0] for column in MTS_REQUIRED_COLUMNS) if mts_rows else False
    mts_nonclaim_ok = no_claim(mts_rows) and any("MISSING" in row["alpha_predicted"] for row in mts_rows)
    runner_ok = runner_status.get("claim_allowed") is False and runner_status.get("valid_mts_rows") == 0
    gates_ok = all(row["claim_allowed"] == "false" for row in claim_rows)
    next_ok = bool(next_rows) and "1052" in next_rows[0]["next_target"]
    generated_ok = all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in generated_paths)
    formalization_changed = 0
    if FORMALIZATION.exists():
        formalization_changed = sum(
            1
            for path in FORMALIZATION.rglob("*")
            if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED
        )
    checks = [
        ("V1051_SUMMARY", True, "1051 no-mixed morphism or first b_alpha prior chain validation summary"),
        ("V1051_1_sources_exist_and_needles", source_ok, "every cited source path exists and every source needle was found"),
        ("V1051_2_no_mixed_lemma_blocked", lemma_ok, "no-mixed lemma has exact conditional piece but current claim remains blocked"),
        ("V1051_3_invariant_obstruction_recorded", invariant_ok, "surviving hidden scalar obstruction is recorded"),
        ("V1051_4_alpha_owner_audited", alpha_ok, "alpha owner/radiative closure audit retains b_alpha product chain"),
        ("V1051_5_balpha_product_chain_nonclaim", balpha_ok, "source-backed b_alpha*tau_clock product rows are staged as nonclaim"),
        ("V1051_6_projection_readiness_nonclaim", readiness_ok, "clock/WEP/R10/PPN projection readiness rows remain nonclaim"),
        ("V1051_7_mts_template_schema_nonclaim", mts_schema_ok and mts_nonclaim_ok, "MTS R10 template has runner schema and no claim-valid rows"),
        ("V1051_8_runner_smoke_refuses_claim", runner_ok, "existing R10 runner refuses the 1051 placeholder rows"),
        ("V1051_9_claim_gates_blocked", gates_ok, "claim gates keep theorem-zero, standalone b_alpha, and transfer claims blocked"),
        ("V1051_10_next_target_written", next_ok, "next target row is present"),
        ("V1051_11_generated_files_in_post_checkpoint", generated_ok, "all generated files are under post-checkpoint-work"),
        ("V1051_12_formalization_untouched", formalization_changed == 0, f"formalization-workbench modified-file count since script start is {formalization_changed}"),
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
        "# 1051 Y5 R10 no mixed hidden visible morphism lemma or first prior width chain",
        "",
        "**Progress:** the no-mixed morphism route is now sharpened. It is exact if the hidden invariant algebra is trivial, but a surviving hidden scalar immediately builds a visible coefficient morphism.",
        "",
        "**Current verdict:** no theorem-zero claim. The scalar-invariant obstruction survives, and alpha owner/radiative/readout closure is still unsigned.",
        "",
        "**Fallback:** the first useful numerical chain is now explicit: clock data provide source-backed nonclaim bounds on `b_alpha*tau_clock_time`, with the best imported row `2.1e-18 yr^-1` at 1 sigma. This is not a standalone `b_alpha` or R10/WEP claim.",
        "",
    ]
    for title, rows, columns in sections:
        lines.extend([f"## {title}", md_table(rows, columns), ""])
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    lemma_rows = no_mixed_morphism_rows()
    invariant_rows = invariant_obstruction_rows()
    alpha_rows = alpha_owner_rows()
    balpha_rows = balpha_prior_chain_rows()
    readiness_rows = projection_readiness_rows()
    mts_rows = mts_template_rows()
    write_csv(MTS_TEMPLATE, mts_rows, MTS_REQUIRED_COLUMNS)
    runner_result = run_runner(MTS_TEMPLATE, BOUND_CANDIDATE, RUN_DIR)
    runner_status = runner_result["status"]
    runner_rows = [
        {
            "smoke_id": "SMOKE1051_0_R10_runner_refusal",
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
        (OUT / "P8_Y5_R10_1051_SOURCE_REGISTER.csv", source_rows),
        (OUT / "P8_Y5_R10_1051_NO_MIXED_MORPHISM_LEMMA_ATTEMPT.csv", lemma_rows),
        (OUT / "P8_Y5_R10_1051_INVARIANT_SCALAR_OBSTRUCTION_AUDIT.csv", invariant_rows),
        (OUT / "P8_Y5_R10_1051_ALPHA_OWNER_RADIATIVE_CLOSURE_AUDIT.csv", alpha_rows),
        (OUT / "P8_Y5_R10_1051_B_ALPHA_CLOCK_PRODUCT_PRIOR_CHAIN.csv", balpha_rows),
        (OUT / "P8_Y5_R10_1051_B_ALPHA_PROJECTION_READINESS.csv", readiness_rows),
        (OUT / "P8_Y5_R10_1051_RUNNER_SMOKE_STATUS.csv", runner_rows),
        (OUT / "P8_Y5_R10_1051_PLACEHOLDER_REFUSAL_RUNNER.csv", refusal_rows),
        (OUT / "P8_Y5_R10_1051_CLAIM_GATES.csv", claim_rows),
        (OUT / "P8_Y5_R10_1051_DECISION_LEDGER.csv", decisions),
        (OUT / "P8_Y5_R10_1051_NEXT_TARGET.csv", next_rows),
    ]
    for path, rows in generated_map:
        write_csv(path, rows)
    validation = validation_rows(
        source_rows,
        lemma_rows,
        invariant_rows,
        alpha_rows,
        balpha_rows,
        readiness_rows,
        mts_rows,
        runner_status,
        claim_rows,
        next_rows,
        [path for path, _ in generated_map] + [MTS_TEMPLATE, DOC],
    )
    validation_path = OUT / "P8_Y5_BRR545_1051_VALIDATION.csv"
    write_csv(validation_path, validation)
    write_doc(
        [
            ("Source register", source_rows, ["source_id", "source_path", "exists", "needle_found", "role"]),
            ("No-mixed morphism lemma attempt", lemma_rows, ["lemma_id", "claim_piece", "mathematical_form", "proof_status", "obstruction", "if_false", "valid_for_claim"]),
            ("Invariant scalar obstruction audit", invariant_rows, ["obstruction_id", "candidate_invariant", "mixed_coefficient", "visible_operator", "status", "needed_to_close", "valid_for_claim"]),
            ("Alpha owner radiative closure audit", alpha_rows, ["audit_id", "object", "current_evidence", "status", "missing_for_balpha_zero", "fallback", "valid_for_claim"]),
            ("b_alpha clock-product prior chain", balpha_rows, ["chain_id", "clock_pair", "delta_K_alpha", "product_bound_1sigma_yr_inv", "product_bound_2sigma_yr_inv", "formula", "standalone_balpha_ready", "valid_for_claim"]),
            ("b_alpha projection readiness", readiness_rows, ["projection_id", "arena", "current_status", "usable_now", "missing_for_claim", "claim_allowed", "valid_for_claim"]),
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
        raise SystemExit(f"1051 validation failed: {failed}")
    print(f"Wrote {DOC}")
    print(f"Wrote {validation_path}")
    print(f"Runner claim_allowed={runner_status.get('claim_allowed')} valid_mts_rows={runner_status.get('valid_mts_rows')}")


if __name__ == "__main__":
    main()
