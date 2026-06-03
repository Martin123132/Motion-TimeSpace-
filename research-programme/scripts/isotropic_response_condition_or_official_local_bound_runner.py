#!/usr/bin/env python3
"""Checkpoint 228: derive the local isotropic/no-slip response condition."""

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

CHECKPOINT_228_NAME = "isotropic-response-condition-or-official-local-bound-runner"
RUN_227 = RUNS_ROOT / "20260601-000044-local-PPN-coefficient-map-or-official-bound-manifest"

STATUS = "isotropic_no_slip_sufficient_condition_derived_parent_boundary_owner_open_no_PPN_promotion"
CLAIM_CEILING = "conditional_no_slip_sufficient_theorem_no_local_GR_or_PPN_promotion"
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
        (Path(__file__).resolve(), "checkpoint 228 derivation script"),
        (WORK_DIR / "221-Noether-source-identity-or-compact-PPN-closure-map.md", "source identity route and closure vector"),
        (WORK_DIR / "222-parent-X-sector-degree-count-and-boundary-action.md", "first-order X boundary contract"),
        (WORK_DIR / "223-X-constraint-algebra-and-Khat-Gamma-constitutive-owner.md", "composite P[Y] multiplier route"),
        (WORK_DIR / "224-defect-potential-Vdef-or-X-route-demotion.md", "V_def demotion and boundary closure status"),
        (WORK_DIR / "226-local-bound-preflight-and-baseline-comparison.md", "local residual pressure point ranking"),
        (WORK_DIR / "227-local-PPN-coefficient-map-or-official-bound-manifest.md", "common-mode coefficient map and official manifest"),
        (RUN_227 / "status.json", "checkpoint 227 machine status"),
        (RUN_227 / "results" / "coefficient_map_attempt.csv", "checkpoint 227 coefficient rows"),
        (RUN_227 / "results" / "official_local_bound_manifest.csv", "official-bound manifest, not applied here"),
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


def isotropic_derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "name": "weak_field_response_variables",
            "statement": "Use local weak-field Newtonian-gauge potentials Phi and Psi; define slip S=Phi-Psi and common mode C=(Phi+Psi)/2.",
            "math": "ds^2=-(1+2 Phi)dt^2+(1-2 Psi)delta_ij dx^i dx^j; S=Phi-Psi",
            "derived_status": "definition",
            "blocker": "",
        },
        {
            "step": 2,
            "name": "boundary_stress_split",
            "statement": "Any compact local boundary response decomposes into scalar trace plus trace-free anisotropic stress.",
            "math": "delta tau^i_j = delta p delta^i_j + pi^i_j, pi^i_i=0",
            "derived_status": "kinematic_decomposition",
            "blocker": "",
        },
        {
            "step": 3,
            "name": "isotropic_boundary_condition",
            "statement": "If the compact memory boundary action depends only on scalar shell invariants, its spatial variation is proportional to the induced shell metric.",
            "math": "delta S_boundary/delta gamma_ij proportional gamma^ij -> pi^i_j=0",
            "derived_status": "conditional_variational_theorem",
            "blocker": "the scalar-only parent boundary action is not derived from the full MTS parent",
        },
        {
            "step": 4,
            "name": "no_slip_constraint",
            "statement": "The trace-free spatial weak-field constraint sources slip only by trace-free anisotropic stress.",
            "math": "D^i_j(Phi-Psi)=8 pi G pi^i_j, D^i_j=partial^i partial_j - delta^i_j nabla^2/3",
            "derived_status": "weak_field_GR_limit_condition",
            "blocker": "assumes the local MTS branch reduces to the Einstein-like trace-free constraint",
        },
        {
            "step": 5,
            "name": "compact_shell_zero_mode",
            "statement": "With pi^i_j=0, the slip is a harmonic trace-free zero mode; regular compact-shell matching removes it up to gauge.",
            "math": "D^i_j S=0 plus no l>=2 boundary data -> S=constant/translation -> gauge-fixed S=0",
            "derived_status": "conditional_shell_result",
            "blocker": "needs explicit boundary primitive to prove no trace-free boundary data",
        },
        {
            "step": 6,
            "name": "common_mode_result",
            "statement": "Therefore the local memory leakage may change the common Newtonian potential but not gamma/slip at leading order.",
            "math": "delta Phi=delta Psi=delta C; delta gamma and delta(Phi-Psi) vanish at O(epsilon_J)",
            "derived_status": "sufficient_condition_derived",
            "blocker": "amplitude delta C and beta remain unowned",
        },
    ]


