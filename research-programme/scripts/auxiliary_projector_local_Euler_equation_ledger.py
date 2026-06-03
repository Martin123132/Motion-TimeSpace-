from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "auxiliary-projector-local-Euler-equation-ledger"
CHECKPOINT_DOC = "436-auxiliary-projector-local-Euler-equation-ledger.md"
STATUS = "auxiliary_projector_local_Euler_equation_ledger_written_C1_owner_contract_no_all_on_shell_no_local_GR_pass"
CLAIM_CEILING = "auxiliary_projector_local_Euler_equation_ledger_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass"
NEXT_TARGET = "437-R10-alpha-lambda-executable-curve-contract.md"


SOURCE_DOCS = [
    {
        "path": "356-parent-action-ward-identity-and-projector-variation.md",
        "role": "parent variation sectors and explicit Ward force ledger",
    },
    {
        "path": "357-Ward-owned-local-nohair-or-retained-PPN-residual-map.md",
        "role": "force fate map and retained PPN residual vector",
    },
    {
        "path": "403-boundary-domain-flux-nohair-numeric-contract.md",
        "role": "boundary/domain/flux numeric locks and alpha3 severity",
    },
    {
        "path": "429-Ward-Bianchi-exchange-owner-for-Poisson-source.md",
        "role": "C1 auxiliary-on-shell condition in q_loc identity",
    },
    {
        "path": "430-Ward-source-residual-zero-route-gate.md",
        "role": "C1 ranked as best theorem route",
    },
    {
        "path": "435-exterior-extra-source-nohair-owner-gate.md",
        "role": "R_extra owner gate and C1 next target",
    },
    {
        "path": "runs/20260601-181500-parent-action-ward-identity-and-projector-variation/results/parent_variation_terms.csv",
        "role": "machine-readable parent variation terms",
    },
    {
        "path": "runs/20260601-181500-parent-action-ward-identity-and-projector-variation/results/force_ledger.csv",
        "role": "machine-readable force origins and zero conditions",
    },
    {
        "path": "runs/20260601-181500-parent-action-ward-identity-and-projector-variation/results/projector_variation_forks.csv",
        "role": "projector variation fork validity table",
    },
    {
        "path": "runs/20260601-183000-Ward-owned-local-nohair-or-retained-PPN-residual-map/results/force_fate_map.csv",
        "role": "Ward-force fates and retained residual targets",
    },
    {
        "path": "runs/20260602-101500-Ward-Bianchi-exchange-owner-for-Poisson-source/results/exchange_owner_conditions.csv",
        "role": "C0-C7 conditions including C1",
    },
    {
        "path": "runs/20260602-103000-Ward-source-residual-zero-route-gate/results/route_ranking.csv",
        "role": "C1 ranked first in zero-route queue",
    },
    {
        "path": "runs/20260602-121500-exterior-extra-source-nohair-owner-gate/results/exterior_source_owner_gate.csv",
        "role": "E5 auxiliary-offshell gate and R_extra routing",
    },
]


