#!/usr/bin/env python3
"""Attempt the canonical-R theorem route from the parent normalization contract.

Private theory-discipline tool. It tries the strongest current route:
field metric for m + normalized boundary charge for R + trace-projection Ward
identity. If any part remains assumed, a_F=1 is demoted to explicit canonical
closure for empirical testing.
"""

from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
FORMALIZATION = POST_CHECKPOINT.parent / "formalization-workbench"
RUNS_ROOT = POST_CHECKPOINT / "runs"

SOURCE_CHECKPOINTS = [
    POST_CHECKPOINT / "96-parent-R-normalization-contract.md",
    POST_CHECKPOINT / "95-trace-coupling-aF-normalization-gate.md",
    POST_CHECKPOINT / "94-endpoint-relaxation-DeltaR-gate.md",
    FORMALIZATION / "04-variable-audit.csv",
    FORMALIZATION / "14-field-definitions-dimensional-ledger.md",
    FORMALIZATION / "69-relaxation-functional-lock.md",
    FORMALIZATION / "70-relaxation-functional-lock-first-results.md",
    FORMALIZATION / "83-parent-equations-v1.md",
    FORMALIZATION / "174-bmem-parent-boundary-law.md",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def latest_contract_run() -> Path:
    runs = sorted(RUNS_ROOT.glob("*-parent-R-normalization-contract"))
    if not runs:
        raise FileNotFoundError("No parent-R normalization contract run found.")
    return runs[-1]


def product_inputs(contract_run: Path) -> list[dict[str, Any]]:
    rows = read_csv(contract_run / "results" / "flrw_eta1_product_inputs.csv")
    return [
        {
            "run_id": row["run_id"],
            "branch": row["branch"],
            "B_mem": float(row["B_mem"]),
            "eta": float(row["eta"]),
            "required_aF_DeltaR": float(row["required_aF_DeltaR"]),
        }
        for row in rows
    ]


def source_rows() -> list[dict[str, Any]]:
    role = {
        "96-parent-R-normalization-contract.md": "C0-C9 theorem contract",
        "95-trace-coupling-aF-normalization-gate.md": "a_F=1 canonical viability and rescaling blocker",
        "94-endpoint-relaxation-DeltaR-gate.md": "DeltaR target range and endpoint-relaxation constraints",
        "04-variable-audit.csv": "canonical variable status for R_lock, a_F, Gamma_eff, L_cg",
        "14-field-definitions-dimensional-ledger.md": "dimension ledger for R, a_F, lambda_R, Gamma_eff",
        "69-relaxation-functional-lock.md": "conditional R-lock and F_1/F_2 relations",
        "70-relaxation-functional-lock-first-results.md": "high-mobility screening and stiff-R warning",
        "83-parent-equations-v1.md": "parent scaffold and conservation/trace split",
        "174-bmem-parent-boundary-law.md": "B_mem endpoint contrast identity",
    }
    return [{"source": str(path), "exists": path.exists(), "role": role[path.name]} for path in SOURCE_CHECKPOINTS]


def theorem_attempt_rows(product_low: float, product_high: float) -> list[dict[str, Any]]:
    return [
        {
            "attempt": "field_metric_plus_potential",
            "construction": "S_m = integral sqrt(-g)[-1/2 G_mm(m,X_B) nabla m nabla m - V_R(m,X_B)]",
            "what_it_would_fix": "m coordinate scale, lambda_R bookkeeping, local F2 meaning",
            "failure_or_gap": "does not by itself fix the absolute unit scale of R or the trace coefficient",
            "status": "partial_template_not_theorem",
        },
        {
            "attempt": "normalized_boundary_charge",
            "construction": "R-R_L = (Q_R-Q_R,L)/Q_* with Q_* fixed by topology, cell count, or normalized flux",
            "what_it_would_fix": "R unit scale and DeltaR cap",
            "failure_or_gap": "no current theorem fixes Q_* independently of the fitted memory amplitude",
            "status": "conditional_if_Qstar_derived",
        },
        {
            "attempt": "trace_projection_Ward_identity",
            "construction": "delta trace projection implies partial Gamma_eff/partial R = L_cg^-2",
            "what_it_would_fix": "a_F=1 as a coefficient theorem",
            "failure_or_gap": "no parent symmetry/Ward identity currently forbids an independent coefficient",
            "status": "missing",
        },
        {
            "attempt": "relative_entropy_distance",
            "construction": "R = D(P_m||P_L)/D_max with a parent probability measure and maximum contrast",
            "what_it_would_fix": "positivity and possibly bounded DeltaR",
            "failure_or_gap": "P_m, D_max, and measure over memory states are not derived",
            "status": "speculative_not_available",
        },
        {
            "attempt": "combined_three_part_theorem_schema",
            "construction": "field metric + normalized charge + Ward projection -> a_F=1 and DeltaR target",
            "what_it_would_fix": f"a_F=1 with DeltaR={product_low:.6f}..{product_high:.6f}",
            "failure_or_gap": "all three ingredients cannot yet be supplied from the current corpus",
            "status": "conditional_schema_only",
        },
        {
            "attempt": "pure_canonical_redefinition",
            "construction": "define R_eff = a_F R and set a_F=1 by convention",
            "what_it_would_fix": "bookkeeping and test discipline",
            "failure_or_gap": "does not create a parent prediction or break the physical degeneracy",
            "status": "valid_closure_fallback",
        },
    ]


def theorem_chain_rows(product_low: float, product_high: float) -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "statement": "Parent field metric fixes m units and lambda_R meaning.",
            "needed_for": "C1_m_field_metric",
            "status": "not_derived",
        },
        {
            "step": 2,
            "statement": "R(m_L;X_B)=0 fixes additive zero.",
            "needed_for": "C2_R_zero",
            "status": "conditional",
        },
        {
            "step": 3,
            "statement": "Normalized boundary charge fixes R unit scale and forbids R->c_R R.",
            "needed_for": "C3_R_unit_scale",
            "status": "not_derived",
        },
        {
            "step": 4,
            "statement": "Same R drives relaxation and trace projection.",
            "needed_for": "C4_same_R_drives_relaxation",
            "status": "conditional",
        },
        {
            "step": 5,
            "statement": "Ward identity fixes partial Gamma_eff/partial R = L_cg^-2.",
            "needed_for": "C5_C6_unit_trace_projection",
            "status": "not_derived",
        },
        {
            "step": 6,
            "statement": "Therefore a_F=1 is forced, not chosen.",
            "needed_for": "a_F_promotion",
            "status": "not_derived_because_steps_3_and_5_fail",
        },
        {
            "step": 7,
            "statement": f"Parent endpoint equations predict DeltaR={product_low:.6f}..{product_high:.6f}.",
            "needed_for": "C8_endpoint_solution",
            "status": "not_derived",
        },
        {
            "step": 8,
            "statement": "B_mem = DeltaR/3 on eta=1, a_F=1 branch.",
            "needed_for": "no_fit_amplitude_prediction",
            "status": "identity_only_not_prediction",
        },
    ]


