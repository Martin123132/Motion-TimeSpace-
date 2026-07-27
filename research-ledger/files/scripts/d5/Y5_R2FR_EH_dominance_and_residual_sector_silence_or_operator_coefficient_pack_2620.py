from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2620-Y5-R2FR-EH-dominance-and-residual-sector-silence-or-operator-coefficient-pack.md"

PREFIX = "P8_Y5_EH_DOMINANCE_GATE_2620"

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "lineage_ledger": RESIDUALS / f"{PREFIX}_LINEAGE_LEDGER.csv",
    "eh_theorem": RESIDUALS / f"{PREFIX}_EH_DOMINANCE_THEOREM_ATTEMPT.csv",
    "sector_variation": RESIDUALS / f"{PREFIX}_SECTOR_VARIATION_AUDIT.csv",
    "scaling_silence": RESIDUALS / f"{PREFIX}_LOCAL_SCALING_SILENCE_AUDIT.csv",
    "operator_coefficients": RESIDUALS / f"{PREFIX}_OPERATOR_COEFFICIENT_PACK.csv",
    "empirical_bound_map": RESIDUALS / f"{PREFIX}_EMPIRICAL_BOUND_MAP.csv",
    "countermodel": RESIDUALS / f"{PREFIX}_COUNTERMODEL_LEDGER.csv",
    "gr_bridge_status": RESIDUALS / f"{PREFIX}_GR_BRIDGE_STATUS.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2620_VALIDATION.csv",
}

SOURCES = [
    {
        "source_id": "SRC2620_00_2619_handoff_doc",
        "description": "2619 selects EH dominance and residual silence as the next target",
        "path": ROOT / "2619-Y5-R2FR-GR-left-hand-Einstein-Newton-limit-or-operator-residual-pack.md",
        "needles": ["NEXT2619_0_primary", "EH_DOMINANCE_AND_RESIDUAL_SILENCE_IS_NEXT", "DeltaE_munu"],
    },
    {
        "source_id": "SRC2620_01_2619_validation",
        "description": "2619 validation passed",
        "path": RESIDUALS / "P8_Y5_BRR545_2619_VALIDATION.csv",
        "needles": ["VAL2619_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC2620_02_2619_residual_silence",
        "description": "2619 residual-sector silence audit",
        "path": RESIDUALS / "P8_Y5_GR_LEFT_HAND_GATE_2619_RESIDUAL_SECTOR_SILENCE_AUDIT.csv",
        "needles": ["RSS2619_0_higher_derivative", "RSS2619_6_verdict"],
    },
    {
        "source_id": "SRC2620_03_2619_operator_pack",
        "description": "2619 operator residual pack",
        "path": RESIDUALS / "P8_Y5_GR_LEFT_HAND_GATE_2619_OPERATOR_RESIDUAL_PACK.csv",
        "needles": ["ORP2619_0_E_LHS_GR_residual", "ORP2619_8_nonclaim_lock"],
    },
    {
        "source_id": "SRC2620_04_2619_gr_bridge",
        "description": "2619 GR bridge status",
        "path": RESIDUALS / "P8_Y5_GR_LEFT_HAND_GATE_2619_GR_NEWTON_BRIDGE_STATUS.csv",
        "needles": ["GBS2619_1_lhs_einstein", "GBS2619_4_next"],
    },
    {
        "source_id": "SRC2620_05_2618_normal_form",
        "description": "2618 parent action normal-form owner rule",
        "path": RESIDUALS / "P8_Y5_PARENT_ACTION_NORMAL_FORM_GATE_2618_PARENT_ACTION_NORMAL_FORM_SIGNATURE.csv",
        "needles": ["ANF2618_1_geometry_left_hand_owner", "ANF2618_6_current_verdict"],
    },
    {
        "source_id": "SRC2620_06_1770_doc",
        "description": "historical EH dominance/residual-sector silence branch",
        "path": ROOT / "1770-Y5-R2FR-EH-dominance-and-residual-sector-silence-or-operator-coefficient-pack.md",
        "needles": ["EHD1770_4_current_verdict", "RSS1770_6_verdict", "NEXT1770_0_primary"],
    },
    {
        "source_id": "SRC2620_07_1770_validation",
        "description": "historical 1770 validation passed",
        "path": RESIDUALS / "P8_Y5_BRR545_1770_VALIDATION.csv",
        "needles": ["VAL1770_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC2620_08_1770_operator_coefficients",
        "description": "historical operator coefficient pack",
        "path": RESIDUALS / "P8_Y5_PARENT_QLOC_1770_OPERATOR_COEFFICIENT_PACK.csv",
        "needles": ["OPC1770_0_total_DeltaE", "OPC1770_6_source_normalization"],
    },
]


def ensure_dirs() -> None:
    for path in (RESIDUALS, LOCAL_BOUNDS, RAB_QUEUE):
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        text = read_text(source["path"])
        exists = source["path"].exists()
        needles_present = exists and all(needle in text for needle in source["needles"])
        rows.append(
            {
                "source_id": source["source_id"],
                "description": source["description"],
                "source_path": str(source["path"]),
                "exists": exists,
                "needles_present": needles_present,
                "needles": "; ".join(source["needles"]),
                "valid_for_claim": False,
            }
        )
    return rows


def lineage_rows() -> list[dict[str, Any]]:
    return [
        {
            "lineage_id": "LIN2620_0_current_handoff",
            "input_checkpoint": "2619",
            "what_it_gave": "DeltaE_munu became the exact local-GR pressure object",
            "current_use": "attempt to prove DeltaE_munu vanishes by EH dominance/residual-sector silence",
            "claim_status": "nonclaim_handoff",
            "valid_for_claim": False,
        },
        {
            "lineage_id": "LIN2620_1_source_side",
            "input_checkpoint": "2618",
            "what_it_gave": "normal-form rule: geometry/MTS variations are LHS operators, not hidden RHS source knobs",
            "current_use": "prevents using source-map cleanup as a fake proof of GR recovery",
            "claim_status": "contract_ready_parent_unsigned",
            "valid_for_claim": False,
        },
        {
            "lineage_id": "LIN2620_2_historical_eh_branch",
            "input_checkpoint": "1770",
            "what_it_gave": "first EH dominance theorem shape and coefficient-pack fallback",
            "current_use": "upgrade that branch into the current 26xx spine with 2618/2619 lineage",
            "claim_status": "historical_nonclaim",
            "valid_for_claim": False,
        },
        {
            "lineage_id": "LIN2620_3_project_status",
            "input_checkpoint": "full local branch",
            "what_it_gave": "the path to GR is now clear enough to state as a theorem contract",
            "current_use": "separate exact GR-reduction route from modified-operator route",
            "claim_status": "fork_made_explicit",
            "valid_for_claim": False,
        },
    ]


def eh_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "EHD2620_0_target",
            "claim_piece": "EH dominance in the local branch",
            "formal_statement": "S_loc = S_EH[g] + S_Lambda[g] + S_matter_min[g,Psi] + S_top + S_bdy + sum_i epsilon_i S_i",
            "required_contract": "delta(S_top+S_bdy)/delta g is silent locally and every epsilon_i delta S_i/delta g is zero or bounded below tolerance",
            "status": "TARGET_EXACT",
            "derivation_gain": "if signed, E_LHS = a(G_munu+Lambda g_munu) + DeltaE_munu with DeltaE_munu -> 0",
            "remaining_gap": "current corpus has not supplied complete sector action variations and local scaling certificates",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "EHD2620_1_variational_skeleton",
            "claim_piece": "operator split from parent variation",
            "formal_statement": "delta S_loc/delta g^{munu}=a(G_munu+Lambda g_munu)+sum_i epsilon_i E_i_munu+E_bdy_munu",
            "required_contract": "all retained terms arise from the parent action and no post-variation source shadow is introduced",
            "status": "DERIVED_CONDITIONAL_SKELETON",
            "derivation_gain": "turns GR recovery into a finite sector audit rather than a vague wish",
            "remaining_gap": "a, epsilon_i, and sector variations are not yet sourced numerically or theorem-zeroed",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "EHD2620_2_lovelock_filter",
            "claim_piece": "Einstein uniqueness route",
            "formal_statement": "metric-only + four-dimensional + local + second-order + divergence-free LHS => a G_munu + b g_munu",
            "required_contract": "extra MTS/memory/projector/coframe fields are frozen, auxiliary, pure gauge, or decoupled in the local branch",
            "status": "CONDITIONAL_FILTER_NOT_MTS_PROOF",
            "derivation_gain": "gives the least-scrutiny path: prove the parent satisfies the known uniqueness hypotheses locally",
            "remaining_gap": "MTS has not yet proven the hypotheses instead of assuming them",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "EHD2620_3_suppression_route",
            "claim_piece": "controlled nonzero residual route",
            "formal_statement": "||DeltaE_munu||/||G_munu|| <= sum_i |epsilon_i| ||E_i||/||G|| <= tau_local",
            "required_contract": "each sector needs units, scale hierarchy, coefficient source, and observable tolerance",
            "status": "BOUND_ROUTE_STAGED_NONCLAIM",
            "derivation_gain": "allows MTS to remain competitive even if exact zero fails, provided residuals are bounded honestly",
            "remaining_gap": "coefficient rows are placeholders/nonclaim until sourced",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "EHD2620_4_current_verdict",
            "claim_piece": "current MTS EH dominance",
            "formal_statement": "DeltaE_munu = 0 or ||DeltaE_munu|| <= tau_local",
            "required_contract": "all sector variation and local scaling rows must close",
            "status": "FAIL_CURRENT_PARENT_PROOF",
            "derivation_gain": "the theorem contract is now exact enough to attack sector by sector",
            "remaining_gap": "operator coefficient pack retained; no local-GR/Newton claim",
            "valid_for_claim": False,
        },
    ]


