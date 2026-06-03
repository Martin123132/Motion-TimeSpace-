#!/usr/bin/env python3
"""Checkpoint 229: scalar boundary owner and second-order beta reduction."""

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

CHECKPOINT_229_NAME = "second-order-beta-or-boundary-scalar-owner"
RUN_228 = RUNS_ROOT / "20260601-000045-isotropic-response-condition-or-official-local-bound-runner"

STATUS = "scalar_boundary_symmetry_owner_derived_sufficient_beta_reduced_to_vacuum_Einstein_gate_no_PPN_promotion"
CLAIM_CEILING = "scalar_boundary_sufficient_owner_plus_beta_reduction_no_parent_local_GR_or_PPN_promotion"
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
        (Path(__file__).resolve(), "checkpoint 229 runner"),
        (WORK_DIR / "138-coherent-volume-pressure-kernel-theorem.md", "N_D as coherent scalar volume variable"),
        (WORK_DIR / "139-density-law-hazard-theorem-attempt.md", "activation shape as scalar hazard route"),
        (WORK_DIR / "143-domain-selector-variational-action-attempt.md", "boundary-current owner obstruction"),
        (WORK_DIR / "177-parent-action-perturbation-local-GR-contract.md", "parent action and local-GR contract"),
        (WORK_DIR / "179-local-GR-PPN-silence-contract.md", "effective local PPN fence and beta warning"),
        (WORK_DIR / "211-GK-parent-metric-Ward-identity-attempt.md", "flow block partial geometric ownership"),
        (WORK_DIR / "224-defect-potential-Vdef-or-X-route-demotion.md", "V_def boundary demotion"),
        (WORK_DIR / "228-isotropic-response-condition-or-official-local-bound-runner.md", "no-slip sufficient condition"),
        (RUN_228 / "status.json", "checkpoint 228 machine status"),
        (RUN_228 / "results" / "coefficient_status_after_228.csv", "checkpoint 228 coefficient status"),
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


def scalar_boundary_derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "name": "boundary_worldtube_data",
            "statement": "Represent the compact local collar by induced boundary metric gamma_AB, normal n^mu, and scalar MTS data only.",
            "math": "Y_boundary={N_D,C_coh,I_M,K,R_boundary,n^mu partial_mu phi_A, scalar memory}",
            "status": "definition",
            "remaining_gap": "",
        },
        {
            "step": 2,
            "name": "scalar_only_action",
            "statement": "Take the boundary action to be a diffeomorphism-invariant scalar functional of Y_boundary with no tangential vector, tensor, or harmonic labels.",
            "math": "S_boundary=int_boundary sqrt(|gamma|) F(Y_boundary)",
            "status": "sufficient_contract",
            "remaining_gap": "F is not yet derived from the full parent action",
        },
        {
            "step": 3,
            "name": "little_group_argument",
            "statement": "On a stationary compact isotropic collar, the tangent little group permits only gamma_AB as a rank-2 stress tensor.",
            "math": "tau_AB invariant under shell rotations => tau_AB=tau gamma_AB",
            "status": "derived_from_symmetry",
            "remaining_gap": "requires no hidden tangent-frame field in the parent variables",
        },
        {
            "step": 4,
            "name": "variational_trace_result",
            "statement": "The boundary stress from the scalar-only action has zero trace-free part on the compact isotropic collar.",
            "math": "tau_AB=-(2/sqrt(|gamma|)) delta S_boundary/delta gamma^AB; tau_TF_AB=0",
            "status": "derived_as_sufficient_condition",
            "remaining_gap": "linear TF response still requires no trace-free boundary Hessian/source",
        },
        {
            "step": 5,
            "name": "link_to_checkpoint_228",
            "statement": "Substituting tau_TF_AB=0 into the trace-free weak-field constraint gives the no-slip result.",
            "math": "D_AB(Phi-Psi)=8 pi G tau_TF_AB=0 => Phi-Psi=0 after compact matching",
            "status": "closes_228_conditionally",
            "remaining_gap": "Einstein-like trace-free constraint still needs parent derivation",
        },
        {
            "step": 6,
            "name": "boundary_owner_readout",
            "statement": "The boundary scalar owner is now symmetry-owned as a sufficient theorem, not parent-owned as the final MTS action.",
            "math": "scalar symmetry owner != parent action owner",
            "status": "partial_promotion_only",
            "remaining_gap": "derive F and allowed Y_boundary from V_def/M_AB/J_rel without closure choices",
        },
    ]


