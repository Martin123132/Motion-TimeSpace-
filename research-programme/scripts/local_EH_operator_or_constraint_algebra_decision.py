#!/usr/bin/env python3
"""Checkpoint 236: local EH operator or constraint-algebra decision."""

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

CHECKPOINT_236_NAME = "local-EH-operator-or-constraint-algebra-decision"
RUN_235 = RUNS_ROOT / "20260601-000052-projector-stress-variation-or-nohair-constraint-algebra"

STATUS = "local_EH_operator_route_selected_constraint_algebra_deferred_no_local_GR_or_PPN_promotion"
CLAIM_CEILING = "route_decision_only_no_EH_or_constraint_algebra_promotion"
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
        (Path(__file__).resolve(), "checkpoint 236 runner"),
        (WORK_DIR / "223-X-constraint-algebra-and-Khat-Gamma-constitutive-owner.md", "constraint algebra blocker"),
        (WORK_DIR / "233-boundary-symplectic-metric-or-local-EH-operator.md", "local EH gate precedent"),
        (WORK_DIR / "234-boundary-metric-variation-and-Bianchi-ledger.md", "Bianchi ledger"),
        (WORK_DIR / "235-projector-stress-variation-or-nohair-constraint-algebra.md", "route choice trigger"),
        (RUN_235 / "status.json", "checkpoint 235 machine status"),
        (RUN_235 / "results" / "safe_branch_conditions.csv", "checkpoint 235 safe branch"),
        (RUN_235 / "results" / "X_nohair_constraint_tests.csv", "checkpoint 235 no-hair tests"),
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


def route_matrix_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "X_Pmem_constraint_algebra",
            "next_requirement": "compute brackets {C_X,C_X} using parent symplectic form",
            "available_inputs": "primary/secondary constraints and rank test only",
            "missing_input": "parent Y symplectic structure and boundary metric ownership",
            "value_if_solved": "direct no-hair proof for X/J_rel/V_def",
            "decision": "defer",
        },
        {
            "route": "local_EH_exterior_operator",
            "next_requirement": "write exact parent contract for metric-only two-derivative exterior branch",
            "available_inputs": "safe branch C1-C6, Bianchi ledger, no-hair conditions, Lovelock gate",
            "missing_input": "proof that parent action reduces to metric-only exterior action",
            "value_if_solved": "Schwarzschild exterior and beta=1 route",
            "decision": "select_next",
        },
        {
            "route": "empirical_local_bound_runner",
            "next_requirement": "apply official Cassini/clock/WEP bounds",
            "available_inputs": "official manifest and coefficient gates",
            "missing_input": "parent-derived coefficients",
            "value_if_solved": "numerical pressure test",
            "decision": "not_yet",
        },
    ]


def local_eh_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause": "EH0",
            "requirement": "exterior region E has ordinary matter removed and compact source represented only by M_eff",
            "test": "T_matter|E=0; Pi_M charge constant",
            "status": "contract",
        },
        {
            "clause": "EH1",
            "requirement": "memory/projector sectors vanish or are boundary-exact under C1-C6",
            "test": "T_TF=0, T_matter_direct=0, d_rel(P_mem J_rel)=0, T_projector cancels or vanishes",
            "status": "contract_not_derived",
        },
        {
            "clause": "EH2",
            "requirement": "X/J_rel/V_def carry no exterior propagating hair",
            "test": "no exterior scalar/vector/tensor profile beyond metric",
            "status": "contract_not_derived",
        },
        {
            "clause": "EH3",
            "requirement": "remaining exterior action is local, diffeomorphism invariant, metric-only, and second order",
            "test": "S_ext[g]=(16 pi G_eff)^-1 int sqrt(-g)(R-2 Lambda_eff)+boundary",
            "status": "target_contract",
        },
        {
            "clause": "EH4",
            "requirement": "Lambda-like term negligible/constant for compact local PPN branch",
            "test": "G_mu_nu=0 to PPN order around source",
            "status": "target_contract",
        },
        {
            "clause": "EH5",
            "requirement": "static spherical exterior solution is Schwarzschild",
            "test": "g_00=-1+2U-2U^2+O(U^3)",
            "status": "conditional_consequence",
        },
    ]


def deferred_constraint_rows() -> list[dict[str, Any]]:
    tests = read_csv_rows(RUN_235 / "results" / "X_nohair_constraint_tests.csv")
    rows: list[dict[str, Any]] = []
    for row in tests:
        rows.append(
            {
                "constraint": row["constraint"],
                "current_status": row["status"],
                "why_deferred": "requires parent symplectic form before bracket computation",
                "resume_condition": "parent boundary metric/symplectic owner exists",
            }
        )
    return rows


def claim_gate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = sum(row["exists"] != "yes" for row in source_rows)
    return [
        {
            "gate": "all cited local sources exist",
            "status": "pass" if missing_sources == 0 else "fail",
            "evidence": f"missing={missing_sources}",
            "claim_allowed": "internal checkpoint only",
        },
        {
            "gate": "route comparison written",
            "status": "pass",
            "evidence": "constraint algebra, local EH, and empirical runner compared",
            "claim_allowed": "planning only",
        },
        {
            "gate": "local EH selected as next target",
            "status": "pass",
            "evidence": "constraint algebra lacks parent symplectic form; EH contract can be attacked now",
            "claim_allowed": "next-work decision",
        },
        {
            "gate": "constraint algebra solved",
            "status": "fail",
            "evidence": "explicitly deferred until parent symplectic structure exists",
            "claim_allowed": "no no-hair claim",
        },
        {
            "gate": "local EH operator derived",
            "status": "fail",
            "evidence": "selected for next derivation, not solved here",
            "claim_allowed": "no beta claim",
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
            "meaning": "The next attack should be the local Einstein-Hilbert exterior operator, not the X/P_mem constraint algebra. The algebra route is real but blocked by the missing parent symplectic structure. The EH route can be sharpened immediately into a concrete parent-action contract: exterior matter absent, memory/projector sectors boundary-exact or vanished, no exterior hair, and only a metric two-derivative diffeomorphism-invariant operator remains.",
            "main_gain": "the local route now has a disciplined next target instead of looping over missing symplectic data",
            "main_failure": "neither EH operator nor constraint algebra is derived in this checkpoint",
            "next_target": "237-local-EH-exterior-action-contract.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_236_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    route_matrix = route_matrix_rows()
    eh_contract = local_eh_contract_rows()
    deferred_constraints = deferred_constraint_rows()
    gates = claim_gate_rows(source_rows)
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "route_decision_matrix.csv": (
            route_matrix,
            ["route", "next_requirement", "available_inputs", "missing_input", "value_if_solved", "decision"],
        ),
        "local_EH_exterior_contract.csv": (
            eh_contract,
            ["clause", "requirement", "test", "status"],
        ),
        "deferred_constraint_algebra_tests.csv": (
            deferred_constraints,
            ["constraint", "current_status", "why_deferred", "resume_condition"],
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
        "local_EH_operator_selected_next": True,
        "constraint_algebra_deferred_until_symplectic_owner": True,
        "local_EH_exterior_operator_derived": False,
        "X_Pmem_constraint_algebra_derived": False,
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
