from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3421-Y5-R2FR-Z-basis-physical-lock-and-Euler-source-free-local-branch-under-AX1090.md"

Q_PROXY = 7.432631961576971e-06
ALPHA3_PRODUCT_LIMIT = 5.381673706808059e-15

SOURCES = {
    "doc_3420": ROOT / "3420-Y5-R2FR-boundary-projector-harmonic-and-no-vector-spurion-silence-gate-under-AX1090.md",
    "next_3420": OUT / "P8_Y5_R2FR_3420_NEXT_TARGET.csv",
    "hodge_3420": OUT / "P8_Y5_R2FR_3420_HODGE_BOUNDARY_SILENCE_THEOREM.csv",
    "promotion_3420": OUT / "P8_Y5_R2FR_3420_PROMOTION_GATES.csv",
    "kmetric_3419": OUT / "P8_Y5_R2FR_3419_RESPONSE_DOUBLET_KMETRIC_EXPANSION.csv",
    "promotion_3419": OUT / "P8_Y5_R2FR_3419_PROMOTION_GATES.csv",
    "vector_zero_3418": OUT / "P8_Y5_R2FR_3418_VECTOR_ZERO_DERIVATION.csv",
    "doublet_action_3413": OUT / "P8_Y5_R2FR_3413_RESPONSE_DOUBLET_ACTION.csv",
    "double_zero_3413": OUT / "P8_Y5_R2FR_3413_DOUBLE_ZERO_PROOF.csv",
    "coverage_3413": OUT / "P8_Y5_R2FR_3413_COMPONENT_COVERAGE_MATRIX.csv",
    "source_neutrality_3413": OUT / "P8_Y5_R2FR_3413_SOURCE_NEUTRALITY_GATES.csv",
    "candidate_ranking_3412": OUT / "P8_Y5_R2FR_3412_CONSTRUCTION_CANDIDATE_RANKING.csv",
    "variation_517": OUT / "P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv",
    "euler_source_517": OUT / "P8_RESPONSE_DOUBLET_EULER_SOURCE_LEDGER.csv",
    "obstruction_517": OUT / "P8_RESPONSE_DOUBLET_OBSTRUCTION_LEDGER.csv",
    "theorem_1011": OUT / "P8_Y5_R10_1011_RESPONSED_DOUBLET_THEOREM_ATTEMPT.csv",
    "qloc_bounds_1011": OUT / "P8_Y5_R10_1011_QLOC_BOUND_FILL_ROWS.csv",
    "component_map_1282": OUT / "P8_Y5_R10_1282_RESPONSE_DOUBLET_COMPONENT_MAP_AUDIT.csv",
    "adoption_gate_2967": OUT / "P8_Y5_R2FR_2967_RESPONSE_DOUBLET_ADOPTION_GATE.csv",
    "owner_lock_2977": OUT / "P8_Y5_R2FR_2977_RESPONSE_DOUBLET_OWNER_LOCK_AUDIT.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3421_SOURCE_REGISTER.csv",
    "euler_fixed_point_theorem": OUT / "P8_Y5_R2FR_3421_EULER_FIXED_POINT_THEOREM.csv",
    "z_basis_lock_matrix": OUT / "P8_Y5_R2FR_3421_Z_BASIS_PHYSICAL_LOCK_MATRIX.csv",
    "source_current_zero_gate": OUT / "P8_Y5_R2FR_3421_SOURCE_CURRENT_ZERO_GATE.csv",
    "coercivity_bound_pack": OUT / "P8_Y5_R2FR_3421_COERCIVITY_BOUND_PACK.csv",
    "residual_fallback_rows": OUT / "P8_Y5_R2FR_3421_RESIDUAL_FALLBACK_ROWS.csv",
    "local_gr_consequence": OUT / "P8_Y5_R2FR_3421_LOCAL_GR_CONSEQUENCE.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3421_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3421_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3421_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3421_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3421_VALIDATION.csv",
}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields = list(rows[0].keys())

    def cell(value: Any) -> str:
        return str(value).replace("|", "/").replace("\n", " ")

    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(cell(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def source_register() -> list[dict[str, Any]]:
    roles = {
        "doc_3420": "boundary/projector/harmonic gate selecting 3421 bulk Euler/Z-basis target",
        "next_3420": "machine-readable 3421 target",
        "hodge_3420": "boundary theorem depends on future Euler/Z-basis closure",
        "promotion_3420": "local GR blocked pending 3421 and flux/projector gates",
        "kmetric_3419": "response-doublet Kmetric expansion and Z-basis risk",
        "promotion_3419": "Z-basis/Euler gate named as blocker",
        "vector_zero_3418": "q_loc vector-zero requires source-free local solutions",
        "doublet_action_3413": "response-doublet quadratic density template",
        "double_zero_3413": "formal double-zero and positive/source-free Euler caveat",
        "coverage_3413": "Y0-Y6 physical residual coverage map",
        "source_neutrality_3413": "source neutrality gates for double-zero promotion",
        "candidate_ranking_3412": "response-doublet density is primary formal candidate",
        "variation_517": "Euler equation and energy identity for response doublet",
        "euler_source_517": "Y0-Y6 source-current obstructions",
        "obstruction_517": "Y5/Y6/PPN/boundary obstructions",
        "theorem_1011": "earlier response-doublet theorem attempt and blockers",
        "qloc_bounds_1011": "fallback q_loc bound rows",
        "component_map_1282": "response doublet component map audit",
        "adoption_gate_2967": "response-doublet adoption gate",
        "owner_lock_2977": "response-doublet owner lock audit",
    }
    return [
        {
            "source_id": key,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[key],
            "valid_for_claim": False,
        }
        for key, path in SOURCES.items()
    ]


def euler_fixed_point_theorem() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "EFT3421_0_parent_density",
            "claim": "Use the adopted parent-response branch with Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B+O(Z^3/Z^4).",
            "derivation": "3413/3419 response-doublet density gives a variational action and Khat=Kmetric in the adopted branch.",
            "requires": "explicit parent branch, fixed sign/volume convention and background Gamma0 subtraction",
            "current_status": "PASS_CONDITIONAL_PARENT_BRANCH",
            "valid_for_claim": False,
        },
        {
            "step_id": "EFT3421_1_Euler_equation",
            "claim": "The local Z Euler equation has the form L_AB Z^B + N_A(Z)=J_A+B_A.",
            "derivation": "delta_Z S_GK gives M_AB Z^B plus derivative/operator terms L_AB, nonlinear remainder N_A, source current J_A and boundary work B_A.",
            "requires": "field domain, operator L_AB, source current J_A and boundary functional B_A identified",
            "current_status": "FORMULA_DERIVED_AS_CONTRACT",
            "valid_for_claim": False,
        },
        {
            "step_id": "EFT3421_2_coercive_energy",
            "claim": "If L is positive/coercive after gauge quotient, source-free local solutions obey an energy inequality.",
            "derivation": "lambda_* ||Z||^2 <= <Z,LZ> = <Z,J+B-N(Z)> on the fixed local domain.",
            "requires": "lambda_*>0, self-adjoint domain, gauge zero modes removed and nonlinear term controlled",
            "current_status": "THEOREM_CONTRACT_NOT_NUMERIC",
            "valid_for_claim": False,
        },
        {
            "step_id": "EFT3421_3_zero_branch",
            "claim": "If J_A=0, B_A=0 and N_A(0)=0 with small-field coercivity, Z=0 is the unique local fixed point.",
            "derivation": "energy identity gives lambda_*||Z||^2 <= c_N||Z||^3; in the local small branch only ||Z||=0 remains if c_N||Z||<lambda_*.",
            "requires": "J_Z/B_Z zero theorem, local small-field branch and positive Hessian",
            "current_status": "EXACT_CONDITIONAL_FIXED_POINT",
            "valid_for_claim": False,
        },
        {
            "step_id": "EFT3421_4_bound_branch",
            "claim": "If sources/boundary work do not vanish, the theory gets a norm bound rather than a GR claim.",
            "derivation": "for nonlinear Lipschitz L_N <= lambda_*/2, ||Z|| <= 2(lambda_*^-1)(||J||+||B||+||R_proj||).",
            "requires": "lambda_*, source norms, boundary norms, projector residual norms and observable response map",
            "current_status": "BOUND_FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "step_id": "EFT3421_5_qloc_implication",
            "claim": "If Z=0 is physically locked to q_loc/Y5/Y6/PPN residuals, the bulk q_loc source is theorem-zero.",
            "derivation": "Z=0 kills the physical residual basis; then 3418/3420 vector-zero route has no bulk Euler source term.",
            "requires": "Z-basis physical lock matrix full-rank and complete through tested local-GR order",
            "current_status": "BLOCKED_BY_PHYSICAL_LOCK_AND_SOURCE_CURRENT",
            "valid_for_claim": False,
        },
    ]


