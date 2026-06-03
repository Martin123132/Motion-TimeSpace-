#!/usr/bin/env python3
"""Write the parent-variation contract for C_coh and its dependencies."""

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
    "64_binding_invariant_doc": Path("64-binding-invariant-domain-selector-attempt.md"),
    "70_Ccoh_variation_doc": Path("70-Ccoh-variation-and-boundary-current-audit.md"),
    "73_blocker_doc": Path("73-local-route-blocker-ledger-and-promotion-gate.md"),
    "74_priority_doc": Path("74-next-derivation-priority-decision.md"),
    "74_status": Path("runs/20260531-114253-next-derivation-priority-decision/status.json"),
    "74_priority": Path("runs/20260531-114253-next-derivation-priority-decision/results/priority_ranking.csv"),
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


def dependency_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "dependency": "observer_congruence_u_mu",
            "appears_in": "theta, sigma, omega, spatial projector h_munu",
            "required_owner": "unit timelike field, æther-like frame, matter-flow frame, or tetrad/coframe variable varied in action",
            "current_status": "open",
            "failure_if_missing": "C_coh is frame-selected by hand",
        },
        {
            "dependency": "spatial_metric_h_munu",
            "appears_in": "decomposition Theta_ij=(1/3)theta h_ij+sigma_ij and norms",
            "required_owner": "derived from g_munu and u_mu with metric variation included",
            "current_status": "partial_contract",
            "failure_if_missing": "delta_g C_coh is incomplete",
        },
        {
            "dependency": "theta_expansion",
            "appears_in": "<theta>_D and <theta^2>_D",
            "required_owner": "theta=nabla_mu u^mu or equivalent motion-load scalar from parent kinematics",
            "current_status": "partial_kinematic",
            "failure_if_missing": "volume-flow silence is diagnostic only",
        },
        {
            "dependency": "sigma_omega_invariants",
            "appears_in": "denominator suppression of shear/orbital/local motion",
            "required_owner": "covariant decomposition of nabla_mu u_nu with metric/u variations",
            "current_status": "open",
            "failure_if_missing": "local shear suppression is hand-selected",
        },
        {
            "dependency": "domain_average_D",
            "appears_in": "all angle-bracket averages and boundary current",
            "required_owner": "chi_D auxiliary selector, relative class, or parent domain field",
            "current_status": "critical_open",
            "failure_if_missing": "averaging window is a hidden fitting/smoothing rule",
        },
        {
            "dependency": "volume_measure_dSigma",
            "appears_in": "V_D and all domain averages",
            "required_owner": "induced spatial measure from h_munu, varied with metric and boundary",
            "current_status": "partial_contract",
            "failure_if_missing": "Bianchi variation misses measure terms",
        },
        {
            "dependency": "eps_D_quiet_limit",
            "appears_in": "regularized C_coh denominator",
            "required_owner": "strict limiting prescription eps_D -> 0+ or parent-derived invariant floor",
            "current_status": "open",
            "failure_if_missing": "eps_D becomes a hidden threshold",
        },
        {
            "dependency": "boundary_motion",
            "appears_in": "variation of D and local-to-FLRW exchange",
            "required_owner": "relative boundary current or domain selector field equation",
            "current_status": "critical_open",
            "failure_if_missing": "boundary exchange current is uncontrolled",
        },
    ]


def variation_obligation_rows() -> list[dict[str, Any]]:
    return [
        {
            "obligation": "delta_g_Ccoh",
            "contract": "metric variation must include h_munu, dSigma, theta/sigma/omega norms, and boundary support",
            "status": "required_not_done",
            "next_test": "76-Ccoh-Bianchi-identity-attempt.md",
        },
        {
            "obligation": "delta_u_Ccoh",
            "contract": "variation of observer congruence must be included or u must be constrained with its own E_u equation",
            "status": "required_not_done",
            "next_test": "u-frame owner decision inside 76",
        },
        {
            "obligation": "delta_domain_Ccoh",
            "contract": "domain variation must produce a boundary/exchange term, not be frozen",
            "status": "required_not_done",
            "next_test": "boundary-current term in 76",
        },
        {
            "obligation": "quiet_bulk_limit",
            "contract": "C_coh=0 constant branches must make delta C_coh vanish in local bulk on shell",
            "status": "pass_conditional",
            "next_test": "local branch in 76",
        },
        {
            "obligation": "FLRW_background_limit",
            "contract": "C_coh=1 constant branch must recover memory background and avoid extra exchange in homogeneous limit",
            "status": "pass_contract",
            "next_test": "FLRW branch in 76",
        },
        {
            "obligation": "perturbation_limit",
            "contract": "C_coh perturbations must have a defined conserved response or be explicitly out of scope",
            "status": "open",
            "next_test": "defer to perturbation contract after 76",
        },
    ]


