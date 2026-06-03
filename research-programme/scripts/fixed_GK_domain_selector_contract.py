#!/usr/bin/env python3
"""Checkpoint 213: zero-knob domain-selector contract for fixed G_K closure."""

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

CHECKPOINT_213_NAME = "fixed-GK-domain-selector-contract"
CHECKPOINT_212_RUN = RUNS_ROOT / "20260601-000029-composite-GK-local-BAO-galaxy-safety-gate"
CHECKPOINT_211_RUN = RUNS_ROOT / "20260601-000028-GK-parent-metric-Ward-identity-attempt"
CHECKPOINT_208_RUN = RUNS_ROOT / "20260601-000025-domain-representative-selection-law"

STATUS = "domain_selector_contract_written_x_gate_insufficient_extended_load_invariant_missing"
CLAIM_CEILING = "domain_selector_contract_no_parent_selection_or_galaxy_promotion"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"

LOCKED_B_MEM = 2.0 / 27.0
LOCAL_DELTA_C_GATE = 4.6e-5
BAO_DELTA_C_GATE = 0.005539695284669133


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
        (Path(__file__).resolve(), "checkpoint 213 fixed G_K domain selector script"),
        (WORK_DIR / "212-composite-GK-local-BAO-galaxy-safety-gate.md", "composite G_K three-arena safety gate"),
        (CHECKPOINT_212_RUN / "status.json", "checkpoint 212 machine status"),
        (CHECKPOINT_212_RUN / "results" / "fixed_closure_arena_readout.csv", "checkpoint 212 arena readout"),
        (CHECKPOINT_212_RUN / "results" / "galaxy_viability_proxy.csv", "checkpoint 212 galaxy proxy readout"),
        (CHECKPOINT_212_RUN / "results" / "domain_separation_necessity.csv", "checkpoint 212 domain separation warning"),
        (WORK_DIR / "211-GK-parent-metric-Ward-identity-attempt.md", "parent metric/Ward checkpoint"),
        (CHECKPOINT_211_RUN / "results" / "future_parent_contract.csv", "checkpoint 211 future parent contract"),
        (WORK_DIR / "208-domain-representative-selection-law.md", "C_coh representative selector checkpoint"),
        (CHECKPOINT_208_RUN / "results" / "coherence_branch_scores.csv", "checkpoint 208 coherence branch scores"),
        (WORK_DIR / "207-domain-projector-action-and-Bianchi-identity.md", "domain projector/Bianchi checkpoint"),
        (WORK_DIR / "143-domain-selector-variational-action-attempt.md", "C_coh/J_rel selector route"),
        (WORK_DIR / "01-motion-load-route-contract.md", "required local/cosmology/galaxy gate contract"),
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


def dimensionless_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "local_gradient_gate",
            "deltaC_gate": LOCAL_DELTA_C_GATE,
            "x_gate_R_over_Lcg": LOCAL_DELTA_C_GATE / LOCKED_B_MEM,
            "meaning": "if x=R/L_cg is below this, the linear full-B_mem local gradient proxy is under the local gate",
        },
        {
            "gate": "BAO_shape_gate",
            "deltaC_gate": BAO_DELTA_C_GATE,
            "x_gate_R_over_Lcg": BAO_DELTA_C_GATE / LOCKED_B_MEM,
            "meaning": "if x=R/L_cg is below this, the linear full-B_mem BAO-like gradient proxy is under the BAO shape gate",
        },
    ]


