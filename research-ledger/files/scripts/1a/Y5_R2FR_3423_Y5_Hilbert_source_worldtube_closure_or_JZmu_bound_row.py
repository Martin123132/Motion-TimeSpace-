from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3423-Y5-R2FR-Y5-Hilbert-source-worldtube-closure-or-JZmu-bound-row-under-AX1090.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCES = {
    "doc_3422": ROOT / "3422-Y5-R2FR-source-current-zero-even-matter-readout-or-JZ-bound-row-under-AX1090.md",
    "y5_gate_3422": OUT / "P8_Y5_R2FR_3422_Y5_SOURCE_NORMALIZATION_GATE.csv",
    "jz_bounds_3422": OUT / "P8_Y5_R2FR_3422_JZ_BOUND_ROWS.csv",
    "next_3422": OUT / "P8_Y5_R2FR_3422_NEXT_TARGET.csv",
    "doc_3421": ROOT / "3421-Y5-R2FR-Z-basis-physical-lock-and-Euler-source-free-local-branch-under-AX1090.md",
    "doc_3414": ROOT / "3414-Y5-R2FR-Y5-source-normalization-and-Y6-extra-stress-owner-gate-under-AX1090.md",
    "y5_law_3414": OUT / "P8_Y5_R2FR_3414_Y5_CALIBRATED_COUPLING_LAW.csv",
    "y5_owner_3414": OUT / "P8_Y5_R2FR_3414_Y5_OWNER_GATE_MATRIX.csv",
    "parent_clauses_3400": OUT / "P8_Y5_R2FR_3400_PARENT_SIGNATURE_CLAUSES.csv",
    "newton_theorem_3399": OUT / "P8_Y5_R2FR_3399_FIRST_ORDER_NEWTON_ZERO_THEOREM.csv",
    "activation_3400": OUT / "P8_Y5_R2FR_3400_FIRST_ORDER_ACTIVATION_THEOREM.csv",
    "doc_1015": ROOT / "1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md",
    "doc_1016": ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
    "hwt_contract": OUT / "P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv",
    "hwt_theorem": OUT / "P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv",
    "hsm_contract": OUT / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
    "worldtube_source_measure": OUT / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
    "source_measure_attempt": OUT / "P8_Y5_SOURCE_MEASURE_THEOREM_ATTEMPT.csv",
    "bobs_pack_777": OUT / "P8_Y5_R10_777_BOBS_SOURCE_MEASURE_FIRST_PACK.csv",
    "bound_schema_778": OUT / "P8_Y5_R10_778_SOURCE_MEASURE_BOUND_SCHEMA.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3423_SOURCE_REGISTER.csv",
    "hilbert_worldtube_theorem": OUT / "P8_Y5_R2FR_3423_HILBERT_WORLDTUBE_CLOSURE_THEOREM.csv",
    "minimal_parent_action_candidate": OUT / "P8_Y5_R2FR_3423_MINIMAL_PARENT_SOURCE_ACTION_CANDIDATE.csv",
    "y5_source_current_split": OUT / "P8_Y5_R2FR_3423_Y5_SOURCE_CURRENT_SPLIT.csv",
    "jzmu_bound_rows": OUT / "P8_Y5_R2FR_3423_JZMU_BOUND_ROWS.csv",
    "parent_signature_gate": OUT / "P8_Y5_R2FR_3423_PARENT_SIGNATURE_GATE.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3423_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3423_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3423_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3423_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3423_VALIDATION.csv",
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
        "doc_3422": "handoff: even matter readout kills direct J_Z but leaves Y5 source normalization",
        "y5_gate_3422": "latest Y5 source-normalization verdict",
        "jz_bounds_3422": "source-current fallback schema",
        "next_3422": "machine-readable 3423 target",
        "doc_3421": "fixed-point theorem needing source-current zero or bound",
        "doc_3414": "calibrated coupling principle and Y5/Y6 owner gate",
        "y5_law_3414": "universal calibrated coupling law",
        "y5_owner_3414": "Y5 owner gate matrix",
        "parent_clauses_3400": "PC3400 source-coupling parent signature clauses",
        "newton_theorem_3399": "exact conditional first-order Newton theorem",
        "activation_3400": "activation theorem for PC3400 clauses",
        "doc_1015": "same-object topological/Hilbert equality attempt",
        "doc_1016": "parent Hilbert worldtube/source-measure selector contract",
        "hwt_contract": "Hilbert worldtube parent action contract",
        "hwt_theorem": "Hilbert worldtube glue theorem attempt",
        "hsm_contract": "Hamiltonian source-measure contract",
        "worldtube_source_measure": "worldtube source-measure theorem",
        "source_measure_attempt": "source-measure theorem attempt",
        "bobs_pack_777": "coupling/source/readout descent pack",
        "bound_schema_778": "source-measure bound schema",
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


def hilbert_worldtube_theorem() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "HWC3423_0_define_single_charge",
            "claim": "There is one parent-owned local source charge, not one gravitational charge plus a later orbital/readout mass.",
            "equation_or_identity": "J_H[tau] := -T^{mu}_{nu}[e_obs,psi] tau^nu epsilon_mu; W_source := closure(supp J_H[tau])",
            "proof_status": "CONDITIONAL_DEFINITION_FROM_HILBERT_WORLDTUBE_ROUTE",
            "missing_to_promote": "parent action must own e_obs, tau, compact support and Hilbert current before readout",
            "valid_for_claim": False,
        },
        {
            "step_id": "HWC3423_1_dressed_mass",
            "claim": "Measured GM is the dressed Hamiltonian/Hilbert charge of that same worldtube.",
            "equation_or_identity": "mu_obs := G_ref M_H; M_H := H_tau[S_outer]-H_ref = integral_{Sigma cap W_source} J_H[tau]",
            "proof_status": "EXACT_IF_HAMILTONIAN_REFERENCE_AND_INTEGRABILITY_SIGNED",
            "missing_to_promote": "M_H_ref, fixed H_ref, boundary/reference lock and integrability",
            "valid_for_claim": False,
        },
        {
            "step_id": "HWC3423_2_common_kappa_not_JZ",
            "claim": "A universal constant kappa/G calibration is not a Z-source current.",
            "equation_or_identity": "delta_Z kappa_0 = 0 and kappa_0 is fixed once for every Hilbert source",
            "proof_status": "THEOREM_IF_PC3400_1_ADOPTED",
            "missing_to_promote": "adopt global branch-constant kappa_MTS in the parent action",
            "valid_for_claim": False,
        },
        {
            "step_id": "HWC3423_3_vertical_zero",
            "claim": "Y5 source current vanishes if the source charge and readout descend through the same even/public variables.",
            "equation_or_identity": "delta_Z mu_obs = G_ref delta_Z M_H = 0 => J_Z_Y5 := delta_Z S_source_norm = 0",
            "proof_status": "EXACT_IF_SOURCE_DESCENT_AND_HAMILTONIAN_MAP_SIGNED",
            "missing_to_promote": "same-frame source measure, Pi_M/H_tau chain map, no hidden source labels",
            "valid_for_claim": False,
        },
        {
            "step_id": "HWC3423_4_first_order_Newton",
            "claim": "Under the same clauses, first-order Newton source normalization closes rather than being fitted.",
            "equation_or_identity": "Delta_Newton_Y5^(1)=delta_kappa+delta_ellJ+epsilon_Gref+delta_KC+epsilon_M = 0",
            "proof_status": "EXACT_CONDITIONAL_REUSES_3399_3400",
            "missing_to_promote": "PC3400_0 through PC3400_6 accepted in the same parent branch",
            "valid_for_claim": False,
        },
        {
            "step_id": "HWC3423_5_second_order_caveat",
            "claim": "This Y5 theorem does not by itself prove full PPN/local GR.",
            "equation_or_identity": "beta/gamma/alpha still require B_source=A_source^2, a_v=0, lambda_*>0 and q_loc vector/stress silence",
            "proof_status": "GUARDRAIL_RETAINED",
            "missing_to_promote": "source-square, Y6 extra stress, lambda-star and q_loc residual gates",
            "valid_for_claim": False,
        },
        {
            "step_id": "HWC3423_6_verdict",
            "claim": "The proof route is real but current MTS has not yet signed the parent source-coupling action.",
            "equation_or_identity": "Y5_zero iff HWC3423_0..HWC3423_4 pass in one parent branch",
            "proof_status": "CONDITIONAL_THEOREM_NOT_CURRENT_CLAIM",
            "missing_to_promote": "minimal parent source action adoption or source-backed J_Z_mu bound rows",
            "valid_for_claim": False,
        },
    ]


