from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "worldtube_source_measure_glue_theorem_contract_built_EH_known_MTS_not_derived_Meff_residual_runner_written"
CLAIM_CEILING = "conditional_EH_Iyer_Wald_style_glue_only_current_MTS_parent_action_not_yet_local_GR"
NEXT_TARGET = "511-minimal-parent-action-local-GR-fixed-point-ansatz.md"

DOC_PATH = Path("510-worldtube-source-measure-glue-or-Meff-residual-runner.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_WORLDTUBE_SOURCE_MEASURE_SOURCE_REGISTER.csv")
THEOREM_PATH = Path("source-intake/mts_residuals/P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv")
CLAUSES_PATH = Path("source-intake/mts_residuals/P8_WORLDTUBE_SOURCE_MEASURE_CLAUSES.csv")
PROOF_SKETCH_PATH = Path("source-intake/mts_residuals/P8_WORLDTUBE_SOURCE_MEASURE_PROOF_SKETCH.csv")
RESIDUAL_RUNNER_PATH = Path("source-intake/mts_residuals/P8_WORLDTUBE_MEFF_RESIDUAL_RUNNER.csv")
GATE_TESTS_PATH = Path("source-intake/mts_residuals/P8_WORLDTUBE_SOURCE_MEASURE_GATE_TESTS.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_WORLDTUBE_SOURCE_MEASURE_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_WORLDTUBE_SOURCE_MEASURE_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_WORLDTUBE_SOURCE_MEASURE_ROUTE_UPDATE.csv")

SOURCE_REGISTER = [
    {
        "source_file": "509-source-measure-Meff-flux-closure-after-kappa-gate.md",
        "role": "previous source-measure flux closure contract and residual map",
    },
    {
        "source_file": "508-constant-kappa-superselection-or-drift-residual.md",
        "role": "conditional constant-kappa premise carried forward without promotion",
    },
    {
        "source_file": "506-local-EH-reduction-and-extra-sector-silence-theorem.md",
        "role": "local EH reduction and extra-sector silence conditions",
    },
    {
        "source_file": "505-parent-Noether-mass-charge-closure-theorem-or-closure-demotion.md",
        "role": "parent Noether mass-charge closure theorem attempt",
    },
    {
        "source_file": "504-parent-Hilbert-worldtube-glue-or-external-radial-input-plan.md",
        "role": "worldtube glue C-term ledger and source-measure blocker",
    },
    {
        "source_file": "451-mass-flux-projector-Euler-calibration-attempt.md",
        "role": "mass-flux projector/Euler calibration contract",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv",
        "role": "T509 source-measure flux theorem rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv",
        "role": "SM509 required source-measure clauses",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv",
        "role": "SMR509 residual map to inherit into runner",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv",
        "role": "existing W504 worldtube source-measure clauses",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_charge_current_equality_DIRECT_ATTEMPT.csv",
        "role": "direct charge-current equality blockers",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_mass_flux_projector_Euler_calibration_CONTRACT.csv",
        "role": "mass-flux projector closure and calibration blockers",
    },
    {
        "source_file": "scripts/worldtube_source_measure_glue_or_Meff_residual_runner.py",
        "role": "this checkpoint generator",
    },
]