def no_go_rows() -> list[dict[str, Any]]:
    return [
        {
            "test": "Noether_identity_alone",
            "finding": "Noether identities relate field equations; they do not fix a numerical trace coefficient by themselves.",
            "result": "fail_as_derivation",
            "lesson": "Need a specific symmetry or constraint whose charge normalization is fixed.",
        },
        {
            "test": "field_metric_alone",
            "finding": "A field metric can fix m units but leaves V_R or R scale as an independent coupling.",
            "result": "partial_only",
            "lesson": "C1 helps local safety but does not kill R->c_R R.",
        },
        {
            "test": "bounded_contrast_assumption",
            "finding": "Assuming 0<=DeltaR<=1 gives useful a_F bounds but does not derive the bound.",
            "result": "closure_only",
            "lesson": "Need a normalized charge or entropy theorem.",
        },
        {
            "test": "action_coefficient_rescaling",
            "finding": "A term c_R R in the action can be reabsorbed into R normalization unless c_R is fixed by a charge/Ward law.",
            "result": "fail_as_derivation",
            "lesson": "Writing an action term is not enough; coefficient ownership matters.",
        },
        {
            "test": "post_fit_endpoint_matching",
            "finding": "Choosing DeltaR to match fitted B_mem reproduces the data but is circular.",
            "result": "fail_as_prediction",
            "lesson": "Endpoint equations must predict DeltaR before the likelihood run.",
        },
    ]


