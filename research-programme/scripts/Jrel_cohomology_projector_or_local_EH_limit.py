#!/usr/bin/env python3
"""Checkpoint 231: J_rel cohomology projector or local EH limit."""

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

CHECKPOINT_231_NAME = "Jrel-cohomology-projector-or-local-EH-limit"
RUN_230 = RUNS_ROOT / "20260601-000047-exterior-vacuum-Einstein-branch-or-Jrel-representative"

STATUS = "Jrel_local_projector_relative_cohomology_sufficient_gate_derived_parent_projector_open_no_PPN_promotion"
CLAIM_CEILING = "Jrel_cohomology_sufficient_gate_no_parent_projector_or_local_EH_promotion"
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
        (Path(__file__).resolve(), "checkpoint 231 runner"),
        (WORK_DIR / "220-Jrel-local-trivial-representative-or-closure-bound.md", "J_rel exactness target"),
        (WORK_DIR / "221-Noether-source-identity-or-compact-PPN-closure-map.md", "source identity target"),
        (WORK_DIR / "223-X-constraint-algebra-and-Khat-Gamma-constitutive-owner.md", "X no-hair algebra gap"),
        (WORK_DIR / "229-second-order-beta-or-boundary-scalar-owner.md", "beta reduction to exterior gate"),
        (WORK_DIR / "230-exterior-vacuum-Einstein-branch-or-Jrel-representative.md", "exterior branch contract"),
        (RUN_230 / "status.json", "checkpoint 230 machine status"),
        (RUN_230 / "results" / "coefficient_status_after_230.csv", "checkpoint 230 coefficient status"),
        (RUN_230 / "results" / "Jrel_representative_conditions.csv", "checkpoint 230 J_rel conditions"),
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


def topology_rows() -> list[dict[str, Any]]:
    return [
        {
            "object": "compact exterior spatial shell",
            "symbol": "Sigma_ext",
            "value": "S^2 x [R_inner,R_outer]",
            "meaning": "annular spatial shell around a compact source",
            "status": "topology_model",
        },
        {
            "object": "absolute H^1",
            "symbol": "H^1(Sigma_ext)",
            "value": "0",
            "meaning": "closed one-form memory currents are exact",
            "status": "useful_safe_channel",
        },
        {
            "object": "absolute H^2",
            "symbol": "H^2(Sigma_ext)",
            "value": "R",
            "meaning": "there is a nontrivial S^2 flux class, matching ordinary enclosed charge/mass danger",
            "status": "danger_channel",
        },
        {
            "object": "relative H^2",
            "symbol": "H^2(Sigma_ext,partial Sigma_ext)",
            "value": "0",
            "meaning": "relative two-form memory flux with pure-gauge boundary primitive has no cohomology obstruction",
            "status": "useful_safe_channel",
        },
        {
            "object": "relative H^1",
            "symbol": "H^1(Sigma_ext,partial Sigma_ext)",
            "value": "R",
            "meaning": "a relative one-form class can exist, so degree/projector choice matters",
            "status": "warning",
        },
    ]


def cohomology_derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "name": "shell_topology",
            "statement": "The local exterior collar is an annulus with spatial topology S^2 x I.",
            "math": "Sigma_ext ~= S^2 x [R_inner,R_outer]",
            "status": "topological_model",
            "remaining_gap": "prove the parent local collar really uses this projected topology",
        },
        {
            "step": 2,
            "name": "mass_flux_warning",
            "statement": "Absolute two-form flux through S^2 is nontrivial, so ordinary enclosed mass charge cannot be forced exact.",
            "math": "H^2(Sigma_ext)=R",
            "status": "derived_warning",
            "remaining_gap": "",
        },
        {
            "step": 3,
            "name": "memory_projector",
            "statement": "Define the local memory projector by removing the absolute S^2 flux/mass class and tangential shear modes.",
            "math": "P_mem J_rel = J_rel - Pi_mass J_rel - Pi_shear J_rel",
            "status": "required_projector_contract",
            "remaining_gap": "P_mem is not parent-derived",
        },
        {
            "step": 4,
            "name": "relative_flux_channel",
            "statement": "For a memory-exchange two-form with pure-gauge/vanishing boundary primitive, the relevant class is relative H^2.",
            "math": "[P_mem J_rel] in H^2(Sigma_ext,partial Sigma_ext)=0",
            "status": "derived_topological_gate",
            "remaining_gap": "boundary primitive still not selected by parent action",
        },
        {
            "step": 5,
            "name": "exactness_result",
            "statement": "Since relative H^2 vanishes, any closed projected relative memory flux is exact.",
            "math": "d_rel(P_mem J_rel)=0 and [P_mem J_rel]=0 => P_mem J_rel=d_rel A_rel",
            "status": "sufficient_cohomology_result",
            "remaining_gap": "closedness and projector ownership are parent gaps",
        },
        {
            "step": 6,
            "name": "one_form_crosscheck",
            "statement": "If the local memory current is represented as a one-form instead, absolute H^1=0 also gives closed implies exact.",
            "math": "H^1(Sigma_ext)=0",
            "status": "degree_crosscheck",
            "remaining_gap": "parent theory must specify degree unambiguously",
        },
        {
            "step": 7,
            "name": "qloc_consequence",
            "statement": "With the source identity, projected exactness gives q_loc=0 in the exterior memory sector.",
            "math": "q_loc^nu=-P_loc d_rel J_rel^nu=0",
            "status": "conditional_consequence",
            "remaining_gap": "Noether source identity and parent projector remain open",
        },
    ]


