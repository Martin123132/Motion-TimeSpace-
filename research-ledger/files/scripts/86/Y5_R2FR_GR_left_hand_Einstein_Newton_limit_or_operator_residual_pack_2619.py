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
DOC_PATH = ROOT / "2619-Y5-R2FR-GR-left-hand-Einstein-Newton-limit-or-operator-residual-pack.md"

PREFIX = "P8_Y5_GR_LEFT_HAND_GATE_2619"

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "lineage_ledger": RESIDUALS / f"{PREFIX}_LINEAGE_LEDGER.csv",
    "einstein_limit": RESIDUALS / f"{PREFIX}_EINSTEIN_LEFT_HAND_LIMIT_ATTEMPT.csv",
    "newton_limit": RESIDUALS / f"{PREFIX}_NEWTON_POISSON_WEAK_FIELD_ATTEMPT.csv",
    "residual_silence": RESIDUALS / f"{PREFIX}_RESIDUAL_SECTOR_SILENCE_AUDIT.csv",
    "operator_residual": RESIDUALS / f"{PREFIX}_OPERATOR_RESIDUAL_PACK.csv",
    "ppn_bridge": RESIDUALS / f"{PREFIX}_PPN_BRIDGE_LEDGER.csv",
    "empirical_bound_map": RESIDUALS / f"{PREFIX}_EMPIRICAL_BOUND_MAP.csv",
    "countermodel": RESIDUALS / f"{PREFIX}_COUNTERMODEL_LEDGER.csv",
    "gr_bridge_status": RESIDUALS / f"{PREFIX}_GR_NEWTON_BRIDGE_STATUS.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2619_VALIDATION.csv",
}

