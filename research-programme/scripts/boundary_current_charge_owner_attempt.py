from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "boundary-current-charge-owner-attempt"
STATUS = "boundary_current_charge_owner_not_derived_exact_quantization_obstruction_identified"
CLAIM_CEILING = "relative_current_support_only_no_amplitude_or_local_GR_promotion"

R_TODAY = Fraction(1, 9)
R_EARLY = Fraction(1, 3)
DELTA_R = R_EARLY - R_TODAY
B_MEM = DELTA_R / 3


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


def fmt_fraction(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "71-relative-boundary-current-construction-attempt.md", "formal relative current J_rel=(j3,b2)"),
        (ROOT / "72-relative-current-action-owner-attempt.md", "closure action can impose d_rel J_rel=0 but not representative selection"),
        (ROOT / "109-boundary-charge-two-ninth-theorem-attempt.md", "first DeltaR=2/9 normalized-boundary-charge attempt"),
        (ROOT / "110-endpoint-charge-equation-attempt.md", "endpoint quadratic theorem target"),
        (ROOT / "278-admissible-domain-class-boundary-current-owner.md", "relative memory charge and admissible variations"),
        (ROOT / "286-memory-stress-normalization-scale-no-go.md", "amplitude scale no-go and exact parent contract"),
        (ROOT / "scripts" / "boundary_current_charge_owner_attempt.py", "this charge-owner attempt"),
    ]
    return [{"source": relpath(path), "role": role, "exists": "yes" if path.exists() else "no"} for path, role in sources]


def current_construction_rows() -> list[dict[str, Any]]:
    return [
        {
            "object": "relative_current",
            "definition": "J_B=(j_3,b_2) in relative degree 3",
            "equation": "d_rel J_B=(d j_3, i_star j_3-d_boundary b_2)=0",
            "what_is_owned": "closed relative class can be written/imposed",
            "what_is_not_owned": "physical representative and normalization",
            "status": "support",
        },
        {
            "object": "relative_charge",
            "definition": "Q_B[D]=integral_D j_3 - integral_boundaryD b_2",
            "equation": "delta_eta Q_B=0 for class-preserving deformations",
            "what_is_owned": "charge invariance under admissible variations",
            "what_is_not_owned": "initial class value and charge unit Q_*",
            "status": "support",
        },
        {
            "object": "normalized_charge",
            "definition": "R=Q_B/Q_*",
            "equation": "DeltaR=(Q_early-Q_today)/Q_*",
            "what_is_owned": "exact target language",
            "what_is_not_owned": "Q_* and endpoint charges",
            "status": "theorem_target",
        },
        {
            "object": "locked_amplitude_map",
            "definition": "B_mem=DeltaR/3",
            "equation": "DeltaR=2/9 -> B_mem=2/27",
            "what_is_owned": "conditional trace partition map",
            "what_is_not_owned": "Ward-fixed trace partition from parent action",
            "status": "conditional",
        },
    ]


def quantization_attempt_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    target_triplets = []
    for level in range(1, 28):
        for n_today in range(0, level + 1):
            for n_early in range(n_today, level + 1):
                r_today = Fraction(n_today, level)
                r_early = Fraction(n_early, level)
                if r_today == R_TODAY and r_early == R_EARLY:
                    target_triplets.append((level, n_today, n_early))

    for level, n_today, n_early in target_triplets:
        rows.append(
            {
                "route": "integral_relative_cohomology_level",
                "level_k": level,
                "n_today": n_today,
                "n_early": n_early,
                "R_today": fmt_fraction(Fraction(n_today, level)),
                "R_early": fmt_fraction(Fraction(n_early, level)),
                "DeltaR": fmt_fraction(Fraction(n_early - n_today, level)),
                "B_mem": fmt_fraction(Fraction(n_early - n_today, 3 * level)),
                "what_it_would_need": "parent action must derive the level family k=9m with endpoint occupancies n=(m,3m), preferably minimal k=9",
                "verdict": "works_arithmetically_not_derived",
            }
        )

    rows.extend(
        [
            {
                "route": "degree_counting_two_over_three_times_trace",
                "level_k": "",
                "n_today": "",
                "n_early": "",
                "R_today": "",
                "R_early": "",
                "DeltaR": "2/9",
                "B_mem": "2/27",
                "what_it_would_need": "action must turn form-degree and trace counts into charge weights",
                "verdict": "motivational_not_derivation",
            },
            {
                "route": "BF_or_integral_period_quantization",
                "level_k": "k",
                "n_today": "n_0",
                "n_early": "n_1",
                "R_today": "n_0/k",
                "R_early": "n_1/k",
                "DeltaR": "(n_1-n_0)/k",
                "B_mem": "(n_1-n_0)/(3k)",
                "what_it_would_need": "derive k=9 and n_1-n_0=2 from a Ward/index theorem",
                "verdict": "best_live_route_but_open",
            },
            {
                "route": "endpoint_quadratic_from_charge_action",
                "level_k": "",
                "n_today": "",
                "n_early": "",
                "R_today": "1/9",
                "R_early": "1/3",
                "DeltaR": "2/9",
                "B_mem": "2/27",
                "what_it_would_need": "derive 27R^2-12R+1=0 before inserting endpoint roots",
                "verdict": "formal_target_not_owner",
            },
        ]
    )
    return rows


