#!/usr/bin/env python3
"""Lock the action/stress contract needed to derive T^2 S = 1 without GR smuggling."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SOURCE_03_STATUS = Path("runs/20260530-223810-reciprocal-routing-parent-origin/status.json")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def action_terms() -> list[dict[str, Any]]:
    return [
        {
            "term": "load_clock_potential",
            "symbol": "A=T^2",
            "required_form": "A(r)=1-L(r) in the local exterior weak-field limit",
            "role": "sets Newtonian clock residue and g_tt order",
            "failure_if_missing": "no Newtonian/GPS clock recovery",
        },
        {
            "term": "routing_metric_factor",
            "symbol": "B=S",
            "required_form": "B is varied independently before the vacuum constraint is applied",
            "role": "prevents p=1 from being inserted by definition",
            "failure_if_missing": "reciprocity is assumed rather than derived",
        },
        {
            "term": "reciprocal_strain",
            "symbol": "R_AB=ln(A B)",
            "required_form": "positive vacuum penalty or constraint depending on derivatives of R_AB",
            "role": "Euler-Lagrange equation can force AB=constant in source-free exterior",
            "failure_if_missing": "no parent equation selects T^2S=1",
        },
        {
            "term": "asymptotic_flatness",
            "symbol": "A->1, B->1",
            "required_form": "boundary condition at infinity sets the constant AB=1",
            "role": "turns reciprocal constant into exact unity",
            "failure_if_missing": "AB may be arbitrary constant",
        },
        {
            "term": "vacuum_source_silence",
            "symbol": "J_R=0",
            "required_form": "local vacuum cannot source the reciprocal strain mode",
            "role": "prevents hidden fitted local force in the p=1 derivation",
            "failure_if_missing": "reciprocity can be spoiled or tuned by local source terms",
        },
    ]


def theorem_steps() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "statement": "Use static spherical areal ansatz with A=T^2 and B=S.",
            "must_show": "A and B are load/routing variables of the parent theory, not imported metric names only.",
            "status": "contract_required",
        },
        {
            "step": 2,
            "statement": "Define reciprocal strain R_AB=ln(A B).",
            "must_show": "R_AB is the independent mode whose vacuum value decides p.",
            "status": "contract_required",
        },
        {
            "step": 3,
            "statement": "Parent variation gives d/dr[W(r,L,fields) dR_AB/dr]=J_R.",
            "must_show": "W>0 and J_R=0 in local vacuum exterior.",
            "status": "contract_required",
        },
        {
            "step": 4,
            "statement": "Finite exterior flux plus asymptotic flatness gives dR_AB/dr=0 and R_AB(infinity)=0.",
            "must_show": "there is no allowed singular reciprocal-flux integration constant outside the source.",
            "status": "contract_required",
        },
        {
            "step": 5,
            "statement": "Therefore R_AB=0, AB=1, T^2S=1, p=1.",
            "must_show": "result follows before fitting light bending, Shapiro, or perihelion.",
            "status": "would_derive_reciprocity_if_steps_1_to_4_pass",
        },
    ]


def forbidden_imports() -> list[dict[str, Any]]:
    return [
        {
            "forbidden_move": "assume Schwarzschild metric",
            "reason": "AB=1 is already built in",
            "allowed_replacement": "derive A and B equations from parent load/routing action",
        },
        {
            "forbidden_move": "assume Einstein vacuum equations",
            "reason": "G^t_t=G^r_r directly gives AB=constant",
            "allowed_replacement": "derive the same stress-balance as an MTS Euler-Lagrange consequence",
        },
        {
            "forbidden_move": "fit p from light bending",
            "reason": "turns GR recovery into parameter tuning",
            "allowed_replacement": "derive p=1 before weak-field tests",
        },
        {
            "forbidden_move": "hide a local source J_R",
            "reason": "would reintroduce a fitted local fifth-force channel",
            "allowed_replacement": "prove J_R=0 or explicitly bounded in local vacuum",
        },
    ]


def gate_rows(source: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate": "source_03_complete",
            "status": "pass" if source.get("readout") == "reciprocal_routing_parent_origin_partial_not_derived" else "fail",
            "detail": str(source.get("readout")),
        },
        {
            "gate": "reciprocal_mode_identified",
            "status": "pass",
            "detail": "R_AB=ln(A B) is the mode that must be killed in local vacuum",
        },
        {
            "gate": "no_smuggling_rules_locked",
            "status": "pass",
            "detail": "Schwarzschild, Einstein-vacuum, and p-fit shortcuts are forbidden",
        },
        {
            "gate": "action_theorem_proved",
            "status": "fail",
            "detail": "contract is written but no parent variation has been derived yet",
        },
        {
            "gate": "promotion_to_main_workbench",
            "status": "fail",
            "detail": "requires completed action theorem and beta/PPN check",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "contract_status",
            "status": "locked_not_satisfied",
            "evidence": "the exact theorem obligations and forbidden imports are now explicit",
            "next_action": "attempt the R_AB action theorem",
        },
        {
            "decision": "best_theorem_target",
            "status": "reciprocal_strain_vacuum_silence",
            "evidence": "derive d(W R_AB')/dr=0 with finite flux and asymptotic flatness",
            "next_action": "write 05-reciprocity-theorem-attempt.md",
        },
        {
            "decision": "promotion_status",
            "status": "not_allowed",
            "evidence": "no parent action has yet produced AB=1",
            "next_action": "keep all work in post-checkpoint folder",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Lock vacuum reciprocity action contract.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    source = load_json(root / SOURCE_03_STATUS)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or root / "runs" / f"{timestamp}-vacuum-reciprocity-action-contract"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    terms = action_terms()
    steps = theorem_steps()
    forbidden = forbidden_imports()
    gates = gate_rows(source)
    decisions = decision_rows()

    write_csv(results_dir / "vacuum_reciprocity_action_terms.csv", terms, list(terms[0].keys()))
    write_csv(results_dir / "vacuum_reciprocity_theorem_steps.csv", steps, list(steps[0].keys()))
    write_csv(results_dir / "vacuum_reciprocity_forbidden_imports.csv", forbidden, list(forbidden[0].keys()))
    write_csv(results_dir / "vacuum_reciprocity_contract_gates.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "vacuum_reciprocity_contract_decision.csv", decisions, list(decisions[0].keys()))

    readout = "vacuum_reciprocity_action_contract_locked_not_satisfied"
    status = {
        "status": "complete_vacuum_reciprocity_action_contract",
        "readout": readout,
        "recommendation": "attempt_reciprocal_strain_vacuum_theorem_next",
        "next_target": "05-reciprocity-theorem-attempt.md",
        "contract_locked": True,
        "contract_satisfied": False,
        "reciprocal_mode": "R_AB=ln(A B)=ln(T^2 S)",
        "forbidden_import_count": len(forbidden),
        "promotion_to_main_workbench_allowed": False,
        "outputs": {
            "vacuum_reciprocity_action_terms": str(results_dir / "vacuum_reciprocity_action_terms.csv"),
            "vacuum_reciprocity_theorem_steps": str(results_dir / "vacuum_reciprocity_theorem_steps.csv"),
            "vacuum_reciprocity_forbidden_imports": str(results_dir / "vacuum_reciprocity_forbidden_imports.csv"),
            "vacuum_reciprocity_contract_gates": str(results_dir / "vacuum_reciprocity_contract_gates.csv"),
            "vacuum_reciprocity_contract_decision": str(results_dir / "vacuum_reciprocity_contract_decision.csv"),
            "status_json": str(out_dir / "status.json"),
        },
    }
    (out_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (out_dir / "log.txt").write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    (out_dir / "DONE.txt").write_text(readout + "\n", encoding="utf-8")
    print(json.dumps(status, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
