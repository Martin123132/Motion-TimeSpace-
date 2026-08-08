from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from R10_alpha_lambda_bound_prediction_runner import run_runner


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RUNS = ROOT / "runs"

SLUG = "Y5-R10-double-zero-exponent-origin-or-source-neutrality-proof"
DOC_PATH = ROOT / "608-Y5-R10-double-zero-exponent-origin-or-source-neutrality-proof.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_608_SOURCE_REGISTER.csv"
NORMSQUARE_PATH = RESIDUALS / "P8_Y5_R10_608_NORMSQUARE_P2_THEOREM_ATTEMPT.csv"
DETERMINANT_PATH = RESIDUALS / "P8_Y5_R10_608_DETERMINANT_P3_THEOREM_ATTEMPT.csv"
SOURCE_NEUTRALITY_PATH = RESIDUALS / "P8_Y5_R10_608_SOURCE_NEUTRALITY_FALLBACK.csv"
COUNTEREXAMPLE_PATH = RESIDUALS / "P8_Y5_R10_608_COUNTEREXAMPLE_GATE.csv"
EXPONENT_DECISION_PATH = RESIDUALS / "P8_Y5_R10_608_EXPONENT_DECISION.csv"
PARENT_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_608_PARENT_INPUT_UPDATE.csv"
MTS_TEMPLATE_PATH = RESIDUALS / "R10_alpha_lambda_curve_MTS_DOUBLE_ZERO_EXPONENT_TEMPLATE.csv"
RUNNER_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_608_RUNNER_SUMMARY.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_BRR545_608_DECISION.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_BRR545_608_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_608_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_608_VALIDATION.csv"

PRIOR_607_VALIDATION = RESIDUALS / "P8_Y5_BRR545_607_VALIDATION.csv"
PRIOR_607_EXPONENT = RESIDUALS / "P8_Y5_R10_607_EPSILON_EXPONENT_GATE.csv"
ANCHOR_BOUND = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv"

STATUS = "Y5_R10_p2_norm_square_theorem_derived_conditionally_parent_marker_exclusion_not_signed"
CLAIM_CEILING = "conditional_p2_p3_origin_attempt_only_no_R10_fifth_force_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "609-Y5-R10-parent-own-norm-square-activation-or-finite-p1-branch.md"
EPSILON_SHELL = 7.432631961576971e-06

SOURCE_FILES = [
    ("607-Y5-R10-compact-shell-parent-coefficient-factorization-or-theorem-zero.md", "immediate 607 handoff"),
    ("source-intake/mts_residuals/P8_Y5_BRR545_607_VALIDATION.csv", "prior validation gate"),
    ("source-intake/mts_residuals/P8_Y5_R10_607_EPSILON_EXPONENT_GATE.csv", "p gate requiring origin"),
    ("476-double-zero-memory-coupling-origin-or-coefficient-runner.md", "p>=2 requirement and determinant clue"),
    ("475-domain-selector-parent-action-clause-or-coefficient-fill.md", "double-zero parent action clause"),
    ("478-determinant-current-parent-ownership-or-demotion.md", "det(Q_coh) p=3 ownership audit"),
    ("275-JC-three-form-memory-current-from-Q.md", "conditional determinant current construction"),
    ("276-coherent-domain-projector-from-parent-variables.md", "fixed-D Q_coh projection"),
    ("309-MTS-boundary-projector-contract-attempt.md", "P_MTS/P_coh projector contract"),
    ("572-Y5-R10-parent-coefficient-envelope-or-neutrality-theorem.md", "zero-factor and neutrality theorem attempts"),
    ("573-Y5-R10-primitive-minimal-no-natural-marker-theorem-or-finite-envelope.md", "no-marker theorem reduction"),
    ("574-Y5-R10-local-invariant-generator-elimination-or-finite-envelope.md", "surviving marker generators"),
    ("576-Y5-R10-constant-source-current-universality-or-qbar-envelope.md", "qbar_XT source-current conditional theorem"),
    ("407-primitive-relational-quotient-action-sketch.md", "primitive quotient action sketch"),
    ("413-no-marker-parent-action-theorem-attempt.md", "no-marker parent theorem attempt"),
    ("source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv", "anchor-only non-claim R10 bound rows"),
    ("scripts/R10_alpha_lambda_bound_prediction_runner.py", "existing comparator reused unchanged"),
    ("scripts/Y5_R10_double_zero_exponent_origin_or_source_neutrality_proof.py", "this checkpoint generator"),
]

