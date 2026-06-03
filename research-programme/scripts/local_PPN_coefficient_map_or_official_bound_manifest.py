#!/usr/bin/env python3
"""Checkpoint 227: local PPN coefficient map attempt plus official-bound manifest."""

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

CHECKPOINT_227_NAME = "local-PPN-coefficient-map-or-official-bound-manifest"
RUN_226 = RUNS_ROOT / "20260601-000043-local-bound-preflight-and-baseline-comparison"

STATUS = "local_PPN_common_mode_coefficient_contract_and_official_manifest_ready_no_promotion"
CLAIM_CEILING = "coefficient_contract_plus_source_manifest_no_PPN_or_local_GR_claim"
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
        (Path(__file__).resolve(), "checkpoint 227 coefficient/manifest script"),
        (WORK_DIR / "179-local-GR-PPN-silence-contract.md", "local effective scalar guardrail"),
        (WORK_DIR / "221-Noether-source-identity-or-compact-PPN-closure-map.md", "PPN closure vector route"),
        (WORK_DIR / "225-local-GR-route-ledger-and-empirical-pivot-gate.md", "local route ledger"),
        (WORK_DIR / "226-local-bound-preflight-and-baseline-comparison.md", "local-bound dry-run preflight"),
        (RUN_226 / "status.json", "checkpoint 226 machine status"),
        (RUN_226 / "results" / "coefficient_budget_ranking.csv", "coefficient budget rows"),
        (RUN_226 / "results" / "residual_priority_queue.csv", "priority queue rows"),
        (RUN_226 / "results" / "fair_baseline_policy.csv", "baseline policy rows"),
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


def official_bound_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual_channel": "gamma_minus_1",
            "observable": "Cassini solar-conjunction Shapiro/time-delay gamma",
            "bound_or_result": "gamma = 1 + (2.1 +/- 2.3)e-5",
            "source_type": "primary_paper",
            "source_label": "Bertotti, Iess & Tortora, Nature 425, 374-376 (2003)",
            "url": "https://www.nature.com/articles/nature01997",
            "doi": "10.1038/nature01997",
            "usage_policy": "official gamma gate candidate; do not apply until MTS c_gamma map is derived",
        },
        {
            "residual_channel": "gamma_minus_1",
            "observable": "Cassini gamma accuracy review/correction context",
            "bound_or_result": "sigma_gamma = 2.3e-5",
            "source_type": "technical_reference",
            "source_label": "Ashby & Bertotti, NIST publication, 2010",
            "url": "https://www.nist.gov/publications/accurate-light-time-correction-due-gravitating-mass",
            "doi": "",
            "usage_policy": "cross-check source for Cassini gamma scale",
        },
        {
            "residual_channel": "beta_minus_1",
            "observable": "planetary ephemeris/Mercury PPN beta review value",
            "bound_or_result": "beta - 1 = (-4.1 +/- 7.8)e-5 adopting Cassini gamma",
            "source_type": "review_with_primary_refs",
            "source_label": "Will, Living Reviews in Relativity 17, 4 (2014)",
            "url": "https://link.springer.com/article/10.12942/lrr-2014-4",
            "doi": "10.12942/lrr-2014-4",
            "usage_policy": "candidate beta gate; primary ephemeris source should be pulled before public use",
        },
        {
            "residual_channel": "alpha_clock",
            "observable": "Gravity Probe A gravitational redshift",
            "bound_or_result": "agreement at 70e-6 level",
            "source_type": "primary_paper_record",
            "source_label": "Vessot et al., Phys. Rev. Lett. 45, 2081 (1980)",
            "url": "https://www.osti.gov/biblio/6981725",
            "doi": "10.1103/PhysRevLett.45.2081",
            "usage_policy": "historic redshift/local-position-invariance gate candidate",
        },
        {
            "residual_channel": "alpha_clock",
            "observable": "Galileo eccentric-satellite gravitational redshift",
            "bound_or_result": "fractional deviation (+0.19 +/- 2.48)e-5",
            "source_type": "primary_paper_preprint_record",
            "source_label": "Delva et al., Phys. Rev. Lett. 121, 231101 (2018)",
            "url": "https://arxiv.org/abs/1812.03711",
            "doi": "10.1103/PhysRevLett.121.231101",
            "usage_policy": "strong redshift/local-position-invariance gate candidate",
        },
        {
            "residual_channel": "epsilon_matter",
            "observable": "MICROSCOPE weak-equivalence-principle Eotvos parameter",
            "bound_or_result": "eta(Ti,Pt)=(-1.5 +/- 2.3 stat +/- 1.5 syst)e-15",
            "source_type": "primary_paper_preprint_record",
            "source_label": "Touboul et al., Phys. Rev. Lett. 129, 121102 (2022)",
            "url": "https://arxiv.org/abs/2209.15487",
            "doi": "10.1103/PhysRevLett.129.121102",
            "usage_policy": "WEP/composition gate; only applies if MTS creates composition-dependent coupling",
        },
    ]


