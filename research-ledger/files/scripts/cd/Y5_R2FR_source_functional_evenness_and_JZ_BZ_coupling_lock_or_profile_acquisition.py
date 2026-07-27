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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1792"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1792_0_1791_doc",
        "source_key": "1791_handoff",
        "source_path": ROOT / "1791-Y5-R2FR-response-displacement-conjugacy-owner-refresh-or-q_loc-profile-pack.md",
        "needles": ["DEC1791_3_next", "NEXT1791_0_primary"],
        "role": "selects source-functional evenness and J_Z/B_Z coupling lock as 1792 target",
    },
    {
        "source_id": "SRC1792_1_1791_validation",
        "source_key": "1791_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1791_VALIDATION.csv",
        "needles": ["VAL1791_OVERALL", "PASS"],
        "role": "confirms 1791 passed",
    },
    {
        "source_id": "SRC1792_2_1791_amplitude_law",
        "source_key": "1791_amplitude_cr2",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1791_AMPLITUDE_AND_CR2_LAW.csv",
        "needles": ["ACL1791_0_sourced_extremum", "ACL1791_5_verdict"],
        "role": "defines how the source vector enters amplitude and c_R2 laws",
    },
    {
        "source_id": "SRC1792_3_1791_profile_pack",
        "source_key": "1791_profile_pack",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1791_QLOC_CR2_PROFILE_PACK.csv",
        "needles": ["QCP1791_2_source_vector", "QCP1791_7_acceptance"],
        "role": "strict pack already names missing source-vector fields",
    },
    {
        "source_id": "SRC1792_4_1353_no_linear_source",
        "source_key": "1353_no_linear_source",
        "source_path": RESIDUALS / "P8_Y5_R10_1353_NO_LINEAR_SOURCE_THEOREM_ATTEMPT.csv",
        "needles": ["NLS1353_0_exchange_symmetry", "NLS1353_5_verdict"],
        "role": "prior no-linear-source theorem attempt",
    },
    {
        "source_id": "SRC1792_5_1353_jz_bz",
        "source_key": "1353_jz_bz_pack",
        "source_path": RESIDUALS / "P8_Y5_R10_1353_JZ_BZ_SOURCE_PACK.csv",
        "needles": ["JZ1353_0_bulk_JZ", "JZ1353_3_Y6_extra_stress"],
        "role": "source coefficient pack names J_Z, B_Z, Y5, Y6 and readout/species channels",
    },
    {
        "source_id": "SRC1792_6_yloc_no_linear",
        "source_key": "yloc_no_linear_theorem",
        "source_path": RESIDUALS / "P8_YLOC_NO_LINEAR_SOURCE_THEOREM.csv",
        "needles": ["T1_exact_reflection", "T5_current_corpus"],
        "role": "older local no-linear-source theorem contract",
    },
    {
        "source_id": "SRC1792_7_yloc_component_audit",
        "source_key": "yloc_component_audit",
        "source_path": RESIDUALS / "P8_YLOC_NO_LINEAR_SOURCE_COMPONENT_AUDIT.csv",
        "needles": ["Y5_source_normalization", "Y6_stress_Bianchi"],
        "role": "component audit identifies Y5 and Y6 as not zeroed",
    },
    {
        "source_id": "SRC1792_8_yloc_noether",
        "source_key": "yloc_noether_audit",
        "source_path": RESIDUALS / "P8_YLOC_SOURCE_CURRENT_NOETHER_AUDIT.csv",
        "needles": ["N4_no_linear_source_symmetry", "N5_verdict"],
        "role": "Noether alone owns currents but does not zero them",
    },
    {
        "source_id": "SRC1792_9_y5_even_scalar",
        "source_key": "y5_even_scalar_gate",
        "source_path": RESIDUALS / "P8_Y5_SOURCE_NORMALIZATION_EVEN_SCALAR_GATE.csv",
        "needles": ["ES518_0_exchange_parity", "ES518_4_bound_branch_trigger"],
        "role": "Y5 measured source strength is an even scalar, not killed by response parity",
    },
    {
        "source_id": "SRC1792_10_y5_owner",
        "source_key": "y5_owner_theorem",
        "source_path": RESIDUALS / "P8_Y5_SOURCE_NORMALIZATION_OWNER_THEOREM.csv",
        "needles": ["Y5O_2_constant_universal_coupling", "Y5O_8_owner_theorem"],
        "role": "source-normalization owner theorem requirements",
    },
    {
        "source_id": "SRC1792_11_source_current_closure",
        "source_key": "source_current_closure",
        "source_path": RESIDUALS / "P8_Y5_SOURCE_CURRENT_CLOSURE_THEOREM_ATTEMPT.csv",
        "needles": ["SC532_2_charge_current_variation_identity", "SC532_7_measured_GM_next_gate"],
        "role": "charge-current equality is necessary but not sufficient for Newton",
    },
    {
        "source_id": "SRC1792_12_ward_bridge",
        "source_key": "source_current_ward_bridge",
        "source_path": RESIDUALS / "P8_Y5_SOURCE_CURRENT_WARD_BRIDGE.csv",
        "needles": ["WB520_4_exact_product_obstruction", "WB520_6_conditional_closure_theorem"],
        "role": "projected mass-current product obstruction",
    },
    {
        "source_id": "SRC1792_13_source_measure_flux",
        "source_key": "source_measure_meff_flux",
        "source_path": RESIDUALS / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv",
        "needles": ["T509_0_charge_identity_needed", "T509_2_no_extra_mass_channel"],
        "role": "measured source mass needs parent charge identity and no extra mass channel",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1792_SOURCE_REGISTER.csv",
    "evenness_theorem_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1792_EVENNESS_THEOREM_ATTEMPT.csv",
    "coupling_decomposition": RESIDUALS / "P8_Y5_PARENT_QLOC_1792_COUPLING_DECOMPOSITION.csv",
    "component_coupling_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1792_COMPONENT_COUPLING_GATE.csv",
    "jz_bz_acquisition_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1792_JZ_BZ_ACQUISITION_LEDGER.csv",
    "countermodel_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1792_COUNTERMODEL_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1792_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1792_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1792_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1792_VALIDATION.csv",
}