def allowed_forbidden_rows() -> list[dict[str, Any]]:
    return [
        {
            "item": "N_D",
            "allowed_or_forbidden": "allowed",
            "reason": "coherent volume scalar from checkpoint 138",
            "stress_effect": "trace pressure only on isotropic collar",
            "status": "partial_owner",
        },
        {
            "item": "C_coh or I_M",
            "allowed_or_forbidden": "allowed",
            "reason": "domain coherence/exposure scalar; shape support from checkpoint 139",
            "stress_effect": "trace/common-mode if no tangential gradients",
            "status": "conditional_owner",
        },
        {
            "item": "K trace and R_boundary scalar",
            "allowed_or_forbidden": "allowed",
            "reason": "geometric shell scalars",
            "stress_effect": "isotropic on stationary maximally symmetric collar",
            "status": "sufficient_condition",
        },
        {
            "item": "trace-free extrinsic curvature K_TF_AB",
            "allowed_or_forbidden": "forbidden_for_local_no_slip",
            "reason": "directly supplies anisotropic boundary response",
            "stress_effect": "can source Phi-Psi",
            "status": "must_be_absent_or_suppressed",
        },
        {
            "item": "tangential J_rel_A or memory shear",
            "allowed_or_forbidden": "forbidden_for_local_no_slip",
            "reason": "creates l>=2 angular boundary data",
            "stress_effect": "can source gamma/slip residuals",
            "status": "main_boundary_blocker",
        },
        {
            "item": "direct matter or clock coupling",
            "allowed_or_forbidden": "forbidden_for_local_universal_coupling",
            "reason": "would face WEP/redshift bounds independently of metric slip",
            "stress_effect": "composition/clock residual",
            "status": "must_be_absent",
        },
    ]


def beta_reduction_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause": "B1",
            "requirement": "exterior q_loc source vanishes",
            "math": "q_loc^nu=0 for r>R_shell",
            "effect_on_beta": "removes non-GR exterior forcing",
            "status": "not_parent_derived",
        },
        {
            "clause": "B2",
            "requirement": "exterior field equation is Einstein vacuum up to mass renormalization",
            "math": "G_mu_nu=0 outside compact collar, M -> M_eff",
            "effect_on_beta": "Birkhoff/Schwarzschild exterior fixes beta=1",
            "status": "theorem_target",
        },
        {
            "clause": "B3",
            "requirement": "scalar boundary response carries monopole/common-mode only",
            "math": "delta Phi=delta Psi=delta(GM/r), no independent U^2 operator",
            "effect_on_beta": "renormalizes source amplitude but not beta",
            "status": "sufficient_if_B1_B2_hold",
        },
        {
            "clause": "B4",
            "requirement": "no exterior scalar/vector/tensor hair",
            "math": "X,J_rel,V_def boundary modes have no propagating exterior profile",
            "effect_on_beta": "prevents fifth-force beta shift",
            "status": "open_constraint_algebra",
        },
        {
            "clause": "B5",
            "requirement": "isotropic-coordinate expansion matches Schwarzschild",
            "math": "g_00=-1+2U-2U^2+O(U^3)",
            "effect_on_beta": "beta=1",
            "status": "conditional_consequence",
        },
    ]


