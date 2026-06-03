from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "boundary-Noether-scale-lock-attempt"
STATUS = "boundary_Noether_scale_lock_not_derived_Hstar_equals_H0_closure_locked_for_now"
CLAIM_CEILING = "scale_lock_closure_only_no_Bmem_parent_amplitude_promotion"
B_MEM_FIXED = 2.0 / 27.0
SOURCE_258 = ROOT / "runs" / "20260601-000076-fixed-vs-kappa-free-SN-BAO-short-smoke-implementation" / "results"
SOURCE_261 = ROOT / "runs" / "20260601-000079-Hstar-H0-scale-lock-and-local-silence-attempt" / "results"


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


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "221-Noether-source-identity-or-compact-PPN-closure-map.md", "Noether source identity template"),
        (ROOT / "234-boundary-metric-variation-and-Bianchi-ledger.md", "boundary/Bianchi stress ledger"),
        (ROOT / "260-C3-unit-stress-normalization-parent-action-attempt.md", "C3 stress split"),
        (ROOT / "261-Hstar-H0-scale-lock-and-local-silence-attempt.md", "Hstar target and local silence"),
        (SOURCE_258 / "fixed_vs_kappa_penalty.csv", "258 empirical anchor"),
        (SOURCE_261 / "scale_lock_gate_results.csv", "261 scale-lock gate results"),
    ]
    return [
        {
            "source": relpath(path),
            "role": role,
            "exists": "yes" if path.exists() else "no",
        }
        for path, role in sources
    ]


def boundary_noether_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "York_time_boundary_match",
            "candidate_equation": "K_boundary/3 = H_star",
            "what_it_can_do": "identifies H_star with a chosen boundary expansion rate",
            "why_not_theorem": "the boundary value K_boundary=3H0 is supplied as present-domain boundary data",
            "status": "closure_condition_not_parent_selection",
        },
        {
            "route": "microcanonical_boundary_action",
            "candidate_equation": "delta S/dH_star=0 imposes <K>/3-H_star=0",
            "what_it_can_do": "can make H_star equal a global/domain average expansion",
            "why_not_theorem": "the average equals H0 only with an extra present-boundary or saturation assumption",
            "status": "conditional_not_derived",
        },
        {
            "route": "Noether_dilation_charge",
            "candidate_equation": "Q_D = a pi_a + weights(fields) = constant",
            "what_it_can_do": "relates expansion, volume, and memory-sector canonical data",
            "why_not_theorem": "conservation preserves the charge but does not choose its numerical value",
            "status": "relation_not_scale_lock",
        },
        {
            "route": "Hamiltonian_constraint_with_memory",
            "candidate_equation": "H_constraint=0",
            "what_it_can_do": "relates matter, constant sector, curvature, and memory density on each solution",
            "why_not_theorem": "because F(0)=0 the present constraint is insensitive to H_star",
            "status": "no_go",
        },
        {
            "route": "global_sequestering_style_constraint",
            "candidate_equation": "partial S/partial H_star=0 sets H_star^2=<H^2>_W",
            "what_it_can_do": "could make H_star a global zero-mode and protect local silence",
            "why_not_theorem": "predicts a weighted historical average, not necessarily present H0",
            "status": "future_route_not_H0_derivation",
        },
        {
            "route": "flux_or_topological_charge_quantization",
            "candidate_equation": "H_star^2 proportional to integer flux / volume unit",
            "what_it_can_do": "could discretize allowed memory scales",
            "why_not_theorem": "does not select the observed H0 sector without an additional boundary selection rule",
            "status": "quantization_not_selection",
        },
    ]


