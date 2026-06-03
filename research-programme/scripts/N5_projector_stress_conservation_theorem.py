from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "N5-projector-stress-conservation-theorem"
STATUS = "N5_conditionally_closed_by_metric_independent_topological_projector_parent_ownership_and_FLRW_stress_bridge_open"
CLAIM_CEILING = "conditional_N5_theorem_only_no_local_GR_PPN_or_Bmem_derivation"


SOURCE_DOCS = [
    ("234-boundary-metric-variation-and-Bianchi-ledger.md", "hidden projector stress and Bianchi obligation"),
    ("235-projector-stress-variation-or-nohair-constraint-algebra.md", "projector stress variation split and safe-branch conditions"),
    ("245-exact-relative-memory-or-projector-stress-bianchi.md", "N4/N5 conservation police gate"),
    ("248-projector-stress-zero-or-retained-theorem.md", "zero/retained fork for T_projector"),
    ("249-projector-boundary-only-condition-or-metric-only-reduction-fail.md", "boundary-only condition and metric-only failure fork"),
    ("251-N5-boundary-projector-parent-owner-or-modified-exterior-branch.md", "topological projector route and Hodge no-go fork"),
    ("252-topological-projector-parent-action-skeleton.md", "metric-independent topological parent-action skeleton"),
    ("255-memory-stress-exchange-normalization-or-kappa-mem-free.md", "local topology vs cosmological stress normalization split"),
    ("347-local-GR-parent-reduction-theorem-attempt.md", "GR reduction theorem and N5 as current blocker"),
]


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
    rows = []
    for filename, role in SOURCE_DOCS:
        path = ROOT / filename
        rows.append(
            {
                "source_path": relpath(path),
                "role": role,
                "exists": path.exists(),
                "issue": "" if path.exists() else "missing",
            }
        )
    script_path = Path(__file__).resolve()
    rows.append(
        {
            "source_path": relpath(script_path),
            "role": "this N5 theorem-ledger builder",
            "exists": script_path.exists(),
            "issue": "" if script_path.exists() else "missing",
        }
    )
    return rows


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_piece": "N5_topological_no_bulk_stress",
            "statement": (
                "If the local projector P_D is a metric-independent relative-chain/topological operator and "
                "the local projector action contains only wedge/chain pairings with no Hodge star, inverse metric, "
                "sqrt(-g) bulk potential, or metric-dependent boundary inner product, then delta_g S_projector|bulk=0."
            ),
            "derivation_status": "conditional_theorem",
            "consequence": "T_projector_munu|bulk=0, so N5 is locally Bianchi-safe in the exterior",
            "failure_if_missing": "Hodge/orthogonal/least-energy projectors generally carry metric variation and bulk stress",
        },
        {
            "theorem_piece": "boundary_only_allowed",
            "statement": (
                "If the remaining projector variation is a well-posed boundary variation on partial E and carries no "
                "trace-free/shear local support, then it does not spoil the bulk Einstein-Hilbert exterior."
            ),
            "derivation_status": "conditional_boundary_theorem",
            "consequence": "metric-only bulk EH can continue with a boundary ledger",
            "failure_if_missing": "boundary shear or unowned boundary metric variation re-enters PPN residuals",
        },
        {
            "theorem_piece": "retained_bulk_stress_route",
            "statement": (
                "If T_projector has bulk support, it must be retained in E_MTS_munu and in the Bianchi identity; "
                "the exterior is then modified, not metric-only GR."
            ),
            "derivation_status": "consistency_theorem",
            "consequence": "Bianchi can remain honest, but local GR promotion fails unless residuals are bounded",
            "failure_if_missing": "dropping the stress creates fake conservation",
        },
        {
            "theorem_piece": "cosmology_stress_split",
            "statement": (
                "The same topological property that kills local bulk projector stress cannot by itself generate the "
                "FLRW memory stress amplitude; cosmology still needs a separate metric stress-response/normalization sector."
            ),
            "derivation_status": "no_free_lunch_result",
            "consequence": "N5 local silence does not derive B_mem=2/27 or kappa_mem",
            "failure_if_missing": "one would falsely use a stress-free topological term to explain H^2 dynamics",
        },
    ]


def fork_rows() -> list[dict[str, Any]]:
    return [
        {
            "fork": "metric_independent_topological_projector",
            "bulk_T_projector": "zero",
            "Bianchi_status": "safe",
            "local_GR_effect": "N5 conditionally cleared",
            "parent_status": "skeleton exists, parent ownership and FLRW compatibility still open",
            "allowed_claim": "conditional route to local projector silence",
        },
        {
            "fork": "boundary_only_projector_stress",
            "bulk_T_projector": "zero",
            "Bianchi_status": "safe_if_boundary_variation_owned",
            "local_GR_effect": "bulk EH can continue if boundary shear/no-hair gates pass",
            "parent_status": "not fully derived",
            "allowed_claim": "conditional boundary route",
        },
        {
            "fork": "retained_bulk_projector_stress",
            "bulk_T_projector": "nonzero",
            "Bianchi_status": "safe_if_retained",
            "local_GR_effect": "modified exterior; no local GR promotion without residual bounds",
            "parent_status": "requires explicit variation and PPN vector",
            "allowed_claim": "consistent modified branch only",
        },
        {
            "fork": "dropped_projector_stress",
            "bulk_T_projector": "ignored",
            "Bianchi_status": "fake_conservation",
            "local_GR_effect": "forbidden",
            "parent_status": "rejected",
            "allowed_claim": "none",
        },
        {
            "fork": "Hodge_or_orthogonal_projector",
            "bulk_T_projector": "generically_nonzero",
            "Bianchi_status": "must_be_retained",
            "local_GR_effect": "metric-only EH fails unless extra cancellation theorem supplied",
            "parent_status": "no-go for simple local-GR route",
            "allowed_claim": "diagnostic/failure branch",
        },
    ]


