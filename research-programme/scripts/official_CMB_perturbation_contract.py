#!/usr/bin/env python3
"""Define the honest contract for an official CMB spectra/lensing stress."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]

SOURCE_PATHS = {
    "34_status": Path("runs/20260531-003434-CMB-compatible-MTS-limit-contract/status.json"),
    "38_status": Path("runs/20260531-005438-calibrated-closure-holdout-contract/status.json"),
    "40_status": Path("runs/20260531-010340-fresh-holdout-or-official-likelihood-roadmap/status.json"),
    "40_official_refs": Path(
        "runs/20260531-010340-fresh-holdout-or-official-likelihood-roadmap/results/"
        "official_likelihood_reference_register.csv"
    ),
    "42_status": Path("runs/20260531-011514-calibrated-closure-candidate-ledger/status.json"),
    "42_missing_gates": Path(
        "runs/20260531-011514-calibrated-closure-candidate-ledger/results/missing_promotion_gates.csv"
    ),
}


def absolute_source(key: str) -> Path:
    return POST_CHECKPOINT / SOURCE_PATHS[key]


def load_json(key: str) -> dict[str, Any]:
    return json.loads(absolute_source(key).read_text(encoding="utf-8"))


def read_csv(key: str) -> list[dict[str, str]]:
    with absolute_source(key).open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, relative_path in SOURCE_PATHS.items():
        absolute_path = POST_CHECKPOINT / relative_path
        rows.append(
            {
                "source_key": key,
                "relative_path": str(relative_path),
                "absolute_path": str(absolute_path),
                "exists": absolute_path.exists(),
            }
        )
    missing = [row["absolute_path"] for row in rows if not row["exists"]]
    if missing:
        raise FileNotFoundError("missing source files: " + "; ".join(missing))
    return rows


def frozen_background_rows(source_38: dict[str, Any]) -> list[dict[str, Any]]:
    params = json.loads(source_38["frozen_params_json"])
    rows = []
    for name in ["h0", "omega_m0", "b_mem", "alpha_act", "nu_act", "rd"]:
        rows.append(
            {
                "quantity": name,
                "value": params[name],
                "status": "frozen",
                "source": str(absolute_source("38_status")),
                "role": "background_closure_parameter",
                "may_move_in_official_CMB_stress": False,
                "notes": "changing this is parameter rescue and invalidates fixed-row stress",
            }
        )
    return rows


def perturbation_variable_rows() -> list[dict[str, Any]]:
    return [
        {
            "block": "metric",
            "symbol_or_variable": "Phi, Psi or h, eta",
            "required_definition": "choose Newtonian or synchronous gauge variables and supply exact mapping",
            "current_status": "missing",
            "must_be_parent_derived": True,
            "failure_if_absent": "official spectra/lensing cannot be support; background-only stress at most",
            "observable_link": "TT, TE, EE, lensing, ISW",
        },
        {
            "block": "standard_species",
            "symbol_or_variable": "delta_i, theta_i, sigma_i for photons, baryons, CDM, neutrinos",
            "required_definition": "state whether standard Boltzmann hierarchy and conservation equations are unchanged",
            "current_status": "implicit_standard_assumption_only",
            "must_be_parent_derived": False,
            "failure_if_absent": "cannot tell whether CMB changes are MTS physics or borrowed GR closure",
            "observable_link": "acoustic peaks, damping tail, polarization",
        },
        {
            "block": "memory_background",
            "symbol_or_variable": "F(N), b_mem, alpha_act, nu_act",
            "required_definition": "fixed background activation already defined; perturbation response still required",
            "current_status": "background_defined_perturbation_missing",
            "must_be_parent_derived": True,
            "failure_if_absent": "compressed distance calibration remains closure-only",
            "observable_link": "theta_star, r_s, late ISW, lensing kernel",
        },
        {
            "block": "memory_perturbation",
            "symbol_or_variable": "delta F, delta b_mem, delta Gamma_eff, delta q_mem",
            "required_definition": "derive whether memory clusters, remains homogeneous, or is constrained by a field equation",
            "current_status": "missing",
            "must_be_parent_derived": True,
            "failure_if_absent": "growth/lensing response is arbitrary",
            "observable_link": "CMB lensing phi-phi, matter growth, ISW",
        },
        {
            "block": "constraint_equations",
            "symbol_or_variable": "modified Poisson, slip, momentum, anisotropic-stress relations",
            "required_definition": "write scalar constraints that close the metric potentials without extra fitted knobs",
            "current_status": "missing",
            "must_be_parent_derived": True,
            "failure_if_absent": "Boltzmann solver cannot be made predictive",
            "observable_link": "peak heights, lensing smoothing, growth",
        },
        {
            "block": "conservation",
            "symbol_or_variable": "nabla_mu T_eff^{mu nu}=0 or source-exchange law",
            "required_definition": "state the Bianchi-compatible exchange between matter, memory, and geometry",
            "current_status": "missing",
            "must_be_parent_derived": True,
            "failure_if_absent": "numerical spectra may violate consistency identities",
            "observable_link": "all spectra and background consistency",
        },
        {
            "block": "initial_conditions",
            "symbol_or_variable": "superhorizon adiabatic/isocurvature modes",
            "required_definition": "derive early-time limits for memory perturbations and standard species",
            "current_status": "missing",
            "must_be_parent_derived": True,
            "failure_if_absent": "primary CMB peaks are not well-defined",
            "observable_link": "low-ell and acoustic phase",
        },
        {
            "block": "lensing",
            "symbol_or_variable": "W_lens(z), Phi+Psi, growth response",
            "required_definition": "derive how the frozen background and perturbations project into CMB lensing",
            "current_status": "missing",
            "must_be_parent_derived": True,
            "failure_if_absent": "ACT/Planck lensing cannot be interpreted",
            "observable_link": "CMB lensing reconstruction and peak smoothing",
        },
    ]


def standard_parameter_policy_rows() -> list[dict[str, Any]]:
    return [
        {
            "parameter_group": "primordial_spectrum",
            "examples": "A_s, n_s, k_pivot, tau_reio",
            "policy": "fix to the selected baseline reference or marginalize identically for all branches",
            "claim_status": "not_MTS_evidence_if_tuned",
            "reason": "spectra need these parameters but they are not yet parent-derived by MTS",
        },
        {
            "parameter_group": "baryon_and_radiation_sector",
            "examples": "omega_b h^2, T_CMB, N_eff, Y_p, sum_mnu",
            "policy": "lock to baseline/reference values unless a parent derivation is supplied",
            "claim_status": "shared_standard_physics_only",
            "reason": "changing these can mimic peak and damping effects",
        },
        {
            "parameter_group": "background_MTS_row",
            "examples": "h0, omega_m0, b_mem, alpha_act, nu_act, rd",
            "policy": "must remain frozen from checkpoint 38",
            "claim_status": "fixed_closure_row",
            "reason": "moving these after CMB inspection is rescue",
        },
        {
            "parameter_group": "instrument_and_foreground_nuisance",
            "examples": "calibration, beam, foreground amplitudes",
            "policy": "allowed only if identical to the official baseline likelihood treatment",
            "claim_status": "nuisance_not_theory",
            "reason": "official likelihoods require nuisance handling but it must not favor MTS",
        },
        {
            "parameter_group": "phenomenological_lensing_rescue",
            "examples": "A_L, arbitrary mu(k,a), arbitrary Sigma(k,a)",
            "policy": "forbidden for promotion runs",
            "claim_status": "rescue_knob",
            "reason": "would hide perturbation failure rather than test the theory",
        },
    ]


def observable_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "observable": "C_l^TT",
            "required_theory_inputs": "background, metric potentials, photon hierarchy, initial conditions",
            "minimal_acceptance": "baseline pipeline reproduction first; then fixed-row MTS evaluated with same likelihood",
            "current_status": "blocked_by_perturbation_contract",
            "claim_limit_until_unblocked": "no_support_claim",
        },
        {
            "observable": "C_l^TE",
            "required_theory_inputs": "same as TT plus polarization source evolution",
            "minimal_acceptance": "same nuisance and masks as baseline",
            "current_status": "blocked_by_perturbation_contract",
            "claim_limit_until_unblocked": "no_support_claim",
        },
        {
            "observable": "C_l^EE",
            "required_theory_inputs": "reionization, polarization source evolution, optical depth policy",
            "minimal_acceptance": "tau/A_s policy predeclared",
            "current_status": "blocked_by_standard_parameter_policy",
            "claim_limit_until_unblocked": "no_support_claim",
        },
        {
            "observable": "CMB lensing phi-phi or convergence likelihood",
            "required_theory_inputs": "Phi+Psi, growth response, lensing kernel, nonlinear policy",
            "minimal_acceptance": "no A_L rescue; same lensing likelihood for baselines and MTS",
            "current_status": "blocked_by_memory_perturbation_closure",
            "claim_limit_until_unblocked": "no_support_claim",
        },
        {
            "observable": "derived theta_star, r_s, D_M(z_star)",
            "required_theory_inputs": "background and sound-horizon convention",
            "minimal_acceptance": "already compressed-tested but not sufficient",
            "current_status": "guardrail_only",
            "claim_limit_until_unblocked": "closure_only",
        },
        {
            "observable": "late ISW and low-ell response",
            "required_theory_inputs": "time evolution of Phi and Psi under MTS memory",
            "minimal_acceptance": "no arbitrary late-time potential damping",
            "current_status": "missing",
            "claim_limit_until_unblocked": "no_support_claim",
        },
    ]


def no_new_knob_rows() -> list[dict[str, Any]]:
    return [
        {
            "rule": "frozen_background",
            "status": "required",
            "allowed": "use checkpoint-38 h0, omega_m0, b_mem, alpha_act, nu_act, rd",
            "forbidden": "refit any frozen background parameter after seeing spectra/lensing",
            "consequence_if_broken": "run becomes tuning diagnostic only",
        },
        {
            "rule": "same_baseline_treatment",
            "status": "required",
            "allowed": "same likelihood, masks, nuisance priors, and standard-parameter policy for all branches",
            "forbidden": "MTS-only nuisance freedom or different data cuts",
            "consequence_if_broken": "comparison invalid",
        },
        {
            "rule": "no_lensing_fudge",
            "status": "required",
            "allowed": "parent-derived lensing response",
            "forbidden": "A_L or arbitrary Sigma/mu rescue in promotion run",
            "consequence_if_broken": "perturbation failure is hidden",
        },
        {
            "rule": "no_after_the_fact_thresholds",
            "status": "required",
            "allowed": "predeclared pass/tension/demotion bands",
            "forbidden": "choosing thresholds after results are known",
            "consequence_if_broken": "no evidence claim",
        },
        {
            "rule": "background_only_run_label",
            "status": "required_if_used",
            "allowed": "label as failure screen only",
            "forbidden": "calling GR-perturbation-on-MTS-background a parent-derived MTS prediction",
            "consequence_if_broken": "category error",
        },
    ]


def run_mode_rows() -> list[dict[str, Any]]:
    return [
        {
            "mode": "compressed_CMB_distance",
            "can_run_now": True,
            "support_claim_allowed": False,
            "role": "already used closure diagnostic",
            "blocker": "not spectra/lensing and can be calibrated",
            "next_action": "do not repeat as promotion evidence",
        },
        {
            "mode": "official_background_only_GR_perturbation_stress",
            "can_run_now": False,
            "support_claim_allowed": False,
            "role": "possible kill-screen if implemented carefully",
            "blocker": "tooling not installed and GR perturbations would be borrowed closure",
            "next_action": "only build if explicitly labelled non-support",
        },
        {
            "mode": "official_parent_perturbation_CMB_stress",
            "can_run_now": False,
            "support_claim_allowed": False,
            "role": "first meaningful official CMB promotion route",
            "blocker": "parent perturbation closure missing",
            "next_action": "derive minimum perturbation closure before setup",
        },
        {
            "mode": "official_lensing_fixed_parameter_stress",
            "can_run_now": False,
            "support_claim_allowed": False,
            "role": "high-leverage lensing/growth consistency test",
            "blocker": "Phi+Psi and memory clustering response missing",
            "next_action": "derive lensing response or use as background-only demotion screen",
        },
        {
            "mode": "fresh_external_growth_holdout",
            "can_run_now": False,
            "support_claim_allowed": False,
            "role": "non-CMB independent empirical pillar",
            "blocker": "manifest and data acquisition not yet locked",
            "next_action": "predeclare dataset and fixed-row thresholds before download/run",
        },
    ]


def pass_fail_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "source_42_complete",
            "status": "pass",
            "test": "checkpoint 42 readout is closure candidate retained, not evidence",
            "pass_condition": "source status exists and support_claim_allowed is false",
            "fail_or_demote_condition": "source missing or already overclaimed",
        },
        {
            "gate": "perturbation_contract_complete",
            "status": "fail_now",
            "test": "all mandatory metric, memory, conservation, initial-condition, and lensing rows are derived",
            "pass_condition": "no mandatory row remains missing",
            "fail_or_demote_condition": "run may proceed only as background-only failure screen",
        },
        {
            "gate": "baseline_reproduction",
            "status": "not_run",
            "test": "official pipeline reproduces a reference LambdaCDM likelihood/spectrum before MTS",
            "pass_condition": "reference agreement documented in setup manifest",
            "fail_or_demote_condition": "pipeline invalid; do not interpret MTS result",
        },
        {
            "gate": "fixed_row_no_rescue",
            "status": "contract_locked",
            "test": "checkpoint-38 background row unchanged and no MTS-only nuisance knobs added",
            "pass_condition": "all frozen values match source manifest",
            "fail_or_demote_condition": "result becomes tuning diagnostic only",
        },
        {
            "gate": "official_CMB_delta_chi2_band",
            "status": "predeclared_not_run",
            "test": "compare fixed-row MTS to matched best baseline under the same likelihood",
            "pass_condition": "Delta chi2 <= 10 with no hidden rescue, then retain for further tests only",
            "fail_or_demote_condition": "Delta chi2 > 25 demotes the CMB-calibrated branch; 10 < Delta chi2 <= 25 marks serious tension",
        },
        {
            "gate": "evidence_language",
            "status": "forbidden_now",
            "test": "whether official CMB, fresh holdout, parent map, and local GR/PPN gates all pass",
            "pass_condition": "multiple promotion gates pass together",
            "fail_or_demote_condition": "until then say retained closure candidate only",
        },
    ]


def setup_manifest_rows(ref_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for ref in ref_rows:
        rows.append(
            {
                "item": ref["component"],
                "source": ref["source"],
                "url": ref["url"],
                "current_local_status": ref["local_status"],
                "required_before_run": ref["requirement_before_run"],
                "output_required": "setup manifest entry with version/hash/path before any long run",
            }
        )
    rows.extend(
        [
            {
                "item": "run_directory_protocol",
                "source": "local workflow",
                "url": "",
                "current_local_status": "defined_by_contract",
                "required_before_run": "write runs/<timestamp>/log.txt, status.json, DONE.txt, configs, and copied data manifests",
                "output_required": "no hour-long watched run; user prompts Codex after DONE marker",
            },
            {
                "item": "baseline_config",
                "source": "local workflow",
                "url": "",
                "current_local_status": "missing",
                "required_before_run": "write baseline and MTS configs side by side before execution",
                "output_required": "config diff proves only allowed theory branch changes",
            },
            {
                "item": "failure_screen_label",
                "source": "local workflow",
                "url": "",
                "current_local_status": "required",
                "required_before_run": "declare whether run is promotion-capable or kill-screen-only",
                "output_required": "claim language automatically inherited from run mode",
            },
        ]
    )
    return rows


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "official_CMB_contract_status",
            "status": "contract_written_run_not_ready",
            "evidence": "mandatory perturbation, conservation, initial-condition, and lensing closures are missing",
            "next_action": "derive minimum parent perturbation closure or run only a labelled background failure screen",
        },
        {
            "decision": "support_claim_status",
            "status": "forbidden",
            "evidence": "checkpoint 42 is retained closure candidate only and official CMB is not implemented",
            "next_action": "keep all CMB language internal and conditional",
        },
        {
            "decision": "recommended_next_target",
            "status": "44-minimal-CMB-perturbation-closure-attempt.md",
            "evidence": "official CMB stress cannot become meaningful until the perturbation sector exists",
            "next_action": "attempt the minimal scalar/lensing closure; if it fails, label official CMB as kill-screen-only",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Official CMB perturbation contract.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    source_register = source_register_rows()
    source_38 = load_json("38_status")
    source_42 = load_json("42_status")
    ref_rows = read_csv("40_official_refs")
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or POST_CHECKPOINT / "runs" / f"{timestamp}-official-CMB-perturbation-contract"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    frozen = frozen_background_rows(source_38)
    perturbations = perturbation_variable_rows()
    standard_policy = standard_parameter_policy_rows()
    observables = observable_contract_rows()
    no_knobs = no_new_knob_rows()
    modes = run_mode_rows()
    gates = pass_fail_gate_rows()
    setup = setup_manifest_rows(ref_rows)
    decisions = decision_rows()

    write_csv(results_dir / "source_checkpoint_register.csv", source_register, list(source_register[0].keys()))
    write_csv(results_dir / "frozen_background_manifest.csv", frozen, list(frozen[0].keys()))
    write_csv(results_dir / "perturbation_variable_contract.csv", perturbations, list(perturbations[0].keys()))
    write_csv(results_dir / "standard_parameter_policy.csv", standard_policy, list(standard_policy[0].keys()))
    write_csv(results_dir / "CMB_observable_contract.csv", observables, list(observables[0].keys()))
    write_csv(results_dir / "no_new_knob_policy.csv", no_knobs, list(no_knobs[0].keys()))
    write_csv(results_dir / "official_CMB_run_mode_register.csv", modes, list(modes[0].keys()))
    write_csv(results_dir / "official_CMB_pass_fail_gates.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "official_CMB_setup_manifest.csv", setup, list(setup[0].keys()))
    write_csv(results_dir / "decision.csv", decisions, list(decisions[0].keys()))

    mandatory_missing = sum(1 for row in perturbations if row["current_status"] in {"missing", "background_defined_perturbation_missing"})
    status = {
        "status": "complete_official_CMB_perturbation_contract",
        "readout": "official_CMB_contract_written_perturbation_closure_missing_no_support_run_yet",
        "recommendation": "attempt_minimal_CMB_perturbation_closure_next",
        "next_target": "44-minimal-CMB-perturbation-closure-attempt.md",
        "source_42_readout": source_42["readout"],
        "frozen_background_parameters": len(frozen),
        "perturbation_contract_rows": len(perturbations),
        "mandatory_missing_perturbation_rows": mandatory_missing,
        "official_reference_rows": len(ref_rows),
        "support_claim_allowed": False,
        "public_claim_allowed": False,
        "background_only_official_run_role": "kill_screen_only_not_support",
        "outputs": {
            "source_checkpoint_register": str(results_dir / "source_checkpoint_register.csv"),
            "frozen_background_manifest": str(results_dir / "frozen_background_manifest.csv"),
            "perturbation_variable_contract": str(results_dir / "perturbation_variable_contract.csv"),
            "standard_parameter_policy": str(results_dir / "standard_parameter_policy.csv"),
            "CMB_observable_contract": str(results_dir / "CMB_observable_contract.csv"),
            "no_new_knob_policy": str(results_dir / "no_new_knob_policy.csv"),
            "official_CMB_run_mode_register": str(results_dir / "official_CMB_run_mode_register.csv"),
            "official_CMB_pass_fail_gates": str(results_dir / "official_CMB_pass_fail_gates.csv"),
            "official_CMB_setup_manifest": str(results_dir / "official_CMB_setup_manifest.csv"),
            "decision": str(results_dir / "decision.csv"),
            "status_json": str(out_dir / "status.json"),
        },
    }
    (out_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (out_dir / "log.txt").write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    (out_dir / "DONE.txt").write_text(status["readout"] + "\n", encoding="utf-8")
    print(json.dumps(status, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
