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
DOC = ROOT / "1058-Y5-R10-visible-operator-domain-exhaustion-or-alpha-counterterm-prior.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1058-visible-operator-domain-exhaustion-alpha-counterterm-smoke" / "results"
MTS_TEMPLATE = OUT / "R10_alpha_lambda_curve_MTS_1058_ALPHA_COUNTERTERM_TEMPLATE_NONCLAIM.csv"
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
        ("SRC1058_0_1057_next", "source-intake/mts_residuals/P8_Y5_R10_1057_NEXT_TARGET.csv", "1058-Y5-R10-visible-operator-domain-exhaustion-or-alpha-counterterm-prior.md", "1057 handoff."),
        ("SRC1058_1_1057_theorem", "source-intake/mts_residuals/P8_Y5_R10_1057_UNIQUE_MAXWELL_SUBBLOCK_THEOREM_ATTEMPT.csv", "UMS1057_5_verdict", "no-independent-F2 theorem status."),
        ("SRC1058_2_1057_operator", "source-intake/mts_residuals/P8_Y5_R10_1057_OPERATOR_DOMAIN_AUDIT.csv", "OD1057_3_contract_adoption", "operator-domain audit."),
        ("SRC1058_3_1057_counterterm", "source-intake/mts_residuals/P8_Y5_R10_1057_F2_COUNTERTERM_LEDGER.csv", "CT1057_0_constant_lambda", "F2 counterterm ledger."),
        ("SRC1058_4_1057_alpha", "source-intake/mts_residuals/P8_Y5_R10_1057_ALPHA_CONSEQUENCE_LEDGER.csv", "AC1057_1_current", "alpha consequence ledger."),
        ("SRC1058_5_1049_operator", "source-intake/mts_residuals/P8_Y5_R10_1049_OPERATOR_CLASSIFICATION_RULE_ATTEMPT.csv", "OCR1049_5_verdict", "operator-classification rule attempt."),
        ("SRC1058_6_1050_product", "source-intake/mts_residuals/P8_Y5_R10_1050_PRODUCT_FUNCTOR_THEOREM_ATTEMPT.csv", "PFT1050_5_verdict", "product functor theorem status."),
        ("SRC1058_7_980_no_marker", "source-intake/mts_residuals/P8_Y5_R10_980_NO_MARKER_FUNCTOR_THEOREM_ATTEMPT.csv", "NMF980_2_scalar_obstruction_lemma", "hidden scalar obstruction."),
        ("SRC1058_8_1051_alpha", "source-intake/mts_residuals/P8_Y5_R10_1051_ALPHA_OWNER_RADIATIVE_CLOSURE_AUDIT.csv", "AOR1051_3_verdict", "alpha owner/radiative closure status."),
        ("SRC1058_9_1052_clock", "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv", "ACB1052_2", "best clock alpha product bound."),
        ("SRC1058_10_1052_WEP", "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv", "AWP1052_0_alpha_Coulomb", "WEP alpha product target."),
        ("SRC1058_11_1053_R10", "source-intake/mts_residuals/P8_Y5_R10_1053_CROSS_ARENA_ALPHA_CHAIN.csv", "CAC1053_3_R10", "R10 finite alpha branch status."),
        ("SRC1058_12_1054_prior", "source-intake/mts_residuals/P8_Y5_R10_1054_NUMERIC_PRIOR_WIDTH_LEDGER.csv", "NPW1054_0_alpha_WEP_product", "numeric product-width ledger."),
        ("SRC1058_13_R10_bound_candidate", "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv", "R10_VECTOR_2020_REVIEW_0000", "R10 review-candidate bound curve for smoke only."),
        ("SRC1058_14_R10_runner", "scripts/R10_alpha_lambda_bound_prediction_runner.py", "MTS_REQUIRED_COLUMNS", "existing R10 runner and schema."),
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