def coefficient_map_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch": "isotropic_common_mode_metric_response",
            "metric_form": "Phi -> Phi + deltaPhi, Psi -> Psi + deltaPsi with deltaPhi=deltaPsi",
            "residual": "gamma_minus_1",
            "coefficient_result": "c_gamma = 0 at leading order",
            "status": "conditional_pass",
            "required_assumption": "compact memory leakage is pure metric common-mode, no anisotropic boundary stress",
            "failure_mode": "if deltaPhi != deltaPsi, gamma/slip become active and coefficient is unowned",
        },
        {
            "branch": "isotropic_common_mode_metric_response",
            "metric_form": "Phi -> Phi + deltaPhi, Psi -> Psi + deltaPsi with deltaPhi=deltaPsi",
            "residual": "Phi_minus_Psi",
            "coefficient_result": "c_slip = 0 at leading order",
            "status": "conditional_pass",
            "required_assumption": "no trace-free local boundary stress from J_rel/X/V_def sector",
            "failure_mode": "boundary anisotropic stress gives nonzero slip",
        },
        {
            "branch": "universal_metric_coupling",
            "metric_form": "matter couples only to g_mu_nu/coframe, not directly to X,J_rel,V_def",
            "residual": "epsilon_matter",
            "coefficient_result": "c_matter = 0 by coupling contract",
            "status": "contract_pass_not_parent_derived",
            "required_assumption": "universal matter coupling survives parent action completion",
            "failure_mode": "composition coupling is crushed by WEP bounds",
        },
        {
            "branch": "universal_metric_coupling",
            "metric_form": "clock rates follow the same metric with no direct clock-sector coupling",
            "residual": "alpha_clock",
            "coefficient_result": "c_clock = 0 by coupling contract",
            "status": "contract_pass_not_parent_derived",
            "required_assumption": "no direct local-position/clock coupling in memory sector",
            "failure_mode": "clock coupling must face redshift/LPI bounds",
        },
        {
            "branch": "common_mode_source_renormalization",
            "metric_form": "memory leakage acts as common rescaling of Newtonian potential",
            "residual": "G_eff_over_G_minus_1",
            "coefficient_result": "|c_G| <= 1 proxy",
            "status": "conditional_bound",
            "required_assumption": "epsilon_J normalizes directly to the q-like source channel",
            "failure_mode": "source renormalization coefficient must be derived from field equations",
        },
        {
            "branch": "nonlinear_temporal_response",
            "metric_form": "second-order weak-field temporal potential",
            "residual": "beta_minus_1",
            "coefficient_result": "not derived",
            "status": "open",
            "required_assumption": "needs second-order local metric solution",
            "failure_mode": "cannot be bounded from first-order common-mode ansatz alone",
        },
    ]


