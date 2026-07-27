from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
MICROSCOPE_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1861"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1861-Y5-R2FR-source-functional-evenness-JZ-BZ-coupling-lock-or-profile-acquisition.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1861_SOURCE_REGISTER.csv",
    "evenness_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1861_SOURCE_FUNCTIONAL_EVENNESS_AUDIT.csv",
    "jz_bz_lock": RESIDUALS / "P8_Y5_PARENT_QLOC_1861_JZ_BZ_COUPLING_LOCK_AUDIT.csv",
    "profile_acquisition": RESIDUALS / "P8_Y5_PARENT_QLOC_1861_JZ_BZ_PROFILE_ACQUISITION.csv",
    "route_selection": RESIDUALS / "P8_Y5_PARENT_QLOC_1861_Y5_Y6_ROUTE_SELECTION.csv",
    "qloc_impact": RESIDUALS / "P8_Y5_PARENT_QLOC_1861_QLOC_IMPACT.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1861_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1861_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1861_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1861_VALIDATION.csv",
}


def as_bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _ in fields) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join([header, separator, *body])


def source_register() -> list[dict[str, Any]]:
    sources = [
        {
            "source_id": "SRC1861_0_1860_doc",
            "source_kind": "prior_checkpoint_doc",
            "source_path": ROOT / "1860-Y5-R2FR-Gamma-Khat-q-loc-action-existence-bridge-to-local-EH-fixed-point.md",
            "required_needle": "NEXT1860_0_primary",
            "extraction_status": "FOUND_NEXT_TARGET",
            "use_in_1861": "1860 selects source-functional evenness/J_Z/B_Z coupling lock as the primary q_loc activation route.",
        },
        {
            "source_id": "SRC1861_1_1713_doc",
            "source_kind": "earlier_coupling_checkpoint",
            "source_path": ROOT / "1713-Y5-R2FR-source-functional-evenness-and-JZ-BZ-coupling-lock-or-profile-acquisition.md",
            "required_needle": "1713 does not prove source-functional exchange-evenness",
            "extraction_status": "FOUND_PRIOR_COUPLING_OBSTRUCTION",
            "use_in_1861": "1713 already separated response-density evenness from source/readout/GM/stress odd-Z leakage.",
        },
        {
            "source_id": "SRC1861_2_1792_evenness",
            "source_kind": "csv_prior_audit",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1792_EVENNESS_THEOREM_ATTEMPT.csv",
            "required_needle": "EVT1792_6_verdict",
            "extraction_status": "FOUND_THEOREM_VERDICT",
            "use_in_1861": "1792 states the exact conditional theorem but blocks activation on Y5/Y6/source/readout/boundary channels.",
        },
        {
            "source_id": "SRC1861_3_1792_jz_bz",
            "source_kind": "csv_prior_audit",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1792_JZ_BZ_ACQUISITION_LEDGER.csv",
            "required_needle": "ACQ1792_5_acceptance",
            "extraction_status": "FOUND_ACQUISITION_REJECTION",
            "use_in_1861": "1792 rejects the complete coupling-lock vector unless all J_Z/B_Z/Y5/Y6 terms are zeroed or sourced.",
        },
        {
            "source_id": "SRC1861_4_1792_component_gate",
            "source_kind": "csv_prior_audit",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1792_COMPONENT_COUPLING_GATE.csv",
            "required_needle": "CCG1792_5_verdict",
            "extraction_status": "FOUND_COMPONENT_VERDICT",
            "use_in_1861": "1792 identifies Y5 and Y6 as the hard blockers for component-level coupling closure.",
        },
        {
            "source_id": "SRC1861_5_1793_y5_owner",
            "source_kind": "csv_prior_audit",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1793_Y5_SOURCE_CHARGE_OWNER_ATTEMPT.csv",
            "required_needle": "Y5SC1793_7_verdict",
            "extraction_status": "FOUND_Y5_OWNER_VERDICT",
            "use_in_1861": "1793 shows that the parent source-charge owner theorem is not activated.",
        },
        {
            "source_id": "SRC1861_6_1793_y6_stress",
            "source_kind": "csv_prior_audit",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1793_Y6_EXTRA_STRESS_GATE.csv",
            "required_needle": "Y6G1793_5_verdict",
            "extraction_status": "FOUND_Y6_STRESS_VERDICT",
            "use_in_1861": "1793 shows that Y6 extra stress is not zeroed by Ward/Bianchi structure alone.",
        },
        {
            "source_id": "SRC1861_7_1793_finite_pack",
            "source_kind": "csv_prior_audit",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1793_FINITE_Y5Y6_COUPLING_PACK.csv",
            "required_needle": "FY1793_7_acceptance",
            "extraction_status": "FOUND_FINITE_PACK_REJECTION",
            "use_in_1861": "1793 rejects finite Y5/Y6 rows as live claim data because parent coefficients and source paths are absent.",
        },
        {
            "source_id": "SRC1861_8_1793_next",
            "source_kind": "csv_prior_decision",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1793_NEXT_TARGET.csv",
            "required_needle": "NEXT1793_0_primary",
            "extraction_status": "FOUND_ROUTE_SELECTION",
            "use_in_1861": "1793 selects parent Pi_M observed-time/Hilbert charge ownership as the primary next target.",
        },
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            **{key: str(value) if isinstance(value, Path) else value for key, value in source.items()},
            "valid_for_claim": as_bool_text(False),
        }
        for source in sources
    ]


