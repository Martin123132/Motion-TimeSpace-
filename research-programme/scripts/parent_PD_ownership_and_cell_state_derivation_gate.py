from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "parent-PD-ownership-and-cell-state-derivation-gate"
STATUS = "parent_PD_owned_as_topological_quotient_not_as_rank_projector_dim27_rank2_kappa_remain_closure_debts"
CLAIM_CEILING = "quotient_PD_parent_ownership_only_no_Bmem_local_GR_or_rank_amplitude_promotion"
NEXT_TARGET = "351-local-GR-spin2-rank2-bridge-or-boundary-PPN-gate.md"


SOURCE_DOCS = [
    (
        "340-full-cell-equivalence-gauge-redundancy-gate.md",
        "cell labels as possible gauge redundancy and active-marker hazard",
    ),
    (
        "341-indistinguishable-cell-quotient-parent-action-gate.md",
        "quotient route for indistinguishable cell labels",
    ),
    (
        "342-finite-fibre-basis-relabeling-gate.md",
        "finite-fibre basis relabeling and rank-readout failure/pass split",
    ),
    (
        "343-dim27-rank2-origin-closure-decision-gate.md",
        "dim-27/rank-2 demotion to explicit closure",
    ),
    (
        "348-N5-projector-stress-conservation-theorem.md",
        "local N5 theorem for metric-independent topological projector stress",
    ),
    (
        "349-parent-PD-FLRW-projection-compatibility-gate.md",
        "same P_D local/FLRW compatibility contract",
    ),
]


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for filename, role in SOURCE_DOCS:
        path = ROOT / filename
        rows.append(
            {
                "source_path": relpath(path),
                "role": role,
                "exists": "yes" if path.exists() else "no",
                "issue": "" if path.exists() else "missing",
            }
        )
    script_path = Path(__file__).resolve()
    rows.append(
        {
            "source_path": relpath(script_path),
            "role": "this parent-ownership derivation-gate builder",
            "exists": "yes" if script_path.exists() else "no",
            "issue": "" if script_path.exists() else "missing",
        }
    )
    return rows


def pd_ownership_rows() -> list[dict[str, Any]]:
    return [
        {
            "object": "P_D_as_relative_quotient_map",
            "candidate_derivation": (
                "Parent variables define a relative chain/cochain complex for domain D; gauge-equivalent "
                "bulk representatives differ by exact/boundary pieces; the canonical map to the relative "
                "cohomology/quotient class is metric-independent."
            ),
            "status": "conditional_parent_owned",
            "what_is_owned": "the quotient/projection-to-class, not a chosen basis subspace",
            "what_is_not_owned": "rank-2 active fibre projector and numerical amplitude",
            "GR_relevance": "enough for local topological no-bulk-stress if the action depends only on quotient data",
        },
        {
            "object": "P_D_as_idempotent_subspace_projector",
            "candidate_derivation": (
                "Choose a splitting from quotient classes back into representatives or into a rank-selected finite fibre."
            ),
            "status": "fail_as_parent_derivation",
            "what_is_owned": "none without extra splitting/gauge-fixing data",
            "what_is_not_owned": "canonical rank, basis, active plane, and marker exclusion",
            "GR_relevance": "dangerous if treated as physical bulk projector; can reintroduce stress/counterterms",
        },
        {
            "object": "P_D_as_Hodge_or_least_energy_projector",
            "candidate_derivation": (
                "Use metric/Hodge/orthogonal projection to pick canonical representatives."
            ),
            "status": "rejected_for_simple_GR_route",
            "what_is_owned": "a mathematically sharp representative only after metric is used",
            "what_is_not_owned": "metric-independent stress silence",
            "GR_relevance": "metric variation generically produces projector stress, so N5 local silence is lost",
        },
        {
            "object": "P_D_as_source_relational_readout",
            "candidate_derivation": (
                "Keep the bulk parent action quotient/basis-free while letting boundary/source data define a relational readout."
            ),
            "status": "conditional_readout_route",
            "what_is_owned": "readout covariance if the source frame transforms with the fibre",
            "what_is_not_owned": "proof that the source frame is not a marker field with new EFT coefficients",
            "GR_relevance": "may allow external observables without adding local bulk stress",
        },
    ]


