from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "projected-trace-source-Ward-identity-attempt"
STATUS = "projected_trace_source_Ward_identity_volume_suppression_derived_exact_silence_not_derived"
CLAIM_CEILING = "trace_projection_internal_only_no_local_GR_CMB_or_BAO_promotion"

B_MEM = 2.0 / 27.0
C_KM_S = 299_792.458
H0_KM_S_MPC = 67.51
L_D_MPC = C_KM_S / H0_KM_S_MPC
LOCAL_DELTA_C_GATE = 4.6e-05
LOCAL_QR_GATE = 2.3e-05
BAO_DELTA_C_GATE = 0.005539695284669133
BAO_DOTC_OVER_H_BOUND = 0.011285628250379043
AU_MPC = 1.0 / 206_264.80624709636 / 1_000_000.0
EARTH_RADIUS_MPC = 6_371.0 / 3.0856775814913673e19
SOLAR_RADIUS_MPC = 695_700.0 / 3.0856775814913673e19


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
        (ROOT / "204-matter-metric-action-and-ruler-transport-owner-contract.md", "matter metric / label transport owner"),
        (ROOT / "205-C-silence-source-bound-for-BAO-and-local-rulers.md", "conformal trace-source hazard and bounds"),
        (ROOT / "206-parent-C-screening-fixed-point-mechanism.md", "coherent zero-mode screening candidate"),
        (ROOT / "207-domain-projector-action-and-Bianchi-identity.md", "projector action and Bianchi accounting"),
        (ROOT / "208-domain-representative-selection-law.md", "domain representative selector"),
        (ROOT / "265-late-memory-calibration-projection-derivation-attempt.md", "late-memory projection theorem attempt"),
        (ROOT / "scripts" / "projected_trace_source_Ward_identity_attempt.py", "this Ward identity attempt"),
    ]
    return [
        {
            "source": relpath(path),
            "role": role,
            "exists": "yes" if path.exists() else "no",
        }
        for path, role in sources
    ]


def variation_identity_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": "matter_trace_variation",
            "identity": "delta S_m / delta C = 1/2 sqrt(-tilde_g) T_tilde",
            "derivation_status": "derived_previous",
            "meaning": "ordinary metric matter coupling sources a conformal C field through the matter trace",
        },
        {
            "step": "projector_split",
            "identity": "C(x)=C_D+C_perp(x), P_D[C_perp]=0",
            "derivation_status": "conditional_projector_action",
            "meaning": "the coherent zero mode and residual local modes are separated at action level",
        },
        {
            "step": "zero_mode_equation",
            "identity": "P_D[E_C]+1/2 P_D[sqrt(-tilde_g)T_tilde]=0",
            "derivation_status": "derived_from_variation",
            "meaning": "the projector alone does not annihilate trace source; it averages it into the domain equation",
        },
        {
            "step": "perp_equation",
            "identity": "(1-P_D)[E_C]+1/2(1-P_D)[sqrt(-tilde_g)T_tilde]=0",
            "derivation_status": "derived_from_variation",
            "meaning": "local trace contrast sources C_perp unless C_perp is constrained, heavy, or Ward-cancelled",
        },
        {
            "step": "volume_suppression",
            "identity": "delta C_D(local support L) ~ B_mem (L/L_D)^3",
            "derivation_status": "conditional_bound",
            "meaning": "a compact support source can only perturb the coherent average by its domain volume fraction",
        },
        {
            "step": "exact_Ward_route",
            "identity": "sqrt(-tilde_g)T_tilde = nabla_mu J_W^mu + A_top",
            "derivation_status": "theorem_target_not_derived",
            "meaning": "exact local silence would follow if compact local trace projects to boundary/topological zero",
        },
    ]


def route_scorecard_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "ordinary_local_C_scalar",
            "result": "rejected_as_lead",
            "reason": "local trace source produces local gradients unless extremely screened",
            "survives_as": "side route only with very stiff/heavy response",
        },
        {
            "route": "projector_only",
            "result": "partial",
            "reason": "splits average and contrast but does not make either source vanish",
            "survives_as": "formal bookkeeping, not exact silence",
        },
        {
            "route": "volume_suppressed_zero_mode",
            "result": "conditional_pass",
            "reason": "compact support perturbs C_D only by volume fraction and C_D has no spatial gradient",
            "survives_as": "best current local-silence bound if C_perp is also suppressed",
        },
        {
            "route": "Weyl_or_scale_Ward_identity",
            "result": "theorem_target",
            "reason": "trace as a divergence/topological residue could annihilate compact local projection",
            "survives_as": "cleanest exact silence route, parent action missing",
        },
        {
            "route": "topological_relative_class_projection",
            "result": "theorem_target",
            "reason": "compact local exact classes can have zero coherent charge while FLRW boundary class remains nonzero",
            "survives_as": "promising but not yet connected to matter trace",
        },
        {
            "route": "hard_Cperp_constraint",
            "result": "closure_risk",
            "reason": "can force local silence but risks becoming a plateau axiom",
            "survives_as": "allowed only if action and stresses are explicit",
        },
    ]