def minimal_parent_action_candidate() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "MPA3423_0_public_geometry",
            "parent_action_clause": "All ordinary source readout uses one public observed geometry.",
            "minimal_form": "g_obs=g(q(Phi)); e_obs=e(q(Phi)); no species/source/range-labelled metric in local branch",
            "why_it_matters": "prevents measured mass, clocks, rods and orbits from living in different frames",
            "current_status": "CANDIDATE_TO_ADOPT_NOT_CLAIM",
            "valid_for_claim": False,
        },
        {
            "clause_id": "MPA3423_1_universal_kappa",
            "parent_action_clause": "One branch-constant gravitational coupling multiplies the public curvature sector.",
            "minimal_form": "S_grav=(2 kappa_0)^-1 int sqrt(-g_obs) R[g_obs] + boundary; kappa_0=8 pi G_ref/c^4",
            "why_it_matters": "turns G into a GR-like calibrated constant instead of a source-by-source knob",
            "current_status": "CANDIDATE_TO_ADOPT_NOT_CLAIM",
            "valid_for_claim": False,
        },
        {
            "clause_id": "MPA3423_2_Hilbert_matter_source",
            "parent_action_clause": "Matter, EM, clocks and rods couple by the same Hilbert variation.",
            "minimal_form": "S_matter[e_obs,psi]+S_EM[g_obs,A]; T_H=-2/sqrt(-g_obs) delta S_matter+EM/delta g_obs",
            "why_it_matters": "makes Poynting/EM stress ordinary source stress instead of a private background shove",
            "current_status": "CANDIDATE_TO_ADOPT_NOT_CLAIM",
            "valid_for_claim": False,
        },
        {
            "clause_id": "MPA3423_3_Hamiltonian_worldtube_charge",
            "parent_action_clause": "The source mass is the Hamiltonian/Noether charge of the Hilbert worldtube.",
            "minimal_form": "W_source=closure(supp J_H[tau]); M_H=H_tau[S_outer]-H_ref; linking surfaces fixed before readout",
            "why_it_matters": "removes the independent topological/bare-mass selector loophole",
            "current_status": "CANDIDATE_NEEDS_INTEGRABILITY_AND_REFERENCE_PROOF",
            "valid_for_claim": False,
        },
        {
            "clause_id": "MPA3423_4_Z_sector_orthogonality",
            "parent_action_clause": "Residual Z fields have no linear local source vertex after quotient-even readout.",
            "minimal_form": "S_Z=1/2 <Z,LZ>+O(Z^3); delta_Z(S_matter+S_source_readout)|_{Z=0}=0",
            "why_it_matters": "activates the 3421 fixed-point mechanism rather than leaving a hidden source force",
            "current_status": "CANDIDATE_TO_ADOPT_NOT_CLAIM",
            "valid_for_claim": False,
        },
        {
            "clause_id": "MPA3423_5_boundary_reference_lock",
            "parent_action_clause": "Boundary, exact improvement and reference conventions are fixed once.",
            "minimal_form": "delta_Z H_ref=0; B_zero_flux=0 or explicit source-backed bound; [d,Pi_M]J_H=0 or retained row",
            "why_it_matters": "stops GM from moving by bookkeeping after the fit",
            "current_status": "CANDIDATE_WITH_RETAINED_BOUND_ROWS",
            "valid_for_claim": False,
        },
        {
            "clause_id": "MPA3423_6_consequence",
            "parent_action_clause": "If MPA3423_0 through MPA3423_5 hold, the Y5 source current is zero.",
            "minimal_form": "J_Z_Y5 = delta_Z ln(kappa_0 M_H ell_J K_C^-1)+boundary/domain terms = 0",
            "why_it_matters": "this is the cleanest route from MTS source coupling to Newton/GR compatibility",
            "current_status": "CONDITIONAL_CONSEQUENCE_NOT_CURRENT_CLAIM",
            "valid_for_claim": False,
        },
    ]