C1_IDENTITY_CHAIN = [
    {
        "step": 1,
        "claim": "Write the local parent configuration with every hidden variable included.",
        "mathematical_form": "Z_A in {X_A, P_D, lambda_P, Y_boundary, chi_D, n_mu, L_cg, Pi_M, c_nonEH}",
        "status": "ledger_contract",
        "meaning": "fixed external or readout-only variables cannot secretly source local equations",
    },
    {
        "step": 2,
        "claim": "Vary every hidden variable before reducing to readout.",
        "mathematical_form": "E_A := delta S_parent / delta Z_A",
        "status": "required_not_fully_supplied",
        "meaning": "C1 can only be theorem-level if every E_A exists as a parent equation",
    },
    {
        "step": 3,
        "claim": "The Ward identity exposes off-shell forces.",
        "mathematical_form": "q_loc^nu contains sum_A E_A nabla^nu Z_A plus projector/boundary/domain force terms",
        "status": "structural_identity_imported",
        "meaning": "off-shell hidden variables are not small by default; they are force sources",
    },
    {
        "step": 4,
        "claim": "On-shell auxiliary equations kill only their own off-shell force term.",
        "mathematical_form": "E_A=0 => E_A nabla^nu Z_A=0",
        "status": "conditional_theorem_shape",
        "meaning": "stress, boundary, non-EH, and source-normalization debts can still remain",
    },
    {
        "step": 5,
        "claim": "Constraint/topological variables need a stronger proof than E_A=0.",
        "mathematical_form": "P_D, chi_D, n_mu, L_cg must be covariant/dynamical/topological and locally silent",
        "status": "not_parent_derived",
        "meaning": "a solved constraint can still choose a preferred frame or location if the selector is physical",
    },
    {
        "step": 6,
        "claim": "Boundary-supported equations are not bulk no-hair by themselves.",
        "mathematical_form": "E_boundary=0 must imply no B_TF, B_0i, B_rad(r), clock/WEP, or drift hair",
        "status": "not_derived",
        "meaning": "boundary flux can be owned but nonzero in local observables",
    },
    {
        "step": 7,
        "claim": "If any E_A is missing, symbolic, or not solved, its force is retained.",
        "mathematical_form": "F_A^nu -> residual rows R7/R9/R10/R11 plus induced PPN rows",
        "status": "retained_policy",
        "meaning": "no row gets theorem-zero credit from an unnamed auxiliary equation",
    },
]


EULER_LEDGER_ROWS = [
    {
        "ledger_id": "A0_bulk_X_memory_load",
        "field_or_selector": "X_A bulk/memory/load fields",
        "required_euler_equation": "E_X_A = delta S_parent/delta X_A = 0",
        "zero_condition": "positive source-free massive/gauge/topological exterior or solved screened static branch",
        "current_status": "operator_and_sources_not_parent_derived",
        "if_not_zero_rows": "R3;R4;R9;R10",
        "next_action": "derive local X operator/sign/source-free exterior or supply alpha_X(lambda_X)",
    },
    {
        "ledger_id": "A1_projector_PD",
        "field_or_selector": "P_D relative-chain/cohomology projector",
        "required_euler_equation": "E_P = delta S_parent/delta P_D = 0 or topological constraint identity",
        "zero_condition": "metric-independent covariant/topological P_D with no bulk stress",
        "current_status": "conditional_open",
        "if_not_zero_rows": "R5;R6;R7;R8;R11",
        "next_action": "derive P_D as parent-owned covariant object or retain projector stress vector",
    },
    {
        "ledger_id": "A2_projector_constraint_multiplier",
        "field_or_selector": "lambda_P enforcing relative-chain/projector constraint",
        "required_euler_equation": "E_lambdaP = C_rel[P_D,Q] = 0",
        "zero_condition": "constraint algebra closes and leaves no local vector/shear/monopole hair",
        "current_status": "not_supplied",
        "if_not_zero_rows": "R5;R6;R7;R8;R11",
        "next_action": "write explicit constraint and show first-class/topological or retain",
    },
    {
        "ledger_id": "A3_boundary_class_variables",
        "field_or_selector": "Y_partialD, boundary class, induced boundary data",
        "required_euler_equation": "E_boundary = delta S_parent/delta Y_partialD = 0 with flux balance",
        "zero_condition": "class-only/topological boundary leaves at most constant universal monopole",
        "current_status": "conditional_noangular_radial_flux_open",
        "if_not_zero_rows": "R3;R4;R7;R8;R9",
        "next_action": "derive class-only boundary action and radial/time no-hair or retain coefficients",
    },
    {
        "ledger_id": "A4_domain_selector",
        "field_or_selector": "chi_D coherent-domain selector",
        "required_euler_equation": "E_chi = delta S_parent/delta chi_D = 0",
        "zero_condition": "domain selected covariantly before scoring with no local preferred location",
        "current_status": "not_parent_derived",
        "if_not_zero_rows": "R5;R6;R7;R8;R10",
        "next_action": "derive zero-knob covariant domain selector or retain domain residuals",
    },
    {
        "ledger_id": "A5_domain_normal_frame",
        "field_or_selector": "n_mu, local frame, domain vector data",
        "required_euler_equation": "E_n = delta S_parent/delta n_mu = 0 plus normalization/orthogonality constraints",
        "zero_condition": "normal/frame data are gauge, dynamically aligned, or absent from local observables",
        "current_status": "not_derived",
        "if_not_zero_rows": "R5;R6;R8",
        "next_action": "prove no preferred-frame/location vector survives or retain alpha1/alpha2/xi rows",
    },
    {
        "ledger_id": "A6_coarse_graining_scale",
        "field_or_selector": "L_cg coarse-graining/domain scale",
        "required_euler_equation": "E_L = delta S_parent/delta L_cg = 0",
        "zero_condition": "nabla_mu L_cg=0 locally or L_cg is global/readout-only with no fifth-force gradient",
        "current_status": "not_derived",
        "if_not_zero_rows": "R8;R9;R10",
        "next_action": "derive local constancy/decoupling of L_cg or supply gradient residual",
    },
    {
        "ledger_id": "A7_mass_flux_projector",
        "field_or_selector": "Pi_M J source-normalization flux",
        "required_euler_equation": "E_PiM or source identity d(Pi_M J)=0",
        "zero_condition": "closed calibrated M_eff monopole and no radial/time/species leakage",
        "current_status": "conditional_flux_calibration_open",
        "if_not_zero_rows": "R1;R4;R9;R10",
        "next_action": "derive flux closure plus absolute calibration or retain source-normalization residuals",
    },
    {
        "ledger_id": "A8_nonEH_operator_coefficients",
        "field_or_selector": "c_nonEH or non-EH operator auxiliaries",
        "required_euler_equation": "E_c = delta S_parent/delta c_nonEH = 0 or c_nonEH fixed by parent symmetry",
        "zero_condition": "EH-only exterior or executable non-EH coefficient vector",
        "current_status": "retained_symbolic",
        "if_not_zero_rows": "R3;R4;R8;R10;R11",
        "next_action": "derive EH-only selection or provide c_nonEH vector for scorer",
    },
    {
        "ledger_id": "A9_readout_active_masks",
        "field_or_selector": "P_read, P_active, fitted masks",
        "required_euler_equation": "not allowed in S_parent; readout after variation only",
        "zero_condition": "readout variables do not enter parent action or local Euler equations",
        "current_status": "conditional_no_cheat_contract",
        "if_not_zero_rows": "R0;R1;R5;R11",
        "next_action": "reject any branch where readout masks backreact through S_parent",
    },
]


