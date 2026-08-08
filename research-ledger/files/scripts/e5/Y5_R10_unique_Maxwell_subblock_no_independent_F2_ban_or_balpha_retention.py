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
DOC = ROOT / "1057-Y5-R10-unique-Maxwell-subblock-no-independent-F2-ban-or-balpha-retention.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1057-unique-Maxwell-subblock-no-independent-F2-smoke" / "results"
MTS_TEMPLATE = OUT / "R10_alpha_lambda_curve_MTS_1057_UNIQUE_MAXWELL_SUBBLOCK_TEMPLATE_NONCLAIM.csv"
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
        ("SRC1057_0_1056_next", "source-intake/mts_residuals/P8_Y5_R10_1056_NEXT_TARGET.csv", "1057-Y5-R10-unique-Maxwell-subblock-no-independent-F2-ban-or-balpha-retention.md", "1056 handoff."),
        ("SRC1057_1_1056_norm", "source-intake/mts_residuals/P8_Y5_R10_1056_VERTICAL_GENERATOR_NORM_DERIVATION_AUDIT.csv", "VNA1056_2_curvature_subblock", "curvature subblock failure."),
        ("SRC1057_2_1056_rescale", "source-intake/mts_residuals/P8_Y5_R10_1056_RESCALING_DEGENERACY_LEDGER.csv", "RSC1056_0_independent_F2", "independent F2 counterexample."),
        ("SRC1057_3_1049_operator", "source-intake/mts_residuals/P8_Y5_R10_1049_OPERATOR_CLASSIFICATION_RULE_ATTEMPT.csv", "OCR1049_5_verdict", "operator-classification rule attempt."),
        ("SRC1057_4_1049_symmetry", "source-intake/mts_residuals/P8_Y5_R10_1049_SYMMETRY_BAN_THEOREM_ATTEMPT.csv", "SBT1049_1_gauge_invariance", "gauge invariance limit."),
        ("SRC1057_5_1050_product", "source-intake/mts_residuals/P8_Y5_R10_1050_PRODUCT_FUNCTOR_THEOREM_ATTEMPT.csv", "PFT1050_3_radiative_readout_closure", "product functor and radiative closure."),
        ("SRC1057_6_1051_alpha", "source-intake/mts_residuals/P8_Y5_R10_1051_ALPHA_OWNER_RADIATIVE_CLOSURE_AUDIT.csv", "AOR1051_3_verdict", "alpha owner/radiative closure blocker."),
        ("SRC1057_7_642_maxwell", "source-intake/mts_residuals/P8_Y5_R10_642_MAXWELL_DESCENT_ATTEMPT.csv", "MD642_4_alpha_constant", "Maxwell alpha constant blocker."),
        ("SRC1057_8_1055_contract", "source-intake/mts_residuals/P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv", "PAC1055_1_EM_owner", "parent EM owner contract."),
        ("SRC1057_9_980_no_marker", "source-intake/mts_residuals/P8_Y5_R10_980_NO_MARKER_FUNCTOR_THEOREM_ATTEMPT.csv", "NMF980_2_scalar_obstruction_lemma", "hidden scalar obstruction."),
        ("SRC1057_10_1054_prior", "source-intake/mts_residuals/P8_Y5_R10_1054_NUMERIC_PRIOR_WIDTH_LEDGER.csv", "NPW1054_0_alpha_WEP_product", "finite alpha WEP product target."),
        ("SRC1057_11_1056_balpha", "source-intake/mts_residuals/P8_Y5_R10_1056_RETAINED_B_ALPHA_BRANCH_LEDGER.csv", "BAB1056_3_verdict", "retained b_alpha branch."),
        ("SRC1057_12_R10_bound_candidate", "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv", "R10_VECTOR_2020_REVIEW_0000", "R10 review-candidate bound curve for smoke only."),
        ("SRC1057_13_R10_runner", "scripts/R10_alpha_lambda_bound_prediction_runner.py", "MTS_REQUIRED_COLUMNS", "existing R10 runner and schema."),
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