def evenness_audit() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SFE1861_0_source_expansion_contract",
            "clause": "all matter/source/boundary/readout functionals admit a local expansion around residual Z=0",
            "mathematical_form": "S[E,Z,psi,eta]=S0[E,psi,eta]+J_A[eta]Z^A+1/2 Z^A N_AB[eta]Z^B+B_A[eta]Z^A|_boundary+...",
            "source_evidence": "EVT1792_0_source_expansion",
            "status": "EXACT_LOCAL_EXPANSION_CONTRACT",
            "blocker": "expansion alone names J_A and B_A; it does not set them to zero",
            "result_if_closed": "finite/profile route becomes well-posed, not automatically GR-safe",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SFE1861_1_exchange_evenness_condition",
            "clause": "exchange-even source labels kill all linear residual terms",
            "mathematical_form": "S[E,Z,psi,eta_even]=S[E,-Z,psi,eta_even] => J_A=B_A=0 at Z=0",
            "source_evidence": "EVT1792_1_exchange_evenness_condition",
            "status": "EXACT_CONDITIONAL_EVENNESS_THEOREM",
            "blocker": "current corpus has not proved observed coframe, source charge, species labels, domain markers, boundary references and readout maps are eta-even",
            "result_if_closed": "F1/source-current branch would close for the affected terms",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SFE1861_2_matter_coframe_readout",
            "clause": "matter, clocks, photons, source current and orbital readout descend through the same observed coframe",
            "mathematical_form": "S_m[g(E),psi] and Readout=R[q(Phi),psi] with delta/delta Z|0=0",
            "source_evidence": "EVT1792_2_matter_minimal_route;Y5SC1793_1_same_observed_coframe",
            "status": "OPEN_UNSIGNED",
            "blocker": "same-coframe and readout-before-variation clauses remain unsigned",
            "result_if_closed": "readout/species leakage would be removed from q_loc and source-normalization gates",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SFE1861_3_boundary_flux",
            "clause": "boundary and collar terms are exchange-even or exact no-flux on linked compact domains",
            "mathematical_form": "delta S_bdy/delta Z^A|0=0 if S_bdy[Z]=S_bdy[-Z] or integral_boundary dTheta_Z=0",
            "source_evidence": "EVT1792_3_boundary_evenness;ACQ1792_1_boundary_BZ",
            "status": "OPEN_UNSIGNED",
            "blocker": "boundary/collar markers and linking-sphere flux are not theorem-zero",
            "result_if_closed": "B_Z can be removed from the local residual source vector",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SFE1861_4_Y5_source_normalization",
            "clause": "measured-GM/source-normalization is a parent Hilbert/worldtube charge, not fitted-G leakage",
            "mathematical_form": "mu_obs = G_ref M_H[Pi_M J_H] with mu_extra=0 before orbital fitting",
            "source_evidence": "EVT1792_4_Y5_parity_failure;Y5SC1793_7_verdict",
            "status": "HARD_BLOCK_NOT_PARITY_ZEROED",
            "blocker": "Y5 is an observed even scalar source strength; Z -> -Z does not force Delta_mu_source=0",
            "result_if_closed": "Newton source normalization can be owned by the parent charge route",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SFE1861_5_Y6_extra_stress",
            "clause": "extra/projector stress is absent, topological, projector-null, or fully source-bounded",
            "mathematical_form": "Pi_local T_extra=0 or q_P^nu=0, not merely nabla_mu T_total^{mu nu}=0",
            "source_evidence": "EVT1792_5_Y6_conservation_failure;Y6G1793_5_verdict",
            "status": "HARD_BLOCK_CONSERVATION_NOT_ZERO",
            "blocker": "Bianchi/Ward conservation gives total conservation, not absence of extra stress in PPN/source channels",
            "result_if_closed": "Khat/Ward tail no longer contaminates q_loc/local-GR inheritance",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SFE1861_6_verdict",
            "clause": "source-functional evenness theorem for current MTS local branch",
            "mathematical_form": "SFE1861_1 plus matter, boundary, readout, Y5 and Y6 clauses all close",
            "source_evidence": "EVT1792_6_verdict;CCG1792_5_verdict",
            "status": "EVENNESS_THEOREM_NOT_ACTIVATED",
            "blocker": "Y5/Y6/source/readout/boundary coupling channels remain active",
            "result_if_closed": "would reopen the q_loc parent-zero route, but that is not current status",
            "valid_for_claim": as_bool_text(False),
        },
    ]


