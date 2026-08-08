from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
MICROSCOPE_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1840"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1840-Y5-R2FR-EH-dominance-and-residual-sector-silence-or-operator-coefficient-pack.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1840_0_1839_next",
        "source_key": "1839_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1839_NEXT_TARGET.csv",
        "needles": ["NEXT1839_0_primary", "1840-Y5-R2FR"],
        "role": "1839 selects EH dominance/residual-sector silence as the next GR bridge target.",
    },
    {
        "source_id": "SRC1840_1_1839_validation",
        "source_key": "1839_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1839_VALIDATION.csv",
        "needles": ["VAL1839_OVERALL", "PASS"],
        "role": "confirms 1839 passed as a nonclaim checkpoint.",
    },
    {
        "source_id": "SRC1840_2_1839_GR_bridge",
        "source_key": "1839_GR_bridge_handoff",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1839_GR_BRIDGE_HANDOFF.csv",
        "needles": ["GBH1839_1_left_hand_gate", "NOW_PRIMARY_PRESSURE_POINT"],
        "role": "source-side cleanup hands pressure to the Einstein/Newton left-hand operator.",
    },
    {
        "source_id": "SRC1840_3_1769_Einstein_limit",
        "source_key": "1769_Einstein_left_hand_limit",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1769_EINSTEIN_LEFT_HAND_LIMIT_ATTEMPT.csv",
        "needles": ["ELH1769_4_current_verdict", "CONDITIONAL_THEOREM_NOT_PARENT_PROOF"],
        "role": "1769 gives the conditional Einstein LHS theorem and its blocker.",
    },
    {
        "source_id": "SRC1840_4_1769_operator_residual_pack",
        "source_key": "1769_operator_residual_pack",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1769_OPERATOR_RESIDUAL_PACK.csv",
        "needles": ["ORP1769_0_E_LHS_GR_residual", "MISSING_EH_DOMINANCE_OR_COEFFICIENT_MAP"],
        "role": "1769 names the non-Einstein residual operator pack.",
    },
    {
        "source_id": "SRC1840_5_1770_EH_attempt",
        "source_key": "1770_EH_dominance_attempt",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1770_EH_DOMINANCE_THEOREM_ATTEMPT.csv",
        "needles": ["EHD1770_4_current_verdict", "FAIL_CURRENT_PARENT_PROOF"],
        "role": "1770 first attempted EH dominance and refused promotion.",
    },
    {
        "source_id": "SRC1840_6_1770_residual_silence",
        "source_key": "1770_residual_sector_silence",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1770_RESIDUAL_SECTOR_SILENCE_AUDIT.csv",
        "needles": ["RSS1770_6_verdict", "RESIDUAL_SECTORS_RETAINED_NONCLAIM"],
        "role": "1770 retained the residual sectors as nonclaim rows.",
    },
    {
        "source_id": "SRC1840_7_1770_operator_coefficients",
        "source_key": "1770_operator_coefficient_pack",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1770_OPERATOR_COEFFICIENT_PACK.csv",
        "needles": ["OPC1770_0_total_DeltaE", "MISSING_ZERO_THEOREM_OR_BOUNDED_COEFFICIENTS"],
        "role": "1770 provides the starting operator coefficient basis.",
    },
    {
        "source_id": "SRC1840_8_1770_empirical_map",
        "source_key": "1770_empirical_bound_map",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1770_EMPIRICAL_BOUND_MAP.csv",
        "needles": ["EBM1770_0_ppn_gamma_beta", "MISSING_PPN_RESIDUAL_MAP"],
        "role": "1770 maps residual operators to PPN/R10/clock/orbit/cosmology arenas.",
    },
    {
        "source_id": "SRC1840_9_1768_normal_form",
        "source_key": "1768_parent_action_normal_form",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1768_PARENT_ACTION_NORMAL_FORM_SIGNATURE.csv",
        "needles": ["ANF1768_6_current_verdict", "SIGNATURE_READY_PARENT_UNSIGNED"],
        "role": "parent action normal form is a signature, not yet a complete parent proof.",
    },
    {
        "source_id": "SRC1840_10_1009_parent_contract",
        "source_key": "1009_parent_current_chain",
        "source_path": ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
        "needles": ["PCS1009_9_total_parent_contract", "not_promoted"],
        "role": "total parent action remains contract-level until each sector has variation certificates.",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1840_SOURCE_REGISTER.csv",
    "eh_dominance": RESIDUALS / "P8_Y5_PARENT_QLOC_1840_EH_DOMINANCE_THEOREM_ATTEMPT.csv",
    "residual_silence": RESIDUALS / "P8_Y5_PARENT_QLOC_1840_RESIDUAL_SECTOR_SILENCE_AUDIT.csv",
    "operator_coefficients": RESIDUALS / "P8_Y5_PARENT_QLOC_1840_OPERATOR_COEFFICIENT_PACK.csv",
    "empirical_map": RESIDUALS / "P8_Y5_PARENT_QLOC_1840_EMPIRICAL_BOUND_MAP.csv",
    "countermodel": RESIDUALS / "P8_Y5_PARENT_QLOC_1840_COUNTERMODEL_LEDGER.csv",
    "gr_bridge": RESIDUALS / "P8_Y5_PARENT_QLOC_1840_GR_BRIDGE_STATUS.csv",
    "current_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1840_CURRENT_CORPUS_GATE.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1840_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1840_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1840_VALIDATION.csv",
}