def unique_subblock_rows() -> list[dict[str, str]]:
    return [
        {
            "proof_id": "UMS1057_0_target",
            "claim_piece": "unique observed Maxwell subblock",
            "mathematical_form": "S_EM[A_Q] = -C_P N_Q/4 int sqrt(-g_obs) F_Q^2, with no independent lambda_A F_Q^2",
            "derivation_status": "TARGET_SHARP",
            "proof_or_blocker": "would follow from parent curvature-norm exhaustion plus nonrescalable T_Q and quotient-fixed readout",
            "if_true": "g_EM^{-2}=C_P N_Q and Lie_v g_EM=0",
            "if_false": "b_alpha remains retained",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "proof_id": "UMS1057_1_parent_curvature_norm",
            "claim_piece": "Maxwell term inherited from parent curvature norm",
            "mathematical_form": "F_parent = F_Q T_Q + F_perp and <F_Q T_Q,F_Q T_Q>_P=N_Q F_Q^2",
            "derivation_status": "CONDITIONAL_SUBLEMMA",
            "proof_or_blocker": "requires parent A_Q projection and fixed fibre norm; not enough by itself",
            "if_true": "supplies one candidate coefficient C_P N_Q",
            "if_false": "Maxwell closure remains appended",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "proof_id": "UMS1057_2_no_independent_F2",
            "claim_piece": "independent lambda_A F_Q^2 is inadmissible",
            "mathematical_form": "Allowed[S_vis] contains no scalar-density operator DeltaS=-lambda_A/4 int F_Q^2 outside parent curvature norm",
            "derivation_status": "NOT_DERIVED_CURRENT_CORPUS",
            "proof_or_blocker": "diffeomorphism and U(1) gauge invariance allow F_Q^2; only an operator-domain exhaustion theorem can ban it",
            "if_true": "unique Maxwell subblock closes alpha owner up to readout/current clauses",
            "if_false": "g_EM^{-2}=C_P N_Q+lambda_A and alpha is not owned",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "proof_id": "UMS1057_3_no_hidden_coefficient",
            "claim_piece": "no hidden scalar coefficient f(Xhat)F_Q^2",
            "mathematical_form": "Hom(C_hid,Coeff(F_Q^2)) is absent or constant",
            "derivation_status": "POWERFUL_BUT_UNSIGNED",
            "proof_or_blocker": "980 scalar obstruction reopens f(I_hid)F_Q^2 unless hidden invariant algebra is trivial or target is forbidden",
            "if_true": "kills b_alpha drift source",
            "if_false": "finite b_alpha branch remains",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "proof_id": "UMS1057_4_radiative_counterterm",
            "claim_piece": "radiative/effective action does not regenerate F_Q^2 counterterm",
            "mathematical_form": "S_vis^eff remains generated by parent curvature norm and fixed representation data",
            "derivation_status": "UNSIGNED",
            "proof_or_blocker": "tree-level operator ban needs RG/readout closure; otherwise lambda_A can be an effective counterterm",
            "if_true": "protects alpha owner after reduction",
            "if_false": "b_alpha/b_clock priors remain live",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "proof_id": "UMS1057_5_verdict",
            "claim_piece": "no-independent-F2 theorem",
            "mathematical_form": "UMS1057_1..4 all signed => alpha_EM parent-owned by unique Maxwell subblock",
            "derivation_status": "FAIL_CURRENT_CLAIM_OPERATOR_DOMAIN_EXHAUSTION_REQUIRED",
            "proof_or_blocker": "current corpus has contracts and counterexamples, not a derived exhaustion theorem",
            "if_true": "b_alpha=0 route reopens",
            "if_false": "retain b_alpha product-prior branch",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def operator_domain_rows() -> list[dict[str, str]]:
    return [
        {
            "operator_id": "OD1057_0_diffeomorphism",
            "operator": "F_Q^2 scalar density",
            "ordinary_symmetry_result": "ALLOWED",
            "reason": "sqrt(-g_obs) F_Q^{mu nu}F^Q_{mu nu} is a covariant scalar density",
            "stronger_rule_needed": "parent operator-domain exhaustion",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "operator_id": "OD1057_1_U1_gauge",
            "operator": "lambda_A F_Q^2",
            "ordinary_symmetry_result": "ALLOWED",
            "reason": "U(1) gauge invariance allows scalar gauge kinetic coefficients",
            "stronger_rule_needed": "unique parent curvature norm or topological inheritance theorem",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "operator_id": "OD1057_2_product_functor",
            "operator": "f(Xhat)F_Q^2",
            "ordinary_symmetry_result": "FORBIDDEN_IF_PARENT_SIGNED",
            "reason": "visible-hidden product functor would remove Xhat from visible coefficients",
            "stronger_rule_needed": "parent-derived product category and radiative closure",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "operator_id": "OD1057_3_contract_adoption",
            "operator": "all non-parent visible kinetic counterterms",
            "ordinary_symmetry_result": "CONTRACT_EXACT_IF_ADOPTED_NOT_DERIVED",
            "reason": "declared parent domain can ban them, but adoption is not derivation",
            "stronger_rule_needed": "derive operator-domain exhaustion from MTS primitives",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def counterterm_rows() -> list[dict[str, str]]:
    return [
        {
            "counterterm_id": "CT1057_0_constant_lambda",
            "counterterm": "constant independent Maxwell kinetic term",
            "formula": "DeltaS=-lambda_A/4 int sqrt(-g_obs)F_Q^2",
            "status": "LEGAL_UNLESS_PARENT_DOMAIN_EXCLUDES",
            "effect": "alpha value is an independent visible coefficient even if parent norm exists",
            "repair_needed": "no-independent-F2 operator-domain theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "counterterm_id": "CT1057_1_hidden_scalar",
            "counterterm": "hidden scalar gauge kinetic function",
            "formula": "DeltaS=-1/4 int sqrt(-g_obs)f(I_hid)F_Q^2",
            "status": "LEGAL_IF_HIDDEN_INVARIANT_SURVIVES",
            "effect": "vertical alpha drift and WEP/clock alpha pressure reopen",
            "repair_needed": "no hidden-visible hom theorem or trivial hidden invariant algebra",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "counterterm_id": "CT1057_2_radiative",
            "counterterm": "radiatively generated F_Q^2 threshold",
            "formula": "DeltaS_eff=-delta lambda_A(mu,Xhat)/4 int F_Q^2",
            "status": "RETAINED_UNTIL_RADIOUT_CLOSURE",
            "effect": "tree-level ban does not protect b_alpha or clock readout",
            "repair_needed": "effective action/readout closure theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def alpha_consequence_rows() -> list[dict[str, str]]:
    return [
        {
            "consequence_id": "AC1057_0_if_unique",
            "condition": "unique parent Maxwell subblock plus fixed norm/current/readout",
            "result": "Lie_v ln alpha_EM=0",
            "impact": "b_alpha=0 and alpha-source branch can be theorem-zero with matter/source clauses",
            "current_status": "CONDITIONAL_ONLY",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "consequence_id": "AC1057_1_current",
            "condition": "current corpus",
            "result": "b_alpha not derived zero",
            "impact": "retain clock product bound and WEP product target; do not claim WEP/R10 alpha pass",
            "current_status": "RETAIN_B_ALPHA_PRODUCT_PRIOR",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "consequence_id": "AC1057_2_local_GR",
            "condition": "no-independent-F2 still unsigned",
            "result": "local GR/Newton reduction still has an EM/source constant-sector debt",
            "impact": "cannot call local branch fully GR-derived until visible constants/source normalizations are owned",
            "current_status": "PARTIAL_BLOCKER_RETAINED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def promotion_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "PG1057_0_unique_subblock",
            "claim_piece": "observed Maxwell F_Q^2 is unique parent subblock",
            "gate_pass": "false",
            "reason": "parent curvature norm route is conditional, not derived",
            "promotion_requirement": "parent A_Q projection plus fixed norm plus no independent F2",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "PG1057_1_no_independent_F2",
            "claim_piece": "lambda_A F_Q^2 is forbidden",
            "gate_pass": "false",
            "reason": "ordinary symmetries allow it; operator-domain exhaustion is unsigned",
            "promotion_requirement": "derive allowed visible operator algebra from parent action",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "PG1057_2_no_hidden_fX",
            "claim_piece": "f(Xhat)F_Q^2 is forbidden",
            "gate_pass": "false",
            "reason": "hidden scalar obstruction remains unless no-mixed functor is parent-signed",
            "promotion_requirement": "no hidden-visible coefficient hom theorem",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "PG1057_3_radiative",
            "claim_piece": "F_Q^2 counterterm stays banned after effective reduction",
            "gate_pass": "false",
            "reason": "radiative/readout closure remains unsigned",
            "promotion_requirement": "RG/readout closure or retained counterterm prior",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "PG1057_4_balpha_zero",
            "claim_piece": "b_alpha=0 from unique Maxwell subblock",
            "gate_pass": "false",
            "reason": "upstream unique-subblock and no-counterterm gates fail",
            "promotion_requirement": "PG1057_0..3 pass plus readout/current owner",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def retained_branch_rows() -> list[dict[str, str]]:
    return [
        {
            "retained_id": "RB1057_0_clock",
            "arena": "clock",
            "quantity": "b_alpha*tau_clock_time",
            "bound_or_status": "2.1e-18 yr^-1 product bound retained",
            "reason": "b_alpha zero is not derived and tau_clock is not parent-owned",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "retained_id": "RB1057_1_WEP",
            "arena": "MICROSCOPE_WEP",
            "quantity": "beta_source_alpha*b_alpha*tau_WEP",
            "bound_or_status": "4.797780522732e-05 product-width target retained",
            "reason": "no-independent-F2 ban and beta_source_alpha zero remain conditional",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "retained_id": "RB1057_2_R10",
            "arena": "R10_short_range",
            "quantity": "K_X^R10 beta_s beta_t + epsilon_tail",
            "bound_or_status": "unscoreable until finite branch inputs and promoted bound curve exist",
            "reason": "R10 alpha branch cannot use unsigned zero theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1057_0_theorem_shape",
            "decision": "unique Maxwell subblock theorem is exact if operator-domain exhaustion is signed",
            "because": "then lambda_A F_Q^2 and f(Xhat)F_Q^2 have no legal slot",
            "next_action": "do not promote until exhaustion is derived",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1057_1_current_status",
            "decision": "current corpus cannot ban independent F_Q^2",
            "because": "gauge/diffeomorphism allow it and product/operator-domain rules remain conditional contracts",
            "next_action": "retain b_alpha product-prior branch",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1057_2_best_next",
            "decision": "next attack is parent operator-domain exhaustion",
            "because": "that is the only route that bans visible kinetic counterterms without handwaving",
            "next_action": "1058-Y5-R10-visible-operator-domain-exhaustion-or-alpha-counterterm-prior.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1057_0_unique_F2",
            "claim": "observed Maxwell F_Q^2 is the unique parent subblock",
            "gate_pass": "false",
            "reason": "no-independent-F2 theorem is not derived",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1057_1_balpha_zero",
            "claim": "b_alpha=0",
            "gate_pass": "false",
            "reason": "lambda_A/f(Xhat) counterterms remain legal",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1057_2_beta_source_alpha_zero",
            "claim": "beta_source_alpha=0 via alpha owner",
            "gate_pass": "false",
            "reason": "EM owner and matter/source functor clauses remain conditional",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1057_3_WEP_R10",
            "claim": "WEP/R10 alpha branch passes",
            "gate_pass": "false",
            "reason": "requires derived zero theorem or full finite branch score inputs",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1058-Y5-R10-visible-operator-domain-exhaustion-or-alpha-counterterm-prior.md",
            "objective": "derive or reject the parent visible-operator-domain exhaustion rule that all visible kinetic/coupling terms are generated by parent quotient/curvature data; if rejected, formalize the retained alpha counterterm prior branch",
            "include": "allowed operator algebra, quotient/product functor, no hidden-visible hom, radiative counterterms, alpha counterterm prior, WEP/clock/R10 product links",
            "exclude": "aesthetic minimality, compactness-alone proof, unit-rescaling, cancellation, tau unity shortcut, public local-GR/R10/WEP/clock claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def mts_template_rows() -> list[dict[str, str]]:
    row = {
        "model_id": "MTS_source_normalized_Newton_branch",
        "branch_id": "unique_Maxwell_subblock_template",
        "curve_id": "MTS_1057_unique_Maxwell_subblock_nonclaim",
        "lambda_value": "MISSING_NO_INDEPENDENT_F2_OR_LAMBDA_X",
        "lambda_units": "m",
        "alpha_predicted": "MISSING_DERIVED_B_ALPHA_ZERO_OR_FINITE_ALPHA_BRANCH",
        "alpha_bound": "MISSING_PROMOTED_BOUND",
        "alpha_bound_source": str(BOUND_CANDIDATE),
        "force_law_form": "unique subblock route gives b_alpha=0 only if independent lambda_A F_Q^2 and f(Xhat)F_Q^2 operators are parent-forbidden",
        "derivation_status": "template_invalid_no_independent_F2_not_derived",
        "formula_reference": "P8_Y5_R10_1057_UNIQUE_MAXWELL_SUBBLOCK_THEOREM_ATTEMPT.csv",
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_1057_UNIQUE_MAXWELL_SUBBLOCK_THEOREM_ATTEMPT.csv",
        "assumptions": "nonclaim placeholder; no aesthetic minimality; no compactness-alone proof; no cancellation",
        "valid_for_claim": "false",
        "notes": "Runner must refuse this row until the no-independent-F2 theorem is derived or a full finite alpha(lambda) prediction is sourced.",
    }
    return [{column: row[column] for column in MTS_REQUIRED_COLUMNS}]


def runner_smoke_rows(status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "smoke_id": "SMOKE1057_0_R10_runner_refusal",
            "valid_mts_rows": str(status.get("valid_mts_rows", "")),
            "valid_bound_rows": str(status.get("valid_bound_rows", "")),
            "comparison_rows": str(status.get("comparison_rows", "")),
            "R10_pass_for_claim": str(status.get("R10_pass_for_claim", "")).lower(),
            "claim_allowed": str(status.get("claim_allowed", "")).lower(),
            "expected_result": "reject no-independent-F2 placeholder until derived",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def refusal_rows(status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "refusal_id": "REF1057_0_no_independent_F2",
            "object": "lambda_A F_Q^2 ban",
            "current_status": "NOT_DERIVED_RETAIN_B_ALPHA",
            "refusal_status": "blocked_for_claim",
            "failure_reasons": "ordinary symmetries allow F_Q^2; operator-domain exhaustion and radiative closure are unsigned",
            "score_eligible": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "refusal_id": "REF1057_1_R10_runner",
            "object": "R10 unique-Maxwell-subblock smoke row",
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
    theorem_rows: list[dict[str, str]],
    operator_rows: list[dict[str, str]],
    counterterm_rows_: list[dict[str, str]],
    alpha_rows: list[dict[str, str]],
    promotion_rows: list[dict[str, str]],
    retained_rows: list[dict[str, str]],
    template_rows: list[dict[str, str]],
    runner_status: dict[str, Any],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()})

    source_ok = all(flag(row.get("exists", "")) and flag(row.get("needle_found", "")) for row in source_rows)
    add("V1057_1_sources_exist_and_needles", source_ok, "every cited source path exists and every source needle was found")
    theorem_blocked = any(row.get("proof_id") == "UMS1057_5_verdict" and row.get("derivation_status") == "FAIL_CURRENT_CLAIM_OPERATOR_DOMAIN_EXHAUSTION_REQUIRED" for row in theorem_rows)
    add("V1057_2_unique_subblock_not_promoted", theorem_blocked, "unique Maxwell subblock theorem remains conditional/nonclaim")
    ordinary_allows = any(row.get("operator_id") == "OD1057_1_U1_gauge" and row.get("ordinary_symmetry_result") == "ALLOWED" for row in operator_rows)
    add("V1057_3_gauge_symmetry_allows_F2", ordinary_allows, "ordinary gauge/diffeomorphism symmetry does not ban independent F2")
    counterterms_retained = any(row.get("counterterm_id") == "CT1057_0_constant_lambda" for row in counterterm_rows_) and all(row.get("valid_for_claim") == "false" for row in counterterm_rows_)
    add("V1057_4_counterterms_retained", counterterms_retained, "constant/hidden/radiative F2 counterterms are retained")
    balpha_retained = any(row.get("consequence_id") == "AC1057_1_current" and row.get("current_status") == "RETAIN_B_ALPHA_PRODUCT_PRIOR" for row in alpha_rows)
    add("V1057_5_balpha_retained", balpha_retained, "b_alpha remains retained as product-prior branch")
    promotion_blocked = promotion_rows and all(row.get("gate_pass") == "false" and row.get("claim_allowed") == "false" for row in promotion_rows)
    add("V1057_6_promotion_gates_blocked", promotion_blocked, "promotion gates remain blocked")
    retained_ok = retained_rows and all(row.get("valid_for_claim") == "false" for row in retained_rows)
    add("V1057_7_retained_branch_rows_nonclaim", retained_ok, "retained branch rows remain nonclaim")
    template_schema = set(MTS_REQUIRED_COLUMNS).issubset(set(template_rows[0].keys())) if template_rows else False
    template_nonclaim = template_schema and all(row.get("valid_for_claim") == "false" for row in template_rows)
    add("V1057_8_mts_template_schema_nonclaim", template_nonclaim, "MTS template has runner schema and no claim-valid rows")
    runner_refused = runner_status.get("valid_mts_rows") == 0 and runner_status.get("claim_allowed") is False
    add("V1057_9_runner_smoke_refuses_claim", runner_refused, "existing R10 runner refuses the 1057 placeholder rows")
    claims_blocked = claim_rows and all(row.get("gate_pass") == "false" and row.get("claim_allowed") == "false" for row in claim_rows)
    add("V1057_10_claim_gates_blocked", claims_blocked, "all unique-F2/balpha/WEP/R10 claim gates remain blocked")
    next_ok = bool(next_rows) and next_rows[0].get("next_target", "").startswith("1058-Y5-R10-visible-operator")
    add("V1057_11_next_target_written", next_ok, "next target row is present")
    generated_inside = all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in outputs.values())
    add("V1057_12_generated_files_in_post_checkpoint", generated_inside, "all generated files are under post-checkpoint-work")
    formalization_count = count_formalization_modified_since_start()
    add("V1057_13_formalization_untouched", formalization_count == 0, f"formalization-workbench modified-file count since script start is {formalization_count}")

    summary_pass = all(row["result"] == "pass" for row in checks)
    checks.insert(0, {"check_id": "V1057_SUMMARY", "result": "pass" if summary_pass else "fail", "detail": "1057 unique Maxwell subblock/no-independent-F2 validation summary", "generated_utc": stamp()})
    return checks


def write_doc(
    source_rows: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    operator_rows: list[dict[str, str]],
    counterterm_rows_: list[dict[str, str]],
    alpha_rows: list[dict[str, str]],
    promotion_rows: list[dict[str, str]],
    retained_rows: list[dict[str, str]],
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
            "# 1057 Y5 R10 unique Maxwell subblock no independent F2 ban or balpha retention",
            "",
            "**Progress:** the no-independent-`F_Q^2` theorem is now stated in exact form. If every visible kinetic term is generated by the parent curvature norm and no extra `lambda_A F_Q^2` or `f(Xhat)F_Q^2` slot exists, then the alpha-owner route can work.",
            "",
            "**Current verdict:** the theorem does not close in the current corpus. Diffeomorphism and U(1) gauge invariance allow `F_Q^2`; only a stronger parent operator-domain exhaustion theorem can ban it.",
            "",
            "**Consequence:** `b_alpha=0` remains nonclaim. The retained branch is still the honest branch: clock product bound, WEP product target, and unscoreable R10 finite branch until upstream inputs are real.",
            "",
            "## Source register",
            md_table(source_rows, ["source_id", "source_path", "exists", "needle_found", "role"]),
            "",
            "## Unique Maxwell subblock theorem attempt",
            md_table(theorem_rows, ["proof_id", "claim_piece", "mathematical_form", "derivation_status", "proof_or_blocker", "if_true", "if_false", "valid_for_claim"]),
            "",
            "## Operator-domain audit",
            md_table(operator_rows, ["operator_id", "operator", "ordinary_symmetry_result", "reason", "stronger_rule_needed", "claim_allowed"]),
            "",
            "## Counterterm ledger",
            md_table(counterterm_rows_, ["counterterm_id", "counterterm", "formula", "status", "effect", "repair_needed", "valid_for_claim"]),
            "",
            "## Alpha consequence ledger",
            md_table(alpha_rows, ["consequence_id", "condition", "result", "impact", "current_status", "valid_for_claim"]),
            "",
            "## Promotion gates",
            md_table(promotion_rows, ["gate_id", "claim_piece", "gate_pass", "reason", "promotion_requirement", "claim_allowed"]),
            "",
            "## Retained branch ledger",
            md_table(retained_rows, ["retained_id", "arena", "quantity", "bound_or_status", "reason", "valid_for_claim"]),
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
    theorem_rows = unique_subblock_rows()
    operator_rows = operator_domain_rows()
    counterterm_rows_ = counterterm_rows()
    alpha_rows = alpha_consequence_rows()
    promotion_rows = promotion_gate_rows()
    retained_rows = retained_branch_rows()
    decisions = decision_rows()
    claim_rows = claim_gate_rows()
    next_rows = next_target_rows()
    template_rows = mts_template_rows()

    outputs: dict[str, Path] = {
        "source_register": OUT / "P8_Y5_R10_1057_SOURCE_REGISTER.csv",
        "theorem": OUT / "P8_Y5_R10_1057_UNIQUE_MAXWELL_SUBBLOCK_THEOREM_ATTEMPT.csv",
        "operator": OUT / "P8_Y5_R10_1057_OPERATOR_DOMAIN_AUDIT.csv",
        "counterterm": OUT / "P8_Y5_R10_1057_F2_COUNTERTERM_LEDGER.csv",
        "alpha": OUT / "P8_Y5_R10_1057_ALPHA_CONSEQUENCE_LEDGER.csv",
        "promotion": OUT / "P8_Y5_R10_1057_PROMOTION_GATES.csv",
        "retained": OUT / "P8_Y5_R10_1057_RETAINED_BRANCH_LEDGER.csv",
        "decisions": OUT / "P8_Y5_R10_1057_DECISION_LEDGER.csv",
        "claim_gates": OUT / "P8_Y5_R10_1057_CLAIM_GATES.csv",
        "next_target": OUT / "P8_Y5_R10_1057_NEXT_TARGET.csv",
        "mts_template": MTS_TEMPLATE,
        "runner_smoke": OUT / "P8_Y5_R10_1057_RUNNER_SMOKE_STATUS.csv",
        "placeholder_refusal": OUT / "P8_Y5_R10_1057_PLACEHOLDER_REFUSAL_RUNNER.csv",
        "validation": OUT / "P8_Y5_BRR545_1057_VALIDATION.csv",
        "doc": DOC,
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["theorem"], theorem_rows)
    write_csv(outputs["operator"], operator_rows)
    write_csv(outputs["counterterm"], counterterm_rows_)
    write_csv(outputs["alpha"], alpha_rows)
    write_csv(outputs["promotion"], promotion_rows)
    write_csv(outputs["retained"], retained_rows)
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
        theorem_rows,
        operator_rows,
        counterterm_rows_,
        alpha_rows,
        promotion_rows,
        retained_rows,
        template_rows,
        runner_status,
        claim_rows,
        next_rows,
    )
    write_csv(outputs["validation"], validation_rows)
    write_doc(
        source_rows,
        theorem_rows,
        operator_rows,
        counterterm_rows_,
        alpha_rows,
        promotion_rows,
        retained_rows,
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