def z_basis_lock_matrix() -> list[dict[str, Any]]:
    return [
        {
            "lock_id": "ZLM3421_0_q_loc_vector",
            "physical_channel": "q_loc^nu vector/scalar residual",
            "Z_candidate": "Z_q^nu normalized to P_loc(nabla^nu Gamma_eff-nabla_mu Khat^{mu nu})",
            "lock_requirement": "full-rank map from Z_q to q_parallel, D chi_q, q_T and q_harmonic through O(U^2)",
            "current_status": "PARTIAL_FROM_3418_3420_NOT_FULL_BULK_LOCK",
            "residual_if_fail": "epsilon_q_loc_bulk",
            "valid_for_claim": False,
        },
        {
            "lock_id": "ZLM3421_1_PPN_metric",
            "physical_channel": "gamma-1, beta-1, alpha_i, xi, zeta_i, Gdot/R11 local response",
            "Z_candidate": "Z_PPN^A",
            "lock_requirement": "source-backed response operator DeltaPPN_A = R_A{}B Z^B with no null physical residual",
            "current_status": "NOT_DERIVED_NO_RESPONSE_OPERATOR",
            "residual_if_fail": "Delta_PPN_unlocked",
            "valid_for_claim": False,
        },
        {
            "lock_id": "ZLM3421_2_Y5_source_normalization",
            "physical_channel": "measured GM/source normalization/Newtonian source strength",
            "Z_candidate": "Z_mu",
            "lock_requirement": "source normalization offsets are odd/local-zero or bounded; no exchange-even measured-GM drift",
            "current_status": "FAILS_CURRENT_ROUTE_EXCHANGE_EVEN_SOURCE_SCALAR",
            "residual_if_fail": "epsilon_Y5_source_normalization",
            "valid_for_claim": False,
        },
        {
            "lock_id": "ZLM3421_3_Y6_extra_stress",
            "physical_channel": "extra stress / non-EH conserved stress",
            "Z_candidate": "Z_T",
            "lock_requirement": "extra stress is topological/invisible/gapped no-hair or generated by Z and killed at Z=0",
            "current_status": "NOT_DERIVED_CONSERVED_KERNEL_POSSIBLE",
            "residual_if_fail": "epsilon_Y6_extra_stress",
            "valid_for_claim": False,
        },
        {
            "lock_id": "ZLM3421_4_boundary_projector",
            "physical_channel": "boundary/harmonic/projector/domain residual",
            "Z_candidate": "Z_B, Z_P, Z_H",
            "lock_requirement": "boundary and projector residuals are included in Z or separately zeroed by 3420",
            "current_status": "CONDITIONAL_ON_3420_GATES",
            "residual_if_fail": "epsilon_boundary_projector",
            "valid_for_claim": False,
        },
        {
            "lock_id": "ZLM3421_5_matter_readout",
            "physical_channel": "matter, clocks, rods, photons and source readout",
            "Z_candidate": "Z_readout",
            "lock_requirement": "matter/readout action descends through even quotient variables only: delta_Z S_matter=0",
            "current_status": "FAIL_OPEN_MATTER_DESCENT",
            "residual_if_fail": "epsilon_matter_readout_Z",
            "valid_for_claim": False,
        },
        {
            "lock_id": "ZLM3421_6_verdict",
            "physical_channel": "full local-GR residual vector",
            "Z_candidate": "Z^A full basis",
            "lock_requirement": "Z=0 iff all physical local residuals vanish in tested arenas",
            "current_status": "COMPONENT_LOCK_NOT_CLOSED",
            "residual_if_fail": "Delta_Z_physical_lock",
            "valid_for_claim": False,
        },
    ]