def jz_bz_lock_audit() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "lock_id": "JBC1861_0_bulk_JZ",
            "component": "bulk source current",
            "symbol": "J_Z^A",
            "required_evidence": "zero theorem or numeric component vector with units/source paths",
            "current_status": "MISSING_ZERO_THEOREM_OR_VALUE",
            "next_action": "derive exchange-even parent source functional or emit sourced finite rows",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "lock_id": "JBC1861_1_boundary_BZ",
            "component": "boundary/linking flux current",
            "symbol": "B_Z^A",
            "required_evidence": "zero-flux theorem or boundary profile/bound",
            "current_status": "MISSING_BOUNDARY_ZERO_OR_BOUND",
            "next_action": "prove linked-sphere no-flux or acquire boundary/collar coefficient row",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "lock_id": "JBC1861_2_readout_species",
            "component": "readout/species/material dependence",
            "symbol": "J_Z[readout/species]",
            "required_evidence": "readout-after-variation theorem and species-blind theorem",
            "current_status": "MISSING_READOUT_SPECIES_MAP",
            "next_action": "prove readout descends through q(Phi) before variation or keep finite species rows",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "lock_id": "JBC1861_3_Y5_source_normalization",
            "component": "Y5 measured-GM/source normalization",
            "symbol": "J_Z[Y5]",
            "required_evidence": "parent source-charge owner theorem or coefficient vector for all Y5 channels",
            "current_status": "HARD_BLOCK_NOT_PARITY_ZEROED",
            "next_action": "derive Pi_M observed-time/Hilbert/worldtube source charge ownership",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "lock_id": "JBC1861_4_Y6_extra_stress",
            "component": "Y6 extra stress/Bianchi tail",
            "symbol": "J_Z[Y6];Delta_K[Y6]",
            "required_evidence": "topological invisibility, projector-null theorem, or finite stress-response rows",
            "current_status": "HARD_BLOCK_CONSERVATION_NOT_ZERO",
            "next_action": "derive topological/projector-null stress theorem in parallel with Y5",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "lock_id": "JBC1861_5_acceptance",
            "component": "complete coupling-lock vector",
            "symbol": "J_total_A=(J_Z,B_Z,J_Z[Y5],J_Z[Y6],J_readout)",
            "required_evidence": "all component rows are theorem-zero or sourced with units and arena maps",
            "current_status": "REJECT_COUPLING_LOCK_NOT_CLOSED",
            "next_action": "select Y5 source-charge owner as primary route and Y6 stress gate as parallel route",
            "valid_for_claim": as_bool_text(False),
        },
    ]