def ensure_dirs() -> None:
    for directory in [RESIDUALS, MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
        directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        missing = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": path.exists(),
                "needles_present": not missing,
                "missing_needles": ";".join(missing),
                "role": source["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def eh_dominance_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "EHD1840_0_target",
            "claim_piece": "local Einstein-Hilbert dominance",
            "mathematical_form": "E_LHS = G_munu + Lambda g_munu + DeltaE_munu",
            "proof_route": "derive parent Euler-Lagrange operator, split EH piece from every retained MTS sector, and prove DeltaE_munu=0 or locally negligible",
            "current_result": "target sharpened but not parent-signed",
            "current_status": "TARGET_EXACT_NONCLAIM",
            "remaining_gap": "sector variation table and local scaling theorem are not complete",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "EHD1840_1_zero_theorem",
            "claim_piece": "residual-sector zero theorem",
            "mathematical_form": "for each retained i: delta S_i / delta e_obs | local = 0",
            "proof_route": "show the non-EH sector is topological, pure boundary, vertically silent, quotient-invisible, or not coupled to the observed coframe",
            "current_result": "available as theorem shape only",
            "current_status": "CONDITIONAL_ZERO_THEOREM_NOT_PROVED",
            "remaining_gap": "no sector-by-sector proof for higher-derivative, projector, boundary, nonminimal, memory/coframe, and source-normalization blocks",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "EHD1840_2_suppression_theorem",
            "claim_piece": "controlled nonzero residual suppression",
            "mathematical_form": "||DeltaE_i|| / ||G_munu|| <= epsilon_i(L_local,L_cg,coefficients)",
            "proof_route": "derive dimensions, coefficients and local scale hierarchy so every residual is below PPN/R10/clock/orbit tolerance",
            "current_result": "not available from current corpus",
            "current_status": "MISSING_SCALING_AND_COEFFICIENTS",
            "remaining_gap": "no signed coefficient normalization or tolerance conversion",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "EHD1840_3_Bianchi_noether",
            "claim_piece": "Bianchi/Noether compatibility",
            "mathematical_form": "nabla_mu(G^{mu nu}+Lambda g^{mu nu}+DeltaE^{mu nu})=0",
            "proof_route": "derive from one complete diffeomorphism-invariant parent action; do not drop terms after variation",
            "current_result": "conditional identity only",
            "current_status": "CONDITIONAL_PARENT_ACTION_IDENTITY",
            "remaining_gap": "1009 total parent action remains not_promoted and sector certificates are incomplete",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "EHD1840_4_Newton_limit",
            "claim_piece": "Newton/Poisson reduction after EH dominance",
            "mathematical_form": "G_00 -> 2 nabla^2 Phi/c^2 and nabla^2 Phi = 4 pi G rho",
            "proof_route": "EH dominance plus source normalization and weak-field slow-motion limit",
            "current_result": "blocked behind EH dominance and source normalization",
            "current_status": "CONDITIONAL_NOT_PROMOTED",
            "remaining_gap": "left-hand residuals and measured-G/source normalization remain open",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "EHD1840_5_current_verdict",
            "claim_piece": "current MTS local GR bridge",
            "mathematical_form": "DeltaE_munu=0 or bounded strongly enough for local GR/PPN",
            "proof_route": "zero theorem or coefficient-bound route",
            "current_result": "not proved; retain explicit residual coefficients",
            "current_status": "FAIL_CURRENT_PARENT_PROOF",
            "remaining_gap": "move to sector-action variation and local scaling, not public claim",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def residual_silence_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "sector_id": "RSS1840_0_higher_derivative",
            "sector": "higher-curvature / higher-derivative geometry",
            "operator_form": "c_R2 R^2 + c_Ricci2 R_munu R^munu + c_boxR R box R",
            "zero_or_suppression_route": "absent from parent normal form, topological in the local branch, or suppressed by a high scale",
            "current_status": "MISSING_OPERATOR_BASIS_AND_SCALE",
            "coefficient_row": "OPC1840_1_higher_derivative",
            "next_requirement": "vary the candidate sector and derive coefficient dimensions/signs",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "RSS1840_1_projector",
            "sector": "domain/projector/readout operator",
            "operator_form": "E_projector(Pi_M), [d,Pi_M]J_H, or local quotient residual",
            "zero_or_suppression_route": "Pi_M becomes identity or commutes in the local branch; otherwise it is a bounded residual",
            "current_status": "MISSING_PROJECTOR_VARIATION_AND_COMMUTATOR_ZERO",
            "coefficient_row": "OPC1840_2_projector",
            "next_requirement": "derive Pi_M local normal form and its variation",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "RSS1840_2_boundary",
            "sector": "boundary/reference/improvement terms",
            "operator_form": "DeltaE_boundary, Q_boundary, reference counterterm or improvement stress",
            "zero_or_suppression_route": "fixed-before-readout reference plus local/falloff boundary silence",
            "current_status": "MISSING_BOUNDARY_SILENCE_AND_FIXED_REFERENCE",
            "coefficient_row": "OPC1840_3_boundary",
            "next_requirement": "prove boundary variation vanishes locally or keep explicit coefficient",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "RSS1840_3_nonminimal",
            "sector": "nonminimal matter-geometry/MTS coupling",
            "operator_form": "f(X,Phi)L_m, A(X)J_m, curvature-matter coupling or hidden source-map channel",
            "zero_or_suppression_route": "forbidden by source-map normal form, or derived as real matter dynamics with a source-backed bound",
            "current_status": "MISSING_FORBID_OR_BOUND",
            "coefficient_row": "OPC1840_4_nonminimal",
            "next_requirement": "prove no representative-dependent matter coupling re-enters",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "RSS1840_4_memory_coframe",
            "sector": "memory/coframe/current-chain residual",
            "operator_form": "DeltaE_mem(theta,Q_tau,C_tau) or coframe-memory stress",
            "zero_or_suppression_route": "closed current chain, exact/boundary-only theta, or small local memory projection",
            "current_status": "MISSING_CURRENT_CHAIN_CERTIFICATES",
            "coefficient_row": "OPC1840_5_memory_coframe",
            "next_requirement": "complete 1009 sector certificates and local scaling",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "RSS1840_5_source_normalization",
            "sector": "measured-G/source normalization",
            "operator_form": "delta_G_source, M_H_ref, source-shadow or Hilbert-source normalization residual",
            "zero_or_suppression_route": "single Hilbert source plus measured-G normalization theorem",
            "current_status": "MISSING_SOURCE_NORMALIZATION_OWNER",
            "coefficient_row": "OPC1840_6_source_normalization",
            "next_requirement": "connect Hilbert source, measured G, and Poisson source without absorbing residuals",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "RSS1840_6_verdict",
            "sector": "all non-EH residual sectors",
            "operator_form": "DeltaE_munu=sum_i c_i O_i_munu",
            "zero_or_suppression_route": "all sectors zero/suppressed/bounded",
            "current_status": "RESIDUAL_SECTORS_RETAINED_NONCLAIM",
            "coefficient_row": "OPC1840_0_total_DeltaE",
            "next_requirement": "1841 must vary sectors and derive local scalings before any GR claim",
            "valid_for_claim": False,
        },
    ]


