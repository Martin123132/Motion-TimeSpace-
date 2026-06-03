#!/usr/bin/env python3
"""Attempt to derive or bound B_mem from a memory-stress exchange law.

Private theory-discipline tool. It converts the current fitted B_mem evidence
into parent-stress corridor requirements, source-profile constraints, and a
promotion verdict.
"""

from __future__ import annotations

import csv
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
RUNS_ROOT = POST_CHECKPOINT / "runs"
OWNERSHIP_RUN = RUNS_ROOT / "20260531-132046-Bmem-p-u3-parent-ownership-gate"
U3_FIXED = 0.25

SOURCE_CHECKPOINTS = [
    "91-Bmem-p-u3-parent-ownership-gate.md",
    "82-amplitude-normalization-gate.md",
    "90-cosmo-model-selection-stability-ledger.md",
    "[local-formalization-workbench]/174-bmem-parent-boundary-law.md",
    "[local-formalization-workbench]/177-parent-amplitude-repair-contract.md",
    "[local-formalization-workbench]/178-parent-amplitude-theorem-attempt.md",
]


def resolve_source(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return POST_CHECKPOINT / path


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def fixed_bmem_values() -> list[dict[str, Any]]:
    rows = read_csv(OWNERSHIP_RUN / "results" / "cosmology_parameter_evidence.csv")
    output: list[dict[str, Any]] = []
    for row in rows:
        if row["model"] != "MTS_fixed_p3_u3quarter" or row["parameter"] != "B_mem":
            continue
        output.append(
            {
                "run_id": row["run_id"],
                "branch": row["branch"],
                "B_mem": float(row["best_fit"]),
                "edge_flag": row["edge_flag"],
            }
        )
    return output


def source_checkpoint_rows() -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for source in SOURCE_CHECKPOINTS:
        path = resolve_source(source)
        output.append(
            {
                "source": str(path),
                "exists": path.exists(),
                "role": {
                    "91-Bmem-p-u3-parent-ownership-gate.md": "latest p/u3/Bmem ownership gate",
                    "82-amplitude-normalization-gate.md": "original amplitude classification",
                    "90-cosmo-model-selection-stability-ledger.md": "scorecard reason to pursue amplitude derivation",
                }.get(Path(source).name, "formalization-workbench parent amplitude context"),
            }
        )
    return output


def stress_equation_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "equation": "Omega_M(N) = Omega_M0 + B_mem F(N)",
            "status": "definition_of_effective_memory_contrast",
            "derived_or_assumed": "closure_definition",
            "issue": "needs stress-energy owner",
        },
        {
            "step": 2,
            "equation": "S_M(N) = dOmega_M/dN = B_mem dF/dN",
            "status": "source_exchange_identity",
            "derived_or_assumed": "derived_from_step_1",
            "issue": "source sign/magnitude still depends on B_mem",
        },
        {
            "step": 3,
            "equation": "integral_0^infinity S_M dN = B_mem",
            "status": "integrated_source_budget",
            "derived_or_assumed": "derived",
            "issue": "budget not predicted",
        },
        {
            "step": 4,
            "equation": "B_mem = a_F DeltaR / (3 eta^2), eta = H0 L_cg/c",
            "status": "parent_trace_corridor",
            "derived_or_assumed": "conditional_contract",
            "issue": "a_F, DeltaR, and eta are not parent-predicted",
        },
        {
            "step": 5,
            "equation": "B_mem >= 0 if a_F > 0 and DeltaR >= 0",
            "status": "conditional_sign_law",
            "derived_or_assumed": "conditional",
            "issue": "endpoint ordering and coupling sign need parent proof",
        },
        {
            "step": 6,
            "equation": "B_mem <= A_max / (3 eta^2), A_max = max(a_F DeltaR)",
            "status": "amplitude_bound",
            "derived_or_assumed": "conditional_bound",
            "issue": "A_max is a prior/corridor, not a prediction",
        },
    ]


def source_profile_rows(values: list[dict[str, Any]]) -> list[dict[str, Any]]:
    x_peak = (2.0 / 3.0) ** (1.0 / 3.0)
    n_peak = U3_FIXED * x_peak
    z_peak = math.exp(n_peak) - 1.0
    shape_peak = (3.0 / U3_FIXED) * x_peak**2 * math.exp(-(x_peak**3))
    return [
        {
            "run_id": row["run_id"],
            "branch": row["branch"],
            "B_mem": row["B_mem"],
            "u3": U3_FIXED,
            "N_peak_source": n_peak,
            "z_peak_source": z_peak,
            "max_dF_dN": shape_peak,
            "max_S_M": row["B_mem"] * shape_peak,
            "integrated_source_budget": row["B_mem"],
        }
        for row in values
    ]


def corridor_rows(values: list[dict[str, Any]]) -> list[dict[str, Any]]:
    etas = [0.25, 0.5, 1.0, 1.25, 1.5, 2.0]
    output: list[dict[str, Any]] = []
    for row in values:
        for eta in etas:
            parent_budget = 3.0 * row["B_mem"] * eta**2
            output.append(
                {
                    "run_id": row["run_id"],
                    "branch": row["branch"],
                    "B_mem": row["B_mem"],
                    "eta": eta,
                    "required_aF_DeltaR": parent_budget,
                    "order_one_pass": 0.0 < parent_budget <= 1.0,
                    "half_budget_pass": 0.0 < parent_budget <= 0.5,
                    "readout": "order_one_corridor" if 0.0 < parent_budget <= 1.0 else "requires_large_parent_budget",
                }
            )
    return output