SOURCES = [
    {
        "source_id": "SRC2619_00_2618_handoff_doc",
        "description": "2618 selects the GR left-hand/Newton limit as the next target",
        "path": ROOT / "2618-Y5-R2FR-parent-action-normal-form-and-source-map-identity-signature-or-shadow-coefficient-pack.md",
        "needles": ["GR_LEFT_HAND_EINSTEIN_AND_NEWTON_LIMIT_IS_NEXT", "NEXT2618_0_primary"],
    },
    {
        "source_id": "SRC2619_01_2618_validation",
        "description": "2618 validation passed",
        "path": RESIDUALS / "P8_Y5_BRR545_2618_VALIDATION.csv",
        "needles": ["VAL2618_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC2619_02_2618_normal_form",
        "description": "current parent action normal-form owner rule",
        "path": RESIDUALS / "P8_Y5_PARENT_ACTION_NORMAL_FORM_GATE_2618_PARENT_ACTION_NORMAL_FORM_SIGNATURE.csv",
        "needles": ["ANF2618_1_geometry_left_hand_owner", "ANF2618_6_current_verdict"],
    },
    {
        "source_id": "SRC2619_03_2618_coefficients",
        "description": "current LHS/operator residual coefficient rows",
        "path": RESIDUALS / "P8_Y5_PARENT_ACTION_NORMAL_FORM_GATE_2618_SHADOW_COEFFICIENT_PACK.csv",
        "needles": ["SCP2618_3_c_lhs_GR", "SCP2618_4_R_total_residual"],
    },
    {
        "source_id": "SRC2619_04_2618_gr_bridge",
        "description": "current GR bridge status",
        "path": RESIDUALS / "P8_Y5_PARENT_ACTION_NORMAL_FORM_GATE_2618_GR_BRIDGE_STATUS.csv",
        "needles": ["GRB2618_1_lhs_operator", "GRB2618_4_next"],
    },
    {
        "source_id": "SRC2619_05_1769_doc",
        "description": "historical GR left-hand/Newton bridge pack",
        "path": ROOT / "1769-Y5-R2FR-GR-left-hand-Einstein-Newton-limit-or-operator-residual-pack.md",
        "needles": ["ELH1769_4_current_verdict", "NWF1769_1_poisson_conditional", "NEXT1769_0_primary"],
    },
    {
        "source_id": "SRC2619_06_1769_operator_pack",
        "description": "historical operator residual pack",
        "path": RESIDUALS / "P8_Y5_PARENT_QLOC_1769_OPERATOR_RESIDUAL_PACK.csv",
        "needles": ["ORP1769_0_E_LHS_GR_residual", "ORP1769_6_nonclaim_lock"],
    },
    {
        "source_id": "SRC2619_07_1770_doc",
        "description": "historical EH dominance/residual-sector silence checkpoint",
        "path": ROOT / "1770-Y5-R2FR-EH-dominance-and-residual-sector-silence-or-operator-coefficient-pack.md",
        "needles": ["EHD1770_4_current_verdict", "OPC1770_0_total_DeltaE", "NEXT1770_0_primary"],
    },
    {
        "source_id": "SRC2619_08_1770_residual_silence",
        "description": "historical residual-sector silence audit",
        "path": RESIDUALS / "P8_Y5_PARENT_QLOC_1770_RESIDUAL_SECTOR_SILENCE_AUDIT.csv",
        "needles": ["RSS1770_0_higher_derivative", "RSS1770_6_verdict"],
    },
    {
        "source_id": "SRC2619_09_1770_operator_coefficients",
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
            "lineage_id": "LIN2619_0_current_pivot",
            "input_checkpoint": "2618",
            "what_it_gave": "source-side normal form and owner rule: geometry/MTS variations live on the LHS",
            "current_use": "attach the current source-normal-form stack to an explicit Einstein/Newton LHS gate",
            "claim_status": "nonclaim",
            "valid_for_claim": False,
        },
        {
            "lineage_id": "LIN2619_1_historical_bridge",
            "input_checkpoint": "1769",
            "what_it_gave": "conditional bridge: EH LHS plus Hilbert source gives Einstein equation; weak-field 00 component gives Poisson",
            "current_use": "reuse as the exact bridge shape, not as a proof that MTS has EH dominance",
            "claim_status": "conditional_template",
            "valid_for_claim": False,
        },
        {
            "lineage_id": "LIN2619_2_historical_eh_dominance",
            "input_checkpoint": "1770",
            "what_it_gave": "residual-sector silence audit and operator coefficient pack",
            "current_use": "identify the next non-circular derivation target after the GR bridge is restated in the 26xx branch",
            "claim_status": "nonclaim_lineage",
            "valid_for_claim": False,
        },
        {
            "lineage_id": "LIN2619_3_current_pressure_point",
            "input_checkpoint": "2614-2618",
            "what_it_gave": "source coupling narrowed enough that the RHS cannot be used as the excuse anymore",
            "current_use": "make DeltaE_munu the central missing object",
            "claim_status": "pressure_point_selected",
            "valid_for_claim": False,
        },
        {
            "lineage_id": "LIN2619_4_claim_policy",
            "input_checkpoint": "all",
            "what_it_gave": "no local-GR/Newton claim while EH dominance, source normalization, and residual silence remain unsigned",
            "current_use": "keep this private and block all public scoring rows",
            "claim_status": "nonclaim_lock",
            "valid_for_claim": False,
        },
    ]


def einstein_limit_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "ELH2619_0_target",
            "claim_piece": "left-hand operator reduces to Einstein form",
            "formal_statement": "E_LHS[g,Phi,X] = G_munu + Lambda g_munu + DeltaE_munu",
            "status": "TARGET_EXACT",
            "conditional_gain": "GR recovery is possible only if DeltaE_munu is zero, silent, or bounded beneath local tolerance",
            "remaining_gap": "parent action has not signed EH dominance or residual-sector silence",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "ELH2619_1_EH_variation_template",
            "claim_piece": "Einstein-Hilbert variation",
            "formal_statement": "delta S_EH/delta g^{munu} -> G_munu + Lambda g_munu",
            "status": "REFERENCE_THEOREM_NONCLAIM",
            "conditional_gain": "if the MTS local parent action reduces to EH plus silent sectors, the Einstein LHS follows",
            "remaining_gap": "EH template is not an MTS proof; it must be derived from the parent normal form",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "ELH2619_2_lovelock_filter",
            "claim_piece": "why Einstein is the low-risk route",
            "formal_statement": "in four-dimensional local metric-only second-order diffeomorphism-invariant dynamics, the divergence-free rank-2 LHS is a G_munu + b g_munu",
            "status": "CONDITIONAL_FILTER",
            "conditional_gain": "this gives the cleanest route to GR if MTS can prove local metric-only, second-order, no-extra-sector conditions",
            "remaining_gap": "MTS still carries possible motion, memory, projector, boundary, nonminimal, and higher-operator sectors",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "ELH2619_3_residual_decomposition",
            "claim_piece": "MTS operator residual split",
            "formal_statement": "DeltaE_munu = E_higher + E_projector + E_boundary + E_nonminimal + E_memory + E_coframe + E_nonlocal",
            "status": "DECOMPOSITION_WRITTEN",
            "conditional_gain": "turns vague not-GR risk into named zero-or-bound targets",
            "remaining_gap": "each sector still needs an action variation, local scaling theorem, or source-backed bound",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "ELH2619_4_bianchi_gate",
            "claim_piece": "Noether/Bianchi compatibility",
            "formal_statement": "nabla_mu(G^{mu nu}+Lambda g^{mu nu}+DeltaE^{mu nu}) = kappa nabla_mu T_H^{mu nu}",
            "status": "CONDITIONAL_PARENT_ACTION_IDENTITY",
            "conditional_gain": "a complete diffeomorphism-invariant parent action can make the final system divergence-consistent",
            "remaining_gap": "dropped or reclassified residuals must not break the identity",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "ELH2619_5_current_verdict",
            "claim_piece": "current MTS Einstein left-hand limit",
            "formal_statement": "E_LHS -> G_munu + Lambda g_munu",
            "status": "CONDITIONAL_THEOREM_NOT_PARENT_PROOF",
            "conditional_gain": "the route is sharp enough to test: prove EH dominance or carry DeltaE_munu into PPN/R10/orbital/clock rows",
            "remaining_gap": "no local-GR claim; DeltaE_munu remains live",
            "valid_for_claim": False,
        },
    ]


def newton_limit_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "NWF2619_0_metric_ansatz",
            "claim_piece": "weak-field metric expansion",
            "formal_statement": "g_00=-(1+2Phi/c^2+O(c^-4)), g_ij=(1-2Psi/c^2)delta_ij+O(c^-4)",
            "status": "STANDARD_WEAK_FIELD_TEMPLATE",
            "conditional_gain": "sets the language for Newton/PPN once the parent LHS is Einstein-dominant",
            "remaining_gap": "observer/coframe map and local-frame lock are not parent-signed here",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "NWF2619_1_poisson_conditional",
            "claim_piece": "Poisson equation from Einstein 00 component",
            "formal_statement": "G_00 ~= 2 nabla^2 Phi/c^2 and T_00 ~= rho c^2 imply nabla^2 Phi = 4 pi G rho",
            "status": "DERIVED_CONDITIONAL_TEMPLATE",
            "conditional_gain": "Poisson follows if EH normalization, clean Hilbert source, and DeltaE_00 silence are signed",
            "remaining_gap": "same parent charge must identify rho_H and measured G without orbital backfill",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "NWF2619_2_inverse_square_worldtube",
            "claim_piece": "Newton inverse-square exterior",
            "formal_statement": "integral nabla^2 Phi dV = 4 pi G M_H gives Phi=-G M_H/r outside a closed source when Gauss/worldtube closure holds",
            "status": "CONDITIONAL_GAUSS_TEMPLATE",
            "conditional_gain": "links Poisson to inverse-square acceleration without using fitted orbital GM as the premise",
            "remaining_gap": "worldtube/exterior closure and source normalization still need a parent proof",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "NWF2619_3_ppn_gamma_beta",
            "claim_piece": "PPN bridge",
            "formal_statement": "gamma=Psi/Phi=1 and beta=1 only after EH nonlinear completion and residual silence",
            "status": "CONDITIONAL_PPN_TEMPLATE",
            "conditional_gain": "names the local-GR observables that will punish surviving DeltaE sectors",
            "remaining_gap": "PPN residual map and preferred-frame terms remain open",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "NWF2619_4_current_verdict",
            "claim_piece": "current MTS Newton/Poisson limit",
            "formal_statement": "nabla^2 Phi = 4 pi G_ref rho_H and a=-nabla Phi",
            "status": "CONDITIONAL_NOT_PARENT_DERIVED",
            "conditional_gain": "Newton is a near-direct corollary after EH dominance, source normalization, and worldtube closure",
            "remaining_gap": "no Newton/local-GR claim from 2619",
            "valid_for_claim": False,
        },
    ]


