from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_minimal_parent_action_Euler_Ward_test_passes_conditional_Noether_chain_but_fails_current_PiM_identification"
CLAIM_CEILING = "conditional_Euler_Ward_chain_only_no_PiM_Hilbert_glue_epsilon_charge_measured_GM_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "539-Y5-PiM-as-Hamiltonian-charge-map-or-topological-demotion.md"

DOC_PATH = Path("538-Y5-minimal-parent-action-Euler-Ward-test-or-closure-demotion.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_EULER_WARD_SOURCE_REGISTER.csv")
TEST_CASES_PATH = Path("source-intake/mts_residuals/P8_Y5_MINIMAL_PARENT_ACTION_TEST_CASES.csv")
CHAIN_TEST_PATH = Path("source-intake/mts_residuals/P8_Y5_EULER_WARD_CHAIN_TEST.csv")
DAT537_GATE_RESULTS_PATH = Path("source-intake/mts_residuals/P8_Y5_DAT537_GATE_RESULTS.csv")
PIM_REPAIR_OPTIONS_PATH = Path("source-intake/mts_residuals/P8_Y5_PIM_REPAIR_OR_DEMOTION_OPTIONS.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_EULER_WARD_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_EULER_WARD_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_EULER_WARD_ROUTE_UPDATE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "537-Y5-Hilbert-worldtube-parent-action-contract-or-PiM-input-fill.md",
        "role": "parent-action contract and DAT537 derivation attempt ledger",
    },
    {
        "source_file": "536-Y5-Hilbert-worldtube-glue-theorem-or-PiM-input-audit.md",
        "role": "Hilbert-worldtube glue theorem contract and Pi_M input audit",
    },
    {
        "source_file": "535-Y5-PiM-commutator-bound-runner-or-Hilbert-worldtube-glue.md",
        "role": "Pi_M equality/commutator runner and Hilbert-worldtube certificate",
    },
    {
        "source_file": "513-Gamma-Khat-q_loc-first-variation-or-demotion.md",
        "role": "q_loc rewritten as projected divergence of an effective stress",
    },
    {
        "source_file": "511-minimal-parent-action-local-GR-fixed-point-ansatz.md",
        "role": "minimal EH plus silent-sector local fixed-point ansatz",
    },
    {
        "source_file": "506-local-EH-reduction-and-extra-sector-silence-theorem.md",
        "role": "positive source-free operator and no-flux silence theorem",
    },
    {
        "source_file": "505-parent-Noether-mass-charge-closure-theorem-or-closure-demotion.md",
        "role": "conditional Noether mass-charge closure theorem",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_PARENT_ACTION_DERIVATION_ATTEMPT.csv",
        "role": "DAT537 chain to be tested",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv",
        "role": "PAC537 parent-action clauses",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_PARENT_ACTION_TO_HWT536_CLAUSE_MAP.csv",
        "role": "mapping from parent-action clauses to HWT536 theorem rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_PIM_INPUT_FILL_TEMPLATE.csv",
        "role": "parallel source-backed residual input fill template",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_PARENT_NOETHER_CLOSURE_DERIVATION_CHAIN.csv",
        "role": "conditional parent Noether closure chain",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_MTS_SYMBOL_FIRST_VARIATION_GATES.csv",
        "role": "first-variation gates including Gamma/Khat/q_loc and Pi_M",
    },
    {
        "source_file": "scripts/Y5_minimal_parent_action_Euler_Ward_test_or_closure_demotion.py",
        "role": "this checkpoint generator",
    },
]


TEST_CASE_ROWS = [
    {
        "case_id": "EW538_A_EH_silent_parent",
        "candidate_parent_action": "S_EH[g_obs] + S_matter[g_obs,psi] + S_silent[g_obs,Phi] + S_boundary",
        "what_it_can_derive": "covariant variation, Noether current, charge decomposition, radial Stokes equality, conditional EH weak-field charge",
        "what_it_cannot_derive_yet": "current independent Pi_M/topological current equals the Hamiltonian mass charge",
        "status": "conditional_pass_through_DAT537_3_fail_DAT537_4",
        "claim_status": "not_local_GR",
    },
    {
        "case_id": "EW538_B_constrained_PiM_topological_parent",
        "candidate_parent_action": "case A plus Lagrange/topological constraint enforcing Pi_M J_H - J_M_top - dB_zero = 0",
        "what_it_can_derive": "a formal equality if the constraint is accepted as parent structure",
        "what_it_cannot_derive_yet": "non-ad-hoc origin, zero projector stress, reference compatibility, and no hidden boundary charge",
        "status": "possible_repair_but_not_current_derivation",
        "claim_status": "constraint_only_not_claim",
    },
    {
        "case_id": "EW538_C_residual_bound_branch",
        "candidate_parent_action": "no Pi_M equality theorem; retain R_eq, I_commutator, B_zero_flux, projector_stress, Delta_extra, Delta_PPN as residual inputs",
        "what_it_can_derive": "honest bounded closure workflow if source-backed rows are supplied",
        "what_it_cannot_derive_yet": "exact local-GR/Newton promotion",
        "status": "fallback_if_DAT537_4_fails",
        "claim_status": "residual_branch_only",
    },
]


