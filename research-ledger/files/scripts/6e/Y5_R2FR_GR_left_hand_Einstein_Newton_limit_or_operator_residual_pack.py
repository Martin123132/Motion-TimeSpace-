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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1769"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1769_0_1768_handoff",
        "source_key": "1768_gr_lhs_next",
        "source_path": ROOT / "1768-Y5-R2FR-parent-action-normal-form-and-source-map-identity-signature-or-shadow-coefficient-pack.md",
        "needles": ["GR_LEFT_HAND_EINSTEIN_AND_NEWTON_LIMIT_IS_NEXT", "NEXT1768_0_primary"],
    },
    {
        "source_id": "SRC1769_1_1768_validation",
        "source_key": "1768_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1768_VALIDATION.csv",
        "needles": ["VAL1768_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC1769_2_1768_normal_form",
        "source_key": "1768_normal_form",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1768_PARENT_ACTION_NORMAL_FORM_SIGNATURE.csv",
        "needles": ["ANF1768_0_parent_action_partition", "ANF1768_6_current_verdict"],
    },
    {
        "source_id": "SRC1769_3_1768_gr_bridge",
        "source_key": "1768_gr_bridge_status",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1768_GR_BRIDGE_STATUS.csv",
        "needles": ["GRB1768_1_lhs_operator", "GRB1768_4_next"],
    },
    {
        "source_id": "SRC1769_4_1009_current_chain",
        "source_key": "1009_parent_current_chain",
        "source_path": ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
        "needles": ["PCS1009_0_EH_core", "PCS1009_9_total_parent_contract"],
    },
    {
        "source_id": "SRC1769_5_1009_worldtube",
        "source_key": "1009_worldtube_glue",
        "source_path": ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
        "needles": ["PCS1009_8_worldtube_source_glue", "Poisson/Newton calibration"],
    },
    {
        "source_id": "SRC1769_6_1012_source_norm",
        "source_key": "1012_newton_poisson_blocker",
        "source_path": ROOT / "1012-Y5-R10-Y5-source-normalization-owner-or-q_loc-bound-implementation.md",
        "needles": ["Y5O1012_7_Newton_Poisson_orbit", "conditional_not_parent_derived"],
    },
    {
        "source_id": "SRC1769_7_1012_nonEH",
        "source_key": "1012_nonEH_operator_residual",
        "source_path": ROOT / "1012-Y5-R10-Y5-source-normalization-owner-or-q_loc-bound-implementation.md",
        "needles": ["Y5C1012_4_nonEH_operator_potential", "MISSING_EH_ONLY_THEOREM_OR_NONEH_OPERATOR_COEFFICIENT_MAP"],
    },
    {
        "source_id": "SRC1769_8_02_weak_field",
        "source_key": "02_motion_load_weak_field",
        "source_path": ROOT / "02-motion-load-local-GR-reduction.md",
        "needles": ["gamma = p", "beta completion = conditional"],
    },
    {
        "source_id": "SRC1769_9_01_route_contract",
        "source_key": "01_motion_load_route_contract",
        "source_path": ROOT / "01-motion-load-route-contract.md",
        "needles": ["gamma = 1", "Newtonian limit"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1769_SOURCE_REGISTER.csv",
    "einstein_limit": RESIDUALS / "P8_Y5_PARENT_QLOC_1769_EINSTEIN_LEFT_HAND_LIMIT_ATTEMPT.csv",
    "newton_limit": RESIDUALS / "P8_Y5_PARENT_QLOC_1769_NEWTON_POISSON_WEAK_FIELD_ATTEMPT.csv",
    "residual_pack": RESIDUALS / "P8_Y5_PARENT_QLOC_1769_OPERATOR_RESIDUAL_PACK.csv",
    "ppn_bridge": RESIDUALS / "P8_Y5_PARENT_QLOC_1769_PPN_BRIDGE_LEDGER.csv",
    "countermodel": RESIDUALS / "P8_Y5_PARENT_QLOC_1769_COUNTERMODEL_LEDGER.csv",
    "bridge_status": RESIDUALS / "P8_Y5_PARENT_QLOC_1769_GR_NEWTON_BRIDGE_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1769_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1769_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1769_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1769_VALIDATION.csv",
}


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": path.exists(),
                "needles_present": all(needle in text for needle in needles),
                "needles": ";".join(needles),
                "role": "GR left-hand Einstein/Newton limit or operator residual pack",
                "valid_for_claim": False,
            }
        )
    return rows