def residual_silence_rows() -> list[dict[str, Any]]:
    return [
        {
            "sector_id": "RSS2619_0_higher_derivative",
            "sector": "higher-curvature / higher-derivative LHS operators",
            "representative_operator": "c_R2 R^2 + c_Ricci2 R_munu R^munu + c_boxR R box R",
            "required_silence_condition": "absent by parent normal form or suppressed by a real high scale below all local tolerances",
            "current_status": "MISSING_OPERATOR_BASIS_AND_SCALE",
            "coefficient_row": "ORP2619_1_higher_derivative",
            "valid_for_claim": False,
        },
        {
            "sector_id": "RSS2619_1_projector",
            "sector": "domain/projector/mass-readout operator",
            "representative_operator": "E_projector or [d,Pi_M]J_H obstruction",
            "required_silence_condition": "projector is identity/commutes in local branch, or obstruction is explicitly bounded",
            "current_status": "MISSING_PARENT_PROJECTOR_VARIATION_AND_COMMUTATOR_ZERO",
            "coefficient_row": "ORP2619_2_projector_operator",
            "valid_for_claim": False,
        },
        {
            "sector_id": "RSS2619_2_boundary",
            "sector": "boundary/reference/improvement",
            "representative_operator": "DeltaE_boundary, Q_boundary, counterterm/improvement residual",
            "required_silence_condition": "fixed-before-readout boundary reference plus local/falloff boundary silence",
            "current_status": "MISSING_BOUNDARY_SILENCE_AND_FIXED_REFERENCE",
            "coefficient_row": "ORP2619_3_boundary_reference",
            "valid_for_claim": False,
        },
        {
            "sector_id": "RSS2619_3_nonminimal",
            "sector": "direct matter-geometry/MTS nonminimal coupling",
            "representative_operator": "f(X,Phi)L_m or A(X)J_m",
            "required_silence_condition": "forbid theorem, reclassification into geometry, or WEP/clock/PPN/R10 bound",
            "current_status": "MISSING_FORBID_OR_BOUND",
            "coefficient_row": "ORP2619_4_nonminimal_matter_geometry",
            "valid_for_claim": False,
        },
        {
            "sector_id": "RSS2619_4_memory_coframe",
            "sector": "memory/coframe/preferred-frame residual",
            "representative_operator": "E_memory + E_coframe + local-frame-lock residual",
            "required_silence_condition": "local vacuum/coframe lock theorem or preferred-frame bounds",
            "current_status": "MISSING_LOCAL_FRAME_LOCK_OR_BOUND",
            "coefficient_row": "ORP2619_5_memory_coframe",
            "valid_for_claim": False,
        },
        {
            "sector_id": "RSS2619_5_nonlocal",
            "sector": "nonlocal/history operator",
            "representative_operator": "E_nonlocal[g,Phi; history]",
            "required_silence_condition": "local branch Markov/adiabatic reduction or explicit nonlocal kernel bound",
            "current_status": "MISSING_LOCALITY_REDUCTION_OR_KERNEL_BOUND",
            "coefficient_row": "ORP2619_6_nonlocal_history",
            "valid_for_claim": False,
        },
        {
            "sector_id": "RSS2619_6_verdict",
            "sector": "all non-EH residual sectors",
            "representative_operator": "DeltaE_munu=sum_i epsilon_i E_i",
            "required_silence_condition": "every retained sector is zeroed, suppressed, reclassified, or source-backed bounded",
            "current_status": "RESIDUAL_SECTORS_RETAINED_NONCLAIM",
            "coefficient_row": "ORP2619_0_E_LHS_GR_residual",
            "valid_for_claim": False,
        },
    ]


