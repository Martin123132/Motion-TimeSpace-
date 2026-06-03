#!/usr/bin/env python3
"""Checkpoint 247: local EH exterior sufficiency stack, no promotion."""

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

CHECKPOINT_247_NAME = "local-EH-exterior-sufficiency-stack-no-promotion"
RUN_246 = RUNS_ROOT / "20260601-000063-auxiliary-nohair-rank-bracket-or-local-EH-pivot"

STATUS = "local_EH_exterior_sufficiency_stack_complete_as_conditional_theorem_parent_N_gates_open_no_promotion"
CLAIM_CEILING = "EH_sufficiency_stack_only_no_parent_reduction_beta_or_local_GR_promotion"
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
        (Path(__file__).resolve(), "checkpoint 247 runner"),
        (WORK_DIR / "237-local-EH-exterior-action-contract.md", "EH exterior action contract"),
        (WORK_DIR / "238-metric-only-exterior-reduction-or-nohair-theorem.md", "metric-only exterior audit"),
        (WORK_DIR / "246-auxiliary-nohair-rank-bracket-or-local-EH-pivot.md", "EH stack pivot"),
        (RUN_246 / "status.json", "checkpoint 246 machine status"),
        (RUN_246 / "results" / "EH_exterior_sufficiency_stack.csv", "checkpoint 246 EH stack"),
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


def sufficiency_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "name": "compact_exterior_definition",
            "premise": "E={r>R_shell}, T_matter|E=0 except enclosed charge encoded by boundary data",
            "consequence": "ordinary local matter source is absent in the exterior field equations",
            "status": "definition",
        },
        {
            "step": 2,
            "name": "nonmetric_sector_removal",
            "premise": "N1-N6 all hold and all residual stress is zero, pure boundary, or conserved M_eff",
            "consequence": "S_parent|E reduces to a metric-only exterior action plus boundary/M_eff labels",
            "status": "conditional_open",
        },
        {
            "step": 3,
            "name": "metric_action_contract",
            "premise": "S_ext[g] is local, four-dimensional, diffeomorphism-invariant, metric-only, and second-order",
            "consequence": "Lovelock/EH gate applies",
            "status": "target_not_parent_derived",
        },
        {
            "step": 4,
            "name": "EH_equation",
            "premise": "Lovelock/EH gate plus compact local exterior",
            "consequence": "G_mu_nu + Lambda_eff g_mu_nu = 0",
            "status": "conditional_theorem",
        },
        {
            "step": 5,
            "name": "local_PPN_limit",
            "premise": "Lambda_eff negligible at Solar-System PPN order",
            "consequence": "G_mu_nu=0 to local PPN order",
            "status": "conditional_theorem",
        },
        {
            "step": 6,
            "name": "Schwarzschild_beta",
            "premise": "static spherical vacuum exterior with conserved M_eff",
            "consequence": "g_00=-1+2U-2U^2+O(U^3), beta=1",
            "status": "conditional_theorem",
        },
        {
            "step": 7,
            "name": "promotion_limit",
            "premise": "N-gates and metric-only reduction must be parent-derived",
            "consequence": "no local-GR/PPN promotion until parent proof exists",
            "status": "claim_ceiling",
        },
    ]