LEGAL_FATES = [
    {
        "fate": "on_shell_theorem_zero",
        "required_evidence": "explicit E_A from parent action plus proof E_A=0 in local exterior",
        "row_policy": "only the E_A nabla Z_A term can receive theorem-zero credit",
    },
    {
        "fate": "gauge_or_topological",
        "required_evidence": "first-class/gauge/topological proof with no local stress or force",
        "row_policy": "can demote local bulk force, but boundary/source remnants still audited",
    },
    {
        "fate": "boundary_only_harmless",
        "required_evidence": "support only on boundary plus class/topological constant monopole",
        "row_policy": "may become calibration only if universal/time/range/species independent",
    },
    {
        "fate": "retained_residual",
        "required_evidence": "coefficient, amplitude, or curve mapped to R rows",
        "row_policy": "score or block depending on executable data",
    },
    {
        "fate": "invalid_hidden_variable",
        "required_evidence": "fixed external projector/domain/mask or dropped metric stress",
        "row_policy": "reject branch rather than retain as small",
    },
]


INVALID_FORKS = [
    {
        "fork": "fixed_external_projector_or_domain",
        "why_invalid": "not varied and explicitly breaks the Ward identity while looking like a definition",
        "required_repair": "make it covariant/dynamical/topological or reject branch",
    },
    {
        "fork": "metric_dependent_projector_without_stress",
        "why_invalid": "delta_g P_D contributes physical stress",
        "required_repair": "retain T_projector/F_P or prove metric independence",
    },
    {
        "fork": "solved_auxiliary_but_stress_dropped",
        "why_invalid": "E_A=0 does not imply T_A=0 or div T_A=0",
        "required_repair": "show stress is zero/pure gauge/topological or retain coefficient",
    },
    {
        "fork": "boundary_EOM_used_as_bulk_nohair",
        "why_invalid": "flux balance can still leave radial/vector/shear hair",
        "required_repair": "derive boundary no-hair or retain boundary multipoles",
    },
    {
        "fork": "readout_mask_backreacts",
        "why_invalid": "post-readout fitting mask becomes a hidden parent source",
        "required_repair": "readout after variation only",
    },
    {
        "fork": "symbolic_Euler_equation_counts_as_zero",
        "why_invalid": "an unnamed E_A=0 cannot be scored or audited",
        "required_repair": "write explicit equation, solution class, and residual fallback",
    },
]