def operator_residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "ORP2619_0_E_LHS_GR_residual",
            "symbol": "DeltaE_munu",
            "meaning": "left-hand deviation from Einstein operator",
            "definition": "DeltaE_munu = E_LHS - (G_munu + Lambda g_munu)",
            "units": "curvature_operator_units",
            "status": "MISSING_EH_DOMINANCE_OR_COEFFICIENT_MAP",
            "observable_links": "PPN gamma,beta; R10 alpha(lambda); clocks; orbital precession; cosmology growth",
            "valid_for_claim": False,
        },
        {
            "row_id": "ORP2619_1_higher_derivative",
            "symbol": "c_R2/c_Ricci2/c_boxR",
            "meaning": "higher-curvature left-hand corrections",
            "definition": "c_R2 R^2 + c_Ricci2 R_munu R^munu + c_boxR R box R",
            "units": "length_power_by_operator",
            "status": "MISSING_OPERATOR_BASIS_AND_BOUNDS",
            "observable_links": "short-range gravity, PPN, waves, cosmology",
            "valid_for_claim": False,
        },
        {
            "row_id": "ORP2619_2_projector_operator",
            "symbol": "c_projector/Pi_M_operator",
            "meaning": "domain/projector modification to LHS/source readout",
            "definition": "E_projector or [d,Pi_M]J_H obstruction",
            "units": "operator_dependent",
            "status": "MISSING_PARENT_PROJECTOR_VARIATION",
            "observable_links": "measured GM, R10, WEP, orbital systems",
            "valid_for_claim": False,
        },
        {
            "row_id": "ORP2619_3_boundary_reference",
            "symbol": "c_boundary/reference",
            "meaning": "boundary/counterterm/improvement deviation",
            "definition": "DeltaE_boundary or Q_boundary residual fixed before readout",
            "units": "boundary_operator_dependent",
            "status": "MISSING_FIXED_BEFORE_READOUT_BOUNDARY_SILENCE",
            "observable_links": "mass charge, orbital GM, local clocks",
            "valid_for_claim": False,
        },
        {
            "row_id": "ORP2619_4_nonminimal_matter_geometry",
            "symbol": "c_nonminimal",
            "meaning": "ordinary matter coupled directly to MTS/geometric scalars",
            "definition": "f(X,Phi)L_m or A(X)J_m",
            "units": "operator_dependent",
            "status": "MISSING_FORBID_OR_BOUND",
            "observable_links": "WEP, clocks, PPN, R10",
            "valid_for_claim": False,
        },
        {
            "row_id": "ORP2619_5_memory_coframe",
            "symbol": "c_memory/c_frame",
            "meaning": "memory/coframe/preferred-frame local residual coefficients",
            "definition": "E_memory + E_coframe + local-frame-lock residual",
            "units": "operator_dependent",
            "status": "MISSING_LOCAL_FRAME_LOCK_OR_PPN_BOUND",
            "observable_links": "PPN alpha_i, clocks, orbits",
            "valid_for_claim": False,
        },
        {
            "row_id": "ORP2619_6_nonlocal_history",
            "symbol": "c_nonlocal/K_history",
            "meaning": "nonlocal/history operator tail in the local branch",
            "definition": "E_nonlocal[g,Phi;history] or kernel memory correction to E_LHS",
            "units": "kernel_or_operator_dependent",
            "status": "MISSING_LOCALITY_REDUCTION_OR_BOUND",
            "observable_links": "clocks, orbital hysteresis, cosmology growth, wave propagation",
            "valid_for_claim": False,
        },
        {
            "row_id": "ORP2619_7_source_normalization",
            "symbol": "delta_G_source/M_H_ref",
            "meaning": "same charge must normalize Poisson and measured GM",
            "definition": "G_ref M_H_ref = surface/exterior charge before orbital fitting",
            "units": "GM_or_fractional",
            "status": "MISSING_POISSON_GAUSS_WORLDTUBE_GLUE",
            "observable_links": "Newtonian orbit, Cavendish/local G, ephemerides",
            "valid_for_claim": False,
        },
        {
            "row_id": "ORP2619_8_nonclaim_lock",
            "symbol": "claim_allowed",
            "meaning": "local-GR/Newton claim status",
            "definition": "claim_allowed=false until every residual is zeroed or bounded and source normalization closes",
            "units": "status",
            "status": "NONCLAIM_LOCK",
            "observable_links": "all local arenas",
            "valid_for_claim": False,
        },
    ]


def ppn_bridge_rows() -> list[dict[str, Any]]:
    return [
        {
            "ppn_id": "PPN2619_0_gamma",
            "parameter": "gamma-1",
            "needed_parent_result": "spatial and temporal weak-field potentials equal after DeltaE silence",
            "formal_readout": "gamma = Psi/Phi = 1 + delta_gamma_residual",
            "status": "MISSING_PARENT_P_EQUALS_1_OR_EH_DOMINANCE",
            "valid_for_claim": False,
        },
        {
            "ppn_id": "PPN2619_1_beta",
            "parameter": "beta-1",
            "needed_parent_result": "nonlinear EH completion dominates at O(Phi^2)",
            "formal_readout": "g_00=-1+2U/c^2-2 beta U^2/c^4+...",
            "status": "MISSING_NONLINEAR_COMPLETION",
            "valid_for_claim": False,
        },
        {
            "ppn_id": "PPN2619_2_preferred_frame",
            "parameter": "alpha1/alpha2/alpha3",
            "needed_parent_result": "observer/coframe and motion field do not create preferred-frame residuals in local branch",
            "formal_readout": "alpha_i = alpha_i(E_projector,E_memory,E_coframe)",
            "status": "MISSING_LOCAL_FRAME_LOCK_OR_BOUND",
            "valid_for_claim": False,
        },
        {
            "ppn_id": "PPN2619_3_yukawa",
            "parameter": "alpha(lambda)",
            "needed_parent_result": "extra operator tails absent or bounded",
            "formal_readout": "Phi(r)=-(GM/r)(1+alpha exp(-r/lambda))",
            "status": "MISSING_R10_OPERATOR_MAP",
            "valid_for_claim": False,
        },
        {
            "ppn_id": "PPN2619_4_verdict",
            "parameter": "PPN/local-GR lane",
            "needed_parent_result": "EH dominance plus residual silence plus source normalization",
            "formal_readout": "gamma=beta=1 and alpha_i=0 only after gates pass",
            "status": "PPN_BRIDGE_LEDGER_READY_NONCLAIM",
            "valid_for_claim": False,
        },
    ]


