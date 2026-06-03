#!/usr/bin/env python3
"""Lock the post-checkpoint CMB-compatible MTS limit contract."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SOURCE_33_STATUS = Path("runs/20260531-003140-CMB-calibration-freedom-audit/status.json")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def early_time_limit_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition": "memory_decoupling_or_absorption",
            "required_form": "f_Gamma(z_star) -> 0, or its nonzero part must be absorbed into declared calibrated matter/radiation densities",
            "success_test": "derive a bound on |Omega_Gamma(z_star)| or a parameter map that preserves the CMB distance-prior definitions",
            "current_status": "not_derived",
        },
        {
            "condition": "sound_horizon_consistency",
            "required_form": "r_s(z_star)=int_{0}^{a_star} c_s(a)/(a^2 H(a)) da with declared baryon loading and radiation content",
            "success_test": "scale-factor quadrature or official Boltzmann likelihood replaces finite redshift cutoff artifacts",
            "current_status": "test_convention_fixed_not_parent_derived",
        },
        {
            "condition": "shift_parameter_consistency",
            "required_form": "R=sqrt(Omega_m0) H0 D_M(z_star)/c uses the same calibrated Omega_m0/H0 meaning in background and CMB branches",
            "success_test": "no silent switch between late-time fitted matter and early-time physical matter",
            "current_status": "contract_required",
        },
        {
            "condition": "acoustic_scale_consistency",
            "required_form": "l_A=pi D_M(z_star)/r_s(z_star) must use the same distance and sound-horizon convention for baselines and C0",
            "success_test": "same code path and calibration-variable treatment for LCDM/wCDM/CPL/C0",
            "current_status": "implemented_as_test_convention",
        },
        {
            "condition": "perturbation_closure",
            "required_form": "c_s2_Gamma=1, pi_Gamma=0, Q_m_nu=0 unless parent perturbation action derives otherwise",
            "success_test": "no CMB rescue through late-added perturbation knobs",
            "current_status": "closure_only",
        },
    ]


def calibration_variable_rows() -> list[dict[str, Any]]:
    return [
        {
            "variable": "H0",
            "allowed_in_secondary_CMB_calibration": True,
            "parent_requirement": "derive whether H0 is a local calibration, global background parameter, or projection of motion-load variables",
            "claim_limit": "CMB retuning, not local-H0 evidence",
        },
        {
            "variable": "Omega_m0",
            "allowed_in_secondary_CMB_calibration": True,
            "parent_requirement": "define whether calibrated matter includes absorbed memory contribution",
            "claim_limit": "calibrated density bookkeeping, not derivation",
        },
        {
            "variable": "b_mem",
            "allowed_in_secondary_CMB_calibration": True,
            "parent_requirement": "derive sign/range/magnitude from parent memory budget before support claim",
            "claim_limit": "count as fitted C0 parameter in AIC/BIC",
        },
        {
            "variable": "alpha_act, nu_act",
            "allowed_in_secondary_CMB_calibration": "stress_only",
            "parent_requirement": "derive transition shape from parent dynamics before using as evidence",
            "claim_limit": "shape-free branch cannot support theory",
        },
        {
            "variable": "Omega_b h^2, n_s, N_eff",
            "allowed_in_secondary_CMB_calibration": False,
            "parent_requirement": "official likelihood or explicit early-universe sector required before varying",
            "claim_limit": "fixed in lightweight distance-prior branch",
        },
    ]


def branch_status_rows(source_33: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "branch": "fixed_no_SH0ES_C0_growth_CMB",
            "status": "demoted",
            "evidence": f"fixed C0 CMB chi2={source_33.get('fixed_C0_CMB_chi2')}",
            "allowed_claim": "growth-only subdiagnostic; repaired fixed CMB tension",
        },
        {
            "branch": "equal_two_parameter_CMB_calibration",
            "status": "non_discriminating_distance_prior_stress",
            "evidence": f"C0 equal two-parameter delta AIC={source_33.get('C0_equal_two_parameter_delta_AIC')}",
            "allowed_claim": "compressed CMB priors can be calibrated by multiple branches",
        },
        {
            "branch": "native_C0_CMB_calibrated_frozen_shape",
            "status": "secondary_closure_only",
            "evidence": f"C0 native calibrated delta AIC={source_33.get('C0_native_calibrated_delta_AIC')}",
            "allowed_claim": "possible missing calibration/early-limit relation",
        },
        {
            "branch": "shape_free_CMB_calibrated",
            "status": "stress_only",
            "evidence": "alpha_act and nu_act are not parent-derived",
            "allowed_claim": "none beyond parameter-space diagnostic",
        },
        {
            "branch": "official_CMB_likelihood",
            "status": "not_implemented",
            "evidence": "current tests use compressed distance priors",
            "allowed_claim": "none yet",
        },
    ]


def derivation_obligation_rows() -> list[dict[str, Any]]:
    return [
        {
            "obligation": "derive_or_bound_memory_at_recombination",
            "question": "Does the MTS memory contribution vanish at z_star, or is it absorbed into effective matter/radiation variables?",
            "acceptance_test": "analytic inequality or parent-action projection that fixes Omega_Gamma(z_star) treatment",
            "failure_label": "CMB_calibration_phenomenology_only",
        },
        {
            "obligation": "derive_calibrated_parameter_map",
            "question": "How do H0, Omega_m0, and b_mem map from parent fields across SN/BAO/growth/CMB splits?",
            "acceptance_test": "single parameter map used consistently across background and CMB branches",
            "failure_label": "post_hoc_CMB_recalibration",
        },
        {
            "obligation": "derive_joint_growth_CMB_limit",
            "question": "Can the same parameters retain near-competitive growth and calibrated CMB distance behavior?",
            "acceptance_test": "same parameter count and same baseline treatment; no CMB-only rescue freedoms",
            "failure_label": "split_success_only",
        },
        {
            "obligation": "official_likelihood_upgrade",
            "question": "Does any branch survive beyond compressed Planck distance priors?",
            "acceptance_test": "predeclared official Planck/ACT likelihood workflow or documented blocker",
            "failure_label": "compressed_CMB_only",
        },
    ]


def gate_rows(source_33: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate": "source_33_complete",
            "status": "pass" if source_33.get("readout") == "CMB_calibration_freedom_changes_C0_status_but_parent_limit_missing" else "fail",
            "detail": str(source_33.get("readout")),
        },
        {
            "gate": "early_time_conditions_locked",
            "status": "pass",
            "detail": "memory, sound-horizon, shift-parameter, acoustic-scale, and perturbation conditions listed",
        },
        {
            "gate": "calibration_variables_labeled",
            "status": "pass",
            "detail": "H0, Omega_m0, b_mem, shape, and early-universe variables separated",
        },
        {
            "gate": "derivation_obligations_locked",
            "status": "pass",
            "detail": "memory recombination bound, parameter map, joint limit, and official likelihood obligations listed",
        },
        {
            "gate": "CMB_support_claim_allowed",
            "status": "fail",
            "detail": "parent early-time/calibration derivation missing",
        },
        {
            "gate": "public_claim_allowed",
            "status": "fail",
            "detail": "official CMB likelihood missing",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Post-checkpoint CMB-compatible MTS limit contract.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    source_33 = load_json(root / SOURCE_33_STATUS)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or root / "runs" / f"{timestamp}-CMB-compatible-MTS-limit-contract"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    early_limits = early_time_limit_rows()
    calibration_variables = calibration_variable_rows()
    branch_status = branch_status_rows(source_33)
    derivation_obligations = derivation_obligation_rows()
    gates = gate_rows(source_33)

    write_csv(results_dir / "early_time_limit_conditions.csv", early_limits, list(early_limits[0].keys()))
    write_csv(results_dir / "calibration_variable_contract.csv", calibration_variables, list(calibration_variables[0].keys()))
    write_csv(results_dir / "branch_status_contract.csv", branch_status, list(branch_status[0].keys()))
    write_csv(results_dir / "derivation_obligations.csv", derivation_obligations, list(derivation_obligations[0].keys()))
    write_csv(results_dir / "contract_gate_criteria.csv", gates, list(gates[0].keys()))

    readout = "CMB_compatible_MTS_limit_contract_locked_parent_derivation_required"
    status = {
        "status": "complete_CMB_compatible_MTS_limit_contract",
        "readout": readout,
        "recommendation": "attempt_early_time_decoupling_or_calibration_derivation_next",
        "next_target": "35-early-time-decoupling-or-calibration-derivation.md",
        "primary_fixed_background_status": "demoted",
        "secondary_calibrated_status": "closure_only_not_support",
        "public_claim_allowed": False,
        "C0_support_claim_allowed": False,
        "C0_death_claim_allowed": False,
        "required_derivation_count": len(derivation_obligations),
        "outputs": {
            "early_time_limit_conditions": str(results_dir / "early_time_limit_conditions.csv"),
            "calibration_variable_contract": str(results_dir / "calibration_variable_contract.csv"),
            "branch_status_contract": str(results_dir / "branch_status_contract.csv"),
            "derivation_obligations": str(results_dir / "derivation_obligations.csv"),
            "contract_gate_criteria": str(results_dir / "contract_gate_criteria.csv"),
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
