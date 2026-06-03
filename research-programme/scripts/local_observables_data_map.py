#!/usr/bin/env python3
"""Map local closure-deviation parameters to real observational channels."""

from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


SOURCE_14_STATUS = Path("runs/20260530-231601-closure-deviation-PPN-sensitivity/status.json")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_bound_rows() -> list[dict[str, Any]]:
    microscope_sigma_total = math.sqrt(2.3**2 + 1.5**2) * 1.0e-15
    return [
        {
            "source_id": "cassini_bertotti_2003",
            "observable_channel": "radio_shapiro_delay",
            "mts_parameter": "q_R",
            "reported_parameter": "gamma-1",
            "reported_central": 2.1e-5,
            "reported_1sigma_or_limit": 2.3e-5,
            "confidence_label": "1sigma",
            "bound_type_for_mts": "primary_gamma_bound",
            "source_url": "https://ideas.repec.org/a/nat/nature/v425y2003i6956d10.1038_nature01997.html",
            "notes": "Cassini radio-link result; use as gamma/q_R primary datum, not raw likelihood",
        },
        {
            "source_id": "inpop20a_fienga_2021",
            "observable_channel": "planetary_ephemerides",
            "mts_parameter": "delta_beta",
            "reported_parameter": "beta-1",
            "reported_central": "",
            "reported_1sigma_or_limit": 7.16e-5,
            "confidence_label": "conservative_acceptable_interval",
            "bound_type_for_mts": "beta_completion_gate",
            "source_url": "https://arxiv.org/abs/2111.04499",
            "notes": "Conservative INPOP20a acceptable interval; not a direct one-parameter Gaussian likelihood",
        },
        {
            "source_id": "inpop20a_fienga_2021",
            "observable_channel": "planetary_ephemerides",
            "mts_parameter": "q_R",
            "reported_parameter": "gamma-1",
            "reported_central": "",
            "reported_1sigma_or_limit": 7.49e-5,
            "confidence_label": "conservative_acceptable_interval",
            "bound_type_for_mts": "secondary_gamma_bound",
            "source_url": "https://arxiv.org/abs/2111.04499",
            "notes": "Useful cross-check against Cassini gamma/q_R channel",
        },
        {
            "source_id": "galileo_delva_2018",
            "observable_channel": "gravitational_redshift",
            "mts_parameter": "alpha_clock",
            "reported_parameter": "redshift_fractional_deviation",
            "reported_central": 0.19e-5,
            "reported_1sigma_or_limit": 2.48e-5,
            "confidence_label": "1sigma",
            "bound_type_for_mts": "clock_load_gate",
            "source_url": "https://arxiv.org/abs/1812.03711",
            "notes": "Galileo eccentric-satellite redshift test; use as clock/load anomaly channel",
        },
        {
            "source_id": "microscope_touboul_2022",
            "observable_channel": "weak_equivalence_principle",
            "mts_parameter": "epsilon_matter",
            "reported_parameter": "eta_Ti_Pt",
            "reported_central": -1.5e-15,
            "reported_1sigma_or_limit": microscope_sigma_total,
            "confidence_label": "combined_1sigma_proxy_from_stat_syst",
            "bound_type_for_mts": "universal_matter_coupling_gate",
            "source_url": "https://arxiv.org/abs/2209.15487",
            "notes": "Combines quoted statistical and systematic uncertainties in quadrature for an internal gate",
        },
    ]