def canonical_pair_rows() -> list[dict[str, Any]]:
    return [
        {
            "canonical_object": "boundary_volume",
            "symbol": "V_boundary ~ a^3",
            "conjugate": "York time / mean curvature K",
            "scale_lock_use": "can define H_boundary=K/3",
            "status": "kinematic_boundary_identity",
        },
        {
            "canonical_object": "memory_scale",
            "symbol": "H_star",
            "conjugate": "global/domain memory charge Q_mem",
            "scale_lock_use": "variation can relate H_star to Q_mem or boundary K",
            "status": "requires_new_parent_boundary_term",
        },
        {
            "canonical_object": "Noether_charge",
            "symbol": "Q_D or Q_T",
            "conjugate": "dilation/time-translation generator",
            "scale_lock_use": "can conserve a relation across the domain",
            "status": "does_not_choose_numeric_H0",
        },
        {
            "canonical_object": "present_H0",
            "symbol": "H0",
            "conjugate": "observed solution boundary datum",
            "scale_lock_use": "sets H_star if imposed as a boundary condition",
            "status": "data_or_closure_until_parent_selection_exists",
        },
    ]


def no_go_rows() -> list[dict[str, Any]]:
    return [
        {
            "lemma": "Noether_conservation_not_selection",
            "proof": "A Noether charge equation gives dQ/dt=0; it fixes evolution after initial/boundary data, not the numerical boundary value itself.",
            "consequence": "Noether symmetry alone cannot prove H_star=H0",
        },
        {
            "lemma": "York_time_boundary_data_no_go",
            "proof": "K/3=H0 at the present slice is the definition of the observed present boundary expansion.",
            "consequence": "H_star=K/3 becomes H_star=H0 only after imposing the present boundary condition",
        },
        {
            "lemma": "F_zero_boundary_no_go",
            "proof": "For the lead activation F(0)=0, the memory stress vanishes at the present normalization point.",
            "consequence": "the Hamiltonian/Friedmann constraint at N=0 cannot determine H_star",
        },
        {
            "lemma": "global_average_not_present_value",
            "proof": "A global constraint naturally returns a weighted average such as <H^2>_W, while H0 is a boundary value.",
            "consequence": "a sequestering route needs an extra theorem that the weighted average equals H0^2",
        },
        {
            "lemma": "local_silence_blocks_local_scale_field",
            "proof": "If the scale-lock variable is an ordinary local field coupled to the observed metric, local matter traces source it.",
            "consequence": "the scale-lock variable must be global/domain/topological or screened",
        },
    ]


def sufficient_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition": "S1_boundary_canonical_pair",
            "required_statement": "The parent action contains a boundary/domain canonical pair (V_D,K_D) and a memory pair (H_star,Q_mem).",
            "current_status": "not_built",
            "if_satisfied": "makes the scale-lock question a variational boundary equation",
        },
        {
            "condition": "S2_variation_locks_scale",
            "required_statement": "Variation yields H_star=K_D/3 without adding an independent scale or fit coefficient.",
            "current_status": "conditional_template_only",
            "if_satisfied": "H_star equals the domain expansion variable",
        },
        {
            "condition": "S3_parent_selects_present_domain",
            "required_statement": "The same parent equations select K_D=3H0 rather than taking it as observational boundary data.",
            "current_status": "not_derived",
            "if_satisfied": "turns H_star=H0 into a theorem",
        },
        {
            "condition": "S4_global_zero_mode_silence",
            "required_statement": "H_star is a global/domain zero-mode with no local trace response and no local fifth force.",
            "current_status": "conditional_requirement",
            "if_satisfied": "keeps local silence compatible",
        },
        {
            "condition": "S5_Bianchi_total_stress",
            "required_statement": "Boundary, memory, projector, and matter stresses are all retained so total stress is conserved.",
            "current_status": "ledger_exists_not_parent_solved",
            "if_satisfied": "prevents fake conservation from dropped boundary/projector stress",
        },
    ]


def branch_policy_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch": "strict_lead_closure",
            "formula": "B_mem = (2/27)*(H_star/H0)^2 with H_star=H0 imposed",
            "status": "allowed_closure_theorem_target",
            "claim_limit": "not parent-derived",
        },
        {
            "branch": "kappa_ablation",
            "formula": "B_mem = kappa_mem*(2/27)",
            "status": "allowed_diagnostic",
            "claim_limit": "extra parameter must pay AIC/BIC tax; 258 says it does not",
        },
        {
            "branch": "future_boundary_theorem",
            "formula": "H_star=K_D/3=H0 from parent boundary/Noether equations",
            "status": "theorem_target",
            "claim_limit": "requires S1-S5, especially S3",
        },
        {
            "branch": "global_average_scale",
            "formula": "H_star^2=<H^2>_W",
            "status": "future_nonlocal_route",
            "claim_limit": "must prove <H^2>_W=H0^2 or accept shifted amplitude",
        },
    ]


