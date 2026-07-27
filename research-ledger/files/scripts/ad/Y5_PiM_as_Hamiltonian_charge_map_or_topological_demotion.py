from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_PiM_Hamiltonian_charge_map_candidate_written_topological_PiM_demoted_as_independent_proof"
CLAIM_CEILING = "PiM_Hamiltonian_charge_map_candidate_only_no_epsilon_charge_measured_GM_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "540-Y5-Hamiltonian-PiM-source-measure-and-PPN-readout-test.md"

DOC_PATH = Path("539-Y5-PiM-as-Hamiltonian-charge-map-or-topological-demotion.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_PIM_HAMILTONIAN_SOURCE_REGISTER.csv")
BRANCH_DEFINITION_PATH = Path("source-intake/mts_residuals/P8_Y5_PIM_HAMILTONIAN_BRANCH_DEFINITION.csv")
GATE_RESULTS_PATH = Path("source-intake/mts_residuals/P8_Y5_PIM_HAMILTONIAN_GATE_RESULTS.csv")
TOPOLOGICAL_DEMOTION_PATH = Path("source-intake/mts_residuals/P8_Y5_TOPOLOGICAL_PIM_DEMOTION_LEDGER.csv")
DAT537_REPAIR_STATUS_PATH = Path("source-intake/mts_residuals/P8_Y5_DAT537_REPAIR_STATUS.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_PIM_HAMILTONIAN_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_PIM_HAMILTONIAN_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_PIM_HAMILTONIAN_ROUTE_UPDATE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "538-Y5-minimal-parent-action-Euler-Ward-test-or-closure-demotion.md",
        "role": "isolates DAT537_4 Pi_M/Hilbert/Hamiltonian identification as blocker",
    },
    {
        "source_file": "537-Y5-Hilbert-worldtube-parent-action-contract-or-PiM-input-fill.md",
        "role": "parent-action contract and DAT537 chain",
    },
    {
        "source_file": "534-Y5-PiM-topological-equality-certificate-or-commutator-bound.md",
        "role": "topological Pi_M equality certificate and wrong-conserved-object warning",
    },
    {
        "source_file": "501-topological-Hilbert-current-equality-or-radial-bound-runner.md",
        "role": "topological-Hilbert equality attempt and Hamiltonian dictionary route",
    },
    {
        "source_file": "454-PiM-parent-symplectic-projector-algebra-attempt.md",
        "role": "conditional Pi_M projector algebra and variation debt",
    },
    {
        "source_file": "510-worldtube-source-measure-glue-or-Meff-residual-runner.md",
        "role": "dressed source charge and EH-style worldtube glue",
    },
    {
        "source_file": "505-parent-Noether-mass-charge-closure-theorem-or-closure-demotion.md",
        "role": "conditional Noether mass-charge closure theorem",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_DAT537_GATE_RESULTS.csv",
        "role": "538 DAT537 gate results",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_PIM_REPAIR_OR_DEMOTION_OPTIONS.csv",
        "role": "538 Pi_M repair/demotion options",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_PIM_INPUT_FILL_TEMPLATE.csv",
        "role": "537 residual input fill branch",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_TOPOLOGICAL_HILBERT_EQUALITY_ATTEMPT.csv",
        "role": "501 topological-Hilbert equality rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
        "role": "454 Pi_M symplectic projector algebra contract",
    },
    {
        "source_file": "scripts/Y5_PiM_as_Hamiltonian_charge_map_or_topological_demotion.py",
        "role": "this checkpoint generator",
    },
]


