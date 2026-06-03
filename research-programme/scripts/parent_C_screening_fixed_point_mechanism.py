#!/usr/bin/env python3
"""Checkpoint 206: construct or reject a parent C-screening fixed-point mechanism."""

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

CHECKPOINT_206_NAME = "parent-C-screening-fixed-point-mechanism"
CHECKPOINT_205_RUN = RUNS_ROOT / "20260601-000022-C-silence-source-bound-for-BAO-and-local-rulers"
CHECKPOINT_204_RUN = RUNS_ROOT / "20260601-000021-matter-metric-action-and-ruler-transport-owner-contract"
CHECKPOINT_179_RUN = RUNS_ROOT / "20260531-235959-local-GR-PPN-silence-contract"

STATUS = "C_screening_zero_mode_candidate_constructed_parent_projector_missing"
CLAIM_CEILING = "C_screening_mechanism_candidate_only_no_local_GR_or_BAO_promotion"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"

LOCKED_B_MEM = 2.0 / 27.0
LOCAL_DELTA_C_GATE = 2.0 * 2.3e-5
H0_KM_S_MPC = 67.50994528839665
LIGHT_SPEED_KM_S = 299_792.458
HUBBLE_RADIUS_MPC = LIGHT_SPEED_KM_S / H0_KM_S_MPC

MPC_PER_M = 1.0 / 3.0856775814913673e22
R_EARTH_M = 6_371_000.0
R_GPS_M = 26_560_000.0
R_SUN_M = 6.957e8
AU_M = 1.495978707e11
PC_M = 3.0856775814913673e16
KPC_M = 1.0e3 * PC_M


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
        (Path(__file__).resolve(), "checkpoint 206 parent C-screening mechanism script"),
        (WORK_DIR / "205-C-silence-source-bound-for-BAO-and-local-rulers.md", "previous C-silence source/bound checkpoint"),
        (CHECKPOINT_205_RUN / "status.json", "checkpoint 205 machine status"),
        (CHECKPOINT_205_RUN / "results" / "C_connection_and_trace_source_derivation.csv", "checkpoint 205 trace source derivation"),
        (CHECKPOINT_205_RUN / "results" / "BAO_spatial_gradient_bounds.csv", "checkpoint 205 BAO spatial C bounds"),
        (CHECKPOINT_205_RUN / "results" / "BAO_radial_drift_bounds.csv", "checkpoint 205 BAO radial C bounds"),
        (CHECKPOINT_205_RUN / "results" / "parent_screening_mechanism_options.csv", "checkpoint 205 mechanism options"),
        (WORK_DIR / "204-matter-metric-action-and-ruler-transport-owner-contract.md", "matter action owner checkpoint"),
        (CHECKPOINT_204_RUN / "status.json", "checkpoint 204 machine status"),
        (WORK_DIR / "179-local-GR-PPN-silence-contract.md", "local PPN silence checkpoint"),
        (CHECKPOINT_179_RUN / "results" / "cosmological_tidal_local_bounds.csv", "checkpoint 179 local background/tidal bounds"),
        (WORK_DIR / "94-endpoint-relaxation-DeltaR-gate.md", "older high-mobility screening preference"),
        (WORK_DIR / "195-late-CMB-domain-rule-and-local-silence-gate.md", "endpoint rule and local silence gate"),
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


def imported_bound_summary() -> dict[str, float]:
    spatial_rows = read_csv_rows(CHECKPOINT_205_RUN / "results" / "BAO_spatial_gradient_bounds.csv")
    radial_rows = read_csv_rows(CHECKPOINT_205_RUN / "results" / "BAO_radial_drift_bounds.csv")
    bao_150 = next(
        row
        for row in spatial_rows
        if row["delta_chi2_threshold"] == "1.0" and row["coherence_length_Mpc"] == "150.0"
    )
    fixed_radial = next(
        row for row in radial_rows if row["alpha_mode"] == "fixed" and row["delta_chi2_threshold"] == "1.0"
    )
    shared_radial = next(
        row for row in radial_rows if row["alpha_mode"] == "best_shared" and row["delta_chi2_threshold"] == "1.0"
    )
    return {
        "BAO_deltaC_150Mpc_chi2_lt1": float(bao_150["max_abs_delta_C_across_length"]),
        "BAO_gradC_150Mpc_chi2_lt1_per_Mpc": float(bao_150["max_abs_grad_C_per_Mpc"]),
        "BAO_fixed_dotC_over_H_chi2_lt1": float(fixed_radial["max_abs_dot_C_over_H"]),
        "BAO_shared_dotC_over_H_chi2_lt1": float(shared_radial["max_abs_dot_C_over_H"]),
        "local_deltaC_gate": LOCAL_DELTA_C_GATE,
    }


