from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "sector-label-SD-origin-attempt"
STATUS = "SD_spectral_support_label_constructed_block_kernel_parent_origin_still_missing"
CLAIM_CEILING = "conditional_SD_label_no_block_kernel_selector_local_GR_or_Bmem_promotion"


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
        (ROOT / "276-coherent-domain-projector-from-parent-variables.md", "fixed-D coherent scalar projector"),
        (ROOT / "278-admissible-domain-class-boundary-current-owner.md", "relative class and admissible variation rule"),
        (ROOT / "287-boundary-current-charge-owner-attempt.md", "relative boundary-current support structure"),
        (ROOT / "309-MTS-boundary-projector-contract-attempt.md", "P_MTS component contract"),
        (ROOT / "310-ordinary-MTS-sector-split-attempt.md", "ordinary/MTS split and S_D target"),
        (ROOT / "runs" / "20260601-000133-ordinary-MTS-sector-split-attempt" / "results" / "promotion_gates.csv", "S_D blocker gates"),
        (ROOT / "runs" / "20260601-000133-ordinary-MTS-sector-split-attempt" / "results" / "block_kernel_theorem.csv", "conditional block-kernel lemma"),
        (ROOT / "scripts" / "sector_label_SD_origin_attempt.py", "this S_D origin attempt"),
    ]
    return [{"source": relpath(path), "role": role, "exists": "yes" if path.exists() else "no"} for path, role in sources]


def activity_operator_rows() -> list[dict[str, Any]]:
    return [
        {
            "object": "boundary_Hilbert_space",
            "symbol": "H_B(D)",
            "definition": "parent boundary data space with inner product <.,.>_D",
            "role": "domain for S_D",
            "status": "inner_product_not_parent_derived",
        },
        {
            "object": "MTS_activity_map",
            "symbol": "C_D = P_rel P_IR P_coh",
            "definition": "maps boundary data to coherent IR relative-memory content",
            "role": "annihilates exact/local/noncoherent ordinary data if all components are parent-owned",
            "status": "component_contract",
        },
        {
            "object": "positive_activity_operator",
            "symbol": "A_D = C_D^† C_D",
            "definition": "positive self-adjoint operator measuring MTS boundary activity",
            "role": "turns the sector label into spectral data rather than a hand threshold",
            "status": "conditional_construction",
        },
        {
            "object": "spectral_support_label",
            "symbol": "S_D = 1_{(0,infinity)}(A_D)",
            "definition": "orthogonal projector onto closure of Ran(A_D)",
            "role": "S_D=0 on Ker(A_D), S_D=1 on active MTS support",
            "status": "threshold_free_if_A_D_parent_owned",
        },
        {
            "object": "ordinary_projector",
            "symbol": "P_ord_perp = 1 - S_D",
            "definition": "projector onto zero MTS-activity subspace",
            "role": "kills ordinary local bath contribution to rho_MTS",
            "status": "conditional_on_A_D_and_kernel",
        },
    ]


def spectral_label_proof_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "claim": "A_D is positive if C_D is defined on H_B.",
            "formula": "<B,A_D B> = ||C_D B||^2 >= 0",
            "result": "spectral theorem applies",
            "status": "proved_from_C_D_contract",
        },
        {
            "step": 2,
            "claim": "ordinary data with no coherent IR relative memory lies in Ker(A_D).",
            "formula": "C_D B_ord=0 -> A_D B_ord=0",
            "result": "S_D B_ord=0",
            "status": "conditional_pass",
        },
        {
            "step": 3,
            "claim": "FLRW coherent memory data lies in support(A_D).",
            "formula": "C_D B_FLRW != 0 -> S_D B_FLRW=B_FLRW_support",
            "result": "FLRW channel retained",
            "status": "conditional_pass",
        },
        {
            "step": 4,
            "claim": "S_D is idempotent and self-adjoint.",
            "formula": "S_D^2=S_D and S_D^†=S_D by spectral calculus",
            "result": "valid sector label if A_D is parent-owned",
            "status": "conditional_pass",
        },
        {
            "step": 5,
            "claim": "Block kernel follows if K_boundary commutes with A_D or S_D.",
            "formula": "[K_boundary,A_D]=0 -> [K_boundary,S_D]=0 -> K_cross=0",
            "result": "ordinary/MTS split follows",
            "status": "conditional_pass",
        },
    ]