def selector_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "selector_branch": "smooth_fossil_ruler",
            "required_inputs": "high C_coh; fossil-ruler matter labels; x_150=150Mpc/L_cg below BAO gate; low transition boundary current",
            "forbidden_inputs": "BAO residuals or post-fit alpha choice",
            "intended_readout": "BAO/common-mode domain",
            "status": "contract_only",
            "missing_parent_piece": "domain D and matter-label representative not selected by variation",
        },
        {
            "selector_branch": "local_PPN_shell",
            "required_inputs": "isolated compact-source/vacuum-shell morphology; x_local=R/L_cg below local gate; q_loc source projected out",
            "forbidden_inputs": "declaring a plateau by hand",
            "intended_readout": "local GR/PPN-silent domain",
            "status": "contract_only",
            "missing_parent_piece": "compact-source/vacuum-shell invariant and q_loc projection not derived",
        },
        {
            "selector_branch": "extended_galaxy_load",
            "required_inputs": "bound extended-load morphology; nontrivial load/routing support; internal gradient below BAO-like gate",
            "forbidden_inputs": "treating every low-x bound object as local PPN shell",
            "intended_readout": "galaxy empirical pillar domain",
            "status": "contract_only",
            "missing_parent_piece": "Q/J_rel morphology invariant separating compact local shells from extended disks",
        },
        {
            "selector_branch": "transition_or_wall",
            "required_inputs": "large x, high shear/boundary current, or failed BAO smoothness",
            "forbidden_inputs": "promoting transition domains as BAO common-mode",
            "intended_readout": "unpromoted transition/stress branch",
            "status": "contract_only",
            "missing_parent_piece": "boundary current representative and stress variation",
        },
    ]


def expected_label(case: str) -> str:
    if case in {"ideal_FLRW", "smooth_BAO_late_domain"}:
        return "smooth_fossil_ruler"
    if case in {"Gpc_transition_domain", "BAO_scale_transition"}:
        return "transition_or_wall"
    if case in {"solar_system_1AU_Weyl", "earth_surface_Weyl"}:
        return "local_PPN_shell"
    if case in {"dwarf_3kpc", "milky_way_8kpc", "outer_spiral_30kpc", "massive_ETG_5kpc"}:
        return "extended_galaxy_load"
    if case == "cluster_1Mpc":
        return "extended_bound_not_galaxy_claim"
    return "unknown"


def x_gate_only_label(x_value: float) -> str:
    local_x = LOCAL_DELTA_C_GATE / LOCKED_B_MEM
    bao_x = BAO_DELTA_C_GATE / LOCKED_B_MEM
    if x_value <= local_x:
        return "local_PPN_shell"
    if x_value <= bao_x:
        return "extended_or_smooth_safe"
    return "transition_or_wall"


def contract_label(case: str, x_value: float, ccoh_class: str, morphology_flag: str) -> str:
    if ccoh_class == "high_coherence" and x_value <= BAO_DELTA_C_GATE / LOCKED_B_MEM:
        return "smooth_fossil_ruler"
    if morphology_flag == "compact_vacuum_shell" and x_value <= LOCAL_DELTA_C_GATE / LOCKED_B_MEM:
        return "local_PPN_shell"
    if morphology_flag == "extended_load" and x_value <= BAO_DELTA_C_GATE / LOCKED_B_MEM:
        return "extended_galaxy_load"
    if case == "cluster_1Mpc" and morphology_flag == "extended_cluster_load":
        return "extended_bound_not_galaxy_claim"
    return "transition_or_wall"


