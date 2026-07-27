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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1770"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1770_0_1769_handoff",
        "source_key": "1769_eh_dominance_next",
        "source_path": ROOT / "1769-Y5-R2FR-GR-left-hand-Einstein-Newton-limit-or-operator-residual-pack.md",
        "needles": ["EH_DOMINANCE_RESIDUAL_SILENCE_AND_OPERATOR_COEFFICIENTS_IS_NEXT", "NEXT1769_0_primary"],
    },
    {
        "source_id": "SRC1770_1_1769_validation",
        "source_key": "1769_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1769_VALIDATION.csv",
        "needles": ["VAL1769_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC1770_2_1769_residual_pack",
        "source_key": "1769_operator_residual_pack",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1769_OPERATOR_RESIDUAL_PACK.csv",
        "needles": ["ORP1769_0_E_LHS_GR_residual", "ORP1769_5_source_normalization"],
    },
    {
        "source_id": "SRC1770_3_1769_ppn",
        "source_key": "1769_ppn_bridge",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1769_PPN_BRIDGE_LEDGER.csv",
        "needles": ["PPN1769_0_gamma", "PPN1769_4_verdict"],
    },
    {
        "source_id": "SRC1770_4_1768_normal_form",
        "source_key": "1768_normal_form",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1768_PARENT_ACTION_NORMAL_FORM_SIGNATURE.csv",
        "needles": ["ANF1768_0_parent_action_partition", "ANF1768_6_current_verdict"],
    },
    {
        "source_id": "SRC1770_5_1009_current_chain",
        "source_key": "1009_parent_current_chain",
        "source_path": ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
        "needles": ["PCS1009_0_EH_core", "PCS1009_9_total_parent_contract"],
    },
    {
        "source_id": "SRC1770_6_1009_sector_refusal",
        "source_key": "1009_sector_refusal",
        "source_path": ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
        "needles": ["REFUSED_INCOMPLETE_PARENT_CURRENT_CHAIN_CONTRACT", "TOTAL_PARENT_ACTION_SWITCH_REJECTED_WITHOUT_SECTOR_CERTIFICATES"],
    },
    {
        "source_id": "SRC1770_7_1012_newton_blocker",
        "source_key": "1012_newton_poisson_blocker",
        "source_path": ROOT / "1012-Y5-R10-Y5-source-normalization-owner-or-q_loc-bound-implementation.md",
        "needles": ["Y5O1012_7_Newton_Poisson_orbit", "conditional_not_parent_derived"],
    },
    {
        "source_id": "SRC1770_8_1012_nonEH",
        "source_key": "1012_nonEH_operator",
        "source_path": ROOT / "1012-Y5-R10-Y5-source-normalization-owner-or-q_loc-bound-implementation.md",
        "needles": ["Y5C1012_4_nonEH_operator_potential", "MISSING_EH_ONLY_THEOREM_OR_NONEH_OPERATOR_COEFFICIENT_MAP"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1770_SOURCE_REGISTER.csv",
    "eh_dominance": RESIDUALS / "P8_Y5_PARENT_QLOC_1770_EH_DOMINANCE_THEOREM_ATTEMPT.csv",
    "residual_silence": RESIDUALS / "P8_Y5_PARENT_QLOC_1770_RESIDUAL_SECTOR_SILENCE_AUDIT.csv",
    "operator_coefficients": RESIDUALS / "P8_Y5_PARENT_QLOC_1770_OPERATOR_COEFFICIENT_PACK.csv",
    "empirical_map": RESIDUALS / "P8_Y5_PARENT_QLOC_1770_EMPIRICAL_BOUND_MAP.csv",
    "countermodel": RESIDUALS / "P8_Y5_PARENT_QLOC_1770_COUNTERMODEL_LEDGER.csv",
    "bridge_status": RESIDUALS / "P8_Y5_PARENT_QLOC_1770_GR_BRIDGE_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1770_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1770_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1770_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1770_VALIDATION.csv",
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
                "role": "EH dominance and residual-sector silence or operator coefficient pack",
                "valid_for_claim": False,
            }
        )
    return rows


def eh_dominance_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "EHD1770_0_target",
            "claim_piece": "EH dominance in the local branch",
            "mathematical_form": "E_LHS = G_munu + Lambda g_munu + sum_i epsilon_i E_i, with epsilon_i E_i -> 0 or bounded",
            "status": "TARGET_EXACT",
            "derivation_result": "local GR recovery requires every non-EH sector to be silent, suppressed, reclassified, or bounded",
            "remaining_gap": "sector variations and local scaling are not parent-signed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "EHD1770_1_zero_theorem_shape",
            "claim_piece": "residual-sector zero theorem",
            "mathematical_form": "for all retained i: delta S_i/delta e_obs | local branch = 0",
            "status": "CONDITIONAL_ZERO_THEOREM",
            "derivation_result": "would prove EH dominance if each sector has an action owner and a local silence theorem",
            "remaining_gap": "no sector-by-sector parent action variation certificate",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "EHD1770_2_suppression_theorem_shape",
            "claim_piece": "residual-sector suppression theorem",
            "mathematical_form": "||epsilon_i E_i|| / ||G_munu|| <= bound_i << local tolerance",
            "status": "CONDITIONAL_SUPPRESSION_THEOREM",
            "derivation_result": "would permit a controlled GR limit without exact zero",
            "remaining_gap": "needs units, local scale hierarchy, coefficient values, and empirical tolerance",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "EHD1770_3_bianchi_compatibility",
            "claim_piece": "residual silence respects Noether/Bianchi identity",
            "mathematical_form": "nabla_mu(G^{mu nu}+Lambda g^{mu nu}+DeltaE^{mu nu})=0",
            "status": "CONDITIONAL_PARENT_ACTION_IDENTITY",
            "derivation_result": "automatic only if the complete parent action variation is owned and no terms are dropped illegally",
            "remaining_gap": "1009 current-chain sector certificates remain incomplete",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "EHD1770_4_current_verdict",
            "claim_piece": "current MTS EH dominance",
            "mathematical_form": "DeltaE_munu=0 or negligible in local branch",
            "status": "FAIL_CURRENT_PARENT_PROOF",
            "derivation_result": "the route is mathematically sharp, but current corpus lacks residual-sector zero/suppression certificates",
            "remaining_gap": "operator coefficient pack retained; no local-GR/Newton claim",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def residual_silence_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "sector_id": "RSS1770_0_higher_derivative",
            "sector": "higher-curvature / higher-derivative LHS operators",
            "mathematical_form": "c_R2 R^2 + c_Ricci2 R_munu R^munu + c_boxR R box R",
            "silence_route": "operator absent by parent normal form, or coefficients suppressed by high scale",
            "status": "MISSING_OPERATOR_BASIS_AND_SCALE",
            "coefficient_row": "OPC1770_1_higher_derivative",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "RSS1770_1_projector",
            "sector": "domain/projector/mass-readout operator",
            "mathematical_form": "E_projector or [d,Pi_M]J_H obstruction",
            "silence_route": "projector is identity/commutes in local branch, or obstruction is bounded",
            "status": "MISSING_PARENT_PROJECTOR_VARIATION_AND_COMMUTATOR_ZERO",
            "coefficient_row": "OPC1770_2_projector",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "RSS1770_2_boundary",
            "sector": "boundary/reference/improvement",
            "mathematical_form": "DeltaE_boundary, Q_boundary, counterterm/improvement residual",
            "silence_route": "fixed-before-readout boundary reference and local/falloff boundary silence",
            "status": "MISSING_BOUNDARY_SILENCE_AND_FIXED_REFERENCE",
            "coefficient_row": "OPC1770_3_boundary",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "RSS1770_3_nonminimal",
            "sector": "nonminimal matter-geometry/MTS coupling",
            "mathematical_form": "f(X,Phi) L_m or A(X)J_m",
            "silence_route": "forbidden by normal form or converted to explicit matter dynamics with bounded coefficient",
            "status": "MISSING_FORBID_OR_BOUND",
            "coefficient_row": "OPC1770_4_nonminimal",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "RSS1770_4_memory_coframe",
            "sector": "memory/coframe/preferred-frame residual",
            "mathematical_form": "E_memory, E_coframe, local-frame-lock residual",
            "silence_route": "local vacuum/coframe lock theorem or PPN preferred-frame bounds",
            "status": "MISSING_LOCAL_FRAME_LOCK_OR_BOUND",
            "coefficient_row": "OPC1770_5_memory_coframe",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "RSS1770_5_source_normalization",
            "sector": "source normalization / worldtube / measured-GM glue",
            "mathematical_form": "G_ref M_H_ref = surface/exterior charge before orbital fitting",
            "silence_route": "Poisson/Gauss/worldtube closure with no orbital-GM laundering",
            "status": "MISSING_POISSON_GAUSS_WORLDTUBE_GLUE",
            "coefficient_row": "OPC1770_6_source_normalization",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "sector_id": "RSS1770_6_verdict",
            "sector": "residual-sector silence for current MTS",
            "mathematical_form": "all DeltaE_i zero/suppressed/bounded",
            "silence_route": "not achieved in current corpus",
            "status": "RESIDUAL_SECTORS_RETAINED_NONCLAIM",
            "coefficient_row": "operator coefficient pack required",
            "valid_for_claim": False,
        },
    ]


