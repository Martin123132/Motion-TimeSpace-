#!/usr/bin/env python3
"""Checkpoint 202: derive the late common-mode H0-r_d BAO owner, or demote."""

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

CHECKPOINT_202_NAME = "late-common-mode-H0-rd-owner-derivation-attempt"
CHECKPOINT_201_RUN = RUNS_ROOT / "20260601-000018-BAO-strict-alpha-results-and-H0-rd-owner-decision"
CHECKPOINT_200_RUN = RUNS_ROOT / "20260601-000017-BAO-strict-alpha-shape-stress-or-parent-H0-rd-contract"
CHECKPOINT_197_RUN = RUNS_ROOT / "20260601-000014-BAO-common-mode-ratio-theorem-attempt"
CHECKPOINT_195_RUN = RUNS_ROOT / "20260601-000012-late-CMB-domain-rule-and-local-silence-gate"

STATUS = "late_common_mode_BAO_owner_partially_derived_ruler_transport_parent_missing"
CLAIM_CEILING = "BAO_late_common_mode_derivation_internal_only_transport_parent_missing"
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


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_register_rows() -> list[dict[str, Any]]:
    paths = [
        (Path(__file__).resolve(), "checkpoint 202 late common-mode BAO derivation script"),
        (WORK_DIR / "201-BAO-strict-alpha-results-and-H0-rd-owner-decision.md", "BAO alpha owner decision checkpoint"),
        (CHECKPOINT_201_RUN / "status.json", "checkpoint 201 machine status"),
        (CHECKPOINT_201_RUN / "results" / "endpoint_domain_assignment.csv", "checkpoint 201 domain assignment"),
        (CHECKPOINT_201_RUN / "results" / "H0_rd_owner_options.csv", "checkpoint 201 H0-r_d owner options"),
        (WORK_DIR / "200-BAO-strict-alpha-shape-stress-or-parent-H0-rd-contract.md", "strict alpha stress checkpoint"),
        (CHECKPOINT_200_RUN / "results" / "alpha_candidate_scorecard.csv", "checkpoint 200 alpha scorecard"),
        (WORK_DIR / "197-BAO-common-mode-ratio-theorem-attempt.md", "BAO common-mode theorem checkpoint"),
        (CHECKPOINT_197_RUN / "status.json", "checkpoint 197 machine status"),
        (WORK_DIR / "195-late-CMB-domain-rule-and-local-silence-gate.md", "endpoint Delta C rule checkpoint"),
        (CHECKPOINT_195_RUN / "status.json", "checkpoint 195 machine status"),
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


def ruler_history_derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "claim": "BAO r_d is generated at the drag epoch as an acoustic scale.",
            "equation_or_rule": "r_d = integral_{z_drag}^{infty} c_s(z)/H(z) dz",
            "status": "standard_background_ruler_definition",
            "derivation_level": "borrowed_standard_physics_with_MTS_background_check",
        },
        {
            "step": 2,
            "claim": "After drag, the BAO scale is transported as a comoving matter-correlation imprint.",
            "equation_or_rule": "r_d^comoving is carried by late galaxy/matter correlations, not by a photon emitted at z_drag",
            "status": "key_late_common_mode_distinction",
            "derivation_level": "physical_observer_map_argument",
        },
        {
            "step": 3,
            "claim": "The observed BAO signal is read out in a late survey using late matter clocks/rulers.",
            "equation_or_rule": "tilde_D_X = exp(C_obs/2) D_X and tilde_r_d^{late} = exp(C_obs/2) r_d",
            "status": "common_mode_if_late_matter_unit_holds",
            "derivation_level": "conditional_conformal_unit_algebra",
        },
        {
            "step": 4,
            "claim": "The conformal unit cancels in BAO ratios.",
            "equation_or_rule": "tilde_D_X/tilde_r_d^{late}=D_X/r_d for X in {M,H,V}, up to radial dot_C/H leakage",
            "status": "conditional_ratio_theorem_from_checkpoint_197",
            "derivation_level": "partial_theorem",
        },
        {
            "step": 5,
            "claim": "CMB differs because it compares an early photon/ruler endpoint to a late observer endpoint.",
            "equation_or_rule": "Delta C_CMB ~= C_obs-C_emit ~= B_mem, while Delta C_BAO_late_readout ~= 0 for common units",
            "status": "domain_distinction",
            "derivation_level": "endpoint_rule_application",
        },
        {
            "step": 6,
            "claim": "The parent theory must still derive comoving ruler transport and late-unit assignment.",
            "equation_or_rule": "D_t r_d^comoving = 0 after drag, and matter survey observable uses tilde_r_d^{late}",
            "status": "parent_transport_missing",
            "derivation_level": "contract_not_proof",
        },
    ]


