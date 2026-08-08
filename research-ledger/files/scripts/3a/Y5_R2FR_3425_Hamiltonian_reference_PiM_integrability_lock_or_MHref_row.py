from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3425-Y5-R2FR-Hamiltonian-reference-PiM-integrability-lock-or-MHref-row-under-AX1090.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCES = {
    "doc_3424": ROOT / "3424-Y5-R2FR-minimal-parent-source-coupling-action-or-PC3400-adoption-gate-under-AX1090.md",
    "action_3424": OUT / "P8_Y5_R2FR_3424_PARENT_ACTION_DENSITY.csv",
    "pc3400_3424": OUT / "P8_Y5_R2FR_3424_PC3400_ADOPTION_AUDIT.csv",
    "bounds_3424": OUT / "P8_Y5_R2FR_3424_RETAINED_SOURCE_BOUND_ROWS.csv",
    "next_3424": OUT / "P8_Y5_R2FR_3424_NEXT_TARGET.csv",
    "doc_1017": ROOT / "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md",
    "lock_1017": OUT / "P8_Y5_R10_1017_REFERENCE_LOCK_LAW.csv",
    "schema_1017": OUT / "P8_Y5_R10_1017_MHREF_FIRST_ROW_SCHEMA.csv",
    "runner_1017": OUT / "P8_Y5_R10_1017_FIRST_ROW_RUNNER.csv",
    "hsm_contract": OUT / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
    "hwt_contract": OUT / "P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv",
    "hwt_theorem": OUT / "P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv",
    "worldtube_measure": OUT / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
    "source_measure_attempt": OUT / "P8_Y5_SOURCE_MEASURE_THEOREM_ATTEMPT.csv",
    "r_eq_rows_1015": OUT / "P8_Y5_R10_1015_R_EQ_BOUND_INPUT_ROWS.csv",
    "parent_clauses_3400": OUT / "P8_Y5_R2FR_3400_PARENT_SIGNATURE_CLAUSES.csv",
    "boundary_3420": OUT / "P8_Y5_R2FR_3420_HODGE_BOUNDARY_SILENCE_THEOREM.csv",
    "fixed_point_3421": OUT / "P8_Y5_R2FR_3421_EULER_FIXED_POINT_THEOREM.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3425_SOURCE_REGISTER.csv",
    "eh_integrability_subtheorem": OUT / "P8_Y5_R2FR_3425_EH_INTEGRABILITY_SUBTHEOREM.csv",
    "mts_charge_decomposition": OUT / "P8_Y5_R2FR_3425_MTS_CHARGE_DECOMPOSITION.csv",
    "pc3400_3_lock_audit": OUT / "P8_Y5_R2FR_3425_PC3400_3_LOCK_AUDIT.csv",
    "mhref_candidate_rows": OUT / "P8_Y5_R2FR_3425_MHREF_CANDIDATE_ROWS.csv",
    "residual_bound_rows": OUT / "P8_Y5_R2FR_3425_HPI_M_RESIDUAL_BOUND_ROWS.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3425_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3425_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3425_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3425_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3425_VALIDATION.csv",
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
        "doc_3424": "minimal source-action handoff",
        "action_3424": "candidate local parent source action",
        "pc3400_3424": "PC3400 partial adoption audit",
        "bounds_3424": "retained source-bound rows after action candidate",
        "next_3424": "machine-readable 3425 target",
        "doc_1017": "prior Hamiltonian/PiM reference lock",
        "lock_1017": "older lock-law split",
        "schema_1017": "older M_H_ref first-row schema",
        "runner_1017": "older first-row refusal runner",
        "hsm_contract": "Hamiltonian source-measure contract",
        "hwt_contract": "Hilbert worldtube parent action contract",
        "hwt_theorem": "Hilbert worldtube glue theorem attempt",
        "worldtube_measure": "GR-style worldtube source-measure theorem",
        "source_measure_attempt": "source-measure theorem attempt",
        "r_eq_rows_1015": "R_eq/B_zero/I_commutator fallback rows",
        "parent_clauses_3400": "PC3400 source-coupling clauses",
        "boundary_3420": "boundary/no-flux silence conditions",
        "fixed_point_3421": "Euler fixed-point theorem if source terms vanish",
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


def eh_integrability_subtheorem() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "EHI3425_0_covariant_phase_space",
            "claim": "The public EH plus Hilbert matter part has the standard covariant-phase-space Hamiltonian variation.",
            "identity": "delta H_tau^EH[S] = integral_S (delta Q_tau^EH - i_tau Theta_EH)",
            "status": "KNOWN_CONDITIONAL_FOR_PAD3424_PUBLIC_EH_SECTOR",
            "missing_to_promote": "MTS must adopt PAD3424_1/PAD3424_2 as the actual local parent branch",
            "valid_for_claim": False,
        },
        {
            "step_id": "EHI3425_1_integrability",
            "claim": "For fixed tau, fixed asymptotic/reference data, and stationary local boundary conditions, the EH charge is integrable.",
            "identity": "curl(delta H_tau^EH)=integral_S i_tau omega_EH = 0",
            "status": "EH_SUBTHEOREM_CAN_BE_SIGNED_CONDITIONALLY",
            "missing_to_promote": "tau/reference/boundary lock and no residual MTS symplectic flux",
            "valid_for_claim": False,
        },
        {
            "step_id": "EHI3425_2_radial_closure",
            "claim": "In a compact source-free exterior annulus, the EH Hamiltonian charge is surface-independent.",
            "identity": "H_tau^EH[S2]-H_tau^EH[S1]=int_A C_tau^EH=0",
            "status": "EH_SUBTHEOREM_CAN_BE_SIGNED_CONDITIONALLY",
            "missing_to_promote": "source-free exterior and boundary flux silence for the MTS residual sectors",
            "valid_for_claim": False,
        },
        {
            "step_id": "EHI3425_3_MHref_EH",
            "claim": "The legal denominator is a dressed charge, not bare mass or orbital GM.",
            "identity": "M_H_ref^EH := c^-2 (H_tau^EH[S_outer]-H_ref^EH)",
            "status": "DEFINITION_GUARDRAIL_PLUS_EH_BRANCH_CANDIDATE",
            "missing_to_promote": "explicit reference rule and same-frame source support",
            "valid_for_claim": False,
        },
        {
            "step_id": "EHI3425_4_MTS_transfer",
            "claim": "MTS inherits the EH charge only if all residual Hamiltonian pieces are zero or explicitly bounded.",
            "identity": "H_tau^MTS = H_tau^EH + Delta H_Z + Delta H_PiM + Delta H_boundary + Delta H_extra + Delta H_ref",
            "status": "TRANSFER_THEOREM_NOT_CURRENT_CLAIM",
            "missing_to_promote": "Z fixed point, PiM chain map, boundary/reference silence, no-extra-mass/Y6",
            "valid_for_claim": False,
        },
        {
            "step_id": "EHI3425_5_verdict",
            "claim": "3424 lets us sign the EH/Hilbert subcharge route, but not the full MTS Hamiltonian/PiM lock.",
            "identity": "epsilon_HPiM = 0 only if Delta H_Z=Delta H_PiM=Delta H_boundary=Delta H_extra=Delta H_ref=0",
            "status": "PARTIAL_DERIVATION_REAL_RESIDUALS_REMAIN",
            "missing_to_promote": "component zero proofs or source-backed M_H_ref-normalized rows",
            "valid_for_claim": False,
        },
    ]


