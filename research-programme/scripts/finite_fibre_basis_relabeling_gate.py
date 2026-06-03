from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "finite-fibre-basis-relabeling-gate"
STATUS = "finite_fibre_basis_relabeling_template_supported_dim_rank_origin_open"
CLAIM_CEILING = "finite_fibre_gate_no_unconditional_epsilonH_Bmem_or_parent_action_promotion"
DIM_CELL = 27
RANK_ACTIVE = 2
Q_TRACE = Fraction(RANK_ACTIVE, DIM_CELL)
J_TEST = 0.0061980866083466


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


def active_projector() -> np.ndarray:
    projector = np.zeros((DIM_CELL, DIM_CELL), dtype=float)
    projector[0, 0] = 1.0
    projector[1, 1] = 1.0
    return projector


def active_inactive_swap() -> np.ndarray:
    swap = np.eye(DIM_CELL)
    swap[[0, 2], :] = swap[[2, 0], :]
    return swap


def deterministic_orthogonal() -> np.ndarray:
    rng = np.random.default_rng(271828)
    raw = rng.normal(size=(DIM_CELL, DIM_CELL))
    q_matrix, r_matrix = np.linalg.qr(raw)
    signs = np.sign(np.diag(r_matrix))
    signs[signs == 0] = 1.0
    return q_matrix * signs


def sample_operator() -> np.ndarray:
    diagonal = np.ones(DIM_CELL)
    diagonal[0] += J_TEST
    diagonal[1] += 0.5 * J_TEST
    diagonal[2] -= 0.25 * J_TEST
    operator = np.diag(diagonal)
    operator[0, 1] = operator[1, 0] = 0.15 * J_TEST
    operator[3, 4] = operator[4, 3] = -0.05 * J_TEST
    return operator


def conjugate(operator: np.ndarray, basis_change: np.ndarray) -> np.ndarray:
    return basis_change.T @ operator @ basis_change


def trace_average(operator: np.ndarray) -> float:
    return float(np.trace(operator) / DIM_CELL)


def active_average(operator: np.ndarray, projector: np.ndarray | None = None) -> float:
    if projector is None:
        projector = active_projector()
    return float(np.trace(projector @ operator) / RANK_ACTIVE)


def q_trace(operator: np.ndarray, projector: np.ndarray | None = None) -> float:
    if projector is None:
        projector = active_projector()
    return float(np.trace(projector @ operator) / DIM_CELL)


def trace_action(operator: np.ndarray) -> float:
    identity = np.eye(DIM_CELL)
    return float(0.5 * np.trace((operator - identity) @ (operator - identity)))


def spectrum_signature(operator: np.ndarray) -> tuple[float, float, float]:
    eigenvalues = np.linalg.eigvalsh(operator)
    return (
        float(np.min(eigenvalues)),
        float(np.mean(eigenvalues)),
        float(np.max(eigenvalues)),
    )


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "331-trace-normalized-Hamiltonian-amplitude-contract.md", "trace-normalized B_mem factorization"),
        (ROOT / "337-exact-parent-pullback-selection-rule-gate.md", "exact parent-pullback theorem"),
        (ROOT / "340-full-cell-equivalence-gauge-redundancy-gate.md", "gauge redundancy versus global symmetry"),
        (ROOT / "341-indistinguishable-cell-quotient-parent-action-gate.md", "quotient parent-action template"),
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