def source_current_zero_gate() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "SCZ3421_0_exchange_symmetry",
            "source_term": "linear odd source J_A Z^A",
            "zero_condition": "exact parent exchange symmetry E:Z->-Z covers the action, matter/source/readout and boundary terms",
            "current_status": "CONDITIONAL_TEMPLATE_ONLY",
            "if_fail": "J_Z_exchange",
            "valid_for_claim": False,
        },
        {
            "gate_id": "SCZ3421_1_even_matter_readout",
            "source_term": "matter/clocks/rods/source readout variation with respect to Z",
            "zero_condition": "S_matter=S_matter[psi,e_obs(R_even)] so delta_Z S_matter=0",
            "current_status": "NOT_DERIVED_HARD_FOR_Y5",
            "if_fail": "J_Z_matter_readout",
            "valid_for_claim": False,
        },
        {
            "gate_id": "SCZ3421_2_Y5_source",
            "source_term": "measured-GM/source-normalization current",
            "zero_condition": "all source-normalization offsets are either even universal calibration already absorbed into GR kappa or odd residuals killed by Z=0",
            "current_status": "FAIL_CURRENT_Y5",
            "if_fail": "J_Z_Y5_source_normalization",
            "valid_for_claim": False,
        },
        {
            "gate_id": "SCZ3421_3_Y6_stress",
            "source_term": "extra stress/Bianchi-conserved current",
            "zero_condition": "extra stress is public Hilbert source, topological exact, gapped no-hair, or Z-generated and zero at branch",
            "current_status": "RETAINED_Y6_DEBT",
            "if_fail": "J_Z_Y6_extra_stress",
            "valid_for_claim": False,
        },
        {
            "gate_id": "SCZ3421_4_boundary_work",
            "source_term": "boundary/collar/source work B_A",
            "zero_condition": "3420 no-flux and fixed boundary reference pass",
            "current_status": "CONDITIONAL_ON_3420_NOT_PARENT_SIGNED",
            "if_fail": "B_Z_boundary_work",
            "valid_for_claim": False,
        },
        {
            "gate_id": "SCZ3421_5_operator_kernel",
            "source_term": "zero modes/gauge kernel and non-coercive directions",
            "zero_condition": "gauge/constraint quotient removes nulls and lambda_*>0 on physical residual space",
            "current_status": "MISSING_COERCIVITY_CERTIFICATE",
            "if_fail": "Z_kernel_residual",
            "valid_for_claim": False,
        },
        {
            "gate_id": "SCZ3421_6_verdict",
            "source_term": "total Z source work",
            "zero_condition": "SCZ3421_0 through SCZ3421_5 pass",
            "current_status": "SOURCE_FREE_EULER_BRANCH_NOT_CLOSED",
            "if_fail": "J_Z_total_plus_B_Z",
            "valid_for_claim": False,
        },
    ]


