#!/usr/bin/env python3
"""Checkpoint 234: boundary metric variation and Bianchi ledger."""

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

CHECKPOINT_234_NAME = "boundary-metric-variation-and-Bianchi-ledger"
RUN_233 = RUNS_ROOT / "20260601-000050-boundary-symplectic-metric-or-local-EH-operator"

STATUS = "boundary_metric_stress_Bianchi_ledger_written_hidden_stress_not_cleared_no_promotion"
CLAIM_CEILING = "Bianchi_ledger_for_projector_metric_no_parent_stress_theorem_or_PPN_promotion"
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
        (Path(__file__).resolve(), "checkpoint 234 runner"),
        (WORK_DIR / "207-domain-projector-action-and-Bianchi-identity.md", "projector stress/Bianchi precedent"),
        (WORK_DIR / "221-Noether-source-identity-or-compact-PPN-closure-map.md", "source identity stress terms"),
        (WORK_DIR / "232-parent-Pmem-projector-or-source-identity-variation.md", "P_mem projector candidate"),
        (WORK_DIR / "233-boundary-symplectic-metric-or-local-EH-operator.md", "boundary Hodge/DeWitt candidate"),
        (RUN_233 / "status.json", "checkpoint 233 machine status"),
        (RUN_233 / "results" / "boundary_metric_candidate.csv", "candidate boundary metric blocks"),
        (RUN_233 / "results" / "coefficient_status_after_233.csv", "checkpoint 233 coefficient status"),
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


def stress_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "block": "Pi_M harmonic mass flux",
            "variation_term": "delta Hodge star and shell area in harmonic H^2 norm",
            "stress_role": "monopole shell/mass renormalization stress",
            "safe_condition": "constant conserved M_eff, no radial memory profile",
            "status": "conditional_not_parent_derived",
        },
        {
            "block": "Pi_TF tracefree shear",
            "variation_term": "delta DeWitt metric and trace-free tensor block",
            "stress_role": "anisotropic boundary stress capable of sourcing Phi-Psi",
            "safe_condition": "Pi_TF sector vanishes or is constrained before local exterior solution",
            "status": "danger_block",
        },
        {
            "block": "Pi_matter direct coupling",
            "variation_term": "delta direct matter/clock vertex",
            "stress_role": "composition or clock force channel",
            "safe_condition": "universal metric coupling makes this block absent",
            "status": "forbidden_block",
        },
        {
            "block": "P_mem relative memory",
            "variation_term": "delta relative Hodge norm plus boundary primitive A_rel",
            "stress_role": "relative boundary stress and possible q_loc source",
            "safe_condition": "exact relative current with pure-gauge primitive; stress cancels into boundary ledger",
            "status": "conditional_not_parent_derived",
        },
        {
            "block": "projector metric itself",
            "variation_term": "delta Pi_M, delta Pi_TF, delta Pi_matter, delta P_mem through metric/decomposition dependence",
            "stress_role": "hidden projector force if dropped",
            "safe_condition": "projectors arise from varied action and their stress is retained",
            "status": "main_Bianchi_blocker",
        },
    ]


def bianchi_identity_rows() -> list[dict[str, Any]]:
    return [
        {
            "term": "T_matter",
            "included": "yes",
            "condition": "universal metric coupling and ordinary matter equations on shell",
            "if_omitted": "WEP/clock conservation can be faked",
        },
        {
            "term": "T_EH_or_metric",
            "included": "yes",
            "condition": "local metric operator specified",
            "if_omitted": "cannot claim exterior vacuum Einstein branch",
        },
        {
            "term": "T_Meff",
            "included": "yes",
            "condition": "Pi_M mass class retained as conserved monopole",
            "if_omitted": "ordinary mass flux is accidentally erased",
        },
        {
            "term": "T_TF",
            "included": "must vanish or be included",
            "condition": "Pi_TF=0 for no-slip, otherwise explicit anisotropic stress",
            "if_omitted": "gamma/slip safety is fake",
        },
        {
            "term": "T_rel",
            "included": "yes",
            "condition": "relative memory primitive and exactness varied",
            "if_omitted": "q_loc silence is fake",
        },
        {
            "term": "T_projector",
            "included": "yes",
            "condition": "metric dependence of projectors varied",
            "if_omitted": "hidden external force from P_mem",
        },
        {
            "term": "T_X",
            "included": "yes until no-hair proved",
            "condition": "X multiplier/source identity sector varied",
            "if_omitted": "source identity may violate Bianchi accounting",
        },
        {
            "term": "T_boundary",
            "included": "yes",
            "condition": "shell boundary action and primitive varied",
            "if_omitted": "wall stress hidden",
        },
    ]