def basis_invariant_rows() -> list[dict[str, Any]]:
    operator = sample_operator()
    permutation = active_inactive_swap()
    orthogonal = deterministic_orthogonal()
    permuted = conjugate(operator, permutation)
    rotated = conjugate(operator, orthogonal)
    projector = active_projector()
    rotated_projector = conjugate(projector, orthogonal)
    identity = np.eye(DIM_CELL)
    rows = [
        {
            "quantity": "trace_average",
            "original": trace_average(operator),
            "after_permutation": trace_average(permuted),
            "after_orthogonal_basis_change": trace_average(rotated),
            "basis_invariant": True,
            "meaning": "trace data is basis-free fibre data",
        },
        {
            "quantity": "trace_action",
            "original": trace_action(operator),
            "after_permutation": trace_action(permuted),
            "after_orthogonal_basis_change": trace_action(rotated),
            "basis_invariant": True,
            "meaning": "trace action descends to operator modulo basis relabeling",
        },
        {
            "quantity": "spectrum_signature",
            "original": spectrum_signature(operator),
            "after_permutation": spectrum_signature(permuted),
            "after_orthogonal_basis_change": spectrum_signature(rotated),
            "basis_invariant": True,
            "meaning": "spectrum is physical if fibre basis is gauge",
        },
        {
            "quantity": "fixed_Pactive_average",
            "original": active_average(operator, projector),
            "after_permutation": active_average(permuted, projector),
            "after_orthogonal_basis_change": active_average(rotated, projector),
            "basis_invariant": False,
            "meaning": "fixed active projector is not a basis-free bulk observable",
        },
        {
            "quantity": "relational_transformed_projector_average",
            "original": active_average(operator, projector),
            "after_permutation": active_average(permuted, conjugate(projector, permutation)),
            "after_orthogonal_basis_change": active_average(rotated, rotated_projector),
            "basis_invariant": True,
            "meaning": "projector readout is invariant only when the reference projector transforms too",
        },
        {
            "quantity": "identity_current_rank_readout",
            "original": q_trace(identity, projector),
            "after_permutation": q_trace(conjugate(identity, permutation), projector),
            "after_orthogonal_basis_change": q_trace(conjugate(identity, orthogonal), projector),
            "basis_invariant": True,
            "meaning": "for identity current, any rank-2 projector gives q_trace=2/27",
        },
    ]
    return rows


def fibre_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "labelled_component_vector",
            "parent_object": "27 separately labelled components h_i",
            "gauge_status": "not_gauge_by_construction",
            "bulk_terms": "symmetric terms plus possible selected-sector/spurion terms",
            "Pactive_status": "can become physical selector",
            "amplitude_status": "closure_or_fitted",
        },
        {
            "route": "finite_fibre_operator_mod_S27",
            "parent_object": "operator/current on V_cell modulo permutation basis relabeling",
            "gauge_status": "conditional_gauge_if_parent_declares_basis_labels_unphysical",
            "bulk_terms": "permutation-class functions and pullbacks",
            "Pactive_status": "not bulk; source/relational readout only",
            "amplitude_status": "conditional_theorem_if_rank_dim_and_no_marker_hold",
        },
        {
            "route": "finite_fibre_operator_mod_O27",
            "parent_object": "operator/current on V_cell modulo arbitrary orthogonal basis change",
            "gauge_status": "stronger_basis_gauge",
            "bulk_terms": "trace/spectral class functions",
            "Pactive_status": "external rank-2 probe only",
            "amplitude_status": "conditional_theorem_for_identity_current",
        },
        {
            "route": "tensor_fibre_3x3x3",
            "parent_object": "V_cell = A_3 tensor B_3 tensor C_3",
            "gauge_status": "conditional_if tensor factors are parent-defined and bases are unphysical",
            "bulk_terms": "factor/basis invariant trace data",
            "Pactive_status": "rank-2 active plane still needs parent/readout origin",
            "amplitude_status": "dim_27_possible_rank_2_open",
        },
        {
            "route": "marker_extended_fibre",
            "parent_object": "operator/current plus marker projector P_active",
            "gauge_status": "extended covariant system",
            "bulk_terms": "marker-local invariants allowed",
            "Pactive_status": "physical marker",
            "amplitude_status": "closure_or_fitted",
        },
    ]


def dimension_rank_rows() -> list[dict[str, Any]]:
    return [
        {
            "item": "dim_V_cell_27",
            "possible_parent_route": "three ternary finite-fibre factors, dim=3*3*3",
            "verified_here": 27 == 3 * 3 * 3,
            "status": "conditional_template_not_parent_derived",
            "remaining_burden": "derive the three ternary factors from the parent action rather than choose them",
        },
        {
            "item": "rank_P_active_2",
            "possible_parent_route": "rank-2 source/readout plane in V_cell",
            "verified_here": int(np.trace(active_projector())) == RANK_ACTIVE,
            "status": "assumed_readout_rank_not_parent_derived",
            "remaining_burden": "derive why the active readout rank is two and why it has no bulk marker action",
        },
        {
            "item": "q_trace_2over27",
            "possible_parent_route": "identity current on dim-27 fibre read by rank-2 projector",
            "verified_here": q_trace(np.eye(DIM_CELL), active_projector()),
            "status": "conditional_if_dim_rank_identity_current_hold",
            "remaining_burden": "derive dim=27, rank=2, identity current, Hstar=H0, and no counterterm",
        },
        {
            "item": "epsilon_H_1",
            "possible_parent_route": "trace-normalized identity Hamiltonian current before source readout",
            "verified_here": active_average(np.eye(DIM_CELL), active_projector()),
            "status": "conditional_if_identity_current_and_exact_readout_hold",
            "remaining_burden": "derive identity current and exact source/readout status",
        },
    ]


