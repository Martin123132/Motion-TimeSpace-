#!/usr/bin/env python3
"""Checkpoint 241: C-silence screening or parent-selection theorem."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

CHECKPOINT_241_NAME = "C-silence-screening-or-parent-selection-theorem"
RUN_240 = RUNS_ROOT / "20260601-000057-universal-coupling-parent-contract-or-local-bound-data-runner"

STATUS = "C_silence_no_go_for_unscreened_conformal_trace_branch_strict_metric_or_screened_zero_mode_required_no_promotion"
CLAIM_CEILING = "C_silence_theorem_conditions_only_no_local_GR_or_BAO_promotion"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"

B_MEM = 2.0 / 27.0
LOCAL_DELTA_C_GATE = 4.6e-5
BAO_150MPC_DELTA_C_GATE = 0.005539695284669133
BAO_FIXED_ALPHA_DOTC_GATE = 0.011285628250379043
BAO_SHARED_ALPHA_DOTC_GATE = 0.018079450186889945


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
        (Path(__file__).resolve(), "checkpoint 241 runner"),
        (WORK_DIR / "205-C-silence-source-bound-for-BAO-and-local-rulers.md", "C trace source and BAO/local bounds"),
        (WORK_DIR / "206-parent-C-screening-fixed-point-mechanism.md", "prior C screening mechanism candidate"),
        (WORK_DIR / "207-domain-projector-action-and-Bianchi-identity.md", "domain projector/Bianchi gap"),
        (WORK_DIR / "240-universal-coupling-parent-contract-or-local-bound-data-runner.md", "universal coupling theorem and C hazard"),
        (RUN_240 / "status.json", "checkpoint 240 machine status"),
        (RUN_240 / "results" / "local_bound_implication.csv", "N3 implication and C trace-source open row"),
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


def C_equation_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch": "strict_local_metric",
            "matter_metric": "ghat_mu_nu = g_mu_nu locally, up to constant unit rescaling",
            "matter_variation": "(delta S_m/delta C)|ghat = 0",
            "local_equation": "E_C[C,Z,g] = 0",
            "silence_result": "C has no direct local matter trace source",
            "status": "sufficient_if_parent_selected",
        },
        {
            "branch": "dynamic_conformal",
            "matter_metric": "ghat_mu_nu = exp(C) g_mu_nu",
            "matter_variation": "delta S_m/delta C = 1/2 sqrt(-ghat) T_hat",
            "local_equation": "E_C[C,Z,g] + 1/2 sqrt(-ghat) T_hat = 0",
            "silence_result": "local matter trace sources C unless screened/cancelled",
            "status": "unscreened_branch_rejected_as_local_silence_theorem",
        },
        {
            "branch": "screened_zero_mode",
            "matter_metric": "ghat may contain coherent C_D but local residuals are projected/screened",
            "matter_variation": "Pi_D(T_hat) drives domain mode; (1-Pi_D)T_hat suppressed",
            "local_equation": "(Z_C[-nabla^2+m_eff^2]) delta C = beta_C (1-Pi_D)delta T + cancellation",
            "silence_result": "possible only if projector/screening is parent-owned",
            "status": "candidate_not_derived",
        },
    ]


def plateau_no_go_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition": "local_plateau_definition",
            "equation": "C(x)=C_* with partial_mu C=0 over local exterior/readout patch",
            "derived_requirement": "E_C(C_*) + beta_C T(x) + E_cancel(C_*,T,x)=0 for allowed T(x)",
            "verdict": "definition",
            "meaning": "a local plateau must solve the field equation, not just be desired",
        },
        {
            "condition": "arbitrary_trace_no_go",
            "equation": "E_C(C_*) + beta_C T_1 = 0 and E_C(C_*) + beta_C T_2 = 0",
            "derived_requirement": "beta_C(T_1-T_2)=0",
            "verdict": "beta_C_must_vanish_without_cancellation",
            "meaning": "one fixed plateau cannot handle independent matter traces if C is directly trace-coupled",
        },
        {
            "condition": "strict_metric_escape",
            "equation": "partial ghat_mu_nu/partial C = 0 locally",
            "derived_requirement": "beta_C=0",
            "verdict": "works_conditionally",
            "meaning": "the trace source is absent because C is not a local matter-metric variable",
        },
        {
            "condition": "owned_cancellation_escape",
            "equation": "E_cancel = -beta_C T for local trace sector",
            "derived_requirement": "cancellation must come from parent action and Bianchi ledger",
            "verdict": "possible_but_not_derived",
            "meaning": "otherwise it is just hiding the forbidden coupling",
        },
        {
            "condition": "screening_escape",
            "equation": "delta C_L / B_mem <= bound_L / B_mem",
            "derived_requirement": "response operator norm R_C(L) below relevant gate",
            "verdict": "possible_but_stiff",
            "meaning": "local gates are much tighter than BAO-domain gates",
        },
    ]


def suppression_bound_rows() -> list[dict[str, Any]]:
    bounds = [
        ("local_Delta_C_gate", LOCAL_DELTA_C_GATE),
        ("BAO_150Mpc_spatial_Delta_C_gate", BAO_150MPC_DELTA_C_GATE),
        ("BAO_fixed_alpha_dotC_over_H_gate", BAO_FIXED_ALPHA_DOTC_GATE),
        ("BAO_shared_alpha_dotC_over_H_gate", BAO_SHARED_ALPHA_DOTC_GATE),
    ]
    rows: list[dict[str, Any]] = []
    for name, bound in bounds:
        fraction = bound / B_MEM
        rows.append(
            {
                "gate": name,
                "bound": bound,
                "reference_amplitude_Bmem": B_MEM,
                "required_response_fraction": fraction,
                "minimum_suppression_factor": 1.0 / fraction if fraction > 0 else math.inf,
                "readout": "dominant_local_gate" if name == "local_Delta_C_gate" else "less_tight_than_local_gate",
            }
        )
    return rows


def branch_scorecard_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch": "ordinary_light_dynamic_C",
            "result": "reject_as_local_silence_route",
            "why": "trace source survives and produces local response",
            "what_would_save_it": "none without turning into screening/cancellation/strict branch",
        },
        {
            "branch": "strict_local_metric_or_coframe",
            "result": "best_clean_route",
            "why": "beta_C=0 locally so delta S_m/delta C is absent",
            "what_would_save_it": "derive parent selection of strict observed coframe",
        },
        {
            "branch": "coherent_domain_zero_mode",
            "result": "viable_candidate",
            "why": "C_D can carry endpoint memory while local residual modes are projected/suppressed",
            "what_would_save_it": "derive Pi_D from action and Bianchi-safe stress ledger",
        },
        {
            "branch": "heavy_or_stiff_C",
            "result": "side_route",
            "why": "can suppress residuals but local gate requires strong stiffness",
            "what_would_save_it": "derive large local m_eff or equivalent operator from parent action",
        },
        {
            "branch": "trace_sequestering",
            "result": "possible_but_dangerous",
            "why": "could cancel T source but risks being a hidden fit unless symmetry-owned",
            "what_would_save_it": "derive exact cancellation plus total Bianchi conservation",
        },
    ]


def parent_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract": "PC1_zero_local_trace_coupling",
            "equation": "partial ghat_mu_nu/partial C = 0 in local branch",
            "needed_for": "strict local C silence",
            "status": "sufficient_not_derived",
        },
        {
            "contract": "PC2_domain_projector",
            "equation": "delta_lambda S -> (1-Pi_D)C = suppressed or constrained",
            "needed_for": "coherent zero-mode memory without local trace response",
            "status": "candidate_not_derived",
        },
        {
            "contract": "PC3_Bianchi_safe_cancellation",
            "equation": "nabla_mu(T_m + T_C + T_projector + T_cancel)^{mu}{}_{nu}=0",
            "needed_for": "any trace cancellation route",
            "status": "not_derived",
        },
        {
            "contract": "PC4_late_endpoint_saturation",
            "equation": "Delta C_cosmic ~= B_mem while local dot_C/H and grad C obey gates",
            "needed_for": "cosmological memory with local/BAO silence",
            "status": "not_derived",
        },
    ]


def target_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "target": "C_silence",
            "status_after_241": "unscreened_conformal_branch_rejected",
            "derived_result": "A fixed local plateau for arbitrary trace T requires beta_C=0 or parent-owned cancellation/screening.",
            "remaining_gap": "derive strict local metric branch or domain projector from parent action",
        },
        {
            "target": "N3_universal_coupling",
            "status_after_241": "sharpened",
            "derived_result": "Universal coupling kills direct composition vertices, but dynamic conformal C is not enough.",
            "remaining_gap": "parent selection and C silence",
        },
        {
            "target": "local_GR",
            "status_after_241": "not_promoted",
            "derived_result": "ordinary dynamic C cannot be smuggled into local GR as silent",
            "remaining_gap": "N1/N2/N4/N5/N6 and EH exterior still open",
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
            "gate": "C trace-source equation written",
            "status": "pass",
            "evidence": "delta S_m/delta C = 1/2 sqrt(-ghat) T_hat",
            "claim_allowed": "theorem bookkeeping only",
        },
        {
            "gate": "unscreened conformal plateau no-go derived",
            "status": "pass",
            "evidence": "beta_C(T1-T2)=0 condition",
            "claim_allowed": "negative result",
        },
        {
            "gate": "strict local metric escape identified",
            "status": "conditional_pass",
            "evidence": "beta_C=0 locally",
            "claim_allowed": "only if parent selection derived",
        },
        {
            "gate": "screening/domain projector parent-derived",
            "status": "fail",
            "evidence": "operator/projector not derived here",
            "claim_allowed": "no",
        },
        {
            "gate": "local GR or BAO support promoted",
            "status": "fail",
            "evidence": CLAIM_CEILING,
            "claim_allowed": "no",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "meaning": "The dynamic conformal C branch is not locally silent by universal coupling alone. A local plateau for arbitrary matter trace requires zero local trace coupling, or a parent-owned cancellation/screening/domain projector. This is a useful negative theorem: ordinary unscreened C cannot be used as a local-GR rescue.",
            "main_gain": "C-silence is now split into strict local metric selection or parent-derived screening, with an explicit no-go for the naive conformal branch",
            "main_failure": "the strict branch and domain projector remain unselected by a deeper parent principle",
            "next_target": "242-strict-local-coframe-branch-or-domain-projector-action.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_241_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    equation_rows = C_equation_rows()
    no_go_rows = plateau_no_go_rows()
    bound_rows = suppression_bound_rows()
    branch_rows = branch_scorecard_rows()
    contract_rows = parent_contract_rows()
    target_rows = target_status_rows()
    gates = claim_gate_rows()
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "C_silence_equation_branches.csv": (
            equation_rows,
            ["branch", "matter_metric", "matter_variation", "local_equation", "silence_result", "status"],
        ),
        "plateau_no_go_conditions.csv": (
            no_go_rows,
            ["condition", "equation", "derived_requirement", "verdict", "meaning"],
        ),
        "suppression_bound_table.csv": (
            bound_rows,
            ["gate", "bound", "reference_amplitude_Bmem", "required_response_fraction", "minimum_suppression_factor", "readout"],
        ),
        "C_silence_branch_scorecard.csv": (
            branch_rows,
            ["branch", "result", "why", "what_would_save_it"],
        ),
        "parent_selection_contracts.csv": (
            contract_rows,
            ["contract", "equation", "needed_for", "status"],
        ),
        "target_status_after_241.csv": (
            target_rows,
            ["target", "status_after_241", "derived_result", "remaining_gap"],
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
        "unscreened_dynamic_conformal_C_rejected_as_local_silence": True,
        "strict_local_metric_branch_sufficient_if_parent_selected": True,
        "screening_or_domain_projector_derived": False,
        "local_GR_promoted": False,
        "BAO_support_promoted": False,
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