THEOREM_ROWS = [
    {
        "theorem_id": "T510_0_EH_reference_glue",
        "statement": "In an EH plus minimally coupled matter parent theory, the on-shell diffeomorphism Noether current gives a closed exterior surface charge; the difference between two linking surfaces is the Hamiltonian constraint flux through the annulus.",
        "mathematical_form": "J_tau = theta(phi,L_tau phi) - tau dot L; on shell J_tau = dQ_tau; Delta H_tau = integral_constraints + integral_boundary(delta Q_tau - tau dot theta)",
        "what_it_derives": "exterior mass charge is independent of linking radius when the exterior is source-free and boundary fluxes are controlled",
        "status": "known_GR_style_conditional_reference",
        "MTS_current_status": "not_yet_inherited",
    },
    {
        "theorem_id": "T510_1_worldtube_source_measure",
        "statement": "A worldtube source measure equals the exterior mass charge only when it is defined as the dressed Hamiltonian/Noether source charge, not as bare rest-matter mass.",
        "mathematical_form": "M_source[W] := H_tau[outer S] - H_tau[reference]; M_bare = integral_W rho_rest is not generally equal to M_source",
        "what_it_derives": "the measured source charge includes binding, boundary, and field dressing already owned by the parent charge",
        "status": "necessary_definition_correction",
        "MTS_current_status": "definition_not_yet_locked",
    },
    {
        "theorem_id": "T510_2_MTS_transfer_condition",
        "statement": "MTS inherits the EH worldtube glue only if its local exterior fixed point has the EH symplectic charge, one observed source frame, constant kappa, silent extra sectors, and a fixed Pi_M projector.",
        "mathematical_form": "Q_MTS_tau = Q_EH_tau + Delta_nonEH + Delta_symp + Delta_PiM + Delta_extra + Delta_frame; all Delta terms must vanish or be bounded",
        "what_it_derives": "conditional epsilon_radial_Meff=0 and source-measure equality for MTS",
        "status": "conditional_MTS_transfer_theorem",
        "MTS_current_status": "premises_open",
    },
    {
        "theorem_id": "T510_3_Newton_PPN_readout",
        "statement": "Even after worldtube glue, local GR needs the same charge to control the 1/r metric coefficient and the second-order PPN terms.",
        "mathematical_form": "g_00=-1+2G_ref M_source/r + O(r^-2); g_ij=(1+2 gamma G_ref M_source/r)delta_ij; beta,gamma residuals explicit",
        "what_it_derives": "Newtonian recovery and PPN consistency only after metric readout is derived",
        "status": "not_reached",
        "MTS_current_status": "local_GR_claim_blocked",
    },
]

CLAUSE_ROWS = [
    {
        "clause_id": "WG510_0_parent_diffeomorphism_invariance",
        "required_clause": "The parent local action is diffeomorphism invariant and has a well-defined covariant symplectic potential theta.",
        "failure_mode": "Noether current and Hamiltonian charge are undefined or gauge-dependent",
        "current_status": "not_explicit_for_full_MTS_parent",
    },
    {
        "clause_id": "WG510_1_minimal_observed_matter_coupling",
        "required_clause": "Matter couples to the same observed metric/coframe used by the local orbital and clock readout.",
        "failure_mode": "source mass and orbital mass live in different frames",
        "current_status": "open",
    },
    {
        "clause_id": "WG510_2_time_generator_lock",
        "required_clause": "The generator tau is fixed once across source variation, exterior charge, and local readout.",
        "failure_mode": "time choice can absorb M_eff drift",
        "current_status": "open",
    },
    {
        "clause_id": "WG510_3_EH_local_fixed_point",
        "required_clause": "The exterior local fixed point reduces to EH at the charge/symplectic level, not just at the equation-shape level.",
        "failure_mode": "non-EH charge hair survives even if equations look GR-like",
        "current_status": "not_derived",
    },
    {
        "clause_id": "WG510_4_extra_sector_charge_silence",
        "required_clause": "Motion/time/domain/memory/range/boundary sectors carry zero independent Hamiltonian mass charge in the local exterior.",
        "failure_mode": "M_eff contains unowned extra source charge",
        "current_status": "conditional_from_506_not_field_specific",
    },
    {
        "clause_id": "WG510_5_projector_ownership",
        "required_clause": "Pi_M is the parent mass projector generated by the symplectic/constraint algebra, not an empirical selector.",
        "failure_mode": "the projector becomes a tunable mass calibration",
        "current_status": "open",
    },
    {
        "clause_id": "WG510_6_reference_zero_and_boundary",
        "required_clause": "The reference background, inner worldtube boundary, and outer linking surface have compatible boundary terms.",
        "failure_mode": "surface charge equality is shifted by reference/boundary bookkeeping",
        "current_status": "open",
    },
    {
        "clause_id": "WG510_7_dressed_source_definition",
        "required_clause": "M_source is defined as the dressed parent Hamiltonian/Noether charge, with bare matter mass treated as an input only after binding corrections are specified.",
        "failure_mode": "bare mass is falsely equated to measured gravitational mass",
        "current_status": "must_be_adopted_for_any_GR_style_branch",
    },
    {
        "clause_id": "WG510_8_PPN_metric_readout",
        "required_clause": "The charge appears in the weak-field metric with controlled beta/gamma/preferred-frame residuals.",
        "failure_mode": "source closure gives Newton-looking leading order while local GR still fails",
        "current_status": "not_derived",
    },
]

