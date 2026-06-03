from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "charge-current-equality-direct-derivation-attempt"
CHECKPOINT_DOC = "462-charge-current-equality-direct-derivation-attempt.md"
STATUS = "charge_current_equality_direct_derivation_attempt_written_residual_identity_constructed_equality_not_parent_derived_dMeff_mu_extra_retained_no_Newton_or_local_GR_pass"
CLAIM_CEILING = "charge_current_equality_attempt_only_no_measured_GM_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "463-EH-only-or-R11-executable-vector-gate.md"
ATTEMPT_PATH = Path("source-intake/mts_residuals/P8_charge_current_equality_DIRECT_ATTEMPT.csv")
RESIDUAL_PATH = Path("source-intake/mts_residuals/P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv")
STATUS_PATH = Path("source-intake/mts_residuals/P8_charge_current_equality_STATUS.csv")


ATTEMPT_COLUMNS = [
    "step_id",
    "claim",
    "mathematical_form",
    "would_imply",
    "required_premise",
    "current_status",
    "residual_if_failed",
    "next_action",
]

RESIDUAL_COLUMNS = [
    "residual_id",
    "symbolic_piece",
    "meaning",
    "activated_components",
    "affected_stack_rungs",
    "current_status",
    "zero_condition",
    "fallback_input",
]

STATUS_COLUMNS = [
    "claim",
    "status",
    "evidence",
    "claim_credit",
]


SOURCE_DOCS = [
    {
        "path": "450-Hilbert-source-to-measured-monopole-calibration-gate.md",
        "role": "Hilbert current to measured monopole calibration blockers",
    },
    {
        "path": "451-mass-flux-projector-Euler-calibration-attempt.md",
        "role": "Pi_M closure and no-ad-hoc multiplier route",
    },
    {
        "path": "455-PiM-flux-closure-Ward-or-topological-current-attempt.md",
        "role": "Ward/topological/Hamiltonian mass-flux closure routes",
    },
    {
        "path": "457-mass-current-Hamiltonian-boundary-charge-attempt.md",
        "role": "Hamiltonian boundary charge route and HC0-HC9 contract",
    },
    {
        "path": "458-Hamiltonian-charge-to-Poisson-Gauss-calibration-gate.md",
        "role": "PG0-PG10 measured-GM calibration gate",
    },
    {
        "path": "459-PG-calibration-residual-mapper.md",
        "role": "failed PG rows mapped to P8/R11 residual components",
    },
    {
        "path": "460-source-normalized-Newton-branch-theorem-stack.md",
        "role": "SN0-SN11 Newton theorem stack",
    },
    {
        "path": "461-PG-residual-input-derive-or-fill-gate.md",
        "role": "nine PG residual input rows retained/unfilled",
    },
    {
        "path": "source-intake/mts_residuals/P8_Hilbert_monopole_calibration_CONTRACT.csv",
        "role": "HM0-HM8 Hilbert-to-measured-monopole contract",
    },
    {
        "path": "source-intake/mts_residuals/P8_mass_flux_projector_Euler_calibration_CONTRACT.csv",
        "role": "MF0-MF8 mass-flux projector Euler/calibration contract",
    },
    {
        "path": "source-intake/mts_residuals/P8_PiM_flux_closure_Ward_topological_CONTRACT.csv",
        "role": "FC0-FC8 Pi_M flux closure Ward/topological contract",
    },
    {
        "path": "source-intake/mts_residuals/P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv",
        "role": "HC0-HC9 Hamiltonian boundary charge contract",
    },
    {
        "path": "source-intake/mts_residuals/P8_PG_residual_input_DERIVE_OR_FILL_GATE.csv",
        "role": "461 derive/fill decisions for active PG residual inputs",
    },
    {
        "path": "source-intake/mts_residuals/P8_source_normalized_Newton_branch_STACK.csv",
        "role": "SN0-SN11 machine theorem stack",
    },
]