def fixed_point_equation_rows() -> list[dict[str, Any]]:
    return [
        {
            "piece": "decompose_C",
            "mathematical_form": "C(x)=C_D(t)+delta C(x)",
            "purpose": "separate endpoint/global memory from local/BAO perturbations",
            "derived_status": "definition_for_mechanism_test",
            "risk": "if delta C is not controlled, C_D split is only notation",
        },
        {
            "piece": "domain_zero_mode_projector",
            "mathematical_form": "Pi_D[J](x)=<J>_D, with (1-Pi_D)J not sourcing C_D",
            "purpose": "local trace inhomogeneities do not source the coherent memory mode",
            "derived_status": "candidate_constraint_not_parent_derived",
            "risk": "nonlocal/projector axiom unless derived from domain field or auxiliary constraint",
        },
        {
            "piece": "coherent_fixed_point",
            "mathematical_form": "E_C(C_D,<T>_D,M_D)=0",
            "purpose": "fix C_D by coarse-grained/domain source rather than local density",
            "derived_status": "candidate_equation",
            "risk": "amplitude and domain average still need parent origin",
        },
        {
            "piece": "stability_condition",
            "mathematical_form": "M_D^2 = partial E_C / partial C_D > 0",
            "purpose": "small perturbations return to the saturated branch",
            "derived_status": "standard_fixed_point_requirement",
            "risk": "stability scale could be tuned if not tied to MTS variables",
        },
        {
            "piece": "local_response",
            "mathematical_form": "delta C_k = (1-Pi_D)delta J_C,k / [Z_C(k^2/a^2+m_C,eff^2)]",
            "purpose": "bound residual response of nonzero modes",
            "derived_status": "linearized_screening_law",
            "risk": "requires Z_C, m_C,eff, and Pi_D from parent action",
        },
        {
            "piece": "late_saturation",
            "mathematical_form": "|dot C_D/H| < BAO radial tolerance, while Delta C_CMB ~= B_mem across endpoints",
            "purpose": "allow cosmic endpoint memory without late BAO/local rolling",
            "derived_status": "bound_contract",
            "risk": "still needs a time-domain transition law",
        },
    ]


def mechanism_scorecard_rows() -> list[dict[str, Any]]:
    return [
        {
            "mechanism": "ordinary_light_local_scalar",
            "can_suppress_local_trace_source": "no",
            "can_keep_CMB_endpoint_memory": "yes",
            "main_failure": "matter trace sources local gradients and dot_C unless response is tiny",
            "status": "rejected_as_lead",
        },
        {
            "mechanism": "heavy_or_stiff_C_mode",
            "can_suppress_local_trace_source": "yes_if_Zm2_large",
            "can_keep_CMB_endpoint_memory": "possible_if_background_roll_saturates",
            "main_failure": "local gates demand an enormous local stiffness if source amplitude is order B_mem",
            "status": "conditional_side_route",
        },
        {
            "mechanism": "chameleon_or_environmental_screening",
            "can_suppress_local_trace_source": "yes_in_principle",
            "can_keep_CMB_endpoint_memory": "possible",
            "main_failure": "imports a known screening architecture unless derived from MTS domain variables",
            "status": "not_MTS_derived",
        },
        {
            "mechanism": "trace_sequestering_cancellation",
            "can_suppress_local_trace_source": "yes_if_exact",
            "can_keep_CMB_endpoint_memory": "yes_if_cancellation_only_removes_fluctuations",
            "main_failure": "requires exact identity; approximate cancellation is fine-tuning",
            "status": "candidate_but_symmetry_missing",
        },
        {
            "mechanism": "non_dynamical_observer_map_C",
            "can_suppress_local_trace_source": "yes_by_not_varying_C",
            "can_keep_CMB_endpoint_memory": "yes_as_projection",
            "main_failure": "demotes C from field-theory variable to closure/projection rule",
            "status": "closure_only",
        },
        {
            "mechanism": "coherent_zero_mode_domain_C",
            "can_suppress_local_trace_source": "yes_if_projector_derives",
            "can_keep_CMB_endpoint_memory": "yes",
            "main_failure": "parent origin of Pi_D/domain average and Bianchi accounting is missing",
            "status": "lead_candidate_not_promoted",
        },
    ]


