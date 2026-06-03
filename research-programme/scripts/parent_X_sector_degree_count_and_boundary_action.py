#!/usr/bin/env python3
"""Checkpoint 222: parent X-sector degree count and boundary action audit."""

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

CHECKPOINT_222_NAME = "parent-X-sector-degree-count-and-boundary-action"
CHECKPOINT_221_RUN = RUNS_ROOT / "20260601-000038-Noether-source-identity-or-compact-PPN-closure-map"

STATUS = "parent_X_first_order_constraint_route_conditional_degree_count_not_derived_boundary_contract_written"
CLAIM_CEILING = "X_sector_constraint_contract_no_local_GR_or_PPN_promotion"
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
        (Path(__file__).resolve(), "checkpoint 222 X-sector degree-count script"),
        (WORK_DIR / "19-constrained-parent-action-skeleton.md", "early constrained parent action skeleton"),
        (WORK_DIR / "72-relative-current-action-owner-attempt.md", "relative-current action and BF route"),
        (WORK_DIR / "207-domain-projector-action-and-Bianchi-identity.md", "Bianchi/projector stress accounting"),
        (WORK_DIR / "220-Jrel-local-trivial-representative-or-closure-bound.md", "local J_rel exactness checkpoint"),
        (WORK_DIR / "221-Noether-source-identity-or-compact-PPN-closure-map.md", "source identity route and PPN closure map"),
        (CHECKPOINT_221_RUN / "status.json", "checkpoint 221 machine status"),
        (CHECKPOINT_221_RUN / "results" / "parent_variation_contract.csv", "checkpoint 221 parent variation contract"),
        (CHECKPOINT_221_RUN / "results" / "compact_PPN_closure_vector.csv", "checkpoint 221 PPN closure vector"),
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


def X_sector_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "regular_kinetic_vector_X",
            "schematic_action": "L_X ~ -1/4 F_X^2 - 1/2 m_X^2 X^2 + X_nu J^nu",
            "source_identity": "modified_or_not_exact",
            "kinetic_hessian_rank": 3,
            "local_hair_risk": "high",
            "boundary_ownership": "not_enough",
            "status": "rejected",
            "reason": "it introduces Proca/vector modes and turns the local fix into a new PPN problem",
        },
        {
            "candidate": "massive_algebraic_auxiliary_X",
            "schematic_action": "L_X ~ -1/2 m_X^2 X^2 + X_nu J^nu",
            "source_identity": "fails",
            "kinetic_hessian_rank": 0,
            "local_hair_risk": "screened_but_identity_lost",
            "boundary_ownership": "none",
            "status": "rejected",
            "reason": "algebraic X gives X=J/m_X^2 rather than the divergence identity",
        },
        {
            "candidate": "pure_first_order_constraint_X",
            "schematic_action": "L_X ~ P^{mu nu} nabla_mu X_nu + J^nu X_nu + S_boundary",
            "source_identity": "yes_conditional",
            "kinetic_hessian_rank": 0,
            "local_hair_risk": "low_if_constraint_algebra_closes",
            "boundary_ownership": "requires_boundary_momentum",
            "status": "best_live_route",
            "reason": "variation of X gives the desired divergence identity without quadratic X kinetics",
        },
        {
            "candidate": "gauge_Stueckelberg_topological_X",
            "schematic_action": "L_X ~ P^{mu nu} nabla_mu X_nu with X-shift/diffeomorphism gauge redundancy",
            "source_identity": "yes_conditional",
            "kinetic_hessian_rank": 0,
            "local_hair_risk": "low_if_gauge_symmetry_real",
            "boundary_ownership": "requires_gauge_compatible_boundary_pair",
            "status": "live_subroute",
            "reason": "first-class gauge constraints can remove X degrees, but the gauge symmetry is not derived",
        },
        {
            "candidate": "BF_boundary_polarized_X",
            "schematic_action": "L_X ~ B wedge F[A] + boundary polarization tied to X and J_rel",
            "source_identity": "partial",
            "kinetic_hessian_rank": 0,
            "local_hair_risk": "low_topological",
            "boundary_ownership": "promising_but_selector_missing",
            "status": "support_route_only",
            "reason": "BF flatness helps no-hair bookkeeping but still does not select the physical representative",
        },
        {
            "candidate": "domain_label_reuse_XA",
            "schematic_action": "reuse domain labels X^A as X^nu source identity carrier",
            "source_identity": "insufficient",
            "kinetic_hessian_rank": 0,
            "local_hair_risk": "medium_confusion_risk",
            "boundary_ownership": "unclear",
            "status": "rejected_as_written",
            "reason": "domain labels can help selection but do not by themselves supply the vector source identity",
        },
    ]


