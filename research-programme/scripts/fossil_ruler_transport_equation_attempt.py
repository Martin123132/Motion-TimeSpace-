#!/usr/bin/env python3
"""Checkpoint 203: derive or bound fossil-ruler transport for BAO."""

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

CHECKPOINT_203_NAME = "fossil-ruler-transport-equation-attempt"
CHECKPOINT_202_RUN = RUNS_ROOT / "20260601-000019-late-common-mode-H0-rd-owner-derivation-attempt"
CHECKPOINT_198_RUN = RUNS_ROOT / "20260601-000015-BAO-radial-drift-and-alpha-owner-gate"
CHECKPOINT_197_RUN = RUNS_ROOT / "20260601-000014-BAO-common-mode-ratio-theorem-attempt"

STATUS = "fossil_ruler_transport_conditionally_derived_parent_matter_action_missing"
CLAIM_CEILING = "fossil_ruler_transport_internal_only_parent_matter_action_missing"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"
H0_BRIDGE_RESIDUAL_DOTC_OVER_H = -0.0004084189185673548
LOCKED_B_MEM = 2.0 / 27.0


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
        (Path(__file__).resolve(), "checkpoint 203 fossil-ruler transport script"),
        (WORK_DIR / "202-late-common-mode-H0-rd-owner-derivation-attempt.md", "previous late common-mode BAO owner checkpoint"),
        (CHECKPOINT_202_RUN / "status.json", "checkpoint 202 machine status"),
        (CHECKPOINT_202_RUN / "results" / "parent_transport_contract.csv", "checkpoint 202 parent transport contract"),
        (WORK_DIR / "197-BAO-common-mode-ratio-theorem-attempt.md", "BAO common-mode ratio theorem checkpoint"),
        (CHECKPOINT_197_RUN / "status.json", "checkpoint 197 machine status"),
        (CHECKPOINT_197_RUN / "results" / "BAO_leakage_tolerance.csv", "checkpoint 197 DESI DR2 leakage tolerance"),
        (WORK_DIR / "198-BAO-radial-drift-and-alpha-owner-gate.md", "BAO radial drift tolerance checkpoint"),
        (CHECKPOINT_198_RUN / "status.json", "checkpoint 198 machine status"),
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


def transport_equation_chain_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "statement": "Post-drag matter is described in the matter metric.",
            "equation": "tilde_g_mn = exp(C) g_mn",
            "derived_from": "checkpoint 194/197 conformal matter-observer map",
            "status": "metric_assumption_for_this_branch",
            "gap": "parent action must still select this coupling",
        },
        {
            "step": 2,
            "statement": "If matter couples diffeomorphism-invariantly to tilde_g_mn, the matter stress/current is conserved in that metric.",
            "equation": "tilde_nabla_m T_m^{mn}=0 and tilde_nabla_m J_m^m=0",
            "derived_from": "Noether/diffeomorphism identity of the matter sector",
            "status": "conditional_derivation",
            "gap": "requires an explicit parent matter action",
        },
        {
            "step": 3,
            "statement": "In the post-drag dust limit, matter worldlines carry conserved Lagrangian labels.",
            "equation": "u^m partial_m X^A = 0 for A=1,2,3",
            "derived_from": "dust flow plus conserved matter number current",
            "status": "conditional_derivation",
            "gap": "baryon pressure, slip, and shell crossing must be standard/shared corrections",
        },
        {
            "step": 4,
            "statement": "A pair of matter elements keeps its label-space separation under pure advection.",
            "equation": "D_t Delta X^A = 0",
            "derived_from": "subtract the two label advection equations",
            "status": "derived_under_pure_advection",
            "gap": "only exact before nonlinear relabeling/source terms",
        },
        {
            "step": 5,
            "statement": "The BAO peak is a maximum of the two-point function in label/comoving separation.",
            "equation": "partial_r xi(r,t)|_{r=r_BAO}=0",
            "derived_from": "definition of the acoustic correlation peak",
            "status": "definition",
            "gap": "peak fitting/reconstruction details are survey-model nuisances",
        },
        {
            "step": 6,
            "statement": "If the post-drag two-point function is only advected, the comoving BAO peak is transported exactly.",
            "equation": "(D_{t1}+D_{t2}) xi = 0 implies D_t r_BAO^comoving = 0",
            "derived_from": "label conservation plus source-free correlation advection",
            "status": "exact_zero_condition_derived",
            "gap": "must prove the source-free condition from the parent matter/ruler sector",
        },
        {
            "step": 7,
            "statement": "If there is a post-drag source S_xi, the peak drift is bounded by the slope of that source at the peak.",
            "equation": "D_t r_peak = - partial_r S_xi / partial_r^2 xi |_{r_peak}",
            "derived_from": "differentiate the peak condition partial_r xi(r_peak,t)=0",
            "status": "amplitude_law_derived",
            "gap": "S_xi must be computed or bounded for the actual parent theory",
        },
        {
            "step": 8,
            "statement": "The late physical ruler gets the same matter-unit factor as late matter distances.",
            "equation": "tilde_l_BAO = exp(C_obs/2) a r_BAO^comoving",
            "derived_from": "matter metric square-root length map",
            "status": "conditional_common_mode_projection",
            "gap": "requires homogeneous/saturated C over the survey patch",
        },
        {
            "step": 9,
            "statement": "BAO ratios are common-mode if the exact-zero or bounded-drift condition holds.",
            "equation": "tilde_D_X / tilde_r_BAO^late = D_X / r_BAO for X in {M,H,V}, up to dot_C/H and peak-drift leakage",
            "derived_from": "checkpoint 197 ratio theorem plus this transport law",
            "status": "conditional_BAO_ratio_theorem_strengthened",
            "gap": "not a public support claim until the parent action owns the assumptions",
        },
    ]