MTS_TEMPLATE_FIELDS = [
    "model_id",
    "branch_id",
    "curve_id",
    "lambda_value",
    "lambda_units",
    "alpha_predicted",
    "alpha_bound",
    "alpha_bound_source",
    "force_law_form",
    "derivation_status",
    "formula_reference",
    "source_file",
    "assumptions",
    "valid_for_claim",
    "notes",
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", "<br>").replace("|", "\\|")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def parse_float(value: str) -> float | None:
    try:
        parsed = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def is_true(value: str) -> bool:
    return str(value).strip().lower() == "true"


def make_sources() -> list[dict[str, str]]:
    return [
        {
            "source_file": source_file,
            "exists": str((ROOT / source_file).exists()),
            "role": role,
        }
        for source_file, role in SOURCE_FILES
    ]


def make_normsquare_rows() -> list[dict[str, str]]:
    return [
        {
            "step_id": "NS608_0_define_primitive_amplitude",
            "claim": "compact-shell activation has a primitive amplitude a_D in a relative-memory/source fibre E_D",
            "math_form": "a_D in E_D, local trivial branch a_D=0, epsilon_amp=||a_D||",
            "derivation": "607's epsilon exponent can be made precise only by deciding whether epsilon_shell is a primitive amplitude or an already-squared invariant.",
            "result": "amplitude_variable_defined_as_theorem_target",
            "promotion_status": "conditional",
            "blocker": "current proxy 7.432631961576971e-06 is not yet proved to be ||a_D|| rather than ||a_D||^2 or another scalar",
            "valid_for_claim": "false",
        },
        {
            "step_id": "NS608_1_no_linear_marker",
            "claim": "a scalar parent action cannot contain a naked linear a_D term if no orientation/source marker vector exists",
            "math_form": "S_act[a_D]=S_act[-a_D] or more generally S_act[R a_D]=S_act[a_D] for R in O(E_D)",
            "derivation": "a linear term L(a_D)=ell(a_D) requires a parent-owned covector ell in E_D*, which is exactly a material/domain/source marker.",
            "result": "linear_term_forbidden_if_no_marker_theorem_holds",
            "promotion_status": "conditional_theorem",
            "blocker": "573/574 did not eliminate all marker generators for claim",
            "valid_for_claim": "false",
        },
        {
            "step_id": "NS608_2_taylor_evenness",
            "claim": "smooth marker-free activation has no odd linear term at a_D=0",
            "math_form": "F(a_D)=F(0)+1/2 H_D(a_D,a_D)+O(||a_D||^4)",
            "derivation": "O(E_D) or sign invariance forces dF_0=0. Local silence additionally requires F(0)=0.",
            "result": "leading_activation_order_is_quadratic_in_primitive_amplitude",
            "promotion_status": "conditional_pass",
            "blocker": "requires parent-owned fibre metric/inner product and no-linear-marker theorem",
            "valid_for_claim": "false",
        },
        {
            "step_id": "NS608_3_p2_source_law",
            "claim": "if epsilon_shell is the primitive amplitude norm, p=2 follows",
            "math_form": "J_X = epsilon_amp^2 kappa_X rho_X + O(epsilon_amp^4); alpha_X=epsilon_amp^2 C_X + O(epsilon_amp^4)",
            "derivation": "insert NS608_2 into 607's Green-function factorization.",
            "result": "p_equals_2_derived_conditionally",
            "promotion_status": "not_parent_signed",
            "blocker": "epsilon proxy/amplitude identification and no-marker symmetry are not parent-derived",
            "valid_for_claim": "false",
        },
        {
            "step_id": "NS608_4_epsilon_notation_warning",
            "claim": "p depends on what epsilon_shell denotes",
            "math_form": "if epsilon_shell=A_D=||a_D||^2, then alpha=epsilon_shell C_X is p=1 in epsilon but p=2 in primitive a_D",
            "derivation": "avoid fake p=2 promotion by locking the primitive variable before scoring.",
            "result": "notation_gate_required",
            "promotion_status": "guardrail",
            "blocker": "current compact-shell proxy has not been decomposed into primitive amplitude versus invariant norm",
            "valid_for_claim": "false",
        },
        {
            "step_id": "NS608_5_normsquare_verdict",
            "claim": "the norm-square route derives p>=2",
            "math_form": "no linear marker + smooth scalar parent + epsilon=||a_D|| => p=2",
            "derivation": "this is the best clean theorem shape for local-GR silence.",
            "result": "conditional_p2_theorem_derived_not_claim_promoted",
            "promotion_status": "theorem_target",
            "blocker": "parent-owned no-marker and epsilon-amplitude identification remain unsatisfied",
            "valid_for_claim": "false",
        },
    ]


def make_determinant_rows() -> list[dict[str, str]]:
    return [
        {
            "step_id": "DET608_0_fixed_domain_shape",
            "claim": "coherent determinant gives p=3",
            "math_form": "J_C=det(Q_coh) Omega_D/V_D; integral_D J_C=(N_D/u3)^3",
            "source_support": "275 derives the fixed-domain kinematic shape",
            "result": "p3_shape_supported_conditionally",
            "blocker": "fixed-D and Q_coh ownership are not enough for physical local branch",
            "valid_for_claim": "false",
        },
        {
            "step_id": "DET608_1_raw_det_rejected",
            "claim": "raw det(Q) is safe",
            "math_form": "det(XI+S)=X^3-(X/2)Tr(S^2)+det(S)",
            "source_support": "275/478 show tracefree shear leaks into raw determinant",
            "result": "fail_raw_route",
            "blocker": "would activate local shear/GW/environmental channels",
            "valid_for_claim": "false",
        },
        {
            "step_id": "DET608_2_Qcoh_projection",
            "claim": "Q_coh projection removes shear",
            "math_form": "P_coh[Q]^i_j=(1/3)<Tr Q>_D delta^i_j",
            "source_support": "276 derives this for fixed D and fixed norm",
            "result": "fixed_D_projection_pass",
            "blocker": "physical D, P_MTS, Ward stress, and source channel still not parent-owned",
            "valid_for_claim": "false",
        },
        {
            "step_id": "DET608_3_FLRW_survival",
            "claim": "determinant route keeps FLRW active",
            "math_form": "FLRW Q_coh=(N/u3)I so integral_D J_C=(N/u3)^3",
            "source_support": "275 gives FLRW reduction and endpoint regularity",
            "result": "FLRW_survival_conditionally_good",
            "blocker": "same parent selector must derive local zero and FLRW nonzero without a fitted window",
            "valid_for_claim": "false",
        },
        {
            "step_id": "DET608_4_parent_ownership",
            "claim": "det(Q_coh) is parent-owned as physical source",
            "math_form": "S_parent -> D, P_MTS, P_coh, Ward-safe stress, R11 source silence",
            "source_support": "478 says this ownership chain fails current corpus",
            "result": "not_parent_owned",
            "blocker": "domain selection/projector/Ward/R11 gates remain open",
            "valid_for_claim": "false",
        },
        {
            "step_id": "DET608_5_verdict",
            "claim": "p=3 is derived for the physical local branch",
            "math_form": "alpha_X=epsilon_amp^3 C_X",
            "source_support": "shape yes, ownership no",
            "result": "p3_theorem_target_not_claim",
            "blocker": "only parent-owned Q_coh determinant can be used; raw determinant is forbidden",
            "valid_for_claim": "false",
        },
    ]


def make_source_neutrality_rows() -> list[dict[str, str]]:
    return [
        {
            "fallback_id": "SN608_0_qbar_XT",
            "zero_target": "qbar_XT=0",
            "proof_shape": "ordinary matter action factors through one observed X-blind coframe and MTS-trivial constants",
            "source_status": "conditional theorem from 572/576",
            "why_not_promoted": "573/574 did not eliminate marker generators and 579 conformal countermodel remains legal",
            "if_closed": "C_X=0 for ordinary test bodies",
            "valid_for_claim": "false",
        },
        {
            "fallback_id": "SN608_1_Qbar_XH",
            "zero_target": "Qbar_XH(lambda)=0",
            "proof_shape": "compact source, boundary, memory, domain, projector channels are in X kernel or orthogonal to Pi_M",
            "source_status": "not derived",
            "why_not_promoted": "hidden source channels and Pi_M projector ownership remain open",
            "if_closed": "C_X=0 for laboratory sources",
            "valid_for_claim": "false",
        },
        {
            "fallback_id": "SN608_2_KX",
            "zero_target": "K_X=0",
            "proof_shape": "X is a first-class constraint/no-pole mode before source variation",
            "source_status": "not derived",
            "why_not_promoted": "607 branch explicitly retains a finite quadratic X block",
            "if_closed": "no finite Yukawa exchange",
            "valid_for_claim": "false",
        },
        {
            "fallback_id": "SN608_3_priority",
            "zero_target": "source neutrality as fallback",
            "proof_shape": "derive one zero factor only if p-origin path cannot be parent-owned",
            "source_status": "defer",
            "why_not_promoted": "p>=2 route is more local-GR-friendly because it attacks source activation, not just one test channel",
            "if_closed": "R10 alpha can be theorem-zero without relying on epsilon power",
            "valid_for_claim": "false",
        },
    ]


def make_counterexample_rows() -> list[dict[str, str]]:
    return [
        {
            "counterexample_id": "CE608_0_linear_marker_covector",
            "construction": "parent action contains ell(a_D) X with a nonzero covector ell in E_D*",
            "why_allowed_without_premise": "if no-marker/O(E_D) symmetry is not parent-derived, ell is a legal source marker",
            "damage": "p=1 returns and double-zero local silence fails",
            "blocked_by": "parent-owned marker exclusion or O(E_D) invariant norm-square action",
            "valid_for_claim": "false",
        },
        {
            "counterexample_id": "CE608_1_epsilon_already_squared",
            "construction": "epsilon_shell is defined as A_D=||a_D||^2 rather than primitive ||a_D||",
            "why_allowed_without_premise": "current proxy provenance does not identify primitive amplitude",
            "damage": "p=1 in epsilon notation can be physically p=2; scoring becomes ambiguous",
            "blocked_by": "explicit amplitude/norm-square ledger before any alpha row promotion",
            "valid_for_claim": "false",
        },
        {
            "counterexample_id": "CE608_2_raw_determinant_shear",
            "construction": "use det(Q) instead of det(Q_coh)",
            "why_allowed_without_premise": "if projection ownership is skipped, raw determinant is the simple-looking parent scalar",
            "damage": "tracefree shear leaks into local branch and can violate GR recovery",
            "blocked_by": "parent-owned coherent projection plus Ward stress accounting",
            "valid_for_claim": "false",
        },
        {
            "counterexample_id": "CE608_3_conformal_matter_coupling",
            "construction": "hat_g_mu_nu=exp(2 a X) g_mu_nu",
            "why_allowed_without_premise": "covariant universal matter coupling alone does not force a=0",
            "damage": "qbar_XT and J_matter are nonzero even if p>=2 reduces compact-shell source",
            "blocked_by": "X-blind observed coframe and constant-sector no-marker theorem",
            "valid_for_claim": "false",
        },
        {
            "counterexample_id": "CE608_4_overstrong_zero_kills_FLRW",
            "construction": "impose all compact-shell/domain activation zero in every domain",
            "why_allowed_without_premise": "a closure can silence local branch by also murdering cosmology",
            "damage": "loses the unified-field spine because FLRW memory branch dies",
            "blocked_by": "same parent selector must give local trivial and FLRW nontrivial classes",
            "valid_for_claim": "false",
        },
    ]


def make_exponent_decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "ED608_0_p2_normsquare",
            "candidate": "p=2 from norm-square/even parent activation",
            "mathematical_status": "conditional theorem derived",
            "claim_status": "not promoted",
            "why": "requires no-linear-marker/O(E_D) symmetry and primitive epsilon identification",
            "next_action": "parent-own norm-square activation",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "ED608_1_p3_determinant",
            "candidate": "p=3 from det(Q_coh)",
            "mathematical_status": "conditional fixed-D shape supported",
            "claim_status": "not promoted",
            "why": "raw det leaks shear and Q_coh/D/P_MTS/Ward/R11 ownership is incomplete",
            "next_action": "keep as theorem target, not first promotion route",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "ED608_2_p1_finite",
            "candidate": "p=1 finite residual",
            "mathematical_status": "still legal unless marker exclusion closes",
            "claim_status": "retained fallback",
            "why": "linear marker covector counterexample remains legal without no-marker theorem",
            "next_action": "score later only if p>=2 cannot be derived and coefficients are numeric",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "ED608_3_zero_factor",
            "candidate": "source/test/no-pole neutrality",
            "mathematical_status": "conditional fallback",
            "claim_status": "not promoted",
            "why": "qbar/source/K zero routes remain blocked by 572/576/579",
            "next_action": "try only after p-origin route is exhausted",
            "valid_for_claim": "false",
        },
    ]


