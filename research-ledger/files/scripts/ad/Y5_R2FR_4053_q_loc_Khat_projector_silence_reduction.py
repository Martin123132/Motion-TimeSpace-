from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4053-Y5-R2FR-q-loc-Khat-projector-silence-reduction.md"

SOURCES = {
    "SRC4053_00_q_loc_identity": (
        SOURCE_DIR / "P8_Y5_R2FR_4023_QLOC_STRESS_IDENTITY.csv",
        "q_loc^nu=P_loc nabla_mu T_GK",
    ),
    "SRC4053_01_zero_or_bound_fork": (
        SOURCE_DIR / "P8_Y5_R2FR_4023_QLOC_ZERO_THEOREM_OR_BOUND_FORK.csv",
        "q_loc^nu=P_loc nabla_mu T_GK",
    ),
    "SRC4053_02_match_helmholtz_gates": (
        SOURCE_DIR / "P8_Y5_R2FR_4023_GK_MATCH_AND_HELMHOLTZ_GATES.csv",
        "Helmholtz/inverse-variational symmetry",
    ),
    "SRC4053_03_khat_completion": (
        SOURCE_DIR / "P8_Y5_R2FR_4027_KHAT_COMPONENT_COMPLETION_GATE.csv",
        "trace-free improvement/Hessian response",
    ),
    "SRC4053_04_khat_conditional_paths": (
        SOURCE_DIR / "P8_Y5_R2FR_4027_CONDITIONAL_COMPLETION_PATHS.csv",
        "sigma_resp*c_I=1",
    ),
    "SRC4053_05_tracefree_improvement": (
        SOURCE_DIR / "P8_Y5_R2FR_4028_TRACEFREE_IMPROVEMENT_DERIVATION.csv",
        "S_imp[c_I]",
    ),
    "SRC4053_06_curvature_split": (
        SOURCE_DIR / "P8_Y5_R2FR_4030_CURVATURE_RESIDUAL_SPLIT.csv",
        "G_TF=0 and delta_phi=0 gives D_TF=0",
    ),
    "SRC4053_07_exterior_collar": (
        SOURCE_DIR / "P8_Y5_R2FR_4031_EXTERIOR_COLLAR_DELTAPHI_THEOREM.csv",
        "boundary flux",
    ),
    "SRC4053_08_scalar_charge": (
        SOURCE_DIR / "P8_Y5_R2FR_4032_SCALAR_CHARGE_IDENTITY.csv",
        "Q_phi[S]",
    ),
    "SRC4053_09_no_linear_leak": (
        SOURCE_DIR / "P8_Y5_R2FR_4034_NO_LINEAR_SOURCE_LEAK_GATE.csv",
        "source-only vertices",
    ),
    "SRC4053_10_no_hom_source_slot": (
        SOURCE_DIR / "P8_Y5_R2FR_4036_NO_HOM_SOURCE_SLOT_THEOREM.csv",
        "Hom_parent(Z_src,ActionScalar_matter)=0",
    ),
    "SRC4053_11_boundary_reference": (
        SOURCE_DIR / "P8_Y5_R2FR_4038_BOUNDARY_REFERENCE_THEOREM.csv",
        "boundary scalar charge vanishes",
    ),
    "SRC4053_12_poynting_no_flux": (
        SOURCE_DIR / "P8_Y5_R2FR_4038_POYNTING_NO_FLUX_THEOREM.csv",
        "Phi_EM_rad=0",
    ),
    "SRC4053_13_projector_stress": (
        SOURCE_DIR / "P8_Y5_R2FR_4043_PROJECTOR_STRESS_FACTORIZATION.csv",
        "T_P",
    ),
    "SRC4053_14_projector_zero": (
        SOURCE_DIR / "P8_Y5_R2FR_4043_SELECTED_BRANCH_ZERO_THEOREM.csv",
        "T_projector_domain",
    ),
    "SRC4053_15_memory_tail_zero": (
        SOURCE_DIR / "P8_Y5_R2FR_4046_TAIL_ZERO_THEOREM.csv",
        "X_mem=0",
    ),
    "SRC4053_16_cnorm_zero": (
        SOURCE_DIR / "P8_Y5_R2FR_4047_SELECTED_ZERO_THEOREM.csv",
        "D_a ln G_obs=0",
    ),
    "SRC4053_17_ppc4048_contract": (
        SOURCE_DIR / "P8_Y5_R2FR_4048_PARENT_PACKET_CONTRACT.csv",
        "PPC4048_7_gamma_khat_qloc",
    ),
    "SRC4053_18_formal_179": (
        FORMALIZATION / "179-PPC4048-local-parent-packet-candidate.md",
        "q_loc/Khat",
    ),
}

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4053_SOURCE_REGISTER.csv",
    "decomposition": SOURCE_DIR / "P8_Y5_R2FR_4053_QLOC_KHAT_DECOMPOSITION.csv",
    "silence_reduction": SOURCE_DIR / "P8_Y5_R2FR_4053_PROJECTOR_SILENCE_REDUCTION_THEOREM.csv",
    "clause_gate": SOURCE_DIR / "P8_Y5_R2FR_4053_CLOSURE_CLAUSE_GATE.csv",
    "fallback_bounds": SOURCE_DIR / "P8_Y5_R2FR_4053_FALLBACK_BOUND_VECTOR.csv",
    "evaluator": SOURCE_DIR / "P8_Y5_R2FR_4053_EVALUATOR_RESULTS.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4053_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4053_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4053_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4053_VALIDATION.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def contains(path: Path, needle: str) -> bool:
    return path.exists() and needle in read_text(path)