def einstein_limit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "ELH1769_0_target",
            "claim_piece": "left-hand operator reduces to Einstein form",
            "mathematical_form": "E_LHS[g,Phi,X] = G_munu + Lambda g_munu + DeltaE_munu",
            "status": "TARGET_EXACT",
            "derivation_result": "GR recovery requires DeltaE_munu -> 0 or bounded/suppressed in the local branch",
            "remaining_gap": "parent action has not signed EH dominance or all residual-sector silence",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "ELH1769_1_EH_variation",
            "claim_piece": "Einstein-Hilbert core gives Einstein tensor",
            "mathematical_form": "delta S_EH/delta g^{munu} -> G_munu + Lambda g_munu",
            "status": "REFERENCE_THEOREM",
            "derivation_result": "valid GR template only; it is not an MTS proof unless S_parent reduces to EH plus signed silent sectors",
            "remaining_gap": "EH-only import guard from 1009/1008 remains active",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "ELH1769_2_residual_decomposition",
            "claim_piece": "MTS operator residual split",
            "mathematical_form": "DeltaE=E_extra+E_projector+E_boundary+E_nonminimal+E_memory+E_higher_derivative",
            "status": "DECOMPOSITION_WRITTEN",
            "derivation_result": "each retained sector needs zero theorem, suppression theorem, or coefficient row",
            "remaining_gap": "sector-by-sector action variation and local scaling are missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "ELH1769_3_bianchi_gate",
            "claim_piece": "left-hand divergence identity",
            "mathematical_form": "nabla_mu E_LHS^{mu nu}=0 or nabla_mu DeltaE^{mu nu} balances retained residual sources",
            "status": "CONDITIONAL_NOETHER_GATE",
            "derivation_result": "a variational parent action supplies the Noether/Bianchi identity if all sectors are action-owned",
            "remaining_gap": "parent current-chain/action-sector certificates remain incomplete",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "ELH1769_4_current_verdict",
            "claim_piece": "current MTS Einstein left-hand limit",
            "mathematical_form": "E_LHS -> G_munu + Lambda g_munu",
            "status": "CONDITIONAL_THEOREM_NOT_PARENT_PROOF",
            "derivation_result": "if EH dominance + residual silence + Bianchi/no hidden sectors are signed, the GR LHS gate closes",
            "remaining_gap": "current corpus only supplies the contract; no local-GR claim",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def newton_limit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "NWF1769_0_metric_ansatz",
            "claim_piece": "weak-field metric expansion",
            "mathematical_form": "g_00=-(1+2Phi/c^2+O(c^-4)), g_ij=(1-2Psi/c^2)delta_ij+O(c^-4)",
            "status": "STANDARD_WEAK_FIELD_TEMPLATE",
            "derivation_result": "Newtonian limit can be read only after the parent LHS and source normalization are owned",
            "remaining_gap": "MTS observer/coframe map to this metric ansatz not parent-signed here",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "NWF1769_1_poisson_conditional",
            "claim_piece": "Poisson equation from Einstein 00 component",
            "mathematical_form": "G_00 ~= 2 nabla^2 Phi/c^2 and T_00 ~= rho c^2 => nabla^2 Phi=4 pi G rho",
            "status": "DERIVED_CONDITIONAL_TEMPLATE",
            "derivation_result": "Poisson follows if EH normalization kappa=8 pi G/c^4, clean Hilbert source, and DeltaE_00=0/bounded",
            "remaining_gap": "same parent charge/operator must identify rho_H and measured G without orbital backfill",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "NWF1769_2_inverse_square",
            "claim_piece": "inverse-square acceleration",
            "mathematical_form": "nabla^2 Phi=4 pi G rho, spherical exterior => Phi=-GM/r and a_r=-GM/r^2",
            "status": "CONDITIONAL_GAUSS_STEP",
            "derivation_result": "requires exterior closure/worldtube source glue before it can be used as an MTS prediction",
            "remaining_gap": "1009/1012 worldtube, Pi_M/J_H, and measured-GM gates remain blocked",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "NWF1769_3_ppn_gamma_beta",
            "claim_piece": "PPN lane",
            "mathematical_form": "gamma=Psi/Phi=1 and beta=1 if EH nonlinear completion dominates and residual anisotropic/nonlinear terms vanish",
            "status": "CONDITIONAL_PPN_TEMPLATE",
            "derivation_result": "recovers the early weak-field lane only under EH dominance/residual silence",
            "remaining_gap": "p=1/gamma=1 and beta=1 are not parent-derived from MTS here",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "NWF1769_4_current_verdict",
            "claim_piece": "current MTS Newton/Poisson limit",
            "mathematical_form": "nabla^2 Phi=4 pi G_ref rho_H and a=-nabla Phi",
            "status": "CONDITIONAL_NOT_PARENT_DERIVED",
            "derivation_result": "the route is clear but blocked by EH dominance, residual silence, source normalization, and worldtube/exterior closure",
            "remaining_gap": "no Newton/local-GR claim from 1769",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def residual_pack_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "ORP1769_0_E_LHS_GR_residual",
            "quantity": "E_LHS_GR_residual",
            "meaning": "left-hand deviation from Einstein operator",
            "mathematical_form": "DeltaE_munu=E_LHS-(G_munu+Lambda g_munu)",
            "units": "curvature_operator_units",
            "status": "MISSING_EH_DOMINANCE_OR_COEFFICIENT_MAP",
            "observable_links": "PPN gamma,beta; R10 alpha(lambda); clocks; orbital precession; cosmology growth",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ORP1769_1_higher_derivative",
            "quantity": "c_R2/c_Ricci2/c_boxR",
            "meaning": "higher-curvature left-hand corrections",
            "mathematical_form": "c_R2 R^2 + c_Ricci2 R_munu R^munu + c_boxR R box R",
            "units": "length_power_by_operator",
            "status": "MISSING_OPERATOR_BASIS_AND_BOUNDS",
            "observable_links": "short-range gravity, PPN, waves, cosmology",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ORP1769_2_projector_operator",
            "quantity": "c_projector/Pi_M_operator",
            "meaning": "domain/projector modification to LHS/source readout",
            "mathematical_form": "E_projector or [d,Pi_M]J_H obstruction",
            "units": "operator_dependent",
            "status": "MISSING_PARENT_PROJECTOR_VARIATION",
            "observable_links": "measured GM, R10, WEP, orbital systems",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ORP1769_3_boundary_reference",
            "quantity": "c_boundary/reference",
            "meaning": "boundary/counterterm/improvement deviation",
            "mathematical_form": "DeltaE_boundary or Q_boundary residual",
            "units": "boundary_operator_dependent",
            "status": "MISSING_FIXED_BEFORE_READOUT_BOUNDARY_SILENCE",
            "observable_links": "mass charge, orbital GM, local clocks",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ORP1769_4_nonminimal_matter_geometry",
            "quantity": "c_nonminimal",
            "meaning": "ordinary matter coupled directly to MTS/geometric scalars",
            "mathematical_form": "f(X,Phi) L_m or A(X)J_m",
            "units": "operator_dependent",
            "status": "MISSING_FORBID_OR_BOUND",
            "observable_links": "WEP, clocks, PPN, R10",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ORP1769_5_source_normalization",
            "quantity": "delta_G_source/M_H_ref",
            "meaning": "same charge must normalize Poisson and measured GM",
            "mathematical_form": "G_ref M_H_ref = surface/exterior charge before orbital fitting",
            "units": "GM_or_mass_units",
            "status": "MISSING_POISSON_GAUSS_WORLDTUBE_GLUE",
            "observable_links": "Newtonian orbit, Cavendish/local G, ephemerides",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ORP1769_6_nonclaim_lock",
            "quantity": "local-GR/Newton claim status",
            "meaning": "operator residual pack blocks promotion",
            "mathematical_form": "claim_allowed=false until every residual is zeroed or bounded",
            "units": "status",
            "status": "NONCLAIM_LOCK",
            "observable_links": "all local arenas",
            "valid_for_claim": False,
        },
    ]