def operator_coefficient_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "OPC1840_0_total_DeltaE",
            "quantity": "DeltaE_munu",
            "definition": "total left-hand non-Einstein operator residual",
            "symbolic_form": "DeltaE_munu=sum_i c_i O_i_munu",
            "units": "curvature_operator_units",
            "source_status": "MISSING_ZERO_THEOREM_OR_BOUNDED_COEFFICIENTS",
            "test_arenas": "PPN;R10;clocks;orbits;cosmology",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OPC1840_1_higher_derivative",
            "quantity": "c_HD",
            "definition": "higher-curvature operator coefficient vector",
            "symbolic_form": "{c_R2,c_Ricci2,c_boxR,...}",
            "units": "length^2 or model-dependent inverse mass powers",
            "source_status": "MISSING_PARENT_VARIATION_AND_SCALE",
            "test_arenas": "PPN;short-range gravity;binary/orbital;cosmology",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OPC1840_2_projector",
            "quantity": "c_projector",
            "definition": "operator strength from quotient/domain/projector residual",
            "symbolic_form": "c_Pi O_Pi_munu",
            "units": "curvature_operator_units after projection",
            "source_status": "MISSING_PROJECTOR_LOCAL_VARIATION",
            "test_arenas": "PPN;WEP;R10;clock/frame tests",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OPC1840_3_boundary",
            "quantity": "c_boundary",
            "definition": "boundary/reference/improvement residual coefficient",
            "symbolic_form": "c_B O_B_munu",
            "units": "boundary-induced curvature_operator_units",
            "source_status": "MISSING_BOUNDARY_SILENCE_THEOREM",
            "test_arenas": "R10;orbital;clock;energy-conservation consistency",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OPC1840_4_nonminimal",
            "quantity": "c_nonminimal",
            "definition": "nonminimal matter-geometry coupling residual",
            "symbolic_form": "c_NM O_NM_munu(T_H,X,Phi)",
            "units": "coupling-dependent curvature_operator_units",
            "source_status": "MISSING_NO_HIDDEN_STRESS_OR_BOUND",
            "test_arenas": "WEP;PPN;clocks;particle/EM side constraints",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OPC1840_5_memory_coframe",
            "quantity": "c_memory",
            "definition": "memory/coframe/current-chain left-hand residual coefficient",
            "symbolic_form": "c_M O_M_munu(theta,Q_tau,C_tau)",
            "units": "current-chain induced curvature_operator_units",
            "source_status": "MISSING_CURRENT_CHAIN_LOCAL_SILENCE",
            "test_arenas": "clocks;cosmology growth;orbital drift;PPN preferred-frame",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OPC1840_6_source_normalization",
            "quantity": "delta_G_source",
            "definition": "source-normalization mismatch in the Poisson/Newton bridge",
            "symbolic_form": "nabla^2 Phi = 4 pi G(1+delta_G_source) rho + residuals",
            "units": "dimensionless after measured-G normalization",
            "source_status": "MISSING_MEASURED_G_OWNER",
            "test_arenas": "Newton limit;orbital systems;laboratory G;PPN",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def empirical_map_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "map_id": "EBM1840_0_ppn_gamma_beta",
            "arena": "PPN gamma and beta",
            "residual_input": "DeltaE_munu,c_HD,c_projector,c_memory,c_nonminimal",
            "required_output": "derive gamma=beta=1 or bound gamma-1,beta-1 from the operator pack",
            "current_status": "MISSING_PPN_RESIDUAL_MAP",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "map_id": "EBM1840_1_R10_Yukawa",
            "arena": "R10 short-range gravity",
            "residual_input": "operator coefficients projected to alpha(lambda)",
            "required_output": "alpha_predicted(lambda) with real source coefficients and real bound curve",
            "current_status": "MISSING_ALPHA_LAMBDA_PROJECTION",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "map_id": "EBM1840_2_clocks",
            "arena": "clock/redshift/preferred-frame tests",
            "residual_input": "c_memory,c_projector,c_nonminimal",
            "required_output": "clock residual vector with units, signs and source paths",
            "current_status": "MISSING_CLOCK_RESIDUAL_VECTOR",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "map_id": "EBM1840_3_orbits",
            "arena": "orbital systems and perihelion/binary constraints",
            "residual_input": "c_HD,c_boundary,delta_G_source",
            "required_output": "orbital residual coefficients after measured-G normalization",
            "current_status": "MISSING_ORBITAL_RESIDUAL_MAP",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "map_id": "EBM1840_4_cosmology",
            "arena": "FLRW/cosmology bridge",
            "residual_input": "large-scale memory/coupling terms",
            "required_output": "keep cosmology separate from the local GR proof until local scaling is derived",
            "current_status": "HELD_SEPARATE_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1840_0_small_residual_tail",
            "obstruction": "DeltaE_munu is tiny but nonzero and produces a PPN/R10 tail",
            "why_survives": "no local scaling bound or exact zero theorem has been derived",
            "effect": "cannot claim exact GR; must score residual coefficient",
            "disposition": "RETAINED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1840_1_cancellation",
            "obstruction": "two non-EH sectors cancel in one arena but not all arenas",
            "why_survives": "cancellations are not parent-signed symmetries",
            "effect": "cannot use one successful arena to infer universal silence",
            "disposition": "RETAINED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1840_2_boundary_fit",
            "obstruction": "boundary/reference choice hides residuals in measured G",
            "why_survives": "fixed-before-readout and boundary silence are unsigned",
            "effect": "Newton/Poisson bridge remains conditional",
            "disposition": "RETAINED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1840_3_source_normalization",
            "obstruction": "source normalization absorbs non-EH terms instead of deriving them away",
            "why_survives": "source-normalization owner remains missing",
            "effect": "measured-G route cannot promote local GR",
            "disposition": "RETAINED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1840_4_verdict",
            "obstruction": "EH dominance is asserted by notation rather than derived from parent action",
            "why_survives": "current corpus still needs sector variations and local scaling",
            "effect": "1840 must hand off to 1841 derivation/bound route",
            "disposition": "RETAINED_AS_RED_TEAM_GUARD",
            "valid_for_claim": False,
        },
    ]


