#!/usr/bin/env python3
"""Checkpoint 240: universal coupling parent contract or local-bound data runner."""

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

CHECKPOINT_240_NAME = "universal-coupling-parent-contract-or-local-bound-data-runner"
RUN_239 = RUNS_ROOT / "20260601-000056-nohair-theorem-targets-or-local-bound-runner"

STATUS = "universal_coupling_contract_derives_Pi_matter_zero_conditionally_C_trace_source_and_parent_selection_open_no_promotion"
CLAIM_CEILING = "N3_direct_coupling_theorem_conditional_no_WEP_or_PPN_pass_claim"
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
        (Path(__file__).resolve(), "checkpoint 240 runner"),
        (WORK_DIR / "204-matter-metric-action-and-ruler-transport-owner-contract.md", "candidate universal matter metric"),
        (WORK_DIR / "205-C-silence-source-bound-for-BAO-and-local-rulers.md", "C trace-source hazard"),
        (WORK_DIR / "232-parent-Pmem-projector-or-source-identity-variation.md", "Pi_matter projector target"),
        (WORK_DIR / "239-nohair-theorem-targets-or-local-bound-runner.md", "N3 pressure priority"),
        (RUN_239 / "status.json", "checkpoint 239 machine status"),
        (RUN_239 / "results" / "closure_scenario_readout.csv", "direct-matter leak pressure"),
        (RUN_239 / "results" / "nohair_priority_after_bound_preflight.csv", "N-target priority after local bounds"),
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


def universal_coupling_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "UC0_single_observed_coframe",
            "statement": "All matter and clocks see one observed coframe ehat^a_mu, equivalently one observed metric ghat_mu_nu.",
            "mathematical_form": "S_m = sum_A S_A[Psi_A, ehat, omega[ehat], constants_A]",
            "status": "required_contract",
            "what_it_blocks": "species-dependent metric, composition-dependent free fall, clock-sector split",
        },
        {
            "contract_id": "UC1_no_direct_memory_arguments",
            "statement": "At fixed observed coframe, the matter action has no argument Z_I from the memory/projector sector.",
            "mathematical_form": "(delta S_m / delta Z_I)|_{ehat,Psi}=0 for Z_I in {X,J_rel,V_def,P_mem,C_direct,...}",
            "status": "conditional_theorem_input",
            "what_it_blocks": "Pi_matter leakage and direct composition coupling",
        },
        {
            "contract_id": "UC2_constants_are_species_constants_not_memory_fields",
            "statement": "Masses, charges, and clock transition constants are not functions of memory-sector variables.",
            "mathematical_form": "partial_Z m_A = partial_Z q_A = partial_Z alpha_EM,A = 0",
            "status": "required_contract",
            "what_it_blocks": "fine-structure drift and composition-dependent WEP violation",
        },
        {
            "contract_id": "UC3_universal_conformal_branch_is_not_enough_locally",
            "statement": "A universal conformal factor preserves composition universality but still sources a trace equation unless screened or frozen.",
            "mathematical_form": "ghat_mu_nu = exp(C) g_mu_nu gives delta S_m/delta C = 1/2 sqrt(-ghat) T_hat",
            "status": "open_hazard",
            "what_it_blocks": "claiming N3 also proves C-silence or local GR",
        },
        {
            "contract_id": "UC4_strict_local_branch",
            "statement": "For the local no-hair/PPN branch, the observed coframe is locally independent of memory variables up to constant unit rescaling.",
            "mathematical_form": "partial ghat_mu_nu / partial Z_I = 0 locally, or Delta C = constant common-mode",
            "status": "sufficient_local_condition",
            "what_it_blocks": "direct local fifth-force and clock residuals",
        },
    ]


def variation_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "name": "parent_split",
            "statement": "Split the action into a geometric/MTS sector and a matter sector.",
            "equation": "S = S_geo[g,Z] + S_boundary[g,Z] + S_matter[Psi, ehat]",
            "result": "memory variables may exist, but matter only sees ehat",
        },
        {
            "step": 2,
            "name": "memory_variation_at_fixed_metric",
            "statement": "Vary a memory variable Z_I while holding the observed coframe fixed.",
            "equation": "(delta S_matter / delta Z_I)|_{ehat,Psi} = 0",
            "result": "direct Pi_matter source is zero",
        },
        {
            "step": 3,
            "name": "composition_coefficient",
            "statement": "Since every species shares the same ehat and no species constant depends on Z_I, the direct composition coefficient vanishes.",
            "equation": "c_matter^direct = 0",
            "result": "the WEP/composition channel is killed by absence, not tuning",
        },
        {
            "step": 4,
            "name": "clock_coefficient",
            "statement": "The same argument removes direct memory-clock vertices at fixed observed coframe.",
            "equation": "c_clock^direct = 0",
            "result": "clock residuals can only enter through metric/coframe dynamics or open C-silence terms",
        },
        {
            "step": 5,
            "name": "ward_identity",
            "statement": "Diffeomorphism invariance gives standard matter conservation on matter shell when the direct Z source is zero.",
            "equation": "nabla_hat_mu T_hat^{mu}{}_{nu} = 0",
            "result": "no extra composition-dependent force current appears",
        },
        {
            "step": 6,
            "name": "conformal_warning",
            "statement": "If ehat is built from a dynamic conformal field C, universal coupling alone leaves a trace source.",
            "equation": "delta_C S_matter = 1/2 int sqrt(-ghat) T_hat delta C",
            "result": "C-silence/screening remains a separate theorem burden",
        },
    ]


