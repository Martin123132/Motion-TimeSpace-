from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1773"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1773_0_1772_handoff",
        "source_key": "1772_handoff",
        "source_path": ROOT / "1772-Y5-R2FR-PiM-commutator-projector-variation-zero-or-coefficient-bound.md",
        "needles": ["NEXT1772_0_primary", "PCZ1772_2_hilbert_equality_blocker"],
    },
    {
        "source_id": "SRC1773_1_1772_validation",
        "source_key": "1772_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1772_VALIDATION.csv",
        "needles": ["VAL1772_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC1773_2_1772_coefficients",
        "source_key": "1772_coefficient_pack",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1772_PIM_COEFFICIENT_BOUND_PACK.csv",
        "needles": ["PCB1772_0_R_eq_integral", "PCB1772_1_I_commutator", "PCB1772_2_B_zero_flux"],
    },
    {
        "source_id": "SRC1773_3_1015_same_object",
        "source_key": "1015_same_object",
        "source_path": ROOT / "1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md",
        "needles": ["SOL1015_6_verdict", "HEA1015_8_verdict"],
    },
    {
        "source_id": "SRC1773_4_1153_parent_signature",
        "source_key": "1153_parent_signature",
        "source_path": ROOT / "1153-Y5-R10-topological-PiM-Hilbert-equality-parent-signature-or-R_eq-source-fill.md",
        "needles": ["THEO1153_7_verdict", "REQ1153_4_R_eq_finite_shell_profile"],
    },
    {
        "source_id": "SRC1773_5_1016_selector",
        "source_key": "1016_selector",
        "source_path": ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
        "needles": ["PSC1016_9_verdict", "FIS1016_4_R_eq_integral"],
    },
    {
        "source_id": "SRC1773_6_1518_chainmap",
        "source_key": "1518_chainmap",
        "source_path": ROOT / "1518-Y5-parent-PiM-commutator-zero-theorem-or-R_eq-I_commutator-source-acquisition.md",
        "needles": ["COM1518_1_conditional_chainmap", "ACQ1518_0_R_eq"],
    },
    {
        "source_id": "SRC1773_7_parent_contract",
        "source_key": "hilbert_worldtube_contract",
        "source_path": RESIDUALS / "P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv",
        "needles": ["PAC537_5_Hilbert_topological_charge_equality", "PAC537_6_reference_and_boundary_zero"],
    },
    {
        "source_id": "SRC1773_8_old_attempt",
        "source_key": "old_topological_attempt",
        "source_path": RESIDUALS / "P8_TOPOLOGICAL_HILBERT_EQUALITY_ATTEMPT.csv",
        "needles": ["EH501_1_worldtube_charge_route", "EH501_5_radial_bound_fallback"],
    },
    {
        "source_id": "SRC1773_9_hwt_attempt",
        "source_key": "hilbert_worldtube_attempt",
        "source_path": RESIDUALS / "P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv",
        "needles": ["HWT536_3_Hilbert_to_PiM_charge_map", "HWT536_5_exact_and_reference_terms_zero"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1773_SOURCE_REGISTER.csv",
    "same_object_theorem": RESIDUALS / "P8_Y5_PARENT_QLOC_1773_SAME_OBJECT_THEOREM.csv",
    "proof_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1773_TOPOLOGICAL_HILBERT_PROOF_AUDIT.csv",
    "period_lock": RESIDUALS / "P8_Y5_PARENT_QLOC_1773_PERIOD_CHARGE_LOCK_AUDIT.csv",
    "bound_pack": RESIDUALS / "P8_Y5_PARENT_QLOC_1773_R_EQ_BOUND_PACK.csv",
    "countermodel": RESIDUALS / "P8_Y5_PARENT_QLOC_1773_COUNTERMODEL_LEDGER.csv",
    "impact": RESIDUALS / "P8_Y5_PARENT_QLOC_1773_GR_NEWTON_IMPACT_LEDGER.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1773_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1773_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1773_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1773_VALIDATION.csv",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["source_path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": exists,
                "needles": ";".join(needles),
                "needles_present": exists and all(needle in text for needle in needles),
                "role": "1773 topological-Hilbert equality / R_eq bound evidence",
            }
        )
    return rows


def same_object_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "SOT1773_0_statement",
            "claim": "conditional topological-Hilbert same-object theorem",
            "mathematical_form": "If Pi_M J_H and J_M_top are closed representatives of the same compact source cohomology class on A_ext, then Pi_M J_H - J_M_top = dB_zero plus retained residual R_eq.",
            "status": "CONDITIONAL_MATH_THEOREM_CLEAN",
            "proof_content": "de Rham/Poincare-dual same-class lemma; exact improvement is allowed only after periods and boundary terms are fixed",
            "missing_for_current_MTS": "parent-signed same worldtube, same Hilbert measure, same periods, boundary-zero flux, no extra exchange",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "SOT1773_1_closed_exterior",
            "claim": "projected Hilbert source is closed in the compact exterior",
            "mathematical_form": "d(Pi_M J_H)=0 on A_ext",
            "status": "NOT_CURRENTLY_DERIVED",
            "proof_content": "1772 gives a conditional topological chain-map route, but it depends on equality with the physical Hilbert source",
            "missing_for_current_MTS": "I_commutator and exchange/projector-stress residuals remain open",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "SOT1773_2_topological_representative",
            "claim": "J_M_top is the Poincare-dual representative of the same Hilbert worldtube",
            "mathematical_form": "J_M_top = Q_M omega_M_top, d omega_M_top=0, integral_L omega_M_top=1 for every allowed linking cycle L around W_source",
            "status": "CONDITIONAL_ONLY",
            "proof_content": "works if Q_M and omega_M_top are selected by W_source before fitting or readout",
            "missing_for_current_MTS": "worldtube support selector and topological boundary-class certificate",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "SOT1773_3_period_equality",
            "claim": "the two currents have equal periods on all linked surfaces",
            "mathematical_form": "for all L in H_link(A_ext): integral_L Pi_M J_H = integral_L J_M_top = Q_M",
            "status": "KEY_BLOCKER_NOT_DERIVED",
            "proof_content": "same cohomology class is equivalent to period equality over the nontrivial linked cycles",
            "missing_for_current_MTS": "M_H_ref/Q_M same-frame denominator and period-charge lock",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "SOT1773_4_exact_boundary_zero",
            "claim": "exact improvement has no measured linked-surface flux",
            "mathematical_form": "integral_boundary dB_zero = 0 after a fixed reference and surface convention",
            "status": "MISSING_BOUNDARY_ZERO_CERTIFICATE",
            "proof_content": "exact terms are harmless only when the compact boundary/reference prescription is fixed once",
            "missing_for_current_MTS": "B_zero_flux and Delta_symp/reference lock",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "SOT1773_5_current_verdict",
            "claim": "Pi_M J_H = J_M_top + dB_zero for current MTS",
            "mathematical_form": "R_eq := Pi_M J_H - J_M_top - dB_zero = 0",
            "status": "FAIL_CURRENT_PARENT_PROOF",
            "proof_content": "the theorem is clean only as a conditional lemma; current MTS has not signed the same-object hypotheses",
            "missing_for_current_MTS": "R_eq_integral, M_H_ref, period lock, boundary lock, exchange silence",
            "valid_for_claim": False,
        },
    ]