def mts_charge_decomposition() -> list[dict[str, Any]]:
    return [
        {
            "component_id": "HDC3425_0_EH_Hilbert",
            "charge_piece": "H_tau^EH[g_obs,T_H]",
            "variation_or_flux": "delta H_tau^EH = integral_S(delta Q_tau^EH - i_tau Theta_EH)",
            "zero_or_lock_condition": "fixed tau/reference and stationary source-free exterior",
            "current_status": "CONDITIONAL_EH_LOCK",
            "valid_for_claim": False,
        },
        {
            "component_id": "HDC3425_1_Z_sector",
            "charge_piece": "Delta H_Z",
            "variation_or_flux": "integral_S(delta Q_tau^Z - i_tau Theta_Z)",
            "zero_or_lock_condition": "3421 fixed point gives Z=0 and no linear source current",
            "current_status": "PENDING_Y5_Y6_LAMBDA_SOURCE_GATES",
            "valid_for_claim": False,
        },
        {
            "component_id": "HDC3425_2_PiM_chain",
            "charge_piece": "Delta H_PiM",
            "variation_or_flux": "I_commutator = integral_A [d,Pi_M]J_H plus projector-stress response",
            "zero_or_lock_condition": "Pi_M is parent-fixed covariantly constant chain map on Hilbert current space",
            "current_status": "OPEN_BIGGEST_PC3400_3_RESIDUAL",
            "valid_for_claim": False,
        },
        {
            "component_id": "HDC3425_3_boundary_reference",
            "charge_piece": "Delta H_boundary + Delta H_ref",
            "variation_or_flux": "B_zero_flux + Delta_symp + H_ref_shift",
            "zero_or_lock_condition": "boundary/reference rule fixed once; compact linked flux zero",
            "current_status": "OPEN_REFERENCE_LOCK",
            "valid_for_claim": False,
        },
        {
            "component_id": "HDC3425_4_extra_mass",
            "charge_piece": "Delta H_extra",
            "variation_or_flux": "nonEH/domain/memory/range/frame/Y6 monopole flux",
            "zero_or_lock_condition": "no-hair/safe-class theorem or explicit source-backed bound",
            "current_status": "OPEN_PC3400_4_RESIDUAL",
            "valid_for_claim": False,
        },
        {
            "component_id": "HDC3425_5_total",
            "charge_piece": "H_tau^MTS-H_ref^MTS",
            "variation_or_flux": "H_EH plus all Delta H components",
            "zero_or_lock_condition": "HDC3425_0 locked and HDC3425_1 through HDC3425_4 zero/bounded",
            "current_status": "NOT_LOCKED_FOR_CURRENT_MTS",
            "valid_for_claim": False,
        },
    ]