def premise_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "premise": "ordinary_matter_absent",
            "required_form": "T_matter|E=0 outside compact source",
            "current_status": "definition_of_exterior",
            "blocking_issue": "",
            "promotion_effect_if_derived": "vacuum field equation domain",
        },
        {
            "premise": "N1_Meff",
            "required_form": "Pi_M flux closed; M_eff conserved and calibrated",
            "current_status": "conditional_gate_from_244",
            "blocking_issue": "Pi_M/source identity/calibration not parent-derived",
            "promotion_effect_if_derived": "source normalization and monopole mass owned",
        },
        {
            "premise": "N2_no_TF",
            "required_form": "tau_TF_AB=0; no tangential shear",
            "current_status": "conditional_gate_from_243",
            "blocking_issue": "parent scalar-only boundary variable set missing",
            "promotion_effect_if_derived": "gamma/slip gate closes",
        },
        {
            "premise": "N3_universal_strict_coframe",
            "required_form": "Pi_matter=0 and beta_C^loc=0",
            "current_status": "conditional_gate_from_240_242",
            "blocking_issue": "R_loc parent selection missing",
            "promotion_effect_if_derived": "direct WEP/clock/C trace source closes",
        },
        {
            "premise": "N4_exact_relative_memory",
            "required_form": "P_mem J_rel=dA_rel with pure-gauge boundary primitive",
            "current_status": "conditional_gate_from_245",
            "blocking_issue": "P_mem/source identity/A_rel not parent-derived",
            "promotion_effect_if_derived": "q_loc relative-memory source closes conditionally",
        },
        {
            "premise": "N5_projector_stress",
            "required_form": "T_projector=0 or retained in conserved total stress",
            "current_status": "open",
            "blocking_issue": "delta P_mem/delta g and boundary metric variation not computed",
            "promotion_effect_if_derived": "Bianchi-safe projector route",
        },
        {
            "premise": "N6_auxiliary_nohair",
            "required_form": "X/J_rel/V_def carry no exterior propagating degrees",
            "current_status": "open",
            "blocking_issue": "constraint algebra/P[Y]/V_def parent ownership missing",
            "promotion_effect_if_derived": "no exterior fifth-force/beta hair",
        },
        {
            "premise": "metric_only_second_order_operator",
            "required_form": "S_ext[g]=(16piG)^-1 int sqrt(-g)(R-2Lambda)+boundary",
            "current_status": "target_not_derived",
            "blocking_issue": "parent exterior reduction not derived",
            "promotion_effect_if_derived": "EH exterior and Schwarzschild route",
        },
    ]


def hidden_sector_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "sector": "M_eff_mass_flux",
            "allowed_exterior_status": "conserved boundary/monopole label",
            "hidden_danger": "radial G_eff hair",
            "current_disposition": "conditional N1",
        },
        {
            "sector": "trace_free_shear",
            "allowed_exterior_status": "zero",
            "hidden_danger": "gamma/slip anisotropic stress",
            "current_disposition": "conditional N2",
        },
        {
            "sector": "direct_matter_clock_vertex",
            "allowed_exterior_status": "absent",
            "hidden_danger": "WEP/clock composition force",
            "current_disposition": "conditional N3",
        },
        {
            "sector": "relative_memory_Jrel",
            "allowed_exterior_status": "exact/pure gauge boundary",
            "hidden_danger": "q_loc source",
            "current_disposition": "conditional N4",
        },
        {
            "sector": "projector_stress",
            "allowed_exterior_status": "zero or retained in total stress",
            "hidden_danger": "fake Bianchi conservation",
            "current_disposition": "open N5",
        },
        {
            "sector": "X_Jrel_Vdef_auxiliary",
            "allowed_exterior_status": "no propagating exterior degrees",
            "hidden_danger": "fifth force / beta hair",
            "current_disposition": "open N6",
        },
        {
            "sector": "boundary_primitive_Arel",
            "allowed_exterior_status": "pure gauge or boundary-cancelled",
            "hidden_danger": "boundary memory hair",
            "current_disposition": "open within N4/N6",
        },
    ]


def claim_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim": "If all N1-N6 and metric-only exterior premises hold, beta=1 follows.",
            "status": "conditional_theorem_allowed",
            "reason": "EH/Lovelock plus Schwarzschild exterior gives beta=1",
        },
        {
            "claim": "MTS derives beta=1 now.",
            "status": "not_allowed",
            "reason": "N5/N6 and metric-only exterior are not parent-derived",
        },
        {
            "claim": "MTS passes local PPN now.",
            "status": "not_allowed",
            "reason": "local coefficient gates remain conditional/open",
        },
        {
            "claim": "MTS local branch is dead.",
            "status": "not_supported",
            "reason": "conditional theorem stack is coherent and has not hit a contradiction",
        },
        {
            "claim": "MTS local branch is derived.",
            "status": "not_allowed",
            "reason": "the stack is sufficient, not parent-owned",
        },
    ]