def local_flrw_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch": "stationary_local_vacuum",
            "desired_current_class": "[J_B]=0 or exact",
            "charge_readout": "Q_B=0",
            "local_stress_risk": "none if topological/exact and uncoupled to wall stress",
            "status": "possible_conditional",
            "missing_parent_step": "prove P_loc J_B=0 from equations, not by domain choice",
        },
        {
            "branch": "coherent_FLRW",
            "desired_current_class": "[J_B] nontrivial",
            "charge_readout": "R=Q_B/Q_* in {1/9,1/3}",
            "local_stress_risk": "low if current is global/topological; Bianchi risk when it sources stress",
            "status": "possible_contract",
            "missing_parent_step": "derive endpoint occupancies and transition arrow",
        },
        {
            "branch": "boundary_transition",
            "desired_current_class": "class change or exchange b_2",
            "charge_readout": "DeltaR=2/9 target",
            "local_stress_risk": "high if b_2 is physical surface stress",
            "status": "open_danger",
            "missing_parent_step": "exchange current must be topological or exactly conserved with no PPN wall",
        },
        {
            "branch": "collapse_or_merger",
            "desired_current_class": "possible event source",
            "charge_readout": "not specified",
            "local_stress_risk": "unbounded unless event law exists",
            "status": "open",
            "missing_parent_step": "derive source/sink law for class changes",
        },
    ]


def source_tension_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "pure_topological_current",
            "advantage": "metric-independent, no PPN wall stress",
            "failure": "inert unless coupled to stress/background equations",
            "promotion_status": "support_only",
        },
        {
            "route": "physical_boundary_surface_stress",
            "advantage": "can carry amplitude",
            "failure": "risks PPN-sized wall stress and local GR failure",
            "promotion_status": "rejected_for_now",
        },
        {
            "route": "topological_current_with_Ward_trace_coupling",
            "advantage": "could be safe locally and source FLRW globally",
            "failure": "Ward identity and trace partition not derived",
            "promotion_status": "best_theorem_target",
        },
        {
            "route": "multiplier_imposed_closure",
            "advantage": "derives d_rel J_B=0 as Euler constraint",
            "failure": "does not select representative, level, endpoint charges, or arrow",
            "promotion_status": "formal_support",
        },
    ]


