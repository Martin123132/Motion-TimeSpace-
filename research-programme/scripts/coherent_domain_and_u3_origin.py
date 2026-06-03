#!/usr/bin/env python3
"""Try to constrain the coherent domain D and the transition scale u3."""

from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]

SOURCE_PATHS = {
    "53_projection_doc": Path("53-coherent-projection-local-silence-gate.md"),
    "53_status": Path("runs/20260531-103107-coherent-projection-local-silence-gate/status.json"),
    "53_projection_ledger": Path(
        "runs/20260531-103107-coherent-projection-local-silence-gate/results/projection_candidate_ledger.csv"
    ),
    "53_equation_chain": Path(
        "runs/20260531-103107-coherent-projection-local-silence-gate/results/coherent_projection_equation_chain.csv"
    ),
    "53_local_tests": Path(
        "runs/20260531-103107-coherent-projection-local-silence-gate/results/local_silence_gate_tests.csv"
    ),
    "53_gates": Path("runs/20260531-103107-coherent-projection-local-silence-gate/results/gate_results.csv"),
}

SAMPLE_N = [0.05, 0.1, 0.2, 0.21500703361675252, 0.5, 1.0]


def absolute_source(key: str) -> Path:
    return POST_CHECKPOINT / SOURCE_PATHS[key]


def load_json(key: str) -> dict[str, Any]:
    return json.loads(absolute_source(key).read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, relative_path in SOURCE_PATHS.items():
        absolute_path = POST_CHECKPOINT / relative_path
        rows.append(
            {
                "source_key": key,
                "relative_path": str(relative_path),
                "absolute_path": str(absolute_path),
                "exists": absolute_path.exists(),
            }
        )
    missing = [row["absolute_path"] for row in rows if not row["exists"]]
    if missing:
        raise FileNotFoundError("missing source files: " + "; ".join(missing))
    return rows


def activation(n_load: float, u_scale: float) -> float:
    return 1.0 - math.exp(-((max(n_load, 0.0) / u_scale) ** 3.0))


def domain_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "maximal_volume_coherent_domain",
            "definition": "D is the largest connected domain over which <theta>_D has one coherent sign and stable averaging",
            "status": "best_contract_candidate",
            "FLRW_behavior": "the whole homogeneous slice or causal patch is coherent with <theta>_D=3H",
            "local_behavior": "bound stationary domains have <theta>_D approximately 0",
            "non_circularity": "defined by volume-flow coherence, not by observed PPN residuals",
            "gap": "maximal connected domain and boundary rule are not derived from parent action",
        },
        {
            "candidate": "turnaround_or_virial_boundary_domain",
            "definition": "D is bounded by the surface where coherent expansion decouples or volume growth averages to zero",
            "status": "plausible_local_silence_rule",
            "FLRW_behavior": "unbound cosmic flow remains outside bound domains",
            "local_behavior": "solar-system/galaxy interiors are silent if bound volumes are stable",
            "non_circularity": "uses physical bound/unbound split",
            "gap": "needs parent criterion for binding, not Newtonian/GR import",
        },
        {
            "candidate": "causal_horizon_domain",
            "definition": "D is the causal/horizon patch of the observer congruence",
            "status": "too_broad_for_local_silence",
            "FLRW_behavior": "preserves cosmological coherence",
            "local_behavior": "does not by itself separate bound local systems",
            "non_circularity": "horizon is physical but not enough",
            "gap": "must still define subdomain decoupling",
        },
        {
            "candidate": "fixed_smoothing_scale_domain",
            "definition": "D is chosen with a smoothing length that makes local tests pass",
            "status": "rejected_rescue_knob",
            "FLRW_behavior": "can be tuned",
            "local_behavior": "can be tuned",
            "non_circularity": "fails",
            "gap": "not allowed unless scale is parent-predicted",
        },
        {
            "candidate": "no_domain_pointwise_projection",
            "definition": "use pointwise theta only, with no averaging domain",
            "status": "insufficient",
            "FLRW_behavior": "works in exact FLRW",
            "local_behavior": "local compression/expansion can still source memory",
            "non_circularity": "not circular but unsafe",
            "gap": "does not solve local dynamical safety",
        },
    ]