def owner_options_rows() -> list[dict[str, Any]]:
    return [
        {
            "option": "full_variational_u_chiD_owner",
            "description": "u_mu, chi_D/domain, and metric all varied; C_coh is composite but fully variational",
            "pros": "most field-theoretic and Bianchi-clean if it works",
            "cons": "hard; may introduce extra equations/constraints",
            "status": "best_if_successful",
        },
        {
            "option": "constrained_auxiliary_owner",
            "description": "u_mu and chi_D are constrained/nonpropagating variables with multiplier equations",
            "pros": "keeps local stress controlled",
            "cons": "risks imposing rather than deriving the frame/domain",
            "status": "live",
        },
        {
            "option": "pure_diagnostic_Ccoh",
            "description": "C_coh used only after solving parent equations, not inside action",
            "pros": "safe as an analysis diagnostic",
            "cons": "cannot gate S_mem or derive local GR",
            "status": "demotion_option",
        },
        {
            "option": "frozen_Ccoh_in_action",
            "description": "C_coh inserted into S_gate but not varied",
            "pros": "easy",
            "cons": "fake Bianchi identity",
            "status": "rejected",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "dependencies_listed",
            "status": "pass",
            "detail": "u,h,theta,sigma,omega,D,dSigma,eps_D,boundary motion are explicit",
        },
        {
            "gate": "frozen_Ccoh_rejected",
            "status": "pass",
            "detail": "C_coh cannot be inserted into action without variation",
        },
        {
            "gate": "parent_owners_available",
            "status": "open",
            "detail": "candidate owner routes exist, but none is derived",
        },
        {
            "gate": "local_bulk_limit_specified",
            "status": "pass_conditional",
            "detail": "constant C_coh=0 bulk can be safe if parent local solution exists",
        },
        {
            "gate": "FLRW_limit_specified",
            "status": "pass_contract",
            "detail": "constant C_coh=1 background can recover memory branch",
        },
        {
            "gate": "metric_variation_ready",
            "status": "fail",
            "detail": "delta_g C_coh is contracted but not computed",
        },
        {
            "gate": "Bianchi_attempt_ready",
            "status": "pass",
            "detail": "the next calculation has a precise dependency list",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "detail": "contract does not prove conservation or local GR",
        },
        {
            "gate": "support_claim_allowed",
            "status": "fail",
            "detail": "this is ownership discipline, not evidence",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "Ccoh_parent_variation_status",
            "status": "contract_written_variation_not_computed",
            "evidence": "all C_coh dependencies and required variations are named; no full delta_g/delta_u/delta_D calculation yet",
            "next_action": "attempt Ccoh/Bianchi identity with these dependencies included",
        },
        {
            "decision": "local_route_status",
            "status": "eligible_for_Bianchi_attempt_not_promotion",
            "evidence": "frozen diagnostic route is rejected, but parent owner options remain live",
            "next_action": "create 76-Ccoh-Bianchi-identity-attempt.md",
        },
        {
            "decision": "recommended_next_target",
            "status": "76-Ccoh-Bianchi-identity-attempt.md",
            "evidence": "checkpoint 75 gives the contract; checkpoint 76 must try the actual conservation math",
            "next_action": "compute whether exchange terms can close or force demotion",
        },
    ]


def status_payload(run_dir: Path, counts: dict[str, int]) -> dict[str, Any]:
    gates = gate_rows()
    return {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "timestamp": run_dir.name.removeprefix("run-"),
        "readout": "contract_written_variation_not_computed",
        "key_metrics": {
            "dependencies": counts["dependency_contract"],
            "variation_obligations": counts["variation_obligations"],
            "owner_options": counts["owner_options"],
            "failed_gates": sum(1 for row in gates if row["status"] == "fail"),
            "open_gates": sum(1 for row in gates if row["status"] == "open"),
            "conditional_pass_gates": sum(1 for row in gates if row["status"] == "pass_conditional"),
        },
        "decision": decision_rows()[0],
        "next_target": "76-Ccoh-Bianchi-identity-attempt.md",
    }


def run(output_root: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-Ccoh-parent-variation-contract"
    result_dir = run_dir / "results"

    tables: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_checkpoint_register": (
            source_register_rows(),
            ["source_key", "relative_path", "absolute_path", "exists"],
        ),
        "dependency_contract": (
            dependency_contract_rows(),
            ["dependency", "appears_in", "required_owner", "current_status", "failure_if_missing"],
        ),
        "variation_obligations": (
            variation_obligation_rows(),
            ["obligation", "contract", "status", "next_test"],
        ),
        "owner_options": (
            owner_options_rows(),
            ["option", "description", "pros", "cons", "status"],
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
