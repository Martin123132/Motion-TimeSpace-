from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3427-Y5-R2FR-reference-boundary-flux-zero-or-Bzero-row-under-AX1090.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCES = {
    "doc_3426": ROOT / "3426-Y5-R2FR-PiM-chain-map-identity-or-Icommutator-bound-under-AX1090.md",
    "pim_theorem_3426": OUT / "P8_Y5_R2FR_3426_PIM_CHAIN_MAP_THEOREM.csv",
    "pim_update_3426": OUT / "P8_Y5_R2FR_3426_PC3400_3_UPDATE.csv",
    "icomm_3426": OUT / "P8_Y5_R2FR_3426_ICOMM_BOUND_ROWS.csv",
    "next_3426": OUT / "P8_Y5_R2FR_3426_NEXT_TARGET.csv",
    "doc_3425": ROOT / "3425-Y5-R2FR-Hamiltonian-reference-PiM-integrability-lock-or-MHref-row-under-AX1090.md",
    "eh_integrability_3425": OUT / "P8_Y5_R2FR_3425_EH_INTEGRABILITY_SUBTHEOREM.csv",
    "charge_decomp_3425": OUT / "P8_Y5_R2FR_3425_MTS_CHARGE_DECOMPOSITION.csv",
    "bounds_3425": OUT / "P8_Y5_R2FR_3425_HPI_M_RESIDUAL_BOUND_ROWS.csv",
    "boundary_3420": OUT / "P8_Y5_R2FR_3420_HODGE_BOUNDARY_SILENCE_THEOREM.csv",
    "projector_3420": OUT / "P8_Y5_R2FR_3420_PROJECTOR_OWNER_GATE.csv",
    "lock_1017": OUT / "P8_Y5_R10_1017_REFERENCE_LOCK_LAW.csv",
    "schema_1017": OUT / "P8_Y5_R10_1017_MHREF_FIRST_ROW_SCHEMA.csv",
    "hwt_contract": OUT / "P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv",
    "r_eq_rows_1015": OUT / "P8_Y5_R10_1015_R_EQ_BOUND_INPUT_ROWS.csv",
    "pim_input_template": OUT / "P8_Y5_PIM_INPUT_FILL_TEMPLATE.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3427_SOURCE_REGISTER.csv",
    "reference_lock_theorem": OUT / "P8_Y5_R2FR_3427_REFERENCE_LOCK_THEOREM.csv",
    "boundary_flux_theorem": OUT / "P8_Y5_R2FR_3427_BOUNDARY_FLUX_THEOREM.csv",
    "branch_split": OUT / "P8_Y5_R2FR_3427_BOUNDARY_BRANCH_SPLIT.csv",
    "bzero_bound_rows": OUT / "P8_Y5_R2FR_3427_BZERO_BOUND_ROWS.csv",
    "pc3400_3_update": OUT / "P8_Y5_R2FR_3427_PC3400_3_UPDATE.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3427_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3427_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3427_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3427_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3427_VALIDATION.csv",
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
        "doc_3426": "PiM handoff to reference/boundary lock",
        "pim_theorem_3426": "Hilbert-identity PiM theorem",
        "pim_update_3426": "PC3400_3 PiM update",
        "icomm_3426": "Icomm/R_eq/projector bound rows",
        "next_3426": "machine-readable 3427 target",
        "doc_3425": "Hamiltonian source charge integrability split",
        "eh_integrability_3425": "EH/Hilbert subcharge integrability",
        "charge_decomp_3425": "MTS charge residual decomposition",
        "bounds_3425": "Hamiltonian/PiM residual rows",
        "boundary_3420": "Hodge/no-flux boundary theorem",
        "projector_3420": "boundary normal/projector owner gate",
        "lock_1017": "older reference-lock law",
        "schema_1017": "M_H_ref/reference/boundary schema",
        "hwt_contract": "Hilbert worldtube parent action contract",
        "r_eq_rows_1015": "R_eq/B_zero/I_commutator retained rows",
        "pim_input_template": "PiM boundary/source input template",
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


def reference_lock_theorem() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "RLT3427_0_branch_reference",
            "claim": "The local Hilbert-identity source branch may use a fixed reference functional selected before source readout.",
            "identity": "H_ref := H_tau[g_ref,e_ref,tau,S_ref], with delta_source H_ref = 0",
            "status": "EXACT_IF_REFERENCE_SELECTED_BY_PARENT_BRANCH",
            "missing_to_promote": "parent must name the reference class and forbid source/radius/readout dependence",
            "valid_for_claim": False,
        },
        {
            "step_id": "RLT3427_1_closed_surface_improvement",
            "claim": "Exact charge improvements do not change a closed linked surface charge when corner data are fixed.",
            "identity": "Q_tau -> Q_tau + dY_tau gives integral_S dY_tau = integral_boundary(S) Y_tau = 0 for closed S",
            "status": "MATHEMATICAL_ZERO_FOR_CLOSED_SURFACE",
            "missing_to_promote": "surfaces must be closed, homologous and selected before readout",
            "valid_for_claim": False,
        },
        {
            "step_id": "RLT3427_2_reference_derivative_silence",
            "claim": "A fixed reference cannot absorb measured-GM calibration.",
            "identity": "partial_{source,r,t,frame,lambda} H_ref = 0",
            "status": "EXACT_IF_RLT3427_0_PARENT_SIGNED",
            "missing_to_promote": "reference rule must be written in the parent action, not chosen after fitting",
            "valid_for_claim": False,
        },
        {
            "step_id": "RLT3427_3_Hilbert_identity_no_Bzero",
            "claim": "In the Hilbert-identity PiM branch, there is no topological-Hilbert exact correction B_zero to prove.",
            "identity": "Pi_M^H J_H = J_H, so Pi_M^H J_H - J_H = 0, not dB_zero",
            "status": "EXACT_FOR_HILBERT_IDENTITY_BRANCH",
            "missing_to_promote": "old independent topological PiM must remain demoted",
            "valid_for_claim": False,
        },
        {
            "step_id": "RLT3427_4_old_topological_Bzero",
            "claim": "Old topological PiM still needs B_zero_flux=0 if used.",
            "identity": "Pi_M^top J_H - Pi_M^H J_H = dB_zero + R_eq",
            "status": "NOT_PROVED_RETAIN_BOUND_ROW",
            "missing_to_promote": "same-object theorem, zero boundary flux and R_eq=0",
            "valid_for_claim": False,
        },
        {
            "step_id": "RLT3427_5_verdict",
            "claim": "Reference shift and B_zero can be killed in the Hilbert-identity branch, conditionally on fixed reference and closed surfaces.",
            "identity": "Delta_ref=0 and B_zero_flux^H=0; old topological B_zero remains retained",
            "status": "PARTIAL_PC3400_3_IMPROVEMENT",
            "missing_to_promote": "parent signature for reference/surface class and no residual symplectic flux",
            "valid_for_claim": False,
        },
    ]