def lagrangian_label_condition_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition": "matter metric coupling",
            "mathematical_form": "S_matter[psi_m, tilde_g_mn] with tilde_g_mn=exp(C)g_mn",
            "needed_for": "Noether conservation in the matter frame",
            "current_status": "candidate_not_parent_derived",
            "failure_consequence": "transport theorem has no owner",
        },
        {
            "condition": "post-drag dust/geodesic limit",
            "mathematical_form": "T_m^{mn}=rho u^m u^n and u^m tilde_nabla_m u^n=0",
            "needed_for": "matter labels are carried by the flow",
            "current_status": "standard_late_matter_approximation",
            "failure_consequence": "pressure/slip can shift the BAO peak",
        },
        {
            "condition": "conserved matter labels",
            "mathematical_form": "u^m partial_m X^A=0",
            "needed_for": "Delta X^A is conserved for matter pairs",
            "current_status": "derived_if_current_conserved",
            "failure_consequence": "D_t r_BAO^comoving is not zero",
        },
        {
            "condition": "source-free post-drag correlation transport",
            "mathematical_form": "(D_{t1}+D_{t2})xi=0, or partial_r S_xi|peak=0",
            "needed_for": "exact BAO peak conservation",
            "current_status": "conditional_exact_zero",
            "failure_consequence": "peak-drift amplitude must be bounded",
        },
        {
            "condition": "homogeneous late C over BAO bin",
            "mathematical_form": "partial_i C approx 0 and |dot_C/H| below DESI radial tolerance",
            "needed_for": "same matter-unit factor for numerator and denominator",
            "current_status": "bounded_not_parent_derived",
            "failure_consequence": "D_H/r_d radial leakage appears",
        },
        {
            "condition": "standard nonlinear BAO shifts treated symmetrically",
            "mathematical_form": "reconstruction, bias, shell crossing, and damping are shared nuisance/modeling terms",
            "needed_for": "fair comparison with LambdaCDM/wCDM/CPL",
            "current_status": "policy_needed_for_tests",
            "failure_consequence": "MTS-only punishment or MTS-only rescue becomes possible",
        },
    ]


