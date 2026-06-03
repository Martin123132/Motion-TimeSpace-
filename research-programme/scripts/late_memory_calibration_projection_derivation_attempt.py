from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "late-memory-calibration-projection-derivation-attempt"
STATUS = "late_memory_calibration_projection_conditionally_derived_half_factor_parent_selector_missing"
CLAIM_CEILING = "calibration_projection_internal_only_no_CMB_BAO_or_local_GR_promotion"

B_MEM = 2.0 / 27.0
C_KM_S = 299_792.458
H0_KM_S_MPC = 67.51
L_H_MPC = C_KM_S / H0_KM_S_MPC
BAO_RATIO_TOLERANCE_CHI2_LT_1 = 0.0027698476423345664
BAO_DOTC_OVER_H_BOUND = 0.011285628250379043
SMALL_H0_BRIDGE_RESIDUAL_DOTC_OVER_H = -0.0004084189185673548
LOCAL_QR_GATE = 2.3e-5
AU_MPC = 1.0 / 206_264.80624709636 / 1_000_000.0


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "202-late-common-mode-H0-rd-owner-derivation-attempt.md", "late common-mode BAO owner"),
        (ROOT / "203-fossil-ruler-transport-equation-attempt.md", "conditional fossil-ruler transport"),
        (ROOT / "205-C-silence-source-bound-for-BAO-and-local-rulers.md", "C gradient/drift/local source bounds"),
        (ROOT / "207-domain-projector-action-and-Bianchi-identity.md", "action-level projector and Bianchi accounting"),
        (ROOT / "208-domain-representative-selection-law.md", "representative selector and Hubble-cap domain"),
        (ROOT / "263-post-scale-lock-CMB-bridge-readiness-gate.md", "post-scale-lock CMB bridge policy"),
        (ROOT / "264-official-CMB-likelihood-preflight.md", "official CMB likelihood preflight gate"),
        (ROOT / "scripts" / "late_memory_calibration_projection_derivation_attempt.py", "this derivation gate script"),
    ]
    return [
        {
            "source": relpath(path),
            "role": role,
            "exists": "yes" if path.exists() else "no",
        }
        for path, role in sources
    ]


def theorem_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "piece": "conformal_metric_map",
            "input": "tilde_g_munu = exp(C_D) g_munu",
            "derivation": "line elements and clock intervals scale as d_tilde_l = exp(C_D/2) d_l and d_tilde_tau = exp(C_D/2) d_tau",
            "status": "conditional_derived",
            "remaining_burden": "parent action must derive the projected zero-mode C_D rather than insert it",
        },
        {
            "piece": "half_factor",
            "input": "dimensionful readout under the conformal map",
            "derivation": "endpoint or clock calibration ratios carry exp(Delta C_D/2), so the factor 1/2 is geometric once exp(C) is chosen",
            "status": "conditional_derived",
            "remaining_burden": "derive Delta C_D = B_mem for the relevant endpoint pair",
        },
        {
            "piece": "same_domain_ratio_cancellation",
            "input": "distance and ruler measured in the same late matter domain",
            "derivation": "tilde_D_X/tilde_r = exp(C_D/2)D_X / exp(C_D/2)r = D_X/r",
            "status": "conditional_derived",
            "remaining_burden": "derive fossil-ruler transport and bound residual gradients/drift",
        },
        {
            "piece": "CMB_endpoint_contrast",
            "input": "emitter and observer belong to different calibration endpoints",
            "derivation": "a photon endpoint comparison is sensitive to exp((C_obs-C_emit)/2)",
            "status": "conditional_derived",
            "remaining_burden": "derive the physical endpoint assignment and prevent theta/H0 profiling from becoming evidence",
        },
        {
            "piece": "BAO_late_common_mode",
            "input": "post-drag matter-correlation ruler transported in label space",
            "derivation": "late BAO survey reads both D_X and r_BAO in the same C_D domain, so only leakage terms survive",
            "status": "conditional_derived",
            "remaining_burden": "derive parent matter action, source-free xi transport, and release-independent alpha",
        },
        {
            "piece": "local_silence",
            "input": "C_D is domain zero-mode; C_perp is constrained/suppressed",
            "derivation": "if grad_i C_D = 0 and local C_perp response is projected out, no local conformal fifth-force term appears",
            "status": "conditional_not_derived",
            "remaining_burden": "derive projected trace-source cancellation or volume-suppressed response from parent action",
        },
        {
            "piece": "Bianchi_safety",
            "input": "projector/domain/auxiliary stresses retained in T_total",
            "derivation": "diffeomorphism invariance can keep nabla_mu T_total^{mu nu}=0 on shell",
            "status": "conditional_derived",
            "remaining_burden": "retain all projector stresses; do not use a projector then drop its stress",
        },
        {
            "piece": "amplitude_and_scale_lock",
            "input": "B_mem=2/27 and Hstar=H0",
            "derivation": "not derived here; imported as closure/theorem target only",
            "status": "not_derived",
            "remaining_burden": "parent amplitude and boundary scale-lock theorem still missing",
        },
    ]