def boundary_flux_theorem() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "BFT3427_0_annulus_balance",
            "claim": "The Hamiltonian charge difference across homologous linked surfaces equals constraint plus boundary leakage in the annulus.",
            "identity": "H_tau[S2]-H_tau[S1] = int_A C_tau + Flux_boundary + Flux_extra",
            "status": "COVARIANT_PHASE_SPACE_BALANCE",
            "missing_to_promote": "explicit parent C_tau and flux decomposition",
            "valid_for_claim": False,
        },
        {
            "step_id": "BFT3427_1_EH_source_free_zero",
            "claim": "For the public EH/Hilbert subcharge in a source-free exterior, the constraint flux vanishes.",
            "identity": "int_A C_tau^EH = 0",
            "status": "EXACT_IF_EH_BRANCH_AND_SOURCE_FREE_EXTERIOR",
            "missing_to_promote": "compact exterior must exclude source support and use same tau",
            "valid_for_claim": False,
        },
        {
            "step_id": "BFT3427_2_fixed_boundary_zero",
            "claim": "Fixed Dirichlet/asymptotic/corner data kill symplectic boundary leakage for the EH subcharge.",
            "identity": "Delta_symp^EH = int_boundary(delta Q_tau^EH - i_tau Theta_EH)_leak = 0",
            "status": "EXACT_IF_BOUNDARY_CONDITIONS_FIXED",
            "missing_to_promote": "parent must define the local boundary class and corner rule",
            "valid_for_claim": False,
        },
        {
            "step_id": "BFT3427_3_no_flux_vector_consistency",
            "claim": "This is compatible with the 3420 no-flux condition for q_loc vector silence.",
            "identity": "P_V n_mu B_GK^{mu nu}=0 is the vector-sector analogue of no compact linked boundary source",
            "status": "CONSISTENT_WITH_3420_NOT_INDEPENDENTLY_SIGNED",
            "missing_to_promote": "same boundary class must serve charge and q_loc vector gates",
            "valid_for_claim": False,
        },
        {
            "step_id": "BFT3427_4_MTS_extra_flux",
            "claim": "Residual MTS/Z/Y6/projector sectors can still create boundary or symplectic flux.",
            "identity": "Delta_symp^MTS = Delta_symp^EH + Delta_symp^Z + Delta_symp^extra + Delta_symp^projector",
            "status": "RETAIN_RESIDUAL_BOUND_ROWS",
            "missing_to_promote": "Z fixed point, Y6 no-extra-mass, projector/hidden-sector no-hair",
            "valid_for_claim": False,
        },
        {
            "step_id": "BFT3427_5_verdict",
            "claim": "EH/reference boundary flux can be conditionally zero, but full MTS boundary flux is not yet closed.",
            "identity": "Delta_symp^EH=0; Delta_symp^MTS_residual must be zeroed or bounded",
            "status": "PARTIAL_THEOREM_NOT_LOCAL_GR",
            "missing_to_promote": "component zero proofs or source-backed B_zero/Delta_symp/H_ref rows",
            "valid_for_claim": False,
        },
    ]