THEOREM_STATEMENT = [
    {
        "part": "conditional_charge_current_equality_theorem",
        "statement": "If the parent action supplies a same-frame EH-like Hamiltonian generator of observed time, an integrable boundary charge, a parent-defined Pi_M Hilbert mass current, zero extra mass-channel charge, constant universal G_eff, and Gauss/orbital calibration, then B_xi/G_eff equals M_eff[Pi_M J_H].",
        "mathematical_form": "B_xi/G_eff = M_eff[Pi_M J_H]",
        "status": "valid_conditional_not_satisfied",
    },
    {
        "part": "direct_residual_identity",
        "statement": "Without those premises the best legal result is a residual identity, not equality.",
        "mathematical_form": "B_xi/G_eff - M_eff[Pi_M J_H] = Delta_frame + Delta_nonEH + Delta_symp + Delta_PiM + Delta_extra + Delta_flux + Delta_G + Delta_cal",
        "status": "constructed_no_zero_proof",
    },
    {
        "part": "current_corpus_status",
        "statement": "The current corpus has route contracts and conditional lemmas but does not prove the residual vector vanishes.",
        "mathematical_form": "Delta_CC != theorem-zero in current evidence",
        "status": "equality_not_parent_derived",
    },
]


ATTEMPT_ROWS = [
    {
        "step_id": "CC0_parent_phase_space_start",
        "claim": "Start from a parent covariant phase-space or Hamiltonian formulation.",
        "mathematical_form": "delta H_xi = integral_{partial Sigma}(delta Q_xi - xi dot theta) + retained terms",
        "would_imply": "a well-defined boundary charge can exist for the observed time flow",
        "required_premise": "parent Lagrangian, symplectic potential, boundary conditions, and exact/asymptotic xi",
        "current_status": "conditional_not_parent_derived",
        "residual_if_failed": "Delta_symp;Delta_frame",
        "next_action": "derive parent symplectic current or retain boundary-reference residual",
    },
    {
        "step_id": "CC1_observed_time_generator",
        "claim": "The charge is generated by observed time, not an arbitrary diffeomorphism.",
        "mathematical_form": "xi = partial_t_obs, stationary Killing, asymptotic time, or admissible quasilocal time with fixed normalization",
        "would_imply": "H_xi is a mass candidate",
        "required_premise": "same observed frame and time normalization",
        "current_status": "not_parent_derived",
        "residual_if_failed": "delta_frame_source;dln_Meff_dt",
        "next_action": "keep frame/source calibration residual active",
    },
    {
        "step_id": "CC2_EH_constraint_source_link",
        "claim": "The Hamiltonian constraint uses the same Hilbert source as the weak-field Poisson equation.",
        "mathematical_form": "C_xi^EH = kappa_eff T_H(n,xi) + no non-EH/source residuals",
        "would_imply": "boundary charge variations are tied to Hilbert source variations",
        "required_premise": "EH-only or complete R11 zero plus same-frame Hilbert current",
        "current_status": "conditional_not_parent_derived",
        "residual_if_failed": "c_nonEH_operator_vector;mu_extra_boundary_bulk_domain",
        "next_action": "derive EH-only exterior or fill R11 vector",
    },
    {
        "step_id": "CC3_projected_mass_current",
        "claim": "The relevant source is the parent-defined projected Hilbert mass current.",
        "mathematical_form": "J_M = Pi_M J_H before readout; M_eff = integral_S J_M with fixed units",
        "would_imply": "the source mass is not chosen after orbital fitting",
        "required_premise": "Pi_M algebra, variation ownership, and absolute mass units",
        "current_status": "conditional_no_cheat_contract_not_parent_derived",
        "residual_if_failed": "dln_Meff_dt;partial_r_ln_mu_obs",
        "next_action": "derive Pi_M parent origin and closure or retain Meff/radial residuals",
    },
    {
        "step_id": "CC4_boundary_variation_equals_projected_source_variation",
        "claim": "The variation of the boundary charge equals the variation of the projected Hilbert mass.",
        "mathematical_form": "delta(B_xi/G_eff) = delta M_eff[Pi_M J_H]",
        "would_imply": "integrating phase space can give B_xi/G_eff = M_eff + constant",
        "required_premise": "integrability, fixed reference zero, no projector/boundary/source leakage",
        "current_status": "not_parent_derived",
        "residual_if_failed": "Delta_symp;Delta_PiM;mu_extra_boundary_bulk_domain",
        "next_action": "derive variation equality or keep mu_extra and boundary residuals",
    },
    {
        "step_id": "CC5_constant_zero_reference",
        "claim": "The integration constant is fixed by the same vacuum/reference branch used for measured GM.",
        "mathematical_form": "B_xi=0 and M_eff=0 on the reference exterior, or constant offset is universal and derivative-free",
        "would_imply": "no hidden constant shift in measured mass",
        "required_premise": "reference subtraction or asymptotic normalization plus derivative silence",
        "current_status": "not_parent_derived",
        "residual_if_failed": "dln_Geff_dt;delta_frame_source;mu_extra_boundary_bulk_domain",
        "next_action": "do not absorb reference shifts unless universal and derivative-free",
    },
    {
        "step_id": "CC6_zero_extra_mass_channel",
        "claim": "All extra boundary, bulk, domain, projector, range, memory, connection, and non-EH charges have zero mass projection.",
        "mathematical_form": "Pi_M(Q_nonEH + Q_boundary + Q_domain + Q_memory + Q_range + Q_connection + Q_delta_kappa)=0",
        "would_imply": "mu_extra=0 in the measured mass channel",
        "required_premise": "Ward/no-hair/topological zero theorem or executable coefficient map",
        "current_status": "not_parent_derived",
        "residual_if_failed": "mu_extra_boundary_bulk_domain;alpha(lambda);partial_r_ln_mu_obs;c_nonEH_operator_vector",
        "next_action": "attempt no-extra-charge theorem only after charge-current ownership is clarified",
    },
    {
        "step_id": "CC7_closed_flux_and_Gauss_calibration",
        "claim": "The equality is stable over the local exterior and reads as the orbital Gauss monopole.",
        "mathematical_form": "d(Pi_M J_H)=0; surface_integral grad Phi dot dS = 4 pi G_eff M_eff; mu_obs = G_eff M_eff",
        "would_imply": "first-order measured-GM Newton if SN0-SN10 are also zeroed",
        "required_premise": "closed Pi_M flux, constant G_eff, zero residuals, slow-particle readout",
        "current_status": "not_parent_derived",
        "residual_if_failed": "dln_Meff_dt;partial_r_ln_mu_obs;dln_Geff_dt;alpha(lambda);eta_source_AB",
        "next_action": "fill residual inputs or derive Gauss/orbital calibration",
    },
    {
        "step_id": "CC8_second_order_limit",
        "claim": "Even if first-order equality lands, local GR needs second-order source stability.",
        "mathematical_form": "delta_beta_source=0 and gamma-1=0 after measured-GM normalization",
        "would_imply": "possible local-GR promotion",
        "required_premise": "second-order weak-field source/operator calculation",
        "current_status": "not_derived",
        "residual_if_failed": "delta_beta_source;gamma_minus_1;c_nonEH_operator_vector",
        "next_action": "defer local-GR promotion until PPN source stability is proved",
    },
]


