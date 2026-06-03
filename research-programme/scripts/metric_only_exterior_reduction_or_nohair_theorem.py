#!/usr/bin/env python3
"""Checkpoint 238: metric-only exterior reduction or no-hair theorem."""

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

CHECKPOINT_238_NAME = "metric-only-exterior-reduction-or-nohair-theorem"
RUN_237 = RUNS_ROOT / "20260601-000054-local-EH-exterior-action-contract"

STATUS = "metric_only_exterior_reduction_sector_audit_partial_nohair_not_derived_no_promotion"
CLAIM_CEILING = "sector_nohair_audit_no_metric_only_parent_reduction_or_PPN_promotion"
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


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    paths = [
        (Path(__file__).resolve(), "checkpoint 238 runner"),
        (WORK_DIR / "178-memory-perturbation-owner-attempt.md", "effective high-cs memory owner"),
        (WORK_DIR / "179-local-GR-PPN-silence-contract.md", "local screened EFT fence"),
        (WORK_DIR / "221-Noether-source-identity-or-compact-PPN-closure-map.md", "source identity and q_loc route"),
        (WORK_DIR / "224-defect-potential-Vdef-or-X-route-demotion.md", "V_def/X demotion"),
        (WORK_DIR / "235-projector-stress-variation-or-nohair-constraint-algebra.md", "safe branch/no-hair conditions"),
        (WORK_DIR / "237-local-EH-exterior-action-contract.md", "EH exterior action contract"),
        (RUN_237 / "status.json", "checkpoint 237 machine status"),
        (RUN_237 / "results" / "EH_exterior_contract_conditions.csv", "checkpoint 237 exterior contract"),
        (RUN_237 / "results" / "coefficient_status_after_237.csv", "checkpoint 237 coefficient status"),
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


def sector_reduction_rows() -> list[dict[str, Any]]:
    return [
        {
            "sector": "ordinary_matter",
            "required_exterior_reduction": "T_matter|E=0 outside compact source",
            "current_support": "standard compact exterior definition",
            "status": "pass_as_region_definition",
            "remaining_gap": "universal matter coupling still needed for clocks/WEP",
        },
        {
            "sector": "effective_memory_scalar",
            "required_exterior_reduction": "no local exterior scalar force; cosmology-only/tidal EFT role",
            "current_support": "checkpoint 179 screened effective scalar fence",
            "status": "screened_effective_not_parent_nohair",
            "remaining_gap": "reconstructed scalar not fundamental MTS parent",
        },
        {
            "sector": "Pi_M_mass_class",
            "required_exterior_reduction": "absolute flux becomes conserved M_eff monopole",
            "current_support": "Hodge/topology split preserves mass class",
            "status": "contract_not_derived",
            "remaining_gap": "M_eff conservation and source normalization not derived",
        },
        {
            "sector": "Pi_TF_shear",
            "required_exterior_reduction": "trace-free/tangential shear vanishes",
            "current_support": "scalar-boundary symmetry sufficient route",
            "status": "conditional",
            "remaining_gap": "parent boundary variable set could still contain tangent tensor channels",
        },
        {
            "sector": "Pi_matter_direct",
            "required_exterior_reduction": "direct memory coupling to matter/clocks absent",
            "current_support": "universal coupling contract",
            "status": "contract_not_derived",
            "remaining_gap": "matter/clock action not written",
        },
        {
            "sector": "P_mem_Jrel",
            "required_exterior_reduction": "relative memory current exact and boundary-cancelled",
            "current_support": "relative H2 cohomology gate plus P_mem candidate",
            "status": "topology_gate_plus_parent_gap",
            "remaining_gap": "P_mem, A_rel, and source identity not parent-derived",
        },
        {
            "sector": "T_projector",
            "required_exterior_reduction": "projector stress included and cancels/vanishes",
            "current_support": "delta P_mem split and safe conditions C1-C6",
            "status": "structured_not_derived",
            "remaining_gap": "delta P_mem/delta g not computed from parent action",
        },
        {
            "sector": "X_multiplier",
            "required_exterior_reduction": "X carries no propagating exterior degree",
            "current_support": "rank-zero first-order route and no-hair tests",
            "status": "not_derived",
            "remaining_gap": "constraint bracket closure requires parent symplectic structure",
        },
        {
            "sector": "V_def_PY",
            "required_exterior_reduction": "defect potential leaves no exterior nonmetric hair",
            "current_support": "partial trace/flow ownership; X route demoted",
            "status": "not_derived",
            "remaining_gap": "V_def, Z_mu_nu, M_AB, cross terms not parent-derived",
        },
        {
            "sector": "boundary_primitive_Arel",
            "required_exterior_reduction": "pure-gauge/vanishing boundary primitive",
            "current_support": "conditional exactness route",
            "status": "not_derived",
            "remaining_gap": "parent action does not select A_rel representative",
        },
    ]


def reduction_verdict_rows() -> list[dict[str, Any]]:
    sector_rows = sector_reduction_rows()
    return [
        {
            "verdict": "fully_reduced_sectors",
            "count": sum(row["status"] == "pass_as_region_definition" for row in sector_rows),
            "meaning": "ordinary matter absence is definitional only",
        },
        {
            "verdict": "conditional_or_screened_sectors",
            "count": sum(row["status"] in {"conditional", "screened_effective_not_parent_nohair", "topology_gate_plus_parent_gap", "structured_not_derived"} for row in sector_rows),
            "meaning": "useful theorem gates exist but parent no-hair is not complete",
        },
        {
            "verdict": "not_derived_sectors",
            "count": sum(row["status"] in {"not_derived", "contract_not_derived"} for row in sector_rows),
            "meaning": "metric-only exterior reduction cannot be promoted",
        },
        {
            "verdict": "metric_only_exterior_parent_derived",
            "count": 0,
            "meaning": "the full reduction is not derived in the current corpus",
        },
    ]


def nohair_theorem_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target": "N1_Meff",
            "required_theorem": "Pi_M harmonic flux is conserved M_eff and has no radial memory profile",
            "failure_if_missing": "G_eff/beta source profile is unowned",
        },
        {
            "target": "N2_no_TF",
            "required_theorem": "scalar boundary variables exclude trace-free/tangential exterior stress",
            "failure_if_missing": "gamma/slip not owned",
        },
        {
            "target": "N3_universal_coupling",
            "required_theorem": "matter and clocks couple only to metric/coframe",
            "failure_if_missing": "WEP/clock bounds attack directly",
        },
        {
            "target": "N4_exact_relative_memory",
            "required_theorem": "P_mem J_rel is exact with pure-gauge boundary primitive and source identity",
            "failure_if_missing": "q_loc not derived",
        },
        {
            "target": "N5_projector_stress",
            "required_theorem": "T_projector vanishes or cancels in total Bianchi identity",
            "failure_if_missing": "conservation is fake",
        },
        {
            "target": "N6_auxiliary_nohair",
            "required_theorem": "X/J_rel/V_def have no exterior propagating degrees",
            "failure_if_missing": "fifth-force or beta hair remains possible",
        },
    ]


