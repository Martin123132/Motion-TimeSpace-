#!/usr/bin/env python3
"""Checkpoint 223: X constraint algebra and Khat/Gamma constitutive ownership."""

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

CHECKPOINT_223_NAME = "X-constraint-algebra-and-Khat-Gamma-constitutive-owner"
CHECKPOINT_222_RUN = RUNS_ROOT / "20260601-000039-parent-X-sector-degree-count-and-boundary-action"

STATUS = "X_multiplier_zero_dof_route_conditional_P_constitutive_owner_missing_no_local_GR_promotion"
CLAIM_CEILING = "X_constraint_algebra_partial_constitutive_owner_missing_no_PPN_promotion"
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
        (Path(__file__).resolve(), "checkpoint 223 constraint algebra script"),
        (WORK_DIR / "177-parent-action-perturbation-local-GR-contract.md", "parent action/local-GR contract"),
        (WORK_DIR / "207-domain-projector-action-and-Bianchi-identity.md", "Bianchi/projector stress accounting"),
        (WORK_DIR / "210-GK-alphaK-parent-invariant-or-fixed-closure.md", "G_K candidate invariant and missing metric"),
        (WORK_DIR / "211-GK-parent-metric-Ward-identity-attempt.md", "partial Ward/norm owner status"),
        (WORK_DIR / "222-parent-X-sector-degree-count-and-boundary-action.md", "first-order X route checkpoint"),
        (CHECKPOINT_222_RUN / "status.json", "checkpoint 222 machine status"),
        (CHECKPOINT_222_RUN / "results" / "degree_count_audit.csv", "checkpoint 222 degree-count audit"),
        (CHECKPOINT_222_RUN / "results" / "local_PPN_hair_risk_map.csv", "checkpoint 222 PPN hair risk map"),
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


def constraint_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "R1_independent_first_order_P",
            "schematic_action": "S=int sqrt(-g)[P^{mu nu} nabla_mu X_nu + J_eff^nu X_nu]",
            "X_degree_result": "no_regular_X_kinetic_but_not_complete",
            "P_status": "free_tensor",
            "status": "rejected_as_final",
            "reason": "variation of P imposes nabla X conditions, while transverse/constitutive parts of P are not parent-owned",
        },
        {
            "route": "R2_invertible_H_of_P",
            "schematic_action": "S=int sqrt(-g)[P nabla X - H(P,Y) + J_eff X]",
            "X_degree_result": "danger",
            "P_status": "algebraic_but_invertible",
            "status": "rejected",
            "reason": "integrating out P generically reintroduces dot(X)^2 or spatial-gradient X stiffness",
        },
        {
            "route": "R3_composite_P_of_parent_fields",
            "schematic_action": "S=int sqrt(-g)[P[Y]^{mu nu} nabla_mu X_nu + J_eff[Y]^nu X_nu]+S_boundary",
            "X_degree_result": "zero_local_X_dof_conditional",
            "P_status": "owned_if_Y_and_defect_potential_derived",
            "status": "best_live_route",
            "reason": "after integration by parts X is a pure multiplier imposing div P[Y]=J_eff[Y]",
        },
        {
            "route": "R4_gauge_topological_X",
            "schematic_action": "S=int P[Y] dX plus gauge symmetry X -> X + exact/gauge",
            "X_degree_result": "zero_if_gauge_real",
            "P_status": "needs_topological_owner",
            "status": "live_subroute",
            "reason": "a genuine gauge symmetry could make X lapse/shift-like, but the symmetry is not derived",
        },
        {
            "route": "R5_direct_matter_P",
            "schematic_action": "P^{mu nu}=functional(T_matter^{mu nu})",
            "X_degree_result": "possibly_zero",
            "P_status": "matter_coupled",
            "status": "rejected",
            "reason": "direct matter dependence risks WEP/clock/composition coupling and is not the memory-sector source identity",
        },
    ]