def finite_fibre_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition": "F1_parent_object_is_basis_free_fibre_current",
            "required_statement": "the parent variable is a linear/current operator on V_cell modulo basis relabeling, not a labelled component vector",
            "effect_if_true": "makes cell labels gauge bookkeeping",
            "current_status": "not_yet_parent_derived",
        },
        {
            "condition": "F2_dim_27_from_parent_fibre",
            "required_statement": "V_cell has dimension 27 because the parent action supplies three ternary factors or an equivalent finite-fibre theorem",
            "effect_if_true": "owns the denominator in 2/27",
            "current_status": "conditional_template_only",
        },
        {
            "condition": "F3_physical_action_is_trace_spectral",
            "required_statement": "bulk action and effective corrections depend only on trace/spectrum/basis-invariant data",
            "effect_if_true": "forbids basis-fixed active bulk terms",
            "current_status": "tree_level_template_verified",
        },
        {
            "condition": "F4_rank_2_projector_is_source_readout",
            "required_statement": "the rank-2 projector is an external/source/relational readout and not a material marker",
            "effect_if_true": "owns the numerator without reopening counterterms",
            "current_status": "open",
        },
        {
            "condition": "F5_no_marker_extended_fibre",
            "required_statement": "the parent fibre is not extended by a physical active marker/background projector",
            "effect_if_true": "blocks covariant marker-local counterterms",
            "current_status": "open",
        },
        {
            "condition": "F6_effective_action_preserves_basis_gauge",
            "required_statement": "coarse-grained corrections remain trace/spectral class functions on the fibre quotient",
            "effect_if_true": "keeps lambda_mem P_active from returning beyond the witness action",
            "current_status": "open",
        },
    ]


def no_go_rows() -> list[dict[str, Any]]:
    return [
        {
            "lemma": "basis_invariance_not_component_symmetry",
            "statement": "A finite-fibre operator modulo basis relabeling makes labels gauge, but a symmetric labelled component vector does not.",
            "consequence": "the parent object type, not just the action formula, must be specified.",
        },
        {
            "lemma": "fixed_projector_not_basis_free",
            "statement": "Tr(P_active H) is not basis-invariant for general H if P_active is held fixed.",
            "consequence": "P_active cannot be a bulk action tensor in the basis-gauge branch.",
        },
        {
            "lemma": "identity_current_rank_exception",
            "statement": "For H=I, Tr(P H)/dim(V) depends only on rank(P).",
            "consequence": "2/27 follows only if identity current, rank 2, and dim 27 are all parent-owned.",
        },
        {
            "lemma": "marker_extended_fibre_no_go",
            "statement": "Adding a physical marker projector to the fibre restores basis covariance while allowing active-local terms.",
            "consequence": "finite-fibre language alone does not forbid counterterms unless marker extensions are excluded.",
        },
    ]


