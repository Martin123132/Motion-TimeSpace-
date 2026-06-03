#!/usr/bin/env python3
"""Checkpoint 215: attempt parent ownership of the load-morphology invariant."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

CHECKPOINT_215_NAME = "QJrel-load-morphology-parent-owner-attempt"
CHECKPOINT_214_RUN = RUNS_ROOT / "20260601-000031-compact-vs-extended-load-invariant-attempt"
CHECKPOINT_213_RUN = RUNS_ROOT / "20260601-000030-fixed-GK-domain-selector-contract"

STATUS = "QJrel_matter_support_owner_partial_Jrel_threshold_missing_closure_retained"
CLAIM_CEILING = "load_morphology_parent_owner_partial_no_selector_or_galaxy_promotion"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_register_rows() -> list[dict[str, Any]]:
    paths = [
        (Path(__file__).resolve(), "checkpoint 215 Q/Jrel load-morphology parent-owner script"),
        (WORK_DIR / "214-compact-vs-extended-load-invariant-attempt.md", "compact-vs-extended load invariant checkpoint"),
        (CHECKPOINT_214_RUN / "status.json", "checkpoint 214 machine status"),
        (CHECKPOINT_214_RUN / "results" / "candidate_load_invariants.csv", "checkpoint 214 candidate invariants"),
        (CHECKPOINT_214_RUN / "results" / "proxy_profile_classification.csv", "checkpoint 214 proxy classification"),
        (WORK_DIR / "213-fixed-GK-domain-selector-contract.md", "domain selector contract checkpoint"),
        (CHECKPOINT_213_RUN / "status.json", "checkpoint 213 machine status"),
        (WORK_DIR / "52-load-tensor-origin-attempt.md", "Q load tensor kinematic origin"),
        (WORK_DIR / "142-domain-load-tensor-owner-promotion-gate.md", "domain/load owner promotion gate"),
        (WORK_DIR / "143-domain-selector-variational-action-attempt.md", "domain selector and J_rel route"),
        (WORK_DIR / "204-matter-metric-action-and-ruler-transport-owner-contract.md", "matter metric/action contract"),
        (WORK_DIR / "207-domain-projector-action-and-Bianchi-identity.md", "domain projector/Bianchi checkpoint"),
    ]
    rows: list[dict[str, Any]] = []
    for path, role in paths:
        exists = path.exists()
        rows.append(
            {
                "source": path.name,
                "path": str(path),
                "exists": "yes" if exists else "no",
                "sha256": sha256_file(path) if exists and path.is_file() else "",
                "role": role,
                "issue": "" if exists else "missing",
            }
        )
    return rows


def owner_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "owner_candidate": "Q_only",
            "proposed_measure": "dmu_Q=sqrt(h)||Q_TF|| d^3x or sqrt(h)||Q|| d^3x",
            "owns": "load anisotropy if Q is present",
            "works_for": "dynamic/anisotropic coherent-load domains",
            "fails_for": "stationary compact matter sources and possibly virialized systems where coherent Q averages away",
            "verdict": "fail_as_sole_owner",
        },
        {
            "owner_candidate": "matter_support_trace",
            "proposed_measure": "dmu_m=sqrt(h)|T_matter| d^3x in the matter frame",
            "owns": "r_80, r_99, support inertia, compact-vs-extended matter morphology",
            "works_for": "compact local sources and extended baryonic load support",
            "fails_for": "pure geometric/routing load not carried by matter stress",
            "verdict": "partial_best_support_owner",
        },
        {
            "owner_candidate": "relative_boundary_current",
            "proposed_measure": "F_edge=||J_rel[outer collar or boundary]||/(int_D dmu_L+epsilon)",
            "owns": "outer-collar/boundary support and transition readout",
            "works_for": "distinguishing true exterior-vacuum shells from extended/transition domains",
            "fails_for": "current representative still not derived",
            "verdict": "formal_best_edge_owner_missing",
        },
        {
            "owner_candidate": "hybrid_matter_Q_Jrel",
            "proposed_measure": "dmu_L=dmu_m plus Q-shape block; F_edge from J_rel",
            "owns": "s_80, r_99, A_I, and edge support without arena labels",
            "works_for": "checkpoint-214 morphology contract",
            "fails_for": "weights/representative/domain variation still not parent-fixed",
            "verdict": "best_fixed_closure_contract",
        },
    ]


def derivation_chain_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "claim": "The matter action can supply a scalar support measure after a domain and matter frame are selected.",
            "equation": "dmu_m = sqrt(h) |T_tilde| d^3x",
            "status": "partial_pass",
            "gap": "depends on matter-frame/domain ownership and does not include pure geometric load",
        },
        {
            "step": 2,
            "claim": "Given dmu_L, percentile support radii are invariant domain functionals.",
            "equation": "int_{B(r80)} dmu_L = 0.8 int_D dmu_L",
            "status": "formal_pass",
            "gap": "requires a parent load measure and a covariant ball/bitensor construction",
        },
        {
            "step": 3,
            "claim": "Given dmu_L, support inertia gives a compact-vs-disk/spheroid shape readout.",
            "equation": "I_ab=int_D X_a X_b dmu_L; A_I=1-3 lambda_min/Tr(I)",
            "status": "formal_pass",
            "gap": "coordinate-free construction and parent load measure still needed",
        },
        {
            "step": 4,
            "claim": "The Q block can add MTS-native load anisotropy but cannot replace matter support.",
            "equation": "A_Q ~ ||Q_TF||/(|Tr Q|+epsilon)",
            "status": "partial_support",
            "gap": "Q owner is partial and can vanish in stationary local or virialized domains",
        },
        {
            "step": 5,
            "claim": "The edge term wants J_rel, not an empirical collar fraction.",
            "equation": "F_edge = ||[J_rel]_{outer}||/(int_D dmu_L+epsilon)",
            "status": "formal_best_route",
            "gap": "J_rel representative and boundary stress are still missing",
        },
        {
            "step": 6,
            "claim": "The full E_L morphology score can be owned only by a hybrid matter/Q/J_rel construction.",
            "equation": "E_L=s80(1+A_I)/2+F_edge",
            "status": "closure_retained",
            "gap": "relative weights, threshold/topology, and Bianchi variation not derived",
        },
    ]


def sole_owner_stress_rows() -> list[dict[str, Any]]:
    return [
        {
            "test": "Q_only_on_solar_shell",
            "expected": "compact_vacuum_shell",
            "Q_only_readout": "may vanish or see no coherent load",
            "failure": "cannot detect compact matter support by itself",
            "verdict": "fail",
        },
        {
            "test": "matter_only_on_disk",
            "expected": "extended_galaxy_load",
            "Q_only_readout": "not applicable",
            "failure": "matter support can classify morphology but not routing/geometric edge load",
            "verdict": "partial_pass",
        },
        {
            "test": "Jrel_only_on_static_shell",
            "expected": "compact_vacuum_shell",
            "Q_only_readout": "not applicable",
            "failure": "if J_rel=0 it says silent, but does not define r80 or inertia",
            "verdict": "partial_fail",
        },
        {
            "test": "hybrid_on_checkpoint214_proxies",
            "expected": "margin-separated compact vs extended readout",
            "Q_only_readout": "uses matter support plus Q/J sidecars",
            "failure": "not parent-derived",
            "verdict": "conditional_pass_as_closure",
        },
    ]


def parent_gap_rows() -> list[dict[str, Any]]:
    return [
        {
            "gap": "domain_D_owner",
            "current_status": "missing",
            "why_blocking": "all support integrals are over D",
            "required_next": "derive D or freeze pre-empirical selector",
        },
        {
            "gap": "J_rel_representative",
            "current_status": "missing",
            "why_blocking": "edge term F_edge otherwise remains a collar proxy",
            "required_next": "derive local trivial / FLRW nontrivial / extended boundary representatives",
        },
        {
            "gap": "load_measure_weights",
            "current_status": "missing",
            "why_blocking": "matter, Q, and J blocks cannot be freely weighted",
            "required_next": "fix weights by parent norm or use matter-only support plus separate J gate",
        },
        {
            "gap": "threshold_or_topological_phase_gap",
            "current_status": "missing",
            "why_blocking": "numeric compact/extended cuts are not theorem-level",
            "required_next": "replace thresholds by vacuum-collar topology or a derived stable phase gap",
        },
        {
            "gap": "Bianchi_stress_variation",
            "current_status": "missing",
            "why_blocking": "domain/support/edge variation must appear in total stress",
            "required_next": "compute variation before field-theory promotion",
        },
    ]


def claim_gate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing = sum(row["exists"] != "yes" for row in source_rows)
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing == 0 else "fail",
            "evidence": f"missing={missing}",
            "claim_allowed": "internal parent-owner audit",
        },
        {
            "gate": "Q sole-owner route",
            "status": "fail",
            "evidence": "Q can vanish in stationary compact domains and cannot alone define matter support",
            "claim_allowed": "no",
        },
        {
            "gate": "matter support owns r80/r99/inertia",
            "status": "partial_pass",
            "evidence": "dmu_m=sqrt(h)|T_matter| can define support percentiles if D/frame are owned",
            "claim_allowed": "partial support owner",
        },
        {
            "gate": "J_rel owns edge term",
            "status": "fail_open",
            "evidence": "J_rel is the right object but representative is still missing",
            "claim_allowed": "formal target only",
        },
        {
            "gate": "hybrid E_L parent-derived",
            "status": "fail",
            "evidence": "weights, threshold/topology, domain variation, and J_rel not derived",
            "claim_allowed": "fixed closure only",
        },
        {
            "gate": "selector/galaxy promotion",
            "status": "fail",
            "evidence": CLAIM_CEILING,
            "claim_allowed": "no",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "meaning": "Matter support can partially own the percentile and inertia pieces of E_L, while Q supplies a possible MTS-native anisotropy block and J_rel is the natural owner of the edge term. But Q alone fails as a sole owner, J_rel is still not represented, and the weights/topological threshold are not parent-derived. The compact-vs-extended morphology invariant therefore remains a fixed closure/theorem target.",
            "main_gain": "the owner structure is now split cleanly: matter support for s80/A_I, J_rel for F_edge, Q as anisotropy sidecar",
            "main_failure": "J_rel representative, D owner, and threshold/topology are missing",
            "next_target": "216-load-morphology-sidecar-galaxy-test-plan.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_215_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    owner_rows = owner_candidate_rows()
    chain_rows = derivation_chain_rows()
    stress_rows = sole_owner_stress_rows()
    gap_rows = parent_gap_rows()
    gates = claim_gate_rows(source_rows)
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "owner_candidate_ledger.csv": (
            owner_rows,
            ["owner_candidate", "proposed_measure", "owns", "works_for", "fails_for", "verdict"],
        ),
        "derivation_chain.csv": (
            chain_rows,
            ["step", "claim", "equation", "status", "gap"],
        ),
        "sole_owner_stress_tests.csv": (
            stress_rows,
            ["test", "expected", "Q_only_readout", "failure", "verdict"],
        ),
        "parent_gap_ledger.csv": (
            gap_rows,
            ["gap", "current_status", "why_blocking", "required_next"],
        ),
        "claim_gate_results.csv": (
            gates,
            ["gate", "status", "evidence", "claim_allowed"],
        ),
        "decision.csv": (
            decision,
            ["decision", "meaning", "main_gain", "main_failure", "next_target", "promotion_allowed", "claim_ceiling"],
        ),
    }
    for filename, (rows, fieldnames) in files.items():
        write_csv(results_dir / filename, rows, fieldnames)

    missing_sources = sum(row["exists"] != "yes" for row in source_rows)
    status_payload = {
        "status": decision[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(files.keys()),
        "missing_sources": missing_sources,
        "Q_sole_owner_sufficient": False,
        "matter_support_owner_partial": True,
        "J_rel_edge_owner_derived": False,
        "hybrid_E_L_parent_derived": False,
        "domain_selector_parent_derived": False,
        "promotion_allowed": False,
        "next_target": decision[0]["next_target"],
    }
    write_json(run_dir / "status.json", status_payload)
    (run_dir / "DONE.txt").write_text(status_payload["status"] + "\n", encoding="utf-8")
    return status_payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timestamp", default=None, help="Optional run timestamp prefix.")
    args = parser.parse_args()
    payload = run(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