def coefficient_status_rows() -> list[dict[str, Any]]:
    previous = read_csv_rows(RUN_233 / "results" / "coefficient_status_after_233.csv")
    previous_by_residual = {row["residual"]: row for row in previous}
    updates = {
        "gamma_minus_1": (
            "stress_ledger_requires_TF_zero",
            "gamma safety now explicitly requires Pi_TF stress to vanish or be retained",
            "derive Pi_TF=0 from parent boundary variation",
        ),
        "Phi_minus_Psi": (
            "stress_ledger_requires_TF_zero",
            "slip safety now explicitly requires no hidden anisotropic projector stress",
            "derive scalar boundary variation with T_TF=0",
        ),
        "G_eff_over_G_minus_1": (
            "M_eff_stress_ledger_required",
            "monopole mass class must be conserved and not a radial memory profile",
            "derive conserved source normalization",
        ),
        "alpha_clock": (
            "matter_clock_stress_forbidden",
            "direct clock block must be absent, not merely ignored",
            "derive universal clock coupling",
        ),
        "epsilon_matter": (
            "matter_clock_stress_forbidden",
            "direct matter/composition block must be absent, not merely ignored",
            "derive universal matter coupling",
        ),
        "beta_minus_1": (
            "Bianchi_EH_nohair_gate_required",
            "beta route now requires total stress conservation plus no-hair before EH gate",
            "derive full stress ledger and local EH exterior operator",
        ),
    }
    rows: list[dict[str, Any]] = []
    for residual, prior in previous_by_residual.items():
        status, result, next_needed = updates[residual]
        rows.append(
            {
                "residual": residual,
                "checkpoint_233_status": prior["checkpoint_233_status"],
                "checkpoint_234_status": status,
                "coefficient_after_234": result,
                "parent_derived": "no",
                "promotion_allowed": "false",
                "next_needed": next_needed,
            }
        )
    return rows


def claim_gate_rows(source_rows: list[dict[str, Any]], coefficient_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = sum(row["exists"] != "yes" for row in source_rows)
    beta_gate = any(row["residual"] == "beta_minus_1" and row["checkpoint_234_status"] == "Bianchi_EH_nohair_gate_required" for row in coefficient_rows)
    return [
        {
            "gate": "all cited local sources exist",
            "status": "pass" if missing_sources == 0 else "fail",
            "evidence": f"missing={missing_sources}",
            "claim_allowed": "internal checkpoint only",
        },
        {
            "gate": "projector metric stress ledger written",
            "status": "pass",
            "evidence": "Pi_M, Pi_TF, Pi_matter, P_mem, and projector metric variation listed",
            "claim_allowed": "ledger only",
        },
        {
            "gate": "Bianchi total-stress terms listed",
            "status": "pass",
            "evidence": "T_matter,T_metric,T_Meff,T_TF,T_rel,T_projector,T_X,T_boundary",
            "claim_allowed": "conservation target only",
        },
        {
            "gate": "beta gate includes Bianchi/no-hair",
            "status": "pass" if beta_gate else "fail",
            "evidence": "beta requires conserved total stress plus EH operator",
            "claim_allowed": "conditional only",
        },
        {
            "gate": "hidden projector stress cleared",
            "status": "fail",
            "evidence": "projector metric not varied from parent action",
            "claim_allowed": "no local GR promotion",
        },
        {
            "gate": "Bianchi identity parent-derived",
            "status": "fail",
            "evidence": "full action/stress variation still missing",
            "claim_allowed": "no PPN promotion",
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
            "meaning": "The candidate boundary metric is no longer allowed to be treated as harmless. Each projector block has an explicit stress/Bianchi obligation: Pi_M must become conserved M_eff, Pi_TF must vanish or be carried as anisotropic stress, Pi_matter must be absent by universal coupling, P_mem must cancel through the relative boundary primitive, and metric dependence of the projectors must be varied. This is a ledger, not a parent stress theorem.",
            "main_gain": "hidden projector stress is now explicitly fenced",
            "main_failure": "full parent variation proving conserved total stress is still missing",
            "next_target": "235-projector-stress-variation-or-nohair-constraint-algebra.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_234_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    stress_ledger = stress_ledger_rows()
    bianchi = bianchi_identity_rows()
    coefficients = coefficient_status_rows()
    gates = claim_gate_rows(source_rows, coefficients)
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "projector_stress_ledger.csv": (
            stress_ledger,
            ["block", "variation_term", "stress_role", "safe_condition", "status"],
        ),
        "Bianchi_total_stress_terms.csv": (
            bianchi,
            ["term", "included", "condition", "if_omitted"],
        ),
        "coefficient_status_after_234.csv": (
            coefficients,
            [
                "residual",
                "checkpoint_233_status",
                "checkpoint_234_status",
                "coefficient_after_234",
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
        "projector_metric_stress_ledger_written": True,
        "Bianchi_total_stress_terms_listed": True,
        "hidden_projector_stress_cleared": False,
        "Bianchi_identity_parent_derived": False,
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
