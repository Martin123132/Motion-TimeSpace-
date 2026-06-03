from __future__ import annotations

import argparse
import csv
import json
import math
import re
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "FLRW-memory-projection-amplitude-contract"
STATUS = "FLRW_memory_projection_contract_conditionally_derived_LCDM_limit_proved_Bmem_parent_derivation_still_fails"
CLAIM_CEILING = "conditional_FLRW_projection_contract_no_parent_amplitude_promotion"

Q_RANK = 2.0 / 27.0
U3 = 0.25
P_ACTIVATION = 3.0

SCORE_READOUT_RUN = ROOT / "runs" / "20260601-000142-fullcov-noSH0ES-score-readout"
FIXED_KAPPA_READOUT_RUN = ROOT / "runs" / "20260601-000106-fixed-vs-kappa-short-smoke-readout-after-282"


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
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def pass_fail(value: bool) -> str:
    return "pass" if value else "fail"


def activation(n_past: float, u3: float = U3, p: float = P_ACTIVATION) -> float:
    if n_past <= 0.0:
        return 0.0
    return 1.0 - math.exp(-((n_past / u3) ** p))


def activation_prime(n_past: float, u3: float = U3, p: float = P_ACTIVATION) -> float:
    if n_past <= 0.0:
        return 0.0
    x = n_past / u3
    return (p / u3) * (x ** (p - 1.0)) * math.exp(-(x**p))


def e2_lcdm(n_past: float, omega_m: float = 0.3) -> float:
    return omega_m * math.exp(3.0 * n_past) + 1.0 - omega_m


def e2_mts(n_past: float, b_mem: float, omega_m: float = 0.3) -> float:
    return e2_lcdm(n_past, omega_m) + b_mem * activation(n_past)


def trapz(values: list[tuple[float, float]]) -> float:
    return sum(0.5 * (y0 + y1) * (x1 - x0) for (x0, y0), (x1, y1) in zip(values, values[1:]))


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "51-FLRW-memory-current-contract.md", "det(Q) cubic FLRW memory-current contract"),
        (ROOT / "92-memory-stress-amplitude-prediction-attempt.md", "stress-exchange amplitude corridor"),
        (ROOT / "97-canonical-R-theorem-attempt.md", "canonical-R amplitude demotion"),
        (ROOT / "253-FLRW-reduction-of-topological-projector-or-Bmem-stays-closure.md", "topological projector FLRW reduction"),
        (ROOT / "254-rank-27-rank-2-cell-theorem-or-Bmem-closure-lock.md", "rank fraction theorem attempt"),
        (ROOT / "255-memory-stress-exchange-normalization-or-kappa-mem-free.md", "kappa normalization no-go"),
        (ROOT / "283-fixed-vs-kappa-short-smoke-readout.md", "fixed 2/27 vs kappa-free empirical readout"),
        (ROOT / "315-fullcov-noSH0ES-score-readout.md", "latest full-cov no-SH0ES score readout"),
        (SCORE_READOUT_RUN / "results" / "prior_edge_audit.csv", "latest fitted-B prior edge audit"),
        (SCORE_READOUT_RUN / "results" / "MTS_fixed_vs_baselines.csv", "latest fitted-B baseline comparisons"),
        (FIXED_KAPPA_READOUT_RUN / "results" / "score_readout.csv", "fixed 2/27 vs kappa score readout"),
        (ROOT / "scripts" / "FLRW_memory_projection_amplitude_contract.py", "this derivation audit"),
    ]
    return [{"source": relpath(path), "role": role, "exists": yes_no(path.exists())} for path, role in sources]


def fitted_b_rows() -> list[dict[str, str]]:
    rows = []
    for row in read_csv(SCORE_READOUT_RUN / "results" / "prior_edge_audit.csv"):
        if row["model"] == "MTS_fixed_p3_u3quarter" and row["parameter"] == "B_mem":
            rows.append(row)
    return rows


def parse_kappa_readout() -> dict[str, float]:
    score_rows = read_csv(FIXED_KAPPA_READOUT_RUN / "results" / "score_readout.csv")
    kappa_row = next(row for row in score_rows if row["readout"] == "kappa_best_fit")
    values = {}
    for key in ["B_mem", "kappa_mem", "fixed_Bmem"]:
        match = re.search(rf"{key}=([-+0-9.eE]+)", kappa_row["value"])
        if not match:
            raise ValueError(f"missing {key} in {kappa_row['value']}")
        values[key] = float(match.group(1))
    return values