def sector_variation_rows() -> list[dict[str, Any]]:
    return [
        {
            "sector_id": "SVA2620_0_EH_core",
            "action_block": "S_EH + S_Lambda",
            "variation_target": "a(G_munu+Lambda g_munu)",
            "zero_or_owner_clause": "owned by EH core if local action coefficient a is signed and normalized",
            "current_status": "TEMPLATE_OWNER_NOT_PARENT_SIGNED",
            "coefficient_row": "OPC2620_0_EH_normalization",
            "valid_for_claim": False,
        },
        {
            "sector_id": "SVA2620_1_topological_boundary",
            "action_block": "S_top + S_bdy + reference/improvement terms",
            "variation_target": "E_top_munu + E_bdy_munu",
            "zero_or_owner_clause": "locally silent only with fixed topology, fixed boundary data, and reference chosen before readout",
            "current_status": "MISSING_BOUNDARY_TOPOLOGY_SILENCE_CERTIFICATE",
            "coefficient_row": "OPC2620_3_boundary_reference",
            "valid_for_claim": False,
        },
        {
            "sector_id": "SVA2620_2_higher_derivative",
            "action_block": "S_R2 + S_Ricci2 + S_boxR + higher operators",
            "variation_target": "E_higher_munu",
            "zero_or_owner_clause": "absent by parent grammar, topological in 4D, or suppressed by a real high scale",
            "current_status": "MISSING_OPERATOR_BASIS_VARIATION_AND_SCALE",
            "coefficient_row": "OPC2620_1_higher_derivative",
            "valid_for_claim": False,
        },
        {
            "sector_id": "SVA2620_3_projector",
            "action_block": "S_projector[Pi_M,q,e,Phi]",
            "variation_target": "E_projector_munu and [d,Pi_M]J_H",
            "zero_or_owner_clause": "projector is identity/commuting in local branch, or variation is bounded",
            "current_status": "MISSING_PROJECTOR_VARIATION_COMMUTATOR_ZERO",
            "coefficient_row": "OPC2620_2_projector",
            "valid_for_claim": False,
        },
        {
            "sector_id": "SVA2620_4_nonminimal",
            "action_block": "S_nonmin[e,Phi,X,Psi]",
            "variation_target": "E_nonminimal_munu and modified matter equations",
            "zero_or_owner_clause": "forbid direct matter-MTS couplings or reclassify them with explicit WEP/clock bounds",
            "current_status": "MISSING_NONMINIMAL_FORBID_OR_BOUND",
            "coefficient_row": "OPC2620_4_nonminimal",
            "valid_for_claim": False,
        },
        {
            "sector_id": "SVA2620_5_memory_coframe",
            "action_block": "S_memory + S_coframe + frame-lock terms",
            "variation_target": "E_memory_munu + E_frame_munu",
            "zero_or_owner_clause": "local vacuum frame lock, auxiliary elimination, or preferred-frame bounds",
            "current_status": "MISSING_LOCAL_FRAME_LOCK_VARIATION",
            "coefficient_row": "OPC2620_5_memory_coframe",
            "valid_for_claim": False,
        },
        {
            "sector_id": "SVA2620_6_nonlocal_history",
            "action_block": "S_nonlocal/history",
            "variation_target": "E_nonlocal_munu",
            "zero_or_owner_clause": "local Markov/adiabatic reduction or explicit kernel tail bound",
            "current_status": "MISSING_LOCALITY_REDUCTION_OR_KERNEL_BOUND",
            "coefficient_row": "OPC2620_6_nonlocal_history",
            "valid_for_claim": False,
        },
    ]