def gr_bridge_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "status_id": "BGS1840_0_source_side",
            "object": "Hilbert/source side",
            "current_status": "NARROWED_NOT_CLAIMED",
            "evidence": "1839 source-shadow classification and WEP sidecar",
            "next_requirement": "do not reopen WEP scoring until left-hand operator and source normalization are stable",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "BGS1840_1_EH_left_hand",
            "object": "Einstein-Hilbert local LHS",
            "current_status": "PRIMARY_BLOCKER",
            "evidence": "EHD1840_5_current_verdict",
            "next_requirement": "prove residual-sector zero/suppression or keep explicit coefficient rows",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "BGS1840_2_Newton_Poisson",
            "object": "Newton/Poisson limit",
            "current_status": "CONDITIONAL_BEHIND_EH_AND_SOURCE_NORMALIZATION",
            "evidence": "EHD1840_4_Newton_limit;OPC1840_6_source_normalization",
            "next_requirement": "derive weak-field EH limit and measured-G/source owner",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "BGS1840_3_empirical_route",
            "object": "PPN/R10/clock/orbit empirical branch",
            "current_status": "COEFFICIENT_PACK_STAGED_NONCLAIM",
            "evidence": "OPC1840 rows; EBM1840 rows",
            "next_requirement": "convert residual operators into source-backed arena coefficients",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "BGS1840_4_next",
            "object": "best next derivation",
            "current_status": "SECTOR_ACTION_VARIATION_AND_LOCAL_SCALING_SILENCE_IS_NEXT",
            "evidence": "RSS1840 residual-sector audit",
            "next_requirement": "1841 should vary each non-EH action block and derive scaling/bounds",
            "valid_for_claim": False,
        },
    ]


