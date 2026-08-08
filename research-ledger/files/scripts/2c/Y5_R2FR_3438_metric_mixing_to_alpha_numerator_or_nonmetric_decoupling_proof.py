from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3438-Y5-R2FR-metric-mixing-to-alpha-numerator-or-nonmetric-decoupling-proof-under-AX1090.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCES = {
    "doc_3437": ROOT / "3437-Y5-R2FR-q_loc-source-current-coupling-map-or-zero-current-theorem-under-AX1090.md",
    "next_3437": OUT / "P8_Y5_R2FR_3437_NEXT_TARGET.csv",
    "coupling_fork_3437": OUT / "P8_Y5_R2FR_3437_COUPLING_BRANCH_FORK.csv",
    "direct_current_3437": OUT / "P8_Y5_R2FR_3437_DIRECT_MATTER_SOURCE_CURRENT_THEOREM.csv",
    "alpha_numerator_3437": OUT / "P8_Y5_R2FR_3437_R10_ALPHA_NUMERATOR_STATUS.csv",
    "counterexamples_3437": OUT / "P8_Y5_R2FR_3437_RETAINED_COUPLING_COUNTEREXAMPLES.csv",
    "source_map_3436": OUT / "P8_Y5_R2FR_3436_MTS_ALPHA_SOURCE_MAP_STATUS.csv",
    "runner_contract_3436": OUT / "P8_Y5_R2FR_3436_ALPHA_LAMBDA_RUNNER_CONTRACT.csv",
    "ppn_stack_3434": OUT / "P8_Y5_R2FR_3434_FIRST_PPN_RESIDUAL_STACK.csv",
    "positive_x_nohair_1042": OUT / "P8_Y5_R10_1042_POSITIVE_X_NOHAIR_IDENTITY.csv",
    "source_owner_contract": OUT / "P8_source_owner_parent_action_terms_CONTRACT.csv",
    "source_norm_channel_audit": OUT / "P8_SOURCE_NORMALIZATION_CHANNEL_AUDIT.csv",
    "source_norm_coefficients": OUT / "P8_SOURCE_NORMALIZATION_COEFFICIENT_FILL.csv",
    "source_norm_stack": OUT / "P8_SOURCE_NORMALIZATION_THEOREM_STACK.csv",
    "constant_gm_hair_gate": OUT / "P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv",
    "eh_selection_1512": ROOT / "1512-Y5-parent-EH-operator-selection-theorem-or-nonEH-residual-vector.md",
    "minimality_1513": ROOT / "1513-Y5-parent-primitive-minimality-no-higher-derivative-theorem-or-R11-vector-lock.md",
    "tau_kernel_1573": ROOT / "1573-Y5-RAB-internal-tauR10-source-kernel-or-manual-curve-acceptance.md",
    "matter_charge_1574": ROOT / "1574-Y5-RAB-R10-matter-charge-and-ZR-MR2-input-row-or-zero-theorem.md",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3438_SOURCE_REGISTER.csv",
    "metric_mixing_schur_theorem": OUT / "P8_Y5_R2FR_3438_METRIC_MIXING_SCHUR_THEOREM.csv",
    "nonmetric_decoupling_conditions": OUT / "P8_Y5_R2FR_3438_NONMETRIC_DECOUPLING_CONDITIONS.csv",
    "metric_mixing_alpha_template": OUT / "P8_Y5_R2FR_3438_METRIC_MIXING_ALPHA_TEMPLATE.csv",
    "operator_input_rows": OUT / "P8_Y5_R2FR_3438_OPERATOR_INPUT_ROWS.csv",
    "ppn_r10_impact_update": OUT / "P8_Y5_R2FR_3438_PPN_R10_IMPACT_UPDATE.csv",
    "residual_counterexamples": OUT / "P8_Y5_R2FR_3438_RESIDUAL_COUNTEREXAMPLES.csv",
    "score_readiness": OUT / "P8_Y5_R2FR_3438_SCORE_READINESS.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3438_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3438_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3438_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3438_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3438_VALIDATION.csv",
}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields = list(rows[0].keys())

    def clean(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "/")

    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |",
            *["| " + " | ".join(clean(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def source_register() -> list[dict[str, Any]]:
    roles = {
        "doc_3437": "direct matter coupling handoff",
        "next_3437": "3438 target declaration",
        "coupling_fork_3437": "identity/class/metric-mixing coupling fork",
        "direct_current_3437": "direct J_i matter zero theorem",
        "alpha_numerator_3437": "retained alpha numerator components",
        "counterexamples_3437": "metric-mixing counterexample",
        "source_map_3436": "R10 alpha source-map blocker",
        "runner_contract_3436": "R10 alpha(lambda) runner contract",
        "ppn_stack_3434": "PPN/R10 residual stack",
        "positive_x_nohair_1042": "positive-X nohair identity",
        "source_owner_contract": "parent source-owner action blocks",
        "source_norm_channel_audit": "source-normalization channel audit",
        "source_norm_coefficients": "missing scalar/range/nonEH coefficients",
        "source_norm_stack": "source-normalization theorem stack",
        "constant_gm_hair_gate": "range/radial/source hair derivative gate",
        "eh_selection_1512": "EH operator selection and retained nonEH vector",
        "minimality_1513": "primitive minimality/nonEH lock",
        "tau_kernel_1573": "formal R10 Yukawa kernel law",
        "matter_charge_1574": "matter charge beta/Z/M input row theorem",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[source_id],
            "valid_for_claim": False,
        }
        for source_id, path in SOURCES.items()
    ]


def metric_mixing_schur_theorem() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "SCH3438_0_quadratic_parent_block",
            "statement": "After gauge fixing and projection to the local weak-field branch, the metric source mode h and finite nonmetric modes X_i have a quadratic Hessian block.",
            "formula": "S2=1/2<h,O_H h>+<h,B_i X_i>+1/2<X_i,O_X^{ij}X_j>+<h,J_H>+<X_i,J_i^direct>+boundary",
            "status": "FORMAL_LOCAL_LINEARIZATION_DERIVED",
            "condition_or_missing": "requires parent quadratic Hessian entries O_H, B_i, O_X^{ij} in one normalization",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "SCH3438_1_direct_current_zero_inserted",
            "statement": "The 3437 identity-coframe branch sets the direct finite-mode matter current to zero but leaves the Hessian mixing block.",
            "formula": "J_i^direct=0, while B_i may be nonzero",
            "status": "USES_3437_ZERO_BRANCH_NONCLAIM",
            "condition_or_missing": "identity coframe/nonmetric-X branch; parent selection still conditional",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "SCH3438_2_induced_source",
            "statement": "Metric mixing induces a finite-mode source whenever the EH metric response sourced by matter has a component in the B_i dagger direction.",
            "formula": "O_X^{ij}X_j = -B_i^dagger h; h≈-G_H J_H; therefore J_i^{gX}:=B_i^dagger G_H J_H",
            "status": "SCHUR_SOURCE_LAW_DERIVED_NONCLAIM",
            "condition_or_missing": "need B_i, G_H projection, source normalization and gauge projector",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "SCH3438_3_effective_metric_operator",
            "statement": "Eliminating X shifts the metric propagator by a Schur-complement term with the finite-mode pole.",
            "formula": "O_H^eff = O_H - B_i (O_X^{-1})^{ij} B_j^dagger",
            "status": "SCHUR_COMPLEMENT_DERIVED_NONCLAIM",
            "condition_or_missing": "finite pole absent only if B-sector or O_X^{-1} pole is theorem-zero/constraint",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "SCH3438_4_yukawa_alpha_template",
            "statement": "If O_X has a positive finite pole, the metric-mixing piece is an R10 alpha(lambda) numerator, not an absorbable G0 calibration.",
            "formula": "lambda_i=sqrt(Z_i/M_i^2); alpha_i^{gX}=Xi_R10 tau_i [Qbar_i^{S,gX} qbar_i^{T,gX}/(4*pi*G0*Z_i)+alpha_i^{tail}]",
            "status": "FIRST_METRIC_MIXING_ALPHA_TEMPLATE_DERIVED_NONCLAIM",
            "condition_or_missing": "Z_i, M_i^2, B_i projections, Xi_R10, tau_i and tail rows missing",
            "valid_for_claim": False,
        },
    ]