def scaling_silence_rows() -> list[dict[str, Any]]:
    return [
        {
            "scaling_id": "LSS2620_0_exact_zero_path",
            "sector_group": "all non-EH sectors",
            "scaling_law": "epsilon_i E_i_munu = 0 in local branch",
            "needed_inputs": "parent grammar forbids sector or Euler variation vanishes under local branch conditions",
            "current_status": "NOT_PROVED",
            "resulting_residual": "DeltaE_munu retained",
            "valid_for_claim": False,
        },
        {
            "scaling_id": "LSS2620_1_scale_suppression_path",
            "sector_group": "higher derivative and nonlocal tails",
            "scaling_law": "|epsilon_i E_i|/|G| ~ |epsilon_i| L_local^{-p_i}",
            "needed_inputs": "operator dimension p_i, coefficient units, and local curvature length",
            "current_status": "MISSING_UNITS_AND_COEFFICIENTS",
            "resulting_residual": "c_R2/c_nonlocal rows remain nonclaim",
            "valid_for_claim": False,
        },
        {
            "scaling_id": "LSS2620_2_domain_suppression_path",
            "sector_group": "projector / boundary / source readout",
            "scaling_law": "||E_projector+E_bdy|| <= U_B(A_boundary+A_projector)",
            "needed_inputs": "fixed-before-readout boundary clause, commutator norm, and local projection theorem",
            "current_status": "MISSING_COMPONENT_NORMS",
            "resulting_residual": "boundary/projector coefficient rows remain nonclaim",
            "valid_for_claim": False,
        },
        {
            "scaling_id": "LSS2620_3_frame_suppression_path",
            "sector_group": "memory/coframe/preferred frame",
            "scaling_law": "|E_frame|/|G| <= tau_PPN_alpha_i",
            "needed_inputs": "local frame-lock theorem or PPN preferred-frame projection",
            "current_status": "MISSING_FRAME_LOCK_OR_PPN_MAP",
            "resulting_residual": "c_memory/c_frame rows remain nonclaim",
            "valid_for_claim": False,
        },
        {
            "scaling_id": "LSS2620_4_verdict",
            "sector_group": "EH dominance",
            "scaling_law": "DeltaE_munu -> 0 or bounded below all local tolerances",
            "needed_inputs": "sector-by-sector action variation, local scaling, and empirical maps",
            "current_status": "RESIDUAL_SILENCE_NOT_CLOSED",
            "resulting_residual": "operator coefficient pack required",
            "valid_for_claim": False,
        },
    ]