DOC_PATH = ROOT / "1792-Y5-R2FR-source-functional-evenness-and-JZ-BZ-coupling-lock-or-profile-acquisition.md"


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
                "role": source["role"],
            }
        )
    return rows


def evenness_theorem_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "EVT1792_0_source_expansion",
            "statement": "expand all source, matter, boundary and readout functionals around Z=0",
            "mathematical_form": "S_src[E,Z,psi,eta] = S_src^0[E,psi,eta] + J_A[eta] Z^A + 1/2 Z^A N_AB[eta] Z^B + B_A[eta] Z^A|_boundary + ...",
            "result": "EXACT_LOCAL_EXPANSION_CONTRACT",
            "blocker": "J_A and B_A must be zero theorem or finite sourced rows",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "EVT1792_1_exchange_evenness_condition",
            "statement": "exchange symmetry kills linear source terms only if all source labels are exchange-even",
            "mathematical_form": "S_src[E,Z,psi,eta_even] = S_src[E,-Z,psi,eta_even] => J_A=B_A=0 at Z=0",
            "result": "EXACT_CONDITIONAL_EVENNESS_THEOREM",
            "blocker": "observed coframe, source charge, species labels, domain markers, boundary references and readout maps are not all parent-shown to be eta_even",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "EVT1792_2_matter_minimal_route",
            "statement": "minimal matter coupling would be safe only if matter sees E/coframe data and not odd Z",
            "mathematical_form": "S_m[g(E),psi] with delta S_m/delta Z^A|_0 = (delta S_m/delta g_mn)(delta g_mn/delta Z^A)|_0 = 0 if g(E,Z) is even in Z",
            "result": "CONDITIONAL_ROUTE_NOT_PARENT_OWNED",
            "blocker": "same-observed-coframe and readout-before/after-variation clauses remain unsigned",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "EVT1792_3_boundary_evenness",
            "statement": "boundary terms must be exchange-even or exact no-flux terms",
            "mathematical_form": "delta S_bdy/delta Z^A|_0 = 0 if S_bdy[Z]=S_bdy[-Z] or int_boundary dTheta_Z=0 on linked compact local domains",
            "result": "CONDITIONAL_BOUNDARY_ROUTE",
            "blocker": "boundary/collar markers and linking-sphere flux are not theorem-zero",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "EVT1792_4_Y5_parity_failure",
            "statement": "source-normalization Y5 is not killed by response parity",
            "mathematical_form": "Y5=Delta_mu_source is an observed even scalar source strength; Z -> -Z does not force Delta_mu_source=0",
            "result": "PHYSICAL_Y5_NOT_ZEROED_BY_PARITY",
            "blocker": "Y5 needs parent source-charge owner theorem or finite bound rows",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "EVT1792_5_Y6_conservation_failure",
            "statement": "Bianchi/conservation does not zero extra stress",
            "mathematical_form": "nabla_mu(T_EH^{mu nu}+T_extra^{mu nu})=0 does not imply T_extra=0 or Pi_PPN T_extra=0",
            "result": "PHYSICAL_Y6_NOT_ZEROED_BY_WARD_ALONE",
            "blocker": "Y6 needs topological invisibility, projector-null theorem, or finite stress-response rows",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "EVT1792_6_verdict",
            "statement": "source-functional evenness theorem for current MTS local branch",
            "mathematical_form": "EVT1792_1 plus matter, boundary, readout, Y5 and Y6 clauses all close",
            "result": "THEOREM_NOT_PROVED_CURRENT_CORPUS",
            "blocker": "Y5/Y6/source/readout/boundary coupling channels remain active",
            "parent_signed": False,
            "valid_for_claim": False,
        },
    ]