def coefficient_status_rows() -> list[dict[str, Any]]:
    previous = read_csv_rows(RUN_228 / "results" / "coefficient_status_after_228.csv")
    previous_by_residual = {row["residual"]: row for row in previous}
    updates = {
        "gamma_minus_1": (
            "stronger_sufficient_owner",
            "c_gamma=0 if scalar-only boundary symmetry and Einstein-like TF constraint hold",
            "symmetry-owned sufficient condition, parent F still open",
        ),
        "Phi_minus_Psi": (
            "stronger_sufficient_owner",
            "c_slip=0 by tau_TF_AB=0 on compact isotropic collar",
            "symmetry-owned sufficient condition, parent F still open",
        ),
        "G_eff_over_G_minus_1": (
            "monopole_only",
            "common-mode scalar boundary may renormalize mass/source amplitude",
            "needs source-normalization equation",
        ),
        "alpha_clock": (
            "unchanged_universal_metric_contract",
            "safe only if clocks couple only to g_mu_nu/coframe",
            "parent matter/clock action open",
        ),
        "epsilon_matter": (
            "unchanged_universal_metric_contract",
            "safe only if no direct composition coupling to memory/boundary sector",
            "parent matter action open",
        ),
        "beta_minus_1": (
            "reduced_not_derived",
            "beta=1 follows if exterior branch is vacuum Einstein/Schwarzschild with only mass renormalization",
            "derive q_loc=0 plus exterior Einstein vacuum and no hair",
        ),
    }
    rows: list[dict[str, Any]] = []
    for residual, prior in previous_by_residual.items():
        status, result, next_needed = updates[residual]
        rows.append(
            {
                "residual": residual,
                "checkpoint_228_status": prior["checkpoint_228_status"],
                "checkpoint_229_status": status,
                "coefficient_after_229": result,
                "parent_derived": "no",
                "promotion_allowed": "false",
                "next_needed": next_needed,
            }
        )
    return rows


def owner_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "owner_piece": "scalar boundary symmetry",
            "status": "derived_as_sufficient",
            "evidence": "little-group/variational argument gives tau_TF_AB=0",
            "remaining_gap": "prove parent variables contain no hidden tangent tensor",
        },
        {
            "owner_piece": "N_D volume scalar",
            "status": "partial_conditional",
            "evidence": "checkpoint 138 pressure kernel from metric variation",
            "remaining_gap": "domain selector and boundary variation not owned",
        },
        {
            "owner_piece": "hazard scalar I_M",
            "status": "partial_conditional",
            "evidence": "checkpoint 139 additive hazard shape",
            "remaining_gap": "amplitude and parent exposure variable open",
        },
        {
            "owner_piece": "J_rel local representative",
            "status": "open",
            "evidence": "checkpoint 143 and 220-224 retain boundary-current obstruction",
            "remaining_gap": "derive local trivial/FLRW nontrivial representative",
        },
        {
            "owner_piece": "local Einstein trace-free constraint",
            "status": "open",
            "evidence": "checkpoint 228 uses it as necessary bridge",
            "remaining_gap": "derive from parent local field equations",
        },
        {
            "owner_piece": "beta second-order temporal equation",
            "status": "reduced_to_vacuum_Einstein_gate",
            "evidence": "Schwarzschild exterior would fix beta=1",
            "remaining_gap": "derive exterior vacuum Einstein branch rather than assume it",
        },
    ]