def leakage_bound_rows() -> list[dict[str, Any]]:
    probes = [
        ("1_AU", AU_MPC),
        ("1_pc", 1.0e-6),
        ("1_Mpc", 1.0),
        ("50_Mpc", 50.0),
        ("100_Mpc", 100.0),
        ("150_Mpc", 150.0),
        ("300_Mpc", 300.0),
        ("1000_Mpc", 1000.0),
    ]
    rows: list[dict[str, Any]] = []
    for label, length_mpc in probes:
        smooth_endpoint_leak = 0.5 * B_MEM * length_mpc / L_H_MPC
        zero_mode_volume_response = B_MEM * (length_mpc / L_H_MPC) ** 3
        rows.append(
            {
                "probe": label,
                "length_Mpc": length_mpc,
                "smooth_half_deltaC_over_Hubble_domain": smooth_endpoint_leak,
                "smooth_BAO_safe_chi2_lt_1": "yes" if smooth_endpoint_leak < BAO_RATIO_TOLERANCE_CHI2_LT_1 else "no",
                "zero_mode_volume_response": zero_mode_volume_response,
                "volume_response_below_local_qR_gate": "yes" if zero_mode_volume_response < LOCAL_QR_GATE else "no",
            }
        )
    return rows


def derived_bound_rows() -> list[dict[str, Any]]:
    max_linear_safe_length = 2.0 * BAO_RATIO_TOLERANCE_CHI2_LT_1 * L_H_MPC / B_MEM
    max_volume_safe_length = L_H_MPC * (LOCAL_QR_GATE / B_MEM) ** (1.0 / 3.0)
    full_memory_drift_ratio = B_MEM / BAO_DOTC_OVER_H_BOUND
    residual_drift_ratio = abs(SMALL_H0_BRIDGE_RESIDUAL_DOTC_OVER_H) / BAO_DOTC_OVER_H_BOUND
    return [
        {
            "quantity": "Hubble_cap_domain_LD_Mpc",
            "value": L_H_MPC,
            "condition": "L_D = c/H0 in the homogeneous FLRW limit",
            "interpretation": "predeclared smooth-domain scale used for leakage tests",
        },
        {
            "quantity": "max_linear_probe_for_BAO_chi2_lt_1_Mpc",
            "value": max_linear_safe_length,
            "condition": "0.5*B_mem*(L/L_D) < BAO ratio tolerance",
            "interpretation": "smooth Hubble-domain memory is BAO-safe below this probe length",
        },
        {
            "quantity": "max_volume_probe_for_local_qR_gate_Mpc",
            "value": max_volume_safe_length,
            "condition": "B_mem*(L/L_D)^3 < local qR gate",
            "interpretation": "zero-mode dilution is locally safe below this scale if the projector theorem is real",
        },
        {
            "quantity": "full_memory_drift_over_BAO_bound",
            "value": full_memory_drift_ratio,
            "condition": "B_mem / BAO |dotC/H| bound",
            "interpretation": "unsaturated full rolling memory is too fast for BAO radial drift",
        },
        {
            "quantity": "small_H0_bridge_residual_over_BAO_bound",
            "value": residual_drift_ratio,
            "condition": "abs(-0.0004084189185673548) / BAO |dotC/H| bound",
            "interpretation": "small residual drift is safely below the imported BAO bound",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "half_factor_from_metric_map",
            "result": "conditional_pass",
            "evidence": "tilde_g=exp(C)g gives lengths/clocks scaling exp(C/2)",
            "claim_effect": "factor 1/2 no longer needs to be pure numerology if the conformal map is parent-owned",
        },
        {
            "gate": "same_domain_ratio_cancellation",
            "result": "conditional_pass",
            "evidence": "same late C_D factor cancels in D_X/r_BAO",
            "claim_effect": "BAO common-mode route strengthened but not promoted",
        },
        {
            "gate": "CMB_endpoint_contrast",
            "result": "conditional_pass",
            "evidence": "different endpoints keep exp(Delta C_D/2)",
            "claim_effect": "half-memory CMB bridge remains theorem target",
        },
        {
            "gate": "BAO_smooth_leakage_bound",
            "result": "pass_as_bound",
            "evidence": "150 Mpc smooth half-leak remains below imported chi2<1 tolerance",
            "claim_effect": "shows route is not automatically BAO-dead",
        },
        {
            "gate": "full_memory_drift",
            "result": "fail_if_unsaturated",
            "evidence": "B_mem rolling drift exceeds imported BAO dotC/H bound",
            "claim_effect": "requires saturation or residual-drift law",
        },
        {
            "gate": "local_trace_source_silence",
            "result": "open",
            "evidence": "domain zero-mode avoids gradients only if parent projector suppresses local C_perp/source response",
            "claim_effect": "local GR/PPN not promoted",
        },
        {
            "gate": "parent_selector_and_transition_law",
            "result": "fail_open",
            "evidence": "domain selector, transition law, B_mem amplitude, and Hstar scale-lock remain parent burdens",
            "claim_effect": "closure/theorem-target status retained",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "The conformal domain-zero-mode route conditionally derives the half-factor, "
                "same-domain BAO cancellation, and endpoint contrast structure. It does not yet "
                "derive the parent selector, local trace-source suppression, transition law, "
                "or B_mem/Hstar amplitude lock."
            ),
            "next_target": "projected_trace_source_Ward_identity_or_demote_local_silence_to_closure",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "projection_theorem_ledger.csv": (theorem_ledger_rows(), ["piece", "input", "derivation", "status", "remaining_burden"]),
        "leakage_bounds.csv": (
            leakage_bound_rows(),
            [
                "probe",
                "length_Mpc",
                "smooth_half_deltaC_over_Hubble_domain",
                "smooth_BAO_safe_chi2_lt_1",
                "zero_mode_volume_response",
                "volume_response_below_local_qR_gate",
            ],
        ),
        "derived_bounds.csv": (derived_bound_rows(), ["quantity", "value", "condition", "interpretation"]),
        "gate_results.csv": (gate_rows(), ["gate", "result", "evidence", "claim_effect"]),
        "decision.csv": (decision_rows(), ["decision", "claim_ceiling", "meaning", "next_target"]),
    }
    for filename, (rows, fieldnames) in outputs.items():
        write_csv(results_dir / filename, rows, fieldnames)

    status = decision_rows()[0]["decision"]
    payload = {
        "status": status,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(outputs),
        "B_mem": B_MEM,
        "L_H_Mpc": L_H_MPC,
        "half_factor_conditionally_derived": True,
        "same_domain_BAO_cancellation_conditionally_derived": True,
        "local_trace_source_silence_derived": False,
        "parent_selector_derived": False,
        "CMB_BAO_or_local_GR_claim_allowed": False,
        "next_target": "projected_trace_source_Ward_identity_or_demote_local_silence_to_closure",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(status + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Attempt a late-memory calibration projection derivation.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
