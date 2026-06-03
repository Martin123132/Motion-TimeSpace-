#!/usr/bin/env python3
"""Checkpoint 210: construct or demote the G_K / alpha_K owner."""

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

CHECKPOINT_210_NAME = "GK-alphaK-parent-invariant-or-fixed-closure"
CHECKPOINT_209_RUN = RUNS_ROOT / "20260601-000026-Lcg-domain-scale-parent-derivation-or-demotion"
CHECKPOINT_208_RUN = RUNS_ROOT / "20260601-000025-domain-representative-selection-law"
CHECKPOINT_205_RUN = RUNS_ROOT / "20260601-000022-C-silence-source-bound-for-BAO-and-local-rulers"

STATUS = "GK_composite_invariant_candidate_alphaK_fixed_closure_parent_metric_missing"
CLAIM_CEILING = "GK_alphaK_internal_candidate_no_domain_scale_or_local_GR_promotion"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"

H0_KM_S_MPC = 67.50994528839665
LIGHT_SPEED_KM_S = 299_792.458
HUBBLE_RADIUS_MPC = LIGHT_SPEED_KM_S / H0_KM_S_MPC
LOCKED_B_MEM = 2.0 / 27.0
LOCAL_DELTA_C_GATE = 4.6e-5

G_NEWTON = 6.67430e-11
LIGHT_SPEED_M_S = 299_792_458.0
MPC_M = 3.0856775814913673e22
PC_M = MPC_M / 1.0e6
AU_M = 149_597_870_700.0
M_SUN_KG = 1.98847e30
M_EARTH_KG = 5.9722e24
R_EARTH_M = 6_371_000.0


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
        (Path(__file__).resolve(), "checkpoint 210 G_K / alpha_K script"),
        (WORK_DIR / "209-Lcg-domain-scale-parent-derivation-or-demotion.md", "previous L_cg rule checkpoint"),
        (CHECKPOINT_209_RUN / "status.json", "checkpoint 209 machine status"),
        (CHECKPOINT_209_RUN / "results" / "Lcg_derivation_chain.csv", "checkpoint 209 derivation chain"),
        (CHECKPOINT_209_RUN / "results" / "branch_limit_table.csv", "checkpoint 209 branch limits"),
        (WORK_DIR / "208-domain-representative-selection-law.md", "domain representative selection law"),
        (CHECKPOINT_208_RUN / "results" / "coherence_branch_scores.csv", "checkpoint 208 C_coh branch readouts"),
        (WORK_DIR / "207-domain-projector-action-and-Bianchi-identity.md", "domain projector/Bianchi checkpoint"),
        (WORK_DIR / "143-domain-selector-variational-action-attempt.md", "auxiliary C_coh/J_rel selector route"),
        (WORK_DIR / "132-smooth-memory-growth-theorem-attempt.md", "linear FLRW memory perturbation result"),
        (WORK_DIR / "96-parent-R-normalization-contract.md", "trace-projection Ward identity gap"),
        (WORK_DIR / "97-canonical-R-theorem-attempt.md", "canonical R theorem failure ledger"),
        (WORK_DIR / "205-C-silence-source-bound-for-BAO-and-local-rulers.md", "C-silence source/bound checkpoint"),
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


def l_cg_from_gk(g_k_per_mpc: float) -> float:
    return 1.0 / math.sqrt(HUBBLE_RADIUS_MPC ** -2 + g_k_per_mpc * g_k_per_mpc)


def schwarzschild_weyl_sqrt_m2(mass_kg: float, radius_m: float) -> float:
    """Return (C_abcd C^abcd)^1/2 for Schwarzschild in SI m^-2."""
    return math.sqrt(48.0) * G_NEWTON * mass_kg / (LIGHT_SPEED_M_S**2 * radius_m**3)


def weyl_component_per_mpc(mass_kg: float, radius_m: float) -> float:
    """Return W=(C_abcd C^abcd)^1/4 as an inverse length in Mpc^-1."""
    sqrt_c2_m2 = schwarzschild_weyl_sqrt_m2(mass_kg, radius_m)
    return math.sqrt(sqrt_c2_m2) * MPC_M