def block_kernel_origin_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "functional_calculus_kernel",
            "parent_action_form": "S_B=1/2 <B, f(A_D) B> + S_ord[(1-S_D)B] + S_edge",
            "what_it_would_prove": "[K_boundary,A_D]=0 and therefore [K_boundary,S_D]=0",
            "failure": "uses spectral support S_D inside the action unless f/A_D is independently derived",
            "status": "conditional_but_close_to_circular",
        },
        {
            "route": "symmetry_charge_kernel",
            "parent_action_form": "S_D generated by conserved boundary charge; K_boundary invariant under that charge",
            "what_it_would_prove": "sector superselection and K_cross=0",
            "failure": "no parent boundary symmetry/charge currently derives S_D",
            "status": "best_theorem_target",
        },
        {
            "route": "block_diagonal_ansatz",
            "parent_action_form": "K_boundary=diag(K_ord,K_MTS)",
            "what_it_would_prove": "ordinary baths excluded from rho_MTS",
            "failure": "imposed by hand unless tied to symmetry/charge",
            "status": "closure_only",
        },
        {
            "route": "relative_cohomology_only",
            "parent_action_form": "S_D=support(Pi_rel^†Pi_rel)",
            "what_it_would_prove": "exact local relative currents vanish",
            "failure": "does not remove generic ordinary gauge-neutral boundary stress",
            "status": "partial_insufficient",
        },
        {
            "route": "domain_coherence_only",
            "parent_action_form": "S_D=support(P_coh^†P_coh)",
            "what_it_would_prove": "tracefree/noncoherent hair removed",
            "failure": "does not by itself distinguish ordinary coherent matter bath from MTS memory bath",
            "status": "partial_insufficient",
        },
    ]


def branch_test_rows() -> list[dict[str, Any]]:
    cases = [
        {
            "case": "ordinary_warm_lab",
            "C_norm": 0.0,
            "K_commutes": True,
            "edge_domain": False,
            "interpretation": "ordinary bath has no coherent IR relative-memory content",
        },
        {
            "case": "stationary_solar_system",
            "C_norm": 0.0,
            "K_commutes": True,
            "edge_domain": False,
            "interpretation": "stationary local exterior is in the zero activity kernel",
        },
        {
            "case": "ordinary_coherent_matter_counterexample",
            "C_norm": 0.2,
            "K_commutes": False,
            "edge_domain": False,
            "interpretation": "ordinary coherent stress can leak if C_D is not MTS-specific",
        },
        {
            "case": "FLRW_coherent_memory",
            "C_norm": 1.0,
            "K_commutes": True,
            "edge_domain": False,
            "interpretation": "MTS coherent memory branch retained",
        },
        {
            "case": "black_hole_horizon",
            "C_norm": 0.8,
            "K_commutes": False,
            "edge_domain": True,
            "interpretation": "edge sector must not be forced into lab-local theorem",
        },
        {
            "case": "galaxy_cluster_extended_domain",
            "C_norm": 0.4,
            "K_commutes": False,
            "edge_domain": True,
            "interpretation": "empirical/domain branch remains separate",
        },
    ]
    rows: list[dict[str, Any]] = []
    for case in cases:
        C_norm = float(case["C_norm"])
        S_value = 1 if C_norm > 0.0 else 0
        if case["edge_domain"]:
            status = "edge_unresolved"
        elif S_value == 0:
            status = "silent_if_A_D_parent_owned"
        elif case["K_commutes"] and case["case"] == "FLRW_coherent_memory":
            status = "active_if_A_D_parent_owned"
        elif S_value == 1 and not case["K_commutes"]:
            status = "fail_leakage_or_noncommuting_kernel"
        else:
            status = "conditional"
        rows.append(
            {
                **case,
                "S_D_support_value": S_value,
                "status": status,
            }
        )
    return rows