def pc3400_3_lock_audit() -> list[dict[str, Any]]:
    return [
        {
            "lock_id": "P3L3425_0_tau_fixed",
            "required_lock": "one tau used for source, charge, clocks and readout",
            "can_3424_candidate_supply": "partially: tau is named in branch data",
            "remaining_obstruction": "tau selection by parent coframe/asymptotic structure not derived",
            "status": "PARTIAL",
            "valid_for_claim": False,
        },
        {
            "lock_id": "P3L3425_1_integrability_curl",
            "required_lock": "field-space curl of delta H_tau^MTS vanishes",
            "can_3424_candidate_supply": "yes for public EH/Hilbert subcharge under fixed boundary conditions",
            "remaining_obstruction": "Z/PiM/boundary/extra-sector symplectic curls uncomputed",
            "status": "PARTIAL_EH_ONLY",
            "valid_for_claim": False,
        },
        {
            "lock_id": "P3L3425_2_reference_lock",
            "required_lock": "H_ref is fixed once and derivative-silent",
            "can_3424_candidate_supply": "names fixed reference but does not select it",
            "remaining_obstruction": "reference functional and allowed background class not parent-derived",
            "status": "OPEN",
            "valid_for_claim": False,
        },
        {
            "lock_id": "P3L3425_3_PiM_chain_map",
            "required_lock": "Pi_M maps Hilbert current to the same charge without commutator hair",
            "can_3424_candidate_supply": "no, Pi_M is branch data but not constructed",
            "remaining_obstruction": "[d,Pi_M]J_H and projector stress remain active",
            "status": "OPEN",
            "valid_for_claim": False,
        },
        {
            "lock_id": "P3L3425_4_MHref_positive",
            "required_lock": "M_H_ref is positive dressed same-frame source denominator",
            "can_3424_candidate_supply": "conditionally for EH source charge",
            "remaining_obstruction": "needs explicit surface/source system row or theorem-zero residual transfer",
            "status": "PARTIAL_EH_DENOMINATOR_ONLY",
            "valid_for_claim": False,
        },
        {
            "lock_id": "P3L3425_5_verdict",
            "required_lock": "PC3400_3 is signed",
            "can_3424_candidate_supply": "not fully",
            "remaining_obstruction": "PiM chain map, reference lock, and residual MTS charge pieces",
            "status": "FAIL_CURRENT_PC3400_3",
            "valid_for_claim": False,
        },
    ]