ROW_IMPLICATIONS = [
    {
        "row_id": "R5_alpha1",
        "C1_channel": "projector/domain vector and fixed-frame selector",
        "current_transition": "retained_not_upgraded",
    },
    {
        "row_id": "R6_alpha2",
        "C1_channel": "projector/domain vector and normal-frame data",
        "current_transition": "retained_not_upgraded",
    },
    {
        "row_id": "R7_alpha3",
        "C1_channel": "unowned off-shell auxiliary/projector/domain momentum flux",
        "current_transition": "conditional_route_not_pass",
    },
    {
        "row_id": "R8_xi",
        "C1_channel": "domain/boundary/projector anisotropy",
        "current_transition": "retained_not_upgraded",
    },
    {
        "row_id": "R9_Gdot",
        "C1_channel": "time-dependent auxiliary/source/boundary/domain flux",
        "current_transition": "retained_contingent_not_upgraded",
    },
    {
        "row_id": "R10_fifth_force",
        "C1_channel": "bulk X, L_cg gradient, radial hair, finite-range auxiliary tail",
        "current_transition": "symbolic_deferred_not_upgraded",
    },
    {
        "row_id": "R11_EH_operator_ledger",
        "C1_channel": "projector stress and non-EH auxiliary/operator coefficients",
        "current_transition": "retained_symbolic_not_upgraded",
    },
]


RESIDUAL_INPUT_SCHEMA = [
    {
        "column": "ledger_id",
        "meaning": "matches one A0-A9 Euler ledger row",
        "required": True,
    },
    {
        "column": "derivation_status",
        "meaning": "theorem_zero, gauge_topological, harmless_calibration, retained_numeric, retained_symbolic, invalid",
        "required": True,
    },
    {
        "column": "equation_source",
        "meaning": "path to derivation/equation source or run artifact",
        "required": True,
    },
    {
        "column": "residual_rows",
        "meaning": "semicolon-separated R rows affected if not theorem-zero",
        "required": True,
    },
    {
        "column": "coefficient_or_curve_source",
        "meaning": "path to numeric coefficient, alpha(lambda), or c_nonEH vector if retained",
        "required": False,
    },
    {
        "column": "claim_allowed",
        "meaning": "false unless all relevant rows are theorem-zero or scored below locks",
        "required": True,
    },
]


THEOREM_ATTEMPT_STATUS = [
    {
        "claim": "C1 Euler owner ledger written",
        "status": "pass",
        "evidence": "10 hidden-variable ledger rows and 5 legal fates recorded",
    },
    {
        "claim": "C1 is structurally the best theorem route",
        "status": "pass",
        "evidence": "route ranking imports C1 as direct owner of E_A nabla Z_A",
    },
    {
        "claim": "all auxiliary/projector/domain equations are parent-derived and solved",
        "status": "fail",
        "evidence": "explicit equations, signs, constraints, and solution classes are not supplied for A0-A8",
    },
    {
        "claim": "off-shell force term is theorem-zero",
        "status": "fail",
        "evidence": "no all-channel E_A=0 proof; retained residuals remain",
    },
    {
        "claim": "local GR/Newton/PPN promoted",
        "status": "fail",
        "evidence": "0 row upgrades; R7/R9/R10/R11 remain retained or symbolic",
    },
]


