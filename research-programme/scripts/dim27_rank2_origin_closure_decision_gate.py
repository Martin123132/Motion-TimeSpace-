from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from fractions import Fraction
from math import comb
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "dim27-rank2-origin-closure-decision-gate"
STATUS = "dim27_rank2_not_parent_derived_amplitude_frozen_as_explicit_closure"
CLAIM_CEILING = "amplitude_closure_decision_no_Bmem_parent_derivation_claim"
DIM_CELL = 27
RANK_ACTIVE = 2
Q_TRACE = Fraction(RANK_ACTIVE, DIM_CELL)
KAPPA_DR2 = 1.0061980866083466


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


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "331-trace-normalized-Hamiltonian-amplitude-contract.md", "trace-normalized amplitude factorization"),
        (ROOT / "337-exact-parent-pullback-selection-rule-gate.md", "conditional exact-readout theorem"),
        (ROOT / "341-indistinguishable-cell-quotient-parent-action-gate.md", "quotient state-space gate"),
        (ROOT / "342-finite-fibre-basis-relabeling-gate.md", "finite-fibre basis-relabeling gate"),
        (Path(__file__).resolve(), "this verifier"),
    ]
    return [
        {
            "source": relpath(path),
            "role": role,
            "exists": path.exists(),
            "issue": "" if path.exists() else "missing",
        }
        for path, role in sources
    ]


def dimension_candidate_rows() -> list[dict[str, Any]]:
    candidates = [
        {
            "candidate": "MTS_three_ternary_factors",
            "construction": "3 x 3 x 3",
            "dimension": 3 * 3 * 3,
            "semantic_fit": "high",
            "what_it_would_mean": "three ternary parent factors, plausibly motion/time/space or three finite fibre axes",
            "parent_derivation_status": "not_derived",
            "failure_mode": "does not prove why there are exactly three factors or why each is ternary",
        },
        {
            "candidate": "nine_by_three_factorization",
            "construction": "9 x 3",
            "dimension": 9 * 3,
            "semantic_fit": "medium",
            "what_it_would_mean": "one 9-state sector and one ternary sector",
            "parent_derivation_status": "degenerate_alternative",
            "failure_mode": "same dimension without the MTS three-factor interpretation",
        },
        {
            "candidate": "single_27_state_fibre",
            "construction": "27",
            "dimension": 27,
            "semantic_fit": "low",
            "what_it_would_mean": "one finite alphabet with 27 internal states",
            "parent_derivation_status": "degenerate_alternative",
            "failure_mode": "same denominator with no factor structure",
        },
        {
            "candidate": "three_by_nine_factorization",
            "construction": "3 x 9",
            "dimension": 3 * 9,
            "semantic_fit": "medium",
            "what_it_would_mean": "ternary selector times 9-dimensional sector",
            "parent_derivation_status": "degenerate_alternative",
            "failure_mode": "same dimension but different readout geometry",
        },
    ]
    return candidates


def rank_candidate_rows() -> list[dict[str, Any]]:
    candidates = [
        {
            "candidate": "arbitrary_rank2_projector",
            "construction": "choose any rank-2 subspace of V_cell",
            "rank": 2,
            "fits_q_trace": True,
            "parent_derivation_status": "not_derived",
            "failure_mode": "rank-2 choice is arbitrary; real Grassmannian dimension is 50",
        },
        {
            "candidate": "coordinate_pair_readout",
            "construction": "choose two coordinate basis states out of 27",
            "rank": 2,
            "fits_q_trace": True,
            "parent_derivation_status": "not_derived",
            "failure_mode": f"there are C(27,2)={comb(DIM_CELL, RANK_ACTIVE)} coordinate choices",
        },
        {
            "candidate": "screen_plane_with_two_frozen_reference_factors",
            "construction": "2D transverse plane inside one ternary factor with the other two factors fixed to reference states",
            "rank": 2,
            "fits_q_trace": True,
            "parent_derivation_status": "conditional_template",
            "failure_mode": "requires parent derivation of transverse plane plus two frozen reference states",
        },
        {
            "candidate": "full_screen_factor",
            "construction": "2D plane in one ternary factor tensored with all states of the other two factors",
            "rank": 2 * 3 * 3,
            "fits_q_trace": False,
            "parent_derivation_status": "wrong_rank_for_2over27",
            "failure_mode": "gives rank 18 and q_trace=2/3, not 2/27",
        },
        {
            "candidate": "two_endpoint_or_polarization_readout",
            "construction": "two boundary/end/polarization modes selected as a readout",
            "rank": 2,
            "fits_q_trace": True,
            "parent_derivation_status": "analogy_not_theorem",
            "failure_mode": "needs action-level reason these two modes and no marker counterterm are physical",
        },
    ]
    return candidates