def nonmetric_decoupling_conditions() -> list[dict[str, Any]]:
    return [
        {
            "condition_id": "NDC3438_0_block_diagonal_hessian",
            "decoupling_condition": "B_i=0 on the local source-coupled EH scalar/vector/tensor blocks.",
            "mathematical_test": "delta^2 S_parent/(delta h_H delta X_i)=0 after gauge/projector fixing",
            "current_status": "NOT_PARENT_SIGNED",
            "claim_effect_if_signed": "kills metric-induced finite-mode source for that channel",
            "valid_for_claim": False,
        },
        {
            "condition_id": "NDC3438_1_source_projector_orthogonality",
            "decoupling_condition": "B_i^dagger G_H J_H=0 for every allowed compact source and test sector.",
            "mathematical_test": "Pi_i B_i^dagger G_H Pi_H J_H[S]=0 and same for test readout",
            "current_status": "NOT_PARENT_SIGNED",
            "claim_effect_if_signed": "allows B_i nonzero while source-visible projection vanishes",
            "valid_for_claim": False,
        },
        {
            "condition_id": "NDC3438_2_constraint_no_pole",
            "decoupling_condition": "X_i has no finite propagating pole in the local branch.",
            "mathematical_test": "O_X^{-1} has no Yukawa pole, or X_i is first-class/auxiliary with algebraic zero response",
            "current_status": "NOT_PARENT_SIGNED",
            "claim_effect_if_signed": "removes lambda_i from R10 rather than bounding alpha_i",
            "valid_for_claim": False,
        },
        {
            "condition_id": "NDC3438_3_positive_nohair_with_induced_source_zero",
            "decoupling_condition": "The positive nohair identity applies with J_i^{direct}+J_i^{gX}+J_i^{boundary}=0.",
            "mathematical_test": "int[Z_i|grad X_i|^2+M_i^2 X_i^2]=0 only after all source terms vanish",
            "current_status": "PARTIAL_ONLY_DIRECT_J_ZERO_FROM_3437",
            "claim_effect_if_signed": "would let NH1042 close the range branch",
            "valid_for_claim": False,
        },
        {
            "condition_id": "NDC3438_4_boundary_projector_orthogonality",
            "decoupling_condition": "Boundary/projector/domain tails are exact, topological, or orthogonal to the source readout.",
            "mathematical_test": "alpha_i^{tail}=0 and no Pi_M/readout source flux",
            "current_status": "NOT_PARENT_SIGNED",
            "claim_effect_if_signed": "removes tail from the absolute alpha envelope",
            "valid_for_claim": False,
        },
    ]