def required_suppression_rows(bounds: dict[str, float]) -> list[dict[str, Any]]:
    targets = [
        ("local_PPN_deltaC", "local", bounds["local_deltaC_gate"]),
        ("BAO_150Mpc_spatial_deltaC", "BAO", bounds["BAO_deltaC_150Mpc_chi2_lt1"]),
        ("BAO_fixed_radial_dotC_over_H", "BAO", bounds["BAO_fixed_dotC_over_H_chi2_lt1"]),
        ("BAO_shared_radial_dotC_over_H", "BAO", bounds["BAO_shared_dotC_over_H_chi2_lt1"]),
    ]
    rows: list[dict[str, Any]] = []
    for target, arena, bound in targets:
        required_suppression = bound / LOCKED_B_MEM
        rows.append(
            {
                "target": target,
                "arena": arena,
                "bound": bound,
                "reference_unscreened_scale": LOCKED_B_MEM,
                "required_response_fraction_below_Bmem": required_suppression,
                "rejection_if_response_order_Bmem": "yes" if required_suppression < 1.0 else "no",
                "readout": "local dominates" if target == "local_PPN_deltaC" else "BAO bound",
            }
        )
    return rows


def massive_mode_threshold_rows(bounds: dict[str, float]) -> list[dict[str, Any]]:
    scales = [
        ("Earth radius", R_EARTH_M * MPC_PER_M, bounds["local_deltaC_gate"]),
        ("GPS orbit", R_GPS_M * MPC_PER_M, bounds["local_deltaC_gate"]),
        ("Solar radius", R_SUN_M * MPC_PER_M, bounds["local_deltaC_gate"]),
        ("1 AU", AU_M * MPC_PER_M, bounds["local_deltaC_gate"]),
        ("1 pc", PC_M * MPC_PER_M, bounds["local_deltaC_gate"]),
        ("8 kpc", 8.0 * KPC_M * MPC_PER_M, bounds["local_deltaC_gate"]),
        ("150 Mpc BAO", 150.0, bounds["BAO_deltaC_150Mpc_chi2_lt1"]),
    ]
    rows: list[dict[str, Any]] = []
    for scale, length_mpc, bound in scales:
        ratio = LOCKED_B_MEM / bound
        mL_min = math.sqrt(max(ratio - 1.0, 0.0))
        m_min_per_mpc = mL_min / length_mpc if length_mpc > 0 else math.inf
        m_over_H0 = m_min_per_mpc * HUBBLE_RADIUS_MPC
        rows.append(
            {
                "scale": scale,
                "length_Mpc": length_mpc,
                "bound_deltaC": bound,
                "Bmem_over_bound": ratio,
                "required_m_eff_times_L_if_order_B_source": mL_min,
                "required_m_eff_per_Mpc": m_min_per_mpc,
                "required_m_eff_over_H0": m_over_H0,
                "verdict": "extreme_local_stiffness" if m_over_H0 > 1.0e9 else "moderate_or_cosmological_stiffness",
            }
        )
    return rows


def zero_mode_dilution_rows(bounds: dict[str, float]) -> list[dict[str, Any]]:
    source_sizes = [
        ("1 AU source", AU_M * MPC_PER_M),
        ("1 pc source", PC_M * MPC_PER_M),
        ("8 kpc source", 8.0 * KPC_M * MPC_PER_M),
        ("1 Mpc source", 1.0),
        ("150 Mpc BAO patch", 150.0),
        ("300 Mpc BAO patch", 300.0),
    ]
    domain_sizes = [
        ("Hubble domain", HUBBLE_RADIUS_MPC),
        ("2 Hubble domain", 2.0 * HUBBLE_RADIUS_MPC),
        ("1 Gpc domain", 1000.0),
    ]
    rows: list[dict[str, Any]] = []
    for source_name, source_mpc in source_sizes:
        for domain_name, domain_mpc in domain_sizes:
            volume_fraction = (source_mpc / domain_mpc) ** 3
            diluted_delta_c = LOCKED_B_MEM * volume_fraction
            rows.append(
                {
                    "source_region": source_name,
                    "domain": domain_name,
                    "source_length_Mpc": source_mpc,
                    "domain_length_Mpc": domain_mpc,
                    "volume_fraction": volume_fraction,
                    "Bmem_times_volume_fraction": diluted_delta_c,
                    "safe_vs_local_deltaC_gate": "yes" if diluted_delta_c < bounds["local_deltaC_gate"] else "no",
                    "safe_vs_BAO_150_deltaC_gate": "yes" if diluted_delta_c < bounds["BAO_deltaC_150Mpc_chi2_lt1"] else "no",
                    "interpretation": "domain zero-mode averaging can make local sources harmless if the projector is real",
                }
            )
    return rows