def endpoint_distinction_rows() -> list[dict[str, Any]]:
    return [
        {
            "observable": "CMB acoustic angle",
            "object_read_out": "photon acoustic pattern from recombination to late observer",
            "endpoint_memory": "early-to-late Delta C ~= B_mem",
            "calibration_branch": "CMB endpoint-jump/half-memory clock bridge",
            "why_not_late_common_mode": "emitter and observer are not in the same late matter-unit frame",
            "status": "separate_CMB_domain",
        },
        {
            "observable": "BAO ratios",
            "object_read_out": "late galaxy correlation separation carrying a fossil comoving acoustic scale",
            "endpoint_memory": "late readout common-mode if the ruler is expressed in late matter units",
            "calibration_branch": "late H0-r_d common-mode alpha",
            "why_not_late_common_mode": "not applicable; this is the late common-mode route",
            "status": "lead_BAO_domain",
        },
        {
            "observable": "SN/local distance ladder",
            "object_read_out": "late local standards and late observer calibration",
            "endpoint_memory": "late common-mode if local/environmental silence holds",
            "calibration_branch": "late H0 calibration",
            "why_not_late_common_mode": "fails if local C gradients/drift leak",
            "status": "conditional_late_domain",
        },
        {
            "observable": "growth",
            "object_read_out": "path-dependent perturbation evolution",
            "endpoint_memory": "not reducible to endpoint algebra",
            "calibration_branch": "none yet",
            "why_not_late_common_mode": "requires perturbation equations",
            "status": "not_closed",
        },
    ]


def strict_alpha_evidence_rows() -> list[dict[str, Any]]:
    scorecard = read_csv_rows(CHECKPOINT_200_RUN / "results" / "alpha_candidate_scorecard.csv")
    rows: list[dict[str, Any]] = []
    for row in scorecard:
        candidate = row["alpha_candidate"]
        if candidate in {"late_reference_H0_rdrag", "same_density_CMB_profile_H0_rdrag", "exp_half_memory_H0_rdrag"}:
            rows.append(
                {
                    "release": row["release"],
                    "alpha_candidate": candidate,
                    "locked_delta_chi2_vs_shared_alpha": row["locked_delta_chi2_vs_shared_alpha"],
                    "verdict": row["verdict"],
                    "domain_readout": (
                        "supports_late_common_mode_candidate"
                        if candidate == "late_reference_H0_rdrag"
                        else "pressures_CMB_endpoint_alpha_for_BAO"
                    ),
                }
            )
    return rows


def theorem_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_piece": "BAO is not direct early photon endpoint",
            "status": "partial_pass",
            "evidence": "BAO is a late matter-correlation readout of a fossil comoving ruler",
            "remaining_gap": "formal parent transport equation for the fossil ruler",
        },
        {
            "theorem_piece": "late conformal unit cancels in D_X/r_d",
            "status": "partial_pass",
            "evidence": "checkpoint 197 common-mode ratio algebra",
            "remaining_gap": "radial dot_C/H suppression and late-unit assignment",
        },
        {
            "theorem_piece": "CMB endpoint alpha demoted for BAO",
            "status": "pass_as_domain_gate",
            "evidence": "checkpoint 200 strict-alpha pressure for CMB-profile and half-memory alpha",
            "remaining_gap": "parent action must derive domain assignment",
        },
        {
            "theorem_piece": "late H0-r_d alpha selected",
            "status": "theorem_target",
            "evidence": "late-reference alpha survives DR1 and soft-warns DR2",
            "remaining_gap": "release-independent parent prediction still missing",
        },
        {
            "theorem_piece": "local silence consistency",
            "status": "open",
            "evidence": "endpoint route requires late common-mode without local clock/PPN leakage",
            "remaining_gap": "derive partial_mu C -> 0 and dot_C -> 0 locally",
        },
    ]