def candidate_invariant_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate_piece": "flow_dispersion",
            "symbol": "I_flow",
            "equation": "I_flow=c^-2 <(theta-<theta>)^2 + sigma_ab sigma^ab + omega_ab omega^ab>_D",
            "units": "L^-2",
            "FLRW_limit": "zero for exactly homogeneous/isotropic expansion",
            "local_role": "suppresses domains with shear, vorticity, or expansion dispersion",
            "BAO_role": "small for smooth late domains; grows for transition/wall domains",
            "parent_status": "covariant candidate from congruence kinematics",
            "risk": "quiet static curvature can evade it unless a curvature term is also present",
        },
        {
            "candidate_piece": "weyl_curvature",
            "symbol": "I_W",
            "equation": "I_W=<sqrt(C_abcd C^abcd)>_D or W_D^2 with W_D=(C_abcd C^abcd)^1/4",
            "units": "L^-2",
            "FLRW_limit": "zero in exact FLRW because Weyl curvature vanishes",
            "local_role": "natural local/PPN suppressor around compact masses without a plateau axiom",
            "BAO_role": "should be tiny in smooth FLRW-like domains; active in collapsed structure",
            "parent_status": "geometric scalar candidate",
            "risk": "can over-suppress galaxy/domain effects if applied too naively",
        },
        {
            "candidate_piece": "relative_boundary_current",
            "symbol": "I_J",
            "equation": "I_J=L_D^-2 ||[J_rel]||_D^2",
            "units": "L^-2 if [J_rel] is dimensionless-normalized",
            "FLRW_limit": "zero for trivial representative; nonzero only for boundary/cohomology obstruction",
            "local_role": "keeps transition boundaries out of promoted local branch",
            "BAO_role": "marks survey/domain edges as conditional rather than fundamental",
            "parent_status": "MTS-native but representative missing",
            "risk": "cannot be promoted until J_rel is action-derived",
        },
        {
            "candidate_piece": "load_anisotropy",
            "symbol": "I_Q",
            "equation": "I_Q=L_D^-2 ||Q-<Q>_D||^2/(||Q||_*^2+epsilon)",
            "units": "L^-2",
            "FLRW_limit": "zero for homogeneous isotropic load",
            "local_role": "suppresses non-coherent or anisotropic load domains",
            "BAO_role": "small if BAO patch samples a smooth common-mode load",
            "parent_status": "MTS-native but Q owner incomplete",
            "risk": "normalization ||Q||_* is another hidden alpha_K unless parent-fixed",
        },
    ]


def composite_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "statement": "Package all coherence-breaking data into a vector Xi_D with inverse-length components.",
            "equation": "Xi_D=(c^-1 delta theta, c^-1 sigma, c^-1 omega, W_D, L_D^-1[J_rel], L_D^-1 delta Q/||Q||_*)",
            "status": "candidate_constructed",
            "gap": "component list and Q/J normalizations are not yet uniquely forced",
        },
        {
            "step": 2,
            "statement": "Define G_K as the positive norm of Xi_D.",
            "equation": "G_K^2[D]=||Xi_D||_M^2=M_AB Xi_D^A Xi_D^B >= 0",
            "status": "candidate_constructed",
            "gap": "parent metric M_AB is not derived",
        },
        {
            "step": 3,
            "statement": "Use the norm definition to absorb alpha_K.",
            "equation": "L_cg^-2=L_H^-2+G_K^2, so alpha_K=1 by definition of canonical G_K",
            "status": "fixed_closure",
            "gap": "alpha_K is fixed only if M_AB is canonical and not refittable",
        },
        {
            "step": 4,
            "statement": "Recover homogeneous FLRW.",
            "equation": "Xi_D=0 -> G_K=0 -> L_cg=L_H=c/H",
            "status": "conditional_pass",
            "gap": "does not prove the parent action selects this representative",
        },
        {
            "step": 5,
            "statement": "Suppress local/transition branches without a separate plateau axiom.",
            "equation": "W_D or flow/boundary terms large -> L_cg ~= 1/G_K",
            "status": "conditional_route",
            "gap": "must be checked against galaxy branch and full PPN residuals",
        },
        {
            "step": 6,
            "statement": "A parent proof would have to vary the field-space metric and selector.",
            "equation": "delta S_parent -> M_AB and Xi_D fixed, not fitted",
            "status": "not_derived",
            "gap": "current corpus lacks the Ward/current identity that fixes M_AB",
        },
    ]