def canonical_count_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "independent_first_order_P_per_X_component",
            "canonical_variables": "X, pi_X, P0, pi_P0, Pi, pi_Pi",
            "primary_constraints": "pi_X - sqrt(h) P0; pi_P0; pi_Pi",
            "secondary_constraints": "D_i X or modified P-equations; div P - J from delta X",
            "local_X_dof_readout": "not_clean",
            "why": "rank-zero Hessian avoids regular X waves, but independent P leaves unresolved multiplier/constitutive freedom",
            "promotion_status": "fail",
        },
        {
            "candidate": "composite_P_multiplier_X_per_component",
            "canonical_variables": "X, pi_X plus parent Y variables",
            "primary_constraints": "pi_X approx 0",
            "secondary_constraints": "C_X= -nabla_mu P[Y]^{mu nu}+J_eff[Y]^nu approx 0",
            "local_X_dof_readout": "zero_conditional",
            "why": "X has no kinetic term and enforces C_X as a constraint; no X phase-space pair remains if the constraint algebra closes",
            "promotion_status": "conditional_pass",
        },
        {
            "candidate": "composite_P_with_boundary_pair",
            "canonical_variables": "X, pi_X; boundary B_X/A_rel variables; parent Y variables",
            "primary_constraints": "bulk pi_X approx 0 plus boundary momenta constraints",
            "secondary_constraints": "bulk C_X approx 0 and B_X=n_mu P[Y]^{mu nu}",
            "local_X_dof_readout": "zero_conditional_boundary_open",
            "why": "bulk X can be a multiplier, but boundary primitive exactness and boundary stress remain unproven",
            "promotion_status": "conditional_boundary_fail",
        },
    ]


def constraint_algebra_tests() -> list[dict[str, Any]]:
    return [
        {
            "test": "A1_primary_X_momentum",
            "required_result": "pi_X_nu approx 0 for composite P[Y] route",
            "current_result": "pass_conditional",
            "evidence": "integrated-by-parts X action has no dot(X)",
            "remaining_gap": "depends on P being composite, not independent canonical P",
        },
        {
            "test": "A2_secondary_source_identity",
            "required_result": "dot(pi_X_nu)=0 gives C_nu=-nabla_mu P[Y]^{mu nu}+J_eff[Y]^nu approx 0",
            "current_result": "pass_conditional",
            "evidence": "same identity as checkpoint 221/222",
            "remaining_gap": "C_nu must be compatible with parent Y equations",
        },
        {
            "test": "A3_constraint_closure",
            "required_result": "{C_nu(x),C_rho(y)} closes on existing parent constraints or vanishes weakly",
            "current_result": "not_derived",
            "evidence": "no explicit symplectic form for parent Y sector",
            "remaining_gap": "main algebra blocker",
        },
        {
            "test": "A4_no_X_matter_coupling",
            "required_result": "delta L_matter/dX=0 and matter sees only g/coframe",
            "current_result": "contract",
            "evidence": "required by PPN/WEP guardrail",
            "remaining_gap": "universal matter coupling still not parent-derived",
        },
        {
            "test": "A5_boundary_constraint_closure",
            "required_result": "boundary equation B_X=n_mu P[Y] and exact/pure-gauge A_rel close with bulk C_nu",
            "current_result": "not_derived",
            "evidence": "checkpoint 222 boundary primitive not selected",
            "remaining_gap": "boundary representative selection",
        },
        {
            "test": "A6_metric_stress_consistency",
            "required_result": "delta_g of X constraint sector retained in total stress and Bianchi identity",
            "current_result": "contract",
            "evidence": "checkpoint 207 stress accounting",
            "remaining_gap": "explicit T_X/T_boundary formula not derived",
        },
    ]