def profile_acquisition() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "profile_id": "PFA1861_0_JZ_vector",
            "symbol": "J_Z^A",
            "required_numeric_input": "component vector in a declared residual basis",
            "units": "action_density_per_Z_component or arena-normalized equivalent",
            "required_source_path": "MISSING_PARENT_SOURCE_PATH",
            "arena_maps": "R10;PPN;clock;orbital;WEP",
            "status": "TEMPLATE_ONLY_RETAIN_NONCLAIM",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "profile_id": "PFA1861_1_BZ_boundary",
            "symbol": "B_Z^A",
            "required_numeric_input": "boundary/linking flux coefficient and domain class",
            "units": "boundary_action_per_Z_component or flux-normalized equivalent",
            "required_source_path": "MISSING_BOUNDARY_SOURCE_PATH",
            "arena_maps": "R10;PPN;orbital;source-normalization",
            "status": "TEMPLATE_ONLY_RETAIN_NONCLAIM",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "profile_id": "PFA1861_2_Y5_source",
            "symbol": "J_Z[Y5]",
            "required_numeric_input": "eight-channel Y5 coefficient vector or Pi_M owner theorem",
            "units": "dimensionless Delta_mu/mu, Gdot/G, beta/gamma/source-charge projections as declared",
            "required_source_path": "MISSING_Y5_PARENT_COEFFICIENT_SOURCE",
            "arena_maps": "Newton;PPN;R10;R11;clock;orbital",
            "status": "HARD_BLOCK_RETAIN_NONCLAIM",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "profile_id": "PFA1861_3_Y6_stress",
            "symbol": "J_Z[Y6];Delta_K[Y6]",
            "required_numeric_input": "stress-response or projector-null/topological theorem",
            "units": "stress_density, acceleration, PPN, clock or q_loc projection units as declared",
            "required_source_path": "MISSING_Y6_STRESS_SOURCE",
            "arena_maps": "local_GR;PPN;clock;orbital;WEP",
            "status": "HARD_BLOCK_RETAIN_NONCLAIM",
            "valid_for_claim": as_bool_text(False),
        },
    ]


def route_selection() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "ROUTE1861_0_Y5_primary",
            "target": "parent Pi_M observed-time/Hilbert/worldtube source charge",
            "why_selected": "Y5 is the cleanest route to Newton/GR source normalization because it decides whether measured GM is parent-owned or a fitted residual",
            "status": "SELECTED_PRIMARY",
            "success_condition": "parent-owned Pi_M, observed-time generator, flux closure, same coframe, no extra mass projection, Gauss/orbital calibration and PPN source stability",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "ROUTE1861_1_Y6_parallel",
            "target": "topological/projector-null stress gate",
            "why_selected": "Bianchi/Ward conservation does not by itself remove extra stress from q_loc/PPN/source channels",
            "status": "HELD_PARALLEL",
            "success_condition": "T_extra is topological, projector-null, pure improvement, or finite source-bounded with arena maps",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "ROUTE1861_2_finite_profile",
            "target": "strict nonclaim J_Z/B_Z/Y5/Y6 profile rows",
            "why_selected": "if derivation fails, finite residuals are the honest scoring route",
            "status": "STAGED_NONCLAIM_ONLY",
            "success_condition": "numeric component values, units, source paths and arena maps; no MISSING markers",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
    ]