def alpha_normalization_rows() -> list[dict[str, Any]]:
    return [
        {
            "normalization_route": "external_alpha_K_parameter",
            "equation": "L_cg^-2=L_H^-2+alpha_K G_K^2",
            "result": "rejected_as_promotion",
            "reason": "alpha_K can become a hidden tuning knob",
            "allowed_use": "only as explicitly predeclared closure sensitivity",
        },
        {
            "normalization_route": "canonical_norm_definition",
            "equation": "G_K^2=||Xi_D||^2 and alpha_K=1",
            "result": "best_current_route",
            "reason": "removes the independent alpha_K knob",
            "allowed_use": "fixed closure, not parent theorem",
        },
        {
            "normalization_route": "parent_field_metric",
            "equation": "M_AB follows from kinetic/current term in S_parent",
            "result": "theorem_target",
            "reason": "would fix relative weights and make alpha_K genuinely derived",
            "allowed_use": "not available yet",
        },
        {
            "normalization_route": "data_fit_alpha_K",
            "equation": "choose alpha_K from BAO/local residuals",
            "result": "forbidden",
            "reason": "would undermine the no-rescue-knob discipline",
            "allowed_use": "none for promotion",
        },
    ]


def branch_numeric_rows() -> list[dict[str, Any]]:
    smooth_bao_gk = 1.0 / 10_000.0
    gpc_transition_gk = 1.0 / 1_000.0
    bao_transition_gk = 1.0 / 150.0
    solar_1au_weyl = weyl_component_per_mpc(M_SUN_KG, AU_M)
    earth_surface_weyl = weyl_component_per_mpc(M_EARTH_KG, R_EARTH_M)
    milky_way_8kpc_weyl = weyl_component_per_mpc(6.0e10 * M_SUN_KG, 8_000.0 * PC_M)
    cases = [
        {
            "case": "ideal_FLRW",
            "G_K_per_Mpc": 0.0,
            "source": "all Xi_D components vanish",
            "test_baseline_Mpc": 150.0,
            "gate_DeltaC": "",
            "interpretation": "recovers Hubble-cap coherent branch",
        },
        {
            "case": "smooth_BAO_late_domain",
            "G_K_per_Mpc": smooth_bao_gk,
            "source": "illustrative weak flow/Weyl dispersion",
            "test_baseline_Mpc": 150.0,
            "gate_DeltaC": "0.005539695284669133",
            "interpretation": "near-Hubble domain, should remain BAO-common-mode safe",
        },
        {
            "case": "Gpc_transition_domain",
            "G_K_per_Mpc": gpc_transition_gk,
            "source": "inverse Gpc coherence hazard",
            "test_baseline_Mpc": 150.0,
            "gate_DeltaC": "0.005539695284669133",
            "interpretation": "begins to pressure BAO shape if full memory varies across it",
        },
        {
            "case": "BAO_scale_transition",
            "G_K_per_Mpc": bao_transition_gk,
            "source": "inverse BAO-scale hazard",
            "test_baseline_Mpc": 150.0,
            "gate_DeltaC": "0.005539695284669133",
            "interpretation": "not allowed as a smooth BAO common-mode branch",
        },
        {
            "case": "solar_system_1AU_Weyl",
            "G_K_per_Mpc": solar_1au_weyl,
            "source": "Schwarzschild Weyl fourth-root for 1 solar mass at 1 AU",
            "test_baseline_Mpc": AU_M / MPC_M,
            "gate_DeltaC": str(LOCAL_DELTA_C_GATE),
            "interpretation": "candidate local suppressor; needs PPN residual derivation",
        },
        {
            "case": "earth_surface_Weyl",
            "G_K_per_Mpc": earth_surface_weyl,
            "source": "Schwarzschild Weyl fourth-root for Earth mass at Earth radius",
            "test_baseline_Mpc": R_EARTH_M / MPC_M,
            "gate_DeltaC": str(LOCAL_DELTA_C_GATE),
            "interpretation": "strong local curvature branch; illustrative only",
        },
        {
            "case": "milky_way_8kpc_Weyl",
            "G_K_per_Mpc": milky_way_8kpc_weyl,
            "source": "rough Schwarzschild Weyl fourth-root for 6e10 solar masses inside 8 kpc",
            "test_baseline_Mpc": 0.008,
            "gate_DeltaC": "",
            "interpretation": "galaxy-safety warning: curvature term may affect galaxy branch if not domain-projected",
        },
    ]
    rows: list[dict[str, Any]] = []
    for case in cases:
        g_k = float(case["G_K_per_Mpc"])
        l_cg = l_cg_from_gk(g_k)
        delta_c = LOCKED_B_MEM * float(case["test_baseline_Mpc"]) / l_cg
        gate_text = str(case["gate_DeltaC"])
        if gate_text:
            gate = float(gate_text)
            safe = "yes" if delta_c < gate else "no"
        else:
            safe = "not_scored"
        rows.append(
            {
                **case,
                "L_cg_Mpc": l_cg,
                "L_cg_pc": l_cg * 1.0e6,
                "eta_today_if_used_as_FLRW_scale": H0_KM_S_MPC * l_cg / LIGHT_SPEED_KM_S,
                "DeltaC_over_test_baseline_if_linear": delta_c,
                "safe_against_named_gate": safe,
                "status": "illustrative_not_promotion",
            }
        )
    return rows


