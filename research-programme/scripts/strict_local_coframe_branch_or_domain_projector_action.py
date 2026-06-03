#!/usr/bin/env python3
"""Checkpoint 242: strict local coframe branch or domain projector action."""

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

CHECKPOINT_242_NAME = "strict-local-coframe-branch-or-domain-projector-action"
RUN_241 = RUNS_ROOT / "20260601-000058-C-silence-screening-or-parent-selection-theorem"

STATUS = "strict_local_coframe_branch_selected_as_local_C_silence_contract_domain_projector_retained_for_cosmology_no_promotion"
CLAIM_CEILING = "strict_coframe_conditional_theorem_no_parent_selection_or_local_GR_promotion"
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
        (Path(__file__).resolve(), "checkpoint 242 runner"),
        (WORK_DIR / "207-domain-projector-action-and-Bianchi-identity.md", "formal domain projector and Bianchi ledger"),
        (WORK_DIR / "208-domain-representative-selection-law.md", "representative selection ledger"),
        (WORK_DIR / "209-Lcg-domain-scale-parent-derivation-or-demotion.md", "domain scale closure status"),
        (WORK_DIR / "233-boundary-symplectic-metric-or-local-EH-operator.md", "projector orthogonality and EH gate"),
        (WORK_DIR / "240-universal-coupling-parent-contract-or-local-bound-data-runner.md", "universal matter/coframe contract"),
        (WORK_DIR / "241-C-silence-screening-or-parent-selection-theorem.md", "C silence no-go"),
        (RUN_241 / "status.json", "checkpoint 241 machine status"),
        (RUN_241 / "results" / "C_silence_branch_scorecard.csv", "C branch scorecard"),
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


def branch_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch": "strict_local_coframe",
            "local_C_trace_source": "absent_if_beta_C_local_zero",
            "matter_coupling": "S_matter[Psi, ehat] with ehat independent of C locally",
            "Bianchi_status": "standard matter Ward identity plus geometric sector ledger",
            "representative_status": "local bound representative must be parent-selected",
            "decision": "lead_local_branch",
            "reason": "kills trace source by absence rather than requiring huge screening",
        },
        {
            "branch": "domain_projector_zero_mode",
            "local_C_trace_source": "suppressed_only_if_Pi_D_and_residual_operator_are_parent_owned",
            "matter_coupling": "coherent C_D allowed in cosmology/BAO common-mode branch",
            "Bianchi_status": "conditional if T_Pi,T_D,T_boundary retained",
            "representative_status": "formal candidate; physical scale/representative not parent-derived",
            "decision": "retain_for_cosmology_not_local_rescue",
            "reason": "useful for endpoint memory but too risky as local-GR silence unless fully derived",
        },
        {
            "branch": "ordinary_dynamic_conformal_C",
            "local_C_trace_source": "present",
            "matter_coupling": "ghat=exp(C)g",
            "Bianchi_status": "not enough; matter trace drives C",
            "representative_status": "none",
            "decision": "rejected_as_local_silence_route",
            "reason": "checkpoint 241 no-go: beta_C(T1-T2)=0 forces beta_C=0 or screening",
        },
    ]


def strict_coframe_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "name": "single_observed_coframe",
            "assumption_or_result": "assumption",
            "equation": "S_m = sum_A S_A[Psi_A, ehat, omega[ehat], constants_A]",
            "meaning": "all matter and clocks use one observed coframe",
        },
        {
            "step": 2,
            "name": "local_representative_map",
            "assumption_or_result": "required_parent_selection",
            "equation": "R_loc[D_bound]: ehat^a_mu = Omega_D e^a_mu, partial_mu Omega_D=0",
            "meaning": "local memory/readout is a constant unit representative, not a dynamic conformal field",
        },
        {
            "step": 3,
            "name": "zero_trace_coupling",
            "assumption_or_result": "derived_from_step_2",
            "equation": "beta_C^loc := partial ln ghat_mu_nu / partial C |loc = 0",
            "meaning": "C is not a local matter-metric variable",
        },
        {
            "step": 4,
            "name": "matter_variation",
            "assumption_or_result": "derived",
            "equation": "delta_C S_m = 1/2 int sqrt(-ghat) T_hat beta_C^loc delta C = 0",
            "meaning": "local matter trace does not source C",
        },
        {
            "step": 5,
            "name": "direct_coefficients",
            "assumption_or_result": "derived",
            "equation": "c_matter^direct = c_clock^direct = c_C_trace^loc = 0",
            "meaning": "WEP/direct clock/C-trace channels are killed by the local coframe contract",
        },
        {
            "step": 6,
            "name": "promotion_limit",
            "assumption_or_result": "not_derived",
            "equation": "R_loc[D_bound] from parent action",
            "meaning": "strict coframe is a clean theorem target, not yet a parent theorem",
        },
    ]


def domain_projector_test_rows() -> list[dict[str, Any]]:
    return [
        {
            "test": "variational_projector_exists",
            "requirement": "C=C_D+C_perp plus zero-domain-average residual constraint",
            "current_status": "conditional_pass_from_207",
            "local_readout": "not enough by itself",
            "reason": "formal projection does not pick physical representative",
        },
        {
            "test": "Bianchi_ledger_closed",
            "requirement": "retain T_C,T_Pi,T_D,T_chi,T_rel,T_boundary",
            "current_status": "conditional_pass_from_207",
            "local_readout": "not enough by itself",
            "reason": "conservation bookkeeping is not screening strength",
        },
        {
            "test": "representative_selected",
            "requirement": "local bound domains select trivial class before fitting",
            "current_status": "conditional_ledger_from_208",
            "local_readout": "open",
            "reason": "ideal local/FLRW split exists, but parent selector is not derived",
        },
        {
            "test": "domain_scale_parent_derived",
            "requirement": "L_D=L_cg with parent-owned G_K and alpha_K",
            "current_status": "fail_from_209",
            "local_readout": "open",
            "reason": "L_cg remains labelled closure/theorem target",
        },
        {
            "test": "local_residual_bound_met_by_theorem",
            "requirement": "residual response fraction below 0.000621",
            "current_status": "fail",
            "local_readout": "not_promoted",
            "reason": "no parent response operator norm is derived",
        },
    ]