def degeneracy_rows() -> list[dict[str, Any]]:
    return [
        {
            "degeneracy": "dimension_factorization_degeneracy",
            "count_or_dimension": "multiple factorizations",
            "example": "27, 9x3, 3x9, 3x3x3",
            "consequence": "dim=27 can be fit by several parent stories; parent action must select one",
        },
        {
            "degeneracy": "coordinate_rank2_choice_degeneracy",
            "count_or_dimension": comb(DIM_CELL, RANK_ACTIVE),
            "example": "351 coordinate two-state projectors",
            "consequence": "rank=2 is not unique without a source/readout rule",
        },
        {
            "degeneracy": "continuous_rank2_subspace_degeneracy",
            "count_or_dimension": 2 * (DIM_CELL - RANK_ACTIVE),
            "example": "real Grassmannian Gr(2,27) has dimension 50",
            "consequence": "basis-free rank-2 planes form a continuum unless selected by parent/boundary data",
        },
        {
            "degeneracy": "marker_extension_degeneracy",
            "count_or_dimension": "unbounded EFT coefficients",
            "example": "lambda_mem P_active plus higher marker-local terms",
            "consequence": "if marker is allowed, amplitude is a coupling, not a theorem",
        },
    ]


def closure_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "quantity": "B_mem",
            "previous_status": "locked empirical lead / theorem target",
            "new_status": "explicit closure value",
            "value_or_relation": "2/27",
            "reason": "dim=27 and rank=2 are not parent-derived after finite-fibre gate",
            "allowed_claim": "use as fixed closure branch and empirical target",
            "forbidden_claim": "parent-derived amplitude",
        },
        {
            "quantity": "epsilon_H",
            "previous_status": "conditionally derived under exact readout",
            "new_status": "explicit closure/fitted coupling unless parent theorem supplied",
            "value_or_relation": "1 in locked closure branch",
            "reason": "identity-current/no-counterterm route remains conditional",
            "allowed_claim": "set to 1 in locked branch and test robustness",
            "forbidden_claim": "unconditionally derived Hamiltonian normalization",
        },
        {
            "quantity": "q_trace",
            "previous_status": "conditional rank/dim ratio",
            "new_status": "conditional algebraic identity, not parent-owned",
            "value_or_relation": "rank(P_active)/dim(V_cell)=2/27",
            "reason": "ratio is exact if rank and dimension are assumed",
            "allowed_claim": "sharp algebraic target",
            "forbidden_claim": "derived from parent action",
        },
        {
            "quantity": "H_star/H0",
            "previous_status": "closure/theorem target",
            "new_status": "closure/theorem target",
            "value_or_relation": "1 in locked closure branch",
            "reason": "not addressed by dim/rank derivation",
            "allowed_claim": "fixed in current lead branch",
            "forbidden_claim": "parent-derived calibration",
        },
    ]