def cell_state_rows() -> list[dict[str, Any]]:
    return [
        {
            "target": "dim(V_cell)=27",
            "candidate_route": "three ternary M/T/S-style finite-fibre factors, 3 x 3 x 3",
            "status": "conditional_template_only",
            "why_not_derived": "the parent action has not forced exactly three factors or ternary state cardinality",
            "what_would_close_it": "derive the finite fibre from parent boundary/cohomology degrees of freedom",
        },
        {
            "target": "dim(V_cell)=27",
            "candidate_route": "relative cohomology Betti number equals 27",
            "status": "not_supported",
            "why_not_derived": "no domain-topology theorem currently fixes the relevant Betti/rank count to 27",
            "what_would_close_it": "prove the physical domain complex has a protected 27-dimensional quotient",
        },
        {
            "target": "rank(P_active)=2",
            "candidate_route": "two local GR massless spin-2 / transverse tensor degrees of freedom",
            "status": "promising_bridge_not_amplitude_derivation",
            "why_not_derived": "rank-2 spin/PPN content is not yet shown to be the same FLRW memory readout plane",
            "what_would_close_it": "derive a Ward map from local GR spin-2 polarizations to P_active trace readout",
        },
        {
            "target": "rank(P_active)=2",
            "candidate_route": "source/readout plane inside a 27-dimensional finite fibre",
            "status": "conditional_readout_template",
            "why_not_derived": "active plane selection is not canonical; many rank-2 planes exist",
            "what_would_close_it": "prove the boundary/source relation selects the plane without marker counterterms",
        },
        {
            "target": "kappa_mem=1",
            "candidate_route": "Bianchi/Ward stress-exchange normalization",
            "status": "open",
            "why_not_derived": "quotient topology fixes class selection, not physical H^2 stress units",
            "what_would_close_it": "derive the metric stress-response normalization from the same conserved parent ledger",
        },
        {
            "target": "B_mem=2/27",
            "candidate_route": "kappa_mem Tr(P_active)/dim(V_cell)",
            "status": "closure_locked",
            "why_not_derived": "dim=27, rank=2, and kappa_mem=1 are not simultaneously parent-derived",
            "what_would_close_it": "close all three target derivations in one parent action, not as separate assumptions",
        },
    ]


def gr_bridge_rows() -> list[dict[str, Any]]:
    return [
        {
            "GR_requirement": "no projector bulk stress",
            "effect_of_350": "improved",
            "reason": "P_D can be parent-owned as a metric-independent quotient map if parent variables are relative-chain data",
            "still_missing": "prove the actual parent action uses only quotient data in the compact exterior",
        },
        {
            "GR_requirement": "metric-only Einstein-Hilbert exterior",
            "effect_of_350": "not_closed",
            "reason": "quotient P_D silence helps N5 but does not close N0/N2/N3/N6",
            "still_missing": "show no remaining MTS bulk support and no unowned boundary shear",
        },
        {
            "GR_requirement": "massless spin-2 local limit",
            "effect_of_350": "new_derivation_target",
            "reason": "a GR-compatible local limit naturally supplies two physical tensor polarizations",
            "still_missing": "prove these two modes are the rank-2 memory readout and not an analogy",
        },
        {
            "GR_requirement": "PPN residual vector",
            "effect_of_350": "not_calculated",
            "reason": "P_D quotient ownership does not compute gamma, beta, preferred-frame, clock, or WEP residuals",
            "still_missing": "insert quotient P_D branch into the PPN/no-hair ledger",
        },
        {
            "GR_requirement": "conserved stress ledger",
            "effect_of_350": "partially_sharpened",
            "reason": "topological quotient can be stress-free locally, but FLRW memory needs metric stress response",
            "still_missing": "derive one Bianchi-safe exchange law for both sectors",
        },
    ]


def theorem_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim": "parent can own P_D as a topological quotient/projection-to-class",
            "status": "conditional_theorem",
            "allowed_wording": "parent-owned quotient P_D route",
            "forbidden_wording": "parent-derived rank projector or amplitude",
        },
        {
            "claim": "local N5 projector silence has a parent route",
            "status": "conditional_theorem",
            "allowed_wording": "if the compact exterior action depends only on quotient data",
            "forbidden_wording": "local GR is derived",
        },
        {
            "claim": "dim(V_cell)=27 is derived",
            "status": "fail",
            "allowed_wording": "three-ternary finite-fibre template",
            "forbidden_wording": "the parent action forces 27",
        },
        {
            "claim": "rank(P_active)=2 is derived",
            "status": "fail_with_promising_GR_bridge",
            "allowed_wording": "rank-2 may be tied to local GR spin-2 degrees in a future theorem",
            "forbidden_wording": "the active rank is already parent-derived",
        },
        {
            "claim": "B_mem=2/27 is parent-derived",
            "status": "fail",
            "allowed_wording": "locked closure/theorem target",
            "forbidden_wording": "derived amplitude",
        },
    ]