def classification_stress_rows() -> list[dict[str, Any]]:
    arena_rows = read_csv_rows(CHECKPOINT_212_RUN / "results" / "fixed_closure_arena_readout.csv")
    galaxy_rows = read_csv_rows(CHECKPOINT_212_RUN / "results" / "galaxy_viability_proxy.csv")
    rows: list[dict[str, Any]] = []
    arena_case_meta = {
        "ideal_FLRW": ("high_coherence", "fossil_ruler"),
        "smooth_BAO_late_domain": ("high_coherence", "fossil_ruler"),
        "Gpc_transition_domain": ("low_or_mixed_coherence", "transition"),
        "BAO_scale_transition": ("low_or_mixed_coherence", "transition"),
        "solar_system_1AU_Weyl": ("low_coherence", "compact_vacuum_shell"),
        "earth_surface_Weyl": ("low_coherence", "compact_vacuum_shell"),
        "milky_way_8kpc_Weyl": ("low_coherence", "extended_load"),
    }
    for row in arena_rows:
        case = row["case"]
        l_cg = float(row["L_cg_Mpc"])
        baseline = float(row["baseline_Mpc"])
        x_value = baseline / l_cg
        ccoh_class, morphology = arena_case_meta.get(case, ("unknown", "unknown"))
        expected = "extended_galaxy_load" if case == "milky_way_8kpc_Weyl" else expected_label(case)
        x_only = x_gate_only_label(x_value)
        contract = contract_label(case, x_value, ccoh_class, morphology)
        rows.append(
            {
                "case": case,
                "x_R_over_Lcg": x_value,
                "C_coh_class": ccoh_class,
                "morphology_flag": morphology,
                "expected_label": expected,
                "x_gate_only_label": x_only,
                "contract_label_with_morphology": contract,
                "x_gate_only_passes": "yes" if x_only == expected or (x_only == "extended_or_smooth_safe" and expected in {"extended_galaxy_load", "smooth_fossil_ruler", "extended_bound_not_galaxy_claim"}) else "no",
                "contract_passes": "yes" if contract == expected else "no",
                "lesson": "x gates alone are insufficient; C_coh and morphology/Q/J_rel information are needed",
            }
        )
    for row in galaxy_rows:
        case = row["case"]
        l_cg = float(row["L_cg_Mpc"])
        radius_mpc = float(row["radius_kpc"]) / 1000.0
        x_value = radius_mpc / l_cg
        morphology = "extended_cluster_load" if case == "cluster_1Mpc" else "extended_load"
        expected = expected_label(case)
        x_only = x_gate_only_label(x_value)
        contract = contract_label(case, x_value, "low_coherence", morphology)
        rows.append(
            {
                "case": case,
                "x_R_over_Lcg": x_value,
                "C_coh_class": "low_coherence",
                "morphology_flag": morphology,
                "expected_label": expected,
                "x_gate_only_label": x_only,
                "contract_label_with_morphology": contract,
                "x_gate_only_passes": "yes" if x_only == expected or (x_only == "extended_or_smooth_safe" and expected in {"extended_galaxy_load", "smooth_fossil_ruler", "extended_bound_not_galaxy_claim"}) else "no",
                "contract_passes": "yes" if contract == expected else "no",
                "lesson": "dwarf-like low-x extended loads expose the need for a morphology invariant",
            }
        )
    return rows


