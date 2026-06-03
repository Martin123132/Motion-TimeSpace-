#!/usr/bin/env python3
"""Draft and audit the constrained parent-action skeleton."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SOURCE_18_STATUS = Path("runs/20260530-233024-parent-action-or-empirical-pillar-decision/status.json")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def field_rows() -> list[dict[str, Any]]:
    return [
        {
            "field": "e^A_mu",
            "role": "observer coframe / metric carrier",
            "definition": "g_mu_nu = eta_AB e^A_mu e^B_nu",
            "status": "standard_geometric_scaffold",
            "risk": "must not assume Einstein equations from the scaffold",
        },
        {
            "field": "C(x)",
            "role": "clock capacity or load-response scalar",
            "definition": "local weak-field target C^2 -> T^2 = 1 - L",
            "status": "postulated_parent_variable",
            "risk": "needs field equation that gives Newtonian limit",
        },
        {
            "field": "P_parallel",
            "role": "local radial/transport projector",
            "definition": "selects the propagation/routing direction in the local reduction",
            "status": "open_covariant_completion",
            "risk": "radial cell rule is not globally covariant until projector origin is defined",
        },
        {
            "field": "R_AB",
            "role": "reciprocal strain / local closure variable",
            "definition": "R_AB = ln(T^2 S) in the static spherical local reduction",
            "status": "closure_variable",
            "risk": "must be constrained, not given kinetic hair",
        },
        {
            "field": "lambda_R",
            "role": "multiplier or constrained-sector reaction field",
            "definition": "delta lambda_R gives R_AB=0",
            "status": "closure_multiplier_not_derived",
            "risk": "calling this derived would overclaim",
        },
        {
            "field": "Psi_matter",
            "role": "all matter fields",
            "definition": "couple universally to the same coframe e^A_mu",
            "status": "postulated_universal_coupling",
            "risk": "MICROSCOPE-scale constraints require this to be exact or derived",
        },
        {
            "field": "M_cosmo_or_memory",
            "role": "cosmology/memory sector placeholder",
            "definition": "must reduce to any C0/M-branch variables without breaking local closure",
            "status": "placeholder_not_action_derived",
            "risk": "phenomenological knobs cannot be hidden in the parent action",
        },
    ]


def action_term_rows() -> list[dict[str, Any]]:
    return [
        {
            "term": "S_geom",
            "schematic_form": "integral sqrt(-g) L_geom(e, connection, C, P_parallel)",
            "variation_target": "metric/coframe field equations and conservation identity",
            "label": "open",
            "must_prove": "Bianchi-like identity and GR/Newton limit without importing Einstein vacuum equations",
        },
        {
            "term": "S_load",
            "schematic_form": "integral sqrt(-g) L_load(C, grad C, matter trace or source scalar)",
            "variation_target": "C^2 -> 1-2GM/(rc^2) in local weak field",
            "label": "postulated_skeleton",
            "must_prove": "Newtonian potential and clock redshift emerge from source coupling",
        },
        {
            "term": "S_projector",
            "schematic_form": "integral sqrt(-g) L_proj(P_parallel, e, C)",
            "variation_target": "covariant origin of the local radial transport direction",
            "label": "open",
            "must_prove": "radial t-r cell is selected physically rather than inserted",
        },
        {
            "term": "S_R_constraint",
            "schematic_form": "integral sqrt(-g) lambda_R R_AB",
            "variation_target": "delta lambda_R -> R_AB=0",
            "label": "closure_term",
            "must_prove": "lambda_R has parent origin or remains explicitly closure-only",
        },
        {
            "term": "S_R_kinetic",
            "schematic_form": "integral sqrt(-g) W (grad R_AB)^2 / 2",
            "variation_target": "propagating reciprocal strain",
            "label": "forbidden",
            "must_prove": "excluded because it generates Q_R hair",
        },
        {
            "term": "S_matter",
            "schematic_form": "integral sqrt(-g) L_m(Psi_matter, e^A_mu)",
            "variation_target": "universal matter coupling and stress tensor",
            "label": "postulated_skeleton",
            "must_prove": "no species-dependent epsilon_matter unless predicted below WEP bounds",
        },
        {
            "term": "S_cosmo_memory",
            "schematic_form": "integral sqrt(-g) L_mem(C, M_cosmo_or_memory, history/curvature scalars)",
            "variation_target": "FLRW memory/cosmology branch",
            "label": "placeholder",
            "must_prove": "same sector connects to cosmology without spoiling local PPN closure",
        },
    ]


def variation_rows() -> list[dict[str, Any]]:
    return [
        {
            "variation": "delta_lambda_R",
            "desired_equation": "R_AB = 0",
            "current_status": "works_as_closure",
            "remaining_gap": "does not explain why lambda_R exists",
        },
        {
            "variation": "delta_R_AB",
            "desired_equation": "lambda_R + source_reaction = 0",
            "current_status": "prevents propagating hair if no kinetic term is present",
            "remaining_gap": "source reaction must not reintroduce Pi_R boundary charge",
        },
        {
            "variation": "delta_C",
            "desired_equation": "load equation giving C^2=1-2U/c^2 locally and cosmological memory globally",
            "current_status": "not_derived",
            "remaining_gap": "source coupling and FLRW reduction missing",
        },
        {
            "variation": "delta_e",
            "desired_equation": "coframe/metric equation with conservation identity",
            "current_status": "not_derived",
            "remaining_gap": "must recover beta=1 and universal free fall",
        },
        {
            "variation": "delta_P_parallel",
            "desired_equation": "physical transport/routing direction and t-r cell selection",
            "current_status": "not_derived",
            "remaining_gap": "projector origin is the covariance bottleneck",
        },
        {
            "variation": "delta_Psi_matter",
            "desired_equation": "matter equations on a universal coframe",
            "current_status": "postulated",
            "remaining_gap": "must derive or impose exact species universality",
        },
    ]


def local_limit_rows() -> list[dict[str, Any]]:
    return [
        {
            "limit_gate": "Newtonian_clock_limit",
            "target": "C^2 = T^2 = 1 - 2U/c^2",
            "skeleton_status": "target_stated_not_derived",
            "test_hook": "alpha_clock",
        },
        {
            "limit_gate": "reciprocity",
            "target": "R_AB=0 -> T^2 S=1",
            "skeleton_status": "closure_multiplier_pass",
            "test_hook": "q_R,Q_R",
        },
        {
            "limit_gate": "PPN_gamma",
            "target": "gamma=1",
            "skeleton_status": "conditional_on_R_AB_zero",
            "test_hook": "q_R",
        },
        {
            "limit_gate": "PPN_beta",
            "target": "beta=1",
            "skeleton_status": "open_completion_gate",
            "test_hook": "delta_beta",
        },
        {
            "limit_gate": "universal_matter_coupling",
            "target": "epsilon_matter=0",
            "skeleton_status": "postulated_not_derived",
            "test_hook": "epsilon_matter",
        },
        {
            "limit_gate": "no_reciprocal_charge",
            "target": "Q_R=0",
            "skeleton_status": "satisfied_only_if_R_AB_has_no_kinetic_mode",
            "test_hook": "Q_R",
        },
    ]


def cosmology_bridge_rows() -> list[dict[str, Any]]:
    return [
        {
            "bridge_item": "FLRW_capacity",
            "requirement": "C(x) must admit homogeneous C(t) or memory reduction",
            "status": "open",
            "risk": "local C^2=1-L may not determine cosmological dynamics",
        },
        {
            "bridge_item": "local_global_screening",
            "requirement": "R_AB=0 local closure must not force away cosmological memory effects",
            "status": "open",
            "risk": "same constraint could overconstrain FLRW branch",
        },
        {
            "bridge_item": "C0_M_branch_mapping",
            "requirement": "map C0/M parameters to action variables or label them phenomenological",
            "status": "open",
            "risk": "cosmology remains disconnected from parent theory",
        },
        {
            "bridge_item": "conservation",
            "requirement": "cosmological modified equations must obey a Bianchi-like identity",
            "status": "open",
            "risk": "energy nonconservation or hidden source terms",
        },
        {
            "bridge_item": "test_priors",
            "requirement": "action-derived parameters should reduce reliance on edge-hitting priors",
            "status": "open",
            "risk": "empirical branch remains fitted closure",
        },
    ]


def skeleton_gate_rows(source: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate": "source_18_complete",
            "status": "pass" if source.get("readout") == "parent_action_or_empirical_decision_two_track_parent_first" else "fail",
            "detail": str(source.get("readout")),
        },
        {
            "gate": "fields_defined",
            "status": "pass",
            "detail": "coframe, load, projector, R_AB, lambda_R, matter, and cosmology placeholders are explicit",
        },
        {
            "gate": "closure_labels_explicit",
            "status": "pass",
            "detail": "lambda_R R_AB is labeled closure, not derivation",
        },
        {
            "gate": "R_AB_zero_parent_derived",
            "status": "fail",
            "detail": "skeleton still uses multiplier closure",
        },
        {
            "gate": "Q_R_hair_removed",
            "status": "conditional_pass",
            "detail": "removed only by forbidding R_AB kinetic term",
        },
        {
            "gate": "beta_completion_derived",
            "status": "fail",
            "detail": "beta=1 remains a local completion gate",
        },
        {
            "gate": "universal_matter_coupling_derived",
            "status": "fail",
            "detail": "currently postulated to satisfy WEP screening",
        },
        {
            "gate": "cosmology_bridge_derived",
            "status": "fail",
            "detail": "FLRW/memory mapping is specified as a future requirement only",
        },
        {
            "gate": "main_workbench_mutation_allowed",
            "status": "fail",
            "detail": "this remains post-checkpoint scaffolding",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "skeleton_status",
            "status": "useful_contract_not_derivation",
            "evidence": "all required sectors are named and labeled, but critical equations remain open",
            "next_action": "turn skeleton into empirical-pillar queue before attempting more formal action algebra",
        },
        {
            "decision": "local_GR_status",
            "status": "closure_control_lane",
            "evidence": "R_AB=0 is still supplied by lambda_R closure",
            "next_action": "do not promote as derived local GR",
        },
        {
            "decision": "next_target",
            "status": "empirical_pillar_test_queue",
            "evidence": "parent skeleton has enough hooks to organize tests without overclaiming",
            "next_action": "create 20-empirical-pillar-test-queue.md",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Constrained parent-action skeleton.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    source = load_json(root / SOURCE_18_STATUS)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or root / "runs" / f"{timestamp}-constrained-parent-action-skeleton"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    fields = field_rows()
    terms = action_term_rows()
    variations = variation_rows()
    local_limits = local_limit_rows()
    cosmology = cosmology_bridge_rows()
    gates = skeleton_gate_rows(source)
    decisions = decision_rows()

    write_csv(results_dir / "parent_action_fields.csv", fields, list(fields[0].keys()))
    write_csv(results_dir / "parent_action_terms.csv", terms, list(terms[0].keys()))
    write_csv(results_dir / "parent_action_variation_targets.csv", variations, list(variations[0].keys()))
    write_csv(results_dir / "parent_action_local_limit_gates.csv", local_limits, list(local_limits[0].keys()))
    write_csv(results_dir / "parent_action_cosmology_bridge.csv", cosmology, list(cosmology[0].keys()))
    write_csv(results_dir / "parent_action_skeleton_gates.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "parent_action_skeleton_decision.csv", decisions, list(decisions[0].keys()))

    readout = "constrained_parent_action_skeleton_contract_not_derivation"
    status = {
        "status": "complete_constrained_parent_action_skeleton",
        "readout": readout,
        "recommendation": "use_as_contract_then_build_empirical_pillar_queue",
        "next_target": "20-empirical-pillar-test-queue.md",
        "skeleton_written": True,
        "derived_local_GR": False,
        "R_AB_zero_parent_derived": False,
        "closure_multiplier_used": True,
        "main_workbench_mutation_allowed_now": False,
        "critical_open_gates": [
            "R_AB_zero_parent_derived",
            "beta_completion_derived",
            "universal_matter_coupling_derived",
            "cosmology_bridge_derived",
        ],
        "outputs": {
            "parent_action_fields": str(results_dir / "parent_action_fields.csv"),
            "parent_action_terms": str(results_dir / "parent_action_terms.csv"),
            "parent_action_variation_targets": str(results_dir / "parent_action_variation_targets.csv"),
            "parent_action_local_limit_gates": str(results_dir / "parent_action_local_limit_gates.csv"),
            "parent_action_cosmology_bridge": str(results_dir / "parent_action_cosmology_bridge.csv"),
            "parent_action_skeleton_gates": str(results_dir / "parent_action_skeleton_gates.csv"),
            "parent_action_skeleton_decision": str(results_dir / "parent_action_skeleton_decision.csv"),
            "status_json": str(out_dir / "status.json"),
        },
    }
    (out_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (out_dir / "log.txt").write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    (out_dir / "DONE.txt").write_text(readout + "\n", encoding="utf-8")
    print(json.dumps(status, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
