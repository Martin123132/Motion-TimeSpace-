from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "local-branch-status-ledger-and-empirical-closure-pivot"
STATUS = "local_branch_status_ledger_written_derived_projector_but_domain_and_representative_closure"
CLAIM_CEILING = "local_branch_disciplined_effective_closure_no_derived_local_GR_claim"


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
        (ROOT / "273-Cperp-relative-exactness-C-sector.md", "scalar Cperp exactness failed"),
        (ROOT / "274-lifted-C-sector-form-holonomy-route.md", "lifted C-sector route selected"),
        (ROOT / "275-JC-three-form-memory-current-from-Q.md", "J_C from Qcoh conditional origin"),
        (ROOT / "276-coherent-domain-projector-from-parent-variables.md", "fixed-D Qcoh projection derived"),
        (ROOT / "277-domain-free-boundary-Euler-equation.md", "Ccoh free-boundary Euler equation derived but degenerate"),
        (ROOT / "278-admissible-domain-class-boundary-current-owner.md", "relative-current admissibility"),
        (ROOT / "279-representative-selection-boundary-polarization-no-go.md", "boundary polarization underselects representative"),
        (ROOT / "scripts" / "local_branch_status_ledger_and_empirical_closure_pivot.py", "this status ledger"),
    ]
    return [
        {"source": relpath(path), "role": role, "exists": "yes" if path.exists() else "no"}
        for path, role in sources
    ]


def status_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "item": "scalar_Cperp_relative_exactness",
            "status": "failed",
            "evidence": "scalar residual profiles are not killed by H0 relative exactness",
            "implication": "scalar Cperp route cannot derive projected matter metric",
        },
        {
            "item": "lifted_C_sector_three_form_route",
            "status": "theorem_target",
            "evidence": "3-form/domain class can make local residuals exact while FLRW class survives",
            "implication": "live derivation route, not promotion",
        },
        {
            "item": "JC_from_Qcoh",
            "status": "conditional_kinematic",
            "evidence": "J_C=det(Qcoh) Omega_D/V_D yields integral_D J_C=(N_D/u3)^3",
            "implication": "3D cubic shape can be owned if D/Qcoh/u3 are owned",
        },
        {
            "item": "fixed_D_Qcoh_projection",
            "status": "derived",
            "evidence": "least-squares projection gives Qcoh=(1/3)<Tr Q>_D I",
            "implication": "tracefree shear removed from projected branch for fixed D",
        },
        {
            "item": "Ccoh_free_boundary_Euler_equation",
            "status": "derived_but_degenerate",
            "evidence": "delta Ccoh boundary integrand obtained, but FLRW/local branches are non-unique extrema",
            "implication": "domain problem sharpened, not solved",
        },
        {
            "item": "relative_current_admissibility",
            "status": "conditional_formal",
            "evidence": "delta_eta Q_rel=0 restricts admissible boundary variations",
            "implication": "arbitrary boundary variation restricted, class selection still open",
        },
        {
            "item": "boundary_polarization_Pi",
            "status": "closure_or_no_go_for_promotion",
            "evidence": "endpoint/regularity constraints underselect Pi",
            "implication": "smooth Pi cannot be used as parent derivation",
        },
        {
            "item": "domain_D_selector",
            "status": "closure_theorem_target",
            "evidence": "no parent Euler equation uniquely selects physical D",
            "implication": "no derived local GR claim",
        },
        {
            "item": "projected_matter_metric_exp_CD_g",
            "status": "explicit_effective_closure",
            "evidence": "decouples Cperp if assumed, but scalar/lifted route not parent-derived",
            "implication": "may be tested only with closure label",
        },
        {
            "item": "Bmem_u3_Hstar",
            "status": "closure_theorem_targets",
            "evidence": "Bmem=2/27, u3=1/4/C2 value, and Hstar=H0 not parent-derived here",
            "implication": "amplitude/scale claims remain capped",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "derived_local_GR",
            "status": "fail",
            "evidence": "domain selector and representative selection remain closure/theorem targets",
            "required_to_reopen": "parent action selects D and relative representative without fitted scale",
        },
        {
            "gate": "PPN_silence",
            "status": "conditional_only",
            "evidence": "fixed-D projector removes tracefree shear, but physical D not selected",
            "required_to_reopen": "official local-bound map using labelled closure variables",
        },
        {
            "gate": "Bianchi_conservation",
            "status": "formal_not_complete",
            "evidence": "relative closure/admissibility exists; Pi(Ccoh) and boundary exchange still open",
            "required_to_reopen": "on-shell Noether identity with domain/boundary variables varied",
        },
        {
            "gate": "cosmology_memory_shape",
            "status": "conditional_strengthened",
            "evidence": "J_C from 3D coherent volume gives cubic activation shape",
            "required_to_reopen": "derive u3, Bmem, and official likelihood pass",
        },
        {
            "gate": "empirical_testing_allowed",
            "status": "yes_with_labels",
            "evidence": "closures are explicit and gated",
            "required_to_reopen": "run closure tests against baselines; do not relabel as derivation",
        },
    ]