def missing_invariant_rows(stress_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    x_failures = sum(row["x_gate_only_passes"] != "yes" for row in stress_rows)
    contract_failures = sum(row["contract_passes"] != "yes" for row in stress_rows)
    return [
        {
            "missing_invariant": "compact_vs_extended_load_morphology",
            "evidence": "x gates alone misclassify at least some representative cases",
            "severity": "blocking",
            "needed_form": "Q/J_rel or matter-support invariant distinguishing compact vacuum shell from extended disk/load",
        },
        {
            "missing_invariant": "C_coh_parent_selection",
            "evidence": "smooth BAO requires high coherence label from checkpoint 208, still not parent-selected",
            "severity": "blocking_for_promotion",
            "needed_form": "variation selecting C_coh representative and domain D",
        },
        {
            "missing_invariant": "transition_boundary_current",
            "evidence": "transition domains must remain unpromoted; boundary current representative still absent",
            "severity": "blocking_for_transition_claims",
            "needed_form": "derived J_rel representative and stress accounting",
        },
        {
            "missing_invariant": "selector_failure_counts",
            "evidence": f"x_gate_only_failures={x_failures}; contract_with_morphology_failures={contract_failures}",
            "severity": "diagnostic",
            "needed_form": "if contract_with_morphology still fails, revise labels before any empirical run",
        },
    ]


def claim_gate_rows(source_rows: list[dict[str, Any]], stress_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing = sum(row["exists"] != "yes" for row in source_rows)
    x_failures = sum(row["x_gate_only_passes"] != "yes" for row in stress_rows)
    contract_failures = sum(row["contract_passes"] != "yes" for row in stress_rows)
    dwarf_row = next(row for row in stress_rows if row["case"] == "dwarf_3kpc")
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing == 0 else "fail",
            "evidence": f"missing={missing}",
            "claim_allowed": "internal selector contract audit",
        },
        {
            "gate": "dimensionless x gates derived from existing bounds",
            "status": "pass",
            "evidence": f"x_local={LOCAL_DELTA_C_GATE / LOCKED_B_MEM}; x_BAO={BAO_DELTA_C_GATE / LOCKED_B_MEM}",
            "claim_allowed": "proxy thresholds",
        },
        {
            "gate": "x-only selector sufficient",
            "status": "fail" if x_failures > 0 else "pass",
            "evidence": f"x_gate_only_failures={x_failures}; dwarf_x_label={dwarf_row['x_gate_only_label']}",
            "claim_allowed": "no x-only selector promotion",
        },
        {
            "gate": "morphology-augmented contract classifies stress cases",
            "status": "conditional_pass" if contract_failures == 0 else "fail",
            "evidence": f"contract_failures={contract_failures}",
            "claim_allowed": "contract only, not parent derivation",
        },
        {
            "gate": "compact-vs-extended morphology invariant derived",
            "status": "fail",
            "evidence": "morphology_flag is supplied by the audit, not derived from parent Q/J_rel",
            "claim_allowed": "no promotion",
        },
        {
            "gate": "domain selector ready for empirical scoring",
            "status": "fail",
            "evidence": CLAIM_CEILING,
            "claim_allowed": "no",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "meaning": "The dimensionless x=R/L_cg gates derived from local and BAO bounds are useful, but not sufficient. They separate smooth/transition behavior and local AU shells, yet low-x extended loads such as dwarf-galaxy proxies can be misread as local unless an additional compact-vs-extended morphology invariant is supplied. A zero-knob selector therefore needs Q/J_rel or equivalent matter-support information.",
            "main_gain": "domain selector contract is now explicit and testable",
            "main_failure": "compact local shells versus extended galaxy loads are not parent-separated",
            "next_target": "214-compact-vs-extended-load-invariant-attempt.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_213_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    gate_rows = dimensionless_gate_rows()
    contract_rows = selector_contract_rows()
    stress_rows = classification_stress_rows()
    missing_rows = missing_invariant_rows(stress_rows)
    gates = claim_gate_rows(source_rows, stress_rows)
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "dimensionless_selector_gates.csv": (
            gate_rows,
            ["gate", "deltaC_gate", "x_gate_R_over_Lcg", "meaning"],
        ),
        "selector_contract.csv": (
            contract_rows,
            ["selector_branch", "required_inputs", "forbidden_inputs", "intended_readout", "status", "missing_parent_piece"],
        ),
        "classification_stress_table.csv": (
            stress_rows,
            [
                "case",
                "x_R_over_Lcg",
                "C_coh_class",
                "morphology_flag",
                "expected_label",
                "x_gate_only_label",
                "contract_label_with_morphology",
                "x_gate_only_passes",
                "contract_passes",
                "lesson",
            ],
        ),
        "missing_invariant_ledger.csv": (
            missing_rows,
            ["missing_invariant", "evidence", "severity", "needed_form"],
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
    x_gate_failures = sum(row["x_gate_only_passes"] != "yes" for row in stress_rows)
    contract_failures = sum(row["contract_passes"] != "yes" for row in stress_rows)
    status_payload = {
        "status": decision[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(files.keys()),
        "missing_sources": missing_sources,
        "x_local_gate_R_over_Lcg": LOCAL_DELTA_C_GATE / LOCKED_B_MEM,
        "x_BAO_gate_R_over_Lcg": BAO_DELTA_C_GATE / LOCKED_B_MEM,
        "x_gate_only_failures": x_gate_failures,
        "morphology_augmented_contract_failures": contract_failures,
        "compact_vs_extended_morphology_invariant_derived": False,
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