def operator_coefficient_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "OPC1770_0_total_DeltaE",
            "quantity": "DeltaE_munu",
            "definition": "total left-hand non-Einstein operator residual",
            "mathematical_form": "DeltaE_munu=sum_i c_i O_i_munu",
            "units": "curvature_operator_units",
            "status": "MISSING_ZERO_THEOREM_OR_BOUNDED_COEFFICIENTS",
            "test_links": "PPN,R10,orbital,clocks,cosmology",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OPC1770_1_higher_derivative",
            "quantity": "c_R2,c_Ricci2,c_boxR",
            "definition": "higher-curvature/higher-derivative LHS coefficients",
            "mathematical_form": "O_i in {R^2,R_munuR^munu,R box R,...}",
            "units": "length_power_by_operator",
            "status": "MISSING_OPERATOR_BASIS_UNITS_BOUNDS",
            "test_links": "R10 alpha(lambda),PPN,waves,cosmology",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OPC1770_2_projector",
            "quantity": "c_projector",
            "definition": "domain/projector/local readout operator residual",
            "mathematical_form": "E_projector or [d,Pi_M]J_H",
            "units": "operator_dependent",
            "status": "MISSING_PROJECTOR_ACTION_VARIATION_OR_BOUND",
            "test_links": "measured GM,R10,WEP,orbits",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OPC1770_3_boundary",
            "quantity": "c_boundary",
            "definition": "boundary/reference/improvement residual coefficient",
            "mathematical_form": "DeltaE_boundary or Q_boundary residual",
            "units": "boundary_operator_dependent",
            "status": "MISSING_BOUNDARY_SILENCE_OR_BOUND",
            "test_links": "mass charge,orbits,clock potentials",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OPC1770_4_nonminimal",
            "quantity": "c_nonminimal",
            "definition": "direct matter-geometry/MTS coupling coefficient",
            "mathematical_form": "f(X,Phi)L_m or A(X)J_m",
            "units": "operator_dependent",
            "status": "MISSING_FORBID_THEOREM_OR_BOUND",
            "test_links": "WEP,clocks,PPN,R10",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OPC1770_5_memory_coframe",
            "quantity": "c_memory,c_frame",
            "definition": "memory/coframe/preferred-frame local residual coefficients",
            "mathematical_form": "E_memory + E_coframe",
            "units": "operator_dependent",
            "status": "MISSING_LOCAL_FRAME_LOCK_OR_PPN_BOUND",
            "test_links": "PPN alpha_i,clocks,orbits",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OPC1770_6_source_normalization",
            "quantity": "delta_G_source,delta_MHref",
            "definition": "Poisson/Gauss/worldtube source-normalization residual",
            "mathematical_form": "mu_obs - G_ref M_H_ref",
            "units": "GM_or_fractional",
            "status": "MISSING_WORLDTUBE_EXTERIOR_CLOSURE",
            "test_links": "Cavendish,ephemerides,binary dynamics",
            "valid_for_claim": False,
        },
    ]