def coupling_decomposition_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "coupling_id": "CPD1792_0_total_source_vector",
            "object": "J_total_A",
            "decomposition": "J_total_A = J_matter_A + B_boundary_A + J_Y5_A + J_Y6_A + J_species_A + J_readout_A + B_R_A R + B_T_A T + B_frame_A",
            "zero_route": "each term is exchange-even/orthogonal/topological or parent-projected zero",
            "finite_route": "source-backed coefficient vector with units and arena projection",
            "current_status": "MISSING_TOTAL_SOURCE_VECTOR",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "coupling_id": "CPD1792_1_matter",
            "object": "J_matter_A",
            "decomposition": "delta S_matter/delta Z^A|_0",
            "zero_route": "same observed coframe depends only on exchange-even E fields",
            "finite_route": "species/material source charge map",
            "current_status": "SAME_COFRAME_NOT_PARENT_DERIVED",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "coupling_id": "CPD1792_2_boundary",
            "object": "B_boundary_A",
            "decomposition": "linear boundary/corner/linking-sphere response after integrations by parts",
            "zero_route": "no-flux or exact topological subtraction before readout",
            "finite_route": "boundary coefficient/profile with units",
            "current_status": "BOUNDARY_EVENNESS_OPEN",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "coupling_id": "CPD1792_3_Y5",
            "object": "J_Y5_A",
            "decomposition": "source-normalization/measured-GM response projected onto Z",
            "zero_route": "mu_obs=G0 M_H from parent source charge with no extra mass projection",
            "finite_route": "Gdot/radial/species/range/frame/mu_extra coefficient vector",
            "current_status": "PHYSICAL_EVEN_SCALAR_NOT_PARITY_ZEROED",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "coupling_id": "CPD1792_4_Y6",
            "object": "J_Y6_A and Delta_K_Y6",
            "decomposition": "extra-stress response in Khat/Ward/PPN channels",
            "zero_route": "topological invisibility or projector-null theorem",
            "finite_route": "PPN/source-stress bound rows",
            "current_status": "CONSERVATION_NOT_ZERO",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "coupling_id": "CPD1792_5_readout_species",
            "object": "J_readout_A + J_species_A",
            "decomposition": "post-readout and material/source composition dependence linear in Z",
            "zero_route": "readout-after-variation theorem and species-blind parent source theorem",
            "finite_route": "species/material coefficient map",
            "current_status": "MISSING_READOUT_AND_SPECIES_MAPS",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def component_coupling_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "component_id": "CCG1792_0_Y0_trace",
            "component": "Y0 trace/scalar residual",
            "gate_status": "CONDITIONAL_ONLY",
            "reason": "matter trace can source scalar response unless matter neutrality and stationarity are derived",
            "next_action": "same-coframe matter neutrality or finite trace-source row",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "CCG1792_1_Y2_boundary_flux",
            "component": "Y2 boundary flux",
            "gate_status": "NOT_ZEROED",
            "reason": "boundary/collar markers can source vector flux unless boundary scalar evenness and no-flux are proved",
            "next_action": "boundary no-flux theorem or boundary coefficient row",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "CCG1792_2_Y3Y4_domain",
            "component": "domain vector/STF stress",
            "gate_status": "NOT_ZEROED",
            "reason": "domain markers and tidal STF stress can couple linearly",
            "next_action": "domain no-vector/isotropy theorem or finite domain coefficient rows",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "CCG1792_3_Y5_source_normalization",
            "component": "Y5 source-normalization",
            "gate_status": "HARD_BLOCK_NOT_PARITY_ZEROED",
            "reason": "Y5 is observed even scalar source strength; response-doublet parity alone cannot set measured GM drift/source-normalization to zero",
            "next_action": "parent source-charge owner theorem or Gdot/radial/species/range/frame/mu_extra bound pack",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "CCG1792_4_Y6_extra_stress",
            "component": "Y6 extra stress/Bianchi channel",
            "gate_status": "HARD_BLOCK_CONSERVATION_NOT_ZERO",
            "reason": "Bianchi identity gives total conservation, not absence of extra stress in PPN/source channels",
            "next_action": "topological/projector-null stress theorem or finite PPN/source-stress rows",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "CCG1792_5_verdict",
            "component": "component coupling lock",
            "gate_status": "COUPLING_LOCK_NOT_CLOSED",
            "reason": "Y5 and Y6 keep the source-functional evenness theorem from activating",
            "next_action": "prioritize Y5 source-charge owner and Y6 extra-stress gate",
            "valid_for_claim": False,
        },
    ]