CHAIN_TEST_ROWS = [
    {
        "chain_id": "EW538_0_variation",
        "input_clause": "PAC537_0_covariant_parent_action",
        "test_equation": "delta L = E_A delta phi^A + dTheta",
        "minimal_parent_result": "conditional_pass_if_action_is_explicit",
        "current_MTS_result": "contract_only",
        "blocks_claim": "false",
    },
    {
        "chain_id": "EW538_1_Noether_current",
        "input_clause": "PAC537_0_covariant_parent_action;PAC537_1_single_observed_source_frame",
        "test_equation": "J_tau = Theta(phi,L_tau phi) - i_tau L",
        "minimal_parent_result": "conditional_pass_if_tau_and_source_frame_are_fixed",
        "current_MTS_result": "tau_source_readout_lock_still_open",
        "blocks_claim": "true",
    },
    {
        "chain_id": "EW538_2_charge_decomposition",
        "input_clause": "PAC537_3_local_EH_symplectic_fixed_point;PAC537_6_reference_and_boundary_zero",
        "test_equation": "J_tau = dQ_tau + C_tau; dQ_tau = C_EH + C_extra + C_projector + C_boundary",
        "minimal_parent_result": "conditional_pass_for_EH_plus_silent_exterior",
        "current_MTS_result": "C_extra_C_projector_C_boundary_not_zeroed",
        "blocks_claim": "true",
    },
    {
        "chain_id": "EW538_3_worldtube_Stokes_equality",
        "input_clause": "PAC537_2_parent_fixed_worldtube;PAC537_8_dressed_source_Gauss_readout",
        "test_equation": "int_S2 Q_tau - int_S1 Q_tau = int_A C_tau + boundary_flux",
        "minimal_parent_result": "mathematical_pass_once_Q_tau_and_W_source_are_defined",
        "current_MTS_result": "conditional_only_worldtube_charge_not_owned",
        "blocks_claim": "true",
    },
    {
        "chain_id": "EW538_4_PiM_Hilbert_identification",
        "input_clause": "PAC537_4_action_owned_PiM_projector;PAC537_5_Hilbert_topological_charge_equality",
        "test_equation": "(4*pi*G_ref)^-1 int_S Pi_M J_H = int_S Q_tau",
        "minimal_parent_result": "fails_unless_Pi_M_is_defined_as_Hamiltonian_charge_map_or_constraint_owned",
        "current_MTS_result": "not_derived_no_claim_valid_input_rows",
        "blocks_claim": "true",
    },
    {
        "chain_id": "EW538_5_local_readout",
        "input_clause": "PAC537_8_dressed_source_Gauss_readout;PAC537_9_second_order_PPN_stability",
        "test_equation": "g_00=-1+2G_ref M_source/r+O(r^-2); Delta_PPN explicit",
        "minimal_parent_result": "not_reached_until_EW538_4_closes",
        "current_MTS_result": "not_reached",
        "blocks_claim": "true",
    },
]


