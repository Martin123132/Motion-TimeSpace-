#!/usr/bin/env python3
"""Write the no-smuggling contract for a BAO/ruler-only projection theorem."""

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

FAILURE_RUN = RUNS_ROOT / "20260531-235959-cell-clock-failure-mode-audit"
FAILURE_RESULTS = FAILURE_RUN / "results"
CLAIM_CEILING = "ruler_only_projection_contract_no_bridge_promotion"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


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
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_role(path: Path) -> str:
    name = path.name
    if name.startswith("158-") or "cell-clock-failure-mode" in str(path):
        return "failure-mode evidence for ruler-only route"
    if name.startswith("154-") or name.startswith("155-") or name.startswith("157-"):
        return "prior projection/clock checkpoint"
    if name.startswith("10-"):
        return "observer/coframe contract"
    if name.startswith("53-") or name.startswith("54-"):
        return "coherent domain/local-silence contract"
    if name.endswith(".py"):
        return "machine auditor"
    return "supporting source"


def source_register_rows(script_path: Path) -> list[dict[str, Any]]:
    paths = [
        script_path,
        WORK_DIR / "10-observer-map-symplectic-contract.md",
        WORK_DIR / "53-coherent-projection-local-silence-gate.md",
        WORK_DIR / "54-coherent-domain-and-u3-origin.md",
        WORK_DIR / "154-anisotropic-BAO-projection-owner-attempt.md",
        WORK_DIR / "155-redshift-projection-clock-map-owner.md",
        WORK_DIR / "157-cell-balanced-clock-map-fixed-branch-retest.md",
        WORK_DIR / "158-cell-clock-BAO-row-and-SN-Hz-failure-mode-audit.md",
        FAILURE_RUN / "status.json",
        FAILURE_RESULTS / "decision.csv",
        FAILURE_RESULTS / "gate_results.csv",
        FAILURE_RESULTS / "ruler_only_projection_scores.csv",
        FAILURE_RESULTS / "chi2_decomposition.csv",
        FAILURE_RESULTS / "bao_observable_summary.csv",
    ]
    rows = []
    for path in paths:
        exists = path.exists()
        rows.append(
            {
                "source": path.name,
                "path": str(path),
                "exists": "yes" if exists else "no",
                "sha256": sha256_file(path) if exists and path.is_file() else "",
                "role": source_role(path),
                "issue": "" if exists else "missing",
            }
        )
    return rows


def evidence_summary_rows() -> list[dict[str, Any]]:
    ruler = read_csv_rows(FAILURE_RESULTS / "ruler_only_projection_scores.csv")
    decisions = read_csv_rows(FAILURE_RESULTS / "decision.csv")
    gates = read_csv_rows(FAILURE_RESULTS / "gate_results.csv")
    summary_rows = []
    for row in ruler:
        summary_rows.append(
            {
                "evidence_item": row["policy"],
                "value": row["delta_BIC_vs_LCDM"],
                "support": f"readout_vs_LCDM={row['readout_vs_LCDM']}; delta_BIC_vs_no_clock={row['delta_BIC_vs_no_clock']}; delta_BIC_vs_global={row['delta_BIC_vs_global_clock']}",
                "interpretation": "ruler-only route beats LCDM but not no-clock MTS",
            }
        )
    for item in ["status", "main_failure_mode", "BAO_projection", "Hz_pressure"]:
        row = next(entry for entry in decisions if entry["item"] == item)
        summary_rows.append(
            {
                "evidence_item": item,
                "value": row["verdict"],
                "support": row["evidence"],
                "interpretation": "failure-mode audit decision",
            }
        )
    for item in ["ruler_only_projection", "global_clock_coupling", "promotion"]:
        row = next(entry for entry in gates if entry["gate"] == item)
        summary_rows.append(
            {
                "evidence_item": item,
                "value": row["status"],
                "support": row["evidence"],
                "interpretation": "gate result",
            }
        )
    return summary_rows