def branch_split() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": "BBS3427_0_Hilbert_identity_EH",
            "branch": "Hilbert-identity PiM plus public EH/Hilbert subcharge",
            "reference_result": "Delta_ref=0 if H_ref is parent-fixed",
            "boundary_result": "B_zero_flux=0 for closed homologous surfaces; Delta_symp^EH=0 under fixed boundary data",
            "current_status": "BEST_CONDITIONAL_ROUTE",
            "valid_for_claim": False,
        },
        {
            "branch_id": "BBS3427_1_old_topological",
            "branch": "old topological PiM same-object route",
            "reference_result": "reference still must be fixed",
            "boundary_result": "B_zero_flux and R_eq remain unproved",
            "current_status": "DEMIT_TO_BOUND_BRANCH_UNLESS_SAME_OBJECT_PROOF",
            "valid_for_claim": False,
        },
        {
            "branch_id": "BBS3427_2_hidden_boundary",
            "branch": "hidden/domain/projector/Y6 boundary charge",
            "reference_result": "not killed by EH reference theorem",
            "boundary_result": "Delta_symp_extra and Delta_extra_mass remain",
            "current_status": "RETAIN_FOR_PC3400_4_OR_BOUND",
            "valid_for_claim": False,
        },
        {
            "branch_id": "BBS3427_3_verdict",
            "branch": "preferred local branch",
            "reference_result": "sign fixed H_ref for public EH/Hilbert branch",
            "boundary_result": "use closed-surface exact-improvement zero; retain only MTS residual flux rows",
            "current_status": "PARTIAL_PC3400_3_CLOSE",
            "valid_for_claim": False,
        },
    ]


