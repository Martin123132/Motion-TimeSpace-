#!/usr/bin/env python3
"""Compile the local-route blocker ledger and promotion gate."""

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
    "61_boundary_theorem_doc": Path("61-bound-domain-boundary-theorem-attempt.md"),
    "65_phase_selector_doc": Path("65-Ccoh-phase-field-selector-attempt.md"),
    "66_stress_scale_doc": Path("66-chiD-stress-and-scale-gate.md"),
    "67_aux_selector_doc": Path("67-auxiliary-selector-parent-contract.md"),
    "69_memory_gate_doc": Path("69-minimal-memory-gate-variation-attempt.md"),
    "70_Ccoh_variation_doc": Path("70-Ccoh-variation-and-boundary-current-audit.md"),
    "72_relative_owner_doc": Path("72-relative-current-action-owner-attempt.md"),
    "72_status": Path("runs/20260531-113740-relative-current-action-owner-attempt/status.json"),
    "72_gates": Path("runs/20260531-113740-relative-current-action-owner-attempt/results/gate_results.csv"),
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


def support_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "item": "coherent_volume_projector",
            "status": "support_conditional",
            "evidence": "P_coh[Theta]=(1/3)<theta>_D delta preserves FLRW and suppresses scalar local volume memory",
            "not_yet": "domain D and parent action not derived",
            "owner_checkpoint": "53",
        },
        {
            "item": "volume_flux_local_silence",
            "status": "support_conditional",
            "evidence": "dV_D/dtau=0 -> <theta>_D=0 -> Q_coh=0",
            "not_yet": "bound-domain boundary selected by parent equations",
            "owner_checkpoint": "61",
        },
        {
            "item": "C_coh_invariant",
            "status": "support_kinematic",
            "evidence": "C_coh separates coherent FLRW expansion from stationary/shear local domains without Newtonian potential",
            "not_yet": "averaging, congruence, eps_D, and domain ownership",
            "owner_checkpoint": "64",
        },
        {
            "item": "threshold_free_selector",
            "status": "support_conditional",
            "evidence": "chi=C_coh branch split avoids fitted threshold",
            "not_yet": "dynamical scalar stress unsafe; auxiliary route preferred",
            "owner_checkpoint": "65-67",
        },
        {
            "item": "action_based_memory_gate",
            "status": "support_conditional",
            "evidence": "minimal gate gives lambda_chi=-L_mem and on-shell C_coh L_mem",
            "not_yet": "T_Ccoh and boundary exchange current missing",
            "owner_checkpoint": "68-69",
        },
        {
            "item": "relative_boundary_current",
            "status": "formal_support",
            "evidence": "J_rel=(j_3,b_2) with d_rel J_rel=0 encodes local trivial and FLRW nontrivial classes",
            "not_yet": "physical representative and parent action not derived",
            "owner_checkpoint": "71-72",
        },
    ]


