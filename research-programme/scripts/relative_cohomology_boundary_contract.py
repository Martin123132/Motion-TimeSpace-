#!/usr/bin/env python3
"""Write the relative-cohomology boundary contract for local-zero / FLRW-nonzero memory."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]

SOURCE_PATHS = {
    "53_projection_doc": Path("53-coherent-projection-local-silence-gate.md"),
    "59_topological_doc": Path("59-topological-cell-current-owner-attempt.md"),
    "59_status": Path("runs/20260531-105343-topological-cell-current-owner-attempt/status.json"),
    "59_no_charge_tests": Path("runs/20260531-105343-topological-cell-current-owner-attempt/results/no_charge_tests.csv"),
    "59_branch_selection": Path("runs/20260531-105343-topological-cell-current-owner-attempt/results/branch_selection_tests.csv"),
    "59_gates": Path("runs/20260531-105343-topological-cell-current-owner-attempt/results/gate_results.csv"),
}


def absolute_source(key: str) -> Path:
    return POST_CHECKPOINT / SOURCE_PATHS[key]


def load_json(key: str) -> dict[str, Any]:
    return json.loads(absolute_source(key).read_text(encoding="utf-8"))


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


def boundary_rule_rows() -> list[dict[str, Any]]:
    return [
        {
            "rule": "relative_pair",
            "statement": "memory class lives in H^3(D,boundary D) or equivalent relative cell-flux group",
            "status": "contract_candidate",
            "local_result": "if boundary volume-flow is stationary, relative class is trivial",
            "FLRW_result": "if boundary is coherent expansion domain, relative class can be nontrivial",
            "risk": "choice of relative group could be post-hoc unless parent domain rule fixes it",
        },
        {
            "rule": "stationary_boundary_zero",
            "statement": "dV_boundary/dtau=0 implies boundary cell flux vanishes",
            "status": "pass_conditional",
            "local_result": "bound solar/virial domains carry zero memory-cell class",
            "FLRW_result": "does not erase expanding FLRW boundary",
            "risk": "needs parent proof that local bound boundaries are the relevant boundaries",
        },
        {
            "rule": "coherent_expansion_boundary_nonzero",
            "statement": "d ln V_D/dtau=3H on coherent FLRW domain sources nonzero class",
            "status": "pass_conditional",
            "local_result": "not triggered by stationary domains",
            "FLRW_result": "produces the Q_coh/N memory branch",
            "risk": "nonzero class still not shown to equal det(Q_coh) with X=4N",
        },
        {
            "rule": "bound_unbound_boundary_selection",
            "statement": "boundary is selected where coherent volume-flow changes class: expanding/unbound vs stationary/bound",
            "status": "open",
            "local_result": "could define local silence without PPN tuning",
            "FLRW_result": "keeps cosmic expansion as active class",
            "risk": "requires parent criterion for bound/unbound transition",
        },
        {
            "rule": "arbitrary_boundary_choice",
            "statement": "pick boundary to make local class zero and FLRW class nonzero",
            "status": "rejected",
            "local_result": "can always silence local tests",
            "FLRW_result": "can always preserve cosmology",
            "risk": "pure rescue knob, not theory",
        },
    ]


def local_flrw_split_rows() -> list[dict[str, Any]]:
    return [
        {
            "arena": "Minkowski_local_patch",
            "boundary_condition": "stationary boundary, dV_D/dtau=0",
            "relative_class": "trivial",
            "memory_result": "I_M=0",
            "status": "pass_conditional",
            "remaining_gap": "trivial but useful control",
        },
        {
            "arena": "stationary_solar_system",
            "boundary_condition": "bound volume boundary stable over PPN averaging",
            "relative_class": "trivial if bound-domain rule holds",
            "memory_result": "no quarter-branch local activation",
            "status": "pass_conditional",
            "remaining_gap": "derive bound-domain rule without importing GR",
        },
        {
            "arena": "virialized_galaxy",
            "boundary_condition": "time-averaged stable virial volume",
            "relative_class": "trivial for local memory channel",
            "memory_result": "local PPN-like hair suppressed; galaxy phenomenology must be separately mapped",
            "status": "pass_conditional",
            "remaining_gap": "avoid erasing intended galaxy empirical pillar",
        },
        {
            "arena": "FLRW_background",
            "boundary_condition": "coherent expanding domain, d ln V_D/dtau=3H",
            "relative_class": "nontrivial expansion class",
            "memory_result": "Q_coh=(N/u3)delta and I_M=det(Q_coh)",
            "status": "pass_conditional",
            "remaining_gap": "nontrivial class magnitude/normalization still not parent-derived",
        },
        {
            "arena": "FLRW_perturbations",
            "boundary_condition": "background plus fluctuating local expansion",
            "relative_class": "mixed/unknown",
            "memory_result": "perturbation response not defined",
            "status": "open",
            "remaining_gap": "needs perturbation/lensing owner",
        },
        {
            "arena": "collapse_merger_dynamic_boundary",
            "boundary_condition": "nonstationary local boundary",
            "relative_class": "possibly nontrivial",
            "memory_result": "dynamic memory signatures possible",
            "status": "open",
            "remaining_gap": "not a PPN baseline; needs strong-field/radiative treatment",
        },
    ]


def cohomology_selection_rows() -> list[dict[str, Any]]:
    return [
        {
            "target": "zero local class",
            "contract": "stationary or virialized bound boundary has trivial relative class",
            "status": "conditional_contract",
            "noncircularity_test": "boundary triviality must follow from dV_D/dtau=0, not from PPN residuals",
            "missing_theorem": "parent proof of bound-domain boundary",
        },
        {
            "target": "nonzero FLRW class",
            "contract": "coherent expansion boundary carries integrated volume-flow class",
            "status": "conditional_contract",
            "noncircularity_test": "class must be fixed by expansion geometry before fitting cosmology",
            "missing_theorem": "normalization to X=4N and det(Q_coh)",
        },
        {
            "target": "p=3 selection",
            "contract": "relative class pairs with spatial coherent triad/3-cycle",
            "status": "open",
            "noncircularity_test": "must derive why the class is spatial 3-form rather than arbitrary p",
            "missing_theorem": "spatial characteristic class or triad flux invariant",
        },
        {
            "target": "u3=1/4 selection",
            "contract": "boundary normalization uses 3+1 coherent coframe cell",
            "status": "open",
            "noncircularity_test": "must derive why four cell legs normalize the spatial flux",
            "missing_theorem": "3+1 relative cell theorem",
        },
        {
            "target": "b_mem amplitude",
            "contract": "boundary class magnitude maps to memory stress amplitude",
            "status": "missing",
            "noncircularity_test": "magnitude must not be fitted after shape survives",
            "missing_theorem": "stress/amplitude map",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "relative_boundary_contract_written",
            "status": "pass",
            "detail": "local-zero/FLRW-nonzero rule is stated as a relative boundary class contract",
        },
        {
            "gate": "local_zero_class_nonarbitrary",
            "status": "pass_conditional",
            "detail": "zero class follows from stationary dV_D/dtau=0 if bound-domain rule is parent-derived",
        },
        {
            "gate": "FLRW_nonzero_class_nonarbitrary",
            "status": "pass_conditional",
            "detail": "nonzero class follows from coherent d ln V_D/dtau=3H if domain rule is parent-derived",
        },
        {
            "gate": "bound_domain_rule_parent_derived",
            "status": "fail",
            "detail": "no parent rule yet defines bound/unbound boundaries",
        },
        {
            "gate": "p3_selected_by_cohomology",
            "status": "open",
            "detail": "spatial 3-cycle/triad class is plausible but not constructed",
        },
        {
            "gate": "u3_quarter_selected_by_boundary_rule",
            "status": "open",
            "detail": "3+1 normalization is plausible but not selected by relative class yet",
        },
        {
            "gate": "bmem_amplitude_selected",
            "status": "fail",
            "detail": "boundary class magnitude not mapped to memory stress amplitude",
        },
        {
            "gate": "support_claim_allowed",
            "status": "fail",
            "detail": "contract is not derivation or empirical support",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "relative_cohomology_boundary_status",
            "status": "contract_written_not_derived",
            "evidence": "local-zero/FLRW-nonzero split can be stated non-arbitrarily using stationary vs coherent-expanding boundaries",
            "next_action": "attempt bound-domain boundary theorem",
        },
        {
            "decision": "topological_owner_status",
            "status": "still_live_but_not_branch_derivation",
            "evidence": "relative boundary contract improves noncircularity but leaves p=3/u3=1/4 selection open",
            "next_action": "derive spatial 3-cycle and 3+1 normalization or demote",
        },
        {
            "decision": "recommended_next_target",
            "status": "61-bound-domain-boundary-theorem-attempt.md",
            "evidence": "local silence now depends on parent-derived bound-domain boundary",
            "next_action": "try to derive dV_D/dtau=0 boundary rule for local bound systems",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Relative cohomology boundary contract.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    source_register = source_register_rows()
    status_59 = load_json("59_status")

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or POST_CHECKPOINT / "runs" / f"{timestamp}-relative-cohomology-boundary-contract"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    boundary = boundary_rule_rows()
    split = local_flrw_split_rows()
    selection = cohomology_selection_rows()
    gates = gate_rows()
    decisions = decision_rows()

    write_csv(results_dir / "source_checkpoint_register.csv", source_register, list(source_register[0].keys()))
    write_csv(results_dir / "boundary_rule_contract.csv", boundary, list(boundary[0].keys()))
    write_csv(results_dir / "local_FLRW_split_tests.csv", split, list(split[0].keys()))
    write_csv(results_dir / "cohomology_selection_requirements.csv", selection, list(selection[0].keys()))
    write_csv(results_dir / "gate_results.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "decision.csv", decisions, list(decisions[0].keys()))

    status = {
        "status": "complete_relative_cohomology_boundary_contract",
        "readout": "relative_boundary_contract_written_not_derived",
        "recommendation": "attempt_bound_domain_boundary_theorem_next",
        "next_target": "61-bound-domain-boundary-theorem-attempt.md",
        "support_claim_allowed": False,
        "public_claim_allowed": False,
        "best_contract": "stationary bound domains trivial relative class; coherent FLRW domains nontrivial expansion class",
        "key_metrics": {
            "u3_quarter": status_59["key_metrics"]["u3_quarter"],
            "boundary_rules": len(boundary),
            "local_FLRW_split_tests": len(split),
            "selection_requirements": len(selection),
            "failed_gates": sum(1 for row in gates if row["status"] == "fail"),
            "open_gates": sum(1 for row in gates if row["status"] == "open"),
            "conditional_pass_gates": sum(1 for row in gates if row["status"] == "pass_conditional"),
        },
        "outputs": {
            "source_checkpoint_register": str(results_dir / "source_checkpoint_register.csv"),
            "boundary_rule_contract": str(results_dir / "boundary_rule_contract.csv"),
            "local_FLRW_split_tests": str(results_dir / "local_FLRW_split_tests.csv"),
            "cohomology_selection_requirements": str(results_dir / "cohomology_selection_requirements.csv"),
            "gate_results": str(results_dir / "gate_results.csv"),
            "decision": str(results_dir / "decision.csv"),
            "status_json": str(out_dir / "status.json"),
        },
    }
    (out_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (out_dir / "log.txt").write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    (out_dir / "DONE.txt").write_text(status["readout"] + "\n", encoding="utf-8")
    print(json.dumps(status, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