def ppn_bridge_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "ppn_id": "PPN1769_0_gamma",
            "parameter": "gamma-1",
            "theory_requirement": "spatial and temporal weak-field potentials equal after residual silence",
            "mathematical_form": "gamma=Psi/Phi=1 + delta_gamma_residual",
            "status": "MISSING_PARENT_P_EQUALS_1_OR_EH_DOMINANCE",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "ppn_id": "PPN1769_1_beta",
            "parameter": "beta-1",
            "theory_requirement": "nonlinear EH completion dominates at O(Phi^2)",
            "mathematical_form": "g_00=-1+2U/c^2-2 beta U^2/c^4+...",
            "status": "MISSING_NONLINEAR_COMPLETION",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "ppn_id": "PPN1769_2_preferred_frame",
            "parameter": "alpha1/alpha2/alpha3",
            "theory_requirement": "observer/coframe and motion field do not create preferred-frame residuals in local branch",
            "mathematical_form": "alpha_i = alpha_i(E_projector,E_memory,E_coframe)",
            "status": "MISSING_LOCAL_FRAME_LOCK_OR_BOUND",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "ppn_id": "PPN1769_3_yukawa",
            "parameter": "alpha(lambda)",
            "theory_requirement": "extra operator tails absent or bounded",
            "mathematical_form": "Phi(r)=-(GM/r)(1+alpha exp(-r/lambda))",
            "status": "MISSING_R10_OPERATOR_MAP",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "ppn_id": "PPN1769_4_verdict",
            "parameter": "PPN/local-GR lane",
            "theory_requirement": "EH dominance + residual silence + source normalization",
            "mathematical_form": "gamma=beta=1 and alpha_i=0 only after gates pass",
            "status": "PPN_BRIDGE_LEDGER_READY_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1769_0_EH_anchor_import",
            "countermodel": "EH action is used as the whole MTS parent action without residual certificates",
            "mathematical_form": "S_parent := S_EH by assertion",
            "survives_current_constraints": True,
            "why_survives": "1009 says EH core is a baseline anchor, not total parent proof",
            "what_kills_it": "sector-by-sector parent action reduction/silence certificates",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1769_1_nonEH_operator_tail",
            "countermodel": "extra left-hand operator survives weak-field limit",
            "mathematical_form": "DeltaE_00 != 0 gives modified Poisson/Yukawa/PPN residual",
            "survives_current_constraints": True,
            "why_survives": "no EH-dominance theorem or coefficient map has been supplied",
            "what_kills_it": "zero/suppression theorem or source-backed operator coefficient bounds",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1769_2_source_normalization_laundering",
            "countermodel": "orbital GM is used to prove the same Newtonian GM",
            "mathematical_form": "M_ref := GM_orbit/G_ref before Poisson/Gauss bridge",
            "survives_current_constraints": True,
            "why_survives": "1012/1006 reject orbital backfill until source/worldtube closure is derived",
            "what_kills_it": "parent charge -> Poisson/Gauss -> exterior orbit chain before fitting",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1769_3_ppn_residual",
            "countermodel": "weak-field metric has gamma or beta deviation",
            "mathematical_form": "gamma-1 or beta-1 sourced by DeltaE/projector/coframe residual",
            "survives_current_constraints": True,
            "why_survives": "early weak-field p=1/beta=1 lanes are conditional, not parent-derived",
            "what_kills_it": "derive p=1/gamma=1 and beta=1 from parent EH-dominant local branch or bound PPN residuals",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1769_4_verdict",
            "countermodel": "GR/Newton recovery remains conditional",
            "mathematical_form": "E_LHS=G+Lambda g+DeltaE; DeltaE and source normalization not closed",
            "survives_current_constraints": True,
            "why_survives": "1769 writes the bridge but does not parent-sign EH dominance/Newton normalization",
            "what_kills_it": "1770 EH dominance/residual-sector silence plus operator coefficient validation",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def bridge_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "status_id": "GBS1769_0_source_side",
            "bridge_piece": "RHS Hilbert source",
            "current_status": "CLEAN_CONTRACT_PARENT_UNSIGNED",
            "evidence": "1764-1768 source-map chain",
            "remaining_gap": "normal-form/action inventory signature",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "GBS1769_1_lhs_einstein",
            "bridge_piece": "Einstein left-hand operator",
            "current_status": "CONDITIONAL_TEMPLATE_NOT_PARENT_PROOF",
            "evidence": "ELH1769_1 through ELH1769_4",
            "remaining_gap": "EH dominance and residual-sector silence",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "GBS1769_2_newton",
            "bridge_piece": "Poisson/Newton weak-field limit",
            "current_status": "CONDITIONAL_NOT_PARENT_DERIVED",
            "evidence": "NWF1769_1 through NWF1769_4",
            "remaining_gap": "source normalization, worldtube/exterior closure, residual-free weak field",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "GBS1769_3_ppn",
            "bridge_piece": "PPN local-GR lane",
            "current_status": "LEDGER_READY_NONCLAIM",
            "evidence": "PPN1769 rows",
            "remaining_gap": "gamma/beta/preferred-frame/Yukawa residual maps",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "GBS1769_4_next",
            "bridge_piece": "next derivation owner",
            "current_status": "EH_DOMINANCE_AND_RESIDUAL_SILENCE_IS_NEXT",
            "evidence": "operator residual pack isolates the remaining LHS blockers",
            "remaining_gap": "build 1770 residual-sector silence or operator coefficient pack",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1769_0_conditional_bridge",
            "decision": "GR_NEWTON_BRIDGE_SHAPE_IS_EXACT_CONDITIONALLY",
            "reason": "EH LHS plus clean Hilbert source gives Einstein equation and Poisson/Newton in the weak-field limit",
            "next_action": "do not claim it until MTS parent reduction to EH plus silent/bounded residuals is signed",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1769_1_no_import",
            "decision": "EH_TEMPLATE_NOT_MTS_PROOF",
            "reason": "1009/1008 explicitly reject using EH alone as the full parent action",
            "next_action": "keep EH as baseline template and require MTS residual certificates",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1769_2_residual_pack",
            "decision": "OPERATOR_RESIDUAL_PACK_STAGED",
            "reason": "if LHS residuals do not theorem-zero, they must become coefficient rows tied to PPN/R10/orbital/clock tests",
            "next_action": "stage zero-or-bound decisions for each residual sector",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1769_3_best_next",
            "decision": "EH_DOMINANCE_RESIDUAL_SILENCE_AND_OPERATOR_COEFFICIENTS_IS_NEXT",
            "reason": "this is the exact gate between a GR-reduction programme and a modified-gravity residual model",
            "next_action": "build 1770 EH dominance/residual-sector silence theorem or operator coefficient pack",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1769_0_EH_dominance",
            "claim": "parent LHS reduces to Einstein tensor plus Lambda",
            "gate_pass": False,
            "status": "NONCLAIM_THEOREM_GATE",
            "blocker": "BLOCKED_EH_DOMINANCE_AND_RESIDUAL_SILENCE_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1769_1_bianchi",
            "claim": "final LHS/RHS system has parent Noether/Bianchi identity",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_PARENT_CURRENT_CHAIN_SECTOR_CERTIFICATES_INCOMPLETE",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1769_2_poisson",
            "claim": "Poisson equation follows from MTS parent weak-field limit",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_SOURCE_NORMALIZATION_AND_LHS_RESIDUALS_OPEN",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1769_3_newton_orbit",
            "claim": "inverse-square Newtonian orbit follows without orbital GM backfill",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_WORLDTUBE_GAUSS_EXTERIOR_CLOSURE_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1769_4_ppn",
            "claim": "PPN gamma=1 beta=1 preferred-frame terms zero",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_PPN_RESIDUAL_MAPS_AND_BOUNDS_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1769_5_local_GR",
            "claim": "local GR/Newton recovery is derived",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_OPERATOR_RESIDUAL_PACK_NOT_ZEROED_OR_BOUNDED",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1769_0_primary",
            "next_target": "1770-Y5-R2FR-EH-dominance-and-residual-sector-silence-or-operator-coefficient-pack.md",
            "script": "scripts/Y5_R2FR_EH_dominance_and_residual_sector_silence_or_operator_coefficient_pack.py",
            "objective": "prove MTS parent LHS reduces to EH/Einstein operator in the local branch by zeroing/suppressing residual sectors, or stage operator coefficients for PPN/R10/orbital/clock bounds",
            "selection_status": "selected",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1769_1_fallback",
            "next_target": "1770b-Y5-R2FR-Poisson-Gauss-worldtube-source-normalization-pack.md",
            "script": "scripts/Y5_R2FR_Poisson_Gauss_worldtube_source_normalization_pack.py",
            "objective": "derive or stage the source-normalization/worldtube/Gauss bridge needed before measured GM or inverse-square orbital claims",
            "selection_status": "held_fallback",
            "valid_for_claim": False,
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "einstein_limit": einstein_limit_rows(),
        "newton_limit": newton_limit_rows(),
        "residual_pack": residual_pack_rows(),
        "ppn_bridge": ppn_bridge_rows(),
        "countermodel": countermodel_rows(),
        "bridge_status": bridge_status_rows(),
        "decision": decision_rows(),
        "claim_gate": claim_gate_rows(),
        "next_target": next_target_rows(),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv_ok(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1769_SOURCE_REGISTER.csv")
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        filename = path.name
        shutil.copy2(path, MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(path, QUARANTINE / filename)
        shutil.copy2(path, RAB_QUEUE / f"JR1769_{key.upper()}.csv")


def claim_like_field(key: str) -> bool:
    return key.lower() in {
        "valid_for_claim",
        "claim_allowed",
        "gate_pass",
        "prediction_allowed",
        "score_allowed",
        "claim_pass",
        "selected",
    }


def boolish_claim_true(key: str, value: Any) -> bool:
    if key.lower() == "selected":
        return False
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            for key, value in row.items():
                if claim_like_field(key) and boolish_claim_true(key, value):
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    status_keys = {"current_status", "status", "remaining_gap"}
    for rows in rows_map.values():
        for row in rows:
            combined_status = " ".join(str(row.get(key, "")) for key in status_keys)
            if "MISSING_" in combined_status:
                for key, value in row.items():
                    if claim_like_field(key) and boolish_claim_true(key, value):
                        return False
    return True


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1769_SOURCE_REGISTER.csv").exists():
        return False
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        filename = path.name
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1769_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched_for_1769() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*1769*"))


def csv_parse_all() -> bool:
    return all(parse_csv_ok(path) for key, path in OUTPUTS.items() if key != "validation")


def einstein_template_recorded(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["attempt_id"] == "ELH1769_1_EH_variation"
        and row["status"] == "REFERENCE_THEOREM"
        and row["valid_for_claim"] is False
        for row in rows_map["einstein_limit"]
    )


def einstein_not_promoted(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["attempt_id"] == "ELH1769_4_current_verdict"
        and row["status"] == "CONDITIONAL_THEOREM_NOT_PARENT_PROOF"
        and row["claim_allowed"] is False
        for row in rows_map["einstein_limit"]
    )


def newton_template_recorded(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["attempt_id"] == "NWF1769_1_poisson_conditional"
        and row["status"] == "DERIVED_CONDITIONAL_TEMPLATE"
        and row["valid_for_claim"] is False
        for row in rows_map["newton_limit"]
    )


def residual_pack_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    rows = rows_map["residual_pack"]
    return any(row["row_id"] == "ORP1769_0_E_LHS_GR_residual" for row in rows) and all(
        row["valid_for_claim"] is False for row in rows
    )


def ppn_bridge_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["ppn_id"] == "PPN1769_4_verdict"
        and row["status"] == "PPN_BRIDGE_LEDGER_READY_NONCLAIM"
        for row in rows_map["ppn_bridge"]
    ) and all(row["valid_for_claim"] is False for row in rows_map["ppn_bridge"])


def countermodel_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["countermodel_id"] == "CM1769_4_verdict"
        and row["survives_current_constraints"] is True
        and row["valid_for_claim"] is False
        for row in rows_map["countermodel"]
    )