def coefficient_status_rows() -> list[dict[str, Any]]:
    previous = read_csv_rows(RUN_237 / "results" / "coefficient_status_after_237.csv")
    previous_by_residual = {row["residual"]: row for row in previous}
    updates = {
        "gamma_minus_1": (
            "sector_audit_blocks_promotion_until_N2",
            "gamma remains conditional on no trace-free exterior stress",
            "derive N2_no_TF",
        ),
        "Phi_minus_Psi": (
            "sector_audit_blocks_promotion_until_N2",
            "slip remains conditional on scalar boundary/no-shear theorem",
            "derive N2_no_TF",
        ),
        "G_eff_over_G_minus_1": (
            "sector_audit_blocks_promotion_until_N1",
            "source normalization remains conditional on conserved M_eff",
            "derive N1_Meff",
        ),
        "alpha_clock": (
            "sector_audit_blocks_promotion_until_N3",
            "clock safety remains universal-coupling contract",
            "derive N3_universal_coupling",
        ),
        "epsilon_matter": (
            "sector_audit_blocks_promotion_until_N3",
            "WEP safety remains universal-coupling contract",
            "derive N3_universal_coupling",
        ),
        "beta_minus_1": (
            "sector_audit_blocks_promotion_until_N1_to_N6",
            "beta=1 still requires complete no-hair plus EH exterior operator",
            "derive N1-N6 and EH exterior action",
        ),
    }
    rows: list[dict[str, Any]] = []
    for residual, prior in previous_by_residual.items():
        status, result, next_needed = updates[residual]
        rows.append(
            {
                "residual": residual,
                "checkpoint_237_status": prior["checkpoint_237_status"],
                "checkpoint_238_status": status,
                "coefficient_after_238": result,
                "parent_derived": "no",
                "promotion_allowed": "false",
                "next_needed": next_needed,
            }
        )
    return rows