def empirical_map_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "map_id": "EBM1770_0_ppn_gamma_beta",
            "observable": "PPN gamma-1 and beta-1",
            "sensitive_coefficients": "c_R2,c_projector,c_memory,c_frame,DeltaE_munu",
            "claim_condition": "derive gamma=beta=1 or bound residual coefficients",
            "status": "MISSING_PPN_RESIDUAL_MAP",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "map_id": "EBM1770_1_R10_yukawa",
            "observable": "short-range alpha(lambda)",
            "sensitive_coefficients": "c_R2,c_Ricci2,c_projector,c_nonminimal",
            "claim_condition": "operator-to-Yukawa map and source-backed bound curve",
            "status": "MISSING_R10_OPERATOR_MAP",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "map_id": "EBM1770_2_clocks",
            "observable": "clock redshift/local time residuals",
            "sensitive_coefficients": "c_nonminimal,c_memory,c_frame,delta_G_source",
            "claim_condition": "clock observable projection and bound",
            "status": "MISSING_CLOCK_PROJECTION",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "map_id": "EBM1770_3_orbits",
            "observable": "perihelion/precession/ephemeris residual",
            "sensitive_coefficients": "DeltaE_munu,delta_G_source,c_boundary,c_projector",
            "claim_condition": "Poisson/Gauss/worldtube closure then orbital readout",
            "status": "MISSING_ORBITAL_READOUT_WITHOUT_GM_BACKFILL",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "map_id": "EBM1770_4_cosmology",
            "observable": "growth/lensing/background expansion residual",
            "sensitive_coefficients": "c_R2,c_memory,c_frame,DeltaE_munu",
            "claim_condition": "separate cosmology branch; not a local-GR substitute",
            "status": "HELD_FOR_COSMOLOGY_BRANCH",
            "valid_for_claim": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1770_0_small_but_not_zero_tail",
            "countermodel": "a non-EH operator survives but is small enough to pass current tests",
            "mathematical_form": "DeltaE_munu = epsilon O_munu with epsilon != 0",
            "survives_current_constraints": True,
            "why_survives": "no zero theorem or bound map has been supplied",
            "what_kills_it": "derive epsilon=0 or source-backed bound below all relevant arenas",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1770_1_operator_cancellation",
            "countermodel": "residual sectors cancel in one observable but not generically",
            "mathematical_form": "sum_i c_i O_i -> 0 for one test but not all",
            "survives_current_constraints": True,
            "why_survives": "no no-cancellation/independent coefficient guard exists",
            "what_kills_it": "absolute-sum/no-cancellation guard or sector zero theorem",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1770_2_boundary_counterterm_fit",
            "countermodel": "boundary/reference term is tuned after readout",
            "mathematical_form": "Q_boundary or B_ref chosen to absorb observed residual",
            "survives_current_constraints": True,
            "why_survives": "fixed-before-readout boundary/reference certificate is missing",
            "what_kills_it": "fixed reference and improvement ambiguity certificate",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1770_3_source_normalization_gap",
            "countermodel": "LHS is EH-like but measured GM is still not the parent source charge",
            "mathematical_form": "Poisson source charge != orbital GM denominator",
            "survives_current_constraints": True,
            "why_survives": "worldtube/Pi_M/Gauss bridge remains blocked",
            "what_kills_it": "derive parent source charge -> Gauss flux -> exterior potential before fitting",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1770_4_verdict",
            "countermodel": "EH dominance remains unproved",
            "mathematical_form": "DeltaE_munu residual sectors retained",
            "survives_current_constraints": True,
            "why_survives": "1770 stages the silence theorem but cannot sign sector variations/scalings",
            "what_kills_it": "1771 sector-by-sector action variation and local scaling silence, or bounds",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def bridge_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "status_id": "BGS1770_0_eh_dominance",
            "bridge_piece": "EH dominance",
            "current_status": "NOT_PARENT_PROVED",
            "evidence": "EHD1770_4",
            "remaining_gap": "sector variation and silence/suppression certificates",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "BGS1770_1_operator_coefficients",
            "bridge_piece": "operator coefficient pack",
            "current_status": "STAGED_NONCLAIM",
            "evidence": "OPC1770 rows",
            "remaining_gap": "source-backed operator basis, units, maps, and bounds",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "BGS1770_2_newton",
            "bridge_piece": "Newton/Poisson",
            "current_status": "STILL_BLOCKED",
            "evidence": "RSS1770_5 and OPC1770_6",
            "remaining_gap": "source normalization/worldtube/exterior closure",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "BGS1770_3_local_GR",
            "bridge_piece": "local GR/PPN",
            "current_status": "NOT_CLAIMABLE",
            "evidence": "claim gates blocked",
            "remaining_gap": "gamma/beta/preferred-frame/Yukawa maps and bounds",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "BGS1770_4_next",
            "bridge_piece": "next derivation owner",
            "current_status": "SECTOR_VARIATION_AND_LOCAL_SCALING_SILENCE_IS_NEXT",
            "evidence": "residual silence audit identifies missing sector certificates",
            "remaining_gap": "build 1771 sector-action variation/local scaling silence or bounds",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1770_0_derivation_attempt",
            "decision": "EH_DOMINANCE_REQUIRES_SECTOR_SILENCE_CERTIFICATES",
            "reason": "declaring EH dominance is not enough; every non-EH sector must be zeroed, suppressed, reclassified, or bounded",
            "next_action": "derive sector-by-sector action variation and local scaling silence",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1770_1_no_promotion",
            "decision": "LOCAL_GR_NEWTON_NOT_CLAIMED",
            "reason": "residual sectors and source normalization remain open",
            "next_action": "keep all local/PPN/Newton/R10 gates blocked",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1770_2_coefficient_pack",
            "decision": "OPERATOR_COEFFICIENT_PACK_IS_REQUIRED_IF_ZERO_FAILS",
            "reason": "surviving residuals are testable only when units, basis, maps, and bounds are explicit",
            "next_action": "do not use qualitative smallness as evidence",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1770_3_best_next",
            "decision": "SECTOR_ACTION_VARIATION_AND_LOCAL_SCALING_SILENCE_IS_NEXT",
            "reason": "this is the smallest derivation target that can actually prove or reject EH dominance",
            "next_action": "build 1771 sector-by-sector variation/scaling silence or operator-bound pack",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1770_0_EH_dominance",
            "claim": "EH dominance is parent-derived",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_SECTOR_SILENCE_CERTIFICATES_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1770_1_residual_silence",
            "claim": "all non-EH residual sectors are zero/suppressed",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_OPERATOR_BASIS_SCALING_BOUND_MAPS_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1770_2_operator_bounds",
            "claim": "operator coefficients have source-backed bounds",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_SOURCE_BACKED_COEFFICIENT_ROWS_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1770_3_poisson_newton",
            "claim": "Poisson/Newton limit follows",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_SOURCE_NORMALIZATION_WORLDTUBE_GAUSS_CLOSURE_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1770_4_ppn_local",
            "claim": "PPN/local-GR residuals pass",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_PPN_OPERATOR_MAPS_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1770_5_public_claim",
            "claim": "local GR/Newton/R10/WEP claim allowed",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_EH_DOMINANCE_NOT_PROVED",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1770_0_primary",
            "next_target": "1771-Y5-R2FR-sector-action-variation-and-local-scaling-silence-or-operator-bounds.md",
            "script": "scripts/Y5_R2FR_sector_action_variation_and_local_scaling_silence_or_operator_bounds.py",
            "objective": "derive or reject local silence/suppression for each non-EH sector by varying its parent action block and estimating local scaling; otherwise fill source-backed operator-bound rows",
            "selection_status": "selected",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1770_1_fallback",
            "next_target": "1771b-Y5-R2FR-Poisson-Gauss-worldtube-source-normalization-pack.md",
            "script": "scripts/Y5_R2FR_Poisson_Gauss_worldtube_source_normalization_pack.py",
            "objective": "derive or stage the source-normalization/worldtube/Gauss bridge needed before measured GM or inverse-square orbital claims",
            "selection_status": "held_fallback",
            "valid_for_claim": False,
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "eh_dominance": eh_dominance_rows(),
        "residual_silence": residual_silence_rows(),
        "operator_coefficients": operator_coefficient_rows(),
        "empirical_map": empirical_map_rows(),
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
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1770_SOURCE_REGISTER.csv")
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        filename = path.name
        shutil.copy2(path, MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(path, QUARANTINE / filename)
        shutil.copy2(path, RAB_QUEUE / f"JR1770_{key.upper()}.csv")


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
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1770_SOURCE_REGISTER.csv").exists():
        return False
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        filename = path.name
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1770_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched_for_1770() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*1770*"))


def csv_parse_all() -> bool:
    return all(parse_csv_ok(path) for key, path in OUTPUTS.items() if key != "validation")


def eh_attempt_recorded(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["attempt_id"] == "EHD1770_0_target"
        and row["status"] == "TARGET_EXACT"
        for row in rows_map["eh_dominance"]
    )


def eh_not_promoted(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["attempt_id"] == "EHD1770_4_current_verdict"
        and row["status"] == "FAIL_CURRENT_PARENT_PROOF"
        and row["claim_allowed"] is False
        for row in rows_map["eh_dominance"]
    )


def residuals_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["sector_id"] == "RSS1770_6_verdict"
        and row["status"] == "RESIDUAL_SECTORS_RETAINED_NONCLAIM"
        for row in rows_map["residual_silence"]
    ) and all(row["valid_for_claim"] is False for row in rows_map["residual_silence"])