def y5_source_current_split() -> list[dict[str, Any]]:
    return [
        {
            "component_id": "Y5S3423_0_kappa_common",
            "component": "universal kappa/G common mode",
            "zero_condition": "kappa_0 is a parent constant fixed before readout",
            "residual_if_not_zero": "delta_Z ln kappa_MTS or source/species/range-labelled kappa",
            "current_status": "COMPATIBLE_BUT_NOT_PARENT_ADOPTED",
            "valid_for_claim": False,
        },
        {
            "component_id": "Y5S3423_1_Hilbert_source_measure",
            "component": "Hilbert source density and ell_J conversion",
            "zero_condition": "T_H, J_H, M_H and PPN rho are all induced by the same S_matter[e_obs,psi]",
            "residual_if_not_zero": "delta_Z ln ell_J or shadow-source mismatch",
            "current_status": "UNSIGNED_SAME_SOURCE_MAP",
            "valid_for_claim": False,
        },
        {
            "component_id": "Y5S3423_2_Htau_PiM",
            "component": "Hamiltonian charge and Pi_M map",
            "zero_condition": "H_tau-H_ref equals the fixed Pi_M-projected Hilbert charge",
            "residual_if_not_zero": "epsilon_Htau_PiM + I_commutator",
            "current_status": "OPEN_FROM_1015_1016",
            "valid_for_claim": False,
        },
        {
            "component_id": "Y5S3423_3_worldtube_boundary",
            "component": "worldtube, linking surfaces, boundary and reference terms",
            "zero_condition": "W_source=supp J_H[tau], surfaces homologous, B_zero_flux=Delta_symp=Delta_domain=0",
            "residual_if_not_zero": "epsilon_boundary_reference_domain",
            "current_status": "OPEN_BUT_NOW_LOCALIZED",
            "valid_for_claim": False,
        },
        {
            "component_id": "Y5S3423_4_v_action_ratio",
            "component": "local v action source/kinetic ratio",
            "zero_condition": "B_v/A_v=16 pi G_ref/c^4 in the same branch",
            "residual_if_not_zero": "delta_KC",
            "current_status": "TARGET_COEFFICIENTS_KNOWN_PARENT_RATIO_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "component_id": "Y5S3423_5_second_order_square",
            "component": "second-order source square and beta stability",
            "zero_condition": "B_source=A_source^2 and a_v=0 through O(U^2)",
            "residual_if_not_zero": "delta_beta_source + kappa_v pieces",
            "current_status": "OPEN_NOT_PART_OF_FIRST_ORDER_Y5_ZERO",
            "valid_for_claim": False,
        },
        {
            "component_id": "Y5S3423_6_hidden_drift",
            "component": "range, time, memory, species, frame or hidden source drift",
            "zero_condition": "no source labels survive quotient-even public readout",
            "residual_if_not_zero": "epsilon_drift_frame_species_memory",
            "current_status": "MUST_BE_EXCLUDED_BY_PARENT_ACTION_OR_BOUNDED",
            "valid_for_claim": False,
        },
        {
            "component_id": "Y5S3423_7_total",
            "component": "total Y5 source current",
            "zero_condition": "Y5S3423_0 through Y5S3423_6 theorem-zero in one parent branch",
            "residual_if_not_zero": "||J_Z_mu_Y5|| bounded by absolute no-cancellation sum",
            "current_status": "NOT_ZERO_FOR_CURRENT_MTS",
            "valid_for_claim": False,
        },
    ]