def forbidden_vertex_rows() -> list[dict[str, Any]]:
    return [
        {
            "vertex": "species_mass_memory_dependence",
            "example": "m_A(Z) psi_A^2",
            "allowed_under_UC": "no",
            "reason": "composition dependence gives non-universal acceleration and WEP leakage",
            "status": "forbidden",
        },
        {
            "vertex": "fine_structure_memory_dependence",
            "example": "f_A(Z) F_A^2 or alpha_EM(Z)",
            "allowed_under_UC": "no",
            "reason": "clock and spectroscopy channels become direct memory probes",
            "status": "forbidden",
        },
        {
            "vertex": "direct_X_current",
            "example": "q_A X_mu J_A^mu",
            "allowed_under_UC": "no",
            "reason": "species charge q_A creates fifth-force/composition channel",
            "status": "forbidden",
        },
        {
            "vertex": "direct_defect_operator",
            "example": "lambda_A V_def O_A",
            "allowed_under_UC": "no",
            "reason": "memory defect potential talks to matter outside the metric",
            "status": "forbidden",
        },
        {
            "vertex": "projector_inside_matter_action",
            "example": "P_mem J_rel contracted with matter current",
            "allowed_under_UC": "no",
            "reason": "the projector would delete a force by hand rather than by action structure",
            "status": "forbidden",
        },
        {
            "vertex": "single_observed_metric",
            "example": "S_A[Psi_A, ehat] for all species A",
            "allowed_under_UC": "yes",
            "reason": "universal metric/coframe coupling is the N3-safe matter branch",
            "status": "allowed",
        },
        {
            "vertex": "constant_common_mode_unit_factor",
            "example": "ehat = Omega_0 e with constant Omega_0",
            "allowed_under_UC": "yes_conditionally",
            "reason": "constant rescaling is unit/common-mode and does not create local composition force",
            "status": "allowed_common_mode",
        },
        {
            "vertex": "dynamic_universal_conformal_factor",
            "example": "ghat_mu_nu = exp(C(x)) g_mu_nu",
            "allowed_under_UC": "not_sufficient_by_itself",
            "reason": "composition universality may survive, but C has trace source and local gradients/drift remain hazardous",
            "status": "open_requires_C_silence",
        },
    ]


def local_bound_implication_rows() -> list[dict[str, Any]]:
    scenario_rows = read_csv_rows(RUN_239 / "results" / "closure_scenario_readout.csv")
    leak_row = next(row for row in scenario_rows if row["scenario"] == "direct_matter_leak_1e-6")
    return [
        {
            "channel": "epsilon_matter",
            "checkpoint_239_pressure": f"1e-6 direct leak ratio_to_bound={float(leak_row['ratio_to_bound']):.6g}",
            "contract_result": "c_matter_direct=0",
            "residual_under_contract": 0.0,
            "status_after_240": "conditionally_removed_by_action_form",
            "remaining_gap": "parent must explain why UC action is mandatory",
        },
        {
            "channel": "alpha_clock",
            "checkpoint_239_pressure": "order-unity tight for direct clock coefficient",
            "contract_result": "c_clock_direct=0",
            "residual_under_contract": 0.0,
            "status_after_240": "direct_clock_vertex_removed_conditionally",
            "remaining_gap": "metric/coframe clock redshift and dynamic C still need their own gate",
        },
        {
            "channel": "C_trace_source",
            "checkpoint_239_pressure": "not represented as composition coefficient",
            "contract_result": "delta S_m/delta C = 1/2 sqrt(-ghat) T_hat if C is in ghat",
            "residual_under_contract": "not_zero_for_dust",
            "status_after_240": "open",
            "remaining_gap": "derive C-silence/screening/fixed-point",
        },
        {
            "channel": "gamma_beta_slip",
            "checkpoint_239_pressure": "N2/N1/N4/N5/N6 remain active",
            "contract_result": "not derived by N3 alone",
            "residual_under_contract": "unchanged",
            "status_after_240": "open",
            "remaining_gap": "derive no-shear, M_eff, relative exactness, projector stress, auxiliary no-hair",
        },
    ]


