from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "trace-normalized-Hamiltonian-amplitude-contract"
STATUS = "trace_normalized_Hamiltonian_contract_written_unit_amplitude_not_parent_derived"
CLAIM_CEILING = "conditional_amplitude_contract_no_parent_Bmem_promotion"
LOCKED_B_MEM = Fraction(2, 27)
LOCKED_MODEL = "MTS_fixed_2over27_no_clock"
FITTED_MODEL = "MTS_fixed_p3_u3quarter"
ZERO_MODEL = "MTS_Bmem_zero"

RELEASE_RUNS = {
    "DR2": ROOT / "runs" / "20260601-174000-DR2-locked2over27-fullcov-noSH0ES-cosmo-SN-BAO-short-smoke",
    "DR1": ROOT / "runs" / "20260601-174500-DR1-locked2over27-fullcov-noSH0ES-cosmo-SN-BAO-short-smoke",
}


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "254-rank-27-rank-2-cell-theorem-or-Bmem-closure-lock.md", "rank fraction no-go and sufficient contract"),
        (ROOT / "259-memory-stress-normalization-theorem-attempt.md", "kappa=1 theorem contract"),
        (ROOT / "260-C3-unit-stress-normalization-parent-action-attempt.md", "C3a stress form and C3b scale-lock split"),
        (ROOT / "261-Hstar-H0-scale-lock-and-local-silence-attempt.md", "Hstar/H0 identity and no-go"),
        (ROOT / "262-boundary-Noether-scale-lock-attempt.md", "boundary/Noether scale-lock no-go"),
        (ROOT / "326-radial-memory-parent-action-contract.md", "active projector trace and cubic hazard contract"),
        (ROOT / "330-official-wrapper-locked-branch-release-split.md", "post-wrapper locked branch empirical checkpoint"),
        (ROOT / "scripts" / "cosmo_SN_BAO_closure_runner.py", "scoring runner with locked branch"),
        (Path(__file__).resolve(), "this verifier"),
    ]
    for release, run in RELEASE_RUNS.items():
        sources.extend(
            [
                (run / "status.json", f"{release} short-smoke status"),
                (run / "results" / "fit_summary.csv", f"{release} fit summary"),
                (run / "results" / "baseline_comparison.csv", f"{release} baseline comparison"),
                (run / "results" / "amplitude_policy.csv", f"{release} amplitude policy"),
                (run / "results" / "prior_edge_table.csv", f"{release} prior-edge table"),
            ]
        )
    return [
        {
            "source": relpath(path),
            "role": role,
            "exists": path.exists(),
            "issue": "" if path.exists() else "missing",
        }
        for path, role in sources
    ]


