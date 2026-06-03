from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "projected-matter-metric-Cperp-decoupling-attempt"
STATUS = "projected_matter_metric_exact_Cperp_matter_decoupling_conditional_parent_projector_coupling_missing"
CLAIM_CEILING = "projected_matter_metric_internal_only_no_local_GR_CMB_or_BAO_promotion"

B_MEM = 2.0 / 27.0
C_KM_S = 299_792.458
H0_KM_S_MPC = 67.51
L_D_MPC = C_KM_S / H0_KM_S_MPC
LOCAL_DELTA_C_GATE = 4.6e-05
LOCAL_QR_GATE = 2.3e-05
BAO_DELTA_C_GATE = 0.005539695284669133
BAO_DOTC_OVER_H_BOUND = 0.011285628250379043


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
        (ROOT / "204-matter-metric-action-and-ruler-transport-owner-contract.md", "ordinary matter metric and label transport"),
        (ROOT / "207-domain-projector-action-and-Bianchi-identity.md", "action-level projector and Bianchi accounting"),
        (ROOT / "208-domain-representative-selection-law.md", "domain representative selector"),
        (ROOT / "265-late-memory-calibration-projection-derivation-attempt.md", "conformal calibration projection"),
        (ROOT / "266-projected-trace-source-Ward-identity-attempt.md", "trace projection and Cperp obstruction"),
        (ROOT / "scripts" / "projected_matter_metric_Cperp_decoupling_attempt.py", "this projected matter metric attempt"),
    ]
    return [
        {
            "source": relpath(path),
            "role": role,
            "exists": "yes" if path.exists() else "no",
        }
        for path, role in sources
    ]


def coupling_comparison_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch": "ordinary_local_C_metric",
            "matter_metric": "tilde_g_munu = exp(C_D + C_perp) g_munu",
            "delta_Sm_delta_CD": "1/2 P_D[sqrt(-tilde_g) T_tilde]",
            "delta_Sm_delta_Cperp": "1/2 (1-P_D)[sqrt(-tilde_g) T_tilde]",
            "local_trace_result": "unsafe",
            "meaning": "local trace contrast directly sources Cperp",
        },
        {
            "branch": "projected_matter_metric",
            "matter_metric": "tilde_g_munu = exp(P_D C) g_munu = exp(C_D) g_munu",
            "delta_Sm_delta_CD": "1/2 P_D[sqrt(-tilde_g_D) T_tilde_D]",
            "delta_Sm_delta_Cperp": "0",
            "local_trace_result": "conditional_pass",
            "meaning": "matter sees only the coherent projected mode; local trace cannot source Cperp through matter coupling",
        },
        {
            "branch": "epsilon_leak_metric",
            "matter_metric": "tilde_g_munu = exp(C_D + epsilon C_perp) g_munu",
            "delta_Sm_delta_CD": "1/2 P_D[sqrt(-tilde_g) T_tilde]",
            "delta_Sm_delta_Cperp": "epsilon/2 (1-P_D)[sqrt(-tilde_g) T_tilde]",
            "local_trace_result": "bounded_only",
            "meaning": "any residual Cperp matter coupling must be tiny enough to beat local gates",
        },
        {
            "branch": "hard_Cperp_zero_constraint",
            "matter_metric": "tilde_g_munu = exp(C_D) g_munu plus Cperp=0 constraint",
            "delta_Sm_delta_CD": "1/2 P_D[sqrt(-tilde_g_D) T_tilde_D]",
            "delta_Sm_delta_Cperp": "constraint stress only",
            "local_trace_result": "closure_risk",
            "meaning": "safe only if constraint stress is varied and not hidden",
        },
    ]