def empirical_bound_map_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "EBM2619_0_ppn_gamma_beta",
            "arena": "PPN gamma beta",
            "residuals": "c_R2,c_projector,c_memory,c_frame,DeltaE_munu",
            "needed_map": "derive gamma=beta=1 or map coefficients to PPN residuals",
            "status": "MISSING_PPN_RESIDUAL_MAP",
            "valid_for_claim": False,
        },
        {
            "bound_id": "EBM2619_1_R10_yukawa",
            "arena": "short-range alpha(lambda)",
            "residuals": "c_R2,c_Ricci2,c_projector,c_nonminimal",
            "needed_map": "operator-to-Yukawa map and source-backed bound curve",
            "status": "MISSING_R10_OPERATOR_MAP",
            "valid_for_claim": False,
        },
        {
            "bound_id": "EBM2619_2_clocks",
            "arena": "clock redshift/local time residuals",
            "residuals": "c_nonminimal,c_memory,c_frame,delta_G_source",
            "needed_map": "clock observable projection and bound",
            "status": "MISSING_CLOCK_PROJECTION",
            "valid_for_claim": False,
        },
        {
            "bound_id": "EBM2619_3_orbits",
            "arena": "perihelion/precession/ephemeris residual",
            "residuals": "DeltaE_munu,delta_G_source,c_boundary,c_projector",
            "needed_map": "Poisson/Gauss/worldtube closure then orbital readout",
            "status": "MISSING_ORBITAL_READOUT_WITHOUT_GM_BACKFILL",
            "valid_for_claim": False,
        },
        {
            "bound_id": "EBM2619_4_cosmology",
            "arena": "growth/lensing/background expansion residual",
            "residuals": "c_R2,c_memory,c_frame,DeltaE_munu",
            "needed_map": "separate cosmology branch; not a local-GR substitute",
            "status": "HELD_FOR_COSMOLOGY_BRANCH",
            "valid_for_claim": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "countermodel_id": "CM2619_0_EH_anchor_import",
            "failure_mode": "EH action is used as the whole MTS parent action without residual certificates",
            "mathematical_form": "S_parent := S_EH by assertion",
            "retained": True,
            "why_survives": "2618 supplies an action-normal-form signature, not an EH reduction proof",
            "what_kills_it": "sector-by-sector parent action reduction/silence certificates",
            "valid_for_claim": False,
        },
        {
            "countermodel_id": "CM2619_1_nonEH_operator_tail",
            "failure_mode": "extra left-hand operator survives weak-field limit",
            "mathematical_form": "DeltaE_00 != 0 gives modified Poisson/Yukawa/PPN residual",
            "retained": True,
            "why_survives": "no EH-dominance theorem or coefficient map has been supplied",
            "what_kills_it": "zero/suppression theorem or source-backed operator coefficient bounds",
            "valid_for_claim": False,
        },
        {
            "countermodel_id": "CM2619_2_source_normalization_laundering",
            "failure_mode": "orbital GM is used to prove the same Newtonian GM",
            "mathematical_form": "M_ref := GM_orbit/G_ref before Poisson/Gauss bridge",
            "retained": True,
            "why_survives": "Poisson source charge and exterior mass have not been glued without backfill",
            "what_kills_it": "parent charge -> Gauss flux -> exterior orbit chain before fitting",
            "valid_for_claim": False,
        },
        {
            "countermodel_id": "CM2619_3_ppn_residual",
            "failure_mode": "weak-field metric has gamma or beta deviation",
            "mathematical_form": "gamma-1 or beta-1 sourced by DeltaE/projector/coframe residual",
            "retained": True,
            "why_survives": "local frame lock and nonlinear completion are not parent-derived",
            "what_kills_it": "derive gamma=1 and beta=1 from EH-dominant local branch or bound PPN residuals",
            "valid_for_claim": False,
        },
        {
            "countermodel_id": "CM2619_4_verdict",
            "failure_mode": "GR/Newton recovery remains conditional",
            "mathematical_form": "E_LHS = G + Lambda g + DeltaE; DeltaE and source normalization not closed",
            "retained": True,
            "why_survives": "2619 writes the bridge but does not parent-sign EH dominance/Newton normalization",
            "what_kills_it": "2620 EH dominance/residual-sector silence plus operator coefficient validation",
            "valid_for_claim": False,
        },
    ]