def decision_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition": "D1_dim27_parent_origin",
            "required_statement": "parent action derives exactly three ternary finite-fibre factors or equivalent unique 27D fibre",
            "status": "fail",
            "evidence": "only conditional templates and degenerate alternatives found",
        },
        {
            "condition": "D2_rank2_parent_origin",
            "required_statement": "parent action derives exactly a rank-2 source/readout plane with no marker action",
            "status": "fail",
            "evidence": "rank-2 readout remains selectable in many inequivalent ways",
        },
        {
            "condition": "D3_no_marker_counterterm",
            "required_statement": "parent action forbids marker-extended fibre and active-local EFT terms",
            "status": "fail",
            "evidence": "no no-marker theorem supplied",
        },
        {
            "condition": "D4_effective_stability",
            "required_statement": "effective corrections preserve finite-fibre basis gauge and closure value",
            "status": "fail",
            "evidence": "no correction-level Ward/quotient identity supplied",
        },
        {
            "condition": "D5_empirical_branch_retained",
            "required_statement": "locked 2/27 branch remains usable as a tested closure branch",
            "status": "pass",
            "evidence": "DR1/DR2 locked branch and corrected kappa corridor remain recorded in earlier gates",
        },
    ]


def no_go_rows() -> list[dict[str, Any]]:
    return [
        {
            "lemma": "dim27_factorization_no_go",
            "statement": "The number 27 alone does not select 3x3x3 over other finite-fibre factorizations.",
            "consequence": "three ternary factors require a parent theorem, not numerology.",
        },
        {
            "lemma": "rank2_selection_no_go",
            "statement": "Rank 2 has many coordinate and continuous subspace realizations in a 27D fibre.",
            "consequence": "the numerator 2 is not parent-owned without a source/readout selection theorem.",
        },
        {
            "lemma": "screen_plane_anchor_no_go",
            "statement": "A transverse 2-plane gives rank 2 only if all other tensor factors are anchored to reference states.",
            "consequence": "rank 2 is a readout construction, not a bulk fibre theorem, unless the anchors are derived.",
        },
        {
            "lemma": "closure_not_failure",
            "statement": "A fixed closure value can still define a serious test branch if it is labelled as closure.",
            "consequence": "the locked 2/27 branch remains valuable, but claims must stop at empirical/theorem target.",
        },
    ]