BRANCH_DEFINITION_ROWS = [
    {
        "branch_id": "PH539_0_charge_functional",
        "definition": "define the mass functional from the parent Hamiltonian/covariant-phase-space surface charge",
        "mathematical_form": "ell_H[J_H;tau,S] := 4*pi*G_ref int_S Q_tau[J_H]",
        "what_this_fixes": "the mass readout is tied to the parent action charge rather than a post-fit Pi_M mask",
        "what_remains_open": "integrability, reference subtraction, source measure, and PPN readout",
        "status": "candidate_definition_not_claim",
        "valid_for_claim": "false",
    },
    {
        "branch_id": "PH539_1_charge_representative",
        "definition": "represent the Hamiltonian mass charge as a parent-fixed mass cohomology representative",
        "mathematical_form": "Pi_M^H J_H := ell_H[J_H;tau,S] omega_M^H with int_S omega_M^H=1",
        "what_this_fixes": "Pi_M becomes a charge-map representative, not an independent conserved object",
        "what_remains_open": "pointwise equality to the old topological current is not proved",
        "status": "cohomology_level_repair_candidate",
        "valid_for_claim": "false",
    },
    {
        "branch_id": "PH539_2_DAT537_4_repair_scope",
        "definition": "repair DAT537_4 only at charge/integral level unless stronger equality is proved",
        "mathematical_form": "(4*pi*G_ref)^-1 int_S Pi_M^H J_H = int_S Q_tau by construction",
        "what_this_fixes": "avoids the conserved-wrong-object failure for measured source charge",
        "what_remains_open": "does not prove d(Pi_M J_H)=0 off shell or old Pi_M topological equality",
        "status": "repair_candidate_not_promotion",
        "valid_for_claim": "false",
    },
    {
        "branch_id": "PH539_3_no_independent_topological_credit",
        "definition": "old topological Pi_M earns no derivation credit unless it is shown to equal Pi_M^H",
        "mathematical_form": "Pi_M^top J_H - Pi_M^H J_H = R_Htop + dB_Htop",
        "what_this_fixes": "prevents the topological current from being counted as measured mass by name alone",
        "what_remains_open": "R_Htop and boundary flux must be zero or bounded",
        "status": "topological_route_demoted_until_equality",
        "valid_for_claim": "false",
    },
    {
        "branch_id": "PH539_4_residual_branch_preserved",
        "definition": "if Hamiltonian Pi_M cannot be adopted non-circularly, use residual fill rows",
        "mathematical_form": "epsilon_PiM_total_abs = |R_eq|/M_H + |I_commutator|/M_H + |B_zero_flux|/M_H + |T_PiM_beta|",
        "what_this_fixes": "keeps failure testable rather than rhetorical",
        "what_remains_open": "source-backed numeric or theorem rows are still missing",
        "status": "fallback_ready_not_filled",
        "valid_for_claim": "false",
    },
]


GATE_RESULT_ROWS = [
    {
        "gate_id": "HG539_0_parent_charge_integrability",
        "gate": "Hamiltonian surface charge Q_tau is integrable with fixed reference and boundary terms",
        "current_result": "not_yet_derived_for_current_MTS",
        "why_it_matters": "without integrability, ell_H is not a stable mass functional",
        "valid_for_claim": "false",
    },
    {
        "gate_id": "HG539_1_same_source_frame",
        "gate": "J_H is the observed matter/source current of the same frame used by clocks/orbits",
        "current_result": "open_from_537",
        "why_it_matters": "otherwise Hamiltonian charge and source mass can describe different frames",
        "valid_for_claim": "false",
    },
    {
        "gate_id": "HG539_2_cohomology_representative_fixed",
        "gate": "omega_M^H is fixed by parent topology/reference before readout",
        "current_result": "conditional_standard_branch_only",
        "why_it_matters": "otherwise Pi_M^H can still become a readout mask",
        "valid_for_claim": "false",
    },
    {
        "gate_id": "HG539_3_old_PiM_equivalence",
        "gate": "old/topological Pi_M equals the Hamiltonian Pi_M^H up to exact zero-flux terms",
        "current_result": "not_derived",
        "why_it_matters": "without this, old Pi_M is demoted as independent proof",
        "valid_for_claim": "false",
    },
    {
        "gate_id": "HG539_4_commutator_zero",
        "gate": "[d,Pi_M^H]J_H = 0 or its residual is source-backed and below locks",
        "current_result": "not_derived",
        "why_it_matters": "charge-map definition does not automatically remove projector/boundary residuals",
        "valid_for_claim": "false",
    },
    {
        "gate_id": "HG539_5_source_measure_glue",
        "gate": "worldtube source measure equals the Hamiltonian charge before orbital fitting",
        "current_result": "not_derived",
        "why_it_matters": "measured GM needs source-measure glue, not only a surface charge definition",
        "valid_for_claim": "false",
    },
    {
        "gate_id": "HG539_6_Gauss_PPN_readout",
        "gate": "the same charge controls the 1/r metric coefficient and second-order PPN vector",
        "current_result": "not_reached",
        "why_it_matters": "local GR requires readout through PPN order",
        "valid_for_claim": "false",
    },
]