def projector_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "projector_clause": "P0",
            "requirement": "J_rel is typed as memory/domain exchange, not mass/Gauss flux",
            "test": "ordinary enclosed mass maps to M_eff, not J_rel",
            "status": "required_contract",
        },
        {
            "projector_clause": "P1",
            "requirement": "remove absolute S^2 harmonic flux class",
            "test": "integral_{S^2_r} P_mem J_rel = 0",
            "status": "topology_required",
        },
        {
            "projector_clause": "P2",
            "requirement": "remove tangential shear/l>=2 shell data",
            "test": "Pi_shear P_mem J_rel = 0",
            "status": "no_slip_required",
        },
        {
            "projector_clause": "P3",
            "requirement": "boundary primitive is pure gauge or vanishes on inner and outer shell",
            "test": "A_rel|partial Sigma_ext = gauge",
            "status": "relative_boundary_required",
        },
        {
            "projector_clause": "P4",
            "requirement": "projected memory current is closed in exterior vacuum",
            "test": "d_rel P_mem J_rel = 0",
            "status": "source_identity_required",
        },
        {
            "projector_clause": "P5",
            "requirement": "projector and current follow from parent variation, not post hoc filtering",
            "test": "P_mem appears in parent symplectic/constraint structure",
            "status": "parent_gap",
        },
    ]


def coefficient_status_rows() -> list[dict[str, Any]]:
    previous = read_csv_rows(RUN_230 / "results" / "coefficient_status_after_230.csv")
    previous_by_residual = {row["residual"]: row for row in previous}
    updates = {
        "gamma_minus_1": (
            "unchanged_no_slip_sufficient",
            "still protected only if scalar boundary/no shear contract holds",
            "derive P_mem shear removal from parent action",
        ),
        "Phi_minus_Psi": (
            "unchanged_no_slip_sufficient",
            "still protected only if P_mem removes tangential shear/l>=2 modes",
            "derive P_mem shear removal from parent action",
        ),
        "G_eff_over_G_minus_1": (
            "mass_class_separated",
            "ordinary mass charge is kept as M_eff while memory flux is projected exact",
            "derive source-normalization relation",
        ),
        "alpha_clock": (
            "unchanged_universal_metric_contract",
            "no update; clock safety still requires universal metric coupling",
            "derive matter/clock action",
        ),
        "epsilon_matter": (
            "unchanged_universal_metric_contract",
            "no update; WEP safety still requires no direct memory composition coupling",
            "derive matter action",
        ),
        "beta_minus_1": (
            "cohomology_gate_sufficient_not_parent_derived",
            "beta route improved because J_rel exactness now has a shell-cohomology gate after mass/shear projection",
            "derive parent P_mem and local EH exterior operator",
        ),
    }
    rows: list[dict[str, Any]] = []
    for residual, prior in previous_by_residual.items():
        status, result, next_needed = updates[residual]
        rows.append(
            {
                "residual": residual,
                "checkpoint_230_status": prior["checkpoint_230_status"],
                "checkpoint_231_status": status,
                "coefficient_after_231": result,
                "parent_derived": "no",
                "promotion_allowed": "false",
                "next_needed": next_needed,
            }
        )
    return rows