def empirical_queue_rows() -> list[dict[str, Any]]:
    return [
        {
            "test": "local_proxy_bound_sweep",
            "purpose": "measure residual memory leakage for labelled closure branch",
            "baseline": "GR/local silence limit",
            "claim_allowed": "closure_viability_only",
            "priority": "high",
        },
        {
            "test": "SN_BAO_noCMB_closure_refresh",
            "purpose": "verify cosmology branch still scores competitively after local-closure labels",
            "baseline": "LCDM/wCDM/CPL fitted baselines",
            "claim_allowed": "empirical closure score",
            "priority": "high",
        },
        {
            "test": "CMB_official_likelihood_preflight_repeat_when_assets_exist",
            "purpose": "avoid unofficial CMB claims",
            "baseline": "official Planck/ACT/SPT likelihoods",
            "claim_allowed": "readiness only until assets exist",
            "priority": "medium",
        },
        {
            "test": "domain_sensitivity_jackknife",
            "purpose": "check whether closure depends on arbitrary domain choices",
            "baseline": "same jackknife applied to baseline models where meaningful",
            "claim_allowed": "stability diagnostic",
            "priority": "high",
        },
        {
            "test": "galaxy_pillar_separate",
            "purpose": "keep SPARC/galaxy work as an empirical pillar without forcing it through local Ccoh silence",
            "baseline": "existing galaxy repo/chat results",
            "claim_allowed": "separate pillar only",
            "priority": "medium",
        },
    ]


def claim_policy_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim": "MTS derives local GR",
            "allowed": "no",
            "replacement": "MTS has a conditional local-silence closure with derived fixed-D projector",
        },
        {
            "claim": "projected matter metric is parent-derived",
            "allowed": "no",
            "replacement": "projected matter metric is explicit effective closure/theorem target",
        },
        {
            "claim": "smooth Pi(Ccoh) selects representative",
            "allowed": "no",
            "replacement": "smooth Pi can be tested only as closure; topological quantization remains theorem target",
        },
        {
            "claim": "local branch is dead",
            "allowed": "no",
            "replacement": "local branch is disciplined but unpromoted; exact blockers are known",
        },
        {
            "claim": "empirical tests can continue",
            "allowed": "yes",
            "replacement": "test labelled closure against proper baselines and stability gates",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "The local branch now has a clean ledger: fixed-D Qcoh projection and Ccoh shape derivative are real derivations, while D selection, representative selection, projected matter metric, Pi(Ccoh), Bmem, u3, and Hstar remain closures or theorem targets. "
                "The correct next move is empirical closure testing plus only one narrow derivation route: topological/discrete representative selection."
            ),
            "next_target": "empirical_closure_test_design_or_topological_quantization_theorem_attempt",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "status_ledger.csv": (status_ledger_rows(), ["item", "status", "evidence", "implication"]),
        "promotion_gates.csv": (promotion_gate_rows(), ["gate", "status", "evidence", "required_to_reopen"]),
        "empirical_queue.csv": (empirical_queue_rows(), ["test", "purpose", "baseline", "claim_allowed", "priority"]),
        "claim_policy.csv": (claim_policy_rows(), ["claim", "allowed", "replacement"]),
        "decision.csv": (decision_rows(), ["decision", "claim_ceiling", "meaning", "next_target"]),
    }
    for filename, (rows, fieldnames) in outputs.items():
        write_csv(results_dir / filename, rows, fieldnames)

    payload = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(outputs),
        "derived_items": ["fixed_D_Qcoh_projection", "Ccoh_shape_derivative", "Ccoh_free_boundary_Euler_equation"],
        "conditional_items": ["JC_from_Qcoh", "relative_current_admissibility", "local_stationary_silence", "FLRW_nonzero_class"],
        "closure_items": ["domain_D_selector", "projected_matter_metric", "boundary_polarization_Pi", "Bmem", "u3", "Hstar"],
        "failed_items": ["scalar_Cperp_relative_exactness", "unprojected_detQ_local_silence", "smooth_Pi_parent_selection", "derived_local_GR_claim"],
        "support_claim_allowed": False,
        "empirical_testing_allowed_with_labels": True,
        "recommended_next": "empirical_closure_test_design_or_topological_quantization_theorem_attempt",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Local branch status ledger and empirical closure pivot.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
