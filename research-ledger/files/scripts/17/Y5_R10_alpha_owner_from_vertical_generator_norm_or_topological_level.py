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
DOC = ROOT / "1056-Y5-R10-alpha-owner-from-vertical-generator-norm-or-topological-level.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1056-alpha-owner-generator-norm-topological-smoke" / "results"
MTS_TEMPLATE = OUT / "R10_alpha_lambda_curve_MTS_1056_ALPHA_OWNER_TEMPLATE_NONCLAIM.csv"
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
        ("SRC1056_0_1055_next", "source-intake/mts_residuals/P8_Y5_R10_1055_NEXT_TARGET.csv", "1056-Y5-R10-alpha-owner-from-vertical-generator-norm-or-topological-level.md", "1055 handoff."),
        ("SRC1056_1_1055_contract", "source-intake/mts_residuals/P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv", "PAC1055_1_EM_owner", "EM owner contract clause."),
        ("SRC1056_2_1055_consequence", "source-intake/mts_residuals/P8_Y5_R10_1055_THEOREM_CONSEQUENCES.csv", "TC1055_2_beta_source_alpha", "conditional beta_source_alpha payoff."),
        ("SRC1056_3_764_owner", "source-intake/mts_residuals/P8_Y5_R10_764_ALPHA_EM_OWNER_AUDIT.csv", "AEO764_2_parent_vertical_generator_norm", "alpha owner candidate audit."),
        ("SRC1056_4_765_norm", "source-intake/mts_residuals/P8_Y5_R10_765_VERTICAL_GENERATOR_NORM_THEOREM_ATTEMPT.csv", "VGN765_6_verdict", "prior vertical-generator norm attempt."),
        ("SRC1056_5_765_inheritance", "source-intake/mts_residuals/P8_Y5_R10_765_MAXWELL_KINETIC_INHERITANCE_GATE.csv", "MKI765_2_unique_F2", "Maxwell kinetic inheritance gates."),
        ("SRC1056_6_765_rescale", "source-intake/mts_residuals/P8_Y5_R10_765_RESCALING_COUNTEREXAMPLE_LEDGER.csv", "RCE765_0_lambda_F2", "rescaling and independent F2 counterexamples."),
        ("SRC1056_7_642_maxwell", "source-intake/mts_residuals/P8_Y5_R10_642_MAXWELL_DESCENT_ATTEMPT.csv", "MD642_4_alpha_constant", "Maxwell descent alpha-owner blocker."),
        ("SRC1056_8_927_compact_BF", "source-intake/mts_residuals/P8_Y5_R10_927_COMPACT_BF_PARENT_ACTION_CONTRACT.csv", "CBF927_1_large_gauge_invariance", "compact/topological BF route."),
        ("SRC1056_9_1049_symmetry", "source-intake/mts_residuals/P8_Y5_R10_1049_SYMMETRY_BAN_THEOREM_ATTEMPT.csv", "SBT1049_1_gauge_invariance", "gauge invariance does not ban scalar kinetic functions."),
        ("SRC1056_10_1049_operator", "source-intake/mts_residuals/P8_Y5_R10_1049_OPERATOR_CLASSIFICATION_RULE_ATTEMPT.csv", "OCR1049_5_verdict", "operator-classification route."),
        ("SRC1056_11_1051_alpha", "source-intake/mts_residuals/P8_Y5_R10_1051_ALPHA_OWNER_RADIATIVE_CLOSURE_AUDIT.csv", "AOR1051_3_verdict", "alpha/radiative closure remains retained."),
        ("SRC1056_12_1054_prior", "source-intake/mts_residuals/P8_Y5_R10_1054_NUMERIC_PRIOR_WIDTH_LEDGER.csv", "NPW1054_0_alpha_WEP_product", "finite alpha product-width target."),
        ("SRC1056_13_1052_clock", "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv", "ACB1052_2", "best clock alpha product bound."),
        ("SRC1056_14_R10_bound_candidate", "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv", "R10_VECTOR_2020_REVIEW_0000", "R10 review-candidate bound curve for smoke only."),
        ("SRC1056_15_R10_runner", "scripts/R10_alpha_lambda_bound_prediction_runner.py", "MTS_REQUIRED_COLUMNS", "existing R10 runner and schema."),
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