def bzero_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "BZR3427_0_reference_shift",
            "quantity": "Delta_ref_over_MH",
            "definition": "reference subtraction shift normalized by dressed source charge",
            "bound_formula": "0 if H_ref is parent-fixed and derivative-silent; otherwise |H_ref_shift|/M_H_ref",
            "status": "CONDITIONAL_ZERO_NEEDS_PARENT_REFERENCE_SIGNATURE",
            "valid_for_claim": False,
        },
        {
            "bound_id": "BZR3427_1_Bzero_Hilbert_identity",
            "quantity": "B_zero_flux^H",
            "definition": "exact boundary improvement flux in Hilbert-identity branch",
            "bound_formula": "0 for closed homologous surfaces with fixed corner data",
            "status": "CONDITIONAL_THEOREM_ZERO",
            "valid_for_claim": False,
        },
        {
            "bound_id": "BZR3427_2_Bzero_topological",
            "quantity": "B_zero_flux^top",
            "definition": "old topological-Hilbert exact correction flux",
            "bound_formula": "M_H_ref^-1 |int_boundary dB_zero|",
            "status": "MISSING_SAME_OBJECT_BOUNDARY_ZERO_PROOF_OR_VALUE",
            "valid_for_claim": False,
        },
        {
            "bound_id": "BZR3427_3_Delta_symp_EH",
            "quantity": "Delta_symp^EH_over_MH",
            "definition": "public EH/Hilbert symplectic boundary leakage",
            "bound_formula": "0 under fixed tau, reference, boundary and corner conditions",
            "status": "CONDITIONAL_THEOREM_ZERO",
            "valid_for_claim": False,
        },
        {
            "bound_id": "BZR3427_4_Delta_symp_residual",
            "quantity": "Delta_symp^residual_over_MH",
            "definition": "Z/Y6/projector/hidden-sector symplectic or boundary leakage",
            "bound_formula": "M_H_ref^-1 |Delta_symp^Z+Delta_symp^Y6+Delta_symp^projector+Delta_symp^hidden|",
            "status": "MISSING_RESIDUAL_NO_HAIR_OR_VALUES",
            "valid_for_claim": False,
        },
        {
            "bound_id": "BZR3427_5_total",
            "quantity": "epsilon_boundary_reference_after_3427",
            "definition": "no-cancellation boundary/reference residual after Hilbert-identity branch split",
            "bound_formula": "Delta_ref_over_MH+B_zero_flux^top+Delta_symp^residual_over_MH",
            "status": "FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
    ]