def BAO_peak_failure_mode_rows() -> list[dict[str, Any]]:
    return [
        {
            "failure_mode": "post-drag source in correlation evolution",
            "mathematical_signature": "S_xi != 0 and partial_r S_xi|peak != 0",
            "effect_on_BAO": "moves the label-space peak",
            "required_bound_or_fix": "|Delta r_BAO/r_BAO| below DESI leakage tolerance or derive partial_r S_xi=0",
            "status": "amplitude_law_available_source_missing",
        },
        {
            "failure_mode": "baryon-CDM relative slip after drag",
            "mathematical_signature": "u_b^m partial_m X_b^A != u_c^m partial_m X_c^A",
            "effect_on_BAO": "ruler is not carried by one conserved matter label",
            "required_bound_or_fix": "show slip corrections are standard/shared and not an MTS-only endpoint memory",
            "status": "standard_correction_owner_needed",
        },
        {
            "failure_mode": "pressure or acoustic remnants after drag",
            "mathematical_signature": "T_m^{mn} not dustlike; pressure-gradient forces in label equation",
            "effect_on_BAO": "continued propagation can shift peak",
            "required_bound_or_fix": "derive dust limit or include controlled source term in S_xi",
            "status": "open",
        },
        {
            "failure_mode": "nonlinear evolution and shell crossing",
            "mathematical_signature": "label map ceases to be one-to-one at small scales",
            "effect_on_BAO": "broadens/shifts BAO feature",
            "required_bound_or_fix": "treat as shared reconstruction/nonlinear BAO modeling, not as proof of MTS",
            "status": "shared_nuisance_policy",
        },
        {
            "failure_mode": "late C spatial gradients",
            "mathematical_signature": "partial_i C not negligible over survey volume",
            "effect_on_BAO": "anisotropic apparent ruler distortion",
            "required_bound_or_fix": "derive local/BAO-domain saturation or fit a constrained anisotropy branch",
            "status": "parent_local_silence_missing",
        },
        {
            "failure_mode": "late C time drift",
            "mathematical_signature": "dot_C/H not small",
            "effect_on_BAO": "radial D_H/r_d leakage",
            "required_bound_or_fix": "|dot_C/H| below checkpoint 198 tolerance",
            "status": "empirically_bounded_not_parent_derived",
        },
        {
            "failure_mode": "non-universal matter metric",
            "mathematical_signature": "different matter tracers couple to different tilde_g_mn",
            "effect_on_BAO": "late common-mode cancellation fails by tracer",
            "required_bound_or_fix": "parent action must enforce universal late matter coupling or predict violations",
            "status": "parent_action_contract",
        },
    ]


def observable_ratio_implication_rows() -> list[dict[str, Any]]:
    return [
        {
            "observable": "D_M/r_d",
            "transport_implication": "safe common-mode ratio if r_BAO^comoving is conserved and C is homogeneous",
            "leakage_form": "Delta(D_M/r_d)/(D_M/r_d) approx -Delta r_BAO/r_BAO",
            "test_status": "bounded_by_checkpoint_197_leakage_tolerance",
        },
        {
            "observable": "D_H/r_d",
            "transport_implication": "same as transverse, but with radial drift correction",
            "leakage_form": "Delta approx -Delta r_BAO/r_BAO - dot_C/(2H)",
            "test_status": "bounded_by_checkpoints_197_and_198",
        },
        {
            "observable": "D_V/r_d",
            "transport_implication": "inherits two transverse factors and one radial factor",
            "leakage_form": "Delta approx -Delta r_BAO/r_BAO - dot_C/(6H)",
            "test_status": "conditional_common_mode",
        },
        {
            "observable": "BAO alpha",
            "transport_implication": "late H0-r_d alpha is allowed only if the fossil ruler is transported into late matter units",
            "leakage_form": "alpha shifts if r_BAO^late is not the transported fossil ruler",
            "test_status": "shared_nuisance_until_parent_owned",
        },
        {
            "observable": "CMB theta_*",
            "transport_implication": "not governed by this late fossil-ruler rule",
            "leakage_form": "early-to-late endpoint memory remains separate",
            "test_status": "domain_separated_not_solved",
        },
        {
            "observable": "growth",
            "transport_implication": "two-point amplitude/growth evolution is not closed by peak-transport alone",
            "leakage_form": "requires perturbation equations and bias/reconstruction model",
            "test_status": "still_open",
        },
    ]


