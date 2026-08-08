from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_boundary_reference_minimal_sufficient_contract_written_not_parent_owned_residual_retained"
CLAIM_CEILING = "conditional_boundary_reference_zero_contract_only_no_source_measure_measured_GM_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "546-Y5-parent-action-boundary-reference-clause-search-or-residual-score.md"

DOC_PATH = Path("545-Y5-boundary-reference-minimal-action-clause-or-residual-row.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_545_SOURCE_REGISTER.csv")
MINIMAL_ACTION_CONTRACT_PATH = Path("source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_MINIMAL_ACTION_CONTRACT.csv")
CONDITIONAL_THEOREM_CHAIN_PATH = Path("source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_CONDITIONAL_THEOREM_CHAIN.csv")
PARENT_OWNERSHIP_AUDIT_PATH = Path("source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_PARENT_OWNERSHIP_AUDIT.csv")
RESIDUAL_ROW_PATH = Path("source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_RESIDUAL_ROW.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_545_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_545_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_545_ROUTE_UPDATE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "544-Y5-boundary-reference-first-row-data-or-theorem-zero.md",
        "role": "corpus data/theorem-zero audit showing no claim-valid first-row evidence",
    },
    {
        "source_file": "543-Y5-boundary-reference-residual-theorem-or-fill-first-row.md",
        "role": "boundary/reference zero theorem attempt and first residual fill pack",
    },
    {
        "source_file": "542-Y5-source-measure-theorem-attempt-or-first-residual-fill.md",
        "role": "source-measure theorem attempt and first residual evaluator",
    },
    {
        "source_file": "510-worldtube-source-measure-glue-or-Meff-residual-runner.md",
        "role": "worldtube source-measure glue and M_eff residual runner",
    },
    {
        "source_file": "486-R11-boundary-stress-theorem-or-closure-fill-pack.md",
        "role": "boundary/R11 stress theorem stack and closure fill pack",
    },
    {
        "source_file": "485-boundary-no-flux-and-R11-silence-from-local-zero.md",
        "role": "boundary no-flux shortcut rejection",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_DATA_SOURCE_AUDIT.csv",
        "role": "544 data source audit",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_THEOREM_ZERO_AUDIT.csv",
        "role": "544 theorem-zero audit",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv",
        "role": "544 first-row status",
    },
    {
        "source_file": "scripts/Y5_boundary_reference_minimal_action_clause_or_residual_row.py",
        "role": "this checkpoint generator",
    },
]


MINIMAL_ACTION_CONTRACT_ROWS = [
    {
        "clause_id": "MAC545_0_covariant_parent_action",
        "minimal_clause": "parent action is diffeomorphism-covariant and supplies the charge/symplectic form before readout",
        "mathematical_form": "S_parent=int_M L[g,fields]+int_dM B_ref; delta L=E_A delta phi^A+dTheta; J_tau=Theta(phi,L_tau phi)-i_tau L",
        "needed_to_zero": "defines Delta_symp and B_zero_flux as derived charge terms instead of names",
        "current_corpus_status": "Noether template exists but explicit parent L and boundary term are not fixed",
        "parent_owned_now": "false",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "MAC545_1_exterior_annulus_vacuum",
        "minimal_clause": "compact local branch has an exterior annulus A between S_inner and S_outer with no source support",
        "mathematical_form": "supp(J_source) cap A=empty; E_A=0 in A; dJ_tau=0 up to listed C terms",
        "needed_to_zero": "lets Stokes/Gauss arguments compare the two linked surfaces",
        "current_corpus_status": "worldtube setup allowed, but all extra C terms are not closed",
        "parent_owned_now": "partial_setup_only",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "MAC545_2_reference_lock",
        "minimal_clause": "Hamiltonian reference subtraction is fixed, universal, and independent of source/surface/frame",
        "mathematical_form": "partial_t Delta_ref=partial_r Delta_ref=partial_source Delta_ref=partial_frame Delta_ref=0",
        "needed_to_zero": "kills source-dependent Delta_symp_ref and absolute monopole drift",
        "current_corpus_status": "reference choice remains a contract, not a parent result",
        "parent_owned_now": "false",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "MAC545_3_boundary_exact_cohomology_zero",
        "minimal_clause": "exact/improvement boundary form is cohomologically trivial on the linking annulus",
        "mathematical_form": "B_imp=dC with int_S2 B_imp-int_S1 B_imp=int_A dB_imp=0",
        "needed_to_zero": "sets B_zero_flux=0 rather than assuming exact terms cannot carry finite charges",
        "current_corpus_status": "current corpus warns exact/topological labels alone are not enough",
        "parent_owned_now": "false",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "MAC545_4_boundary_no_vector_tensor_hair",
        "minimal_clause": "boundary variation carries only source-independent scalar trace or vanishes",
        "mathematical_form": "n_mu P_loc_nu T_B^{mu nu}=0; T_B^{TF}=0; T_B^{vector}=0; partial_t,r,frame T_B=0",
        "needed_to_zero": "prevents alpha_i/xi/source-normalization hair from re-entering through the boundary",
        "current_corpus_status": "scalar no-flux lemma is conditional and not parent-owned",
        "parent_owned_now": "false",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "MAC545_5_projector_symplectic_silence",
        "minimal_clause": "mass projector is parent-fixed and covariantly constant in the exterior annulus",
        "mathematical_form": "nabla Pi_M=0; delta Pi_M=0 or exact topological cancellation; delta(Pi_M J_H)=Pi_M delta J_H",
        "needed_to_zero": "prevents projector variation stress from shifting Delta_symp or M_H_ref",
        "current_corpus_status": "Pi_M projector variation/stress remains retained",
        "parent_owned_now": "false",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "MAC545_6_positive_measured_denominator",
        "minimal_clause": "M_H_ref is positive and tied to the same measured-GM normalization used by the orbital readout",
        "mathematical_form": "M_H_ref>0 and G M_H_ref = GM_orbit in the same observed frame",
        "needed_to_zero": "makes epsilon_boundary_reference_abs well-defined and prevents denominator/readout cheating",
        "current_corpus_status": "Hilbert monopole and Poisson/Gauss calibration contracts remain conditional",
        "parent_owned_now": "false",
        "valid_for_claim": "false",
    },
]