def nohair_target_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "target": "N3_universal_coupling",
            "status_after_240": "conditional_theorem_for_direct_vertices",
            "what_was_derived": "If matter action depends only on one observed coframe/metric, Pi_matter direct source and direct WEP coefficient vanish exactly.",
            "what_remains": "why the parent action enforces this matter form; dynamic C trace source remains separate",
            "promotion_allowed": "false",
        },
        {
            "target": "N3_clock_part",
            "status_after_240": "conditional_theorem_for_direct_clock_vertices",
            "what_was_derived": "No direct memory-clock vertex at fixed observed coframe.",
            "what_remains": "clock redshift through metric/C dynamics still needs C-silence/local metric branch",
            "promotion_allowed": "false",
        },
        {
            "target": "N2_no_TF",
            "status_after_240": "unchanged_open",
            "what_was_derived": "nothing new",
            "what_remains": "derive no trace-free/tangential exterior stress",
            "promotion_allowed": "false",
        },
        {
            "target": "N1_Meff",
            "status_after_240": "unchanged_open",
            "what_was_derived": "nothing new",
            "what_remains": "derive conserved M_eff and no radial memory profile",
            "promotion_allowed": "false",
        },
        {
            "target": "N4_N5_N6",
            "status_after_240": "unchanged_open",
            "what_was_derived": "nothing new",
            "what_remains": "derive exact relative memory, projector-stress cancellation, and auxiliary no-hair",
            "promotion_allowed": "false",
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
            "gate": "universal matter/coframe contract written",
            "status": "pass",
            "evidence": "UC0-UC4",
            "claim_allowed": "conditional theorem input",
        },
        {
            "gate": "direct Pi_matter source removed",
            "status": "conditional_pass",
            "evidence": "(delta S_m/delta Z_I)|ehat=0",
            "claim_allowed": "only if parent enforces UC action",
        },
        {
            "gate": "WEP/direct composition coefficient zero",
            "status": "conditional_pass",
            "evidence": "c_matter_direct=0, not fitted small",
            "claim_allowed": "no public WEP pass",
        },
        {
            "gate": "dynamic C trace source cleared",
            "status": "fail",
            "evidence": "delta S_m/delta C = 1/2 sqrt(-ghat) T_hat on conformal branch",
            "claim_allowed": "no",
        },
        {
            "gate": "parent selection of universal matter action derived",
            "status": "fail",
            "evidence": "contract is exact but not yet forced by deeper MTS principle",
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
            "meaning": "N3 can be made mathematically sharp: with one observed coframe/metric and no direct memory-sector arguments in S_matter, the direct matter and clock coefficients vanish exactly. This is a conditional theorem from action structure, not a small fitted coefficient. The conformal C branch still has a matter trace source, and the deeper parent principle selecting universal coupling is not derived.",
            "main_gain": "Pi_matter is no longer just a desired projector; it has an exact matter-action condition",
            "main_failure": "universal coupling is a parent contract, not yet a parent selection theorem; C-silence remains open",
            "next_target": "241-C-silence-screening-or-parent-selection-theorem.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_240_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    contract_rows = universal_coupling_contract_rows()
    theorem_rows = variation_theorem_rows()
    vertex_rows = forbidden_vertex_rows()
    implication_rows = local_bound_implication_rows()
    target_rows = nohair_target_status_rows()
    gates = claim_gate_rows()
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "universal_coupling_contract.csv": (
            contract_rows,
            ["contract_id", "statement", "mathematical_form", "status", "what_it_blocks"],
        ),
        "variation_theorem_steps.csv": (
            theorem_rows,
            ["step", "name", "statement", "equation", "result"],
        ),
        "forbidden_vertex_audit.csv": (
            vertex_rows,
            ["vertex", "example", "allowed_under_UC", "reason", "status"],
        ),
        "local_bound_implication.csv": (
            implication_rows,
            ["channel", "checkpoint_239_pressure", "contract_result", "residual_under_contract", "status_after_240", "remaining_gap"],
        ),
        "nohair_target_status_after_240.csv": (
            target_rows,
            ["target", "status_after_240", "what_was_derived", "what_remains", "promotion_allowed"],
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
        "N3_direct_vertices_conditionally_removed": True,
        "c_matter_direct": 0.0,
        "c_clock_direct": 0.0,
        "dynamic_C_trace_source_cleared": False,
        "parent_selection_theorem_derived": False,
        "WEP_pass_claimed": False,
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
