#!/usr/bin/env python3
"""Checkpoint 205: derive or bound C-silence sources for BAO and local rulers."""

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

CHECKPOINT_205_NAME = "C-silence-source-bound-for-BAO-and-local-rulers"
CHECKPOINT_204_RUN = RUNS_ROOT / "20260601-000021-matter-metric-action-and-ruler-transport-owner-contract"
CHECKPOINT_198_RUN = RUNS_ROOT / "20260601-000015-BAO-radial-drift-and-alpha-owner-gate"
CHECKPOINT_197_RUN = RUNS_ROOT / "20260601-000014-BAO-common-mode-ratio-theorem-attempt"
CHECKPOINT_195_RUN = RUNS_ROOT / "20260601-000012-late-CMB-domain-rule-and-local-silence-gate"
CHECKPOINT_179_RUN = RUNS_ROOT / "20260531-235959-local-GR-PPN-silence-contract"

STATUS = "C_silence_bounds_derived_matter_trace_source_requires_parent_screening"
CLAIM_CEILING = "C_silence_internal_bounds_only_no_local_GR_or_BAO_promotion"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"

LOCKED_B_MEM = 2.0 / 27.0
H0_BRIDGE_RESIDUAL_DOTC_OVER_H = -0.0004084189185673548
H0_KM_S_MPC = 67.50994528839665
LIGHT_SPEED_KM_S = 299_792.458
HUBBLE_RADIUS_MPC = LIGHT_SPEED_KM_S / H0_KM_S_MPC
LOCAL_QR_GATE = 2.3e-5


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
        (Path(__file__).resolve(), "checkpoint 205 C-silence bound script"),
        (WORK_DIR / "204-matter-metric-action-and-ruler-transport-owner-contract.md", "previous matter-action owner checkpoint"),
        (CHECKPOINT_204_RUN / "status.json", "checkpoint 204 machine status"),
        (CHECKPOINT_204_RUN / "results" / "BAO_source_term_audit.csv", "checkpoint 204 source audit"),
        (WORK_DIR / "195-late-CMB-domain-rule-and-local-silence-gate.md", "endpoint/local silence checkpoint"),
        (CHECKPOINT_195_RUN / "status.json", "checkpoint 195 machine status"),
        (WORK_DIR / "179-local-GR-PPN-silence-contract.md", "local PPN silence checkpoint"),
        (CHECKPOINT_179_RUN / "results" / "cosmological_tidal_local_bounds.csv", "checkpoint 179 local tidal bounds"),
        (CHECKPOINT_179_RUN / "results" / "PPN_residual_vector.csv", "checkpoint 179 PPN residual vector"),
        (WORK_DIR / "197-BAO-common-mode-ratio-theorem-attempt.md", "BAO common-mode tolerance checkpoint"),
        (CHECKPOINT_197_RUN / "results" / "BAO_leakage_tolerance.csv", "checkpoint 197 BAO leakage tolerance"),
        (WORK_DIR / "198-BAO-radial-drift-and-alpha-owner-gate.md", "BAO radial drift checkpoint"),
        (CHECKPOINT_198_RUN / "results" / "radial_drift_tolerance.csv", "checkpoint 198 radial drift tolerance"),
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


def C_connection_and_source_derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "statement": "The matter-observer metric is conformal to the g-frame metric.",
            "equation": "tilde_g_mn = exp(C) g_mn",
            "status": "carried_from_checkpoint_194_204",
            "consequence": "constant C is common-mode; gradients and time drift are observable hazards",
        },
        {
            "step": 2,
            "statement": "The conformal connection shift is gradient-controlled.",
            "equation": "Delta Gamma^rho_mn = 1/2(delta^rho_m partial_n C + delta^rho_n partial_m C - g_mn partial^rho C)",
            "status": "derived_geometric_identity",
            "consequence": "local/BAO silence requires partial_mu C to be small or common-mode",
        },
        {
            "step": 3,
            "statement": "Matter variation with respect to C is not automatically zero.",
            "equation": "delta_C tilde_g_mn = tilde_g_mn delta C",
            "status": "derived_from_metric_map",
            "consequence": "universal matter coupling is safe for WEP but can source C through the trace",
        },
        {
            "step": 4,
            "statement": "A metric-only matter action contributes a trace source to the C equation.",
            "equation": "delta S_m / delta C = 1/2 sqrt(-tilde_g) T_tilde",
            "status": "conditional_variational_result",
            "consequence": "local dust matter has T_tilde ~= -rho, so a dynamical C needs screening/cancellation",
        },
        {
            "step": 5,
            "statement": "A generic C field equation must therefore contain a counterbalancing parent sector.",
            "equation": "E_C[g,C,...] + 1/2 sqrt(-tilde_g) T_tilde = 0",
            "status": "parent_equation_contract",
            "consequence": "C silence is not derived by the matter action; it is a new parent burden",
        },
        {
            "step": 6,
            "statement": "Linearized local response has a simple bound target.",
            "equation": "(Box_tilde - m_C,eff^2) delta C = delta J_C/Z_C",
            "status": "screening_contract_not_derivation",
            "consequence": "need delta C, L partial_i C, and dot_C/H below observable gates",
        },
    ]