def bridge_next(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["status_id"] == "GBS1769_4_next"
        and row["current_status"] == "EH_DOMINANCE_AND_RESIDUAL_SILENCE_IS_NEXT"
        for row in rows_map["bridge_status"]
    )


def next_selected(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["route_id"] == "NEXT1769_0_primary" and row["selection_status"] == "selected"
        for row in rows_map["next_target"]
    )


def check_row(check_id: str, condition: bool, pass_detail: str, fail_detail: str) -> dict[str, str]:
    return {
        "branch_id": BRANCH_ID,
        "check_id": check_id,
        "result": "PASS" if condition else "FAIL",
        "detail": pass_detail if condition else fail_detail,
    }


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    sources = rows_map["source_register"]
    claim_gates = rows_map["claim_gate"]
    checks = [
        check_row("VAL1769_0_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist", "one or more cited source paths missing"),
        check_row("VAL1769_1_needles_present", all(row["needles_present"] for row in sources), "required source needles are present", "one or more source needles missing"),
        check_row("VAL1769_2_einstein_template", einstein_template_recorded(rows_map), "EH/Einstein reference theorem recorded as nonclaim", "Einstein reference theorem missing"),
        check_row("VAL1769_3_einstein_not_promoted", einstein_not_promoted(rows_map), "Einstein limit remains conditional/nonclaim", "Einstein limit was promoted"),
        check_row("VAL1769_4_newton_template", newton_template_recorded(rows_map), "Poisson/Newton conditional template recorded", "Poisson/Newton template missing"),
        check_row("VAL1769_5_residual_pack_nonclaim", residual_pack_nonclaim(rows_map), "operator residual rows remain nonclaim", "operator residual pack missing or promoted"),
        check_row("VAL1769_6_ppn_bridge_nonclaim", ppn_bridge_nonclaim(rows_map), "PPN bridge rows remain nonclaim", "PPN bridge rows missing or promoted"),
        check_row("VAL1769_7_countermodel_retained", countermodel_retained(rows_map), "GR/Newton countermodel remains retained", "countermodel missing or promoted"),
        check_row("VAL1769_8_bridge_next", bridge_next(rows_map), "EH dominance/residual silence selected next", "bridge next status missing"),
        check_row(
            "VAL1769_9_claim_gates_safe",
            all(row["gate_pass"] is False and row["status"] in {"BLOCKED", "NONCLAIM_THEOREM_GATE"} for row in claim_gates),
            "all claim gates remain blocked/nonclaim",
            "one or more claim gates opened",
        ),
        check_row("VAL1769_10_no_claim_flags", no_claim_flags(rows_map), "claim/no-score flags stay false", "one or more claim/no-score flags enabled"),
        check_row("VAL1769_11_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready", "a MISSING_* row is marked ready"),
        check_row(
            "VAL1769_12_decision_next",
            any(row["decision_id"] == "DEC1769_3_best_next" and row["decision"] == "EH_DOMINANCE_RESIDUAL_SILENCE_AND_OPERATOR_COEFFICIENTS_IS_NEXT" for row in rows_map["decision"]),
            "decision selects EH dominance/residual-silence route",
            "best-next decision missing",
        ),
        check_row("VAL1769_13_next_selected", next_selected(rows_map), "next target selected", "next target missing"),
        check_row("VAL1769_14_csv_parse", csv_parse_all(), "all generated 1769 CSVs parse", "one or more generated 1769 CSVs fail to parse"),
        check_row("VAL1769_15_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "branch copies missing"),
        check_row("VAL1769_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check_row("VAL1769_17_formalization_untouched", formalization_untouched_for_1769(), "no 1769 outputs found under formalization-workbench", "1769 outputs found under formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in checks)
    checks.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1769_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1769 GR left-hand Einstein/Newton limit or operator residual pack",
        }
    )
    return checks


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, separator, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, str]]) -> str:
    sections = [
        "# 1769 - GR Left-Hand Einstein Newton Limit Or Operator Residual Pack",
        "",
        "## Verdict",
        "- 1769 writes the exact conditional bridge from a clean parent action to GR/Newton: EH left-hand operator + clean Hilbert source gives Einstein equation; the weak-field 00 equation then gives Poisson/Newton.",
        "- This is not an MTS claim. EH is only a reference template until the MTS parent action proves EH dominance and every extra/projector/boundary/nonminimal sector is zero, silent, suppressed, or explicitly bounded.",
        "- The Newton lane is also blocked by source normalization/worldtube closure: we cannot use orbital `GM` to prove the same `GM`.",
        "- The honest residual object is now `DeltaE_munu=E_LHS-(G_munu+Lambda g_munu)` plus source-normalization and PPN residual rows.",
        "- No GitHub, public, local-GR, Newton, PPN, WEP, clock, orbital, R10, or `q_loc=0` claim is made.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Einstein Left-Hand Limit Attempt",
        markdown_table(rows_map["einstein_limit"], ["attempt_id", "claim_piece", "mathematical_form", "status", "derivation_result", "remaining_gap"]),
        "",
        "## Newton Poisson Weak-Field Attempt",
        markdown_table(rows_map["newton_limit"], ["attempt_id", "claim_piece", "mathematical_form", "status", "derivation_result", "remaining_gap"]),
        "",
        "## Operator Residual Pack",
        markdown_table(rows_map["residual_pack"], ["row_id", "quantity", "meaning", "mathematical_form", "units", "status", "observable_links"]),
        "",
        "## PPN Bridge Ledger",
        markdown_table(rows_map["ppn_bridge"], ["ppn_id", "parameter", "theory_requirement", "mathematical_form", "status"]),
        "",
        "## Countermodel Ledger",
        markdown_table(rows_map["countermodel"], ["countermodel_id", "countermodel", "mathematical_form", "survives_current_constraints", "why_survives", "what_kills_it"]),
        "",
        "## GR Newton Bridge Status",
        markdown_table(rows_map["bridge_status"], ["status_id", "bridge_piece", "current_status", "evidence", "remaining_gap"]),
        "",
        "## Decisions",
        markdown_table(rows_map["decision"], ["decision_id", "decision", "reason", "next_action"]),
        "",
        "## Claim Gates",
        markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "status", "blocker"]),
        "",
        "## Next Target",
        markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status"]),
        "",
        "## Validation",
        markdown_table(validation_rows, ["check_id", "result", "detail"]),
        "",
        "## Working Interpretation",
        "This is the GR bridge in its honest form. The source side has been cleaned enough that the LHS is now the central pressure point. If MTS can prove EH dominance and residual-sector silence in the local branch, the path to Einstein and Newton is real. If it cannot, then MTS becomes a modified-operator theory with explicit PPN/R10/orbital/clock coefficients. Either route is respectable; what is not allowed is smuggling EH in and calling it derived.",
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
    doc_path = ROOT / "1769-Y5-R2FR-GR-left-hand-Einstein-Newton-limit-or-operator-residual-pack.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1769 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