def constitutive_owner_rows() -> list[dict[str, Any]]:
    return [
        {
            "owner_route": "free_P_tensor",
            "definition": "P^{mu nu} is declared as Khat^{mu nu}-Gamma_eff g^{mu nu}",
            "trace_split": "by_definition",
            "status": "rejected",
            "blocker": "free P makes the source identity a named tensor equation rather than a parent result",
        },
        {
            "owner_route": "defect_potential_Hessian",
            "definition": "P^{mu nu}=partial V_def(Y,Z)/partial Z_{mu nu}",
            "trace_split": "Gamma_eff=-1/4 trace(P), Khat^{mu nu}=P^{mu nu}+Gamma_eff g^{mu nu}",
            "status": "best_live_contract",
            "blocker": "V_def and response deformation Z_{mu nu} are not derived",
        },
        {
            "owner_route": "GK_norm_derivative",
            "definition": "P derived from variation of ||Xi_D||_M^2 or related coherence-defect norm",
            "trace_split": "possible_if_trace_and_traceless_blocks_orthogonal",
            "status": "partial_route",
            "blocker": "M_AB and cross terms remain closure from checkpoints 210-211",
        },
        {
            "owner_route": "ADM_flow_block",
            "definition": "flow part of P from ADM/DeWitt norm on expansion/shear/vorticity defect",
            "trace_split": "partial_geometric",
            "status": "partial_pass",
            "blocker": "only the kinematic block is partially owned; Weyl/Q/J_rel blocks are missing",
        },
        {
            "owner_route": "relative_current_Hodge_norm",
            "definition": "J_rel contribution from Hodge norm of relative pair (j3,b2)",
            "trace_split": "boundary_sector_only",
            "status": "open",
            "blocker": "local representative and boundary primitive still not selected",
        },
        {
            "owner_route": "matter_stress_direct",
            "definition": "P built directly from T_matter",
            "trace_split": "matter_trace",
            "status": "rejected",
            "blocker": "risks direct matter/composition coupling and collapses memory-sector distinction",
        },
    ]


def PPN_margin_rows() -> list[dict[str, Any]]:
    risk_path = CHECKPOINT_222_RUN / "results" / "local_PPN_hair_risk_map.csv"
    with risk_path.open("r", encoding="utf-8-sig", newline="") as handle:
        source_rows = list(csv.DictReader(handle))
    rows: list[dict[str, Any]] = []
    for source in source_rows:
        margin = float(source["max_order_unity_response_coefficient_proxy"])
        rows.append(
            {
                "case": source["case"],
                "epsilon_fraction_of_gate": float(source["epsilon_fraction_of_gate"]),
                "max_response_coefficient_proxy": margin,
                "risk_readout": source["risk_readout"],
                "constraint_algebra_implication": (
                    "requires especially clean zero-X-hair proof"
                    if margin < 1.2
                    else "order-unity coefficients may fit proxy but still need derivation"
                ),
            }
        )
    return rows


def claim_gate_rows(
    source_rows: list[dict[str, Any]],
    algebra_rows: list[dict[str, Any]],
    owner_rows: list[dict[str, Any]],
    margin_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = sum(row["exists"] != "yes" for row in source_rows)
    algebra_blockers = sum(row["current_result"] == "not_derived" for row in algebra_rows)
    best_owner_count = sum(row["status"] == "best_live_contract" for row in owner_rows)
    tight_cases = sum(row["risk_readout"] == "tight" for row in margin_rows)
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing_sources == 0 else "fail",
            "evidence": f"missing={missing_sources}",
            "claim_allowed": "internal checkpoint only",
        },
        {
            "gate": "independent free P rejected",
            "status": "pass",
            "evidence": "free P leaves unowned tensor freedom",
            "claim_allowed": "guardrail",
        },
        {
            "gate": "composite P multiplier route gives zero X dof",
            "status": "conditional_pass",
            "evidence": "pi_X=0 and C_X constraint remove X if algebra closes",
            "claim_allowed": "conditional algebra route",
        },
        {
            "gate": "constraint algebra closed",
            "status": "fail" if algebra_blockers else "conditional_pass",
            "evidence": f"algebra_blockers={algebra_blockers}",
            "claim_allowed": "no local-GR promotion",
        },
        {
            "gate": "P constitutive owner identified",
            "status": "conditional_pass" if best_owner_count == 1 else "fail",
            "evidence": f"best_owner_contracts={best_owner_count}; V_def not derived",
            "claim_allowed": "contract only",
        },
        {
            "gate": "P constitutive owner derived",
            "status": "fail",
            "evidence": "V_def/Z_mu_nu, M_AB, and cross terms are not parent-derived",
            "claim_allowed": "no theorem",
        },
        {
            "gate": "trace/traceless split fixes Gamma and Khat",
            "status": "conditional_pass",
            "evidence": "works if Khat is defined traceless and Gamma=-trace(P)/4",
            "claim_allowed": "definition contract",
        },
        {
            "gate": "PPN margin survives X route",
            "status": "conditional_pass",
            "evidence": f"tight_cases={tight_cases}; proxy only",
            "claim_allowed": "risk map only",
        },
        {
            "gate": "local GR or PPN promoted",
            "status": "fail",
            "evidence": CLAIM_CEILING,
            "claim_allowed": "no",
        },
    ]


