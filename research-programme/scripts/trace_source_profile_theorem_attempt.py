from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "trace-source-profile-theorem-attempt"
STATUS = "trace_source_flat_profile_conditional_neumann_theorem_not_parent_derived"
CLAIM_CEILING = "conditional_flat_profile_theorem_no_fifth_force_or_local_GR_promotion"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "298-open-boundary-parent-sector-attempt.md", "trace source coupling in open sector"),
        (ROOT / "299-local-silence-selector-attempt.md", "local selector and epsilon_loc contract"),
        (ROOT / "305-fifth-force-gradient-runner.md", "gradient runner and profile-scale blocker"),
        (ROOT / "runs" / "20260601-000128-fifth-force-gradient-runner" / "results" / "gradient_results.csv", "gradient runner results"),
        (ROOT / "scripts" / "trace_source_profile_theorem_attempt.py", "this profile theorem attempt"),
    ]
    return [{"source": relpath(path), "role": role, "exists": "yes" if path.exists() else "no"} for path, role in sources]


def profile_equation_rows() -> list[dict[str, Any]]:
    return [
        {
            "object": "local_trace_source",
            "symbol": "s_D",
            "definition": "s_D = Lambda_D Tr(P_iso q_r)",
            "role": "local scalar source whose gradient can create fifth-force-like residuals",
            "status": "effective_source_from_open_sector",
        },
        {
            "object": "profile_functional",
            "symbol": "F_s",
            "definition": "integral_D [kappa_s/2 |grad s_D|^2 + m_s^2/2 (s_D-s0)^2 - j_s s_D]",
            "role": "minimal elliptic profile model for local trace source",
            "status": "constructed_effective_profile_contract",
        },
        {
            "object": "Euler_Lagrange_profile",
            "symbol": "(-kappa_s Laplacian + m_s^2)s_D = m_s^2 s0 + j_s",
            "definition": "local profile equation",
            "role": "determines whether s_D is flat or spatially varying",
            "status": "conditional_equation",
        },
        {
            "object": "Neumann_no_flux_boundary",
            "symbol": "n.grad s_D | boundary D = 0",
            "definition": "no local exchange of trace source through boundary",
            "role": "boundary condition that admits constant local profiles",
            "status": "not_parent_derived",
        },
        {
            "object": "inhomogeneous_local_source",
            "symbol": "j_s(x)",
            "definition": "domain-local forcing of trace source",
            "role": "if spatially varying, generically creates fifth-force gradient",
            "status": "danger_channel",
        },
    ]


def solution_class_rows() -> list[dict[str, Any]]:
    return [
        {
            "case": "exact_selector_silence",
            "conditions": "sigma_D=0 so s_D=0",
            "profile_result": "s_D constant zero",
            "gradient_result": "grad s_D=0",
            "status": "pass_exact",
            "blocker": "requires selector theorem",
        },
        {
            "case": "Neumann_constant_source",
            "conditions": "j_s constant, s0 constant, n.grad s_D=0",
            "profile_result": "s_D=(m_s^2 s0+j_s)/m_s^2 constant if m_s^2>0",
            "gradient_result": "grad s_D=0",
            "status": "conditional_flat_profile",
            "blocker": "Neumann/no-inhomogeneous-source conditions not parent-derived",
        },
        {
            "case": "massless_Neumann_constant_mode",
            "conditions": "m_s=0, j_s=0, n.grad s_D=0",
            "profile_result": "constant zero-mode allowed",
            "gradient_result": "grad s_D=0 but amplitude undetermined",
            "status": "flat_but_amplitude_unowned",
            "blocker": "zero-mode normalization/constant source still closure",
        },
        {
            "case": "Dirichlet_mismatch",
            "conditions": "boundary values differ across local domain",
            "profile_result": "s_D interpolates between boundary values",
            "gradient_result": "grad s_D nonzero",
            "status": "fail_gradient_risk",
            "blocker": "requires fifth-force runner/bound",
        },
        {
            "case": "localized_inhomogeneous_source",
            "conditions": "j_s(x) spatially varying",
            "profile_result": "Yukawa/Poisson-like profile",
            "gradient_result": "grad s_D generically nonzero",
            "status": "fail_gradient_risk",
            "blocker": "must be screened, flattened, or exactly silenced",
        },
    ]


def gradient_implication_rows() -> list[dict[str, Any]]:
    return [
        {
            "profile_condition": "exact selector silence",
            "runner_mapping": "epsilon_loc=0",
            "fifth_force_status": "pass_exact_zero_gradient",
            "promotion_status": "conditional_on_selector_theorem",
        },
        {
            "profile_condition": "constant trace source",
            "runner_mapping": "shape_factor=0",
            "fifth_force_status": "pass_exact_zero_gradient",
            "promotion_status": "conditional_on_parent_boundary_profile_theorem",
        },
        {
            "profile_condition": "very flat nonzero source",
            "runner_mapping": "L_profile >> L_test",
            "fifth_force_status": "pass_proxy_gradient_bound_if_flat_enough",
            "promotion_status": "requires derived profile scale",
        },
        {
            "profile_condition": "localized source or boundary mismatch",
            "runner_mapping": "L_profile ~ L_test and shape_factor ~ 1",
            "fifth_force_status": "fail_proxy_gradient_bound_for_beta_bounded_leakage",
            "promotion_status": "requires exact silence or official bound/screening",
        },
    ]