def transport_bound_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    leakage_rows = read_csv_rows(CHECKPOINT_197_RUN / "results" / "BAO_leakage_tolerance.csv")
    for row in leakage_rows:
        rows.append(
            {
                "bound_type": "isotropic_fossil_ruler_peak_drift",
                "threshold": row["delta_chi2_threshold"],
                "quantity": "max_abs_Delta_r_BAO_over_r_BAO",
                "value": row["max_abs_fractional_BAO_ratio_shift"],
                "source": "checkpoint_197_DESI_DR2_common_mode_leakage",
                "interpretation": "If the transported comoving BAO ruler drifts by more than this, all BAO ratios feel a denominator shift.",
            }
        )
    radial_rows = read_csv_rows(CHECKPOINT_198_RUN / "results" / "radial_drift_tolerance.csv")
    for row in radial_rows:
        if row["delta_chi2_threshold"] == "1.0":
            rows.append(
                {
                    "bound_type": f"radial_C_drift_{row['alpha_mode']}",
                    "threshold": row["delta_chi2_threshold"],
                    "quantity": "max_abs_dot_C_over_H",
                    "value": row["max_abs_dot_C_over_H"],
                    "source": "checkpoint_198_DESI_DR2_radial_drift_tolerance",
                    "interpretation": "Late matter-unit drift must stay below this for radial BAO to remain common-mode.",
                }
            )
    rows.append(
        {
            "bound_type": "H0_bridge_residual_radial_safety_check",
            "threshold": "checkpoint_198_fixed_alpha_delta_chi2_less_than_1",
            "quantity": "dot_C_over_H_residual",
            "value": H0_BRIDGE_RESIDUAL_DOTC_OVER_H,
            "source": "checkpoint_194_to_198_residual",
            "interpretation": "The small residual needed by the half-memory H0 bridge is safely below BAO radial tolerance, but this is not a parent derivation.",
        }
    )
    rows.append(
        {
            "bound_type": "full_memory_scale_radial_drift_rejected",
            "threshold": "comparison_scale",
            "quantity": "dot_C_over_H",
            "value": LOCKED_B_MEM,
            "source": "locked_B_mem_2_over_27",
            "interpretation": "A full memory-scale late drift is far too large for BAO radial ratios; saturation/local silence is required.",
        }
    )
    return rows


def parent_matter_action_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract": "universal matter metric",
            "required_statement": "all late BAO matter tracers couple to the same tilde_g_mn",
            "mathematical_form": "S_matter = integral L_m(psi_m, tilde_g_mn) sqrt(-tilde_g) d^4x",
            "what_it_would_prove": "late matter distances and late ruler use one common unit",
            "current_status": "not_yet_written_as_parent_action",
        },
        {
            "contract": "matter Noether identity",
            "required_statement": "diffeomorphism invariance in tilde_g_mn gives conservation",
            "mathematical_form": "tilde_nabla_m T_m^{mn}=0",
            "what_it_would_prove": "no unaccounted force term in the matter frame",
            "current_status": "conditional_standard_identity",
        },
        {
            "contract": "number current conservation",
            "required_statement": "post-drag matter number is conserved",
            "mathematical_form": "tilde_nabla_m(n u^m)=0",
            "what_it_would_prove": "matter labels can be defined and advected",
            "current_status": "conditional_standard_identity",
        },
        {
            "contract": "convective label action",
            "required_statement": "Lagrangian labels X^A are parent variables or derived hydrodynamic labels",
            "mathematical_form": "u^m partial_m X^A=0",
            "what_it_would_prove": "D_t Delta X^A=0 exactly in the source-free branch",
            "current_status": "derived_after_assuming_conserved_flow",
        },
        {
            "contract": "correlation source owner",
            "required_statement": "post-drag source S_xi vanishes at the BAO peak or is bounded",
            "mathematical_form": "partial_r S_xi|peak=0 or |partial_r S_xi/(r_peak partial_r^2 xi)| below tolerance",
            "what_it_would_prove": "D_t r_BAO^comoving=0 or acceptably small drift",
            "current_status": "main_theorem_debt",
        },
        {
            "contract": "domain selector",
            "required_statement": "same action classifies CMB as photon endpoint and BAO as late fossil-ruler readout",
            "mathematical_form": "observable map O -> {endpoint photon, late transported matter ruler, path perturbation}",
            "what_it_would_prove": "no post-hoc switching between CMB and BAO projection rules",
            "current_status": "rule_written_not_action_derived",
        },
    ]