def jz_bz_acquisition_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "acq_id": "ACQ1792_0_bulk_JZ",
            "symbol": "J_Z^A",
            "definition": "bulk source current delta S_source/delta Z_A evaluated at Z=0",
            "required_evidence": "zero theorem or numeric component vector with units, source path and projection map",
            "current_status": "MISSING_JZ_THEOREM_OR_VALUE",
            "valid_for_claim": False,
            "accepted_for_scoring": False,
        },
        {
            "branch_id": BRANCH_ID,
            "acq_id": "ACQ1792_1_boundary_BZ",
            "symbol": "B_Z^A",
            "definition": "linear boundary/source-current term from integrations by parts and linking-sphere flux",
            "required_evidence": "zero-flux theorem or boundary profile/bound",
            "current_status": "MISSING_BZ_THEOREM_OR_VALUE",
            "valid_for_claim": False,
            "accepted_for_scoring": False,
        },
        {
            "branch_id": BRANCH_ID,
            "acq_id": "ACQ1792_2_Y5_source_normalization",
            "symbol": "J_Z[Y5]",
            "definition": "measured-GM/source-normalization response projected onto Z",
            "required_evidence": "parent source-charge theorem or coefficient vector for Gdot, radial, species, range, frame, mu_extra, beta/PPN and q_loc projection",
            "current_status": "RETAINED_NONCLAIM_HARD_BLOCK",
            "valid_for_claim": False,
            "accepted_for_scoring": False,
        },
        {
            "branch_id": BRANCH_ID,
            "acq_id": "ACQ1792_3_Y6_extra_stress",
            "symbol": "J_Z[Y6]; Delta_K[Y6]",
            "definition": "extra-stress response entering Khat/Ward/q_loc at linear order",
            "required_evidence": "topological invisibility theorem, projector-null theorem, or finite PPN/source-stress bound",
            "current_status": "RETAINED_NONCLAIM_HARD_BLOCK",
            "valid_for_claim": False,
            "accepted_for_scoring": False,
        },
        {
            "branch_id": BRANCH_ID,
            "acq_id": "ACQ1792_4_readout_species",
            "symbol": "J_Z[readout/species]",
            "definition": "post-readout/material/source composition dependence linear in Z",
            "required_evidence": "readout-after-variation theorem and species-blind theorem or finite composition map",
            "current_status": "MISSING_READOUT_SPECIES_MAP",
            "valid_for_claim": False,
            "accepted_for_scoring": False,
        },
        {
            "branch_id": BRANCH_ID,
            "acq_id": "ACQ1792_5_acceptance",
            "symbol": "J_total_A",
            "definition": "complete coupling-lock vector for the response-displacement branch",
            "required_evidence": "all ACQ1792_0 through ACQ1792_4 zeroed or sourced with units and arena maps",
            "current_status": "REJECT_CURRENT_COUPLING_PACK",
            "valid_for_claim": False,
            "accepted_for_scoring": False,
        },
    ]


