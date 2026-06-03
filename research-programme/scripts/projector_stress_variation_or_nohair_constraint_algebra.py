#!/usr/bin/env python3
"""Checkpoint 235: projector stress variation or no-hair constraint algebra."""

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

CHECKPOINT_235_NAME = "projector-stress-variation-or-nohair-constraint-algebra"
RUN_234 = RUNS_ROOT / "20260601-000051-boundary-metric-variation-and-Bianchi-ledger"

STATUS = "projector_variation_safe_branch_conditions_written_X_nohair_rank_test_not_derived_no_promotion"
CLAIM_CEILING = "projector_stress_variation_conditions_no_nohair_or_PPN_promotion"
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


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_register_rows() -> list[dict[str, Any]]:
    paths = [
        (Path(__file__).resolve(), "checkpoint 235 runner"),
        (WORK_DIR / "221-Noether-source-identity-or-compact-PPN-closure-map.md", "source identity and stress accounting"),
        (WORK_DIR / "222-parent-X-sector-degree-count-and-boundary-action.md", "X first-order boundary action"),
        (WORK_DIR / "223-X-constraint-algebra-and-Khat-Gamma-constitutive-owner.md", "X no-hair constraint algebra gap"),
        (WORK_DIR / "233-boundary-symplectic-metric-or-local-EH-operator.md", "boundary metric candidate"),
        (WORK_DIR / "234-boundary-metric-variation-and-Bianchi-ledger.md", "projector stress ledger"),
        (RUN_234 / "status.json", "checkpoint 234 machine status"),
        (RUN_234 / "results" / "projector_stress_ledger.csv", "checkpoint 234 projector stress rows"),
        (RUN_234 / "results" / "coefficient_status_after_234.csv", "checkpoint 234 coefficient status"),
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


def projector_variation_rows() -> list[dict[str, Any]]:
    return [
        {
            "piece": "projector_action",
            "variation_formula": "S_proj=1/2 <J,P_mem J>_B; delta_g S_proj=1/2<J,delta_g B P_mem J>+1/2<J,B delta_g P_mem J>+source variations",
            "safe_condition": "all metric dependence of B and P_mem is varied or shown zero on the safe branch",
            "status": "formal_variation_written",
            "remaining_gap": "parent boundary metric B not derived",
        },
        {
            "piece": "delta_Pmem_split",
            "variation_formula": "delta P_mem = -delta Pi_M - delta Pi_TF - delta Pi_matter",
            "safe_condition": "each removed sector has an owned stress destination",
            "status": "exact_for_candidate_projector",
            "remaining_gap": "projectors not parent-owned",
        },
        {
            "piece": "delta_Pi_M",
            "variation_formula": "delta Pi_M changes harmonic representative/Hodge star and shell area",
            "safe_condition": "maps only to conserved M_eff monopole; no radial memory profile",
            "status": "conditional_safe",
            "remaining_gap": "M_eff conservation/source normalization not derived",
        },
        {
            "piece": "delta_Pi_TF",
            "variation_formula": "delta Pi_TF probes trace-free l>=2 shell response",
            "safe_condition": "scalar boundary little-group symmetry gives block diagonal trace/TF split and Pi_TF J=0",
            "status": "conditional_safe_if_exact_symmetry",
            "remaining_gap": "full parent boundary variable set not derived",
        },
        {
            "piece": "delta_Pi_matter",
            "variation_formula": "delta Pi_matter probes direct matter/clock memory vertices",
            "safe_condition": "block absent at action level by universal metric coupling",
            "status": "conditional_safe_if_forbidden",
            "remaining_gap": "matter/clock action not derived",
        },
        {
            "piece": "delta_relative_Hodge",
            "variation_formula": "variation of relative Hodge norm and boundary primitive A_rel",
            "safe_condition": "P_mem J_rel=d_rel A_rel with pure-gauge boundary primitive, so stress cancels into T_boundary+T_rel",
            "status": "conditional_safe_not_parent_derived",
            "remaining_gap": "A_rel primitive and relative boundary action not derived",
        },
    ]


def nohair_constraint_rows() -> list[dict[str, Any]]:
    return [
        {
            "constraint": "primary_X",
            "expression": "pi_X^nu approx 0",
            "meaning": "X has no independent kinetic momentum",
            "safe_condition": "X appears only as multiplier",
            "status": "candidate",
        },
        {
            "constraint": "secondary_X",
            "expression": "C_X^nu=-nabla_mu P[Y]^{mu nu}+S_L^nu+d_rel(P_mem J_rel)^nu approx 0",
            "meaning": "source identity enforced as a constraint",
            "safe_condition": "P[Y] and P_mem are parent-owned composites",
            "status": "candidate",
        },
        {
            "constraint": "bracket_closure",
            "expression": "{C_X^nu(x),C_X^rho(y)} closes on parent diffeo/boundary constraints",
            "meaning": "no new exterior X hair",
            "safe_condition": "parent symplectic form specified",
            "status": "not_derived",
        },
        {
            "constraint": "boundary_constraint",
            "expression": "B_X^nu=n_mu P^{mu nu}; A_rel boundary primitive pure gauge",
            "meaning": "no boundary leakage mode",
            "safe_condition": "boundary action owns primitive and shell matching",
            "status": "not_derived",
        },
        {
            "constraint": "rank_test",
            "expression": "rank Hessian(dot X,dot X)=0 and constraint pair removes X phase variables",
            "meaning": "no propagating X degree",
            "safe_condition": "Dirac count closes without second-class leftover hair",
            "status": "necessary_not_sufficient",
        },
    ]


def safe_branch_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition": "C1",
            "requirement": "M_eff is conserved monopole and not a radial memory field",
            "protects": "G_eff/G and beta exterior profile",
            "status": "not_derived",
        },
        {
            "condition": "C2",
            "requirement": "Pi_TF sector vanishes by scalar boundary symmetry before solving local exterior",
            "protects": "gamma and Phi-Psi",
            "status": "conditional",
        },
        {
            "condition": "C3",
            "requirement": "Pi_matter block absent by parent universal metric coupling",
            "protects": "clock and WEP channels",
            "status": "not_derived",
        },
        {
            "condition": "C4",
            "requirement": "relative memory current exact with pure-gauge boundary primitive",
            "protects": "q_loc source",
            "status": "topology_gate_plus_parent_gap",
        },
        {
            "condition": "C5",
            "requirement": "X/J_rel/V_def carry no exterior propagating hair",
            "protects": "beta and fifth-force safety",
            "status": "not_derived",
        },
        {
            "condition": "C6",
            "requirement": "all projector metric variations are included in T_projector or vanish by C1-C5",
            "protects": "Bianchi consistency",
            "status": "structured_not_cleared",
        },
    ]