def qloc_impact() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "impact_id": "QI1861_0_formal_double_zero",
            "quantity": "F1/source-current linear term",
            "status": "FORMAL_CONDITIONAL_ONLY",
            "impact": "the normal form can kill first-order terms only inside the exchange-even/descended source class",
            "required_to_promote": "parent-signed evenness or quotient-descent for source, matter, boundary and readout functionals",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "QI1861_1_physical_q_loc_zero",
            "quantity": "q_loc^nu=P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})",
            "status": "BLOCKED_BY_COUPLING_LOCK",
            "impact": "odd source, boundary, Y5, Y6 or readout terms can feed the local projected residual",
            "required_to_promote": "J_Z/B_Z/Y5/Y6/readout coupling lock closes or finite profile is source-bounded below local arena thresholds",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "QI1861_2_epsilon_GK_q_loc",
            "quantity": "epsilon_GK_q_loc",
            "status": "RETAIN_NONCLAIM",
            "impact": "explicit residual remains in the local EH/source-map branch",
            "required_to_promote": "q_loc parent-zero theorem or source-backed finite q_loc/J_Z profile rows",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "QI1861_3_local_EH_GR_Newton",
            "quantity": "local EH/GR/Newton inheritance",
            "status": "NOT_REOPENED",
            "impact": "GR reduction is still blocked by source-charge ownership and extra-stress silence",
            "required_to_promote": "Y5 source owner plus Y6 stress gate plus readout/boundary closure",
            "valid_for_claim": as_bool_text(False),
        },
    ]