def claim_gate_rows(source_rows: list[dict[str, Any]], coefficient_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = sum(row["exists"] != "yes" for row in source_rows)
    no_slip_owned = sum(row["checkpoint_229_status"] == "stronger_sufficient_owner" for row in coefficient_rows)
    beta_reduced = any(row["residual"] == "beta_minus_1" and row["checkpoint_229_status"] == "reduced_not_derived" for row in coefficient_rows)
    return [
        {
            "gate": "all cited local sources exist",
            "status": "pass" if missing_sources == 0 else "fail",
            "evidence": f"missing={missing_sources}",
            "claim_allowed": "internal checkpoint only",
        },
        {
            "gate": "scalar boundary symmetry gives trace-only stress",
            "status": "pass",
            "evidence": "little-group/variational theorem on compact isotropic collar",
            "claim_allowed": "sufficient theorem condition",
        },
        {
            "gate": "gamma/slip coefficient owner strengthened",
            "status": "pass" if no_slip_owned >= 2 else "fail",
            "evidence": f"stronger_sufficient_owner_rows={no_slip_owned}",
            "claim_allowed": "conditional, no PPN promotion",
        },
        {
            "gate": "beta reduced to exact vacuum-Einstein gate",
            "status": "pass" if beta_reduced else "fail",
            "evidence": "beta=1 follows from exterior Schwarzschild branch, but branch not derived",
            "claim_allowed": "theorem target only",
        },
        {
            "gate": "parent scalar boundary action derived",
            "status": "fail",
            "evidence": "F(Y_boundary), J_rel representative, and parent variable set still open",
            "claim_allowed": "no local-GR claim",
        },
        {
            "gate": "exterior vacuum Einstein branch derived",
            "status": "fail",
            "evidence": "q_loc=0 and no-hair constraint algebra still not parent-derived",
            "claim_allowed": "no beta/PPN claim",
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
            "meaning": "The scalar-only compact boundary owner is now derived as a sufficient symmetry theorem: if the boundary action uses only scalar shell data and no tangential memory shear, its compact isotropic stress is trace-only, so the checkpoint-228 no-slip condition is owned at the symmetry level. Beta is not derived, but its exact target is now cleaner: beta=1 follows if the exterior compact branch is vacuum Einstein/Schwarzschild with only mass renormalization and no exterior memory hair.",
            "main_gain": "gamma/slip local safety moved from assumed common-mode to scalar-boundary symmetry ownership",
            "main_failure": "parent F(Y_boundary), J_rel representative, q_loc=0 exterior branch, and second-order beta remain open",
            "next_target": "230-exterior-vacuum-Einstein-branch-or-Jrel-representative.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_229_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    scalar_rows = scalar_boundary_derivation_rows()
    allowed_rows = allowed_forbidden_rows()
    beta_rows = beta_reduction_rows()
    coefficient_rows = coefficient_status_rows()
    owner_rows = owner_status_rows()
    gates = claim_gate_rows(source_rows, coefficient_rows)
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "scalar_boundary_derivation_steps.csv": (
            scalar_rows,
            ["step", "name", "statement", "math", "status", "remaining_gap"],
        ),
        "allowed_forbidden_boundary_terms.csv": (
            allowed_rows,
            ["item", "allowed_or_forbidden", "reason", "stress_effect", "status"],
        ),
        "beta_reduction_ledger.csv": (
            beta_rows,
            ["clause", "requirement", "math", "effect_on_beta", "status"],
        ),
        "coefficient_status_after_229.csv": (
            coefficient_rows,
            [
                "residual",
                "checkpoint_228_status",
                "checkpoint_229_status",
                "coefficient_after_229",
                "parent_derived",
                "promotion_allowed",
                "next_needed",
            ],
        ),
        "owner_status_matrix.csv": (
            owner_rows,
            ["owner_piece", "status", "evidence", "remaining_gap"],
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
    stronger_no_slip_rows = sum(row["checkpoint_229_status"] == "stronger_sufficient_owner" for row in coefficient_rows)
    status_payload = {
        "status": decision[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(files.keys()),
        "missing_sources": missing_sources,
        "scalar_boundary_symmetry_owner_derived_sufficient": True,
        "stronger_no_slip_coefficients": stronger_no_slip_rows,
        "parent_scalar_boundary_action_derived": False,
        "beta_reduced_to_vacuum_Einstein_gate": True,
        "beta_second_order_parent_derived": False,
        "exterior_vacuum_Einstein_branch_derived": False,
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