def coercivity_bound_pack() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "CBP3421_0_energy_identity",
            "quantity": "Z_norm",
            "formula": "lambda_* ||Z||^2 <= <Z,J_Z+B_Z+R_proj-N(Z)>",
            "needed_inputs": "lambda_*, J_Z norm, B_Z norm, projector residual norm, nonlinear Lipschitz radius",
            "current_status": "FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "CBP3421_1_small_branch",
            "quantity": "small-field fixed-point radius",
            "formula": "if Lip(N)<=lambda_*/2 then ||Z|| <= 2 lambda_*^-1 (||J_Z||+||B_Z||+||R_proj||)",
            "needed_inputs": "coercivity lower bound and source/boundary/projector norms",
            "current_status": "BOUND_READY_NOT_NUMERIC",
            "valid_for_claim": False,
        },
        {
            "bound_id": "CBP3421_2_zero_switch",
            "quantity": "Z=0 theorem switch",
            "formula": "theorem_zero=true iff lambda_*>0 and J_Z=B_Z=R_proj=0 in the physical Z basis",
            "needed_inputs": "parent-signed coercivity, source-current zero, boundary/projector zero and component lock",
            "current_status": "ZERO_SWITCH_NOT_ACTIVE",
            "valid_for_claim": False,
        },
        {
            "bound_id": "CBP3421_3_q_loc_map",
            "quantity": "q_loc residual from Z",
            "formula": "||q_loc|| <= C_qZ ||Z|| + epsilon_boundary_projector",
            "needed_inputs": "C_qZ response operator and boundary/projector envelope",
            "current_status": "MISSING_C_QZ_RESPONSE_OPERATOR",
            "valid_for_claim": False,
        },
        {
            "bound_id": "CBP3421_4_alpha3_map",
            "quantity": "alpha3 from Z/vector leakage",
            "formula": "|alpha3_q| <= Q_PROXY * (C_alphaZ ||Z|| + epsilon_V_total)",
            "needed_inputs": "C_alphaZ, Z_norm bound, epsilon_V_total and alpha3 arena bound",
            "current_status": "MISSING_ALPHA_RESPONSE_OPERATOR",
            "valid_for_claim": False,
        },
    ]