def no_go_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim": "S_D=support(A_D) derives the whole local branch by itself",
            "result": "fail",
            "reason": "A_D itself depends on parent-owned P_rel, P_IR, P_coh and the boundary inner product",
            "repair": "derive C_D and <.,.>_D from the parent action",
        },
        {
            "claim": "spectral support avoids all closure",
            "result": "partial",
            "reason": "it removes arbitrary thresholds, but parent must still derive the activity operator and kernel commutation",
            "repair": "prove A_D is the parent boundary charge/constraint operator",
        },
        {
            "claim": "ordinary coherent stress is automatically in Ker(A_D)",
            "result": "fail",
            "reason": "ordinary coherent stress can be scalar/coherent unless P_rel/P_IR are genuinely MTS-specific",
            "repair": "derive the MTS-specific relative IR map C_D",
        },
        {
            "claim": "K_cross=0 follows from S_D without an action statement",
            "result": "fail",
            "reason": "a generic K_boundary can mix Ker(A_D) and support(A_D)",
            "repair": "derive [K_boundary,A_D]=0 or [K_boundary,S_D]=0",
        },
        {
            "claim": "hard spectral support handles small leakage gently",
            "result": "fail",
            "reason": "any nonzero C_D norm activates the hard support projector",
            "repair": "either prove exact zero for ordinary/local data or use a smooth selector with empirical bounds",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    source_missing = [source for source in source_register_rows() if source["exists"] != "yes"]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not source_missing else "fail",
            "evidence": "all cited S_D/projector sources exist" if not source_missing else ";".join(source["source"] for source in source_missing),
            "claim_effect": "attempt traceable",
        },
        {
            "gate": "activity_operator_constructed",
            "status": "conditional_pass",
            "evidence": "A_D=C_D^dagger C_D with C_D=P_rel P_IR P_coh",
            "claim_effect": "S_D can be tied to boundary activity rather than hand choice",
        },
        {
            "gate": "threshold_free_sector_label_constructed",
            "status": "conditional_pass",
            "evidence": "S_D=1_(0,infinity)(A_D)",
            "claim_effect": "no fitted threshold is needed if A_D is parent-owned",
        },
        {
            "gate": "ordinary_kernel_silence_condition_written",
            "status": "conditional_pass",
            "evidence": "C_D B_ord=0 implies S_D B_ord=0",
            "claim_effect": "ordinary baths can be silenced exactly if C_D annihilates them",
        },
        {
            "gate": "FLRW_retention_condition_written",
            "status": "conditional_pass",
            "evidence": "C_D B_FLRW != 0 implies FLRW support retained",
            "claim_effect": "cosmology can remain active",
        },
        {
            "gate": "activity_operator_parent_derived",
            "status": "fail",
            "evidence": "P_rel/P_IR/P_coh and the boundary inner product are still not all parent-owned",
            "claim_effect": "S_D not promoted",
        },
        {
            "gate": "kernel_commutation_parent_derived",
            "status": "fail",
            "evidence": "no parent action proves [K_boundary,A_D]=0",
            "claim_effect": "block kernel remains conditional",
        },
        {
            "gate": "ordinary_coherent_counterexample_closed",
            "status": "fail",
            "evidence": "ordinary scalar/coherent stress can leak unless C_D is proven MTS-specific",
            "claim_effect": "generic bath problem not fully closed",
        },
        {
            "gate": "hard_support_regularized",
            "status": "fail",
            "evidence": "support projector jumps at arbitrarily small nonzero activity",
            "claim_effect": "exact-zero theorem or smooth bounded runner needed",
        },
        {
            "gate": "selector_parent_derived",
            "status": "fail",
            "evidence": "S_D is only a conditional spectral label",
            "claim_effect": "sigma_D remains theorem target/effective closure",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "S_D, domain, beta, profile, and official PPN manifest remain incomplete",
            "claim_effect": "no local-GR/PPN promotion",
        },
        {
            "gate": "empirical_pivot_recommended",
            "status": "pass",
            "evidence": "the remaining theory obstruction is now narrowly identified",
            "claim_effect": "pivot to holdout testing with local branch labelled conditional",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "priority": 1,
            "target": "empirical_holdout_pivot",
            "task": "return to strict cosmology/galaxy holdout testing while keeping local branch conditional",
            "success_gate": "no local S_D/projector result is used as evidence",
        },
        {
            "priority": 2,
            "target": "parent_activity_operator",
            "task": "derive C_D=P_rel P_IR P_coh and <.,.>_D from the parent boundary action",
            "success_gate": "A_D is not an invented diagnostic but a parent constraint/charge operator",
        },
        {
            "priority": 3,
            "target": "kernel_commutation_theorem",
            "task": "derive [K_boundary,A_D]=0 or [K_boundary,S_D]=0",
            "success_gate": "K_cross=0 follows from action symmetry/superselection",
        },
        {
            "priority": 4,
            "target": "smooth_selector_bound",
            "task": "if exact support is too brittle, map smooth S_D leakage into epsilon_loc/fifth-force runners",
            "success_gate": "small nonzero ordinary leakage is bounded, not silently ignored",
        },
        {
            "priority": 5,
            "target": "edge_domain_manifest",
            "task": "keep horizons and galaxies out of lab-local silence claims",
            "success_gate": "edge domains are routed to separate theory/data branches",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "decision": "S_D can be constructed as a spectral support label, but A_D and the commuting kernel are not parent-derived",
            "recommended_next": "pivot to empirical holdouts or derive A_D/K commutation as a later parent-action target",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    outputs = {
        "source_register": source_register_rows(),
        "activity_operator": activity_operator_rows(),
        "spectral_label_proof": spectral_label_proof_rows(),
        "block_kernel_origin": block_kernel_origin_rows(),
        "branch_tests": branch_test_rows(),
        "no_go_tests": no_go_rows(),
        "promotion_gates": promotion_gate_rows(),
        "next_targets": next_target_rows(),
        "decision": decision_rows(),
    }

    write_csv(results_dir / "source_register.csv", outputs["source_register"], ["source", "role", "exists"])
    write_csv(
        results_dir / "activity_operator.csv",
        outputs["activity_operator"],
        ["object", "symbol", "definition", "role", "status"],
    )
    write_csv(
        results_dir / "spectral_label_proof.csv",
        outputs["spectral_label_proof"],
        ["step", "claim", "formula", "result", "status"],
    )
    write_csv(
        results_dir / "block_kernel_origin.csv",
        outputs["block_kernel_origin"],
        ["route", "parent_action_form", "what_it_would_prove", "failure", "status"],
    )
    write_csv(
        results_dir / "branch_tests.csv",
        outputs["branch_tests"],
        ["case", "C_norm", "K_commutes", "edge_domain", "interpretation", "S_D_support_value", "status"],
    )
    write_csv(results_dir / "no_go_tests.csv", outputs["no_go_tests"], ["claim", "result", "reason", "repair"])
    write_csv(results_dir / "promotion_gates.csv", outputs["promotion_gates"], ["gate", "status", "evidence", "claim_effect"])
    write_csv(results_dir / "next_targets.csv", outputs["next_targets"], ["priority", "target", "task", "success_gate"])
    write_csv(results_dir / "decision.csv", outputs["decision"], ["status", "claim_ceiling", "decision", "recommended_next"])

    payload = {
        "run_slug": RUN_SLUG,
        "timestamp": timestamp,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": relpath(run_dir),
        "outputs": {name: len(rows) for name, rows in outputs.items()},
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "COMPLETE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Attempt to derive S_D as a spectral support label from MTS boundary activity.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