def metric_mixing_alpha_template() -> list[dict[str, Any]]:
    return [
        {
            "template_id": "MMAT3438_0_operator_form",
            "lambda_value": "sqrt(Z_i/M_i^2)",
            "alpha_predicted": "Xi_R10*tau_i*(Qbar_i_S_gX*qbar_i_T_gX/(4*pi*G0*Z_i)+alpha_i_tail)",
            "source_leg": "Qbar_i_S_gX := normalized(Pi_i B_i^dagger G_H J_H[source])",
            "test_leg": "qbar_i_T_gX := normalized(Pi_i B_i^dagger G_H J_H[test]) or equivalent metric-readout response",
            "status": "TEMPLATE_ONLY_INPUTS_MISSING",
            "failure_reasons": "MISSING_B_i;MISSING_Z_i;MISSING_M_i2;MISSING_SOURCE_PROJECTOR;MISSING_TEST_PROJECTOR;MISSING_Xi_R10;MISSING_TAU_i;MISSING_TAIL;MISSING_BOUND_CURVE",
            "valid_for_claim": False,
        },
        {
            "template_id": "MMAT3438_1_zero_case",
            "lambda_value": "not_required_if_NDC3438_0_or_NDC3438_1_or_NDC3438_2_signed",
            "alpha_predicted": "0 for metric-mixing component only",
            "source_leg": "Qbar_i_S_gX=0",
            "test_leg": "qbar_i_T_gX=0",
            "status": "ZERO_TEMPLATE_CONDITIONAL_NOT_SIGNED",
            "failure_reasons": "BLOCK_DIAGONAL_OR_ORTHOGONALITY_OR_NO_POLE_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "template_id": "MMAT3438_2_absolute_envelope",
            "lambda_value": "sqrt(Z_i/M_i^2) if finite pole survives",
            "alpha_predicted": "abs(alpha_i_gX)+abs(alpha_i_class)+abs(alpha_i_boundary)+abs(alpha_i_projector)+abs(alpha_i_q_loc)",
            "source_leg": "absolute no-cancellation source envelope",
            "test_leg": "absolute no-cancellation test/readout envelope",
            "status": "ENVELOPE_POLICY_DERIVED_VALUES_MISSING",
            "failure_reasons": "all component values/zero certificates missing",
            "valid_for_claim": False,
        },
    ]