def first_order_variation_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "statement": "Define P^{mu nu}=Khat^{mu nu}-Gamma_eff g^{mu nu}.",
            "result": "single conjugate momentum candidate",
            "open_issue": "P must be built from parent fields, not free-fitted",
        },
        {
            "step": 2,
            "statement": "Use S_X=integral sqrt(-g)[P^{mu nu} nabla_mu X_nu + J_eff^nu X_nu] + S_boundary, with J_eff^nu=S_L^nu+d_rel J_rel^nu.",
            "result": "first_order_bulk_action_template",
            "open_issue": "constitutive owner of P and J_eff still missing",
        },
        {
            "step": 3,
            "statement": "Vary X_nu and integrate by parts.",
            "result": "-nabla_mu P^{mu nu}+J_eff^nu=0",
            "open_issue": "boundary term must be owned",
        },
        {
            "step": 4,
            "statement": "Substitute P^{mu nu}=Khat^{mu nu}-Gamma_eff g^{mu nu}.",
            "result": "nabla_mu Khat^{mu nu}-nabla^nu Gamma_eff=S_L^nu+d_rel J_rel^nu",
            "open_issue": "source identity derived only inside this first-order template",
        },
        {
            "step": 5,
            "statement": "Because L_X is linear in dot(X), the Hessian with respect to dot(X) has rank zero.",
            "result": "no regular kinetic vector mode in the template",
            "open_issue": "zero Hessian is necessary but not sufficient; constraint algebra must close",
        },
        {
            "step": 6,
            "statement": "Require X to be pure constraint/gauge/auxiliary and forbid X kinetic, Proca, direct matter, and clock-composition couplings.",
            "result": "local PPN hair can be avoided conditionally",
            "open_issue": "the parent theory has not yet proven the required gauge/constraint structure",
        },
    ]


def degree_count_rows() -> list[dict[str, Any]]:
    return [
        {
            "test": "regular_kinetic_hessian_rank",
            "requirement": "rank d^2 L/d dotX d dotX = 0 for the local branch",
            "best_route_status": "pass_conditional",
            "evidence": "pure_first_order_constraint_X has no dotX squared term",
            "remaining_gap": "rank-zero degeneracy does not by itself prove zero propagating degrees",
        },
        {
            "test": "primary_constraints",
            "requirement": "pi_X_nu - sqrt(h) P^{0 nu} approx 0 gives four primary constraints",
            "best_route_status": "conditional_pass",
            "evidence": "first-order action gives momenta algebraically",
            "remaining_gap": "Poisson bracket class not computed from a complete Hamiltonian",
        },
        {
            "test": "secondary_source_constraints",
            "requirement": "preservation of primary constraints or delta_X gives four source-identity constraints",
            "best_route_status": "conditional_pass",
            "evidence": "Euler equation is the desired source identity",
            "remaining_gap": "constraint closure and boundary compatibility not proven",
        },
        {
            "test": "first_class_or_second_class_closure",
            "requirement": "constraints remove all X phase-space variables or make X pure gauge",
            "best_route_status": "not_derived",
            "evidence": "no complete symplectic form/Dirac matrix yet",
            "remaining_gap": "this is the main degree-count blocker",
        },
        {
            "test": "no_direct_matter_clock_coupling",
            "requirement": "delta L_matter/dX = 0 in local weak-field systems",
            "best_route_status": "contract",
            "evidence": "forbidden by local PPN/WEP guardrail",
            "remaining_gap": "universal matter coupling still a parent-action postulate",
        },
        {
            "test": "no_boundary_wall_stress_hidden",
            "requirement": "boundary stress from S_boundary is retained in metric variation",
            "best_route_status": "contract",
            "evidence": "checkpoint 207 Bianchi accounting demands T_boundary",
            "remaining_gap": "explicit boundary stress tensor not derived",
        },
    ]