def claim_gate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = sum(row["exists"] != "yes" for row in source_rows)
    return [
        {
            "gate": "all cited local sources exist",
            "status": "pass" if missing_sources == 0 else "fail",
            "evidence": f"missing={missing_sources}",
            "claim_allowed": "internal checkpoint only",
        },
        {
            "gate": "nonmetric exterior sector audit written",
            "status": "pass",
            "evidence": "10 sector rows",
            "claim_allowed": "audit only",
        },
        {
            "gate": "no-hair theorem targets listed",
            "status": "pass",
            "evidence": "N1-N6",
            "claim_allowed": "theorem roadmap",
        },
        {
            "gate": "metric-only exterior parent-derived",
            "status": "fail",
            "evidence": "multiple sectors remain conditional/not-derived",
            "claim_allowed": "no EH promotion",
        },
        {
            "gate": "beta derived",
            "status": "fail",
            "evidence": "requires N1-N6 plus EH operator",
            "claim_allowed": "no PPN claim",
        },
        {
            "gate": "local GR or PPN promoted",
            "status": "fail",
            "evidence": CLAIM_CEILING,
            "claim_allowed": "no",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "meaning": "The metric-only exterior reduction does not derive yet. The audit shows one definitional pass, several useful conditional/screened gates, and multiple not-derived sectors. The route is not dead: it is now split into six no-hair theorem targets N1-N6. But local EH, beta=1, and PPN promotion remain blocked until those targets are parent-owned.",
            "main_gain": "the non-metric exterior leftovers are now enumerated sector by sector",
            "main_failure": "X/V_def/A_rel/projector stress and source normalization still block metric-only reduction",
            "next_target": "239-nohair-theorem-targets-or-local-bound-runner.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_238_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    sectors = sector_reduction_rows()
    verdict = reduction_verdict_rows()
    nohair_targets = nohair_theorem_target_rows()
    coefficients = coefficient_status_rows()
    gates = claim_gate_rows(source_rows)
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "nonmetric_exterior_sector_audit.csv": (
            sectors,
            ["sector", "required_exterior_reduction", "current_support", "status", "remaining_gap"],
        ),
        "metric_only_reduction_verdict.csv": (
            verdict,
            ["verdict", "count", "meaning"],
        ),
        "nohair_theorem_targets.csv": (
            nohair_targets,
            ["target", "required_theorem", "failure_if_missing"],
        ),
        "coefficient_status_after_238.csv": (
            coefficients,
            [
                "residual",
                "checkpoint_237_status",
                "checkpoint_238_status",
                "coefficient_after_238",
                "parent_derived",
                "promotion_allowed",
                "next_needed",
            ],
        ),
        "claim_gate_results.csv": (
            gates,
            ["gate", "status", "evidence", "claim_allowed"],
        ),
        "decision.csv": (
            decision,
            [
                "decision",
                "meaning",
                "main_gain",
                "main_failure",
                "next_target",
                "promotion_allowed",
                "claim_ceiling",
            ],
        ),
    }
    for filename, file_data in files.items():
        rows, fieldnames = file_data
        write_csv(results_dir / filename, rows, fieldnames)

    missing_sources = sum(row["exists"] != "yes" for row in source_rows)
    not_derived_sectors = sum(row["status"] in {"not_derived", "contract_not_derived"} for row in sectors)
    status_payload = {
        "status": decision[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(files.keys()),
        "missing_sources": missing_sources,
        "nonmetric_exterior_sector_audit_written": True,
        "sector_rows": len(sectors),
        "not_derived_sector_count": not_derived_sectors,
        "nohair_theorem_targets_written": True,
        "metric_only_exterior_parent_derived": False,
        "local_EH_operator_derived": False,
        "beta_second_order_parent_derived": False,
        "official_bounds_applied_as_pass_fail": False,
        "PPN_promoted": False,
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
    print(json.dumps(run(args.timestamp), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