CONDITIONAL_THEOREM_CHAIN_ROWS = [
    {
        "step_id": "CT545_0_define_charge_residual",
        "claim": "boundary/reference residual is the difference of derived charge/symplectic data between S_inner and S_outer",
        "mathematical_step": "epsilon_BR=(abs(B_zero_flux)+abs(Delta_symp))/M_H_ref",
        "requires_contract_clauses": "MAC545_0;MAC545_6",
        "result_if_premises_owned": "residual is a derived observable gate",
        "current_status": "definition_allowed_not_claim_filled",
        "valid_for_claim": "false",
    },
    {
        "step_id": "CT545_1_annulus_stokes",
        "claim": "if the exterior annulus has no source support and all C terms vanish, linked surface charge difference is zero",
        "mathematical_step": "int_S2 q_tau-int_S1 q_tau=int_A dq_tau=0",
        "requires_contract_clauses": "MAC545_1",
        "result_if_premises_owned": "no radial charge drift from the bulk",
        "current_status": "conditional_C_terms_not_closed",
        "valid_for_claim": "false",
    },
    {
        "step_id": "CT545_2_boundary_flux_zero",
        "claim": "if the improvement form is exact and cohomologically trivial, the boundary flux numerator vanishes",
        "mathematical_step": "B_zero_flux=int_S2 B_imp-int_S1 B_imp=int_A dB_imp=0",
        "requires_contract_clauses": "MAC545_3;MAC545_4",
        "result_if_premises_owned": "B_zero_flux=0",
        "current_status": "conditional_not_parent_owned",
        "valid_for_claim": "false",
    },
    {
        "step_id": "CT545_3_reference_symplectic_zero",
        "claim": "if the reference is locked and the exterior symplectic flux has no projector stress, Delta_symp vanishes",
        "mathematical_step": "Delta_symp=int_dA(omega_extra+omega_ref+omega_PiM)=0",
        "requires_contract_clauses": "MAC545_2;MAC545_5",
        "result_if_premises_owned": "Delta_symp=0",
        "current_status": "conditional_not_parent_owned",
        "valid_for_claim": "false",
    },
    {
        "step_id": "CT545_4_denominator_safe",
        "claim": "if the Hilbert/source denominator is same-frame measured mass, the zero numerator has a physical normalization",
        "mathematical_step": "M_H_ref>0 and tied to GM_orbit",
        "requires_contract_clauses": "MAC545_6",
        "result_if_premises_owned": "epsilon_BR is physical rather than a gauge ratio",
        "current_status": "conditional_GM_calibration_open",
        "valid_for_claim": "false",
    },
    {
        "step_id": "CT545_5_conditional_plateau",
        "claim": "under all MAC545 clauses, the first residual row vanishes without adding a plateau axiom",
        "mathematical_step": "B_zero_flux=0 and Delta_symp=0 imply epsilon_boundary_reference_abs=0",
        "requires_contract_clauses": "MAC545_0;MAC545_1;MAC545_2;MAC545_3;MAC545_4;MAC545_5;MAC545_6",
        "result_if_premises_owned": "boundary/reference part of source-measure gate closes",
        "current_status": "sufficient_theorem_only_not_current_claim",
        "valid_for_claim": "false",
    },
]


