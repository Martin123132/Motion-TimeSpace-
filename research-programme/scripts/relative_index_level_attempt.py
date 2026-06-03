from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "relative-index-level-attempt"
STATUS = "relative_index_level_derives_conditional_k9_not_full_Bmem"
CLAIM_CEILING = "conditional_index_theorem_only_no_Bmem_or_local_GR_promotion"


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
        (ROOT / "276-coherent-domain-projector-from-parent-variables.md", "fixed-domain coherent projector and SO(3) trace projection"),
        (ROOT / "286-memory-stress-normalization-scale-no-go.md", "amplitude scale no-go and exact B_mem contract"),
        (ROOT / "287-boundary-current-charge-owner-attempt.md", "boundary-current owner and k=9 integer obstruction"),
        (ROOT / "288-k9-Ward-index-level-attempt.md", "rank-nine theorem target before explicit complex"),
        (ROOT / "291-CPL-prior-sensitivity-readout.md", "latest empirical ceiling before theory pivot"),
    ]
    return [{"source": relpath(path), "role": role, "exists": "yes" if path.exists() else "no"} for path, role in sources]


def complex_construction_rows() -> list[dict[str, Any]]:
    return [
        {
            "object": "coherent_domain",
            "definition": "oriented compact spatial 3-domain D with boundary partial D",
            "derived_or_assumed": "assumed_theorem_target",
            "role": "domain on which relative boundary current and load endomorphism live",
        },
        {
            "object": "coefficient_bundle",
            "definition": "E_D = End(TSigma_D), rank(E_D)=3*3=9",
            "derived_or_assumed": "conditional_from_Q_branch",
            "role": "nine spatial load/coframe endomorphism channels",
        },
        {
            "object": "relative_complex",
            "definition": "0 -> Omega^0(D,E_D) -> Omega^1(D,E_D) -> Omega^2(D,E_D) -> Omega^3(D,E_D) -> 0 with relative boundary conditions",
            "derived_or_assumed": "constructed_mathematically_not_parent_derived",
            "role": "elliptic de Rham complex whose index can count relative charge channels",
        },
        {
            "object": "flat_connection_condition",
            "definition": "d_A^2=0 on E_D; torsion/curvature corrections do not change the topological index under admissible homotopy",
            "derived_or_assumed": "closure_condition",
            "role": "needed so the complex is actually a complex and has stable index",
        },
        {
            "object": "relative_index_formula",
            "definition": "index(D,E_D,rel)=rank(E_D)*chi(D,partial D)",
            "derived_or_assumed": "standard_index_step_conditional",
            "role": "turns nine load channels plus domain topology into a signed integer index",
        },
    ]


def domain_index_rows() -> list[dict[str, Any]]:
    candidates = [
        {
            "domain": "contractible_3_cell",
            "chi_domain": 1,
            "chi_boundary": 2,
            "boundary_type": "S2",
            "interpretation": "minimal coherent cell",
        },
        {
            "domain": "solid_torus",
            "chi_domain": 0,
            "chi_boundary": 0,
            "boundary_type": "T2",
            "interpretation": "handled/vortex-like coherent domain",
        },
        {
            "domain": "spherical_shell",
            "chi_domain": 2,
            "chi_boundary": 4,
            "boundary_type": "S2_union_S2",
            "interpretation": "two-boundary shell",
        },
        {
            "domain": "closed_3_domain",
            "chi_domain": 0,
            "chi_boundary": 0,
            "boundary_type": "none",
            "interpretation": "no relative boundary current",
        },
    ]
    rows: list[dict[str, Any]] = []
    rank_end_bundle = 9
    for candidate in candidates:
        chi_relative = candidate["chi_domain"] - candidate["chi_boundary"]
        signed_index = rank_end_bundle * chi_relative
        abs_level = abs(signed_index)
        if candidate["domain"] == "contractible_3_cell":
            status = "conditional_k9_pass"
            claim_effect = "gives signed index -9, so level magnitude 9 if the coherent domain is a single 3-cell"
        elif candidate["domain"] == "closed_3_domain":
            status = "not_relative_source"
            claim_effect = "no boundary source route"
        elif abs_level == 0:
            status = "fails_k9"
            claim_effect = "relative index vanishes"
        else:
            status = "wrong_level"
            claim_effect = f"relative index magnitude {abs_level}, not 9"
        rows.append(
            {
                "domain": candidate["domain"],
                "boundary_type": candidate["boundary_type"],
                "chi_domain": candidate["chi_domain"],
                "chi_boundary": candidate["chi_boundary"],
                "chi_relative": chi_relative,
                "rank_End_TSigma": rank_end_bundle,
                "signed_index": signed_index,
                "abs_level": abs_level,
                "status": status,
                "claim_effect": claim_effect,
                "interpretation": candidate["interpretation"],
            }
        )
    return rows


def period_and_trace_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": "relative_index_to_channels",
            "formula": "|index|=9 for a contractible 3-cell",
            "status": "conditional_pass",
            "meaning": "there are nine relative load channels in the cell complex",
            "blocker": "channel count is not yet a normalized period denominator",
        },
        {
            "step": "integral_period_lattice",
            "formula": "H^3(D,partial D;Z_E) ~= Z^9 for the cell case",
            "status": "mathematical_support",
            "meaning": "integral periods can exist on nine channels",
            "blocker": "does not force scalar unit Q_*=1/9 by itself",
        },
        {
            "step": "normalized_trace_over_channels",
            "formula": "q_scalar=(1/9) Tr_End q",
            "status": "closure_or_Ward_target",
            "meaning": "would turn nine channels into a denominator 9",
            "blocker": "parent action must choose normalized trace rather than unnormalized trace",
        },
        {
            "step": "SO3_isotropic_projection",
            "formula": "Pi_iso(Q)=(Tr Q/3) I",
            "status": "conditional_pass",
            "meaning": "unique rotationally invariant spatial scalar projection supplies the one-third trace partition",
            "blocker": "only applies after the coherent isotropic FLRW projection is selected",
        },
        {
            "step": "target_amplitude_chain",
            "formula": "B_mem = (n_early-n_today)/(3*9)",
            "status": "conditional_chain",
            "meaning": "if n_early=3 and n_today=1, then B_mem=2/27",
            "blocker": "endpoint occupancies and arrow remain unproved",
        },
    ]