def proof_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "THA1773_0_same_worldtube",
            "clause": "same compact Hilbert source worldtube",
            "required_identity": "W_source = supp(J_H[e_obs,tau]); all linked surfaces enclose the same W_source",
            "current_status": "NOT_PARENT_DERIVED",
            "failure_mode": "the topological source can be chosen after seeing the orbital/radial readout",
            "next_action": "derive source support selector or keep Delta_worldtube_domain row",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "THA1773_1_same_measure",
            "clause": "same-frame Hilbert/Noether source measure",
            "required_identity": "Q_M = M_H_ref = H_tau[S]-H_ref = integral_W rho_H dV_H in the observed coframe",
            "current_status": "MISSING_MHREF_SOURCE_FRAME_LOCK",
            "failure_mode": "bare/topological mass and measured gravitational source can be different quantities",
            "next_action": "derive observed coframe/tau/M_H_ref lock",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "THA1773_2_same_cohomology_class",
            "clause": "period equality over linked cycles",
            "required_identity": "integral_L(Pi_M J_H - J_M_top)=0 for every allowed linked cycle L",
            "current_status": "KEY_BLOCKER_NOT_DERIVED",
            "failure_mode": "closed topological current may be the wrong conserved object",
            "next_action": "build period-charge lock theorem or R_eq period-bound row",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "THA1773_3_boundary_reference",
            "clause": "exact/reference boundary terms are fixed",
            "required_identity": "integral_boundary dB_zero=0 and Delta_symp=0, or source-backed finite rows",
            "current_status": "MISSING_B_ZERO_DELTA_SYMP_INPUT",
            "failure_mode": "surface charge equality shifts by bookkeeping rather than physics",
            "next_action": "carry B_zero_flux and Delta_symp into the next bound pack",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "THA1773_4_no_exchange",
            "clause": "no hidden non-Hilbert/source exchange",
            "required_identity": "Delta_extra + Delta_domain + Delta_frame + Delta_memory + Delta_range = 0 or bounded below local locks",
            "current_status": "RETAINED_RESIDUAL_VECTOR",
            "failure_mode": "R_eq can hide non-EH/non-matter source hair",
            "next_action": "keep absolute residual envelope; no cancellation credit",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "THA1773_5_verdict",
            "clause": "current MTS parent-signs topological-Hilbert equality",
            "required_identity": "THA1773_0 through THA1773_4 all pass in the same parent action",
            "current_status": "NOT_PARENT_SIGNED",
            "failure_mode": "GR/Newton bridge still has a wrong-source loophole",
            "next_action": "1774 period-charge/M_H_ref lock or first source-backed R_eq row",
            "valid_for_claim": False,
        },
    ]