def operator_input_rows() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "OP3438_0_B_i",
            "symbol": "B_i = delta^2 S_parent/(delta h_H delta X_i)",
            "role": "metric/X Hessian mixing entry",
            "minimum_required_form": "parent-signed zero, or operator value with gauge/projector convention and units",
            "current_status": "MISSING_OPERATOR_ENTRY",
            "valid_for_claim": False,
        },
        {
            "input_id": "OP3438_1_G_H",
            "symbol": "G_H",
            "role": "gauge-fixed EH metric Green/projector used to map Hilbert source to h_H",
            "minimum_required_form": "same-frame local EH projector and source normalization",
            "current_status": "CONDITIONAL_EH_ONLY_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "input_id": "OP3438_2_OX",
            "symbol": "O_X=Z_i(-nabla^2)+M_i^2+...",
            "role": "finite-mode operator and range",
            "minimum_required_form": "Z_i, M_i^2, pole/no-pole signature in same normalization as B_i",
            "current_status": "MISSING_Z_M2_OR_NO_POLE",
            "valid_for_claim": False,
        },
        {
            "input_id": "OP3438_3_source_projection",
            "symbol": "Qbar_i_S_gX",
            "role": "source body metric-mixing charge",
            "minimum_required_form": "normalized Pi_i B_i^dagger G_H J_H[source] or zero theorem",
            "current_status": "MISSING_SOURCE_PROJECTION",
            "valid_for_claim": False,
        },
        {
            "input_id": "OP3438_4_test_projection",
            "symbol": "qbar_i_T_gX",
            "role": "test body/readout metric-mixing response",
            "minimum_required_form": "normalized Pi_i B_i^dagger G_H J_H[test] or readout zero theorem",
            "current_status": "MISSING_TEST_PROJECTION",
            "valid_for_claim": False,
        },
        {
            "input_id": "OP3438_5_R10_readout",
            "symbol": "Xi_R10, tau_i, alpha_i_tail",
            "role": "convert parent propagator correction into R10 alpha(lambda)",
            "minimum_required_form": "source-backed convention and tail zero/bound rows",
            "current_status": "MISSING_READOUT_AND_TAILS",
            "valid_for_claim": False,
        },
    ]


