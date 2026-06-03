from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "arrow-semigroup-parent-time-attempt"
STATUS = "arrow_semigroup_conditionally_derives_3_to_1_parent_time_not_owned"
CLAIM_CEILING = "conditional_H_theorem_arrow_only_no_full_Bmem_or_local_GR_promotion"


Matrix = list[list[Fraction]]


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


def matmul(a: Matrix, b: Matrix) -> Matrix:
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def matadd(a: Matrix, b: Matrix) -> Matrix:
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def matsub(a: Matrix, b: Matrix) -> Matrix:
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def trace(a: Matrix) -> Fraction:
    return sum(a[i][i] for i in range(len(a)))


def matrix_equal(a: Matrix, b: Matrix) -> bool:
    return a == b


def matrix_string(a: Matrix) -> str:
    return "; ".join(",".join(str(value) for value in row) for row in a)


def identity(n: int) -> Matrix:
    return [[Fraction(1 if i == j else 0, 1) for j in range(n)] for i in range(n)]


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "292-relative-index-level-theorem-attempt.md", "conditional relative-index k=9"),
        (ROOT / "293-domain-topology-selection-attempt.md", "conditional B3 topology route"),
        (ROOT / "294-endpoint-occupancy-arrow-law-attempt.md", "projector-rank endpoint law and missing arrow"),
        (ROOT / "276-coherent-domain-projector-from-parent-variables.md", "SO(3) coherent projector context"),
    ]
    return [{"source": relpath(path), "role": role, "exists": "yes" if path.exists() else "no"} for path, role in sources]


def projector_data() -> dict[str, Matrix]:
    p_axis = identity(3)
    p_iso = [[Fraction(1, 3) for _ in range(3)] for _ in range(3)]
    residual = matsub(p_axis, p_iso)
    return {"P_axis": p_axis, "P_iso": p_iso, "R_aniso": residual}


def semigroup_algebra_rows() -> list[dict[str, Any]]:
    data = projector_data()
    p_axis = data["P_axis"]
    p_iso = data["P_iso"]
    residual = data["R_aniso"]
    return [
        {
            "object": "P_axis",
            "definition": "identity on resolved diagonal axis-load sector A",
            "exact_matrix": matrix_string(p_axis),
            "trace": trace(p_axis),
            "status": "early_endpoint_projector",
        },
        {
            "object": "P_iso",
            "definition": "(1/3)11^T scalar trace projector on A",
            "exact_matrix": matrix_string(p_iso),
            "trace": trace(p_iso),
            "status": "late_endpoint_projector",
        },
        {
            "object": "R_aniso",
            "definition": "I-P_iso anisotropic residual projector",
            "exact_matrix": matrix_string(residual),
            "trace": trace(residual),
            "status": "rank_defect_Delta_n_2",
        },
        {
            "object": "generator_L",
            "definition": "L=-gamma R_aniso on the axis-load sector",
            "exact_matrix": "-gamma*(I-P_iso)",
            "trace": "-2 gamma",
            "status": "conditional_positive_coarse_graining_generator",
        },
        {
            "object": "semigroup_solution",
            "definition": "Phi_tau=P_iso+exp(-gamma tau) R_aniso",
            "exact_matrix": "P_iso + exp(-gamma tau)*(I-P_iso)",
            "trace": "1+2 exp(-gamma tau)",
            "status": "P_axis_at_tau0_to_P_iso_as_tau_infinity",
        },
    ]


def monotonicity_check_rows() -> list[dict[str, Any]]:
    data = projector_data()
    p_axis = data["P_axis"]
    p_iso = data["P_iso"]
    residual = data["R_aniso"]
    zero = [[Fraction(0, 1) for _ in range(3)] for _ in range(3)]
    checks = [
        {
            "check": "P_iso_idempotent",
            "calculation": "P_iso^2=P_iso",
            "result": "pass" if matrix_equal(matmul(p_iso, p_iso), p_iso) else "fail",
            "meaning": "late endpoint is a true projector",
        },
        {
            "check": "R_aniso_idempotent",
            "calculation": "R_aniso^2=R_aniso",
            "result": "pass" if matrix_equal(matmul(residual, residual), residual) else "fail",
            "meaning": "anisotropic residual is a true projector",
        },
        {
            "check": "orthogonal_split",
            "calculation": "P_iso R_aniso=0 and P_iso+R_aniso=I",
            "result": (
                "pass"
                if matrix_equal(matmul(p_iso, residual), zero) and matrix_equal(matadd(p_iso, residual), p_axis)
                else "fail"
            ),
            "meaning": "axis sector splits into scalar plus anisotropic residual",
        },
        {
            "check": "rank_defect_trace",
            "calculation": "Tr(R_aniso)=Tr(P_axis)-Tr(P_iso)=2",
            "result": "pass" if trace(residual) == Fraction(2, 1) else "fail",
            "meaning": "Delta n=2 is the residual rank",
        },
        {
            "check": "residual_norm_decay",
            "calculation": "||R Phi_tau q||^2 = exp(-2 gamma tau)||R q||^2 for gamma>0",
            "result": "conditional_pass",
            "meaning": "anisotropic information decays monotonically along positive coarse-graining time",
        },
        {
            "check": "entropy_direction",
            "calculation": "for positive normalized q, dH/dtau=gamma sum_i (q_i-1/3) log(q_i/(1/3)) >= 0",
            "result": "conditional_pass",
            "meaning": "same direction is an H-theorem if q is interpreted as resolved axis weight",
        },
    ]
    return checks