def next_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "rank": 1,
            "target": "N5_projector_stress_zero_or_retained",
            "why": "Bianchi safety is the nearest hard blocker in the EH stack",
            "next_action": "compute/structure delta P_mem stress or prove topological zero-stress route",
        },
        {
            "rank": 2,
            "target": "metric_only_exterior_reduction",
            "why": "EH operator cannot be claimed until nonmetric sectors are removed",
            "next_action": "turn premise table into parent-reduction proof obligations",
        },
        {
            "rank": 3,
            "target": "N6_auxiliary_nohair",
            "why": "remaining possible exterior fifth-force/beta hair",
            "next_action": "defer brackets until parent symplectic structure exists",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    missing_sources = sum(row["exists"] != "yes" for row in source_register_rows())
    open_premises = sum(1 for row in premise_status_rows() if "open" in row["current_status"] or "not_derived" in row["current_status"] or "target" in row["current_status"])
    return [
        {
            "gate": "all cited local sources exist",
            "status": "pass" if missing_sources == 0 else "fail",
            "evidence": f"missing={missing_sources}",
            "claim_allowed": "internal checkpoint only",
        },
        {
            "gate": "EH sufficiency theorem internally written",
            "status": "pass",
            "evidence": "N1-N6 plus metric-only Lovelock/EH chain",
            "claim_allowed": "conditional theorem",
        },
        {
            "gate": "hidden nonmetric exterior sectors audited",
            "status": "pass",
            "evidence": "all known sectors have allowed status or open blocker",
            "claim_allowed": "audit only",
        },
        {
            "gate": "all premises parent-derived",
            "status": "fail",
            "evidence": f"open_or_target_premises={open_premises}",
            "claim_allowed": "no",
        },
        {
            "gate": "beta/local GR promoted",
            "status": "fail",
            "evidence": CLAIM_CEILING,
            "claim_allowed": "no",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "meaning": "The local EH exterior route is now an internally complete conditional sufficiency theorem: if ordinary exterior matter is absent, N1-N6 remove or account for every non-metric sector, and the remaining exterior action is local/diffeomorphic/metric-only/two-derivative, then EH/Lovelock gives vacuum Einstein and static spherical beta=1. This is not a parent derivation because several premises remain conditional or open.",
            "main_gain": "local GR is now a finite premise stack rather than a vague hope or a hidden assumption",
            "main_failure": "N5, N6, parent metric-only reduction, and several parent owners remain unproved",
            "next_target": "248-projector-stress-zero-or-retained-theorem.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_247_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    theorem_rows = sufficiency_theorem_rows()
    premise_rows = premise_status_rows()
    hidden_rows = hidden_sector_audit_rows()
    claim_rows = claim_status_rows()
    next_rows = next_gate_rows()
    gates = claim_gate_rows()
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "EH_sufficiency_theorem_chain.csv": (
            theorem_rows,
            ["step", "name", "premise", "consequence", "status"],
        ),
        "EH_premise_status_table.csv": (
            premise_rows,
            ["premise", "required_form", "current_status", "blocking_issue", "promotion_effect_if_derived"],
        ),
        "hidden_nonmetric_sector_audit.csv": (
            hidden_rows,
            ["sector", "allowed_exterior_status", "hidden_danger", "current_disposition"],
        ),
        "claim_status_table.csv": (
            claim_rows,
            ["claim", "status", "reason"],
        ),
        "next_gate_priority_after_247.csv": (
            next_rows,
            ["rank", "target", "why", "next_action"],
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
        "EH_sufficiency_theorem_written": True,
        "all_premises_parent_derived": False,
        "beta_promoted": False,
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