def coefficient_status_rows() -> list[dict[str, Any]]:
    previous = read_csv_rows(RUN_234 / "results" / "coefficient_status_after_234.csv")
    previous_by_residual = {row["residual"]: row for row in previous}
    updates = {
        "gamma_minus_1": (
            "delta_Pi_TF_condition_explicit",
            "gamma safety requires delta Pi_TF stress to vanish by scalar boundary symmetry or be included",
            "derive scalar boundary variable set and TF block closure",
        ),
        "Phi_minus_Psi": (
            "delta_Pi_TF_condition_explicit",
            "slip safety requires no hidden trace-free projector variation",
            "derive Pi_TF=0 at action level",
        ),
        "G_eff_over_G_minus_1": (
            "delta_Pi_M_monopole_condition",
            "source effect must be conserved M_eff only, not a radial memory stress",
            "derive M_eff conservation/source normalization",
        ),
        "alpha_clock": (
            "delta_Pi_matter_forbidden_condition",
            "clock safety requires direct clock projector block absent in the action",
            "derive universal clock coupling",
        ),
        "epsilon_matter": (
            "delta_Pi_matter_forbidden_condition",
            "WEP safety requires direct composition projector block absent in the action",
            "derive universal matter coupling",
        ),
        "beta_minus_1": (
            "X_nohair_and_projector_stress_conditions_explicit",
            "beta route now requires C1-C6 plus local EH exterior operator",
            "derive no-hair constraint algebra and local EH operator",
        ),
    }
    rows: list[dict[str, Any]] = []
    for residual, prior in previous_by_residual.items():
        status, result, next_needed = updates[residual]
        rows.append(
            {
                "residual": residual,
                "checkpoint_234_status": prior["checkpoint_234_status"],
                "checkpoint_235_status": status,
                "coefficient_after_235": result,
                "parent_derived": "no",
                "promotion_allowed": "false",
                "next_needed": next_needed,
            }
        )
    return rows