def claim_gate() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1861_0_exact_source_expansion",
            "claim": "local residual source expansion exists",
            "gate_pass": as_bool_text(True),
            "reason": "SFE1861_0 is a formal expansion contract",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1861_1_conditional_evenness",
            "claim": "exchange-even source functionals imply J_Z=B_Z=0",
            "gate_pass": as_bool_text(True),
            "reason": "SFE1861_1 is exact only under eta-even/quotient-descended source labels",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1861_2_current_MTS_evenness",
            "claim": "current MTS source-functional evenness is parent-signed",
            "gate_pass": as_bool_text(False),
            "reason": "observed coframe, source charge, species, boundary and readout clauses remain unsigned",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1861_3_JZ_BZ_zero",
            "claim": "all J_Z/B_Z terms vanish in the physical branch",
            "gate_pass": as_bool_text(False),
            "reason": "bulk, boundary, readout/species, Y5 and Y6 rows are not zeroed",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1861_4_Y5_source_owner",
            "claim": "measured-GM/source normalization is derived from a parent charge",
            "gate_pass": as_bool_text(False),
            "reason": "Y5SC1793_7 verdict remains open; Pi_M observed-time generator not yet derived",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1861_5_Y6_extra_stress_silence",
            "claim": "extra/projector stress is absent from local q_loc/PPN/source channels",
            "gate_pass": as_bool_text(False),
            "reason": "Y6G1793_5 remains open; Ward/Bianchi alone does not prove T_extra=0",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1861_6_q_loc_zero",
            "claim": "physical q_loc is theorem-zero on the local branch",
            "gate_pass": as_bool_text(False),
            "reason": "formal double-zero is not activated because the coupling lock is open",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1861_7_local_GR_Newton",
            "claim": "local EH/GR/Newton inheritance is reopened",
            "gate_pass": as_bool_text(False),
            "reason": "epsilon_GK_q_loc, Y5 source ownership and Y6 stress silence remain unresolved",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1861_0_no_shortcut",
            "decision": "do not promote formal response-doublet evenness to physical q_loc=0",
            "reason": "source/readout/boundary/Y5/Y6 channels can carry odd-Z leakage",
            "next_action": "keep epsilon_GK_q_loc explicit until coupling lock closes",
            "claim_allowed": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1861_1_Y5_primary",
            "decision": "select Y5 source-charge ownership as the primary derivation target",
            "reason": "this is the least ambiguous route to recovering Newton/GR source normalization without fitted-G hiding",
            "next_action": "build 1862 Pi_M observed-time generator / Hilbert charge owner checkpoint",
            "claim_allowed": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1861_2_Y6_parallel",
            "decision": "hold Y6 topological/projector-null stress gate as parallel route",
            "reason": "extra stress can spoil local GR even if Y5 closes",
            "next_action": "prepare 1862b stress gate after or alongside Pi_M owner route",
            "claim_allowed": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1861_3_profile_fallback",
            "decision": "stage finite J_Z/B_Z/Y5/Y6 rows only as nonclaim acquisition templates",
            "reason": "no parent coefficients, units or arena maps are sourced yet",
            "next_action": "only score finite profiles after missing source rows are replaced by real inputs",
            "claim_allowed": as_bool_text(False),
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1861_0_primary",
            "next_target": "1862-Y5-R2FR-parent-PiM-observed-time-generator-or-finite-Y5-pack.md",
            "script": "scripts/Y5_R2FR_parent_PiM_observed_time_generator_or_finite_Y5_pack_1862.py",
            "objective": "derive Pi_M as a parent observed-time/Hilbert/worldtube source charge map with integrability, same coframe, flux closure, no extra mass projection, Gauss/orbital calibration and PPN source stability; otherwise emit finite nonclaim Y5 rows",
            "selection_status": "SELECTED_PRIMARY",
            "success_condition": "parent-owned Pi_M source charge or source-backed finite Y5 coefficients with units and arena maps",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1861_1_parallel_Y6",
            "next_target": "1862b-Y5-R2FR-Y6-topological-projector-null-stress-gate.md",
            "script": "scripts/Y5_R2FR_Y6_topological_projector_null_stress_gate_1862b.py",
            "objective": "test whether Y6 extra/projector stress is topological, projector-null, pure improvement, or finite residual with PPN/source-stress projections",
            "selection_status": "HELD_PARALLEL",
            "success_condition": "Y6 stress-zero theorem or finite stress rows with units, source paths and arena maps",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1861_2_boundary_readout",
            "next_target": "1862c-Y5-R2FR-boundary-readout-evenness-and-linked-flux-gate.md",
            "script": "scripts/Y5_R2FR_boundary_readout_evenness_and_linked_flux_gate_1862c.py",
            "objective": "prove boundary/readout terms are exchange-even or exact no-flux terms after the source-charge route is fixed",
            "selection_status": "HELD_UNTIL_Y5_OR_Y6_PROGRESS",
            "success_condition": "B_Z/readout/species leakage is theorem-zero or bounded with source rows",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register(),
        "evenness_audit": evenness_audit(),
        "jz_bz_lock": jz_bz_lock_audit(),
        "profile_acquisition": profile_acquisition(),
        "route_selection": route_selection(),
        "qloc_impact": qloc_impact(),
        "claim_gate": claim_gate(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
    }


def copy_outputs(include_validation: bool = False) -> None:
    keys = list(OUTPUTS)
    if not include_validation:
        keys = [key for key in keys if key != "validation"]
    for key in keys:
        src = OUTPUTS[key]
        if not src.exists():
            continue
        targets = [
            MICROSCOPE_RESIDUALS / src.name,
            QUARANTINE / src.name,
            RAB_QUEUE / f"JR1861_{src.name}",
        ]
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, target)


