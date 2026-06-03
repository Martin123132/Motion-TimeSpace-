from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "ordinary-MTS-sector-split-attempt"
STATUS = "ordinary_MTS_sector_split_conditional_superselection_lemma_cross_kernel_not_parent_derived"
CLAIM_CEILING = "conditional_sector_split_no_Pord_parent_derivation_no_local_GR_or_selector_promotion"


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
        (ROOT / "207-domain-projector-action-and-Bianchi-identity.md", "projector must be variational and Bianchi-accounted"),
        (ROOT / "276-coherent-domain-projector-from-parent-variables.md", "fixed-D coherent projection evidence"),
        (ROOT / "278-admissible-domain-class-boundary-current-owner.md", "relative-class preserving variations"),
        (ROOT / "287-boundary-current-charge-owner-attempt.md", "relative boundary current and local/FLRW split"),
        (ROOT / "302-epsilon-loc-parent-coefficient-map-attempt.md", "universal metric coupling condition"),
        (ROOT / "308-selector-parent-theorem-attempt.md", "generic bath problem and P_MTS target"),
        (ROOT / "309-MTS-boundary-projector-contract-attempt.md", "P_MTS component contract and next target"),
        (ROOT / "runs" / "20260601-000132-MTS-boundary-projector-contract-attempt" / "results" / "promotion_gates.csv", "P_MTS gate evidence"),
        (ROOT / "runs" / "20260601-000132-MTS-boundary-projector-contract-attempt" / "results" / "next_targets.csv", "ordinary/MTS sector-split target"),
        (ROOT / "scripts" / "ordinary_MTS_sector_split_attempt.py", "this sector-split runner"),
    ]
    return [{"source": relpath(path), "role": role, "exists": "yes" if path.exists() else "no"} for path, role in sources]


def sector_decomposition_rows() -> list[dict[str, Any]]:
    return [
        {
            "object": "boundary_state_space",
            "symbol": "H_B(D)",
            "definition": "boundary data space on domain D",
            "required_split": "H_B = H_ord ⊕ H_MTS ⊕ H_edge",
            "role": "separates ordinary baths, MTS memory boundary channel, and unresolved edge domains",
            "status": "contract",
        },
        {
            "object": "ordinary_boundary_sector",
            "symbol": "H_ord",
            "definition": "ordinary EM/matter/environmental boundary operators and their gauge-invariant stress response",
            "required_split": "sector label s=0",
            "role": "allowed to couple through the universal metric, not through the MTS open selector",
            "status": "must_be_projected_out_of_rho_MTS",
        },
        {
            "object": "MTS_boundary_sector",
            "symbol": "H_MTS",
            "definition": "coherent scalar, IR/gapless, nontrivial relative boundary-current memory channel",
            "required_split": "sector label s=1",
            "role": "the only sector that may contribute to rho_MTS and sigma_D",
            "status": "conditional_theorem_target",
        },
        {
            "object": "edge_boundary_sector",
            "symbol": "H_edge",
            "definition": "horizon, galaxy/cluster, or time-dependent mixed domains whose sector label is not settled",
            "required_split": "sector label unresolved",
            "role": "prevents blanket local-GR claims",
            "status": "defer_to_domain_branch",
        },
        {
            "object": "sector_label_operator",
            "symbol": "S_D",
            "definition": "self-adjoint projector/charge with S=0 on H_ord and S=1 on H_MTS",
            "required_split": "P_ord=1-S_D, P_MTS=S_D on the clean two-sector subspace",
            "role": "would derive P_ord_perp if parent-owned",
            "status": "not_parent_derived",
        },
    ]


def block_kernel_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "statement": "Assume H_B decomposes into self-adjoint sector eigenspaces of S_D.",
            "formula": "S_D u=0 for u in H_ord; S_D v=v for v in H_MTS",
            "result": "ordinary and MTS modes have distinct sector labels",
            "status": "premise",
        },
        {
            "step": 2,
            "statement": "Assume the boundary kinetic kernel is sector-symmetric.",
            "formula": "[K_boundary,S_D]=0",
            "result": "K_boundary preserves the sector eigenspaces",
            "status": "premise",
        },
        {
            "step": 3,
            "statement": "For u in H_ord and v in H_MTS, the cross matrix element vanishes.",
            "formula": "<u,Kv>=<u,S Kv>=<S u,Kv>=0",
            "result": "<B_ord,K_boundary B_MTS>=0",
            "status": "conditional_proof",
        },
        {
            "step": 4,
            "statement": "The boundary kernel is block diagonal on the clean sectors.",
            "formula": "K_boundary = [[K_ord,0],[0,K_MTS]] on H_ord ⊕ H_MTS",
            "result": "ordinary baths cannot contribute to rho_MTS",
            "status": "conditional_proof",
        },
        {
            "step": 5,
            "statement": "Ordinary matter may still couple universally through g_eff.",
            "formula": "S_m=S_m[psi_m,g_eff], not S_m[psi_m,P_MTS B_D]",
            "result": "ordinary GR/metric coupling is separated from MTS open-sector activation",
            "status": "required_separation_contract",
        },
    ]