RESIDUAL_ROWS = [
    {
        "residual_id": "Delta_frame",
        "symbolic_piece": "B_xi[e_charge]/G_eff - B_xi[e_obs]/G_eff",
        "meaning": "boundary charge generated in a different frame or normalization than matter/orbital readout",
        "activated_components": "P8_frame_calibration_split",
        "affected_stack_rungs": "SN0;SN2;SN9;SN10",
        "current_status": "retained_unfilled",
        "zero_condition": "one observed coframe for charge, source variation, matter, clocks, rods, and orbits",
        "fallback_input": "delta_frame_source",
    },
    {
        "residual_id": "Delta_nonEH",
        "symbolic_piece": "sum_i c_i Q_i^nonEH / G_eff",
        "meaning": "non-EH operator terms alter the Hamiltonian charge or weak-field source",
        "activated_components": "R11_EH_operator_ledger",
        "affected_stack_rungs": "SN1;SN5;SN11",
        "current_status": "retained_unfilled",
        "zero_condition": "EH-only exterior theorem or complete R11 coefficient vector scoring to zero",
        "fallback_input": "c_nonEH_operator_vector",
    },
    {
        "residual_id": "Delta_symp",
        "symbolic_piece": "integral_{partial Sigma}(xi dot theta_extra - delta Q_extra)",
        "meaning": "nonintegrable or reference-dependent boundary symplectic term",
        "activated_components": "P8_boundary_bulk_domain_mu_extra;R11_EH_operator_ledger",
        "affected_stack_rungs": "SN1;SN2;SN3;SN6",
        "current_status": "retained_unfilled",
        "zero_condition": "integrable parent Hamiltonian with fixed reference/subtraction and no extra symplectic leakage",
        "fallback_input": "mu_extra_boundary_bulk_domain;c_nonEH_operator_vector",
    },
    {
        "residual_id": "Delta_PiM",
        "symbolic_piece": "M_eff[delta Pi_M J_H] + M_eff[Pi_M J_H - J_M^parent]",
        "meaning": "projector variation or readout-defined mass projector shifts the source charge",
        "activated_components": "P8_Meff_conservation;P8_boundary_bulk_domain_mu_extra",
        "affected_stack_rungs": "SN3;SN4;SN6;SN8",
        "current_status": "retained_unfilled",
        "zero_condition": "Pi_M parent-derived, variation-owned, and equal to the parent mass current before readout",
        "fallback_input": "dln_Meff_dt;mu_extra_boundary_bulk_domain",
    },
    {
        "residual_id": "Delta_extra",
        "symbolic_piece": "Pi_M(Q_boundary + Q_bulk + Q_domain + Q_memory + Q_range + Q_connection)",
        "meaning": "non-Hilbert sectors carry unowned mass-channel charge",
        "activated_components": "P8_boundary_bulk_domain_mu_extra;P8_range_dependence;P8_radial_source_hair",
        "affected_stack_rungs": "SN4;SN6;SN8;SN10",
        "current_status": "retained_unfilled",
        "zero_condition": "Ward/no-hair/topological zero theorem for every extra mass-channel source",
        "fallback_input": "mu_extra_boundary_bulk_domain;alpha(lambda);partial_r_ln_mu_obs",
    },
    {
        "residual_id": "Delta_flux",
        "symbolic_piece": "integral_annulus d(Pi_M J_H)",
        "meaning": "projected source mass drifts with time or radius",
        "activated_components": "P8_Meff_conservation;P8_radial_source_hair",
        "affected_stack_rungs": "SN4;SN8;SN10",
        "current_status": "retained_unfilled",
        "zero_condition": "d(Pi_M J_H)=0 from Ward/Killing, Hamiltonian, topological, or owned Euler route",
        "fallback_input": "dln_Meff_dt;partial_r_ln_mu_obs",
    },
    {
        "residual_id": "Delta_G",
        "symbolic_piece": "B_xi(1/G_eff - 1/G0) or d ln G_eff",
        "meaning": "charge normalization drifts with time, range, species, frame, or domain",
        "activated_components": "P8_Geff_time_drift;P8_species_source_charge;P8_range_dependence",
        "affected_stack_rungs": "SN7;SN10",
        "current_status": "retained_unfilled",
        "zero_condition": "constant universal G_eff/kappa_eff superselection",
        "fallback_input": "dln_Geff_dt;eta_source_AB;alpha(lambda)",
    },
    {
        "residual_id": "Delta_cal",
        "symbolic_piece": "M_eff[Pi_M J_H] - M_Gauss_orbital",
        "meaning": "closed charge is not absolutely calibrated to the Poisson/Gauss/orbital mass",
        "activated_components": "P8_Meff_conservation;P8_boundary_bulk_domain_mu_extra;P8_radial_source_hair",
        "affected_stack_rungs": "SN8;SN9;SN10",
        "current_status": "retained_unfilled",
        "zero_condition": "Gauss surface integral and slow-particle inverse-square readout with no residuals",
        "fallback_input": "dln_Meff_dt;mu_extra_boundary_bulk_domain;partial_r_ln_mu_obs",
    },
    {
        "residual_id": "Delta_PPN",
        "symbolic_piece": "delta_beta_source and gamma_minus_1 after first-order normalization",
        "meaning": "first-order equality fails to promote local GR at second order",
        "activated_components": "P8_nonlinear_beta_source_residue;R11_EH_operator_ledger",
        "affected_stack_rungs": "SN11",
        "current_status": "retained_unfilled",
        "zero_condition": "second-order source/operator calculation gives beta=gamma=1 after measured-GM normalization",
        "fallback_input": "delta_beta_source;gamma_minus_1;c_nonEH_operator_vector",
    },
]