def bao_bound_rows() -> list[dict[str, Any]]:
    bound_row = next(
        row
        for row in read_csv_rows(CHECKPOINT_205_RUN / "results" / "BAO_spatial_gradient_bounds.csv")
        if row["delta_chi2_threshold"] == "1.0" and row["coherence_length_Mpc"] == "150.0"
    )
    max_delta_c = float(bound_row["max_abs_delta_C_across_length"])
    rows: list[dict[str, Any]] = []
    for g_k in [0.0, 1.0 / 10_000.0, 1.0 / 4_440.715463763339, 1.0 / 1_000.0, 1.0 / 500.0, 1.0 / 150.0]:
        l_cg = l_cg_from_gk(g_k)
        delta_c = LOCKED_B_MEM * 150.0 / l_cg
        rows.append(
            {
                "G_K_per_Mpc": g_k,
                "L_cg_Mpc": l_cg,
                "DeltaC_across_150Mpc_if_linear": delta_c,
                "checkpoint205_max_DeltaC_chi2_lt1": max_delta_c,
                "safe": "yes" if delta_c < max_delta_c else "no",
                "meaning": "BAO common-mode branch needs G_K well below inverse Gpc unless endpoint profile is flatter than linear",
            }
        )
    return rows


def parent_action_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_clause": "C1_covariant_vector",
            "required_statement": "Xi_D is built only from covariant scalars/tensors of the selected domain/congruence",
            "current_status": "partial",
            "failure_if_missing": "G_K becomes coordinate/gauge artefact",
        },
        {
            "contract_clause": "C2_positive_norm",
            "required_statement": "M_AB is positive semidefinite so G_K^2>=0",
            "current_status": "candidate_pass",
            "failure_if_missing": "L_cg can become imaginary or branch-unstable",
        },
        {
            "contract_clause": "C3_FLRW_zero",
            "required_statement": "Xi_D=0 in exact FLRW",
            "current_status": "candidate_pass",
            "failure_if_missing": "eta=1/Hubble-cap limit lost",
        },
        {
            "contract_clause": "C4_local_activation",
            "required_statement": "Weyl/flow/boundary pieces activate in local bound or transition domains",
            "current_status": "conditional_pass",
            "failure_if_missing": "local branch smuggles in a plateau axiom again",
        },
        {
            "contract_clause": "C5_metric_owned",
            "required_statement": "M_AB and component weights are fixed by parent action or Ward identity",
            "current_status": "fail",
            "failure_if_missing": "alpha_K has merely moved into hidden weights",
        },
        {
            "contract_clause": "C6_Bianchi_accounting",
            "required_statement": "variation of Xi_D and M_AB contributes to total stress/conservation",
            "current_status": "fail_open",
            "failure_if_missing": "domain selector violates conservation or double-counts stress",
        },
        {
            "contract_clause": "C7_empirical_precommitment",
            "required_statement": "no component or weight is chosen after BAO/local/galaxy scoring",
            "current_status": "pass_as_policy",
            "failure_if_missing": "route becomes post-hoc tuning",
        },
    ]