def ppn_r10_impact_update() -> list[dict[str, Any]]:
    return [
        {
            "impact_id": "IMP3438_0_3437_metric_mixing",
            "prior_row": "AN3437_3_metric_mixing",
            "before_status": "RETAINED",
            "after_status": "SCHUR_ALPHA_TEMPLATE_READY_VALUES_MISSING",
            "impact": "metric mixing is no longer vague; it is B_i O_X^{-1} B_i^dagger Schur leakage",
            "valid_for_claim": False,
        },
        {
            "impact_id": "IMP3438_1_R10_range",
            "prior_row": "PPRS3434_7_R10_range",
            "before_status": "BLOCKED_CURVE_AND_SOURCE_MAP_MISSING",
            "after_status": "BLOCKED_BUT_SOURCE_MAP_REFINED",
            "impact": "R10 source map now includes Qbar_i_S_gX and qbar_i_T_gX from Hessian mixing",
            "valid_for_claim": False,
        },
        {
            "impact_id": "IMP3438_2_gamma_beta",
            "prior_row": "PPRS3434_0_gamma/PPRS3434_1_beta",
            "before_status": "BLOCKED_MAP_VALUES_MISSING",
            "after_status": "NON_EH_SCHUR_VECTOR_RETAINED",
            "impact": "same Schur term can shift gamma/beta if it has massless or long-enough support",
            "valid_for_claim": False,
        },
        {
            "impact_id": "IMP3438_3_Newton",
            "prior_row": "source-normalized Poisson/Newton branch",
            "before_status": "range residual retained",
            "after_status": "finite-pole not absorbable into G0",
            "impact": "if B_i finite-pole survives, Newton is inverse-square plus Yukawa residual, not pure GR reduction",
            "valid_for_claim": False,
        },
    ]


def residual_counterexamples() -> list[dict[str, Any]]:
    return [
        {
            "counterexample_id": "CEX3438_0_scalar_tensor",
            "construction": "EH metric plus a scalar X with h-X trace mixing",
            "why_decoupling_fails": "direct matter X charge can be zero while the matter trace sources h and h sources X",
            "required_blocker": "B_trace,X=0 or scalar pole absent",
            "valid_for_claim": False,
        },
        {
            "counterexample_id": "CEX3438_1_R2_auxiliary",
            "construction": "higher-curvature/R2 auxiliary scalar integrated into the metric operator",
            "why_decoupling_fails": "matter couples to metric; the metric propagator contains an extra scalar pole",
            "required_blocker": "primitive minimality/no-higher-derivative theorem or coefficient bound",
            "valid_for_claim": False,
        },
        {
            "counterexample_id": "CEX3438_2_boundary_tail",
            "construction": "bulk B_i=0 but boundary/projector readout tail has source projection",
            "why_decoupling_fails": "exterior force sees surface/readout charge",
            "required_blocker": "zero boundary flux/projector orthogonality",
            "valid_for_claim": False,
        },
        {
            "counterexample_id": "CEX3438_3_no_pole_only",
            "construction": "X_i is auxiliary but elimination leaves local higher-derivative metric terms",
            "why_decoupling_fails": "no Yukawa pole may still leave PPN beta/gamma operators",
            "required_blocker": "EH operator selection plus local higher-operator bound",
            "valid_for_claim": False,
        },
    ]