def volume_suppression_rows() -> list[dict[str, Any]]:
    probes = [
        ("Earth_radius", EARTH_RADIUS_MPC),
        ("Solar_radius", SOLAR_RADIUS_MPC),
        ("1_AU", AU_MPC),
        ("1_pc", 1.0e-6),
        ("8_kpc_galactic", 0.008),
        ("1_Mpc", 1.0),
        ("50_Mpc", 50.0),
        ("150_Mpc_BAO", 150.0),
        ("300_Mpc", 300.0),
        ("1000_Mpc", 1000.0),
    ]
    rows: list[dict[str, Any]] = []
    for probe, length_mpc in probes:
        volume_fraction = (length_mpc / L_D_MPC) ** 3
        delta_c = B_MEM * volume_fraction
        rows.append(
            {
                "probe": probe,
                "length_Mpc": length_mpc,
                "volume_fraction_vs_LD": volume_fraction,
                "Bmem_volume_suppressed_deltaC": delta_c,
                "below_local_deltaC_gate": "yes" if delta_c < LOCAL_DELTA_C_GATE else "no",
                "below_local_qR_gate": "yes" if delta_c < LOCAL_QR_GATE else "no",
                "below_BAO_deltaC_gate": "yes" if delta_c < BAO_DELTA_C_GATE else "no",
            }
        )
    return rows


def derived_bound_rows() -> list[dict[str, Any]]:
    local_delta_c_scale = L_D_MPC * (LOCAL_DELTA_C_GATE / B_MEM) ** (1.0 / 3.0)
    local_qr_scale = L_D_MPC * (LOCAL_QR_GATE / B_MEM) ** (1.0 / 3.0)
    bao_delta_c_scale = L_D_MPC * (BAO_DELTA_C_GATE / B_MEM) ** (1.0 / 3.0)
    drift_ratio = B_MEM / BAO_DOTC_OVER_H_BOUND
    return [
        {
            "quantity": "domain_scale_LD_Mpc",
            "value": L_D_MPC,
            "condition": "homogeneous Hubble-cap domain L_D=c/H0",
            "meaning": "predeclared coherent-domain scale for current bounds",
        },
        {
            "quantity": "max_L_for_volume_deltaC_below_local_gate_Mpc",
            "value": local_delta_c_scale,
            "condition": "B_mem*(L/L_D)^3 < 4.6e-05",
            "meaning": "compact supports below this scale are volume-suppressed below the local Delta C gate",
        },
        {
            "quantity": "max_L_for_volume_response_below_qR_gate_Mpc",
            "value": local_qr_scale,
            "condition": "B_mem*(L/L_D)^3 < 2.3e-05",
            "meaning": "same volume response under the stricter qR-like proxy",
        },
        {
            "quantity": "max_L_for_volume_response_below_BAO_deltaC_gate_Mpc",
            "value": bao_delta_c_scale,
            "condition": "B_mem*(L/L_D)^3 < 0.005539695284669133",
            "meaning": "BAO-scale compact support is safely below this volume bound",
        },
        {
            "quantity": "full_memory_drift_over_BAO_drift_bound",
            "value": drift_ratio,
            "condition": "B_mem / 0.011285628250379043",
            "meaning": "volume suppression does not solve late time drift; saturation/residual drift law still required",
        },
    ]