def vertical_norm_attempt_rows() -> list[dict[str, str]]:
    return [
        {
            "attempt_id": "VNA1056_0_parent_charge_generator",
            "route": "compact parent generator",
            "mathematical_form": "T_Q in Lie(G_parent) or charge lattice L_Q, exp(2*pi*T_Q)=1, A_parent includes A_Q T_Q",
            "would_derive": "charge labels and connection period are representation/lattice data",
            "current_result": "PARTIAL_SUPPORT_ONLY",
            "blocker": "T_Q is not yet supplied as a varied parent-action object with source/readout owner",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "VNA1056_1_fixed_generator_norm",
            "route": "fixed parent norm",
            "mathematical_form": "N_Q=<T_Q,T_Q>_P fixed by parent fibre metric/symplectic/lattice data and Lie_v N_Q=0",
            "would_derive": "generator rescaling is forbidden and A_Q normalization becomes parent-owned",
            "current_result": "NOT_PARENT_SIGNED",
            "blocker": "no current parent theorem fixes N_Q or forbids T_Q -> s T_Q in the EM sector",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "VNA1056_2_curvature_subblock",
            "route": "literal parent curvature subblock",
            "mathematical_form": "S_parent contains -C_P/4 int <F,F>_P, so g_EM^{-2}=C_P N_Q",
            "would_derive": "Maxwell kinetic coefficient inherited from parent norm",
            "current_result": "FAILS_CURRENT_CORPUS",
            "blocker": "independent DeltaS=-lambda_A/4 int F_Q^2 is not forbidden",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "VNA1056_3_same_current_owner",
            "route": "same generator owns current",
            "mathematical_form": "delta S_m/delta A_Q = J_Q with charges as T_Q representation weights",
            "would_derive": "charge unit, source current, and Lorentz readout share one normalization",
            "current_result": "NOT_PARENT_SIGNED",
            "blocker": "current normalization and matter derivative normalization remain unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "VNA1056_4_readout_descent",
            "route": "dimensionless alpha readout",
            "mathematical_form": "alpha_EM=g_EM^2/(4*pi*hbar*c) and Lie_v ln(hbar*c)=Lie_v ln(*_obs)=0",
            "would_derive": "fixed abstract EM norm becomes fixed observed alpha",
            "current_result": "NOT_PARENT_SIGNED",
            "blocker": "coframe/Hodge/spectroscopy readout descent and hbar*c status remain separate clauses",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "VNA1056_5_conditional_theorem",
            "route": "vertical-generator norm theorem",
            "mathematical_form": "VNA1056_0..4 plus no independent F_Q^2 => Lie_v ln alpha_EM=0",
            "would_derive": "b_alpha=0 and alpha-marker beta_source_alpha route closes structurally",
            "current_result": "VALID_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "blocker": "VNA1056_1..4 are not all signed and VNA1056_2 fails",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "VNA1056_6_verdict",
            "route": "current alpha-owner status",
            "mathematical_form": "cannot promote alpha_EM owner while lambda_A F_Q^2, generator/current rescaling, or readout leakage remains legal",
            "would_derive": "none yet",
            "current_result": "ALPHA_OWNER_NOT_DERIVED_RETAIN_B_ALPHA",
            "blocker": "unique Maxwell subblock/no-independent-F2 theorem missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def topological_route_rows() -> list[dict[str, str]]:
    return [
        {
            "route_id": "TL1056_0_compact_U1",
            "candidate": "compact U(1) connection",
            "mathematical_form": "F/2pi has integral periods and charges are lattice/representation labels",
            "what_it_owns": "charge quantization and connection period",
            "what_it_does_not_own": "continuous 4D Maxwell kinetic coefficient g_EM^{-2}",
            "status": "SUPPORT_ONLY_NOT_ALPHA_OWNER",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "route_id": "TL1056_1_BF_or_CS_level",
            "candidate": "BF/Chern-Simons/topological level",
            "mathematical_form": "S_top=2*pi*k int b wedge da or analogous quantized response",
            "what_it_owns": "integer level or topological response coefficient",
            "what_it_does_not_own": "ordinary Maxwell F_Q^2 coefficient unless the low-energy kinetic term inherits the level",
            "status": "POSSIBLE_BUT_NOT_PRESENT_AS_PARENT_THEOREM",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "route_id": "TL1056_2_index_anomaly_monopole",
            "candidate": "index/anomaly/monopole normalization",
            "mathematical_form": "charge/current level fixed by topological index or monopole quantization",
            "what_it_owns": "may own charge unit or theta/topological response",
            "what_it_does_not_own": "alpha_EM unless gauge kinetic norm is linked to the same index",
            "status": "SOURCE_ABSENT_IN_CURRENT_CORPUS",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "route_id": "TL1056_3_KK_radius_modulus",
            "candidate": "compact fibre radius or modulus",
            "mathematical_form": "g_EM^{-2} proportional to fixed fibre radius/volume",
            "what_it_owns": "alpha_EM only if modulus is parent-fixed and vertical-silent",
            "what_it_does_not_own": "local alpha silence if the radius/modulus can vary with Xhat",
            "status": "DANGEROUS_OPEN_ROUTE",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "route_id": "TL1056_4_verdict",
            "candidate": "topological alpha owner",
            "mathematical_form": "topology fixes alpha_EM only with an explicit inheritance theorem to F_Q^2",
            "what_it_owns": "nothing claim-grade yet",
            "what_it_does_not_own": "b_alpha zero in the current corpus",
            "status": "TOPOLOGICAL_ROUTE_NOT_CLOSED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def rescaling_rows() -> list[dict[str, str]]:
    return [
        {
            "counterexample_id": "RSC1056_0_independent_F2",
            "legal_if_unsigned": "add independent Maxwell kinetic invariant",
            "mathematical_form": "Delta S=-lambda_A/4 int sqrt(-g_obs) F_Q^{mu nu}F^Q_{mu nu}",
            "effect": "g_EM^{-2}=C_P N_Q+lambda_A, so alpha_EM is not fixed by parent curvature norm",
            "repair_needed": "operator classification forbids independent F_Q^2",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "counterexample_id": "RSC1056_1_generator_rescale",
            "legal_if_unsigned": "rescale generator and compensate connection/current labels",
            "mathematical_form": "T_Q -> s T_Q, A_Q -> A_Q/s, n_A -> s n_A when lattice/norm owner is absent",
            "effect": "charge unit and A normalization remain conventional/free",
            "repair_needed": "fixed compact lattice plus nonrescalable parent norm",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "counterexample_id": "RSC1056_2_current_rescale",
            "legal_if_unsigned": "current normalization independent from kinetic coefficient",
            "mathematical_form": "S_int=sum_A q_A(Xhat) int A_Q J_A",
            "effect": "same F_Q^2 coefficient but different WEP/R10/source-test charge response",
            "repair_needed": "same Noether owner for kinetic term, charge unit, current, and matter coupling",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "counterexample_id": "RSC1056_3_readout_leak",
            "legal_if_unsigned": "Hodge star or hbar*c readout carries vertical data",
            "mathematical_form": "*_obs=A_X^p *bar or d ln(hbar*c)/dXhat != 0",
            "effect": "dimensionless alpha readout changes despite fixed abstract generator norm",
            "repair_needed": "quotient-fixed coframe/Hodge/spectroscopy readout",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def b_alpha_branch_rows() -> list[dict[str, str]]:
    return [
        {
            "branch_id": "BAB1056_0_clock_product",
            "arena": "clock",
            "retained_quantity": "b_alpha*tau_clock_time",
            "current_bound_or_status": "2.1e-18 yr^-1 best Yb+ E3/E2 product row",
            "why_retained": "alpha owner not derived, tau_clock_time not parent-owned",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "branch_id": "BAB1056_1_WEP_product",
            "arena": "MICROSCOPE_WEP",
            "retained_quantity": "beta_source_alpha*b_alpha*tau_WEP",
            "current_bound_or_status": "4.797780522732e-05 product target in 1052/1054 smoke convention",
            "why_retained": "alpha zero theorem and tau_WEP map not derived",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "branch_id": "BAB1056_2_R10_product",
            "arena": "R10_short_range",
            "retained_quantity": "K_X^R10(lambda)*beta_s(lambda)*beta_t(lambda)+epsilon_tail(lambda)",
            "current_bound_or_status": "unscoreable; lambda_X, K_X/Z_X, tau_R10, beta_s, beta_t, and promoted bound curve missing",
            "why_retained": "alpha-marker source/test zero is only conditional",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "branch_id": "BAB1056_3_verdict",
            "arena": "cross_arena",
            "retained_quantity": "b_alpha finite branch",
            "current_bound_or_status": "retain product-prior branch, not standalone alpha claim",
            "why_retained": "unique Maxwell subblock/no-independent-F2 proof is missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def promotion_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "PG1056_0_parent_generator",
            "claim_piece": "T_Q parent generator exists with nonrescalable norm",
            "gate_pass": "false",
            "reason": "compact charge support exists only as template; parent norm is not signed",
            "promotion_requirement": "source-backed parent fibre metric/lattice/symplectic norm",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "PG1056_1_unique_F2",
            "claim_piece": "Maxwell kinetic term is unique parent subblock",
            "gate_pass": "false",
            "reason": "independent lambda_A F_Q^2 invariant remains legal",
            "promotion_requirement": "operator-classification/no-independent-F2 theorem",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "PG1056_2_same_current",
            "claim_piece": "charge current and kinetic term share same owner",
            "gate_pass": "false",
            "reason": "Noether current normalization and matter charge derivative are unsigned",
            "promotion_requirement": "same T_Q owner for S_EM and S_int",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "PG1056_3_readout",
            "claim_piece": "dimensionless alpha readout is quotient-fixed",
            "gate_pass": "false",
            "reason": "Hodge/coframe/hbar*c readout descent remains a separate open clause",
            "promotion_requirement": "observed readout descent theorem",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "PG1056_4_alpha_zero",
            "claim_piece": "b_alpha=0 and beta_source_alpha=0 from alpha owner",
            "gate_pass": "false",
            "reason": "requires all upstream alpha-owner gates",
            "promotion_requirement": "PG1056_0..3 pass together plus radiative closure",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1056_0_norm_route",
            "decision": "vertical-generator norm route has the right theorem shape",
            "because": "if T_Q, its norm, F_Q^2, current, and readout share one parent owner, Lie_v alpha_EM=0 follows",
            "next_action": "try to prove no independent F_Q^2 operator",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1056_1_topology_route",
            "decision": "topology/compactness alone does not own alpha_EM",
            "because": "compact U1 fixes charge lattice/periods, not the continuous 4D Maxwell kinetic coefficient unless inheritance is proved",
            "next_action": "do not claim b_alpha=0 from compactness alone",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1056_2_choke_point",
            "decision": "independent F_Q^2 is the next choke point",
            "because": "lambda_A F_Q^2 defeats generator-norm inheritance even if a parent norm exists",
            "next_action": "1057-Y5-R10-unique-Maxwell-subblock-no-independent-F2-ban-or-balpha-retention.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1056_0_alpha_owner",
            "claim": "alpha_EM is parent-owned and vertically constant",
            "gate_pass": "false",
            "reason": "generator norm, unique F2, current owner, and readout descent are not jointly derived",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1056_1_topology",
            "claim": "topological/compact route fixes alpha_EM",
            "gate_pass": "false",
            "reason": "topology fixes charge/level data but not Maxwell kinetic coefficient without an inheritance theorem",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1056_2_balpha_zero",
            "claim": "b_alpha=0",
            "gate_pass": "false",
            "reason": "alpha owner remains unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1056_3_beta_source_alpha_zero",
            "claim": "beta_source_alpha=0 via EM owner",
            "gate_pass": "false",
            "reason": "conditional on b_alpha/EM owner plus matter/source functor clauses",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1056_4_WEP_R10",
            "claim": "WEP/R10 alpha branch passes",
            "gate_pass": "false",
            "reason": "requires derived alpha zero theorem or full finite branch inputs",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1057-Y5-R10-unique-Maxwell-subblock-no-independent-F2-ban-or-balpha-retention.md",
            "objective": "try to prove the observed Maxwell F_Q^2 term is the unique parent curvature subblock and that no independent lambda_A F_Q^2 operator is admissible; if not, keep b_alpha as a retained product-prior branch",
            "include": "operator classification, gauge invariance limits, parent curvature norm, independent F2 counterexample, radiative closure, consequence for b_alpha and beta_source_alpha",
            "exclude": "compactness-alone proof, declaring alpha fixed by taste, unit-rescaling, cancellation, tau unity shortcut, public local-GR/R10/WEP/clock claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def mts_template_rows() -> list[dict[str, str]]:
    row = {
        "model_id": "MTS_source_normalized_Newton_branch",
        "branch_id": "alpha_owner_generator_norm_template",
        "curve_id": "MTS_1056_alpha_owner_nonclaim",
        "lambda_value": "MISSING_ALPHA_OWNER_OR_LAMBDA_X",
        "lambda_units": "m",
        "alpha_predicted": "MISSING_DERIVED_ALPHA_ZERO_OR_FINITE_ALPHA_BRANCH",
        "alpha_bound": "MISSING_PROMOTED_BOUND",
        "alpha_bound_source": str(BOUND_CANDIDATE),
        "force_law_form": "alpha owner route would give b_alpha=0 only if generator norm, unique F2, current owner, and readout descent are parent-signed",
        "derivation_status": "template_invalid_alpha_owner_not_derived",
        "formula_reference": "P8_Y5_R10_1056_VERTICAL_GENERATOR_NORM_DERIVATION_AUDIT.csv",
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_1056_VERTICAL_GENERATOR_NORM_DERIVATION_AUDIT.csv",
        "assumptions": "nonclaim placeholder; compactness alone not enough; no rescaling; no cancellation",
        "valid_for_claim": "false",
        "notes": "Runner must refuse this row until alpha owner is derived or a full finite alpha(lambda) prediction is sourced.",
    }
    return [{column: row[column] for column in MTS_REQUIRED_COLUMNS}]


def runner_smoke_rows(status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "smoke_id": "SMOKE1056_0_R10_runner_refusal",
            "valid_mts_rows": str(status.get("valid_mts_rows", "")),
            "valid_bound_rows": str(status.get("valid_bound_rows", "")),
            "comparison_rows": str(status.get("comparison_rows", "")),
            "R10_pass_for_claim": str(status.get("R10_pass_for_claim", "")).lower(),
            "claim_allowed": str(status.get("claim_allowed", "")).lower(),
            "expected_result": "reject alpha-owner placeholder until derived",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def refusal_rows(status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "refusal_id": "REF1056_0_alpha_owner",
            "object": "alpha_EM parent owner",
            "current_status": "ALPHA_OWNER_NOT_DERIVED_RETAIN_B_ALPHA",
            "refusal_status": "blocked_for_claim",
            "failure_reasons": "independent F_Q^2, generator/current rescaling, and readout leakage remain legal",
            "score_eligible": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "refusal_id": "REF1056_1_R10_runner",
            "object": "R10 alpha-owner smoke row",
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
    norm_rows: list[dict[str, str]],
    topology_rows: list[dict[str, str]],
    rescale_rows: list[dict[str, str]],
    balpha_rows: list[dict[str, str]],
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
    add("V1056_1_sources_exist_and_needles", source_ok, "every cited source path exists and every source needle was found")
    norm_verdict = any(row.get("attempt_id") == "VNA1056_6_verdict" and row.get("current_result") == "ALPHA_OWNER_NOT_DERIVED_RETAIN_B_ALPHA" for row in norm_rows)
    add("V1056_2_norm_route_not_promoted", norm_verdict, "vertical-generator norm route is conditional and not promoted")
    topology_blocked = any(row.get("route_id") == "TL1056_4_verdict" and row.get("status") == "TOPOLOGICAL_ROUTE_NOT_CLOSED" for row in topology_rows)
    add("V1056_3_topology_route_not_closed", topology_blocked, "topological route does not fix alpha without inheritance theorem")
    independent_f2 = any(row.get("counterexample_id") == "RSC1056_0_independent_F2" for row in rescale_rows)
    add("V1056_4_rescaling_counterexamples_retained", independent_f2 and all(row.get("valid_for_claim") == "false" for row in rescale_rows), "independent F2/rescaling counterexamples are retained")
    balpha_retained = any(row.get("branch_id") == "BAB1056_3_verdict" and "retain" in row.get("current_bound_or_status", "") for row in balpha_rows)
    add("V1056_5_balpha_branch_retained", balpha_retained, "b_alpha remains a retained product-prior branch")
    promotion_blocked = promotion_rows and all(row.get("gate_pass") == "false" and row.get("claim_allowed") == "false" for row in promotion_rows)
    add("V1056_6_promotion_gates_blocked", promotion_blocked, "alpha-owner promotion gates remain blocked")
    template_schema = set(MTS_REQUIRED_COLUMNS).issubset(set(template_rows[0].keys())) if template_rows else False
    template_nonclaim = template_schema and all(row.get("valid_for_claim") == "false" for row in template_rows)
    add("V1056_7_mts_template_schema_nonclaim", template_nonclaim, "MTS template has runner schema and no claim-valid rows")
    runner_refused = runner_status.get("valid_mts_rows") == 0 and runner_status.get("claim_allowed") is False
    add("V1056_8_runner_smoke_refuses_claim", runner_refused, "existing R10 runner refuses the 1056 placeholder rows")
    claims_blocked = claim_rows and all(row.get("gate_pass") == "false" and row.get("claim_allowed") == "false" for row in claim_rows)
    add("V1056_9_claim_gates_blocked", claims_blocked, "all alpha-owner/balpha/WEP/R10 claim gates remain blocked")
    next_ok = bool(next_rows) and next_rows[0].get("next_target", "").startswith("1057-Y5-R10-unique-Maxwell")
    add("V1056_10_next_target_written", next_ok, "next target row is present")
    generated_inside = all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in outputs.values())
    add("V1056_11_generated_files_in_post_checkpoint", generated_inside, "all generated files are under post-checkpoint-work")
    formalization_count = count_formalization_modified_since_start()
    add("V1056_12_formalization_untouched", formalization_count == 0, f"formalization-workbench modified-file count since script start is {formalization_count}")

    summary_pass = all(row["result"] == "pass" for row in checks)
    checks.insert(0, {"check_id": "V1056_SUMMARY", "result": "pass" if summary_pass else "fail", "detail": "1056 alpha-owner vertical-generator norm/topological route validation summary", "generated_utc": stamp()})
    return checks


def write_doc(
    source_rows: list[dict[str, str]],
    norm_rows: list[dict[str, str]],
    topology_rows: list[dict[str, str]],
    rescale_rows: list[dict[str, str]],
    balpha_rows: list[dict[str, str]],
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
            "# 1056 Y5 R10 alpha owner from vertical generator norm or topological level",
            "",
            "**Progress:** the alpha-owner route is now narrowed to a precise inheritance theorem: `T_Q`, its norm, the Maxwell `F_Q^2` coefficient, the current normalization, and the observed alpha readout must share one parent owner.",
            "",
            "**Current verdict:** compactness/topology helps with charge labels but does not by itself fix `alpha_EM`. The live obstruction is the independent `lambda_A F_Q^2` operator plus generator/current/readout rescaling freedom.",
            "",
            "**Consequence:** `b_alpha=0` and `beta_source_alpha=0` are not claimable from EM ownership yet. The honest state is retained product-prior branch, with the next attack aimed at banning independent `F_Q^2`.",
            "",
            "## Source register",
            md_table(source_rows, ["source_id", "source_path", "exists", "needle_found", "role"]),
            "",
            "## Vertical generator norm derivation audit",
            md_table(norm_rows, ["attempt_id", "route", "mathematical_form", "would_derive", "current_result", "blocker", "valid_for_claim"]),
            "",
            "## Topological level/index route audit",
            md_table(topology_rows, ["route_id", "candidate", "mathematical_form", "what_it_owns", "what_it_does_not_own", "status", "valid_for_claim"]),
            "",
            "## Rescaling degeneracy ledger",
            md_table(rescale_rows, ["counterexample_id", "legal_if_unsigned", "mathematical_form", "effect", "repair_needed", "valid_for_claim"]),
            "",
            "## Retained b_alpha branch ledger",
            md_table(balpha_rows, ["branch_id", "arena", "retained_quantity", "current_bound_or_status", "why_retained", "valid_for_claim"]),
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
    norm_rows = vertical_norm_attempt_rows()
    topology_rows = topological_route_rows()
    rescale_rows = rescaling_rows()
    balpha_rows = b_alpha_branch_rows()
    promotion_rows = promotion_gate_rows()
    decisions = decision_rows()
    claim_rows = claim_gate_rows()
    next_rows = next_target_rows()
    template_rows = mts_template_rows()

    outputs: dict[str, Path] = {
        "source_register": OUT / "P8_Y5_R10_1056_SOURCE_REGISTER.csv",
        "norm": OUT / "P8_Y5_R10_1056_VERTICAL_GENERATOR_NORM_DERIVATION_AUDIT.csv",
        "topology": OUT / "P8_Y5_R10_1056_TOPOLOGICAL_LEVEL_INDEX_ROUTE_AUDIT.csv",
        "rescale": OUT / "P8_Y5_R10_1056_RESCALING_DEGENERACY_LEDGER.csv",
        "balpha": OUT / "P8_Y5_R10_1056_RETAINED_B_ALPHA_BRANCH_LEDGER.csv",
        "promotion": OUT / "P8_Y5_R10_1056_PROMOTION_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1056_DECISION_LEDGER.csv",
        "mts_template": MTS_TEMPLATE,
        "runner_smoke": OUT / "P8_Y5_R10_1056_RUNNER_SMOKE_STATUS.csv",
        "placeholder_refusal": OUT / "P8_Y5_R10_1056_PLACEHOLDER_REFUSAL_RUNNER.csv",
        "claim_gates": OUT / "P8_Y5_R10_1056_CLAIM_GATES.csv",
        "next_target": OUT / "P8_Y5_R10_1056_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1056_VALIDATION.csv",
        "doc": DOC,
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["norm"], norm_rows)
    write_csv(outputs["topology"], topology_rows)
    write_csv(outputs["rescale"], rescale_rows)
    write_csv(outputs["balpha"], balpha_rows)
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
        norm_rows,
        topology_rows,
        rescale_rows,
        balpha_rows,
        promotion_rows,
        template_rows,
        runner_status,
        claim_rows,
        next_rows,
    )
    write_csv(outputs["validation"], validation_rows)
    write_doc(
        source_rows,
        norm_rows,
        topology_rows,
        rescale_rows,
        balpha_rows,
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