DAT537_GATE_ROWS = [
    {
        "dat537_id": "DAT537_0_variation",
        "538_result": "conditional_pass",
        "basis": "a covariant parent action would provide Euler variation and symplectic potential",
        "current_claim": "false",
        "next_requirement": "write the explicit MTS local parent Lagrangian terms",
    },
    {
        "dat537_id": "DAT537_1_Noether_current",
        "538_result": "conditional_pass_with_open_tau_lock",
        "basis": "Noether current exists if tau and source/readout frame are fixed once",
        "current_claim": "false",
        "next_requirement": "derive same observed source/readout time generator",
    },
    {
        "dat537_id": "DAT537_2_charge_decomposition",
        "538_result": "conditional_pass_with_open_C_terms",
        "basis": "EH plus silent/topological sectors give charge plus constraint decomposition",
        "current_claim": "false",
        "next_requirement": "zero or bound C_extra, C_projector, C_boundary",
    },
    {
        "dat537_id": "DAT537_3_worldtube_Stokes_equality",
        "538_result": "mathematical_pass_once_Q_tau_is_owned",
        "basis": "Stokes theorem works for linked surfaces after Q_tau and W_source are fixed",
        "current_claim": "false",
        "next_requirement": "define M_source as dressed parent charge before orbital fitting",
    },
    {
        "dat537_id": "DAT537_4_PiM_Hilbert_identification",
        "538_result": "fail_for_current_MTS",
        "basis": "the minimal EH parent action does not automatically make the existing Pi_M/topological current equal the Hamiltonian charge",
        "current_claim": "false",
        "next_requirement": "derive Pi_M as Hamiltonian charge map or demote topological Pi_M route",
    },
    {
        "dat537_id": "DAT537_5_local_readout",
        "538_result": "not_reached",
        "basis": "PPN/readout must wait until DAT537_4 source-charge equality closes",
        "current_claim": "false",
        "next_requirement": "after Pi_M closure, derive weak-field metric and PPN vector",
    },
]