def current_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1840_0_EH_dominance",
            "claim": "parent LHS is EH-dominated in the local branch",
            "gate_pass": False,
            "reason": "sector zero/suppression theorem is not parent-signed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1840_1_residual_silence",
            "claim": "all non-EH residual sectors vanish locally",
            "gate_pass": False,
            "reason": "higher-derivative, projector, boundary, nonminimal, memory and source-normalization routes remain open",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1840_2_PPN",
            "claim": "MTS passes local PPN as GR",
            "gate_pass": False,
            "reason": "PPN residual vector is not derived from operator coefficients",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1840_3_Newton",
            "claim": "MTS derives Newton/Poisson limit like GR derives Newton",
            "gate_pass": False,
            "reason": "EH dominance and source normalization remain conditional",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1840_4_local_GR_promotion",
            "claim": "local GR/Newton branch is promoted",
            "gate_pass": False,
            "reason": "1840 is a residual operator checkpoint, not a pass claim",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1840_0_EH_result",
            "decision": "EH_DOMINANCE_NOT_PARENT_PROVED",
            "reason": "the theorem shape is exact but each non-EH sector still needs a variation/silence/scaling certificate",
            "next_action": "retain DeltaE_munu operator pack",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1840_1_operator_pack",
            "decision": "OPERATOR_COEFFICIENT_PACK_STAGED_NONCLAIM",
            "reason": "residual sectors are now explicit enough to become PPN/R10/clock/orbit rows once coefficients are sourced",
            "next_action": "derive sector variations before numeric scoring",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1840_2_countermodels",
            "decision": "COUNTERMODELS_RETAINED",
            "reason": "small residuals, cancellations, boundary choices and source normalization can fake a GR pass if not controlled",
            "next_action": "use red-team guards in 1841",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1840_3_best_next",
            "decision": "SECTOR_ACTION_VARIATION_AND_LOCAL_SCALING_SILENCE_IS_NEXT",
            "reason": "the least-handwavy route is to vary every retained non-EH action block and either silence it or derive its local scaling",
            "next_action": "1841-Y5-R2FR-sector-action-variation-and-local-scaling-silence-or-operator-bounds.md",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1840_0_primary",
            "next_target": "1841-Y5-R2FR-sector-action-variation-and-local-scaling-silence-or-operator-bounds.md",
            "script": "scripts/Y5_R2FR_sector_action_variation_and_local_scaling_silence_or_operator_bounds_1841.py",
            "objective": "vary each retained non-EH sector and derive local zero/suppression conditions; otherwise convert it into a source-backed operator-bound row",
            "selection_status": "selected",
            "success_condition": "every residual sector is parent-silent, scale-suppressed, or carried forward as a valid nonclaim coefficient with units and arena projection",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1840_1_sidecar",
            "next_target": "1841b-Y5-R2FR-Poisson-Gauss-worldtube-source-normalization-pack.md",
            "script": "scripts/Y5_R2FR_Poisson_Gauss_worldtube_source_normalization_pack_1841b.py",
            "objective": "derive the measured-G/source-normalization owner needed after EH dominance",
            "selection_status": "held_sidecar",
            "success_condition": "Poisson source is derived from one Hilbert/worldtube normalization without residual absorption",
        },
    ]