def boundary_stress_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition": "scalar_shell_invariants_only",
            "required_form": "S_boundary = integral sqrt(|gamma|) F(N_D, K_shell, R_shell, n dot flow, scalar memory)",
            "what_it_forbids": "explicit preferred tangential vector/tensor couplings on compact shell",
            "local_effect": "delta tau^i_j has no trace-free spatial component",
            "status": "sufficient_not_parent_derived",
        },
        {
            "condition": "no_tangential_memory_shear",
            "required_form": "projected memory current has only normal/scalar components on compact shell",
            "what_it_forbids": "J_rel^A with l>=2 tangential shear on shell",
            "local_effect": "no l>=2 slip boundary data",
            "status": "sufficient_not_parent_derived",
        },
        {
            "condition": "universal_metric_coupling",
            "required_form": "matter and clocks couple through g_mu_nu/coframe only",
            "what_it_forbids": "direct composition or clock coupling to X, J_rel, or V_def",
            "local_effect": "WEP/redshift residuals stay contract-zero at leading order",
            "status": "contract_not_parent_derived",
        },
        {
            "condition": "Einstein_like_TF_constraint",
            "required_form": "local weak-field trace-free spatial equation has GR form with effective anisotropic stress source",
            "what_it_forbids": "extra unsuppressed trace-free operator in local branch",
            "local_effect": "slip is controlled only by trace-free boundary stress",
            "status": "local_GR_limit_theorem_target",
        },
        {
            "condition": "regular_compact_matching",
            "required_form": "no incoming l>=2 homogeneous slip mode on compact collar; asymptotic/gauge modes fixed",
            "what_it_forbids": "hiding slip in boundary homogeneous modes",
            "local_effect": "Phi-Psi=0 rather than only source-free",
            "status": "sufficient_not_parent_derived",
        },
    ]


def harmonic_mode_rows() -> list[dict[str, Any]]:
    return [
        {
            "mode": "l=0",
            "slip_solution_role": "constant",
            "removal_condition": "absorbed by equal potential zero/gauge choice",
            "status": "safe_if_gauge_fixed",
        },
        {
            "mode": "l=1",
            "slip_solution_role": "translation/center-of-mass homogeneous mode",
            "removal_condition": "compact-shell frame and asymptotic matching fix center-of-mass mode",
            "status": "safe_if_frame_fixed",
        },
        {
            "mode": "l>=2",
            "slip_solution_role": "physical quadrupole-and-higher trace-free boundary slip",
            "removal_condition": "requires zero trace-free boundary stress and no tangential memory shear",
            "status": "hard_condition",
        },
    ]


def coefficient_status_rows() -> list[dict[str, Any]]:
    prior_rows = read_csv_rows(RUN_227 / "results" / "coefficient_map_attempt.csv")
    prior_by_residual = {row["residual"]: row for row in prior_rows}
    updates = {
        "gamma_minus_1": (
            "derived_as_sufficient_condition",
            "c_gamma=0 if scalar-shell boundary action plus Einstein-like trace-free constraint plus no l>=2 shell mode",
            "not a parent theorem because scalar boundary action and local GR limit are still contracts",
        ),
        "Phi_minus_Psi": (
            "derived_as_sufficient_condition",
            "c_slip=0 under the same no-trace-free-stress compact-shell conditions",
            "not a parent theorem because trace-free boundary primitive is not derived",
        ),
        "G_eff_over_G_minus_1": (
            "still_proxy_bound",
            "common-mode amplitude deltaC can renormalize the Newtonian source; |c_G| remains proxy only",
            "needs local source-renormalization equation",
        ),
        "alpha_clock": (
            "unchanged_contract_zero",
            "c_clock=0 only if universal metric clock coupling survives parent completion",
            "not derived from parent matter/clock action",
        ),
        "epsilon_matter": (
            "unchanged_contract_zero",
            "c_matter=0 only if no direct composition coupling to memory/X/boundary sector",
            "not derived from parent matter action",
        ),
        "beta_minus_1": (
            "open_second_order",
            "no-slip first-order result does not set beta; beta needs O(U^2) temporal response",
            "derive second-order weak-field temporal equation",
        ),
    }
    rows: list[dict[str, Any]] = []
    for residual, prior in prior_by_residual.items():
        status, result, next_needed = updates[residual]
        rows.append(
            {
                "residual": residual,
                "checkpoint_227_status": prior["status"],
                "checkpoint_228_status": status,
                "coefficient_after_228": result,
                "parent_derived": "no",
                "promotion_allowed": "false",
                "next_needed": next_needed,
            }
        )
    return rows