def bianchi_and_covariance_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract": "projector_from_action",
            "required_statement": "Pi_D is generated by a domain/coherent-mode field, not chosen after fitting",
            "mathematical_form": "delta_{lambda_D} S -> (1-Pi_D)C = 0 or equivalent covariant constraint",
            "current_status": "missing",
            "failure_if_missing": "zero-mode route is a plateau/projector axiom",
        },
        {
            "contract": "Bianchi_accounting",
            "required_statement": "constraint stress plus C stress makes total divergence vanish",
            "mathematical_form": "nabla_mu(E_g^{mu nu}+E_C^{mu nu}+E_D^{mu nu}+T_g^{mu nu})=0",
            "current_status": "not_derived",
            "failure_if_missing": "local silence violates conservation or hides exchange force",
        },
        {
            "contract": "endpoint_memory_without_late_drift",
            "required_statement": "C_D evolves between early and late endpoints but has small late dot_C/H",
            "mathematical_form": "Delta C_CMB ~= B_mem and |dot_C/H|_late < 0.011285628250379043",
            "current_status": "bound_known_transition_law_missing",
            "failure_if_missing": "CMB bridge and BAO/local silence cannot both hold",
        },
        {
            "contract": "local_trace_decoupling",
            "required_statement": "nonzero local trace modes do not source observable delta C above local gates",
            "mathematical_form": "||(1-Pi_D)delta J_C/[Z(k^2+m_eff^2)]|| < 4.6e-5",
            "current_status": "bound_contract",
            "failure_if_missing": "local GR/PPN silence remains closure-only",
        },
        {
            "contract": "domain_not_data_tuned",
            "required_statement": "domain scale/coherence follows from MTS variables such as L_cg, chi_D, or boundary charge",
            "mathematical_form": "L_D = F[L_cg, chi_D, Q] before BAO/CMB scoring",
            "current_status": "missing",
            "failure_if_missing": "domain size becomes an empirical rescue knob",
        },
    ]


def transition_law_target_rows(bounds: dict[str, float]) -> list[dict[str, Any]]:
    return [
        {
            "transition_requirement": "early_to_late_endpoint_jump",
            "mathematical_target": "C_late - C_early ~= B_mem = 2/27",
            "bound_or_value": LOCKED_B_MEM,
            "status": "empirical_locked_theorem_target",
            "reason": "needed for half-memory H0/CMB endpoint bridge",
        },
        {
            "transition_requirement": "late_BAO_drift_suppression",
            "mathematical_target": "|dot_C/H|_late < fixed-alpha BAO bound",
            "bound_or_value": bounds["BAO_fixed_dotC_over_H_chi2_lt1"],
            "status": "numeric_bound",
            "reason": "full Bmem per Hubble time is rejected",
        },
        {
            "transition_requirement": "late_spatial_coherence_150Mpc",
            "mathematical_target": "|Delta C| over 150 Mpc < BAO chi2<1 bound",
            "bound_or_value": bounds["BAO_deltaC_150Mpc_chi2_lt1"],
            "status": "numeric_bound",
            "reason": "BAO common-mode ratio must not leak spatially",
        },
        {
            "transition_requirement": "local_PPN_silence",
            "mathematical_target": "|Delta C| local < local q_R-derived delta C gate",
            "bound_or_value": bounds["local_deltaC_gate"],
            "status": "numeric_bound",
            "reason": "local rulers/clocks cannot see unscreened conformal variation",
        },
        {
            "transition_requirement": "activation_shape",
            "mathematical_target": "dot_C/H large enough in transition era but small today",
            "bound_or_value": "profile_not_derived",
            "status": "missing",
            "reason": "must connect endpoint memory to late saturation without branch switching",
        },
    ]


