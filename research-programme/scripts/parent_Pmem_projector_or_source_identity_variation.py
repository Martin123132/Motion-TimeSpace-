#!/usr/bin/env python3
"""Checkpoint 232: parent P_mem projector or source-identity variation."""

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

CHECKPOINT_232_NAME = "parent-Pmem-projector-or-source-identity-variation"
RUN_231 = RUNS_ROOT / "20260601-000048-Jrel-cohomology-projector-or-local-EH-limit"

STATUS = "Pmem_charge_projector_candidate_and_projected_source_identity_template_parent_symplectic_owner_open_no_promotion"
CLAIM_CEILING = "Pmem_projector_candidate_no_parent_symplectic_or_local_GR_promotion"
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
        (Path(__file__).resolve(), "checkpoint 232 runner"),
        (WORK_DIR / "221-Noether-source-identity-or-compact-PPN-closure-map.md", "source identity variation template"),
        (WORK_DIR / "223-X-constraint-algebra-and-Khat-Gamma-constitutive-owner.md", "X multiplier and symplectic gap"),
        (WORK_DIR / "224-defect-potential-Vdef-or-X-route-demotion.md", "V_def and boundary demotion"),
        (WORK_DIR / "230-exterior-vacuum-Einstein-branch-or-Jrel-representative.md", "exterior beta contract"),
        (WORK_DIR / "231-Jrel-cohomology-projector-or-local-EH-limit.md", "J_rel cohomology/projector gate"),
        (RUN_231 / "status.json", "checkpoint 231 machine status"),
        (RUN_231 / "results" / "Pmem_projector_contract.csv", "checkpoint 231 projector contract"),
        (RUN_231 / "results" / "coefficient_status_after_231.csv", "checkpoint 231 coefficient status"),
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


def charge_projector_rows() -> list[dict[str, Any]]:
    return [
        {
            "piece": "mass_harmonic_flux",
            "definition": "Pi_M J = H_S2 * integral_{S^2} J / integral_{S^2} H_S2",
            "projector_action": "subtract from memory current and store as M_eff",
            "parent_status": "charge_split_candidate",
            "why_needed": "absolute H^2 class is real and must not be erased",
        },
        {
            "piece": "tangential_shear",
            "definition": "Pi_TF J = trace-free/tangential l>=2 shell component",
            "projector_action": "subtract from local memory sector",
            "parent_status": "symmetry_candidate",
            "why_needed": "prevents Phi-Psi/gamma slip source",
        },
        {
            "piece": "clock_matter_direct",
            "definition": "Pi_matter J = component coupling directly to matter or clocks",
            "projector_action": "forbid from memory sector",
            "parent_status": "universal_coupling_contract",
            "why_needed": "protects WEP/redshift channels",
        },
        {
            "piece": "relative_exact_memory",
            "definition": "P_mem J = (1-Pi_M-Pi_TF-Pi_matter)J",
            "projector_action": "place in relative exact cohomology channel",
            "parent_status": "candidate_not_parent_derived",
            "why_needed": "lets H^2_relative=0 force exactness",
        },
    ]


def derivation_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "name": "boundary_phase_space_split",
            "statement": "Decompose boundary current data into charge, shear, matter-coupled, and relative memory sectors.",
            "math": "J = Pi_M J + Pi_TF J + Pi_matter J + P_mem J",
            "status": "canonical_candidate",
            "gap": "requires parent boundary symplectic form to be a theorem",
        },
        {
            "step": 2,
            "name": "mass_charge_not_erased",
            "statement": "The absolute S^2 harmonic flux is retained as the ordinary monopole/effective mass.",
            "math": "Q_M=integral_S2 J; Q_M -> M_eff",
            "status": "derived_requirement_from_231",
            "gap": "",
        },
        {
            "step": 3,
            "name": "no_slip_shear_removal",
            "statement": "The trace-free/tangential shell component is excluded from the local memory sector by scalar-boundary symmetry.",
            "math": "Pi_TF P_mem J = 0",
            "status": "conditional_from_229",
            "gap": "scalar boundary owner not full parent action",
        },
        {
            "step": 4,
            "name": "relative_memory_channel",
            "statement": "The remaining projected current is assigned to the relative memory sector.",
            "math": "P_mem J in Omega^2(Sigma,partial Sigma)",
            "status": "candidate",
            "gap": "parent action has not supplied boundary primitive A_rel",
        },
        {
            "step": 5,
            "name": "cohomology_exactness",
            "statement": "If projected current is closed, shell relative cohomology forces exactness.",
            "math": "d_rel P_mem J=0 and H^2(Sigma,partial Sigma)=0 => P_mem J=d_rel A_rel",
            "status": "topological_sufficient",
            "gap": "closedness follows only after source identity/projector ownership",
        },
        {
            "step": 6,
            "name": "parent_projector_verdict",
            "statement": "The projector is now a unique minimal charge/shear decomposition candidate, not a parent-derived operator.",
            "math": "P_mem = 1 - Pi_M - Pi_TF - Pi_matter",
            "status": "partial_progress_no_promotion",
            "gap": "need parent symplectic metric or constraints deriving Pi_M/Pi_TF/Pi_matter",
        },
    ]