def make_parent_update_rows() -> list[dict[str, str]]:
    return [
        {
            "input_id": "PUI608_0_primitive_amplitude",
            "required_input": "a_D and epsilon_amp=||a_D||",
            "exact_definition": "primitive compact-shell relative-memory/source amplitude before squaring",
            "current_status": "not_parent_identified",
            "needed_to_promote": "prove current epsilon_shell proxy is the primitive amplitude or rewrite p in primitive variables",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "input_id": "PUI608_1_marker_exclusion",
            "required_input": "no parent covector ell(a_D)",
            "exact_definition": "no natural material/domain/source marker can select a sign/direction in E_D",
            "current_status": "conditional_only",
            "needed_to_promote": "eliminate 573/574 marker generators or encode O(E_D) symmetry in parent action",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "input_id": "PUI608_2_fibre_metric",
            "required_input": "parent-owned inner product on E_D",
            "exact_definition": "positive relative-memory/domain fibre metric used to form ||a_D||^2",
            "current_status": "not_parent_owned",
            "needed_to_promote": "derive inner product from parent symplectic/Hodge/relative complex without closure",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "input_id": "PUI608_3_local_FLRW_split",
            "required_input": "local a_D=0, FLRW a_D!=0",
            "exact_definition": "same selector gives exact local trivial class and nontrivial FLRW coherent class",
            "current_status": "conditional",
            "needed_to_promote": "derive branch split without fitted window or PPN-motivated collar choice",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "input_id": "PUI608_4_CX",
            "required_input": "C_X(lambda_X)",
            "exact_definition": "sigma_X kappa_X Qbar_XH(lambda_X) qbar_XT/(4*pi Z_X G_obs)",
            "current_status": "symbolic",
            "needed_to_promote": "numeric source/test/Hessian coefficients or a source-neutrality zero",
            "next_action": "defer until p branch is parent-owned",
            "valid_for_claim": "false",
        },
    ]