def residual_fallback_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "RFR3421_0_JZ_total",
            "residual": "J_Z_total",
            "definition": "absolute norm of all nonzero source currents driving the Z Euler equation",
            "arena": "q_loc;PPN;source-normalization;clock/orbital",
            "status": "MISSING_SOURCE_CURRENT_ZERO_OR_NORM",
            "valid_for_claim": False,
        },
        {
            "row_id": "RFR3421_1_Y5",
            "residual": "epsilon_Y5_source_normalization",
            "definition": "measured-GM/source-normalization piece not killed by exchange-odd Z doublet",
            "arena": "Newtonian source;R11;PPN beta;Gdot/orbital",
            "status": "HARD_FAIL_CURRENT_ROUTE",
            "valid_for_claim": False,
        },
        {
            "row_id": "RFR3421_2_Y6",
            "residual": "epsilon_Y6_extra_stress",
            "definition": "conserved/topological/hidden extra stress not generated and zeroed by Z",
            "arena": "local GR;PPN;EM stress;orbital",
            "status": "RETAINED_STRESS_DEBT",
            "valid_for_claim": False,
        },
        {
            "row_id": "RFR3421_3_physical_lock",
            "residual": "Delta_Z_physical_lock",
            "definition": "null physical residual not represented by the Z basis",
            "arena": "all local-GR observables",
            "status": "MISSING_FULL_RANK_COMPONENT_MAP",
            "valid_for_claim": False,
        },
        {
            "row_id": "RFR3421_4_coercivity",
            "residual": "lambda_*^-1",
            "definition": "inverse coercivity controlling how source work becomes residual amplitude",
            "arena": "all residual bounds",
            "status": "MISSING_POSITIVE_OPERATOR_CONSTANT",
            "valid_for_claim": False,
        },
        {
            "row_id": "RFR3421_5_bound_verdict",
            "residual": "Z_bound_to_observables",
            "definition": "||Z|| bound pushed through q_loc/PPN/Y5/Y6 response operators",
            "arena": "local-GR acceptance gates",
            "status": "BOUND_SCHEMA_READY_NOT_SCORE_READY",
            "valid_for_claim": False,
        },
    ]