def boundary_action_rows() -> list[dict[str, Any]]:
    return [
        {
            "boundary_clause": "B1_bulk_boundary_term",
            "expression": "delta S_X|boundary = integral_boundary sqrt(|gamma|) n_mu P^{mu nu} delta X_nu",
            "status": "unavoidable",
            "risk": "dropping it hides local force exchange",
        },
        {
            "boundary_clause": "B2_Dirichlet_X",
            "expression": "fix delta X_nu|boundary=0",
            "status": "conditional_not_enough",
            "risk": "boundary condition may be chosen only to silence local systems",
        },
        {
            "boundary_clause": "B3_boundary_momentum_pair",
            "expression": "add S_boundary = - integral_boundary sqrt(|gamma|) B_X^nu X_nu + S_rel[B_X,A_rel,b_2]",
            "status": "best_live_contract",
            "risk": "B_X/A_rel relation and stress tensor not derived",
        },
        {
            "boundary_clause": "B4_boundary_Euler_match",
            "expression": "delta_X boundary equation gives B_X^nu = n_mu P^{mu nu}",
            "status": "conditional_pass",
            "risk": "only works if B_X is a real relative-boundary momentum",
        },
        {
            "boundary_clause": "B5_compact_shell_exact_primitive",
            "expression": "A_rel exact or pure gauge on compact shell, so B_X carries no projected local memory flux",
            "status": "not_derived",
            "risk": "closed non-exact relative memory charge survives",
        },
        {
            "boundary_clause": "B6_metric_variation",
            "expression": "delta_g S_boundary contributes T_boundary and must be retained",
            "status": "contract",
            "risk": "fake Bianchi conservation if omitted",
        },
    ]


def PPN_risk_rows() -> list[dict[str, Any]]:
    ppn_rows = read_csv_rows(CHECKPOINT_221_RUN / "results" / "compact_PPN_closure_vector.csv")
    cases: dict[str, dict[str, float | str]] = {}
    for row in ppn_rows:
        if row["use_in_gate"] != "yes":
            continue
        case = row["case"]
        if case not in cases:
            cases[case] = {
                "q_like_gate": float(row["q_like_gate"]),
                "base_q_proxy": float(row["base_q_proxy"]),
                "max_allowed_epsilon_J": float(row["max_allowed_epsilon_J"]),
                "worst_nonq_coefficient_margin": float("inf"),
            }
        if row["residual_component"] != "q_loc_source":
            margin = float(row["max_unit_coefficient_before_q_gate_proxy"])
            cases[case]["worst_nonq_coefficient_margin"] = min(
                float(cases[case]["worst_nonq_coefficient_margin"]),
                margin,
            )
    rows: list[dict[str, Any]] = []
    for case, data in cases.items():
        epsilon = float(data["max_allowed_epsilon_J"])
        gate = float(data["q_like_gate"])
        base = float(data["base_q_proxy"])
        margin = float(data["worst_nonq_coefficient_margin"])
        rows.append(
            {
                "case": case,
                "q_like_gate": gate,
                "base_q_proxy": base,
                "max_allowed_epsilon_J": epsilon,
                "epsilon_fraction_of_gate": epsilon / gate,
                "max_order_unity_response_coefficient_proxy": margin,
                "risk_readout": "tight" if margin < 1.2 else "moderate" if margin < 2.0 else "loose",
                "meaning": "new X-sector response coefficients must stay below this proxy margin unless a sharper PPN map is derived",
            }
        )
    return rows


def claim_gate_rows(
    source_rows: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    degree_rows: list[dict[str, Any]],
    ppn_risks: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = sum(source["exists"] != "yes" for source in source_rows)
    best_live_routes = sum(row["status"] == "best_live_route" for row in candidates)
    degree_blockers = sum(row["best_route_status"] == "not_derived" for row in degree_rows)
    tight_cases = sum(row["risk_readout"] == "tight" for row in ppn_risks)
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing_sources == 0 else "fail",
            "evidence": f"missing={missing_sources}",
            "claim_allowed": "internal checkpoint only",
        },
        {
            "gate": "regular kinetic X rejected",
            "status": "pass",
            "evidence": "regular/proca vector X introduces local PPN hair",
            "claim_allowed": "guardrail",
        },
        {
            "gate": "first-order constraint route exists",
            "status": "conditional_pass" if best_live_routes == 1 else "fail",
            "evidence": f"best_live_routes={best_live_routes}",
            "claim_allowed": "candidate action class",
        },
        {
            "gate": "source identity reproduced",
            "status": "conditional_pass",
            "evidence": "delta_X first-order action gives nabla_mu Khat^{mu nu}-nabla^nu Gamma_eff=S_L^nu+d_rel J_rel^nu",
            "claim_allowed": "inside template only",
        },
        {
            "gate": "zero propagating X degree count derived",
            "status": "fail" if degree_blockers else "conditional_pass",
            "evidence": f"degree_blockers={degree_blockers}; constraint algebra not computed",
            "claim_allowed": "no local-GR promotion",
        },
        {
            "gate": "boundary action contract written",
            "status": "conditional_pass",
            "evidence": "boundary momentum pair B_X/A_rel specified",
            "claim_allowed": "contract",
        },
        {
            "gate": "boundary primitive selected",
            "status": "fail",
            "evidence": "compact shell exact/pure-gauge A_rel remains not derived",
            "claim_allowed": "no theorem",
        },
        {
            "gate": "PPN response margin safe",
            "status": "conditional_pass",
            "evidence": f"tight_cases={tight_cases}; closure proxy only",
            "claim_allowed": "risk map only",
        },
        {
            "gate": "local GR or PPN promoted",
            "status": "fail",
            "evidence": CLAIM_CEILING,
            "claim_allowed": "no",
        },
    ]