STATUS_ROWS = [
    {
        "claim": "direct residual identity constructed",
        "status": "pass",
        "evidence": "B_xi/G_eff - M_eff[Pi_M J_H] decomposed into nine explicit residual pieces",
        "claim_credit": "architecture_only",
    },
    {
        "claim": "charge-current equality parent-derived",
        "status": "fail",
        "evidence": "Delta_frame, Delta_nonEH, Delta_symp, Delta_PiM, Delta_extra, Delta_flux, Delta_G, Delta_cal are not theorem-zero",
        "claim_credit": "none",
    },
    {
        "claim": "P8_Meff_conservation derived",
        "status": "fail",
        "evidence": "d(Pi_M J_H)=0 remains conditional; dln_Meff_dt retained",
        "claim_credit": "none",
    },
    {
        "claim": "P8_boundary_bulk_domain_mu_extra zeroed",
        "status": "fail",
        "evidence": "mu_extra mass-channel pieces remain visible and unfilled",
        "claim_credit": "none",
    },
    {
        "claim": "Newtonian reduction promoted",
        "status": "fail",
        "evidence": "charge-current equality, Gauss calibration, constant G_eff, zero mu_extra, and derivative silence are unproved",
        "claim_credit": "none",
    },
    {
        "claim": "local GR promoted",
        "status": "fail",
        "evidence": "second-order PPN source stability and R11 operator vector remain unfilled",
        "claim_credit": "none",
    },
]