TOPOLOGICAL_DEMOTION_ROWS = [
    {
        "old_route": "Pi_M^top as independent topological mass current",
        "old_claim_risk": "closed topological current may be a conserved wrong object",
        "new_status": "demoted_unless_equivalent_to_PiM_H",
        "repair_condition": "Pi_M^top J_H = Pi_M^H J_H + dB_zero with zero boundary flux",
        "fallback": "retain R_Htop/R_eq and commutator residual rows",
        "valid_for_claim": "false",
    },
    {
        "old_route": "Pi_M algebra idempotence",
        "old_claim_risk": "Pi_M^2=Pi_M can be mistaken for d(Pi_M J_H)=0",
        "new_status": "algebra_only_no_flux_closure",
        "repair_condition": "derive Ward/Euler closure of the Hamiltonian mass channel",
        "fallback": "source-backed I_commutator or radial mass-drift residual",
        "valid_for_claim": "false",
    },
    {
        "old_route": "Hodge/metric projector representative",
        "old_claim_risk": "metric-dependent projector variation can create hidden stress",
        "new_status": "retained_variation_debt",
        "repair_condition": "delta Pi_M stress is zero/topological or mapped below local locks",
        "fallback": "projector_stress_beta_equiv row",
        "valid_for_claim": "false",
    },
    {
        "old_route": "late equality multiplier",
        "old_claim_risk": "imposes source normalization by hand",
        "new_status": "forbidden_as_derivation",
        "repair_condition": "multiplier sector must have independent gauge/topological origin and zero stress",
        "fallback": "closure-only label",
        "valid_for_claim": "false",
    },
]