PROOF_SKETCH_ROWS = [
    {
        "step_id": "P510_0",
        "step": "Start with a diffeomorphism-invariant parent action S[phi] = integral L(phi) plus a source worldtube W.",
        "equation": "delta L = E_phi delta phi + d theta(phi,delta phi)",
        "dependency": "WG510_0",
        "status": "formal_reference_step",
    },
    {
        "step_id": "P510_1",
        "step": "Use a diffeomorphism generated by tau to define the Noether current.",
        "equation": "J_tau = theta(phi,L_tau phi) - tau dot L",
        "dependency": "WG510_0/WG510_2",
        "status": "formal_reference_step",
    },
    {
        "step_id": "P510_2",
        "step": "On shell, decompose the current into a surface charge plus constraints.",
        "equation": "J_tau = dQ_tau + C_tau",
        "dependency": "field equations and constraints",
        "status": "formal_reference_step",
    },
    {
        "step_id": "P510_3",
        "step": "Integrate between two linking surfaces around W.",
        "equation": "integral_S2 Q_tau - integral_S1 Q_tau = integral_A (J_tau - C_tau)",
        "dependency": "Stokes theorem and boundary orientation",
        "status": "formal_reference_step",
    },
    {
        "step_id": "P510_4",
        "step": "In a source-free EH exterior with no side flux, constraints vanish and the exterior charge is radially closed.",
        "equation": "C_tau=0 outside W; boundary flux=0 => Delta M=0",
        "dependency": "WG510_3/WG510_6",
        "status": "conditional_EH_step",
    },
    {
        "step_id": "P510_5",
        "step": "Pull the outer charge onto the worldtube definition of source mass.",
        "equation": "M_source[W] := H_tau[S_outer]-H_tau[reference]",
        "dependency": "WG510_7",
        "status": "definition_lock_required",
    },
    {
        "step_id": "P510_6",
        "step": "For MTS, add every possible difference between its parent charge and the EH charge as explicit Delta terms.",
        "equation": "Q_MTS_tau - Q_EH_tau = Delta_nonEH + Delta_symp + Delta_PiM + Delta_extra + Delta_frame",
        "dependency": "WG510_3/WG510_4/WG510_5",
        "status": "MTS_transfer_condition",
    },
    {
        "step_id": "P510_7",
        "step": "Only after charge closure, derive the weak-field metric readout and PPN residual vector.",
        "equation": "g_00=-1+2G_ref M_source/r+...; gamma,beta residuals explicit",
        "dependency": "WG510_8",
        "status": "not_yet_done",
    },
]