def make_mts_template_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    anchors = read_csv(ANCHOR_BOUND)
    for anchor in anchors:
        for branch_id, p, note in [
            ("R10_normsquare_p2_symbolic", 2, "conditional norm-square theorem target"),
            ("R10_determinant_p3_symbolic", 3, "conditional determinant theorem target"),
        ]:
            rows.append(
                {
                    "model_id": "MTS_double_zero_exponent_origin",
                    "branch_id": branch_id,
                    "curve_id": "R10_alpha_lambda_curve_MTS_DOUBLE_ZERO_EXPONENT_TEMPLATE",
                    "lambda_value": anchor.get("lambda_value", ""),
                    "lambda_units": anchor.get("lambda_units", "m"),
                    "alpha_predicted": f"(epsilon_amp**{p})*C_X(lambda_X)",
                    "alpha_bound": anchor.get("alpha_bound", "1.0"),
                    "alpha_bound_source": f"source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv::{anchor.get('bound_id', '')}",
                    "force_law_form": "Yukawa_potential_alpha",
                    "derivation_status": "symbolic_double_zero_origin_nonclaim",
                    "formula_reference": "608-Y5-R10-double-zero-exponent-origin-or-source-neutrality-proof.md::NS608_3_or_DET608_0",
                    "source_file": "608-Y5-R10-double-zero-exponent-origin-or-source-neutrality-proof.md",
                    "assumptions": "MISSING_PARENT_OWNED_EPSILON_AMP;MISSING_NO_MARKER_SYMMETRY;MISSING_C_X;anchor_bound_only",
                    "valid_for_claim": "false",
                    "notes": f"Template row only: {note}; runner must reject until parent inputs and bound curve are claim-grade.",
                }
            )
    return rows