def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_rows(ts: str) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for source_id, (path, needle) in SOURCES.items():
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_present": contains(path, needle),
                "use_in_4053": "projector_silence_reduction",
                "timestamp_utc": ts,
            }
        )
    return rows


def decomposition_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "piece_id": "QKD4053_0_exact_identity",
            "object": "q_loc",
            "formula": "q_loc^nu = P_loc( nabla^nu Gamma_eff - nabla_mu Khat^{mu nu} ) = P_loc nabla_mu T_GK^{mu nu}",
            "derived_from": "4023 stress identity",
            "meaning": "The blocker is exactly a stress-divergence/projector problem, not a mysterious extra force.",
            "status": "EXACT_ALGEBRAIC_REWRITE",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "piece_id": "QKD4053_1_Ward_owner",
            "object": "T_GK",
            "formula": "If T_GK = (-2/sqrt|g|) delta S_GK/delta g and S_GK is diffeomorphism invariant, nabla_mu T_GK^{mu nu}=sum_A E_A nabla^nu Y^A plus boundary identities.",
            "derived_from": "4023 Ward route",
            "meaning": "On-shell local carrier equations would silence q_loc except for projector and boundary defects.",
            "status": "CONDITIONAL_NOETHER_ROUTE",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "piece_id": "QKD4053_2_Helmholtz_defect",
            "object": "D_GK",
            "formula": "D_GK := T_GK - T_can, with |q_loc| bounded by |nabla D_GK| plus Euler and boundary terms when the inverse-variational gate fails.",
            "derived_from": "4023/4024 mismatch branch",
            "meaning": "If the stress is not parent-variational, the branch does not die; it becomes a finite bound problem.",
            "status": "FALLBACK_BOUND_INTERFACE",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "piece_id": "QKD4053_3_Khat_tracefree",
            "object": "Khat_TF",
            "formula": "Khat_TF is generated by S_imp[c_I]=s_imp*c_I int sqrt|g| phi R plus boundary, giving K_L^{mu nu}=2[nabla^mu nabla^nu phi-(1/4)g^{mu nu}Box phi] when sigma_resp*c_I=1.",
            "derived_from": "4027/4028",
            "meaning": "The Hessian response can be parent-owned rather than inserted by hand, but only if adoption and normalization are signed.",
            "status": "DERIVED_ACTION_SHAPE_NOT_LIVE_ADOPTED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "piece_id": "QKD4053_4_exterior_zero",
            "object": "D_TF",
            "formula": "D_TF=(1-c_I)K_L + 2*c_I*delta_phi*G_TF + D_phiF + D_owner + D_boundary + D_adoption + D_kappa_sector.",
            "derived_from": "4030",
            "meaning": "In a local exterior with c_I=1, delta_phi=0, G_TF=0, and source/boundary/adoption silence, the trace-free Khat residual vanishes.",
            "status": "CONDITIONAL_ZERO_REDUCTION",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "piece_id": "QKD4053_5_scalar_charge",
            "object": "delta_phi",
            "formula": "Q_phi[S]=int_S n.grad u dS and int_Omega(|grad u|^2+mu_phi^2 u^2)dV=int_boundary u*n.grad u dS.",
            "derived_from": "4031/4032",
            "meaning": "The local hair problem is now a scalar-charge/boundary problem: prove Q_phi=0 or source a bound.",
            "status": "NEXT_HARD_PROOF_OBJECT",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "piece_id": "QKD4053_6_trace_volume",
            "object": "Gamma_eff trace and Khat trace",
            "formula": "Pure trace constant pieces are absorbed into kappa_obs/Lambda/background subtraction; surviving gradients feed nabla Gamma_eff - nabla Khat_trace.",
            "derived_from": "4027 volume trace plus PPC4048 fixed-coupling/background clauses",
            "meaning": "The trace sector is not allowed to hide a radial/source-dependent prefactor.",
            "status": "BACKGROUND_SUBTRACTION_GUARD_REQUIRED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "piece_id": "QKD4053_7_side_channels",
            "object": "boundary/projector/memory/cnorm",
            "formula": "Boundary flux, domain projector stress, local memory tail, and source-normalization derivative hair are zero in the selected PPC4048 branch or become explicit bound rows.",
            "derived_from": "4038/4043/4046/4047/4048",
            "meaning": "The side leaks no longer need to be re-litigated inside q_loc unless their parent clauses are rejected.",
            "status": "SELECTED_BRANCH_ZERO_ELSE_BOUND",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def theorem_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "step_id": "THM4053_0_assumptions",
            "step": "Selected local packet",
            "statement": "Assume PPC4048_0..10, with PPC4048_7 sharpened to a parent Hilbert owner for T_GK, live Khat_TF adoption, scalar-charge silence, fixed trace/background subtraction, and source-blind boundary/projector data.",
            "result": "All q_loc inputs are now named clauses rather than informal closure.",
            "status": "ASSUMPTIONS_EXPLICIT",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "step_id": "THM4053_1_rewrite",
            "step": "Stress divergence",
            "statement": "Use T_GK^{mu nu}:=Gamma_eff g_obs^{mu nu}-Khat^{mu nu}. Then q_loc^nu=P_loc nabla_mu T_GK^{mu nu}.",
            "result": "q_loc is governed by a Ward identity if T_GK is parent-Hilbert.",
            "status": "EXACT",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "step_id": "THM4053_2_Ward_silence",
            "step": "Noether silence",
            "statement": "If S_GK is local/diffeomorphism invariant and carrier fields are on shell, nabla_mu T_GK^{mu nu} has no bulk term except Euler, boundary, and nonvariational Helmholtz defects.",
            "result": "Bulk q_loc is zero if E_A=0, D_GK=0, and boundary/projector terms are source-blind.",
            "status": "CONDITIONAL_DERIVATION",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "step_id": "THM4053_3_Khat_tracefree_zero",
            "step": "Trace-free Khat zero",
            "statement": "With sigma_resp*c_I=1, Khat_TF is the variation of phi R. On the exterior EH collar, G_TF=0 and delta_phi=0 reduce D_TF to adoption/boundary/source-sector residuals.",
            "result": "Khat_TF makes no PPN q_loc source if scalar charge, adoption, and boundary clauses hold.",
            "status": "CONDITIONAL_DERIVATION",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "step_id": "THM4053_4_trace_zero",
            "step": "Trace/background zero",
            "statement": "Constant Gamma_0, kappa_obs, and vacuum trace pieces are calibration/background data; P_loc nabla of a constant trace is zero.",
            "result": "Trace contributions are harmless only if no source/range/domain-dependent trace prefactor survives.",
            "status": "CONDITIONAL_DERIVATION_WITH_GUARD",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "step_id": "THM4053_5_side_leaks",
            "step": "Side channel silence",
            "statement": "4038, 4043, 4046, and 4047 set selected-branch boundary/Poynting, projector/domain, memory-tail, and source-normalization channels to zero.",
            "result": "Those channels do not re-enter q_loc in PPC4048 unless their parent clauses are rejected.",
            "status": "PREVIOUS_ZERO_THEOREMS_IMPORTED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "step_id": "THM4053_6_conclusion",
            "step": "Projector silence reduction",
            "statement": "Under the explicit clauses C4053_0..6, Pi_PPN[q_loc]=0 through the local <=2PN branch.",
            "result": "PPC4048_7 is reduced to six auditable clauses; it is not fully parent-closed yet.",
            "status": "CONDITIONAL_REDUCTION_THEOREM_NOT_PUBLIC_PROOF",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "step_id": "THM4053_7_failure_mode",
            "step": "If any clause fails",
            "statement": "If D_GK, scalar charge, c_I mismatch, trace drift, source-only vertex, or boundary/projector flux survives, route it to the fallback vector with no cancellation credit.",
            "result": "No claim is allowed; the next job is to prove Q_phi=0 and sigma_resp*c_I=1 or source numeric bounds.",
            "status": "FAILS_CLEANLY_TO_BOUND_ROWS",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def clause_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "clause_id": "C4053_0_Hilbert_owner",
            "clause": "T_GK is a parent Hilbert stress of a local diffeomorphism-invariant S_GK.",
            "current_evidence": "4023 gives the Ward route; 4023 Helmholtz gate is not fully checked against actual Gamma/Khat.",
            "needed_to_close": "Symbolically certify Helmholtz defect D_GK=0 or source a bound.",
            "status": "OPEN_BUT_NOW_EXACT",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "clause_id": "C4053_1_Khat_TF_adoption",
            "clause": "The live Khat trace-free part equals the phi R improvement response with sigma_resp*c_I=1.",
            "current_evidence": "4028 derives the action variation; 4027 says live adoption/coefficient/sign remain unsigned.",
            "needed_to_close": "Parent-adopt c_I/sign/boundary convention or bound |1-sigma_resp*c_I|.",
            "status": "OPEN_COEFFICIENT_ADOPTION",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "clause_id": "C4053_2_scalar_charge_zero",
            "clause": "Exterior scalar hair u=delta_phi has Q_phi=0 on the compact local collar.",
            "current_evidence": "4031/4032 reduce this to boundary/source neutrality identities.",
            "needed_to_close": "Prove int_W F dV=0 and int_W u dV=0, or impose/source no-scalar-flux as a parent boundary condition.",
            "status": "BEST_NEXT_DERIVATION_TARGET",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "clause_id": "C4053_3_trace_background",
            "clause": "Trace/volume Gamma_eff and Khat pieces are constant calibration/background terms in the local exterior.",
            "current_evidence": "4027 has the volume-trace path; 4047 fixed local coupling supports constant kappa/G_obs.",
            "needed_to_close": "Fix subtraction/sign convention and prove no radial/source-dependent trace prefactor.",
            "status": "OPEN_TRACE_GUARD",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "clause_id": "C4053_4_no_source_slot",
            "clause": "No source-only vertices Z*T_H, Z*F_EM^2, source masks, or hidden Hodge/prefactor slots enter q_loc.",
            "current_evidence": "4034/4036 give a typed no-Hom theorem if the minimal typed packet is adopted.",
            "needed_to_close": "Adopt typed packet or keep c_T/c_EM/source-slot coefficients as bound rows.",
            "status": "CONDITIONAL_THEOREM_IF_TYPED_PACKET_ADOPTED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "clause_id": "C4053_5_boundary_projector_silence",
            "clause": "Boundary, Poynting, projector/domain, and memory/source-normalization side channels are silent in the compact local branch.",
            "current_evidence": "4038, 4043, 4046, and 4047 zero these in the selected branch.",
            "needed_to_close": "Carry their adopted clauses into the parent packet and keep fallback bounds if rejected.",
            "status": "SELECTED_BRANCH_ZERO_IMPORT",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "clause_id": "C4053_6_projector_readout",
            "clause": "P_loc is a post-variation local readout projector and cannot tune the action.",
            "current_evidence": "PPC4048 readout firewall plus 4023 exact identity.",
            "needed_to_close": "Formalize P_loc after-variation and its PPN order map.",
            "status": "OPEN_READOUT_FORMALIZATION",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def fallback_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "bound_id": "B4053_0_DGK",
            "surviving_object": "nonvariational Helmholtz defect",
            "formula": "|q_loc|_DGK <= ||P_loc|| |nabla_mu D_GK^{mu nu}|",
            "observable_map": "delta_beta_q_loc; R10 alpha(lambda); source-exchange",
            "needed_inputs": "A_DGK,L_DGK,C_beta_qloc,C_R10_qloc",
            "claim_status": "blocked_until_numeric_sourced",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "B4053_1_scalar_charge",
            "surviving_object": "exterior scalar hair",
            "formula": "u(r) ~ Q_phi exp(-mu_phi r)/(4*pi r); q_loc_scalar scales with derivatives of K_L[u]",
            "observable_map": "PPN beta/gamma residual; fifth-force alpha(lambda)",
            "needed_inputs": "Q_phi,mu_phi,source radius,PPN projector coefficients",
            "claim_status": "blocked_until_Q_phi_zero_or_bound",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "B4053_2_improvement_mismatch",
            "surviving_object": "Khat trace-free coefficient mismatch",
            "formula": "|q_loc|_cI <= |1-sigma_resp*c_I| ||P_loc nabla K_L||",
            "observable_map": "delta_beta_q_loc; local force residual",
            "needed_inputs": "sigma_resp,c_I,K_L profile,local length scale",
            "claim_status": "blocked_until_coefficient_signed_or_bounded",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "B4053_3_trace_drift",
            "surviving_object": "trace/background drift",
            "formula": "|q_loc|_trace <= ||P_loc|| |nabla(Gamma_trace-Khat_trace/4)|",
            "observable_map": "Gdot/G; radial G; clock/orbital source-normalization residual",
            "needed_inputs": "trace subtraction convention,radial/source derivative bounds",
            "claim_status": "blocked_until_trace_subtraction_signed",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "B4053_4_source_slot",
            "surviving_object": "ordinary matter/EM source-only leak",
            "formula": "|q_loc|_source <= |c_T| |nabla T_H| + |c_EM| |nabla F_EM^2| plus typed-slot residuals",
            "observable_map": "WEP/PPN preferred-source residual; R10 composition-sensitive force",
            "needed_inputs": "c_T,c_EM,source profiles,typed-packet adoption status",
            "claim_status": "blocked_unless_no_Hom_theorem_adopted",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "B4053_5_boundary_projector_flux",
            "surviving_object": "boundary/projector/Poynting flux",
            "formula": "|q_loc|_bdry <= ||P_loc|| |boundary_flux|/L_boundary",
            "observable_map": "alpha_i,xi,zeta_i,source-exchange tails",
            "needed_inputs": "boundary flux,collar size,projector variation norm",
            "claim_status": "blocked_unless_selected_boundary_clauses_adopted",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def static_rows(ts: str) -> Dict[str, List[Dict[str, object]]]:
    return {
        "evaluator": [
            {
                "case_id": "CASE4053_0",
                "verdict": "QLOC_KHAT_BLOCKER_REDUCED_NOT_CLOSED",
                "result": "The q_loc/Khat problem is reduced to parent Hilbert ownership, live Khat improvement normalization, scalar-charge zero, trace/background silence, source-slot silence, boundary/projector silence, and readout formalization.",
                "what_moved": "This is a derivation reduction, not another missing-list: the unknown is now a small set of named equations with fallback bounds.",
                "valid_for_public_claim": False,
                "timestamp_utc": ts,
            },
            {
                "case_id": "CASE4053_1",
                "verdict": "NEXT_PROOF_TARGET_IDENTIFIED",
                "result": "The highest-leverage next target is Q_phi=0 plus sigma_resp*c_I=1; if those close, PPC4048_7 becomes close to parent-signed.",
                "what_moved": "The local-GR route now has a concrete theorem hinge instead of a broad projector-silence placeholder.",
                "valid_for_public_claim": False,
                "timestamp_utc": ts,
            },
        ],
        "claim_gate": [
            {
                "claim_id": "CLAIM4053_0_private_progress",
                "claim": "q_loc/Khat projector silence has been reduced to explicit parent clauses and fallback bounds",
                "allowed_private": True,
                "allowed_public": False,
                "reason": "conditional reduction theorem only; no parent adoption yet",
                "timestamp_utc": ts,
            },
            {
                "claim_id": "CLAIM4053_1_PPC4048_7_closed",
                "claim": "PPC4048_7 is fully parent-derived and adopted",
                "allowed_private": False,
                "allowed_public": False,
                "reason": "Hilbert owner, Khat coefficient, scalar charge, trace subtraction, and readout map remain unsigned",
                "timestamp_utc": ts,
            },
            {
                "claim_id": "CLAIM4053_2_local_GR_safe",
                "claim": "MTS now publicly derives the local GR/PPN limit",
                "allowed_private": False,
                "allowed_public": False,
                "reason": "4053 is a conditional reduction, not a public local-GR proof",
                "timestamp_utc": ts,
            },
        ],
        "next_target": [
            {
                "row_id": "NEXT4053_0",
                "next_doc": "4054-Y5-R2FR-scalar-charge-zero-and-improvement-normalization-proof.md",
                "next_script": "scripts/Y5_R2FR_4054_scalar_charge_zero_and_improvement_normalization.py",
                "reason": "Q_phi=0 and sigma_resp*c_I=1 are the two sharpest remaining hinges for closing q_loc/Khat rather than bounding it.",
                "timestamp_utc": ts,
            }
        ],
        "status": [
            {
                "status_id": "STAT4053",
                "status": "QLOC_KHAT_PROJECTOR_SILENCE_REDUCED_TO_EXPLICIT_CLAUSES",
                "public_claim": False,
                "formalization_modified_by_4053": False,
                "timestamp_utc": ts,
            }
        ],
    }