def coefficient_pack_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    rows = rows_map["operator_coefficients"]
    return any(row["row_id"] == "OPC1770_0_total_DeltaE" for row in rows) and all(
        row["valid_for_claim"] is False for row in rows
    )


def empirical_map_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return all(row["valid_for_claim"] is False for row in rows_map["empirical_map"])


def countermodel_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["countermodel_id"] == "CM1770_4_verdict"
        and row["survives_current_constraints"] is True
        and row["valid_for_claim"] is False
        for row in rows_map["countermodel"]
    )


def next_selected(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["route_id"] == "NEXT1770_0_primary" and row["selection_status"] == "selected"
        for row in rows_map["next_target"]
    )


def bridge_next(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["status_id"] == "BGS1770_4_next"
        and row["current_status"] == "SECTOR_VARIATION_AND_LOCAL_SCALING_SILENCE_IS_NEXT"
        for row in rows_map["bridge_status"]
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
        check_row("VAL1770_0_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist", "one or more cited source paths missing"),
        check_row("VAL1770_1_needles_present", all(row["needles_present"] for row in sources), "required source needles are present", "one or more source needles missing"),
        check_row("VAL1770_2_eh_attempt", eh_attempt_recorded(rows_map), "EH dominance target recorded", "EH dominance target missing"),
        check_row("VAL1770_3_eh_not_promoted", eh_not_promoted(rows_map), "EH dominance remains unproved/nonclaim", "EH dominance was promoted"),
        check_row("VAL1770_4_residuals_retained", residuals_retained(rows_map), "residual sectors retained as nonclaim", "residual sector verdict missing or promoted"),
        check_row("VAL1770_5_coefficient_pack_nonclaim", coefficient_pack_nonclaim(rows_map), "operator coefficient rows remain nonclaim", "coefficient pack missing or promoted"),
        check_row("VAL1770_6_empirical_map_nonclaim", empirical_map_nonclaim(rows_map), "empirical map rows remain nonclaim", "empirical map promoted"),
        check_row("VAL1770_7_countermodel_retained", countermodel_retained(rows_map), "EH-dominance countermodel remains retained", "countermodel missing or promoted"),
        check_row("VAL1770_8_bridge_next", bridge_next(rows_map), "sector variation/local scaling selected next", "bridge next status missing"),
        check_row(
            "VAL1770_9_claim_gates_safe",
            all(row["gate_pass"] is False and row["status"] == "BLOCKED" for row in claim_gates),
            "all claim gates remain blocked",
            "one or more claim gates opened",
        ),
        check_row("VAL1770_10_no_claim_flags", no_claim_flags(rows_map), "claim/no-score flags stay false", "one or more claim/no-score flags enabled"),
        check_row("VAL1770_11_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready", "a MISSING_* row is marked ready"),
        check_row(
            "VAL1770_12_decision_next",
            any(row["decision_id"] == "DEC1770_3_best_next" and row["decision"] == "SECTOR_ACTION_VARIATION_AND_LOCAL_SCALING_SILENCE_IS_NEXT" for row in rows_map["decision"]),
            "decision selects sector-variation/local-scaling route",
            "best-next decision missing",
        ),
        check_row("VAL1770_13_next_selected", next_selected(rows_map), "next target selected", "next target missing"),
        check_row("VAL1770_14_csv_parse", csv_parse_all(), "all generated 1770 CSVs parse", "one or more generated 1770 CSVs fail to parse"),
        check_row("VAL1770_15_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "branch copies missing"),
        check_row("VAL1770_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check_row("VAL1770_17_formalization_untouched", formalization_untouched_for_1770(), "no 1770 outputs found under formalization-workbench", "1770 outputs found under formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in checks)
    checks.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1770_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1770 EH dominance and residual-sector silence or operator coefficient pack",
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
        "# 1770 - EH Dominance And Residual-Sector Silence Or Operator Coefficient Pack",
        "",
        "## Verdict",
        "- 1770 attempts the real GR-left-hand closure: prove the parent LHS is Einstein-Hilbert dominated in the local branch.",
        "- The exact theorem shape is now clear: `E_LHS = G_munu + Lambda g_munu + sum_i epsilon_i E_i`, and every non-EH residual must be zero, suppressed below local tolerance, reclassified, or bounded.",
        "- The current corpus does not yet prove this. Sector-by-sector parent variations, local scaling, boundary silence, projector commutator silence, and source-normalization closure remain missing.",
        "- Therefore EH dominance is not claimed. The surviving residuals are staged as operator coefficient rows tied to PPN, R10, clocks, orbits, and cosmology.",
        "- No GitHub, public, local-GR, Newton, PPN, WEP, clock, orbital, R10, or `q_loc=0` claim is made.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## EH Dominance Theorem Attempt",
        markdown_table(rows_map["eh_dominance"], ["attempt_id", "claim_piece", "mathematical_form", "status", "derivation_result", "remaining_gap"]),
        "",
        "## Residual Sector Silence Audit",
        markdown_table(rows_map["residual_silence"], ["sector_id", "sector", "mathematical_form", "silence_route", "status", "coefficient_row"]),
        "",
        "## Operator Coefficient Pack",
        markdown_table(rows_map["operator_coefficients"], ["row_id", "quantity", "definition", "mathematical_form", "units", "status", "test_links"]),
        "",
        "## Empirical Bound Map",
        markdown_table(rows_map["empirical_map"], ["map_id", "observable", "sensitive_coefficients", "claim_condition", "status"]),
        "",
        "## Countermodel Ledger",
        markdown_table(rows_map["countermodel"], ["countermodel_id", "countermodel", "mathematical_form", "survives_current_constraints", "why_survives", "what_kills_it"]),
        "",
        "## GR Bridge Status",
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
        "This checkpoint keeps the project honest. The path to GR is not merely saying EH appears somewhere; it is proving the MTS sectors either do not contribute locally or contribute in a controlled, bounded way. The next derivation target is therefore sector-by-sector: vary each retained action block, estimate its local scaling, and either silence it or turn it into a real test coefficient.",
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
    doc_path = ROOT / "1770-Y5-R2FR-EH-dominance-and-residual-sector-silence-or-operator-coefficient-pack.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1770 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