def endpoint_blocker_rows() -> list[dict[str, Any]]:
    return [
        {
            "blocker": "domain_topology_selection",
            "needed": "coherent FLRW memory domains must be single contractible 3-cells",
            "current_status": "not_derived",
            "why_it_matters": "other topologies give index 0 or 18 instead of 9",
        },
        {
            "blocker": "period_normalization",
            "needed": "Ward action must use normalized End trace or equivalent scalar averaging",
            "current_status": "not_parent_derived",
            "why_it_matters": "index 9 counts channels but does not itself create Q_*=1/9",
        },
        {
            "blocker": "endpoint_occupancies",
            "needed": "the action must select n_early=3 and n_today=1",
            "current_status": "not_derived",
            "why_it_matters": "without Delta n=2 the 2/27 amplitude is not fixed",
        },
        {
            "blocker": "endpoint_arrow",
            "needed": "dynamics must prefer 3 -> 1 rather than 1 -> 3 or arbitrary occupancy",
            "current_status": "not_derived",
            "why_it_matters": "cosmic time direction must be owned by the parent theory",
        },
        {
            "blocker": "local_silence",
            "needed": "same relative-current theorem must set local measured source periods to zero or tightly bounded",
            "current_status": "not_derived",
            "why_it_matters": "otherwise the branch can fit cosmology but fail local GR/PPN",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    source_missing = [source for source in source_register_rows() if source["exists"] != "yes"]
    contractible_row = next(row for row in domain_index_rows() if row["domain"] == "contractible_3_cell")
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not source_missing else "fail",
            "evidence": "all cited post-checkpoint sources exist" if not source_missing else ";".join(source["source"] for source in source_missing),
            "claim_effect": "audit traceable",
        },
        {
            "gate": "relative_complex_constructed",
            "status": "conditional_pass",
            "evidence": "relative de Rham complex on E_D=End(TSigma_D) is mathematically defined",
            "claim_effect": "k=9 target upgraded from naked rank count to conditional index construction",
        },
        {
            "gate": "contractible_cell_gives_level_9",
            "status": "conditional_pass",
            "evidence": f"signed_index={contractible_row['signed_index']}; abs_level={contractible_row['abs_level']}",
            "claim_effect": "k=9 can be derived if the domain topology theorem is supplied",
        },
        {
            "gate": "domain_topology_derived",
            "status": "fail",
            "evidence": "single contractible 3-cell is assumed, not selected by parent action",
            "claim_effect": "index result is conditional",
        },
        {
            "gate": "period_denominator_derived",
            "status": "fail",
            "evidence": "index counts channels; normalized scalar period Q_*=1/9 still needs Ward trace rule",
            "claim_effect": "B_mem not promoted",
        },
        {
            "gate": "trace_partition_from_SO3",
            "status": "conditional_pass",
            "evidence": "Pi_iso(Q)=(Tr Q/3)I is the unique SO(3)-equivariant isotropic projection",
            "claim_effect": "one-third partition has a clean conditional derivation",
        },
        {
            "gate": "endpoint_law_derived",
            "status": "fail",
            "evidence": "n_early=3, n_today=1, and arrow 3->1 are still theorem targets",
            "claim_effect": "2/27 amplitude remains locked closure",
        },
        {
            "gate": "local_silence_derived",
            "status": "fail",
            "evidence": "relative index does not force local source periods to vanish",
            "claim_effect": "no local-GR/PPN promotion",
        },
        {
            "gate": "B_mem_derived",
            "status": "fail",
            "evidence": "conditional k=9 plus conditional 1/3 is still missing domain, period, endpoint, and local-silence theorems",
            "claim_effect": "empirical closure retained",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "A genuine relative-index route exists: the de Rham complex with relative boundary conditions "
                "on E_D=End(TSigma_D) has index rank(E_D)*chi(D,partial D). For a single contractible 3-cell, "
                "this gives signed index -9 and level magnitude 9. This is better than pure component counting, "
                "but it is conditional on a domain-topology theorem and still does not derive period normalization, "
                "endpoint occupancies, endpoint arrow, or local silence."
            ),
            "next_target": "derive_domain_topology_selection_or_endpoint_occupancy_law",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "complex_construction.csv": (
            complex_construction_rows(),
            ["object", "definition", "derived_or_assumed", "role"],
        ),
        "domain_index_sensitivity.csv": (
            domain_index_rows(),
            [
                "domain",
                "boundary_type",
                "chi_domain",
                "chi_boundary",
                "chi_relative",
                "rank_End_TSigma",
                "signed_index",
                "abs_level",
                "status",
                "claim_effect",
                "interpretation",
            ],
        ),
        "period_and_trace_chain.csv": (
            period_and_trace_rows(),
            ["step", "formula", "status", "meaning", "blocker"],
        ),
        "endpoint_blockers.csv": (
            endpoint_blocker_rows(),
            ["blocker", "needed", "current_status", "why_it_matters"],
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
        "conditional_k9_index_route": True,
        "B_mem_derived_now": False,
        "local_GR_promoted_now": False,
        "next_target": "derive_domain_topology_selection_or_endpoint_occupancy_law",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Relative index level derivation attempt for k=9.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