def countermodel_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1792_0_even_scalar_Y5",
            "countermodel": "Y5 is an even measured source strength and survives Z parity",
            "survives_current_constraints": True,
            "why_survives": "ES518_0 explicitly fails exchange parity for physical Y5",
            "what_kills_it": "parent source-charge owner theorem or finite source-normalization bound rows",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1792_1_extra_stress_conserved_nonzero",
            "countermodel": "Y6 extra stress is conserved with total stress but remains nonzero",
            "survives_current_constraints": True,
            "why_survives": "Bianchi/Ward identities do not imply T_extra=0",
            "what_kills_it": "topological invisibility/projector-null theorem or finite PPN stress bounds",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1792_2_projected_mass_commutator",
            "countermodel": "d(Pi_M J_H) has a commutator or extra exchange term causing radial/source mass hair",
            "survives_current_constraints": True,
            "why_survives": "WB520 product obstruction and Y5 owner theorem remain open",
            "what_kills_it": "parent Pi_M, zero commutator, zero extra projection and no anomaly",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1792_3_boundary_marker",
            "countermodel": "boundary/collar marker creates a linear B_Z even when bulk source is even",
            "survives_current_constraints": True,
            "why_survives": "boundary evenness/no-flux is open",
            "what_kills_it": "boundary scalar evenness or linked compact no-flux theorem",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1792_4_species_readout_source",
            "countermodel": "species/material/readout labels are odd or post-variation and generate J_Z",
            "survives_current_constraints": True,
            "why_survives": "species/readout source maps are missing",
            "what_kills_it": "species-blind/readout-after-variation theorem or finite composition map",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1792_0_no_linear_source",
            "claim": "J_Z=B_Z=0 for the local response branch",
            "status": "BLOCKED",
            "reason": "source-functional evenness is conditional and Y5/Y6 remain active",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1792_1_physical_F1_zero",
            "claim": "formal F1=0 becomes physical q_loc zero",
            "status": "BLOCKED",
            "reason": "component/source coupling lock not closed",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1792_2_Y5_source_normalization_zero",
            "claim": "measured source normalization is theorem-zero",
            "status": "BLOCKED",
            "reason": "parent source-charge owner theorem premises are not satisfied",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1792_3_Y6_extra_stress_zero",
            "claim": "extra stress is absent/projector-null in local GR branch",
            "status": "BLOCKED",
            "reason": "Bianchi conservation is not a zero theorem",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1792_4_q_loc_cR2_scores",
            "claim": "q_loc/c_R2/R10/PPN scores can be run",
            "status": "BLOCKED",
            "reason": "J_total_A acquisition ledger is rejected and not score-ready",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1792_5_local_GR_Newton",
            "claim": "derived local GR/Newton reduction",
            "status": "BLOCKED",
            "reason": "source-normalized Newton, extra stress, q_loc, c_R2 and PPN gates are not jointly closed",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1792_0_evenness",
            "decision": "SOURCE_FUNCTIONAL_EVENNESS_NOT_PROVED",
            "reason": "exchange symmetry gives an exact conditional zero theorem, but current source labels/readout/boundary/Y5/Y6 are not all parent-even",
            "next_action": "do not use response parity as a local-GR proof",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1792_1_Y5",
            "decision": "Y5_SOURCE_NORMALIZATION_IS_PRIMARY_HARD_BLOCK",
            "reason": "Y5 is an observed even scalar and cannot be killed by Z parity; it needs source-charge ownership or finite rows",
            "next_action": "attack source-normalized EH charge owner theorem first",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1792_2_Y6",
            "decision": "Y6_EXTRA_STRESS_REMAINS_SECOND_HARD_BLOCK",
            "reason": "conservation/Ward identities do not zero extra stress by themselves",
            "next_action": "build a topological/projector-null stress gate or finite PPN/source-stress rows",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1792_3_next",
            "decision": "Y5_SOURCE_CHARGE_OWNER_AND_Y6_EXTRA_STRESS_GATE_NEXT",
            "reason": "the least-scrutiny route is to derive Newton's source charge from the parent EH/Hilbert/Noether mass chain and isolate Y6 separately",
            "next_action": "build 1793 source-normalized EH charge owner or finite Y5/Y6 coupling pack",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1792_0_primary",
            "next_target": "1793-Y5-R2FR-Y5-source-charge-owner-and-Y6-extra-stress-gate-or-finite-coupling-pack.md",
            "script": "scripts/Y5_R2FR_Y5_source_charge_owner_and_Y6_extra_stress_gate_or_finite_coupling_pack.py",
            "objective": "try to derive measured source normalization from a parent EH/Hilbert/Noether mass charge and separately gate Y6 extra stress; if not, emit finite nonclaim Y5/Y6 coupling rows",
            "selection_status": "selected",
            "success_condition": "Y5 source charge owner theorem plus Y6 projector-null/topological theorem, or finite source-backed coupling rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1792_1_parallel_boundary",
            "next_target": "1793b-Y5-R2FR-boundary-evenness-and-linked-flux-gate.md",
            "script": "scripts/Y5_R2FR_boundary_evenness_and_linked_flux_gate.py",
            "objective": "separate B_Z boundary/collar marker flux from bulk J_Z",
            "selection_status": "held_parallel",
            "success_condition": "boundary no-flux theorem or finite boundary profile",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1792_2_parallel_species",
            "next_target": "1793c-Y5-R2FR-species-readout-source-map.md",
            "script": "scripts/Y5_R2FR_species_readout_source_map.py",
            "objective": "map species/material/readout source labels into J_Z or prove species-blindness/readout-after-variation",
            "selection_status": "held_parallel",
            "success_condition": "species/readout zero theorem or finite composition-source map",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "evenness_theorem_attempt": evenness_theorem_attempt_rows(),
        "coupling_decomposition": coupling_decomposition_rows(),
        "component_coupling_gate": component_coupling_gate_rows(),
        "jz_bz_acquisition_ledger": jz_bz_acquisition_ledger_rows(),
        "countermodel_ledger": countermodel_ledger_rows(),
        "claim_gate": claim_gate_rows(),
        "decision_ledger": decision_ledger_rows(),
        "next_target": next_target_rows(),
    }