GATE_RESULTS_TEMPLATE = [
    {
        "gate": "C1_identity_chain_written",
        "status": "pass",
        "evidence": "7 identity stages recorded",
    },
    {
        "gate": "Euler_ledger_written",
        "status": "pass",
        "evidence": "10 hidden-variable rows recorded",
    },
    {
        "gate": "legal_fates_written",
        "status": "pass",
        "evidence": "5 legal fates recorded",
    },
    {
        "gate": "invalid_forks_forbidden",
        "status": "pass",
        "evidence": "6 fake-zero forks rejected",
    },
    {
        "gate": "all_auxiliary_equations_parent_supplied",
        "status": "fail",
        "evidence": "explicit parent Euler equations missing for several hidden variables",
    },
    {
        "gate": "all_auxiliary_equations_on_shell_locally",
        "status": "fail",
        "evidence": "no proof E_A=0 for A0-A8 in compact ordinary exterior",
    },
    {
        "gate": "projector_domain_covariance_derived",
        "status": "fail",
        "evidence": "P_D/chi_D/n_mu/L_cg local silence not parent-derived",
    },
    {
        "gate": "auxiliary_stress_zero_or_harmless",
        "status": "fail",
        "evidence": "E_A=0 does not yet imply T_A/div T_A harmless for all sectors",
    },
    {
        "gate": "residual_input_schema_written",
        "status": "pass",
        "evidence": "template schema for retained C1 rows recorded",
    },
    {
        "gate": "runner_rows_promoted_to_theorem_zero",
        "status": "fail",
        "evidence": "0 row upgrades; C1 remains owner contract",
    },
    {
        "gate": "local_GR_promoted",
        "status": "fail",
        "evidence": "Euler ledger only; no EH/Newton/PPN/local-GR pass",
    },
    {
        "gate": "claim_ceiling_enforced",
        "status": "pass",
        "evidence": CLAIM_CEILING,
    },
]