def exhaustion_attempt_rows() -> list[dict[str, str]]:
    return [
        {
            "attempt_id": "VOE1058_0_target",
            "claim_piece": "visible operator-domain exhaustion",
            "mathematical_form": "Allowed[S_vis] = Image(ParentGenerate[q_loc, F_parent, theta_rep, topological levels]) and no additional local visible counterterm algebra is admitted",
            "current_status": "TARGET_SHARP",
            "proof_or_blocker": "would ban lambda_A F_Q^2, f(Xhat)F_Q^2, m_A(Xhat), and hidden readout coefficients",
            "if_signed": "visible constants become quotient/representation data; b_alpha route can close",
            "if_unsigned": "alpha counterterm prior branch remains mandatory",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "VOE1058_1_declared_parent_domain",
            "claim_piece": "operator generation by declared parent fields",
            "mathematical_form": "Op_allowed subset Alg[q(Phi), Dq(Phi), F_parent, theta_rep, topological classes]",
            "current_status": "CONTRACT_EXACT_IF_ADOPTED_NOT_DERIVED",
            "proof_or_blocker": "this is an action-domain discipline rule, not yet a derivation from MTS primitives",
            "if_signed": "post-hoc F_Q^2/mass/clock coefficient slots are forbidden",
            "if_unsigned": "any neutral scalar can multiply visible operators",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "VOE1058_2_product_functor",
            "claim_piece": "visible-hidden product functor",
            "mathematical_form": "C_parent -> C_vis x C_hid; S_vis factors through C_vis=q_loc(Phi), theta_rep",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_DERIVED",
            "proof_or_blocker": "parent product category and projection functors are not constructed",
            "if_signed": "f(Xhat)F_Q^2 and other hidden coefficient maps vanish",
            "if_unsigned": "Xhat can feed visible coefficients through legal scalar functions",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "VOE1058_3_no_hidden_visible_hom",
            "claim_piece": "no hidden-to-visible coefficient morphisms",
            "mathematical_form": "Hom(C_hid,Coeff(O_vis)) = Const or absent",
            "current_status": "BLOCKED_BY_SCALAR_OBSTRUCTION",
            "proof_or_blocker": "one surviving invariant scalar I_hid permits c=c0+epsilon I_hid unless target action forbids it",
            "if_signed": "no f(I_hid)F_Q^2 or hidden mass/readout coefficients",
            "if_unsigned": "finite b_alpha and constant-sector priors remain live",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "VOE1058_4_radiative_exhaustion",
            "claim_piece": "effective/readout action remains exhausted by parent generators",
            "mathematical_form": "S_vis^eff and readout maps remain in Image(ParentGenerate) at all relevant reduction scales",
            "current_status": "UNSIGNED",
            "proof_or_blocker": "loops/thresholds/readout reductions can regenerate F_Q^2 counterterms",
            "if_signed": "tree-level exhaustion is stable",
            "if_unsigned": "radiative alpha counterterm prior remains mandatory",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "VOE1058_5_verdict",
            "claim_piece": "visible operator-domain exhaustion theorem",
            "mathematical_form": "VOE1058_1 through VOE1058_4 signed => no independent alpha counterterm",
            "current_status": "REJECT_CURRENT_CLAIM_RETAIN_COUNTERTERM_PRIOR",
            "proof_or_blocker": "current corpus has conditional contracts and explicit counterexamples, not a derived exhaustion rule",
            "if_signed": "b_alpha=0 route reopens",
            "if_unsigned": "formalize retained alpha counterterm prior branch",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def operator_algebra_rows() -> list[dict[str, str]]:
    return [
        {
            "operator_id": "OA1058_0_parent_generated",
            "operator_class": "parent-generated visible kinetic terms",
            "example": "C_P <F_Q T_Q,F_Q T_Q>_P",
            "status": "ALLOWED_CONDITIONAL",
            "claim_effect": "may own one Maxwell coefficient if parent projection/norm is derived",
            "retained_if_unsigned": "yes",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "operator_id": "OA1058_1_constant_counterterm",
            "operator_class": "constant visible counterterm",
            "example": "lambda_A F_Q^2",
            "status": "ALLOWED_BY_ORDINARY_SYMMETRIES",
            "claim_effect": "blocks alpha ownership as a derived statement",
            "retained_if_unsigned": "yes",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "operator_id": "OA1058_2_hidden_counterterm",
            "operator_class": "hidden scalar visible counterterm",
            "example": "f(I_hid) F_Q^2",
            "status": "ALLOWED_IF_HIDDEN_INVARIANT_SURVIVES",
            "claim_effect": "opens vertical alpha drift and clock/WEP pressure",
            "retained_if_unsigned": "yes",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "operator_id": "OA1058_3_radiative_counterterm",
            "operator_class": "effective/radiative threshold",
            "example": "delta lambda_A(mu,Xhat) F_Q^2",
            "status": "RETAINED_UNTIL_RADIOUT_CLOSURE",
            "claim_effect": "tree-level ban is insufficient for claim-grade alpha silence",
            "retained_if_unsigned": "yes",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "operator_id": "OA1058_4_forbidden_only_if_exhaustion",
            "operator_class": "non-parent visible kinetic/coupling slots",
            "example": "any O_vis with coefficient outside Image(ParentGenerate)",
            "status": "FORBIDDEN_ONLY_BY_EXHAUSTION_AXIOM_OR_THEOREM",
            "claim_effect": "would close alpha/mass/clock slots if derived",
            "retained_if_unsigned": "yes",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def alpha_counterterm_prior_rows() -> list[dict[str, str]]:
    return [
        {
            "prior_id": "ACP1058_0_ZA_decomposition",
            "quantity": "Z_A := g_EM^{-2}",
            "definition": "Z_A = C_P N_Q + lambda_A0 + lambda_Ahid(I_hid) + delta_lambda_A_rad + retained readout terms",
            "current_status": "SYMBOLIC_COUNTERTERM_BRANCH",
            "observable_link": "alpha_EM = 1/(4*pi*hbar*c*Z_A) in the selected readout convention",
            "source_or_bound": "no standalone numeric Z_A counterterm source",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "prior_id": "ACP1058_1_balpha_counterterm",
            "quantity": "b_alpha_counterterm",
            "definition": "b_alpha = -Lie_v ln Z_A - Lie_v ln(hbar*c readout)",
            "current_status": "PRODUCT_ONLY",
            "observable_link": "clock frequency ratios bound b_alpha*tau_clock_time",
            "source_or_bound": "best current product bound 2.1e-18 yr^-1",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "prior_id": "ACP1058_2_WEP_product",
            "quantity": "C_alpha_WEP := beta_source_alpha*b_alpha*tau_WEP",
            "definition": "eta_AB_alpha = DeltaQ_alpha_AB*C_alpha_WEP under the 1052 smoke convention",
            "current_status": "PRODUCT_WIDTH_TARGET_ONLY",
            "observable_link": "MICROSCOPE WEP alpha/Coulomb channel",
            "source_or_bound": "required |C_alpha_WEP| <= 4.797780522732e-05",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "prior_id": "ACP1058_3_R10_product",
            "quantity": "C_alpha_R10(lambda)",
            "definition": "C_alpha_R10(lambda)=K_X^R10(lambda)*beta_s(lambda)*beta_t(lambda)+epsilon_tail(lambda)",
            "current_status": "UNSCOREABLE_PLACEHOLDER",
            "observable_link": "R10 alpha(lambda) comparison",
            "source_or_bound": "lambda_X, K_X/Z_X, tau_R10, beta_s, beta_t, and promoted bound curve missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "prior_id": "ACP1058_4_counterterm_policy",
            "quantity": "alpha counterterm prior branch",
            "definition": "retain alpha counterterm products until exhaustion/no-hidden-visible/radiative/readout closure is derived",
            "current_status": "RETAINED_NONCLAIM_BRANCH",
            "observable_link": "clock; WEP; R10; future EM/readout tests",
            "source_or_bound": "product gates only; no standalone public claim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def cross_arena_rows() -> list[dict[str, str]]:
    return [
        {
            "link_id": "CAL1058_0_clock",
            "arena": "clock",
            "counterterm_product": "b_alpha*tau_clock_time",
            "available_bound": "2.1e-18 yr^-1 best current product row",
            "missing_for_score": "tau_clock_time parent derivation and Xhat/readout normalization",
            "claim_status": "PRODUCT_BOUND_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "link_id": "CAL1058_1_WEP",
            "arena": "MICROSCOPE_WEP",
            "counterterm_product": "beta_source_alpha*b_alpha*tau_WEP",
            "available_bound": "4.797780522732e-05 normalized alpha/Coulomb product target",
            "missing_for_score": "beta_source_alpha owner, tau_WEP, full material convention",
            "claim_status": "PRODUCT_TARGET_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "link_id": "CAL1058_2_R10",
            "arena": "R10_short_range",
            "counterterm_product": "K_X^R10 beta_s beta_t + epsilon_tail",
            "available_bound": "review-candidate alpha(lambda) curve only, valid_for_claim=false",
            "missing_for_score": "lambda_X; Z_X; K_X; tau_R10; beta_s; beta_t; promoted curve",
            "claim_status": "UNSCOREABLE_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "link_id": "CAL1058_3_cross_arena_policy",
            "arena": "cross_arena",
            "counterterm_product": "shared alpha counterterm branch",
            "available_bound": "mixed product constraints only",
            "missing_for_score": "single parent normalization linking clock, WEP, and R10 projections",
            "claim_status": "NO_TRANSFER_WITHOUT_PARENT_MAP",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def radiative_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "RCG1058_0_tree_level",
            "claim_piece": "tree-level visible operator exhaustion",
            "gate_pass": "false",
            "reason": "operator-domain rule is not derived",
            "if_missing": "constant/hidden alpha counterterms remain",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "RCG1058_1_loop_threshold",
            "claim_piece": "loop/threshold counterterms cannot regenerate F_Q^2",
            "gate_pass": "false",
            "reason": "radiative closure theorem is unsigned",
            "if_missing": "delta_lambda_A(mu,Xhat) remains retained",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "RCG1058_2_readout",
            "claim_piece": "clock/readout maps preserve alpha ownership",
            "gate_pass": "false",
            "reason": "readout descent is not parent-derived",
            "if_missing": "clock spectroscopy can see alpha pressure even if abstract gauge norm is fixed",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "RCG1058_3_policy",
            "claim_piece": "radiative/readout alpha silence",
            "gate_pass": "false",
            "reason": "all upstream closure gates must pass",
            "if_missing": "keep alpha counterterm prior branch",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def promotion_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "PG1058_0_exhaustion",
            "claim_piece": "visible operator-domain exhaustion is derived",
            "gate_pass": "false",
            "reason": "current evidence supports an exact contract, not a derived theorem",
            "promotion_requirement": "derive allowed visible operator algebra from MTS primitives",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "PG1058_1_alpha_counterterm_zero",
            "claim_piece": "alpha counterterm branch vanishes",
            "gate_pass": "false",
            "reason": "lambda_A, f(I_hid), and radiative/readout counterterms remain legal",
            "promotion_requirement": "exhaustion plus no-hidden-visible hom plus radiative/readout closure",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "PG1058_2_product_prior",
            "claim_piece": "standalone numeric alpha counterterm prior exists",
            "gate_pass": "false",
            "reason": "current numerical evidence is product-only, not standalone b_alpha or lambda_A",
            "promotion_requirement": "source tau maps and parent normalization in one convention",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "PG1058_3_WEP_R10",
            "claim_piece": "WEP/R10 alpha counterterm branch passes",
            "gate_pass": "false",
            "reason": "requires derived zero theorem or complete finite branch prediction",
            "promotion_requirement": "product prediction below bounds with source-backed projections",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1058_0_exhaustion_result",
            "decision": "visible operator-domain exhaustion is not derived in the current corpus",
            "because": "all available support is conditional; ordinary symmetries allow visible kinetic counterterms",
            "next_action": "treat exhaustion as a contract, not a claim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1058_1_counterterm_result",
            "decision": "alpha counterterm prior branch is now formalized",
            "because": "lambda_A, f(I_hid), and radiative/readout terms remain legal until exhaustion closes",
            "next_action": "source/fill product priors and projection maps rather than pretending zero",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1058_2_best_next",
            "decision": "move to alpha counterterm product-prior source pack",
            "because": "the derivation path is now blocked at operator-domain exhaustion, but empirical product gates are available",
            "next_action": "1059-Y5-R10-alpha-counterterm-product-prior-source-pack-and-cross-arena-gate.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1058_0_exhaustion",
            "claim": "visible operator-domain exhaustion is proved",
            "gate_pass": "false",
            "reason": "only conditional contracts exist",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1058_1_balpha_zero",
            "claim": "b_alpha=0",
            "gate_pass": "false",
            "reason": "alpha counterterm branch remains legal",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1058_2_beta_source_alpha_zero",
            "claim": "beta_source_alpha=0 via alpha owner",
            "gate_pass": "false",
            "reason": "alpha owner and matter/source clauses remain conditional",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1058_3_product_prior_claim",
            "claim": "standalone counterterm prior is numeric and score-ready",
            "gate_pass": "false",
            "reason": "only cross-arena product bounds/targets are available",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1058_4_WEP_R10",
            "claim": "WEP/R10 alpha branch passes",
            "gate_pass": "false",
            "reason": "requires derived zero theorem or complete sourced product predictions",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1059-Y5-R10-alpha-counterterm-product-prior-source-pack-and-cross-arena-gate.md",
            "objective": "turn the retained alpha counterterm branch into a source-backed product-prior pack for clock, WEP, and R10, while keeping standalone b_alpha/beta_source_alpha claims blocked unless tau/source projections are derived",
            "include": "clock product import, WEP product target, R10 finite branch schema, tau/source projection debts, product-only score rules, no-transfer policy",
            "exclude": "standalone b_alpha claim, unit-rescaling, cancellation, tau unity shortcut, public local-GR/R10/WEP/clock claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def mts_template_rows() -> list[dict[str, str]]:
    row = {
        "model_id": "MTS_source_normalized_Newton_branch",
        "branch_id": "alpha_counterterm_prior_template",
        "curve_id": "MTS_1058_alpha_counterterm_prior_nonclaim",
        "lambda_value": "MISSING_ALPHA_COUNTERTERM_PROJECTION_OR_LAMBDA_X",
        "lambda_units": "m",
        "alpha_predicted": "MISSING_PRODUCT_PRIOR_OR_FINITE_ALPHA_BRANCH",
        "alpha_bound": "MISSING_PROMOTED_BOUND",
        "alpha_bound_source": str(BOUND_CANDIDATE),
        "force_law_form": "operator exhaustion rejected currently; retained alpha branch uses product constraints b_alpha*tau_clock, beta_source_alpha*b_alpha*tau_WEP, and K_X beta_s beta_t for R10",
        "derivation_status": "template_invalid_counterterm_branch_product_only",
        "formula_reference": "P8_Y5_R10_1058_ALPHA_COUNTERTERM_PRIOR_BRANCH.csv",
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_1058_ALPHA_COUNTERTERM_PRIOR_BRANCH.csv",
        "assumptions": "nonclaim placeholder; no standalone b_alpha; no rescaling; no cancellation",
        "valid_for_claim": "false",
        "notes": "Runner must refuse this row until product predictions and claim-valid bound data are sourced.",
    }
    return [{column: row[column] for column in MTS_REQUIRED_COLUMNS}]


def runner_smoke_rows(status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "smoke_id": "SMOKE1058_0_R10_runner_refusal",
            "valid_mts_rows": str(status.get("valid_mts_rows", "")),
            "valid_bound_rows": str(status.get("valid_bound_rows", "")),
            "comparison_rows": str(status.get("comparison_rows", "")),
            "R10_pass_for_claim": str(status.get("R10_pass_for_claim", "")).lower(),
            "claim_allowed": str(status.get("claim_allowed", "")).lower(),
            "expected_result": "reject alpha-counterterm placeholders until product predictions are sourced",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def refusal_rows(status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "refusal_id": "REF1058_0_exhaustion",
            "object": "visible operator-domain exhaustion",
            "current_status": "REJECT_CURRENT_CLAIM_RETAIN_COUNTERTERM_PRIOR",
            "refusal_status": "blocked_for_claim",
            "failure_reasons": "declared parent domain/product functor/no-hidden-hom/radiative closure are not parent-derived",
            "score_eligible": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "refusal_id": "REF1058_1_counterterm_prior",
            "object": "standalone alpha counterterm prior",
            "current_status": "PRODUCT_ONLY_NONCLAIM",
            "refusal_status": "blocked_for_standalone_claim",
            "failure_reasons": "clock/WEP/R10 rows are product constraints without tau/source projection ownership",
            "score_eligible": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "refusal_id": "REF1058_2_R10_runner",
            "object": "R10 alpha-counterterm smoke row",
            "current_status": "runner_refusal_expected",
            "refusal_status": "blocked",
            "failure_reasons": f"valid_mts_rows={status.get('valid_mts_rows')}; valid_bound_rows={status.get('valid_bound_rows')}",
            "score_eligible": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
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
    exhaustion_rows: list[dict[str, str]],
    operator_rows: list[dict[str, str]],
    prior_rows: list[dict[str, str]],
    cross_rows: list[dict[str, str]],
    radiative_rows: list[dict[str, str]],
    promotion_rows: list[dict[str, str]],
    template_rows: list[dict[str, str]],
    runner_status: dict[str, Any],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()})

    source_ok = all(flag(row.get("exists", "")) and flag(row.get("needle_found", "")) for row in source_rows)
    add("V1058_1_sources_exist_and_needles", source_ok, "every cited source path exists and every source needle was found")
    exhaustion_rejected = any(row.get("attempt_id") == "VOE1058_5_verdict" and row.get("current_status") == "REJECT_CURRENT_CLAIM_RETAIN_COUNTERTERM_PRIOR" for row in exhaustion_rows)
    add("V1058_2_exhaustion_rejected_current_claim", exhaustion_rejected, "operator-domain exhaustion remains conditional and not promoted")
    counterterm_allowed = any(row.get("operator_id") == "OA1058_1_constant_counterterm" and row.get("status") == "ALLOWED_BY_ORDINARY_SYMMETRIES" for row in operator_rows)
    add("V1058_3_counterterm_operator_retained", counterterm_allowed, "constant alpha counterterm remains allowed unless exhaustion is derived")
    prior_branch = any(row.get("prior_id") == "ACP1058_4_counterterm_policy" and row.get("current_status") == "RETAINED_NONCLAIM_BRANCH" for row in prior_rows)
    add("V1058_4_alpha_counterterm_prior_formalized", prior_branch, "retained alpha counterterm prior branch is formalized")
    cross_nonclaim = cross_rows and all(row.get("valid_for_claim") == "false" for row in cross_rows)
    add("V1058_5_cross_arena_links_nonclaim", cross_nonclaim, "clock/WEP/R10 cross-arena links remain product-only nonclaim")
    radiative_blocked = radiative_rows and all(row.get("gate_pass") == "false" for row in radiative_rows)
    add("V1058_6_radiative_gates_blocked", radiative_blocked, "radiative/readout closure remains blocked")
    promotion_blocked = promotion_rows and all(row.get("gate_pass") == "false" and row.get("claim_allowed") == "false" for row in promotion_rows)
    add("V1058_7_promotion_gates_blocked", promotion_blocked, "promotion gates remain blocked")
    template_schema = set(MTS_REQUIRED_COLUMNS).issubset(set(template_rows[0].keys())) if template_rows else False
    template_nonclaim = template_schema and all(row.get("valid_for_claim") == "false" for row in template_rows)
    add("V1058_8_mts_template_schema_nonclaim", template_nonclaim, "MTS template has runner schema and no claim-valid rows")
    runner_refused = runner_status.get("valid_mts_rows") == 0 and runner_status.get("claim_allowed") is False
    add("V1058_9_runner_smoke_refuses_claim", runner_refused, "existing R10 runner refuses the 1058 placeholder rows")
    claims_blocked = claim_rows and all(row.get("gate_pass") == "false" and row.get("claim_allowed") == "false" for row in claim_rows)
    add("V1058_10_claim_gates_blocked", claims_blocked, "all exhaustion/counterterm/WEP/R10 claim gates remain blocked")
    next_ok = bool(next_rows) and next_rows[0].get("next_target", "").startswith("1059-Y5-R10-alpha-counterterm")
    add("V1058_11_next_target_written", next_ok, "next target row is present")
    generated_inside = all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in outputs.values())
    add("V1058_12_generated_files_in_post_checkpoint", generated_inside, "all generated files are under post-checkpoint-work")
    formalization_count = count_formalization_modified_since_start()
    add("V1058_13_formalization_untouched", formalization_count == 0, f"formalization-workbench modified-file count since script start is {formalization_count}")

    summary_pass = all(row["result"] == "pass" for row in checks)
    checks.insert(0, {"check_id": "V1058_SUMMARY", "result": "pass" if summary_pass else "fail", "detail": "1058 visible operator-domain exhaustion or alpha counterterm prior validation summary", "generated_utc": stamp()})
    return checks


def write_doc(
    source_rows: list[dict[str, str]],
    exhaustion_rows: list[dict[str, str]],
    operator_rows: list[dict[str, str]],
    prior_rows: list[dict[str, str]],
    cross_rows: list[dict[str, str]],
    radiative_rows: list[dict[str, str]],
    promotion_rows: list[dict[str, str]],
    decisions: list[dict[str, str]],
    template_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
    refusal_rows_: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1058 Y5 R10 visible operator domain exhaustion or alpha counterterm prior",
            "",
            "**Progress:** the parent visible-operator-domain exhaustion theorem is now stated explicitly. If it were derived, it would ban non-parent `F_Q^2`, hidden `f(Xhat)F_Q^2`, and radiative/readout alpha counterterms.",
            "",
            "**Current verdict:** exhaustion is not derived in the current corpus. It remains a clean contract, not a theorem, so the alpha counterterm branch must be retained honestly.",
            "",
            "**Fallback now formalized:** `Z_A=g_EM^{-2}` is treated as a parent piece plus retained counterterms; only product constraints are currently source-backed, so no standalone `b_alpha` or WEP/R10 pass is claimed.",
            "",
            "## Source register",
            md_table(source_rows, ["source_id", "source_path", "exists", "needle_found", "role"]),
            "",
            "## Visible operator-domain exhaustion attempt",
            md_table(exhaustion_rows, ["attempt_id", "claim_piece", "mathematical_form", "current_status", "proof_or_blocker", "if_signed", "if_unsigned", "valid_for_claim"]),
            "",
            "## Allowed operator algebra audit",
            md_table(operator_rows, ["operator_id", "operator_class", "example", "status", "claim_effect", "retained_if_unsigned", "valid_for_claim"]),
            "",
            "## Alpha counterterm prior branch",
            md_table(prior_rows, ["prior_id", "quantity", "definition", "current_status", "observable_link", "source_or_bound", "valid_for_claim"]),
            "",
            "## Cross-arena alpha counterterm links",
            md_table(cross_rows, ["link_id", "arena", "counterterm_product", "available_bound", "missing_for_score", "claim_status", "valid_for_claim"]),
            "",
            "## Radiative/readout closure gate",
            md_table(radiative_rows, ["gate_id", "claim_piece", "gate_pass", "reason", "if_missing", "valid_for_claim"]),
            "",
            "## Promotion gates",
            md_table(promotion_rows, ["gate_id", "claim_piece", "gate_pass", "reason", "promotion_requirement", "claim_allowed"]),
            "",
            "## Decision ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
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
    exhaustion_rows = exhaustion_attempt_rows()
    operator_rows = operator_algebra_rows()
    prior_rows = alpha_counterterm_prior_rows()
    cross_rows = cross_arena_rows()
    radiative_rows = radiative_gate_rows()
    promotion_rows = promotion_gate_rows()
    decisions = decision_rows()
    claim_rows = claim_gate_rows()
    next_rows = next_target_rows()
    template_rows = mts_template_rows()

    outputs: dict[str, Path] = {
        "source_register": OUT / "P8_Y5_R10_1058_SOURCE_REGISTER.csv",
        "exhaustion": OUT / "P8_Y5_R10_1058_VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_ATTEMPT.csv",
        "operator": OUT / "P8_Y5_R10_1058_ALLOWED_OPERATOR_ALGEBRA_AUDIT.csv",
        "prior": OUT / "P8_Y5_R10_1058_ALPHA_COUNTERTERM_PRIOR_BRANCH.csv",
        "cross": OUT / "P8_Y5_R10_1058_CROSS_ARENA_ALPHA_COUNTERTERM_LINKS.csv",
        "radiative": OUT / "P8_Y5_R10_1058_RADIATIVE_READOUT_CLOSURE_GATE.csv",
        "promotion": OUT / "P8_Y5_R10_1058_PROMOTION_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1058_DECISION_LEDGER.csv",
        "claim_gates": OUT / "P8_Y5_R10_1058_CLAIM_GATES.csv",
        "next_target": OUT / "P8_Y5_R10_1058_NEXT_TARGET.csv",
        "mts_template": MTS_TEMPLATE,
        "runner_smoke": OUT / "P8_Y5_R10_1058_RUNNER_SMOKE_STATUS.csv",
        "placeholder_refusal": OUT / "P8_Y5_R10_1058_PLACEHOLDER_REFUSAL_RUNNER.csv",
        "validation": OUT / "P8_Y5_BRR545_1058_VALIDATION.csv",
        "doc": DOC,
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["exhaustion"], exhaustion_rows)
    write_csv(outputs["operator"], operator_rows)
    write_csv(outputs["prior"], prior_rows)
    write_csv(outputs["cross"], cross_rows)
    write_csv(outputs["radiative"], radiative_rows)
    write_csv(outputs["promotion"], promotion_rows)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["claim_gates"], claim_rows)
    write_csv(outputs["next_target"], next_rows)
    write_csv(outputs["mts_template"], template_rows, MTS_REQUIRED_COLUMNS)

    runner_result = run_runner(MTS_TEMPLATE, BOUND_CANDIDATE, RUN_DIR)
    runner_status = runner_result["status"]
    smoke_rows = runner_smoke_rows(runner_status)
    refusal_rows_ = refusal_rows(runner_status)
    write_csv(outputs["runner_smoke"], smoke_rows)
    write_csv(outputs["placeholder_refusal"], refusal_rows_)

    validation_rows = validate_outputs(
        outputs,
        source_rows,
        exhaustion_rows,
        operator_rows,
        prior_rows,
        cross_rows,
        radiative_rows,
        promotion_rows,
        template_rows,
        runner_status,
        claim_rows,
        next_rows,
    )
    write_csv(outputs["validation"], validation_rows)
    write_doc(
        source_rows,
        exhaustion_rows,
        operator_rows,
        prior_rows,
        cross_rows,
        radiative_rows,
        promotion_rows,
        decisions,
        template_rows,
        smoke_rows,
        refusal_rows_,
        claim_rows,
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