def build_rows_map() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "eh_dominance": eh_dominance_rows(),
        "residual_silence": residual_silence_rows(),
        "operator_coefficients": operator_coefficient_rows(),
        "empirical_map": empirical_map_rows(),
        "countermodel": countermodel_rows(),
        "gr_bridge": gr_bridge_rows(),
        "current_gate": current_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }


def fieldnames(rows: list[dict[str, Any]]) -> list[str]:
    names: list[str] = []
    for row in rows:
        for key in row:
            if key not in names:
                names.append(key)
    return names


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames(rows))
        writer.writeheader()
        writer.writerows(rows)


def copy_outputs() -> list[Path]:
    copied: list[Path] = []
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        targets = [
            MICROSCOPE_RESIDUALS / path.name,
            QUARANTINE / path.name,
            RAB_QUEUE / f"JR1840_{key.upper()}.csv",
        ]
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
            copied.append(target)
    return copied


def parse_csv_ok(path: Path) -> bool:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def csv_parse_all() -> bool:
    return all(parse_csv_ok(path) for key, path in OUTPUTS.items() if key != "validation")


def no_formalization_outputs() -> bool:
    if not FORMALIZATION.exists():
        return True
    output_markers = [
        "1840-Y5-R2FR",
        "P8_Y5_PARENT_QLOC_1840",
        "P8_Y5_BRR545_1840",
        "Y5_R2FR_EH_dominance_and_residual_sector_silence_or_operator_coefficient_pack_1840",
    ]
    return not any(any(marker in path.name for marker in output_markers) for path in FORMALIZATION.rglob("*"))


