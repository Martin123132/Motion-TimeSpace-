#!/usr/bin/env python3
"""Checkpoint 211: attempt to derive the parent metric for the G_K norm."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

CHECKPOINT_211_NAME = "GK-parent-metric-Ward-identity-attempt"
CHECKPOINT_210_RUN = RUNS_ROOT / "20260601-000027-GK-alphaK-parent-invariant-or-fixed-closure"
CHECKPOINT_209_RUN = RUNS_ROOT / "20260601-000026-Lcg-domain-scale-parent-derivation-or-demotion"
CHECKPOINT_205_RUN = RUNS_ROOT / "20260601-000022-C-silence-source-bound-for-BAO-and-local-rulers"

STATUS = "GK_metric_Ward_identity_partial_flow_block_only_composite_metric_fixed_closure"
CLAIM_CEILING = "GK_metric_partial_no_parent_norm_promotion"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"

H0_KM_S_MPC = 67.50994528839665
LIGHT_SPEED_KM_S = 299_792.458
HUBBLE_RADIUS_MPC = LIGHT_SPEED_KM_S / H0_KM_S_MPC
LOCKED_B_MEM = 2.0 / 27.0
LOCAL_DELTA_C_GATE = 4.6e-5
BAO_DELTA_C_GATE = 0.005539695284669133


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
        (Path(__file__).resolve(), "checkpoint 211 parent metric/Ward script"),
        (WORK_DIR / "210-GK-alphaK-parent-invariant-or-fixed-closure.md", "G_K invariant candidate checkpoint"),
        (CHECKPOINT_210_RUN / "status.json", "checkpoint 210 machine status"),
        (CHECKPOINT_210_RUN / "results" / "composite_GK_contract.csv", "checkpoint 210 G_K contract"),
        (CHECKPOINT_210_RUN / "results" / "branch_numeric_readout.csv", "checkpoint 210 branch numeric readout"),
        (CHECKPOINT_210_RUN / "results" / "parent_action_contract.csv", "checkpoint 210 parent action contract"),
        (WORK_DIR / "209-Lcg-domain-scale-parent-derivation-or-demotion.md", "L_cg rule checkpoint"),
        (CHECKPOINT_209_RUN / "results" / "Lcg_derivation_chain.csv", "checkpoint 209 derivation chain"),
        (WORK_DIR / "207-domain-projector-action-and-Bianchi-identity.md", "domain projector/Bianchi checkpoint"),
        (WORK_DIR / "143-domain-selector-variational-action-attempt.md", "C_coh/J_rel selector route"),
        (WORK_DIR / "96-parent-R-normalization-contract.md", "Ward identity gap"),
        (WORK_DIR / "97-canonical-R-theorem-attempt.md", "canonical theorem failure ledger"),
        (WORK_DIR / "205-C-silence-source-bound-for-BAO-and-local-rulers.md", "BAO/local C-silence bound checkpoint"),
        (CHECKPOINT_205_RUN / "results" / "BAO_spatial_gradient_bounds.csv", "checkpoint 205 BAO spatial bounds"),
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


def l_cg_from_beta(g0_per_mpc: float, beta: float) -> float:
    return 1.0 / math.sqrt(HUBBLE_RADIUS_MPC ** -2 + beta * g0_per_mpc * g0_per_mpc)


def delta_c_linear(g0_per_mpc: float, beta: float, baseline_mpc: float) -> float:
    return LOCKED_B_MEM * baseline_mpc / l_cg_from_beta(g0_per_mpc, beta)


def beta_max_for_gate(g0_per_mpc: float, baseline_mpc: float, gate: float) -> float:
    numerator = (gate / (LOCKED_B_MEM * baseline_mpc)) ** 2 - HUBBLE_RADIUS_MPC ** -2
    if numerator <= 0.0:
        return 0.0
    return numerator / (g0_per_mpc * g0_per_mpc)


def ward_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "ADM_DeWitt_flow_block",
            "equation": "||delta K||^2_G = delta K_ij delta K^ij - lambda_K (delta K)^2; split into variance(theta)+sigma^2",
            "derives": "relative normalization of expansion-dispersion/shear pieces up to trace convention",
            "status": "partial_pass",
            "failure": "does not derive Weyl/J_rel/Q weights or the full composite metric",
        },
        {
            "route": "Raychaudhuri_optical_scalars",
            "equation": "d theta/dtau = -theta^2/3 - sigma^2 + omega^2 - R_mn u^m u^n + div a",
            "derives": "why shear/flow dispersion are coherence hazards",
            "status": "partial_support",
            "failure": "focusing signs are dynamical, not a positive norm metric by themselves",
        },
        {
            "route": "Bel_Robinson_Weyl_norm",
            "equation": "W_D^2=(C_abcd C^abcd)^1/2 or superenergy norm",
            "derives": "natural positive local curvature piece",
            "status": "partial_support",
            "failure": "normalization relative to flow block needs a parent length/metric",
        },
        {
            "route": "Hodge_norm_relative_current",
            "equation": "||[J_rel]||^2 = integral_D J_rel wedge *J_rel after representative selection",
            "derives": "canonical boundary/current norm if J_rel representative exists",
            "status": "conditional_support",
            "failure": "checkpoint 143/207 still lack the representative/current owner",
        },
        {
            "route": "load_tensor_field_metric",
            "equation": "||delta Q||^2_M = M_QQ delta Q delta Q",
            "derives": "possible MTS-native anisotropy block",
            "status": "fail_open",
            "failure": "Q owner and Q_* normalization are incomplete",
        },
        {
            "route": "single_internal_Ward_identity",
            "equation": "delta S under Xi^A -> R^A_B Xi^B fixes one M_AB for every component",
            "derives": "would promote the composite metric",
            "status": "fail",
            "failure": "flow, Weyl, boundary current, and load tensor are heterogeneous objects; no shared symmetry is present",
        },
    ]


def metric_block_rows() -> list[dict[str, Any]]:
    return [
        {
            "block": "flow",
            "component": "c^-1(delta theta, sigma, omega)",
            "metric_choice": "ADM/kinematic unit block after trace normalization",
            "status": "partial_derived",
            "promotion_risk": "trace sign and vorticity positivity need exact convention",
        },
        {
            "block": "weyl",
            "component": "W_D=(C_abcd C^abcd)^1/4",
            "metric_choice": "unit coefficient beta_W=1 as fixed closure",
            "status": "not_parent_derived",
            "promotion_risk": "relative coefficient can affect local and galaxy branches",
        },
        {
            "block": "relative_current",
            "component": "L_D^-1[J_rel]",
            "metric_choice": "Hodge unit norm if representative is later derived",
            "status": "conditional_not_owned",
            "promotion_risk": "without representative this is a label, not a field equation",
        },
        {
            "block": "load",
            "component": "L_D^-1 delta Q/||Q||_*",
            "metric_choice": "unit coefficient beta_Q=1 as fixed closure",
            "status": "not_parent_derived",
            "promotion_risk": "Q_* can hide a normalization knob",
        },
        {
            "block": "cross_terms",
            "component": "Xi_A Xi_B for A != B",
            "metric_choice": "zero by minimal diagonal closure",
            "status": "closure_policy",
            "promotion_risk": "parent action could generate cross terms that alter all branch readouts",
        },
    ]


def beta_sensitivity_rows() -> list[dict[str, Any]]:
    branch_rows = {row["case"]: row for row in read_csv_rows(CHECKPOINT_210_RUN / "results" / "branch_numeric_readout.csv")}
    cases = [
        ("smooth_BAO_late_domain", BAO_DELTA_C_GATE, 150.0, "BAO smooth branch"),
        ("Gpc_transition_domain", BAO_DELTA_C_GATE, 150.0, "Gpc transition branch"),
        ("BAO_scale_transition", BAO_DELTA_C_GATE, 150.0, "BAO-scale transition branch"),
        ("solar_system_1AU_Weyl", LOCAL_DELTA_C_GATE, float(branch_rows["solar_system_1AU_Weyl"]["test_baseline_Mpc"]), "solar-system local Weyl branch"),
        ("earth_surface_Weyl", LOCAL_DELTA_C_GATE, float(branch_rows["earth_surface_Weyl"]["test_baseline_Mpc"]), "Earth-surface Weyl branch"),
    ]
    rows: list[dict[str, Any]] = []
    for case, gate, baseline, meaning in cases:
        g0 = float(branch_rows[case]["G_K_per_Mpc"])
        beta_max = beta_max_for_gate(g0, baseline, gate)
        rows.append(
            {
                "case": case,
                "meaning": meaning,
                "G0_per_Mpc": g0,
                "baseline_Mpc": baseline,
                "gate_DeltaC": gate,
                "DeltaC_beta_1": delta_c_linear(g0, 1.0, baseline),
                "beta_max_before_gate": beta_max,
                "beta_1_safe": "yes" if 1.0 <= beta_max else "no",
                "interpretation": "unit metric is acceptable for smooth/local examples but transition-scale G_K cannot be promoted as smooth BAO",
            }
        )
    return rows


def parent_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause": "P1_domain_congruence_owner",
            "future_parent_requirement": "derive u^mu_D and D from varied fields, not from observer choice",
            "current_result": "missing",
            "why_it_matters": "Xi_D is otherwise domain-gauge dependent",
        },
        {
            "clause": "P2_defect_vector_owner",
            "future_parent_requirement": "derive Xi_D components as projections of one coherent defect operator",
            "current_result": "candidate_only",
            "why_it_matters": "prevents arbitrary adding/removing of components",
        },
        {
            "clause": "P3_metric_Hessian",
            "future_parent_requirement": "M_AB = partial_A partial_B V_defect evaluated on the FLRW fixed point",
            "current_result": "partial_flow_only",
            "why_it_matters": "this would turn alpha_K=1 from convention into theorem",
        },
        {
            "clause": "P4_no_cross_term_policy",
            "future_parent_requirement": "prove off-diagonal M_AB terms vanish by symmetry or include them before scoring",
            "current_result": "closure_zero",
            "why_it_matters": "cross terms could mimic fitted coefficients",
        },
        {
            "clause": "P5_Bianchi_variation",
            "future_parent_requirement": "vary Xi_D and M_AB with respect to metric/coframe and include resulting stress",
            "current_result": "missing",
            "why_it_matters": "without this the field theory can violate conservation accounting",
        },
        {
            "clause": "P6_pre_empirical_freeze",
            "future_parent_requirement": "freeze M_AB and all weights before BAO/local/galaxy/CMB scoring",
            "current_result": "policy_pass",
            "why_it_matters": "keeps the branch from becoming post-hoc",
        },
    ]


def no_go_rows() -> list[dict[str, Any]]:
    return [
        {
            "temptation": "claim alpha_K derived because it was set to one",
            "why_wrong": "setting alpha_K=1 is a canonical convention unless M_AB is parent-derived",
            "safe_statement": "alpha_K is fixed closure, not a fitted parameter and not a theorem",
        },
        {
            "temptation": "let Weyl coefficient float for local PPN safety",
            "why_wrong": "that recreates the hidden tuning problem",
            "safe_statement": "use beta_W=1 or predeclared sensitivity only",
        },
        {
            "temptation": "ignore galaxy impact of Weyl/load suppression",
            "why_wrong": "a unified branch cannot protect local GR by silently killing galaxy phenomenology",
            "safe_statement": "run a composite-GK galaxy/BAO/local safety gate before promotion",
        },
        {
            "temptation": "use positive norms but skip Bianchi stress",
            "why_wrong": "field theory promotion requires conservation accounting",
            "safe_statement": "stress variation remains an explicit blocker",
        },
    ]


def claim_gate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing = sum(row["exists"] != "yes" for row in source_rows)
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing == 0 else "fail",
            "evidence": f"missing={missing}",
            "claim_allowed": "internal parent metric audit",
        },
        {
            "gate": "flow block partially derived",
            "status": "partial_pass",
            "evidence": "ADM/kinematic decomposition gives a natural norm for expansion dispersion/shear",
            "claim_allowed": "partial derivation",
        },
        {
            "gate": "Weyl block parent-normalized",
            "status": "fail",
            "evidence": "Bel-Robinson/Weyl norm exists, but relative coefficient not fixed",
            "claim_allowed": "fixed closure only",
        },
        {
            "gate": "J_rel representative derived",
            "status": "fail",
            "evidence": "Hodge norm needs a representative still missing from 143/207",
            "claim_allowed": "no promotion",
        },
        {
            "gate": "Q load metric derived",
            "status": "fail_open",
            "evidence": "Q owner and Q_* normalization incomplete",
            "claim_allowed": "no promotion",
        },
        {
            "gate": "single Ward identity for M_AB",
            "status": "fail",
            "evidence": "no symmetry unifies flow, Weyl, boundary, and load components",
            "claim_allowed": "no parent metric theorem",
        },
        {
            "gate": "unit diagonal metric safe as predeclared closure",
            "status": "conditional_pass",
            "evidence": "beta sensitivity table shows unit beta passes named smooth/local gates but not transition BAO branches",
            "claim_allowed": "closure branch for later safety testing",
        },
        {
            "gate": "Bianchi/stress variation derived",
            "status": "fail",
            "evidence": "no variation of Xi_D and M_AB stress has been calculated",
            "claim_allowed": "no field-theory completion claim",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "meaning": "The parent metric route partially works for the flow/kinematic block, but no current Ward identity fixes the full composite metric over flow, Weyl, J_rel, and Q. The safest honest branch is therefore a fixed diagonal closure M_AB=diag(1,1,1,1) after canonical normalization, with no fitted alpha_K and no promotion.",
            "main_gain": "flow block has partial geometric ownership and alpha_K remains frozen",
            "main_failure": "full composite M_AB is not parent-derived",
            "required_next_check": "test whether the fixed composite G_K closure is safe across BAO/local/galaxy branches before further promotion work",
            "next_target": "212-composite-GK-local-BAO-galaxy-safety-gate.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_211_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    ward_rows = ward_route_rows()
    metric_rows = metric_block_rows()
    beta_rows = beta_sensitivity_rows()
    contract_rows = parent_contract_rows()
    shortcut_rows = no_go_rows()
    gates = claim_gate_rows(source_rows)
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "Ward_identity_routes.csv": (
            ward_rows,
            ["route", "equation", "derives", "status", "failure"],
        ),
        "metric_block_ledger.csv": (
            metric_rows,
            ["block", "component", "metric_choice", "status", "promotion_risk"],
        ),
        "beta_sensitivity_gates.csv": (
            beta_rows,
            [
                "case",
                "meaning",
                "G0_per_Mpc",
                "baseline_Mpc",
                "gate_DeltaC",
                "DeltaC_beta_1",
                "beta_max_before_gate",
                "beta_1_safe",
                "interpretation",
            ],
        ),
        "future_parent_contract.csv": (
            contract_rows,
            ["clause", "future_parent_requirement", "current_result", "why_it_matters"],
        ),
        "forbidden_shortcuts.csv": (
            shortcut_rows,
            ["temptation", "why_wrong", "safe_statement"],
        ),
        "claim_gate_results.csv": (
            gates,
            ["gate", "status", "evidence", "claim_allowed"],
        ),
        "decision.csv": (
            decision,
            ["decision", "meaning", "main_gain", "main_failure", "required_next_check", "next_target", "promotion_allowed", "claim_ceiling"],
        ),
    }
    for filename, (rows, fieldnames) in files.items():
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
        "flow_metric_block_partially_derived": True,
        "Weyl_metric_parent_normalized": False,
        "J_rel_representative_derived": False,
        "Q_load_metric_derived": False,
        "single_Ward_identity_for_M_AB": False,
        "unit_diagonal_metric_fixed_closure": True,
        "Bianchi_stress_variation_derived": False,
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