def fieldnames_for(rows: list[dict[str, Any]]) -> list[str]:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    return fieldnames


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames_for(rows))
        writer.writeheader()
        writer.writerows(rows)


def copy_outputs() -> None:
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        shutil.copy2(path, MICROSCOPE_RESIDUALS / path.name)
        shutil.copy2(path, QUARANTINE / path.name)
        shutil.copy2(path, RAB_QUEUE / f"JR1792_{key.upper()}.csv")


def boolish(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"1", "true", "yes", "y", "pass", "passed"}


def sources_ok(rows_map: dict[str, list[dict[str, Any]]]) -> tuple[bool, bool]:
    rows = rows_map["source_register"]
    return (
        all(boolish(row["exists"]) for row in rows),
        all(boolish(row["needles_present"]) for row in rows),
    )


def parse_csv(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except csv.Error:
        return False


def generated_csvs() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            for flag in (
                "valid_for_claim",
                "claim_allowed",
                "score_ready",
                "score_emitted",
                "accepted_for_scoring",
                "theorem_closed_for_claim",
                "parent_signed",
                "valid_prediction_row",
                "gate_pass",
            ):
                if flag in row and boolish(row[flag]):
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            text = " ".join(str(value) for value in row.values()).upper()
            if "MISSING" in text:
                for flag in (
                    "valid_for_claim",
                    "claim_allowed",
                    "score_ready",
                    "score_emitted",
                    "accepted_for_scoring",
                    "theorem_closed_for_claim",
                    "valid_prediction_row",
                    "gate_pass",
                ):
                    if boolish(row.get(flag, False)):
                        return False
    return True


def branch_copies_exist() -> bool:
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        if not (MICROSCOPE_RESIDUALS / path.name).exists():
            return False
        if not (QUARANTINE / path.name).exists():
            return False
        if not (RAB_QUEUE / f"JR1792_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    generated_names = {path.name for path in OUTPUTS.values()}
    generated_names.add(DOC_PATH.name)
    return not any(path.name in generated_names for path in FORMALIZATION.rglob("*"))


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    exists_ok, needles_ok = sources_ok(rows_map)
    checks: list[tuple[str, bool, str]] = [
        ("VAL1792_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1792_1_needles_present", needles_ok, "all cited source needles are present"),
        (
            "VAL1792_2_evenness_theorem_attempted",
            any(row["theorem_id"] == "EVT1792_1_exchange_evenness_condition" and row["result"] == "EXACT_CONDITIONAL_EVENNESS_THEOREM" for row in rows_map["evenness_theorem_attempt"]),
            "exchange-evenness theorem condition is written",
        ),
        (
            "VAL1792_3_theorem_not_proved",
            any(row["theorem_id"] == "EVT1792_6_verdict" and row["result"] == "THEOREM_NOT_PROVED_CURRENT_CORPUS" for row in rows_map["evenness_theorem_attempt"])
            and all(not boolish(row["parent_signed"]) and not boolish(row["valid_for_claim"]) for row in rows_map["evenness_theorem_attempt"]),
            "source-functional evenness is not promoted",
        ),
        (
            "VAL1792_4_y5_y6_explicit",
            any(row["theorem_id"] == "EVT1792_4_Y5_parity_failure" and row["result"] == "PHYSICAL_Y5_NOT_ZEROED_BY_PARITY" for row in rows_map["evenness_theorem_attempt"])
            and any(row["theorem_id"] == "EVT1792_5_Y6_conservation_failure" and row["result"] == "PHYSICAL_Y6_NOT_ZEROED_BY_WARD_ALONE" for row in rows_map["evenness_theorem_attempt"]),
            "Y5 and Y6 failure modes are explicit",
        ),
        (
            "VAL1792_5_coupling_decomposition",
            any(row["coupling_id"] == "CPD1792_0_total_source_vector" and row["current_status"] == "MISSING_TOTAL_SOURCE_VECTOR" for row in rows_map["coupling_decomposition"])
            and all(not boolish(row["score_ready"]) for row in rows_map["coupling_decomposition"]),
            "total source vector decomposition is strict and non-scoreable",
        ),
        (
            "VAL1792_6_component_gate_blocks",
            any(row["component_id"] == "CCG1792_5_verdict" and row["gate_status"] == "COUPLING_LOCK_NOT_CLOSED" for row in rows_map["component_coupling_gate"]),
            "component coupling gate remains blocked",
        ),
        (
            "VAL1792_7_acquisition_rejected",
            any(row["acq_id"] == "ACQ1792_5_acceptance" and row["current_status"] == "REJECT_CURRENT_COUPLING_PACK" for row in rows_map["jz_bz_acquisition_ledger"])
            and all(not boolish(row["accepted_for_scoring"]) and not boolish(row["valid_for_claim"]) for row in rows_map["jz_bz_acquisition_ledger"]),
            "J_Z/B_Z acquisition ledger rejects current pack",
        ),
        (
            "VAL1792_8_countermodels_retained",
            all(boolish(row["survives_current_constraints"]) for row in rows_map["countermodel_ledger"]),
            "countermodels remain live",
        ),
        (
            "VAL1792_9_claim_gates_blocked",
            all(row["status"] == "BLOCKED" and not boolish(row["gate_pass"]) and not boolish(row["valid_for_claim"]) for row in rows_map["claim_gate"]),
            "claim gates are blocked",
        ),
        ("VAL1792_10_no_claim_flags", no_claim_flags(rows_map), "no generated score/claim flags are true"),
        ("VAL1792_11_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1792_12_decision_next",
            any(
                row["decision_id"] == "DEC1792_3_next"
                and row["decision"] == "Y5_SOURCE_CHARGE_OWNER_AND_Y6_EXTRA_STRESS_GATE_NEXT"
                for row in rows_map["decision_ledger"]
            ),
            "decision selects Y5/Y6 owner gate next",
        ),
        (
            "VAL1792_13_next_selected",
            any(row["route_id"] == "NEXT1792_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1792_14_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1792 CSVs parse"),
        ("VAL1792_15_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1792_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1792_17_formalization_untouched", formalization_untouched(), "no 1792 outputs found under formalization-workbench"),
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
            "check_id": "VAL1792_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1792 source-functional evenness and J_Z/B_Z coupling lock checkpoint",
        }
    )
    return rows


def clean_cell(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "/")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(clean_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, str]]) -> str:
    return "\n".join(
        [
            "# 1792 - Y5/R2FR Source-Functional Evenness and JZ/BZ Coupling Lock",
            "",
            "## Verdict",
            "",
            "1792 goes directly at the coupling. The exact conditional theorem is clear: if every source, matter, boundary and readout functional is exchange-even in the response displacement `Z`, then the linear source vector vanishes: `J_Z=B_Z=0`. That would let the 1791 formal `F_1=0` become physical.",
            "",
            "But the current corpus does not prove the required evenness. The key obstruction is not mysterious anymore: `Y5` source-normalization is an observed even scalar source-strength channel, so `Z -> -Z` does not force measured GM/source normalization to vanish. `Y6` extra stress is also not killed by Bianchi conservation; total conservation is not absence of extra stress. Therefore 1792 emits a strict nonclaim acquisition ledger for `J_Z`, `B_Z`, `Y5`, `Y6`, readout and species/source channels.",
            "",
            "**Claim ceiling:** no no-linear-source theorem, no physical `F_1=0`, no `q_loc=0`, no `c_R2=0`, no R10/PPN/clock/orbital score, no local-GR/Newton claim, no GitHub action, and no `formalization-workbench` edit is allowed from 1792.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "role"]),
            "",
            "## Evenness Theorem Attempt",
            markdown_table(rows_map["evenness_theorem_attempt"], ["theorem_id", "statement", "mathematical_form", "result", "blocker", "valid_for_claim"]),
            "",
            "## Coupling Decomposition",
            markdown_table(rows_map["coupling_decomposition"], ["coupling_id", "object", "decomposition", "zero_route", "finite_route", "current_status", "score_ready", "valid_for_claim"]),
            "",
            "## Component Coupling Gate",
            markdown_table(rows_map["component_coupling_gate"], ["component_id", "component", "gate_status", "reason", "next_action", "valid_for_claim"]),
            "",
            "## JZ/BZ Acquisition Ledger",
            markdown_table(rows_map["jz_bz_acquisition_ledger"], ["acq_id", "symbol", "definition", "required_evidence", "current_status", "accepted_for_scoring", "valid_for_claim"]),
            "",
            "## Countermodel Ledger",
            markdown_table(rows_map["countermodel_ledger"], ["countermodel_id", "countermodel", "survives_current_constraints", "why_survives", "what_kills_it"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["claim_id", "claim", "status", "reason", "gate_pass", "valid_for_claim"]),
            "",
            "## Decision Ledger",
            markdown_table(rows_map["decision_ledger"], ["decision_id", "decision", "reason", "next_action"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This is the least-smuggly route now. Do not try to make parity do too much. If local GR/Newton is going to become derived, `Y5` must be owned as a parent EH/Hilbert/Noether source charge, and `Y6` must be separated as a topological/projector-null stress theorem or bounded finite residual. That is sharper, more defensible, and much harder to accuse of a plateau axiom.",
            "",
        ]
    )


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1792 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