def score_readiness() -> list[dict[str, Any]]:
    return [
        {
            "score_id": "SR3438_0_schur_law",
            "item": "metric-mixing Schur source law",
            "before_status": "retained vague metric mixing",
            "after_status": "DERIVED_FORMAL_OPERATOR_LAW_NONCLAIM",
            "score_readiness": "formula-ready but value-missing",
            "valid_for_claim": False,
        },
        {
            "score_id": "SR3438_1_decoupling",
            "item": "nonmetric decoupling proof",
            "before_status": "not attempted at 3437",
            "after_status": "CONDITIONAL_CRITERIA_WRITTEN_NOT_SIGNED",
            "score_readiness": "not score-ready; B_i or projector orthogonality missing",
            "valid_for_claim": False,
        },
        {
            "score_id": "SR3438_2_alpha_template",
            "item": "metric-mixing alpha numerator",
            "before_status": "AN3437_3 retained",
            "after_status": "TEMPLATE_READY_VALUES_MISSING",
            "score_readiness": "first explicit operator-entry template exists",
            "valid_for_claim": False,
        },
        {
            "score_id": "SR3438_3_R10_claim",
            "item": "R10 comparison",
            "before_status": "blocked",
            "after_status": "blocked with sharper missing inputs",
            "score_readiness": "no claim until B_i/Z/M/projections/readout/bound curve are sourced",
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PG3438_0_derivation",
            "gate": "Schur complement metric-mixing law derived",
            "result": "PASS_FORMAL_NONCLAIM",
            "evidence": "SCH3438_2/SCH3438_3",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3438_1_decoupling",
            "gate": "metric/X decoupling is proved for MTS",
            "result": "BLOCKED",
            "evidence": "NDC3438_0/NDC3438_1/NDC3438_2 not parent-signed",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3438_2_alpha_numerator",
            "gate": "first explicit alpha numerator template exists",
            "result": "PASS_TEMPLATE_NONCLAIM",
            "evidence": "MMAT3438_0",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3438_3_R10",
            "gate": "R10 alpha(lambda) can be scored",
            "result": "BLOCKED_VALUES_AND_BOUND_CURVE",
            "evidence": "OP3438 rows missing plus 3436 bound curve gate",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3438_4_local_GR",
            "gate": "local GR/Newton reduction is derived",
            "result": "BLOCKED",
            "evidence": "finite pole/nonEH/PPN/source-normalization rows remain active",
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3438_0_progress",
            "decision": "Metric mixing is now an exact Schur-complement residual law, not a handwave.",
            "reason": "Direct matter current zero does not prevent h-sourced X unless B_i or the pole vanishes.",
            "next_action": "source or zero the parent Hessian block B_i",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3438_1_no_claim",
            "decision": "Do not claim nonmetric decoupling or R10/local-GR pass.",
            "reason": "B_i, Z_i/M_i^2, source/test projectors, Xi_R10, tau_i and tails are not parent-signed.",
            "next_action": "build block-diagonal parent Hessian proof or first B_i input row",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3438_2_best_next",
            "decision": "Attack B_i directly.",
            "reason": "B_i=0 is the least-scrutiny route; if it fails, B_i becomes the numerator leg for R10/PPN.",
            "next_action": "3439 block-diagonal parent Hessian or first B_HX source row",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3439-Y5-R2FR-block-diagonal-parent-Hessian-or-first-BHX-source-row-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3439_block_diagonal_parent_Hessian_or_first_BHX_source_row.py",
            "objective": "try to prove B_i=delta^2 S_parent/(delta h_H delta X_i)=0 in the identity-coframe local branch; if not, stage the first source-ready B_HX operator row for R10/PPN scoring",
            "success_condition": "a parent-signed block-diagonal theorem candidate for one finite channel, or a nonclaim B_HX input row with normalization, units, affected arena, and source path requirements",
            "valid_for_claim": False,
        }
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3438_0",
            "status": "METRIC_MIXING_SCHUR_LAW_DERIVED_ALPHA_TEMPLATE_NONCLAIM",
            "claim_allowed": False,
            "reason": "formal Schur law and template exist, but operator coefficients and decoupling premises are missing",
            "next_safe_action": "derive or source B_i before any R10/PPN/local-GR promotion",
            "valid_for_claim": False,
        }
    ]