def gr_bridge_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "GBS2619_0_source_side",
            "bridge_piece": "RHS Hilbert source / source-shadow control",
            "current_status": "CONTRACT_READY_PARENT_UNSIGNED",
            "evidence": "2614-2618",
            "remaining_gap": "complete action inventory and source-map identity signature",
            "valid_for_claim": False,
        },
        {
            "status_id": "GBS2619_1_lhs_einstein",
            "bridge_piece": "Einstein left-hand operator",
            "current_status": "CONDITIONAL_TEMPLATE_NOT_PARENT_PROOF",
            "evidence": "ELH2619_1 through ELH2619_5",
            "remaining_gap": "EH dominance and residual-sector silence",
            "valid_for_claim": False,
        },
        {
            "status_id": "GBS2619_2_newton",
            "bridge_piece": "Poisson/Newton weak-field limit",
            "current_status": "CONDITIONAL_NOT_PARENT_DERIVED",
            "evidence": "NWF2619_1 through NWF2619_4",
            "remaining_gap": "source normalization, worldtube/exterior closure, residual-free weak field",
            "valid_for_claim": False,
        },
        {
            "status_id": "GBS2619_3_ppn",
            "bridge_piece": "PPN local-GR lane",
            "current_status": "RESIDUAL_MAP_READY_NONCLAIM",
            "evidence": "PPN2619 rows",
            "remaining_gap": "gamma beta preferred-frame and Yukawa residual maps",
            "valid_for_claim": False,
        },
        {
            "status_id": "GBS2619_4_next",
            "bridge_piece": "next derivation owner",
            "current_status": "EH_DOMINANCE_AND_RESIDUAL_SILENCE_IS_NEXT",
            "evidence": "operator residual pack isolates the remaining LHS blockers",
            "remaining_gap": "build 2620 residual-sector silence or operator coefficient pack",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE2619_0_EH_dominance",
            "claim": "parent LHS reduces to Einstein tensor plus Lambda",
            "claim_allowed": False,
            "status": "NONCLAIM_THEOREM_GATE",
            "blocker": "BLOCKED_EH_DOMINANCE_AND_RESIDUAL_SILENCE_UNSIGNED",
        },
        {
            "gate_id": "GATE2619_1_bianchi",
            "claim": "final LHS/RHS system has parent Noether/Bianchi identity",
            "claim_allowed": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_PARENT_CURRENT_CHAIN_SECTOR_CERTIFICATES_INCOMPLETE",
        },
        {
            "gate_id": "GATE2619_2_poisson",
            "claim": "Poisson equation follows from MTS parent weak-field limit",
            "claim_allowed": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_SOURCE_NORMALIZATION_AND_LHS_RESIDUALS_OPEN",
        },
        {
            "gate_id": "GATE2619_3_newton_orbit",
            "claim": "inverse-square Newtonian orbit follows without orbital GM backfill",
            "claim_allowed": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_WORLDTUBE_GAUSS_EXTERIOR_CLOSURE_MISSING",
        },
        {
            "gate_id": "GATE2619_4_ppn",
            "claim": "PPN gamma=1 beta=1 preferred-frame terms zero",
            "claim_allowed": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_PPN_RESIDUAL_MAPS_AND_BOUNDS_MISSING",
        },
        {
            "gate_id": "GATE2619_5_local_GR",
            "claim": "local GR/Newton recovery is derived",
            "claim_allowed": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_OPERATOR_RESIDUAL_PACK_NOT_ZEROED_OR_BOUNDED",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2619_0_conditional_bridge",
            "decision": "GR_NEWTON_BRIDGE_SHAPE_IS_EXACT_CONDITIONALLY",
            "reason": "EH LHS plus clean Hilbert source gives Einstein equation and Poisson/Newton in the weak-field limit",
            "next_action": "do not claim it until MTS parent reduction to EH plus silent/bounded residuals is signed",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2619_1_no_import",
            "decision": "EH_TEMPLATE_NOT_MTS_PROOF",
            "reason": "2618 makes LHS ownership explicit but does not prove the operator is EH",
            "next_action": "keep EH as the target template and require MTS residual certificates",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2619_2_residual_pack",
            "decision": "OPERATOR_RESIDUAL_PACK_STAGED",
            "reason": "if LHS residuals do not theorem-zero, they must become coefficient rows tied to PPN/R10/orbital/clock tests",
            "next_action": "stage zero-or-bound decisions for each residual sector",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2619_3_best_next",
            "decision": "EH_DOMINANCE_RESIDUAL_SILENCE_AND_OPERATOR_COEFFICIENTS_IS_NEXT",
            "reason": "this is the exact gate between a GR-reduction programme and a modified-operator residual model",
            "next_action": "build 2620 EH dominance/residual-sector silence theorem or operator coefficient pack",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "NEXT2619_0_primary",
            "selection_status": "selected",
            "target_doc": "2620-Y5-R2FR-EH-dominance-and-residual-sector-silence-or-operator-coefficient-pack.md",
            "target_script": "scripts/Y5_R2FR_EH_dominance_and_residual_sector_silence_or_operator_coefficient_pack_2620.py",
            "objective": "prove MTS parent LHS reduces to EH/Einstein operator in the local branch by zeroing/suppressing residual sectors, or stage explicit operator coefficients for PPN/R10/orbital/clock bounds",
            "acceptance_gate": "DeltaE_munu is either theorem-zero/suppressed below tolerance or carried as sourced nonclaim coefficient rows",
            "claim_policy": "do not claim local GR/Newton until both source normal form and LHS operator limits pass",
            "valid_for_claim": False,
        },
        {
            "route_id": "NEXT2619_1_fallback",
            "selection_status": "held_fallback",
            "target_doc": "2620b-Y5-R2FR-Poisson-Gauss-worldtube-source-normalization-pack.md",
            "target_script": "scripts/Y5_R2FR_Poisson_Gauss_worldtube_source_normalization_pack_2620b.py",
            "objective": "derive or stage the source-normalization/worldtube/Gauss bridge needed before measured GM or inverse-square orbital claims",
            "acceptance_gate": "parent charge maps to exterior potential before orbital backfill",
            "claim_policy": "no fitted GM denominator is allowed as a premise",
            "valid_for_claim": False,
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "sources": source_register_rows(),
        "lineage": lineage_rows(),
        "einstein": einstein_limit_rows(),
        "newton": newton_limit_rows(),
        "silence": residual_silence_rows(),
        "operator": operator_residual_rows(),
        "ppn": ppn_bridge_rows(),
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
            "COPY2619_einstein_limit",
            "einstein_limit",
            OUTPUTS["einstein_limit"],
            LOCAL_BOUNDS / "Einstein_left_hand_limit_attempt_2619_NONCLAIM.csv",
        ),
        (
            "COPY2619_operator_residual",
            "operator_residual",
            OUTPUTS["operator_residual"],
            LOCAL_BOUNDS / "Operator_residual_pack_2619_NONCLAIM.csv",
        ),
        (
            "COPY2619_ppn_bridge",
            "ppn_bridge",
            OUTPUTS["ppn_bridge"],
            LOCAL_BOUNDS / "PPN_bridge_2619_NONCLAIM.csv",
        ),
        (
            "COPY2619_gr_bridge_status",
            "gr_bridge_status",
            OUTPUTS["gr_bridge_status"],
            LOCAL_BOUNDS / "GR_Newton_bridge_status_2619_NONCLAIM.csv",
        ),
        (
            "COPY2619_next_target",
            "next_target",
            OUTPUTS["next_target"],
            RAB_QUEUE / "JR2619_EH_DOMINANCE_RESIDUAL_SILENCE_NEXT.csv",
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
    ids = {row["lineage_id"] for row in rows_map["lineage"]}
    required = {"LIN2619_0_current_pivot", "LIN2619_1_historical_bridge", "LIN2619_2_historical_eh_dominance", "LIN2619_3_current_pressure_point"}
    return required.issubset(ids)


def einstein_template_recorded(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(row["attempt_id"] == "ELH2619_1_EH_variation_template" for row in rows_map["einstein"])


def einstein_not_promoted(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["attempt_id"] == "ELH2619_5_current_verdict"
        and row["status"] == "CONDITIONAL_THEOREM_NOT_PARENT_PROOF"
        and not bool(row["valid_for_claim"])
        for row in rows_map["einstein"]
    )


def deltae_decomposition_recorded(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["attempt_id"] == "ELH2619_3_residual_decomposition"
        and "DeltaE_munu" in row["formal_statement"]
        for row in rows_map["einstein"]
    )


def newton_template_recorded(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(row["attempt_id"] == "NWF2619_1_poisson_conditional" for row in rows_map["newton"])


def residual_pack_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    rows = rows_map["operator"]
    return any(row["row_id"] == "ORP2619_0_E_LHS_GR_residual" for row in rows) and all(
        not bool(row["valid_for_claim"]) for row in rows
    )


def silence_audit_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["sector_id"] == "RSS2619_6_verdict"
        and row["current_status"] == "RESIDUAL_SECTORS_RETAINED_NONCLAIM"
        and not bool(row["valid_for_claim"])
        for row in rows_map["silence"]
    )


def ppn_bridge_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["ppn_id"] == "PPN2619_4_verdict"
        and row["status"] == "PPN_BRIDGE_LEDGER_READY_NONCLAIM"
        and not bool(row["valid_for_claim"])
        for row in rows_map["ppn"]
    )


def empirical_map_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return all(not bool(row["valid_for_claim"]) for row in rows_map["bounds"]) and any(
        row["bound_id"] == "EBM2619_1_R10_yukawa" for row in rows_map["bounds"]
    )


def countermodel_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["countermodel_id"] == "CM2619_4_verdict"
        and bool(row["retained"])
        and not bool(row["valid_for_claim"])
        for row in rows_map["countermodel"]
    )