def theorem_object_rows() -> list[dict[str, Any]]:
    return [
        {
            "object": "BAO pair-separation observable",
            "symbol": "ell_BAO^A",
            "required_definition": "a two-point spatial/radial separation vector inferred from galaxy clustering, not a one-point photon luminosity observable",
            "current_status": "conceptual_target",
            "non_smuggling_condition": "must be defined before fitting DESI rows",
        },
        {
            "object": "ruler projection tensor",
            "symbol": "R^A_B[D,Q]",
            "required_definition": "maps the FLRW standard-ruler separation into observed radial/transverse BAO channels",
            "current_status": "missing_parent_object",
            "non_smuggling_condition": "Pi_parallel and Pi_perp must be components/eigenvalues of one tensor, not row-wise factors",
        },
        {
            "object": "screen projector",
            "symbol": "P_perp^A_B",
            "required_definition": "observer-screen projection transverse to line of sight",
            "current_status": "standard_geometric_piece",
            "non_smuggling_condition": "must use the same observer coframe as local/SN/H(z) limits",
        },
        {
            "object": "radial projector",
            "symbol": "n^A n_B",
            "required_definition": "line-of-sight projection for radial BAO interval",
            "current_status": "standard_geometric_piece",
            "non_smuggling_condition": "radial derivative response must be integrable with transverse response",
        },
        {
            "object": "coherent scalar load",
            "symbol": "X_D",
            "required_definition": "X_D=(1/u3) integral P_coh[Theta] d tau with local silence X_D=0 in bound domains",
            "current_status": "conditional_from_prior_work",
            "non_smuggling_condition": "domain D and u3 must be parent-owned; no fitted BAO smoothing scale",
        },
        {
            "object": "projection amplitude",
            "symbol": "Xi_D",
            "required_definition": "fixed scalar such as B_mem*(1/24)*X_D*F_D*(1-X_D/4) or derived replacement",
            "current_status": "candidate_not_derived",
            "non_smuggling_condition": "B_mem->0 implies Xi_D=0; constants fixed before data",
        },
        {
            "object": "SN immunity condition",
            "symbol": "delta D_L_SN = 0 at this order",
            "required_definition": "standard candles/one-point photon luminosity distance do not inherit the BAO ruler projection",
            "current_status": "required_not_derived",
            "non_smuggling_condition": "must follow from two-point ruler transport, not by saying SN is exempt",
        },
        {
            "object": "metric/equivalence safety",
            "symbol": "not delta g_mu_nu",
            "required_definition": "projection is not a universal metric or photon-geodesic deformation",
            "current_status": "mandatory",
            "non_smuggling_condition": "if it is metric/geodesic, SN and H(z) must see it and global clock failure returns",
        },
    ]


def candidate_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "metric_projection",
            "definition": "modify spacetime metric or null geodesic distances directly",
            "status": "rejected_for_ruler_only",
            "why": "SN, H(z), lensing, and local clocks must also see a metric/geodesic change",
            "next_action": "only use as global model, which 157/158 disfavored",
        },
        {
            "route": "universal_clock_map",
            "definition": "global z_true=z_obs+zeta applies to BAO and SN",
            "status": "demoted",
            "why": "strict SN and primary SN+BAO penalize it",
            "next_action": "do not use as leading bridge route",
        },
        {
            "route": "two_point_ruler_transport",
            "definition": "projection acts on galaxy-pair separation/ruler inference, not individual photon distance",
            "status": "best_live_route",
            "why": "matches 158: BAO projection live, SN global coupling damaging",
            "next_action": "derive R^A_B[D,Q] from coframe/domain-boundary physics",
        },
        {
            "route": "late_time_ruler_calibration",
            "definition": "effective BAO ruler transport changes inferred D_M/r_d and D_H/r_d after recombination without changing r_d",
            "status": "live_high_risk",
            "why": "could protect primary CMB r_d, but risks becoming a BAO-only calibration patch",
            "next_action": "derive redshift dependence and CMB/lensing safety",
        },
        {
            "route": "galaxy_bias_or_selection_projection",
            "definition": "BAO feature position shifts through tracer/statistical selection effects",
            "status": "deferred",
            "why": "plausible observationally but too survey-specific for field-theory spine unless parent-derived",
            "next_action": "use only after checking official likelihood/systematics",
        },
        {
            "route": "ad_hoc_BAO_only_patch",
            "definition": "insert Pi_parallel and Pi_perp to improve DESI rows",
            "status": "rejected",
            "why": "not a field-theory route",
            "next_action": "forbidden except as diagnostic closure",
        },
    ]