RESIDUAL_RUNNER_ROWS = [
    {
        "residual_id": "MR510_0_flux_leak",
        "equation": "dln_Meff_dt or epsilon_radial_Meff = integral_A d(Pi_M J_H) / M_eff",
        "zero_condition": "d(Pi_M J_H)=0 in source-free exterior",
        "observable_lock": "GMdot/Gdot, orbital radial mass drift",
        "required_input": "time/radial profile or theorem row closing d(Pi_M J_H)",
        "current_value": "missing",
        "claim_status": "blocks_local_GR",
    },
    {
        "residual_id": "MR510_1_nonEH_charge",
        "equation": "Delta_nonEH = integral_S (Q_MTS - Q_EH)_nonEH",
        "zero_condition": "local EH fixed point at symplectic charge level",
        "observable_lock": "PPN gamma/beta, fifth force, light bending",
        "required_input": "field-specific EH reduction or non-EH charge coefficient",
        "current_value": "missing",
        "claim_status": "blocks_local_GR",
    },
    {
        "residual_id": "MR510_2_symplectic_boundary",
        "equation": "Delta_symp = integral_boundary(delta Q - tau dot theta)_MTS-extra",
        "zero_condition": "boundary/reference terms cancel or are topological constants",
        "observable_lock": "absolute mass calibration, radial closure",
        "required_input": "boundary term ledger with reference zero",
        "current_value": "missing",
        "claim_status": "blocks_Newton_promotion",
    },
    {
        "residual_id": "MR510_3_projector_hair",
        "equation": "Delta_PiM = integral_S delta(Pi_M) J_H + Pi_M delta J_H",
        "zero_condition": "Pi_M fixed by parent algebra and source independent",
        "observable_lock": "source universality, PPN preferred-frame/projector effects",
        "required_input": "Pi_M parent algebra derivation",
        "current_value": "missing",
        "claim_status": "blocks_source_measure",
    },
    {
        "residual_id": "MR510_4_extra_sector_mass",
        "equation": "Delta_extra = Delta_motion + Delta_time + Delta_domain + Delta_memory + Delta_range + Delta_connection",
        "zero_condition": "extra sectors silent or pure gauge/topological in local exterior",
        "observable_lock": "local fifth-force, WEP, clocks, PPN",
        "required_input": "field-specific silence rows from 507 onward",
        "current_value": "missing",
        "claim_status": "blocks_local_GR",
    },
    {
        "residual_id": "MR510_5_frame_split",
        "equation": "Delta_frame = H_tau_source - H_tau_readout",
        "zero_condition": "one observed source/readout frame",
        "observable_lock": "WEP, clock comparison, preferred-frame PPN",
        "required_input": "same-frame matter coupling theorem",
        "current_value": "missing",
        "claim_status": "blocks_local_GR",
    },
    {
        "residual_id": "MR510_6_calibration_mismatch",
        "equation": "Delta_cal = M_orbit - M_source",
        "zero_condition": "Gauss/orbital readout derives inverse-square coefficient from parent charge",
        "observable_lock": "Kepler/Newton readout, absolute GM",
        "required_input": "metric readout theorem or calibration ledger",
        "current_value": "missing",
        "claim_status": "blocks_Newton_promotion",
    },
    {
        "residual_id": "MR510_7_PPN_tail",
        "equation": "Delta_PPN = {gamma-1, beta-1, alpha_i, zeta_i, xi}",
        "zero_condition": "second-order metric and conservation expansion matches GR within bounds",
        "observable_lock": "solar-system PPN tests",
        "required_input": "PPN expansion from parent action",
        "current_value": "missing",
        "claim_status": "blocks_local_GR",
    },
]

GATE_TEST_ROWS = [
    {
        "gate_id": "G510_0_EH_reference",
        "gate": "GR/EH has a known worldtube/noether surface-charge glue route",
        "result": "pass_conditional_reference",
        "evidence": "T510_0 proof sketch P510_0-P510_5",
    },
    {
        "gate_id": "G510_1_MTS_parent_inheritance",
        "gate": "current MTS parent action is proven to inherit the EH charge and source measure",
        "result": "fail_for_current_claim",
        "evidence": "WG510_3/WG510_4/WG510_5/WG510_8 remain open",
    },
    {
        "gate_id": "G510_2_bare_mass_guardrail",
        "gate": "bare matter mass is not falsely equated to measured gravitational source mass",
        "result": "pass",
        "evidence": "T510_1 and WG510_7 define M_source as dressed Hamiltonian/Noether charge",
    },
    {
        "gate_id": "G510_3_residual_runner",
        "gate": "all missing M_eff glue terms are represented as explicit residual rows",
        "result": "pass",
        "evidence": f"runner_rows={len(RESIDUAL_RUNNER_ROWS)}",
    },
    {
        "gate_id": "G510_4_local_GR_claim",
        "gate": "local GR/Newton/PPN is promoted",
        "result": "fail_blocked",
        "evidence": "requires 511 parent-action local-GR fixed-point ansatz plus PPN readout",
    },
]