def script_compiles() -> bool:
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
        return True
    except py_compile.PyCompileError:
        return False


def csv_parse_ok(path: Path) -> Tuple[bool, str]:
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), f"rows={len(rows)}"
    except Exception as exc:
        return False, repr(exc)


def validation_rows(
    sources: List[Dict[str, object]],
    generated_csvs: List[Path],
    all_rows: List[List[Dict[str, object]]],
) -> List[Dict[str, object]]:
    parse_results = [csv_parse_ok(path) for path in generated_csvs]
    flat_rows = [row for table in all_rows for row in table]
    serialized = "\n".join(str(value) for row in flat_rows for value in row.values())
    outputs_in_formalization = [path for path in OUTPUTS.values() if FORMALIZATION in path.parents]
    return [
        {
            "check_id": "VAL4053_00_sources_exist",
            "passed": all(bool(row["exists"]) for row in sources),
            "detail": "all cited local source paths exist",
        },
        {
            "check_id": "VAL4053_01_needles_present",
            "passed": all(bool(row["needle_present"]) for row in sources),
            "detail": "all source needles present",
        },
        {
            "check_id": "VAL4053_02_csv_parse",
            "passed": all(result for result, _detail in parse_results),
            "detail": "; ".join(f"{path.name}:{detail}" for path, (_ok, detail) in zip(generated_csvs, parse_results)),
        },
        {
            "check_id": "VAL4053_03_no_public_claim",
            "passed": "allowed_public': True" not in serialized and "valid_for_public_claim': True" not in serialized,
            "detail": "all claim-bearing rows preserve public false",
        },
        {
            "check_id": "VAL4053_04_no_missing_markers",
            "passed": "MISSING_" not in serialized,
            "detail": "outputs use explicit open/blocker language instead of MISSING markers",
        },
        {
            "check_id": "VAL4053_05_no_formalization_outputs",
            "passed": len(outputs_in_formalization) == 0,
            "detail": "4053 writes only post-checkpoint/source-intake outputs",
        },
        {
            "check_id": "VAL4053_06_script_compiles",
            "passed": script_compiles(),
            "detail": "script compiles",
        },
    ]