def decision_rows(ppn_risks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    tightest_case = min(ppn_risks, key=lambda row: float(row["max_order_unity_response_coefficient_proxy"]))
    return [
        {
            "decision": STATUS,
            "meaning": "The parent response field X^nu can be made plausible only as a first-order constraint/gauge/auxiliary sector with no quadratic kinetic term. That route reproduces the source identity and avoids obvious vector hair at the template level, but zero propagating degree count is not proven until the constraint algebra, boundary primitive, and constitutive P=Khat-Gamma g owner are derived.",
            "main_gain": "regular kinetic X routes are rejected and a precise first-order constraint route is isolated",
            "main_failure": "Dirac constraint closure, compact boundary primitive, and explicit boundary stress tensor are not derived",
            "tightest_ppn_proxy_case": tightest_case["case"],
            "tightest_response_coefficient_proxy": tightest_case["max_order_unity_response_coefficient_proxy"],
            "next_target": "223-X-constraint-algebra-and-Khat-Gamma-constitutive-owner.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_222_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    candidates = X_sector_candidate_rows()
    variation_rows = first_order_variation_rows()
    degree_rows = degree_count_rows()
    boundary_rows = boundary_action_rows()
    ppn_risks = PPN_risk_rows()
    gates = claim_gate_rows(source_rows, candidates, degree_rows, ppn_risks)
    decision = decision_rows(ppn_risks)

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "X_sector_candidate_ledger.csv": (
            candidates,
            [
                "candidate",
                "schematic_action",
                "source_identity",
                "kinetic_hessian_rank",
                "local_hair_risk",
                "boundary_ownership",
                "status",
                "reason",
            ],
        ),
        "first_order_variation_chain.csv": (
            variation_rows,
            ["step", "statement", "result", "open_issue"],
        ),
        "degree_count_audit.csv": (
            degree_rows,
            ["test", "requirement", "best_route_status", "evidence", "remaining_gap"],
        ),
        "boundary_action_contract.csv": (
            boundary_rows,
            ["boundary_clause", "expression", "status", "risk"],
        ),
        "local_PPN_hair_risk_map.csv": (
            ppn_risks,
            [
                "case",
                "q_like_gate",
                "base_q_proxy",
                "max_allowed_epsilon_J",
                "epsilon_fraction_of_gate",
                "max_order_unity_response_coefficient_proxy",
                "risk_readout",
                "meaning",
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

    missing_sources = sum(source["exists"] != "yes" for source in source_rows)
    degree_blockers = sum(row["best_route_status"] == "not_derived" for row in degree_rows)
    rejected_kinetic_routes = sum(row["status"] == "rejected" and "kinetic" in row["candidate"] for row in candidates)
    tightest_case = min(ppn_risks, key=lambda row: float(row["max_order_unity_response_coefficient_proxy"]))
    status_payload = {
        "status": decision[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(files.keys()),
        "missing_sources": missing_sources,
        "regular_kinetic_X_rejected": rejected_kinetic_routes >= 1,
        "first_order_constraint_route_written": True,
        "source_identity_reproduced_inside_template": True,
        "kinetic_hessian_rank_best_route": 0,
        "zero_propagating_X_degree_count_derived": False,
        "degree_count_blockers": degree_blockers,
        "boundary_action_contract_written": True,
        "boundary_primitive_selected": False,
        "explicit_boundary_stress_tensor_derived": False,
        "tightest_ppn_proxy_case": tightest_case["case"],
        "tightest_response_coefficient_proxy": float(tightest_case["max_order_unity_response_coefficient_proxy"]),
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