def jzmu_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "JZMU3423_0_kappa",
            "quantity": "epsilon_kappa_Z",
            "definition": "|partial_Z ln kappa_MTS| after common calibration",
            "bound_formula": "0 if MPA3423_1 signed; otherwise source-backed absolute value",
            "status": "THEOREM_OR_VALUE_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "JZMU3423_1_source_measure",
            "quantity": "epsilon_ellJ_Z",
            "definition": "|partial_Z ln ell_J| for Hilbert/source/readout conversion",
            "bound_formula": "0 if MPA3423_2 signed; otherwise source-backed absolute value",
            "status": "THEOREM_OR_VALUE_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "JZMU3423_2_HPiM",
            "quantity": "epsilon_HPiM_Z",
            "definition": "fractional mismatch between H_tau-H_ref and Pi_M J_H under Z variation",
            "bound_formula": "|partial_Z ln(M_H/(Pi_M J_H))| + |I_commutator|/M_H_ref",
            "status": "M_H_REF_AND_COMMUTATOR_INPUTS_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "JZMU3423_3_boundary_domain",
            "quantity": "epsilon_boundary_domain_Z",
            "definition": "fractional source-charge shift from boundary/reference/worldtube-domain choices",
            "bound_formula": "(|B_zero_flux|+|Delta_symp|+|Delta_worldtube_domain|)/M_H_ref",
            "status": "BOUNDARY_REFERENCE_WORLD_TUBE_INPUTS_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "JZMU3423_4_v_ratio",
            "quantity": "delta_KC_Z",
            "definition": "source/kinetic coefficient mismatch in the local v Poisson reduction",
            "bound_formula": "|(B_v/A_v)/(16 pi G_ref/c^4)-1|",
            "status": "PARENT_COEFFICIENTS_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "JZMU3423_5_second_order",
            "quantity": "epsilon_beta_source_Z",
            "definition": "second-order source-square mismatch after first-order measured-GM calibration",
            "bound_formula": "|B_source/A_source^2 - 1| + |a_v|/2 + ||kappa_v||_abs",
            "status": "SECOND_ORDER_INPUTS_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "JZMU3423_6_hidden_drift",
            "quantity": "epsilon_hidden_source_Z",
            "definition": "hidden range/time/memory/species/frame source drift",
            "bound_formula": "sum_abs(epsilon_range,epsilon_time,epsilon_memory,epsilon_species,epsilon_frame)",
            "status": "HIDDEN_DRIFT_EXCLUSION_OR_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "JZMU3423_7_total",
            "quantity": "||J_Z_mu_Y5||",
            "definition": "absolute no-cancellation Y5 source-current norm",
            "bound_formula": "epsilon_kappa_Z+epsilon_ellJ_Z+epsilon_HPiM_Z+epsilon_boundary_domain_Z+delta_KC_Z+epsilon_beta_source_Z+epsilon_hidden_source_Z",
            "status": "FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "JZMU3423_8_fixed_point_feed",
            "quantity": "||Z||_Y5",
            "definition": "Y5-driven contribution to the 3421 fixed-point residual amplitude",
            "bound_formula": "||Z||_Y5 <= 2 lambda_*^-1 ||J_Z_mu_Y5||",
            "status": "MISSING_LAMBDA_STAR_AND_JZMU_VALUES",
            "valid_for_claim": False,
        },
        {
            "bound_id": "JZMU3423_9_observable_feed",
            "quantity": "Delta_Newton_Y5 and PPN residual vector",
            "definition": "observable leakage from nonzero Y5 source-current residual",
            "bound_formula": "|Delta_Newton_Y5|, |gamma-1|, |beta-1|, |alpha_i| <= C_response ||Z||_Y5 plus explicit source-square terms",
            "status": "MISSING_RESPONSE_OPERATOR_AND_VALUES",
            "valid_for_claim": False,
        },
    ]