def gate_result_rows(sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources_ok = all(row["exists"] == "yes" for row in sources)
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if sources_ok else "fail",
            "evidence": "all cited source checkpoints and this script exist" if sources_ok else "missing cited source",
        },
        {
            "gate": "parent_owns_P_D_as_quotient",
            "status": "conditional_pass",
            "evidence": "relative-chain quotient map is canonical and metric-independent if parent variables define the complex",
        },
        {
            "gate": "parent_owns_P_D_as_rank_idempotent",
            "status": "fail",
            "evidence": "idempotent representative/projector requires noncanonical splitting or extra readout data",
        },
        {
            "gate": "local_N5_route_improved",
            "status": "conditional_pass",
            "evidence": "quotient P_D can carry no bulk metric variation in local exterior",
        },
        {
            "gate": "dim27_parent_derived",
            "status": "fail",
            "evidence": "three-ternary template exists but parent action does not force it",
        },
        {
            "gate": "rank2_parent_derived",
            "status": "fail",
            "evidence": "GR spin-2 bridge is promising but not proven to be FLRW active readout",
        },
        {
            "gate": "kappa_mem_parent_derived",
            "status": "fail",
            "evidence": "topological quotient does not set physical stress units",
        },
        {
            "gate": "Bmem_2over27_parent_derived",
            "status": "fail",
            "evidence": "needs dim=27, rank=2, and kappa_mem=1 together",
        },
        {
            "gate": "local_GR_or_PPN_promoted",
            "status": "fail",
            "evidence": "P_D quotient ownership closes only one conditional local blocker",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "The parent can plausibly own P_D as a canonical metric-independent quotient map on relative "
                "chain/cohomology data. That is enough to sharpen the local N5/no-bulk-stress route, because the "
                "action can depend on quotient classes without metric variation. But this is not the same as owning "
                "a rank-2 idempotent finite-fibre projector. The 27-dimensional cell space, rank-2 active readout, "
                "and kappa_mem=1 stress normalization remain closure debts. The strongest new bridge is that local "
                "GR's two massless spin-2 polarizations may be the right future source of rank=2, but that bridge is "
                "not yet proved."
            ),
            "next_target": NEXT_TARGET,
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    result_dir = run_dir / "results"
    result_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    outputs = {
        "source_register.csv": (
            sources,
            ["source_path", "role", "exists", "issue"],
        ),
        "PD_ownership_derivation.csv": (
            pd_ownership_rows(),
            ["object", "candidate_derivation", "status", "what_is_owned", "what_is_not_owned", "GR_relevance"],
        ),
        "cell_state_derivation_candidates.csv": (
            cell_state_rows(),
            ["target", "candidate_route", "status", "why_not_derived", "what_would_close_it"],
        ),
        "GR_bridge_implications.csv": (
            gr_bridge_rows(),
            ["GR_requirement", "effect_of_350", "reason", "still_missing"],
        ),
        "theorem_status_ledger.csv": (
            theorem_status_rows(),
            ["claim", "status", "allowed_wording", "forbidden_wording"],
        ),
        "gate_results.csv": (
            gate_result_rows(sources),
            ["gate", "status", "evidence"],
        ),
        "decision.csv": (
            decision_rows(),
            ["decision", "claim_ceiling", "meaning", "next_target"],
        ),
    }

    for filename, (rows, fieldnames) in outputs.items():
        write_csv(result_dir / filename, rows, fieldnames)

    payload = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "results_dir": str(result_dir),
        "generated": list(outputs),
        "missing_sources": sum(row["exists"] != "yes" for row in sources),
        "parent_owns_P_D_as_quotient": "conditional_pass",
        "parent_owns_P_D_as_rank_idempotent": False,
        "local_N5_route_improved": "conditional_pass",
        "dim27_parent_derived": False,
        "rank2_parent_derived": False,
        "kappa_mem_parent_derived": False,
        "Bmem_2over27_parent_derived": False,
        "local_GR_or_PPN_promoted": False,
        "next_target": NEXT_TARGET,
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build checkpoint 350: parent P_D ownership and cell-state derivation gate.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