def local_gr_consequence() -> list[dict[str, Any]]:
    return [
        {
            "consequence_id": "LGC3421_0_best_case",
            "claim": "If Z-basis lock, coercivity, source-current zero and 3420 boundary/projector gates all pass, q_loc bulk and vector lanes are theorem-zero.",
            "status": "REAL_DERIVATION_ROUTE",
            "why_not_claim": "Z-basis physical lock, J_Z=0, Y5/Y6 and coercivity are not parent-signed",
            "valid_for_claim": False,
        },
        {
            "consequence_id": "LGC3421_1_current_state",
            "claim": "Current MTS has a strong conditional fixed-point theorem but not a local-GR derivation.",
            "status": "CONDITIONAL_THEOREM_PLUS_RESIDUAL_BOUND_SCHEMA",
            "why_not_claim": "Y5 source normalization and Y6 stress can remain exchange-even/nonzero",
            "valid_for_claim": False,
        },
        {
            "consequence_id": "LGC3421_2_fallback",
            "claim": "If source-current zero fails, MTS must bound J_Z_total and propagate it to PPN/R11/local tests.",
            "status": "BOUND_BRANCH_REQUIRED_IF_NOT_DERIVED",
            "why_not_claim": "numeric/source-backed J_Z and response operators are missing",
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PG3421_0_fixed_point_theorem",
            "gate": "Euler/coercive fixed-point theorem is mathematically written",
            "current_result": "PASS_CONDITIONAL_THEOREM",
            "promotes_if": "not a claim gate alone",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3421_1_Z_basis_lock",
            "gate": "Z=0 equals physical q_loc/PPN/Y5/Y6/source/stress zero",
            "current_result": "BLOCKED_COMPONENT_LOCK_NOT_CLOSED",
            "promotes_if": "ZLM3421_0 through ZLM3421_6 pass",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3421_2_source_current_zero",
            "gate": "J_Z and B_Z vanish in the local branch",
            "current_result": "BLOCKED_Y5_Y6_SOURCE_CURRENT",
            "promotes_if": "SCZ3421_0 through SCZ3421_6 pass",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3421_3_coercivity",
            "gate": "positive/coercive operator after gauge quotient",
            "current_result": "BLOCKED_MISSING_LAMBDA_STAR",
            "promotes_if": "lambda_*>0 with units/domain/source path",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3421_4_bound_branch",
            "gate": "if not zero, source-current residuals are bounded into observables",
            "current_result": "FORMULA_READY_VALUES_MISSING",
            "promotes_if": "J_Z/B_Z/lambda_*/response operators are numeric or theorem-zero",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3421_5_q_loc_vector_zero",
            "gate": "q_loc vector projection is theorem-zero",
            "current_result": "BLOCKED_PENDING_3420_AND_3421_GATES",
            "promotes_if": "3420 and PG3421_1 through PG3421_3 pass",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3421_6_local_GR",
            "gate": "local GR/Newton/PPN branch is derived",
            "current_result": "BLOCKED",
            "promotes_if": "q_loc vector-zero plus retained beta/source/stress/nonEH envelopes close",
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3421_0_leap_made",
            "finding": "The actual derivation leap is now written: coercive Euler plus zero source/boundary work forces Z=0.",
            "evidence": "EFT3421_1 through EFT3421_4 provide equation, energy identity, zero branch and bound branch.",
            "action": "Use this as the core local fixed-point mechanism.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3421_1_not_enough",
            "finding": "Formal double-zero is not enough unless Z is the physical residual vector.",
            "evidence": "ZLM3421 keeps Y5, Y6, PPN and matter/readout lock open.",
            "action": "Do not claim local GR until the physical lock matrix closes.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3421_2_hard_block",
            "finding": "Y5 source normalization and Y6 extra stress remain the hardest bulk source-current blockers.",
            "evidence": "SCZ3421_2 and SCZ3421_3 fail/open from prior source ledgers.",
            "action": "Attack source-current zero/even matter readout next before more alpha arithmetic.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3421_3_fallback",
            "finding": "If J_Z cannot be proved zero, the theory must become a source-current bound branch.",
            "evidence": "CBP3421 gives ||Z|| <= 2 lambda_*^-1 (||J||+||B||+||R_proj||).",
            "action": "Fill J_Z/lambda/response operator rows if theorem route fails.",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3422-Y5-R2FR-source-current-zero-even-matter-readout-or-JZ-bound-row-under-AX1090.md",
            "script": "scripts/Y5_R2FR_3422_source_current_zero_even_matter_readout_or_JZ_bound_row.py",
            "objective": "prove delta_Z S_matter=0 and J_Z=0 for source/readout/Y5/Y6 channels in the adopted parent branch; otherwise emit source-current bound rows",
            "why_next": "3421 shows the fixed-point theorem is real, but it activates only if J_Z/B_Z vanish or are bounded",
            "valid_for_claim": False,
        },
        {
            "target_id": "3423-Y5-R2FR-positive-operator-lambda-star-or-Znorm-bound-runner-under-AX1090.md",
            "script": "scripts/Y5_R2FR_3423_positive_operator_lambda_star_or_Znorm_bound_runner.py",
            "objective": "prove lambda_*>0 after gauge quotient or stage a numeric/symbolic coercivity bound input pack",
            "why_next": "if source current is nonzero, lambda_* controls the residual amplitude and testability",
            "valid_for_claim": False,
        },
        {
            "target_id": "3424-Y5-R2FR-EM-Poynting-flux-zero-or-alpha-vector-bound-row-under-AX1090.md",
            "script": "scripts/Y5_R2FR_3424_EM_Poynting_flux_zero_or_alpha_vector_bound_row.py",
            "objective": "return to the Poynting vector gate if EM/wave flux remains in the local branch",
            "why_next": "3420 identified Poynting as an alpha-vector spurion, but 3421 source-current zero is higher leverage first",
            "valid_for_claim": False,
        },
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "run_id": "RUN3421_0",
            "script": str(Path(__file__).resolve()),
            "mode": "Z_BASIS_EULER_FIXED_POINT_AND_BOUND_SCHEMA",
            "result": "coercive Euler fixed-point theorem and Z-bound branch written; local GR remains blocked by physical Z-basis lock, J_Z/B_Z source-current zero, Y5/Y6 and lambda_* inputs",
            "valid_for_claim": False,
        }
    ]