def BAO_spatial_gradient_bound_rows() -> list[dict[str, Any]]:
    leakage_rows = read_csv_rows(CHECKPOINT_197_RUN / "results" / "BAO_leakage_tolerance.csv")
    scales_mpc = [50.0, 100.0, 150.0, 300.0, 500.0, 1000.0]
    rows: list[dict[str, Any]] = []
    for row in leakage_rows:
        threshold = float(row["delta_chi2_threshold"])
        frac = float(row["max_abs_fractional_BAO_ratio_shift"])
        max_delta_c = 2.0 * frac
        for scale_mpc in scales_mpc:
            rows.append(
                {
                    "delta_chi2_threshold": threshold,
                    "coherence_length_Mpc": scale_mpc,
                    "max_abs_fractional_BAO_ratio_shift": frac,
                    "max_abs_delta_C_across_length": max_delta_c,
                    "max_abs_grad_C_per_Mpc": max_delta_c / scale_mpc,
                    "rule": "|Delta C|/2 below BAO ratio leakage tolerance",
                    "status": "bound_derived_from_checkpoint_197",
                }
            )
    return rows


def BAO_radial_drift_bound_rows() -> list[dict[str, Any]]:
    radial_rows = read_csv_rows(CHECKPOINT_198_RUN / "results" / "radial_drift_tolerance.csv")
    rows: list[dict[str, Any]] = []
    for row in radial_rows:
        threshold = float(row["delta_chi2_threshold"])
        dotc_bound = float(row["max_abs_dot_C_over_H"])
        rows.append(
            {
                "alpha_mode": row["alpha_mode"],
                "delta_chi2_threshold": threshold,
                "max_abs_dot_C_over_H": dotc_bound,
                "full_memory_drift_ratio_to_bound": LOCKED_B_MEM / dotc_bound,
                "H0_bridge_residual_ratio_to_bound": abs(H0_BRIDGE_RESIDUAL_DOTC_OVER_H) / dotc_bound,
                "full_memory_late_drift_verdict": "rejected" if LOCKED_B_MEM > dotc_bound else "allowed",
                "H0_bridge_residual_verdict": "safe" if abs(H0_BRIDGE_RESIDUAL_DOTC_OVER_H) < dotc_bound else "unsafe",
                "status": "bound_imported_from_checkpoint_198",
            }
        )
    return rows


def memory_gradient_scenario_rows() -> list[dict[str, Any]]:
    frac_1sigma = float(
        read_csv_rows(CHECKPOINT_197_RUN / "results" / "BAO_leakage_tolerance.csv")[0][
            "max_abs_fractional_BAO_ratio_shift"
        ]
    )
    scenarios = [
        ("full_B_over_Hubble_radius", HUBBLE_RADIUS_MPC),
        ("full_B_over_2_Hubble_radii", 2.0 * HUBBLE_RADIUS_MPC),
        ("full_B_over_1_Gpc", 1000.0),
        ("full_B_over_500_Mpc", 500.0),
        ("full_B_over_300_Mpc", 300.0),
        ("full_B_over_150_Mpc", 150.0),
    ]
    probe_lengths = [100.0, 150.0, 300.0]
    rows: list[dict[str, Any]] = []
    for scenario, gradient_length_mpc in scenarios:
        grad = LOCKED_B_MEM / gradient_length_mpc
        for probe_length_mpc in probe_lengths:
            delta_c = grad * probe_length_mpc
            half_shift = 0.5 * delta_c
            rows.append(
                {
                    "scenario": scenario,
                    "gradient_length_Mpc": gradient_length_mpc,
                    "probe_length_Mpc": probe_length_mpc,
                    "grad_C_per_Mpc": grad,
                    "delta_C_across_probe": delta_c,
                    "half_delta_C_ratio_shift": half_shift,
                    "chi2_lt_1_fractional_bound": frac_1sigma,
                    "verdict": "safe_for_chi2_lt_1" if abs(half_shift) < frac_1sigma else "too_steep_for_chi2_lt_1",
                    "interpretation": "smooth horizon-scale C variation can be BAO-safe; sharp late gradients are not",
                }
            )
    return rows