def mixing_risk_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "case": "exact_sector_symmetry",
            "sector_label_owned": True,
            "kernel_commutes_with_label": True,
            "ordinary_stress_gauge_neutral": False,
            "universal_metric_only": True,
            "edge_domain": False,
            "interpretation": "clean superselection proof",
        },
        {
            "case": "no_sector_label",
            "sector_label_owned": False,
            "kernel_commutes_with_label": False,
            "ordinary_stress_gauge_neutral": True,
            "universal_metric_only": False,
            "edge_domain": False,
            "interpretation": "nothing forbids ordinary/MTS mixing",
        },
        {
            "case": "EM_stress_counterexample",
            "sector_label_owned": False,
            "kernel_commutes_with_label": False,
            "ordinary_stress_gauge_neutral": True,
            "universal_metric_only": False,
            "edge_domain": False,
            "interpretation": "gauge invariance alone is insufficient because EM stress is gauge-neutral",
        },
        {
            "case": "universal_metric_separated",
            "sector_label_owned": True,
            "kernel_commutes_with_label": True,
            "ordinary_stress_gauge_neutral": True,
            "universal_metric_only": True,
            "edge_domain": False,
            "interpretation": "ordinary stress couples to metric but not to MTS boundary selector",
        },
        {
            "case": "black_hole_horizon_edge",
            "sector_label_owned": False,
            "kernel_commutes_with_label": False,
            "ordinary_stress_gauge_neutral": True,
            "universal_metric_only": False,
            "edge_domain": True,
            "interpretation": "sector split cannot be assumed for horizon domains",
        },
        {
            "case": "FLRW_memory_sector",
            "sector_label_owned": True,
            "kernel_commutes_with_label": True,
            "ordinary_stress_gauge_neutral": False,
            "universal_metric_only": True,
            "edge_domain": False,
            "interpretation": "coherent MTS boundary sector remains retained",
        },
    ]
    scored: list[dict[str, Any]] = []
    for row in rows:
        clean_split = row["sector_label_owned"] and row["kernel_commutes_with_label"] and row["universal_metric_only"] and not row["edge_domain"]
        if row["edge_domain"]:
            status = "edge_unresolved"
            cross_kernel = "unknown"
        elif clean_split:
            status = "conditional_pass"
            cross_kernel = "zero_by_sector_lemma"
        elif row["ordinary_stress_gauge_neutral"]:
            status = "fail_counterexample"
            cross_kernel = "allowed_without_extra_sector_label"
        else:
            status = "fail_unconstrained"
            cross_kernel = "allowed"
        scored.append({**row, "cross_kernel_status": cross_kernel, "status": status})
    return scored


