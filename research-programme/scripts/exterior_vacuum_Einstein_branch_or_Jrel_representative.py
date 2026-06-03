#!/usr/bin/env python3
"""Checkpoint 230: exterior vacuum-Einstein branch or J_rel representative."""

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

CHECKPOINT_230_NAME = "exterior-vacuum-Einstein-branch-or-Jrel-representative"
RUN_229 = RUNS_ROOT / "20260601-000046-second-order-beta-or-boundary-scalar-owner"

STATUS = "exterior_vacuum_Einstein_sufficient_contract_written_Jrel_representative_open_beta_not_promoted"
CLAIM_CEILING = "exterior_vacuum_sufficient_contract_no_parent_local_GR_or_PPN_promotion"
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
        (Path(__file__).resolve(), "checkpoint 230 runner"),
        (WORK_DIR / "219-compact-shell-q_loc-source-projection-attempt.md", "q_loc source-projection route"),
        (WORK_DIR / "220-Jrel-local-trivial-representative-or-closure-bound.md", "J_rel exactness route"),
        (WORK_DIR / "221-Noether-source-identity-or-compact-PPN-closure-map.md", "Noether/source identity route"),
        (WORK_DIR / "222-parent-X-sector-degree-count-and-boundary-action.md", "X multiplier boundary action"),
        (WORK_DIR / "223-X-constraint-algebra-and-Khat-Gamma-constitutive-owner.md", "X constraint algebra gap"),
        (WORK_DIR / "224-defect-potential-Vdef-or-X-route-demotion.md", "V_def demotion"),
        (WORK_DIR / "228-isotropic-response-condition-or-official-local-bound-runner.md", "no-slip condition"),
        (WORK_DIR / "229-second-order-beta-or-boundary-scalar-owner.md", "beta reduction gate"),
        (RUN_229 / "status.json", "checkpoint 229 machine status"),
        (RUN_229 / "results" / "coefficient_status_after_229.csv", "checkpoint 229 coefficient status"),
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


def exterior_derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "name": "define_exterior_region",
            "statement": "Work outside a compact stationary collar, r>R_shell, with ordinary matter source removed.",
            "math": "E={r>R_shell}; S_L^nu=0; T_matter_mu_nu=0 in E",
            "status": "definition",
            "remaining_gap": "",
        },
        {
            "step": 2,
            "name": "use_source_identity",
            "statement": "If the parent Noether identity holds, q_loc is controlled only by the relative memory current in vacuum.",
            "math": "q_loc^nu=P_loc(nabla^nu Gamma_eff-nabla_mu Khat^{mu nu})=-P_loc d_rel J_rel^nu",
            "status": "conditional_on_checkpoint_221",
            "remaining_gap": "source identity is not parent-derived",
        },
        {
            "step": 3,
            "name": "exact_memory_representative",
            "statement": "If the projected memory current is exact in the local exterior sector, its relative derivative vanishes.",
            "math": "J_rel=d_rel A_rel => d_rel J_rel=d_rel^2 A_rel=0",
            "status": "sufficient_condition",
            "remaining_gap": "parent action has not selected this representative",
        },
        {
            "step": 4,
            "name": "cohomology_filter",
            "statement": "The exactness route is allowed only for the memory-exchange class, not for the ordinary mass/Gauss charge.",
            "math": "memory H_rel class trivial; ordinary enclosed mass charge not identified with J_rel",
            "status": "necessary_separation",
            "remaining_gap": "requires explicit J_rel type and projector",
        },
        {
            "step": 5,
            "name": "no_exterior_memory_stress",
            "statement": "With scalar boundary stress localized on the shell and exact J_rel outside, exterior memory stress vanishes or is absorbed into M_eff.",
            "math": "T_memory_mu_nu|E=0, M -> M_eff",
            "status": "sufficient_condition",
            "remaining_gap": "metric variation of boundary/V_def sector still open",
        },
        {
            "step": 6,
            "name": "Einstein_operator_gate",
            "statement": "If the local metric operator outside the shell is the Einstein-Hilbert one, the exterior equation is vacuum Einstein.",
            "math": "G_mu_nu=0 in E",
            "status": "theorem_gate_not_derived",
            "remaining_gap": "parent local metric operator is not derived from MTS action",
        },
        {
            "step": 7,
            "name": "Schwarzschild_beta",
            "statement": "Static spherical asymptotically-flat vacuum Einstein exterior gives Schwarzschild and beta=1.",
            "math": "g_00=-1+2U-2U^2+O(U^3), beta=1",
            "status": "conditional_consequence",
            "remaining_gap": "depends on steps 2-6",
        },
    ]