def source_identity_template_rows() -> list[dict[str, Any]]:
    return [
        {
            "template_piece": "projected_X_constraint",
            "action_form": "S_X=-int sqrt(-g) X_nu[nabla_mu P[Y]^{mu nu}-S_L^nu-d_rel(P_mem J_rel)^nu]+boundary",
            "variation_result": "nabla_mu P[Y]^{mu nu}=S_L^nu+d_rel(P_mem J_rel)^nu",
            "status": "valid_template",
            "gap": "P_mem and P[Y] not parent-owned",
        },
        {
            "template_piece": "trace_split",
            "action_form": "P^{mu nu}=Khat^{mu nu}-Gamma_eff g^{mu nu}",
            "variation_result": "nabla_mu Khat^{mu nu}-nabla^nu Gamma_eff=S_L^nu+d_rel(P_mem J_rel)^nu",
            "status": "valid_template",
            "gap": "Khat/Gamma constitutive owner still partial",
        },
        {
            "template_piece": "boundary_cancellation",
            "action_form": "S_boundary=-int_boundary B_X^nu X_nu+S_rel[B_X,A_rel]",
            "variation_result": "B_X^nu=n_mu P^{mu nu}; A_rel supplies relative primitive",
            "status": "conditional_template",
            "gap": "boundary primitive not selected by parent action",
        },
        {
            "template_piece": "no_hair_constraint",
            "action_form": "X appears as multiplier only",
            "variation_result": "pi_X=0, C_X=0 should remove X degrees",
            "status": "conditional_template",
            "gap": "constraint algebra still open",
        },
    ]


def ownership_matrix_rows() -> list[dict[str, Any]]:
    return [
        {
            "object": "Pi_M",
            "candidate_owner": "asymptotic/Komar-like mass charge or ADM monopole",
            "current_status": "candidate",
            "promotion_blocker": "local mass definition in parent MTS action not derived",
        },
        {
            "object": "Pi_TF",
            "candidate_owner": "scalar boundary symmetry and trace-free shell projector",
            "current_status": "conditional",
            "promotion_blocker": "parent boundary variables may still contain tangent tensor channel",
        },
        {
            "object": "Pi_matter",
            "candidate_owner": "universal metric coupling action",
            "current_status": "contract",
            "promotion_blocker": "matter/clock action not specified",
        },
        {
            "object": "P_mem",
            "candidate_owner": "orthogonal complement under parent boundary symplectic metric",
            "current_status": "not_derived",
            "promotion_blocker": "parent boundary symplectic metric missing",
        },
        {
            "object": "source_identity",
            "candidate_owner": "X multiplier variation",
            "current_status": "template",
            "promotion_blocker": "X no-hair algebra and P[Y] owner missing",
        },
    ]