def claim_policy_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim": "Boundary/Noether derives H_star=H0 now",
            "status": "forbidden",
            "reason": "Noether conservation and boundary variation still require numerical boundary/selection data",
        },
        {
            "claim": "H_star=H0 is a disciplined closure condition",
            "status": "allowed",
            "reason": "it is exact, minimal, and 258 shows no empirical need for kappa freedom",
        },
        {
            "claim": "Noether route is dead",
            "status": "forbidden",
            "reason": "a real theorem target exists via boundary canonical pairs, but it is not built",
        },
        {
            "claim": "Scale-lock can be locally silent only as a global/domain zero-mode",
            "status": "allowed",
            "reason": "ordinary local trace-coupled scale field fails local C-silence",
        },
        {
            "claim": "Move on after this attempt unless new boundary equations are supplied",
            "status": "allowed",
            "reason": "repeating H_star=H0 without S3 would be circular",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "lead_branch": "MTS_2over27_no_clock_u3quarter",
            "meaning": (
                "The boundary/Noether route produces a clean theorem target but not the theorem. Noether identities conserve "
                "charges and boundary actions can match H_star to a domain York time, but the equality to the observed H0 still "
                "enters as boundary data unless a new parent selection equation is built. Therefore H_star=H0 is closure-locked for now."
            ),
            "next_target": "stop_repeating_scale_lock_move_to_rank_27_rank_2_or_CMB_bridge_or_build_new_boundary_equations_if_available",
        }
    ]


def empirical_anchor_rows() -> list[dict[str, Any]]:
    penalty = read_csv(SOURCE_258 / "fixed_vs_kappa_penalty.csv")
    if not penalty:
        return [{"quantity": "258_penalty", "value": "missing", "interpretation": "no empirical anchor imported"}]
    row = penalty[0]
    kappa = float(row["kappa_best_kappa_mem"])
    return [
        {
            "quantity": "kappa_best",
            "value": kappa,
            "interpretation": "free scale is close to one but not AIC/BIC promoted",
        },
        {
            "quantity": "Hstar_over_H0_if_ablation_used",
            "value": math.sqrt(kappa),
            "interpretation": "would be close to unity; clue only",
        },
        {
            "quantity": "AIC_tax_paid",
            "value": row["AIC_tax_paid"],
            "interpretation": "free scale fails AIC tax",
        },
        {
            "quantity": "BIC_tax_paid",
            "value": row["BIC_tax_paid"],
            "interpretation": "free scale fails BIC tax",
        },
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "boundary_Noether_attempts.csv": (
            boundary_noether_attempt_rows(),
            ["route", "candidate_equation", "what_it_can_do", "why_not_theorem", "status"],
        ),
        "boundary_canonical_pair_ledger.csv": (
            canonical_pair_rows(),
            ["canonical_object", "symbol", "conjugate", "scale_lock_use", "status"],
        ),
        "scale_lock_no_go_lemmas.csv": (
            no_go_rows(),
            ["lemma", "proof", "consequence"],
        ),
        "sufficient_boundary_theorem_contract.csv": (
            sufficient_theorem_rows(),
            ["condition", "required_statement", "current_status", "if_satisfied"],
        ),
        "empirical_anchor_from_258.csv": (
            empirical_anchor_rows(),
            ["quantity", "value", "interpretation"],
        ),
        "scale_lock_branch_policy.csv": (
            branch_policy_rows(),
            ["branch", "formula", "status", "claim_limit"],
        ),
        "claim_policy_after_262.csv": (
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
        "boundary_Noether_scale_lock_derived": False,
        "Hstar_equals_H0_status": "closure_locked_not_parent_derived",
        "recommended_pivot": "rank_27_rank_2_or_CMB_bridge_or_new_boundary_equations_only",
        "B_mem_fixed": B_MEM_FIXED,
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Attempt the boundary/Noether Hstar=H0 scale-lock theorem.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