def local_C_variation_bound_rows() -> list[dict[str, Any]]:
    local_rows = read_csv_rows(CHECKPOINT_179_RUN / "results" / "cosmological_tidal_local_bounds.csv")
    rows: list[dict[str, Any]] = []
    for row in local_rows:
        tidal = float(row["Omega_mem_H0r_over_c_squared"])
        max_delta_c = 2.0 * LOCAL_QR_GATE
        rows.append(
            {
                "scale": row["scale"],
                "radius_m": row["radius_m"],
                "cosmological_tidal_C_proxy": tidal,
                "local_qR_gate": LOCAL_QR_GATE,
                "max_abs_delta_C_across_scale": max_delta_c,
                "tidal_ratio_to_delta_C_gate": tidal / max_delta_c,
                "verdict": "tidal_safe" if tidal < max_delta_c else "not_safe",
                "claim_limit": "cosmological background/tidal proxy only; local matter trace sourcing still needs parent screening",
            }
        )
    return rows


def C_field_equation_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract": "stationary local fixed point",
            "mathematical_form": "E_C(C_*) + 1/2 sqrt(-tilde_g) T_tilde = 0 with partial_mu C_* ~= 0",
            "what_it_would_prove": "constant local C is a solution even in matter environments",
            "current_status": "not_derived",
            "hazard_if_missing": "matter trace creates local C gradients/fifth-force-like projection effects",
        },
        {
            "contract": "weak response to density contrast",
            "mathematical_form": "delta C ~= delta J_C/(Z_C m_C,eff^2), with |delta C| below local and BAO bounds",
            "what_it_would_prove": "matter inhomogeneities cannot move the clock/ruler conformal factor enough to be seen",
            "current_status": "bound_target_only",
            "hazard_if_missing": "galaxies/clusters/source environments generate non-common-mode ruler shifts",
        },
        {
            "contract": "BAO-domain spatial coherence",
            "mathematical_form": "|Delta C|/2 < 0.0027698476423345664 over the relevant BAO coherence length for Delta chi2<1",
            "what_it_would_prove": "spatial C gradients do not spoil DESI-like BAO ratios",
            "current_status": "numeric_bound_derived",
            "hazard_if_missing": "BAO common-mode theorem leaks through anisotropic/radial shape shifts",
        },
        {
            "contract": "late-time drift saturation",
            "mathematical_form": "|dot_C/H| < 0.011285628250379043 for fixed-alpha Delta chi2<1",
            "what_it_would_prove": "radial BAO D_H/r_d stays common-mode",
            "current_status": "numeric_bound_derived_not_parent_derived",
            "hazard_if_missing": "full B_mem per Hubble time is rejected by BAO radial drift",
        },
        {
            "contract": "local PPN/ruler silence",
            "mathematical_form": "|Delta C| < 4.6e-5 across PPN-sensitive local scales, plus no composition coupling",
            "what_it_would_prove": "conformal ruler/clock variation remains below local screening gates",
            "current_status": "bound_written_background_tidal_safe_trace_source_open",
            "hazard_if_missing": "local GR reduction remains closure-only",
        },
        {
            "contract": "domain separation",
            "mathematical_form": "CMB endpoint Delta C ~= B_mem, while late local/BAO domains have small partial_mu C",
            "what_it_would_prove": "the same C field can explain endpoint memory without wrecking local/BAO ratios",
            "current_status": "not_derived",
            "hazard_if_missing": "branch switching returns",
        },
    ]