def eta_bound_rows(values: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in values:
        for budget_limit in [0.25, 0.5, 1.0]:
            eta_max = math.sqrt(budget_limit / (3.0 * row["B_mem"]))
            output.append(
                {
                    "run_id": row["run_id"],
                    "branch": row["branch"],
                    "B_mem": row["B_mem"],
                    "Amax": budget_limit,
                    "eta_max_for_budget": eta_max,
                    "Lcg_bound": f"L_cg <= {eta_max:.6f} c/H0",
                }
            )
    return output


def gate_rows(values: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not values:
        return [{"gate": "Bmem_values_available", "result": "fail", "reason": "no fixed branch values found"}]
    edge_hits = sum(str(row["edge_flag"]).lower() == "true" for row in values)
    b_values = [row["B_mem"] for row in values]
    b_min = min(b_values)
    b_max = max(b_values)
    required_at_eta1_min = 3.0 * b_min
    required_at_eta1_max = 3.0 * b_max
    eta_max_for_unit_budget = math.sqrt(1.0 / (3.0 * b_max))
    return [
        {
            "gate": "fixed_Bmem_positive",
            "result": "pass" if b_min > 0.0 else "fail",
            "reason": f"range={b_min:.6f} to {b_max:.6f}",
        },
        {
            "gate": "fixed_Bmem_non_edge",
            "result": "pass" if edge_hits == 0 else "fail",
            "reason": f"edge_hits={edge_hits} across {len(values)} inspected values",
        },
        {
            "gate": "eta1_order_one_budget",
            "result": "pass",
            "reason": f"eta=1 requires a_F DeltaR={required_at_eta1_min:.6f} to {required_at_eta1_max:.6f}",
        },
        {
            "gate": "unit_budget_eta_bound",
            "result": "pass_conditional",
            "reason": f"if a_F DeltaR <= 1, largest observed B_mem requires eta <= {eta_max_for_unit_budget:.6f}",
        },
        {
            "gate": "sign_predicted",
            "result": "pass_conditional",
            "reason": "positive B_mem follows only if a_F > 0 and DeltaR >= 0 are parent-derived",
        },
        {
            "gate": "magnitude_predicted_without_fit",
            "result": "fail",
            "reason": "eta, a_F, and DeltaR remain free within a corridor",
        },
        {
            "gate": "conservation_exchange_owned",
            "result": "open",
            "reason": "integrated source identity exists, but stress tensor exchange is not varied from parent action",
        },
        {
            "gate": "promotion_allowed",
            "result": "fail",
            "reason": "bound/corridor is not a no-fit prediction",
        },
    ]


def decision_rows(values: list[dict[str, Any]]) -> list[dict[str, Any]]:
    b_values = [row["B_mem"] for row in values]
    b_min = min(b_values) if b_values else ""
    b_max = max(b_values) if b_values else ""
    return [
        {
            "decision": "Bmem_prediction_status",
            "value": "bounded_order_one_corridor_not_prediction",
        },
        {
            "decision": "Bmem_empirical_range_used",
            "value": f"{b_min} to {b_max}",
        },
        {
            "decision": "allowed_use",
            "value": "tight prior/corridor discipline for future tests",
        },
        {
            "decision": "forbidden_use",
            "value": "field-theory support claim from fitted B_mem",
        },
        {
            "decision": "next_target",
            "value": "derive_eta_Lcg_or_memory_trace_contrast_before_more_support_fits",
        },
    ]


def main() -> None:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{timestamp}-memory-stress-amplitude-prediction-attempt"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    values = fixed_bmem_values()
    write_csv(
        results_dir / "source_checkpoint_register.csv",
        source_checkpoint_rows(),
        ["source", "exists", "role"],
    )
    write_csv(
        results_dir / "stress_exchange_equations.csv",
        stress_equation_rows(),
        ["step", "equation", "status", "derived_or_assumed", "issue"],
    )
    write_csv(
        results_dir / "source_profile_summary.csv",
        source_profile_rows(values),
        [
            "run_id",
            "branch",
            "B_mem",
            "u3",
            "N_peak_source",
            "z_peak_source",
            "max_dF_dN",
            "max_S_M",
            "integrated_source_budget",
        ],
    )
    write_csv(
        results_dir / "amplitude_corridor_grid.csv",
        corridor_rows(values),
        [
            "run_id",
            "branch",
            "B_mem",
            "eta",
            "required_aF_DeltaR",
            "order_one_pass",
            "half_budget_pass",
            "readout",
        ],
    )
    write_csv(
        results_dir / "eta_bound_table.csv",
        eta_bound_rows(values),
        ["run_id", "branch", "B_mem", "Amax", "eta_max_for_budget", "Lcg_bound"],
    )
    write_csv(
        results_dir / "gate_results.csv",
        gate_rows(values),
        ["gate", "result", "reason"],
    )
    write_csv(results_dir / "decision.csv", decision_rows(values), ["decision", "value"])

    b_values = [row["B_mem"] for row in values]
    status = {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "readout": "memory_stress_amplitude_bounded_not_predicted",
        "fixed_branch_Bmem_range": [min(b_values), max(b_values)] if b_values else [],
        "stable_evidence_allowed": False,
        "promotion_allowed": False,
        "next_action": "write checkpoint 92; derive eta/Lcg or trace contrast before more support fitting",
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