def mathematical_identity_rows() -> list[dict[str, Any]]:
    f3 = 6.0 / (U3**3)
    return [
        {
            "identity": "FLRW_load_tensor_reduction",
            "equation": "Q^i_j = X_FLRW delta^i_j -> det(Q)=X_FLRW^3",
            "result": "p=3 shape follows if Q is parent-owned and isotropic",
            "status": "pass_conditional",
            "derivation_limit": "does not derive Q, X_FLRW, u3, rank, or kappa_mem",
        },
        {
            "identity": "no_clock_activation_shape",
            "equation": "X_FLRW=N/u3 -> F(N)=1-exp[-(N/u3)^3]",
            "result": f"F(0)=F'(0)=F''(0)=0 and F'''(0)={f3:.12g}",
            "status": "pass_analytic_given_X_equals_N_over_u3",
            "derivation_limit": "u3=1/4 remains conditional cell/no-clock route",
        },
        {
            "identity": "memory_source_budget",
            "equation": "Omega_mem=B_mem F; S_mem=dOmega_mem/dN=B_mem F'",
            "result": "integral_0^infinity S_mem dN = B_mem",
            "status": "pass_analytic",
            "derivation_limit": "integral identifies the budget but not the budget normalization",
        },
        {
            "identity": "effective_stress_conservation",
            "equation": "rho_mem'=3(rho_mem+p_mem) with N=ln(a0/a)",
            "result": "p_mem=-rho_mem+rho_mem'/3 gives conserved effective stress for supplied B_mem",
            "status": "pass_for_supplied_background",
            "derivation_limit": "Bianchi fixes pressure response, not B_mem",
        },
        {
            "identity": "LCDM_background_limit",
            "equation": "E_MTS^2=Omega_m e^(3N)+1-Omega_m+B_mem F(N)",
            "result": "B_mem -> 0 exactly returns LCDM background expansion",
            "status": "pass_analytic_and_runner_control",
            "derivation_limit": "background limit is proven, local GR and perturbations are not",
        },
        {
            "identity": "rank_fraction_amplitude_contract",
            "equation": "B_mem=kappa_mem Tr(P_active)/dim(V_cell)",
            "result": "B_mem=2/27 if dim(V_cell)=27, rank(P_active)=2, kappa_mem=1",
            "status": "theorem_target_not_derived",
            "derivation_limit": "rank, cell dimension, and stress normalization are still parent-action debts",
        },
    ]


def amplitude_budget_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = [
        {
            "branch_or_quantity": "rank_fraction_target",
            "B_mem": Q_RANK,
            "q_rank": Q_RANK,
            "kappa_implied": 1.0,
            "deviation_from_2over27": 0.0,
            "status": "strict_closure_target",
            "evidence": "q_rank=2/27 from rank-27/rank-2 theorem target, not parent-derived",
        }
    ]
    for row in fitted_b_rows():
        b_value = float(row["best_fit"])
        kappa = b_value / Q_RANK
        rows.append(
            {
                "branch_or_quantity": f"{row['release_branch']}_fitted_shape_fixed",
                "B_mem": b_value,
                "q_rank": Q_RANK,
                "kappa_implied": kappa,
                "deviation_from_2over27": b_value - Q_RANK,
                "status": "fitted_B_close_to_rank_fraction",
                "evidence": f"prior_edge_flag={row['edge_flag']}; distance_to_edge={row['distance_to_edge']}",
            }
        )
    kappa_readout = parse_kappa_readout()
    rows.append(
        {
            "branch_or_quantity": "DR2_kappa_free_short_smoke",
            "B_mem": kappa_readout["B_mem"],
            "q_rank": kappa_readout["fixed_Bmem"],
            "kappa_implied": kappa_readout["kappa_mem"],
            "deviation_from_2over27": kappa_readout["B_mem"] - Q_RANK,
            "status": "kappa_fit_lands_near_unity_but_not_theorem",
            "evidence": "checkpoint 283: kappa-free gains negligible chi2 and fails AIC/BIC tax",
        }
    )
    return rows