def validation_rows(generated: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = generated["source_register"]
    all_sources_exist = all(row["exists"] for row in source_rows)
    scope_ok = all(str(path).startswith(str(ROOT)) and "formalization-workbench" not in str(path) for path in OUTPUTS.values())
    nonclaim = all(
        str(row.get("valid_for_claim", False)).lower() == "false"
        for key, rows in generated.items()
        if key != "validation"
        for row in rows
    )
    fixed_point = any(row["step_id"] == "EFT3421_3_zero_branch" for row in generated["euler_fixed_point_theorem"])
    bound_branch = any(row["step_id"] == "EFT3421_4_bound_branch" for row in generated["euler_fixed_point_theorem"])
    y5_flag = any(row["lock_id"] == "ZLM3421_2_Y5_source_normalization" and row["current_status"].startswith("FAILS") for row in generated["z_basis_lock_matrix"])
    jz_gate = any(row["gate_id"] == "SCZ3421_6_verdict" and row["current_status"] == "SOURCE_FREE_EULER_BRANCH_NOT_CLOSED" for row in generated["source_current_zero_gate"])
    local_gr_blocked = any(row["gate_id"] == "PG3421_6_local_GR" and row["current_result"] == "BLOCKED" for row in generated["promotion_gates"])
    next_jz = generated["next_target"][0]["target_id"].startswith("3422-Y5-R2FR-source-current-zero")

    rows = [
        {
            "check_id": "VAL3421_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": all_sources_exist,
            "detail": f"{sum(1 for row in source_rows if row['exists'])}/{len(source_rows)} source paths exist",
        },
        {
            "check_id": "VAL3421_1_scope",
            "check": "all outputs stay under post-checkpoint-work",
            "passed": scope_ok,
            "detail": str(ROOT),
        },
        {
            "check_id": "VAL3421_2_all_nonclaim",
            "check": "3421 does not claim local GR",
            "passed": nonclaim,
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "VAL3421_3_fixed_point",
            "check": "coercive zero-branch theorem exists",
            "passed": fixed_point,
            "detail": "EFT3421_3 present",
        },
        {
            "check_id": "VAL3421_4_bound_branch",
            "check": "nonzero source-current fallback bound exists",
            "passed": bound_branch,
            "detail": "EFT3421_4 present",
        },
        {
            "check_id": "VAL3421_5_Y5_flag",
            "check": "Y5 exchange-even/source-normalization blocker remains visible",
            "passed": y5_flag,
            "detail": "Y5 not silently zeroed by response doublet",
        },
        {
            "check_id": "VAL3421_6_source_current_block",
            "check": "source-free Euler branch remains blocked",
            "passed": jz_gate,
            "detail": "J_Z/B_Z zero not proved",
        },
        {
            "check_id": "VAL3421_7_local_GR_blocked",
            "check": "local GR remains blocked",
            "passed": local_gr_blocked,
            "detail": "physical Z lock, source current and coercivity gates open",
        },
        {
            "check_id": "VAL3421_8_next_target",
            "check": "next target attacks source-current zero",
            "passed": next_jz,
            "detail": generated["next_target"][0]["target_id"],
        },
    ]
    overall = all(row["passed"] for row in rows)
    rows.append(
        {
            "check_id": "VAL3421_9_overall",
            "check": "3421 Z-basis/Euler fixed-point checkpoint is internally valid",
            "passed": overall,
            "detail": "PASS" if overall else "FAIL",
        }
    )
    return rows


def build_doc(generated: dict[str, list[dict[str, Any]]]) -> str:
    return "\n\n".join(
        [
            "# 3421 - Z-Basis Physical Lock and Euler Source-Free Local Branch",
            "## Summary\n"
            "- This checkpoint derives the actual local fixed-point mechanism: a coercive Euler operator plus zero source/boundary work forces `Z=0` on the small local branch.\n"
            "- The theorem form is `L_AB Z^B + N_A(Z)=J_A+B_A`; if `lambda_*>0`, `J_A=0`, `B_A=0`, and nonlinear terms are controlled, then `Z=0` is the unique local fixed point.\n"
            "- If the zero theorem fails, the honest fallback is a bound: `||Z|| <= 2 lambda_*^-1 (||J_Z||+||B_Z||+||R_proj||)`.\n"
            "- The hard obstruction remains physical locking: `Z=0` must mean actual q_loc/PPN/Y5/Y6/source/stress residuals vanish, not merely auxiliary variables vanish.\n"
            "- Y5 source normalization and Y6 extra stress remain the biggest bulk blockers because they can be exchange-even or conserved while still observable.\n"
            "- Local GR is not claimed. Next strike is source-current zero/even matter readout, then lambda-star/coercivity.",
            "## Source Register\n" + md_table(generated["source_register"]),
            "## Euler Fixed-Point Theorem\n" + md_table(generated["euler_fixed_point_theorem"]),
            "## Z-Basis Physical Lock Matrix\n" + md_table(generated["z_basis_lock_matrix"]),
            "## Source-Current Zero Gate\n" + md_table(generated["source_current_zero_gate"]),
            "## Coercivity Bound Pack\n" + md_table(generated["coercivity_bound_pack"]),
            "## Residual Fallback Rows\n" + md_table(generated["residual_fallback_rows"]),
            "## Local-GR Consequence\n" + md_table(generated["local_gr_consequence"]),
            "## Promotion Gates\n" + md_table(generated["promotion_gates"]),
            "## Decision Ledger\n" + md_table(generated["decision_ledger"]),
            "## Next Target\n" + md_table(generated["next_target"]),
            "## Runner Nonclaim\n" + md_table(generated["runner_nonclaim"]),
            "## Validation\n" + md_table(generated["validation"]),
            "## Bottom Line\n"
            "This is a real derivation route, not a ledger loop: prove `J_Z=B_Z=0`, prove `lambda_*>0`, and prove the Z-basis is the physical local residual basis, then the local branch has teeth. "
            "If any of those fail, the framework must use the Z-norm bound branch and test it.",
        ]
    ) + "\n"


def main() -> None:
    if "formalization-workbench" in str(ROOT):
        raise RuntimeError(f"Refusing to run from formalization-workbench: {ROOT}")

    generated: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register(),
        "euler_fixed_point_theorem": euler_fixed_point_theorem(),
        "z_basis_lock_matrix": z_basis_lock_matrix(),
        "source_current_zero_gate": source_current_zero_gate(),
        "coercivity_bound_pack": coercivity_bound_pack(),
        "residual_fallback_rows": residual_fallback_rows(),
        "local_gr_consequence": local_gr_consequence(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    generated["validation"] = validation_rows(generated)

    for key, rows in generated.items():
        write_csv(OUTPUTS[key], rows)

    DOC.write_text(build_doc(generated), encoding="utf-8")

    if not all(str(row["passed"]).lower() == "true" for row in generated["validation"]):
        failed = [row for row in generated["validation"] if str(row["passed"]).lower() != "true"]
        raise SystemExit(f"3421 validation failed: {failed}")

    print(f"wrote {len(generated)} CSV artefacts and {DOC}")


if __name__ == "__main__":
    main()