def make_runner_summary(run_result: dict[str, Any]) -> list[dict[str, str]]:
    status = run_result["status"]
    return [
        {
            "runner_id": "R10_RUNNER_608_DOUBLE_ZERO_TEMPLATE_RECHECK",
            "mts_curve": status["mts_curve"],
            "bound_curve": status["bound_curve"],
            "mts_rows": str(status["mts_rows"]),
            "valid_mts_rows": str(status["valid_mts_rows"]),
            "bound_rows": str(status["bound_rows"]),
            "valid_bound_rows": str(status["valid_bound_rows"]),
            "comparison_rows": str(status["comparison_rows"]),
            "passed_rows": str(status["passed_rows"]),
            "blocked_or_failed_rows": str(status["blocked_or_failed_rows"]),
            "R10_pass_for_claim": str(status["R10_pass_for_claim"]),
            "claim_allowed": str(status["claim_allowed"]),
            "notes": "required blocked result: p=2/p=3 templates remain symbolic and anchor bounds are nonclaim",
        }
    ]


def make_decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "D608_0_normsquare_theorem",
            "status": "conditional_theorem_derived",
            "decision": "accept p=2 as a valid theorem if parent owns primitive amplitude, norm-square action, and no-linear-marker symmetry",
            "meaning": "this is the cleanest local-GR-friendly route but not a current claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D608_1_determinant_theorem",
            "status": "conditional_shape_only",
            "decision": "keep p=3 determinant route as a theorem target, not first promotion route",
            "meaning": "det(Q_coh) is stronger but depends on more projector/domain ownership than norm-square p=2",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D608_2_source_neutrality",
            "status": "fallback_not_promoted",
            "decision": "do not switch to source neutrality until p-origin route is exhausted",
            "meaning": "qbar/source/no-pole zeros are useful but currently less close than the norm-square theorem",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D608_3_claim_ceiling",
            "status": CLAIM_CEILING,
            "decision": "no R10, WEP, PPN, or local-GR pass",
            "meaning": "p>=2 is conditional and C_X/lambda/bound-curve inputs remain unresolved",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def make_route_rows() -> list[dict[str, str]]:
    return [
        {
            "route_id": "RU608_0_primary",
            "allowed_after_608": "try to parent-own the norm-square activation and no-linear-marker symmetry",
            "forbidden_after_608": "use p=2 in claim rows before epsilon_amp and marker exclusion are parent-derived",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU608_1_determinant",
            "allowed_after_608": "retain det(Q_coh) as p=3 theorem target",
            "forbidden_after_608": "use raw det(Q) or ignore shear leakage",
            "next_action": "defer unless norm-square route fails",
        },
        {
            "route_id": "RU608_2_fallback",
            "allowed_after_608": "fallback to qbar/source/no-pole neutrality or finite p=1 score if p>=2 fails",
            "forbidden_after_608": "erase p=1 counterexample without no-marker theorem",
            "next_action": "keep finite branch retained",
        },
    ]