def claim_gate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing = sum(row["exists"] != "yes" for row in source_rows)
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing == 0 else "fail",
            "evidence": f"missing={missing}",
            "claim_allowed": "internal mechanism audit",
        },
        {
            "gate": "ordinary light scalar rejected as lead",
            "status": "pass",
            "evidence": "trace source creates local gradients unless response is suppressed",
            "claim_allowed": "negative route",
        },
        {
            "gate": "massive/stiff response bound derived",
            "status": "pass",
            "evidence": "m_eff L thresholds computed against local and BAO gates",
            "claim_allowed": "bound target",
        },
        {
            "gate": "coherent zero-mode route constructed",
            "status": "conditional_pass",
            "evidence": "C_D plus Pi_D projector can suppress local trace sources while preserving endpoint memory",
            "claim_allowed": "candidate mechanism only",
        },
        {
            "gate": "projector/domain origin parent-derived",
            "status": "fail",
            "evidence": "Pi_D, L_D, and constraint stress are not derived from a full parent action",
            "claim_allowed": "no promotion",
        },
        {
            "gate": "Bianchi/covariance accounting derived",
            "status": "fail",
            "evidence": "constraint stress and total divergence identity remain contracts",
            "claim_allowed": "no local GR promotion",
        },
        {
            "gate": "BAO/local support claim allowed",
            "status": "fail",
            "evidence": CLAIM_CEILING,
            "claim_allowed": "no",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "meaning": "The strongest parent C-screening route is not an ordinary local scalar. It is a coherent zero-mode/domain projector: C_D carries endpoint memory, while nonzero local trace modes are projected out or heavily suppressed. This can satisfy the numerical local/BAO silence bounds in principle, but the projector/domain origin, Bianchi accounting, and late transition law are not yet derived.",
            "constructed_mechanism": "C(x)=C_D(t)+delta C with Pi_D sourcing only the coherent mode and bounded residual delta C_k",
            "rejected_route": "ordinary_light_local_C_scalar_with_universal_matter_trace_source",
            "main_gain": "local and BAO silence now point to a specific zero-mode/constraint parent action rather than vague screening language",
            "main_blocker": "derive_Pi_D_domain_constraint_and_Bianchi_identity_from_parent_action",
            "next_target": "207-domain-projector-action-and-Bianchi-identity.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_206_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    bounds = imported_bound_summary()
    source_rows = source_register_rows()
    fixed_rows = fixed_point_equation_rows()
    mechanism_rows = mechanism_scorecard_rows()
    suppression_rows = required_suppression_rows(bounds)
    threshold_rows = massive_mode_threshold_rows(bounds)
    dilution_rows = zero_mode_dilution_rows(bounds)
    bianchi_rows = bianchi_and_covariance_contract_rows()
    transition_rows = transition_law_target_rows(bounds)
    gates = claim_gate_rows(source_rows)
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "fixed_point_equation_contract.csv": (
            fixed_rows,
            ["piece", "mathematical_form", "purpose", "derived_status", "risk"],
        ),
        "screening_mechanism_scorecard.csv": (
            mechanism_rows,
            ["mechanism", "can_suppress_local_trace_source", "can_keep_CMB_endpoint_memory", "main_failure", "status"],
        ),
        "required_suppression_factors.csv": (
            suppression_rows,
            [
                "target",
                "arena",
                "bound",
                "reference_unscreened_scale",
                "required_response_fraction_below_Bmem",
                "rejection_if_response_order_Bmem",
                "readout",
            ],
        ),
        "massive_mode_thresholds.csv": (
            threshold_rows,
            [
                "scale",
                "length_Mpc",
                "bound_deltaC",
                "Bmem_over_bound",
                "required_m_eff_times_L_if_order_B_source",
                "required_m_eff_per_Mpc",
                "required_m_eff_over_H0",
                "verdict",
            ],
        ),
        "zero_mode_domain_dilution.csv": (
            dilution_rows,
            [
                "source_region",
                "domain",
                "source_length_Mpc",
                "domain_length_Mpc",
                "volume_fraction",
                "Bmem_times_volume_fraction",
                "safe_vs_local_deltaC_gate",
                "safe_vs_BAO_150_deltaC_gate",
                "interpretation",
            ],
        ),
        "Bianchi_and_covariance_contract.csv": (
            bianchi_rows,
            ["contract", "required_statement", "mathematical_form", "current_status", "failure_if_missing"],
        ),
        "transition_law_targets.csv": (
            transition_rows,
            ["transition_requirement", "mathematical_target", "bound_or_value", "status", "reason"],
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
                "constructed_mechanism",
                "rejected_route",
                "main_gain",
                "main_blocker",
                "next_target",
                "promotion_allowed",
                "claim_ceiling",
            ],
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
        "ordinary_light_scalar_rejected_as_lead": True,
        "massive_mode_bounds_derived": True,
        "zero_mode_domain_projector_candidate_constructed": True,
        "projector_parent_origin_derived": False,
        "Bianchi_accounting_derived": False,
        "transition_law_derived": False,
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