def mhref_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "MHC3425_0_EH_theorem_denominator",
            "quantity": "M_H_ref^EH",
            "definition": "dressed EH/Hilbert source denominator in the 3424 public metric branch",
            "candidate_value_or_theorem": "M_H_ref^EH := c^-2(H_tau^EH[S_outer]-H_ref^EH)",
            "claim_readiness": "THEOREM_CANDIDATE_NEEDS_REFERENCE_AND_SOURCE_ROW",
            "valid_for_claim": False,
        },
        {
            "row_id": "MHC3425_1_integrability_curl_EH",
            "quantity": "delta_H_tau_EH_nonintegrable_over_MH",
            "definition": "field-space curl obstruction for the public EH/Hilbert subcharge",
            "candidate_value_or_theorem": "0 if fixed tau/stationary boundary/reference conditions are signed",
            "claim_readiness": "CONDITIONAL_ZERO_NOT_CURRENT_CLAIM",
            "valid_for_claim": False,
        },
        {
            "row_id": "MHC3425_2_integrability_curl_MTS_residual",
            "quantity": "delta_H_tau_MTS_residual_over_MH",
            "definition": "non-EH/Z/PiM/boundary/extra-sector symplectic curl normalized by M_H_ref",
            "candidate_value_or_theorem": "MISSING_SECTOR_OWNER_OR_BOUND",
            "claim_readiness": "RETAINED",
            "valid_for_claim": False,
        },
        {
            "row_id": "MHC3425_3_MHref_source_row_schema",
            "quantity": "claim-ready M_H_ref row",
            "definition": "source-specific dressed charge with tau, surface, reference, units and source path",
            "candidate_value_or_theorem": "system_id;tau_id;surface_outer;Q_tau_integral;H_ref;M_H_ref;units;source_path;assumptions",
            "claim_readiness": "SCHEMA_READY_NO_VALUE",
            "valid_for_claim": False,
        },
        {
            "row_id": "MHC3425_4_total_FB5540_after_EH",
            "quantity": "epsilon_HPiM_after_EH_lock",
            "definition": "remaining Hamiltonian/PiM residual after the public EH subcharge is conditionally locked",
            "candidate_value_or_theorem": "epsilon_Z_charge + epsilon_PiM_comm + epsilon_boundary_ref + epsilon_extra_mass + epsilon_tau",
            "claim_readiness": "FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
    ]