def endpoint_level_rows() -> list[dict[str, Any]]:
    return [
        {
            "target": "endpoint_roots",
            "required_value": "R_today=1/9, R_early=1/3",
            "equivalent_integer_data": "level k=9, occupancies n_today=1, n_early=3",
            "derived_now": "no",
            "noncircular_path": "index/Ward theorem fixes k=9 and allowed endpoint occupancies",
        },
        {
            "target": "endpoint_equation",
            "required_value": "27R^2-12R+1=0",
            "equivalent_integer_data": "3^3 R^2 - 3*4 R + 1=0",
            "derived_now": "no",
            "noncircular_path": "variation of parent boundary-charge action fixes coefficients 27,12,1",
        },
        {
            "target": "endpoint_arrow",
            "required_value": "1/3 -> 1/9",
            "equivalent_integer_data": "n=3 -> n=1 at fixed k=9",
            "derived_now": "no",
            "noncircular_path": "monotone boundary charge relaxation or event law with correct stability",
        },
        {
            "target": "trace_partition",
            "required_value": "B_mem=DeltaR/3",
            "equivalent_integer_data": "B_mem=(3-1)/(3*9)=2/27",
            "derived_now": "conditional_only",
            "noncircular_path": "Ward-fixed spatial trace coupling in Gamma_eff",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    source_missing = [row for row in source_register_rows() if row["exists"] != "yes"]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not source_missing else "fail",
            "evidence": "all sources present" if not source_missing else ";".join(row["source"] for row in source_missing),
            "claim_effect": "audit is traceable",
        },
        {
            "gate": "relative_current_owner",
            "status": "pass_formal",
            "evidence": "J_B=(j_3,b_2), d_rel J_B=0 can be written/imposed",
            "claim_effect": "conservation support retained",
        },
        {
            "gate": "charge_invariance",
            "status": "pass_conditional",
            "evidence": "Q_B[D]=int_D j_3-int_boundary b_2 invariant for class-preserving variations",
            "claim_effect": "boundary-current language is mathematically sharp",
        },
        {
            "gate": "charge_unit_Qstar_derived",
            "status": "fail",
            "evidence": "closure is invariant under J_B -> lambda J_B and Q_* -> lambda Q_*",
            "claim_effect": "normalized amplitude not fixed",
        },
        {
            "gate": "level_k9_derived",
            "status": "fail",
            "evidence": "k=9 is the needed integral-period level, but no Ward/index theorem supplies it",
            "claim_effect": "1/9 and 1/3 endpoints remain theorem targets",
        },
        {
            "gate": "endpoint_occupancies_derived",
            "status": "fail",
            "evidence": "n_today=1 and n_early=3 are arithmetically identified, not dynamically selected",
            "claim_effect": "DeltaR=2/9 not promoted",
        },
        {
            "gate": "topological_safety_vs_physical_source",
            "status": "open",
            "evidence": "pure topology is safe but inert; physical boundary stress can source amplitude but risks PPN",
            "claim_effect": "needs Ward trace coupling",
        },
        {
            "gate": "local_silence_derived",
            "status": "fail",
            "evidence": "local trivial class remains conditional",
            "claim_effect": "no local-GR promotion",
        },
        {
            "gate": "B_mem_derived",
            "status": "fail",
            "evidence": "requires Q_*, k=9, endpoint occupancies, endpoint arrow, and trace partition",
            "claim_effect": "B_mem=2/27 remains locked empirical closure/theorem target",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "The relative boundary current can own conservation/invariance language, but it does not yet own the normalized charge. "
                "Integral-period language makes the exact missing data visible: k=9, n_today=1, n_early=3, endpoint arrow 3->1, and trace partition 1/3. "
                "None of those are derived by d_rel closure alone."
            ),
            "next_target": "derive_k9_Ward_index_level_or_keep_Bmem_locked_empirical_closure",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "current_construction_contract.csv": (
            current_construction_rows(),
            ["object", "definition", "equation", "what_is_owned", "what_is_not_owned", "status"],
        ),
        "charge_quantization_attempts.csv": (
            quantization_attempt_rows(),
            ["route", "level_k", "n_today", "n_early", "R_today", "R_early", "DeltaR", "B_mem", "what_it_would_need", "verdict"],
        ),
        "local_FLRW_branch_tests.csv": (
            local_flrw_rows(),
            ["branch", "desired_current_class", "charge_readout", "local_stress_risk", "status", "missing_parent_step"],
        ),
        "topological_vs_physical_source_tension.csv": (
            source_tension_rows(),
            ["route", "advantage", "failure", "promotion_status"],
        ),
        "endpoint_integer_level_tests.csv": (
            endpoint_level_rows(),
            ["target", "required_value", "equivalent_integer_data", "derived_now", "noncircular_path"],
        ),
        "gate_results.csv": (gate_rows(), ["gate", "status", "evidence", "claim_effect"]),
        "decision.csv": (decision_rows(), ["decision", "claim_ceiling", "meaning", "next_target"]),
    }
    for filename, (rows, fieldnames) in outputs.items():
        write_csv(results_dir / filename, rows, fieldnames)

    payload = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(outputs),
        "R_today_target": fmt_fraction(R_TODAY),
        "R_early_target": fmt_fraction(R_EARLY),
        "DeltaR_target": fmt_fraction(DELTA_R),
        "B_mem_target": fmt_fraction(B_MEM),
        "exact_integer_data_needed": {"level_k": 9, "n_today": 1, "n_early": 3, "delta_n": 2},
        "B_mem_derived_now": False,
        "relative_current_status": "formal_conservation_support_not_charge_normalization_owner",
        "next_target": "derive_k9_Ward_index_level_or_keep_Bmem_locked_empirical_closure",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Boundary-current normalized charge owner attempt.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
