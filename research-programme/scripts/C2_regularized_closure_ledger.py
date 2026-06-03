#!/usr/bin/env python3
"""Package the C2 regularized activation route without promoting it to evidence."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]

SOURCE_PATHS = {
    "45_status": Path("runs/20260531-013422-memory-scalar-reconstruction-gate/status.json"),
    "45_endpoint": Path("runs/20260531-013422-memory-scalar-reconstruction-gate/results/endpoint_regularities.csv"),
    "46_status": Path("runs/20260531-013929-activation-regularity-repair-gate/status.json"),
    "46_candidate_laws": Path("runs/20260531-013929-activation-regularity-repair-gate/results/candidate_activation_laws.csv"),
    "46_background_deviation": Path("runs/20260531-013929-activation-regularity-repair-gate/results/candidate_background_deviation.csv"),
    "47_status": Path("runs/20260531-014459-C2-activation-background-smoke/status.json"),
    "47_scores": Path("runs/20260531-014459-C2-activation-background-smoke/results/C2_activation_background_scores.csv"),
    "48_status": Path("runs/20260531-015005-C2-activation-growth-CMB-retest/status.json"),
    "48_scores": Path("runs/20260531-015005-C2-activation-growth-CMB-retest/results/C2_activation_growth_CMB_scores.csv"),
    "48_gates": Path("runs/20260531-015005-C2-activation-growth-CMB-retest/results/C2_activation_growth_CMB_gates.csv"),
}

C2_LABEL = "C2_weibull_p3_match_N50"
ORIGINAL_LABEL = "C0_frozen_original_fractional_weibull"


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
        rows.append({"source_key": key, "relative_path": str(relative_path), "absolute_path": str(absolute_path), "exists": absolute_path.exists()})
    missing = [row["absolute_path"] for row in rows if not row["exists"]]
    if missing:
        raise FileNotFoundError("missing source files: " + "; ".join(missing))
    return rows


def fix_survival_rows(statuses: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    endpoint_rows = read_csv("45_endpoint")
    candidate_rows = read_csv("46_candidate_laws")
    deviation_rows = read_csv("46_background_deviation")
    late_rows = read_csv("47_scores")
    cmb_rows = read_csv("48_scores")

    original_law = row_where(candidate_rows, candidate="original_fractional_weibull")
    c2_law = row_where(candidate_rows, candidate="weibull_p3_match_N50")
    c2_deviation = row_where(deviation_rows, candidate="weibull_p3_match_N50")
    c2_late = row_where(late_rows, model=C2_LABEL)
    c2_cmb = row_where(cmb_rows, model=C2_LABEL)
    c2_endpoint = row_where(endpoint_rows, test="smooth_canonical_threshold")

    return [
        {
            "checkpoint": "45",
            "item": "original_fractional_endpoint_failure",
            "status": "fixed_by_C2_replacement",
            "source": str(absolute_source("45_endpoint")),
            "old_value": statuses["45_status"]["key_metrics"]["nu_act"],
            "new_value": c2_law["endpoint_power"],
            "metric": "endpoint_power",
            "interpretation": f"original status was {c2_endpoint['status']}; C2 p=3 reaches finite canonical dV/dphi threshold",
            "claim_limit": "regularity_fix_only",
        },
        {
            "checkpoint": "46",
            "item": "C2_C1_no_knob_candidate",
            "status": "pass",
            "source": str(absolute_source("46_candidate_laws")),
            "old_value": f"C2={original_law['C2_endpoint_status']}; canonical={original_law['canonical_C1_potential_status']}",
            "new_value": f"C2={c2_law['C2_endpoint_status']}; canonical={c2_law['canonical_C1_potential_status']}",
            "metric": "regularity_law_status",
            "interpretation": "minimal p=3 Weibull is regularity-safe without adding a continuous shape knob",
            "claim_limit": "candidate_not_parent_derivation",
        },
        {
            "checkpoint": "46",
            "item": "background_shape_shift_precheck",
            "status": "small_but_requires_retest",
            "source": str(absolute_source("46_background_deviation")),
            "old_value": "0",
            "new_value": c2_deviation["frac_delta_DM_zstar_vs_original"],
            "metric": "fractional_D_M_zstar_shift_vs_original",
            "interpretation": "C2 repair is close in distance but not identical, so retest was required",
            "claim_limit": "no_inheritance_from_original_fit",
        },
        {
            "checkpoint": "47",
            "item": "late_background_smoke",
            "status": "pass_guardrail",
            "source": str(absolute_source("47_scores")),
            "old_value": "original frozen fractional branch",
            "new_value": c2_late["delta_late_plus_Hz_vs_original_frozen"],
            "metric": "delta_chi2_SN_BAO_Hz_vs_original",
            "interpretation": "regularity repair did not wreck late-background/H(z) closure behaviour",
            "claim_limit": "guardrail_only",
        },
        {
            "checkpoint": "48",
            "item": "growth_CMB_Hz_retest",
            "status": "pass_guardrail",
            "source": str(absolute_source("48_scores")),
            "old_value": "original frozen fractional branch",
            "new_value": c2_cmb["delta_total_vs_original_frozen"],
            "metric": "delta_chi2_growth_CMB_Hz_vs_original",
            "interpretation": "C2 repair survived primary growth, full-shape growth, compressed CMB, and H(z) gates",
            "claim_limit": "regularized_closure_candidate_only",
        },
    ]


def surviving_metric_rows(statuses: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    late_rows = read_csv("47_scores")
    cmb_rows = read_csv("48_scores")
    c2_late = row_where(late_rows, model=C2_LABEL)
    original_late = row_where(late_rows, model=ORIGINAL_LABEL)
    c2_cmb = row_where(cmb_rows, model=C2_LABEL)
    original_cmb = row_where(cmb_rows, model=ORIGINAL_LABEL)
    return [
        {
            "metric": "late_SN_BAO_Hz_delta_vs_original",
            "C2_value": c2_late["chi2_late_plus_Hz"],
            "original_value": original_late["chi2_late_plus_Hz"],
            "delta": c2_late["delta_late_plus_Hz_vs_original_frozen"],
            "status": "survived",
            "source": str(absolute_source("47_scores")),
        },
        {
            "metric": "primary_growth_delta_vs_original",
            "C2_value": c2_cmb["chi2_growth_primary"],
            "original_value": original_cmb["chi2_growth_primary"],
            "delta": statuses["48_status"]["C2_delta_growth_primary_vs_original"],
            "status": "survived",
            "source": str(absolute_source("48_scores")),
        },
        {
            "metric": "full_shape_growth_delta_vs_original",
            "C2_value": c2_cmb["chi2_growth_full_shape_only"],
            "original_value": original_cmb["chi2_growth_full_shape_only"],
            "delta": statuses["48_status"]["C2_delta_growth_full_shape_vs_original"],
            "status": "survived",
            "source": str(absolute_source("48_scores")),
        },
        {
            "metric": "compressed_CMB_delta_vs_original",
            "C2_value": c2_cmb["chi2_CMB_repaired"],
            "original_value": original_cmb["chi2_CMB_repaired"],
            "delta": statuses["48_status"]["C2_delta_CMB_vs_original"],
            "status": "survived",
            "source": str(absolute_source("48_scores")),
        },
        {
            "metric": "Hz_delta_vs_original",
            "C2_value": c2_cmb["chi2_Hz_suggested"],
            "original_value": original_cmb["chi2_Hz_suggested"],
            "delta": statuses["48_status"]["C2_delta_Hz_vs_original"],
            "status": "survived",
            "source": str(absolute_source("48_scores")),
        },
        {
            "metric": "total_growth_CMB_Hz_delta_vs_original",
            "C2_value": c2_cmb["chi2_primary_growth_plus_CMB_plus_Hz"],
            "original_value": original_cmb["chi2_primary_growth_plus_CMB_plus_Hz"],
            "delta": statuses["48_status"]["C2_delta_total_vs_original"],
            "status": "survived",
            "source": str(absolute_source("48_scores")),
        },
    ]


def still_borrowed_rows() -> list[dict[str, Any]]:
    return [
        {
            "gap": "parent_activation_derivation",
            "status": "missing",
            "why_it_matters": "p=3 was selected by regularity gate, not derived from Gamma/S_memory/psi/C dynamics",
            "required_for_promotion": "derive F(N)=1-exp[-(N/u3)^3] or a replacement as a parent solution",
        },
        {
            "gap": "amplitude_origin",
            "status": "missing",
            "why_it_matters": "b_mem remains the checkpoint-38 frozen calibrated amplitude",
            "required_for_promotion": "derive b_mem from a memory-source or trace-budget invariant",
        },
        {
            "gap": "transition_scale_origin",
            "status": "missing",
            "why_it_matters": "u3 is fixed by original N50, which is inherited from the old closure branch",
            "required_for_promotion": "derive N50/u3 from parent invariants or predeclare a theory value",
        },
        {
            "gap": "perturbation_and_lensing_closure",
            "status": "missing",
            "why_it_matters": "CMB support would still import GR/quintessence perturbations",
            "required_for_promotion": "derive metric potentials, sound speed, anisotropic stress, conservation, and lensing response",
        },
        {
            "gap": "official_CMB_likelihood",
            "status": "missing",
            "why_it_matters": "compressed distance priors are not official spectra/lensing",
            "required_for_promotion": "run official fixed-parameter spectra/lensing after perturbation closure and baseline reproduction",
        },
        {
            "gap": "fresh_independent_holdout",
            "status": "missing",
            "why_it_matters": "current checks are internal guardrails, some reusing previously touched datasets",
            "required_for_promotion": "predeclare and run a genuinely fresh holdout with no rescue",
        },
        {
            "gap": "local_GR_PPN_connection",
            "status": "missing",
            "why_it_matters": "regularized cosmology is not yet tied to the local GR/PPN reduction branch",
            "required_for_promotion": "show why the same parent sector is locally silent but cosmologically active",
        },
    ]


def claim_language_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim": "C2-safe activation repair survived fixed-row internal guardrails",
            "status": "allowed",
            "replacement_if_forbidden": "same",
            "reason": "matches checkpoints 46-48",
        },
        {
            "claim": "C2 repair is supported by CMB",
            "status": "forbidden",
            "replacement_if_forbidden": "C2 repair survived compressed-CMB distance guardrail",
            "reason": "compressed prior is not official spectra/lensing and the row is calibrated closure",
        },
        {
            "claim": "C2 repair beats LCDM",
            "status": "forbidden",
            "replacement_if_forbidden": "standard baselines remain references; model selection is invalid here",
            "reason": "frozen closure rows and compressed CMB calibration are not a fair model-selection comparison",
        },
        {
            "claim": "activation law is derived",
            "status": "forbidden",
            "replacement_if_forbidden": "activation law is regularity-selected and empirically smoke-tested",
            "reason": "p=3 and u3 are not derived from parent MTS variables",
        },
        {
            "claim": "official CMB is solved",
            "status": "forbidden",
            "replacement_if_forbidden": "official CMB remains a future kill-screen/support gate",
            "reason": "perturbation/lensing closure and official likelihood are missing",
        },
    ]


def promotion_ladder_rows() -> list[dict[str, Any]]:
    return [
        {
            "stage": 0,
            "name": "regularized_closure_candidate",
            "current_status": "current_stage_retained",
            "requirement": "regularity fix plus no-rescue internal guardrail survival",
            "claim_level": "internal closure candidate",
        },
        {
            "stage": 1,
            "name": "parent_activation_law",
            "current_status": "missing",
            "requirement": "derive p=3/u3/b_mem or replacements from parent equations",
            "claim_level": "partial theory spine if passed",
        },
        {
            "stage": 2,
            "name": "perturbation_lensing_closure",
            "current_status": "missing",
            "requirement": "derive scalar/metric/lensing response without GR import",
            "claim_level": "support-capable CMB setup if passed",
        },
        {
            "stage": 3,
            "name": "fresh_or_official_holdout",
            "current_status": "not_run",
            "requirement": "predeclared external holdout or official spectra/lensing fixed-row test",
            "claim_level": "empirical stress result if passed",
        },
        {
            "stage": 4,
            "name": "unified_field_theory_promotion",
            "current_status": "not_available",
            "requirement": "connect cosmology activation to local GR/PPN, galaxies, conservation, and parent action",
            "claim_level": "serious field-theory candidate",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "C2_regularized_route_status",
            "status": "retained_regularized_closure_candidate_not_evidence",
            "evidence": "C2 repair fixes the scalar regularity snag and survives late-background/growth/CMB/H(z) guardrails",
            "next_action": "attempt parent activation law derivation rather than more internal scoring",
        },
        {
            "decision": "support_claim_status",
            "status": "forbidden",
            "evidence": "activation, amplitude, perturbations, official likelihood, fresh holdout, and local-GR link remain missing",
            "next_action": "keep private closure language",
        },
        {
            "decision": "recommended_next_target",
            "status": "50-parent-activation-law-attempt.md",
            "evidence": "C2 closure has survived enough internal guardrails; the next bottleneck is derivation, not another nearby score",
            "next_action": "try to derive or reject the p=3 activation law from parent memory variables",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="C2 regularized closure ledger.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    source_register = source_register_rows()
    statuses = {key: load_json(key) for key in SOURCE_PATHS if key.endswith("_status")}
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or POST_CHECKPOINT / "runs" / f"{timestamp}-C2-regularized-closure-ledger"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    fixes = fix_survival_rows(statuses)
    metrics = surviving_metric_rows(statuses)
    borrowed = still_borrowed_rows()
    claims = claim_language_rows()
    ladder = promotion_ladder_rows()
    decisions = decision_rows()

    write_csv(results_dir / "source_checkpoint_register.csv", source_register, list(source_register[0].keys()))
    write_csv(results_dir / "regularity_fix_survival_ledger.csv", fixes, list(fixes[0].keys()))
    write_csv(results_dir / "surviving_metric_ledger.csv", metrics, list(metrics[0].keys()))
    write_csv(results_dir / "still_borrowed_missing_gates.csv", borrowed, list(borrowed[0].keys()))
    write_csv(results_dir / "claim_language_ledger.csv", claims, list(claims[0].keys()))
    write_csv(results_dir / "promotion_ladder.csv", ladder, list(ladder[0].keys()))
    write_csv(results_dir / "decision.csv", decisions, list(decisions[0].keys()))

    status = {
        "status": "complete_C2_regularized_closure_ledger",
        "readout": "C2_regularized_closure_candidate_retained_not_evidence_parent_derivation_next",
        "recommendation": "attempt_parent_activation_law_next",
        "next_target": "50-parent-activation-law-attempt.md",
        "fix_survival_rows": len(fixes),
        "surviving_metric_rows": len(metrics),
        "missing_promotion_gates": len(borrowed),
        "support_claim_allowed": False,
        "public_claim_allowed": False,
        "key_metrics": {
            "C2_delta_late_plus_Hz_vs_original": statuses["47_status"]["best_repair_delta_late_plus_Hz_vs_original"],
            "C2_delta_growth_primary_vs_original": statuses["48_status"]["C2_delta_growth_primary_vs_original"],
            "C2_delta_growth_full_shape_vs_original": statuses["48_status"]["C2_delta_growth_full_shape_vs_original"],
            "C2_delta_CMB_vs_original": statuses["48_status"]["C2_delta_CMB_vs_original"],
            "C2_delta_Hz_vs_original": statuses["48_status"]["C2_delta_Hz_vs_original"],
            "C2_delta_total_vs_original": statuses["48_status"]["C2_delta_total_vs_original"],
        },
        "outputs": {
            "source_checkpoint_register": str(results_dir / "source_checkpoint_register.csv"),
            "regularity_fix_survival_ledger": str(results_dir / "regularity_fix_survival_ledger.csv"),
            "surviving_metric_ledger": str(results_dir / "surviving_metric_ledger.csv"),
            "still_borrowed_missing_gates": str(results_dir / "still_borrowed_missing_gates.csv"),
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