def bridge_next(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["status_id"] == "GBS2619_4_next"
        and row["current_status"] == "EH_DOMINANCE_AND_RESIDUAL_SILENCE_IS_NEXT"
        for row in rows_map["gr_bridge"]
    )


def claim_gates_safe(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return all(not bool(row["claim_allowed"]) and row["status"] in {"BLOCKED", "NONCLAIM_THEOREM_GATE"} for row in rows_map["claim_gates"])


def generated_rows_have_no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    claim_like_keys = {"valid_for_claim", "claim_allowed", "score_ready", "claim_ready", "public_claim_allowed"}
    for key, rows in rows_map.items():
        if key == "validation":
            continue
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
        row["decision_id"] == "DEC2619_3_best_next"
        and row["decision"] == "EH_DOMINANCE_RESIDUAL_SILENCE_AND_OPERATOR_COEFFICIENTS_IS_NEXT"
        for row in rows_map["decisions"]
    )


def next_selected(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["route_id"] == "NEXT2619_0_primary" and row["selection_status"] == "selected" for row in rows_map["next"]
    )


def no_formalization_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*2619*"))


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
        check_row("VAL2619_00_sources_exist", sources_pass(rows_map), "all cited source paths exist and needles are present", "one or more cited source paths or needles missing"),
        check_row("VAL2619_01_lineage_complete", lineage_complete(rows_map), "lineage covers 2618 current gate plus historical 1769/1770 bridge work", "lineage is incomplete"),
        check_row("VAL2619_02_einstein_template", einstein_template_recorded(rows_map), "EH/Einstein reference theorem recorded as nonclaim", "Einstein template missing"),
        check_row("VAL2619_03_einstein_not_promoted", einstein_not_promoted(rows_map), "Einstein limit remains conditional/nonclaim", "Einstein limit was promoted"),
        check_row("VAL2619_04_deltaE_decomposition", deltae_decomposition_recorded(rows_map), "DeltaE_munu residual decomposition recorded", "DeltaE_munu decomposition missing"),
        check_row("VAL2619_05_newton_template", newton_template_recorded(rows_map), "Poisson/Newton conditional template recorded", "Poisson/Newton template missing"),
        check_row("VAL2619_06_residual_pack_nonclaim", residual_pack_nonclaim(rows_map), "operator residual rows remain nonclaim", "operator residual pack missing or promoted"),
        check_row("VAL2619_07_silence_audit_retained", silence_audit_retained(rows_map), "residual-sector silence audit retains blockers", "residual-sector silence verdict missing"),
        check_row("VAL2619_08_ppn_bridge_nonclaim", ppn_bridge_nonclaim(rows_map), "PPN bridge rows remain nonclaim", "PPN bridge rows missing or promoted"),
        check_row("VAL2619_09_empirical_map_nonclaim", empirical_map_nonclaim(rows_map), "empirical bound map remains nonclaim", "empirical bound map missing or promoted"),
        check_row("VAL2619_10_countermodel_retained", countermodel_retained(rows_map), "GR/Newton countermodel remains retained", "countermodel missing or promoted"),
        check_row("VAL2619_11_bridge_next", bridge_next(rows_map), "EH dominance/residual silence selected next", "bridge next status missing"),
        check_row("VAL2619_12_claim_gates_safe", claim_gates_safe(rows_map), "all claim gates remain blocked/nonclaim", "one or more claim gates opened"),
        check_row("VAL2619_13_no_claim_flags", generated_rows_have_no_claim_flags(rows_map), "claim/no-score flags stay false", "one or more claim/no-score flags enabled"),
        check_row("VAL2619_14_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready", "a MISSING_* row is marked ready"),
        check_row("VAL2619_15_formalization_untouched", no_formalization_artifacts(), "no 2619 outputs found under formalization-workbench", "2619 outputs found under formalization-workbench"),
        check_row("VAL2619_16_decision_next", decision_next(rows_map), "decision selects EH dominance/residual silence route", "decision route missing"),
        check_row("VAL2619_17_next_selected", next_selected(rows_map), "next target selected", "next target missing"),
        check_row("VAL2619_18_branch_copies", branch_copies_pass(rows_map), "branch/local/queue copies exist and parse", "branch copies missing or malformed"),
        check_row("VAL2619_19_csv_parse", csv_parse_all(), "all generated 2619 CSVs parse", "one or more generated 2619 CSVs fail to parse"),
        check_row("VAL2619_20_pycache_absent", pycache_absent(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
    ]
    overall = all(row["result"] == "PASS" for row in rows)
    rows.append(
        {
            "check_id": "VAL2619_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "2619 GR left-hand Einstein/Newton limit or operator residual pack",
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
        "# 2619 - GR Left-Hand Einstein Newton Limit Or Operator Residual Pack",
        "## Summary\n"
        "- 2619 connects the current 2618 source-normal-form branch to the exact GR/Newton bridge.\n"
        "- The honest object is `DeltaE_munu = E_LHS - (G_munu + Lambda g_munu)`: if this vanishes or is bounded, the route to GR/Newton opens; if it survives, MTS becomes a modified-operator theory with explicit local-test coefficients.\n"
        "- The Poisson/Newton lane is conditional only: EH dominance, clean Hilbert source, source normalization, and worldtube/Gauss closure are all required.\n"
        "- No GitHub, public, local-GR, Newton, PPN, WEP, clock, orbital, R10, or `q_loc=0` claim is made.",
        "## Source Register\n" + markdown_table(rows_map["sources"], ["source_id", "description", "source_path", "exists", "needles_present"]),
        "## Lineage Ledger\n" + markdown_table(rows_map["lineage"], ["lineage_id", "input_checkpoint", "what_it_gave", "current_use", "claim_status"]),
        "## Einstein Left-Hand Limit Attempt\n" + markdown_table(rows_map["einstein"], ["attempt_id", "claim_piece", "formal_statement", "status", "conditional_gain", "remaining_gap"]),
        "## Newton Poisson Weak-Field Attempt\n" + markdown_table(rows_map["newton"], ["attempt_id", "claim_piece", "formal_statement", "status", "conditional_gain", "remaining_gap"]),
        "## Residual Sector Silence Audit\n" + markdown_table(rows_map["silence"], ["sector_id", "sector", "representative_operator", "required_silence_condition", "current_status", "coefficient_row"]),
        "## Operator Residual Pack\n" + markdown_table(rows_map["operator"], ["row_id", "symbol", "meaning", "definition", "units", "status", "observable_links"]),
        "## PPN Bridge Ledger\n" + markdown_table(rows_map["ppn"], ["ppn_id", "parameter", "needed_parent_result", "formal_readout", "status"]),
        "## Empirical Bound Map\n" + markdown_table(rows_map["bounds"], ["bound_id", "arena", "residuals", "needed_map", "status"]),
        "## Countermodel Ledger\n" + markdown_table(rows_map["countermodel"], ["countermodel_id", "failure_mode", "mathematical_form", "retained", "why_survives", "what_kills_it"]),
        "## GR Newton Bridge Status\n" + markdown_table(rows_map["gr_bridge"], ["status_id", "bridge_piece", "current_status", "evidence", "remaining_gap"]),
        "## Claim Gates\n" + markdown_table(rows_map["claim_gates"], ["gate_id", "claim", "claim_allowed", "status", "blocker"]),
        "## Decision Ledger\n" + markdown_table(rows_map["decisions"], ["decision_id", "decision", "reason", "next_action"]),
        "## Next Target\n" + markdown_table(rows_map["next"], ["route_id", "selection_status", "target_doc", "target_script", "objective", "acceptance_gate", "claim_policy"]),
        "## Branch Copies\n" + markdown_table(rows_map["branch_copies"], ["copy_id", "source_key", "copy_path", "copy_exists", "csv_parse", "row_count"]),
        "## Validation\n" + markdown_table(validations, ["check_id", "result", "detail", "valid_for_claim"]),
        "## Verdict\n"
        "This is a useful tightening, not a victory lap. The current source-side work is clean enough to make the real missing theorem visible: MTS needs an EH-dominant local parent LHS, or it must admit explicit non-Einstein operator coefficients. If `DeltaE_munu` can be theorem-zeroed by local residual silence, then GR/Newton recovery becomes a serious route. If not, the same rows become the honest local-test residual model.",
    ]
    return "\n\n".join(sections) + "\n"


def main() -> None:
    ensure_dirs()
    rows_map = rows_by_key()
    write_csv(OUTPUTS["source_register"], rows_map["sources"])
    write_csv(OUTPUTS["lineage_ledger"], rows_map["lineage"])
    write_csv(OUTPUTS["einstein_limit"], rows_map["einstein"])
    write_csv(OUTPUTS["newton_limit"], rows_map["newton"])
    write_csv(OUTPUTS["residual_silence"], rows_map["silence"])
    write_csv(OUTPUTS["operator_residual"], rows_map["operator"])
    write_csv(OUTPUTS["ppn_bridge"], rows_map["ppn"])
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
    print(f"2619 validation {validations[-1]['result']}")
    print(f"doc={DOC_PATH}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