def all_generated_nonclaim(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for output_name, rows in rows_by_name.items():
        if output_name == "validation":
            continue
        for row in rows:
            if "valid_for_claim" in row and str(row["valid_for_claim"]).lower() != "false":
                return False
            if "claim_allowed" in row and str(row["claim_allowed"]).lower() != "false":
                return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], start_utc: datetime) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    theorem_rows = rows_by_name["metric_mixing_schur_theorem"]
    decoupling_rows = rows_by_name["nonmetric_decoupling_conditions"]
    alpha_rows = rows_by_name["metric_mixing_alpha_template"]
    input_rows = rows_by_name["operator_input_rows"]
    promotion_rows = rows_by_name["promotion_gates"]
    next_rows = rows_by_name["next_target"]
    modified_count = 0
    if FORMALIZATION.exists():
        start_timestamp = start_utc.timestamp()
        modified_count = sum(
            1 for checked_path in FORMALIZATION.rglob("*") if checked_path.is_file() and checked_path.stat().st_mtime >= start_timestamp
        )
    validations = [
        {
            "check_id": "VAL3438_0_sources_exist",
            "condition": "all cited source paths exist",
            "passed": all(row["exists"] for row in source_rows),
            "detail": f"{sum(1 for row in source_rows if row['exists'])}/{len(source_rows)} source paths exist",
        },
        {
            "check_id": "VAL3438_1_outputs_scoped",
            "condition": "all outputs are in post-checkpoint-work",
            "passed": all(str(path).startswith(str(ROOT)) for path in OUTPUTS.values()),
            "detail": str(ROOT),
        },
        {
            "check_id": "VAL3438_2_nonclaim",
            "condition": "all generated rows remain nonclaim",
            "passed": all_generated_nonclaim(rows_by_name),
            "detail": "valid_for_claim=false and claim_allowed=false throughout generated rows",
        },
        {
            "check_id": "VAL3438_3_schur_law",
            "condition": "metric-mixing Schur source law is derived",
            "passed": any(row["theorem_id"] == "SCH3438_2_induced_source" and row["status"] == "SCHUR_SOURCE_LAW_DERIVED_NONCLAIM" for row in theorem_rows),
            "detail": "J_i^{gX}=B_i^dagger G_H J_H",
        },
        {
            "check_id": "VAL3438_4_decoupling_not_promoted",
            "condition": "nonmetric decoupling remains blocked unless B_i/no-pole/orthogonality is signed",
            "passed": any(row["condition_id"] == "NDC3438_0_block_diagonal_hessian" and row["current_status"] == "NOT_PARENT_SIGNED" for row in decoupling_rows)
            and any(row["gate_id"] == "PG3438_1_decoupling" and row["result"] == "BLOCKED" for row in promotion_rows),
            "detail": "B_i block diagonal theorem not signed",
        },
        {
            "check_id": "VAL3438_5_alpha_template",
            "condition": "first metric-mixing alpha numerator template exists",
            "passed": any(row["template_id"] == "MMAT3438_0_operator_form" and row["status"] == "TEMPLATE_ONLY_INPUTS_MISSING" for row in alpha_rows),
            "detail": "alpha_i^{gX} operator template written",
        },
        {
            "check_id": "VAL3438_6_required_inputs_missing",
            "condition": "B_i/Z/M/projector/readout inputs are explicit blockers",
            "passed": len(input_rows) >= 6 and all(str(row["current_status"]).startswith(("MISSING", "CONDITIONAL")) for row in input_rows),
            "detail": f"{len(input_rows)} operator input rows retained",
        },
        {
            "check_id": "VAL3438_7_next_target",
            "condition": "next target attacks B_i parent Hessian",
            "passed": "BHX" in next_rows[0]["target_doc"] or "B_HX" in next_rows[0]["objective"],
            "detail": next_rows[0]["target_doc"],
        },
        {
            "check_id": "VAL3438_8_formalization_untouched",
            "condition": "formalization-workbench modified-file count remains 0 during this run",
            "passed": modified_count == 0,
            "detail": f"modified_count_since_start={modified_count}",
        },
    ]
    validations.append(
        {
            "check_id": "VAL3438_9_overall",
            "condition": "3438 metric-mixing checkpoint is internally valid",
            "passed": all(row["passed"] for row in validations),
            "detail": "PASS" if all(row["passed"] for row in validations) else "FAIL",
        }
    )
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    text = f"""# 3438 - Metric Mixing to Alpha Numerator or Nonmetric Decoupling Proof

## Summary
- This checkpoint takes the next leap after 3437: even if the direct matter vertex is zero, matter can still source finite `X_i` through the metric/X Hessian block.
- The result is the exact Schur-complement law: `J_i^gX = B_i^dagger G_H J_H`, and the metric propagator gets `O_H^eff = O_H - B_i O_X^{-1} B_i^dagger`.
- Therefore nonmetric decoupling requires a real parent statement: `B_i=0`, source-projector orthogonality, no finite pole, or zero boundary/projector tails.
- If those are not signed, the R10 numerator is explicit rather than vague: `alpha_i^gX = Xi_R10 tau_i [Qbar_i^S,gX qbar_i^T,gX/(4 pi G0 Z_i)+alpha_i^tail]`.
- No R10/Newton/local-GR claim is made, but the next missing object is now brutally specific: the parent Hessian block `B_i`.

## Source Register
{md_table(rows_by_name["source_register"])}

## Metric-Mixing Schur Theorem
{md_table(rows_by_name["metric_mixing_schur_theorem"])}

## Nonmetric Decoupling Conditions
{md_table(rows_by_name["nonmetric_decoupling_conditions"])}

## Metric-Mixing Alpha Template
{md_table(rows_by_name["metric_mixing_alpha_template"])}

## Operator Input Rows
{md_table(rows_by_name["operator_input_rows"])}

## PPN/R10 Impact Update
{md_table(rows_by_name["ppn_r10_impact_update"])}

## Residual Counterexamples
{md_table(rows_by_name["residual_counterexamples"])}

## Score Readiness
{md_table(rows_by_name["score_readiness"])}

## Promotion Gates
{md_table(rows_by_name["promotion_gates"])}

## Decision Ledger
{md_table(rows_by_name["decision_ledger"])}

## Next Target
{md_table(rows_by_name["next_target"])}

## Runner Nonclaim
{md_table(rows_by_name["runner_nonclaim"])}

## Validation
{md_table(rows_by_name["validation"])}

## Bottom Line
This moves the ladder: direct matter coupling is no longer the only question. The decisive local-GR question is now whether the parent Hessian is block diagonal between the EH metric source mode and finite nonmetric modes. If yes, the clean branch gets much stronger. If no, `B_i` becomes the first real alpha numerator leg.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    start_utc = datetime.now(timezone.utc)
    rows_by_name = {
        "source_register": source_register(),
        "metric_mixing_schur_theorem": metric_mixing_schur_theorem(),
        "nonmetric_decoupling_conditions": nonmetric_decoupling_conditions(),
        "metric_mixing_alpha_template": metric_mixing_alpha_template(),
        "operator_input_rows": operator_input_rows(),
        "ppn_r10_impact_update": ppn_r10_impact_update(),
        "residual_counterexamples": residual_counterexamples(),
        "score_readiness": score_readiness(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    rows_by_name["validation"] = validation_rows(rows_by_name, start_utc)
    for output_name, rows in rows_by_name.items():
        write_csv(OUTPUTS[output_name], rows)
    write_doc(rows_by_name)
    failed_rows = [row for row in rows_by_name["validation"] if not row["passed"]]
    if failed_rows:
        raise SystemExit(f"3438 validation failed: {failed_rows}")
    print(f"wrote {DOC}")
    print(f"wrote {len(OUTPUTS)} csv outputs")


if __name__ == "__main__":
    main()