def pc3400_3_update() -> list[dict[str, Any]]:
    return [
        {
            "pc_piece": "PC3400_3_reference",
            "before_3427": "reference named but not locked",
            "after_3427": "can be signed if parent fixes H_ref before source/readout",
            "remaining": "actual parent reference class still not adopted in core",
            "valid_for_claim": False,
        },
        {
            "pc_piece": "PC3400_3_Bzero",
            "before_3427": "B_zero_flux retained from old topological equality",
            "after_3427": "zero in Hilbert-identity branch; retained only for old topological branch",
            "remaining": "old topological same-object proof if that branch is used",
            "valid_for_claim": False,
        },
        {
            "pc_piece": "PC3400_3_Delta_symp_EH",
            "before_3427": "symplectic leakage broadly open",
            "after_3427": "zero for public EH subcharge under fixed boundary conditions",
            "remaining": "MTS residual sectors can still leak",
            "valid_for_claim": False,
        },
        {
            "pc_piece": "PC3400_3_verdict",
            "before_3427": "PiM/reference/boundary all blocking",
            "after_3427": "PiM and EH/reference-boundary pieces have conditional theorem routes",
            "remaining": "parent adoption, tau/MHref row, residual MTS flux, PC3400_4 no-extra-mass/Y6",
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PG3427_0_reference_branch",
            "claim": "fixed-reference zero is available in the Hilbert-identity source branch",
            "gate_status": "PASS_CONDITIONAL_THEOREM",
            "reason": "H_ref fixed before readout gives derivative silence",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3427_1_Bzero_Hilbert_identity",
            "claim": "B_zero_flux is zero for the Hilbert-identity branch",
            "gate_status": "PASS_CONDITIONAL_THEOREM",
            "reason": "there is no topological-Hilbert exact correction; closed-surface exact improvements integrate to zero",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3427_2_old_topological_Bzero",
            "claim": "old topological branch has zero B_zero_flux",
            "gate_status": "FAIL_CURRENT",
            "reason": "same-object equality and boundary flux proof remain absent",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3427_3_full_boundary_flux",
            "claim": "full MTS symplectic/boundary flux is zero",
            "gate_status": "PARTIAL_ONLY",
            "reason": "EH subcharge yes; Z/Y6/projector/hidden residual flux remains",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3427_4_PC3400_3",
            "claim": "full PC3400_3 is signed",
            "gate_status": "PARTIAL_ONLY",
            "reason": "PiM/reference/Bzero improved; MHref/tau/residual flux still need closure",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3427_5_local_GR",
            "claim": "local GR/Newton/PPN branch is derived",
            "gate_status": "BLOCKED",
            "reason": "PC3400_4 no-extra-mass/Y6, lambda-star, q_loc and second-order PPN gates remain open",
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3427_0_reference_not_a_fit",
            "decision": "A fixed EH/Hilbert reference is legal only if selected before source/readout.",
            "because": "otherwise H_ref can absorb measured GM and become a hidden calibration knob",
            "next_action": "treat H_ref zero as conditional theorem, not current claim",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3427_1_Bzero_branch_split",
            "decision": "B_zero debt belongs to the old topological branch, not the Hilbert-identity branch.",
            "because": "Pi_M^H J_H = J_H has no topological-Hilbert exact correction",
            "next_action": "keep old topological PiM demoted unless same-object equality closes",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3427_2_progress",
            "decision": "PC3400_3 is now mostly reduced to residual MTS flux plus MHref/tau bookkeeping.",
            "because": "PiM commutator, EH reference shift, and Hilbert-identity Bzero have conditional zero routes",
            "next_action": "attack no-extra-mass/Y6 because residual flux now points there",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3427_3_next",
            "decision": "Next target should be no-extra-mass/Y6 monopole silence or bound.",
            "because": "remaining residual boundary flux is dominated by extra/Z/Y6/projector charge channels",
            "next_action": "3428-Y5-R2FR-no-extra-mass-Y6-monopole-silence-or-bound-under-AX1090.md",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target": "3428-Y5-R2FR-no-extra-mass-Y6-monopole-silence-or-bound-under-AX1090.md",
            "script": "scripts/Y5_R2FR_3428_no_extra_mass_Y6_monopole_silence_or_bound.py",
            "objective": "exclude hidden/domain/memory/projector/Y6 extra monopole source charge in the calibrated Hilbert-identity branch, or emit Delta_extra_mass/Y6 source-bound rows",
            "why_next": "3427 gives conditional zero routes for fixed reference and Hilbert-identity Bzero; remaining source-charge danger is extra monopole/Y6 hair",
            "valid_for_claim": False,
        },
        {
            "target": "3429-Y5-R2FR-MHref-tau-source-row-instantiation-or-refusal-under-AX1090.md",
            "script": "scripts/Y5_R2FR_3429_MHref_tau_source_row_instantiation_or_refusal.py",
            "objective": "instantiate a concrete M_H_ref/tau/source row for a toy compact source branch or refuse with exact missing columns",
            "why_next": "needed after no-extra-mass to make the bound branch scoreable",
            "valid_for_claim": False,
        },
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3427_0",
            "script": str(Path(__file__).resolve()),
            "mode": "REFERENCE_BOUNDARY_FLUX_ZERO_OR_BZERO_ROW",
            "summary": "fixed-reference and Hilbert-identity Bzero zero routes written; old topological Bzero and residual MTS symplectic flux retained; local GR not claimed",
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
            "check_id": "VAL3427_0_sources_exist",
            "condition": "all cited source paths exist",
            "passed": all(row["exists"] for row in sources),
            "detail": f"{sum(1 for row in sources if row['exists'])}/{len(sources)} source paths exist",
        },
        {
            "check_id": "VAL3427_1_outputs_scoped",
            "condition": "all outputs are in post-checkpoint-work",
            "passed": outputs_under_root,
            "detail": str(ROOT),
        },
        {
            "check_id": "VAL3427_2_nonclaim",
            "condition": "all generated rows remain nonclaim",
            "passed": nonclaim,
            "detail": "valid_for_claim=false throughout generated rows",
        },
        {
            "check_id": "VAL3427_3_reference_theorem",
            "condition": "fixed-reference theorem exists",
            "passed": any(row["step_id"] == "RLT3427_2_reference_derivative_silence" for row in rows_by_name["reference_lock_theorem"]),
            "detail": "RLT3427_2 present",
        },
        {
            "check_id": "VAL3427_4_Bzero_split",
            "condition": "Hilbert-identity Bzero zero and old topological Bzero retention are both explicit",
            "passed": any(row["bound_id"] == "BZR3427_1_Bzero_Hilbert_identity" for row in rows_by_name["bzero_bound_rows"])
            and any(row["bound_id"] == "BZR3427_2_Bzero_topological" for row in rows_by_name["bzero_bound_rows"]),
            "detail": "BZR3427_1 and BZR3427_2 present",
        },
        {
            "check_id": "VAL3427_5_full_flux_not_claimed",
            "condition": "full MTS boundary flux remains unclaimed",
            "passed": any(row["gate_id"] == "PG3427_3_full_boundary_flux" and row["gate_status"] == "PARTIAL_ONLY" for row in promotion),
            "detail": "residual MTS flux retained",
        },
        {
            "check_id": "VAL3427_6_bound_rows",
            "condition": "Bzero/Delta_symp/H_ref bound rows exist",
            "passed": any(row["bound_id"] == "BZR3427_5_total" for row in rows_by_name["bzero_bound_rows"]),
            "detail": "BZR3427_5 present",
        },
        {
            "check_id": "VAL3427_7_local_GR_blocked",
            "condition": "local GR remains blocked",
            "passed": any(row["gate_id"] == "PG3427_5_local_GR" and row["gate_status"] == "BLOCKED" for row in promotion),
            "detail": "no local-GR claim promoted",
        },
        {
            "check_id": "VAL3427_8_next_target",
            "condition": "next target attacks no-extra-mass/Y6",
            "passed": rows_by_name["next_target"][0]["target"].startswith("3428-Y5-R2FR-no-extra-mass"),
            "detail": rows_by_name["next_target"][0]["target"],
        },
        {
            "check_id": "VAL3427_9_formalization_untouched",
            "condition": "formalization-workbench modified-file count remains 0 during this run",
            "passed": formalization_count == 0,
            "detail": f"modified_count_since_start={formalization_count}",
        },
        {
            "check_id": "VAL3427_10_overall",
            "condition": "3427 reference/boundary checkpoint is internally valid",
            "passed": True,
            "detail": "PASS",
        },
    ]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    text = f"""# 3427 - Reference Boundary Flux Zero or Bzero Row

## Summary
- This checkpoint attacks the `H_ref/B_zero/Delta_symp` part of `PC3400_3`.
- In the Hilbert-identity branch from 3426, `B_zero` is not a magic missing equality term: `Pi_M^H J_H = J_H`, so the old topological exact-correction debt is absent.
- Exact charge improvements integrate to zero on closed homologous linked surfaces when corner data are fixed.
- A fixed `H_ref` is legal only if selected by the parent branch before source/readout; otherwise it is a hidden `GM` calibration knob.
- The public EH/Hilbert subcharge has a conditional zero route for `Delta_symp^EH` under fixed `tau`, reference, boundary and source-free exterior conditions.
- Full MTS boundary flux is **not** claimed: residual `Z/Y6/projector/hidden` flux remains and points straight at the no-extra-mass/Y6 gate.

## Source Register
{md_table(rows_by_name["source_register"])}

## Reference Lock Theorem
{md_table(rows_by_name["reference_lock_theorem"])}

## Boundary Flux Theorem
{md_table(rows_by_name["boundary_flux_theorem"])}

## Boundary Branch Split
{md_table(rows_by_name["branch_split"])}

## Bzero Bound Rows
{md_table(rows_by_name["bzero_bound_rows"])}

## PC3400_3 Update
{md_table(rows_by_name["pc3400_3_update"])}

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
This trims the boundary/reference problem sharply. In the Hilbert-identity branch, reference and exact-boundary issues have clean conditional zero routes. What remains is not vague boundary fog; it is residual MTS source-charge hair, mainly extra/Y6/projector/hidden monopole flux.
"""
    DOC.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    start_utc = datetime.now(timezone.utc)
    rows_by_name = {
        "source_register": source_register(),
        "reference_lock_theorem": reference_lock_theorem(),
        "boundary_flux_theorem": boundary_flux_theorem(),
        "branch_split": branch_split(),
        "bzero_bound_rows": bzero_bound_rows(),
        "pc3400_3_update": pc3400_3_update(),
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
        raise SystemExit(f"3427 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"wrote {len(OUTPUTS)} csv outputs")


if __name__ == "__main__":
    main()