def claim_gate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing = sum(row["exists"] != "yes" for row in source_rows)
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing == 0 else "fail",
            "evidence": f"missing={missing}",
            "claim_allowed": "internal G_K/alpha_K audit",
        },
        {
            "gate": "G_K candidate invariant constructed",
            "status": "pass",
            "evidence": "G_K^2=||Xi_D||_M^2 with flow, Weyl, J_rel, and load-anisotropy candidates",
            "claim_allowed": "candidate theorem route",
        },
        {
            "gate": "alpha_K independent knob removed",
            "status": "conditional_pass",
            "evidence": "alpha_K=1 if G_K is defined as canonical norm",
            "claim_allowed": "fixed closure only",
        },
        {
            "gate": "FLRW limit recovered",
            "status": "conditional_pass",
            "evidence": "Xi_D=0 -> G_K=0 -> L_cg=L_H",
            "claim_allowed": "conditional branch readout",
        },
        {
            "gate": "local suppressor route available",
            "status": "conditional_pass",
            "evidence": "Weyl fourth-root supplies nonzero inverse length around compact masses",
            "claim_allowed": "candidate only; no PPN promotion",
        },
        {
            "gate": "BAO smooth-domain danger identified",
            "status": "pass",
            "evidence": "G_K near inverse BAO scale fails checkpoint-205 C-gradient safety",
            "claim_allowed": "guardrail",
        },
        {
            "gate": "parent metric M_AB derived",
            "status": "fail",
            "evidence": "no action/Ward identity fixes component weights",
            "claim_allowed": "no promotion",
        },
        {
            "gate": "Bianchi/stress accounting derived",
            "status": "fail_open",
            "evidence": "Xi_D variation stress not yet calculated",
            "claim_allowed": "no field-theory completion claim",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "meaning": "A viable next derivation route exists: define G_K as the positive norm of a coherence-breaking vector Xi_D whose components are flow dispersion, Weyl curvature, relative boundary current, and load anisotropy. This removes alpha_K as an independent parameter by setting alpha_K=1 in the canonical norm. But the field-space metric M_AB and the Bianchi/stress variation are not parent-derived, so this is fixed closure/theorem-target, not promotion.",
            "main_gain": "alpha_K can be frozen honestly rather than left as a hidden fit knob",
            "main_risk": "if Weyl/load pieces are applied naively they may over-suppress galaxy or domain branches",
            "demotion": "G_K is a candidate invariant norm, not a proven parent scalar",
            "next_target": "211-GK-parent-metric-Ward-identity-attempt.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_210_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    invariant_rows = candidate_invariant_rows()
    composite_rows = composite_contract_rows()
    alpha_rows = alpha_normalization_rows()
    numeric_rows = branch_numeric_rows()
    bao_rows = bao_bound_rows()
    action_rows = parent_action_contract_rows()
    gates = claim_gate_rows(source_rows)
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "candidate_invariant_pieces.csv": (
            invariant_rows,
            ["candidate_piece", "symbol", "equation", "units", "FLRW_limit", "local_role", "BAO_role", "parent_status", "risk"],
        ),
        "composite_GK_contract.csv": (
            composite_rows,
            ["step", "statement", "equation", "status", "gap"],
        ),
        "alphaK_normalization_ledger.csv": (
            alpha_rows,
            ["normalization_route", "equation", "result", "reason", "allowed_use"],
        ),
        "branch_numeric_readout.csv": (
            numeric_rows,
            [
                "case",
                "G_K_per_Mpc",
                "source",
                "test_baseline_Mpc",
                "gate_DeltaC",
                "interpretation",
                "L_cg_Mpc",
                "L_cg_pc",
                "eta_today_if_used_as_FLRW_scale",
                "DeltaC_over_test_baseline_if_linear",
                "safe_against_named_gate",
                "status",
            ],
        ),
        "BAO_GK_safety_scan.csv": (
            bao_rows,
            ["G_K_per_Mpc", "L_cg_Mpc", "DeltaC_across_150Mpc_if_linear", "checkpoint205_max_DeltaC_chi2_lt1", "safe", "meaning"],
        ),
        "parent_action_contract.csv": (
            action_rows,
            ["contract_clause", "required_statement", "current_status", "failure_if_missing"],
        ),
        "claim_gate_results.csv": (
            gates,
            ["gate", "status", "evidence", "claim_allowed"],
        ),
        "decision.csv": (
            decision,
            ["decision", "meaning", "main_gain", "main_risk", "demotion", "next_target", "promotion_allowed", "claim_ceiling"],
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
        "G_K_candidate_invariant_constructed": True,
        "alpha_K_fixed_as_canonical_norm_closure": True,
        "alpha_K_parent_derived": False,
        "parent_metric_M_AB_derived": False,
        "Bianchi_stress_accounting_derived": False,
        "FLRW_limit_recovered_conditionally": True,
        "local_suppressor_route_available_conditionally": True,
        "BAO_GK_safety_scanned": True,
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