def utc_now_tag() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")


def exists(path: str) -> bool:
    return (ROOT / path).exists()


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def read_csv_count(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def source_register() -> list[dict[str, Any]]:
    return [
        {
            "source_file": item["path"],
            "exists": str(exists(item["path"])),
            "role": item["role"],
        }
        for item in SOURCE_DOCS
    ]


def gate_results(source_paths_missing: int, attempt_rows: int, residual_rows: int) -> list[dict[str, Any]]:
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if source_paths_missing == 0 else "fail",
            "evidence": f"missing source paths = {source_paths_missing}",
        },
        {
            "gate": "direct_attempt_rows_written",
            "status": "pass" if attempt_rows == 9 else "fail",
            "evidence": f"{attempt_rows} derivation steps written",
        },
        {
            "gate": "residual_decomposition_written",
            "status": "pass" if residual_rows == 9 else "fail",
            "evidence": f"{residual_rows} residual pieces written",
        },
        {
            "gate": "residual_identity_constructed",
            "status": "pass",
            "evidence": "B_xi/G_eff - M_eff[Pi_M J_H] residual identity written",
        },
        {
            "gate": "charge_current_equality_parent_derived",
            "status": "fail",
            "evidence": "zero conditions for residual pieces are not satisfied in current corpus",
        },
        {
            "gate": "P8_Meff_conservation_derived",
            "status": "fail",
            "evidence": "d(Pi_M J_H)=0 not parent-derived",
        },
        {
            "gate": "P8_mu_extra_zero_derived",
            "status": "fail",
            "evidence": "extra mass-channel charges not theorem-zero or numerically filled",
        },
        {
            "gate": "Newtonian_reduction_promoted",
            "status": "fail",
            "evidence": "direct derivation attempt only; PG residual inputs remain retained",
        },
        {
            "gate": "local_GR_claim_allowed",
            "status": "fail",
            "evidence": "SN11/R11 second-order rows remain open",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def render_doc(timestamp: str, run_dir: Path, source_paths_missing: int, attempt_rows: int, residual_rows: int) -> str:
    source_rows = source_register()
    gates = gate_results(source_paths_missing, attempt_rows, residual_rows)
    next_queue = [
        {
            "rank": "1",
            "target": "463-EH-only-or-R11-executable-vector-gate.md",
            "why_next": "Delta_nonEH blocks the charge-current equality and the Poisson coefficient; either derive EH-only or make the R11 vector executable",
        },
        {
            "rank": "2",
            "target": "464-constant-GM-derivative-hair-fill-gate.md",
            "why_next": "Delta_G, Delta_flux, and Delta_cal decide whether constant measured GM can be legal",
        },
        {
            "rank": "3",
            "target": "465-mu-extra-nohair-or-residual-coefficient-map.md",
            "why_next": "Delta_extra is the central hidden mass-channel obstruction after charge ownership",
        },
    ]

    return f"""# 462 - Charge-Current Equality Direct Derivation Attempt

Private source-normalized Newton checkpoint. This is not a public measured-GM, Newtonian-limit, PPN, local-GR, cosmology, EM, or unified-field claim.

## 1. Purpose

Checkpoint 461 identified the rank-one first-order Newton blocker:

```text
B_xi/G_eff = M_eff[Pi_M J_H]
```

This checkpoint attempts that identity directly. The goal is not to gesture at ADM/Komar/Hamiltonian mass. The goal is to decide whether the Hamiltonian boundary charge is the same object as the parent-defined projected Hilbert mass current.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/charge_current_equality_direct_derivation_attempt.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Direct attempt CSV | `{ATTEMPT_PATH}` |
| Residual decomposition CSV | `{RESIDUAL_PATH}` |
| Status CSV | `{STATUS_PATH}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{md_table(source_rows, ["source_file", "exists", "role"])}

## 4. Theorem Statement

{md_table(THEOREM_STATEMENT, ["part", "statement", "mathematical_form", "status"])}

## 5. Direct Derivation Attempt

The direct attempt table has been written to `{ATTEMPT_PATH}`.

{md_table(ATTEMPT_ROWS, ATTEMPT_COLUMNS)}

## 6. Residual Decomposition

The residual decomposition has been written to `{RESIDUAL_PATH}`.

The legal current result is:

```text
B_xi/G_eff - M_eff[Pi_M J_H]
= Delta_frame
+ Delta_nonEH
+ Delta_symp
+ Delta_PiM
+ Delta_extra
+ Delta_flux
+ Delta_G
+ Delta_cal
+ Delta_PPN
```

{md_table(RESIDUAL_ROWS, RESIDUAL_COLUMNS)}

## 7. Machine Status

{md_table(STATUS_ROWS, STATUS_COLUMNS)}

## 8. What Was Actually Derived

The useful result is not equality. The useful result is the exact residual identity. It says the charge-current equality is legal only if the boundary charge, Hilbert source current, projector, source normalization, coupling, and measured orbital readout are all the same branch with no leftover mass-channel pieces.

That is a real narrowing:

```text
equality claim -> nine residual zero conditions
```

At the present checkpoint none of those residual pieces are theorem-zero.

## 9. Why This Does Not Kill the Route

This does not kill the route because the conditional theorem is structurally the same kind of route GR uses: a boundary/asymptotic/Hamiltonian charge becomes mass only after the field equations, symmetry generator, boundary conditions, source current, coupling normalization, and readout map are all aligned.

MTS is not allowed to skip those steps, but it now knows the exact steps.

## 10. Gate Results

{md_table(gates, ["gate", "status", "evidence"])}

## 11. Decision

The direct charge-current derivation did not land as a parent theorem. What landed is the sharp identity:

```text
B_xi/G_eff = M_eff[Pi_M J_H] + Delta_CC
```

where `Delta_CC` is the explicit nine-piece residual vector in section 6. Therefore `P8_Meff_conservation` and `P8_boundary_bulk_domain_mu_extra` remain retained, unfilled, and invalid for Newton/local-GR claim.

Practical read: this is the correct kind of failure. We did not wave the boundary charge into Newtonian mass; we found the exact places where it can fail. The next most efficient route is to attack `Delta_nonEH`: either derive the EH-only local exterior or make the R11 coefficient vector executable. Without that, the Hamiltonian charge and the Poisson coefficient both stay conditional.

## 12. Next Queue

{md_table(next_queue, ["rank", "target", "why_next"])}
"""


def write_run(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_paths_missing = sum(1 for item in SOURCE_DOCS if not exists(item["path"]))
    missing_sources = [item["path"] for item in SOURCE_DOCS if not exists(item["path"])]

    write_csv(ROOT / ATTEMPT_PATH, ATTEMPT_ROWS, ATTEMPT_COLUMNS)
    write_csv(ROOT / RESIDUAL_PATH, RESIDUAL_ROWS, RESIDUAL_COLUMNS)
    write_csv(ROOT / STATUS_PATH, STATUS_ROWS, STATUS_COLUMNS)
    write_csv(results_dir / "charge_current_equality_direct_attempt.csv", ATTEMPT_ROWS, ATTEMPT_COLUMNS)
    write_csv(results_dir / "charge_current_residual_decomposition.csv", RESIDUAL_ROWS, RESIDUAL_COLUMNS)
    write_csv(results_dir / "charge_current_equality_status.csv", STATUS_ROWS, STATUS_COLUMNS)

    attempt_rows = read_csv_count(ROOT / ATTEMPT_PATH)
    residual_rows = read_csv_count(ROOT / RESIDUAL_PATH)
    status_rows = read_csv_count(ROOT / STATUS_PATH)

    doc_text = render_doc(timestamp, run_dir, source_paths_missing, attempt_rows, residual_rows)
    (ROOT / CHECKPOINT_DOC).write_text(doc_text, encoding="utf-8")

    status = {
        "timestamp": timestamp,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": CHECKPOINT_DOC,
        "run_dir": str(run_dir.relative_to(ROOT)),
        "source_paths_missing": source_paths_missing,
        "missing_sources": missing_sources,
        "attempt_rows": attempt_rows,
        "residual_decomposition_rows": residual_rows,
        "status_rows": status_rows,
        "residual_identity_constructed": True,
        "charge_current_equality_parent_derived": False,
        "P8_Meff_conservation_derived": False,
        "P8_mu_extra_zero_derived": False,
        "Newtonian_reduction_promoted": False,
        "local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    return status


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=utc_now_tag())
    args = parser.parse_args()
    status = write_run(args.timestamp)
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