def u3_candidate_rows(u_fit: float, n50_fit: float) -> list[dict[str, Any]]:
    candidates = [
        ("fitted_C2_value", u_fit, "current_closure", "borrowed from C2 N50 match"),
        ("spacetime_cell_quarter", 1.0 / 4.0, "near_hit_candidate", "1/(3 spatial + 1 temporal coherence directions)"),
        ("spatial_cell_third", 1.0 / 3.0, "poor_match", "1/(3 spatial directions)"),
        ("six_face_cell", 1.0 / 6.0, "poor_match", "1/(six oriented spatial cell faces)"),
        ("half_spacetime_cell", 1.0 / 8.0, "poor_match", "1/(two orientations times four spacetime directions)"),
    ]
    rows: list[dict[str, Any]] = []
    for name, value, status, interpretation in candidates:
        n50 = value * (math.log(2.0) ** (1.0 / 3.0))
        rows.append(
            {
                "candidate": name,
                "u3": value,
                "N50_implied": n50,
                "delta_u3_vs_fit": value - u_fit,
                "frac_delta_u3_vs_fit": (value - u_fit) / u_fit,
                "delta_N50_vs_fit": n50 - n50_fit,
                "frac_delta_N50_vs_fit": (n50 - n50_fit) / n50_fit,
                "status": status,
                "interpretation": interpretation,
            }
        )
    return rows


def u3_shape_comparison_rows(u_fit: float) -> list[dict[str, Any]]:
    u_quarter = 0.25
    rows: list[dict[str, Any]] = []
    for n_load in SAMPLE_N:
        f_fit = activation(n_load, u_fit)
        f_quarter = activation(n_load, u_quarter)
        rows.append(
            {
                "N": n_load,
                "F_fit_u3": f_fit,
                "F_quarter_u3": f_quarter,
                "delta_F_quarter_minus_fit": f_quarter - f_fit,
                "relative_delta_F": (f_quarter - f_fit) / f_fit if f_fit != 0.0 else "",
            }
        )
    return rows


def origin_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "D_from_volume_coherence_and_u3_from_quarter_cell",
            "status": "best_combined_hypothesis",
            "claim": "D is the maximal coherent volume-flow domain and u3 is close to 1/4 from a 3+1 coherent cell normalization",
            "strength": "both pieces are pre-data structural ideas and avoid arbitrary smoothing",
            "weakness": "neither follows from a parent action yet",
            "next_test": "lock u3=1/4 and rerun fixed-row smoke against the C2 fitted-u3 branch",
        },
        {
            "route": "D_from_turnaround_and_u3_from_fit",
            "status": "local_silence_only",
            "claim": "bound domains are silent but transition scale remains phenomenological",
            "strength": "addresses PPN risk",
            "weakness": "does not improve cosmology derivation",
            "next_test": "derive bound criterion or demote D rule",
        },
        {
            "route": "D_from_horizon_and_u3_from_horizon",
            "status": "insufficient",
            "claim": "use causal horizon as the coherence scale",
            "strength": "covariant-sounding",
            "weakness": "does not naturally give dimensionless u3 or local bound-domain silence",
            "next_test": "reject unless a concrete dimensionless invariant appears",
        },
        {
            "route": "arbitrary_D_and_fitted_u3",
            "status": "rejected",
            "claim": "choose smoothing and scale to preserve the branch",
            "strength": "would be easy",
            "weakness": "not theory",
            "next_test": "not allowed",
        },
    ]