def check_sources(rows: list[dict[str, Any]]) -> tuple[bool, str]:
    failures: list[str] = []
    for row in rows:
        path = Path(str(row["source_path"]))
        if not path.exists():
            failures.append(f"{row['source_id']} missing path {path}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        needle = str(row["required_needle"])
        if needle not in text:
            failures.append(f"{row['source_id']} missing needle {needle}")
    return not failures, "; ".join(failures) if failures else "all source paths and needles found"


def check_csv_outputs() -> tuple[bool, str]:
    failures: list[str] = []
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        try:
            rows = read_csv(path)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{path.name}: {exc}")
            continue
        if not rows:
            failures.append(f"{path.name}: no rows")
    return not failures, "; ".join(failures) if failures else "all generated CSV outputs parse and have rows"


def check_branch_copies() -> tuple[bool, str]:
    missing: list[str] = []
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        targets = [
            MICROSCOPE_RESIDUALS / path.name,
            QUARANTINE / path.name,
            RAB_QUEUE / f"JR1861_{path.name}",
        ]
        for target in targets:
            if not target.exists():
                missing.append(str(target))
    return not missing, "missing copies: " + "; ".join(missing) if missing else "branch/quarantine/queue copies exist"


def has_true_valid_for_claim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            if str(row.get("valid_for_claim", "False")).lower() == "true":
                return True
    return False


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = []
    ok, detail = check_sources(rows_map["source_register"])
    checks.append(("VAL1861_0_sources_found", ok, detail))
    ok, detail = check_csv_outputs()
    checks.append(("VAL1861_1_csv_outputs_parse", ok, detail))
    checks.append(
        (
            "VAL1861_2_conditional_evenness_recorded",
            any(row["audit_id"] == "SFE1861_1_exchange_evenness_condition" and row["status"] == "EXACT_CONDITIONAL_EVENNESS_THEOREM" for row in rows_map["evenness_audit"]),
            "conditional theorem row exists",
        )
    )
    checks.append(
        (
            "VAL1861_3_current_evenness_not_activated",
            any(row["audit_id"] == "SFE1861_6_verdict" and row["status"] == "EVENNESS_THEOREM_NOT_ACTIVATED" for row in rows_map["evenness_audit"]),
            "current source-functional evenness remains blocked",
        )
    )
    checks.append(
        (
            "VAL1861_4_coupling_lock_rejected",
            any(row["lock_id"] == "JBC1861_5_acceptance" and row["current_status"] == "REJECT_COUPLING_LOCK_NOT_CLOSED" for row in rows_map["jz_bz_lock"]),
            "J_Z/B_Z coupling lock acceptance rejects current branch",
        )
    )
    hard_blocks = {
        row["current_status"]
        for row in rows_map["jz_bz_lock"]
        if row["lock_id"] in {"JBC1861_3_Y5_source_normalization", "JBC1861_4_Y6_extra_stress"}
    }
    checks.append(
        (
            "VAL1861_5_y5_y6_hard_blocks_present",
            hard_blocks == {"HARD_BLOCK_NOT_PARITY_ZEROED", "HARD_BLOCK_CONSERVATION_NOT_ZERO"},
            "Y5 and Y6 hard blockers are explicitly retained",
        )
    )
    checks.append(
        (
            "VAL1861_6_profile_rows_nonclaim",
            all(row["valid_for_claim"] == "False" and "NONCLAIM" in row["status"] for row in rows_map["profile_acquisition"]),
            "finite profile/acquisition rows are template-only nonclaim rows",
        )
    )
    blocked_claims = {
        row["claim_id"]: row
        for row in rows_map["claim_gate"]
        if row["claim_id"] in {"CG1861_6_q_loc_zero", "CG1861_7_local_GR_Newton"}
    }
    checks.append(
        (
            "VAL1861_7_qloc_local_GR_blocked",
            all(row["gate_pass"] == "False" and row["claim_allowed"] == "False" for row in blocked_claims.values()) and len(blocked_claims) == 2,
            "q_loc and local EH/GR/Newton claims remain blocked",
        )
    )
    checks.append(
        (
            "VAL1861_8_no_claim_rows_promoted",
            not has_true_valid_for_claim(rows_map),
            "no generated 1861 row has valid_for_claim=True",
        )
    )
    checks.append(
        (
            "VAL1861_9_next_target_selected",
            any(row["route_id"] == "NEXT1861_0_primary" and row["selection_status"] == "SELECTED_PRIMARY" for row in rows_map["next_target"]),
            "1862 Pi_M/source-charge owner target selected",
        )
    )
    ok, detail = check_branch_copies()
    checks.append(("VAL1861_10_branch_copies", ok, detail))
    pycache_path = ROOT / "scripts" / "__pycache__"
    checks.append(("VAL1861_11_pycache_absent", not pycache_path.exists(), "scripts __pycache__ absent"))
    formalization_outputs: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in [
            "*1861*",
            "P8_Y5_PARENT_QLOC_1861*",
            "P8_Y5_BRR545_1861*",
            "Y5_R2FR_source_functional_evenness_JZ_BZ_coupling_lock_or_profile_acquisition_1861.py",
        ]:
            formalization_outputs.extend(FORMALIZATION.rglob(pattern))
    formalization_detail = (
        "found generated outputs: " + "; ".join(str(path) for path in formalization_outputs)
        if formalization_outputs
        else "no generated 1861 outputs found under formalization-workbench"
    )
    checks.append(("VAL1861_12_formalization_untouched", not formalization_outputs, formalization_detail))
    overall = all(result for _, result, _ in checks)
    validation_rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    validation_rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1861_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1861 coupling-lock checkpoint passes private validation" if overall else "one or more 1861 checks failed",
        }
    )
    return validation_rows


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    return "\n".join(
        [
            "# 1861 - Y5/R2FR Source-Functional Evenness, J_Z/B_Z Coupling Lock, Or Profile Acquisition",
            "",
            "**Current verdict:** the coupling hunch is now sharp: the exact conditional evenness theorem exists, but current MTS has not activated it as a physical source theorem. The formal response-doublet/double-zero route stays alive only inside an exchange-even or quotient-descended source class. The live branch still has open bulk `J_Z`, boundary `B_Z`, readout/species, Y5 source-normalization and Y6 extra-stress channels. Therefore `epsilon_GK_q_loc` remains a nonclaim residual and local EH/GR/Newton inheritance is not reopened.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_kind", "source_path", "required_needle", "extraction_status", "valid_for_claim"]),
            "",
            "## Source-Functional Evenness Audit",
            markdown_table(rows_map["evenness_audit"], ["audit_id", "clause", "mathematical_form", "status", "blocker", "valid_for_claim"]),
            "",
            "## J_Z/B_Z Coupling Lock Audit",
            markdown_table(rows_map["jz_bz_lock"], ["lock_id", "component", "symbol", "required_evidence", "current_status", "next_action", "valid_for_claim"]),
            "",
            "## Strict Nonclaim Profile Acquisition",
            markdown_table(rows_map["profile_acquisition"], ["profile_id", "symbol", "required_numeric_input", "units", "required_source_path", "arena_maps", "status", "valid_for_claim"]),
            "",
            "## Y5/Y6 Route Selection",
            markdown_table(rows_map["route_selection"], ["route_id", "target", "why_selected", "status", "success_condition", "claim_allowed"]),
            "",
            "## q_loc Impact",
            markdown_table(rows_map["qloc_impact"], ["impact_id", "quantity", "status", "impact", "required_to_promote", "valid_for_claim"]),
            "",
            "## Claim Gate",
            markdown_table(rows_map["claim_gate"], ["claim_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "",
            "## Decision Ledger",
            markdown_table(rows_map["decision_ledger"], ["decision_id", "decision", "reason", "next_action", "claim_allowed"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status", "success_condition", "claim_allowed"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "",
            "- The good news: this is not a vague failure anymore. The exact theorem we would need is named cleanly: source, matter, boundary and readout functionals must be exchange-even or quotient-descended in the residual `Z`.",
            "- The hard news: the live theory does not yet prove that theorem for the physical source side. Y5 and Y6 are the real locks, not cosmetic loose ends.",
            "- The best route is now surgical: derive `Pi_M` as the parent observed-time/Hilbert/worldtube source charge, then keep Y6 as the parallel stress-silence gate.",
            "- No public/local-GR claim is produced here; this is a private discipline checkpoint that prevents us smuggling in the result we want.",
            "",
        ]
    )


def main() -> None:
    for directory in [RESIDUALS, MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
        directory.mkdir(parents=True, exist_ok=True)
    rows_map = build_rows()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs(include_validation=False)
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    copy_outputs(include_validation=True)
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1861 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