def jrel_conditions_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition": "memory_current_not_mass_flux",
            "requirement": "J_rel must represent memory/domain exchange, not ordinary Newtonian or GR Gauss flux",
            "why_needed": "ordinary mass flux is nontrivial around a compact source and cannot be set exact",
            "status": "contract_required",
        },
        {
            "condition": "relative_exactness",
            "requirement": "J_rel=d_rel A_rel in the projected local memory sector",
            "why_needed": "gives d_rel J_rel=0 without declaring J_rel=0",
            "status": "sufficient_not_parent_derived",
        },
        {
            "condition": "boundary_primitive_pure_gauge",
            "requirement": "A_rel vanishes or matches pure gauge on inner and outer compact-shell boundaries",
            "why_needed": "prevents hidden boundary exchange through the collar",
            "status": "sufficient_not_parent_derived",
        },
        {
            "condition": "no_nontrivial_local_cohomology_class",
            "requirement": "projected memory class has no local harmonic representative in the exterior shell",
            "why_needed": "closed but non-exact memory current would source q_loc",
            "status": "open_topology_projector",
        },
        {
            "condition": "X_multiplier_no_hair",
            "requirement": "X enforces the source identity but carries no exterior propagating degree",
            "why_needed": "otherwise the cure becomes a fifth-force/vector-hair source",
            "status": "open_constraint_algebra",
        },
    ]


def beta_branch_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_piece": "q_loc exterior silence",
            "needed_result": "q_loc^nu=0 in E",
            "current_status": "sufficient route written through exact J_rel",
            "beta_effect": "removes explicit MTS exterior force",
        },
        {
            "branch_piece": "memory stress exterior silence",
            "needed_result": "T_memory_mu_nu|E=0 except mass renormalization",
            "current_status": "sufficient scalar-boundary route, not metric-variation theorem",
            "beta_effect": "prevents non-Schwarzschild stress profile",
        },
        {
            "branch_piece": "local metric operator",
            "needed_result": "Einstein-Hilbert vacuum operator outside shell",
            "current_status": "not derived",
            "beta_effect": "required for Schwarzschild beta=1",
        },
        {
            "branch_piece": "no exterior hair",
            "needed_result": "X, J_rel, V_def have no propagating exterior profile",
            "current_status": "not derived; constraint algebra open",
            "beta_effect": "prevents PPN deviations",
        },
        {
            "branch_piece": "Schwarzschild expansion",
            "needed_result": "g_00=-1+2U-2U^2+O(U^3)",
            "current_status": "conditional consequence only",
            "beta_effect": "beta=1",
        },
    ]


def coefficient_status_rows() -> list[dict[str, Any]]:
    previous = read_csv_rows(RUN_229 / "results" / "coefficient_status_after_229.csv")
    previous_by_residual = {row["residual"]: row for row in previous}
    updates = {
        "gamma_minus_1": (
            "unchanged_scalar_boundary_sufficient",
            "c_gamma=0 remains conditionally owned by scalar boundary symmetry",
            "derive parent boundary variable set and TF constraint",
        ),
        "Phi_minus_Psi": (
            "unchanged_scalar_boundary_sufficient",
            "c_slip=0 remains conditionally owned by tau_TF_AB=0",
            "derive parent boundary variable set and TF constraint",
        ),
        "G_eff_over_G_minus_1": (
            "mass_renormalization_gate",
            "allowed only as M -> M_eff monopole; no radial profile/hair allowed",
            "derive source normalization and exterior stress silence",
        ),
        "alpha_clock": (
            "unchanged_universal_metric_contract",
            "safe only under universal metric coupling",
            "derive parent matter/clock action",
        ),
        "epsilon_matter": (
            "unchanged_universal_metric_contract",
            "safe only with no direct memory composition coupling",
            "derive parent matter action",
        ),
        "beta_minus_1": (
            "conditional_vacuum_Einstein_consequence",
            "beta=1 follows if exact J_rel + exterior no-hair + Einstein vacuum branch are derived",
            "derive exterior branch; not promoted",
        ),
    }
    rows: list[dict[str, Any]] = []
    for residual, prior in previous_by_residual.items():
        status, result, next_needed = updates[residual]
        rows.append(
            {
                "residual": residual,
                "checkpoint_229_status": prior["checkpoint_229_status"],
                "checkpoint_230_status": status,
                "coefficient_after_230": result,
                "parent_derived": "no",
                "promotion_allowed": "false",
                "next_needed": next_needed,
            }
        )
    return rows