def variation_chain_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": "define_projected_matter_metric",
            "equation": "tilde_g_munu = exp(C_m) g_munu, C_m = P_D C = C_D",
            "status": "contract",
            "consequence": "matter metric excludes Cperp before variation",
        },
        {
            "step": "vary_Cperp",
            "equation": "delta C_m / delta Cperp = P_D[Cperp variation] = 0",
            "status": "conditional_derived",
            "consequence": "delta S_matter / delta Cperp = 0",
        },
        {
            "step": "vary_CD",
            "equation": "delta S_matter / delta C_D = 1/2 P_D[sqrt(-tilde_g_D) T_tilde_D]",
            "status": "conditional_derived",
            "consequence": "local compact sources enter only as domain average",
        },
        {
            "step": "local_connection",
            "equation": "partial_i C_D = 0 inside coherent local readout",
            "status": "conditional_derived",
            "consequence": "no local conformal spatial acceleration from C_D",
        },
        {
            "step": "BAO_common_mode",
            "equation": "tilde_D_X/tilde_r_BAO = exp(C_D/2)D_X / exp(C_D/2)r_BAO",
            "status": "conditional_derived",
            "consequence": "same-domain ratio cancellation survives",
        },
        {
            "step": "CMB_endpoint",
            "equation": "calibration contrast = exp((C_D,obs-C_D,emit)/2)",
            "status": "conditional_derived",
            "consequence": "endpoint contrast survives if endpoint selector is derived",
        },
        {
            "step": "Bianchi_accounting",
            "equation": "nabla_mu T_total^{mu nu}=0 with projector/domain stresses retained",
            "status": "conditional_previous",
            "consequence": "projected nonlocal coupling is allowed only with explicit domain stress bookkeeping",
        },
    ]


def epsilon_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "local_DeltaC_gate",
            "threshold": LOCAL_DELTA_C_GATE,
            "reference_unscreened_amplitude": B_MEM,
            "max_epsilon": LOCAL_DELTA_C_GATE / B_MEM,
            "meaning": "residual Cperp matter coupling must be below this fraction of a B_mem-scale response",
        },
        {
            "gate": "local_qR_like_gate",
            "threshold": LOCAL_QR_GATE,
            "reference_unscreened_amplitude": B_MEM,
            "max_epsilon": LOCAL_QR_GATE / B_MEM,
            "meaning": "stricter local proxy for residual response",
        },
        {
            "gate": "BAO_DeltaC_gate",
            "threshold": BAO_DELTA_C_GATE,
            "reference_unscreened_amplitude": B_MEM,
            "max_epsilon": BAO_DELTA_C_GATE / B_MEM,
            "meaning": "BAO spatial response is much less restrictive than local gates",
        },
        {
            "gate": "BAO_dotC_over_H_gate",
            "threshold": BAO_DOTC_OVER_H_BOUND,
            "reference_unscreened_amplitude": B_MEM,
            "max_epsilon": BAO_DOTC_OVER_H_BOUND / B_MEM,
            "meaning": "late drift still requires saturation or residual drift law",
        },
    ]


def volume_rows() -> list[dict[str, Any]]:
    probes = [
        ("1_Mpc", 1.0),
        ("50_Mpc", 50.0),
        ("150_Mpc_BAO", 150.0),
        ("300_Mpc", 300.0),
        ("1000_Mpc", 1000.0),
    ]
    rows: list[dict[str, Any]] = []
    for probe, length in probes:
        volume_fraction = (length / L_D_MPC) ** 3
        response = B_MEM * volume_fraction
        rows.append(
            {
                "probe": probe,
                "length_Mpc": length,
                "domain_volume_fraction": volume_fraction,
                "projected_CD_response": response,
                "below_local_DeltaC_gate": "yes" if response < LOCAL_DELTA_C_GATE else "no",
                "below_local_qR_gate": "yes" if response < LOCAL_QR_GATE else "no",
                "below_BAO_DeltaC_gate": "yes" if response < BAO_DELTA_C_GATE else "no",
            }
        )
    return rows