def parent_mechanism_option_rows() -> list[dict[str, Any]]:
    return [
        {
            "mechanism": "heavy_or_stiff_C_mode",
            "how_it_could_help": "large m_C,eff suppresses trace-sourced local delta C",
            "cost": "introduces a scale that must be derived, not tuned after seeing bounds",
            "compatible_with_current_route": "possible",
            "status": "theorem_target",
        },
        {
            "mechanism": "auxiliary_constraint_C",
            "how_it_could_help": "C is fixed by a global/domain constraint instead of propagating as a locally sourced scalar",
            "cost": "must preserve Bianchi consistency and avoid arbitrary plateau axiom",
            "compatible_with_current_route": "possible_but_dangerous",
            "status": "closure_until_variation_written",
        },
        {
            "mechanism": "trace_sequestering_or_cancellation",
            "how_it_could_help": "matter trace source is cancelled by another parent sector",
            "cost": "needs exact symmetry/identity; otherwise looks engineered",
            "compatible_with_current_route": "possible",
            "status": "not_derived",
        },
        {
            "mechanism": "chameleon_symmetron_or_Vainshtein_like_screening",
            "how_it_could_help": "environment-dependent response keeps local C gradients small",
            "cost": "adds a known screening architecture that must be justified inside MTS",
            "compatible_with_current_route": "possible_side_route",
            "status": "not_MTS_derived",
        },
        {
            "mechanism": "pure_observer_map_non_dynamical_C",
            "how_it_could_help": "avoids local trace sourcing by not varying C as a field",
            "cost": "risks demoting C to projection closure rather than field theory",
            "compatible_with_current_route": "weak",
            "status": "closure_only_if_used",
        },
        {
            "mechanism": "late_saturation_endpoint_memory",
            "how_it_could_help": "C changes across cosmic history but is nearly constant within late domains",
            "cost": "must derive why dot_C/H today is tiny while Delta C_CMB ~= B_mem",
            "compatible_with_current_route": "lead_candidate",
            "status": "next_derivation_target",
        },
    ]


def source_owner_scorecard_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_or_silence_requirement": "matter trace source in C equation",
            "bound_or_derivation": "delta S_m/delta C = 1/2 sqrt(-tilde_g) T_tilde",
            "current_result": "derived_as_hazard",
            "promotion_effect": "blocks promotion until screened/cancelled",
        },
        {
            "source_or_silence_requirement": "BAO spatial gradient",
            "bound_or_derivation": "|Delta C|/2 < BAO leakage tolerance",
            "current_result": "numeric_bounds_derived",
            "promotion_effect": "sets target for parent C coherence",
        },
        {
            "source_or_silence_requirement": "BAO radial time drift",
            "bound_or_derivation": "|dot_C/H| < 0.011285628250379043 at fixed-alpha Delta chi2<1",
            "current_result": "numeric_bound_imported",
            "promotion_effect": "full B_mem/H late rolling rejected; saturation needed",
        },
        {
            "source_or_silence_requirement": "local cosmological tidal C proxy",
            "bound_or_derivation": "Omega_mem(H0 r/c)^2 below local q_R-like gate",
            "current_result": "safe_from_checkpoint_179",
            "promotion_effect": "background tide not the problem",
        },
        {
            "source_or_silence_requirement": "local matter-induced C gradients",
            "bound_or_derivation": "requires response bound for trace-sourced delta C",
            "current_result": "not_derived",
            "promotion_effect": "main local GR blocker",
        },
        {
            "source_or_silence_requirement": "CMB/late domain split",
            "bound_or_derivation": "Delta C_CMB ~= B_mem but late partial_mu C small",
            "current_result": "rule_target_not_parent_derived",
            "promotion_effect": "domain selector still open",
        },
    ]


