#!/usr/bin/env python3
"""Write and gate the parent-action contract needed to normalize R.

Private theory-discipline tool. It does not claim to derive the parent action;
it specifies the exact conditions required to break the R/a_F rescaling
degeneracy and turn a_F=1 from convention into theorem.
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
    POST_CHECKPOINT / "95-trace-coupling-aF-normalization-gate.md",
    POST_CHECKPOINT / "94-endpoint-relaxation-DeltaR-gate.md",
    FORMALIZATION / "69-relaxation-functional-lock.md",
    FORMALIZATION / "70-relaxation-functional-lock-first-results.md",
    FORMALIZATION / "83-parent-equations-v1.md",
    FORMALIZATION / "116-FLRW-memory-projection-derivation.md",
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


def latest_af_run() -> Path:
    runs = sorted(RUNS_ROOT.glob("*-trace-coupling-aF-normalization-gate"))
    if not runs:
        raise FileNotFoundError("No trace-coupling aF normalization gate run found.")
    return runs[-1]


def product_inputs(af_run: Path) -> list[dict[str, Any]]:
    rows = read_csv(af_run / "results" / "flrw_eta1_product_inputs.csv")
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
        "95-trace-coupling-aF-normalization-gate.md": "current a_F status and rescaling blocker",
        "94-endpoint-relaxation-DeltaR-gate.md": "DeltaR sign/order target and endpoint-relaxation law",
        "69-relaxation-functional-lock.md": "R-gradient flow, F_1=0, F_2=a_F lambda_R",
        "70-relaxation-functional-lock-first-results.md": "high-mobility design rule and stiff-R failure mode",
        "83-parent-equations-v1.md": "parent equation scaffold, conservation, Gamma_eff trace/tensor split",
        "116-FLRW-memory-projection-derivation.md": "effective FLRW memory projection status",
        "174-bmem-parent-boundary-law.md": "B_mem endpoint contrast identity and missing a_F/R law",
    }
    return [{"source": str(path), "exists": path.exists(), "role": role[path.name]} for path in SOURCE_CHECKPOINTS]


def contract_clause_rows(product_low: float, product_high: float) -> list[dict[str, Any]]:
    return [
        {
            "clause": "C0_dimensions_and_sectors",
            "required_statement": "[Gamma_eff]=L^-2, [L_cg]=L, R and F are dimensionless, and K_MTS owns the trace/tensor split",
            "breaks_degeneracy": "prevents inserting a sector-specific scalar curvature term by notation",
            "current_evidence": "83 locks dimensions and trace split at scaffold level",
            "status": "partial_scaffold",
        },
        {
            "clause": "C1_m_field_metric",
            "required_statement": "the parent action fixes the coordinate/metric of m, e.g. a canonical or invariant field-space metric G_mm(m,X_B)",
            "breaks_degeneracy": "blocks moving amplitude between lambda_R and Delta m by m-rescaling",
            "current_evidence": "m is used in relaxation laws, but its field metric is not parent-derived",
            "status": "missing",
        },
        {
            "clause": "C2_R_zero",
            "required_statement": "R(m_L;X_B)=0 or R_L(X_B) is fixed by the action, not chosen after fitting",
            "breaks_degeneracy": "fixes the additive freedom in R",
            "current_evidence": "relaxation checkpoints use R-R_L consistently",
            "status": "conditional",
        },
        {
            "clause": "C3_R_unit_scale",
            "required_statement": "R has a parent-fixed unit scale, e.g. 0<=R-R_L<=1 or a normalized boundary charge integral equals one",
            "breaks_degeneracy": "kills R -> c_R R and a_F -> a_F/c_R",
            "current_evidence": "not present; this is the hard blocker from checkpoint 95",
            "status": "missing",
        },
        {
            "clause": "C4_same_R_drives_relaxation",
            "required_statement": "nabla_mu J_m^mu = -gamma_B delta R/delta m + [1-Pi_B]S_cg follows from the same R",
            "breaks_degeneracy": "prevents using one R for local screening and a different R for cosmology",
            "current_evidence": "69/70 show the conditional functional-lock route",
            "status": "conditional",
        },
        {
            "clause": "C5_unit_trace_projection",
            "required_statement": "Gamma_eff=L_cg^-2[F_L+(R-R_L)] so partial Gamma_eff/partial R = L_cg^-2",
            "breaks_degeneracy": "turns a_F=1 into a projection theorem rather than a convention",
            "current_evidence": "95 labels this the cleanest closure choice, not action-derived",
            "status": "missing",
        },
        {
            "clause": "C6_Ward_or_Noether_identity",
            "required_statement": "a diffeomorphism/coarse-graining/Ward identity fixes the unit trace coefficient and forbids independent a_F",
            "breaks_degeneracy": "makes arbitrary trace rescaling illegal",
            "current_evidence": "Noether-style conservation scaffolds exist, but no R-normalization Ward identity",
            "status": "missing",
        },
        {
            "clause": "C7_local_F2_guard",
            "required_statement": "F_2=lambda_R is PPN-safe, with local screening mainly through gamma_B rather than huge lambda_R",
            "breaks_degeneracy": "prevents cosmology amplitude from being bought by unsafe local stiffness",
            "current_evidence": "70 and 95 support the high-mobility design rule",
            "status": "conditional_guard",
        },
        {
            "clause": "C8_endpoint_solution",
            "required_statement": f"the parent endpoint equations predict DeltaR={product_low:.6f}..{product_high:.6f} for a_F=1 before SN+BAO",
            "breaks_degeneracy": "separates prediction from post-fit amplitude reading",
            "current_evidence": "range currently comes from fitted B_mem after eta=1",
            "status": "missing",
        },
        {
            "clause": "C9_no_hidden_fit",
            "required_statement": "R scale, a_F, lambda_R, gamma_B, and endpoint conditions are fixed before data scoring and kept common across branches",
            "breaks_degeneracy": "stops per-dataset normalization drift",
            "current_evidence": "discipline exists in ledgers, but parent constants remain unproved",
            "status": "policy_pass_theory_missing",
        },
    ]


def theorem_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "field_metric_plus_potential",
            "idea": "derive m units from a parent kinetic/field-space metric and R from a canonical potential or Lyapunov functional",
            "would_fix": "m-rescaling, lambda_R meaning, R curvature, local F2 bookkeeping",
            "fatal_if_missing": "a_F and lambda_R remain coordinate conventions",
            "current_status": "best_primary_route",
        },
        {
            "route": "normalized_boundary_charge",
            "idea": "define R contrast as a normalized boundary/source charge with total admissible contrast one",
            "would_fix": "R unit scale and DeltaR cap",
            "fatal_if_missing": "DeltaR<=1 remains an assumption",
            "current_status": "best_amplitude_route",
        },
        {
            "route": "trace_projection_Ward_identity",
            "idea": "derive partial Gamma_eff/partial R=L_cg^-2 from metric trace variation or coarse-graining symmetry",
            "would_fix": "a_F=1",
            "fatal_if_missing": "unit trace coupling remains closure convention",
            "current_status": "needed_for_promotion",
        },
        {
            "route": "relative_entropy_or_distance_functional",
            "idea": "make R a normalized non-negative distance from local equilibrium",
            "would_fix": "positive sign and possibly bounded contrast",
            "fatal_if_missing": "endpoint ordering remains conditional",
            "current_status": "speculative_candidate",
        },
        {
            "route": "pure_canonical_convention",
            "idea": "declare a_F=1 by defining R to carry the trace-coupling scale",
            "would_fix": "bookkeeping only",
            "fatal_if_missing": "not fatal for testing, fatal for support claims",
            "current_status": "closure_fallback",
        },
    ]


def degeneracy_breaker_rows() -> list[dict[str, Any]]:
    return [
        {
            "degeneracy": "additive_R_shift",
            "transformation": "R -> R + c0(X_B)",
            "required_breaker": "R_L or R(m_L;X_B)=0 fixed by variation",
            "contract_clause": "C2_R_zero",
        },
        {
            "degeneracy": "multiplicative_R_scale",
            "transformation": "R -> c_R R, a_F -> a_F/c_R",
            "required_breaker": "unit boundary charge, normalized contrast, or Ward-fixed trace coefficient",
            "contract_clause": "C3_R_unit_scale/C5_unit_trace_projection/C6_Ward_or_Noether_identity",
        },
        {
            "degeneracy": "m_coordinate_scale",
            "transformation": "m -> c_m m; lambda_R -> lambda_R/c_m^2 in quadratic bookkeeping",
            "required_breaker": "parent field metric or kinetic term fixes m units",
            "contract_clause": "C1_m_field_metric",
        },
        {
            "degeneracy": "cosmology_local_split",
            "transformation": "keep a_F DeltaR fixed while changing a_F lambda_R",
            "required_breaker": "same R and same lambda_R control both endpoint amplitude and local F2",
            "contract_clause": "C4_same_R_drives_relaxation/C7_local_F2_guard",
        },
        {
            "degeneracy": "post_fit_endpoint_selection",
            "transformation": "choose DeltaR after observing B_mem",
            "required_breaker": "parent endpoint solution predicts DeltaR before fitting",
            "contract_clause": "C8_endpoint_solution/C9_no_hidden_fit",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "exact_contract_written",
            "result": "pass",
            "reason": "C0-C9 specify what a parent action must satisfy to normalize R and a_F",
        },
        {
            "gate": "source_paths_exist",
            "result": "pass",
            "reason": "all cited source checkpoints are present in the current worktree",
        },
        {
            "gate": "R_additive_zero_condition",
            "result": "pass_conditional",
            "reason": "R-R_L is already used consistently, but action-level zero fixing remains to be shown",
        },
        {
            "gate": "R_unit_scale_derived",
            "result": "fail",
            "reason": "no parent normalized charge or field metric currently kills R -> c_R R",
        },
        {
            "gate": "aF_equals_1_derived",
            "result": "fail",
            "reason": "unit trace coefficient is still a canonical closure convention",
        },
        {
            "gate": "Ward_identity_available",
            "result": "fail",
            "reason": "no Noether/Ward identity fixes partial Gamma_eff/partial R=L_cg^-2",
        },
        {
            "gate": "local_F2_guard_preserved",
            "result": "pass_conditional",
            "reason": "contract preserves F2=lambda_R and high-mobility screening preference for a_F=1",
        },
        {
            "gate": "DeltaR_predicted_pre_fit",
            "result": "fail",
            "reason": "DeltaR range is still inferred from fitted B_mem, not parent endpoint equations",
        },
        {
            "gate": "closure_use_allowed",
            "result": "pass",
            "reason": "a_F=1 may be used as a clearly labelled canonical closure for testing",
        },
        {
            "gate": "support_claim_allowed",
            "result": "fail",
            "reason": "contract-only status is not enough for field-theory promotion",
        },
    ]


def decision_rows(product_low: float, product_high: float) -> list[dict[str, Any]]:
    return [
        {
            "decision": "contract_status",
            "value": "R_normalization_contract_written_not_derived",
        },
        {
            "decision": "allowed_closure",
            "value": f"a_F_equals_1_with_DeltaR_target_{product_low:.6f}_to_{product_high:.6f}",
        },
        {
            "decision": "promotion_blocker",
            "value": "missing_R_unit_scale_and_missing_trace_projection_Ward_identity",
        },
        {
            "decision": "primary_theorem_route",
            "value": "field_metric_plus_normalized_boundary_charge_plus_trace_projection_Ward_identity",
        },
        {
            "decision": "next_target",
            "value": "attempt_or_reject_canonical_R_theorem_from_parent_action",
        },
    ]


def main() -> None:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{timestamp}-parent-R-normalization-contract"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    af_run = latest_af_run()
    inputs = product_inputs(af_run)
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
        results_dir / "parent_R_contract_clauses.csv",
        contract_clause_rows(product_low, product_high),
        ["clause", "required_statement", "breaks_degeneracy", "current_evidence", "status"],
    )
    write_csv(
        results_dir / "candidate_theorem_routes.csv",
        theorem_route_rows(),
        ["route", "idea", "would_fix", "fatal_if_missing", "current_status"],
    )
    write_csv(
        results_dir / "degeneracy_breakers.csv",
        degeneracy_breaker_rows(),
        ["degeneracy", "transformation", "required_breaker", "contract_clause"],
    )
    write_csv(results_dir / "gate_results.csv", gate_rows(), ["gate", "result", "reason"])
    write_csv(results_dir / "decision.csv", decision_rows(product_low, product_high), ["decision", "value"])

    status = {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "input_aF_run": str(af_run),
        "readout": "R_normalization_contract_written_not_derived",
        "canonical_aF1_DeltaR_target": [product_low, product_high],
        "contract_clauses": 10,
        "primary_theorem_route": "field_metric_plus_normalized_boundary_charge_plus_trace_projection_Ward_identity",
        "stable_evidence_allowed": False,
        "promotion_allowed": False,
        "next_action": "write checkpoint 96; attempt canonical R theorem or demote a_F=1 to explicit closure convention",
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