def theorem_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract": "P1_projector_before_matter_coupling",
            "required_form": "S_matter[psi, exp(P_D C) g_munu], not S_matter[psi, exp(C) g_munu]",
            "status": "new_conditional_contract",
            "risk_if_missing": "Cperp remains trace-sourced",
        },
        {
            "contract": "P2_projector_is_variational",
            "required_form": "P_D built from varied domain labels/weights and constraints",
            "status": "conditional_previous",
            "risk_if_missing": "nonlocal average inserted by hand",
        },
        {
            "contract": "P3_universal_projected_matter_metric",
            "required_form": "all late matter species see the same exp(C_D)g metric",
            "status": "contract",
            "risk_if_missing": "composition-dependent clocks/rulers and WEP danger",
        },
        {
            "contract": "P4_domain_stress_retained",
            "required_form": "T_total includes matter, C, projector, domain, auxiliary, and boundary stresses",
            "status": "conditional_previous",
            "risk_if_missing": "Bianchi identity faked",
        },
        {
            "contract": "P5_endpoint_domain_selector",
            "required_form": "derive when observables compare different C_D endpoints versus same-domain ratios",
            "status": "open",
            "risk_if_missing": "post-hoc CMB/BAO branch switching",
        },
        {
            "contract": "P6_transition_saturation",
            "required_form": "late |dot_C_D/H| below BAO drift bound while endpoint Delta C can remain B_mem",
            "status": "open",
            "risk_if_missing": "radial BAO drift failure",
        },
        {
            "contract": "P7_amplitude_scale_lock",
            "required_form": "derive B_mem=2/27 and Hstar=H0 or keep them closure-locked",
            "status": "not_derived",
            "risk_if_missing": "no parent amplitude promotion",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "ordinary_expC_metric",
            "result": "fail_as_lead",
            "evidence": "delta S_m/delta Cperp contains (1-P_D)T",
            "claim_effect": "ordinary local C matter coupling is not locally silent",
        },
        {
            "gate": "projected_expPD_C_metric",
            "result": "conditional_pass",
            "evidence": "delta S_m/delta Cperp = 0 by projection before matter coupling",
            "claim_effect": "Cperp matter-source obstruction removed if parent owns projected metric",
        },
        {
            "gate": "zero_mode_local_force",
            "result": "conditional_pass",
            "evidence": "partial_i C_D=0; compact response is volume-suppressed",
            "claim_effect": "coherent mode does not create a local spatial fifth force",
        },
        {
            "gate": "universal_late_matter_rulers",
            "result": "conditional_pass",
            "evidence": "same projected metric for all late matter preserves common-mode ruler cancellation",
            "claim_effect": "BAO late-ruler branch strengthened but not promoted",
        },
        {
            "gate": "projector_parent_origin",
            "result": "open",
            "evidence": "P_D coupling must come from parent action and domain labels",
            "claim_effect": "no field-theory completion claim",
        },
        {
            "gate": "late_drift_saturation",
            "result": "open",
            "evidence": "projected metric decouples Cperp but does not derive dot_C_D/H suppression",
            "claim_effect": "BAO/CMB bridge still not promoted",
        },
        {
            "gate": "support_claim_allowed",
            "result": "no",
            "evidence": "projector origin, endpoint selector, drift law, and amplitude lock remain open",
            "claim_effect": "no local-GR/CMB/BAO support claim",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "If matter couples to exp(P_D C)g rather than exp(C)g, the dangerous residual mode Cperp is not matter-sourced: "
                "delta S_m/delta Cperp = 0. This is a cleaner exact decoupling than a heavy scalar or hand plateau, but it is only "
                "a conditional parent-action contract until the projected matter metric, domain selector, Bianchi stresses, and drift law are derived."
            ),
            "next_target": "derive_projected_matter_metric_from_parent_action_or_reject_as_nonlocal_closure",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "coupling_comparison.csv": (
            coupling_comparison_rows(),
            ["branch", "matter_metric", "delta_Sm_delta_CD", "delta_Sm_delta_Cperp", "local_trace_result", "meaning"],
        ),
        "variation_chain.csv": (variation_chain_rows(), ["step", "equation", "status", "consequence"]),
        "epsilon_bounds.csv": (epsilon_bound_rows(), ["gate", "threshold", "reference_unscreened_amplitude", "max_epsilon", "meaning"]),
        "volume_suppression_bounds.csv": (
            volume_rows(),
            [
                "probe",
                "length_Mpc",
                "domain_volume_fraction",
                "projected_CD_response",
                "below_local_DeltaC_gate",
                "below_local_qR_gate",
                "below_BAO_DeltaC_gate",
            ],
        ),
        "theorem_contract.csv": (theorem_contract_rows(), ["contract", "required_form", "status", "risk_if_missing"]),
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
        "L_D_Mpc": L_D_MPC,
        "ordinary_expC_metric_leaves_Cperp_trace_source": True,
        "projected_metric_deltaSm_deltaCperp_zero": True,
        "projected_matter_metric_parent_derived": False,
        "late_drift_law_derived": False,
        "local_GR_CMB_or_BAO_claim_allowed": False,
        "next_target": "derive_projected_matter_metric_from_parent_action_or_reject_as_nonlocal_closure",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(status + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Projected matter metric Cperp decoupling attempt.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