def row_by(rows: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    matches = [row for row in rows if row.get(key) == value]
    if not matches:
        raise KeyError(f"missing row {key}={value}")
    return matches[0]


def comparison_by(rows: list[dict[str, str]], model: str, baseline: str) -> dict[str, str]:
    matches = [row for row in rows if row.get("model") == model and row.get("reference_baseline") == baseline]
    if not matches:
        raise KeyError(f"missing comparison {model} vs {baseline}")
    return matches[0]


def amplitude_value(rows: list[dict[str, str]], factor: str) -> float:
    row = row_by(rows, "factor", factor)
    return float(row["best_fit"])


def release_summary_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    locked_value = float(LOCKED_B_MEM)
    for release, run in RELEASE_RUNS.items():
        result_dir = run / "results"
        fits = read_csv(result_dir / "fit_summary.csv")
        comparisons = read_csv(result_dir / "baseline_comparison.csv")
        amplitudes = read_csv(result_dir / "amplitude_policy.csv")
        locked = row_by(fits, "model", LOCKED_MODEL)
        fitted = row_by(fits, "model", FITTED_MODEL)
        zero = row_by(fits, "model", ZERO_MODEL)
        lcdm = row_by(fits, "model", "LCDM")
        fitted_b = amplitude_value(amplitudes, "B_mem/b_mem")
        kappa_fit = fitted_b / locked_value
        chi2_penalty = float(locked["chi2_total"]) - float(fitted["chi2_total"])
        aic_delta_locked_minus_fitted = float(locked["AIC"]) - float(fitted["AIC"])
        bic_delta_locked_minus_fitted = float(locked["BIC"]) - float(fitted["BIC"])
        zero_chi2_delta = float(zero["chi2_total"]) - float(lcdm["chi2_total"])
        locked_vs_lcdm = comparison_by(comparisons, LOCKED_MODEL, "LCDM")
        locked_vs_wcdm = comparison_by(comparisons, LOCKED_MODEL, "wCDM")
        locked_vs_cpl = comparison_by(comparisons, LOCKED_MODEL, "CPL")
        rows.append(
            {
                "release": release,
                "locked_B_mem": locked_value,
                "fitted_B_mem": fitted_b,
                "kappa_fit": kappa_fit,
                "kappa_minus_1": kappa_fit - 1.0,
                "abs_kappa_minus_1": abs(kappa_fit - 1.0),
                "locked_minus_fitted_chi2": chi2_penalty,
                "locked_minus_fitted_AIC": aic_delta_locked_minus_fitted,
                "locked_minus_fitted_BIC": bic_delta_locked_minus_fitted,
                "locked_delta_BIC_vs_LCDM": float(locked_vs_lcdm["delta_BIC"]),
                "locked_delta_BIC_vs_wCDM": float(locked_vs_wcdm["delta_BIC"]),
                "locked_delta_BIC_vs_CPL": float(locked_vs_cpl["delta_BIC"]),
                "locked_edge_flag": locked["prior_edge_flag"],
                "fitted_edge_flag": fitted["prior_edge_flag"],
                "zero_minus_LCDM_chi2": zero_chi2_delta,
                "readout": "locked_close_to_free_amplitude_and_IC_preferred" if chi2_penalty < 0.001 and aic_delta_locked_minus_fitted < 0.0 else "inspect",
            }
        )
    return rows


def theorem_factor_rows() -> list[dict[str, Any]]:
    q_trace = LOCKED_B_MEM
    return [
        {
            "factor": "q_trace",
            "definition": "Tr(P_active)/dim(V_cell)",
            "required_value": "2/27",
            "current_value": f"{q_trace.numerator}/{q_trace.denominator}",
            "status": "conditional_trace_contract",
            "meaning": "supplies channel fraction if rank-2/rank-27 parent theorem is proved",
        },
        {
            "factor": "epsilon_H",
            "definition": "dimensionless Hamiltonian-current normalization",
            "required_value": "1",
            "current_value": "not parent-derived",
            "status": "open",
            "meaning": "any independent lambda here is observationally kappa_mem",
        },
        {
            "factor": "H_star/H0",
            "definition": "memory stress scale divided by present critical-density scale",
            "required_value": "1",
            "current_value": "closure/theorem target",
            "status": "open",
            "meaning": "H_star route reduces amplitude theorem to scale-lock theorem",
        },
        {
            "factor": "F(N)",
            "definition": "activation kernel normalized by F(0)=0 and F(infinity)=1",
            "required_value": "shape normalized",
            "current_value": "conditional survival-law route",
            "status": "conditional",
            "meaning": "prevents hiding a constant amplitude inside the kernel shape",
        },
        {
            "factor": "B_mem",
            "definition": "q_trace * epsilon_H * (H_star/H0)^2",
            "required_value": "2/27",
            "current_value": "exact only if epsilon_H=1 and H_star=H0",
            "status": "conditional_theorem_not_parent_derived",
            "meaning": "this is the full amplitude contract after the locked-branch release split",
        },
    ]


def derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "statement": "Assume the parent memory term is a trace-normalized Hamiltonian current, not an independent potential.",
            "formula": "rho_mem = epsilon_H * (3 M_Pl^2 H_star^2) * q_trace * F(N)",
            "status": "theorem_premise",
        },
        {
            "step": 2,
            "statement": "Divide by the observed present critical density.",
            "formula": "rho_c0 = 3 M_Pl^2 H0^2",
            "status": "definition",
        },
        {
            "step": 3,
            "statement": "The dimensionless memory amplitude factorizes.",
            "formula": "B_mem = q_trace * epsilon_H * (H_star/H0)^2",
            "status": "derived_algebraically",
        },
        {
            "step": 4,
            "statement": "Insert the active trace fraction.",
            "formula": "q_trace = Tr(P_active)/27 = 2/27",
            "status": "conditional_projector_contract",
        },
        {
            "step": 5,
            "statement": "The locked empirical branch follows only under unit Hamiltonian normalization and scale-lock.",
            "formula": "epsilon_H=1 and H_star=H0 => B_mem=2/27",
            "status": "valid_conditional_theorem",
        },
        {
            "step": 6,
            "statement": "If either epsilon_H or H_star/H0 is free, the amplitude is not derived.",
            "formula": "kappa_mem = epsilon_H * (H_star/H0)^2",
            "status": "no_go_for_unconditional_promotion",
        },
    ]