def operator_coefficient_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "OPC2620_0_EH_normalization",
            "symbol": "a_EH",
            "meaning": "coefficient multiplying Einstein-Hilbert local operator",
            "definition": "S_EH=(a_EH/2) int sqrt(-g)(R-2 Lambda)",
            "units": "1/kappa_or_action_units",
            "status": "MISSING_PARENT_NORMALIZATION_AND_G_CALIBRATION",
            "observable_links": "Newton G, PPN normalization, cosmology background",
            "valid_for_claim": False,
        },
        {
            "row_id": "OPC2620_1_higher_derivative",
            "symbol": "c_R2,c_Ricci2,c_boxR",
            "meaning": "higher-curvature/higher-derivative LHS coefficients",
            "definition": "DeltaE_higher=sum c_i O_i_munu",
            "units": "length_power_by_operator",
            "status": "MISSING_OPERATOR_BASIS_UNITS_BOUNDS",
            "observable_links": "R10 alpha(lambda), PPN, gravitational waves, cosmology",
            "valid_for_claim": False,
        },
        {
            "row_id": "OPC2620_2_projector",
            "symbol": "c_projector",
            "meaning": "domain/projector/local readout operator residual",
            "definition": "E_projector or [d,Pi_M]J_H",
            "units": "operator_dependent",
            "status": "MISSING_PROJECTOR_ACTION_VARIATION_OR_BOUND",
            "observable_links": "measured GM, R10, WEP, orbits",
            "valid_for_claim": False,
        },
        {
            "row_id": "OPC2620_3_boundary_reference",
            "symbol": "c_boundary",
            "meaning": "boundary/reference/improvement residual coefficient",
            "definition": "DeltaE_boundary or Q_boundary residual",
            "units": "boundary_operator_dependent",
            "status": "MISSING_BOUNDARY_SILENCE_OR_BOUND",
            "observable_links": "mass charge, orbits, clock potentials",
            "valid_for_claim": False,
        },
        {
            "row_id": "OPC2620_4_nonminimal",
            "symbol": "c_nonminimal",
            "meaning": "direct matter-geometry/MTS coupling coefficient",
            "definition": "f(X,Phi)L_m or A(X)J_m",
            "units": "operator_dependent",
            "status": "MISSING_FORBID_THEOREM_OR_BOUND",
            "observable_links": "WEP, clocks, PPN, R10",
            "valid_for_claim": False,
        },
        {
            "row_id": "OPC2620_5_memory_coframe",
            "symbol": "c_memory,c_frame",
            "meaning": "memory/coframe/preferred-frame local residual coefficients",
            "definition": "E_memory + E_coframe",
            "units": "operator_dependent",
            "status": "MISSING_LOCAL_FRAME_LOCK_OR_PPN_BOUND",
            "observable_links": "PPN alpha_i, clocks, orbits",
            "valid_for_claim": False,
        },
        {
            "row_id": "OPC2620_6_nonlocal_history",
            "symbol": "c_nonlocal,K_history",
            "meaning": "nonlocal/history kernel residual",
            "definition": "E_nonlocal[g,Phi;history]",
            "units": "kernel_or_operator_dependent",
            "status": "MISSING_LOCALITY_REDUCTION_OR_KERNEL_BOUND",
            "observable_links": "clocks, orbital hysteresis, cosmology growth, wave propagation",
            "valid_for_claim": False,
        },
        {
            "row_id": "OPC2620_7_total_DeltaE",
            "symbol": "DeltaE_munu",
            "meaning": "total non-Einstein left-hand residual",
            "definition": "DeltaE_munu=sum_i c_i O_i_munu",
            "units": "curvature_operator_units",
            "status": "MISSING_ZERO_THEOREM_OR_BOUNDED_COEFFICIENTS",
            "observable_links": "PPN, R10, orbital, clocks, cosmology",
            "valid_for_claim": False,
        },
        {
            "row_id": "OPC2620_8_nonclaim_lock",
            "symbol": "claim_allowed",
            "meaning": "EH dominance/local-GR claim status",
            "definition": "claim_allowed=false until DeltaE_munu is theorem-zeroed or source-backed bounded and source normalization closes",
            "units": "status",
            "status": "NONCLAIM_LOCK",
            "observable_links": "all local arenas",
            "valid_for_claim": False,
        },
    ]


def empirical_bound_map_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "EBM2620_0_R10",
            "arena": "short-range inverse-square / Yukawa",
            "coefficient_inputs": "c_R2,c_Ricci2,c_projector,c_nonminimal",
            "needed_projection": "operator-to-alpha(lambda) map plus real bound curve",
            "current_status": "MISSING_R10_OPERATOR_MAP_OR_NUMERIC_COEFFICIENTS",
            "valid_for_claim": False,
        },
        {
            "bound_id": "EBM2620_1_PPN",
            "arena": "solar-system PPN",
            "coefficient_inputs": "DeltaE_munu,c_memory,c_frame,c_projector",
            "needed_projection": "gamma,beta,alpha_i residual equations",
            "current_status": "MISSING_PPN_RESIDUAL_MAP",
            "valid_for_claim": False,
        },
        {
            "bound_id": "EBM2620_2_clocks",
            "arena": "clock/redshift/local time",
            "coefficient_inputs": "c_nonminimal,c_memory,c_frame,a_EH",
            "needed_projection": "clock observable and redshift residual projection",
            "current_status": "MISSING_CLOCK_PROJECTION",
            "valid_for_claim": False,
        },
        {
            "bound_id": "EBM2620_3_orbits",
            "arena": "orbital dynamics",
            "coefficient_inputs": "DeltaE_munu,c_boundary,c_projector,a_EH",
            "needed_projection": "Poisson/Gauss/worldtube/exterior potential chain without GM backfill",
            "current_status": "MISSING_WORLDTUBE_GAUSS_ORBITAL_CHAIN",
            "valid_for_claim": False,
        },
        {
            "bound_id": "EBM2620_4_cosmology",
            "arena": "cosmology",
            "coefficient_inputs": "DeltaE_munu,c_R2,c_memory,c_nonlocal",
            "needed_projection": "background/growth/lensing sector equations separate from local-GR proof",
            "current_status": "HELD_FOR_COSMOLOGY_BRANCH",
            "valid_for_claim": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "countermodel_id": "CM2620_0_EH_appearance_not_dominance",
            "failure_mode": "an EH term appears in the parent action but is not dominant",
            "mathematical_form": "S_loc=S_EH+epsilon S_extra with epsilon E_extra not negligible",
            "retained": True,
            "why_survives": "appearance of EH does not by itself zero DeltaE_munu",
            "what_kills_it": "sector silence/suppression certificates for every S_extra",
            "valid_for_claim": False,
        },
        {
            "countermodel_id": "CM2620_1_lovelock_hypothesis_failure",
            "failure_mode": "Lovelock filter is invoked while MTS carries extra local fields or higher derivatives",
            "mathematical_form": "E_LHS=G+Lambda g+E_X+E_higher",
            "retained": True,
            "why_survives": "metric-only second-order hypotheses are not proven",
            "what_kills_it": "prove extra fields are auxiliary/gauge/frozen or suppressed in the local branch",
            "valid_for_claim": False,
        },
        {
            "countermodel_id": "CM2620_2_smallness_without_units",
            "failure_mode": "residuals are called small without units, coefficients, or tolerances",
            "mathematical_form": "||DeltaE||/||G|| << 1 by assertion",
            "retained": True,
            "why_survives": "no dimensional coefficient rows or observable maps have closed",
            "what_kills_it": "source-backed coefficient values and arena-specific tolerance maps",
            "valid_for_claim": False,
        },
        {
            "countermodel_id": "CM2620_3_cancellation_only",
            "failure_mode": "different residual sectors cancel in one readout but not generically",
            "mathematical_form": "sum_i c_i O_i approx 0 for a chosen observable",
            "retained": True,
            "why_survives": "no no-cancellation or independent-sector guard exists",
            "what_kills_it": "absolute-sum bound or structural zero theorem for each sector",
            "valid_for_claim": False,
        },
        {
            "countermodel_id": "CM2620_4_verdict",
            "failure_mode": "EH dominance remains unproved",
            "mathematical_form": "DeltaE_munu residual sectors retained",
            "retained": True,
            "why_survives": "2620 writes the exact contract but cannot sign sector variations/scalings from current evidence",
            "what_kills_it": "2621 sector-by-sector variation and local scaling closure, or source-backed operator bounds",
            "valid_for_claim": False,
        },
    ]