def period_lock_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "lock_id": "PCL1773_0_linked_period",
            "object": "linked-surface period",
            "definition": "Delta_period[L] = integral_L Pi_M J_H - integral_L J_M_top",
            "required_zero_or_bound": "Delta_period[L]=0 for all allowed linked cycles, or max_L abs(Delta_period[L])/M_H_ref <= bound",
            "status": "MISSING_PERIOD_LOCK",
            "why_it_matters": "same-class de Rham exactness requires period equality, not just local closure",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "lock_id": "PCL1773_1_charge_normalization",
            "object": "M_H_ref denominator",
            "definition": "M_H_ref = H_tau[S_outer]-H_ref in the observed source/readout frame",
            "required_zero_or_bound": "positive source-backed denominator with tau, surface, reference, and units",
            "status": "MISSING_M_H_REF",
            "why_it_matters": "R_eq, B_zero, and commutator rows cannot be claim-scaled without an honest denominator",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "lock_id": "PCL1773_2_PD_normalization",
            "object": "topological representative normalization",
            "definition": "integral_L omega_M_top=1 on every canonical linking cycle for the same W_source",
            "required_zero_or_bound": "source-independent certificate tying omega_M_top to W_source",
            "status": "MISSING_PD_CERTIFICATE",
            "why_it_matters": "otherwise J_M_top can be normalized to match by definition",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "lock_id": "PCL1773_3_no_readout_selection",
            "object": "readout independence",
            "definition": "W_source, L, tau, and omega_M_top are selected before fitting local acceleration/orbital data",
            "required_zero_or_bound": "proven parent selector or frozen source-file row",
            "status": "MISSING_SELECTOR_CERTIFICATE",
            "why_it_matters": "post-hoc source selection would smuggle Newtonian calibration into the theorem",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "lock_id": "PCL1773_4_verdict",
            "object": "period-charge lock",
            "definition": "Delta_period=0, M_H_ref real, PD normalized, and no readout selection",
            "required_zero_or_bound": "all PCL1773_0 through PCL1773_3 pass",
            "status": "FAIL_CURRENT_LOCK",
            "why_it_matters": "this is now the sharpest missing bridge between topological closure and measured source mass",
            "valid_for_claim": False,
        },
    ]


