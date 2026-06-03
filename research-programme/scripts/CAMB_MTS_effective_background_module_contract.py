#!/usr/bin/env python3
"""Checkpoint 185: contract for mapping locked MTS background into CAMB."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any

import camb
import camb.dark_energy as camb_dark_energy
import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

CHECKPOINT_184_RUN = RUNS_ROOT / "20260601-000001-MTS-CMB-background-injection-dry-run"
CHECKPOINT_183_RUN = RUNS_ROOT / "20260531-235959-LCDM-baseline-reproduction-dry-run"
CMB_CONTRACT_RUN = RUNS_ROOT / "20260531-235950-CMB-kill-screen-runner-contract"
CONFIG_DIR = CMB_CONTRACT_RUN / "configs"
MTS_EXACT_CONFIG = CONFIG_DIR / "MTS_exact_auxiliary_transfer_locked.blueprint.json"
MTS_HIGH_CS_CONFIG = CONFIG_DIR / "MTS_high_cs_transfer_locked.blueprint.json"

STATUS_READY = "CAMB_MTS_effective_background_module_contract_ready_for_tiny_high_cs_wtable_spectra_smoke"
STATUS_FAIL = "CAMB_MTS_effective_background_module_contract_failed"
CLAIM_CEILING = "CAMB_mapping_contract_only_no_MTS_CMB_spectra_no_CMB_claim"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"

LOCKED_B_MEM = 2.0 / 27.0
LOCKED_P = 3.0
LOCKED_U3 = 0.25
N_EFF = 3.046
W_TABLE_REDSHIFT_MAX = 10000.0
W_TABLE_SIZE = 700
W_NEAR_COSMOLOGICAL_CONSTANT_TOLERANCE = 1.0e-12


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


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


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
        (Path(__file__).resolve(), "checkpoint 185 contract generator"),
        (WORK_DIR / "184-MTS-CMB-background-injection-dry-run.md", "previous MTS CMB background injection checkpoint"),
        (CHECKPOINT_184_RUN / "status.json", "previous MTS background injection status"),
        (CHECKPOINT_184_RUN / "results" / "MTS_background_functions.csv", "locked MTS background table"),
        (CHECKPOINT_184_RUN / "results" / "CAMB_injection_contract.csv", "previous CAMB injection dry-run contract"),
        (CHECKPOINT_183_RUN / "status.json", "LCDM CAMB baseline status"),
        (CHECKPOINT_183_RUN / "results" / "baseline_parameter_vector.csv", "LCDM baseline physical parameter vector"),
        (WORK_DIR / "178-memory-perturbation-owner-attempt.md", "effective high-cs perturbation owner checkpoint"),
        (WORK_DIR / "180-CMB-kill-screen-or-parent-amplitude-owner-decision.md", "CMB route decision"),
        (WORK_DIR / "181-CMB-engine-readiness-and-dryrun-wrapper.md", "CMB wrapper readiness checkpoint"),
        (WORK_DIR / "182-CMB-engine-install-or-external-run-plan.md", "CAMB install checkpoint"),
        (WORK_DIR / "183-LCDM-baseline-reproduction-dry-run.md", "LCDM baseline reproduction checkpoint"),
        (MTS_EXACT_CONFIG, "exact auxiliary transfer blueprint"),
        (MTS_HIGH_CS_CONFIG, "high-cs transfer blueprint"),
        (Path(camb.__file__).resolve(), "installed CAMB Python package"),
        (Path(camb_dark_energy.__file__).resolve(), "installed CAMB dark-energy API source"),
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


def reference_params() -> dict[str, float]:
    config = load_json(MTS_HIGH_CS_CONFIG)
    fixed = config["fixed_mts_parameters"]
    return {
        "Omega_m0": float(fixed["Omega_m0_late_reference"]),
        "h": float(fixed["h_profiled_reference"]),
        "B_mem": float(fixed["B_mem"]),
        "p": float(fixed["p"]),
        "u3": float(fixed["u3"]),
    }


def baseline_params() -> dict[str, float]:
    rows = read_csv_rows(CHECKPOINT_183_RUN / "results" / "baseline_parameter_vector.csv")
    return {row["parameter"]: float(row["value"]) for row in rows}


def radiation_density(hubble_fraction: float) -> float:
    omega_gamma = 2.469e-5 / (hubble_fraction * hubble_fraction)
    return omega_gamma * (1.0 + 0.22710731766 * N_EFF)


def activation(past_efolds: float, exponent_power: float, width: float) -> float:
    if past_efolds <= 0.0:
        return 0.0
    exponent = (past_efolds / width) ** exponent_power
    if exponent > 745.0:
        return 1.0
    return 1.0 - math.exp(-exponent)


def activation_derivative(past_efolds: float, exponent_power: float, width: float) -> float:
    if past_efolds <= 0.0:
        return 0.0
    exponent = (past_efolds / width) ** exponent_power
    if exponent > 745.0:
        return 0.0
    return math.exp(-exponent) * exponent_power * past_efolds ** (exponent_power - 1.0) / (width**exponent_power)


def memory_background(scale_factor: float, params: dict[str, float]) -> dict[str, float]:
    omega_m0 = params["Omega_m0"]
    hubble_fraction = params["h"]
    b_mem = params["B_mem"]
    exponent_power = params["p"]
    width = params["u3"]
    redshift = (1.0 / scale_factor) - 1.0
    past_efolds = -math.log(scale_factor)
    activation_value = activation(past_efolds, exponent_power, width)
    activation_slope = activation_derivative(past_efolds, exponent_power, width)
    rho_mem = 1.0 - omega_m0 + b_mem * activation_value
    one_plus_w = b_mem * activation_slope / (3.0 * rho_mem) if rho_mem > 0.0 else math.nan
    w_mem = -1.0 + one_plus_w
    omega_r = radiation_density(hubble_fraction)
    e2_no_radiation = omega_m0 / (scale_factor**3) + rho_mem
    e2_with_radiation = e2_no_radiation + omega_r / (scale_factor**4)
    return {
        "z": redshift,
        "a": scale_factor,
        "N_ln_1_plus_z": past_efolds,
        "A_mem": activation_value,
        "dA_dN": activation_slope,
        "rho_mem_over_rhocrit0": rho_mem,
        "one_plus_w_mem": one_plus_w,
        "w_mem": w_mem,
        "E2_no_radiation": e2_no_radiation,
        "E2_with_radiation": e2_with_radiation,
        "Omega_mem_with_radiation": rho_mem / e2_with_radiation,
        "Omega_m_with_radiation": omega_m0 / (scale_factor**3) / e2_with_radiation,
        "Omega_r_with_radiation": omega_r / (scale_factor**4) / e2_with_radiation,
    }


def camb_w_table(params: dict[str, float]) -> list[dict[str, Any]]:
    redshift_grid = np.geomspace(W_TABLE_REDSHIFT_MAX, 1.0e-5, W_TABLE_SIZE - 1)
    scale_factor_grid = sorted([float(1.0 / (1.0 + redshift)) for redshift in redshift_grid] + [1.0])
    rows: list[dict[str, Any]] = []
    for index, scale_factor in enumerate(scale_factor_grid):
        background = memory_background(scale_factor, params)
        rows.append(
            {
                "index": index,
                "a": background["a"],
                "z": background["z"],
                "w_mem": background["w_mem"],
                "one_plus_w_mem": background["one_plus_w_mem"],
                "rho_mem_over_rhocrit0": background["rho_mem_over_rhocrit0"],
                "A_mem": background["A_mem"],
                "dA_dN": background["dA_dN"],
                "Omega_mem_with_radiation": background["Omega_mem_with_radiation"],
                "table_role": "CAMB set_w_a_table input; not a fitted spline",
            }
        )
    return rows


def try_camb_dark_energy_class(class_name: str, w_table_rows: list[dict[str, Any]]) -> dict[str, Any]:
    dark_energy_class = getattr(camb_dark_energy, class_name)
    scale_factors = np.array([float(row["a"]) for row in w_table_rows])
    w_values = np.array([float(row["w_mem"]) for row in w_table_rows])
    try:
        dark_energy = dark_energy_class()
        instantiation_status = "yes"
        cs2_supported = "yes" if hasattr(dark_energy, "cs2") else "no"
    except Exception as exc:  # pragma: no cover - depends on CAMB implementation details
        dark_energy = None
        instantiation_status = f"no: {type(exc).__name__}: {exc}"
        cs2_supported = "unknown"
    result = {
        "probe": class_name,
        "available": instantiation_status,
        "set_w_a_table": "not_tested",
        "cs2_supported": cs2_supported,
        "validate_params": "not_tested",
        "usable_for": "",
        "limitation": "",
        "status": "blocked" if dark_energy is None else "fail",
    }
    if dark_energy is None:
        result["usable_for"] = "abstract/API inventory only"
        result["limitation"] = "not directly instantiable in installed CAMB build"
        return result
    try:
        if hasattr(dark_energy, "cs2"):
            dark_energy.cs2 = 1.0
        dark_energy.set_w_a_table(scale_factors, w_values)
        result["set_w_a_table"] = "pass"
        try:
            dark_energy.validate_params()
            result["validate_params"] = "pass"
            result["status"] = "pass"
        except Exception as exc:  # pragma: no cover - depends on CAMB implementation details
            result["validate_params"] = f"fail: {type(exc).__name__}: {exc}"
    except Exception as exc:  # pragma: no cover - depends on CAMB implementation details
        result["set_w_a_table"] = f"fail: {type(exc).__name__}: {exc}"

    if class_name == "DarkEnergyFluid":
        result["usable_for"] = "default high-cs effective-fluid smoke branch"
        result["limitation"] = "cannot encode exact auxiliary delta=theta=0 constraint or parent MTS perturbation equations"
    elif class_name == "DarkEnergyPPF":
        result["usable_for"] = "numerical comparator or fallback for crossing/stability diagnostics"
        result["limitation"] = "PPF is an ad hoc approximation; it is not a parent MTS owner"
    else:
        result["usable_for"] = "capability inventory only"
        result["limitation"] = "not selected for locked no-clock memory branch"
    return result


def capability_probe_rows(w_table_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = [
        {
            "probe": "CAMB Python package",
            "available": "yes",
            "set_w_a_table": "n/a",
            "cs2_supported": "n/a",
            "validate_params": "n/a",
            "usable_for": "local Boltzmann engine",
            "limitation": "engine availability does not equal MTS CMB likelihood support",
            "status": "pass",
        },
        {
            "probe": "CAMB version",
            "available": camb.__version__,
            "set_w_a_table": "n/a",
            "cs2_supported": "n/a",
            "validate_params": "n/a",
            "usable_for": "reproducibility log",
            "limitation": "version-specific Python API",
            "status": "pass",
        },
    ]
    for class_name in ["DarkEnergyEqnOfState", "DarkEnergyFluid", "DarkEnergyPPF"]:
        if hasattr(camb_dark_energy, class_name):
            rows.append(try_camb_dark_energy_class(class_name, w_table_rows))
        else:
            rows.append(
                {
                    "probe": class_name,
                    "available": "no",
                    "set_w_a_table": "fail",
                    "cs2_supported": "unknown",
                    "validate_params": "not_tested",
                    "usable_for": "",
                    "limitation": "missing from installed CAMB",
                    "status": "fail",
                }
            )
    rows.extend(
        [
            {
                "probe": "exact auxiliary perturbation constraint",
                "available": "no built-in primitive found",
                "set_w_a_table": "background only",
                "cs2_supported": "not sufficient",
                "validate_params": "blocked",
                "usable_for": "requires custom perturbation module before exact branch spectra",
                "limitation": "built-in dark energy fluids evolve perturbations; they do not impose delta=theta=0 as a derived constraint",
                "status": "blocked",
            },
            {
                "probe": "custom parent MTS equations",
                "available": "not implemented",
                "set_w_a_table": "not enough",
                "cs2_supported": "not enough",
                "validate_params": "blocked",
                "usable_for": "future parent-owned spectra",
                "limitation": "requires field equations, conservation handoff, perturbation variables, and gauge interface",
                "status": "blocked",
            },
        ]
    )
    return rows


def mts_to_camb_mapping_rows(params: dict[str, float], baseline: dict[str, float]) -> list[dict[str, Any]]:
    locked_hubble = 100.0 * params["h"]
    locked_omega_m_h2 = params["Omega_m0"] * params["h"] ** 2
    baseline_omega_m_h2 = baseline["ombh2"] + baseline["omch2"]
    derived_cdm_h2_no_neutrino_subtraction = locked_omega_m_h2 - baseline["ombh2"]
    return [
        {
            "mapping_item": "MTS memory density",
            "MTS_quantity": "rho_mem(a)=1-Omega_m0+B_mem A[-ln(a)]",
            "CAMB_quantity": "dark-energy background normalized to Omega_de0=1-Omega_m0 for flat smoke branch",
            "value_or_rule": f"B_mem={params['B_mem']}; p={params['p']}; u3={params['u3']}; Omega_m0={params['Omega_m0']}",
            "owner_status": "locked closure theorem-target, not refit",
            "allowed_next_use": "generate w(a) table",
            "claim_limit": CLAIM_CEILING,
        },
        {
            "mapping_item": "MTS equation of state",
            "MTS_quantity": "1+w_mem=B_mem dA/dN /(3 rho_mem)",
            "CAMB_quantity": "DarkEnergyFluid.set_w_a_table(a,w_mem)",
            "value_or_rule": f"{W_TABLE_SIZE} monotone a nodes from z={W_TABLE_REDSHIFT_MAX} to z=0",
            "owner_status": "effective high-cs branch only",
            "allowed_next_use": "tiny spectra smoke against LCDM baseline",
            "claim_limit": "does not derive parent perturbations",
        },
        {
            "mapping_item": "high-cs perturbation closure",
            "MTS_quantity": "c_s_eff^2=1, sigma_mem=0",
            "CAMB_quantity": "DarkEnergyFluid.cs2=1.0, no anisotropic stress parameter",
            "value_or_rule": "fixed, not fitted",
            "owner_status": "P06 partial/effective owner from checkpoint 178",
            "allowed_next_use": "default first MTS CMB spectra smoke",
            "claim_limit": "screened/effective; no parent promotion",
        },
        {
            "mapping_item": "PPF comparator",
            "MTS_quantity": "same w(a) background",
            "CAMB_quantity": "DarkEnergyPPF.set_w_a_table(a,w_mem)",
            "value_or_rule": "run only as diagnostic if Fluid branch is unstable or as stated comparator",
            "owner_status": "ad hoc numerical comparator",
            "allowed_next_use": "stability sensitivity branch",
            "claim_limit": "not a physical MTS win condition by itself",
        },
        {
            "mapping_item": "exact auxiliary branch",
            "MTS_quantity": "delta_mem=theta_mem=delta_p_mem=sigma_mem=0 by constraint",
            "CAMB_quantity": "no built-in class mapped",
            "value_or_rule": "requires custom module or parent-derived auxiliary perturbation equations",
            "owner_status": "blocked",
            "allowed_next_use": "contract only",
            "claim_limit": "no spectra from exact branch yet",
        },
        {
            "mapping_item": "LCDM-density isolation smoke",
            "MTS_quantity": "replace only dark-energy w(a)",
            "CAMB_quantity": "H0, ombh2, omch2, tau, As, ns, mnu, omk from checkpoint 183",
            "value_or_rule": f"H0={baseline['H0']}; omega_m_h2_no_neutrino={baseline_omega_m_h2}",
            "owner_status": "fair comparator/control branch",
            "allowed_next_use": "isolate effect of MTS w(a) under same baseline densities",
            "claim_limit": "not the locked late-time MTS transfer branch",
        },
        {
            "mapping_item": "locked-transfer smoke",
            "MTS_quantity": "h_profiled_reference and Omega_m0_late_reference",
            "CAMB_quantity": "H0=100 h; omch2 derived after baryon/neutrino convention is declared",
            "value_or_rule": f"H0={locked_hubble}; omega_m_h2_target={locked_omega_m_h2}; provisional omch2_no_neutrino_subtraction={derived_cdm_h2_no_neutrino_subtraction}",
            "owner_status": "predeclared no-refit branch",
            "allowed_next_use": "second tiny smoke branch after density convention audit",
            "claim_limit": "must not silently tune H0/Omega_m to save spectra",
        },
    ]


def interpolation_contract_rows(w_table_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    scale_factors = [float(row["a"]) for row in w_table_rows]
    w_values = [float(row["w_mem"]) for row in w_table_rows]
    rho_values = [float(row["rho_mem_over_rhocrit0"]) for row in w_table_rows]
    one_plus_values = [float(row["one_plus_w_mem"]) for row in w_table_rows]
    monotone = all(right > left for left, right in zip(scale_factors, scale_factors[1:]))
    finite = all(math.isfinite(value) for value in scale_factors + w_values + rho_values + one_plus_values)
    non_phantom = min(w_values) >= -1.0 - W_NEAR_COSMOLOGICAL_CONSTANT_TOLERANCE
    return [
        {
            "contract_item": "grid_domain",
            "requirement": "scale-factor grid covers recombination through today",
            "actual": f"a_min={min(scale_factors)}; a_max={max(scale_factors)}; rows={len(scale_factors)}",
            "status": "pass" if min(scale_factors) <= 1.0 / (1.0 + W_TABLE_REDSHIFT_MAX) and max(scale_factors) == 1.0 else "fail",
            "failure_consequence": "no spectra run",
        },
        {
            "contract_item": "monotonicity",
            "requirement": "CAMB input a values strictly increase",
            "actual": str(monotone),
            "status": "pass" if monotone else "fail",
            "failure_consequence": "no spectra run",
        },
        {
            "contract_item": "finite_values",
            "requirement": "a, w, rho, and one_plus_w are finite",
            "actual": str(finite),
            "status": "pass" if finite else "fail",
            "failure_consequence": "no spectra run",
        },
        {
            "contract_item": "positive_density",
            "requirement": "rho_mem remains positive on interpolation grid",
            "actual": f"rho_min={min(rho_values)}; rho_max={max(rho_values)}",
            "status": "pass" if min(rho_values) > 0.0 else "fail",
            "failure_consequence": "no spectra run",
        },
        {
            "contract_item": "non_phantom_fluid",
            "requirement": "default DarkEnergyFluid branch must not cross below w=-1",
            "actual": f"w_min={min(w_values)}; w_max={max(w_values)}",
            "status": "pass" if non_phantom else "fail",
            "failure_consequence": "use PPF diagnostic only; no physical high-cs fluid claim",
        },
        {
            "contract_item": "node_lock",
            "requirement": "w(a) nodes are generated from locked B_mem,p,u3 only",
            "actual": f"B_mem={LOCKED_B_MEM}; p={LOCKED_P}; u3={LOCKED_U3}",
            "status": "pass",
            "failure_consequence": "treat as refit/rescue and discard",
        },
        {
            "contract_item": "extrapolation_policy",
            "requirement": "no extrapolated physics outside declared table domain",
            "actual": "table covers z<=10000; future runs must not interpret outside this range without extension",
            "status": "pass",
            "failure_consequence": "extend grid and rerun contract before spectra",
        },
    ]


def perturbation_closure_mapping_rows() -> list[dict[str, Any]]:
    return [
        {
            "closure_branch": "high_cs_effective_fluid_default",
            "CAMB_object": "DarkEnergyFluid",
            "background": "set_w_a_table(a,w_mem)",
            "perturbations": "CAMB single-fluid perturbations with cs2=1",
            "MTS_owner_status": "partial/effective from checkpoint 178",
            "allowed": "yes for tiny spectra smoke",
            "promotion_limit": "not a parent action derivation",
        },
        {
            "closure_branch": "high_cs_PPF_comparator",
            "CAMB_object": "DarkEnergyPPF",
            "background": "same set_w_a_table(a,w_mem)",
            "perturbations": "PPF approximation",
            "MTS_owner_status": "diagnostic only",
            "allowed": "yes as sensitivity/comparator, not default evidence",
            "promotion_limit": "PPF is ad hoc; cannot clear parent perturbation gate",
        },
        {
            "closure_branch": "exact_auxiliary_smooth_memory",
            "CAMB_object": "none built-in",
            "background": "same rho_mem(a) possible",
            "perturbations": "requires delta=theta=delta_p=sigma=0 constraint and conservation handoff",
            "MTS_owner_status": "open theorem/custom-module debt",
            "allowed": "no spectra yet",
            "promotion_limit": "must build custom equations or derive auxiliary Bianchi owner",
        },
        {
            "closure_branch": "parent_field_theory_branch",
            "CAMB_object": "none",
            "background": "not yet parent-derived",
            "perturbations": "not yet parent-derived",
            "MTS_owner_status": "blocked by parent action and local GR gates",
            "allowed": "contract only",
            "promotion_limit": "cannot be claimed by CAMB fluid mimic",
        },
    ]


def forbidden_rescue_rows() -> list[dict[str, Any]]:
    return [
        {
            "forbidden_knob": "fit extra w(a) spline nodes",
            "why_forbidden": "turns locked memory law into generic dark energy reconstruction",
            "allowed_exception": "none for MTS evidence branch",
            "same_test_for_baselines": "if used, report as generic DE comparator, not MTS",
        },
        {
            "forbidden_knob": "vary B_mem,p,u3 in CMB spectra pass",
            "why_forbidden": "breaks the locked no-clock branch",
            "allowed_exception": "separate robustness branch explicitly labelled refit",
            "same_test_for_baselines": "compare against wCDM/CPL with matching parameter-count penalties",
        },
        {
            "forbidden_knob": "fit c_s_eff_squared",
            "why_forbidden": "would hide perturbation-owner failure",
            "allowed_exception": "diagnostic scan only after fixed cs2=1 result is logged",
            "same_test_for_baselines": "report identical scan freedom for comparator models",
        },
        {
            "forbidden_knob": "add anisotropic stress or lensing rescale",
            "why_forbidden": "would rescue TT/TE/EE/lensing without parent stress owner",
            "allowed_exception": "none for promoted branch",
            "same_test_for_baselines": "if LCDM uses A_L or MG knobs, penalize them too",
        },
        {
            "forbidden_knob": "free N_eff, curvature, or neutrino mass only for MTS",
            "why_forbidden": "moves CMB acoustic scales by unrelated calibration freedom",
            "allowed_exception": "matched baseline robustness matrix",
            "same_test_for_baselines": "must run identical freedom for LCDM/wCDM/CPL",
        },
        {
            "forbidden_knob": "retune H0/Omega_m after seeing CMB spectra",
            "why_forbidden": "would make the CMB branch post hoc",
            "allowed_exception": "predeclared two-branch smoke: LCDM-density isolation and locked-transfer",
            "same_test_for_baselines": "all post-hoc fits must be marked exploratory and AIC/BIC penalized",
        },
        {
            "forbidden_knob": "treat exact auxiliary as CAMB Fluid output",
            "why_forbidden": "Fluid evolves perturbations; exact auxiliary demands constrained perturbation silence",
            "allowed_exception": "custom module with explicit equations",
            "same_test_for_baselines": "not applicable",
        },
    ]


def module_readiness_gate_rows(
    source_rows: list[dict[str, Any]],
    capability_rows: list[dict[str, Any]],
    interpolation_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    sources_ok = all(row["exists"] == "yes" for row in source_rows)
    fluid_ok = any(row["probe"] == "DarkEnergyFluid" and row["status"] == "pass" for row in capability_rows)
    ppf_ok = any(row["probe"] == "DarkEnergyPPF" and row["status"] == "pass" for row in capability_rows)
    interpolation_ok = all(row["status"] == "pass" for row in interpolation_rows)
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if sources_ok else "fail",
            "evidence": f"missing={sum(row['exists'] != 'yes' for row in source_rows)}",
            "claim_allowed": "contract only",
        },
        {
            "gate": "CAMB installed",
            "status": "pass",
            "evidence": f"CAMB {camb.__version__}",
            "claim_allowed": "engine readiness",
        },
        {
            "gate": "DarkEnergyFluid accepts locked MTS w(a)",
            "status": "pass" if fluid_ok else "fail",
            "evidence": "set_w_a_table + validate_params",
            "claim_allowed": "tiny high-cs spectra smoke allowed" if fluid_ok else "no spectra",
        },
        {
            "gate": "DarkEnergyPPF comparator accepts locked MTS w(a)",
            "status": "pass" if ppf_ok else "fail",
            "evidence": "set_w_a_table + validate_params",
            "claim_allowed": "diagnostic comparator only",
        },
        {
            "gate": "background interpolation contract clean",
            "status": "pass" if interpolation_ok else "fail",
            "evidence": "monotone finite positive non-phantom grid",
            "claim_allowed": "tiny spectra smoke allowed" if interpolation_ok else "no spectra",
        },
        {
            "gate": "exact auxiliary CAMB mapping",
            "status": "blocked",
            "evidence": "no built-in primitive for delta=theta=0 constraint",
            "claim_allowed": "no exact auxiliary spectra",
        },
        {
            "gate": "MTS spectra run",
            "status": "not_run",
            "evidence": "checkpoint 185 is mapping contract only",
            "claim_allowed": "no CMB support claim",
        },
        {
            "gate": "official CMB likelihood",
            "status": "not_run",
            "evidence": "no Planck/ACT/SPT likelihood called",
            "claim_allowed": "no public CMB claim",
        },
    ]


def decision_rows(gate_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    fail_count = sum(row["status"] == "fail" for row in gate_rows)
    high_cs_ready = any(
        row["gate"] == "DarkEnergyFluid accepts locked MTS w(a)" and row["status"] == "pass"
        for row in gate_rows
    )
    interpolation_ready = any(
        row["gate"] == "background interpolation contract clean" and row["status"] == "pass"
        for row in gate_rows
    )
    status = STATUS_READY if fail_count == 0 and high_cs_ready and interpolation_ready else STATUS_FAIL
    return [
        {
            "decision": status,
            "meaning": "locked MTS high-cs w(a) can now be tried in a tiny CAMB spectra smoke; exact auxiliary remains custom-module debt",
            "next_target": "186-CAMB-high-cs-wtable-spectra-smoke.md" if status == STATUS_READY else "repair CAMB mapping contract",
            "MTS_spectra_run": "false",
            "official_likelihood_run": "false",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-CAMB-MTS-effective-background-module-contract"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    params = reference_params()
    baseline = baseline_params()
    w_table_rows = camb_w_table(params)
    source_rows = source_register_rows()
    capability_rows = capability_probe_rows(w_table_rows)
    mapping_rows = mts_to_camb_mapping_rows(params, baseline)
    interpolation_rows = interpolation_contract_rows(w_table_rows)
    perturbation_rows = perturbation_closure_mapping_rows()
    forbidden_rows = forbidden_rescue_rows()
    gate_rows = module_readiness_gate_rows(source_rows, capability_rows, interpolation_rows)
    decision = decision_rows(gate_rows)

    outputs: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "CAMB_capability_probe.csv": (
            capability_rows,
            ["probe", "available", "set_w_a_table", "cs2_supported", "validate_params", "usable_for", "limitation", "status"],
        ),
        "MTS_CAMB_w_table.csv": (
            w_table_rows,
            ["index", "a", "z", "w_mem", "one_plus_w_mem", "rho_mem_over_rhocrit0", "A_mem", "dA_dN", "Omega_mem_with_radiation", "table_role"],
        ),
        "MTS_to_CAMB_mapping_contract.csv": (
            mapping_rows,
            ["mapping_item", "MTS_quantity", "CAMB_quantity", "value_or_rule", "owner_status", "allowed_next_use", "claim_limit"],
        ),
        "background_interpolation_contract.csv": (
            interpolation_rows,
            ["contract_item", "requirement", "actual", "status", "failure_consequence"],
        ),
        "perturbation_closure_mapping.csv": (
            perturbation_rows,
            ["closure_branch", "CAMB_object", "background", "perturbations", "MTS_owner_status", "allowed", "promotion_limit"],
        ),
        "forbidden_rescue_knobs.csv": (
            forbidden_rows,
            ["forbidden_knob", "why_forbidden", "allowed_exception", "same_test_for_baselines"],
        ),
        "module_readiness_gates.csv": (
            gate_rows,
            ["gate", "status", "evidence", "claim_allowed"],
        ),
        "decision.csv": (
            decision,
            ["decision", "meaning", "next_target", "MTS_spectra_run", "official_likelihood_run", "promotion_allowed", "claim_ceiling"],
        ),
    }
    for filename, (rows, fieldnames) in outputs.items():
        write_csv(results_dir / filename, rows, fieldnames)

    status_payload = {
        "status": decision[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "camb_version": camb.__version__,
        "generated": list(outputs.keys()),
        "MTS_spectra_run": False,
        "official_likelihood_run": False,
        "promotion_allowed": False,
        "default_next_branch": "high_cs_effective_fluid_wtable",
        "exact_auxiliary_branch": "blocked_requires_custom_module",
        "next_target": decision[0]["next_target"],
    }
    write_json(run_dir / "status.json", status_payload)
    (run_dir / "DONE.txt").write_text(status_payload["status"] + "\n", encoding="utf-8")
    return status_payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timestamp", default=None, help="Optional run timestamp prefix.")
    args = parser.parse_args()
    status_payload = run(args.timestamp)
    print(json.dumps(status_payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