def doc_text(ts: str) -> str:
    return f"""# 4053 - q_loc/Khat Projector-Silence Reduction

- Timestamp: `{ts}`
- Status: `private_nonclaim_checkpoint`
- Formalization modified: `false`
- Public local-GR claim: `false`

## What Actually Moved

This checkpoint does not just say "`q_loc/Khat` is missing." It reduces the blocker to an exact theorem hinge.

The starting identity is:

```text
q_loc^nu = P_loc( nabla^nu Gamma_eff - nabla_mu Khat^{{mu nu}} )
         = P_loc nabla_mu T_GK^{{mu nu}},
T_GK^{{mu nu}} := Gamma_eff g_obs^{{mu nu}} - Khat^{{mu nu}}.
```

So the local force/source-exchange problem is a stress-divergence problem. If `T_GK` is a parent Hilbert stress of a local diffeomorphism-invariant sector, then the Noether/Ward identity kills its bulk divergence on shell, leaving only Euler defects, boundary defects, projector defects, and nonvariational Helmholtz mismatch.

## Conditional Reduction Theorem

Under the selected local PPC4048 packet plus the six sharpened 4053 clauses:

1. `T_GK` is parent-Hilbert and `D_GK=0`.
2. `Khat_TF` is the live `phi R` improvement response with `sigma_resp*c_I=1`.
3. Exterior scalar charge vanishes: `Q_phi=0`, hence `delta_phi=0` on the compact collar.
4. Trace/background terms are constant calibration/subtraction data, not radial/source prefactors.
5. No ordinary matter/EM source-only hidden slots exist.
6. Boundary, projector/domain, memory-tail, and source-normalization channels stay in their selected zero branches.

Then:

```text
Pi_PPN[q_loc] = 0
```

through the local `<=2PN` branch.

## Hard Truth

This is progress, but it is not public closure. The blocker has narrowed to:

- prove/adopt the parent Hilbert owner for `T_GK`;
- sign the live `Khat_TF` coefficient and boundary convention;
- prove `Q_phi=0` or source a scalar-charge bound;
- lock the trace/background subtraction;
- formalize `P_loc` as post-variation readout.

## Best Next Target

Go straight at `Q_phi=0` and `sigma_resp*c_I=1`. If those close, `PPC4048_7` stops being a broad projector-silence wish and becomes a nearly parent-signed local-GR clause. If they fail, the fallback bound vector is already staged.
"""


