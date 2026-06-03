#!/usr/bin/env python3
"""Checkpoint 214: attempt a compact-vs-extended load invariant."""

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

CHECKPOINT_214_NAME = "compact-vs-extended-load-invariant-attempt"
CHECKPOINT_213_RUN = RUNS_ROOT / "20260601-000030-fixed-GK-domain-selector-contract"
CHECKPOINT_212_RUN = RUNS_ROOT / "20260601-000029-composite-GK-local-BAO-galaxy-safety-gate"

STATUS = "compact_extended_load_invariant_candidate_margin_separates_proxies_parent_QJ_missing"
CLAIM_CEILING = "load_morphology_candidate_no_parent_selector_or_galaxy_promotion"
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


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_register_rows() -> list[dict[str, Any]]:
    paths = [
        (Path(__file__).resolve(), "checkpoint 214 compact-vs-extended load invariant script"),
        (WORK_DIR / "213-fixed-GK-domain-selector-contract.md", "domain selector contract checkpoint"),
        (CHECKPOINT_213_RUN / "status.json", "checkpoint 213 machine status"),
        (CHECKPOINT_213_RUN / "results" / "classification_stress_table.csv", "checkpoint 213 classification stress table"),
        (CHECKPOINT_213_RUN / "results" / "missing_invariant_ledger.csv", "checkpoint 213 missing invariant ledger"),
        (WORK_DIR / "212-composite-GK-local-BAO-galaxy-safety-gate.md", "composite G_K safety gate"),
        (CHECKPOINT_212_RUN / "results" / "galaxy_viability_proxy.csv", "checkpoint 212 galaxy proxy readout"),
        (WORK_DIR / "143-domain-selector-variational-action-attempt.md", "C_coh/J_rel selector route"),
        (WORK_DIR / "142-domain-load-tensor-owner-promotion-gate.md", "domain load tensor owner gate"),
        (WORK_DIR / "52-load-tensor-origin-attempt.md", "load tensor origin attempt"),
        (WORK_DIR / "01-motion-load-route-contract.md", "required local/cosmology/galaxy gate contract"),
        (WORK_DIR / "179-local-GR-PPN-silence-contract.md", "local PPN silence contract"),
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


def candidate_invariant_rows() -> list[dict[str, Any]]:
    return [
        {
            "piece": "support_percentile_radius",
            "symbol": "s_80=r_80/R_D",
            "definition": "radius enclosing 80 percent of matter/load support divided by selected domain radius",
            "compact_readout": "small when a compact source sits inside a large exterior-vacuum shell",
            "extended_readout": "order-one when load support fills the galaxy/domain",
            "parent_status": "candidate_from_matter_support",
            "open_issue": "the parent action must define the load measure whose percentile is used",
        },
        {
            "piece": "vacuum_collar_fraction",
            "symbol": "v_collar=1-r_99/R_D",
            "definition": "fractional outer domain collar that is matter/load-free at 99 percent support",
            "compact_readout": "large for Solar-System exterior domains",
            "extended_readout": "small for disk/galaxy domains whose support extends across the observed domain",
            "parent_status": "candidate_topology",
            "open_issue": "real tails need a load threshold or current norm, not a hand cutoff",
        },
        {
            "piece": "inertia_anisotropy",
            "symbol": "A_I=1-3 lambda_min/Tr(I)",
            "definition": "dimensionless inertia/load-shape anisotropy from domain support tensor",
            "compact_readout": "near zero for spherical compact sources",
            "extended_readout": "large for disks/flattened extended loads",
            "parent_status": "candidate_Q_block",
            "open_issue": "spherical extended clusters are extended but not disk-like, so A_I cannot act alone",
        },
        {
            "piece": "edge_load_fraction",
            "symbol": "F_edge=M_outer_collar/M_D or ||J_rel(boundary)||",
            "definition": "load/current fraction in an outer domain collar or relative boundary current norm",
            "compact_readout": "near zero for true exterior-vacuum shells",
            "extended_readout": "nonzero for extended load domains and transitions",
            "parent_status": "candidate_J_rel_block",
            "open_issue": "requires derived J_rel representative and collar definition",
        },
        {
            "piece": "composite_extended_load_score",
            "symbol": "E_L=s_80(1+A_I)/2+F_edge",
            "definition": "minimal diagonal fixed-closure score for compact-vs-extended morphology",
            "compact_readout": "small",
            "extended_readout": "large",
            "parent_status": "candidate_closure",
            "open_issue": "formula weights and edge term are not parent-derived",
        },
    ]


def proxy_profile_rows() -> list[dict[str, Any]]:
    profiles = [
        {
            "case": "solar_1AU_shell",
            "intended_branch": "local_PPN_shell",
            "s80_r80_over_RD": 0.00465,
            "s99_r99_over_RD": 0.00465,
            "A_I": 0.02,
            "F_edge": 0.0,
            "notes": "Sun inside 1 AU exterior shell; compact with large vacuum collar",
        },
        {
            "case": "solar_Mercury_shell",
            "intended_branch": "local_PPN_shell",
            "s80_r80_over_RD": 0.012,
            "s99_r99_over_RD": 0.012,
            "A_I": 0.02,
            "F_edge": 0.0,
            "notes": "Sun inside Mercury-scale exterior shell",
        },
        {
            "case": "earth_GPS_shell",
            "intended_branch": "local_PPN_shell",
            "s80_r80_over_RD": 0.24,
            "s99_r99_over_RD": 0.24,
            "A_I": 0.03,
            "F_edge": 0.0,
            "notes": "Earth source inside GPS-scale exterior shell; worst local compact proxy here",
        },
        {
            "case": "dwarf_3kpc_extended_load",
            "intended_branch": "extended_galaxy_load",
            "s80_r80_over_RD": 0.65,
            "s99_r99_over_RD": 0.95,
            "A_I": 0.65,
            "F_edge": 0.20,
            "notes": "low-x dwarf proxy from checkpoint 213, extended matter/load support",
        },
        {
            "case": "milky_way_8kpc_disk",
            "intended_branch": "extended_galaxy_load",
            "s80_r80_over_RD": 0.85,
            "s99_r99_over_RD": 0.98,
            "A_I": 0.90,
            "F_edge": 0.30,
            "notes": "disk-like extended load through the domain",
        },
        {
            "case": "outer_spiral_30kpc_disk",
            "intended_branch": "extended_galaxy_load",
            "s80_r80_over_RD": 0.55,
            "s99_r99_over_RD": 0.85,
            "A_I": 0.85,
            "F_edge": 0.10,
            "notes": "outer disk proxy with extended but declining support",
        },
        {
            "case": "massive_ETG_5kpc",
            "intended_branch": "extended_galaxy_load",
            "s80_r80_over_RD": 0.65,
            "s99_r99_over_RD": 0.90,
            "A_I": 0.35,
            "F_edge": 0.05,
            "notes": "more spheroidal but still extended galactic load support",
        },
        {
            "case": "cluster_1Mpc_extended_bound",
            "intended_branch": "extended_bound_not_galaxy_claim",
            "s80_r80_over_RD": 0.75,
            "s99_r99_over_RD": 0.95,
            "A_I": 0.20,
            "F_edge": 0.15,
            "notes": "extended bound system, not a galaxy-rotation claim",
        },
        {
            "case": "ambiguous_compact_core",
            "intended_branch": "ambiguous_requires_parent_selector",
            "s80_r80_over_RD": 0.32,
            "s99_r99_over_RD": 0.55,
            "A_I": 0.10,
            "F_edge": 0.02,
            "notes": "stress case deliberately inside the local/extended margin gap",
        },
    ]
    rows: list[dict[str, Any]] = []
    for profile in profiles:
        s80 = float(profile["s80_r80_over_RD"])
        s99 = float(profile["s99_r99_over_RD"])
        anisotropy = float(profile["A_I"])
        edge = float(profile["F_edge"])
        load_score = s80 * (1.0 + anisotropy) / 2.0 + edge
        collar = max(0.0, 1.0 - s99)
        rows.append(
            {
                **profile,
                "vacuum_collar_fraction": collar,
                "E_L_extended_load_score": load_score,
                "compact_indicator": "yes" if collar > 0.5 and load_score < 0.25 else "no",
                "extended_indicator": "yes" if load_score > 0.40 or edge > 0.05 else "no",
                "candidate_class": (
                    "compact_vacuum_shell"
                    if collar > 0.5 and load_score < 0.25
                    else "extended_load"
                    if load_score > 0.40 or edge > 0.05
                    else "ambiguous"
                ),
            }
        )
    return rows


def separation_margin_rows(profile_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    compact_scores = [
        float(row["E_L_extended_load_score"])
        for row in profile_rows
        if row["intended_branch"] == "local_PPN_shell"
    ]
    extended_scores = [
        float(row["E_L_extended_load_score"])
        for row in profile_rows
        if row["intended_branch"] in {"extended_galaxy_load", "extended_bound_not_galaxy_claim"}
    ]
    compact_max = max(compact_scores)
    extended_min = min(extended_scores)
    return [
        {
            "comparison": "representative_compact_vs_extended_proxy_gap",
            "compact_max_E_L": compact_max,
            "extended_min_E_L": extended_min,
            "margin_width": extended_min - compact_max,
            "ratio_extended_min_over_compact_max": extended_min / compact_max,
            "interpretation": "the candidate score margin-separates the representative proxies but does not derive a universal threshold",
        },
        {
            "comparison": "x_gate_failure_repair",
            "compact_max_E_L": compact_max,
            "extended_min_E_L": extended_min,
            "margin_width": extended_min - compact_max,
            "ratio_extended_min_over_compact_max": extended_min / compact_max,
            "interpretation": "dwarf-like low-x extended load is no longer misread as local when support morphology is included",
        },
    ]


def parent_owner_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_clause": "L1_load_measure",
            "required_parent_statement": "define dmu_L from Q, T_matter, or MTS load current so r_80 and r_99 are invariant",
            "current_status": "missing",
            "failure_if_missing": "support percentiles are bookkeeping, not theory",
        },
        {
            "contract_clause": "L2_support_tensor",
            "required_parent_statement": "derive I_ab[D]=integral_D x_a x_b dmu_L or covariant replacement",
            "current_status": "candidate",
            "failure_if_missing": "A_I can become coordinate-dependent",
        },
        {
            "contract_clause": "L3_boundary_current",
            "required_parent_statement": "derive F_edge from J_rel or outer-collar load flux",
            "current_status": "missing",
            "failure_if_missing": "edge term is an inserted morphology flag",
        },
        {
            "contract_clause": "L4_threshold_or_topology",
            "required_parent_statement": "replace numerical cutoffs by topological vacuum-collar class or parent-stable phase gap",
            "current_status": "missing",
            "failure_if_missing": "selector remains closure-level",
        },
        {
            "contract_clause": "L5_domain_variation",
            "required_parent_statement": "variation of D and dmu_L must preserve Bianchi/stress accounting",
            "current_status": "missing",
            "failure_if_missing": "domain selector cannot be promoted as field theory",
        },
    ]