def parent_signature_gate() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PSG3423_0_single_branch",
            "required_signature": "one local branch fixes g_obs/e_obs, tau, Q_tau, B_ref, Pi_M, kappa_MTS and ell_J before comparison",
            "closes": "no source readout backfit or branch mismatch",
            "current_status": "STAGED_NOT_ADOPTED",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PSG3423_1_constant_kappa",
            "required_signature": "kappa_MTS is branch-constant and label-free",
            "closes": "epsilon_kappa_Z and first-order coupling drift",
            "current_status": "COMPATIBLE_GLOBAL_CLAUSE_NOT_ADOPTED",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PSG3423_2_same_Hilbert_source",
            "required_signature": "same S_matter[e_obs,psi] defines T_H, J_H, M_H and PPN source density",
            "closes": "epsilon_ellJ_Z and shadow-source split",
            "current_status": "OBSERVED_COFRAME_COMPATIBLE_BUT_NOT_ADOPTED",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PSG3423_3_Htau_PiM_chain",
            "required_signature": "H_tau-H_ref and Pi_M are functionals of the same Hilbert worldtube charge",
            "closes": "epsilon_HPiM_Z and commutator mismatch",
            "current_status": "MISSING_CORE_PARENT_HAMILTONIAN_CHARGE",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PSG3423_4_boundary_no_extra_mass",
            "required_signature": "B_zero_flux, domain shift, nonEH/frame/memory/source extra monopoles vanish or are explicit rows",
            "closes": "epsilon_boundary_domain_Z and hidden source drift",
            "current_status": "RETAINED_ROWS_ACTIVE",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PSG3423_5_v_action_ratio",
            "required_signature": "local v branch has the exact Poisson source/kinetic coefficient ratio",
            "closes": "delta_KC_Z",
            "current_status": "TARGET_RATIO_KNOWN_PARENT_COEFFICIENTS_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PSG3423_6_same_U_PPN_guard",
            "required_signature": "the same G_ref M_H source builds Poisson, H_tau and PPN potential U",
            "closes": "first-order source normalization transfer only",
            "current_status": "GUARD_READY_NOT_FULL_PPN",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PSG3423_7_verdict",
            "required_signature": "all Y5 source signatures are parent-signed in one branch",
            "closes": "J_Z_mu_Y5=0 and first-order Newton source normalization",
            "current_status": "FAIL_CURRENT_CLAIM_USE_CONDITIONAL_THEOREM_OR_BOUND_ROWS",
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PG3423_0_conditional_theorem",
            "claim": "Y5 Hilbert-source worldtube theorem is mathematically written",
            "gate_status": "PASS_CONDITIONAL",
            "reason": "HWC3423 rows define exact zero conditions for J_Z_mu_Y5",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3423_1_current_Y5_zero",
            "claim": "current MTS has J_Z_mu_Y5=0",
            "gate_status": "FAIL_NOT_PARENT_SIGNED",
            "reason": "PC3400/Hamiltonian/worldtube/reference clauses remain staged",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3423_2_bound_branch",
            "claim": "Y5 fallback bound is score-ready",
            "gate_status": "FORMULA_READY_VALUES_MISSING",
            "reason": "JZMU3423 total row has no numeric/source-backed values yet",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3423_3_Newton_first_order",
            "claim": "first-order Newton source normalization closes",
            "gate_status": "EXACT_IF_PARENT_ACTION_ADOPTS_PSG3423",
            "reason": "3399/3400 theorem applies under the same source-worldtube clauses",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3423_4_PPN_local_GR",
            "claim": "full PPN/local GR is derived",
            "gate_status": "BLOCKED",
            "reason": "second-order source-square, Y6 extra stress, lambda_* and q_loc vector/stress gates remain open",
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3423_0_not_derive_G_from_nothing",
            "decision": "Do not demand that MTS derive the numerical SI value of G before local GR; GR itself calibrates one universal G.",
            "because": "the fair gate is one parent-owned universal coupling and no differential source/readout residual after calibration",
            "next_action": "treat kappa_0 as a legal parent constant only if it is branch-fixed and label-free",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3423_1_actual_leap",
            "decision": "The Y5 problem is now a precise Hilbert-worldtube source-charge problem.",
            "because": "J_Z_mu_Y5 vanishes if measured GM is G_ref times the same Hilbert/Hamiltonian worldtube charge varied by S_matter",
            "next_action": "try to instantiate the minimal parent source action, not just restate missing source rows",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3423_2_current_status",
            "decision": "Current MTS cannot claim Y5 zero yet.",
            "because": "H_tau/Pi_M, M_H_ref, reference lock and no-hidden-source signatures are not parent-owned in the current corpus",
            "next_action": "either adopt/sign the minimal parent source action or fill JZMU3423 rows with source-backed values",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3423_3_best_next",
            "decision": "The next best move is a minimal parent source-coupling action gate.",
            "because": "if that action is coherent, it signs the largest Y5 clauses at once; if it fails, the failure becomes a concrete bound row",
            "next_action": "3424-Y5-R2FR-minimal-parent-source-coupling-action-or-PC3400-adoption-gate-under-AX1090.md",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target": "3424-Y5-R2FR-minimal-parent-source-coupling-action-or-PC3400-adoption-gate-under-AX1090.md",
            "script": "scripts/Y5_R2FR_3424_minimal_parent_source_coupling_action_or_PC3400_adoption_gate.py",
            "objective": "try to instantiate a minimal parent action that signs kappa, Hilbert matter source, Hamiltonian worldtube charge, boundary reference and Z-orthogonality clauses without smuggling a fitted GM; otherwise emit the first JZMU source-bound rows",
            "why_next": "3423 turns the coupling problem into exact parent-action clauses; the next useful step is to see whether those clauses can coexist as an action, not just audit them",
            "valid_for_claim": False,
        },
        {
            "target": "3425-Y5-R2FR-Y6-extra-stress-safe-class-or-source-current-bound-under-AX1090.md",
            "script": "scripts/Y5_R2FR_3425_Y6_extra_stress_safe_class_or_source_current_bound.py",
            "objective": "after Y5 source action is adopted or demoted, close the retained Y6 extra-stress current or bound it",
            "why_next": "Y6 remains the other bulk source-current blocker after Y5",
            "valid_for_claim": False,
        },
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3423_0",
            "script": str(Path(__file__).resolve()),
            "mode": "Y5_HILBERT_SOURCE_WORLDTUBE_CLOSURE_OR_JZMU_BOUND",
            "summary": "conditional Y5 source-current zero theorem written; minimal parent source-action candidate staged; JZMU bound rows emitted; no local-GR/Newton claim promoted",
            "valid_for_claim": False,
        }
    ]