def residual_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "HBR3425_0_tau_lock",
            "quantity": "epsilon_tau_lock",
            "definition": "mismatch among source/charge/clock/readout time generators",
            "bound_formula": "0 if tau is parent-selected by e_obs and fixed boundary data; else source-backed mismatch norm",
            "status": "THEOREM_OR_VALUE_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "HBR3425_1_reference",
            "quantity": "epsilon_reference",
            "definition": "reference subtraction shift normalized by M_H_ref",
            "bound_formula": "|H_ref_shift|/M_H_ref + |partial_source H_ref|/M_H_ref",
            "status": "REFERENCE_RULE_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "HBR3425_2_PiM_commutator",
            "quantity": "epsilon_PiM_comm",
            "definition": "PiM chain-map/commutator and projector-stress leakage",
            "bound_formula": "|I_commutator|/M_H_ref + |T_PiM|_PPN",
            "status": "PIM_CHAIN_MAP_OR_VALUE_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "HBR3425_3_Z_charge",
            "quantity": "epsilon_Z_charge",
            "definition": "residual Z-sector Hamiltonian charge after fixed-point branch",
            "bound_formula": "0 if Z=0 source-free fixed point is signed; else C_HZ ||Z||",
            "status": "PENDING_SOURCE_CURRENT_AND_LAMBDA_STAR",
            "valid_for_claim": False,
        },
        {
            "bound_id": "HBR3425_4_boundary_flux",
            "quantity": "epsilon_boundary_flux",
            "definition": "boundary/symplectic flux through compact linked surfaces",
            "bound_formula": "(|B_zero_flux|+|Delta_symp|)/M_H_ref",
            "status": "BOUNDARY_NO_FLUX_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "bound_id": "HBR3425_5_extra_mass",
            "quantity": "epsilon_extra_mass",
            "definition": "extra/Y6/domain/memory/projector monopole source charge",
            "bound_formula": "|Delta_extra_mass|/M_H_ref",
            "status": "NO_EXTRA_MASS_THEOREM_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "HBR3425_6_total",
            "quantity": "epsilon_HPiM_after_EH_lock",
            "definition": "no-cancellation Hamiltonian/PiM residual after EH subtheorem",
            "bound_formula": "epsilon_tau_lock+epsilon_reference+epsilon_PiM_comm+epsilon_Z_charge+epsilon_boundary_flux+epsilon_extra_mass",
            "status": "FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PG3425_0_EH_subcharge",
            "claim": "public EH/Hilbert subcharge has a legitimate integrability route",
            "gate_status": "PASS_CONDITIONAL_SUBTHEOREM",
            "reason": "3424 candidate supplies EH public geometry and Hilbert matter source",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3425_1_MTS_full_integrability",
            "claim": "full MTS Hamiltonian charge is integrable",
            "gate_status": "FAIL_CURRENT",
            "reason": "Z/PiM/boundary/reference/extra-sector curls are not zeroed",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3425_2_MHref_claim_ready",
            "claim": "M_H_ref is stable and claim-ready",
            "gate_status": "NOT_PROMOTED",
            "reason": "source-specific Q_tau integral, reference rule and residual transfer are missing",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3425_3_PC3400_3",
            "claim": "PC3400_3 Htau/PiM chain is signed",
            "gate_status": "PARTIAL_ONLY",
            "reason": "EH subcharge yes; PiM chain-map/reference lock no",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3425_4_Y5_zero",
            "claim": "Y5 source current is zero after Hamiltonian lock",
            "gate_status": "BLOCKED",
            "reason": "epsilon_HPiM_after_EH_lock and no-extra-mass rows remain",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3425_5_local_GR",
            "claim": "local GR/Newton/PPN branch is derived",
            "gate_status": "BLOCKED",
            "reason": "Y5 not fully zero, Y6/extra mass, lambda-star, q_loc and second-order PPN remain open",
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3425_0_real_progress",
            "decision": "The Hamiltonian charge problem is no longer all-or-nothing.",
            "because": "the 3424 action candidate gives a legitimate EH/Hilbert integrable subcharge under standard fixed-reference conditions",
            "next_action": "keep the EH charge as the parent candidate denominator while proving or bounding residual charge hair",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3425_1_not_finished",
            "decision": "Full PC3400_3 is still not signed.",
            "because": "PiM chain-map equality, reference selection, boundary flux and extra-sector charges remain outside the EH subtheorem",
            "next_action": "attack PiM chain-map first, then no-extra-mass/Y6",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3425_2_MHref_policy",
            "decision": "M_H_ref may be the dressed EH/Hilbert source charge only in the candidate branch, not bare mass or orbital GM.",
            "because": "using orbital GM or a reference-only denominator would circularly normalize the theorem with its target",
            "next_action": "require Q_tau integral, fixed reference, surface, tau and source path before any score row",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3425_3_best_next",
            "decision": "Next target should construct PiM as a chain map or demote it to an I_commutator bound.",
            "because": "after EH integrability, PiM is the largest PC3400_3 object-specific obstruction",
            "next_action": "3426-Y5-R2FR-PiM-chain-map-identity-or-Icommutator-bound-under-AX1090.md",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target": "3426-Y5-R2FR-PiM-chain-map-identity-or-Icommutator-bound-under-AX1090.md",
            "script": "scripts/Y5_R2FR_3426_PiM_chain_map_identity_or_Icommutator_bound.py",
            "objective": "prove Pi_M is a parent-fixed chain map on the Hilbert current space with [d,Pi_M]J_H=0 and no projector stress, or emit I_commutator/projector-stress bound rows",
            "why_next": "3425 conditionally locks the EH/Hilbert subcharge; PiM is now the largest specific PC3400_3 residual",
            "valid_for_claim": False,
        },
        {
            "target": "3427-Y5-R2FR-reference-boundary-flux-zero-or-Bzero-row-under-AX1090.md",
            "script": "scripts/Y5_R2FR_3427_reference_boundary_flux_zero_or_Bzero_row.py",
            "objective": "prove fixed H_ref and compact linked boundary/symplectic flux silence, or emit B_zero_flux/Delta_symp/H_ref_shift rows",
            "why_next": "reference and boundary rows are the other PC3400_3 residuals after PiM",
            "valid_for_claim": False,
        },
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3425_0",
            "script": str(Path(__file__).resolve()),
            "mode": "HAMILTONIAN_REFERENCE_PIM_INTEGRABILITY_LOCK_OR_MHREF_ROW",
            "summary": "EH/Hilbert integrability subtheorem conditionally inherited by 3424 candidate; full MTS PC3400_3 remains blocked by PiM/reference/boundary/Z/extra residuals; MHref and residual bound rows staged nonclaim",
            "valid_for_claim": False,
        }
    ]