DECISION_ROWS = [
    {
        "decision_id": "D510_0",
        "decision": "worldtube_glue_is_derivable_in_GR_style_parent_theory",
        "meaning": "the mathematical route is real; it is not a vague plateau axiom if the parent action has the right EH/symplectic fixed point",
        "claim_status": "conditional_reference",
    },
    {
        "decision_id": "D510_1",
        "decision": "current_MTS_does_not_yet_inherit_the_theorem",
        "meaning": "MTS needs an explicit parent-action fixed point that owns EH charge, Pi_M, source frame, extra-sector silence, and PPN readout",
        "claim_status": "local_GR_claim_false",
    },
    {
        "decision_id": "D510_2",
        "decision": "M_source_must_be_dressed_charge",
        "meaning": "use ADM/Hamiltonian/Noether-style source mass, not bare rest matter, or the source-measure equality is wrong before MTS even starts",
        "claim_status": "guardrail_adopted_for_branch",
    },
    {
        "decision_id": "D510_3",
        "decision": "next_step_is_minimal_parent_action_fixed_point",
        "meaning": "construct the smallest local parent action/limit that satisfies WG510 clauses or explicitly demote the local branch to residual closure-only",
        "claim_status": NEXT_TARGET,
    },
]

ROUTE_UPDATE_ROWS = [
    {
        "route_id": "RU510_0",
        "status": "GR_style_derivation_route_identified",
        "update": "worldtube source-measure glue is available as an EH/covariant-phase-space theorem route",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "RU510_1",
        "status": "MTS_transfer_premises_open",
        "update": "MTS must now build an EH-local fixed point at charge/symplectic/readout level, not merely assert a local plateau",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "RU510_2",
        "status": "residual_runner_ready",
        "update": "if parent-action transfer fails, MR510 residual rows become the closure-only local branch",
        "next_target": NEXT_TARGET,
    },
]


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in SOURCE_REGISTER:
        path = ROOT / item["source_file"]
        rows.append(
            {
                "source_file": item["source_file"],
                "role": item["role"],
                "exists": path.exists(),
            }
        )
    return rows