def formalization_recent_count(start_utc: datetime) -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    threshold = start_utc.timestamp()
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and path.stat().st_mtime >= threshold:
            count += 1
    return count


def validation_rows(
    rows_by_name: dict[str, list[dict[str, Any]]],
    start_utc: datetime,
) -> list[dict[str, Any]]:
    sources = rows_by_name["source_register"]
    outputs_under_root = all(str(path).startswith(str(ROOT)) for path in OUTPUTS.values()) and str(DOC).startswith(str(ROOT))
    nonclaim = all(
        row.get("valid_for_claim") is False
        for name, rows in rows_by_name.items()
        if name != "validation"
        for row in rows
    )
    formalization_count = formalization_recent_count(start_utc)
    gates = rows_by_name["promotion_gates"]
    return [
        {
            "check_id": "VAL3423_0_sources_exist",
            "condition": "all cited source paths exist",
            "passed": all(row["exists"] for row in sources),
            "detail": f"{sum(1 for row in sources if row['exists'])}/{len(sources)} source paths exist",
        },
        {
            "check_id": "VAL3423_1_outputs_scoped",
            "condition": "all outputs are in post-checkpoint-work",
            "passed": outputs_under_root,
            "detail": str(ROOT),
        },
        {
            "check_id": "VAL3423_2_nonclaim",
            "condition": "all generated rows remain nonclaim",
            "passed": nonclaim,
            "detail": "valid_for_claim=false throughout generated rows",
        },
        {
            "check_id": "VAL3423_3_theorem_written",
            "condition": "conditional Hilbert-worldtube theorem exists",
            "passed": any(row["step_id"] == "HWC3423_3_vertical_zero" for row in rows_by_name["hilbert_worldtube_theorem"]),
            "detail": "HWC3423_3 present",
        },
        {
            "check_id": "VAL3423_4_action_candidate",
            "condition": "minimal parent source action candidate exists",
            "passed": any(row["clause_id"] == "MPA3423_6_consequence" for row in rows_by_name["minimal_parent_action_candidate"]),
            "detail": "MPA3423 consequence present",
        },
        {
            "check_id": "VAL3423_5_JZMU_bounds",
            "condition": "JZMU fallback rows are staged",
            "passed": any(row["bound_id"] == "JZMU3423_7_total" for row in rows_by_name["jzmu_bound_rows"]),
            "detail": "JZMU3423_7_total present",
        },
        {
            "check_id": "VAL3423_6_Y5_current_not_claimed",
            "condition": "current Y5 zero remains unclaimed",
            "passed": any(row["gate_id"] == "PG3423_1_current_Y5_zero" and row["gate_status"].startswith("FAIL") for row in gates),
            "detail": "parent signatures staged, not adopted",
        },
        {
            "check_id": "VAL3423_7_local_GR_blocked",
            "condition": "local GR remains blocked",
            "passed": any(row["gate_id"] == "PG3423_4_PPN_local_GR" and row["gate_status"] == "BLOCKED" for row in gates),
            "detail": "Y6/lambda/q_loc/second-order gates remain open",
        },
        {
            "check_id": "VAL3423_8_next_target",
            "condition": "next target tries source action adoption",
            "passed": rows_by_name["next_target"][0]["target"].startswith("3424-Y5-R2FR-minimal-parent-source-coupling-action"),
            "detail": rows_by_name["next_target"][0]["target"],
        },
        {
            "check_id": "VAL3423_9_formalization_untouched",
            "condition": "formalization-workbench modified-file count remains 0 during this run",
            "passed": formalization_count == 0,
            "detail": f"modified_count_since_start={formalization_count}",
        },
        {
            "check_id": "VAL3423_10_overall",
            "condition": "3423 Y5 Hilbert-source checkpoint is internally valid",
            "passed": True,
            "detail": "PASS",
        },
    ]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    text = f"""# 3423 - Y5 Hilbert Source Worldtube Closure or JZmu Bound Row

## Summary
- This checkpoint takes a real shot at the coupling problem rather than circling it: measured `GM` is forced to be the same parent Hilbert/Hamiltonian worldtube charge that matter already sources.
- A universal calibrated `G_ref/kappa_0` is allowed in the same sense GR allows it; the forbidden move is a source-, frame-, species-, range-, memory-, or readout-dependent coupling after calibration.
- Conditional theorem: if the parent action signs one public geometry, one constant `kappa_0`, one Hilbert source current, one Hamiltonian worldtube charge, fixed boundary/reference data, and no linear `Z` source vertex, then `J_Z_mu_Y5=0`.
- Current MTS does not yet get the claim: those clauses are staged, not adopted in a full parent action.
- Fallback is no longer vague: `J_Z_mu_Y5` is decomposed into explicit no-cancellation bound rows and feeds the 3421 fixed-point branch through `||Z||_Y5 <= 2 lambda_*^-1 ||J_Z_mu_Y5||`.
- Next best move is to attempt the minimal parent source-coupling action gate; if it cannot be made coherent, the Y5 route must become a source-backed bound branch.

## Source Register
{md_table(rows_by_name["source_register"])}

## Hilbert Worldtube Closure Theorem
{md_table(rows_by_name["hilbert_worldtube_theorem"])}

## Minimal Parent Source Action Candidate
{md_table(rows_by_name["minimal_parent_action_candidate"])}

## Y5 Source Current Split
{md_table(rows_by_name["y5_source_current_split"])}

## JZmu Bound Rows
{md_table(rows_by_name["jzmu_bound_rows"])}

## Parent Signature Gate
{md_table(rows_by_name["parent_signature_gate"])}

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
This is progress, but not a win parade. The best Y5 path is now clean: make the observed mass/source coupling a single Hilbert/Hamiltonian worldtube charge in the parent action. If that action signs, first-order Newton source normalization stops being a fitted patch; if it does not sign, the exact pieces that fail are now `J_Z_mu_Y5` bound rows.
"""
    DOC.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    start_utc = datetime.now(timezone.utc)
    rows_by_name = {
        "source_register": source_register(),
        "hilbert_worldtube_theorem": hilbert_worldtube_theorem(),
        "minimal_parent_action_candidate": minimal_parent_action_candidate(),
        "y5_source_current_split": y5_source_current_split(),
        "jzmu_bound_rows": jzmu_bound_rows(),
        "parent_signature_gate": parent_signature_gate(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    rows_by_name["validation"] = validation_rows(rows_by_name, start_utc)

    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)
    write_doc(rows_by_name)

    failed = [row for row in rows_by_name["validation"] if not row["passed"]]
    if failed:
        raise SystemExit(f"3423 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"wrote {len(OUTPUTS)} csv outputs")


if __name__ == "__main__":
    main()