def closure_label_rows(product_low: float, product_high: float) -> list[dict[str, Any]]:
    return [
        {
            "branch_label": "canonical_R_closure",
            "fixed_choices": "eta=1; a_F=1; p=3; u3=1/4",
            "derived_parts": "p=3 conditional shape route; u3=1/4 conditional cell route; eta=1 conditional FLRW L_cg route",
            "closure_parts": "a_F=1; DeltaR read from fitted B_mem; R unit scale",
            "allowed_use": "empirical scorecard branch with transparent amplitude debt",
            "forbidden_use": "field-theory support claim from B_mem amplitude",
        },
        {
            "branch_label": "canonical_R_target_range",
            "fixed_choices": f"DeltaR target {product_low:.6f} to {product_high:.6f}",
            "derived_parts": "range follows algebraically from eta=1 and a_F=1",
            "closure_parts": "range is fitted-output inherited, not predicted",
            "allowed_use": "target for future parent endpoint theorem",
            "forbidden_use": "pre-fit prediction",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "theorem_attempt_made",
            "result": "pass",
            "reason": "field metric, normalized boundary charge, and Ward identity routes were explicitly tested",
        },
        {
            "gate": "field_metric_constructed",
            "result": "partial",
            "reason": "template fixes m-scale in principle but not R unit scale or trace coefficient",
        },
        {
            "gate": "normalized_boundary_charge_derived",
            "result": "fail",
            "reason": "no parent theorem fixes Q_* or a unit charge independently of B_mem",
        },
        {
            "gate": "trace_projection_Ward_identity_derived",
            "result": "fail",
            "reason": "no current Ward/Noether identity fixes partial Gamma_eff/partial R=L_cg^-2",
        },
        {
            "gate": "R_rescaling_degeneracy_broken",
            "result": "fail",
            "reason": "R->c_R R remains physically unbroken in the current scaffold",
        },
        {
            "gate": "DeltaR_predicted_pre_fit",
            "result": "fail",
            "reason": "DeltaR target remains inherited from fitted B_mem",
        },
        {
            "gate": "concrete_parent_action_found",
            "result": "fail",
            "reason": "only a conditional theorem schema was found, not a completed construction",
        },
        {
            "gate": "aF1_demoted_to_closure",
            "result": "pass",
            "reason": "a_F=1 is now explicitly labelled canonical closure, not derived amplitude",
        },
        {
            "gate": "empirical_testing_allowed",
            "result": "pass",
            "reason": "canonical closure is disciplined enough for fair scorecard tests",
        },
        {
            "gate": "support_claim_allowed",
            "result": "fail",
            "reason": "amplitude support language remains blocked until C1/C3/C5/C6/C8 are actually proved",
        },
    ]


def decision_rows(product_low: float, product_high: float) -> list[dict[str, Any]]:
    return [
        {
            "decision": "theorem_status",
            "value": "canonical_R_theorem_not_derived",
        },
        {
            "decision": "aF1_status",
            "value": "explicit_canonical_closure_for_empirical_testing",
        },
        {
            "decision": "target_range",
            "value": f"DeltaR_target_for_future_theorem_{product_low:.6f}_to_{product_high:.6f}",
        },
        {
            "decision": "main_failure",
            "value": "missing_normalized_boundary_charge_and_missing_trace_projection_Ward_identity",
        },
        {
            "decision": "next_target",
            "value": "return_to_empirical_scorecard_or_attempt_normalized_boundary_charge_theorem",
        },
    ]


def main() -> None:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{timestamp}-canonical-R-theorem-attempt"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    contract_run = latest_contract_run()
    inputs = product_inputs(contract_run)
    products = [item["required_aF_DeltaR"] for item in inputs]
    product_low = min(products)
    product_high = max(products)

    source_table = source_rows()
    if not all(row["exists"] for row in source_table):
        missing = [row["source"] for row in source_table if not row["exists"]]
        raise FileNotFoundError(f"Missing source checkpoints: {missing}")

    write_csv(results_dir / "source_checkpoint_register.csv", source_table, ["source", "exists", "role"])
    write_csv(
        results_dir / "flrw_eta1_product_inputs.csv",
        inputs,
        ["run_id", "branch", "B_mem", "eta", "required_aF_DeltaR"],
    )
    write_csv(
        results_dir / "theorem_attempts.csv",
        theorem_attempt_rows(product_low, product_high),
        ["attempt", "construction", "what_it_would_fix", "failure_or_gap", "status"],
    )
    write_csv(
        results_dir / "conditional_theorem_chain.csv",
        theorem_chain_rows(product_low, product_high),
        ["step", "statement", "needed_for", "status"],
    )
    write_csv(results_dir / "no_go_tests.csv", no_go_rows(), ["test", "finding", "result", "lesson"])
    write_csv(
        results_dir / "closure_label_register.csv",
        closure_label_rows(product_low, product_high),
        ["branch_label", "fixed_choices", "derived_parts", "closure_parts", "allowed_use", "forbidden_use"],
    )
    write_csv(results_dir / "gate_results.csv", gate_rows(), ["gate", "result", "reason"])
    write_csv(results_dir / "decision.csv", decision_rows(product_low, product_high), ["decision", "value"])

    status = {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "input_contract_run": str(contract_run),
        "readout": "canonical_R_theorem_not_derived_aF1_demoted_to_closure",
        "canonical_aF1_DeltaR_target": [product_low, product_high],
        "concrete_parent_action_found": False,
        "aF1_status": "explicit_canonical_closure_for_empirical_testing",
        "stable_evidence_allowed": False,
        "promotion_allowed": False,
        "next_action": "write checkpoint 97; choose empirical scorecard retest or narrower normalized-boundary-charge theorem attempt",
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