def official_bound_stance_rows() -> list[dict[str, Any]]:
    manifest_rows = read_csv_rows(RUN_227 / "results" / "official_local_bound_manifest.csv")
    rows: list[dict[str, Any]] = []
    for row in manifest_rows:
        residual = row["residual_channel"]
        if residual == "gamma_minus_1":
            readiness = "more_ready_but_still_nonclaiming"
            reason = "gamma coefficient now has a sufficient no-slip theorem target, but parent ownership is open"
        elif residual == "beta_minus_1":
            readiness = "not_ready"
            reason = "beta remains second-order open"
        elif residual in {"alpha_clock", "epsilon_matter"}:
            readiness = "contract_ready_not_claimable"
            reason = "universal coupling is still a contract, not parent-derived"
        else:
            readiness = "not_ready"
            reason = "residual channel not updated by checkpoint 228"
        rows.append(
            {
                "residual_channel": residual,
                "observable": row["observable"],
                "source_label": row["source_label"],
                "bound_or_result": row["bound_or_result"],
                "checkpoint_228_readiness": readiness,
                "reason": reason,
                "applied_as_pass_fail": "false",
            }
        )
    return rows


def claim_gate_rows(
    source_rows: list[dict[str, Any]],
    coefficient_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = sum(row["exists"] != "yes" for row in source_rows)
    sufficient_conditions = sum(row["checkpoint_228_status"] == "derived_as_sufficient_condition" for row in coefficient_rows)
    open_beta = any(row["residual"] == "beta_minus_1" and row["checkpoint_228_status"] == "open_second_order" for row in coefficient_rows)
    return [
        {
            "gate": "all cited local sources exist",
            "status": "pass" if missing_sources == 0 else "fail",
            "evidence": f"missing={missing_sources}",
            "claim_allowed": "internal checkpoint only",
        },
        {
            "gate": "isotropic/no-slip sufficient condition derived",
            "status": "pass" if sufficient_conditions >= 2 else "fail",
            "evidence": f"sufficient_condition_coefficients={sufficient_conditions}",
            "claim_allowed": "theorem target, not parent promotion",
        },
        {
            "gate": "scalar boundary owner parent-derived",
            "status": "fail",
            "evidence": "boundary action scalar-only form remains a contract",
            "claim_allowed": "no local-GR claim",
        },
        {
            "gate": "beta second-order response derived",
            "status": "fail" if open_beta else "pass",
            "evidence": "beta remains open at O(U^2)",
            "claim_allowed": "no full PPN claim",
        },
        {
            "gate": "official bounds applied as pass/fail",
            "status": "fail",
            "evidence": "official manifest remains non-claiming until parent assumptions are owned",
            "claim_allowed": "no observational pass/fail",
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
            "meaning": "The common-mode/no-slip route is no longer just a wish: it is a sufficient local theorem if compact-shell memory leakage has scalar/isotropic boundary stress, no tangential l>=2 memory shear, regular shell matching, universal metric coupling, and an Einstein-like trace-free weak-field constraint. Under those conditions gamma/slip vanish at leading order while a common Newtonian amplitude can remain. The parent theory still has to derive the scalar boundary owner, the local GR trace-free constraint, and the second-order beta response.",
            "main_gain": "gamma/slip assumptions are converted into exact local boundary conditions",
            "main_failure": "the boundary scalar owner and beta O(U^2) response are not parent-derived",
            "next_target": "229-second-order-beta-or-boundary-scalar-owner.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_228_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    derivation_rows = isotropic_derivation_rows()
    boundary_rows = boundary_stress_contract_rows()
    harmonic_rows = harmonic_mode_rows()
    coefficient_rows = coefficient_status_rows()
    official_rows = official_bound_stance_rows()
    gates = claim_gate_rows(source_rows, coefficient_rows)
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "isotropic_derivation_steps.csv": (
            derivation_rows,
            ["step", "name", "statement", "math", "derived_status", "blocker"],
        ),
        "boundary_stress_contract.csv": (
            boundary_rows,
            ["condition", "required_form", "what_it_forbids", "local_effect", "status"],
        ),
        "harmonic_shell_modes.csv": (
            harmonic_rows,
            ["mode", "slip_solution_role", "removal_condition", "status"],
        ),
        "coefficient_status_after_228.csv": (
            coefficient_rows,
            [
                "residual",
                "checkpoint_227_status",
                "checkpoint_228_status",
                "coefficient_after_228",
                "parent_derived",
                "promotion_allowed",
                "next_needed",
            ],
        ),
        "official_bound_nonclaiming_stance.csv": (
            official_rows,
            [
                "residual_channel",
                "observable",
                "source_label",
                "bound_or_result",
                "checkpoint_228_readiness",
                "reason",
                "applied_as_pass_fail",
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
    sufficient_conditions = sum(row["checkpoint_228_status"] == "derived_as_sufficient_condition" for row in coefficient_rows)
    status_payload = {
        "status": decision[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(files.keys()),
        "missing_sources": missing_sources,
        "isotropic_no_slip_sufficient_condition_derived": sufficient_conditions >= 2,
        "sufficient_condition_coefficients": sufficient_conditions,
        "parent_boundary_owner_derived": False,
        "local_GR_trace_free_constraint_parent_derived": False,
        "beta_second_order_derived": False,
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