PARENT_OWNERSHIP_AUDIT_ROWS = [
    {
        "ownership_id": "POA545_0_parent_action",
        "contract_clause": "MAC545_0_covariant_parent_action",
        "current_evidence": "Noether/Ward templates exist, but no fixed parent Lagrangian and boundary Theta/B_ref for the current branch",
        "owned_by_current_corpus": "false",
        "repair": "write parent action clause and variation ledger",
        "valid_for_claim": "false",
    },
    {
        "ownership_id": "POA545_1_C_terms",
        "contract_clause": "MAC545_1_exterior_annulus_vacuum",
        "current_evidence": "worldtube annulus setup exists, but C_extra, C_projector, C_boundary, and source normalization remain open",
        "owned_by_current_corpus": "false",
        "repair": "derive exterior C-term silence or keep residuals",
        "valid_for_claim": "false",
    },
    {
        "ownership_id": "POA545_2_reference",
        "contract_clause": "MAC545_2_reference_lock",
        "current_evidence": "544 found no claim-valid reference-lock row and 543 rejects reference-only zero as MTS evidence",
        "owned_by_current_corpus": "false",
        "repair": "derive reference independence from action normalization",
        "valid_for_claim": "false",
    },
    {
        "ownership_id": "POA545_3_boundary",
        "contract_clause": "MAC545_3_boundary_exact_cohomology_zero;MAC545_4_boundary_no_vector_tensor_hair",
        "current_evidence": "boundary scalar/no-flux statements are conditional and do not kill vector/tensor hair by themselves",
        "owned_by_current_corpus": "false",
        "repair": "prove scalar homogeneous marker-free boundary class from parent dynamics",
        "valid_for_claim": "false",
    },
    {
        "ownership_id": "POA545_4_projector",
        "contract_clause": "MAC545_5_projector_symplectic_silence",
        "current_evidence": "projector variation stress remains retained in Pi_M audits",
        "owned_by_current_corpus": "false",
        "repair": "derive Pi_M as topological/covariantly constant charge data",
        "valid_for_claim": "false",
    },
    {
        "ownership_id": "POA545_5_denominator",
        "contract_clause": "MAC545_6_positive_measured_denominator",
        "current_evidence": "Hilbert monopole and Poisson/Gauss calibration contracts are conditional, not measured-GM proofs",
        "owned_by_current_corpus": "false",
        "repair": "derive same-frame GM_orbit = G M_H_ref",
        "valid_for_claim": "false",
    },
]


RESIDUAL_ROW = [
    {
        "system_id": "MTS_Hamiltonian_PiM_local_branch",
        "residual_id": "BRR545_0_boundary_reference_retained",
        "formula": "epsilon_boundary_reference_abs=(abs(B_zero_flux)+abs(Delta_symp))/M_H_ref",
        "B_zero_flux_status": "missing_theorem_or_source_value",
        "Delta_symp_status": "missing_theorem_or_source_value",
        "M_H_ref_status": "missing_same_frame_measured_GM_denominator",
        "current_value": "",
        "units": "dimensionless_after_dividing_by_M_H_ref",
        "source_file": "545-Y5-boundary-reference-minimal-action-clause-or-residual-row.md",
        "derivation_status": "retained_residual_until_MAC545_clauses_parent_owned",
        "valid_for_claim": "false",
    }
]