def make_summary_rows() -> list[dict[str, str]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "epsilon_shell": f"{EPSILON_SHELL:.15g}",
            "p2_normsquare": "conditional_theorem_derived",
            "p3_determinant": "conditional_shape_only",
            "p_parent_signed": "false",
            "source_neutrality_signed": "false",
            "R10_pass": "false",
            "WEP_pass": "false",
            "PPN_pass": "false",
            "local_GR_pass": "false",
            "next_target": NEXT_TARGET,
        }
    ]


def count_claim_rows(row_sets: list[list[dict[str, Any]]]) -> int:
    return sum(1 for rows in row_sets for row in rows if is_true(str(row.get("valid_for_claim", ""))))


def make_validation_rows(
    sources: list[dict[str, str]],
    norm_rows: list[dict[str, str]],
    det_rows: list[dict[str, str]],
    source_neutrality_rows: list[dict[str, str]],
    counterexample_rows: list[dict[str, str]],
    exponent_rows: list[dict[str, str]],
    parent_rows: list[dict[str, str]],
    mts_rows: list[dict[str, str]],
    runner_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    prior_validation = read_csv(PRIOR_607_VALIDATION)
    prior_failures = [row for row in prior_validation if row.get("result") != "pass"]
    missing_sources = [row["source_file"] for row in sources if row["exists"] != "True"]
    p2_verdict = [row for row in norm_rows if row["step_id"] == "NS608_5_normsquare_verdict"]
    p3_verdict = [row for row in det_rows if row["step_id"] == "DET608_5_verdict"]
    source_claim_rows = [row for row in source_neutrality_rows if is_true(row.get("valid_for_claim", ""))]
    template_symbolic = all(parse_float(row.get("alpha_predicted", "")) is None for row in mts_rows)
    template_nonclaim = all(row.get("valid_for_claim") == "false" for row in mts_rows)
    runner = runner_rows[0]
    claim_rows = count_claim_rows(
        [
            norm_rows,
            det_rows,
            source_neutrality_rows,
            counterexample_rows,
            exponent_rows,
            parent_rows,
            mts_rows,
            decision_rows,
            summary_rows,
        ]
    )
    return [
        {
            "check_id": "V608_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}" + (f";{';'.join(missing_sources)}" if missing_sources else ""),
        },
        {
            "check_id": "V608_1_prior_607_clean",
            "result": "pass" if prior_validation and not prior_failures else "fail",
            "detail": f"prior_rows={len(prior_validation)};prior_failures={len(prior_failures)}",
        },
        {
            "check_id": "V608_2_normsquare_p2_conditional",
            "result": "pass"
            if p2_verdict and p2_verdict[0]["result"] == "conditional_p2_theorem_derived_not_claim_promoted"
            else "fail",
            "detail": p2_verdict[0]["math_form"] if p2_verdict else "missing_normsquare_verdict",
        },
        {
            "check_id": "V608_3_p2_not_promoted",
            "result": "pass" if all(row["valid_for_claim"] == "false" for row in norm_rows) else "fail",
            "detail": f"norm_rows={len(norm_rows)};claim_rows={count_claim_rows([norm_rows])}",
        },
        {
            "check_id": "V608_4_determinant_p3_not_promoted",
            "result": "pass"
            if p3_verdict and p3_verdict[0]["result"] == "p3_theorem_target_not_claim" and all(row["valid_for_claim"] == "false" for row in det_rows)
            else "fail",
            "detail": p3_verdict[0]["blocker"] if p3_verdict else "missing_det_verdict",
        },
        {
            "check_id": "V608_5_source_neutrality_not_promoted",
            "result": "pass" if not source_claim_rows and source_neutrality_rows else "fail",
            "detail": f"source_neutrality_rows={len(source_neutrality_rows)};claim_rows={len(source_claim_rows)}",
        },
        {
            "check_id": "V608_6_counterexamples_block_shortcuts",
            "result": "pass" if len(counterexample_rows) >= 5 else "fail",
            "detail": f"counterexamples={len(counterexample_rows)}",
        },
        {
            "check_id": "V608_7_template_symbolic_nonclaim",
            "result": "pass" if mts_rows and template_symbolic and template_nonclaim else "fail",
            "detail": f"template_rows={len(mts_rows)};symbolic={template_symbolic};nonclaim={template_nonclaim}",
        },
        {
            "check_id": "V608_8_runner_blocks_template",
            "result": "pass"
            if runner["R10_pass_for_claim"] == "False"
            and runner["claim_allowed"] == "False"
            and runner["valid_mts_rows"] == "0"
            and runner["valid_bound_rows"] == "0"
            else "fail",
            "detail": (
                f"valid_mts={runner['valid_mts_rows']};valid_bound={runner['valid_bound_rows']};"
                f"R10_pass={runner['R10_pass_for_claim']};claim_allowed={runner['claim_allowed']}"
            ),
        },
        {
            "check_id": "V608_9_no_claim_rows",
            "result": "pass" if claim_rows == 0 else "fail",
            "detail": f"claim_rows={claim_rows}",
        },
        {
            "check_id": "V608_10_no_R10_or_local_GR_claim",
            "result": "pass"
            if summary_rows[0]["R10_pass"] == "false"
            and summary_rows[0]["WEP_pass"] == "false"
            and summary_rows[0]["PPN_pass"] == "false"
            and summary_rows[0]["local_GR_pass"] == "false"
            else "fail",
            "detail": "R10_pass=false;WEP=false;PPN=false;local_GR=false",
        },
    ]


def write_doc(
    generated: str,
    run_root: Path,
    sources: list[dict[str, str]],
    norm_rows: list[dict[str, str]],
    det_rows: list[dict[str, str]],
    source_neutrality_rows: list[dict[str, str]],
    counterexample_rows: list[dict[str, str]],
    exponent_rows: list[dict[str, str]],
    parent_rows: list[dict[str, str]],
    mts_rows: list[dict[str, str]],
    runner_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    route_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    doc = f"""# 608 Y5 R10 double-zero exponent origin or source-neutrality proof

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`  
Run root: `{rel(run_root)}`

## Verdict
- The best derivation is the norm-square theorem: if the compact-shell variable is a primitive amplitude `a_D`, and the parent action has no linear marker covector, then smooth scalar activation starts at `||a_D||^2`, so `p=2`.
- This is a real conditional theorem, not just a wish. It is also not yet a claim, because the current corpus has not parent-owned the amplitude, fibre metric, and no-marker symmetry.
- The determinant route still gives a beautiful `p=3` shape, but only for parent-owned `Q_coh`; raw `det(Q)` is forbidden because it leaks tracefree shear.
- Source/test/no-pole neutrality remains a fallback, not the first promotion route.

## Source Register
{markdown_table(sources, ["source_file", "exists", "role"])}

## Norm-Square P2 Theorem Attempt
{markdown_table(norm_rows, ["step_id", "claim", "math_form", "derivation", "result", "promotion_status", "blocker", "valid_for_claim"])}

## Determinant P3 Theorem Attempt
{markdown_table(det_rows, ["step_id", "claim", "math_form", "source_support", "result", "blocker", "valid_for_claim"])}

## Source-Neutrality Fallback
{markdown_table(source_neutrality_rows, ["fallback_id", "zero_target", "proof_shape", "source_status", "why_not_promoted", "if_closed", "valid_for_claim"])}

## Counterexample Gate
{markdown_table(counterexample_rows, ["counterexample_id", "construction", "why_allowed_without_premise", "damage", "blocked_by", "valid_for_claim"])}

## Exponent Decision
{markdown_table(exponent_rows, ["decision_id", "candidate", "mathematical_status", "claim_status", "why", "next_action", "valid_for_claim"])}

## Parent Input Update
{markdown_table(parent_rows, ["input_id", "required_input", "exact_definition", "current_status", "needed_to_promote", "next_action", "valid_for_claim"])}

## MTS Double-Zero Template
{markdown_table(mts_rows, MTS_TEMPLATE_FIELDS)}

## Runner Summary
{markdown_table(runner_rows, ["runner_id", "mts_curve", "bound_curve", "mts_rows", "valid_mts_rows", "bound_rows", "valid_bound_rows", "comparison_rows", "passed_rows", "blocked_or_failed_rows", "R10_pass_for_claim", "claim_allowed", "notes"])}

## Decision
{markdown_table(decision_rows, ["decision_id", "status", "decision", "meaning", "next_target", "valid_for_claim"])}

## Route Update
{markdown_table(route_rows, ["route_id", "allowed_after_608", "forbidden_after_608", "next_action"])}

## Validation
{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Practical Read
This is one of the better-looking local-branch moves so far. We have not proved local GR, but we found the exact parent-action shape that would make the annoying linear residual illegal: no linear marker plus norm-square activation. That is very engineering-flavoured: if there is no signed handle to grab, the first scalar you can build is quadratic. The next lock is therefore narrow and concrete: parent-own the primitive amplitude/fibre metric/no-marker symmetry, or admit the finite `p=1` branch remains legal.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def main() -> None:
    generated = datetime.now(timezone.utc).isoformat()
    run_root = RUNS / f"{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{SLUG}"
    result_dir = run_root / "results"

    sources = make_sources()
    norm_rows = make_normsquare_rows()
    det_rows = make_determinant_rows()
    source_neutrality_rows = make_source_neutrality_rows()
    counterexample_rows = make_counterexample_rows()
    exponent_rows = make_exponent_decision_rows()
    parent_rows = make_parent_update_rows()
    mts_rows = make_mts_template_rows()

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_file", "exists", "role"])
    write_csv(NORMSQUARE_PATH, norm_rows, ["step_id", "claim", "math_form", "derivation", "result", "promotion_status", "blocker", "valid_for_claim"])
    write_csv(DETERMINANT_PATH, det_rows, ["step_id", "claim", "math_form", "source_support", "result", "blocker", "valid_for_claim"])
    write_csv(SOURCE_NEUTRALITY_PATH, source_neutrality_rows, ["fallback_id", "zero_target", "proof_shape", "source_status", "why_not_promoted", "if_closed", "valid_for_claim"])
    write_csv(COUNTEREXAMPLE_PATH, counterexample_rows, ["counterexample_id", "construction", "why_allowed_without_premise", "damage", "blocked_by", "valid_for_claim"])
    write_csv(EXPONENT_DECISION_PATH, exponent_rows, ["decision_id", "candidate", "mathematical_status", "claim_status", "why", "next_action", "valid_for_claim"])
    write_csv(PARENT_UPDATE_PATH, parent_rows, ["input_id", "required_input", "exact_definition", "current_status", "needed_to_promote", "next_action", "valid_for_claim"])
    write_csv(MTS_TEMPLATE_PATH, mts_rows, MTS_TEMPLATE_FIELDS)

    runner_result = run_runner(MTS_TEMPLATE_PATH, ANCHOR_BOUND, result_dir)
    runner_rows = make_runner_summary(runner_result)
    write_csv(RUNNER_SUMMARY_PATH, runner_rows, ["runner_id", "mts_curve", "bound_curve", "mts_rows", "valid_mts_rows", "bound_rows", "valid_bound_rows", "comparison_rows", "passed_rows", "blocked_or_failed_rows", "R10_pass_for_claim", "claim_allowed", "notes"])

    decision_rows = make_decision_rows()
    route_rows = make_route_rows()
    summary_rows = make_summary_rows()
    validation_rows = make_validation_rows(
        sources,
        norm_rows,
        det_rows,
        source_neutrality_rows,
        counterexample_rows,
        exponent_rows,
        parent_rows,
        mts_rows,
        runner_rows,
        decision_rows,
        summary_rows,
    )

    write_csv(DECISION_PATH, decision_rows, ["decision_id", "status", "decision", "meaning", "next_target", "valid_for_claim"])
    write_csv(ROUTE_UPDATE_PATH, route_rows, ["route_id", "allowed_after_608", "forbidden_after_608", "next_action"])
    write_csv(SUMMARY_PATH, summary_rows, ["status", "claim_ceiling", "epsilon_shell", "p2_normsquare", "p3_determinant", "p_parent_signed", "source_neutrality_signed", "R10_pass", "WEP_pass", "PPN_pass", "local_GR_pass", "next_target"])
    write_csv(VALIDATION_PATH, validation_rows, ["check_id", "result", "detail"])

    write_doc(
        generated,
        run_root,
        sources,
        norm_rows,
        det_rows,
        source_neutrality_rows,
        counterexample_rows,
        exponent_rows,
        parent_rows,
        mts_rows,
        runner_rows,
        decision_rows,
        route_rows,
        validation_rows,
    )

    status = {
        "generated": generated,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
        "doc": rel(DOC_PATH),
        "validation": rel(VALIDATION_PATH),
        "runner_status": rel(result_dir / "R10_runner_status.json"),
        "all_validation_pass": all(row["result"] == "pass" for row in validation_rows),
    }
    (run_root / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