def blocker_rows() -> list[dict[str, Any]]:
    return [
        {
            "blocker": "bound_domain_rule",
            "severity": "critical",
            "current_state": "stationary/virial volume rule is plausible but not parent-derived",
            "promotion_requirement": "derive D/boundary selection without PPN or GR import",
            "next_test": "domain/congruence parent equation or demote to closure",
        },
        {
            "blocker": "Ccoh_parent_ownership",
            "severity": "critical",
            "current_state": "C_coh uses theta/sigma/omega/domain averages but their parent variational status is open",
            "promotion_requirement": "derive observer congruence, averaging, eps_D limit, and metric variation",
            "next_test": "C_coh parent-variable audit",
        },
        {
            "blocker": "Bianchi_conservation",
            "severity": "critical",
            "current_state": "minimal gate works algebraically but T_Ccoh/boundary current not derived",
            "promotion_requirement": "close nabla_mu T_total^munu=0 with memory, auxiliary selector, matter",
            "next_test": "derive exchange current or demote memory gate",
        },
        {
            "blocker": "relative_current_representative",
            "severity": "major",
            "current_state": "d_rel closure can be imposed; local-zero/FLRW-nonzero representative not selected",
            "promotion_requirement": "action selects physical representative, not just closure",
            "next_test": "representative selection or topological demotion",
        },
        {
            "blocker": "amplitude_normalization",
            "severity": "critical",
            "current_state": "p=3, u3=1/4, b_mem not selected by local/topological route",
            "promotion_requirement": "derive determinant degree, quarter normalization, and memory amplitude",
            "next_test": "return to amplitude theorem or empirical closure label",
        },
        {
            "blocker": "perturbations_lensing_growth",
            "severity": "major",
            "current_state": "background/local bulk discussed; perturbative current unresolved",
            "promotion_requirement": "define perturbation equations and lensing/growth response",
            "next_test": "perturbation conservation contract",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "local_bulk_silence",
            "required_evidence": "Q_coh=0 and T_mem=0 in stationary local interiors from parent equations",
            "current_status": "pass_conditional",
            "promote": "no",
        },
        {
            "gate": "FLRW_background_activity",
            "required_evidence": "Q_coh=(N/u3)delta and memory branch recovered from same equations",
            "current_status": "pass_contract",
            "promote": "no",
        },
        {
            "gate": "boundary_exchange",
            "required_evidence": "local-to-FLRW boundary exchange current conserved and not PPN-sized",
            "current_status": "fail_open",
            "promote": "no",
        },
        {
            "gate": "Bianchi_identity",
            "required_evidence": "full stress conservation with C_coh metric variation",
            "current_status": "fail",
            "promote": "no",
        },
        {
            "gate": "normalization_amplitude",
            "required_evidence": "p=3,u3=1/4,b_mem selected by action/topology or explicitly demoted",
            "current_status": "fail",
            "promote": "no",
        },
        {
            "gate": "empirical_test_readiness",
            "required_evidence": "closed equations produce local, background, perturbation observables",
            "current_status": "not_ready",
            "promote": "no",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "local_route_promotion_status",
            "status": "not_promoted_support_structure_retained",
            "evidence": "several conditional supports exist, but critical blockers remain in domain selection, Ccoh ownership, Bianchi conservation, and amplitude normalization",
            "next_action": "pivot from topology sub-branches to highest-value blocker: Bianchi/Ccoh ownership or amplitude normalization",
        },
        {
            "decision": "best_current_description",
            "status": "conditional_local_silence_closure_with_formal_conservation_support",
            "evidence": "quiet bulk and FLRW background are plausible at contract level, but boundary/current and perturbations are not derived",
            "next_action": "keep as internal route, no support claim",
        },
        {
            "decision": "recommended_next_target",
            "status": "74-next-derivation-priority-decision.md",
            "evidence": "need to choose between Ccoh/Bianchi derivation, amplitude normalization, or empirical test branch",
            "next_action": "rank next derivation by promotion value and failure risk",
        },
    ]


def status_payload(run_dir: Path, counts: dict[str, int]) -> dict[str, Any]:
    return {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "timestamp": run_dir.name.removeprefix("run-"),
        "readout": "local_route_not_promoted_support_structure_retained",
        "key_metrics": {
            "support_items": counts["support_ledger"],
            "critical_blockers": 4,
            "major_blockers": 2,
            "promotion_gates": counts["promotion_gate"],
            "promotable_gates": 0,
        },
        "decision": decision_rows()[0],
        "next_target": "74-next-derivation-priority-decision.md",
    }


def run(output_root: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-local-route-blocker-ledger-and-promotion-gate"
    result_dir = run_dir / "results"

    tables: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_checkpoint_register": (
            source_register_rows(),
            ["source_key", "relative_path", "absolute_path", "exists"],
        ),
        "support_ledger": (
            support_ledger_rows(),
            ["item", "status", "evidence", "not_yet", "owner_checkpoint"],
        ),
        "blocker_ledger": (
            blocker_rows(),
            ["blocker", "severity", "current_state", "promotion_requirement", "next_test"],
        ),
        "promotion_gate": (
            promotion_gate_rows(),
            ["gate", "required_evidence", "current_status", "promote"],
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