def parameter_gate_rows(source_bounds: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_by_id = {row["source_id"] + ":" + row["mts_parameter"]: row for row in source_bounds}
    cassini = source_by_id["cassini_bertotti_2003:q_R"]
    beta = source_by_id["inpop20a_fienga_2021:delta_beta"]
    redshift = source_by_id["galileo_delva_2018:alpha_clock"]
    microscope = source_by_id["microscope_touboul_2022:epsilon_matter"]
    return [
        {
            "mts_parameter": "q_R",
            "adopted_screening_gate": cassini["reported_1sigma_or_limit"],
            "gate_source": cassini["source_id"],
            "why_this_gate": "direct gamma-like channel, strongest simple bound in this map",
            "claim_status": "screening_gate_not_fit_result",
        },
        {
            "mts_parameter": "delta_beta",
            "adopted_screening_gate": beta["reported_1sigma_or_limit"],
            "gate_source": beta["source_id"],
            "why_this_gate": "nonlinear PPN completion primarily constrained by ephemerides",
            "claim_status": "screening_gate_not_fit_result",
        },
        {
            "mts_parameter": "alpha_clock",
            "adopted_screening_gate": redshift["reported_1sigma_or_limit"],
            "gate_source": redshift["source_id"],
            "why_this_gate": "direct clock/redshift anomaly channel",
            "claim_status": "screening_gate_not_fit_result",
        },
        {
            "mts_parameter": "epsilon_matter",
            "adopted_screening_gate": microscope["reported_1sigma_or_limit"],
            "gate_source": microscope["source_id"],
            "why_this_gate": "universal matter-coupling drift must satisfy WEP tests",
            "claim_status": "screening_gate_not_fit_result",
        },
        {
            "mts_parameter": "Q_R",
            "adopted_screening_gate": 0.0,
            "gate_source": "closure_definition",
            "why_this_gate": "closure benchmark requires no reciprocal charge; any nonzero Q_R maps into q_R-like residuals",
            "claim_status": "theory_gate_not_observational_fit",
        },
    ]


def observable_translation_rows(coefficients: dict[str, float], gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    gate_by_param = {row["mts_parameter"]: float(row["adopted_screening_gate"]) for row in gates if row["mts_parameter"] != "Q_R"}
    translations = [
        ("solar_light_bending", "q_R", "solar_light_bending_vs_q_R", "arcsec"),
        ("solar_shapiro", "q_R", "solar_shapiro_vs_q_R", "microseconds"),
        ("mercury_perihelion_gamma", "q_R", "mercury_perihelion_gamma_vs_q_R", "arcsec_per_century"),
        ("mercury_perihelion_beta", "delta_beta", "mercury_perihelion_beta_vs_delta_beta", "arcsec_per_century"),
        ("gps_gravitational_redshift", "alpha_clock", "gps_gravitational_redshift_vs_alpha_clock", "microseconds_per_day"),
        ("eotvos_proxy", "epsilon_matter", "eotvos_proxy_vs_epsilon_matter", "dimensionless"),
    ]
    rows: list[dict[str, Any]] = []
    for observable, parameter, coefficient_key, unit in translations:
        coefficient = coefficients[coefficient_key]
        gate = gate_by_param[parameter]
        rows.append(
            {
                "observable": observable,
                "mts_parameter": parameter,
                "linear_coefficient": coefficient,
                "adopted_parameter_gate": gate,
                "implied_1gate_observable_shift": coefficient * gate,
                "observable_unit": unit,
                "interpretation": "order-of-magnitude screening shift, not a fit residual",
            }
        )
    return rows


def data_channel_rows() -> list[dict[str, Any]]:
    return [
        {
            "priority": 1,
            "channel": "Cassini/radio-science Shapiro",
            "parameters": "q_R",
            "what_to_do_next": "build a one-parameter gamma/q_R likelihood or use published covariance if available",
            "risk": "do not double-count with ephemeris gamma constraints",
        },
        {
            "priority": 2,
            "channel": "planetary ephemerides / perihelia",
            "parameters": "delta_beta,q_R",
            "what_to_do_next": "use beta-gamma covariance or keep as conservative gate",
            "risk": "Mercury-like perihelion combination mixes 2 q_R - delta_beta",
        },
        {
            "priority": 3,
            "channel": "Galileo eccentric-satellite redshift",
            "parameters": "alpha_clock",
            "what_to_do_next": "map clock-load model to redshift violation parameter",
            "risk": "clock anomaly must be separated from coordinate/time-standard choices",
        },
        {
            "priority": 4,
            "channel": "MICROSCOPE WEP",
            "parameters": "epsilon_matter",
            "what_to_do_next": "define matter-sector charges before applying the bound",
            "risk": "no species-dependent prediction exists yet, so this is a gate not a test",
        },
        {
            "priority": 5,
            "channel": "raw VLBI/Gaia light deflection",
            "parameters": "q_R",
            "what_to_do_next": "add later as independent gamma-like check",
            "risk": "needs careful current data curation before use",
        },
    ]


def gate_rows(source: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate": "source_14_complete",
            "status": "pass" if source.get("readout") == "closure_deviation_ppn_sensitivity_internal_budget_complete" else "fail",
            "detail": str(source.get("readout")),
        },
        {
            "gate": "literature_bounds_mapped",
            "status": "pass",
            "detail": "Cassini, INPOP, Galileo redshift, and MICROSCOPE bounds are mapped to MTS parameters",
        },
        {
            "gate": "raw_data_likelihoods_available",
            "status": "fail",
            "detail": "this stage uses published bounds only; no raw covariance/likelihood is ingested",
        },
        {
            "gate": "parameter_degeneracies_flagged",
            "status": "pass",
            "detail": "perihelion beta-gamma degeneracy and q_R double-counting risk are flagged",
        },
        {
            "gate": "empirical_claim_allowed",
            "status": "fail",
            "detail": "screening map is not a new data fit and cannot establish an MTS signal",
        },
        {
            "gate": "next_test_plan_defined",
            "status": "pass",
            "detail": "next step is a conservative gate-runner, then optional raw-likelihood work",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "data_map_status",
            "status": "screening_ready",
            "evidence": "published bounds are connected to q_R, delta_beta, alpha_clock, and epsilon_matter",
            "next_action": "write a gate-runner that marks candidate local branches pass/fail against these bounds",
        },
        {
            "decision": "claim_status",
            "status": "no_empirical_claim",
            "evidence": "no raw data likelihoods or covariance matrices are used",
            "next_action": "report as conservative screening only",
        },
        {
            "decision": "next_target",
            "status": "local_bounds_gate_runner",
            "evidence": "parameter gates are now tabulated",
            "next_action": "create 16-local-bounds-gate-runner.md",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Local observables data map.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    source = load_json(root / SOURCE_14_STATUS)
    coefficients = source["key_linear_coefficients"]
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or root / "runs" / f"{timestamp}-local-observables-data-map"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_bounds = source_bound_rows()
    parameter_gates = parameter_gate_rows(source_bounds)
    translations = observable_translation_rows(coefficients, parameter_gates)
    channels = data_channel_rows()
    gates = gate_rows(source)
    decisions = decision_rows()

    write_csv(results_dir / "published_bound_sources.csv", source_bounds, list(source_bounds[0].keys()))
    write_csv(results_dir / "mts_parameter_screening_gates.csv", parameter_gates, list(parameter_gates[0].keys()))
    write_csv(results_dir / "observable_bound_translations.csv", translations, list(translations[0].keys()))
    write_csv(results_dir / "data_channel_priority_map.csv", channels, list(channels[0].keys()))
    write_csv(results_dir / "local_observables_data_map_gates.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "local_observables_data_map_decision.csv", decisions, list(decisions[0].keys()))

    readout = "local_observables_data_map_screening_ready_not_fit"
    status = {
        "status": "complete_local_observables_data_map",
        "readout": readout,
        "recommendation": "write_local_bounds_gate_runner_next",
        "next_target": "16-local-bounds-gate-runner.md",
        "uses_published_bounds": True,
        "uses_raw_data_likelihoods": False,
        "empirical_claim_allowed": False,
        "adopted_screening_gates": {
            row["mts_parameter"]: row["adopted_screening_gate"] for row in parameter_gates
        },
        "primary_sources": [row["source_url"] for row in source_bounds],
        "outputs": {
            "published_bound_sources": str(results_dir / "published_bound_sources.csv"),
            "mts_parameter_screening_gates": str(results_dir / "mts_parameter_screening_gates.csv"),
            "observable_bound_translations": str(results_dir / "observable_bound_translations.csv"),
            "data_channel_priority_map": str(results_dir / "data_channel_priority_map.csv"),
            "local_observables_data_map_gates": str(results_dir / "local_observables_data_map_gates.csv"),
            "local_observables_data_map_decision": str(results_dir / "local_observables_data_map_decision.csv"),
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