def gate_rows(
    sources: list[dict[str, Any]],
    dimension_candidates: list[dict[str, Any]],
    rank_candidates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    sources_ok = all(bool(row["exists"]) for row in sources)
    dim_template = next(row for row in dimension_candidates if row["candidate"] == "MTS_three_ternary_factors")
    rank_template = next(row for row in rank_candidates if row["candidate"] == "screen_plane_with_two_frozen_reference_factors")
    wrong_rank = next(row for row in rank_candidates if row["candidate"] == "full_screen_factor")
    return [
        {"gate": "source_paths_exist", "status": "pass" if sources_ok else "fail", "evidence": sources_ok},
        {
            "gate": "dim27_template_exists",
            "status": "pass" if int(dim_template["dimension"]) == DIM_CELL else "fail",
            "evidence": dim_template["construction"],
        },
        {
            "gate": "dim27_parent_derived",
            "status": "fail",
            "evidence": dim_template["failure_mode"],
        },
        {
            "gate": "rank2_template_exists",
            "status": "pass" if int(rank_template["rank"]) == RANK_ACTIVE else "fail",
            "evidence": rank_template["construction"],
        },
        {
            "gate": "rank2_parent_derived",
            "status": "fail",
            "evidence": rank_template["failure_mode"],
        },
        {
            "gate": "full_screen_factor_rejected_for_2over27",
            "status": "pass" if not bool(wrong_rank["fits_q_trace"]) else "fail",
            "evidence": f"rank={wrong_rank['rank']} not 2",
        },
        {
            "gate": "coordinate_rank2_degeneracy_identified",
            "status": "pass" if comb(DIM_CELL, RANK_ACTIVE) == 351 else "fail",
            "evidence": comb(DIM_CELL, RANK_ACTIVE),
        },
        {
            "gate": "continuous_rank2_degeneracy_identified",
            "status": "pass" if 2 * (DIM_CELL - RANK_ACTIVE) == 50 else "fail",
            "evidence": 2 * (DIM_CELL - RANK_ACTIVE),
        },
        {
            "gate": "marker_extension_forbidden",
            "status": "fail",
            "evidence": "marker-extended fibre remains legal unless parent forbids it",
        },
        {
            "gate": "effective_stability_parent_derived",
            "status": "fail",
            "evidence": "no effective Ward/quotient theorem supplied",
        },
        {
            "gate": "epsilon_H_parent_derived_unconditionally",
            "status": "fail",
            "evidence": "dim/rank/no-marker/Hstar/correction chain remains incomplete",
        },
        {
            "gate": "Bmem_parent_promotion_allowed",
            "status": "fail",
            "evidence": "D1-D4 fail",
        },
        {
            "gate": "amplitude_demoted_to_explicit_closure",
            "status": "pass",
            "evidence": "2/27 retained as locked empirical closure/theorem target, not parent-derived",
        },
        {
            "gate": "empirical_branch_retained",
            "status": "pass",
            "evidence": "closure demotion does not discard the DR1/DR2 locked 2/27 branch",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "The final dim/rank gate found useful conditional templates but no parent derivation. Dim=27 can be represented "
                "as 3x3x3, and rank=2 can be represented by a source/readout plane, but both are underdetermined without a "
                "parent variable theorem. Therefore the amplitude should be frozen as explicit closure: B_mem=2/27 remains "
                "the locked empirical lead/theorem target, not a parent-derived result."
            ),
            "next_target": "move_from_amplitude_derivation_to_empirical_and_other_theory_gates",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    result_dir = run_dir / "results"
    result_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    dimension_candidates = dimension_candidate_rows()
    rank_candidates = rank_candidate_rows()
    degeneracy = degeneracy_rows()
    closure = closure_status_rows()
    contract = decision_contract_rows()
    no_gos = no_go_rows()
    gates = gate_rows(sources, dimension_candidates, rank_candidates)
    decisions = decision_rows()

    outputs = {
        "source_register.csv": (sources, ["source", "role", "exists", "issue"]),
        "dimension_candidate_audit.csv": (
            dimension_candidates,
            [
                "candidate",
                "construction",
                "dimension",
                "semantic_fit",
                "what_it_would_mean",
                "parent_derivation_status",
                "failure_mode",
            ],
        ),
        "rank_candidate_audit.csv": (
            rank_candidates,
            ["candidate", "construction", "rank", "fits_q_trace", "parent_derivation_status", "failure_mode"],
        ),
        "degeneracy_audit.csv": (
            degeneracy,
            ["degeneracy", "count_or_dimension", "example", "consequence"],
        ),
        "closure_status_update.csv": (
            closure,
            ["quantity", "previous_status", "new_status", "value_or_relation", "reason", "allowed_claim", "forbidden_claim"],
        ),
        "decision_contract.csv": (
            contract,
            ["condition", "required_statement", "status", "evidence"],
        ),
        "no_go_lemmas.csv": (no_gos, ["lemma", "statement", "consequence"]),
        "gate_results.csv": (gates, ["gate", "status", "evidence"]),
        "decision.csv": (decisions, ["decision", "claim_ceiling", "meaning", "next_target"]),
    }
    for filename, (rows, fieldnames) in outputs.items():
        write_csv(result_dir / filename, rows, fieldnames)

    payload = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "results_dir": str(result_dir),
        "generated": list(outputs),
        "q_trace_identity": f"{Q_TRACE.numerator}/{Q_TRACE.denominator}",
        "dim27_template_exists": True,
        "rank2_template_exists": True,
        "dim27_parent_derived": False,
        "rank2_parent_derived": False,
        "marker_extension_forbidden": False,
        "epsilon_H_parent_derived_unconditionally": False,
        "Bmem_parent_derived": False,
        "amplitude_demoted_to_explicit_closure": True,
        "empirical_branch_retained": True,
        "next_target": "move_from_amplitude_derivation_to_empirical_and_other_theory_gates",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Dim-27/rank-2 origin and closure decision gate.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
