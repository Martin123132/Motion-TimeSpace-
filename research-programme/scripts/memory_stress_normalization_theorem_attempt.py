from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "memory-stress-normalization-theorem-attempt"
STATUS = "kappa1_not_unconditionally_derived_conditional_unit_stress_theorem_written"
CLAIM_CEILING = "conditional_kappa1_theorem_contract_no_parent_amplitude_promotion"
B_MEM_FIXED = 2.0 / 27.0
SOURCE_258 = ROOT / "runs" / "20260601-000076-fixed-vs-kappa-free-SN-BAO-short-smoke-implementation" / "results"


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
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def activation_samples() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    u3 = 0.25
    power = 3.0
    for n_past in [0.05, 0.10, 0.25, 0.50, 1.00, 2.00]:
        activation = 1.0 - math.exp(-((n_past / u3) ** power))
        derivative = (power * n_past ** (power - 1.0) / u3**power) * math.exp(-((n_past / u3) ** power))
        w_eff = -1.0 + derivative / (3.0 * activation) if activation > 0.0 else ""
        rows.append(
            {
                "N": n_past,
                "F_N": activation,
                "dF_dN": derivative,
                "w_mem_conserved": w_eff,
                "note": "for N=ln(a0/a)=ln(1+z), p_mem=-rho_mem+rho_mem_prime/3",
            }
        )
    return rows


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "253-FLRW-reduction-of-topological-projector-or-Bmem-stays-closure.md", "FLRW rank-fraction target"),
        (ROOT / "254-rank-27-rank-2-cell-theorem-or-Bmem-closure-lock.md", "rank-27/rank-2/kappa theorem target"),
        (ROOT / "255-memory-stress-exchange-normalization-or-kappa-mem-free.md", "previous kappa no-go checkpoint"),
        (ROOT / "258-fixed-vs-kappa-free-SN-BAO-short-smoke-implementation.md", "empirical fixed-vs-kappa readout"),
        (SOURCE_258 / "fixed_vs_kappa_penalty.csv", "machine fixed-vs-kappa penalty row"),
        (SOURCE_258 / "fit_summary.csv", "machine fit summary"),
    ]
    return [
        {
            "source": relpath(path),
            "role": role,
            "exists": "yes" if path.exists() else "no",
        }
        for path, role in sources
    ]


def conservation_identity_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "object": "memory_density",
            "formula": "rho_mem(N)=rho_c0*kappa_mem*(r_active/D_cell)*F(N)",
            "derived_status": "definition_of_FLRW_effective_stress",
            "normalization_status": "kappa_mem_not_fixed",
        },
        {
            "step": 2,
            "object": "Bianchi_FLRW",
            "formula": "d rho_mem/dN = 3*(rho_mem+p_mem), with N=ln(a0/a)",
            "derived_status": "standard_covariant_conservation_identity",
            "normalization_status": "homogeneous_in_kappa_mem",
        },
        {
            "step": 3,
            "object": "conserved_pressure",
            "formula": "p_mem(N)=-rho_mem(N)+(1/3)*d rho_mem/dN",
            "derived_status": "follows_directly_from_Bianchi",
            "normalization_status": "scales_with_kappa_mem",
        },
        {
            "step": 4,
            "object": "equation_of_state",
            "formula": "w_mem(N)=-1+(1/3)*d ln(F)/dN",
            "derived_status": "amplitude_cancels",
            "normalization_status": "cannot_fix_kappa_mem",
        },
        {
            "step": 5,
            "object": "F_shape",
            "formula": "F(N)=1-exp[-(N/u3)^3], u3=1/4",
            "derived_status": "conditional_shape_branch",
            "normalization_status": "F(infinity)=1_only_normalizes_shape",
        },
    ]


def no_go_rows() -> list[dict[str, Any]]:
    return [
        {
            "lemma": "Bianchi_homogeneity_no_go",
            "assumption": "rho_mem is multiplied by any constant kappa_mem",
            "result": "Bianchi fixes p_mem for that rho_mem but leaves kappa_mem arbitrary",
            "why_it_matters": "conservation cannot promote 2/27 into a parent amplitude",
        },
        {
            "lemma": "topological_projector_no_bulk_stress_no_go",
            "assumption": "P_D is metric-independent and purely topological",
            "result": "delta_g P_D=0 protects local silence but cannot create an FLRW stress amplitude by itself",
            "why_it_matters": "rank fraction is channel counting until coupled to metric stress",
        },
        {
            "lemma": "free_coupling_rescaling_no_go",
            "assumption": "S_mem contains an unfixed coefficient lambda_mem multiplying the memory invariant",
            "result": "lambda_mem rescales rho_mem and is observationally kappa_mem",
            "why_it_matters": "a parent action with a free memory coupling has not derived B_mem",
        },
        {
            "lemma": "Hamiltonian_constraint_no_go",
            "assumption": "E(0)=1 is enforced by adjusting the constant/background sector",
            "result": "the present-day normalization fixes the residual constant sector, not kappa_mem",
            "why_it_matters": "closure of the Friedmann budget is not an amplitude theorem",
        },
    ]


