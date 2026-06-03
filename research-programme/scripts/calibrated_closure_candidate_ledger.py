#!/usr/bin/env python3
"""Package the frozen calibrated closure row without promoting it to evidence."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]

SOURCE_PATHS = {
    "33_status": Path("runs/20260531-003140-CMB-calibration-freedom-audit/status.json"),
    "34_status": Path("runs/20260531-003434-CMB-compatible-MTS-limit-contract/status.json"),
    "35_status": Path("runs/20260531-004152-early-time-decoupling-or-calibration-derivation/status.json"),
    "36_status": Path("runs/20260531-004705-parent-CMB-calibration-map-attempt/status.json"),
    "37_status": Path("runs/20260531-005015-CMB-calibrated-joint-growth-stress/status.json"),
    "37_growth_scores": Path(
        "runs/20260531-005015-CMB-calibrated-joint-growth-stress/results/joint_growth_CMB_same_parameter_scores.csv"
    ),
    "38_status": Path("runs/20260531-005438-calibrated-closure-holdout-contract/status.json"),
    "39_status": Path("runs/20260531-005921-calibrated-background-backreaction-guardrail/status.json"),
    "39_background_scores": Path(
        "runs/20260531-005921-calibrated-background-backreaction-guardrail/results/background_backreaction_scores.csv"
    ),
    "40_status": Path("runs/20260531-010340-fresh-holdout-or-official-likelihood-roadmap/status.json"),
    "41_status": Path("runs/20260531-010754-calibrated-Hz-covariance-guardrail/status.json"),
    "41_hz_summary": Path(
        "runs/20260531-010754-calibrated-Hz-covariance-guardrail/results/Hz_covariance_variant_summary.csv"
    ),
    "36_bmem_corridor": Path(
        "runs/20260531-004705-parent-CMB-calibration-map-attempt/results/bmem_parent_amplitude_corridor.csv"
    ),
}

LOCKED_C0 = "MTS_C0_minimal_smooth_memory_fixed_no_SH0ES"
FROZEN_NATIVE = "C0_native_bmem_CMB_calibrated_shape_frozen"


def absolute_source(key: str) -> Path:
    return POST_CHECKPOINT / SOURCE_PATHS[key]


def load_json(key: str) -> dict[str, Any]:
    return json.loads(absolute_source(key).read_text(encoding="utf-8"))


def read_csv(key: str) -> list[dict[str, str]]:
    with absolute_source(key).open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def row_where(rows: list[dict[str, str]], **matches: str) -> dict[str, str]:
    for row in rows:
        if all(row.get(key) == value for key, value in matches.items()):
            return row
    raise ValueError(f"row not found: {matches}")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, relative_path in SOURCE_PATHS.items():
        absolute_path = POST_CHECKPOINT / relative_path
        rows.append(
            {
                "source_key": key,
                "relative_path": str(relative_path),
                "absolute_path": str(absolute_path),
                "exists": absolute_path.exists(),
            }
        )
    missing = [row["absolute_path"] for row in rows if not row["exists"]]
    if missing:
        raise FileNotFoundError("missing source files: " + "; ".join(missing))
    return rows


def survived_guardrail_rows(statuses: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    growth_rows = read_csv("37_growth_scores")
    background_rows = read_csv("39_background_scores")
    hz_rows = read_csv("41_hz_summary")
    bmem_rows = read_csv("36_bmem_corridor")

    locked_growth = row_where(growth_rows, model=LOCKED_C0)
    frozen_growth = row_where(growth_rows, model=FROZEN_NATIVE)
    locked_background = row_where(background_rows, model="locked_C0_no_SH0ES_fit")
    frozen_background = row_where(background_rows, model=FROZEN_NATIVE)
    suggested_hz = row_where(hz_rows, variant="suggested")
    frozen_eta_one = row_where(bmem_rows, branch=FROZEN_NATIVE, eta_H0_Lcg_over_c="1.0")

    primary_growth_delta = float(frozen_growth["chi2_growth_primary"]) - float(locked_growth["chi2_growth_primary"])
    full_shape_growth_delta = float(frozen_growth["chi2_growth_full_shape_only"]) - float(
        locked_growth["chi2_growth_full_shape_only"]
    )
    sn_delta = float(frozen_background["chi2_sn"]) - float(locked_background["chi2_sn"])
    bao_delta = float(frozen_background["chi2_bao"]) - float(locked_background["chi2_bao"])
    total_delta = float(frozen_background["chi2_total"]) - float(locked_background["chi2_total"])

    return [
        {
            "checkpoint": "35",
            "guardrail": "recombination_background_memory_bound",
            "source": str(absolute_source("35_status")),
            "status": "pass_guardrail",
            "metric": "fractional_memory_contribution_to_H2_at_recombination",
            "value": statuses["35_status"]["worst_recombination_fraction_H2"],
            "comparator": "must be tiny for early plasma safety",
            "interpretation": "direct early-time background memory is bounded as safe",
            "claim_limit": "background_recombination_only_not_CMB_spectra",
            "next_action": "supply perturbation and official CMB contract",
        },
        {
            "checkpoint": "37",
            "guardrail": "compressed_CMB_distance_calibration",
            "source": str(absolute_source("37_status")),
            "status": "pass_closure_only",
            "metric": "native_CMB_calibrated_CMB_chi2",
            "value": statuses["37_status"]["native_CMB_calibrated_CMB_chi2"],
            "comparator": "compressed Planck distance prior",
            "interpretation": "calibration can absorb compressed distance prior",
            "claim_limit": "trained_closure_not_independent_evidence",
            "next_action": "do not use this score for model selection",
        },
        {
            "checkpoint": "37",
            "guardrail": "growth_same_parameter_stress",
            "source": str(absolute_source("37_growth_scores")),
            "status": "pass_guardrail",
            "metric": "delta_chi2_growth_primary_vs_locked; delta_chi2_growth_full_shape_vs_locked",
            "value": f"{primary_growth_delta}; {full_shape_growth_delta}",
            "comparator": "frozen calibrated row vs locked no-SH0ES C0",
            "interpretation": "growth worsens mildly but stays near the locked C0 row",
            "claim_limit": "stress_test_only_not_growth_support",
            "next_action": "require fresh external growth or official perturbation likelihood",
        },
        {
            "checkpoint": "39",
            "guardrail": "late_background_backreaction",
            "source": str(absolute_source("39_background_scores")),
            "status": "pass_guardrail",
            "metric": "delta_chi2_SN; delta_chi2_BAO; delta_chi2_total_vs_locked",
            "value": f"{sn_delta}; {bao_delta}; {total_delta}",
            "comparator": "frozen calibrated row vs locked no-SH0ES C0",
            "interpretation": "late SN/BAO background does not catastrophically backreact",
            "claim_limit": "guardrail_only_not_late_background_win",
            "next_action": "hold parameters frozen in any further test",
        },
        {
            "checkpoint": "41",
            "guardrail": "Hz_covariance_guardrail",
            "source": str(absolute_source("41_hz_summary")),
            "status": "pass_guardrail",
            "metric": "suggested_covariance_delta_vs_locked; suggested_delta_vs_best_baseline",
            "value": (
                f"{suggested_hz['native_delta_vs_locked_C0']}; "
                f"{suggested_hz['native_delta_vs_best_baseline']}"
            ),
            "comparator": "row-locked Moresco15_BC03 covariance branch",
            "interpretation": "frozen calibrated row beats locked C0 and is near LCDM on this reused guardrail",
            "claim_limit": "reused_guardrail_not_independent_support",
            "next_action": "move to official CMB or genuinely fresh holdout",
        },
        {
            "checkpoint": "36",
            "guardrail": "bmem_parent_corridor",
            "source": str(absolute_source("36_bmem_corridor")),
            "status": "plausible_corridor_only",
            "metric": "required_aF_DeltaR_at_eta_1",
            "value": frozen_eta_one["required_aF_DeltaR"],
            "comparator": "order-one trace-budget corridor",
            "interpretation": "amplitude is not absurd but remains conditional",
            "claim_limit": "not_a_parent_prediction",
            "next_action": "derive b_mem from parent invariants or keep closure-only",
        },
    ]


def missing_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "parent_H0_Omega_m0_bmem_map",
            "status": "missing",
            "why_missing": "candidate maps are algebraic or conditional corridors, not predictions",
            "required_work": "derive H0, Omega_m0, and b_mem from parent invariants without fitting to CMB",
            "promotion_if_passed": "closure row can become a parent-predicted cosmology branch",
            "source": str(absolute_source("36_status")),
        },
        {
            "gate": "official_CMB_spectra_lensing_fixed_parameter_likelihood",
            "status": "missing",
            "why_missing": "only compressed distance prior has been used",
            "required_work": "run fixed-parameter official spectra/lensing stress after perturbation contract exists",
            "promotion_if_passed": "CMB guardrail can become a serious high-leverage empirical test",
            "source": str(absolute_source("40_status")),
        },
        {
            "gate": "parent_perturbation_and_early_universe_contract",
            "status": "missing",
            "why_missing": "background expansion is defined but perturbation variables and no-new-knob rules are not",
            "required_work": "define scalar/vector/tensor perturbation closure, sound-horizon policy, and lensing response",
            "promotion_if_passed": "official CMB and growth tests become well-posed",
            "source": str(absolute_source("34_status")),
        },
        {
            "gate": "fresh_external_growth_or_RSD_holdout",
            "status": "missing",
            "why_missing": "current growth/H(z) branches are reused or semi-fresh internal guardrails",
            "required_work": "predeclare and run an external fixed-parameter growth/RSD holdout",
            "promotion_if_passed": "one independent non-CMB empirical pillar becomes available",
            "source": str(absolute_source("40_status")),
        },
        {
            "gate": "independent_predeclaration_and_falsification_rule",
            "status": "missing",
            "why_missing": "closure candidate survived after calibration, so new tests need locked pass/fail rules",
            "required_work": "write exact fail thresholds before seeing any new holdout result",
            "promotion_if_passed": "guardrail language can advance toward evidence language",
            "source": str(absolute_source("38_status")),
        },
        {
            "gate": "local_GR_PPN_reduction",
            "status": "missing",
            "why_missing": "local branch still relies on closure/double-zero obligations rather than derived PPN suppression",
            "required_work": "derive local GR/PPN limit from parent action or keep as explicit closure",
            "promotion_if_passed": "cosmology branch can sit inside a broader field-theory spine",
            "source": "post-checkpoint local branch checkpoints 70-88",
        },
    ]


def claim_language_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim": "the frozen CMB-calibrated closure candidate survived internal guardrails",
            "status": "allowed",
            "allowed_replacement": "same",
            "reason": "matches the evidence level of checkpoints 35-41",
        },
        {
            "claim": "MTS is supported by CMB",
            "status": "forbidden",
            "allowed_replacement": "the compressed CMB distance prior can be absorbed by a frozen closure candidate",
            "reason": "the row was calibrated on compressed CMB information and official spectra/lensing are missing",
        },
        {
            "claim": "the calibrated row beats LCDM, wCDM, or CPL",
            "status": "forbidden",
            "allowed_replacement": "the row remains near baselines on selected guardrails but has no valid model-selection claim",
            "reason": "training/calibration and missing promotion gates invalidate comparison language",
        },
        {
            "claim": "the parent theory derives this branch",
            "status": "forbidden",
            "allowed_replacement": "the branch is a closure candidate awaiting a parent map",
            "reason": "H0, Omega_m0, b_mem, perturbations, and local GR limits are not derived",
        },
        {
            "claim": "local GR is solved",
            "status": "forbidden",
            "allowed_replacement": "local GR/PPN reduction remains an open promotion gate",
            "reason": "closure mechanisms have been bounded and constrained but not derived from a parent action",
        },
        {
            "claim": "public claim",
            "status": "forbidden",
            "allowed_replacement": "private internal checkpoint",
            "reason": "fresh independent holdout and official likelihood work are still missing",
        },
    ]


def promotion_ladder_rows() -> list[dict[str, Any]]:
    return [
        {
            "stage": 0,
            "name": "closure_candidate",
            "current_status": "current_stage_retained",
            "requirement": "survive internal fixed-row guardrails without rescue",
            "claim_level": "internal closure candidate only",
        },
        {
            "stage": 1,
            "name": "fresh_independent_holdout",
            "current_status": "not_started",
            "requirement": "predeclared fixed-parameter external growth/RSD or independent background holdout",
            "claim_level": "empirical stress result if passed",
        },
        {
            "stage": 2,
            "name": "official_CMB_stress",
            "current_status": "blocked_by_contract",
            "requirement": "official spectra/lensing likelihood with no new perturbation knobs",
            "claim_level": "serious CMB stress test if passed",
        },
        {
            "stage": 3,
            "name": "parent_map_derivation",
            "current_status": "missing",
            "requirement": "derive H0, Omega_m0, b_mem, activation shape, and amplitude from parent structure",
            "claim_level": "parent-predicted cosmology branch",
        },
        {
            "stage": 4,
            "name": "theory_promotion",
            "current_status": "not_available",
            "requirement": "local GR/PPN, covariance/conservation, and multiple empirical pillars all pass",
            "claim_level": "serious unified field-theory candidate",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "current_status",
            "status": "calibrated_closure_candidate_retained_not_evidence",
            "evidence": "passed recombination, compressed-CMB closure, growth, late-background, and H(z) guardrails",
            "next_action": "lock claim language and choose official CMB perturbation contract or fresh external holdout",
        },
        {
            "decision": "support_claim",
            "status": "forbidden",
            "evidence": "CMB calibration and reused/semi-fresh guardrails are not independent evidence",
            "next_action": "no public support language until promotion gates pass",
        },
        {
            "decision": "next_target",
            "status": "43-official-CMB-perturbation-contract.md",
            "evidence": "local guardrails are mostly exhausted; official likelihood needs a perturbation/no-knob contract first",
            "next_action": "write exact variables, observables, and fail rules for fixed-parameter official CMB stress",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Calibrated closure candidate ledger.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    source_register = source_register_rows()
    statuses = {key: load_json(key) for key in SOURCE_PATHS if key.endswith("_status")}
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or POST_CHECKPOINT / "runs" / f"{timestamp}-calibrated-closure-candidate-ledger"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    survived = survived_guardrail_rows(statuses)
    missing = missing_gate_rows()
    claims = claim_language_rows()
    ladder = promotion_ladder_rows()
    decisions = decision_rows()

    write_csv(results_dir / "source_checkpoint_register.csv", source_register, list(source_register[0].keys()))
    write_csv(results_dir / "survived_guardrail_ledger.csv", survived, list(survived[0].keys()))
    write_csv(results_dir / "missing_promotion_gates.csv", missing, list(missing[0].keys()))
    write_csv(results_dir / "claim_language_ledger.csv", claims, list(claims[0].keys()))
    write_csv(results_dir / "promotion_ladder.csv", ladder, list(ladder[0].keys()))
    write_csv(results_dir / "decision.csv", decisions, list(decisions[0].keys()))

    status = {
        "status": "complete_calibrated_closure_candidate_ledger",
        "readout": "calibrated_closure_candidate_retained_not_evidence_promotion_gates_locked",
        "recommendation": "write_official_CMB_perturbation_contract_next",
        "next_target": "43-official-CMB-perturbation-contract.md",
        "source_files_checked": len(source_register),
        "survived_guardrails": len(survived),
        "missing_promotion_gates": len(missing),
        "support_claim_allowed": False,
        "public_claim_allowed": False,
        "key_metrics": {
            "recombination_fraction_H2": statuses["35_status"]["worst_recombination_fraction_H2"],
            "native_CMB_calibrated_CMB_chi2": statuses["37_status"]["native_CMB_calibrated_CMB_chi2"],
            "growth_delta_primary_vs_locked": statuses["37_status"][
                "native_CMB_calibrated_growth_delta_vs_locked"
            ],
            "late_background_delta_total_vs_locked": statuses["39_status"]["native_delta_total_vs_locked_C0"],
            "Hz_suggested_delta_vs_locked": statuses["41_status"][
                "suggested_covariance_native_delta_vs_locked_C0"
            ],
            "Hz_suggested_delta_vs_best_baseline": statuses["41_status"][
                "suggested_covariance_native_delta_vs_best_baseline"
            ],
        },
        "outputs": {
            "source_checkpoint_register": str(results_dir / "source_checkpoint_register.csv"),
            "survived_guardrail_ledger": str(results_dir / "survived_guardrail_ledger.csv"),
            "missing_promotion_gates": str(results_dir / "missing_promotion_gates.csv"),
            "claim_language_ledger": str(results_dir / "claim_language_ledger.csv"),
            "promotion_ladder": str(results_dir / "promotion_ladder.csv"),
            "decision": str(results_dir / "decision.csv"),
            "status_json": str(out_dir / "status.json"),
        },
    }
    (out_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (out_dir / "log.txt").write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    (out_dir / "DONE.txt").write_text(status["readout"] + "\n", encoding="utf-8")
    print(json.dumps(status, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