def acceptance_gate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing = sum(row["exists"] != "yes" for row in source_rows)
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing == 0 else "fail",
            "evidence": f"missing={missing}",
            "claim_allowed": "internal derivation/bound audit",
        },
        {
            "gate": "conformal connection C-gradient hazard derived",
            "status": "pass",
            "evidence": "Delta Gamma is proportional to partial_mu C",
            "claim_allowed": "mathematical identity",
        },
        {
            "gate": "matter trace source identified",
            "status": "pass",
            "evidence": "delta S_m/delta C = 1/2 sqrt(-tilde_g) T_tilde",
            "claim_allowed": "hazard theorem",
        },
        {
            "gate": "BAO spatial C bound derived",
            "status": "pass",
            "evidence": "|Delta C|/2 tied to checkpoint 197 leakage tolerance",
            "claim_allowed": "numeric bound",
        },
        {
            "gate": "BAO radial C drift bound imported",
            "status": "pass",
            "evidence": "checkpoint 198 dot_C/H tolerance applied",
            "claim_allowed": "numeric bound",
        },
        {
            "gate": "local background tidal C proxy safe",
            "status": "pass",
            "evidence": "checkpoint 179 tidal bounds far below q_R-like local gate",
            "claim_allowed": "compatibility note",
        },
        {
            "gate": "local matter trace response screened by parent action",
            "status": "fail",
            "evidence": "screening/cancellation mechanism not derived",
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
            "meaning": "C-silence has been sharpened into explicit source and bound conditions. The conformal metric gives a trace source delta S_m/delta C = 1/2 sqrt(-tilde_g) T_tilde, so matter coupling does not automatically make C locally silent. BAO spatial and radial tolerance bounds are now explicit; local background tides are safe, but local matter-induced C response still needs a parent screening/cancellation mechanism.",
            "derived_gain": "C-gradient connection hazard, matter trace source, BAO gradient bounds, and BAO drift bounds are explicit",
            "good_news": "horizon-scale smooth C variation and the small H0-bridge residual can be BAO-safe; local cosmological tidal terms are tiny",
            "bad_news": "a dynamical universally coupled C is trace-sourced by matter unless the parent action screens/cancels it",
            "main_blocker": "parent_C_screening_or_constraint_mechanism",
            "next_target": "206-parent-C-screening-fixed-point-mechanism.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_205_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    connection_rows = C_connection_and_source_derivation_rows()
    spatial_rows = BAO_spatial_gradient_bound_rows()
    radial_rows = BAO_radial_drift_bound_rows()
    memory_rows = memory_gradient_scenario_rows()
    local_rows = local_C_variation_bound_rows()
    field_contract_rows = C_field_equation_contract_rows()
    mechanism_rows = parent_mechanism_option_rows()
    scorecard_rows = source_owner_scorecard_rows()
    gates = acceptance_gate_rows(source_rows)
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "C_connection_and_trace_source_derivation.csv": (
            connection_rows,
            ["step", "statement", "equation", "status", "consequence"],
        ),
        "BAO_spatial_gradient_bounds.csv": (
            spatial_rows,
            [
                "delta_chi2_threshold",
                "coherence_length_Mpc",
                "max_abs_fractional_BAO_ratio_shift",
                "max_abs_delta_C_across_length",
                "max_abs_grad_C_per_Mpc",
                "rule",
                "status",
            ],
        ),
        "BAO_radial_drift_bounds.csv": (
            radial_rows,
            [
                "alpha_mode",
                "delta_chi2_threshold",
                "max_abs_dot_C_over_H",
                "full_memory_drift_ratio_to_bound",
                "H0_bridge_residual_ratio_to_bound",
                "full_memory_late_drift_verdict",
                "H0_bridge_residual_verdict",
                "status",
            ],
        ),
        "memory_gradient_scenarios.csv": (
            memory_rows,
            [
                "scenario",
                "gradient_length_Mpc",
                "probe_length_Mpc",
                "grad_C_per_Mpc",
                "delta_C_across_probe",
                "half_delta_C_ratio_shift",
                "chi2_lt_1_fractional_bound",
                "verdict",
                "interpretation",
            ],
        ),
        "local_C_variation_bounds.csv": (
            local_rows,
            [
                "scale",
                "radius_m",
                "cosmological_tidal_C_proxy",
                "local_qR_gate",
                "max_abs_delta_C_across_scale",
                "tidal_ratio_to_delta_C_gate",
                "verdict",
                "claim_limit",
            ],
        ),
        "C_field_equation_contract.csv": (
            field_contract_rows,
            ["contract", "mathematical_form", "what_it_would_prove", "current_status", "hazard_if_missing"],
        ),
        "parent_screening_mechanism_options.csv": (
            mechanism_rows,
            ["mechanism", "how_it_could_help", "cost", "compatible_with_current_route", "status"],
        ),
        "C_source_owner_scorecard.csv": (
            scorecard_rows,
            ["source_or_silence_requirement", "bound_or_derivation", "current_result", "promotion_effect"],
        ),
        "acceptance_gates.csv": (
            gates,
            ["gate", "status", "evidence", "claim_allowed"],
        ),
        "decision.csv": (
            decision,
            [
                "decision",
                "meaning",
                "derived_gain",
                "good_news",
                "bad_news",
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
        "C_connection_gradient_hazard_derived": True,
        "matter_trace_source_derived": True,
        "BAO_spatial_gradient_bounds_derived": True,
        "BAO_radial_drift_bounds_applied": True,
        "local_background_tidal_proxy_safe": True,
        "local_matter_trace_screening_derived": False,
        "parent_C_screening_derived": False,
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
