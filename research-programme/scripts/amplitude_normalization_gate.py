#!/usr/bin/env python3
"""Classify MTS amplitude and normalization factors after the local-route pivot."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]

SOURCE_PATHS = {
    "45_memory_scalar_reconstruction_gate": Path("45-memory-scalar-reconstruction-gate.md"),
    "49_C2_regularized_closure_ledger": Path("49-C2-regularized-closure-ledger.md"),
    "50_parent_activation_law_attempt": Path("50-parent-activation-law-attempt.md"),
    "55_u3_quarter_lock_smoke": Path("55-u3-quarter-lock-smoke.md"),
    "56_u3_quarter_parent_cell_theorem": Path("56-u3-quarter-parent-cell-theorem-attempt.md"),
    "80_stress_free_reference_gate": Path("80-stress-free-reference-action-gate.md"),
    "81_post_local_route_pivot_decision": Path("81-post-local-route-pivot-decision.md"),
    "81_decision": Path("runs/20260531-120847-post-local-route-pivot-decision/results/decision.csv"),
}


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, relative_path in SOURCE_PATHS.items():
        absolute_path = POST_CHECKPOINT / relative_path
        rows.append(
            {
                "source_key": key,
                "relative_path": str(relative_path),
                "absolute_path": str(absolute_path),
                "exists": absolute_path.exists(),
            }
        )
    missing = [row["absolute_path"] for row in rows if not row["exists"]]
    if missing:
        raise FileNotFoundError("missing source files: " + "; ".join(missing))
    return rows


def amplitude_register_rows() -> list[dict[str, Any]]:
    return [
        {
            "factor": "p_activation",
            "symbol_or_value": "p = 3",
            "sector": "cosmology_memory_activation",
            "current_evidence": "minimal regularity/cubic onset argument and C2 regularized closure performance",
            "classification": "bounded_structural_closure_not_parent_derived",
            "allowed_use": "fixed structural closure exponent with explicit derivation gap",
            "must_not_claim": "parent action derivation",
        },
        {
            "factor": "u3_transition_scale",
            "symbol_or_value": "u_3 = 1/4",
            "sector": "cosmology_memory_activation",
            "current_evidence": "no-refit quarter-lock smoke survives and reduces fitted freedom",
            "classification": "bounded_structural_candidate_not_parent_derived",
            "allowed_use": "fixed less-free closure candidate",
            "must_not_claim": "cell theorem or local/FLRW domain derivation",
        },
        {
            "factor": "memory_amplitude",
            "symbol_or_value": "B_mem or b_mem",
            "sector": "cosmology_background_memory",
            "current_evidence": "frozen calibrated amplitude in scalar reconstruction and C2 closure ledgers",
            "classification": "fitted_or_calibrated_closure_parameter",
            "allowed_use": "fit/calibration parameter with prior-edge and baseline diagnostics",
            "must_not_claim": "derived memory charge normalization",
        },
        {
            "factor": "Ccoh_gate_amplitude",
            "symbol_or_value": "C_coh in [0,1]",
            "sector": "local_to_cosmology_selector",
            "current_evidence": "local parent-action route demoted at checkpoint 80",
            "classification": "diagnostic_closure_selector",
            "allowed_use": "diagnostic empirical closure only",
            "must_not_claim": "derived local GR suppression mechanism",
        },
        {
            "factor": "activation_shape_normalization",
            "symbol_or_value": "F(N)=1-exp[-(N/u_3)^3]",
            "sector": "cosmology_background_shape",
            "current_evidence": "regularized C2 closure retained; shape is mathematically cleaner than prior fitted exponent",
            "classification": "regularized_closure_shape",
            "allowed_use": "internal closure benchmark and empirical test target",
            "must_not_claim": "fundamental scalar potential",
        },
        {
            "factor": "scalar_proxy_normalization",
            "symbol_or_value": "rho_X/H0^2 = 1 - Omega_m0 + b_mem F",
            "sector": "scalar_proxy_reconstruction",
            "current_evidence": "reconstructable but reverse-engineered from fitted background",
            "classification": "reverse_engineered_proxy",
            "allowed_use": "diagnostic reconstruction only",
            "must_not_claim": "fundamental MTS scalar action",
        },
        {
            "factor": "local_transition_amplitude",
            "symbol_or_value": "A_loc or q_loc suppression amplitude",
            "sector": "local_PPN",
            "current_evidence": "local Ccoh parent route failed; no derived local suppression amplitude",
            "classification": "rejected_as_derived_in_current_route",
            "allowed_use": "explicit blocker or empirical bound target",
            "must_not_claim": "derived local vacuum plateau",
        },
    ]


def gate_result_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "p3_parent_derived",
            "result": "fail",
            "reason": "p=3 has regularity/structural support but no parent action theorem",
        },
        {
            "gate": "u3_quarter_parent_derived",
            "result": "fail",
            "reason": "u3=1/4 survives as less-free closure but lacks parent cell/domain derivation",
        },
        {
            "gate": "B_mem_derived",
            "result": "fail",
            "reason": "B_mem/b_mem remains calibrated/fitted amplitude",
        },
        {
            "gate": "Ccoh_amplitude_derived",
            "result": "fail",
            "reason": "checkpoint 80 demoted local Ccoh parent route",
        },
        {
            "gate": "closure_use_allowed",
            "result": "pass",
            "reason": "regularized closures may be tested if labelled and baselined fairly",
        },
        {
            "gate": "public_claim_allowed",
            "result": "fail",
            "reason": "no amplitude is fully parent-derived yet",
        },
    ]


def empirical_handling_rows() -> list[dict[str, Any]]:
    return [
        {
            "factor": "p = 3",
            "empirical_handling": "fix in primary closure tests; compare against fitted exponent as ablation",
            "baseline_requirement": "show whether p=3 loses materially against fitted-p and LambdaCDM/wCDM/CPL-style baselines",
        },
        {
            "factor": "u_3 = 1/4",
            "empirical_handling": "fix in primary closure tests; compare against fitted u3 and inherited C2 u3",
            "baseline_requirement": "report no-refit and refit deltas separately",
        },
        {
            "factor": "B_mem/b_mem",
            "empirical_handling": "fit or calibrate with explicit priors; never freeze silently",
            "baseline_requirement": "prior-edge, AIC/BIC, and data-split sensitivity are mandatory",
        },
        {
            "factor": "C_coh",
            "empirical_handling": "test as diagnostic selector only",
            "baseline_requirement": "compare to non-Ccoh closure and standard baselines where applicable",
        },
        {
            "factor": "A_loc/q_loc",
            "empirical_handling": "do not fit as derived local mechanism; only bound as local residual",
            "baseline_requirement": "PPN/local bounds must be quoted as constraints, not wins",
        },
    ]


def next_obligation_rows() -> list[dict[str, Any]]:
    return [
        {
            "obligation": "B_mem_origin",
            "question": "Can memory amplitude be tied to a conserved memory charge, boundary term, or normalization integral?",
            "next_test": "derive_or_bound_Bmem_from_memory_current",
        },
        {
            "obligation": "u3_cell_origin",
            "question": "Can u3=1/4 be connected to a real cell/domain theorem without the failed Ccoh parent route?",
            "next_test": "treat_as_ablation_variable_until_new_derivation",
        },
        {
            "obligation": "p3_regularization_origin",
            "question": "Can the cubic onset be derived from differentiability, extremality, or memory-current smoothness?",
            "next_test": "keep_p3_fixed_but_compare_to_fitted_p",
        },
        {
            "obligation": "local_amplitude_suppression",
            "question": "Can local residual amplitude be bounded without claiming a plateau theorem?",
            "next_test": "PPN_bound_manifest_not_parent_claim",
        },
        {
            "obligation": "fair_empirical_matrix",
            "question": "Which amplitude choices are fixed, fitted, or ablated in the next data tests?",
            "next_test": "83_empirical_closure_test_manifest",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "amplitude_gate_status",
            "status": "no_amplitude_fully_parent_derived",
            "evidence": "p=3 and u3=1/4 are bounded structural closures; B_mem remains fitted/calibrated; Ccoh local amplitude is demoted",
            "next_action": "build empirical closure manifest with fixed/fitted/ablated amplitude columns",
        },
        {
            "decision": "allowed_claim_level",
            "status": "disciplined_closure_program_not_field_theory_promotion",
            "evidence": "amplitude factors are now labelled and cannot be used as hidden evidence",
            "next_action": "create 83-empirical-closure-test-manifest.md",
        },
        {
            "decision": "highest_value_derivation_gap",
            "status": "B_mem_origin",
            "evidence": "B_mem/b_mem is the least structurally constrained amplitude and most dangerous free normalization",
            "next_action": "track as derivation target while running fair closure tests",
        },
    ]


def status_payload(run_dir: Path, counts: dict[str, int]) -> dict[str, Any]:
    return {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "timestamp": run_dir.name,
        "readout": "amplitudes_classified_none_fully_parent_derived",
        "key_metrics": {
            "amplitude_factors": counts["amplitude_register"],
            "gate_results": counts["gate_results"],
            "empirical_handling_rows": counts["empirical_handling"],
            "next_obligations": counts["next_obligations"],
            "fully_parent_derived_count": 0,
        },
        "decision": decision_rows()[0],
        "next_target": "83-empirical-closure-test-manifest.md",
    }


def run(output_root: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-amplitude-normalization-gate"
    result_dir = run_dir / "results"

    tables: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_checkpoint_register": (
            source_register_rows(),
            ["source_key", "relative_path", "absolute_path", "exists"],
        ),
        "amplitude_register": (
            amplitude_register_rows(),
            ["factor", "symbol_or_value", "sector", "current_evidence", "classification", "allowed_use", "must_not_claim"],
        ),
        "gate_results": (
            gate_result_rows(),
            ["gate", "result", "reason"],
        ),
        "empirical_handling": (
            empirical_handling_rows(),
            ["factor", "empirical_handling", "baseline_requirement"],
        ),
        "next_obligations": (
            next_obligation_rows(),
            ["obligation", "question", "next_test"],
        ),
        "decision": (
            decision_rows(),
            ["decision", "status", "evidence", "next_action"],
        ),
    }

    counts: dict[str, int] = {}
    for table_name, (rows, fieldnames) in tables.items():
        write_csv(result_dir / f"{table_name}.csv", rows, fieldnames)
        counts[table_name] = len(rows)

    status = status_payload(run_dir, counts)
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    return run_dir


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-root",
        type=Path,
        default=POST_CHECKPOINT / "runs",
        help="Directory where timestamped run output is written.",
    )
    args = parser.parse_args()

    run_dir = run(args.output_root)
    status = json.loads((run_dir / "status.json").read_text(encoding="utf-8"))
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