def gate_rows(u_fit: float) -> list[dict[str, Any]]:
    quarter_frac = (0.25 - u_fit) / u_fit
    return [
        {
            "gate": "domain_rule_nonarbitrary",
            "status": "pass_partial",
            "reason": "maximal coherent volume-flow domain is defined by <theta>_D behavior rather than by fitting local residuals",
            "allowed_claim": "D has a plausible physical contract",
        },
        {
            "gate": "domain_rule_parent_derived",
            "status": "fail",
            "reason": "no parent action or constraint yet defines D, its boundary, or averaging measure",
            "allowed_claim": "D is not derived",
        },
        {
            "gate": "u3_quarter_near_lock_identified",
            "status": "pass_partial",
            "reason": f"u3=1/4 is within {quarter_frac:.6g} fractional difference of the fitted C2 u3",
            "allowed_claim": "u3 has a plausible 3+1 cell candidate",
        },
        {
            "gate": "u3_parent_derived",
            "status": "fail",
            "reason": "the 1/4 rule is a structural guess, not a theorem",
            "allowed_claim": "u3 remains underived",
        },
        {
            "gate": "u3_quarter_empirically_checked",
            "status": "open",
            "reason": "the fixed u3=1/4 branch has not yet been scored against the fitted-u3 C2 branch",
            "allowed_claim": "requires smoke test before retention",
        },
        {
            "gate": "local_silence_preserved",
            "status": "pass_conditional",
            "reason": "volume-stable bound domains remain silent under the D rule",
            "allowed_claim": "local silence remains conditional",
        },
        {
            "gate": "support_claim_allowed",
            "status": "fail",
            "reason": "D, u3, amplitude, action ownership, conservation, and perturbations remain incomplete",
            "allowed_claim": "private derivation branch only",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "coherent_domain_and_u3_origin",
            "status": "partial_contract_with_quarter_candidate_not_derivation",
            "best_domain": "maximal coherent volume-flow domain",
            "best_u3": "u3=1/4 spacetime-cell candidate",
            "what_was_earned": "D is less arbitrary and u3 has a near structural candidate",
            "what_failed": "neither D nor u3 is parent-action-derived",
            "next_target": "55-u3-quarter-lock-smoke.md",
        },
        {
            "decision": "testing_priority",
            "status": "run_fixed_quarter_smoke_next",
            "best_domain": "keep P_coh volume-domain rule frozen",
            "best_u3": "replace fitted u3=0.2429466120286312 with u3=0.25",
            "what_was_earned": "a concrete near-derived value can now be tested without fitting",
            "what_failed": "no public claim until fixed-quarter branch survives empirical guardrails",
            "next_target": "score fixed u3=1/4 versus fitted C2 branch",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Coherent domain and u3 origin gate.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    source_register = source_register_rows()
    status_53 = load_json("53_status")
    u_fit = float(status_53["key_metrics"]["u3"])
    n50_fit = float(status_53["key_metrics"]["N50"])

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or POST_CHECKPOINT / "runs" / f"{timestamp}-coherent-domain-and-u3-origin"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    domains = domain_candidate_rows()
    u3_candidates = u3_candidate_rows(u_fit, n50_fit)
    u3_shape = u3_shape_comparison_rows(u_fit)
    routes = origin_route_rows()
    gates = gate_rows(u_fit)
    decisions = decision_rows()

    write_csv(results_dir / "source_checkpoint_register.csv", source_register, list(source_register[0].keys()))
    write_csv(results_dir / "domain_candidate_ledger.csv", domains, list(domains[0].keys()))
    write_csv(results_dir / "u3_candidate_ledger.csv", u3_candidates, list(u3_candidates[0].keys()))
    write_csv(results_dir / "u3_quarter_shape_comparison.csv", u3_shape, list(u3_shape[0].keys()))
    write_csv(results_dir / "origin_route_ledger.csv", routes, list(routes[0].keys()))
    write_csv(results_dir / "gate_results.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "decision.csv", decisions, list(decisions[0].keys()))

    quarter_row = next(row for row in u3_candidates if row["candidate"] == "spacetime_cell_quarter")
    max_abs_delta_f = max(abs(float(row["delta_F_quarter_minus_fit"])) for row in u3_shape)
    status = {
        "status": "complete_coherent_domain_and_u3_origin",
        "readout": "domain_contract_partial_u3_quarter_candidate_not_derived",
        "recommendation": "run_u3_quarter_lock_smoke_next",
        "next_target": "55-u3-quarter-lock-smoke.md",
        "support_claim_allowed": False,
        "public_claim_allowed": False,
        "best_domain_candidate": "maximal coherent volume-flow domain",
        "best_u3_candidate": "u3=1/4 spacetime-cell normalization",
        "key_metrics": {
            "u3_fit": u_fit,
            "u3_quarter": 0.25,
            "frac_delta_u3_quarter_vs_fit": quarter_row["frac_delta_u3_vs_fit"],
            "N50_fit": n50_fit,
            "N50_quarter": quarter_row["N50_implied"],
            "frac_delta_N50_quarter_vs_fit": quarter_row["frac_delta_N50_vs_fit"],
            "max_abs_delta_F_quarter_vs_fit_on_sample": max_abs_delta_f,
            "domain_candidates": len(domains),
            "u3_candidates": len(u3_candidates),
            "failed_gates": sum(1 for row in gates if row["status"] == "fail"),
            "open_gates": sum(1 for row in gates if row["status"] == "open"),
        },
        "outputs": {
            "source_checkpoint_register": str(results_dir / "source_checkpoint_register.csv"),
            "domain_candidate_ledger": str(results_dir / "domain_candidate_ledger.csv"),
            "u3_candidate_ledger": str(results_dir / "u3_candidate_ledger.csv"),
            "u3_quarter_shape_comparison": str(results_dir / "u3_quarter_shape_comparison.csv"),
            "origin_route_ledger": str(results_dir / "origin_route_ledger.csv"),
            "gate_results": str(results_dir / "gate_results.csv"),
            "decision": str(results_dir / "decision.csv"),
            "status_json": str(out_dir / "status.json"),
        },
    }
    (out_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (out_dir / "log.txt").write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    (out_dir / "DONE.txt").write_text(status["readout"] + "\n", encoding="utf-8")
    print(json.dumps(status, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