def gr_bridge_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "BGS2620_0_source_side",
            "bridge_piece": "source normal form",
            "current_status": "CONTRACT_READY_PARENT_UNSIGNED",
            "evidence": "2614-2618 plus 2619 handoff",
            "remaining_gap": "complete parent action inventory",
            "valid_for_claim": False,
        },
        {
            "status_id": "BGS2620_1_EH_dominance",
            "bridge_piece": "EH/Einstein left-hand operator",
            "current_status": "NOT_PARENT_PROVED",
            "evidence": "EHD2620_4_current_verdict",
            "remaining_gap": "sector variation and local scaling certificates",
            "valid_for_claim": False,
        },
        {
            "status_id": "BGS2620_2_operator_coefficients",
            "bridge_piece": "operator coefficient pack",
            "current_status": "STAGED_NONCLAIM",
            "evidence": "OPC2620 rows",
            "remaining_gap": "source-backed operator basis, units, maps, and bounds",
            "valid_for_claim": False,
        },
        {
            "status_id": "BGS2620_3_newton",
            "bridge_piece": "Poisson/Newton weak-field limit",
            "current_status": "BLOCKED_DOWNSTREAM",
            "evidence": "EH dominance and source normalization still open",
            "remaining_gap": "worldtube/Gauss/exterior closure",
            "valid_for_claim": False,
        },
        {
            "status_id": "BGS2620_4_next",
            "bridge_piece": "next derivation owner",
            "current_status": "SECTOR_VARIATION_AND_LOCAL_SCALING_SILENCE_IS_NEXT",
            "evidence": "SVA2620 and LSS2620 rows isolate missing certificates",
            "remaining_gap": "build 2621 sector-action variation/local scaling silence or bounds",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE2620_0_EH_dominance",
            "claim": "EH dominance is parent-derived",
            "claim_allowed": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_SECTOR_VARIATION_AND_SILENCE_CERTIFICATES_MISSING",
        },
        {
            "gate_id": "GATE2620_1_residual_silence",
            "claim": "all non-EH residual sectors are zero/suppressed",
            "claim_allowed": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_OPERATOR_BASIS_SCALING_BOUND_MAPS_MISSING",
        },
        {
            "gate_id": "GATE2620_2_operator_bounds",
            "claim": "operator coefficients have source-backed bounds",
            "claim_allowed": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_SOURCE_BACKED_COEFFICIENT_ROWS_MISSING",
        },
        {
            "gate_id": "GATE2620_3_poisson_newton",
            "claim": "Poisson/Newton limit follows",
            "claim_allowed": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_EH_DOMINANCE_AND_WORLDTUBE_GAUSS_CLOSURE_MISSING",
        },
        {
            "gate_id": "GATE2620_4_ppn_local",
            "claim": "PPN/local-GR residuals pass",
            "claim_allowed": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_PPN_OPERATOR_MAPS_MISSING",
        },
        {
            "gate_id": "GATE2620_5_public_claim",
            "claim": "local GR/Newton/R10/WEP claim allowed",
            "claim_allowed": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_EH_DOMINANCE_NOT_PROVED",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2620_0_derivation_contract",
            "decision": "EH_DOMINANCE_REQUIRES_SECTOR_SILENCE_CERTIFICATES",
            "reason": "declaring an EH core is not enough; every non-EH variation must vanish, suppress, reclassify, or be bounded",
            "next_action": "derive sector-by-sector action variations and local scaling laws",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2620_1_best_route",
            "decision": "LOVELOOCK_STYLE_FILTER_IS_LOWEST_SCRUTINY_ROUTE",
            "reason": "the cleanest GR route is proving local metric-only second-order divergence-free dynamics, not fitting GR-like behavior after the fact",
            "next_action": "audit each MTS sector against metric-only/second-order/local/no-extra-field hypotheses",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2620_2_no_promotion",
            "decision": "LOCAL_GR_NEWTON_NOT_CLAIMED",
            "reason": "DeltaE_munu, source normalization, and worldtube/Gauss closure remain open",
            "next_action": "keep all local/PPN/Newton/R10 gates blocked",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2620_3_best_next",
            "decision": "SECTOR_ACTION_VARIATION_AND_LOCAL_SCALING_SILENCE_IS_NEXT",
            "reason": "this is the smallest derivation step that can actually close or kill EH dominance",
            "next_action": "build 2621 sector-by-sector variation/scaling silence or operator-bound pack",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "NEXT2620_0_primary",
            "selection_status": "selected",
            "target_doc": "2621-Y5-R2FR-sector-action-variation-and-local-scaling-silence-or-operator-bounds.md",
            "target_script": "scripts/Y5_R2FR_sector_action_variation_and_local_scaling_silence_or_operator_bounds_2621.py",
            "objective": "vary each retained non-EH action block, estimate its local scaling against the Einstein operator, and either theorem-zero it or convert it into a source-backed bound row",
            "acceptance_gate": "every sector receives one of ZERO, SUPPRESSED_WITH_UNITS, RECLASSIFIED, or NONCLAIM_BOUND_REQUIRED",
            "claim_policy": "local GR remains blocked unless all sectors close and source normalization/worldtube closure also pass",
            "valid_for_claim": False,
        },
        {
            "route_id": "NEXT2620_1_fallback",
            "selection_status": "held_fallback",
            "target_doc": "2621b-Y5-R2FR-Poisson-Gauss-worldtube-source-normalization-pack.md",
            "target_script": "scripts/Y5_R2FR_Poisson_Gauss_worldtube_source_normalization_pack_2621b.py",
            "objective": "derive or stage the source-normalization/worldtube/Gauss bridge once the left-hand operator is sufficiently controlled",
            "acceptance_gate": "parent charge maps to exterior potential without fitted orbital GM backfill",
            "claim_policy": "downstream fallback only; do not skip EH dominance",
            "valid_for_claim": False,
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "sources": source_register_rows(),
        "lineage": lineage_rows(),
        "eh": eh_theorem_rows(),
        "sector_variation": sector_variation_rows(),
        "scaling": scaling_silence_rows(),
        "coefficients": operator_coefficient_rows(),
        "bounds": empirical_bound_map_rows(),
        "countermodel": countermodel_rows(),
        "gr_bridge": gr_bridge_status_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
        "branch_copies": [],
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def csv_parse(path: Path) -> tuple[bool, int]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            return True, sum(1 for _ in csv.DictReader(handle))
    except Exception:
        return False, 0


def copy_outputs() -> list[dict[str, Any]]:
    copy_specs = [
        (
            "COPY2620_eh_theorem",
            "eh_theorem",
            OUTPUTS["eh_theorem"],
            LOCAL_BOUNDS / "EH_dominance_theorem_attempt_2620_NONCLAIM.csv",
        ),
        (
            "COPY2620_sector_variation",
            "sector_variation",
            OUTPUTS["sector_variation"],
            LOCAL_BOUNDS / "Sector_variation_audit_2620_NONCLAIM.csv",
        ),
        (
            "COPY2620_operator_coefficients",
            "operator_coefficients",
            OUTPUTS["operator_coefficients"],
            LOCAL_BOUNDS / "Operator_coefficient_pack_2620_NONCLAIM.csv",
        ),
        (
            "COPY2620_gr_bridge_status",
            "gr_bridge_status",
            OUTPUTS["gr_bridge_status"],
            LOCAL_BOUNDS / "EH_GR_bridge_status_2620_NONCLAIM.csv",
        ),
        (
            "COPY2620_next_target",
            "next_target",
            OUTPUTS["next_target"],
            RAB_QUEUE / "JR2620_SECTOR_VARIATION_LOCAL_SCALING_NEXT.csv",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_key, source_path, target_path in copy_specs:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, target_path)
        parsed, row_count = csv_parse(target_path)
        rows.append(
            {
                "copy_id": copy_id,
                "source_key": source_key,
                "copy_path": str(target_path),
                "copy_exists": target_path.exists(),
                "csv_parse": parsed,
                "row_count": row_count,
                "valid_for_claim": False,
            }
        )
    return rows


def sources_pass(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return all(row["exists"] and row["needles_present"] for row in rows_map["sources"])


def lineage_complete(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    required = {"LIN2620_0_current_handoff", "LIN2620_1_source_side", "LIN2620_2_historical_eh_branch", "LIN2620_3_project_status"}
    return required.issubset({row["lineage_id"] for row in rows_map["lineage"]})


def eh_contract_recorded(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(row["theorem_id"] == "EHD2620_0_target" and "S_loc" in row["formal_statement"] for row in rows_map["eh"])


def eh_not_promoted(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["theorem_id"] == "EHD2620_4_current_verdict"
        and row["status"] == "FAIL_CURRENT_PARENT_PROOF"
        and not bool(row["valid_for_claim"])
        for row in rows_map["eh"]
    )


def lovelock_filter_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["theorem_id"] == "EHD2620_2_lovelock_filter"
        and row["status"] == "CONDITIONAL_FILTER_NOT_MTS_PROOF"
        for row in rows_map["eh"]
    )


def sector_variation_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return all(not bool(row["valid_for_claim"]) for row in rows_map["sector_variation"]) and any(
        row["sector_id"] == "SVA2620_5_memory_coframe" for row in rows_map["sector_variation"]
    )


def scaling_silence_not_closed(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["scaling_id"] == "LSS2620_4_verdict"
        and row["current_status"] == "RESIDUAL_SILENCE_NOT_CLOSED"
        and not bool(row["valid_for_claim"])
        for row in rows_map["scaling"]
    )


def coefficient_pack_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(row["row_id"] == "OPC2620_7_total_DeltaE" for row in rows_map["coefficients"]) and all(
        not bool(row["valid_for_claim"]) for row in rows_map["coefficients"]
    )


def empirical_map_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(row["bound_id"] == "EBM2620_1_PPN" for row in rows_map["bounds"]) and all(
        not bool(row["valid_for_claim"]) for row in rows_map["bounds"]
    )


def countermodel_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["countermodel_id"] == "CM2620_4_verdict"
        and bool(row["retained"])
        and not bool(row["valid_for_claim"])
        for row in rows_map["countermodel"]
    )


def gr_bridge_next(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["status_id"] == "BGS2620_4_next"
        and row["current_status"] == "SECTOR_VARIATION_AND_LOCAL_SCALING_SILENCE_IS_NEXT"
        for row in rows_map["gr_bridge"]
    )


def claim_gates_safe(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return all(not bool(row["claim_allowed"]) and row["status"] == "BLOCKED" for row in rows_map["claim_gates"])


def generated_rows_have_no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    claim_like_keys = {"valid_for_claim", "claim_allowed", "score_ready", "claim_ready", "public_claim_allowed"}
    for rows in rows_map.values():
        for row in rows:
            for field, value in row.items():
                if field in claim_like_keys and bool(value):
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            joined = " ".join(str(value) for value in row.values())
            if "MISSING_" in joined and bool(row.get("valid_for_claim", False)):
                return False
            if "MISSING_" in joined and str(row.get("current_status", "")).upper() == "READY":
                return False
    return True


def decision_next(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["decision_id"] == "DEC2620_3_best_next"
        and row["decision"] == "SECTOR_ACTION_VARIATION_AND_LOCAL_SCALING_SILENCE_IS_NEXT"
        for row in rows_map["decisions"]
    )


def next_selected(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["route_id"] == "NEXT2620_0_primary" and row["selection_status"] == "selected" for row in rows_map["next"]
    )


def no_formalization_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*2620*"))


def pycache_absent() -> bool:
    return not (ROOT / "scripts" / "__pycache__").exists()


def csv_parse_all() -> bool:
    keys_to_check = [key for key in OUTPUTS if key != "validation"]
    return all(csv_parse(OUTPUTS[key])[0] for key in keys_to_check if OUTPUTS[key].exists())


def branch_copies_pass(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return bool(rows_map["branch_copies"]) and all(row["copy_exists"] and row["csv_parse"] for row in rows_map["branch_copies"])


def check_row(check_id: str, passed: bool, detail: str, blocker: str = "") -> dict[str, Any]:
    return {
        "check_id": check_id,
        "result": "PASS" if passed else "FAIL",
        "detail": detail if passed else blocker,
        "valid_for_claim": False,
    }


def validation_rows(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows = [
        check_row("VAL2620_00_sources_exist", sources_pass(rows_map), "all cited source paths exist and needles are present", "one or more cited source paths or needles missing"),
        check_row("VAL2620_01_lineage_complete", lineage_complete(rows_map), "lineage covers 2619 current gate plus 2618 and historical 1770 branch", "lineage is incomplete"),
        check_row("VAL2620_02_eh_contract_recorded", eh_contract_recorded(rows_map), "EH dominance theorem contract recorded", "EH dominance contract missing"),
        check_row("VAL2620_03_eh_not_promoted", eh_not_promoted(rows_map), "EH dominance remains unproved/nonclaim", "EH dominance was promoted"),
        check_row("VAL2620_04_lovelock_filter_nonclaim", lovelock_filter_nonclaim(rows_map), "Lovelock-style filter recorded as conditional, not proof", "Lovelock filter missing or promoted"),
        check_row("VAL2620_05_sector_variation_retained", sector_variation_retained(rows_map), "sector variation audit remains nonclaim", "sector variation audit missing or promoted"),
        check_row("VAL2620_06_scaling_silence_not_closed", scaling_silence_not_closed(rows_map), "local scaling silence remains open", "local scaling silence was incorrectly closed"),
        check_row("VAL2620_07_coefficient_pack_nonclaim", coefficient_pack_nonclaim(rows_map), "operator coefficient rows remain nonclaim", "operator coefficient rows missing or promoted"),
        check_row("VAL2620_08_empirical_map_nonclaim", empirical_map_nonclaim(rows_map), "empirical bound map remains nonclaim", "empirical bound map missing or promoted"),
        check_row("VAL2620_09_countermodel_retained", countermodel_retained(rows_map), "EH dominance countermodel remains retained", "countermodel missing or promoted"),
        check_row("VAL2620_10_gr_bridge_next", gr_bridge_next(rows_map), "sector variation/local scaling selected next", "GR bridge next status missing"),
        check_row("VAL2620_11_claim_gates_safe", claim_gates_safe(rows_map), "all claim gates remain blocked/nonclaim", "one or more claim gates opened"),
        check_row("VAL2620_12_no_claim_flags", generated_rows_have_no_claim_flags(rows_map), "claim/no-score flags stay false", "one or more claim/no-score flags enabled"),
        check_row("VAL2620_13_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready", "a MISSING_* row is marked ready"),
        check_row("VAL2620_14_formalization_untouched", no_formalization_artifacts(), "no 2620 outputs found under formalization-workbench", "2620 outputs found under formalization-workbench"),
        check_row("VAL2620_15_decision_next", decision_next(rows_map), "decision selects sector action variation/local scaling route", "decision route missing"),
        check_row("VAL2620_16_next_selected", next_selected(rows_map), "next target selected", "next target missing"),
        check_row("VAL2620_17_branch_copies", branch_copies_pass(rows_map), "branch/local/queue copies exist and parse", "branch copies missing or malformed"),
        check_row("VAL2620_18_csv_parse", csv_parse_all(), "all generated 2620 CSVs parse", "one or more generated 2620 CSVs fail to parse"),
        check_row("VAL2620_19_pycache_absent", pycache_absent(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
    ]
    overall = all(row["result"] == "PASS" for row in rows)
    rows.append(
        {
            "check_id": "VAL2620_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "2620 EH dominance and residual-sector silence or operator coefficient pack",
            "valid_for_claim": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    divider = "| " + " | ".join("---" for _ in fields) + " |"
    body = []
    for row in rows:
        values = [str(row.get(field, "")).replace("|", "\\|").replace("\n", " ") for field in fields]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, divider, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validations: list[dict[str, Any]]) -> str:
    sections = [
        "# 2620 - EH Dominance And Residual Sector Silence Or Operator Coefficient Pack",
        "## Summary\n"
        "- 2620 attempts the exact EH-dominance route rather than assuming GR.\n"
        "- The theorem shape is now explicit: `S_loc = S_EH + S_Lambda + S_matter_min + S_top + S_bdy + sum_i epsilon_i S_i`; GR recovery requires every non-EH variation to vanish, suppress below tolerance, reclassify, or become a sourced coefficient row.\n"
        "- Current evidence does not close EH dominance; `DeltaE_munu` remains live and nonclaim.\n"
        "- No GitHub, public, local-GR, Newton, PPN, WEP, clock, orbital, R10, or `q_loc=0` claim is made.",
        "## Source Register\n" + markdown_table(rows_map["sources"], ["source_id", "description", "source_path", "exists", "needles_present"]),
        "## Lineage Ledger\n" + markdown_table(rows_map["lineage"], ["lineage_id", "input_checkpoint", "what_it_gave", "current_use", "claim_status"]),
        "## EH Dominance Theorem Attempt\n" + markdown_table(rows_map["eh"], ["theorem_id", "claim_piece", "formal_statement", "required_contract", "status", "derivation_gain", "remaining_gap"]),
        "## Sector Variation Audit\n" + markdown_table(rows_map["sector_variation"], ["sector_id", "action_block", "variation_target", "zero_or_owner_clause", "current_status", "coefficient_row"]),
        "## Local Scaling Silence Audit\n" + markdown_table(rows_map["scaling"], ["scaling_id", "sector_group", "scaling_law", "needed_inputs", "current_status", "resulting_residual"]),
        "## Operator Coefficient Pack\n" + markdown_table(rows_map["coefficients"], ["row_id", "symbol", "meaning", "definition", "units", "status", "observable_links"]),
        "## Empirical Bound Map\n" + markdown_table(rows_map["bounds"], ["bound_id", "arena", "coefficient_inputs", "needed_projection", "current_status"]),
        "## Countermodel Ledger\n" + markdown_table(rows_map["countermodel"], ["countermodel_id", "failure_mode", "mathematical_form", "retained", "why_survives", "what_kills_it"]),
        "## GR Bridge Status\n" + markdown_table(rows_map["gr_bridge"], ["status_id", "bridge_piece", "current_status", "evidence", "remaining_gap"]),
        "## Claim Gates\n" + markdown_table(rows_map["claim_gates"], ["gate_id", "claim", "claim_allowed", "status", "blocker"]),
        "## Decision Ledger\n" + markdown_table(rows_map["decisions"], ["decision_id", "decision", "reason", "next_action"]),
        "## Next Target\n" + markdown_table(rows_map["next"], ["route_id", "selection_status", "target_doc", "target_script", "objective", "acceptance_gate", "claim_policy"]),
        "## Branch Copies\n" + markdown_table(rows_map["branch_copies"], ["copy_id", "source_key", "copy_path", "copy_exists", "csv_parse", "row_count"]),
        "## Validation\n" + markdown_table(validations, ["check_id", "result", "detail", "valid_for_claim"]),
        "## Verdict\n"
        "This is the right kind of hard wall. We did not prove local GR yet, but we now know exactly what would count: the non-EH sectors must be varied and silenced one by one, or carried as honest coefficients into R10/PPN/clock/orbital tests. The next move is not another broad overview; it is the sector-by-sector action variation and local scaling pass.",
    ]
    return "\n\n".join(sections) + "\n"


def main() -> None:
    ensure_dirs()
    rows_map = rows_by_key()
    write_csv(OUTPUTS["source_register"], rows_map["sources"])
    write_csv(OUTPUTS["lineage_ledger"], rows_map["lineage"])
    write_csv(OUTPUTS["eh_theorem"], rows_map["eh"])
    write_csv(OUTPUTS["sector_variation"], rows_map["sector_variation"])
    write_csv(OUTPUTS["scaling_silence"], rows_map["scaling"])
    write_csv(OUTPUTS["operator_coefficients"], rows_map["coefficients"])
    write_csv(OUTPUTS["empirical_bound_map"], rows_map["bounds"])
    write_csv(OUTPUTS["countermodel"], rows_map["countermodel"])
    write_csv(OUTPUTS["gr_bridge_status"], rows_map["gr_bridge"])
    write_csv(OUTPUTS["claim_gates"], rows_map["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], rows_map["decisions"])
    write_csv(OUTPUTS["next_target"], rows_map["next"])
    rows_map["branch_copies"] = copy_outputs()
    write_csv(OUTPUTS["branch_copies"], rows_map["branch_copies"])
    validations = validation_rows(rows_map)
    write_csv(OUTPUTS["validation"], validations)
    DOC_PATH.write_text(build_markdown(rows_map, validations), encoding="utf-8")
    print(f"2620 validation {validations[-1]['result']}")
    print(f"doc={DOC_PATH}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