def decision_rows(margin_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    tightest = min(margin_rows, key=lambda row: float(row["max_response_coefficient_proxy"]))
    return [
        {
            "decision": STATUS,
            "meaning": "The zero-X-hair route is viable only if X is a pure multiplier imposing C_nu=-nabla_mu P[Y]^{mu nu}+J_eff[Y]^nu=0 with P composite in parent fields. This can remove local X degrees conditionally. However, the constraint algebra is not closed because the parent Y symplectic structure is not specified, and P=Khat-Gamma g is not derived from a defect potential.",
            "main_gain": "independent free-P and invertible-H routes are rejected; composite P[Y] multiplier route isolates the clean no-hair path",
            "main_failure": "constraint closure and defect-potential constitutive owner are missing",
            "tightest_ppn_proxy_case": tightest["case"],
            "tightest_response_coefficient_proxy": tightest["max_response_coefficient_proxy"],
            "next_target": "224-defect-potential-Vdef-or-X-route-demotion.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_223_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    route_rows = constraint_route_rows()
    canonical_rows = canonical_count_rows()
    algebra_rows = constraint_algebra_tests()
    owner_rows = constitutive_owner_rows()
    margin_rows = PPN_margin_rows()
    gates = claim_gate_rows(source_rows, algebra_rows, owner_rows, margin_rows)
    decision = decision_rows(margin_rows)

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "constraint_route_ledger.csv": (
            route_rows,
            ["route", "schematic_action", "X_degree_result", "P_status", "status", "reason"],
        ),
        "canonical_count_table.csv": (
            canonical_rows,
            [
                "candidate",
                "canonical_variables",
                "primary_constraints",
                "secondary_constraints",
                "local_X_dof_readout",
                "why",
                "promotion_status",
            ],
        ),
        "constraint_algebra_tests.csv": (
            algebra_rows,
            ["test", "required_result", "current_result", "evidence", "remaining_gap"],
        ),
        "Khat_Gamma_constitutive_owner_tests.csv": (
            owner_rows,
            ["owner_route", "definition", "trace_split", "status", "blocker"],
        ),
        "PPN_margin_carryforward.csv": (
            margin_rows,
            [
                "case",
                "epsilon_fraction_of_gate",
                "max_response_coefficient_proxy",
                "risk_readout",
                "constraint_algebra_implication",
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
                "tightest_ppn_proxy_case",
                "tightest_response_coefficient_proxy",
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
    algebra_blockers = sum(row["current_result"] == "not_derived" for row in algebra_rows)
    tightest = min(margin_rows, key=lambda row: float(row["max_response_coefficient_proxy"]))
    status_payload = {
        "status": decision[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(files.keys()),
        "missing_sources": missing_sources,
        "independent_free_P_rejected": True,
        "invertible_H_of_P_rejected": True,
        "composite_P_multiplier_route_written": True,
        "zero_local_X_dof_conditional": True,
        "constraint_algebra_closed": False,
        "constraint_algebra_blockers": algebra_blockers,
        "P_constitutive_owner_contract": "defect_potential_Hessian",
        "P_constitutive_owner_derived": False,
        "trace_traceless_split_contract": "Gamma_eff=-trace(P)/4; Khat=P+Gamma_eff*g",
        "tightest_ppn_proxy_case": tightest["case"],
        "tightest_response_coefficient_proxy": float(tightest["max_response_coefficient_proxy"]),
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
    payload = run(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