def obstruction_rows() -> list[dict[str, Any]]:
    return [
        {
            "obstruction": "Noether source identity",
            "why_it_blocks": "without it, q_loc cannot be rewritten as the relative current source",
            "current_status": "conditional X-route only",
            "next_attack": "derive from parent variation with retained stresses",
        },
        {
            "obstruction": "J_rel representative",
            "why_it_blocks": "closed but non-exact exterior memory current can source q_loc",
            "current_status": "exact route written, not selected",
            "next_attack": "derive memory-sector cohomology/projector",
        },
        {
            "obstruction": "X constraint algebra",
            "why_it_blocks": "X multiplier route must not introduce exterior hair",
            "current_status": "not computed",
            "next_attack": "specify parent symplectic structure or avoid X as independent field",
        },
        {
            "obstruction": "exterior metric operator",
            "why_it_blocks": "beta=1 needs vacuum Einstein operator, not only source silence",
            "current_status": "not parent-derived",
            "next_attack": "derive local EH limit from parent action",
        },
        {
            "obstruction": "boundary metric variation",
            "why_it_blocks": "scalar boundary stress must not leave radial exterior profile",
            "current_status": "symmetry sufficient, not full variation",
            "next_attack": "derive boundary stress as shell monopole/M_eff only",
        },
    ]


def claim_gate_rows(source_rows: list[dict[str, Any]], coefficient_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = sum(row["exists"] != "yes" for row in source_rows)
    beta_conditional = any(
        row["residual"] == "beta_minus_1"
        and row["checkpoint_230_status"] == "conditional_vacuum_Einstein_consequence"
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
            "gate": "exterior q_loc sufficient route written",
            "status": "pass",
            "evidence": "q_loc=-P_loc d_rel J_rel and exact J_rel would give q_loc=0",
            "claim_allowed": "theorem target only",
        },
        {
            "gate": "ordinary mass flux separated from J_rel",
            "status": "pass",
            "evidence": "J_rel restricted to memory/domain exchange current",
            "claim_allowed": "contract requirement",
        },
        {
            "gate": "beta conditional consequence identified",
            "status": "pass" if beta_conditional else "fail",
            "evidence": "Schwarzschild exterior gives beta=1 if exterior vacuum branch is derived",
            "claim_allowed": "conditional only",
        },
        {
            "gate": "J_rel exact representative parent-derived",
            "status": "fail",
            "evidence": "representative and projector remain open",
            "claim_allowed": "no q_loc promotion",
        },
        {
            "gate": "exterior vacuum Einstein branch parent-derived",
            "status": "fail",
            "evidence": "source identity, no-hair, and local EH operator remain open",
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
            "meaning": "The exterior beta route is now an exact sufficient contract: if the source identity holds, J_rel is exact/trivial in the projected local memory sector, ordinary mass flux is not J_rel, exterior memory stress vanishes except for M_eff, and the local metric operator is vacuum Einstein, then the exterior is Schwarzschild and beta=1. The contract is not parent-derived because the J_rel representative, X/no-hair algebra, and exterior Einstein-Hilbert limit remain open.",
            "main_gain": "beta is no longer a floating coefficient; it is tied to the exterior no-hair/vacuum-Einstein theorem",
            "main_failure": "the exact J_rel representative and exterior EH branch are still not derived",
            "next_target": "231-Jrel-cohomology-projector-or-local-EH-limit.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_230_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    exterior_rows = exterior_derivation_rows()
    jrel_rows = jrel_conditions_rows()
    beta_rows = beta_branch_rows()
    coefficient_rows = coefficient_status_rows()
    obstruction_matrix = obstruction_rows()
    gates = claim_gate_rows(source_rows, coefficient_rows)
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "exterior_derivation_steps.csv": (
            exterior_rows,
            ["step", "name", "statement", "math", "status", "remaining_gap"],
        ),
        "Jrel_representative_conditions.csv": (
            jrel_rows,
            ["condition", "requirement", "why_needed", "status"],
        ),
        "beta_branch_conditions.csv": (
            beta_rows,
            ["branch_piece", "needed_result", "current_status", "beta_effect"],
        ),
        "coefficient_status_after_230.csv": (
            coefficient_rows,
            [
                "residual",
                "checkpoint_229_status",
                "checkpoint_230_status",
                "coefficient_after_230",
                "parent_derived",
                "promotion_allowed",
                "next_needed",
            ],
        ),
        "obstruction_matrix.csv": (
            obstruction_matrix,
            ["obstruction", "why_it_blocks", "current_status", "next_attack"],
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
        "exterior_q_loc_sufficient_route_written": True,
        "ordinary_mass_flux_separated_from_Jrel": True,
        "Jrel_exact_representative_parent_derived": False,
        "exterior_vacuum_Einstein_branch_parent_derived": False,
        "beta_conditional_consequence_identified": True,
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