def ward_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract": "W1_projector_from_action",
            "required_form": "P_D defined by varied domain labels/weights, not post-solution averaging",
            "status": "conditional_previous",
            "failure_mode": "external projector violates Bianchi discipline",
        },
        {
            "contract": "W2_trace_as_exact_plus_topological",
            "required_form": "sqrt(-tilde_g)T_tilde = nabla_mu J_W^mu + A_top[D]",
            "status": "not_derived",
            "failure_mode": "ordinary massive matter trace remains a local C source",
        },
        {
            "contract": "W3_compact_local_boundary_zero",
            "required_form": "integral_D nabla_mu J_W^mu = boundary flux = 0 for stationary compact local domains",
            "status": "theorem_target",
            "failure_mode": "local systems excite coherent memory",
        },
        {
            "contract": "W4_FLRW_boundary_nonzero",
            "required_form": "A_top or domain boundary term survives for coherent FLRW expansion",
            "status": "theorem_target",
            "failure_mode": "same Ward identity kills the cosmological memory signal",
        },
        {
            "contract": "W5_Cperp_operator_suppression",
            "required_form": "(1-P_D)C response below local Delta C gate",
            "status": "open",
            "failure_mode": "local fifth-force/PPN branch fails",
        },
        {
            "contract": "W6_Bianchi_stress_retained",
            "required_form": "T_total includes matter, C, projector, domain, auxiliary, and boundary stresses",
            "status": "conditional_previous",
            "failure_mode": "hidden external force",
        },
        {
            "contract": "W7_transition_saturation",
            "required_form": "late |dot_C/H| below BAO bound while endpoint Delta C can remain B_mem",
            "status": "open",
            "failure_mode": "full rolling memory violates radial BAO drift gate",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "plain_trace_source_annihilated",
            "result": "fail",
            "evidence": "projected variation gives P_D[T], not zero",
            "claim_effect": "projector alone is insufficient",
        },
        {
            "gate": "zero_mode_volume_suppression",
            "result": "conditional_pass",
            "evidence": "compact support response scales like B_mem*(L/L_D)^3",
            "claim_effect": "local coherent response can be tiny if C_D is a real zero mode",
        },
        {
            "gate": "local_gradient_from_C_D",
            "result": "pass_conditional",
            "evidence": "grad_i C_D=0 by construction",
            "claim_effect": "zero-mode response does not create a spatial fifth force",
        },
        {
            "gate": "Cperp_trace_response",
            "result": "open",
            "evidence": "(1-P_D)T still sources residual mode unless constrained or Ward-cancelled",
            "claim_effect": "local GR/PPN not promoted",
        },
        {
            "gate": "exact_Ward_identity",
            "result": "not_derived",
            "evidence": "requires T = divergence + topological/domain term",
            "claim_effect": "exact local silence remains theorem target",
        },
        {
            "gate": "late_drift_safety",
            "result": "fail_if_unsaturated",
            "evidence": "B_mem / BAO drift bound is above unity",
            "claim_effect": "needs saturation/residual drift law",
        },
        {
            "gate": "support_claim_allowed",
            "result": "no",
            "evidence": "exact Ward identity and Cperp suppression missing",
            "claim_effect": "no local-GR, CMB, or BAO promotion",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "Variation of a projected C field proves the projector alone does not annihilate local trace sources. "
                "It does derive a useful volume-suppressed coherent zero-mode response, and C_D has no spatial gradient, "
                "but exact local silence still needs a Ward/topological trace identity or a derived C_perp suppression operator."
            ),
            "next_target": "derive_Cperp_response_operator_or_Weyl_topological_trace_current",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "variation_identity.csv": (variation_identity_rows(), ["step", "identity", "derivation_status", "meaning"]),
        "route_scorecard.csv": (route_scorecard_rows(), ["route", "result", "reason", "survives_as"]),
        "volume_suppression_bounds.csv": (
            volume_suppression_rows(),
            [
                "probe",
                "length_Mpc",
                "volume_fraction_vs_LD",
                "Bmem_volume_suppressed_deltaC",
                "below_local_deltaC_gate",
                "below_local_qR_gate",
                "below_BAO_deltaC_gate",
            ],
        ),
        "derived_bounds.csv": (derived_bound_rows(), ["quantity", "value", "condition", "meaning"]),
        "Ward_contract.csv": (ward_contract_rows(), ["contract", "required_form", "status", "failure_mode"]),
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
        "projector_annihilates_plain_trace_source": False,
        "volume_suppressed_zero_mode_response": True,
        "exact_Ward_identity_derived": False,
        "Cperp_suppression_derived": False,
        "local_GR_CMB_or_BAO_claim_allowed": False,
        "next_target": "derive_Cperp_response_operator_or_Weyl_topological_trace_current",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(status + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Projected trace-source Ward identity attempt.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