def branch_copies_exist() -> bool:
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        expected = [
            MICROSCOPE_RESIDUALS / path.name,
            QUARANTINE / path.name,
            RAB_QUEUE / f"JR1840_{key.upper()}.csv",
        ]
        if not all(target.exists() for target in expected):
            return False
    return True


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    ignored_true_fields = {"exists", "needles_present"}
    for key, rows in rows_map.items():
        if key == "source_register":
            continue
        for row in rows:
            for field, value in row.items():
                if field in ignored_true_fields:
                    continue
                if field in {"valid_for_claim", "claim_allowed", "score_ready", "gate_pass"} and value is True:
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for key, rows in rows_map.items():
        if key == "source_register":
            continue
        for row in rows:
            has_missing = any("MISSING_" in str(value) for value in row.values())
            if not has_missing:
                continue
            for field in ["valid_for_claim", "claim_allowed", "score_ready", "gate_pass"]:
                if row.get(field) is True:
                    return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = rows_map["source_register"]
    checks = [
        ("VAL1840_0_sources_exist", all(row["exists"] is True for row in source_rows), "all cited source paths exist"),
        ("VAL1840_1_needles_present", all(row["needles_present"] is True for row in source_rows), "all cited source needles are present"),
        (
            "VAL1840_2_EH_attempt_recorded",
            any(row["attempt_id"] == "EHD1840_0_target" for row in rows_map["eh_dominance"]),
            "EH dominance target recorded",
        ),
        (
            "VAL1840_3_EH_not_promoted",
            any(row["attempt_id"] == "EHD1840_5_current_verdict" and row["current_status"] == "FAIL_CURRENT_PARENT_PROOF" for row in rows_map["eh_dominance"]),
            "EH dominance remains unproved/nonclaim",
        ),
        (
            "VAL1840_4_residuals_retained",
            any(row["sector_id"] == "RSS1840_6_verdict" and row["current_status"] == "RESIDUAL_SECTORS_RETAINED_NONCLAIM" for row in rows_map["residual_silence"]),
            "residual sectors retained as nonclaim",
        ),
        (
            "VAL1840_5_coefficient_pack_nonclaim",
            {"OPC1840_0_total_DeltaE", "OPC1840_1_higher_derivative", "OPC1840_2_projector", "OPC1840_3_boundary", "OPC1840_4_nonminimal", "OPC1840_5_memory_coframe", "OPC1840_6_source_normalization"}.issubset({row["row_id"] for row in rows_map["operator_coefficients"]})
            and all(row["valid_for_claim"] is False and row["score_ready"] is False for row in rows_map["operator_coefficients"]),
            "operator coefficient rows remain explicit and nonclaim",
        ),
        (
            "VAL1840_6_empirical_map_nonclaim",
            {"EBM1840_0_ppn_gamma_beta", "EBM1840_1_R10_Yukawa", "EBM1840_2_clocks", "EBM1840_3_orbits", "EBM1840_4_cosmology"}.issubset({row["map_id"] for row in rows_map["empirical_map"]})
            and all(row["claim_allowed"] is False and row["valid_for_claim"] is False for row in rows_map["empirical_map"]),
            "PPN/R10/clock/orbit/cosmology map remains nonclaim",
        ),
        (
            "VAL1840_7_countermodels_retained",
            any(row["countermodel_id"] == "CM1840_4_verdict" and row["disposition"] == "RETAINED_AS_RED_TEAM_GUARD" for row in rows_map["countermodel"]),
            "EH-dominance countermodel guard retained",
        ),
        (
            "VAL1840_8_GR_bridge_next",
            any(row["status_id"] == "BGS1840_4_next" and row["current_status"] == "SECTOR_ACTION_VARIATION_AND_LOCAL_SCALING_SILENCE_IS_NEXT" for row in rows_map["gr_bridge"]),
            "sector variation/local scaling selected next",
        ),
        (
            "VAL1840_9_current_gates_block",
            all(row["gate_pass"] is False and row["claim_allowed"] is False for row in rows_map["current_gate"]),
            "all current corpus gates remain blocked",
        ),
        ("VAL1840_10_no_claim_flags", no_claim_flags(rows_map), "no generated claim flags are true"),
        ("VAL1840_11_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1840_12_decision_next",
            any(row["decision_id"] == "DEC1840_3_best_next" and row["decision"] == "SECTOR_ACTION_VARIATION_AND_LOCAL_SCALING_SILENCE_IS_NEXT" for row in rows_map["decision"]),
            "best-next decision selects sector variation/local scaling",
        ),
        (
            "VAL1840_13_next_selected",
            any(row["route_id"] == "NEXT1840_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1840_14_csv_parse", csv_parse_all(), "all generated 1840 CSVs parse"),
        ("VAL1840_15_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1840_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1840_17_formalization_untouched", no_formalization_outputs(), "no 1840 outputs found under formalization-workbench"),
    ]
    rows = [{"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail} for check_id, passed, detail in checks]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1840_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1840 EH dominance and residual-sector silence or operator coefficient pack",
        }
    )
    return rows


def markdown_cell(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(markdown_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    return "\n".join(
        [
            "# 1840 Y5 R2FR EH dominance and residual-sector silence or operator coefficient pack",
            "",
            "**Progress:** 1840 attacks the actual GR-left-hand problem. The source side is cleaner after 1839, so the question is now whether the parent LHS genuinely reduces to Einstein-Hilbert locally, or whether non-EH MTS sectors must survive as explicit residual coefficients.",
            "",
            "**Current verdict:** EH dominance is not parent-proved. The theorem shape is clean, but every retained non-EH sector still needs a variation certificate and either a zero theorem, a local suppression law, or a source-backed empirical coefficient row.",
            "",
            "**Claim ceiling:** no local GR, Newton, PPN, R10, WEP, clock, orbital or cosmology pass is allowed from 1840. This checkpoint is a private bridge discipline step, not a public claim.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "missing_needles", "role"]),
            "",
            "## EH Dominance Theorem Attempt",
            markdown_table(rows_map["eh_dominance"], ["attempt_id", "claim_piece", "mathematical_form", "current_status", "remaining_gap", "claim_allowed", "valid_for_claim"]),
            "",
            "## Residual-Sector Silence Audit",
            markdown_table(rows_map["residual_silence"], ["sector_id", "sector", "operator_form", "current_status", "coefficient_row", "next_requirement", "valid_for_claim"]),
            "",
            "## Operator Coefficient Pack",
            markdown_table(rows_map["operator_coefficients"], ["row_id", "quantity", "definition", "symbolic_form", "source_status", "test_arenas", "score_ready", "valid_for_claim"]),
            "",
            "## Empirical Bound Map",
            markdown_table(rows_map["empirical_map"], ["map_id", "arena", "residual_input", "required_output", "current_status", "claim_allowed", "valid_for_claim"]),
            "",
            "## Countermodel Ledger",
            markdown_table(rows_map["countermodel"], ["countermodel_id", "obstruction", "why_survives", "effect", "disposition", "valid_for_claim"]),
            "",
            "## GR Bridge Status",
            markdown_table(rows_map["gr_bridge"], ["status_id", "object", "current_status", "evidence", "next_requirement", "valid_for_claim"]),
            "",
            "## Current Corpus Gate",
            markdown_table(rows_map["current_gate"], ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "",
            "## Decision Ledger",
            markdown_table(rows_map["decision"], ["decision_id", "decision", "reason", "next_action"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This is not grim; it is the exact fork we wanted to expose. To reduce to GR the way GR reduces to Newton, MTS must not merely contain an Einstein-looking term. It must show why the other local left-hand sectors vanish, scale away, or become small bounded coefficients. That is now a finite target list rather than fog.",
            "",
        ]
    )


def main() -> None:
    ensure_dirs()
    rows_map = build_rows_map()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1840 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