def official_bound_application_rows(
    manifest_rows: list[dict[str, Any]],
    coefficient_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    status_by_residual = {row["residual"]: row["status"] for row in coefficient_rows}
    result_by_residual = {row["residual"]: row["coefficient_result"] for row in coefficient_rows}
    rows: list[dict[str, Any]] = []
    for row in manifest_rows:
        residual = row["residual_channel"]
        coeff_status = status_by_residual.get(residual, "not_mapped")
        coeff_result = result_by_residual.get(residual, "")
        if coeff_status in {"conditional_pass", "contract_pass_not_parent_derived"}:
            readiness = "conditional_ready_not_claimable"
        elif coeff_status == "conditional_bound":
            readiness = "proxy_bound_ready_not_claimable"
        else:
            readiness = "not_ready"
        rows.append(
            {
                "residual_channel": residual,
                "observable": row["observable"],
                "source_label": row["source_label"],
                "bound_or_result": row["bound_or_result"],
                "coefficient_status": coeff_status,
                "coefficient_result": coeff_result,
                "application_readiness": readiness,
                "claim_allowed": "no_public_claim",
                "next_needed": "derive parent assumptions before applying as observational pass/fail",
            }
        )
    return rows


def top_priority_rows() -> list[dict[str, Any]]:
    budget_rows = read_csv_rows(RUN_226 / "results" / "coefficient_budget_ranking.csv")
    highest = [row for row in budget_rows if row["priority"] == "highest"]
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(highest, start=1):
        residual = row["residual"]
        if residual in {"gamma_minus_1", "Phi_minus_Psi"}:
            recommended = "derive no-anisotropic-stress/common-mode condition from boundary sector"
        elif residual in {"alpha_clock", "epsilon_matter"}:
            recommended = "prove universal metric coupling and no direct memory-sector matter coupling"
        elif residual == "G_eff_over_G_minus_1":
            recommended = "derive local source-renormalization coefficient from weak-field equation"
        else:
            recommended = "derive second-order weak-field temporal response"
        rows.append(
            {
                "rank": index,
                "case": row["case"],
                "residual": residual,
                "max_abs_coefficient_before_proxy_gate": float(row["max_abs_coefficient_before_proxy_gate"]),
                "unit_coefficient_ratio_to_gate": float(row["unit_coefficient_ratio_to_gate"]),
                "recommended_next": recommended,
            }
        )
    return rows


def claim_gate_rows(
    source_rows: list[dict[str, Any]],
    manifest_rows: list[dict[str, Any]],
    coefficient_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = sum(row["exists"] != "yes" for row in source_rows)
    manifest_count = len(manifest_rows)
    conditional_coefficients = sum(row["status"] in {"conditional_pass", "conditional_bound"} for row in coefficient_rows)
    open_coefficients = sum(row["status"] == "open" for row in coefficient_rows)
    return [
        {
            "gate": "all cited local sources exist",
            "status": "pass" if missing_sources == 0 else "fail",
            "evidence": f"missing={missing_sources}",
            "claim_allowed": "internal checkpoint only",
        },
        {
            "gate": "official bound manifest seeded",
            "status": "pass" if manifest_count >= 5 else "fail",
            "evidence": f"manifest_rows={manifest_count}",
            "claim_allowed": "later official-bound run",
        },
        {
            "gate": "at least one coefficient conditionally bounded",
            "status": "pass" if conditional_coefficients > 0 else "fail",
            "evidence": f"conditional_coefficients={conditional_coefficients}",
            "claim_allowed": "theorem target only",
        },
        {
            "gate": "all PPN coefficients parent-derived",
            "status": "fail",
            "evidence": f"open_coefficients={open_coefficients}; assumptions not parent-derived",
            "claim_allowed": "no PPN promotion",
        },
        {
            "gate": "external bounds applied as pass/fail",
            "status": "fail",
            "evidence": "manifest prepared but not used as observational likelihood",
            "claim_allowed": "no external pass/fail",
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
            "meaning": "A conditional coefficient map now exists for the safe local branch: common-mode metric response kills gamma/slip at leading order, universal metric coupling kills direct clock/matter residuals by contract, and G_eff is bounded only as a proxy. Beta remains open. An official-bound manifest is seeded from primary/review sources, but the sources are not applied as observational pass/fail because the parent assumptions behind the coefficient map are not derived.",
            "main_gain": "coefficient pressure points are converted into explicit assumptions and an official-bound source manifest exists for a later run",
            "main_failure": "common-mode/no-slip/universal-coupling assumptions are still not parent-derived and beta remains open",
            "next_target": "228-isotropic-response-condition-or-official-local-bound-runner.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_227_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    manifest_rows = official_bound_manifest_rows()
    coefficient_rows = coefficient_map_attempt_rows()
    application_rows = official_bound_application_rows(manifest_rows, coefficient_rows)
    priority_rows = top_priority_rows()
    gates = claim_gate_rows(source_rows, manifest_rows, coefficient_rows)
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "official_local_bound_manifest.csv": (
            manifest_rows,
            [
                "residual_channel",
                "observable",
                "bound_or_result",
                "source_type",
                "source_label",
                "url",
                "doi",
                "usage_policy",
            ],
        ),
        "coefficient_map_attempt.csv": (
            coefficient_rows,
            [
                "branch",
                "metric_form",
                "residual",
                "coefficient_result",
                "status",
                "required_assumption",
                "failure_mode",
            ],
        ),
        "official_bound_application_readiness.csv": (
            application_rows,
            [
                "residual_channel",
                "observable",
                "source_label",
                "bound_or_result",
                "coefficient_status",
                "coefficient_result",
                "application_readiness",
                "claim_allowed",
                "next_needed",
            ],
        ),
        "top_coefficient_priority.csv": (
            priority_rows,
            [
                "rank",
                "case",
                "residual",
                "max_abs_coefficient_before_proxy_gate",
                "unit_coefficient_ratio_to_gate",
                "recommended_next",
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
    conditional_coefficients = sum(row["status"] in {"conditional_pass", "conditional_bound"} for row in coefficient_rows)
    status_payload = {
        "status": decision[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(files.keys()),
        "missing_sources": missing_sources,
        "official_bound_manifest_rows": len(manifest_rows),
        "official_bound_manifest_ready_for_later_run": True,
        "conditional_or_bounded_coefficients": conditional_coefficients,
        "parent_derived_coefficients": 0,
        "beta_coefficient_status": "open",
        "external_bounds_applied_as_pass_fail": False,
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
    payload = run(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
