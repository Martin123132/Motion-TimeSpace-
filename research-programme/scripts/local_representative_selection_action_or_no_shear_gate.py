#!/usr/bin/env python3
"""Checkpoint 243: local representative selection action or no-shear gate."""

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

CHECKPOINT_243_NAME = "local-representative-selection-action-or-no-shear-gate"
RUN_239 = RUNS_ROOT / "20260601-000056-nohair-theorem-targets-or-local-bound-runner"
RUN_242 = RUNS_ROOT / "20260601-000059-strict-local-coframe-branch-or-domain-projector-action"

STATUS = "Rloc_parent_selection_not_derived_N2_no_shear_sufficient_gate_locked_no_local_GR_promotion"
CLAIM_CEILING = "N2_no_shear_conditional_gate_no_Rloc_parent_selection_or_PPN_promotion"
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
        (Path(__file__).resolve(), "checkpoint 243 runner"),
        (WORK_DIR / "228-isotropic-response-condition-or-official-local-bound-runner.md", "isotropic/no-slip sufficient condition"),
        (WORK_DIR / "229-second-order-beta-or-boundary-scalar-owner.md", "scalar boundary owner and beta reduction"),
        (WORK_DIR / "233-boundary-symplectic-metric-or-local-EH-operator.md", "boundary projector metric candidate"),
        (WORK_DIR / "239-nohair-theorem-targets-or-local-bound-runner.md", "local-bound pressure ranking"),
        (WORK_DIR / "242-strict-local-coframe-branch-or-domain-projector-action.md", "strict local coframe branch decision"),
        (RUN_239 / "results" / "nohair_priority_after_bound_preflight.csv", "N-target priority after local bounds"),
        (RUN_242 / "status.json", "checkpoint 242 machine status"),
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


def Rloc_selection_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "piece": "candidate_selector_term",
            "equation": "S_Rloc = int sqrt(-g) lambda_R chi_bound beta_C^loc",
            "what_it_would_do": "enforce beta_C^loc=0 inside stationary bound domains",
            "verdict": "formal_constraint_candidate_only",
            "failure": "chi_bound and beta_C^loc are not parent-selected variables",
        },
        {
            "piece": "coherence_readout",
            "equation": "C_coh[D_bound] -> 0 selects trivial local class",
            "what_it_would_do": "align stationary bound domains with strict local coframe",
            "verdict": "conditional_selection_ledger",
            "failure": "C_coh law does not yet vary from parent action",
        },
        {
            "piece": "constant_unit_rescaling",
            "equation": "ehat^a_mu = Omega_D e^a_mu, partial_mu Omega_D=0",
            "what_it_would_do": "make local readout common-mode with no local C force",
            "verdict": "sufficient_if_selected",
            "failure": "Omega_D representative is not parent-derived",
        },
        {
            "piece": "decision",
            "equation": "R_loc[D_bound] not derived",
            "what_it_would_do": "would close C local trace source if derived",
            "verdict": "open_parent_theorem",
            "failure": "do not pretend R_loc is proven",
        },
    ]


def no_shear_theorem_chain_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "name": "scalar_boundary_data",
            "condition": "Y_boundary contains scalar shell invariants only",
            "equation": "S_boundary = int_boundary sqrt(|gamma|) F(Y_boundary)",
            "result": "no tangent vector/tensor memory channel is present",
        },
        {
            "step": 2,
            "name": "little_group_trace_only",
            "condition": "stationary compact isotropic collar",
            "equation": "tau_AB = tau gamma_AB",
            "result": "tau_TF_AB=0",
        },
        {
            "step": 3,
            "name": "trace_free_constraint",
            "condition": "local trace-free weak-field constraint is Einstein-like",
            "equation": "D_AB(Phi-Psi)=8 pi G tau_TF_AB",
            "result": "D_AB(Phi-Psi)=0",
        },
        {
            "step": 4,
            "name": "compact_matching",
            "condition": "regular collar, no incoming l>=2 homogeneous slip mode",
            "equation": "Phi-Psi = l=0,l=1 gauge/frame modes only",
            "result": "Phi-Psi=0 after gauge and matching",
        },
        {
            "step": 5,
            "name": "coefficient_readout",
            "condition": "N2 assumptions hold",
            "equation": "c_gamma=c_slip=0",
            "result": "gamma/slip channel is conditionally removed",
        },
        {
            "step": 6,
            "name": "promotion_limit",
            "condition": "parent must derive scalar-only boundary variables",
            "equation": "no K_TF_AB, no tangential J_rel_A, no hidden angular label",
            "result": "N2 is a locked sufficient gate, not full local GR",
        },
    ]