def claim_gate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing = sum(row["exists"] != "yes" for row in source_rows)
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing == 0 else "fail",
            "evidence": f"missing={missing}",
            "claim_allowed": "internal derivation attempt",
        },
        {
            "gate": "label transport equation derived",
            "status": "conditional_pass",
            "evidence": "u^m partial_m X^A=0 implies D_t Delta X^A=0 for matter pairs",
            "claim_allowed": "conditional theorem piece",
        },
        {
            "gate": "exact fossil ruler zero condition derived",
            "status": "conditional_pass",
            "evidence": "(D_t1+D_t2)xi=0 implies D_t r_BAO^comoving=0",
            "claim_allowed": "exact only under source-free post-drag correlation transport",
        },
        {
            "gate": "amplitude law for nonzero source derived",
            "status": "pass",
            "evidence": "D_t r_peak = - partial_r S_xi / partial_r^2 xi at peak",
            "claim_allowed": "bound target",
        },
        {
            "gate": "parent matter action owns assumptions",
            "status": "fail",
            "evidence": "universal matter metric and S_xi owner are still contracts",
            "claim_allowed": "no promotion",
        },
        {
            "gate": "BAO support claim allowed",
            "status": "fail",
            "evidence": CLAIM_CEILING,
            "claim_allowed": "no",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "meaning": "Fossil-ruler transport is conditionally derived: conserved matter labels and source-free post-drag correlation advection give D_t r_BAO^comoving=0. If a source exists, the peak-drift amplitude law is explicit. The parent action still has to own universal matter coupling and the source-free/bounded S_xi condition.",
            "derived_zero_condition": "(D_t1+D_t2)xi=0 and u^m partial_m X^A=0 imply D_t r_BAO^comoving=0",
            "derived_amplitude_law": "D_t r_peak = - partial_r S_xi / partial_r^2 xi | peak",
            "main_blocker": "parent_matter_action_and_correlation_source_owner",
            "next_target": "204-matter-metric-action-and-ruler-transport-owner-contract.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_203_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    chain_rows = transport_equation_chain_rows()
    condition_rows = lagrangian_label_condition_rows()
    failure_rows = BAO_peak_failure_mode_rows()
    observable_rows = observable_ratio_implication_rows()
    bound_rows = transport_bound_rows()
    action_rows = parent_matter_action_contract_rows()
    gates = claim_gate_rows(source_rows)
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "transport_equation_chain.csv": (
            chain_rows,
            ["step", "statement", "equation", "derived_from", "status", "gap"],
        ),
        "lagrangian_label_conditions.csv": (
            condition_rows,
            ["condition", "mathematical_form", "needed_for", "current_status", "failure_consequence"],
        ),
        "BAO_peak_failure_modes.csv": (
            failure_rows,
            ["failure_mode", "mathematical_signature", "effect_on_BAO", "required_bound_or_fix", "status"],
        ),
        "observable_ratio_implications.csv": (
            observable_rows,
            ["observable", "transport_implication", "leakage_form", "test_status"],
        ),
        "transport_bound_summary.csv": (
            bound_rows,
            ["bound_type", "threshold", "quantity", "value", "source", "interpretation"],
        ),
        "parent_matter_action_contract.csv": (
            action_rows,
            ["contract", "required_statement", "mathematical_form", "what_it_would_prove", "current_status"],
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
                "derived_zero_condition",
                "derived_amplitude_law",
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
        "label_transport_equation_derived_conditionally": True,
        "exact_fossil_ruler_zero_condition_derived_conditionally": True,
        "peak_drift_amplitude_law_derived": True,
        "parent_matter_action_derived": False,
        "correlation_source_owner_derived": False,
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