def sufficient_condition_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition": "C1_cell_state_space",
            "required_statement": "V_cell is parent-defined with dim(V_cell)=27",
            "current_status": "not_derived",
            "if_satisfied": "supplies D_cell=27 without numerology",
        },
        {
            "condition": "C2_active_projector_rank",
            "required_statement": "P_active^2=P_active and Tr(P_active)=2 in the FLRW memory sector",
            "current_status": "not_derived",
            "if_satisfied": "supplies r_active=2",
        },
        {
            "condition": "C3_unit_stress_normalization",
            "required_statement": "metric variation gives rho_mem/rho_c0=(Tr(P_active)/dim(V_cell))*F(N) with no independent lambda_mem",
            "current_status": "missing_core_theorem",
            "if_satisfied": "sets kappa_mem=1",
        },
        {
            "condition": "C4_shape_normalization",
            "required_statement": "F(0)=0 and F(infinity)=1 follow from the parent memory activation law",
            "current_status": "conditional_route",
            "if_satisfied": "prevents hiding amplitude inside F",
        },
        {
            "condition": "C5_conservation_pressure",
            "required_statement": "p_mem=-rho_mem+rho_mem_prime/3 is the stress pressure from variation or exchange identity",
            "current_status": "derived_as_effective_FLRW_identity_only",
            "if_satisfied": "keeps Bianchi consistency without extra tuning",
        },
    ]


def conditional_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem": "conditional_kappa1_theorem",
            "premises": "C1 and C2 and C3 and C4 and C5",
            "derivation": "B_mem=kappa_mem*r_active/D_cell = 1*2/27 = 2/27",
            "status": "valid_conditional_theorem_contract",
            "failure_mode": "if C3 fails, kappa_mem remains an amplitude closure or ablation parameter",
        },
        {
            "theorem": "unconditional_kappa1_theorem",
            "premises": "Bianchi plus topology plus rank fraction only",
            "derivation": "does not follow",
            "status": "rejected_for_now",
            "failure_mode": "Bianchi is homogeneous in amplitude and topology alone carries no stress units",
        },
    ]


def empirical_anchor_rows() -> list[dict[str, Any]]:
    penalty = read_csv(SOURCE_258 / "fixed_vs_kappa_penalty.csv")
    if not penalty:
        return [
            {
                "quantity": "258_penalty_row",
                "value": "missing",
                "interpretation": "no empirical anchor imported",
            }
        ]
    row = penalty[0]
    kappa = float(row["kappa_best_kappa_mem"])
    return [
        {
            "quantity": "fixed_B_mem",
            "value": row["fixed_B_mem"],
            "interpretation": "strict closure amplitude used in 258",
        },
        {
            "quantity": "kappa_best_fit",
            "value": row["kappa_best_kappa_mem"],
            "interpretation": "free amplitude wants kappa very close to unity but does not pay AIC/BIC tax",
        },
        {
            "quantity": "kappa_minus_1",
            "value": kappa - 1.0,
            "interpretation": "interesting clue, not a derivation",
        },
        {
            "quantity": "kappa_promoted",
            "value": row["kappa_promoted"],
            "interpretation": "kappa branch remains ablation only",
        },
    ]


def claim_policy_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim": "Bianchi derives kappa_mem=1",
            "status": "forbidden",
            "reason": "Bianchi fixes pressure/exchange consistency for any amplitude",
        },
        {
            "claim": "topology derives the FLRW amplitude by itself",
            "status": "forbidden",
            "reason": "metric-independent topology carries no bulk stress normalization",
        },
        {
            "claim": "kappa_mem=1 follows conditionally if C1-C5 are proved",
            "status": "allowed",
            "reason": "the theorem contract is now exact",
        },
        {
            "claim": "258 makes kappa_mem=1 empirical evidence",
            "status": "forbidden",
            "reason": "kappa-free did not pay the parameter tax",
        },
        {
            "claim": "fixed 2/27 remains the clean lead closure",
            "status": "allowed",
            "reason": "258 supports parsimony in SN+BAO only, not parent derivation",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "lead_branch": "MTS_2over27_no_clock_u3quarter",
            "meaning": (
                "The exact FLRW conservation law can be written and it proves that the pressure/exchange response is "
                "Bianchi-consistent for any kappa_mem. It therefore cannot fix the amplitude. A clean conditional theorem "
                "for kappa_mem=1 now exists, but its decisive premise is the missing unit stress normalization from the parent action."
            ),
            "next_target": "derive_or_reject_C3_unit_stress_normalization_from_parent_memory_action",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "FLRW_conservation_identity.csv": (
            conservation_identity_rows(),
            ["step", "object", "formula", "derived_status", "normalization_status"],
        ),
        "activation_pressure_samples.csv": (
            activation_samples(),
            ["N", "F_N", "dF_dN", "w_mem_conserved", "note"],
        ),
        "normalization_no_go_lemmas.csv": (
            no_go_rows(),
            ["lemma", "assumption", "result", "why_it_matters"],
        ),
        "kappa1_sufficient_conditions.csv": (
            sufficient_condition_rows(),
            ["condition", "required_statement", "current_status", "if_satisfied"],
        ),
        "conditional_theorem_status.csv": (
            conditional_theorem_rows(),
            ["theorem", "premises", "derivation", "status", "failure_mode"],
        ),
        "empirical_anchor_from_258.csv": (
            empirical_anchor_rows(),
            ["quantity", "value", "interpretation"],
        ),
        "claim_policy_after_259.csv": (
            claim_policy_rows(),
            ["claim", "status", "reason"],
        ),
        "decision.csv": (
            decision_rows(),
            ["decision", "claim_ceiling", "lead_branch", "meaning", "next_target"],
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
        "B_mem_fixed": B_MEM_FIXED,
        "kappa1_unconditionally_derived": False,
        "conditional_theorem_written": True,
        "next_target": "derive_or_reject_C3_unit_stress_normalization_from_parent_memory_action",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Attempt the kappa_mem=1 memory-stress normalization theorem.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