def conservation_lcdm_limit_rows() -> list[dict[str, Any]]:
    rows = []
    for n_past in [0.0, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0]:
        f_value = activation(n_past)
        f_prime = activation_prime(n_past)
        source = Q_RANK * f_prime
        rho = Q_RANK * f_value
        pressure = -rho + source / 3.0
        rows.append(
            {
                "N_past": n_past,
                "z": math.exp(n_past) - 1.0,
                "F": f_value,
                "F_prime": f_prime,
                "Omega_mem_fixed_2over27": rho,
                "source_dOmega_dN": source,
                "pressure_mem_effective": pressure,
                "rho_plus_p": rho + pressure,
                "E2_MTS_minus_E2_LCDM": e2_mts(n_past, Q_RANK) - e2_lcdm(n_past),
                "E2_Bmem_zero_minus_LCDM": e2_mts(n_past, 0.0) - e2_lcdm(n_past),
            }
        )
    grid = [(4.0 * index / 4000.0, Q_RANK * activation_prime(4.0 * index / 4000.0)) for index in range(4001)]
    integral = trapz(grid)
    rows.append(
        {
            "N_past": "integral_0_to_4",
            "z": math.exp(4.0) - 1.0,
            "F": activation(4.0),
            "F_prime": "",
            "Omega_mem_fixed_2over27": Q_RANK * activation(4.0),
            "source_dOmega_dN": integral,
            "pressure_mem_effective": "",
            "rho_plus_p": "",
            "E2_MTS_minus_E2_LCDM": "",
            "E2_Bmem_zero_minus_LCDM": "",
        }
    )
    return rows


def theorem_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause": "C1_same_parent_projector",
            "required_statement": "P_D is parent-defined, covariant/topological, and has both local-silent and FLRW-memory reductions",
            "current_status": "conditional",
            "if_satisfied": "one object can own both local silence and FLRW memory shape",
            "if_missing": "local and cosmology branches remain patched together",
        },
        {
            "clause": "C2_FLRW_load_tensor",
            "required_statement": "Q^i_j is parent-owned and reduces on FLRW to X_FLRW delta^i_j",
            "current_status": "conditional",
            "if_satisfied": "det(Q) gives cubic p=3 without fitting p",
            "if_missing": "p=3 remains structural closure",
        },
        {
            "clause": "C3_no_clock_cell_scale",
            "required_statement": "X_FLRW=N/u3 and u3=1/4 follow from a no-clock 3+1 cell/domain theorem",
            "current_status": "open_conditional",
            "if_satisfied": "transition scale stops being a fitted or inherited closure",
            "if_missing": "u3=1/4 remains closure/ablation discipline",
        },
        {
            "clause": "C4_cell_rank_fraction",
            "required_statement": "dim(V_cell)=27 and Tr(P_active)=2 are derived before seeing B_mem",
            "current_status": "fail_not_derived",
            "if_satisfied": "q_rank=2/27 becomes a parent fraction",
            "if_missing": "2/27 remains a theorem target",
        },
        {
            "clause": "C5_unit_stress_normalization",
            "required_statement": "metric variation/Ward identity fixes kappa_mem=1",
            "current_status": "fail_not_derived",
            "if_satisfied": "B_mem=q_rank rather than kappa_mem q_rank",
            "if_missing": "kappa_mem is the hidden amplitude",
        },
        {
            "clause": "C6_LCDM_limit",
            "required_statement": "B_mem -> 0 removes the projected memory stress and returns LCDM background",
            "current_status": "pass",
            "if_satisfied": "negative control is a true background limit",
            "if_missing": "runner could be testing a phenomenological add-on",
        },
        {
            "clause": "C7_local_silence",
            "required_statement": "local domains have F=0 and delta F^(1)=0, or equivalent projector-null stress",
            "current_status": "open",
            "if_satisfied": "FLRW memory does not automatically endanger local PPN",
            "if_missing": "no local-GR promotion",
        },
    ]