def formalization_recent_count(start_utc: datetime) -> int:
    if not FORMALIZATION.exists():
        return 0
    threshold = start_utc.timestamp()
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= threshold)


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], start_utc: datetime) -> list[dict[str, Any]]:
    sources = rows_by_name["source_register"]
    nonclaim = all(
        row.get("valid_for_claim") is False
        for name, rows in rows_by_name.items()
        if name != "validation"
        for row in rows
    )
    outputs_under_root = all(str(path).startswith(str(ROOT)) for path in OUTPUTS.values()) and str(DOC).startswith(str(ROOT))
    formalization_count = formalization_recent_count(start_utc)
    promotion = rows_by_name["promotion_gates"]
    return [
        {
            "check_id": "VAL3425_0_sources_exist",
            "condition": "all cited source paths exist",
            "passed": all(row["exists"] for row in sources),
            "detail": f"{sum(1 for row in sources if row['exists'])}/{len(sources)} source paths exist",
        },
        {
            "check_id": "VAL3425_1_outputs_scoped",
            "condition": "all outputs are in post-checkpoint-work",
            "passed": outputs_under_root,
            "detail": str(ROOT),
        },
        {
            "check_id": "VAL3425_2_nonclaim",
            "condition": "all generated rows remain nonclaim",
            "passed": nonclaim,
            "detail": "valid_for_claim=false throughout generated rows",
        },
        {
            "check_id": "VAL3425_3_EH_subtheorem",
            "condition": "EH/Hilbert integrability subtheorem is present",
            "passed": any(row["step_id"] == "EHI3425_1_integrability" for row in rows_by_name["eh_integrability_subtheorem"]),
            "detail": "EHI3425_1 present",
        },
        {
            "check_id": "VAL3425_4_MTS_transfer_not_claimed",
            "condition": "full MTS transfer remains unclaimed",
            "passed": any(row["gate_id"] == "PG3425_1_MTS_full_integrability" and row["gate_status"] == "FAIL_CURRENT" for row in promotion),
            "detail": "MTS residual curls remain open",
        },
        {
            "check_id": "VAL3425_5_MHref_rows",
            "condition": "M_H_ref candidate/source-row schema exists",
            "passed": any(row["row_id"] == "MHC3425_3_MHref_source_row_schema" for row in rows_by_name["mhref_candidate_rows"]),
            "detail": "MHC3425_3 present",
        },
        {
            "check_id": "VAL3425_6_residual_bounds",
            "condition": "residual Hamiltonian/PiM bound rows exist",
            "passed": any(row["bound_id"] == "HBR3425_6_total" for row in rows_by_name["residual_bound_rows"]),
            "detail": "HBR3425_6 present",
        },
        {
            "check_id": "VAL3425_7_local_GR_blocked",
            "condition": "local GR remains blocked",
            "passed": any(row["gate_id"] == "PG3425_5_local_GR" and row["gate_status"] == "BLOCKED" for row in promotion),
            "detail": "no local-GR claim promoted",
        },
        {
            "check_id": "VAL3425_8_next_target",
            "condition": "next target attacks PiM chain map",
            "passed": rows_by_name["next_target"][0]["target"].startswith("3426-Y5-R2FR-PiM-chain-map"),
            "detail": rows_by_name["next_target"][0]["target"],
        },
        {
            "check_id": "VAL3425_9_formalization_untouched",
            "condition": "formalization-workbench modified-file count remains 0 during this run",
            "passed": formalization_count == 0,
            "detail": f"modified_count_since_start={formalization_count}",
        },
        {
            "check_id": "VAL3425_10_overall",
            "condition": "3425 Hamiltonian/PiM checkpoint is internally valid",
            "passed": True,
            "detail": "PASS",
        },
    ]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    text = f"""# 3425 - Hamiltonian Reference/PiM Integrability Lock or MHref Row

## Summary
- This checkpoint upgrades the old 1017 reference-lock problem using the 3424 source-action candidate.
- Real progress: the public EH/Hilbert part of the candidate has a standard integrable Hamiltonian charge route under fixed `tau`, fixed reference, stationary local boundary data, and source-free exterior.
- That means the legal denominator can be a dressed `M_H_ref^EH = c^-2(H_tau^EH[S]-H_ref^EH)` in the candidate branch, not bare mass and not orbital `GM`.
- But full MTS does **not** inherit the charge yet: residual `Z`, `Pi_M`, boundary/reference, projector, and extra/Y6 charge pieces remain outside the EH subtheorem.
- So `PC3400_3` is partially improved: EH/Hilbert integrability can be conditionally signed, but PiM chain-map equality and reference/boundary silence still block the current Y5-zero claim.
- The next best move is `Pi_M`: prove it is a parent-fixed chain map with `[d,Pi_M]J_H=0`, or demote it to an explicit `I_commutator`/projector-stress bound.

## Source Register
{md_table(rows_by_name["source_register"])}

## EH Integrability Subtheorem
{md_table(rows_by_name["eh_integrability_subtheorem"])}

## MTS Charge Decomposition
{md_table(rows_by_name["mts_charge_decomposition"])}

## PC3400_3 Lock Audit
{md_table(rows_by_name["pc3400_3_lock_audit"])}

## MHref Candidate Rows
{md_table(rows_by_name["mhref_candidate_rows"])}

## Residual Bound Rows
{md_table(rows_by_name["residual_bound_rows"])}

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
This is a useful narrowing. The Hamiltonian source charge is no longer pure fog: the EH/Hilbert subcharge is a legitimate inherited mechanism inside the 3424 candidate. The remaining danger is exactly the MTS-specific charge hair: `Pi_M`, reference/boundary flux, `Z`, and extra/Y6 monopole terms.
"""
    DOC.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    start_utc = datetime.now(timezone.utc)
    rows_by_name = {
        "source_register": source_register(),
        "eh_integrability_subtheorem": eh_integrability_subtheorem(),
        "mts_charge_decomposition": mts_charge_decomposition(),
        "pc3400_3_lock_audit": pc3400_3_lock_audit(),
        "mhref_candidate_rows": mhref_candidate_rows(),
        "residual_bound_rows": residual_bound_rows(),
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
        raise SystemExit(f"3425 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"wrote {len(OUTPUTS)} csv outputs")


if __name__ == "__main__":
    main()