def validation_rows(sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in sources if row["exists"] != True]
    return [
        {
            "check_id": "V510_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V510_1_GR_reference_guarded",
            "result": "pass",
            "detail": "EH glue is marked reference/conditional, not current MTS proof",
        },
        {
            "check_id": "V510_2_bare_mass_guardrail",
            "result": "pass",
            "detail": "M_source defined as dressed Hamiltonian/Noether charge",
        },
        {
            "check_id": "V510_3_residual_runner_complete",
            "result": "pass",
            "detail": f"runner_rows={len(RESIDUAL_RUNNER_ROWS)}",
        },
        {
            "check_id": "V510_4_no_overclaim",
            "result": "pass",
            "detail": "MTS_worldtube_glue_derived=false; local_GR_claim_allowed=false",
        },
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    full_path = ROOT / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with full_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_run_csv(results_dir: Path, filename: str, rows: list[dict[str, Any]]) -> None:
    fieldnames = list(rows[0].keys())
    with (results_dir / filename).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    headers = list(rows[0].keys())
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        values = []
        for header in headers:
            value = str(row.get(header, "")).replace("\n", " ").replace("|", "\\|")
            values.append(value)
        output.append("| " + " | ".join(values) + " |")
    return "\n".join(output)


def build_doc(
    timestamp: str,
    generated_at_utc: str,
    run_dir: Path,
    sources: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> str:
    return f"""# 510 - Worldtube Source-Measure Glue or M_eff Residual Runner

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

This is the key local-GR lesson:

```text
The worldtube/source-mass glue is derivable in a GR/EH-style parent theory,
but current MTS has not yet shown that it inherits that theorem.
```

That is not grim. It is actually the cleanest possible narrowing.

The correct route is not a local plateau axiom. It is:

```text
diffeomorphism-invariant parent action
-> Noether/Hamiltonian charge for tau
-> surface charge equality between linking spheres
-> source mass defined as dressed parent charge
-> weak-field metric readout and PPN residual vector.
```

The important correction is that `M_source` must mean a dressed gravitational source charge. It cannot simply mean bare rest-matter mass. GR itself does not make that naive identification either.

## 2. Theorem Rows

{markdown_table(THEOREM_ROWS)}

## 3. Required Clauses

{markdown_table(CLAUSE_ROWS)}

## 4. Proof Sketch

{markdown_table(PROOF_SKETCH_ROWS)}

## 5. M_eff Residual Runner

{markdown_table(RESIDUAL_RUNNER_ROWS)}

## 6. Gate Tests

{markdown_table(GATE_TEST_ROWS)}

## 7. Decision

{markdown_table(DECISION_ROWS)}

## 8. Source Register

{markdown_table(sources)}

## 9. Validation

{markdown_table(validations)}

## 10. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 11. Claim Ceiling

Allowed:

```text
MTS has identified a real GR-style theorem route for local source-measure glue.
MTS now knows the exact parent-action clauses required to inherit it.
MTS has an explicit M_eff residual runner if the theorem route fails.
```

Forbidden:

```text
MTS has derived local GR.
MTS has derived Newtonian source normalization.
MTS has proved M_eff equals source mass in the current parent action.
MTS may equate bare rest mass with measured gravitational source mass.
```

## 12. Next Target

`{NEXT_TARGET}`

The next move is to build the smallest parent-action local fixed point that satisfies the worldtube clauses. If that cannot be made coherent, the local branch becomes residual closure-only rather than derived local GR.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-worldtube-source-measure-glue-or-Meff-residual-runner"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)

    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (THEOREM_PATH, THEOREM_ROWS),
        (CLAUSES_PATH, CLAUSE_ROWS),
        (PROOF_SKETCH_PATH, PROOF_SKETCH_ROWS),
        (RESIDUAL_RUNNER_PATH, RESIDUAL_RUNNER_ROWS),
        (GATE_TESTS_PATH, GATE_TEST_ROWS),
        (DECISION_PATH, DECISION_ROWS),
        (VALIDATION_PATH, validations),
        (ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS),
    ]

    for path, rows in csv_outputs:
        write_csv(path, rows)
        write_run_csv(results_dir, path.name, rows)

    doc = build_doc(args.timestamp, generated_at_utc, run_dir, sources, validations)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    missing_sources = [row["source_file"] for row in sources if row["exists"] != True]
    failed_validations = [row for row in validations if row["result"] == "fail"]
    status = {
        "timestamp": args.timestamp,
        "generated_at_utc": generated_at_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "theorem": str(ROOT / THEOREM_PATH),
        "clauses": str(ROOT / CLAUSES_PATH),
        "proof_sketch": str(ROOT / PROOF_SKETCH_PATH),
        "residual_runner": str(ROOT / RESIDUAL_RUNNER_PATH),
        "gate_tests": str(ROOT / GATE_TESTS_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "failed_validation_rows": len(failed_validations),
        "EH_worldtube_glue_known_conditional": True,
        "MTS_worldtube_glue_derived": False,
        "M_eff_must_be_ADM_dressed_charge": True,
        "bare_matter_mass_equality_allowed": False,
        "MTS_parent_EH_charge_fixed_point_derived": False,
        "PiM_projector_derived": False,
        "extra_sector_charge_silence_derived": False,
        "weak_field_metric_readout_derived": False,
        "M_eff_residual_runner_written": True,
        "source_normalized_Newton_promoted": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(
        f"{STATUS}\nnext={NEXT_TARGET}\nlocal_GR_claim_allowed=false\n",
        encoding="utf-8",
    )
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