def no_go_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim": "gauge invariance alone forbids ordinary/MTS mixing",
            "result": "fail",
            "reason": "ordinary EM/matter stress can be gauge-invariant and neutral, so a cross boundary kernel is not forbidden by gauge symmetry alone",
            "repair": "derive a separate MTS sector label S_D or block boundary kernel",
        },
        {
            "claim": "relative cohomology alone removes all ordinary baths",
            "result": "partial",
            "reason": "relative exactness kills memory-class activation but ordinary gauge-neutral stress can still exist",
            "repair": "combine P_rel with ordinary/MTS sector superselection",
        },
        {
            "claim": "universal metric coupling is the same as MTS boundary mixing",
            "result": "fail",
            "reason": "ordinary matter must still gravitate through g_eff; the banned coupling is direct activation of rho_MTS/sigma_D",
            "repair": "write the parent action with S_m[g_eff] and a separate MTS boundary sector",
        },
        {
            "claim": "block diagonal kernel can be imposed after variation",
            "result": "fail",
            "reason": "that would be an external projector and could hide Bianchi/projector stress",
            "repair": "derive the block kernel in S_boundary and vary it with projector/domain stresses retained",
        },
        {
            "claim": "the split covers horizons and galaxies automatically",
            "result": "fail",
            "reason": "edge domains may carry genuine boundary channels and must not be erased by a lab-local theorem",
            "repair": "keep H_edge and empirical/domain branches separate",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    source_missing = [source for source in source_register_rows() if source["exists"] != "yes"]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not source_missing else "fail",
            "evidence": "all cited sector/projector sources exist" if not source_missing else ";".join(source["source"] for source in source_missing),
            "claim_effect": "attempt traceable",
        },
        {
            "gate": "sector_decomposition_written",
            "status": "pass",
            "evidence": "H_B=H_ord⊕H_MTS⊕H_edge and S_D label are defined",
            "claim_effect": "ordinary/MTS split is well-posed",
        },
        {
            "gate": "block_kernel_lemma_proved",
            "status": "conditional_pass",
            "evidence": "[K,S]=0 with distinct sector eigenvalues implies <H_ord,K H_MTS>=0",
            "claim_effect": "cross kernel can vanish by theorem if parent owns S_D",
        },
        {
            "gate": "ordinary_GR_metric_coupling_preserved",
            "status": "conditional_pass",
            "evidence": "ordinary matter may couple through g_eff while direct rho_MTS activation is forbidden",
            "claim_effect": "projector need not delete ordinary gravity",
        },
        {
            "gate": "gauge_neutral_stress_counterexample_closed",
            "status": "fail",
            "evidence": "EM/matter stress is gauge-neutral enough that gauge slogans alone do not forbid mixing",
            "claim_effect": "need sector label or block kernel from parent action",
        },
        {
            "gate": "sector_label_parent_derived",
            "status": "fail",
            "evidence": "S_D is not derived from parent variables/symmetry",
            "claim_effect": "P_ord_perp not parent-owned",
        },
        {
            "gate": "block_kernel_parent_derived",
            "status": "fail",
            "evidence": "no parent S_boundary proves K_cross=0",
            "claim_effect": "ordinary/MTS split remains conditional",
        },
        {
            "gate": "Bianchi_safe_split_parent_closed",
            "status": "conditional_pass",
            "evidence": "can be honest if block kernel is varied with projector/domain/boundary stress",
            "claim_effect": "no conservation claim without stress ledger",
        },
        {
            "gate": "selector_parent_derived",
            "status": "fail",
            "evidence": "ordinary/MTS split is only one required component of P_MTS",
            "claim_effect": "sigma_D remains theorem target",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "sector label, domain, beta, profile, and official PPN manifest remain underived",
            "claim_effect": "no local-GR/PPN promotion",
        },
        {
            "gate": "B_mem_parent_derived",
            "status": "fail",
            "evidence": "sector split does not derive Q_*, k=9, endpoint occupancies, arrow, or trace partition",
            "claim_effect": "2/27 remains empirical closure/theorem target",
        },
        {
            "gate": "empirical_pivot_allowed",
            "status": "pass",
            "evidence": "local route has a precise remaining blocker and should not be used as evidence",
            "claim_effect": "data work can proceed with local branch labelled conditional",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "priority": 1,
            "target": "derive_sector_label_SD",
            "task": "construct S_D from parent boundary variables, relative class, and ordinary gauge/matter charges",
            "success_gate": "S_D is self-adjoint, gauge/diffeomorphism compatible, and has H_ord/H_MTS as distinct eigenspaces",
        },
        {
            "priority": 2,
            "target": "derive_boundary_block_kernel",
            "task": "write S_boundary whose kinetic kernel commutes with S_D",
            "success_gate": "K_cross=0 follows from variation/symmetry, not from an imposed projector",
        },
        {
            "priority": 3,
            "target": "stress_ledger_for_block_split",
            "task": "write T_boundary+T_projector terms generated by varying S_D, K_boundary, and D",
            "success_gate": "Bianchi identity closes with ordinary metric coupling preserved",
        },
        {
            "priority": 4,
            "target": "edge_domain_manifest",
            "task": "separate lab-local, horizon, galaxy/cluster, and FLRW domain labels",
            "success_gate": "sector split is not used to erase edge domains or galaxy phenomenology",
        },
        {
            "priority": 5,
            "target": "empirical_holdout_pivot",
            "task": "return to strict cosmology/galaxy holdouts with local branch marked conditional",
            "success_gate": "no local-sector theorem is treated as evidence until parent-owned",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "decision": "ordinary/MTS split has a conditional superselection theorem but no parent sector label or block kernel yet",
            "recommended_next": "derive S_D/block kernel or pivot back to empirical holdout testing",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    outputs = {
        "source_register": source_register_rows(),
        "sector_decomposition": sector_decomposition_rows(),
        "block_kernel_theorem": block_kernel_theorem_rows(),
        "mixing_risk_tests": mixing_risk_rows(),
        "no_go_tests": no_go_rows(),
        "promotion_gates": promotion_gate_rows(),
        "next_targets": next_target_rows(),
        "decision": decision_rows(),
    }

    write_csv(results_dir / "source_register.csv", outputs["source_register"], ["source", "role", "exists"])
    write_csv(
        results_dir / "sector_decomposition.csv",
        outputs["sector_decomposition"],
        ["object", "symbol", "definition", "required_split", "role", "status"],
    )
    write_csv(
        results_dir / "block_kernel_theorem.csv",
        outputs["block_kernel_theorem"],
        ["step", "statement", "formula", "result", "status"],
    )
    write_csv(
        results_dir / "mixing_risk_tests.csv",
        outputs["mixing_risk_tests"],
        [
            "case",
            "sector_label_owned",
            "kernel_commutes_with_label",
            "ordinary_stress_gauge_neutral",
            "universal_metric_only",
            "edge_domain",
            "interpretation",
            "cross_kernel_status",
            "status",
        ],
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
    parser = argparse.ArgumentParser(description="Attempt the ordinary/MTS boundary sector split theorem.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