def Bianchi_requirement_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "strict_local_coframe",
            "required_stress_terms": "T_matter + T_metric + T_memory + T_boundary",
            "forbidden_shortcut": "let memory alter matter clocks while pretending beta_C=0",
            "conservation_condition": "matter Ward identity on ehat plus total geometric Bianchi ledger",
            "status": "cleaner_but_parent_selection_open",
        },
        {
            "route": "domain_projector",
            "required_stress_terms": "T_matter + T_C + T_Pi + T_D + T_chi + T_rel + T_boundary",
            "forbidden_shortcut": "use Pi_D in field equations and drop projector/domain stress",
            "conservation_condition": "all auxiliary/domain variables varied on shell",
            "status": "formal_conditional",
        },
        {
            "route": "trace_cancellation",
            "required_stress_terms": "T_matter + T_C + T_cancel + T_projector",
            "forbidden_shortcut": "insert -T cancellation without stress owner",
            "conservation_condition": "cancellation derived from symmetry or multiplier action",
            "status": "not_derived",
        },
    ]


def local_GR_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "N3 direct matter/clock vertices",
            "status_after_242": "conditional_pass",
            "evidence": "strict coframe theorem gives c_matter_direct=c_clock_direct=0",
            "still_needed": "parent selection of local representative",
        },
        {
            "gate": "C local trace source",
            "status_after_242": "conditional_pass_for_strict_branch",
            "evidence": "beta_C^loc=0 implies delta_C S_m=0",
            "still_needed": "derive R_loc from parent action",
        },
        {
            "gate": "domain projector as local screening",
            "status_after_242": "fail_as_promotion",
            "evidence": "projector action is formal but response bound and representative are not derived",
            "still_needed": "derive Pi_D, L_D, response operator, and stress ledger",
        },
        {
            "gate": "N1/N2/N4/N5/N6",
            "status_after_242": "open",
            "evidence": "not addressed by strict coframe theorem",
            "still_needed": "M_eff, no trace-free shear, exact relative memory, projector stress, auxiliary no-hair",
        },
        {
            "gate": "local Einstein-Hilbert exterior",
            "status_after_242": "open",
            "evidence": "metric-only EH gate not parent-derived",
            "still_needed": "derive metric-only exterior operator",
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
            "gate": "strict local coframe theorem written",
            "status": "conditional_pass",
            "evidence": "beta_C^loc=0 -> delta_C S_m=0",
            "claim_allowed": "conditional theorem only",
        },
        {
            "gate": "domain projector judged for local branch",
            "status": "pass",
            "evidence": "retained for cosmology; not accepted as local rescue",
            "claim_allowed": "branch decision only",
        },
        {
            "gate": "parent selects strict local coframe",
            "status": "fail",
            "evidence": "R_loc[D_bound] not parent-derived",
            "claim_allowed": "no",
        },
        {
            "gate": "domain projector response bound derived",
            "status": "fail",
            "evidence": "operator norm below local gate not derived",
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
            "meaning": "The strict local coframe branch is selected as the clean local C-silence target: if the parent selects a local representative where the observed matter coframe is independent of C up to constant unit rescaling, then beta_C^loc=0 and local matter trace does not source C. The domain projector remains useful for cosmology/BAO endpoint memory but is not allowed as a local-GR rescue until its representative, response bound, and stress ledger are parent-derived.",
            "main_gain": "local C-silence is reduced to a precise representative-selection theorem rather than a vague screening wish",
            "main_failure": "the parent action still has not derived R_loc[D_bound] or the full metric-only exterior",
            "next_target": "243-local-representative-selection-action-or-no-shear-gate.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_242_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    branch_rows = branch_decision_rows()
    theorem_rows = strict_coframe_theorem_rows()
    projector_rows = domain_projector_test_rows()
    bianchi_rows = Bianchi_requirement_rows()
    local_gate_rows = local_GR_gate_rows()
    gates = claim_gate_rows()
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "branch_decision_matrix.csv": (
            branch_rows,
            ["branch", "local_C_trace_source", "matter_coupling", "Bianchi_status", "representative_status", "decision", "reason"],
        ),
        "strict_coframe_theorem_steps.csv": (
            theorem_rows,
            ["step", "name", "assumption_or_result", "equation", "meaning"],
        ),
        "domain_projector_local_test.csv": (
            projector_rows,
            ["test", "requirement", "current_status", "local_readout", "reason"],
        ),
        "Bianchi_requirements_by_route.csv": (
            bianchi_rows,
            ["route", "required_stress_terms", "forbidden_shortcut", "conservation_condition", "status"],
        ),
        "local_GR_gate_after_242.csv": (
            local_gate_rows,
            ["gate", "status_after_242", "evidence", "still_needed"],
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
        "lead_local_C_silence_route": "strict_local_coframe",
        "beta_C_local": 0.0,
        "domain_projector_local_GR_rescue_allowed": False,
        "parent_local_representative_selection_derived": False,
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