PIM_REPAIR_OPTION_ROWS = [
    {
        "option_id": "PRO538_0_define_PiM_as_Hamiltonian_charge_map",
        "proposal": "replace independent Pi_M mass selector with the parent Hamiltonian/covariant-phase-space mass charge map",
        "mathematical_form": "Pi_M J_H := 4*pi*G_ref dQ_tau on the local fixed-point branch, with residuals named off branch",
        "cost": "Pi_M becomes derived/readout infrastructure, not an independent topological proof",
        "benefit": "DAT537_4 can become definitional from the parent charge rather than a separate equality miracle",
        "status": "best_next_derivation_target",
        "valid_for_claim": "false",
    },
    {
        "option_id": "PRO538_1_topological_constraint_parent",
        "proposal": "add a parent constraint forcing Pi_M J_H to match a closed topological representative",
        "mathematical_form": "S_constraint = int lambda wedge (Pi_M J_H - J_M_top - dB_zero)",
        "cost": "risks being a disguised closure axiom unless lambda sector has zero stress and non-ad-hoc origin",
        "benefit": "keeps original topological-current language if all integrability/boundary gates pass",
        "status": "possible_but_high_risk",
        "valid_for_claim": "false",
    },
    {
        "option_id": "PRO538_2_residual_fill_branch",
        "proposal": "accept DAT537_4 failure and use source-backed residual rows",
        "mathematical_form": "epsilon_PiM_total_abs = |R_eq|/M_H + |I_commutator|/M_H + |B_zero_flux|/M_H + |T_PiM_beta|",
        "cost": "local-GR branch becomes bounded residual/closure rather than exact derivation",
        "benefit": "honest, testable, and prevents hidden calibration",
        "status": "fallback_ready",
        "valid_for_claim": "false",
    },
    {
        "option_id": "PRO538_3_no_action_no_claim",
        "proposal": "if neither parent map nor source-backed residuals can be supplied, demote local transition route",
        "mathematical_form": "DAT537_4 unresolved => epsilon_charge=false and local_GR_claim_allowed=false",
        "cost": "cannot claim derived local Newton/GR from this branch",
        "benefit": "keeps theory discipline and avoids overclaim",
        "status": "guardrail",
        "valid_for_claim": "false",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D538_0_Euler_Ward_partial_pass",
        "status": "DAT537_0_to_DAT537_3_conditionally_pass",
        "meaning": "the minimal EH plus silent-sector parent shape can carry the standard Noether/Stokes charge route",
        "claim_status": "conditional_only",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D538_1_PiM_identification_fails_current_claim",
        "status": "DAT537_4_fails_for_current_MTS",
        "meaning": "existing Pi_M/topological-current language is not yet derived as the Hamiltonian source charge",
        "claim_status": "epsilon_charge_false",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D538_2_best_repair",
        "status": "derive_PiM_as_Hamiltonian_charge_map_or_demote",
        "meaning": "the clean repair is to make Pi_M the parent charge map, otherwise use residual input rows",
        "claim_status": "active_private_derivation",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D538_3_no_PPN_readout_yet",
        "status": "DAT537_5_not_reached",
        "meaning": "weak-field and PPN derivation waits until source-charge equality closes",
        "claim_status": "local_GR_false",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D538_4_private_no_push",
        "status": "private_no_github",
        "meaning": "no public/GitHub action is performed",
        "claim_status": "safe_private_work",
        "next_action": "continue_private_derivation",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "EULER_WARD_CHAIN",
        "previous_status": "next_required_test",
        "new_status": "conditional_pass_until_PiM_identification",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "PIM_AS_SOURCE_CHARGE",
        "previous_status": "not_derived",
        "new_status": "hard_blocker_now_isolated",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "PIM_INPUT_FILL",
        "previous_status": "source_backed_fill_template_written",
        "new_status": "fallback_if_Hamiltonian_charge_map_fails",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_NORMALIZED_NEWTON",
        "previous_status": "blocked_until_parent_action_or_input_fill_closes",
        "new_status": "still_blocked_by_DAT537_4",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR",
        "previous_status": "blocked_until_Euler_Ward_charge_glue_and_PPN_readout",
        "new_status": "still_blocked_PiM_charge_map_and_PPN_not_reached",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
]


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    full_path = ROOT / path
    if not full_path.exists():
        return []
    with full_path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in SOURCE_REGISTER:
        full_path = ROOT / item["source_file"]
        rows.append({**item, "exists": full_path.exists()})
    return rows


def validation_rows(sources: list[dict[str, Any]]) -> list[dict[str, str]]:
    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
    dat537_rows = read_csv(Path("source-intake/mts_residuals/P8_Y5_PARENT_ACTION_DERIVATION_ATTEMPT.csv"))
    dat537_ids = {row.get("attempt_id", "") for row in dat537_rows}
    mapped_ids = {row["dat537_id"] for row in DAT537_GATE_ROWS}
    missing_dat537 = dat537_ids - mapped_ids
    claim_gate_rows = [row for row in DAT537_GATE_ROWS if row["current_claim"] == "true"]
    claim_repair_rows = [row for row in PIM_REPAIR_OPTION_ROWS if row["valid_for_claim"] == "true"]
    dat537_4 = [row for row in DAT537_GATE_ROWS if row["dat537_id"] == "DAT537_4_PiM_Hilbert_identification"]
    dat537_5 = [row for row in DAT537_GATE_ROWS if row["dat537_id"] == "DAT537_5_local_readout"]
    return [
        {
            "check_id": "V538_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V538_1_DAT537_rows_loaded",
            "result": "pass" if len(dat537_rows) == 6 else "fail",
            "detail": f"dat537_rows={len(dat537_rows)}",
        },
        {
            "check_id": "V538_2_all_DAT537_rows_tested",
            "result": "pass" if not missing_dat537 and len(mapped_ids) == 6 else "fail",
            "detail": f"mapped_rows={len(mapped_ids)};missing_dat537={len(missing_dat537)}",
        },
        {
            "check_id": "V538_3_test_cases_complete",
            "result": "pass" if len(TEST_CASE_ROWS) == 3 and len(CHAIN_TEST_ROWS) == 6 else "fail",
            "detail": f"test_cases={len(TEST_CASE_ROWS)};chain_rows={len(CHAIN_TEST_ROWS)}",
        },
        {
            "check_id": "V538_4_DAT537_4_correctly_blocks",
            "result": "pass" if dat537_4 and dat537_4[0]["538_result"] == "fail_for_current_MTS" else "fail",
            "detail": dat537_4[0]["basis"] if dat537_4 else "DAT537_4_missing",
        },
        {
            "check_id": "V538_5_DAT537_5_not_reached",
            "result": "pass" if dat537_5 and dat537_5[0]["538_result"] == "not_reached" else "fail",
            "detail": dat537_5[0]["basis"] if dat537_5 else "DAT537_5_missing",
        },
        {
            "check_id": "V538_6_no_claim_rows",
            "result": "pass" if not claim_gate_rows and not claim_repair_rows else "fail",
            "detail": f"claim_gate_rows={len(claim_gate_rows)};claim_repair_rows={len(claim_repair_rows)}",
        },
        {
            "check_id": "V538_7_no_overclaim",
            "result": "pass" if not claim_gate_rows and not claim_repair_rows else "fail",
            "detail": "PiM_Hilbert_identification_derived=false; epsilon_charge_filled=false; measured_GM=false; Newton=false; PPN=false; local_GR=false",
        },
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    full_path = ROOT / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with full_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_run_csv(results_dir: Path, filename: str, rows: list[dict[str, Any]]) -> None:
    fieldnames = list(rows[0].keys()) if rows else []
    with (results_dir / filename).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_doc(
    generated_at_utc: str,
    run_dir: Path,
    sources: list[dict[str, Any]],
    validations: list[dict[str, str]],
) -> str:
    return f"""# 538 - Y5 Minimal Parent Action Euler-Ward Test or Closure Demotion

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

This is a useful partial win, with one hard failure left exposed.

The minimal EH-plus-silent parent shape can carry the standard derivation chain:

```text
covariant action
-> Euler variation and symplectic potential
-> Noether current
-> surface charge plus constraints
-> Stokes equality between linked worldtube surfaces.
```

But current MTS still fails the crucial identification:

```text
(4*pi*G_ref)^-1 int_S Pi_M J_H = int_S Q_tau.
```

That means the route is not dead, but it is not local GR. The next honest move is to derive `Pi_M` as the Hamiltonian charge map, or demote the topological `Pi_M` route to residual input fill.

## 2. Minimal Parent-Action Test Cases

{markdown_table(TEST_CASE_ROWS)}

## 3. Euler-Ward Chain Test

{markdown_table(CHAIN_TEST_ROWS)}

## 4. DAT537 Gate Results

{markdown_table(DAT537_GATE_ROWS)}

## 5. PiM Repair or Demotion Options

{markdown_table(PIM_REPAIR_OPTION_ROWS)}

## 6. Decision

{markdown_table(DECISION_ROWS)}

## 7. Source Register

{markdown_table(sources)}

## 8. Validation

{markdown_table(validations)}

## 9. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 10. Claim Ceiling

Allowed:

```text
MTS has a conditional Euler/Ward/Noether chain through the worldtube Stokes step.
The exact current blocker is DAT537_4: Pi_M Hilbert current must equal the Hamiltonian mass charge.
```

Forbidden:

```text
MTS has derived Pi_M Hilbert-worldtube glue.
MTS has filled epsilon_charge.
MTS has derived measured GM, source-normalized Newton, beta, PPN, or local GR.
```

## 11. Practical Read

This is a good narrowing. The path through GR-like mathematics is not fantasy: the Noether/Stokes machinery is structurally available. The problem is that `Pi_M` cannot remain both an independent selector and magically the Hamiltonian source charge. It must be derived as that charge map, constrained by a non-ad-hoc parent sector, or demoted to a residual runner.

## 12. Next Target

`{NEXT_TARGET}`

Next: try the clean repair first: define or derive `Pi_M` as the parent Hamiltonian/covariant-phase-space mass charge map. If that cannot be made non-circular, topological `Pi_M` becomes a residual route rather than a derivation route.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Y5-minimal-parent-action-Euler-Ward-test-or-closure-demotion"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)
    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (TEST_CASES_PATH, TEST_CASE_ROWS),
        (CHAIN_TEST_PATH, CHAIN_TEST_ROWS),
        (DAT537_GATE_RESULTS_PATH, DAT537_GATE_ROWS),
        (PIM_REPAIR_OPTIONS_PATH, PIM_REPAIR_OPTION_ROWS),
        (DECISION_PATH, DECISION_ROWS),
        (VALIDATION_PATH, validations),
        (ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS),
    ]

    for path, rows in csv_outputs:
        write_csv(path, rows)
        write_run_csv(results_dir, path.name, rows)

    doc = build_doc(generated_at_utc, run_dir, sources, validations)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
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
        "test_cases": str(ROOT / TEST_CASES_PATH),
        "chain_test": str(ROOT / CHAIN_TEST_PATH),
        "dat537_gate_results": str(ROOT / DAT537_GATE_RESULTS_PATH),
        "pim_repair_options": str(ROOT / PIM_REPAIR_OPTIONS_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "failed_validation_rows": len(failed_validations),
        "test_case_rows": len(TEST_CASE_ROWS),
        "chain_test_rows": len(CHAIN_TEST_ROWS),
        "dat537_gate_rows": len(DAT537_GATE_ROWS),
        "PiM_Hilbert_identification_derived": False,
        "Euler_Ward_chain_conditional_pass_to_Stokes": True,
        "DAT537_4_blocks_current_claim": True,
        "epsilon_charge_filled": False,
        "measured_GM_derived": False,
        "source_normalized_Newton_derived": False,
        "beta_equals_one_derived": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "github_push_performed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(
        "done\nprivate_no_github\nconditional_Euler_Ward_only_no_PiM_Hilbert_glue_or_local_GR_promotion\n",
        encoding="utf-8",
    )

    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