def no_go_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim": "trace-only source automatically means no fifth force",
            "result": "fail",
            "reason": "trace-only controls tensor structure, not spatial profile",
            "consequence": "need flatness or selector silence",
        },
        {
            "claim": "constant profile can be assumed locally",
            "result": "fail_as_derivation",
            "reason": "constant profile requires boundary/no-source conditions",
            "consequence": "flatness is a theorem target, not an axiom",
        },
        {
            "claim": "mass term always screens gradients safely",
            "result": "partial",
            "reason": "screening reduces range but can still create local gradients near sources/boundaries",
            "consequence": "must run gradient bound",
        },
        {
            "claim": "nonzero bounded beta leakage is automatically locally safe",
            "result": "fail",
            "reason": "beta bound does not test spatial acceleration gradients",
            "consequence": "fifth-force runner remains required",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    source_missing = [source for source in source_register_rows() if source["exists"] != "yes"]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not source_missing else "fail",
            "evidence": "all cited checkpoints/scripts exist" if not source_missing else ";".join(source["source"] for source in source_missing),
            "claim_effect": "attempt traceable",
        },
        {
            "gate": "profile_equation_constructed",
            "status": "pass",
            "evidence": "(-kappa Laplacian + m^2)s = m^2 s0 + j_s",
            "claim_effect": "trace-source flatness is now a profile theorem target",
        },
        {
            "gate": "constant_profile_sufficient_condition",
            "status": "conditional_pass",
            "evidence": "constant source plus Neumann no-flux gives grad s_D=0",
            "claim_effect": "fifth-force can vanish for nonzero epsilon if profile theorem holds",
        },
        {
            "gate": "profile_parent_derived",
            "status": "fail",
            "evidence": "parent action has not derived Neumann/no-inhomogeneous-source conditions",
            "claim_effect": "flatness not promoted",
        },
        {
            "gate": "localized_source_safe",
            "status": "fail",
            "evidence": "localized j_s or boundary mismatch generically creates gradients",
            "claim_effect": "nonzero local leakage remains dangerous without exact silence/flatness",
        },
        {
            "gate": "official_fifth_force_claim_allowed",
            "status": "fail",
            "evidence": "no official fifth-force bound or parent profile scale",
            "claim_effect": "no local evidence claim",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "selector and profile theorem remain conditional",
            "claim_effect": "local branch remains unpromoted",
        },
        {
            "gate": "B_mem_parent_derived",
            "status": "fail",
            "evidence": "profile theorem does not derive 2/27 amplitude",
            "claim_effect": "amplitude remains closure/theorem target",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "A flat local trace profile can be derived from an effective elliptic profile equation if the local domain "
                "has Neumann/no-flux boundary conditions and no spatially varying inhomogeneous trace source. That would make "
                "nonzero epsilon_loc fifth-force safe at the profile level. But those boundary/no-source conditions are not "
                "parent-derived, and localized sources or boundary mismatch generically create gradients."
            ),
            "next_target": "local_branch_status_ledger_or_stronger_empirical_holdout",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "profile_equation.csv": (
            profile_equation_rows(),
            ["object", "symbol", "definition", "role", "status"],
        ),
        "solution_classes.csv": (
            solution_class_rows(),
            ["case", "conditions", "profile_result", "gradient_result", "status", "blocker"],
        ),
        "gradient_implications.csv": (
            gradient_implication_rows(),
            ["profile_condition", "runner_mapping", "fifth_force_status", "promotion_status"],
        ),
        "no_go_tests.csv": (
            no_go_rows(),
            ["claim", "result", "reason", "consequence"],
        ),
        "promotion_gates.csv": (
            gate_rows(),
            ["gate", "status", "evidence", "claim_effect"],
        ),
        "decision.csv": (
            decision_rows(),
            ["decision", "claim_ceiling", "meaning", "next_target"],
        ),
    }
    for filename, (rows, fieldnames) in outputs.items():
        write_csv(results_dir / filename, rows, fieldnames)

    payload = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(outputs),
        "flat_profile_condition_identified": True,
        "profile_parent_derived_now": False,
        "official_fifth_force_claim_now": False,
        "local_GR_promoted_now": False,
        "B_mem_parent_derived_now": False,
        "next_target": "local_branch_status_ledger_or_stronger_empirical_holdout",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Trace-source profile theorem attempt.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