def local_eh_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "EH_clause": "EH1",
            "requirement": "source identity reduces q_loc to projected memory current",
            "current_status": "conditional",
            "effect": "needed before cohomology can silence q_loc",
        },
        {
            "EH_clause": "EH2",
            "requirement": "projected J_rel exact/trivial in exterior",
            "current_status": "topology sufficient gate written",
            "effect": "removes memory source",
        },
        {
            "EH_clause": "EH3",
            "requirement": "all memory stress vanishes or becomes M_eff monopole",
            "current_status": "not derived",
            "effect": "prevents exterior non-Schwarzschild stress",
        },
        {
            "EH_clause": "EH4",
            "requirement": "metric kinetic/operator block reduces to Einstein-Hilbert",
            "current_status": "not derived",
            "effect": "required for G_mu_nu=0",
        },
        {
            "EH_clause": "EH5",
            "requirement": "X/V_def/J_rel no exterior propagating hair",
            "current_status": "not derived",
            "effect": "required for PPN safety",
        },
    ]


def claim_gate_rows(source_rows: list[dict[str, Any]], coefficient_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = sum(row["exists"] != "yes" for row in source_rows)
    beta_gate = any(
        row["residual"] == "beta_minus_1"
        and row["checkpoint_231_status"] == "cohomology_gate_sufficient_not_parent_derived"
        for row in coefficient_rows
    )
    return [
        {
            "gate": "all cited local sources exist",
            "status": "pass" if missing_sources == 0 else "fail",
            "evidence": f"missing={missing_sources}",
            "claim_allowed": "internal checkpoint only",
        },
        {
            "gate": "shell cohomology computed",
            "status": "pass",
            "evidence": "H1_abs=0; H2_abs=R; H2_relative=0",
            "claim_allowed": "topological sufficient gate",
        },
        {
            "gate": "mass flux danger separated",
            "status": "pass",
            "evidence": "absolute H2 class retained as M_eff, not J_rel",
            "claim_allowed": "contract requirement",
        },
        {
            "gate": "J_rel exactness has non-cheating route",
            "status": "pass",
            "evidence": "relative H2=0 after P_mem and boundary primitive",
            "claim_allowed": "sufficient theorem target",
        },
        {
            "gate": "beta route strengthened by cohomology",
            "status": "pass" if beta_gate else "fail",
            "evidence": "J_rel exactness condition is now topological/projector gate",
            "claim_allowed": "conditional only",
        },
        {
            "gate": "parent P_mem projector derived",
            "status": "fail",
            "evidence": "projector is required but not derived from parent action",
            "claim_allowed": "no q_loc promotion",
        },
        {
            "gate": "local EH exterior limit derived",
            "status": "fail",
            "evidence": "metric operator and no-hair algebra remain open",
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
            "meaning": "The local J_rel exactness route now has a real topology gate. On a compact exterior shell Sigma ~= S^2 x I, absolute H^2 carries the ordinary enclosed mass/flux danger and must be kept as M_eff, not J_rel. After projecting J_rel to memory exchange, removing S^2 harmonic flux and tangential shear, and imposing relative pure-gauge boundary primitive, H^2(Sigma,partial Sigma)=0 forces closed projected memory flux to be exact. This strengthens q_loc/beta but still does not derive the parent projector, source identity, or local Einstein-Hilbert exterior limit.",
            "main_gain": "J_rel exactness is no longer only a hope; it has a shell-cohomology projector criterion",
            "main_failure": "P_mem, source identity, no-hair algebra, and local EH limit remain parent gaps",
            "next_target": "232-parent-Pmem-projector-or-source-identity-variation.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_231_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    topology = topology_rows()
    derivation = cohomology_derivation_rows()
    projector = projector_contract_rows()
    coefficients = coefficient_status_rows()
    local_eh = local_eh_status_rows()
    gates = claim_gate_rows(source_rows, coefficients)
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "shell_topology_cohomology.csv": (
            topology,
            ["object", "symbol", "value", "meaning", "status"],
        ),
        "Jrel_cohomology_derivation_steps.csv": (
            derivation,
            ["step", "name", "statement", "math", "status", "remaining_gap"],
        ),
        "Pmem_projector_contract.csv": (
            projector,
            ["projector_clause", "requirement", "test", "status"],
        ),
        "coefficient_status_after_231.csv": (
            coefficients,
            [
                "residual",
                "checkpoint_230_status",
                "checkpoint_231_status",
                "coefficient_after_231",
                "parent_derived",
                "promotion_allowed",
                "next_needed",
            ],
        ),
        "local_EH_limit_status.csv": (
            local_eh,
            ["EH_clause", "requirement", "current_status", "effect"],
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
        "shell_cohomology_gate_written": True,
        "absolute_mass_flux_class_separated": True,
        "relative_H2_memory_exactness_sufficient": True,
        "parent_Pmem_projector_derived": False,
        "source_identity_parent_derived": False,
        "local_EH_exterior_limit_derived": False,
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