def no_go_rows() -> list[dict[str, Any]]:
    return [
        {
            "no_go": "Bianchi_does_not_fix_Bmem",
            "reason": "continuity fixes p_mem for a supplied rho_mem but scales linearly with B_mem",
            "surviving_use": "conservation and pressure-response consistency",
        },
        {
            "no_go": "determinant_does_not_fix_amplitude",
            "reason": "det(Q) explains a cubic invariant, not the normalization in H^2/H0^2",
            "surviving_use": "conditional p=3 derivation route",
        },
        {
            "no_go": "topology_alone_cannot_source_FLRW_bulk_stress",
            "reason": "metric-independent projectors can select channels but need a metric stress response to alter E^2",
            "surviving_use": "local silence and channel-count theorem target",
        },
        {
            "no_go": "empirical_closeness_is_not_derivation",
            "reason": "B_fit close to 2/27 is a clue; it does not prove dim=27, rank=2, or kappa=1",
            "surviving_use": "sharp target for further theorem work and robustness tests",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    source_ok = all(row["exists"] == "yes" for row in source_register_rows())
    budget = amplitude_budget_rows()
    fitted_close = all(abs(float(row["kappa_implied"]) - 1.0) < 0.02 for row in budget if "fitted_shape_fixed" in row["branch_or_quantity"])
    b0_limit_ok = all(
        abs(float(row["E2_Bmem_zero_minus_LCDM"])) < 1.0e-14
        for row in conservation_lcdm_limit_rows()
        if isinstance(row["E2_Bmem_zero_minus_LCDM"], float)
    )
    integral_row = conservation_lcdm_limit_rows()[-1]
    integral_ok = abs(float(integral_row["source_dOmega_dN"]) - Q_RANK) < 1.0e-8
    gates = [
        ("source_paths_exist", source_ok, "all cited source/checkpoint artifacts exist"),
        ("p3_shape_route", True, "det(Q) gives X^3 on FLRW if Q is parent-owned"),
        ("endpoint_double_zero", True, "F'(0)=F''(0)=0, so the memory source has a double zero at the local endpoint"),
        ("positive_sign_condition", True, "if kappa_mem>=0 and q_rank>=0 then B_mem>=0 and S_mem>=0"),
        ("source_integral_identity", integral_ok, "numerical integral of B F' matches B on [0,4] to tolerance"),
        ("LCDM_background_limit", b0_limit_ok, "B_mem=0 exactly returns LCDM E^2 in sampled checks"),
        ("empirical_B_near_2over27", fitted_close, "latest fitted B values imply kappa within 2 percent of unity"),
        ("rank27_rank2_parent_derived", False, "current work has not derived dim(V_cell)=27 or rank(P_active)=2"),
        ("kappa_mem_parent_derived", False, "current work has not derived unit stress normalization"),
        ("Bmem_2over27_parent_derived", False, "requires rank fraction plus kappa theorem; still closure-only"),
        ("local_GR_promotion_allowed", False, "local projector silence/PPN branch is not fully derived"),
        ("stable_evidence_allowed", False, "derivation contract and short-smoke results do not authorize stable evidence language"),
    ]
    return [{"gate": gate, "status": pass_fail(ok), "evidence": evidence} for gate, ok, evidence in gates]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "key": "status",
            "value": STATUS,
        },
        {
            "key": "claim_ceiling",
            "value": CLAIM_CEILING,
        },
        {
            "key": "derived_now",
            "value": "conditional_FLRW_shape; source_integral_budget; conserved_effective_pressure; LCDM_background_limit",
        },
        {
            "key": "not_derived",
            "value": "dim(V_cell)=27; rank(P_active)=2; kappa_mem=1; local_PPN_silence",
        },
        {
            "key": "best_next_theory_target",
            "value": "derive_kappa_mem_from_metric_variation_or_Ward_identity",
        },
        {
            "key": "best_next_empirical_target",
            "value": "run fixed_2over27_fullcov_noSH0ES_DR1_DR2_release_matrix_with_same_baselines",
        },
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=None)
    args = parser.parse_args()
    timestamp = args.timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    result_dir = run_dir / "results"
    result_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    missing = [row["source"] for row in sources if row["exists"] != "yes"]
    if missing:
        raise FileNotFoundError(f"missing source artifacts: {missing}")

    write_csv(result_dir / "source_register.csv", sources, ["source", "role", "exists"])
    write_csv(
        result_dir / "mathematical_identities.csv",
        mathematical_identity_rows(),
        ["identity", "equation", "result", "status", "derivation_limit"],
    )
    write_csv(
        result_dir / "amplitude_budget.csv",
        amplitude_budget_rows(),
        ["branch_or_quantity", "B_mem", "q_rank", "kappa_implied", "deviation_from_2over27", "status", "evidence"],
    )
    write_csv(
        result_dir / "conservation_LCDM_limit_checks.csv",
        conservation_lcdm_limit_rows(),
        [
            "N_past",
            "z",
            "F",
            "F_prime",
            "Omega_mem_fixed_2over27",
            "source_dOmega_dN",
            "pressure_mem_effective",
            "rho_plus_p",
            "E2_MTS_minus_E2_LCDM",
            "E2_Bmem_zero_minus_LCDM",
        ],
    )
    write_csv(
        result_dir / "theorem_contract_clauses.csv",
        theorem_contract_rows(),
        ["clause", "required_statement", "current_status", "if_satisfied", "if_missing"],
    )
    write_csv(result_dir / "no_go_lemmas.csv", no_go_rows(), ["no_go", "reason", "surviving_use"])
    write_csv(result_dir / "gate_results.csv", gate_rows(), ["gate", "status", "evidence"])
    write_csv(result_dir / "decision.csv", decision_rows(), ["key", "value"])

    payload = {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "stable_evidence_allowed": False,
        "parent_amplitude_derived": False,
        "lcdm_background_limit_proved": True,
        "next_action": "derive kappa_mem from a metric-variation/Ward identity or keep B_mem=2/27 closure-only",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "COMPLETE.txt").write_text(STATUS + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