DAT537_REPAIR_ROWS = [
    {
        "dat537_id": "DAT537_4_PiM_Hilbert_identification",
        "before_539": "fail_for_current_MTS",
        "after_539": "candidate_repair_if_PiM_redefined_as_Hamiltonian_charge_map",
        "remaining_blocker": "adoption/integrability/source-measure/readout gates HG539_0 through HG539_6",
        "claim_status": "false",
    },
    {
        "dat537_id": "DAT537_5_local_readout",
        "before_539": "not_reached",
        "after_539": "still_not_reached",
        "remaining_blocker": "requires HG539_5 source-measure glue and HG539_6 Gauss/PPN readout",
        "claim_status": "false",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D539_0_Hamiltonian_PiM_candidate",
        "status": "PiM_Hamiltonian_charge_map_candidate_written",
        "meaning": "the clean repair is to make Pi_M the parent Hamiltonian charge representative rather than an independent selector",
        "claim_status": "candidate_only",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D539_1_topological_PiM_demoted",
        "status": "topological_PiM_not_independent_proof",
        "meaning": "old Pi_M/topological current must equal the Hamiltonian charge map or remain a residual branch",
        "claim_status": "no_epsilon_charge_credit",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D539_2_DAT537_4_not_closed_for_claim",
        "status": "DAT537_4_candidate_repair_not_claim",
        "meaning": "charge-level identity can be made by definition only if the branch is adopted and downstream gates pass",
        "claim_status": "local_GR_false",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D539_3_next_is_source_measure_and_PPN",
        "status": "source_measure_Gauss_PPN_still_required",
        "meaning": "even the repaired Pi_M branch must still prove measured GM and local readout",
        "claim_status": "Newton_false",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D539_4_private_no_push",
        "status": "private_no_github",
        "meaning": "no public/GitHub action is performed",
        "claim_status": "safe_private_work",
        "next_action": "continue_private_derivation",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "PIM_AS_SOURCE_CHARGE",
        "previous_status": "hard_blocker_now_isolated",
        "new_status": "Hamiltonian_charge_map_candidate_written",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "TOPOLOGICAL_PIM",
        "previous_status": "wrong_conserved_object_risk",
        "new_status": "demoted_unless_equivalent_to_Hamiltonian_PiM",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "DAT537_4",
        "previous_status": "fail_for_current_MTS",
        "new_status": "candidate_repair_not_claim",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_NORMALIZED_NEWTON",
        "previous_status": "still_blocked_by_DAT537_4",
        "new_status": "still_blocked_source_measure_and_Gauss_readout",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR",
        "previous_status": "still_blocked_PiM_charge_map_and_PPN_not_reached",
        "new_status": "still_blocked_PPN_readout_not_reached",
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
    dat537 = read_csv(Path("source-intake/mts_residuals/P8_Y5_DAT537_GATE_RESULTS.csv"))
    repair_options = read_csv(Path("source-intake/mts_residuals/P8_Y5_PIM_REPAIR_OR_DEMOTION_OPTIONS.csv"))
    old_topology = read_csv(Path("source-intake/mts_residuals/P8_TOPOLOGICAL_HILBERT_EQUALITY_ATTEMPT.csv"))
    old_projector = read_csv(Path("source-intake/mts_residuals/P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv"))
    claim_branch_rows = [row for row in BRANCH_DEFINITION_ROWS if row["valid_for_claim"] == "true"]
    claim_gate_rows = [row for row in GATE_RESULT_ROWS if row["valid_for_claim"] == "true"]
    claim_demotion_rows = [row for row in TOPOLOGICAL_DEMOTION_ROWS if row["valid_for_claim"] == "true"]
    return [
        {
            "check_id": "V539_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V539_1_prior_538_loaded",
            "result": "pass" if len(dat537) == 6 and len(repair_options) == 4 else "fail",
            "detail": f"dat537_rows={len(dat537)};repair_option_rows={len(repair_options)}",
        },
        {
            "check_id": "V539_2_old_topological_evidence_loaded",
            "result": "pass" if len(old_topology) >= 6 and len(old_projector) >= 8 else "fail",
            "detail": f"topological_rows={len(old_topology)};projector_contract_rows={len(old_projector)}",
        },
        {
            "check_id": "V539_3_branch_definition_complete",
            "result": "pass" if len(BRANCH_DEFINITION_ROWS) == 5 else "fail",
            "detail": f"branch_rows={len(BRANCH_DEFINITION_ROWS)}",
        },
        {
            "check_id": "V539_4_gate_results_complete",
            "result": "pass" if len(GATE_RESULT_ROWS) == 7 else "fail",
            "detail": f"gate_rows={len(GATE_RESULT_ROWS)}",
        },
        {
            "check_id": "V539_5_topological_demotion_explicit",
            "result": "pass" if len(TOPOLOGICAL_DEMOTION_ROWS) == 4 else "fail",
            "detail": f"demotion_rows={len(TOPOLOGICAL_DEMOTION_ROWS)}",
        },
        {
            "check_id": "V539_6_no_claim_rows",
            "result": "pass" if not claim_branch_rows and not claim_gate_rows and not claim_demotion_rows else "fail",
            "detail": f"claim_branch_rows={len(claim_branch_rows)};claim_gate_rows={len(claim_gate_rows)};claim_demotion_rows={len(claim_demotion_rows)}",
        },
        {
            "check_id": "V539_7_no_overclaim",
            "result": "pass" if not claim_branch_rows and not claim_gate_rows and not claim_demotion_rows else "fail",
            "detail": "PiM_Hamiltonian_branch_adopted=false; epsilon_charge_filled=false; measured_GM=false; Newton=false; PPN=false; local_GR=false",
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
    return f"""# 539 - Y5 PiM as Hamiltonian Charge Map or Topological Demotion

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

The clean repair is available as a candidate, but it is not a promotion.

The move is:

```text
Do not let Pi_M be an independent topological/readout selector.
Define Pi_M^H from the parent Hamiltonian surface charge itself.
Then the measured mass channel is tied to Q_tau by construction at charge level.
```

That repairs the "wrong conserved object" risk only if MTS adopts this Hamiltonian branch and then proves integrability, source-measure glue, zero residuals, and PPN readout.

The old topological `Pi_M` route is demoted as an independent proof unless it is shown to equal this Hamiltonian charge map.

## 2. Hamiltonian PiM Branch Definition

{markdown_table(BRANCH_DEFINITION_ROWS)}

## 3. Gate Results

{markdown_table(GATE_RESULT_ROWS)}

## 4. Topological PiM Demotion Ledger

{markdown_table(TOPOLOGICAL_DEMOTION_ROWS)}

## 5. DAT537 Repair Status

{markdown_table(DAT537_REPAIR_ROWS)}

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
MTS has a candidate Hamiltonian-charge-map definition of Pi_M.
The old topological Pi_M route is demoted unless it equals the Hamiltonian charge map.
DAT537_4 has a candidate repair path, not a completed proof.
```

Forbidden:

```text
MTS has adopted/proved the Hamiltonian Pi_M branch.
MTS has filled epsilon_charge.
MTS has derived measured GM, source-normalized Newton, beta, PPN, or local GR.
```

## 11. Practical Read

This is probably the right conceptual pivot. In GR-like mathematics the mass charge is not a free selector; it is the Hamiltonian/Noether charge. If MTS wants derived local GR, `Pi_M` should become that parent charge map. Any separate topological current can still be useful, but only as a representation of the same charge or as a bounded residual.

## 12. Next Target

`{NEXT_TARGET}`

Next: test the Hamiltonian `Pi_M^H` branch against source-measure glue and weak-field/PPN readout. If it cannot produce measured GM and the PPN vector, the repair remains only a cleaner notation.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Y5-PiM-as-Hamiltonian-charge-map-or-topological-demotion"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)
    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (BRANCH_DEFINITION_PATH, BRANCH_DEFINITION_ROWS),
        (GATE_RESULTS_PATH, GATE_RESULT_ROWS),
        (TOPOLOGICAL_DEMOTION_PATH, TOPOLOGICAL_DEMOTION_ROWS),
        (DAT537_REPAIR_STATUS_PATH, DAT537_REPAIR_ROWS),
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
        "branch_definition": str(ROOT / BRANCH_DEFINITION_PATH),
        "gate_results": str(ROOT / GATE_RESULTS_PATH),
        "topological_demotion": str(ROOT / TOPOLOGICAL_DEMOTION_PATH),
        "dat537_repair_status": str(ROOT / DAT537_REPAIR_STATUS_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "failed_validation_rows": len(failed_validations),
        "branch_definition_rows": len(BRANCH_DEFINITION_ROWS),
        "gate_rows": len(GATE_RESULT_ROWS),
        "topological_demotion_rows": len(TOPOLOGICAL_DEMOTION_ROWS),
        "PiM_Hamiltonian_charge_map_candidate_written": True,
        "PiM_Hamiltonian_branch_adopted_or_proved": False,
        "topological_PiM_demoted_as_independent_proof": True,
        "DAT537_4_candidate_repair_path": True,
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
        "done\nprivate_no_github\nPiM_Hamiltonian_candidate_only_no_measured_GM_Newton_PPN_or_local_GR_promotion\n",
        encoding="utf-8",
    )

    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