def parent_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_item": "physical_coarse_graining_time",
            "needed_statement": "parent time tau is the monotone loss of resolved axis-load information",
            "current_status": "not_derived",
            "why_it_matters": "without this, Phi_tau is an observer/projection map, not dynamics",
        },
        {
            "contract_item": "positive_gamma",
            "needed_statement": "gamma>=0 follows from a parent positivity, entropy, or influence-functional principle",
            "current_status": "not_derived",
            "why_it_matters": "negative gamma reverses the arrow and amplifies anisotropy",
        },
        {
            "contract_item": "Ward_trace_coupling",
            "needed_statement": "only the scalar trace projector couples to FLRW stress after coarse-graining",
            "current_status": "partial_contract",
            "why_it_matters": "connects arrow endpoint to the cosmological memory source",
        },
        {
            "contract_item": "early_axis_resolution",
            "needed_statement": "early endpoint starts in the resolved axis-load sector rather than the scalar quotient",
            "current_status": "not_derived",
            "why_it_matters": "needed for n_early=3 as a physical endpoint, not a chosen initial basis",
        },
        {
            "contract_item": "local_silence",
            "needed_statement": "local bound domains either never carry the FLRW coarse-graining charge or project it to zero",
            "current_status": "not_derived",
            "why_it_matters": "cosmology arrow cannot be allowed to generate PPN-violating local sources",
        },
    ]


def route_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "pure_projector_algebra",
            "what_it_now_gives": "exact endpoints 3 and 1 plus Delta n=2",
            "remaining_failure": "no time direction",
            "status": "completed_by_294",
        },
        {
            "route": "SO3_equivariant_semigroup",
            "what_it_now_gives": "unique scalar fixed point and monotone decay of the 2D anisotropic residual under gamma>0",
            "remaining_failure": "gamma positivity and physical tau are not parent-derived",
            "status": "conditional_arrow_theorem",
        },
        {
            "route": "entropy_H_theorem",
            "what_it_now_gives": "resolved axis weights flow toward uniform scalar trace with nondecreasing entropy",
            "remaining_failure": "requires probabilistic/coarse-grained interpretation of axis weights",
            "status": "conditional_support",
        },
        {
            "route": "ordinary_reversible_action",
            "what_it_now_gives": "cannot by itself produce irreversible projection without environment/boundary/doubling",
            "remaining_failure": "needs open-system, boundary, or thermodynamic sector",
            "status": "no_go_for_plain_action",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    source_missing = [source for source in source_register_rows() if source["exists"] != "yes"]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not source_missing else "fail",
            "evidence": "all cited post-checkpoint sources exist" if not source_missing else ";".join(source["source"] for source in source_missing),
            "claim_effect": "audit traceable",
        },
        {
            "gate": "semigroup_constructed",
            "status": "pass",
            "evidence": "Phi_tau=P_iso+exp(-gamma tau)(I-P_iso)",
            "claim_effect": "arrow has an exact mathematical carrier",
        },
        {
            "gate": "monotone_3_to_1_arrow",
            "status": "conditional_pass",
            "evidence": "for gamma>0, anisotropic residual decays and endpoint trace goes 3 to 1",
            "claim_effect": "3 -> 1 is derivable if parent time is positive coarse-graining time",
        },
        {
            "gate": "entropy_H_theorem",
            "status": "conditional_pass",
            "evidence": "dH/dtau>=0 for positive normalized axis weights",
            "claim_effect": "arrow has a non-handwavy irreversibility criterion",
        },
        {
            "gate": "parent_time_derived",
            "status": "fail",
            "evidence": "no parent action yet identifies physical time with this coarse-graining semigroup",
            "claim_effect": "arrow not fully promoted",
        },
        {
            "gate": "positive_gamma_parent_owned",
            "status": "fail",
            "evidence": "gamma>=0 is required, not derived from the parent action",
            "claim_effect": "irreversibility remains a contract",
        },
        {
            "gate": "B_mem_derived",
            "status": "fail",
            "evidence": "2/27 follows only after conditional k=9, B3 topology, trace partition, endpoint projectors, and semigroup arrow",
            "claim_effect": "locked empirical closure retained",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "semigroup arrow does not prove q_loc suppression or PPN safety",
            "claim_effect": "no local-GR promotion",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "The missing arrow can be made into a precise conditional theorem. On the axis-load sector, "
                "Phi_tau=P_iso+exp(-gamma tau)(I-P_iso) maps the three resolved axis degrees toward the one scalar "
                "trace degree, with anisotropic residual norm decaying for gamma>0 and an entropy-production form for "
                "positive normalized axis weights. This derives 3 -> 1 if physical parent time is positive coarse-graining "
                "time. But that identification and gamma>=0 are not yet derived from the parent action."
            ),
            "next_target": "derive_positive_coarse_graining_time_from_parent_action_or_demote_2over27_to_closure_contract",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "semigroup_algebra.csv": (
            semigroup_algebra_rows(),
            ["object", "definition", "exact_matrix", "trace", "status"],
        ),
        "monotonicity_checks.csv": (
            monotonicity_check_rows(),
            ["check", "calculation", "result", "meaning"],
        ),
        "parent_contract.csv": (
            parent_contract_rows(),
            ["contract_item", "needed_statement", "current_status", "why_it_matters"],
        ),
        "route_status.csv": (
            route_status_rows(),
            ["route", "what_it_now_gives", "remaining_failure", "status"],
        ),
        "gate_results.csv": (
            gate_rows(),
            ["gate", "status", "evidence", "claim_effect"],
        ),
        "decision.csv": (
            decision_rows(),
            ["decision", "claim_ceiling", "meaning", "next_target"],
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
        "arrow_derived_conditionally": True,
        "parent_time_derived_now": False,
        "B_mem_derived_now": False,
        "local_GR_promoted_now": False,
        "next_target": "derive_positive_coarse_graining_time_from_parent_action_or_demote_2over27_to_closure_contract",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Arrow semigroup parent-time derivation attempt.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