def claim_gate_rows(source_rows: list[dict[str, Any]], coefficient_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = sum(row["exists"] != "yes" for row in source_rows)
    beta_condition = any(row["residual"] == "beta_minus_1" and row["checkpoint_235_status"] == "X_nohair_and_projector_stress_conditions_explicit" for row in coefficient_rows)
    return [
        {
            "gate": "all cited local sources exist",
            "status": "pass" if missing_sources == 0 else "fail",
            "evidence": f"missing={missing_sources}",
            "claim_allowed": "internal checkpoint only",
        },
        {
            "gate": "delta P_mem variation split written",
            "status": "pass",
            "evidence": "delta P_mem=-delta Pi_M-delta Pi_TF-delta Pi_matter",
            "claim_allowed": "formal condition only",
        },
        {
            "gate": "safe branch conditions listed",
            "status": "pass",
            "evidence": "C1-C6",
            "claim_allowed": "theorem target only",
        },
        {
            "gate": "X no-hair rank/bracket tests written",
            "status": "pass",
            "evidence": "primary/secondary/boundary/bracket/rank rows",
            "claim_allowed": "constraint target only",
        },
        {
            "gate": "beta gate sharpened",
            "status": "pass" if beta_condition else "fail",
            "evidence": "beta requires projector-stress safe branch plus no-hair plus EH",
            "claim_allowed": "conditional only",
        },
        {
            "gate": "T_projector derived or shown to vanish",
            "status": "fail",
            "evidence": "conditions written but parent variation not computed",
            "claim_allowed": "no q_loc promotion",
        },
        {
            "gate": "X/J_rel/V_def no-hair derived",
            "status": "fail",
            "evidence": "constraint algebra still not computed",
            "claim_allowed": "no beta promotion",
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
            "meaning": "The projector-stress problem is now structured: delta P_mem splits into mass, trace-free, matter-coupling, and relative-memory variations, each with a named safe condition. The X no-hair route is also reduced to primary/secondary constraints, bracket closure, boundary primitive, and rank-count tests. This is stronger than a ledger, but not a derivation: T_projector is not computed from a parent action and the no-hair algebra is still open.",
            "main_gain": "hidden projector stress has explicit vanishing/cancellation conditions",
            "main_failure": "the parent variation and X/J_rel/V_def no-hair proof are still missing",
            "next_target": "236-local-EH-operator-or-constraint-algebra-decision.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_235_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    projector_variation = projector_variation_rows()
    nohair_constraints = nohair_constraint_rows()
    safe_branch = safe_branch_rows()
    coefficients = coefficient_status_rows()
    gates = claim_gate_rows(source_rows, coefficients)
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "projector_variation_conditions.csv": (
            projector_variation,
            ["piece", "variation_formula", "safe_condition", "status", "remaining_gap"],
        ),
        "X_nohair_constraint_tests.csv": (
            nohair_constraints,
            ["constraint", "expression", "meaning", "safe_condition", "status"],
        ),
        "safe_branch_conditions.csv": (
            safe_branch,
            ["condition", "requirement", "protects", "status"],
        ),
        "coefficient_status_after_235.csv": (
            coefficients,
            [
                "residual",
                "checkpoint_234_status",
                "checkpoint_235_status",
                "coefficient_after_235",
                "parent_derived",
                "promotion_allowed",
                "next_needed",
            ],
        ),
        "claim_gate_results.csv": (
            gates,
            ["gate", "status", "evidence", "claim_allowed"],
        ),
        "decision.csv": (
            decision,
            [
                "decision",
                "meaning",
                "main_gain",
                "main_failure",
                "next_target",
                "promotion_allowed",
                "claim_ceiling",
            ],
        ),
    }
    for filename, file_data in files.items():
        rows, fieldnames = file_data
        write_csv(results_dir / filename, rows, fieldnames)

    missing_sources = sum(row["exists"] != "yes" for row in source_rows)
    status_payload = {
        "status": decision[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(files.keys()),
        "missing_sources": missing_sources,
        "delta_Pmem_variation_split_written": True,
        "safe_branch_conditions_written": True,
        "X_nohair_constraint_tests_written": True,
        "T_projector_parent_derived_or_vanishing_proved": False,
        "X_Jrel_Vdef_nohair_derived": False,
        "local_EH_exterior_operator_derived": False,
        "beta_second_order_parent_derived": False,
        "official_bounds_applied_as_pass_fail": False,
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