def no_smuggling_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "two_point_vs_one_point_distinction",
            "condition": "derive why BAO pair separations can carry R^A_B while SN luminosity distance does not",
            "status": "open_mandatory",
            "failure_if_missing": "BAO-only exemption by hand",
        },
        {
            "gate": "not_metric_deformation",
            "condition": "prove R^A_B is not a universal delta g_mu_nu or photon-geodesic remap",
            "status": "open_mandatory",
            "failure_if_missing": "SN/H(z)/lensing must inherit it; global-clock failure returns",
        },
        {
            "gate": "single_tensor_integrability",
            "condition": "derive Pi_perp and Pi_parallel from one R^A_B[D,Q] with D_M, D_H, and D_V consistency",
            "status": "open_mandatory",
            "failure_if_missing": "row-wise BAO patch",
        },
        {
            "gate": "zero_memory_limit",
            "condition": "B_mem or X_D -> 0 implies R^A_B -> identity",
            "status": "contract_satisfied_if_candidate_owned",
            "failure_if_missing": "projection not tied to MTS memory",
        },
        {
            "gate": "local_silence",
            "condition": "bound/local domains with X_D=0 do not change local rods/clocks/PPN",
            "status": "conditional_from_coherent_domain_work",
            "failure_if_missing": "local GR route threatened",
        },
        {
            "gate": "CMB_r_d_safety",
            "condition": "projection does not alter early sound horizon unless full Boltzmann branch derives it",
            "status": "open_mandatory",
            "failure_if_missing": "CMB bridge becomes uncontrolled",
        },
        {
            "gate": "SN_Hz_null_prediction",
            "condition": "at leading order, SN and H(z) use the no-clock late-time branch",
            "status": "empirically_motivated_not_theorem",
            "failure_if_missing": "ruler-only diagnostic loses physics status",
        },
        {
            "gate": "pre_data_shape_lock",
            "condition": "R^A_B redshift shape and constants are fixed before DESI/Pantheon scoring",
            "status": "open_mandatory",
            "failure_if_missing": "projection is a tuned BAO repair",
        },
    ]


def formula_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "formula": "ell_obs^A = R^A_B[D,Q] ell_FLRW^B",
            "meaning": "BAO is treated as a projected two-point separation observable",
            "allowed_claim": "definition target only",
            "blocker": "R^A_B not parent-derived",
        },
        {
            "step": 2,
            "formula": "R^A_B = delta^A_B + Pi_perp P_perp^A_B + Pi_parallel n^A n_B",
            "meaning": "one tensor supplies transverse and radial BAO projection",
            "allowed_claim": "integrability contract",
            "blocker": "Pi_perp/Pi_parallel source law missing",
        },
        {
            "step": 3,
            "formula": "Pi_AB = Pi_AB[X_D,F_D,boundary/coframe invariants]",
            "meaning": "projection must come from coherent-domain memory variables",
            "allowed_claim": "theorem target",
            "blocker": "boundary/coframe scalar/tensor not constructed",
        },
        {
            "step": 4,
            "formula": "D_M^BAO/r_d -> (1+Pi_perp) D_M/r_d; D_H^BAO/r_d -> (1+Pi_parallel) D_H/r_d",
            "meaning": "BAO observable correction if the tensor is derived",
            "allowed_claim": "diagnostic projection form",
            "blocker": "currently empirical diagnostic, not action-derived",
        },
        {
            "step": 5,
            "formula": "D_L^SN = D_L^no-clock + O(Pi^2 or explicitly derived coupling)",
            "meaning": "SN immunity condition",
            "allowed_claim": "required null theorem",
            "blocker": "must derive why one-point photon luminosity is not projected",
        },
        {
            "step": 6,
            "formula": "H_CC(z) = H_no-clock(z) + O(Pi^2 or explicitly derived coupling)",
            "meaning": "cosmic chronometer immunity/null test",
            "allowed_claim": "required null theorem",
            "blocker": "derivative-map coupling not parent-derived",
        },
    ]