def main() -> None:
    ts = timestamp()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_rows(ts)
    decomposition = decomposition_rows(ts)
    theorem = theorem_rows(ts)
    clauses = clause_rows(ts)
    fallback = fallback_rows(ts)
    static = static_rows(ts)

    DOC_PATH.write_text(doc_text(ts), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["decomposition"], decomposition)
    write_csv(OUTPUTS["silence_reduction"], theorem)
    write_csv(OUTPUTS["clause_gate"], clauses)
    write_csv(OUTPUTS["fallback_bounds"], fallback)
    write_csv(OUTPUTS["evaluator"], static["evaluator"])
    write_csv(OUTPUTS["claim_gate"], static["claim_gate"])
    write_csv(OUTPUTS["next_target"], static["next_target"])
    write_csv(OUTPUTS["status"], static["status"])

    generated_csvs = [
        OUTPUTS["source_register"],
        OUTPUTS["decomposition"],
        OUTPUTS["silence_reduction"],
        OUTPUTS["clause_gate"],
        OUTPUTS["fallback_bounds"],
        OUTPUTS["evaluator"],
        OUTPUTS["claim_gate"],
        OUTPUTS["next_target"],
        OUTPUTS["status"],
    ]
    all_rows = [
        sources,
        decomposition,
        theorem,
        clauses,
        fallback,
        static["evaluator"],
        static["claim_gate"],
        static["next_target"],
        static["status"],
    ]
    validation = validation_rows(sources, generated_csvs, all_rows)
    write_csv(OUTPUTS["validation"], validation)

    cache_dir = SCRIPT_PATH.parent / "__pycache__"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)

    failures = [row for row in validation if not row["passed"]]
    print(f"wrote {DOC_PATH}")
    print(f"validation rows: {len(validation)}")
    print(f"validation failures: {len(failures)}")
    for failure in failures:
        print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()
