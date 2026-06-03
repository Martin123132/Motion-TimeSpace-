#!/usr/bin/env python3
"""Checkpoint 246: auxiliary no-hair rank/bracket or local EH pivot."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

CHECKPOINT_246_NAME = "auxiliary-nohair-rank-bracket-or-local-EH-pivot"
RUN_245 = RUNS_ROOT / "20260601-000062-exact-relative-memory-or-projector-stress-bianchi"

STATUS = "N6_auxiliary_nohair_rank_necessary_not_sufficient_bracket_blocked_EH_exterior_pivot_selected_no_promotion"
CLAIM_CEILING = "N6_route_decision_no_auxiliary_nohair_or_local_EH_promotion"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_register_rows() -> list[dict[str, Any]]:
    paths = [
        (Path(__file__).resolve(), "checkpoint 246 runner"),
        (WORK_DIR / "222-parent-X-sector-degree-count-and-boundary-action.md", "first-order X route and degree-count hazard"),
        (WORK_DIR / "223-X-constraint-algebra-and-Khat-Gamma-constitutive-owner.md", "X multiplier and bracket blocker"),
        (WORK_DIR / "235-projector-stress-variation-or-nohair-constraint-algebra.md", "safe branch conditions and rank/bracket tests"),
        (WORK_DIR / "236-local-EH-operator-or-constraint-algebra-decision.md", "prior EH pivot decision"),
        (WORK_DIR / "245-exact-relative-memory-or-projector-stress-bianchi.md", "N4/N5 checkpoint and N6 next target"),
        (RUN_245 / "status.json", "checkpoint 245 machine status"),
        (RUN_245 / "results" / "local_gate_priority_after_245.csv", "local gate priority before N6 decision"),
    ]
    rows: list[dict[str, Any]] = []
    for path, role in paths:
        exists = path.exists()
        rows.append(
            {
                "source": path.name,
                "path": str(path),
                "exists": "yes" if exists else "no",
                "sha256": sha256_file(path) if exists and path.is_file() else "",
                "role": role,
                "issue": "" if exists else "missing",
            }
        )
    return rows


def auxiliary_nohair_test_rows() -> list[dict[str, Any]]:
    return [
        {
            "test": "no_regular_kinetic_X",
            "required_condition": "rank d2L/d(dot X)d(dot X)=0",
            "current_evidence": "first-order multiplier route exists",
            "status": "necessary_condition_met_conditionally",
            "failure_if_absent": "X becomes vector/scalar fifth-force hair",
        },
        {
            "test": "primary_constraint",
            "required_condition": "pi_X^nu approx 0 or pi_X^nu - sqrt(h)P^{0nu} approx 0",
            "current_evidence": "written as constraint template",
            "status": "formal_template",
            "failure_if_absent": "X phase-space variables propagate",
        },
        {
            "test": "secondary_constraint",
            "required_condition": "C_X^nu=-nabla_mu P[Y]^{mu nu}+J_eff[Y]^nu approx 0",
            "current_evidence": "source identity template",
            "status": "formal_template",
            "failure_if_absent": "q_loc source identity not enforced",
        },
        {
            "test": "bracket_closure",
            "required_condition": "{C_X^nu(x), C_X^rho(y)} closes on parent constraints",
            "current_evidence": "not computed",
            "status": "fail_blocked_by_missing_parent_symplectic_structure",
            "failure_if_absent": "secondary constraints can create new modes or inconsistency",
        },
        {
            "test": "P_constitutive_owner",
            "required_condition": "P^{mu nu}=partial V_def/partial Z_mu_nu from parent variables",
            "current_evidence": "contract identified but V_def/Z not derived",
            "status": "fail",
            "failure_if_absent": "P is a named tensor inserted to make the identity work",
        },
        {
            "test": "boundary_primitive_owner",
            "required_condition": "A_rel boundary primitive pure gauge from parent action",
            "current_evidence": "required by N4 but not selected",
            "status": "fail",
            "failure_if_absent": "relative memory hair can live on the boundary",
        },
    ]


def route_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "continue_constraint_algebra_now",
            "value": "direct N6 proof if brackets close",
            "blocker": "parent Y symplectic structure and boundary metric not derived",
            "decision": "defer",
            "reason": "bracket calculation would be theatre without owned Poisson structure",
        },
        {
            "route": "declare_auxiliary_by_rank_only",
            "value": "fast local no-hair story",
            "blocker": "rank-zero is necessary not sufficient",
            "decision": "reject",
            "reason": "would smuggle no-hair by assumption",
        },
        {
            "route": "pivot_to_local_EH_exterior_stack",
            "value": "finite sufficient route to Schwarzschild/beta=1",
            "blocker": "must carry all unresolved N1-N6 conditions explicitly",
            "decision": "select",
            "reason": "can build a no-promotion sufficiency theorem without pretending N6 is solved",
        },
    ]


def EH_exterior_stack_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition": "ordinary_matter_absent",
            "required_form": "T_matter|E=0 outside compact source",
            "status": "definition_of_exterior",
            "needed_for": "vacuum field equation",
        },
        {
            "condition": "N1_Meff",
            "required_form": "Pi_M flux conserved; M_eff constant",
            "status": "conditional_gate_from_244",
            "needed_for": "monopole source only",
        },
        {
            "condition": "N2_no_TF",
            "required_form": "tau_TF_AB=0 and no tangential shear",
            "status": "conditional_gate_from_243",
            "needed_for": "gamma/slip silence",
        },
        {
            "condition": "N3_universal_strict_coframe",
            "required_form": "Pi_matter=0 and beta_C^loc=0",
            "status": "conditional_gate_from_240_242",
            "needed_for": "WEP/clock/C trace-source silence",
        },
        {
            "condition": "N4_exact_relative_memory",
            "required_form": "P_mem J_rel=d_rel A_rel with pure-gauge boundary primitive",
            "status": "conditional_gate_from_245",
            "needed_for": "q_loc relative-memory silence",
        },
        {
            "condition": "N5_projector_stress",
            "required_form": "T_projector=0 or retained in conserved total stress",
            "status": "open",
            "needed_for": "Bianchi-safe q_loc/EH reduction",
        },
        {
            "condition": "N6_auxiliary_nohair",
            "required_form": "X/J_rel/V_def carry no exterior propagating degrees",
            "status": "open",
            "needed_for": "no fifth-force/beta hair",
        },
        {
            "condition": "metric_only_two_derivative_operator",
            "required_form": "S_ext[g]=(16piG)^-1 int sqrt(-g)(R-2Lambda)+boundary",
            "status": "target",
            "needed_for": "Schwarzschild exterior and beta=1",
        },
    ]


def coefficient_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual": "beta_minus_1",
            "status_after_246": "open_EH_stack_selected",
            "coefficient_status": "beta=1 only if N1-N6 plus metric-only EH exterior hold",
            "remaining_gap": "N5/N6 and EH operator",
        },
        {
            "residual": "G_eff_over_G_minus_1",
            "status_after_246": "unchanged_N1_conditional",
            "coefficient_status": "M_eff monopole condition needed",
            "remaining_gap": "Pi_M parent flux closure/calibration",
        },
        {
            "residual": "gamma_minus_1",
            "status_after_246": "unchanged_N2_conditional",
            "coefficient_status": "scalar-boundary no-shear route",
            "remaining_gap": "parent scalar-boundary owner",
        },
        {
            "residual": "Phi_minus_Psi",
            "status_after_246": "unchanged_N2_conditional",
            "coefficient_status": "tau_TF_AB=0 route",
            "remaining_gap": "parent no tangential shear theorem",
        },
        {
            "residual": "epsilon_matter",
            "status_after_246": "unchanged_N3_conditional",
            "coefficient_status": "strict coframe direct coupling zero",
            "remaining_gap": "R_loc parent selection",
        },
        {
            "residual": "alpha_clock",
            "status_after_246": "unchanged_direct_vertex_conditional",
            "coefficient_status": "direct clock memory vertex zero under strict coframe",
            "remaining_gap": "metric/C clock branch",
        },
    ]


def next_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "rank": 1,
            "target": "local_EH_exterior_sufficiency_stack",
            "why": "constraint algebra cannot close without parent symplectic structure",
            "action": "write exact EH exterior reduction theorem with all N-gates as assumptions, no promotion",
        },
        {
            "rank": 2,
            "target": "N5_projector_stress",
            "why": "EH stack cannot be Bianchi-safe while projector stress is open",
            "action": "derive zero-stress or retained-stress route",
        },
        {
            "rank": 3,
            "target": "N6_auxiliary_nohair",
            "why": "X/J_rel/V_def can still carry exterior degrees",
            "action": "return after parent symplectic structure is specified",
        },
        {
            "rank": 4,
            "target": "parent_symplectic_structure",
            "why": "needed for real bracket closure",
            "action": "derive boundary/parent Poisson structure for Y fields",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    missing_sources = sum(row["exists"] != "yes" for row in source_register_rows())
    return [
        {
            "gate": "all cited local sources exist",
            "status": "pass" if missing_sources == 0 else "fail",
            "evidence": f"missing={missing_sources}",
            "claim_allowed": "internal checkpoint only",
        },
        {
            "gate": "rank-zero X kinetic condition identified",
            "status": "conditional_pass",
            "evidence": "first-order multiplier route has no regular X kinetic term",
            "claim_allowed": "necessary condition only",
        },
        {
            "gate": "constraint algebra closed",
            "status": "fail",
            "evidence": "parent symplectic structure missing",
            "claim_allowed": "no",
        },
        {
            "gate": "auxiliary no-hair declared by rank only",
            "status": "fail",
            "evidence": "explicitly rejected as insufficient",
            "claim_allowed": "no",
        },
        {
            "gate": "local EH exterior pivot selected",
            "status": "pass",
            "evidence": "finite sufficiency stack with N1-N6 obligations",
            "claim_allowed": "route decision only",
        },
        {
            "gate": "local GR or PPN promoted",
            "status": "fail",
            "evidence": CLAIM_CEILING,
            "claim_allowed": "no",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "meaning": "N6 cannot be honestly derived from rank-zero alone. The X/J_rel/V_def sector has a viable multiplier template, but bracket closure and P[Y]/V_def ownership are blocked by the missing parent symplectic structure. Therefore auxiliary-by-assertion is rejected and the next disciplined move is to pivot to a local EH exterior sufficiency stack that carries every unresolved N-gate explicitly.",
            "main_gain": "the no-hair route is prevented from becoming handwaving, and the local EH pivot is selected with all assumptions visible",
            "main_failure": "N6, N5, and the metric-only EH exterior are still not parent-derived",
            "next_target": "247-local-EH-exterior-sufficiency-stack-no-promotion.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_246_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    nohair_rows = auxiliary_nohair_test_rows()
    route_rows = route_decision_rows()
    stack_rows = EH_exterior_stack_rows()
    coefficient_rows = coefficient_status_rows()
    next_rows = next_gate_rows()
    gates = claim_gate_rows()
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "auxiliary_nohair_rank_bracket_tests.csv": (
            nohair_rows,
            ["test", "required_condition", "current_evidence", "status", "failure_if_absent"],
        ),
        "route_decision_matrix.csv": (
            route_rows,
            ["route", "value", "blocker", "decision", "reason"],
        ),
        "EH_exterior_sufficiency_stack.csv": (
            stack_rows,
            ["condition", "required_form", "status", "needed_for"],
        ),
        "coefficient_status_after_246.csv": (
            coefficient_rows,
            ["residual", "status_after_246", "coefficient_status", "remaining_gap"],
        ),
        "next_gate_priority_after_246.csv": (
            next_rows,
            ["rank", "target", "why", "action"],
        ),
        "claim_gate_results.csv": (
            gates,
            ["gate", "status", "evidence", "claim_allowed"],
        ),
        "decision.csv": (
            decision,
            ["decision", "meaning", "main_gain", "main_failure", "next_target", "promotion_allowed", "claim_ceiling"],
        ),
    }
    for filename, file_data in files.items():
        rows, fieldnames = file_data
        write_csv(results_dir / filename, rows, fieldnames)

    status_payload = {
        "status": decision[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(files.keys()),
        "missing_sources": sum(row["exists"] != "yes" for row in source_rows),
        "rank_zero_X_condition_necessary_only": True,
        "constraint_algebra_closed": False,
        "auxiliary_nohair_derived": False,
        "local_EH_exterior_pivot_selected": True,
        "local_GR_promoted": False,
        "PPN_promoted": False,
        "promotion_allowed": False,
        "next_target": decision[0]["next_target"],
    }
    write_json(run_dir / "status.json", status_payload)
    (run_dir / "DONE.txt").write_text(status_payload["status"] + "\n", encoding="utf-8")
    return status_payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timestamp", default=None, help="Optional run timestamp prefix.")
    args = parser.parse_args()
    print(json.dumps(run(args.timestamp), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