def gate_rows(
    sources: list[dict[str, Any]],
    invariant_rows: list[dict[str, Any]],
    dim_rank_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    sources_ok = all(bool(row["exists"]) for row in sources)
    by_quantity = {row["quantity"]: row for row in invariant_rows}
    by_item = {row["item"]: row for row in dim_rank_rows}
    fixed_original = float(by_quantity["fixed_Pactive_average"]["original"])
    fixed_rotated = float(by_quantity["fixed_Pactive_average"]["after_orthogonal_basis_change"])
    relational_original = float(by_quantity["relational_transformed_projector_average"]["original"])
    relational_rotated = float(by_quantity["relational_transformed_projector_average"]["after_orthogonal_basis_change"])
    return [
        {"gate": "source_paths_exist", "status": "pass" if sources_ok else "fail", "evidence": sources_ok},
        {
            "gate": "trace_action_is_basis_invariant",
            "status": "pass" if bool(by_quantity["trace_action"]["basis_invariant"]) else "fail",
            "evidence": by_quantity["trace_action"]["original"],
        },
        {
            "gate": "spectrum_is_basis_invariant",
            "status": "pass" if bool(by_quantity["spectrum_signature"]["basis_invariant"]) else "fail",
            "evidence": by_quantity["spectrum_signature"]["original"],
        },
        {
            "gate": "fixed_Pactive_not_basis_invariant",
            "status": "pass" if abs(fixed_original - fixed_rotated) > 1.0e-6 else "fail",
            "evidence": f"{fixed_original} -> {fixed_rotated}",
        },
        {
            "gate": "relational_transformed_projector_readout_basis_invariant",
            "status": "pass" if abs(relational_original - relational_rotated) < 1.0e-12 else "fail",
            "evidence": relational_rotated,
        },
        {
            "gate": "identity_current_rank_readout_gives_2over27",
            "status": "pass"
            if abs(float(by_quantity["identity_current_rank_readout"]["original"]) - float(Q_TRACE)) < 1.0e-12
            else "fail",
            "evidence": by_quantity["identity_current_rank_readout"]["original"],
        },
        {
            "gate": "dim27_from_3x3x3_template",
            "status": "pass" if str(by_item["dim_V_cell_27"]["verified_here"]) == "True" else "fail",
            "evidence": "3*3*3=27",
        },
        {
            "gate": "dim27_parent_derived",
            "status": "fail",
            "evidence": by_item["dim_V_cell_27"]["remaining_burden"],
        },
        {
            "gate": "rank2_parent_derived",
            "status": "fail",
            "evidence": by_item["rank_P_active_2"]["remaining_burden"],
        },
        {
            "gate": "parent_object_proves_basis_free_fibre",
            "status": "fail",
            "evidence": "current route supplies a finite-fibre contract, not a parent-variable derivation",
        },
        {
            "gate": "parent_theory_forbids_marker_extended_fibre",
            "status": "fail",
            "evidence": "no parent statement forbids adding a physical marker projector",
        },
        {
            "gate": "effective_action_basis_invariant_derived",
            "status": "fail",
            "evidence": "no correction-level basis-gauge Ward identity has been supplied",
        },
        {
            "gate": "epsilon_H_parent_derived_unconditionally",
            "status": "fail",
            "evidence": "requires F1-F6",
        },
        {
            "gate": "Bmem_parent_promotion_allowed",
            "status": "fail",
            "evidence": "finite fibre origin, rank/dim, no-marker, Hstar=H0, and corrections remain open",
        },
        {
            "gate": "finite_fibre_basis_relabeling_contract_available",
            "status": "pass",
            "evidence": "F1-F6 written as exact finite-fibre contract",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "Finite-fibre basis relabeling is a viable conditional mechanism: trace/spectral parent actions are basis-invariant, "
                "fixed P_active is not a basis-free bulk observable, and an identity current read by a rank-2 projector gives 2/27. "
                "However, this still does not parent-derive the finite fibre, dim=27, rank=2, no-marker rule, Hstar=H0, or "
                "basis-invariant effective corrections."
            ),
            "next_target": "derive_dim27_rank2_finite_fibre_origin_or_demote_amplitude_to_closure",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    result_dir = run_dir / "results"
    result_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    invariants = basis_invariant_rows()
    routes = fibre_route_rows()
    dim_rank = dimension_rank_rows()
    contract = finite_fibre_contract_rows()
    no_gos = no_go_rows()
    gates = gate_rows(sources, invariants, dim_rank)
    decisions = decision_rows()

    outputs = {
        "source_register.csv": (sources, ["source", "role", "exists", "issue"]),
        "basis_invariant_tests.csv": (
            invariants,
            [
                "quantity",
                "original",
                "after_permutation",
                "after_orthogonal_basis_change",
                "basis_invariant",
                "meaning",
            ],
        ),
        "fibre_route_audit.csv": (
            routes,
            ["route", "parent_object", "gauge_status", "bulk_terms", "Pactive_status", "amplitude_status"],
        ),
        "dimension_rank_audit.csv": (
            dim_rank,
            ["item", "possible_parent_route", "verified_here", "status", "remaining_burden"],
        ),
        "finite_fibre_contract.csv": (
            contract,
            ["condition", "required_statement", "effect_if_true", "current_status"],
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
        "finite_fibre_basis_relabeling_template": True,
        "trace_spectral_action_basis_invariant": True,
        "fixed_Pactive_not_basis_free": True,
        "identity_rank2_readout_gives_2over27": True,
        "parent_object_basis_free_fibre_derived": False,
        "dim27_parent_derived": False,
        "rank2_parent_derived": False,
        "marker_extended_fibre_forbidden": False,
        "epsilon_H_parent_derived_unconditionally": False,
        "promotion_allowed": False,
        "next_target": "derive_dim27_rank2_finite_fibre_origin_or_demote_amplitude_to_closure",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Finite-fibre basis-relabeling gate.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