def no_go_rows() -> list[dict[str, Any]]:
    return [
        {
            "lemma": "lambda_rescaling_no_go",
            "test": "rho_mem -> lambda*rho_mem",
            "result": "all stress-form and Bianchi equations remain valid while B_mem rescales",
            "consequence": "stress-form derivation alone cannot fix epsilon_H=1",
        },
        {
            "lemma": "Hstar_scale_no_go",
            "test": "H_star -> xi*H_star",
            "result": "B_mem rescales by xi^2",
            "consequence": "geometric EH normalization still needs H_star=H0 as a theorem or closure",
        },
        {
            "lemma": "E0_constraint_no_go",
            "test": "use E(0)=1 to fix the memory amplitude",
            "result": "F(0)=0 removes the memory term from the present Friedmann normalization",
            "consequence": "present normalization does not derive B_mem",
        },
        {
            "lemma": "trace_fraction_no_go",
            "test": "use Tr(P_active)/27 alone as the amplitude",
            "result": "gives channel counting but no stress units",
            "consequence": "rank arithmetic becomes amplitude only after Hamiltonian-current normalization",
        },
        {
            "lemma": "empirical_closeness_no_go",
            "test": "use fitted B_mem near 2/27 as proof",
            "result": "release-split proximity is a clue, not a parent variation",
            "consequence": "2/27 remains theorem-target/closure until the parent action supplies the missing factors",
        },
    ]


