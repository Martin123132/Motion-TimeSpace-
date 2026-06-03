#!/usr/bin/env python3
"""Write the auxiliary/no-independent-stress chi_D selector parent contract."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]

SOURCE_PATHS = {
    "64_binding_invariant_doc": Path("64-binding-invariant-domain-selector-attempt.md"),
    "65_phase_field_doc": Path("65-Ccoh-phase-field-selector-attempt.md"),
    "66_stress_scale_doc": Path("66-chiD-stress-and-scale-gate.md"),
    "66_status": Path("runs/20260531-111832-chiD-stress-and-scale-gate/status.json"),
    "66_stress_chain": Path("runs/20260531-111832-chiD-stress-and-scale-gate/results/stress_equation_chain.csv"),
    "66_scale_options": Path("runs/20260531-111832-chiD-stress-and-scale-gate/results/scale_option_ledger.csv"),
    "66_gates": Path("runs/20260531-111832-chiD-stress-and-scale-gate/results/gate_results.csv"),
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


def parent_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "obligation": "nonpropagating_selector",
            "contract": "chi_D has no independent kinetic term and no propagating local degree of freedom",
            "reason": "avoid fifth-force/PPN stress from selector gradients",
            "status": "required",
            "failure_mode": "dynamical chi_D reintroduces T_chi and ell_chi",
        },
        {
            "obligation": "constraint_equation",
            "contract": "variation enforces chi_D = C_coh or an equivalent monotone projector of C_coh",
            "reason": "local/FLRW branch split comes from coherent-volume invariant, not data threshold",
            "status": "required",
            "failure_mode": "selector becomes arbitrary window field",
        },
        {
            "obligation": "on_shell_no_stress",
            "contract": "constraint sector stress vanishes on shell or is included as a conserved boundary/topological term",
            "reason": "cannot delete stress by decree",
            "status": "required",
            "failure_mode": "fake local-GR recovery",
        },
        {
            "obligation": "metric_variation_includes_Ccoh",
            "contract": "variation of C_coh through theta, sigma, omega, averaging, and u^mu is included",
            "reason": "Bianchi identity is not valid if C_coh is frozen by hand",
            "status": "required",
            "failure_mode": "hidden conservation violation",
        },
        {
            "obligation": "memory_coupling_owner",
            "contract": "chi_D gates only the scalar coherent memory channel, not all gravity or matter",
            "reason": "preserve local GR and avoid erasing galaxy/dynamic sectors",
            "status": "required",
            "failure_mode": "over-broad switch kills physical content",
        },
        {
            "obligation": "no_empirical_threshold",
            "contract": "no C_star or per-system fitted smoothing length appears unless parent-derived",
            "reason": "avoid hidden MOND/window knob",
            "status": "required",
            "failure_mode": "phenomenological patch",
        },
    ]


def candidate_parent_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "algebraic_multiplier",
            "schematic_action": "S_aux = integral sqrt(-g) lambda_chi (chi_D - C_coh)",
            "variations": "delta_lambda -> chi_D=C_coh; delta_chi -> lambda_chi=0",
            "stress_result": "on-shell lambda_chi=0 makes direct constraint stress vanish",
            "verdict": "best_minimal_contract",
            "risk": "imposes the invariant projector rather than deriving C_coh itself",
        },
        {
            "candidate": "topological_boundary_projector",
            "schematic_action": "S_aux = boundary/relative-class pairing with chi_D as projector",
            "variations": "enforces allowed relative class without propagating local scalar",
            "stress_result": "can be metric-independent or boundary-conserved if constructed correctly",
            "verdict": "best_long_term_route",
            "risk": "needs explicit relative-class construction and memory coupling",
        },
        {
            "candidate": "nondynamical_background_window",
            "schematic_action": "insert chi_D=C_coh by definition in S_mem",
            "variations": "none",
            "stress_result": "no selector stress",
            "verdict": "rejected_too_weak",
            "risk": "not a variational theory",
        },
        {
            "candidate": "small_stress_dynamic_scalar",
            "schematic_action": "phase-field action with tiny rho_chi",
            "variations": "dynamical chi equation",
            "stress_result": "small but nonzero T_chi",
            "verdict": "deferred",
            "risk": "new hierarchy and ell_chi remain",
        },
    ]


def variation_chain_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "statement": "S_aux = integral sqrt(-g) lambda_chi (chi_D - C_coh)",
            "result": "minimal algebraic constraint owner",
            "status": "candidate",
            "gap": "C_coh still depends on parent-defined congruence and averaging",
        },
        {
            "step": 2,
            "statement": "delta S_aux / delta lambda_chi = 0 -> chi_D = C_coh",
            "result": "selector follows coherent-volume invariant with no threshold",
            "status": "pass_contract",
            "gap": "smooth projector, not sharp relative boundary",
        },
        {
            "step": 3,
            "statement": "delta S_aux / delta chi_D = 0 -> lambda_chi = 0 if chi_D appears nowhere else",
            "result": "direct constraint stress vanishes on shell",
            "status": "pass_conditional",
            "gap": "if S_mem depends on chi_D, lambda_chi is replaced by memory-channel source",
        },
        {
            "step": 4,
            "statement": "delta_g S_aux includes lambda_chi delta_g C_coh and metric determinant terms",
            "result": "vanishes only if lambda_chi=0 or is cancelled/included in total stress",
            "status": "Bianchi_warning",
            "gap": "must redo with memory coupling included",
        },
        {
            "step": 5,
            "statement": "S_mem[chi_D,C_coh,Q] changes delta_chi equation to lambda_chi = -delta S_mem/delta chi_D",
            "result": "selector stress may reappear through the memory channel",
            "status": "open",
            "gap": "next target is memory-coupling conservation",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "no_independent_kinetic_stress",
            "status": "pass",
            "detail": "auxiliary contract removes chi_D kinetic gradients and ell_chi",
        },
        {
            "gate": "threshold_free_selection",
            "status": "pass",
            "detail": "chi_D=C_coh uses invariant value rather than C_star",
        },
        {
            "gate": "on_shell_constraint_stress_safe",
            "status": "pass_conditional",
            "detail": "minimal multiplier has lambda_chi=0 on shell before memory coupling",
        },
        {
            "gate": "memory_coupled_Bianchi_resolved",
            "status": "open",
            "detail": "once S_mem depends on chi_D, lambda_chi and metric variation must be recomputed",
        },
        {
            "gate": "Ccoh_parent_derived",
            "status": "fail",
            "detail": "C_coh still needs parent congruence/averaging/domain derivation",
        },
        {
            "gate": "sharp_relative_boundary_derived",
            "status": "open",
            "detail": "chi_D=C_coh is smooth; relative cohomology boundary still needs a class owner",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "detail": "contract is cleaner but not yet a full GR reduction",
        },
        {
            "gate": "support_claim_allowed",
            "status": "fail",
            "detail": "this is a parent contract, not empirical support",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "auxiliary_selector_status",
            "status": "minimal_no_stress_contract_written_memory_coupling_open",
            "evidence": "algebraic multiplier can enforce chi_D=C_coh without kinetic stress, but S_mem coupling reopens Bianchi/stress accounting",
            "next_action": "derive memory-channel coupling with chi_D and total conservation",
        },
        {
            "decision": "local_GR_route_status",
            "status": "cleaner_but_still_unpromoted",
            "evidence": "ell_chi is removed in auxiliary route, but C_coh ownership and memory coupling are unresolved",
            "next_action": "write conserved chi_D-gated memory stress contract",
        },
        {
            "decision": "recommended_next_target",
            "status": "68-chiD-gated-memory-conservation-contract.md",
            "evidence": "the selector only matters through the memory sector; conservation must be checked there",
            "next_action": "state exact condition for nabla_mu(T_mem[chi_D]+T_matter+T_aux)=0",
        },
    ]


def status_payload(run_dir: Path, counts: dict[str, int]) -> dict[str, Any]:
    gates = gate_rows()
    return {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "timestamp": run_dir.name.removeprefix("run-"),
        "readout": "minimal_no_stress_contract_written_memory_coupling_open",
        "key_metrics": {
            "contract_obligations": counts["parent_contract_obligations"],
            "candidate_parents": counts["candidate_parent_routes"],
            "variation_steps": counts["variation_chain"],
            "failed_gates": sum(1 for row in gates if row["status"] == "fail"),
            "open_gates": sum(1 for row in gates if row["status"] == "open"),
            "conditional_pass_gates": sum(1 for row in gates if row["status"] == "pass_conditional"),
        },
        "decision": decision_rows()[0],
        "next_target": "68-chiD-gated-memory-conservation-contract.md",
    }


def run(output_root: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-auxiliary-selector-parent-contract"
    result_dir = run_dir / "results"

    tables: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_checkpoint_register": (
            source_register_rows(),
            ["source_key", "relative_path", "absolute_path", "exists"],
        ),
        "parent_contract_obligations": (
            parent_contract_rows(),
            ["obligation", "contract", "reason", "status", "failure_mode"],
        ),
        "candidate_parent_routes": (
            candidate_parent_rows(),
            ["candidate", "schematic_action", "variations", "stress_result", "verdict", "risk"],
        ),
        "variation_chain": (
            variation_chain_rows(),
            ["step", "statement", "result", "status", "gap"],
        ),
        "gate_results": (
            gate_rows(),
            ["gate", "status", "detail"],
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