def gate_result_rows(no_smuggling_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    open_mandatory = [row for row in no_smuggling_rows if str(row["status"]).startswith("open")]
    return [
        {
            "gate": "ruler_only_empirical_motivation",
            "status": "pass",
            "evidence": "158 ruler-only u3quarter delta_BIC_vs_LCDM=-3.868328116780731 and better than global clock",
        },
        {
            "gate": "global_clock_demoted",
            "status": "pass",
            "evidence": "158 strict SN and primary SN+BAO demote universal clock coupling",
        },
        {
            "gate": "field_theory_contract_complete",
            "status": "fail",
            "evidence": f"open mandatory gates={len(open_mandatory)}",
        },
        {
            "gate": "equivalence_metric_safety",
            "status": "fail_open",
            "evidence": "must prove projection is not metric/geodesic or accept SN/H(z)/lensing coupling",
        },
        {
            "gate": "BAO_patch_guard",
            "status": "fail_open",
            "evidence": "single parent tensor and pre-data shape not derived",
        },
        {
            "gate": "promotion",
            "status": "fail",
            "evidence": CLAIM_CEILING,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "item": "status",
            "verdict": "ruler_only_projection_contract_written_parent_theorem_missing",
            "evidence": "global clock is demoted; ruler-only projection has a no-smuggling contract but no parent derivation",
        },
        {
            "item": "live_route",
            "verdict": "two_point_BAO_ruler_transport_or_late_ruler_calibration",
            "evidence": "must affect BAO pair separations without altering SN one-point luminosity distances",
        },
        {
            "item": "rejected_route",
            "verdict": "universal_metric_or_clock_projection_as_bridge",
            "evidence": "would couple to SN/H(z)/lensing and is already empirically disfavored in 157/158",
        },
        {
            "item": "main_risk",
            "verdict": "BAO_only_patch_or_equivalence_violation",
            "evidence": "ruler-only exemption must be parent-derived, not asserted",
        },
        {
            "item": "claim_status",
            "verdict": CLAIM_CEILING,
            "evidence": "contract only; no BAO/CMB/local-GR promotion",
        },
        {
            "item": "next_target",
            "verdict": "160-ruler-projection-parent-tensor-attempt.md",
            "evidence": "construct or reject R^A_B[D,Q] from observer coframe/coherent-domain boundary physics",
        },
    ]


def run_contract(output_root: Path, timestamp: str | None) -> Path:
    run_stamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{run_stamp}-ruler-only-projection-theorem-contract"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows(Path(__file__).resolve())
    missing = [row["path"] for row in sources if row["exists"] != "yes"]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    evidence = evidence_summary_rows()
    theorem_objects = theorem_object_rows()
    routes = candidate_route_rows()
    no_smuggling = no_smuggling_gate_rows()
    formulas = formula_contract_rows()
    gates = gate_result_rows(no_smuggling)
    decisions = decision_rows()

    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "sha256", "role", "issue"])
    write_csv(results_dir / "evidence_summary.csv", evidence, ["evidence_item", "value", "support", "interpretation"])
    write_csv(
        results_dir / "theorem_object_contract.csv",
        theorem_objects,
        ["object", "symbol", "required_definition", "current_status", "non_smuggling_condition"],
    )
    write_csv(results_dir / "candidate_route_ledger.csv", routes, ["route", "definition", "status", "why", "next_action"])
    write_csv(
        results_dir / "no_smuggling_gates.csv",
        no_smuggling,
        ["gate", "condition", "status", "failure_if_missing"],
    )
    write_csv(
        results_dir / "formula_contract.csv",
        formulas,
        ["step", "formula", "meaning", "allowed_claim", "blocker"],
    )
    write_csv(results_dir / "gate_results.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    status_value = next(row["verdict"] for row in decisions if row["item"] == "status")
    status = {
        "status": status_value,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "claim_ceiling": CLAIM_CEILING,
        "open_mandatory_gates": sum(1 for row in no_smuggling if str(row["status"]).startswith("open")),
        "generated": [
            "source_register.csv",
            "evidence_summary.csv",
            "theorem_object_contract.csv",
            "candidate_route_ledger.csv",
            "no_smuggling_gates.csv",
            "formula_contract.csv",
            "gate_results.csv",
            "decision.csv",
        ],
        "next_target": "160-ruler-projection-parent-tensor-attempt.md",
    }
    write_json(run_dir / "status.json", status)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    parser.add_argument("--timestamp", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(run_contract(args.output_root, args.timestamp))


if __name__ == "__main__":
    main()