def gate_rows(sources: list[dict[str, Any]], summaries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources_ok = all(bool(row["exists"]) for row in sources)
    max_abs_kappa_shift = max(abs(float(row["kappa_minus_1"])) for row in summaries)
    zero_control_ok = all(math.isclose(float(row["zero_minus_LCDM_chi2"]), 0.0, abs_tol=1e-10) for row in summaries)
    edge_clean = all(row["locked_edge_flag"] == "False" and row["fitted_edge_flag"] == "False" for row in summaries)
    locked_ic_beats_fitted = all(float(row["locked_minus_fitted_AIC"]) < 0.0 and float(row["locked_minus_fitted_BIC"]) < 0.0 for row in summaries)
    return [
        {"gate": "source_paths_exist", "status": "pass" if sources_ok else "fail", "evidence": sources_ok},
        {"gate": "locked_release_split_edge_clean", "status": "pass" if edge_clean else "fail", "evidence": edge_clean},
        {"gate": "zero_memory_reproduces_LCDM", "status": "pass" if zero_control_ok else "fail", "evidence": zero_control_ok},
        {
            "gate": "fitted_amplitude_within_one_percent_of_locked",
            "status": "pass" if max_abs_kappa_shift < 0.01 else "fail",
            "evidence": max_abs_kappa_shift,
        },
        {
            "gate": "locked_beats_fitted_by_information_criteria",
            "status": "pass" if locked_ic_beats_fitted else "fail",
            "evidence": locked_ic_beats_fitted,
        },
        {
            "gate": "conditional_factorization_theorem",
            "status": "pass",
            "evidence": "B_mem=q_trace*epsilon_H*(H_star/H0)^2",
        },
        {
            "gate": "epsilon_H_parent_derived",
            "status": "fail",
            "evidence": "no parent Hamiltonian-current normalization theorem yet",
        },
        {
            "gate": "Hstar_equals_H0_parent_derived",
            "status": "fail",
            "evidence": "previous boundary/Noether attempts left this closure-locked",
        },
        {
            "gate": "rank27_rank2_parent_derived",
            "status": "fail",
            "evidence": "active trace algebra is conditional; parent cell theorem remains open",
        },
        {
            "gate": "Bmem_parent_promotion_allowed",
            "status": "fail",
            "evidence": "conditional theorem contract only; empirical proximity is not variation",
        },
    ]


def decision_rows(summaries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    kappa_values = [float(row["kappa_fit"]) for row in summaries]
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "lead_branch": LOCKED_MODEL,
            "kappa_fit_min": min(kappa_values),
            "kappa_fit_max": max(kappa_values),
            "meaning": (
                "The post-330 release split makes the locked amplitude look disciplined: the free diagnostic amplitude "
                "sits within one percent of kappa=1 and the locked branch wins information criteria by not spending "
                "the amplitude parameter. The derivation status still does not promote: the exact parent theorem must "
                "derive q_trace, epsilon_H=1, and H_star=H0."
            ),
            "next_target": "derive_parent_Hamiltonian_trace_current_or_keep_Bmem_2over27_as_empirical_closure",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    summaries = release_summary_rows()
    theorem_factors = theorem_factor_rows()
    derivation = derivation_rows()
    no_go = no_go_rows()
    gates = gate_rows(sources, summaries)
    decisions = decision_rows(summaries)

    outputs = {
        "source_register.csv": (sources, ["source", "role", "exists", "issue"]),
        "release_split_amplitude_summary.csv": (
            summaries,
            [
                "release",
                "locked_B_mem",
                "fitted_B_mem",
                "kappa_fit",
                "kappa_minus_1",
                "abs_kappa_minus_1",
                "locked_minus_fitted_chi2",
                "locked_minus_fitted_AIC",
                "locked_minus_fitted_BIC",
                "locked_delta_BIC_vs_LCDM",
                "locked_delta_BIC_vs_wCDM",
                "locked_delta_BIC_vs_CPL",
                "locked_edge_flag",
                "fitted_edge_flag",
                "zero_minus_LCDM_chi2",
                "readout",
            ],
        ),
        "theorem_factorization.csv": (
            theorem_factors,
            ["factor", "definition", "required_value", "current_value", "status", "meaning"],
        ),
        "derivation_steps.csv": (derivation, ["step", "statement", "formula", "status"]),
        "normalization_no_go_lemmas.csv": (no_go, ["lemma", "test", "result", "consequence"]),
        "gate_results.csv": (gates, ["gate", "status", "evidence"]),
        "decision.csv": (
            decisions,
            ["decision", "claim_ceiling", "lead_branch", "kappa_fit_min", "kappa_fit_max", "meaning", "next_target"],
        ),
    }
    for filename, (rows, fieldnames) in outputs.items():
        write_csv(results_dir / filename, rows, fieldnames)

    payload = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(outputs),
        "locked_B_mem": float(LOCKED_B_MEM),
        "conditional_factorization": "B_mem=q_trace*epsilon_H*(H_star/H0)^2",
        "Bmem_parent_derived": False,
        "promotion_allowed": False,
        "next_target": "derive_parent_Hamiltonian_trace_current_or_keep_Bmem_2over27_as_empirical_closure",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Trace-normalized Hamiltonian amplitude contract after the locked release split.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