def parent_transport_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract": "fossil ruler transport",
            "required_statement": "after drag, the acoustic scale is transported as a conserved comoving matter-correlation ruler",
            "mathematical_form": "D_t r_d^comoving = 0 plus controlled corrections",
            "failure_if_missing": "BAO r_d could inherit early endpoint memory incorrectly",
            "status": "missing_parent_equation",
        },
        {
            "contract": "late matter-unit projection",
            "required_statement": "the observed BAO ruler is projected into the same late matter metric as D_M, D_H, and D_V",
            "mathematical_form": "tilde_r_d^{late}=exp(C_obs/2) r_d",
            "failure_if_missing": "D_X/r_d common-mode cancellation is only asserted",
            "status": "conditional_projection",
        },
        {
            "contract": "radial drift silence",
            "required_statement": "dot_C/H is small in BAO redshift bins",
            "mathematical_form": "tilde_D_H/tilde_r_d=(D_H/r_d)/(1+dot_C/(2H)) with dot_C/H within DESI tolerance",
            "failure_if_missing": "radial BAO shape can leak clock drift",
            "status": "bounded_not_parent_derived",
        },
        {
            "contract": "domain selector",
            "required_statement": "one parent rule separates CMB early-to-late endpoint memory from BAO late common-mode readout",
            "mathematical_form": "observable class determined by whether the measured standard is a photon endpoint or late matter-correlation readout",
            "failure_if_missing": "domain assignment becomes post-hoc",
            "status": "partial_rule_not_action_derived",
        },
        {
            "contract": "release-independent alpha",
            "required_statement": "derive a predeclared alpha or controlled release-independent calibration",
            "mathematical_form": "alpha_BAO=c/(H0_late r_d^{late}) with parent-owned H0_late and r_d^{late}",
            "failure_if_missing": "BAO remains shared-alpha empirical closure",
            "status": "missing",
        },
    ]


def claim_gate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing = sum(row["exists"] != "yes" for row in source_rows)
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing == 0 else "fail",
            "evidence": f"missing={missing}",
            "claim_allowed": "internal derivation attempt",
        },
        {
            "gate": "BAO late-readout distinction written",
            "status": "pass",
            "evidence": "BAO ruler treated as late matter-correlation fossil, not direct early photon endpoint",
            "claim_allowed": "conditional theorem piece",
        },
        {
            "gate": "CMB endpoint branch separated from BAO",
            "status": "pass",
            "evidence": "CMB-profile and half-memory alpha demoted for BAO by strict-alpha stress",
            "claim_allowed": "domain guardrail",
        },
        {
            "gate": "parent fossil-ruler transport derived",
            "status": "fail",
            "evidence": "D_t r_d^comoving=0 is a required contract, not parent-derived here",
            "claim_allowed": "no promotion",
        },
        {
            "gate": "release-independent alpha prediction derived",
            "status": "fail",
            "evidence": "late alpha is a theorem candidate; readbacks remain quarantined",
            "claim_allowed": "no promotion",
        },
        {
            "gate": "BAO support claim allowed",
            "status": "fail",
            "evidence": CLAIM_CEILING,
            "claim_allowed": "no",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "meaning": "The BAO late common-mode H0-r_d owner has a plausible derivation route: BAO is a late matter-correlation readout of a fossil comoving ruler, so the conformal late matter unit cancels in D_X/r_d. But the parent transport equation and release-independent alpha prediction remain missing.",
            "partial_derivation": "BAO is late fossil-ruler readout, not direct early photon endpoint",
            "lead_owner": "late_common_mode_H0_rd_alpha",
            "demoted_owner": "CMB_endpoint_jump_alpha_for_BAO",
            "next_target": "203-fossil-ruler-transport-equation-attempt.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_202_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    ruler_rows = ruler_history_derivation_rows()
    endpoint_rows = endpoint_distinction_rows()
    evidence_rows = strict_alpha_evidence_rows()
    theorem_rows = theorem_status_rows()
    contract_rows = parent_transport_contract_rows()
    gates = claim_gate_rows(source_rows)
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "BAO_ruler_history_derivation.csv": (
            ruler_rows,
            ["step", "claim", "equation_or_rule", "status", "derivation_level"],
        ),
        "endpoint_distinction_table.csv": (
            endpoint_rows,
            ["observable", "object_read_out", "endpoint_memory", "calibration_branch", "why_not_late_common_mode", "status"],
        ),
        "strict_alpha_domain_evidence.csv": (
            evidence_rows,
            ["release", "alpha_candidate", "locked_delta_chi2_vs_shared_alpha", "verdict", "domain_readout"],
        ),
        "theorem_status.csv": (
            theorem_rows,
            ["theorem_piece", "status", "evidence", "remaining_gap"],
        ),
        "parent_transport_contract.csv": (
            contract_rows,
            ["contract", "required_statement", "mathematical_form", "failure_if_missing", "status"],
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
                "partial_derivation",
                "lead_owner",
                "demoted_owner",
                "next_target",
                "promotion_allowed",
                "claim_ceiling",
            ],
        ),
    }
    for filename, (rows, fieldnames) in files.items():
        write_csv(results_dir / filename, rows, fieldnames)

    status_payload = {
        "status": decision[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(files.keys()),
        "BAO_late_common_mode_owner_partially_derived": True,
        "fossil_ruler_transport_parent_derived": False,
        "release_independent_alpha_parent_derived": False,
        "CMB_endpoint_alpha_demoted_for_BAO": True,
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
    payload = run(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