def bound_pack_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REQ1773_0_R_eq_integral",
            "quantity": "R_eq_integral",
            "definition": "finite-shell absolute integral of Pi_M J_H - J_M_top - dB_zero",
            "units": "dimensionless_after_MHref_normalization",
            "required_inputs": "system_id;r1;r2;PiM_JH_profile;JM_top_profile;B_zero_profile;M_H_ref;source_path",
            "status": "MISSING_R_EQ_INTEGRAL",
            "maps_to": "wrong conserved object; Newton source normalization; R10/R11 radial hair",
            "ready_for_claim": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REQ1773_1_Delta_period",
            "quantity": "Delta_period",
            "definition": "max linked-surface period mismatch integral_L(Pi_M J_H - J_M_top)",
            "units": "GM_flux_or_dimensionless_after_MHref_normalization",
            "required_inputs": "linked_cycles;surface_integrals;M_H_ref;tau;W_source;source_path",
            "status": "MISSING_PERIOD_MISMATCH_BOUND",
            "maps_to": "same cohomology class gate; measured-GM lock",
            "ready_for_claim": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REQ1773_2_B_zero_flux",
            "quantity": "B_zero_flux",
            "definition": "boundary/reference/exact improvement flux through compact linked boundary",
            "units": "GM_flux_or_dimensionless",
            "required_inputs": "boundary_type;reference_choice;B_zero_definition;flux_value;M_H_ref;source_path",
            "status": "MISSING_B_ZERO_FLUX",
            "maps_to": "boundary/reference charge closure; local source equality",
            "ready_for_claim": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REQ1773_3_I_commutator",
            "quantity": "I_commutator",
            "definition": "finite-annulus integral of [d,Pi_M]J_H",
            "units": "GM_flux_or_dimensionless_after_MHref_normalization",
            "required_inputs": "PiM_profile;J_H_profile;annulus;M_H_ref;source_path",
            "status": "MISSING_I_COMMUTATOR",
            "maps_to": "projector/source hair; R10/R11; local-GR residual",
            "ready_for_claim": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REQ1773_4_M_H_ref",
            "quantity": "M_H_ref",
            "definition": "same-frame Hilbert/Hamiltonian source charge used to normalize equality residuals",
            "units": "mass_or_GM_source_charge",
            "required_inputs": "tau;e_obs;H_tau;H_ref;surface;units;source_path",
            "status": "MISSING_M_H_REF",
            "maps_to": "R_eq denominator; Newtonian GM bridge; PPN normalization",
            "ready_for_claim": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REQ1773_5_Delta_worldtube_domain",
            "quantity": "Delta_worldtube_domain",
            "definition": "source support/linking surface/domain mismatch contribution",
            "units": "dimensionless_or_GM_flux",
            "required_inputs": "W_source_certificate;S1;S2;domain_rule;readout_independence;source_path",
            "status": "MISSING_WORLDTUBE_DOMAIN_LOCK",
            "maps_to": "readout-independent source selector; finite-source local limits",
            "ready_for_claim": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REQ1773_6_projector_stress_beta_equiv",
            "quantity": "projector_stress_beta_equiv",
            "definition": "PPN/local weak-field equivalent of metric stress from projector variation",
            "units": "PPN_or_operator_units",
            "required_inputs": "delta_PiM;stress_map;weak_field_expansion;source_path",
            "status": "MISSING_PROJECTOR_STRESS_MAP",
            "maps_to": "gamma,beta,alpha_i,R11,local-GR",
            "ready_for_claim": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REQ1773_7_epsilon_eq_abs",
            "quantity": "epsilon_eq_abs",
            "definition": "absolute no-cancellation envelope of R_eq, period, boundary, commutator, worldtube, frame, and stress residuals",
            "units": "dimensionless",
            "required_inputs": "component_abs_sum;M_H_ref;all_component_source_paths",
            "status": "MISSING_COMPONENT_INPUTS",
            "maps_to": "claim-safe equality residual envelope",
            "ready_for_claim": False,
            "valid_for_claim": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1773_0_closed_wrong_charge",
            "countermodel": "closed topological current with wrong period",
            "mathematical_form": "dJ_M_top=0 but integral_L J_M_top != integral_L Pi_M J_H",
            "survives_current_constraints": True,
            "why_survives": "current branch has no period-charge lock",
            "what_kills_it": "Delta_period=0 theorem or source-backed small bound",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1773_1_same_period_boundary_shift",
            "countermodel": "same periods but nonzero exact/reference boundary flux",
            "mathematical_form": "Pi_M J_H - J_M_top = dB_zero with integral_boundary dB_zero != 0",
            "survives_current_constraints": True,
            "why_survives": "B_zero_flux and reference lock remain missing",
            "what_kills_it": "fixed reference plus B_zero_flux=0 theorem or bound",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1773_2_readout_defined_topology",
            "countermodel": "topological representative normalized after orbital readout",
            "mathematical_form": "Q_M := measured GM/G_ref then J_M_top := Q_M omega_M_top",
            "survives_current_constraints": True,
            "why_survives": "readout-independent source selector is not signed",
            "what_kills_it": "parent source support and PD normalization before data fitting",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1773_3_hidden_exchange",
            "countermodel": "Hilbert-topological mismatch absorbed by extra/memory/projector channel",
            "mathematical_form": "R_eq = -Delta_extra - Delta_memory - Delta_PiM with no single term bounded",
            "survives_current_constraints": True,
            "why_survives": "absolute residual envelope is unfilled",
            "what_kills_it": "zero theorem or no-cancellation source rows for every component",
        },
    ]