def claim_gate_rows(source_rows: list[dict[str, Any]], profile_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing = sum(row["exists"] != "yes" for row in source_rows)
    intended_failures = representative_failure_count(profile_rows)
    dwarf = next(row for row in profile_rows if row["case"] == "dwarf_3kpc_extended_load")
    ambiguous = next(row for row in profile_rows if row["case"] == "ambiguous_compact_core")
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing == 0 else "fail",
            "evidence": f"missing={missing}",
            "claim_allowed": "internal load-morphology audit",
        },
        {
            "gate": "candidate invariant written",
            "status": "pass",
            "evidence": "E_L=s80(1+A_I)/2+F_edge plus vacuum-collar support",
            "claim_allowed": "candidate closure",
        },
        {
            "gate": "dwarf x-gate failure repaired",
            "status": "pass" if dwarf["candidate_class"] == "extended_load" else "fail",
            "evidence": f"dwarf_E_L={dwarf['E_L_extended_load_score']} class={dwarf['candidate_class']}",
            "claim_allowed": "proxy repair only",
        },
        {
            "gate": "representative stress cases classified",
            "status": "conditional_pass" if intended_failures == 0 else "fail",
            "evidence": f"intended_failures={intended_failures}",
            "claim_allowed": "margin-separated proxy only",
        },
        {
            "gate": "ambiguous cases exposed",
            "status": "pass" if ambiguous["candidate_class"] == "ambiguous" else "fail",
            "evidence": f"ambiguous_E_L={ambiguous['E_L_extended_load_score']} class={ambiguous['candidate_class']}",
            "claim_allowed": "guardrail",
        },
        {
            "gate": "Q/J_rel parent owner derived",
            "status": "fail",
            "evidence": "support measure, boundary current, and threshold/topology not derived",
            "claim_allowed": "no promotion",
        },
        {
            "gate": "galaxy/local selector promoted",
            "status": "fail",
            "evidence": CLAIM_CEILING,
            "claim_allowed": "no",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "meaning": "A compact-vs-extended load candidate was constructed from matter/load support percentiles, inertia anisotropy, and an edge/boundary-current term. It repairs the checkpoint-213 dwarf x-gate failure in representative proxy cases and exposes ambiguous compact-core cases instead of hiding them. But the support measure, edge current, and threshold/topology are not parent-derived, so this is a theorem target/closure object only.",
            "main_gain": "local compact shells and extended galaxy loads can be separated by load-support morphology rather than arena labels",
            "main_failure": "Q/J_rel parent ownership of the load measure and edge current is missing",
            "next_target": "215-QJrel-load-morphology-parent-owner-attempt.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def representative_failure_count(profile_rows: list[dict[str, Any]]) -> int:
    expected_class = {
        "local_PPN_shell": "compact_vacuum_shell",
        "extended_galaxy_load": "extended_load",
        "extended_bound_not_galaxy_claim": "extended_load",
        "ambiguous_requires_parent_selector": "ambiguous",
    }
    return sum(
        row["candidate_class"] != expected_class[row["intended_branch"]]
        for row in profile_rows
        if row["intended_branch"] in expected_class
    )


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_214_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    invariant_rows = candidate_invariant_rows()
    profile_rows = proxy_profile_rows()
    margin_rows = separation_margin_rows(profile_rows)
    contract_rows = parent_owner_contract_rows()
    gates = claim_gate_rows(source_rows, profile_rows)
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "candidate_load_invariants.csv": (
            invariant_rows,
            ["piece", "symbol", "definition", "compact_readout", "extended_readout", "parent_status", "open_issue"],
        ),
        "proxy_profile_classification.csv": (
            profile_rows,
            [
                "case",
                "intended_branch",
                "s80_r80_over_RD",
                "s99_r99_over_RD",
                "A_I",
                "F_edge",
                "notes",
                "vacuum_collar_fraction",
                "E_L_extended_load_score",
                "compact_indicator",
                "extended_indicator",
                "candidate_class",
            ],
        ),
        "separation_margin.csv": (
            margin_rows,
            ["comparison", "compact_max_E_L", "extended_min_E_L", "margin_width", "ratio_extended_min_over_compact_max", "interpretation"],
        ),
        "parent_owner_contract.csv": (
            contract_rows,
            ["contract_clause", "required_parent_statement", "current_status", "failure_if_missing"],
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
    representative_failures = representative_failure_count(profile_rows)
    status_payload = {
        "status": decision[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(files.keys()),
        "missing_sources": missing_sources,
        "candidate_load_invariant_written": True,
        "dwarf_x_gate_failure_repaired_in_proxy": True,
        "representative_proxy_failures": representative_failures,
        "ambiguous_case_exposed": True,
        "Q_Jrel_parent_owner_derived": False,
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