def unresolved_rows() -> list[dict[str, Any]]:
    return [
        {
            "open_item": "parent_owns_P_D",
            "why_open": "topological projector route requires parent action to select P_D, not insert it by hand",
            "next_action": "derive P_D as a relative cohomology/chain projector from parent variables",
        },
        {
            "open_item": "FLRW_projector_compatibility",
            "why_open": "local topological silence must reduce to the same cosmological memory projector",
            "next_action": "prove local P_D and FLRW memory projection are limits of one operator",
        },
        {
            "open_item": "cosmological_stress_response",
            "why_open": "stress-free topological projector cannot produce H^2 memory amplitude",
            "next_action": "derive separate metric stress-response sector and its normalization",
        },
        {
            "open_item": "boundary_shear_nohair",
            "why_open": "boundary-only stress can still generate gamma/slip if trace-free/shear terms survive",
            "next_action": "prove boundary trace-free/no-hair conditions or compute residuals",
        },
        {
            "open_item": "PPN_residual_vector",
            "why_open": "conditional N5 silence does not yet calculate gamma, beta, preferred-frame, clock, or WEP residuals",
            "next_action": "insert N5 branch into the symbolic PPN residual map",
        },
    ]


def gate_rows(sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources_ok = all(bool(row["exists"]) for row in sources)
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if sources_ok else "fail",
            "evidence": "all cited N5/local-GR sources exist" if sources_ok else "missing source",
        },
        {
            "gate": "topological_no_bulk_stress_theorem_written",
            "status": "pass",
            "evidence": "metric-independent wedge/chain projector has delta_g S_projector|bulk=0",
        },
        {
            "gate": "Hodge_projector_no_go_preserved",
            "status": "pass",
            "evidence": "metric-dependent projector branches must retain stress",
        },
        {
            "gate": "dropped_stress_forbidden",
            "status": "pass",
            "evidence": "fake conservation route remains rejected",
        },
        {
            "gate": "N5_parent_owned",
            "status": "fail",
            "evidence": "parent action skeleton exists but P_D selection is not derived",
        },
        {
            "gate": "FLRW_same_operator_proved",
            "status": "fail",
            "evidence": "local topological P_D has not been proven to reduce to the cosmological memory projector",
        },
        {
            "gate": "Bmem_or_kappa_mem_derived",
            "status": "fail",
            "evidence": "topological local silence does not fix cosmological stress amplitude",
        },
        {
            "gate": "local_GR_or_PPN_promoted",
            "status": "fail",
            "evidence": "N5 is conditional; N0/N2/N3/N6 and PPN vector remain open",
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
                "N5 now has a precise conditional theorem: a metric-independent topological/relative-chain projector "
                "has no bulk metric variation and therefore no bulk projector stress. This conditionally clears the "
                "local projector-stress obstruction, while preserving the no-go for Hodge/metric projectors and the "
                "ban on dropped stress. Promotion is blocked because the parent action has not yet derived P_D, shown "
                "FLRW compatibility, or supplied the separate cosmological stress-response normalization."
            ),
            "next_target": "derive_parent_P_D_and_FLRW_projection_compatibility_or_keep_N5_as_conditional_closure",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    result_dir = run_dir / "results"
    result_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    theorem = theorem_rows()
    forks = fork_rows()
    unresolved = unresolved_rows()
    gates = gate_rows(sources)
    decisions = decision_rows()

    outputs = {
        "source_register.csv": (sources, ["source_path", "role", "exists", "issue"]),
        "N5_theorem_pieces.csv": (
            theorem,
            ["theorem_piece", "statement", "derivation_status", "consequence", "failure_if_missing"],
        ),
        "projector_stress_fork_table.csv": (
            forks,
            ["fork", "bulk_T_projector", "Bianchi_status", "local_GR_effect", "parent_status", "allowed_claim"],
        ),
        "unresolved_bridge_ledger.csv": (unresolved, ["open_item", "why_open", "next_action"]),
        "gate_results.csv": (gates, ["gate", "status", "evidence"]),
        "decision.csv": (decisions, ["decision", "claim_ceiling", "meaning", "next_target"]),
    }
    for filename, (rows, fieldnames) in outputs.items():
        write_csv(result_dir / filename, rows, fieldnames)

    payload = {
        "status": decisions[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "results_dir": str(result_dir),
        "generated": list(outputs),
        "source_paths_missing": sum(1 for row in sources if not row["exists"]),
        "N5_conditionally_closed": True,
        "N5_parent_owned": False,
        "local_GR_promoted": False,
        "Bmem_derived": False,
        "next_target": decisions[0]["next_target"],
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(payload["status"] + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build N5 projector-stress conservation theorem ledger.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