DECISION_ROWS = [
    {
        "decision_id": "D545_0_conditional_sufficient_theorem_written",
        "status": "minimal_sufficient_contract_written",
        "meaning": "a precise set of clauses would derive B_zero_flux=Delta_symp=0 without a plateau axiom",
        "claim_status": "conditional_only",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D545_1_not_parent_owned",
        "status": "current_corpus_does_not_own_the_contract",
        "meaning": "the clauses are sufficient but not yet derived from the current parent action",
        "claim_status": "boundary_reference_zero_not_derived",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D545_2_residual_retained",
        "status": "epsilon_boundary_reference_abs_retained_as_explicit_residual",
        "meaning": "the first row is no longer hidden; it remains a visible gate until derived or filled",
        "claim_status": "source_measure_false",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D545_3_private_no_push",
        "status": "private_no_github",
        "meaning": "no public/GitHub action is performed",
        "claim_status": "safe_private_work",
        "next_action": "continue_private_derivation",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "BOUNDARY_REFERENCE_ZERO",
        "previous_status": "data_and_theorem_audit_done_no_claim_value_found",
        "new_status": "minimal_sufficient_contract_written_not_parent_owned",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_MEASURE_THEOREM",
        "previous_status": "still_blocked_first_row_unfilled",
        "new_status": "still_blocked_until_MAC545_parent_ownership_or_residual_bound",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_NORMALIZED_NEWTON",
        "previous_status": "still_blocked_boundary_reference_and_GM_denominator_missing",
        "new_status": "still_blocked_by_denominator_and_boundary_reference_contract",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR",
        "previous_status": "still_blocked_no_boundary_reference_parent_zero",
        "new_status": "still_blocked_but_exact_parent_action_target_identified",
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
    prior_validation = read_csv(Path("source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_544_VALIDATION.csv"))
    prior_data_audit = read_csv(Path("source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_DATA_SOURCE_AUDIT.csv"))
    prior_theorem_audit = read_csv(Path("source-intake/mts_residuals/P8_Y5_BOUNDARY_REFERENCE_THEOREM_ZERO_AUDIT.csv"))
    prior_fails = [row for row in prior_validation if row.get("result") == "fail"]
    owned_rows = [row for row in PARENT_OWNERSHIP_AUDIT_ROWS if row["owned_by_current_corpus"] == "true"]
    claim_contract_rows = [row for row in MINIMAL_ACTION_CONTRACT_ROWS if row["valid_for_claim"] == "true"]
    claim_theorem_rows = [row for row in CONDITIONAL_THEOREM_CHAIN_ROWS if row["valid_for_claim"] == "true"]
    claim_ownership_rows = [row for row in PARENT_OWNERSHIP_AUDIT_ROWS if row["valid_for_claim"] == "true"]
    claim_residual_rows = [row for row in RESIDUAL_ROW if row["valid_for_claim"] == "true"]
    return [
        {
            "check_id": "V545_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V545_1_prior_544_clean",
            "result": "pass" if len(prior_validation) == 7 and not prior_fails else "fail",
            "detail": f"prior_validation_rows={len(prior_validation)};prior_fails={len(prior_fails)}",
        },
        {
            "check_id": "V545_2_prior_544_audits_loaded",
            "result": "pass" if len(prior_data_audit) >= 10 and len(prior_theorem_audit) >= 10 else "fail",
            "detail": f"prior_data_rows={len(prior_data_audit)};prior_theorem_rows={len(prior_theorem_audit)}",
        },
        {
            "check_id": "V545_3_contract_complete",
            "result": "pass" if len(MINIMAL_ACTION_CONTRACT_ROWS) == 7 and len(CONDITIONAL_THEOREM_CHAIN_ROWS) == 6 else "fail",
            "detail": f"contract_rows={len(MINIMAL_ACTION_CONTRACT_ROWS)};theorem_steps={len(CONDITIONAL_THEOREM_CHAIN_ROWS)}",
        },
        {
            "check_id": "V545_4_parent_ownership_not_overstated",
            "result": "pass" if len(PARENT_OWNERSHIP_AUDIT_ROWS) == 6 and not owned_rows else "fail",
            "detail": f"ownership_rows={len(PARENT_OWNERSHIP_AUDIT_ROWS)};owned_rows={len(owned_rows)}",
        },
        {
            "check_id": "V545_5_residual_retained",
            "result": "pass" if len(RESIDUAL_ROW) == 1 and RESIDUAL_ROW[0]["derivation_status"].startswith("retained_residual") else "fail",
            "detail": f"residual_rows={len(RESIDUAL_ROW)};status={RESIDUAL_ROW[0]['derivation_status']}",
        },
        {
            "check_id": "V545_6_no_claim_rows",
            "result": "pass" if not claim_contract_rows and not claim_theorem_rows and not claim_ownership_rows and not claim_residual_rows else "fail",
            "detail": f"claim_contract={len(claim_contract_rows)};claim_theorem={len(claim_theorem_rows)};claim_ownership={len(claim_ownership_rows)};claim_residual={len(claim_residual_rows)}",
        },
        {
            "check_id": "V545_7_no_overclaim",
            "result": "pass" if not claim_contract_rows and not claim_theorem_rows and not claim_ownership_rows and not claim_residual_rows else "fail",
            "detail": "boundary_reference_zero_derived=false; source_measure=false; measured_GM=false; Newton=false; PPN=false; local_GR=false",
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
    return f"""# 545 - Y5 Boundary Reference Minimal Action Clause or Residual Row

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

We can write the exact shape of a sufficient local mechanism, but the current corpus does not yet own it.

That is an important distinction:

```text
If MAC545_0...MAC545_6 are derived from the parent action,
then B_zero_flux = 0 and Delta_symp = 0 follow without a plateau axiom.
```

But right now those clauses are not parent-derived. So the honest output is a conditional theorem plus an explicit retained residual row.

## 2. Minimal Action Contract

{markdown_table(MINIMAL_ACTION_CONTRACT_ROWS)}

## 3. Conditional Theorem Chain

{markdown_table(CONDITIONAL_THEOREM_CHAIN_ROWS)}

## 4. Parent Ownership Audit

{markdown_table(PARENT_OWNERSHIP_AUDIT_ROWS)}

## 5. Retained Residual Row

{markdown_table(RESIDUAL_ROW)}

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
MTS has an exact sufficient contract for deriving the boundary/reference numerator zero.
MTS has not hidden the missing term; epsilon_boundary_reference_abs is retained explicitly.
```

Forbidden:

```text
MTS has derived B_zero_flux=Delta_symp=0 from the existing parent action.
MTS has filled measured GM, Newton, PPN, or local GR.
```

## 11. Practical Read

This is actually progress. The local-GR path is no longer a fog bank; it has a checklist. The price is steep, but not vague:

```text
parent action -> fixed reference -> cohomology-trivial boundary -> no vector/tensor boundary hair -> silent Pi_M variation -> measured GM denominator
```

Miss any one of those and the branch does not die automatically, but the missing piece must be scored as a residual, not smuggled in as "local vacuum plateau".

## 12. Next Target

`{NEXT_TARGET}`

Next: search the current parent-action corpus for anything that can own MAC545_0...MAC545_6. If ownership is still absent, convert `BRR545_0` into the first scoreable residual in the local PPN branch.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Y5-boundary-reference-minimal-action-clause-or-residual-row"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)

    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (MINIMAL_ACTION_CONTRACT_PATH, MINIMAL_ACTION_CONTRACT_ROWS),
        (CONDITIONAL_THEOREM_CHAIN_PATH, CONDITIONAL_THEOREM_CHAIN_ROWS),
        (PARENT_OWNERSHIP_AUDIT_PATH, PARENT_OWNERSHIP_AUDIT_ROWS),
        (RESIDUAL_ROW_PATH, RESIDUAL_ROW),
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
        "minimal_action_contract": str(ROOT / MINIMAL_ACTION_CONTRACT_PATH),
        "conditional_theorem_chain": str(ROOT / CONDITIONAL_THEOREM_CHAIN_PATH),
        "parent_ownership_audit": str(ROOT / PARENT_OWNERSHIP_AUDIT_PATH),
        "residual_row": str(ROOT / RESIDUAL_ROW_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "failed_validation_rows": len(failed_validations),
        "contract_rows": len(MINIMAL_ACTION_CONTRACT_ROWS),
        "conditional_theorem_steps": len(CONDITIONAL_THEOREM_CHAIN_ROWS),
        "parent_ownership_rows": len(PARENT_OWNERSHIP_AUDIT_ROWS),
        "residual_rows": len(RESIDUAL_ROW),
        "boundary_reference_zero_derived": False,
        "conditional_boundary_reference_zero_theorem_written": True,
        "first_boundary_reference_residual_claim_filled": False,
        "source_measure_theorem_derived": False,
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
        "done\nprivate_no_github\nconditional_boundary_reference_zero_contract_only_residual_retained_no_Newton_PPN_or_local_GR_promotion\n",
        encoding="utf-8",
    )

    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