def coefficient_status_rows() -> list[dict[str, Any]]:
    previous = read_csv_rows(RUN_231 / "results" / "coefficient_status_after_231.csv")
    previous_by_residual = {row["residual"]: row for row in previous}
    updates = {
        "gamma_minus_1": (
            "projector_candidate_supports_no_shear",
            "Pi_TF removal is now part of the candidate parent projector",
            "derive Pi_TF from parent boundary variables",
        ),
        "Phi_minus_Psi": (
            "projector_candidate_supports_no_shear",
            "Pi_TF removal is now part of the candidate parent projector",
            "derive scalar boundary owner fully",
        ),
        "G_eff_over_G_minus_1": (
            "mass_projector_candidate",
            "Pi_M explicitly preserves monopole mass as M_eff rather than erasing it",
            "derive M_eff/source normalization from parent action",
        ),
        "alpha_clock": (
            "unchanged_universal_metric_contract",
            "Pi_matter forbids direct clock channel but is not parent-derived",
            "derive matter/clock action",
        ),
        "epsilon_matter": (
            "unchanged_universal_metric_contract",
            "Pi_matter forbids direct composition channel but is not parent-derived",
            "derive matter action",
        ),
        "beta_minus_1": (
            "projector_candidate_plus_source_identity_template",
            "beta route gains a candidate P_mem and projected source-identity template",
            "derive parent symplectic projector and local EH exterior limit",
        ),
    }
    rows: list[dict[str, Any]] = []
    for residual, prior in previous_by_residual.items():
        status, result, next_needed = updates[residual]
        rows.append(
            {
                "residual": residual,
                "checkpoint_231_status": prior["checkpoint_231_status"],
                "checkpoint_232_status": status,
                "coefficient_after_232": result,
                "parent_derived": "no",
                "promotion_allowed": "false",
                "next_needed": next_needed,
            }
        )
    return rows


def claim_gate_rows(source_rows: list[dict[str, Any]], coefficient_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = sum(row["exists"] != "yes" for row in source_rows)
    beta_candidate = any(
        row["residual"] == "beta_minus_1"
        and row["checkpoint_232_status"] == "projector_candidate_plus_source_identity_template"
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
            "gate": "P_mem minimal decomposition candidate written",
            "status": "pass",
            "evidence": "P_mem=1-Pi_M-Pi_TF-Pi_matter",
            "claim_allowed": "candidate only",
        },
        {
            "gate": "mass class preserved rather than erased",
            "status": "pass",
            "evidence": "Pi_M maps absolute S2 flux to M_eff",
            "claim_allowed": "contract requirement",
        },
        {
            "gate": "projected source-identity template written",
            "status": "pass",
            "evidence": "X variation with d_rel(P_mem J_rel)",
            "claim_allowed": "template only",
        },
        {
            "gate": "beta route strengthened",
            "status": "pass" if beta_candidate else "fail",
            "evidence": "candidate projector plus source identity template",
            "claim_allowed": "conditional only",
        },
        {
            "gate": "parent boundary symplectic projector derived",
            "status": "fail",
            "evidence": "parent boundary metric/constraints missing",
            "claim_allowed": "no q_loc promotion",
        },
        {
            "gate": "source identity parent-derived",
            "status": "fail",
            "evidence": "X no-hair and P[Y] owner still open",
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
            "meaning": "A minimal non-cheating P_mem candidate now exists: keep the absolute S2 harmonic flux as M_eff, remove trace-free/tangential shear, forbid direct matter/clock coupling, and send only the remaining relative memory current into the exact cohomology channel. The projected source-identity variation is also written. This strengthens the local q_loc/beta route, but P_mem is still not parent-derived because the parent boundary symplectic metric, constraints, matter coupling, and X no-hair algebra remain open.",
            "main_gain": "P_mem is now a named charge/shear decomposition candidate rather than an arbitrary eraser",
            "main_failure": "parent symplectic ownership of the projector and source identity is still missing",
            "next_target": "233-boundary-symplectic-metric-or-local-EH-operator.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_232_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    charge_projectors = charge_projector_rows()
    derivation = derivation_attempt_rows()
    source_identity = source_identity_template_rows()
    ownership = ownership_matrix_rows()
    coefficients = coefficient_status_rows()
    gates = claim_gate_rows(source_rows, coefficients)
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "charge_projector_decomposition.csv": (
            charge_projectors,
            ["piece", "definition", "projector_action", "parent_status", "why_needed"],
        ),
        "Pmem_derivation_attempt_steps.csv": (
            derivation,
            ["step", "name", "statement", "math", "status", "gap"],
        ),
        "projected_source_identity_template.csv": (
            source_identity,
            ["template_piece", "action_form", "variation_result", "status", "gap"],
        ),
        "ownership_matrix.csv": (
            ownership,
            ["object", "candidate_owner", "current_status", "promotion_blocker"],
        ),
        "coefficient_status_after_232.csv": (
            coefficients,
            [
                "residual",
                "checkpoint_231_status",
                "checkpoint_232_status",
                "coefficient_after_232",
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
        "Pmem_minimal_candidate_written": True,
        "mass_class_preserved_as_Meff": True,
        "projected_source_identity_template_written": True,
        "parent_boundary_symplectic_projector_derived": False,
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