def impact_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "impact_id": "IMP1773_0_Einstein_source",
            "bridge_piece": "Einstein equation source side",
            "impact": "T_matter cannot be reduced to the topological mass current until Pi_M J_H is the same source object",
            "current_status": "BLOCKED_BY_R_EQ_PERIOD_LOCK",
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "IMP1773_1_Newton_Poisson",
            "bridge_piece": "Poisson/Newton limit",
            "impact": "inverse-square coefficient can still be calibrated to a wrong or shifted charge",
            "current_status": "BLOCKED_BY_M_H_REF_AND_B_ZERO",
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "IMP1773_2_PPN",
            "bridge_piece": "PPN residual vector",
            "impact": "projector stress and equality residuals remain admissible local fifth-force sources",
            "current_status": "BLOCKED_BY_PROJECTOR_STRESS_AND_EPSILON_EQ",
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "IMP1773_3_R10_R11",
            "bridge_piece": "finite-source/local range tests",
            "impact": "R_eq/I_commutator/B_zero rows are now the source-ready nonclaim inputs for bound acquisition",
            "current_status": "NONCLAIM_SOURCE_ROWS_STAGED",
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "IMP1773_4_local_GR",
            "bridge_piece": "local GR recovery",
            "impact": "no local-GR claim reopens from topological closure alone",
            "current_status": "CLAIM_BLOCKED",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1773_0_math_status",
            "decision": "SAME_OBJECT_LEMMA_IS_MATHEMATICALLY_CLEAN",
            "reason": "closed same-class currents differ by an exact term; the topological route is not nonsense",
            "next_action": "do not count it as MTS evidence until the parent signs same object and periods",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1773_1_physics_status",
            "decision": "CURRENT_MTS_EQUALITY_NOT_PARENT_SIGNED",
            "reason": "worldtube selector, M_H_ref, period equality, boundary zero, and residual envelope remain missing",
            "next_action": "keep R_eq/I_commutator/B_zero rows nonclaim",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1773_2_no_shortcut",
            "decision": "NO_READOUT_DEFINED_TOPOLOGY_OR_BARE_MASS_DENOMINATOR",
            "reason": "those would define the source charge from the quantity the theorem is supposed to derive",
            "next_action": "require parent coframe/tau/source-frame lock or source-backed denominator",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1773_3_best_next",
            "decision": "PERIOD_CHARGE_LOCK_OR_MHREF_FIRST_ROW_IS_NEXT",
            "reason": "period equality is the remaining theorem gate and M_H_ref is the denominator for the fallback bound",
            "next_action": "build 1774 period-charge/M_H_ref lock checkpoint",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1773_0_conditional_theorem",
            "claim": "same-object theorem is valid as conditional mathematics",
            "gate_pass": True,
            "status": "PASS_NONCLAIM",
            "blocker": "does not prove current MTS hypotheses",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1773_1_topological_Hilbert_equality",
            "claim": "Pi_M J_H = J_M_top + dB_zero for current MTS",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_PERIOD_CHARGE_LOCK_AND_MHREF_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1773_2_R_eq_bound_ready",
            "claim": "R_eq/I_commutator/B_zero rows are source-backed claim rows",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_MISSING_NUMERIC_OR_THEOREM_ZERO_INPUTS",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1773_3_Newton_GR_reduction",
            "claim": "Newton/local-GR gates can reopen",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_WRONG_SOURCE_COUNTERMODEL_RETAINED",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1773_0_primary",
            "next_target": "1774-Y5-R2FR-period-charge-lock-or-MHref-first-row.md",
            "script": "scripts/Y5_R2FR_period_charge_lock_or_MHref_first_row.py",
            "objective": "derive linked-period equality and same-frame M_H_ref from the parent source object, or stage the first source-backed denominator/period mismatch row",
            "selection_status": "selected",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1773_1_fallback",
            "next_target": "1774b-Y5-R2FR-boundary-zero-and-projector-stress-bound-pack.md",
            "script": "scripts/Y5_R2FR_boundary_zero_and_projector_stress_bound_pack.py",
            "objective": "if period lock stalls, source B_zero_flux, Delta_symp, and projector-stress beta-equivalent bound rows without claiming local GR",
            "selection_status": "fallback",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "same_object_theorem": same_object_theorem_rows(),
        "proof_audit": proof_audit_rows(),
        "period_lock": period_lock_rows(),
        "bound_pack": bound_pack_rows(),
        "countermodel": countermodel_rows(),
        "impact": impact_rows(),
        "decision": decision_rows(),
        "claim_gate": claim_gate_rows(),
        "next_target": next_target_rows(),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        filename = path.name
        shutil.copy2(path, MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(path, QUARANTINE / filename)
        shutil.copy2(path, RAB_QUEUE / f"JR1773_{key.upper()}.csv")


def parse_csv(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def boolish(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def generated_csvs() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def sources_ok(rows_map: dict[str, list[dict[str, Any]]]) -> tuple[bool, bool]:
    rows = rows_map["source_register"]
    return all(boolish(row["exists"]) for row in rows), all(boolish(row["needles_present"]) for row in rows)


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for key, rows in rows_map.items():
        if key == "source_register":
            continue
        for row in rows:
            for flag in ("valid_for_claim", "ready_for_claim", "claim_allowed"):
                if flag in row and boolish(row[flag]):
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            text = " ".join(str(value) for value in row.values()).upper()
            if "MISSING" in text:
                if boolish(row.get("valid_for_claim", False)) or boolish(row.get("ready_for_claim", False)):
                    return False
    return True


def branch_copies_exist() -> bool:
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        filename = path.name
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1773_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    return not any(FORMALIZATION.rglob("*1773*")) if FORMALIZATION.exists() else True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    exists_ok, needles_ok = sources_ok(rows_map)
    checks: list[tuple[str, bool, str]] = [
        ("VAL1773_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1773_1_needles_present", needles_ok, "required source needles are present"),
        (
            "VAL1773_2_conditional_theorem_recorded",
            any(row["theorem_id"] == "SOT1773_0_statement" and row["status"] == "CONDITIONAL_MATH_THEOREM_CLEAN" for row in rows_map["same_object_theorem"]),
            "conditional same-object theorem is explicit",
        ),
        (
            "VAL1773_3_current_equality_not_promoted",
            any(row["theorem_id"] == "SOT1773_5_current_verdict" and row["status"] == "FAIL_CURRENT_PARENT_PROOF" for row in rows_map["same_object_theorem"]),
            "current topological-Hilbert equality remains unpromoted",
        ),
        (
            "VAL1773_4_period_lock_blocker",
            any(row["lock_id"] == "PCL1773_4_verdict" and row["status"] == "FAIL_CURRENT_LOCK" for row in rows_map["period_lock"]),
            "period-charge lock is retained as the sharp blocker",
        ),
        (
            "VAL1773_5_bound_pack_nonclaim",
            all(not boolish(row["valid_for_claim"]) and not boolish(row["ready_for_claim"]) for row in rows_map["bound_pack"]),
            "R_eq bound rows remain nonclaim",
        ),
        (
            "VAL1773_6_countermodels_retained",
            all(boolish(row["survives_current_constraints"]) for row in rows_map["countermodel"]),
            "wrong-charge countermodels remain live",
        ),
        (
            "VAL1773_7_claim_gates_safe",
            all(not boolish(row["valid_for_claim"]) for row in rows_map["claim_gate"]),
            "all claim gates remain nonclaim",
        ),
        ("VAL1773_8_no_claim_flags", no_claim_flags(rows_map), "no generated claim/ready flags are true"),
        ("VAL1773_9_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1773_10_decision_next",
            any(row["decision_id"] == "DEC1773_3_best_next" and "PERIOD_CHARGE_LOCK" in row["decision"] for row in rows_map["decision"]),
            "decision selects period-charge/M_H_ref next",
        ),
        (
            "VAL1773_11_next_selected",
            any(row["route_id"] == "NEXT1773_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1773_12_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1773 CSVs parse"),
        ("VAL1773_13_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        (
            "VAL1773_14_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
        ),
        (
            "VAL1773_15_formalization_untouched",
            formalization_untouched(),
            "no 1773 outputs found under formalization-workbench",
        ),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1773_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1773 topological-Hilbert equality or R_eq bound checkpoint",
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(str(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, str]]) -> str:
    sections = [
        "# 1773 - Y5/R2FR Topological-Hilbert Equality or R_eq Bound",
        "",
        "## Verdict",
        "",
        "The same-object route is mathematically clean but not yet a current-MTS result. If `Pi_M J_H` and `J_M_top` are closed representatives of the same compact source cohomology class, then their difference is exact up to the retained residual `R_eq`. The missing physics is the period-charge lock: the topological periods must equal the same-frame Hilbert/Hamiltonian source charge before any Newton/local-GR gate can reopen.",
        "",
        "**Claim ceiling:** no topological-Hilbert equality, closed Hilbert flux, measured-GM closure, Newton/GR reduction, R10/R11 pass, PPN pass, or local-GR claim is allowed from 1773.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "role"]),
        "",
        "## Same-Object Theorem",
        markdown_table(rows_map["same_object_theorem"], ["theorem_id", "claim", "mathematical_form", "status", "proof_content", "missing_for_current_MTS", "valid_for_claim"]),
        "",
        "## Proof Audit",
        markdown_table(rows_map["proof_audit"], ["audit_id", "clause", "required_identity", "current_status", "failure_mode", "next_action", "valid_for_claim"]),
        "",
        "## Period-Charge Lock",
        markdown_table(rows_map["period_lock"], ["lock_id", "object", "definition", "required_zero_or_bound", "status", "why_it_matters", "valid_for_claim"]),
        "",
        "## R_eq Bound Pack",
        markdown_table(rows_map["bound_pack"], ["row_id", "quantity", "definition", "units", "required_inputs", "status", "maps_to", "ready_for_claim", "valid_for_claim"]),
        "",
        "## Countermodel Ledger",
        markdown_table(rows_map["countermodel"], ["countermodel_id", "countermodel", "mathematical_form", "survives_current_constraints", "why_survives", "what_kills_it"]),
        "",
        "## GR/Newton Impact Ledger",
        markdown_table(rows_map["impact"], ["impact_id", "bridge_piece", "impact", "current_status"]),
        "",
        "## Decision Ledger",
        markdown_table(rows_map["decision"], ["decision_id", "decision", "reason", "next_action"]),
        "",
        "## Claim Gates",
        markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "status", "blocker", "valid_for_claim"]),
        "",
        "## Next Target",
        markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status"]),
        "",
        "## Validation",
        markdown_table(validation_rows, ["check_id", "result", "detail"]),
        "",
        "## Working Interpretation",
        "This is a useful narrowing, not a win-banner. The theory now has a clean mathematical door: same worldtube, same periods, same Hilbert charge, fixed boundary terms. The thing to hunt next is the parent-owned period/charge denominator. If that closes, the topological mass current can become the actual source current; if not, `R_eq` becomes a measurable residual rather than a slogan.",
        "",
    ]
    return "\n".join(sections)


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    doc_path = ROOT / "1773-Y5-R2FR-topological-Hilbert-equality-or-R-eq-bound.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1773 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