def gate_priority_rows() -> list[dict[str, Any]]:
    return [
        {
            "rank_after_243": 1,
            "target": "Rloc_parent_selection",
            "status": "open",
            "why": "strict local coframe/C-silence still needs parent representative selection",
            "next_action": "derive selector from local stationary-domain action or keep as explicit theorem gap",
        },
        {
            "rank_after_243": 2,
            "target": "N2_no_TF",
            "status": "conditional_gate_locked",
            "why": "scalar boundary symmetry removes gamma/slip if parent forbids tangential shear channels",
            "next_action": "derive scalar-only boundary variable set from parent action",
        },
        {
            "rank_after_243": 3,
            "target": "N1_Meff",
            "status": "next_clean_local_gate",
            "why": "source normalization/common-mode mass must become conserved monopole only",
            "next_action": "derive Pi_M/M_eff conservation and no radial memory hair",
        },
        {
            "rank_after_243": 4,
            "target": "N4_N5_N6",
            "status": "open",
            "why": "relative exactness, projector stress, and auxiliary no-hair still block EH exterior",
            "next_action": "derive q_loc=0/no-hair chain",
        },
        {
            "rank_after_243": 5,
            "target": "local_EH_exterior",
            "status": "open",
            "why": "beta=1 still needs metric-only vacuum exterior",
            "next_action": "derive exterior operator after N1/N4/N5/N6",
        },
    ]


def coefficient_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual": "gamma_minus_1",
            "status_after_243": "conditionally_zero_if_N2_holds",
            "coefficient_status": "c_gamma=0 under scalar-boundary/no-shear theorem",
            "remaining_gap": "parent scalar-only boundary variable set",
        },
        {
            "residual": "Phi_minus_Psi",
            "status_after_243": "conditionally_zero_if_N2_holds",
            "coefficient_status": "c_slip=0 under tau_TF_AB=0 and compact matching",
            "remaining_gap": "forbid tangential shear/J_rel_A from parent action",
        },
        {
            "residual": "epsilon_matter",
            "status_after_243": "conditionally_zero_from_N3",
            "coefficient_status": "c_matter_direct=0 under strict matter coframe",
            "remaining_gap": "parent selection of strict coframe/R_loc",
        },
        {
            "residual": "alpha_clock",
            "status_after_243": "conditionally_zero_for_direct_vertex",
            "coefficient_status": "c_clock_direct=0 under strict matter coframe",
            "remaining_gap": "metric clock redshift/C representative still open",
        },
        {
            "residual": "G_eff_over_G_minus_1",
            "status_after_243": "open",
            "coefficient_status": "monopole/common-mode source normalization not derived",
            "remaining_gap": "N1_Meff",
        },
        {
            "residual": "beta_minus_1",
            "status_after_243": "open",
            "coefficient_status": "requires metric-only vacuum exterior",
            "remaining_gap": "N1/N4/N5/N6 plus EH gate",
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
            "gate": "R_loc parent selection derived",
            "status": "fail",
            "evidence": "selector action would require unowned chi_bound/beta_C variables",
            "claim_allowed": "no",
        },
        {
            "gate": "N2 no-shear sufficient theorem locked",
            "status": "conditional_pass",
            "evidence": "scalar boundary symmetry -> tau_TF_AB=0 -> Phi-Psi=0",
            "claim_allowed": "conditional local gate only",
        },
        {
            "gate": "gamma/slip public pass claimed",
            "status": "fail",
            "evidence": "parent scalar-boundary owner still missing",
            "claim_allowed": "no",
        },
        {
            "gate": "beta/local EH exterior derived",
            "status": "fail",
            "evidence": "N1/N4/N5/N6 and EH gate still open",
            "claim_allowed": "no",
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
            "meaning": "The parent selection of R_loc[D_bound] cannot be honestly derived yet without introducing unowned selector variables. Rather than smuggling it in, checkpoint 243 locks the independent N2 no-shear gate: scalar-only compact boundary stress implies tau_TF_AB=0 and therefore Phi-Psi=0 after compact matching. This conditionally removes gamma/slip but does not promote local GR.",
            "main_gain": "gamma/slip safety is isolated as a precise scalar-boundary theorem target while R_loc remains explicitly open",
            "main_failure": "the parent action still has not derived the scalar-only boundary variable set or the strict local representative",
            "next_target": "244-Meff-monopole-source-normalization-or-radial-memory-hair.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_243_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    selection_rows = Rloc_selection_attempt_rows()
    no_shear_rows = no_shear_theorem_chain_rows()
    priority_rows = gate_priority_rows()
    coefficient_rows = coefficient_status_rows()
    gates = claim_gate_rows()
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "Rloc_selection_action_attempt.csv": (
            selection_rows,
            ["piece", "equation", "what_it_would_do", "verdict", "failure"],
        ),
        "N2_no_shear_theorem_chain.csv": (
            no_shear_rows,
            ["step", "name", "condition", "equation", "result"],
        ),
        "local_gate_priority_after_243.csv": (
            priority_rows,
            ["rank_after_243", "target", "status", "why", "next_action"],
        ),
        "coefficient_status_after_243.csv": (
            coefficient_rows,
            ["residual", "status_after_243", "coefficient_status", "remaining_gap"],
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
        "Rloc_parent_selection_derived": False,
        "N2_no_shear_gate_conditionally_locked": True,
        "gamma_slip_public_pass_claimed": False,
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