DECISION = [
    {
        "decision": "C1 is now an explicit Euler owner ledger. This is the best structural route for the off-shell Ward force because q_loc contains the terms E_A nabla Z_A, and those terms vanish only when the parent action supplies and solves every hidden-variable Euler equation. The current corpus does not yet provide explicit local equations, signs, constraint algebra, source-free exterior conditions, stress harmlessness, or residual coefficients for all auxiliary/projector/domain sectors. Therefore C1 is sharpened but not promoted: hidden-variable forces are either future theorem targets or retained residuals, and local GR remains unclaimed.",
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "rank": 1,
        "target": "437-R10-alpha-lambda-executable-curve-contract.md",
        "why_next": "R10 is still symbolic; finite-range auxiliary tails need theorem-zero or an executable alpha(lambda) curve",
    },
    {
        "rank": 2,
        "target": "438-R11-nonEH-coefficient-vector-contract.md",
        "why_next": "R11 remains symbolic unless EH-only exterior is derived or c_nonEH is supplied",
    },
    {
        "rank": 3,
        "target": "filled local residual vector smoke",
        "why_next": "C1 retained rows need actual coefficients/curves before empirical local testing",
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", " ")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCE_DOCS:
        source_path = ROOT / source["path"]
        rows.append(
            {
                "source_file": source["path"],
                "exists": source_path.exists(),
                "role": source["role"],
            }
        )
    return rows


def gate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    source_gate = {
        "gate": "source_paths_exist",
        "status": "pass" if not missing_sources else "fail",
        "evidence": "all cited source paths exist" if not missing_sources else ";".join(missing_sources),
    }
    return [source_gate, *GATE_RESULTS_TEMPLATE]


def write_checkpoint_markdown(run_dir: Path, gate_result_rows: list[dict[str, Any]]) -> None:
    source_rows = source_register_rows()
    text = f"""# 436 - Auxiliary/Projector Local Euler-Equation Ledger

Private C1/local-Ward derivation checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 435 routed every exterior extra source. This checkpoint attacks the highest-ranked theorem route from checkpoint 430: C1, the requirement that every hidden auxiliary/projector/domain variable has a parent Euler equation and is either on shell locally or retained as a force.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/auxiliary_projector_local_Euler_equation_ledger.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(source_rows, ["source_file", "exists", "role"])}

## 4. C1 Identity Chain

{markdown_table(C1_IDENTITY_CHAIN, ["step", "claim", "status", "meaning"])}

Core local identity:

```text
For hidden variables Z_A, define E_A := delta S_parent / delta Z_A.

The local Ward/Bianchi force contains

q_loc^nu superset sum_A E_A nabla^nu Z_A
                 + F_projector^nu + F_boundary^nu + F_domain^nu.

C1 passes only if each E_A is explicitly supplied and either:
  E_A=0 in the local exterior,
  Z_A is pure gauge/topological with no local stress,
  the source is harmless constant universal calibration,
  or the residual is retained and scored.
```

## 5. Euler Ledger Rows

{markdown_table(EULER_LEDGER_ROWS, ["ledger_id", "field_or_selector", "current_status", "if_not_zero_rows", "next_action"])}

## 6. Legal Fates

{markdown_table(LEGAL_FATES, ["fate", "required_evidence", "row_policy"])}

## 7. Invalid Forks

{markdown_table(INVALID_FORKS, ["fork", "why_invalid", "required_repair"])}

## 8. Row Implications

{markdown_table(ROW_IMPLICATIONS, ["row_id", "C1_channel", "current_transition"])}

## 9. Residual Input Schema

{markdown_table(RESIDUAL_INPUT_SCHEMA, ["column", "meaning", "required"])}

## 10. Theorem Attempt Status

{markdown_table(THEOREM_ATTEMPT_STATUS, ["claim", "status", "evidence"])}

## 11. Gate Results

{markdown_table(gate_result_rows, ["gate", "status", "evidence"])}

## 12. Decision

{DECISION[0]["decision"]}

Practical read: this is good plumbing. C1 is where hidden machinery stops being mystique and becomes engineering: write the equation, solve it, or carry the force. No local-GR belt until that ledger closes.

## 13. Next Queue

{markdown_table(NEXT_QUEUE, ["rank", "target", "why_next"])}
"""
    (ROOT / CHECKPOINT_DOC).write_text(text, encoding="utf-8")


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()
    gate_result_rows = gate_rows(source_rows)

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "C1_identity_chain.csv", C1_IDENTITY_CHAIN)
    write_csv(results_dir / "Euler_ledger_rows.csv", EULER_LEDGER_ROWS)
    write_csv(results_dir / "legal_fates.csv", LEGAL_FATES)
    write_csv(results_dir / "invalid_forks.csv", INVALID_FORKS)
    write_csv(results_dir / "row_implications.csv", ROW_IMPLICATIONS)
    write_csv(results_dir / "residual_input_schema.csv", RESIDUAL_INPUT_SCHEMA)
    write_csv(results_dir / "theorem_attempt_status.csv", THEOREM_ATTEMPT_STATUS)
    write_csv(results_dir / "gate_results.csv", gate_result_rows)
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)

    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "C1_identity_steps": len(C1_IDENTITY_CHAIN),
        "Euler_ledger_rows": len(EULER_LEDGER_ROWS),
        "legal_fates": len(LEGAL_FATES),
        "invalid_forks": len(INVALID_FORKS),
        "residual_schema_columns": len(RESIDUAL_INPUT_SCHEMA),
        "C1_owner_contract_written": True,
        "all_auxiliary_equations_parent_supplied": False,
        "all_auxiliary_equations_on_shell_locally": False,
        "projector_domain_covariance_derived": False,
        "auxiliary_stress_zero_or_harmless": False,
        "theorem_zero_upgrades": 0,
        "claim_allowed_rows": 0,
        "local_GR_claim_allowed": False,
        "checkpoint_doc": CHECKPOINT_DOC,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    write_checkpoint_markdown(run_dir, gate_result_rows)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 436 auxiliary/projector local Euler-equation ledger artifacts."
    )
    parser.add_argument(
        "--timestamp",
        default=datetime.now().strftime("%Y%m%d-%H%M%S"),
        help="Run timestamp prefix.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_dir = write_run(args.timestamp)
    print(json.dumps({"status": STATUS, "run_dir": str(run_dir)}, indent=2))


if __name__ == "__main__":
    main()
